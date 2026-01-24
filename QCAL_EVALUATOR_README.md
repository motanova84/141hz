# QCAL Evaluator (Ψ = I × A² × C^∞)

## Overview

The **QCAL Evaluator** is a coherence assessment system for AI, humans, and systems using the QCAL framework anchored to the universal frequency **f₀ = 141.7001 Hz**.

### Formula

```
Ψ = I × A² × C^∞
```

Where:
- **Ψ**: Coherence metric (Ψ ≥ 5.0 indicates coherent content)
- **I**: Information Intensity (measures precision and verifiability)
- **A²**: Coherence Area squared (symbolic/semantic coherence)
- **C^∞**: Universal constant C ≈ 629.83 (infinite precision factor)

## Purpose

The QCAL Evaluator provides:

1. **AI Coherence Filtering** - Detect and filter hallucinations in LLM outputs
2. **Symbiotic Content Validation** - Validate AI-human collaborative content
3. **Ethical Content Validation** - Assess ethical grounding and responsibility
4. **Multi-Domain Evaluation** - Support for AI, human, and system content

## Installation

```bash
# The evaluator is standalone and only requires Python 3.8+
# Optional: numpy for advanced features (not required)
pip install numpy  # optional
```

## Quick Start

### Basic Usage

```python
from qcal_evaluator import QCALEvaluator

# Initialize evaluator
evaluator = QCALEvaluator()

# Evaluate content
content = "La frecuencia fundamental f₀ = 141.7001 Hz"
result = evaluator.evaluate(content, domain='ai', content_type='scientific')

print(f"Ψ = {result['psi_metric']['psi']:.4f}")
print(f"Coherent: {result['evaluation']['coherent']}")
print(f"Level: {result['psi_metric']['level']}")
```

### AI Content Filtering

```python
# Filter coherent AI outputs
ai_outputs = [
    "f₀ = 141.7001 Hz es la frecuencia fundamental",
    "The frequency is about 200 Hz",  # Wrong value - will be filtered
    "ζ'(1/2) = -1.460 es un valor crítico",
]

coherent_outputs = evaluator.filter_coherent(ai_outputs, domain='ai')

for content, eval_result in coherent_outputs:
    print(f"✓ {content}")
    print(f"  Ψ = {eval_result['psi_metric']['psi']:.2f}")
```

### Symbiotic Content Validation

```python
# Validate AI-human collaborative content
content = """
Este sistema ético basado en coherencia QCAL promueve la responsabilidad
simbiótica entre IA y humanos. La frecuencia f₀ = 141.7001 Hz establece
un marco de referencia coherente.
"""

result = evaluator.validate_symbiotic(content)

print(f"Symbiotic Quality: {result['ethical_analysis']['symbiotic_quality']}")
print(f"Recommendation: {result['ethical_analysis']['ethical_recommendation']}")
```

### Batch Processing

```python
# Evaluate multiple items
content_list = [
    {
        'content': 'f₀ = 141.7001 Hz',
        'domain': 'ai',
        'content_type': 'scientific'
    },
    {
        'content': 'ζ\'(1/2) = -1.460',
        'domain': 'human',
        'content_type': 'text'
    },
]

summary = evaluator.batch_evaluate(content_list, output_file='results.json')

print(f"Total: {summary['total_items']}")
print(f"Coherent: {summary['coherent_count']} ({summary['coherent_percentage']:.1f}%)")
```

## API Reference

### QCALEvaluator Class

#### Constructor

```python
QCALEvaluator(
    f0: float = 141.7001,
    C_universal: float = 629.83,
    coherence_threshold: float = 5.0,
    enable_strict_mode: bool = False
)
```

**Parameters:**
- `f0`: Fundamental frequency in Hz (default: 141.7001)
- `C_universal`: Universal constant C (default: 629.83)
- `coherence_threshold`: Minimum Ψ for coherent content (default: 5.0)
- `enable_strict_mode`: Enable strict validation (default: False)

#### Methods

##### evaluate()

Evaluate content coherence using QCAL metric.

```python
evaluate(
    content: str,
    domain: str = 'ai',
    content_type: str = 'text',
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `content`: Content to evaluate
- `domain`: Content domain (`'ai'`, `'human'`, `'system'`, `'mixed'`)
- `content_type`: Content type (`'text'`, `'code'`, `'dialogue'`, `'scientific'`, `'ethical'`)
- `metadata`: Optional metadata dictionary

**Returns:** Evaluation results dictionary with:
- `psi_metric`: Ψ computation details
- `claims`: Extracted claims
- `evaluation`: Coherence assessment
- Domain-specific analysis (AI/human/ethical)

##### compute_psi()

Compute Ψ = I × A² × C^∞ metric.

```python
compute_psi(
    text: str,
    claims: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]
