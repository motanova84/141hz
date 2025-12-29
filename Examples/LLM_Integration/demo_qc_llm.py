"""
Demo script to test QC-LLM with sample LLM outputs

This script demonstrates the compute_coherence function with various
text samples that simulate LLM outputs.
"""

import sys
import os
# Add API/Python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'API', 'Python'))

from qc_llm import compute_coherence, QC_LLM, F0

def print_separator():
    print("=" * 80)

def analyze_text(text, label, use_bert=False):
    """Analyze a text sample and print results"""
    print(f"\n{label}:")
    print(f"Text: '{text[:100]}{'...' if len(text) > 100 else ''}'")
    print("-" * 80)
    
    result = compute_coherence(text, use_bert=use_bert)
    
    print(f"Coherence Score:      {result['coherence']:.3f}")
    print(f"Frequency Alignment:  {result['frequency_alignment']:.3f}")
    print(f"Quantum Metric:       {result['quantum_metric']:.3f}")
    print(f"Recommendation:       {result['recommendation']}")

def main():
    print_separator()
    print(f"QC-LLM Demo: Testing Quantum Coherence with f₀ = {F0} Hz")
    print_separator()
    
    # Sample 1: High-quality scientific text (expected HIGH COHERENCE)
    sample1 = """
    Quantum coherence emerges as a fundamental property of complex systems, 
    bridging the microscopic world of quantum mechanics with macroscopic phenomena. 
    This universal principle manifests across multiple scales, from subatomic particles 
    to gravitational waves, suggesting a deep mathematical structure underlying nature.
    """
    analyze_text(sample1.strip(), "Sample 1: High-Quality Scientific Text")
    
    # Sample 2: Short casual text (expected MODERATE COHERENCE)
    sample2 = "The quick brown fox jumps over the lazy dog."
    analyze_text(sample2, "Sample 2: Short Casual Text")
    
    # Sample 3: Repetitive low-quality text (expected LOW COHERENCE)
    sample3 = "quantum quantum quantum quantum quantum"
    analyze_text(sample3, "Sample 3: Repetitive Text")
    
    # Sample 4: Mixed quality (expected MODERATE COHERENCE)
    sample4 = """
    AI systems process information efficiently. The models learn patterns from data. 
    Neural networks compute representations through layers of transformations.
    """
    analyze_text(sample4.strip(), "Sample 4: Technical Description")
    
    # Sample 5: Philosophical coherent text (expected HIGH/MODERATE COHERENCE)
    sample5 = """
    The fundamental frequency of consciousness resonates at 141.7 Hz, 
    connecting quantum field dynamics with emergent awareness. This harmonic 
    correspondence suggests that information processing at biological scales 
    may naturally synchronize with universal mathematical constants.
    """
    analyze_text(sample5.strip(), "Sample 5: Philosophical Text")
    
    # Sample 6: Incoherent text (expected LOW COHERENCE)
    sample6 = "a b c d e f g h i j k"
    analyze_text(sample6, "Sample 6: Random Characters")
    
    print_separator()
    print("\nBatch Analysis with QC_LLM Class:")
    print_separator()
    
    # Demonstrate batch processing
    validator = QC_LLM(model_name="demo")
    
    batch_texts = [
        "Quantum coherence is fundamental to information processing.",
        "Hello world",
        "The integration of mathematics and physics reveals deep connections."
    ]
    
    results = validator.batch_validate(batch_texts)
    
    for i, (text, result) in enumerate(zip(batch_texts, results), 1):
        print(f"\n{i}. Text: {text}")
        print(f"   Coherence: {result['coherence']:.2%} - {result['recommendation']}")
    
    print_separator()
    print("\n✅ Demo completed successfully!")
    print(f"All texts analyzed using f₀ = {QC_LLM.get_frequency()} Hz standard")
    print_separator()

if __name__ == "__main__":
    main()
