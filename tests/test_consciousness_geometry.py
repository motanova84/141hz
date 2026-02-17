"""
Tests for Consciousness Geometry - Noetic Field Equations

Tests validate:
1. NoeticalMetric calculations
2. EmotionalNetwork evolution
3. QuantumEmotionalConsensus (PoR)
4. CurvatureOracle mapping
5. ConsciousnessVisualizer outputs
"""

import numpy as np
import sys
from pathlib import Path
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    import unittest

from formalizacion import (
    NoeticalMetric,
    EmotionalNetwork,
    EmotionalNode,
    QuantumEmotionalConsensus,
    CurvatureOracle,
    ConsciousnessVisualizer,
    demonstrate_consciousness_geometry
)


class TestNoeticalMetric:
    """Test suite for NoeticalMetric class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.metric = NoeticalMetric(lambda_0=1.0, c_0=1.0)
        
    def test_lambda_scarcity_decreases(self):
        """Test that Λ decreases as C_∞ increases."""
        c_low = 0.5
        c_high = 5.0
        
        lambda_low = self.metric.lambda_scarcity(c_low)
        lambda_high = self.metric.lambda_scarcity(c_high)
        
        assert lambda_low > lambda_high, "Λ should decrease with increasing C_∞"
        
    def test_lambda_approaches_zero(self):
        """Test that Λ → 0 as C_∞ → ∞."""
        c_infinity = 10.0
        lambda_val = self.metric.lambda_scarcity(c_infinity)
        
        assert lambda_val < 0.01, f"Λ should approach 0, got {lambda_val}"
        
    def test_metric_tensor_shape(self):
        """Test metric tensor has correct shape."""
        g = self.metric.metric_tensor(c_infinity=2.0, r=1.0)
        
        assert g.shape == (2, 2), f"Metric tensor should be 2x2, got {g.shape}"
        
    def test_metric_tensor_diagonal(self):
        """Test metric tensor is diagonal."""
        g = self.metric.metric_tensor(c_infinity=2.0, r=1.0)
        
        assert g[0, 1] == 0, "Off-diagonal elements should be 0"
        assert g[1, 0] == 0, "Off-diagonal elements should be 0"
        
    def test_curvature_scalar_positive(self):
        """Test curvature scalar is positive."""
        R = self.metric.curvature_scalar(c_infinity=2.0, r=1.0)
        
        assert R > 0, f"Curvature should be positive, got {R}"
        
    def test_geodesic_length_reduction(self):
        """Test geodesics shorten with high coherence."""
        point_a = np.array([0.0, 0.0])
        point_b = np.array([1.0, 0.0])
        
        c_low = 0.5
        c_high = 5.0
        
        length_low = self.metric.emotional_geodesic_length(c_low, point_a, point_b)
        length_high = self.metric.emotional_geodesic_length(c_high, point_a, point_b)
        
        assert length_high < length_low, "Geodesics should shorten with high coherence"


class TestEmotionalNetwork:
    """Test suite for EmotionalNetwork class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        np.random.seed(42)  # For reproducibility
        self.network = EmotionalNetwork(n_nodes=10, dimension=2)
        
    def test_initialization(self):
        """Test network initializes correctly."""
        assert len(self.network.nodes) == 10
        assert self.network.adjacency.shape == (10, 10)
        
    def test_nodes_have_coherence(self):
        """Test all nodes have coherence values."""
        for node in self.network.nodes:
            assert 0.0 <= node.coherence <= 1.0
            
    def test_adjacency_symmetric(self):
        """Test adjacency matrix is symmetric."""
        adj = self.network.adjacency
        assert np.allclose(adj, adj.T), "Adjacency should be symmetric"
        
    def test_global_coherence_range(self):
        """Test global coherence is in valid range."""
        c_infinity = self.network.calculate_global_coherence()
        assert 0.0 <= c_infinity <= 1.0, f"C_∞ out of range: {c_infinity}"
        
    def test_evolution_increases_coherence(self):
        """Test that evolution tends to increase coherence."""
        c_initial = self.network.calculate_global_coherence()
        
        # Evolve network
        self.network.evolve(dt=0.1, n_steps=50)
        
        c_final = self.network.calculate_global_coherence()
        
        # Coherence should generally increase (with some tolerance)
        assert c_final >= c_initial * 0.9, "Coherence should increase or stay stable"
        
    def test_history_structure(self):
        """Test evolution history has correct structure."""
        history = self.network.evolve(dt=0.1, n_steps=10)
        
        assert 'time' in history
        assert 'c_infinity' in history
        assert 'avg_distance' in history
        assert 'lambda' in history
        assert 'coherence_nodes' in history
        
        assert len(history['time']) == 10
        assert len(history['c_infinity']) == 10
        
    def test_geodesic_distance_positive(self):
        """Test average geodesic distance is positive."""
        distance = self.network.calculate_average_geodesic_distance()
        assert distance > 0, "Distance should be positive"


