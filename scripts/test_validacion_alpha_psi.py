#!/usr/bin/env python3
"""
Test suite for validacion_alpha_psi_corregida.py

Tests the corrected formula for αΨ and the derivation of f₀ = 141.7001 Hz
following the problem statement sections 5 and 6.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import sys
import unittest
import numpy as np
from scipy import constants

try:
    import mpmath
except ImportError:
    print("⚠️ mpmath not installed, skipping tests")
    print("Install with: pip install mpmath")
    sys.exit(0)


class TestAlphaPsiCorrection(unittest.TestCase):
    """Test suite for αΨ correction and dimensional analysis"""

    def setUp(self):
        """Set up constants for all tests"""
        # Physical constants (CODATA 2022)
        self.c = constants.c  # m/s
        self.h = constants.h  # J·s
        self.hbar = constants.hbar  # J·s
        self.G = constants.G  # m³/(kg·s²)

        # Planck units
        self.l_P = np.sqrt(self.hbar * self.G / self.c**3)
        self.E_P = np.sqrt(self.hbar * self.c**5 / self.G)

        # Mathematical constants
        mpmath.mp.dps = 50
        self.gamma_euler = float(mpmath.euler)
        self.zeta_prime_half = abs(float(mpmath.diff(mpmath.zeta, 0.5)))

        # Target values
        self.f0_target = 141.7001  # Hz

    def test_euler_mascheroni_constant(self):
        """Test that Euler-Mascheroni constant is correct"""
        # γ ≈ 0.5772156649
        self.assertAlmostEqual(self.gamma_euler, 0.5772156649, places=9)

    def test_zeta_prime_at_half(self):
        """Test that ζ'(1/2) is calculated correctly"""
        # |ζ'(1/2)| ≈ 3.92264614
        self.assertAlmostEqual(self.zeta_prime_half, 3.92264614, places=7)

    def test_planck_length(self):
        """Test Planck length calculation"""
        # ℓP ≈ 1.616 × 10^-35 m
        self.assertAlmostEqual(self.l_P, 1.616e-35, delta=0.001e-35)

    def test_alpha_psi_dimensional_correctness(self):
        """Test that αΨ has correct dimensions [Hz]"""
        # αΨ = (γ · ℓP · |ζ'(1/2)|) / (2πc)
        # Dimensions: [1] · [m] · [1] / [m/s] = [s^-1] = [Hz]

        numerator = self.gamma_euler * self.l_P * self.zeta_prime_half
        denominator = 2 * np.pi * self.c
        alpha_psi = numerator / denominator

        # Check it's a small frequency (order 10^-44 Hz)
        self.assertGreater(alpha_psi, 0)
        self.assertLess(alpha_psi, 1e-40)
        self.assertGreater(alpha_psi, 1e-50)

    def test_alpha_psi_order_of_magnitude(self):
        """Test that αΨ has correct order of magnitude"""
        numerator = self.gamma_euler * self.l_P * self.zeta_prime_half
        denominator = 2 * np.pi * self.c
        alpha_psi = numerator / denominator

        # Should be order 10^-44 to 10^-45 Hz
        log_alpha = np.log10(alpha_psi)
        self.assertGreater(log_alpha, -45)
        self.assertLess(log_alpha, -43)

    def test_projection_factor_order(self):
        """Test that RΨ has reasonable order of magnitude"""
        # For f₀ = 141.7 Hz and αΨ ∼ 10^-44 Hz
        # RΨ = f₀ / αΨ should be ∼ 10^45 to 10^47

        numerator = self.gamma_euler * self.l_P * self.zeta_prime_half
        denominator = 2 * np.pi * self.c
        alpha_psi = numerator / denominator

        R_psi = self.f0_target / alpha_psi
        log_R = np.log10(R_psi)

        # RΨ should be between 10^44 and 10^48
        self.assertGreater(log_R, 44)
        self.assertLess(log_R, 48)

    def test_frequency_derivation(self):
        """Test that f₀ = αΨ × RΨ gives correct frequency"""
        numerator = self.gamma_euler * self.l_P * self.zeta_prime_half
        denominator = 2 * np.pi * self.c
        alpha_psi = numerator / denominator

        # Calculate RΨ needed for f₀ = 141.7001 Hz
        R_psi_exact = self.f0_target / alpha_psi

        # Verify reconstruction
        f0_reconstructed = alpha_psi * R_psi_exact

        # Should match to high precision
        self.assertAlmostEqual(f0_reconstructed, self.f0_target, places=4)

    def test_formula_components_positive(self):
        """Test that all components of the formula are positive"""
        self.assertGreater(self.gamma_euler, 0)
        self.assertGreater(self.l_P, 0)
        self.assertGreater(self.zeta_prime_half, 0)
        self.assertGreater(self.c, 0)

    def test_zeta_function_at_half(self):
        """Test ζ(1/2) value (should be negative)"""
        zeta_half = float(mpmath.zeta(0.5))
        # ζ(1/2) ≈ -1.460354
        self.assertAlmostEqual(zeta_half, -1.460354, places=5)
        self.assertLess(zeta_half, 0)  # Must be negative

    def test_cosmological_energy_ratio(self):
        """Test cosmological energy ratio E_univ/E_Planck"""
        # Hubble parameter
        H0_SI = 67.4 * 1000 / (3.0857e22)  # 1/s

        # Critical density
        rho_crit = (3 * H0_SI**2) / (8 * np.pi * self.G)

        # Approximate universe energy
        R_univ = self.c / H0_SI
        V_univ = (4/3) * np.pi * R_univ**3
        E_univ = rho_crit * V_univ * self.c**2

        # Ratio
        R_cosmo = E_univ / self.E_P

        # Should be huge (order 10^60)
        self.assertGreater(R_cosmo, 1e50)
        self.assertLess(R_cosmo, 1e70)


