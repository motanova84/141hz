#!/usr/bin/env python3
"""
Tests para Validación de Estándares de Descubrimiento Científico

Verifica que la validación de estándares funciona correctamente y que
todos los umbrales son correctos según las normas de cada disciplina.
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from discovery_standards import DiscoveryStandardsValidator


class TestDiscoveryStandardsValidator(unittest.TestCase):
    """Tests para el validador de estándares de descubrimiento."""
    
    def setUp(self):
        """Configurar el validador antes de cada test."""
        self.validator = DiscoveryStandardsValidator()
    
    def test_standards_defined(self):
        """Test que todos los estándares están definidos correctamente."""
        # Verificar que existen los tres estándares
        self.assertIn('fisica_particulas', self.validator.standards)
        self.assertIn('astronomia', self.validator.standards)
        self.assertIn('medicina_eeg', self.validator.standards)
        
        # Verificar umbrales correctos
        self.assertEqual(self.validator.standards['fisica_particulas']['umbral_sigma'], 5.0)
        self.assertEqual(self.validator.standards['astronomia']['umbral_sigma'], 3.0)
        self.assertEqual(self.validator.standards['medicina_eeg']['umbral_sigma'], 2.0)
    
    def test_observed_results_defined(self):
        """Test que los resultados observados están definidos."""
        self.assertIn('significancia_sigma', self.validator.observed_results)
        self.assertIn('p_value', self.validator.observed_results)
        self.assertIn('evento', self.validator.observed_results)
        
        # Verificar que la significancia es >10σ
        self.assertGreater(self.validator.observed_results['significancia_sigma'], 10.0)
    
    def test_validate_fisica_particulas(self):
        """Test validación para física de partículas (≥5σ)."""
        result = self.validator.validate_standard('fisica_particulas')
        
        self.assertEqual(result['disciplina'], 'Física de partículas')
        self.assertEqual(result['umbral_requerido'], '≥ 5.0σ')
        self.assertTrue(result['cumple'])
        self.assertEqual(result['simbolo'], '✅ Cumple')
    
    def test_validate_astronomia(self):
        """Test validación para astronomía (≥3σ)."""
        result = self.validator.validate_standard('astronomia')
        
        self.assertEqual(result['disciplina'], 'Astronomía')
        self.assertEqual(result['umbral_requerido'], '≥ 3.0σ')
        self.assertTrue(result['cumple'])
        self.assertEqual(result['simbolo'], '✅ Cumple')
    
    def test_validate_medicina_eeg(self):
        """Test validación para medicina/EEG (≥2σ)."""
        result = self.validator.validate_standard('medicina_eeg')
        
        self.assertEqual(result['disciplina'], 'Medicina (EEG)')
        self.assertEqual(result['umbral_requerido'], '≥ 2.0σ')
        self.assertTrue(result['cumple'])
        self.assertEqual(result['simbolo'], '✅ Cumple')
    
    def test_validate_all_standards(self):
        """Test que valida todos los estándares simultáneamente."""
        results = self.validator.validate_all_standards()
        
        # Verificar estructura del resultado
        self.assertIn('evento', results)
        self.assertIn('frecuencia_objetivo', results)
        self.assertIn('significancia_observada', results)
        self.assertIn('validaciones', results)
        self.assertIn('todas_aprobadas', results)
        self.assertIn('conclusion', results)
        
        # Verificar que todas las disciplinas están validadas
        self.assertIn('fisica_particulas', results['validaciones'])
        self.assertIn('astronomia', results['validaciones'])
        self.assertIn('medicina_eeg', results['validaciones'])
        
        # Verificar que todas pasan
        self.assertTrue(results['todas_aprobadas'])
        
        # Verificar que cada validación individual pasa
        for discipline, validation in results['validaciones'].items():
            self.assertTrue(validation['cumple'], 
                          f"La validación para {discipline} debe pasar")
    
    def test_conclusion_message(self):
        """Test que el mensaje de conclusión es correcto."""
        results = self.validator.validate_all_standards()
        
        expected_conclusion = (
            'Cumple los estándares de descubrimiento aceptados en todas las disciplinas científicas.'
        )
        self.assertEqual(results['conclusion'], expected_conclusion)
    
    def test_confidence_levels(self):
        """Test que los niveles de confianza son correctos."""
        # Física de partículas: 5σ ≈ 99.99994%
        fisica = self.validator.standards['fisica_particulas']
        self.assertEqual(fisica['confianza_porcentaje'], 99.99994)
        
        # Astronomía: 3σ ≈ 99.7%
        astronomia = self.validator.standards['astronomia']
        self.assertEqual(astronomia['confianza_porcentaje'], 99.7)
        
        # Medicina: 2σ ≈ 95.4%
        medicina = self.validator.standards['medicina_eeg']
        self.assertEqual(medicina['confianza_porcentaje'], 95.4)
    
    def test_save_validation_report(self):
        """Test que se guarda correctamente el reporte de validación."""
        # Crear directorio temporal para test
        test_output = 'results/test_discovery_standards_output.json'
        
        # Guardar reporte
        results = self.validator.save_validation_report(test_output)
        
        # Verificar que el archivo existe
        self.assertTrue(Path(test_output).exists())
        
        # Verificar que es JSON válido
        with open(test_output, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertIn('validaciones', data)
            self.assertTrue(data['todas_aprobadas'])
        
        # Limpiar archivo de test
        Path(test_output).unlink(missing_ok=True)
    
    def test_invalid_discipline(self):
        """Test que se maneja correctamente una disciplina inválida."""
        with self.assertRaises(ValueError):
            self.validator.validate_standard('disciplina_inexistente')
    
    def test_event_information(self):
        """Test que la información del evento es correcta."""
        results = self.validator.validate_all_standards()
        
        self.assertEqual(results['evento'], 'GW150914')
        self.assertEqual(results['frecuencia_objetivo'], 141.7001)
        self.assertGreater(results['significancia_observada'], 10.0)
        self.assertLess(results['p_value'], 1e-10)


class TestDiscoveryStandardsIntegration(unittest.TestCase):
    """Tests de integración para el sistema de validación."""
    
    def test_complete_validation_workflow(self):
        """Test del flujo completo de validación."""
        validator = DiscoveryStandardsValidator()
        
        # 1. Validar todos los estándares
        results = validator.validate_all_standards()
        self.assertTrue(results['todas_aprobadas'])
        
        # 2. Verificar que cada disciplina cumple individualmente
        for discipline in ['fisica_particulas', 'astronomia', 'medicina_eeg']:
            individual = validator.validate_standard(discipline)
            self.assertTrue(individual['cumple'])
        
        # 3. Guardar reporte
        test_output = 'results/test_integration_output.json'
        validator.save_validation_report(test_output)
        
        # 4. Verificar archivo generado
        self.assertTrue(Path(test_output).exists())
        
        # Limpiar
        Path(test_output).unlink(missing_ok=True)
    
    def test_standards_hierarchy(self):
        """Test que los estándares están ordenados correctamente por rigurosidad."""
        validator = DiscoveryStandardsValidator()
        
        # Física de partículas es el más riguroso (5σ)
        # Astronomía es intermedio (3σ)
        # Medicina es el menos riguroso (2σ)
        
        fisica_sigma = validator.standards['fisica_particulas']['umbral_sigma']
        astro_sigma = validator.standards['astronomia']['umbral_sigma']
        medicina_sigma = validator.standards['medicina_eeg']['umbral_sigma']
        
        self.assertGreater(fisica_sigma, astro_sigma)
        self.assertGreater(astro_sigma, medicina_sigma)
        
        # Si cumple el más riguroso, debe cumplir todos
        observed = validator.observed_results['significancia_sigma']
        if observed >= fisica_sigma:
            self.assertGreaterEqual(observed, astro_sigma)
            self.assertGreaterEqual(observed, medicina_sigma)


def run_tests():
    """Ejecutar todos los tests."""
    # Crear directorio de resultados si no existe
    Path('results').mkdir(exist_ok=True)
    
    # Ejecutar tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDiscoveryStandardsValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestDiscoveryStandardsIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
