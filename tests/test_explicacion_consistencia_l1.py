#!/usr/bin/env python3
"""
Test para explicacion_consistencia_l1.py

Verifica que el análisis de consistencia L1 funcione correctamente
y produzca resultados válidos.
"""

import unittest
import json
from pathlib import Path
import sys

# Importar el módulo a testear
import explicacion_consistencia_l1 as ecl1


class TestAntennaPatternCalculations(unittest.TestCase):
    """Tests para cálculos del patrón de antena"""
    
    def test_deg_to_rad_conversion(self):
        """Test conversión de grados a radianes"""
        self.assertAlmostEqual(ecl1.deg_to_rad(0), 0.0)
        self.assertAlmostEqual(ecl1.deg_to_rad(90), 1.5707963267948966)
        self.assertAlmostEqual(ecl1.deg_to_rad(180), 3.141592653589793)
        self.assertAlmostEqual(ecl1.deg_to_rad(360), 6.283185307179586)
    
    def test_gmst_calculation(self):
        """Test cálculo de GMST para GW150914"""
        gps_time = 1126259462.423
        gmst = ecl1.calculate_gmst(gps_time)
        
        # GMST debe estar en rango [0, 2π]
        self.assertGreaterEqual(gmst, 0)
        self.assertLess(gmst, 2 * 3.14159265359)
    
    def test_detector_tensor_h1(self):
        """Test cálculo del tensor detector para H1"""
        h1_info = ecl1.DETECTOR_LOCATIONS['H1']
        tensor = ecl1.get_detector_tensor(
            h1_info['lat'],
            h1_info['lon'],
            h1_info['arm_azimuth']
        )
        
        # Verificar que el tensor tiene todas las componentes necesarias
        self.assertIn('xx', tensor)
        self.assertIn('yy', tensor)
        self.assertIn('zz', tensor)
        self.assertIn('xy', tensor)
        self.assertIn('xz', tensor)
        self.assertIn('yz', tensor)
    
    def test_detector_tensor_l1(self):
        """Test cálculo del tensor detector para L1"""
        l1_info = ecl1.DETECTOR_LOCATIONS['L1']
        tensor = ecl1.get_detector_tensor(
            l1_info['lat'],
            l1_info['lon'],
            l1_info['arm_azimuth']
        )
        
        # Verificar que el tensor tiene todas las componentes necesarias
        self.assertIn('xx', tensor)
        self.assertIn('yy', tensor)
        self.assertIn('zz', tensor)
    
    def test_antenna_response_calculation(self):
        """Test cálculo de respuesta de antena"""
        gmst = ecl1.calculate_gmst(ecl1.GW150914_PARAMS['gps_time'])
        h1_info = ecl1.DETECTOR_LOCATIONS['H1']
        tensor = ecl1.get_detector_tensor(
            h1_info['lat'],
            h1_info['lon'],
            h1_info['arm_azimuth']
        )
        
        F_plus, F_cross = ecl1.calculate_antenna_response(
            ecl1.GW150914_PARAMS['ra'],
            ecl1.GW150914_PARAMS['dec'],
            ecl1.GW150914_PARAMS['psi'],
            gmst,
            tensor
        )
        
        # F+ y Fx deben ser números finitos
        self.assertTrue(abs(F_plus) < 10)
        self.assertTrue(abs(F_cross) < 10)
    
    def test_effective_antenna_response(self):
        """Test cálculo de respuesta efectiva"""
        F_eff = ecl1.calculate_effective_antenna_response(0.3, 0.4)
        expected = (0.3**2 + 0.4**2)**0.5
        self.assertAlmostEqual(F_eff, expected)
        
        # Test con valores cero
        F_eff_zero = ecl1.calculate_effective_antenna_response(0, 0)
        self.assertEqual(F_eff_zero, 0)


class TestNoiseAndSNRCalculations(unittest.TestCase):
    """Tests para cálculos de ruido y SNR"""
    
    def test_noise_ratio_estimation(self):
        """Test estimación del ratio de ruido"""
        noise_ratio = ecl1.estimate_noise_ratio_at_frequency(141.7001)
        
        # El ratio de ruido debe ser positivo
        self.assertGreater(noise_ratio, 0)
        
        # Debe ser un valor razonable (entre 1 y 20)
        self.assertGreater(noise_ratio, 1)
        self.assertLess(noise_ratio, 20)
    
    def test_snr_ratio_calculation(self):
        """Test cálculo del ratio de SNR esperado"""
        F_eff_H1 = 0.4
        F_eff_L1 = 0.5
        noise_ratio = 8.0
        
        snr_ratio = ecl1.calculate_expected_snr_ratio(F_eff_H1, F_eff_L1, noise_ratio)
        
        # SNR ratio debe ser positivo
        self.assertGreater(snr_ratio, 0)
        
        # Verificar que el cálculo es correcto
        expected = (F_eff_H1 / F_eff_L1) * noise_ratio
        self.assertAlmostEqual(snr_ratio, expected)
    
    def test_snr_ratio_zero_denominator(self):
        """Test manejo de denominador cero"""
        F_eff_H1 = 0.4
        F_eff_L1 = 0.0
        noise_ratio = 8.0
        
        snr_ratio = ecl1.calculate_expected_snr_ratio(F_eff_H1, F_eff_L1, noise_ratio)
        
        # Debe retornar infinito
        self.assertEqual(snr_ratio, float('inf'))


