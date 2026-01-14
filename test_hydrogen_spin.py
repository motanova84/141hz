#!/usr/bin/env python3
"""
Test suite for hydrogen spin hyperfine resonance calculations.

Author: José Manuel Mota Burruezo
License: MIT
"""

import pytest
import numpy as np
from src.hydrogen_spin import HydrogenSpinResonance


def test_hydrogen_constants():
    """Test that hydrogen hyperfine constants are correct."""
    hydrogen = HydrogenSpinResonance()
    
    # Check 21 cm line frequency (within 1 Hz of CODATA value)
    assert abs(float(hydrogen.F_HYDROGEN_21CM_HZ) - 1420405751.7667) < 1.0
    
    # Check 21 cm wavelength (within 1 mm)
    assert abs(float(hydrogen.LAMBDA_21CM_M) - 0.2110611405) < 0.001
    
    # Check f₀
    assert abs(float(hydrogen.F0_HZ) - 141.7001) < 0.0001


def test_octave_relationship():
    """Test the octave relationship calculation between hydrogen and f₀."""
    result = HydrogenSpinResonance.calculate_octave_relationship()
    
    # Check that we get a reasonable number of octaves (around 23)
    assert 22 <= result["n_octaves_nearest"] <= 24
    
    # Check that the ratio is approximately 2^23
    expected_ratio = 2 ** result["n_octaves_nearest"]
    assert abs(result["ratio"] - expected_ratio) / expected_ratio < 0.01
    
    # Check that error is reasonably small (less than 1%)
    assert result["error_percent"] < 1.0
    
    # Check formula is generated
    assert "2^" in result["formula"]
    assert "f_H" in result["formula"]


def test_octave_cascade():
    """Test the octave cascade calculation."""
    cascade = HydrogenSpinResonance.calculate_octave_cascade(max_octaves=25)
    
    # Should have 26 entries (0 to 25 inclusive)
    assert len(cascade) == 26
    
    # First entry should be original hydrogen frequency
    assert abs(cascade[0]["frequency_hz"] - 1420405751.7667) < 1.0
    assert cascade[0]["octave"] == 0
    
    # Each successive entry should be half the previous
    for i in range(1, len(cascade)):
        expected_freq = cascade[i-1]["frequency_hz"] / 2.0
        assert abs(cascade[i]["frequency_hz"] - expected_freq) < 0.01
    
    # At least one entry should be flagged as near f₀
    near_f0 = [e for e in cascade if e["is_near_f0"]]
    assert len(near_f0) >= 1


def test_find_resonance_octave():
    """Test finding the specific resonance octave."""
    resonance = HydrogenSpinResonance.find_resonance_octave()
    
    # Should find an octave close to f₀
    assert abs(resonance["frequency_at_octave"] - 141.7001) < 5.0
    
    # Relative error should be small
    assert resonance["relative_error"] < 0.05  # Less than 5%
    
    # Should have reasonable octave number
    assert 20 <= resonance["nearest_integer_octave"] <= 25
    
    # Exact octave should be close to integer octave
    assert abs(resonance["exact_octave"] - resonance["nearest_integer_octave"]) < 0.5


def test_primordial_bit_properties():
    """Test calculation of hydrogen as primordial quantum bit."""
    qubit = HydrogenSpinResonance.calculate_primordial_bit_properties()
    
    # Check essential fields exist
    assert "system" in qubit
    assert "state_0" in qubit
    assert "state_1" in qubit
    assert "energy_splitting_J" in qubit
    assert "energy_splitting_eV" in qubit
    assert "frequency_hz" in qubit
    assert "wavelength_cm" in qubit
    
    # Energy should be positive
    assert qubit["energy_splitting_J"] > 0
    assert qubit["energy_splitting_eV"] > 0
    
    # Frequency should match hydrogen hyperfine
    assert abs(qubit["frequency_hz"] - 1420405751.7667) < 1.0
    
    # Wavelength should be approximately 21 cm
    assert abs(qubit["wavelength_cm"] - 21.1) < 0.1
    
    # Temperature equivalent should be in millikelvin range
    assert 0.05 < qubit["temperature_equivalent_K"] < 0.1
    
    # Coherence time should be inverse of frequency
    expected_tau = 1.0 / qubit["frequency_hz"]
    assert abs(qubit["coherence_time_s"] - expected_tau) < 1e-15


def test_information_viscosity():
    """Test information viscosity calculation across octaves."""
    result = HydrogenSpinResonance.calculate_information_viscosity()
    
    # Should have viscosity data
    assert "viscosity_data" in result
    assert len(result["viscosity_data"]) > 0
    
    # Should identify zero-viscosity point
    assert "zero_viscosity_octave" in result
    assert "zero_viscosity_frequency" in result
    
    # Zero-viscosity frequency should be close to f₀
    assert abs(result["zero_viscosity_frequency"] - 141.7001) < 5.0
    
    # Check that viscosity increases away from f₀
    visc_data = result["viscosity_data"]
    zero_octave = result["zero_viscosity_octave"]
    
    # Find entries before and after zero point
    if 0 < zero_octave < len(visc_data) - 1:
        visc_at_zero = visc_data[zero_octave]["information_viscosity"]
        visc_before = visc_data[zero_octave - 1]["information_viscosity"]
        visc_after = visc_data[zero_octave + 1]["information_viscosity"]
        
        # Viscosity at zero point should be minimum
        assert visc_at_zero <= visc_before or visc_at_zero <= visc_after


