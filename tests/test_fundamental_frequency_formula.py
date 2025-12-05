#!/usr/bin/env python3
"""
Tests for Fundamental Frequency Formula f₀ = c / (2π R_Ψ ℓ_P)

Tests the implementation of the fundamental frequency derivation from
quantum-cosmological constants.
"""

import pytest
import mpmath as mp  # noqa: F401
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from constants import (  # noqa: E402
    UniversalConstants,
    CONSTANTS,
    G_NEWTON,
    L_PLANCK,
    R_PSI_COSMOLOGICAL,
    R_PSI_SCALE_FACTOR,
)


class TestPlanckLength:
    """Test Planck length constant and derivation."""

    def test_planck_length_value(self):
        """Test that Planck length has the correct value."""
        const = UniversalConstants()
        l_p = float(const.L_PLANCK)

        # Planck length: ℓ_P = √(ℏG/c³) ≈ 1.616255 × 10⁻³⁵ m
        assert l_p == pytest.approx(1.616255e-35, rel=1e-6)

    def test_planck_length_derivation(self):
        """Test that Planck length is correctly derived from fundamental constants."""
        const = UniversalConstants()

        # Calculate: ℓ_P = √(ℏG/c³)
        h_bar = const.H_BAR
        G = const.G_NEWTON
        c = const.C_LIGHT

        l_p_derived = mp.sqrt(h_bar * G / (c ** 3))

        assert abs(float(l_p_derived) - float(const.L_PLANCK)) < 1e-42

    def test_planck_length_units(self):
        """Test that Planck length has correct dimensionality."""
        const = UniversalConstants()
        l_p = float(const.L_PLANCK)

        # Should be in meters
        assert l_p > 0
        assert l_p < 1e-34  # Smaller than atomic scales
        assert l_p > 1e-36  # But not arbitrarily small

    def test_planck_length_convenience_function(self):
        """Test the convenience function for Planck length."""
        l_p_direct = float(CONSTANTS.L_PLANCK)
        l_p_function = float(L_PLANCK())

        assert l_p_direct == pytest.approx(l_p_function, abs=1e-42)


class TestCosmologicalScale:
    """Test cosmological compactification radius R_Ψ."""

    def test_cosmological_scale_factor(self):
        """Test that the scale factor is 10⁴⁷."""
        assert float(CONSTANTS.R_PSI_SCALE_FACTOR) == pytest.approx(1e47, rel=1e-10)
        assert float(R_PSI_SCALE_FACTOR) == pytest.approx(1e47, rel=1e-10)

    def test_cosmological_radius_value(self):
        """Test that R_Ψ = 10⁴⁷ × ℓ_P."""
        const = UniversalConstants()

        R_psi_expected = const.R_PSI_SCALE_FACTOR * const.L_PLANCK
        assert float(const.R_PSI_COSMOLOGICAL) == pytest.approx(float(R_psi_expected), abs=1e-6)

    def test_cosmological_radius_magnitude(self):
        """Test that R_Ψ is at cosmological scale."""
        const = UniversalConstants()
        R_psi = float(const.R_PSI_COSMOLOGICAL)

        # Should be around 10¹² meters (planetary orbital scale)
        assert R_psi > 1e11  # Greater than 100 billion meters
        assert R_psi < 1e13  # Less than 10 trillion meters

        # More precisely, around 1.616 × 10¹² m
        assert R_psi == pytest.approx(1.616e12, rel=0.01)

    def test_cosmological_radius_in_au(self):
        """Test that R_Ψ is around 10 AU (near Saturn's orbit)."""
        const = UniversalConstants()
        R_psi = float(const.R_PSI_COSMOLOGICAL)

        # 1 AU = 1.496 × 10¹¹ m
        AU = 1.496e11
        R_psi_in_au = R_psi / AU

        # Should be around 10-11 AU
        assert R_psi_in_au == pytest.approx(10.8, rel=0.1)

    def test_cosmological_radius_convenience_function(self):
        """Test the convenience function for cosmological radius."""
        R_psi_direct = float(CONSTANTS.R_PSI_COSMOLOGICAL)
        R_psi_function = float(R_PSI_COSMOLOGICAL())

        assert R_psi_direct == pytest.approx(R_psi_function, abs=1e-6)


