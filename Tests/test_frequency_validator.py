"""
Unit tests for QC-LLM frequency validator

Tests the compute_coherence function and API endpoints as specified in the problem statement.
"""

import pytest
import sys
import os

# Add API to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'API', 'Python'))

from qc_llm import compute_coherence, compute_coherence_score, F0


class TestComputeCoherence:
    """Test suite for compute_coherence function"""
    
    def test_compute_coherence_basic(self):
        """Test basic coherence computation"""
        result = compute_coherence("Quantum coherence is fascinating", use_bert=False)
        
        # Verify return type and structure
        assert isinstance(result, dict)
        assert "coherence" in result
        assert "frequency_alignment" in result
        assert "quantum_metric" in result
        assert "recommendation" in result
    
    def test_coherence_bounds(self):
        """Test that coherence values are in [0, 1]"""
        test_texts = [
            "Quantum coherence is fascinating",
            "The quick brown fox jumps over the lazy dog",
            "Hello world",
            "A" * 100,  # Repetitive text
        ]
        
        for text in test_texts:
            result = compute_coherence(text, use_bert=False)
            assert 0 <= result["coherence"] <= 1, f"Coherence out of bounds for text: {text[:50]}"
            assert 0 <= result["frequency_alignment"] <= 1
            assert 0 <= result["quantum_metric"] <= 1
    
    def test_frequency_alignment_bounds(self):
        """Test frequency alignment is in [0, 1]"""
        result = compute_coherence("Test text for frequency alignment", use_bert=False)
        assert 0 <= result["frequency_alignment"] <= 1
    
    def test_quantum_metric_bounds(self):
        """Test quantum metric is in [0, 1]"""
        result = compute_coherence("Test text with some repeated words words", use_bert=False)
        assert 0 <= result["quantum_metric"] <= 1
    
    def test_recommendation_values(self):
        """Test recommendation values match specification"""
        valid_recommendations = [
            "HIGH COHERENCE",
            "MODERATE COHERENCE",
            "LOW COHERENCE - Consider rephrasing",
            "INVALID - Empty text"
        ]
        
        test_texts = [
            "Quantum coherence is fascinating",
            "Hello world",
            "",
            "A",
        ]
        
        for text in test_texts:
            result = compute_coherence(text, use_bert=False)
            assert result["recommendation"] in valid_recommendations
    
    def test_high_coherence_threshold(self):
        """Test HIGH COHERENCE recommendation threshold"""
        # We can't guarantee HIGH without BERT, but we can verify the logic
        result = compute_coherence("The quantum field exhibits remarkable coherence properties", use_bert=False)
        
        if result["coherence"] > 0.8:
            assert result["recommendation"] == "HIGH COHERENCE"
    
    def test_moderate_coherence_threshold(self):
        """Test MODERATE COHERENCE recommendation threshold"""
        result = compute_coherence("Some text here", use_bert=False)
        
        if 0.6 < result["coherence"] <= 0.8:
            assert result["recommendation"] == "MODERATE COHERENCE"
    
    def test_low_coherence_threshold(self):
        """Test LOW COHERENCE recommendation threshold"""
        result = compute_coherence("a", use_bert=False)
        
        if result["coherence"] <= 0.6:
            assert result["recommendation"] == "LOW COHERENCE - Consider rephrasing"
    
    def test_empty_text(self):
        """Test handling of empty text"""
        result = compute_coherence("", use_bert=False)
        assert result["coherence"] == 0.0
        assert result["recommendation"] == "INVALID - Empty text"
    
    def test_whitespace_only(self):
        """Test handling of whitespace-only text"""
        result = compute_coherence("   \n\t  ", use_bert=False)
        assert result["coherence"] == 0.0
        assert result["recommendation"] == "INVALID - Empty text"
    
    def test_backward_compatibility(self):
        """Test backward compatibility with compute_coherence_score"""
        text = "Quantum coherence is fascinating"
        
        result = compute_coherence_score(text)
        
        # Verify old API still works
        assert "coherence" in result
        assert "frequency_alignment" in result
        assert "quantum_entropy" in result  # Legacy field
        assert "recommendation" in result
    
    def test_f0_constant(self):
        """Test that F0 constant is correct"""
        assert F0 == 141.7001
    
    def test_repetitive_text(self):
        """Test quantum metric with highly repetitive text"""
        repetitive = "quantum quantum quantum quantum"
        varied = "quantum coherence frequency alignment"
        
        result_rep = compute_coherence(repetitive, use_bert=False)
        result_var = compute_coherence(varied, use_bert=False)
        
        # Repetitive text should have higher quantum_metric
        # (quantum_metric = 1 - unique/total, so higher = more repetition)
        assert result_rep["quantum_metric"] > result_var["quantum_metric"]
    
    def test_long_text(self):
        """Test with longer text"""
        long_text = " ".join(["quantum coherence"] * 100)
        result = compute_coherence(long_text, use_bert=False)
        
        assert 0 <= result["coherence"] <= 1
        assert isinstance(result["recommendation"], str)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "Quantum @#$% coherence!!! is... fascinating???"
        result = compute_coherence(text, use_bert=False)
        
        # Should not crash and should return valid values
        assert 0 <= result["coherence"] <= 1


