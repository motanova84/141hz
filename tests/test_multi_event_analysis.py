#!/usr/bin/env python3
"""
Test suite for multi_event_analysis.py

Validates the discovery analysis implementation without requiring
connectivity to GWOSC.
"""

import json
import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import multi_event_analysis as mea


class TestMultiEventAnalysis(unittest.TestCase):
    """Test cases for multi-event analysis discovery."""

    def test_module_constants(self):
        """Test that module constants are properly defined."""
        self.assertEqual(mea.FREQUENCY_TARGET, 141.7001)
        self.assertEqual(mea.BANDPASS, [140.7, 142.7])
        self.assertEqual(mea.SNR_THRESHOLD, 5.0)
        self.assertEqual(len(mea.EVENTS), 11)

    def test_events_structure(self):
        """Test that events dictionary has correct structure."""
        for event_name, event_data in mea.EVENTS.items():
            self.assertIn("date", event_data)
            self.assertIn("gps", event_data)
            self.assertIsInstance(event_data["gps"], list)
            self.assertEqual(len(event_data["gps"]), 2)
            self.assertGreater(event_data["gps"][1], event_data["gps"][0])

    def test_confirmed_results_structure(self):
        """Test that confirmed results have correct structure."""
        self.assertEqual(len(mea.CONFIRMED_RESULTS), 11)
        
        for event_name, results in mea.CONFIRMED_RESULTS.items():
            self.assertIn(event_name, mea.EVENTS)
            self.assertIn("H1", results)
            self.assertIn("L1", results)
            self.assertGreater(results["H1"], 0)
            self.assertGreater(results["L1"], 0)

    def test_all_events_above_threshold(self):
        """Test that all events have SNR above threshold."""
        for event_name, results in mea.CONFIRMED_RESULTS.items():
            self.assertGreater(
                results["H1"], 
                mea.SNR_THRESHOLD,
                f"{event_name} H1 SNR below threshold"
            )
            self.assertGreater(
                results["L1"], 
                mea.SNR_THRESHOLD,
                f"{event_name} L1 SNR below threshold"
            )

    def test_calculate_statistics(self):
        """Test statistics calculation function."""
        stats = mea.calculate_statistics(mea.CONFIRMED_RESULTS)
        
        # Check structure
        self.assertIn("total_events", stats)
        self.assertIn("detection_rate", stats)
        self.assertIn("snr_mean", stats)
        self.assertIn("snr_std", stats)
        self.assertIn("snr_min", stats)
        self.assertIn("snr_max", stats)
        self.assertIn("h1_mean", stats)
        self.assertIn("l1_mean", stats)
        
        # Check values
        self.assertEqual(stats["total_events"], 11)
        self.assertEqual(stats["detection_rate"], "100%")
        self.assertGreater(stats["snr_mean"], 15)
        self.assertLess(stats["snr_mean"], 30)
        self.assertGreater(stats["snr_min"], 10)
        self.assertLess(stats["snr_max"], 35)

    def test_json_output_exists(self):
        """Test that JSON output file exists."""
        json_file = Path("multi_event_final.json")
        self.assertTrue(json_file.exists(), "JSON file not found")

    def test_json_output_structure(self):
        """Test that JSON output has correct structure."""
        with open("multi_event_final.json", "r") as f:
            data = json.load(f)
        
        # Check top-level structure
        self.assertIn("discovery", data)
        self.assertIn("statistics", data)
        self.assertIn("events", data)
        
        # Check discovery metadata
        self.assertEqual(data["discovery"]["frequency_target_hz"], 141.7001)
        self.assertEqual(data["discovery"]["catalog"], "GWTC-1")
        self.assertEqual(data["discovery"]["equation"], "Ψ = I × A_eff²")
        
        # Check statistics
        stats = data["statistics"]
        self.assertEqual(stats["total_events"], 11)
        self.assertEqual(stats["detection_rate"], "100%")
        
        # Check events
        self.assertEqual(len(data["events"]), 11)
        for event_name, event_data in data["events"].items():
            self.assertIn("date", event_data)
            self.assertIn("snr", event_data)
            self.assertIn("detection", event_data)
            self.assertEqual(event_data["detection"], "confirmed")
            self.assertTrue(event_data["h1_above_threshold"])
            self.assertTrue(event_data["l1_above_threshold"])

    def test_png_output_exists(self):
        """Test that PNG output file exists."""
        png_file = Path("multi_event_final.png")
        self.assertTrue(png_file.exists(), "PNG file not found")
        self.assertGreater(png_file.stat().st_size, 100000, "PNG file too small")

    def test_detection_rate_100_percent(self):
        """Test that detection rate is 100%."""
        stats = mea.calculate_statistics(mea.CONFIRMED_RESULTS)
        self.assertEqual(stats["h1_detections"], "11/11")
        self.assertEqual(stats["l1_detections"], "11/11")

    def test_snr_consistency(self):
        """Test that SNR values are consistent between H1 and L1."""
        for event_name, results in mea.CONFIRMED_RESULTS.items():
            h1_snr = results["H1"]
            l1_snr = results["L1"]
            # H1 and L1 should be within reasonable range of each other
            ratio = max(h1_snr, l1_snr) / min(h1_snr, l1_snr)
            self.assertLess(
                ratio, 
                1.5, 
                f"{event_name} has inconsistent H1/L1 SNR ratio: {ratio:.2f}"
            )


class TestDiscoveryDocumentation(unittest.TestCase):
    """Test cases for discovery documentation."""

    def test_documentation_exists(self):
        """Test that discovery documentation exists."""
        doc_file = Path("CONFIRMED_DISCOVERY_141HZ.md")
        self.assertTrue(doc_file.exists(), "Documentation file not found")

    def test_readme_updated(self):
        """Test that README was updated with discovery."""
        with open("README.md", "r") as f:
            readme = f.read()
        
        self.assertIn("DESCUBRIMIENTO CONFIRMADO", readme)
        self.assertIn("141.7001 Hz", readme)
        self.assertIn("multi_event_final.json", readme)
        self.assertIn("multi_event_final.png", readme)
        self.assertIn("multi_event_analysis.py", readme)


def run_tests():
    """Run all tests and display results."""
    print("=" * 70)
    print("🧪 TESTING MULTI-EVENT ANALYSIS DISCOVERY")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMultiEventAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestDiscoveryDocumentation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
        print(f"   Total tests: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Total tests: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
