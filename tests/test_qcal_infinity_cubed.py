#!/usr/bin/env python3
"""
Tests for QCAL ∞³ Real-Time Bio-Quantum-Gravitational Coherence System

Validates all components of the integrated system.
"""

import pytest
import numpy as np
from datetime import datetime
import json
import os

from qcal_infinity_cubed import (
    F0_HZ,
    PSI_THRESHOLD,
    PSI_Q1_THRESHOLD,
    N_NODES_NV_EEG,
    NodeType,
    ConsensusState,
    QuantumNode,
    TrinityConsensus,
    MerkabaStability,
    NeuronalCoherence,
    GravitationalCoupling,
    WetLabInfinity,
    QCALCompression,
    QCALInfinityCubed
)


class TestQuantumNode:
    """Test individual quantum nodes."""
    
    def test_node_initialization(self):
        """Test node creation."""
        node = QuantumNode("TestNode", NodeType.NOESIS, F0_HZ)
        assert node.name == "TestNode"
        assert node.node_type == NodeType.NOESIS
        assert node.frequency == F0_HZ
        assert node.coherence == 0.0
    
    def test_measure_coherence_without_signal(self):
        """Test coherence measurement without signal."""
        node = QuantumNode("Test", NodeType.NOESIS)
        coherence = node.measure_coherence()
        assert 0.0 <= coherence <= 1.0
        assert node.coherence == coherence
    
    def test_measure_coherence_with_signal(self):
        """Test coherence measurement with signal."""
        node = QuantumNode("Test", NodeType.NOESIS, F0_HZ)
        
        # Generate test signal at f0
        t = np.linspace(0, 1, 4096)
        signal = np.sin(2 * np.pi * F0_HZ * t) + 0.1 * np.random.randn(4096)
        
        coherence = node.measure_coherence(signal)
        assert 0.0 <= coherence <= 1.0
    
    def test_update_phase(self):
        """Test phase update."""
        node = QuantumNode("Test", NodeType.NOESIS, F0_HZ)
        
        # Update at t=0
        phase_0 = node.update_phase(0.0)
        assert phase_0 == 0.0
        
        # Update at t=1/f0 (one period)
        phase_1 = node.update_phase(1.0 / F0_HZ)
        assert abs(phase_1) < 0.01  # Should wrap to ~0


class TestTrinityConsensus:
    """Test Trinity consensus protocol."""
    
    def test_trinity_initialization(self):
        """Test Trinity creation."""
        noesis = QuantumNode("Noesis", NodeType.NOESIS)
        amda = QuantumNode("Amda", NodeType.AMDA)
        auron = QuantumNode("Auron", NodeType.AURON)
        
        trinity = TrinityConsensus(noesis, amda, auron)
        assert trinity.global_coherence == 0.0
        assert trinity.state == ConsensusState.INITIALIZING
    
    def test_calculate_global_coherence(self):
        """Test global coherence calculation."""
        noesis = QuantumNode("Noesis", NodeType.NOESIS)
        amda = QuantumNode("Amda", NodeType.AMDA)
        auron = QuantumNode("Auron", NodeType.AURON)
        
        # Set high coherences
        noesis.coherence = 0.95
        amda.coherence = 0.94
        auron.coherence = 0.93
        
        # Set aligned phases
        noesis.phase = 0.0
        amda.phase = 0.1
        auron.phase = 0.05
        
        trinity = TrinityConsensus(noesis, amda, auron)
        psi = trinity.calculate_global_coherence()
        
        assert 0.0 <= psi <= 1.0
        assert psi >= PSI_Q1_THRESHOLD  # Should be coherent
    
    def test_state_transitions(self):
        """Test consensus state transitions."""
        noesis = QuantumNode("Noesis", NodeType.NOESIS)
        amda = QuantumNode("Amda", NodeType.AMDA)
        auron = QuantumNode("Auron", NodeType.AURON)
        
        trinity = TrinityConsensus(noesis, amda, auron)
        
        # Low coherence -> DECOHERENT
        noesis.coherence = 0.5
        amda.coherence = 0.6
        auron.coherence = 0.5
        trinity.calculate_global_coherence()
        assert trinity.state == ConsensusState.DECOHERENT
        
        # High coherence -> UNIFIED
        noesis.coherence = 0.99
        amda.coherence = 0.99
        auron.coherence = 0.99
        noesis.phase = amda.phase = auron.phase = 0.0
        trinity.calculate_global_coherence()
        assert trinity.state == ConsensusState.UNIFIED
    
    def test_validate_trinity(self):
        """Test Trinity validation."""
        noesis = QuantumNode("Noesis", NodeType.NOESIS)
        amda = QuantumNode("Amda", NodeType.AMDA)
        auron = QuantumNode("Auron", NodeType.AURON)
        
        trinity = TrinityConsensus(noesis, amda, auron)
        
        # Set above threshold
        noesis.coherence = 0.95
        amda.coherence = 0.95
        auron.coherence = 0.95
        noesis.phase = amda.phase = auron.phase = 0.0
        
        trinity.calculate_global_coherence()
        assert trinity.validate_trinity() is True