def _check_bert_available():
    """Helper to check if BERT/transformers is available"""
    try:
        import qc_llm.metrics as metrics_module
        return getattr(metrics_module, 'TRANSFORMERS_AVAILABLE', False)
    except:
        return False


@pytest.mark.skipif(
    not _check_bert_available(),
    reason="Transformers not available"
)
class TestComputeCoherenceBERT:
    """Test suite for BERT-based coherence computation"""
    
    def test_bert_coherence_basic(self):
        """Test BERT-based coherence computation"""
        result = compute_coherence("Quantum coherence is fascinating", use_bert=True)
        
        # Verify return type and structure
        assert isinstance(result, dict)
        assert 0 <= result["coherence"] <= 1
    
    def test_bert_vs_basic(self):
        """Test that BERT and basic methods both work"""
        text = "Quantum coherence is fascinating"
        
        result_bert = compute_coherence(text, use_bert=True)
        result_basic = compute_coherence(text, use_bert=False)
        
        # Both should return valid results
        assert 0 <= result_bert["coherence"] <= 1
        assert 0 <= result_basic["coherence"] <= 1


def test_import_structure():
    """Test that all required functions are importable"""
    from qc_llm import (
        compute_coherence,
        compute_coherence_score,
        compute_frequency_alignment,
        compute_quantum_entropy,
        F0,
        QC_LLM
    )
    
    assert callable(compute_coherence)
    assert callable(compute_coherence_score)
    assert callable(compute_frequency_alignment)
    assert callable(compute_quantum_entropy)
    assert isinstance(F0, float)
    assert F0 == 141.7001


class TestQCLLMClass:
    """Test the QC_LLM wrapper class"""
    
    def test_qc_llm_init(self):
        """Test QC_LLM initialization"""
        from qc_llm import QC_LLM
        
        validator = QC_LLM()
        assert hasattr(validator, 'validate')
        assert hasattr(validator, 'batch_validate')
    
    def test_qc_llm_validate(self):
        """Test QC_LLM validate method"""
        from qc_llm import QC_LLM
        
        validator = QC_LLM()
        result = validator.validate("Quantum coherence is fascinating")
        
        assert isinstance(result, dict)
        assert "coherence" in result
    
    def test_qc_llm_batch_validate(self):
        """Test QC_LLM batch validation"""
        from qc_llm import QC_LLM
        
        validator = QC_LLM()
        texts = [
            "First quantum text",
            "Second coherence text",
            "Third alignment text"
        ]
        
        results = validator.batch_validate(texts)
        assert len(results) == 3
        assert all(isinstance(r, dict) for r in results)
        assert all("coherence" in r for r in results)
    
    def test_qc_llm_get_frequency(self):
        """Test QC_LLM.get_frequency static method"""
        from qc_llm import QC_LLM
        
        freq = QC_LLM.get_frequency()
        assert freq == 141.7001


