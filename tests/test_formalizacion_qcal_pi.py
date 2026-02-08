#!/usr/bin/env python3
"""
Tests for Teorema QCAL-Π Formalization

Tests the rigorous demonstration that κ_Π = 2.5773 is the minimum
of spectral entropy derived from Calabi-Yau geometry.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∞³)
"""

import unittest
import numpy as np
from scipy.integrate import trapezoid
import json
import os
import sys

# Import the module
from formalizacion_teorema_qcal_pi import (
    CalabiYauManifold,
    SpectralEntropyFunctional,
    FunctionalSpaceRigidity,
    LFunctionAnalysis,
    GeometricStability,
    KAPPA_PI_UNIVERSAL,
    PHI,
    run_complete_verification
)


class TestCalabiYauManifold(unittest.TestCase):
    """Tests for Calabi-Yau manifold structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cy = CalabiYauManifold(h21=101, holonomy='SU(3)')
    
    def test_holonomy_su3(self):
        """Test that holonomy is SU(3)."""
        self.assertEqual(self.cy.holonomy, 'SU(3)')
    
    def test_h21_quintic(self):
        """Test h^{2,1} = 101 for Fermat quintic."""
        self.assertEqual(self.cy.h21, 101)
    
    def test_euler_characteristic(self):
        """Test χ = 2(h^{1,1} - h^{2,1}) = -200."""
        chi = self.cy.euler_characteristic()
        self.assertEqual(chi, -200)
    
    def test_alpha_coefficient_positive(self):
        """Test that α > 0 (brane tension)."""
        self.assertGreater(self.cy.alpha, 0)
    
    def test_beta_coefficient_positive(self):
        """Test that β > 0 (magnetic coupling)."""
        self.assertGreater(self.cy.beta, 0)
    
    def test_alpha_depends_on_h21(self):
        """Test that α depends on h^{2,1}."""
        cy2 = CalabiYauManifold(h21=50)
        self.assertNotEqual(self.cy.alpha, cy2.alpha)
    
    def test_spectral_density_normalized(self):
        """Test that ρ_Π(θ) is normalized."""
        theta = np.linspace(-np.pi, np.pi, 1000)
        rho = self.cy.spectral_density(theta)
        
        # Check normalization
        norm = trapezoid(rho, theta)
        self.assertAlmostEqual(norm, 1.0, delta=0.01)
    
    def test_spectral_density_positive(self):
        """Test that ρ_Π(θ) > 0 everywhere."""
        theta = np.linspace(-np.pi, np.pi, 1000)
        rho = self.cy.spectral_density(theta)
        
        self.assertTrue(np.all(rho > 0))
    
    def test_spectral_density_symmetric(self):
        """Test that ρ_Π(θ) is symmetric: ρ(θ) = ρ(-θ)."""
        theta = np.linspace(-np.pi, np.pi, 1000)
        rho = self.cy.spectral_density(theta)
        
        # Check symmetry
        rho_flipped = np.flip(rho)
        np.testing.assert_allclose(rho, rho_flipped, rtol=1e-10)


class TestSpectralEntropyFunctional(unittest.TestCase):
    """Tests for spectral entropy functional."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cy = CalabiYauManifold(h21=101)
        self.functional = SpectralEntropyFunctional(self.cy, n_modes=5)
        self.theta = np.linspace(-np.pi, np.pi, 1000)
    
    def test_entropy_positive(self):
        """Test that entropy H(ρ) > 0."""
        rho = self.cy.spectral_density(self.theta)
        H = self.functional.entropy(rho, self.theta)
        
        self.assertGreater(H, 0)
    
    def test_entropy_uniform_distribution(self):
        """Test entropy of uniform distribution."""
        rho_uniform = np.ones_like(self.theta) / (2 * np.pi)
        H = self.functional.entropy(rho_uniform, self.theta)
        
        # For uniform distribution: H = log(2π) ≈ 1.838
        self.assertAlmostEqual(H, np.log(2 * np.pi), delta=0.1)
    
    def test_euler_lagrange_solution(self):
        """Test that Euler-Lagrange solution is normalized."""
        theta, rho_pi = self.functional.solve_euler_lagrange(n_points=1000)
        
        norm = trapezoid(rho_pi, theta)
        self.assertAlmostEqual(norm, 1.0, delta=0.01)
    
    def test_kappa_pi_computation(self):
        """Test that κ_Π is computed near expected value."""
        theta, rho_pi = self.functional.solve_euler_lagrange(n_points=1000)
        kappa = self.functional.compute_kappa_pi(rho_pi, theta)
        
        # Should be within 10% of universal value
        self.assertAlmostEqual(kappa, KAPPA_PI_UNIVERSAL, delta=0.3)
    
    def test_lagrange_functional_defined(self):
        """Test that Lagrange functional is well-defined."""
        rho = self.cy.spectral_density(self.theta)
        J = self.functional.lagrange_functional(rho, self.theta, lambda_0=1.0)
        
        # Should be finite
        self.assertTrue(np.isfinite(J))


