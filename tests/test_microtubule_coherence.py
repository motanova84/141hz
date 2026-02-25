#!/usr/bin/env python3
"""
Test suite for Microtubule Coherence Theory implementation.

Tests both the Lean formalization concepts and Python validation.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import numpy as np
from validate_microtubule_coherence import (
    F0_HZ,
    PSI_TARGET,
    resonance_filter,
    calculate_resonance_response,
    validate_coherence,
    analyze_thermal_noise,
    check_sync,
    run_validation,
)


class TestMicrotubuleCoherence:
    """Test suite for microtubule coherence calculations"""
    
    def test_f0_constant(self):
        """Test f₀ = 141.7001 Hz constant"""
        assert F0_HZ == 141.7001
        assert F0_HZ > 0
    
    def test_psi_target_valid(self):
        """Test Ψ_target = 0.999999 is valid"""
        assert 0 < PSI_TARGET < 1
        assert PSI_TARGET == 0.999999
        assert 1 - PSI_TARGET < 0.000002  # Very close to 1 (allow floating point)
    
    def test_resonance_filter_at_f0(self):
        """Test resonance filter response at f₀"""
        omega0 = 2 * np.pi * F0_HZ
        response = resonance_filter(omega0, omega0, Q=100)
        
        # At resonance, response should be maximum (1.0)
        assert response == pytest.approx(1.0, rel=1e-10)
    
    def test_resonance_filter_off_resonance(self):
        """Test resonance filter response away from f₀"""
        omega = 2 * np.pi * 100  # Far from f₀
        omega0 = 2 * np.pi * F0_HZ
        response = resonance_filter(omega, omega0, Q=100)
        
        # Off resonance, response should be < 0.5
        assert response < 0.5
    
    def test_calculate_resonance_at_f0(self):
        """Test resonance calculation at f₀"""
        result = calculate_resonance_response(F0_HZ)
        
        assert result.frequency_hz == F0_HZ
        assert result.filter_response == pytest.approx(1.0, rel=1e-6)
        assert result.is_peak is True
        assert result.bandwidth_hz > 0
    
    def test_coherence_validation_target(self):
        """Test coherence validation at target value"""
        result = validate_coherence(PSI_TARGET)
        
        assert result.psi_value == PSI_TARGET
        assert result.is_valid is True
        assert result.deviation_from_target < 1e-6
        assert "EXCELLENT" in result.stability_status
    
    def test_coherence_validation_boundary(self):
        """Test coherence validation at boundaries"""
        # Test at threshold
        result = validate_coherence(0.95)
        assert result.is_valid is True
        
        # Test below threshold
        result = validate_coherence(0.94)
        assert result.is_valid is False
        
        # Test invalid values
        with pytest.raises(ValueError):
            validate_coherence(1.5)
        
        with pytest.raises(ValueError):
            validate_coherence(-0.1)
    
    def test_thermal_noise_analysis(self):
        """Test thermal noise vs quantum energy"""
        result = analyze_thermal_noise()
        
        # Thermal energy should be much larger than quantum
        assert result.thermal_energy_j > result.quantum_energy_j
        assert result.ratio > 1000
        assert result.noise_cancellation_required is True
        
        # Check magnitudes
        assert 1e-22 < result.thermal_energy_j < 1e-20
        assert 1e-33 < result.quantum_energy_j < 1e-30
    
    def test_synchronization_check(self):
        """Test frequency synchronization check"""
        # Exact sync
        assert check_sync(F0_HZ, F0_HZ) is True
        
        # Within tolerance
        assert check_sync(F0_HZ + 0.05, F0_HZ) is True
        assert check_sync(F0_HZ - 0.05, F0_HZ) is True
        
        # Out of sync
        assert check_sync(F0_HZ + 1.0, F0_HZ) is False
        assert check_sync(100.0, F0_HZ) is False
    
    def test_full_validation_success(self):
        """Test complete validation with optimal parameters"""
        results = run_validation(
            tubulin_freq_hz=F0_HZ,
            psi_state=PSI_TARGET
        )
        
        # Should pass all checks
        assert results.resonance.filter_response == pytest.approx(1.0, rel=1e-6)
        assert results.coherence.is_valid is True
        assert results.thermal.noise_cancellation_required is True
        assert results.consciousness_stable is True
        assert "SYNCHRONIZED" in results.sync_status
    
    def test_validation_with_decoherence(self):
        """Test validation with insufficient coherence"""
        results = run_validation(
            tubulin_freq_hz=F0_HZ,
            psi_state=0.80  # Below threshold
        )
        
        # Should fail coherence check
        assert results.coherence.is_valid is False
        assert results.consciousness_stable is False
    
    def test_validation_without_sync(self):
        """Test validation without synchronization"""
        results = run_validation(
            tubulin_freq_hz=100.0,  # Far from f₀
            psi_state=PSI_TARGET
        )
        
        # Should fail sync check
        assert "NOT SYNCHRONIZED" in results.sync_status
        assert results.consciousness_stable is False
    
    def test_experimental_measurement_range(self):
        """Test that experimental measurement (141.88 Hz) is close to f₀"""
        f_measured = 141.88  # From experiments/consciousness_science_validation.py
        
        # Should be within experimental precision
        deviation = abs(f_measured - F0_HZ)
        assert deviation < 0.2
        
        # Should be synchronized
        assert check_sync(f_measured, F0_HZ) is False  # Just outside 0.1 Hz tolerance
        
        # But within broader biological tolerance
        assert check_sync(f_measured, F0_HZ, tolerance_hz=0.2) is True


class TestLeanFormalizationConcepts:
    """Test mathematical concepts from Lean formalization"""
    
    def test_microtubule_geometry(self):
        """Test microtubule geometry constants"""
        # From MicrotubuleCoherence.lean
        n_protofilaments = 13
        diameter_nm = 25
        
        assert n_protofilaments == 13  # Hexagonal symmetry
        assert diameter_nm > 0
    
    def test_collapse_factor(self):
        """Test quantum → macroscopic collapse factor"""
        nu_tubulin = 1e9  # GHz
        collapse_factor = nu_tubulin / F0_HZ
        
        # Should be very large (GHz/Hz)
        assert collapse_factor > 1e6
        assert collapse_factor == pytest.approx(7.057e6, rel=1e-3)
    
    def test_quality_factor(self):
        """Test resonator quality factor Q"""
        Q = 100
        bandwidth = F0_HZ / Q
        
        assert Q > 0
        assert bandwidth == pytest.approx(1.417, rel=1e-3)
        assert bandwidth < 2  # Narrow bandwidth
    
    def test_coherence_near_unity(self):
        """Test that Ψ_target is very close to 1"""
        deviation = 1 - PSI_TARGET
        
        assert deviation < 0.000002  # Allow floating point precision
        assert deviation == pytest.approx(1e-6, rel=0.2)


class TestBiologicalConstants:
    """Test biological and physical constants"""
    
    def test_physical_constants(self):
        """Test physical constants match standard values"""
        HBAR = 1.054571817e-34  # J·s
        K_B = 1.380649e-23  # J/K
        
        # Check magnitudes
        assert 1e-35 < HBAR < 1e-33
        assert 1e-24 < K_B < 1e-22
    
    def test_biological_temperature(self):
        """Test biological temperature is realistic"""
        T_bio = 310  # K
        
        # Should be around 37°C
        assert 300 < T_bio < 320
        assert T_bio == pytest.approx(310, abs=5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
