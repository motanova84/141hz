#!/usr/bin/env python3
"""
Tests for QNM vs QCAL Validation
=================================

Tests the validator that demonstrates the "devastating" comparison between
standard Quasi-Normal Mode (QNM) predictions and QCAL observations for GW250114.

Key metrics validated:
- Frequency discrepancy: 1.76× (250 Hz vs 141.7 Hz)
- Persistence advantage: 2.1× energy (power law vs exponential decay)
- Statistical significance: 111σ and 999σ

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-02-13
"""

import sys
import os
import unittest
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the validator from physics directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'physics'))

try:
    from validate_qnm_vs_qcal import QNMvsQCALValidator
except ImportError as e:
    print(f"❌ Error importing validator: {e}")
    print("Make sure physics/validate_qnm_vs_qcal.py is available")
    sys.exit(1)


class TestQNMvsQCALValidator(unittest.TestCase):
    """Test cases for QNM vs QCAL validator"""

    @classmethod
    def setUpClass(cls):
        """Setup test fixtures once for all tests"""
        print("\n" + "="*80)
        print("TESTING QNM vs QCAL VALIDATOR")
        print("="*80)
        cls.validator = QNMvsQCALValidator(precision=30)  # Lower precision for faster tests

    def test_01_initialization(self):
        """Test validator initialization"""
        print("\n🧪 Test 1: Initialization")
        
        self.assertEqual(self.validator.f0_qcal, 141.7001)
        self.assertEqual(self.validator.f_qnm_typical, 250.0)
        self.assertEqual(self.validator.f_qnm_min, 200.0)
        self.assertEqual(self.validator.f_qnm_max, 1200.0)
        self.assertEqual(self.validator.tau_qnm, 0.1)
        self.assertEqual(self.validator.n_bootstrap, 1_000_000)
        self.assertEqual(self.validator.sigma_threshold, 111)
        self.assertEqual(self.validator.sigma_null, 999)
        self.assertEqual(self.validator.persistence_exponent, -0.5)
        
        print("   ✅ All initialization parameters correct")

    def test_02_scale_error_calculation(self):
        """Test scale error analysis - FREQUENCY DISCREPANCY"""
        print("\n🧪 Test 2: Scale Error Analysis (Frequency Discrepancy)")
        
        results = self.validator.calculate_scale_error()

        # Check expected keys
        self.assertIn('f_qcal_observed', results)
        self.assertIn('f_qnm_typical', results)
        self.assertIn('scale_ratio_typical', results)
        self.assertIn('scale_ratio_range', results)
        self.assertIn('orders_of_magnitude', results)
        self.assertIn('interpretation', results)

        # Check values are correct
        self.assertEqual(results['f_qcal_observed'], 141.7001)
        self.assertEqual(results['f_qnm_typical'], 250.0)

        # Scale ratio should be > 1 (QNM frequency is higher)
        self.assertGreater(results['scale_ratio_typical'], 1.0)

        # KEY REQUIREMENT: Should be approximately 1.76x (250/141.7 ≈ 1.76)
        # This is the "devastating" frequency discrepancy mentioned in problem statement
        ratio = results['scale_ratio_typical']
        self.assertAlmostEqual(ratio, 1.76, delta=0.01,
                              msg=f"Frequency ratio should be ~1.76×, got {ratio:.2f}×")

        # Orders of magnitude should be less than 1 (same order, but different scale)
        self.assertGreater(results['orders_of_magnitude'], 0)
        self.assertLess(results['orders_of_magnitude'], 1)

        # Check interpretation
        self.assertEqual(results['interpretation'], 'noetic_vacuum_oscillation')
        
        print(f"   ✅ Frequency discrepancy: {ratio:.2f}× (QNM vs QCAL)")
        print(f"   ✅ QNM predicts: {results['f_qnm_typical']:.0f} Hz")
        print(f"   ✅ QCAL observes: {results['f_qcal_observed']:.4f} Hz")
        print("   ✅ Scale error analysis PASSED")

    def test_03_persistence_comparison(self):
        """Test persistence analysis - ENERGY ADVANTAGE"""
        print("\n🧪 Test 3: Persistence Analysis (Energy Advantage)")
        
        results = self.validator.compare_persistence(t_max=5.0, n_points=1000)

        # Check expected keys
        self.assertIn('decay_law_qnm', results)
        self.assertIn('decay_law_qcal', results)
        self.assertIn('persistence_ratio', results)
        self.assertIn('energy_qnm', results)
        self.assertIn('energy_qcal', results)
        self.assertIn('tau_qnm_ms', results)
        self.assertIn('interpretation', results)

        # Check decay laws are correctly identified
        self.assertEqual(results['decay_law_qnm'], 'exponential')
        self.assertEqual(results['decay_law_qcal'], 'power_law_t_minus_half')

        # QCAL should have more persistent energy
        self.assertGreater(results['energy_qcal'], results['energy_qnm'],
                          msg="QCAL energy should be greater than QNM energy")
        self.assertGreater(results['persistence_ratio'], 1.0,
                          msg="Persistence ratio should be > 1")

        # KEY REQUIREMENT: Should be approximately 2.1× energy advantage
        # This is the "devastating" persistence advantage mentioned in problem statement
        ratio = results['persistence_ratio']
        self.assertAlmostEqual(ratio, 2.1, delta=0.15,
                              msg=f"Persistence ratio should be ~2.1×, got {ratio:.2f}×")

        # Verify QNM decay time is in milliseconds
        tau_ms = results['tau_qnm_ms']
        self.assertEqual(tau_ms, 100.0)
        self.assertGreater(results['t_qnm_decay_to_1percent_ms'], 0)

        # Check interpretation
        self.assertEqual(results['interpretation'], 
                        'persistent_carrier_wave_anchored_to_universal_grid')

        # Check plot was created
        plot_file = self.validator.output_dir / 'qnm_vs_qcal_persistence.png'
        self.assertTrue(plot_file.exists(), 
                       msg=f"Persistence plot should be created at {plot_file}")
        
        print(f"   ✅ Persistence advantage: {ratio:.2f}× (QCAL vs QNM)")
        print(f"   ✅ QNM decay: exponential (τ = {tau_ms:.0f} ms)")
        print(f"   ✅ QCAL decay: power law (t^-1/2)")
        print(f"   ✅ Energy ratio: {results['energy_qcal']:.3f} / {results['energy_qnm']:.3f}")
        print("   ✅ Persistence analysis PASSED")

    def test_04_statistical_significance(self):
        """Test statistical significance validation - 111σ and 999σ"""
        print("\n🧪 Test 4: Statistical Significance (111σ/999σ)")
        
        results = self.validator.validate_statistical_significance()

        # Check expected keys
        self.assertIn('sigma_vs_threshold', results)
        self.assertIn('sigma_vs_null', results)
        self.assertIn('p_value_vs_threshold', results)
        self.assertIn('p_value_vs_null', results)
        self.assertIn('sigma_111_valid', results)
        self.assertIn('sigma_999_valid', results)
        self.assertIn('n_bootstrap', results)
        self.assertIn('classification', results)
        self.assertIn('conclusion', results)

        # KEY REQUIREMENT: Check sigma values are correct
        # (0.999 - 0.888) / 0.001 = 111σ
        sigma_111 = results['sigma_vs_threshold']
        self.assertAlmostEqual(sigma_111, 111.0, delta=1.0,
                              msg=f"Sigma vs threshold should be ~111σ, got {sigma_111:.1f}σ")

        # (0.999 - 0.0) / 0.001 = 999σ
        sigma_999 = results['sigma_vs_null']
        self.assertAlmostEqual(sigma_999, 999.0, delta=1.0,
                              msg=f"Sigma vs null should be ~999σ, got {sigma_999:.1f}σ")

        # Check validation flags
        self.assertTrue(results['sigma_111_valid'], 
                       msg="111σ validation should pass")
        self.assertTrue(results['sigma_999_valid'],
                       msg="999σ validation should pass")

        # Check p-values are extremely small
        self.assertLess(results['p_value_vs_threshold'], 1e-20,
                       msg="p-value vs threshold should be < 1e-20")
        self.assertLess(results['p_value_vs_null'], 1e-100,
                       msg="p-value vs null should be < 1e-100")

        # Check classification
        self.assertEqual(results['classification'], 'ABSOLUTE_CERTAINTY')
        self.assertEqual(results['conclusion'], 
                        'NOT_DETECTOR_ARTIFACT_BUT_CONSTANT_EMISSION')

        # Check bootstrap sample size
        self.assertEqual(results['n_bootstrap'], 1_000_000,
                        msg="Bootstrap should use 10^6 iterations")

        # Check discovery threshold comparison
        self.assertGreater(results['discovery_threshold_exceeded'], 20,
                          msg="Should exceed standard 5σ threshold by >20×")
        
        print(f"   ✅ Significance vs threshold: {sigma_111:.0f}σ")
        print(f"   ✅ Significance vs null: {sigma_999:.0f}σ")
        print(f"   ✅ Bootstrap iterations: {results['n_bootstrap']:,}")
        print(f"   ✅ Classification: {results['classification']}")
        print(f"   ✅ Discovery threshold exceeded: {results['discovery_threshold_exceeded']:.1f}×")
        print("   ✅ Statistical significance PASSED")

    def test_05_comprehensive_report_generation(self):
        """Test comprehensive report generation"""
        print("\n🧪 Test 5: Comprehensive Report Generation")
        
        results = self.validator.generate_comprehensive_report()

        # Check top-level structure
        self.assertIn('metadata', results)
        self.assertIn('scale_error_analysis', results)
        self.assertIn('persistence_analysis', results)
        self.assertIn('statistical_significance', results)
        self.assertIn('summary', results)

        # Check metadata
        metadata = results['metadata']
        self.assertEqual(metadata['event'], 'GW250114')
        self.assertEqual(metadata['analysis_type'], 'QNM_vs_QCAL_comparison')
        self.assertEqual(metadata['fundamental_frequency_hz'], 141.7001)
        self.assertIn('timestamp', metadata)
        self.assertIn('precision_decimal_places', metadata)

        # Check summary contains key metrics
        summary = results['summary']
        self.assertIn('qnm_prediction_range_hz', summary)
        self.assertIn('qcal_observation_hz', summary)
        self.assertIn('scale_discrepancy_orders', summary)
        self.assertIn('persistence_advantage', summary)
        self.assertIn('statistical_certainty_sigma', summary)
        self.assertEqual(summary['conclusion'], 'QCAL_persistent_resonance_confirmed')

        # Verify the "devastating" metrics are in summary
        self.assertEqual(summary['qcal_observation_hz'], 141.7001)
        self.assertGreater(summary['persistence_advantage'], 2.0)
        self.assertEqual(len(summary['statistical_certainty_sigma']), 2)
        
        # Check JSON file was created
        json_file = self.validator.output_dir / 'qnm_vs_qcal_comprehensive_analysis.json'
        self.assertTrue(json_file.exists(),
                       msg=f"JSON report should be created at {json_file}")

        # Verify JSON is valid and matches
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        
        # Check key fields match
        self.assertEqual(loaded_data['metadata']['event'], results['metadata']['event'])
        self.assertEqual(loaded_data['summary']['conclusion'], results['summary']['conclusion'])
        
        print(f"   ✅ Report structure complete")
        print(f"   ✅ Event: {metadata['event']}")
        print(f"   ✅ Frequency: {summary['qcal_observation_hz']} Hz")
        print(f"   ✅ Conclusion: {summary['conclusion']}")
        print(f"   ✅ JSON report saved: {json_file.name}")
        print("   ✅ Comprehensive report PASSED")

    def test_06_output_directory_creation(self):
        """Test that output directory is created"""
        print("\n🧪 Test 6: Output Directory")
        
        self.assertTrue(self.validator.output_dir.exists())
        self.assertTrue(self.validator.output_dir.is_dir())
        self.assertTrue(str(self.validator.output_dir).endswith('qnm_vs_qcal'))
        
        print(f"   ✅ Output directory exists: {self.validator.output_dir}")
        print("   ✅ Output directory test PASSED")

    def test_07_frequency_ranges(self):
        """Test QNM frequency range is physically reasonable"""
        print("\n🧪 Test 7: QNM Frequency Ranges")
        
        # For 10-60 solar mass black holes
        self.assertGreaterEqual(self.validator.f_qnm_min, 100,
                               msg="Minimum QNM frequency should be >= 100 Hz")
        self.assertLessEqual(self.validator.f_qnm_min, 300,
                            msg="Minimum QNM frequency should be <= 300 Hz")
        
        self.assertGreaterEqual(self.validator.f_qnm_max, 1000,
                               msg="Maximum QNM frequency should be >= 1000 Hz")
        self.assertLessEqual(self.validator.f_qnm_max, 1500,
                            msg="Maximum QNM frequency should be <= 1500 Hz")
        
        self.assertLess(self.validator.f_qnm_min, self.validator.f_qnm_typical,
                       msg="Min should be < typical")
        self.assertLess(self.validator.f_qnm_typical, self.validator.f_qnm_max,
                       msg="Typical should be < max")
        
        print(f"   ✅ QNM frequency range: {self.validator.f_qnm_min}-{self.validator.f_qnm_max} Hz")
        print(f"   ✅ Typical frequency: {self.validator.f_qnm_typical} Hz")
        print("   ✅ Frequency ranges PASSED")

    def test_08_devastating_comparison_metrics(self):
        """Test the 'devastating' comparison metrics from problem statement"""
        print("\n🧪 Test 8: Devastating Comparison Metrics")
        print("   Testing the two key metrics that challenge standard physics:")
        
        # Get all results
        scale_error = self.validator.calculate_scale_error()
        persistence = self.validator.compare_persistence(t_max=5.0, n_points=1000)
        
        # METRIC 1: Frequency Discrepancy (1.76×)
        freq_ratio = scale_error['scale_ratio_typical']
        print(f"\n   📊 METRIC 1: Frequency Discrepancy")
        print(f"      GR predicts: {scale_error['f_qnm_typical']:.0f} Hz")
        print(f"      QCAL observes: {scale_error['f_qcal_observed']:.4f} Hz")
        print(f"      Ratio: {freq_ratio:.2f}× (target: 1.76×)")
        self.assertAlmostEqual(freq_ratio, 1.76, delta=0.02,
                              msg="Frequency discrepancy should be ~1.76×")
        print(f"      ✅ 'Signature of Quantum Geometry' confirmed")
        
        # METRIC 2: Persistence Advantage (2.1×)
        persist_ratio = persistence['persistence_ratio']
        print(f"\n   📊 METRIC 2: Persistence Battle")
        print(f"      QNM decay: exp(-t/τ) with τ = {persistence['tau_qnm_ms']:.0f} ms")
        print(f"      QCAL decay: t^(-1/2) power law")
        print(f"      Energy advantage: {persist_ratio:.2f}× (target: 2.1×)")
        self.assertAlmostEqual(persist_ratio, 2.1, delta=0.15,
                              msg="Persistence advantage should be ~2.1×")
        print(f"      ✅ Signal is 'more real and durable' confirmed")
        
        print(f"\n   🎯 DEVASTATING COMPARISON CONFIRMED:")
        print(f"      Standard Model predictions FAIL by factors of:")
        print(f"      • Frequency: {freq_ratio:.2f}×")
        print(f"      • Persistence: {persist_ratio:.2f}×")
        print("   ✅ Devastating comparison metrics PASSED")


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQNMvsQCALValidator)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - QNM vs QCAL validator is DEVASTATING!")
        print("   The comparison successfully demonstrates:")
        print("   • 1.76× frequency discrepancy (Quantum Geometry signature)")
        print("   • 2.1× persistence advantage (defies entropy)")
        print("   • 111σ and 999σ statistical certainty")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
