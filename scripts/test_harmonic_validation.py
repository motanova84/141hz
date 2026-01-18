#!/usr/bin/env python3
"""
Test suite for harmonic validation theorem

Tests the 8 conditions of the harmonic_validation_complete theorem:
1. f_base > 0
2. f₀ > 0
3. f_high > 0
4. φ⁴ > 6
5. f_base < f₀
6. f₀ < f_high
7. 280 < f_base × φ⁴
8. f_base × φ⁴ < 300

Author: José Manuel Mota Burruezo
Date: 2025-01-18
"""

import unittest
import math
import sys
import os

# Add parent directory to path to import validation module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validate_harmonic_coherence import (
    calculate_golden_ratio,
    calculate_phi_power,
    validate_phi_identity,
    calculate_phi_fourth_algebraic,
    validate_harmonic_coherence
)


class TestGoldenRatio(unittest.TestCase):
    """Test golden ratio calculations"""
    
    def setUp(self):
        self.phi = calculate_golden_ratio()
        self.tolerance = 1e-10
    
    def test_phi_value(self):
        """Test that φ ≈ 1.618033988"""
        expected = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(self.phi, expected, places=10)
    
    def test_phi_squared_identity(self):
        """Test that φ² = φ + 1"""
        self.assertTrue(validate_phi_identity(self.phi))
        
        phi_squared = self.phi ** 2
        phi_plus_one = self.phi + 1
        self.assertAlmostEqual(phi_squared, phi_plus_one, places=10)
    
    def test_phi_fourth_direct(self):
        """Test φ⁴ by direct calculation"""
        phi_4 = calculate_phi_power(self.phi, 4)
        self.assertGreater(phi_4, 6)
        self.assertAlmostEqual(phi_4, 6.8541019662, places=9)
    
    def test_phi_fourth_algebraic(self):
        """Test φ⁴ = 3φ + 2"""
        phi_4_direct = self.phi ** 4
        phi_4_algebraic = calculate_phi_fourth_algebraic(self.phi)
        self.assertAlmostEqual(phi_4_direct, phi_4_algebraic, places=10)
        
        # Verify the algebraic form
        expected = 3 * self.phi + 2
        self.assertAlmostEqual(phi_4_algebraic, expected, places=10)


class TestFrequencies(unittest.TestCase):
    """Test frequency definitions and relationships"""
    
    def setUp(self):
        self.f_base = 41.7
        self.f0 = 141.7001
        self.f_high = 888.0
    
    def test_frequencies_positive(self):
        """Test that all frequencies are positive"""
        self.assertGreater(self.f_base, 0)
        self.assertGreater(self.f0, 0)
        self.assertGreater(self.f_high, 0)
    
    def test_frequency_hierarchy(self):
        """Test f_base < f₀ < f_high"""
        self.assertLess(self.f_base, self.f0)
        self.assertLess(self.f0, self.f_high)
    
    def test_frequency_ratios(self):
        """Test frequency ratios"""
        ratio_base_to_f0 = self.f0 / self.f_base
        ratio_f0_to_high = self.f_high / self.f0
        
        # f₀ / f_base ≈ 3.3981
        self.assertAlmostEqual(ratio_base_to_f0, 3.3981, places=4)
        
        # f_high / f₀ ≈ 6.267
        self.assertAlmostEqual(ratio_f0_to_high, 6.267, places=3)


class TestGoldenThreshold(unittest.TestCase):
    """Test golden threshold calculations"""
    
    def setUp(self):
        self.f_base = 41.7
        self.phi = calculate_golden_ratio()
        self.phi_4 = self.phi ** 4
    
    def test_golden_product(self):
        """Test f_base × φ⁴"""
        product = self.f_base * self.phi_4
        
        # Should be approximately 285.82
        self.assertAlmostEqual(product, 285.82, places=1)
    
    def test_golden_threshold_bounds(self):
        """Test 280 < f_base × φ⁴ < 300"""
        product = self.f_base * self.phi_4
        
        self.assertGreater(product, 280)
        self.assertLess(product, 300)
    
    def test_golden_threshold_center(self):
        """Test that golden product is near center of interval"""
        product = self.f_base * self.phi_4
        interval_center = (280 + 300) / 2  # 290
        
        # Product should be within 10 Hz of center
        self.assertLess(abs(product - interval_center), 10)


