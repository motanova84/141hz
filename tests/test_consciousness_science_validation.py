#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         TEST SUITE: Consciousness Science Validation                      ║
║         Comprehensive testing of experimental convergence framework        ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Test Coverage: 28 unit tests covering all validation functions, constants,
and integration matrix properties.
"""

import sys
import os
import unittest
import numpy as np
import json
from dataclasses import asdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.consciousness_science_validation import (
    # Constants
    F0_THEORETICAL_HZ,
    F1_MANIFESTATION_HZ,
    F_PROTECTION_HZ,
    COHERENCE_TOLERANCE,
    METABOLIC_SIGNATURE_MIN_HZ,
    METABOLIC_SIGNATURE_MAX_HZ,
    MAGNETORECEPTION_ASYMMETRY_TARGET,
    TARGET_COHERENCE_AAA,
    RIEMANN_ZERO_FREQ_1,
    RIEMANN_ZERO_FREQ_2,
    RIEMANN_ZERO_FREQ_3,
    # Classes
    NumpyEncoder,
    MagnetoreceptionValidator,
    MicrotubuleResonanceValidator,
    AAACodonCoherenceValidator,
    IntegrationMatrixValidator,
    ConsciousnessScienceValidator,
    # Results
    MagnetoreceptionResult,
    MicrotubuleResonanceResult,
    AAACodonCoherenceResult,
    IntegrationNode
)


class TestConstants(unittest.TestCase):
    """Test constant definitions"""
    
    def test_f0_theoretical_value(self):
        """Test F0_THEORETICAL_HZ constant"""
        self.assertEqual(F0_THEORETICAL_HZ, 141.7001)
    
    def test_f1_manifestation_value(self):
        """Test F1_MANIFESTATION_HZ constant"""
        self.assertEqual(F1_MANIFESTATION_HZ, 141.88)
    
    def test_protection_frequency_value(self):
        """Test F_PROTECTION_HZ constant"""
        self.assertEqual(F_PROTECTION_HZ, 888.0)
    
    def test_coherence_tolerance(self):
        """Test COHERENCE_TOLERANCE constant"""
        self.assertEqual(COHERENCE_TOLERANCE, 0.05)
    
    def test_metabolic_signature_bounds(self):
        """Test metabolic signature boundaries"""
        self.assertEqual(METABOLIC_SIGNATURE_MIN_HZ, 141.5)
        self.assertEqual(METABOLIC_SIGNATURE_MAX_HZ, 142.2)
        self.assertLess(METABOLIC_SIGNATURE_MIN_HZ, F0_THEORETICAL_HZ)
        self.assertGreater(METABOLIC_SIGNATURE_MAX_HZ, F1_MANIFESTATION_HZ)
    
    def test_magnetoreception_asymmetry_target(self):
        """Test magnetoreception asymmetry target"""
        self.assertEqual(MAGNETORECEPTION_ASYMMETRY_TARGET, 0.002)
        self.assertEqual(MAGNETORECEPTION_ASYMMETRY_TARGET * 100, 0.2)  # 0.2%
    
    def test_target_coherence_aaa(self):
        """Test AAA coherence target"""
        self.assertEqual(TARGET_COHERENCE_AAA, 0.8991)


class TestNumpyEncoder(unittest.TestCase):
    """Test numpy JSON encoder"""
    
    def test_encode_numpy_int(self):
        """Test encoding numpy integers"""
        encoder = NumpyEncoder()
        data = {'value': np.int64(42)}
        json_str = json.dumps(data, cls=NumpyEncoder)
        self.assertIn('42', json_str)
    
    def test_encode_numpy_float(self):
        """Test encoding numpy floats"""
        encoder = NumpyEncoder()
        data = {'value': np.float64(3.14159)}
        json_str = json.dumps(data, cls=NumpyEncoder)
        result = json.loads(json_str)
        self.assertAlmostEqual(result['value'], 3.14159, places=5)
    
    def test_encode_numpy_array(self):
        """Test encoding numpy arrays"""
        encoder = NumpyEncoder()
        data = {'array': np.array([1, 2, 3])}
        json_str = json.dumps(data, cls=NumpyEncoder)
        result = json.loads(json_str)
        self.assertEqual(result['array'], [1, 2, 3])
    
    def test_encode_numpy_bool(self):
        """Test encoding numpy booleans"""
        encoder = NumpyEncoder()
        data = {'flag': np.bool_(True)}
        json_str = json.dumps(data, cls=NumpyEncoder)
        result = json.loads(json_str)
        self.assertEqual(result['flag'], True)


class TestMagnetoreceptionValidator(unittest.TestCase):
    """Test magnetoreception validation"""
    
    def setUp(self):
        self.validator = MagnetoreceptionValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.name, "Avian Magnetoreception - Radical Pair Mechanism")
        self.assertEqual(self.validator.asymmetry_measured, 0.001987)
        self.assertEqual(self.validator.asymmetry_theoretical, 0.002)
    
    def test_calculate_sigma_significance(self):
        """Test sigma calculation"""
        result = self.validator.calculate_sigma_significance(
            delta_P=0.002,
            n_trials=5000000
        )
        
        # Should have high sigma
        self.assertGreater(result['sigma'], 8.0)
        self.assertIn('p_value', result)
        self.assertIn('std_error', result)
        self.assertLess(result['p_value'], 1e-9)
    
    def test_validate_returns_correct_type(self):
        """Test validate returns MagnetoreceptionResult"""
        result = self.validator.validate()
        self.assertIsInstance(result, MagnetoreceptionResult)
    
    def test_validate_sigma_threshold(self):
        """Test sigma exceeds 8.7 threshold"""
        result = self.validator.validate()
        self.assertGreater(result.sigma, 8.7)
        self.assertGreater(result.sigma, 9.0)  # Should be around 9.2
    
    def test_validate_p_value(self):
        """Test p-value is extremely small"""
        result = self.validator.validate()
        self.assertLess(result.p_value, 1e-9)
    
    def test_validate_asymmetry_accuracy(self):
        """Test asymmetry measurement accuracy"""
        result = self.validator.validate()
        self.assertAlmostEqual(result.asymmetry_measured, 0.001987, places=6)
        self.assertLess(result.error_relative, 0.05)  # < 5% error
    
    def test_validate_is_valid_flag(self):
        """Test validation flag is True"""
        result = self.validator.validate()
        self.assertTrue(result.is_valid)
        self.assertIn('✓', result.significance_status)


class TestMicrotubuleResonanceValidator(unittest.TestCase):
    """Test microtubule resonance validation"""
    
    def setUp(self):
        self.validator = MicrotubuleResonanceValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.f_theoretical, F0_THEORETICAL_HZ)
        self.assertEqual(self.validator.f_measured, F1_MANIFESTATION_HZ)
    
    def test_calculate_precision(self):
        """Test precision calculation"""
        result = self.validator.calculate_precision()
        
        self.assertIn('precision_percent', result)
        self.assertGreater(result['precision_percent'], 99.8)
        self.assertLess(result['error_Hz'], 0.2)
    
    def test_precision_target(self):
        """Test precision meets 99.873% target"""
        result = self.validator.calculate_precision()
        self.assertGreater(result['precision_percent'], 99.87)
    
    def test_calculate_sigma(self):
        """Test sigma calculation from measurement error"""
        error = 0.18  # Hz
        sigma = self.validator.calculate_sigma(error)
        
        # Should be around 8.7
        self.assertGreater(sigma, 7.0)
        self.assertLess(sigma, 10.0)
    
    def test_validate_returns_correct_type(self):
        """Test validate returns MicrotubuleResonanceResult"""
        result = self.validator.validate()
        self.assertIsInstance(result, MicrotubuleResonanceResult)
    
    def test_validate_sigma_threshold(self):
        """Test sigma exceeds 8.7 threshold"""
        result = self.validator.validate()
        self.assertGreater(result.sigma, 8.7)
    
    def test_validate_is_valid_flag(self):
        """Test validation flag is True"""
        result = self.validator.validate()
        self.assertTrue(result.is_valid)
        self.assertIn('✓', result.validation_status)
    
    def test_bandwidth_encompasses_f0(self):
        """Test bandwidth encompasses theoretical frequency"""
        result = self.validator.validate()
        self.assertLessEqual(result.bandwidth_min_Hz, F0_THEORETICAL_HZ)
        self.assertGreaterEqual(result.bandwidth_max_Hz, F0_THEORETICAL_HZ)


class TestAAACodonCoherenceValidator(unittest.TestCase):
    """Test AAA codon coherence validation"""
    
    def setUp(self):
        self.validator = AAACodonCoherenceValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.f0, F0_THEORETICAL_HZ)
        self.assertEqual(self.validator.f1, F1_MANIFESTATION_HZ)
        self.assertEqual(self.validator.target_coherence, TARGET_COHERENCE_AAA)
    
    def test_riemann_zero_frequencies(self):
        """Test Riemann zero frequency values"""
        self.assertEqual(self.validator.freq1, RIEMANN_ZERO_FREQ_1)
        self.assertEqual(self.validator.freq2, RIEMANN_ZERO_FREQ_2)
        self.assertEqual(self.validator.freq3, RIEMANN_ZERO_FREQ_3)
    
    def test_calculate_rms_frequency(self):
        """Test RMS frequency calculation"""
        freq_rms = self.validator.calculate_rms_frequency()
        
        # RMS should be greater than arithmetic mean for positive values
        freq_mean = (self.validator.freq1 + self.validator.freq2 + self.validator.freq3) / 3
        self.assertGreater(freq_rms, freq_mean)
        
        # RMS formula validation
        expected_rms = np.sqrt((self.validator.freq1**2 + 
                               self.validator.freq2**2 + 
                               self.validator.freq3**2) / 3)
        self.assertAlmostEqual(freq_rms, expected_rms, places=6)
    
    def test_calculate_coherence(self):
        """Test coherence calculation"""
        result = self.validator.calculate_coherence()
        
        self.assertIn('freq_rms', result)
        self.assertIn('A_eff', result)
        self.assertIn('coherence_aaa', result)
        self.assertIn('error_relative', result)
    
    def test_coherence_value_close_to_target(self):
        """Test coherence value is close to 0.8991"""
        result = self.validator.calculate_coherence()
        
        # Should be close to 0.8991 (within 5% tolerance)
        self.assertLess(result['error_relative'], COHERENCE_TOLERANCE)
        self.assertGreater(result['coherence_aaa'], 0.85)
        self.assertLess(result['coherence_aaa'], 0.95)
    
    def test_validate_returns_correct_type(self):
        """Test validate returns AAACodonCoherenceResult"""
        result = self.validator.validate()
        self.assertIsInstance(result, AAACodonCoherenceResult)
    
    def test_validate_is_valid_flag(self):
        """Test validation flag is True"""
        result = self.validator.validate()
        self.assertTrue(result.is_valid)
        self.assertIn('✓', result.validation_status)
    
    def test_a_eff_calculation(self):
        """Test A_eff calculation"""
        result = self.validator.calculate_coherence()
        freq_rms = result['freq_rms']
        expected_a_eff = freq_rms / F0_THEORETICAL_HZ
        self.assertAlmostEqual(result['A_eff'], expected_a_eff, places=6)


class TestIntegrationMatrixValidator(unittest.TestCase):
    """Test integration matrix validation"""
    
    def setUp(self):
        self.validator = IntegrationMatrixValidator()
        
        # Create mock results for testing
        self.mag_result = MagnetoreceptionResult(
            sigma=9.2,
            p_value=1.5e-10,
            asymmetry_measured=0.001987,
            asymmetry_theoretical=0.002,
            error_relative=0.0065,
            n_trials=5300000,
            is_valid=True,
            significance_status="✓ DISCOVERY"
        )
        
        self.mic_result = MicrotubuleResonanceResult(
            f_theoretical_Hz=141.7001,
            f_measured_Hz=141.88,
            precision_percent=99.873,
            error_Hz=0.1799,
            error_percent=0.127,
            sigma=8.7,
            bandwidth_min_Hz=141.7,
            bandwidth_max_Hz=142.1,
            is_valid=True,
            validation_status="✓ VALIDATED"
        )
        
        self.aaa_result = AAACodonCoherenceResult(
            freq_rms=20.5,
            A_eff=0.145,
            coherence_aaa=0.907,
            target_coherence=0.8991,
            error_relative=0.0088,
            riemann_zero_freqs=[14.134725, 21.022040, 25.010858],
            is_valid=True,
            validation_status="✓ COHERENT"
        )
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.name, "Consciousness Science Integration Matrix")
    
    def test_create_mathematical_node(self):
        """Test mathematical node creation"""
        node = self.validator.create_mathematical_node()
        self.assertIsInstance(node, IntegrationNode)
        self.assertEqual(node.name, "Mathematical")
        self.assertEqual(node.frequency_Hz, F_PROTECTION_HZ)
        self.assertEqual(node.value, "888 Hz")
        self.assertIn('✓', node.status)
    
    def test_create_theoretical_node(self):
        """Test theoretical node creation"""
        node = self.validator.create_theoretical_node()
        self.assertIsInstance(node, IntegrationNode)
        self.assertEqual(node.name, "Theoretical")
        self.assertEqual(node.frequency_Hz, F0_THEORETICAL_HZ)
        self.assertIn('✓', node.status)
    
    def test_create_biological_node(self):
        """Test biological node creation"""
        node = self.validator.create_biological_node(self.mic_result)
        self.assertIsInstance(node, IntegrationNode)
        self.assertEqual(node.name, "Biological")
        self.assertEqual(node.frequency_Hz, F1_MANIFESTATION_HZ)
        self.assertIn('✓', node.status)
    
    def test_create_quantum_node(self):
        """Test quantum node creation"""
        node = self.validator.create_quantum_node(self.mag_result)
        self.assertIsInstance(node, IntegrationNode)
        self.assertEqual(node.name, "Quantum")
        self.assertIn('ΔP', node.value)
        self.assertIn('✓', node.status)
    
    def test_validate_holoinformatic_properties(self):
        """Test holoinformatic properties validation"""
        nodes = [
            self.validator.create_mathematical_node(),
            self.validator.create_theoretical_node(),
            self.validator.create_biological_node(self.mic_result),
            self.validator.create_quantum_node(self.mag_result)
        ]
        
        result = self.validator.validate_holoinformatic_properties(nodes)
        
        self.assertIn('hierarchy_valid', result)
        self.assertIn('all_nodes_confirmed', result)
        self.assertIn('holoinformatic_coherence', result)
        self.assertTrue(result['all_nodes_confirmed'])
        self.assertEqual(result['num_nodes'], 4)
    
    def test_validate_resonant_coupling(self):
        """Test resonant coupling validation"""
        result = self.validator.validate_resonant_coupling(
            self.mic_result,
            self.aaa_result
        )
        
        self.assertIn('bio_theoretical_coupling', result)
        self.assertIn('aaa_coherence', result)
        self.assertIn('resonant_strength', result)
        self.assertIn('is_resonant', result)
    
    def test_validate_complete_matrix(self):
        """Test complete integration matrix validation"""
        result = self.validator.validate(
            self.mag_result,
            self.mic_result,
            self.aaa_result
        )
        
        self.assertIn('nodes', result)
        self.assertIn('holoinformatic_properties', result)
        self.assertIn('resonant_coupling', result)
        self.assertIn('matrix_valid', result)
        
        # Should have 4 nodes
        self.assertEqual(len(result['nodes']), 4)
    
    def test_integration_matrix_validity(self):
        """Test integration matrix overall validity"""
        result = self.validator.validate(
            self.mag_result,
            self.mic_result,
            self.aaa_result
        )
        
        self.assertTrue(result['matrix_valid'])
        self.assertIn('✓', result['validation_status'])


class TestConsciousnessScienceValidator(unittest.TestCase):
    """Test main consciousness science validator"""
    
    def setUp(self):
        self.validator = ConsciousnessScienceValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertIsNotNone(self.validator.magnetoreception)
        self.assertIsNotNone(self.validator.microtubule)
        self.assertIsNotNone(self.validator.aaa_coherence)
        self.assertIsNotNone(self.validator.integration_matrix)
    
    def test_validate_all_structure(self):
        """Test validate_all returns correct structure"""
        results = self.validator.validate_all(verbose=False)
        
        self.assertIn('magnetoreception', results)
        self.assertIn('microtubule_resonance', results)
        self.assertIn('aaa_codon_coherence', results)
        self.assertIn('integration_matrix', results)
        self.assertIn('global_validation', results)
        self.assertIn('constants', results)
        self.assertIn('timestamp', results)
    
    def test_validate_all_passes(self):
        """Test all validations pass"""
        results = self.validator.validate_all(verbose=False)
        
        self.assertTrue(results['global_validation']['all_valid'])
        self.assertEqual(results['global_validation']['num_validations'], 4)
        self.assertEqual(results['global_validation']['num_passed'], 4)
    
    def test_magnetoreception_sigma(self):
        """Test magnetoreception sigma > 8.7"""
        results = self.validator.validate_all(verbose=False)
        self.assertGreater(results['magnetoreception']['sigma'], 8.7)
    
    def test_microtubule_sigma(self):
        """Test microtubule sigma > 8.7"""
        results = self.validator.validate_all(verbose=False)
        self.assertGreater(results['microtubule_resonance']['sigma'], 8.7)
    
    def test_aaa_coherence_value(self):
        """Test AAA coherence is close to target"""
        results = self.validator.validate_all(verbose=False)
        coherence = results['aaa_codon_coherence']['coherence_aaa']
        target = results['aaa_codon_coherence']['target_coherence']
        
        # Should be within 5% of target
        error = abs(coherence - target) / target
        self.assertLess(error, COHERENCE_TOLERANCE)
    
    def test_generate_json_report(self):
        """Test JSON report generation"""
        json_str = self.validator.generate_json_report()
        
        # Should be valid JSON
        data = json.loads(json_str)
        
        self.assertIn('magnetoreception', data)
        self.assertIn('global_validation', data)
        self.assertTrue(data['global_validation']['all_valid'])
    
    def test_constants_in_results(self):
        """Test constants are included in results"""
        results = self.validator.validate_all(verbose=False)
        constants = results['constants']
        
        self.assertEqual(constants['F0_THEORETICAL_HZ'], F0_THEORETICAL_HZ)
        self.assertEqual(constants['F1_MANIFESTATION_HZ'], F1_MANIFESTATION_HZ)
        self.assertEqual(constants['F_PROTECTION_HZ'], F_PROTECTION_HZ)
        self.assertEqual(constants['COHERENCE_TOLERANCE'], COHERENCE_TOLERANCE)
        self.assertEqual(constants['METABOLIC_SIGNATURE_MIN_HZ'], METABOLIC_SIGNATURE_MIN_HZ)
        self.assertEqual(constants['METABOLIC_SIGNATURE_MAX_HZ'], METABOLIC_SIGNATURE_MAX_HZ)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
