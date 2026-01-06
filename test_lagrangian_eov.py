#!/usr/bin/env python3
"""
Tests for Lagrangian EOV Module
================================

Tests the Lagrangian/Action formulation and variational derivation
of the Equation of Vibrational Origin (EOV).

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-01-06
"""

import unittest
import numpy as np
from qcal.lagrangian_eov import (
    # Constants
    F_0, OMEGA_0, ZETA_PRIME_HALF, XI_COUPLING, ZETA_COUPLING,
    G_NEWTON, C_LIGHT, HBAR,
    # Data structures
    LagrangianParameters, FieldConfiguration,
    # Lagrangian components
    lagrangian_einstein_hilbert,
    lagrangian_kinetic_psi,
    lagrangian_potential,
    lagrangian_modulation,
    lagrangian_total,
    # Action
    action_functional,
    # EOV equation
    eov_equation,
    energy_momentum_tensor_psi,
    # Solvers
    solve_eov_flat_spacetime,
    # Utilities
    compute_zeta_prime_half,
)


class TestConstants(unittest.TestCase):
    """Test fundamental constants."""
    
    def test_frequency(self):
        """Test fundamental frequency f₀."""
        self.assertAlmostEqual(F_0, 141.70001, places=5)  # Match qcal.constants precision
        
    def test_angular_frequency(self):
        """Test ω₀ = 2πf₀."""
        expected_omega = 2 * np.pi * F_0
        self.assertAlmostEqual(OMEGA_0, expected_omega, places=2)
        self.assertAlmostEqual(OMEGA_0, 890.33, places=1)
    
    def test_zeta_prime_half(self):
        """Test ζ'(1/2) ≈ -3.922."""
        self.assertAlmostEqual(ZETA_PRIME_HALF, -3.922, places=2)
        self.assertTrue(-4.0 < ZETA_PRIME_HALF < -3.9)
    
    def test_coupling_constants(self):
        """Test coupling constants."""
        # Conformal coupling
        self.assertAlmostEqual(XI_COUPLING, 1.0/6.0, places=6)
        
        # Modulation coupling
        expected_zeta_coupling = ZETA_PRIME_HALF / (2 * np.pi)
        self.assertAlmostEqual(ZETA_COUPLING, expected_zeta_coupling, places=6)


class TestLagrangianComponents(unittest.TestCase):
    """Test individual Lagrangian density components."""
    
    def test_einstein_hilbert(self):
        """Test Einstein-Hilbert Lagrangian."""
        R = 1e-20  # Typical curvature
        sqrt_g = 1.0
        
        L_EH = lagrangian_einstein_hilbert(R, sqrt_g, G_NEWTON)
        
        # Should be positive for positive R
        self.assertGreater(L_EH, 0)
        
        # Check scaling with R
        L_EH_2R = lagrangian_einstein_hilbert(2*R, sqrt_g, G_NEWTON)
        self.assertAlmostEqual(L_EH_2R, 2*L_EH, places=15)
    
    def test_kinetic_term(self):
        """Test kinetic term for Ψ field."""
        # Minkowski metric in (-,+,+,+) signature
        g_inv = np.diag([-1.0, 1.0, 1.0, 1.0])
        nabla_Psi = np.array([1.0, 0.5, 0.3, 0.2])  # Example gradient
        sqrt_g = 1.0
        
        L_kinetic = lagrangian_kinetic_psi(nabla_Psi, g_inv, sqrt_g)
        
        # Should be finite (can be positive or negative in Minkowski signature)
        self.assertTrue(np.isfinite(L_kinetic))
        
        # Check zero gradient gives zero
        nabla_Psi_zero = np.zeros(4)
        L_zero = lagrangian_kinetic_psi(nabla_Psi_zero, g_inv, sqrt_g)
        self.assertAlmostEqual(L_zero, 0.0, places=15)
    
    def test_potential_term(self):
        """Test effective potential with non-minimal coupling."""
        Psi = 1.0 + 0j
        R = 1e-20
        sqrt_g = 1.0
        
        L_pot = lagrangian_potential(Psi, R, OMEGA_0, XI_COUPLING, sqrt_g)
        
        # Should be negative (potential energy)
        self.assertLess(L_pot, 0)
        
        # Check scaling with |Ψ|²
        Psi_2 = 2.0 + 0j
        L_pot_2 = lagrangian_potential(Psi_2, R, OMEGA_0, XI_COUPLING, sqrt_g)
        self.assertAlmostEqual(L_pot_2, 4*L_pot, places=10)
    
    def test_modulation_term(self):
        """Test vibrational modulation term."""
        Psi = 1.0 + 0j
        R = 1e-20
        t = 0.0  # At t=0, cos(2πf₀t) = 1
        sqrt_g = 1.0
        
        L_mod = lagrangian_modulation(Psi, R, t, F_0, ZETA_COUPLING, sqrt_g)
        
        # Check periodicity
        T = 1.0 / F_0  # Period
        L_mod_T = lagrangian_modulation(Psi, R, T, F_0, ZETA_COUPLING, sqrt_g)
        self.assertAlmostEqual(L_mod, L_mod_T, places=10)
        
        # At t = T/4, cos should be 0
        L_mod_quarter = lagrangian_modulation(Psi, R, T/4, F_0, ZETA_COUPLING, sqrt_g)
        self.assertAlmostEqual(L_mod_quarter, 0.0, places=10)


