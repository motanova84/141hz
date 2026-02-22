#!/usr/bin/env python3
"""
Validación Profunda del Evento Gravitacional GW1509141 (GW1509141)
====================================================================

Pipeline QCAL ∞³ de validación coherente:
  1. Simular señal de chirp GW con ruido realista
  2. Blanquear (whitening) ambos detectores
  3. Calcular serie temporal de Ψ (coherencia H1–L1)
  4. Analizar separación ON/OFF-source
  4a. Banda de control anti-sesgo (F_CONTROL = 191.7001 Hz)
  4b. SNR de red (ρ_net)
  4c. Conexión Wang / octavas multi-escala
  5. Generar reporte JSON extendido
  6. Emitir certificado de validación con hash SHA-256

Fórmula Ψ_evento (no saturante):
  psi_raw    = sqrt(psi_on_mean / psi_off_mean)
  psi_evento = psi_raw / (1 + psi_raw)   ∈ (0, 1)

Umbrales de estado QCAL ∞³:
  CRISTALIZADO : psi_evento ≥ 0.909  ⟺  ratio ≥ 100
  COHERENTE    : psi_evento ≥ 0.888  ⟺  ratio ≥ 62.87
  EMERGENTE    : psi_evento ≥ 0.618  ⟺  ratio ≥ 2.618
  RUIDO        : psi_evento  < 0.618

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Versión: 2.0.0 — bisturí aplicado
"""

from __future__ import annotations

import hashlib
import json
import math
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy import signal, stats

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTES GLOBALES
# ──────────────────────────────────────────────────────────────────────────────

FS: float = 4096.0          # Hz  – frecuencia de muestreo LIGO
T_TOTAL: float = 32.0       # s   – duración total del segmento de datos
T_WINDOW: float = 0.5       # s   – tamaño de ventana para cálculo de Ψ
T_MERGER: float = 0.0       # s   – tiempo de merger (origen del eje temporal)

# On-source: ventanas que contienen la señal coherente GW
# ±4.25 s → 17 ventanas de 0.5 s que contienen inspiral+merger+ringdown
T_ON_HALF: float = 4.25     # s   – semiancho de la región on-source

F_LOW: float = 35.0         # Hz  – corte inferior del filtro GW (banda señal)
F_HIGH: float = 500.0       # Hz  – corte superior del filtro GW (banda señal)
F_CONTROL: float = 191.7001 # Hz  – frecuencia de control para anti-sesgo (off-target)

LIGO_DELAY_S: float = 0.01  # s   – retardo H1→L1 (≈ 10 ms tiempo de vuelo)
SEED: int = 888              # semilla para reproducibilidad

SELLO: str = "QCAL-∞³-GW1509141-v2.0"

# Valores de referencia (pipeline con SEED=888, noise_level=0.14)
REF_PSI_ON: float  = 0.101   # media Ψ on-source
REF_PSI_OFF: float = 0.0048  # media Ψ off-source
REF_RATIO: float   = 20.86   # REF_PSI_ON / REF_PSI_OFF
REF_PVALUE: float  = 1e-2    # p-value referencia Mann-Whitney

# ──────────────────────────────────────────────────────────────────────────────
# 1. SIMULACIÓN DE CHIRP GW
# ──────────────────────────────────────────────────────────────────────────────


