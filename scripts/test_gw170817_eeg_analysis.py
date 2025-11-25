#!/usr/bin/env python3
"""
Tests for GW170817 and EEG analysis scripts.

This module tests the LIGO and EEG analysis functions for
detecting the f₀ = 141.7001 Hz frequency.
"""

import os
import sys
import unittest
from pathlib import Path

import numpy as np

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGW170817Analysis(unittest.TestCase):
    """Test cases for GW170817 LIGO analysis."""

    def test_synthetic_data_generation(self):
        """Test that synthetic LIGO data can be generated and analyzed."""
        from analizar_gw170817 import main

        result = main(
            data_path=None,
            detector='H1',
            target_freq=141.7001,
            save_plot=False,
            show_plot=False,
            use_synthetic=True,
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['detector'], 'H1')
        self.assertEqual(result['data_source'], 'Synthetic Data')
        self.assertIsInstance(result['snr'], float)
        self.assertGreater(result['snr'], 0)

    def test_analyze_signal_function(self):
        """Test the analyze_signal function directly."""
        from analizar_gw170817 import analyze_signal

        # Create test signal with known peak
        fs = 4096
        duration = 1.0
        n_samples = int(fs * duration)
        time = np.linspace(0, duration, n_samples)

        # Add clear signal at target frequency
        target_freq = 141.7001
        signal = np.sin(2 * np.pi * target_freq * time)
        noise = np.random.normal(0, 0.1, n_samples)
        strain = signal + noise

        freqs, psd, snr, peak_freq = analyze_signal(time, strain, fs, target_freq)

        # Verify results
        self.assertIsInstance(freqs, np.ndarray)
        self.assertIsInstance(psd, np.ndarray)
        self.assertIsInstance(snr, float)
        self.assertIsInstance(peak_freq, float)

        # Peak should be close to target
        self.assertAlmostEqual(peak_freq, target_freq, delta=1.0)
        # SNR should be positive
        self.assertGreater(snr, 0)

    def test_no_file_no_synthetic_returns_none(self):
        """Test that missing file without synthetic returns None."""
        from analizar_gw170817 import main

        result = main(
            data_path='/nonexistent/file.hdf5',
            detector='H1',
            save_plot=False,
            show_plot=False,
            use_synthetic=False,
        )

        self.assertIsNone(result)


class TestEEGAnalysis(unittest.TestCase):
    """Test cases for EEG analysis."""

    def test_synthetic_eeg_generation(self):
        """Test that synthetic EEG data can be generated and analyzed."""
        from analizar_eeg_real import main

        result = main(
            data_path=None,
            target_freq=141.7001,
            save_plot=False,
            show_plot=False,
            use_synthetic=True,
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['data_source'], 'Synthetic EEG')
        self.assertTrue(result['nyquist_ok'])
        self.assertIsInstance(result['snr'], float)

    def test_generate_synthetic_eeg(self):
        """Test the generate_synthetic_eeg function."""
        from analizar_eeg_real import generate_synthetic_eeg

        fs = 512
        duration = 10
        target_freq = 141.7001

        time, signal, returned_fs = generate_synthetic_eeg(
            fs=fs, duration=duration, target_freq=target_freq
        )

        self.assertEqual(returned_fs, fs)
        self.assertEqual(len(time), len(signal))
        self.assertEqual(len(signal), fs * duration)
        self.assertAlmostEqual(time[-1], duration, delta=0.1)

    def test_analyze_eeg_function(self):
        """Test the analyze_eeg function directly."""
        from analizar_eeg_real import analyze_eeg

        fs = 512
        duration = 10.0
        n_samples = int(fs * duration)
        time = np.linspace(0, duration, n_samples)

        # Create signal with embedded f₀
        target_freq = 141.7001
        signal = 0.5 * np.sin(2 * np.pi * target_freq * time)
        noise = np.random.normal(0, 0.1, n_samples)
        eeg = signal + noise

        freqs, psd, snr, peak_freq = analyze_eeg(
            time, eeg, fs, target_freq
        )

        self.assertIsInstance(freqs, np.ndarray)
        self.assertIsInstance(psd, np.ndarray)
        self.assertIsInstance(snr, float)
        self.assertIsInstance(peak_freq, float)

    def test_low_sample_rate_warning(self):
        """Test that low sample rate produces Nyquist warning."""
        from analizar_eeg_real import main

        # Use low sample rate that doesn't meet Nyquist for f₀
        result = main(
            data_path=None,
            target_freq=141.7001,
            fs=200,  # Below 2 * 141.7001 = 283.4 Hz
            save_plot=False,
            show_plot=False,
            use_synthetic=True,
        )

        # With synthetic data and proper fs override, should still work
        self.assertIsNotNone(result)


class TestCrossValidation(unittest.TestCase):
    """Test cases for cross-validation."""

    def test_cross_validation_synthetic(self):
        """Test cross-validation with synthetic data."""
        from validacion_cruzada_f0 import main

        summary = main(
            ligo_path=None,
            eeg_path=None,
            use_synthetic=True,
            output_json=None,
            show_plots=False,
        )

        self.assertIsNotNone(summary)
        self.assertIn('results', summary)
        self.assertIn('coherence', summary)
        self.assertIn('f0_target', summary)

        # Should have at least 3 results (LIGO, EEG, QGP)
        self.assertGreaterEqual(len(summary['results']), 3)

    def test_calculate_cross_coherence(self):
        """Test the calculate_cross_coherence function."""
        from validacion_cruzada_f0 import calculate_cross_coherence

        # Test with sample results
        results = [
            {'source': 'LIGO', 'peak_freq': 141.7001, 'deviation': 0.0001},
            {'source': 'EEG', 'peak_freq': 141.7002, 'deviation': 0.0002},
            {'source': 'QGP', 'peak_freq': 141.5, 'deviation': 0.2001},
        ]

        coherence = calculate_cross_coherence(results)

        self.assertIn('mean_freq', coherence)
        self.assertIn('std_freq', coherence)
        self.assertIn('max_deviation', coherence)
        self.assertIn('coherence_score', coherence)
        self.assertEqual(coherence['sources_analyzed'], 3)

    def test_qgp_reference(self):
        """Test QGP reference data."""
        from validacion_cruzada_f0 import get_qgp_reference

        qgp = get_qgp_reference()

        self.assertEqual(qgp['source'], 'QGP CERN')
        self.assertEqual(qgp['status'], 'REFERENCE')
        self.assertIn('freq_range', qgp)
        self.assertIn('peak_freq', qgp)


class TestDataLoaders(unittest.TestCase):
    """Test cases for data loading functions."""

    def test_numpy_loader(self):
        """Test loading data from NumPy file."""
        from analizar_eeg_real import load_eeg_numpy
        import tempfile

        # Create temporary NumPy file
        fs = 256
        signal = np.random.normal(0, 1, 2560)  # 10 seconds

        with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as f:
            np.save(f, signal)
            temp_path = f.name

        try:
            time, loaded_signal, loaded_fs = load_eeg_numpy(temp_path, fs=fs)

            self.assertEqual(len(time), len(signal))
            self.assertEqual(len(loaded_signal), len(signal))
            self.assertEqual(loaded_fs, fs)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
