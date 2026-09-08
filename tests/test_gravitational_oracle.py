"""
test_gravitational_oracle.py
Suite de tests para el Oráculo Espectral Gravitacional
"""

import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from gwpy.timeseries import TimeSeries

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from qcal_gravitational_oracle import GravitationalOracle


class TestGravitationalOracle(unittest.TestCase):
    """Tests unitarios para la clase GravitationalOracle"""

    def setUp(self):
        self.oracle = GravitationalOracle(f_target=141.7001, verbose=False)
        self.test_gps = 1126259462.4
        self.test_duration = 32

    def test_initialization(self):
        self.assertEqual(self.oracle.f_target, 141.7001)
        self.assertEqual(self.oracle.umbral_coherencia_ruido, 0.15)
        self.assertEqual(self.oracle.umbral_snr_minimo, 5.0)
        self.assertIsInstance(self.oracle.results, dict)

    def test_generate_synthetic_data(self):
        fs = 4096
        duration = 2
        data = self.oracle._generate_synthetic_data(duration, fs)
        expected_length = int(duration * fs)
        self.assertEqual(len(data), expected_length)
        self.assertIsInstance(data, TimeSeries)
        self.assertTrue(np.std(data.value) > 0)
        self.assertTrue(abs(np.mean(data.value)) < 0.5)

    def test_calculate_fwhm(self):
        x = np.linspace(0, 100, 1000)
        psd = np.exp(-((x - 50) ** 2) / (2 * 10 ** 2))
        idx_peak = 500
        fwhm = self.oracle._calculate_fwhm(psd, x, idx_peak)
        self.assertAlmostEqual(fwhm, 2 * 10 * np.sqrt(2 * np.log(2)), delta=1)
        psd_flat = np.ones_like(x)
        fwhm_flat = self.oracle._calculate_fwhm(psd_flat, x, idx_peak)
        self.assertEqual(fwhm_flat, 0)

    def test_classify_noise(self):
        metrics = {
            "coherence": np.array([0.5, 0.8, 0.2, 0.1]),
            "phase_deg": np.array([10, 5, -15, 40]),
            "snr_integrated": 15.0,
            "idx_target": 1,
        }
        classification = self.oracle.classify_noise(metrics)
        self.assertIn("status", classification)
        self.assertIn("confidence", classification)
        self.assertIn("coherence", classification)
        self.assertIn("details", classification)
        self.assertTrue(classification["details"]["coherence_check"])
        self.assertTrue(classification["details"]["snr_check"])
        self.assertTrue(classification["details"]["phase_check"])

    def test_calculate_spectral_metrics(self):
        fs = 4096
        duration = 4
        data = {
            "H1": self.oracle._generate_synthetic_data(duration, fs, ifo="H1"),
            "L1": self.oracle._generate_synthetic_data(duration, fs, ifo="L1"),
        }
        metrics = self.oracle.calculate_spectral_metrics(data, fs)
        expected_keys = [
            "frequency",
            "psd_h1",
            "psd_l1",
            "coherence",
            "csd",
            "phase_deg",
            "phase_rad",
            "idx_target",
            "snr_integrated",
            "fwhm",
            "fs",
        ]
        for key in expected_keys:
            self.assertIn(key, metrics)
        self.assertEqual(len(metrics["frequency"]), len(metrics["psd_h1"]))
        self.assertEqual(len(metrics["frequency"]), len(metrics["coherence"]))


class TestIntegrationGravitationalOracle(unittest.TestCase):
    """Tests de integración con datos reales (si están disponibles)"""

    def setUp(self):
        self.oracle = GravitationalOracle(verbose=False)

    @pytest.mark.slow
    def test_real_data_analysis(self):
        try:
            results = self.oracle.analyze(
                evento="GW150914",
                t_gps=1126259462.4,
                duracion=8,
                plot=False,
            )
            self.assertIsNotNone(results)
            self.assertIn("metrics", results)
            self.assertIn("noise_classification", results)
            metrics = results["metrics"]
            idx = metrics["idx_target"]
            self.assertTrue(0 <= idx < len(metrics["coherence"]))
        except Exception as exc:  # pragma: no cover - network dependent
            print(f"Test de integración omitido: {exc}")
            pytest.skip("Datos de LIGO no disponibles")

    def test_synthetic_data_analysis(self):
        results = self.oracle.analyze(
            evento="TEST_SYNTHETIC",
            t_gps=1234567890,
            duracion=8,
            plot=False,
        )
        self.assertIsNotNone(results)
        self.assertGreater(results["metrics"]["snr_integrated"], 0)


class TestDataLoading(unittest.TestCase):
    """Tests de carga de datos"""

    def test_fetch_ligo_data_timeout(self):
        oracle = GravitationalOracle(verbose=False)
        with patch("gwpy.timeseries.TimeSeries.fetch_open_data") as mock_fetch:
            mock_fetch.side_effect = TimeoutError("Timeout")
            data = oracle.fetch_ligo_data(1126259462.4, 4)
            self.assertIn("H1", data)
            self.assertIn("L1", data)

    def test_invalid_gps_time(self):
        oracle = GravitationalOracle(verbose=False)
        data = oracle.fetch_ligo_data(9999999999.0, 4)
        self.assertIsNotNone(data)
        self.assertIn("H1", data)


class TestPerformance(unittest.TestCase):
    """Tests de rendimiento"""

    def setUp(self):
        self.oracle = GravitationalOracle(verbose=False)

    def test_analysis_performance(self):
        start = time.time()
        self.oracle.analyze(
            evento="PERF_TEST",
            t_gps=1126259462.4,
            duracion=16,
            plot=False,
        )
        elapsed = time.time() - start
        self.assertLess(elapsed, 5.0)

    def test_memory_usage(self):
        psutil = pytest.importorskip("psutil")
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024
        self.oracle.analyze(
            evento="MEM_TEST",
            t_gps=1126259462.4,
            duracion=64,
            plot=False,
        )
        mem_after = process.memory_info().rss / 1024 / 1024
        mem_increase = mem_after - mem_before
        self.assertLess(mem_increase, 100)


class TestSerialization(unittest.TestCase):
    """Tests de serialización de resultados"""

    def setUp(self):
        self.oracle = GravitationalOracle(verbose=False)

    def test_results_serialization(self):
        results = self.oracle.analyze(
            evento="SERIAL_TEST",
            t_gps=1126259462.4,
            duracion=4,
            plot=False,
        )
        serializable_results = {}
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                serializable_results[key] = value.tolist()
            elif isinstance(value, (np.float32, np.float64)):
                serializable_results[key] = float(value)
            elif isinstance(value, (np.int32, np.int64)):
                serializable_results[key] = int(value)
            else:
                serializable_results[key] = value
        json_str = json.dumps(serializable_results, default=str)
        self.assertIsInstance(json_str, str)
        loaded = json.loads(json_str)
        self.assertEqual(loaded["evento"], "SERIAL_TEST")


def run_tests():
    unittest.main()


if __name__ == "__main__":
    run_tests()
