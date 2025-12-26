#!/usr/bin/env python3
"""
Test suite for validate_riemann_zeros.py

Validates the Riemann zeros computation implementation without requiring
extensive computation time.
"""

import json
import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import validate_riemann_zeros as vrz

# Import mpmath
try:
    import mpmath as mp
except ImportError:
    print("❌ Error: mpmath is required for tests")
    sys.exit(1)


class TestRiemannZerosValidation(unittest.TestCase):
    """Test cases for Riemann zeros validation."""

    def test_get_riemann_zeros_basic(self):
        """Test that get_riemann_zeros returns valid zeros."""
        zeros = vrz.get_riemann_zeros(T=100, limit=10)
        
        self.assertEqual(len(zeros), 10)
        
        # First zero should be approximately 14.134725
        self.assertAlmostEqual(float(zeros[0]), 14.134725, places=5)
        
        # Zeros should be in ascending order
        for i in range(len(zeros) - 1):
            self.assertLess(zeros[i], zeros[i + 1])
        
        # All zeros should be positive
        for z in zeros:
            self.assertGreater(float(z), 0)

    def test_get_riemann_zeros_limit(self):
        """Test that limit parameter works correctly."""
        zeros_10 = vrz.get_riemann_zeros(T=1000, limit=10)
        zeros_20 = vrz.get_riemann_zeros(T=1000, limit=20)
        
        self.assertEqual(len(zeros_10), 10)
        self.assertEqual(len(zeros_20), 20)
        
        # First 10 should match
        for i in range(10):
            self.assertEqual(zeros_10[i], zeros_20[i])

    def test_compute_zeros_sum_positive(self):
        """Test that compute_zeros_sum returns positive values."""
        sum_val, num_zeros = vrz.compute_zeros_sum(T=100, alpha=0.01, precision=30)
        
        self.assertGreater(float(sum_val), 0)
        self.assertGreater(num_zeros, 0)
        self.assertIsInstance(num_zeros, int)

    def test_compute_zeros_sum_decreases_with_alpha(self):
        """Test that sum decreases as alpha increases."""
        sum_low, _ = vrz.compute_zeros_sum(T=100, alpha=0.001, precision=30)
        sum_high, _ = vrz.compute_zeros_sum(T=100, alpha=0.01, precision=30)
        
        self.assertGreater(float(sum_low), float(sum_high))

    def test_validate_zeros_relationship_structure(self):
        """Test that validation results have correct structure."""
        results = vrz.validate_zeros_relationship(precision=30, alpha=0.006695, T=500)
        
        # Check top-level keys
        self.assertIn("constants", results)
        self.assertIn("parameters", results)
        self.assertIn("computation", results)
        self.assertIn("status", results)
        
        # Check constants
        self.assertIn("phi", results["constants"])
        self.assertIn("gamma", results["constants"])
        self.assertIn("pi", results["constants"])
        self.assertIn("e_gamma_pi", results["constants"])
        
        # Check computation results
        self.assertIn("zeros_sum", results["computation"])
        self.assertIn("expected_sum", results["computation"])
        self.assertIn("validation_result", results["computation"])
        
        # Check status is valid
        self.assertIn(results["status"], ["PASS", "FAIL"])

    def test_validate_zeros_relationship_with_optimal_alpha(self):
        """Test validation with optimal alpha for small dataset."""
        # Use small T for faster testing
        results = vrz.validate_zeros_relationship(precision=30, alpha=0.006695, T=500)
        
        # Sum should be positive
        self.assertGreater(results["computation"]["zeros_sum"], 0)
        
        # Result should be positive
        self.assertGreater(results["computation"]["validation_result"], 0)

    def test_compute_frequency_structure(self):
        """Test that frequency computation has correct structure."""
        results = vrz.compute_frequency(precision=30)
        
        # Check top-level keys
        self.assertIn("frequency_hz", results)
        self.assertIn("components", results)
        self.assertIn("precision_digits", results)
        
        # Check components
        self.assertIn("f_base", results["components"])
        self.assertIn("scaling_factor", results["components"])
        self.assertIn("psi_prime", results["components"])
        self.assertIn("psi_effective", results["components"])
        self.assertIn("delta_correction", results["components"])
        
        # Frequency should be positive
        self.assertGreater(results["frequency_hz"], 0)

    def test_compute_frequency_consistent_precision(self):
        """Test that frequency computation respects precision parameter."""
        results_low = vrz.compute_frequency(precision=20)
        results_high = vrz.compute_frequency(precision=50)
        
        # Should be approximately equal
        self.assertAlmostEqual(
            results_low["frequency_hz"],
            results_high["frequency_hz"],
            places=5
        )

    def test_find_optimal_alpha(self):
        """Test that find_optimal_alpha converges."""
        optimal_alpha, achieved_sum, iterations = vrz.find_optimal_alpha(
            target_sum=105.562150,
            T=500,
            precision=30,
            tolerance=0.01
        )
        
        # Alpha should be in reasonable range
        self.assertGreater(optimal_alpha, 0)
        self.assertLess(optimal_alpha, 1)
        
        # Should achieve close to target
        self.assertAlmostEqual(achieved_sum, 105.562150, delta=2.0)
        
        # Should converge in reasonable iterations
        self.assertLess(iterations, 50)

    def test_constants_values(self):
        """Test that fundamental constants have expected values."""
        mp.dps = 50
        
        phi = mp.mpf('1.618033988749894848204586834365638117720309179805762862135448622705260')
        gamma = mp.mpf('0.577215664901532860606512090082402431042159335939923598805767234648689')
        pi = mp.mpf('3.141592653589793238462643383279502884197169399375105820974944592307816')
        
        # Check phi (golden ratio)
        self.assertAlmostEqual(float(phi), 1.618033988749895, places=14)
        
        # Check gamma (Euler-Mascheroni constant)
        self.assertAlmostEqual(float(gamma), 0.5772156649015329, places=15)
        
        # Check pi
        self.assertAlmostEqual(float(pi), 3.141592653589793, places=15)
        
        # Check e^(γπ)
        e_gamma_pi = mp.exp(gamma * pi)
        self.assertAlmostEqual(float(e_gamma_pi), 6.131114182422604, places=10)

    def test_run_complete_validation_structure(self):
        """Test that complete validation has correct structure."""
        results = vrz.run_complete_validation(precision=30, alpha=0.006695, T=500)
        
        # Check top-level keys
        self.assertIn("timestamp", results)
        self.assertIn("precision_digits", results)
        self.assertIn("validation_suite", results)
        self.assertIn("zeros_validation", results)
        self.assertIn("frequency_computation", results)
        self.assertIn("overall_status", results)
        self.assertIn("summary", results)
        
        # Check summary
        self.assertIn("tests_run", results["summary"])
        self.assertIn("tests_passed", results["summary"])
        self.assertIn("tests_failed", results["summary"])
        
        # Validation suite should be riemann_zeros
        self.assertEqual(results["validation_suite"], "riemann_zeros")


