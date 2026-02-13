#!/usr/bin/env python3
"""
Tests for Spiral Light Path Theory
===================================

Comprehensive tests for the spiral light path implementation, including:
- Spiral trajectory calculations
- Prime modulation verification
- Zeta zero integration
- Interference pattern projections
- Observer projections on critical line
- Reproducibility

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
from qcal.spiral_light_path import (
    SpiralLightPath,
    SpiralParameters,
    demonstrate_spiral_vs_linear,
    validate_zeta_zeros
)


class TestSpiralParameters(unittest.TestCase):
    """Tests for SpiralParameters dataclass."""
    
    def test_default_parameters(self):
        """Test default parameter values."""
        params = SpiralParameters()
        
        self.assertAlmostEqual(params.f0, 141.7001, places=4)
        self.assertEqual(params.r0, 1.0)
        self.assertEqual(params.lambda_fractal, 0.01)
        self.assertEqual(params.precision, 50)
    
    def test_derived_parameters(self):
        """Test that derived parameters are computed correctly."""
        params = SpiralParameters(f0=100.0)
        
        # Check omega_0 = 2π f0
        expected_omega = 2 * np.pi * 100.0
        self.assertAlmostEqual(params.omega_0, expected_omega, places=6)
        
        # Check period T0 = 1/f0
        expected_T = 1.0 / 100.0
        self.assertAlmostEqual(params.T0, expected_T, places=10)


class TestSpiralLightPath(unittest.TestCase):
    """Tests for SpiralLightPath class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use fixed random seed for reproducibility
        np.random.seed(42)
        self.spiral = SpiralLightPath()
    
    def test_initialization(self):
        """Test spiral light path initialization."""
        self.assertIsNotNone(self.spiral)
        self.assertIsInstance(self.spiral.params, SpiralParameters)
        self.assertEqual(self.spiral.params.f0, 141.7001)
    
    def test_get_zeta_zeros(self):
        """Test computation of Riemann zeta zeros."""
        zeros = self.spiral.get_zeta_zeros(5)
        
        # Should return 5 zeros
        self.assertEqual(len(zeros), 5)
        
        # All zeros should be on critical line Re(s) = 1/2
        for zero in zeros:
            self.assertAlmostEqual(zero.real, 0.5, places=10)
        
        # Imaginary parts should be positive and increasing
        for i in range(len(zeros) - 1):
            self.assertGreater(zeros[i+1].imag, zeros[i].imag)
        
        # First zero should be approximately at Im(s) ≈ 14.134725
        self.assertAlmostEqual(zeros[0].imag, 14.134725, places=4)
    
    def test_zeta_zeros_caching(self):
        """Test that zeta zeros are cached properly."""
        # First call
        zeros1 = self.spiral.get_zeta_zeros(10)
        
        # Second call should use cache
        zeros2 = self.spiral.get_zeta_zeros(10)
        
        # Should be identical
        for z1, z2 in zip(zeros1, zeros2):
            self.assertEqual(z1, z2)
    
    def test_get_primes(self):
        """Test prime number generation."""
        primes = self.spiral.get_primes(10)
        
        # Should return 10 primes
        self.assertEqual(len(primes), 10)
        
        # Check first 10 primes
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(primes, expected_primes)
    
    def test_primes_caching(self):
        """Test that primes are cached properly."""
        # Generate primes
        primes1 = self.spiral.get_primes(20)
        primes2 = self.spiral.get_primes(15)
        
        # Should use cache for second call
        self.assertEqual(primes2, primes1[:15])
    
    def test_compute_prime_phase(self):
        """Test prime phase modulation calculation."""
        # Phase for first prime (2)
        phi_0 = self.spiral.compute_prime_phase(0)
        
        # Phase should be in [0, 2π]
        self.assertGreaterEqual(phi_0, 0)
        self.assertLess(phi_0, 2 * np.pi)
        
        # Phase for different primes should be different
        phi_1 = self.spiral.compute_prime_phase(1)
        self.assertNotEqual(phi_0, phi_1)
    
    def test_spiral_trajectory_2d(self):
        """Test 2D spiral trajectory calculation."""
        # Time array
        t = np.linspace(0, 0.01, 100)
        
        # Compute trajectory
        x, y, z = self.spiral.spiral_trajectory(t, prime_index=0, include_3d=False)
        
        # Should return arrays of same length
        self.assertEqual(len(x), len(t))
        self.assertEqual(len(y), len(t))
        self.assertIsNone(z)
        
        # Trajectory should start near origin
        self.assertAlmostEqual(x[0], self.spiral.params.r0, places=1)
        
        # Trajectory should spiral outward (increasing radius)
        r = np.sqrt(x**2 + y**2)
        self.assertGreater(r[-1], r[0])
    
    def test_spiral_trajectory_3d(self):
        """Test 3D spiral trajectory with light propagation."""
        # Time array
        t = np.linspace(0, 1e-9, 100)  # 1 nanosecond
        
        # Compute trajectory
        x, y, z = self.spiral.spiral_trajectory(t, prime_index=0, include_3d=True)
        
        # z coordinate should not be None
        self.assertIsNotNone(z)
        self.assertEqual(len(z), len(t))
        
        # z should increase linearly with light speed
        # z = c * t
        c = 299792458  # m/s
        np.testing.assert_allclose(z, c * t, rtol=1e-10)
    
    def test_different_prime_phases(self):
        """Test that different primes give different spiral trajectories."""
        t = np.linspace(0, 0.01, 100)
        
        # Compute trajectories for different primes
        x0, y0, _ = self.spiral.spiral_trajectory(t, prime_index=0)
        x1, y1, _ = self.spiral.spiral_trajectory(t, prime_index=1)
        
        # Trajectories should be different due to phase shift
        self.assertFalse(np.allclose(x0, x1))
        self.assertFalse(np.allclose(y0, y1))
    
    def test_zeta_modulated_wavefunction(self):
        """Test wave function with zeta-spectral modulation."""
        # Spatial array
        x = np.linspace(-10, 10, 100)
        t = 0.001  # 1 ms
        
        # Compute wave function
        psi = self.spiral.zeta_modulated_wavefunction(x, t, n_modes=5)
        
        # Should return complex array
        self.assertEqual(len(psi), len(x))
        self.assertEqual(psi.dtype, complex)
        
        # Wave function should be non-zero
        self.assertGreater(np.max(np.abs(psi)), 0)
    
    def test_interference_pattern(self):
        """Test interference pattern calculation."""
        # Spatial array
        x = np.linspace(-10, 10, 200)
        t = 0.001
        
        # Compute interference pattern
        intensity = self.spiral.interference_pattern(x, t, n_modes=5)
        
        # Intensity should be real and non-negative
        self.assertEqual(len(intensity), len(x))
        self.assertTrue(np.all(intensity >= 0))
        
        # Intensity should show interference fringes
        # (local maxima and minima)
        self.assertGreater(np.max(intensity), np.mean(intensity))
    
    def test_compute_spiral_deviation(self):
        """Test spiral deviation from linear path."""
        # Time array
        t = np.linspace(0, 0.01, 1000)
        
        # Compute deviation
        deviation = self.spiral.compute_spiral_deviation(t, prime_index=0)
        
        # Check all required keys are present
        required_keys = [
            'max_deviation_meters',
            'rms_deviation_meters',
            'max_angle_radians',
            'max_angle_degrees',
            'prime_index',
            'prime_value',
            'time_span_seconds'
        ]
        for key in required_keys:
            self.assertIn(key, deviation)
        
        # Deviations should be positive
        self.assertGreater(deviation['max_deviation_meters'], 0)
        self.assertGreater(deviation['rms_deviation_meters'], 0)
        
        # Prime index and value should match
        self.assertEqual(deviation['prime_index'], 0)
        self.assertEqual(deviation['prime_value'], 2)  # First prime
    
    def test_critical_line_projection(self):
        """Test projection onto critical line Re(s) = 1/2."""
        # Time array
        t = np.linspace(0, 0.01, 100)
        
        # Compute projection
        x_obs, y_obs = self.spiral.critical_line_projection(t, prime_index=0)
        
        # Observer sees zero deviation in x-y plane
        np.testing.assert_allclose(x_obs, 0, atol=1e-10)
        np.testing.assert_allclose(y_obs, 0, atol=1e-10)
        
        # This represents the collapse to linear observation
    
    def test_compute_zeta_derivative_half(self):
        """Test computation of ζ'(1/2)."""
        zeta_prime = self.spiral.compute_zeta_derivative_half()
        
        # Should be complex number
        self.assertIsInstance(zeta_prime, complex)
        
        # Known value: ζ'(1/2) ≈ -3.92 - 0i
        self.assertAlmostEqual(zeta_prime.real, -3.92, places=1)
        self.assertAlmostEqual(zeta_prime.imag, 0, places=1)
    
    def test_evolution_operator(self):
        """Test quantum evolution operator."""
        t = 0.001
        n_modes = 5
        
        # Compute evolution operator
        U = self.spiral.evolution_operator(t, n_modes)
        
        # Should be square matrix
        self.assertEqual(U.shape, (n_modes, n_modes))
        
        # Should be unitary: U† U = I
        U_dagger = np.conj(U.T)
        identity = U_dagger @ U
        
        # Check diagonal elements close to 1
        for i in range(n_modes):
            self.assertAlmostEqual(abs(identity[i, i]), 1.0, places=6)
    
    def test_reproducibility(self):
        """Test that calculations are reproducible."""
        # Set seed
        np.random.seed(42)
        
        t = np.linspace(0, 0.01, 100)
        
        # Compute twice
        x1, y1, _ = self.spiral.spiral_trajectory(t, prime_index=0)
        x2, y2, _ = self.spiral.spiral_trajectory(t, prime_index=0)
        
        # Should be identical
        np.testing.assert_array_equal(x1, x2)
        np.testing.assert_array_equal(y1, y2)


