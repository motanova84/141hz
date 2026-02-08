#!/usr/bin/env python3
"""
Tests for QCAL ∞³ Cosmic Parameters Module

Tests the cosmological constants and timeline integration.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qcal.cosmic_parameters import (
    CurrentUniverseParameters,
    CosmicEpoch,
    CosmicTimeline,
    CURRENT_UNIVERSE,
    COSMIC_TIMELINE,
    get_universe_age,
    get_cmb_temperature,
    get_epoch,
)
from qcal.constants import F0_HZ


class TestCurrentUniverseParameters:
    """Test current universe observational parameters."""
    
    def test_universe_age(self):
        """Test universe age is correctly defined."""
        universe = CurrentUniverseParameters()
        assert universe.age_years == 13.8e9
        assert universe.age_seconds > 0
        
        # Check conversion
        expected_seconds = 13.8e9 * 365.25 * 24 * 3600
        assert abs(universe.age_seconds - expected_seconds) < 1e6
    
    def test_cmb_temperature(self):
        """Test CMB temperature matches Planck 2018."""
        universe = CurrentUniverseParameters()
        assert 2.7 < universe.cmb_temperature_K < 2.8
        assert abs(universe.cmb_temperature_K - 2.72548) < 0.01
    
    def test_qcal_coordinates(self):
        """Test QCAL ∞³ symbolic coordinates."""
        universe = CurrentUniverseParameters()
        coords = universe.qcal_coordinates()
        
        assert len(coords) == 3
        assert coords[0] == 0.57
        assert coords[1] == -0.28
        assert coords[2] == 0.77
        
        # Check it's a numpy array
        assert isinstance(coords, np.ndarray)
    
    def test_cosmic_time_Ga(self):
        """Test cosmic time in Gigayears."""
        universe = CurrentUniverseParameters()
        time_Ga = universe.cosmic_time_Ga()
        
        assert time_Ga == 13.8
    
    def test_consciousness_level(self):
        """Test consciousness level classification."""
        universe = CurrentUniverseParameters()
        level = universe.consciousness_level()
        
        assert level == "emergente"
        
        # Test boundary cases
        universe.collective_consciousness_psi = 0.005
        assert universe.consciousness_level() == "primordial"
        
        universe.collective_consciousness_psi = 0.3
        assert universe.consciousness_level() == "desarrollada"
        
        universe.collective_consciousness_psi = 0.8
        assert universe.consciousness_level() == "avanzada"
    
    def test_kardashev_type(self):
        """Test civilization Kardashev type."""
        universe = CurrentUniverseParameters()
        assert 0 < universe.kardashev_type < 1
        assert universe.kardashev_type == 0.7
    
    def test_large_scale_structure(self):
        """Test galaxy and star counts."""
        universe = CurrentUniverseParameters()
        
        # Reasonable ranges
        assert 1e11 < universe.galaxies_formed < 1e13
        assert 1e22 < universe.active_stars < 1e24
        assert 1e9 < universe.habitable_planets < 1e11


class TestCosmicEpoch:
    """Test individual cosmic epoch functionality."""
    
    def test_epoch_creation(self):
        """Test creating a cosmic epoch."""
        epoch = CosmicEpoch(
            name="Test Epoch",
            time_seconds=1e10,
            temperature_K=1e6,
            entropy_normalized=0.5,
            coherence_psi=0.8,
            description="Test description"
        )
        
        assert epoch.name == "Test Epoch"
        assert epoch.time_seconds == 1e10
        assert epoch.temperature_K == 1e6
        assert epoch.entropy_normalized == 0.5
        assert epoch.coherence_psi == 0.8
    
    def test_time_in_years(self):
        """Test time conversion to years."""
        epoch = CosmicEpoch(
            name="Test",
            time_seconds=365.25 * 24 * 3600,  # 1 year
            temperature_K=100,
            entropy_normalized=0.5,
            coherence_psi=0.5,
            description="Test"
        )
        
        assert abs(epoch.time_in_years() - 1.0) < 1e-6
    
    def test_time_formatted(self):
        """Test human-readable time formatting."""
        # Test various scales
        epoch_ms = CosmicEpoch("ms", 0.5, 1e6, 0, 1, "test")
        assert "ms" in epoch_ms.time_formatted()
        
        epoch_s = CosmicEpoch("s", 10, 1e6, 0, 1, "test")
        assert "s" in epoch_s.time_formatted()
        
        epoch_yr = CosmicEpoch("yr", 1e9 * 365.25 * 24 * 3600, 100, 0, 1, "test")
        assert "Ga" in epoch_yr.time_formatted()


class TestCosmicTimeline:
    """Test cosmic timeline functionality."""
    
    def test_timeline_creation(self):
        """Test creating cosmic timeline."""
        timeline = CosmicTimeline()
        
        assert len(timeline.epochs) > 0
        assert 'planck' in timeline.epochs
        assert 'inflation' in timeline.epochs
        assert 'recombination' in timeline.epochs
        assert 'present' in timeline.epochs
    
    def test_get_epoch(self):
        """Test retrieving epochs by name."""
        timeline = CosmicTimeline()
        
        # Valid epochs
        planck = timeline.get_epoch('planck')
        assert planck.name == 'Planck Epoch'
        assert planck.coherence_psi == 1.0
        
        recomb = timeline.get_epoch('recombination')
        assert 'Recombinación' in recomb.name
        assert recomb.temperature_K == 3000
        
        # Invalid epoch
        with pytest.raises(ValueError):
            timeline.get_epoch('invalid_epoch')
    
    def test_epoch_ordering(self):
        """Test that epochs are chronologically ordered."""
        timeline = CosmicTimeline()
        
        # Check key ordering
        t_planck = timeline.get_epoch('planck').time_seconds
        t_inflation = timeline.get_epoch('inflation').time_seconds
        t_nucleosynthesis = timeline.get_epoch('nucleosynthesis').time_seconds
        t_recombination = timeline.get_epoch('recombination').time_seconds
        t_present = timeline.get_epoch('present').time_seconds
        
        assert t_planck < t_inflation
        assert t_inflation < t_nucleosynthesis
        assert t_nucleosynthesis < t_recombination
        assert t_recombination < t_present
    
    def test_temperature_evolution(self):
        """Test temperature decreases with time."""
        timeline = CosmicTimeline()
        
        # Early universe hotter than late universe
        t_early = 1e10  # 10 seconds
        t_late = 1e17   # ~3 billion years
        
        T_early = timeline.temperature_at_time(t_early)
        T_late = timeline.temperature_at_time(t_late)
        
        assert T_early > T_late
        
        # Present day should match CMB
        t_now = CURRENT_UNIVERSE.age_seconds
        T_now = timeline.temperature_at_time(t_now)
        
        assert abs(T_now - CURRENT_UNIVERSE.cmb_temperature_K) < 1.0
    
    def test_coherence_evolution(self):
        """Test coherence decreases with time."""
        timeline = CosmicTimeline()
        
        # Early universe more coherent
        psi_early = timeline.coherence_evolution(1e-40)
        psi_late = timeline.coherence_evolution(1e17)
        
        assert psi_early > psi_late
        assert 0 <= psi_early <= 1
        assert 0 <= psi_late <= 1
        
        # Planck time should have perfect coherence
        psi_planck = timeline.coherence_evolution(timeline.planck_time)
        assert psi_planck == 1.0
    
    def test_power_spectrum(self):
        """Test primordial power spectrum."""
        timeline = CosmicTimeline()
        
        # P(k) ~ k^(n_s - 1)
        k1 = 1.0
        k2 = 2.0
        
        P1 = timeline.power_spectrum_mode(k1)
        P2 = timeline.power_spectrum_mode(k2)
        
        # For n_s ≈ 0.966 < 1, larger k should have less power
        assert P2 < P1
        
        # Check scaling
        expected_ratio = (k2 / k1) ** (timeline.spectral_index_ns - 1)
        actual_ratio = P2 / P1
        assert abs(actual_ratio - expected_ratio) < 1e-10
    
    def test_qcal_frequency_at_epoch(self):
        """Test QCAL frequency evolution with redshift."""
        timeline = CosmicTimeline()
        
        # Present day frequency
        f_present = timeline.qcal_frequency_at_epoch('present')
        assert abs(f_present - F0_HZ) < 1.0  # Should be close to f₀
        
        # Earlier epochs have higher frequency due to redshift
        f_recomb = timeline.qcal_frequency_at_epoch('recombination')
        f_inflation = timeline.qcal_frequency_at_epoch('inflation')
        
        assert f_recomb > f_present
        assert f_inflation > f_recomb
    
    def test_primordial_parameters(self):
        """Test primordial quantum fluctuation parameters."""
        timeline = CosmicTimeline()
        
        # Check quantum fluctuations
        assert timeline.delta_rho_over_rho == 1e-5
        
        # Check spectral index (Planck 2018)
        assert 0.96 < timeline.spectral_index_ns < 0.97
        
        # Check Planck scale
        assert timeline.planck_time > 0
        assert timeline.planck_temperature > 0
    
    def test_summary(self):
        """Test timeline summary generation."""
        timeline = CosmicTimeline()
        
        summary = timeline.summary()
        
        # Should contain key information
        assert "QCAL ∞³ COSMIC TIMELINE" in summary
        assert "13.8" in summary
        assert "2.72548" in summary
        assert "Planck Epoch" in summary
        assert "Recombinación" in summary


class TestModuleLevelFunctions:
    """Test module-level convenience functions."""
    
    def test_get_universe_age(self):
        """Test get_universe_age function."""
        age = get_universe_age()
        assert age == 13.8e9
    
    def test_get_cmb_temperature(self):
        """Test get_cmb_temperature function."""
        T_cmb = get_cmb_temperature()
        assert abs(T_cmb - 2.72548) < 0.01
    
    def test_get_epoch(self):
        """Test get_epoch convenience function."""
        recomb = get_epoch('recombination')
        assert 'Recombinación' in recomb.name
        assert recomb.temperature_K == 3000


class TestGlobalInstances:
    """Test global module instances."""
    
    def test_current_universe_instance(self):
        """Test CURRENT_UNIVERSE global instance."""
        assert CURRENT_UNIVERSE is not None
        assert isinstance(CURRENT_UNIVERSE, CurrentUniverseParameters)
        assert CURRENT_UNIVERSE.age_years == 13.8e9
    
    def test_cosmic_timeline_instance(self):
        """Test COSMIC_TIMELINE global instance."""
        assert COSMIC_TIMELINE is not None
        assert isinstance(COSMIC_TIMELINE, CosmicTimeline)
        assert len(COSMIC_TIMELINE.epochs) > 0


class TestPhysicalConsistency:
    """Test physical consistency of cosmic parameters."""
    
    def test_entropy_increases(self):
        """Test that entropy increases with time (2nd law)."""
        timeline = CosmicTimeline()
        
        # Get chronologically ordered epochs
        epochs_ordered = sorted(
            timeline.epochs.values(),
            key=lambda e: e.time_seconds
        )
        
        # Entropy should generally increase
        for i in range(len(epochs_ordered) - 1):
            assert epochs_ordered[i].entropy_normalized <= epochs_ordered[i+1].entropy_normalized
    
    def test_coherence_decreases(self):
        """Test that coherence decreases with time (decoherence)."""
        timeline = CosmicTimeline()
        
        epochs_ordered = sorted(
            timeline.epochs.values(),
            key=lambda e: e.time_seconds
        )
        
        # Coherence should generally decrease
        for i in range(len(epochs_ordered) - 1):
            assert epochs_ordered[i].coherence_psi >= epochs_ordered[i+1].coherence_psi
    
    def test_temperature_decreases(self):
        """Test that temperature decreases with expansion."""
        timeline = CosmicTimeline()
        
        epochs_ordered = sorted(
            timeline.epochs.values(),
            key=lambda e: e.time_seconds
        )
        
        # Temperature should decrease (with some exceptions during reheating)
        # Check overall trend
        assert epochs_ordered[0].temperature_K > epochs_ordered[-1].temperature_K
        assert epochs_ordered[2].temperature_K > epochs_ordered[-2].temperature_K


class TestQCALIntegration:
    """Test integration with QCAL ∞³ framework."""
    
    def test_f0_present_in_framework(self):
        """Test that f₀ is correctly integrated."""
        from qcal.constants import F0_HZ
        
        # Verify f₀ is the fundamental frequency (with tolerance for floating point)
        assert abs(F0_HZ - 141.70001) < 1e-5
    
    def test_cosmic_coordinates_dimensionality(self):
        """Test QCAL ∞³ cosmic coordinates are 3D."""
        coords = CURRENT_UNIVERSE.qcal_coordinates()
        assert coords.shape == (3,)
    
    def test_consciousness_parameter_range(self):
        """Test consciousness parameter Ψ is properly bounded."""
        for epoch in COSMIC_TIMELINE.epochs.values():
            assert 0 <= epoch.coherence_psi <= 1


def main():
    """Run all tests with detailed output."""
    import sys
    
    print("\n" + "=" * 80)
    print("QCAL ∞³ COSMIC PARAMETERS - TEST SUITE")
    print("=" * 80 + "\n")
    
    # Run pytest with verbose output
    exit_code = pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--color=yes'
    ])
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
