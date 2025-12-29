#!/usr/bin/env python3
"""
Tests para el análisis de 141.7001 Hz con filtro bandpass [140.5-143.0 Hz]

Este módulo contiene tests unitarios para validar la funcionalidad del script
de análisis bandpass, incluyendo:
- Validación de parámetros de filtro
- Verificación de ventanas temporales
- Validación de análisis de coherencia
- Tests de funciones auxiliares
"""

import unittest
import sys
import os
from datetime import datetime

# Agregar path al módulo si es necesario
sys.path.insert(0, os.path.dirname(__file__))

# Mock numpy if not available for testing constants only
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy no disponible - tests limitados a validación de constantes")

# Mock matplotlib if not available
try:
    import matplotlib
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False
    print("⚠️  Matplotlib no disponible - tests limitados")

# Mock gwpy if not available
try:
    import gwpy
    GWPY_AVAILABLE = True
except ImportError:
    GWPY_AVAILABLE = False
    # Create minimal mock for testing
    sys.modules['gwpy'] = type(sys)('gwpy')
    sys.modules['gwpy.timeseries'] = type(sys)('gwpy.timeseries')
    sys.modules['gwpy.signal'] = type(sys)('gwpy.signal')
    print("⚠️  GWPy no disponible - usando mocks para tests")

# Importar módulo a testear
try:
    import analisis_141hz_bandpass as bandpass
except ImportError:
    print("❌ No se pudo importar el módulo analisis_141hz_bandpass")
    sys.exit(1)


class TestBandpassParameters(unittest.TestCase):
    """Tests para los parámetros del filtro bandpass"""
    
    def test_target_frequency(self):
        """Verificar que la frecuencia objetivo es correcta"""
        self.assertEqual(bandpass.TARGET_FREQUENCY, 141.7001)
    
    def test_frequency_uncertainty(self):
        """Verificar que la incertidumbre de frecuencia es correcta"""
        self.assertEqual(bandpass.FREQUENCY_UNCERTAINTY, 0.0012)
    
    def test_bandpass_range(self):
        """Verificar que el rango del filtro bandpass es correcto"""
        self.assertEqual(bandpass.BANDPASS_LOW, 140.5)
        self.assertEqual(bandpass.BANDPASS_HIGH, 143.0)
        
        # Verificar que el rango incluye la frecuencia objetivo
        self.assertGreater(bandpass.TARGET_FREQUENCY, bandpass.BANDPASS_LOW)
        self.assertLess(bandpass.TARGET_FREQUENCY, bandpass.BANDPASS_HIGH)
    
    def test_merger_window(self):
        """Verificar que la ventana del merger es ±0.3s"""
        self.assertEqual(bandpass.MERGER_WINDOW, 0.3)
    
    def test_min_q_value(self):
        """Verificar que Q > 30"""
        self.assertGreaterEqual(bandpass.MIN_Q_VALUE, 30)
    
    def test_min_detectors(self):
        """Verificar que se requieren al menos 2 detectores"""
        self.assertGreaterEqual(bandpass.MIN_DETECTORS, 2)


class TestEventValidation(unittest.TestCase):
    """Tests para validación de eventos"""
    
    def test_validate_known_event(self):
        """Verificar que eventos conocidos son validados correctamente"""
        gps_time = bandpass.validate_event('GW150914')
        self.assertIsNotNone(gps_time)
        self.assertAlmostEqual(gps_time, 1126259462.423, places=3)
    
    def test_validate_unknown_event(self):
        """Verificar que eventos desconocidos retornan None"""
        gps_time = bandpass.validate_event('GW999999')
        self.assertIsNone(gps_time)
    
    def test_known_events_catalog(self):
        """Verificar que el catálogo contiene eventos conocidos"""
        self.assertIn('GW150914', bandpass.KNOWN_EVENTS)
        self.assertIn('GW151226', bandpass.KNOWN_EVENTS)
        self.assertIn('GW170814', bandpass.KNOWN_EVENTS)


class TestFrequencyAnalysis(unittest.TestCase):
    """Tests para análisis de frecuencia"""
    
    def test_frequency_within_expected_range(self):
        """Verificar detección dentro del rango esperado"""
        # Frecuencia detectada dentro del rango
        detected = 141.7001
        deviation = abs(detected - bandpass.TARGET_FREQUENCY)
        within_expected = deviation <= bandpass.FREQUENCY_UNCERTAINTY
        self.assertTrue(within_expected)
    
    def test_frequency_outside_expected_range(self):
        """Verificar detección fuera del rango esperado"""
        # Frecuencia detectada fuera del rango
        detected = 141.710
        deviation = abs(detected - bandpass.TARGET_FREQUENCY)
        within_expected = deviation <= bandpass.FREQUENCY_UNCERTAINTY
        self.assertFalse(within_expected)
    
    def test_frequency_at_boundary(self):
        """Verificar detección en el límite del rango"""
        # Frecuencia exactamente en el límite superior
        detected = bandpass.TARGET_FREQUENCY + bandpass.FREQUENCY_UNCERTAINTY
        deviation = abs(detected - bandpass.TARGET_FREQUENCY)
        # Use assertAlmostEqual to handle floating point precision
        self.assertAlmostEqual(deviation, bandpass.FREQUENCY_UNCERTAINTY, places=6)


