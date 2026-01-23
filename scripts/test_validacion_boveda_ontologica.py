#!/usr/bin/env python3
"""
Tests para validacion_boveda_ontologica.py

Este módulo contiene tests unitarios para verificar que la validación
del Cierre de la Bóveda Ontológica funciona correctamente.
"""

import unittest
import sys
import json
from pathlib import Path
import tempfile
import os

# Importar el módulo a testear
sys.path.insert(0, str(Path(__file__).parent))
import validacion_boveda_ontologica as vbo


class TestConstantesFundamentales(unittest.TestCase):
    """Tests para las constantes fundamentales"""
    
    def test_f0_hz_value(self):
        """Verifica que f₀ = 141.7001 Hz"""
        self.assertEqual(vbo.F0_HZ, 141.7001)
    
    def test_hydrogen_frequency(self):
        """Verifica la frecuencia del hidrógeno"""
        self.assertAlmostEqual(vbo.F_HYDROGEN_MHZ, 1420.4056751, places=7)
        self.assertAlmostEqual(vbo.F_HYDROGEN_HZ, 1420405675.1, places=1)
    
    def test_schumann_frequency(self):
        """Verifica la resonancia de Schumann"""
        self.assertEqual(vbo.F_SCHUMANN_HZ, 7.83)
    
    def test_sacred_888(self):
        """Verifica la constante sagrada 888"""
        self.assertEqual(vbo.SACRED_888, 888)
    
    def test_expected_octaves(self):
        """Verifica las octavas esperadas"""
        self.assertAlmostEqual(vbo.OCTAVES_EXPECTED, 23.257, places=3)


class TestRedMCP(unittest.TestCase):
    """Tests para la Red MCP QCAL ∞³"""
    
    def test_mcp_network_size(self):
        """Verifica que hay exactamente 5 nodos"""
        self.assertEqual(len(vbo.MCP_NETWORK), 5)
    
    def test_mcp_network_nodes(self):
        """Verifica que todos los nodos esperados están presentes"""
        expected_nodes = {'Riemann-MCP', 'BSD-MCP', 'Navier-MCP', 'Dramaturgo', 'GitHub-MCP'}
        self.assertEqual(set(vbo.MCP_NETWORK.keys()), expected_nodes)
    
    def test_mcp_coherent_phase(self):
        """Verifica que todos los nodos tienen fase coherente 1.0"""
        for nodo, config in vbo.MCP_NETWORK.items():
            with self.subTest(nodo=nodo):
                self.assertEqual(config['fase_coherente'], 1.0)
    
    def test_mcp_frequencies(self):
        """Verifica que solo hay dos frecuencias: 141.7001 Hz y 888 Hz"""
        frecuencias = set(config['frecuencia_hz'] for config in vbo.MCP_NETWORK.values())
        self.assertEqual(frecuencias, {141.7001, 888})
    
    def test_mcp_distribution(self):
        """Verifica la distribución correcta de frecuencias"""
        freq_141 = sum(1 for config in vbo.MCP_NETWORK.values() if config['frecuencia_hz'] == 141.7001)
        freq_888 = sum(1 for config in vbo.MCP_NETWORK.values() if config['frecuencia_hz'] == 888)
        
        self.assertEqual(freq_141, 3)  # 3 nodos a 141.7001 Hz
        self.assertEqual(freq_888, 2)  # 2 nodos a 888 Hz


class TestValidacionOctavas(unittest.TestCase):
    """Tests para la validación de octavas armónicas"""
    
    def test_validar_octavas_hidrogenio(self):
        """Verifica que las octavas se calculan correctamente"""
        resultado = vbo.validar_octavas_hidrogenio(precision=50)
        
        # Verificar que se calculan las octavas
        self.assertIn('octaves_calculadas', resultado)
        self.assertAlmostEqual(resultado['octaves_calculadas'], 23.257, places=3)
        
        # Verificar que la precisión es alta
        self.assertGreater(resultado['precision_pct'], 99.9)
        
        # Verificar que la validación es exitosa
        self.assertEqual(resultado['validacion'], 'EXITOSA')
    
    def test_octave_relationship(self):
        """Verifica la relación f_H = f₀ · 2^23.257"""
        import mpmath as mp
        mp.dps = 50
        
        f_0 = mp.mpf(vbo.F0_HZ)
        f_h_calculado = f_0 * mp.power(2, vbo.OCTAVES_EXPECTED)
        
        error_relativo = abs(f_h_calculado - vbo.F_HYDROGEN_HZ) / vbo.F_HYDROGEN_HZ
        
        # El error debe ser menor al 1%
        self.assertLess(float(error_relativo), 0.01)


