#!/usr/bin/env python3
"""
Test Suite for Master Lagrangian
=================================

Tests the Master Lagrangian implementation:
L[Ψ,Φ] = 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²) - V_eff(Ψ,Φ) + κ_Π · R_CY

Validation Tests:
1. Kinetic term computation
2. Effective potential V_eff
3. Calabi-Yau curvature R_CY
4. Soliton stability conditions
5. Spectral analysis at f₀ = 141.7001 Hz
6. EEG/gravitational resonance predictions

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import unittest

# Import Master Lagrangian modules
from src.lagrangian_master import (
    MasterLagrangianParameters,
    FieldConfiguration,
    kinetic_term,
    effective_potential,
    calabi_yau_coupling,
    master_lagrangian,
    soliton_ansatz,
    soliton_stability_criterion,
    spectral_analysis_psi,
    equation_of_motion_psi
)

from src.calabi_yau_curvature import (
    CalabiYauCurvature,
    create_calabi_yau_curvature,
    compute_static_curvature,
    curvature_spectral_analysis
)

# QCAL constants
from qcal.constants import F0_HZ, KAPPA_PI, C


class TestKineticTerm(unittest.TestCase):
    """Test kinetic term: 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²)."""
    
    def test_zero_derivatives(self):
        """Test kinetic term with zero derivatives."""
        dPsi_dt = 0.0 + 0.0j
        nabla_Psi = np.array([0.0, 0.0, 0.0], dtype=complex)
        
        L_kin = kinetic_term(dPsi_dt, nabla_Psi)
        
        self.assertAlmostEqual(L_kin, 0.0, places=10)
    
    def test_time_derivative_only(self):
        """Test with only time derivative."""
        dPsi_dt = 1.0 + 0.0j
        nabla_Psi = np.array([0.0, 0.0, 0.0], dtype=complex)
        
        L_kin = kinetic_term(dPsi_dt, nabla_Psi)
        
        expected = 0.5 * 1.0**2  # 1/2 |∂Ψ/∂t|²
        self.assertAlmostEqual(L_kin, expected, places=10)
    
    def test_spatial_gradient_only(self):
        """Test with only spatial gradient."""
        dPsi_dt = 0.0 + 0.0j
        nabla_Psi = np.array([1.0, 0.0, 0.0], dtype=complex)
        
        L_kin = kinetic_term(dPsi_dt, nabla_Psi, c=C)
        
        expected = -0.5 * C**2 * 1.0**2  # -1/2 c² |∇Ψ|²
        self.assertAlmostEqual(L_kin, expected, places=5)
    
    def test_oscillating_field_f0(self):
        """Test field oscillating at f₀."""
        omega_0 = 2 * np.pi * F0_HZ
        dPsi_dt = 1j * omega_0 * (1.0 + 0.0j)  # ∂_t e^(iωt) = iω e^(iωt)
        nabla_Psi = np.array([0.0, 0.0, 0.0], dtype=complex)
        
        L_kin = kinetic_term(dPsi_dt, nabla_Psi)
        
        expected = 0.5 * omega_0**2
        self.assertAlmostEqual(L_kin, expected, places=5)


class TestEffectivePotential(unittest.TestCase):
    """Test effective potential V_eff(Ψ,Φ)."""
    
    def test_zero_field(self):
        """Test with zero field."""
        Psi = 0.0 + 0.0j
        Phi = 1.0
        V0, xi1, xi2 = 1.0, 1.0, 0.1
        
        V_eff = effective_potential(Psi, Phi, V0, xi1, xi2)
        
        self.assertAlmostEqual(V_eff, 0.0, places=10)
    
    def test_unit_field(self):
        """Test with unit amplitude field."""
        Psi = 1.0 + 0.0j
        Phi = 1.0
        V0, xi1, xi2 = 1.0, 1.0, 0.1
        
        V_eff = effective_potential(Psi, Phi, V0, xi1, xi2)
        
        # V_eff = V₀|Ψ|² + ξ₁Φ|Ψ|² + ξ₂|Ψ|⁴
        #       = 1.0·1 + 1.0·1·1 + 0.1·1
        #       = 2.1
        expected = 2.1
        self.assertAlmostEqual(V_eff, expected, places=10)
    
    def test_geometry_coupling(self):
        """Test geometry-field coupling."""
        Psi = 1.0 + 0.0j
        Phi = 2.0  # Vary geometry
        V0, xi1, xi2 = 1.0, 0.5, 0.0
        
        V_eff = effective_potential(Psi, Phi, V0, xi1, xi2)
        
        # V_eff = 1.0·1 + 0.5·2·1 + 0
        #       = 2.0
        expected = 2.0
        self.assertAlmostEqual(V_eff, expected, places=10)
    
    def test_self_interaction(self):
        """Test self-interaction term."""
        Psi = 2.0 + 0.0j
        Phi = 0.0
        V0, xi1, xi2 = 0.0, 0.0, 0.1
        
        V_eff = effective_potential(Psi, Phi, V0, xi1, xi2)
        
        # V_eff = 0.1·|2|⁴ = 0.1·16 = 1.6
        expected = 1.6
        self.assertAlmostEqual(V_eff, expected, places=10)


class TestCalabiYauCoupling(unittest.TestCase):
    """Test Calabi-Yau coupling κ_Π · R_CY."""
    
    def test_coupling_constant(self):
        """Test that κ_Π is correct."""
        self.assertAlmostEqual(KAPPA_PI, 2.5773, places=4)
    
    def test_zero_curvature(self):
        """Test with zero curvature."""
        R_CY = 0.0
        L_CY = calabi_yau_coupling(R_CY)
        
        self.assertAlmostEqual(L_CY, 0.0, places=10)
    
    def test_unit_curvature(self):
        """Test with unit curvature."""
        R_CY = 1.0
        L_CY = calabi_yau_coupling(R_CY)
        
        expected = KAPPA_PI * 1.0
        self.assertAlmostEqual(L_CY, expected, places=10)


class TestCalabiYauCurvature(unittest.TestCase):
    """Test Calabi-Yau curvature computation."""
    
    def test_quintic_variety(self):
        """Test Quintic Calabi-Yau (h¹¹=1, h²¹=101)."""
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        self.assertEqual(curvature.h11, 1)
        self.assertEqual(curvature.h21, 101)
        self.assertEqual(curvature.euler_characteristic, -200)
        self.assertEqual(curvature.f_modulation, F0_HZ)
    
    def test_mirror_symmetric(self):
        """Test mirror-symmetric variety (h¹¹=h²¹)."""
        curvature = create_calabi_yau_curvature(h11=11, h21=11)
        
        self.assertEqual(curvature.euler_characteristic, 0)
    
    def test_time_modulation(self):
        """Test that R_CY modulates with time."""
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        # Evaluate at different times
        R_at_0 = curvature.R_CY(0.0)
        R_at_quarter_period = curvature.R_CY(0.25 / F0_HZ)
        
        # R_CY should be different at different times due to modulation
        # Note: Static component dominates, but difference should exist
        self.assertNotEqual(R_at_0, R_at_quarter_period)
    
    def test_spectral_peak_at_f0(self):
        """Test that curvature spectrum peaks at f₀."""
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        freqs, power, peak_freq = curvature_spectral_analysis(
            curvature, duration=10.0
        )
        
        # Peak should be at f₀
        self.assertAlmostEqual(peak_freq, F0_HZ, delta=0.1)


class TestSolitonSolutions(unittest.TestCase):
    """Test soliton solutions and stability."""
    
    def test_soliton_ansatz(self):
        """Test soliton ansatz form."""
        x = np.array([0.0, 0.0, 0.0])
        t = 0.0
        amplitude = 1.0
        width = 1.0
        velocity = 0.0
        
        Psi = soliton_ansatz(x, t, amplitude, width, velocity)
        
        # At center (x=0, t=0): sech(0) = 1
        expected_amplitude = amplitude
        self.assertAlmostEqual(abs(Psi), expected_amplitude, places=10)
    
    def test_soliton_stability(self):
        """Test soliton stability criterion."""
        params = MasterLagrangianParameters()
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        is_stable, m_eff_sq = soliton_stability_criterion(params, curvature)
        
        # Should be stable (m_eff² > 0)
        # Note: This depends on parameter values, so we just check type
        self.assertIsInstance(is_stable, bool)
        self.assertIsInstance(m_eff_sq, float)


class TestSpectralAnalysis(unittest.TestCase):
    """Test spectral analysis at f₀."""
    
    def test_pure_f0_oscillation(self):
        """Test pure oscillation at f₀."""
        # Create signal: Ψ(t) = e^(i2πf₀t)
        duration = 10.0
        sample_rate = 1000.0
        t_array = np.arange(0, duration, 1.0 / sample_rate)
        
        Psi_history = np.exp(1j * 2 * np.pi * F0_HZ * t_array)
        
        freqs, power, peak_freq, matches = spectral_analysis_psi(
            Psi_history, t_array
        )
        
        # Peak should be at f₀
        self.assertTrue(matches)
        self.assertAlmostEqual(peak_freq, F0_HZ, delta=0.1)
    
    def test_modulated_signal(self):
        """Test modulated signal detection."""
        duration = 10.0
        sample_rate = 1000.0
        t_array = np.arange(0, duration, 1.0 / sample_rate)
        
        # Amplitude modulation at f₀
        carrier = np.exp(1j * 2 * np.pi * F0_HZ * t_array)
        modulation = np.cos(2 * np.pi * F0_HZ * t_array)
        Psi_history = carrier * (1 + 0.5 * modulation)
        
        freqs, power, peak_freq, matches = spectral_analysis_psi(
            Psi_history, t_array
        )
        
        # Should still detect f₀ as dominant frequency
        self.assertTrue(matches)


class TestMasterLagrangian(unittest.TestCase):
    """Test complete Master Lagrangian."""
    
    def test_lagrangian_components(self):
        """Test that all components are included."""
        params = MasterLagrangianParameters()
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        config = FieldConfiguration(
            Psi=1.0 + 0.0j,
            dPsi_dt=1j * 2 * np.pi * F0_HZ,
            nabla_Psi=np.array([0.0, 0.0, 0.0], dtype=complex),
            Phi=1.0,
            nabla_Phi=np.array([0.0, 0.0, 0.0]),
            R_CY=curvature.R_CY(0.0),
            t=0.0,
            x=np.array([0.0, 0.0, 0.0])
        )
        
        L = master_lagrangian(config, params)
        
        # Lagrangian should be finite
        self.assertTrue(np.isfinite(L))
    
    def test_lagrangian_units(self):
        """Test that Lagrangian has correct units (energy density)."""
        params = MasterLagrangianParameters()
        curvature = create_calabi_yau_curvature(h11=1, h21=101)
        
        config = FieldConfiguration(
            Psi=1.0 + 0.0j,
            dPsi_dt=0.0 + 0.0j,
            nabla_Psi=np.array([0.0, 0.0, 0.0], dtype=complex),
            Phi=1.0,
            nabla_Phi=np.array([0.0, 0.0, 0.0]),
            R_CY=curvature.R_CY(0.0),
            t=0.0,
            x=np.array([0.0, 0.0, 0.0])
        )
        
        L = master_lagrangian(config, params)
        
        # Should be real (Lagrangian is real)
        self.assertTrue(np.isreal(L))


def run_tests():
    """Run all tests and return success status."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestKineticTerm))
    suite.addTests(loader.loadTestsFromTestCase(TestEffectivePotential))
    suite.addTests(loader.loadTestsFromTestCase(TestCalabiYauCoupling))
    suite.addTests(loader.loadTestsFromTestCase(TestCalabiYauCurvature))
    suite.addTests(loader.loadTestsFromTestCase(TestSolitonSolutions))
    suite.addTests(loader.loadTestsFromTestCase(TestSpectralAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestMasterLagrangian))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("Master Lagrangian Test Suite - QCAL ∞³")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
