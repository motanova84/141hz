# Coherencia Descendente - Quick Start

## Overview

**Coherencia Descendente** (Descending Coherence Cascade) is a mechanism in the QCAL ∞³ Emotional Field framework that models how collective coherence propagates down through hierarchical levels:

- **Macro** (Collective): Ψ_col = (1/N) Σᵢ Ψᵢ
- **Meso** (Groups): Ψ_group_j = (1/n_j) Σᵢ∈G_j Ψᵢ
- **Micro** (Individual): Ψᵢ

The 141.7 Hz QCAL fundamental frequency acts as a universal synchronizer across all levels.

---

## Installation

The module is part of the QCAL emotional field framework:

```bash
# Already included in the repository
cd /path/to/141hz
```

Requires: `numpy`, `scipy`

---

## Quick Example

```python
from qcal.emotional_field.descending_coherence import (
    DescendingCoherencePropagator,
    create_example_cascade
)

# Create a 60-node network with 6 groups
propagator, coherences, connections = create_example_cascade(
    num_nodes=60,
    num_groups=6,
    initial_coherence=0.5
)

# Define stress levels
stress_levels = {i: 0.3 for i in range(60)}

# Detect meso-level groups
groups = propagator.detect_groups(
    list(range(60)),
    connections,
    stress_levels
)
print(f"Detected {len(groups)} groups")

# Simulate cascade evolution
dt = 0.01  # 10 ms time steps
for step in range(500):
    coherences = propagator.propagate_coherence(coherences, stress_levels, dt)
    
    if step % 100 == 0:
        summary = propagator.get_summary()
        print(f"Step {step}: Ψ_col = {summary['collective_coherence']:.4f}")

# Final results
final_summary = propagator.get_summary()
print(f"\nFinal collective coherence: {final_summary['collective_coherence']:.4f}")
print(f"Mean alignment: {final_summary['alignment_metrics']['mean_alignment']:.4f}")
```

---

## Understanding the Hierarchy

### Micro Level (Individual)

Each node i has individual coherence Ψᵢ:

```python
info = propagator.get_hierarchy_info(node_id=0)
print(f"Individual coherence: {info['micro']['coherence']:.4f}")
print(f"Individual phase: {info['micro']['phase']:.4f} rad")
```

### Meso Level (Group)

Nodes belong to groups with average coherence:

```python
print(f"Group ID: {info['meso']['group_id']}")
print(f"Group coherence: {info['meso']['coherence']:.4f}")
```

### Macro Level (Collective)

Global average across all nodes:

```python
print(f"Collective coherence: {info['macro']['coherence']:.4f}")
```

### Target Coherence

What the individual is drawn toward:

```python
print(f"Target coherence: {info['target']['coherence']:.4f}")
```

The target is a weighted combination:
```
Ψ_target = 0.4·Ψ_col + 0.35·Ψ_group + 0.25·Ψᵢ
```

---

## Cascade Dynamics

The evolution follows:

```
∂Ψᵢ/∂t = -γᵢ(Ψᵢ - Ψ_target) + ηᵢ·sin(2πf₀t)
```

Where:
- **γᵢ**: Relaxation rate (modulated by stress)
- **Ψ_target**: Hierarchical target from macro/meso/micro
- **f₀ = 141.7 Hz**: QCAL fundamental frequency
- **ηᵢ**: Resonance amplitude

### Stress Modulation

High stress reduces collective influence:

```python
# Stress reduces effective relaxation rate
gamma_eff = gamma_0 * (1 - beta * T_00)
```

This preserves individual autonomy under stress.

---

## Custom Parameters

Customize coupling coefficients (must sum to 1.0):

```python
from qcal.emotional_field.descending_coherence import (
    DescendingCoherenceParameters
)

params = DescendingCoherenceParameters(
    alpha_macro=0.5,   # More collective influence
    alpha_meso=0.3,    # Less group influence
    alpha_micro=0.2,   # Less individual autonomy
    
    gamma_individual=0.3,  # Slower relaxation
    eta_individual=0.2,    # Stronger resonance
)

propagator = DescendingCoherencePropagator(params)
```

---

## Monitoring Alignment

Track how well individuals follow the cascade:

```python
alignment = propagator.compute_coherence_alignment()
print(f"Mean alignment: {alignment['mean_alignment']:+.4f}")
print(f"Std alignment: {alignment['std_alignment']:.4f}")
```

Alignment ranges from -1 (anti-aligned) to +1 (fully aligned).

Values near +1 indicate successful cascade propagation.

---

## Running Demonstrations

### Built-in Demo
```bash
python qcal/emotional_field/descending_coherence.py
```

### Full Example
```bash
python examples/demo_descending_coherence.py
```

Output shows:
- Initial and final coherence statistics
- Convergence analysis (spread reduction)
- Example node hierarchies
- Alignment metrics

---

## Key Insights

### 1. Collective Influence Without Control

The cascade creates an "attractor field" that influences individuals while preserving autonomy (α_micro = 25%).

### 2. Group Mediation

Meso-level groups mediate between collective and individual, making the cascade more realistic (people respond to their immediate community, not just global averages).

### 3. Stress Resistance

High individual stress reduces susceptibility to collective influence, preventing forced coherence in traumatic states.

### 4. 141.7 Hz Synchronization

The fundamental QCAL frequency acts as a universal clock, enabling phase locking across hierarchical levels.

### 5. Emergent Order

Collective coherence both emerges from and influences individual states—a true bidirectional relationship.

---

## Integration with Emotional Field

The cascade integrates with:

1. **Stress Tensor** - Uses T_00 for stress modulation
2. **Synchronization Protocol** - 141.7 Hz resonance drive
3. **Network Topology** - Group detection via community structure
4. **Emotional Potential** - Couples to V(Φ) dynamics

---

## Testing

Run the test suite:

```bash
python tests/test_descending_coherence.py
```

21 tests cover:
- Parameter validation
- Group formation
- Coherence propagation
- Hierarchical state tracking
- Alignment computation
- Convergence behavior

All tests should pass ✅

---

## Further Reading

- `IMPLEMENTATION_SUMMARY_COHERENCIA_DESCENDENTE.md` - Complete implementation details
- `qcal/emotional_field/README.md` - Emotional field framework overview
- `qcal/emotional_field/descending_coherence.py` - Source code with detailed docstrings

---

## Citation

If you use this module, please cite:

```bibtex
@software{qcal_descending_coherence,
  title = {QCAL ∞³ Descending Coherence Cascade},
  author = {Instituto Consciencia Cuántica},
  year = {2026},
  url = {https://github.com/motanova84/141hz}
}
```

---

**Date**: February 13, 2026  
**Version**: 1.1.0  
**Status**: Production Ready ✅
