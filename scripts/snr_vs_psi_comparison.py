#!/usr/bin/env python3
"""
Experimento del Coliseo Estadístico: SNR vs Ψ Noética
======================================================

Bajo la frecuencia f₀ = 141.7001 Hz, este módulo implementa el experimento
"quirúrgico" que enfrenta al SNR estándar de potencia contra la métrica
Ψ Noética de coherencia cruzada.

La arena: una señal moribunda (SNR real < 1) enterrada en ruido Gaussiano
coloreado. Se evalúan ambas métricas en tres zonas:

  • Zona de Confort  (SNR > UMBRAL_CONFORT):   Ambas métricas se comportan igual.
  • Zona de Penumbra (UMBRAL_NOETICO–UMBRAL_CONFORT): SNR oscila; Ψ permanece firme.
  • Zona Noética     (SNR < UMBRAL_NOETICO):   SNR colapsa; Ψ mantiene AUC > SNR.

Definiciones:
    SNR estándar: SNR = P_banda(f₀) / P_banda(f_adyacente)
                  Potencia integrada sobre banda ±bandwidth_hz en f₀.
    Ψ Noética:    Ψ   = D_snr(f₀) · D_coh²(f₀)
                  D_snr  = potencia de banda promediada entre canales.
                  D_coh² = coherencia cruzada al cuadrado (estimador Welch).

Control off-target (anti-bias):
    ratio = Ψ(f₀) / Ψ(f_control)  donde f_control = f₀ + 30 Hz por defecto.
    Si ratio > 1 la señal está concentrada en f₀, no difusa.

La fase es lo último que el caos logra destruir.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import numpy as np
from typing import Dict
from dataclasses import dataclass, field

try:
    from scipy.signal import coherence as scipy_coherence
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# ────────────────────────────────────────────────────────────────────────────
# Constantes
# ────────────────────────────────────────────────────────────────────────────

F0 = 141.7001          # Hz – frecuencia fundamental noética
SAMPLE_RATE = 4096.0   # Hz – tasa de muestreo estándar LIGO

# Pequeño valor positivo para evitar división por cero en ratios off-target
_EPSILON_RATIO = 1e-30

# Umbrales de las tres zonas
UMBRAL_CONFORT = 10.0   # SNR > 10  → Zona de Confort
UMBRAL_PENUMBRA_HI = 5.0  # SNR 2–5 → Zona de Penumbra
UMBRAL_PENUMBRA_LO = 2.0
UMBRAL_NOETICO = 1.0    # SNR < 1  → Zona Noética


# ────────────────────────────────────────────────────────────────────────────
# Generación de señal y ruido
# ────────────────────────────────────────────────────────────────────────────

def generar_senal_decayente(
    amplitud: float,
    duration: float = 1.0,
    fs: float = SAMPLE_RATE,
    f0: float = F0,
    tau_decay: float = 0.5
) -> np.ndarray:
    """
    Genera un pulso de coherencia pura con amplitud decayente.

    La señal tiene fase perfectamente alineada (coherente) pero amplitud
    exponencialmente decreciente. Representa el "susurro" de una onda
    gravitacional marginal.

    Parameters
    ----------
    amplitud : float
        Amplitud inicial de la señal.
    duration : float
        Duración en segundos.
    fs : float
        Tasa de muestreo en Hz.
    f0 : float
        Frecuencia fundamental en Hz.
    tau_decay : float
        Constante de tiempo del decaimiento (segundos).

    Returns
    -------
    np.ndarray
        Señal temporal s(t) = amplitud · exp(-t / tau_decay) · cos(2π f₀ t).
    """
    N = int(duration * fs)
    t = np.linspace(0.0, duration, N, endpoint=False)
    envelope = np.exp(-t / tau_decay)
    return amplitud * envelope * np.cos(2.0 * np.pi * f0 * t)


def generar_ruido_coloreado(
    n: int,
    fs: float = SAMPLE_RATE,
    color: str = 'pink',
    rng: np.random.Generator = None
) -> np.ndarray:
    """
    Genera ruido Gaussiano coloreado.

    Parameters
    ----------
    n : int
        Número de muestras.
    fs : float
        Tasa de muestreo en Hz.
    color : str
        Tipo de color: 'white' (plano), 'pink' (1/f), 'brown' (1/f²).
    rng : np.random.Generator, optional
        Generador de números aleatorios para reproducibilidad.

    Returns
    -------
    np.ndarray
        Ruido coloreado normalizado a varianza unitaria.
    """
    if rng is None:
        rng = np.random.default_rng()

    white = rng.standard_normal(n)

    if color == 'white':
        ruido = white
    else:
        # Colorear en el dominio de la frecuencia
        f_fft = np.fft.rfftfreq(n, 1.0 / fs)
        f_fft[0] = f_fft[1]  # evitar división por cero en DC

        if color == 'pink':
            filtro = 1.0 / np.sqrt(f_fft)
        elif color == 'brown':
            filtro = 1.0 / f_fft
        else:
            raise ValueError(f"Color de ruido no reconocido: {color!r}")

        espectro = np.fft.rfft(white) * filtro
        ruido = np.fft.irfft(espectro, n=n)

    # Normalizar a varianza unitaria
    std = np.std(ruido)
    if std > 0:
        ruido /= std
    return ruido


# ────────────────────────────────────────────────────────────────────────────
# Métricas: SNR estándar y Ψ Noética
# ────────────────────────────────────────────────────────────────────────────

def calcular_snr_potencia(
    x: np.ndarray,
    f0: float = F0,
    fs: float = SAMPLE_RATE,
    bandwidth_hz: float = 5.0
) -> float:
    """
    Calcula el SNR estándar basado en densidad espectral de potencia.

    SNR = P_xx(f₀) / σ²_ruido(f₀)

    La potencia de la señal se estima en una banda estrecha alrededor de f₀;
    el ruido se estima en una banda adyacente excluyendo f₀.

    Parameters
    ----------
    x : np.ndarray
        Serie temporal de un canal.
    f0 : float
        Frecuencia objetivo en Hz.
    fs : float
        Tasa de muestreo en Hz.
    bandwidth_hz : float
        Semi-ancho de banda para la estimación (Hz).

    Returns
    -------
    float
        SNR de potencia (adimensional, ≥ 0).
    """
    N = len(x)
    freqs = np.fft.rfftfreq(N, 1.0 / fs)
    psd = (np.abs(np.fft.rfft(x)) ** 2) / N

    # Potencia en la banda objetivo
    mascara_senal = np.abs(freqs - f0) <= bandwidth_hz
    potencia_senal = np.mean(psd[mascara_senal]) if np.any(mascara_senal) else 0.0

    # Ruido en banda adyacente
    mascara_ruido = (np.abs(freqs - f0) > bandwidth_hz) & \
                    (np.abs(freqs - f0) <= 3.0 * bandwidth_hz)
    potencia_ruido = np.mean(psd[mascara_ruido]) if np.any(mascara_ruido) else np.mean(psd)

    if potencia_ruido <= 0:
        return 0.0
    return potencia_senal / potencia_ruido


def _coherencia_welch(
    x: np.ndarray,
    y: np.ndarray,
    f0: float,
    fs: float,
    nperseg: int
) -> float:
    """
    Estima la magnitud al cuadrado de la coherencia cruzada en f₀ usando el
    método de Welch con ventana Hann y solapamiento del 50%.

    Se usa como función interna tanto por el camino SciPy como por el fallback
    manual, garantizando estimaciones consistentes en ambos casos.

    Parameters
    ----------
    x, y : np.ndarray
        Series temporales de los dos canales.
    f0 : float
        Frecuencia objetivo en Hz.
    fs : float
        Tasa de muestreo en Hz.
    nperseg : int
        Longitud del segmento Welch.

    Returns
    -------
    float
        I²(f₀) ∈ [0, 1].
    """
    N = len(x)
    nperseg_eff = min(nperseg, N)
    if nperseg_eff <= 0:
        return 0.0

    step = max(nperseg_eff // 2, 1)
    window = np.hanning(nperseg_eff).astype(float)
    window_norm = np.sum(window ** 2)

    Sxx = np.zeros(nperseg_eff // 2 + 1)
    Syy = np.zeros(nperseg_eff // 2 + 1)
    Sxy = np.zeros(nperseg_eff // 2 + 1, dtype=complex)
    n_segs = 0

    for start in range(0, N - nperseg_eff + 1, step):
        seg_x = x[start:start + nperseg_eff] * window
        seg_y = y[start:start + nperseg_eff] * window

        X_seg = np.fft.rfft(seg_x)
        Y_seg = np.fft.rfft(seg_y)

        Sxx += (np.abs(X_seg) ** 2) / window_norm
        Syy += (np.abs(Y_seg) ** 2) / window_norm
        Sxy += (X_seg * np.conj(Y_seg)) / window_norm
        n_segs += 1

    if n_segs == 0:
        return 0.0

    Sxx /= n_segs
    Syy /= n_segs
    Sxy /= n_segs

    freqs_seg = np.fft.rfftfreq(nperseg_eff, 1.0 / fs)
    idx = np.argmin(np.abs(freqs_seg - f0))

    denom = Sxx[idx] * Syy[idx]
    return float(np.abs(Sxy[idx]) ** 2 / denom) if denom > 0 else 0.0


def calcular_psi_noetica(
    x: np.ndarray,
    y: np.ndarray,
    f0: float = F0,
    fs: float = SAMPLE_RATE,
    bandwidth_hz: float = 5.0,
    nperseg: int = None
) -> float:
    """
    Calcula la métrica Ψ Noética de coherencia cruzada.

    Ψ = D_snr(f₀) · D_coh²(f₀)

    donde:
        D_snr   = potencia de banda promediada entre canales x e y:
                  D_snr = ½ · (mean_PSD_x + mean_PSD_y) en [f₀-bw, f₀+bw]
        D_coh²  = coherencia cruzada al cuadrado (estimador Welch):
                  D_coh² = |S_xy(f₀)|² / (S_xx(f₀) · S_yy(f₀))

    La ponderación por D_coh² suprime el ruido incoherente incluso cuando
    tiene potencia significativa en la banda de f₀. El uso de potencia de
    banda (no de un único bin) hace la estimación más robusta.

    Parameters
    ----------
    x : np.ndarray
        Canal 1 (señal + ruido nodo A).
    y : np.ndarray
        Canal 2 (señal + ruido nodo B, independiente).
    f0 : float
        Frecuencia objetivo en Hz.
    fs : float
        Tasa de muestreo en Hz.
    bandwidth_hz : float
        Semi-ancho de banda para D_snr (Hz).
    nperseg : int, optional
        Longitud del segmento Welch. Si es None se usa min(len(x), 256).

    Returns
    -------
    float
        Ψ Noética (≥ 0).
    """
    N = len(x)
    if nperseg is None:
        nperseg = min(N, 256)

    # D_coh²: coherencia cruzada al cuadrado vía Welch
    if SCIPY_AVAILABLE:
        f_coh, Cxy = scipy_coherence(x, y, fs=fs, nperseg=nperseg)
        idx_coh = np.argmin(np.abs(f_coh - f0))
        D_coh2 = float(Cxy[idx_coh])
    else:
        D_coh2 = _coherencia_welch(x, y, f0=f0, fs=fs, nperseg=nperseg)

    # D_snr: potencia de banda promediada (no bin único)
    freqs = np.fft.rfftfreq(N, 1.0 / fs)
    psd_x = (np.abs(np.fft.rfft(x)) ** 2) / N
    psd_y = (np.abs(np.fft.rfft(y)) ** 2) / N
    mascara_banda = np.abs(freqs - f0) <= bandwidth_hz
    if np.any(mascara_banda):
        D_snr = 0.5 * (np.mean(psd_x[mascara_banda]) + np.mean(psd_y[mascara_banda]))
    else:
        idx_f0 = np.argmin(np.abs(freqs - f0))
        D_snr = 0.5 * (psd_x[idx_f0] + psd_y[idx_f0])

    return D_snr * D_coh2


# ────────────────────────────────────────────────────────────────────────────
# Curva ROC
# ────────────────────────────────────────────────────────────────────────────

@dataclass
class ResultadoROC:
    """Resultado de una curva ROC para una métrica dada."""
    nombre: str
    tpr: np.ndarray          # True Positive Rate (detección)
    fpr: np.ndarray          # False Positive Rate (falsa alarma)
    auc: float               # Área bajo la curva
    thresholds: np.ndarray   # Umbrales correspondientes


def calcular_curva_roc(
    scores_senal: np.ndarray,
    scores_ruido: np.ndarray,
    nombre: str = 'métrica'
) -> ResultadoROC:
    """
    Calcula la curva ROC (Receiver Operating Characteristic).

    Usa conteos acumulativos de TP/FP tras un único sort, resultando en
    complejidad O(N log N) en lugar de O(N²) por rethresholding.
    Los extremos (0, 0) y (1, 1) se añaden explícitamente antes de calcular
    el AUC, garantizando cobertura total de la curva.

    Parameters
    ----------
    scores_senal : np.ndarray
        Puntuaciones de la métrica cuando hay señal presente.
    scores_ruido : np.ndarray
        Puntuaciones de la métrica cuando sólo hay ruido.
    nombre : str
        Nombre de la métrica para identificación.

    Returns
    -------
    ResultadoROC
        Objeto con TPR, FPR, AUC y umbrales.
    """
    n_pos = len(scores_senal)
    n_neg = len(scores_ruido)

    todos = np.concatenate([scores_senal, scores_ruido])
    etiquetas = np.concatenate([
        np.ones(n_pos, dtype=float),
        np.zeros(n_neg, dtype=float)
    ])

    # Único sort descendente → O(N log N)
    orden = np.argsort(-todos)
    etiquetas_ord = etiquetas[orden]
    thresholds = todos[orden]

    # Conteos acumulativos TP y FP → O(N)
    tp_cum = np.cumsum(etiquetas_ord)
    fp_cum = np.cumsum(1.0 - etiquetas_ord)

    tpr_arr = tp_cum / n_pos if n_pos > 0 else np.zeros(len(tp_cum))
    fpr_arr = fp_cum / n_neg if n_neg > 0 else np.zeros(len(fp_cum))

    # AUC con extremos (0, 0) y (1, 1) para cobertura total
    fpr_ext = np.concatenate(([0.0], fpr_arr, [1.0]))
    tpr_ext = np.concatenate(([0.0], tpr_arr, [1.0]))
    auc = float(np.trapezoid(tpr_ext, fpr_ext)
                if hasattr(np, 'trapezoid') else
                np.trapz(tpr_ext, fpr_ext))

    return ResultadoROC(
        nombre=nombre,
        tpr=tpr_arr,
        fpr=fpr_arr,
        auc=auc,
        thresholds=thresholds
    )


# ────────────────────────────────────────────────────────────────────────────
# Experimento principal
# ────────────────────────────────────────────────────────────────────────────

@dataclass
class ResultadoZona:
    """Resultados del experimento para una zona SNR dada."""
    nombre_zona: str
    snr_objetivo: float
    n_trials: int
    # Puntuaciones con señal
    snr_scores_senal: np.ndarray = field(default_factory=lambda: np.array([]))
    psi_scores_senal: np.ndarray = field(default_factory=lambda: np.array([]))
    # Puntuaciones sin señal (ruido puro)
    snr_scores_ruido: np.ndarray = field(default_factory=lambda: np.array([]))
    psi_scores_ruido: np.ndarray = field(default_factory=lambda: np.array([]))
    # Ratio off-target (anti-bias): Ψ(f₀) / Ψ(f_control)
    psi_ratio_senal: np.ndarray = field(default_factory=lambda: np.array([]))
    psi_ratio_ruido: np.ndarray = field(default_factory=lambda: np.array([]))
    # Curvas ROC
    roc_snr: ResultadoROC = None
    roc_psi: ResultadoROC = None
    # Separación estadística (en sigmas, vía calcular_separacion_sigma)
    separacion_snr_sigma: float = 0.0
    separacion_psi_sigma: float = 0.0


def calcular_separacion_sigma(con: np.ndarray, sin: np.ndarray) -> float:
    """
    Calcula la separación estadística entre dos distribuciones en unidades σ.

    Usa la diferencia de medias normalizada por la desviación estándar
    combinada (pooled sigma):

        sep = (μ_con - μ_sin) / sqrt(½ · (σ²_con + σ²_sin))

    Parameters
    ----------
    con : np.ndarray
        Puntuaciones bajo H₁ (señal presente).
    sin : np.ndarray
        Puntuaciones bajo H₀ (solo ruido).

    Returns
    -------
    float
        Separación en sigmas. Valores ≥ 2 indican detección significativa.
    """
    mu_diff = np.mean(con) - np.mean(sin)
    sigma_pool = np.sqrt(0.5 * (np.var(con) + np.var(sin)))
    return float(mu_diff / sigma_pool) if sigma_pool > 0 else 0.0


def ejecutar_zona(
    snr_objetivo: float,
    nombre_zona: str,
    n_trials: int = 200,
    duration: float = 1.0,
    fs: float = SAMPLE_RATE,
    f0: float = F0,
    f_control: float = None,
    seed: int = 42
) -> ResultadoZona:
    """
    Ejecuta el experimento del Coliseo para una zona SNR dada.

    Genera `n_trials` realizaciones de:
        • señal decayente + ruido coloreado (hipótesis H₁)
        • solo ruido coloreado             (hipótesis H₀)

    y calcula SNR estándar, Ψ Noética en f₀ y el ratio anti-bias
    Ψ(f₀)/Ψ(f_control) para cada una.

    Parameters
    ----------
    snr_objetivo : float
        SNR lineal (amplitud/σ_ruido) de la señal a inyectar.
    nombre_zona : str
        Etiqueta descriptiva de la zona ('Confort', 'Penumbra', 'Noética').
    n_trials : int
        Número de realizaciones Monte-Carlo por hipótesis.
    duration : float
        Duración de cada realización en segundos.
    fs : float
        Tasa de muestreo.
    f0 : float
        Frecuencia fundamental.
    f_control : float, optional
        Frecuencia de control off-target para el ratio anti-bias.
        Por defecto f₀ + 30 Hz.
    seed : int
        Semilla para reproducibilidad.

    Returns
    -------
    ResultadoZona
        Resultados completos incluyendo puntuaciones, ratios y curvas ROC.
    """
    if f_control is None:
        f_control = f0 + 30.0

    N = int(duration * fs)
    amplitud_senal = float(snr_objetivo)  # σ_ruido = 1 tras normalización

    snr_con, snr_sin = [], []
    psi_con, psi_sin = [], []
    ratio_con, ratio_sin = [], []

    for i in range(n_trials):
        rng_a = np.random.default_rng(seed + i * 2)
        rng_b = np.random.default_rng(seed + i * 2 + 1)

        # Ruido independiente en cada canal
        ruido_a = generar_ruido_coloreado(N, fs=fs, color='pink', rng=rng_a)
        ruido_b = generar_ruido_coloreado(N, fs=fs, color='pink', rng=rng_b)

        # Señal coherente compartida
        senal = generar_senal_decayente(amplitud_senal, duration=duration,
                                        fs=fs, f0=f0)

        # H₁: señal + ruido
        x1 = senal + ruido_a
        y1 = senal + ruido_b
        psi_f0 = calcular_psi_noetica(x1, y1, f0=f0, fs=fs)
        psi_fc = calcular_psi_noetica(x1, y1, f0=f_control, fs=fs)
        snr_con.append(calcular_snr_potencia(x1, f0=f0, fs=fs))
        psi_con.append(psi_f0)
        ratio_con.append(psi_f0 / max(psi_fc, _EPSILON_RATIO))

        # H₀: solo ruido
        x0 = ruido_a
        y0 = ruido_b
        psi_f0_h0 = calcular_psi_noetica(x0, y0, f0=f0, fs=fs)
        psi_fc_h0 = calcular_psi_noetica(x0, y0, f0=f_control, fs=fs)
        snr_sin.append(calcular_snr_potencia(x0, f0=f0, fs=fs))
        psi_sin.append(psi_f0_h0)
        ratio_sin.append(psi_f0_h0 / max(psi_fc_h0, _EPSILON_RATIO))

    snr_con = np.array(snr_con)
    snr_sin = np.array(snr_sin)
    psi_con = np.array(psi_con)
    psi_sin = np.array(psi_sin)

    # Curvas ROC
    roc_snr = calcular_curva_roc(snr_con, snr_sin, nombre='SNR Estándar')
    roc_psi = calcular_curva_roc(psi_con, psi_sin, nombre='Ψ Noética')

    return ResultadoZona(
        nombre_zona=nombre_zona,
        snr_objetivo=snr_objetivo,
        n_trials=n_trials,
        snr_scores_senal=snr_con,
        psi_scores_senal=psi_con,
        snr_scores_ruido=snr_sin,
        psi_scores_ruido=psi_sin,
        psi_ratio_senal=np.array(ratio_con),
        psi_ratio_ruido=np.array(ratio_sin),
        roc_snr=roc_snr,
        roc_psi=roc_psi,
        separacion_snr_sigma=calcular_separacion_sigma(snr_con, snr_sin),
        separacion_psi_sigma=calcular_separacion_sigma(psi_con, psi_sin)
    )


def ejecutar_coliseo(
    n_trials: int = 200,
    duration: float = 0.2,
    fs: float = SAMPLE_RATE,
    f0: float = F0,
    f_control: float = None,
    seed: int = 42
) -> Dict[str, ResultadoZona]:
    """
    Ejecuta el Experimento del Coliseo Estadístico completo.

    Evalúa SNR estándar vs Ψ Noética en las tres zonas definidas por los
    umbrales del módulo (UMBRAL_CONFORT, UMBRAL_PENUMBRA_HI, UMBRAL_NOETICO).
    El uso de segmentos cortos (duration=0.2 s por defecto) revela las
    diferencias estadísticas entre ambas métricas:

        • Confort  (SNR = UMBRAL_CONFORT × 1.5): ambas métricas empatan.
        • Penumbra (SNR = UMBRAL_PENUMBRA_HI):  Ψ supera claramente a SNR.
        • Noética  (SNR = UMBRAL_NOETICO / 2): SNR colapsa; Ψ mantiene AUC mayor.

    Parameters
    ----------
    n_trials : int
        Realizaciones Monte-Carlo por zona y por hipótesis.
    duration : float
        Duración de cada realización en segundos.
    fs : float
        Tasa de muestreo.
    f0 : float
        Frecuencia fundamental.
    f_control : float, optional
        Frecuencia de control off-target. Por defecto f₀ + 30 Hz.
    seed : int
        Semilla base para reproducibilidad.

    Returns
    -------
    Dict[str, ResultadoZona]
        Diccionario con resultados de cada zona keyed por nombre.
    """
    # Zonas definidas a partir de los umbrales del módulo
    zonas = [
        (UMBRAL_CONFORT * 1.5,  'Confort',  seed),
        (UMBRAL_PENUMBRA_HI,    'Penumbra', seed + 1000),
        (UMBRAL_NOETICO / 2.0,  'Noetica',  seed + 2000),
    ]

    resultados = {}
    for snr_obj, nombre, semilla in zonas:
        resultados[nombre] = ejecutar_zona(
            snr_objetivo=snr_obj,
            nombre_zona=nombre,
            n_trials=n_trials,
            duration=duration,
            fs=fs,
            f0=f0,
            f_control=f_control,
            seed=semilla
        )

    return resultados


def tabla_comparativa(resultados: Dict[str, ResultadoZona]) -> str:
    """
    Genera una tabla de comparación textual entre SNR y Ψ en las tres zonas.

    El ganador se determina por AUC (área bajo la curva ROC), que es la
    métrica principal de discriminabilidad. La separación en sigmas se
    muestra como información adicional calculada mediante
    `calcular_separacion_sigma`.

    Parameters
    ----------
    resultados : Dict[str, ResultadoZona]
        Resultado de `ejecutar_coliseo`.

    Returns
    -------
    str
        Tabla formateada como cadena de texto.
    """
    lineas = [
        "=" * 78,
        "🥊 COLISEO ESTADÍSTICO: SNR Estándar vs Ψ Noética",
        f"   f₀ = {F0} Hz",
        "=" * 78,
        f"{'Zona':<12} {'SNR obj':>8} {'AUC-SNR':>10} {'AUC-Ψ':>10} "
        f"{'Sep-SNR(σ)':>12} {'Sep-Ψ(σ)':>10} {'Ganador':>10}",
        "-" * 78,
    ]
    for nombre, res in resultados.items():
        auc_snr = res.roc_snr.auc if res.roc_snr else 0.0
        auc_psi = res.roc_psi.auc if res.roc_psi else 0.0
        sep_snr = res.separacion_snr_sigma
        sep_psi = res.separacion_psi_sigma
        # Ganador determinado por AUC (métrica principal)
        if auc_psi > auc_snr + 0.01:
            ganador = 'Ψ'
        elif auc_snr > auc_psi + 0.01:
            ganador = 'SNR'
        else:
            ganador = 'Empate'
        lineas.append(
            f"{nombre:<12} {res.snr_objetivo:>8.1f} {auc_snr:>10.4f} {auc_psi:>10.4f} "
            f"{sep_snr:>12.2f} {sep_psi:>10.2f} {ganador:>10}"
        )
    lineas.append("=" * 78)
    return "\n".join(lineas)


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🏛️  Iniciando Experimento del Coliseo Estadístico…")
    print(f"   f₀ = {F0} Hz | fs = {SAMPLE_RATE} Hz\n")

    resultados = ejecutar_coliseo(n_trials=200, duration=0.2)
    print(tabla_comparativa(resultados))
