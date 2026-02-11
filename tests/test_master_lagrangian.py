#!/usr/bin/env python3
"""
Unit Tests for Master Lagrangian
================================

Tests for the unified master Lagrangian implementation:
- Lagrangian component calculations
- Equations of motion
- Energy conservation
- Consciousness emergence threshold

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
from qcal.master_lagrangian import (
    MasterLagrangianParameters,
    FieldState,
    ConsciousnessMetrics,
    L_QCAL,
    L_FIBRATION,
    L_COUPLING,
    L_MASTER,
    equation_of_motion_Psi,
    equation_of_motion_Phi,
    compute_intersection_parameter,
    check_consciousness_emergence,
    compute_quantized_spectrum,
    compute_total_energy,
    verify_energy_conservation,
    F0_HZ,
    PSI_INTERSECTION_CRITICAL
)


class TestMasterLagrangianParameters(unittest.TestCase):
    """Test parameter initialization."""
    
    def test_default_parameters(self):
        """Test default parameter values."""
        params = MasterLagrangianParameters()
        
        self.assertAlmostEqual(params.f_0, F0_HZ, places=4)
        self.assertAlmostEqual(params.f_0, 141.7001, places=4)
        self.assertGreater(params.omega_0, 0)
        self.assertGreater(params.kappa_pi, 0)
        self.assertGreater(params.lambda_G, 0)
        self.assertGreater(params.gamma_GD, 0)
    
    def test_fundamental_frequency(self):
        """Test f₀ = 141.7001 Hz is correctly set."""
        params = MasterLagrangianParameters()
        self.assertAlmostEqual(params.f_0, 141.7001, places=4)


class TestLagrangianComponents(unittest.TestCase):
    """Test individual Lagrangian components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = MasterLagrangianParameters()
        self.state = FieldState(
            Psi=1.0 + 0.0j,
            Phi=0.5,
            nabla_Psi=np.array([0.1j, 0.0, 0.0, 0.0], dtype=complex),
            nabla_Phi=np.array([0.2, 0.0, 0.0, 0.0]),
            R_scalar=0.1,
            berry_phase=np.pi/2,
            t=0.0
        )
    
    def test_L_QCAL_returns_real(self):
        """Test L_QCAL returns real value."""
        L = L_QCAL(self.state, self.params)
        self.assertIsInstance(L, float)
        self.assertTrue(np.isfinite(L))
    
    def test_L_QCAL_has_kinetic_term(self):
        """Test L_QCAL includes kinetic energy."""
        # State with gradient
        state_with_gradient = FieldState(
            Psi=1.0,
            nabla_Psi=np.array([1.0j, 0.0, 0.0, 0.0], dtype=complex),
            t=0.0
        )
        
        # State without gradient
        state_no_gradient = FieldState(
            Psi=1.0,
            nabla_Psi=np.zeros(4, dtype=complex),
            t=0.0
        )
        
        L_with = L_QCAL(state_with_gradient, self.params)
        L_without = L_QCAL(state_no_gradient, self.params)
        
        # Kinetic energy should make them different
        self.assertNotAlmostEqual(L_with, L_without, places=5)
    
    def test_L_FIBRATION_returns_real(self):
        """Test L_FIBRATION returns real value."""
        Psi_intersection = 0.9
        L = L_FIBRATION(self.state, Psi_intersection, self.params)
        self.assertIsInstance(L, float)
        self.assertTrue(np.isfinite(L))
    
    def test_L_FIBRATION_berry_phase_dependence(self):
        """Test L_FIBRATION depends on Berry phase."""
        Psi_intersection = 0.9
        
        # Different Berry phases
        state1 = FieldState(berry_phase=0.0)
        state2 = FieldState(berry_phase=np.pi)
        
        L1 = L_FIBRATION(state1, Psi_intersection, self.params)
        L2 = L_FIBRATION(state2, Psi_intersection, self.params)
        
        self.assertNotAlmostEqual(L1, L2, places=5)
    
    def test_L_FIBRATION_intersection_dependence(self):
        """Test L_FIBRATION depends on intersection parameter."""
        # Low intersection (far from consciousness)
        L_low = L_FIBRATION(self.state, 0.1, self.params)
        
        # High intersection (near consciousness)
        L_high = L_FIBRATION(self.state, 0.95, self.params)
        
        # Higher intersection should be energetically favored
        self.assertGreater(L_high, L_low)
    
    def test_L_COUPLING_returns_real(self):
        """Test L_COUPLING returns real value."""
        Psi_field = 1.0 + 0.5j
        Psi_geometric = 0.8 + 0.3j
        
        L = L_COUPLING(Psi_field, Psi_geometric, self.params)
        self.assertIsInstance(L, float)
        self.assertTrue(np.isfinite(L))
    
    def test_L_COUPLING_alignment_dependence(self):
        """Test L_COUPLING maximized when states align."""
        Psi_field = 1.0 + 0.0j
        
        # Aligned geometric state
        Psi_geom_aligned = 1.0 + 0.0j
        L_aligned = L_COUPLING(Psi_field, Psi_geom_aligned, self.params)
        
        # Orthogonal geometric state
        Psi_geom_orthogonal = 0.0 + 1.0j
        L_orthogonal = L_COUPLING(Psi_field, Psi_geom_orthogonal, self.params)
        
        # Aligned should have larger coupling
        self.assertGreater(abs(L_aligned), abs(L_orthogonal))
    
    def test_L_MASTER_combines_components(self):
        """Test L_MASTER properly combines all components."""
        Psi_intersection = 0.9
        Psi_geometric = 0.8 + 0.3j
        
        L_total = L_MASTER(self.state, Psi_intersection, Psi_geometric, self.params)
        
        # Should be real and finite
        self.assertIsInstance(L_total, float)
        self.assertTrue(np.isfinite(L_total))


