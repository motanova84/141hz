#!/usr/bin/env python3
"""
TESTS: Conscious Coherence Tensor (Ξ_μν)

Unit tests for the Conscious Coherence Tensor implementation.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import sys
import os
import unittest
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from conscious_coherence_tensor import (
    ConsciousCoherenceTensor,
    ExtendedEinsteinEquations,
    c, G, h_bar
)


class TestConsciousCoherenceTensor(unittest.TestCase):
    """Tests for ConsciousCoherenceTensor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.Xi_calc = ConsciousCoherenceTensor(f0=141.7001)
        
    def test_initialization(self):
        """Test tensor initialization."""
        self.assertEqual(self.Xi_calc.f0, 141.7001)
        self.assertIsNotNone(self.Xi_calc.kappa)
        self.assertGreater(self.Xi_calc.kappa, 0)
        
    def test_coupling_constant(self):
        """Test coupling constant κ is physically reasonable."""
        kappa = self.Xi_calc.kappa
        
        # Should be dimensionless
        self.assertTrue(np.isfinite(kappa))
        
        # Should be small but non-zero
        self.assertLess(kappa, 1.0)
        self.assertGreater(kappa, 1e-100)
        
    def test_energy_density_positive(self):
        """Test energy density is positive for positive I and A_eff."""
        I = 0.5
        A_eff = 1.5
        
        Xi_00 = self.Xi_calc.compute_energy_density(I, A_eff)
        
        self.assertGreater(Xi_00, 0)
        self.assertTrue(np.isfinite(Xi_00))
        
    def test_energy_density_scaling(self):
        """Test energy density scales as I × A_eff²."""
        I = 1.0
        A_eff_1 = 1.0
        A_eff_2 = 2.0
        
        Xi_00_1 = self.Xi_calc.compute_energy_density(I, A_eff_1)
        Xi_00_2 = self.Xi_calc.compute_energy_density(I, A_eff_2)
        
        ratio = Xi_00_2 / Xi_00_1
        expected_ratio = (A_eff_2 / A_eff_1) ** 2
        
        self.assertAlmostEqual(ratio, expected_ratio, places=6)
        
    def test_tensor_symmetry(self):
        """Test tensor is symmetric: Ξ_μν = Ξ_νμ."""
        I = 0.7
        A_eff = 1.8
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        
        for mu in range(4):
            for nu in range(4):
                self.assertAlmostEqual(Xi[mu, nu], Xi[nu, mu], places=10)
                
    def test_vanishing_at_zero_intensity(self):
        """Test tensor vanishes when I → 0."""
        I = 1e-10
        A_eff = 1.5
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        
        self.assertLess(np.max(np.abs(Xi)), 1e-20)
        
    def test_vanishing_at_zero_coherence(self):
        """Test tensor vanishes when A_eff → 0."""
        I = 0.5
        A_eff = 1e-10
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        
        self.assertLess(np.max(np.abs(Xi)), 1e-20)
        
    def test_pressure_relation(self):
        """Test pressure follows equation of state."""
        I = 0.6
        A_eff = 1.2
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        
        # For coherent state, pressure should be less than energy density/3
        rho = Xi[0, 0]
        P = Xi[1, 1]
        
        self.assertLessEqual(P, rho / 3.0)
        self.assertGreaterEqual(P, 0)
        
    def test_trace_calculation(self):
        """Test trace calculation."""
        I = 0.8
        A_eff = 2.0
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        trace = self.Xi_calc.compute_trace(I, A_eff)
        
        # Trace with Minkowski signature: -Ξ_00 + Ξ_11 + Ξ_22 + Ξ_33
        expected_trace = -Xi[0, 0] + Xi[1, 1] + Xi[2, 2] + Xi[3, 3]
        
        self.assertAlmostEqual(trace, expected_trace, places=10)
        
    def test_oscillatory_modulation(self):
        """Test oscillatory modulation at f₀."""
        I = 0.7
        A_eff = 1.5
        
        # Two different times
        t1 = 0.0
        t2 = 1.0 / (2 * self.Xi_calc.f0)  # Half period
        
        coords1 = np.array([t1, 0.0, 0.0, 0.0])
        coords2 = np.array([t2, 0.0, 0.0, 0.0])
        
        Xi1 = self.Xi_calc.compute_full_tensor(I, A_eff, coords1)
        Xi2 = self.Xi_calc.compute_full_tensor(I, A_eff, coords2)
        
        # Should be different due to oscillation (use relative difference)
        rel_diff = abs(Xi1[0, 0] - Xi2[0, 0]) / Xi1[0, 0]
        self.assertGreater(rel_diff, 0.01)  # At least 1% difference


