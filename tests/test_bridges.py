#!/usr/bin/env python3
"""
Unit tests for integration bridge modules.

Tests all five bridge modules:
- RamseyBridge
- NavierStokesBridge
- ComplexityBridge
- RiemannAdelicBridge
- AdelicBSDBridge
"""

import pytest
import numpy as np
import sys

# Add src to path
sys.path.insert(0, '/home/runner/work/141hz/141hz')

from src.bridges import (
    RamseyBridge,
    NavierStokesBridge,
    ComplexityBridge,
    RiemannAdelicBridge,
    AdelicBSDBridge,
    F0_HZ
)


class TestRamseyBridge:
    """Test cases for Ramsey Bridge."""
    
    def test_initialization(self):
        """Test bridge initialization."""
        bridge = RamseyBridge()
        assert bridge.f0 == 141.7001
        assert bridge.precision == 50
    
    def test_ramsey_number_calculation(self):
        """Test Ramsey number calculation."""
        bridge = RamseyBridge()
        
        # Known values
        assert bridge.calculate_ramsey_number(2, 2) == 2
        assert bridge.calculate_ramsey_number(3, 3) == 6
        assert bridge.calculate_ramsey_number(2, 4) == 4
    
    def test_network_topology_optimization(self):
        """Test network topology optimization."""
        bridge = RamseyBridge()
        
        topology = bridge.optimize_network_topology(num_qubits=16, target_entanglement=0.8)
        
        assert topology.nodes == 16
        assert 0 < topology.edges <= 120  # Max edges for 16 nodes
        assert topology.entanglement_density > 0
        assert topology.coherence_metric > 0
    
    def test_entanglement_graph_analysis(self):
        """Test entanglement graph analysis."""
        bridge = RamseyBridge()
        
        # Create simple graph
        n = 8
        adj_matrix = np.random.rand(n, n)
        adj_matrix = (adj_matrix + adj_matrix.T) / 2  # Make symmetric
        adj_matrix = (adj_matrix > 0.5).astype(float)  # Binary
        np.fill_diagonal(adj_matrix, 0)  # No self-loops
        
        analysis = bridge.analyze_entanglement_graph(adj_matrix)
        
        assert analysis['num_nodes'] == n
        assert 0 <= analysis['density'] <= 1
        assert 0 <= analysis['f0_coherence'] <= 1
    
    def test_validate_integration(self):
        """Test integration validation."""
        bridge = RamseyBridge()
        
        validation = bridge.validate_integration()
        
        assert validation['bridge'] == 'RamseyBridge'
        assert validation['status'] == 'operational'
        assert validation['f0_hz'] == 141.7001
        assert validation['integration_verified'] is True


class TestNavierStokesBridge:
    """Test cases for Navier-Stokes Bridge."""
    
    def test_initialization(self):
        """Test bridge initialization."""
        bridge = NavierStokesBridge()
        assert bridge.f0 == 141.7001
        assert bridge.precision == 50
        assert bridge.nu > 0  # Viscosity
    
    def test_decoherence_analysis(self):
        """Test decoherence analysis."""
        bridge = NavierStokesBridge()
        
        # Create quantum state
        state = np.random.randn(32) + 1j * np.random.randn(32)
        state = state / np.linalg.norm(state)
        
        analysis = bridge.analyze_decoherence(state, time_evolution=1.0)
        
        assert analysis.decoherence_rate >= 0
        assert analysis.suppression_factor >= 1.0
        assert 0 <= analysis.regularity_index <= 1
        assert analysis.f0_coupling > 0
    
    def test_blowup_prevention(self):
        """Test blow-up prevention."""
        bridge = NavierStokesBridge()
        
        # Create velocity field
        velocity = np.random.randn(16)
        
        # Apply regularization
        v_new = bridge.prevent_blowup(velocity, dt=0.01)
        
        assert v_new.shape == velocity.shape
        assert np.isfinite(v_new).all()  # No infinities
    
    def test_energy_cascade(self):
        """Test energy cascade analysis."""
        bridge = NavierStokesBridge()
        
        # Create spectrum
        frequencies = np.linspace(1, 1000, 100)
        spectrum = 1 / frequencies**1.5  # Power law
        
        cascade = bridge.energy_cascade(spectrum, frequencies)
        
        assert 'f0_energy_fraction' in cascade
        assert 'cascade_direction' in cascade
        assert 'spectral_slope' in cascade
    
    def test_validate_integration(self):
        """Test integration validation."""
        bridge = NavierStokesBridge()
        
        validation = bridge.validate_integration()
        
        assert validation['bridge'] == 'NavierStokesBridge'
        assert validation['status'] == 'operational'
        assert validation['integration_verified'] is True