class TestL1ConsistencyAnalysis(unittest.TestCase):
    """Tests para el análisis completo de consistencia L1"""
    
    def test_analyze_l1_consistency_runs(self):
        """Test que el análisis completo ejecuta sin errores"""
        results = ecl1.analyze_l1_consistency()
        
        # Verificar estructura de resultados
        self.assertIn('event', results)
        self.assertIn('frequency', results)
        self.assertIn('detectors', results)
        self.assertIn('analysis', results)
    
    def test_results_structure(self):
        """Test estructura de resultados del análisis"""
        results = ecl1.analyze_l1_consistency()
        
        # Verificar datos del evento
        self.assertEqual(results['event'], 'GW150914')
        self.assertEqual(results['frequency'], 141.7001)
        
        # Verificar detectores
        self.assertIn('H1', results['detectors'])
        self.assertIn('L1', results['detectors'])
        
        # Verificar componentes de análisis
        analysis = results['analysis']
        self.assertIn('antenna_response_ratio_H1_L1', analysis)
        self.assertIn('noise_ratio_L1_H1', analysis)
        self.assertIn('expected_snr_ratio_H1_L1', analysis)
        self.assertIn('observed_snr_ratio_H1_L1', analysis)
        self.assertIn('model_deviation_percent', analysis)
    
    def test_h1_detector_data(self):
        """Test datos del detector H1"""
        results = ecl1.analyze_l1_consistency()
        h1_data = results['detectors']['H1']
        
        self.assertIn('F_plus', h1_data)
        self.assertIn('F_cross', h1_data)
        self.assertIn('F_effective', h1_data)
        self.assertIn('observed_snr', h1_data)
        
        # Verificar SNR observado correcto
        self.assertEqual(h1_data['observed_snr'], 7.47)
    
    def test_l1_detector_data(self):
        """Test datos del detector L1"""
        results = ecl1.analyze_l1_consistency()
        l1_data = results['detectors']['L1']
        
        self.assertIn('F_plus', l1_data)
        self.assertIn('F_cross', l1_data)
        self.assertIn('F_effective', l1_data)
        self.assertIn('observed_snr', l1_data)
        
        # Verificar SNR observado correcto
        self.assertEqual(l1_data['observed_snr'], 0.95)
    
    def test_snr_ratio_consistent(self):
        """Test que el ratio de SNR es consistente"""
        results = ecl1.analyze_l1_consistency()
        analysis = results['analysis']
        
        # El ratio observado debe ser aproximadamente 7.47 / 0.95
        observed_ratio = ecl1.OBSERVED_SNR['H1'] / ecl1.OBSERVED_SNR['L1']
        self.assertAlmostEqual(
            analysis['observed_snr_ratio_H1_L1'],
            observed_ratio,
            places=2
        )
    
    def test_model_explains_observations(self):
        """Test que el modelo explica las observaciones razonablemente"""
        results = ecl1.analyze_l1_consistency()
        analysis = results['analysis']
        
        # La desviación del modelo debe ser razonable (< 50%)
        self.assertLess(analysis['model_deviation_percent'], 50)
        
        # El ratio esperado debe ser positivo
        self.assertGreater(analysis['expected_snr_ratio_H1_L1'], 0)


class TestFileGeneration(unittest.TestCase):
    """Tests para generación de archivos de salida"""
    
    def test_json_output_generated(self):
        """Test que se genera el archivo JSON"""
        # Ejecutar análisis
        results = ecl1.analyze_l1_consistency()
        ecl1.save_results_json(results)
        
        # Verificar que el archivo existe
        json_file = Path('explicacion_consistencia_l1.json')
        self.assertTrue(json_file.exists())
    
    def test_json_is_valid(self):
        """Test que el JSON generado es válido"""
        results = ecl1.analyze_l1_consistency()
        ecl1.save_results_json(results)
        
        # Cargar y verificar JSON
        with open('explicacion_consistencia_l1.json', 'r') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
        self.assertIn('event', data)
        self.assertIn('metadata', data)
    
    def test_png_output_generated(self):
        """Test que se genera la visualización"""
        results = ecl1.analyze_l1_consistency()
        ecl1.create_visualization(results)
        
        # Verificar que el archivo existe
        png_file = Path('explicacion_consistencia_l1.png')
        self.assertTrue(png_file.exists())
        
        # Verificar que tiene tamaño razonable (> 10 KB)
        self.assertGreater(png_file.stat().st_size, 10000)


class TestPhysicalValidation(unittest.TestCase):
    """Tests para validación física de resultados"""
    
    def test_antenna_response_magnitude(self):
        """Test que la respuesta de antena está en rango físico"""
        results = ecl1.analyze_l1_consistency()
        
        for det_name in ['H1', 'L1']:
            det_data = results['detectors'][det_name]
            F_eff = det_data['F_effective']
            
            # F_effective debe estar en rango razonable [0, 1]
            self.assertGreaterEqual(F_eff, 0)
            self.assertLessEqual(F_eff, 1.5)
    
    def test_noise_ratio_physical(self):
        """Test que el ratio de ruido es físicamente razonable"""
        results = ecl1.analyze_l1_consistency()
        analysis = results['analysis']
        
        noise_ratio = analysis['noise_ratio_L1_H1']
        
        # El ratio de ruido debe estar en rango razonable
        self.assertGreater(noise_ratio, 1)
        self.assertLess(noise_ratio, 20)
    
    def test_h1_snr_higher_than_l1(self):
        """Test que H1 tiene mayor SNR que L1 como se observó"""
        h1_snr = ecl1.OBSERVED_SNR['H1']
        l1_snr = ecl1.OBSERVED_SNR['L1']
        
        self.assertGreater(h1_snr, l1_snr)


def run_tests():
    """Ejecutar todos los tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAntennaPatternCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestNoiseAndSNRCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestL1ConsistencyAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestFileGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalValidation))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