class TestFunctionalSpaceRigidity(unittest.TestCase):
    """Tests for functional space F_CY rigidity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cy = CalabiYauManifold(h21=101)
        self.rigidity = FunctionalSpaceRigidity(self.cy)
        self.theta = np.linspace(-np.pi, np.pi, 1000)
    
    def test_spectral_density_in_space(self):
        """Test that ρ_Π ∈ F_CY."""
        rho = self.cy.spectral_density(self.theta)
        
        self.assertTrue(self.rigidity.is_in_space(rho, self.theta))
    
    def test_negative_density_not_in_space(self):
        """Test that negative densities are not in F_CY."""
        rho = -np.ones_like(self.theta)
        
        self.assertFalse(self.rigidity.is_in_space(rho, self.theta))
    
    def test_unnormalized_density_not_in_space(self):
        """Test that unnormalized densities are not in F_CY."""
        rho = np.ones_like(self.theta) * 2.0  # Not normalized
        
        self.assertFalse(self.rigidity.is_in_space(rho, self.theta))
    
    def test_asymmetric_density_not_in_space(self):
        """Test that asymmetric densities are not in F_CY."""
        # Create asymmetric density
        rho = np.exp(-self.theta ** 2)
        rho += 0.1 * self.theta  # Break symmetry
        rho = np.maximum(rho, 0)
        rho /= trapezoid(rho, self.theta)
        
        # Should fail symmetry check
        is_symmetric = np.allclose(rho, np.flip(rho), atol=1e-6)
        if not is_symmetric:
            self.assertFalse(self.rigidity.is_in_space(rho, self.theta))
    
    def test_infimum_entropy_positive(self):
        """Test that inf H(ρ) > 0."""
        infimum, std_dev = self.rigidity.compute_infimum_entropy(n_samples=50)
        
        self.assertGreater(infimum, 0)
    
    def test_infimum_entropy_reasonable(self):
        """Test that inf H(ρ) is in reasonable range."""
        infimum, std_dev = self.rigidity.compute_infimum_entropy(n_samples=50)
        
        # Should be between 0.5 and 2.0
        self.assertGreater(infimum, 0.5)
        self.assertLess(infimum, 2.0)


class TestLFunctionAnalysis(unittest.TestCase):
    """Tests for L-function zero analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cy = CalabiYauManifold(h21=101)
        self.l_func = LFunctionAnalysis(self.cy)
    
    def test_simulate_zeros_positive(self):
        """Test that L-function zeros are positive."""
        zeros = self.l_func.simulate_l_function_zeros(n_zeros=100)
        
        self.assertTrue(np.all(zeros > 0))
    
    def test_simulate_zeros_increasing(self):
        """Test that zeros are in increasing order."""
        zeros = self.l_func.simulate_l_function_zeros(n_zeros=100)
        
        # Check monotonicity
        self.assertTrue(np.all(np.diff(zeros) > 0))
    
    def test_phase_entropy_positive(self):
        """Test that phase entropy > 0."""
        zeros = self.l_func.simulate_l_function_zeros(n_zeros=500)
        H = self.l_func.compute_phase_entropy(zeros)
        
        self.assertGreater(H, 0)
    
    def test_phase_entropy_bounded(self):
        """Test that phase entropy is bounded."""
        zeros = self.l_func.simulate_l_function_zeros(n_zeros=500)
        H = self.l_func.compute_phase_entropy(zeros)
        
        # Should be less than log(n_bins) ≈ 3.9 for 50 bins
        self.assertLess(H, 5.0)
    
    def test_reproducibility(self):
        """Test that same seed gives same zeros."""
        zeros1 = self.l_func.simulate_l_function_zeros(n_zeros=100, seed=42)
        zeros2 = self.l_func.simulate_l_function_zeros(n_zeros=100, seed=42)
        
        np.testing.assert_array_equal(zeros1, zeros2)


