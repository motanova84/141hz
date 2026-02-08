#!/usr/bin/env python3
"""
Tests for Local Node Simulation - Protocol Ψ-Q1

Tests the local node simulation system for neurons, MCP servers, and cells
operating at f₀ = 141.7001 Hz.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import pytest
import numpy as np
from qcal.local_node_simulation import LocalNodeSimulation, NodeState


class TestNodeState:
    """Tests for NodeState dataclass."""
    
    def test_node_state_creation(self):
        """Test creating a NodeState."""
        state = NodeState(
            node_id="TEST_001",
            node_type="neuron",
            I=0.8,
            A_eff=2.0
        )
        
        assert state.node_id == "TEST_001"
        assert state.node_type == "neuron"
        assert state.I == 0.8
        assert state.A_eff == 2.0
        assert state.timestamp > 0
    
    def test_psi_calculation(self):
        """Test Ψ = I × A_eff² calculation."""
        state = NodeState(
            node_id="TEST_002",
            node_type="cell",
            I=0.5,
            A_eff=2.0
        )
        
        expected_psi = 0.5 * (2.0 ** 2)
        assert state.psi == expected_psi
        assert state.psi == 2.0
    
    def test_coherence_levels(self):
        """Test coherence level classification."""
        # Sueño profundo
        state1 = NodeState("n1", "neuron", I=0.2, A_eff=1.0)
        assert state1.coherence_level == "sueño_profundo"
        
        # Vigilia
        state2 = NodeState("n2", "neuron", I=0.5, A_eff=1.0)
        assert state2.coherence_level == "vigilia"
        
        # Meditación
        state3 = NodeState("n3", "neuron", I=0.8, A_eff=1.5)
        assert state3.coherence_level == "meditación"
        
        # Coherencia máxima
        state4 = NodeState("n4", "neuron", I=0.9, A_eff=3.0)
        assert state4.coherence_level == "coherencia_máxima"


class TestLocalNodeSimulation:
    """Tests for LocalNodeSimulation class."""
    
    def test_initialization(self):
        """Test node initialization."""
        node = LocalNodeSimulation(
            node_id="TEST_MCP_001",
            node_type="mcp_server",
            f0=141.7001
        )
        
        assert node.node_id == "TEST_MCP_001"
        assert node.node_type == "mcp_server"
        assert node.f0 == 141.7001
        assert node.state.I == 0.5
        assert node.state.A_eff == 1.0
    
    def test_set_attention_level(self):
        """Test setting attention level."""
        node = LocalNodeSimulation()
        
        initial_A_eff = node.state.A_eff
        node.set_attention_level(2.5)
        
        assert node.state.A_eff == 2.5
        assert len(node.state_history) == 1
        assert node.state_history[0].A_eff == initial_A_eff
    
    def test_invalid_attention_level(self):
        """Test that negative A_eff raises error."""
        node = LocalNodeSimulation()
        
        with pytest.raises(ValueError):
            node.set_attention_level(-1.0)
    
    def test_energy_density_Xi00(self):
        """Test energy density calculation Ξ₀₀."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.0)
        
        Xi_00 = node.compute_energy_density_Xi00(t=0.0)
        
        # Should be positive
        assert Xi_00 > 0
        
        # Should increase with A_eff
        node.set_attention_level(3.0)
        Xi_00_higher = node.compute_energy_density_Xi00(t=0.0)
        assert Xi_00_higher > Xi_00
    
    def test_coherence_lens_strength(self):
        """Test coherence lens strength calculation."""
        node = LocalNodeSimulation()
        
        # A_eff = 1.0 → No lens
        node.set_attention_level(1.0)
        lens1 = node.compute_coherence_lens_strength()
        assert lens1 == 0.0
        
        # A_eff > 1.0 → Lens activates
        node.set_attention_level(2.0)
        lens2 = node.compute_coherence_lens_strength()
        assert lens2 > 0
        
        # A_eff = 3.0 → Strong lens
        node.set_attention_level(3.0)
        lens3 = node.compute_coherence_lens_strength()
        assert lens3 > lens2
        assert lens3 <= 1.0
    
    def test_thermal_noise_filtering(self):
        """Test thermal noise filtering."""
        node = LocalNodeSimulation()
        
        # Create clean signal
        signal = np.ones(100)
        
        # Low coherence → More noise passes
        node.set_attention_level(1.0)
        filtered_low = node.filter_thermal_noise(signal, noise_level=0.1)
        noise_low = np.std(filtered_low - signal)
        
        # High coherence → Less noise passes
        node.set_attention_level(3.0)
        filtered_high = node.filter_thermal_noise(signal, noise_level=0.1)
        noise_high = np.std(filtered_high - signal)
        
        # High coherence should have less noise
        assert noise_high < noise_low
    
    def test_metric_tensor(self):
        """Test metric tensor computation."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.0)
        
        coords = np.array([0.0, 0.0, 0.0, 0.0])
        g = node.compute_metric_tensor(coords)
        
        # Should be 4x4
        assert g.shape == (4, 4)
        
        # Should be close to Minkowski for small perturbations
        g_minkowski = np.diag([-1, 1, 1, 1])
        diff = np.abs(g - g_minkowski)
        assert np.all(diff < 0.1)  # Small perturbation
    
    def test_einstein_tensor(self):
        """Test Einstein tensor computation."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.0)
        
        coords = np.array([0.0, 0.0, 0.0, 0.0])
        G = node.compute_einstein_tensor(coords)
        
        # Should be 4x4
        assert G.shape == (4, 4)
        
        # Energy density should be positive
        assert G[0, 0] > 0
    
    def test_phase_coupling_141hz(self):
        """Test phase coupling at 141.7 Hz."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.5)
        
        # At t=0
        coupling_0 = node.compute_phase_coupling_141hz(t=0.0)
        assert isinstance(coupling_0, complex)
        assert abs(coupling_0) <= 1.0
        
        # At different time
        coupling_1 = node.compute_phase_coupling_141hz(t=0.1)
        assert coupling_0 != coupling_1  # Should vary with time
    
    def test_merkaba_stability(self):
        """Test Merkaba stability calculation."""
        node = LocalNodeSimulation()
        
        # Low coherence
        node.set_attention_level(1.0)
        stability_low = node.compute_merkaba_stability()
        
        # High coherence
        node.set_attention_level(3.0)
        stability_high = node.compute_merkaba_stability()
        
        # Higher coherence → Higher stability
        assert stability_high > stability_low
        assert 0 <= stability_high <= 1.0
    
    def test_weyl_resonance(self):
        """Test Weyl resonance verification."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.5)
        
        # First Riemann zeros (imaginary parts)
        riemann_zeros = np.array([14.134725, 21.022040, 25.010858])
        
        weyl = node.verify_weyl_resonance(riemann_zeros)
        
        assert "frequencies_hz" in weyl
        assert "alignment_scores" in weyl
        assert "mean_alignment" in weyl
        assert "resonance_strength" in weyl
        assert "riemann_coupling" in weyl
        
        assert len(weyl["frequencies_hz"]) == 3
        assert 0 <= weyl["mean_alignment"] <= 1.0
        assert isinstance(weyl["riemann_coupling"], bool)
    
    def test_picode_certificate_generation(self):
        """Test πCODE certificate generation."""
        node = LocalNodeSimulation()
        node.set_attention_level(2.8)
        
        cert = node.generate_picode_certificate()
        
        # Check structure
        assert "protocol" in cert
        assert cert["protocol"] == "Ψ-Q1"
        assert "node_state" in cert
        assert "metrics" in cert
        assert "certification" in cert
        assert "compression_ratio" in cert
        assert "signature" in cert
        
        # Check metrics
        assert "merkaba_stability" in cert["metrics"]
        assert "psi_value" in cert["metrics"]
        assert "weyl_resonance" in cert["metrics"]
        
        # Check certification flags
        assert isinstance(cert["certification"]["merkaba_achieved"], bool)
        assert isinstance(cert["certification"]["psi_achieved"], bool)
        assert isinstance(cert["certification"]["protocol_compliant"], bool)
    
    def test_compression_ratio(self):
        """Test token compression ratio."""
        node = LocalNodeSimulation()
        
        # Low coherence → Low compression
        node.set_attention_level(1.0)
        ratio_low = node._compute_compression_ratio()
        
        # High coherence → High compression
        node.set_attention_level(3.0)
        ratio_high = node._compute_compression_ratio()
        
        assert ratio_high > ratio_low
        assert ratio_high <= 1000.0  # Max compression
    
    def test_protocol_psi_q1_execution(self):
        """Test full Protocol Ψ-Q1 execution."""
        node = LocalNodeSimulation(
            node_id="TEST_PROTOCOL",
            node_type="neuron"
        )
        
        results = node.run_protocol_psi_q1(
            target_A_eff=3.0,
            duration=0.5,
            steps=50
        )
        
        # Check structure
        assert "protocol" in results
        assert results["protocol"] == "Ψ-Q1"
        assert "time_series" in results
        assert "final_state" in results
        assert "certificate" in results
        assert "success_metrics" in results
        
        # Check time series
        ts = results["time_series"]
        assert len(ts["time"]) == 50
        assert len(ts["A_eff"]) == 50
        assert len(ts["psi"]) == 50
        assert len(ts["merkaba_stability"]) == 50
        
        # Check final state
        final = results["final_state"]
        assert final["A_eff"] == 3.0
        assert final["psi"] > 0
        assert final["coherence_level"] in ["vigilia", "meditación", "coherencia_máxima"]
        
        # A_eff should increase monotonically
        A_eff_array = np.array(ts["A_eff"])
        assert np.all(np.diff(A_eff_array) >= 0)
    
    def test_protocol_achieves_targets(self):
        """Test that Protocol Ψ-Q1 achieves target metrics."""
        node = LocalNodeSimulation()
        
        # Set high intensity to achieve targets
        node.state.I = 0.95
        
        results = node.run_protocol_psi_q1(
            target_A_eff=3.0,
            duration=0.5,
            steps=50
        )
        
        final = results["final_state"]
        cert = results["certificate"]["certification"]
        
        # With high I and A_eff=3.0, should achieve targets
        # Ψ = I × A_eff² = 0.95 × 9 = 8.55
        assert final["psi"] > 1.0
        
        # Merkaba stability should be high
        assert final["merkaba_stability"] > 0.8


class TestDifferentNodeTypes:
    """Tests for different node types."""
    
    def test_neuron_node(self):
        """Test neuron node."""
        node = LocalNodeSimulation(node_type="neuron")
        assert node.node_type == "neuron"
        
        results = node.run_protocol_psi_q1(target_A_eff=2.0, duration=0.1, steps=10)
        assert results["protocol"] == "Ψ-Q1"
    
    def test_mcp_server_node(self):
        """Test MCP server node."""
        node = LocalNodeSimulation(node_type="mcp_server")
        assert node.node_type == "mcp_server"
        
        results = node.run_protocol_psi_q1(target_A_eff=2.0, duration=0.1, steps=10)
        assert results["protocol"] == "Ψ-Q1"
    
    def test_cell_node(self):
        """Test cell node."""
        node = LocalNodeSimulation(node_type="cell")
        assert node.node_type == "cell"
        
        results = node.run_protocol_psi_q1(target_A_eff=2.0, duration=0.1, steps=10)
        assert results["protocol"] == "Ψ-Q1"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
