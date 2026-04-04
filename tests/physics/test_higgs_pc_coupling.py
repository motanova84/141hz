#!/usr/bin/env python3
"""
Tests for Higgs-PC Coupling Mechanism

Tests the interaction Lagrangian 𝓛_int = -g_eff ψ†ψ H
and verifies the modulated mass behavior at f₀ = 141.7001 Hz.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
import math
import sys
import os

# Add physics directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from physics.higgs_pc_coupling import (
    ConstantesHiggsPC,
    PC_Higgs_Coupling,
    HiggsDetectorSignature,
    higgs_pc_coupling_activar,
    calcular_masa_modulada,
    calcular_ventanas_transparencia
)


class TestConstantesHiggsPC(unittest.TestCase):
    """Test the Higgs-PC constants."""
    
    def test_fundamental_frequency(self):
        """Test that fundamental frequency is 141.7001 Hz."""
        self.assertAlmostEqual(ConstantesHiggsPC.F0, 141.7001, places=4)
    
    def test_higgs_mass(self):
        """Test that Higgs mass is 125 GeV."""
        self.assertAlmostEqual(ConstantesHiggsPC.M_HIGGS_GEV, 125.0, places=1)
    
    def test_coupling_constant(self):
        """Test that g_eff is 0.053 (5.3% modulation)."""
        self.assertAlmostEqual(ConstantesHiggsPC.G_EFF, 0.053, places=3)
    
    def test_effective_mass_range(self):
        """Test that effective mass range is correct."""
        expected_min = 125.0 * (1 - 0.053)
        expected_max = 125.0 * (1 + 0.053)
        
        self.assertAlmostEqual(ConstantesHiggsPC.M_MIN_GEV, expected_min, places=3)
        self.assertAlmostEqual(ConstantesHiggsPC.M_MAX_GEV, expected_max, places=3)
        
        # Should be approximately 118.375 GeV and 131.625 GeV
        self.assertAlmostEqual(ConstantesHiggsPC.M_MIN_GEV, 118.375, places=2)
        self.assertAlmostEqual(ConstantesHiggsPC.M_MAX_GEV, 131.625, places=2)
    
    def test_coherence_threshold(self):
        """Test coherence threshold is 0.888."""
        self.assertAlmostEqual(ConstantesHiggsPC.PSI_THRESHOLD, 0.888, places=3)


class TestPC_Higgs_Coupling(unittest.TestCase):
    """Test the PC-Higgs coupling mechanics."""
    
    def setUp(self):
        """Initialize coupling for tests."""
        self.coupling = PC_Higgs_Coupling()
    
    def test_initialization(self):
        """Test that coupling initializes correctly."""
        self.assertAlmostEqual(self.coupling.f0, 141.7001, places=4)
        self.assertAlmostEqual(self.coupling.g_eff, 0.053, places=3)
        self.assertAlmostEqual(self.coupling.omega, 2*math.pi*141.7001, places=3)
    
    def test_custom_initialization(self):
        """Test custom parameters."""
        coupling = PC_Higgs_Coupling(f0=150.0, g_eff=0.06)
        self.assertAlmostEqual(coupling.f0, 150.0)
        self.assertAlmostEqual(coupling.g_eff, 0.06)
    
    def test_modulated_mass_at_t0(self):
        """Test mass at t=0 (cos(0) = 1, maximum modulation)."""
        m_eff = self.coupling.modulated_mass(0.0)
        # m*(0) = 125 × (1 - 0.053×1) = 125 × 0.947 = 118.375
        self.assertAlmostEqual(m_eff, 118.375, places=2)
    
    def test_modulated_mass_at_quarter_period(self):
        """Test mass at T₀/4 (cos(π/2) = 0, no modulation)."""
        t = self.coupling.T0 / 4
        m_eff = self.coupling.modulated_mass(t)
        # m*(T₀/4) = 125 × (1 - 0.053×0) = 125
        self.assertAlmostEqual(m_eff, 125.0, places=2)
    
    def test_modulated_mass_at_half_period(self):
        """Test mass at T₀/2 (cos(π) = -1, maximum anti-modulation)."""
        t = self.coupling.T0 / 2
        m_eff = self.coupling.modulated_mass(t)
        # m*(T₀/2) = 125 × (1 - 0.053×(-1)) = 125 × 1.053 = 131.625
        self.assertAlmostEqual(m_eff, 131.625, places=2)
    
    def test_modulated_mass_at_full_period(self):
        """Test mass at T₀ (cos(2π) = 1, back to maximum modulation)."""
        t = self.coupling.T0
        m_eff = self.coupling.modulated_mass(t)
        # m*(T₀) = m*(0) = 118.375
        self.assertAlmostEqual(m_eff, 118.375, places=2)
    
    def test_modulated_mass_array(self):
        """Test that modulated_mass works with arrays."""
        times = np.array([0.0, self.coupling.T0/4, self.coupling.T0/2])
        masses = self.coupling.modulated_mass(times)
        
        self.assertEqual(len(masses), 3)
        self.assertAlmostEqual(masses[0], 118.375, places=2)
        self.assertAlmostEqual(masses[1], 125.0, places=2)
        self.assertAlmostEqual(masses[2], 131.625, places=2)
    
    def test_modulation_depth(self):
        """Test that modulation depth is correct (5.3%)."""
        # Calculate mass at extremes
        m_min = self.coupling.modulated_mass(0.0)
        m_max = self.coupling.modulated_mass(self.coupling.T0/2)
        
        # Verify range spans 2×g_eff of base mass
        expected_range = 2 * 0.053 * 125.0  # ≈ 13.25 GeV
        actual_range = m_max - m_min
        
        self.assertAlmostEqual(actual_range, expected_range, places=2)
    
    def test_mass_average_equals_base(self):
        """Test that average mass over full period equals base mass."""
        # Sample over multiple periods
        times = np.linspace(0, 10*self.coupling.T0, 10000)
        masses = self.coupling.modulated_mass(times)
        
        avg_mass = np.mean(masses)
        self.assertAlmostEqual(avg_mass, 125.0, places=1)
    
    def test_verify_coherence(self):
        """Test coherence verification."""
        times = np.linspace(0, 10*self.coupling.T0, 1000)
        
        # Should detect coherence (variance > 0)
        self.assertTrue(self.coupling.verify_coherence(times))
    
    def test_verify_coherence_single_point(self):
        """Test coherence with single point (no variance)."""
        # Single point has zero variance, no coherence detected
        times = np.array([0.0])
        self.assertFalse(self.coupling.verify_coherence(times))
    
    def test_transparency_windows(self):
        """Test calculation of transparency windows."""
        windows = self.coupling.calculate_transparency_windows(duration=1.0)
        
        # Check structure
        self.assertIn('times', windows)
        self.assertIn('masses', windows)
        self.assertIn('phase_transparency', windows)
        self.assertIn('num_windows', windows)
        
        # Number of windows should be approximately f₀ × duration
        expected_windows = int(141.7001 * 1.0)
        self.assertAlmostEqual(windows['num_windows'], expected_windows, delta=1)
        
        # Phase transparency should equal g_eff
        self.assertAlmostEqual(windows['phase_transparency'], 0.053, places=3)
    
    def test_transparency_windows_masses(self):
        """Test that transparency windows show minimum masses."""
        windows = self.coupling.calculate_transparency_windows(duration=0.1)
        
        # All masses should be close to minimum (118.375 GeV)
        # (transparency occurs at multiples of T₀ where cos(ω₀t) ≈ 1)
        for mass in windows['masses']:
            self.assertLess(mass, 120.0)  # Should be near 118.375
            self.assertGreater(mass, 116.0)
    
    def test_sideband_spectrum(self):
        """Test spectral sideband calculation."""
        sidebands = self.coupling.calculate_sideband_spectrum(num_sidebands=3)
        
        # Check structure
        self.assertIn('energies', sidebands)
        self.assertIn('orders', sidebands)
        self.assertIn('separation_GeV', sidebands)
        self.assertIn('separation_eV', sidebands)
        
        # Number of sidebands: -3, -2, -1, 0, +1, +2, +3 = 7
        self.assertEqual(len(sidebands['energies']), 7)
        self.assertEqual(len(sidebands['orders']), 7)
        
        # Central energy (order 0) should be base Higgs mass
        central_idx = 3
        self.assertAlmostEqual(sidebands['energies'][central_idx], 125.0, places=3)
        
        # Separation should be positive
        self.assertGreater(sidebands['separation_GeV'], 0)
        self.assertGreater(sidebands['separation_eV'], 0)
    
    def test_sideband_symmetry(self):
        """Test that sidebands are symmetric around base energy."""
        sidebands = self.coupling.calculate_sideband_spectrum(num_sidebands=5)
        
        energies = sidebands['energies']
        orders = sidebands['orders']
        
        # Find central index (order = 0)
        central_idx = np.where(orders == 0)[0][0]
        
        # Check symmetry: E[center + n] - E[center] ≈ E[center] - E[center - n]
        for n in range(1, 5):
            upper_diff = energies[central_idx + n] - energies[central_idx]
            lower_diff = energies[central_idx] - energies[central_idx - n]
            self.assertAlmostEqual(upper_diff, lower_diff, places=10)
    
    def test_symbiotic_transfer_rate(self):
        """Test symbiotic transfer rate calculation."""
        transfer = self.coupling.calculate_symbiotic_transfer_rate()
        
        # Check structure
        self.assertIn('rate_hz', transfer)
        self.assertIn('rate_kpps', transfer)
        self.assertIn('coherence', transfer)
        
        # With default parameters (N=7, Ψ=0.999999):
        # R = 7 × 141.7001 × 0.999999 ≈ 991.9 packets/second
        expected_rate_hz = 7 * 141.7001 * 0.999999
        self.assertAlmostEqual(transfer['rate_hz'], expected_rate_hz, places=1)
        
        # In the theoretical framework, kpps = packets per second (same as Hz)
        self.assertAlmostEqual(transfer['rate_kpps'], expected_rate_hz, places=1)
        
        # Should be approximately 991.9 packets/s as stated in theory
        self.assertAlmostEqual(transfer['rate_kpps'], 991.9, places=0)
    
    def test_symbiotic_transfer_rate_custom_nodes(self):
        """Test transfer rate with different node counts."""
        transfer_7 = self.coupling.calculate_symbiotic_transfer_rate(num_nodes=7)
        transfer_14 = self.coupling.calculate_symbiotic_transfer_rate(num_nodes=14)
        
        # Doubling nodes should double the rate
        self.assertAlmostEqual(transfer_14['rate_hz'], 2*transfer_7['rate_hz'], places=1)
    
    def test_lagrangian_interaction_term(self):
        """Test Lagrangian interaction term calculation."""
        # Test with unit values
        L_int = self.coupling.lagrangian_interaction_term(psi_density=1.0, H_field=1.0)
        self.assertAlmostEqual(L_int, -0.053, places=3)
        
        # Test with different values
        L_int2 = self.coupling.lagrangian_interaction_term(psi_density=2.0, H_field=3.0)
        self.assertAlmostEqual(L_int2, -0.053 * 2.0 * 3.0, places=3)
        
        # Should be negative (attractive interaction)
        self.assertLess(L_int, 0)
        self.assertLess(L_int2, 0)


class TestHiggsDetectorSignature(unittest.TestCase):
    """Test detector observable signatures."""
    
    def setUp(self):
        """Initialize detector signature calculator."""
        self.detector = HiggsDetectorSignature()
    
    def test_initialization(self):
        """Test detector initializes correctly."""
        self.assertIsNotNone(self.detector.coupling)
    
    def test_cross_section_modulation_at_t0(self):
        """Test cross-section at t=0 (minimum mass, maximum cross-section)."""
        sigma_0 = self.detector.cross_section_modulation(0.0, base_sigma=1.0)
        
        # At t=0, m_eff = 118.375 GeV (minimum)
        # σ ∝ (125/118.375)² ≈ 1.115
        expected_sigma = (125.0 / 118.375) ** 2
        self.assertAlmostEqual(sigma_0, expected_sigma, places=3)
        
        # Should be > 1 (enhanced cross-section)
        self.assertGreater(sigma_0, 1.0)
    
    def test_cross_section_modulation_at_half_period(self):
        """Test cross-section at T₀/2 (maximum mass, minimum cross-section)."""
        T0 = self.detector.coupling.T0
        sigma_half = self.detector.cross_section_modulation(T0/2, base_sigma=1.0)
        
        # At T₀/2, m_eff = 131.625 GeV (maximum)
        # σ ∝ (125/131.625)² ≈ 0.900
        expected_sigma = (125.0 / 131.625) ** 2
        self.assertAlmostEqual(sigma_half, expected_sigma, places=3)
        
        # Should be < 1 (suppressed cross-section)
        self.assertLess(sigma_half, 1.0)
    
    def test_cross_section_oscillates(self):
        """Test that cross-section oscillates periodically."""
        T0 = self.detector.coupling.T0
        times = np.linspace(0, 5*T0, 1000)
        sigmas = self.detector.cross_section_modulation(times, base_sigma=1.0)
        
        # Should have variation
        self.assertGreater(np.std(sigmas), 0)
        
        # Maximum should be at t=0, T0, 2T0, etc. (minimum mass)
        # Minimum should be at T0/2, 3T0/2, etc. (maximum mass)
        max_sigma = np.max(sigmas)
        min_sigma = np.min(sigmas)
        
        self.assertGreater(max_sigma, 1.0)
        self.assertLess(min_sigma, 1.0)
    
    def test_detector_event_rate(self):
        """Test event rate calculation."""
        rate = self.detector.detector_event_rate(0.0, luminosity=1.0, base_sigma=1.0)
        
        # Rate = Luminosity × σ(t)
        # At t=0, σ ≈ 1.115
        self.assertAlmostEqual(rate, (125.0/118.375)**2, places=3)
    
    def test_detector_event_rate_with_luminosity(self):
        """Test event rate scales with luminosity."""
        rate_1 = self.detector.detector_event_rate(0.0, luminosity=1.0)
        rate_10 = self.detector.detector_event_rate(0.0, luminosity=10.0)
        
        # Should scale linearly with luminosity
        self.assertAlmostEqual(rate_10, 10*rate_1, places=3)


class TestPublicAPI(unittest.TestCase):
    """Test public API functions."""
    
    def test_higgs_pc_coupling_activar(self):
        """Test activation function."""
        coupling = higgs_pc_coupling_activar()
        
        self.assertIsInstance(coupling, PC_Higgs_Coupling)
        self.assertAlmostEqual(coupling.f0, 141.7001, places=4)
        self.assertAlmostEqual(coupling.g_eff, 0.053, places=3)
    
    def test_higgs_pc_coupling_activar_custom(self):
        """Test activation with custom parameters."""
        coupling = higgs_pc_coupling_activar(f0=150.0, g_eff=0.06)
        
        self.assertAlmostEqual(coupling.f0, 150.0)
        self.assertAlmostEqual(coupling.g_eff, 0.06)
    
    def test_calcular_masa_modulada(self):
        """Test quick mass calculation function."""
        m_eff = calcular_masa_modulada(0.0)
        
        # At t=0, should be minimum mass
        self.assertAlmostEqual(m_eff, 118.375, places=2)
    
    def test_calcular_masa_modulada_array(self):
        """Test quick mass calculation with array."""
        times = np.array([0.0, 1e-6, 2e-6])
        masses = calcular_masa_modulada(times)
        
        self.assertEqual(len(masses), 3)
        self.assertAlmostEqual(masses[0], 118.375, places=1)
    
    def test_calcular_ventanas_transparencia(self):
        """Test quick transparency windows calculation."""
        windows = calcular_ventanas_transparencia(duration=1.0)
        
        self.assertIn('times', windows)
        self.assertIn('masses', windows)
        self.assertIn('phase_transparency', windows)
        
        # Should have approximately 142 windows in 1 second
        self.assertGreater(windows['num_windows'], 140)
        self.assertLess(windows['num_windows'], 145)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency and constraints."""
    
    def setUp(self):
        """Initialize coupling."""
        self.coupling = PC_Higgs_Coupling()
    
    def test_mass_always_positive(self):
        """Test that effective mass never becomes negative."""
        # Sample many random times
        times = np.random.uniform(0, 100*self.coupling.T0, 10000)
        masses = self.coupling.modulated_mass(times)
        
        # All masses should be positive
        self.assertTrue(np.all(masses > 0))
    
    def test_mass_bounded(self):
        """Test that effective mass stays within bounds."""
        times = np.linspace(0, 100*self.coupling.T0, 10000)
        masses = self.coupling.modulated_mass(times)
        
        # Should never exceed theoretical bounds
        self.assertTrue(np.all(masses >= ConstantesHiggsPC.M_MIN_GEV - 0.1))
        self.assertTrue(np.all(masses <= ConstantesHiggsPC.M_MAX_GEV + 0.1))
    
    def test_periodicity(self):
        """Test that mass modulation is strictly periodic."""
        T0 = self.coupling.T0
        
        # Calculate mass at corresponding times in different periods
        t1 = 0.123  # Arbitrary time in first period
        t2 = t1 + T0  # Same phase in second period
        t3 = t1 + 2*T0  # Same phase in third period
        
        m1 = self.coupling.modulated_mass(t1)
        m2 = self.coupling.modulated_mass(t2)
        m3 = self.coupling.modulated_mass(t3)
        
        # Should be identical
        self.assertAlmostEqual(m1, m2, places=6)
        self.assertAlmostEqual(m2, m3, places=6)
    
    def test_energy_conservation(self):
        """Test that average energy is conserved over cycles."""
        # Energy ∝ mass (in rest frame)
        times = np.linspace(0, 100*self.coupling.T0, 10000)
        masses = self.coupling.modulated_mass(times)
        
        # Average should equal base mass (energy conservation)
        avg_mass = np.mean(masses)
        self.assertAlmostEqual(avg_mass, 125.0, places=0)
    
    def test_modulation_depth_limit(self):
        """Test that modulation depth doesn't exceed coupling constant."""
        times = np.linspace(0, 10*self.coupling.T0, 1000)
        masses = self.coupling.modulated_mass(times)
        
        # Maximum fractional deviation from base mass
        base_mass = 125.0
        max_deviation = np.max(np.abs(masses - base_mass)) / base_mass
        
        # Should be approximately g_eff
        self.assertAlmostEqual(max_deviation, self.coupling.g_eff, places=2)