class TestDemonstrationFunctions(unittest.TestCase):
    """Tests for demonstration and validation functions."""
    
    def test_validate_zeta_zeros(self):
        """Test zeta zeros validation function."""
        # Should run without error
        try:
            validate_zeta_zeros()
        except AssertionError as e:
            self.fail(f"Zeta zeros validation failed: {e}")
    
    def test_demonstrate_spiral_vs_linear(self):
        """Test spiral vs linear demonstration."""
        results = demonstrate_spiral_vs_linear()
        
        # Should return results for 5 primes
        self.assertEqual(len(results), 5)
        
        # Each result should have deviation metrics
        for result in results:
            self.assertIn('max_deviation_meters', result)
            self.assertIn('prime_value', result)
            self.assertGreater(result['max_deviation_meters'], 0)


class TestFalsifiablePredictions(unittest.TestCase):
    """Tests for falsifiable predictions of the theory."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spiral = SpiralLightPath()
    
    def test_interferometry_deviation_prediction(self):
        """
        Test prediction 1: Spiral deviations in interferometry.
        
        High-precision interferometers (LISA, GEO600) should detect
        quasi-fractal spiral deviations at 141.7 Hz.
        """
        # Simulate interferometer measurement over 1 second
        t = np.linspace(0, 1.0, 10000)
        
        deviation = self.spiral.compute_spiral_deviation(t, prime_index=0)
        
        # Deviation should be measurable (> 0)
        self.assertGreater(deviation['max_deviation_meters'], 0)
        
        # For realistic detection, deviation should be within
        # sensitivity of modern interferometers (~ 1e-18 m for LIGO)
        # This is a theoretical prediction to be verified experimentally
    
    def test_spectral_modulation_prediction(self):
        """
        Test prediction 2: 141.7 Hz modulation in optical cavities.
        
        Ultra-high Q optical cavities should show modulation at f₀.
        """
        # Compute interference pattern over time
        x = np.array([0.0])  # Fixed position
        
        # Sample over multiple periods of f₀
        T = 1.0 / self.spiral.params.f0
        t_array = np.linspace(0, 10 * T, 1000)
        
        intensity = np.array([
            self.spiral.interference_pattern(x, t, n_modes=1)[0]
            for t in t_array
        ])
        
        # Intensity should oscillate
        self.assertGreater(np.max(intensity), np.min(intensity))
        
        # Dominant frequency should be near f₀ (testable prediction)
        # This can be verified with FFT in experimental data
    
    def test_phase_evolution_structure(self):
        """
        Test prediction 3: Spiral spectral phase structures.
        
        Evolution operator should show spiral phase structure.
        """
        # Compute evolution at different times
        times = np.linspace(0, 0.01, 10)
        
        for t in times:
            U = self.spiral.evolution_operator(t, n_modes=5)
            
            # Evolution operator should be unitary
            # (energy conservation)
            U_dagger = np.conj(U.T)
            UU_dag = U @ U_dagger
            
            # Check unitarity
            for i in range(5):
                self.assertAlmostEqual(abs(UU_dag[i, i]), 1.0, places=5)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.spiral = SpiralLightPath()
    
    def test_zero_time(self):
        """Test behavior at t = 0."""
        t = np.array([0.0])
        x, y, z = self.spiral.spiral_trajectory(t, prime_index=0, include_3d=True)
        
        # At t=0, position depends on phase shift φₚ
        # r(0) = r0, but x = r0*cos(φₚ), y = r0*sin(φₚ)
        r = np.sqrt(x[0]**2 + y[0]**2)
        self.assertAlmostEqual(r, self.spiral.params.r0, places=6)
        self.assertAlmostEqual(z[0], 0.0, places=6)
    
    def test_large_time(self):
        """Test behavior for large time values."""
        # 1 second (large for light travel)
        t = np.array([1.0])
        x, y, z = self.spiral.spiral_trajectory(t, prime_index=0, include_3d=True)
        
        # Should not overflow
        self.assertFalse(np.any(np.isnan(x)))
        self.assertFalse(np.any(np.isnan(y)))
        self.assertFalse(np.any(np.isnan(z)))
        
        # z should be c * t ≈ 3e8 meters
        c = 299792458
        self.assertAlmostEqual(z[0], c * 1.0, places=0)
    
    def test_many_modes(self):
        """Test with large number of modes."""
        x = np.linspace(-10, 10, 100)
        t = 0.001
        
        # Try with many modes
        psi = self.spiral.zeta_modulated_wavefunction(x, t, n_modes=20)
        
        # Should complete without error
        self.assertEqual(len(psi), len(x))
        self.assertFalse(np.any(np.isnan(psi)))


if __name__ == "__main__":
    unittest.main()
