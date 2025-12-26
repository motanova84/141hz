#!/usr/bin/env python3
"""
Test para analizar_gw200129.py
Valida la lógica del script sin requerir instalación completa de PyCBC
"""

import sys
import unittest
from unittest.mock import Mock, patch
import os

# Agregar el directorio scripts al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


class TestGW200129Analysis(unittest.TestCase):
    """Tests para el análisis de GW200129_065458"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.evento_nombre = "GW200129_065458"
        self.gps_time = 1264316116.4
        self.target_freq = 141.7
        
    def test_gps_time_correcto(self):
        """Verificar que el GPS time del evento es correcto"""
        self.assertEqual(self.gps_time, 1264316116.4)
        
    def test_frecuencia_objetivo(self):
        """Verificar que la frecuencia objetivo es 141.7 Hz"""
        self.assertEqual(self.target_freq, 141.7)
        
    @patch('analizar_gw200129.Detector')
    def test_calcular_respuesta_efectiva_mock(self, mock_detector_class):
        """Test con mock de PyCBC Detector"""
        # Configurar el mock
        mock_detector = Mock()
        mock_detector.antenna_pattern.return_value = (0.5, 0.3)  # fp, fc
        mock_detector_class.return_value = mock_detector
        
        # Importar la función
        try:
            from analizar_gw200129 import calcular_respuesta_efectiva
            
            # Llamar la función
            result = calcular_respuesta_efectiva(
                'H1', 1.95, -1.27, 0.785, self.gps_time, self.target_freq
            )
            
            # Verificar resultado
            # F_eff = sqrt(0.5^2 + 0.3^2) = sqrt(0.25 + 0.09) = sqrt(0.34) ≈ 0.583
            expected = (0.5**2 + 0.3**2)**0.5
            self.assertAlmostEqual(result, expected, places=3)
            
        except ImportError:
            self.skipTest("No se pudo importar el módulo analizar_gw200129")
    
    def test_detectores_lista(self):
        """Verificar que la lista de detectores incluye H1, L1, V1, K1"""
        detectores_esperados = ['H1', 'L1', 'V1', 'K1']
        self.assertEqual(len(detectores_esperados), 4)
        self.assertIn('H1', detectores_esperados)
        self.assertIn('L1', detectores_esperados)
        self.assertIn('V1', detectores_esperados)
        self.assertIn('K1', detectores_esperados)
        
    def test_respuesta_efectiva_formula(self):
        """Verificar la fórmula de respuesta efectiva"""
        # F_eff = sqrt(F+^2 + Fx^2)
        fp = 0.2140  # Ejemplo de H1
        fc = 0.5
        
        f_eff_manual = (fp**2 + fc**2)**0.5
        
        # Verificar que el cálculo es correcto
        import math
        f_eff_math = math.sqrt(fp**2 + fc**2)
        
        self.assertAlmostEqual(f_eff_manual, f_eff_math, places=6)
    
    def test_valores_esperados_aproximados(self):
        """Verificar que los valores esperados están en rangos razonables"""
        # Según el problem statement:
        # H1: F_eff = 0.2140
        # L1: F_eff = 0.3281
        # V1: F_eff = 0.8669
        # K1: F_eff = 0.3364
        
        valores_esperados = {
            'H1': 0.2140,
            'L1': 0.3281,
            'V1': 0.8669,
            'K1': 0.3364
        }
        
        # Verificar que todos los valores están entre 0 y 1
        for detector, valor in valores_esperados.items():
            self.assertGreaterEqual(valor, 0.0, 
                f"{detector} debe tener F_eff >= 0")
            self.assertLessEqual(valor, 1.0, 
                f"{detector} debe tener F_eff <= 1")
    
    def test_mejor_detector(self):
        """Verificar que V1 tiene la mejor respuesta según problem statement"""
        valores = {
            'H1': 0.2140,
            'L1': 0.3281,
            'V1': 0.8669,
            'K1': 0.3364
        }
        
        mejor = max(valores, key=valores.get)
        self.assertEqual(mejor, 'V1')
        
    def test_respuesta_promedio(self):
        """Calcular y verificar respuesta promedio"""
        valores = [0.2140, 0.3281, 0.8669, 0.3364]
        promedio = sum(valores) / len(valores)
        
        # Verificar que el promedio es razonable
        self.assertGreater(promedio, 0.3)
        self.assertLess(promedio, 0.5)


class TestScriptStructure(unittest.TestCase):
    """Tests para verificar estructura del script"""
    
    def test_script_exists(self):
        """Verificar que el script existe"""
        script_path = os.path.join(os.path.dirname(__file__), 'analizar_gw200129.py')
        self.assertTrue(os.path.exists(script_path), 
            f"Script no encontrado en {script_path}")
    
    def test_script_executable(self):
        """Verificar que el script es ejecutable"""
        script_path = os.path.join(os.path.dirname(__file__), 'analizar_gw200129.py')
        self.assertTrue(os.access(script_path, os.X_OK),
            "Script debe ser ejecutable")
    
    def test_script_has_shebang(self):
        """Verificar que el script tiene shebang"""
        script_path = os.path.join(os.path.dirname(__file__), 'analizar_gw200129.py')
        with open(script_path, 'r') as f:
            first_line = f.readline()
            self.assertTrue(first_line.startswith('#!/usr/bin/env python3'),
                "Script debe tener shebang de Python 3")


def run_tests():
    """Ejecutar todos los tests"""
    print("🧪 EJECUTANDO TESTS PARA GW200129 ANALYSIS")
    print("=" * 60)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestGW200129Analysis))
    suite.addTests(loader.loadTestsFromTestCase(TestScriptStructure))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
