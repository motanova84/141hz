#!/usr/bin/env python3
"""
Tests for QCAL Spectral Embedding
==================================

Tests spectral embedding implementation and comparison framework.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import pytest
import numpy as np
from qcal import (
    SpectralEmbedding,
    DatasetGenerator,
    BaselineEmbedding,
    EmbeddingEvaluator
)


class TestDatasetGenerator:
    """Test dataset generation."""
    
    def test_init(self):
        """Test initialization."""
        generator = DatasetGenerator(random_state=42)
        assert generator.random_state == 42
    
    def test_generate_definitions(self):
        """Test definition generation."""
        generator = DatasetGenerator(random_state=42)
        definitions = generator.generate_definitions(n_samples=50)
        
        assert len(definitions) == 50
        assert all(isinstance(d, str) for d in definitions)
        assert all(len(d) > 0 for d in definitions)
    
    def test_generate_qa_pairs(self):
        """Test QA pair generation."""
        generator = DatasetGenerator(random_state=42)
        qa_pairs = generator.generate_qa_pairs(n_samples=30)
        
        assert len(qa_pairs) == 30
        assert all(isinstance(pair, tuple) for pair in qa_pairs)
        assert all(len(pair) == 2 for pair in qa_pairs)
    
    def test_generate_semantic_clusters(self):
        """Test semantic cluster generation."""
        generator = DatasetGenerator(random_state=42)
        clusters = generator.generate_semantic_clusters(
            n_clusters=3,
            samples_per_cluster=20
        )
        
        assert len(clusters) == 3
        assert all(len(sentences) == 20 for sentences in clusters.values())
    
    def test_generate_full_dataset(self):
        """Test full dataset generation."""
        generator = DatasetGenerator(random_state=42)
        texts = generator.generate_full_dataset(n_total=100)
        
        assert len(texts) == 100
        assert all(isinstance(t, str) for t in texts)
        
        # Check diversity
        unique_texts = set(texts)
        assert len(unique_texts) > 50  # At least 50% unique


class TestSpectralEmbedding:
    """Test spectral embedding."""
    
    def test_init(self):
        """Test initialization."""
        emb = SpectralEmbedding(n_components=32, f0=141.7001)
        
        assert emb.n_components == 32
        assert emb.f0 == 141.7001
        assert emb.use_qcal_resonance is True
        assert not emb.is_fitted
    
    def test_fit_transform(self):
        """Test fit and transform."""
        texts = [
            "quantum mechanics describes wave-particle duality",
            "gravity curves spacetime according to Einstein",
            "energy and momentum are conserved quantities",
            "photons exhibit quantum interference patterns",
            "electromagnetic waves propagate through space"
        ]
        
        emb = SpectralEmbedding(n_components=4, random_state=42)
        vectors = emb.fit_transform(texts)
        
        assert vectors.shape == (5, 4)
        assert emb.is_fitted
        assert emb.spectral_basis_ is not None
    
    def test_transform_unfitted(self):
        """Test transform before fitting raises error."""
        emb = SpectralEmbedding(n_components=4)
        
        with pytest.raises(ValueError, match="must be fitted"):
            emb.transform(["test"])
    
    def test_similarity(self):
        """Test similarity computation."""
        texts = [
            "quantum mechanics and wave functions",
            "quantum theory and particle physics",
            "classical mechanics and Newton laws"
        ]
        
        emb = SpectralEmbedding(n_components=8, random_state=42)
        emb.fit(texts)
        
        # Similar texts should have higher similarity
        sim1 = emb.similarity(texts[0], texts[1])
        sim2 = emb.similarity(texts[0], texts[2])
        
        assert 0 <= sim1 <= 1
        assert 0 <= sim2 <= 1
        # First two are more similar (both mention quantum)
        assert sim1 > sim2
    
    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        texts = ["text " + str(i) for i in range(10)]
        
        emb = SpectralEmbedding(n_components=16, random_state=42)
        emb.fit_transform(texts)
        
        ratio = emb.get_compression_ratio()
        assert ratio > 1.0  # Should compress
    
    def test_explained_variance(self):
        """Test explained variance."""
        texts = ["text " + str(i) for i in range(20)]
        
        emb = SpectralEmbedding(n_components=8, random_state=42)
        emb.fit_transform(texts)
        
        var_ratio = emb.explained_variance_ratio()
        
        assert len(var_ratio) == 8
        assert all(0 <= v <= 1 for v in var_ratio)
        assert var_ratio.sum() <= 1.0
    
    def test_qcal_resonance(self):
        """Test QCAL resonance mode."""
        texts = ["sample text " + str(i) for i in range(10)]
        
        # With QCAL resonance
        emb_qcal = SpectralEmbedding(
            n_components=8,
            use_qcal_resonance=True,
            random_state=42
        )
        vectors_qcal = emb_qcal.fit_transform(texts)
        
        # Without QCAL resonance
        emb_no_qcal = SpectralEmbedding(
            n_components=8,
            use_qcal_resonance=False,
            random_state=42
        )
        vectors_no_qcal = emb_no_qcal.fit_transform(texts)
        
        # Should produce different results
        assert not np.allclose(vectors_qcal, vectors_no_qcal)
    
    def test_reproducibility(self):
        """Test reproducibility with same random state."""
        texts = ["text " + str(i) for i in range(10)]
        
        emb1 = SpectralEmbedding(n_components=8, random_state=42)
        vectors1 = emb1.fit_transform(texts)
        
        emb2 = SpectralEmbedding(n_components=8, random_state=42)
        vectors2 = emb2.fit_transform(texts)
        
        np.testing.assert_array_almost_equal(vectors1, vectors2)


class TestBaselineEmbedding:
    """Test baseline embedding."""
    
    def test_init(self):
        """Test initialization."""
        emb = BaselineEmbedding(n_components=32)
        
        assert emb.n_components == 32
        assert not emb.is_fitted
    
    def test_fit_transform(self):
        """Test fit and transform."""
        texts = [
            "quantum mechanics",
            "general relativity",
            "statistical mechanics",
            "quantum field theory"
        ]
        
        emb = BaselineEmbedding(n_components=8, random_state=42)
        vectors = emb.fit_transform(texts)
        
        assert vectors.shape == (4, 8)
        assert emb.is_fitted
    
    def test_transform_unfitted(self):
        """Test transform before fitting raises error."""
        emb = BaselineEmbedding(n_components=8)
        
        with pytest.raises(ValueError, match="must be fitted"):
            emb.transform(["test"])


class TestEmbeddingEvaluator:
    """Test embedding evaluator."""
    
    def test_init(self):
        """Test initialization."""
        evaluator = EmbeddingEvaluator(random_state=42)
        assert evaluator.random_state == 42
    
    def test_evaluate_semantic_similarity(self):
        """Test semantic similarity evaluation."""
        texts = [
            "quantum physics",
            "quantum mechanics",
            "classical physics",
            "computer science"
        ]
        
        # Create simple embeddings
        embeddings = np.random.randn(4, 8)
        
        evaluator = EmbeddingEvaluator(random_state=42)
        metrics = evaluator.evaluate_semantic_similarity(embeddings, texts)
        
        assert 'similarity_correlation' in metrics
        assert 'similarity_mae' in metrics
        assert 'mean_similarity' in metrics
        assert 'std_similarity' in metrics
    
    def test_evaluate_clustering(self):
        """Test clustering evaluation."""
        # Create embeddings with clear clusters
        cluster1 = np.random.randn(10, 8) + [1, 0, 0, 0, 0, 0, 0, 0]
        cluster2 = np.random.randn(10, 8) + [0, 1, 0, 0, 0, 0, 0, 0]
        embeddings = np.vstack([cluster1, cluster2])
        
        evaluator = EmbeddingEvaluator(random_state=42)
        metrics = evaluator.evaluate_clustering(embeddings, n_clusters=2)
        
        assert 'silhouette_score' in metrics
        assert 'inertia' in metrics
        assert metrics['n_clusters'] == 2
        
        # With true labels
        true_labels = np.array([0]*10 + [1]*10)
        metrics_with_labels = evaluator.evaluate_clustering(
            embeddings,
            true_labels=true_labels,
            n_clusters=2
        )
        
        assert 'purity' in metrics_with_labels
        assert metrics_with_labels['purity'] > 0.5
    
    def test_evaluate_retrieval(self):
        """Test retrieval evaluation."""
        texts = ["text " + str(i) for i in range(20)]
        embeddings = np.random.randn(20, 8)
        
        evaluator = EmbeddingEvaluator(random_state=42)
        metrics = evaluator.evaluate_retrieval(embeddings, texts, k=5)
        
        assert 'mean_retrieval_score' in metrics
        assert 'std_retrieval_score' in metrics
        assert metrics['k'] == 5
    
    def test_compare_embeddings(self):
        """Test embedding comparison."""
        texts = ["text " + str(i) for i in range(30)]
        
        emb1 = np.random.randn(30, 16)
        emb2 = np.random.randn(30, 32)
        
        embeddings_dict = {
            'method1-16D': emb1,
            'method2-32D': emb2
        }
        
        evaluator = EmbeddingEvaluator(random_state=42)
        results = evaluator.compare_embeddings(embeddings_dict, texts)
        
        assert 'method1-16D' in results
        assert 'method2-32D' in results
        
        # Check all expected metrics
        for method_results in results.values():
            assert 'similarity_correlation' in method_results
            assert 'silhouette_score' in method_results
            assert 'mean_retrieval_score' in method_results
            assert 'n_dimensions' in method_results
            assert 'compression_ratio' in method_results


class TestIntegration:
    """Integration tests."""
    
    def test_full_pipeline(self):
        """Test complete pipeline."""
        # Generate dataset
        generator = DatasetGenerator(random_state=42)
        texts = generator.generate_full_dataset(n_total=50)
        
        # Train embeddings
        spectral_emb = SpectralEmbedding(n_components=8, random_state=42)
        spectral_vectors = spectral_emb.fit_transform(texts)
        
        baseline_emb = BaselineEmbedding(n_components=16, random_state=42)
        baseline_vectors = baseline_emb.fit_transform(texts)
        
        # Evaluate
        evaluator = EmbeddingEvaluator(random_state=42)
        results = evaluator.compare_embeddings(
            {
                'Spectral-8D': spectral_vectors,
                'Baseline-16D': baseline_vectors
            },
            texts
        )
        
        # Verify results
        assert 'Spectral-8D' in results
        assert 'Baseline-16D' in results
        
        # Check compression
        assert results['Spectral-8D']['n_dimensions'] == 8
        assert results['Baseline-16D']['n_dimensions'] == 16
        
        # Both should have reasonable performance
        assert results['Spectral-8D']['silhouette_score'] > -1
        assert results['Baseline-16D']['silhouette_score'] > -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
