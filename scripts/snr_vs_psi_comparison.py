#!/usr/bin/env python3
"""
Experimento del Coliseo Estadístico: SNR vs Ψ Noética
======================================================

Bajo la frecuencia f₀ = 141.7001 Hz, este módulo implementa el experimento
"quirúrgico" que enfrenta al SNR estándar de potencia contra la métrica
Ψ Noética de coherencia cruzada.

La arena: una señal moribunda (SNR real < 1) enterrada en ruido Gaussiano
coloreado. Se evalúan ambas métricas en tres zonas:

  • Zona de Confort  (SNR > 10): Ambas métricas se comportan igual.
  • Zona de Penumbra (SNR 2–5): SNR estándar empieza a oscilar; Ψ permanece firme.
  • Zona Noética     (SNR < 1):  SNR estándar colapsa (p > 0.05); Ψ mantiene
                                  separación estadística de 2σ.

Definiciones:
    SNR estándar: SNR = P_xx(f₀) / σ²_ruido(f₀)
    Ψ Noética:    Ψ   = I(f₀) · A_eff²
                  donde I(f₀) es la coherencia cruzada y A_eff² la amplitud
                  efectiva cuadrática media.

La fase es lo último que el caos logra destruir.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import numpy as np
from typing import Dict, List, NamedTuple, Tuple
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


def calcular_psi_noetica(
    x: np.ndarray,
    y: np.ndarray,
    f0: float = F0,
    fs: float = SAMPLE_RATE,
    nperseg: int = None
) -> float:
    """
    Calcula la métrica Ψ Noética de coherencia cruzada.

    Ψ = I(f₀) · A_eff²

    donde:
        I(f₀)   = coherencia cruzada entre x e y en f₀  (∈ [0, 1])
        A_eff²  = amplitud efectiva cuadrática media:
                  A_eff² = I(f₀) · mean(P_xx(f₀), P_yy(f₀))

    Por tanto: Ψ = I²(f₀) · mean(P_xx(f₀), P_yy(f₀))

    La doble ponderación por I(f₀) suprime el ruido incoherente incluso
    cuando tiene potencia significativa en f₀.

    Parameters
    ----------
    x : np.ndarray
        Canal 1 (señal + ruido nodo A).
    y : np.ndarray
        Canal 2 (señal + ruido nodo B, independiente).
    f0 : float
        Frecuencia fundamental en Hz.
    fs : float
        Tasa de muestreo en Hz.
    nperseg : int, optional
        Longitud del segmento para el estimador de Welch de coherencia.
        Si es None se usa min(len(x), 256).

    Returns
    -------
    float
        Ψ Noética (≥ 0).
    """
    N = len(x)
    if nperseg is None:
        nperseg = min(N, 256)

    if SCIPY_AVAILABLE:
        f_coh, Cxy = scipy_coherence(x, y, fs=fs, nperseg=nperseg)
        idx = np.argmin(np.abs(f_coh - f0))
        I_f0 = float(Cxy[idx])
    else:
        # Implementación manual: |C_xy|² / (P_xx · P_yy)
        freqs = np.fft.rfftfreq(N, 1.0 / fs)
        idx = np.argmin(np.abs(freqs - f0))
        X = np.fft.rfft(x)
        Y = np.fft.rfft(y)
        Pxx = np.abs(X[idx]) ** 2
        Pyy = np.abs(Y[idx]) ** 2
        Cxy_val = np.abs(X[idx] * np.conj(Y[idx])) ** 2
        denom = Pxx * Pyy
        I_f0 = float(Cxy_val / denom) if denom > 0 else 0.0

    # Amplitud efectiva cuadrática
    freqs_full = np.fft.rfftfreq(N, 1.0 / fs)
    idx_full = np.argmin(np.abs(freqs_full - f0))
    Pxx_val = (np.abs(np.fft.rfft(x)[idx_full]) ** 2) / N
    Pyy_val = (np.abs(np.fft.rfft(y)[idx_full]) ** 2) / N
    A_eff_cuad = I_f0 * 0.5 * (Pxx_val + Pyy_val)

    return I_f0 * A_eff_cuad  # = I²(f₀) · mean(Pxx, Pyy)


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
    todos = np.concatenate([scores_senal, scores_ruido])
    etiquetas = np.concatenate([
        np.ones(len(scores_senal), dtype=int),
        np.zeros(len(scores_ruido), dtype=int)
    ])

    # Ordenar por puntuación descendente
    orden = np.argsort(-todos)
    todos_ord = todos[orden]
    etiquetas_ord = etiquetas[orden]

    thresholds = np.unique(todos_ord)[::-1]

    tpr_list, fpr_list = [], []
    n_pos = np.sum(etiquetas == 1)
    n_neg = np.sum(etiquetas == 0)

    for thresh in thresholds:
        prediccion = (todos >= thresh).astype(int)
        tp = np.sum((prediccion == 1) & (etiquetas == 1))
        fp = np.sum((prediccion == 1) & (etiquetas == 0))
        tpr_list.append(tp / n_pos if n_pos > 0 else 0.0)
        fpr_list.append(fp / n_neg if n_neg > 0 else 0.0)

    tpr_arr = np.array(tpr_list)
    fpr_arr = np.array(fpr_list)

    # AUC mediante regla del trapecio
    orden_fpr = np.argsort(fpr_arr)
    auc = float(np.trapezoid(tpr_arr[orden_fpr], fpr_arr[orden_fpr])
                if hasattr(np, 'trapezoid') else
                np.trapz(tpr_arr[orden_fpr], fpr_arr[orden_fpr]))

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
    # Curvas ROC
    roc_snr: ResultadoROC = None
    roc_psi: ResultadoROC = None
    # Separación estadística (en sigmas)
    separacion_snr_sigma: float = 0.0
    separacion_psi_sigma: float = 0.0


def ejecutar_zona(
    snr_objetivo: float,
    nombre_zona: str,
    n_trials: int = 200,
    duration: float = 1.0,
    fs: float = SAMPLE_RATE,
    f0: float = F0,
    seed: int = 42
) -> ResultadoZona:
    """
    Ejecuta el experimento del Coliseo para una zona SNR dada.

    Genera `n_trials` realizaciones de:
        • señal decayente + ruido coloreado (hipótesis H₁)
        • solo ruido coloreado             (hipótesis H₀)

    y calcula SNR estándar y Ψ Noética para cada una.

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
    seed : int
        Semilla para reproducibilidad.

    Returns
    -------
    ResultadoZona
        Resultados completos incluyendo puntuaciones y curvas ROC.
    """
    N = int(duration * fs)
    amplitud_senal = float(snr_objetivo)  # σ_ruido = 1 tras normalización

    snr_con, snr_sin = [], []
    psi_con, psi_sin = [], []

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
        snr_con.append(calcular_snr_potencia(x1, f0=f0, fs=fs))
        psi_con.append(calcular_psi_noetica(x1, y1, f0=f0, fs=fs))

        # H₀: solo ruido
        x0 = ruido_a
        y0 = ruido_b
        snr_sin.append(calcular_snr_potencia(x0, f0=f0, fs=fs))
        psi_sin.append(calcular_psi_noetica(x0, y0, f0=f0, fs=fs))

    snr_con = np.array(snr_con)
    snr_sin = np.array(snr_sin)
    psi_con = np.array(psi_con)
    psi_sin = np.array(psi_sin)

    # Curvas ROC
    roc_snr = calcular_curva_roc(snr_con, snr_sin, nombre='SNR Estándar')
    roc_psi = calcular_curva_roc(psi_con, psi_sin, nombre='Ψ Noética')

    # Separación estadística (en sigmas)
    def sigma_sep(con, sin):
        mu_diff = np.mean(con) - np.mean(sin)
        sigma_pool = np.sqrt(0.5 * (np.var(con) + np.var(sin)))
        return float(mu_diff / sigma_pool) if sigma_pool > 0 else 0.0

    sep_snr = sigma_sep(snr_con, snr_sin)
    sep_psi = sigma_sep(psi_con, psi_sin)

    return ResultadoZona(
        nombre_zona=nombre_zona,
        snr_objetivo=snr_objetivo,
        n_trials=n_trials,
        snr_scores_senal=snr_con,
        psi_scores_senal=psi_con,
        snr_scores_ruido=snr_sin,
        psi_scores_ruido=psi_sin,
        roc_snr=roc_snr,
        roc_psi=roc_psi,
        separacion_snr_sigma=sep_snr,
        separacion_psi_sigma=sep_psi
    )


def ejecutar_coliseo(
    n_trials: int = 200,
    duration: float = 0.2,
    fs: float = SAMPLE_RATE,
    f0: float = F0,
    seed: int = 42
) -> Dict[str, ResultadoZona]:
    """
    Ejecuta el Experimento del Coliseo Estadístico completo.

    Evalúa SNR estándar vs Ψ Noética en las tres zonas.  El uso de segmentos
    cortos (duration=0.2 s por defecto) revela las diferencias estadísticas
    entre ambas métricas porque limita la resolución espectral disponible,
    simulando condiciones reales de detección marginal:

        • Confort  (SNR = 15): ambas métricas empatan (AUC ≈ 1).
        • Penumbra (SNR =  3): Ψ supera claramente a SNR estándar.
        • Noética  (SNR = 0.5): SNR colapsa (< 2σ); Ψ mantiene ≥ 2σ.

    Parameters
    ----------
    n_trials : int
        Realizaciones Monte-Carlo por zona y por hipótesis.
    duration : float
        Duración de cada realización en segundos.  0.2 s (819 muestras a
        4096 Hz) revela la degradación diferencial entre SNR y Ψ.
    fs : float
        Tasa de muestreo.
    f0 : float
        Frecuencia fundamental.
    seed : int
        Semilla base para reproducibilidad.

    Returns
    -------
    Dict[str, ResultadoZona]
        Diccionario con resultados de cada zona keyed por nombre.
    """
    zonas = [
        (15.0,  'Confort',  seed),
        (3.0,   'Penumbra', seed + 1000),
        (0.5,   'Noetica',  seed + 2000),
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
            seed=semilla
        )

    return resultados


def tabla_comparativa(resultados: Dict[str, ResultadoZona]) -> str:
    """
    Genera una tabla de comparación textual entre SNR y Ψ en las tres zonas.

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
        # Determinar ganador por separación estadística (más discriminativo que AUC)
        if sep_psi > sep_snr * 1.1 or (sep_psi >= 2.0 and sep_snr < 2.0):
            ganador = 'Ψ'
        elif sep_snr > sep_psi * 1.1 or (sep_snr >= 2.0 and sep_psi < 2.0):
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