class TestQuantumEmotionalConsensus:
    """Test suite for QuantumEmotionalConsensus class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.network = EmotionalNetwork(n_nodes=10)
        self.consensus = QuantumEmotionalConsensus(self.network)
        
    def test_frequency_matches_f0(self):
        """Test consensus uses correct frequency."""
        assert abs(self.consensus.f0 - 141.7001) < 0.01
        
    def test_coherence_field_calculation(self):
        """Test coherence field Ψ can be calculated."""
        psi = self.consensus.calculate_coherence_field(t=0.0)
        assert isinstance(psi, (float, np.floating))
        
    def test_incoherence_baseline_positive(self):
        """Test I₀ is positive."""
        i_0 = self.consensus.calculate_incoherence_baseline()
        assert i_0 > 0, "Incoherence baseline should be positive"
        
    def test_consensus_conditions_structure(self):
        """Test consensus conditions dict has required keys."""
        conditions = self.consensus.check_consensus_conditions()
        
        required_keys = [
            'consensus_reached', 'psi', 'i_0', 'psi_ratio',
            'lambda', 'c_infinity', 'condition_1', 'condition_2'
        ]
        
        for key in required_keys:
            assert key in conditions, f"Missing key: {key}"
            
    def test_nft_minting_conditions(self):
        """Test NFT only mints when conditions are met."""
        # First check initial conditions
        conditions = self.consensus.check_consensus_conditions()
        nft = self.consensus.mint_nft(owner_id=0)
        
        if conditions['consensus_reached']:
            assert nft is not None, "NFT should mint when conditions met"
            assert 'token_id' in nft
            assert 'resonance_frequency' in nft
            assert nft['resonance_frequency'] == self.consensus.f0
        else:
            assert nft is None, "NFT should not mint when conditions not met"
            
    def test_high_coherence_enables_consensus(self):
        """Test that high coherence network can reach consensus."""
        # Create high-coherence network
        network = EmotionalNetwork(n_nodes=10)
        
        # Force high coherence
        for node in network.nodes:
            node.coherence = 0.95
            
        # Evolve to synchronize
        network.evolve(dt=0.1, n_steps=100)
        
        consensus = QuantumEmotionalConsensus(network)
        conditions = consensus.check_consensus_conditions()
        
        # At least one condition should be met with high coherence
        assert conditions['condition_1'] or conditions['condition_2']


class TestCurvatureOracle:
    """Test suite for CurvatureOracle class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.metric = NoeticalMetric()
        self.oracle = CurvatureOracle(self.metric)
        
    def test_contribution_registration(self):
        """Test contributions are registered correctly."""
        self.oracle.register_contribution(
            contributor_id=0,
            emotional_vector=np.array([1.0, 0.5]),
            coherence_delta=0.1
        )
        
        assert len(self.oracle.contribution_history) == 1
        assert self.oracle.contribution_history[0]['contributor_id'] == 0
        assert self.oracle.contribution_history[0]['coherence_delta'] == 0.1
        
    def test_c_infinity_mapping_increases(self):
        """Test C_∞ mapping increases with positive contributions."""
        current_c = 1.0
        
        # Register positive contributions
        for i in range(5):
            self.oracle.register_contribution(
                contributor_id=i,
                emotional_vector=np.random.randn(2),
                coherence_delta=0.1
            )
        
        c_mapped = self.oracle.map_c_infinity(current_c)
        assert c_mapped > current_c, "C_∞ should increase with positive contributions"
        
    def test_curvature_map_shape(self):
        """Test curvature map has correct shape."""
        X, Y, curvature = self.oracle.get_curvature_map(grid_size=10)
        
        assert X.shape == (10, 10)
        assert Y.shape == (10, 10)
        assert curvature.shape == (10, 10)