class TestComputeAutomaticSize:
    """Tests for compute_automatic_size — Patent Claim 10 (automatic sizing)."""

    def setup_method(self):
        """Import once per test."""
        from qc_llm import compute_automatic_size
        self.compute_automatic_size = compute_automatic_size

    def test_returns_dict_with_required_keys(self):
        """Result must contain all expected keys."""
        result = self.compute_automatic_size()
        for key in ("a_eff", "a_eff_sq", "psi_achieved", "quantum_scale", "recommendation"):
            assert key in result, f"Missing key: {key}"

    def test_a_eff_positive(self):
        """A_eff must be strictly positive."""
        result = self.compute_automatic_size(target_psi=0.5, information_density=1.0)
        assert result["a_eff"] > 0

    def test_a_eff_sq_equals_square_of_a_eff(self):
        """a_eff_sq must equal a_eff²."""
        result = self.compute_automatic_size(target_psi=0.888, information_density=1.0)
        assert result["a_eff_sq"] == pytest.approx(result["a_eff"] ** 2, rel=1e-6)

    def test_a_eff_in_unit_interval(self):
        """A_eff must be in (0, 1] across varied parameter combinations."""
        test_cases = [
            {"target_psi": 0.1},
            {"target_psi": 0.5},
            {"target_psi": 0.888},
            {"target_psi": 1.0},
            {"target_psi": 0.5, "information_density": 2.0},
            {"target_psi": 0.5, "temperature": 273.0},
            {"target_psi": 0.5, "a_bio": 1e8},
        ]
        for kwargs in test_cases:
            result = self.compute_automatic_size(**kwargs)
            assert 0 < result["a_eff"] <= 1.0, (
                f"a_eff out of range for kwargs={kwargs}: got {result['a_eff']}"
            )

    def test_quantum_scale_positive(self):
        """Quantum thermal scale ℏ/(k_B T) must be positive."""
        result = self.compute_automatic_size(target_psi=0.888)
        assert result["quantum_scale"] > 0

    def test_psi_achieved_positive(self):
        """Achieved Ψ must be positive."""
        result = self.compute_automatic_size(target_psi=0.888)
        assert result["psi_achieved"] > 0

    def test_recommendation_is_string(self):
        """Recommendation must be a non-empty string."""
        result = self.compute_automatic_size(target_psi=0.888)
        assert isinstance(result["recommendation"], str)
        assert len(result["recommendation"]) > 0

    def test_invalid_target_psi_raises(self):
        """Non-positive target_psi must raise ValueError."""
        with pytest.raises(ValueError):
            self.compute_automatic_size(target_psi=0.0)
        with pytest.raises(ValueError):
            self.compute_automatic_size(target_psi=-1.0)

    def test_invalid_information_density_raises(self):
        """Non-positive information_density must raise ValueError."""
        with pytest.raises(ValueError):
            self.compute_automatic_size(target_psi=0.888, information_density=0.0)

    def test_invalid_temperature_raises(self):
        """Non-positive temperature must raise ValueError."""
        with pytest.raises(ValueError):
            self.compute_automatic_size(target_psi=0.888, temperature=0.0)

    def test_recommendation_optimal_for_large_a_eff(self):
        """Systems with a_eff >= 0.8 receive OPTIMAL recommendation."""
        result = self.compute_automatic_size(target_psi=0.888)
        if result["a_eff"] >= 0.8:
            assert result["recommendation"] == "OPTIMAL SIZE - High coherence achievable"

    def test_automatic_size_importable_from_qc_llm(self):
        """compute_automatic_size must be importable from the top-level package."""
        from qc_llm import compute_automatic_size  # noqa: F401 — verify import works


class TestQCALLLMCoreAutomaticSize:
    """Tests for QCALLLMCore.compute_automatic_size method."""

    def setup_method(self):
        from qc_llm import QCALLLMCore
        self.core = QCALLLMCore()

    def test_method_exists(self):
        """QCALLLMCore must expose compute_automatic_size."""
        assert hasattr(self.core, "compute_automatic_size")
        assert callable(self.core.compute_automatic_size)

    def test_returns_dict(self):
        """Method must return a dict."""
        result = self.core.compute_automatic_size(target_psi=0.888)
        assert isinstance(result, dict)

    def test_a_eff_positive(self):
        """A_eff from core method must be positive."""
        result = self.core.compute_automatic_size(target_psi=0.5)
        assert result["a_eff"] > 0

    def test_uses_instance_f0(self):
        """Method must pass instance f0 to compute_automatic_size, affecting psi_achieved."""
        from qc_llm import QCALLLMCore
        core_custom = QCALLLMCore(f0=200.0)
        result_default = self.core.compute_automatic_size(target_psi=0.888)
        result_custom = core_custom.compute_automatic_size(target_psi=0.888)
        # Different f0 → different denominator → different psi_achieved
        # (quantum_scale is the same because it only depends on ℏ, k_B, T)
        assert result_default["quantum_scale"] == pytest.approx(result_custom["quantum_scale"], rel=1e-9)
        assert result_default["psi_achieved"] != result_custom["psi_achieved"]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
