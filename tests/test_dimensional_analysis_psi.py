"""
Tests for dimensional analysis of Ψ = I · A_eff²

Validates that the formula is dimensionally consistent and follows
standard physics principles.
"""

import pytest
import sys
from pathlib import Path

# Add qcal to path
qcal_path = Path(__file__).parent.parent / 'qcal'
sys.path.insert(0, str(qcal_path))

from dimensional_analysis_psi import (
    DimensionalQuantity,
    validate_aeff_dimensionless,
    validate_psi_formula,
    validate_limit_behavior,
    compare_to_physics_coupling_factors,
    complete_dimensional_validation,
)


class TestDimensionalQuantity:
    """Test the DimensionalQuantity dataclass."""
    
    def test_dimensionless_quantity(self):
        """Test creation of dimensionless quantity."""
        A_eff = DimensionalQuantity(0.92, "1", "A_eff")
        assert A_eff.is_dimensionless()
        assert A_eff.value == 0.92
        assert A_eff.dimensions == "1"
    
    def test_dimensional_quantity(self):
        """Test creation of dimensional quantity."""
        I = DimensionalQuantity(10.0, "bits", "I")
        assert not I.is_dimensionless()
        assert I.value == 10.0
        assert I.dimensions == "bits"
    
    def test_multiplication_dimensionless(self):
        """Test multiplying two dimensionless quantities."""
        a = DimensionalQuantity(2.0, "1", "a")
        b = DimensionalQuantity(3.0, "1", "b")
        c = a * b
        
        assert c.value == 6.0
        assert c.is_dimensionless()
    
    def test_multiplication_mixed(self):
        """Test multiplying dimensional and dimensionless quantities."""
        I = DimensionalQuantity(10.0, "bits", "I")
        A_eff = DimensionalQuantity(0.92, "1", "A_eff")
        Psi = I * A_eff
        
        assert Psi.value == pytest.approx(9.2)
        assert "bits" in Psi.dimensions
    
    def test_power_operation(self):
        """Test raising to a power."""
        A_eff = DimensionalQuantity(0.92, "1", "A_eff")
        A_eff_squared = A_eff ** 2
        
        assert A_eff_squared.value == pytest.approx(0.8464)
        assert A_eff_squared.is_dimensionless()


class TestAeffValidation:
    """Test validation of A_eff as dimensionless."""
    
    def test_valid_aeff(self):
        """Test A_eff in valid range [0, 1]."""
        result = validate_aeff_dimensionless(0.92)
        
        assert result['is_dimensionless']
        assert result['is_ratio']
        assert result['in_valid_range']
        assert result['dimensions'] == '1 (dimensionless)'
    
    def test_aeff_at_zero(self):
        """Test A_eff at zero (minimum effectiveness)."""
        result = validate_aeff_dimensionless(0.0)
        
        assert result['is_dimensionless']
        assert result['in_valid_range']
    
    def test_aeff_at_one(self):
        """Test A_eff at one (perfect effectiveness)."""
        result = validate_aeff_dimensionless(1.0)
        
        assert result['is_dimensionless']
        assert result['in_valid_range']
    
    def test_aeff_outside_range(self):
        """Test A_eff outside typical range [0, 1]."""
        result = validate_aeff_dimensionless(1.5)
        
        assert result['is_dimensionless']  # Still dimensionless
        assert not result['in_valid_range']
        assert 'warning' in result
    
    def test_proof_structure(self):
        """Test that proof is included."""
        result = validate_aeff_dimensionless(0.92)
        
        assert 'proof' in result
        assert len(result['proof']) > 0
        assert any('dimensionless' in line for line in result['proof'])


class TestPsiFormulaValidation:
    """Test dimensional validation of Ψ = I · A_eff²."""
    
    def test_basic_formula_validation(self):
        """Test basic formula with standard values."""
        result = validate_psi_formula(I=10.0, A_eff=0.92, I_dimensions="bits")
        
        assert result['dimensionally_consistent']
        assert result['A_eff_is_dimensionless']
        assert result['Psi_has_same_dims_as_I']
        assert result['Psi_value'] == pytest.approx(8.464)
    
    def test_psi_dimensions_match_I(self):
        """Test that Ψ has same dimensions as I."""
        result = validate_psi_formula(I=10.0, A_eff=0.92, I_dimensions="bits")
        
        assert result['Psi_dimensions'] == "bits"
    
    def test_different_I_dimensions(self):
        """Test with different dimensional units for I."""
        result = validate_psi_formula(I=5.0, A_eff=0.8, I_dimensions="nats")
        
        assert result['dimensionally_consistent']
        assert result['Psi_dimensions'] == "nats"
    
    def test_proof_included(self):
        """Test that dimensional proof is included."""
        result = validate_psi_formula(I=10.0, A_eff=0.92)
        
        assert 'dimensional_proof' in result
        assert len(result['dimensional_proof']) > 0
        assert any('NO DIMENSIONAL BREAKING' in line for line in result['dimensional_proof'])
    
    def test_aeff_equals_one(self):
        """Test special case where A_eff = 1."""
        result = validate_psi_formula(I=10.0, A_eff=1.0)
        
        assert result['Psi_value'] == pytest.approx(10.0)
        assert result['dimensionally_consistent']
    
    def test_aeff_equals_zero(self):
        """Test special case where A_eff = 0."""
        result = validate_psi_formula(I=10.0, A_eff=0.0)
        
        assert result['Psi_value'] == pytest.approx(0.0)
        assert result['dimensionally_consistent']


