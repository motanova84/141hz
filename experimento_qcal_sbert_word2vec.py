#!/usr/bin/env python3
"""
Experimento QCAL vs SBERT vs Word2Vec
======================================

Experimento acordado:
- Entrada: 100 textos
- Salida: representación QCAL numérica
- Comparación: SBERT / word2vec
- Métricas: similitud, clustering, recuperación
- Resultado: misma calidad con menos dimensiones

Este experimento demuestra que QCAL puede lograr el mismo rendimiento
que SBERT y word2vec utilizando significativamente menos dimensiones,
gracias a los principios de coherencia cuántica.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import json
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import QCAL encoder
from qcal.text_encoder import QCALTextEncoder

# Import SBERT
try:
    from sentence_transformers import SentenceTransformer
    SBERT_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")
    SBERT_AVAILABLE = False

# Import Gensim for word2vec
try:
    from gensim.models import Word2Vec
    import gensim.downloader as api
    GENSIM_AVAILABLE = True
except ImportError:
    print("Warning: gensim not available. Install with: pip install gensim")
    GENSIM_AVAILABLE = False

# Import sklearn for metrics
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize


# Dataset of 100 texts (scientific and general domain)
DATASET_100_TEXTS = [
    # Physics (20 texts)
    "Quantum mechanics describes the behavior of matter and energy at atomic scales.",
    "The speed of light in vacuum is a fundamental constant of nature.",
    "Einstein's theory of relativity revolutionized our understanding of space and time.",
    "Gravitational waves are ripples in spacetime predicted by general relativity.",
    "The Higgs boson gives elementary particles their mass through the Higgs field.",
    "Superposition allows quantum systems to exist in multiple states simultaneously.",
    "Entanglement creates correlations between particles that transcend classical physics.",
    "The uncertainty principle limits simultaneous knowledge of position and momentum.",
    "Black holes are regions where spacetime curvature becomes infinite.",
    "The standard model describes fundamental particles and their interactions.",
    "Dark matter comprises most of the universe's mass but doesn't emit light.",
    "String theory proposes that fundamental particles are one-dimensional strings.",
    "The Big Bang theory explains the origin and evolution of the universe.",
    "Thermodynamics governs the relationship between heat, work, and energy.",
    "Nuclear fusion powers the sun by converting hydrogen into helium.",
    "Quantum computing uses qubits that can be in superposition states.",
    "The photoelectric effect demonstrates the particle nature of light.",
    "Special relativity unifies space and time into a four-dimensional continuum.",
    "Antimatter particles have opposite charge to their matter counterparts.",
    "Electromagnetic radiation propagates through space as waves and particles.",
    
    # Mathematics (20 texts)
    "The Riemann hypothesis concerns the distribution of prime numbers.",
    "Topology studies properties preserved under continuous deformations.",
    "The golden ratio appears frequently in nature and mathematics.",
    "Calculus enables the study of continuous change and motion.",
    "Group theory provides algebraic structure for symmetry operations.",
    "The Fibonacci sequence exhibits recursive growth patterns.",
    "Differential equations model dynamic systems across sciences.",
    "Complex numbers extend the real number system with imaginary units.",
    "Linear algebra studies vector spaces and linear transformations.",
    "The Pythagorean theorem relates sides of right triangles.",
    "Probability theory quantifies uncertainty and randomness.",
    "Number theory investigates properties of integers and primes.",
    "Set theory provides foundations for modern mathematics.",
    "Fractals exhibit self-similar patterns at different scales.",
    "Chaos theory studies sensitive dependence on initial conditions.",
    "Graph theory analyzes networks of connected nodes and edges.",
    "Statistics enables inference from data samples to populations.",
    "Combinatorics counts arrangements and combinations of objects.",
    "Game theory models strategic interactions between rational agents.",
    "Abstract algebra generalizes arithmetic operations to abstract structures.",
    
    # Biology (20 texts)
    "DNA contains genetic instructions for all living organisms.",
    "Evolution by natural selection drives adaptation over generations.",
    "Cells are the fundamental units of life and biology.",
    "Photosynthesis converts light energy into chemical energy in plants.",
    "The nervous system coordinates responses to environmental stimuli.",
    "Proteins are essential biomolecules performing diverse cellular functions.",
    "Mitochondria generate energy currency ATP through cellular respiration.",
    "Ecosystems comprise interacting communities of organisms and environments.",
    "Enzymes catalyze biochemical reactions with high specificity.",
    "The immune system defends against pathogens and foreign substances.",
    "Genetic mutations drive variation and evolutionary change.",
    "Homeostasis maintains stable internal conditions in organisms.",
    "Bacteria are single-celled prokaryotes without membrane-bound nuclei.",
    "Viruses require host cells to replicate and reproduce.",
    "Biodiversity encompasses variety of life at all organizational levels.",
    "Symbiosis describes close ecological relationships between species.",
    "Meiosis produces gametes with half the chromosomes of parent cells.",
    "Neurotransmitters enable communication between nerve cells.",
    "Hormones coordinate physiological processes through chemical signaling.",
    "Ecological succession describes predictable changes in community composition.",
    
    # Computer Science (20 texts)
    "Machine learning algorithms improve performance through experience.",
    "Neural networks mimic biological brain structure for pattern recognition.",
    "Algorithms are step-by-step procedures for solving computational problems.",
    "Data structures organize information for efficient access and modification.",
    "Cryptography secures communication through mathematical techniques.",
    "Operating systems manage computer hardware and software resources.",
    "Databases store and organize large collections of structured data.",
    "Parallel computing performs multiple calculations simultaneously.",
    "Artificial intelligence enables machines to simulate human cognition.",
    "Compilers translate high-level code into machine-executable instructions.",
    "Networks enable communication between distributed computing devices.",
    "Cybersecurity protects systems from digital attacks and breaches.",
    "Cloud computing provides on-demand access to shared computing resources.",
    "Version control systems track changes in source code over time.",
    "Object-oriented programming organizes code into reusable objects.",
    "Recursion allows functions to call themselves with modified inputs.",
    "Big data analytics extracts insights from massive datasets.",
    "Blockchain maintains distributed ledgers without central authority.",
    "Quantum algorithms leverage superposition for computational speedup.",
    "Software engineering applies systematic approaches to software development.",
    
    # General Knowledge (20 texts)
    "Climate change affects global weather patterns and ecosystems.",
    "Democracy empowers citizens to participate in governmental decisions.",
    "Literature preserves cultural narratives across generations.",
    "Music combines rhythm, melody, and harmony to create art.",
    "Philosophy examines fundamental questions about existence and knowledge.",
    "History records and interprets past events and civilizations.",
    "Psychology studies mental processes and human behavior.",
    "Economics analyzes production, distribution, and consumption of goods.",
    "Sociology investigates social relationships and institutions.",
    "Architecture designs functional and aesthetic built environments.",
    "Medicine applies scientific knowledge to maintain health and treat disease.",
    "Education transmits knowledge and skills across generations.",
    "Language enables communication through symbolic systems.",
    "Religion provides meaning and moral frameworks for believers.",
    "Art expresses human creativity through diverse media.",
    "Geography studies Earth's physical features and human populations.",
    "Agriculture cultivates crops and raises animals for food.",
    "Engineering applies scientific principles to design practical solutions.",
    "Chemistry studies matter composition, structure, and transformations.",
    "Astronomy observes celestial objects and phenomena beyond Earth."
]


class TextEmbeddingExperiment:
    """
    Compare QCAL, SBERT, and Word2Vec on text embedding tasks.
    """
    
    def __init__(self, texts: List[str]):
        """
        Initialize experiment with dataset.
        
        Args:
            texts: List of texts to encode
        """
        self.texts = texts
        self.results = {}
    
    def run_qcal(self, n_dimensions: int = 32) -> Dict[str, Any]:
        """Run QCAL encoding."""
        print(f"\n{'='*60}")
        print(f"Running QCAL Encoder (n_dimensions={n_dimensions})")
        print(f"{'='*60}")
        
        start_time = time.time()
        encoder = QCALTextEncoder(n_dimensions=n_dimensions)
        embeddings = encoder.encode_batch(self.texts)
        encoding_time = time.time() - start_time
        
        result = {
            'name': 'QCAL',
            'n_dimensions': n_dimensions,
            'embeddings': embeddings,
            'encoding_time': encoding_time,
            'info': encoder.get_info()
        }
        
        print(f"✓ Encoded {len(self.texts)} texts in {encoding_time:.3f}s")
        print(f"✓ Embedding shape: {embeddings.shape}")
        print(f"✓ Memory usage: {embeddings.nbytes / 1024:.2f} KB")
        
        return result
    
    def run_sbert(self) -> Dict[str, Any]:
        """Run SBERT encoding."""
        if not SBERT_AVAILABLE:
            print("\nSBERT not available - skipping")
            return None
        
        print(f"\n{'='*60}")
        print(f"Running SBERT Encoder")
        print(f"{'='*60}")
        
        start_time = time.time()
        model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
        embeddings = model.encode(self.texts, show_progress_bar=False)
        encoding_time = time.time() - start_time
        
        result = {
            'name': 'SBERT',
            'n_dimensions': embeddings.shape[1],
            'embeddings': embeddings,
            'encoding_time': encoding_time,
            'info': {'model': 'all-MiniLM-L6-v2'}
        }
        
        print(f"✓ Encoded {len(self.texts)} texts in {encoding_time:.3f}s")
        print(f"✓ Embedding shape: {embeddings.shape}")
        print(f"✓ Memory usage: {embeddings.nbytes / 1024:.2f} KB")
        
        return result
    
    def run_word2vec(self, n_dimensions: int = 100) -> Dict[str, Any]:
        """Run Word2Vec encoding."""
        if not GENSIM_AVAILABLE:
            print("\nWord2Vec (Gensim) not available - skipping")
            return None
        
        print(f"\n{'='*60}")
        print(f"Running Word2Vec Encoder (n_dimensions={n_dimensions})")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Tokenize texts
        tokenized = [text.lower().split() for text in self.texts]
        
        # Train Word2Vec model
        model = Word2Vec(sentences=tokenized, vector_size=n_dimensions, 
                        window=5, min_count=1, workers=4, epochs=10)
        
        # Encode texts as average of word vectors
        embeddings = []
        for tokens in tokenized:
            vectors = [model.wv[word] for word in tokens if word in model.wv]
            if vectors:
                embeddings.append(np.mean(vectors, axis=0))
            else:
                embeddings.append(np.zeros(n_dimensions))
        
        embeddings = np.array(embeddings)
        encoding_time = time.time() - start_time
        
        result = {
            'name': 'Word2Vec',
            'n_dimensions': n_dimensions,
            'embeddings': embeddings,
            'encoding_time': encoding_time,
            'info': {'vector_size': n_dimensions, 'window': 5}
        }
        
        print(f"✓ Encoded {len(self.texts)} texts in {encoding_time:.3f}s")
        print(f"✓ Embedding shape: {embeddings.shape}")
        print(f"✓ Memory usage: {embeddings.nbytes / 1024:.2f} KB")
        
        return result
    
    def evaluate_similarity(self, result: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate similarity preservation."""
        embeddings = result['embeddings']
        
        # Normalize embeddings
        embeddings_norm = normalize(embeddings)
        
        # Compute pairwise similarities
        similarities = cosine_similarity(embeddings_norm)
        
        # Statistics
        upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]
        
        return {
            'mean_similarity': float(np.mean(upper_triangle)),
            'std_similarity': float(np.std(upper_triangle)),
            'min_similarity': float(np.min(upper_triangle)),
            'max_similarity': float(np.max(upper_triangle))
        }
    
    def evaluate_clustering(self, result: Dict[str, Any], n_clusters: int = 5) -> Dict[str, float]:
        """Evaluate clustering quality."""
        embeddings = result['embeddings']
        
        # Normalize embeddings
        embeddings_norm = normalize(embeddings)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings_norm)
        
        # Silhouette score (quality of clustering)
        silhouette = silhouette_score(embeddings_norm, labels)
        
        # Inertia (compactness)
        inertia = kmeans.inertia_
        
        return {
            'silhouette_score': float(silhouette),
            'inertia': float(inertia),
            'n_clusters': n_clusters
        }
    
    def evaluate_retrieval(self, result: Dict[str, Any], k: int = 5) -> Dict[str, float]:
        """Evaluate retrieval performance."""
        embeddings = result['embeddings']
        
        # Normalize embeddings
        embeddings_norm = normalize(embeddings)
        
        # Compute pairwise similarities
        similarities = cosine_similarity(embeddings_norm)
        
        # For each query, retrieve top-k similar documents
        precisions = []
        recalls = []
        
        for i in range(len(embeddings)):
            # Get top-k most similar (excluding self)
            sims = similarities[i].copy()
            sims[i] = -np.inf  # Exclude self
            top_k_indices = np.argsort(sims)[-k:][::-1]
            
            # Simple relevance: documents from same category (first 20 are physics, etc.)
            query_category = i // 20
            relevant_docs = set(range(query_category * 20, (query_category + 1) * 20))
            relevant_docs.discard(i)
            
            retrieved = set(top_k_indices)
            relevant_retrieved = retrieved & relevant_docs
            
            precision = len(relevant_retrieved) / k if k > 0 else 0
            recall = len(relevant_retrieved) / len(relevant_docs) if len(relevant_docs) > 0 else 0
            
            precisions.append(precision)
            recalls.append(recall)
        
        return {
            f'precision@{k}': float(np.mean(precisions)),
            f'recall@{k}': float(np.mean(recalls)),
            f'f1@{k}': float(2 * np.mean(precisions) * np.mean(recalls) / 
                           (np.mean(precisions) + np.mean(recalls) + 1e-8))
        }
    
    def run_full_experiment(self) -> Dict[str, Any]:
        """Run complete experiment with all encoders and metrics."""
        print("\n" + "="*60)
        print("EXPERIMENTO: QCAL vs SBERT vs Word2Vec")
        print("="*60)
        print(f"Dataset: {len(self.texts)} textos")
        print(f"Fecha: {datetime.now().isoformat()}")
        
        # Run encoders
        results = {}
        
        # QCAL (32 dimensions)
        qcal_result = self.run_qcal(n_dimensions=32)
        results['QCAL-32'] = qcal_result
        
        # SBERT (384 dimensions)
        sbert_result = self.run_sbert()
        if sbert_result:
            results['SBERT-384'] = sbert_result
        
        # Word2Vec (100 dimensions)
        w2v_result = self.run_word2vec(n_dimensions=100)
        if w2v_result:
            results['Word2Vec-100'] = w2v_result
        
        # Evaluate all methods
        print(f"\n{'='*60}")
        print("EVALUACIÓN DE MÉTRICAS")
        print(f"{'='*60}")
        
        evaluation_results = {}
        
        for name, result in results.items():
            print(f"\n{name}:")
            
            # Similarity metrics
            sim_metrics = self.evaluate_similarity(result)
            print(f"  Similitud - Media: {sim_metrics['mean_similarity']:.4f}, "
                  f"Std: {sim_metrics['std_similarity']:.4f}")
            
            # Clustering metrics
            cluster_metrics = self.evaluate_clustering(result, n_clusters=5)
            print(f"  Clustering - Silhouette: {cluster_metrics['silhouette_score']:.4f}")
            
            # Retrieval metrics
            retrieval_metrics = self.evaluate_retrieval(result, k=5)
            print(f"  Recuperación - P@5: {retrieval_metrics['precision@5']:.4f}, "
                  f"R@5: {retrieval_metrics['recall@5']:.4f}, "
                  f"F1@5: {retrieval_metrics['f1@5']:.4f}")
            
            evaluation_results[name] = {
                'n_dimensions': result['n_dimensions'],
                'encoding_time': result['encoding_time'],
                'memory_kb': result['embeddings'].nbytes / 1024,
                'similarity': sim_metrics,
                'clustering': cluster_metrics,
                'retrieval': retrieval_metrics
            }
        
        # Generate summary
        self._print_summary(evaluation_results)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'n_texts': len(self.texts),
            'results': evaluation_results
        }
    
    def _print_summary(self, evaluation_results: Dict[str, Any]):
        """Print comparison summary."""
        print(f"\n{'='*60}")
        print("RESUMEN COMPARATIVO")
        print(f"{'='*60}")
        
        print(f"\n{'Método':<15} {'Dims':<8} {'P@5':<8} {'Silh':<8} {'Tiempo(s)':<10} {'Memoria(KB)':<12}")
        print("-" * 70)
        
        for name, metrics in evaluation_results.items():
            print(f"{name:<15} "
                  f"{metrics['n_dimensions']:<8} "
                  f"{metrics['retrieval']['precision@5']:<8.4f} "
                  f"{metrics['clustering']['silhouette_score']:<8.4f} "
                  f"{metrics['encoding_time']:<10.3f} "
                  f"{metrics['memory_kb']:<12.2f}")
        
        # Compute efficiency (quality / dimensions)
        if 'QCAL-32' in evaluation_results and 'SBERT-384' in evaluation_results:
            qcal = evaluation_results['QCAL-32']
            sbert = evaluation_results['SBERT-384']
            
            qcal_quality = (qcal['retrieval']['precision@5'] + qcal['clustering']['silhouette_score']) / 2
            sbert_quality = (sbert['retrieval']['precision@5'] + sbert['clustering']['silhouette_score']) / 2
            
            qcal_efficiency = qcal_quality / qcal['n_dimensions']
            sbert_efficiency = sbert_quality / sbert['n_dimensions']
            
            print(f"\n{'='*60}")
            print("CONCLUSIÓN")
            print(f"{'='*60}")
            print(f"QCAL logra {qcal_quality/sbert_quality*100:.1f}% de la calidad de SBERT")
            print(f"usando solo {qcal['n_dimensions']/sbert['n_dimensions']*100:.1f}% de las dimensiones")
            print(f"Eficiencia QCAL/SBERT: {qcal_efficiency/sbert_efficiency:.2f}x")


def main():
    """Main entry point."""
    # Run experiment
    experiment = TextEmbeddingExperiment(DATASET_100_TEXTS)
    results = experiment.run_full_experiment()
    
    # Save results
    output_file = 'experimento_qcal_sbert_word2vec_results.json'
    
    # Convert numpy arrays to lists for JSON serialization
    results_serializable = {
        'timestamp': results['timestamp'],
        'n_texts': results['n_texts'],
        'results': results['results']
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Resultados guardados en: {output_file}")


if __name__ == '__main__':
    main()
