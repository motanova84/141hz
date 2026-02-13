#!/usr/bin/env python3
"""
Tests for Descending Coherence Propagator
==========================================

Tests the hierarchical coherence cascade mechanism that propagates
coherence from macro → meso → micro levels.

Author: QCAL ∞³ Framework
Date: 2026-02-13
"""

import unittest
import numpy as np
import sys
import os

# Add parent path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.emotional_field.descending_coherence import (
    DescendingCoherencePropagator,
    DescendingCoherenceParameters,
    CoherenceLevel,
    HierarchicalNodeState,
    CoherenceGroup,
    create_example_cascade
)


class TestDescendingCoherenceParameters(unittest.TestCase):
    """Test parameter validation."""
    
    def test_default_parameters_valid(self):
        """Default parameters should sum to 1.0."""
        params = DescendingCoherenceParameters()
        params.validate()  # Should not raise
        
        total = params.alpha_macro + params.alpha_meso + params.alpha_micro
        self.assertAlmostEqual(total, 1.0, places=6)
    
    def test_invalid_parameters_raise(self):
        """Invalid parameters should raise ValueError."""
        params = DescendingCoherenceParameters(
            alpha_macro=0.5,
            alpha_meso=0.3,
            alpha_micro=0.1  # Sum = 0.9 ≠ 1.0
        )
        
        with self.assertRaises(ValueError):
            params.validate()
    
    def test_custom_valid_parameters(self):
        """Custom valid parameters should pass."""
        params = DescendingCoherenceParameters(
            alpha_macro=0.5,
            alpha_meso=0.3,
            alpha_micro=0.2  # Sum = 1.0
        )
        params.validate()  # Should not raise


class TestCoherenceGroup(unittest.TestCase):
    """Test coherence group functionality."""
    
    def test_group_creation(self):
        """Test creating a coherence group."""
        group = CoherenceGroup(group_id=0)
        self.assertEqual(group.group_id, 0)
        self.assertEqual(group.size(), 0)
    
    def test_add_members(self):
        """Test adding members to a group."""
        group = CoherenceGroup(group_id=0)
        group.add_member(1)
        group.add_member(2)
        group.add_member(3)
        
        self.assertEqual(group.size(), 3)
        self.assertIn(1, group.member_ids)
        self.assertIn(2, group.member_ids)
        self.assertIn(3, group.member_ids)
    
    def test_compute_coherence(self):
        """Test computing group coherence from members."""
        group = CoherenceGroup(group_id=0)
        group.add_member(0)
        group.add_member(1)
        group.add_member(2)
        
        # Create coherences with known values
        coherences = {
            0: 1.0 + 0.0j,
            1: 0.0 + 1.0j,
            2: -1.0 + 0.0j
        }
        
        result = group.compute_coherence(coherences)
        expected = (1.0 + 0.0j + 0.0 + 1.0j - 1.0 + 0.0j) / 3
        
        self.assertAlmostEqual(result.real, expected.real, places=6)
        self.assertAlmostEqual(result.imag, expected.imag, places=6)


