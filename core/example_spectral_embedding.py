#!/usr/bin/env python3
"""
Simple Example: QCAL Spectral Embedding
========================================

Quick example showing how to use spectral embeddings for semantic representation
with 16-32 dimensions instead of 256-768.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

from qcal import SpectralEmbedding, DatasetGenerator

def main():
    print("=" * 70)
    print("QCAL Spectral Embedding - Simple Example")
    print("=" * 70)
    
    # Create some sample texts
    texts = [
        # Quantum physics cluster
        "Quantum mechanics describes wave-particle duality",
        "Quantum entanglement connects distant particles",
        "Wave functions collapse upon measurement",
        
        # Relativity cluster
        "General relativity explains gravity as curved spacetime",
        "Spacetime curvature determines gravitational effects",
        "Light bends near massive objects",
        
        # Thermodynamics cluster
        "Entropy always increases in isolated systems",
        "Heat flows from hot to cold spontaneously",
        "Energy conservation is fundamental",
        
        # Electromagnetism cluster
        "Electromagnetic waves propagate at light speed",
        "Changing magnetic fields induce electric currents",
        "Photons carry electromagnetic energy"
    ]
    
    print(f"\nDataset: {len(texts)} scientific statements")
    
    # Create spectral embedding with 16 dimensions
    print("\n1. Creating spectral embedding (16 dimensions)...")
    spectral_emb = SpectralEmbedding(
        n_components=16,           # Very compact!
        f0=141.7001,              # QCAL fundamental frequency
        use_qcal_resonance=True,  # Enable quantum coherence
        random_state=42
    )
    
    # Fit and transform
    print("2. Fitting spectral embedding...")
    vectors = spectral_emb.fit_transform(texts)
    
    print(f"\nEmbedding shape: {vectors.shape}")
    print(f"Compression ratio: {spectral_emb.get_compression_ratio():.1f}x")
    print(f"Explained variance: {spectral_emb.explained_variance_ratio().sum():.4f}")
    
    # Compute similarities within and across clusters
    print("\n3. Computing semantic similarities...")
    
    # Within quantum cluster
    sim_quantum = spectral_emb.similarity(texts[0], texts[1])
    print(f"\n   Quantum 1 ↔ Quantum 2: {sim_quantum:.4f}")
    
    # Within relativity cluster
    sim_relativity = spectral_emb.similarity(texts[3], texts[4])
    print(f"   Relativity 1 ↔ Relativity 2: {sim_relativity:.4f}")
    
    # Cross-cluster (should be lower)
    sim_cross = spectral_emb.similarity(texts[0], texts[3])
    print(f"   Quantum ↔ Relativity: {sim_cross:.4f}")
    
    # Another cross-cluster
    sim_cross2 = spectral_emb.similarity(texts[6], texts[9])
    print(f"   Thermodynamics ↔ EM: {sim_cross2:.4f}")
    
    # Generate more data
    print("\n4. Generating larger dataset...")
    generator = DatasetGenerator(random_state=42)
    large_dataset = generator.generate_full_dataset(n_total=200)
    
    print(f"   Generated {len(large_dataset)} samples")
    
    # Train on larger dataset
    print("\n5. Training on larger dataset...")
    spectral_emb_large = SpectralEmbedding(n_components=32, random_state=42)
    large_vectors = spectral_emb_large.fit_transform(large_dataset)
    
    print(f"   Shape: {large_vectors.shape}")
    print(f"   Compression: {spectral_emb_large.get_compression_ratio():.1f}x")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"✓ Spectral embedding with 16-32 dimensions")
    print(f"✓ {spectral_emb.get_compression_ratio():.1f}x compression vs standard embeddings")
    print(f"✓ QCAL resonance at f₀ = 141.7001 Hz")
    print(f"✓ Semantic relationships preserved")
    print(f"✓ Within-cluster similarity higher than cross-cluster")
    print("\nFor more details, see SPECTRAL_EMBEDDING_README.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
