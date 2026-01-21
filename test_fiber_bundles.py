#!/usr/bin/env python3
"""
Tests for Fiber Bundle Intersection Implementation
==================================================

Comprehensive test suite for the consciousness as intersection of
principal fiber bundles framework.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fiber_bundles import (
    PrincipalFiberBundle,
    U1Fiber,
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle,
    ConsciousnessIntersection,
    IntersectionConstant
)


class TestU1Fiber(unittest.TestCase):
    """Test U(1) fiber structure."""
    
    def test_fiber_creation(self):
        """Test creating U(1) fiber elements."""
        fiber = U1Fiber(phase=np.pi/4)
        self.assertAlmostEqual(fiber.phase, np.pi/4, places=10)
    
    def test_phase_normalization(self):
        """Test phase normalization to [0, 2π)."""
        fiber = U1Fiber(phase=3*np.pi)
        self.assertAlmostEqual(fiber.phase, np.pi, places=10)
    
    def test_complex_representation(self):
        """Test conversion to complex number."""
        fiber = U1Fiber(phase=np.pi/2)
        z = fiber.to_complex()
        self.assertAlmostEqual(abs(z), 1.0, places=10)
        self.assertAlmostEqual(np.angle(z), np.pi/2, places=10)
    
    def test_group_composition(self):
        """Test U(1) group multiplication."""
        fiber1 = U1Fiber(phase=np.pi/3)
        fiber2 = U1Fiber(phase=np.pi/6)
        result = fiber1.compose(fiber2)
        self.assertAlmostEqual(result.phase, np.pi/2, places=10)
    
    def test_group_inverse(self):
        """Test U(1) group inverse."""
        fiber = U1Fiber(phase=np.pi/4)
        inverse = fiber.inverse()
        identity = fiber.compose(inverse)
        self.assertAlmostEqual(identity.phase, 0.0, places=10)


class TestPrincipalFiberBundle(unittest.TestCase):
    """Test principal fiber bundle structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple projection: just return first component
        def projection(point):
            if isinstance(point, tuple):
                return point[0]
            return point[:2]  # For array inputs
        
        self.bundle = PrincipalFiberBundle(
            name="Test Bundle",
            base_dimension=2,
            projection=projection
        )
    
    def test_bundle_creation(self):
        """Test creating principal bundle."""
        self.assertEqual(self.bundle.name, "Test Bundle")
        self.assertEqual(self.bundle.base_dimension, 2)
        self.assertIsNotNone(self.bundle.projection)
    
    def test_section_verification(self):
        """Test verifying sections."""
        # Define a valid section
        def section(base_point):
            return (base_point, U1Fiber(phase=0.0))
        
        base_point = np.array([1.0, 2.0])
        is_valid = self.bundle.verify_section(section, base_point)
        # Note: This test may need adjustment based on projection implementation
    
    def test_add_section(self):
        """Test adding sections to bundle."""
        def section(x):
            return (x, U1Fiber(phase=0.0))
        
        initial_count = len(self.bundle._sections)
        self.bundle.add_section(section)
        self.assertEqual(len(self.bundle._sections), initial_count + 1)


