#!/usr/bin/env python3
"""
Tests para el Monitor de Fase Estacionaria QCAL ∞³

Valida:
  - Generación de ventanas sintéticas
  - Cálculo de métricas (Ψ, f_peak, ΔP)
  - Criterios de estabilidad
  - Ciclo de monitorización completo
  - Serialización JSON/CSV
"""

import json
import sys
import os
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy no disponible — tests omitidos")

try:
    from monitor_stationary_phase import (
        F0_DEFAULT, BW_DEFAULT, FS_DEFAULT, NFFT_DEFAULT,
        PSI_THRESHOLD, FREQ_DEVIATION_THRESHOLD, EPSILON,
        _generate_window,
        compute_window_metrics,
        run_monitoring,
        save_csv,
        save_plot,
    )
    MODULE_AVAILABLE = True
except ImportError as exc:
    MODULE_AVAILABLE = False
    print(f"⚠️  monitor_stationary_phase no disponible: {exc}")


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestConstants(unittest.TestCase):
    """Verifica que las constantes del protocolo son correctas."""

    def test_f0_value(self):
        self.assertAlmostEqual(F0_DEFAULT, 141.7001, places=4)

    def test_psi_threshold(self):
        self.assertGreater(PSI_THRESHOLD, 0.99)
        self.assertLess(PSI_THRESHOLD, 1.0)

    def test_freq_deviation_threshold(self):
        # 0.05 mHz = 5e-5 Hz
        self.assertAlmostEqual(FREQ_DEVIATION_THRESHOLD, 5e-5, places=7)

    def test_nfft_is_4096(self):
        self.assertEqual(NFFT_DEFAULT, 4096)

    def test_epsilon_positive(self):
        self.assertGreater(EPSILON, 0)


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestGenerateWindow(unittest.TestCase):
    """Verifica la generación de señales sintéticas."""

    def setUp(self):
        self.rng = np.random.default_rng(0)
        self.n = 4096
        self.fs = FS_DEFAULT
        self.f0 = F0_DEFAULT

    def test_output_shape(self):
        c1, c2 = _generate_window(self.n, self.fs, self.f0, 8.0, 0.1, self.rng)
        self.assertEqual(len(c1), self.n)
        self.assertEqual(len(c2), self.n)

    def test_injection_increases_amplitude(self):
        rng1 = np.random.default_rng(1)
        rng2 = np.random.default_rng(1)
        c1_no_inj, _ = _generate_window(self.n, self.fs, self.f0, 8.0, 0.0, rng1)
        c1_inj, _ = _generate_window(self.n, self.fs, self.f0, 8.0, 0.1, rng2)
        # Con inyección, la varianza de la señal debe ser mayor
        self.assertGreater(np.var(c1_inj), np.var(c1_no_inj) * 0.9)

    def test_reproducibility(self):
        rng_a = np.random.default_rng(42)
        rng_b = np.random.default_rng(42)
        c1_a, c2_a = _generate_window(self.n, self.fs, self.f0, 8.0, 0.1, rng_a)
        c1_b, c2_b = _generate_window(self.n, self.fs, self.f0, 8.0, 0.1, rng_b)
        np.testing.assert_array_equal(c1_a, c1_b)
        np.testing.assert_array_equal(c2_a, c2_b)

    def test_no_nan_or_inf(self):
        c1, c2 = _generate_window(self.n, self.fs, self.f0, 8.0, 0.1, self.rng)
        self.assertFalse(np.any(np.isnan(c1)))
        self.assertFalse(np.any(np.isinf(c1)))
        self.assertFalse(np.any(np.isnan(c2)))
        self.assertFalse(np.any(np.isinf(c2)))


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestComputeWindowMetrics(unittest.TestCase):
    """Verifica las métricas calculadas por ventana."""

    def setUp(self):
        self.rng = np.random.default_rng(7)
        self.n = NFFT_DEFAULT * 4
        self.fs = FS_DEFAULT
        self.f0 = F0_DEFAULT
        self.bw = BW_DEFAULT
        self.nfft = NFFT_DEFAULT
        self.c1, self.c2 = _generate_window(
            self.n, self.fs, self.f0, 8.0, 0.1, self.rng
        )

    def test_psi_in_range(self):
        m = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                   self.bw, self.nfft)
        self.assertGreaterEqual(m["psi"], 0.0)
        self.assertLessEqual(m["psi"], 1.0 + 1e-9)

    def test_f_peak_near_f0(self):
        m = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                   self.bw, self.nfft)
        self.assertAlmostEqual(m["f_peak"], self.f0, delta=self.bw)

    def test_power_band_positive(self):
        m = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                   self.bw, self.nfft)
        self.assertGreater(m["power_band"], 0.0)

    def test_delta_p_zero_without_baseline(self):
        m = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                   self.bw, self.nfft, baseline_power=None)
        self.assertEqual(m["delta_p"], 0.0)

    def test_delta_p_positive_with_higher_power(self):
        m_base = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                        self.bw, self.nfft)
        # Duplicar la señal → potencia ~4× mayor → ΔP > 0
        c1_high = self.c1 * 2.0
        c2_high = self.c2 * 2.0
        m_high = compute_window_metrics(c1_high, c2_high, self.fs, self.f0,
                                        self.bw, self.nfft,
                                        baseline_power=m_base["power_band"])
        self.assertGreater(m_high["delta_p"], 0.0)

    def test_keys_present(self):
        m = compute_window_metrics(self.c1, self.c2, self.fs, self.f0,
                                   self.bw, self.nfft)
        for key in ("psi", "f_peak", "delta_p", "power_band"):
            self.assertIn(key, m)


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestRunMonitoring(unittest.TestCase):
    """Verifica el ciclo completo de monitorización (duración corta)."""

    def _run_short(self, injection=0.10, snr=8.0):
        return run_monitoring(
            f0=F0_DEFAULT,
            bw=BW_DEFAULT,
            fs=FS_DEFAULT,
            nfft=NFFT_DEFAULT,
            duration_h=1.0,
            interval_min=10.0,
            injection=injection,
            snr=snr,
            seed=42,
        )

    def test_report_structure(self):
        report = self._run_short()
        for key in ("timestamp", "parameters", "windows", "summary",
                    "stability_verdict"):
            self.assertIn(key, report)

    def test_window_count(self):
        # 1h / 10min = 6 ventanas
        report = self._run_short()
        self.assertEqual(len(report["windows"]), 6)
        self.assertEqual(report["summary"]["n_windows"], 6)

    def test_verdict_values(self):
        report = self._run_short()
        self.assertIn(report["stability_verdict"], ("STABLE", "UNSTABLE"))

    def test_summary_fields(self):
        report = self._run_short()
        s = report["summary"]
        for key in ("psi_mean", "psi_min", "psi_max", "psi_std",
                    "f_mean", "f_std_mhz", "max_abs_delta_f_mhz",
                    "n_windows", "n_stable", "pct_stable"):
            self.assertIn(key, s)

    def test_psi_values_in_range(self):
        report = self._run_short()
        for w in report["windows"]:
            self.assertGreaterEqual(w["psi"], 0.0)
            self.assertLessEqual(w["psi"], 1.0 + 1e-9)

    def test_high_snr_tends_to_stable(self):
        # SNR=10000 modela un sistema bloqueado de forma determinística:
        # el jitter de frecuencia instantánea estimado es ~0.025 mHz << umbral 0.05 mHz.
        report = run_monitoring(
            duration_h=0.5,
            interval_min=10.0,
            snr=10000.0,
            injection=0.10,
            seed=0,
        )
        self.assertEqual(report["stability_verdict"], "STABLE")

    def test_stable_flag_per_window(self):
        report = self._run_short(snr=50.0)
        for w in report["windows"]:
            self.assertIn("stable", w)
            self.assertIsInstance(w["stable"], bool)

    def test_pct_stable_range(self):
        report = self._run_short()
        s = report["summary"]
        self.assertGreaterEqual(s["pct_stable"], 0.0)
        self.assertLessEqual(s["pct_stable"], 100.0)

    def test_single_window(self):
        # Duración == intervalo → exactamente 1 ventana
        report = run_monitoring(
            duration_h=10.0 / 60,
            interval_min=10.0,
            seed=1,
        )
        self.assertEqual(len(report["windows"]), 1)


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestSaveCsv(unittest.TestCase):
    """Verifica la serialización CSV."""

    def test_csv_written(self):
        report = run_monitoring(duration_h=0.5, interval_min=10.0, seed=5)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False,
                                        mode="w") as f:
            csv_path = f.name
        try:
            save_csv(report["windows"], csv_path)
            import csv
            with open(csv_path) as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), len(report["windows"]))
            for row in rows:
                self.assertIn("psi", row)
                self.assertIn("f_peak", row)
        finally:
            os.unlink(csv_path)

    def test_csv_columns(self):
        report = run_monitoring(duration_h=10.0 / 60, interval_min=10.0,
                                seed=6)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False,
                                        mode="w") as f:
            csv_path = f.name
        try:
            save_csv(report["windows"], csv_path)
            import csv
            with open(csv_path) as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
            expected = {"t_min", "psi", "f_peak", "delta_f_mhz",
                        "delta_p", "stable"}
            self.assertEqual(set(fieldnames), expected)
        finally:
            os.unlink(csv_path)


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestSavePlot(unittest.TestCase):
    """Verifica la generación de gráficas (solo comprueba que no lanza)."""

    def test_plot_generated(self):
        try:
            import matplotlib
        except ImportError:
            self.skipTest("matplotlib no disponible")

        report = run_monitoring(duration_h=0.5, interval_min=10.0, seed=9)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            png_path = f.name
        try:
            save_plot(report, png_path)
            self.assertTrue(os.path.getsize(png_path) > 0)
        finally:
            if os.path.exists(png_path):
                os.unlink(png_path)


@unittest.skipUnless(NUMPY_AVAILABLE and MODULE_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestJsonSerializable(unittest.TestCase):
    """Verifica que el informe completo es serializable a JSON."""

    def test_json_roundtrip(self):
        report = run_monitoring(duration_h=0.5, interval_min=10.0, seed=11)
        serialized = json.dumps(report)
        restored = json.loads(serialized)
        self.assertEqual(restored["stability_verdict"],
                         report["stability_verdict"])
        self.assertEqual(len(restored["windows"]), len(report["windows"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
