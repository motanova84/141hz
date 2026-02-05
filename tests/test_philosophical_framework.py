#!/usr/bin/env python3
"""
Unit Tests for Philosophical Framework
=======================================

Tests for the five fundamental principles that redefine physical reality
as rhythmic, cyclical phenomena.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import sys
import pytest
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from philosophical_framework import (
    PhilosophicalFramework,
    OscillationState,
    validate_framework
)


class TestOscillationState:
    """Tests for OscillationState dataclass."""
    
    def test_valid_state(self):
        """Test creation of valid oscillation state."""
        state = OscillationState(
            frequency=141.7001,
            amplitude=1.0,
            phase=0.0,
            coherence=1.0
        )
        assert state.frequency == 141.7001
        assert state.amplitude == 1.0
        assert state.coherence == 1.0
    
    def test_negative_frequency_raises_error(self):
        """Test that negative frequency raises ValueError."""
        with pytest.raises(ValueError):
            OscillationState(
                frequency=-10,
                amplitude=1.0,
                phase=0.0
            )
    
    def test_invalid_coherence_raises_error(self):
        """Test that coherence outside [0,1] raises ValueError."""
        with pytest.raises(ValueError):
            OscillationState(
                frequency=141.7001,
                amplitude=1.0,
                phase=0.0,
                coherence=1.5
            )


class TestPrinciple1Mass:
    """Tests for Principle 1: Mass is an illusion of detention."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.framework = PhilosophicalFramework()
    
    def test_mass_from_complete_detention(self):
        """Test that complete frequency detention produces mass."""
        m = self.framework.mass_from_frequency_reduction(0.001)
        assert m > 0
    
    def test_mass_from_no_detention(self):
        """Test that no detention produces zero mass."""
        m = self.framework.mass_from_frequency_reduction(self.framework.f0)
        assert m == 0
    
    def test_mass_increases_with_detention(self):
        """Test that mass increases as frequency decreases."""
        m1 = self.framework.mass_from_frequency_reduction(100.0)
        m2 = self.framework.mass_from_frequency_reduction(50.0)
        assert m2 > m1
    
    def test_mass_oscillation_spectrum_inverse(self):
        """Test that mass_oscillation_spectrum inverts mass calculation."""
        test_mass = 1e-30
        state = self.framework.mass_oscillation_spectrum(test_mass)
        assert state.frequency >= 0
        assert state.frequency <= self.framework.f0


class TestPrinciple2Energy:
    """Tests for Principle 2: Energy is rhythm."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.framework = PhilosophicalFramework()
    
    def test_energy_from_fundamental(self):
        """Test energy calculation at fundamental frequency."""
        E = self.framework.energy_from_rhythm(self.framework.f0)
        assert E > 0
    
    def test_energy_scales_with_harmonic(self):
        """Test that energy scales linearly with harmonic number."""
        E1 = self.framework.energy_from_rhythm(
            self.framework.f0, harmonic_n=1
        )
        E2 = self.framework.energy_from_rhythm(
            self.framework.f0, harmonic_n=2
        )
        assert np.isclose(E2 / E1, 2.0, rtol=1e-10)
    
    def test_energy_scales_with_amplitude_squared(self):
        """Test that energy scales with amplitude squared."""
        E1 = self.framework.energy_from_rhythm(
            self.framework.f0, amplitude=1.0
        )
        E2 = self.framework.energy_from_rhythm(
            self.framework.f0, amplitude=2.0
        )
        assert np.isclose(E2 / E1, 4.0, rtol=1e-10)
    
    def test_rhythm_spectrum_decomposition(self):
        """Test energy decomposition into rhythm spectrum."""
        energy = 1e-30
        spectrum = self.framework.rhythm_spectrum(energy)
        assert spectrum['fundamental_f0'] == self.framework.f0
        assert spectrum['total_energy'] == energy


class TestPrinciple3Space:
    """Tests for Principle 3: Space is an interval between pulses."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.framework = PhilosophicalFramework()
    
    def test_spatial_quantum_positive(self):
        """Test that spatial quantum is positive."""
        lambda_0 = self.framework.spatial_quantum()
        assert lambda_0 > 0
    
    def test_space_from_phase_inverse(self):
        """Test that space and phase conversions are inverses."""
        phase = np.pi
        distance = self.framework.space_from_phase_difference(phase)
        phase_back = self.framework.phase_difference_from_space(distance)
        assert np.isclose(abs(phase_back), phase, rtol=1e-10)
    
    def test_phase_from_space_inverse(self):
        """Test inverse: distance -> phase -> distance."""
        distance = 1000.0  # meters
        phase = self.framework.phase_difference_from_space(distance)
        distance_back = self.framework.space_from_phase_difference(phase)
        assert np.isclose(distance_back, distance, rtol=1e-10)
    
    def test_wavelength_gives_2pi_phase(self):
        """Test that one wavelength corresponds to 2π phase."""
        lambda_0 = self.framework.spatial_quantum()
        phase = self.framework.phase_difference_from_space(lambda_0)
        assert np.isclose(abs(phase), 2 * np.pi, rtol=1e-10)