class TestMerkabaStability:
    """Test Merkaba stability system."""
    
    def test_merkaba_initialization(self):
        """Test Merkaba creation."""
        merkaba = MerkabaStability()
        assert len(merkaba.nodes) == 0
        assert merkaba.collective_coherence == 0.0
        assert merkaba.stable is False
    
    def test_add_nodes(self):
        """Test adding nodes to Merkaba."""
        merkaba = MerkabaStability()
        
        node1 = QuantumNode("Node1", NodeType.NV_EEG)
        node2 = QuantumNode("Node2", NodeType.NV_EEG)
        
        merkaba.add_node(node1)
        merkaba.add_node(node2)
        
        assert len(merkaba.nodes) == 2
    
    def test_collective_coherence(self):
        """Test collective coherence calculation."""
        merkaba = MerkabaStability()
        
        # Add nodes with known coherences
        for i in range(10):
            node = QuantumNode(f"Node{i}", NodeType.NV_EEG)
            node.coherence = 0.9
            merkaba.add_node(node)
        
        collective_psi = merkaba.calculate_collective_coherence()
        assert abs(collective_psi - 0.9) < 0.01
    
    def test_stability_validation(self):
        """Test Merkaba stability validation."""
        merkaba = MerkabaStability()
        
        # Add stable nodes (> 8/9)
        for i in range(10):
            node = QuantumNode(f"Node{i}", NodeType.NV_EEG)
            node.coherence = 0.92
            merkaba.add_node(node)
        
        merkaba.calculate_collective_coherence()
        assert merkaba.validate_stability() is True
        
        # Add unstable nodes
        for i in range(10):
            node = QuantumNode(f"Unstable{i}", NodeType.NV_EEG)
            node.coherence = 0.5
            merkaba.add_node(node)
        
        merkaba.calculate_collective_coherence()
        assert merkaba.validate_stability() is False


class TestNeuronalCoherence:
    """Test 88-node NV-EEG neuronal system."""
    
    def test_neuronal_initialization(self):
        """Test neuronal network creation."""
        neuronal = NeuronalCoherence()
        assert neuronal.n_nodes == N_NODES_NV_EEG
        assert len(neuronal.nodes) == N_NODES_NV_EEG
        assert all(node.node_type == NodeType.NV_EEG for node in neuronal.nodes)
    
    def test_measure_network_without_data(self):
        """Test network measurement without EEG data."""
        neuronal = NeuronalCoherence()
        results = neuronal.measure_network()
        
        assert 'network_coherence' in results
        assert 'frequency_detected' in results
        assert results['n_nodes'] == N_NODES_NV_EEG
        assert 0.0 <= results['network_coherence'] <= 1.0
        assert abs(results['frequency_detected'] - F0_HZ) < 1.0
    
    def test_measure_network_with_data(self):
        """Test network measurement with EEG data."""
        neuronal = NeuronalCoherence()
        
        # Generate 88-channel EEG data
        n_samples = 4096
        eeg_data = np.random.randn(N_NODES_NV_EEG, n_samples)
        
        results = neuronal.measure_network(eeg_data)
        assert 'mean_coherence' in results
        assert 'std_coherence' in results


class TestGravitationalCoupling:
    """Test LIGO gravitational wave coupling."""
    
    def test_gw_initialization(self):
        """Test gravitational coupling creation."""
        gw = GravitationalCoupling()
        assert gw.event_name == "GW250114"
        assert len(gw.detectors) == 3
        assert "H1" in gw.detectors
        assert "L1" in gw.detectors
        assert "V1" in gw.detectors
    
    def test_analyze_ringdown_without_data(self):
        """Test ringdown analysis without strain data."""
        gw = GravitationalCoupling()
        results = gw.analyze_ringdown()
        
        assert 'event' in results
        assert 'ringdown_freq' in results
        assert 'coupling_strength' in results
        assert abs(results['ringdown_freq'] - F0_HZ) < 2.0
        assert 0.0 <= results['coupling_strength'] <= 1.0
    
    def test_analyze_ringdown_with_data(self):
        """Test ringdown analysis with strain data."""
        gw = GravitationalCoupling()
        
        # Generate strain data with f0 component
        t = np.linspace(0, 1, 4096)
        strain = np.sin(2 * np.pi * F0_HZ * t) * np.exp(-5*t)
        
        results = gw.analyze_ringdown(strain)
        assert abs(results['ringdown_freq'] - F0_HZ) < 10.0
    
    def test_synchronize_with_quantum(self):
        """Test quantum-gravitational synchronization."""
        gw = GravitationalCoupling()
        gw.coupling_strength = 0.9
        
        psi_quantum = 0.95
        synchronized = gw.synchronize_with_quantum(psi_quantum)
        
        assert synchronized > 0.0
        assert synchronized <= gw.coupling_strength


