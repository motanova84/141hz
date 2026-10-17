/-
============================================================
QCAL ∞³ — Domain_Invariant (Lema de Nagumo)
============================================================
Dominio D(p) = [0, A_max] × [0, S_max] × [0, 2 P_th].

Se demuestran las **condiciones de Nagumo** en las caras de la frontera
donde el campo F_Ψ_Purified apunta hacia el interior. Éstas son las
piezas *puntuales* que un teorema de invariancia positiva (Bony-Nagumo)
combinaría con existencia/unicidad de trayectorias para obtener la
invariancia del dominio bajo el flujo.

Estado Hilo A (sorries en este módulo): 0.
El teorema global `Domain_Invariant_via_Nagumo` se enuncia como
conjunción de las condiciones puntuales, dejando el paso ODE → flujo
para `Completeness.lean`.
============================================================
-/
import Mathlib
import QCAL.F_Ψ_Purified

open Set Real

namespace QCAL

/-- Dominio invariante propuesto. -/
def D (p : FieldParams) : Set ΨSpace :=
  { s | 0 ≤ s.1 ∧ s.1 ≤ p.A_max ∧
        0 ≤ s.2.1 ∧ s.2.1 ≤ p.S_max ∧
        0 ≤ s.2.2 ∧ s.2.2 ≤ 2 * p.P_th }

/-- Barreras (funciones cuya no-negatividad define D). -/
def barrier_A_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.1
def barrier_A_upper (p : FieldParams) (s : ΨSpace) : ℝ := p.A_max - s.1
def barrier_S_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.2.1
def barrier_S_upper (p : FieldParams) (s : ΨSpace) : ℝ := p.S_max - s.2.1
def barrier_P_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.2.2
def barrier_P_upper (p : FieldParams) (s : ΨSpace) : ℝ := 2 * p.P_th - s.2.2

/-! ### Condiciones de Nagumo puntuales en cada cara

Cada teorema `Nagumo_*` establece: en la cara correspondiente de la
frontera de `D p`, el campo `F_Ψ_Purified` apunta hacia el interior
(o es tangente). Estas son las hipótesis puntuales del teorema de
Bony-Nagumo.
-/

/-- Cara A = 0: dA = −λ · 0 · (1 − 0/A_max) = 0 ≥ 0. -/
theorem Nagumo_A_lower (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.1 = 0) :
    (F_Ψ_Purified p s).1 ≥ 0 := by
  simp [F_Ψ_Purified, h_boundary]

/-- Cara A = A_max: dA = −λ · A_max · (1 − 1) = 0 ≤ 0. -/
theorem Nagumo_A_upper (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.1 = p.A_max) :
    (F_Ψ_Purified p s).1 ≤ 0 := by
  have hA : (0 : ℝ) < p.A_max := p.h_A_max_pos
  simp [F_Ψ_Purified, h_boundary, ne_of_gt hA]

/-- Cara S = 0 con P ≥ 0: dS = κP − 0 = κP ≥ 0. -/
theorem Nagumo_S_lower (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.2.1 = 0) (h_P_nn : 0 ≤ s.2.2) :
    (F_Ψ_Purified p s).2.1 ≥ 0 := by
  have hκ : (0 : ℝ) < p.kappa := p.h_kappa_pos
  have : 0 ≤ p.kappa * s.2.2 := mul_nonneg hκ.le h_P_nn
  simp [F_Ψ_Purified, h_boundary]
  linarith

/-- Cara P = 2·P_th con A ∈ [0, A_max]: dP = −ν·2P_th + ρ·dA.