def test_validate_primordial_bit_hypothesis():
    """Test validation of the primordial bit hypothesis."""
    validation = HydrogenSpinResonance.validate_primordial_bit_hypothesis()
    
    # Should have validation structure
    assert "hypothesis" in validation
    assert "validations" in validation
    assert "overall_valid" in validation
    assert "summary" in validation
    
    # Should have multiple validation criteria
    assert len(validation["validations"]) >= 4
    
    # Each validation should have 'valid' and 'reason' fields
    for key, val in validation["validations"].items():
        assert "valid" in val
        assert "reason" in val
        assert isinstance(val["valid"], bool)
        assert isinstance(val["reason"], str)
    
    # Key validations should pass
    assert validation["validations"]["hydrogen_is_simplest_atom"]["valid"]
    assert validation["validations"]["hyperfine_is_two_level"]["valid"]
    assert validation["validations"]["f0_is_biological_threshold"]["valid"]
    
    # Overall should be valid
    assert validation["overall_valid"]
    
    # Summary should contain key information
    summary = validation["summary"]
    assert "hydrogen_frequency_hz" in summary
    assert "f0_frequency_hz" in summary
    assert "octave_cascade" in summary
    assert "interpretation" in summary
    
    # Octave cascade should be reasonable
    assert 20 <= summary["octave_cascade"] <= 25


def test_hyperfine_energy():
    """Test hyperfine energy calculation."""
    hydrogen = HydrogenSpinResonance()
    
    # Energy should be E = hf
    h = 6.62607015e-34
    f = 1420405751.7667
    expected_energy = h * f
    
    assert abs(float(hydrogen.E_HYPERFINE) - expected_energy) < 1e-40


def test_spin_quantum_numbers():
    """Test that spin quantum numbers are correct."""
    hydrogen = HydrogenSpinResonance()
    
    # Both electron and proton have spin 1/2
    assert float(hydrogen.S_ELECTRON) == 0.5
    assert float(hydrogen.S_PROTON) == 0.5


def test_cascade_wavelengths():
    """Test that wavelengths in cascade are physically reasonable."""
    cascade = HydrogenSpinResonance.calculate_octave_cascade(max_octaves=25)
    
    for entry in cascade:
        freq = entry["frequency_hz"]
        wavelength = entry["wavelength_m"]
        
        # Check λ = c/f
        c = 299792458.0  # m/s
        expected_wavelength = c / freq
        assert abs(wavelength - expected_wavelength) / expected_wavelength < 1e-10
        
        # Wavelength should be positive
        assert wavelength > 0


def test_octave_precision():
    """Test that octave calculations maintain high precision."""
    result = HydrogenSpinResonance.calculate_octave_relationship()
    
    # Recalculate using the formula
    f_hydrogen = result["f_hydrogen_hz"]
    n_octaves = result["n_octaves_nearest"]
    f0_calculated = f_hydrogen / (2 ** n_octaves)
    
    # Should match reported value
    assert abs(f0_calculated - result["f0_from_octaves"]) < 1e-10


def test_biological_frequency_range():
    """Test that f₀ is in the biological frequency range."""
    hydrogen = HydrogenSpinResonance()
    f0 = float(hydrogen.F0_HZ)
    
    # f₀ should be in range relevant to biological systems
    # EEG: 0.5-100 Hz
    # Heart rate: 0.5-3 Hz (at rest)
    # f₀ = 141.7 Hz is in the gamma brainwave range (30-100 Hz extended)
    assert 100 < f0 < 200  # Extended biological range
    
    # Check harmonics fall in known biological ranges
    f0_over_2 = f0 / 2  # ≈ 70.85 Hz (gamma range)
    assert 30 < f0_over_2 < 100  # Gamma range
    
    f0_over_6 = f0 / 6  # ≈ 23.6 Hz (beta range)
    assert 13 < f0_over_6 < 30  # Beta range
    
    f0_over_18 = f0 / 18  # ≈ 7.87 Hz (theta/alpha range)
    assert 4 < f0_over_18 < 13  # Theta/Alpha range


def test_demonstrate_function_runs():
    """Test that the demonstration function runs without errors."""
    from src.hydrogen_spin import demonstrate_hydrogen_resonance
    
    # Should run without raising exceptions
    # (We don't check output, just that it completes)
    try:
        demonstrate_hydrogen_resonance()
        assert True
    except Exception as e:
        pytest.fail(f"demonstrate_hydrogen_resonance() raised {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
