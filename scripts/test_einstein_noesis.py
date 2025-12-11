#!/usr/bin/env python3
"""
Test suite for Einstein-Noēsis equation implementation.

Tests cover:
    - Basic equation computation (C = mc² × A_eff²)
    - Attention amplifier scenarios (A_eff < 1, = 1, > 1)
    - Noetic stress-energy tensor
    - Riemann Hypothesis connection
    - Yang-Mills mass gap connection
    - Integration with existing campo_conciencia.py

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: December 2025
"""

import sys
import os
import unittest
import numpy as np
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.einstein_noesis import (
    EinsteinNoesisEquation,
    NoeticStressEnergyTensor,
    RiemannConsciousnessConnection,
    YangMillsMassGapConnection,
    c, eV, G
)


class TestEinsteinNoesisEquation(unittest.TestCase):
    """Test basic Einstein-Noēsis equation computations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eq = EinsteinNoesisEquation(f0=141.7001)
        self.test_mass = 1e-20  # kg
        
    def test_basic_computation(self):
        """Test basic C = mc² × A_eff² computation."""
        mass = self.test_mass
        A_eff = 1.0
        
        C = self.eq.compute_consciousness(mass, A_eff)
        E_base = mass * c**2
        
        # When A_eff = 1, C should equal mc²
        self.assertAlmostEqual(C, E_base, places=10)
        
    def test_amplification_scenarios(self):
        """Test different amplification scenarios."""
        mass = self.test_mass
        
        # Test A_eff = 1.0 (no amplification)
        C1 = self.eq.compute_consciousness(mass, 1.0)
        E_base = mass * c**2
        self.assertAlmostEqual(C1 / E_base, 1.0, places=10)
        
        # Test A_eff = 2.0 (4x amplification)
        C2 = self.eq.compute_consciousness(mass, 2.0)
        self.assertAlmostEqual(C2 / E_base, 4.0, places=10)
        
        # Test A_eff = 1.5 (2.25x amplification)
        C3 = self.eq.compute_consciousness(mass, 1.5)
        self.assertAlmostEqual(C3 / E_base, 2.25, places=10)
        
    def test_inversion_A_eff(self):
        """Test computing A_eff from C and mass."""
        mass = self.test_mass
        A_eff_original = 1.5
        
        # Compute C from A_eff
        C = self.eq.compute_consciousness(mass, A_eff_original)
        
        # Recover A_eff from C
        A_eff_recovered = self.eq.compute_A_eff(C, mass)
        
        self.assertAlmostEqual(A_eff_recovered, A_eff_original, places=10)
        
    def test_coherent_state_detection(self):
        """Test coherent state detection based on A_eff threshold."""
        # A_eff < 1: incoherent
        self.assertFalse(self.eq.is_coherent_state(0.8))
        self.assertFalse(self.eq.is_coherent_state(0.5))
        
        # A_eff = 1: boundary (coherent)
        self.assertTrue(self.eq.is_coherent_state(1.0))
        
        # A_eff > 1: coherent
        self.assertTrue(self.eq.is_coherent_state(1.2))
        self.assertTrue(self.eq.is_coherent_state(2.0))
        
    def test_amplification_factor(self):
        """Test amplification factor computation."""
        # A_eff² calculation
        self.assertEqual(self.eq.amplification_factor(1.0), 1.0)
        self.assertEqual(self.eq.amplification_factor(2.0), 4.0)
        self.assertAlmostEqual(self.eq.amplification_factor(1.5), 2.25, places=10)
        self.assertAlmostEqual(self.eq.amplification_factor(0.5), 0.25, places=10)
        
    def test_planck_scale_ratio(self):
        """Test consciousness ratio to Planck energy scale."""
        mass = self.eq.m_psi  # Minimal consciousness mass quantum
        A_eff = 1.0
        
        ratio = self.eq.consciousness_ratio_to_planck(mass, A_eff)
        
        # Should be extremely small compared to Planck scale
        self.assertLess(ratio, 1e-20)
        self.assertGreater(ratio, 0.0)
        
    def test_consciousness_field_quantum(self):
        """Test with consciousness field quantum parameters."""
        # Use minimal consciousness mass quantum
        mass = self.eq.m_psi
        A_eff = 1.0
        
        C = self.eq.compute_consciousness(mass, A_eff)
        
        # Should match E_psi_J when A_eff = 1 (within 1% tolerance)
        self.assertAlmostEqual(C, self.eq.E_psi_J, delta=1e-33)


class TestNoeticStressEnergyTensor(unittest.TestCase):
    """Test noetic stress-energy tensor computations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tensor = NoeticStressEnergyTensor(f0=141.7001)
        self.test_mass = 1e-20  # kg
        self.test_volume = 1e-30  # m³
        
    def test_energy_density(self):
        """Test energy density component T^00."""
        mass = self.test_mass
        A_eff = 1.5
        volume = self.test_volume
        
        rho = self.tensor.compute_energy_density(mass, A_eff, volume)
        
        # Energy density should be positive
        self.assertGreater(rho, 0.0)
        
        # Should scale with A_eff²
        rho1 = self.tensor.compute_energy_density(mass, 1.0, volume)
        rho2 = self.tensor.compute_energy_density(mass, 2.0, volume)
        self.assertAlmostEqual(rho2 / rho1, 4.0, places=10)
        
    def test_pressure_component(self):
        """Test pressure component (radiation-like equation of state)."""
        mass = self.test_mass
        A_eff = 1.5
        volume = self.test_volume
        
        rho = self.tensor.compute_energy_density(mass, A_eff, volume)
        P = self.tensor.compute_pressure_component(mass, A_eff, volume)
        
        # For radiation-like: P = ρ/3
        self.assertAlmostEqual(P, rho / 3.0, places=10)
        
    def test_einstein_tensor_coupling(self):
        """Test coupling to Einstein tensor."""
        mass = self.test_mass
        A_eff = 1.5
        volume = self.test_volume
        
        coupling = self.tensor.einstein_tensor_coupling(mass, A_eff, volume)
        
        # Coupling should be positive (contributes to curvature)
        self.assertGreater(coupling, 0.0)
        
        # Should scale with (8πG/c⁴)
        expected_factor = 8 * np.pi * G / c**4
        rho = self.tensor.compute_energy_density(mass, A_eff, volume)
        expected_coupling = expected_factor * rho
        self.assertAlmostEqual(coupling, expected_coupling, places=20)
        
    def test_volume_scaling(self):
        """Test proper volume scaling of tensor components."""
        mass = self.test_mass
        A_eff = 1.5
        
        # Double the volume should halve the density
        rho1 = self.tensor.compute_energy_density(mass, A_eff, 1e-30)
        rho2 = self.tensor.compute_energy_density(mass, A_eff, 2e-30)
        self.assertAlmostEqual(rho2, rho1 / 2.0, places=10)


