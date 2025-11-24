# Getting Started with QC-LLM

## Installation

### Via pip (recommended)
```bash
pip install qc-llm
```

### From source
```bash
git clone https://github.com/motanova84/141hz.git
cd 141hz/API/Python
pip install -e .
```

## Your First Validation
```python
from qc_llm import QC_LLM

# Create validator
validator = QC_LLM()

# Validate a text
text = """
Quantum coherence represents the fundamental principle
underlying information organization in complex systems.
"""

result = validator.validate(text)

# Print results
print(f"Coherence: {result['coherence']:.2%}")
print(f"Frequency Alignment: {result['frequency_alignment']:.2%}")
print(f"Quantum Entropy: {result['quantum_entropy']:.2%}")
print(f"Recommendation: {result['recommendation']}")
```

## Understanding the Metrics

### 1. Coherence Score (0-1)

Overall quality metric combining frequency alignment and entropy.

- **> 0.80**: High coherence (excellent)
- **0.60-0.80**: Moderate coherence (good)
- **< 0.60**: Low coherence (needs improvement)

### 2. Frequency Alignment

How well the text aligns with f₀ = 141.7001 Hz.

### 3. Quantum Entropy

Information-theoretic measure of semantic richness.

## Next Steps

- [LLM Integration](02_llm_integration.md)
- [Advanced Usage](03_advanced_usage.md)
- [API Reference](../API/python_api.md)