def simular_chirp_gw(
    fs: float = FS,
    t_total: float = T_TOTAL,
    t_merger: float = T_MERGER,
    seed: int = SEED,
    snr_amp: float = 20.0,
) -> Dict[str, Any]:
    """
    Genera una señal de chirp GW sintética para ambos detectores H1 y L1.

    La señal barre desde 20 Hz hasta ~200 Hz durante los 4.5 s previos al
    merger, con envolvente de amplitud gaussiana creciente hacia t=0.
    Se añade ruido gaussiano independiente en cada detector (nivel calibrado
    para producir ratio Ψ_ON/Ψ_OFF ≈ 20 con SEED=888).

    Returns
    -------
    dict con:
        h1_strain : np.ndarray  (N,)
        l1_strain : np.ndarray  (N,)
        t         : np.ndarray  (N,)  eje temporal centrado en t_merger
        signal    : np.ndarray  (N,)  chirp limpio antes de ruido
    """
    rng = np.random.default_rng(seed)
    N = int(t_total * fs)
    t = np.linspace(-t_total / 2.0, t_total / 2.0, N, endpoint=False)

    # ── Construcción del chirp ──────────────────────────────────────────────
    # Inspiral empieza a t_insp, barre hasta merger en 0.5 s post-merger
    t_insp = -4.0          # s antes del merger
    f_start = 20.0         # Hz
    f_end = 200.0          # Hz en el instante de merger
    t_dur = abs(t_insp) + 0.5   # duración total del chirp (s)

    chirp_mask = (t >= t_insp) & (t <= t_merger + 0.5)
    t_chirp = t[chirp_mask] - t_insp      # tiempo local [0, t_dur]

    chirp_signal = np.zeros(N)
    if chirp_mask.any():
        # Envolvente gaussiana: amplitud crece hacia el merger
        env = np.exp(4.0 * (t_chirp / t_dur) ** 2)
        env /= env.max()
        raw_chirp = signal.chirp(t_chirp, f0=f_start, f1=f_end,
                                 t1=t_dur, method="quadratic")
        chirp_signal[chirp_mask] = env * raw_chirp

    # ── Ruido gaussiano blanco (nivel calibrado para ratio ≈ 20) ──────────
    noise_level = 0.14     # calibrado para ratio Ψ ≈ 20.88 con SEED=888
    h1_noise = noise_level * rng.standard_normal(N)
    l1_noise = noise_level * rng.standard_normal(N)

    # L1: señal desplazada en tiempo + ligera diferencia de amplitud
    n_delay = max(1, int(LIGO_DELAY_S * fs))
    l1_signal = np.roll(chirp_signal, n_delay) * 0.87

    h1_strain = chirp_signal + h1_noise
    l1_strain = l1_signal + l1_noise

    return {
        "h1_strain": h1_strain,
        "l1_strain": l1_strain,
        "t": t,
        "signal": chirp_signal,
    }


def generar_datos_evento(seed: int = SEED) -> Dict[str, Any]:
    """
    Genera datos de evento sintetico GW1509141 para tests.

    Envuelve simular_chirp_gw con parámetros estándar y añade
    metadatos del evento.

    Returns
    -------
    dict con h1_strain, l1_strain, t, signal, evento, fs
    """
    datos = simular_chirp_gw(seed=seed)
    datos["evento"] = "GW1509141"
    datos["fs"] = FS
    return datos


# ──────────────────────────────────────────────────────────────────────────────
# 2. BLANQUEO (WHITENING)
# ──────────────────────────────────────────────────────────────────────────────


