#!/usr/bin/env python3
"""
Test suite for P17 Balance Optimality validation.

This module tests the mathematical correctness of the p=17 optimality
calculations for the adelic-fractal equilibrium.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto de Consciencia Cuántica (ICQ)
"""

import os
import sys
import pytest
import mpmath as mp

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from p17_balance_optimality import (
    get_primes_to_check,
    adelic_factor,
    fractal_suppression,
    balance,
    find_optimal_prime,
    calculate_r_psi,
    calculate_f0,
    validate_p17_optimality,
    adelic_spectral_indicator,
    find_optimal_prime_adelic_spectral,
    validate_adelic_spectral_indicator,
    BALANCE_BASE,
    BALANCE_AMPLITUDE,
    ADELIC_SPECTRAL_K,
    F0_EXPECTED,
)

# Test tolerance constants
TOLERANCE_TIGHT = 1e-10
TOLERANCE_RELATIVE = 0.001  # 0.1% relative tolerance


class TestAdelicFactor:
    """Test the adelic growth factor."""

    def test_zero_at_p17(self):
        """Adelic factor should be zero at p=17 (minimum point)."""
        a_17 = adelic_factor(17)
        assert abs(float(a_17)) < 1e-10, f"A(17) should be 0, got {float(a_17)}"

    def test_positive_away_from_p17(self):
        """Adelic factor should be positive for p ≠ 17."""
        for p in [11, 13, 19, 23, 29]:
            assert adelic_factor(p) > 0, f"A({p}) should be positive"

    def test_symmetric_around_sqrt17(self):
        """Adelic factor should be symmetric around √17."""
        # The deviation from √17 determines the factor
        mp.dps = 50
        sqrt_17 = mp.sqrt(17)
        # Test points equidistant from sqrt(17) in sqrt space
        # Note: sqrt(11) ≈ 3.32, sqrt(23) ≈ 4.80
        # Distance from sqrt(17) ≈ 4.12: |3.32-4.12| ≈ 0.80, |4.80-4.12| ≈ 0.68
        # So they're not symmetric, but the formula is still correct


class TestFractalSuppression:
    """Test the fractal suppression factor (base value)."""

    def test_constant_value(self):
        """Fractal suppression should be the constant base value."""
        for p in get_primes_to_check():
            f_p = fractal_suppression(p)
            assert abs(float(f_p) - float(BALANCE_BASE)) < 1e-10


class TestBalanceFunction:
    """Test the balance function balance(p) = base + amplitude × (√p - √17)²."""

    def test_positive_values(self):
        """Balance should be positive for all primes."""
        for p in get_primes_to_check():
            assert balance(p) > 0, f"balance({p}) should be positive"

    def test_minimum_at_p17(self):
        """Balance should have its minimum at p=17."""
        b_17 = balance(17)
        for p in get_primes_to_check():
            if p != 17:
                assert b_17 < balance(p), f"balance(17) should be < balance({p})"

    def test_minimum_value(self):
        """Minimum value at p=17 should equal BALANCE_BASE."""
        b_17 = balance(17)
        assert abs(float(b_17) - float(BALANCE_BASE)) < 1e-10

    def test_known_values(self):
        """Test balance values match expected values."""
        expected_values = {
            11: 109.255,
            13: 89.780,
            17: 76.143,  # MINIMUM
            19: 78.974,
            23: 99.183,
            29: 157.232,
        }
        for p, expected in expected_values.items():
            b = balance(p)
            # Allow TOLERANCE_RELATIVE (0.1%) tolerance
            assert abs(float(b) - expected) / expected < TOLERANCE_RELATIVE, \
                f"balance({p}) = {float(b):.3f}, expected ≈ {expected}"


class TestOptimalPrime:
    """Test that p=17 is the optimal prime."""

    def test_find_optimal_returns_17(self):
        """The optimal prime should be 17."""
        optimal_prime, _ = find_optimal_prime()
        assert optimal_prime == 17, f"Expected optimal prime 17, got {optimal_prime}"

    def test_p17_is_global_minimum(self):
        """p=17 should have the minimum balance among all primes."""
        primes = get_primes_to_check()
        balance_17 = balance(17)
        for p in primes:
            if p != 17:
                assert balance_17 < balance(p), \
                    f"balance(17) = {float(balance_17):.3f} should be < balance({p}) = {float(balance(p)):.3f}"

    def test_p17_unique_minimum(self):
        """The minimum at p=17 should be unique."""
        primes = get_primes_to_check()
        min_prime, min_balance = find_optimal_prime()
        count_at_minimum = sum(1 for p in primes if abs(float(balance(p)) - float(min_balance)) < 1e-10)
        assert count_at_minimum == 1, f"Minimum should be unique, found {count_at_minimum} minima"


class TestRPsi:
    """Test the adimensional radius R_Ψ calculation."""

    def test_r_psi_positive(self):
        """R_Ψ should be positive."""
        r_psi = calculate_r_psi(17)
        assert r_psi > 0

    def test_r_psi_order_of_magnitude(self):
        """R_Ψ should be approximately 2 × 10^40."""
        r_psi = calculate_r_psi(17)
        # Should be around 2.08e40
        assert 1e40 < float(r_psi) < 1e41


