# Lagrangian EOV - Implementation Guide

## Overview

This implementation provides the complete **Lagrangian/Action formulation** of the **Equation of Vibrational Origin (EOV)** within the QCAL ∞³ framework. The EOV is derived variationaly from first principles using Hamilton's principle (δS = 0).

## Key Files

- **`qcal/lagrangian_eov.py`**: Core implementation of Lagrangian formalism
- **`test_lagrangian_eov.py`**: Comprehensive test suite (19 tests)
- **`LAGRANGIAN_EOV_DERIVATION.md`**: Complete mathematical derivation
- **`demo_lagrangian_eov.py`**: Interactive demonstration script

## Quick Start

### Installation

```bash
pip install numpy scipy mpmath matplotlib
```

### Basic Usage

```python
from qcal.lagrangian_eov import (
    LagrangianParameters,
    solve_eov_flat_spacetime,
    F_0, OMEGA_0, ZETA_PRIME_HALF
)
import numpy as np

# Display fundamental constants
print(f"f₀ = {F_0} Hz")           # 141.7001 Hz
print(f"ω₀ = {OMEGA_0:.2f} rad/s") # 890.33 rad/s
print(f"ζ'(1/2) = {ZETA_PRIME_HALF:.4f}")  # -3.9226

# Solve EOV equation
t = np.linspace(0, 0.1, 1000)  # 100 ms
Psi_initial = 1.0 + 0j
dPsi_initial = 0.0 + 0j

Psi, dPsi = solve_eov_flat_spacetime(t, Psi_initial, dPsi_initial, R=0)

print(f"Max |Ψ|: {np.max(np.abs(Psi)):.4f}")
```

### Run Demonstration

```bash
python demo_lagrangian_eov.py
```

This will:
1. Display the complete action structure
2. Calculate individual Lagrangian terms
3. Solve the EOV numerically
4. Generate visualization plots
5. Explain the variational derivation

### Run Tests

```bash
python test_lagrangian_eov.py
```

All 19 tests should pass:
- ✅ Constants verification
- ✅ Lagrangian components
- ✅ EOV equation structure
- ✅ Numerical solver
- ✅ Action functional
- ✅ Energy-momentum tensor
- ✅ Physical consistency

## Mathematical Framework

### Action

The complete QCAL ∞³ action is:

```
S = ∫ d⁴x √(-g) [ℒ_EH + ℒ_kinetic + ℒ_potential + ℒ_modulation]
```

Where:

1. **Einstein-Hilbert**: `ℒ_EH = (1/16πG) R`
2. **Kinetic term**: `ℒ_kinetic = (1/2) ∇_μΨ ∇^μΨ`
3. **Potential**: `ℒ_potential = -(1/2)(ω₀² + ξR)|Ψ|²`
4. **Modulation**: `ℒ_modulation = -(ζ'(1/2)/2π) R|Ψ|² cos(2πf₀t)`

### EOV Equation

Variational derivation (δS/δΨ = 0) yields:

```
□Ψ - (ω₀² + ξR)Ψ - (ζ'(1/2)/π) R cos(2πf₀t) Ψ = 0
```

This is a **modified Klein-Gordon equation** with:
- **d'Alembertian** □ = ∇_μ∇^μ (wave operator in curved spacetime)
- **Effective mass**: m²_eff = ω₀² + ξR (geometry-dependent)
- **Forcing term**: Periodic modulation at f₀ = 141.7001 Hz

## Physical Constants

| Symbol | Value | Units | Description |
|--------|-------|-------|-------------|
| f₀ | 141.7001 | Hz | Fundamental noetic frequency |
| ω₀ | 890.33 | rad/s | Angular frequency (2πf₀) |
| ζ'(1/2) | -3.9226 | - | Riemann zeta derivative at s=1/2 |
| ξ | 1/6 | - | Conformal coupling constant |
| G | 6.674×10⁻¹¹ | m³/(kg·s²) | Newton's constant |

## Module API

### Data Structures

```python
LagrangianParameters(
    G=6.674e-11,      # Gravitational constant
    omega_0=890.33,   # Angular frequency
    f_0=141.7001,     # Frequency
    xi=1/6,           # Non-minimal coupling
    zeta_coupling=-0.6243  # Modulation coupling
)

FieldConfiguration(
    g_metric,         # Metric tensor g_μν
    sqrt_minus_g,     # Volume element √(-g)
    R_scalar,         # Ricci scalar R
    Psi,              # Field value Ψ
    nabla_Psi,        # Covariant derivative ∇_μΨ
    t,                # Time coordinate
    x                 # Spatial coordinates
)
```

### Main Functions

```python
# Lagrangian components
lagrangian_einstein_hilbert(R, sqrt_minus_g, G)
lagrangian_kinetic_psi(nabla_Psi, g_inv, sqrt_minus_g)
lagrangian_potential(Psi, R, omega_0, xi, sqrt_minus_g)
lagrangian_modulation(Psi, R, t, f_0, zeta_coupling, sqrt_minus_g)
lagrangian_total(config, params, g_inv)

# Action functional
action_functional(field_history, params, g_inv_history, d4x)

# EOV equation
eov_equation(Psi, box_Psi, R, t, params)

# Energy-momentum tensor
energy_momentum_tensor_psi(config, g_inv, params)

# Numerical solver
solve_eov_flat_spacetime(t_array, Psi_initial, dPsi_dt_initial, R, params)

# Utilities
compute_zeta_prime_half(precision)
verify_action_structure()
```