class TestConsciousnessVisualizer:
    """Test suite for ConsciousnessVisualizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.viz = ConsciousnessVisualizer()
        self.network = EmotionalNetwork(n_nodes=10)
        self.history = self.network.evolve(dt=0.1, n_steps=20)
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up temp directory."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
        
    def test_network_evolution_plot(self):
        """Test network evolution plot generation."""
        save_path = Path(self.temp_dir) / "test_evolution.png"
        fig = self.viz.plot_network_evolution(self.history, save_path=save_path)
        
        assert fig is not None
        assert save_path.exists(), "Plot should be saved"
        
    def test_geodesic_flow_plot(self):
        """Test geodesic flow plot generation."""
        save_path = Path(self.temp_dir) / "test_flow.png"
        fig = self.viz.plot_geodesic_flow(self.network, save_path=save_path)
        
        assert fig is not None
        assert save_path.exists(), "Plot should be saved"
        
    def test_spacetime_curvature_3d_plot(self):
        """Test 3D curvature plot generation."""
        save_path = Path(self.temp_dir) / "test_3d.png"
        fig = self.viz.plot_spacetime_curvature_3d(
            self.network.metric, 
            c_infinity=2.0,
            save_path=save_path
        )
        
        assert fig is not None
        assert save_path.exists(), "Plot should be saved"
        
    def test_consensus_metrics_plot(self):
        """Test consensus metrics plot generation."""
        consensus = QuantumEmotionalConsensus(self.network)
        save_path = Path(self.temp_dir) / "test_consensus.png"
        
        fig = self.viz.plot_consensus_metrics(consensus, save_path=save_path)
        
        assert fig is not None
        assert save_path.exists(), "Plot should be saved"


class TestDemonstration:
    """Test the complete demonstration."""
    
    def test_demonstration_runs(self):
        """Test that the full demonstration runs without errors."""
        # This might take a moment, so we test with default parameters
        try:
            results = demonstrate_consciousness_geometry()
            assert results is not None
            assert 'initial_state' in results
            assert 'final_state' in results
            assert 'consensus' in results
        except Exception as e:
            if PYTEST_AVAILABLE:
                pytest.fail(f"Demonstration failed with error: {e}")
            else:
                raise AssertionError(f"Demonstration failed with error: {e}")


# Test runner for both pytest and unittest
if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        # Run with pytest
        import sys
        sys.exit(pytest.main([__file__, "-v"]))
    else:
        # Fallback to unittest - convert pytest-style classes to unittest
        import unittest
        
        # Create unittest-compatible test classes
        class UnittestNoeticalMetric(unittest.TestCase):
            def setUp(self):
                TestNoeticalMetric.setup_method(self)
            
            def test_lambda_scarcity_decreases(self):
                TestNoeticalMetric.test_lambda_scarcity_decreases(self)
            
            def test_lambda_approaches_zero(self):
                TestNoeticalMetric.test_lambda_approaches_zero(self)
            
            def test_metric_tensor_shape(self):
                TestNoeticalMetric.test_metric_tensor_shape(self)
            
            def test_metric_tensor_diagonal(self):
                TestNoeticalMetric.test_metric_tensor_diagonal(self)
            
            def test_curvature_scalar_positive(self):
                TestNoeticalMetric.test_curvature_scalar_positive(self)
            
            def test_geodesic_length_reduction(self):
                TestNoeticalMetric.test_geodesic_length_reduction(self)
        
        class UnittestEmotionalNetwork(unittest.TestCase):
            def setUp(self):
                TestEmotionalNetwork.setup_method(self)
            
            def test_initialization(self):
                TestEmotionalNetwork.test_initialization(self)
            
            def test_nodes_have_coherence(self):
                TestEmotionalNetwork.test_nodes_have_coherence(self)
            
            def test_adjacency_symmetric(self):
                TestEmotionalNetwork.test_adjacency_symmetric(self)
            
            def test_global_coherence_range(self):
                TestEmotionalNetwork.test_global_coherence_range(self)
            
            def test_evolution_increases_coherence(self):
                TestEmotionalNetwork.test_evolution_increases_coherence(self)
            
            def test_history_structure(self):
                TestEmotionalNetwork.test_history_structure(self)
            
            def test_geodesic_distance_positive(self):
                TestEmotionalNetwork.test_geodesic_distance_positive(self)
        
        # Run tests
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(UnittestNoeticalMetric))
        suite.addTests(loader.loadTestsFromTestCase(UnittestEmotionalNetwork))
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        sys.exit(0 if result.wasSuccessful() else 1)