class TestPrinciple4Time:
    """Tests for Principle 4: Time is the number of cycles."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.framework = PhilosophicalFramework()
    
    def test_temporal_quantum_positive(self):
        """Test that temporal quantum is positive."""
        T_0 = self.framework.temporal_quantum()
        assert T_0 > 0
    
    def test_time_from_cycles_inverse(self):
        """Test that time and cycle conversions are inverses."""
        N = 1000
        t = self.framework.time_from_cycles(N)
        N_back = self.framework.cycles_from_time(t)
        assert np.isclose(N_back, N, rtol=1e-10)
    
    def test_cycles_from_time_inverse(self):
        """Test inverse: time -> cycles -> time."""
        time = 1.0  # second
        cycles = self.framework.cycles_from_time(time)
        time_back = self.framework.time_from_cycles(cycles)
        assert np.isclose(time_back, time, rtol=1e-10)
    
    def test_one_period_is_one_cycle(self):
        """Test that one period corresponds to one cycle."""
        T_0 = self.framework.temporal_quantum()
        cycles = self.framework.cycles_from_time(T_0)
        assert np.isclose(cycles, 1.0, rtol=1e-10)


class TestPrinciple5Symphony:
    """Tests for Principle 5: Universe is a self-contained symphony."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.framework = PhilosophicalFramework()
    
    def test_perfect_harmonics_high_coherence(self):
        """Test that perfect harmonics have high coherence."""
        harmonics = np.array([1, 2, 3, 5]) * self.framework.f0
        coherence = self.framework.universal_coherence(harmonics)
        assert coherence > 0.99
    
    def test_incoherent_low_coherence(self):
        """Test that incoherent frequencies have low coherence."""
        incoherent = np.array([123.45, 234.56, 345.67])
        coherence = self.framework.universal_coherence(incoherent)
        assert coherence < 0.5
    
    def test_harmonic_decomposition_identifies_harmonics(self):
        """Test that harmonic decomposition identifies harmonic numbers."""
        frequencies = np.array([
            1 * self.framework.f0,
            2 * self.framework.f0,
            3 * self.framework.f0
        ])
        decomposition = self.framework.harmonic_decomposition(frequencies)
        
        assert len(decomposition['harmonic_table']) == 3
        for i, h in enumerate(decomposition['harmonic_table']):
            assert h['harmonic_number'] == i + 1
    
    def test_symphony_signature_has_five_principles(self):
        """Test that symphony signature contains five principles."""
        signature = self.framework.symphony_signature()
        assert len(signature['principles']) == 5
        assert signature['fundamental_frequency'] == self.framework.f0


class TestFrameworkValidation:
    """Tests for overall framework validation."""
    
    def test_validate_framework_all_pass(self):
        """Test that validate_framework returns all True."""
        results = validate_framework()
        assert all(results.values())
    
    def test_framework_consistency(self):
        """Test that framework maintains internal consistency."""
        framework = PhilosophicalFramework()
        
        # Temporal and spatial quanta should be consistent
        T_0 = framework.temporal_quantum()
        lambda_0 = framework.spatial_quantum()
        c = framework.c_light
        
        # c = λ / T should hold
        c_calculated = lambda_0 / T_0
        assert np.isclose(c_calculated, c, rtol=1e-6)


def test_framework_demonstration():
    """Test that framework demonstration runs without error."""
    # Just test that we can create and use the framework
    framework = PhilosophicalFramework()
    signature = framework.symphony_signature()
    assert len(signature['principles']) == 5
    
    # Test validation runs
    results = validate_framework()
    assert all(results.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