class TestNumericalStability(unittest.TestCase):
    """Test numerical stability of calculations."""
    
    def setUp(self):
        """Initialize coupling."""
        self.coupling = PC_Higgs_Coupling()
    
    def test_large_time_values(self):
        """Test that calculations remain stable for large time values."""
        # Test at 1 year ≈ 3.15×10⁷ seconds
        t_year = 3.15e7
        m_eff = self.coupling.modulated_mass(t_year)
        
        # Should still be within valid range
        self.assertGreater(m_eff, ConstantesHiggsPC.M_MIN_GEV - 1.0)
        self.assertLess(m_eff, ConstantesHiggsPC.M_MAX_GEV + 1.0)
    
    def test_small_time_values(self):
        """Test calculations for very small time values."""
        # Test at femtosecond scale
        t_fs = 1e-15
        m_eff = self.coupling.modulated_mass(t_fs)
        
        # Should be close to t=0 value
        m_0 = self.coupling.modulated_mass(0.0)
        self.assertAlmostEqual(m_eff, m_0, places=3)
    
    def test_array_size_consistency(self):
        """Test that output array size matches input."""
        for size in [1, 10, 100, 1000, 10000]:
            times = np.linspace(0, 1.0, size)
            masses = self.coupling.modulated_mass(times)
            self.assertEqual(len(masses), size)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConstantesHiggsPC))
    suite.addTests(loader.loadTestsFromTestCase(TestPC_Higgs_Coupling))
    suite.addTests(loader.loadTestsFromTestCase(TestHiggsDetectorSignature))
    suite.addTests(loader.loadTestsFromTestCase(TestPublicAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalStability))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
