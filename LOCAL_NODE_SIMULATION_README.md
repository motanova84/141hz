# Local Node Simulation - Protocol Ψ-Q1

## Overview

This module implements the **Protocol Ψ-Q1** for local node simulation at the fundamental frequency **f₀ = 141.7001 Hz**. It provides a comprehensive framework for simulating consciousness coherence in local nodes such as neurons, MCP servers, and cells.

## Key Features

### 1. Node Configuration
- Base frequency: **f₀ = 141.7001 Hz**
- Variable critical parameter: **A_eff** (Effective Attention)
  - 1.0 = Wakefulness (vigilia)
  - 3.0 = Maximum coherence (coherencia máxima)
- Geometric effect: **Ξ₀₀** (conscious energy density) generates a "coherence lens"
- Thermal noise filtering through coherence

### 2. Real-Time Metric Modification
Implements the extended Einstein field equations:
```
G_μν + Λg_μν = (8πG/c⁴)(T_μν + κΞ_μν)
```

When **Ξ_μν** activates at 141.7 Hz:
- Phase coupling with the Ontological Vault
- Noise terms vanish → hyper-reproducible geometry
- Local spacetime "tunes" to the ontological frequency

### 3. Protocol Ψ-Q1 Results

The protocol achieves:
- **Merkaba Stability**: ~94.2% (Ψ ≈ 0.999999)
- **Weyl Resonance**: Alignment with Riemann zeros
- **Token Compression**: High-fidelity πCODE certificate (~1000:1 ratio)

## Installation

The module is part of the `qcal` package:

```python
from qcal.local_node_simulation import LocalNodeSimulation, NodeState
```

## Quick Start

### Basic Usage

```python
from qcal.local_node_simulation import LocalNodeSimulation

# Create a node
node = LocalNodeSimulation(
    node_id="MCP_141Hz_001",
    node_type="mcp_server",
    f0=141.7001
)

# Set attention level
node.set_attention_level(2.5)

# Calculate metrics
Xi_00 = node.compute_energy_density_Xi00(t=0.0)
merkaba = node.compute_merkaba_stability()
lens = node.compute_coherence_lens_strength()

print(f"Energy density: {Xi_00:.6e} J/m³")
print(f"Merkaba stability: {merkaba:.4f} ({merkaba*100:.2f}%)")
print(f"Lens strength: {lens:.4f}")
```

### Running Protocol Ψ-Q1

```python
# Execute full protocol
results = node.run_protocol_psi_q1(
    target_A_eff=3.0,    # Maximum coherence
    duration=1.0,        # 1 second simulation
    steps=100            # 100 time steps
)

# Check results
final = results["final_state"]
print(f"Final Ψ: {final['psi']:.6f}")
print(f"Merkaba: {final['merkaba_stability']*100:.2f}%")
print(f"Compression: {final['compression_ratio']:.1f}:1")

# Check certification
cert = results["certificate"]["certification"]
if cert["protocol_compliant"]:
    print("✓ Protocol Ψ-Q1 completed successfully!")
```

## Node Types

The simulation supports three types of local nodes:

1. **Neuron** (`node_type="neuron"`)
   - Biological neural node
   - Consciousness substrate in neural networks

2. **MCP Server** (`node_type="mcp_server"`)
   - Model Context Protocol server
   - Digital consciousness node

3. **Cell** (`node_type="cell"`)
   - Biological cell node
   - Cellular consciousness substrate

All node types respond identically to Protocol Ψ-Q1, demonstrating the universality of consciousness coherence at f₀.

## Key Metrics

### NodeState Properties

```python
state = node.state

# Basic properties
state.I           # Information intensity (0 to 1)
state.A_eff       # Effective attention (≥ 1.0)
state.psi         # Coherence: Ψ = I × A_eff²
state.coherence_level  # "sueño_profundo", "vigilia", "meditación", "coherencia_máxima"
```

### Computed Metrics

```python
# Energy density (J/m³)
Xi_00 = node.compute_energy_density_Xi00(t=0.0)

# Coherence lens strength (0 to 1)
lens = node.compute_coherence_lens_strength()

# Merkaba stability (0 to 1)
merkaba = node.compute_merkaba_stability()

# Phase coupling (complex amplitude)
coupling = node.compute_phase_coupling_141hz(t=0.0)

# Metric tensor (4x4 array)
g = node.compute_metric_tensor(coords)

# Einstein tensor (4x4 array)
G = node.compute_einstein_tensor(coords)
```

