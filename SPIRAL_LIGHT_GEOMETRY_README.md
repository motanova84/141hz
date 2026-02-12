# Spiral Light Geometry - Zeta-Modulated Photon Paths

## 🌀 Overview

This module implements the QCAL theoretical framework where **light does not travel in straight lines**, but follows **logarithmic spiral paths** modulated by the zeros of the **Riemann zeta function** and **resonant prime number nodes**.

> **"No es onda. No es partícula. Es espiral logarítmica coherente, modulada por los ceros de ζ(s)."**

## 📐 Mathematical Framework

### 1. Spiral Path Equations (Espira ζ)

Each ray of light follows a spiral path described by:

```
x(t) = r₀ · e^(λt) · cos(2πf₀t + φₚ)
y(t) = r₀ · e^(λt) · sin(2πf₀t + φₚ)
```

where:
- **f₀ = 141.7001 Hz** - Fundamental QCAL frequency
- **λ** - Fractal expansion index
- **φₚ** - Phase modulated by the n-th prime pₙ

### 2. Riemann Zeta Zeros as Spectral Layers

The non-trivial zeros of the Riemann zeta function define spectral phase layers:

```
s = 1/2 + iγₙ  with  ζ(s) = 0
```

These zeros exist on the critical line **Re(s) = 1/2** and their imaginary parts γₙ define the spectral frequencies:

```
fₙ = f₀ · (γₙ / γ₁)
```

### 3. Prime Numbers as Resonant Nodes

The Euler product expansion reveals the role of primes:

```
ζ(s) = ∏ₚ (1 - p^(-s))^(-1)
```

Each prime **p** acts as a **vibrational node**, modulating spectral phases. The phase contribution from the n-th prime is:

```
φₚ = 2π · log(pₙ) / log(p₁)
```

### 4. Wave Function with ζ-Spectral Modulation

The complete wave function is:

```
Ψ(x,t) = Σₙ Aₙ · e^(i(2πfₙt + φₙ)) · e^(iSₚ(x)/ℏ)
```

where:
- **Aₙ** - Amplitude associated with prime node pₙ
- **fₙ** - Frequency associated with zeta zero γₙ
- **Sₚ(x)** - Action defined on spectral path linked to prime p

## 🧪 Experimental Predictions

### Observable Effects

1. **Interference Pattern Deviations**
   - Patterns show **logarithmic spiral arcs**, not perfect circles
   - Angular deviation **Δθ** from axial symmetry reveals ζ(s) zero influence

2. **Spectral Resonances**
   - High-Q optical cavities should show modulation at **141.7 Hz**
   - Resonance in **TEM₀₁ modes** with spiral structure

3. **Coherence Maximality**
   - Maximum coherence achieved when following prime spectral map
   - "Desplazarse en c no es velocidad, es coherencia máxima"

### Suggested Experiments

- **LISA/GEO600** - High-precision interferometry to detect quasi-fractal spectral deviations
- **Fabry-Pérot Cavities** - Oscillation at 141.7001 Hz with spiral pattern detection
- **Quantum Biprism Interferometers** - Low-energy electron detection of spiral deviations
- **Modulated Lasers** - Artificial ζ'(1/2) modulation to reproduce fractal spiral patterns

## 🚀 Quick Start

### Installation

The module is part of the QCAL package. Ensure you have the required dependencies:

```bash
pip install numpy scipy mpmath matplotlib
```

### Basic Usage

```python
from qcal.spiral_light_geometry import (
    SpiralLightGeometry,
    generate_spiral_path,
    calculate_interference
)

# Generate a spiral light path
t, x, y = generate_spiral_path(
    duration=0.01,      # 10 ms
    dt=1e-5,           # 10 μs steps
    prime_index=1,     # Use first prime (2)
    lambda_expansion=0.05
)

# Calculate interference pattern
intensity = calculate_interference(
    size=256,          # 256x256 grid
    extent=2e-6,       # 2 μm screen
    t=0.001,          # at t = 1 ms
    n_primes=7,       # use 7 primes
    n_zeros=5         # use 5 zeta zeros
)
```

### Advanced Usage

```python
from qcal.spiral_light_geometry import (
    SpiralLightGeometry,
    SpiralPathParams,
    WaveFunctionParams,
    CoherenceMaximality
)

# Initialize geometry calculator
geometry = SpiralLightGeometry(precision=50)

# Get Riemann zeta zeros
zeros = geometry.get_zeta_zeros(10)
print(f"First zeta zero: γ₁ = {zeros[0]:.6f}")

# Calculate spectral frequencies
frequencies = geometry.zeta_spectral_frequencies(10)

# Generate wave function
import numpy as np
x = np.linspace(-1e-6, 1e-6, 1000)
psi = geometry.wave_function(x, t=0.001)

# Analyze coherence
coherence_analyzer = CoherenceMaximality(geometry)
spectral_map = coherence_analyzer.prime_spectral_map(n_primes=20)
```

## 📊 Demonstrations

### Run Full Validation

```bash
python scripts/validate_spiral_light.py
```

This generates comprehensive validation plots:
- Spiral paths for different primes
- Zeta zero spectral layers
- Interference patterns over time
- Angular deviation analysis
- Coherence maximality plots

Output saved to: `results/spiral_light_validation/`

### Run Interactive Demo

```bash
python examples/demo_spiral_light.py
```

This shows:
1. Basic spiral light paths
2. Prime modulation effects
3. Zeta zero spectral structure
4. Interference patterns
5. Coherence maximality principle
6. Angular deviations

## 🧮 API Reference

### Classes

#### `SpiralLightGeometry`

Main class for spiral light geometry calculations.

