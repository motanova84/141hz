#!/usr/bin/env python3
"""
Test suite for PrimeHarmonicCalculator
Tests the complete production code for 141.7001 Hz frequency derivation
"""

import pytest
from prime_harmonic_calculator import PrimeHarmonicCalculator


def test_initialization():
    """Test that calculator initializes with correct constants"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Check that fundamental constants are set
    assert calc.target_frequency == 141.7001
    assert float(calc.phi) > 1.618  # Golden ratio
    assert float(calc.gamma) > 0.577  # Euler-Mascheroni constant
    assert calc.omega_0 is not None
    assert calc.scaling_factor is not None


def test_prime_generation():
    """Test prime number generation"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Generate first 10 primes
    primes = calc.generate_primes(10)

    # Check count
    assert len(primes) == 10

    # Check first few primes are correct
    expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes == expected_primes


def test_phase_calculation():
    """Test prime phase calculation"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Use small set of primes
    primes = [2, 3, 5, 7]
    phases = calc.calculate_prime_phases(primes)

    # Check that we get correct number of phases
    assert len(phases) == len(primes)

    # Check all phases are positive numbers
    assert all(p > 0 for p in phases)

    # Check phases are ordered (increasing)
    for i in range(len(phases) - 1):
        assert phases[i] < phases[i + 1]


def test_harmonic_sum():
    """Test harmonic sum calculation"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Use small set of primes
    primes = [2, 3, 5, 7, 11]
    phases = calc.calculate_prime_phases(primes)

    harmonic_sum, magnitude = calc.calculate_harmonic_sum(primes, phases)

    # Check that we get complex number
    assert isinstance(harmonic_sum, complex)

    # Check magnitude is positive
    assert magnitude > 0

    # Check magnitude matches absolute value
    assert abs(abs(harmonic_sum) - magnitude) < 1e-6


def test_A_eff_squared():
    """Test A_eff² calculation"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    A_eff_squared = calc.calculate_A_eff_squared()

    # Check it's a positive number
    assert A_eff_squared > 0

    # Check it's in reasonable range (around 1-10)
    assert 0.1 < A_eff_squared < 100


def test_complete_analysis_small():
    """Test complete analysis with small prime set"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Run with 50 primes (quick test)
    results = calc.run_complete_analysis(n_primes=50)

    # Check all expected keys are present
    expected_keys = ['n_primes', 'primes', 'phases', 'harmonic_sum',
                     'magnitude', 'A_eff_squared', 'final_frequency',
                     'target_frequency', 'error_absolute', 'error_relative',
                     'success']
    for key in expected_keys:
        assert key in results

    # Check n_primes matches
    assert results['n_primes'] == 50

    # Check frequency is positive
    assert results['final_frequency'] > 0

    # Check target frequency is correct
    assert results['target_frequency'] == 141.7001


def test_frequency_calculation():
    """Test final frequency calculation"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Use sample values
    magnitude = 100.0
    A_eff_squared = 4.0

    frequency = calc.calculate_final_frequency(magnitude, A_eff_squared)

    # Check frequency is positive
    assert frequency > 0

    # Check it's in reasonable range for this calculation
    assert 0 < frequency < 10000


def test_convergence_structure():
    """Test convergence analysis structure (without running full analysis)"""
    calc = PrimeHarmonicCalculator(precision_digits=30)

    # Run very short convergence test
    df = calc.convergence_analysis(max_primes=100, step=50)

    # Check DataFrame has expected columns
    expected_columns = ['n_primes', 'frequency', 'error_abs', 'error_rel',
                        'magnitude', 'sqrt_n', 'ratio']
    for col in expected_columns:
        assert col in df.columns

    # Check we have expected number of rows
    assert len(df) == 2  # (50, 100)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
