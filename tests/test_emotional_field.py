#!/usr/bin/env python3
"""
Unit Tests for Emotional Field Framework
========================================

Tests core functionality of the emotional stress-energy tensor framework.

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import unittest
import numpy as np
import sys
import os

# Add path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from qcal.emotional_field.stress_tensor import (
    EmotionalStressTensor,
    EmotionalFieldState,
    StressClassification,
    minkowski_metric
)
from qcal.emotional_field.potential import EmotionalPotential, PotentialParameters
from qcal.emotional_field.sync_protocol import (
    SynchronizationProtocol,
    NodeState
)
from qcal.emotional_field.network_topology import NetworkTopology


class TestStressTensor(unittest.TestCase):
    """Test emotional stress-energy tensor calculations."""
    
    def setUp(self):
        """Initialize test fixtures."""
        self.calculator = EmotionalStressTensor()
        self.g_metric = minkowski_metric()
    
    def test_tensor_symmetry(self):
        """Test that stress tensor is symmetric."""
        state = EmotionalFieldState(
            Phi=0.3,
            nabla_Phi=np.array([0.1, 0.0, 0.0, 0.0]),
            Psi=0.85+0j,
            coherence=0.85,
            x_mu=np.array([0, 0, 0, 0])
        )
        
        V_Phi = 0.045  # Example potential value
        
        T = self.calculator.compute_tensor(state, self.g_metric, V_Phi)
        
        # Check symmetry
        is_symmetric = self.calculator.verify_symmetry(T)
        self.assertTrue(is_symmetric, "Stress tensor should be symmetric")
    
    def test_stress_classification(self):
        """Test stress level classification."""
        # Peace valley
        classification = StressClassification.classify(0.1, coherence=0.9)
        self.assertEqual(classification.region, "Peace Valley")
        self.assertEqual(classification.risk_level, "LOW")
        
        # Work plateau
        classification = StressClassification.classify(0.3, coherence=0.85)
        self.assertEqual(classification.region, "Work Plateau")
        
        # Alert zone
        classification = StressClassification.classify(0.5, coherence=0.75)
        self.assertEqual(classification.region, "Alert Zone")
        self.assertEqual(classification.risk_level, "MEDIUM")
        
        # Singularity
        classification = StressClassification.classify(0.65, coherence=0.7)
        self.assertEqual(classification.region, "Singularity")
        self.assertEqual(classification.risk_level, "HIGH")


class TestEmotionalPotential(unittest.TestCase):
    """Test emotional potential calculations."""
    
    def test_restored_phase(self):
        """Test restored phase (μ² > 0)."""
        params = PotentialParameters(
            lambda_rigidity=1.0,
            mu_squared=1.0,  # Positive
            Phi_0=1.0
        )
        potential = EmotionalPotential(params)
        
        # Should have single minimum at Φ = 0
        minima = potential.find_minima(Psi_squared=0.0)
        
        self.assertEqual(len(minima), 1, "Restored phase should have single minimum")
        self.assertAlmostEqual(minima[0], 0.0, places=2)
    
    def test_broken_symmetry(self):
        """Test broken symmetry phase (μ² < 0)."""
        params = PotentialParameters(
            lambda_rigidity=1.0,
            mu_squared=-1.0,  # Negative
            Phi_0=1.0
        )
        potential = EmotionalPotential(params)
        
        # Should have two minima at ±Φ_min
        minima = potential.find_minima(Psi_squared=0.0)
        
        self.assertEqual(len(minima), 2, "Broken symmetry should have two minima")
        self.assertAlmostEqual(minima[0], -minima[1], places=2)
    
    def test_coherence_healing(self):
        """Test that coherence can restore symmetry."""
        params = PotentialParameters(
            lambda_rigidity=1.0,
            mu_squared=-1.0,
            Phi_0=1.0,
            kappa_int=0.15
        )
        potential = EmotionalPotential(params)
        
        # Low coherence: broken symmetry
        minima_low = potential.find_minima(Psi_squared=0.0)
        self.assertEqual(len(minima_low), 2, "Low coherence: broken symmetry")
        
        # High coherence: restored
        minima_high = potential.find_minima(Psi_squared=10.0)
        self.assertEqual(len(minima_high), 1, "High coherence: symmetry restored")


class TestSynchronizationProtocol(unittest.TestCase):
    """Test synchronization protocol."""
    
    def setUp(self):
        """Initialize test fixtures."""
        self.protocol = SynchronizationProtocol()
    
    def test_resonance_signal(self):
        """Test 141.7 Hz signal generation."""
        t = 0.0
        signal = self.protocol.generate_resonance_signal(t, amplitude=1.0)
        
        # At t=0, sin(0) = 0
        self.assertAlmostEqual(signal, 0.0, places=6)
        
        # At quarter period
        T = 1.0 / self.protocol.f0
        t = T / 4
        signal = self.protocol.generate_resonance_signal(t, amplitude=1.0)
        
        # Should be close to 1.0
        self.assertAlmostEqual(signal, 1.0, places=2)
    
    def test_critical_node_detection(self):
        """Test detection of critical stress nodes."""
        # Create test network
        network = [
            NodeState(
                node_id=0,
                Phi=0.3, dPhi_dt=0.0,
                Psi=0.85+0j, coherence=0.85, phase=0.0,
                T_00=0.3,  # Below critical
                stress_level="Work",
                neighbors=[1]
            ),
            NodeState(
                node_id=1,
                Phi=0.5, dPhi_dt=0.0,
                Psi=0.7+0j, coherence=0.7, phase=0.0,
                T_00=0.65,  # Above critical
                stress_level="Critical",
                neighbors=[0]
            )
        ]
        
        critical = self.protocol.detect_critical_nodes(network)
        
        self.assertEqual(len(critical), 1, "Should detect 1 critical node")
        self.assertEqual(critical[0], 1, "Node 1 should be critical")
    
    def test_sovereignty_index(self):
        """Test collective sovereignty index calculation."""
        # Create simple network
        network = [
            NodeState(
                node_id=i,
                Phi=0.2, dPhi_dt=0.0,
                Psi=0.9+0j, coherence=0.9, phase=0.0,
                T_00=0.1,  # Low stress
                stress_level="Peace",
                neighbors=[]
            )
            for i in range(10)
        ]
        
        S_col = self.protocol.compute_sovereignty_index(network)
        
        # High coherence, low stress → high sovereignty
        self.assertGreater(S_col, 0.5, "High coherence should give S_col > 0.5")


class TestNetworkTopology(unittest.TestCase):
    """Test network topology analysis."""
    
    def setUp(self):
        """Initialize test fixtures."""
        self.analyzer = NetworkTopology()
    
    def test_betti_0(self):
        """Test β₀ calculation (connected components)."""
        # Two separate components
        nodes = [0, 1, 2, 3]
        connections = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        
        G = self.analyzer.build_graph(nodes, connections)
        beta_0 = self.analyzer.compute_beta_0(G)
        
        self.assertEqual(beta_0, 2, "Should detect 2 connected components")
    
    def test_betti_1(self):
        """Test β₁ calculation (cycles)."""
        # Triangle (1 cycle)
        nodes = [0, 1, 2]
        connections = {
            0: [1, 2],
            1: [0, 2],
            2: [0, 1]
        }
        
        G = self.analyzer.build_graph(nodes, connections)
        beta_1 = self.analyzer.compute_beta_1(G)
        
        self.assertGreater(beta_1, 0, "Triangle should have at least 1 cycle")
    
    def test_winding_number(self):
        """Test winding number calculation."""
        # Simple cycle with phases
        phases = {0: 0.0, 1: np.pi/2, 2: np.pi, 3: 3*np.pi/2}
        boundary = [0, 1, 2, 3]
        
        W = self.analyzer.compute_winding_number(phases, boundary)
        
        # Full 2π winding → W ≈ 1
        self.assertAlmostEqual(W, 1.0, places=1)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def test_complete_workflow(self):
        """Test complete analysis workflow."""
        # Create small network
        from qcal.emotional_field.sync_protocol import create_example_network
        
        network = create_example_network(num_nodes=10)
        
        # Initialize components
        protocol = SynchronizationProtocol()
        topology = NetworkTopology()
        
        # Extract data
        nodes = [n.node_id for n in network]
        connections = {n.node_id: n.neighbors for n in network}
        stress_levels = {n.node_id: n.T_00 for n in network}
        
        # Analyze
        features = topology.analyze_network(nodes, connections, stress_levels)
        S_col = protocol.compute_sovereignty_index(network)
        
        # Verify results make sense
        self.assertGreater(features.num_nodes, 0)
        self.assertGreaterEqual(features.beta_0, 1)
        self.assertGreaterEqual(S_col, 0.0)
        self.assertLessEqual(S_col, 1.0)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStressTensor))
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionalPotential))
    suite.addTests(loader.loadTestsFromTestCase(TestSynchronizationProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkTopology))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
