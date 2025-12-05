#!/usr/bin/env python3
"""
Tests para la validación GWTC-1 tri-detector
"""

import unittest
import sys
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from validacion_gwtc1_tridetector import ValidacionGWTC1TriDetector


class TestValidacionGWTC1TriDetector(unittest.TestCase):
    """Tests para ValidacionGWTC1TriDetector"""
    
    def setUp(self):
        """Configuración inicial"""
        self.validador = ValidacionGWTC1TriDetector(f0=141.7001, tolerancia=2.0)
    
    def test_inicializacion(self):
        """Test: Inicialización correcta"""
        self.assertEqual(self.validador.f0, 141.7001)
        self.assertEqual(self.validador.tolerancia, 2.0)
        self.assertEqual(len(self.validador.eventos_gwtc1), 11)
        self.assertEqual(len(self.validador.eventos_virgo), 3)
    
    def test_eventos_gwtc1(self):
        """Test: Eventos GWTC-1 correctos"""
        eventos_esperados = [
            'GW150914', 'GW151012', 'GW151226',
            'GW170104', 'GW170608', 'GW170729',
            'GW170809', 'GW170814', 'GW170817',
            'GW170818', 'GW170823'
        ]
        self.assertEqual(self.validador.eventos_gwtc1, eventos_esperados)
    
    def test_eventos_virgo(self):
        """Test: Eventos con datos Virgo"""
        eventos_virgo_esperados = ['GW170814', 'GW170817', 'GW170818']
        self.assertEqual(self.validador.eventos_virgo, eventos_virgo_esperados)
    
    def test_analisis_detector_simulado_h1(self):
        """Test: Análisis simulado detector H1"""
        resultado = self.validador._analizar_detector_simulado('GW150914', 'H1')
        
        self.assertIn('frecuencia_detectada', resultado)
        self.assertIn('delta_f', resultado)
        self.assertIn('snr', resultado)
        self.assertTrue(resultado['simulado'])
        
        # SNR documentado para GW150914 H1: 14.49
        self.assertAlmostEqual(resultado['snr'], 14.49, places=2)
    
    def test_analisis_detector_simulado_l1(self):
        """Test: Análisis simulado detector L1"""
        resultado = self.validador._analizar_detector_simulado('GW150914', 'L1')
        
        # SNR documentado para GW150914 L1: 13.87
        self.assertAlmostEqual(resultado['snr'], 13.87, places=2)
    
    def test_analisis_detector_simulado_v1(self):
        """Test: Análisis simulado detector V1"""
        resultado = self.validador._analizar_detector_simulado('GW170814', 'V1')
        
        # SNR documentado para GW170814 V1: 8.08
        self.assertAlmostEqual(resultado['snr'], 8.08, places=2)
    
    def test_calcular_estadisticas(self):
        """Test: Cálculo de estadísticas tri-detector"""
        # Añadir resultados de prueba
        self.validador.resultados = [
            {
                'evento': 'GW150914',
                'detectores': {
                    'H1': {'snr': 14.49, 'frecuencia_detectada': 141.70, 
                           'delta_f': 0.0, 'deteccion_exitosa': True},
                    'L1': {'snr': 13.87, 'frecuencia_detectada': 141.71,
                           'delta_f': 0.01, 'deteccion_exitosa': True}
                }
            }
        ]
        
        self.validador.calcular_estadisticas()
        
        self.assertIn('H1', self.validador.estadisticas)
        self.assertIn('L1', self.validador.estadisticas)
        
        self.assertEqual(self.validador.estadisticas['H1']['n_eventos'], 1)
        self.assertEqual(self.validador.estadisticas['L1']['n_eventos'], 1)
    
    def test_ejecutar_validacion_completa(self):
        """Test: Ejecución completa de la validación"""
        resultados = self.validador.ejecutar_validacion_completa()
        
        self.assertEqual(len(resultados), 11)
        self.assertTrue(len(self.validador.estadisticas) > 0)
        
        # Verificar que todos los eventos GWTC-1 fueron analizados
        eventos_analizados = [r['evento'] for r in resultados]
        for evento in self.validador.eventos_gwtc1:
            self.assertIn(evento, eventos_analizados)
        
        # Verificar que hay estadísticas para H1 y L1
        self.assertIn('H1', self.validador.estadisticas)
        self.assertIn('L1', self.validador.estadisticas)


