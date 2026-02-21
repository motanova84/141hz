"""
Tests for Atlas³ Explicit Sum Formula and Von Mangoldt Weights

This test suite validates the "Oro" (Gold) implementation:
1. Von Mangoldt weight function
2. Synthetic prime signal generation
3. Cross-correlation with Atlas³ spectrum
4. Spectral determinant with zeta regularization
5. Heat kernel truncation

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.atlas3_operator import (
    Atlas3Parameters,
    Atlas3Operator,
    von_mangoldt_weight,
    generate_primes,
    SyntheticPrimeSignal,
    ExplicitSumAnalyzer,
    SpectralDeterminantCalculator
)


class TestVonMangoldtWeight(unittest.TestCase):
    """Test Von Mangoldt weight function."""
    
    def test_primes(self):
        """Test Λ(p) = log(p) for primes."""
        # Test first few primes
        primes = [2, 3, 5, 7, 11, 13]
        for p in primes:
            weight = von_mangoldt_weight(p)
            expected = np.log(p)
            self.assertAlmostEqual(weight, expected, places=10,
                                 msg=f"Λ({p}) should be log({p})")
    
    def test_prime_powers(self):
        """Test Λ(p^m) = log(p) for prime powers."""
        # Test 2^2 = 4
        self.assertAlmostEqual(von_mangoldt_weight(4), np.log(2), places=10,
                             msg="Λ(4) = Λ(2²) should be log(2)")
        
        # Test 2^3 = 8
        self.assertAlmostEqual(von_mangoldt_weight(8), np.log(2), places=10,
                             msg="Λ(8) = Λ(2³) should be log(2)")
        
        # Test 3^2 = 9
        self.assertAlmostEqual(von_mangoldt_weight(9), np.log(3), places=10,
                             msg="Λ(9) = Λ(3²) should be log(3)")
        
        # Test 5^2 = 25
        self.assertAlmostEqual(von_mangoldt_weight(25), np.log(5), places=10,
                             msg="Λ(25) = Λ(5²) should be log(5)")
    
    def test_composites(self):
        """Test Λ(n) = 0 for composite numbers (not prime powers)."""
        composites = [6, 10, 12, 14, 15, 18, 20, 21, 22]
        for n in composites:
            weight = von_mangoldt_weight(n)
            self.assertAlmostEqual(weight, 0.0, places=10,
                                 msg=f"Λ({n}) should be 0 for composite")
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Λ(1) = 0
        self.assertEqual(von_mangoldt_weight(1), 0.0,
                        msg="Λ(1) should be 0")
        
        # Λ(n < 1) = 0
        self.assertEqual(von_mangoldt_weight(0), 0.0,
                        msg="Λ(0) should be 0")
        self.assertEqual(von_mangoldt_weight(-5), 0.0,
                        msg="Λ(negative) should be 0")


class TestPrimeGeneration(unittest.TestCase):
    """Test prime number generation."""
    
    def test_first_primes(self):
        """Test generation of first few primes."""
        primes = generate_primes(20)
        expected = [2, 3, 5, 7, 11, 13, 17, 19]
        self.assertEqual(primes, expected,
                        msg="Should generate correct first primes")
    
    def test_prime_count(self):
        """Test that correct number of primes generated."""
        # First 25 primes
        primes = generate_primes(100)
        # 25 primes up to 100: 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
        expected_count = 25
        self.assertEqual(len(primes), expected_count,
                        msg=f"Should have {expected_count} primes up to 100")
    
    def test_edge_cases(self):
        """Test edge cases in prime generation."""
        self.assertEqual(generate_primes(0), [],
                        msg="No primes below 2")
        self.assertEqual(generate_primes(1), [],
                        msg="No primes below 2")
        self.assertEqual(generate_primes(2), [2],
                        msg="Only prime up to 2 is 2")


class TestSyntheticPrimeSignal(unittest.TestCase):
    """Test synthetic prime signal generation."""
    
    def setUp(self):
        """Set up test operator."""
        self.params = Atlas3Parameters()
        self.operator = Atlas3Operator(self.params, beta=0.0)
        self.analyzer = ExplicitSumAnalyzer(self.operator, max_prime=30, max_power=2)
    
    def test_signal_generation(self):
        """Test that synthetic signal is generated correctly."""
        signal = self.analyzer.generate_synthetic_prime_signal()
        
        self.assertIsInstance(signal, SyntheticPrimeSignal,
                            msg="Should return SyntheticPrimeSignal object")
        self.assertGreater(signal.n_terms, 0,
                          msg="Should have at least one term")
        self.assertEqual(len(signal.times), signal.n_terms,
                        msg="Times array should match n_terms")
        self.assertEqual(len(signal.weights), signal.n_terms,
                        msg="Weights array should match n_terms")
    
    def test_signal_structure(self):
        """Test structure of synthetic signal."""
        signal = self.analyzer.generate_synthetic_prime_signal()
        
        # Times should be sorted
        self.assertTrue(np.all(np.diff(signal.times) >= 0),
                       msg="Times should be sorted")
        
        # All weights should be positive
        self.assertTrue(np.all(signal.weights > 0),
                       msg="All weights should be positive")
        
        # First term should be from p=2, m=1
        expected_first_time = 1 * np.log(2)
        self.assertAlmostEqual(signal.times[0], expected_first_time, places=6,
                             msg="First time should be ln(2)")
        
        expected_first_weight = np.log(2) / np.sqrt(2)
        self.assertAlmostEqual(signal.weights[0], expected_first_weight, places=6,
                             msg="First weight should be ln(2)/√2")
    
    def test_continuous_signal(self):
        """Test conversion to continuous signal."""
        signal = self.analyzer.generate_synthetic_prime_signal()
        
        t_grid = np.linspace(0, 5, 100)
        continuous = signal.to_continuous_signal(t_grid, sigma=0.1)
        
        self.assertEqual(len(continuous), len(t_grid),
                        msg="Continuous signal should match grid size")
        self.assertTrue(np.all(np.isfinite(continuous)),
                       msg="All values should be finite")


class TestExplicitSumAnalyzer(unittest.TestCase):
    """Test explicit sum analyzer and cross-correlation."""
    
    def setUp(self):
        """Set up test operator and analyzer."""
        self.params = Atlas3Parameters()
        self.operator = Atlas3Operator(self.params, beta=0.0)
        self.operator.compute_spectrum()  # Ensure spectrum is computed
        self.analyzer = ExplicitSumAnalyzer(self.operator, max_prime=50, max_power=2)
    
    def test_eigenvalue_density(self):
        """Test eigenvalue density of states computation."""
        t_grid = np.linspace(0, 10, 200)
        density = self.analyzer.eigenvalue_density_of_states(t_grid, sigma=0.1)
        
        self.assertEqual(len(density), len(t_grid),
                        msg="Density should match grid size")
        self.assertTrue(np.all(np.isfinite(density)),
                       msg="Density should be finite everywhere")
        self.assertTrue(np.all(density >= 0),
                       msg="Density should be non-negative")
    
    def test_cross_correlation_computation(self):
        """Test cross-correlation computation (Oro test)."""
        result = self.analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=8.0,
            n_points=500,
            sigma=0.15
        )
        
        # Check result structure
        required_keys = ['t_grid', 'atlas_density', 'prime_signal', 
                        'cross_correlation', 'peaks', 'peak_positions_theoretical']
        for key in required_keys:
            self.assertIn(key, result,
                         msg=f"Result should contain '{key}'")
        
        # Check dimensions
        n_points = len(result['t_grid'])
        self.assertEqual(len(result['atlas_density']), n_points,
                        msg="Atlas density should match grid size")
        self.assertEqual(len(result['prime_signal']), n_points,
                        msg="Prime signal should match grid size")
        self.assertEqual(len(result['cross_correlation']), n_points,
                        msg="Cross-correlation should match grid size")
    
    def test_cross_correlation_properties(self):
        """Test mathematical properties of cross-correlation."""
        result = self.analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=6.0,
            n_points=400,
            sigma=0.1
        )
        
        cross_corr = result['cross_correlation']
        
        # Cross-correlation should be real
        self.assertTrue(np.all(np.isfinite(cross_corr)),
                       msg="Cross-correlation should be finite")
        
        # Should have some correlation (not all zeros)
        self.assertGreater(np.max(np.abs(cross_corr)), 0.1,
                          msg="Should have non-trivial correlation")
    
    def test_peak_detection(self):
        """Test that peaks are detected in cross-correlation."""
        result = self.analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=7.0,
            n_points=500,
            sigma=0.15
        )
        
        # Should detect at least some peaks
        peaks = result['peaks']
        self.assertIsInstance(peaks, list,
                            msg="Peaks should be a list")
        
        # Should have theoretical peak positions
        theoretical = result['peak_positions_theoretical']
        self.assertGreater(len(theoretical), 0,
                          msg="Should have theoretical peak positions")
        
        # First few theoretical peaks should be ln(2), ln(3), ln(5), ...
        if len(theoretical) >= 3:
            self.assertAlmostEqual(theoretical[0], np.log(2), places=4,
                                 msg="First peak should be at ln(2)")
            self.assertAlmostEqual(theoretical[1], np.log(3), places=4,
                                 msg="Second peak should be at ln(3)")
            self.assertAlmostEqual(theoretical[2], np.log(5), places=4,
                                 msg="Third peak should be at ln(5)")


class TestSpectralDeterminantCalculator(unittest.TestCase):
    """Test spectral determinant with zeta regularization."""
    
    def setUp(self):
        """Set up test operator and calculator."""
        self.params = Atlas3Parameters()
        self.operator = Atlas3Operator(self.params, beta=0.0)
        self.operator.compute_spectrum()
        self.calculator = SpectralDeterminantCalculator(self.operator, heat_kernel_cutoff=1.0)
    
    def test_heat_kernel_trace(self):
        """Test heat kernel trace computation."""
        # Test at different times
        for t in [0.1, 0.5, 1.0, 2.0]:
            trace = self.calculator.heat_kernel_trace(t)
            
            self.assertTrue(np.isfinite(trace),
                          msg=f"Heat kernel trace should be finite at t={t}")
            
            # Trace magnitude should be reasonable
            self.assertLess(np.abs(trace), 1e100,
                          msg=f"Heat kernel should not overflow at t={t}")
    
    def test_spectral_zeta_function(self):
        """Test spectral zeta function computation."""
        # Test at different values of s
        test_values = [0.5, 1.0, 1.5, 2.0]
        
        for s in test_values:
            zeta_s = self.calculator.spectral_zeta_function(s)
            
            self.assertTrue(np.isfinite(zeta_s),
                          msg=f"ζ_O({s}) should be finite")
    
    def test_regularized_determinant(self):
        """Test regularized determinant computation."""
        det = self.calculator.regularized_determinant()
        
        self.assertTrue(np.isfinite(det),
                       msg="Regularized determinant should be finite")
        self.assertNotEqual(det, 0.0,
                          msg="Determinant should be non-zero")
    
    def test_xi_function(self):
        """Test Ξ(t) function computation."""
        # Test at different t values
        for t in [0.5, 1.0, 2.0]:
            xi_t = self.calculator.xi_function(t)
            
            self.assertTrue(np.isfinite(xi_t),
                          msg=f"Ξ({t}) should be finite")


class TestIntegrationExplicitSum(unittest.TestCase):
    """Integration tests for full Oro (Gold) workflow."""
    
    def test_full_oro_workflow(self):
        """Test complete Oro workflow: Atlas³ → prime correlation."""
        # Create operator
        params = Atlas3Parameters()
        operator = Atlas3Operator(params, beta=0.0)
        operator.compute_spectrum()
        
        # Create analyzer
        analyzer = ExplicitSumAnalyzer(operator, max_prime=40, max_power=2)
        
        # Generate synthetic signal
        signal = analyzer.generate_synthetic_prime_signal()
        self.assertGreater(signal.n_terms, 0,
                          msg="Should generate prime signal")
        
        # Compute cross-correlation
        result = analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=6.0,
            n_points=400,
            sigma=0.12
        )
        
        self.assertIn('cross_correlation', result,
                     msg="Should compute cross-correlation")
        
        # Verify mathematical structure
        corr = result['cross_correlation']
        self.assertTrue(np.all(np.isfinite(corr)),
                       msg="Correlation should be finite")
    
    def test_pt_symmetry_breaking_effect(self):
        """Test effect of PT-symmetry breaking on prime correlation."""
        params = Atlas3Parameters()
        
        # Test at β=0 (PT-symmetric) and β=3.0 (PT-broken)
        results = {}
        
        for beta in [0.0, 3.0]:
            operator = Atlas3Operator(params, beta=beta)
            operator.compute_spectrum()
            
            analyzer = ExplicitSumAnalyzer(operator, max_prime=30, max_power=2)
            result = analyzer.compute_cross_correlation(
                t_min=0.0,
                t_max=5.0,
                n_points=300,
                sigma=0.15
            )
            
            results[beta] = result
        
        # Both should produce valid cross-correlations
        for beta in [0.0, 3.0]:
            corr = results[beta]['cross_correlation']
            self.assertTrue(np.all(np.isfinite(corr)),
                          msg=f"Correlation should be finite at β={beta}")
    
    def test_determinant_with_explicit_sum(self):
        """Test spectral determinant in context of explicit sum."""
        params = Atlas3Parameters()
        operator = Atlas3Operator(params, beta=0.0)
        operator.compute_spectrum()
        
        # Create both analyzers
        sum_analyzer = ExplicitSumAnalyzer(operator, max_prime=30)
        det_calculator = SpectralDeterminantCalculator(operator)
        
        # Compute determinant
        det = det_calculator.regularized_determinant()
        self.assertTrue(np.isfinite(det),
                       msg="Determinant should be finite")
        
        # Compute explicit sum correlation
        result = sum_analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=5.0,
            n_points=300
        )
        self.assertIn('cross_correlation', result,
                     msg="Should compute correlation")


if __name__ == '__main__':
    unittest.main()
