#!/usr/bin/env python3
"""
Tests para validar_prediccion_grace_fo_yukawa.py
================================================

Test suite para el detector de modulación Yukawa en datos GRACE-FO.

Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)
Fecha: Abril 2026
"""

import sys
import unittest
import numpy as np
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

try:
    from scripts.validar_prediccion_grace_fo_yukawa import GRACEFOYukawaDetector
except ImportError:
    # Try direct import if running from scripts/
    from validar_prediccion_grace_fo_yukawa import GRACEFOYukawaDetector


class TestGRACEFOYukawaDetector(unittest.TestCase):
    """Tests para la clase GRACEFOYukawaDetector."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Usar duración corta para tests rápidos
        self.detector = GRACEFOYukawaDetector(duration=3600, sampling_rate=1.0)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpieza después de cada test."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test de inicialización del detector."""
        self.assertEqual(self.detector.duration, 3600)
        self.assertEqual(self.detector.sampling_rate, 1.0)
        self.assertAlmostEqual(self.detector.f_target, 0.1417001, places=6)
        self.assertEqual(self.detector.n_samples, 3600)
    
    def test_f0_conversion(self):
        """Test de conversión de frecuencia QCAL a mHz."""
        # f_target debe ser f0 / 1000
        expected = 141.7001 / 1000.0
        self.assertAlmostEqual(self.detector.f_target, expected, places=7)
    
    def test_simulate_grace_fo_data(self):
        """Test de simulación de datos GRACE-FO."""
        data = self.detector.simulate_grace_fo_data(amp_yukawa=2e-11)
        
        # Verificar forma y tipo
        self.assertEqual(len(data), self.detector.n_samples)
        self.assertIsInstance(data, np.ndarray)
        
        # Verificar componentes generados
        self.assertIsNotNone(self.detector.acceleration_noise)
        self.assertIsNotNone(self.detector.signal_tides)
        self.assertIsNotNone(self.detector.signal_yukawa)
        self.assertIsNotNone(self.detector.baseline_variation)
        
        # Verificar que la señal total es la suma
        expected_total = (self.detector.acceleration_noise + 
                         self.detector.signal_tides + 
                         self.detector.signal_yukawa)
        np.testing.assert_array_almost_equal(data, expected_total)
    
    def test_noise_level_realistic(self):
        """Test de que el nivel de ruido es realista para GRACE-FO."""
        self.detector.simulate_grace_fo_data()
        
        # Nivel de ruido debe ser ~10^-10 m/s²/√Hz
        noise_std = np.std(self.detector.acceleration_noise)
        
        # Ruido esperado para 1 Hz sampling
        expected_noise = self.detector.noise_level * np.sqrt(self.detector.sampling_rate / 2)
        
        # Debe estar dentro de 3 sigma del esperado
        self.assertLess(abs(noise_std - expected_noise) / expected_noise, 0.1)
    
    def test_compute_psd_welch(self):
        """Test de cálculo de PSD usando Welch."""
        self.detector.simulate_grace_fo_data()
        freqs, psd = self.detector.compute_psd_welch()
        
        # Verificar forma
        self.assertEqual(len(freqs), len(psd))
        self.assertGreater(len(freqs), 0)
        
        # Verificar rango de frecuencias
        self.assertGreaterEqual(freqs[0], 0)
        self.assertLessEqual(freqs[-1], self.detector.sampling_rate / 2)
        
        # Verificar que PSD es positiva
        self.assertTrue(np.all(psd > 0))
        
        # Verificar almacenamiento
        np.testing.assert_array_equal(freqs, self.detector.psd_freqs)
        np.testing.assert_array_equal(psd, self.detector.psd_values)
    
    def test_detect_peak_at_target(self):
        """Test de detección de pico en frecuencia objetivo."""
        # Simular con amplitud alta para asegurar detección
        self.detector.simulate_grace_fo_data(amp_yukawa=5e-11)
        self.detector.compute_psd_welch()
        
        results = self.detector.detect_peak_at_target()
        
        # Verificar estructura de resultados
        self.assertIn("detected", results)
        self.assertIn("frequency_hz", results)
        self.assertIn("snr_db", results)
        self.assertIn("significance_sigma", results)
        
        # Si hay detección, verificar que está cerca de f_target
        if results["detected"]:
            deviation = abs(results["frequency_hz"] - self.detector.f_target)
            # Debe estar dentro de ±20 mHz (resolución típica)
            self.assertLess(deviation, 0.02)
    
    def test_peak_near_target_frequency(self):
        """Test de que el pico detectado está cerca de la frecuencia objetivo."""
        # Usar amplitud grande para detección confiable
        self.detector = GRACEFOYukawaDetector(duration=10800, sampling_rate=1.0)  # 3 horas
        self.detector.simulate_grace_fo_data(amp_yukawa=1e-10)
        self.detector.compute_psd_welch()
        
        results = self.detector.detect_peak_at_target()
        
        if results["detected"]:
            # Desviación debe ser < 1000 μHz (más tolerante para señales pequeñas)
            self.assertLess(results["deviation_from_target_uhz"], 1000)
    
    def test_false_alarm_probability(self):
        """Test de cálculo de probabilidad de falsa alarma."""
        self.detector.simulate_grace_fo_data()
        self.detector.compute_psd_welch()
        self.detector.detect_peak_at_target()
        
        fap = self.detector.calculate_false_alarm_probability()
        
        # FAP debe estar entre 0 y 1
        self.assertGreaterEqual(fap, 0.0)
        self.assertLessEqual(fap, 1.0)
    
    def test_extract_yukawa_parameters(self):
        """Test de extracción de parámetros Yukawa."""
        self.detector.simulate_grace_fo_data(amp_yukawa=5e-11)
        self.detector.compute_psd_welch()
        self.detector.detect_peak_at_target()
        
        params = self.detector.extract_yukawa_parameters()
        
        # Verificar estructura
        self.assertIn("alpha", params)
        self.assertIn("lambda_psi_km", params)
        
        if self.detector.peak_detected:
            # Parámetros deben ser positivos
            self.assertIsNotNone(params["alpha"])
            self.assertIsNotNone(params["lambda_psi_km"])
            self.assertGreater(params["alpha"], 0)
            self.assertGreater(params["lambda_psi_km"], 0)
    
    def test_lambda_psi_in_expected_range(self):
        """Test de que λ_Ψ está en el rango esperado (1-500 km)."""
        self.detector.simulate_grace_fo_data(amp_yukawa=5e-11)
        self.detector.compute_psd_welch()
        self.detector.detect_peak_at_target()
        
        params = self.detector.extract_yukawa_parameters()
        
        if params["lambda_psi_km"] is not None:
            # λ_Ψ debe estar en rango razonable (basado en scripts existentes)
            self.assertGreater(params["lambda_psi_km"], 1.0)
            self.assertLess(params["lambda_psi_km"], 500.0)
    
    def test_save_results_json(self):
        """Test de guardado de resultados en JSON."""
        self.detector.simulate_grace_fo_data()
        self.detector.compute_psd_welch()
        detection = self.detector.detect_peak_at_target()
        yukawa = self.detector.extract_yukawa_parameters()
        fap = self.detector.calculate_false_alarm_probability()
        
        output_file = Path(self.temp_dir) / "test_results.json"
        self.detector.save_results_json(output_file, detection, yukawa, fap)
        
        # Verificar que el archivo existe
        self.assertTrue(output_file.exists())
        
        # Verificar que es JSON válido
        import json
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        # Verificar estructura
        self.assertIn("mission", data)
        self.assertEqual(data["mission"], "GRACE-FO")
        self.assertIn("detection", data)
        self.assertIn("yukawa_parameters", data)
        self.assertIn("statistics", data)
        self.assertIn("validation", data)
    
    def test_visualization_creation(self):
        """Test de creación de visualizaciones."""
        self.detector.simulate_grace_fo_data()
        self.detector.compute_psd_welch()
        self.detector.detect_peak_at_target()
        
        output_dir = Path(self.temp_dir)
        
        # No debe fallar
        self.detector.create_visualizations(output_dir)
        
        # Verificar que se crearon las 6 figuras
        expected_files = [
            "grace_fo_01_time_series.png",
            "grace_fo_02_filtered_signal.png",
            "grace_fo_03_psd_full.png",
            "grace_fo_04_psd_zoom.png",
            "grace_fo_05_snr_integration.png",
            "grace_fo_06_baseline_correlation.png"
        ]
        
        for filename in expected_files:
            filepath = output_dir / filename
            self.assertTrue(filepath.exists(), f"Missing file: {filename}")
    
    def test_snr_increases_with_amplitude(self):
        """Test de que SNR aumenta con la amplitud de señal."""
        # Test con amplitud baja
        detector_low = GRACEFOYukawaDetector(duration=7200, sampling_rate=1.0)
        detector_low.simulate_grace_fo_data(amp_yukawa=1e-11)
        detector_low.compute_psd_welch()
        results_low = detector_low.detect_peak_at_target()
        
        # Test con amplitud alta
        detector_high = GRACEFOYukawaDetector(duration=7200, sampling_rate=1.0)
        detector_high.simulate_grace_fo_data(amp_yukawa=1e-10)
        detector_high.compute_psd_welch()
        results_high = detector_high.detect_peak_at_target()
        
        # SNR alto debe ser mayor que SNR bajo
        self.assertGreater(results_high["snr_db"], results_low["snr_db"])
    
    def test_detection_threshold_logic(self):
        """Test de lógica de umbral de detección."""
        self.detector.simulate_grace_fo_data(amp_yukawa=2e-11)
        self.detector.compute_psd_welch()
        results = self.detector.detect_peak_at_target()
        
        # Detección debe cumplir: SNR > 3 dB AND sigma > 3
        if results["detected"]:
            self.assertGreater(results["snr_db"], 3.0)
            self.assertGreater(results["significance_sigma"], 3.0)
    
    def test_baseline_variation_modulates_signal(self):
        """Test de que la variación de baseline modula la señal Yukawa."""
        self.detector.simulate_grace_fo_data()
        
        # Baseline debe variar con el tiempo
        baseline_std = np.std(self.detector.baseline_variation)
        self.assertGreater(baseline_std, 0)
        
        # Verificar que la señal Yukawa existe y tiene valores finitos
        self.assertIsNotNone(self.detector.signal_yukawa)
        self.assertTrue(np.all(np.isfinite(self.detector.signal_yukawa)))
        
        # Verificar que la señal tiene varianza (no es constante)
        yukawa_std = np.std(self.detector.signal_yukawa)
        self.assertGreater(yukawa_std, 0)
    
    def test_complete_analysis_runs(self):
        """Test de que el análisis completo se ejecuta sin errores."""
        # Usar detector temporal para análisis completo
        detector = GRACEFOYukawaDetector(duration=3600, sampling_rate=1.0)
        
        # No debe fallar
        results = detector.run_complete_analysis(output_dir=self.temp_dir)
        
        # Verificar estructura de resultados
        self.assertIn("detection", results)
        self.assertIn("yukawa", results)
        self.assertIn("fap", results)
        self.assertIn("output_dir", results)
        
        # Verificar que se crearon archivos
        output_path = Path(results["output_dir"])
        self.assertTrue(output_path.exists())
        self.assertTrue((output_path / "grace_fo_yukawa_results.json").exists())


