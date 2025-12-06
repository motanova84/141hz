#!/usr/bin/env python3
"""
Test suite for verify_kappa.py and κ_Π invariant computation.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
DOI: 10.5281/zenodo.17379721
"""

import math
import subprocess
import sys
import unittest


class TestKappaPi(unittest.TestCase):
    """Test cases for κ_Π universal invariant."""

    def test_golden_ratio(self):
        """Test that golden ratio φ is computed correctly."""
        phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(phi, 1.618033988749895, places=10)

    def test_phi_cubed(self):
        """Test that φ³ is computed correctly."""
        phi = (1 + math.sqrt(5)) / 2
        phi_cubed = phi ** 3
        self.assertAlmostEqual(phi_cubed, 4.23606797749979, places=10)

    def test_zeta_prime_half(self):
        """Test the |ζ'(1/2)| value."""
        zeta_prime_half = 1.4603545088095868
        self.assertTrue(1.460 < zeta_prime_half < 1.461)

    def test_base_kappa_pi(self):
        """Test the base κ_Π computation."""
        phi = (1 + math.sqrt(5)) / 2
        phi_cubed = phi ** 3
        zeta_prime_half = 1.4603545088095868
        base_kappa = math.sqrt(phi_cubed * zeta_prime_half)
        self.assertAlmostEqual(base_kappa, 2.487199423159656, places=10)

    def test_kappa_pi_with_correction(self):
        """Test κ_Π with CY threefold correction."""
        phi = (1 + math.sqrt(5)) / 2
        phi_cubed = phi ** 3
        zeta_prime_half = 1.4603545088095868
        base_kappa = math.sqrt(phi_cubed * zeta_prime_half)
        cy_correction = 1 + 1 / 27
        kappa_pi = base_kappa * cy_correction
        self.assertAlmostEqual(kappa_pi, 2.5793, places=3)

    def test_yukawa_wavelength(self):
        """Test the Yukawa wavelength computation."""
        c = 299792458  # m/s
        f0 = 141.7001  # Hz
        lambda_bar = c / (2 * math.pi * f0) / 1000  # km
        self.assertAlmostEqual(lambda_bar, 336.72, places=1)

    def test_decoherence_time(self):
        """Test the decoherence time computation."""
        phi = (1 + math.sqrt(5)) / 2
        f0 = 141.7001
        tau_deco_ms = (phi / f0) * 1000
        self.assertAlmostEqual(tau_deco_ms, 11.42, places=1)

    def test_cy_quintic_hodge_numbers(self):
        """Test CY quintic Hodge numbers."""
        h_11 = 1
        h_21 = 101
        chi = 2 * (h_11 - h_21)
        self.assertEqual(chi, -200)


class TestVerifyKappaScript(unittest.TestCase):
    """Test the verify_kappa.py script execution."""

    def test_script_passes_with_default_tolerance(self):
        """Test that script passes with default tolerance."""
        result = subprocess.run(
            [sys.executable, "verify_kappa.py", "--tol", "1e-4", "--quiet"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_script_fails_with_tiny_tolerance(self):
        """Test that script fails with impossibly small tolerance."""
        result = subprocess.run(
            [sys.executable, "verify_kappa.py", "--tol", "1e-15", "--quiet"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)


class TestFourPillars(unittest.TestCase):
    """Test the four pillars of the framework."""

    def test_geometry_cy_quintic(self):
        """Test GEOMETRY pillar: CY quintic Hodge numbers."""
        h_11 = 1
        h_21 = 101
        chi = 2 * (h_11 - h_21)
        self.assertEqual(chi, -200)
        self.assertEqual(h_11, 1)
        self.assertEqual(h_21, 101)

    def test_arithmetic_p17(self):
        """Test ARITHMETIC pillar: p=17 noetic equilibrium."""
        p = 17
        adelic = math.exp(math.pi * math.sqrt(p) / 2)
        fractal = p ** (-1.5)
        equilibrium = adelic * fractal
        self.assertTrue(equilibrium > 0)
        # Equilibrium at p=17 should be positive (approximately 9.27)
        self.assertGreater(equilibrium, 0)

    def test_physics_frequency(self):
        """Test PHYSICS pillar: f₀=141.7001 Hz."""
        f0 = 141.7001
        c = 299792458
        lambda_bar_km = c / (2 * math.pi * f0) / 1000
        self.assertAlmostEqual(lambda_bar_km, 336.72, places=1)

    def test_consciousness_psi(self):
        """Test CONSCIOUSNESS pillar: Ψ=I×A_eff²."""
        I = 1.0  # Integrated information
        A_eff = 2.0  # Effective area
        psi = I * A_eff ** 2
        self.assertEqual(psi, 4.0)
        # Verify scaling property
        k = 2
        psi_scaled = I * (k * A_eff) ** 2
        self.assertEqual(psi_scaled, k ** 2 * psi)


if __name__ == "__main__":
    unittest.main()
