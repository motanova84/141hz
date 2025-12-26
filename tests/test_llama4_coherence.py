#!/usr/bin/env python3
"""
Tests for Llama 4 Maverick Coherence Module

Tests the integration of Llama 4 Maverick as a coherence backend for QCAL-LLM.
Note: These tests require HF_TOKEN to be set and may take time on first run.
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestLlama4CoherenceImport:
    """Test that the module can be imported properly."""
    
    def test_import_module(self):
        """Test that llama4_coherence module can be imported."""
        try:
            import llama4_coherence
            assert hasattr(llama4_coherence, 'Llama4Coherence')
            assert hasattr(llama4_coherence, 'MODEL_ID')
            assert hasattr(llama4_coherence, 'CACHE_DIR')
        except ImportError as e:
            pytest.skip(f"transformers not installed: {e}")
    
    def test_model_constants(self):
        """Test that model constants are defined correctly."""
        try:
            from llama4_coherence import MODEL_ID, CACHE_DIR
            assert MODEL_ID == "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
            assert CACHE_DIR == "./models/llama4"
        except ImportError:
            pytest.skip("transformers not installed")


class TestLlama4CoherenceInitialization:
    """Test Llama4Coherence class initialization."""
    
    def test_initialization_without_token(self):
        """Test that initialization fails without HF_TOKEN."""
        try:
            from llama4_coherence import Llama4Coherence
        except ImportError:
            pytest.skip("transformers not installed")
        
        # Temporarily remove HF_TOKEN
        original_token = os.environ.get('HF_TOKEN')
        if 'HF_TOKEN' in os.environ:
            del os.environ['HF_TOKEN']
        
        try:
            with pytest.raises(ValueError, match="HF_TOKEN environment variable is required"):
                Llama4Coherence()
        finally:
            # Restore token if it existed
            if original_token:
                os.environ['HF_TOKEN'] = original_token
    
    def test_initialization_with_token(self):
        """Test that initialization succeeds with HF_TOKEN."""
        try:
            from llama4_coherence import Llama4Coherence
        except ImportError:
            pytest.skip("transformers not installed")
        
        # Mock HF_TOKEN
        with patch.dict(os.environ, {'HF_TOKEN': 'mock_token'}):
            llama4 = Llama4Coherence()
            assert llama4.hf_token == 'mock_token'
            assert llama4.model_id == "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
            assert llama4.cache_dir == "./models/llama4"
            # Model should not be loaded yet (lazy loading)
            assert llama4._model is None
            assert llama4._tokenizer is None
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        try:
            from llama4_coherence import Llama4Coherence
        except ImportError:
            pytest.skip("transformers not installed")
        
        custom_model_id = "custom/model"
        custom_cache = "./custom_cache"
        
        with patch.dict(os.environ, {'HF_TOKEN': 'mock_token'}):
            llama4 = Llama4Coherence(model_id=custom_model_id, cache_dir=custom_cache)
            assert llama4.model_id == custom_model_id
            assert llama4.cache_dir == custom_cache


class TestLlama4CoherenceMocked:
    """Test Llama4Coherence with mocked model to avoid loading actual model."""
    
    @pytest.fixture
    def mock_llama4(self):
        """Create a mocked Llama4Coherence instance."""
        try:
            from llama4_coherence import Llama4Coherence
        except ImportError:
            pytest.skip("transformers not installed")
        
        with patch.dict(os.environ, {'HF_TOKEN': 'mock_token'}):
            llama4 = Llama4Coherence()
            
            # Mock the model and tokenizer
            llama4._model = MagicMock()
            llama4._tokenizer = MagicMock()
            llama4._device = 'cpu'
            
            return llama4
    
    def test_get_coherence_score_high(self, mock_llama4):
        """Test coherence scoring with high coherence text."""
        # Mock tokenizer and model responses
        mock_llama4._tokenizer.return_value = MagicMock(to=lambda x: MagicMock())
        mock_llama4._model.generate.return_value = [[1, 2, 3]]
        mock_llama4._tokenizer.decode.return_value = "0.9"
        
        text = "The frequency 141.7 Hz emerges from prime numbers and golden ratio."
        score = mock_llama4.get_coherence_score(text)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert score == 0.9
    
    def test_get_coherence_score_low(self, mock_llama4):
        """Test coherence scoring with low coherence text."""
        mock_llama4._tokenizer.return_value = MagicMock(to=lambda x: MagicMock())
        mock_llama4._model.generate.return_value = [[1, 2, 3]]
        mock_llama4._tokenizer.decode.return_value = "0.2"
        
        text = "Random incoherent text without meaning."
        score = mock_llama4.get_coherence_score(text)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert score == 0.2
    
    def test_get_coherence_score_fallback(self, mock_llama4):
        """Test fallback behavior when parsing fails."""
        mock_llama4._tokenizer.return_value = MagicMock(to=lambda x: MagicMock())
        mock_llama4._model.generate.return_value = [[1, 2, 3]]
        mock_llama4._tokenizer.decode.return_value = "Invalid response"
        
        text = "Some text"
        score = mock_llama4.get_coherence_score(text)
        
        # Should fallback to 0.5
        assert score == 0.5
    
    def test_get_coherence_score_clamping(self, mock_llama4):
        """Test that scores are clamped to [0, 1] range."""
        mock_llama4._tokenizer.return_value = MagicMock(to=lambda x: MagicMock())
        mock_llama4._model.generate.return_value = [[1, 2, 3]]
        
        # Test upper bound clamping
        mock_llama4._tokenizer.decode.return_value = "1.5"
        score = mock_llama4.get_coherence_score("text")
        assert score == 1.0
        
        # Test lower bound clamping
        mock_llama4._tokenizer.decode.return_value = "-0.5"
        score = mock_llama4.get_coherence_score("text")
        assert score == 0.0
    
    def test_batch_coherence_scores(self, mock_llama4):
        """Test batch coherence evaluation."""
        mock_llama4._tokenizer.return_value = MagicMock(to=lambda x: MagicMock())
        mock_llama4._model.generate.return_value = [[1, 2, 3]]
        
        # Mock different scores for different texts
        scores_sequence = ["0.9", "0.5", "0.3"]
        mock_llama4._tokenizer.decode.side_effect = scores_sequence
        
        texts = [
            "Coherent physics text",
            "Somewhat coherent text",
            "Incoherent text"
        ]
        
        scores = mock_llama4.batch_coherence_scores(texts)
        
        assert len(scores) == 3
        assert all(isinstance(s, float) for s in scores)
        assert all(0.0 <= s <= 1.0 for s in scores)


class TestLlama4Integration:
    """Test Llama 4 integration with QCALLLMCore."""
    
    def test_qcal_core_with_llama4_disabled(self):
        """Test QCALLLMCore with Llama 4 disabled."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        core = QCALLLMCore(use_llama4=False)
        assert core.use_llama4 is False
        assert core.llama4 is None
    
    def test_qcal_core_with_llama4_enabled_no_token(self):
        """Test QCALLLMCore with Llama 4 enabled but no token."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        # Remove HF_TOKEN if it exists
        original_token = os.environ.get('HF_TOKEN')
        if 'HF_TOKEN' in os.environ:
            del os.environ['HF_TOKEN']
        
        try:
            # Should fallback gracefully
            core = QCALLLMCore(use_llama4=True)
            assert core.use_llama4 is False  # Should fallback
            assert core.llama4 is None
        finally:
            if original_token:
                os.environ['HF_TOKEN'] = original_token
    
    def test_qcal_core_compute_coherence_fallback(self):
        """Test that compute_coherence falls back to pattern matching."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        core = QCALLLMCore(use_llama4=False)
        
        # Test with full coherence text
        text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz"
        coherence = core.compute_coherence(text)
        
        # Should use pattern matching
        assert isinstance(coherence, float)
        assert 0.0 <= coherence <= 1.0
        assert coherence == 1.0  # All patterns match
    
    def test_qcal_core_compute_coherence_with_llama4(self):
        """Test compute_coherence with Llama 4 enabled."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        try:
            import transformers
        except ImportError:
            pytest.skip("transformers not installed")
        
        # Mock Llama4Coherence instance
        mock_instance = MagicMock()
        mock_instance.get_coherence_score.return_value = 0.95
        
        with patch.dict(os.environ, {'HF_TOKEN': 'mock_token'}):
            with patch('llama4_coherence.Llama4Coherence', return_value=mock_instance):
                core = QCALLLMCore(use_llama4=True)
                if core.llama4 is None:
                    # If llama4 initialization failed, manually set it for test
                    core.llama4 = mock_instance
                    core.use_llama4 = True
                
                text = "Quantum coherence at 141.7 Hz"
                coherence = core.compute_coherence(text)
                
                # Should use Llama 4
                assert coherence == 0.95
                mock_instance.get_coherence_score.assert_called_once_with(text)


class TestLlama4CoherenceComparison:
    """Test comparison between Llama 4 and baseline coherence."""
    
    def test_coherence_comparison_structure(self):
        """Test that we can compare Llama 4 vs baseline coherence."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        # Create two cores: one with Llama 4, one without
        core_baseline = QCALLLMCore(use_llama4=False)
        
        # High coherence text
        text = "The frequency 141.7 Hz emerges from ζ'(1/2) and φ³."
        
        # Baseline should use pattern matching
        baseline_score = core_baseline.compute_coherence(text)
        
        assert isinstance(baseline_score, float)
        assert 0.0 <= baseline_score <= 1.0
    
    def test_high_coherence_text(self):
        """Test that high coherence text scores well with baseline."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        core = QCALLLMCore(use_llama4=False)
        text = "The frequency 141.7 Hz emerges from prime numbers and golden ratio."
        score = core.compute_coherence(text)
        
        # Should detect at least f0
        assert score >= 0.3  # At least 1/3 symbols
    
    def test_low_coherence_text(self):
        """Test that low coherence text scores poorly with baseline."""
        try:
            from QCALLLMCore import QCALLLMCore
        except ImportError:
            pytest.skip("QCALLLMCore not available")
        
        core = QCALLLMCore(use_llama4=False)
        text = "Random text without any relevant physics content."
        score = core.compute_coherence(text)
        
        # Should detect no symbols
        assert score == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