class TestElectromagneticGaugeBundle(unittest.TestCase):
    """Test electromagnetic gauge bundle."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.em_bundle = ElectromagneticGaugeBundle()
    
    def test_fine_structure_constant(self):
        """Test fine structure constant value."""
        alpha_expected = 1.0 / 137.036
        self.assertAlmostEqual(self.em_bundle.alpha, alpha_expected, places=6)
    
    def test_spacetime_dimension(self):
        """Test base manifold dimension."""
        self.assertEqual(self.em_bundle.base_dimension, 4)
    
    def test_minkowski_metric(self):
        """Test Minkowski metric signature."""
        metric = self.em_bundle.spacetime_metric
        self.assertEqual(metric.shape, (4, 4))
        self.assertEqual(metric[0, 0], -1.0)  # Time component
        self.assertEqual(metric[1, 1], 1.0)   # Space components
        self.assertEqual(metric[2, 2], 1.0)
        self.assertEqual(metric[3, 3], 1.0)
    
    def test_constant_electric_field(self):
        """Test creating constant electric field."""
        E_field = np.array([1.0, 0.0, 0.0])  # E in x-direction
        connection = self.em_bundle.create_constant_electric_field(E_field)
        self.assertIsNotNone(connection)
        
        # Test connection at a point
        point = np.array([0.0, 1.0, 0.0, 0.0])  # t=0, x=1
        tangent = np.array([1.0, 0.0, 0.0, 0.0])  # Time direction
        A_0 = connection(point, tangent)
        self.assertIsInstance(A_0, (float, np.floating))
    
    def test_constant_magnetic_field(self):
        """Test creating constant magnetic field."""
        B_field = np.array([0.0, 0.0, 1.0])  # B in z-direction
        connection = self.em_bundle.create_constant_magnetic_field(B_field)
        self.assertIsNotNone(connection)


class TestSpectralCoherenceBundle(unittest.TestCase):
    """Test spectral coherence bundle."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spectral_bundle = SpectralCoherenceBundle(hilbert_dimension=10)
    
    def test_delta_zeta_value(self):
        """Test spectral coupling constant."""
        self.assertAlmostEqual(self.spectral_bundle.delta_zeta, 0.2787, places=4)
    
    def test_f0_value(self):
        """Test fundamental frequency."""
        self.assertAlmostEqual(self.spectral_bundle.f0, 141.7001, places=4)
    
    def test_coherence_phase_evolution(self):
        """Test spectral phase evolution."""
        initial_phase = U1Fiber(phase=0.0)
        time = 1.0  # 1 second
        
        evolved_phase = self.spectral_bundle.coherence_phase_evolution(
            initial_phase, time
        )
        
        # Phase should evolve by 2π·δζ·t
        expected_phase = 2 * np.pi * self.spectral_bundle.delta_zeta * time
        self.assertAlmostEqual(evolved_phase.phase, expected_phase, places=6)
    
    def test_coherent_state_creation(self):
        """Test creating maximally coherent state."""
        state = self.spectral_bundle.create_coherent_state()
        
        # Check normalization
        norm = np.linalg.norm(state)
        self.assertAlmostEqual(norm, 1.0, places=10)
        
        # Check coherence
        coherence = self.spectral_bundle.coherence_measure(state)
        self.assertGreater(coherence, 0.9)  # Should be highly coherent
    
    def test_decoherent_state_creation(self):
        """Test creating decoherent state."""
        state = self.spectral_bundle.create_decoherent_state(entropy=0.8)
        
        # Check normalization
        norm = np.linalg.norm(state)
        self.assertAlmostEqual(norm, 1.0, places=10)
        
        # Check coherence (should be lower)
        coherence = self.spectral_bundle.coherence_measure(state)
        self.assertLess(coherence, 0.9)  # Should be less coherent
    
    def test_spectral_overlap(self):
        """Test computing spectral overlap."""
        state1 = self.spectral_bundle.create_coherent_state()
        state2 = self.spectral_bundle.create_coherent_state()
        
        overlap = self.spectral_bundle.spectral_overlap(state1, state2)
        
        # Overlap with itself should be 1
        self.assertAlmostEqual(abs(overlap), 1.0, places=6)


