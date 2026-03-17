#!/usr/bin/env python3
"""
Tests for scripts/plot_psi_snr_publication.py
==============================================

Validates:
1. PsiSnrBinData — correct construction and array properties
2. compute_survival_snr — numerical correctness of the fit and root
3. PsiSnrPublicationPlot — figure creation and save (matplotlib optional)
4. _generate_spectral_inset — shape and physical plausibility

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import importlib.util
import math
import sys
import unittest
from pathlib import Path

import numpy as np

# ─── load the module under test directly (avoids __init__ import chains) ──────
_SCRIPT = Path(__file__).parent.parent / "scripts" / "plot_psi_snr_publication.py"
_spec = importlib.util.spec_from_file_location("plot_psi_snr_publication", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

PsiSnrBin = _mod.PsiSnrBin
PsiSnrBinData = _mod.PsiSnrBinData
compute_survival_snr = _mod.compute_survival_snr
_psi_model = _mod._psi_model
_generate_spectral_inset = _mod._generate_spectral_inset
PSI_NOISE_FLOOR = _mod.PSI_NOISE_FLOOR
PSI_SURVIVAL_THRESHOLD = _mod.PSI_SURVIVAL_THRESHOLD
F0_HZ = _mod.F0_HZ
DELTA_F_HZ = _mod.DELTA_F_HZ

# Matplotlib / seaborn may be absent in CI — flag accordingly
_MATPLOTLIB_AVAILABLE = _mod.MATPLOTLIB_AVAILABLE


class TestPsiSnrBinData(unittest.TestCase):
    """Unit tests for the PsiSnrBinData data container."""

    def setUp(self):
        self.data = PsiSnrBinData.from_problem_statement()

    def test_four_bins_loaded(self):
        """There must be exactly four bins from the problem statement."""
        self.assertEqual(len(self.data.bins), 4)

    def test_snr_values_positive(self):
        """All SNR bin-centre values must be strictly positive."""
        for b in self.data.bins:
            self.assertGreater(b.snr, 0, f"SNR must be > 0; got {b.snr}")

    def test_psi_mean_in_range(self):
        """Ψ mean must be in (0, 1]."""
        for b in self.data.bins:
            self.assertGreater(b.psi_mean, 0)
            self.assertLessEqual(b.psi_mean, 1.0)

    def test_psi_std_non_negative(self):
        """Ψ std must be ≥ 0."""
        for b in self.data.bins:
            self.assertGreaterEqual(b.psi_std, 0.0)

    def test_snr_descending_order(self):
        """Bins should be in descending SNR order (highest SNR first)."""
        snrs = self.data.snr_array
        self.assertTrue(
            np.all(np.diff(snrs) < 0),
            "Bins must be ordered from highest to lowest SNR",
        )

    def test_psi_descending_with_snr(self):
        """Higher SNR bins should have higher (or equal) Ψ mean."""
        psi = self.data.psi_mean_array
        self.assertTrue(
            np.all(np.diff(psi) <= 0),
            "Ψ mean must be non-increasing as SNR decreases",
        )

    def test_diamond_stability_bin(self):
        """The highest-SNR bin corresponds to the Diamond Stability node."""
        top = self.data.bins[0]
        self.assertAlmostEqual(top.snr, 18.42, places=2)
        self.assertAlmostEqual(top.psi_mean, 0.9984, places=4)
        self.assertAlmostEqual(top.psi_std, 0.0002, places=4)
        self.assertIn("Diamond", top.label)

    def test_symbiosis_rupture_bin(self):
        """The lowest-SNR bin corresponds to the Symbiosis Rupture node."""
        bot = self.data.bins[-1]
        self.assertAlmostEqual(bot.snr, 0.24, places=2)
        self.assertAlmostEqual(bot.psi_mean, 0.5421, places=4)
        self.assertAlmostEqual(bot.psi_std, 0.0890, places=4)
        self.assertIn("Rupture", bot.label)

    def test_array_shapes_consistent(self):
        """All convenience arrays must have the same length."""
        n = len(self.data.bins)
        self.assertEqual(len(self.data.snr_array), n)
        self.assertEqual(len(self.data.psi_mean_array), n)
        self.assertEqual(len(self.data.psi_std_array), n)
        self.assertEqual(len(self.data.colors), n)
        self.assertEqual(len(self.data.labels), n)

    def test_f0_value(self):
        """f₀ stored in the container must equal the module constant."""
        self.assertAlmostEqual(self.data.f0_hz, F0_HZ, places=4)

    def test_delta_f_value(self):
        """Δf stored in the container must equal the module constant."""
        self.assertAlmostEqual(self.data.delta_f_hz, DELTA_F_HZ, places=4)


class TestPsiModel(unittest.TestCase):
    """Unit tests for the parametric Ψ(SNR) model."""

    def test_model_approaches_one_at_high_snr(self):
        """For very high SNR, Ψ should approach 1.0."""
        val = _psi_model(1e6, a=1.0, k=2.0, c=0.5)
        self.assertAlmostEqual(val, 1.0, places=4)

    def test_model_approaches_floor_at_low_snr(self):
        """For very low SNR, Ψ should approach the noise floor c."""
        c = 0.5
        val = _psi_model(1e-9, a=1.0, k=2.0, c=c)
        self.assertAlmostEqual(val, c, delta=0.02)

    def test_model_monotone(self):
        """Ψ(SNR) must be monotonically non-decreasing in SNR."""
        snrs = np.logspace(-1, 2, 200)
        vals = _psi_model(snrs, a=1.0, k=1.5, c=0.5)
        diffs = np.diff(vals)
        self.assertTrue(np.all(diffs >= -1e-12), "Model must be non-decreasing")

    def test_model_output_in_unit_interval(self):
        """All model outputs must be in [0, 1]."""
        snrs = np.logspace(-2, 3, 500)
        vals = _psi_model(snrs, a=1.0, k=1.5, c=0.5)
        self.assertTrue(np.all(vals >= 0))
        self.assertTrue(np.all(vals <= 1.0 + 1e-9))


class TestComputeSurvivalSnr(unittest.TestCase):
    """Unit tests for compute_survival_snr."""

    def setUp(self):
        self.data = PsiSnrBinData.from_problem_statement()

    def test_returns_positive_survival_snr(self):
        """Survival SNR must be a positive finite float."""
        snr_sv, _ = compute_survival_snr(self.data)
        self.assertTrue(math.isfinite(snr_sv), "Survival SNR must be finite")
        self.assertGreater(snr_sv, 0.0, "Survival SNR must be positive")

    def test_survival_snr_below_minimum_data_snr(self):
        """Survival SNR must be < the lowest observed bin SNR (0.24),
        since at 0.24 the signal is already near the noise floor.
        """
        snr_sv, _ = compute_survival_snr(self.data)
        min_data_snr = self.data.snr_array.min()
        self.assertLess(
            snr_sv,
            min_data_snr,
            f"Survival SNR ({snr_sv:.4f}) should be below min data SNR ({min_data_snr})",
        )

    def test_psi_at_survival_snr_near_threshold(self):
        """Evaluating the model at SNR* should yield Ψ ≈ threshold."""
        snr_sv, popt = compute_survival_snr(self.data)
        if not math.isnan(snr_sv):
            psi_at_sv = _psi_model(snr_sv, *popt)
            self.assertAlmostEqual(
                psi_at_sv, PSI_SURVIVAL_THRESHOLD, delta=0.02,
                msg="Ψ at survival SNR must equal threshold within tolerance"
            )

    def test_popt_shape(self):
        """Fit parameters must be a 3-element array."""
        _, popt = compute_survival_snr(self.data)
        self.assertEqual(len(popt), 3)

    def test_custom_threshold_changes_result(self):
        """Using a higher threshold should yield a higher survival SNR."""
        snr_low, _ = compute_survival_snr(self.data, threshold=0.51)
        snr_high, _ = compute_survival_snr(self.data, threshold=0.70)
        self.assertGreater(
            snr_high, snr_low,
            "Higher Ψ threshold must require a higher SNR to survive",
        )


class TestGenerateSpectralInset(unittest.TestCase):
    """Unit tests for the spectral inset data generator."""

    def setUp(self):
        self.freqs, self.asd = _generate_spectral_inset()

    def test_output_shapes_match(self):
        self.assertEqual(len(self.freqs), len(self.asd))

    def test_frequencies_within_zoom_window(self):
        """All returned frequencies must fall within [f0 - 5, f0 + 5] Hz."""
        self.assertTrue(np.all(self.freqs >= F0_HZ - 5.0))
        self.assertTrue(np.all(self.freqs <= F0_HZ + 5.0))

    def test_asd_positive(self):
        """ASD values must be strictly positive."""
        self.assertTrue(np.all(self.asd > 0))

    def test_peak_near_f0(self):
        """The ASD maximum should be located within 1 Hz of f₀."""
        idx_peak = np.argmax(self.asd)
        self.assertAlmostEqual(self.freqs[idx_peak], F0_HZ, delta=1.0)

    def test_reproducible_with_same_seed(self):
        """Two calls with the same seed must produce identical arrays."""
        freqs2, asd2 = _generate_spectral_inset(seed=42)
        np.testing.assert_array_equal(self.freqs, freqs2)
        np.testing.assert_array_almost_equal(self.asd, asd2)


@unittest.skipUnless(_MATPLOTLIB_AVAILABLE, "matplotlib not installed")
class TestPsiSnrPublicationPlot(unittest.TestCase):
    """Integration tests for the PsiSnrPublicationPlot class."""

    def setUp(self):
        self.data = PsiSnrBinData.from_problem_statement()
        self.plotter = _mod.PsiSnrPublicationPlot(self.data)

    def tearDown(self):
        # Close any open matplotlib figures to avoid resource leaks
        import matplotlib.pyplot as plt
        plt.close("all")

    def test_create_publication_figure_returns_figure(self):
        """create_publication_figure must return a matplotlib Figure."""
        import matplotlib.pyplot as plt
        fig = self.plotter.create_publication_figure()
        self.assertIsNotNone(fig)
        self.assertIsInstance(fig, plt.Figure)

    def test_survival_snr_set_after_figure_creation(self):
        """snr_survival attribute must be populated after figure creation."""
        self.plotter.create_publication_figure()
        self.assertIsNotNone(self.plotter.snr_survival)
        self.assertTrue(math.isfinite(self.plotter.snr_survival))

    def test_save_figure_creates_png(self):
        """save_figure must create at least one PNG file on disk."""
        import tempfile
        self.plotter.create_publication_figure()
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.plotter.save_figure(output_dir=Path(tmp))
        png_paths = [p for p in paths if p.suffix == ".png"]
        self.assertGreater(len(png_paths), 0, "At least one PNG must be saved")


class TestModuleConstants(unittest.TestCase):
    """Sanity checks on module-level constants."""

    def test_f0_value(self):
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)

    def test_delta_f_value(self):
        self.assertAlmostEqual(DELTA_F_HZ, 2.0, places=4)

    def test_noise_floor(self):
        self.assertAlmostEqual(PSI_NOISE_FLOOR, 0.5, places=4)

    def test_survival_threshold_above_noise_floor(self):
        self.assertGreater(PSI_SURVIVAL_THRESHOLD, PSI_NOISE_FLOOR)


if __name__ == "__main__":
    unittest.main(verbosity=2)
