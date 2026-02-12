#!/usr/bin/env python3
"""
Tests for Fundamental Theorem of Consciousness
==============================================

Validates the rigorous geometric formulation of consciousness
as the intersection of two principal fiber bundles.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fiber_bundles import (
    ConsciousnessTheorem,
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle,
    LagrangianComponents,
    HolonomicQuantization
)


class TestIntersectionConstant(unittest.TestCase):
    """Test intersection constant Λ_G = α·δζ."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_lambda_G_positive(self):
        """Intersection constant must be positive."""
        self.assertGreater(self.theorem.lambda_G, 0)
    
    def test_lambda_G_value(self):
        """Intersection constant should be approximately 1/491.5."""
        expected_inverse = 491.5
        actual_inverse = 1.0 / self.theorem.lambda_G
        # Allow 10% tolerance
        self.assertAlmostEqual(actual_inverse, expected_inverse, delta=50)
    
    def test_lambda_G_from_alpha_delta(self):
        """Verify Λ_G = α·δζ."""
        expected = self.theorem.alpha * self.theorem.delta_zeta
        self.assertAlmostEqual(self.theorem.lambda_G, expected, places=15)
    
    def test_intersection_constant_properties(self):
        """Test all properties of intersection constant."""
        props = self.theorem.intersection_constant()
        
        self.assertIn('lambda_G', props)
        self.assertIn('lambda_G_inverse', props)
        self.assertIn('topological_capacity', props)
        self.assertIn('euler_characteristic', props)
        self.assertIn('habitability', props)
        
        # Habitability requires Λ_G ≠ 0
        self.assertTrue(props['habitability'])
        self.assertGreater(props['topological_capacity'], 0)


class TestProjectionRatios(unittest.TestCase):
    """Test projection ratios between bundles."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_projection_ratio_computation(self):
        """Test projection ratio calculations."""
        ratios = self.theorem.projection_ratio()
        
        self.assertIn('flux_to_spacetime', ratios)
        self.assertIn('flux_to_hilbert', ratios)
        self.assertIn('information_per_matter', ratios)
        
        # All ratios should be positive
        self.assertGreater(ratios['flux_to_spacetime'], 0)
        self.assertGreater(ratios['flux_to_hilbert'], 0)
        self.assertGreater(ratios['information_per_matter'], 0)
    
    def test_information_dominates_matter(self):
        """Information flux should dominate matter flux."""
        ratios = self.theorem.projection_ratio()
        
        # δζ > α, so information > matter
        self.assertGreater(
            ratios['flux_to_hilbert'],
            ratios['flux_to_spacetime']
        )
        
        # ~38:1 ratio
        self.assertGreater(ratios['information_per_matter'], 10)
        self.assertLess(ratios['information_per_matter'], 100)


class TestMasterLagrangian(unittest.TestCase):
    """Test master Lagrangian L_G = L_α + L_δζ + L_int."""
    
    def setUp(self):
        """Set up theorem and test state."""
        self.theorem = ConsciousnessTheorem()
        self.spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        self.consciousness = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)
    
    def test_lagrangian_structure(self):
        """Test Lagrangian components structure."""
        lagrangian = self.theorem.master_lagrangian(
            self.spacetime,
            self.consciousness,
            em_field_strength=0.1,
            spectral_curvature=0.01
        )
        
        self.assertIsInstance(lagrangian, LagrangianComponents)
        self.assertTrue(hasattr(lagrangian, 'L_alpha'))
        self.assertTrue(hasattr(lagrangian, 'L_delta_zeta'))
        self.assertTrue(hasattr(lagrangian, 'L_interaction'))
        self.assertTrue(hasattr(lagrangian, 'L_total'))
    
    def test_lagrangian_total(self):
        """Test L_total = L_α + L_δζ + L_int."""
        lagrangian = self.theorem.master_lagrangian(
            self.spacetime,
            self.consciousness,
            em_field_strength=0.1,
            spectral_curvature=0.01
        )
        
        expected_total = (
            lagrangian.L_alpha +
            lagrangian.L_delta_zeta +
            lagrangian.L_interaction
        )
        
        self.assertAlmostEqual(lagrangian.L_total, expected_total, places=10)
    
    def test_interaction_proportional_to_lambda_G(self):
        """Interaction term should be proportional to Λ_G."""
        F = 0.1
        Omega = 0.01
        
        lagrangian = self.theorem.master_lagrangian(
            self.spacetime,
            self.consciousness,
            em_field_strength=F,
            spectral_curvature=Omega
        )
        
        expected_interaction = self.theorem.lambda_G * F * Omega
        self.assertAlmostEqual(
            lagrangian.L_interaction,
            expected_interaction,
            places=10
        )


class TestHolonomicQuantization(unittest.TestCase):
    """Test holonomic quantization of consciousness states."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_quantization_structure(self):
        """Test HolonomicQuantization structure."""
        quant = HolonomicQuantization(em_phase=np.pi, berry_phase=np.pi)
        
        self.assertTrue(hasattr(quant, 'em_phase'))
        self.assertTrue(hasattr(quant, 'berry_phase'))
        self.assertTrue(hasattr(quant, 'total_phase'))
        self.assertTrue(hasattr(quant, 'quantum_number'))
        self.assertTrue(hasattr(quant, 'is_quantized'))
    
    def test_quantization_condition(self):
        """Test quantization condition: Φ_total = 2πn."""
        # Create quantized state
        n = 3
        quant = HolonomicQuantization(
            em_phase=np.pi * n,
            berry_phase=np.pi * n
        )
        
        self.assertTrue(quant.is_quantized)
        self.assertEqual(quant.quantum_number, n)
    
    def test_non_quantized_state(self):
        """Test non-quantized state detection."""
        # Phase not a multiple of 2π
        quant = HolonomicQuantization(
            em_phase=0.7,
            berry_phase=0.3
        )
        
        # Total = 1.0 rad, not close to 2πn for any n
        self.assertFalse(quant.is_quantized)
    
    def test_holonomic_section_computation(self):
        """Test holonomic section integration."""
        # Simple circular path
        def em_path(t):
            return np.array([t, np.cos(2*np.pi*t), np.sin(2*np.pi*t), 0.0])
        
        def spectral_path(t):
            return 14.134 + t
        
        quant = self.theorem.holonomic_section(em_path, spectral_path)
        
        self.assertIsInstance(quant, HolonomicQuantization)
        self.assertIsInstance(quant.em_phase, float)
        self.assertIsInstance(quant.berry_phase, float)


