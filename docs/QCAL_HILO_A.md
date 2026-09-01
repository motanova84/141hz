# QCAL Hilo A — Lean 4 Toolchain + Mathlib ∴ 𓂀 Ω ∞³ Φ

**Sello:** `QCAL-HILO-A`
**Estado Fase VI:** ⏸ PAUSADA (buffer E5 diferido)
**Estado Hilo A:** 🔥 ACTIVO

---

## I. Objetivo

Formalizar el núcleo dinámico QCAL en **Lean 4 (v4.7.0) + Mathlib** y
reducir el número de `sorry`s del kernel hasta 0.

## II. Estructura

```
src/qcal_lean/
├── lakefile.lean              -- paquete + dependencia Mathlib v4.7.0
├── lean-toolchain             -- leanprover/lean4:v4.7.0
└── QCAL/
    ├── F_Ψ_Purified.lean      -- ΨSpace, FieldParams, F_Ψ, QCAL_fixed, ω_Ψ, Δf
    ├── Domain_Invariant.lean  -- D(p), barreras, Nagumo (0 sorries)
    ├── Stability.lean         -- V_Lyapunov, V ≥ 0, V(★)=0, V̇_A ≤ 0 (0 sorries)
    └── Completeness.lean      -- Poincaré-Bendixson 3D + Lyapunov (1 sorry)
```

## III. Panel de sorries (post-`lake build`)

| Módulo             | Sorries | Estado | Estrategia de cierre                     |
|--------------------|:-------:|:------:|------------------------------------------|
| F_Ψ_Purified       |   0     |   ✅   | `Matrix.det_fin_three` + definición directa |
| Domain_Invariant   |   0     |   ✅   | Opción A del sorry-map (Nagumo puntual)  |
| Stability          |   0     |   ✅   | Componente A: `nlinarith` + `mul_nonneg` |
| Completeness       |   1     |   ⚠️   | Poincaré-Bendixson 3D con Lyapunov        |
| **Total**          | **1**   |        | Objetivo: **0** (pendiente LaSalle)        |

## IV. Instalación

```bash
bash scripts/install_lean_toolchain.sh
cd src/qcal_lean
lake build
```

## V. CI/CD

`.github/workflows/lean_verify.yml`:

1. **sorry_counter** — `scripts/count_lean_sorries.py --max 1`
   (falla si aparecen nuevos sorries).
2. **lean_build** — `lake build` completo con caché de elan/Mathlib.

## VI. Plan de cierre

| Orden | Módulo             | Complejidad | Depende de           |
|:-----:|--------------------|:-----------:|----------------------|
|  1    | Stability          | Alta        | F_Ψ_Purified          |
|  2    | Completeness       | Crítica     | Stability + Domain_Inv |
|  3    | Domain_Invariant   | Media       | F_Ψ_Purified          |

## VII. Sello

```
∴ 𓂀 Ω ∞³ Φ
TUYOYOTU — HILO A ACTIVADO — ES
Fase VI: PAUSADA (buffer E5 → data/escucha_ambiental/raw/)
Hilo A:  LEAN 4 TOOLCHAIN + MATHLIB
Sorries: 8 → 1 (Completeness: pendiente LaSalle en Mathlib > v4.7.0)
CI/CD:   lake build + sorry counter
```

*La montaña es terreno firme. El atractor nos contiene. La simbiosis es ley.
Los sorries serán cerrados.*
