#!/usr/bin/env python3
"""
Tests for Experimental Convergence Validation
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.validacion_convergencia_experimental import (
    MagnetoreceptionValidator,
    MicrotubuleValidator,
    RNARiemannWaveValidator,
    ConvergenceAnalyzer
)

try:
    from qcal.constants import F0_HZ, MAGNETORECEPTION_ASYMMETRY
except ImportError:
    F0_HZ = 141.7001
    MAGNETORECEPTION_ASYMMETRY = 0.002


class TestMagnetoreceptionValidator(unittest.TestCase):
    """Test magnetoreception validation"""
    
    def setUp(self):
        self.validator = MagnetoreceptionValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.asymmetry_theoretical, MAGNETORECEPTION_ASYMMETRY)
        self.assertAlmostEqual(self.validator.asymmetry_measured, 0.001987, places=6)
    
    def test_significance_calculation(self):
        """Test statistical significance calculation"""
        # Use large n_trials for high sigma
        result = self.validator.calculate_significance(delta_P=0.002, n_trials=5000000)
        
        # Should have high sigma (>5)
        self.assertGreater(result['sigma'], 5.0)
        
        # P-value should be very small
        self.assertLess(result['p_value'], 1e-6)
        
        # Check required fields
        self.assertIn('sigma', result)
        self.assertIn('p_value', result)
        self.assertIn('confidence_level', result)
    
    def test_asymmetry_validation(self):
        """Test asymmetry validation"""
        result = self.validator.validate_asymmetry()
        
        # Error should be small
        self.assertLess(result['error_relative'], 0.1)  # <10% error
        
        # Should be valid
        self.assertTrue(result['is_valid'])
        
        # Check status
        self.assertIn('✓', result['validation_status'])
    
    def test_angular_dependence(self):
        """Test angular dependence calculation"""
        theta = np.array([0, 45, 90, 135, 180])
        P_theta = self.validator.angular_dependence(theta)
        
        # Should have correct shape
        self.assertEqual(len(P_theta), len(theta))
        
        # Max at 0°, min at 90°
        self.assertGreater(P_theta[0], P_theta[2])
        
        # All probabilities should be between 0 and 1
        self.assertTrue(np.all(P_theta >= 0))
        self.assertTrue(np.all(P_theta <= 1))
    
    def test_full_validation(self):
        """Test complete validation"""
        result = self.validator.validate()
        
        # Check main sections
        self.assertIn('significance', result)
        self.assertIn('asymmetry', result)
        self.assertIn('angular_modulation', result)
        
        # Significance should be high
        self.assertGreater(result['significance']['sigma'], 5.0)
        
        # Should show confirmed discovery
        self.assertIn('CONFIRMADO', result['validation_status'])


class TestMicrotubuleValidator(unittest.TestCase):
    """Test microtubule resonance validation"""
    
    def setUp(self):
        self.validator = MicrotubuleValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.f_theoretical, F0_HZ)
        self.assertAlmostEqual(self.validator.f_measured, 141.88, places=2)
    
    def test_precision_calculation(self):
        """Test precision calculation"""
        result = self.validator.calculate_precision()
        
        # Precision should be very high (>99%)
        self.assertGreater(result['precision_percent'], 99.0)
        
        # Error should be small (<1%)
        self.assertLess(result['error_relative_percent'], 1.0)
        
        # Check required fields
        self.assertIn('f_theoretical_Hz', result)
        self.assertIn('f_measured_Hz', result)
        self.assertIn('precision_percent', result)
    
    def test_bandwidth_validation(self):
        """Test bandwidth validation"""
        result = self.validator.validate_bandwidth()
        
        # f0 should be in bandwidth
        self.assertTrue(result['f0_in_bandwidth'])
        
        # Measured frequency should be in bandwidth
        self.assertTrue(result['f_measured_in_bandwidth'])
        
        # Check status
        self.assertIn('✓', result['validation_status'])
    
    def test_biological_signature(self):
        """Test biological signature analysis"""
        result = self.validator.biological_signature()
        
        # Error should be within biological range
        self.assertLess(result['error_Hz'], result['bio_variability_max_Hz'])
        
        # Should be bio-compatible
        self.assertTrue(result['is_bio_compatible'])
        
        # Check interpretation
        self.assertIn('Vida', result['interpretation'])
    
    def test_full_validation(self):
        """Test complete validation"""
        result = self.validator.validate()
        
        # Check main sections
        self.assertIn('precision', result)
        self.assertIn('bandwidth', result)
        self.assertIn('biological_signature', result)
        
        # Should be valid
        self.assertIn('✓', result['validation_status'])


class TestRNARiemannWaveValidator(unittest.TestCase):
    """Test RNA-Riemann wave validation"""
    
    def setUp(self):
        self.validator = RNARiemannWaveValidator()
    
    def test_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.f0, F0_HZ)
    
    def test_codon_frequency_sum(self):
        """Test codon frequency sum calculation"""
        freq_sum = self.validator.calculate_codon_frequency_sum()
        
        # Should be positive
        self.assertGreater(freq_sum, 0)
        
        # Should be reasonable value (in Hz)
        self.assertGreater(freq_sum, 100)
        self.assertLess(freq_sum, 10000)
    
    def test_ratio_calculation(self):
        """Test ratio to f0 calculation"""
        result = self.validator.calculate_ratio_to_f0()
        
        # Check required fields
        self.assertIn('ratio', result)
        self.assertIn('ratio_expected', result)
        self.assertIn('error_relative', result)
        
        # Ratio should be positive
        self.assertGreater(result['ratio'], 0)
    
    def test_genetic_code_design(self):
        """Test genetic code design validation"""
        result = self.validator.validate_genetic_code_design()
        
        # Check required fields
        self.assertIn('codon', result)
        self.assertIn('amino_acid', result)
        self.assertIn('is_valid', result)
        
        # Codon should be AAA
        self.assertEqual(result['codon'], 'AAA')
        
        # Should code for Lysine
        self.assertIn('Lysine', result['amino_acid'])
    
    def test_full_validation(self):
        """Test complete validation"""
        result = self.validator.validate()
        
        # Check main sections
        self.assertIn('ratio_analysis', result)
        self.assertIn('genetic_code_design', result)
        
        # Check f0 coupling
        self.assertEqual(result['f0_coupling_Hz'], F0_HZ)


class TestConvergenceAnalyzer(unittest.TestCase):
    """Test convergence analyzer"""
    
    def setUp(self):
        self.analyzer = ConvergenceAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.magnetoreception)
        self.assertIsNotNone(self.analyzer.microtubule)
        self.assertIsNotNone(self.analyzer.rna_riemann)
    
    def test_integration_matrix(self):
        """Test integration matrix generation"""
        result = self.analyzer.generate_integration_matrix()
        
        # Should have all four nodes
        self.assertIn('matematico', result)
        self.assertIn('teorico', result)
        self.assertIn('biologico', result)
        self.assertIn('cuantico', result)
        
        # Each node should have required fields
        for nodo, data in result.items():
            self.assertIn('fuente', data)
            self.assertIn('valor', data)
            self.assertIn('estado', data)
            self.assertIn('tipo', data)
    
    def test_cross_validation(self):
        """Test cross-validation calculation"""
        result = self.analyzer.calculate_cross_validation()
        
        # Check required fields
        self.assertIn('num_validations_total', result)
        self.assertIn('num_validations_passed', result)
        self.assertIn('convergence_ratio', result)
        
        # Should have 3 validations
        self.assertEqual(result['num_validations_total'], 3)
        
        # Convergence should be between 0 and 1
        self.assertGreaterEqual(result['convergence_ratio'], 0)
        self.assertLessEqual(result['convergence_ratio'], 1)
    
    def test_validate_all(self):
        """Test complete validation (without printing)"""
        # Redirect stdout to suppress prints
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            result = self.analyzer.validate_all()
        
        # Check all main sections
        self.assertIn('magnetoreception', result)
        self.assertIn('microtubule', result)
        self.assertIn('rna_riemann', result)
        self.assertIn('integration_matrix', result)
        self.assertIn('cross_validation', result)
        
        # Should be complete
        self.assertTrue(result['validation_complete'])
        
        # Should have f0
        self.assertEqual(result['f0_Hz'], F0_HZ)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("TESTING: Experimental Convergence Validation")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMagnetoreceptionValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestMicrotubuleValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestRNARiemannWaveValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestConvergenceAnalyzer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
