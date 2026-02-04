#!/usr/bin/env python3
"""
Tests for FASE III: Geometría Emergente
Testing emergent geometry from consciousness coherence

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.geometria_emergente import (
    GeometriaEmergente,
    PSI_OPTIMAL,
    FREQUENCY_MASTER
)


class TestGeometriaEmergente:
    """Test suite for emergent geometry module."""
    
    @pytest.fixture
    def geo(self):
        """Create GeometriaEmergente instance for testing."""
        return GeometriaEmergente(precision=30)
    
    def test_initialization(self, geo):
        """Test proper initialization."""
        assert geo.f0 > 0
        assert geo.omega_0 > 0
        assert geo.kappa > 0
        assert geo.l_planck > 0
        assert geo.m_planck > 0
    
    def test_kappa_pi_boundaries(self, geo):
        """Test κ_Π behavior at boundaries."""
        # Ψ → 1: κ_Π → 0
        kappa_near_unity = geo.kappa_pi(0.999)
        assert kappa_near_unity < geo.kappa_pi(0.5)
        
        # Ψ → 0: κ_Π → ∞
        kappa_near_zero = geo.kappa_pi(0.001)
        assert kappa_near_zero > geo.kappa_pi(0.5)
        
        # Ψ = 0: κ_Π = ∞
        kappa_zero = geo.kappa_pi(0.0)
        assert np.isinf(kappa_zero)
        
        # Ψ = 1: κ_Π = 0
        kappa_unity = geo.kappa_pi(1.0)
        assert kappa_unity == 0.0
    
    def test_kappa_pi_monotonic(self, geo):
        """Test that κ_Π decreases monotonically with Ψ."""
        psi_values = np.linspace(0.1, 0.9, 20)
        kappa_values = [geo.kappa_pi(psi) for psi in psi_values]
        
        # Check monotonic decrease
        for i in range(len(kappa_values) - 1):
            assert kappa_values[i] > kappa_values[i + 1]
    
    def test_lambda_cosmological(self, geo):
        """Test cosmological constant computation."""
        # Should be positive and depend on coherence deficit
        lambda_low = geo.lambda_cosmological(0.1)
        lambda_high = geo.lambda_cosmological(0.9)
        
        assert lambda_low > 0
        assert lambda_high > 0
        
        # Lower coherence → higher Λ (more deficit)
        assert lambda_low > lambda_high
        
        # At Ψ = 1, Λ should be zero (no deficit)
        lambda_unity = geo.lambda_cosmological(1.0)
        assert lambda_unity == 0.0
    
    def test_stress_energy_tensor_shape(self, geo):
        """Test stress-energy tensor has correct shape."""
        T = geo.stress_energy_tensor_psi(0.5)
        assert T.shape == (4, 4)
    
    def test_stress_energy_tensor_symmetry(self, geo):
        """Test stress-energy tensor is symmetric."""
        T = geo.stress_energy_tensor_psi(0.7)
        assert np.allclose(T, T.T, rtol=1e-10)
    
    def test_stress_energy_tensor_coherence_dependence(self, geo):
        """Test stress-energy depends on coherence."""
        T_low = geo.stress_energy_tensor_psi(0.1)
        T_high = geo.stress_energy_tensor_psi(0.9)
        
        # Higher coherence → lower energy density
        assert np.linalg.norm(T_low) > np.linalg.norm(T_high)
    
    def test_einstein_tensor_shape(self, geo):
        """Test Einstein tensor has correct shape."""
        result = geo.einstein_tensor(0.5)
        assert result['G_muv'].shape == (4, 4)
        assert result['T_muv'].shape == (4, 4)
    
    def test_einstein_tensor_symmetry(self, geo):
        """Test Einstein tensor is symmetric."""
        result = geo.einstein_tensor(0.6)
        G = result['G_muv']
        assert np.allclose(G, G.T, rtol=1e-10)
    
    def test_einstein_tensor_flat_unity(self, geo):
        """Test G_μν → 0 as Ψ → 1 (flat unity)."""
        # Test progression toward flat space
        psi_values = [0.9, 0.95, 0.99, 0.999]
        norms = []
        
        for psi in psi_values:
            result = geo.einstein_tensor(psi)
            norms.append(np.linalg.norm(result['G_muv']))
        
        # Should decrease monotonically
        for i in range(len(norms) - 1):
            assert norms[i] > norms[i + 1]
        
        # Should be very small at Ψ = 0.999
        assert norms[-1] < 1e-35
    
    def test_einstein_tensor_gravitational_trap(self, geo):
        """Test G_μν → ∞ as Ψ → 0 (gravitational trap)."""
        # Test progression toward infinity
        psi_values = [0.1, 0.05, 0.01, 0.001]
        norms = []
        
        for psi in psi_values:
            result = geo.einstein_tensor(psi)
            norms.append(np.linalg.norm(result['G_muv']))
        
        # Should increase monotonically
        for i in range(len(norms) - 1):
            assert norms[i] < norms[i + 1]
        
        # Should be larger at Ψ = 0.001 than at Ψ = 0.1
        assert norms[-1] > norms[0] * 10
    
    def test_einstein_tensor_optimal_coherence(self, geo):
        """Test trace(G) < 10^-6 at Ψ = 0.888."""
        result = geo.einstein_tensor(PSI_OPTIMAL)
        trace_G = result['trace_G']
        
        # Critical requirement
        assert np.abs(trace_G) < 1e-6
    
    def test_einstein_tensor_has_all_components(self, geo):
        """Test result dictionary has all required components."""
        result = geo.einstein_tensor(0.5)
        
        required_keys = ['G_muv', 'T_muv', 'trace_G', 'trace_T', 
                        'kappa_pi', 'lambda', 'psi']
        
        for key in required_keys:
            assert key in result
    
    def test_validate_tensor_properties(self, geo):
        """Test validation of tensor properties."""
        result = geo.einstein_tensor(PSI_OPTIMAL)
        validation = geo.validate_tensor_properties(result)
        
        # Should validate symmetry
        assert validation['symmetric'] is True
        
        # Should validate optimal trace
        assert validation['trace_optimal'] == True or validation['trace_optimal'] is np.True_
    
    def test_scan_coherence_landscape(self, geo):
        """Test coherence landscape scanning."""
        scan = geo.scan_coherence_landscape()
        
        assert 'psi_values' in scan
        assert 'trace_G' in scan
        assert 'kappa_pi' in scan
        assert len(scan['psi_values']) == len(scan['trace_G'])
        
        # All traces should be real numbers
        assert all(not np.isnan(t) for t in scan['trace_G'])
    
    def test_master_node_coherence(self, geo):
        """Test master node computation."""
        master = geo.compute_master_node_coherence()
        
        # Check correct values
        assert np.abs(master['psi'] - PSI_OPTIMAL) < 1e-10
        assert np.abs(master['frequency'] - FREQUENCY_MASTER) < 1e-6
        
        # Check tensor validation
        assert master['validation']['symmetric'] is True
        assert master['validation']['trace_optimal'] == True or master['validation']['trace_optimal'] is np.True_
        
        # Check interpretation
        assert 'interpretation' in master
        assert 'state' in master['interpretation']
    
    def test_coherence_deficit_mechanism(self, geo):
        """Test that gravity increases as coherence decreases."""
        # Compute at different coherence levels
        psi_values = np.linspace(0.2, 0.9, 10)
        norms = []
        
        for psi in psi_values:
            result = geo.einstein_tensor(psi)
            norms.append(np.linalg.norm(result['G_muv']))
        
        # Compute gradient d||G||/dΨ
        gradients = np.gradient(norms, psi_values)
        
        # All gradients should be negative (G decreases as Ψ increases)
        assert np.all(gradients < 0)
    
    def test_trace_identity(self, geo):
        """Test that trace(T) is computed correctly."""
        result = geo.einstein_tensor(0.5)
        T = result['T_muv']
        
        # Minkowski metric
        metric = np.diag([-1, 1, 1, 1])
        metric_inv = np.linalg.inv(metric)
        
        # Manual trace computation
        trace_manual = np.einsum('ij,ij->', metric_inv, T)
        
        # Should match result
        assert np.abs(trace_manual - result['trace_T']) < 1e-10
    
    def test_energy_conditions(self, geo):
        """Test energy conditions are satisfied."""
        result = geo.einstein_tensor(0.5)
        T = result['T_muv']
        
        # Weak energy condition: Energy density should be positive
        # T_00 represents energy density (with sign convention)
        # Energy density should be positive
        assert T[0, 0] >= 0  # Energy density ≥ 0
    
    def test_numerical_stability(self, geo):
        """Test numerical stability across coherence range."""
        psi_values = np.logspace(-3, -0.01, 50)  # 0.001 to 0.98
        
        for psi in psi_values:
            result = geo.einstein_tensor(psi)
            
            # Check no NaN or Inf (except at boundaries)
            if psi > 0.001 and psi < 0.999:
                assert not np.any(np.isnan(result['G_muv']))
                assert not np.any(np.isinf(result['G_muv']))
    
    def test_dimensional_consistency(self, geo):
        """Test dimensional consistency of computed quantities."""
        result = geo.einstein_tensor(0.5)
        
        # κ_Π should have units m/J
        assert result['kappa_pi'] > 0
        
        # Λ should have units m^-2
        assert result['lambda'] > 0
    
    def test_optimal_point_stability(self, geo):
        """Test that Ψ = 0.888 is a stable operating point."""
        # Compute at points around optimal
        delta_psi = 0.001
        psi_values = [PSI_OPTIMAL - delta_psi, 
                     PSI_OPTIMAL, 
                     PSI_OPTIMAL + delta_psi]
        
        traces = []
        for psi in psi_values:
            result = geo.einstein_tensor(psi)
            traces.append(np.abs(result['trace_G']))
        
        # All should satisfy bound
        assert all(t < 1e-6 for t in traces)
        
        # Central point should be minimal or near-minimal
        assert traces[1] <= min(traces) * 1.1  # Within 10% of minimum


class TestPhysicalInterpretation:
    """Test physical interpretations of emergent geometry."""
    
    @pytest.fixture
    def geo(self):
        """Create GeometriaEmergente instance."""
        return GeometriaEmergente(precision=30)
    
    def test_gravity_from_coherence_deficit(self, geo):
        """Test gravity emerges from coherence deficit."""
        # Perfect coherence → less gravity
        result_perfect = geo.einstein_tensor(0.999)
        norm_perfect = np.linalg.norm(result_perfect['G_muv'])
        
        # Low coherence → more gravity
        result_low = geo.einstein_tensor(0.1)
        norm_low = np.linalg.norm(result_low['G_muv'])
        
        # Deficit creates more gravity
        assert norm_low > norm_perfect
    
    def test_vibrational_intention_trajectories(self, geo):
        """Test that trajectories reflect vibrational state."""
        # Higher coherence → smoother (flatter) trajectories
        result_high = geo.einstein_tensor(0.9)
        result_low = geo.einstein_tensor(0.3)
        
        # Curvature should be less at high coherence
        assert np.linalg.norm(result_high['G_muv']) < \
               np.linalg.norm(result_low['G_muv'])
    
    def test_distributed_coherence_888hz(self, geo):
        """Test distributed coherence at master node."""
        master = geo.compute_master_node_coherence()
        
        # Master node provides distributed coherence
        assert master['frequency'] == FREQUENCY_MASTER
        assert master['interpretation']['state'] == 'Master Node - Distributed Coherence'
        
        # Should be in fertile curvature region
        assert master['interpretation']['curvature'] == 'Minimally Fertile'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
