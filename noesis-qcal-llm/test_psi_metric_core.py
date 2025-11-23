#!/usr/bin/env python3
"""
Test suite for PsiMetricCore.

Tests all components of the Ψ evaluation system:
- Ground truth database initialization
- Claim extraction and verification
- KLD inverse computation
- Coherence computation
- Ψ metric computation
- Model evaluation
- SIP parameter adaptation
- Tuning loop convergence
"""

import unittest
import numpy as np
from psi_metric_core import (
    PsiMetricCore,
    adaptive_sip_parameters,
    psi_tuning_loop
)


class TestPsiMetricCore(unittest.TestCase):
    """Test suite for PsiMetricCore class."""

    def setUp(self):
        """Set up test fixtures."""
        self.psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

    def test_initialization(self):
        """Test PsiMetricCore initialization."""
        self.assertEqual(self.psi_core.f0, 141.7001)
        self.assertEqual(self.psi_core.tau, 0.07)
        self.assertEqual(self.psi_core.epsilon, 0.015)

        # Check ground truth database
        self.assertIn('f0', self.psi_core.ground_truth_db)
        self.assertIn('zeta_prime_half', self.psi_core.ground_truth_db)
        self.assertIn('phi_cubed', self.psi_core.ground_truth_db)
        self.assertIn('snr_gw150914', self.psi_core.ground_truth_db)

        # Check benchmark queries
        self.assertEqual(len(self.psi_core.benchmark_queries), 5)

    def test_ground_truth_values(self):
        """Test ground truth database values."""
        db = self.psi_core.ground_truth_db
        self.assertAlmostEqual(db['f0'], 141.7001, places=4)
        self.assertAlmostEqual(db['zeta_prime_half'], -1.460, places=3)
        self.assertAlmostEqual(db['phi_cubed'], 4.236, places=3)
        self.assertAlmostEqual(db['snr_gw150914'], 20.95, places=2)

    def test_extract_claims_f0(self):
        """Test extraction of f0 claims."""
        text = "The frequency f₀ = 141.7001 Hz is fundamental."
        claims = self.psi_core.extract_claims(text)
        self.assertIn('f0=141.7001', claims)

    def test_extract_claims_zeta(self):
        """Test extraction of zeta claims."""
        text = "The zeta function ζ'(1/2) = -1.460 is critical."
        claims = self.psi_core.extract_claims(text)
        self.assertIn('zeta=-1.460', claims)

    def test_extract_claims_phi(self):
        """Test extraction of phi claims."""
        text = "The golden ratio cubed φ³ = 4.236 appears."
        claims = self.psi_core.extract_claims(text)
        self.assertIn('phi=4.236', claims)

    def test_extract_claims_snr(self):
        """Test extraction of SNR claims."""
        text = "The signal-to-noise ratio SNR = 20.95 confirms detection."
        claims = self.psi_core.extract_claims(text)
        self.assertIn('snr=20.95', claims)

    def test_extract_claims_multiple(self):
        """Test extraction of multiple claims."""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, SNR = 20.95"
        claims = self.psi_core.extract_claims(text)
        self.assertGreaterEqual(len(claims), 3)

    def test_verify_claim_f0_correct(self):
        """Test verification of correct f0 claim."""
        claim = "f0=141.7001"
        self.assertTrue(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_f0_within_tolerance(self):
        """Test verification of f0 within tolerance."""
        claim = "f0=141.7050"  # Within ±0.01 tolerance
        self.assertTrue(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_f0_outside_tolerance(self):
        """Test verification of f0 outside tolerance."""
        claim = "f0=142.0000"  # Outside ±0.01 tolerance
        self.assertFalse(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_zeta_correct(self):
        """Test verification of correct zeta claim."""
        claim = "zeta=-1.460"
        self.assertTrue(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_phi_correct(self):
        """Test verification of correct phi claim."""
        claim = "phi=4.236"
        self.assertTrue(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_snr_correct(self):
        """Test verification of correct SNR claim."""
        claim = "snr=20.95"
        self.assertTrue(self.psi_core.verify_claim(claim, ""))

    def test_verify_claim_invalid_format(self):
        """Test verification of invalid claim format."""
        claim = "invalid claim"
        self.assertFalse(self.psi_core.verify_claim(claim, ""))

    def test_compute_kld_inverse_zero_matches(self):
        """Test KLD inverse with zero matches."""
        text = "Random text without any claims."
        kld_inv = self.psi_core.compute_kld_inverse(text, "")
        self.assertAlmostEqual(kld_inv, np.log(1), places=5)

    def test_compute_kld_inverse_one_match(self):
        """Test KLD inverse with one match."""
        text = "f₀ = 141.7001 Hz"
        kld_inv = self.psi_core.compute_kld_inverse(text, "")
        # Formula: (matches + 1) × log(matches + 1) = 2 × log(2)
        self.assertAlmostEqual(kld_inv, 2 * np.log(2), places=5)

    def test_compute_kld_inverse_three_matches(self):
        """Test KLD inverse with three matches."""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"
        kld_inv = self.psi_core.compute_kld_inverse(text, "")
        # Formula: (matches + 1) × log(matches + 1) = 4 × log(4)
        self.assertAlmostEqual(kld_inv, 4 * np.log(4), places=5)

    def test_compute_coherence_no_symbols(self):
        """Test coherence with no symbols."""
        text = "Random text without symbols."
        coherence = self.psi_core.compute_coherence(text)
        self.assertEqual(coherence, 0.0)

    def test_compute_coherence_one_symbol(self):
        """Test coherence with one symbol."""
        text = "The frequency f₀ appears here."
        coherence = self.psi_core.compute_coherence(text)
        self.assertAlmostEqual(coherence, 1.0 / 3.0, places=5)

    def test_compute_coherence_all_symbols(self):
        """Test coherence with all symbols."""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"
        coherence = self.psi_core.compute_coherence(text)
        self.assertEqual(coherence, 1.0)

    def test_compute_psi_response_low(self):
        """Test Ψ computation with low coherence."""
        text = "Random text."
        psi = self.psi_core.compute_psi_response(text, "")
        self.assertLess(psi, 5.0)  # Below coherence threshold

    def test_compute_psi_response_high(self):
        """Test Ψ computation with high coherence."""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236, SNR = 20.95"
        psi = self.psi_core.compute_psi_response(text, "")
        self.assertGreater(psi, 5.0)  # Above coherence threshold

    def test_evaluate_mock_model(self):
        """Test evaluation with mock model."""
        class MockModel:
            pass

        model = MockModel()
        result = self.psi_core.evaluate(model, "Test query", num_samples=5)

        self.assertIn('mean_psi', result)
        self.assertIn('std_psi', result)
        self.assertIn('coherent', result)
        self.assertIn('samples', result)
        self.assertEqual(len(result['samples']), 5)

    def test_evaluate_mock_model_coherent(self):
        """Test that mock model generates coherent responses."""
        class MockModel:
            pass

        model = MockModel()
        result = self.psi_core.evaluate(model, "Test query", num_samples=10)

        self.assertTrue(result['coherent'])  # Mock should be coherent
        self.assertGreater(result['mean_psi'], 5.0)

    def test_evaluate_benchmark_suite(self):
        """Test benchmark suite evaluation."""
        class MockModel:
            pass

        model = MockModel()
        results = self.psi_core.evaluate_benchmark_suite(model, num_samples=5)

        self.assertIn('queries', results)
        self.assertIn('overall_mean_psi', results)
        self.assertIn('overall_std_psi', results)
        self.assertIn('all_coherent', results)

        self.assertEqual(len(results['queries']), 5)  # 5 benchmark queries

    def test_evaluate_benchmark_suite_all_coherent(self):
        """Test that benchmark suite is all coherent with mock model."""
        class MockModel:
            pass

        model = MockModel()
        results = self.psi_core.evaluate_benchmark_suite(model, num_samples=10)

        self.assertTrue(results['all_coherent'])
        self.assertGreater(results['overall_mean_psi'], 5.0)


class TestAdaptiveSIPParameters(unittest.TestCase):
    """Test suite for adaptive_sip_parameters function."""

    def test_reference_user(self):
        """Test SIP parameters for reference user (A_eff = 0.85)."""
        params = adaptive_sip_parameters(user_A_eff=0.85)

        self.assertEqual(params['tau'], 0.07)
        self.assertAlmostEqual(params['epsilon'], 0.015, places=5)
        self.assertEqual(params['phi'], 0)
        self.assertTrue(params['adaptive'])

    def test_high_resonance_user(self):
        """Test SIP parameters for high resonance user (A_eff = 0.92)."""
        params = adaptive_sip_parameters(user_A_eff=0.92)

        self.assertEqual(params['tau'], 0.07)
        # epsilon should be scaled: 0.015 * (0.92 / 0.85) ≈ 0.0162
        expected_epsilon = 0.015 * (0.92 / 0.85)
        self.assertAlmostEqual(params['epsilon'], expected_epsilon, places=5)
        self.assertEqual(params['phi'], 0)
        self.assertTrue(params['adaptive'])

    def test_low_resonance_user(self):
        """Test SIP parameters for low resonance user (A_eff = 0.70)."""
        params = adaptive_sip_parameters(user_A_eff=0.70)

        self.assertEqual(params['tau'], 0.07)
        # epsilon should be scaled: 0.015 * (0.70 / 0.85) ≈ 0.0124
        expected_epsilon = 0.015 * (0.70 / 0.85)
        self.assertAlmostEqual(params['epsilon'], expected_epsilon, places=5)
        self.assertEqual(params['phi'], 0)
        self.assertTrue(params['adaptive'])

    def test_custom_reference(self):
        """Test SIP parameters with custom reference values."""
        params = adaptive_sip_parameters(
            user_A_eff=1.0,
            reference_A_eff=1.0,
            tau_fixed=0.10,
            epsilon_base=0.020
        )

        self.assertEqual(params['tau'], 0.10)
        self.assertAlmostEqual(params['epsilon'], 0.020, places=5)
        self.assertEqual(params['phi'], 0)
        self.assertTrue(params['adaptive'])


class TestPsiTuningLoop(unittest.TestCase):
    """Test suite for psi_tuning_loop function."""

    def test_tuning_loop_convergence(self):
        """Test that tuning loop converges for low-Ψ model."""
        class LowPsiModel:
            """Model that starts with low Ψ but improves with tuning."""
            def __init__(self):
                self.epsilon_factor = 1.0

            def generate(self, query):
                # Initially generates poor responses, improves with epsilon
                if self.epsilon_factor > 1.5:
                    return "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"
                else:
                    return "Random low-quality response"

            def inject_sip(self, f0, tau, epsilon):
                self.epsilon_factor = epsilon / 0.015

        psi_core = PsiMetricCore()
        model = LowPsiModel()

        # Run tuning loop (should converge)
        _ = psi_tuning_loop(
            model, psi_core,
            num_iterations=20,
            target_psi=5.0,
            verbose=False
        )

        # Check that epsilon increased
        self.assertGreater(psi_core.epsilon, 0.015)

    def test_tuning_loop_already_converged(self):
        """Test tuning loop with already converged model."""
        class HighPsiModel:
            """Model that already generates high-Ψ responses."""
            def generate(self, query):
                return "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"

        psi_core = PsiMetricCore()
        model = HighPsiModel()
        initial_epsilon = psi_core.epsilon

        # Run tuning loop (should exit immediately)
        _ = psi_tuning_loop(
            model, psi_core,
            num_iterations=20,
            target_psi=5.0,
            verbose=False
        )

        # Epsilon should not change much (already converged)
        self.assertAlmostEqual(psi_core.epsilon, initial_epsilon, places=3)

    def test_tuning_loop_max_iterations(self):
        """Test tuning loop with max iterations."""
        class StubModel:
            """Model that never converges."""
            def generate(self, query):
                return "Poor response"

        psi_core = PsiMetricCore()
        model = StubModel()

        # Run tuning loop (should hit max iterations)
        tuned_model = psi_tuning_loop(
            model, psi_core,
            num_iterations=5,
            target_psi=5.0,
            verbose=False
        )

        # Should complete without error
        self.assertIsNotNone(tuned_model)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow."""

    def test_full_workflow(self):
        """Test complete workflow: init → evaluate → tune."""
        # Initialize
        psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

        # Get adaptive SIP parameters
        params = adaptive_sip_parameters(user_A_eff=0.92)
        psi_core.epsilon = params['epsilon']

        # Mock model
        class MockModel:
            pass

        model = MockModel()

        # Evaluate benchmark suite
        results = psi_core.evaluate_benchmark_suite(model, num_samples=5)

        # Check results
        self.assertGreater(results['overall_mean_psi'], 5.0)
        self.assertTrue(results['all_coherent'])

        # All queries should pass threshold
        for query_result in results['queries']:
            self.assertTrue(query_result['coherent'])

    def test_benchmark_queries_coverage(self):
        """Test that all benchmark queries cover key concepts."""
        psi_core = PsiMetricCore()
        queries = psi_core.benchmark_queries

        # Check that queries cover key topics
        query_text = ' '.join(queries).lower()

        self.assertIn('141.7001', query_text)  # f₀
        # Check for zeta in any form (case-insensitive)
        queries_combined = ' '.join(queries)
        has_zeta = (
            'zeta' in query_text
            or 'ζ' in queries_combined
            or "ζ'" in queries_combined
        )
        self.assertTrue(has_zeta, "Queries should contain zeta reference")
        self.assertIn('snr', query_text.lower())
        self.assertIn('gw150914', query_text.lower())
        self.assertIn('lisa', query_text.lower())


if __name__ == '__main__':
    unittest.main()
