#!/usr/bin/env python3
"""
Test script for AT2020afhd analysis

Tests data download, analysis, and result validation for the
Tidal Disruption Event analysis pipeline.
"""

import os
import sys
import json
import unittest
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAT2020afhdDownload(unittest.TestCase):
    """Test data download functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.data_dir = Path('data/tde/at2020afhd')
        self.xray_file = self.data_dir / 'xray' / 'swift_xray_at2020afhd.csv'
        self.radio_file = self.data_dir / 'radio' / 'vla_radio_at2020afhd.csv'
        self.metadata_file = self.data_dir / 'metadata.json'
    
    def test_data_directory_exists(self):
        """Test that data directory exists after download"""
        self.assertTrue(
            self.data_dir.exists(),
            f"Data directory {self.data_dir} should exist"
        )
    
    def test_xray_data_exists(self):
        """Test that X-ray data file exists"""
        self.assertTrue(
            self.xray_file.exists(),
            f"X-ray data file {self.xray_file} should exist"
        )
    
    def test_radio_data_exists(self):
        """Test that radio data file exists"""
        self.assertTrue(
            self.radio_file.exists(),
            f"Radio data file {self.radio_file} should exist"
        )
    
    def test_metadata_exists(self):
        """Test that metadata file exists"""
        self.assertTrue(
            self.metadata_file.exists(),
            f"Metadata file {self.metadata_file} should exist"
        )
    
    def test_xray_data_format(self):
        """Test X-ray data has correct format"""
        if not self.xray_file.exists():
            self.skipTest("X-ray data not downloaded yet")
        
        import pandas as pd
        df = pd.read_csv(self.xray_file)
        
        # Check required columns
        required_cols = ['time_mjd', 'flux', 'flux_error']
        for col in required_cols:
            self.assertIn(col, df.columns, f"Column {col} should exist")
        
        # Check data integrity
        self.assertGreater(len(df), 0, "Should have observations")
        self.assertTrue(all(df['flux'] >= 0), "Flux should be non-negative")
        self.assertTrue(all(df['flux_error'] >= 0), "Errors should be non-negative")
    
    def test_radio_data_format(self):
        """Test radio data has correct format"""
        if not self.radio_file.exists():
            self.skipTest("Radio data not downloaded yet")
        
        import pandas as pd
        df = pd.read_csv(self.radio_file)
        
        # Check required columns
        required_cols = ['time_mjd', 'flux_mjy', 'flux_error_mjy']
        for col in required_cols:
            self.assertIn(col, df.columns, f"Column {col} should exist")
        
        # Check data integrity
        self.assertGreater(len(df), 0, "Should have observations")
        self.assertTrue(all(df['flux_mjy'] >= 0), "Flux should be non-negative")
    
    def test_metadata_format(self):
        """Test metadata has correct format"""
        if not self.metadata_file.exists():
            self.skipTest("Metadata not created yet")
        
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Check required fields
        self.assertIn('object', metadata)
        self.assertEqual(metadata['object'], 'AT2020afhd')
        self.assertIn('precession_period_days', metadata)
        self.assertAlmostEqual(metadata['precession_period_days'], 19.8, delta=1.0)


class TestAT2020afhdAnalysis(unittest.TestCase):
    """Test analysis functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.results_dir = Path('results/at2020afhd')
        self.results_file = self.results_dir / 'at2020afhd_results.json'
        self.lightcurves_plot = self.results_dir / 'at2020afhd_lightcurves.png'
        self.periodograms_plot = self.results_dir / 'at2020afhd_periodograms.png'
        self.combined_plot = self.results_dir / 'at2020afhd_combined_analysis.png'
    
    def test_results_directory_exists(self):
        """Test that results directory exists"""
        if not self.results_file.exists():
            self.skipTest("Analysis not run yet")
        
        self.assertTrue(
            self.results_dir.exists(),
            f"Results directory {self.results_dir} should exist"
        )
    
    def test_results_file_exists(self):
        """Test that results JSON exists"""
        if not Path('data/tde/at2020afhd').exists():
            self.skipTest("Data not downloaded yet")
        
        self.assertTrue(
            self.results_file.exists(),
            f"Results file {self.results_file} should exist"
        )
    
    def test_results_structure(self):
        """Test results JSON has correct structure"""
        if not self.results_file.exists():
            self.skipTest("Analysis not run yet")
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        # Check top-level keys
        self.assertIn('object', results)
        self.assertIn('analysis_type', results)
        self.assertIn('xray', results)
        self.assertIn('radio', results)
        self.assertIn('interpretation', results)
        
        # Check X-ray results
        xray = results['xray']
        self.assertIn('n_observations', xray)
        self.assertIn('fit_period_days', xray)
        self.assertIn('fit_chi2_reduced', xray)
        
        # Check radio results
        radio = results['radio']
        self.assertIn('n_observations', radio)
        self.assertIn('fit_period_days', radio)
        self.assertIn('fit_chi2_reduced', radio)
    
    def test_period_detection(self):
        """Test that detected periods are reasonable"""
        if not self.results_file.exists():
            self.skipTest("Analysis not run yet")
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        xray_period = results['xray']['fit_period_days']
        radio_period = results['radio']['fit_period_days']
        
        # X-ray period should be within reasonable range
        # (Allowing for variation in simulated data)
        self.assertGreater(xray_period, 5, "X-ray period too short")
        self.assertLess(xray_period, 40, "X-ray period too long")
        
        # Radio period should also be reasonable
        self.assertGreater(radio_period, 5, "Radio period too short")
        self.assertLess(radio_period, 40, "Radio period too long")
    
    def test_chi_squared_reasonable(self):
        """Test that chi-squared values are reasonable"""
        if not self.results_file.exists():
            self.skipTest("Analysis not run yet")
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        xray_chi2 = results['xray']['fit_chi2_reduced']
        radio_chi2 = results['radio']['fit_chi2_reduced']
        
        # Chi-squared should be positive and reasonable
        self.assertGreater(xray_chi2, 0, "X-ray χ² should be positive")
        self.assertLess(xray_chi2, 10, "X-ray χ² too large (bad fit)")
        
        self.assertGreater(radio_chi2, 0, "Radio χ² should be positive")
        self.assertLess(radio_chi2, 10, "Radio χ² too large (bad fit)")
    
    def test_plots_generated(self):
        """Test that plots are generated"""
        if not self.results_file.exists():
            self.skipTest("Analysis not run yet")
        
        # Check that at least one plot exists
        plot_exists = (
            self.lightcurves_plot.exists() or
            self.periodograms_plot.exists() or
            self.combined_plot.exists()
        )
        
        self.assertTrue(
            plot_exists,
            "At least one plot should be generated"
        )


class TestQCALConnection(unittest.TestCase):
    """Test QCAL framework connection"""
    
    def test_frequency_calculation(self):
        """Test QCAL frequency comparison"""
        # Period in days
        period_days = 20.0
        
        # Convert to Hz
        period_seconds = period_days * 86400
        f_prec = 1 / period_seconds
        
        # QCAL fundamental
        f0_qcal = 141.7
        
        # Scale ratio
        ratio = f0_qcal / f_prec
        
        # Should be on order of 10^8
        self.assertGreater(ratio, 1e7, "Scale ratio should be > 10^7")
        self.assertLess(ratio, 1e9, "Scale ratio should be < 10^9")
        
        # Log scale
        log_ratio = np.log10(ratio)
        self.assertGreater(log_ratio, 7, "Log scale should be > 7")
        self.assertLess(log_ratio, 9, "Log scale should be < 9")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAT2020afhdDownload))
    suite.addTests(loader.loadTestsFromTestCase(TestAT2020afhdAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestQCALConnection))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("AT2020afhd Analysis Test Suite")
    print("="*60 + "\n")
    
    success = run_tests()
    
    print("\n" + "="*60)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