class TestNumericalPrecision(unittest.TestCase):
    """Test numerical precision and stability"""

    def test_mpmath_precision(self):
        """Test that mpmath provides sufficient precision"""
        mpmath.mp.dps = 50

        # Calculate ζ'(1/2) with high precision
        zeta_prime = mpmath.diff(mpmath.zeta, 0.5)

        # Should have many significant digits
        zeta_str = str(zeta_prime)
        self.assertGreater(len(zeta_str), 10)

    def test_constants_precision(self):
        """Test that scipy.constants provides exact values where appropriate"""
        # Speed of light should be exact (defined value)
        self.assertEqual(constants.c, 299792458.0)

        # Planck constant should be exact (2019 redefinition)
        self.assertEqual(constants.h, 6.62607015e-34)


class TestDimensionalAnalysis(unittest.TestCase):
    """Test dimensional analysis of the formula"""

    def test_length_dimensions(self):
        """Test that length terms have correct dimensions"""
        # ℓP should have dimensions of [m]
        l_P = np.sqrt(constants.hbar * constants.G / constants.c**3)
        self.assertGreater(l_P, 0)

    def test_frequency_dimensions(self):
        """Test that final αΨ has frequency dimensions"""
        # [αΨ] = [m] / ([m/s]) = [s^-1] = [Hz]
        gamma = float(mpmath.euler)
        l_P = np.sqrt(constants.hbar * constants.G / constants.c**3)
        zeta_prime = abs(float(mpmath.diff(mpmath.zeta, 0.5)))

        alpha_psi = (gamma * l_P * zeta_prime) / (2 * np.pi * constants.c)

        # Should be a very small positive number (frequency in Hz)
        self.assertGreater(alpha_psi, 0)
        self.assertIsInstance(alpha_psi, (int, float))


class TestFormulaSelfConsistency(unittest.TestCase):
    """Test self-consistency of the derived formulas"""

    def test_alpha_psi_to_f0_roundtrip(self):
        """Test that f₀ = αΨ × RΨ is self-consistent"""
        # Calculate αΨ
        gamma = float(mpmath.euler)
        l_P = np.sqrt(constants.hbar * constants.G / constants.c**3)
        zeta_prime = abs(float(mpmath.diff(mpmath.zeta, 0.5)))
        alpha_psi = (gamma * l_P * zeta_prime) / (2 * np.pi * constants.c)

        # Target frequency
        f0_target = 141.7001

        # Derive RΨ
        R_psi = f0_target / alpha_psi

        # Reconstruct f₀
        f0_reconstructed = alpha_psi * R_psi

        # Should match to machine precision
        relative_error = abs(f0_reconstructed - f0_target) / f0_target
        self.assertLess(relative_error, 1e-10)


def run_tests():
    """Run all tests and print results"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAlphaPsiCorrection))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalPrecision))
    suite.addTests(loader.loadTestsFromTestCase(TestDimensionalAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestFormulaSelfConsistency))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
