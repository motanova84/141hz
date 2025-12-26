/-
Copyright (c) 2025 José Manuel Mota Burruezo.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace QC_LLM.Core

/-- Golden ratio φ = (1 + √5) / 2 -/
noncomputable def φ : ℝ := (1 + Real.sqrt 5) / 2

/-- φ cubed -/
noncomputable def φ_cubed : ℝ := φ ^ 3

/-- Golden ratio equation: φ² = φ + 1 -/
theorem phi_golden_equation : φ ^ 2 = φ + 1 := by
  unfold φ
  field_simp
  ring_nf
  rw [pow_two (Real.sqrt 5)]
  rw [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 5)]
  ring

/-- φ is positive -/
theorem phi_pos : 0 < φ := by
  unfold φ
  apply div_pos
  · apply add_pos_of_pos_of_nonneg
    · norm_num
    · exact Real.sqrt_nonneg 5
  · norm_num

/-- Numerical bounds on φ -/
theorem phi_bounds : 1.618 < φ ∧ φ < 1.619 := by
  unfold φ
  constructor
  · have : (2.236:ℝ) < Real.sqrt 5 := by
      rw [Real.sqrt_lt']
      constructor <;> norm_num
      norm_num
    linarith
  · have : Real.sqrt 5 < (2.237:ℝ) := by
      rw [Real.sqrt_lt']
      constructor <;> norm_num
      norm_num
    linarith

/-- φ³ bounds -/
theorem phi_cubed_bounds : 4.236 < φ_cubed ∧ φ_cubed < 4.237 := by
  unfold φ_cubed
  have h := phi_bounds
  constructor
  · calc φ^3 > (1.618:ℝ)^3 := by
      apply pow_lt_pow_left h.1
      · linarith [phi_pos]
      · norm_num
    _ > 4.236 := by norm_num
  · calc φ^3 < (1.619:ℝ)^3 := by
      apply pow_lt_pow_left h.2 phi_pos
      norm_num
    _ < 4.237 := by norm_num

end QC_LLM.Core
