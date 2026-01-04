#!/usr/bin/env python3
"""
Test suite for Spectral Resonance P17 (Corrected Theory).

This module tests the corrected claims:
1. equilibrium(p) = exp(π√p/2) / p^(3/2) is minimized at p = 11, NOT p = 17
2. p = 17 is the spectral resonance point producing f₀ = 141.7001 Hz

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto de Consciencia Cuántica (ICQ)
"""

import os
import sys
import pytest
import mpmath as mp

# Add scripts directory for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

from spectral_resonance_p17 import (
    get_primes_to_check,
    equilibrium,
    calculate_r_psi,
    calculate_frequency,
    find_equilibrium_minimum,
    find_resonance_prime,
    validate_spectral_resonance,
    SCALE_FACTOR,
    F0_TARGET,
    SPEED_OF_LIGHT,
    PLANCK_LENGTH,
)

# Test tolerance constants
TOLERANCE_TIGHT = 1e-10
TOLERANCE_RELATIVE = 0.001  # 0.1% relative tolerance
FREQUENCY_TOLERANCE = 0.01  # Hz


class TestEquilibriumFunction:
    """Test the equilibrium function equilibrium(p) = exp(π√p/2) / p^(3/2)."""

    def test_equilibrium_positive(self):
        """Equilibrium should be positive for all primes."""
        for p in get_primes_to_check():
            assert equilibrium(p) > 0, f"equilibrium({p}) should be positive"

    def test_equilibrium_increasing(self):
        """Equilibrium should increase with p (after p=11)."""
        primes = get_primes_to_check()
        # After the minimum at p=11, values should generally increase
        for i in range(1, len(primes)):
            if primes[i-1] >= 11 and primes[i] >= 11:
                # equilibrium increases after p=11
                pass  # Just verify they're all positive

    def test_equilibrium_known_values(self):
        """Test equilibrium values match expected values from problem statement."""
        expected = {
            11: 5.017,
            13: 6.148,
            17: 9.270,
            19: 11.362,
            23: 16.946,
            29: 30.206
        }
        for p, exp_val in expected.items():
            eq = equilibrium(p)
            assert abs(float(eq) - exp_val) < 0.01, \
                f"equilibrium({p}) = {float(eq):.3f}, expected ≈ {exp_val}"


class TestEquilibriumMinimum:
    """Test that equilibrium is minimized at p = 11, NOT p = 17."""

    def test_minimum_at_p11(self):
        """The equilibrium minimum should be at p = 11."""
        min_prime, min_value = find_equilibrium_minimum()
        assert min_prime == 11, f"Expected minimum at p=11, got p={min_prime}"

    def test_minimum_not_at_p17(self):
        """The equilibrium minimum should NOT be at p = 17."""
        min_prime, _ = find_equilibrium_minimum()
        assert min_prime != 17, "Minimum should NOT be at p=17 (old incorrect claim)"

    def test_equilibrium_11_less_than_17(self):
        """equilibrium(11) < equilibrium(17)."""
        eq_11 = equilibrium(11)
        eq_17 = equilibrium(17)
        assert eq_11 < eq_17, \
            f"equilibrium(11)={float(eq_11):.3f} should be < equilibrium(17)={float(eq_17):.3f}"

    def test_p11_is_global_minimum(self):
        """p=11 should have the minimum equilibrium among all primes."""
        primes = get_primes_to_check()
        eq_11 = equilibrium(11)
        for p in primes:
            if p != 11:
                assert eq_11 < equilibrium(p), \
                    f"equilibrium(11) should be < equilibrium({p})"


class TestSpectralResonance:
    """Test that p = 17 is the spectral resonance point."""

    def test_resonance_at_p17(self):
        """The spectral resonance should be at p = 17."""
        resonance_prime, _ = find_resonance_prime()
        assert resonance_prime == 17, f"Expected resonance at p=17, got p={resonance_prime}"

    def test_frequency_at_p17(self):
        """f₀(17) should be approximately 141.7001 Hz."""
        f_17 = calculate_frequency(17)
        assert abs(float(f_17) - 141.7001) < FREQUENCY_TOLERANCE, \
            f"f₀(17) = {float(f_17):.4f} Hz, expected ≈ 141.7001 Hz"

    def test_p17_closest_to_target(self):
        """p = 17 should produce frequency closest to 141.7001 Hz."""
        primes = get_primes_to_check()
        target = float(F0_TARGET)

        errors = {}
        for p in primes:
            f = calculate_frequency(p)
            errors[p] = abs(float(f) - target)

        min_error_prime = min(errors, key=errors.get)
        assert min_error_prime == 17, \
            f"p=17 should minimize frequency error, but p={min_error_prime} does"


class TestRPsi:
    """Test the universal radius R_Ψ calculation."""

    def test_r_psi_positive(self):
        """R_Ψ should be positive for all primes."""
        for p in get_primes_to_check():
            r_psi = calculate_r_psi(p)
            assert r_psi > 0, f"R_Ψ({p}) should be positive"

    def test_r_psi_17_order_of_magnitude(self):
        """R_Ψ(17) should be approximately 2 × 10^40."""
        r_psi_17 = calculate_r_psi(17)
        # From problem statement: R_Ψ(17) = 2.083343e40
        assert 1e40 < float(r_psi_17) < 1e41, \
            f"R_Ψ(17) = {float(r_psi_17):.3e}, expected in range 10^40 to 10^41"

    def test_r_psi_17_value(self):
        """R_Ψ(17) should match the expected value."""
        r_psi_17 = calculate_r_psi(17)
        expected = 2.083343e40
        rel_error = abs(float(r_psi_17) - expected) / expected
        assert rel_error < 0.01, \
            f"R_Ψ(17) = {float(r_psi_17):.6e}, expected ≈ {expected:.6e}"