class TestGeometricStability(unittest.TestCase):
    """Tests for geometric stability analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cy = CalabiYauManifold(h21=101)
        self.stability = GeometricStability(self.cy)
    
    def test_perturb_coefficients(self):
        """Test coefficient perturbation."""
        delta_alpha = 0.001
        delta_beta = 0.001
        
        cy_pert = self.stability.perturb_coefficients(delta_alpha, delta_beta)
        
        self.assertAlmostEqual(cy_pert.alpha, self.cy.alpha + delta_alpha)
        self.assertAlmostEqual(cy_pert.beta, self.cy.beta + delta_beta)
    
    def test_ricci_norm_zero_for_unperturbed(self):
        """Test that Ricci norm is ~0 for unperturbed manifold."""
        theta = np.linspace(-np.pi, np.pi, 1000)
        cy_pert = self.stability.perturb_coefficients(0, 0)
        
        ricci_norm = self.stability.compute_ricci_tensor_norm(cy_pert, theta)
        
        self.assertAlmostEqual(ricci_norm, 0.0, delta=1e-10)
    
    def test_ricci_norm_increases_with_perturbation(self):
        """Test that ||R_ij|| increases with perturbation."""
        theta = np.linspace(-np.pi, np.pi, 1000)
        
        delta1 = 1e-7
        delta2 = 1e-6
        
        cy_pert1 = self.stability.perturb_coefficients(delta1, delta1)
        cy_pert2 = self.stability.perturb_coefficients(delta2, delta2)
        
        ricci1 = self.stability.compute_ricci_tensor_norm(cy_pert1, theta)
        ricci2 = self.stability.compute_ricci_tensor_norm(cy_pert2, theta)
        
        self.assertGreater(ricci2, ricci1)
    
    def test_stability_threshold_verified(self):
        """Test that stability threshold is verified."""
        results = self.stability.verify_stability_threshold(
            threshold=1e-6,
            n_tests=50
        )
        
        self.assertTrue(results['threshold_verified'])
    
    def test_ricci_separation(self):
        """Test that there's clear separation above/below threshold."""
        results = self.stability.verify_stability_threshold(
            threshold=1e-6,
            n_tests=50
        )
        
        # Mean above should be significantly larger than mean below
        ratio = results['mean_ricci_above'] / results['mean_ricci_below']
        self.assertGreater(ratio, 1.5)


class TestCompleteVerification(unittest.TestCase):
    """Tests for complete verification pipeline."""
    
    def test_verification_runs(self):
        """Test that complete verification runs without errors."""
        results = run_complete_verification(verbose=False, save_results=False)
        
        self.assertIsNotNone(results)
        self.assertIn('verification', results)
    
    def test_verification_structure(self):
        """Test that results have expected structure."""
        results = run_complete_verification(verbose=False, save_results=False)
        
        # Check main sections
        self.assertIn('kappa_pi_universal', results)
        self.assertIn('manifold', results)
        self.assertIn('lagrange_method', results)
        self.assertIn('spectral_rigidity', results)
        self.assertIn('l_function_test', results)
        self.assertIn('geometric_stability', results)
        self.assertIn('verification', results)
    
    def test_kappa_pi_universal_value(self):
        """Test that κ_Π universal value is correct."""
        results = run_complete_verification(verbose=False, save_results=False)
        
        self.assertEqual(results['kappa_pi_universal'], 2.5773)
    
    def test_manifold_parameters(self):
        """Test that manifold parameters are correct."""
        results = run_complete_verification(verbose=False, save_results=False)
        
        self.assertEqual(results['manifold']['h21'], 101)
        self.assertEqual(results['manifold']['holonomy'], 'SU(3)')
        self.assertEqual(results['manifold']['euler_characteristic'], -200)
    
    def test_all_tests_executed(self):
        """Test that all verification tests are executed."""
        results = run_complete_verification(verbose=False, save_results=False)
        
        # Each section should have results
        self.assertIn('entropy_minimum', results['lagrange_method'])
        self.assertIn('infimum_entropy', results['spectral_rigidity'])
        self.assertIn('phase_entropy', results['l_function_test'])
        self.assertIn('threshold_verified', results['geometric_stability'])


