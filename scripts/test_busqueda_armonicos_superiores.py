#!/usr/bin/env python3
"""
Tests para Búsqueda de Armónicos Superiores
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import unittest
from busqueda_armonicos_superiores import BuscadorArmonicosSuperiores


class TestBuscadorArmonicos(unittest.TestCase):
    """Tests para el buscador de armónicos superiores"""
    
    def setUp(self):
        """Configuración inicial"""
        self.buscador = BuscadorArmonicosSuperiores()
    
    def test_inicializacion(self):
        """Test de inicialización correcta"""
        self.assertEqual(self.buscador.f0, 141.7001)
        self.assertIsNotNone(self.buscador.armonicos)
        self.assertGreater(len(self.buscador.armonicos), 0)
    
    def test_calculo_armonicos(self):
        """Test de cálculo de armónicos"""
        armonicos = self.buscador.armonicos
        
        # Verificar que contiene tipos esperados
        tipos = set(info['tipo'] for info in armonicos.values())
        self.assertIn('submúltiplo', tipos)
        self.assertIn('múltiplo', tipos)
        self.assertIn('áureo', tipos)
        self.assertIn('pi', tipos)
        
        # Verificar algunos valores específicos
        self.assertIn('f0/2', armonicos)
        self.assertAlmostEqual(armonicos['f0/2']['frecuencia'], 141.7001/2, places=2)
        
        self.assertIn('2f0', armonicos)
        self.assertAlmostEqual(armonicos['2f0']['frecuencia'], 141.7001*2, places=2)
    
    def test_busqueda_en_datos_sinteticos(self):
        """Test de búsqueda en datos sintéticos"""
        # Generar datos sintéticos con varios armónicos
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        # Señal con f0 y 2f0
        señal = (1e-21 * np.sin(2 * np.pi * self.buscador.f0 * t) +
                0.5e-21 * np.sin(2 * np.pi * 2 * self.buscador.f0 * t))
        ruido = np.random.normal(0, 1e-22, len(t))
        datos = señal + ruido
        
        # Buscar armónicos
        resultados = self.buscador.buscar_en_datos(datos, fs, 'TEST')
        
        # Verificar que detectó 2f0 (que está en la señal)
        self.assertIn('2f0', resultados)
        
        # Verificar estructura de resultados
        for nombre, res in resultados.items():
            if res.get('detectable', False):
                self.assertIn('frecuencia_teorica', res)
                self.assertIn('snr', res)
                self.assertIn('tipo', res)
    
    def test_analisis_simulado(self):
        """Test de análisis simulado completo"""
        resultados = self.buscador._analisis_simulado('GW150914', ['H1', 'L1'])
        
        self.assertEqual(resultados['evento'], 'GW150914')
        self.assertEqual(resultados['f0'], 141.7001)
        self.assertIn('H1', resultados['detectores'])
        self.assertIn('L1', resultados['detectores'])
        self.assertTrue(resultados.get('simulado', False))
    
    def test_rango_frecuencias(self):
        """Test de que las frecuencias están en rangos razonables"""
        for nombre, info in self.buscador.armonicos.items():
            freq = info['frecuencia']
            # LIGO sensible a 10-2000 Hz
            # Algunos armónicos pueden estar fuera, es normal
            self.assertGreater(freq, 0, f"{nombre} tiene frecuencia no positiva")
            self.assertLess(freq, 5000, f"{nombre} tiene frecuencia muy alta")


def run_tests():
    """Ejecuta todos los tests"""
    print("🧪 EJECUTANDO TESTS: Búsqueda de Armónicos Superiores")
    print("=" * 70)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBuscadorArmonicos)
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
