#!/usr/bin/env python3
"""
Tests for benchmarks/roc_psi_vs_snr.py and scripts/subthreshold_o3b_scan.py
=============================================================================

Validates:
- Individual detector scoring functions (score_snr, score_psi, score_coh)
- ROC / AUC computation helpers
- Monte-Carlo benchmark engine (run_benchmark)
- SNR sweep
- Sub-threshold O3b candidate analysis (simulation mode)
"""

import sys
import numpy as np
import pytest
from pathlib import Path

# ── Add repo root and submodule dirs to import path ─────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_REPO_ROOT / "benchmarks"))
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import roc_psi_vs_snr as roc_mod
import subthreshold_o3b_scan as o3b_mod


# ─── Fixtures ────────────────────────────────────────────────────────────────

FS = 1000       # low sample-rate for fast tests
F0 = 141.7001
N = FS          # 1 second


@pytest.fixture
def rng():
    return np.random.default_rng(42)


@pytest.fixture
def pure_noise(rng):
    """Two independent noise channels."""
    x = rng.standard_normal(N)
    y = rng.standard_normal(N)
    return x, y


@pytest.fixture
def signal_plus_noise(rng):
    """Two coherent signal + noise channels."""
    t = np.arange(N) / FS
    s = np.sin(2 * np.pi * F0 * t)
    x = 2.0 * s + rng.standard_normal(N)
    y = 2.0 * s + rng.standard_normal(N)
    return x, y


# ─── TestDetectorFunctions ───────────────────────────────────────────────────

class TestDetectorFunctions:
    """Unit tests for scoring functions."""

    def test_score_snr_returns_nonnegative(self, pure_noise):
        x, _ = pure_noise
        score = roc_mod.score_snr(x, fs=FS, f0=F0)
        assert score >= 0.0

    def test_score_snr_higher_with_signal(self, rng):
        t = np.arange(N) / FS
        s = np.sin(2 * np.pi * F0 * t)
        x_noise = rng.standard_normal(N)
        x_signal = 3.0 * s + rng.standard_normal(N)
        score_noise = roc_mod.score_snr(x_noise, fs=FS, f0=F0)
        score_signal = roc_mod.score_snr(x_signal, fs=FS, f0=F0)
        assert score_signal > score_noise

    def test_score_psi_returns_nonnegative(self, pure_noise):
        x, y = pure_noise
        score = roc_mod.score_psi(x, y, fs=FS, f0=F0)
        assert score >= 0.0

    def test_score_psi_higher_with_coherent_signal(self, rng):
        """Ψ should be larger when both channels share a coherent component."""
        t = np.arange(N) / FS
        s = np.sin(2 * np.pi * F0 * t)
        xn, yn = rng.standard_normal(N), rng.standard_normal(N)
        xs = 2.0 * s + rng.standard_normal(N)
        ys = 2.0 * s + rng.standard_normal(N)
        psi_noise = roc_mod.score_psi(xn, yn, fs=FS, f0=F0)
        psi_signal = roc_mod.score_psi(xs, ys, fs=FS, f0=F0)
        assert psi_signal > psi_noise

    def test_score_coh_in_range(self, pure_noise):
        x, y = pure_noise
        score = roc_mod.score_coh(x, y, fs=FS, f0=F0)
        assert 0.0 <= score <= 1.0


# ─── TestROCComputation ──────────────────────────────────────────────────────

