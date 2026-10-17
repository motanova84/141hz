"""
test_coherence_field.py — pytest suite for qcal/spectrum/resonance_engine.py

Tests
-----
Test 1 — Normalisation and spectral convergence (synthetic in-phase signals).
Test 2 — Phase convergence: detuned signals converge to Ψ = 0.999999 at f₀.
Test 3 — Noise resistance: white Gaussian noise is rejected; Ψ ≥ 0.999999.
"""

import json
import os

import numpy as np
import pytest

from qcal.spectrum.resonance_engine import (
    F0,
    PSI_THRESHOLD,
    compute_coherence,
    spectral_transform,
)

# ---------------------------------------------------------------------------
# Constants from config
# ---------------------------------------------------------------------------
_CONFIG_PATH_T = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "qcal", "config", "constants.json")
)
with open(_CONFIG_PATH_T) as _fp_t:
    _CONFIG = json.load(_fp_t)
FS = _CONFIG["nyquist_min_fs_hz"] * 4  # 1133.6008 Hz — well above Nyquist
DURATION = 5.0                          # seconds of synthetic signal
N = int(FS * DURATION)
T = np.linspace(0, DURATION, N, endpoint=False)

PSI_MARGIN = 1e-6  # tolerance used in assertions


def _pure_tone(freq: float = F0, phase: float = 0.0) -> np.ndarray:
    """Return a unit-amplitude pure tone at *freq* Hz with given phase offset."""
    return np.sin(2 * np.pi * freq * T + phase)


# ---------------------------------------------------------------------------
# Test 1: Normalisation — in-phase signals at f₀ yield Ψ = 1
# ---------------------------------------------------------------------------

class TestNormalisationAndNullGeodesic:
    """Verify that identical in-phase signals achieve perfect coherence."""

    def test_identical_signals_psi_equals_one(self):
        sig = _pure_tone()
        psi, delta_f, is_coherent = compute_coherence(sig, sig.copy(), FS)
        assert abs(psi - 1.0) < PSI_MARGIN, f"Ψ={psi} expected ≈ 1.0"

    def test_is_coherent_flag_set(self):
        sig = _pure_tone()
        _, _, is_coherent = compute_coherence(sig, sig.copy(), FS)
        assert is_coherent

    def test_delta_f_near_zero_for_pure_f0(self):
        sig = _pure_tone()
        _, delta_f, _ = compute_coherence(sig, sig.copy(), FS)
        # Peak detection resolution is bounded by frequency bin width = 1/duration
        assert delta_f < 1.0 / DURATION + 1.0, f"Δf={delta_f} Hz unexpectedly large"

    def test_sampling_rate_below_nyquist_raises(self):
        sig = _pure_tone()
        with pytest.raises(ValueError, match="Nyquist"):
            compute_coherence(sig, sig.copy(), fs=100.0)

    def test_spectral_transform_peak_at_f0(self):
        sig = _pure_tone()
        freqs, mags, f_peak = spectral_transform(sig, FS)
        assert abs(f_peak - F0) < 1.0, f"Spectral peak {f_peak} Hz ≠ f₀ {F0} Hz"


# ---------------------------------------------------------------------------
# Test 2: Spectral phase convergence
# ---------------------------------------------------------------------------

