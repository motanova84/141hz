#!/usr/bin/env python3
"""
Tests for NV-EEG Quantum-Biological Measurement System

Validates:
- NV center state measurements
- EEG gamma synchrony filtering
- Dynamic Decoupling sequences
- Measurement tensor calculation
- 88-node network coordination
- Statistical validation
"""

import pytest
import numpy as np
from nv_eeg_measurement import (
    NVEEGNode, NVEEGNetwork, DDSequence,
    NVCenterState, EEGState, MeasurementTensor,
    F0_HZ, ODMR_CONTRAST_TARGET, C_INFINITY,
    GAMMA_BAND_MIN_HZ, GAMMA_BAND_MAX_HZ,
    PSI_TARGET, P_VALUE_TARGET, SNR_IMPROVEMENT_FACTOR
)


class TestNVCenterState:
    """Test NV center state validation"""
    
    def test_valid_state(self):
        """Test creating valid NV center state"""
        state = NVCenterState(
            odmr_contrast=0.35,
            magnetic_field_nt=13.0,
            spin_coherence=0.95,
            t1_time_ms=1.0
        )
        assert state.odmr_contrast == 0.35
        assert state.magnetic_field_nt == 13.0
        assert state.spin_coherence == 0.95
        assert state.t1_time_ms == 1.0
    
    def test_invalid_odmr_contrast(self):
        """Test that invalid ODMR contrast raises error"""
        with pytest.raises(ValueError, match="ODMR contrast must be in"):
            NVCenterState(
                odmr_contrast=1.5,  # Invalid: > 1
                magnetic_field_nt=13.0,
                spin_coherence=0.95,
                t1_time_ms=1.0
            )
    
    def test_invalid_coherence(self):
        """Test that invalid coherence raises error"""
        with pytest.raises(ValueError, match="Spin coherence must be in"):
            NVCenterState(
                odmr_contrast=0.35,
                magnetic_field_nt=13.0,
                spin_coherence=-0.1,  # Invalid: < 0
                t1_time_ms=1.0
            )
    
    def test_negative_t1(self):
        """Test that negative T1 raises error"""
        with pytest.raises(ValueError, match="T1 time must be positive"):
            NVCenterState(
                odmr_contrast=0.35,
                magnetic_field_nt=13.0,
                spin_coherence=0.95,
                t1_time_ms=-0.5  # Invalid: negative
            )


class TestEEGState:
    """Test EEG state validation"""
    
    def test_valid_state(self):
        """Test creating valid EEG state"""
        state = EEGState(
            gamma_amplitude_uv=50.0,
            gamma_power=0.8,
            coherence_with_neighbors=0.9
        )
        assert state.gamma_amplitude_uv == 50.0
        assert state.gamma_power == 0.8
        assert state.coherence_with_neighbors == 0.9
    
    def test_invalid_gamma_power(self):
        """Test that invalid gamma power raises error"""
        with pytest.raises(ValueError, match="Gamma power must be in"):
            EEGState(
                gamma_amplitude_uv=50.0,
                gamma_power=1.5,  # Invalid: > 1
                coherence_with_neighbors=0.9
            )
    
    def test_invalid_coherence(self):
        """Test that invalid coherence raises error"""
        with pytest.raises(ValueError, match="Coherence must be in"):
            EEGState(
                gamma_amplitude_uv=50.0,
                gamma_power=0.8,
                coherence_with_neighbors=1.2  # Invalid: > 1
            )


class TestMeasurementTensor:
    """Test measurement tensor validation and calculation"""
    
    def test_valid_tensor(self):
        """Test creating valid measurement tensor"""
        I_NV = 1.0
        A_eff = 0.8
        C_inf = C_INFINITY
        psi = I_NV * (A_eff ** 2) * C_inf
        
        tensor = MeasurementTensor(
            I_NV=I_NV,
            A_eff=A_eff,
            C_inf=C_inf,
            psi_measured=psi
        )
        
        assert tensor.I_NV == I_NV
        assert tensor.A_eff == A_eff
        assert tensor.C_inf == C_inf
        assert abs(tensor.psi_measured - psi) < 1e-10
    
    def test_negative_intensity(self):
        """Test that negative intensity raises error"""
        with pytest.raises(ValueError, match="Intensity and amplitude must be non-negative"):
            MeasurementTensor(
                I_NV=-0.5,  # Invalid: negative
                A_eff=0.8,
                C_inf=C_INFINITY,
                psi_measured=1.0
            )
    
    def test_calculation_mismatch(self):
        """Test that incorrect Ψ calculation raises error"""
        with pytest.raises(ValueError, match="Ψ mismatch"):
            MeasurementTensor(
                I_NV=1.0,
                A_eff=0.8,
                C_inf=C_INFINITY,
                psi_measured=999.0  # Wrong value
            )


