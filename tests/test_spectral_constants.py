#!/usr/bin/env python3
"""
Tests for the Spectral Constants Module (Dual-Constant Framework)

Tests the implementation of the spectral constants C_PRIMARY (629.83) and 
C_COHERENCE (244.36) and their role in deriving f₀ = 141.7001 Hz.

The dual-constant framework establishes:
- C_PRIMARY = 629.83: Primary spectral residue from λ₀ (structure)
- C_COHERENCE = 244.36: Derived coherence constant from second moment (form)

Both constants emerge from the H_Ψ operator and combine to produce f₀.
"""

import pytest
import mpmath as mp
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from spectral_constants import (
    SpectralConstants,
    SPECTRAL,
    C_PRIMARY,
    C_COHERENCE,
    COHERENCE_FACTOR,
    LAMBDA_0,
    LAMBDA_MEAN,
)


class TestSpectralConstantsValues:
    """Test that spectral constants have correct values."""
    
    def test_c_primary_value(self):
        """Test C_PRIMARY = 629.83."""
        assert float(C_PRIMARY) == pytest.approx(629.83, abs=0.01)
        assert float(SPECTRAL.C_PRIMARY) == pytest.approx(629.83, abs=0.01)
    
    def test_c_coherence_value(self):
        """Test C_COHERENCE = 244.36."""
        assert float(C_COHERENCE) == pytest.approx(244.36, abs=0.01)
        assert float(SPECTRAL.C_COHERENCE) == pytest.approx(244.36, abs=0.01)
    
    def test_coherence_factor_value(self):
        """Test COHERENCE_FACTOR ≈ 0.388."""
        assert float(COHERENCE_FACTOR) == pytest.approx(0.388, abs=0.001)
        assert float(SPECTRAL.COHERENCE_FACTOR) == pytest.approx(0.388, abs=0.001)
    
    def test_lambda_0_value(self):
        """Test minimum eigenvalue λ₀ ≈ 0.00158773."""
        assert float(LAMBDA_0) == pytest.approx(0.00158773, abs=1e-7)
    
    def test_lambda_mean_value(self):
        """Test mean eigenvalue ⟨λ⟩ ≈ 0.6228786."""
        assert float(LAMBDA_MEAN) == pytest.approx(0.6228786, abs=1e-6)


class TestSpectralConstantsRelationships:
    """Test relationships between spectral constants."""
    
    def test_c_primary_from_lambda0(self):
        """Test C_PRIMARY ≈ 1/λ₀."""
        c_computed = 1 / LAMBDA_0
        tolerance = 0.0001 * float(C_PRIMARY)  # 0.01% tolerance
        assert abs(float(c_computed) - float(C_PRIMARY)) < tolerance
    
    def test_c_coherence_from_moments(self):
        """Test C_COHERENCE ≈ ⟨λ⟩²/λ₀."""
        c_computed = (LAMBDA_MEAN ** 2) / LAMBDA_0
        tolerance = 0.0001 * float(C_COHERENCE)  # 0.01% tolerance
        assert abs(float(c_computed) - float(C_COHERENCE)) < tolerance
    
    def test_coherence_factor_is_ratio(self):
        """Test COHERENCE_FACTOR = C_COHERENCE / C_PRIMARY."""
        factor_computed = C_COHERENCE / C_PRIMARY
        assert abs(float(factor_computed) - float(COHERENCE_FACTOR)) < 1e-10
    
    def test_constants_are_distinct(self):
        """Test that both constants are distinct."""
        # They should differ by more than 300
        diff = abs(float(C_PRIMARY) - float(C_COHERENCE))
        assert diff > 300


class TestSpectralLevels:
    """Test the spectral level analysis."""
    
    def test_analyze_spectral_levels_structure(self):
        """Test structure of spectral levels analysis."""
        levels = SpectralConstants.analyze_spectral_levels()
        
        # Check required keys
        assert "level_1" in levels
        assert "level_2" in levels
        assert "relationship" in levels
        assert "physical_analogy" in levels
    
    def test_level_1_properties(self):
        """Test Level 1 (Spectral Direct) properties."""
        levels = SpectralConstants.analyze_spectral_levels()
        level_1 = levels["level_1"]
        
        assert level_1["name"] == "Spectral Direct"
        assert level_1["constant"] == pytest.approx(629.83, abs=0.01)
        assert "structure" in level_1["interpretation"].lower()
    
    def test_level_2_properties(self):
        """Test Level 2 (Spectral Coherence) properties."""
        levels = SpectralConstants.analyze_spectral_levels()
        level_2 = levels["level_2"]
        
        assert level_2["name"] == "Spectral Coherence"
        assert level_2["constant"] == pytest.approx(244.36, abs=0.01)
        assert "form" in level_2["interpretation"].lower()
    
    def test_relationship_properties(self):
        """Test relationship between levels."""
        levels = SpectralConstants.analyze_spectral_levels()
        relationship = levels["relationship"]
        
        assert "ratio" in relationship
        assert relationship["ratio"] == pytest.approx(0.388, abs=0.001)