class TestROCComputation:
    """Tests for ROC / AUC helpers."""

    def test_roc_curve_numpy_perfect_classifier(self):
        labels = np.array([0, 0, 1, 1])
        scores = np.array([0.1, 0.2, 0.8, 0.9])
        fpr, tpr = roc_mod._roc_curve_numpy(labels, scores)
        auc_val = roc_mod._auc_trapz(fpr, tpr)
        assert auc_val == pytest.approx(1.0, abs=0.01)

    def test_roc_curve_numpy_random_classifier(self):
        rng = np.random.default_rng(7)
        labels = rng.integers(0, 2, 200)
        scores = rng.uniform(0, 1, 200)
        fpr, tpr = roc_mod._roc_curve_numpy(labels, scores)
        auc_val = roc_mod._auc_trapz(fpr, tpr)
        assert 0.4 <= auc_val <= 0.6  # should be near 0.5

    def test_compute_roc_returns_valid_auc(self):
        rng = np.random.default_rng(99)
        labels = rng.integers(0, 2, 100)
        scores = rng.uniform(0, 1, 100)
        fpr, tpr, auc_val = roc_mod.compute_roc(labels, scores)
        assert 0.0 <= auc_val <= 1.0
        assert len(fpr) == len(tpr)
        assert fpr[0] == pytest.approx(0.0, abs=0.01)


# ─── TestRunBenchmark ────────────────────────────────────────────────────────

class TestRunBenchmark:
    """Tests for the Monte-Carlo benchmark engine."""

    def test_run_benchmark_returns_expected_keys(self):
        result = roc_mod.run_benchmark(n_trials=50, snr=0.5,
                                       fs=FS, f0=F0, seed=42)
        expected = {"labels", "scores_snr", "scores_psi", "scores_coh",
                    "auc_snr", "auc_psi", "auc_coh",
                    "roc_snr", "roc_psi", "roc_coh", "params"}
        assert expected.issubset(result.keys())

    def test_run_benchmark_label_counts(self):
        result = roc_mod.run_benchmark(n_trials=100, snr=0.5,
                                       fs=FS, f0=F0, seed=0)
        labels = result["labels"]
        assert len(labels) == 100
        # Both classes should appear
        assert np.sum(labels == 0) > 0
        assert np.sum(labels == 1) > 0

    def test_run_benchmark_auc_bounds(self):
        result = roc_mod.run_benchmark(n_trials=100, snr=0.5,
                                       fs=FS, f0=F0, seed=1)
        for key in ("auc_snr", "auc_psi", "auc_coh"):
            assert 0.0 <= result[key] <= 1.0, f"{key} out of [0,1]"

    def test_run_benchmark_high_snr_detectable(self):
        """At high SNR all detectors should achieve AUC well above 0.5."""
        result = roc_mod.run_benchmark(n_trials=200, snr=5.0,
                                       fs=FS, f0=F0, seed=2)
        assert result["auc_snr"] > 0.6
        assert result["auc_psi"] > 0.6

    def test_run_benchmark_reproducible(self):
        r1 = roc_mod.run_benchmark(n_trials=50, snr=0.5, fs=FS, f0=F0,
                                   seed=77)
        r2 = roc_mod.run_benchmark(n_trials=50, snr=0.5, fs=FS, f0=F0,
                                   seed=77)
        np.testing.assert_array_equal(r1["labels"], r2["labels"])
        np.testing.assert_array_almost_equal(r1["scores_snr"],
                                             r2["scores_snr"])


# ─── TestSNRSweep ────────────────────────────────────────────────────────────

class TestSNRSweep:
    """Tests for the multi-SNR sweep."""

    def test_snr_sweep_length(self):
        snr_vals = [0.5, 1.0, 2.0]
        results = roc_mod.snr_sweep(snr_values=snr_vals, n_trials=50,
                                    fs=FS, f0=F0, seed=10)
        assert len(results) == len(snr_vals)

    def test_snr_sweep_auc_increases_with_snr(self):
        """Higher SNR should generally produce higher AUC for D_SNR."""
        snr_vals = [0.1, 2.0]
        results = roc_mod.snr_sweep(snr_values=snr_vals, n_trials=200,
                                    fs=FS, f0=F0, seed=20)
        auc_low = results[0]["auc_snr"]
        auc_high = results[1]["auc_snr"]
        assert auc_high >= auc_low


# ─── TestSerialisation ───────────────────────────────────────────────────────

