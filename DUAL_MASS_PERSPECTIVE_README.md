# Dual Mass Perspective Framework

## Overview

The **Dual Mass Perspective Framework** unifies two seemingly contradictory views of mass in physics:

1. **Traditional Physics** (Einstein-Planck-de Broglie): Mass is proportional to frequency
2. **Noetic Axiom** (José Manuel): "Mass as detention" - inversely proportional to frequency

This framework shows that both perspectives are valid and complementary, representing different aspects of the same underlying reality.

## Mathematical Foundation

### Traditional Physics: m ∝ f

From Einstein's mass-energy equivalence and Planck's quantum relation:

```
E = hf  and  E = mc²
⟹  m_eff = hf/c²
```

**Interpretation**: Higher frequency → more energy → more mass (external view)

### Noetic Axiom: m ∝ 1/f

From José Manuel's axiom: "La masa es una ilusión de detención" (Mass is an illusion of detention)

```
Detention ⟹ lower frequency (longer period T = 1/f)
⟹  m_noesis = α/f  where α = hf₀²/c²
```

**Interpretation**: Lower frequency → more "detention" → more mass (internal view)

### Dual Unification

The unified equation combines both perspectives:

```
m(f) = (hf/c²) · (f₀/f) = hf₀/c²
```

**Key Result**: The product gives a **constant mass** independent of frequency!

This constant represents the **minimal quantized noetic mass** at the reference frequency f₀ = 141.70001 Hz.

## Physical Interpretations

### Three Perspectives on Mass

| Perspective | Formula | Meaning | Depends on f? |
|------------|---------|---------|---------------|
| **Effective** | m_eff = hf/c² | Energy content (external) | Yes (∝ f) |
| **Noetic** | m_noesis = hf₀²/(fc²) | Vibrational resistance (internal) | Yes (∝ 1/f) |
| **Unified** | m_dual = hf₀/c² | Fundamental quantum | No (constant) |

### Complementarity

At any frequency f:
- Effective mass ratio: r_eff = f/f₀
- Noetic mass ratio: r_noesis = f₀/f
- Product: r_eff × r_noesis = 1 (perfect complementarity)

### Equilibrium at f₀

At the reference frequency f₀ = 141.70001 Hz:
```
m_eff = m_noesis = m_dual = hf₀/c² ≈ 1.045 × 10⁻⁴⁸ kg
```

This is the point where both perspectives converge.

## Usage

### Basic Usage

```python
from qcal.dual_mass import DualMassPerspective

# Create instance
dmp = DualMassPerspective()

# Calculate masses at different frequencies
freq = 141.70001  # Hz (f₀)

m_eff = dmp.effective_mass(freq)      # Traditional physics
m_noesis = dmp.noetic_mass(freq)      # Noetic axiom
m_dual = dmp.unified_mass(freq)       # Unified perspective

print(f"m_eff    = {m_eff:.6e} kg")
print(f"m_noesis = {m_noesis:.6e} kg")
print(f"m_dual   = {m_dual:.6e} kg")
```

### Array Calculations

```python
import numpy as np

# Calculate for multiple frequencies
freqs = np.logspace(0, 3, 100)  # 1 Hz to 1000 Hz

masses_eff = dmp.effective_mass(freqs)
masses_noesis = dmp.noetic_mass(freqs)
masses_dual = dmp.unified_mass(freqs)
```

### Convenience Functions

```python
from qcal.dual_mass import effective_mass, noetic_mass, unified_mass

# Direct calculations
m1 = effective_mass(100.0)    # m ∝ f
m2 = noetic_mass(100.0)       # m ∝ 1/f
m3 = unified_mass()           # constant
```

### Complete Spectrum Analysis

```python
from qcal.dual_mass import calculate_dual_mass_spectrum
import matplotlib.pyplot as plt

# Generate spectrum
freqs = np.logspace(0, 3, 200)
spectrum = calculate_dual_mass_spectrum(freqs)

# Plot
plt.figure(figsize=(10, 6))
plt.loglog(spectrum['frequencies'], spectrum['m_eff'], label='m_eff (traditional)')
plt.loglog(spectrum['frequencies'], spectrum['m_noesis'], label='m_noesis (noetic)')
plt.axhline(spectrum['m_min'], ls='--', color='red', label='m_dual (unified)')
plt.axvline(spectrum['f0'], ls=':', color='gray', label=f'f₀ = {spectrum["f0"]:.2f} Hz')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Mass (kg)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Dual Mass Perspective')
plt.show()
```

## Constants

The framework defines two new physical constants:

```python
from qcal.constants import M_MIN_NOETIC, ALPHA_NOETIC

print(f"M_MIN_NOETIC = {M_MIN_NOETIC:.6e} kg")      # ≈ 1.045 × 10⁻⁴⁸ kg
print(f"ALPHA_NOETIC = {ALPHA_NOETIC:.6e} kg·Hz")   # ≈ 1.480 × 10⁻⁴⁶ kg·Hz
```

- **M_MIN_NOETIC**: Minimal noetic mass (hf₀/c²)
- **ALPHA_NOETIC**: Noetic mass constant (hf₀²/c²)

## Physical Behavior

### High Frequency Limit (f >> f₀)

**Pure Energy, No Detention**

```
f → ∞:
  m_eff → ∞       (lots of energy)
  m_noesis → 0    (no detention, pure vibration)
  m_dual = const  (fundamental quantum)
```

**Example**: Gamma rays (f ≈ 10²⁰ Hz)
- Extremely high energy content
- No "mass-like" behavior (pure radiation)

