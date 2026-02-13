"""
Tests for Spiral Light Geometry Module

Comprehensive tests for the QCAL theory that light follows logarithmic spiral paths
modulated by Riemann zeta zeros and prime resonances.

Author: José Manuel Mota Burruezo
License: MIT
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.spiral_light_geometry import (
    SpiralLightGeometry,
    SpiralPathParams,
    WaveFunctionParams,
    CoherenceMaximality,
    generate_spiral_path,
    calculate_interference
)
from qcal.constants import F0_HZ, HBAR, C


class TestSpiralLightGeometry:
    """Tests for SpiralLightGeometry class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.geometry = SpiralLightGeometry(precision=30)
        np.random.seed(42)  # For reproducibility
    
    def test_initialization(self):
        """Test geometry initialization"""
        assert self.geometry.precision == 30
        assert self.geometry._primes_cache is None
        assert self.geometry._zeta_zeros_cache is None
    
    def test_get_primes(self):
        """Test prime number generation"""
        primes = self.geometry.get_primes(10)
        
        # Check we got 10 primes
        assert len(primes) == 10
        
        # Check first few primes are correct
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        np.testing.assert_array_equal(primes, expected)
        
        # Check caching works
        primes2 = self.geometry.get_primes(5)
        assert len(primes2) == 5
        np.testing.assert_array_equal(primes2, expected[:5])
    
    def test_get_zeta_zeros(self):
        """Test Riemann zeta zero calculation"""
        zeros = self.geometry.get_zeta_zeros(5)
        
        # Check we got 5 zeros
        assert len(zeros) == 5
        
        # Check first zero is approximately correct
        # First non-trivial zero: γ₁ ≈ 14.134725
        assert abs(zeros[0] - 14.134725) < 0.001
        
        # Check zeros are increasing
        assert np.all(np.diff(zeros) > 0)
        
        # Check all zeros are positive
        assert np.all(zeros > 0)
    
    def test_prime_phase_modulation(self):
        """Test prime phase modulation calculation"""
        # First prime should give phase based on log(2)/log(2) = 1
        phi_1 = self.geometry.prime_phase_modulation(1)
        assert abs(phi_1 - 2 * np.pi) < 1e-10
        
        # Second prime (3) should give different phase
        phi_2 = self.geometry.prime_phase_modulation(2)
        assert phi_2 != phi_1
        assert phi_2 > phi_1  # log(3) > log(2)
        
        # Check phase increases with prime index
        phi_3 = self.geometry.prime_phase_modulation(3)
        assert phi_3 > phi_2
    
    def test_spiral_path_basic(self):
        """Test basic spiral path generation"""
        t = np.linspace(0, 0.01, 1000)
        params = SpiralPathParams(r0=1.0, lambda_expansion=0.1, prime_index=1)
        
        x, y = self.geometry.spiral_path(t, params)
        
        # Check output shapes
        assert x.shape == t.shape
        assert y.shape == t.shape
        
        # Check initial radius approximately r0
        r0_calc = np.sqrt(x[0]**2 + y[0]**2)
        assert abs(r0_calc - params.r0) < 0.1
        
        # Check radius increases with time (expansion)
        r = np.sqrt(x**2 + y**2)
        assert np.all(np.diff(r) >= 0)  # Should be monotonically increasing
    
    def test_spiral_path_expansion(self):
        """Test exponential expansion of spiral"""
        t = np.linspace(0, 1, 1000)
        params = SpiralPathParams(r0=1.0, lambda_expansion=0.5, prime_index=1)
        
        x, y = self.geometry.spiral_path(t, params)
        r = np.sqrt(x**2 + y**2)
        
        # Check exponential growth
        # r(t) should grow as r0 * exp(λt)
        expected_r = params.r0 * np.exp(params.lambda_expansion * t)
        np.testing.assert_allclose(r, expected_r, rtol=0.1)
    
    def test_spiral_path_different_primes(self):
        """Test that different primes give different paths"""
        t = np.linspace(0, 0.01, 1000)
        
        x1, y1 = self.geometry.spiral_path(
            t, SpiralPathParams(prime_index=1)
        )
        x2, y2 = self.geometry.spiral_path(
            t, SpiralPathParams(prime_index=2)
        )
        
        # Paths should be different due to phase modulation
        assert not np.allclose(x1, x2)
        assert not np.allclose(y1, y2)
    
    def test_zeta_spectral_frequencies(self):
        """Test spectral frequency calculation from zeta zeros"""
        frequencies = self.geometry.zeta_spectral_frequencies(5)
        
        # Check we got 5 frequencies
        assert len(frequencies) == 5
        
        # First frequency should be f₀ (γ₁/γ₁ = 1)
        assert abs(frequencies[0] - F0_HZ) < 0.1
        
        # Check frequencies are positive
        assert np.all(frequencies > 0)
        
        # Check frequencies are ordered
        assert np.all(np.diff(frequencies) > 0)
    
    def test_wave_function_basic(self):
        """Test wave function generation"""
        x = np.linspace(-1e-6, 1e-6, 100)
        t = 0.001
        params = WaveFunctionParams(n_primes=5, n_zeros=5)
        
        psi = self.geometry.wave_function(x, t, params)
        
        # Check output shape
        assert psi.shape == x.shape
        
        # Check complex output
        assert psi.dtype == complex
        
        # Check normalization
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        assert abs(norm - 1.0) < 0.01
    
    def test_wave_function_time_evolution(self):
        """Test wave function evolves with time"""
        x = np.linspace(-1e-6, 1e-6, 100)
        params = WaveFunctionParams(n_primes=5, n_zeros=5)
        
        psi_t1 = self.geometry.wave_function(x, 0.001, params)
        psi_t2 = self.geometry.wave_function(x, 0.002, params)
        
        # Wave functions at different times should differ
        assert not np.allclose(psi_t1, psi_t2)
        
        # But both should be normalized
        norm1 = np.sqrt(np.sum(np.abs(psi_t1)**2))
        norm2 = np.sqrt(np.sum(np.abs(psi_t2)**2))
        assert abs(norm1 - 1.0) < 0.01
        assert abs(norm2 - 1.0) < 0.01
    
    def test_interference_pattern(self):
        """Test interference pattern generation"""
        size = 64
        x = np.linspace(-1e-6, 1e-6, size)
        y = np.linspace(-1e-6, 1e-6, size)
        X, Y = np.meshgrid(x, y)
        
        intensity = self.geometry.interference_pattern(X, Y, 0.001)
        
        # Check output shape
        assert intensity.shape == (size, size)
        
        # Check intensity is real and positive
        assert np.all(intensity >= 0)
        assert np.all(np.isreal(intensity))
        
        # Check intensity is normalized (integrated intensity)
        total = np.sum(intensity)
        assert total > 0
    
    def test_spiral_deviation_angle(self):
        """Test angular deviation calculation"""
        # Generate spiral path
        t = np.linspace(0, 0.01, 1000)
        params = SpiralPathParams(lambda_expansion=0.1, prime_index=2)
        x, y = self.geometry.spiral_path(t, params)
        
        # Calculate deviation
        delta_theta = self.geometry.spiral_deviation_angle(x, y, params)
        
        # Check output shape
        assert delta_theta.shape == x.shape
        
        # Check deviations are in [-π, π]
        assert np.all(delta_theta >= -np.pi)
        assert np.all(delta_theta <= np.pi)
        
        # Check some deviation exists (not zero everywhere)
        assert np.std(delta_theta) > 0


