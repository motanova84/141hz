#!/usr/bin/env python3
"""
Tests for the explicit function f(h₁₁, h₂₁) → κ_Π
===================================================

This test suite verifies the correct implementation of the explicit function
that calculates κ_Π from Hodge numbers.

Author: JMMB Ψ✧
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kappa_pi_function import (
    kappa_pi_function,
    kappa_pi_ideal,
    kappa_pi_from_alpha_beta,
    compute_alpha,
    compute_beta,
    compute_alpha_beta,
    differential_entropy,
    compute_normalization,
    density_function,
    verify_function_f,
    get_universal_kappa_pi,
    find_ideal_hodge_numbers,
    analyze_kappa_variation,
    KAPPA_PI_UNIVERSAL,
    ALPHA_IDEAL,
    BETA_IDEAL,
    A_CONSTANT,
    B_CONSTANT,
)


class TestParameterFunctions:
    """Test α and β parameter computation from Hodge numbers."""
    
    def test_compute_alpha_basic(self):
        """Test basic α computation."""
        # For h11=1, h21=1: α = 0.45 * 1/2 = 0.225
        alpha = compute_alpha(1, 1)
        assert abs(alpha - 0.225) < 1e-10
    
    def test_compute_beta_basic(self):
        """Test basic β computation."""
        # For h11=1, h21=1: β = 0.28 * 1/2 = 0.14
        beta = compute_beta(1, 1)
        assert abs(beta - 0.14) < 1e-10
    
    def test_compute_alpha_beta_quintic(self):
        """Test α, β for quintic CY (h11=1, h21=101)."""
        alpha, beta = compute_alpha_beta(1, 101)
        # α = 0.45 * 1/102 ≈ 0.00441
        # β = 0.28 * 101/102 ≈ 0.27725
        assert 0.004 < alpha < 0.005
        assert 0.27 < beta < 0.28
    
    def test_alpha_beta_sum_property(self):
        """Test that α/A + β/B ≈ 1 when A and B are properly scaled."""
        h11, h21 = 10, 90
        alpha = compute_alpha(h11, h21)
        beta = compute_beta(h11, h21)
        
        # α/A + β/B should equal (h11 + h21)/(h11 + h21) = 1
        ratio_sum = alpha / A_CONSTANT + beta / B_CONSTANT
        assert abs(ratio_sum - 1.0) < 1e-10
    
    def test_zero_hodge_raises_error(self):
        """Test that zero total Hodge numbers raise an error."""
        with pytest.raises(ValueError):
            compute_alpha(0, 0)
        with pytest.raises(ValueError):
            compute_beta(0, 0)
    
    def test_alpha_beta_range(self):
        """Test that α and β are in reasonable ranges."""
        for h11 in [1, 5, 10]:
            for h21 in [20, 50, 100, 200]:
                alpha, beta = compute_alpha_beta(h11, h21)
                # α and β should be positive and less than their constants
                assert 0 < alpha <= A_CONSTANT
                assert 0 < beta <= B_CONSTANT


class TestDensityAndNormalization:
    """Test density function and normalization."""
    
    def test_normalization_positive(self):
        """Test that normalization Z is always positive."""
        for alpha in [0.1, 0.3, 0.5]:
            for beta in [0.1, 0.2, 0.3]:
                Z = compute_normalization(alpha, beta)
                assert Z > 0
    
    def test_density_integrates_to_one(self):
        """Test that density integrates to 1."""
        from scipy import integrate
        
        alpha, beta = 0.385, 0.244
        Z = compute_normalization(alpha, beta)
        
        def rho(theta):
            return density_function(theta, alpha, beta, Z)
        
        integral, _ = integrate.quad(rho, -np.pi, np.pi)
        assert abs(integral - 1.0) < 1e-6
    
    def test_density_non_negative(self):
        """Test that density is non-negative everywhere."""
        alpha, beta = 0.385, 0.244
        Z = compute_normalization(alpha, beta)
        
        theta_values = np.linspace(-np.pi, np.pi, 1000)
        rho_values = density_function(theta_values, alpha, beta, Z)
        
        assert np.all(rho_values >= 0)
    
    def test_density_symmetric_for_zero_beta(self):
        """Test that density is symmetric when β=0."""
        alpha, beta = 0.3, 0.0
        Z = compute_normalization(alpha, beta)
        
        theta = np.array([0.5, -0.5])
        rho = density_function(theta, alpha, beta, Z)
        
        # Should be equal due to cos symmetry
        assert abs(rho[0] - rho[1]) < 1e-10


class TestEntropyCalculation:
    """Test differential entropy calculation."""
    
    def test_entropy_positive(self):
        """Test that entropy is positive."""
        alpha, beta = 0.385, 0.244
        H = differential_entropy(alpha, beta)
        assert H > 0
    
    def test_entropy_bounded(self):
        """Test that entropy is in reasonable range."""
        # For a continuous distribution on [-π, π], entropy should be
        # roughly log(2π) ≈ 1.84 for uniform, and can be higher
        alpha, beta = 0.385, 0.244
        H = differential_entropy(alpha, beta)
        assert 0 < H < 5.0  # Reasonable upper bound
    
    def test_entropy_ideal_parameters(self):
        """Test entropy for ideal α, β gives κ_Π ≈ 2.5773."""
        H = differential_entropy(ALPHA_IDEAL, BETA_IDEAL)
        assert abs(H - KAPPA_PI_UNIVERSAL) < 0.01
    
    def test_entropy_varies_with_parameters(self):
        """Test that entropy changes with α and β."""
        H1 = differential_entropy(0.1, 0.1)
        H2 = differential_entropy(0.3, 0.2)
        H3 = differential_entropy(0.5, 0.3)
        
        # Entropies should be different
        assert not np.allclose([H1, H2, H3], H1)


class TestKappaPiFunction:
    """Test the main κ_Π function."""
    
    def test_kappa_pi_ideal(self):
        """Test ideal κ_Π value."""
        kappa = kappa_pi_ideal()
        assert abs(kappa - KAPPA_PI_UNIVERSAL) < 0.01
    
    def test_kappa_pi_from_alpha_beta(self):
        """Test direct computation from α, β."""
        kappa = kappa_pi_from_alpha_beta(ALPHA_IDEAL, BETA_IDEAL)
        assert abs(kappa - KAPPA_PI_UNIVERSAL) < 0.01
    
    def test_kappa_pi_function_quintic(self):
        """Test κ_Π for quintic CY."""
        kappa = kappa_pi_function(1, 101)
        # Should be < universal value due to non-ideal α, β
        assert kappa < KAPPA_PI_UNIVERSAL
        assert 1.5 < kappa < 3.0
    
    def test_kappa_pi_function_various_hodge(self):
        """Test κ_Π for various Hodge numbers."""
        test_cases = [
            (1, 20),
            (1, 50),
            (1, 101),
            (1, 150),
            (5, 100),
            (10, 90),
        ]
        
        for h11, h21 in test_cases:
            kappa = kappa_pi_function(h11, h21)
            # All should be positive and in reasonable range
            assert 1.0 < kappa < 3.5
            # All should be ≤ universal value (with some numerical tolerance)
            assert kappa <= KAPPA_PI_UNIVERSAL + 0.5
    
    def test_kappa_pi_function_return_details(self):
        """Test detailed return format."""
        result = kappa_pi_function(1, 101, return_details=True)
        
        assert 'kappa_pi' in result
        assert 'h11' in result
        assert 'h21' in result
        assert 'alpha' in result
        assert 'beta' in result
        assert 'Z' in result
        
        assert result['h11'] == 1
        assert result['h21'] == 101
        assert result['kappa_pi'] > 0
    
    def test_kappa_pi_continuous(self):
        """Test that κ_Π varies continuously with h21."""
        h21_values = np.linspace(50, 150, 10)
        kappa_values = [kappa_pi_function(1, h21) for h21 in h21_values]
        
        # Check no sudden jumps
        diffs = np.diff(kappa_values)
        assert np.all(np.abs(diffs) < 0.5)  # No jump larger than 0.5


class TestCalibration:
    """Test calibration and analysis functions."""
    
    def test_find_ideal_hodge_numbers(self):
        """Test finding Hodge numbers for ideal α, β."""
        h11, h21 = find_ideal_hodge_numbers()
        
        # Compute α, β from these
        alpha = compute_alpha(h11, h21)
        beta = compute_beta(h11, h21)
        
        # Should match ideal values
        assert abs(alpha - ALPHA_IDEAL) < 1e-6
        assert abs(beta - BETA_IDEAL) < 1e-6
    
    def test_analyze_kappa_variation(self):
        """Test variation analysis."""
        h21_range = np.array([20, 50, 101, 150])
        result = analyze_kappa_variation(h21_range, h11=1)
        
        assert 'kappa_values' in result
        assert 'alpha_values' in result
        assert 'beta_values' in result
        assert 'mean_kappa' in result
        assert 'std_kappa' in result
        
        assert len(result['kappa_values']) == len(h21_range)
        assert result['mean_kappa'] > 0


class TestVerification:
    """Test verification functions."""
    
    def test_verify_function_f(self):
        """Test overall verification."""
        result = verify_function_f()
        
        assert 'verification_passed' in result
        assert 'ideal_kappa' in result
        assert 'quintic_kappa' in result
        assert 'test_cases' in result
        
        # Verification should pass
        assert result['verification_passed'] is True
    
    def test_get_universal_kappa_pi(self):
        """Test universal constant getter."""
        kappa = get_universal_kappa_pi()
        assert kappa == KAPPA_PI_UNIVERSAL


class TestMathematicalProperties:
    """Test mathematical properties of the function."""
    
    def test_entropy_maximum_at_ideal(self):
        """Test that ideal α, β give maximum (or near-maximum) entropy."""
        # Compute κ_Π for ideal and several other parameter combinations
        kappa_ideal = kappa_pi_from_alpha_beta(ALPHA_IDEAL, BETA_IDEAL)
        
        # Test nearby values
        test_alphas = [ALPHA_IDEAL - 0.05, ALPHA_IDEAL, ALPHA_IDEAL + 0.05]
        test_betas = [BETA_IDEAL - 0.05, BETA_IDEAL, BETA_IDEAL + 0.05]
        
        for alpha in test_alphas:
            for beta in test_betas:
                if alpha > 0 and beta > 0:
                    kappa = kappa_pi_from_alpha_beta(alpha, beta)
                    # Ideal should be close to maximum
                    # (allowing some tolerance for numerical effects)
                    assert kappa <= kappa_ideal + 0.1
    
    def test_kappa_symmetry_property(self):
        """Test expected symmetry properties."""
        # For equal h11 and h21, α and β should have ratio A/B
        h = 50
        alpha, beta = compute_alpha_beta(h, h)
        
        ratio = alpha / beta
        expected_ratio = A_CONSTANT / B_CONSTANT
        
        assert abs(ratio - expected_ratio) < 1e-10
    
    def test_limiting_behavior_large_h21(self):
        """Test behavior when h21 >> h11."""
        # When h21 >> h11, β should dominate
        alpha1, beta1 = compute_alpha_beta(1, 100)
        alpha2, beta2 = compute_alpha_beta(1, 1000)
        
        # α should decrease, β should approach B_CONSTANT
        assert alpha2 < alpha1
        assert beta2 > beta1
        assert beta2 < B_CONSTANT
    
    def test_limiting_behavior_large_h11(self):
        """Test behavior when h11 >> h21."""
        # When h11 >> h21, α should dominate
        alpha1, beta1 = compute_alpha_beta(100, 1)
        alpha2, beta2 = compute_alpha_beta(1000, 1)
        
        # β should decrease, α should approach A_CONSTANT
        assert beta2 < beta1
        assert alpha2 > alpha1
        assert alpha2 < A_CONSTANT


class TestNumericalStability:
    """Test numerical stability and edge cases."""
    
    def test_small_hodge_numbers(self):
        """Test with small Hodge numbers."""
        kappa = kappa_pi_function(1, 1)
        assert np.isfinite(kappa)
        assert kappa > 0
    
    def test_large_hodge_numbers(self):
        """Test with large Hodge numbers."""
        kappa = kappa_pi_function(100, 1000)
        assert np.isfinite(kappa)
        assert kappa > 0
    
    def test_extreme_ratio(self):
        """Test with extreme h11/h21 ratios."""
        # Very small h11
        kappa1 = kappa_pi_function(1, 500)
        assert np.isfinite(kappa1)
        
        # Very small h21
        kappa2 = kappa_pi_function(500, 1)
        assert np.isfinite(kappa2)
    
    def test_reproducibility(self):
        """Test that function gives same results on repeated calls."""
        kappa1 = kappa_pi_function(1, 101)
        kappa2 = kappa_pi_function(1, 101)
        
        assert kappa1 == kappa2


class TestDocumentation:
    """Test that documentation examples work."""
    
    def test_readme_example(self):
        """Test example from module docstring."""
        # For quintic CY with h11=1, h21=101
        kappa = kappa_pi_function(1, 101)
        assert isinstance(kappa, float)
        assert kappa > 0
    
    def test_detailed_output_example(self):
        """Test detailed output example."""
        result = kappa_pi_function(1, 101, return_details=True)
        assert isinstance(result, dict)
        assert 'kappa_pi' in result
        assert 'alpha' in result
        assert 'beta' in result


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