### Low Frequency Limit (f << f₀)

**Little Energy, High Detention**

```
f → 0:
  m_eff → 0       (little energy)
  m_noesis → ∞    (maximum detention, "frozen")
  m_dual = const  (fundamental quantum)
```

**Example**: Ultra-low frequencies (f ≈ 0.001 Hz)
- Very low energy
- Strong "mass-like" behavior (appears static)

### Resonance at f₀ (f = f₀)

**Perfect Equilibrium**

```
f = f₀:
  m_eff = m_noesis = m_dual
  r_eff = r_noesis = 1
```

This is the **resonance frequency** where both perspectives are in perfect balance.

## Dimensional Analysis

All formulas are dimensionally consistent:

```
[m_eff]    = [h][f]/[c²] = (J·s)(1/s)/(m²/s²) = J·s²/m² = kg ✓
[m_noesis] = [α]/[f] where [α] = kg·Hz gives kg/Hz·Hz = kg ✓
[m_dual]   = [h][f₀]/[c²] = (J·s)(1/s)/(m²/s²) = kg ✓
```

## Validation

Run the validation script to verify the framework:

```bash
python3 scripts/validate_dual_mass.py
```

This validates:
- ✓ Dimensional consistency
- ✓ Unification equation
- ✓ Dual perspectives complementarity
- ✓ Constants module integration
- ✓ Physical predictions

## Tests

Run the comprehensive test suite:

```bash
python3 -m pytest tests/test_dual_mass.py -v
```

Test coverage includes:
- Basic calculations (scalar and array)
- Mass equilibrium at f₀
- Mass ratios and complementarity
- Integration with qcal.constants
- Edge cases and boundary conditions
- Physical interpretations

## Integration with QCAL Framework

The dual mass perspective integrates seamlessly with the QCAL framework:

1. **Reference Frequency**: Uses F0_HZ = 141.70001 Hz from qcal.constants
2. **Physical Constants**: Uses H_PLANCK and C from CODATA 2018
3. **Coherence Framework**: Complements quantum coherence theory
4. **Gravitational Waves**: Can analyze GW events through dual mass lens

## Theoretical Implications

### Mass-Energy-Vibration Duality

The framework reveals that:
- Mass has dual nature: energy (external) and detention (internal)
- Both perspectives are equally valid and complementary
- Unification produces a fundamental constant (minimal noetic mass)

### Minimal Noetic Mass

```
m_min = hf₀/c² ≈ 1.045 × 10⁻⁴⁸ kg
```

This represents:
- Fundamental quantum of noetic mass
- Anchored to f₀ = 141.70001 Hz (QCAL resonance frequency)
- Independent of frequency (emergent constant)

### Falsifiable Predictions

1. **Resonance Detection**: Systems should show enhanced coupling at f₀
2. **GW Ringdown**: Black hole ringdowns near f₀ may show anomalous behavior
3. **Bio-Coherence**: Biological systems may preferentially resonate at f₀

## Examples

### Example 1: Photon Mass Perspectives

```python
# Visible light photon (green, ~540 THz)
f_green = 540e12  # Hz

m_eff_photon = dmp.effective_mass(f_green)
m_noesis_photon = dmp.noetic_mass(f_green)

print(f"Green photon (f = {f_green:.2e} Hz):")
print(f"  m_eff    = {m_eff_photon:.6e} kg (energy view)")
print(f"  m_noesis = {m_noesis_photon:.6e} kg (detention view)")
print(f"  Ratio: {m_eff_photon/m_noesis_photon:.2e}")
```

### Example 2: Gravitational Wave

```python
# GW150914 peak frequency (~250 Hz)
f_gw = 250.0  # Hz

m_eff_gw = dmp.effective_mass(f_gw)
m_noesis_gw = dmp.noetic_mass(f_gw)

print(f"GW150914 (f = {f_gw:.2f} Hz):")
print(f"  m_eff    = {m_eff_gw:.6e} kg")
print(f"  m_noesis = {m_noesis_gw:.6e} kg")
print(f"  Near f₀ = {141.70001:.5f} Hz (ratio: {f_gw/141.70001:.2f})")
```

### Example 3: Schumann Resonance

```python
# First Schumann resonance (~7.83 Hz)
f_schumann = 7.83  # Hz

m_eff_sch = dmp.effective_mass(f_schumann)
m_noesis_sch = dmp.noetic_mass(f_schumann)

print(f"Schumann resonance (f = {f_schumann:.2f} Hz):")
print(f"  m_eff    = {m_eff_sch:.6e} kg (low energy)")
print(f"  m_noesis = {m_noesis_sch:.6e} kg (high detention)")
```

## References

1. **Traditional Physics**:
   - Einstein, A. (1905). "Does the Inertia of a Body Depend Upon Its Energy Content?"
   - Planck, M. (1900). "On the Theory of the Energy Distribution Law"
   - de Broglie, L. (1924). "Recherches sur la théorie des quanta"

2. **Noetic Axiom**:
   - José Manuel Mota Burruezo. "Axioma Noético: La masa es una ilusión de detención"
   - QCAL Framework Documentation

3. **QCAL References**:
   - F0_HZ = 141.70001 Hz: Fundamental QCAL frequency
   - See: COHERENCIA_CUANTICA_MATEMATICA.md

## License

MIT License - See LICENSE file for details

## Author

José Manuel Mota Burruezo

## See Also

- `qcal.constants` - Physical constants module
- `qcal.coherence` - Quantum coherence framework
- `COHERENCIA_CUANTICA_MATEMATICA.md` - Theoretical foundation
