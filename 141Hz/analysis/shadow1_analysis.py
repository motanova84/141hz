#!/usr/bin/env python3
"""
Shadow-1: Subthreshold Gravitational-Wave Candidate Analysis
=============================================================

Este módulo implementa el análisis del candidato subumbral "Shadow-1"
usando coherencia de fase cruzada (Welch) entre detectores H1 y L1.

HIPÓTESIS
---------
H0 (Nula):  la señal es ruido instrumental con líneas espectrales,
            glitches y blanqueo imperfecto – NO hay fuente GW coherente.
H1 (Señal): existe una fuente GW subumbral que produce coherencia de
            fase entre H1 y L1 en la banda de interés.

ESTADÍSTICA CANÓNICA
--------------------
El factor de Bayes se reporta en su forma NATURAL (ln_bayes_factor).
La conversión log10 se provee solo como referencia:

    ln_bayes_factor  = ln(B₁₀)       ← CANÓNICO
    log10_bayes_factor = ln_bayes_factor / ln(10)

Si  ln_bayes_factor ≈ 8.3  →  B₁₀ ≈ e^8.3 ≈ 4 000  →  log10(B) ≈ 3.6

MÓDULO EEG
----------
El módulo de demostración EEG está separado bajo la guarda
``if __name__ == "__main__":``.  No existe inferencia conjunta
GW + EEG; la coherencia EEG aplica el mismo feature A_eff pero
sobre datos de electroencefalografía independientes.

AUTOR
-----
José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import numpy as np
from scipy import signal as scipy_signal
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


# ---------------------------------------------------------------------------
# Parámetros del candidato Shadow-1
# ---------------------------------------------------------------------------
SHADOW1_PARAMS: Dict = {
    "nombre": "Shadow-1",
    "detectors": ["H1", "L1"],
    "sample_rate": 4096.0,           # Hz
    "duration": 0.4,                 # segundos (segmento analizado)
    "f_start": 35.0,                 # Hz – inicio de evolución de frecuencia
    "f_end": 150.0,                  # Hz – fin de evolución de frecuencia
    "f0_band": 141.7,                # Hz – frecuencia objetivo QCAL
    "bandwidth_gw": 10.0,            # Hz – ancho de banda señal GW
    "f_ctrl": 300.0,                 # Hz – frecuencia banda de control
    "bandwidth_ctrl": 10.0,          # Hz – ancho de banda de control
    "threshold_A_eff": 0.85,         # umbral de A_eff para detección
    "threshold_duration": 0.05,      # s – duración mínima para colisión
    # Priors para el factor de Bayes
    "prior_signal_prob": 1e-3,       # P(H1) – prior de señal subumbral
    "noise_snr_sigma": 1.0,          # dispersión de SNR bajo H0 (ruido)
    "signal_snr_mu": 5.0,            # SNR esperado bajo H1
    "signal_snr_sigma": 1.0,         # dispersión del SNR bajo H1
}

# Desplazamiento temporal para el control time-slide (claramente fuera
# del retardo físico inter-detector, que es ≤ 10 ms)
TIME_SLIDE_S: float = 0.2           # segundos


# ---------------------------------------------------------------------------
# Estructuras de datos
# ---------------------------------------------------------------------------
@dataclass
class BayesResult:
    """
    Resultado del cálculo del factor de Bayes.

    Attributes
    ----------
    ln_bayes_factor : float
        Logaritmo natural del factor de Bayes B₁₀  ← CANÓNICO.
        Escala Jeffreys (Kass & Raftery 1995):
          |lnB| < 1   → sin evidencia
          1 ≤ |lnB| < 3 → evidencia positiva
          3 ≤ |lnB| < 5 → evidencia fuerte
          |lnB| ≥ 5   → evidencia muy fuerte
    log10_bayes_factor : float
        Equivalente en log₁₀, solo para referencia:
          log10_bayes_factor = ln_bayes_factor / ln(10)
    bayes_factor : float
        Factor de Bayes lineal B₁₀ = exp(ln_bayes_factor).
    interpretation : str
        Texto de interpretación según escala Jeffreys.
    h0_description : str
        Descripción del modelo nulo H0.
    h1_description : str
        Descripción del modelo alternativo H1.
    prior_signal_prob : float
        Prior P(H1) utilizado en el cálculo.
    """
    ln_bayes_factor: float
    log10_bayes_factor: float
    bayes_factor: float
    interpretation: str
    h0_description: str
    h1_description: str
    prior_signal_prob: float


@dataclass
class ChirpMassResult:
    """
    Resultado de la estimación de masa chirp.

    Attributes
    ----------
    chirp_mass_solar : float
        Estimación central de la masa chirp en masas solares (M☉).
    chirp_mass_uncertainty : float
        Incertidumbre (1σ) de la masa chirp en M☉ (bootstrap).
    f_start : float
        Frecuencia inicial usada en Hz.
    f_end : float
        Frecuencia final usada en Hz.
    dt : float
        Duración del segmento en segundos.
    n_bootstrap : int
        Número de iteraciones de bootstrap.
    bootstrap_samples : np.ndarray
        Muestras bootstrap de masa chirp (para análisis posterior).
    warning : str
        Advertencia sobre limitaciones de la estimación.
    """
    chirp_mass_solar: float
    chirp_mass_uncertainty: float
    f_start: float
    f_end: float
    dt: float
    n_bootstrap: int
    bootstrap_samples: np.ndarray
    warning: str


@dataclass
class CoherenceResult:
    """Resultado del cálculo de coherencia de fase."""
    A_eff: float
    freqs: np.ndarray
    coherence: np.ndarray
    band_f0: float
    band_width: float


@dataclass
class SilentCollisionResult:
    """
    Veredicto de colisión silenciosa.

    Attributes
    ----------
    flag_silent_collision : bool
        True si el candidato supera los umbrales de A_eff y duración.
    silent_score : float
        Puntuación continua (no binaria):
            silent_score = A_eff × log1p(duration / threshold_duration)
        Aumenta monótonamente con A_eff y con duration.
    A_eff : float
        Coherencia efectiva usada.
    duration : float
        Duración del candidato en segundos.
    threshold_A_eff : float
        Umbral de A_eff aplicado.
    threshold_duration : float
        Umbral de duración aplicado (segundos).
    """
    flag_silent_collision: bool
    silent_score: float
    A_eff: float
    duration: float
    threshold_A_eff: float
    threshold_duration: float


# ---------------------------------------------------------------------------
# 1. Factor de Bayes con H0/H1 explícitos y priors documentados
# ---------------------------------------------------------------------------
def compute_bayes_factor(
    snr: float,
    params: Optional[Dict] = None,
) -> BayesResult:
    """
    Calcula el factor de Bayes B₁₀ para el candidato subumbral Shadow-1.

    MODELO
    ------
    H0 (ruido instrumental con líneas + glitches + whitening imperfecto):
        SNR ~ HalfNormal(σ=noise_snr_sigma)

    H1 (fuente GW coherente subumbral):
        SNR ~ Normal(μ=signal_snr_mu, σ=signal_snr_sigma)

    ESTADÍSTICA CANÓNICA
    --------------------
    El resultado canónico es ``ln_bayes_factor = ln(B₁₀)``.
    El campo ``log10_bayes_factor`` se deriva de él:

        log10_bayes_factor = ln_bayes_factor / ln(10)

    Si ln_bayes_factor ≈ 8.3  →  B₁₀ ≈ e^8.3 ≈ 4 000  →  log10(B) ≈ 3.6
    Si log10_bayes_factor ≈ 8.3  →  B₁₀ ≈ 2×10^8  (otro orden de magnitud)

    Parameters
    ----------
    snr : float
        Relación señal-ruido observada del candidato.
    params : dict, optional
        Parámetros del análisis.  Si None usa SHADOW1_PARAMS.

    Returns
    -------
    BayesResult
        Factor de Bayes con campos ``ln_bayes_factor`` (canónico) y
        ``log10_bayes_factor`` (solo referencia).
    """
    if params is None:
        params = SHADOW1_PARAMS

    noise_sigma = float(params.get("noise_snr_sigma", 1.0))
    signal_mu = float(params.get("signal_snr_mu", 5.0))
    signal_sigma = float(params.get("signal_snr_sigma", 1.0))
    prior_h1 = float(params.get("prior_signal_prob", 1e-3))
    prior_h0 = 1.0 - prior_h1

    # Log-verosimilitud bajo H0: HalfNormal  →  p(snr|H0) ∝ exp(-snr²/2σ²)
    log_p_snr_h0 = -0.5 * (snr / noise_sigma) ** 2

    # Log-verosimilitud bajo H1: Normal(μ, σ)
    log_p_snr_h1 = -0.5 * ((snr - signal_mu) / signal_sigma) ** 2

    # Log-evidencias con priors
    log_evidence_h0 = np.log(prior_h0) + log_p_snr_h0
    log_evidence_h1 = np.log(prior_h1) + log_p_snr_h1

    # ln(B₁₀) = ln P(data|H1) - ln P(data|H0)   ← CANÓNICO
    ln_bf = float(log_evidence_h1 - log_evidence_h0)
    log10_bf = float(ln_bf / np.log(10.0))
    b10 = float(np.exp(np.clip(ln_bf, -700, 700)))

    interpretation = _interpret_jeffreys(ln_bf)

    h0_desc = (
        "H0: ruido con líneas espectrales + glitches + whitening imperfecto. "
        f"Modelo: HalfNormal(σ={noise_sigma}).  P(H0)={prior_h0:.4f}."
    )
    h1_desc = (
        "H1: fuente GW subumbral coherente entre H1 y L1. "
        f"Modelo: Normal(μ={signal_mu}, σ={signal_sigma}).  "
        f"P(H1)={prior_h1:.4f} (prior conservador para subumbrales)."
    )

    return BayesResult(
        ln_bayes_factor=ln_bf,
        log10_bayes_factor=log10_bf,
        bayes_factor=b10,
        interpretation=interpretation,
        h0_description=h0_desc,
        h1_description=h1_desc,
        prior_signal_prob=prior_h1,
    )


def _interpret_jeffreys(ln_bf: float) -> str:
    """Interpreta ln(B₁₀) según la escala de Jeffreys / Kass & Raftery 1995."""
    abs_lnb = abs(ln_bf)
    if abs_lnb < 1.0:
        strength = "Sin evidencia apreciable"
    elif abs_lnb < 3.0:
        strength = "Evidencia positiva"
    elif abs_lnb < 5.0:
        strength = "Evidencia fuerte"
    else:
        strength = "Evidencia muy fuerte"
    direction = "para H1 (señal)" if ln_bf > 0 else "para H0 (ruido)"
    return f"{strength} {direction}"


# ---------------------------------------------------------------------------
# 2. Masa chirp desde evolución de frecuencia (PN0) con incertidumbre
# ---------------------------------------------------------------------------
_MSUN_KG = 1.989e30
_G = 6.674e-11
_C = 2.998e8


def chirp_mass_from_frequency_evolution(
    f_start: float,
    f_end: float,
    dt: float,
    n_bootstrap: int = 500,
    jitter_frac: float = 0.05,
    rng: Optional[np.random.Generator] = None,
) -> ChirpMassResult:
    """
    Estima la masa chirp a partir de la evolución de frecuencia (PN0).

    ADVERTENCIA
    -----------
    En segmentos cortos (dt ≲ 0.4 s) y señales subumbrales, df/dt puede
    estar dominado por el filtrado, la ventana y el leakage espectral.
    Esta función reporta incertidumbre bootstrap y debe complementarse
    con un test de "falso positivo" sobre segmentos off-source.

    FÓRMULA PN0
    -----------
        Ṁ_c = (c³/G) × [5/(96 π^(8/3)) × f^(-11/3) × |df/dt|]^(3/5)

    Parameters
    ----------
    f_start : float
        Frecuencia inicial en Hz.
    f_end : float
        Frecuencia final en Hz.
    dt : float
        Duración del segmento en segundos.
    n_bootstrap : int
        Iteraciones bootstrap para estimar incertidumbre.
    jitter_frac : float
        Fracción de jitter aplicada a f_start/f_end en bootstrap (p.ej., 0.05 = 5%).
    rng : np.random.Generator, optional
        Generador de números aleatorios para reproducibilidad.

    Returns
    -------
    ChirpMassResult
        Masa chirp central + incertidumbre 1σ bootstrap en M☉.
    """
    if rng is None:
        rng = np.random.default_rng(seed=42)

    def _pn0_chirp_mass(f0: float, dfdt: float) -> float:
        """Masa chirp PN0 en kg."""
        if dfdt <= 0 or f0 <= 0:
            return 0.0
        factor = (5.0 / (96.0 * np.pi ** (8.0 / 3.0))) * f0 ** (-11.0 / 3.0) * dfdt
        m_kg = (_C ** 3 / _G) * factor ** 0.6
        return m_kg / _MSUN_KG

    f_mean = 0.5 * (f_start + f_end)
    dfdt_central = abs(f_end - f_start) / max(dt, 1e-9)
    mc_central = _pn0_chirp_mass(f_mean, dfdt_central)

    # Bootstrap: jitter en f_start, f_end para cuantificar sensibilidad
    jitter_start = f_start * jitter_frac
    jitter_end = f_end * jitter_frac
    samples = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        fs_i = f_start + rng.uniform(-jitter_start, jitter_start)
        fe_i = f_end + rng.uniform(-jitter_end, jitter_end)
        fm_i = 0.5 * (fs_i + fe_i)
        dfdt_i = abs(fe_i - fs_i) / max(dt, 1e-9)
        samples[i] = _pn0_chirp_mass(fm_i, dfdt_i)

    mc_uncertainty = float(np.std(samples))

    warning = (
        "ADVERTENCIA: estimación PN0 sobre segmento corto (dt="
        f"{dt:.2f} s). df/dt puede estar dominado por filtrado/leakage. "
        "Validar con test off-source de pseudoevolución aleatoria."
    )

    return ChirpMassResult(
        chirp_mass_solar=float(mc_central),
        chirp_mass_uncertainty=mc_uncertainty,
        f_start=f_start,
        f_end=f_end,
        dt=dt,
        n_bootstrap=n_bootstrap,
        bootstrap_samples=samples,
        warning=warning,
    )


# ---------------------------------------------------------------------------
# 3. Coherencia de fase: A_eff = median(sqrt(γ))
# ---------------------------------------------------------------------------
def compute_phase_coherence(
    data_h1: np.ndarray,
    data_l1: np.ndarray,
    fs: float = 4096.0,
    f0: float = 141.7,
    bandwidth: float = 10.0,
    nperseg: Optional[int] = None,
) -> CoherenceResult:
    """
    Calcula la coherencia de fase cruzada (Welch) entre H1 y L1.

    A_eff = median(√γ(f))   para f ∈ [f0 - bw/2, f0 + bw/2]

    donde γ(f) ∈ [0,1] es la coherencia al cuadrado de Welch (MSC).

    Parameters
    ----------
    data_h1 : np.ndarray
        Strain del detector H1.
    data_l1 : np.ndarray
        Strain del detector L1.
    fs : float
        Tasa de muestreo en Hz.
    f0 : float
        Frecuencia central de la banda en Hz.
    bandwidth : float
        Ancho de banda en Hz.
    nperseg : int, optional
        Longitud del segmento Welch.  Por defecto min(N, 256).

    Returns
    -------
    CoherenceResult
        Coherencia efectiva A_eff y el espectro completo de coherencia.
    """
    N = min(len(data_h1), len(data_l1))
    if nperseg is None:
        nperseg = min(N, 256)

    freqs, coh = scipy_signal.coherence(
        data_h1[:N], data_l1[:N],
        fs=fs,
        nperseg=nperseg,
    )

    flo = f0 - bandwidth / 2.0
    fhi = f0 + bandwidth / 2.0
    mask = (freqs >= flo) & (freqs <= fhi)

    if not np.any(mask):
        A_eff = 0.0
    else:
        A_eff = float(np.median(np.sqrt(np.maximum(coh[mask], 0.0))))

    return CoherenceResult(
        A_eff=A_eff,
        freqs=freqs,
        coherence=coh,
        band_f0=f0,
        band_width=bandwidth,
    )


# ---------------------------------------------------------------------------
# 4. Control A: time-slide
# ---------------------------------------------------------------------------
def time_slide_control(
    data_h1: np.ndarray,
    data_l1: np.ndarray,
    fs: float = 4096.0,
    f0: float = 141.7,
    bandwidth: float = 10.0,
    slide_s: float = TIME_SLIDE_S,
) -> Dict:
    """
    Control de desplazamiento temporal (time-slide).

    Desplaza L1 en ``slide_s`` segundos (muy por encima del retardo
    físico ≤ 10 ms).  Si A_eff_slide ≈ A_eff_on → artefacto instrumental.
    Si A_eff_slide << A_eff_on → coherencia física plausible.

    Parameters
    ----------
    data_h1 : np.ndarray
        Strain de H1.
    data_l1 : np.ndarray
        Strain de L1.
    fs : float
        Tasa de muestreo en Hz.
    f0 : float
        Frecuencia objetivo en Hz.
    bandwidth : float
        Ancho de banda en Hz.
    slide_s : float
        Desplazamiento temporal en segundos (default: 0.2 s).

    Returns
    -------
    dict
        Claves: A_eff_on_source, A_eff_time_slide, slide_s,
                coherence_drop_fraction, is_physical.
    """
    # Coherencia nominal (on-source)
    res_on = compute_phase_coherence(data_h1, data_l1, fs, f0, bandwidth)
    A_on = res_on.A_eff

    # Desplazamiento temporal
    n_slide = int(slide_s * fs)
    n = min(len(data_h1), len(data_l1))
    if n_slide >= n:
        n_slide = n // 4

    data_l1_slid = np.roll(data_l1[:n], n_slide)
    # Los primeros n_slide muestras son artefacto de wrap-around: cero-rellenar
    data_l1_slid[:n_slide] = 0.0

    res_slide = compute_phase_coherence(data_h1[:n], data_l1_slid, fs, f0, bandwidth)
    A_slide = res_slide.A_eff

    drop_fraction = (A_on - A_slide) / max(A_on, 1e-12)
    # Se considera coherencia física si A_eff cae al menos un 20 %
    is_physical = bool(drop_fraction > 0.20)

    return {
        "A_eff_on_source": A_on,
        "A_eff_time_slide": A_slide,
        "slide_s": slide_s,
        "coherence_drop_fraction": float(drop_fraction),
        "is_physical": is_physical,
    }


# ---------------------------------------------------------------------------
# 5. Control B: banda de control (frequency scramble)
# ---------------------------------------------------------------------------
def band_coherence_control(
    data_h1: np.ndarray,
    data_l1: np.ndarray,
    fs: float = 4096.0,
    f0: float = 141.7,
    bandwidth_gw: float = 10.0,
    f_ctrl: float = 300.0,
    bandwidth_ctrl: float = 10.0,
) -> Dict:
    """
    Control de banda de frecuencia (frequency scramble).

    Compara A_eff en la banda GW con A_eff en una banda de control vacía
    para detectar artefactos instrumentales (líneas espectrales comunes).

    Parameters
    ----------
    data_h1 : np.ndarray
        Strain de H1.
    data_l1 : np.ndarray
        Strain de L1.
    fs : float
        Tasa de muestreo en Hz.
    f0 : float
        Frecuencia central de la banda GW en Hz.
    bandwidth_gw : float
        Ancho de banda GW en Hz.
    f_ctrl : float
        Frecuencia central de la banda de control en Hz.
    bandwidth_ctrl : float
        Ancho de banda de control en Hz.

    Returns
    -------
    dict
        Claves: A_eff_gw_band, A_eff_ctrl_band, relative_ratio,
                f0, f_ctrl, is_excess_coherence.
    """
    res_gw = compute_phase_coherence(data_h1, data_l1, fs, f0, bandwidth_gw)
    res_ctrl = compute_phase_coherence(data_h1, data_l1, fs, f_ctrl, bandwidth_ctrl)

    A_gw = res_gw.A_eff
    A_ctrl = res_ctrl.A_eff

    relative_ratio = A_gw / max(A_ctrl, 1e-12)
    # Hay exceso de coherencia si la razón GW/control es > 2
    is_excess = bool(relative_ratio > 2.0)

    return {
        "A_eff_gw_band": A_gw,
        "A_eff_ctrl_band": A_ctrl,
        "relative_ratio": float(relative_ratio),
        "f0": f0,
        "f_ctrl": f_ctrl,
        "is_excess_coherence": is_excess,
    }


# ---------------------------------------------------------------------------
# 6. Veredicto de colisión silenciosa (score continuo + flag binario)
# ---------------------------------------------------------------------------
def silent_collision_verdict(
    A_eff: float,
    duration: float,
    threshold_A_eff: float = SHADOW1_PARAMS["threshold_A_eff"],
    threshold_duration: float = SHADOW1_PARAMS["threshold_duration"],
) -> SilentCollisionResult:
    """
    Emite un veredicto de "colisión silenciosa" con puntuación continua.

    La puntuación continua evita que la etiqueta parezca "mágica":

        silent_score = A_eff × log1p(duration / threshold_duration)

    Aumenta monótonamente con A_eff y con duration.  El flag binario
    requiere que AMBOS umbrales sean superados simultáneamente.

    Parameters
    ----------
    A_eff : float
        Coherencia efectiva medida (entre 0 y 1).
    duration : float
        Duración del candidato en segundos.
    threshold_A_eff : float
        Umbral de A_eff para activar el flag (default 0.85).
    threshold_duration : float
        Duración mínima en segundos (default 0.05 s).

    Returns
    -------
    SilentCollisionResult
        Flag binario y puntuación continua.
    """
    silent_score = float(A_eff * np.log1p(duration / max(threshold_duration, 1e-12)))
    flag = bool(A_eff >= threshold_A_eff and duration >= threshold_duration)

    return SilentCollisionResult(
        flag_silent_collision=flag,
        silent_score=silent_score,
        A_eff=A_eff,
        duration=duration,
        threshold_A_eff=threshold_A_eff,
        threshold_duration=threshold_duration,
    )


# ---------------------------------------------------------------------------
# Función de análisis completo
# ---------------------------------------------------------------------------
def analizar_shadow1(
    data_h1: Optional[np.ndarray] = None,
    data_l1: Optional[np.ndarray] = None,
    params: Optional[Dict] = None,
    mostrar_detalles: bool = True,
) -> Dict:
    """
    Ejecuta el análisis completo de Shadow-1.

    Si no se proveen datos reales, genera datos sintéticos de prueba.

    Parameters
    ----------
    data_h1 : np.ndarray, optional
        Strain del detector H1.  Si None, se simulan datos.
    data_l1 : np.ndarray, optional
        Strain del detector L1.  Si None, se simulan datos.
    params : dict, optional
        Parámetros del análisis.  Si None usa SHADOW1_PARAMS.
    mostrar_detalles : bool
        Si True, imprime un resumen de los resultados.

    Returns
    -------
    dict
        Resultados completos con claves:
        bayes, chirp_mass, coherence, time_slide, band_control,
        silent_collision.
    """
    if params is None:
        params = SHADOW1_PARAMS

    fs = float(params["sample_rate"])
    duration = float(params["duration"])
    N = int(fs * duration)

    # Datos sintéticos de prueba si no se proveen reales
    if data_h1 is None or data_l1 is None:
        rng = np.random.default_rng(seed=141)
        noise_level = 4e-24
        signal_amp = 0.5 * noise_level  # señal subumbral
        t = np.linspace(0, duration, N)
        f0 = float(params["f0_band"])
        noise_h1 = rng.normal(0, noise_level, N)
        noise_l1 = rng.normal(0, noise_level, N)
        signal = signal_amp * np.sin(2.0 * np.pi * f0 * t)
        data_h1 = noise_h1 + signal
        data_l1 = noise_l1 + signal * 0.9  # ligera atenuación en L1

    # --- Factor de Bayes ---
    snr_proxy = float(np.std(data_h1)) / float(np.std(
        np.random.default_rng(seed=0).normal(0, 1e-24, len(data_h1))
    ))
    bayes_res = compute_bayes_factor(snr_proxy, params)

    # --- Masa chirp ---
    chirp_res = chirp_mass_from_frequency_evolution(
        f_start=float(params["f_start"]),
        f_end=float(params["f_end"]),
        dt=duration,
    )

    # --- Coherencia ---
    coh_res = compute_phase_coherence(
        data_h1, data_l1, fs,
        f0=float(params["f0_band"]),
        bandwidth=float(params["bandwidth_gw"]),
    )

    # --- Control time-slide ---
    slide_res = time_slide_control(
        data_h1, data_l1, fs,
        f0=float(params["f0_band"]),
        bandwidth=float(params["bandwidth_gw"]),
    )

    # --- Control de banda ---
    band_res = band_coherence_control(
        data_h1, data_l1, fs,
        f0=float(params["f0_band"]),
        bandwidth_gw=float(params["bandwidth_gw"]),
        f_ctrl=float(params["f_ctrl"]),
        bandwidth_ctrl=float(params["bandwidth_ctrl"]),
    )

    # --- Veredicto ---
    verdict = silent_collision_verdict(coh_res.A_eff, duration)

    if mostrar_detalles:
        _print_resumen(bayes_res, chirp_res, coh_res, slide_res, band_res, verdict)

    return {
        "bayes": bayes_res,
        "chirp_mass": chirp_res,
        "coherence": coh_res,
        "time_slide": slide_res,
        "band_control": band_res,
        "silent_collision": verdict,
    }


def _print_resumen(bayes_res, chirp_res, coh_res, slide_res, band_res, verdict):
    sep = "=" * 70
    print(f"\n{sep}")
    print("SHADOW-1: Análisis de Candidato Subumbral")
    print(sep)

    print("\n▶ FACTOR DE BAYES")
    print(f"  ln(B₁₀)        [CANÓNICO] : {bayes_res.ln_bayes_factor:+.3f}")
    print(f"  log10(B₁₀)     [referencia]: {bayes_res.log10_bayes_factor:+.3f}")
    print(f"  B₁₀ lineal               : {bayes_res.bayes_factor:.3e}")
    print(f"  Interpretación            : {bayes_res.interpretation}")
    print(f"  H0 : {bayes_res.h0_description}")
    print(f"  H1 : {bayes_res.h1_description}")

    print("\n▶ MASA CHIRP (PN0)")
    print(f"  M_chirp = {chirp_res.chirp_mass_solar:.4f} ± {chirp_res.chirp_mass_uncertainty:.4f} M☉")
    print(f"  ⚠  {chirp_res.warning}")

    print("\n▶ COHERENCIA (A_eff)")
    print(f"  A_eff (banda GW)    : {coh_res.A_eff:.4f}")
    print(f"  A_eff (time-slide)  : {slide_res['A_eff_time_slide']:.4f}")
    drop = slide_res['coherence_drop_fraction']
    phys = "✅ coherencia física plausible" if slide_res['is_physical'] else "⚠️  posible artefacto"
    print(f"  Caída con slide     : {drop*100:.1f}%  → {phys}")
    print(f"  A_eff (banda ctrl)  : {band_res['A_eff_ctrl_band']:.4f}")
    ratio = band_res['relative_ratio']
    excess = "✅ exceso real" if band_res['is_excess_coherence'] else "⚠️  sin exceso claro"
    print(f"  Ratio GW/ctrl       : {ratio:.2f}  → {excess}")

    print("\n▶ VEREDICTO COLISIÓN SILENCIOSA")
    print(f"  flag_silent_collision : {verdict.flag_silent_collision}")
    print(f"  silent_score          : {verdict.silent_score:.4f}")
    print(f"  (A_eff={verdict.A_eff:.4f}, duration={verdict.duration:.3f} s)")
    print(sep + "\n")


# ---------------------------------------------------------------------------
# Módulo EEG – COMPLETAMENTE INDEPENDIENTE del análisis GW
# ---------------------------------------------------------------------------
def demo_eeg():
    """
    Demostración de A_eff aplicada a datos EEG.

    NOTA: Esta función es solo una aplicación del feature de coherencia.
    NO existe inferencia conjunta GW + EEG.  Los datos EEG son
    completamente independientes del evento Shadow-1.

    "EEG module is independent; no joint inference."
    """
    print("\n[EEG DEMO – módulo independiente, sin inferencia conjunta GW+EEG]")
    rng = np.random.default_rng(seed=888)
    fs_eeg = 256.0
    duration_eeg = 4.0
    N_eeg = int(fs_eeg * duration_eeg)

    # Simulación: canal frontal y parietal con coherencia parcial en ~10 Hz (alfa)
    t_eeg = np.linspace(0, duration_eeg, N_eeg)
    f_alpha = 10.0
    signal_eeg = 50e-6 * np.sin(2 * np.pi * f_alpha * t_eeg)
    ch1 = rng.normal(0, 10e-6, N_eeg) + signal_eeg
    ch2 = rng.normal(0, 10e-6, N_eeg) + signal_eeg * 0.8

    res = compute_phase_coherence(ch1, ch2, fs=fs_eeg, f0=f_alpha, bandwidth=4.0)
    print(f"  A_eff EEG en banda alfa ({f_alpha} Hz): {res.A_eff:.4f}")
    print("  [Fin demo EEG]\n")


if __name__ == "__main__":
    # Análisis GW Shadow-1
    print("\n" + "=" * 70)
    print("SHADOW-1: Ejecución de análisis completo")
    print("=" * 70)
    analizar_shadow1(mostrar_detalles=True)

    # Demo EEG (independiente)
    demo_eeg()