class TestCoherenceAnalysis(unittest.TestCase):
    """Tests para análisis de coherencia"""
    
    @unittest.skipIf(not NUMPY_AVAILABLE, "NumPy no disponible")
    def test_check_coherence_insufficient_detectors(self):
        """Verificar coherencia con detectores insuficientes"""
        results_dict = {
            'H1': {
                'detected_frequency': 141.7001,
                'snr': 3.5
            }
        }
        
        coherence = bandpass.check_coherence(results_dict)
        self.assertFalse(coherence['coherent'])
        self.assertIn('reason', coherence)
    
    @unittest.skipIf(not NUMPY_AVAILABLE, "NumPy no disponible")
    def test_check_coherence_sufficient_detectors_coherent(self):
        """Verificar coherencia con detectores suficientes y coherentes"""
        results_dict = {
            'H1': {
                'detected_frequency': 141.7001,
                'snr': 3.5
            },
            'L1': {
                'detected_frequency': 141.7010,
                'snr': 3.2
            }
        }
        
        coherence = bandpass.check_coherence(results_dict)
        self.assertTrue(coherence['coherent'])
        self.assertEqual(coherence['num_detectors'], 2)
        self.assertLess(coherence['freq_std'], 0.1)
    
    @unittest.skipIf(not NUMPY_AVAILABLE, "NumPy no disponible")
    def test_check_coherence_sufficient_detectors_incoherent(self):
        """Verificar coherencia con detectores suficientes pero incoherentes"""
        results_dict = {
            'H1': {
                'detected_frequency': 141.7001,
                'snr': 1.0
            },
            'L1': {
                'detected_frequency': 142.5000,
                'snr': 1.2
            }
        }
        
        coherence = bandpass.check_coherence(results_dict)
        self.assertFalse(coherence['coherent'])
        self.assertGreaterEqual(coherence['freq_std'], 0.1)


class TestBandpassFilter(unittest.TestCase):
    """Tests para el filtro bandpass"""
    
    def test_bandpass_frequency_range(self):
        """Verificar que el rango de frecuencias del filtro es correcto"""
        # El filtro debe cubrir [140.5-143.0] Hz
        bandwidth = bandpass.BANDPASS_HIGH - bandpass.BANDPASS_LOW
        self.assertEqual(bandwidth, 2.5)
        
        # La frecuencia objetivo debe estar en el centro aproximado
        center = (bandpass.BANDPASS_HIGH + bandpass.BANDPASS_LOW) / 2
        self.assertAlmostEqual(center, 141.75, places=2)
        
        # Verificar margen alrededor de la frecuencia objetivo
        margin_low = bandpass.TARGET_FREQUENCY - bandpass.BANDPASS_LOW
        margin_high = bandpass.BANDPASS_HIGH - bandpass.TARGET_FREQUENCY
        
        self.assertGreater(margin_low, 1.0)  # Al menos 1 Hz de margen
        self.assertGreater(margin_high, 1.0)


class TestMergerWindow(unittest.TestCase):
    """Tests para la ventana temporal del merger"""
    
    def test_merger_window_size(self):
        """Verificar que la ventana temporal es de ±0.3s"""
        self.assertEqual(bandpass.MERGER_WINDOW, 0.3)
        
        # La ventana total es 2 * 0.3 = 0.6s
        total_window = 2 * bandpass.MERGER_WINDOW
        self.assertEqual(total_window, 0.6)
    
    def test_merger_window_samples(self):
        """Verificar el número de muestras en la ventana"""
        # Con sample_rate=4096 Hz y ventana de 0.6s
        sample_rate = 4096
        expected_samples = int(2 * bandpass.MERGER_WINDOW * sample_rate)
        
        # Debe haber aproximadamente 2457 muestras
        self.assertAlmostEqual(expected_samples, 2457, delta=1)