class TestRiemannZerosIntegration(unittest.TestCase):
    """Integration tests for the validation script."""

    def test_complete_validation_runs(self):
        """Test that complete validation runs without errors."""
        # Test with smaller dataset for faster execution
        results = vrz.run_complete_validation(precision=20, alpha=0.006695, T=500)
        
        # Should return a dict
        self.assertIsInstance(results, dict)
        
        # Should have expected keys
        self.assertIn("overall_status", results)
        self.assertIn("zeros_validation", results)
        self.assertIn("frequency_computation", results)
        
        # Status should be valid
        self.assertIn(results["overall_status"], ["PASS", "FAIL"])

    def test_output_file_can_be_created(self):
        """Test that validation results can be saved as JSON."""
        output_path = Path("/tmp/test_riemann_zeros.json")
        if output_path.exists():
            output_path.unlink()
        
        # Run validation
        results = vrz.run_complete_validation(precision=20, alpha=0.006695, T=500)
        
        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # File should be created
        self.assertTrue(output_path.exists())
        
        # Should be valid JSON
        with open(output_path, 'r') as f:
            data = json.load(f)
            self.assertIn("validation_suite", data)
            self.assertEqual(data["validation_suite"], "riemann_zeros")
        
        # Clean up
        output_path.unlink()


if __name__ == '__main__':
    unittest.main()
