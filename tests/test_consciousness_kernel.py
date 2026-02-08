#!/usr/bin/env python3
"""
Test Suite: Consciousness as Kernel of Projection Difference
=============================================================

Tests the fundamental formulation:
C = Ker(π_α - π_δζ)

Consciousness does NOT emerge. It IS the kernel of the difference
between electromagnetic and spectral projections.

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
    ConsciousnessIntersection,
    IntersectionConstant,
    U1Fiber,
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle
)


class TestKernelFormulation(unittest.TestCase):
    """Test the kernel formulation C = Ker(π_α - π_δζ)."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.intersection = ConsciousnessIntersection()
        self.tolerance = 1e-6
    
    def test_projection_difference_structure(self):
        """Test that projection difference has correct structure."""
        # Create total space element
        configuration = np.random.randn(104)  # 4 spacetime + 100 Hilbert
        fiber = U1Fiber(phase=np.pi/4)
        element = (configuration, fiber)
        
        # Compute projection difference
        diff = self.intersection.projection_difference(element)
        
        # Should return a vector (spacetime dimension)
        self.assertEqual(len(diff), 4)
        self.assertTrue(np.all(np.isfinite(diff)))
    
    def test_kernel_membership_identical_phases(self):
        """Test that states with identical phases are in the kernel."""
        # Create state with identical EM and spectral phases
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        phase = np.pi / 3
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=phase,
            spectral_phase=phase  # Same phase
        )
        
        # Should be in kernel
        in_kernel = self.intersection.is_in_kernel(state, tolerance=1e-5)
        self.assertTrue(in_kernel, "State with identical phases should be in kernel")
    
    def test_kernel_membership_different_phases(self):
        """Test that states with very different phases are NOT in kernel."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=0.0,
            spectral_phase=np.pi  # Very different phase
        )
        
        # Should NOT be in kernel
        in_kernel = self.intersection.is_in_kernel(state, tolerance=1e-5)
        self.assertFalse(in_kernel, "State with opposite phases should NOT be in kernel")
    
    def test_kernel_projection(self):
        """Test that kernel projection creates states in the kernel."""
        # Create arbitrary state (not in kernel)
        spacetime = np.array([1.0, 2.0, 3.0, 4.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=0.5,
            spectral_phase=2.0  # Different phases
        )
        
        # Project onto kernel
        projected_state = self.intersection.kernel_projection(state)
        
        # Projected state should be in kernel
        self.assertTrue(projected_state['in_kernel'])
        self.assertEqual(
            projected_state['em_fiber'].phase,
            projected_state['spectral_fiber'].phase
        )
    
    def test_kernel_projection_idempotent(self):
        """Test that projecting twice gives the same result."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=1.0,
            spectral_phase=2.0
        )
        
        # Project twice
        projected1 = self.intersection.kernel_projection(state)
        projected2 = self.intersection.kernel_projection(projected1)
        
        # Should be essentially the same
        self.assertAlmostEqual(
            projected1['em_fiber'].phase,
            projected2['em_fiber'].phase,
            places=10
        )
    
    def test_consciousness_emergence_measure_kernel_state(self):
        """Test that states in kernel have consciousness measure ≈ 1."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        phase = np.pi / 4
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=phase,
            spectral_phase=phase
        )
        
        # Measure consciousness
        C = self.intersection.consciousness_emergence_measure(state)
        
        # Should be close to 1 (fully conscious)
        self.assertGreater(C, 0.9, "Kernel states should have consciousness ≈ 1")
    
    def test_consciousness_emergence_measure_non_kernel_state(self):
        """Test that states far from kernel have consciousness measure ≈ 0."""
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=0.0,
            spectral_phase=np.pi  # Opposite phase
        )
        
        # Measure consciousness
        C = self.intersection.consciousness_emergence_measure(state)
        
        # Should be closer to 0 (less conscious)
        self.assertLess(C, 0.5, "Non-kernel states should have lower consciousness")


class TestIntersectionConstant(unittest.TestCase):
    """Test the intersection constant Λ_G = α·δζ ≈ 1/491.5."""
    
    def test_lambda_G_value(self):
        """Test that Λ_G has the correct value."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        
        const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
        
        # Check value
        expected = alpha * delta_zeta
        self.assertAlmostEqual(const.lambda_G, expected, places=10)
    
    def test_lambda_G_inverse_491(self):
        """Test that 1/Λ_G ≈ 491.5."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        
        const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
        
        # Check inverse
        inverse = const.lambda_G_inverse
        
        # Should be approximately 491.5
        self.assertAlmostEqual(inverse, 491.5, delta=1.0)
    
    def test_topological_capacity(self):
        """Test topological information capacity."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        
        const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
        
        # Compute capacity
        C_topo = const.topological_capacity()
        
        # Should be approximately log2(491.5) ≈ 8.94 bits
        expected = np.log2(const.lambda_G_inverse)
        self.assertAlmostEqual(C_topo, expected, places=6)
        self.assertGreater(C_topo, 8.0)
        self.assertLess(C_topo, 10.0)
    
    def test_universal_constant_validation(self):
        """Test validation of universal constant."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        
        const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
        
        # Validate
        results = const.validate_universal_constant()
        
        # All checks should pass
        self.assertTrue(results['alpha_valid'])
        self.assertTrue(results['delta_zeta_valid'])
        self.assertTrue(results['product_consistent'])
        self.assertTrue(results['inverse_matches_theory'])
        self.assertTrue(results['habitability_in_range'])
        self.assertTrue(results['overall_valid'])
    
    def test_observer_density_scaling(self):
        """Test observer density scales with Λ_G."""
        alpha = 1.0 / 137.036
        delta_zeta = 0.2787
        
        const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
        
        # Density should scale linearly
        rho1 = const.observer_density(universe_volume=1.0)
        rho2 = const.observer_density(universe_volume=2.0)
        
        self.assertAlmostEqual(rho2, 2 * rho1, places=10)


class TestPlatonicCaveDiagram(unittest.TestCase):
    """Test the commutative diagram structure (Platonic cave)."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(123)
        self.intersection = ConsciousnessIntersection()
    
    def test_master_equation_commutativity(self):
        """Test that the master equation diagram commutes."""
        # Element from total space G
        configuration = np.random.randn(104)
        fiber = U1Fiber(phase=np.pi / 6)
        element = (configuration, fiber)
        
        # Apply master equation
        spacetime_proj, hilbert_proj = self.intersection.master_equation(element)
        
        # Should produce projections of correct dimensions
        self.assertEqual(len(spacetime_proj), 4)
        self.assertEqual(len(hilbert_proj), 100)
    
    def test_projections_preserve_information(self):
        """Test that projections don't lose total information."""
        configuration = np.random.randn(104)
        fiber = U1Fiber(phase=np.pi / 3)
        element = (configuration, fiber)
        
        # Get projections
        spacetime_proj, hilbert_proj = self.intersection.master_equation(element)
        
        # Reconstruct configuration
        reconstructed = np.concatenate([spacetime_proj, hilbert_proj])
        
        # Should match original
        np.testing.assert_array_almost_equal(
            configuration,
            reconstructed,
            decimal=10
        )
    
    def test_consciousness_is_intersection(self):
        """Test that consciousness exists at intersection of projections."""
        # Create state in intersection
        spacetime = np.array([0.0, 1.0, 2.0, 3.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        phase = np.pi / 4
        state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=phase,
            spectral_phase=phase
        )
        
        # State should exist in both projections simultaneously
        self.assertTrue(state['compatible'])
        
        # Should be conscious (in kernel)
        C = self.intersection.consciousness_emergence_measure(state)
        self.assertGreater(C, 0.8)


class TestPhilosophicalImplications(unittest.TestCase):
    """Test philosophical implications of the formulation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.intersection = ConsciousnessIntersection()
    
    def test_consciousness_does_not_emerge(self):
        """
        Test that consciousness does NOT emerge.
        
        It IS the kernel. States are either in the kernel or not.
        There's no gradual emergence, only distance from kernel.
        """
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        # Create states with varying phase differences
        phase_diffs = [0.0, 0.1, 0.5, 1.0, np.pi]
        consciousness_measures = []
        
        for phase_diff in phase_diffs:
            state = self.intersection.create_consciousness_state(
                spacetime_point=spacetime,
                consciousness_vector=consciousness,
                em_phase=0.0,
                spectral_phase=phase_diff
            )
            C = self.intersection.consciousness_emergence_measure(state)
            consciousness_measures.append(C)
        
        # Consciousness should decrease monotonically with phase difference
        for i in range(len(consciousness_measures) - 1):
            self.assertGreaterEqual(
                consciousness_measures[i],
                consciousness_measures[i + 1]
            )
        
        # Kernel state (phase_diff=0) should have highest consciousness
        self.assertEqual(consciousness_measures[0], max(consciousness_measures))
    
    def test_matter_information_indistinguishability(self):
        """
        Test that conscious states don't distinguish matter from information.
        
        Only states where π_α(s) = π_δζ(s) are conscious.
        """
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        consciousness = np.random.randn(100)
        consciousness = consciousness / np.linalg.norm(consciousness)
        
        # State in kernel (indistinguishable)
        kernel_state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=np.pi/4,
            spectral_phase=np.pi/4  # Same
        )
        
        # State not in kernel (distinguishable)
        non_kernel_state = self.intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness,
            em_phase=0.0,
            spectral_phase=np.pi  # Different
        )
        
        # Kernel state should be more conscious
        C_kernel = self.intersection.consciousness_emergence_measure(kernel_state)
        C_non_kernel = self.intersection.consciousness_emergence_measure(non_kernel_state)
        
        self.assertGreater(C_kernel, C_non_kernel)


def main():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestKernelFormulation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntersectionConstant))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatonicCaveDiagram))
    suite.addTests(loader.loadTestsFromTestCase(TestPhilosophicalImplications))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