class TestNVEEGNode:
    """Test single NV-EEG node functionality"""
    
    def test_node_initialization(self):
        """Test node initialization"""
        node = NVEEGNode(node_id=0)
        assert node.node_id == 0
        assert node.dd_sequence == DDSequence.XY8
        assert node.nv_state is None
        assert node.eeg_state is None
    
    def test_invalid_node_id(self):
        """Test that invalid node ID raises error"""
        with pytest.raises(ValueError, match="Node ID must be in"):
            NVEEGNode(node_id=100)  # Invalid: >= 88
    
    def test_dynamic_decoupling_xy8(self):
        """Test XY8 dynamic decoupling sequence"""
        node = NVEEGNode(node_id=0, dd_sequence=DDSequence.XY8)
        t1_extended = node.apply_dynamic_decoupling(coherence_time_initial_ms=1.0)
        
        assert t1_extended > 1.0  # Should extend T1
        assert node.snr_improvement == SNR_IMPROVEMENT_FACTOR
        assert node.noise_level_nt_sqrthz < 50.0  # Should reduce noise
    
    def test_dynamic_decoupling_kdd(self):
        """Test KDD dynamic decoupling sequence"""
        node = NVEEGNode(node_id=0, dd_sequence=DDSequence.KDD)
        t1_extended = node.apply_dynamic_decoupling(coherence_time_initial_ms=1.0)
        
        assert t1_extended > 1.0  # Should extend T1
        assert node.snr_improvement > SNR_IMPROVEMENT_FACTOR  # KDD better than XY8
    
    def test_dynamic_decoupling_none(self):
        """Test no dynamic decoupling"""
        node = NVEEGNode(node_id=0, dd_sequence=DDSequence.NONE)
        t1_extended = node.apply_dynamic_decoupling(coherence_time_initial_ms=1.0)
        
        assert t1_extended == 1.0  # No extension
        assert node.snr_improvement == 1.0  # No improvement
    
    def test_gamma_synchrony_filtering(self):
        """Test gamma band filtering (40-45 Hz)"""
        node = NVEEGNode(node_id=0, sampling_rate_hz=4096.0)
        
        # Create signal with gamma component
        t = np.linspace(0, 1, 4096)
        gamma_signal = np.sin(2 * np.pi * 42.5 * t)  # 42.5 Hz (in gamma band)
        noise = np.random.normal(0, 0.1, len(t))
        eeg_data = gamma_signal + noise
        
        gamma_power, _ = node.filter_gamma_synchrony(eeg_data)
        
        assert gamma_power > 0  # Should detect gamma power
        assert isinstance(gamma_power, float)
    
    def test_nv_center_measurement(self):
        """Test NV center measurement"""
        node = NVEEGNode(node_id=0)
        nv_state = node.measure_nv_center()
        
        assert 0 <= nv_state.odmr_contrast <= 1
        assert nv_state.magnetic_field_nt >= 0
        assert 0 <= nv_state.spin_coherence <= 1
        assert nv_state.t1_time_ms > 0
    
    def test_eeg_measurement(self):
        """Test EEG measurement"""
        node = NVEEGNode(node_id=0, sampling_rate_hz=4096.0)
        
        # Create test EEG data
        t = np.linspace(0, 1, 4096)
        eeg_data = np.sin(2 * np.pi * 42.5 * t) + np.random.normal(0, 0.1, len(t))
        
        eeg_state = node.measure_eeg(eeg_data)
        
        assert eeg_state.gamma_amplitude_uv > 0
        assert 0 <= eeg_state.gamma_power <= 1
        assert 0 <= eeg_state.coherence_with_neighbors <= 1
    
    def test_measurement_tensor_calculation(self):
        """Test full measurement tensor calculation"""
        node = NVEEGNode(node_id=0, sampling_rate_hz=4096.0)
        
        # Generate test data
        t = np.linspace(0, 1, 4096)
        eeg_data = np.sin(2 * np.pi * 42.5 * t) + np.random.normal(0, 0.1, len(t))
        
        # Perform measurements
        node.measure_nv_center()
        node.measure_eeg(eeg_data)
        tensor = node.calculate_measurement_tensor()
        
        assert tensor.I_NV > 0
        assert tensor.A_eff > 0
        assert tensor.C_inf == C_INFINITY
        assert tensor.psi_measured > 0
        
        # Verify calculation
        expected_psi = tensor.I_NV * (tensor.A_eff ** 2) * tensor.C_inf
        assert abs(tensor.psi_measured - expected_psi) < 1e-10
    
    def test_full_measurement_cycle(self):
        """Test complete measurement cycle"""
        node = NVEEGNode(node_id=5, sampling_rate_hz=4096.0)
        
        # Generate coherent signal at f₀
        t = np.linspace(0, 1, 4096)
        signal_f0 = np.sin(2 * np.pi * F0_HZ * t)
        gamma_signal = 0.5 * np.sin(2 * np.pi * 42.5 * t)
        eeg_data = signal_f0 + gamma_signal + np.random.normal(0, 0.1, len(t))
        
        results = node.full_measurement_cycle(eeg_data)
        
        # Validate results structure
        assert results['node_id'] == 5
        assert 'nv_state' in results
        assert 'eeg_state' in results
        assert 'measurement_tensor' in results
        assert results['dd_sequence'] == 'xy8'
        
        # Validate NV state
        assert 0 <= results['nv_state']['odmr_contrast'] <= 1
        assert results['nv_state']['t1_time_ms'] > 0
        
        # Validate EEG state
        assert results['eeg_state']['gamma_power'] > 0
        
        # Validate measurement tensor
        assert results['measurement_tensor']['C_inf'] == C_INFINITY
        assert results['measurement_tensor']['psi_measured'] > 0


