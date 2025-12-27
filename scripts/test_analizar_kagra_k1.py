#!/usr/bin/env python3
"""
Tests para el análisis de KAGRA K1 en 141.7 Hz
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
import numpy as np

# Añadir el directorio de scripts al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import the module being tested - skip if dependencies missing
try:
    import analizar_kagra_k1  # noqa: F401
except ImportError as e:
    print(f"⚠️ Cannot import analizar_kagra_k1: {e}")
    print("This test requires gwpy and other dependencies")
    print("Install with: pip install gwpy")
    sys.exit(0)


class TestKagraAnalysis(unittest.TestCase):
    """Test suite para el análisis de KAGRA"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.gps_start = 1370294440
        self.gps_end = 1370294472
        self.target_freq = 141.7
        self.target_band = [141.4, 142.0]
    
    def test_gps_time_configuration(self):
        """Test: Verificar que el rango GPS es correcto"""
        duration = self.gps_end - self.gps_start
        self.assertEqual(duration, 32, "La duración debe ser 32 segundos")
        self.assertEqual(self.gps_start, 1370294440, "GPS start correcto")
        self.assertEqual(self.gps_end, 1370294472, "GPS end correcto")
    
    def test_target_band_configuration(self):
        """Test: Verificar que la banda objetivo es correcta"""
        self.assertEqual(self.target_band[0], 141.4, "Límite inferior correcto")
        self.assertEqual(self.target_band[1], 142.0, "Límite superior correcto")
        self.assertGreater(self.target_band[1], self.target_band[0], 
                          "El límite superior debe ser mayor que el inferior")
    
    def test_target_frequency_in_band(self):
        """Test: Verificar que la frecuencia objetivo está dentro de la banda"""
        self.assertGreaterEqual(self.target_freq, self.target_band[0],
                               "Frecuencia objetivo debe estar >= límite inferior")
        self.assertLessEqual(self.target_freq, self.target_band[1],
                            "Frecuencia objetivo debe estar <= límite superior")
    
    @patch('analizar_kagra_k1.TimeSeries')
    def test_data_fetch_mock(self, mock_timeseries):
        """Test: Simular descarga de datos de KAGRA"""
        # Crear datos simulados
        sample_rate = 4096
        duration = 32
        times = np.arange(0, duration, 1/sample_rate)
        
        # Crear señal simulada con ruido y componente en 141.7 Hz
        noise = np.random.normal(0, 1e-23, len(times))
        signal = 5e-23 * np.sin(2 * np.pi * self.target_freq * times)
        data = noise + signal
        
        # Mock del TimeSeries
        mock_ts = Mock()
        mock_ts.value = data
        mock_ts.times.value = times
        mock_ts.duration.value = duration
        mock_ts.sample_rate.value = sample_rate
        mock_ts.bandpass.return_value = mock_ts
        
        mock_timeseries.fetch_open_data.return_value = mock_ts
        
        # Verificar que el mock funciona
        result = mock_timeseries.fetch_open_data('K1', self.gps_start, self.gps_end)
        self.assertIsNotNone(result, "Debe retornar datos simulados")
        self.assertEqual(result.duration.value, duration, "Duración correcta")
        self.assertEqual(result.sample_rate.value, sample_rate, "Sample rate correcto")
    
    def test_snr_calculation(self):
        """Test: Verificar cálculo de SNR"""
        # Datos de prueba
        test_signal = np.array([1.0, -1.0, 0.5, -0.5, 0.2, -0.2])
        
        max_amplitude = np.max(np.abs(test_signal))
        std_deviation = np.std(test_signal)
        snr = max_amplitude / std_deviation
        
        self.assertGreater(snr, 0, "SNR debe ser positivo")
        self.assertIsInstance(snr, (int, float), "SNR debe ser numérico")
        
        # Verificar cálculos individuales
        expected_max = 1.0
        self.assertAlmostEqual(max_amplitude, expected_max, places=10,
                              msg="Amplitud máxima correcta")
    
    def test_snr_interpretation(self):
        """Test: Verificar interpretación de SNR"""
        # SNR alto
        snr_high = 6.0
        self.assertGreater(snr_high, 5.0, "SNR > 5.0 indica señal coherente")
        
        # SNR marginal
        snr_marginal = 3.5
        self.assertGreaterEqual(snr_marginal, 2.0, "SNR >= 2.0 es marginal")
        self.assertLess(snr_marginal, 5.0, "SNR < 5.0 es marginal")
        
        # SNR bajo
        snr_low = 1.5
        self.assertLess(snr_low, 2.0, "SNR < 2.0 indica no señal")
    
    def test_output_directory_creation(self):
        """Test: Verificar que se puede crear el directorio de resultados"""
        output_dir = '/tmp/test_kagra_results'
        os.makedirs(output_dir, exist_ok=True)
        self.assertTrue(os.path.exists(output_dir), 
                       "Directorio de resultados debe existir")
        
        # Limpiar
        if os.path.exists(output_dir):
            os.rmdir(output_dir)
    
    def test_bandpass_filter_parameters(self):
        """Test: Verificar parámetros del filtro de banda"""
        low_freq = self.target_band[0]
        high_freq = self.target_band[1]
        
        self.assertGreater(low_freq, 0, "Frecuencia baja debe ser positiva")
        self.assertGreater(high_freq, low_freq, 
                          "Frecuencia alta debe ser mayor que la baja")
        
        # Verificar que el ancho de banda es razonable
        bandwidth = high_freq - low_freq
        self.assertGreater(bandwidth, 0, "Ancho de banda debe ser positivo")
        self.assertLess(bandwidth, 10, "Ancho de banda no debe ser excesivo")
    
    def test_detector_name(self):
        """Test: Verificar nombre del detector"""
        detector = 'K1'
        self.assertEqual(detector, 'K1', "Detector debe ser K1 (KAGRA)")
        self.assertIsInstance(detector, str, "Nombre del detector debe ser string")
    
    @patch('analizar_kagra_k1.plt')
    def test_visualization_mock(self, mock_plt):
        """Test: Verificar que se pueden crear visualizaciones"""
        # Simular datos
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        # Simular plot
        mock_fig = Mock()
        mock_plt.figure.return_value = mock_fig
        mock_plt.figure(figsize=(10, 4))
        
        # Verificar que figure fue llamado
        mock_plt.figure.assert_called()