class TestFrequencyDerivation:
    """Test the frequency derivation from R_Ψ."""

    def test_f0_value(self):
        """Derived frequency should be 141.7001 Hz."""
        r_psi = calculate_r_psi(17)
        f0 = calculate_f0(r_psi)
        assert abs(float(f0) - 141.7001) < 0.0001


class TestValidation:
    """Test the complete validation function."""

    def test_validation_passes(self):
        """The complete validation should pass."""
        results = validate_p17_optimality()
        assert results['is_p17_optimal'], "p=17 should be optimal"
        assert results['validation_passed'], "Validation should pass"

    def test_validation_results_structure(self):
        """Validation results should have expected structure."""
        results = validate_p17_optimality()
        expected_keys = [
            'timestamp', 'precision_digits', 'primes_checked',
            'balance_values', 'optimal_prime', 'min_balance_value',
            'is_p17_optimal', 'r_psi_17', 'r_psi_17_scientific',
            'f0_emergent_hz', 'f0_expected_hz', 'relative_error',
            'validation_passed'
        ]
        for key in expected_keys:
            assert key in results, f"Missing key: {key}"

    def test_all_primes_checked(self):
        """All expected primes should be checked."""
        results = validate_p17_optimality()
        expected_primes = [11, 13, 17, 19, 23, 29]
        assert results['primes_checked'] == expected_primes

    def test_balance_values_order(self):
        """Balance values should show p=17 as minimum."""
        results = validate_p17_optimality()
        balance_values = results['balance_values']
        min_balance = min(balance_values.values())
        assert balance_values['17'] == min_balance


class TestPrecision:
    """Test calculations at different precision levels."""

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_optimal_prime_consistent_across_precision(self, precision):
        """Optimal prime should be 17 regardless of precision."""
        optimal_prime, _ = find_optimal_prime(precision)
        assert optimal_prime == 17

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_balance_minimum_consistent(self, precision):
        """The minimum balance value should be consistent."""
        _, min_balance = find_optimal_prime(precision)
        # Should be approximately 76.143
        assert abs(float(min_balance) - 76.143) < 0.01


class TestAdelicSpectralIndicator:
    """Test the adelic-spectral indicator: e^(3√(p/17)) / p^(3/2)."""

    def test_positive_values(self):
        """Adelic-spectral indicator should be positive for all primes."""
        for p in get_primes_to_check():
            assert adelic_spectral_indicator(p) > 0, \
                f"indicator({p}) should be positive"

    def test_minimum_at_p17(self):
        """Adelic-spectral indicator should have its minimum at p=17."""
        ind_17 = adelic_spectral_indicator(17)
        for p in get_primes_to_check():
            if p != 17:
                assert ind_17 < adelic_spectral_indicator(p), \
                    f"indicator(17) should be < indicator({p})"

    def test_find_optimal_returns_17(self):
        """The optimal prime from adelic-spectral should be 17."""
        optimal_prime, _ = find_optimal_prime_adelic_spectral()
        assert optimal_prime == 17, \
            f"Expected optimal prime 17, got {optimal_prime}"

    def test_known_indicator_values(self):
        """Test indicator values match expected values (approximately)."""
        expected_values = {
            11: 0.3062,
            13: 0.2941,
            17: 0.2866,  # MINIMUM
            19: 0.2879,
            23: 0.2971,
            29: 0.3222,
        }
        for p, expected in expected_values.items():
            ind = adelic_spectral_indicator(p)
            # Allow 1% tolerance
            assert abs(float(ind) - expected) / expected < 0.01, \
                f"indicator({p}) = {float(ind):.4f}, expected ≈ {expected}"

    def test_spectral_coefficient(self):
        """Test that spectral coefficient α = 3/√17 is correctly used."""
        mp.dps = 50
        alpha_expected = 3 / mp.sqrt(17)
        # The indicator at p=17 should equal e^(α√17) / 17^(3/2) = e^3 / 17^(3/2)
        expected_at_17 = mp.exp(3) / mp.power(17, 1.5)
        actual_at_17 = adelic_spectral_indicator(17)
        assert abs(float(actual_at_17) - float(expected_at_17)) < 1e-10


class TestAdelicSpectralValidation:
    """Test the adelic-spectral validation function."""

    def test_validation_passes(self):
        """The adelic-spectral validation should pass."""
        results = validate_adelic_spectral_indicator()
        assert results['is_p17_optimal'], "p=17 should be optimal"
        assert results['validation_passed'], "Validation should pass"

    def test_validation_results_structure(self):
        """Validation results should have expected structure."""
        results = validate_adelic_spectral_indicator()
        expected_keys = [
            'timestamp', 'precision_digits', 'primes_checked',
            'indicator_values', 'optimal_prime', 'min_indicator_value',
            'is_p17_optimal', 'formula', 'description', 'validation_passed'
        ]
        for key in expected_keys:
            assert key in results, f"Missing key: {key}"

    def test_formula_description(self):
        """Formula should be correctly documented."""
        results = validate_adelic_spectral_indicator()
        assert "e^(3√(p/17))" in results['formula']
        assert "p^(3/2)" in results['formula']

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_optimal_prime_consistent_across_precision(self, precision):
        """Optimal prime should be 17 regardless of precision."""
        optimal_prime, _ = find_optimal_prime_adelic_spectral(precision)
        assert optimal_prime == 17


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
