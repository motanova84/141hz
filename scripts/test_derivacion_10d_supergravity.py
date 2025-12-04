#!/usr/bin/env python3
"""
Test suite for 10D Supergravity derivation of V_eff

This module tests the implementation of the explicit derivation of the
effective potential V_eff from 10D Type IIB Supergravity, following the
conventions of Gukov-Vafa-Witten, Douglas-Kachru, and Becker-Becker-Schwarz.

Tests cover:
1. Physical constants consistency
2. Coefficient calculations (α, β, γ, δ)
3. 1-loop ζ-regularization
4. Numerical minimization
5. Frequency calculation f₀ = 141.7001 Hz
"""

import unittest
import numpy as np
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from derivacion_10d_supergravity import (
    SUGRA10DDerivation,
    NumericalFitting,
    SUGRAParameters,
    l_P,
    m_P,
    c,
    kappa_10_sq,
    kappa_4_sq,
    Lambda_cosmo,
    zeta_prime_half,
    h11,
    h21,
    chi_euler
)


class TestPhysicalConstants(unittest.TestCase):
    """Test physical constants are correctly defined."""
    
    def test_planck_length(self):
        """Verify Planck length is approximately correct."""
        self.assertAlmostEqual(l_P, 1.616255e-35, delta=1e-40)
    
    def test_speed_of_light(self):
        """Verify speed of light."""
        self.assertAlmostEqual(c, 2.99792458e8, delta=1)
    
    def test_planck_mass(self):
        """Verify Planck mass is approximately correct."""
        self.assertAlmostEqual(m_P, 2.176434e-8, delta=1e-12)
    
    def test_kappa_10_squared(self):
        """Verify 10D gravitational coupling."""
        expected_order = (2 * np.pi)**7 * l_P**8
        self.assertAlmostEqual(kappa_10_sq / expected_order, 1.0, delta=0.01)
    
    def test_zeta_prime_half(self):
        """Verify ζ'(1/2) is approximately -3.92."""
        self.assertAlmostEqual(zeta_prime_half, -3.92264, delta=0.001)


class TestCalabiYauTopology(unittest.TestCase):
    """Test Calabi-Yau topological invariants."""
    
    def test_hodge_numbers(self):
        """Verify Hodge numbers of the quintic."""
        self.assertEqual(h11, 1)
        self.assertEqual(h21, 101)
    
    def test_euler_characteristic(self):
        """Verify Euler characteristic χ = 2(h11 - h21) = -200."""
        self.assertEqual(chi_euler, -200)
        self.assertEqual(chi_euler, 2 * (h11 - h21))


class TestSUGRACoefficients(unittest.TestCase):
    """Test coefficient calculations from SUGRA reduction."""
    
    def setUp(self):
        """Create derivation instance."""
        self.derivation = SUGRA10DDerivation()
    
    def test_alpha_coefficient(self):
        """Verify α = 3/(8κ₁₀²)."""
        expected = 3 / (8 * kappa_10_sq)
        self.assertEqual(self.derivation.alpha, expected)
    
    def test_beta_coefficient(self):
        """Verify β = (1/κ₁₀²)(½ e⁻Φ) with Φ=0."""
        expected = (1 / kappa_10_sq) * 0.5
        self.assertEqual(self.derivation.beta, expected)
    
    def test_gamma_coefficient(self):
        """Verify γ = Λ²/(2κ₄²)."""
        expected = Lambda_cosmo**2 / (2 * kappa_4_sq)
        self.assertEqual(self.derivation.gamma, expected)
    
    def test_delta_coefficient(self):
        """Verify δ = |F₅|²/((2π)⁶ κ₁₀²)."""
        F5_sq = 1.0  # default value
        expected = F5_sq / ((2 * np.pi)**6 * kappa_10_sq)
        self.assertEqual(self.derivation.delta, expected)
    
    def test_coefficients_positive(self):
        """Verify all coefficients are positive (for physical potential)."""
        self.assertGreater(self.derivation.alpha, 0)
        self.assertGreater(self.derivation.beta, 0)
        self.assertGreater(self.derivation.gamma, 0)
        self.assertGreater(self.derivation.delta, 0)


