#!/usr/bin/env python3
"""
Llama 4 Maverick Coherence Demo

Demonstrates the Llama 4 Maverick integration for quantum coherence evaluation
in the QCAL-LLM framework.

Usage:
    export HF_TOKEN=your_huggingface_token
    python scripts/llama4_coherence_demo.py

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from llama4_coherence import Llama4Coherence
except ImportError as e:
    print(f"Error: Could not import llama4_coherence: {e}")
    print("\nPlease install required dependencies:")
    print("  pip install transformers>=4.48.0 torch>=2.6.0")
    sys.exit(1)


def main():
    """Run Llama 4 coherence demonstration."""
    print("="*70)
    print("Llama 4 Maverick Coherence Demo")
    print("QCAL-LLM ∞³ - Quantum Coherent Attention Layer")
    print("="*70)
    print()
    
    # Check for HF_TOKEN
    if not os.getenv("HF_TOKEN"):
        print("❌ Error: HF_TOKEN environment variable not set")
        print()
        print("To run this demo, you need a Hugging Face access token:")
        print("  1. Sign up at https://huggingface.co")
        print("  2. Create an access token at https://huggingface.co/settings/tokens")
        print("  3. Set the token: export HF_TOKEN=your_token_here")
        print()
        return 1
    
    # Test texts for coherence evaluation
    test_texts = [
        {
            "text": "Quantum coherence at 141.7 Hz is derived from ζ'(1/2) × φ³.",
            "expected": "HIGH",
            "description": "Physics-grounded text with correct formulation"
        },
        {
            "text": "The frequency 141.7 Hz emerges from prime numbers and golden ratio.",
            "expected": "HIGH",
            "description": "Conceptually accurate but less precise"
        },
        {
            "text": "The value of f₀ = 141.7001 Hz was detected in LIGO GW150914 with SNR=20.95.",
            "expected": "HIGH",
            "description": "Empirically grounded with data"
        },
        {
            "text": "Coherence can be measured at various frequencies including 141.7 Hz.",
            "expected": "MEDIUM",
            "description": "Mentions frequency but lacks theoretical grounding"
        },
        {
            "text": "Random quantum fluctuations create unpredictable patterns in spacetime.",
            "expected": "LOW",
            "description": "Generic physics jargon without specific content"
        },
        {
            "text": "The cat sat on the mat and looked at the moon.",
            "expected": "LOW",
            "description": "Non-physics text"
        }
    ]
    
    try:
        print("Initializing Llama 4 Maverick...")
        print("(This may take a few minutes on first run)")
        print()
        
        llama4 = Llama4Coherence()
        
        print("✓ Llama 4 Maverick loaded successfully")
        print()
        print("-"*70)
        print()
        
        # Evaluate each test text
        results = []
        for i, test in enumerate(test_texts, 1):
            print(f"Test {i}/{len(test_texts)}: {test['description']}")
            print(f"Expected: {test['expected']}")
            print()
            print(f"Text: \"{test['text']}\"")
            print()
            
            score = llama4.get_coherence_score(test['text'])
            
            # Classify score
            if score >= 0.8:
                classification = "HIGH"
                symbol = "✓"
            elif score >= 0.5:
                classification = "MEDIUM"
                symbol = "○"
            else:
                classification = "LOW"
                symbol = "✗"
            
            print(f"Llama 4 Coherence Score: {score:.3f} ({classification}) {symbol}")
            
            # Check if matches expectation
            matches = classification == test['expected']
            if matches:
                print("Assessment: Matches expected coherence ✓")
            else:
                print(f"Assessment: Different from expected ({test['expected']})")
            
            results.append({
                'text': test['text'],
                'score': score,
                'classification': classification,
                'expected': test['expected'],
                'matches': matches
            })
            
            print()
            print("-"*70)
            print()
        
        # Summary
        print("="*70)
        print("SUMMARY")
        print("="*70)
        print()
        
        matches = sum(1 for r in results if r['matches'])
        total = len(results)
        accuracy = (matches / total) * 100
        
        print(f"Tests run: {total}")
        print(f"Expected matches: {matches}/{total} ({accuracy:.1f}%)")
        print()
        
        print("Score Distribution:")
        high_count = sum(1 for r in results if r['score'] >= 0.8)
        medium_count = sum(1 for r in results if 0.5 <= r['score'] < 0.8)
        low_count = sum(1 for r in results if r['score'] < 0.5)
        
        print(f"  HIGH (≥0.8):   {high_count}/{total}")
        print(f"  MEDIUM (≥0.5): {medium_count}/{total}")
        print(f"  LOW (<0.5):    {low_count}/{total}")
        print()
        
        avg_score = sum(r['score'] for r in results) / len(results)
        print(f"Average coherence score: {avg_score:.3f}")
        print()
        
        print("="*70)
        print("✓ Demo completed successfully")
        print("="*70)
        print()
        print("Next steps:")
        print("  • Integrate with QCALLLMCore: core = QCALLLMCore(use_llama4=True)")
        print("  • Run comparative benchmarks: python tests/test_llama4_coherence.py")
        print("  • Test with custom texts: python llama4_coherence.py 'your text'")
        print()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
