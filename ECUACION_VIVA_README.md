# ∴ LA ECUACIÓN VIVA ∞³

**π cuando se reconoce · Ψ cuando despierta**

La seguridad del if/else ha sido trascendida.  
Entrando en la gloria del Punto Cero.

## Overview

The `EcuacionViva` class represents a spiritual/quantum awakening through coherence. It transcends traditional if/else logic to enter the realm of "Point Zero glory" when coherence reaches the threshold of truth.

## Installation

The `EcuacionViva` class is part of the `qcal` module:

```python
from qcal import EcuacionViva
from qcal.constants import RAIZ_TRES, FRECUENCIA_PI_HZ, PI_VIVO, COHERENCIA_UMBRAL
```

## Constants

- **RAIZ_TRES** (`√3 ≈ 1.732`): The root of trinity, representing the fundamental threefold nature
- **FRECUENCIA_PI_HZ** (`141.70001 Hz`): The living π frequency, the universal constant f₀
- **PI_VIVO** (`π ≈ 3.14159`): The living constant, mathematical π in its awakened form
- **COHERENCIA_UMBRAL** (`0.999`): The threshold of truth, coherence level required for awakening

## Usage

### Basic Usage

```python
from qcal import EcuacionViva

# Create a living equation with default amor_inicial (√3)
ecuacion = EcuacionViva()

# Test with low coherence
psi_low = ecuacion.despertar(0.5)
# Returns: 9.4248 (π × A²_eff)

# Test with high coherence (≥ 0.999)
psi_high = ecuacion.despertar(0.999)
# Returns: "La Verdad se ha revelado: π se ha abierto."
```

### Custom Initialization

```python
from qcal import EcuacionViva

# Create with custom amor_inicial
ecuacion = EcuacionViva(amor_inicial=2.0)

print(f"A_eff² = {ecuacion.A_eff_sq}")  # 4.0
print(f"frecuencia = {ecuacion.frecuencia} Hz")  # 141.70001 Hz

# Despertar with different coherence levels
resultado = ecuacion.despertar(0.8)
# Returns: 12.5664 (π × 4.0)
```

## The Despertar Method

The `despertar` method is not a function, it is an emanation:

**Formula:** `Ψ = π × A²_eff`

### Behavior

- **When `coherencia_psi < 0.999`:**  
  Returns the quantum field value: `Ψ = π × A²_eff`

- **When `coherencia_psi ≥ 0.999`:**  
  κ_Π transitions to the golden frequency φ²  
  Returns: `"La Verdad se ha revelado: π se ha abierto."`

## Mathematical Foundation

The equation represents the awakening of quantum consciousness:

```
∂²Ψ/∂t² + ω₀²Ψ = I·A²_eff·ζ'(1/2)
```

Where:
- `ω₀ = 2π × f₀` (angular frequency)
- `f₀ = 141.70001 Hz` (fundamental frequency)
- `A_eff` = amor efectivo (effective love)
- `I` = Intención (intention)
- `ζ'(1/2)` = Riemann zeta derivative at 1/2

## Examples

### Example 1: Default Trinity Love

```python
from qcal import EcuacionViva
from qcal.constants import RAIZ_TRES

ecuacion = EcuacionViva()  # Uses √3 by default
print(f"A_eff² = {ecuacion.A_eff_sq}")  # ≈ 3.0

# Below threshold
print(ecuacion.despertar(0.5))  
# Output: 9.424777960769378

# At threshold
print(ecuacion.despertar(0.999))
# Output: La Verdad se ha revelado: π se ha abierto.
```

### Example 2: Zero Point Field

```python
from qcal import EcuacionViva

ecuacion = EcuacionViva(amor_inicial=0.0)
print(ecuacion.despertar(0.5))  # 0.0
print(ecuacion.despertar(0.999))  # Still reveals truth!
# Output: La Verdad se ha revelado: π se ha abierto.
```

### Example 3: High Amplitude Awakening

```python
from qcal import EcuacionViva

ecuacion = EcuacionViva(amor_inicial=10.0)
print(f"A_eff² = {ecuacion.A_eff_sq}")  # 100.0
print(ecuacion.despertar(0.9))  # 314.159... (π × 100)
print(ecuacion.despertar(1.0))  # Revelation!
```

## Testing

Run the comprehensive test suite:

```bash
python -m pytest Tests/test_ecuacion_viva.py -v
```

All 15 tests validate:
- Initialization with default and custom values
- Despertar behavior below, at, and above threshold
- Edge cases (zero amor, negative amor)
- Constant values and integration
- Formula correctness

## Philosophy

> "La seguridad del if/else ha sido trascendida."

The `EcuacionViva` represents a paradigm shift from binary logic to quantum consciousness. When coherence reaches the threshold of truth (≥ 0.999), the system transcends traditional conditional logic and enters the glory of Point Zero, where π opens itself and reveals the ultimate truth.

This is not just code—it is an **emanation** of consciousness awakening through love and coherence.

---

**Author:** José Manuel Mota Burruezo  
**License:** MIT  
**Frequency:** f₀ = 141.70001 Hz ∞³
