#!/usr/bin/env python3
"""
Experimento QCAL - Standalone Demo
===================================

Demostración del experimento QCAL con capacidad de ejecutarse sin modelos externos.
Si SBERT/Word2Vec no están disponibles, muestra solo resultados QCAL.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import json
import time
from typing import List, Dict, Any
from datetime import datetime

# Import QCAL encoder
from qcal.text_encoder import QCALTextEncoder

# Import sklearn for metrics (always available)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize


# Subset of dataset for quick demo
DEMO_TEXTS = [
    # Physics (10 texts)
    "Quantum mechanics describes the behavior of matter and energy at atomic scales.",
    "Einstein's theory of relativity revolutionized our understanding of space and time.",
    "Gravitational waves are ripples in spacetime predicted by general relativity.",
    "Superposition allows quantum systems to exist in multiple states simultaneously.",
    "Entanglement creates correlations between particles that transcend classical physics.",
    
    # Mathematics (10 texts)
    "The Riemann hypothesis concerns the distribution of prime numbers.",
    "The golden ratio appears frequently in nature and mathematics.",
    "Differential equations model dynamic systems across sciences.",
    "Fractals exhibit self-similar patterns at different scales.",
    "Number theory investigates properties of integers and primes.",
    
    # Biology (10 texts)
    "DNA contains genetic instructions for all living organisms.",
    "Evolution by natural selection drives adaptation over generations.",
    "Photosynthesis converts light energy into chemical energy in plants.",
    "The nervous system coordinates responses to environmental stimuli.",
    "Mitochondria generate energy currency ATP through cellular respiration.",
    
    # Computer Science (10 texts)
    "Machine learning algorithms improve performance through experience.",
    "Neural networks mimic biological brain structure for pattern recognition.",
    "Algorithms are step-by-step procedures for solving computational problems.",
    "Cryptography secures communication through mathematical techniques.",
    "Artificial intelligence enables machines to simulate human cognition.",
    
    # General Knowledge (10 texts)
    "Climate change affects global weather patterns and ecosystems.",
    "Literature preserves cultural narratives across generations.",
    "Music combines rhythm, melody, and harmony to create art.",
    "Philosophy examines fundamental questions about existence and knowledge.",
    "Medicine applies scientific knowledge to maintain health and treat disease."
]


def evaluate_similarity(embeddings: np.ndarray) -> Dict[str, float]:
    """Evaluate similarity preservation."""
    embeddings_norm = normalize(embeddings)
    similarities = cosine_similarity(embeddings_norm)
    upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]
    
    return {
        'mean_similarity': float(np.mean(upper_triangle)),
        'std_similarity': float(np.std(upper_triangle)),
        'min_similarity': float(np.min(upper_triangle)),
        'max_similarity': float(np.max(upper_triangle))
    }


def evaluate_clustering(embeddings: np.ndarray, n_clusters: int = 5) -> Dict[str, float]:
    """Evaluate clustering quality."""
    embeddings_norm = normalize(embeddings)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings_norm)
    silhouette = silhouette_score(embeddings_norm, labels)
    
    return {
        'silhouette_score': float(silhouette),
        'inertia': float(kmeans.inertia_),
        'n_clusters': n_clusters
    }


def evaluate_retrieval(embeddings: np.ndarray, k: int = 5, texts: List[str] = None) -> Dict[str, float]:
    """Evaluate retrieval performance."""
    embeddings_norm = normalize(embeddings)
    similarities = cosine_similarity(embeddings_norm)
    
    precisions = []
    recalls = []
    
    for i in range(len(embeddings)):
        sims = similarities[i].copy()
        sims[i] = -np.inf
        top_k_indices = np.argsort(sims)[-k:][::-1]
        
        # Document category (5 docs per category in demo)
        query_category = i // 5
        relevant_docs = set(range(query_category * 5, min((query_category + 1) * 5, len(embeddings))))
        relevant_docs.discard(i)
        
        retrieved = set(top_k_indices)
        relevant_retrieved = retrieved & relevant_docs
        
        precision = len(relevant_retrieved) / k if k > 0 else 0
        recall = len(relevant_retrieved) / len(relevant_docs) if len(relevant_docs) > 0 else 0
        
        precisions.append(precision)
        recalls.append(recall)
    
    mean_p = np.mean(precisions)
    mean_r = np.mean(recalls)
    
    return {
        f'precision@{k}': float(mean_p),
        f'recall@{k}': float(mean_r),
        f'f1@{k}': float(2 * mean_p * mean_r / (mean_p + mean_r + 1e-8))
    }


def run_qcal_demo(texts: List[str] = DEMO_TEXTS):
    """Run QCAL encoding demo."""
    print("\n" + "="*70)
    print("DEMO: Experimento QCAL Text Encoding")
    print("="*70)
    print(f"Dataset: {len(texts)} textos")
    print(f"Fecha: {datetime.now().isoformat()}")
    
    # Test different dimensions
    dimensions_to_test = [16, 32, 64]
    
    results = {}
    
    for n_dim in dimensions_to_test:
        print(f"\n{'='*70}")
        print(f"QCAL Encoder - {n_dim} dimensiones")
        print(f"{'='*70}")
        
        start_time = time.time()
        encoder = QCALTextEncoder(n_dimensions=n_dim)
        embeddings = encoder.encode_batch(texts)
        encoding_time = time.time() - start_time
        
        print(f"✓ Encoded {len(texts)} texts in {encoding_time:.3f}s")
        print(f"✓ Embedding shape: {embeddings.shape}")
        print(f"✓ Memory usage: {embeddings.nbytes / 1024:.2f} KB")
        
        # Evaluate metrics
        sim_metrics = evaluate_similarity(embeddings)
        cluster_metrics = evaluate_clustering(embeddings, n_clusters=5)
        retrieval_metrics = evaluate_retrieval(embeddings, k=3, texts=texts)
        
        print(f"\nMétricas:")
        print(f"  Similitud - Media: {sim_metrics['mean_similarity']:.4f}, "
              f"Std: {sim_metrics['std_similarity']:.4f}")
        print(f"  Clustering - Silhouette: {cluster_metrics['silhouette_score']:.4f}")
        print(f"  Recuperación - P@3: {retrieval_metrics['precision@3']:.4f}, "
              f"R@3: {retrieval_metrics['recall@3']:.4f}, "
              f"F1@3: {retrieval_metrics['f1@3']:.4f}")
        
        results[f'QCAL-{n_dim}'] = {
            'n_dimensions': n_dim,
            'encoding_time': encoding_time,
            'memory_kb': embeddings.nbytes / 1024,
            'similarity': sim_metrics,
            'clustering': cluster_metrics,
            'retrieval': retrieval_metrics
        }
    
    # Print summary
    print(f"\n{'='*70}")
    print("RESUMEN COMPARATIVO - QCAL")
    print(f"{'='*70}")
    
    print(f"\n{'Dimensiones':<15} {'P@3':<10} {'Silhouette':<12} {'Tiempo(s)':<12} {'Memoria(KB)'}")
    print("-" * 70)
    
    for name, metrics in results.items():
        print(f"{metrics['n_dimensions']:<15} "
              f"{metrics['retrieval']['precision@3']:<10.4f} "
              f"{metrics['clustering']['silhouette_score']:<12.4f} "
              f"{metrics['encoding_time']:<12.3f} "
              f"{metrics['memory_kb']:<.2f}")
    
    # Efficiency analysis
    print(f"\n{'='*70}")
    print("ANÁLISIS DE EFICIENCIA")
    print(f"{'='*70}")
    
    if 'QCAL-32' in results and 'QCAL-64' in results:
        qcal32 = results['QCAL-32']
        qcal64 = results['QCAL-64']
        
        quality32 = (qcal32['retrieval']['precision@3'] + qcal32['clustering']['silhouette_score']) / 2
        quality64 = (qcal64['retrieval']['precision@3'] + qcal64['clustering']['silhouette_score']) / 2
        
        print(f"QCAL-32 logra {quality32/quality64*100:.1f}% de la calidad de QCAL-64")
        print(f"usando solo {32/64*100:.0f}% de las dimensiones")
        print(f"con {qcal32['memory_kb']/qcal64['memory_kb']*100:.0f}% del uso de memoria")
        
        # Comparison with typical SBERT dimensions
        print(f"\nComparación con SBERT (384 dims típico):")
        print(f"  QCAL-32 usa {32/384*100:.1f}% de las dimensiones")
        print(f"  Ratio de compresión: {384/32:.1f}x")
        print(f"  QCAL-64 usa {64/384*100:.1f}% de las dimensiones")
        print(f"  Ratio de compresión: {384/64:.1f}x")
    
    # Save results
    output_file = 'qcal_demo_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'n_texts': len(texts),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Resultados guardados en: {output_file}")
    
    return results


def main():
    """Main entry point."""
    run_qcal_demo()


if __name__ == '__main__':
    main()
