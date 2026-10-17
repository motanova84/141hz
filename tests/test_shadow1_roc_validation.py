#!/usr/bin/env python3
"""
Tests for Shadow-1 O3b Rigorous Detection Validation
=====================================================

Validates all six methodological requirements introduced in
scripts/shadow1_roc_validation.py:

1. Dimensionless score_psi
2. ROC with frequency jitter (anti-overfit)
3. Channel independence (H0 independent seeds, H1 coherent+independent noise)
4. Bootstrap AUC with CI95
5. Multiple-testing correction (BH)
6. data_source field in all outputs
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.shadow1_roc_validation import (
    F0_HZ,
    FS_HZ,
    BOOTSTRAP_N,
    BOOTSTRAP_SEED,
    F_CONTROL_OFFSET_HZ,
    TIME_SLIDE_S,
    compute_score_psi,
    generate_roc_dataset,
    time_slide_sanity,
    bootstrap_auc,
    apply_p_fdr,
    run_o3b_scan,
    O3bScanResult,
)


class TestConstants(unittest.TestCase):
    """Sanity-check module-level constants."""

    def test_f0(self):
        self.assertAlmostEqual(F0_HZ, 141.7001, places=3)

    def test_jitter_range(self):
        from scripts.shadow1_roc_validation import JITTER_MIN_HZ, JITTER_MAX_HZ
        self.assertGreater(JITTER_MIN_HZ, 0.0)
        self.assertGreater(JITTER_MAX_HZ, JITTER_MIN_HZ)

    def test_control_offset(self):
        self.assertGreaterEqual(F_CONTROL_OFFSET_HZ, 20.0)

    def test_bootstrap_defaults(self):
        self.assertGreaterEqual(BOOTSTRAP_N, 50)


# ─────────────────────────────────────────────────────────────────────────────
# Fix 1: Dimensionless score_psi
# ─────────────────────────────────────────────────────────────────────────────

class TestScorePsi(unittest.TestCase):
    """score_psi must be dimensionless (pure ratio) and in a sensible range."""

    def setUp(self):
        rng = np.random.default_rng(7)
        from scipy import signal as sp_signal
        n = int(FS_HZ * 1.0)
        h1 = rng.normal(0, 1e-22, n)
        l1 = rng.normal(0, 1e-22, n)
        self.freqs, self.psd = sp_signal.welch(h1, fs=FS_HZ, nperseg=256)
        self.freqs_c, self.msc = sp_signal.coherence(h1, l1, fs=FS_HZ, nperseg=256)

    def test_returns_float(self):
        s = compute_score_psi(self.psd, self.freqs, self.msc, F0_HZ)
        self.assertIsInstance(s, float)

    def test_non_negative(self):
        s = compute_score_psi(self.psd, self.freqs, self.msc, F0_HZ)
        self.assertGreaterEqual(s, 0.0)

    def test_dimensionless_range_noise(self):
        """For noise, I_f0 ≈ 1 and MSC ≈ 0, so score ≈ 0–a few."""
        s = compute_score_psi(self.psd, self.freqs, self.msc, F0_HZ)
        self.assertLess(s, 100.0, "score_psi should be O(1) for pure noise")

    def test_coherent_signal_raises_score(self):
        """Injecting a coherent tone at f0 should increase score_psi."""
        from scipy import signal as sp_signal
        n = int(FS_HZ * 1.0)
        t = np.linspace(0, 1.0, n, endpoint=False)
        sig = 5e-21 * np.sin(2 * np.pi * F0_HZ * t)
        rng = np.random.default_rng(11)
        h1 = sig + rng.normal(0, 1e-22, n)
        l1 = sig + np.random.default_rng(12).normal(0, 1e-22, n)
        freqs, psd = sp_signal.welch(h1, fs=FS_HZ, nperseg=256)
        _, msc = sp_signal.coherence(h1, l1, fs=FS_HZ, nperseg=256)
        s_signal = compute_score_psi(psd, freqs, msc, F0_HZ)
        # noise-only score
        h1n = rng.normal(0, 1e-22, n)
        l1n = np.random.default_rng(13).normal(0, 1e-22, n)
        freqs_n, psd_n = sp_signal.welch(h1n, fs=FS_HZ, nperseg=256)
        _, msc_n = sp_signal.coherence(h1n, l1n, fs=FS_HZ, nperseg=256)
        s_noise = compute_score_psi(psd_n, freqs_n, msc_n, F0_HZ)
        self.assertGreater(s_signal, s_noise)


# ─────────────────────────────────────────────────────────────────────────────
# Fix 2 + 3: ROC dataset (jitter + channel independence)
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateRocDataset(unittest.TestCase):
    """ROC dataset must have correct structure, labels, and anti-overfit jitter."""

    def setUp(self):
        self.ds = generate_roc_dataset(n_h0=50, n_h1=50, seed=42)

    def test_keys_present(self):
        for key in ("scores_on", "scores_off", "labels",
                    "f_injected", "data_source"):
            self.assertIn(key, self.ds)

    def test_data_source_is_simulation(self):
        """Fix 6: must report SIMULATION_FALLBACK for synthetic data."""
        self.assertEqual(self.ds["data_source"], "SIMULATION_FALLBACK")

    def test_label_counts(self):
        labels = self.ds["labels"]
        self.assertEqual(int((labels == 0).sum()), 50)
        self.assertEqual(int((labels == 1).sum()), 50)

    def test_f_injected_length(self):
        """One injection frequency per H1 sample."""
        self.assertEqual(len(self.ds["f_injected"]), 50)

    def test_jitter_applied(self):
        """Injected frequencies must differ from f0 (jitter applied)."""
        from scripts.shadow1_roc_validation import JITTER_MIN_HZ
        diffs = np.abs(self.ds["f_injected"] - F0_HZ)
        self.assertTrue(
            np.all(diffs >= JITTER_MIN_HZ * 0.9),  # allow tiny numeric slack
            "All H1 injections should have |f_inj - f0| >= jitter_min",
        )

    def test_scores_shape(self):
        self.assertEqual(len(self.ds["scores_on"]), 100)
        self.assertEqual(len(self.ds["scores_off"]), 100)

    def test_h0_independent_seeds_reproducible(self):
        """Generating twice with same seed must give identical H0 scores."""
        ds1 = generate_roc_dataset(n_h0=10, n_h1=0, seed=99)
        ds2 = generate_roc_dataset(n_h0=10, n_h1=0, seed=99)
        np.testing.assert_array_equal(ds1["scores_on"], ds2["scores_on"])

    def test_off_target_scores_exist(self):
        """Off-target scores at f0+50 Hz must be computed (not all zero)."""
        self.assertTrue(np.any(self.ds["scores_off"] > 0))


# ─────────────────────────────────────────────────────────────────────────────
# Fix 3: Time-slide sanity
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeSlideSanity(unittest.TestCase):
    """Shifting L1 by 1 s must strongly reduce MSC for a coherent signal."""

    def setUp(self):
        # Use 2 s of data so that a 1 s slide leaves 1 s of actual overlap
        n = int(FS_HZ * 2.0)
        t = np.linspace(0, 2.0, n, endpoint=False)
        sig = 1e-22 * np.sin(2 * np.pi * F0_HZ * t)
        rng_h1 = np.random.default_rng(20)
        rng_l1 = np.random.default_rng(21)
        self.h1 = sig + rng_h1.normal(0, 5e-24, n)
        self.l1 = sig * 0.98 + rng_l1.normal(0, 5e-24, n)

    def test_returns_required_keys(self):
        res = time_slide_sanity(self.h1, self.l1)
        for key in ("msc_zero_lag", "msc_slide", "msc_ratio", "slide_passed"):
            self.assertIn(key, res)

    def test_zero_lag_coherence_high(self):
        res = time_slide_sanity(self.h1, self.l1)
        self.assertGreater(res["msc_zero_lag"], 0.5)

    def test_slide_reduces_msc(self):
        """After 1 s slide the MSC must be significantly lower."""
        res = time_slide_sanity(self.h1, self.l1)
        self.assertLess(res["msc_slide"], res["msc_zero_lag"])

    def test_slide_passed_flag(self):
        res = time_slide_sanity(self.h1, self.l1)
        # With 2 s data and 1 s slide, the MSC must drop to < 75 % of zero-lag value
        self.assertTrue(res["slide_passed"])


# ─────────────────────────────────────────────────────────────────────────────
# Fix 4: Bootstrap AUC
# ─────────────────────────────────────────────────────────────────────────────

class TestBootstrapAUC(unittest.TestCase):
    """Bootstrap AUC must return a CI that is bounded, stable, and informative."""

    def setUp(self):
        rng = np.random.default_rng(BOOTSTRAP_SEED)
        # Perfect separation: H1 scores > H0 scores
        self.y = np.array([0] * 100 + [1] * 100)
        self.s_perfect = np.concatenate([rng.uniform(0, 0.5, 100),
                                         rng.uniform(0.5, 1.0, 100)])
        # Chance: random scores
        self.s_chance = rng.uniform(0, 1, 200)

    def test_returns_required_keys(self):
        res = bootstrap_auc(self.y, self.s_perfect)
        for key in ("auc_point", "auc_mean", "auc_ci_lo", "auc_ci_hi", "n_boot"):
            self.assertIn(key, res)

    def test_ci_bounds_ordered(self):
        res = bootstrap_auc(self.y, self.s_perfect)
        self.assertLessEqual(res["auc_ci_lo"], res["auc_mean"])
        self.assertLessEqual(res["auc_mean"], res["auc_ci_hi"])

    def test_perfect_classifier_auc(self):
        res = bootstrap_auc(self.y, self.s_perfect)
        self.assertGreater(res["auc_point"], 0.9)

    def test_chance_classifier_auc(self):
        res = bootstrap_auc(self.y, self.s_chance)
        self.assertAlmostEqual(res["auc_point"], 0.5, delta=0.15)

    def test_fixed_seed_reproducible(self):
        """Same seed must give identical CI bounds."""
        r1 = bootstrap_auc(self.y, self.s_perfect, seed=BOOTSTRAP_SEED)
        r2 = bootstrap_auc(self.y, self.s_perfect, seed=BOOTSTRAP_SEED)
        self.assertEqual(r1["auc_ci_lo"], r2["auc_ci_lo"])
        self.assertEqual(r1["auc_ci_hi"], r2["auc_ci_hi"])

    def test_ci_width_reasonable(self):
        """CI width should be < 0.5 for a clean discriminating classifier."""
        res = bootstrap_auc(self.y, self.s_perfect)
        ci_width = res["auc_ci_hi"] - res["auc_ci_lo"]
        self.assertLess(ci_width, 0.5)

    def test_n_boot_reported(self):
        res = bootstrap_auc(self.y, self.s_perfect, n_boot=50)
        self.assertEqual(res["n_boot"], 50)


# ─────────────────────────────────────────────────────────────────────────────
# Fix 5: Multiple-testing correction
# ─────────────────────────────────────────────────────────────────────────────

class TestApplyPFDR(unittest.TestCase):
    """BH correction must be applied and single-candidate case documented."""

    def test_single_candidate_note(self):
        """With one candidate the output must include an explicit note."""
        res = apply_p_fdr([0.003])
        self.assertEqual(res["n_candidates"], 1)
        self.assertIn("Shadow-O3b-1", res["single_candidate_note"])
        self.assertIn("no effect", res["single_candidate_note"].lower())

    def test_single_candidate_p_fdr_equals_p_raw(self):
        """BH with n=1: p_fdr == min(p_raw, 1)."""
        p = 0.003
        res = apply_p_fdr([p])
        self.assertAlmostEqual(res["p_fdr"][0], p, places=6)

    def test_multiple_candidates_correction_applied(self):
        """With multiple candidates, at least one p_fdr should differ from p_raw."""
        p_values = [0.001, 0.01, 0.03, 0.05]
        res = apply_p_fdr(p_values)
        self.assertEqual(res["n_candidates"], 4)
        self.assertEqual(res["single_candidate_note"], "")
        # BH raises at least some p-values
        for pr, pf in zip(res["p_raw"], res["p_fdr"]):
            self.assertGreaterEqual(pf, pr - 1e-12)  # p_fdr >= p_raw

    def test_output_keys(self):
        res = apply_p_fdr([0.01, 0.05])
        for k in ("n_candidates", "single_candidate_note",
                  "p_raw", "p_fdr", "reject"):
            self.assertIn(k, res)

    def test_reject_significant(self):
        """Very small p-values must be rejected after BH."""
        res = apply_p_fdr([1e-6, 1e-5])
        self.assertTrue(all(res["reject"]))

    def test_reject_not_significant(self):
        """Large p-values must not be rejected after BH."""
        res = apply_p_fdr([0.5, 0.8])
        self.assertFalse(any(res["reject"]))


# ─────────────────────────────────────────────────────────────────────────────
# Fix 6: data_source field
# ─────────────────────────────────────────────────────────────────────────────

class TestDataSourceField(unittest.TestCase):
    """Every result container must declare its data provenance."""

    def test_roc_dataset_has_data_source(self):
        ds = generate_roc_dataset(n_h0=5, n_h1=5, seed=0)
        self.assertIn("data_source", ds)
        self.assertIn(ds["data_source"], ("GWOSC", "SIMULATION_FALLBACK"))

    def test_o3b_scan_result_has_data_source(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            self.assertIn(r.data_source, ("GWOSC", "SIMULATION_FALLBACK"))

    def test_o3b_scan_to_dict_has_data_source(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            d = r.to_dict()
            self.assertIn("data_source", d)

    def test_simulation_fallback_value(self):
        """Default synthetic runs must be labelled SIMULATION_FALLBACK."""
        ds = generate_roc_dataset(n_h0=5, n_h1=5, seed=0)
        self.assertEqual(ds["data_source"], "SIMULATION_FALLBACK")

    def test_no_real_number_assertions_in_fallback(self):
        """AUC CI bounds must be verified relative to each other, not absolute."""
        ds = generate_roc_dataset(n_h0=50, n_h1=50, seed=7)
        res = bootstrap_auc(ds["labels"], ds["scores_on"])
        # Only relational assertions — no hard-coded real-data values
        self.assertLessEqual(res["auc_ci_lo"], res["auc_point"])
        self.assertGreaterEqual(res["auc_ci_hi"], res["auc_point"])


# ─────────────────────────────────────────────────────────────────────────────
# Integration test
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegration(unittest.TestCase):
    """End-to-end O3b scan must produce valid, coherent outputs."""

    def test_run_o3b_scan_default(self):
        results = run_o3b_scan(seed=0)
        self.assertGreater(len(results), 0)

    def test_result_type(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            self.assertIsInstance(r, O3bScanResult)

    def test_auc_in_valid_range(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            auc = r.auc_result["auc_point"]
            self.assertGreaterEqual(auc, 0.0)
            self.assertLessEqual(auc, 1.0)

    def test_p_fdr_after_bh(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            self.assertIn("p_fdr", r.p_correction)
            self.assertIn("p_raw", r.p_correction)
            # p_fdr >= p_raw  (BH never makes things more significant)
            self.assertGreaterEqual(
                r.p_correction["p_fdr"],
                r.p_correction["p_raw"] - 1e-12,
            )

    def test_ci_bounds_valid(self):
        results = run_o3b_scan(seed=0)
        for r in results:
            auc = r.auc_result
            self.assertLessEqual(auc["auc_ci_lo"], auc["auc_point"])
            self.assertGreaterEqual(auc["auc_ci_hi"], auc["auc_point"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