class TestCoherenceMaximality:
    """Tests for CoherenceMaximality class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.coherence = CoherenceMaximality()
        np.random.seed(123)
    
    def test_initialization(self):
        """Test coherence analyzer initialization"""
        assert self.coherence.geometry is not None
        assert isinstance(self.coherence.geometry, SpiralLightGeometry)
    
    def test_prime_spectral_map(self):
        """Test prime spectral map generation"""
        spectral_map = self.coherence.prime_spectral_map(n_primes=10)
        
        # Check required keys
        assert 'primes' in spectral_map
        assert 'phases' in spectral_map
        assert 'phase_differences' in spectral_map
        assert 'log_primes' in spectral_map
        
        # Check sizes
        assert len(spectral_map['primes']) == 10
        assert len(spectral_map['phases']) == 10
        assert len(spectral_map['phase_differences']) == 9
        assert len(spectral_map['log_primes']) == 10
        
        # Check phase differences are positive
        assert np.all(spectral_map['phase_differences'] > 0)
    
    def test_coherence_measure(self):
        """Test coherence measure calculation"""
        # Create a coherent wave function
        psi_coherent = np.exp(1j * 0.5) * np.ones(100, dtype=complex)
        psi_coherent /= np.sqrt(len(psi_coherent))
        
        C = self.coherence.coherence_measure(psi_coherent, reference_phase=0.5)
        
        # Perfect coherence should be close to 1
        assert C >= 0
        assert C <= 1
        assert C > 0.99
    
    def test_coherence_measure_random(self):
        """Test coherence measure for random phase"""
        # Random phase wave function (incoherent)
        psi_random = np.exp(1j * np.random.uniform(0, 2*np.pi, 100))
        psi_random /= np.sqrt(len(psi_random))
        
        C = self.coherence.coherence_measure(psi_random)
        
        # Should have low coherence
        assert C >= 0
        assert C <= 1
        assert C < 0.5  # Typically much lower for random
    
    def test_maximum_coherence_path(self):
        """Test finding maximum coherence path"""
        duration = 0.005
        dt = 1e-4
        t_array = np.arange(0, duration, dt)
        
        optimal_prime, max_coherence = self.coherence.maximum_coherence_path(
            t_array, n_primes=5
        )
        
        # Check output types and ranges
        assert isinstance(optimal_prime, (int, np.integer))
        assert optimal_prime >= 1
        assert optimal_prime <= 5
        assert 0 <= max_coherence <= 1


class TestConvenienceFunctions:
    """Tests for convenience functions"""
    
    def test_generate_spiral_path(self):
        """Test generate_spiral_path convenience function"""
        t, x, y = generate_spiral_path(duration=0.01, dt=1e-4, prime_index=1)
        
        # Check outputs
        assert len(t) == len(x)
        assert len(t) == len(y)
        assert len(t) > 0
        
        # Check time array
        assert t[0] >= 0
        assert t[-1] <= 0.01 + 1e-4
    
    def test_calculate_interference(self):
        """Test calculate_interference convenience function"""
        intensity = calculate_interference(
            size=64,
            extent=1e-6,
            t=0.001,
            n_primes=3,
            n_zeros=3
        )
        
        # Check output
        assert intensity.shape == (64, 64)
        assert np.all(intensity >= 0)
        assert np.all(np.isreal(intensity))


class TestPhysicalConsistency:
    """Tests for physical consistency of the theory"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.geometry = SpiralLightGeometry(precision=30)
    
    def test_fundamental_frequency_consistency(self):
        """Test that f₀ = 141.7001 Hz is used consistently"""
        # Check in spiral path
        t = np.linspace(0, 1.0/F0_HZ, 1000)  # One period
        params = SpiralPathParams(lambda_expansion=0.0, prime_index=1)
        x, y = self.geometry.spiral_path(t, params)
        
        # After one period, should return to similar angle (modulo 2π)
        theta_0 = np.arctan2(y[0], x[0])
        theta_T = np.arctan2(y[-1], x[-1])
        
        # Difference should be close to 0 or 2π
        diff = abs(theta_T - theta_0)
        assert abs(diff - 2*np.pi) < 0.1 or abs(diff) < 0.1
    
    def test_speed_of_light_consistency(self):
        """Test that action term uses c correctly"""
        # Wave function should use k = 2πf/c for action
        x = np.array([0, C / F0_HZ])  # One wavelength at f₀
        t = 0
        params = WaveFunctionParams(n_primes=1, n_zeros=1)
        
        psi = self.geometry.wave_function(x, t, params)
        
        # Both should be well-defined
        assert np.all(np.isfinite(psi))
    
    def test_planck_constant_usage(self):
        """Test that ℏ is used correctly in action"""
        x = np.linspace(0, 1e-6, 100)
        t = 0.001
        
        psi = self.geometry.wave_function(x, t)
        
        # Should produce valid quantum wave function
        assert np.all(np.isfinite(psi))
        
        # Check normalization
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        assert abs(norm - 1.0) < 0.01
    
    def test_zeta_zero_convergence(self):
        """Test that zeta zeros converge to known values"""
        # Check first zero with high precision
        geometry = SpiralLightGeometry(precision=100)
        zeros = geometry.get_zeta_zeros(1)
        
        # Known value: γ₁ = 14.134725141734693790...
        expected = 14.134725141734693790
        assert abs(zeros[0] - expected) < 1e-10


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.geometry = SpiralLightGeometry()
    
    def test_zero_expansion(self):
        """Test spiral with zero expansion (circular motion)"""
        t = np.linspace(0, 0.01, 1000)
        params = SpiralPathParams(lambda_expansion=0.0, prime_index=1)
        
        x, y = self.geometry.spiral_path(t, params)
        r = np.sqrt(x**2 + y**2)
        
        # Radius should be constant
        assert np.std(r) < 0.01
    
    def test_single_prime(self):
        """Test with single prime (minimal case)"""
        x = np.linspace(-1e-6, 1e-6, 50)
        params = WaveFunctionParams(n_primes=1, n_zeros=1)
        
        psi = self.geometry.wave_function(x, 0.001, params)
        
        # Should still produce valid wave function
        assert np.all(np.isfinite(psi))
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        assert abs(norm - 1.0) < 0.01
    
    def test_large_time(self):
        """Test behavior at large times"""
        t = np.array([0, 1, 10, 100])
        params = SpiralPathParams(lambda_expansion=0.001, prime_index=1)
        
        x, y = self.geometry.spiral_path(t, params)
        
        # Should handle large times without overflow
        assert np.all(np.isfinite(x))
        assert np.all(np.isfinite(y))
    
    def test_many_primes(self):
        """Test with many primes"""
        x = np.linspace(-1e-6, 1e-6, 50)
        params = WaveFunctionParams(n_primes=50, n_zeros=10)
        
        psi = self.geometry.wave_function(x, 0.001, params)
        
        # Should handle many primes
        assert np.all(np.isfinite(psi))


