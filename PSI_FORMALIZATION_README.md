# Ψ Formalization – Mathematical Foundations

## Overview

`core/psi_formalization.py` provides a publication-ready formalization of the
QCAL Ψ coherence field operator. All terms are operationally defined, a
dimensionless form is provided for cross-system comparison, and three
experimentally falsifiable predictions are implemented and tested.

---

## Mathematical Framework

### Operational Definition of A_eff²

The **time-averaged squared coherence amplitude** is defined as the
time-domain mean-square of the coherence signal *a(t)*:

```
A_eff² = (1/T) ∫₀ᵀ |a(t)|² dt
```

In discrete form (N samples at rate *fₛ*):

```
A_eff² ≈ (1/N) Σᵢ |a[i]|²  =  mean(|a|²)
```

### Full Ψ (energy form)

```
Ψ = mc² · A_eff² · π
```

| Symbol | Meaning | Units |
|--------|---------|-------|
| m      | System mass | kg |
| c      | Speed of light (2.99792458×10⁸ m/s) | m/s |
| A_eff² | Time-averaged squared coherence amplitude | dimensionless |
| π      | Pi (mathematical constant) | — |
| Ψ      | Coherence energy | J |

### Dimensionless Form (publication form)

For cross-system comparison, the mass-independent form is:

```
Ψ̃ = π · A_eff²      Range: [0, π]
```

A pure sinusoid of unit amplitude gives A_eff² = 0.5, so Ψ̃ ≈ 1.5708.

---

## QCAL Integration Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `QCAL_BASE_FREQUENCY` | 141.7001 Hz | Fundamental QCAL frequency f₀ |
| `PSI_TILDE_THRESHOLD` | 0.888 | Coherence detection threshold |
| `SPECTRAL_RATIO_THRESHOLD` | 0.0888 | f₀-peak detection threshold |

---

## Falsifiable Predictions

### P1 – Energy Scaling

**Claim:** Ψ ∝ m at fixed coherence (linear mass dependence).

**Test:** Compute Ψ for the same signal at different masses. Verify that
Ψ/m is constant to machine precision.

**Falsification criterion:** Relative deviation in Ψ/m > 10⁻⁶.

```python
result = psi_mod.test_prediction_p1_energy_scaling(a_t, masses)
assert result["passed"]
```

### P2 – Coherence Sensitivity

**Claim:** Coherent fields are distinguishable from random noise via the
dominant spectral peak at f₀.

**Test:** Compare spectral ratio at f₀ for a coherent signal and white noise.
The coherent signal must have f₀ detected; the noise signal must not.

**Falsification criterion:** White noise regularly shows spectral_ratio ≥ 0.0888
at 141.7001 Hz.

```python
result = psi_mod.test_prediction_p2_coherence_sensitivity(a_coh, a_inc)
assert result["passed"]
```

### P3 – Spectral Peak at f₀

**Claim:** In coherent QCAL systems, the dominant spectral component is at
f₀ = 141.7001 Hz.

**Test:** Compute the FFT dominant frequency; verify |f_dom − f₀| < 1 Hz.

**Falsification criterion:** Dominant frequency deviates from f₀ by more than
1 Hz in a system claimed to be coherent.

```python
result = psi_mod.test_prediction_p3_spectral_peak(a_t)
assert result["passed"]
```

---

## API Reference

### `compute_psi_from_timeseries`

```python
metrics = compute_psi_from_timeseries(
    a_t,           # Time series array
    T=1.0,         # Duration (s)
    fs=1000.0,     # Sampling rate (Hz)
    mass=1e-12,    # System mass (kg)
)
```

Returns a `PsiMetrics` dataclass with fields:

| Field | Type | Description |
|-------|------|-------------|
| `psi` | float | Full Ψ in Joules |
| `psi_tilde` | float | Dimensionless Ψ̃ ∈ [0, π] |
| `A_eff_squared` | float | A_eff² |
| `is_coherent` | bool | Ψ̃ ≥ 0.888 |
| `f0_detected` | bool | spectral_ratio ≥ 0.0888 at f₀ |
| `dominant_frequency` | float | Frequency of max spectral power (Hz) |
| `spectral_ratio` | float | Power fraction at f₀ |
| `mass_kg` | float | Input mass (kg) |
| `duration_s` | float | Input duration T (s) |
| `sampling_rate_hz` | float | Input sampling rate (Hz) |
| `n_samples` | int | Number of samples |

### `generate_coherent_signal`

```python
t, a_t = generate_coherent_signal(
    duration=1.0, fs=1000.0, f0=141.7001,
    amplitude=1.0, noise_level=0.05
)
```

### `generate_incoherent_signal`

```python
t, a_t = generate_incoherent_signal(duration=1.0, fs=1000.0, amplitude=1.0)
```

---

## Example Usage

```python
from core.psi_formalization import (
    compute_psi_from_timeseries,
    generate_coherent_signal,
)
import core.psi_formalization as psi_mod
import numpy as np

# Generate coherent signal at f₀
t, a_t = generate_coherent_signal(duration=1.0, fs=1000, f0=141.7001)

# Compute metrics
metrics = compute_psi_from_timeseries(a_t, T=1.0, fs=1000, mass=1e-12)

assert metrics.is_coherent        # True for coherent signals
assert metrics.f0_detected        # True when f₀ peak present
print(f"Ψ̃ = {metrics.psi_tilde:.4f}")  # ~1.57 for sine wave

# Test predictions
masses = [1e-15, 1e-12, 1e-9]
p1 = psi_mod.test_prediction_p1_energy_scaling(a_t, masses, T=1.0)
assert p1["passed"]

a_noise = np.random.randn(1000)
p2 = psi_mod.test_prediction_p2_coherence_sensitivity(a_t, a_noise, T=1.0, fs=1000)
assert p2["passed"]

p3 = psi_mod.test_prediction_p3_spectral_peak(a_t, fs=1000)
assert p3["passed"]
```

---

## Files

| File | Description |
|------|-------------|
| `core/psi_formalization.py` | Core implementation |
| `tests/test_psi_formalization.py` | Test suite (49 tests) |
| `PSI_FORMALIZATION_README.md` | This document |
| `demo_psi_formalization.py` | Interactive demonstration |
| `PSI_FORMALIZATION_IMPLEMENTATION_SUMMARY.md` | Implementation overview |
