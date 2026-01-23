#!/usr/bin/env python3
"""
QCAL Embedding Comparison Framework
====================================

Compares spectral embeddings against baseline methods:
- Word2Vec (gensim)
- Simple TF-IDF + SVD baseline

Evaluates on:
- Semantic similarity
- Clustering coherence
- Meaning retrieval with fewer dimensions

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Try to import gensim for Word2Vec, but make it optional
try:
    from gensim.models import Word2Vec
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False
    warnings.warn("gensim not available, Word2Vec baseline will be skipped")


class BaselineEmbedding:
    """Simple TF-IDF + SVD baseline embedding."""
    
    def __init__(self, n_components: int = 32, random_state: Optional[int] = 42):
        """
        Initialize baseline embedding.
        
        Args:
            n_components: Target dimensionality
            random_state: Random seed
        """
        self.n_components = n_components
        self.random_state = random_state
        
        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=1
        )
        
        # SVD for dimensionality reduction
        self.svd = TruncatedSVD(
            n_components=n_components,
            random_state=random_state
        )
        
        self.is_fitted = False
        
    def fit(self, texts: List[str]) -> 'BaselineEmbedding':
        """Fit baseline to corpus."""
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.svd.fit(tfidf_matrix)
        self.is_fitted = True
        return self
        
    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform texts to embeddings."""
        if not self.is_fitted:
            raise ValueError("BaselineEmbedding must be fitted first")
        
        tfidf_matrix = self.vectorizer.transform(texts)
        embeddings = self.svd.transform(tfidf_matrix)
        return embeddings
        
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit and transform."""
        return self.fit(texts).transform(texts)


class Word2VecEmbedding:
    """Word2Vec baseline embedding."""
    
    def __init__(self, vector_size: int = 32, random_state: Optional[int] = 42):
        """
        Initialize Word2Vec embedding.
        
        Args:
            vector_size: Embedding dimensionality
            random_state: Random seed
        """
        if not GENSIM_AVAILABLE:
            raise ImportError("gensim is required for Word2Vec baseline")
            
        self.vector_size = vector_size
        self.random_state = random_state
        self.model = None
        self.is_fitted = False
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()
        
    def fit(self, texts: List[str]) -> 'Word2VecEmbedding':
        """Fit Word2Vec to corpus."""
        # Tokenize texts
        tokenized_texts = [self._tokenize(text) for text in texts]
        
        # Train Word2Vec
        self.model = Word2Vec(
            sentences=tokenized_texts,
            vector_size=self.vector_size,
            window=5,
            min_count=1,
            workers=1,
            seed=self.random_state
        )
        
        self.is_fitted = True
        return self
        
    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform texts to embeddings."""
        if not self.is_fitted:
            raise ValueError("Word2VecEmbedding must be fitted first")
        
        embeddings = []
        for text in texts:
            tokens = self._tokenize(text)
            # Average word vectors
            word_vectors = []
            for token in tokens:
                if token in self.model.wv:
                    word_vectors.append(self.model.wv[token])
            
            if word_vectors:
                avg_vector = np.mean(word_vectors, axis=0)
            else:
                # Zero vector for unknown words
                avg_vector = np.zeros(self.vector_size)
            
            embeddings.append(avg_vector)
        
        return np.array(embeddings)
        
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit and transform."""
        return self.fit(texts).transform(texts)


class EmbeddingEvaluator:
    """Evaluate and compare embedding methods."""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize evaluator.
        
        Args:
            random_state: Random seed
        """
        self.random_state = random_state
        np.random.seed(random_state)
        
    def evaluate_semantic_similarity(
        self,
        embeddings: np.ndarray,
        texts: List[str],
        test_pairs: Optional[List[Tuple[int, int, float]]] = None
    ) -> Dict[str, float]:
        """
        Evaluate semantic similarity preservation.
        
        Args:
            embeddings: Embedding matrix
            texts: Original texts
            test_pairs: List of (idx1, idx2, expected_similarity) tuples
            
        Returns:
            Dictionary of similarity metrics
        """
        if test_pairs is None:
            # Generate random test pairs
            n_samples = len(texts)
            n_pairs = min(100, n_samples * (n_samples - 1) // 2)
            
            test_pairs = []
            for _ in range(n_pairs):
                i = np.random.randint(0, n_samples)
                j = np.random.randint(0, n_samples)
                if i != j:
                    # Use simple text overlap as proxy for expected similarity
                    words_i = set(texts[i].lower().split())
                    words_j = set(texts[j].lower().split())
                    overlap = len(words_i & words_j) / max(len(words_i | words_j), 1)
                    test_pairs.append((i, j, overlap))
        
        # Compute embedding similarities
        similarities = []
        expected_similarities = []
        
        for i, j, expected_sim in test_pairs:
            emb_sim = cosine_similarity(
                embeddings[i:i+1],
                embeddings[j:j+1]
            )[0, 0]
            
            similarities.append(emb_sim)
            expected_similarities.append(expected_sim)
        
        # Compute correlation
        correlation = np.corrcoef(similarities, expected_similarities)[0, 1]
        
        # Mean absolute error
        mae = np.mean(np.abs(np.array(similarities) - np.array(expected_similarities)))
        
        return {
            'similarity_correlation': float(correlation),
            'similarity_mae': float(mae),
            'mean_similarity': float(np.mean(similarities)),
            'std_similarity': float(np.std(similarities))
        }
    
    def evaluate_clustering(
        self,
        embeddings: np.ndarray,
        true_labels: Optional[np.ndarray] = None,
        n_clusters: int = 5,
        n_init: int = 3
    ) -> Dict[str, float]:
        """
        Evaluate clustering coherence.
        
        Args:
            embeddings: Embedding matrix
            true_labels: Optional ground truth labels
            n_clusters: Number of clusters for K-means
            n_init: Number of K-means initializations (default: 3)
                   Note: Reduced from 10 for performance. Trade-off: faster
                   evaluation with slightly less stable clustering results.
            
        Returns:
            Dictionary of clustering metrics
        """
        # K-means clustering
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=self.random_state,
            n_init=n_init
        )
        pred_labels = kmeans.fit_predict(embeddings)
        
        # Silhouette score
        silhouette = silhouette_score(embeddings, pred_labels)
        
        # Inertia (within-cluster sum of squares)
        inertia = kmeans.inertia_
        
        metrics = {
            'silhouette_score': float(silhouette),
            'inertia': float(inertia),
            'n_clusters': n_clusters
        }
        
        # If true labels provided, compute purity
        if true_labels is not None:
            purity = self._compute_purity(true_labels, pred_labels)
            metrics['purity'] = float(purity)
        
        return metrics
    
    def _compute_purity(self, true_labels: np.ndarray, pred_labels: np.ndarray) -> float:
        """Compute clustering purity."""
        from collections import Counter
        
        # Group by predicted clusters
        clusters = {}
        for i, pred_label in enumerate(pred_labels):
            if pred_label not in clusters:
                clusters[pred_label] = []
            clusters[pred_label].append(true_labels[i])
        
        # Compute purity
        total_correct = 0
        for cluster_labels in clusters.values():
            # Most common true label in this cluster
            most_common = Counter(cluster_labels).most_common(1)[0][1]
            total_correct += most_common
        
        purity = total_correct / len(true_labels)
        return purity
    
    def evaluate_retrieval(
        self,
        embeddings: np.ndarray,
        texts: List[str],
        query_indices: Optional[List[int]] = None,
        k: int = 5
    ) -> Dict[str, float]:
        """
        Evaluate meaning retrieval (k-NN search).
        
        Args:
            embeddings: Embedding matrix
            texts: Original texts
            query_indices: Indices to use as queries
            k: Number of nearest neighbors
            
        Returns:
            Dictionary of retrieval metrics
        """
        if query_indices is None:
            # Random queries
            n_queries = min(20, len(texts))
            query_indices = np.random.choice(len(texts), n_queries, replace=False)
        
        # Compute pairwise distances
        distances = pairwise_distances(embeddings, metric='cosine')
        
        # For each query, find k nearest neighbors
        retrieval_scores = []
        
        for query_idx in query_indices:
            # Get k+1 nearest (including self)
            nearest_indices = np.argsort(distances[query_idx])[:k+1]
            
            # Exclude self
            nearest_indices = nearest_indices[nearest_indices != query_idx][:k]
            
            # Compute retrieval quality based on text similarity
            query_words = set(texts[query_idx].lower().split())
            
            overlaps = []
            for neighbor_idx in nearest_indices:
                neighbor_words = set(texts[neighbor_idx].lower().split())
                overlap = len(query_words & neighbor_words) / max(len(query_words | neighbor_words), 1)
                overlaps.append(overlap)
            
            # Mean overlap for this query
            retrieval_scores.append(np.mean(overlaps))
        
        return {
            'mean_retrieval_score': float(np.mean(retrieval_scores)),
            'std_retrieval_score': float(np.std(retrieval_scores)),
            'k': k
        }
    
    def compare_embeddings(
        self,
        embeddings_dict: Dict[str, np.ndarray],
        texts: List[str],
        true_labels: Optional[np.ndarray] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare multiple embedding methods.
        
        Args:
            embeddings_dict: Dictionary mapping method names to embedding matrices
            texts: Original texts
            true_labels: Optional ground truth labels
            
        Returns:
            Dictionary of results for each method
        """
        results = {}
        
        for method_name, embeddings in embeddings_dict.items():
            print(f"\nEvaluating {method_name}...")
            
            # Semantic similarity
            sim_metrics = self.evaluate_semantic_similarity(embeddings, texts)
            
            # Clustering
            cluster_metrics = self.evaluate_clustering(
                embeddings,
                true_labels=true_labels
            )
            
            # Retrieval
            retrieval_metrics = self.evaluate_retrieval(embeddings, texts)
            
            # Combine metrics
            results[method_name] = {
                **sim_metrics,
                **cluster_metrics,
                **retrieval_metrics,
                'n_dimensions': embeddings.shape[1],
                'compression_ratio': 768 / embeddings.shape[1]  # Assuming 768 as standard
            }
        
        return results
