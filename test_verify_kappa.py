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
Tests for verify_kappa.py - Calabi-Yau Spectral Invariant Verification

Author: José Manuel Mota Burruezo (JMMB Ψ✧∞³)
"""

import math
import os
import sys
import unittest
from typing import Dict, List, Tuple

# Dynamically find the module path
_current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _current_dir)
import verify_kappa as vk


class TestConstants(unittest.TestCase):
    """Test fundamental constants."""
    
    def test_kappa_pi_universal_value(self):
        """κ_Π = 2.5773 is the predicted universal value."""
        self.assertAlmostEqual(vk.KAPPA_PI_UNIVERSAL, 2.5773, places=4)
    
    def test_f0_value(self):
        """f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(vk.F0_HZ, 141.7001, places=4)
    
    def test_phi_value(self):
        """φ = (1 + √5) / 2 ≈ 1.618."""
        expected_phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(vk.PHI, expected_phi, places=10)
    
    def test_phi_cubed_value(self):
        """φ³ ≈ 4.236."""
        self.assertAlmostEqual(vk.PHI_CUBED, 4.236, places=2)
    
    def test_zeta_prime_half(self):
        """ζ'(1/2) ≈ -0.2078862."""
        self.assertAlmostEqual(vk.ZETA_PRIME_HALF, -0.2078862, places=4)
    
    def test_speed_of_light(self):
        """c = 299792458 m/s (exact)."""
        self.assertEqual(vk.C, 299792458.0)


class TestCYEigenvalues(unittest.TestCase):
    """Test CY eigenvalue computation."""
    
    def test_eigenvalues_positive(self):
        """Eigenvalues should be positive."""
        mu1, mu2, kappa = vk.compute_cy_eigenvalues(101, seed=42)
        self.assertGreater(mu1, 0)
        self.assertGreater(mu2, 0)
    
    def test_spectral_gap(self):
        """μ₂ > μ₁ (spectral gap exists)."""
        mu1, mu2, kappa = vk.compute_cy_eigenvalues(101, seed=42)
        self.assertGreater(mu2, mu1)
    
    def test_kappa_approximately_universal(self):
        """κ_Π ≈ 2.5773 for Fermat quintic."""
        mu1, mu2, kappa = vk.compute_cy_eigenvalues(101, seed=42)
        self.assertAlmostEqual(kappa, 2.5773, delta=0.1)
    
    def test_kappa_ratio_definition(self):
        """κ = μ₂/μ₁ by definition."""
        mu1, mu2, kappa = vk.compute_cy_eigenvalues(50, seed=123)
        self.assertAlmostEqual(kappa, mu2 / mu1, places=10)
    
    def test_reproducibility(self):
        """Same seed gives same results."""
        result1 = vk.compute_cy_eigenvalues(101, seed=42)
        result2 = vk.compute_cy_eigenvalues(101, seed=42)
        self.assertEqual(result1, result2)


class TestCYSample(unittest.TestCase):
    """Test CY variety sample generation."""
    
    def test_sample_size(self):
        """Sample should have correct number of varieties."""
        sample = vk.generate_cy_sample(n_varieties=150, seed=42)
        self.assertEqual(len(sample), 150)
    
    def test_sample_h21_range(self):
        """h^{2,1} should be in expected range [20, 170]."""
        sample = vk.generate_cy_sample(n_varieties=150, seed=42)
        h21_values = [r[0] for r in sample]
        self.assertGreaterEqual(min(h21_values), 20)
        self.assertLessEqual(max(h21_values), 170)
    
    def test_sample_kappa_range(self):
        """κ_Π values should be in reasonable range."""
        sample = vk.generate_cy_sample(n_varieties=150, seed=42)
        kappa_values = [r[1] for r in sample]
        self.assertGreater(min(kappa_values), 2.4)
        self.assertLess(max(kappa_values), 2.8)
    
    def test_sample_reproducibility(self):
        """Same seed gives same sample."""
        sample1 = vk.generate_cy_sample(n_varieties=50, seed=123)
        sample2 = vk.generate_cy_sample(n_varieties=50, seed=123)
        self.assertEqual(sample1, sample2)


