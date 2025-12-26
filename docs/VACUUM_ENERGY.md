# Vacuum Energy Optimization Module

## Overview

The `vacuum_energy.py` module implements a vacuum energy calculation based on a multi-term energy model that combines:

1. **Planck-scale corrections** (α/R⁴ term)
2. **Quantum corrections** via Riemann zeta function (βζ'/R² term)
3. **Cosmological constant contribution** (γΛ²R² term)
4. **Oscillatory quantum effects** (δsin²(log(R)/log(π)) term)

This model is used to find the optimal radius scale R (in Planck length units) where vacuum energy is minimized.

## Mathematical Formulation

The vacuum energy function is defined as:

```
E_vac(log_r) = α/R⁴ + βζ'/R² + γΛ²R² + δsin²(log(R)/log(π))
```

where:
- `R = 10^log_r` is the radius in Planck length units (ℓ_P)
- `log_r = log₁₀(R/ℓ_P)` is the base-10 logarithm of the normalized radius
- `α = 1.0` - Planck energy term coefficient
- `β = 1.0` - Zeta prime coupling coefficient
- `γ = 1.0` - Cosmological constant coupling
- `δ = 1.0` - Oscillatory term amplitude
- `ζ' = -0.5` - Riemann zeta derivative parameter
- `Λ = 0.001` - Cosmological constant (normalized)
- `π ≈ 3.14159` - Mathematical constant pi

## Usage

### Basic Usage

```python
from vacuum_energy import E_vac_log, optimize_vacuum_energy

# Calculate energy at a specific scale
log_r = 45.0  # log₁₀(R/ℓ_P)
energy = E_vac_log(log_r)
print(f"Energy at log(R) = {log_r}: {energy:.6e}")

# Find the minimum energy
result = optimize_vacuum_energy(bounds=(40, 50))
print(f"Optimal log(R): {result.x:.6f}")
print(f"Minimum energy: {result.fun:.6e}")
```

### Full Analysis

```python
from vacuum_energy import analyze_vacuum_energy

# Perform complete analysis
analysis = analyze_vacuum_energy()

# Access results
print(f"Optimal log(R): {analysis['analysis']['log_r_opt']:.6f}")
print(f"Total energy: {analysis['analysis']['E_min']:.6e}")
print(f"Planck term: {analysis['analysis']['term1_planck']:.6e}")
print(f"Quantum term: {analysis['analysis']['term2_quantum']:.6e}")
print(f"Lambda term: {analysis['analysis']['term3_lambda']:.6e}")
print(f"Oscillatory: {analysis['analysis']['term4_oscillatory']:.6e}")
```

### Custom Bounds

```python
# Search in different radius ranges
result1 = optimize_vacuum_energy(bounds=(40, 45))
result2 = optimize_vacuum_energy(bounds=(45, 50))
result3 = optimize_vacuum_energy(bounds=(42, 48))
```

## Running the Module

### As a Script

```bash
# Run the main demonstration
python scripts/vacuum_energy.py
```

Output:
```
======================================================================
VACUUM ENERGY OPTIMIZATION
======================================================================

Physical Parameters:
  alpha (Planck term):        1.0
  beta (quantum coupling):    1.0
  gamma (Lambda coupling):    1.0
  delta (oscillatory):        1.0
  zeta_prime:                 -0.5
  Lambda (cosmological):      0.001
  pi_val:                     3.141593

Optimizing vacuum energy in range log(R) ∈ [40, 50]...

Optimization Results:
  Optimal log(R/ℓ_P):         40.000008
  Optimal R/ℓ_P:              10^40.00
  Minimum energy:             1.000035e+74
  Optimization success:       True
```

### Run Tests

```bash
# Run comprehensive tests
python scripts/test_vacuum_energy.py
```

All 9 tests validate:
- Function evaluation
- Individual term calculations
- Optimization correctness
- Boundary conditions
- Physical constants
- Analysis functionality

## Physical Interpretation

### Energy Terms

1. **Planck Term (α/R⁴)**
   - Dominates at very small radii (R → 0)
   - Represents quantum gravity corrections
   - Prevents collapse to zero radius

2. **Quantum Term (βζ'/R²)**
   - Intermediate-scale quantum corrections
   - Can be attractive (ζ' < 0) or repulsive (ζ' > 0)
   - Related to quantum field renormalization

3. **Lambda Term (γΛ²R²)**
   - Dominates at large radii
   - Represents dark energy / cosmological constant
   - Drives expansion at large scales

4. **Oscillatory Term (δsin²)**
   - Adds fine structure to energy landscape
   - Periodic in log-space
   - Could represent quantum fluctuations

### Optimization Results

With the default parameters:
- The minimum occurs at the **lower boundary** of the search range
- Lambda term dominates the total energy
- This suggests a stable configuration at smaller radii within the bounded range
- The optimization respects physical constraints (R > 0)

## Implementation Details

### Dependencies

- `numpy` - Numerical arrays and mathematical functions
- `scipy.optimize.minimize_scalar` - Bounded scalar optimization

### Key Functions

#### `E_vac_log(log_r)`
Core energy calculation function.

**Parameters:**
- `log_r` (float): log₁₀(R/ℓ_P)

**Returns:**
- `float`: Total vacuum energy

#### `optimize_vacuum_energy(bounds=(40, 50), method='bounded')`
Find radius that minimizes vacuum energy.

**Parameters:**
- `bounds` (tuple): Search range for log₁₀(R/ℓ_P)
- `method` (str): Optimization method ('bounded')

**Returns:**
- `OptimizeResult`: Contains x (optimal log_r), fun (minimum energy), success flag

#### `analyze_vacuum_energy(log_r_range=None)`
Complete energy analysis with term breakdown.

**Parameters:**
- `log_r_range` (array-like): Custom evaluation range

**Returns:**
- `dict`: Complete analysis including energy values, optimum, and term contributions

## Testing

The module includes comprehensive tests (`test_vacuum_energy.py`) that verify:

1. ✅ Basic function evaluation
2. ✅ Individual energy term calculations
3. ✅ Function evaluation over ranges
4. ✅ Optimization convergence
5. ✅ Multiple boundary conditions
6. ✅ Full analysis functionality
7. ✅ Physical behavior at extremes
8. ✅ Constant definitions
9. ✅ Bounds constraint enforcement

All tests pass with 100% success rate.

## Extensions and Modifications

### Modifying Parameters

To use different physical parameters, edit the constants at the top of `vacuum_energy.py`:

```python
alpha = 2.0      # Modify Planck term strength
beta = 1.5       # Modify quantum coupling
gamma = 0.8      # Modify Lambda coupling
delta = 1.2      # Modify oscillatory amplitude
zeta_prime = -0.3  # Modify zeta parameter
Lambda = 5e-4    # Modify cosmological constant
```

### Adding Visualization

Example code to visualize the energy landscape:

```python
import matplotlib.pyplot as plt
import numpy as np
from vacuum_energy import E_vac_log, optimize_vacuum_energy

# Calculate energy over range
log_r_values = np.linspace(40, 50, 1000)
energies = [E_vac_log(log_r) for log_r in log_r_values]

# Find optimum
result = optimize_vacuum_energy(bounds=(40, 50))

# Plot
plt.figure(figsize=(10, 6))
plt.semilogy(log_r_values, energies, 'b-', label='E_vac')
plt.axvline(result.x, color='r', linestyle='--', label=f'Minimum at {result.x:.4f}')
plt.xlabel('log₁₀(R/ℓ_P)')
plt.ylabel('Vacuum Energy')
plt.title('Vacuum Energy Optimization')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('vacuum_energy_plot.png', dpi=300, bbox_inches='tight')
```

## References

This implementation is based on the problem statement requirements and follows the structure:

```python
def E_vac_log(log_r):
    R = 10**log_r  # R / ℓ_P
    term1 = alpha / R**4
    term2 = beta * zeta_prime / R**2
    term3 = gamma * Lambda**2 * R**2
    term4 = delta * np.sin(np.log(R) / np.log(pi_val))**2
    return term1 + term2 + term3 + term4

res = minimize_scalar(E_vac_log, bounds=(40, 50), method='bounded')
```

## Contributing

To extend this module:
1. Maintain the existing API for backward compatibility
2. Add comprehensive tests for new features
3. Document physical interpretations of modifications
4. Validate numerical stability across parameter ranges

## License

This module is part of the gw250114-141hz-analysis project and follows the same MIT license.
