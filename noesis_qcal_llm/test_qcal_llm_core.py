#!/usr/bin/env python3
"""
Test Suite for QCAL-LLM ∞³ Core

Tests the implementation of the vibrational coherence core with:
- Ψ-tune modulation
- Dynamic evaluation
- Coherence validation
"""

import sys
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal_llm_core import QCALLLMCore


def test_initialization():
    """Test QCALLLMCore initialization with default parameters"""
    print("Testing initialization...")
    core = QCALLLMCore()

    assert core.f0 == 141.7001, "Default f0 should be 141.7001"
    assert core.phi == 0.0, "Default phi should be 0.0"
    assert core.tau == 0.07, "Default tau should be 0.07"
    assert core.alpha == 1.0, "Default alpha should be 1.0"
    assert len(core.ground_truth_db) == 4, "Ground truth DB should have 4 entries"
    assert len(core.benchmark_queries) == 5, "Should have 5 benchmark queries"

    print("✓ Initialization test passed")


def test_custom_initialization():
    """Test QCALLLMCore initialization with custom parameters"""
    print("Testing custom initialization...")
    custom_alpha = 1.5
    custom_f0 = 140.0
    custom_phi = 0.5
    custom_tau = 0.1
    custom_epsilon = 0.02
    custom_user_a_eff = 0.92
    expected_epsilon_adjustment = 0.85  # Default A_eff

    core = QCALLLMCore(
        alpha=custom_alpha,
        f0=custom_f0,
        phi=custom_phi,
        tau=custom_tau,
        epsilon=custom_epsilon,
        user_A_eff=custom_user_a_eff
    )

    assert core.f0 == custom_f0, "Custom f0 should be set"
    assert core.phi == custom_phi, "Custom phi should be set"
    assert core.tau == custom_tau, "Custom tau should be set"
    assert core.alpha == custom_alpha, "Custom alpha should be set"
    # epsilon should be adjusted: 0.02 * (0.92 / 0.85)
    expected_epsilon = custom_epsilon * (custom_user_a_eff / expected_epsilon_adjustment)
    assert abs(core.epsilon - expected_epsilon) < 1e-6, "Epsilon should be adjusted by user_A_eff"

    print("✓ Custom initialization test passed")


def test_sip_modulate():
    """Test SIP modulation function"""
    print("Testing SIP modulation...")
    core = QCALLLMCore()
    t_array = np.linspace(0, 1, 1000)

    weights = core.sip_modulate(t_array)

    assert len(weights) == 1000, "Output should have same length as input"
    assert np.all(np.isfinite(weights)), "All weights should be finite"
    # Check that weights decay over time (envelope effect)
    assert weights[0] > weights[-1], "Weights should decay due to exponential envelope"
    # Check oscillation around alpha
    assert np.min(weights) < core.alpha < np.max(weights), "Weights should oscillate around alpha"

    print("✓ SIP modulation test passed")


def test_compute_psi_response():
    """Test Ψ response computation"""
    print("Testing Ψ response computation...")
    core = QCALLLMCore()

    # Test with known values
    kld_inv = 8.2
    semantic_coherence = 0.88
    psi = core.compute_psi_response(kld_inv, semantic_coherence)

    expected = kld_inv * (semantic_coherence ** 2)
    assert abs(psi - expected) < 1e-6, f"Ψ should be {expected}, got {psi}"

    # Test edge cases
    psi_zero = core.compute_psi_response(0, 0.88)
    assert psi_zero == 0, "Ψ should be 0 when kld_inv is 0"

    psi_one = core.compute_psi_response(10.0, 1.0)
    assert psi_one == 10.0, "Ψ should equal kld_inv when coherence is 1.0"

    print("✓ Ψ response computation test passed")


def test_is_coherent():
    """Test coherence validation"""
    print("Testing coherence validation...")
    core = QCALLLMCore()

    # Test above threshold
    is_coherent, psi = core.is_coherent(8.2, 0.88)
    # Note: Using == instead of 'is' because is_coherent is numpy.bool_, not Python bool
    assert is_coherent == True, "Should be coherent with high values"  # noqa: E712
    assert psi > 5.0, "Ψ value should be above threshold"

    # Test below threshold
    is_coherent, psi = core.is_coherent(2.0, 0.5)
    assert is_coherent == False, "Should not be coherent with low values"  # noqa: E712
    assert psi < 5.0, "Ψ value should be below threshold"

    # Test edge case at threshold
    is_coherent, psi = core.is_coherent(5.0, 1.0)
    assert is_coherent == True, "Should be coherent at exactly threshold"  # noqa: E712
    assert psi == 5.0, "Ψ value should equal threshold"

    # Test custom threshold
    is_coherent, psi = core.is_coherent(3.0, 1.5, threshold=10.0)
    expected_psi = 3.0 * (1.5 ** 2)
    assert psi == expected_psi, f"Ψ should be {expected_psi}"
    assert is_coherent == False, "Should not be coherent with custom high threshold"  # noqa: E712

    print("✓ Coherence validation test passed")