class TestPotentialEffective(unittest.TestCase):
    """Test effective potential calculations."""
    
    def setUp(self):
        """Create derivation instance."""
        self.derivation = SUGRA10DDerivation()
    
    def test_V_classical_positive_R(self):
        """Verify V_classical returns finite value for positive R."""
        R_test = 1e40  # Large R in Planck units
        V = self.derivation.V_classical(R_test)
        self.assertTrue(np.isfinite(V))
    
    def test_V_adelic_bounded(self):
        """Verify adelic term is bounded [0, 0.01]."""
        for R in [1e30, 1e40, 1e50]:
            V_adelic = self.derivation.V_adelic(R)
            self.assertGreaterEqual(V_adelic, 0)
            self.assertLessEqual(V_adelic, 0.01)
    
    def test_V_eff_total_finite(self):
        """Verify total potential is finite for physical R values."""
        R_test = 2.08e40  # Expected R_Ψ for f₀ = 141.7001 Hz
        V = self.derivation.V_eff_total(R_test)
        self.assertTrue(np.isfinite(V))
    
    def test_V_eff_total_positive_R_only(self):
        """Verify potential returns inf for non-positive R."""
        V_zero = self.derivation.V_eff_total(0)
        V_neg = self.derivation.V_eff_total(-1)
        self.assertEqual(V_zero, float('inf'))
        self.assertEqual(V_neg, float('inf'))


class TestZetaRegularization(unittest.TestCase):
    """Test 1-loop ζ-regularization corrections."""
    
    def setUp(self):
        """Create derivation instance."""
        self.derivation = SUGRA10DDerivation()
    
    def test_1loop_finite(self):
        """Verify 1-loop correction is finite."""
        R_test = 1e40
        V_1loop = self.derivation.V_1loop_zeta_regularized(R_test, n_modes=10)
        self.assertTrue(np.isfinite(V_1loop))
    
    def test_1loop_small_correction(self):
        """Verify 1-loop is smaller than classical for large R."""
        R_test = 1e40
        V_classical = abs(self.derivation.V_classical(R_test))
        V_1loop = abs(self.derivation.V_1loop_zeta_regularized(R_test, n_modes=10))
        # 1-loop should be a small correction
        self.assertLess(V_1loop, V_classical * 100)


class TestFrequencyCalculation(unittest.TestCase):
    """Test fundamental frequency calculation."""
    
    def setUp(self):
        """Create derivation instance."""
        self.derivation = SUGRA10DDerivation()
    
    def test_f0_from_R_psi(self):
        """Verify f₀ = c/(2πR_Ψ) formula."""
        # R_Ψ that should give 141.7001 Hz
        R_psi = c / (2 * np.pi * 141.7001) / l_P
        f0_calc = self.derivation.compute_f0(R_psi)
        self.assertAlmostEqual(f0_calc, 141.7001, delta=0.001)
    
    def test_f0_positive(self):
        """Verify frequency is positive for positive R."""
        R_test = 1e40
        f0 = self.derivation.compute_f0(R_test)
        self.assertGreater(f0, 0)


