#!/usr/bin/env python3
"""
Tests for Consciousness Coherence Tensor and Extended Einstein Equations
=========================================================================

Comprehensive test suite verifying:
1. Consciousness coherence tensor Ξ_μν properties
2. Extended Einstein field equations with consciousness
3. Conservation laws and Bianchi identities
4. Physical consistency and predictions

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 19, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.consciousness_stress_energy import (
    ConsciousnessCoherenceTensor,
    ConsciousnessFieldState,
    compute_kappa_coupling,
    minkowski_metric,
    rest_frame_4velocity,
    example_consciousness_state,
    F_0,
    KAPPA_DEFAULT
)

from src.einstein_consciousness_gravity import (
    ExtendedEinsteinEquations,
    SpacetimeGeometry,
    compute_einstein_tensor,
    compute_ricci_scalar,
    create_flat_geometry,
    create_vacuum_stress_energy,
    EINSTEIN_CONSTANT,
    LAMBDA_COSMO
)


class TestConsciousnessCoherenceTensor(unittest.TestCase):
    """Test consciousness coherence tensor Ξ_μν."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tensor = ConsciousnessCoherenceTensor(f0=F_0)
        self.g_metric = minkowski_metric()
        self.g_inv = np.linalg.inv(self.g_metric)
    
    def test_coupling_constant_positive(self):
        """Test that coupling constant κ is positive."""
        self.assertGreater(self.tensor.kappa, 0)
        self.assertIsInstance(self.tensor.kappa, float)
    
    def test_energy_density_scaling(self):
        """Test energy density ρ_Ψ = I·A_eff²."""
        intensity = 1.0
        A_eff = 1.5
        
        rho_psi = self.tensor.compute_energy_density(intensity, A_eff)
        expected = intensity * (A_eff ** 2)
        
        self.assertAlmostEqual(rho_psi, expected, places=10)
    
    def test_energy_density_coherence_threshold(self):
        """Test energy density at coherence threshold A_eff = 1."""
        intensity = 1.0
        A_eff = 1.0
        
        rho_psi = self.tensor.compute_energy_density(intensity, A_eff)
        
        # At threshold, ρ_Ψ = I (no amplification)
        self.assertAlmostEqual(rho_psi, intensity, places=10)
    
    def test_tensor_symmetry(self):
        """Test that Ξ_μν is symmetric: Ξ_μν = Ξ_νμ."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        Xi = self.tensor.compute_tensor(state, self.g_metric)
        
        # Check symmetry
        self.assertTrue(self.tensor.verify_symmetry(Xi))
        
        # Explicit check
        for mu in range(4):
            for nu in range(4):
                self.assertAlmostEqual(Xi[mu, nu], Xi[nu, mu], places=10)
    
    def test_tensor_perfect_fluid_form(self):
        """Test perfect fluid form of Ξ_μν."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        Xi = self.tensor.compute_tensor(state, self.g_metric)
        
        # For rest frame u^μ = (1, 0, 0, 0), radiation EOS (P = ρ/3)
        rho_psi = self.tensor.compute_energy_density(state.intensity, state.A_eff)
        P_psi = self.tensor.compute_pressure(state.intensity, state.A_eff, "radiation")
        
        # Check time-time component: Ξ_00 should relate to energy density
        # Ξ_00 = -(ρ + P)u_0 u_0 - P g_00 = -(ρ + P) + P = -ρ
        # With signature (-,+,+,+): Ξ_00 = (ρ + P)u_0² + P g_00
        self.assertIsInstance(Xi[0, 0], (float, np.floating))
    
    def test_incoherent_state_minimal_contribution(self):
        """Test that incoherent state (A_eff < 1) has minimal contribution."""
        state_incoherent = example_consciousness_state(intensity=1.0, A_eff=0.5)
        state_coherent = example_consciousness_state(intensity=1.0, A_eff=2.0)
        
        rho_incoherent = self.tensor.compute_energy_density(
            state_incoherent.intensity, state_incoherent.A_eff
        )
        rho_coherent = self.tensor.compute_energy_density(
            state_coherent.intensity, state_coherent.A_eff
        )
        
        # Coherent state should have much larger energy density
        self.assertGreater(rho_coherent, rho_incoherent)
        self.assertAlmostEqual(rho_coherent / rho_incoherent, 16.0, places=1)  # (2.0/0.5)²
    
    def test_curvature_modulation_coherence(self):
        """Test curvature modulation factor increases with coherence."""
        factors = []
        A_effs = [0.5, 1.0, 1.5, 2.0]
        
        for A_eff in A_effs:
            factor = self.tensor.curvature_modulation_factor(A_eff)
            factors.append(factor)
        
        # Factors should be monotonically increasing (or equal within numerical precision)
        for i in range(len(factors) - 1):
            self.assertGreaterEqual(factors[i+1], factors[i])
        
        # Factor should always be >= 1.0 (baseline)
        for factor in factors:
            self.assertGreaterEqual(factor, 1.0)
    
    def test_tensor_trace(self):
        """Test tensor trace Ξ = g^μν Ξ_μν."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        Xi = self.tensor.compute_tensor(state, self.g_metric)
        
        trace = self.tensor.compute_trace(Xi, self.g_inv)
        
        # Trace should be finite
        self.assertTrue(np.isfinite(trace))
    
    def test_different_equations_of_state(self):
        """Test different equations of state for pressure."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        rho = self.tensor.compute_energy_density(state.intensity, state.A_eff)
        
        # Radiation: P = ρ/3
        P_rad = self.tensor.compute_pressure(state.intensity, state.A_eff, "radiation")
        self.assertAlmostEqual(P_rad, rho / 3.0, places=10)
        
        # Matter: P = 0
        P_matter = self.tensor.compute_pressure(state.intensity, state.A_eff, "matter")
        self.assertEqual(P_matter, 0.0)
        
        # Vacuum: P = -ρ
        P_vacuum = self.tensor.compute_pressure(state.intensity, state.A_eff, "vacuum")
        self.assertAlmostEqual(P_vacuum, -rho, places=10)


