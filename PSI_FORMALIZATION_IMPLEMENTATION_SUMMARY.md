# Ψ Formalization – Implementation Summary

## What Was Implemented

### `core/psi_formalization.py`

Core module (~350 LOC) providing a publication-ready formalization of the
QCAL Ψ coherence field operator.

**Key components:**

- **`PsiMetrics` dataclass** – container for all Ψ-related metrics
- **`compute_A_eff_squared()`** – operational definition: A_eff² = mean(|a|²)
- **`compute_psi_from_timeseries()`** – main API returning a `PsiMetrics` instance
- **`generate_coherent_signal()`** – sinusoidal signal at f₀ with optional noise
- **`generate_incoherent_signal()`** – white-noise reference signal
- **`test_prediction_p1_energy_scaling()`** – P1: Ψ ∝ m
- **`test_prediction_p2_coherence_sensitivity()`** – P2: coherent vs. incoherent
- **`test_prediction_p3_spectral_peak()`** – P3: dominant peak at f₀

**Mathematical forms:**

```
A_eff² = (1/T) ∫₀ᵀ |a(t)|² dt   [operational definition]
Ψ      = mc² · A_eff² · π         [energy, Joules]
Ψ̃     = π  · A_eff²              [dimensionless, ∈ [0, π]]
```

**QCAL compatibility:**
- f₀ = 141.7001 Hz (`QCAL_BASE_FREQUENCY`)
- Ψ̃ threshold = 0.888 (`PSI_TILDE_THRESHOLD`)
- Spectral ratio threshold = 0.0888 (`SPECTRAL_RATIO_THRESHOLD`)

### `tests/test_psi_formalization.py`

49 tests across 8 test classes, all passing:

| Class | Tests | Coverage |
|-------|-------|----------|
| `TestConstants` | 4 | Module constants |
| `TestPsiMetrics` | 2 | Dataclass fields |
| `TestComputeAEffSquared` | 8 | A_eff² edge cases |
| `TestComputePsiFromTimeseries` | 12 | Core API |
| `TestGenerateCoherentSignal` | 4 | Signal generation |
| `TestGenerateIncoherentSignal` | 3 | Noise generation |
| `TestPredictionP1` | 6 | P1 validation |
| `TestPredictionP2` | 5 | P2 validation |
| `TestPredictionP3` | 5 | P3 validation |

### `demo_psi_formalization.py`

Complete demonstration script showing all metrics and predictions with
printed output.

## Falsifiable Predictions

| ID | Claim | Falsification criterion |
|----|-------|------------------------|
| P1 | Ψ ∝ m at fixed coherence | Relative deviation in Ψ/m > 10⁻⁶ |
| P2 | Coherent fields distinguishable from noise via f₀ peak | Noise regularly shows spectral_ratio ≥ 0.0888 at f₀ |
| P3 | Dominant component at f₀ = 141.7001 Hz in coherent systems | Dominant frequency deviates from f₀ by > 1 Hz |

## Integration

Fully compatible with the existing QCAL ∞³ system. No changes to existing
modules were required. The module depends only on `numpy` (already a
repository dependency).
