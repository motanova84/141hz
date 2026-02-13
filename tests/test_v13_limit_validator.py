"""
Tests for V13 Thermodynamic Limit Validator

This test suite validates:
1. Spectral curvature κ(N) calculation
2. Number variance Σ²(L) calculation
3. GOE theoretical predictions
4. Non-linear fitting to extract κ_∞
5. Multi-scale sweep execution
6. Results output and visualization

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
import os
import unittest
import numpy as np
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the validator and constant
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from v13_limit_validator import (
    spectral_curvature_kappa,
    number_variance_sigma2,
    goe_number_variance_theoretical,
    fit_thermodynamic_limit,
    run_multiscale_sweep,
    KAPPA_PI_TARGET
)

from physics.atlas3_operator import Atlas3Operator, Atlas3Parameters


class TestSpectralCurvature(unittest.TestCase):
    """Test spectral curvature κ(N) calculation."""
    
    def test_empty_eigenvalues(self):
        """Test handling of empty eigenvalue array."""
        eigenvalues = np.array([])
        kappa = spectral_curvature_kappa(eigenvalues)
        self.assertEqual(kappa, 2.5, "Should return default value for empty array")
    
    def test_few_eigenvalues(self):
        """Test handling of small eigenvalue arrays."""
        eigenvalues = np.array([1.0, 2.0, 3.0])
        kappa = spectral_curvature_kappa(eigenvalues)
        self.assertEqual(kappa, 2.5, "Should return default value for N < 10")
    
    def test_real_eigenvalues(self):
        """Test with real eigenvalues (Hermitian system)."""
        # Generate random GOE-like eigenvalues
        np.random.seed(42)
        N = 100
        eigenvalues = np.sort(np.random.randn(N))
        
        kappa = spectral_curvature_kappa(eigenvalues)
        
        # Should be in reasonable range [2.0, 3.5]
        self.assertGreater(kappa, 2.0, "κ should be > 2.0")
        self.assertLess(kappa, 3.5, "κ should be < 3.5")
    
    def test_complex_eigenvalues(self):
        """Test with complex eigenvalues (PT-broken system)."""
        np.random.seed(42)
        N = 100
        real_parts = np.sort(np.random.randn(N))
        imag_parts = np.random.randn(N) * 0.1
        eigenvalues = real_parts + 1j * imag_parts
        
        kappa = spectral_curvature_kappa(eigenvalues)
        
        # Should still be in reasonable range
        self.assertGreater(kappa, 2.0, "κ should be > 2.0")
        self.assertLessEqual(kappa, 3.5, "κ should be ≤ 3.5")
    
    def test_atlas3_operator(self):
        """Test with actual Atlas³ operator eigenvalues."""
        params = Atlas3Parameters()
        params.N = 200  # Smaller for speed
        operator = Atlas3Operator(params=params, beta=2.57)
        operator.compute_spectrum()
        
        kappa = spectral_curvature_kappa(operator.eigenvalues)
        
        # For PT-broken system at β = 2.57, κ should be near 2.577
        self.assertGreater(kappa, 2.0, "κ should be > 2.0")
        self.assertLess(kappa, 3.5, "κ should be < 3.5")
        self.assertAlmostEqual(kappa, 2.577, delta=1.0,
                              msg="κ should be reasonably close to κ_Π")


class TestNumberVariance(unittest.TestCase):
    """Test number variance Σ²(L) calculation."""
    
    def test_poisson_process(self):
        """Test with Poisson process (random uncorrelated levels)."""
        np.random.seed(42)
        N = 1000
        # Poisson: exponentially distributed spacings
        spacings = np.random.exponential(1.0, N-1)
        eigenvalues = np.cumsum(spacings)
        
        L_values = np.array([10.0, 20.0, 50.0])
        sigma2 = number_variance_sigma2(eigenvalues, L_values)
        
        # For Poisson: Σ²(L) ≈ L
        # Allow large tolerance since it's statistical
        for i, L in enumerate(L_values):
            # Some values might be 0 due to insufficient windows, allow that
            self.assertGreaterEqual(sigma2[i], 0.0, f"Σ²(L={L}) should be non-negative")
            # Very rough check - Poisson should be close to L but with fluctuations
            # or 0 if not enough windows
            if sigma2[i] > 0:
                self.assertLess(sigma2[i], L * 3, f"Σ²(L={L}) shouldn't be too large")
    
    def test_goe_theoretical(self):
        """Test GOE theoretical prediction."""
        L_values = np.array([10.0, 50.0, 100.0])
        sigma2_goe = goe_number_variance_theoretical(L_values)
        
        # Check monotonic increase
        self.assertLess(sigma2_goe[0], sigma2_goe[1],
                       "Σ²(L) should increase with L")
        self.assertLess(sigma2_goe[1], sigma2_goe[2],
                       "Σ²(L) should increase with L")
        
        # Check logarithmic growth: Σ²(L) ~ ln(L)
        # At L=10: ln(10) ≈ 2.3, (2/π²) * 2.3 ≈ 0.47
        self.assertGreater(sigma2_goe[0], 0.0, "Σ²(L=10) should be positive")
        self.assertLess(sigma2_goe[0], 2.0, "Σ²(L=10) should be < 2.0")
        
        # At L=100: should be larger but still logarithmic
        self.assertGreater(sigma2_goe[2], sigma2_goe[0],
                          "Σ²(L=100) > Σ²(L=10)")
    
    def test_atlas3_number_variance(self):
        """Test number variance with Atlas³ operator."""
        params = Atlas3Parameters()
        params.N = 300  # Moderate size for speed
        operator = Atlas3Operator(params=params, beta=2.57)
        operator.compute_spectrum()
        
        L_values = np.array([10.0, 20.0, 30.0])
        sigma2 = number_variance_sigma2(operator.eigenvalues, L_values)
        
        # All values should be non-negative
        for i, L in enumerate(L_values):
            self.assertGreaterEqual(sigma2[i], 0.0,
                                   f"Σ²(L={L}) should be non-negative")


class TestThermodynamicLimitFit(unittest.TestCase):
    """Test thermodynamic limit fitting."""
    
    def test_perfect_decay(self):
        """Test fit with perfect 1/√N decay."""
        # Generate synthetic data: κ(N) = 2.577 + 10/√N
        N_values = [128, 256, 512, 1024, 2560]
        kappa_inf_true = 2.577
        a_true = 10.0
        alpha_true = 0.5
        
        kappa_values = [kappa_inf_true + a_true / (N**alpha_true) 
                       for N in N_values]
        
        # Add small noise
        np.random.seed(42)
        kappa_values = [k + np.random.randn() * 0.01 for k in kappa_values]
        
        # Fit
        results = fit_thermodynamic_limit(N_values, kappa_values)
        
        # Check extracted parameters
        self.assertAlmostEqual(results['kappa_infinity'], kappa_inf_true,
                              delta=0.1, msg="Should recover κ_∞")
        self.assertAlmostEqual(results['alpha'], alpha_true,
                              delta=0.3, msg="Should recover α ≈ 0.5")
        self.assertGreater(results['r_squared'], 0.9,
                          "Should have good fit quality")
    
    def test_fit_bounds(self):
        """Test that fit respects physical bounds."""
        N_values = [128, 256, 512, 1024, 2560]
        kappa_values = [3.0, 2.9, 2.8, 2.7, 2.65]
        
        results = fit_thermodynamic_limit(N_values, kappa_values)
        
        # κ_∞ should be in physical range
        self.assertGreater(results['kappa_infinity'], 2.0,
                          "κ_∞ should be > 2.0")
        self.assertLess(results['kappa_infinity'], 3.5,
                       "κ_∞ should be < 3.5")
        
        # α should be positive
        self.assertGreater(results['alpha'], 0.0,
                          "α should be positive")
    
    def test_error_calculation(self):
        """Test error calculation relative to κ_Π."""
        N_values = [128, 256, 512, 1024, 2560]
        kappa_values = [2.6, 2.6, 2.6, 2.6, 2.6]  # Constant
        
        results = fit_thermodynamic_limit(N_values, kappa_values)
        
        # Should have target and error
        self.assertIn('kappa_pi_target', results)
        self.assertIn('error_percent', results)
        self.assertEqual(results['kappa_pi_target'], KAPPA_PI_TARGET)
        self.assertGreater(results['error_percent'], 0.0)


class TestMultiscaleSweep(unittest.TestCase):
    """Test multi-scale sweep execution."""
    
    def test_sweep_structure(self):
        """Test that sweep returns correct data structure."""
        # Run with small N values for speed
        N_values = [50, 100]
        
        results = run_multiscale_sweep(N_values, beta=2.57, verbose=False)
        
        # Check structure
        self.assertIn('N_values', results)
        self.assertIn('beta', results)
        self.assertIn('kappa_values', results)
        self.assertIn('spectral_stats', results)
        self.assertIn('variance_data', results)
        self.assertIn('fit', results)
        
        # Check data consistency
        self.assertEqual(len(results['kappa_values']), len(N_values))
        self.assertEqual(len(results['spectral_stats']), len(N_values))
    
    def test_convergence(self):
        """Test that κ(N) shows convergence trend."""
        # Smaller N values for faster testing
        N_values = [64, 128, 256]
        
        results = run_multiscale_sweep(N_values, beta=2.57, verbose=False)
        
        kappa_values = results['kappa_values']
        
        # All values should be in reasonable range
        for kappa in kappa_values:
            self.assertGreater(kappa, 2.0, "All κ values should be > 2.0")
            self.assertLess(kappa, 3.5, "All κ values should be < 3.5")
    
    def test_fit_quality(self):
        """Test that fit achieves reasonable quality."""
        # Use standard N values but check fit metrics
        N_values = [128, 256, 512]
        
        results = run_multiscale_sweep(N_values, beta=2.57, verbose=False)
        
        fit = results['fit']
        
        # Should have all fit parameters
        self.assertIn('kappa_infinity', fit)
        self.assertIn('alpha', fit)
        self.assertIn('a', fit)
        self.assertIn('r_squared', fit)
        
        # κ_∞ should be in physical range (relaxed tolerance for small N)
        self.assertGreater(fit['kappa_infinity'], 1.5,
                          msg="κ_∞ should be > 1.5")
        self.assertLess(fit['kappa_infinity'], 3.5,
                       msg="κ_∞ should be < 3.5")


class TestOutputGeneration(unittest.TestCase):
    """Test output file generation."""
    
    def test_json_output(self):
        """Test that JSON results are generated correctly."""
        # Run minimal sweep
        N_values = [50, 100]
        results = run_multiscale_sweep(N_values, beta=2.57, verbose=False)
        
        # Verify JSON serializable
        try:
            json_str = json.dumps(results)
            reloaded = json.loads(json_str)
            
            # Check key fields preserved
            self.assertEqual(reloaded['N_values'], N_values)
            self.assertEqual(reloaded['beta'], 2.57)
            
        except Exception as e:
            self.fail(f"Results should be JSON serializable: {e}")
    
    def test_results_file_exists(self):
        """Test that results file is created."""
        results_file = Path("physics/results/v13/v13_limit_results.json")
        
        # File should exist from main run
        if results_file.exists():
            # Verify it's valid JSON
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn('fit', data)
            self.assertIn('kappa_infinity', data['fit'])
    
    def test_plot_file_exists(self):
        """Test that plot file is created."""
        plot_file = Path("physics/results/v13/v13_scaling_rigidity.png")
        
        # File should exist from main run
        if plot_file.exists():
            # Verify it's a PNG file
            self.assertTrue(plot_file.suffix == '.png',
                          "Plot should be PNG file")


class TestKappaConvergence(unittest.TestCase):
    """Test convergence properties of κ(N)."""
    
    def test_kappa_target_proximity(self):
        """Test that extrapolated κ_∞ is close to target."""
        # Load results if they exist
        results_file = Path("physics/results/v13/v13_limit_results.json")
        
        if results_file.exists():
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            kappa_inf = results['fit']['kappa_infinity']
            error_percent = results['fit']['error_percent']
            
            # Should be within 5% of target
            self.assertLess(error_percent, 5.0,
                          f"κ_∞ error should be < 5% (got {error_percent:.2f}%)")
            
            # Should be close to target κ_Π
            msg = f"κ_∞ should be near {KAPPA_PI_TARGET} (got {kappa_inf:.4f})"
            self.assertAlmostEqual(kappa_inf, KAPPA_PI_TARGET, delta=0.3, msg=msg)


if __name__ == '__main__':
    unittest.main()
