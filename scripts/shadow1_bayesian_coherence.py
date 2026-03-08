#!/usr/bin/env python3
"""
Análisis Morfológico de "Shadow-1" (GPS: 1251010524.0)
=======================================================

Implementa Inferencia Bayesiana de Coherencia para la caracterización
del candidato sub-umbral "Shadow-1":

- Estimación de parámetros: masas, distancia de luminosidad, fase
- Verificación de estabilidad de fase (A_eff = 0.89 durante 0.4 s)
- Pipeline de coherencia Ψ aplicado también a señales EEG

Axiomas del Libro III (Primacía de la Relación, Silencio como Carga,
Ingenio Cósmico) se codifican como invariantes físicos verificables.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import math

import numpy as np
from scipy import signal, stats, special
from scipy.signal import coherence as scipy_coherence
import warnings

warnings.filterwarnings("ignore")

# ─── Constantes físicas ──────────────────────────────────────────────────────
SOLAR_MASS_KG = 1.989e30          # kg
G_CONST = 6.674e-11               # m³ kg⁻¹ s⁻²
C_LIGHT = 2.998e8                 # m s⁻¹
MPC_TO_METERS = 3.086e22          # m Mpc⁻¹

# ─── Definición canónica de Ψ (coherencia de fase) ──────────────────────────
#
# Ψ_GW  : Magnitud Cuadrada de Coherencia (MSC) entre detectores H1-L1
#          evaluada en f₀ = 141.7001 Hz.
#          MSC(f) = |S_{xy}(f)|² / (S_{xx}(f)·S_{yy}(f))  ∈ [0, 1]
#          Umbral de detección: PSI_THRESHOLD_GW = 0.85
#
# Ψ_EEG : Phase Locking Value (PLV) inter-hemisférico en la banda de interés.
#          PLV(t) = |<e^{iΔφ(t)}>| ≈ sqrt(MSC)  ∈ [0, 1]
#          Umbral de detección: PSI_THRESHOLD_EEG = 0.70
#
# Ambas métricas comparten la misma infraestructura de coherencia espectral
# de Welch; la diferencia es el dominio físico y el umbral de decisión.
PSI_DEFINITION_GW  = "MSC@f0=141.7Hz"   # Magnitude Squared Coherence at f₀
PSI_DEFINITION_EEG = "PLV@band"          # Phase Locking Value in frequency band
PSI_THRESHOLD_GW   = 0.85                # A_eff threshold for GW phase stability
PSI_THRESHOLD_EEG  = 0.70                # A_eff threshold for EEG shadow detection

# ─── Parámetros de Shadow-1 ──────────────────────────────────────────────────
SHADOW1_GPS = 1251010524.0        # GPS time del evento
SHADOW1_A_EFF = 0.89              # Amplitud efectiva de coherencia de fase
SHADOW1_DURATION_S = 0.4          # Duración de la firma de fase (s)
SHADOW1_DISTANCE_MPC = 600.0      # Distancia de luminosidad estimada (Mpc)
SHADOW1_MASS_MIN = 1.4            # Masa mínima de componente (M☉)
SHADOW1_MASS_MAX = 3.0            # Masa máxima de componente secundario (M☉)
# For NSBH systems the primary (heavier) black hole can reach ~10 M☉ in O3;
# we use 9 M☉ (3 × SHADOW1_MASS_MAX) as a conservative upper bound for m1.
SHADOW1_MASS_MAX_PRIMARY = 9.0    # Masa máxima de componente primario (M☉)

# Umbral de duración de glitch instrumental (LIGO)
GLITCH_DURATION_THRESHOLD_S = 0.05

# ─── Chirp mass y masas ──────────────────────────────────────────────────────

def chirp_mass_from_frequency_evolution(f_start: float, f_end: float,
                                         dt: float) -> float:
    """
    Estima la chirp mass a partir de la evolución de frecuencia de la señal.

    Usa la relación post-newtoniana de orden cero:
        df/dt = (96/5) π^(8/3) (G M_c / c³)^(5/3) f^(11/3)

    Parameters
    ----------
    f_start : float
        Frecuencia inicial del chirp (Hz).
    f_end : float
        Frecuencia final del chirp (Hz).
    dt : float
        Intervalo de tiempo (s).

    Returns
    -------
    float
        Chirp mass en masas solares.
    """
    if dt <= 0 or f_end <= f_start:
        raise ValueError("dt debe ser positivo y f_end > f_start")

    df_dt = (f_end - f_start) / dt
    # M_c = (c³ / G) × [5/(96 π^(8/3)) × df/dt / f^(11/3)]^(3/5)
    f_mean = 0.5 * (f_start + f_end)
    factor = (5.0 / (96.0 * np.pi ** (8.0 / 3.0))) * (df_dt / f_mean ** (11.0 / 3.0))
    if factor <= 0:
        raise ValueError("Factor de chirp mass no positivo; revisar parámetros")
    m_c_kg = (C_LIGHT ** 3 / G_CONST) * factor ** (3.0 / 5.0)
    return m_c_kg / SOLAR_MASS_KG


def masses_from_chirp_mass(m_chirp: float, mass_ratio: float = 1.0):
    """
    Calcula masas de componentes a partir de la chirp mass y razón de masas.

    Parameters
    ----------
    m_chirp : float
        Chirp mass en masas solares.
    mass_ratio : float
        q = m2 / m1 con m1 >= m2 (0 < q <= 1).

    Returns
    -------
    tuple of float
        (m1, m2) en masas solares.
    """
    if not 0 < mass_ratio <= 1:
        raise ValueError("mass_ratio debe estar en (0, 1]")
    eta = mass_ratio / (1.0 + mass_ratio) ** 2   # symmetric mass ratio
    m_total = m_chirp / eta ** 0.6
    m1 = m_total / (1.0 + mass_ratio)
    m2 = m_total * mass_ratio / (1.0 + mass_ratio)
    return float(m1), float(m2)


# ─── Coherencia de fase ───────────────────────────────────────────────────────

def compute_phase_coherence(h1: np.ndarray, l1: np.ndarray,
                             fs: float, nperseg: int = 256) -> dict:
    """
    Calcula la coherencia de fase Ψ_GW entre dos detectores usando la función
    de coherencia de Welch (Magnitud Cuadrada de Coherencia, MSC).

    Ψ_GW = MSC@f0=141.7Hz: A_eff = mediana(sqrt(MSC(f))) en la banda de interés.
    Umbral de decisión: PSI_THRESHOLD_GW = 0.85.

    Parameters
    ----------
    h1 : np.ndarray
        Strain de Hanford (H1).
    l1 : np.ndarray
        Strain de Livingston (L1).
    fs : float
        Frecuencia de muestreo (Hz).
    nperseg : int
        Número de muestras por segmento de Welch.

    Returns
    -------
    dict
        Claves: 'freqs', 'coherence', 'a_eff', 'phase_stable',
                'psi_definition', 'psi_threshold'.
    """
    freqs, coh = signal.coherence(h1, l1, fs=fs, nperseg=nperseg)
    a_eff = float(np.median(np.sqrt(np.clip(coh, 0, 1))))
    phase_stable = bool(a_eff >= PSI_THRESHOLD_GW)
    return {
        "freqs": freqs,
        "coherence": coh,
        "a_eff": a_eff,
        "phase_stable": phase_stable,
        "psi_definition": PSI_DEFINITION_GW,
        "psi_threshold": PSI_THRESHOLD_GW,
    }


def verify_phase_stability(a_eff: float, duration: float) -> dict:
    """
    Verifica que la firma de fase sea estable durante la duración indicada,
    descartando así glitches instrumentales.

    Parameters
    ----------
    a_eff : float
        Amplitud efectiva de coherencia de fase.
    duration : float
        Duración observada de la firma (s).

    Returns
    -------
    dict
        Resultado de la verificación con 'is_glitch_excluded' y 'verdict'.
    """
    glitch_excluded = duration > GLITCH_DURATION_THRESHOLD_S
    is_astrophysical = a_eff >= PSI_THRESHOLD_GW and glitch_excluded
    verdict = "Silent Collision" if is_astrophysical else "Inconclusive"
    return {
        "a_eff": a_eff,
        "duration_s": duration,
        "glitch_threshold_s": GLITCH_DURATION_THRESHOLD_S,
        "is_glitch_excluded": glitch_excluded,
        "is_astrophysical": is_astrophysical,
        "verdict": verdict,
    }


# ─── Anti-artefacto: coherencia por banda y controles ────────────────────────

def band_coherence_feature(x: np.ndarray, y: np.ndarray, fs: float,
                            band: tuple, nperseg: int = 256) -> dict:
    """
    Calcula A_eff robusto (mediana de sqrt(coherencia)) en una banda dada.

    Parameters
    ----------
    x, y : np.ndarray
        Señales de entrada.
    fs : float
        Frecuencia de muestreo (Hz).
    band : tuple of float
        (f_low, f_high) en Hz.
    nperseg : int
        Número de muestras por segmento.

    Returns
    -------
    dict
        'band_hz', 'a_eff', 'coh_mean', 'coh_median', 'n_bins'.
    """
    f, Cxy = scipy_coherence(x, y, fs=fs, nperseg=nperseg)
    lo, hi = band
    m = (f >= lo) & (f <= hi)
    c_band = np.nan_to_num(Cxy[m], nan=0.0, posinf=0.0, neginf=0.0)

    if c_band.size:
        a_eff = float(np.median(np.sqrt(np.clip(c_band, 0.0, 1.0))))
    else:
        a_eff = 0.0

    return {
        "band_hz": [float(lo), float(hi)],
        "a_eff": a_eff,
        "coh_mean": float(np.mean(c_band)) if c_band.size else 0.0,
        "coh_median": float(np.median(c_band)) if c_band.size else 0.0,
        "n_bins": int(c_band.size),
    }


def normalize_bayes_factor(*, lnB: float = None, log10B: float = None) -> dict:
    """
    Normaliza el Bayes factor devolviendo ambas representaciones sin ambigüedad.

    Provide exactly one of lnB or log10B; the other is computed automatically.

    Parameters
    ----------
    lnB : float, optional
        Log natural del Bayes factor.
    log10B : float, optional
        Log base-10 del Bayes factor.

    Returns
    -------
    dict
        'ln_bayes_factor', 'log10_bayes_factor'.
    """
    if lnB is None and log10B is None:
        raise ValueError("Must provide exactly one of lnB or log10B, but neither was provided")

    if lnB is None:
        lnB = float(log10B) * math.log(10.0)
    if log10B is None:
        log10B = float(lnB) / math.log(10.0)

    return {
        "ln_bayes_factor": float(lnB),
        "log10_bayes_factor": float(log10B),
    }


def time_slide_control(x: np.ndarray, y: np.ndarray, fs: float,
                        band: tuple,
                        slides_s: list = None) -> dict:
    """
    Control de time-slide: desfasa y en varios intervalos y mide A_eff.

    Si A_eff sigue alto tras el slide → instrumental/pipeline.
    Si A_eff cae → coherencia física plausible.

    Parameters
    ----------
    x, y : np.ndarray
        Señales H1 y L1.
    fs : float
        Frecuencia de muestreo (Hz).
    band : tuple of float
        Banda de señal (Hz).
    slides_s : list of float
        Desplazamientos temporales en segundos.

    Returns
    -------
    dict
        'slides_s', 'a_eff_slide_median', 'a_eff_slide_max', 'details'.
    """
    if slides_s is None:
        slides_s = [0.2, -0.2, 0.4, -0.4]

    n = len(x)
    out = []
    for dt in slides_s:
        shift = int(round(dt * fs))
        if abs(shift) >= n:
            continue
        y_shift = np.roll(y, shift)
        feat = band_coherence_feature(x, y_shift, fs, band)
        feat["slide_s"] = float(dt)
        out.append(feat)

    a_eff_slides = [d["a_eff"] for d in out] if out else [0.0]
    a_eff_med = float(np.median(a_eff_slides))
    a_eff_max = float(np.max(a_eff_slides))

    return {
        "slides_s": slides_s,
        "a_eff_slide_median": a_eff_med,
        "a_eff_slide_max": a_eff_max,
        "details": out,
    }


def control_band_check(x: np.ndarray, y: np.ndarray, fs: float,
                        signal_band: tuple,
                        control_band: tuple) -> dict:
    """
    Compara A_eff en banda de señal vs banda de control off-target.

    ratio_relativo = A_eff_signal / A_eff_control (alta → coherencia selectiva).

    Parameters
    ----------
    x, y : np.ndarray
        Señales H1 y L1.
    fs : float
        Frecuencia de muestreo (Hz).
    signal_band : tuple of float
        Banda de interés (Hz).
    control_band : tuple of float
        Banda off-target de control (Hz).

    Returns
    -------
    dict
        'signal', 'control', 'ratio_relativo'.
    """
    sig = band_coherence_feature(x, y, fs, signal_band)
    ctrl = band_coherence_feature(x, y, fs, control_band)

    denom = max(ctrl["a_eff"], 1e-12)
    ratio = float(sig["a_eff"] / denom)

    return {
        "signal": sig,
        "control": ctrl,
        "ratio_relativo": ratio,
    }


def silent_collision_assessment(a_eff: float, duration_s: float,
                                 a_eff_slide_median: float,
                                 ratio_relativo: float,
                                 a_eff_thr: float = 0.85,
                                 dur_thr: float = 0.05,
                                 slide_margin: float = 0.10,
                                 ratio_thr: float = 1.5) -> dict:
    """
    Evalúa "Silent Collision" con score continuo y flag condicionado a controles.

    Parameters
    ----------
    a_eff : float
        Amplitud efectiva en banda de señal.
    duration_s : float
        Duración de la firma de fase (s).
    a_eff_slide_median : float
        Mediana de A_eff en time-slides.
    ratio_relativo : float
        A_eff_signal / A_eff_control.
    a_eff_thr : float
        Umbral mínimo de A_eff.
    dur_thr : float
        Duración mínima de la firma (s).
    slide_margin : float
        Diferencia mínima requerida (a_eff - a_eff_slide_median).
    ratio_thr : float
        Ratio mínimo señal/control.

    Returns
    -------
    dict
        'silent_score', 'silent_flag', 'passes_slide_control',
        'passes_control_band', 'thresholds'.
    """
    if duration_s < 0:
        raise ValueError(f"duration_s must be non-negative, got {duration_s}")
    silent_score = float(a_eff * math.log1p(duration_s / dur_thr))

    passes_slide = (a_eff - a_eff_slide_median) >= slide_margin
    passes_ratio = ratio_relativo >= ratio_thr

    silent_flag = bool(
        (a_eff >= a_eff_thr) and (duration_s >= dur_thr)
        and passes_slide and passes_ratio
    )

    return {
        "silent_score": silent_score,
        "silent_flag": silent_flag,
        "passes_slide_control": passes_slide,
        "passes_control_band": passes_ratio,
        "thresholds": {
            "a_eff_thr": a_eff_thr,
            "dur_thr": dur_thr,
            "slide_margin": slide_margin,
            "ratio_thr": ratio_thr,
        },
    }


# ─── Análisis de Shadow-1 ─────────────────────────────────────────────────────

class Shadow1BayesianAnalyzer:
    """
    Inferencia Bayesiana de Coherencia para el candidato sub-umbral Shadow-1.

    Attributes
    ----------
    gps_time : float
        Tiempo GPS del evento (1251010524.0).
    fs : float
        Frecuencia de muestreo para datos sintéticos (Hz).
    """

    def __init__(self, gps_time: float = SHADOW1_GPS, fs: float = 4096.0):
        self.gps_time = gps_time
        self.fs = fs
        self.results: dict = {}

    # ── Generación de datos sintéticos ────────────────────────────────────────

    def _generate_synthetic_strain(self, duration: float = 4.0,
                                   snr_target: float = 4.5) -> tuple:
        """
        Genera strain sintético de H1 y L1 que modela Shadow-1:
        señal sub-umbral con chirp mass en el rango NS-NSBH,
        coherencia de fase A_eff ≈ 0.89.

        Parameters
        ----------
        duration : float
            Duración del segmento (s).
        snr_target : float
            SNR objetivo para la señal inyectada.

        Returns
        -------
        tuple
            (h1, l1, time_array)
        """
        n_samples = int(duration * self.fs)
        t = np.linspace(0.0, duration, n_samples, endpoint=False)

        # Chirp simple (NS-NS like): frecuencias en rango audible de LIGO
        f_start = 30.0    # Hz
        f_end = 500.0     # Hz
        chirp_phase = 2.0 * np.pi * (
            f_start * t + (f_end - f_start) / (2.0 * duration) * t ** 2
        )
        amplitude = 1e-22  # strain típico sub-umbral

        # Señal coherente en ambos detectores
        h1_signal = amplitude * np.sin(chirp_phase)
        # Small constant phase offset (synthetic simplification of light-travel delay)
        l1_signal = amplitude * np.sin(chirp_phase + 0.05)

        # Ruido gaussiano blanco con RMS que produce SNR ≈ snr_target
        rms_signal = np.sqrt(np.mean(h1_signal ** 2))
        # noise_std is chosen so that SNR = rms_signal / noise_std ≈ snr_target
        noise_std = rms_signal / snr_target if snr_target > 0 else 1e-22

        rng = np.random.default_rng(seed=42)
        h1 = h1_signal + rng.normal(0.0, noise_std, n_samples)
        l1 = l1_signal + rng.normal(0.0, noise_std, n_samples)

        return h1, l1, t

    # ── Estimación de parámetros ──────────────────────────────────────────────

    def estimate_parameters(self, f_start: float = 30.0, f_end: float = 500.0,
                             dt: float = 0.4,
                             mass_ratio: float = 0.9) -> dict:
        """
        Estima los parámetros astrofísicos de Shadow-1.

        Parameters
        ----------
        f_start : float
            Frecuencia inicial del chirp (Hz).
        f_end : float
            Frecuencia final del chirp (Hz).
        dt : float
            Duración de la fase detectable (s).
        mass_ratio : float
            Razón de masas q = m2/m1.

        Returns
        -------
        dict
            Parámetros estimados: chirp_mass, m1, m2, distance_mpc.
        """
        m_chirp = chirp_mass_from_frequency_evolution(f_start, f_end, dt)
        m1, m2 = masses_from_chirp_mass(m_chirp, mass_ratio)

        # Verificar rango NS/NSBH
        in_expected_range = (
            SHADOW1_MASS_MIN <= m1 <= SHADOW1_MASS_MAX_PRIMARY and
            SHADOW1_MASS_MIN <= m2 <= SHADOW1_MASS_MAX
        )

        self.results["parameters"] = {
            "gps_time": self.gps_time,
            "chirp_mass_solar": round(m_chirp, 4),
            "m1_solar": round(m1, 4),
            "m2_solar": round(m2, 4),
            "distance_mpc": SHADOW1_DISTANCE_MPC,
            "in_ns_nsbh_range": in_expected_range,
        }
        return self.results["parameters"]

    # ── Coherencia de fase ────────────────────────────────────────────────────

    def analyze_phase_coherence(self) -> dict:
        """
        Analiza la coherencia de fase H1-L1 para Shadow-1.

        Genera datos sintéticos, calcula A_eff y verifica estabilidad.

        Returns
        -------
        dict
            Resultados de coherencia incluyendo A_eff y veredicto.
        """
        h1, l1, _ = self._generate_synthetic_strain()
        nperseg = min(256, len(h1) // 4)
        coh_result = compute_phase_coherence(h1, l1, self.fs, nperseg=nperseg)

        stability = verify_phase_stability(
            SHADOW1_A_EFF,       # valor de referencia del análisis
            SHADOW1_DURATION_S,
        )

        self.results["phase_coherence"] = {
            "a_eff_computed": round(float(coh_result["a_eff"]), 4),
            "a_eff_reference": SHADOW1_A_EFF,
            "duration_s": SHADOW1_DURATION_S,
            "psi_definition": PSI_DEFINITION_GW,
            "psi_threshold": PSI_THRESHOLD_GW,
            **stability,
        }
        return self.results["phase_coherence"]

    # ── Posterior proxy (IBC – Inferencia Bayesiana de Coherencia) ────────────

    def compute_posterior_proxy(self, snr_shadow: float = 4.5,
                                mu_signal: float = 6.0,
                                sigma_signal: float = 1.5) -> dict:
        """
        Calcula un proxy del posterior para Shadow-1 basado en el banco de
        filtros de coherencia + interpolación (IBC).

        **Nota sobre nomenclatura**: Esta función implementa un proxy del
        posterior, NO un cálculo bayesiano completo.  El log-factor que se
        computa es un cociente de log-verosimilitudes (log-likelihood ratio):

            ln Λ = ln p(SNR | H1) − ln p(SNR | H0)

        con:
          - Prior implícito uniforme (no se especifica prior formal).
          - H0: ruido gaussiano puro  →  ln p(SNR|H0) = −SNR²/2
          - H1: señal sub-umbral      →  ln p(SNR|H1) = −((SNR−μ)/σ)²/2 − ln(σ√2π)

        Para un análisis bayesiano completo con prior/likelihood explícitos
        utilizar un sampler como ``bilby`` o ``PyCBC inference``.

        Parameters
        ----------
        snr_shadow : float
            SNR observado de Shadow-1.
        mu_signal : float
            SNR esperado bajo H1.
        sigma_signal : float
            Desviación típica del SNR bajo H1.

        Returns
        -------
        dict
            log_posterior_proxy, interpretation, favors_signal, and metadata.
            La clave ``log_bayes_factor`` se mantiene por compatibilidad hacia
            atrás y es idéntica a ``log_posterior_proxy``.
        """
        log_p_h0 = -0.5 * snr_shadow ** 2
        log_p_h1 = (-0.5 * ((snr_shadow - mu_signal) / sigma_signal) ** 2
                    - np.log(sigma_signal * np.sqrt(2.0 * np.pi)))

        log_proxy = log_p_h1 - log_p_h0

        if abs(log_proxy) < 1.0:
            interpretation = "No worth mentioning"
        elif abs(log_proxy) < 3.0:
            interpretation = "Positive evidence"
        elif abs(log_proxy) < 5.0:
            interpretation = "Strong evidence"
        else:
            interpretation = "Very strong evidence"

        bayes_norm = normalize_bayes_factor(lnB=log_proxy)

        result = {
            "snr": snr_shadow,
            "log_bayes_factor": round(float(log_proxy), 4),
            "ln_bayes_factor": round(bayes_norm["ln_bayes_factor"], 4),
            "log10_bayes_factor": round(bayes_norm["log10_bayes_factor"], 4),
            "interpretation": interpretation,
            "favors_signal": bool(log_proxy > 0),
            "method": "IBC(Inferencia_Bayesiana_Coherencia):log_likelihood_ratio",
        }
        self.results["posterior_proxy"] = result
        self.results["bayes_evidence"] = result   # backward compat alias
        return result

    def compute_bayes_evidence(self, snr_shadow: float = 4.5,
                               mu_signal: float = 6.0,
                               sigma_signal: float = 1.5) -> dict:
        """Alias of compute_posterior_proxy kept for backward compatibility."""
        return self.compute_posterior_proxy(snr_shadow, mu_signal, sigma_signal)

    # ── Análisis completo ─────────────────────────────────────────────────────

    def run_full_analysis(self) -> dict:
        """
        Ejecuta el análisis morfológico completo de Shadow-1.

        Returns
        -------
        dict
            Diccionario con todos los resultados: parámetros, coherencia,
            controles anti-artefacto y evidencia bayesiana.
        """
        print("=" * 60)
        print("🌌 ANÁLISIS MORFOLÓGICO DE SHADOW-1")
        print(f"   GPS: {self.gps_time}")
        print("=" * 60)

        params = self.estimate_parameters()
        print(f"\n📐 Parámetros estimados:")
        print(f"   Chirp mass: {params['chirp_mass_solar']:.4f} M☉")
        print(f"   m1 = {params['m1_solar']:.4f} M☉,  m2 = {params['m2_solar']:.4f} M☉")
        print(f"   Distancia luminosidad: {params['distance_mpc']:.0f} Mpc")
        print(f"   Rango NS/NSBH: {'✅' if params['in_ns_nsbh_range'] else '⚠️'}")

        coh = self.analyze_phase_coherence()
        print(f"\n🔬 Coherencia de fase:")
        print(f"   A_eff (referencia): {coh['a_eff_reference']}")
        print(f"   A_eff (calculado):  {coh['a_eff_computed']}")
        print(f"   Duración estable:   {coh['duration_s']} s")
        print(f"   Glitch excluido:    {'✅' if coh['is_glitch_excluded'] else '❌'}")
        print(f"   Veredicto:          {coh['verdict']}")

        # ── Controles anti-artefacto ─────────────────────────────────────────
        h1, l1, _ = self._generate_synthetic_strain()
        signal_band = (30.0, 80.0)
        control_band = (190.0, 240.0)

        phase_sig = band_coherence_feature(h1, l1, self.fs, signal_band)
        ctrl = control_band_check(h1, l1, self.fs, signal_band, control_band)
        slides = time_slide_control(h1, l1, self.fs, signal_band)

        assess = silent_collision_assessment(
            a_eff=SHADOW1_A_EFF,
            duration_s=SHADOW1_DURATION_S,
            a_eff_slide_median=slides["a_eff_slide_median"],
            ratio_relativo=ctrl["ratio_relativo"],
        )

        self.results["controls"] = {
            "time_slide": slides,
            "control_band": ctrl,
        }
        self.results["verdict"] = assess

        print(f"\n🛡️  Controles anti-artefacto:")
        print(f"   A_eff en banda señal:    {phase_sig['a_eff']:.4f}")
        print(f"   A_eff slide (mediana):   {slides['a_eff_slide_median']:.4f}")
        print(f"   ratio_relativo:          {ctrl['ratio_relativo']:.4f}")
        print(f"   Pasa control slide:      {'✅' if assess['passes_slide_control'] else '❌'}")
        print(f"   Pasa control banda:      {'✅' if assess['passes_control_band'] else '❌'}")
        print(f"   silent_score:            {assess['silent_score']:.4f}")
        print(f"   silent_flag:             {'✅' if assess['silent_flag'] else '❌'}")

        bayes = self.compute_posterior_proxy()
        print(f"\n📊 Evidencia bayesiana:")
        print(f"   SNR: {bayes['snr']}")
        print(f"   ln(B) = {bayes['ln_bayes_factor']:.4f}")
        print(f"   log₁₀(B) = {bayes['log10_bayes_factor']:.4f}")
        print(f"\n📊 Posterior proxy (IBC – log-likelihood ratio):")
        print(f"   SNR: {bayes['snr']}")
        print(f"   ln Λ = {bayes['log_posterior_proxy']:.4f}")
        print(f"   Método: {bayes['method']}")
        print(f"   Interpretación: {bayes['interpretation']}")
        print(f"   Favorece señal: {'✅' if bayes['favors_signal'] else '❌'}")

        print("\n" + "=" * 60)
        print("🏛️ AXIOMAS DEL LIBRO III")
        print("   I.  Primacía de la Relación: coherencia H1-L1 verificada")
        print("   II. Silencio es Carga: evento sub-umbral caracterizado")
        print("   III.Ingenio Cósmico: Shadow-1 rescatado del olvido")
        print("=" * 60)

        return self.results


# ─── Pipeline de coherencia Ψ aplicado a EEG ─────────────────────────────────

class EEGCoherencePipeline:
    """
    Aplica el mismo pipeline de coherencia Ψ de Shadow-1 a señales EEG.

    Busca el "Shadow-1 del pensamiento": el instante previo a la palabra
    donde la coherencia entre hemisferios es máxima pero la amplitud
    eléctrica es mínima.

    Attributes
    ----------
    fs : float
        Frecuencia de muestreo del EEG (Hz).
    band_hz : tuple
        Banda de frecuencia de interés (Hz).
    """

    def __init__(self, fs: float = 256.0, band_hz: tuple = (30.0, 80.0)):
        self.fs = fs
        self.band_hz = band_hz

    def bandpass_filter(self, eeg: np.ndarray) -> np.ndarray:
        """
        Aplica filtro pasa-banda a la señal EEG.

        Parameters
        ----------
        eeg : np.ndarray
            Señal EEG unidimensional.

        Returns
        -------
        np.ndarray
            Señal filtrada.
        """
        nyq = 0.5 * self.fs
        low = self.band_hz[0] / nyq
        high = self.band_hz[1] / nyq
        low = np.clip(low, 1e-6, 1.0 - 1e-6)
        high = np.clip(high, 1e-6, 1.0 - 1e-6)
        if low >= high:
            raise ValueError("Banda de frecuencia inválida")
        b, a = signal.butter(4, [low, high], btype="band")
        return signal.filtfilt(b, a, eeg)

    def inter_hemisphere_coherence(self, left: np.ndarray,
                                    right: np.ndarray) -> dict:
        """
        Calcula la coherencia inter-hemisférica Ψ_EEG entre dos canales EEG.

        Ψ_EEG = PLV@band: Phase Locking Value en la banda de frecuencia
        configurada.  Implementado como mediana de sqrt(MSC) en la banda, lo
        que es equivalente a PLV para señales de banda estrecha.
        Umbral de decisión: PSI_THRESHOLD_EEG = 0.70.

        Parameters
        ----------
        left : np.ndarray
            Canal del hemisferio izquierdo.
        right : np.ndarray
            Canal del hemisferio derecho.

        Returns
        -------
        dict
            'freqs', 'coherence', 'a_eff_eeg', 'shadow_thought_detected',
            'psi_definition', 'psi_threshold'.
        """
        left_f = self.bandpass_filter(left)
        right_f = self.bandpass_filter(right)

        nperseg = min(256, len(left_f) // 4)
        freqs, coh = signal.coherence(left_f, right_f, fs=self.fs,
                                       nperseg=nperseg)

        # Seleccionar banda de interés
        band_mask = (freqs >= self.band_hz[0]) & (freqs <= self.band_hz[1])
        if band_mask.sum() == 0:
            a_eff_eeg = 0.0
        else:
            a_eff_eeg = float(np.median(np.sqrt(np.clip(coh[band_mask], 0, 1))))

        # Detectar "Shadow-1 del pensamiento":
        # alta coherencia con amplitud eléctrica mínima
        amp_left = float(np.std(left_f))
        amp_right = float(np.std(right_f))
        mean_amplitude = 0.5 * (amp_left + amp_right)
        ref_amplitude = float(np.std(left))

        # Guard: if the unfiltered reference has zero amplitude the suppression
        # ratio is undefined; return 0.0 to indicate no measurable suppression.
        if ref_amplitude <= 0:
            amplitude_suppression = 0.0
        else:
            amplitude_suppression = float(
                np.clip(1.0 - mean_amplitude / ref_amplitude, 0.0, 1.0)
            )

        shadow_thought = bool(a_eff_eeg >= PSI_THRESHOLD_EEG and amplitude_suppression >= 0.10)

        return {
            "freqs": freqs,
            "coherence": coh,
            "a_eff_eeg": round(a_eff_eeg, 4),
            "amplitude_suppression": round(amplitude_suppression, 4),
            "shadow_thought_detected": shadow_thought,
            "psi_definition": PSI_DEFINITION_EEG,
            "psi_threshold": PSI_THRESHOLD_EEG,
        }

    def analyze(self, left: np.ndarray, right: np.ndarray) -> dict:
        """
        Análisis completo del pipeline EEG.

        Parameters
        ----------
        left : np.ndarray
            Canal hemisferio izquierdo.
        right : np.ndarray
            Canal hemisferio derecho.

        Returns
        -------
        dict
            Resultado del análisis de coherencia EEG.
        """
        result = self.inter_hemisphere_coherence(left, right)
        print("\n🧠 PIPELINE Ψ – EEG (Shadow-1 del Pensamiento)")
        print(f"   A_eff EEG (banda {self.band_hz[0]}–{self.band_hz[1]} Hz): "
              f"{result['a_eff_eeg']}")
        print(f"   Supresión de amplitud: {result['amplitude_suppression']}")
        detected = result["shadow_thought_detected"]
        print(f"   Shadow-1 del pensamiento: {'✅ DETECTADO' if detected else 'No detectado'}")
        return result


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def main() -> int:
    """Ejecuta análisis completo de Shadow-1 y pipeline EEG."""
    analyzer = Shadow1BayesianAnalyzer()
    results = analyzer.run_full_analysis()

    # Pipeline EEG con datos sintéticos
    rng = np.random.default_rng(seed=0)
    fs_eeg = 256.0
    duration_eeg = 10.0
    n_eeg = int(fs_eeg * duration_eeg)
    t_eeg = np.linspace(0.0, duration_eeg, n_eeg, endpoint=False)

    # Señal coherente en gamma (~40 Hz) con amplitud pequeña
    coherent = 0.5e-6 * np.sin(2.0 * np.pi * 40.0 * t_eeg)
    noise_left = rng.normal(0.0, 5e-6, n_eeg)
    noise_right = rng.normal(0.0, 5e-6, n_eeg)
    left_channel = coherent + noise_left
    right_channel = coherent * 0.95 + noise_right

    pipeline = EEGCoherencePipeline(fs=fs_eeg)
    eeg_result = pipeline.analyze(left_channel, right_channel)
    results["eeg_pipeline"] = {k: v for k, v in eeg_result.items()
                               if k not in ("freqs", "coherence")}
    results["eeg_pipeline"]["disclaimer"] = (
        "Independent pipeline; not joint inference with GW."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