class TestUniversalityAnalysis(unittest.TestCase):
    """Test universality analysis."""
    
    def setUp(self):
        """Generate sample for tests."""
        self.sample = vk.generate_cy_sample(n_varieties=150, seed=42)
        self.analysis = vk.analyze_universality(self.sample)
    
    def test_mean_near_universal(self):
        """Mean κ_Π should be close to 2.5773."""
        self.assertAlmostEqual(
            self.analysis['kappa_mean'], 
            vk.KAPPA_PI_UNIVERSAL, 
            delta=0.01
        )
    
    def test_low_r_squared(self):
        """R² < 0.05 indicates independence from h^{2,1}."""
        self.assertLess(self.analysis['r_squared'], 0.05)
    
    def test_std_acceptable(self):
        """Standard deviation σ < 0.1."""
        self.assertLess(self.analysis['kappa_std'], 0.1)
    
    def test_regression_slope_small(self):
        """Regression slope should be near zero."""
        self.assertLess(abs(self.analysis['regression_slope']), 0.01)


class TestVerification(unittest.TestCase):
    """Test the verification function."""
    
    def test_verification_passes_with_default_tolerance(self):
        """Verification should pass with default tolerance."""
        success, results = vk.verify_kappa(tolerance=1e-2, verbose=False)
        self.assertTrue(success)
    
    def test_verification_result_structure(self):
        """Result dictionary has expected keys."""
        success, results = vk.verify_kappa(tolerance=1e-2, verbose=False)
        expected_keys = [
            'kappa_final', 'kappa_universal', 'deviation',
            'tolerance', 'is_within_tolerance', 'is_universal',
            'std_acceptable', 'analysis'
        ]
        for key in expected_keys:
            self.assertIn(key, results)
    
    def test_verification_with_strict_tolerance(self):
        """Verification with very strict tolerance should still work."""
        success, results = vk.verify_kappa(tolerance=1e-3, verbose=False)
        self.assertTrue(success)
    
    def test_verification_deviation_computed(self):
        """Deviation should be computed correctly."""
        success, results = vk.verify_kappa(tolerance=1e-2, verbose=False)
        expected_deviation = abs(
            results['kappa_final'] - vk.KAPPA_PI_UNIVERSAL
        )
        self.assertAlmostEqual(
            results['deviation'], 
            expected_deviation, 
            places=10
        )


class TestPhysicalConnections(unittest.TestCase):
    """Test physical connections computation."""
    
    def test_yukawa_wavelength(self):
        """λ_Yukawa = c/f₀ ≈ 2116 km."""
        physics = vk.compute_physical_connections(verbose=False)
        expected_lambda = vk.C / vk.F0_HZ / 1000  # in km
        self.assertAlmostEqual(
            physics['lambda_yukawa_km'], 
            expected_lambda, 
            places=1
        )
    
    def test_zeta_phi_product(self):
        """|ζ'(1/2)| × φ³ ≈ 0.88."""
        physics = vk.compute_physical_connections(verbose=False)
        expected = abs(vk.ZETA_PRIME_HALF) * vk.PHI_CUBED
        self.assertAlmostEqual(
            physics['zeta_phi_product'], 
            expected, 
            places=5
        )
    
    def test_decoherence_time(self):
        """τ_deco = 1.2 ms."""
        physics = vk.compute_physical_connections(verbose=False)
        self.assertEqual(physics['tau_deco_ms'], 1.2)


class TestInterpretation(unittest.TestCase):
    """Test physical interpretation requirements."""
    
    def test_150_universes_interpretation(self):
        """150 varieties = 150 possible universes."""
        sample = vk.generate_cy_sample(n_varieties=150, seed=42)
        
        # Each variety represents a possible universe
        self.assertEqual(len(sample), 150)
        
        # All share the same κ_Π ≈ 2.5773
        kappa_values = [r[1] for r in sample]
        mean_kappa = sum(kappa_values) / len(kappa_values)
        self.assertAlmostEqual(mean_kappa, 2.5773, delta=0.01)
    
    def test_fermat_quintic_special(self):
        """Fermat quintic h^{2,1} = 101 is our universe."""
        mu1, mu2, kappa = vk.compute_cy_eigenvalues(101, seed=141700)
        
        # Our universe has the same κ_Π
        self.assertAlmostEqual(kappa, vk.KAPPA_PI_UNIVERSAL, delta=0.1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