Como `dA = −λ A (1 − A/A_max) ≤ 0` para `A ∈ [0, A_max]` (logística
frenada), y `ν, P_th, ρ > 0`, se cumple `dP ≤ 0`. -/
theorem Nagumo_P_upper (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.2.2 = 2 * p.P_th)
    (h_A_nn : 0 ≤ s.1) (h_A_le : s.1 ≤ p.A_max) :
    (F_Ψ_Purified p s).2.2 ≤ 0 := by
  have hν := p.h_nu_pos
  have hP := p.h_P_th_pos
  have hρ := p.h_rho_pos
  have hλ := p.h_lambda_pos
  have hA := p.h_A_max_pos
  -- dA = −λ s.1 (1 − s.1/A_max) ≤ 0
  have h_dA_nonpos : -p.lambda * s.1 * (1 - s.1 / p.A_max) ≤ 0 := by
    have h_factor : 0 ≤ 1 - s.1 / p.A_max := by
      have : s.1 / p.A_max ≤ 1 := by
        rw [div_le_one hA]; exact h_A_le
      linarith
    have h_prod_nn : 0 ≤ p.lambda * s.1 * (1 - s.1 / p.A_max) :=
      mul_nonneg (mul_nonneg hλ.le h_A_nn) h_factor
    linarith
  simp [F_Ψ_Purified, h_boundary]
  nlinarith [h_dA_nonpos, hν, hP, hρ, mul_pos hν hP]

/-! ### Sub-caras de S⁺ y P⁻ (invariancia condicional)

En `S = S_max` con `P > 0`, el campo tiene `dS = κP > 0`, por lo que
el dominio *no* es invariante puntualmente en esa cara. La invariancia
completa requiere restringir a la sub-región donde el flujo global
compensa (Fase V — dispersión matricial). En este módulo enunciamos
sólo el caso trivial `P = 0`, en el que `dS = 0` (tangente).
-/

/-- Cara S = S_max con P = 0: dS = 0 (campo tangente). -/
theorem Nagumo_S_upper_when_P_zero (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.2.1 = p.S_max) (h_P_zero : s.2.2 = 0) :
    (F_Ψ_Purified p s).2.1 = 0 := by
  have hS : (0 : ℝ) < p.S_max := p.h_S_max_pos
  simp [F_Ψ_Purified, h_boundary, h_P_zero, ne_of_gt hS]

/-- Cara P = 0 con dA = 0 (o sea A = 0 o A = A_max): dP = 0 (tangente).
Es la única sub-cara donde el flujo respeta la barrera P⁻ puntualmente:
para A ∈ (0, A_max), dA < 0 y dP = ρ·dA < 0 sale del dominio, lo que
confirma que el dominio no es invariante en el sentido fuerte. -/
theorem Nagumo_P_lower_when_dA_zero (p : FieldParams) (s : ΨSpace)
    (h_boundary : s.2.2 = 0)
    (h_dA_zero : -p.lambda * s.1 * (1 - s.1 / p.A_max) = 0) :
    (F_Ψ_Purified p s).2.2 = 0 := by
  simp [F_Ψ_Purified, h_boundary, h_dA_zero]

/-! ### Teorema estructural

`Domain_Invariant_via_Nagumo` compila las 4 condiciones de Nagumo que
sí se cumplen puntualmente. La invariancia completa `s ∈ D p →
F_Ψ_Purified p s ∈ D p` **no es cierta** en la formulación puntual
(véanse las notas anteriores); su versión correcta —invariancia de
trayectorias— requiere `Completeness.lean`.
-/

/-- Teorema estructural de Nagumo: las cuatro caras donde el campo
apunta hacia el interior del dominio. -/
theorem Domain_Invariant_via_Nagumo (p : FieldParams) :
    (∀ s : ΨSpace, s.1 = 0 → (F_Ψ_Purified p s).1 ≥ 0) ∧
    (∀ s : ΨSpace, s.1 = p.A_max → (F_Ψ_Purified p s).1 ≤ 0) ∧
    (∀ s : ΨSpace, s.2.1 = 0 → 0 ≤ s.2.2 →
      (F_Ψ_Purified p s).2.1 ≥ 0) ∧
    (∀ s : ΨSpace, s.2.2 = 2 * p.P_th → 0 ≤ s.1 → s.1 ≤ p.A_max →
      (F_Ψ_Purified p s).2.2 ≤ 0) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro s h; exact Nagumo_A_lower p s h
  · intro s h; exact Nagumo_A_upper p s h
  · intro s h hP; exact Nagumo_S_lower p s h hP
  · intro s h hA1 hA2; exact Nagumo_P_upper p s h hA1 hA2

end QCAL
