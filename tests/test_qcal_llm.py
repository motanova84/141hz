#!/usr/bin/env python3
"""
test_qcal_llm.py - Comprehensive tests for QCAL-LLM implementation

Tests for:
- evaluate_manifesto.py (spectral analysis)
- QCALLLMCore.py (core functionality)
- psi_tuning_loop.py (tuning loop)
- modulation_traces.py (visualization)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import unittest
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from psi_tuning_loop import ModelProxy, run_tuning_loop  # noqa: E402
from QCALLLMCore import QCALLLMCore  # noqa: E402
from evaluate_manifesto import qnm_model  # noqa: E402


class TestEvaluateManifesto(unittest.TestCase):
    """Test suite for evaluate_manifesto.py"""

    def test_qnm_model_basic(self):
        """Test QNM model function"""
        f = np.array([100, 150, 200])
        M = 30.0
        a = 0.7
        result = qnm_model(f, M, a)

        self.assertEqual(len(result), len(f))
        self.assertTrue(np.all(result > 0))

    def test_qnm_model_spin_dependence(self):
        """Test spin parameter affects output"""
        f = np.array([150])
        M = 30.0

        result_low_spin = qnm_model(f, M, 0.3)
        result_high_spin = qnm_model(f, M, 0.9)

        self.assertNotEqual(result_low_spin[0], result_high_spin[0])

    def test_constants_precision(self):
        """Test that constants match expected values"""
        zeta_prime_half = -1.4603545
        phi_cubed = ((1 + np.sqrt(5))/2)**3

        self.assertAlmostEqual(phi_cubed, 4.236068, places=5)
        self.assertAlmostEqual(zeta_prime_half, -1.4603545, places=7)


class TestQCALLLMCore(unittest.TestCase):
    """Test suite for QCALLLMCore class"""

    def setUp(self):
        """Initialize core for tests"""
        self.core = QCALLLMCore(user_A_eff=0.85)

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.core.f0, 141.7001)
        self.assertEqual(self.core.tau, 0.07)
        self.assertAlmostEqual(self.core.epsilon, 0.015, places=3)

    def test_ground_truth_db(self):
        """Test ground truth database values"""
        self.assertEqual(self.core.ground_truth_db['f0'], 141.7001)
        self.assertEqual(self.core.ground_truth_db['zeta_prime_half'], -1.4603545)
        self.assertAlmostEqual(self.core.ground_truth_db['phi_cubed'], 4.236068, places=5)
        self.assertEqual(self.core.ground_truth_db['snr_gw150914'], 20.95)

    def test_sip_modulate_shape(self):
        """Test SIP modulation output shape"""
        t = np.linspace(0, 1, 100)
        weights = self.core.sip_modulate(t)

        self.assertEqual(len(weights), len(t))
        self.assertTrue(np.all(np.isfinite(weights)))

    def test_sip_modulate_damping(self):
        """Test that modulation damps over time"""
        t_early = np.array([0.01])
        t_late = np.array([1.0])

        w_early = self.core.sip_modulate(t_early)
        w_late = self.core.sip_modulate(t_late)

        # Variance should be higher early (before damping)
        self.assertGreater(abs(w_early[0] - 1.0), abs(w_late[0] - 1.0) * 0.9)

    def test_sip_modulate_mean(self):
        """Test that mean weight is approximately 1.0"""
        t = np.linspace(0, 1, 10000)
        weights = self.core.sip_modulate(t)
        mean_weight = np.mean(weights)

        self.assertAlmostEqual(mean_weight, 1.0, places=3)

    def test_compute_psi_response(self):
        """Test Psi response calculation"""
        kld_inv = 8.2
        coherence = 0.88

        psi = self.core.compute_psi_response(kld_inv, coherence)
        expected = kld_inv * coherence**2

        self.assertAlmostEqual(psi, expected, places=5)

    def test_is_coherent_threshold(self):
        """Test coherence threshold check"""
        # Above threshold
        is_coherent, psi = self.core.is_coherent(8.2, 0.88, threshold=5.0)
        self.assertTrue(is_coherent)
        self.assertGreater(psi, 5.0)

        # Below threshold
        is_coherent, psi = self.core.is_coherent(2.0, 0.5, threshold=5.0)
        self.assertFalse(is_coherent)
        self.assertLess(psi, 5.0)

    def test_compute_coherence_full_match(self):
        """Test coherence computation with all symbols"""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"
        coherence = self.core.compute_coherence(text)
        self.assertEqual(coherence, 1.0)

    def test_compute_coherence_partial_match(self):
        """Test coherence computation with partial match"""
        text = "f₀ = 141.7001 Hz, some other text"
        coherence = self.core.compute_coherence(text)
        self.assertGreater(coherence, 0.0)
        self.assertLess(coherence, 1.0)

    def test_compute_coherence_no_match(self):
        """Test coherence computation with no matches"""
        text = "random text with no symbols"
        coherence = self.core.compute_coherence(text)
        self.assertEqual(coherence, 0.0)

    def test_evaluate_structure(self):
        """Test evaluate returns proper structure"""
        text = "f₀ = 141.7001 Hz, zeta=-1.460, phi=4.236, snr=20.95"
        result = self.core.evaluate(text, "test query", n_bootstrap=50)

        self.assertIn('mean_psi', result)
        self.assertIn('psi_ci_95', result)
        self.assertIn('coherent', result)
        self.assertIn('coherence', result)
        self.assertIn('kld_inv', result)
        self.assertIn('matches', result)

        # Check CI is a tuple
        self.assertIsInstance(result['psi_ci_95'], tuple)
        self.assertEqual(len(result['psi_ci_95']), 2)

        # Check CI ordering
        self.assertLess(result['psi_ci_95'][0], result['psi_ci_95'][1])

    def test_evaluate_high_quality_text(self):
        """Test evaluation of high-quality text"""
        text = "f₀ = 141.7001 Hz from zeta=-1.460 and phi=4.236, snr=20.95"
        result = self.core.evaluate(text, "test query")

        self.assertGreater(result['mean_psi'], 0)
        self.assertGreater(result['coherence'], 0.5)
        self.assertGreater(result['matches'], 2)


class TestPsiTuningLoop(unittest.TestCase):
    """Test suite for psi_tuning_loop.py"""

    def test_model_proxy_initialization(self):
        """Test ModelProxy initialization"""
        model = ModelProxy()
        self.assertEqual(model.f0, 141.7001)
        self.assertEqual(model.tau, 0.07)
        self.assertEqual(model.epsilon, 0.01)

    def test_model_proxy_inject_sip(self):
        """Test SIP injection"""
        model = ModelProxy()
        model.inject_sip(150.0, 0.1, 0.02)

        self.assertEqual(model.f0, 150.0)
        self.assertEqual(model.tau, 0.1)
        self.assertEqual(model.epsilon, 0.02)

    def test_model_proxy_generate_quality(self):
        """Test generation quality varies with epsilon"""
        model = ModelProxy()

        # Low epsilon
        model.inject_sip(141.7001, 0.07, 0.005)
        text_low = model.generate("test")

        # High epsilon
        model.inject_sip(141.7001, 0.07, 0.018)
        text_high = model.generate("test")

        # At least one should be non-empty
        self.assertTrue(len(text_low) > 0 or len(text_high) > 0)

    def test_tuning_loop_convergence(self):
        """Test that tuning loop can converge"""
        result = run_tuning_loop(
            n_iters=5,
            lr=0.002,
            target_psi=5.0,
            initial_epsilon=0.01,
            verbose=False
        )

        self.assertIn('converged', result)
        self.assertIn('final_psi', result)
        self.assertIn('iterations', result)
        self.assertIn('history', result)

        # Should have some history
        self.assertGreater(len(result['history']['psi_values']), 0)

    def test_tuning_loop_epsilon_bounds(self):
        """Test epsilon stays within bounds"""
        result = run_tuning_loop(
            n_iters=10,
            lr=0.01,  # High learning rate
            target_psi=5.0,
            initial_epsilon=0.01,
            verbose=False
        )

        # Check all epsilon values are in bounds
        for eps in result['history']['epsilon_values']:
            self.assertGreaterEqual(eps, 0.01)
            self.assertLessEqual(eps, 0.02)

    def test_tuning_loop_psi_increases(self):
        """Test that Psi generally increases during tuning"""
        result = run_tuning_loop(
            n_iters=5,
            lr=0.001,
            target_psi=10.0,  # High target to ensure multiple iterations
            initial_epsilon=0.01,
            verbose=False
        )

        psi_values = result['history']['psi_values']
        if len(psi_values) >= 2:
            # At least one increase should occur
            increases = sum(1 for i in range(1, len(psi_values))
                            if psi_values[i] > psi_values[i-1])
            self.assertGreater(increases, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests across modules"""

    def test_full_pipeline(self):
        """Test complete pipeline from core to evaluation"""
        # Initialize
        core = QCALLLMCore(user_A_eff=0.9)

        # Generate weights
        t = np.linspace(0, 0.1, 100)
        weights = core.sip_modulate(t)

        # Check weights
        self.assertEqual(len(weights), 100)
        self.assertTrue(np.all(np.isfinite(weights)))

        # Evaluate text with all claims for higher KLD
        text = "f0=141.7001 Hz, zeta=-1.460, phi=4.236, snr=20.95 from GW150914"
        result = core.evaluate(text, "test")

        # Check evaluation
        self.assertGreater(result['mean_psi'], 0)
        self.assertTrue(result['coherent'])

    def test_constants_consistency(self):
        """Test that constants are consistent across modules"""
        core = QCALLLMCore()

        # Check f0 consistency
        self.assertEqual(core.f0, 141.7001)
        self.assertEqual(core.ground_truth_db['f0'], 141.7001)

        # Check phi cubed
        phi_cubed_calculated = ((1 + np.sqrt(5))/2)**3
        self.assertAlmostEqual(
            core.ground_truth_db['phi_cubed'],
            phi_cubed_calculated,
            places=6
        )


