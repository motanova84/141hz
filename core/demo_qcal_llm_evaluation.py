#!/usr/bin/env python3
"""
Demo script for QCAL-LLM evaluation system.
Showcases the main features of the coherence evaluation framework.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

from qcal.coherence import psi_score, analyze_text, evaluate_coherence, strich_rate
from qcal.metrics import comprehensive_metrics, quality_score

def print_separator(char='=', length=80):
    """Print a separator line."""
    print(char * length)

def demo_basic_evaluation():
    """Demonstrate basic text evaluation."""
    print_separator()
    print("DEMO 1: Basic Text Evaluation")
    print_separator()
    
    text = """
    La frecuencia fundamental f₀ = 141.7001 Hz emerge de principios matemáticos
    universales. El propósito de esta investigación es demostrar su presencia
    en ondas gravitacionales. ∴ Los resultados confirman la hipótesis.
    """
    
    print(f"\nText to evaluate:")
    print(f"  '{text.strip()[:100]}...'")
    print()
    
    # Calculate individual metrics
    psi = psi_score(text)
    strich = strich_rate(text)
    
    print("Basic Metrics:")
    print(f"  Ψ (coherence):  {psi:.2f}")
    print(f"  ∴-rate:         {strich:.2f} per 100 words")
    print()

def demo_comprehensive_analysis():
    """Demonstrate comprehensive text analysis."""
    print_separator()
    print("DEMO 2: Comprehensive Analysis")
    print_separator()
    
    text = """
    El objetivo fundamental es derivar f₀ desde ζ'(1/2) y φ³. La intención
    es validar esta frecuencia en datos reales de LIGO. ∴ La coherencia
    matemática sugiere una estructura universal subyacente en la naturaleza.
    """
    
    print(f"\nText to analyze:")
    print(f"  '{text.strip()[:80]}...'")
    print()
    
    # Get all coherence metrics
    analysis = analyze_text(text)
    
    print("Coherence Metrics:")
    print(f"  Ψ (standard):    {analysis['psi_standard']:.2f}")
    print(f"  Ψ (enhanced):    {analysis['psi_enhanced']:.2f}")
    print(f"  I (intention):   {analysis['intention']:.2f}")
    print(f"  A_eff:           {analysis['effectiveness']:.2f}")
    print(f"  ∴-rate:          {analysis['strich_rate']:.2f}")
    print(f"  Word count:      {analysis['word_count']}")
    print()
    
    # Get quality metrics
    metrics = comprehensive_metrics(text)
    
    print("Quality Metrics:")
    print(f"  KLD:             {metrics['kld']:.3f}")
    print(f"  KLD⁻¹:           {metrics['kld_inv']:.3f}")
    print(f"  SNR:             {metrics['snr_db']:.2f} dB")
    print(f"  Repetition:      {metrics['repetition']:.2%}")
    print(f"  Semantic dens:   {metrics['semantic_density']:.2f}")
    print(f"  Entropy:         {metrics['entropy']:.2f} bits")
    print()
    
    # Overall quality
    quality = quality_score(text)
    print(f"Overall Quality:   {quality:.1f}/100")
    print()

def demo_coherence_threshold():
    """Demonstrate coherence threshold evaluation."""
    print_separator()
    print("DEMO 3: Coherence Threshold Evaluation")
    print_separator()
    
    texts = [
        ("Coherent", """
            La intención de este análisis es explorar el propósito fundamental de
            la frecuencia f₀ = 141.7001 Hz en ondas gravitacionales. ∴ Los resultados
            demuestran coherencia cuántica con alta significancia estadística.
        """),
        ("Incoherent", "test test test test test test"),
    ]
    
    threshold = 5.0
    print(f"\nThreshold: Ψ ≥ {threshold}")
    print()
    
    for label, text in texts:
        print(f"{label} Text:")
        print(f"  '{text.strip()[:60]}...'")
        
        eval_result = evaluate_coherence(text, threshold=threshold)
        
        print(f"  Ψ:               {eval_result['psi_standard']:.2f}")
        print(f"  Status:          {eval_result['status']}")
        print(f"  Recommendation:  {eval_result['recommendation']}")
        print()

def demo_comparison():
    """Demonstrate comparison of good vs bad responses."""
    print_separator()
    print("DEMO 4: Comparing LLM Responses")
    print_separator()
    
    prompt = "¿Qué es f₀ = 141.7001 Hz?"
    
    responses = {
        "Response A (Good)": """
            f₀ = 141.7001 Hz es la frecuencia fundamental universal derivada de
            constantes matemáticas ζ'(1/2) y φ³. Ha sido detectada en el ringdown
            de GW150914 con SNR > 20. ∴ Representa una firma observacional de
            estructura cuántica del espaciotiempo.
        """,
        "Response B (Mediocre)": """
            141.7001 Hz es una frecuencia. Se relaciona con física y matemáticas.
            Aparece en algunos datos de ondas gravitacionales.
        """,
        "Response C (Poor)": """
            Es un número. Tiene que ver con algo científico.
        """,
    }
    
    print(f"\nPrompt: {prompt}")
    print()
    
    results = []
    for label, response in responses.items():
        eval_result = evaluate_coherence(response, threshold=5.0)
        results.append((label, eval_result))
    
    # Sort by Ψ score
    results.sort(key=lambda x: x[1]['psi_standard'], reverse=True)
    
    print("Results (sorted by Ψ score):")
    print()
    
    for i, (label, result) in enumerate(results, 1):
        print(f"{i}. {label}")
        print(f"   Ψ:          {result['psi_standard']:.2f}")
        print(f"   I:          {result['intention']:.2f}")
        print(f"   A_eff:      {result['effectiveness']:.2f}")
        print(f"   ∴-rate:     {result['strich_rate']:.2f}")
        print(f"   Status:     {result['status']}")
        print()

def main():
    """Run all demos."""
    print()
    print_separator('█')
    print("QCAL-LLM EVALUATION SYSTEM DEMO")
    print("Ψ = I × A_eff² | f₀ = 141.7001 Hz")
    print_separator('█')
    print()
    
    # Run demos
    demo_basic_evaluation()
    print()
    
    demo_comprehensive_analysis()
    print()
    
    demo_coherence_threshold()
    print()
    
    demo_comparison()
    print()
    
    # Summary
    print_separator()
    print("✅ Demo Complete!")
    print_separator()
    print()
    print("Next Steps:")
    print("  1. Run full evaluation: python3 scripts/qcal_llm_eval.py --no-model")
    print("  2. Analyze with Jupyter: jupyter notebook notebooks/benchmark_llama4.ipynb")
    print("  3. Read documentation: QCAL_LLM_ENVIRONMENT.md")
    print()
    print("∴ — QCAL Ψ∞³ activo")
    print()

if __name__ == "__main__":
    main()