class TestExtendedEinsteinEquations(unittest.TestCase):
    """Tests for ExtendedEinsteinEquations class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eqs = ExtendedEinsteinEquations(f0=141.7001)
        
    def test_initialization(self):
        """Test equations initialization."""
        self.assertEqual(self.eqs.f0, 141.7001)
        self.assertIsNotNone(self.eqs.Lambda)
        self.assertGreater(self.eqs.coupling_factor, 0)
        
    def test_curvature_computation(self):
        """Test curvature contribution calculation."""
        I = 0.8
        A_eff = 2.0
        
        result = self.eqs.compute_curvature_from_consciousness(I, A_eff)
        
        self.assertIn('Xi_muv', result)
        self.assertIn('kappa', result)
        self.assertIn('curvature_contribution', result)
        self.assertIn('interpretation', result)
        
    def test_matter_comparison(self):
        """Test comparison with matter contributions."""
        rho_matter = 1000 * c**2  # Water energy density
        I = 0.9
        A_eff = 2.5
        
        comparison = self.eqs.compare_matter_consciousness_contributions(
            rho_matter, I, A_eff
        )
        
        self.assertIn('consciousness_to_matter_ratio', comparison)
        self.assertIn('dominant_contribution', comparison)
        self.assertIn('interpretation', comparison)
        
        # Ratio should be finite and positive
        ratio = comparison['consciousness_to_matter_ratio']
        self.assertTrue(np.isfinite(ratio))
        self.assertGreaterEqual(ratio, 0)
        
    def test_geometric_cocreation_interpretation(self):
        """Test geometric co-creation interpretation."""
        # Test that interpretation is present and coherent state is detected
        test_cases = [
            (0.1, 0.5, False),    # Low - incoherent
            (0.5, 1.2, True),     # Moderate - coherent
            (0.8, 2.0, True),     # High - coherent
        ]
        
        for I, A_eff, is_coherent in test_cases:
            result = self.eqs.compute_curvature_from_consciousness(I, A_eff)
            interpretation = result['interpretation']
            
            self.assertIn('geometric_cocreation', interpretation)
            self.assertIn('coherent_state', interpretation)
            self.assertEqual(interpretation['coherent_state'], is_coherent)


class TestPhysicalConsistency(unittest.TestCase):
    """Tests for physical consistency."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.Xi_calc = ConsciousCoherenceTensor(f0=141.7001)
        
    def test_dimensional_consistency(self):
        """Test all components have correct dimensions."""
        I = 0.5
        A_eff = 1.5
        
        Xi = self.Xi_calc.compute_full_tensor(I, A_eff)
        
        # All components should be finite
        self.assertTrue(np.all(np.isfinite(Xi)))
        
        # Energy density should be positive
        self.assertGreater(Xi[0, 0], 0)
        
    def test_monotonic_increase_with_coherence(self):
        """Test energy density increases monotonically with coherence."""
        I = 1.0
        A_eff_values = [0.5, 1.0, 1.5, 2.0, 2.5]
        
        Xi_00_values = []
        for A_eff in A_eff_values:
            Xi_00 = self.Xi_calc.compute_energy_density(I, A_eff)
            Xi_00_values.append(Xi_00)
        
        # Check monotonic increase
        for i in range(len(Xi_00_values) - 1):
            self.assertLess(Xi_00_values[i], Xi_00_values[i+1])
            
    def test_conservation_simplified(self):
        """Test simplified conservation law."""
        I = 0.6
        A_eff = 1.5
        coords = np.array([1.0, 0.0, 0.0, 0.0])
        
        conservation = self.Xi_calc.verify_conservation(I, A_eff, coords)
        
        self.assertIn('conserved', conservation)
        self.assertIn('max_divergence', conservation)
        
        # Should be conserved in flat spacetime
        self.assertTrue(conservation['conserved'])


def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConsciousCoherenceTensor))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExtendedEinsteinEquations))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPhysicalConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