class TestNVEEGNetwork:
    """Test 88-node network functionality"""
    
    def test_network_initialization(self):
        """Test network initialization"""
        network = NVEEGNetwork(num_nodes=88)
        assert len(network.nodes) == 88
        assert all(node.node_id == i for i, node in enumerate(network.nodes))
    
    def test_custom_num_nodes(self):
        """Test network with custom number of nodes"""
        network = NVEEGNetwork(num_nodes=10)
        assert len(network.nodes) == 10
    
    def test_network_synchronization(self):
        """Test network synchronization"""
        network = NVEEGNetwork(num_nodes=88)
        # Should not raise error
        network.synchronize_network(t_sync_seconds=1.0)
    
    def test_network_measurement(self):
        """Test network-wide measurement"""
        network = NVEEGNetwork(num_nodes=10, dd_sequence=DDSequence.XY8)
        
        # Generate coherent EEG data for all nodes
        t = np.linspace(0, 1, 4096)
        eeg_data = np.zeros((10, len(t)))
        
        for i in range(10):
            signal_f0 = np.sin(2 * np.pi * F0_HZ * t)
            gamma_signal = 0.5 * np.sin(2 * np.pi * 42.5 * t)
            noise = np.random.normal(0, 0.1, len(t))
            eeg_data[i] = signal_f0 + gamma_signal + noise
        
        results = network.measure_network(eeg_data)
        
        # Validate results
        assert results['num_nodes'] == 10
        assert 0 <= results['global_psi'] <= 10  # Reasonable range
        assert 0 <= results['network_coherence'] <= 1
        assert results['p_value'] > 0
        assert len(results['node_results']) == 10
        
        # Check target flags
        assert 'targets_achieved' in results
        assert 'psi_target' in results['targets_achieved']
        assert 'p_value_target' in results['targets_achieved']
        assert 'snr_target' in results['targets_achieved']
    
    def test_network_measurement_wrong_shape(self):
        """Test that wrong EEG data shape raises error"""
        network = NVEEGNetwork(num_nodes=88)
        
        # Wrong number of channels
        eeg_data = np.random.randn(50, 4096)  # Only 50 channels, need 88
        
        with pytest.raises(ValueError, match="Expected 88 EEG channels"):
            network.measure_network(eeg_data)
    
    def test_high_coherence_network(self):
        """Test network with highly coherent signals"""
        network = NVEEGNetwork(num_nodes=20, dd_sequence=DDSequence.XY8)
        
        # Generate highly coherent EEG data
        t = np.linspace(0, 1, 4096)
        base_signal = np.sin(2 * np.pi * F0_HZ * t) + 0.5 * np.sin(2 * np.pi * 42.5 * t)
        
        eeg_data = np.zeros((20, len(t)))
        for i in range(20):
            # Very small noise and phase variation → high coherence
            phase = 2 * np.pi * i / 20
            noise = np.random.normal(0, 0.01, len(t))
            eeg_data[i] = base_signal + 0.05 * np.sin(2 * np.pi * F0_HZ * t + phase) + noise
        
        results = network.measure_network(eeg_data)
        
        # Should have high coherence
        assert results['network_coherence'] > 0.7  # High coherence expected
        assert results['p_value'] < 1e-5  # Significant


