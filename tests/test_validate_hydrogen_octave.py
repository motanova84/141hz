#!/usr/bin/env python3
"""
Tests for Hydrogen 21cm → f₀ Quantum Phase Progression Validation
==================================================================

This test suite validates the validation script for the hydrogen line
octave relationship with f₀.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import sys
import json
import unittest
from pathlib import Path
import numpy as np

# Import the validation module from core directory
try:
    import core.validate_hydrogen_octave_relationship as vhor
except ImportError:
    # If running from different directory, try to add parent to path
    repo_root = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_root))
    sys.path.insert(0, str(repo_root / 'core'))
    import validate_hydrogen_octave_relationship as vhor


class TestOctaveCalculations(unittest.TestCase):
    """Test octave calculation functions."""
    
    def test_octave_calculation_basic(self):
        """Test basic octave calculation."""
        # 2 octaves = factor of 4
        result = vhor.calculate_octaves(400.0, 100.0, precision=50)
        self.assertAlmostEqual(result['octaves'], 2.0, places=6)
        self.assertEqual(result['whole_octaves'], 2)
        
    def test_octave_calculation_fractional(self):
        """Test fractional octave calculation."""
        # 2.5 octaves ≈ factor of 5.657
        result = vhor.calculate_octaves(565.685, 100.0, precision=50)
        self.assertAlmostEqual(result['octaves'], 2.5, places=2)
        
    def test_hydrogen_f0_octaves(self):
        """Test the exact hydrogen-f₀ octave relationship."""
        f_h = vhor.F_HYDROGEN_HZ
        f_0 = vhor.F0_HZ
        
        result = vhor.calculate_octaves(f_h, f_0, precision=100)
        
        # Should be approximately 23.257 octaves
        self.assertGreater(result['octaves'], 23.2)
        self.assertLess(result['octaves'], 23.3)
        
        # Check that it's the specific value mentioned in the problem
        self.assertAlmostEqual(result['octaves'], 23.2570, places=3)


class TestHydrogenRelationship(unittest.TestCase):
    """Test hydrogen-f₀ relationship validation."""
    
    def test_validate_hydrogen_f0_relationship(self):
        """Test complete hydrogen-f₀ validation."""
        result = vhor.validate_hydrogen_f0_relationship(precision=100)
        
        # Check required keys exist
        self.assertIn('hydrogen_line_hz', result)
        self.assertIn('f0_hz', result)
        self.assertIn('octave_relationship', result)
        self.assertIn('is_exact_match', result)
        
        # Check values
        self.assertEqual(result['f0_hz'], vhor.F0_HZ)
        self.assertEqual(result['hydrogen_line_hz'], vhor.F_HYDROGEN_HZ)
        
        # Check octave relationship
        octave_data = result['octave_relationship']
        self.assertGreater(octave_data['octaves'], 23.2)
        self.assertLess(octave_data['octaves'], 23.3)
        
    def test_exact_match_criterion(self):
        """Test that the exact match criterion is reasonable."""
        result = vhor.validate_hydrogen_f0_relationship(precision=100)
        
        # Should match within measurement precision
        octave_data = result['octave_relationship']
        fractional = octave_data['fractional_octave']
        
        # Fractional part should be close to 0.257
        self.assertAlmostEqual(fractional, 0.257, places=2)


class TestMathematicalMatrix(unittest.TestCase):
    """Test mathematical matrix validation."""
    
    def test_schumann_relation(self):
        """Test Schumann resonance relation (f₀/18 ≈ 7.83 Hz)."""
        result = vhor.validate_mathematical_matrix(precision=100)
        
        schumann = result['schumann_relation']
        
        # Should be very close to 7.83 Hz
        self.assertAlmostEqual(schumann['calculated_hz'], 7.83, places=1)
        
        # Precision should be > 99%
        self.assertGreater(schumann['precision_percent'], 99.0)
        
    def test_sacred_geometry(self):
        """Test sacred geometry relation (888/f₀ ≈ 2π)."""
        result = vhor.validate_mathematical_matrix(precision=100)
        
        sacred = result['sacred_geometry']
        
        # Should be very close to 2π
        two_pi = 2 * np.pi
        self.assertAlmostEqual(sacred['calculated'], two_pi, places=1)
        
        # Precision should be > 99%
        self.assertGreater(sacred['precision_percent'], 99.0)
        
    def test_matrix_sum_perfect_square(self):
        """Test that matrix sum is a perfect square (361 = 19²)."""
        result = vhor.validate_mathematical_matrix(precision=100)
        
        matrix_sum = result['matrix_sum']
        
        # Should be 361
        self.assertEqual(matrix_sum['sum'], 361)
        
        # Should be a perfect square
        self.assertTrue(matrix_sum['is_perfect_square'])
        
        # Square root should be 19
        self.assertEqual(matrix_sum['sqrt'], 19)
        
    def test_statistical_significance(self):
        """Test statistical significance calculation."""
        result = vhor.validate_mathematical_matrix(precision=100)
        
        stats = result['statistical_significance']
        
        # Combined p-value should be very small
        self.assertLess(stats['p_combined'], 1e-6)
        
        # Sigma equivalent should be high (approaching 9σ)
        self.assertGreater(stats['sigma_equivalent'], 5.0)
        
    def test_all_validated_flag(self):
        """Test that all_validated flag is set correctly."""
        result = vhor.validate_mathematical_matrix(precision=100)
        
        # Should be validated
        self.assertTrue(result['all_validated'])


class TestConstants(unittest.TestCase):
    """Test that fundamental constants are correct."""
    
    def test_f0_value(self):
        """Test that f₀ has the correct value."""
        self.assertEqual(vhor.F0_HZ, 141.7001)
        
    def test_hydrogen_frequency(self):
        """Test that hydrogen frequency is correct."""
        # Should be 1420.4056751 MHz
        self.assertAlmostEqual(vhor.F_HYDROGEN_MHZ, 1420.4056751, places=6)
        
        # In Hz
        expected_hz = 1420.4056751e6
        self.assertAlmostEqual(vhor.F_HYDROGEN_HZ, expected_hz, places=1)
        
    def test_schumann_frequency(self):
        """Test that Schumann frequency is correct."""
        self.assertEqual(vhor.F_SCHUMANN_HZ, 7.83)
        
    def test_sacred_constant(self):
        """Test that sacred geometry constant is correct."""
        self.assertEqual(vhor.SACRED_888, 888)


class TestDataStructure(unittest.TestCase):
    """Test that data structures are well-formed."""
    
    def test_octave_data_structure(self):
        """Test octave calculation returns proper structure."""
        result = vhor.calculate_octaves(1000.0, 100.0)
        
        required_keys = [
            'f_high_hz', 'f_low_hz', 'ratio', 'octaves', 'decades',
            'whole_octaves', 'fractional_octave', 'f_exact_octaves_hz',
            'deviation_hz', 'deviation_percent'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
            self.assertIsNotNone(result[key])
            
    def test_hydrogen_validation_structure(self):
        """Test hydrogen validation returns proper structure."""
        result = vhor.validate_hydrogen_f0_relationship(precision=50)
        
        required_keys = [
            'hydrogen_line_mhz', 'hydrogen_line_hz', 'f0_hz',
            'octave_relationship', 'is_exact_match', 'timestamp'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)
            
    def test_matrix_validation_structure(self):
        """Test matrix validation returns proper structure."""
        result = vhor.validate_mathematical_matrix(precision=50)
        
        required_keys = [
            'schumann_relation', 'sacred_geometry', 'matrix_sum',
            'statistical_significance', 'all_validated', 'timestamp'
        ]
        
        for key in required_keys:
            self.assertIn(key, result)


class TestNumericalPrecision(unittest.TestCase):
    """Test numerical precision and accuracy."""
    
    def test_high_precision_calculation(self):
        """Test that high precision calculations work."""
        result = vhor.calculate_octaves(
            vhor.F_HYDROGEN_HZ, 
            vhor.F0_HZ, 
            precision=200
        )
        
        # Should still get reasonable results
        self.assertGreater(result['octaves'], 23.0)
        self.assertLess(result['octaves'], 24.0)
        
    def test_precision_consistency(self):
        """Test that results are consistent across precision levels."""
        result_50 = vhor.calculate_octaves(
            vhor.F_HYDROGEN_HZ, 
            vhor.F0_HZ, 
            precision=50
        )
        result_100 = vhor.calculate_octaves(
            vhor.F_HYDROGEN_HZ, 
            vhor.F0_HZ, 
            precision=100
        )
        
        # Results should be very close
        self.assertAlmostEqual(
            result_50['octaves'], 
            result_100['octaves'], 
            places=4
        )


def run_tests():
    """Run all tests and return status."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
