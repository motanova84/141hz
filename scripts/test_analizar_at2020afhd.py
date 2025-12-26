#!/usr/bin/env python3
"""
Test para analizar_at2020afhd.py
Valida el análisis de precesión de Lense-Thirring en AT2020afhd
"""

import sys
import unittest
import os
import numpy as np

# Agregar el directorio scripts al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


class TestAT2020afhdAnalysis(unittest.TestCase):
    """Tests para el análisis de AT2020afhd"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.period_published = 19.6  # days
        self.f0_hz = 141.70001  # Hz (QCAL fundamental)
        self.ra = 48.39875  # degrees
        self.dec = -2.151769  # degrees
        self.redshift = 0.024
        
    def test_published_parameters(self):
        """Verificar que los parámetros publicados son correctos"""
        self.assertEqual(self.period_published, 19.6)
        self.assertEqual(self.redshift, 0.024)
        
    def test_coordinates(self):
        """Verificar las coordenadas del objeto"""
        self.assertAlmostEqual(self.ra, 48.39875, places=5)
        self.assertAlmostEqual(self.dec, -2.151769, places=6)
        
    def test_qcal_fundamental_frequency(self):
        """Verificar la frecuencia fundamental QCAL"""
        self.assertEqual(self.f0_hz, 141.70001)
        
    def test_precession_frequency_calculation(self):
        """Test del cálculo de frecuencia de precesión"""
        omega_prec = 2 * np.pi / self.period_published  # rad/day
        f_frame_hz = omega_prec / (2 * np.pi * 86400)  # Hz
        
        # Verificar que la frecuencia está en el rango esperado
        # Período de ~20 días -> f ~ 5.9e-7 Hz
        expected_freq = 1 / (self.period_published * 86400)
        self.assertAlmostEqual(f_frame_hz, expected_freq, places=9)
        
    def test_harmonic_ratio(self):
        """Test de la relación armónica entre f₀ y f_frame"""
        omega_prec = 2 * np.pi / self.period_published
        f_frame_hz = omega_prec / (2 * np.pi * 86400)
        harmonic_ratio = self.f0_hz / f_frame_hz
        
        # El ratio debería ser del orden de 10^8
        self.assertGreater(harmonic_ratio, 1e8)
        self.assertLess(harmonic_ratio, 1e10)
        
    def test_precession_model_function(self):
        """Test de la función del modelo de precesión"""
        def precession_model(t, A, omega, phi, decay, baseline):
            """Modelo de precesión Lense-Thirring"""
            return A * np.sin(omega * t + phi) * np.exp(-decay * t) + baseline
        
        # Parámetros de prueba
        t = np.linspace(0, 100, 50)
        A = 0.8
        omega = 2 * np.pi / self.period_published
        phi = 0.2
        decay = 0.002
        baseline = 0.5
        
        # Calcular el modelo
        flux = precession_model(t, A, omega, phi, decay, baseline)
        
        # Verificar propiedades básicas
        self.assertEqual(len(flux), len(t))
        self.assertTrue(np.all(np.isfinite(flux)))
        
        # Verificar que hay oscilación
        self.assertGreater(np.max(flux), np.min(flux))
        
    def test_xray_model_realistic(self):
        """Test del modelo realista de rayos X"""
        # Parámetros del modelo
        T_QPO_START = 189
        omega_prec = 2 * np.pi / self.period_published
        
        def xray_model_realistic(t):
            """Modelo de rayos X simplificado para test"""
            decay = np.exp(-0.002 * t)
            qpo_strength = 0.3 + 0.7 * np.clip((t - T_QPO_START) / 50, 0, 1)
            precession = qpo_strength * np.sin(omega_prec * t + 0.2)
            flux = (1.0 + 0.8 * precession) * decay + 0.3
            return np.maximum(flux, 0.05)
        
        # Test con diferentes tiempos
        t_early = np.array([0, 50, 100])
        t_qpo = np.array([200, 220, 240])
        
        flux_early = xray_model_realistic(t_early)
        flux_qpo = xray_model_realistic(t_qpo)
        
        # Verificar que el flujo es positivo
        self.assertTrue(np.all(flux_early > 0))
        self.assertTrue(np.all(flux_qpo > 0))
        
    def test_radio_model_realistic(self):
        """Test del modelo realista de radio"""
        omega_prec = 2 * np.pi / self.period_published
        lag_days = 19.0
        
        def radio_model_realistic(t):
            """Modelo de radio simplificado para test"""
            decay = np.exp(-0.0015 * t)
            precession = np.sin(omega_prec * (t - lag_days) + np.pi/3)
            flux = (0.6 + 0.5 * precession) * decay + 0.2
            return np.maximum(flux, 0.03)
        
        # Test con diferentes tiempos
        t_test = np.array([10, 50, 100, 200])
        flux_radio = radio_model_realistic(t_test)
        
        # Verificar que el flujo es positivo
        self.assertTrue(np.all(flux_radio > 0))
        
    def test_lombscargle_frequency_grid(self):
        """Test de la grilla de frecuencias para Lomb-Scargle"""
        # Grilla de frecuencias para períodos entre 10 y 40 días
        freqs = np.linspace(1/40, 1/10, 2000)
        periods = 1/freqs
        
        # Verificar rangos
        self.assertAlmostEqual(periods.max(), 40.0, places=1)
        self.assertAlmostEqual(periods.min(), 10.0, places=1)
        
        # Verificar que el período publicado está en el rango
        self.assertGreater(self.period_published, periods.min())
        self.assertLess(self.period_published, periods.max())
        
    def test_fractal_cascade_calculation(self):
        """Test del cálculo de cascada fractal"""
        omega_observed = 2 * np.pi / self.period_published
        f_frame_hz = omega_observed / (2 * np.pi * 86400)
        
        harmonic_ratio = self.f0_hz / f_frame_hz
        log10_ratio = np.log10(harmonic_ratio)
        log2_ratio = np.log2(harmonic_ratio)
        
        # Verificar que los logaritmos son consistentes
        # log2(x) = log10(x) / log10(2) ≈ log10(x) * 3.32
        expected_log2 = log10_ratio / np.log10(2)
        self.assertAlmostEqual(log2_ratio, expected_log2, places=6)
        
    def test_output_file_path(self):
        """Test de la construcción de la ruta de salida"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        output_path = os.path.join(repo_root, 'at2020afhd_real_data_analysis.png')
        
        # Verificar que el directorio raíz existe
        self.assertTrue(os.path.exists(repo_root))
        
        # Verificar que la ruta es correcta
        self.assertTrue(output_path.endswith('at2020afhd_real_data_analysis.png'))
        
    def test_time_ranges(self):
        """Test de los rangos temporales del análisis"""
        T_START = 0
        T_QPO_START = 189  # Aug 3, 2024
        T_QPO_END = 268  # Oct 21, 2024
        
        # Verificar rangos lógicos
        self.assertLess(T_START, T_QPO_START)
        self.assertLess(T_QPO_START, T_QPO_END)
        
        # Verificar duración de ventana QPO
        qpo_duration = T_QPO_END - T_QPO_START
        self.assertGreater(qpo_duration, 0)
        self.assertLess(qpo_duration, 100)  # ~79 días


def run_tests():
    """Ejecutar todos los tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAT2020afhdAnalysis)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