class TestEquationsOfMotion(unittest.TestCase):
    """Test equations of motion derived from variational principle."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = MasterLagrangianParameters()
        self.state = FieldState(
            Psi=1.0 + 0.0j,
            Phi=0.5,
            R_scalar=0.1,
            t=0.0
        )
    
    def test_equation_Psi_returns_complex(self):
        """Test Ψ equation of motion returns complex number."""
        Psi_geometric = 0.8 + 0.3j
        eom = equation_of_motion_Psi(self.state, Psi_geometric, self.params)
        
        self.assertIsInstance(eom, (complex, np.complexfloating))
        self.assertTrue(np.isfinite(eom.real))
        self.assertTrue(np.isfinite(eom.imag))
    
    def test_equation_Phi_returns_real(self):
        """Test Φ equation of motion returns real number."""
        eom = equation_of_motion_Phi(self.state, self.params)
        
        self.assertIsInstance(eom, (float, np.floating))
        self.assertTrue(np.isfinite(eom))
    
    def test_equation_Psi_curvature_coupling(self):
        """Test Ψ equation includes curvature coupling."""
        Psi_geometric = 1.0 + 0.0j
        
        # Flat spacetime
        state_flat = FieldState(Psi=1.0, R_scalar=0.0, t=0.0)
        eom_flat = equation_of_motion_Psi(state_flat, Psi_geometric, self.params)
        
        # Curved spacetime
        state_curved = FieldState(Psi=1.0, R_scalar=1.0, t=0.0)
        eom_curved = equation_of_motion_Psi(state_curved, Psi_geometric, self.params)
        
        # Should be different
        self.assertNotAlmostEqual(abs(eom_flat), abs(eom_curved), places=5)


class TestConsciousnessEmergence(unittest.TestCase):
    """Test consciousness emergence criteria."""
    
    def test_intersection_parameter_range(self):
        """Test Ψ_∩ is in [0, 1]."""
        Psi_field = 1.0 + 0.0j
        Psi_geometric = 1.0 + 0.0j
        berry_phase = np.pi
        
        Psi_int = compute_intersection_parameter(Psi_field, Psi_geometric, berry_phase)
        
        self.assertGreaterEqual(Psi_int, 0.0)
        self.assertLessEqual(Psi_int, 1.0)
    
    def test_intersection_parameter_berry_phase_peak(self):
        """Test Ψ_∩ peaks at Berry phase = π."""
        Psi_field = 1.0 + 0.0j
        Psi_geometric = 1.0 + 0.0j
        
        # Berry phase at π
        Psi_int_pi = compute_intersection_parameter(Psi_field, Psi_geometric, np.pi)
        
        # Berry phase away from π
        Psi_int_zero = compute_intersection_parameter(Psi_field, Psi_geometric, 0.0)
        
        # Should be maximum at π
        self.assertGreater(Psi_int_pi, Psi_int_zero)
    
    def test_consciousness_emergence_threshold(self):
        """Test consciousness emerges at Ψ_∩ ≥ 0.888."""
        # Above threshold
        emerged = check_consciousness_emergence(
            Psi_intersection=0.9,
            berry_phase=np.pi,
            coherence=0.8
        )
        self.assertTrue(emerged)
        
        # Below threshold
        not_emerged = check_consciousness_emergence(
            Psi_intersection=0.8,
            berry_phase=np.pi,
            coherence=0.8
        )
        self.assertFalse(not_emerged)
    
    def test_consciousness_requires_berry_phase(self):
        """Test consciousness requires Berry phase ≥ π."""
        # Sufficient Berry phase
        emerged = check_consciousness_emergence(
            Psi_intersection=0.9,
            berry_phase=np.pi,
            coherence=0.8
        )
        self.assertTrue(emerged)
        
        # Insufficient Berry phase
        not_emerged = check_consciousness_emergence(
            Psi_intersection=0.9,
            berry_phase=0.1,
            coherence=0.8
        )
        self.assertFalse(not_emerged)
    
    def test_consciousness_requires_coherence(self):
        """Test consciousness requires coherence ≥ 0.7."""
        # Sufficient coherence
        emerged = check_consciousness_emergence(
            Psi_intersection=0.9,
            berry_phase=np.pi,
            coherence=0.75
        )
        self.assertTrue(emerged)
        
        # Insufficient coherence
        not_emerged = check_consciousness_emergence(
            Psi_intersection=0.9,
            berry_phase=np.pi,
            coherence=0.5
        )
        self.assertFalse(not_emerged)


class TestSpectralAnalysis(unittest.TestCase):
    """Test quantized spectrum calculation."""
    
    def test_spectrum_detects_f0(self):
        """Test spectrum detects f₀ = 141.7001 Hz."""
        params = MasterLagrangianParameters()
        
        # Create oscillating state at f₀
        dt = 1.0 / 4096  # 4096 Hz sampling
        duration = 1.0  # 1 second
        n_samples = int(duration / dt)
        
        state_history = []
        for i in range(n_samples):
            t = i * dt
            Psi_osc = np.exp(2j * np.pi * F0_HZ * t)
            state = FieldState(Psi=Psi_osc, t=t)
            state_history.append(state)
        
        # Compute spectrum
        freqs, power, metrics = compute_quantized_spectrum(state_history, params, dt)
        
        # Check peak frequency is near f₀
        peak_freq = metrics['peak_freq']
        self.assertAlmostEqual(peak_freq, F0_HZ, delta=5.0)
    
    def test_spectrum_returns_valid_arrays(self):
        """Test spectrum returns valid frequency and power arrays."""
        params = MasterLagrangianParameters()
        dt = 1.0 / 4096
        duration = 0.5
        n_samples = int(duration / dt)
        
        state_history = [FieldState(Psi=1.0, t=i*dt) for i in range(n_samples)]
        
        freqs, power, metrics = compute_quantized_spectrum(state_history, params, dt)
        
        self.assertEqual(len(freqs), len(power))
        self.assertTrue(all(f >= 0 for f in freqs))
        self.assertTrue(all(p >= 0 for p in power))
        
        # Check metrics
        self.assertIn('peak_freq', metrics)
        self.assertIn('peak_power', metrics)
        self.assertIn('f0_power', metrics)


class TestEnergyConservation(unittest.TestCase):
    """Test energy conservation."""
    
    def test_energy_is_real(self):
        """Test total energy is real."""
        params = MasterLagrangianParameters()
        state = FieldState(
            Psi=1.0,
            nabla_Psi=np.array([0.1j, 0.0, 0.0, 0.0], dtype=complex),
            t=0.0
        )
        Psi_intersection = 0.9
        Psi_geometric = 1.0 + 0.0j
        
        E = compute_total_energy(state, Psi_intersection, Psi_geometric, params)
        
        self.assertIsInstance(E, (float, np.floating))
        self.assertTrue(np.isfinite(E))
    
    def test_energy_conservation_constant_state(self):
        """Test energy conservation for constant state."""
        params = MasterLagrangianParameters()
        
        # Create constant state history
        n_steps = 100
        state_history = []
        Psi_int_history = []
        Psi_geom_history = []
        
        for i in range(n_steps):
            state = FieldState(
                Psi=1.0,
                Phi=0.5,
                nabla_Psi=np.array([0.1j, 0.0, 0.0, 0.0], dtype=complex),
                nabla_Phi=np.array([0.1, 0.0, 0.0, 0.0]),
                t=i * 0.01
            )
            state_history.append(state)
            Psi_int_history.append(0.9)
            Psi_geom_history.append(1.0 + 0.0j)
        
        # Verify conservation
        conserved, diagnostics = verify_energy_conservation(
            state_history,
            Psi_int_history,
            Psi_geom_history,
            params,
            tolerance=0.1
        )
        
        # Energy should be conserved for constant state
        self.assertTrue(conserved or diagnostics['relative_variation'] < 0.2)
        self.assertIn('E_mean', diagnostics)
        self.assertIn('E_std', diagnostics)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def test_complete_evolution_workflow(self):
        """Test complete workflow: initialization → evolution → analysis."""
        params = MasterLagrangianParameters()
        
        # Initialize
        state = FieldState(Psi=1.0+0.0j, Phi=0.5, t=0.0)
        Psi_intersection = compute_intersection_parameter(
            state.Psi,
            1.0+0.0j,
            np.pi/2
        )
        
        # Check valid initialization
        self.assertGreater(Psi_intersection, 0.0)
        self.assertLess(Psi_intersection, 1.0)
        
        # Compute Lagrangian
        L = L_MASTER(state, Psi_intersection, 1.0+0.0j, params)
        self.assertTrue(np.isfinite(L))
        
        # Compute energy
        E = compute_total_energy(state, Psi_intersection, 1.0+0.0j, params)
        self.assertTrue(np.isfinite(E))
    
    def test_f0_frequency_constant(self):
        """Test f₀ = 141.7001 Hz is consistently used."""
        params = MasterLagrangianParameters()
        
        # Verify f₀ in parameters
        self.assertAlmostEqual(params.f_0, 141.7001, places=4)
        
        # Verify f₀ in global constant
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)
        
        # Verify they match
        self.assertEqual(params.f_0, F0_HZ)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