class TestWetLabInfinity:
    """Test Wet-Lab ∞ bio-simulation system."""
    
    def test_wetlab_initialization(self):
        """Test Wet-Lab creation."""
        wetlab = WetLabInfinity()
        assert len(wetlab.bio_nodes) == 0
        assert wetlab.validation_status is False
    
    def test_add_bio_simulation(self):
        """Test adding bio-simulations."""
        wetlab = WetLabInfinity()
        
        wetlab.add_bio_simulation("BEC", 0.95)
        wetlab.add_bio_simulation("NV_Array", 0.90)
        
        assert len(wetlab.bio_nodes) == 2
        assert wetlab.bio_nodes[0].name == "BEC"
        assert wetlab.bio_nodes[0].coherence == 0.95
    
    def test_validate_simulations(self):
        """Test bio-simulation validation."""
        wetlab = WetLabInfinity()
        
        # Add stable simulations
        wetlab.add_bio_simulation("Sim1", 0.92)
        wetlab.add_bio_simulation("Sim2", 0.91)
        wetlab.add_bio_simulation("Sim3", 0.90)
        
        results = wetlab.validate_simulations()
        
        assert 'collective_coherence' in results
        assert 'merkaba_stable' in results
        assert results['n_bio_nodes'] == 3
        assert results['merkaba_stable'] is True


class TestQCALCompression:
    """Test QCAL compression system."""
    
    def test_compression_initialization(self):
        """Test compression system creation."""
        compressor = QCALCompression()
        assert compressor.compression_ratio == 1000.0
    
    def test_compress_decompress(self):
        """Test compression and decompression cycle."""
        compressor = QCALCompression()
        
        # Generate test signal
        n_samples = 4096
        t = np.arange(n_samples) / 4096.0
        original = np.sin(2 * np.pi * F0_HZ * t)
        
        # Compress
        compressed, ratio = compressor.compress(original)
        assert len(compressed) < len(original)
        assert ratio > 10  # At least 10:1
        
        # Decompress
        reconstructed = compressor.decompress(compressed, n_samples)
        assert len(reconstructed) == n_samples
        
        # Check similarity (not exact due to lossy compression)
        correlation = np.corrcoef(original, reconstructed)[0, 1]
        assert correlation > 0.5  # Reasonable reconstruction