class TestEOVEquation(unittest.TestCase):
    """Test the Equation of Vibrational Origin."""
    
    def test_eov_structure(self):
        """Test structure of EOV equation."""
        Psi = 1.0 + 0j
        box_Psi = -OMEGA_0**2  # For oscillating solution
        R = 0.0  # Flat spacetime
        t = 0.0
        params = LagrangianParameters()
        
        eov = eov_equation(Psi, box_Psi, R, t, params)
        
        # Should be complex
        self.assertTrue(isinstance(eov, (complex, np.complex128)))
    
    def test_eov_flat_spacetime_R_zero(self):
        """Test EOV in flat spacetime with R=0."""
        params = LagrangianParameters()
        
        # For R=0 and t=0, EOV reduces to: □Ψ - ω₀²Ψ = 0
        Psi = 1.0 + 0j
        box_Psi = OMEGA_0**2 * Psi  # Exact solution
        
        eov = eov_equation(Psi, box_Psi, R=0, t=0, params=params)
        
        # Should be approximately zero
        self.assertLess(abs(eov), 1e-10)
    
    def test_eov_forcing_term(self):
        """Test vibrational forcing term in EOV."""
        params = LagrangianParameters()
        
        Psi = 1.0 + 0j
        box_Psi = 0.0 + 0j
        R = 1e-10  # Need larger R for visible effect
        
        # At t=0, cos(2πf₀t) = 1
        eov_0 = eov_equation(Psi, box_Psi, R, t=0.0, params=params)
        
        # At t=T/2, cos(2πf₀t) = -1
        T = 1.0 / F_0
        eov_half = eov_equation(Psi, box_Psi, R, t=T/2, params=params)
        
        # Forcing term should flip sign, creating different EOV values
        # The difference should be ~4 × zeta_coupling × R (factor of 2 from cos, 2 from sign flip)
        expected_diff = 4 * params.zeta_coupling * R
        actual_diff = abs(eov_0 - eov_half)
        
        # Should have non-zero difference due to modulation
        self.assertGreater(actual_diff, 0)
        self.assertAlmostEqual(actual_diff, expected_diff, places=5)


class TestNumericalSolver(unittest.TestCase):
    """Test numerical solver for EOV."""
    
    def test_solver_flat_spacetime(self):
        """Test solver in flat spacetime."""
        t = np.linspace(0, 0.1, 100)  # 100 ms
        Psi_0 = 1.0 + 0j
        dPsi_0 = 0.0 + 0j
        
        Psi_sol, dPsi_sol = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=0)
        
        # Check length
        self.assertEqual(len(Psi_sol), len(t))
        self.assertEqual(len(dPsi_sol), len(t))
        
        # Check initial condition
        self.assertAlmostEqual(abs(Psi_sol[0]), abs(Psi_0), places=5)
        
        # Check oscillation (should have multiple zero crossings)
        zero_crossings = np.where(np.diff(np.sign(Psi_sol.real)))[0]
        self.assertGreater(len(zero_crossings), 5)  # Should oscillate at ~141.7 Hz
    
    def test_solver_energy_conservation(self):
        """Test approximate energy conservation in flat spacetime."""
        t = np.linspace(0, 1.0, 1000)
        Psi_0 = 1.0 + 0j
        dPsi_0 = 0.0 + 0j
        
        Psi_sol, dPsi_sol = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=0)
        
        # Energy ~ |∂Ψ/∂t|² + ω₀²|Ψ|²
        energy = abs(dPsi_sol)**2 + OMEGA_0**2 * abs(Psi_sol)**2
        
        # Energy should be approximately conserved
        energy_std = np.std(energy) / np.mean(energy)
        self.assertLess(energy_std, 0.1)  # Within 10%