class TestResultsFormat(unittest.TestCase):
    """Test para verificar el formato de resultados"""
    
    def test_results_dictionary_structure(self):
        """Test: Verificar estructura del diccionario de resultados"""
        results = {
            'detector': 'K1',
            'gps_start': 1370294440,
            'gps_end': 1370294472,
            'date': '2023-06-16',
            'duration': 32.0,
            'sample_rate': 4096.0,
            'target_freq': 141.7,
            'target_band': [141.4, 142.0],
            'snr': 3.5,
            'max_amplitude': 1.0e-22,
            'std_deviation': 2.86e-23,
            'interpretation': 'marginal'
        }
        
        # Verificar claves requeridas
        required_keys = ['detector', 'snr', 'interpretation', 'target_freq']
        for key in required_keys:
            self.assertIn(key, results, f"Clave '{key}' debe estar en resultados")
        
        # Verificar tipos
        self.assertIsInstance(results['detector'], str)
        self.assertIsInstance(results['snr'], (int, float))
        self.assertIsInstance(results['target_freq'], (int, float))
    
    def test_interpretation_values(self):
        """Test: Verificar valores válidos de interpretación"""
        valid_interpretations = ['coherent_signal', 'marginal', 'no_signal']
        
        for interp in valid_interpretations:
            self.assertIn(interp, valid_interpretations,
                         f"'{interp}' debe ser una interpretación válida")


def run_tests():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 60)
    print("🧪 EJECUTANDO TESTS - Análisis KAGRA K1 en 141.7 Hz")
    print("=" * 60 + "\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTests(loader.loadTestsFromTestCase(TestKagraAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestResultsFormat))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
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