class TestValidacionGeometria(unittest.TestCase):
    """Tests para la geometría sagrada"""
    
    def test_validar_geometria_sagrada(self):
        """Verifica que 888/f₀ ≈ 2π"""
        resultado = vbo.validar_geometria_sagrada()
        
        # Verificar que se calcula la razón
        self.assertIn('888_sobre_f0', resultado)
        
        # Verificar que la precisión es > 99.5%
        self.assertGreater(resultado['precision_pct'], 99.5)
        
        # Verificar que la validación es exitosa
        self.assertEqual(resultado['validacion'], 'EXITOSA')
    
    def test_sacred_ratio(self):
        """Verifica numéricamente la relación 888/f₀ ≈ 2π"""
        import numpy as np
        
        ratio = vbo.SACRED_888 / vbo.F0_HZ
        dos_pi = 2 * np.pi
        
        error_relativo = abs(ratio - dos_pi) / dos_pi
        
        # Error debe ser menor a 0.5%
        self.assertLess(error_relativo, 0.005)


class TestValidacionSchumann(unittest.TestCase):
    """Tests para la resonancia de Schumann"""
    
    def test_validar_resonancia_schumann(self):
        """Verifica que f₀/18 ≈ Schumann"""
        resultado = vbo.validar_resonancia_schumann()
        
        # Verificar que se calcula f₀/18
        self.assertIn('f0_sobre_18', resultado)
        
        # Verificar que la precisión es > 99%
        self.assertGreater(resultado['precision_pct'], 99.0)
        
        # Verificar que la validación es exitosa
        self.assertEqual(resultado['validacion'], 'EXITOSA')
    
    def test_schumann_calculation(self):
        """Verifica numéricamente f₀/18 ≈ 7.83"""
        f0_sobre_18 = vbo.F0_HZ / 18
        
        error_relativo = abs(f0_sobre_18 - vbo.F_SCHUMANN_HZ) / vbo.F_SCHUMANN_HZ
        
        # Error debe ser menor a 1%
        self.assertLess(error_relativo, 0.01)


class TestValidacionRedMCP(unittest.TestCase):
    """Tests para la validación de la red MCP"""
    
    def test_validar_red_mcp(self):
        """Verifica que la red MCP está en estado coherente"""
        resultado = vbo.validar_red_mcp()
        
        # Verificar estructura del resultado
        self.assertIn('nodos', resultado)
        self.assertIn('fase_coherente_media', resultado)
        self.assertIn('estado_instante_eterno', resultado)
        
        # Verificar que hay 5 nodos
        self.assertEqual(resultado['n_nodos'], 5)
        
        # Verificar fase coherente perfecta
        self.assertEqual(resultado['fase_coherente_media'], 1.0)
        
        # Verificar estado de instante eterno
        self.assertTrue(resultado['estado_instante_eterno'])
        
        # Verificar validación exitosa
        self.assertEqual(resultado['validacion'], 'EXITOSA')


