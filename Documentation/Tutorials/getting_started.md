# Getting Started with QC-LLM

Welcome to QC-LLM (Quantum Coherence for Language Models)! This guide will help you get started with using the f₀ = 141.7001 Hz frequency standard for validating LLM coherence.

## What is QC-LLM?

QC-LLM establishes **f₀ = 141.7001 Hz** as a universal standard for measuring quantum coherence in language model outputs. This frequency emerges from deep mathematical structures:

- **Riemann Zeta Function:** |ζ'(1/2)| ≈ 1.4604
- **Golden Ratio:** φ³ ≈ 4.236
- **Prime Distribution:** Spectral emergence from number theory

## Installation

### Python

```bash
pip install numpy scipy

# Add to your Python path
export PYTHONPATH=$PYTHONPATH:/path/to/141hz/API/Python
```

### JavaScript/TypeScript

```bash
cd API/JavaScript/qc-llm-js
npm install
npm run build
```

## Quick Start

### Python API

```python
# Import the validator
import sys
sys.path.insert(0, 'API/Python')
from qc_llm import QC_LLM

# Initialize
validator = QC_LLM()

# Validate text
text = "Quantum coherence in language models represents a fundamental alignment."
result = validator.validate(text)

# Print results
print(f"Coherence: {result['coherence']:.2%}")
print(f"Frequency Alignment: {result['frequency_alignment']:.2%}")
print(f"Quantum Entropy: {result['quantum_entropy']:.2%}")
print(f"Recommendation: {result['recommendation']}")
```

**Output:**
```
Coherence: 87.3%
Frequency Alignment: 92.1%
Quantum Entropy: 78.5%
Recommendation: HIGH COHERENCE - Excellent quality
```

### REST API

Start the server:
```bash
cd API/REST
python3 frequency_validator.py
```

Test with curl:
```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test quantum coherence validation"}'
```

Visit the interactive docs:
```
http://localhost:8000/docs
```

### JavaScript API

```typescript
import { QC_LLM } from 'qc-llm-js';

const validator = new QC_LLM();
const result = validator.validate("Your text here");

console.log(`Coherence: ${(result.coherence * 100).toFixed(1)}%`);
```

## Core Concepts

### Coherence Score

The coherence score is computed as:

```
coherence = 0.6 × frequency_alignment + 0.4 × quantum_entropy
```

Where:
- **Frequency Alignment:** How well text aligns with f₀ = 141.7001 Hz
- **Quantum Entropy:** Token diversity and distribution

### Interpretation

| Score Range | Quality Level | Recommendation |
|-------------|---------------|----------------|
| > 0.8 | High Coherence | Excellent - use as is |
| 0.6 - 0.8 | Moderate | Good - minor improvements possible |
| 0.4 - 0.6 | Low | Consider rephrasing |
| < 0.4 | Very Low | Significant revision needed |

## Common Use Cases

### 1. LLM Output Validation

```python
from qc_llm import QC_LLM

validator = QC_LLM(model_name="gpt-4")

# Generate output (placeholder)
llm_output = "Generated text from language model..."

# Validate
result = validator.validate(llm_output)

if result['coherence'] < 0.6:
    print("Low coherence - consider regenerating")
```

### 2. Batch Processing

```python
texts = [
    "First document...",
    "Second document...",
    "Third document..."
]

results = validator.batch_validate(texts)

for i, result in enumerate(results):
    print(f"Doc {i+1}: {result['coherence']:.2%}")
```

### 3. Real-Time Monitoring

```python
import sys
sys.path.insert(0, 'Applications/LLM')
from RealTimeMonitor import RealTimeMonitor

monitor = RealTimeMonitor(window_size=100)

for chunk in text_stream:
    coherence = monitor.update(chunk)
    print(f"Current: {coherence:.2%}")
```

### 4. Model Comparison

```python
from Applications.LLM.CoherenceMetric import CoherenceMetric

metric = CoherenceMetric()

outputs = {
    "GPT-4": "GPT-4 generated text...",
    "Claude": "Claude generated text...",
    "Llama": "Llama generated text..."
}

# Compare and rank
rankings = metric.rank_outputs(outputs)

for rank, (model, score) in enumerate(rankings, 1):
    print(f"{rank}. {model}: {score:.2%}")
```

## Advanced Features

### Coherence Metric

```python
from Applications.LLM.CoherenceMetric import CoherenceMetric

metric = CoherenceMetric()

# Detailed analysis
analysis = metric.detailed_analysis("Your text")
print(analysis)
```

### Quantum Alignment

```python
from Applications.LLM.QuantumAlignment import QuantumAlignment

aligner = QuantumAlignment(threshold=0.80)

# Align text to target coherence
result = aligner.align_text("Original text")

print(f"Aligned: {result['aligned']}")
print(f"Coherence: {result['coherence']:.2%}")
print(f"Iterations: {result['iterations']}")
```

### Benchmarking

```python
from Benchmarks.LLMComparison.benchmark import LLMBenchmark

benchmark = LLMBenchmark()

# Prepare responses for each model
model_responses = {
    "GPT-4": [resp1, resp2, resp3, ...],
    "Claude": [resp1, resp2, resp3, ...]
}

# Run benchmark
results = benchmark.run_benchmark(model_responses)

# Generate leaderboard
leaderboard = benchmark.generate_leaderboard(results)
print(leaderboard)
```

## Testing Your Installation

Run the validation tests:
```bash
python3 Tools/Validators/validate_coherence.py
```

Expected output:
```
============================================================
QC-LLM Coherence Validation Tests
============================================================
Fundamental Frequency: f₀ = 141.7001 Hz

✅ Frequency constant test passed
✅ Basic validation test passed
✅ Batch validation test passed
✅ Empty text handling test passed

============================================================
✅ All tests passed!
============================================================
```

## Next Steps

1. **Read the theory:** [Documentation/Theory/mathematical_foundation.md](../Theory/mathematical_foundation.md)
2. **Explore examples:** [Examples/](../../Examples/)
3. **Try benchmarking:** [Benchmarks/LLMComparison/](../../Benchmarks/LLMComparison/)
4. **Integrate with your LLM:** [Examples/LLM_Integration/](../../Examples/LLM_Integration/)

## Troubleshooting

### Import errors
```bash
# Make sure you've added to Python path
export PYTHONPATH=$PYTHONPATH:/path/to/141hz/API/Python
```

### Missing dependencies
```bash
pip install numpy scipy fastapi pydantic uvicorn
```

### API server not starting
```bash
# Check port 8000 is available
lsof -i :8000

# Or use different port
uvicorn main:app --port 8001
```

## Support

- **Issues:** https://github.com/motanova84/141hz/issues
- **Discussions:** https://github.com/motanova84/141hz/discussions
- **Email:** institutoconsciencia@proton.me

## Citation

If you use QC-LLM in your research:

```bibtex
@software{qc_llm_2025,
  author = {Mota Burruezo, José Manuel},
  title = {QC-LLM: Quantum Coherence Standard for Language Models},
  year = {2025},
  doi = {10.5281/zenodo.17379721},
  url = {https://github.com/motanova84/141hz}
}
```

## License

MIT License - See [LICENSE](../../LICENSE)
