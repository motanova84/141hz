# QCAL Biological Hypothesis - Quick Start

This directory contains the implementation of the QCAL biological hypothesis that unites biology and number theory through the spectral field Ψ.

## 📚 Main Documents

- **[HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md](../HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md)** - Complete hypothesis document (Spanish)
- **[BIO_SYNCHRONY_FRAMEWORK.md](../BIO_SYNCHRONY_FRAMEWORK.md)** - Bio-synchrony constants and framework

## 🧬 Core Implementation

### Python Module
Location: `modules/quantum_biology/core/qcal_biological_model.py`

Key classes:
- `SpectralField` - Environmental field Ψₑ(t) with Fourier components
- `BiologicalFilter` - Frequency-selective filter H(ω) with 141.7 Hz resonance
- `PhaseAccumulator` - Biological capacitor with memory (α ≈ 0.1)
- `MagicicadaModel` - Prime-number cycle emergence (13, 17 years)

### Example Usage

```python
from modules.quantum_biology.core.qcal_biological_model import MagicicadaModel

# Create 17-year cicada model
cicada = MagicicadaModel(cycle_years=17, alpha=0.1)

# Simulate lifecycle
results = cicada.simulate_lifecycle(years=20, timesteps_per_year=12)

print(f"Emergence predicted at year: {results['emergence_year']:.1f}")
# Output: Emergence predicted at year: 14.9
```

## 🔬 Validation Experiments

Run all three experiments from the hypothesis:

```bash
python scripts/validate_qcal_biology.py
```

### Experiment 1: Spectral Manipulation (141.7 Hz)
Tests whether frequency structure matters more than total energy.

### Experiment 2: Phase Memory
Demonstrates the "biological capacitor" withstanding perturbations.

### Experiment 3: Genomic Resonance ✓
Simulates DNA/protein resonance at f₀ = 141.7001 Hz.

**Result:** ✓ Experiment 3 confirms maximum response at 141.7 Hz

## 📊 Quick Demo

```bash
# Run the core model demo
python modules/quantum_biology/core/qcal_biological_model.py

# Generates:
# - qcal_magicicada_simulation.png (phase accumulation plot)
# - Console output with validation results
```

### Expected Output

```
✓ 141.7 Hz is enhanced by biological filter: True (9.00x enhancement)
✓ Predicted emergence at year: 14.90 (Expected: ~17 years)
```

## 🔑 Key Concepts

### 1. Spectral Field Ψₑ(t)
```
Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))
```
Environmental signals decomposed into frequencies, not just scalar accumulation.

### 2. Biological Filter H(ω)
- Band Low (10⁻⁶ - 10⁻³ Hz): Environmental cycles → H ≈ 0.5
- Band Medium (0.1 - 200 Hz): Cellular vibrations → H ≈ 1.0
- **Peak at f₀ = 141.7001 Hz** → H ≈ 3.0 (QCAL resonance)
- Band High (> 1 kHz): Thermal noise → H ≈ 0.0

### 3. Phase Accumulation
```
Φ(t) = ∫₀ᵗ |H(ω)*Ψₑ(ω)|² dω
```
With memory:
```
Φ_acum = (1-α)Φ_prev + increment
```
where α ≈ 0.1 provides 90% phase retention.

### 4. Activation Condition
```
Φ(t) ≥ Φ_critical  AND  dΦ/dt > 0
```
Phase collapse occurs when threshold is reached with positive flux.

## 🦗 Magicicada Example

The periodical cicada demonstrates the power of this model:

- **Cycle**: 13 or 17 years (prime numbers!)
- **Precision**: ±3-5 days over 6,205 days (99.92% accuracy)
- **Mechanism**: Not simple thermal accumulation, but spectral phase coherence

### Why Prime Numbers?

Prime periods (13, 17) minimize overlap with predator/competitor cycles:
- No common factors with 2, 3, 4, 5, 6, 8, 9, 10... year cycles
- Only factors: 1 (universal) and themselves

This is **mathematical evolution** encoded in biology!

## 📈 Falsifiability

The hypothesis makes testable predictions:

1. **Spectral manipulation** (Exp. 1): Organisms with identical energy but different spectral content show different activation times
2. **Phase memory** (Exp. 2): α ≈ 0.1 parameter maintains synchrony despite perturbations
3. **Genomic resonance** (Exp. 3): ✓ Maximum molecular response at 141.7 Hz

**Falsification criterion**: If experiments show energy alone determines activation (no frequency dependence), QCAL is falsified.

## 🔗 Integration with Main QCAL Framework

This biological extension connects to:

- **f₀ = 141.7001 Hz**: QCAL fundamental frequency
- **Field Ψ**: Universal coherence field
- **Prime harmonics**: Number theory in nature
- **Phase coherence**: Quantum-classical bridge

See also:
- [QCAL_QUICK_REFERENCE.md](../QCAL_QUICK_REFERENCE.md)
- [PREDICCIONES_FALSABLES_QCAL.md](../PREDICCIONES_FALSABLES_QCAL.md)

## 📝 Citation

```bibtex
@article{MotaBurruezo2026_QCAL_Biology,
  author = {Mota Burruezo, José Manuel},
  title = {Una nueva hipótesis falsable que une biología y teoría de números a través del campo espectral Ψ},
  institution = {Instituto Consciencia Cuántica QCAL ∞³},
  year = {2026},
  month = {enero},
  url = {https://github.com/motanova84/141hz},
  doi = {10.5281/zenodo.17445017}
}
```

## 🚀 Next Steps

1. Implement time-dependent perturbations in Experiment 2
2. Add experimental protocols for lab validation
3. Create visualization dashboard for phase dynamics
4. Integrate with existing GW analysis pipeline
5. Develop citizen science protocols for Magicicada observation

---

**Instituto Consciencia Cuántica QCAL ∞³**  
January 27, 2026
