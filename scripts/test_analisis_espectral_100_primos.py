#!/usr/bin/env python3
"""
Test suite for Spectral Analysis of the First 100 Prime Numbers.

This module tests the adelic-fractal equilibrium calculations and
spectral frequency derivations.

Run with: python -m pytest scripts/test_analisis_espectral_100_primos.py -v

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto de Consciencia Cuántica (ICQ)
"""

import os
import sys
import pytest

# Add scripts directory for imports (follows existing pattern in repository)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analisis_espectral_100_primos import (  # noqa: E402
    generate_primes,
    equilibrium_function,
    calculate_r_psi,
    calculate_frequency,
    frequency_to_note,
    get_octave,
    analyze_prime_spectrum,
)

# Test tolerance constants
TOLERANCE_TIGHT = 1e-6
TOLERANCE_RELATIVE = 0.01  # 1% relative tolerance


class TestPrimeGeneration:
    """Test prime number generation."""

    def test_generate_first_10_primes(self):
        """Verify the first 10 primes are correct."""
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        result = generate_primes(10)
        assert result == expected

    def test_generate_100_primes(self):
        """Verify we can generate 100 primes correctly."""
        primes = generate_primes(100)
        assert len(primes) == 100
        assert primes[0] == 2
        assert primes[-1] == 541  # 100th prime is 541

    def test_empty_list_for_zero(self):
        """Generating 0 primes should return empty list."""
        assert generate_primes(0) == []


class TestEquilibriumFunction:
    """Test the equilibrium function: equilibrium(p) = exp(π√p/2) / p^(3/2)."""

    def test_equilibrium_p2(self):
        """Equilibrium at p=2 should be approximately 3.260."""
        eq_2 = float(equilibrium_function(2))
        assert abs(eq_2 - 3.260) < 0.01

    def test_equilibrium_p3(self):
        """Equilibrium at p=3 should be approximately 2.923 (minimum)."""
        eq_3 = float(equilibrium_function(3))
        assert abs(eq_3 - 2.923) < 0.01

    def test_equilibrium_p17(self):
        """Equilibrium at p=17 should be approximately 9.270."""
        eq_17 = float(equilibrium_function(17))
        assert abs(eq_17 - 9.270) < 0.01

    def test_equilibrium_monotonic_after_minimum(self):
        """Equilibrium should be monotonically increasing for p > 3."""
        primes = [5, 7, 11, 13, 17, 19, 23, 29, 31]
        equilibriums = [float(equilibrium_function(p)) for p in primes]
        for i in range(1, len(equilibriums)):
            assert equilibriums[i] > equilibriums[i - 1], \
                f"equilibrium({primes[i]}) should be > equilibrium({primes[i - 1]})"

    def test_equilibrium_positive(self):
        """Equilibrium should always be positive."""
        for p in [2, 3, 5, 7, 11, 17, 29, 97]:
            assert float(equilibrium_function(p)) > 0


class TestFrequencyCalculation:
    """Test frequency calculations from primes."""

    def test_frequency_p3(self):
        """Frequency at p=3 should be approximately 44.69 Hz."""
        freq_3 = float(calculate_frequency(3))
        assert abs(freq_3 - 44.69) < 0.1

    def test_frequency_p17(self):
        """Frequency at p=17 (noetic point) should be approximately 141.70 Hz."""
        freq_17 = float(calculate_frequency(17))
        assert abs(freq_17 - 141.70) < 0.1

    def test_frequency_p23(self):
        """Frequency at p=23 should be close to C4 (261.63 Hz)."""
        freq_23 = float(calculate_frequency(23))
        assert abs(freq_23 - 259.05) < 0.5

    def test_frequency_p541(self):
        """Frequency at p=541 should be in THz range."""
        freq_541 = float(calculate_frequency(541))
        assert freq_541 > 1e12  # Greater than 1 THz
        assert freq_541 < 1e13  # Less than 10 THz

    def test_frequency_ordering(self):
        """Frequencies should generally increase with primes (after p=3)."""
        primes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
        frequencies = [float(calculate_frequency(p)) for p in primes]
        # After the minimum at p=3, frequencies should increase
        for i in range(2, len(frequencies)):
            assert frequencies[i] > frequencies[i - 1], \
                f"freq({primes[i]}) should be > freq({primes[i - 1]})"


class TestMusicalMapping:
    """Test musical note and octave mapping."""

    def test_frequency_to_note_a4(self):
        """440 Hz should map to A4."""
        note, cents, octave = frequency_to_note(440.0)
        assert note == "A4"
        assert abs(cents) < 1  # Should be very close to 0

    def test_frequency_to_note_c4(self):
        """261.63 Hz should map to C4."""
        note, cents, octave = frequency_to_note(261.63)
        assert note == "C4"
        assert abs(cents) < 1

    def test_get_octave_low(self):
        """Low frequencies should be in low octaves."""
        # 32.70 Hz should be in octave 1
        assert get_octave(32.70) == 1

    def test_get_octave_a4(self):
        """A4 (440 Hz) should be in octave 5 (in 0-indexed C notation)."""
        assert get_octave(440.0) == 5

    def test_p17_musical_note(self):
        """p=17 (141.7 Hz) should map to C#3."""
        freq = float(calculate_frequency(17))
        note, cents, octave = frequency_to_note(freq)
        assert note == "C#3"
        assert octave == 3


