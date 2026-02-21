#!/usr/bin/env python3
"""
Tests for RAC Protocol Scripts:
  - gw_rac_residuals.py
  - gw_rac_timeslides.py
  - bio_link_phase_entrainment.py

Tests focus on the computational logic using synthetic data so that
GWOSC/GWPy availability is not required.
"""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Path setup – allow imports from scripts/ directory
# ---------------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import importlib.util


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(
        name, str(SCRIPTS_DIR / f"{name}.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rac = _load_module("gw_rac_residuals")
slides = _load_module("gw_rac_timeslides")
bio = _load_module("bio_link_phase_entrainment")


# ---------------------------------------------------------------------------
# gw_rac_residuals tests
# ---------------------------------------------------------------------------

class TestGWRACResiduals:
    """Unit tests for gw_rac_residuals.py."""

    FS = 4096
    DURATION = 4.0  # short duration for speed
    N = int(FS * DURATION)

    def _make_strain(self, seed: int = 0) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.standard_normal(self.N) * 1e-23

    def test_gr_template_shape(self):
        """Template has same length as input time array."""
        t = np.linspace(0, self.DURATION, self.N)
        tmpl = rac._gr_template(t, self.FS)
        assert tmpl.shape == t.shape

    def test_gr_template_finite(self):
        """Template contains no NaN or Inf."""
        t = np.linspace(0, self.DURATION, self.N)
        tmpl = rac._gr_template(t, self.FS)
        assert np.all(np.isfinite(tmpl))

    def test_gr_template_peak_amplitude(self):
        """Template peak is within realistic GW strain range (~10^-21)."""
        t = np.linspace(0, self.DURATION, self.N)
        tmpl = rac._gr_template(t, self.FS)
        peak = np.max(np.abs(tmpl))
        assert 1e-23 < peak < 1e-18

    def test_compute_psi_shape(self):
        """Ψ(t) output has correct shape and values in [0, 1]."""
        h1 = self._make_strain(0)
        l1 = self._make_strain(1)
        t_psi, psi = rac.compute_psi(h1, l1, fs=self.FS)
        assert t_psi.shape == psi.shape
        assert np.all(psi >= 0.0)
        assert np.all(psi <= 1.0 + 1e-10)

    def test_compute_psi_self_coherence(self):
        """Self-coherence of a signal with itself should be ~1."""
        h1 = self._make_strain(0)
        _, psi = rac.compute_psi(h1, h1, fs=self.FS)
        assert np.mean(psi) > 0.9

    def test_compute_psi_band_shape(self):
        """Ψ_band(t) output has correct shape and values in [0, 1]."""
        h1 = self._make_strain(0)
        l1 = self._make_strain(1)
        t_b, psi_b = rac.compute_psi_band(h1, l1, fs=self.FS)
        assert t_b.shape == psi_b.shape
        assert np.all(psi_b >= 0.0)
        assert np.all(psi_b <= 1.0 + 1e-10)

    def test_detect_echo_found(self):
        """Echo detected when coherence exceeds threshold in expected window."""
        merger_t = 0.5
        n = 100
        t_psi = np.linspace(0, 2.0, n)
        psi = np.ones(n) * 0.3
        # Inject a high-coherence point just after the merger + echo delay
        target_t = merger_t + rac.ECHO_DELAY
        idx = np.argmin(np.abs(t_psi - target_t))
        psi[idx] = 0.85

        result = rac.detect_echo(t_psi, psi, merger_time=merger_t,
                                 echo_window=rac.ECHO_DELAY,
                                 coherence_threshold=0.80)
        assert result["detected"] is True
        assert result["echo_psi"] == pytest.approx(0.85, abs=1e-6)

    def test_detect_echo_not_found(self):
        """No echo detected when coherence is below threshold."""
        n = 100
        t_psi = np.linspace(0, 2.0, n)
        psi = np.ones(n) * 0.3
        result = rac.detect_echo(t_psi, psi, merger_time=0.5,
                                 coherence_threshold=0.80)
        assert result["detected"] is False

    def test_run_rac_analysis_output(self):
        """Full pipeline runs and produces expected output keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = rac.run_rac_analysis(
                output_dir=Path(tmpdir),
                verbose=False,
            )
        assert "event" in results
        assert results["event"] == "GW150914"
        assert "psi_broadband" in results
        assert "psi_band" in results
        assert "residuals" in results

    def test_run_rac_analysis_json_saved(self):
        """JSON results file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            rac.run_rac_analysis(output_dir=Path(tmpdir), verbose=False)
            out = Path(tmpdir) / "gw_rac_residuals_results.json"
            assert out.exists()
            data = json.loads(out.read_text())
            assert data["event"] == "GW150914"


# ---------------------------------------------------------------------------
# gw_rac_timeslides tests
# ---------------------------------------------------------------------------

class TestGWRACTimeslides:
    """Unit tests for gw_rac_timeslides.py."""

    FS = 4096
    N = 4 * 4096  # 4 s

    def _make_residual(self, seed: int = 0) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.standard_normal(self.N) * 1e-23

    def test_compute_background_length(self):
        """Background distribution has exactly n_slides entries."""
        h1 = self._make_residual(0)
        l1 = self._make_residual(1)
        bg = slides.compute_background(
            h1, l1, fs=self.FS,
            n_slides=5, slide_step_s=1.0,
            fmin=300.0, fmax=1000.0,
            verbose=False,
        )
        assert len(bg) == 5

    def test_compute_background_values_in_range(self):
        """All slide maxima are in [0, 1]."""
        h1 = self._make_residual(0)
        l1 = self._make_residual(1)
        bg = slides.compute_background(
            h1, l1, fs=self.FS,
            n_slides=5, slide_step_s=1.0,
            fmin=300.0, fmax=1000.0,
            verbose=False,
        )
        assert all(0.0 <= v <= 1.0 + 1e-10 for v in bg)

    def test_compute_pvalue_far_keys(self):
        """p-value / FAR dictionary contains expected keys."""
        bg = [0.5, 0.6, 0.7, 0.4, 0.55]
        stats = slides.compute_pvalue_far(
            psi_observed=0.65,
            background_maxima=bg,
            analysis_duration_s=4.0,
        )
        for key in ("p_value", "FAR_Hz", "FAR_per_year", "n_slides",
                    "background_mean", "background_std"):
            assert key in stats

    def test_pvalue_one_when_all_exceed(self):
        """p-value = 1 when all background values exceed the observed stat."""
        bg = [0.9, 0.95, 0.91]
        stats = slides.compute_pvalue_far(0.5, bg, analysis_duration_s=4.0)
        assert stats["p_value"] == pytest.approx(1.0, abs=1e-9)

    def test_pvalue_zero_when_none_exceed(self):
        """p-value = 0 when no background values exceed the observed stat."""
        bg = [0.3, 0.2, 0.25]
        stats = slides.compute_pvalue_far(0.9, bg, analysis_duration_s=4.0)
        assert stats["p_value"] == pytest.approx(0.0, abs=1e-9)

    def test_run_timeslide_analysis_output(self):
        """Full pipeline returns expected result structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = slides.run_timeslide_analysis(
                n_slides=5,
                slide_step_s=1.0,
                output_dir=Path(tmpdir),
                verbose=False,
            )
        assert "statistics" in results
        assert "background_distribution" in results
        assert "significant" in results

    def test_run_timeslide_analysis_json_saved(self):
        """JSON results file is created by the pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            slides.run_timeslide_analysis(
                n_slides=5,
                slide_step_s=1.0,
                output_dir=Path(tmpdir),
                verbose=False,
            )
            out = Path(tmpdir) / "gw_rac_timeslides_results.json"
            assert out.exists()
            data = json.loads(out.read_text())
            assert "statistics" in data


# ---------------------------------------------------------------------------
# bio_link_phase_entrainment tests
# ---------------------------------------------------------------------------

class TestBioLinkPhaseEntrainment:
    """Unit tests for bio_link_phase_entrainment.py."""

    FS = bio.EEG_FS
    DURATION = bio.EEG_DURATION_S
    N = int(FS * DURATION)

    # --- Stimulus generators ---

    def test_stimulus_A_shape(self):
        """Stimulus A has expected length."""
        s = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        assert len(s) == self.N

    def test_stimulus_A_amplitude(self):
        """Stimulus A peak amplitude respects safety ceiling."""
        s = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        assert np.max(np.abs(s)) <= bio.MAX_STIMULUS_AMP + 1e-10

    def test_stimulus_B_same_shape_as_A(self):
        """Stimulus B has same shape as A."""
        s_a = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        s_b = bio.stimulus_B(stim_a=s_a, fs=self.FS, duration=self.DURATION)
        assert s_b.shape == s_a.shape

    def test_stimulus_B_different_phase_from_A(self):
        """Stimulus B differs from A (phases scrambled)."""
        s_a = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        s_b = bio.stimulus_B(stim_a=s_a, fs=self.FS, duration=self.DURATION)
        assert not np.allclose(s_a, s_b)

    def test_stimulus_B_similar_power_to_A(self):
        """Stimulus B has similar RMS power to A (within 10x)."""
        s_a = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        s_b = bio.stimulus_B(stim_a=s_a, fs=self.FS, duration=self.DURATION)
        rms_a = np.sqrt(np.mean(s_a ** 2))
        rms_b = np.sqrt(np.mean(s_b ** 2))
        assert rms_b > 0
        ratio = rms_a / rms_b
        assert 0.1 < ratio < 10.0

    def test_stimulus_C_is_zero(self):
        """Stimulus C is identically zero."""
        s = bio.stimulus_C(fs=self.FS, duration=self.DURATION)
        assert np.all(s == 0.0)

    def test_stimulus_D_shape_and_freq(self):
        """Stimulus D has correct shape and dominant frequency ~40 Hz."""
        s = bio.stimulus_D(fs=self.FS, duration=self.DURATION)
        assert len(s) == self.N
        # Dominant frequency via FFT
        freqs = np.fft.rfftfreq(self.N, d=1.0 / self.FS)
        psd = np.abs(np.fft.rfft(s)) ** 2
        dom_freq = freqs[np.argmax(psd)]
        assert abs(dom_freq - bio.GAMMA_CENTER_HZ) < 1.0

    def test_stimulus_D_amplitude(self):
        """Stimulus D peak amplitude equals MAX_STIMULUS_AMP."""
        s = bio.stimulus_D(fs=self.FS, duration=self.DURATION)
        assert np.max(np.abs(s)) == pytest.approx(bio.MAX_STIMULUS_AMP, abs=1e-10)

    # --- EEG loader ---

    def test_load_eeg_synthetic_shape(self):
        """Synthetic EEG has expected length."""
        eeg, fs = bio.load_eeg(None, fs=self.FS, duration=self.DURATION)
        assert len(eeg) == self.N
        assert fs == self.FS

    def test_load_eeg_with_stimulus(self):
        """EEG generated with stimulus is not pure noise."""
        stim = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        eeg, _ = bio.load_eeg(None, fs=self.FS, duration=self.DURATION,
                               stimulus=stim)
        assert len(eeg) == self.N
        assert np.any(eeg != 0)

    # --- Metrics ---

    def test_compute_genesis_score_shape(self):
        """G(t) has finite positive values."""
        stim = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        eeg, fs = bio.load_eeg(None, fs=self.FS, duration=self.DURATION,
                                stimulus=stim)
        t_g, G = bio.compute_genesis_score(stim, eeg, fs=fs)
        assert t_g.shape == G.shape
        assert np.all(np.isfinite(G))
        assert np.all(G >= 0.0)

    def test_compute_plv_range(self):
        """PLV is in [0, 1]."""
        stim = bio.stimulus_A(fs=self.FS, duration=self.DURATION)
        eeg, fs = bio.load_eeg(None, fs=self.FS, duration=self.DURATION,
                                stimulus=stim)
        plv = bio.compute_plv(stim, eeg, fs=fs)
        assert 0.0 <= plv <= 1.0

    def test_compute_plv_self_is_one(self):
        """PLV of a signal with itself is 1."""
        stim = bio.stimulus_D(fs=self.FS, duration=self.DURATION)
        plv = bio.compute_plv(stim, stim, fs=self.FS)
        assert plv == pytest.approx(1.0, abs=0.01)

    def test_compare_A_vs_B_keys(self):
        """A vs B comparison dict contains required keys."""
        comp = bio.compare_A_vs_B(0.6, 0.4, 0.55, 0.45)
        for key in ("PLV_A", "PLV_B", "delta_PLV", "G_mean_A", "G_mean_B",
                    "delta_G", "A_greater_B_PLV", "phase_structure_effect"):
            assert key in comp

    def test_compare_A_vs_B_effect_true(self):
        """phase_structure_effect is True when A > B on both metrics."""
        comp = bio.compare_A_vs_B(0.7, 0.4, 0.65, 0.5)
        assert comp["phase_structure_effect"] is True

    def test_compare_A_vs_B_effect_false(self):
        """phase_structure_effect is False when A ≤ B."""
        comp = bio.compare_A_vs_B(0.3, 0.6, 0.3, 0.6)
        assert comp["phase_structure_effect"] is False

    # --- Full pipeline ---

    def test_run_phase_entrainment_all(self):
        """Full pipeline with all stimuli returns expected structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = bio.run_phase_entrainment(
                stimulus_label="all",
                output_dir=Path(tmpdir),
                verbose=False,
            )
        assert "stimuli" in results
        for label in ("A", "B", "C", "D"):
            assert label in results["stimuli"]
        assert "A_vs_B_comparison" in results

    def test_run_phase_entrainment_single(self):
        """Pipeline with single stimulus label works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = bio.run_phase_entrainment(
                stimulus_label="D",
                output_dir=Path(tmpdir),
                verbose=False,
            )
        assert "D" in results["stimuli"]

    def test_run_phase_entrainment_json_saved(self):
        """JSON results file is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bio.run_phase_entrainment(
                stimulus_label="all",
                output_dir=Path(tmpdir),
                verbose=False,
            )
            out = Path(tmpdir) / "bio_link_phase_entrainment_results.json"
            assert out.exists()
            data = json.loads(out.read_text())
            assert "stimuli" in data

    def test_safety_config_in_results(self):
        """Results include safety metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = bio.run_phase_entrainment(
                stimulus_label="A",
                output_dir=Path(tmpdir),
                verbose=False,
            )
        assert "safety" in results
        safety = results["safety"]
        assert safety["amplitude_normalised"] is True
        assert safety["no_visual_flicker"] is True
        assert safety["photosensitive_epilepsy_warning"] is True
