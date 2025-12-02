"""
Unit tests for QCALLLMCore
"""

import sys
from pathlib import Path

# Add noesis-qcal-llm directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'noesis-qcal-llm'))

import pytest  # noqa: E402
import numpy as np  # noqa: E402

from QCALLLMCore import QCALLLMCore  # noqa: E402


class TestQCALLLMCoreInitialization:
    """Test QCALLLMCore initialization"""

    def test_default_initialization(self):
        """Test default parameters"""
        core = QCALLLMCore()
        assert core.f0 == 141.7001
        assert core.phi == 0.0
        assert core.tau == 0.07
        assert core.alpha == 1.0
        assert core.epsilon == pytest.approx(0.015, rel=1e-6)

    def test_custom_initialization(self):
        """Test custom parameters"""
        core = QCALLLMCore(alpha=2.0, f0=150.0, phi=0.5, tau=0.1, epsilon=0.02, user_A_eff=0.90)
        assert core.f0 == 150.0
        assert core.phi == 0.5
        assert core.tau == 0.1
        assert core.alpha == 2.0
        # epsilon should be scaled by user_A_eff
        expected_epsilon = 0.02 * (0.90 / 0.85)
        assert core.epsilon == pytest.approx(expected_epsilon, rel=1e-6)

    def test_ground_truth_database(self):
        """Test ground truth database is properly initialized"""
        core = QCALLLMCore()
        assert 'f0' in core.ground_truth_db
        assert 'zeta_prime_half' in core.ground_truth_db
        assert 'phi_cubed' in core.ground_truth_db
        assert 'snr_gw150914' in core.ground_truth_db

        assert core.ground_truth_db['f0'] == 141.7001
        assert core.ground_truth_db['zeta_prime_half'] == -1.460
        assert core.ground_truth_db['phi_cubed'] == 4.236
        assert core.ground_truth_db['snr_gw150914'] == 20.95

    def test_benchmark_queries(self):
        """Test benchmark queries are properly initialized"""
        core = QCALLLMCore()
        assert len(core.benchmark_queries) == 5
        assert isinstance(core.benchmark_queries, list)


class TestSIPModulation:
    """Test SIP (Signal Induced Perturbation) modulation"""

    def test_sip_basic(self):
        """Test basic SIP modulation"""
        core = QCALLLMCore()
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)

        assert isinstance(weights, np.ndarray)
        assert len(weights) == len(t)
        assert np.all(np.isfinite(weights))

    def test_sip_mean_near_one(self):
        """Test that SIP weights average near 1.0"""
        core = QCALLLMCore()
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)

        # Should be close to 1.0 with small perturbations
        assert np.mean(weights) == pytest.approx(1.0, abs=0.01)

    def test_sip_small_std(self):
        """Test that SIP weights have small standard deviation"""
        core = QCALLLMCore()
        t = np.linspace(0, 1, 1000)
        weights = core.sip_modulate(t)

        # Should have small std (coherent oscillation)
        assert np.std(weights) < 0.02

    def test_sip_different_epsilon(self):
        """Test SIP with different epsilon values"""
        core1 = QCALLLMCore(epsilon=0.01)
        core2 = QCALLLMCore(epsilon=0.02)

        t = np.linspace(0, 1, 1000)
        weights1 = core1.sip_modulate(t)
        weights2 = core2.sip_modulate(t)

        # Larger epsilon should give larger std
        assert np.std(weights2) > np.std(weights1)


class TestPsiResponse:
    """Test Ψ (Psi) response computation"""

    def test_compute_psi_response(self):
        """Test basic Ψ computation"""
        core = QCALLLMCore()
        psi = core.compute_psi_response(8.2, 0.88)

        # Ψ = 8.2 * 0.88^2
        expected = 8.2 * (0.88 ** 2)
        assert psi == pytest.approx(expected, rel=1e-6)

    def test_is_coherent_above_threshold(self):
        """Test coherence check above threshold"""
        core = QCALLLMCore()
        is_coherent, psi_val = core.is_coherent(8.2, 0.88, threshold=5.0)

        assert is_coherent is True
        assert psi_val > 5.0
        assert psi_val == pytest.approx(6.3501, rel=1e-3)

    def test_is_coherent_below_threshold(self):
        """Test coherence check below threshold"""
        core = QCALLLMCore()
        is_coherent, psi_val = core.is_coherent(2.0, 0.5, threshold=5.0)

        assert is_coherent is False
        assert psi_val < 5.0

    def test_is_coherent_at_threshold(self):
        """Test coherence check at exact threshold"""
        core = QCALLLMCore()
        # Find kld_inv and coherence that give exactly 5.0
        # Ψ = kld_inv * coherence^2 = 5.0
        # If coherence = 1.0, then kld_inv = 5.0
        is_coherent, psi_val = core.is_coherent(5.0, 1.0, threshold=5.0)

        assert is_coherent is True
        assert psi_val == pytest.approx(5.0, rel=1e-6)


class TestSymbolicCoherence:
    """Test symbolic coherence computation"""

    def test_compute_coherence_all_symbols(self):
        """Test coherence with all symbols present"""
        core = QCALLLMCore()
        text = "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"
        coherence = core.compute_coherence(text)

        # Should find all 3 symbols
        assert coherence == pytest.approx(1.0, rel=1e-6)

    def test_compute_coherence_no_symbols(self):
        """Test coherence with no symbols"""
        core = QCALLLMCore()
        text = "This is unrelated text about nothing relevant"
        coherence = core.compute_coherence(text)

        assert coherence == pytest.approx(0.0, rel=1e-6)

    def test_compute_coherence_partial_symbols(self):
        """Test coherence with some symbols"""
        core = QCALLLMCore()
        text = "The frequency is 141.7001 Hz"
        coherence = core.compute_coherence(text)

        # Should find f0 pattern (1/3)
        assert coherence == pytest.approx(1 / 3, rel=1e-6)

    def test_compute_coherence_case_insensitive(self):
        """Test that pattern matching is case insensitive"""
        core = QCALLLMCore()
        text1 = "141.7001 Hz and zeta' and phi^3"
        text2 = "141.7001 hz and ZETA' and PHI^3"

        coherence1 = core.compute_coherence(text1)
        coherence2 = core.compute_coherence(text2)

        # Should be the same
        assert coherence1 == coherence2


class TestEvaluation:
    """Test main evaluation function"""

    def test_evaluate_coherent_text(self):
        """Test evaluation of coherent text"""
        core = QCALLLMCore(user_A_eff=0.92)
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
        result = core.evaluate(text, "Deriva f₀")

        assert 'mean_psi' in result
        assert 'coherent' in result
        assert 'coherence' in result

        assert isinstance(result['mean_psi'], float)
        assert isinstance(result['coherent'], (bool, np.bool_))
        assert isinstance(result['coherence'], float)

        # Should have high coherence
        assert result['coherence'] == pytest.approx(1.0, rel=1e-6)

    def test_evaluate_non_coherent_text(self):
        """Test evaluation of non-coherent text"""
        core = QCALLLMCore()
        text = "This is some random text without relevant content"
        result = core.evaluate(text, "Test query")

        assert result['coherence'] == pytest.approx(0.0, rel=1e-6)
        assert not result['coherent']  # Preferred pytest style for False checks
        assert result['mean_psi'] < 5.0

    def test_evaluate_with_claim_matches(self):
        """Test that claim matching works"""
        core = QCALLLMCore()
        text = "The frequency 141.7001 Hz is important"
        result = core.evaluate(text, "Test")

        # Should match at least one claim pattern
        assert result['mean_psi'] > 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