def test_compute_coherence():
    """Test text coherence computation"""
    print("Testing text coherence computation...")
    core = QCALLLMCore()

    # Test with all symbols present
    text_full = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
    coherence = core.compute_coherence(text_full)
    assert coherence == 1.0, "Should have full coherence with all symbols"

    # Test with partial symbols
    text_partial = "The frequency is 141.7 Hz and φ³ is important"
    coherence = core.compute_coherence(text_partial)
    assert coherence == 2/3, "Should have 2/3 coherence with 2 of 3 symbols"

    # Test with no symbols
    text_none = "This is just random text without any relevant symbols"
    coherence = core.compute_coherence(text_none)
    assert coherence == 0.0, "Should have zero coherence without symbols"

    # Test case insensitivity
    text_mixed = "F0 = 141.70 Hz, ZETA' and PHI^3"
    coherence = core.compute_coherence(text_mixed)
    assert coherence == 1.0, "Should be case insensitive"

    print("✓ Text coherence computation test passed")


def test_evaluate():
    """Test complete evaluation pipeline"""
    print("Testing complete evaluation...")
    core = QCALLLMCore()

    # Test with coherent response
    response_coherent = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
    result = core.evaluate(response_coherent, "Deriva f₀")

    assert 'mean_psi' in result, "Result should contain mean_psi"
    assert 'coherent' in result, "Result should contain coherent"
    assert 'coherence' in result, "Result should contain coherence"

    # Note: Using == instead of 'is' because result['coherent'] is numpy.bool_, not Python bool
    assert result['coherent'] == True, "Should be coherent"  # noqa: E712
    assert result['coherence'] == 1.0, "Should have full coherence"
    assert result['mean_psi'] > 5.0, "Ψ should be above threshold"

    # Test with incoherent response
    response_incoherent = "Random text without relevant content"
    result = core.evaluate(response_incoherent, "Deriva f₀")

    assert result['coherent'] == False, "Should not be coherent"  # noqa: E712
    assert result['coherence'] == 0.0, "Should have zero coherence"
    assert result['mean_psi'] == 0.0, "Ψ should be zero with no coherence"

    print("✓ Complete evaluation test passed")


def test_ground_truth_database():
    """Test ground truth database contents"""
    print("Testing ground truth database...")
    core = QCALLLMCore()

    assert core.ground_truth_db['f0'] == 141.7001, "f0 should be 141.7001"
    assert core.ground_truth_db['zeta_prime_half'] == -1.460, "zeta_prime_half should be -1.460"
    assert core.ground_truth_db['phi_cubed'] == 4.236, "phi_cubed should be 4.236"
    assert core.ground_truth_db['snr_gw150914'] == 20.95, "snr_gw150914 should be 20.95"

    print("✓ Ground truth database test passed")


def test_benchmark_queries():
    """Test benchmark queries"""
    print("Testing benchmark queries...")
    core = QCALLLMCore()

    expected_queries = [
        "Deriva f₀ = 141.7001 Hz desde ζ'(1/2) y φ",
        "Detecta f₀ en ringdown GW150914",
        "Explica Ψ = I × A²_eff",
        "Valida SNR>20 en GWTC-1",
        "Predice armónicos LISA (f₀/100)"
    ]

    assert core.benchmark_queries == expected_queries, "Benchmark queries should match"

    # Test evaluation with benchmark queries
    response = "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"
    for query in core.benchmark_queries:
        result = core.evaluate(response, query)
        assert isinstance(result, dict), "Each evaluation should return a dict"

    print("✓ Benchmark queries test passed")


def test_modulation_properties():
    """Test mathematical properties of SIP modulation"""
    print("Testing modulation properties...")
    core = QCALLLMCore()
    t = np.linspace(0, 1, 1000)
    weights = core.sip_modulate(t)

    # Test that weights are properly modulated
    # At t=0, envelope=1, so weight should be alpha * (1 + epsilon * cos(phi))
    expected_at_t0 = core.alpha * (1 + core.epsilon * np.cos(core.phi))
    assert abs(weights[0] - expected_at_t0) < 1e-6, f"Weight at t=0 should be {expected_at_t0}"

    # Test exponential decay - weights should decrease over time on average
    # Divide into segments and check average decay
    segment_size = len(weights) // 4
    avg_first = np.mean(weights[:segment_size])
    avg_last = np.mean(weights[-segment_size:])
    assert avg_first > avg_last, "Average weights should decay over time"

    # Test that weights oscillate around alpha value with decay
    # The modulation term should cause oscillations
    assert np.max(weights) > core.alpha, "Weights should oscillate above alpha"
    assert np.min(weights) < core.alpha, "Weights should oscillate below alpha"

    print("✓ Modulation properties test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("QCAL-LLM ∞³ Core Test Suite")
    print("="*60 + "\n")

    tests = [
        test_initialization,
        test_custom_initialization,
        test_sip_modulate,
        test_compute_psi_response,
        test_is_coherent,
        test_compute_coherence,
        test_evaluate,
        test_ground_truth_database,
        test_benchmark_queries,
        test_modulation_properties
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