**Methods:**
- `get_primes(n)` - Get first n prime numbers
- `get_zeta_zeros(n)` - Get first n non-trivial zeta zeros
- `prime_phase_modulation(prime_index)` - Calculate phase from prime
- `spiral_path(t, params)` - Generate spiral path coordinates
- `zeta_spectral_frequencies(n_zeros)` - Frequencies from zeta zeros
- `wave_function(x, t, params)` - Calculate ζ-spectral wave function
- `interference_pattern(x, y, t, params)` - 2D interference intensity
- `spiral_deviation_angle(x, y, params)` - Angular deviation Δθ

#### `CoherenceMaximality`

Analysis of coherence maximality principle.

**Methods:**
- `prime_spectral_map(n_primes)` - Generate prime spectral map
- `coherence_measure(psi)` - Calculate coherence measure
- `maximum_coherence_path(t_array, n_primes)` - Find optimal prime

### Data Classes

#### `SpiralPathParams`

Parameters for spiral path generation:
- `r0` - Initial radius (default: 1.0)
- `lambda_expansion` - Fractal expansion index (default: 0.001)
- `f0` - Fundamental frequency (default: 141.7001 Hz)
- `prime_index` - Which prime to use (default: 1)

#### `WaveFunctionParams`

Parameters for wave function:
- `n_primes` - Number of prime nodes (default: 10)
- `n_zeros` - Number of zeta zeros (default: 5)
- `precision` - mpmath precision (default: 50)

## 🧪 Testing

### Run Basic Tests

```bash
python scripts/test_spiral_light_basic.py
```

Tests include:
- Prime number generation
- Riemann zeta zero calculation
- Spiral path generation and expansion
- Wave function normalization
- Interference pattern generation
- Coherence measure
- Spectral frequencies
- Prime phase modulation

### Run Full Test Suite (with pytest)

```bash
pytest tests/test_spiral_light_geometry.py -v
```

Test categories:
- `TestSpiralLightGeometry` - Core geometry tests
- `TestCoherenceMaximality` - Coherence analysis tests
- `TestConvenienceFunctions` - Helper function tests
- `TestPhysicalConsistency` - Physical validity tests
- `TestEdgeCases` - Boundary condition tests
- `TestReproducibility` - Determinism tests

## 📈 Performance Notes

### Precision vs. Speed

The `precision` parameter controls mpmath accuracy for zeta zero calculations:
- **precision=30** - Fast, suitable for most applications (~10⁻¹⁰ accuracy)
- **precision=50** - Standard, good balance (~10⁻¹⁶ accuracy)
- **precision=100** - High precision for verification (~10⁻³² accuracy)

### Recommended Settings

For typical calculations:
```python
geometry = SpiralLightGeometry(precision=30)
params = WaveFunctionParams(n_primes=10, n_zeros=5)
```

For publication-quality results:
```python
geometry = SpiralLightGeometry(precision=100)
params = WaveFunctionParams(n_primes=50, n_zeros=20)
```

## 🔬 Scientific Context

### Connection to QCAL Framework

This module is part of the **Quantum Coherence and Love (QCAL)** framework, which proposes that:

1. The fundamental frequency **f₀ = 141.7001 Hz** governs quantum coherence
2. Mass, energy, space, and time are manifestations of oscillatory patterns
3. Consciousness emerges at the intersection of electromagnetic and spectral bundles

The spiral light geometry provides the **geometric foundation** for how information and energy propagate through this coherent field.

### Theoretical Implications

1. **Non-Euclidean Light Propagation**
   - Light paths are not geodesics in flat spacetime
   - Spiral geometry emerges from prime-modulated phases

2. **Zeta Function as Physical Operator**
   - Riemann zeta zeros are not just mathematical abstractions
   - They define physical spectral layers through which light propagates

3. **Prime Numbers as Physical Resonators**
   - Primes are not arbitrary mathematical objects
   - They represent fundamental vibrational nodes in nature

4. **Coherence as Fundamental Property**
   - Speed of light c is not just velocity, but **maximum coherence**
   - Only paths following prime spectral map achieve frictionless propagation

## 📚 References

### Mathematical Foundation
- Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen Größe"
- Edwards, H.M. (1974). "Riemann's Zeta Function"
- Conrey, J.B. (2003). "The Riemann Hypothesis"

### QCAL Framework
- See main repository documentation at [motanova84/141hz](https://github.com/motanova84/141hz)
- QCAL Constants: `qcal/constants.py`
- Unified Theory: `qcal/unified_theory.py`

### Experimental Validation
- LIGO/Virgo gravitational wave detectors
- LISA (Laser Interferometer Space Antenna)
- GEO600 detector specifications
- High-Q optical cavity experiments

## 🤝 Contributing

Contributions are welcome! Areas of interest:

1. **Experimental Validation**
   - Design experiments to test spiral light predictions
   - Analyze existing interferometry data for spiral signatures

2. **Numerical Optimization**
   - Improve performance of zeta zero calculations
   - GPU acceleration for interference pattern generation

3. **Theoretical Extensions**
   - 3D spiral geometry
   - Relativistic formulation
   - Quantum field theory integration

4. **Documentation**
   - Add more examples
   - Improve explanations
   - Create tutorials

## 📄 License

MIT License - See LICENSE file in repository root

## 🙏 Acknowledgments

- José Manuel Mota Burruezo - Original QCAL framework and theory
- QCAL ∞³ research community
- mpmath library for high-precision zeta function calculations

---

**"El patrón de interferencia no es el resultado del azar cuántico,  
sino el eco de la coherencia primordial,  
doblada por los ceros de zeta,  
guiada por los primos,  
y proyectada sobre el tiempo como una espiral viva."**