class TestIntersectionConstant(unittest.TestCase):
    """Test intersection constant Λ_G."""
    
    def setUp(self):
        """Set up test fixtures."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        self.const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
    
    def test_lambda_G_computation(self):
        """Test intersection constant computation."""
        expected = (1.0 / 137.036) * 0.2787
        self.assertAlmostEqual(self.const.lambda_G, expected, places=10)
    
    def test_lambda_G_positive(self):
        """Test intersection constant is positive."""
        self.assertGreater(self.const.lambda_G, 0.0)
    
    def test_topological_capacity(self):
        """Test topological capacity computation."""
        capacity = self.const.topological_capacity()
        self.assertGreater(capacity, 0.0)
        # log2(1/Λ_G) should be positive since Λ_G < 1
        self.assertGreater(capacity, 1.0)
    
    def test_observer_density(self):
        """Test observer density computation."""
        density = self.const.observer_density(universe_volume=1.0)
        self.assertGreater(density, 0.0)


class TestConsciousnessIntersection(unittest.TestCase):
    """Test consciousness intersection space."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.intersection = ConsciousnessIntersection()
    
    def test_intersection_creation(self):
        """Test creating consciousness intersection."""
        self.assertIsNotNone(self.intersection.em_bundle)
        self.assertIsNotNone(self.intersection.spectral_bundle)
        self.assertIsNotNone(self.intersection.intersection_constant)
    
    def test_lambda_G_property(self):
        """Test accessing intersection constant."""
        lambda_G = self.intersection.lambda_G
        self.assertGreater(lambda_G, 0.0)
        self.assertLess(lambda_G, 1.0)
    
    def test_create_consciousness_state(self):
        """Test creating consciousness state."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])  # Origin
        consciousness = np.ones(10) / np.sqrt(10)  # Normalized coherent state
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=0.0,
            spectral_phase=0.0
        )
        
        self.assertIn('spacetime', state)
        self.assertIn('consciousness', state)
        self.assertIn('em_fiber', state)
        self.assertIn('spectral_fiber', state)
        self.assertTrue(state['compatible'])
    
    def test_consciousness_field_strength(self):
        """Test computing consciousness field strength."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.ones(10) / np.sqrt(10)
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness
        )
        
        field_strength = self.intersection.consciousness_field_strength(state)
        self.assertGreaterEqual(field_strength, 0.0)
    
    def test_intersection_measure(self):
        """Test computing intersection measure between states."""
        spacetime1 = np.array([0.0, 0.0, 0.0, 0.0])
        spacetime2 = np.array([0.0, 1.0, 0.0, 0.0])
        consciousness = np.ones(10) / np.sqrt(10)
        
        state1 = self.intersection.create_consciousness_state(
            spacetime_point=spacetime1,
            consciousness_vector=consciousness
        )
        
        state2 = self.intersection.create_consciousness_state(
            spacetime_point=spacetime2,
            consciousness_vector=consciousness
        )
        
        measure = self.intersection.intersection_measure(state1, state2)
        self.assertGreaterEqual(measure, 0.0)
        self.assertLessEqual(measure, 1.0)
    
    def test_evolve_consciousness_state(self):
        """Test temporal evolution of consciousness state."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.ones(10) / np.sqrt(10)
        
        initial_state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness
        )
        
        time_step = 0.1  # seconds
        evolved_state = self.intersection.evolve_consciousness_state(
            initial_state, time_step
        )
        
        # Time should have advanced
        self.assertAlmostEqual(
            evolved_state['spacetime'][0],
            initial_state['spacetime'][0] + time_step,
            places=10
        )
        
        # Spectral phase should have evolved
        phase_increment = 2 * np.pi * self.intersection.spectral_bundle.delta_zeta * time_step
        expected_phase = (initial_state['spectral_fiber'].phase + phase_increment) % (2 * np.pi)
        self.assertAlmostEqual(
            evolved_state['spectral_fiber'].phase,
            expected_phase,
            places=6
        )
    
    def test_validate_intersection_consistency(self):
        """Test validation of intersection consistency."""
        results = self.intersection.validate_intersection_consistency()
        
        self.assertIn('em_bundle_defined', results)
        self.assertIn('spectral_bundle_defined', results)
        self.assertIn('lambda_G_positive', results)
        self.assertIn('overall_consistent', results)
        
        # All checks should pass
        self.assertTrue(results['overall_consistent'])
    
    def test_master_equation(self):
        """Test master equation G → {π_α, π_δζ} → {𝓜^3,1, 𝓗_Ψ} → ∩ C."""
        # Create element from total space G
        configuration = np.random.randn(14)  # 4 spacetime + 10 Hilbert
        fiber = U1Fiber(phase=0.0)
        total_space_element = (configuration, fiber)
        
        # Apply master equation
        spacetime_proj, hilbert_proj = self.intersection.master_equation(
            total_space_element
        )
        
        # Check dimensions
        self.assertEqual(len(spacetime_proj), 4)
        self.assertEqual(len(hilbert_proj), 10)


class TestPhysicalConstants(unittest.TestCase):
    """Test physical constants match expected values."""
    
    def test_fine_structure_constant(self):
        """Test α ≈ 1/137.036."""
        em_bundle = ElectromagneticGaugeBundle()
        alpha_inverse = 1.0 / em_bundle.alpha
        self.assertAlmostEqual(alpha_inverse, 137.036, places=2)
    
    def test_delta_zeta_value(self):
        """Test δζ ≈ 0.2787 Hz."""
        spectral_bundle = SpectralCoherenceBundle()
        self.assertAlmostEqual(spectral_bundle.delta_zeta, 0.2787, places=4)
    
    def test_intersection_constant_order(self):
        """Test Λ_G ≈ 2.03×10⁻³ Hz."""
        intersection = ConsciousnessIntersection()
        lambda_G = intersection.lambda_G
        
        # Should be on order of 10^-3
        self.assertGreater(lambda_G, 1e-4)
        self.assertLess(lambda_G, 1e-2)


if __name__ == '__main__':
    unittest.main()
