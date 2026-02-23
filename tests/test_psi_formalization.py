#!/usr/bin/env python3
"""
tests/test_psi_formalization.py - Tests for core/psi_formalization.py

Validates the rigorous mathematical formalization of Ψ including:
- Operational definition of A_eff²
- Dimensional and dimensionless Ψ forms
- PsiMetrics dataclass structure
- Coherence and spectral-peak detection
- Falsifiable predictions P1, P2, P3
"""

import math

import numpy as np
import pytest
import core.psi_formalization as psi_mod
from core.psi_formalization import (
    QCAL_BASE_FREQUENCY,
    PSI_TILDE_THRESHOLD,
    SPECTRAL_RATIO_THRESHOLD,
    C_LIGHT,
    PsiMetrics,
    compute_A_eff_squared,
    compute_psi_from_timeseries,
    generate_coherent_signal,
    generate_incoherent_signal,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DURATION = 1.0
FS = 1000.0
MASS = 1e-12  # 1 picogram
RNG = np.random.default_rng(42)


@pytest.fixture
def coherent_signal():
    _, a_t = generate_coherent_signal(
        duration=DURATION, fs=FS, f0=QCAL_BASE_FREQUENCY,
        amplitude=1.0, noise_level=0.01, rng=np.random.default_rng(0)
    )
    return a_t


@pytest.fixture
def incoherent_signal():
    _, a_t = generate_incoherent_signal(
        duration=DURATION, fs=FS, amplitude=1.0,
        rng=np.random.default_rng(1)
    )
    return a_t


# ---------------------------------------------------------------------------
# TestConstants
# ---------------------------------------------------------------------------

class TestConstants:
    """Validate module-level constants."""

    def test_qcal_base_frequency(self):
        assert QCAL_BASE_FREQUENCY == pytest.approx(141.7001, rel=1e-6)

    def test_psi_tilde_threshold(self):
        assert PSI_TILDE_THRESHOLD == pytest.approx(0.888, rel=1e-6)

    def test_spectral_ratio_threshold(self):
        assert SPECTRAL_RATIO_THRESHOLD == pytest.approx(0.0888, rel=1e-6)

    def test_c_light(self):
        assert C_LIGHT == pytest.approx(2.99792458e8, rel=1e-9)


# ---------------------------------------------------------------------------
# TestPsiMetrics
# ---------------------------------------------------------------------------

class TestPsiMetrics:
    """Validate PsiMetrics dataclass."""

    def test_default_construction(self):
        m = PsiMetrics()
        assert m.psi == 0.0
        assert m.psi_tilde == 0.0
        assert m.A_eff_squared == 0.0
        assert m.is_coherent is False
        assert m.f0_detected is False

    def test_all_fields_settable(self):
        m = PsiMetrics(
            psi=1.0, psi_tilde=2.0, A_eff_squared=0.5,
            is_coherent=True, f0_detected=True,
            dominant_frequency=141.7, spectral_ratio=0.5,
            mass_kg=1e-12, duration_s=1.0, sampling_rate_hz=1000.0,
            n_samples=1000
        )
        assert m.psi == 1.0
        assert m.psi_tilde == 2.0
        assert m.A_eff_squared == 0.5
        assert m.is_coherent is True
        assert m.f0_detected is True
        assert m.n_samples == 1000


# ---------------------------------------------------------------------------
# TestComputeAEffSquared
# ---------------------------------------------------------------------------

class TestComputeAEffSquared:
    """Tests for compute_A_eff_squared()."""

    def test_zero_signal(self):
        a = np.zeros(100)
        assert compute_A_eff_squared(a, T=1.0) == pytest.approx(0.0)

    def test_unit_constant_signal(self):
        a = np.ones(100)
        assert compute_A_eff_squared(a, T=1.0) == pytest.approx(1.0)

    def test_pure_sine_half_amplitude(self):
        # Pure sine: mean(sin²) = 0.5
        t = np.linspace(0, 1, 10000, endpoint=False)
        a = np.sin(2 * np.pi * 141.7001 * t)
        result = compute_A_eff_squared(a, T=1.0)
        assert result == pytest.approx(0.5, rel=1e-3)

    def test_scaled_signal(self):
        t = np.linspace(0, 1, 1000, endpoint=False)
        a = 3.0 * np.sin(2 * np.pi * 50 * t)
        # mean(9 sin²) = 4.5
        assert compute_A_eff_squared(a, T=1.0) == pytest.approx(4.5, rel=1e-3)

    def test_negative_T_raises(self):
        with pytest.raises(ValueError):
            compute_A_eff_squared(np.ones(10), T=-1.0)

    def test_zero_T_raises(self):
        with pytest.raises(ValueError):
            compute_A_eff_squared(np.ones(10), T=0.0)

    def test_empty_signal_raises(self):
        with pytest.raises(ValueError):
            compute_A_eff_squared(np.array([]), T=1.0)

    def test_T_does_not_change_mean_result(self):
        a = np.ones(100)
        # A_eff² is mean(|a|²) regardless of T; T is retained for dimensional use
        r1 = compute_A_eff_squared(a, T=1.0)
        r2 = compute_A_eff_squared(a, T=2.0)
        assert r1 == pytest.approx(r2)


# ---------------------------------------------------------------------------
# TestComputePsiFromTimeseries
# ---------------------------------------------------------------------------

class TestComputePsiFromTimeseries:
    """Tests for compute_psi_from_timeseries()."""

    def test_returns_psi_metrics(self, coherent_signal):
        result = compute_psi_from_timeseries(coherent_signal, T=DURATION, fs=FS)
        assert isinstance(result, PsiMetrics)

    def test_psi_tilde_formula(self, coherent_signal):
        result = compute_psi_from_timeseries(coherent_signal, T=DURATION, fs=FS)
        expected = math.pi * result.A_eff_squared
        assert result.psi_tilde == pytest.approx(expected, rel=1e-10)

    def test_psi_formula(self, coherent_signal):
        m = 1e-10
        result = compute_psi_from_timeseries(
            coherent_signal, T=DURATION, fs=FS, mass=m
        )
        expected = m * C_LIGHT ** 2 * result.A_eff_squared * math.pi
        assert result.psi == pytest.approx(expected, rel=1e-10)

    def test_psi_tilde_range_coherent(self, coherent_signal):
        result = compute_psi_from_timeseries(coherent_signal, T=DURATION, fs=FS)
        assert 0.0 <= result.psi_tilde <= math.pi + 1e-9

    def test_psi_tilde_range_incoherent(self, incoherent_signal):
        result = compute_psi_from_timeseries(incoherent_signal, T=DURATION, fs=FS)
        assert result.psi_tilde >= 0.0

    def test_metadata_stored(self, coherent_signal):
        result = compute_psi_from_timeseries(
            coherent_signal, T=DURATION, fs=FS, mass=MASS
        )
        assert result.mass_kg == MASS
        assert result.duration_s == DURATION
        assert result.sampling_rate_hz == FS
        assert result.n_samples == len(coherent_signal)

    def test_coherent_flag_above_threshold(self):
        # Amplitude 1 → A_eff² ≈ 0.5 → Ψ̃ ≈ 1.57 > 0.888
        _, a_t = generate_coherent_signal(
            duration=1.0, fs=FS, f0=QCAL_BASE_FREQUENCY,
            amplitude=1.0, noise_level=0.0
        )
        result = compute_psi_from_timeseries(a_t, T=1.0, fs=FS)
        assert result.is_coherent is True

    def test_coherent_flag_below_threshold(self):
        # Very small amplitude → Ψ̃ well below 0.888
        a_t = np.zeros(1000)
        result = compute_psi_from_timeseries(a_t, T=1.0, fs=FS)
        assert result.is_coherent is False

    def test_f0_detected_coherent_signal(self):
        _, a_t = generate_coherent_signal(
            duration=1.0, fs=FS, f0=QCAL_BASE_FREQUENCY,
            amplitude=1.0, noise_level=0.0
        )
        result = compute_psi_from_timeseries(a_t, T=1.0, fs=FS)
        assert result.f0_detected is True

    def test_f0_not_detected_incoherent_signal(self, incoherent_signal):
        result = compute_psi_from_timeseries(
            incoherent_signal, T=DURATION, fs=FS
        )
        # White noise should not have a dominant peak at f₀
        assert result.f0_detected is False

    def test_dominant_frequency_near_f0(self):
        _, a_t = generate_coherent_signal(
            duration=1.0, fs=FS, f0=QCAL_BASE_FREQUENCY,
            amplitude=1.0, noise_level=0.0
        )
        result = compute_psi_from_timeseries(a_t, T=1.0, fs=FS)
        assert abs(result.dominant_frequency - QCAL_BASE_FREQUENCY) < 1.0

    def test_zero_signal_is_not_coherent(self):
        a_t = np.zeros(1000)
        result = compute_psi_from_timeseries(a_t, T=1.0, fs=FS)
        assert result.psi == 0.0
        assert result.psi_tilde == 0.0
        assert result.is_coherent is False


# ---------------------------------------------------------------------------
# TestGenerateCoherentSignal
# ---------------------------------------------------------------------------

class TestGenerateCoherentSignal:
    """Tests for generate_coherent_signal()."""

    def test_returns_tuple(self):
        t, a = generate_coherent_signal()
        assert isinstance(t, np.ndarray)
        assert isinstance(a, np.ndarray)

    def test_correct_length(self):
        t, a = generate_coherent_signal(duration=2.0, fs=500.0)
        assert len(t) == 1000
        assert len(a) == 1000

    def test_time_vector_starts_at_zero(self):
        t, _ = generate_coherent_signal()
        assert t[0] == pytest.approx(0.0)

    def test_reproducibility_with_rng(self):
        rng1 = np.random.default_rng(99)
        rng2 = np.random.default_rng(99)
        _, a1 = generate_coherent_signal(rng=rng1)
        _, a2 = generate_coherent_signal(rng=rng2)
        np.testing.assert_array_equal(a1, a2)


# ---------------------------------------------------------------------------
# TestGenerateIncoherentSignal
# ---------------------------------------------------------------------------

class TestGenerateIncoherentSignal:
    """Tests for generate_incoherent_signal()."""

    def test_returns_tuple(self):
        t, a = generate_incoherent_signal()
        assert isinstance(t, np.ndarray)
        assert isinstance(a, np.ndarray)

    def test_correct_length(self):
        _, a = generate_incoherent_signal(duration=0.5, fs=200.0)
        assert len(a) == 100

    def test_no_dominant_peak_at_f0(self):
        rng = np.random.default_rng(42)
        _, a = generate_incoherent_signal(
            duration=2.0, fs=FS, amplitude=1.0, rng=rng
        )
        result = compute_psi_from_timeseries(a, T=2.0, fs=FS)
        assert result.f0_detected is False


# ---------------------------------------------------------------------------
# TestPredictionP1
# ---------------------------------------------------------------------------

class TestPredictionP1:
    """Tests for test_prediction_p1_energy_scaling() – P1."""

    def test_p1_passes_for_coherent_signal(self, coherent_signal):
        masses = [1e-15, 1e-12, 1e-9, 1e-6]
        result = psi_mod.test_prediction_p1_energy_scaling(
            coherent_signal, masses, T=DURATION, fs=FS
        )
        assert result["passed"] is True

    def test_p1_linear_scaling(self, coherent_signal):
        masses = [1e-12, 2e-12, 4e-12]
        result = psi_mod.test_prediction_p1_energy_scaling(
            coherent_signal, masses, T=DURATION, fs=FS
        )
        # Ψ/m should be constant → relative deviation ≈ 0
        assert result["relative_deviation"] < 1e-9

    def test_p1_psi_proportional_to_mass(self, coherent_signal):
        masses = [1e-12, 2e-12]
        result = psi_mod.test_prediction_p1_energy_scaling(
            coherent_signal, masses, T=DURATION, fs=FS
        )
        psi = result["psi_values"]
        assert psi[1] == pytest.approx(2 * psi[0], rel=1e-9)

    def test_p1_raises_on_single_mass(self, coherent_signal):
        with pytest.raises(ValueError):
            psi_mod.test_prediction_p1_energy_scaling(coherent_signal, [1e-12])

    def test_p1_raises_on_negative_mass(self, coherent_signal):
        with pytest.raises(ValueError):
            psi_mod.test_prediction_p1_energy_scaling(coherent_signal, [-1e-12, 1e-12])

    def test_p1_result_keys(self, coherent_signal):
        result = psi_mod.test_prediction_p1_energy_scaling(
            coherent_signal, [1e-12, 2e-12]
        )
        for key in ("passed", "psi_per_mass", "relative_deviation",
                    "masses", "psi_values"):
            assert key in result


# ---------------------------------------------------------------------------
# TestPredictionP2
# ---------------------------------------------------------------------------

class TestPredictionP2:
    """Tests for test_prediction_p2_coherence_sensitivity() – P2."""

    def test_p2_passes(self, coherent_signal, incoherent_signal):
        result = psi_mod.test_prediction_p2_coherence_sensitivity(
            coherent_signal, incoherent_signal, T=DURATION, fs=FS
        )
        assert result["passed"] is True

    def test_p2_coherent_f0_detected(self, coherent_signal, incoherent_signal):
        result = psi_mod.test_prediction_p2_coherence_sensitivity(
            coherent_signal, incoherent_signal, T=DURATION, fs=FS
        )
        assert result["coherent_f0_detected"] is True

    def test_p2_incoherent_f0_not_detected(self, coherent_signal, incoherent_signal):
        result = psi_mod.test_prediction_p2_coherence_sensitivity(
            coherent_signal, incoherent_signal, T=DURATION, fs=FS
        )
        assert result["incoherent_f0_detected"] is False

    def test_p2_result_keys(self, coherent_signal, incoherent_signal):
        result = psi_mod.test_prediction_p2_coherence_sensitivity(
            coherent_signal, incoherent_signal, T=DURATION, fs=FS
        )
        for key in ("passed", "coherent_f0_detected", "incoherent_f0_detected",
                    "coherent_spectral_ratio", "incoherent_spectral_ratio",
                    "coherent_psi_tilde", "incoherent_psi_tilde"):
            assert key in result

    def test_p2_coherent_spectral_ratio_higher(self, coherent_signal, incoherent_signal):
        result = psi_mod.test_prediction_p2_coherence_sensitivity(
            coherent_signal, incoherent_signal, T=DURATION, fs=FS
        )
        assert (result["coherent_spectral_ratio"] >
                result["incoherent_spectral_ratio"])


# ---------------------------------------------------------------------------
# TestPredictionP3
# ---------------------------------------------------------------------------

class TestPredictionP3:
    """Tests for test_prediction_p3_spectral_peak() – P3."""

    def test_p3_passes_for_coherent_signal(self, coherent_signal):
        result = psi_mod.test_prediction_p3_spectral_peak(coherent_signal, fs=FS)
        assert result["passed"] is True

    def test_p3_dominant_frequency_near_f0(self, coherent_signal):
        result = psi_mod.test_prediction_p3_spectral_peak(coherent_signal, fs=FS)
        assert result["frequency_error"] < 1.0

    def test_p3_f0_detected(self, coherent_signal):
        result = psi_mod.test_prediction_p3_spectral_peak(coherent_signal, fs=FS)
        assert result["f0_detected"] is True

    def test_p3_result_keys(self, coherent_signal):
        result = psi_mod.test_prediction_p3_spectral_peak(coherent_signal, fs=FS)
        for key in ("passed", "dominant_frequency", "f0_expected",
                    "frequency_error", "bandwidth", "spectral_ratio",
                    "f0_detected"):
            assert key in result

    def test_p3_pure_sine_exact_frequency(self):
        # Pure sine at exactly f₀ with no noise
        _, a_t = generate_coherent_signal(
            duration=1.0, fs=FS, f0=QCAL_BASE_FREQUENCY,
            amplitude=1.0, noise_level=0.0
        )
        result = psi_mod.test_prediction_p3_spectral_peak(a_t, fs=FS)
        assert result["frequency_error"] < 1.0
        assert result["passed"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
