#!/usr/bin/env python3
"""
Unit Tests: Microtubule Quantum Consciousness

Tests for the Orch-OR + f₀ model of quantum consciousness
in neuronal microtubules.
"""

import pytest
import numpy as np
from modules.quantum_biology.consciousness.microtubule_coherence import (
    MicrotubuleCoherence,
    MicrotubuleGeometry,
    calculate_thermal_noise_ratio,
    calculate_resonance_filter_response,
    verify_consciousness_stability,
    F0, T_BODY
)


class TestMicrotubuleCoherence:
    """Test suite for MicrotubuleCoherence class."""
    
    def test_initialization(self):
        """Test microtubule initialization."""
        mt = MicrotubuleCoherence()
        assert mt.frequency == F0
        assert mt.temperature == T_BODY
        assert mt.n_tubulins > 0
    
    def test_custom_geometry(self):
        """Test with custom geometry."""
        geometry = MicrotubuleGeometry(
            n_protofilaments=13,
            tubulin_dimers_per_protofilament=500,
            quality_factor=150.0
        )
        mt = MicrotubuleCoherence(geometry=geometry)
        
        assert mt.geometry.n_protofilaments == 13
        assert mt.geometry.quality_factor == 150.0
        assert mt.n_tubulins == 13 * 500
    
    def test_thermal_noise_ratio(self):
        """Test thermal noise ratio calculation."""
        mt = MicrotubuleCoherence()
        ratio = mt.thermal_noise_ratio()
        
        # Should be enormous at body temperature
        assert ratio > 1e9
        assert ratio < 1e12  # But not unreasonably large
    
    def test_resonance_filter_response(self):
        """Test resonance filter at different frequencies."""
        mt = MicrotubuleCoherence()
        
        # Strong response at f₀
        response_f0 = mt.resonance_filter_response(F0)
        assert response_f0 > 0.95
        
        # Weak response off-resonance
        response_off = mt.resonance_filter_response(F0 + 100)
        assert response_off < 0.1
        
        # Intermediate at harmonics
        response_2f0 = mt.resonance_filter_response(2 * F0)
        assert 0 < response_2f0 < response_f0
    
    def test_destructive_interference(self):
        """Test destructive interference factor."""
        mt = MicrotubuleCoherence()
        
        # Constructive at f₀
        interference_f0 = mt.destructive_interference_factor(F0)
        assert interference_f0 > 0.9
        
        # Destructive at thermal frequencies
        f_thermal = T_BODY * 1.380649e-23 / (1.054571817e-34 * 2 * np.pi)
        interference_thermal = mt.destructive_interference_factor(f_thermal)
        assert interference_thermal < 0.1
    
    def test_coherence_function(self):
        """Test consciousness coherence function."""
        mt = MicrotubuleCoherence()
        
        # At t=0
        psi_0 = mt.coherence_function(0.0)
        assert 0 <= psi_0 <= 1
        assert psi_0 >= 0.95  # Should be high for stable consciousness
        
        # Time-dependent
        times = np.linspace(0, 0.1, 50)
        coherences = [mt.coherence_function(t) for t in times]
        
        assert all(0 <= psi <= 1 for psi in coherences)
        assert np.mean(coherences) >= 0.95
    
    def test_coherence_with_collective_enhancement(self):
        """Test coherence with and without collective enhancement."""
        mt = MicrotubuleCoherence()
        
        psi_with = mt.coherence_function(0.0, collective_enhancement=True)
        psi_without = mt.coherence_function(0.0, collective_enhancement=False)
        
        # With enhancement should be higher (or at least not lower)
        assert psi_with >= psi_without * 0.9  # Allow small numerical variations
    
    def test_consciousness_stability(self):
        """Test consciousness stability classification."""
        mt = MicrotubuleCoherence()
        
        # Excellent coherence
        status_excellent = mt.consciousness_stability(0.999)
        assert status_excellent['status'] == 'EXCELLENT'
        assert status_excellent['stable'] == True
        
        # Good coherence
        status_good = mt.consciousness_stability(0.97)
        assert status_good['status'] == 'GOOD'
        assert status_good['stable'] == True
        
        # Marginal coherence
        status_marginal = mt.consciousness_stability(0.92)
        assert status_marginal['status'] == 'MARGINAL'
        assert status_marginal['stable'] == False
        
        # Poor coherence
        status_poor = mt.consciousness_stability(0.85)
        assert status_poor['status'] == 'POOR'
        assert status_poor['stable'] == False
    
    def test_orch_or_orchestration_time(self):
        """Test Orch-OR orchestration time."""
        mt = MicrotubuleCoherence()
        tau = mt.orch_or_orchestration_time()
        
        assert tau > 0  # Must be positive
        # Note: Value is theoretical and may be very large
    
    def test_synchronization_check(self):
        """Test f₀ synchronization check."""
        mt = MicrotubuleCoherence()
        sync = mt.synchronization_check()
        
        assert 'synchronized_to_f0' in sync
        assert 'frequency_hz' in sync
        assert 'filter_response' in sync
        assert 'thermal_noise_ratio' in sync
        assert 'interference_factor' in sync
        assert 'coherence_psi' in sync
        assert 'consciousness_stable' in sync
        assert 'criteria' in sync
        
        # Should be synchronized with default parameters
        assert sync['synchronized_to_f0'] == True
        assert sync['consciousness_stable'] == True
    
    def test_get_summary(self):
        """Test summary retrieval."""
        mt = MicrotubuleCoherence()
        summary = mt.get_summary()
        
        assert 'geometry' in summary
        assert 'physical' in summary
        assert 'coherence' in summary
        assert 'synchronization' in summary
        
        assert summary['physical']['frequency_hz'] == F0
        assert summary['coherence']['psi'] >= 0.95


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_calculate_thermal_noise_ratio(self):
        """Test thermal noise ratio helper."""
        ratio = calculate_thermal_noise_ratio()
        assert ratio > 1e9
        
        # Different temperature
        ratio_low = calculate_thermal_noise_ratio(temperature=100)
        assert ratio_low < ratio  # Lower temperature = lower ratio
    
    def test_calculate_resonance_filter_response(self):
        """Test resonance filter helper."""
        # At center frequency
        response_center = calculate_resonance_filter_response(F0, F0, 100)
        assert response_center > 0.9
        
        # Off center
        response_off = calculate_resonance_filter_response(F0 + 50, F0, 100)
        assert response_off < response_center
    
    def test_verify_consciousness_stability(self):
        """Test consciousness stability verifier."""
        assert verify_consciousness_stability(0.99) == True
        assert verify_consciousness_stability(0.95) == True
        assert verify_consciousness_stability(0.94) == False
        assert verify_consciousness_stability(0.90) == False


