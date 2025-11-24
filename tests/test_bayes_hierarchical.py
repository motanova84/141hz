#!/usr/bin/env python3
"""
Test suite for Bayesian hierarchical model.

This module tests the hierarchical Bayes factor implementation
used for multi-event gravitational wave analysis.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from bayes.hierarchical_model import loglik_event, logpost, bayes_factor


class TestBayesianHierarchicalModel(unittest.TestCase):
    """Test cases for hierarchical Bayesian analysis functions."""

    def test_loglik_event_basic(self):
        """Test log-likelihood calculation for a single event."""
        snr = 5.0
        pi = 0.5
        mu = 6.0
        sigma = 1.0

        ll0, ll1 = loglik_event(snr, pi, mu, sigma)

        # ll0 should be negative (noise hypothesis)
        self.assertLess(ll0, 0)
        # ll1 should be less negative (closer to expected SNR)
        self.assertLess(ll1, 0)
        # Both should be finite
        self.assertTrue(np.isfinite(ll0))
        self.assertTrue(np.isfinite(ll1))

    def test_loglik_event_high_snr(self):
        """Test that high SNR favors signal hypothesis."""
        snr = 8.0
        pi = 0.5
        mu = 6.0
        sigma = 1.0

        ll0, ll1 = loglik_event(snr, pi, mu, sigma)

        # High SNR should favor signal (ll1 > ll0)
        self.assertGreater(ll1, ll0)

    def test_loglik_event_low_snr(self):
        """Test that low SNR favors noise hypothesis."""
        snr = 1.0
        pi = 0.5
        mu = 6.0
        sigma = 1.0

        ll0, ll1 = loglik_event(snr, pi, mu, sigma)

        # Low SNR should favor noise (ll0 > ll1)
        self.assertGreater(ll0, ll1)

    def test_logpost_consistency(self):
        """Test log-posterior for multiple events."""
        snr_list = [4.0, 5.0, 6.0]
        pi = 0.5

        lp = logpost(snr_list, pi)

        # Log-posterior should be finite
        self.assertTrue(np.isfinite(lp))
        # Should be negative (log of probability < 1)
        self.assertLess(lp, 0)

    def test_logpost_single_vs_multiple(self):
        """Test that logpost is consistent with individual events."""
        snr = 5.0
        pi = 0.5

        # Single event
        lp_single = logpost([snr], pi)

        # Should be close to individual log-likelihood computation
        ll0, ll1 = loglik_event(snr, pi)
        expected = np.logaddexp(ll0, ll1)

        self.assertAlmostEqual(lp_single, expected, places=10)

    def test_bayes_factor_positive(self):
        """Test that Bayes factor is positive."""
        snr_list = [4.0, 5.0, 6.0]

        bf = bayes_factor(snr_list, grid_size=101)

        # Bayes factor should be positive
        self.assertGreater(bf, 0)
        # Should be finite
        self.assertTrue(np.isfinite(bf))

    def test_bayes_factor_high_snr_list(self):
        """Test that high SNR list gives large Bayes factor."""
        snr_list = [6.0, 7.0, 8.0, 6.5, 7.5]

        bf = bayes_factor(snr_list, grid_size=101)

        # High SNR list should give BF >> 1
        self.assertGreater(bf, 100)

    def test_bayes_factor_low_snr_list(self):
        """Test that low SNR list gives small Bayes factor."""
        snr_list = [0.5, 0.8, 1.0, 0.6]

        bf = bayes_factor(snr_list, grid_size=101)

        # Very low SNR list should give BF < 10
        self.assertLess(bf, 10.0)

    def test_bayes_factor_grid_convergence(self):
        """Test that Bayes factor converges with increasing grid size."""
        snr_list = [5.0, 6.0]

        bf_coarse = bayes_factor(snr_list, grid_size=51)
        bf_medium = bayes_factor(snr_list, grid_size=101)
        bf_fine = bayes_factor(snr_list, grid_size=201)

        # Results should be similar (within 10% relative error)
        rel_error_1 = abs(bf_medium - bf_coarse) / bf_coarse
        rel_error_2 = abs(bf_fine - bf_medium) / bf_medium

        self.assertLess(rel_error_1, 0.1)
        self.assertLess(rel_error_2, 0.1)

    def test_analysis_plan_compatibility(self):
        """Test that module can be used with analysis_plan.json parameters."""
        import json

        # Load analysis plan from root directory
        plan_path = Path(__file__).parent.parent / "analysis_plan.json"
        with open(plan_path, 'r') as f:
            plan = json.load(f)

        # Check expected fields exist
        self.assertIn("f0_hz", plan)
        self.assertIn("detectors", plan)
        self.assertIn("multiple_events", plan)
        self.assertEqual(plan["multiple_events"], "hierarchical_bayes")
        self.assertEqual(plan["f0_hz"], 141.7001)

        # Simulate multi-detector SNR measurements
        n_events = 5
        snr_list = [5.0 + np.random.randn() for _ in range(n_events)]

        # Should be able to compute Bayes factor
        bf = bayes_factor(snr_list, grid_size=101)
        self.assertGreater(bf, 0)
        self.assertTrue(np.isfinite(bf))


if __name__ == '__main__':
    unittest.main()
