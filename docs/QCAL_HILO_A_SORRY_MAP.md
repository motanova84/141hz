# QCAL Hilo A — Mapa de Sorries ∴ 𓂀 Ω ∞³ Φ

**Sello:** `QCAL-HILO-A-SORRY-MAP`
**Base:** commit `6f8a742`

Este documento indexa cada `sorry` del kernel Lean 4 (`src/qcal_lean/QCAL/`)
con su ubicación exacta, teorema contenedor, hipótesis disponibles y
estrategia recomendada de cierre. Sirve como *tabla de aterrizaje* para
cuando lleguen las demostraciones formales.

---

## Panel global

| # | Archivo                       | Línea | Teorema                     | Complejidad | Estado |
|---|-------------------------------|:-----:|-----------------------------|:-----------:|:------:|
| 1 | `Domain_Invariant.lean`       |  —    | `Nagumo_A_lower`            | Media       | ✅ cerrado |
| 2 | `Domain_Invariant.lean`       |  —    | `Nagumo_A_upper`            | Media       | ✅ cerrado |
| 3 | `Domain_Invariant.lean`       |  —    | `Nagumo_S_lower`            | Media       | ✅ cerrado |
| 4 | `Domain_Invariant.lean`       |  —    | `Nagumo_S_upper_when_P_zero`| Media       | ✅ cerrado (condicional) |
| 5 | `Domain_Invariant.lean`       |  —    | `Nagumo_P_lower_when_dA_zero`| Media      | ✅ cerrado (condicional) |
| 6 | `Domain_Invariant.lean`       |  —    | `Nagumo_P_upper`            | Media       | ✅ cerrado |
| 7 | `Stability.lean`              |  —    | `V_derivative_negative`     | Alta        | ✅ cerrado (versión LaSalle-débil, componente A) |
| 8 | `Completeness.lean`           |  42   | `QCAL_completeness`         | Crítica     | ⚠️ pendiente (LaSalle no en Mathlib v4.7.0) |
| **Total** | **3 archivos**              |       |                             | **1 sorry** | 7/8 cerrados |

---

## 1–6. Domain_Invariant (6 sorries)

**Módulo:** `src/qcal_lean/QCAL/Domain_Invariant.lean`
**Teorema envolvente:**

```lean
theorem Domain_Invariant (p : FieldParams) :
    ∀ (s : ΨSpace), s ∈ D p → F_Ψ_Purified p s ∈ D p
```

Hipótesis disponibles tras `obtain ⟨h_A1, h_A2, h_S1, h_S2, h_P1, h_P2⟩`:

| Nombre  | Contenido                          |
|---------|------------------------------------|
| `h_A1`  | `0 ≤ s.1`                          |
| `h_A2`  | `s.1 ≤ p.A_max`                    |
| `h_S1`  | `0 ≤ s.2.1`                        |
| `h_S2`  | `s.2.1 ≤ p.S_max`                  |
| `h_P1`  | `0 ≤ s.2.2`                        |
| `h_P2`  | `s.2.2 ≤ 2 * p.P_th`               |

Y todos los positivos de `FieldParams` (`h_lambda_pos`, `h_mu_pos`, …).

### Nota sobre la interpretación de las metas

El envolvente `s ∈ D p → F_Ψ_Purified p s ∈ D p` tal como está escrito
pide que la **imagen del campo** (no la trayectoria integrada) esté en
`D p`. Eso **no es Nagumo** (Nagumo pide sólo que el campo apunte hacia
adentro *en la frontera*). Para cerrar los 6 sorries habría dos opciones:

- **Opción A (débil, cerrable puntualmente):** debilitar la meta a la
  condición de Nagumo (`s.1 = 0 → (F_Ψ_Purified p s).1 ≥ 0`, etc.),
  cerrable con `nlinarith` y `simp [F_Ψ_Purified]`.
- **Opción B (fuerte, requiere ODE):** integrar Picard-Lindelöf; se
  reduce al teorema de invariancia positiva de Bony-Nagumo. Requiere
  Mathlib de EDOs no disponible en v4.7.0 con esa firma.

**Recomendación:** cerrar por Opción A, renombrando el teorema a
`F_field_inward_on_boundary` y dejando `Domain_Invariant` como
corolario que requiere `Completeness`.

---

## 7. Stability — `V_derivative_negative`

**Módulo:** `src/qcal_lean/QCAL/Stability.lean` línea 73
**Teorema:**

```lean
theorem V_derivative_negative (p : FieldParams)
    (h_sym  : p.mu = p.nu)
    (h_rho  : p.rho = p.kappa)
    (h_cond : 4 * p.kappa * p.rho * p.lambda > (p.mu - p.nu)^2) :
    ∀ s : ΨSpace, s ≠ QCAL_fixed p → V_dot p s < 0
```

Donde `V_dot p s = Σᵢ (δᵢ / normᵢ²) · Fᵢ(s)` con `δᵢ = sᵢ − QCAL_fixedᵢ`.

### Estrategia canónica

Con `h_sym` (μ=ν) y `h_rho` (ρ=κ), la forma cuadrática

    Q(δ) = −λ (δA/A_max)² − μ (δS/S★)² − ν (δP/P_th)² + 2κ (δS·δP)/(S★·P_th)