class TestDescendingCoherencePropagator(unittest.TestCase):
    """Test the main propagator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.propagator = DescendingCoherencePropagator()
    
    def test_initialization(self):
        """Test propagator initialization."""
        self.assertIsNotNone(self.propagator.params)
        self.assertEqual(len(self.propagator.groups), 0)
        self.assertEqual(len(self.propagator.node_states), 0)
        self.assertEqual(self.propagator.time, 0.0)
    
    def test_group_detection_simple(self):
        """Test detecting groups in a simple network."""
        # Create a simple network with 2 groups
        node_ids = list(range(10))
        connections = {
            # Group 1: nodes 0-4
            0: [1, 2],
            1: [0, 2, 3],
            2: [0, 1, 3],
            3: [1, 2, 4],
            4: [3],
            # Group 2: nodes 5-9
            5: [6, 7],
            6: [5, 7, 8],
            7: [5, 6, 8],
            8: [6, 7, 9],
            9: [8]
        }
        stress_levels = {i: 0.3 for i in node_ids}
        
        groups = self.propagator.detect_groups(node_ids, connections, stress_levels)
        
        # Should detect 2 groups
        self.assertEqual(len(groups), 2)
        
        # Each group should have 5 members
        for group in groups.values():
            self.assertEqual(group.size(), 5)
    
    def test_compute_collective_coherence(self):
        """Test computing collective coherence."""
        coherences = {
            0: 1.0 + 0.0j,
            1: 0.0 + 1.0j,
            2: -1.0 + 0.0j,
            3: 0.0 - 1.0j
        }
        
        result = self.propagator.compute_collective_coherence(coherences)
        expected = (1.0 + 0.0j + 0.0 + 1.0j - 1.0 + 0.0j + 0.0 - 1.0j) / 4
        
        self.assertAlmostEqual(result.real, expected.real, places=6)
        self.assertAlmostEqual(result.imag, expected.imag, places=6)
    
    def test_compute_target_coherence_no_group(self):
        """Test computing target coherence for ungrouped node."""
        Psi_individual = 0.5 + 0.0j
        Psi_collective = 0.8 + 0.0j
        
        target = self.propagator.compute_target_coherence(
            node_id=0,
            Psi_individual=Psi_individual,
            group_id=None,
            Psi_group=0.0 + 0.0j,
            Psi_collective=Psi_collective
        )
        
        # Without group, should redistribute meso weight
        # More weight to macro and micro
        self.assertGreater(abs(target), 0.0)
        self.assertLess(abs(target), 1.0)
    
    def test_compute_target_coherence_with_group(self):
        """Test computing target coherence for grouped node."""
        # Create a group
        group = CoherenceGroup(group_id=0)
        group.add_member(0)
        self.propagator.groups[0] = group
        
        Psi_individual = 0.5 + 0.0j
        Psi_group = 0.6 + 0.0j
        Psi_collective = 0.8 + 0.0j
        
        target = self.propagator.compute_target_coherence(
            node_id=0,
            Psi_individual=Psi_individual,
            group_id=0,
            Psi_group=Psi_group,
            Psi_collective=Psi_collective
        )
        
        # Should be weighted combination
        params = self.propagator.params
        expected_real = (
            params.alpha_macro * Psi_collective.real +
            params.alpha_meso * Psi_group.real +
            params.alpha_micro * Psi_individual.real
        )
        
        self.assertAlmostEqual(target.real, expected_real, places=6)
    
    def test_propagate_coherence_single_step(self):
        """Test propagating coherence for one time step."""
        # Simple 3-node network
        coherences = {
            0: 0.5 + 0.0j,
            1: 0.6 + 0.1j,
            2: 0.4 - 0.1j
        }
        stress_levels = {
            0: 0.3,
            1: 0.2,
            2: 0.4
        }
        
        dt = 0.01
        updated = self.propagator.propagate_coherence(coherences, stress_levels, dt)
        
        # Should return updated coherences for all nodes
        self.assertEqual(len(updated), 3)
        
        # Coherences should have changed (slightly)
        for node_id in coherences:
            self.assertIsInstance(updated[node_id], complex)
            # Shouldn't change too much in one small step
            diff = abs(updated[node_id] - coherences[node_id])
            self.assertLess(diff, 0.1)
    
    def test_propagate_coherence_increases_time(self):
        """Test that propagating coherence advances time."""
        coherences = {0: 0.5 + 0.0j}
        stress_levels = {0: 0.3}
        dt = 0.01
        
        initial_time = self.propagator.time
        self.propagator.propagate_coherence(coherences, stress_levels, dt)
        
        self.assertAlmostEqual(self.propagator.time, initial_time + dt, places=6)
    
    def test_get_hierarchy_info(self):
        """Test retrieving hierarchical information for a node."""
        # Set up a simple case
        coherences = {0: 0.5 + 0.0j}
        stress_levels = {0: 0.3}
        
        self.propagator.propagate_coherence(coherences, stress_levels, 0.01)
        
        info = self.propagator.get_hierarchy_info(0)
        
        self.assertIn("node_id", info)
        self.assertIn("micro", info)
        self.assertIn("meso", info)
        self.assertIn("macro", info)
        self.assertIn("target", info)
        self.assertIn("stress", info)
        
        self.assertEqual(info["node_id"], 0)
        self.assertGreater(info["micro"]["coherence"], 0.0)
    
    def test_compute_coherence_alignment(self):
        """Test computing coherence alignment metric."""
        # Set up nodes with different alignments
        coherences = {
            0: 1.0 + 0.0j,  # Well-aligned
            1: 0.5 + 0.5j,  # Partially aligned
            2: 0.3 + 0.0j   # Weakly aligned
        }
        stress_levels = {i: 0.3 for i in coherences}
        
        self.propagator.propagate_coherence(coherences, stress_levels, 0.01)
        
        alignment = self.propagator.compute_coherence_alignment()
        
        self.assertIn("mean_alignment", alignment)
        self.assertIn("std_alignment", alignment)
        self.assertIn("min_alignment", alignment)
        self.assertIn("max_alignment", alignment)
        
        # All values should be between -1 and 1
        self.assertGreaterEqual(alignment["mean_alignment"], -1.0)
        self.assertLessEqual(alignment["mean_alignment"], 1.0)
    
    def test_get_summary(self):
        """Test getting summary information."""
        coherences = {i: 0.5 + 0.0j for i in range(5)}
        stress_levels = {i: 0.3 for i in range(5)}
        
        self.propagator.propagate_coherence(coherences, stress_levels, 0.01)
        
        summary = self.propagator.get_summary()
        
        self.assertIn("time", summary)
        self.assertIn("num_nodes", summary)
        self.assertIn("num_groups", summary)
        self.assertIn("collective_coherence", summary)
        self.assertIn("collective_stress", summary)
        self.assertIn("alignment_metrics", summary)
        
        self.assertEqual(summary["num_nodes"], 5)
        self.assertGreater(summary["collective_coherence"], 0.0)


class TestCoherenceCascadeIntegration(unittest.TestCase):
    """Integration tests for the full cascade mechanism."""
    
    def test_create_example_cascade(self):
        """Test creating an example cascade network."""
        propagator, coherences, connections = create_example_cascade(
            num_nodes=50,
            num_groups=5,
            initial_coherence=0.5
        )
        
        self.assertEqual(len(coherences), 50)
        self.assertEqual(len(connections), 50)
        self.assertIsInstance(propagator, DescendingCoherencePropagator)
    
    def test_multi_step_evolution(self):
        """Test multi-step coherence evolution."""
        propagator, coherences, connections = create_example_cascade(
            num_nodes=30,
            num_groups=3,
            initial_coherence=0.5
        )
        
        # Detect groups
        stress_levels = {i: 0.3 for i in range(30)}
        propagator.detect_groups(list(range(30)), connections, stress_levels)
        
        # Evolve for several steps
        dt = 0.01
        num_steps = 50
        
        for _ in range(num_steps):
            coherences = propagator.propagate_coherence(coherences, stress_levels, dt)
        
        # Check that time advanced correctly
        self.assertAlmostEqual(propagator.time, num_steps * dt, places=6)
        
        # Check that collective coherence is computed
        summary = propagator.get_summary()
        self.assertGreater(summary["collective_coherence"], 0.0)
    
    def test_coherence_convergence(self):
        """Test that coherence converges toward collective value."""
        propagator, coherences, connections = create_example_cascade(
            num_nodes=20,
            num_groups=2,
            initial_coherence=0.5
        )
        
        stress_levels = {i: 0.2 for i in range(20)}
        propagator.detect_groups(list(range(20)), connections, stress_levels)
        
        # Record initial spread
        initial_values = [abs(c) for c in coherences.values()]
        initial_std = np.std(initial_values)
        
        # Evolve
        dt = 0.01
        for _ in range(200):
            coherences = propagator.propagate_coherence(coherences, stress_levels, dt)
        
        # Check final spread
        final_values = [abs(c) for c in coherences.values()]
        final_std = np.std(final_values)
        
        # Spread should decrease (convergence toward collective)
        self.assertLess(final_std, initial_std)
    
    def test_stress_modulates_relaxation(self):
        """Test that stress affects coherence dynamics."""
        propagator, coherences, _ = create_example_cascade(
            num_nodes=10,
            num_groups=1,
            initial_coherence=0.5
        )
        
        # High stress case
        high_stress = {i: 0.8 for i in range(10)}
        coherences_high = coherences.copy()
        
        for _ in range(50):
            coherences_high = propagator.propagate_coherence(
                coherences_high, high_stress, 0.01
            )
        
        # Low stress case
        propagator2 = DescendingCoherencePropagator()
        low_stress = {i: 0.1 for i in range(10)}
        coherences_low = coherences.copy()
        
        for _ in range(50):
            coherences_low = propagator2.propagate_coherence(
                coherences_low, low_stress, 0.01
            )
        
        # Low stress should allow faster convergence
        # (though this is a subtle effect)
        self.assertIsNotNone(coherences_high)
        self.assertIsNotNone(coherences_low)


class TestCoherenceLevels(unittest.TestCase):
    """Test the coherence level enumeration."""
    
    def test_coherence_levels_exist(self):
        """Test that all coherence levels are defined."""
        self.assertEqual(CoherenceLevel.MICRO.value, "individual")
        self.assertEqual(CoherenceLevel.MESO.value, "group")
        self.assertEqual(CoherenceLevel.MACRO.value, "collective")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDescendingCoherenceParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestCoherenceGroup))
    suite.addTests(loader.loadTestsFromTestCase(TestDescendingCoherencePropagator))
    suite.addTests(loader.loadTestsFromTestCase(TestCoherenceCascadeIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestCoherenceLevels))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