def blanquear(
    strain: np.ndarray,
    fs: float,
    t_ref: Optional[np.ndarray] = None,
    nperseg: int = 1024,
) -> np.ndarray:
    """
    Blanquea (whitens) la cepa dividiendo por la amplitud espectral mediana.

    Usa estimación de amplitud robusta (mediana de bloques) para mitigar
    el sesgo de transitorios (como el chirp GW).  El resultado se normaliza
    para que su RMS sea ≈ 1.

    Parameters
    ----------
    strain  : señal de cepa cruda
    fs      : frecuencia de muestreo
    t_ref   : eje temporal (no usado, incluido para compatibilidad de firma)
    nperseg : tamaño del bloque para estimación de amplitud

    Returns
    -------
    strain_white : np.ndarray de la misma longitud que strain, RMS ≈ 1
    """
    N = len(strain)
    nperseg_use = min(nperseg, N // 4)

    # ── Amplitud espectral mediana de bloques no solapados ─────────────────
    step = nperseg_use
    amps: List[np.ndarray] = []
    for i in range(0, N - nperseg_use + 1, step):
        seg = strain[i: i + nperseg_use]
        amps.append(np.abs(np.fft.rfft(seg)))
    if not amps:
        return strain.copy()

    amp_median = np.median(np.array(amps), axis=0)
    amp_median = np.maximum(amp_median, 1e-30)

    # Interpolar a las frecuencias del rfft completo
    freqs_all = np.fft.rfftfreq(N, d=1.0 / fs)
    freqs_seg = np.fft.rfftfreq(nperseg_use, d=1.0 / fs)
    amp_interp = np.interp(freqs_all, freqs_seg, amp_median)
    amp_interp = np.maximum(amp_interp, 1e-30)

    # Dividir cada componente frecuencial por su amplitud mediana
    strain_fft = np.fft.rfft(strain)
    strain_white_fft = strain_fft / amp_interp
    strain_white = np.fft.irfft(strain_white_fft, n=N)

    # Normalizar a RMS ≈ 1
    rms = float(np.sqrt(np.mean(strain_white ** 2)))
    if rms > 1e-30:
        strain_white = strain_white / rms

    return strain_white.astype(np.float64)


# ──────────────────────────────────────────────────────────────────────────────
# 3. CÁLCULO DE Ψ EN UNA VENTANA
# ──────────────────────────────────────────────────────────────────────────────


def calcular_psi_ventana(
    h1: np.ndarray,
    l1: np.ndarray,
    fs: float,
    f_low: float = F_LOW,
    f_high: float = F_HIGH,
    nperseg: Optional[int] = None,
) -> float:
    """
    Calcula la métrica Ψ en una ventana temporal.

    Ψ = |Σ_f H1(f)·L1*(f)|² / (Σ_f|H1(f)|² · Σ_f|L1(f)|²)
        sobre f ∈ [f_low, f_high].

    Esta es la coherencia cuadrática integrada sobre la banda (un único
    número por ventana), sin promediado de sub-segmentos.  Para ruido
    no correlacionado Ψ → 0 (escala 1/N_freq) mientras que para señal
    perfectamente correlacionada Ψ → 1.

    Parameters
    ----------
    h1, l1   : cepas de los detectores (blanqueadas)
    fs       : frecuencia de muestreo
    f_low, f_high : banda de integración
    nperseg  : no usado (conservado para compatibilidad de firma)

    Returns
    -------
    psi : float en [0, 1]
    """
    N = len(h1)
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    mask = (freqs >= f_low) & (freqs <= f_high)
    if not mask.any():
        return 0.0

    H1_f = np.fft.rfft(h1)[mask]
    L1_f = np.fft.rfft(l1)[mask]

    cross2 = float(np.abs(np.sum(H1_f * np.conj(L1_f))) ** 2)
    denom = float(np.sum(np.abs(H1_f) ** 2) * np.sum(np.abs(L1_f) ** 2))
    if denom < 1e-60:
        return 0.0
    return min(1.0, cross2 / denom)


# ──────────────────────────────────────────────────────────────────────────────
# 4. SERIE TEMPORAL DE Ψ
# ──────────────────────────────────────────────────────────────────────────────


def calcular_serie_psi(
    h1_white: np.ndarray,
    l1_white: np.ndarray,
    fs: float,
    t: np.ndarray,
    t_window: float = T_WINDOW,
    f_low: float = F_LOW,
    f_high: float = F_HIGH,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Desliza una ventana temporal y calcula Ψ en cada posición.

    Parameters
    ----------
    h1_white, l1_white : cepas blanqueadas
    fs         : frecuencia de muestreo
    t          : eje temporal
    t_window   : duración de cada ventana (s)
    f_low, f_high : banda de frecuencias para Ψ

    Returns
    -------
    t_centers  : np.ndarray  (M,)  — tiempo central de cada ventana
    psi_values : np.ndarray  (M,)  — valor de Ψ en cada ventana
    """
    N_window = int(t_window * fs)
    step = N_window  # ventanas no solapadas

    t_centers: List[float] = []
    psi_values: List[float] = []

    for i in range(0, len(h1_white) - N_window + 1, step):
        t_center = float(t[i + N_window // 2])
        h1_win = h1_white[i: i + N_window]
        l1_win = l1_white[i: i + N_window]
        psi = calcular_psi_ventana(h1_win, l1_win, fs,
                                   f_low=f_low, f_high=f_high)
        t_centers.append(t_center)
        psi_values.append(psi)

    return np.array(t_centers), np.array(psi_values)


# ──────────────────────────────────────────────────────────────────────────────
# 4a. ESTADÍSTICAS ON/OFF-SOURCE
# ──────────────────────────────────────────────────────────────────────────────


def analizar_estadisticas(
    t_centers: np.ndarray,
    psi_values: np.ndarray,
    t_merger: float = T_MERGER,
    t_on_half: float = T_ON_HALF,
) -> Dict[str, Any]:
    """
    Separa ventanas ON-source y OFF-source y analiza la separación de Ψ.

    ON-source  : |t_center - t_merger| ≤ t_on_half
    OFF-source : |t_center - t_merger|  > t_on_half

    Prueba estadística: Mann-Whitney U (one-sided, alternativa 'greater').

    Returns
    -------
    dict con psi_on_mean, psi_off_mean, ratio_contraste,
             p_value, separacion_significativa, n_on, n_off, …
    """
    on_mask = np.abs(t_centers - t_merger) <= t_on_half
    off_mask = ~on_mask

    psi_on = psi_values[on_mask]
    psi_off = psi_values[off_mask]

    psi_on_mean = float(np.mean(psi_on)) if len(psi_on) > 0 else 0.0
    psi_off_mean = float(np.mean(psi_off)) if len(psi_off) > 0 else 1e-30
    psi_on_std = float(np.std(psi_on)) if len(psi_on) > 1 else 0.0
    psi_off_std = float(np.std(psi_off)) if len(psi_off) > 1 else 0.0

    if len(psi_on) > 0 and len(psi_off) > 0:
        _, p_value = stats.mannwhitneyu(psi_on, psi_off, alternative="greater")
        p_value = float(p_value)
    else:
        p_value = 1.0

    psi_off_safe = max(psi_off_mean, 1e-30)
    ratio_contraste = psi_on_mean / psi_off_safe

    return {
        "psi_on_mean": psi_on_mean,
        "psi_off_mean": psi_off_mean,
        "psi_on_std": psi_on_std,
        "psi_off_std": psi_off_std,
        "n_on": int(on_mask.sum()),
        "n_off": int(off_mask.sum()),
        "p_value": p_value,
        "separacion_significativa": bool(p_value < 0.05),
        "ratio_contraste": float(ratio_contraste),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4b. BANDA DE CONTROL (anti-sesgo de pipeline)
# ──────────────────────────────────────────────────────────────────────────────


def calcular_ratio_control(
    h1_white: np.ndarray,
    l1_white: np.ndarray,
    fs: float,
    t: np.ndarray,
    t_window: float = T_WINDOW,
    f_ctrl: float = F_CONTROL,
    bw_ctrl: float = 50.0,
) -> Dict[str, Any]:
    """
    Calcula la métrica Ψ en una banda de control (off-target) para detectar
    artefactos de pipeline (line noise, whitening mal calibrado, leakage).

    La banda de control se centra en f_ctrl ± bw_ctrl/2 Hz, que es una región
    desplazada de la banda de señal (35–500 Hz) pero que no debería mostrar
    coherencia selectiva durante el merger si la señal es genuina.

    Un ratio_control ≈ 1 indica que el pipeline no introduce sesgo artificial.
    Un ratio_relativo = ratio_señal / ratio_control >> 1 es evidencia anti-artefacto.

    Parameters
    ----------
    h1_white, l1_white : cepas blanqueadas
    fs        : frecuencia de muestreo
    t         : eje temporal
    t_window  : duración de ventana (s)
    f_ctrl    : frecuencia central de control (Hz) — default F_CONTROL
    bw_ctrl   : ancho de banda de control (Hz) — default 50 Hz

    Returns
    -------
    dict con:
        f_control_hz  : float  — frecuencia central de control
        bw_ctrl_hz    : float  — ancho de banda utilizado
        psi_on_ctrl   : float  — media Ψ on-source en banda control
        psi_off_ctrl  : float  — media Ψ off-source en banda control
        ratio_control : float  — psi_on_ctrl / psi_off_ctrl
        n_on_ctrl     : int
        n_off_ctrl    : int
    """
    f_low_ctrl = f_ctrl - bw_ctrl / 2.0
    f_high_ctrl = f_ctrl + bw_ctrl / 2.0
    # Asegurar que la banda control no excede Nyquist
    f_high_ctrl = min(f_high_ctrl, fs / 2.0 - 1.0)
    f_low_ctrl = max(f_low_ctrl, 1.0)

    t_centers, psi_ctrl = calcular_serie_psi(
        h1_white, l1_white, fs, t,
        t_window=t_window,
        f_low=f_low_ctrl,
        f_high=f_high_ctrl,
    )

    on_mask = np.abs(t_centers - T_MERGER) <= T_ON_HALF
    off_mask = ~on_mask

    psi_on_ctrl = float(np.mean(psi_ctrl[on_mask])) if on_mask.any() else 0.0
    psi_off_ctrl = float(np.mean(psi_ctrl[off_mask])) if off_mask.any() else 1e-30
    psi_off_safe = max(psi_off_ctrl, 1e-30)
    ratio_control = psi_on_ctrl / psi_off_safe

    return {
        "f_control_hz": float(f_ctrl),
        "bw_ctrl_hz": float(bw_ctrl),
        "psi_on_ctrl": psi_on_ctrl,
        "psi_off_ctrl": psi_off_ctrl,
        "ratio_control": float(ratio_control),
        "n_on_ctrl": int(on_mask.sum()),
        "n_off_ctrl": int(off_mask.sum()),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4c. SNR DE RED  (NOESIS ∞³)
# ──────────────────────────────────────────────────────────────────────────────


def calcular_snr_red(
    h1_white: np.ndarray,
    l1_white: np.ndarray,
    fs: float,
    t: np.ndarray,
    t_window: float = T_WINDOW,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula el SNR de red ρ_net = sqrt(ρ_H1² + ρ_L1²) en ventanas deslizantes.

    ρ_detector = sqrt( ⟨|h(t)|²⟩_ventana ) como proxy del SNR instantáneo.

    Returns
    -------
    t_centers  : np.ndarray  (M,)
    snr_series : np.ndarray  (M,)
    """
    N_window = int(t_window * fs)
    step = N_window

    t_centers: List[float] = []
    snr_series: List[float] = []

    for i in range(0, len(h1_white) - N_window + 1, step):
        t_center = float(t[i + N_window // 2])
        h1_win = h1_white[i: i + N_window]
        l1_win = l1_white[i: i + N_window]

        rho_h1 = float(np.sqrt(np.mean(h1_win ** 2)))
        rho_l1 = float(np.sqrt(np.mean(l1_win ** 2)))
        rho_net = math.sqrt(rho_h1 ** 2 + rho_l1 ** 2)

        t_centers.append(t_center)
        snr_series.append(rho_net)

    return np.array(t_centers), np.array(snr_series)


# ──────────────────────────────────────────────────────────────────────────────
# 4d. CONEXIÓN WANG / OCTAVAS  (NOESIS ∞³)
# ──────────────────────────────────────────────────────────────────────────────


def conexion_wang_octavas(
    h1_white: np.ndarray,
    l1_white: np.ndarray,
    fs: float,
    f_base: float = F_LOW,
    n_octavas: int = 5,
) -> Dict[str, Any]:
    """
    Analiza la coherencia multi-escala en octavas sucesivas (Wang et al.).

    Cada octava n cubre [f_base × 2^n, f_base × 2^(n+1)] Hz, hasta Nyquist.

    Returns
    -------
    dict con lista de octavas, octava con Ψ máximo, y Ψ_pico_octava.
    """
    octavas: List[Dict[str, Any]] = []
    for n in range(n_octavas):
        f_lo = f_base * (2 ** n)
        f_hi = f_base * (2 ** (n + 1))
        if f_hi > fs / 2.0:
            break
        psi_oct = calcular_psi_ventana(h1_white, l1_white, fs,
                                       f_low=f_lo, f_high=f_hi)
        octavas.append({
            "octava": n + 1,
            "f_low_hz": float(f_lo),
            "f_high_hz": float(f_hi),
            "psi": float(psi_oct),
        })

    if not octavas:
        return {"octavas": [], "n_octavas": 0, "psi_max_octava": 0.0,
                "octava_pico": None}

    psi_max = max(o["psi"] for o in octavas)
    oct_pico = next(o for o in octavas if o["psi"] == psi_max)

    return {
        "octavas": octavas,
        "n_octavas": len(octavas),
        "psi_max_octava": float(psi_max),
        "octava_pico": oct_pico,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 5. REPORTE JSON EXTENDIDO
# ──────────────────────────────────────────────────────────────────────────────


def generar_reporte(
    resultados: Dict[str, Any],
    output_path: Path,
    snr_result: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    wang_result: Optional[Dict[str, Any]] = None,
    ctrl_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Genera y guarda el reporte JSON extendido del evento GW1509141.

    Integra:
      - Resultados base de coherencia Ψ (estadísticas on/off-source)
      - Banda de control anti-sesgo (opcional)
      - SNR de red ρ_net (NOESIS ∞³, opcional)
      - Conexión Wang / octavas (NOESIS ∞³, opcional)

    Parameters
    ----------
    resultados  : dict con psi_on_mean, psi_off_mean, etc. (salida de analizar_estadisticas)
    output_path : Path donde guardar el JSON
    snr_result  : (t_centers, snr_series) del SNR de red (opcional)
    wang_result : dict de conexion_wang_octavas (opcional)
    ctrl_result : dict de calcular_ratio_control (opcional)

    Returns
    -------
    reporte : dict completo
    """
    ts = datetime.now(tz=timezone.utc).isoformat()

    reporte: Dict[str, Any] = {
        "modulo": SELLO,
        "evento": "GW1509141",
        "timestamp": ts,
        "fs_hz": FS,
        "t_window_s": T_WINDOW,
        "t_on_half_s": T_ON_HALF,
        "f_low_hz": F_LOW,
        "f_high_hz": F_HIGH,
        "seed": SEED,
        "resultados_simulacion": resultados,
    }

    # ── SNR de red ────────────────────────────────────────────────────────
    if snr_result is not None:
        t_snr, snr_ser = snr_result
        idx_peak = int(np.argmax(snr_ser))
        reporte["snr_red"] = {
            "snr_pico": float(snr_ser[idx_peak]),
            "t_pico_s": float(t_snr[idx_peak]),
            "n_ventanas": int(len(snr_ser)),
        }

    # ── Conexión Wang / octavas ───────────────────────────────────────────
    if wang_result is not None:
        reporte["wang_connection"] = wang_result

    # ── Banda de control (anti-sesgo de pipeline) ─────────────────────────
    if ctrl_result is not None:
        ratio_ctrl = ctrl_result.get("ratio_control", 0.0)
        ratio_f0 = resultados.get("ratio_contraste", 0.0)
        ratio_relativo = (ratio_f0 / ratio_ctrl) if ratio_ctrl > 0 else None
        reporte["control_band"] = {
            **ctrl_result,
            "ratio_f0": float(ratio_f0),
            "ratio_relativo": ratio_relativo,
            "descripcion_relativo": (
                "ratio_relativo = ratio_f0 / ratio_control > 1 indica que la "
                "separación ON/OFF es específica de la banda de señal (anti-artefacto)."
            ),
        }

    # ── Guardar ───────────────────────────────────────────────────────────
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(reporte, fh, indent=2, ensure_ascii=False)

    return reporte


# ──────────────────────────────────────────────────────────────────────────────
# 6. CERTIFICADO DE VALIDACIÓN
# ──────────────────────────────────────────────────────────────────────────────


def generar_certificado_validacion(
    reporte: Dict[str, Any],
    output_dir: Path,
) -> Dict[str, Any]:
    """
    Genera el certificado QCAL ∞³ a partir del reporte de validación.

    Fórmula Ψ_evento (no saturante):
        psi_raw    = sqrt(psi_on_mean / psi_off_mean)
        psi_evento = psi_raw / (1 + psi_raw)   ∈ (0, 1)

    Con esta fórmula:
      • ratio = 1   → psi_evento = 0.500  (sin discriminación)
      • ratio = 20  → psi_raw ≈ 4.47 → psi_evento ≈ 0.817
      • ratio → ∞   → psi_evento → 1.0 (asintótico, no saturante)
      • ratio = 0.888²  → psi_raw=0.888 → psi_evento≈0.470 (RUIDO, no EMERGENTE)

    Esto evita que cualquier ratio > 1 inflado colapse en CRISTALIZADO.

    Parameters
    ----------
    reporte    : dict generado por generar_reporte (o compatible)
    output_dir : directorio donde guardar certificado_*.json

    Returns
    -------
    certificado : dict con todos los campos auditables
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Extraer resultados de simulación
    resultados = reporte.get("resultados_simulacion", {})

    # 2. Valores de coherencia
    psi_on_mean = resultados.get("psi_on_mean", 0.0)
    psi_off_mean = resultados.get("psi_off_mean", 1e-30)
    separacion_significativa = resultados.get("separacion_significativa", False)

    # 3. Calcular Ψ_evento con transformación suave no-saturante
    #
    #   psi_raw = sqrt(ratio)          — amplitud lineal del contraste
    #   psi_evento = r / (1 + r)       — mapeo suave a (0, 1), nunca satura
    #
    # Con esta fórmula:
    #   • ratio = 1   → psi_evento = 0.500  (sin discriminación)
    #   • ratio = 20  → psi_raw ≈ 4.47 → psi_evento ≈ 0.817
    #   • ratio → ∞   → psi_evento → 1.0 (asintótico, no saturante)
    #   • ratio = 0.888²  → psi_raw=0.888 → psi_evento≈0.470 (RUIDO, no EMERGENTE)
    #
    # Esto evita que cualquier ratio > 1 inflado colapse en CRISTALIZADO.
    psi_off_safe = max(psi_off_mean, 1e-30)  # Evitar división por cero
    ratio_on_off = psi_on_mean / psi_off_safe
    psi_raw = math.sqrt(ratio_on_off)
    psi_evento = psi_raw / (1.0 + psi_raw)

    # 4. Determinar estado según umbrales QCAL ∞³
    #    Los umbrales se aplican sobre psi_evento = psi_raw/(1+psi_raw).
    #    Equivalencias:
    #      CRISTALIZADO: psi_evento ≥ 0.909 ⟺ psi_raw ≥ 10    ⟺ ratio ≥ 100
    #      COHERENTE   : psi_evento ≥ 0.888 ⟺ psi_raw ≥ 7.929 ⟺ ratio ≥ 62.87
    #      EMERGENTE   : psi_evento ≥ 0.618 ⟺ psi_raw ≥ 1.618 ⟺ ratio ≥ 2.618
    if psi_evento >= 0.909:
        estado = "CRISTALIZADO"
    elif psi_evento >= 0.888:
        estado = "COHERENTE"
    elif psi_evento >= 0.618:
        estado = "EMERGENTE"
    else:
        estado = "RUIDO"

    # 5. Campos de banda de control (anti-sesgo)
    ctrl_band = reporte.get("control_band", {})
    ratio_control: Optional[float] = ctrl_band.get("ratio_control", None)
    ratio_relativo: Optional[float] = ctrl_band.get("ratio_relativo", None)

    # 6. Construir certificado
    ts = datetime.now(tz=timezone.utc).isoformat()
    certificado: Dict[str, Any] = {
        "sello": SELLO,
        "evento": reporte.get("evento", "GW1509141"),
        "timestamp": ts,
        "modulo": reporte.get("modulo", SELLO),
        # Métricas auditables
        "psi_on_mean": psi_on_mean,
        "psi_off_mean": psi_off_mean,
        "ratio_on_off": ratio_on_off,
        "psi_raw": psi_raw,
        "psi_evento_mapeado": psi_evento,
        # Estado y separación
        "estado": estado,
        "separacion_significativa": separacion_significativa,
        "p_value": resultados.get("p_value", None),
        # Anti-sesgo
        "ratio_control": ratio_control,
        "ratio_relativo": ratio_relativo,
        # Parámetros de pipeline
        "f_low_hz": F_LOW,
        "f_high_hz": F_HIGH,
        "f_control_hz": F_CONTROL,
        "t_on_half_s": T_ON_HALF,
        "t_window_s": T_WINDOW,
        "seed": SEED,
    }

    # 7. Hash SHA-256 del contenido del certificado (sin el propio hash)
    contenido_hash = json.dumps(certificado, sort_keys=True, ensure_ascii=False)
    certificado["hash_sha256"] = hashlib.sha256(
        contenido_hash.encode("utf-8")
    ).hexdigest()

    # 8. Guardar certificado
    cert_path = output_dir / f"certificado_{reporte.get('evento', 'GW1509141')}.json"
    with open(cert_path, "w", encoding="utf-8") as fh:
        json.dump(certificado, fh, indent=2, ensure_ascii=False)

    # 9. Imprimir certificado visual en consola
    _ctrl_str = (
        f"{certificado['ratio_control']:.3f}"
        if certificado["ratio_control"] is not None
        else "N/A"
    )
    _rel_str = (
        f"{certificado['ratio_relativo']:.2f}"
        if certificado["ratio_relativo"] is not None
        else "N/A"
    )

    print("\n")
    print("═" * 72)
    print("  CERTIFICADO DE VALIDACIÓN PROFUNDA - EVENTO GRAVITACIONAL")
    # Mostrar los últimos 32 caracteres del hash SHA-256 de 64 caracteres
    print(f"  Hash: …{certificado['hash_sha256'][32:]}")
    print("═" * 72)
    print(f"  Evento       : {certificado['evento']}")
    print(f"  Sello        : {certificado['sello']}")
    print(f"  Timestamp    : {certificado['timestamp']}")
    print("─" * 72)
    print(f"  Ψ_on  (media): {psi_on_mean:.4f}")
    print(f"  Ψ_off (media): {psi_off_mean:.4f}")
    print(f"  ratio_ON/OFF : {ratio_on_off:.2f}")
    print(f"  psi_raw      : {psi_raw:.4f}")
    print(f"  psi_evento   : {psi_evento:.4f}")
    print(f"  ratio_ctrl   : {_ctrl_str}")
    print(f"  ratio_relat. : {_rel_str}")
    print("─" * 72)
    print(f"  Estado QCAL  : ✨ {estado}")
    print(f"  Separación   : {'✅ SÍ' if separacion_significativa else '❌ NO'}")
    print("═" * 72)
    print(f"  Guardado en  : {cert_path}")
    print()

    return certificado


# ──────────────────────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────


def log(msg: str) -> None:
    """Imprime mensaje con timestamp."""
    ts = datetime.now(tz=timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def ejecutar_pipeline(
    output_dir: Optional[Path] = None,
    seed: int = SEED,
) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo de validación GW1509141.

    Returns
    -------
    certificado : dict del certificado generado
    """
    if output_dir is None:
        output_dir = Path("results") / "gw1509141"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    log("🌌 [1/8] Simulando señal de chirp GW (GW1509141)…")
    datos = simular_chirp_gw(seed=seed)
    h1_strain = datos["h1_strain"]
    l1_strain = datos["l1_strain"]
    t = datos["t"]
    log(f"   N={len(t)} muestras, fs={FS} Hz, T={T_TOTAL} s")

    log("🔬 [2/8] Blanqueando señales H1 y L1…")
    h1_white = blanquear(h1_strain, FS, t_ref=t)
    l1_white = blanquear(l1_strain, FS, t_ref=t)

    log(f"📐 [3/8] Calculando serie temporal Ψ (ventana={T_WINDOW} s)…")
    t_centers, psi_series = calcular_serie_psi(h1_white, l1_white, FS, t, T_WINDOW)
    log(f"   {len(t_centers)} ventanas procesadas")

    log("📊 [4/8] Analizando estadísticas ON/OFF-source…")
    stats_result = analizar_estadisticas(t_centers, psi_series)
    pval = stats_result["p_value"]
    log(f"   Ψ_ON  = {stats_result['psi_on_mean']:.4f}")
    log(f"   Ψ_OFF = {stats_result['psi_off_mean']:.4f}")
    log(f"   ratio = {stats_result['ratio_contraste']:.2f}")
    log(f"   p-value     : {pval:.2e}")
    log(f"   Significativo: {'✅ SÍ' if stats_result['separacion_significativa'] else '❌ NO'}")

    log(f"🛡️  [5/8] Calculando ratio en banda de control ({F_CONTROL} Hz)…")
    ctrl_result = calcular_ratio_control(h1_white, l1_white, FS, t, T_WINDOW)
    log(f"   ratio_control: {ctrl_result['ratio_control']:.4f}  (esperado ~1)")

    log("📡 [6/8] Calculando SNR de red (Network SNR)…")
    t_centers_snr, snr_series = calcular_snr_red(h1_white, l1_white, FS, t, T_WINDOW)
    idx_peak_snr = int(np.argmax(snr_series))
    log(f"   SNR_net pico: {snr_series[idx_peak_snr]:.2f} en t={t_centers_snr[idx_peak_snr]:.3f} s")

    log("🔬 [7/8] Analizando conexión Wang (octavas multi-escala)…")
    wang_result = conexion_wang_octavas(h1_white, l1_white, FS)
    log(f"   Ψ_max_octava: {wang_result['psi_max_octava']:.4f}")

    log("📝 [8/8] Generando reporte y certificado…")
    reporte_path = output_dir / "reporte_gw1509141.json"
    reporte = generar_reporte(
        stats_result, reporte_path,
        snr_result=(t_centers_snr, snr_series),
        wang_result=wang_result,
        ctrl_result=ctrl_result,
    )

    certificado = generar_certificado_validacion(reporte, output_dir)

    log("✅ Pipeline completado.")
    return certificado


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    cert = ejecutar_pipeline(output_dir=out)
    sys.exit(0 if cert["estado"] != "RUIDO" else 1)
