/-
============================================================
QCAL ∞³ — StabilityMatrix (Matriz de Estabilidad M)
============================================================
Matriz de estabilidad M (JMMB, 12/Jul/2026):

  M = [[κ,   0,   (μ-ν)/2],
       [0,   ρ,   0],
       [(μ-ν)/2, 0,   λ]]

Forma cuadrática: Q(x) = κ·x₁² + ρ·x₂² + λ·x₃² + (μ−ν)·x₁·x₃

Criterio de Sylvester:
  D₁ = κ        > 0
  D₂ = κρ       > 0
  D₃ = ρ(4κλ − (μ−ν)²)/4  > 0  ⇔  4κλ > (μ−ν)²

Módulo independiente — matemática pura de matrices.
No importa F_Ψ_Purified ni FieldParams.

f₀ = 141.7001 Hz · TUYOYOTU · HECHO ESTÁ
============================================================
-/
import Mathlib

open Real Matrix

namespace QCAL.StabilityMatrix

/-! ───────────────────────────────────────────────────────────
  1. MATRIZ DE ESTABILIDAD M
  ─────────────────────────────────────────────────────────── -/

/-- Matriz de estabilidad M (3×3, parámetros escalares). -/
def M (κ ρ λ μ ν : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![κ, 0, (μ - ν) / 2;
    0, ρ, 0;
    (μ - ν) / 2, 0, λ]

/-- M es simétrica. -/
theorem M_symmetric (κ ρ λ μ ν : ℝ) : M κ ρ λ μ ν = (M κ ρ λ μ ν)ᵀ := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [M]

/-! ───────────────────────────────────────────────────────────
  2. FORMA CUADRÁTICA Q(x) = xᵀMx
  ─────────────────────────────────────────────────────────── -/

/-- Forma cuadrática Q(x) = κ·x₁² + ρ·x₂² + λ·x₃² + (μ−ν)·x₁·x₃. -/
def Q (κ ρ λ μ ν : ℝ) (x : Fin 3 → ℝ) : ℝ :=
  κ * x 0 ^ 2 + ρ * x 1 ^ 2 + λ * x 2 ^ 2 + (μ - ν) * x 0 * x 2

/── Q = xᵀMx. -/
theorem Q_eq_matrix (κ ρ λ μ ν : ℝ) (x : Fin 3 → ℝ) :
    Q κ ρ λ μ ν x = ∑ i, ∑ j, (M κ ρ λ μ ν) i j * x i * x j := by
  simp [Q, M, Fin.sum_univ_three]; ring

/-! ───────────────────────────────────────────────────────────
  3. MENORES PRINCIPALES — CRITERIO DE SYLVESTER
  ─────────────────────────────────────────────────────────── -/

/-- Primer menor: D₁ = κ. -/
def D1 (κ ρ λ μ ν : ℝ) : ℝ := κ

/-- Segundo menor: D₂ = κ·ρ. -/
def D2 (κ ρ λ μ ν : ℝ) : ℝ := κ * ρ

/-- Tercer menor: D₃ = det(M) = ρ·(κ·λ − ((μ−ν)/2)²). -/
def D3 (κ ρ λ μ ν : ℝ) : ℝ := ρ * (κ * λ - ((μ - ν) / 2)^2)

/── Determinante de M = D₃. -/
theorem det_eq_D3 (κ ρ λ μ ν : ℝ) :
    Matrix.det (M κ ρ λ μ ν) = D3 κ ρ λ μ ν := by
  unfold M D3
  simp [Matrix.det_fin_three]; ring

/── Sylvester: κ>0, ρ>0, λ>0, 4κλ > (μ−ν)² ⇒ D₁>0, D₂>0, D₃>0. -/
theorem Sylvester (κ ρ λ μ ν : ℝ)
    (hκ : κ > 0) (hρ : ρ > 0) (hλ : λ > 0)
    (h_strong : 4 * κ * λ > (μ - ν)^2) :
    D1 κ ρ λ μ ν > 0 ∧ D2 κ ρ λ μ ν > 0 ∧ D3 κ ρ λ μ ν > 0 := by
  refine ⟨hκ, mul_pos hκ hρ, ?_⟩
  unfold D3
  have h_inner : κ * λ - ((μ - ν) / 2)^2 > 0 := by nlinarith
  positivity

/── Sylvester with h_cond + ρ ≥ 1 (sufficient): 4κρλ > (μ−ν)² ∧ ρ ≥ 1 ⇒ D₃>0. -/
theorem Sylvester_from_h_cond (κ ρ λ μ ν : ℝ)
    (hκ : κ > 0) (hρ : ρ > 0) (hλ : λ > 0)
    (h_cond : 4 * κ * ρ * λ > (μ - ν)^2) (h_ρ_ge_one : 1 ≤ ρ) :
    D1 κ ρ λ μ ν > 0 ∧ D2 κ ρ λ μ ν > 0 ∧ D3 κ ρ λ μ ν > 0 := by
  apply Sylvester κ ρ λ μ ν hκ hρ hλ
  nlinarith

/-! ───────────────────────────────────────────────────────────
  4. POSITIVIDAD DE Q — COMPLETAR CUADRADOS
  ───────────────────────────────────────────────────────────

  Q = κ·(x₁ + α·x₃)² + ρ·x₂² + (λ − κ·α²)·x₃²
  donde α = (μ−ν)/(2κ)

  Bajo 4κλ > (μ−ν)²: λ − κ·α² = (4κλ − (μ−ν)²)/(4κ) > 0
  ∴ Q > 0 para todo x ≠ 0. (Independiente de ρ.)
  ─────────────────────────────────────────────────────────── -/

/── Q(x) > 0 para x ≠ 0 bajo 4κλ > (μ−ν)² (condición de Sylvester). -/
theorem Q_positive_definite (κ ρ λ μ ν : ℝ)
    (hκ : κ > 0) (hρ : ρ > 0) (hλ : λ > 0)
    (h_strong : 4 * κ * λ > (μ - ν)^2) :
    ∀ x : Fin 3 → ℝ, x ≠ 0 → 0 < Q κ ρ λ μ ν x := by
  intro x hx_ne; unfold Q
  set α := (μ - ν) / (2 * κ) with hα_def
  have h_sq : κ * x 0 ^ 2 + ρ * x 1 ^ 2 + λ * x 2 ^ 2 + (μ - ν) * x 0 * x 2 =
    κ * (x 0 + α * x 2) ^ 2 + ρ * x 1 ^ 2 + (λ - κ * α ^ 2) * x 2 ^ 2 := by
    nlinarith
  rw [h_sq]
  have h_coeff : 0 < λ - κ * α ^ 2 := by
    dsimp [α]; nlinarith
  have h_nonneg : 0 ≤ κ * (x 0 + α * x 2) ^ 2 + ρ * x 1 ^ 2 +
    (λ - κ * α ^ 2) * x 2 ^ 2 := by positivity
  by_contra h_not
  push_neg at h_not
  have hx0t : x 0 + α * x 2 = 0 := by
    have : κ * (x 0 + α * x 2) ^ 2 = 0 := by nlinarith; nlinarith
  have hx1 : x 1 = 0 := by
    have : ρ * x 1 ^ 2 = 0 := by nlinarith; nlinarith
  have hx2 : x 2 = 0 := by
    have : (λ - κ * α ^ 2) * x 2 ^ 2 = 0 := by nlinarith
    nlinarith
  have hx0 : x 0 = 0 := by subst hx2; simp at hx0t; exact hx0t
  subst hx0 hx1 hx2
  apply hx_ne; ext i; fin_cases i <;> rfl

/── Q(x) > 0 bajo h_cond + ρ ≥ 1 (corolario). -/
theorem Q_positive_definite_from_h_cond (κ ρ λ μ ν : ℝ)
    (hκ : κ > 0) (hρ : ρ > 0) (hλ : λ > 0)
    (h_cond : 4 * κ * ρ * λ > (μ - ν)^2) (h_ρ_ge_one : 1 ≤ ρ) :
    ∀ x : Fin 3 → ℝ, x ≠ 0 → 0 < Q κ ρ λ μ ν x := by
  apply Q_positive_definite κ ρ λ μ ν hκ hρ hλ
  nlinarith

end QCAL.StabilityMatrix
