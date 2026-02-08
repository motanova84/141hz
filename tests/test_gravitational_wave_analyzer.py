#!/usr/bin/env python3
"""
Tests for Gravitational Wave Analyzer
======================================

Pruebas unitarias para el módulo gravitational_wave_analyzer.py
que busca la firma de 141.7 Hz en datos de ondas gravitacionales.

Autor: Sistema QCAL ∞³
Fecha: 2026-02-03
"""

import unittest
import numpy as np
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gravitational_wave_analyzer import GravitationalWaveAnalyzer


class TestGravitationalWaveAnalyzer(unittest.TestCase):
    """
    Tests para GravitationalWaveAnalyzer.
    """
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.analyzer = GravitationalWaveAnalyzer(evento="GW250114", precision=30)
    
    def test_inicializacion(self):
        """Test de inicialización del analizador."""
        self.assertEqual(self.analyzer.evento, "GW250114")
        self.assertEqual(self.analyzer.f0, 141.7001)
        self.assertEqual(self.analyzer.precision, 30)
        self.assertIn('H1', self.analyzer.detectores)
        self.assertIn('L1', self.analyzer.detectores)
        self.assertIn('V1', self.analyzer.detectores)
    
    def test_f0_value(self):
        """Test de que f0 es la frecuencia QCAL correcta."""
        self.assertAlmostEqual(self.analyzer.f0, 141.7001, places=4)
    
    def test_directorios_creados(self):
        """Test de que los directorios necesarios se crean."""
        self.assertTrue(self.analyzer.data_dir.exists())
        self.assertTrue(self.analyzer.results_dir.exists())
    
    def test_generar_strain_simulado(self):
        """Test de generación de datos simulados."""
        strain = self.analyzer._generar_strain_simulado('H1')
        
        # Verificar que se generó correctamente
        self.assertIsNotNone(strain)
        self.assertEqual(strain.sample_rate.value, 4096)
        
        # Verificar que tiene la duración correcta (32 segundos)
        expected_length = 32 * 4096
        self.assertEqual(len(strain), expected_length)
    
    def test_analizar_ringdown_simulado(self):
        """Test de análisis de ringdown con datos simulados."""
        # Generar datos simulados
        strain = self.analyzer._generar_strain_simulado('H1')
        
        # Analizar ringdown
        resultado = self.analyzer.analizar_ringdown(strain, 'H1')
        
        # Verificar estructura de resultados
        self.assertIn('detector', resultado)
        self.assertIn('freq_detected', resultado)
        self.assertIn('snr', resultado)
        self.assertIn('power', resultado)
        self.assertIn('sigma', resultado)
        
        # Verificar que el detector es correcto
        self.assertEqual(resultado['detector'], 'H1')
        
        # Verificar que la frecuencia detectada está en un rango razonable
        self.assertGreater(resultado['freq_detected'], 140.0)
        self.assertLess(resultado['freq_detected'], 143.0)
    
    def test_analisis_multidetector_simulado(self):
        """Test de análisis coherente multi-detector con datos simulados."""
        # Simular resultados de múltiples detectores
        resultados_detectores = {
            'H1': {
                'freq_detected': 141.70,
                'snr': 5.0,
                'power': 0.8
            },
            'L1': {
                'freq_detected': 141.71,
                'snr': 4.5,
                'power': 0.7
            },
            'V1': {
                'freq_detected': 141.69,
                'snr': 3.0,
                'power': 0.6
            }
        }
        
        # Realizar análisis coherente
        analisis = self.analyzer.analisis_coherente_multidetector(resultados_detectores)
        
        # Verificar estructura
        self.assertIn('n_detectores', analisis)
        self.assertIn('freq_coherente', analisis)
        self.assertIn('snr_coherente', analisis)
        self.assertIn('coherencia', analisis)
        
        # Verificar valores
        self.assertEqual(analisis['n_detectores'], 3)
        self.assertGreater(analisis['snr_coherente'], 0)
        self.assertGreater(analisis['coherencia'], 0)
        self.assertLessEqual(analisis['coherencia'], 1.0)
        
        # Verificar que la frecuencia coherente está cerca de f0
        self.assertAlmostEqual(analisis['freq_coherente'], 141.70, delta=0.5)
    
    def test_ejecutar_analisis_completo_simulado(self):
        """Test de ejecución completa del análisis en modo simulado."""
        # Ejecutar análisis completo
        resultados = self.analyzer.ejecutar_analisis_completo(simulated=True)
        
        # Verificar estructura de resultados
        self.assertIn('evento', resultados)
        self.assertIn('f0_qcal', resultados)
        self.assertIn('detectores', resultados)
        self.assertIn('timestamp', resultados)
        
        # Verificar que se procesaron detectores
        self.assertGreater(len(resultados['detectores']), 0)
        
        # Verificar que existe análisis coherente
        if len(resultados['detectores']) > 1:
            self.assertIn('analisis_coherente', resultados)
    
    def test_resultados_guardados(self):
        """Test de que los resultados se guardan correctamente."""
        # Ejecutar análisis
        self.analyzer.ejecutar_analisis_completo(simulated=True)
        
        # Verificar que se creó el archivo de resultados
        output_file = self.analyzer.results_dir / f"{self.analyzer.evento}_resultados_141hz.json"
        self.assertTrue(output_file.exists())
        
        # Verificar que el archivo contiene datos
        self.assertGreater(output_file.stat().st_size, 0)
    
    def test_visualizaciones_generadas(self):
        """Test de que se generan las visualizaciones."""
        # Ejecutar análisis
        self.analyzer.ejecutar_analisis_completo(simulated=True)
        
        # Verificar que se creó la visualización
        viz_file = self.analyzer.results_dir / f"{self.analyzer.evento}_analisis_espectral.png"
        self.assertTrue(viz_file.exists())
        
        # Verificar que el archivo tiene contenido
        self.assertGreater(viz_file.stat().st_size, 0)
    
    def test_precision_configuracion(self):
        """Test de configuración de precisión."""
        # Crear analizador con precisión específica
        analyzer_hp = GravitationalWaveAnalyzer(evento="GW150914", precision=100)
        self.assertEqual(analyzer_hp.precision, 100)
    
    def test_diferentes_eventos(self):
        """Test de análisis con diferentes eventos."""
        eventos = ["GW150914", "GW250114", "GW170814"]
        
        for evento in eventos:
            analyzer = GravitationalWaveAnalyzer(evento=evento, precision=30)
            self.assertEqual(analyzer.evento, evento)
            
            # Verificar que los directorios tienen el nombre correcto
            expected_dir = evento.lower() + "_141hz"
            self.assertTrue(str(analyzer.results_dir).endswith(expected_dir))
    
    def test_banda_frecuencias(self):
        """Test de configuración de bandas de frecuencia."""
        self.assertEqual(self.analyzer.freq_band, (100.0, 200.0))
        self.assertEqual(self.analyzer.freq_target_band, (140.0, 143.0))
        
        # Verificar que f0 está dentro de la banda objetivo
        self.assertGreater(self.analyzer.f0, self.analyzer.freq_target_band[0])
        self.assertLess(self.analyzer.f0, self.analyzer.freq_target_band[1])
    
    def test_parametros_analisis(self):
        """Test de parámetros de análisis temporal."""
        self.assertEqual(self.analyzer.sample_rate, 4096)
        self.assertEqual(self.analyzer.pre_merger, 2.0)
        self.assertEqual(self.analyzer.post_merger, 4.0)
        self.assertEqual(self.analyzer.ringdown_start, 0.010)
        self.assertEqual(self.analyzer.ringdown_duration, 0.500)