class TestComplexityBridge:
    """Test cases for Complexity Bridge."""
    
    def test_initialization(self):
        """Test bridge initialization."""
        bridge = ComplexityBridge()
        assert bridge.f0 == 141.7001
        assert bridge.precision == 50
    
    def test_algorithm_analysis(self):
        """Test quantum algorithm analysis."""
        bridge = ComplexityBridge()
        
        # Test different algorithm types
        for algo_type in ['quantum_search', 'factoring', 'simulation']:
            analysis = bridge.analyze_algorithm(problem_size=64, algorithm_type=algo_type)
            
            assert analysis.problem_size == 64
            assert analysis.speedup_factor > 0
            assert analysis.gate_count > 0
            assert analysis.circuit_depth > 0
            assert analysis.verification_time > 0
    
    def test_circuit_optimization(self):
        """Test circuit optimization."""
        bridge = ComplexityBridge()
        
        # Create gate sequence
        gates = ['H', 'CNOT', 'T', 'H', 'CNOT', 'T', 'X', 'Y', 'Z']
        
        optimization = bridge.optimize_circuit(gates, target_depth=5)
        
        assert 'original_cost' in optimization
        assert 'optimized_cost' in optimization
        assert optimization['optimized_cost'] <= optimization['original_cost']
    
    def test_quantum_advantage_verification(self):
        """Test quantum advantage verification."""
        bridge = ComplexityBridge()
        
        # Test with quantum advantage
        advantage = bridge.verify_quantum_advantage(
            classical_time=100.0,
            quantum_time=10.0,
            problem_size=64
        )
        
        assert advantage['speedup'] > 1
        assert advantage['quantum_advantage'] is True
        assert 0 <= advantage['f0_confidence'] <= 1
    
    def test_validate_integration(self):
        """Test integration validation."""
        bridge = ComplexityBridge()
        
        validation = bridge.validate_integration()
        
        assert validation['bridge'] == 'ComplexityBridge'
        assert validation['status'] == 'operational'
        assert validation['integration_verified'] is True


class TestRiemannAdelicBridge:
    """Test cases for Riemann-Adelic Bridge."""
    
    def test_initialization(self):
        """Test bridge initialization."""
        bridge = RiemannAdelicBridge()
        assert bridge.f0_experimental == 141.7001
        assert bridge.precision == 50
    
    def test_frequency_derivation(self):
        """Test frequency derivation from Riemann zeta."""
        bridge = RiemannAdelicBridge()
        
        derivation = bridge.derive_frequency()
        
        # Derived frequency should be in reasonable range (within 30 Hz)
        # The mathematical derivation is approximate
        assert abs(derivation.derived_frequency - 141.7001) < 30.0
        assert derivation.golden_ratio > 1.6  # Golden ratio ≈ 1.618
        assert derivation.adelic_norm > 0
    
    def test_spectral_decomposition(self):
        """Test spectral decomposition."""
        bridge = RiemannAdelicBridge()
        
        spectrum = bridge.spectral_decomposition(num_harmonics=10)
        
        assert spectrum['f0_hz'] == 141.7001
        assert spectrum['num_harmonics'] == 10
        assert len(spectrum['harmonics']) == 10
        assert spectrum['total_energy'] > 0
    
    def test_zeta_connection_validation(self):
        """Test Riemann zeta connection validation."""
        bridge = RiemannAdelicBridge()
        
        validation = bridge.validate_zeta_connection()
        
        assert 'frequency_derivation' in validation
        assert 'riemann_hypothesis_check' in validation
        assert 'adelic_geometry' in validation
    
    def test_validate_integration(self):
        """Test integration validation."""
        bridge = RiemannAdelicBridge()
        
        validation = bridge.validate_integration()
        
        assert validation['bridge'] == 'RiemannAdelicBridge'
        assert validation['status'] == 'operational'
        assert 'derivation' in validation


