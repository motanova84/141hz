#!/usr/bin/env python3
"""
Unit tests for Superconducting Gravimeter Sensitivity Analysis
"""

import unittest
import numpy as np
from sg_sensitivity_analysis import (
    SGSpecifications,
    SGSensitivityAnalyzer
)


class TestSGSpecifications(unittest.TestCase):
    """Test SG specifications dataclass."""
    
    def test_default_values(self):
        """Test default specification values."""
        specs = SGSpecifications()
        self.assertEqual(specs.sigma_single, 1e-11)
        self.assertEqual(specs.f_sampling, 1.0)
        self.assertEqual(specs.f_target, 141.7001)
    
    def test_custom_values(self):
        """Test custom specification values."""
        specs = SGSpecifications(
            sigma_single=2e-11,
            f_sampling=2.0,
            f_target=100.0
        )
        self.assertEqual(specs.sigma_single, 2e-11)
        self.assertEqual(specs.f_sampling, 2.0)
        self.assertEqual(specs.f_target, 100.0)
    
    def test_validation(self):
        """Test that invalid values raise errors."""
        with self.assertRaises(ValueError):
            SGSpecifications(sigma_single=0)
        
        with self.assertRaises(ValueError):
            SGSpecifications(sigma_single=-1e-11)
        
        with self.assertRaises(ValueError):
            SGSpecifications(f_sampling=0)
        
        with self.assertRaises(ValueError):
            SGSpecifications(f_target=-100)