class TestLimitBehavior:
    """Test limit behavior: As A_eff → 1, Ψ → I."""
    
    def test_limit_convergence(self):
        """Test that Ψ converges to I as A_eff → 1."""
        result = validate_limit_behavior(I=10.0)
        
        assert result['converges_to_I']
        assert result['Psi_at_Aeff_1'] == pytest.approx(10.0)
    
    def test_monotonic_increase(self):
        """Test that Ψ increases monotonically as A_eff → 1."""
        result = validate_limit_behavior(I=10.0)
        
        # Check that Ψ increases as A_eff increases
        psi_values = [point['Psi'] for point in result['limit_points']]
        
        for i in range(len(psi_values) - 1):
            assert psi_values[i] <= psi_values[i + 1]
    
    def test_ratio_approaches_one(self):
        """Test that Ψ/I approaches 1 as A_eff → 1."""
        result = validate_limit_behavior(I=10.0)
        
        # Last point should have A_eff = 1.0
        last_point = result['limit_points'][-1]
        assert last_point['A_eff'] == 1.0
        assert last_point['ratio_Psi_over_I'] == pytest.approx(1.0)
    
    def test_perfect_effectiveness(self):
        """Test that perfect effectiveness (A_eff=1) gives Ψ=I."""
        result = validate_limit_behavior(I=15.0)
        
        # Find the point where A_eff = 1.0
        perfect_point = [p for p in result['limit_points'] if p['A_eff'] == 1.0][0]
        
        assert perfect_point['Psi'] == pytest.approx(15.0)
        assert perfect_point['I - Psi'] == pytest.approx(0.0)
    
    def test_proof_included(self):
        """Test that limit proof is included."""
        result = validate_limit_behavior(I=10.0)
        
        assert 'limit_proof' in result
        assert any('VERIFIED' in line for line in result['limit_proof'])


class TestPhysicsComparison:
    """Test comparison to standard physics coupling factors."""
    
    def test_coupling_factors_included(self):
        """Test that standard physics coupling factors are included."""
        result = compare_to_physics_coupling_factors()
        
        assert 'fine_structure_alpha' in result['examples']
        assert 'strong_coupling_alpha_s' in result['examples']
        assert 'weak_coupling_g' in result['examples']
        assert 'higgs_self_coupling_lambda' in result['examples']
    
    def test_all_dimensionless(self):
        """Test that all physics coupling factors are dimensionless."""
        result = compare_to_physics_coupling_factors()
        
        for name, factor in result['examples'].items():
            assert factor['dimensionless']
    
    def test_analogies_to_aeff(self):
        """Test that analogies to A_eff are provided."""
        result = compare_to_physics_coupling_factors()
        
        for name, factor in result['examples'].items():
            assert 'analogy_to_Aeff' in factor
            assert 'Modulates' in factor['analogy_to_Aeff']
    
    def test_conclusion_present(self):
        """Test that conclusion about standard physics is present."""
        result = compare_to_physics_coupling_factors()
        
        assert 'conclusion' in result
        assert any('STANDARD' in line for line in result['conclusion'])
        assert any('NO dimensional breaking' in line for line in result['conclusion'])


class TestCompleteValidation:
    """Test complete dimensional validation."""
    
    def test_all_components_present(self):
        """Test that all validation components are present."""
        result = complete_dimensional_validation(I=10.0, A_eff=0.92)
        
        assert 'aeff_validation' in result
        assert 'psi_formula_validation' in result
        assert 'limit_behavior' in result
        assert 'physics_comparison' in result
        assert 'problem_solved' in result
        assert 'conclusion' in result
    
    def test_problem_solved(self):
        """Test that problem is marked as solved."""
        result = complete_dimensional_validation(I=10.0, A_eff=0.92)
        
        assert result['problem_solved']
    
    def test_conclusion_format(self):
        """Test that conclusion is properly formatted."""
        result = complete_dimensional_validation(I=10.0, A_eff=0.92)
        
        conclusion = result['conclusion']
        assert len(conclusion) > 0
        assert any('PROBLEMA RESUELTO' in line for line in conclusion)
        assert any('NO HAY RUPTURA DIMENSIONAL' in line for line in conclusion)
    
    def test_with_different_values(self):
        """Test validation with different I and A_eff values."""
        test_cases = [
            (5.0, 0.5),
            (10.0, 0.8),
            (15.0, 0.95),
            (20.0, 1.0),
        ]
        
        for I, A_eff in test_cases:
            result = complete_dimensional_validation(I=I, A_eff=A_eff)
            assert result['problem_solved']
    
    def test_reproducibility(self):
        """Test that validation is reproducible."""
        result1 = complete_dimensional_validation(I=10.0, A_eff=0.92)
        result2 = complete_dimensional_validation(I=10.0, A_eff=0.92)
        
        assert result1['problem_solved'] == result2['problem_solved']
        assert result1['psi_formula_validation']['Psi_value'] == \
               result2['psi_formula_validation']['Psi_value']


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_information(self):
        """Test with I = 0."""
        result = validate_psi_formula(I=0.0, A_eff=0.92)
        
        assert result['Psi_value'] == pytest.approx(0.0)
        assert result['dimensionally_consistent']
    
    def test_zero_effectiveness(self):
        """Test with A_eff = 0."""
        result = validate_psi_formula(I=10.0, A_eff=0.0)
        
        assert result['Psi_value'] == pytest.approx(0.0)
        assert result['dimensionally_consistent']
    
    def test_large_values(self):
        """Test with large values."""
        result = validate_psi_formula(I=1000.0, A_eff=0.99)
        
        assert result['dimensionally_consistent']
        assert result['Psi_value'] == pytest.approx(980.1, rel=1e-3)
    
    def test_small_effectiveness(self):
        """Test with very small A_eff."""
        result = validate_psi_formula(I=10.0, A_eff=0.01)
        
        assert result['dimensionally_consistent']
        assert result['Psi_value'] == pytest.approx(0.001)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
