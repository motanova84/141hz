#!/usr/bin/env python3
"""
Tests for Dual Mass Perspective Framework

Tests the implementation of the dual mass perspective unifying:
1. Traditional physics: m_eff = hf/c² (m ∝ f)
2. Noetic axiom: m_noesis ∝ 1/f (mass as detention)
3. Unified equation: m(f) = hf₀/c² (constant)
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add qcal to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.dual_mass import (
    DualMassPerspective,
    effective_mass,
    noetic_mass,
    unified_mass,
    calculate_dual_mass_spectrum,
    H_PLANCK,
    C_LIGHT,
    F0_HZ
)

from qcal.constants import M_MIN_NOETIC, ALPHA_NOETIC


class TestDualMassPerspective:
    """Test suite for DualMassPerspective class."""
    
    def test_initialization(self):
        """Test that DualMassPerspective initializes correctly."""
        dmp = DualMassPerspective()
        assert dmp.f0 == F0_HZ
        assert dmp.h == H_PLANCK
        assert dmp.c == C_LIGHT
        
        # Check minimal mass calculation
        expected_m_min = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        assert dmp.m_min == pytest.approx(expected_m_min, rel=1e-10)
        
        # Check alpha constant
        expected_alpha = H_PLANCK * F0_HZ
        assert dmp.alpha == pytest.approx(expected_alpha, rel=1e-10)
    
    def test_custom_f0(self):
        """Test initialization with custom f₀."""
        custom_f0 = 100.0
        dmp = DualMassPerspective(f0=custom_f0)
        assert dmp.f0 == custom_f0
        assert dmp.m_min == pytest.approx(H_PLANCK * custom_f0 / (C_LIGHT ** 2), rel=1e-10)
    
    def test_effective_mass_scalar(self):
        """Test effective mass calculation with scalar input."""
        dmp = DualMassPerspective()
        
        # Test at f₀
        m_eff_f0 = dmp.effective_mass(F0_HZ)
        assert m_eff_f0 == pytest.approx(dmp.m_min, rel=1e-10)
        
        # Test proportionality: m_eff ∝ f
        f1, f2 = 100.0, 200.0
        m1 = dmp.effective_mass(f1)
        m2 = dmp.effective_mass(f2)
        assert m2 / m1 == pytest.approx(f2 / f1, rel=1e-10)
    
    def test_effective_mass_array(self):
        """Test effective mass calculation with array input."""
        dmp = DualMassPerspective()
        freqs = np.array([10.0, 100.0, 1000.0])
        masses = dmp.effective_mass(freqs)
        
        assert isinstance(masses, np.ndarray)
        assert len(masses) == len(freqs)
        
        # Verify each element
        for i, f in enumerate(freqs):
            expected = H_PLANCK * f / (C_LIGHT ** 2)
            assert masses[i] == pytest.approx(expected, rel=1e-10)
    
    def test_noetic_mass_scalar(self):
        """Test noetic mass calculation with scalar input."""
        dmp = DualMassPerspective()
        
        # Test at f₀
        m_noesis_f0 = dmp.noetic_mass(F0_HZ)
        assert m_noesis_f0 == pytest.approx(dmp.m_min, rel=1e-10)
        
        # Test inverse proportionality: m_noesis ∝ 1/f
        f1, f2 = 100.0, 200.0
        m1 = dmp.noetic_mass(f1)
        m2 = dmp.noetic_mass(f2)
        assert m2 / m1 == pytest.approx(f1 / f2, rel=1e-10)
    
    def test_noetic_mass_array(self):
        """Test noetic mass calculation with array input."""
        dmp = DualMassPerspective()
        freqs = np.array([10.0, 100.0, 1000.0])
        masses = dmp.noetic_mass(freqs)
        
        assert isinstance(masses, np.ndarray)
        assert len(masses) == len(freqs)
        
        # Verify each element
        for i, f in enumerate(freqs):
            expected = dmp.alpha / f
            assert masses[i] == pytest.approx(expected, rel=1e-10)
    
    def test_unified_mass_constant(self):
        """Test that unified mass is constant for all frequencies."""
        dmp = DualMassPerspective()
        
        # Test various frequencies
        test_freqs = [1.0, 10.0, 141.7001, 1000.0, 1e6]
        for f in test_freqs:
            m = dmp.unified_mass(f)
            assert m == pytest.approx(dmp.m_min, rel=1e-15)
    
    def test_unified_mass_array(self):
        """Test that unified mass returns constant array."""
        dmp = DualMassPerspective()
        freqs = np.linspace(1, 1000, 100)
        masses = dmp.unified_mass(freqs)
        
        assert isinstance(masses, np.ndarray)
        assert len(masses) == len(freqs)
        assert np.all(masses == dmp.m_min)
    
    def test_mass_equilibrium_at_f0(self):
        """Test that all three masses are equal at f₀."""
        dmp = DualMassPerspective()
        
        m_eff = dmp.effective_mass(F0_HZ)
        m_noesis = dmp.noetic_mass(F0_HZ)
        m_dual = dmp.unified_mass(F0_HZ)
        
        assert m_eff == pytest.approx(m_noesis, rel=1e-10)
        assert m_eff == pytest.approx(m_dual, rel=1e-10)
        assert m_noesis == pytest.approx(m_dual, rel=1e-10)
    
    def test_mass_ratio(self):
        """Test mass ratio calculations."""
        dmp = DualMassPerspective()
        
        # At f₀, both ratios should be 1
        r_eff, r_noesis = dmp.mass_ratio(F0_HZ)
        assert r_eff == pytest.approx(1.0, rel=1e-10)
        assert r_noesis == pytest.approx(1.0, rel=1e-10)
        
        # At 2*f₀
        r_eff, r_noesis = dmp.mass_ratio(2 * F0_HZ)
        assert r_eff == pytest.approx(2.0, rel=1e-10)
        assert r_noesis == pytest.approx(0.5, rel=1e-10)
        
        # At f₀/2
        r_eff, r_noesis = dmp.mass_ratio(F0_HZ / 2)
        assert r_eff == pytest.approx(0.5, rel=1e-10)
        assert r_noesis == pytest.approx(2.0, rel=1e-10)
        
        # Product should always be 1
        r_eff, r_noesis = dmp.mass_ratio(123.456)
        assert r_eff * r_noesis == pytest.approx(1.0, rel=1e-10)
    
    def test_mass_ratio_array(self):
        """Test mass ratio with array input."""
        dmp = DualMassPerspective()
        freqs = np.array([F0_HZ/2, F0_HZ, 2*F0_HZ])
        r_eff, r_noesis = dmp.mass_ratio(freqs)
        
        assert isinstance(r_eff, np.ndarray)
        assert isinstance(r_noesis, np.ndarray)
        
        # Check product is always 1
        products = r_eff * r_noesis
        assert np.allclose(products, 1.0, rtol=1e-10)
    
    def test_get_constants(self):
        """Test getting constants dictionary."""
        dmp = DualMassPerspective()
        const = dmp.get_constants()
        
        assert 'f0' in const
        assert 'm_min' in const
        assert 'alpha' in const
        assert 'h' in const
        assert 'c' in const
        assert 'c2' in const
        
        assert const['f0'] == F0_HZ
        assert const['h'] == H_PLANCK
        assert const['c'] == C_LIGHT
    
    def test_dimensional_analysis(self):
        """Test that all masses have correct dimensions (kg)."""
        dmp = DualMassPerspective()
        
        # All masses should be in kg (positive values)
        m_eff = dmp.effective_mass(141.7001)
        m_noesis = dmp.noetic_mass(141.7001)
        m_dual = dmp.unified_mass(141.7001)
        
        assert m_eff > 0
        assert m_noesis > 0
        assert m_dual > 0
        
        # Check expected order of magnitude
        # For f₀ ≈ 141.7 Hz, m ≈ 10⁻⁴⁸ kg
        assert 1e-50 < m_eff < 1e-46
        assert 1e-50 < m_noesis < 1e-46
        assert 1e-50 < m_dual < 1e-46


class TestConvenienceFunctions:
    """Test convenience functions for direct calculations."""
    
    def test_effective_mass_function(self):
        """Test standalone effective_mass function."""
        m = effective_mass(141.7001)
        expected = H_PLANCK * 141.7001 / (C_LIGHT ** 2)
        assert m == pytest.approx(expected, rel=1e-10)
    
    def test_noetic_mass_function(self):
        """Test standalone noetic_mass function."""
        m = noetic_mass(141.7001)
        expected = (H_PLANCK * (F0_HZ ** 2) / (C_LIGHT ** 2)) / 141.7001
        assert m == pytest.approx(expected, rel=1e-10)
    
    def test_unified_mass_function(self):
        """Test standalone unified_mass function."""
        m = unified_mass()
        expected = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        assert m == pytest.approx(expected, rel=1e-10)
    
    def test_custom_constants(self):
        """Test functions with custom physical constants."""
        custom_h = 7e-34
        custom_c = 3e8
        custom_f0 = 100.0
        
        m_eff = effective_mass(100.0, h=custom_h, c=custom_c)
        expected = custom_h * 100.0 / (custom_c ** 2)
        assert m_eff == pytest.approx(expected, rel=1e-10)
        
        m_noesis = noetic_mass(100.0, f0=custom_f0, h=custom_h, c=custom_c)
        expected = (custom_h * (custom_f0 ** 2) / (custom_c ** 2)) / 100.0
        assert m_noesis == pytest.approx(expected, rel=1e-10)


class TestDualMassSpectrum:
    """Test complete spectrum calculations."""
    
    def test_calculate_dual_mass_spectrum(self):
        """Test spectrum calculation function."""
        freqs = np.logspace(0, 3, 50)  # 1 Hz to 1000 Hz
        spectrum = calculate_dual_mass_spectrum(freqs)
        
        # Check all expected keys
        assert 'frequencies' in spectrum
        assert 'm_eff' in spectrum
        assert 'm_noesis' in spectrum
        assert 'm_dual' in spectrum
        assert 'r_eff' in spectrum
        assert 'r_noesis' in spectrum
        assert 'm_min' in spectrum
        assert 'f0' in spectrum
        
        # Check array shapes
        assert len(spectrum['frequencies']) == len(freqs)
        assert len(spectrum['m_eff']) == len(freqs)
        assert len(spectrum['m_noesis']) == len(freqs)
        assert len(spectrum['m_dual']) == len(freqs)
        
        # Check m_dual is constant
        assert np.all(spectrum['m_dual'] == spectrum['m_min'])
    
    def test_spectrum_with_custom_f0(self):
        """Test spectrum with custom reference frequency."""
        freqs = np.array([50.0, 100.0, 200.0])
        custom_f0 = 100.0
        spectrum = calculate_dual_mass_spectrum(freqs, f0=custom_f0)
        
        assert spectrum['f0'] == custom_f0
        
        # At custom_f0, m_eff should equal m_noesis
        idx = 1  # 100.0 Hz
        assert spectrum['m_eff'][idx] == pytest.approx(spectrum['m_noesis'][idx], rel=1e-10)


class TestPhysicalInterpretations:
    """Test physical interpretations and relationships."""
    
    def test_high_frequency_limit(self):
        """Test behavior at high frequencies (pure energy)."""
        dmp = DualMassPerspective()
        high_freq = 1e20  # Very high frequency
        
        m_eff = dmp.effective_mass(high_freq)
        m_noesis = dmp.noetic_mass(high_freq)
        
        # High frequency: large m_eff (lots of energy)
        assert m_eff > dmp.m_min
        # High frequency: small m_noesis (no detention, pure vibration)
        assert m_noesis < dmp.m_min
    
    def test_low_frequency_limit(self):
        """Test behavior at low frequencies (detention)."""
        dmp = DualMassPerspective()
        low_freq = 0.01  # Very low frequency
        
        m_eff = dmp.effective_mass(low_freq)
        m_noesis = dmp.noetic_mass(low_freq)
        
        # Low frequency: small m_eff (little energy)
        assert m_eff < dmp.m_min
        # Low frequency: large m_noesis (lots of detention, slow vibration)
        assert m_noesis > dmp.m_min
    
    def test_duality_complementarity(self):
        """Test that effective and noetic masses are complementary."""
        dmp = DualMassPerspective()
        
        # At any frequency, the product of ratios should be 1
        test_freqs = [0.1, 1.0, 10.0, 100.0, 1000.0]
        for f in test_freqs:
            r_eff, r_noesis = dmp.mass_ratio(f)
            # r_eff = f/f₀, r_noesis = f₀/f
            # Product: (f/f₀) × (f₀/f) = 1
            assert r_eff * r_noesis == pytest.approx(1.0, rel=1e-10)
    
    def test_unification_identity(self):
        """Test that unified mass equals product of dual perspectives."""
        dmp = DualMassPerspective()
        
        test_freqs = [1.0, 141.7001, 1000.0]
        for f in test_freqs:
            m_eff = dmp.effective_mass(f)
            m_noesis = dmp.noetic_mass(f)
            m_dual = dmp.unified_mass(f)
            
            # Mathematical identity: m_dual = m_eff × (f₀/f) = m_noesis × (f/f₀)
            assert m_dual == pytest.approx(m_eff * (dmp.f0 / f), rel=1e-10)
            assert m_dual == pytest.approx(m_noesis * (f / dmp.f0), rel=1e-10)


class TestIntegrationWithConstants:
    """Test integration with qcal.constants module."""
    
    def test_m_min_consistency(self):
        """Test that M_MIN_NOETIC from constants matches calculation."""
        dmp = DualMassPerspective()
        assert dmp.m_min == pytest.approx(M_MIN_NOETIC, rel=1e-10)
    
    def test_alpha_consistency(self):
        """Test that ALPHA_NOETIC from constants matches calculation."""
        dmp = DualMassPerspective()
        assert dmp.alpha == pytest.approx(ALPHA_NOETIC, rel=1e-10)
    
    def test_constants_value_range(self):
        """Test that constants have physically reasonable values."""
        # M_MIN_NOETIC should be on order of 10⁻⁴⁸ kg
        assert 1e-50 < M_MIN_NOETIC < 1e-46
        
        # ALPHA_NOETIC has units kg·Hz (since α = hf₀²/c²)
        # Should be on order of 10⁻⁴⁶ kg·Hz
        assert 1e-48 < ALPHA_NOETIC < 1e-44


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_frequency_handling(self):
        """Test behavior with zero frequency (should handle gracefully)."""
        dmp = DualMassPerspective()
        
        # Effective mass at f=0 should be 0
        m_eff = dmp.effective_mass(0.0)
        assert m_eff == 0.0
        
        # Noetic mass at f=0 would be infinite (division by zero)
        # This should either raise an error or return inf
        with pytest.raises(ZeroDivisionError):
            m_noesis = dmp.noetic_mass(0.0)
    
    def test_negative_frequency_handling(self):
        """Test with negative frequency (unphysical but mathematically valid)."""
        dmp = DualMassPerspective()
        
        # Negative frequencies give negative masses (unphysical but consistent)
        m_eff = dmp.effective_mass(-100.0)
        assert m_eff < 0
        
        m_noesis = dmp.noetic_mass(-100.0)
        assert m_noesis < 0
    
    def test_very_large_arrays(self):
        """Test with large arrays for performance."""
        dmp = DualMassPerspective()
        freqs = np.logspace(-2, 6, 10000)  # 10,000 points
        
        m_eff = dmp.effective_mass(freqs)
        m_noesis = dmp.noetic_mass(freqs)
        m_dual = dmp.unified_mass(freqs)
        
        assert len(m_eff) == 10000
        assert len(m_noesis) == 10000
        assert len(m_dual) == 10000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