class TestSGSensitivityAnalyzer(unittest.TestCase):
    """Test SG sensitivity analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SGSensitivityAnalyzer()
    
    def test_required_noise_level(self):
        """Test required noise level calculation."""
        # For A = 1e-12 g, SNR = 5:
        # σ_required = 1e-12 / 5 = 2e-13 g
        sigma_req = self.analyzer.required_noise_level(1e-12, 5.0)
        self.assertAlmostEqual(sigma_req, 2e-13, places=20)
        
        # For A = 1e-13 g, SNR = 5:
        # σ_required = 1e-13 / 5 = 2e-14 g
        sigma_req = self.analyzer.required_noise_level(1e-13, 5.0)
        self.assertAlmostEqual(sigma_req, 2e-14, places=21)
    
    def test_required_samples_case1(self):
        """Test required samples for A = 1e-12 g."""
        # From problem statement:
        # N_samples = (σ_single / σ_required)²
        #           = (10⁻¹¹ / 2×10⁻¹³)²
        #           = 2500
        n_samples = self.analyzer.required_samples(1e-12, 5.0)
        self.assertEqual(n_samples, 2500)
    
    def test_required_samples_case2(self):
        """Test required samples for A = 1e-13 g."""
        # From problem statement:
        # N_samples = (10⁻¹¹ / 2×10⁻¹⁴)²
        #           = 2.5×10⁵
        n_samples = self.analyzer.required_samples(1e-13, 5.0)
        self.assertEqual(n_samples, 250000)
    
    def test_observation_time_case1(self):
        """Test observation time for A = 1e-12 g."""
        # From problem statement:
        # Time = 2500 s ≈ 42 minutes
        time_seconds = self.analyzer.observation_time(1e-12, 5.0)
        self.assertEqual(time_seconds, 2500)
        
        time_info = self.analyzer.observation_time_formatted(1e-12, 5.0)
        self.assertAlmostEqual(time_info['minutes'], 41.67, places=1)
    
    def test_observation_time_case2(self):
        """Test observation time for A = 1e-13 g."""
        # From problem statement:
        # Time = 2.5×10⁵ s ≈ 3 days
        time_seconds = self.analyzer.observation_time(1e-13, 5.0)
        self.assertEqual(time_seconds, 250000)
        
        time_info = self.analyzer.observation_time_formatted(1e-13, 5.0)
        self.assertAlmostEqual(time_info['days'], 2.89, places=1)
    
    def test_is_feasible_case1(self):
        """Test feasibility for A = 1e-12 g."""
        # Should be feasible (< 1 day)
        feasible = self.analyzer.is_feasible(1e-12, 5.0, max_observation_days=30)
        self.assertTrue(feasible)
    
    def test_is_feasible_case2(self):
        """Test feasibility for A = 1e-13 g."""
        # Should be feasible (~3 days < 30 days)
        feasible = self.analyzer.is_feasible(1e-13, 5.0, max_observation_days=30)
        self.assertTrue(feasible)
    
    def test_is_feasible_strict(self):
        """Test feasibility with strict time constraint."""
        # Should not be feasible with 1 day limit for A = 1e-13 g
        feasible = self.analyzer.is_feasible(1e-13, 5.0, max_observation_days=1)
        self.assertFalse(feasible)
    
    def test_analyze_amplitude_range(self):
        """Test amplitude range analysis."""
        results = self.analyzer.analyze_amplitude_range(
            amplitude_min=1e-13,
            amplitude_max=1e-12,
            n_points=3,
            target_snr=5.0
        )
        
        self.assertEqual(len(results['analyses']), 3)
        self.assertEqual(results['target_snr'], 5.0)
        
        # Check first and last points
        first = results['analyses'][0]
        last = results['analyses'][-1]
        
        self.assertAlmostEqual(first['amplitude'], 1e-13, places=20)
        self.assertAlmostEqual(last['amplitude'], 1e-12, places=19)
        
        # All should be feasible
        for analysis in results['analyses']:
            self.assertTrue(analysis['feasible'])
    
    def test_invalid_inputs(self):
        """Test that invalid inputs raise errors."""
        with self.assertRaises(ValueError):
            self.analyzer.required_noise_level(0, 5.0)
        
        with self.assertRaises(ValueError):
            self.analyzer.required_noise_level(-1e-12, 5.0)
        
        with self.assertRaises(ValueError):
            self.analyzer.required_noise_level(1e-12, 0)
        
        with self.assertRaises(ValueError):
            self.analyzer.required_noise_level(1e-12, -5.0)
    
    def test_different_snr_targets(self):
        """Test with different SNR targets."""
        # Higher SNR requires more samples
        n_samples_snr5 = self.analyzer.required_samples(1e-12, 5.0)
        n_samples_snr10 = self.analyzer.required_samples(1e-12, 10.0)
        
        self.assertGreater(n_samples_snr10, n_samples_snr5)
        
        # For SNR = 10 with A = 1e-12:
        # σ_required = 1e-12 / 10 = 1e-13
        # N = (1e-11 / 1e-13)² = 10000
        self.assertEqual(n_samples_snr10, 10000)
    
    def test_custom_specs(self):
        """Test with custom SG specifications."""
        # Double the noise level
        custom_specs = SGSpecifications(sigma_single=2e-11)
        analyzer = SGSensitivityAnalyzer(custom_specs)
        
        # Should need 4x more samples (noise squared)
        n_samples_default = self.analyzer.required_samples(1e-12, 5.0)
        n_samples_custom = analyzer.required_samples(1e-12, 5.0)
        
        self.assertEqual(n_samples_custom, 4 * n_samples_default)


class TestProblemStatementCompliance(unittest.TestCase):
    """
    Test compliance with exact problem statement specifications.
    """
    
    def setUp(self):
        """Set up analyzer with exact problem statement specs."""
        specs = SGSpecifications(
            sigma_single=1e-11,  # g @ 1 Hz
            f_sampling=1.0        # Hz
        )
        self.analyzer = SGSensitivityAnalyzer(specs)
    
    def test_case1_amplitude_1e12(self):
        """
        Verify Case 1: A = 10⁻¹² g, SNR = 5
        
        Expected from problem statement:
        - σ_required = 2×10⁻¹³ g
        - N_samples = 2500
        - Time ≈ 42 minutes
        """
        A = 1e-12
        SNR = 5
        
        # Calculate values
        sigma_req = self.analyzer.required_noise_level(A, SNR)
        n_samples = self.analyzer.required_samples(A, SNR)
        time_info = self.analyzer.observation_time_formatted(A, SNR)
        
        # Verify exact matches from problem statement
        self.assertAlmostEqual(sigma_req, 2e-13, places=20)
        self.assertEqual(n_samples, 2500)
        self.assertAlmostEqual(time_info['seconds'], 2500, places=5)
        self.assertAlmostEqual(time_info['minutes'], 41.67, places=1)
        
        # Verify feasibility
        self.assertTrue(self.analyzer.is_feasible(A, SNR))
        
        print(f"\n✓ Case 1 verified: A = 10⁻¹² g")
        print(f"  N_samples = {n_samples}")
        print(f"  Time = {time_info['minutes']:.0f} minutes")
    
    def test_case2_amplitude_1e13(self):
        """
        Verify Case 2: A = 10⁻¹³ g, SNR = 5
        
        Expected from problem statement:
        - N_samples = 2.5×10⁵
        - Time ≈ 3 days
        """
        A = 1e-13
        SNR = 5
        
        # Calculate values
        n_samples = self.analyzer.required_samples(A, SNR)
        time_info = self.analyzer.observation_time_formatted(A, SNR)
        
        # Verify exact matches from problem statement
        self.assertEqual(n_samples, 250000)
        self.assertAlmostEqual(time_info['seconds'], 2.5e5, places=5)
        self.assertAlmostEqual(time_info['days'], 2.89, places=1)
        
        # Verify feasibility
        self.assertTrue(self.analyzer.is_feasible(A, SNR))
        
        print(f"\n✓ Case 2 verified: A = 10⁻¹³ g")
        print(f"  N_samples = {n_samples:,}")
        print(f"  Time = {time_info['days']:.1f} days")
    
    def test_both_feasible_with_igets(self):
        """
        Verify that both cases are feasible with IGETS.
        
        Both should be feasible within reasonable timeframes.
        """
        # Case 1: A = 10⁻¹² g
        feasible_1 = self.analyzer.is_feasible(1e-12, 5.0, max_observation_days=30)
        
        # Case 2: A = 10⁻¹³ g
        feasible_2 = self.analyzer.is_feasible(1e-13, 5.0, max_observation_days=30)
        
        self.assertTrue(feasible_1, "A = 10⁻¹² g should be feasible")
        self.assertTrue(feasible_2, "A = 10⁻¹³ g should be feasible")
        
        print(f"\n✓ Both amplitudes feasible with IGETS")


def run_tests():
    """Run all tests and print summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSGSpecifications))
    suite.addTests(loader.loadTestsFromTestCase(TestSGSensitivityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestProblemStatementCompliance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
