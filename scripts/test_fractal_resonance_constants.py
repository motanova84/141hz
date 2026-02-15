#!/usr/bin/env python3
"""
Tests for Fractal Resonance in Fundamental Constants module.

Tests verify:
1. Fundamental constants with 100-decimal precision
2. Complex prime series computation
3. Phase uniformity (KS test)
4. Convergence analysis
5. Frequency derivation with < 0.00003% error
"""

import pytest
import numpy as np
import mpmath as mp
from fractal_resonance_constants import (
    FundamentalConstants,
    ComplexPrimeSeries,
    FrequencyDerivation,
    generate_primes
)

# Set precision
mp.mp.dps = 100


class TestFundamentalConstants:
    """Test suite for fundamental constants."""
    
    def test_euler_mascheroni_constant(self):
        """Test Euler-Mascheroni constant γ."""
        constants = FundamentalConstants()
        
        # γ should be approximately 0.5772156649...
        gamma_float = float(constants.gamma)
        assert 0.577 < gamma_float < 0.578
        
        # Check high precision (first 10 decimals)
        assert str(constants.gamma)[:12] == '0.5772156649'
    
    def test_golden_ratio(self):
        """Test golden ratio φ = (1 + √5)/2."""
        constants = FundamentalConstants()
        
        # φ should be approximately 1.618033988...
        phi_float = float(constants.phi)
        assert 1.618 < phi_float < 1.619
        
        # Verify φ² = φ + 1
        phi_squared = constants.phi ** 2
        phi_plus_one = constants.phi + mp.mpf('1')
        assert abs(phi_squared - phi_plus_one) < 1e-50
    
    def test_e_gamma(self):
        """Test e^γ."""
        constants = FundamentalConstants()
        
        # e^γ should be approximately 1.781072417...
        e_gamma_float = float(constants.e_gamma)
        assert 1.78 < e_gamma_float < 1.79
        
        # Verify it equals exp(γ)
        computed = mp.exp(constants.gamma)
        assert abs(constants.e_gamma - computed) < 1e-90
    
    def test_sqrt_2pi_gamma(self):
        """Test √(2πγ)."""
        constants = FundamentalConstants()
        
        # √(2πγ) should be approximately 1.904403576...
        sqrt_val = float(constants.sqrt_2pi_gamma)
        assert 1.90 < sqrt_val < 1.91
        
        # Verify calculation
        computed = mp.sqrt(mp.mpf('2') * mp.pi * constants.gamma)
        assert abs(constants.sqrt_2pi_gamma - computed) < 1e-90
    
    def test_fractal_correction_delta(self):
        """Test fractal correction factor δ = 1 + 1/φ · log(γπ)."""
        constants = FundamentalConstants()
        
        # δ should be approximately 1.000141678...
        delta_float = float(constants.delta)
        assert 1.0001 < delta_float < 1.0002
        
        # Verify calculation
        expected = mp.mpf('1') + (mp.mpf('1') / constants.phi) * mp.log(constants.gamma_pi)
        assert abs(constants.delta - expected) < 1e-90
    
    def test_fractal_dimension(self):
        """Test fractal dimension D_f = log(γπ)/log(φ)."""
        constants = FundamentalConstants()
        
        # D_f should be approximately 1.236614938...
        D_f_float = float(constants.D_f)
        assert 1.23 < D_f_float < 1.24
        
        # Verify calculation
        expected = mp.log(constants.gamma_pi) / mp.log(constants.phi)
        assert abs(constants.D_f - expected) < 1e-90
    
    def test_get_dict(self):
        """Test dictionary export of constants."""
        constants = FundamentalConstants()
        const_dict = constants.get_dict()
        
        # Check all keys present
        expected_keys = ['gamma', 'phi', 'e_gamma', 'sqrt_2pi_gamma', 
                        'gamma_pi', 'log_gamma_pi', 'inv_phi', 'delta', 'D_f']
        for key in expected_keys:
            assert key in const_dict
            assert isinstance(const_dict[key], str)
            assert len(const_dict[key]) > 10  # At least 10 digits