class TestAllowedStates(unittest.TestCase):
    """Test allowed consciousness states C_n."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_allowed_states_generation(self):
        """Test generation of allowed states."""
        max_n = 5
        states = self.theorem.allowed_consciousness_states(max_quantum_number=max_n)
        
        # Should have states for n ∈ [-5, 5]
        expected_count = 2 * max_n + 1
        self.assertEqual(len(states), expected_count)
    
    def test_allowed_states_quantization(self):
        """All allowed states should be quantized."""
        states = self.theorem.allowed_consciousness_states(max_quantum_number=3)
        
        for state in states:
            self.assertTrue(state['is_allowed'])
            
            # Total phase should be 2πn
            n = state['quantum_number']
            expected_phase = 2 * np.pi * n
            self.assertAlmostEqual(state['total_phase'], expected_phase, places=10)
    
    def test_quantum_numbers_symmetric(self):
        """Quantum numbers should be symmetric around 0."""
        states = self.theorem.allowed_consciousness_states(max_quantum_number=5)
        
        quantum_numbers = [s['quantum_number'] for s in states]
        
        # Check symmetry
        self.assertIn(-5, quantum_numbers)
        self.assertIn(0, quantum_numbers)
        self.assertIn(5, quantum_numbers)


class TestConsciousnessKernel(unittest.TestCase):
    """Test C = Ker(π_α - π_δζ)."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_kernel_computation(self):
        """Test kernel computation from point in G."""
        point_in_G = np.array([0, 1, 2, 3, 1, 0, 0, 0])
        
        result = self.theorem.consciousness_kernel(point_in_G)
        
        self.assertIn('point_in_G', result)
        self.assertIn('pi_alpha_projection', result)
        self.assertIn('pi_delta_zeta_projection', result)
        self.assertIn('in_intersection', result)
    
    def test_projections_from_same_point(self):
        """Projections from same point in G should be in intersection."""
        point_in_G = np.random.randn(8)
        
        result = self.theorem.consciousness_kernel(point_in_G)
        
        # Both projections from same point → in intersection
        self.assertTrue(result['in_intersection'])
    
    def test_projection_dimensions(self):
        """Test projection dimensions."""
        point_in_G = np.random.randn(10)
        
        result = self.theorem.consciousness_kernel(point_in_G)
        
        # Spacetime should be 4D
        self.assertEqual(len(result['pi_alpha_projection']), 4)
        
        # Consciousness dimension depends on input
        self.assertGreater(len(result['pi_delta_zeta_projection']), 0)