class TestQTransformParameters(unittest.TestCase):
    """Tests para parámetros del Q-transform"""
    
    def test_min_q_value(self):
        """Verificar que Q mínimo es mayor que 30"""
        self.assertGreater(bandpass.MIN_Q_VALUE, 29)
        self.assertEqual(bandpass.MIN_Q_VALUE, 30)
    
    def test_q_range_valid(self):
        """Verificar que el rango de Q es válido para Q-transform"""
        # Un rango típico para Q-transform es (30, 100)
        # Verificar que MIN_Q_VALUE está dentro de un rango razonable
        self.assertGreaterEqual(bandpass.MIN_Q_VALUE, 10)
        self.assertLessEqual(bandpass.MIN_Q_VALUE, 100)


class TestKnownEvents(unittest.TestCase):
    """Tests para el catálogo de eventos conocidos"""
    
    def test_gw150914_gps_time(self):
        """Verificar tiempo GPS de GW150914"""
        self.assertIn('GW150914', bandpass.KNOWN_EVENTS)
        self.assertAlmostEqual(
            bandpass.KNOWN_EVENTS['GW150914'], 
            1126259462.423, 
            places=3
        )
    
    def test_events_in_chronological_order(self):
        """Verificar que los eventos están en orden cronológico (opcional)"""
        events = list(bandpass.KNOWN_EVENTS.keys())
        gps_times = list(bandpass.KNOWN_EVENTS.values())
        
        # Los tiempos GPS deben ser crecientes
        for i in range(len(gps_times) - 1):
            self.assertLess(
                gps_times[i], 
                gps_times[i+1],
                f"{events[i]} debe ser anterior a {events[i+1]}"
            )


class TestConstants(unittest.TestCase):
    """Tests para constantes del módulo"""
    
    def test_all_constants_defined(self):
        """Verificar que todas las constantes están definidas"""
        self.assertTrue(hasattr(bandpass, 'TARGET_FREQUENCY'))
        self.assertTrue(hasattr(bandpass, 'FREQUENCY_UNCERTAINTY'))
        self.assertTrue(hasattr(bandpass, 'BANDPASS_LOW'))
        self.assertTrue(hasattr(bandpass, 'BANDPASS_HIGH'))
        self.assertTrue(hasattr(bandpass, 'MERGER_WINDOW'))
        self.assertTrue(hasattr(bandpass, 'MIN_Q_VALUE'))
        self.assertTrue(hasattr(bandpass, 'MIN_DETECTORS'))
        self.assertTrue(hasattr(bandpass, 'KNOWN_EVENTS'))
    
    def test_constants_positive(self):
        """Verificar que las constantes son positivas"""
        self.assertGreater(bandpass.TARGET_FREQUENCY, 0)
        self.assertGreater(bandpass.FREQUENCY_UNCERTAINTY, 0)
        self.assertGreater(bandpass.BANDPASS_LOW, 0)
        self.assertGreater(bandpass.BANDPASS_HIGH, 0)
        self.assertGreater(bandpass.MERGER_WINDOW, 0)
        self.assertGreater(bandpass.MIN_Q_VALUE, 0)
        self.assertGreater(bandpass.MIN_DETECTORS, 0)


class TestIntegration(unittest.TestCase):
    """Tests de integración para el flujo completo"""
    
    def test_complete_parameter_consistency(self):
        """Verificar consistencia entre todos los parámetros"""
        # Frecuencia objetivo debe estar dentro del bandpass
        self.assertGreater(bandpass.TARGET_FREQUENCY, bandpass.BANDPASS_LOW)
        self.assertLess(bandpass.TARGET_FREQUENCY, bandpass.BANDPASS_HIGH)
        
        # Incertidumbre debe ser mucho menor que el ancho del bandpass
        bandwidth = bandpass.BANDPASS_HIGH - bandpass.BANDPASS_LOW
        self.assertLess(bandpass.FREQUENCY_UNCERTAINTY * 10, bandwidth)
        
        # Ventana del merger debe ser razonable (entre 0.1 y 1.0 segundos)
        self.assertGreater(bandpass.MERGER_WINDOW, 0.1)
        self.assertLess(bandpass.MERGER_WINDOW, 1.0)
        
        # Min Q debe ser un valor estándar para análisis gravitacional
        self.assertGreaterEqual(bandpass.MIN_Q_VALUE, 20)
        self.assertLessEqual(bandpass.MIN_Q_VALUE, 100)


def run_tests():
    """Ejecutar todos los tests"""
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestBandpassParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestEventValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequencyAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestCoherenceAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestBandpassFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestMergerWindow))
    suite.addTests(loader.loadTestsFromTestCase(TestQTransformParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestKnownEvents))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida apropiado
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 TESTS PARA ANÁLISIS 141.7001 Hz CON FILTRO BANDPASS")
    print("=" * 70)
    print()
    
    exit_code = run_tests()
    
    print()
    print("=" * 70)
    if exit_code == 0:
        print("✅ TODOS LOS TESTS PASARON")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
    print("=" * 70)
    
    sys.exit(exit_code)
