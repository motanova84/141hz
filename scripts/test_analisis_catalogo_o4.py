#!/usr/bin/env python3
"""
Tests para el análisis del catálogo O4
"""

import unittest
import sys
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from analisis_catalogo_o4 import AnalisisCatalogoO4


class TestAnalisisCatalogoO4(unittest.TestCase):
    """Tests para AnalisisCatalogoO4"""
    
    def setUp(self):
        """Configuración inicial"""
        self.analizador = AnalisisCatalogoO4(f0=141.7001, tolerancia=0.55)
    
    def test_inicializacion(self):
        """Test: Inicialización correcta"""
        self.assertEqual(self.analizador.f0, 141.7001)
        self.assertEqual(self.analizador.tolerancia, 0.55)
        self.assertEqual(len(self.analizador.eventos_o4), 5)
    
    def test_eventos_o4(self):
        """Test: Eventos O4 correctos"""
        eventos_esperados = [
            'GW240109_050431',
            'GW240107_013215',
            'GW240105_151143',
            'GW240104_164932',
            'GW231231_154016'
        ]
        self.assertEqual(self.analizador.eventos_o4, eventos_esperados)
    
    def test_analisis_evento_simulado(self):
        """Test: Análisis de evento simulado"""
        resultado = self.analizador._analizar_evento_simulado('GW240109_050431', 'H1')
        
        self.assertIn('evento', resultado)
        self.assertIn('detector', resultado)
        self.assertIn('frecuencia_detectada', resultado)
        self.assertIn('delta_f', resultado)
        self.assertIn('snr', resultado)
        self.assertTrue(resultado['simulado'])
        
        # Verificar que la frecuencia está cerca de f0
        self.assertLess(abs(resultado['frecuencia_detectada'] - 141.7001), 2.0)
    
    def test_valores_documentados(self):
        """Test: Valores documentados correctos"""
        # GW240109_050431: 140.95 Hz (Δf = -0.7501)
        resultado = self.analizador._analizar_evento_simulado('GW240109_050431', 'H1')
        self.assertAlmostEqual(resultado['frecuencia_detectada'], 140.95, places=2)
        self.assertAlmostEqual(resultado['delta_f'], -0.7501, places=4)
        
        # GW240104_164932: 142.05 Hz (Δf = +0.3499)
        resultado = self.analizador._analizar_evento_simulado('GW240104_164932', 'H1')
        self.assertAlmostEqual(resultado['frecuencia_detectada'], 142.05, places=2)
        self.assertAlmostEqual(resultado['delta_f'], +0.3499, places=4)
    
    def test_calcular_estadisticas(self):
        """Test: Cálculo de estadísticas"""
        # Añadir resultados de prueba
        self.analizador.resultados = [
            {'delta_f': -0.75, 'abs_delta_f': 0.75, 'frecuencia_detectada': 140.95,
             'snr': 20.0, 'deteccion_exitosa': True},
            {'delta_f': -0.50, 'abs_delta_f': 0.50, 'frecuencia_detectada': 141.20,
             'snr': 25.0, 'deteccion_exitosa': True},
        ]
        
        self.analizador.calcular_estadisticas()
        
        self.assertIn('n_eventos', self.analizador.estadisticas)
        self.assertEqual(self.analizador.estadisticas['n_eventos'], 2)
        self.assertIn('media_delta_f', self.analizador.estadisticas)
        self.assertIn('std_delta_f', self.analizador.estadisticas)
        self.assertIn('media_snr', self.analizador.estadisticas)
        self.assertIn('tasa_deteccion', self.analizador.estadisticas)
    
    def test_ejecutar_analisis_completo(self):
        """Test: Ejecución completa del análisis"""
        resultados = self.analizador.ejecutar_analisis_completo(detector='H1')
        
        self.assertEqual(len(resultados), 5)
        self.assertTrue(len(self.analizador.estadisticas) > 0)
        
        # Verificar que todos los eventos fueron analizados
        eventos_analizados = [r['evento'] for r in resultados]
        for evento in self.analizador.eventos_o4:
            self.assertIn(evento, eventos_analizados)


class TestEstadisticasO4(unittest.TestCase):
    """Tests para estadísticas del análisis O4"""
    
    def test_estadisticas_documentadas(self):
        """Test: Estadísticas documentadas en el paper"""
        analizador = AnalisisCatalogoO4()
        
        # Simular resultados documentados
        analizador.resultados = [
            {'delta_f': -0.7501, 'abs_delta_f': 0.7501, 'frecuencia_detectada': 140.95,
             'snr': 20.0, 'deteccion_exitosa': True},
            {'delta_f': -0.9301, 'abs_delta_f': 0.9301, 'frecuencia_detectada': 140.77,
             'snr': 22.0, 'deteccion_exitosa': False},
            {'delta_f': -0.5001, 'abs_delta_f': 0.5001, 'frecuencia_detectada': 141.20,
             'snr': 25.0, 'deteccion_exitosa': True},
            {'delta_f': +0.3499, 'abs_delta_f': 0.3499, 'frecuencia_detectada': 142.05,
             'snr': 28.0, 'deteccion_exitosa': True},
            {'delta_f': -1.3001, 'abs_delta_f': 1.3001, 'frecuencia_detectada': 140.40,
             'snr': 18.0, 'deteccion_exitosa': False},
        ]
        
        analizador.calcular_estadisticas()
        
        # Media Δf documentada: -0.6261 Hz
        self.assertAlmostEqual(analizador.estadisticas['media_delta_f'], -0.6261, places=3)
        
        # Desviación estándar documentada: 0.6186 Hz
        self.assertAlmostEqual(analizador.estadisticas['std_delta_f'], 0.6186, places=3)
        
        # Valor p documentado: 0.0864
        self.assertAlmostEqual(analizador.estadisticas['p_value'], 0.0864, places=3)


def run_tests():
    """Ejecuta todos los tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestAnalisisCatalogoO4))
    suite.addTests(loader.loadTestsFromTestCase(TestEstadisticasO4))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