class TestSpecialPrimes:
    """Test identification of special primes."""

    def test_noetic_point_is_17(self):
        """The noetic point should be p=17 with frequency ~141.7 Hz."""
        result = analyze_prime_spectrum(20)
        special = result.special_primes
        assert "noetic_point" in special
        assert special["noetic_point"]["prime"] == 17
        assert abs(special["noetic_point"]["frequency_hz"] - 141.7) < 0.1

    def test_fundamental_is_p3(self):
        """The fundamental (lowest frequency) should be p=3."""
        result = analyze_prime_spectrum(20)
        special = result.special_primes
        assert "fundamental" in special
        assert special["fundamental"]["prime"] == 3

    def test_closest_c4_is_p23(self):
        """The closest to C4 should be p=23."""
        result = analyze_prime_spectrum(50)
        special = result.special_primes
        assert "closest_c4" in special
        assert special["closest_c4"]["prime"] == 23


class TestFractalStructure:
    """Test fractal structure analysis."""

    def test_r_squared_high(self):
        """R² should be very high (> 0.99) indicating strong fractal structure."""
        result = analyze_prime_spectrum(100)
        r_squared = result.fractal_analysis["r_squared"]
        assert r_squared > 0.99, f"R² = {r_squared} should be > 0.99"

    def test_positive_slope(self):
        """Slope should be positive (frequency increases with √p)."""
        result = analyze_prime_spectrum(100)
        slope = result.fractal_analysis["slope_a"]
        assert slope > 0

    def test_effective_dimension_positive(self):
        """Effective dimension should be positive."""
        result = analyze_prime_spectrum(100)
        d_eff = result.fractal_analysis["effective_dimension"]
        assert d_eff > 0


class TestSpectralMoments:
    """Test spectral moment calculations."""

    def test_moments_positive(self):
        """All moments should be positive."""
        result = analyze_prime_spectrum(100)
        moments = result.spectral_moments
        assert moments["mu_1_first_moment"] > 0
        assert moments["mu_2_second_moment"] > 0

    def test_kappa_psi_positive(self):
        """κΨ ratio should be positive."""
        result = analyze_prime_spectrum(100)
        kappa = result.spectral_moments["kappa_psi_ratio"]
        assert kappa > 0


class TestStatistics:
    """Test global statistics of the analysis."""

    def test_100_primes_statistics(self):
        """Verify statistics for 100 primes."""
        result = analyze_prime_spectrum(100)
        stats = result.statistics

        assert stats["n_primes"] == 100
        assert stats["prime_min"] == 2
        assert stats["prime_max"] == 541
        assert stats["freq_min_prime"] == 3
        assert stats["freq_max_prime"] == 541

    def test_dynamic_range(self):
        """Dynamic range should be approximately 2 × 10¹¹."""
        result = analyze_prime_spectrum(100)
        dynamic_range = result.statistics["dynamic_range"]
        assert 1e11 < dynamic_range < 3e11

    def test_octaves_covered(self):
        """Should cover approximately 38 octaves."""
        result = analyze_prime_spectrum(100)
        octaves = result.statistics["octaves_covered"]
        assert 35 <= octaves <= 40


class TestOctaveDistribution:
    """Test octave distribution of primes."""

    def test_octave_1_contains_4_primes(self):
        """Octave 1 should contain 4 primes: 2, 3, 5, 7."""
        result = analyze_prime_spectrum(100)
        octave_dist = result.octave_distribution
        if 1 in octave_dist:
            assert len(octave_dist[1]) == 4
            assert set(octave_dist[1]) == {2, 3, 5, 7}

    def test_octave_3_contains_p17(self):
        """Octave 3 (noetic octave) should contain p=17."""
        result = analyze_prime_spectrum(100)
        octave_dist = result.octave_distribution
        assert 3 in octave_dist
        assert 17 in octave_dist[3]


class TestRPsiCalculation:
    """Test R_Ψ (universal radius) calculation."""

    def test_r_psi_positive(self):
        """R_Ψ should always be positive."""
        for p in [2, 3, 5, 17, 29, 97]:
            assert float(calculate_r_psi(p)) > 0

    def test_r_psi_order_of_magnitude(self):
        """R_Ψ should be in the 10^40 range for small primes."""
        r_psi_17 = float(calculate_r_psi(17))
        assert 1e40 < r_psi_17 < 1e42


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_prime(self):
        """Analysis should work with a single prime."""
        result = analyze_prime_spectrum(1)
        assert len(result.prime_data) == 1
        assert result.prime_data[0].prime == 2

    def test_small_analysis(self):
        """Analysis should work with small number of primes."""
        result = analyze_prime_spectrum(5)
        assert len(result.prime_data) == 5

    def test_large_analysis(self):
        """Analysis should work with larger number of primes."""
        result = analyze_prime_spectrum(200)
        assert len(result.prime_data) == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
