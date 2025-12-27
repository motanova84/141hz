#!/usr/bin/env python3
"""
Tests para los 3 Pilares del Método Científico

Verifica que los scripts de validación funcionen correctamente:
1. reproducibilidad_garantizada.py
2. falsabilidad_explicita.py
3. evidencia_empirica.py
4. validacion_completa_3_pilares.py
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from reproducibilidad_garantizada import garantizar_reproducibilidad
from falsabilidad_explicita import criterios_falsacion
from evidencia_empirica import resultados_gw150914


class TestReproducibilidad(unittest.TestCase):
    """Tests para reproducibilidad_garantizada.py"""
    
    def test_garantizar_reproducibilidad(self):
        """Test que garantizar_reproducibilidad retorna estructura correcta"""
        resultado = garantizar_reproducibilidad()
        
        # Verificar estructura
        self.assertIn('reproducibilidad', resultado)
        self.assertIn('pasos_verificacion', resultado)
        self.assertIn('componentes_verificables', resultado)
        self.assertIn('estado', resultado)
        
        # Verificar estado
        self.assertEqual(resultado['estado'], 'GARANTIZADO')
        
        # Verificar componentes clave
        self.assertIn('repositorio', resultado['reproducibilidad'])
        self.assertEqual(
            resultado['reproducibilidad']['repositorio'],
            'https://github.com/motanova84/gw250114-141hz-analysis'
        )
        self.assertEqual(
            resultado['reproducibilidad']['comando_validacion'],
            'make validate'
        )
        
    def test_archivo_json_generado(self):
        """Test que se genera el archivo JSON de reproducibilidad"""
        garantizar_reproducibilidad()
        
        output_file = Path('results/validacion_reproducibilidad.json')
        self.assertTrue(output_file.exists())
        
        # Verificar que es JSON válido
        with open(output_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)


class TestFalsabilidad(unittest.TestCase):
    """Tests para falsabilidad_explicita.py"""
    
    def test_criterios_falsacion(self):
        """Test que criterios_falsacion retorna estructura correcta"""
        resultado = criterios_falsacion()
        
        # Verificar estructura
        self.assertIn('falsabilidad', resultado)
        self.assertIn('criterios', resultado)
        self.assertIn('principio', resultado)
        
        # Verificar estado
        self.assertEqual(resultado['falsabilidad'], 'EXPLÍCITA')
        
        # Verificar que existen los 4 criterios
        criterios = resultado['criterios']
        self.assertIn('gravitacional', criterios)
        self.assertIn('topologico', criterios)
        self.assertIn('cosmologico', criterios)
        self.assertIn('neurociencia', criterios)
        
        # Verificar estructura de cada criterio
        for nombre, criterio in criterios.items():
            self.assertIn('criterio', criterio)
            self.assertIn('descripcion', criterio)
            self.assertIn('metodo_verificacion', criterio)
            self.assertIn('umbral_falsacion', criterio)
            self.assertIn('estado', criterio)
    
    def test_criterios_especificos(self):
        """Test valores específicos de criterios"""
        resultado = criterios_falsacion()
        criterios = resultado['criterios']
        
        # Verificar criterio gravitacional
        self.assertEqual(
            criterios['gravitacional']['criterio'],
            'Ausencia en GWTC-3+'
        )
        
        # Verificar criterio topológico
        self.assertEqual(
            criterios['topologico']['criterio'],
            'No detección en Bi₂Se₃ @ 4K'
        )
    
    def test_archivo_json_generado(self):
        """Test que se genera el archivo JSON de falsabilidad"""
        criterios_falsacion()
        
        output_file = Path('results/criterios_falsacion.json')
        self.assertTrue(output_file.exists())
        
        with open(output_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)


class TestEvidenciaEmpirica(unittest.TestCase):
    """Tests para evidencia_empirica.py"""
    
    def test_resultados_gw150914(self):
        """Test que resultados_gw150914 retorna estructura correcta"""
        resultado = resultados_gw150914()
        
        # Verificar estructura principal
        self.assertIn('evento', resultado)
        self.assertIn('detectores', resultado)
        self.assertIn('estado_validacion', resultado)
        
        # Verificar evento
        self.assertEqual(resultado['evento'], 'GW150914')
        self.assertEqual(resultado['estado_validacion'], 'CONFIRMADO')
        
        # Verificar detectores
        detectores = resultado['detectores']
        self.assertIn('H1', detectores)
        self.assertIn('L1', detectores)
    
    def test_valores_h1(self):
        """Test valores específicos del detector H1"""
        resultado = resultados_gw150914()
        h1 = resultado['detectores']['H1']
        
        # Verificar frecuencia
        self.assertEqual(h1['frecuencia'], 141.69)
        
        # Verificar SNR
        self.assertEqual(h1['SNR'], 7.47)
        
        # Verificar p-value
        self.assertEqual(h1['p_value'], '< 0.001')
    
    def test_valores_l1(self):
        """Test valores específicos del detector L1"""
        resultado = resultados_gw150914()
        l1 = resultado['detectores']['L1']
        
        # Verificar frecuencia
        self.assertEqual(l1['frecuencia'], 141.75)
        
        # Verificar SNR
        self.assertEqual(l1['SNR'], 0.95)
        
        # Verificar coincidencia
        self.assertTrue(l1['coincidencia'])
    
    def test_estadistica_combinada(self):
        """Test estadística combinada"""
        resultado = resultados_gw150914()
        
        self.assertIn('estadistica_combinada', resultado)
        stats = resultado['estadistica_combinada']
        
        # Verificar frecuencia promedio
        self.assertAlmostEqual(stats['frecuencia_promedio'], 141.72, places=2)
        
        # Verificar que está cerca del objetivo teórico
        self.assertLess(stats['diferencia_relativa_porcentaje'], 0.1)
    
    def test_archivo_json_generado(self):
        """Test que se genera el archivo JSON de evidencia empírica"""
        resultados_gw150914()
        
        output_file = Path('results/evidencia_empirica_gw150914.json')
        self.assertTrue(output_file.exists())
        
        with open(output_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)


class TestValidacionCompleta(unittest.TestCase):
    """Tests para la validación completa de 3 pilares"""
    
    def test_archivo_consolidado(self):
        """Test que se genera el archivo consolidado de validación completa"""
        # Ejecutar los tres pilares
        garantizar_reproducibilidad()
        criterios_falsacion()
        resultados_gw150914()
        
        # Verificar que se generaron todos los archivos
        self.assertTrue(Path('results/validacion_reproducibilidad.json').exists())
        self.assertTrue(Path('results/criterios_falsacion.json').exists())
        self.assertTrue(Path('results/evidencia_empirica_gw150914.json').exists())


def run_tests():
    """Ejecutar todos los tests"""
    # Crear directorio de resultados si no existe
    Path('results').mkdir(exist_ok=True)
    
    # Ejecutar tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestReproducibilidad))
    suite.addTests(loader.loadTestsFromTestCase(TestFalsabilidad))
    suite.addTests(loader.loadTestsFromTestCase(TestEvidenciaEmpirica))
    suite.addTests(loader.loadTestsFromTestCase(TestValidacionCompleta))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