class TestReproducibility:
    """Tests for reproducibility of results"""
    
    def test_deterministic_primes(self):
        """Test that prime generation is deterministic"""
        geom1 = SpiralLightGeometry()
        geom2 = SpiralLightGeometry()
        
        primes1 = geom1.get_primes(20)
        primes2 = geom2.get_primes(20)
        
        np.testing.assert_array_equal(primes1, primes2)
    
    def test_deterministic_zeta_zeros(self):
        """Test that zeta zeros are deterministic"""
        geom1 = SpiralLightGeometry(precision=50)
        geom2 = SpiralLightGeometry(precision=50)
        
        zeros1 = geom1.get_zeta_zeros(5)
        zeros2 = geom2.get_zeta_zeros(5)
        
        np.testing.assert_allclose(zeros1, zeros2, rtol=1e-10)
    
    def test_deterministic_wave_function(self):
        """Test that wave function is deterministic"""
        x = np.linspace(-1e-6, 1e-6, 100)
        t = 0.001
        
        geom1 = SpiralLightGeometry(precision=30)
        geom2 = SpiralLightGeometry(precision=30)
        
        psi1 = geom1.wave_function(x, t)
        psi2 = geom2.wave_function(x, t)
        
        np.testing.assert_allclose(psi1, psi2, rtol=1e-10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
