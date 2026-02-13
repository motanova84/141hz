#!/usr/bin/env python3
"""
Tests para Validación de Biología Cuántica QCAL ∞³

Verifica que las validaciones de:
1. Magnetorrecepción
2. Microtúbulos
3. Replicación independiente
4. Correlación AAA

funcionen correctamente y den resultados esperados.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import unittest
import sys
import os
import json
import numpy as np

# Add scripts to path
sys.path.insert(0, '/home/runner/work/141hz/141hz/scripts')

from validacion_biologia_cuantica_qcal import (
    validate_magnetoreception,
    validate_microtubule_resonance,
    validate_independent_replication,
    validate_AAA_correlation,
    F0_HZ
)


class TestMagnetoreceptionValidation(unittest.TestCase):
    """Tests para validación de magnetorrecepción."""
    
    def test_magnetoreception_returns_dict(self):
        """Verifica que retorna un diccionario."""
        result = validate_magnetoreception()
        self.assertIsInstance(result, dict)
    
    def test_magnetoreception_has_required_fields(self):
        """Verifica que tiene los campos requeridos."""
        result = validate_magnetoreception()
        required_fields = [
            'system', 'prediction_percent', 'measured_percent',
            'uncertainty_percent', 'sigma_from_prediction',
            'experimental_sigma', 'p_value', 'validated'
        ]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_magnetoreception_measured_near_prediction(self):
        """Verifica que medición está cerca de predicción."""
        result = validate_magnetoreception()
        # 0.1987% vs 0.20% - diferencia < 0.02%
        diff = abs(result['measured_percent'] - result['prediction_percent'])
        self.assertLess(diff, 0.02)
    
    def test_magnetoreception_high_significance(self):
        """Verifica alta significancia experimental."""
        result = validate_magnetoreception()
        self.assertGreater(result['experimental_sigma'], 9.0)
        self.assertLess(result['p_value'], 1e-9)
    
    def test_magnetoreception_validated(self):
        """Verifica que predicción está validada."""
        result = validate_magnetoreception()
        self.assertTrue(result['validated'])
    
    def test_magnetoreception_coherence_time(self):
        """Verifica tiempo de coherencia suficiente."""
        result = validate_magnetoreception()
        self.assertGreater(result['coherence_time_us'], 50)  # > 50 μs
        self.assertGreater(result['coherence_ratio'], 10)  # >> 1


class TestMicrotubuleValidation(unittest.TestCase):
    """Tests para validación de microtúbulos."""
    
    def test_microtubule_returns_dict(self):
        """Verifica que retorna un diccionario."""
        result = validate_microtubule_resonance()
        self.assertIsInstance(result, dict)
    
    def test_microtubule_has_required_fields(self):
        """Verifica que tiene los campos requeridos."""
        result = validate_microtubule_resonance()
        required_fields = [
            'system', 'prediction_range_Hz', 'measured_Hz',
            'uncertainty_Hz', 'in_range', 'experimental_sigma',
            'p_value', 'validated'
        ]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_microtubule_in_predicted_range(self):
        """Verifica que medición está en rango predicho."""
        result = validate_microtubule_resonance()
        self.assertTrue(result['in_range'])
        self.assertGreaterEqual(result['measured_Hz'], result['prediction_range_Hz'][0])
        self.assertLessEqual(result['measured_Hz'], result['prediction_range_Hz'][1])
    
    def test_microtubule_near_f0(self):
        """Verifica que está cerca de f₀."""
        result = validate_microtubule_resonance()
        diff = abs(result['measured_Hz'] - F0_HZ)
        self.assertLess(diff, 0.5)  # Dentro de 0.5 Hz
    
    def test_microtubule_high_significance(self):
        """Verifica alta significancia experimental."""
        result = validate_microtubule_resonance()
        self.assertGreater(result['experimental_sigma'], 8.0)
        self.assertLess(result['p_value'], 1e-17)
    
    def test_microtubule_biological_response(self):
        """Verifica interpretación como respuesta biológica."""
        result = validate_microtubule_resonance()
        self.assertTrue(result['biological_response'])


class TestIndependentReplicationValidation(unittest.TestCase):
    """Tests para replicación independiente."""
    
    def test_replication_returns_dict(self):
        """Verifica que retorna un diccionario."""
        result = validate_independent_replication()
        self.assertIsInstance(result, dict)
    
    def test_replication_has_required_fields(self):
        """Verifica que tiene los campos requeridos."""
        result = validate_independent_replication()
        required_fields = [
            'system', 'prediction_percent', 'original_percent',
            'replicated_percent', 'sigma_replicated', 'validated'
        ]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_replication_consistent_with_original(self):
        """Verifica consistencia con medición original."""
        result = validate_independent_replication()
        # Diferencia entre original y replicación < 0.05%
        diff = abs(result['original_percent'] - result['replicated_percent'])
        self.assertLess(diff, 0.05)
    
    def test_replication_near_prediction(self):
        """Verifica que replicación está cerca de predicción."""
        result = validate_independent_replication()
        diff = abs(result['replicated_percent'] - result['prediction_percent'])
        self.assertLess(diff, 0.01)
    
    def test_replication_significant(self):
        """Verifica significancia de replicación."""
        result = validate_independent_replication()
        self.assertGreater(result['sigma_replicated'], 5.0)
        self.assertLess(result['p_value_replicated'], 1e-7)
    
    def test_replication_combined_pvalue(self):
        """Verifica p-value combinado es muy bajo."""
        result = validate_independent_replication()
        self.assertLess(result['combined_p_value'], 1e-15)


class TestAAACorrelationValidation(unittest.TestCase):
    """Tests para correlación AAA."""
    
    def test_AAA_returns_dict(self):
        """Verifica que retorna un diccionario."""
        result = validate_AAA_correlation()
        self.assertIsInstance(result, dict)
    
    def test_AAA_has_required_fields(self):
        """Verifica que tiene los campos requeridos."""
        result = validate_AAA_correlation()
        required_fields = [
            'system', 'AAA_relation', 'n_nodes',
            'coherence_per_node', 'chirality_filter', 'validated'
        ]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_AAA_value(self):
        """Verifica valor de AAA."""
        result = validate_AAA_correlation()
        self.assertAlmostEqual(result['AAA_relation'], 0.8991, places=4)
    
    def test_AAA_nodes(self):
        """Verifica número de nodos Noesis88."""
        result = validate_AAA_correlation()
        self.assertEqual(result['n_nodes'], 88)
    
    def test_AAA_coherence_per_node(self):
        """Verifica coherencia por nodo."""
        result = validate_AAA_correlation()
        # C_per_node = AAA^(1/88)
        expected = result['AAA_relation'] ** (1/88)
        self.assertAlmostEqual(result['coherence_per_node'], expected, places=6)
    
    def test_AAA_chirality_filter(self):
        """Verifica filtro de quiralidad."""
        result = validate_AAA_correlation()
        self.assertTrue(result['chirality_filter'])
    
    def test_AAA_dna_pitch(self):
        """Verifica pitch de DNA."""
        result = validate_AAA_correlation()
        # DNA pitch ~3.4 nm
        self.assertAlmostEqual(result['dna_pitch_nm'], 3.4, places=1)


class TestIntegration(unittest.TestCase):
    """Tests de integración."""
    
    def test_all_validations_pass(self):
        """Verifica que todas las validaciones pasan."""
        results = {
            'mag': validate_magnetoreception(),
            'mic': validate_microtubule_resonance(),
            'rep': validate_independent_replication(),
            'aaa': validate_AAA_correlation()
        }
        
        for key, result in results.items():
            self.assertTrue(result.get('validated', False),
                          f"Validación {key} falló")
    
    def test_constants_consistency(self):
        """Verifica consistencia de constantes."""
        mag = validate_magnetoreception()
        mic = validate_microtubule_resonance()
        
        # Ambos usan F0_HZ
        self.assertEqual(F0_HZ, 141.7001)
        
        # Microtúbulos deben estar cerca de f₀
        self.assertAlmostEqual(mic['measured_Hz'], F0_HZ, delta=0.5)


def run_tests():
    """Ejecuta todos los tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMagnetoreceptionValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestMicrotubuleValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIndependentReplicationValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestAAACorrelationValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
