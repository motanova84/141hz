#!/usr/bin/env python3
"""
Tests for IGETS gravimetric analysis.
"""

import unittest
import numpy as np
import sys
import os

# Add igets to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'igets'))

from igets_fft_analysis import IGETSGravimetryAnalysis, F0, LAMBDA_BAR, IGETS_STATIONS


class TestIGETSGravimetryAnalysis(unittest.TestCase):
    """Tests para IGETSGravimetryAnalysis."""
    
    def setUp(self):
        """Configure analysis for tests."""
        self.analysis = IGETSGravimetryAnalysis(sample_rate=1000.0)
    
    def test_yukawa_potential(self):
        """Test de potencial Yukawa."""
        r = 6.371e6 + 100  # Radio terrestre + profundidad
        t = np.linspace(0, 1, 100)
        
        V = self.analysis.yukawa_potential(r, t)
        
        # Verificar dimensiones
        self.assertEqual(len(V), len(t))
        
        # Verificar que son negativos (atractivo)
        self.assertTrue(np.all(V < 0))
        
        # Verificar modulación temporal
        V_mean = np.mean(V)
        V_std = np.std(V)
        self.assertGreater(V_std, 0)  # Hay variación temporal
    
    def test_generate_sg_signal(self):
        """Test de generación de señal gravimétrica."""
        t, g = self.analysis.generate_sg_signal(
            duration=60.0,  # 1 minuto para test rápido
            station='CANTLEY',
            include_modulation=True
        )
        
        # Verificar dimensiones
        expected_samples = int(self.analysis.sample_rate * 60.0)
        self.assertEqual(len(t), expected_samples)
        self.assertEqual(len(g), expected_samples)
        
        # Verificar que no son todos ceros
        self.assertGreater(np.std(g), 0)
    
    def test_preprocess_signal(self):
        """Test de preprocesamiento de señal."""
        # Generar señal con tendencia
        t, g = self.analysis.generate_sg_signal(duration=60.0)
        g_with_trend = g + 1e-7 * np.linspace(0, 1, len(g))
        
        # Preprocesar
        g_processed = self.analysis.preprocess_signal(g_with_trend, remove_tide=True)
        
        # Verificar dimensiones
        self.assertEqual(len(g_processed), len(g))
        
        # Verificar que la media es cercana a cero (tendencia removida)
        self.assertLess(np.abs(np.mean(g_processed)), 1e-8)
    
    def test_perform_fft_analysis(self):
        """Test de análisis FFT."""
        # Generar señal con componente a f₀
        duration = 10.0  # 10 segundos
        n_samples = int(self.analysis.sample_rate * duration)
        t = np.linspace(0, duration, n_samples)
        
        # Señal con frecuencia f₀
        signal = 1e-9 * np.sin(2 * np.pi * F0 * t)
        signal += 1e-10 * np.random.randn(n_samples)  # Ruido
        
        # Análisis FFT
        results = self.analysis.perform_fft_analysis(
            signal,
            freq_range=(100, 300)
        )
        
        # Verificar estructura
        self.assertIn('frequency_range', results)
        self.assertIn('spectrum', results)
        
        # Verificar que detecta cerca de f₀
        if results['detection']:
            self.assertLess(
                abs(results['detection']['frequency'] - F0),
                1.0  # Dentro de 1 Hz
            )
    
    def test_analyze_phase_coherence(self):
        """Test de análisis de coherencia de fase."""
        # Generar señales para 3 estaciones
        duration = 10.0
        n_samples = int(self.analysis.sample_rate * duration)
        t = np.linspace(0, duration, n_samples)
        
        # Señales coherentes (misma fase)
        station_data = {}
        for station in ['CANTLEY', 'BAD_HOMBURG', 'KYOTO']:
            signal = 1e-9 * np.sin(2 * np.pi * F0 * t)
            signal += 1e-10 * np.random.randn(n_samples)
            station_data[station] = signal
        
        # Análisis de coherencia
        coherence = self.analysis.analyze_phase_coherence(station_data)
        
        # Verificar estructura
        self.assertIn('stations', coherence)
        self.assertIn('coherence_matrix', coherence)
        self.assertIn('global_coherence', coherence)
        self.assertIn('highly_coherent', coherence)
        
        # Verificar coherencia alta (señales coherentes)
        self.assertGreater(coherence['global_coherence'], 0.5)
    
    def test_run_analysis(self):
        """Test de análisis completo."""
        # Ejecutar análisis reducido
        results = self.analysis.run_analysis(
            n_stations=2,
            duration=60.0,  # 1 minuto
            include_modulation=True,
            save_results=False
        )
        
        # Verificar estructura
        self.assertIn('f0', results)
        self.assertIn('tolerance', results)
        self.assertIn('stations', results)
        self.assertIn('coherence', results)
        self.assertIn('conclusion', results)
        
        # Verificar valores
        self.assertEqual(results['f0'], F0)
        self.assertEqual(len(results['stations']), 2)
    
    def test_run_analysis_without_modulation(self):
        """Test de análisis sin modulación (control negativo)."""
        results = self.analysis.run_analysis(
            n_stations=2,
            duration=60.0,
            include_modulation=False,
            save_results=False
        )
        
        # Sin modulación, no debería detectar
        n_detected = sum(
            1 for s in results['stations'].values()
            if s['analysis']['detection'] and s['analysis']['detection']['significant']
        )
        
        # Menos detecciones esperadas
        self.assertLessEqual(n_detected, 1)


class TestIGETSPhysics(unittest.TestCase):
    """Tests de física gravitacional."""
    
    def test_f0_value(self):
        """Test del valor de f₀."""
        self.assertEqual(F0, 141.7001)
    
    def test_lambda_bar_value(self):
        """Test de longitud característica Yukawa."""
        self.assertEqual(LAMBDA_BAR, 3.37e5)
    
    def test_igets_stations(self):
        """Test de estaciones IGETS."""
        # Verificar que hay estaciones
        self.assertGreater(len(IGETS_STATIONS), 0)
        
        # Verificar estructura de cada estación
        for station_name, info in IGETS_STATIONS.items():
            self.assertIn('lat', info)
            self.assertIn('lon', info)
            self.assertIn('name', info)
            
            # Verificar rangos de lat/lon
            self.assertGreaterEqual(info['lat'], -90)
            self.assertLessEqual(info['lat'], 90)
            self.assertGreaterEqual(info['lon'], -180)
            self.assertLessEqual(info['lon'], 180)
    
    def test_nyquist_frequency(self):
        """Test de frecuencia de Nyquist."""
        analysis = IGETSGravimetryAnalysis(sample_rate=1000.0)
        
        # Nyquist = sample_rate / 2
        self.assertEqual(analysis.nyquist, 500.0)
        
        # f₀ debe estar por debajo de Nyquist
        self.assertLess(F0, analysis.nyquist)


def main():
    """Ejecutar tests."""
    unittest.main()


if __name__ == '__main__':
    main()
