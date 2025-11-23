"""
QC-LLM × OpenAI Integration Example
"""

import os
from openai import OpenAI
import sys
sys.path.append('../../API/Python')
from qc_llm import QC_LLM

# Initialize
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
validator = QC_LLM(model_name="gpt-4")

def coherent_completion(prompt: str, threshold: float = 0.80, max_iterations: int = 3):
    """
    Generate completion with coherence guarantee
    
    Iteratively refines until coherence > threshold
    """
    print(f"🎯 Target coherence: {threshold:.0%}\n")
    
    for iteration in range(1, max_iterations + 1):
        print(f"🔄 Iteration {iteration}/{max_iterations}")
        
        # Generate completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.choices[0].message.content
        
        # Validate
        result = validator.validate(text)
        coherence = result["coherence"]
        
        print(f"   Coherence: {coherence:.2%}")
        print(f"   Freq Align: {result['frequency_alignment']:.2%}")
        print(f"   Entropy: {result['quantum_entropy']:.2%}")
        print(f"   {result['recommendation']}\n")
        
        if coherence >= threshold:
            print(f"✅ Success! Coherence achieved: {coherence:.2%}\n")
            return text, result
        
        # Refine prompt
        prompt = (f"{prompt}\n\n"
                 f"[Previous attempt: coherence={coherence:.2%}. "
                 f"Please rephrase with clearer, more coherent structure.]")
    
    print(f"⚠️  Max iterations reached. Best coherence: {coherence:.2%}\n")
    return text, result

# Example usage
if __name__ == "__main__":
    result, metrics = coherent_completion(
        "Explain the relationship between quantum coherence and language models in simple terms."
    )
    
    print("="*60)
    print("FINAL RESULT:")
    print("="*60)
    print(result)
    print("\n" + "="*60)
    print("METRICS:")
    print("="*60)
    for key, value in metrics.items():
        print(f"{key}: {value}")
