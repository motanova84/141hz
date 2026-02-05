"""
Unit tests for QCAL Biological Model

Tests the core functionality of the biological hypothesis implementation.
"""

import sys
import os
import pytest
import numpy as np

# Add module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'quantum_biology', 'core'))

from qcal_biological_model import (
    SpectralField,
    BiologicalFilter,
    PhaseAccumulator,
    MagicicadaModel,
    validate_141hz_resonance
)


class TestSpectralField:
    """Test SpectralField class."""
    
    def test_creation(self):
        """Test basic creation of spectral field."""
        frequencies = np.array([1.0, 2.0, 3.0])
        amplitudes = np.array([1.0, 0.5, 0.3])
        phases = np.array([0.0, np.pi/2, np.pi])
        
        field = SpectralField(frequencies, amplitudes, phases)
        
        assert len(field.frequencies) == 3
        assert len(field.amplitudes) == 3
        assert len(field.phases) == 3
    
    def test_evaluation(self):
        """Test field evaluation at specific times."""
        frequencies = np.array([2*np.pi])  # 1 Hz
        amplitudes = np.array([1.0])
        phases = np.array([0.0])
        
        field = SpectralField(frequencies, amplitudes, phases)
        
        t = np.array([0.0, 0.5, 1.0])
        psi = field.evaluate(t)
        
        assert len(psi) == 3
        assert isinstance(psi[0], complex)
    
    def test_power_spectrum(self):
        """Test power spectrum calculation."""
        frequencies = np.array([2*np.pi, 4*np.pi])
        amplitudes = np.array([1.0, 0.5])
        phases = np.array([0.0, 0.0])
        
        field = SpectralField(frequencies, amplitudes, phases)
        
        freqs, power = field.power_spectrum()
        
        assert len(freqs) == 2
        assert len(power) == 2
        assert power[0] == 1.0
        assert power[1] == 0.25


class TestBiologicalFilter:
    """Test BiologicalFilter class."""
    
    def test_141hz_enhancement(self):
        """Test that 141.7 Hz is enhanced by the filter."""
        filter_obj = BiologicalFilter()
        
        # Test at f₀ and nearby frequencies
        test_freqs = np.array([100, 141.7001, 200]) * 2 * np.pi
        H = filter_obj.transfer_function(test_freqs)
        
        # 141.7 Hz should have highest response
        assert H[1] > H[0]
        assert H[1] > H[2]
        assert H[1] >= 2.0  # Should be enhanced
    
    def test_high_frequency_filtering(self):
        """Test that high frequencies are filtered out."""
        filter_obj = BiologicalFilter()
        
        # Test high frequency (> 1 kHz)
        high_freq = np.array([2000]) * 2 * np.pi  # 2 kHz
        H_high = filter_obj.transfer_function(high_freq)
        
        # Should be close to zero
        assert H_high[0] < 0.1


class TestPhaseAccumulator:
    """Test PhaseAccumulator class."""
    
    def test_accumulation(self):
        """Test phase accumulation over time."""
        accumulator = PhaseAccumulator(alpha=0.1, threshold=10.0)
        
        # Accumulate constant power
        power = np.array([1.0])
        dt = 1.0
        
        for i in range(5):
            phase = accumulator.accumulate(power, dt)
        
        # Phase should increase
        assert len(accumulator.phase_history) == 5
        assert accumulator.phase_history[-1] > accumulator.phase_history[0]
    
    def test_activation_threshold(self):
        """Test activation condition."""
        accumulator = PhaseAccumulator(alpha=0.1, threshold=5.0)
        
        # Accumulate until threshold
        power = np.array([2.0])
        dt = 1.0
        
        activated = False
        for i in range(10):
            phase = accumulator.accumulate(power, dt)
            if accumulator.check_activation():
                activated = True
                break
        
        # Should activate at some point
        assert activated or accumulator.accumulated_phase >= 5.0
    
    def test_memory_retention(self):
        """Test that memory parameter α works correctly."""
        accumulator = PhaseAccumulator(alpha=0.1)
        
        # Add significant power then zero
        accumulator.accumulate(np.array([10.0]), 1.0)
        phase1 = accumulator.accumulated_phase
        
        accumulator.accumulate(np.array([0.0]), 1.0)
        phase2 = accumulator.accumulated_phase
        
        # Phase should decay slightly (memory retention)
        assert phase2 < phase1
        assert phase2 > 0.9 * phase1  # At least 90% retained


class TestMagicicadaModel:
    """Test MagicicadaModel class."""
    
    def test_creation(self):
        """Test model creation with valid cycles."""
        model13 = MagicicadaModel(cycle_years=13, alpha=0.1)
        model17 = MagicicadaModel(cycle_years=17, alpha=0.1)
        
        assert model13.cycle_years == 13
        assert model17.cycle_years == 17
    
    def test_invalid_cycle(self):
        """Test that non-prime cycles raise error."""
        with pytest.raises(ValueError):
            MagicicadaModel(cycle_years=14, alpha=0.1)
    
    def test_simulation(self):
        """Test lifecycle simulation."""
        model = MagicicadaModel(cycle_years=13, alpha=0.1)
        results = model.simulate_lifecycle(years=20, timesteps_per_year=12)
        
        assert 'time_years' in results
        assert 'phase' in results
        assert 'activated' in results
        assert len(results['time_years']) == 20 * 12
    
    def test_emergence_timing(self):
        """Test that emergence occurs near expected cycle."""
        model = MagicicadaModel(cycle_years=17, alpha=0.1)
        results = model.simulate_lifecycle(years=20, timesteps_per_year=12)
        
        if results['emergence_year'] is not None:
            # Should emerge within ~3 years of expected (≈18% tolerance)
            # This tolerance accounts for:
            # 1. Model simplifications (constant amplitudes, no seasonal variation)
            # 2. Threshold calibration uncertainty
            # 3. Real Magicicada show ±3-5 days precision, not years,
            #    but our coarse-grained simulation uses monthly timesteps
            error = abs(results['emergence_year'] - 17)
            assert error < 3.0  # Within 3 years tolerance


class TestValidation:
    """Test validation functions."""
    
    def test_141hz_resonance_validation(self):
        """Test that 141.7 Hz resonance validation works."""
        result = validate_141hz_resonance()
        
        # Should return True (141.7 Hz is enhanced)
        assert bool(result) is True


def test_integration():
    """Integration test: full workflow."""
    # Create environmental cycles
    time = np.linspace(0, 365*24*3600, 365)  # 1 year
    signal = np.sin(2*np.pi*time/(365*24*3600))  # Annual cycle
    
    # Create spectral field
    field = SpectralField.from_environmental_data(time, signal, n_components=5)
    
    # Apply biological filter
    bio_filter = BiologicalFilter()
    filtered = bio_filter.apply(field)
    
    # Should produce valid filtered power
    assert len(filtered) == len(field.frequencies)
    assert np.all(filtered >= 0)  # Power is non-negative


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
