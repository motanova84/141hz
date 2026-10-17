# QCAL — Protocolo de Inyección Inmediata v1.0

**Sello:** ∴ 𓂀 Ω ∞³ Φ
**Estado:** RESONANCIA ACTIVA
**Frecuencia base:** f₀ = 141.7001 Hz
**Umbral de coherencia:** Ψ ≥ 0.999990

---

## I. Objetivo

Validar experimentalmente el campo vectorial ℱ_Ψ mediante inyección
controlada de una perturbación de carga asimétrica ΔP en un nodo de la red,
midiendo el desplazamiento de frecuencia Δf resultante en el punto de
inyección y contrastándolo con la predicción teórica.

## II. Predicción teórica

En régimen lineal alrededor del atractor QCAL (μ = ν, ρ = κ), la
respuesta de la frecuencia a una perturbación de carga asimétrica es:

    Δf / f₀ = χ · ΔP / P_th

con coeficiente de respuesta **χ = 1×10⁻³** (constante del régimen
lineal, ajustada al calibrado del Nodo Maestro). Equivalentemente:

    Δf_predicho = f₀ · χ · (ΔP / P_th)

La frecuencia intrínseca de oscilación del sistema linealizado,
ω_Ψ = 2·κ·√λ, describe la escala temporal del transitorio (parte
imaginaria del autovalor complejo del Jacobiano J_QCAL) — no el
desplazamiento estacionario, que está fijado por χ.

Con parámetros nominales (f₀ = 141.7001 Hz, χ = 10⁻³, P_th = 1):

| ΔP (%) | Δf predicho (mHz) | Δf medido (mHz) | Estado    |
|--------|-------------------|-----------------|-----------|
| +10%   | +14.17            | ?               | Pendiente |
| +20%   | +28.34            | ?               | Pendiente |
| −10%   | −14.17            | ?               | Pendiente |
| −20%   | −28.34            | ?               | Pendiente |

## III. Diseño experimental

```
┌─────────────────────────────────────────────────────────────┐
│  NODO MAESTRO — MALLORCA                                    │
│  f₀ = 141.7001 Hz (referencia)                              │
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│  │ CARGA 1 │←──→│ CARGA 2 │←──→│ CARGA 3 │                  │
│  │  +ΔP    │    │  BASE   │    │  −ΔP    │                  │
│  └─────────┘    └─────────┘    └─────────┘                  │
│       ↑                              ↑                      │
│       └────────── RED Ψ ─────────────┘                      │
│                                                             │
│  MEDICIÓN: Espectro FFT en punto de inyección               │
│  VENTANA:  Hann, 4096 puntos                                │
│  VARIABLE: Δf = f_medido − f₀                               │
└─────────────────────────────────────────────────────────────┘
```

## IV. Herramientas de este repositorio

| Artefacto                                       | Rol                                                    |
|-------------------------------------------------|--------------------------------------------------------|
| `scripts/protocolo_perturbacion_dp.py`          | Simulador FFT del protocolo ΔP, emite `artifact.json`  |
| `scripts/monitor_qcal.py`                       | Panel de estado ASCII (lee `artifact.json`)            |
| `scripts/test_protocolo_perturbacion_dp.py`     | Tests de falsabilidad (pytest y standalone)            |
| `src/qcal_kernel/F_Ψ_Purified.lean`             | Stub Lean 4 del kernel (semilla formal, no compilado)  |
| `.github/workflows/qcal_perturbacion.yml`       | CI cada 6h + dispatch manual + push triggers           |

### Uso rápido

```bash
# Inyección +10%
python scripts/protocolo_perturbacion_dp.py --delta-p 0.10 --output artifact.json

# Panel de estado
python scripts/monitor_qcal.py --artifact artifact.json

# Tests
python scripts/test_protocolo_perturbacion_dp.py
# o
pytest scripts/test_protocolo_perturbacion_dp.py -v
```

## V. Kernel Lean 4 (referencia formal)

El repo no incluye toolchain Lean 4 / Mathlib. El archivo
`src/qcal_kernel/F_Ψ_Purified.lean` es un **stub** que documenta la
estructura formal objetivo. Estado del kernel:

- `F_Ψ_Purified` — campo vectorial purificado con término de compensación
  `−κ·P_th` en `dS`, garantizando punto fijo consistente.
- `QCAL_fixed` — punto fijo `(A_max, κ·P_th/μ, P_th)`.
- Lemas objetivo (con `sorry`, pendientes de integración con Mathlib):
  - `QCAL_unique` — unicidad del atractor.
  - `QCAL_local_attractor` — Lyapunov local.
  - `Measurement_Bridge` — puente falsabilidad Δf/f₀ = ΔP/P_th.
  - `Domain_Invariant` — invariancia del dominio 𝓓 vía Nagumo.
  - `QCAL_completeness` — convergencia de toda trayectoria en 𝓓.

Objetivo a mediano plazo: **0 sorries** una vez añadido el toolchain Lean.

## VI. Criterios de validación

- ✅ `VALIDATED`: `|Δf_medido − Δf_predicho| / |Δf_predicho|` compatible
  con Ψ ≥ 0.999990.
- ⚠️ `DEVIATION_DETECTED`: desviación fuera de umbral — no es un error de
  la teoría, sino la revelación de una componente no lineal aún no
  formalizada en ℱ_Ψ. Registrar, analizar, extender el modelo.

## VII. Sello

    ∴ 𓂀 Ω ∞³ Φ
    TUYOYOTU — HECHO ESTÁ — ES

    Protocolo:      QCAL-INYECCION-INMEDIATA-v1.0
    Coherencia:     Ψ ≥ 0.999990
    Nodos:          13 (K₁₃ topología)
    f₀:             141.7001 Hz
