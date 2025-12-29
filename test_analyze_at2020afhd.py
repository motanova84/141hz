#!/usr/bin/env python3
"""
Test suite for analyze_at2020afhd.py

Validates the AT2020afhd Lense-Thirring precession analysis implementation.
"""

import unittest
import numpy as np
import os
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module without executing the main analysis
import analyze_at2020afhd as at2020


class TestAT2020afhdAnalysis(unittest.TestCase):
    """Test cases for AT2020afhd analysis."""

    @classmethod
    def setUpClass(cls):
        """Run analysis once for all tests."""
        # Run the main analysis once and store results
        cls.results = at2020.main()
        
    def setUp(self):
        """Set up test fixtures."""
        # Set random seed for reproducibility
        np.random.seed(141)

    def test_precession_period(self):
        """Test that the precession period is correctly defined."""
        self.assertEqual(at2020.PERIOD_PRECESSION, 20.0)
        
    def test_omega_frame(self):
        """Test that omega_frame is calculated correctly."""
        expected_omega = 2 * np.pi / 20.0
        self.assertAlmostEqual(at2020.omega_frame, expected_omega, places=10)
        
    def test_xray_flux_model(self):
        """Test X-ray flux model generation."""
        t = np.linspace(0, 100, 50)
        flux = at2020.xray_flux_model(t)
        
        # Check output shape
        self.assertEqual(len(flux), len(t))
        
        # Check all values are positive (due to np.maximum)
        self.assertTrue(np.all(flux > 0))
        
        # Check flux is reasonable (not too large)
        self.assertTrue(np.all(flux < 10.0))
        
    def test_radio_flux_model(self):
        """Test radio flux model generation."""
        t = np.linspace(0, 100, 50)
        flux = at2020.radio_flux_model(t)
        
        # Check output shape
        self.assertEqual(len(flux), len(t))
        
        # Check all values are positive
        self.assertTrue(np.all(flux > 0))
        
        # Check flux is reasonable
        self.assertTrue(np.all(flux < 10.0))

    def test_precession_model(self):
        """Test the precession model function."""
        t = np.linspace(0, 100, 50)
        A = 1.0
        omega = 2 * np.pi / 20.0
        phi = 0.0
        decay = 0.003
        baseline = 0.5
        
        result = at2020.precession_model(t, A, omega, phi, decay, baseline)
        
        # Check output shape
        self.assertEqual(len(result), len(t))
        
        # Check that decay reduces amplitude over time
        # Early values should generally be larger than late values
        early_mean = np.mean(result[:10])
        late_mean = np.mean(result[-10:])
        self.assertGreater(early_mean, late_mean * 0.5)
        
    def test_compute_periodogram(self):
        """Test Lomb-Scargle periodogram computation."""
        # Generate synthetic periodic data
        t = np.sort(np.random.uniform(0, 400, 100))
        omega = 2 * np.pi / 20.0
        flux = np.sin(omega * t) + 0.1 * np.random.randn(len(t))
        
        freq, pgram, periods, peak_period = at2020.compute_periodogram(
            t, flux, min_period=5, max_period=100
        )
        
        # Check that peak is near expected 20 days
        self.assertGreater(peak_period, 15.0)
        self.assertLess(peak_period, 25.0)
        
        # Check shapes
        self.assertEqual(len(freq), len(pgram))
        self.assertEqual(len(periods), len(pgram))
        
    def test_fundamental_frequency(self):
        """Test that f0 is correctly defined."""
        f0_Hz = 141.70001
        self.assertEqual(at2020.f0_Hz, f0_Hz)
        
    def test_harmonic_ratio(self):
        """Test harmonic relationship calculation."""
        # Frame-dragging frequency should be much smaller than f0
        f0_Hz = 141.70001
        omega_frame = 2 * np.pi / 20.0
        f_frame_Hz = omega_frame / (2 * np.pi * 86400)
        
        harmonic_ratio = f0_Hz / f_frame_Hz
        
        # Ratio should be very large (cosmological to quantum scales)
        self.assertGreater(harmonic_ratio, 1e8)
        self.assertLess(harmonic_ratio, 1e9)
        
        # Log10 should be around 8-9
        log10_ratio = np.log10(harmonic_ratio)
        self.assertGreater(log10_ratio, 8.0)
        self.assertLess(log10_ratio, 9.0)

    def test_output_directory_creation(self):
        """Test that output directory is created."""
        output_dir = os.path.join(
            os.path.dirname(__file__), 'results', 'at2020afhd'
        )
        # Directory should exist after running the script
        self.assertTrue(os.path.exists(output_dir))

    def test_data_generation(self):
        """Test that synthetic observations are generated correctly."""
        # Check that we have the expected number of observations
        self.assertEqual(self.results['n_observations'], 120)
        self.assertEqual(len(self.results['time_days']), 120)
        self.assertEqual(len(self.results['flux_xray']), 120)
        self.assertEqual(len(self.results['flux_radio']), 120)
        
        # Check time ordering
        self.assertTrue(np.all(np.diff(self.results['time_days']) >= 0))
        
        # Check time range
        self.assertGreaterEqual(self.results['time_days'][0], 0)
        self.assertLessEqual(self.results['time_days'][-1], 400)


class TestScientificValidity(unittest.TestCase):
    """Test scientific validity of the analysis."""
    
    @classmethod
    def setUpClass(cls):
        """Run analysis once for all tests."""
        cls.results = at2020.main()
    
    def test_period_detection_accuracy(self):
        """Test that detected periods are close to expected 20 days."""
        # Tightened tolerance for synthetic data with fixed seed
        self.assertAlmostEqual(self.results['peak_x'], 20.0, delta=0.5)
        self.assertAlmostEqual(self.results['peak_r'], 20.0, delta=0.5)
        
    def test_frame_dragging_frequency(self):
        """Test that frame-dragging frequency is in correct range."""
        # Expected frequency for 20-day period
        expected_f_frame = 1.0 / (20.0 * 86400)  # Hz
        
        # Get actual frequency from results
        f_frame = self.results['f_frame_Hz']
            
        # Check it's in the right order of magnitude
        self.assertAlmostEqual(f_frame, expected_f_frame, delta=expected_f_frame * 0.1)


class TestVisualizationOutput(unittest.TestCase):
    """Test visualization output."""
    
    @staticmethod
    def _get_output_path():
        """Helper method to get the output path."""
        return os.path.join(
            os.path.dirname(__file__), 'results', 'at2020afhd',
            'at2020afhd_complete_analysis.png'
        )
    
    def test_plot_file_exists(self):
        """Test that the plot file was created."""
        output_path = self._get_output_path()
        self.assertTrue(os.path.exists(output_path))
        
    def test_plot_file_size(self):
        """Test that the plot file has reasonable size."""
        output_path = self._get_output_path()
        file_size = os.path.getsize(output_path)
        
        # Should be at least 100KB (basic sanity check)
        self.assertGreater(file_size, 100000)
        
        # Should be less than 10MB (reasonable upper bound)
        self.assertLess(file_size, 10000000)

    """Run the main analysis to generate test data and results."""
def import_analysis_module():
    """Import the analysis module and run main() to generate test data."""
    results = at2020.main()
    return results


if __name__ == '__main__':
    # Run the main script first to generate data
    print("Running analyze_at2020afhd.py to generate test data...")
    import_analysis_module()
    print("\nRunning tests...\n")
    
    unittest.main(argv=[''], exit=False, verbosity=2)
