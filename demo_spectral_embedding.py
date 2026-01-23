#!/usr/bin/env python3
"""
QCAL Spectral Embedding Demonstration
======================================

Demonstrates the spectral embedding approach for semantic representation
with 16-32 dimensions achieving comparable results to 256-768 dimensional
standard embeddings.

This script:
1. Generates a dataset of 100-1000 short phrases
2. Trains spectral embedding (QCAL-inspired) with 16-32 dimensions
3. Trains baseline embeddings (TF-IDF+SVD, Word2Vec) with 256-768 dimensions
4. Compares performance on:
   - Semantic similarity preservation
   - Clustering coherence
   - Meaning retrieval

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import json
from typing import Dict, Any

# Import QCAL modules
from qcal import (
    SpectralEmbedding,
    DatasetGenerator,
    BaselineEmbedding,
    EmbeddingEvaluator
)

# Try to import Word2Vec if available
try:
    from qcal import Word2VecEmbedding
    WORD2VEC_AVAILABLE = True
except ImportError:
    WORD2VEC_AVAILABLE = False
    print("Note: gensim not available, Word2Vec baseline will be skipped")


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")


def print_metrics(method_name: str, metrics: Dict[str, float]):
    """Print metrics in formatted way."""
    print(f"\n{method_name}:")
    print("-" * 60)
    for key, value in sorted(metrics.items()):
        if isinstance(value, float):
            print(f"  {key:30s}: {value:8.4f}")
        else:
            print(f"  {key:30s}: {value}")
    print()


def main():
    """Run spectral embedding demonstration."""
    
    print_header("QCAL Spectral Embedding Demonstration")
    
    # Configuration
    dataset_size = 500
    spectral_dims = 32
    baseline_dims = 256
    random_state = 42
    
    print(f"Configuration:")
    print(f"  Dataset size: {dataset_size}")
    print(f"  Spectral embedding dimensions: {spectral_dims}")
    print(f"  Baseline embedding dimensions: {baseline_dims}")
    print(f"  Random state: {random_state}")
    
    # Step 1: Generate dataset
    print_header("Step 1: Generating Dataset")
    
    generator = DatasetGenerator(random_state=random_state)
    
    # Generate full dataset
    print(f"Generating {dataset_size} samples...")
    texts = generator.generate_full_dataset(n_total=dataset_size)
    
    print(f"Generated {len(texts)} text samples")
    print("\nSample texts:")
    for i, text in enumerate(texts[:5]):
        print(f"  {i+1}. {text}")
    
    # Generate semantic clusters for evaluation
    print("\nGenerating semantic clusters for evaluation...")
    clusters = generator.generate_semantic_clusters(n_clusters=5, samples_per_cluster=20)
    
    # Create labels
    cluster_texts = []
    cluster_labels = []
    for idx, (cluster_name, cluster_samples) in enumerate(clusters.items()):
        cluster_texts.extend(cluster_samples)
        cluster_labels.extend([idx] * len(cluster_samples))
    
    cluster_labels = np.array(cluster_labels)
    print(f"Generated {len(cluster_texts)} clustered samples in {len(clusters)} clusters")
    
    # Step 2: Train embeddings
    print_header("Step 2: Training Embeddings")
    
    # Spectral embedding (QCAL)
    print("Training Spectral Embedding (QCAL)...")
    spectral_emb = SpectralEmbedding(
        n_components=spectral_dims,
        use_qcal_resonance=True,
        random_state=random_state
    )
    spectral_vectors = spectral_emb.fit_transform(texts)
    print(f"  Shape: {spectral_vectors.shape}")
    print(f"  Compression ratio: {spectral_emb.get_compression_ratio():.2f}x")
    print(f"  Explained variance: {spectral_emb.explained_variance_ratio().sum():.4f}")
    
    # Baseline embedding (TF-IDF + SVD)
    print("\nTraining Baseline Embedding (TF-IDF+SVD)...")
    baseline_emb = BaselineEmbedding(
        n_components=baseline_dims,
        random_state=random_state
    )
    baseline_vectors = baseline_emb.fit_transform(texts)
    print(f"  Shape: {baseline_vectors.shape}")
    
    # Word2Vec if available
    embeddings_dict = {
        'Spectral-32D': spectral_vectors,
        'Baseline-256D': baseline_vectors
    }
    
    if WORD2VEC_AVAILABLE:
        print("\nTraining Word2Vec Embedding...")
        word2vec_emb = Word2VecEmbedding(
            vector_size=baseline_dims,
            random_state=random_state
        )
        word2vec_vectors = word2vec_emb.fit_transform(texts)
        print(f"  Shape: {word2vec_vectors.shape}")
        embeddings_dict['Word2Vec-256D'] = word2vec_vectors
    
    # Step 3: Evaluate on full dataset
    print_header("Step 3: Evaluation on Full Dataset")
    
    evaluator = EmbeddingEvaluator(random_state=random_state)
    results = evaluator.compare_embeddings(embeddings_dict, texts)
    
    for method_name, metrics in results.items():
        print_metrics(method_name, metrics)
    
    # Step 4: Evaluate on clustered data
    print_header("Step 4: Evaluation on Clustered Data")
    
    # Get embeddings for clustered texts
    spectral_cluster_vectors = spectral_emb.transform(cluster_texts)
    baseline_cluster_vectors = baseline_emb.transform(cluster_texts)
    
    cluster_embeddings_dict = {
        'Spectral-32D': spectral_cluster_vectors,
        'Baseline-256D': baseline_cluster_vectors
    }
    
    if WORD2VEC_AVAILABLE:
        word2vec_cluster_vectors = word2vec_emb.transform(cluster_texts)
        cluster_embeddings_dict['Word2Vec-256D'] = word2vec_cluster_vectors
    
    cluster_results = evaluator.compare_embeddings(
        cluster_embeddings_dict,
        cluster_texts,
        true_labels=cluster_labels
    )
    
    for method_name, metrics in cluster_results.items():
        print_metrics(method_name, metrics)
    
    # Step 5: Comparative analysis
    print_header("Step 5: Comparative Analysis")
    
    print("Performance Comparison (Spectral vs Baseline):")
    print("-" * 60)
    
    spectral_metrics = results['Spectral-32D']
    baseline_metrics = results['Baseline-256D']
    
    key_metrics = [
        ('similarity_correlation', 'Semantic Similarity Correlation'),
        ('silhouette_score', 'Clustering Silhouette Score'),
        ('mean_retrieval_score', 'Mean Retrieval Score'),
    ]
    
    print(f"\n{'Metric':<35} {'Spectral-32D':>12} {'Baseline-256D':>15} {'Ratio':>10}")
    print("-" * 75)
    
    for metric_key, metric_name in key_metrics:
        spectral_val = spectral_metrics.get(metric_key, 0.0)
        baseline_val = baseline_metrics.get(metric_key, 0.0)
        ratio = spectral_val / baseline_val if baseline_val != 0 else 0.0
        
        print(f"{metric_name:<35} {spectral_val:>12.4f} {baseline_val:>15.4f} {ratio:>10.2f}x")
    
    # Dimensionality comparison
    print("\n" + "-" * 75)
    print(f"{'Dimensionality':<35} {spectral_dims:>12d} {baseline_dims:>15d}")
    print(f"{'Compression ratio':<35} {baseline_dims/spectral_dims:>12.2f}x {1.0:>15.2f}x")
    
    # Step 6: Save results
    print_header("Step 6: Saving Results")
    
    output_file = "spectral_embedding_results.json"
    
    output_data = {
        'configuration': {
            'dataset_size': dataset_size,
            'spectral_dims': spectral_dims,
            'baseline_dims': baseline_dims,
            'random_state': random_state
        },
        'full_dataset_results': results,
        'clustered_data_results': cluster_results,
        'summary': {
            'spectral_compression': baseline_dims / spectral_dims,
            'performance_ratios': {
                metric_key: spectral_metrics.get(metric_key, 0.0) / baseline_metrics.get(metric_key, 1.0)
                for metric_key, _ in key_metrics
            }
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Results saved to {output_file}")
    
    # Final summary
    print_header("Summary")
    
    print("✓ Spectral embedding with 32 dimensions demonstrated")
    print(f"✓ Achieved {baseline_dims/spectral_dims:.1f}x compression vs baseline")
    print(f"✓ Semantic similarity correlation: {spectral_metrics['similarity_correlation']:.4f}")
    print(f"✓ Clustering silhouette score: {spectral_metrics['silhouette_score']:.4f}")
    print(f"✓ Mean retrieval score: {spectral_metrics['mean_retrieval_score']:.4f}")
    
    # Performance ratio
    avg_performance_ratio = np.mean([
        spectral_metrics.get(mk, 0.0) / baseline_metrics.get(mk, 1.0)
        for mk, _ in key_metrics
    ])
    
    print(f"\nAverage performance ratio: {avg_performance_ratio:.2f}x")
    
    if avg_performance_ratio > 0.8:
        print("\n✓ SUCCESS: Spectral embedding achieves comparable results with 8x fewer dimensions!")
    else:
        print(f"\n⚠ Note: Performance ratio is {avg_performance_ratio:.2f}x (target: >0.8x)")


if __name__ == "__main__":
    main()
