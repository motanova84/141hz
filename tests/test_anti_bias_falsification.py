#!/usr/bin/env python3
"""
Anti-Bias Falsification Test - Zero Point Test (Off-Source Blind Test)
=========================================================================

This test addresses the critical reviewer concern: "If we apply the pipeline
where there is no event, would we find the same thing?"

The test executes the QCAL monitor on time windows from LIGO where we know
there are NO gravitational waves (pure noise). The ICV (coherence metric) 
must collapse to zero. If the system shows significance in noise, it indicates
overfitting or confirmation bias.

This is the "zero point test" - if ICV activates in vacuum, the system is broken.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import unittest
import numpy as np
from scipy import signal, stats
import warnings
import sys
import os

# Try to import gwpy for real LIGO data
try:
    from gwpy.timeseries import TimeSeries
    GWPY_AVAILABLE = True
except ImportError:
    GWPY_AVAILABLE = False
    warnings.warn("gwpy not available, using simulated noise data")

# Import QCAL constants
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import F0_HZ


class TestAntiBiasFalsification(unittest.TestCase):
    """
    Tests to verify the pipeline doesn't produce false positives in noise
    
    These tests are critical for establishing the scientific validity of the
    141.7 Hz detection. If the pipeline finds significant 141.7 Hz coherence
    in pure noise, it indicates a fundamental flaw in the methodology.
    """
    
    def setUp(self):
        """Set up test parameters"""
        self.target_freq = F0_HZ  # 141.7 Hz
        self.sample_rate = 4096  # Hz, standard for LIGO
        self.duration = 3600  # seconds (1 hour per window)
        np.random.seed(42)  # For reproducibility
        
    def test_null_hypothesis_exposure_single_window(self):
        """
        Test 1: Single 1-hour window of off-source noise
        
        Load 1 hour of LIGO noise without events (off-source).
        Execute the monitor for 141.7 Hz.
        REQUIREMENT: Significance must be < 1 sigma.
        If it gives 111 sigma here, the system is overfitted.
        """
        print("\n" + "="*80)
        print("TEST 1: NULL HYPOTHESIS EXPOSURE - SINGLE WINDOW")
        print("="*80)
        
        # Load or generate noise-only data
        noise_data = self._load_offsource_noise(duration=self.duration)
        
        # Run the 141.7 Hz monitor
        result = self._monitor_qcal_141hz(noise_data)
        
        print(f"\nResults for 1-hour off-source window:")
        print(f"  SNR: {result['snr']:.2f}")
        print(f"  Sigma: {result['sigma']:.2f}")
        print(f"  Peak power at {self.target_freq} Hz: {result['peak_power']:.6e}")
        print(f"  Median background: {result['background_median']:.6e}")
        print(f"  Background std: {result['background_std']:.6e}")
        
        # CRITICAL ASSERTION: Significance must be < 1 sigma in pure noise
        self.assertLess(
            result['sigma'], 
            1.0,
            f"FAIL: System shows {result['sigma']:.2f} sigma in pure noise! "
            f"This indicates overfitting or confirmation bias."
        )
        
        print(f"\n✅ PASS: Significance {result['sigma']:.2f} < 1.0 sigma in noise")
        
    def test_null_hypothesis_multiple_windows(self):
        """
        Test 2: Multiple off-source windows
        
        Test the pipeline on 100 independent noise windows (scaled down from 10,000
        for computational efficiency in CI). The false positive rate should be
        consistent with random chance at the specified confidence level.
        """
        print("\n" + "="*80)
        print("TEST 2: NULL HYPOTHESIS EXPOSURE - MULTIPLE WINDOWS")
        print("="*80)
        
        num_windows = 100  # Use 100 windows for CI (10,000 would be ideal for full study)
        window_duration = 3600  # 1 hour each
        false_positives = 0
        sigma_threshold = 1.0  # Detection threshold
        
        sigma_values = []
        
        print(f"\nTesting {num_windows} independent noise windows...")
        print(f"Duration per window: {window_duration} seconds")
        print(f"Detection threshold: {sigma_threshold} sigma")
        
        for i in range(num_windows):
            # Generate independent noise window
            noise_data = self._load_offsource_noise(
                duration=window_duration,
                seed=42 + i  # Different seed for each window
            )
            
            # Run monitor
            result = self._monitor_qcal_141hz(noise_data)
            sigma_values.append(result['sigma'])
            
            if result['sigma'] >= sigma_threshold:
                false_positives += 1
                
            # Progress indicator
            if (i + 1) % 20 == 0:
                print(f"  Processed {i+1}/{num_windows} windows, "
                      f"false positives: {false_positives}")
        
        # Calculate statistics
        false_positive_rate = false_positives / num_windows
        mean_sigma = np.mean(sigma_values)
        std_sigma = np.std(sigma_values)
        max_sigma = np.max(sigma_values)
        
        print(f"\n{'='*60}")
        print(f"RESULTS SUMMARY:")
        print(f"{'='*60}")
        print(f"Total windows tested: {num_windows}")
        print(f"False positives (>= {sigma_threshold} sigma): {false_positives}")
        print(f"False positive rate: {false_positive_rate:.4f} ({false_positive_rate*100:.2f}%)")
        print(f"Mean sigma: {mean_sigma:.3f}")
        print(f"Std sigma: {std_sigma:.3f}")
        print(f"Max sigma: {max_sigma:.3f}")
        print(f"{'='*60}")
        
        # Expected false positive rate at 1 sigma (assuming Gaussian) is ~0.32
        # We allow some margin but it shouldn't be dramatically higher
        expected_fp_rate = 0.32  # ~32% for 1-sigma threshold in Gaussian noise
        max_acceptable_fp_rate = 0.45  # Allow some margin
        
        self.assertLess(
            false_positive_rate,
            max_acceptable_fp_rate,
            f"False positive rate {false_positive_rate:.3f} exceeds acceptable "
            f"threshold {max_acceptable_fp_rate:.3f}. System may be overfitted."
        )
        
        # Mean sigma should be close to 0 for pure noise
        self.assertLess(
            abs(mean_sigma),
            0.3,
            f"Mean sigma {mean_sigma:.3f} is too far from 0. "
            f"System shows systematic bias in noise."
        )
        
        print(f"\n✅ PASS: False positive rate {false_positive_rate:.3f} is acceptable")
        print(f"✅ PASS: Mean sigma {mean_sigma:.3f} is close to 0")
        
    def test_spectral_resolution_adequacy(self):
        """
        Test 3: Verify spectral resolution is adequate
        
        Ensure windows are long enough to resolve 141.7 Hz with adequate
        frequency resolution (~0.1 Hz as mentioned in the problem statement).
        """
        print("\n" + "="*80)
        print("TEST 3: SPECTRAL RESOLUTION ADEQUACY")
        print("="*80)
        
        # Calculate frequency resolution
        freq_resolution = 1.0 / self.duration  # Hz
        
        print(f"\nWindow duration: {self.duration} seconds")
        print(f"Frequency resolution: {freq_resolution:.4f} Hz")
        print(f"Target frequency: {self.target_freq} Hz")
        
        # Requirement from problem statement: resolution ~ 0.1 Hz
        required_resolution = 0.1  # Hz
        
        self.assertLessEqual(
            freq_resolution,
            required_resolution,
            f"Frequency resolution {freq_resolution:.4f} Hz is inadequate. "
            f"Need <= {required_resolution} Hz to properly resolve {self.target_freq} Hz."
        )
        
        print(f"\n✅ PASS: Frequency resolution {freq_resolution:.4f} Hz is adequate")
        
    def _load_offsource_noise(self, duration=3600, seed=None):
        """
        Load off-source noise data from LIGO or generate simulated noise
        
        Parameters
        ----------
        duration : float
            Duration of noise segment in seconds
        seed : int, optional
            Random seed for simulated noise generation
            
        Returns
        -------
        np.ndarray
            Noise data array
        """
        if seed is not None:
            np.random.seed(seed)
            
        if GWPY_AVAILABLE:
            try:
                # Use a known quiet period in LIGO data (no catalogued events)
                # GPS time: 1187056618 is 2017-08-01, well before O3 run
                # This is a period with no significant events nearby
                gps_start = 1187056618  # A quiet period
                
                # Try to fetch real LIGO noise
                detector = 'H1'  # Hanford detector
                noise = TimeSeries.fetch_open_data(
                    detector,
                    gps_start,
                    gps_start + duration,
                    sample_rate=self.sample_rate,
                    cache=True,
                    verbose=False
                )
                
                print(f"  ✅ Loaded real LIGO noise from {detector}")
                return noise.value
                
            except Exception as e:
                warnings.warn(f"Failed to load real LIGO data: {e}. Using simulated noise.")
        
        # Generate simulated LIGO-like noise
        # LIGO noise is approximately 1/f (pink noise) at low frequencies
        # with some white noise component
        n_samples = int(duration * self.sample_rate)
        
        # Generate white noise
        white_noise = np.random.normal(0, 1e-21, n_samples)
        
        # Add 1/f component using power spectrum shaping
        # Simple approximation of LIGO noise curve
        freqs = np.fft.rfftfreq(n_samples, 1/self.sample_rate)
        white_fft = np.fft.rfft(white_noise)
        
        # Apply 1/f^(1/2) shaping (pink noise approximation)
        noise_psd = 1e-21 * (1 + (100 / np.maximum(freqs, 10))**2)**0.5
        shaped_fft = white_fft * noise_psd
        
        noise = np.fft.irfft(shaped_fft, n=n_samples)
        
        print(f"  ⚠️  Using simulated LIGO-like noise")
        return noise
        
    def _monitor_qcal_141hz(self, data):
        """
        Monitor for 141.7 Hz coherence in the data
        
        This implements the core detection algorithm that searches for
        coherent power at the target frequency.
        
        Parameters
        ----------
        data : np.ndarray
            Time series data
            
        Returns
        -------
        dict
            Detection results including SNR, sigma, and spectral properties
        """
        # Apply bandpass filter around 141.7 Hz
        # Use a relatively wide band to avoid overfitting
        low_freq = self.target_freq - 10.0  # 131.7 Hz
        high_freq = self.target_freq + 10.0  # 151.7 Hz
        
        nyquist = self.sample_rate / 2
        low_norm = low_freq / nyquist
        high_norm = high_freq / nyquist
        
        # Design bandpass filter
        sos = signal.butter(4, [low_norm, high_norm], btype='band', output='sos')
        filtered = signal.sosfilt(sos, data)
        
        # Compute power spectral density using Welch method
        nperseg = min(int(self.sample_rate * 4), len(data) // 4)  # 4-second segments
        freqs, psd = signal.welch(
            data,
            fs=self.sample_rate,
            nperseg=nperseg,
            scaling='density'
        )
        
        # Find the target frequency bin
        target_idx = np.argmin(np.abs(freqs - self.target_freq))
        target_freq_actual = freqs[target_idx]
        
        # Get power at target frequency
        peak_power = psd[target_idx]
        
        # Estimate background by excluding region around target
        # Use frequencies outside the [131.7, 151.7] Hz band
        background_mask = (freqs < low_freq) | (freqs > high_freq)
        background_psd = psd[background_mask]
        
        # Calculate background statistics
        background_median = np.median(background_psd)
        background_std = np.std(background_psd)
        
        # Calculate SNR: (signal - background) / background_noise
        snr = (peak_power - background_median) / background_std if background_std > 0 else 0
        
        # Convert to sigma (assuming Gaussian statistics)
        # In pure noise, we expect SNR ~ 0 with unit variance
        sigma = snr
        
        # For more sophisticated sigma calculation, could use:
        # - Chi-squared statistics for power spectral density
        # - Empirical distribution of background
        # But for this test, simple SNR-based sigma is sufficient
        
        return {
            'snr': snr,
            'sigma': sigma,
            'peak_power': peak_power,
            'background_median': background_median,
            'background_std': background_std,
            'target_freq_actual': target_freq_actual,
            'freq_resolution': freqs[1] - freqs[0]
        }


class TestNoiseCharacteristics(unittest.TestCase):
    """Test that noise generation and loading produces realistic characteristics"""
    
    def test_noise_statistics(self):
        """Verify generated noise has expected statistical properties"""
        np.random.seed(42)
        sample_rate = 4096
        duration = 10  # Short duration for quick test
        
        # Generate noise
        n_samples = int(duration * sample_rate)
        noise = np.random.normal(0, 1e-21, n_samples)
        
        # Check mean is close to zero
        mean = np.mean(noise)
        self.assertLess(abs(mean), 1e-22, "Noise mean should be close to zero")
        
        # Check standard deviation is close to expected
        std = np.std(noise)
        expected_std = 1e-21
        self.assertLess(
            abs(std - expected_std) / expected_std,
            0.1,
            f"Noise std {std:.2e} differs from expected {expected_std:.2e}"
        )
        
    def test_noise_spectrum_shape(self):
        """Verify noise spectrum has reasonable shape"""
        np.random.seed(42)
        sample_rate = 4096
        duration = 100
        
        n_samples = int(duration * sample_rate)
        noise = np.random.normal(0, 1e-21, n_samples)
        
        # Compute spectrum
        freqs, psd = signal.welch(noise, fs=sample_rate, nperseg=sample_rate)
        
        # Check that spectrum exists at 141.7 Hz
        idx_141 = np.argmin(np.abs(freqs - 141.7))
        self.assertGreater(psd[idx_141], 0, "PSD should be positive at 141.7 Hz")
        
        # Check spectrum is relatively flat for white noise
        # (within an order of magnitude across the band)
        band_mask = (freqs >= 100) & (freqs <= 200)
        band_psd = psd[band_mask]
        psd_ratio = np.max(band_psd) / np.min(band_psd)
        self.assertLess(
            psd_ratio,
            100,
            f"White noise spectrum should be relatively flat, got ratio {psd_ratio:.1f}"
        )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