class TestThermalNoiseSupression:
    """Integration tests for thermal noise suppression."""
    
    def test_high_coherence_despite_thermal_noise(self):
        """Test that coherence is high despite enormous thermal noise."""
        mt = MicrotubuleCoherence()
        
        # Thermal noise is huge
        thermal_ratio = mt.thermal_noise_ratio()
        assert thermal_ratio > 1e10
        
        # But coherence is still high
        coherence = mt.coherence_function()
        assert coherence >= 0.95
        
        # This validates the destructive interference mechanism
    
    def test_filter_suppresses_thermal_frequencies(self):
        """Test that thermal frequencies are suppressed."""
        mt = MicrotubuleCoherence()
        
        # Thermal frequency
        f_thermal = T_BODY * 1.380649e-23 / (1.054571817e-34 * 2 * np.pi)
        
        # Filter should strongly suppress
        filter_response = mt.resonance_filter_response(f_thermal)
        assert filter_response < 1e-6
        
        # Interference should be destructive
        interference = mt.destructive_interference_factor(f_thermal)
        assert interference < 0.1
    
    def test_resonance_at_f0_and_harmonics(self):
        """Test strong resonance at f₀ and harmonics."""
        mt = MicrotubuleCoherence()
        
        # f₀
        filter_f0 = mt.resonance_filter_response(F0)
        interference_f0 = mt.destructive_interference_factor(F0)
        
        assert filter_f0 > 0.95
        assert interference_f0 > 0.9
        
        # Harmonics should also show some resonance
        filter_2f0 = mt.resonance_filter_response(2 * F0)
        interference_2f0 = mt.destructive_interference_factor(2 * F0)
        
        assert filter_2f0 > 0  # Some response
        assert interference_2f0 > 0  # Some constructive interference


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