class TestConstants:
    """Test that constants are properly defined"""
    
    def test_f0_value(self):
        """Test fundamental frequency"""
        assert F0_HZ == 141.7001
    
    def test_odmr_contrast_target(self):
        """Test ODMR contrast target"""
        assert ODMR_CONTRAST_TARGET == 0.35
    
    def test_c_infinity(self):
        """Test fractal expansion factor"""
        assert abs(C_INFINITY - 1.987) < 0.001
    
    def test_gamma_band_range(self):
        """Test gamma band frequency range"""
        assert GAMMA_BAND_MIN_HZ == 40.0
        assert GAMMA_BAND_MAX_HZ == 45.0
    
    def test_psi_target(self):
        """Test Ψ measurement target"""
        assert PSI_TARGET == 0.999
    
    def test_p_value_target(self):
        """Test statistical significance target"""
        assert P_VALUE_TARGET == 1.5e-10
    
    def test_snr_improvement(self):
        """Test SNR improvement factor"""
        assert SNR_IMPROVEMENT_FACTOR == 3.85


class TestIntegration:
    """Integration tests for complete system"""
    
    def test_full_88_node_experiment(self):
        """Test complete 88-node experiment"""
        # Create full 88-node network
        network = NVEEGNetwork(num_nodes=88, dd_sequence=DDSequence.XY8)
        
        # Generate coherent data
        t = np.linspace(0, 1, 4096)
        eeg_data = np.zeros((88, len(t)))
        
        for i in range(88):
            signal_f0 = np.sin(2 * np.pi * F0_HZ * t)
            gamma = 0.5 * np.sin(2 * np.pi * 42.5 * t)
            noise = np.random.normal(0, 0.1, len(t))
            phase = 2 * np.pi * i / 88
            
            eeg_data[i] = (signal_f0 + gamma + noise +
                          0.1 * np.sin(2 * np.pi * F0_HZ * t + phase))
        
        # Measure
        results = network.measure_network(eeg_data)
        
        # Basic validation
        assert results['num_nodes'] == 88
        assert results['global_psi'] > 0
        assert 0 <= results['network_coherence'] <= 1
        
        # All nodes should have results
        assert len(results['node_results']) == 88
        
        # Each node should have valid measurements
        for node_result in results['node_results']:
            assert 'measurement_tensor' in node_result
            assert node_result['measurement_tensor']['psi_measured'] > 0
    
    def test_different_dd_sequences(self):
        """Test network with different DD sequences"""
        for dd_seq in [DDSequence.NONE, DDSequence.XY8, DDSequence.KDD]:
            network = NVEEGNetwork(num_nodes=10, dd_sequence=dd_seq)
            
            # Generate data
            t = np.linspace(0, 1, 4096)
            eeg_data = np.zeros((10, len(t)))
            
            for i in range(10):
                eeg_data[i] = (np.sin(2 * np.pi * F0_HZ * t) +
                              0.5 * np.sin(2 * np.pi * 42.5 * t) +
                              np.random.normal(0, 0.1, len(t)))
            
            results = network.measure_network(eeg_data)
            
            # Should work with all DD sequences
            assert results['num_nodes'] == 10
            assert results['global_psi'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