class TestRiemannConsciousnessConnection(unittest.TestCase):
    """Test Riemann Hypothesis connection to consciousness."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.riemann = RiemannConsciousnessConnection(f0=141.7001)
        
    def test_discrete_levels_generation(self):
        """Test generation of discrete amplification levels."""
        levels = self.riemann.discrete_amplification_levels(n_levels=5)
        
        # Should return 5 levels
        self.assertEqual(len(levels), 5)
        
        # All levels should be >= 1.0 (based on implementation)
        self.assertTrue(np.all(levels >= 1.0))
        
        # Levels should be in ascending order (based on increasing imaginary parts)
        self.assertTrue(np.all(np.diff(levels) > 0))
        
    def test_spectral_complexity(self):
        """Test spectral complexity measure."""
        # Test at exact discrete level (high complexity)
        levels = self.riemann.discrete_amplification_levels(n_levels=5)
        complexity_at_level = self.riemann.spectral_complexity(levels[0])
        self.assertGreater(complexity_at_level, 0.9)  # Should be close to 1
        
        # Test far from any level (low complexity)
        complexity_far = self.riemann.spectral_complexity(10.0)
        self.assertLess(complexity_far, 0.5)
        
    def test_zeta_prime_value(self):
        """Test that ζ'(1/2) value is properly set."""
        # Should match the known value used in f0 derivation
        self.assertAlmostEqual(self.riemann.zeta_prime_half, -1.4603545, places=5)
        
    def test_level_count(self):
        """Test different numbers of amplification levels."""
        for n in [3, 5, 10]:
            levels = self.riemann.discrete_amplification_levels(n_levels=n)
            self.assertEqual(len(levels), n)