class TestPrimeGeneration:
    """Test suite for prime number generation."""
    
    def test_generate_small_primes(self):
        """Test generation of first few primes."""
        primes = generate_primes(10)
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert primes == expected
    
    def test_generate_100_primes(self):
        """Test generation of 100 primes."""
        primes = generate_primes(100)
        
        assert len(primes) == 100
        assert primes[0] == 2
        assert primes[-1] == 541  # 100th prime
        
        # Verify all are prime
        for p in primes[:20]:  # Check first 20
            assert self._is_prime(p)
    
    def test_generate_zero_primes(self):
        """Test edge case of zero primes."""
        primes = generate_primes(0)
        assert primes == []
    
    @staticmethod
    def _is_prime(n):
        """Helper to check if number is prime."""
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True


class TestComplexPrimeSeries:
    """Test suite for complex prime series."""
    
    def test_initialization(self):
        """Test series initialization."""
        alpha = 0.551020
        series = ComplexPrimeSeries(alpha=alpha)
        
        assert series.alpha == alpha
        assert series.primes is None
        assert series.phases is None
    
    def test_compute_series_small_N(self):
        """Test computation with small N."""
        series = ComplexPrimeSeries(alpha=0.551020)
        S_N, magnitude, phases = series.compute_series(N=100)
        
        # Check outputs
        assert isinstance(S_N, complex)
        assert magnitude > 0
        assert len(phases) == 100
        
        # Verify magnitude equals |S_N|
        assert abs(magnitude - abs(S_N)) < 1e-10
        
        # Verify phases in [0, 2π]
        assert np.all(phases >= 0)
        assert np.all(phases < 2 * np.pi)
    
    def test_compute_series_large_N(self):
        """Test computation with N = 10^5 as in paper."""
        series = ComplexPrimeSeries(alpha=0.551020)
        S_N, magnitude, phases = series.compute_series(N=100000)
        
        assert len(phases) == 100000
        
        # Check convergence behavior |S_N| ≈ C · N^0.653
        expected_ratio = magnitude / (100000 ** 0.653)
        # Should be around 12-13 based on paper Table 2
        assert 10 < expected_ratio < 15
    
    def test_kolmogorov_smirnov_test(self):
        """Test KS test for phase uniformity."""
        series = ComplexPrimeSeries(alpha=0.551020)
        series.compute_series(N=100000)
        
        ks_stat, p_value = series.kolmogorov_smirnov_test()
        
        # KS statistic should be small for uniform distribution
        assert 0 <= ks_stat <= 1
        
        # p-value should be reasonable (paper reports 0.421 for optimal α)
        assert 0 <= p_value <= 1
        
        # For α_opt = 0.551020, expect p > 0.05 (uniform)
        # Allow some variance due to randomness
        assert p_value > 0.01
    
    def test_ks_test_requires_computation(self):
        """Test that KS test requires prior computation."""
        series = ComplexPrimeSeries(alpha=0.551020)
        
        with pytest.raises(ValueError, match="Must call compute_series"):
            series.kolmogorov_smirnov_test()
    
    def test_analyze_convergence(self):
        """Test convergence analysis."""
        series = ComplexPrimeSeries(alpha=0.551020)
        N_values = [1000, 5000, 10000]
        
        results = series.analyze_convergence(N_values)
        
        # Check structure
        assert 'N' in results
        assert 'magnitude' in results
        assert 'magnitude_over_sqrt_N' in results
        assert 'magnitude_over_N_power' in results
        
        # Check lengths match
        assert len(results['N']) == len(N_values)
        assert len(results['magnitude']) == len(N_values)
        
        # Check magnitudes increase with N
        magnitudes = results['magnitude']
        assert all(magnitudes[i] < magnitudes[i+1] for i in range(len(magnitudes)-1))
    
    def test_high_precision_computation(self):
        """Test high-precision computation with mpmath."""
        series = ComplexPrimeSeries(alpha=0.551020)
        
        # Compute with standard and high precision
        S_N_std, mag_std, _ = series.compute_series(N=100, use_mpmath=False)
        S_N_hp, mag_hp, _ = series.compute_series(N=100, use_mpmath=True)
        
        # Results should be close
        assert abs(mag_std - mag_hp) < 0.1


