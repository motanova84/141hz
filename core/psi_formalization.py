#!/usr/bin/env python3
"""
core/psi_formalization.py - Rigorous Mathematical Formalization of Ψ

Provides a publication-ready formalization of the Ψ coherence field operator
for the QCAL ∞³ system. All terms are operationally defined, a dimensionless
form is provided for cross-system comparison, and three experimentally
falsifiable predictions are implemented.

Mathematical Framework
----------------------
Time-averaged coherence amplitude (operational definition):

    A_eff² = (1/T) ∫₀ᵀ |a(t)|² dt

Full Ψ (with physical dimensions of energy):

    Ψ = mc² · A_eff² · π

Dimensionless form (publication form, range [0, π]):

    Ψ̃ = π · A_eff²

Falsifiable Predictions
-----------------------
P1 – Energy scaling:  Ψ ∝ m at fixed coherence (linear mass dependence)
P2 – Coherence sensitivity: coherent fields distinguishable from random
     noise via the dominant spectral peak at f₀
P3 – Spectral peak:  dominant component at f₀ = 141.7001 Hz in coherent
     systems (QCAL hypothesis validation)

QCAL Integration Constants
---------------------------
    f₀              = 141.7001 Hz  (QCAL_BASE_FREQUENCY)
    Ψ̃_threshold    = 0.888         (coherence detection)
    r_spectral_thr  = 0.0888        (f₀-peak detection)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: MIT
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Physical and QCAL constants
# ---------------------------------------------------------------------------

#: Speed of light (m/s)
C_LIGHT: float = 2.99792458e8

#: QCAL fundamental frequency (Hz)
QCAL_BASE_FREQUENCY: float = 141.7001

#: Dimensionless Ψ̃ coherence threshold (existing QCAL standard)
PSI_TILDE_THRESHOLD: float = 0.888

#: Spectral ratio threshold for f₀-peak detection (existing QCAL standard)
SPECTRAL_RATIO_THRESHOLD: float = 0.0888

# ---------------------------------------------------------------------------
# Data container
# ---------------------------------------------------------------------------


@dataclass
class PsiMetrics:
    """
    Container for all Ψ-related metrics computed from a time series.

    Attributes
    ----------
    psi : float
        Full Ψ value (energy units, Joules) = mc² · A_eff² · π
    psi_tilde : float
        Dimensionless Ψ̃ = π · A_eff².  Range: [0, π].
    A_eff_squared : float
        Time-averaged squared coherence amplitude = (1/T) ∫|a(t)|² dt
    is_coherent : bool
        True when Ψ̃ ≥ PSI_TILDE_THRESHOLD (0.888)
    f0_detected : bool
        True when dominant spectral power fraction at f₀ ≥
        SPECTRAL_RATIO_THRESHOLD (0.0888)
    dominant_frequency : float
        Frequency (Hz) of the largest spectral component
    spectral_ratio : float
        Fraction of total spectral power concentrated at f₀ (±Δf)
    mass_kg : float
        System mass used to compute Ψ (kg)
    duration_s : float
        Analysis window duration T (s)
    sampling_rate_hz : float
        Sampling rate fs (Hz)
    n_samples : int
        Number of samples in the time series
    """

    psi: float = 0.0
    psi_tilde: float = 0.0
    A_eff_squared: float = 0.0
    is_coherent: bool = False
    f0_detected: bool = False
    dominant_frequency: float = 0.0
    spectral_ratio: float = 0.0
    mass_kg: float = 1.0
    duration_s: float = 1.0
    sampling_rate_hz: float = 1000.0
    n_samples: int = 0


# ---------------------------------------------------------------------------
# Signal generation utilities
# ---------------------------------------------------------------------------


def generate_coherent_signal(
    duration: float = 1.0,
    fs: float = 1000.0,
    f0: float = QCAL_BASE_FREQUENCY,
    amplitude: float = 1.0,
    noise_level: float = 0.05,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a coherent sinusoidal signal at frequency *f0* with additive noise.

    Parameters
    ----------
    duration : float
        Duration of the signal in seconds.
    fs : float
        Sampling rate in Hz.
    f0 : float
        Fundamental frequency in Hz (default: QCAL_BASE_FREQUENCY).
    amplitude : float
        Peak amplitude of the coherent component.
    noise_level : float
        Standard deviation of additive Gaussian noise relative to *amplitude*.
    rng : numpy.random.Generator, optional
        Random number generator for reproducibility.

    Returns
    -------
    t : np.ndarray
        Time vector (s).
    a_t : np.ndarray
        Signal samples ``a_t = signal + noise``. For a pure sine with
        ``amplitude = 1`` and ``noise_level = 0``, A_eff² ≈ 0.5.
    """
    if rng is None:
        rng = np.random.default_rng()

    n = int(duration * fs)
    t = np.arange(n) / fs
    signal = amplitude * np.sin(2.0 * np.pi * f0 * t)
    noise = noise_level * amplitude * rng.standard_normal(n)
    a_t = signal + noise
    return t, a_t