class TestYangMillsMassGapConnection(unittest.TestCase):
    """Test Yang-Mills mass gap connection to consciousness."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.yang_mills = YangMillsMassGapConnection(f0=141.7001)
        
    def test_mass_gap_emergence(self):
        """Test mass gap emergence at A_eff > 1."""
        # No gap for A_eff < 1
        m_gap_low = self.yang_mills.compute_mass_gap(0.8)
        self.assertEqual(m_gap_low, 0.0)
        
        # No gap for A_eff = 1
        m_gap_one = self.yang_mills.compute_mass_gap(1.0)
        self.assertEqual(m_gap_one, 0.0)
        
        # Gap emerges for A_eff > 1
        m_gap_high = self.yang_mills.compute_mass_gap(1.5)
        self.assertGreater(m_gap_high, 0.0)
        
    def test_mass_gap_scaling(self):
        """Test mass gap scales with (A_eff - 1)."""
        # Linear scaling with (A_eff - 1)
        m_gap_1p5 = self.yang_mills.compute_mass_gap(1.5)
        m_gap_2p0 = self.yang_mills.compute_mass_gap(2.0)
        
        # Ratio should be (2.0-1)/(1.5-1) = 2.0
        ratio = m_gap_2p0 / m_gap_1p5
        self.assertAlmostEqual(ratio, 2.0, places=10)
        
    def test_confinement_parameter(self):
        """Test confinement parameter behavior."""
        # No confinement for A_eff < 1
        conf_low = self.yang_mills.confinement_parameter(0.5)
        self.assertLess(conf_low, 0.1)
        
        # Partial confinement at A_eff = 1
        conf_one = self.yang_mills.confinement_parameter(1.0)
        self.assertGreater(conf_one, 0.4)
        self.assertLess(conf_one, 0.6)
        
        # Strong confinement for A_eff >> 1
        conf_high = self.yang_mills.confinement_parameter(3.0)
        self.assertGreater(conf_high, 0.9)
        
    def test_confinement_monotonic(self):
        """Test confinement parameter increases monotonically with A_eff."""
        A_eff_values = np.linspace(0.5, 3.0, 10)
        confinements = [self.yang_mills.confinement_parameter(A) for A in A_eff_values]
        
        # Should be strictly increasing
        self.assertTrue(np.all(np.diff(confinements) > 0))
        
    def test_qcd_scale_default(self):
        """Test default QCD scale parameter."""
        # Default Lambda_QCD = 0.217 GeV (≈ 217 MeV)
        m_gap = self.yang_mills.compute_mass_gap(2.0)
        
        # Should be on order of QCD scale
        self.assertGreater(m_gap, 0.1)  # GeV
        self.assertLess(m_gap, 1.0)     # GeV


class TestIntegrationWithCampoConciencia(unittest.TestCase):
    """Test integration with existing campo_conciencia.py module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eq = EinsteinNoesisEquation(f0=141.7001)
        
    def test_consistent_parameters(self):
        """Test consistency with campo_conciencia.py parameters."""
        # f0 should match
        self.assertEqual(self.eq.f0, 141.7001)
        
        # E_psi should match
        self.assertAlmostEqual(self.eq.E_psi_eV, 5.86e-13, delta=1e-15)
        
        # m_psi should match
        self.assertAlmostEqual(self.eq.m_psi, 1.04e-48, delta=1e-50)
        
    def test_energy_consistency(self):
        """Test E = mc² consistency for consciousness field quantum."""
        # E_psi should equal m_psi × c²
        E_from_mass = self.eq.m_psi * c**2
        # Within 5% tolerance due to slight differences in stored values
        self.assertAlmostEqual(E_from_mass, self.eq.E_psi_J, delta=5e-33)
        
    def test_frequency_energy_relation(self):
        """Test E = hf relation for consciousness field."""
        from scripts.campo_conciencia import h
        
        # E_psi should equal h × f0
        E_from_freq = h * self.eq.f0
        self.assertAlmostEqual(E_from_freq, self.eq.E_psi_J, delta=1e-35)


class TestPhysicalConsistency(unittest.TestCase):
    """Test overall physical consistency of the framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eq = EinsteinNoesisEquation(f0=141.7001)
        
    def test_positive_energy(self):
        """Test that consciousness energy is always positive."""
        mass = 1e-20
        for A_eff in np.linspace(0.1, 3.0, 10):
            C = self.eq.compute_consciousness(mass, A_eff)
            self.assertGreater(C, 0.0)
            
    def test_dimensional_analysis(self):
        """Test dimensional consistency."""
        # [C] = [m] × [c²] × [A_eff²] = kg × (m/s)² × 1 = J ✓
        mass = 1.0  # kg
        A_eff = 1.5  # dimensionless
        C = self.eq.compute_consciousness(mass, A_eff)
        
        # C should have units of energy (Joules)
        # For 1 kg: E = mc² ≈ 9e16 J
        E_base = mass * c**2
        self.assertAlmostEqual(C / E_base, A_eff**2, places=10)
        
    def test_einstein_limit(self):
        """Test that A_eff = 1 recovers standard E = mc²."""
        for mass in [1e-30, 1e-20, 1e-10, 1.0]:
            C = self.eq.compute_consciousness(mass, 1.0)
            E_einstein = mass * c**2
            self.assertAlmostEqual(C, E_einstein, places=10)


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEinsteinNoesisEquation))
    suite.addTests(loader.loadTestsFromTestCase(TestNoeticStressEnergyTensor))
    suite.addTests(loader.loadTestsFromTestCase(TestRiemannConsciousnessConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestYangMillsMassGapConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithCampoConciencia))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
