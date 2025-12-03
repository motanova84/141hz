#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for P17 Resonance Verification.

This module tests the theoretical correction that p=17 is a resonance
point rather than an optimization minimum.

Author: JMMB Ψ✧ (motanova84)
Instituto de Conciencia Cuántica (ICQ) – QCAL ∞³
"""

import os
import sys
import pytest

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from p17_resonance_verification import (
    PRIMES,
    C_LIGHT,
    PLANCK_LENGTH,
    TARGET_FREQUENCY,
    SCALE_FACTOR,
    adelic_factor,
    equilibrium,
    R_Psi,
    frequency,
)

# Test tolerance constants
TOLERANCE_TIGHT = 1e-6
TOLERANCE_FREQUENCY = 0.001  # 0.001 Hz


class TestEquilibriumFunction:
    """Test the equilibrium function exp(π√p/2) / p^(3/2)."""

    def test_equilibrium_positive(self):
        """Equilibrium values should be positive for all primes."""
        for p in PRIMES:
            assert equilibrium(p) > 0, f"equilibrium({p}) should be positive"

    def test_equilibrium_minimum_at_p11(self):
        """The minimum of equilibrium(p) should be at p=11, NOT p=17."""
        eq_11 = float(equilibrium(11))
        for p in PRIMES:
            eq_p = float(equilibrium(p))
            if p != 11:
                assert eq_11 < eq_p, \
                    f"equilibrium(11) = {eq_11:.6f} should be < equilibrium({p}) = {eq_p:.6f}"

    def test_equilibrium_not_minimum_at_p17(self):
        """Verify p=17 is NOT the minimum of equilibrium(p)."""
        values = {p: float(equilibrium(p)) for p in PRIMES}
        min_p = min(values, key=values.get)
        assert min_p != 17, f"Minimum should NOT be at p=17, got p={min_p}"
        assert min_p == 11, f"Minimum should be at p=11, got p={min_p}"

    def test_equilibrium_known_values(self):
        """Test equilibrium values match expected values."""
        expected = {
            11: 5.0173,
            13: 6.1482,
            17: 9.2696,
            19: 11.3621,
            23: 16.9460,
            29: 30.2064,
        }
        for p, exp_val in expected.items():
            eq_p = float(equilibrium(p))
            assert abs(eq_p - exp_val) < 0.001, \
                f"equilibrium({p}) = {eq_p:.4f}, expected ≈ {exp_val}"


class TestFrequencyDerivation:
    """Test that p=17 produces f₀ = 141.7001 Hz."""

    def test_frequency_positive(self):
        """Frequencies should be positive for all primes."""
        for p in PRIMES:
            assert frequency(p) > 0, f"frequency({p}) should be positive"

    def test_frequency_p17_is_141_7001(self):
        """p=17 should produce f₀ ≈ 141.7001 Hz."""
        f17 = frequency(17)
        error = abs(f17 - TARGET_FREQUENCY)
        assert error < TOLERANCE_FREQUENCY, \
            f"frequency(17) = {f17:.4f} Hz, expected 141.7001 Hz (error: {error:.6f} Hz)"

    def test_frequency_p17_unique_resonance(self):
        """p=17 should be the only prime producing f₀ ≈ 141.7 Hz."""
        for p in PRIMES:
            if p != 17:
                f_p = frequency(p)
                diff = abs(f_p - TARGET_FREQUENCY)
                assert diff > 10, \
                    f"frequency({p}) = {f_p:.4f} Hz is too close to 141.7001 Hz"

    def test_frequency_ordering(self):
        """Frequencies should increase with the prime value."""
        freqs = [frequency(p) for p in PRIMES]
        for i in range(len(freqs) - 1):
            assert freqs[i] < freqs[i + 1], \
                f"frequency({PRIMES[i]}) >= frequency({PRIMES[i+1]})"


class TestRPsi:
    """Test the R_Ψ calculation."""

    def test_r_psi_positive(self):
        """R_Ψ should be positive."""
        for p in PRIMES:
            assert R_Psi(p) > 0

    def test_r_psi_order_of_magnitude(self):
        """R_Ψ should be approximately 2 × 10^40."""
        r_psi_17 = R_Psi(17)
        # Should be around 2.08e40
        assert 1e40 < r_psi_17 < 1e41


class TestDimensionalConsistency:
    """Test dimensional consistency of the calculations."""

    def test_r_psi_from_frequency(self):
        """R_Ψ derived from equilibrium(17) should match the needed value."""
        import math

        # R_Ψ needed to produce 141.7001 Hz
        R_needed = C_LIGHT / (2 * math.pi * TARGET_FREQUENCY * PLANCK_LENGTH)

        # R_Ψ from equilibrium(17)
        R_from_eq17 = SCALE_FACTOR / float(equilibrium(17))

        ratio = R_from_eq17 / R_needed
        assert 0.999 < ratio < 1.001, \
            f"R_Ψ(17) / R_needed = {ratio:.6f}, expected ≈ 1.0"


class TestTheorems:
    """Test the main theoretical claims."""

    def test_theorem_minimization_is_false(self):
        """The claim that p=17 minimizes equilibrium(p) is FALSE."""
        values = {p: float(equilibrium(p)) for p in PRIMES}
        min_p = min(values, key=values.get)
        # The original theorem was false: p=17 does NOT minimize equilibrium
        assert min_p == 11, "p=11 should minimize equilibrium(p)"
        assert min_p != 17, "p=17 should NOT minimize equilibrium(p)"

    def test_theorem_resonance_is_true(self):
        """The claim that p=17 produces f₀ = 141.7001 Hz is TRUE."""
        f17 = frequency(17)
        error = abs(f17 - TARGET_FREQUENCY)
        # p=17 DOES produce the target frequency
        assert error < TOLERANCE_FREQUENCY, \
            f"p=17 should produce 141.7001 Hz (got {f17:.4f} Hz)"

    def test_theorem_uniqueness_is_true(self):
        """p=17 is the UNIQUE prime producing f₀ ≈ 141.7001 Hz."""
        close_primes = [p for p in PRIMES if abs(frequency(p) - TARGET_FREQUENCY) < 10]
        assert close_primes == [17], \
            f"Only p=17 should be close to 141.7001 Hz, got {close_primes}"


class TestPhysicalInterpretation:
    """Test the physical interpretation of the primes as frequencies."""

    def test_prime_frequency_map(self):
        """Each prime maps to a specific frequency range."""
        freq_ranges = {
            11: (70, 85),    # D#2 - Grave universe
            13: (85, 105),   # F#2-G2 - Transition
            17: (135, 150),  # C#3-D3 - Our universe
            19: (165, 185),  # F3 - Accelerated
            23: (250, 270),  # C4 - High resonance
            29: (450, 480),  # A#4 - Acute universe
        }
        for p, (low, high) in freq_ranges.items():
            f = frequency(p)
            assert low < f < high, \
                f"frequency({p}) = {f:.2f} Hz, expected in ({low}, {high})"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