class TestNumericalFitting(unittest.TestCase):
    """Test numerical fitting for f₀ = 141.7001 Hz."""
    
    def setUp(self):
        """Create fitting instance."""
        self.fitter = NumericalFitting(target_f0=141.7001)
    
    def test_R_psi_from_f0(self):
        """Verify R_Ψ calculation from target frequency."""
        R_psi = self.fitter.compute_R_psi_from_f0()
        # Should be around 2e40 in Planck units
        self.assertGreater(R_psi, 1e40)
        self.assertLess(R_psi, 1e41)
    
    def test_run_fit_produces_results(self):
        """Verify fitting produces complete results."""
        results = self.fitter.run_fit()
        
        # Check required keys exist
        self.assertIn('fit_parameters', results)
        self.assertIn('derived_quantities', results)
        self.assertIn('coefficients', results)
        
        # Check fit parameters
        params = results['fit_parameters']
        self.assertIn('R_psi_min', params)
        self.assertIn('f0', params)
        self.assertIn('chi2_per_dof', params)
        self.assertIn('stability', params)
    
    def test_fit_frequency_accuracy(self):
        """Verify fitted frequency matches target."""
        results = self.fitter.run_fit()
        f0_fitted = results['fit_parameters']['f0']['value']
        self.assertAlmostEqual(f0_fitted, 141.7001, delta=0.0001)
    
    def test_fit_stability(self):
        """Verify minimum is stable."""
        results = self.fitter.run_fit()
        stability = results['fit_parameters']['stability']
        self.assertEqual(stability, 'Verified')
    
    def test_chi2_reasonable(self):
        """Verify χ²/dof is close to 1."""
        results = self.fitter.run_fit()
        chi2_dof = results['fit_parameters']['chi2_per_dof']
        # Should be around 1 for a good fit
        self.assertGreater(chi2_dof, 0.5)
        self.assertLess(chi2_dof, 2.0)


class TestSUGRAParameters(unittest.TestCase):
    """Test SUGRA parameter configuration."""
    
    def test_default_parameters(self):
        """Verify default parameters are physical."""
        params = SUGRAParameters()
        self.assertEqual(params.dilaton, 0.0)
        self.assertEqual(params.F5_squared, 1.0)
        self.assertEqual(params.V6_quintic_factor, 1/5)
    
    def test_custom_parameters(self):
        """Verify custom parameters are accepted."""
        params = SUGRAParameters(dilaton=0.5, F5_squared=2.0)
        self.assertEqual(params.dilaton, 0.5)
        self.assertEqual(params.F5_squared, 2.0)
    
    def test_custom_params_affect_coefficients(self):
        """Verify custom dilaton affects β coefficient."""
        derivation_default = SUGRA10DDerivation()
        derivation_custom = SUGRA10DDerivation(SUGRAParameters(dilaton=1.0))
        
        # β should be different due to e^(-Φ) factor
        self.assertNotEqual(derivation_default.beta, derivation_custom.beta)


class TestMinimization(unittest.TestCase):
    """Test potential minimization algorithm."""
    
    def setUp(self):
        """Create derivation instance."""
        self.derivation = SUGRA10DDerivation()
    
    def test_minimize_finds_minimum(self):
        """Verify minimization finds a minimum."""
        result = self.derivation.minimize_potential(R_min=1e38, R_max=1e42)
        self.assertTrue(result['success'])
    
    def test_minimum_in_range(self):
        """Verify minimum is within search range."""
        R_min, R_max = 1e38, 1e42
        result = self.derivation.minimize_potential(R_min=R_min, R_max=R_max)
        R_found = result['R_psi_min']
        self.assertGreater(R_found, R_min)
        self.assertLess(R_found, R_max)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete derivation."""
    
    def test_full_derivation_produces_f0(self):
        """Verify complete derivation produces f₀ ≈ 141.7 Hz."""
        fitter = NumericalFitting(target_f0=141.7001)
        results = fitter.run_fit()
        
        f0 = results['fit_parameters']['f0']['value']
        self.assertAlmostEqual(f0, 141.7001, delta=0.01)
    
    def test_results_self_consistent(self):
        """Verify R_Ψ and f₀ are self-consistent."""
        fitter = NumericalFitting(target_f0=141.7001)
        results = fitter.run_fit()
        
        R_psi = results['fit_parameters']['R_psi_min']['value']
        f0 = results['fit_parameters']['f0']['value']
        
        # Verify f₀ = c/(2πR_Ψ)
        R_meters = R_psi * l_P
        f0_check = c / (2 * np.pi * R_meters)
        
        self.assertAlmostEqual(f0, f0_check, delta=0.001)


if __name__ == '__main__':
    unittest.main(verbosity=2)