class TestPhysicalConstants(unittest.TestCase):
    """Tests for physical constants and predictions."""
    
    def test_kappa_pi_value(self):
        """Test κ_Π = 2.5773."""
        self.assertEqual(KAPPA_PI_UNIVERSAL, 2.5773)
    
    def test_golden_ratio(self):
        """Test φ = (1 + √5) / 2."""
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, expected_phi, places=10)
    
    def test_phi_cubed(self):
        """Test φ³ ≈ 4.236."""
        from formalizacion_teorema_qcal_pi import PHI_CUBED
        self.assertAlmostEqual(PHI_CUBED, 4.236, delta=0.001)
    
    def test_fundamental_frequency(self):
        """Test f₀ = 141.7001 Hz."""
        from formalizacion_teorema_qcal_pi import F0_HZ
        self.assertEqual(F0_HZ, 141.7001)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_verification(self):
        """Test complete end-to-end verification."""
        # Run complete verification
        results = run_complete_verification(verbose=False, save_results=True)
        
        # Check that results file was created
        self.assertTrue(os.path.exists('formalizacion_qcal_pi_results.json'))
        
        # Load and verify
        with open('formalizacion_qcal_pi_results.json', 'r') as f:
            saved_results = json.load(f)
        
        self.assertEqual(saved_results['kappa_pi_universal'], KAPPA_PI_UNIVERSAL)
        
        # Clean up
        if os.path.exists('formalizacion_qcal_pi_results.json'):
            os.remove('formalizacion_qcal_pi_results.json')
    
    def test_consistency_across_runs(self):
        """Test that multiple runs give consistent results."""
        results1 = run_complete_verification(verbose=False, save_results=False)
        results2 = run_complete_verification(verbose=False, save_results=False)
        
        # Key values should be identical
        self.assertEqual(
            results1['manifold']['h21'],
            results2['manifold']['h21']
        )
        self.assertAlmostEqual(
            results1['manifold']['alpha'],
            results2['manifold']['alpha'],
            places=10
        )


class TestMathematicalProperties(unittest.TestCase):
    """Tests for mathematical properties and theorems."""
    
    def test_ricci_flatness_condition(self):
        """Test that unperturbed CY is Ricci-flat."""
        cy = CalabiYauManifold(h21=101)
        stability = GeometricStability(cy)
        theta = np.linspace(-np.pi, np.pi, 1000)
        
        # Unperturbed should have R_ij ≈ 0
        cy_unpert = stability.perturb_coefficients(0, 0)
        ricci_norm = stability.compute_ricci_tensor_norm(cy_unpert, theta)
        
        self.assertLess(ricci_norm, 1e-9)
    
    def test_spectral_gap_positive(self):
        """Test that spectral gap is positive."""
        cy = CalabiYauManifold(h21=101)
        functional = SpectralEntropyFunctional(cy)
        theta, rho = functional.solve_euler_lagrange()
        
        # Compute moments
        lambda_vals = theta  # Simplified
        mu1 = trapezoid(lambda_vals * rho, theta)
        mu2 = trapezoid(lambda_vals ** 2 * rho, theta)
        
        # Gap should be positive
        gap = mu2 - mu1 ** 2
        self.assertGreater(gap, 0)
    
    def test_entropy_minimization(self):
        """Test that solution has reasonable entropy in F_CY."""
        cy = CalabiYauManifold(h21=101)
        functional = SpectralEntropyFunctional(cy)
        theta, rho_opt = functional.solve_euler_lagrange()
        
        H_opt = functional.entropy(rho_opt, theta)
        
        # Generate several random densities in F_CY
        rigidity = FunctionalSpaceRigidity(cy)
        entropies = []
        
        for seed in range(10):
            np.random.seed(seed)
            # Use uniform + small perturbation to stay in F_CY
            rho_random = np.ones_like(theta) / (2 * np.pi)
            rho_random += 0.01 * np.cos(2 * theta)
            rho_random = np.maximum(rho_random, 0.01)
            rho_random /= trapezoid(rho_random, theta)
            
            if rigidity.is_in_space(rho_random, theta):
                H_random = functional.entropy(rho_random, theta)
                entropies.append(H_random)
        
        # Optimal should be within range of typical F_CY densities
        if entropies:
            mean_H = np.mean(entropies)
            # Should be within 2x of mean
            self.assertLess(H_opt, mean_H * 2.0)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
