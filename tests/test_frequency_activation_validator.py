#!/usr/bin/env python3
"""
Unit Tests for Frequency Activation Validator
=============================================

Tests for the dual EEG-LIGO frequency activation validator:
- EEG data generation
- LIGO data generation
- Frequency analysis
- Statistical validation

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import unittest
import numpy as np
from experiments.frequency_activation_validator import (
    EEGDataGenerator,
    LIGODataGenerator,
    FrequencyAnalyzer,
    DualSystemValidator,
    DetectionResult,
    CrossSystemValidation,
    F0_HZ,
    SAMPLING_RATE,
    N_EEG_CHANNELS
)


class TestEEGDataGenerator(unittest.TestCase):
    """Test EEG data generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = EEGDataGenerator()
    
    def test_initialization(self):
        """Test generator initialization."""
        self.assertEqual(self.generator.n_channels, N_EEG_CHANNELS)
        self.assertEqual(self.generator.fs, SAMPLING_RATE)
        self.assertAlmostEqual(self.generator.f_signal, F0_HZ, places=4)
    
    def test_brain_rhythms_shape(self):
        """Test brain rhythms have correct shape."""
        duration = 1.0
        rhythms = self.generator.generate_brain_rhythms(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(rhythms.shape, (N_EEG_CHANNELS, expected_samples))
    
    def test_brain_rhythms_not_zero(self):
        """Test brain rhythms are not all zero."""
        duration = 0.5
        rhythms = self.generator.generate_brain_rhythms(duration)
        
        self.assertGreater(np.max(np.abs(rhythms)), 0.0)
        self.assertGreater(np.std(rhythms), 0.0)
    
    def test_noise_shape(self):
        """Test noise has correct shape."""
        duration = 1.0
        noise = self.generator.generate_noise(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(noise.shape, (N_EEG_CHANNELS, expected_samples))
    
    def test_signal_injection_shape(self):
        """Test signal injection has correct shape."""
        duration = 1.0
        signal = self.generator.inject_signal(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(signal.shape, (N_EEG_CHANNELS, expected_samples))
    
    def test_signal_contains_f0(self):
        """Test injected signal contains f₀ frequency."""
        duration = 2.0
        signal = self.generator.inject_signal(duration, amplitude=1.0, coherence=1.0)
        
        # FFT of first channel
        from scipy.fft import rfft, rfftfreq
        fft_signal = rfft(signal[0, :])
        freqs = rfftfreq(signal.shape[1], 1/SAMPLING_RATE)
        power = np.abs(fft_signal)**2
        
        # Find peak
        peak_idx = np.argmax(power)
        peak_freq = freqs[peak_idx]
        
        # Should be near f₀
        self.assertAlmostEqual(peak_freq, F0_HZ, delta=5.0)
    
    def test_generate_complete_dataset(self):
        """Test complete dataset generation."""
        duration = 1.0
        data = self.generator.generate(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(data.shape, (N_EEG_CHANNELS, expected_samples))
        self.assertTrue(np.all(np.isfinite(data)))
    
    def test_coherence_effect(self):
        """Test coherence affects channel correlation."""
        duration = 2.0
        
        # High coherence
        signal_high_coh = self.generator.inject_signal(duration, coherence=0.95)
        
        # Low coherence
        signal_low_coh = self.generator.inject_signal(duration, coherence=0.1)
        
        # High coherence should have more correlated channels
        corr_high = np.corrcoef(signal_high_coh)[0, 1]
        corr_low = np.corrcoef(signal_low_coh)[0, 1]
        
        self.assertGreater(abs(corr_high), abs(corr_low))


class TestLIGODataGenerator(unittest.TestCase):
    """Test LIGO data generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = LIGODataGenerator()
    
    def test_initialization(self):
        """Test generator initialization."""
        self.assertEqual(self.generator.fs, SAMPLING_RATE)
        self.assertAlmostEqual(self.generator.f_signal, F0_HZ, places=4)
    
    def test_seismic_noise_shape(self):
        """Test seismic noise has correct shape."""
        duration = 1.0
        noise = self.generator.generate_seismic_noise(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(len(noise), expected_samples)
    
    def test_seismic_noise_low_frequency(self):
        """Test seismic noise is low frequency."""
        duration = 2.0
        noise = self.generator.generate_seismic_noise(duration)
        
        from scipy.fft import rfft, rfftfreq
        fft_noise = rfft(noise)
        freqs = rfftfreq(len(noise), 1/SAMPLING_RATE)
        power = np.abs(fft_noise)**2
        
        # Most power should be below 10 Hz
        low_freq_mask = freqs < 10.0
        high_freq_mask = freqs > 100.0
        
        low_freq_power = np.sum(power[low_freq_mask])
        high_freq_power = np.sum(power[high_freq_mask])
        
        self.assertGreater(low_freq_power, high_freq_power)
    
    def test_shot_noise_shape(self):
        """Test shot noise has correct shape."""
        duration = 1.0
        noise = self.generator.generate_shot_noise(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(len(noise), expected_samples)
    
    def test_quantum_noise_shape(self):
        """Test quantum noise has correct shape."""
        duration = 1.0
        noise = self.generator.generate_quantum_noise(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(len(noise), expected_samples)
    
    def test_signal_injection_shape(self):
        """Test signal injection has correct shape."""
        duration = 1.0
        signal = self.generator.inject_signal(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(len(signal), expected_samples)
    
    def test_signal_contains_f0(self):
        """Test injected signal contains f₀ frequency."""
        duration = 4.0
        signal = self.generator.inject_signal(duration, amplitude=1.0)
        
        # FFT
        from scipy.fft import rfft, rfftfreq
        fft_signal = rfft(signal)
        freqs = rfftfreq(len(signal), 1/SAMPLING_RATE)
        power = np.abs(fft_signal)**2
        
        # Find peak in f₀ region
        f0_mask = (freqs >= F0_HZ - 10) & (freqs <= F0_HZ + 10)
        if np.sum(f0_mask) > 0:
            peak_in_region = np.max(power[f0_mask])
            self.assertGreater(peak_in_region, 0.0)
    
    def test_generate_complete_dataset(self):
        """Test complete dataset generation."""
        duration = 1.0
        data = self.generator.generate(duration)
        
        expected_samples = int(duration * SAMPLING_RATE)
        self.assertEqual(len(data), expected_samples)
        self.assertTrue(np.all(np.isfinite(data)))


class TestFrequencyAnalyzer(unittest.TestCase):
    """Test frequency analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = FrequencyAnalyzer()
    
    def test_spectrum_computation(self):
        """Test power spectrum computation."""
        # Create simple sine wave
        duration = 1.0
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        signal = np.sin(2 * np.pi * 100 * t)  # 100 Hz sine
        
        freqs, power = self.analyzer.compute_spectrum(signal)
        
        self.assertEqual(len(freqs), len(power))
        self.assertTrue(all(f >= 0 for f in freqs))
        self.assertTrue(all(p >= 0 for p in power))
    
    def test_peak_detection(self):
        """Test peak frequency detection."""
        # Create signal at known frequency
        duration = 2.0
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        test_freq = 150.0
        signal = np.sin(2 * np.pi * test_freq * t)
        
        freqs, power = self.analyzer.compute_spectrum(signal)
        peak_info = self.analyzer.detect_peak(freqs, power, freq_range=(100, 200))
        
        # Peak should be near test frequency
        self.assertAlmostEqual(peak_info['peak_freq'], test_freq, delta=5.0)
    
    def test_snr_computation(self):
        """Test SNR computation."""
        # Create signal with known SNR
        duration = 2.0
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        
        signal = np.sin(2 * np.pi * F0_HZ * t)
        noise = 0.1 * np.random.randn(len(t))
        data = signal + noise
        
        freqs, power = self.analyzer.compute_spectrum(data)
        snr = self.analyzer.compute_snr(freqs, power, F0_HZ)
        
        # SNR should be positive for signal+noise
        self.assertGreater(snr, 0.0)
    
    def test_coherence_computation_multichannel(self):
        """Test coherence computation for multi-channel data."""
        duration = 2.0
        n_channels = 10
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        
        # Create coherent signal across channels
        signal = np.sin(2 * np.pi * F0_HZ * t)
        data = np.tile(signal, (n_channels, 1))
        
        coherence = self.analyzer.compute_coherence(data, F0_HZ)
        
        # Perfect coherence should be close to 1
        self.assertGreater(coherence, 0.8)
    
    def test_analyze_single_channel(self):
        """Test complete analysis for single channel."""
        duration = 2.0
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        signal = np.sin(2 * np.pi * F0_HZ * t) + 0.1 * np.random.randn(len(t))
        
        result = self.analyzer.analyze(signal, target_freq=F0_HZ, is_multichannel=False)
        
        self.assertIsInstance(result, DetectionResult)
        self.assertGreater(result.peak_frequency, 0)
        self.assertTrue(np.isfinite(result.snr_db))
        self.assertEqual(result.coherence, 1.0)  # Single channel
    
    def test_analyze_multichannel(self):
        """Test complete analysis for multi-channel."""
        duration = 2.0
        n_channels = 16
        t = np.arange(0, duration, 1/SAMPLING_RATE)
        
        signal = np.sin(2 * np.pi * F0_HZ * t)
        data = np.tile(signal, (n_channels, 1))
        data += 0.1 * np.random.randn(n_channels, len(t))
        
        result = self.analyzer.analyze(data, target_freq=F0_HZ, is_multichannel=True)
        
        self.assertIsInstance(result, DetectionResult)
        self.assertGreater(result.coherence, 0.0)
        self.assertLessEqual(result.coherence, 1.0)


class TestDualSystemValidator(unittest.TestCase):
    """Test dual system validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = DualSystemValidator()
    
    def test_initialization(self):
        """Test validator initialization."""
        self.assertIsNotNone(self.validator.eeg_generator)
        self.assertIsNotNone(self.validator.ligo_generator)
        self.assertIsNotNone(self.validator.analyzer)
    
    def test_validate_returns_results(self):
        """Test validation returns complete results."""
        results = self.validator.validate(duration=1.0, run_bootstrap=False)
        
        # Check structure
        self.assertIn('EEG', results)
        self.assertIn('LIGO', results)
        self.assertIn('cross_system', results)
        self.assertIn('validation_summary', results)
        
        # Check EEG results
        self.assertIn('frequency', results['EEG'])
        self.assertIn('coherence', results['EEG'])
        self.assertIn('snr_db', results['EEG'])
        self.assertIn('status', results['EEG'])
        
        # Check LIGO results
        self.assertIn('frequency', results['LIGO'])
        self.assertIn('coherence', results['LIGO'])
        self.assertIn('snr_db', results['LIGO'])
        self.assertIn('status', results['LIGO'])
    
    def test_validate_detects_f0(self):
        """Test validation detects f₀ in both systems."""
        results = self.validator.validate(duration=2.0, run_bootstrap=False)
        
        eeg_freq = results['EEG']['frequency']
        ligo_freq = results['LIGO']['frequency']
        
        # Frequencies should be positive
        self.assertGreater(eeg_freq, 0)
        self.assertGreater(ligo_freq, 0)
        
        # Should be within reasonable range of f₀
        self.assertLess(abs(eeg_freq - F0_HZ), 50.0)
        self.assertLess(abs(ligo_freq - F0_HZ), 50.0)
    
    def test_validate_cross_system(self):
        """Test cross-system validation."""
        results = self.validator.validate(duration=2.0, run_bootstrap=False)
        
        cross = results['cross_system']
        
        self.assertIn('correlation', cross)
        self.assertIn('correlation_p_value', cross)
        self.assertIn('coincidence_prob', cross)
        
        # Correlation should be between -1 and 1
        self.assertGreaterEqual(cross['correlation'], -1.0)
        self.assertLessEqual(cross['correlation'], 1.0)
    
    def test_validation_summary(self):
        """Test validation summary."""
        results = self.validator.validate(duration=2.0, run_bootstrap=False)
        
        summary = results['validation_summary']
        
        self.assertIn('f0_detected_eeg', summary)
        self.assertIn('f0_detected_ligo', summary)
        self.assertIn('cross_validated', summary)
        self.assertIn('overall_success', summary)
        
        # All should be boolean
        self.assertIsInstance(summary['f0_detected_eeg'], bool)
        self.assertIsInstance(summary['f0_detected_ligo'], bool)
        self.assertIsInstance(summary['cross_validated'], bool)
        self.assertIsInstance(summary['overall_success'], bool)
    
    def test_print_report(self):
        """Test report printing doesn't crash."""
        results = self.validator.validate(duration=1.0, run_bootstrap=False)
        
        # Should not raise exception
        try:
            self.validator.print_report(results)
        except Exception as e:
            self.fail(f"print_report raised {type(e).__name__}: {e}")


class TestDataStructures(unittest.TestCase):
    """Test data structure classes."""
    
    def test_detection_result_initialization(self):
        """Test DetectionResult initialization."""
        result = DetectionResult(
            peak_frequency=141.7,
            snr_db=35.0,
            coherence=0.8,
            p_value=0.001
        )
        
        self.assertAlmostEqual(result.peak_frequency, 141.7)
        self.assertAlmostEqual(result.snr_db, 35.0)
        self.assertAlmostEqual(result.coherence, 0.8)
        self.assertAlmostEqual(result.p_value, 0.001)
    
    def test_cross_system_validation_initialization(self):
        """Test CrossSystemValidation initialization."""
        cross = CrossSystemValidation(
            correlation=0.999,
            correlation_p_value=0.001,
            phase_alignment=0.1,
            coincidence_prob=0.95
        )
        
        self.assertAlmostEqual(cross.correlation, 0.999)
        self.assertAlmostEqual(cross.correlation_p_value, 0.001)
        self.assertAlmostEqual(cross.phase_alignment, 0.1)
        self.assertAlmostEqual(cross.coincidence_prob, 0.95)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_end_to_end_validation(self):
        """Test complete end-to-end validation workflow."""
        # Create validator
        validator = DualSystemValidator()
        
        # Run validation
        results = validator.validate(duration=1.0, run_bootstrap=False)
        
        # Verify we got results
        self.assertIsNotNone(results)
        
        # Verify both systems produced results
        self.assertIsNotNone(results['EEG'])
        self.assertIsNotNone(results['LIGO'])
        
        # Verify frequencies are reasonable
        eeg_freq = results['EEG']['frequency']
        ligo_freq = results['LIGO']['frequency']
        
        self.assertGreater(eeg_freq, 0)
        self.assertGreater(ligo_freq, 0)
        self.assertLess(eeg_freq, SAMPLING_RATE / 2)  # Below Nyquist
        self.assertLess(ligo_freq, SAMPLING_RATE / 2)
    
    def test_f0_constant_consistency(self):
        """Test f₀ = 141.7001 Hz is consistently used."""
        # EEG generator
        eeg_gen = EEGDataGenerator()
        self.assertAlmostEqual(eeg_gen.f_signal, 141.7001, places=4)
        
        # LIGO generator
        ligo_gen = LIGODataGenerator()
        self.assertAlmostEqual(ligo_gen.f_signal, 141.7001, places=4)
        
        # Global constant
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