class TestGravitationalWaveAnalyzerIntegration(unittest.TestCase):
    """
    Tests de integración para el analizador completo.
    """
    
    def test_pipeline_completo_gw250114(self):
        """Test del pipeline completo para GW250114."""
        analyzer = GravitationalWaveAnalyzer(evento="GW250114", precision=30)
        
        # Ejecutar análisis en modo simulado
        resultados = analyzer.ejecutar_analisis_completo(simulated=True)
        
        # Verificar estructura completa
        self.assertIn('evento', resultados)
        self.assertIn('f0_qcal', resultados)
        self.assertIn('detectores', resultados)
        self.assertIn('analisis_coherente', resultados)
        
        # Verificar coherencia de resultados
        ac = resultados['analisis_coherente']
        self.assertGreater(ac['snr_coherente'], 0)
        self.assertGreater(ac['coherencia'], 0)
        
        # Verificar que el error es razonable
        self.assertLess(ac['error_vs_f0'], 1.0)  # Error menor a 1 Hz
    
    def test_consistencia_multidetector(self):
        """Test de consistencia entre detectores."""
        analyzer = GravitationalWaveAnalyzer(evento="GW150914", precision=30)
        
        # Generar strains para múltiples detectores
        strains = {}
        for detector in ['H1', 'L1']:
            strains[detector] = analyzer._generar_strain_simulado(detector)
        
        # Analizar cada detector
        resultados = {}
        for detector, strain in strains.items():
            resultados[detector] = analyzer.analizar_ringdown(strain, detector)
        
        # Verificar que las frecuencias son consistentes
        freqs = [r['freq_detected'] for r in resultados.values()]
        freq_std = np.std(freqs)
        
        # La desviación estándar debe ser pequeña (coherencia)
        self.assertLess(freq_std, 1.0)  # Menos de 1 Hz de dispersión
    
    def test_robustez_ruido(self):
        """Test de robustez frente a diferentes niveles de ruido."""
        analyzer = GravitationalWaveAnalyzer(evento="GW250114", precision=30)
        
        # Generar strain con ruido
        strain = analyzer._generar_strain_simulado('H1')
        
        # Analizar múltiples veces (el ruido es aleatorio)
        resultados = []
        for _ in range(3):
            strain = analyzer._generar_strain_simulado('H1')
            res = analyzer.analizar_ringdown(strain, 'H1')
            resultados.append(res)
        
        # Verificar que todas las detecciones están cerca de f0
        for res in resultados:
            self.assertLess(res['freq_error'], 1.0)


def suite():
    """Crear suite de tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGravitationalWaveAnalyzer))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGravitationalWaveAnalyzerIntegration))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
