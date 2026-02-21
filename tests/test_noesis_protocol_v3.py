#!/usr/bin/env python3
"""
Tests for src/noesis_protocol_v3.py
=====================================

Validates the three critical adjustments of the Refined Noēsis Protocol v3.0:
1. Sharpened metric: Ψ = I(f₀) · A_eff²
2. Off-target control band at f_control = f₀ + 50 Hz = 191.7001 Hz
3. Realistic Channel 2 with thermal noise (SNR_ref ≈ 50)
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

# Load module directly to avoid numpy/mpmath dependency from src/__init__
_ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "noesis_protocol_v3",
    _ROOT / "src" / "noesis_protocol_v3.py",
)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["noesis_protocol_v3"] = _mod
_spec.loader.exec_module(_mod)

from noesis_protocol_v3 import (
    F0_NOESIS,
    F_CONTROL,
    F_CONTROL_OFFSET,
    NOISE_SIGMA_REF,
    SNR_REF_THERMAL,
    NoesisAnalysisResult,
    PsiResult,
    analyze_gwtc_event,
    calculate_psi_refined,
    generate_channel2_realistic,
    run_noesis_pipeline,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    """Verify physical constants of the Noēsis Protocol v3.0."""

    def test_f0_value(self):
        assert F0_NOESIS == pytest.approx(141.7001)

    def test_f_control_offset(self):
        assert F_CONTROL_OFFSET == pytest.approx(50.0)

    def test_f_control_equals_f0_plus_offset(self):
        assert F_CONTROL == pytest.approx(F0_NOESIS + F_CONTROL_OFFSET)

    def test_snr_ref_thermal(self):
        assert SNR_REF_THERMAL == pytest.approx(50.0)

    def test_noise_sigma_ref(self):
        assert NOISE_SIGMA_REF == pytest.approx(1.0 / SNR_REF_THERMAL)


# ---------------------------------------------------------------------------
# Channel 2 generation
# ---------------------------------------------------------------------------


class TestChannel2Realistic:
    """Tests for generate_channel2_realistic."""

    def test_output_length(self):
        fs = 512.0
        t = np.arange(0, 1.0, 1.0 / fs)
        canal2 = generate_channel2_realistic(t, seed=0)
        assert len(canal2) == len(t)

    def test_reproducible_with_seed(self):
        fs = 512.0
        t = np.arange(0, 1.0, 1.0 / fs)
        c1 = generate_channel2_realistic(t, seed=7)
        c2 = generate_channel2_realistic(t, seed=7)
        np.testing.assert_array_equal(c1, c2)

    def test_different_seeds_differ(self):
        fs = 512.0
        t = np.arange(0, 1.0, 1.0 / fs)
        c1 = generate_channel2_realistic(t, seed=1)
        c2 = generate_channel2_realistic(t, seed=2)
        assert not np.allclose(c1, c2)

    def test_noise_level_realistic(self):
        """Noise amplitude ≈ NOISE_SIGMA_REF (small relative to unit sine)."""
        fs = 4096.0
        t = np.arange(0, 5.0, 1.0 / fs)
        canal2 = generate_channel2_realistic(t, seed=42)
        # Amplitude should be close to 1 (sine) with small noise
        assert np.std(canal2) == pytest.approx(np.sqrt(0.5), rel=0.1)

    def test_custom_phase_offset(self):
        fs = 512.0
        t = np.arange(0, 1.0, 1.0 / fs)
        c0 = generate_channel2_realistic(t, phase_offset=0.0, noise_sigma=0.0)
        cpi = generate_channel2_realistic(t, phase_offset=np.pi, noise_sigma=0.0)
        np.testing.assert_allclose(c0, -cpi, atol=1e-10)


# ---------------------------------------------------------------------------
# Sharpened metric Ψ = I(f₀) · A_eff²
# ---------------------------------------------------------------------------


class TestCalculatePsiRefined:
    """Tests for calculate_psi_refined."""

    def _make_signals(self, fs=1024.0, duration=5.0, f0=F0_NOESIS, snr=10.0, seed=0):
        rng = np.random.default_rng(seed)
        t = np.arange(0, duration, 1.0 / fs)
        noise = rng.normal(0.0, 1.0, len(t))
        tone = snr * np.sin(2 * np.pi * f0 * t)
        xf = noise + tone
        yf = generate_channel2_realistic(t, f0=f0, seed=seed)
        return xf, yf, fs

    def test_returns_psi_result(self):
        xf, yf, fs = self._make_signals()
        result = calculate_psi_refined(xf, yf, fs, F0_NOESIS)
        assert isinstance(result, PsiResult)

    def test_psi_non_negative(self):
        xf, yf, fs = self._make_signals()
        result = calculate_psi_refined(xf, yf, fs, F0_NOESIS)
        assert result.psi >= 0.0

    def test_a_eff_sq_is_cxy_squared(self):
        """A_eff² must equal C_xy²(f₀), not C_xy(f₀)."""
        from scipy.signal import coherence, welch

        xf, yf, fs = self._make_signals()
        win = int(2.0 * fs)
        nperseg = max(win // 2, 4)
        f_coh, Cxy = coherence(xf, yf, fs=fs, nperseg=nperseg)
        idx = int(np.argmin(np.abs(f_coh - F0_NOESIS)))
        expected_a_eff_sq = float(Cxy[idx]) ** 2

        result = calculate_psi_refined(xf, yf, fs, F0_NOESIS)
        assert result.A_eff_sq == pytest.approx(expected_a_eff_sq, rel=1e-9)

    def test_psi_equals_I_times_A_eff_sq(self):
        """Ψ = I(f₀) · A_eff² must hold exactly."""
        xf, yf, fs = self._make_signals()
        result = calculate_psi_refined(xf, yf, fs, F0_NOESIS)
        assert result.psi == pytest.approx(result.I_f * result.A_eff_sq, rel=1e-9)

    def test_psi_larger_at_tone_frequency(self):
        """Ψ at f₀ (where tone exists) must exceed Ψ at f_control (no tone)."""
        xf, yf, fs = self._make_signals(snr=5.0)
        psi_target = calculate_psi_refined(xf, yf, fs, F0_NOESIS)
        psi_control = calculate_psi_refined(xf, yf, fs, F_CONTROL)
        assert psi_target.psi > psi_control.psi

    def test_f_target_stored_correctly(self):
        xf, yf, fs = self._make_signals()
        for freq in [F0_NOESIS, F_CONTROL]:
            result = calculate_psi_refined(xf, yf, fs, freq)
            assert result.f_target == pytest.approx(freq)


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------


class TestRunNoesisPipeline:
    """Tests for run_noesis_pipeline."""

    def test_returns_noesis_analysis_result(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, snr_signal=5.0, seed=0)
        assert isinstance(result, NoesisAnalysisResult)

    def test_target_and_control_present(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        assert isinstance(result.target, PsiResult)
        assert isinstance(result.control, PsiResult)

    def test_target_label(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        assert result.target.label == "target"

    def test_control_label(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        assert result.control.label == "control"

    def test_control_band_frequency(self):
        """Control band must be evaluated at f₀ + 50 Hz."""
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        assert result.control.f_target == pytest.approx(F_CONTROL)

    def test_contrast_ratio_positive(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, snr_signal=5.0, seed=0)
        assert result.contrast_ratio > 0.0

    def test_high_snr_produces_large_contrast(self):
        """With high SNR, target Ψ must dominate the control band."""
        result = run_noesis_pipeline(duration=5.0, fs=1024.0, snr_signal=10.0, seed=42)
        assert result.contrast_ratio > 1.0

    def test_metadata_keys(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        for key in ("f0", "f_control", "duration_s", "fs_hz", "snr_signal", "snr_ref"):
            assert key in result.metadata

    def test_metadata_snr_ref_value(self):
        result = run_noesis_pipeline(duration=2.0, fs=512.0, seed=0)
        assert result.metadata["snr_ref"] == pytest.approx(SNR_REF_THERMAL)

    def test_reproducible_with_seed(self):
        r1 = run_noesis_pipeline(duration=2.0, fs=512.0, seed=99)
        r2 = run_noesis_pipeline(duration=2.0, fs=512.0, seed=99)
        assert r1.target.psi == pytest.approx(r2.target.psi)
        assert r1.control.psi == pytest.approx(r2.control.psi)


# ---------------------------------------------------------------------------
# GWTC integration
# ---------------------------------------------------------------------------


class TestAnalyzeGwtcEvent:
    """Tests for analyze_gwtc_event (uses simulated fallback when GWOSC absent)."""

    def test_returns_result(self):
        result = analyze_gwtc_event("GW150914", detector="H1", duration=4.0, fs=512.0)
        assert isinstance(result, NoesisAnalysisResult)

    def test_metadata_event_name(self):
        result = analyze_gwtc_event("GW150914", detector="L1", duration=4.0, fs=512.0)
        assert result.metadata["event"] == "GW150914"

    def test_metadata_detector(self):
        result = analyze_gwtc_event("GW150914", detector="L1", duration=4.0, fs=512.0)
        assert result.metadata["detector"] == "L1"

    def test_metadata_frequencies(self):
        result = analyze_gwtc_event("GW150914", duration=4.0, fs=512.0)
        assert result.metadata["f0"] == pytest.approx(F0_NOESIS)
        assert result.metadata["f_control"] == pytest.approx(F_CONTROL)

    def test_psi_values_finite(self):
        result = analyze_gwtc_event("GW150914", duration=4.0, fs=512.0)
        assert np.isfinite(result.target.psi)
        assert np.isfinite(result.control.psi)

    def test_data_source_key_present(self):
        result = analyze_gwtc_event("GW150914", duration=4.0, fs=512.0)
        assert "data_source" in result.metadata

    def test_different_events_differ(self):
        r1 = analyze_gwtc_event("GW150914", duration=4.0, fs=512.0)
        r2 = analyze_gwtc_event("GW200129_215028", duration=4.0, fs=512.0)
        # Different events should generally produce different Ψ values
        assert r1.target.psi != r2.target.psi or r1.control.psi != r2.control.psi


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
