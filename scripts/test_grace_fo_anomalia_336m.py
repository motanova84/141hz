#!/usr/bin/env python3
"""
Test Suite para GRACE-FO Satellite Analysis

Valida el script grace_fo_anomalia_336m.py con datos sintéticos.
"""

import sys
import unittest
import numpy as np
import h5py
import tempfile
import os
from pathlib import Path

# Añadir directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar módulo a testear (usando importación dinámica)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "grace_fo_anomalia_336m",
    Path(__file__).parent / "grace_fo_anomalia_336m.py"
)
grace_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grace_module)

GRACEFOAnalyzer = grace_module.GRACEFOAnalyzer
F0_LEO = grace_module.F0_LEO
LAMBDA_DECOH = grace_module.LAMBDA_DECOH
ALPHA_YUKAWA = grace_module.ALPHA_YUKAWA


class TestGRACEFOAnalyzer(unittest.TestCase):
    """Tests para GRACEFOAnalyzer."""
    
    def setUp(self):
        """Crear archivo HDF5 sintético para tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_grace_fo.h5')
        
        # Generar datos sintéticos con señal @ 0.1417001 Hz
        n_samples = 100000
        fs = 1.0  # Hz
        duration = n_samples / fs
        time = np.arange(n_samples) / fs
        
        # Señal base: modulación Yukawa @ f0_LEO
        signal = ALPHA_YUKAWA * np.cos(2 * np.pi * F0_LEO * time)
        
        # Ruido blanco
        noise = np.random.normal(0, 1e-9, n_samples)
        
        # Aceleración total
        accel = signal + noise
        
        # Guardar en HDF5
        with h5py.File(self.test_file, 'w') as f:
            f.create_dataset('accelerometer_x', data=accel)
            f.create_dataset('accelerometer_y', data=accel * 0.5)
            f.create_dataset('accelerometer_z', data=accel * 0.3)
            f.create_dataset('time', data=time)
            
    def tearDown(self):
        """Limpiar archivos temporales."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
        
    def test_cargar_datos(self):
        """Test: Cargar datos HDF5."""
        analyzer = GRACEFOAnalyzer(self.test_file, verbose=False)
        resultado = analyzer.cargar_datos()
        
        self.assertTrue(resultado)
        self.assertIsNotNone(analyzer.accel_x)
        self.assertIsNotNone(analyzer.time)
        self.assertGreater(analyzer.fs, 0)
        
    def test_filtro_bandpass(self):
        """Test: Aplicar filtro pasa-banda."""
        analyzer = GRACEFOAnalyzer(self.test_file, verbose=False)
        analyzer.cargar_datos()
        
        filtered = analyzer.aplicar_filtro_bandpass(analyzer.accel_x)
        
        self.assertEqual(len(filtered), len(analyzer.accel_x))
        self.assertLess(np.std(filtered), np.std(analyzer.accel_x))
        
    def test_calcular_psd(self):
        """Test: Calcular PSD."""
        analyzer = GRACEFOAnalyzer(self.test_file, verbose=False)
        analyzer.cargar_datos()
        
        frequencies, psd = analyzer.calcular_psd(analyzer.accel_x)
        
        self.assertGreater(len(frequencies), 0)
        self.assertEqual(len(frequencies), len(psd))
        self.assertTrue(np.all(psd >= 0))
        
    def test_analizar_pico_aureo(self):
        """Test: Analizar pico @ 0.1417001 Hz."""
        analyzer = GRACEFOAnalyzer(self.test_file, verbose=False)
        analyzer.cargar_datos()
        
        resultados = analyzer.analizar_pico_aureo()
        
        self.assertIn('freq_teorica', resultados)
        self.assertIn('freq_observada', resultados)
        self.assertIn('snr_db', resultados)
        self.assertIn('significancia_sigma', resultados)
        
        # Verificar que detecta pico cerca de F0_LEO
        self.assertAlmostEqual(resultados['freq_teorica'], F0_LEO, places=6)
        self.assertLess(resultados['delta_freq'], 0.01)  # < 10 mHz error
        
    def test_deteccion_confirmada(self):
        """Test: Detección confirmada con señal fuerte."""
        # Crear señal muy fuerte
        n_samples = 100000
        fs = 1.0
        time = np.arange(n_samples) / fs
        
        # Señal fuerte: 10x amplitud Yukawa
        signal_strong = 10 * ALPHA_YUKAWA * np.cos(2 * np.pi * F0_LEO * time)
        noise = np.random.normal(0, 1e-10, n_samples)
        accel_strong = signal_strong + noise
        
        # Guardar
        strong_file = os.path.join(self.temp_dir, 'test_strong.h5')
        with h5py.File(strong_file, 'w') as f:
            f.create_dataset('accelerometer_x', data=accel_strong)
            f.create_dataset('time', data=time)
            
        # Analizar
        analyzer = GRACEFOAnalyzer(strong_file, verbose=False)
        analyzer.cargar_datos()
        resultados = analyzer.analizar_pico_aureo()
        
        # Debe detectar
        self.assertTrue(resultados['deteccion_confirmada'])
        self.assertGreater(resultados['significancia_sigma'], 5.0)
        
        os.remove(strong_file)
        
    def test_no_deteccion_ruido(self):
        """Test: No detección con solo ruido."""
        # Crear solo ruido
        n_samples = 50000
        fs = 1.0
        time = np.arange(n_samples) / fs
        noise_only = np.random.normal(0, 1e-8, n_samples)
        
        # Guardar
        noise_file = os.path.join(self.temp_dir, 'test_noise.h5')
        with h5py.File(noise_file, 'w') as f:
            f.create_dataset('accelerometer_x', data=noise_only)
            f.create_dataset('time', data=time)
            
        # Analizar
        analyzer = GRACEFOAnalyzer(noise_file, verbose=False)
        analyzer.cargar_datos()
        resultados = analyzer.analizar_pico_aureo()
        
        # No debe detectar
        self.assertFalse(resultados['deteccion_confirmada'])
        
        os.remove(noise_file)


class TestConstantesGRACEFO(unittest.TestCase):
    """Tests para constantes físicas."""
    
    def test_frecuencia_leo(self):
        """Test: F0_LEO = F0 / 1000."""
        self.assertAlmostEqual(F0_LEO, 141.7001 / 1000, places=7)
        
    def test_lambda_decoh(self):
        """Test: λ = 336.7 m."""
        self.assertAlmostEqual(LAMBDA_DECOH, 336.7, places=1)
        
    def test_alpha_yukawa(self):
        """Test: α ≈ 0.053 (5.3%)."""
        self.assertAlmostEqual(ALPHA_YUKAWA, 0.05312, places=4)
        self.assertGreater(ALPHA_YUKAWA, 0.05)
        self.assertLess(ALPHA_YUKAWA, 0.06)


def run_tests():
    """Ejecutar todos los tests."""
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
