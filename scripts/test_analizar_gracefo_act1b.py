#!/usr/bin/env python3
"""
Test suite para el análisis GRACE-FO ACT1B

Valida las funciones de lectura, filtrado y análisis espectral
usando datos sintéticos.
"""

import numpy as np
import os
import sys
import tempfile
import unittest

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Import the analysis module
import analizar_gracefo_act1b as gracefo

class TestACT1BReader(unittest.TestCase):
    """Tests para la lectura de archivos ACT1B."""
    
    def setUp(self):
        """Crear archivo ACT1B sintético para pruebas."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "ACT1B_2024-001_C_04.dat")
        
        # Crear archivo de prueba con cabecera YAML y datos
        with open(self.test_file, 'w') as f:
            f.write("# YAML header\n")
            f.write("product_name: ACT1B\n")
            f.write("satellite: GRACE-C\n")
            f.write("release: RL04\n")
            f.write("# End of YAML header\n")
            f.write("# Data columns: gps_time GRACEFO_id lin_accl_x lin_accl_y lin_accl_z ")
            f.write("ang_accl_x ang_accl_y ang_accl_z acl_x_res acl_y_res acl_z_res qualflg\n")
            
            # Escribir algunas líneas de datos sintéticos
            gps_time = 1000000000.0
            for i in range(100):
                f.write(f"{gps_time + i:.6f} C ")
                f.write(f"{1e-8*np.sin(2*np.pi*0.1417001*i):.12e} ")  # lin_accl_x con señal QCAL
                f.write(f"{1e-9:.12e} {1e-9:.12e} ")  # lin_accl_y, z
                f.write(f"{0:.12e} {0:.12e} {0:.12e} ")  # ang_accl_x, y, z
                f.write(f"{1e-10:.12e} {1e-10:.12e} {1e-10:.12e} ")  # residuos
                f.write("0\n")  # qualflg
    
    def tearDown(self):
        """Limpiar archivos temporales."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_read_act1b_file(self):
        """Test lectura de archivo ACT1B."""
        data = gracefo.read_act1b_file(self.test_file)
        
        # Verificar que se leyeron los datos
        self.assertIsNotNone(data)
        self.assertIn('gps_time', data)
        self.assertIn('lin_accl_x', data)
        self.assertIn('header', data)
        
        # Verificar número de muestras
        self.assertEqual(len(data['gps_time']), 100)
        
        # Verificar que los datos son arrays numpy
        self.assertIsInstance(data['gps_time'], np.ndarray)
        self.assertIsInstance(data['lin_accl_x'], np.ndarray)
        
        # Verificar cabecera YAML
        self.assertIsInstance(data['header'], dict)
        self.assertEqual(data['header']['product_name'], 'ACT1B')
        self.assertEqual(data['header']['satellite'], 'GRACE-C')
    
    def test_quality_filter(self):
        """Test filtrado de calidad."""
        # Crear datos de prueba
        data = {
            'gps_time': np.arange(10),
            'lin_accl_x': np.random.randn(10) * 1e-8,
            'lin_accl_y': np.random.randn(10) * 1e-8,
            'lin_accl_z': np.random.randn(10) * 1e-8,
            'acl_x_res': np.random.randn(10) * 1e-10,
            'acl_y_res': np.random.randn(10) * 1e-10,
            'acl_z_res': np.random.randn(10) * 1e-10,
            'qualflg': np.zeros(10, dtype=int),
            'header': {}
        }
        
        # Marcar algunos datos como malos (bit 2 activado)
        data['qualflg'][5] = 0x04
        
        # Aplicar filtro
        filtered = gracefo.quality_filter(data)
        
        # Verificar que se filtraron los datos malos
        self.assertEqual(len(filtered['gps_time']), 9)
        self.assertNotIn(data['gps_time'][5], filtered['gps_time'])


class TestSpectralAnalysis(unittest.TestCase):
    """Tests para el análisis espectral."""
    
    def test_spectral_analysis(self):
        """Test análisis FFT."""
        # Crear señal sintética con componente a 141.7001 mHz
        sampling_rate = 1.0  # Hz
        duration = 24 * 3600  # 24 horas
        t = np.arange(0, duration, 1/sampling_rate)
        
        f_signal = 0.1417001  # Hz
        amplitude = 1e-8
        noise_level = 1e-9
        
        signal = amplitude * np.sin(2 * np.pi * f_signal * t)
        noise = noise_level * np.random.randn(len(t))
        acceleration = signal + noise
        
        # Realizar análisis espectral
        freqs, psd = gracefo.spectral_analysis(acceleration, sampling_rate, window_hours=24)
        
        # Verificar salidas
        self.assertIsInstance(freqs, np.ndarray)
        self.assertIsInstance(psd, np.ndarray)
        self.assertEqual(len(freqs), len(psd))
        
        # Verificar que las frecuencias son positivas
        self.assertTrue(np.all(freqs >= 0))
        
        # Verificar que hay un pico cerca de la frecuencia de señal
        idx_peak = np.argmax(psd)
        f_peak = freqs[idx_peak]
        self.assertAlmostEqual(f_peak, f_signal, delta=0.001)
    
    def test_detect_qcal_peak(self):
        """Test detección de pico QCAL."""
        # Crear espectro sintético con pico en QCAL
        freqs = np.linspace(0, 0.5, 10000)
        
        # Ruido de fondo
        psd = np.ones_like(freqs) * 1e-16
        
        # Agregar pico en QCAL
        f_target = 0.1417001
        idx_target = np.argmin(np.abs(freqs - f_target))
        psd[idx_target] = 1e-14  # Pico 100x sobre ruido
        
        # Detectar pico
        result = gracefo.detect_qcal_peak(freqs, psd, f_target)
        
        # Verificar resultado
        self.assertIsNotNone(result)
        self.assertIn('f_peak', result)
        self.assertIn('snr_db', result)
        self.assertIn('sigma', result)
        self.assertIn('detected', result)
        
        # Verificar que la frecuencia detectada es correcta
        self.assertAlmostEqual(result['f_peak'], f_target, delta=0.001)
        
        # Verificar que SNR es positivo y alto
        self.assertGreater(result['snr_db'], 10)
        
        # Verificar detección
        self.assertTrue(result['detected'])


class TestIntegration(unittest.TestCase):
    """Tests de integración."""
    
    def test_no_data_directory(self):
        """Test comportamiento cuando no hay archivos."""
        temp_dir = tempfile.mkdtemp()
        
        # Intentar ejecutar análisis sin archivos
        result = gracefo.main(data_dir=temp_dir, output_dir=temp_dir)
        
        # Debería retornar None
        self.assertIsNone(result)
        
        # Limpiar
        import shutil
        shutil.rmtree(temp_dir)


def run_tests():
    """Ejecutar todos los tests."""
    print("="*70)
    print("GRACE-FO ACT1B - TEST SUITE")
    print("="*70)
    print()
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestACT1BReader))
    suite.addTests(loader.loadTestsFromTestCase(TestSpectralAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print()
    print("="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