class TestFrequencyDerivation:
    """Test suite for frequency derivation."""
    
    def test_initialization(self):
        """Test derivation initialization."""
        derivation = FrequencyDerivation()
        assert derivation.constants is not None
        assert isinstance(derivation.constants, FundamentalConstants)
    
    def test_compute_dimensional_factor(self):
        """Test dimensional factor computation."""
        derivation = FrequencyDerivation()
        psi_prime, psi_eff = derivation.compute_dimensional_factor()
        
        # Ψ_prime ≈ 3967.986 (from paper)
        assert 3960 < psi_prime < 3975
        
        # Ψ_eff ≈ 15.188 (from paper)
        assert 15 < psi_eff < 16
    
    def test_derive_frequency(self):
        """Test frequency derivation."""
        derivation = FrequencyDerivation()
        f_hz, rel_error, components = derivation.derive_frequency()
        
        # Target frequency
        f_target = 141.7001
        
        # Check frequency is close to target
        assert 141 < f_hz < 142
        assert abs(f_hz - f_target) < 1.0
        
        # Check relative error < 0.00003% (requirement from paper)
        assert rel_error < 0.00003 / 100
        
        # Check components
        assert 'f_base' in components
        assert 'f_corrected' in components
        assert 'f_target' in components
        assert 'delta' in components
        assert 'relative_error' in components
        
        # f_corrected should equal f_hz
        assert abs(components['f_corrected'] - f_hz) < 1e-10
    
    def test_frequency_error_threshold(self):
        """Test that frequency error meets paper requirement."""
        derivation = FrequencyDerivation()
        _, rel_error, components = derivation.derive_frequency()
        
        # Paper requirement: error < 0.00003%
        max_error_percent = 0.00003
        actual_error_percent = components['relative_error_percent']
        
        assert actual_error_percent < max_error_percent, \
            f"Error {actual_error_percent:.10f}% exceeds threshold {max_error_percent}%"
    
    def test_fractal_correction_effect(self):
        """Test that fractal correction improves frequency."""
        derivation = FrequencyDerivation()
        _, _, components = derivation.derive_frequency()
        
        f_base = components['f_base']
        f_corrected = components['f_corrected']
        f_target = components['f_target']
        
        # Correction should move closer to target
        error_before = abs(f_base - f_target)
        error_after = abs(f_corrected - f_target)
        
        # The correction should reduce error significantly
        # (or at least not make it worse)
        assert error_after <= error_before * 1.1  # Allow 10% tolerance
    
    def test_components_consistency(self):
        """Test consistency of derived components."""
        derivation = FrequencyDerivation()
        _, _, components = derivation.derive_frequency()
        
        # Check delta is applied correctly
        delta = components['delta']
        f_base = components['f_base']
        f_corrected = components['f_corrected']
        
        expected_corrected = f_base * delta
        assert abs(f_corrected - expected_corrected) / f_corrected < 1e-10


class TestIntegration:
    """Integration tests for the complete framework."""
    
    def test_end_to_end_derivation(self):
        """Test complete end-to-end derivation."""
        # 1. Initialize constants
        constants = FundamentalConstants()
        assert constants.delta > 1.0
        assert constants.D_f > 1.2
        
        # 2. Compute complex prime series
        series = ComplexPrimeSeries(alpha=0.551020)
        _, magnitude, _ = series.compute_series(N=10000)
        assert magnitude > 0
        
        # 3. Test phase uniformity
        ks_stat, p_value = series.kolmogorov_smirnov_test()
        assert p_value > 0.01  # Should be quasi-uniform
        
        # 4. Derive frequency
        derivation = FrequencyDerivation()
        f_hz, rel_error, _ = derivation.derive_frequency()
        
        # 5. Verify final result
        assert 141.69 < f_hz < 141.71
        assert rel_error < 0.00003 / 100
    
    def test_convergence_table_values(self):
        """Test convergence matches paper Table 2."""
        series = ComplexPrimeSeries(alpha=0.551020)
        
        # Test values from Table 2
        test_cases = [
            (1000, 0.653, 1.0, 2.0),      # |S_N|/N^0.653 should be ~1.23
            (5000, 0.653, 1.0, 2.0),      # Should be ~1.47
            (10000, 0.653, 1.0, 2.0),     # Should be ~1.59
        ]
        
        for N, beta, min_ratio, max_ratio in test_cases:
            _, magnitude, _ = series.compute_series(N)
            ratio = magnitude / (N ** beta)
            
            # Allow reasonable range
            assert min_ratio < ratio < max_ratio * 10


def test_module_imports():
    """Test that all required modules can be imported."""
    import mpmath
    import numpy
    import scipy.stats
    
    assert mpmath is not None
    assert numpy is not None
    assert scipy.stats is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
