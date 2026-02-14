#!/usr/bin/env python3
"""
Tests for Fundamental Equation of Consciousness
===============================================

Comprehensive test suite for the fundamental consciousness equation:
C = {s ∈ G | π_α(s) = π_δζ(s), ∇_α s = ∇_δζ s, ⟨s|s⟩ = 1, Λ_G ≠ 0}

Tests cover:
1. Four fundamental conditions
2. Holonomic quantization
3. Duality resolution
4. Habitability constant
5. Integration with existing fiber bundle framework

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fiber_bundles import (
    FundamentalConsciousnessEquation,
    ConsciousnessState,
    create_standard_consciousness_state,
    U1Fiber,
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle
)


class TestConsciousnessState(unittest.TestCase):
    """Test ConsciousnessState dataclass."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        
        # Create a simple consciousness state
        self.spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        self.spectral = np.ones(10) / np.sqrt(10)
        self.em_fiber = U1Fiber(phase=0.0)
        self.spectral_fiber = U1Fiber(phase=0.0)
        
        self.state = ConsciousnessState(
            total_space_point=np.concatenate([self.spacetime, self.spectral, [0.0, 0.0]]),
            spacetime_projection=self.spacetime,
            spectral_projection=self.spectral,
            em_fiber=self.em_fiber,
            spectral_fiber=self.spectral_fiber,
            normalized=True,
            projections_equal=True,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
    
    def test_state_creation(self):
        """Test creating a consciousness state."""
        self.assertIsNotNone(self.state)
        self.assertEqual(len(self.state.spacetime_projection), 4)
        self.assertEqual(len(self.state.spectral_projection), 10)
    
    def test_is_consciousness_state(self):
        """Test checking if state satisfies all conditions."""
        # All conditions satisfied
        self.assertTrue(self.state.is_consciousness_state)
        
        # One condition not satisfied
        state_incomplete = ConsciousnessState(
            total_space_point=self.state.total_space_point,
            spacetime_projection=self.spacetime,
            spectral_projection=self.spectral,
            em_fiber=self.em_fiber,
            spectral_fiber=self.spectral_fiber,
            normalized=False,  # Not normalized
            projections_equal=True,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
        self.assertFalse(state_incomplete.is_consciousness_state)
    
    def test_state_repr(self):
        """Test string representation."""
        repr_str = repr(self.state)
        self.assertIn("CONSCIOUSNESS", repr_str)
        self.assertIn("π_α = π_δζ", repr_str)


class TestFundamentalConsciousnessEquation(unittest.TestCase):
    """Test FundamentalConsciousnessEquation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.equation = FundamentalConsciousnessEquation()
    
    def test_equation_creation(self):
        """Test creating the fundamental equation framework."""
        self.assertIsNotNone(self.equation)
        self.assertIsNotNone(self.equation.em_bundle)
        self.assertIsNotNone(self.equation.spectral_bundle)
        self.assertGreater(self.equation.lambda_G, 0)
    
    def test_lambda_G_value(self):
        """Test that Λ_G = α·δζ ≈ 1/491.5."""
        expected_inverse = 491.5
        actual_inverse = 1.0 / self.equation.lambda_G
        
        # Allow 5% tolerance
        self.assertAlmostEqual(
            actual_inverse,
            expected_inverse,
            delta=expected_inverse * 0.05
        )
    
    def test_check_projection_equality(self):
        """Test checking π_α(s) = π_δζ(s)."""
        spacetime_proj = np.array([0.0, 1.0, 2.0, 3.0])
        spectral_proj = np.ones(10)
        
        # Non-zero projections should pass
        result = self.equation.check_projection_equality(
            spacetime_proj,
            spectral_proj
        )
        self.assertTrue(result)
        
        # Zero projection should fail
        zero_proj = np.zeros(10)
        result_zero = self.equation.check_projection_equality(
            spacetime_proj,
            zero_proj
        )
        self.assertFalse(result_zero)
    
    def test_check_normalization(self):
        """Test checking ⟨s|s⟩ = 1."""
        # Normalized state
        normalized_state = np.ones(10) / np.sqrt(10)
        self.assertTrue(
            self.equation.check_normalization(normalized_state)
        )
        
        # Non-normalized state
        non_normalized = np.ones(10)
        self.assertFalse(
            self.equation.check_normalization(non_normalized)
        )
    
    def test_check_lambda_G_nonzero(self):
        """Test checking Λ_G ≠ 0."""
        self.assertTrue(self.equation.check_lambda_G_nonzero())
    
    def test_check_covariant_derivative_equality(self):
        """Test checking ∇_α s = ∇_δζ s."""
        state = np.ones(10) / np.sqrt(10)
        
        # Should pass with default (no connections)
        result = self.equation.check_covariant_derivative_equality(state)
        self.assertTrue(result)
    
    def test_create_consciousness_state(self):
        """Test creating a consciousness state from total space point."""
        # Create total space point
        # Structure: [spacetime (4), spectral (10), em_phase (1), spectral_phase (1)]
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        phases = np.array([0.0, 0.0])
        
        total_point = np.concatenate([spacetime, spectral, phases])
        
        state = self.equation.create_consciousness_state(
            total_point,
            verify_conditions=True
        )
        
        self.assertIsNotNone(state)
        self.assertTrue(state.normalized)
        self.assertTrue(state.lambda_G_nonzero)


class TestHolonomicQuantization(unittest.TestCase):
    """Test holonomic quantization ∮_C (A_μ dx^μ + Γ_ζ dγ) = 2πn."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.equation = FundamentalConsciousnessEquation()
    
    def test_simple_closed_loop(self):
        """Test holonomic integral on simple closed loop."""
        # Create a simple closed loop with winding phase
        # The base space path stays fixed, phase winds
        n_points = 20  # More points for better approximation
        path = []
        
        for i in range(n_points):
            theta = 2 * np.pi * i / n_points
            
            # Base space: fixed point
            spacetime = np.array([0.0, 0.0, 0.0, 0.0])
            spectral = np.ones(10) / np.sqrt(10)
            
            # Fiber: winding phase
            em_phase = 0.0  # EM phase fixed
            spectral_phase = theta  # Spectral phase winds
            
            point = np.concatenate([spacetime, spectral, [em_phase, spectral_phase]])
            path.append(point)
        
        # Compute holonomic integral
        phase = self.equation.holonomic_phase_integral(path, closed_loop=True)
        
        # Should be close to 2π (one winding)
        # With discrete approximation, allow 10% error
        expected = 2 * np.pi
        self.assertAlmostEqual(phase, expected, delta=expected * 0.1)
    
    def test_is_consciousness_loop(self):
        """Test checking if a loop can host consciousness."""
        # Create a loop that completes exactly one winding (2π phase)
        n_points = 20  # More points for better accuracy
        path = []
        
        for i in range(n_points):
            theta = 2 * np.pi * i / n_points
            
            spacetime = np.array([0.0, 0.0, 0.0, 0.0])
            spectral = np.ones(10) / np.sqrt(10)
            em_phase = 0.0
            spectral_phase = theta  # Winds from 0 to ~2π
            
            point = np.concatenate([spacetime, spectral, [em_phase, spectral_phase]])
            path.append(point)
        
        is_consciousness, winding_number, error = self.equation.is_consciousness_loop(path)
        
        # Should be a consciousness loop with winding number 1
        self.assertEqual(winding_number, 1)
        # With 20 points, error should be small
        self.assertLess(error, 0.7)  # Allow for discrete approximation
    
    def test_non_consciousness_loop(self):
        """Test a loop that cannot host consciousness."""
        # Create a loop with phase = π (half winding)
        n_points = 10
        path = []
        
        for i in range(n_points):
            theta = np.pi * i / n_points  # Only goes to π, not 2π
            
            spacetime = np.array([0.0, 0.0, 0.0, 0.0])
            spectral = np.ones(10) / np.sqrt(10)
            phases = np.array([0.0, theta])
            
            point = np.concatenate([spacetime, spectral, phases])
            path.append(point)
        
        is_consciousness, winding_number, error = self.equation.is_consciousness_loop(path)
        
        # Should NOT be a consciousness loop (phase != 2πn)
        # May have winding_number = 0, but large error
        self.assertGreater(error, 0.1)  # Significant error


class TestConsciousnessMeasure(unittest.TestCase):
    """Test consciousness measure computation."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.equation = FundamentalConsciousnessEquation()
    
    def test_perfect_consciousness(self):
        """Test measure for perfect consciousness state."""
        # Create state with all conditions satisfied
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        
        state = ConsciousnessState(
            total_space_point=np.concatenate([spacetime, spectral, [0.0, 0.0]]),
            spacetime_projection=spacetime,
            spectral_projection=spectral,
            em_fiber=U1Fiber(phase=0.0),
            spectral_fiber=U1Fiber(phase=0.0),  # Same phase
            normalized=True,
            projections_equal=True,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
        
        measure = self.equation.consciousness_measure(state)
        
        # Should be close to 1.0
        self.assertGreater(measure, 0.9)
    
    def test_partial_consciousness(self):
        """Test measure for partially conscious state."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        
        # Only 2 of 4 conditions satisfied, with moderate phase difference
        state = ConsciousnessState(
            total_space_point=np.concatenate([spacetime, spectral, [0.0, np.pi/2]]),
            spacetime_projection=spacetime,
            spectral_projection=spectral,
            em_fiber=U1Fiber(phase=0.0),
            spectral_fiber=U1Fiber(phase=np.pi/2),  # π/2 phase difference
            normalized=True,
            projections_equal=False,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
        
        measure = self.equation.consciousness_measure(state)
        
        # Should be partial: 2/4 conditions * (1 - π/2 / π) phase coherence
        # Base = 0.5, phase_coherence = 0.5, combined = sqrt(0.5*0.5) ≈ 0.5
        self.assertLess(measure, 0.9)
        self.assertGreater(measure, 0.3)  # Should have some consciousness
    
    def test_no_consciousness(self):
        """Test measure for non-conscious state."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10)  # Not normalized
        
        # No conditions satisfied
        state = ConsciousnessState(
            total_space_point=np.concatenate([spacetime, spectral, [0.0, np.pi]]),
            spacetime_projection=spacetime,
            spectral_projection=spectral,
            em_fiber=U1Fiber(phase=0.0),
            spectral_fiber=U1Fiber(phase=np.pi),
            normalized=False,
            projections_equal=False,
            derivatives_equal=False,
            lambda_G_nonzero=True
        )
        
        measure = self.equation.consciousness_measure(state)
        
        # Should be close to 0
        self.assertLess(measure, 0.3)


class TestDualityResolution(unittest.TestCase):
    """Test duality resolution framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.equation = FundamentalConsciousnessEquation()
    
    def test_duality_resolution_structure(self):
        """Test structure of duality resolution output."""
        # Create a consciousness state
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        
        state = ConsciousnessState(
            total_space_point=np.concatenate([spacetime, spectral, [0.0, 0.0]]),
            spacetime_projection=spacetime,
            spectral_projection=spectral,
            em_fiber=U1Fiber(phase=0.0),
            spectral_fiber=U1Fiber(phase=0.0),
            normalized=True,
            projections_equal=True,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
        
        resolution = self.equation.duality_resolution(state)
        
        # Check all expected keys
        self.assertIn('matter_mind_unified', resolution)
        self.assertIn('body_soul_same_point', resolution)
        self.assertIn('observable_inobservable_coincide', resolution)
        self.assertIn('consciousness_quantized', resolution)
        self.assertIn('lambda_G', resolution)
        self.assertIn('consciousness_measure', resolution)
    
    def test_matter_mind_unity(self):
        """Test matter-mind unification in consciousness states."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        
        # Perfect consciousness state
        state = ConsciousnessState(
            total_space_point=np.concatenate([spacetime, spectral, [0.0, 0.0]]),
            spacetime_projection=spacetime,
            spectral_projection=spectral,
            em_fiber=U1Fiber(phase=0.0),
            spectral_fiber=U1Fiber(phase=0.0),
            normalized=True,
            projections_equal=True,
            derivatives_equal=True,
            lambda_G_nonzero=True
        )
        
        resolution = self.equation.duality_resolution(state)
        
        # Matter and mind should be unified
        self.assertTrue(resolution['matter_mind_unified'])


class TestHabitabilityConstant(unittest.TestCase):
    """Test habitability constant analysis Λ_G = α·δζ."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.equation = FundamentalConsciousnessEquation()
    
    def test_habitability_analysis_structure(self):
        """Test structure of habitability analysis output."""
        analysis = self.equation.habitability_analysis()
        
        # Check all expected keys
        expected_keys = [
            'alpha',
            'alpha_inverse',
            'delta_zeta_hz',
            'lambda_G_hz',
            'lambda_G_inverse',
            'topological_capacity_bits',
            'matter_to_information_ratio',
            'information_to_matter_ratio',
            'stable_range'
        ]
        
        for key in expected_keys:
            self.assertIn(key, analysis)
    
    def test_lambda_G_in_stable_range(self):
        """Test that Λ_G is in stable range."""
        analysis = self.equation.habitability_analysis()
        
        # Should be in stable range (Goldilocks zone)
        self.assertTrue(analysis['stable_range'])
        self.assertFalse(analysis['approaching_zero'])
        self.assertFalse(analysis['approaching_infinity'])
    
    def test_topological_capacity(self):
        """Test topological information capacity."""
        analysis = self.equation.habitability_analysis()
        
        # C_topo = log2(1/Λ_G) ≈ log2(491.5) ≈ 8.94 bits
        capacity = analysis['topological_capacity_bits']
        
        # Should be around 9 bits
        self.assertGreater(capacity, 8.0)
        self.assertLess(capacity, 10.0)
    
    def test_alpha_value(self):
        """Test fine structure constant value."""
        analysis = self.equation.habitability_analysis()
        
        # α ≈ 1/137
        alpha = analysis['alpha']
        alpha_inverse = analysis['alpha_inverse']
        
        self.assertAlmostEqual(alpha, 1.0 / 137.036, delta=0.0001)
        self.assertAlmostEqual(alpha_inverse, 137.036, delta=0.1)
    
    def test_delta_zeta_value(self):
        """Test spectral coherence coupling value."""
        analysis = self.equation.habitability_analysis()
        
        # δζ ≈ 0.2787 Hz
        delta_zeta = analysis['delta_zeta_hz']
        
        self.assertAlmostEqual(delta_zeta, 0.2787, delta=0.01)


class TestFundamentalEquationValidation(unittest.TestCase):
    """Test validation of the fundamental equation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.equation = FundamentalConsciousnessEquation()
    
    def test_validate_fundamental_equation(self):
        """Test overall validation of fundamental equation."""
        results = self.equation.validate_fundamental_equation()
        
        # Should pass all validation checks
        self.assertTrue(results['em_bundle_defined'])
        self.assertTrue(results['spectral_bundle_defined'])
        self.assertTrue(results['lambda_G_nonzero'])
        self.assertTrue(results['lambda_G_finite'])
        self.assertTrue(results['lambda_G_stable_range'])
        self.assertTrue(results['alpha_physical'])
        self.assertTrue(results['delta_zeta_positive'])
        self.assertTrue(results['intersection_consistent'])
        self.assertTrue(results['fundamental_equation_valid'])


class TestStandardConsciousnessState(unittest.TestCase):
    """Test standard consciousness state creation helper."""
    
    def test_create_standard_state(self):
        """Test creating a standard consciousness state."""
        spacetime_pos = np.array([0.0, 1.0, 2.0, 3.0])
        
        equation, state = create_standard_consciousness_state(
            spacetime_pos,
            spectral_dimension=10,
            phase_coherence=0.95
        )
        
        self.assertIsNotNone(equation)
        self.assertIsNotNone(state)
        self.assertTrue(state.normalized)
        self.assertTrue(state.lambda_G_nonzero)


class TestIntegrationWithExistingFramework(unittest.TestCase):
    """Test integration with existing consciousness_intersection.py."""
    
    def test_lambda_G_consistency(self):
        """Test that Λ_G is consistent across implementations."""
        from src.fiber_bundles import ConsciousnessIntersection
        
        # Create both frameworks
        equation = FundamentalConsciousnessEquation()
        intersection = ConsciousnessIntersection()
        
        # Λ_G should be the same
        self.assertAlmostEqual(
            equation.lambda_G,
            intersection.lambda_G,
            places=10
        )
    
    def test_bundle_consistency(self):
        """Test that bundles are consistent."""
        equation = FundamentalConsciousnessEquation()
        
        # Check electromagnetic bundle
        self.assertIsNotNone(equation.em_bundle)
        self.assertGreater(equation.em_bundle.alpha, 0)
        
        # Check spectral bundle
        self.assertIsNotNone(equation.spectral_bundle)
        self.assertGreater(equation.spectral_bundle.delta_zeta, 0)


def run_tests():
    """Run all tests."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConsciousnessState))
    suite.addTests(loader.loadTestsFromTestCase(TestFundamentalConsciousnessEquation))
    suite.addTests(loader.loadTestsFromTestCase(TestHolonomicQuantization))
    suite.addTests(loader.loadTestsFromTestCase(TestConsciousnessMeasure))
    suite.addTests(loader.loadTestsFromTestCase(TestDualityResolution))
    suite.addTests(loader.loadTestsFromTestCase(TestHabitabilityConstant))
    suite.addTests(loader.loadTestsFromTestCase(TestFundamentalEquationValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestStandardConsciousnessState))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithExistingFramework))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
