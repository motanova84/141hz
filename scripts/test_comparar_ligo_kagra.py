#!/usr/bin/env python3
"""
Test para comparar_ligo_vs_kagra_sensibilidad.py
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.comparar_ligo_vs_kagra_sensibilidad import (
    obtener_sensibilidad_teorica,
    analizar_141hz_especificamente
)


class TestCompararLigoKagra(unittest.TestCase):
    
    def test_obtener_sensibilidad_teorica(self):
        """Verificar que se obtienen curvas de sensibilidad correctas"""
        sensibilidades = obtener_sensibilidad_teorica()
        
        # Verificar estructura
        self.assertIn('freqs', sensibilidades)
        self.assertIn('H1', sensibilidades)
        self.assertIn('L1', sensibilidades)
        self.assertIn('K1', sensibilidades)
        
        # Verificar que son arrays numpy
        self.assertIsInstance(sensibilidades['freqs'], np.ndarray)
        self.assertIsInstance(sensibilidades['H1'], np.ndarray)
        self.assertIsInstance(sensibilidades['L1'], np.ndarray)
        self.assertIsInstance(sensibilidades['K1'], np.ndarray)
        
        # Verificar que tienen la misma longitud
        n = len(sensibilidades['freqs'])
        self.assertEqual(len(sensibilidades['H1']), n)
        self.assertEqual(len(sensibilidades['L1']), n)
        self.assertEqual(len(sensibilidades['K1']), n)
        
        # Verificar rango de frecuencias
        self.assertGreater(sensibilidades['freqs'][0], 5)  # Al menos 5 Hz
        self.assertLess(sensibilidades['freqs'][-1], 2000)  # Menos de 2000 Hz
        
        # Verificar que los valores son positivos
        self.assertTrue(np.all(sensibilidades['H1'] > 0))
        self.assertTrue(np.all(sensibilidades['L1'] > 0))
        self.assertTrue(np.all(sensibilidades['K1'] > 0))
    
    def test_analizar_141hz_especificamente(self):
        """Verificar análisis específico en 141.7 Hz"""
        sensibilidades = obtener_sensibilidad_teorica()
        analisis = analizar_141hz_especificamente(sensibilidades)
        
        # Verificar estructura del resultado
        self.assertIn('freq', analisis)
        self.assertIn('asd_h1', analisis)
        self.assertIn('asd_l1', analisis)
        self.assertIn('asd_k1', analisis)
        self.assertIn('ratio_k1_h1', analisis)
        self.assertIn('ratio_k1_l1', analisis)
        
        # Verificar que la frecuencia es cercana a 141.7 Hz
        self.assertGreater(analisis['freq'], 140)
        self.assertLess(analisis['freq'], 143)
        
        # Verificar que los valores son positivos
        self.assertGreater(analisis['asd_h1'], 0)
        self.assertGreater(analisis['asd_l1'], 0)
        self.assertGreater(analisis['asd_k1'], 0)
        
        # Verificar que los ratios son razonables
        self.assertGreater(analisis['ratio_k1_h1'], 0)
        self.assertLess(analisis['ratio_k1_h1'], 10)  # No más de 10x diferencia
        self.assertGreater(analisis['ratio_k1_l1'], 0)
        self.assertLess(analisis['ratio_k1_l1'], 10)
    
    def test_sensibilidad_comparativa(self):
        """Verificar que KAGRA es comparable a LIGO en 141.7 Hz"""
        sensibilidades = obtener_sensibilidad_teorica()
        analisis = analizar_141hz_especificamente(sensibilidades)
        
        # Según el diseño, KAGRA debería ser comparable (<3x diferencia)
        # en la banda de 100-200 Hz donde es más sensible
        self.assertLess(analisis['ratio_k1_h1'], 3.0,
                       "KAGRA debería ser comparable a H1 en 141.7 Hz")
        self.assertLess(analisis['ratio_k1_l1'], 3.0,
                       "KAGRA debería ser comparable a L1 en 141.7 Hz")
    
    def test_orden_sensibilidad(self):
        """Verificar orden de magnitud de las sensibilidades"""
        sensibilidades = obtener_sensibilidad_teorica()
        analisis = analizar_141hz_especificamente(sensibilidades)
        
        # Las sensibilidades deberían estar en el orden de 10^-23 Hz^-1/2
        # en la banda de 100-200 Hz para detectores avanzados
        self.assertGreater(analisis['asd_h1'], 1e-24)
        self.assertLess(analisis['asd_h1'], 1e-22)
        
        self.assertGreater(analisis['asd_l1'], 1e-24)
        self.assertLess(analisis['asd_l1'], 1e-22)
        
        self.assertGreater(analisis['asd_k1'], 1e-24)
        self.assertLess(analisis['asd_k1'], 1e-22)
    
    def test_l1_peor_que_h1(self):
        """Verificar que L1 es típicamente menos sensible que H1"""
        sensibilidades = obtener_sensibilidad_teorica()
        analisis = analizar_141hz_especificamente(sensibilidades)
        
        # Históricamente L1 ha sido ~10% menos sensible que H1
        self.assertGreater(analisis['asd_l1'], analisis['asd_h1'],
                          "L1 debería ser menos sensible (ASD mayor) que H1")


if __name__ == '__main__':
    unittest.main(verbosity=2)