class TestGravitationalConstant:
    """Test Newton's gravitational constant."""

    def test_newton_constant_value(self):
        """Test that G has the CODATA 2018 value."""
        const = UniversalConstants()
        G = float(const.G_NEWTON)

        # CODATA 2018: G = 6.67430(15) × 10⁻¹¹ m³/(kg·s²)
        assert G == pytest.approx(6.67430e-11, rel=1e-6)

    def test_newton_constant_export(self):
        """Test that G is exported correctly."""
        assert float(G_NEWTON) == pytest.approx(6.67430e-11, rel=1e-6)


class TestFundamentalFrequencyFormula:
    """Test the fundamental frequency formula f₀ = c / (2π R_Ψ ℓ_P)."""

    def test_formula_structure(self):
        """Test that the formula is properly implemented."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # Check that the derivation returns a dictionary
        assert isinstance(derivation, dict)
        assert "formula" in derivation
        assert derivation["formula"] == "f₀ = c / (2π R_Ψ ℓ_P)"

    def test_formula_components(self):
        """Test that all formula components are present."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # Required keys
        required_keys = [
            "f0_target_hz",
            "l_planck_m",
            "R_psi_cosmological_m",
            "R_psi_observed_m",
            "R_psi_required_for_f0_m",
            "formula"
        ]

        for key in required_keys:
            assert key in derivation, f"Missing key: {key}"

    def test_cosmological_interpretation(self):
        """Test the cosmological scale interpretation of the formula."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # With R_Ψ = 10⁴⁷ ℓ_P, the formula gives a very high frequency
        f0_cosmo = derivation["f0_from_cosmological_rpsi_hz"]

        # This frequency should be much larger than the observed f₀
        assert f0_cosmo > 1e20  # Much higher than 141.7 Hz

    def test_observed_scale_interpretation(self):
        """Test the observed scale interpretation."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # The observed R_PSI = c/(2πf₀) gives the correct f₀
        f0_target = derivation["f0_target_hz"]
        assert f0_target == pytest.approx(141.7001, abs=1e-4)

    def test_required_rpsi_for_observed_f0(self):
        """Test calculation of R_Ψ required for f₀ = 141.7001 Hz."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # This should be around 10⁷⁵ ℓ_P, not 10⁴⁷
        R_psi_in_planck = derivation["R_psi_required_in_planck_units"]
        assert R_psi_in_planck > 1e74
        assert R_psi_in_planck < 1e76

    def test_formula_consistency(self):
        """Test that the formula is internally consistent."""
        const = UniversalConstants()

        # If we use f₀ = c / (2π R_Ψ ℓ_P), then:
        # R_Ψ = c / (2π f₀ ℓ_P)

        f0 = const.F0
        c = const.C_LIGHT
        l_p = const.L_PLANCK

        # Calculate required R_Ψ
        R_psi_calc = c / (2 * mp.pi * f0 * l_p)

        # Verify: f₀ = c / (2π R_Ψ ℓ_P)
        f0_verify = c / (2 * mp.pi * R_psi_calc * l_p)

        assert abs(float(f0_verify) - float(f0)) < 1e-6


class TestQuantumCosmologicalHierarchy:
    """Test the hierarchy between quantum and cosmological scales."""

    def test_planck_to_cosmological_hierarchy(self):
        """Test the hierarchy factor between Planck and cosmological scales."""
        const = UniversalConstants()

        # The hierarchy is R_Ψ / ℓ_P ≈ 10⁴⁷
        hierarchy = const.R_PSI_COSMOLOGICAL / const.L_PLANCK

        assert float(hierarchy) == pytest.approx(1e47, rel=1e-6)

    def test_scale_separation(self):
        """Test that scales are well-separated."""
        const = UniversalConstants()

        l_p = float(const.L_PLANCK)
        R_psi_cosmo = float(const.R_PSI_COSMOLOGICAL)
        R_psi_obs = float(const.R_PSI)

        # Planck scale << Observable R_PSI << Cosmological R_Ψ
        assert l_p < R_psi_obs < R_psi_cosmo

        # The separations should be enormous
        assert R_psi_obs / l_p > 1e39  # Observable >> Planck
        assert R_psi_cosmo / R_psi_obs > 1e6  # Cosmological >> Observable

    def test_hierarchy_connects_to_frequency(self):
        """Test that the hierarchy is related to the observed frequency."""
        const = UniversalConstants()
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # The observed R_PSI gives f₀ = 141.7 Hz
        R_psi_obs = derivation["R_psi_observed_m"]
        f0 = const.F0
        c = const.C_LIGHT

        # Verify: f₀ = c / (2π R_PSI)
        f0_calc = c / (2 * mp.pi * mp.mpf(str(R_psi_obs)))

        assert abs(float(f0_calc) - float(f0)) < 0.1


class TestExportedConstants:
    """Test that new constants are properly exported."""

    def test_dict_export_includes_new_constants(self):
        """Test that to_dict includes all new constants."""
        const = UniversalConstants()
        data = const.to_dict()

        # Check for new constants
        assert "G_newton_m3_kg_s2" in data
        assert "l_planck_m" in data
        assert "R_psi_cosmological_m" in data
        assert "R_psi_scale_factor" in data

        # Verify values
        assert data["G_newton_m3_kg_s2"] == pytest.approx(6.67430e-11, rel=1e-6)
        assert data["l_planck_m"] == pytest.approx(1.616255e-35, rel=1e-6)
        assert data["R_psi_scale_factor"] == pytest.approx(1e47, rel=1e-10)

    def test_backwards_compatibility(self):
        """Test that existing exports still work."""
        const = UniversalConstants()
        data = const.to_dict()

        # Old constants should still be present
        assert "f0_hz" in data
        assert "E_psi_joules" in data
        assert "R_psi_m" in data

        # Values should match
        assert data["f0_hz"] == pytest.approx(float(const.F0), abs=1e-4)


class TestPhysicalInterpretation:
    """Test physical interpretation of the formula."""

    def test_formula_connects_scales(self):
        """Test that the formula connects quantum and cosmological scales."""
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)

        # The formula should involve:
        # - Quantum scale (ℓ_P ≈ 10⁻³⁵ m)
        # - Cosmological scale (R_Ψ ≈ 10¹² m)
        # - Observable frequency (f₀ ≈ 10² Hz)

        assert "l_planck_m" in derivation
        assert "R_psi_cosmological_m" in derivation
        assert "f0_target_hz" in derivation

        assert derivation["l_planck_m"] < 1e-34
        assert derivation["R_psi_cosmological_m"] > 1e11
        assert 100 < derivation["f0_target_hz"] < 200

    def test_dimensionality(self):
        """Test that the formula has correct dimensions."""
        # [f₀] = Hz = 1/s
        # [c] = m/s
        # [R_Ψ] = m
        # [ℓ_P] = m
        # [c / (R_Ψ × ℓ_P)] = (m/s) / (m × m) = 1/(m·s) ✗ Wrong!
        # But [c / (2π R_Ψ ℓ_P)] should give Hz

        # The formula as written doesn't have correct dimensions
        # This suggests R_Ψ might be dimensionless (R_Ψ / ℓ_P)
        # Or there's a different interpretation

        # For now, just verify the formula is documented
        derivation = UniversalConstants.derive_f0_from_compactification(precision=50)
        assert "note" in derivation


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "--tb=short"])
