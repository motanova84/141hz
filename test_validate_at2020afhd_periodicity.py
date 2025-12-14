#!/usr/bin/env python3
"""
Test suite for AT2020afhd periodicity validation script.

This test suite validates the correctness of the AT2020afhd periodicity
calculations and ensures the script properly verifies the fractal harmonic
relationship with f₀ = 141.7001 Hz.
"""

import unittest
import sys
import json
from pathlib import Path
import tempfile
import subprocess

# Import the validation module
try:
    import validate_at2020afhd_periodicity as validator
except ImportError:
    print("❌ Could not import validate_at2020afhd_periodicity module")
    sys.exit(1)


class TestAT2020afdPeriodicityValidation(unittest.TestCase):
    """Test cases for AT2020afhd periodicity validation."""
    
    def test_calculate_periodicity_validation(self):
        """Test that periodicity validation calculation returns expected values."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Check that all required keys are present
        required_keys = [
            'period_days', 'period_uncertainty', 'period_seconds',
            'f_frame_hz', 'f0_hz', 'harmonic_ratio', 'octaves',
            'decades', 'expected_ratio', 'expected_octaves',
            'ratio_error_percent', 'octaves_error',
            'period_validated', 'ratio_validated', 'octaves_validated',
            'all_checks_passed'
        ]
        
        for key in required_keys:
            self.assertIn(key, results, f"Missing key: {key}")
    
    def test_period_in_range(self):
        """Test that detected period is within published range."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Published value: 19.6 ± 0.5 days
        self.assertGreaterEqual(results['period_days'], 19.0)
        self.assertLessEqual(results['period_days'], 20.5)
        self.assertTrue(results['period_validated'])
    
    def test_fundamental_frequency(self):
        """Test that fundamental frequency f₀ is correct."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # f₀ = 141.70001 Hz
        self.assertAlmostEqual(results['f0_hz'], 141.70001, places=5)
    
    def test_frame_frequency_order_of_magnitude(self):
        """Test that frame frequency is in expected order of magnitude."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # f_frame ≈ 5.897×10⁻⁷ Hz
        self.assertGreater(results['f_frame_hz'], 5e-7)
        self.assertLess(results['f_frame_hz'], 6e-7)
    
    def test_harmonic_ratio(self):
        """Test that harmonic ratio is within expected range."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Expected: ~2.403×10⁸
        self.assertGreater(results['harmonic_ratio'], 2.3e8)
        self.assertLess(results['harmonic_ratio'], 2.5e8)
        
        # Error should be less than 1%
        self.assertLess(results['ratio_error_percent'], 1.0)
        self.assertTrue(results['ratio_validated'])
    
    def test_fractal_cascade_octaves(self):
        """Test that fractal cascade is approximately 27.84 octaves."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Expected: ~27.84 octaves
        self.assertGreater(results['octaves'], 27.7)
        self.assertLess(results['octaves'], 28.0)
        
        # Error should be less than 0.1 octaves
        self.assertLess(results['octaves_error'], 0.1)
        self.assertTrue(results['octaves_validated'])
    
    def test_all_validations_pass(self):
        """Test that all validation checks pass."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        self.assertTrue(results['all_checks_passed'],
                       "Not all validation checks passed")
    
    def test_generate_validation_report(self):
        """Test that validation report generation works."""
        results = validator.calculate_periodicity_validation(precision=50)
        report = validator.generate_validation_report(results)
        
        # Check that report contains key information
        self.assertIn("AT2020afhd", report)
        self.assertIn("PERIODICITY VALIDATION", report)
        self.assertIn("141.70001", report)
        self.assertIn("octaves", report)
        
        # Check for success message
        if results['all_checks_passed']:
            self.assertIn("ALL VALIDATIONS PASSED", report)
    
    def test_json_output(self):
        """Test that JSON output is correctly formatted."""
        results = validator.calculate_periodicity_validation(precision=50)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_output.json"
            validator.generate_validation_report(results, output_path)
            
            # Check that file was created
            self.assertTrue(output_path.exists())
            
            # Load and validate JSON
            with open(output_path) as f:
                data = json.load(f)
            
            self.assertIn('validation_type', data)
            self.assertEqual(data['validation_type'], 'at2020afhd_periodicity')
            self.assertIn('timestamp', data)
            self.assertIn('results', data)
            self.assertIn('status', data)
            
            if results['all_checks_passed']:
                self.assertEqual(data['status'], 'PASSED')
    
    def test_high_precision_calculation(self):
        """Test that high precision calculations work."""
        # Test with different precision levels
        for precision in [30, 50, 100]:
            results = validator.calculate_periodicity_validation(precision=precision)
            self.assertTrue(results['all_checks_passed'],
                          f"Validation failed at precision {precision}")
    
    def test_cli_execution(self):
        """Test that CLI script executes without errors."""
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, 'validate_at2020afhd_periodicity.py', '--no-json'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        # Check that script executed successfully
        self.assertEqual(result.returncode, 0,
                        f"Script failed with stderr: {result.stderr}")
        
        # Check that output contains expected content
        self.assertIn("AT2020afhd", result.stdout)
        self.assertIn("VALIDATION", result.stdout)


class TestAT2020afdTheoreticalValues(unittest.TestCase):
    """Test theoretical values and relationships."""
    
    def test_period_conversion(self):
        """Test period to frequency conversion."""
        # 19.62 days = 19.62 * 86400 seconds
        expected_seconds = 19.62 * 86400
        
        results = validator.calculate_periodicity_validation(precision=50)
        self.assertAlmostEqual(results['period_seconds'], expected_seconds, places=1)
    
    def test_octaves_to_ratio_relationship(self):
        """Test that octaves and ratio are consistent."""
        import math
        
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Verify: octaves = log₂(ratio)
        calculated_octaves = math.log2(results['harmonic_ratio'])
        self.assertAlmostEqual(results['octaves'], calculated_octaves, places=2)
    
    def test_decades_to_ratio_relationship(self):
        """Test that decades and ratio are consistent."""
        import math
        
        results = validator.calculate_periodicity_validation(precision=50)
        
        # Verify: decades = log₁₀(ratio)
        calculated_decades = math.log10(results['harmonic_ratio'])
        self.assertAlmostEqual(results['decades'], calculated_decades, places=2)


def run_tests():
    """Run all tests and return success status."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAT2020afdPeriodicityValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestAT2020afdTheoreticalValues))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