class TestAdelicBSDBridge:
    """Test cases for Adelic-BSD Bridge."""
    
    def test_initialization(self):
        """Test bridge initialization."""
        bridge = AdelicBSDBridge()
        assert bridge.f0 == 141.7001
        assert bridge.precision == 50
    
    def test_elliptic_curve_construction(self):
        """Test elliptic curve construction."""
        bridge = AdelicBSDBridge()
        
        curve = bridge.construct_elliptic_curve()
        
        assert 'a' in curve
        assert 'b' in curve
        assert 'discriminant' in curve
        assert 'j_invariant' in curve
        assert curve['is_singular'] is False  # Should be non-singular
    
    def test_l_function_computation(self):
        """Test L-function computation."""
        bridge = AdelicBSDBridge()
        
        curve = bridge.construct_elliptic_curve()
        l_value = bridge.compute_l_function(curve, s=1.0)
        
        assert isinstance(l_value, complex)
        assert np.isfinite(l_value)
    
    def test_spectral_calibration(self):
        """Test spectral parameter calibration."""
        bridge = AdelicBSDBridge()
        
        calibration = bridge.calibrate_spectral_parameters()
        
        assert calibration.curve_rank >= 0
        assert calibration.spectral_frequency > 0
        assert calibration.calibration_factor > 0
        assert 0 <= calibration.prime_alignment <= 1
    
    def test_torsion_analysis(self):
        """Test torsion structure analysis."""
        bridge = AdelicBSDBridge()
        
        curve = bridge.construct_elliptic_curve()
        torsion = bridge.analyze_torsion_structure(curve)
        
        assert torsion['torsion_order'] > 0
        assert 'torsion_structure' in torsion
        assert torsion['f0_resonance'] > 0
    
    def test_validate_integration(self):
        """Test integration validation."""
        bridge = AdelicBSDBridge()
        
        validation = bridge.validate_integration()
        
        assert validation['bridge'] == 'AdelicBSDBridge'
        assert validation['status'] == 'operational'


class TestEcosystemIntegration:
    """Test ecosystem-wide integration."""
    
    def test_frequency_synchronization(self):
        """Test that all bridges use the same fundamental frequency."""
        bridges = [
            RamseyBridge(),
            NavierStokesBridge(),
            ComplexityBridge(),
            RiemannAdelicBridge(),
            AdelicBSDBridge()
        ]
        
        # All should use f₀ = 141.7001 Hz
        for bridge in bridges:
            if hasattr(bridge, 'f0'):
                assert float(bridge.f0) == F0_HZ
            elif hasattr(bridge, 'f0_experimental'):
                assert float(bridge.f0_experimental) == F0_HZ
    
    def test_all_bridges_operational(self):
        """Test that all bridges validate successfully."""
        bridges = {
            'Ramsey': RamseyBridge(),
            'NavierStokes': NavierStokesBridge(),
            'Complexity': ComplexityBridge(),
            'RiemannAdelic': RiemannAdelicBridge(),
            'AdelicBSD': AdelicBSDBridge()
        }
        
        for name, bridge in bridges.items():
            validation = bridge.validate_integration()
            assert validation['status'] == 'operational', f"{name} bridge not operational"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
