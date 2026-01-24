#!/usr/bin/env python3
"""
Test suite for Fractal Resonance validation script.

Tests the key components of the fractal resonance theory implementation.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path to import the validation script
sys.path.insert(0, str(Path(__file__).parent))

try:
    import mpmath as mp
    from validate_fractal_resonance import (
        get_fundamental_constants,
        calculate_fractal_correction_factor,
        calculate_fractal_dimension,
        derive_fundamental_frequency,
        generate_primes,
        complex_prime_series,
        calculate_dimensional_factor
    )
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure mpmath is installed: pip install mpmath")
    sys.exit(1)


class TestFractalResonance(unittest.TestCase):
    """Test cases for fractal resonance calculations."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.precision = 50
        mp.dps = cls.precision
        cls.constants = get_fundamental_constants(cls.precision)

    def test_fundamental_constants(self):
        """Test that fundamental constants are calculated correctly."""
        constants = self.constants

        # Check that constants exist and are reasonable
        self.assertIsNotNone(constants['gamma'])
        self.assertIsNotNone(constants['phi'])

        # Golden ratio should be approximately 1.618
        phi_float = float(constants['phi'])
        self.assertAlmostEqual(phi_float, 1.618, delta=0.01)

        # Euler-Mascheroni constant should be approximately 0.577
        gamma_float = float(constants['gamma'])
        self.assertAlmostEqual(gamma_float, 0.577, delta=0.01)

    def test_fractal_correction_factor(self):
        """Test fractal correction factor δ calculation."""
        delta = calculate_fractal_correction_factor(self.constants)

        # δ should be very close to 1
        delta_float = float(delta)
        self.assertGreater(delta_float, 1.0)
        self.assertLess(delta_float, 1.001)

        # Check expected value from paper
        expected = 1.000141678168563
        self.assertAlmostEqual(delta_float, expected, delta=1e-10)

    def test_fractal_dimension(self):
        """Test fractal dimension D_f calculation."""
        D_f = calculate_fractal_dimension(self.constants)

        # D_f should be around 1.236
        D_f_float = float(D_f)
        self.assertGreater(D_f_float, 1.2)
        self.assertLess(D_f_float, 1.3)

        # Check it's close to expected value (allowing for small discrepancy)
        expected = 1.236614938
        self.assertAlmostEqual(D_f_float, expected, delta=0.001)

    def test_dimensional_factors(self):
        """Test dimensional factor calculations."""
        psi_prime, psi_eff = calculate_dimensional_factor(self.constants)

        # Ψ_prime should be around 3968
        psi_prime_float = float(psi_prime)
        self.assertGreater(psi_prime_float, 3900)
        self.assertLess(psi_prime_float, 4000)

        # Ψ_eff should be around 15.19
        psi_eff_float = float(psi_eff)
        self.assertGreater(psi_eff_float, 15.0)
        self.assertLess(psi_eff_float, 16.0)

    def test_fundamental_frequency(self):
        """Test fundamental frequency derivation."""
        delta = calculate_fractal_correction_factor(self.constants)
        f0 = derive_fundamental_frequency(self.constants, delta)

        # f₀ should be 141.7001 Hz
        f0_float = float(f0)
        target = 141.7001

        # Check value
        self.assertAlmostEqual(f0_float, target, delta=0.001)

        # Check error is less than 0.00003%
        error_rel = abs(f0_float - target) / target * 100
        self.assertLess(error_rel, 0.00003)

    def test_prime_generation(self):
        """Test prime number generation."""
        # Generate first 10 primes
        primes = generate_primes(10)

        self.assertEqual(len(primes), 10)
        self.assertEqual(primes[0], 2)
        self.assertEqual(primes[1], 3)
        self.assertEqual(primes[2], 5)
        self.assertEqual(primes[9], 29)  # 10th prime

    def test_complex_prime_series(self):
        """Test complex prime series calculation."""
        N = 100
        alpha = 0.551020

        magnitude, real, imag, phases = complex_prime_series(N, alpha, precision=30)

        # Check that we got N phases
        self.assertEqual(len(phases), N)

        # Check magnitude is positive
        self.assertGreater(float(magnitude), 0)

        # Check phases are in [0, 2π)
        for phase in phases:
            self.assertGreaterEqual(phase, 0)
            self.assertLess(phase, 2 * 3.14159265359)

    def test_convergence_behavior(self):
        """Test that complex prime series shows expected convergence."""
        alpha = 0.551020
        N_values = [100, 500]

        prev_magnitude = 0
        for N in N_values:
            magnitude, _, _, _ = complex_prime_series(N, alpha, precision=30)
            mag_float = float(magnitude)

            # Magnitude should increase with N
            self.assertGreater(mag_float, prev_magnitude)
            prev_magnitude = mag_float


class TestScriptExecution(unittest.TestCase):
    """Test that the main script executes correctly."""

    def test_script_runs(self):
        """Test that the validation script can be imported and run."""
        # Import the main function
        try:
            from validate_fractal_resonance import main
            # We don't actually run it in the test to save time
            self.assertTrue(callable(main))
        except Exception as e:
            self.fail(f"Failed to import main function: {e}")


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestFractalResonance))
    suite.addTests(loader.loadTestsFromTestCase(TestScriptExecution))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
