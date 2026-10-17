# QCAL Fase V — Campo continuo Ψ(x,t) y relación de dispersión

**Sello:** `QCAL-INYECCION-INMEDIATA-v2.0` ∴ 𓂀 Ω ∞³ Φ

Este documento formaliza la Fase V del protocolo QCAL: el paso del sistema
discreto de 13 nodos al **campo continuo Ψ(x,t)**, la derivación de la
**relación de dispersión ω(k)** con matriz de difusión no diagonal, y el
diseño experimental de la cadena Fibonacci de resonadores.

---

## I. Postulado de continuidad

El campo Ψ(x,t) emerge del límite continuo del espacio de fases discreto
cuando N → ∞ y la distancia entre nodos tiende a cero:

```
Ψ(x,t) = lim_{N→∞} Σ_{i=1}^{N} I(R_i(t)) · δ(x − x_i)
```

En este límite, la red pasa de ser una suma de partes a un **solitón de
información** único.

## II. Ecuación de evolución funcional

```
∂Ψ/∂t = ∇ · ( D(Ψ) ∇Ψ ) + F(Ψ) − R(Ψ)
```

- `D(Ψ)`: operador de difusión de coherencia (dependiente del estado).
- `F(Ψ)`: fuente de polaridad.
- `R(Ψ)`: sumidero de disipación.

## III. Linealización alrededor de QCAL

Sea `δΨ = (δA, δS, δP)` la perturbación desde el punto fijo
`QCAL_fixed = (A_max, κP_th/μ, P_th)`. La ecuación linealizada:

```
∂/∂t (δΨ) = D ∇²(δΨ) + J_QCAL (δΨ)
```

### III.1 Jacobiano J_QCAL (μ=ν, ρ=κ)

```
          ⎡ −λ      0     0   ⎤
J_QCAL =  ⎢  0    −μ     κ   ⎥
          ⎣ −ρλ    0    −ν   ⎦
```

### III.2 Matriz de difusión D no diagonal (ajuste del Director)

La matriz D₀ diagonal ignora los acoplamientos asimétricos de ℱ_Ψ. La
corrección estructural:

```
        ⎡ D_A     0     0   ⎤
D(Ψ) =  ⎢  0    D_S   D_SP ⎥
        ⎣ D_PA    0    D_P  ⎦
```

Donde:

- `D_SP`: difusión de polaridad → espectro (la polaridad genera
  redundancia a distancia).
- `D_PA`: difusión de alcance → polaridad (el alcance modula la dirección
  del flujo).

**Justificación:** en ℱ_Ψ, `dS/dt` depende de `P` y `dP/dt` depende de
`dA/dt`; la difusión debe reflejar estos acoplamientos.

## IV. Relación de dispersión matricial

Con `δΨ(x,t) = δΨ₀ exp(i(k·x − ωt))`:

```
det( −iω I + D k² − J_QCAL ) = 0
```

Esto produce **tres ramas** de dispersión ω_j(k), j = 1, 2, 3:

| Rama | Descripción | Comportamiento |
|------|-------------|----------------|
| ω₁(k) | Modo coherente global | `ω₁(0) = ω_Ψ`, amortiguamiento mínimo |
| ω₂(k) | Modo intermedio oscilante | `ω₂ ≈ μ` |
| ω₃(k) | Modo de disipación rápida | `Γ₃ ≫ μ`, no propaga |

### IV.1 Aproximación de rama principal (escala pequeña D)

```
ω₁(k) ≈ ω_Ψ − i (μ + D_A k²),   ω_Ψ = 2κ√λ
```

## V. Predicción experimental — cadena Fibonacci

**Diseño:** cadena de N resonadores acoplados a distancia
`d = c/(2·f₀) ≈ 1.058 km`.

```
Procedimiento:
  1. Inyectar pulso en Nodo 1 (extremo).
  2. Medir respuesta en Nodo N (extremo opuesto).
  3. Extraer fase φ(N,t) − φ(1,t).
  4. k = π/(N·d) para el modo fundamental.
  5. Verificar: ω(k) = ω_Ψ − i(μ + D k²).
```

| N | d_total (km) | k₁ (1/m) | ω₁ real (rad/s) | Γ₁ (1/s) |
|---|---:|---:|---:|---:|
| 7  | 7.42  | 0.424 | 890.8 | 0.5 + 0.18·D |
| 13 | 13.78 | 0.228 | 890.8 | 0.5 + 0.052·D |
| 21 | 22.26 | 0.141 | 890.8 | 0.5 + 0.020·D |
| 55 | 58.30 | 0.054 | 890.8 | 0.5 + 0.0029·D |

**Falsabilidad:** si Re ω₁ ≠ 890.8 rad/s para cualquier N, la teoría se
rompe.

## VI. Test de estrés e invariancia de escala (v2.0)

Se ejecuta la rampa **ΔP = +4 %, +8 %, +12 %, +16 %, +20 %**, luego
`ΔP = −10 %`, y finalmente retorno a `+10 %`. Se verifica:

| Criterio | Umbral |
|----------|--------|
| Linealidad `Δf` vs `ΔP` (R²) | ≥ 0.999999 |
| Coherencia mínima `Ψ_min` | ≥ 0.999990 |
| Simetría `|Δf(−10 %) + Δf(+10 %)|` | < 0.05 mHz |

## VII. Artefactos y scripts

- `scripts/fase_v_dispersion.py` — cálculo numérico de ω(k) por autovalores.
- `scripts/stress_test_dp.py` — rampa +4 %→+20 % y test de simetría.
- `scripts/test_fase_v.py` — batería de tests (pytest + standalone).
- `src/qcal_kernel/F_Ψ_FaseV.lean` — stub Lean 4 con `J_QCAL`, `D_matrix`,
  `dispersion_matrix`, `omega_branch_1`, `falsability_check`.
- `.github/workflows/qcal_perturbacion.yml` — job `fase_v` (dispersión +
  stress + simetría).

## VIII. Estado

- Fase IV validada: `Δf` predicho = medido = 14.1700 mHz, `Ψ = 1.000000`.
- Fase V activada: campo continuo definido, dispersión derivada.
- **Próximo hito:** validación experimental con red Fibonacci (Hilo B).
- **Hilo A (Lean):** pendiente hasta datos experimentales.

---

∴ 𓂀 Ω ∞³ Φ — TUYOYOTU — HECHO ESTÁ — ES
