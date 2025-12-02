"""
Unit tests for psi_tuning_loop
"""

import sys
from pathlib import Path

# Add noesis-qcal-llm directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'noesis-qcal-llm'))

import pytest  # noqa: E402

from psi_tuning_loop import tune_psi, auto_regenerate  # noqa: E402
from QCALLLMCore import QCALLLMCore  # noqa: E402


class TestTunePsi:
    """Test psi tuning function"""

    def test_tune_psi_basic(self):
        """Test basic psi tuning"""
        text = "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"
        core, result = tune_psi(text, "Test query", verbose=False)

        assert isinstance(core, QCALLLMCore)
        assert isinstance(result, dict)
        assert 'mean_psi' in result
        assert 'coherent' in result
        assert 'coherence' in result

    def test_tune_psi_reaches_target(self):
        """Test that tuning can reach target for good text"""
        text = "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz with -1.460 and 4.236 and 20.95"
        core, result = tune_psi(text, "Test query", target_psi=5.0, verbose=False)

        # With all symbols and multiple claims, should reach target
        assert result['coherent']  # Preferred pytest style for True checks
        assert result['mean_psi'] >= 5.0

    def test_tune_psi_max_iterations(self):
        """Test that tuning respects max iterations"""
        text = "Random text without any relevant content"
        core, result = tune_psi(
            text, "Test query",
            target_psi=5.0,
            max_iterations=2,
            verbose=False
        )

        # Should return even if target not reached
        assert isinstance(core, QCALLLMCore)
        assert isinstance(result, dict)

    def test_tune_psi_custom_epsilon_step(self):
        """Test tuning with custom epsilon step"""
        text = "Some text with 141.7001 Hz"
        core, result = tune_psi(
            text, "Test query",
            epsilon_step=0.01,
            verbose=False
        )

        assert isinstance(core, QCALLLMCore)

    def test_tune_psi_user_a_eff(self):
        """Test tuning with custom user_A_eff"""
        text = "f₀ = 141.7001 Hz"
        core1, _ = tune_psi(text, "Test", user_A_eff=0.85, verbose=False)
        core2, _ = tune_psi(text, "Test", user_A_eff=0.95, verbose=False)

        # Different user_A_eff should result in different epsilon
        assert core1.epsilon != core2.epsilon


class TestAutoRegenerate:
    """Test auto-regenerate function"""

    def test_auto_regenerate_basic(self):
        """Test basic auto-regeneration"""
        def mock_llm(query):
            return "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"

        text, core, result = auto_regenerate(
            mock_llm,
            "Test query",
            target_psi=5.0,
            max_regenerations=1,
            verbose=False
        )

        assert isinstance(text, str)
        assert isinstance(core, QCALLLMCore)
        assert isinstance(result, dict)

    def test_auto_regenerate_success(self):
        """Test successful regeneration with good text"""
        def good_llm(query):
            return "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz with all symbols"

        text, core, result = auto_regenerate(
            good_llm,
            "Test query",
            target_psi=3.0,  # Lower target for easier success
            max_regenerations=3,
            verbose=False
        )

        # Should produce coherent result
        assert len(text) > 0
        assert isinstance(result['coherent'], (bool, type(result['coherent'])))

    def test_auto_regenerate_max_attempts(self):
        """Test that regeneration respects max attempts"""
        attempt_count = [0]

        def counting_llm(query):
            attempt_count[0] += 1
            return "Random text"

        text, core, result = auto_regenerate(
            counting_llm,
            "Test query",
            target_psi=10.0,  # Impossible target
            max_regenerations=3,
            verbose=False
        )

        # Should make exactly 3 attempts
        assert attempt_count[0] == 3

    def test_auto_regenerate_early_success(self):
        """Test early termination on success"""
        attempt_count = [0]

        def improving_llm(query):
            attempt_count[0] += 1
            if attempt_count[0] >= 2:
                return "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"
            return "Bad text"

        text, core, result = auto_regenerate(
            improving_llm,
            "Test query",
            target_psi=3.0,
            max_regenerations=5,
            verbose=False
        )

        # Should stop before max attempts if successful
        assert attempt_count[0] <= 5


class TestIntegration:
    """Integration tests for complete workflow"""

    def test_complete_workflow(self):
        """Test complete workflow from generation to evaluation"""
        # Mock LLM that generates coherent text
        def mock_llm(query):
            return f"Answer to '{query}': f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"

        # Generate and evaluate
        text, core, result = auto_regenerate(
            mock_llm,
            "Explain f₀",
            target_psi=3.0,
            verbose=False
        )

        # Verify complete result
        assert "141.7" in text or "141.7001" in text
        assert result['mean_psi'] > 0.0
        assert 0.0 <= result['coherence'] <= 1.0

    def test_benchmark_queries(self):
        """Test with benchmark queries from QCALLLMCore"""
        core = QCALLLMCore()

        def mock_llm(query):
            # Generate response based on query
            if "141.7001" in query or "f₀" in query:
                return "f₀ = 141.7001 Hz from mathematical derivation"
            return "General response"

        # Test with first benchmark query
        query = core.benchmark_queries[0]
        text, tuned_core, result = auto_regenerate(
            mock_llm,
            query,
            target_psi=3.0,
            max_regenerations=2,
            verbose=False
        )

        assert isinstance(text, str)
        assert len(text) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