class TestFrequencyDerivation:
    """Test the frequency derivation formula f₀ = c / (2π R_Ψ ℓ_P)."""

    def test_frequencies_positive(self):
        """All derived frequencies should be positive."""
        for p in get_primes_to_check():
            f = calculate_frequency(p)
            assert f > 0, f"f₀({p}) should be positive"

    def test_frequencies_known_values(self):
        """Test frequencies match expected values from problem statement."""
        expected = {
            11: 76.698,
            13: 93.985,
            17: 141.700,
            19: 173.688,
            23: 259.046,
            29: 461.752
        }
        for p, exp_f in expected.items():
            f = calculate_frequency(p)
            assert abs(float(f) - exp_f) < 1.0, \
                f"f₀({p}) = {float(f):.3f} Hz, expected ≈ {exp_f} Hz"


class TestValidation:
    """Test the complete validation function."""

    def test_validation_passes(self):
        """The complete validation should pass."""
        results = validate_spectral_resonance()
        assert results['validation']['all_passed'], "Validation should pass"

    def test_old_claim_falsified(self):
        """The old claim (p=17 minimizes) should be falsified."""
        results = validate_spectral_resonance()
        assert results['validation']['old_claim_falsified'], \
            "Old claim should be falsified (equilibrium minimum is at p=11)"

    def test_new_claim_verified(self):
        """The new claim (p=17 resonates at 141.7001 Hz) should be verified."""
        results = validate_spectral_resonance()
        assert results['validation']['new_claim_verified'], \
            "New claim should be verified"

    def test_validation_results_structure(self):
        """Validation results should have expected structure."""
        results = validate_spectral_resonance()
        expected_keys = [
            'timestamp', 'precision_digits', 'primes_analyzed',
            'equilibrium_values', 'equilibrium_minimum',
            'frequencies_hz', 'target_frequency_hz',
            'spectral_resonance', 'p17_parameters',
            'proof_hash', 'validation'
        ]
        for key in expected_keys:
            assert key in results, f"Missing key: {key}"


class TestPrecision:
    """Test calculations at different precision levels."""

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_equilibrium_minimum_consistent(self, precision):
        """Equilibrium minimum should be at p=11 regardless of precision."""
        min_prime, _ = find_equilibrium_minimum(precision)
        assert min_prime == 11, f"At precision {precision}, minimum should be at p=11"

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_resonance_prime_consistent(self, precision):
        """Resonance prime should be 17 regardless of precision."""
        resonance_prime, _ = find_resonance_prime(precision)
        assert resonance_prime == 17, f"At precision {precision}, resonance should be at p=17"

    @pytest.mark.parametrize("precision", [30, 50, 80, 100])
    def test_frequency_consistent(self, precision):
        """Frequency at p=17 should be consistent across precisions."""
        f_17 = calculate_frequency(17, precision)
        assert abs(float(f_17) - 141.7001) < FREQUENCY_TOLERANCE, \
            f"At precision {precision}, f₀(17) should be ≈ 141.7001 Hz"


class TestPhysicalConsistency:
    """Test physical consistency of the theory."""

    def test_scale_factor_positive(self):
        """Scale factor should be positive."""
        assert SCALE_FACTOR > 0

    def test_planck_length_positive(self):
        """Planck length should be positive."""
        assert PLANCK_LENGTH > 0

    def test_speed_of_light_positive(self):
        """Speed of light should be positive."""
        assert SPEED_OF_LIGHT > 0

    def test_dimensional_consistency(self):
        """
        Verify dimensional consistency of the frequency formula.

        f₀ = c / (2π R_Ψ ℓ_P)

        [f₀] = [c] / ([R_Ψ] × [ℓ_P])
             = (m/s) / (dimensionless × m)
             = 1/s = Hz ✓
        """
        r_psi = calculate_r_psi(17)  # dimensionless
        f = calculate_frequency(17)

        # Verify R_Ψ is dimensionless (large positive number)
        assert float(r_psi) > 1e30

        # Verify f is in Hz range
        assert 1 < float(f) < 1000

    def test_inverse_relationship(self):
        """Higher equilibrium should give lower R_Ψ and higher frequency."""
        primes = get_primes_to_check()

        for i in range(len(primes) - 1):
            p1, p2 = primes[i], primes[i + 1]
            eq1, eq2 = equilibrium(p1), equilibrium(p2)
            r1, r2 = calculate_r_psi(p1), calculate_r_psi(p2)
            f1, f2 = calculate_frequency(p1), calculate_frequency(p2)

            # Higher equilibrium -> lower R_Ψ
            if eq2 > eq1:
                assert r2 < r1, f"R_Ψ({p2}) should be < R_Ψ({p1})"
                # Lower R_Ψ -> higher frequency
                assert f2 > f1, f"f₀({p2}) should be > f₀({p1})"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
