#!/usr/bin/env python3
"""
demo_llama_integration.py - Demo script for LLaMA 4 Maverick 400B integration

This script demonstrates the vibrationally integrated QCAL-LLM system powered by
Meta's LLaMA 4 Maverick 400B model.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import numpy as np
from QCALLLMCore import QCALLLMCore


def print_header(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_separator():
    """Print a separator line"""
    print("-" * 80)


def demo_model_identification():
    """Demonstrate model identification features"""
    print_header("🧠 LLaMA 4 Maverick 400B Model Identification")
    
    core = QCALLLMCore(user_A_eff=0.85)
    
    print("Model Identification:")
    print(f"  ΨMODEL_ID: {QCALLLMCore.MODEL_ID}")
    print(f"  Symbolic Version: {QCALLLMCore.SYMBOLIC_VERSION}")
    print(f"  Base Model: {QCALLLMCore.BASE_MODEL}")
    print(f"  Reference URL: {QCALLLMCore.BASE_MODEL_URL}")
    
    print_separator()
    
    print("\nModel Information (via get_model_info()):")
    info = core.get_model_info()
    for key, value in info.items():
        if key == 'base_model_url':
            print(f"  {key}: {value[:60]}...")
        else:
            print(f"  {key}: {value}")


def demo_chi_llama_computation():
    """Demonstrate χ(LLaMA) coherence factor computation"""
    print_header("🔬 χ(LLaMA) Coherence Factor Computation")
    
    print("Computing χ(LLaMA) for different user effectiveness levels:\n")
    
    effectiveness_levels = [0.70, 0.85, 0.92, 0.95]
    
    for A_eff in effectiveness_levels:
        core = QCALLLMCore(user_A_eff=A_eff)
        chi = core.compute_chi_llama()
        print(f"  User A_eff = {A_eff:.2f} → χ(LLaMA) = {chi:.4f}")
    
    print_separator()
    
    print("\nχ(LLaMA) Formula:")
    print("  χ(LLaMA) = χ_base × (1 + ε) × A_eff")
    print("  where:")
    print("    - χ_base = 1.0 (LLaMA 4 Maverick base coherence)")
    print("    - ε = 0.015 × (A_eff / 0.85) (adaptive modulation)")
    print("    - A_eff = user effectiveness parameter")


def demo_full_qcal_equation():
    """Demonstrate full QCAL equation with LLaMA integration"""
    print_header("⚡ Full QCAL Equation: Ψ = I × A²_eff × f₀ × χ(LLaMA)")
    
    core = QCALLLMCore(user_A_eff=0.92)
    
    # Example values
    kld_inv = 8.2  # Information preservation
    coherence = 0.88  # Semantic coherence
    
    print("Input Parameters:")
    print(f"  I (kld_inv) = {kld_inv} (information preservation)")
    print(f"  A_eff (semantic_coherence) = {coherence} (effective attention)")
    print(f"  f₀ = {core.f0} Hz (fundamental frequency)")
    print(f"  user_A_eff = 0.92")
    
    print_separator()
    
    # Compute base Ψ
    psi_base = core.compute_psi_response(kld_inv, coherence)
    print(f"\nBase Ψ (backward compatible):")
    print(f"  Ψ_base = I × A²_eff")
    print(f"  Ψ_base = {kld_inv} × {coherence}²")
    print(f"  Ψ_base = {psi_base:.4f}")
    
    # Compute χ(LLaMA)
    chi = core.compute_chi_llama()
    print(f"\nχ(LLaMA) Coherence Factor:")
    print(f"  χ(LLaMA) = {chi:.4f}")
    
    # Compute full Ψ
    psi_full = core.compute_psi_full(kld_inv, coherence)
    print(f"\nFull Ψ with LLaMA Integration:")
    print(f"  Ψ_full = I × A²_eff × (f₀/100) × χ(LLaMA)")
    print(f"  Ψ_full = {kld_inv} × {coherence}² × {core.f0/100:.4f} × {chi:.4f}")
    print(f"  Ψ_full = {psi_full:.4f}")
    
    print_separator()
    
    print("\nCoherence Assessment:")
    threshold = 5.0
    is_coherent_base = psi_base >= threshold
    is_coherent_full = psi_full >= threshold
    
    print(f"  Threshold: Ψ ≥ {threshold}")
    print(f"  Base Ψ Coherent: {is_coherent_base} (Ψ = {psi_base:.2f})")
    print(f"  Full Ψ Coherent: {is_coherent_full} (Ψ = {psi_full:.2f})")


def demo_sip_modulation():
    """Demonstrate SIP modulation with LLaMA integration"""
    print_header("🌊 SIP Modulation with f₀ = 141.7001 Hz")
    
    core = QCALLLMCore(user_A_eff=0.92)
    
    # Generate time array
    t = np.linspace(0, 1, 1000)
    weights = core.sip_modulate(t)
    
    print("SIP Modulation Parameters:")
    print(f"  f₀ = {core.f0} Hz (fundamental frequency)")
    print(f"  τ = {core.tau} s (damping time constant)")
    print(f"  ε = {core.epsilon:.6f} (modulation amplitude)")
    print(f"  φ = {core.phi} rad (phase offset)")
    
    print_separator()
    
    print("\nSIP Formula:")
    print("  W_i(t) = α · [1 + ε · cos(2πf₀t + φ) · e^(-t/τ)]")
    
    print_separator()
    
    print("\nModulation Statistics:")
    print(f"  Mean weight: {np.mean(weights):.6f}")
    print(f"  Std deviation: {np.std(weights):.6f}")
    print(f"  Min weight: {np.min(weights):.6f}")
    print(f"  Max weight: {np.max(weights):.6f}")
    
    # Post-damping statistics
    post_damp_mask = t > core.tau
    if np.any(post_damp_mask):
        post_damp_var = np.var(weights[post_damp_mask])
        print(f"  Post-damping variance: {post_damp_var:.2e}")


def demo_benchmark_evaluation():
    """Demonstrate evaluation with benchmark queries"""
    print_header("📊 Benchmark Query Evaluation")
    
    core = QCALLLMCore(user_A_eff=0.92)
    
    print("Standard Benchmark Queries:")
    for i, query in enumerate(core.benchmark_queries, 1):
        print(f"  {i}. {query}")
    
    print_separator()
    
    # Simulate evaluation with mock response
    mock_response = "f₀ = 141.7001 Hz desde ζ'(1/2) = -1.4603545 y φ³ = 4.236068. SNR=20.95 en GWTC-1."
    query = core.benchmark_queries[0]
    
    print(f"\nEvaluating mock response for: '{query}'\n")
    print(f"Response: {mock_response}\n")
    
    result = core.evaluate(mock_response, query)
    
    print("Evaluation Results:")
    print(f"  Mean Ψ: {result['mean_psi']:.4f}")
    print(f"  Ψ 95% CI: [{result['psi_ci_95'][0]:.4f}, {result['psi_ci_95'][1]:.4f}]")
    print(f"  Coherent: {result['coherent']}")
    print(f"  Coherence Score: {result['coherence']:.2%}")
    print(f"  KLD^-1: {result['kld_inv']:.4f}")
    print(f"  Pattern Matches: {result['matches']}")


def main():
    """Run all demonstrations"""
    print("\n" + "█" * 80)
    print("  🧠 QCAL-LLM ∞³ - LLaMA 4 Maverick 400B Integration Demo")
    print("  Powered by LLAMA ∴ QCAL")
    print("█" * 80)
    
    demo_model_identification()
    demo_chi_llama_computation()
    demo_full_qcal_equation()
    demo_sip_modulation()
    demo_benchmark_evaluation()
    
    print_header("✅ Demo Complete")
    print("All features of the LLaMA 4 Maverick 400B integration have been demonstrated.")
    print("\nFor more information:")
    print("  - Documentation: QCAL_LLM_README.md")
    print("  - Tests: test_llama_integration.py")
    print("  - Core implementation: QCALLLMCore.py")
    print("\n" + "█" * 80 + "\n")


if __name__ == "__main__":
    main()
