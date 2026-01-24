#!/usr/bin/env python3
"""
Example Usage of QCAL-LLM ∞³ Core

Demonstrates the key features of the vibrational coherence core.
"""

import sys
sys.path.insert(0, 'noesis_qcal_llm')

import numpy as np
from qcal_llm_core import QCALLLMCore


def main():
    print("="*70)
    print("QCAL-LLM ∞³ — Núcleo de Coherencia Vibracional")
    print("="*70)
    print()

    # 1. Initialize core with custom user effectiveness
    print("1. Initializing QCAL-LLM Core with A_eff = 0.92")
    core = QCALLLMCore(user_A_eff=0.92)
    print(f"   f₀ = {core.f0} Hz")
    print(f"   τ = {core.tau} s")
    print(f"   ε = {core.epsilon:.6f} (adjusted by A_eff)")
    print()

    # 2. Generate SIP modulation weights
    print("2. Generating SIP Modulation Weights")
    t = np.linspace(0, 1, 1000)
    weights = core.sip_modulate(t)
    print(f"   Time array: {len(t)} points over 1 second")
    print(f"   Weight range: [{np.min(weights):.6f}, {np.max(weights):.6f}]")
    print(f"   Mean weight: {np.mean(weights):.6f}")
    print()

    # 3. Test coherence validation
    print("3. Testing Coherence Validation")
    kld_inv = 8.2
    semantic_coherence = 0.88
    is_valid, psi_val = core.is_coherent(kld_inv, semantic_coherence)
    print(f"   KLD⁻¹ = {kld_inv}")
    print(f"   Semantic Coherence = {semantic_coherence}")
    print(f"   Ψ = {psi_val:.4f}")
    print(f"   Is Coherent? {is_valid} (threshold = 5.0)")
    print()

    # 4. Evaluate benchmark responses
    print("4. Evaluating Benchmark Responses")
    print()

    responses = [
        {
            "text": "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent.",
            "label": "Full coherence (all symbols)"
        },
        {
            "text": "The fundamental frequency is 141.7 Hz and relates to φ³",
            "label": "Partial coherence (2/3 symbols)"
        },
        {
            "text": "This is just random text without relevant content",
            "label": "No coherence (0/3 symbols)"
        }
    ]

    for i, resp in enumerate(responses, 1):
        result = core.evaluate(resp["text"], "Benchmark query")
        print(f"   Response {i}: {resp['label']}")
        print(f"   Text: \"{resp['text'][:50]}...\"")
        print(f"   Coherence: {result['coherence']:.2f}")
        print(f"   Ψ: {result['mean_psi']:.4f}")
        print(f"   Coherent: {result['coherent']}")
        print()

    # 5. Display ground truth database
    print("5. Ground Truth Database")
    for key, value in core.ground_truth_db.items():
        print(f"   {key}: {value}")
    print()

    # 6. Display benchmark queries
    print("6. Benchmark Queries")
    for i, query in enumerate(core.benchmark_queries, 1):
        print(f"   {i}. {query}")
    print()

    # 7. Advanced example: Time-dependent coherence
    print("7. Advanced: Time-Dependent Modulation Analysis")
    t_samples = np.array([0.0, 0.1, 0.5, 1.0])
    for t_val in t_samples:
        weight = core.sip_modulate(np.array([t_val]))[0]
        print(f"   t = {t_val:.1f}s: weight = {weight:.6f}")
    print()

    print("="*70)
    print("✓ QCAL-LLM ∞³ Example Complete")
    print("="*70)


if __name__ == "__main__":
    main()