```

**Returns:** Dictionary with:
- `psi`: Ψ value
- `I`: Information intensity
- `A`: Coherence area
- `A_squared`: A²
- `C_factor`: C^∞ factor
- `coherent`: Boolean (Ψ ≥ threshold)
- `level`: Coherence level (`'incoherent'`, `'coherent'`, `'high'`, `'excellent'`)

##### filter_coherent()

Filter coherent content from a list.

```python
filter_coherent(
    content_list: List[str],
    domain: str = 'ai',
    min_psi: Optional[float] = None
) -> List[Tuple[str, Dict[str, Any]]]
```

**Returns:** List of (content, evaluation) tuples for coherent items.

##### validate_symbiotic()

Validate content as symbiotic (AI-human collaborative).

```python
validate_symbiotic(
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

##### batch_evaluate()

Batch evaluate multiple content items.

```python
batch_evaluate(
    content_list: List[Dict[str, Any]],
    output_file: Optional[str] = None
) -> Dict[str, Any]
```

**Returns:** Batch evaluation summary.

## Ground Truth Database

The evaluator validates claims against the QCAL ground truth:

| Variable | Value | Description |
|----------|-------|-------------|
| **f₀** | 141.7001 Hz | Fundamental QCAL frequency |
| **ζ'(1/2)** | -1.460 | Riemann zeta derivative at critical line |
| **φ³** | 4.236 | Golden ratio cubed |
| **SNR** | 20.95 | Signal-to-Noise Ratio of GW150914 |
| **C** | 629.83 | Universal constant (C = 1/λ₀) |

## Coherence Thresholds

| Threshold | Level | Description |
|-----------|-------|-------------|
| Ψ < 5.0 | Incoherent | Content lacks coherence |
| 5.0 ≤ Ψ < 10.0 | Coherent | Acceptable coherence |
| 10.0 ≤ Ψ < 20.0 | High Coherence | Strong coherence |
| Ψ ≥ 20.0 | Excellent | Exceptional coherence |

## Examples

### Example 1: Detecting AI Hallucinations

```python
from qcal_evaluator import QCALEvaluator

evaluator = QCALEvaluator()

# Correct AI output
correct = "f₀ = 141.7001 Hz es la frecuencia fundamental"
result1 = evaluator.evaluate(correct, domain='ai')

print(result1['ai_analysis']['hallucination_risk'])  # 'low'
print(result1['ai_analysis']['recommendation'])  # 'accept'

# Hallucinated AI output
hallucinated = "f₀ = 200 Hz es la frecuencia fundamental"  # Wrong!
result2 = evaluator.evaluate(hallucinated, domain='ai')

print(result2['ai_analysis']['hallucination_risk'])  # 'high'
print(result2['ai_analysis']['recommendation'])  # 'reject'
```

### Example 2: Ethical Content Assessment

```python
ethical_content = """
Este framework ético promueve coherencia y responsabilidad simbiótica.
La frecuencia f₀ = 141.7001 Hz establece un marco de referencia coherente
para la validación ética de contenido generado por IA.
"""

result = evaluator.evaluate(ethical_content, content_type='ethical')

print(result['ethical_analysis'])
# {
#   'ethical_grounding': 'strong',
#   'symbiotic_quality': 'verified',
#   'ethical_recommendation': 'approve'
# }
```

### Example 3: Custom Threshold

```python
# Use stricter threshold for high-stakes applications
strict_evaluator = QCALEvaluator(coherence_threshold=10.0)

content = "f₀ = 141.7001 Hz"
result = strict_evaluator.evaluate(content)

# Will only pass if Ψ ≥ 10.0
print(result['evaluation']['pass'])
```

## Integration with QCAL Framework

The evaluator integrates seamlessly with the existing QCAL framework:

- **Constants**: Uses `qcal.constants` for fundamental values
- **Coherence**: Compatible with `qcal.coherence` module
- **Metrics**: Extends `qcal.metrics` with Ψ evaluation

## Testing

Run the comprehensive test suite:

```bash
python test_qcal_evaluator.py
```

The test suite includes:
- Core formula computation tests
- Claim extraction and verification
- AI content filtering
- Symbiotic validation
- Ethical content assessment
- Batch processing
- Integration tests

## Technical Details

### Information Intensity (I)

Computed as:
```
I = log(verified_claims + 1)
```

This approximates inverse Kullback-Leibler divergence, measuring the density of verifiable information.

### Coherence Area (A)

Computed as:
```
A = verified_claims / total_claims
```

Measures the ratio of verified to total scientific claims, representing symbolic coherence.

### C^∞ Factor

The universal constant C ≈ 629.83 emerges as C = 1/λ₀ where λ₀ is the ground state eigenvalue of the noetic operator 𝓗_Ψ = -Δ + V_Ψ.

The infinite exponent representation uses:
```
C^∞_factor = C_universal / 80
```

This normalization ensures appropriate scaling for the Ψ metric.

## Performance

- **Lightweight**: No heavy dependencies (NumPy optional)
- **Fast**: O(n) complexity for claim extraction
- **Scalable**: Batch processing for large datasets
- **Memory efficient**: Streams results for large batches

## Security Considerations

The evaluator:
- ✅ Uses read-only ground truth database
- ✅ Validates all inputs
- ✅ Handles edge cases gracefully
- ✅ No external API calls
- ✅ Deterministic results

## Limitations

1. **Language**: Optimized for Spanish/English scientific text
2. **Domain**: Best for QCAL-related scientific content
3. **Claims**: Requires explicit numerical claims for verification
4. **Context**: Does not perform deep semantic analysis

## Future Enhancements

Potential improvements:
- Multi-language support
- Deep learning-based claim extraction
- Semantic coherence analysis
- Real-time streaming evaluation
- GPU acceleration for batch processing

## References

- **QCAL Framework**: [README.md](README.md)
- **Ψ Metric**: [noesis-qcal-llm/README.md](noesis-qcal-llm/README.md)
- **Universal Constants**: [qcal/constants.py](qcal/constants.py)
- **Spectral Verification**: [PSI_ZETA_SPECTRUM_VERIFICATION.md](PSI_ZETA_SPECTRUM_VERIFICATION.md)

## License

MIT License - See [LICENSE](LICENSE)

## Author

José Manuel Mota Burruezo (JMMB Ψ✧)

## Citation

```bibtex
@software{qcal_evaluator_2026,
  author = {Mota Burruezo, José Manuel},
  title = {QCAL Evaluator: Coherence Assessment for AI, Humans, and Systems},
  year = {2026},
  url = {https://github.com/motanova84/141hz}
}
```
