#!/usr/bin/env python3
"""
Tests para Análisis de Resonancia Cruzada Virgo/KAGRA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import unittest
from resonancia_cruzada_virgo_kagra import AnalizadorResonanciaCruzada


class TestResonanciaCruzada(unittest.TestCase):
    """Tests para análisis de resonancia cruzada"""
    
    def setUp(self):
        """Configuración inicial"""
        self.analizador = AnalizadorResonanciaCruzada()
    
    def test_inicializacion(self):
        """Test de inicialización correcta"""
        self.assertEqual(self.analizador.f0, 141.7001)
        self.assertEqual(self.analizador.banda_ancho, 2.0)
        self.assertIn('H1', self.analizador.detectores_disponibles)
        self.assertIn('V1', self.analizador.detectores_disponibles)
        self.assertIn('K1', self.analizador.detectores_disponibles)
    
    def test_analizar_detector_sintetico(self):
        """Test de análisis de detector individual con datos sintéticos"""
        # Generar señal sintética
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        señal = 1e-21 * np.sin(2 * np.pi * self.analizador.f0 * t)
        ruido = np.random.normal(0, 2e-22, len(t))
        datos = señal + ruido
        
        # Analizar
        resultado = self.analizador.analizar_detector(datos, fs, 'TEST')
        
        # Verificar estructura
        self.assertEqual(resultado['detector'], 'TEST')
        self.assertIn('frecuencia_detectada', resultado)
        self.assertIn('snr_espectral', resultado)
        self.assertIn('snr_temporal', resultado)
        
        # Verificar que detectó cerca de f0
        self.assertLess(abs(resultado['frecuencia_detectada'] - self.analizador.f0), 1.0)
    
    def test_calcular_coherencia_sintetica(self):
        """Test de cálculo de coherencia con señales sintéticas"""
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        # Señales coherentes con ruido
        señal_base = 1e-21 * np.sin(2 * np.pi * self.analizador.f0 * t)
        
        datos1 = señal_base + np.random.normal(0, 2e-22, len(t))
        datos2 = señal_base + np.random.normal(0, 2e-22, len(t))
        
        # Calcular coherencia
        coherencia = self.analizador.calcular_coherencia(datos1, datos2, fs, 'H1', 'L1')
        
        # Verificar estructura
        self.assertEqual(coherencia['par'], 'H1-L1')
        self.assertIn('coherencia_banda', coherencia)
        self.assertIn('coherencia_f0', coherencia)
        self.assertIn('fase_relativa', coherencia)
        
        # Coherencia debe ser alta para señales similares
        self.assertGreater(coherencia['coherencia_f0'], 0.3)
    
    def test_coherencia_señales_independientes(self):
        """Test de coherencia baja con señales independientes"""
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        # Señales completamente independientes
        datos1 = np.random.normal(0, 1e-21, len(t))
        datos2 = np.random.normal(0, 1e-21, len(t))
        
        coherencia = self.analizador.calcular_coherencia(datos1, datos2, fs, 'H1', 'L1')
        
        # Coherencia debe ser baja para ruido independiente
        self.assertLess(coherencia['coherencia_f0'], 0.5)
    
    def test_analisis_simulado_completo(self):
        """Test de análisis simulado completo de evento"""
        resultados = self.analizador._analisis_simulado('GW150914', ['H1', 'L1', 'V1'])
        
        # Verificar estructura
        self.assertEqual(resultados['evento'], 'GW150914')
        self.assertEqual(resultados['f0'], 141.7001)
        self.assertTrue(resultados.get('simulado', False))
        
        # Verificar detectores
        self.assertIn('H1', resultados['detectores'])
        self.assertIn('L1', resultados['detectores'])
        self.assertIn('V1', resultados['detectores'])
        
        # Verificar coherencias
        self.assertGreater(len(resultados['coherencias']), 0)
        
        # Verificar pares de coherencia
        pares_esperados = {'H1-L1', 'H1-V1', 'L1-V1'}
        pares_encontrados = {c['par'] for c in resultados['coherencias']}
        self.assertEqual(pares_esperados, pares_encontrados)
    
    def test_coherencia_alta_señal_coherente(self):
        """Test de que señales coherentes producen alta coherencia"""
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        # Señal exactamente igual con ruido pequeño
        señal = 1e-21 * np.sin(2 * np.pi * self.analizador.f0 * t)
        
        datos1 = señal + np.random.normal(0, 1e-23, len(t))
        datos2 = señal + np.random.normal(0, 1e-23, len(t))
        
        coherencia = self.analizador.calcular_coherencia(datos1, datos2, fs, 'H1', 'L1')
        
        # Alta coherencia esperada
        self.assertGreater(coherencia['coherencia_f0'], 0.6)


def run_tests():
    """Ejecuta todos los tests"""
    print("🧪 EJECUTANDO TESTS: Resonancia Cruzada Virgo/KAGRA")
    print("=" * 70)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResonanciaCruzada)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