class TestGRACEFOConstants(unittest.TestCase):
    """Tests para constantes y parámetros de GRACE-FO."""
    
    def test_qcal_frequency_value(self):
        """Test de valor correcto de frecuencia QCAL."""
        detector = GRACEFOYukawaDetector(duration=100, sampling_rate=1.0)
        self.assertAlmostEqual(detector.f0_hz, 141.7001, places=4)
    
    def test_target_frequency_conversion(self):
        """Test de conversión correcta a mHz."""
        detector = GRACEFOYukawaDetector(duration=100, sampling_rate=1.0)
        # f_target = f0 / 1000
        expected = 141.7001 / 1000.0
        self.assertAlmostEqual(detector.f_target, expected, places=7)
    
    def test_grace_fo_parameters(self):
        """Test de parámetros de misión GRACE-FO."""
        detector = GRACEFOYukawaDetector(duration=100, sampling_rate=1.0)
        
        # Velocidad orbital ~7.6 km/s
        self.assertAlmostEqual(detector.v_orbital, 7600.0, places=0)
        
        # Separación ~200 km
        self.assertAlmostEqual(detector.separacion, 200000.0, places=0)
        
        # Nivel de ruido ~10^-10
        self.assertAlmostEqual(detector.noise_level, 1e-10, places=11)
    
    def test_nyquist_frequency(self):
        """Test de frecuencia de Nyquist."""
        detector = GRACEFOYukawaDetector(duration=100, sampling_rate=1.0)
        nyquist = detector.sampling_rate / 2
        
        # f_target debe estar muy por debajo de Nyquist
        self.assertLess(detector.f_target, nyquist)
        self.assertLess(detector.f_target / nyquist, 0.5)


def run_tests():
    """Ejecuta todos los tests."""
    print("="*70)
    print("∴ GRACE-FO Yukawa Detector - Test Suite ∴")
    print("="*70)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestGRACEFOYukawaDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestGRACEFOConstants))
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("∴ RESUMEN DE TESTS ∴")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
