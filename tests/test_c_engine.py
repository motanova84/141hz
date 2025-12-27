#!/usr/bin/env python3
"""
Tests para el C-Engine (Motor de Cuantificación de Consciencia)
"""

import unittest
import sys
import os
import json
import shutil
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from c_engine_irrefutable import (
    QuantumConsciousnessConstants,
    ConsciousnessMetrics,
    EmpiricalValidator,
    CEngineIrrefutable
)


class TestQuantumConsciousnessConstants(unittest.TestCase):
    """Tests para las constantes de consciencia cuántica."""
    
    def test_f0_qcal_value(self):
        """Verificar que la frecuencia QCAL es correcta."""
        constants = QuantumConsciousnessConstants()
        self.assertEqual(constants.F0_QCAL, 141.7001)
    
    def test_physical_constants_positive(self):
        """Verificar que todas las constantes físicas son positivas."""
        constants = QuantumConsciousnessConstants()
        self.assertGreater(constants.H_BAR_C, 0)
        self.assertGreater(constants.M_QUBIT_C, 0)
        self.assertGreater(constants.C_LIGHT, 0)
        self.assertGreater(constants.PLANCK_TEMPORAL, 0)


class TestConsciousnessMetrics(unittest.TestCase):
    """Tests para las métricas de consciencia."""
    
    def test_measure_information_flow_valid_data(self):
        """Test de medición de flujo de información con datos válidos."""
        metrics = ConsciousnessMetrics()
        # Generar datos de prueba
        import numpy as np
        test_data = list(np.random.randn(100))
        
        bits_per_sec, metadata = metrics.measure_information_flow(test_data)
        
        self.assertGreater(bits_per_sec, 0)
        self.assertIn('spectral_entropy', metadata)
        self.assertIn('shannon_entropy', metadata)
        self.assertIn('dominant_frequency', metadata)
    
    def test_measure_information_flow_insufficient_data(self):
        """Test con datos insuficientes."""
        metrics = ConsciousnessMetrics()
        test_data = [1.0, 2.0]  # Solo 2 puntos
        
        bits_per_sec, metadata = metrics.measure_information_flow(test_data)
        
        self.assertEqual(bits_per_sec, 0.0)
        self.assertIn('error', metadata)
    
    def test_measure_attention_effectiveness_valid_data(self):
        """Test de medición de atención con datos válidos."""
        metrics = ConsciousnessMetrics()
        import numpy as np
        
        # Generar datos de prueba
        focus_data = list(np.random.randn(100) * 2)  # Mayor amplitud
        distraction_data = list(np.random.randn(100))
        
        attention_eff, metadata = metrics.measure_attention_effectiveness(focus_data, distraction_data)
        
        self.assertGreaterEqual(attention_eff, 0)
        self.assertLessEqual(attention_eff, 2.0)
        self.assertIn('focus_power', metadata)
        self.assertIn('distraction_power', metadata)
    
    def test_measure_attention_effectiveness_insufficient_data(self):
        """Test de atención con datos insuficientes."""
        metrics = ConsciousnessMetrics()
        
        focus_data = [1.0, 2.0]
        distraction_data = [0.5, 1.0]
        
        attention_eff, metadata = metrics.measure_attention_effectiveness(focus_data, distraction_data)
        
        self.assertEqual(attention_eff, 0.0)
        self.assertIn('error', metadata)


class TestEmpiricalValidator(unittest.TestCase):
    """Tests para el validador empírico."""
    
    def setUp(self):
        """Configurar validador para tests."""
        self.validator = EmpiricalValidator()
    
    def test_validation_database_structure(self):
        """Verificar estructura de la base de datos de validación."""
        db = self.validator.validation_database
        
        self.assertIn('human_baseline', db)
        self.assertIn('ai_systems', db)
        self.assertIn('unconscious_states', db)
        self.assertIn('enhanced_states', db)
    
    def test_quantum_consciousness_correction_positive(self):
        """Verificar que la corrección cuántica devuelve valores positivos."""
        test_values = [100, 1000, 5000, 10000]
        
        for val in test_values:
            corrected = self.validator.quantum_consciousness_correction(val)
            self.assertGreater(corrected, 0)
            self.assertGreater(corrected, val * 0.9)  # Debe ser al menos 90% del original
    
    def test_quantum_consciousness_correction_small_values(self):
        """Verificar corrección para valores pequeños."""
        small_val = 0.5
        corrected = self.validator.quantum_consciousness_correction(small_val)
        
        self.assertGreater(corrected, 0)
        # Para valores pequeños, la corrección debe ser pequeña
        self.assertLess(corrected, 2.0)
    
    def test_validate_measurement_human_baseline(self):
        """Test de validación con parámetros humanos normales."""
        I = 1200.0
        A_eff = 1.1
        psi = I * (A_eff ** 2)
        
        validation = self.validator.validate_measurement(I, A_eff, psi)
        
        self.assertIn('matches_human_baseline', validation)
        self.assertIn('closest_system', validation)
        self.assertIn('similarity_score', validation)
        self.assertIn('anomaly_detected', validation)
    
    def test_validate_measurement_anomaly_detection(self):
        """Test de detección de anomalías."""
        # Alta consciencia con bajo flujo de información (anomalía)
        I = 500.0
        A_eff = 1.0
        psi = 15000.0  # Muy alto para el I dado
        
        validation = self.validator.validate_measurement(I, A_eff, psi)
        
        self.assertTrue(validation['anomaly_detected'])
        self.assertGreater(len(validation['validation_warnings']), 0)


