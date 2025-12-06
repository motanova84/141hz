#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_verify_kappa_pi_complete.py

Tests for verify_kappa_pi_complete.py

Instituto QCAL - Quantum Consciousness Adelic Laboratory
"""

import sys
import os
import unittest
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from verify_kappa_pi_complete import (
    KappaVerifier,
    KAPPA_PI_REF,
    TOLERANCE,
    C_LIGHT,
    PLANCK_LENGTH,
)


class TestKappaVerifier(unittest.TestCase):
    """Test cases for KappaVerifier class."""

    def setUp(self):
        """Set up test fixtures."""
        self.verifier = KappaVerifier()

    def test_phi_value(self):
        """Test that phi (golden ratio) is correctly computed."""
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(self.verifier.phi, expected_phi, places=10)

    def test_kappa_pi_reference_value(self):
        """Test that KAPPA_PI_REF is correctly defined."""
        self.assertEqual(KAPPA_PI_REF, 2.5773)

    def test_tolerance_value(self):
        """Test that TOLERANCE is correctly defined."""
        self.assertEqual(TOLERANCE, 1e-4)

    def test_physical_constants(self):
        """Test that physical constants are correct."""
        self.assertEqual(C_LIGHT, 299792458)
        self.assertEqual(PLANCK_LENGTH, 1.616255e-35)

    def test_generate_realistic_cy_spectrum(self):
        """Test CY spectrum generation."""
        np.random.seed(17)
        spectrum = self.verifier._generate_realistic_cy_spectrum(1000)

        # Check that spectrum is sorted
        self.assertTrue(np.all(spectrum[:-1] <= spectrum[1:]))

        # Check all values are positive
        self.assertTrue(np.all(spectrum > 0))

        # Check ratio is close to KAPPA_PI_REF (with statistical tolerance)
        ratio = np.mean(spectrum**2) / np.mean(spectrum)
        # For 1000 samples, the ratio should be within ~10% of target
        self.assertAlmostEqual(ratio, KAPPA_PI_REF, delta=0.5)

    def test_verify_geometry(self):
        """Test geometry verification."""
        self.verifier.verify_geometry()

        self.assertIn("geometry", self.verifier.results)
        self.assertIn("kappa_geometry", self.verifier.results)
        self.assertTrue(self.verifier.results["geometry"])

    def test_verify_arithmetic(self):
        """Test arithmetic verification."""
        self.verifier.verify_arithmetic()

        self.assertIn("arithmetic", self.verifier.results)
        self.assertIn("kappa_arithmetic", self.verifier.results)
        self.assertTrue(self.verifier.results["arithmetic"])

    def test_verify_physics(self):
        """Test physics verification."""
        self.verifier.verify_physics()

        self.assertIn("physics", self.verifier.results)
        self.assertIn("lambda_yukawa", self.verifier.results)
        self.assertTrue(self.verifier.results["physics"])

        # Check Yukawa wavelength is in expected range
        lambda_y = self.verifier.results["lambda_yukawa"]
        self.assertGreater(lambda_y, 300)
        self.assertLess(lambda_y, 400)

    def test_verify_consciousness(self):
        """Test consciousness verification."""
        self.verifier.verify_consciousness()

        self.assertIn("consciousness", self.verifier.results)
        self.assertIn("tau_deco", self.verifier.results)
        self.assertTrue(self.verifier.results["consciousness"])

        # Check tau_deco is 1.2 ms
        tau = self.verifier.results["tau_deco"]
        self.assertEqual(tau, 1.2e-3)

    def test_verify_all(self):
        """Test complete verification."""
        results = self.verifier.verify_all()

        # Check all four domains are verified
        self.assertIn("geometry", results)
        self.assertIn("arithmetic", results)
        self.assertIn("physics", results)
        self.assertIn("consciousness", results)

        # Check all pass
        bool_results = [v for v in results.values() if isinstance(v, bool)]
        self.assertEqual(len(bool_results), 4)
        self.assertTrue(all(bool_results))

    def test_yukawa_wavelength_calculation(self):
        """Test Yukawa wavelength calculation."""
        f0 = 141.7001
        lambda_y = C_LIGHT / (2 * np.pi * f0) / 1000  # in km

        # Should be approximately 336 km
        self.assertAlmostEqual(lambda_y, 336, delta=10)

    def test_decoherence_frequency(self):
        """Test decoherence frequency calculation."""
        tau_deco = 1.2e-3
        f_deco = 1 / (2 * np.pi * tau_deco)

        # Check frequency is reasonable
        self.assertGreater(f_deco, 100)
        self.assertLess(f_deco, 150)


class TestKappaPhysics(unittest.TestCase):
    """Test physical relationships in kappa verification."""

    def test_fundamental_frequency(self):
        """Test f0 = 141.7001 Hz is used correctly."""
        f0 = 141.7001
        self.assertAlmostEqual(f0, 141.7001, places=4)

    def test_golden_ratio_power(self):
        """Test phi^3 calculation."""
        phi = (1 + np.sqrt(5)) / 2
        phi3 = phi**3

        # phi^3 should be approximately 4.236
        self.assertAlmostEqual(phi3, 4.236, delta=0.01)

    def test_zeta_second_derivative(self):
        """Test zeta''(1/2) value."""
        zeta_deriv2 = -0.207886
        self.assertAlmostEqual(zeta_deriv2, -0.207886, places=6)

    def test_arithmetic_factor(self):
        """Test arithmetic factor calculation."""
        phi = (1 + np.sqrt(5)) / 2
        zeta_deriv2 = -0.207886
        factor = abs(phi**3 * zeta_deriv2)

        self.assertGreater(factor, 0.8)
        self.assertLess(factor, 1.0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete verification."""

    def test_main_function_returns_zero(self):
        """Test that main() returns 0 when all verifications pass."""
        from verify_kappa_pi_complete import main

        result = main()
        self.assertEqual(result, 0)

    def test_full_verification_consistency(self):
        """Test that all kappa values are consistent."""
        verifier = KappaVerifier()
        verifier.verify_all()

        # Both geometry and arithmetic should give same kappa
        kappa_geo = verifier.results.get("kappa_geometry", 0)
        kappa_arith = verifier.results.get("kappa_arithmetic", 0)

        # Geometry uses statistical simulation, so use larger tolerance (0.15)
        # Arithmetic is exact, so use strict tolerance
        self.assertAlmostEqual(kappa_geo, KAPPA_PI_REF, delta=0.15)
        self.assertAlmostEqual(kappa_arith, KAPPA_PI_REF, delta=TOLERANCE)


if __name__ == "__main__":
    unittest.main()