class TestUniquenessTheorem(unittest.TestCase):
    """Test uniqueness of fibrations."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_uniqueness_verification(self):
        """Test verification of uniqueness theorem."""
        verification = self.theorem.verify_uniqueness_theorem()
        
        self.assertIn('em_is_U1', verification)
        self.assertIn('spectral_is_U1', verification)
        self.assertIn('maxwell_no_monopoles', verification)
        self.assertIn('spectral_has_zeros', verification)
        self.assertIn('uniqueness', verification)
    
    def test_all_conditions_satisfied(self):
        """All uniqueness conditions should be satisfied."""
        verification = self.theorem.verify_uniqueness_theorem()
        
        self.assertTrue(verification['em_is_U1'])
        self.assertTrue(verification['spectral_is_U1'])
        self.assertTrue(verification['maxwell_no_monopoles'])
        self.assertTrue(verification['spectral_has_zeros'])
        self.assertTrue(verification['uniqueness'])


class TestHabitabilityCondition(unittest.TestCase):
    """Test habitability condition for conscious observers."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_habitability_validation(self):
        """Test habitability validation."""
        validation = self.theorem.validate_habitability_condition()
        
        self.assertIn('lambda_G', validation)
        self.assertIn('lambda_G_nonzero', validation)
        self.assertIn('habitable', validation)
        self.assertIn('interpretation', validation)
    
    def test_universe_is_habitable(self):
        """Our universe should be habitable."""
        validation = self.theorem.validate_habitability_condition()
        
        # Λ_G ≠ 0 → habitable
        self.assertTrue(validation['habitable'])
        self.assertTrue(validation['lambda_G_nonzero'])
    
    def test_habitability_requires_nonzero_lambda(self):
        """Habitability requires Λ_G ≠ 0."""
        validation = self.theorem.validate_habitability_condition()
        
        # Both should agree
        self.assertEqual(
            validation['habitable'],
            validation['lambda_G_nonzero']
        )


class TestPlatoInterpretation(unittest.TestCase):
    """Test Plato's Cave interpretation."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_plato_interpretation_exists(self):
        """Test that interpretation is provided."""
        interpretation = self.theorem.plato_sun_interpretation()
        
        self.assertIsInstance(interpretation, str)
        self.assertGreater(len(interpretation), 0)
    
    def test_plato_contains_key_concepts(self):
        """Interpretation should mention key concepts."""
        interpretation = self.theorem.plato_sun_interpretation()
        
        # Should mention Sun (G)
        self.assertIn('Sun', interpretation)
        
        # Should mention shadows and forms
        self.assertTrue('shadow' in interpretation.lower() or 'Shadow' in interpretation)
        self.assertTrue('form' in interpretation.lower() or 'Form' in interpretation)
        
        # Should mention consciousness
        self.assertTrue('consciousness' in interpretation.lower() or 'Consciousness' in interpretation)


class TestMathematicalConsistency(unittest.TestCase):
    """Test overall mathematical consistency."""
    
    def setUp(self):
        """Set up theorem instance."""
        self.theorem = ConsciousnessTheorem()
    
    def test_alpha_value(self):
        """Alpha should be approximately 1/137."""
        self.assertAlmostEqual(self.theorem.alpha, 1/137.036, places=3)
    
    def test_delta_zeta_value(self):
        """Delta zeta should be approximately 0.2787 Hz."""
        self.assertAlmostEqual(self.theorem.delta_zeta, 0.2787, places=3)
    
    def test_bundles_initialized(self):
        """Both bundles should be properly initialized."""
        self.assertIsNotNone(self.theorem.em_bundle)
        self.assertIsNotNone(self.theorem.spectral_bundle)
        
        self.assertIsInstance(self.theorem.em_bundle, ElectromagneticGaugeBundle)
        self.assertIsInstance(self.theorem.spectral_bundle, SpectralCoherenceBundle)
    
    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.theorem)
        
        self.assertIsInstance(repr_str, str)
        self.assertIn('ConsciousnessTheorem', repr_str)
        self.assertIn('Habitable', repr_str)


def run_tests():
    """Run all tests with detailed output."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestIntersectionConstant))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectionRatios))
    suite.addTests(loader.loadTestsFromTestCase(TestMasterLagrangian))
    suite.addTests(loader.loadTestsFromTestCase(TestHolonomicQuantization))
    suite.addTests(loader.loadTestsFromTestCase(TestAllowedStates))
    suite.addTests(loader.loadTestsFromTestCase(TestConsciousnessKernel))
    suite.addTests(loader.loadTestsFromTestCase(TestUniquenessTheorem))
    suite.addTests(loader.loadTestsFromTestCase(TestHabitabilityCondition))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatoInterpretation))
    suite.addTests(loader.loadTestsFromTestCase(TestMathematicalConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