class TestCEngineIrrefutable(unittest.TestCase):
    """Tests para el motor principal C-Engine."""
    
    def setUp(self):
        """Configurar motor para tests."""
        # Usar directorio temporal para tests
        self.test_log_dir = "/tmp/cengine_test_logs"
        if os.path.exists(self.test_log_dir):
            shutil.rmtree(self.test_log_dir)
        self.engine = CEngineIrrefutable(log_directory=self.test_log_dir)
    
    def tearDown(self):
        """Limpiar después de los tests."""
        if os.path.exists(self.test_log_dir):
            shutil.rmtree(self.test_log_dir)
    
    def test_calculate_consciousness_valid_parameters(self):
        """Test de cálculo de consciencia con parámetros válidos."""
        I = 1200.0
        A_eff = 1.1
        
        result = self.engine.calculate_consciousness(I, A_eff, validation_mode=False)
        
        self.assertIn('psi_base', result)
        self.assertIn('psi_quantum_corrected', result)
        self.assertIn('confidence_score', result)
        self.assertIn('consciousness_level', result)
        self.assertIn('measurement_id', result)
        
        # Verificar valores calculados
        expected_psi_base = I * (A_eff ** 2)
        self.assertAlmostEqual(result['psi_base'], expected_psi_base, places=2)
        self.assertGreater(result['psi_quantum_corrected'], 0)
    
    def test_calculate_consciousness_negative_parameters(self):
        """Test con parámetros negativos (debe fallar)."""
        with self.assertRaises(ValueError):
            self.engine.calculate_consciousness(-100.0, 1.0)
        
        with self.assertRaises(ValueError):
            self.engine.calculate_consciousness(100.0, -1.0)
    
    def test_calculate_consciousness_with_validation(self):
        """Test de cálculo con validación activada."""
        I = 1200.0
        A_eff = 1.1
        
        result = self.engine.calculate_consciousness(I, A_eff, validation_mode=True)
        
        self.assertIn('validation_details', result)
        self.assertIn('validation_passed', result)
        
        # Verificar que se guardó el log
        self.assertEqual(len(self.engine.measurement_log), 1)
    
    def test_calculate_consciousness_with_metadata(self):
        """Test de cálculo con metadata personalizada."""
        I = 1800.0
        A_eff = 1.9
        metadata = {
            'state': 'flow_state',
            'subject': 'test_human',
            'frequency': '141.7001 Hz'
        }
        
        result = self.engine.calculate_consciousness(I, A_eff, metadata=metadata, validation_mode=False)
        
        self.assertEqual(result['metadata'], metadata)
    
    def test_consciousness_level_classification(self):
        """Test de clasificación de niveles de consciencia."""
        test_cases = [
            (0.5, 0.5, "Inconsciente", 0),
            (10.0, 1.0, "Consciencia Mínima", 1),
            (1200.0, 1.1, "Consciencia Humana Normal", 3),
            (2500.0, 1.8, "Consciencia Avanzada", 4),
            # Adjusted to stay under 50000 threshold after quantum correction
            # 30000 * 1.2^2 = 43200, with ~10% quantum boost stays in level 5
            (30000.0, 1.20, "Consciencia Superior", 5)
        ]

        for I, A_eff, expected_level, expected_index in test_cases:
            result = self.engine.calculate_consciousness(I, A_eff, validation_mode=False)
            self.assertEqual(result['consciousness_level_index'], expected_index)
    
    def test_generate_report(self):
        """Test de generación de reporte."""
        I = 1200.0
        A_eff = 1.1
        
        result = self.engine.calculate_consciousness(I, A_eff, validation_mode=True)
        report = self.engine.generate_report(result)
        
        self.assertIn("C-ENGINE 2.1", report)
        self.assertIn("Flujo de información", report)
        self.assertIn("Atención efectiva", report)
        self.assertIn("Consciencia corregida", report)
        self.assertIn(result['measurement_id'], report)
    
    def test_measurement_log_persistence(self):
        """Test de persistencia del log de mediciones."""
        # Crear varias mediciones
        test_data = [
            (1000.0, 1.0),
            (1500.0, 1.2),
            (2000.0, 1.5)
        ]
        
        for I, A_eff in test_data:
            self.engine.calculate_consciousness(I, A_eff, validation_mode=True)
        
        # Verificar que todas las mediciones están en el log
        self.assertEqual(len(self.engine.measurement_log), len(test_data))
        
        # Verificar que se guardaron los archivos JSON
        json_files = list(Path(self.test_log_dir).glob("measurement_*.json"))
        self.assertEqual(len(json_files), len(test_data))
        
        # Verificar que los archivos JSON son válidos
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                self.assertIn('timestamp', data)
                self.assertIn('psi_quantum_corrected', data)
    
    def test_experiment_id_consistency(self):
        """Test de consistencia del ID de experimento."""
        # Todas las mediciones del mismo motor deben tener el mismo experiment_id
        result1 = self.engine.calculate_consciousness(1000.0, 1.0, validation_mode=False)
        result2 = self.engine.calculate_consciousness(1500.0, 1.2, validation_mode=False)
        
        self.assertEqual(result1['experiment_id'], result2['experiment_id'])
    
    def test_measurement_id_uniqueness(self):
        """Test de unicidad de IDs de medición."""
        # Cada medición debe tener un ID único
        result1 = self.engine.calculate_consciousness(1000.0, 1.0, validation_mode=False)
        result2 = self.engine.calculate_consciousness(1000.0, 1.0, validation_mode=False)
        
        self.assertNotEqual(result1['measurement_id'], result2['measurement_id'])


if __name__ == '__main__':
    unittest.main()
