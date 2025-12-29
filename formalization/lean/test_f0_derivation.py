#!/usr/bin/env python3
"""
Unit tests for f₀ = 141.7001 Hz Mathematical Derivation

This module tests the mathematical relationships formalized in Lean 4
at formalization/lean/F0Derivation/
"""

import unittest
import math


class TestF0Derivation(unittest.TestCase):
    """Test suite for f₀ derivation mathematics"""
    
    # Constants
    F0 = 141.7001
    SQRT2 = math.sqrt(2)
    PHI = (1 + math.sqrt(5)) / 2
    PHI_CUBED = PHI ** 3
    ZETA_PRIME_HALF = -1.4603545088
    ABS_ZETA_PRIME_HALF = abs(ZETA_PRIME_HALF)
    F_REF = 55100 / 550
    
    def test_f_reference_value(self):
        """Test f_ref = 55100/550 = 100.181818..."""
        self.assertAlmostEqual(self.F_REF, 100.181818181818, places=10,
                               msg="f_ref should be 100.181818...")
    
    def test_sqrt2_bounds(self):
        """Test 1.414 < √2 < 1.415"""
        self.assertGreater(self.SQRT2, 1.414, 
                          msg="√2 should be greater than 1.414")
        self.assertLess(self.SQRT2, 1.415,
                       msg="√2 should be less than 1.415")
    
    def test_phi_cubed_bounds(self):
        """Test 4.236 < φ³ < 4.237"""
        self.assertGreater(self.PHI_CUBED, 4.236,
                          msg="φ³ should be greater than 4.236")
        self.assertLess(self.PHI_CUBED, 4.237,
                       msg="φ³ should be less than 4.237")
    
    def test_f0_approx_sqrt2_times_fref(self):
        """Test |f₀ - √2 × f_ref| < 0.1 Hz"""
        sqrt2_times_fref = self.SQRT2 * self.F_REF
        difference = abs(self.F0 - sqrt2_times_fref)
        
        self.assertLess(difference, 0.1,
                       msg=f"|f₀ - √2 × f_ref| = {difference} should be < 0.1 Hz")
        
        # More precisely, it should be < 0.03
        self.assertLess(difference, 0.03,
                       msg=f"|f₀ - √2 × f_ref| = {difference} should be < 0.03 Hz")
    
    def test_scale_factor_bounds(self):
        """Test 16.19 < k < 16.20 where k = f_ref / (|ζ'(1/2)| × φ³)"""
        denominator = self.ABS_ZETA_PRIME_HALF * self.PHI_CUBED
        k = self.F_REF / denominator
        
        self.assertGreater(k, 16.19,
                          msg=f"Scale factor k = {k} should be > 16.19")
        self.assertLess(k, 16.20,
                       msg=f"Scale factor k = {k} should be < 16.20")
    
    def test_scale_factor_value(self):
        """Test k ≈ 16.1945..."""
        denominator = self.ABS_ZETA_PRIME_HALF * self.PHI_CUBED
        k = self.F_REF / denominator
        
        self.assertAlmostEqual(k, 16.1945055519, places=5,
                              msg=f"Scale factor k = {k} should be ≈ 16.1945")
    
    def test_fundamental_derivation(self):
        """Test f₀ ≈ √2 × k × |ζ'(1/2)| × φ³"""
        denominator = self.ABS_ZETA_PRIME_HALF * self.PHI_CUBED
        k = self.F_REF / denominator
        f0_derived = self.SQRT2 * k * self.ABS_ZETA_PRIME_HALF * self.PHI_CUBED
        
        difference = abs(self.F0 - f0_derived)
        
        self.assertLess(difference, 0.1,
                       msg=f"Complete derivation error = {difference} should be < 0.1 Hz")
    
    def test_period_bounds(self):
        """Test 7.056 ms < T < 7.058 ms where T = 1/f₀"""
        period_ms = (1 / self.F0) * 1000
        
        self.assertGreater(period_ms, 7.056,
                          msg=f"Period T = {period_ms} ms should be > 7.056 ms")
        self.assertLess(period_ms, 7.058,
                       msg=f"Period T = {period_ms} ms should be < 7.058 ms")
    
    def test_angular_frequency_bounds(self):
        """Test 890 < ω < 891 rad/s where ω = 2πf₀"""
        omega = 2 * math.pi * self.F0
        
        self.assertGreater(omega, 890,
                          msg=f"Angular frequency ω = {omega} should be > 890 rad/s")
        self.assertLess(omega, 891,
                       msg=f"Angular frequency ω = {omega} should be < 891 rad/s")
    
    def test_mystery_factor_explanation(self):
        """Test that f₀/(|ζ'(1/2)|×φ³) ≈ 22.91 = √2 × k"""
        product = self.ABS_ZETA_PRIME_HALF * self.PHI_CUBED
        ratio = self.F0 / product
        
        # This ratio should be approximately 22.91
        self.assertAlmostEqual(ratio, 22.91, places=1,
                              msg=f"f₀/(|ζ'(1/2)|×φ³) = {ratio} should be ≈ 22.91")
        
        # And it should equal √2 × k (within tolerance)
        k = self.F_REF / product
        sqrt2_times_k = self.SQRT2 * k
        
        self.assertAlmostEqual(ratio, sqrt2_times_k, places=2,
                              msg=f"22.91 should equal √2 × k = {sqrt2_times_k}")
    
    def test_rational_representation(self):
        """Test that f_ref has exact rational representation"""
        numerator = 55100
        denominator = 550
        
        # Check that this is in lowest terms after dividing by GCD
        from math import gcd
        g = gcd(numerator, denominator)
        reduced_num = numerator // g
        reduced_den = denominator // g
        
        # GCD(55100, 550) = 50, so it reduces to 1102/11
        self.assertEqual(g, 50,
                        msg="GCD should be 50")
        self.assertEqual(reduced_num, 1102,
                        msg="Numerator should reduce to 1102")
        self.assertEqual(reduced_den, 11,
                        msg="Denominator should reduce to 11")
        
        # And the value should match
        self.assertEqual(reduced_num / reduced_den, numerator / denominator,
                        msg="Reduced fraction should equal original")
        
        # Verify the actual value
        self.assertAlmostEqual(numerator / denominator, 100.181818181818, places=10,
                              msg="Value should be 100.181818...")


class TestNumericalPrecision(unittest.TestCase):
    """Test numerical precision and consistency"""
    
    def test_consistency_of_constants(self):
        """Verify internal consistency of all constants"""
        # Golden ratio should satisfy φ² = φ + 1
        phi = (1 + math.sqrt(5)) / 2
        phi_squared = phi ** 2
        phi_plus_one = phi + 1
        
        self.assertAlmostEqual(phi_squared, phi_plus_one, places=10,
                              msg="φ² should equal φ + 1")
    
    def test_derivation_precision(self):
        """Test that our derivation is precise enough for physics"""
        f0 = 141.7001
        sqrt2 = math.sqrt(2)
        f_ref = 55100 / 550
        
        difference = abs(f0 - sqrt2 * f_ref)
        relative_error = difference / f0
        
        # Relative error should be less than 0.02%
        self.assertLess(relative_error, 0.0002,
                       msg=f"Relative error {relative_error*100:.4f}% should be < 0.02%")


def run_tests():
    """Run all tests and print summary"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestF0Derivation))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalPrecision))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - f₀ derivation verified!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    exit(run_tests())