class TestSpectralPhaseConvergence:
    """
    Inject phase-shifted versions of the same f₀ tone.
    After bandpass projection the coherence must recover to ≥ 0.999999.
    """

    @pytest.mark.parametrize("phase_offset", [
        np.pi / 6,   # 30°
        np.pi / 4,   # 45°
        np.pi / 3,   # 60°
        np.pi / 2,   # 90°
    ])
    def test_phase_offset_psi_recovers(self, phase_offset):
        s_luz = _pure_tone(F0, phase=0.0)
        s_obs = _pure_tone(F0, phase=phase_offset)
        psi, delta_f, is_coherent = compute_coherence(s_luz, s_obs, FS, adaptive=True)
        # After projection onto f₀ eigenmode the signals become co-linear
        assert psi >= PSI_THRESHOLD - PSI_MARGIN, (
            f"Ψ={psi:.8f} below threshold {PSI_THRESHOLD} for phase_offset={phase_offset:.4f} rad"
        )
        assert is_coherent, f"is_coherent=False for phase_offset={phase_offset:.4f} rad"

    def test_delta_f_within_tolerance(self):
        """Central frequency deviation must be < 1 Hz for a pure f₀ signal."""
        s_luz = _pure_tone(F0)
        s_obs = _pure_tone(F0, phase=np.pi / 4)
        _, delta_f, _ = compute_coherence(s_luz, s_obs, FS, adaptive=True)
        assert delta_f < 1.0, f"Δf={delta_f} Hz exceeds tolerance"

    def test_off_frequency_signal_incoherent_without_filter(self):
        """Off-frequency signals without adaptive filter should yield low Ψ."""
        s_luz = _pure_tone(F0)
        s_obs = _pure_tone(F0 * 2)  # harmonic — clearly different
        psi, _, _ = compute_coherence(s_luz, s_obs, FS, adaptive=False)
        assert psi < 0.5, f"Expected low Ψ for off-frequency signal, got {psi}"


# ---------------------------------------------------------------------------
# Test 3: Noise resistance (adaptive auto-adjustment)
# ---------------------------------------------------------------------------

class TestNoiseResistance:
    """
    Mix f₀ signal with uncorrelated white Gaussian noise.
    At high SNR (≥ 40 dB) the adaptive demodulation filter maintains Ψ ≥ 0.999999.
    At moderate SNR the adaptive filter significantly improves Ψ over the raw signal.
    """

    @pytest.mark.parametrize("snr_db", [60, 50, 40])
    def test_high_snr_psi_above_threshold(self, snr_db):
        rng = np.random.default_rng(seed=42)
        signal_power = 0.5  # sin² average
        noise_power = signal_power / (10 ** (snr_db / 10.0))
        noise_std = np.sqrt(noise_power)

        s_luz = _pure_tone(F0) + rng.normal(0, noise_std, N)
        s_obs = _pure_tone(F0) + rng.normal(0, noise_std, N)

        psi, _, is_coherent = compute_coherence(s_luz, s_obs, FS, adaptive=True)
        assert psi >= PSI_THRESHOLD - PSI_MARGIN, (
            f"Ψ={psi:.8f} below threshold at SNR={snr_db} dB"
        )
        assert is_coherent, f"is_coherent=False at SNR={snr_db} dB"

    @pytest.mark.parametrize("snr_db", [20, 10])
    def test_moderate_snr_filter_improves_psi(self, snr_db):
        """Adaptive filter must improve Ψ significantly over the unfiltered case."""
        rng = np.random.default_rng(seed=7)
        signal_power = 0.5
        noise_power = signal_power / (10 ** (snr_db / 10.0))
        noise_std = np.sqrt(noise_power)

        s_luz = _pure_tone(F0) + rng.normal(0, noise_std, N)
        s_obs = _pure_tone(F0) + rng.normal(0, noise_std, N)

        psi_raw, _, _ = compute_coherence(s_luz, s_obs, FS, adaptive=False)
        psi_filt, _, _ = compute_coherence(s_luz, s_obs, FS, adaptive=True)

        assert psi_filt > psi_raw, (
            f"Adaptive filter did not improve Ψ at SNR={snr_db} dB "
            f"(raw={psi_raw:.6f}, filtered={psi_filt:.6f})"
        )

    def test_pure_noise_incoherent_without_filter(self):
        """Two independent noise signals should not be coherent without filtering."""
        rng = np.random.default_rng(seed=0)
        s1 = rng.normal(0, 1, N)
        s2 = rng.normal(0, 1, N)
        psi, _, _ = compute_coherence(s1, s2, FS, adaptive=False)
        assert psi < 0.5, f"Independent noise gave Ψ={psi}, expected < 0.5"