def generate_incoherent_signal(
    duration: float = 1.0,
    fs: float = 1000.0,
    amplitude: float = 1.0,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a purely incoherent (white-noise) signal.

    Parameters
    ----------
    duration : float
        Duration in seconds.
    fs : float
        Sampling rate in Hz.
    amplitude : float
        Standard deviation of the white-noise signal.
    rng : numpy.random.Generator, optional
        Random number generator.

    Returns
    -------
    t : np.ndarray
        Time vector (s).
    a_t : np.ndarray
        White-noise signal.
    """
    if rng is None:
        rng = np.random.default_rng()

    n = int(duration * fs)
    t = np.arange(n) / fs
    a_t = amplitude * rng.standard_normal(n)
    return t, a_t


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------


def compute_A_eff_squared(
    a_t: np.ndarray,
    T: float,
) -> float:
    """
    Compute the time-averaged squared coherence amplitude.

    Operational definition::

        A_eff² = (1/T) ∫₀ᵀ |a(t)|² dt  ≈  mean(|a_t|²)

    Parameters
    ----------
    a_t : array-like
        Time series of the coherence amplitude *a(t)*.
    T : float
        Duration of the analysis window in seconds.  Must be > 0.

    Returns
    -------
    float
        A_eff² ≥ 0.
    """
    a = np.asarray(a_t)
    if T <= 0:
        raise ValueError(f"Duration T must be positive, got {T}")
    if a.size == 0:
        raise ValueError("Time series a_t must not be empty")
    return float(np.mean(np.abs(a) ** 2))


def _compute_spectral_metrics(
    a_t: np.ndarray,
    fs: float,
    f0: float = QCAL_BASE_FREQUENCY,
    bandwidth: float = 1.0,
) -> Tuple[float, float]:
    """
    Compute spectral metrics for f₀-peak detection.

    Parameters
    ----------
    a_t : np.ndarray
        Time series.
    fs : float
        Sampling rate (Hz).
    f0 : float
        Target frequency (Hz).
    bandwidth : float
        Half-bandwidth (Hz) around f₀ used to accumulate peak power.

    Returns
    -------
    dominant_frequency : float
        Frequency of the bin with maximum power (Hz).
    spectral_ratio : float
        Fraction of total power within [f₀ − bandwidth, f₀ + bandwidth].
    """
    n = len(a_t)
    if n < 2:
        return 0.0, 0.0

    spectrum = np.abs(np.fft.rfft(a_t)) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)

    total_power = float(np.sum(spectrum))
    if total_power == 0.0:
        return 0.0, 0.0

    dominant_frequency = float(freqs[np.argmax(spectrum)])

    mask = np.abs(freqs - f0) <= bandwidth
    peak_power = float(np.sum(spectrum[mask]))
    spectral_ratio = peak_power / total_power

    return dominant_frequency, spectral_ratio


def compute_psi_from_timeseries(
    a_t: Sequence[float],
    T: float = 1.0,
    fs: float = 1000.0,
    mass: float = 1e-12,
    f0: float = QCAL_BASE_FREQUENCY,
    psi_tilde_threshold: float = PSI_TILDE_THRESHOLD,
    spectral_ratio_threshold: float = SPECTRAL_RATIO_THRESHOLD,
    spectral_bandwidth: float = 1.0,
) -> PsiMetrics:
    """
    Compute all Ψ metrics from a coherence-amplitude time series.

    Parameters
    ----------
    a_t : array-like
        Time series of coherence amplitude *a(t)* sampled over duration T.
    T : float
        Analysis window duration in seconds.
    fs : float
        Sampling rate in Hz.
    mass : float
        System mass in kg (used for dimensional Ψ).
    f0 : float
        QCAL fundamental frequency for spectral-peak detection (Hz).
    psi_tilde_threshold : float
        Ψ̃ threshold above which the system is classified as coherent.
    spectral_ratio_threshold : float
        Spectral-ratio threshold for f₀-peak detection.
    spectral_bandwidth : float
        Half-bandwidth (Hz) used for spectral-peak integration.

    Returns
    -------
    PsiMetrics
        All Ψ-related metrics.

    Notes
    -----
    Equations::

        A_eff² = (1/T) ∫₀ᵀ |a(t)|² dt   [operational definition]
        Ψ      = mc² · A_eff² · π         [energy form]
        Ψ̃     = π  · A_eff²              [dimensionless, ∈ [0, π]]
    """
    a = np.asarray(a_t, dtype=float)

    A_eff_sq = compute_A_eff_squared(a, T)

    psi_tilde = np.pi * A_eff_sq
    psi = mass * C_LIGHT ** 2 * A_eff_sq * np.pi

    is_coherent = psi_tilde >= psi_tilde_threshold

    dominant_freq, spectral_ratio = _compute_spectral_metrics(
        a, fs, f0=f0, bandwidth=spectral_bandwidth
    )
    f0_detected = spectral_ratio >= spectral_ratio_threshold

    return PsiMetrics(
        psi=float(psi),
        psi_tilde=float(psi_tilde),
        A_eff_squared=float(A_eff_sq),
        is_coherent=bool(is_coherent),
        f0_detected=bool(f0_detected),
        dominant_frequency=float(dominant_freq),
        spectral_ratio=float(spectral_ratio),
        mass_kg=float(mass),
        duration_s=float(T),
        sampling_rate_hz=float(fs),
        n_samples=int(a.size),
    )


# ---------------------------------------------------------------------------
# Falsifiable predictions
# ---------------------------------------------------------------------------


def test_prediction_p1_energy_scaling(
    a_t: Sequence[float],
    masses: Sequence[float],
    T: float = 1.0,
    fs: float = 1000.0,
    tolerance: float = 1e-6,
) -> dict:
    """
    P1 – Energy-scaling prediction: Ψ ∝ m at fixed coherence.

    Computes Ψ for each mass in *masses* and verifies that the
    mass-normalised value Ψ/m is constant (linear dependence).

    Parameters
    ----------
    a_t : array-like
        Fixed coherence-amplitude time series.
    masses : array-like
        Sequence of system masses (kg) to test.
    T : float
        Duration (s).
    fs : float
        Sampling rate (Hz).
    tolerance : float
        Maximum allowed relative deviation in Ψ/m across masses.

    Returns
    -------
    dict
        Keys:
        ``passed`` (bool) – prediction verified,
        ``psi_per_mass`` (list[float]) – Ψ/m values,
        ``relative_deviation`` (float) – max relative deviation,
        ``masses`` (list[float]) – input masses,
        ``psi_values`` (list[float]) – computed Ψ values.
    """
    masses_arr = np.asarray(masses, dtype=float)
    if masses_arr.size < 2:
        raise ValueError("At least two mass values are required for P1.")
    if np.any(masses_arr <= 0):
        raise ValueError("All masses must be positive.")

    psi_values = []
    for m in masses_arr:
        metrics = compute_psi_from_timeseries(a_t, T=T, fs=fs, mass=float(m))
        psi_values.append(metrics.psi)

    psi_arr = np.array(psi_values)
    psi_per_mass = psi_arr / masses_arr

    # Relative deviation from the mean
    mean_ratio = float(np.mean(psi_per_mass))
    if mean_ratio == 0.0:
        relative_deviation = 0.0
    else:
        relative_deviation = float(
            np.max(np.abs(psi_per_mass - mean_ratio)) / mean_ratio
        )

    passed = relative_deviation <= tolerance

    return {
        "passed": passed,
        "psi_per_mass": psi_per_mass.tolist(),
        "relative_deviation": relative_deviation,
        "masses": masses_arr.tolist(),
        "psi_values": psi_arr.tolist(),
    }


def test_prediction_p2_coherence_sensitivity(
    a_coherent: Sequence[float],
    a_incoherent: Sequence[float],
    T: float = 1.0,
    fs: float = 1000.0,
    f0: float = QCAL_BASE_FREQUENCY,
) -> dict:
    """
    P2 – Coherence-sensitivity prediction.

    Coherent fields must be distinguishable from random (incoherent) noise
    via the dominant spectral peak at f₀.  Specifically:

    * The coherent signal must have f₀ detected (spectral_ratio ≥ threshold).
    * The incoherent signal must *not* have f₀ detected.

    Parameters
    ----------
    a_coherent : array-like
        Time series from a coherent (organised) field.
    a_incoherent : array-like
        Time series from an incoherent (random) field.
    T : float
        Duration (s).
    fs : float
        Sampling rate (Hz).
    f0 : float
        Target frequency (Hz).

    Returns
    -------
    dict
        Keys:
        ``passed`` (bool),
        ``coherent_f0_detected`` (bool),
        ``incoherent_f0_detected`` (bool),
        ``coherent_spectral_ratio`` (float),
        ``incoherent_spectral_ratio`` (float),
        ``coherent_psi_tilde`` (float),
        ``incoherent_psi_tilde`` (float).
    """
    m_coh = compute_psi_from_timeseries(a_coherent, T=T, fs=fs, f0=f0)
    m_inc = compute_psi_from_timeseries(a_incoherent, T=T, fs=fs, f0=f0)

    passed = m_coh.f0_detected and not m_inc.f0_detected

    return {
        "passed": passed,
        "coherent_f0_detected": m_coh.f0_detected,
        "incoherent_f0_detected": m_inc.f0_detected,
        "coherent_spectral_ratio": m_coh.spectral_ratio,
        "incoherent_spectral_ratio": m_inc.spectral_ratio,
        "coherent_psi_tilde": m_coh.psi_tilde,
        "incoherent_psi_tilde": m_inc.psi_tilde,
    }


def test_prediction_p3_spectral_peak(
    a_t: Sequence[float],
    fs: float = 1000.0,
    f0: float = QCAL_BASE_FREQUENCY,
    bandwidth: float = 1.0,
) -> dict:
    """
    P3 – Spectral-peak prediction.

    In coherent systems the dominant spectral component must be at
    f₀ = 141.7001 Hz (QCAL hypothesis).

    Parameters
    ----------
    a_t : array-like
        Time series.
    fs : float
        Sampling rate (Hz).
    f0 : float
        Expected fundamental frequency (Hz).
    bandwidth : float
        Tolerance window (Hz) around f₀.

    Returns
    -------
    dict
        Keys:
        ``passed`` (bool) – dominant frequency is within bandwidth of f₀,
        ``dominant_frequency`` (float),
        ``f0_expected`` (float),
        ``frequency_error`` (float) – |f_dom − f₀|,
        ``bandwidth`` (float),
        ``spectral_ratio`` (float),
        ``f0_detected`` (bool).
    """
    a = np.asarray(a_t, dtype=float)
    dominant_freq, spectral_ratio = _compute_spectral_metrics(
        a, fs, f0=f0, bandwidth=bandwidth
    )
    freq_error = abs(dominant_freq - f0)
    passed = freq_error <= bandwidth

    return {
        "passed": passed,
        "dominant_frequency": dominant_freq,
        "f0_expected": f0,
        "frequency_error": freq_error,
        "bandwidth": bandwidth,
        "spectral_ratio": spectral_ratio,
        "f0_detected": spectral_ratio >= SPECTRAL_RATIO_THRESHOLD,
    }