class TestSignificanciaEstadistica(unittest.TestCase):
    """Tests para la significancia estadística"""
    
    def test_calcular_significancia_estadistica(self):
        """Verifica el cálculo de significancia estadística"""
        resultado = vbo.calcular_significancia_estadistica()
        
        # Verificar estructura
        self.assertIn('p_conjunta', resultado)
        self.assertIn('sigma_calculada', resultado)
        self.assertIn('sigma_rango', resultado)
        
        # Verificar que p_conjunta es muy pequeña (< 1e-6)
        self.assertLess(resultado['p_conjunta'], 1e-6)
        
        # Verificar que sigma es al menos 5
        self.assertGreater(resultado['sigma_calculada'], 5.0)
        
        # Verificar validación
        self.assertIn(resultado['validacion'], ['SIGNIFICATIVA', 'ALTAMENTE_SIGNIFICATIVA'])
    
    def test_probabilidades_individuales(self):
        """Verifica que las probabilidades individuales son razonables"""
        resultado = vbo.calcular_significancia_estadistica()
        
        p_ind = resultado['p_individual']
        
        # Todas las probabilidades deben estar entre 0 y 1
        for nombre, prob in p_ind.items():
            with self.subTest(probabilidad=nombre):
                self.assertGreaterEqual(prob, 0.0)
                self.assertLessEqual(prob, 1.0)
        
        # La probabilidad conjunta debe ser menor que cualquier individual
        for prob in p_ind.values():
            self.assertLess(resultado['p_conjunta'], prob)


class TestOutputFiles(unittest.TestCase):
    """Tests para la generación de archivos de salida"""
    
    def setUp(self):
        """Crear directorio temporal para tests"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpiar directorio temporal"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generar_visualizacion(self):
        """Verifica que se puede generar la visualización"""
        # Preparar resultados mínimos
        resultados = {
            'octavas': vbo.validar_octavas_hidrogenio(precision=50),
            'geometria': vbo.validar_geometria_sagrada(),
            'schumann': vbo.validar_resonancia_schumann(),
            'red_mcp': vbo.validar_red_mcp(),
            'estadistica': vbo.calcular_significancia_estadistica()
        }
        
        output_path = os.path.join(self.temp_dir, 'test_viz.png')
        
        # No debe lanzar excepción
        try:
            vbo.generar_visualizacion(resultados, output_path)
        except Exception as e:
            self.fail(f"generar_visualizacion() lanzó excepción: {e}")
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(output_path))
        
        # Verificar que tiene contenido
        self.assertGreater(os.path.getsize(output_path), 0)
    
    def test_generar_reporte_markdown(self):
        """Verifica que se puede generar el reporte Markdown"""
        # Preparar resultados mínimos
        resultados = {
            'octavas': vbo.validar_octavas_hidrogenio(precision=50),
            'geometria': vbo.validar_geometria_sagrada(),
            'schumann': vbo.validar_resonancia_schumann(),
            'red_mcp': vbo.validar_red_mcp(),
            'estadistica': vbo.calcular_significancia_estadistica()
        }
        
        output_path = os.path.join(self.temp_dir, 'test_report.md')
        
        # No debe lanzar excepción
        try:
            vbo.generar_reporte_markdown(resultados, output_path)
        except Exception as e:
            self.fail(f"generar_reporte_markdown() lanzó excepción: {e}")
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(output_path))
        
        # Verificar que tiene contenido
        self.assertGreater(os.path.getsize(output_path), 100)
        
        # Verificar que contiene las secciones esperadas
        with open(output_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        self.assertIn('Bóveda Ontológica', contenido)
        self.assertIn('Hidrógeno', contenido)
        self.assertIn('23.257', contenido)
        self.assertIn('888', contenido)
        self.assertIn('Schumann', contenido)


class TestIntegration(unittest.TestCase):
    """Tests de integración"""
    
    def test_validacion_completa(self):
        """Test de integración: ejecutar validación completa"""
        # Ejecutar todas las validaciones
        resultados = {
            'octavas': vbo.validar_octavas_hidrogenio(precision=50),
            'geometria': vbo.validar_geometria_sagrada(),
            'schumann': vbo.validar_resonancia_schumann(),
            'red_mcp': vbo.validar_red_mcp(),
            'estadistica': vbo.calcular_significancia_estadistica()
        }
        
        # Verificar que todas las validaciones son exitosas
        validaciones = [
            resultados['octavas']['validacion'],
            resultados['geometria']['validacion'],
            resultados['schumann']['validacion'],
            resultados['red_mcp']['validacion'],
            resultados['estadistica']['validacion']
        ]
        
        for validacion in validaciones:
            self.assertIn(validacion, ['EXITOSA', 'ALTAMENTE_SIGNIFICATIVA'])


def run_tests():
    """Ejecuta todos los tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