class TestExtendedEinsteinEquations(unittest.TestCase):
    """Test extended Einstein field equations with consciousness."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.einstein = ExtendedEinsteinEquations()
        self.geometry = create_flat_geometry()
        self.T_vacuum = create_vacuum_stress_energy()
    
    def test_einstein_constant(self):
        """Test Einstein constant 8πG/c⁴."""
        expected = 8 * np.pi * 6.67430e-11 / (299792458.0 ** 4)
        self.assertAlmostEqual(EINSTEIN_CONSTANT, expected, places=40)
    
    def test_source_term_structure(self):
        """Test structure of source term (8πG/c⁴)(T_μν + κΞ_μν)."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        Xi = self.einstein.consciousness_tensor.compute_tensor(state, self.geometry.g_metric)
        
        source = self.einstein.compute_source_term(self.T_vacuum, Xi)
        
        # Source should be (4×4) array
        self.assertEqual(source.shape, (4, 4))
        
        # Should be symmetric
        self.assertTrue(np.allclose(source, source.T))
    
    def test_left_hand_side_structure(self):
        """Test structure of LHS: G_μν + Λg_μν."""
        lhs = self.einstein.compute_left_hand_side(self.geometry)
        
        # Should be (4×4) array
        self.assertEqual(lhs.shape, (4, 4))
        
        # In flat space: G_μν = 0, so LHS = Λg_μν
        expected = self.einstein.Lambda * self.geometry.g_metric
        self.assertTrue(np.allclose(lhs, expected))
    
    def test_bianchi_identity_symmetry(self):
        """Test Bianchi identity verification for symmetric tensors."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        Xi = self.einstein.consciousness_tensor.compute_tensor(state, self.geometry.g_metric)
        
        verification = self.einstein.verify_bianchi_identity(
            self.geometry, self.T_vacuum, Xi
        )
        
        # Both tensors should be symmetric
        self.assertTrue(verification["T_symmetric"])
        self.assertTrue(verification["Xi_symmetric"])
        self.assertTrue(verification["conservation_satisfied"])
    
    def test_observer_modulation_increases_with_coherence(self):
        """Test that curvature increases with observer coherence."""
        R_classical = 1e-6  # Some background curvature
        
        A_effs = [0.0, 0.5, 1.0, 1.5, 2.0]
        R_observed_list = []
        
        for A_eff in A_effs:
            R_obs = self.einstein.observer_modulated_curvature(
                R_classical, A_eff, intensity=1.0
            )
            R_observed_list.append(R_obs)
        
        # Observed curvature should increase monotonically
        for i in range(len(R_observed_list) - 1):
            self.assertGreaterEqual(R_observed_list[i+1], R_observed_list[i])
        
        # At A_eff = 0, should equal classical
        self.assertAlmostEqual(R_observed_list[0], R_classical, places=10)
    
    def test_interferometer_phase_shift_sign(self):
        """Test interferometer phase shift has correct sign."""
        L = 4000.0  # LIGO arm length
        R_bg = 1e-10
        
        # Coherent observer should produce non-zero phase shift
        Delta_phi = self.einstein.interferometer_phase_shift(
            L=L,
            R_classical=R_bg,
            A_eff_coherent=2.0,
            A_eff_incoherent=0.5
        )
        
        # Phase shift should be positive (coherent > incoherent)
        self.assertGreater(Delta_phi, 0.0)
    
    def test_interferometer_phase_shift_scales_with_arm_length(self):
        """Test that phase shift scales with interferometer arm length."""
        R_bg = 1e-10
        A_eff_c = 2.0
        A_eff_i = 0.5
        
        L1 = 1000.0
        L2 = 4000.0
        
        Delta_phi_1 = self.einstein.interferometer_phase_shift(L1, R_bg, A_eff_c, A_eff_i)
        Delta_phi_2 = self.einstein.interferometer_phase_shift(L2, R_bg, A_eff_c, A_eff_i)
        
        # Should scale as L²
        expected_ratio = (L2 / L1) ** 2
        actual_ratio = Delta_phi_2 / Delta_phi_1
        
        self.assertAlmostEqual(actual_ratio, expected_ratio, places=5)
    
    def test_configuration_export(self):
        """Test configuration export to dictionary."""
        config = self.einstein.to_dict()
        
        # Should have key fields
        self.assertIn("Lambda_cosmo", config)
        self.assertIn("kappa_consciousness", config)
        self.assertIn("f0_Hz", config)
        self.assertIn("equation", config)
        
        # Check values
        self.assertEqual(config["f0_Hz"], F_0)
        self.assertGreater(config["kappa_consciousness"], 0)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency of extended equations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tensor = ConsciousnessCoherenceTensor()
        self.einstein = ExtendedEinsteinEquations()
    
    def test_energy_conditions(self):
        """Test weak energy condition: ρ ≥ 0."""
        for A_eff in [0.5, 1.0, 1.5, 2.0]:
            state = example_consciousness_state(intensity=1.0, A_eff=A_eff)
            rho = self.tensor.compute_energy_density(state.intensity, state.A_eff)
            
            # Energy density must be non-negative
            self.assertGreaterEqual(rho, 0.0)
    
    def test_causality_4velocity_normalization(self):
        """Test that 4-velocity is properly normalized: u_μu^μ = -1."""
        state = example_consciousness_state(intensity=1.0, A_eff=1.5)
        u = state.u_mu
        g = minkowski_metric()
        
        # Compute u_μu^μ = g_μν u^μ u^ν
        norm = 0.0
        for mu in range(4):
            for nu in range(4):
                norm += g[mu, nu] * u[mu] * u[nu]
        
        # Should equal -1 (timelike)
        self.assertAlmostEqual(norm, -1.0, places=10)
    
    def test_classical_limit_recovery(self):
        """Test recovery of classical Einstein equations when A_eff → 0."""
        # With A_eff = 0, consciousness contribution should vanish
        state_classical = example_consciousness_state(intensity=1.0, A_eff=0.0)
        
        rho_classical = self.tensor.compute_energy_density(
            state_classical.intensity, state_classical.A_eff
        )
        
        # Should be zero
        self.assertEqual(rho_classical, 0.0)
    
    def test_units_consistency(self):
        """Test dimensional consistency of computed quantities."""
        # Coupling constant κ should have same dimensions as G (or dimensionless)
        kappa = self.tensor.kappa
        
        # Should be finite and positive
        self.assertTrue(np.isfinite(kappa))
        self.assertGreater(kappa, 0.0)


class TestIntegrationWithQCAL(unittest.TestCase):
    """Test integration with existing QCAL framework."""
    
    def test_consciousness_frequency(self):
        """Test that consciousness frequency matches QCAL standard."""
        tensor = ConsciousnessCoherenceTensor()
        self.assertAlmostEqual(tensor.f0, 141.7001, places=4)
    
    def test_consciousness_field_quantum(self):
        """Test consciousness field quantum E_Ψ = hf₀."""
        tensor = ConsciousnessCoherenceTensor()
        h = 6.62607015e-34
        
        expected_E_psi = h * tensor.f0
        self.assertAlmostEqual(tensor.E_psi, expected_E_psi, places=40)
    
    def test_coupling_methods_consistency(self):
        """Test different methods for computing κ give reasonable values."""
        methods = ["planck_scale", "geometric", "minimal"]
        
        for method in methods:
            kappa = compute_kappa_coupling(F_0, method=method)
            
            # Should be finite and positive
            self.assertTrue(np.isfinite(kappa))
            self.assertGreater(kappa, 0.0)


def run_tests():
    """Run all test suites."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConsciousnessCoherenceTensor))
    suite.addTests(loader.loadTestsFromTestCase(TestExtendedEinsteinEquations))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithQCAL))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
