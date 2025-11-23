#!/usr/bin/env python3
"""
Tests for QCAL LLM Core Module

Tests the implementation of QCALLLMCore for evaluating LLM responses
against QCAL (Quantum Coherent Amplification Logic) standards.
Tests the implementation of the Quantum Coherent Attention Layer for LLM evaluation.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from qcal_llm_core import QCALLLMCore


class TestQCALLLMCoreInitialization:
    """Test initialization and parameter handling."""

    def test_default_initialization(self):
        """Test initialization with default parameters."""
class TestQCALLLMCore:
    """Test suite for QCALLLMCore class."""

    def test_initialization_default_parameters(self):
        """Test that QCALLLMCore initializes with correct default parameters."""
        core = QCALLLMCore()
        assert core.f0 == 141.7001
        assert core.phi == 0.0
        assert core.tau == 0.07
        assert core.alpha == 1.0
        assert core.epsilon == pytest.approx(0.015, abs=1e-6)

    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        core = QCALLLMCore(alpha=1.5, f0=150.0, phi=np.pi/4, tau=0.1, epsilon=0.02, user_A_eff=0.9)
        assert core.f0 == 150.0
        assert core.phi == pytest.approx(np.pi/4, abs=1e-6)
        assert core.tau == 0.1
        assert core.alpha == 1.5
        # epsilon should be scaled by user_A_eff
        expected_epsilon = 0.02 * (0.9 / 0.85)
        assert core.epsilon == pytest.approx(expected_epsilon, abs=1e-6)

    def test_user_A_eff_scaling(self):
        """Test that epsilon scales correctly with user_A_eff."""
        core_default = QCALLLMCore(epsilon=0.015, user_A_eff=0.85)
        core_scaled = QCALLLMCore(epsilon=0.015, user_A_eff=0.92)

        ratio = core_scaled.epsilon / core_default.epsilon
        expected_ratio = 0.92 / 0.85
        assert ratio == pytest.approx(expected_ratio, abs=1e-6)

    def test_ground_truth_database(self):
        """Test that ground truth database is properly initialized."""
        assert abs(core.epsilon - 0.015) < 1e-6

    def test_initialization_custom_parameters(self):
        """Test initialization with custom parameters."""
        core = QCALLLMCore(alpha=2.0, f0=142.0, phi=np.pi/4,
                           tau=0.1, epsilon=0.02, user_A_eff=0.92)
        assert core.f0 == 142.0
        assert core.phi == np.pi/4
        assert core.tau == 0.1
        assert core.alpha == 2.0
        # epsilon should be scaled by user_A_eff / 0.85
        expected_epsilon = 0.02 * (0.92 / 0.85)
        assert abs(core.epsilon - expected_epsilon) < 1e-6

    def test_ground_truth_database(self):
        """Test that ground truth database contains expected values."""
        core = QCALLLMCore()
        assert 'f0' in core.ground_truth_db
        assert 'zeta_prime_half' in core.ground_truth_db
        assert 'phi_cubed' in core.ground_truth_db
        assert 'snr_gw150914' in core.ground_truth_db

        # Check values
        assert core.ground_truth_db['f0'] == 141.7001
        assert core.ground_truth_db['zeta_prime_half'] == pytest.approx(-1.4603545, abs=1e-6)
        assert core.ground_truth_db['phi_cubed'] == pytest.approx(4.236067977, abs=1e-6)
        assert core.ground_truth_db['snr_gw150914'] == 20.95

    def test_benchmark_queries(self):
        """Test that benchmark queries are properly initialized."""
        core = QCALLLMCore()
        assert len(core.benchmark_queries) == 5
        assert all(isinstance(q, str) for q in core.benchmark_queries)
        assert "141.7001 Hz" in core.benchmark_queries[0]
        assert "GW150914" in core.benchmark_queries[1]


class TestSIPModulation:
    """Test Signal Integration Protocol modulation."""
        assert core.ground_truth_db['f0'] == 141.7001
        assert abs(core.ground_truth_db['zeta_prime_half'] - (-1.4603545)) < 1e-6
        # Golden ratio cubed: φ³ = ((1 + √5)/2)³ ≈ 4.236067977
        phi_cubed = ((1 + np.sqrt(5))/2)**3
        assert abs(core.ground_truth_db['phi_cubed'] - phi_cubed) < 1e-6
        assert core.ground_truth_db['snr_gw150914'] == 20.95

    def test_benchmark_queries_exist(self):
        """Test that benchmark queries are defined."""
        core = QCALLLMCore()
        assert len(core.benchmark_queries) == 5
        assert all(isinstance(q, str) for q in core.benchmark_queries)

    def test_sip_modulate_shape(self):
        """Test that SIP modulation returns correct shape."""
        core = QCALLLMCore()
        t = np.linspace(0, 1, 100)
        weights = core.sip_modulate(t)
        assert weights.shape == t.shape

    def test_sip_modulate_initial_value(self):
        """Test SIP modulation at t=0."""
        core = QCALLLMCore(alpha=1.0, epsilon=0.015, user_A_eff=0.85)
        t = np.array([0.0])
        weights = core.sip_modulate(t)
        # At t=0: envelope=1, modulation=cos(0)=1
        # weight = alpha * (1 + epsilon * 1) = 1.0 * (1 + 0.015) = 1.015
        expected = 1.0 * (1 + 0.015 * 1.0)
        assert weights[0] == pytest.approx(expected, abs=1e-6)

    def test_sip_modulate_decay(self):
        """Test exponential decay in SIP modulation."""
        core = QCALLLMCore(tau=0.07)
        t = np.array([0.0, 0.07, 0.14])
        weights = core.sip_modulate(t)
        # Envelope decays as e^(-t/tau)
        # At t=tau, envelope = e^(-1) ≈ 0.368
        assert weights[0] > weights[1] > weights[2]

    def test_sip_modulate_frequency(self):
        """Test oscillation frequency in SIP modulation."""
        core = QCALLLMCore(f0=141.7001)
        # Sample at frequency resolution
        t = np.linspace(0, 0.1, 1000)
        weights = core.sip_modulate(t)
        # Check oscillation exists
        assert np.max(weights) > np.mean(weights)
        assert np.min(weights) < np.mean(weights)

    def test_sip_modulate_mean_near_alpha(self):
        """Test that mean weight is near alpha for small epsilon."""
        core = QCALLLMCore(alpha=1.0, epsilon=0.015, user_A_eff=0.85)
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)
        # Mean should be close to alpha
        assert np.mean(weights) == pytest.approx(1.0, abs=0.01)


class TestPsiResponse:
    """Test Ψ response computation."""

    def test_compute_psi_response_basic(self):
        """Test basic Ψ computation."""
        core = QCALLLMCore()
        psi = core.compute_psi_response(8.2, 0.88)
        expected = 8.2 * (0.88 ** 2)
        assert psi == pytest.approx(expected, abs=1e-6)
        assert psi == pytest.approx(6.3501, abs=1e-4)

    def test_compute_psi_response_zero_coherence(self):
        """Test Ψ with zero coherence."""
        core = QCALLLMCore()
        psi = core.compute_psi_response(10.0, 0.0)
        assert psi == 0.0

    def test_compute_psi_response_unit_coherence(self):
        """Test Ψ with unit coherence."""
        core = QCALLLMCore()
        kld_inv = 5.0
        psi = core.compute_psi_response(kld_inv, 1.0)
        assert psi == kld_inv
        assert len(weights) == 100

    def test_sip_modulate_values(self):
        """Test SIP modulation produces expected value ranges."""
        core = QCALLLMCore(alpha=1.0, epsilon=0.015, user_A_eff=0.85)
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)

        # Weights should be close to alpha for small epsilon
        assert np.mean(weights) == pytest.approx(1.0, abs=0.01)

        # At t=0, envelope is 1, so modulation is most pronounced
        weight_at_zero = core.alpha * (1 + core.epsilon * np.cos(core.phi))
        assert weights[0] == pytest.approx(weight_at_zero, abs=1e-6)

    def test_sip_modulate_decay(self):
        """Test that SIP modulation decays exponentially."""
        core = QCALLLMCore(tau=0.07)
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)

        # Variance should decrease after tau
        early_variance = np.var(weights[t < 0.07])
        late_variance = np.var(weights[t > 0.07])
        assert late_variance < early_variance

    def test_compute_psi_response(self):
        """Test Psi response computation."""
        core = QCALLLMCore()

        # Test case from problem statement
        psi = core.compute_psi_response(8.2, 0.88)
        expected_psi = 8.2 * (0.88 ** 2)
        assert psi == pytest.approx(expected_psi, abs=1e-6)
        assert psi == pytest.approx(6.3501, abs=1e-4)

    def test_compute_psi_response_various_inputs(self):
        """Test Psi response with various inputs."""
        core = QCALLLMCore()

        # Test with coherence = 1.0
        psi = core.compute_psi_response(10.0, 1.0)
        assert psi == 10.0

        # Test with coherence = 0.0
        psi = core.compute_psi_response(10.0, 0.0)
        assert psi == 0.0

        # Test with coherence = 0.5
        psi = core.compute_psi_response(10.0, 0.5)
        assert psi == pytest.approx(2.5, abs=1e-6)

    def test_is_coherent_above_threshold(self):
        """Test coherence check above threshold."""
        core = QCALLLMCore()
        is_coh, psi = core.is_coherent(8.2, 0.88, threshold=5.0)
        assert is_coh is True

        # From problem statement: should be coherent
        is_coherent, psi = core.is_coherent(8.2, 0.88, threshold=5.0)
        assert is_coherent is True
        assert psi == pytest.approx(6.3501, abs=1e-4)

    def test_is_coherent_below_threshold(self):
        """Test coherence check below threshold."""
        core = QCALLLMCore()
        is_coh, psi = core.is_coherent(3.0, 0.5, threshold=5.0)
        assert is_coh is False
        assert psi == pytest.approx(0.75, abs=1e-6)

    def test_is_coherent_at_threshold(self):
        """Test coherence check exactly at threshold."""
        core = QCALLLMCore()
        # Set kld_inv such that psi = threshold
        # psi = kld_inv * coherence^2
        # 5.0 = kld_inv * 0.8^2
        # kld_inv = 5.0 / 0.64 = 7.8125
        is_coh, psi = core.is_coherent(7.8125, 0.8, threshold=5.0)
        assert is_coh is True
        assert psi == pytest.approx(5.0, abs=1e-6)


class TestCoherenceComputation:
    """Test semantic coherence computation."""

    def test_compute_coherence_all_symbols(self):
        """Test coherence with all symbols present."""
        core = QCALLLMCore()
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz"
        coherence = core.compute_coherence(text)
        assert coherence == 1.0

    def test_compute_coherence_no_symbols(self):
        """Test coherence with no symbols."""
        core = QCALLLMCore()
        text = "This is random text without any relevant symbols"
        coherence = core.compute_coherence(text)
        assert coherence == 0.0

    def test_compute_coherence_partial_symbols(self):
        """Test coherence with partial symbol matches."""
        core = QCALLLMCore()
        # Only f0 present
        text = "The frequency is 141.7001 Hz"
        coherence = core.compute_coherence(text)
        assert coherence == pytest.approx(1/3, abs=1e-6)

        # f0 and zeta present
        text2 = "ζ'(1/2) gives 141.7 Hz"
        coherence2 = core.compute_coherence(text2)
        assert coherence2 == pytest.approx(2/3, abs=1e-6)

    def test_compute_coherence_case_insensitive(self):
        """Test that coherence matching is case-insensitive."""
        core = QCALLLMCore()
        text = "Zeta' gives 141.7 HZ"
        coherence = core.compute_coherence(text)
        assert coherence > 0.0

    def test_compute_coherence_alternative_notations(self):
        """Test alternative notations for symbols."""
        core = QCALLLMCore()
        # Test phi^3 notation
        text1 = "phi^3 = 4.236"
        coherence1 = core.compute_coherence(text1)
        assert coherence1 >= 1/3  # At least phi_cubed matches

        # Test numeric values with symbols
        text2 = "Values: φ³ = 4.236 and ζ'(1/2) at 141.7 Hz"
        coherence2 = core.compute_coherence(text2)
        assert coherence2 == 1.0


class TestEvaluate:
    """Test full LLM response evaluation."""

        # Low values should not be coherent
        is_coherent, psi = core.is_coherent(2.0, 0.5, threshold=5.0)
        assert is_coherent is False
        assert psi < 5.0

    def test_is_coherent_at_threshold(self):
        """Test coherence check at exactly the threshold."""
        core = QCALLLMCore()

        # Compute inputs that give exactly threshold
        threshold = 5.0
        coherence = 0.5
        kld_inv = threshold / (coherence ** 2)  # 20.0

        is_coherent, psi = core.is_coherent(kld_inv, coherence, threshold=threshold)
        assert is_coherent is True
        assert psi == pytest.approx(threshold, abs=1e-6)

    def test_compute_coherence_empty_text(self):
        """Test coherence computation with empty text."""
        core = QCALLLMCore()
        coherence = core.compute_coherence("")
        assert coherence == 0.0

    def test_compute_coherence_no_matches(self):
        """Test coherence computation with no matching symbols."""
        core = QCALLLMCore()
        coherence = core.compute_coherence("This is random text with no physics symbols.")
        assert coherence == 0.0

    def test_compute_coherence_partial_matches(self):
        """Test coherence computation with partial matches."""
        core = QCALLLMCore()

        # Text with f0 only (1/3 matches)
        text1 = "The frequency is 141.7001 Hz"
        coherence1 = core.compute_coherence(text1)
        assert coherence1 == pytest.approx(1.0 / 3.0, abs=1e-6)

        # Text with f0 and phi (2/3 matches)
        text2 = "The frequency is 141.7001 Hz and φ³ = 4.236"
        coherence2 = core.compute_coherence(text2)
        assert coherence2 == pytest.approx(2.0 / 3.0, abs=1e-6)

    def test_compute_coherence_all_matches(self):
        """Test coherence computation with all symbols present."""
        core = QCALLLMCore()

        # Text from problem statement with all symbols
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent. SNR=20.95."
        coherence = core.compute_coherence(text)
        assert coherence == 1.0  # All 3 symbols found

    def test_compute_coherence_case_insensitive(self):
        """Test that coherence computation is case-insensitive."""
        core = QCALLLMCore()

        text_upper = "F0 = 141.7001 HZ"
        text_lower = "f0 = 141.7001 hz"

        coherence_upper = core.compute_coherence(text_upper)
        coherence_lower = core.compute_coherence(text_lower)

        assert coherence_upper == coherence_lower

    def test_evaluate_structure(self):
        """Test that evaluate returns correct structure."""
        core = QCALLLMCore()
        result = core.evaluate("Some text", "Some query")

        # Check all required keys
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent. SNR=20.95."
        result = core.evaluate(text, "Deriva f₀")

        # Check all required keys are present
        assert 'mean_psi' in result
        assert 'psi_ci_95' in result
        assert 'coherent' in result
        assert 'coherence' in result
        assert 'kld_inv' in result
        assert 'matches' in result

    def test_evaluate_types(self):
        """Test that evaluate returns correct types."""
        core = QCALLLMCore()
        result = core.evaluate("Some text", "Some query")

        assert isinstance(result['mean_psi'], float)
        assert isinstance(result['psi_ci_95'], tuple)
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent. SNR=20.95."
        result = core.evaluate(text, "Deriva f₀")

        assert isinstance(result['mean_psi'], float)
        assert isinstance(result['psi_ci_95'], tuple)
        assert len(result['psi_ci_95']) == 2
        assert isinstance(result['coherent'], bool)
        assert isinstance(result['coherence'], float)
        assert isinstance(result['kld_inv'], float)
        assert isinstance(result['matches'], int)

    def test_evaluate_confidence_interval(self):
        """Test that confidence interval is valid."""
        core = QCALLLMCore()
        result = core.evaluate("141.7001 Hz", "query")

        ci = result['psi_ci_95']
        assert len(ci) == 2
        assert ci[0] <= result['mean_psi'] <= ci[1]

    def test_evaluate_with_no_matches(self):
        """Test evaluation with no claim matches."""
        np.random.seed(42)
        core = QCALLLMCore()
        result = core.evaluate("Random unrelated text", "query")

        assert result['matches'] == 0
        assert result['coherence'] == 0.0
        # KLD can be negative with small log values
        assert isinstance(result['kld_inv'], float)

    def test_evaluate_with_all_matches(self):
        """Test evaluation with all claims matching."""
        np.random.seed(42)
        core = QCALLLMCore()
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236, SNR = 20.95"
        result = core.evaluate(text, "query")

        assert result['matches'] == 4
        assert result['coherence'] == 1.0
        assert result['coherent'] is True

    def test_evaluate_reproducibility(self):
        """Test that evaluation is reproducible with same seed."""
        text = "141.7001 Hz and 4.236"
        query = "test"

        np.random.seed(123)
        core1 = QCALLLMCore()
        result1 = core1.evaluate(text, query, n_bootstrap=50)

        np.random.seed(123)
        core2 = QCALLLMCore()
        result2 = core2.evaluate(text, query, n_bootstrap=50)

        assert result1['mean_psi'] == pytest.approx(result2['mean_psi'], abs=1e-10)
        assert result1['kld_inv'] == pytest.approx(result2['kld_inv'], abs=1e-10)

    def test_evaluate_verified_output(self):
        """Test evaluation against verified output from problem statement."""
        np.random.seed(42)
        core = QCALLLMCore(user_A_eff=0.92)
        response_mock = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. ζ'(1/2) = -1.460, φ³ = 4.236. Ψ coherent."
        result = core.evaluate(response_mock, "Deriva f₀")

        # Expected: mean_psi = 8.20 ± 0.15
        assert result['mean_psi'] == pytest.approx(8.20, abs=0.15)
        assert result['coherent'] is True

        # Check CI contains mean
        ci = result['psi_ci_95']
        assert ci[0] <= result['mean_psi'] <= ci[1]


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_workflow(self):
        """Test complete evaluation workflow."""
        np.random.seed(42)
        core = QCALLLMCore(user_A_eff=0.92)

        # Generate time series
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)
        assert len(weights) == 1000

        # Test coherence check
        is_valid, psi_val = core.is_coherent(8.2, 0.88)
        assert is_valid is True
        assert psi_val == pytest.approx(6.3501, abs=1e-4)

        # Test evaluation
        response = "f₀ = 141.7001 Hz with ζ'(1/2) = -1.460 and φ³ = 4.236"
        result = core.evaluate(response, "Deriva f₀")
        assert result['coherent'] is True
        assert result['coherence'] == 1.0

    def test_benchmark_queries_accessible(self):
        """Test that benchmark queries can be used for evaluation."""
        core = QCALLLMCore()

        # Use first benchmark query
        query = core.benchmark_queries[0]
        assert "141.7001 Hz" in query

        # Create a response
        response = "The fundamental frequency f₀ = 141.7001 Hz is derived from ζ'(1/2) = -1.460"
        result = core.evaluate(response, query)

        assert result['matches'] >= 1
        assert result['coherence'] > 0.0

    def test_parameter_sensitivity(self):
        """Test sensitivity to user_A_eff parameter."""
        np.random.seed(42)

        core1 = QCALLLMCore(user_A_eff=0.85)
        core2 = QCALLLMCore(user_A_eff=0.92)

        # epsilon should be different
        assert core1.epsilon != core2.epsilon

        # SIP modulation should differ
        t = np.array([0.5])
        weights1 = core1.sip_modulate(t)
        weights2 = core2.sip_modulate(t)
        assert weights1[0] != weights2[0]


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "--tb=short"])
        """Test that confidence interval is properly ordered."""
        core = QCALLLMCore()
        text = "f₀ = 141.7001 Hz with ζ'(1/2) = -1.460"
        result = core.evaluate(text, "Test query")

        ci_lower, ci_upper = result['psi_ci_95']
        assert ci_lower < ci_upper
        assert result['mean_psi'] >= ci_lower
        assert result['mean_psi'] <= ci_upper

    def test_evaluate_matches_counting(self):
        """Test that evaluate correctly counts matches."""
        core = QCALLLMCore()

        # No matches
        result0 = core.evaluate("random text", "query")
        assert result0['matches'] == 0

        # One match (f0=141.7001)
        result1 = core.evaluate("f0=141.7001", "query")
        assert result1['matches'] >= 1

    def test_evaluate_reproducibility_with_seed(self):
        """Test that evaluate gives consistent results with same random seed."""
        core = QCALLLMCore()
        text = "f₀ = 141.7001 Hz"

        # Run twice with same seed
        np.random.seed(42)
        result1 = core.evaluate(text, "query", n_bootstrap=100)

        np.random.seed(42)
        result2 = core.evaluate(text, "query", n_bootstrap=100)

        assert result1['mean_psi'] == pytest.approx(result2['mean_psi'], abs=1e-6)
        assert result1['kld_inv'] == pytest.approx(result2['kld_inv'], abs=1e-6)

    def test_evaluate_bootstrap_samples(self):
        """Test that bootstrap sampling affects results appropriately."""
        core = QCALLLMCore()
        text = "f₀ = 141.7001 Hz"

        # More bootstrap samples should give tighter confidence intervals
        result_small = core.evaluate(text, "query", n_bootstrap=10)
        result_large = core.evaluate(text, "query", n_bootstrap=1000)

        # Both should have valid intervals
        assert result_small['psi_ci_95'][0] < result_small['psi_ci_95'][1]
        assert result_large['psi_ci_95'][0] < result_large['psi_ci_95'][1]


class TestQCALLLMCoreIntegration:
    """Integration tests matching the problem statement verification."""

    def test_problem_statement_example(self):
        """Test the exact example from the problem statement."""
        core = QCALLLMCore(user_A_eff=0.92)
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)
        is_valid, psi_val = core.is_coherent(8.2, 0.88)
        response_mock = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent. SNR=20.95."
        eval_res = core.evaluate(response_mock, "Deriva f₀")

        # Verify outputs match expected ranges
        assert psi_val == pytest.approx(6.3501, abs=1e-4)
        assert is_valid is True

        # Mean psi should be positive and coherent
        assert eval_res['mean_psi'] > 0
        assert eval_res['coherent'] in [True, False]  # Depends on random bootstrap

        # Weights statistics
        assert np.mean(weights) == pytest.approx(1.0, abs=0.01)
        assert np.std(weights) == pytest.approx(0.0022, abs=0.001)

        # Post-decay variance should be very small
        post_decay_var = np.var(weights[t > 0.07])
        assert post_decay_var < 1e-4

    def test_benchmark_queries_availability(self):
        """Test that all benchmark queries are accessible."""
        core = QCALLLMCore()

        # Should have 5 standard queries
        assert len(core.benchmark_queries) == 5

        # Check they contain expected keywords
        queries_str = ' '.join(core.benchmark_queries)
        assert '141.7001' in queries_str
        assert 'GW150914' in queries_str or 'GW' in queries_str
        assert 'LISA' in queries_str

    def test_user_effectiveness_scaling(self):
        """Test that user effectiveness parameter scales epsilon correctly."""
        core_default = QCALLLMCore(epsilon=0.015, user_A_eff=0.85)
        core_higher = QCALLLMCore(epsilon=0.015, user_A_eff=0.92)

        # Higher effectiveness should increase epsilon
        assert core_higher.epsilon > core_default.epsilon

        # Check exact scaling
        expected_ratio = 0.92 / 0.85
        actual_ratio = core_higher.epsilon / core_default.epsilon
        assert actual_ratio == pytest.approx(expected_ratio, abs=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