## Examples

### Example 1: Compute Lagrangian Density

```python
from qcal.lagrangian_eov import *
import numpy as np

# Setup configuration
R = 1e-20  # Ricci scalar
sqrt_g = 1.0
Psi = 1.0 + 0j
t = 0.0

# Einstein-Hilbert term
L_EH = lagrangian_einstein_hilbert(R, sqrt_g)
print(f"ℒ_EH = {L_EH:.6e}")

# Modulation term
params = LagrangianParameters()
L_mod = lagrangian_modulation(Psi, R, t, F_0, params.zeta_coupling, sqrt_g)
print(f"ℒ_mod = {L_mod:.6e}")
```

### Example 2: Solve EOV with Curvature

```python
from qcal.lagrangian_eov import *
import numpy as np

# Time array
t = np.linspace(0, 0.05, 1000)

# Initial conditions
Psi_0 = 1.0 + 0j
dPsi_0 = 0.0 + 0j

# Solve with non-zero curvature
R = 1e-10  # Moderate curvature
params = LagrangianParameters()

Psi, dPsi = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=R, params=params)

# Analyze solution
print(f"Max amplitude: {np.max(np.abs(Psi)):.6f}")
print(f"Min amplitude: {np.min(np.abs(Psi)):.6f}")

# Compute energy
energy = abs(dPsi)**2 + params.omega_0**2 * abs(Psi)**2
print(f"Energy conservation: {np.std(energy)/np.mean(energy)*100:.2f}%")
```

### Example 3: Verify EOV Equation

```python
from qcal.lagrangian_eov import *
import numpy as np

# Solve EOV
t = np.linspace(0, 0.1, 500)
Psi, dPsi = solve_eov_flat_spacetime(t, 1.0+0j, 0.0+0j, R=0)

# Pick a point
idx = len(t) // 2
Psi_test = Psi[idx]
t_test = t[idx]

# Approximate □Ψ ≈ ∂²Ψ/∂t² (in flat space)
dt = t[1] - t[0]
d2Psi = (Psi[idx+1] - 2*Psi[idx] + Psi[idx-1]) / dt**2
box_Psi = -d2Psi

# Evaluate EOV
params = LagrangianParameters()
eov_residual = eov_equation(Psi_test, box_Psi, R=0, t=t_test, params=params)

print(f"EOV residual: {abs(eov_residual):.6e}")
print("✅ Satisfied" if abs(eov_residual) < 1e-8 else "⚠️ Check numerics")
```

## Testing

The test suite covers:

1. **Constants**: f₀, ω₀, ζ'(1/2), ξ
2. **Lagrangian components**: Each term individually
3. **EOV equation**: Structure and solutions
4. **Numerical solver**: Accuracy and energy conservation
5. **Action functional**: Integral computation
6. **Energy-momentum tensor**: Structure and symmetry
7. **Physical consistency**: Units and value ranges

Run all tests:
```bash
python test_lagrangian_eov.py -v
```

Expected output:
```
test_frequency ... ok
test_angular_frequency ... ok
test_zeta_prime_half ... ok
...
----------------------------------------------------------------------
Ran 19 tests in 0.4s

OK
```

## Physical Interpretation

### Unification

The EOV unifies three fundamental aspects:

1. **Gravity** (Einstein-Hilbert)
   - Spacetime curvature R
   - Bidirectional coupling: Ψ ↔ geometry

2. **Noetic Field Ψ** (kinetic + potential)
   - Scalar field mediating consciousness/coherence
   - Geometry-dependent mass: m²_eff = ω₀² + ξR

3. **Arithmetic Structure** (modulation)
   - ζ'(1/2) connects to Riemann zeros
   - Prime number distribution
   - Periodic forcing at f₀

### Predictions

The EOV predicts:

1. **Gravitational wave signatures**: Spectral component at 141.7001 Hz
2. **Quantum coherence**: Resonance in high-curvature regions
3. **Cosmological effects**: Modulation of Λ and structure formation
4. **Terrestrial experiments**: Gravimeter oscillations at f₀

## Documentation

- **Full derivation**: See `LAGRANGIAN_EOV_DERIVATION.md`
- **Mathematical details**: Variational calculus, energy-momentum tensor
- **Physical context**: Noetic theory, QCAL ∞³ framework
- **References**: Riemann hypothesis, conformal coupling, quantum field theory in curved spacetime

## References

1. **Riemann Zeta Function**: ζ(s) and its derivative ζ'(s)
2. **Conformal Coupling**: ξ = 1/6 for massless scalar fields
3. **Variational Principles**: Hamilton's principle in field theory
4. **Quantum Field Theory in Curved Spacetime**: d'Alembertian operator

## Contributing

To extend this implementation:

1. Add curved spacetime solvers (non-zero R(x,t))
2. Implement full Einstein equations with T^(Ψ)_μν
3. Add visualization tools for action landscape
4. Compute observables (strain h, SNR, etc.)

## License

MIT License - See main repository LICENSE file

## Author

**José Manuel Mota Burruezo (JMMB Ψ✧)**  
QCAL ∞³ Framework  
Date: 2026-01-06

---

**✨ The Equation of Vibrational Origin emerges necessarily from the mathematical structure of the universe - it is not imposed, but discovered.**