class TestF0Derivation:
    """Test derivation of f₀ = 141.7001 Hz from spectral constants."""
    
    def test_derive_f0_structure(self):
        """Test structure of f₀ derivation results."""
        result = SpectralConstants.derive_f0_from_spectral_constants()
        
        # Check required keys
        assert "C_primary" in result
        assert "C_coherence" in result
        assert "coherence_factor" in result
        assert "f_from_primary_hz" in result
        assert "f0_target_hz" in result
        assert "error_relative" in result
    
    def test_derive_f0_values(self):
        """Test values in f₀ derivation."""
        result = SpectralConstants.derive_f0_from_spectral_constants()
        
        assert result["C_primary"] == pytest.approx(629.83, abs=0.01)
        assert result["C_coherence"] == pytest.approx(244.36, abs=0.01)
        assert result["coherence_factor"] == pytest.approx(0.388, abs=0.001)
    
    def test_f0_derivation_accuracy(self):
        """Test that derived f₀ is close to 141.7001 Hz."""
        result = SpectralConstants.derive_f0_from_spectral_constants()
        
        # Error should be less than 1%
        assert result["error_relative"] < 0.01
        
        # Derived value should be close to target
        assert result["f_from_primary_hz"] == pytest.approx(141.7001, abs=1.0)
    
    def test_step_by_step_derivation(self):
        """Test step-by-step frequency construction."""
        result = SpectralConstants.derive_f0_from_spectral_constants()
        
        # f_base = 1/(2π) ≈ 0.159
        assert result["f_base_hz"] == pytest.approx(0.159, abs=0.01)
        
        # Each step should increase the frequency
        assert result["f_step1_hz"] > result["f_base_hz"]
        assert result["f_step2_hz"] > result["f_step1_hz"]
        # f3 is scaled by φ²/(2π) < 1, so it's smaller than f2
        assert result["f_step3_hz"] < result["f_step2_hz"]
        # Final multiplication by C_PRIMARY gives f₀
        assert result["f_from_primary_hz"] > 100


class TestValidation:
    """Test framework validation."""
    
    def test_validation_structure(self):
        """Test structure of validation results."""
        result = SpectralConstants.validate_dual_constant_framework()
        
        assert "framework" in result
        assert "validations" in result
        assert "all_valid" in result
        assert "overall_status" in result
    
    def test_all_validations_pass(self):
        """Test that all validations pass."""
        result = SpectralConstants.validate_dual_constant_framework()
        
        assert result["all_valid"] is True
        assert "VALIDATED" in result["overall_status"]
    
    def test_individual_validations(self):
        """Test individual validation results."""
        result = SpectralConstants.validate_dual_constant_framework()
        validations = result["validations"]
        
        # All validations should exist and pass
        assert "c_primary_from_lambda0" in validations
        assert validations["c_primary_from_lambda0"]["valid"] is True
        
        assert "c_coherence_from_moments" in validations
        assert validations["c_coherence_from_moments"]["valid"] is True
        
        assert "coherence_factor" in validations
        assert validations["coherence_factor"]["valid"] is True
        
        assert "f0_derivation" in validations
        assert validations["f0_derivation"]["valid"] is True


class TestExport:
    """Test export functionality."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        spec = SpectralConstants()
        data = spec.to_dict()
        
        # Check required fields
        assert "C_primary" in data
        assert "C_coherence" in data
        assert "coherence_factor" in data
        assert "lambda_0" in data
        assert "lambda_mean" in data
        assert "f0_hz" in data
    
    def test_to_dict_values(self):
        """Test values in exported dictionary."""
        spec = SpectralConstants()
        data = spec.to_dict()
        
        assert data["C_primary"] == pytest.approx(629.83, abs=0.01)
        assert data["C_coherence"] == pytest.approx(244.36, abs=0.01)
        assert data["f0_hz"] == pytest.approx(141.7001, abs=0.0001)


class TestPhysicalInterpretation:
    """Test physical interpretation of the dual-constant framework."""
    
    def test_structure_vs_form(self):
        """Test structure/form interpretation.
        
        C_PRIMARY represents STRUCTURE (local, from λ₀)
        C_COHERENCE represents FORM (global, from spectral distribution)
        """
        # C_PRIMARY > C_COHERENCE (structure > form)
        assert float(C_PRIMARY) > float(C_COHERENCE)
        
        # Both are positive
        assert float(C_PRIMARY) > 0
        assert float(C_COHERENCE) > 0
    
    def test_constants_coexist_without_contradiction(self):
        """Test that both constants coexist without contradiction.
        
        They describe two different levels of the same operator:
        - Level 1: Spectral Direct (λ₀ → C_PRIMARY)
        - Level 2: Spectral Coherence (second moment → C_COHERENCE)
        """
        levels = SpectralConstants.analyze_spectral_levels()
        
        # Both levels are defined
        assert levels["level_1"]["constant"] > 0
        assert levels["level_2"]["constant"] > 0
        
        # They represent different aspects
        assert levels["level_1"]["name"] != levels["level_2"]["name"]
        
        # The ratio between them is meaningful
        assert 0 < levels["relationship"]["ratio"] < 1
    
    def test_coherence_factor_meaning(self):
        """Test physical meaning of coherence factor.
        
        The coherence factor (≈0.388) modulates structure into form.
        """
        factor = float(COHERENCE_FACTOR)
        
        # Should be between 0 and 1
        assert 0 < factor < 1
        
        # Should be the exact ratio
        expected = float(C_COHERENCE) / float(C_PRIMARY)
        assert abs(factor - expected) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
