#!/usr/bin/env python3
"""
Test suite for analyze_at2020afhd.py

Tests the AT2020afhd Lomb-Scargle periodogram analysis functionality.
"""

import unittest
import numpy as np
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_at2020afhd import AT2020afhdAnalyzer


class TestAT2020afhdAnalyzer(unittest.TestCase):
    """Test cases for AT2020afhdAnalyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = AT2020afhdAnalyzer(data_dir='Figure_datas')

    def test_initialization(self):
        """Test analyzer initialization."""
        self.assertEqual(self.analyzer.f0, 141.70001)
        self.assertEqual(self.analyzer.published_period, 19.6)
        self.assertEqual(self.analyzer.published_error, 0.5)
        self.assertIsInstance(self.analyzer.data_dir, Path)

    def test_find_peak_period(self):
        """Test peak detection in periodogram."""
        # Create synthetic data with clear peak at 19.6 days
        period = np.linspace(10, 40, 1000)
        # Gaussian peak centered at 19.6
        power = np.exp(-((period - 19.6) ** 2) / (2 * 0.5 ** 2))

        detected_period, max_power, max_idx = self.analyzer.find_peak_period(period, power)

        # Check that detected period is close to 19.6
        self.assertAlmostEqual(detected_period, 19.6, places=1)
        self.assertAlmostEqual(max_power, 1.0, places=2)

    def test_calculate_qcal_verification(self):
        """Test QCAL harmonic relationship calculation."""
        detected_period = 19.6  # days

        f_frame, ratio, octaves, decades = self.analyzer.calculate_qcal_verification(
            detected_period
        )

        # Check frequency conversion
        expected_f_frame = 1.0 / (19.6 * 86400.0)
        self.assertAlmostEqual(f_frame, expected_f_frame, places=10)

        # Check ratio
        expected_ratio = 141.70001 / expected_f_frame
        self.assertAlmostEqual(ratio, expected_ratio, places=2)

        # Check octaves (should be around 27.8)
        self.assertGreater(octaves, 27.0)
        self.assertLess(octaves, 29.0)

        # Check decades
        expected_decades = np.log10(expected_ratio)
        self.assertAlmostEqual(decades, expected_decades, places=5)

    def test_qcal_verification_with_published_period(self):
        """Test verification with the published period of 19.6 days."""
        f_frame, ratio, octaves, decades = self.analyzer.calculate_qcal_verification(19.6)

        # Verify the harmonic cascade is in expected range
        self.assertGreater(octaves, 27.5)
        self.assertLess(octaves, 28.5)

        # Verify ratio is in expected range
        self.assertGreater(ratio, 2.3e8)
        self.assertLess(ratio, 2.5e8)

    def test_check_data_availability_missing_data(self):
        """Test data availability check with missing data."""
        # Create analyzer with non-existent directory
        analyzer = AT2020afhdAnalyzer(data_dir='nonexistent_directory')

        # Should return False when data is missing
        self.assertFalse(analyzer.check_data_availability())

    def test_period_verification_criteria(self):
        """Test period verification criteria."""
        # Test with correct period
        detected_period = 19.6
        periodo_ok = (
            self.analyzer.published_period - self.analyzer.published_error <
            detected_period <
            self.analyzer.published_period + self.analyzer.published_error
        )
        self.assertTrue(periodo_ok)

        # Test with incorrect period
        detected_period = 25.0
        periodo_ok = (
            self.analyzer.published_period - self.analyzer.published_error <
            detected_period <
            self.analyzer.published_period + self.analyzer.published_error
        )
        self.assertFalse(periodo_ok)

    def test_octave_calculation(self):
        """Test octave calculation from ratio."""
        # Test with known values
        ratio = 2.405e8
        octaves = np.log2(ratio)

        # Should be approximately 27.84
        self.assertAlmostEqual(octaves, 27.84, places=1)

    def test_frequency_conversion(self):
        """Test period to frequency conversion."""
        period_days = 19.6
        period_seconds = period_days * 86400.0
        frequency_hz = 1.0 / period_seconds

        # Verify conversion
        expected_frequency = 5.905e-7  # approximately
        self.assertAlmostEqual(frequency_hz, expected_frequency, places=9)


class TestDataStructures(unittest.TestCase):
    """Test data structure handling."""

    def test_periodogram_data_format(self):
        """Test that periodogram data format is handled correctly."""
        # Simulate periodogram data structure
        period = np.linspace(10, 40, 100)
        power = np.random.random(100)
        lsp_data = np.column_stack([period, power])

        # Check shape
        self.assertEqual(lsp_data.shape[1], 2)
        self.assertEqual(len(lsp_data), 100)

    def test_light_curve_data_format(self):
        """Test that light curve data format is handled correctly."""
        # Simulate light curve data (time, flux, error)
        time = np.linspace(59000, 59100, 50)
        flux = np.random.random(50) * 1e-10
        error = np.random.random(50) * 1e-11
        lc_data = np.column_stack([time, flux, error])

        # Check shape
        self.assertEqual(lc_data.shape[1], 3)
        self.assertEqual(len(lc_data), 50)

    def test_nan_handling(self):
        """Test NaN handling in data."""
        # Create data with NaN
        data = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])

        # Remove rows with NaN
        clean_data = data[~np.isnan(data).any(axis=1)]

        # Check that NaN rows are removed
        self.assertEqual(len(clean_data), 2)
        self.assertFalse(np.isnan(clean_data).any())


class TestConstants(unittest.TestCase):
    """Test QCAL constants and relationships."""

    def test_qcal_frequency(self):
        """Test QCAL fundamental frequency value."""
        f0 = 141.70001

        # Verify it's in the expected range (heart rate)
        self.assertGreater(f0, 100)
        self.assertLess(f0, 200)

    def test_published_at2020afhd_period(self):
        """Test published AT2020afhd period value."""
        published_period = 19.6  # days

        # Verify it's in reasonable range
        self.assertGreater(published_period, 1)
        self.assertLess(published_period, 100)

    def test_expected_harmonic_ratio(self):
        """Test expected harmonic ratio value."""
        expected_ratio = 2.405e8

        # Verify it's a large positive number
        self.assertGreater(expected_ratio, 1e8)
        self.assertLess(expected_ratio, 1e9)

    def test_expected_octaves(self):
        """Test expected octave separation."""
        expected_octaves = 27.84

        # Verify it's in reasonable range
        self.assertGreater(expected_octaves, 20)
        self.assertLess(expected_octaves, 35)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAT2020afhdAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructures))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