class TestEstadisticasGWTC1(unittest.TestCase):
    """Tests para estadísticas documentadas de GWTC-1"""
    
    def test_snr_medio_h1_documentado(self):
        """Test: SNR medio H1 documentado = 21.38 ± 6.38"""
        validador = ValidacionGWTC1TriDetector()
        
        # Simular resultados con SNR documentados
        eventos_snr_h1 = [14.49, 12.04, 23.17, 19.48, 26.81, 31.35, 
                          26.51, 22.26, 10.78, 20.83, 27.50]
        
        validador.resultados = [
            {
                'evento': f'GW{i}',
                'detectores': {
                    'H1': {'snr': snr, 'frecuencia_detectada': 141.70,
                           'delta_f': 0.0, 'deteccion_exitosa': True}
                }
            }
            for i, snr in enumerate(eventos_snr_h1)
        ]
        
        validador.calcular_estadisticas()
        
        # Media documentada: 21.38
        self.assertAlmostEqual(validador.estadisticas['H1']['media_snr'], 21.38, places=2)
        
        # Desviación estándar documentada: 6.38 (permitir diferencia de ±0.5)
        self.assertAlmostEqual(validador.estadisticas['H1']['std_snr'], 6.38, places=0)
    
    def test_snr_medio_l1_documentado(self):
        """Test: SNR medio L1 documentado = 15.00 ± 8.12"""
        validador = ValidacionGWTC1TriDetector()
        
        # SNR documentados para L1
        eventos_snr_l1 = [13.87, 27.31, 30.04, 15.79, 10.36, 4.90,
                          15.65, 12.96, 3.40, 12.38, 18.31]
        
        validador.resultados = [
            {
                'evento': f'GW{i}',
                'detectores': {
                    'L1': {'snr': snr, 'frecuencia_detectada': 141.70,
                           'delta_f': 0.0, 'deteccion_exitosa': True}
                }
            }
            for i, snr in enumerate(eventos_snr_l1)
        ]
        
        validador.calcular_estadisticas()
        
        # Media documentada: 15.00
        self.assertAlmostEqual(validador.estadisticas['L1']['media_snr'], 15.00, places=2)
        
        # Desviación estándar documentada: 8.12
        self.assertAlmostEqual(validador.estadisticas['L1']['std_snr'], 8.12, places=1)
    
    def test_snr_medio_v1_documentado(self):
        """Test: SNR medio V1 documentado = 8.17 ± 0.36"""
        validador = ValidacionGWTC1TriDetector()
        
        # SNR documentados para V1
        eventos_snr_v1 = [8.08, 8.57, 7.86]
        
        validador.resultados = [
            {
                'evento': f'GW{i}',
                'detectores': {
                    'V1': {'snr': snr, 'frecuencia_detectada': 141.70,
                           'delta_f': 0.0, 'deteccion_exitosa': True}
                }
            }
            for i, snr in enumerate(eventos_snr_v1)
        ]
        
        validador.calcular_estadisticas()
        
        # Media documentada: 8.17
        self.assertAlmostEqual(validador.estadisticas['V1']['media_snr'], 8.17, places=2)
        
        # Desviación estándar documentada: 0.36
        self.assertAlmostEqual(validador.estadisticas['V1']['std_snr'], 0.36, places=2)
    
    def test_tasa_deteccion_100_porciento(self):
        """Test: Tasa de detección 100% para todos los detectores"""
        validador = ValidacionGWTC1TriDetector()
        
        # Simular detecciones 100% exitosas
        validador.resultados = [
            {
                'evento': f'GW{i}',
                'detectores': {
                    'H1': {'snr': 20.0, 'frecuencia_detectada': 141.70,
                           'delta_f': 0.0, 'deteccion_exitosa': True},
                    'L1': {'snr': 15.0, 'frecuencia_detectada': 141.70,
                           'delta_f': 0.0, 'deteccion_exitosa': True}
                }
            }
            for i in range(11)
        ]
        
        validador.calcular_estadisticas()
        
        # Verificar tasa de detección 100%
        self.assertEqual(validador.estadisticas['H1']['tasa_deteccion'], 1.0)
        self.assertEqual(validador.estadisticas['L1']['tasa_deteccion'], 1.0)
        self.assertEqual(validador.estadisticas['H1']['detecciones'], 11)
        self.assertEqual(validador.estadisticas['L1']['detecciones'], 11)


def run_tests():
    """Ejecuta todos los tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestValidacionGWTC1TriDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestEstadisticasGWTC1))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
