#!/usr/bin/env python3
"""
Tests para el pipeline de búsqueda LISA.
"""

import unittest
import numpy as np
import sys
import os
from pathlib import Path

# Añadir lisa al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lisa'))

from lisa_search_pipeline import LISASearchPipeline


class TestLISASearchPipeline(unittest.TestCase):
    """Tests para LISASearchPipeline."""
    
    def setUp(self):
        """Configurar pipeline para tests."""
        self.pipeline = LISASearchPipeline(
            sample_rate=10.0,
            duration=3600.0  # 1 hora para tests rápidos
        )
    
    def test_calculate_harmonic_frequencies(self):
        """Test de cálculo de frecuencias armónicas."""
        harmonics = self.pipeline.calculate_harmonic_frequencies(n_max=1000)
        
        # Verificar que hay frecuencias
        self.assertGreater(len(harmonics), 0)
        
        # Verificar que están en rango LISA
        for f in harmonics:
            self.assertGreaterEqual(f, 0.0001)
            self.assertLessEqual(f, 1.0)
        
        # Verificar que están ordenadas descendentemente
        for i in range(len(harmonics) - 1):
            self.assertGreater(harmonics[i], harmonics[i+1])
    
    def test_noise_spectral_density(self):
        """Test de densidad espectral de ruido."""
        f_test = np.array([0.001, 0.01, 0.1, 1.0])
        S_n = self.pipeline.noise_spectral_density(f_test)
        
        # Verificar dimensiones
        self.assertEqual(len(S_n), len(f_test))
        
        # Verificar que son positivos
        self.assertTrue(np.all(S_n > 0))
    
    def test_calculate_snr(self):
        """Test de cálculo de SNR."""
        h0 = 1e-20
        f_target = 0.1
        
        snr = self.pipeline.calculate_snr(h0, f_target)
        
        # Verificar que es positivo
        self.assertGreater(snr, 0)
        
        # Verificar que escala con h0
        snr2 = self.pipeline.calculate_snr(2*h0, f_target)
        self.assertAlmostEqual(snr2/snr, 2.0, places=5)
    
    def test_generate_tdi_signal(self):
        """Test de generación de señal TDI."""
        frequencies = [0.1, 0.05]
        amplitudes = [1e-20, 5e-21]
        
        t, signal = self.pipeline.generate_tdi_signal(
            frequencies=frequencies,
            amplitudes=amplitudes,
            noise_level=1e-21
        )
        
        # Verificar dimensiones
        expected_samples = int(self.pipeline.sample_rate * self.pipeline.duration)
        self.assertEqual(len(t), expected_samples)
        self.assertEqual(len(signal), expected_samples)
        
        # Verificar que no son todos ceros
        self.assertGreater(np.std(signal), 0)
    
    def test_perform_fft_analysis(self):
        """Test de análisis FFT."""
        # Generar señal de prueba
        frequencies = [0.0877]  # Primer armónico
        t, signal = self.pipeline.generate_tdi_signal(
            frequencies=frequencies,
            amplitudes=[1e-20],
            noise_level=1e-22
        )
        
        # Análisis FFT
        results = self.pipeline.perform_fft_analysis(signal, frequencies)
        
        # Verificar estructura de resultados
        self.assertIn('frequencies_searched', results)
        self.assertIn('detections', results)
        self.assertIn('spectrum', results)
        
        # Verificar que detecta la frecuencia
        self.assertGreater(len(results['detections']), 0)
    
    def test_run_targeted_search(self):
        """Test de búsqueda dirigida completa."""
        # Ejecutar con parámetros reducidos para tests
        results = self.pipeline.run_targeted_search(
            n_harmonics=1000,
            save_results=False
        )
        
        # Verificar estructura de resultados
        self.assertIn('f0', results)
        self.assertIn('phi', results)
        self.assertIn('harmonics', results)
        self.assertIn('detections', results)
        
        # Verificar valores
        self.assertEqual(results['f0'], 141.7001)
        self.assertAlmostEqual(results['phi'], 1.618033988749895, places=10)
        
        # Verificar que hay detecciones (debería tener harmonics en rango LISA)
        self.assertGreater(len(results['harmonics']), 0)


class TestLISAPhysics(unittest.TestCase):
    """Tests de física LISA."""
    
    def test_phi_value(self):
        """Test del valor del número áureo."""
        from lisa_search_pipeline import PHI
        
        # Verificar valor exacto
        phi_expected = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, phi_expected, places=15)


def main():
    """Ejecutar tests."""
    unittest.main()


if __name__ == '__main__':
    main()