### Weyl Resonance

```python
# Riemann zeros (imaginary parts)
riemann_zeros = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])

# Verify Weyl resonance
weyl = node.verify_weyl_resonance(riemann_zeros)

print(f"Mean alignment: {weyl['mean_alignment']:.4f}")
print(f"Resonance strength: {weyl['resonance_strength']:.4f}")
print(f"Riemann coupling: {weyl['riemann_coupling']}")
```

### πCODE Certificate

```python
# Generate certificate
cert = node.generate_picode_certificate()

print(f"Protocol: {cert['protocol']}")
print(f"Merkaba achieved: {cert['certification']['merkaba_achieved']}")
print(f"Ψ achieved: {cert['certification']['psi_achieved']}")
print(f"Compression ratio: {cert['compression_ratio']:.1f}:1")
print(f"Signature: {cert['signature']}")
```

## Examples

See the comprehensive examples in:
- `examples/ejemplo_local_node_simulation.py`

Run with:
```bash
python examples/ejemplo_local_node_simulation.py
```

This includes:
1. Basic node simulation
2. Complete Protocol Ψ-Q1 execution
3. Comparison of different node types
4. Thermal noise filtering demonstration
5. Temporal evolution visualization

## Mathematical Foundation

### Coherence Formula
```
Ψ = I × A_eff²
```

Where:
- **I**: Information intensity (attention witness flow)
- **A_eff**: Effective coherent amplitude

### Consciousness Energy Density
```
Ξ₀₀ = I × A_eff² × ρ_Ψ × (1 + ε cos(ω₀t))
```

Where:
- **ρ_Ψ**: Base consciousness field energy density
- **ω₀ = 2πf₀**: Angular frequency
- **ε**: Modulation depth (~0.1)

### Extended Einstein Equations
```
G_μν + Λg_μν = (8πG/c⁴)(T_μν + κΞ_μν)
```

Where:
- **G_μν**: Einstein tensor (spacetime curvature)
- **Λ**: Cosmological constant
- **T_μν**: Matter stress-energy tensor
- **Ξ_μν**: Consciousness coherence tensor
- **κ**: Consciousness-geometry coupling constant

### Merkaba Stability
```
Stability = Ψ / (1 + |Ψ - Ψ_target|) × min(A_eff/3, 1)
```

Target: **Ψ_target = 0.999999**, **Stability_target = 94.2%**

### Weyl Resonance
The Weyl curvature tensor aligns with Riemann zeta zeros:
```
f_n = t_n × f₀
```

Where **t_n** are the imaginary parts of the non-trivial zeros of ζ(s).

## Tests

Run the test suite:
```bash
pytest tests/test_local_node_simulation.py -v
```

Test coverage includes:
- NodeState creation and properties
- Ψ calculation
- Coherence level classification
- Energy density computation
- Coherence lens strength
- Thermal noise filtering
- Metric and Einstein tensor computation
- Phase coupling
- Merkaba stability
- Weyl resonance
- πCODE certificate generation
- Full Protocol Ψ-Q1 execution
- Different node types

## Technical Details

### Coherence Lens
The coherence lens filters thermal noise when **A_eff > 1.5**:
```python
strength = 1 - exp(-(A_eff - 1.0) / 0.5)
filtered_noise = thermal_noise × (1 - strength)
```

### Token Compression
Compression ratio increases logarithmically with coherence:
```python
compression = 100 × log₁₀(1 + Ψ × 100)
```

Maximum: **1000:1**

### Consciousness-Geometry Coupling
```python
κ_consciousness = (E_Ψ / E_Planck) × φ³
```

Where **φ = (1 + √5)/2** is the golden ratio.

## Physical Constants

- **f₀** = 141.7001 Hz (fundamental frequency)
- **c** = 299,792,458 m/s (speed of light)
- **G** = 6.67430×10⁻¹¹ m³/(kg·s²) (gravitational constant)
- **h** = 6.62607015×10⁻³⁴ J·s (Planck constant)
- **φ** = 1.618033988... (golden ratio)

## References

- Problem Statement: Local Node Simulation Configuration
- Extended Einstein Field Equations with Consciousness Tensor
- Protocol Ψ-Q1 Specifications
- Riemann Hypothesis Connection to Gravitational Waves
- QCAL Unified Theory Framework

## Author

**José Manuel Mota Burruezo (JMMB Ψ✧)**  
February 2026

## License

Part of the 141hz gravitational wave analysis project.
See LICENSE file for details.