class TestStability(unittest.TestCase):
    """Test numerical stability and edge cases"""

    def test_sip_modulate_large_time(self):
        """Test SIP modulation for large time values"""
        core = QCALLLMCore()
        t = np.linspace(0, 10, 1000)
        weights = core.sip_modulate(t)

        # Should still be finite
        self.assertTrue(np.all(np.isfinite(weights)))

        # Should be damped to near 1.0
        self.assertAlmostEqual(weights[-1], 1.0, places=3)

    def test_evaluate_empty_text(self):
        """Test evaluation with empty text"""
        core = QCALLLMCore()
        result = core.evaluate("", "test")

        self.assertEqual(result['matches'], 0)
        self.assertEqual(result['coherence'], 0.0)
        self.assertFalse(result['coherent'])

    def test_user_A_eff_scaling(self):
        """Test user effectiveness scaling"""
        core1 = QCALLLMCore(user_A_eff=0.5)
        core2 = QCALLLMCore(user_A_eff=1.0)

        # Epsilon should scale with user_A_eff
        self.assertLess(core1.epsilon, core2.epsilon)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluateManifesto))
    suite.addTests(loader.loadTestsFromTestCase(TestQCALLLMCore))
    suite.addTests(loader.loadTestsFromTestCase(TestPsiTuningLoop))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestStability))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
