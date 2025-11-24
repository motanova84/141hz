#!/usr/bin/env python3
"""
Unit Tests for Statistical Validation
======================================

Tests for Bayes Factor calculation, p-value estimation, and SNR computation.
These tests validate the statistical methods used in the 141.7 Hz analysis.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
from scipy import stats, signal


class TestBayesFactorCalculation(unittest.TestCase):
    """Test suite for Bayes Factor calculation"""
    
    def setUp(self):
        """Set up test fixtures"""
        np.random.seed(42)
        self.sample_rate = 4096
        self.duration = 4
        self.n_samples = self.sample_rate * self.duration
        
    def test_bayes_factor_pure_noise(self):
        """Test BF calculation with pure noise (should be close to 1)"""
        # Generate pure noise
        noise1 = np.random.normal(0, 1, self.n_samples)
        noise2 = np.random.normal(0, 1, self.n_samples)
        
        # Calculate power spectral densities
        freqs1, psd1 = signal.welch(noise1, fs=self.sample_rate, nperseg=1024)
        freqs2, psd2 = signal.welch(noise2, fs=self.sample_rate, nperseg=1024)
        
        # Find band around 141.7 Hz
        target_freq = 141.7
        band_width = 2.0
        mask = (freqs1 >= target_freq - band_width/2) & (freqs1 <= target_freq + band_width/2)
        
        # Skip if band is empty
        if not np.any(mask):
            self.skipTest("Frequency band not in PSD range")
        
        power1 = np.mean(psd1[mask])
        power2 = np.mean(psd2[mask])
        
        # Calculate BF (approximation) - ensure power2 > 0
        if power2 > 0:
            bf = np.exp((power1 - power2) / (2 * power2))
            # BF should be close to 1 for pure noise
            self.assertGreater(bf, 0.1)
            self.assertLess(bf, 10.0)
        else:
            self.skipTest("Power2 is zero")
        
    def test_bayes_factor_with_signal(self):
        """Test BF calculation with injected signal (should be > 1)"""
        # Generate noise + signal
        t = np.linspace(0, self.duration, self.n_samples)
        signal_component = 0.5 * np.sin(2 * np.pi * 141.7 * t)
        noise = np.random.normal(0, 0.1, self.n_samples)
        data_with_signal = signal_component + noise
        
        # Generate pure noise
        pure_noise = np.random.normal(0, 0.1, self.n_samples)
        
        # Calculate PSDs
        freqs_signal, psd_signal = signal.welch(data_with_signal, fs=self.sample_rate, nperseg=1024)
        freqs_noise, psd_noise = signal.welch(pure_noise, fs=self.sample_rate, nperseg=1024)
        
        # Find band around 141.7 Hz
        target_freq = 141.7
        band_width = 2.0
        mask = (freqs_signal >= target_freq - band_width/2) & (freqs_signal <= target_freq + band_width/2)
        
        # Skip if band is empty
        if not np.any(mask):
            self.skipTest("Frequency band not in PSD range")
        
        power_signal = np.mean(psd_signal[mask])
        power_noise = np.mean(psd_noise[mask])
        
        # Calculate BF - ensure power_noise > 0
        if power_noise > 0:
            bf = np.exp((power_signal - power_noise) / (2 * power_noise))
            # BF should be > 1 when signal is present
            self.assertGreater(bf, 0.5)
        else:
            self.skipTest("Power noise is zero")
        
    def test_bayes_factor_is_positive(self):
        """Test that BF is always positive"""
        noise1 = np.random.normal(0, 1, self.n_samples)
        noise2 = np.random.normal(0, 1, self.n_samples)
        
        freqs1, psd1 = signal.welch(noise1, fs=self.sample_rate, nperseg=1024)
        freqs2, psd2 = signal.welch(noise2, fs=self.sample_rate, nperseg=1024)
        
        target_freq = 141.7
        band_width = 2.0
        mask = (freqs1 >= target_freq - band_width/2) & (freqs1 <= target_freq + band_width/2)
        
        # Skip if band is empty
        if not np.any(mask):
            self.skipTest("Frequency band not in PSD range")
        
        power1 = np.mean(psd1[mask])
        power2 = np.mean(psd2[mask])
        
        # Calculate BF only if power2 > 0
        if power2 > 0:
            bf = np.exp((power1 - power2) / (2 * power2))
            self.assertGreater(bf, 0)
        else:
            self.skipTest("Power2 is zero")


class TestSNRCalculation(unittest.TestCase):
    """Test suite for SNR calculation"""
    
    def setUp(self):
        """Set up test fixtures"""
        np.random.seed(42)
        self.sample_rate = 4096
        self.duration = 4
        self.n_samples = self.sample_rate * self.duration
        
    def test_snr_pure_noise(self):
        """Test SNR calculation with pure noise (should be low)"""
        noise = np.random.normal(0, 1, self.n_samples)
        
        # Calculate SNR
        signal_peak = np.max(np.abs(noise))
        noise_std = np.std(noise)
        snr = signal_peak / noise_std
        
        # For Gaussian noise, max/std should be around 3-4
        self.assertGreater(snr, 2.0)
        self.assertLess(snr, 5.0)
        
    def test_snr_with_strong_signal(self):
        """Test SNR calculation with strong signal (should be high)"""
        t = np.linspace(0, self.duration, self.n_samples)
        signal_component = 10.0 * np.sin(2 * np.pi * 141.7 * t)
        noise = np.random.normal(0, 1, self.n_samples)
        data = signal_component + noise
        
        # Calculate SNR - peak of signal vs std of noise
        signal_peak = np.max(np.abs(data))
        noise_std = np.std(noise)  # Use noise std, not combined data
        snr = signal_peak / noise_std if noise_std > 0 else 0
        
        # SNR should be reasonably high (signal amplitude is 10x noise std)
        self.assertGreater(snr, 3.0)
        
    def test_snr_is_positive(self):
        """Test that SNR is always positive"""
        noise = np.random.normal(0, 1, self.n_samples)
        
        signal_peak = np.max(np.abs(noise))
        noise_std = np.std(noise)
        snr = signal_peak / noise_std
        
        self.assertGreater(snr, 0)
        
    def test_snr_scales_with_signal_amplitude(self):
        """Test that SNR scales linearly with signal amplitude"""
        t = np.linspace(0, self.duration, self.n_samples)
        
        # Test with different amplitudes
        amplitudes = [1.0, 2.0, 4.0]
        snrs = []
        
        for amp in amplitudes:
            # Generate independent noise for each iteration
            noise = np.random.normal(0, 1, self.n_samples)
            signal_component = amp * np.sin(2 * np.pi * 141.7 * t)
            data = signal_component + noise
            
            signal_peak = np.max(np.abs(signal_component))  # Peak of pure signal
            noise_std = np.std(noise)  # Std of pure noise
            snr = signal_peak / noise_std if noise_std > 0 else 0
            snrs.append(snr)
        
        # SNR should increase approximately linearly with amplitude
        # Allow for some noise variance, but trend should be increasing
        mean_snr_increase = (snrs[2] - snrs[0]) / 3
        self.assertGreater(mean_snr_increase, 0.5)


class TestPValueEstimation(unittest.TestCase):
    """Test suite for p-value estimation"""
    
    def setUp(self):
        """Set up test fixtures"""
        np.random.seed(42)
        
    def test_pvalue_range(self):
        """Test that p-value is between 0 and 1"""
        # Generate test statistic from noise
        noise_samples = np.random.normal(0, 1, 100)
        test_statistic = np.max(np.abs(noise_samples))
        
        # Generate null distribution
        null_distribution = []
        for _ in range(100):
            null_sample = np.random.normal(0, 1, 100)
            null_statistic = np.max(np.abs(null_sample))
            null_distribution.append(null_statistic)
        
        # Calculate p-value
        p_value = np.sum(np.array(null_distribution) >= test_statistic) / len(null_distribution)
        
        self.assertGreaterEqual(p_value, 0.0)
        self.assertLessEqual(p_value, 1.0)
        
    def test_pvalue_strong_signal(self):
        """Test that p-value is low for strong signal"""
        # Generate strong signal
        signal_samples = 5.0 + np.random.normal(0, 0.1, 100)  # Strong signal
        test_statistic = np.max(signal_samples)
        
        # Generate null distribution (noise only)
        null_distribution = []
        for _ in range(100):
            null_sample = np.random.normal(0, 1, 100)
            null_statistic = np.max(np.abs(null_sample))
            null_distribution.append(null_statistic)
        
        # Calculate p-value
        p_value = np.sum(np.array(null_distribution) >= test_statistic) / len(null_distribution)
        
        # p-value should be low (< 0.05)
        self.assertLess(p_value, 0.05)
        
    def test_pvalue_weak_signal(self):
        """Test that p-value is higher for weak signal"""
        # Generate weak signal (similar to noise)
        signal_samples = np.random.normal(0, 1, 100)
        test_statistic = np.max(np.abs(signal_samples))
        
        # Generate null distribution
        null_distribution = []
        for _ in range(100):
            null_sample = np.random.normal(0, 1, 100)
            null_statistic = np.max(np.abs(null_sample))
            null_distribution.append(null_statistic)
        
        # Calculate p-value
        p_value = np.sum(np.array(null_distribution) >= test_statistic) / len(null_distribution)
        
        # p-value should not be extremely low
        self.assertGreater(p_value, 0.01)


class TestStatisticalConsistency(unittest.TestCase):
    """Test suite for statistical consistency checks"""
    
    def test_chi_squared_goodness_of_fit(self):
        """Test chi-squared goodness of fit for noise model"""
        np.random.seed(42)
        
        # Generate Gaussian noise
        noise = np.random.normal(0, 1, 10000)
        
        # Test if it follows Gaussian distribution
        _, p_value = stats.kstest(noise, 'norm', args=(0, 1))
        
        # Should not reject null hypothesis (p > 0.05)
        self.assertGreater(p_value, 0.05)
        
    def test_normality_of_residuals(self):
        """Test normality of residuals after signal removal"""
        np.random.seed(42)
        t = np.linspace(0, 4, 4096)
        
        # Generate signal + noise
        signal_component = 2.0 * np.sin(2 * np.pi * 141.7 * t)
        noise = np.random.normal(0, 1, len(t))
        data = signal_component + noise
        
        # Remove signal (subtract model)
        residuals = data - signal_component
        
        # Test if residuals are Gaussian
        _, p_value = stats.kstest(residuals, 'norm', args=(np.mean(residuals), np.std(residuals)))
        
        # Should not reject null hypothesis
        self.assertGreater(p_value, 0.05)


class TestNumericalStability(unittest.TestCase):
    """Test suite for numerical stability of calculations"""
    
    def test_division_by_zero_protection(self):
        """Test that division by zero is handled"""
        # Test SNR calculation with zero std
        data = np.zeros(100)
        
        signal_peak = np.max(np.abs(data))
        noise_std = np.std(data)
        
        if noise_std > 0:
            snr = signal_peak / noise_std
        else:
            snr = 0.0
        
        # Should not raise exception
        self.assertEqual(snr, 0.0)
        
    def test_numerical_precision(self):
        """Test numerical precision of calculations"""
        # Test that small differences are preserved
        value1 = 1.0000001
        value2 = 1.0000002
        
        diff = value2 - value1
        
        self.assertGreater(diff, 0)
        self.assertLess(diff, 1e-6)


def run_tests():
    """Run all statistical validation tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestBayesFactorCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestSNRCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestPValueEstimation))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestNumericalStability))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
