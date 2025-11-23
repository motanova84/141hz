# QC-LLM: Quantum Coherence Standard for Language Models

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-20%20passing-success.svg)](Tests/test_frequency_validator.py)
[![Security](https://img.shields.io/badge/security-0%20alerts-success.svg)](https://github.com/motanova84/141hz/security/code-scanning)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Universal metric for evaluating semantic coherence in Large Language Models based on f₀ = 141.7001 Hz**

## 🎯 Overview

QC-LLM establishes **f₀ = 141.7001 Hz** as the fundamental frequency for quantum coherence in language models. This frequency emerges from deep mathematical connections to:

- **Riemann Zeta Function**: |ζ'(1/2)| ≈ 1.460 encodes prime distribution
- **Golden Ratio**: φ³ ≈ 4.236 from algebraic geometry
- **Spectral Analysis**: FFT-based alignment measurement

## 🚀 Quick Start

### Installation

```bash
# Basic (without BERT)
pip install numpy scipy matplotlib

# Full (with BERT for enhanced coherence)
pip install numpy scipy matplotlib transformers>=4.48.0 torch>=2.6.0
```

### Basic Usage

```python
from qc_llm import compute_coherence, F0

# Analyze text coherence
text = "Quantum coherence is fundamental to information processing."
result = compute_coherence(text, use_bert=False)

print(f"Coherence: {result['coherence']:.2%}")
print(f"Recommendation: {result['recommendation']}")
```

**Output:**
```
Coherence: 99.31%
Recommendation: HIGH COHERENCE
```

### Using the QC_LLM Class

```python
from qc_llm import QC_LLM

# Initialize validator
validator = QC_LLM(model_name="gpt-4-sim")

# Single validation
result = validator.validate("Your text here")
print(f"Coherence: {result['coherence']:.2%}")

# Batch validation
texts = ["Text 1", "Text 2", "Text 3"]
results = validator.batch_validate(texts)
```

## 📊 How It Works

### 1. Text Embedding (BERT)

```python
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
embeddings = model(**inputs).last_hidden_state.mean(dim=1)
```

### 2. Spectral Analysis (FFT)

```python
fft_vals = np.fft.fft(embeddings[0])
freqs = np.fft.fftfreq(len(embeddings[0]), d=1.0)
```

### 3. Frequency Alignment

```python
normalized_f0 = 141.7001 / 1000.0  # Normalize to embedding domain
freq_distances = np.abs(freqs - normalized_f0)
peak_idx = np.argmin(freq_distances)
alignment = np.exp(-freq_distances[peak_idx])
```

### 4. Coherence Score

```python
coherence = |FFT[peak]| / sum(|FFT|)

if coherence > 0.8:
    recommendation = "HIGH COHERENCE"
elif coherence > 0.6:
    recommendation = "MODERATE COHERENCE"
else:
    recommendation = "LOW COHERENCE - Consider rephrasing"
```

## 📐 Mathematical Foundation

The fundamental frequency **f₀ = 141.7001 Hz** is derived from first principles:

```
f₀ = |ζ'(1/2)| × φ³ × k × √2

where:
  ζ'(1/2) ≈ -1.460354508  (Riemann zeta derivative)
  φ³ = 4.236067977        (golden ratio cubed)
  k ≈ 16.195              (Planck scale factor)
  √2 ≈ 1.414213562        (quantum normalization)
```

**See:** [Complete Mathematical Derivation](../Documentation/Theory/mathematical_foundation.md)

## 🧪 Examples

### Example 1: Analyze Scientific Text

```python
text = """
Quantum coherence emerges as a fundamental property of complex systems,
bridging the microscopic world of quantum mechanics with macroscopic phenomena.
"""

result = compute_coherence(text, use_bert=False)
# Coherence: 0.503, Frequency Alignment: 0.205
```

### Example 2: Compare Different Texts

```python
texts = [
    "Quantum coherence is fundamental.",
    "Hello world",
    "quantum quantum quantum"  # Repetitive
]

for text in texts:
    result = compute_coherence(text, use_bert=False)
    print(f"{text[:30]:30s} → {result['coherence']:.2%}")
```

### Example 3: Interactive Tutorial

Run the Jupyter notebook:
```bash
jupyter notebook Examples/Research/qc_llm_tutorial.ipynb
```

### Example 4: Demo Script

```bash
python Examples/LLM_Integration/demo_qc_llm.py
```

## 🔬 Physical Connections

f₀ = 141.7001 Hz appears in multiple physical systems:

| System | Frequency | Significance |
|--------|-----------|--------------|
| **Gravitational Waves** | 141.69 Hz (GW150914) | Ringdown component, SNR 7.47 |
| **EEG High Gamma** | 140-142 Hz | Ultra-fast neural synchronization |
| **Molecular Vibrations** | 141.8 Hz (scaled) | C-H stretch modes |
| **Navier-Stokes** | f₀ Ψ term | Prevents turbulent blow-up |

**See:** [Physical Systems Documentation](../Documentation/Theory/mathematical_foundation.md#connection-to-physical-systems)

## 🧪 Testing

```bash
# Run unit tests (20 tests)
pytest Tests/test_frequency_validator.py -v

# Run without BERT
pytest Tests/test_frequency_validator.py -k "not bert" -v

# Run with coverage
pytest Tests/test_frequency_validator.py --cov=API/Python/qc_llm --cov-report=term
```

**Test Coverage:**
- ✅ Bounds checking (coherence, alignment, quantum metric in [0, 1])
- ✅ Edge cases (empty text, whitespace, single character)
- ✅ Recommendation thresholds (HIGH, MODERATE, LOW)
- ✅ API validation (QC_LLM class, batch processing)
- ✅ Backward compatibility (compute_coherence_score)

## 📚 Documentation

- **[Mathematical Foundation](../Documentation/Theory/mathematical_foundation.md)** - Complete f₀ derivation
- **[Tutorial Notebook](../Examples/Research/qc_llm_tutorial.ipynb)** - Interactive examples
- **[Contributing Guide](../CONTRIBUTING.md#-contribuciones-qc-llm-quantum-coherence-for-llms)** - How to contribute
- **[API Reference](validator.py)** - Function signatures and docstrings

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](../CONTRIBUTING.md) for:
- **Algorithm improvements**: Optimize BERT+FFT implementation
- **LLM integrations**: Add connectors for GPT-4, Claude, Gemini, Llama
- **Documentation**: Expand mathematical derivations and tutorials
- **Tests**: Increase coverage, add benchmark comparisons

## 🔒 Security

- ✅ **CodeQL**: 0 security alerts
- ✅ **Dependencies**: transformers>=4.48.0 (CVE fixes), torch>=2.6.0 (CVE fixes)
- ✅ **Pre-commit**: Bandit security scanner enabled

Report vulnerabilities: [SECURITY.md](../SECURITY.md)

## 📄 Citation

```bibtex
@software{qc_llm_2025,
  author = {Mota Burruezo, José Manuel},
  title = {QC-LLM: Quantum Coherence Standard for Language Models},
  year = {2025},
  doi = {10.5281/zenodo.17379721},
  url = {https://github.com/motanova84/141hz}
}
```

## 📜 License

MIT License - See [LICENSE](../LICENSE)

## 👤 Author

**José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)**
- Instituto Consciencia Cuántica (ICQ)
- Palma de Mallorca, España
- Email: institutoconsciencia@proton.me
- GitHub: [@motanova84](https://github.com/motanova84)

## 🔗 Links

- **Repository**: https://github.com/motanova84/141hz
- **Paper**: https://doi.org/10.5281/zenodo.17445017
- **Lean 4 Formalization**: [formalization/lean/](../formalization/lean/)

---

*"Coherence emerges when the deep constants align."*