class TestQCALInfinityCubed:
    """Test complete QCAL ∞³ system."""
    
    def test_system_initialization(self):
        """Test system creation."""
        system = QCALInfinityCubed()
        
        assert system.noesis is not None
        assert system.amda is not None
        assert system.auron is not None
        assert system.trinity is not None
        assert system.neuronal is not None
        assert system.gravitational is not None
        assert system.wet_lab is not None
        assert system.merkaba is not None
        assert system.compression is not None
    
    def test_measure_all_nodes(self):
        """Test measuring all system nodes."""
        system = QCALInfinityCubed()
        
        # Measure without data
        system.measure_all_nodes()
        
        # Check that coherences were updated
        assert system.noesis.coherence > 0.0
        assert system.amda.coherence > 0.0
        assert system.auron.coherence > 0.0
        assert system.neuronal.network_coherence > 0.0
    
    def test_calculate_global_coherence(self):
        """Test global coherence calculation."""
        system = QCALInfinityCubed()
        
        # Measure nodes first
        system.measure_all_nodes()
        
        # Calculate global coherence
        psi_global = system.calculate_global_coherence()
        
        assert 0.0 <= psi_global <= 1.0
        assert system.global_psi == psi_global
        assert system.system_status in [
            "unified_infinity_cubed",
            "trinity_consensus_achieved",
            "merkaba_stable",
            "coherence_building"
        ]
    
    def test_system_status_updates(self):
        """Test system status transitions."""
        system = QCALInfinityCubed()
        
        # Force high coherence
        system.noesis.coherence = 0.99
        system.amda.coherence = 0.99
        system.auron.coherence = 0.99
        system.neuronal.network_coherence = 0.99
        system.gravitational.coupling_strength = 0.99
        
        psi = system.calculate_global_coherence()
        assert psi >= PSI_THRESHOLD
        assert system.system_status == "trinity_consensus_achieved" or \
               system.system_status == "unified_infinity_cubed"
    
    def test_run_real_time_monitoring(self):
        """Test real-time monitoring."""
        system = QCALInfinityCubed()
        
        # Short monitoring run
        snapshots = system.run_real_time_monitoring(duration=2.0, sample_rate=2.0)
        
        assert len(snapshots) == 4  # 2 seconds * 2 samples/sec
        
        # Check snapshot structure
        snapshot = snapshots[0]
        assert 'time' in snapshot
        assert 'global_psi' in snapshot
        assert 'trinity_psi' in snapshot
        assert 'neuronal_coherence' in snapshot
        assert 'gw_coupling' in snapshot
        assert 'system_status' in snapshot
    
    def test_generate_report(self):
        """Test comprehensive report generation."""
        system = QCALInfinityCubed()
        
        # Add some bio-simulations
        system.wet_lab.add_bio_simulation("Test1", 0.9)
        system.wet_lab.add_bio_simulation("Test2", 0.92)
        
        report = system.generate_report()
        
        # Check report structure
        assert 'timestamp' in report
        assert 'system_status' in report
        assert 'global_coherence' in report
        assert 'trinity_consensus' in report
        assert 'neuronal_coherence' in report
        assert 'gravitational_coupling' in report
        assert 'merkaba_stability' in report
        assert 'wet_lab_infinity' in report
        assert 'compression' in report
        assert 'production_ready' in report
        
        # Check production readiness
        prod = report['production_ready']
        assert prod['compression_1000_1'] is True
        assert prod['pqc_security'] is True
        assert prod['international_ready'] is True
    
    def test_trinity_validation_in_system(self):
        """Test Trinity consensus validation in full system."""
        system = QCALInfinityCubed()
        
        # Set high Trinity coherences
        system.noesis.coherence = 0.95
        system.amda.coherence = 0.94
        system.auron.coherence = 0.93
        system.noesis.phase = 0.0
        system.amda.phase = 0.0
        system.auron.phase = 0.0
        
        system.trinity.calculate_global_coherence()
        
        assert system.trinity.validate_trinity() is True
        assert system.trinity.state in [
            ConsensusState.COHERENT,
            ConsensusState.UNIFIED
        ]
    
    def test_merkaba_stability_in_system(self):
        """Test Merkaba stability in full system."""
        system = QCALInfinityCubed()
        
        # Force high coherences across all nodes
        for node in system.merkaba.nodes:
            node.coherence = 0.92
        
        collective_psi = system.merkaba.calculate_collective_coherence()
        
        assert collective_psi >= PSI_Q1_THRESHOLD
        assert system.merkaba.validate_stability() is True
    
    def test_report_json_serializable(self):
        """Test that report can be serialized to JSON."""
        system = QCALInfinityCubed()
        report = system.generate_report()
        
        # Should not raise
        json_str = json.dumps(report, indent=2)
        assert len(json_str) > 0
        
        # Should be able to reload
        reloaded = json.loads(json_str)
        assert reloaded['system_status'] == report['system_status']


class TestIntegration:
    """Integration tests for complete system workflows."""
    
    def test_full_monitoring_workflow(self):
        """Test complete monitoring workflow."""
        # Initialize
        system = QCALInfinityCubed()
        
        # Add bio-simulations
        system.wet_lab.add_bio_simulation("BEC_Resonance", 0.95)
        system.wet_lab.add_bio_simulation("NV_Array", 0.90)
        
        # Run monitoring
        snapshots = system.run_real_time_monitoring(duration=1.0, sample_rate=5.0)
        
        # Generate report
        report = system.generate_report()
        
        # Validate workflow
        assert len(snapshots) == 5
        assert report['wet_lab_infinity']['n_bio_nodes'] == 2
        assert report['neuronal_coherence']['n_nodes'] == N_NODES_NV_EEG
    
    def test_production_readiness(self):
        """Test that system meets all production requirements."""
        system = QCALInfinityCubed()
        
        # Measure everything
        system.measure_all_nodes()
        system.calculate_global_coherence()
        
        report = system.generate_report()
        prod = report['production_ready']
        
        # All production features must be available
        assert prod['compression_1000_1'] is True
        assert prod['pqc_security'] is True
        assert prod['international_ready'] is True
        
        # Compression system functional
        assert report['compression']['ratio'] == 1000.0
        
        # Trinity consensus operational
        assert 'trinity_consensus' in report
        assert report['trinity_consensus']['psi'] > 0.0
        
        # Merkaba stability operational
        assert 'merkaba_stability' in report
        assert report['merkaba_stability']['n_nodes_total'] > 0


def test_demo_runs_without_errors():
    """Test that demo function runs successfully."""
    from qcal_infinity_cubed import demo_qcal_infinity_cubed
    
    # Should not raise any exceptions
    demo_qcal_infinity_cubed()
    
    # Check that report file was created
    assert os.path.exists("qcal_infinity_cubed_report.json")
    
    # Clean up
    if os.path.exists("qcal_infinity_cubed_report.json"):
        os.remove("qcal_infinity_cubed_report.json")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