class TestSerialisation:
    """Tests for JSON serialisation of results."""

    def test_save_and_load(self, tmp_path):
        result = roc_mod.run_benchmark(n_trials=30, snr=0.5, fs=FS,
                                       f0=F0, seed=5)
        out = str(tmp_path / "test_results.json")
        roc_mod.save_results(result, out)

        import json
        with open(out) as fh:
            data = json.load(fh)
        assert "f0_hz" in data
        assert "results" in data
        assert data["f0_hz"] == pytest.approx(F0)


# ─── TestSubthresholdO3b ─────────────────────────────────────────────────────

class TestSubthresholdO3b:
    """Tests for the sub-threshold O3b scan (simulation mode)."""

    def test_compute_psi_positive(self):
        rng = np.random.default_rng(0)
        x = rng.standard_normal(4096)
        y = rng.standard_normal(4096)
        psi = o3b_mod.compute_psi(x, y, fs=1000, f0=F0)
        assert psi >= 0.0

    def test_psi_pvalue_in_range(self):
        bg = np.random.default_rng(3).uniform(0.01, 0.05, 50)
        p = o3b_mod.psi_pvalue(0.10, bg)
        assert 0.0 <= p <= 1.0

    def test_simulate_candidate_returns_arrays(self):
        cand = {"id": "test", "gps": 1251010524.0, "snr_official": 6.1}
        data = o3b_mod._simulate_candidate(cand, fs=512, f0=F0, seed=0)
        assert "h1" in data
        assert "l1" in data
        assert len(data["h1"]) == o3b_mod.WINDOW_S * 512
        assert len(data["l1"]) == o3b_mod.WINDOW_S * 512

    def test_analyse_candidate_shadow_o3b1(self):
        """Reference candidate Shadow-O3b-1 should run without errors."""
        cand = o3b_mod.O3B_CANDIDATES[0]
        result = o3b_mod.analyse_candidate(
            cand, use_real_data=False, fs=512, f0=F0, seed=42
        )
        assert result["candidate_id"] == "Shadow-O3b-1"
        assert "psi_full_window" in result
        assert "coherence_aeff2" in result
        assert 0.0 <= result["coherence_aeff2"] <= 1.0
        assert "contrast_sigma" in result
        assert "p_value" in result
        assert isinstance(result["detected"], bool)

    def test_analyse_candidate_returns_gps(self):
        cand = o3b_mod.O3B_CANDIDATES[0]
        result = o3b_mod.analyse_candidate(
            cand, use_real_data=False, fs=512, f0=F0, seed=7
        )
        assert result["gps"] == cand["gps"]

    def test_analyse_candidate_snr_official(self):
        cand = {"id": "test-cand", "gps": 1251010524.0,
                "snr_official": 6.5, "description": "test"}
        result = o3b_mod.analyse_candidate(
            cand, use_real_data=False, fs=512, f0=F0, seed=10
        )
        assert result["snr_official"] == 6.5


# ─── Integration ─────────────────────────────────────────────────────────────

class TestIntegration:
    """End-to-end integration tests (small trial counts for speed)."""

    def test_full_benchmark_pipeline(self, tmp_path):
        """Run a minimal benchmark and verify output structure."""
        result = roc_mod.run_benchmark(n_trials=60, snr=1.0,
                                       fs=FS, f0=F0, seed=99)
        # All AUCs valid
        for key in ("auc_snr", "auc_psi", "auc_coh"):
            assert 0.0 <= result[key] <= 1.0
        # ROC curves non-trivial
        fpr, tpr = result["roc_snr"]
        assert len(fpr) > 2

    def test_full_o3b_scan_pipeline(self):
        """Run O3b scan on all built-in candidates in simulation mode."""
        results = []
        for i, cand in enumerate(o3b_mod.O3B_CANDIDATES):
            res = o3b_mod.analyse_candidate(
                cand, use_real_data=False, fs=512, f0=F0, seed=i
            )
            results.append(res)
        assert len(results) == len(o3b_mod.O3B_CANDIDATES)
        for r in results:
            assert "detected" in r
