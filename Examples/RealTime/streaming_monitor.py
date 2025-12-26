"""
Real-time coherence streaming monitor
"""

import sys
sys.path.append('../../API/Python')
from qc_llm import QC_LLM
import time

validator = QC_LLM()

def monitor_stream(text_generator):
    """
    Monitor coherence of streaming text
    
    Args:
        text_generator: Iterator yielding text chunks
    """
    buffer = ""
    coherence_history = []
    
    print("🌊 Starting real-time coherence monitoring...\n")
    print(f"Target frequency: {validator.get_frequency()} Hz\n")
    print("-" * 60)
    
    for chunk in text_generator:
        buffer += chunk
        
        # Validate every 50 characters
        if len(buffer) >= 50:
            result = validator.validate(buffer)
            coherence = result["coherence"]
            coherence_history.append(coherence)
            
            # Visual indicator
            bar_length = int(coherence * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            print(f"\r[{bar}] {coherence:.1%} | {result['recommendation'][:30]}", end="")
            
            time.sleep(0.1)
    
    print("\n" + "-" * 60)
    
    # Final statistics
    if coherence_history:
        avg_coherence = sum(coherence_history) / len(coherence_history)
        print(f"\n📊 Final Statistics:")
        print(f"   Average Coherence: {avg_coherence:.2%}")
        print(f"   Min: {min(coherence_history):.2%}")
        print(f"   Max: {max(coherence_history):.2%}")
        print(f"   Samples: {len(coherence_history)}")

# Example generator
def example_text_stream():
    """Simulate streaming text"""
    text = """
    Quantum coherence in language models represents a fundamental principle
    where the semantic structure of generated text aligns with natural
    frequencies observed in complex systems. The frequency f₀ = 141.7001 Hz
    emerges from deep mathematical connections to the Riemann zeta function
    and the golden ratio, suggesting an underlying universal principle of
    information organization.
    """
    
    for char in text:
        yield char
        time.sleep(0.01)

if __name__ == "__main__":
    monitor_stream(example_text_stream())