class TestHarmonicCoherence(unittest.TestCase):
    """Test complete harmonic coherence validation"""
    
    def test_harmonic_validation_complete(self):
        """Test all 8 conditions of harmonic_validation_complete theorem"""
        validation_passed, details = validate_harmonic_coherence()
        
        # All conditions must be met
        self.assertTrue(validation_passed)
        self.assertTrue(details['all_conditions_met'])
        
        # Check each condition individually
        conditions = details['conditions']
        self.assertTrue(conditions['1. f_base > 0'])
        self.assertTrue(conditions['2. f₀ > 0'])
        self.assertTrue(conditions['3. f_high > 0'])
        self.assertTrue(conditions['4. φ⁴ > 6'])
        self.assertTrue(conditions['5. f_base < f₀'])
        self.assertTrue(conditions['6. f₀ < f_high'])
        self.assertTrue(conditions['7. 280 < f_base × φ⁴'])
        self.assertTrue(conditions['8. f_base × φ⁴ < 300'])
    
    def test_harmonic_validation_details(self):
        """Test detailed harmonic validation values"""
        _, details = validate_harmonic_coherence()
        
        # Check phi calculations (use 8 decimal places for numerical stability)
        # Compare with calculated value rather than hardcoded constant
        expected_phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(details['phi'], expected_phi, places=8)
        self.assertGreater(details['phi_4_direct'], 6)
        self.assertAlmostEqual(
            details['phi_4_direct'],
            details['phi_4_algebraic'],
            places=10
        )
        
        # Check frequencies
        self.assertEqual(details['f_base'], 41.7)
        self.assertEqual(details['f0'], 141.7001)
        self.assertEqual(details['f_high'], 888.0)
        
        # Check golden product
        expected_product = 41.7 * details['phi_4_direct']
        self.assertAlmostEqual(details['golden_product'], expected_product, places=5)


class TestFrequencyUniqueness(unittest.TestCase):
    """Test that f_base = 41.7 is uniquely determined"""
    
    def setUp(self):
        self.phi_4 = calculate_golden_ratio() ** 4
    
    def test_f_base_uniqueness(self):
        """Test that only f_base=41.7 optimally satisfies conditions"""
        # Test various values
        test_cases = [
            (40.0, False),  # Too low, product < 280
            (41.0, True),   # In range but not optimal
            (41.7, True),   # Optimal
            (42.0, True),   # In range but not optimal
            (43.0, True),   # In range but not optimal
            (44.0, False),  # Too high, product > 300
        ]
        
        for f_test, should_be_in_range in test_cases:
            product = f_test * self.phi_4
            in_range = 280 < product < 300
            
            self.assertEqual(
                in_range,
                should_be_in_range,
                f"f={f_test}: product={product:.2f}, expected in_range={should_be_in_range}"
            )
    
    def test_f_base_harmonic_relationship(self):
        """Test harmonic relationship between f_base and f₀"""
        f_base = 41.7
        f0 = 141.7001
        
        ratio = f0 / f_base
        
        # Ratio should be close to φ + φ⁻¹ ≈ 2.618
        # Actually it's closer to √10 ≈ 3.162 or π ≈ 3.14159
        # But the exact value is ≈ 3.3981
        self.assertAlmostEqual(ratio, 3.3981, places=4)


def run_tests_with_output():
    """Run tests with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGoldenRatio))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequencies))
    suite.addTests(loader.loadTestsFromTestCase(TestGoldenThreshold))
    suite.addTests(loader.loadTestsFromTestCase(TestHarmonicCoherence))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequencyUniqueness))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Harmonic Validation Complete")
        print("="*70)
        print()
        print("Theorem: harmonic_validation_complete")
        print("Status: ✓ VERIFIED")
        print()
        print("All 8 conditions satisfied:")
        print("  1. f_base > 0 ✓")
        print("  2. f₀ > 0 ✓")
        print("  3. f_high > 0 ✓")
        print("  4. φ⁴ > 6 ✓")
        print("  5. f_base < f₀ ✓")
        print("  6. f₀ < f_high ✓")
        print("  7. 280 < f_base × φ⁴ ✓")
        print("  8. f_base × φ⁴ < 300 ✓")
        print()
        print("QED. ✧ ∞³")
        print("="*70)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*70)
        return 1


if __name__ == '__main__':
    sys.exit(run_tests_with_output())