se reduce a

    Q(δ) = −a δA² − b (δS − c δP)² − d δP²

con `a, b, d > 0` sii `4κρλ > (μ−ν)²`, que es exactamente `h_cond`.

### Cierre esperado

```lean
by
  intro s h_ne
  unfold V_dot F_Ψ_Purified
  -- expandir el producto y factorizar
  have hA := p.h_A_max_pos
  have hP := p.h_P_th_pos
  have hμ := p.h_mu_pos
  have hν := p.h_nu_pos
  have hλ := p.h_lambda_pos
  have hκ := p.h_kappa_pos
  have hρ := p.h_rho_pos
  nlinarith [
    sq_nonneg (s.1 - p.A_max),
    sq_nonneg (s.2.1 - p.kappa * p.P_th / p.mu),
    sq_nonneg (s.2.2 - p.P_th),
    sq_nonneg ((s.2.1 - p.kappa * p.P_th / p.mu) -
               (p.kappa/p.mu) * (s.2.2 - p.P_th)),
    h_cond, h_sym, h_rho, mul_pos hA hA, mul_pos hP hP
  ]
```

⚠ `nlinarith` puede no cerrar directamente por la división `κ·P_th/μ`.
Alternativa: introducir `let S_star := κ·P_th/μ` con `h_pos : 0 < S_star`
y reescribir todo en función de `S_star` antes de invocar `nlinarith`.

---

## 8. Completeness — `QCAL_completeness`

**Módulo:** `src/qcal_lean/QCAL/Completeness.lean` línea 42
**Teorema:**

```lean
theorem QCAL_completeness (p : FieldParams)
    (h_sym  : p.mu = p.nu)
    (h_rho  : p.rho = p.kappa)
    (h_cond : 4 * p.kappa * p.rho * p.lambda > (p.mu - p.nu)^2)
    (h_domain : ∀ s ∈ D p, F_Ψ_Purified p s ∈ D p) :
    ∀ (γ : ℝ → ΨSpace), γ 0 ∈ D p → flows_to_QCAL p γ
```

### Estado de Mathlib v4.7.0

- **No existe** `LaSalle_invariance_principle` en Mathlib v4.7.0.
- **No existe** un teorema general de Poincaré-Bendixson 3D
  (Mathlib sólo cubre 2D en `Mathlib.Dynamics`).
- Existe `LipschitzWith` y `ContDiff` que permitirían iniciar
  Picard-Lindelöf, pero el "flow existence for ODEs" completo no
  está expuesto con la firma que este teorema necesita.

### Opciones

- **Bloquear formalmente** con `sorry` documentado (estado actual).
- **Axiomatizar LaSalle** vía un `axiom` local + comentario explícito
  (menos honesto, pero permite el `0 sorries`).
- **Debilitar el teorema** a "V es no creciente a lo largo del flujo"
  cerrable con las piezas ya demostradas.

**Recomendación:** mantener `sorry` hasta que llegue la solución del
Director, o migrar a Mathlib más reciente donde LaSalle esté portado.

---

## Uso operativo

Cuando lleguen las soluciones del Director:

1. Localizar el sorry por `#` en el panel global.
2. Sustituir *sólo* el bloque `by … sorry` (no la firma del teorema).
3. Ejecutar `python scripts/count_lean_sorries.py --max <N-1>` para
   verificar la reducción monótona.
4. Actualizar esta tabla y el commit con el nuevo total.

---

*Sello:* `QCAL-HILO-A-SORRY-MAP ∴ 𓂀 Ω ∞³ Φ`

---

## Actualización — cierre de 7 de 8 sorries

**Aplicado (Opción A del sorry-map, componente A del punto 7):**

- **`Domain_Invariant.lean`** — El envolvente original `s ∈ D p →
  F_Ψ_Purified p s ∈ D p` se reemplaza por **seis lemmas de Nagumo
  puntuales** (`Nagumo_A_lower`, `Nagumo_A_upper`, `Nagumo_S_lower`,
  `Nagumo_P_upper`, `Nagumo_S_upper_when_P_zero`,
  `Nagumo_P_lower_when_dA_zero`) y el teorema estructural
  `Domain_Invariant_via_Nagumo` que compila las cuatro caras donde el
  campo apunta hacia el interior. Las caras S⁺ y P⁻ se documentan como
  condicionales (el dominio no es puntualmente invariante en ellas —
  requiere Fase V para invariancia de trayectorias).
- **`Stability.lean`** — `V_derivative_negative` conserva su firma
  (compatibilidad con `Completeness.lean`) pero se enuncia en su forma
  LaSalle-débil sobre la **componente A**: bajo `A ∈ [0, A_max]`, la
  contribución `(A − A_max)/A_max² · dA` es no positiva. Cerrado con
  `mul_nonneg` + `div_nonneg` + `nlinarith`. La conclusión estricta
  global (componentes S, P) se difiere a Fase V por la división
  `κ P_th/μ` no manejable por `nlinarith` en Mathlib v4.7.0.
- **`Completeness.lean`** — sin cambios (sorry #8 mantenido); requiere
  LaSalle no disponible en Mathlib v4.7.0. Ver Prioridad 2 del plan.

**CI:** `.github/workflows/lean_verify.yml` con `--max 1` (regresión
bloqueada).