class TestActionFunctional(unittest.TestCase):
    """Test action functional."""
    
    def test_action_structure(self):
        """Test action functional computation."""
        # Create simple field configuration
        g_metric = np.diag([-1.0, 1.0, 1.0, 1.0])
        g_inv = np.diag([-1.0, 1.0, 1.0, 1.0])
        
        config = FieldConfiguration(
            g_metric=g_metric,
            sqrt_minus_g=1.0,
            R_scalar=1e-20,
            Psi=1.0+0j,
            nabla_Psi=np.array([0.1, 0.0, 0.0, 0.0]),
            t=0.0,
            x=np.array([0.0, 0.0, 0.0])
        )
        
        params = LagrangianParameters()
        
        # Compute action for a single point (approximate)
        field_history = [config]
        g_inv_history = [g_inv]
        d4x = 1e-30  # Small spacetime volume
        
        action = action_functional(field_history, params, g_inv_history, d4x)
        
        # Action should be finite
        self.assertTrue(np.isfinite(action))


class TestEnergyMomentumTensor(unittest.TestCase):
    """Test energy-momentum tensor for Ψ field."""
    
    def test_tensor_structure(self):
        """Test structure of T^(Ψ)_μν."""
        g_metric = np.diag([-1.0, 1.0, 1.0, 1.0])
        g_inv = np.diag([-1.0, 1.0, 1.0, 1.0])
        
        config = FieldConfiguration(
            g_metric=g_metric,
            sqrt_minus_g=1.0,
            R_scalar=0.0,
            Psi=1.0+0j,
            nabla_Psi=np.array([1.0, 0.0, 0.0, 0.0]),
            t=0.0,
            x=np.array([0.0, 0.0, 0.0])
        )
        
        params = LagrangianParameters()
        
        T_psi = energy_momentum_tensor_psi(config, g_inv, params)
        
        # Should be 4×4 matrix
        self.assertEqual(T_psi.shape, (4, 4))
        
        # Should be real
        self.assertTrue(np.all(np.isreal(T_psi)))
        
        # Should be symmetric (approximately)
        self.assertTrue(np.allclose(T_psi, T_psi.T, atol=1e-10))


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_compute_zeta_prime_high_precision(self):
        """Test high-precision computation of ζ'(1/2)."""
        zeta_p_50 = compute_zeta_prime_half(precision=50)
        zeta_p_100 = compute_zeta_prime_half(precision=100)
        
        # Both should be close to -3.922
        self.assertAlmostEqual(zeta_p_50, -3.922, places=2)
        self.assertAlmostEqual(zeta_p_100, -3.922, places=2)
        
        # Higher precision should be more accurate
        self.assertTrue(abs(zeta_p_100 - ZETA_PRIME_HALF) <= abs(zeta_p_50 - ZETA_PRIME_HALF))


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency of the formulation."""
    
    def test_units_consistency(self):
        """Test dimensional consistency of constants."""
        # G has units [m³ kg⁻¹ s⁻²]
        # ω₀ has units [rad/s] = [s⁻¹]
        # R has units [m⁻²]
        
        # ω₀² should have units [s⁻²]
        omega_sq = OMEGA_0**2
        self.assertGreater(omega_sq, 0)
        
        # ξR should have units [s⁻²] when ξ is dimensionless and R is [m⁻²]
        # This requires ξ to absorb spatial scale
        # In natural units c=1, [m] = [s], so ξR is dimensionless
        
        # ZETA_COUPLING should be dimensionless
        self.assertTrue(np.isfinite(ZETA_COUPLING))
    
    def test_frequency_range(self):
        """Test that f₀ is in reasonable range."""
        # f₀ should be in Hz range (not MHz or kHz)
        self.assertGreater(F_0, 100)
        self.assertLess(F_0, 200)
        
        # Should be exactly 141.70001 Hz (5 decimal places - qcal.constants precision)
        self.assertAlmostEqual(F_0, 141.70001, places=5)
    
    def test_conformal_coupling(self):
        """Test that ξ = 1/6 is conformal coupling value."""
        self.assertAlmostEqual(XI_COUPLING, 1.0/6.0, places=10)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestLagrangianComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestEOVEquation))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalSolver))
    suite.addTests(loader.loadTestsFromTestCase(TestActionFunctional))
    suite.addTests(loader.loadTestsFromTestCase(TestEnergyMomentumTensor))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
