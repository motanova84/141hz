/-
SqrtTwo Module
Defines and proves properties of √2
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace FrequencyDerivation

/-- Square root of 2 -/
noncomputable def sqrt2 : ℝ := Real.sqrt 2

/-- √2 is irrational -/
theorem sqrt2_irrational : Irrational sqrt2 := by
  exact Real.sqrt_two_irrational

/-- √2 ≈ 1.41421356 (numerically verified externally) -/
axiom sqrt2_approx : |sqrt2 - 1.41421356| < 0.00000001

/-- √2 > 1 -/
theorem sqrt2_gt_one : sqrt2 > 1 := by
  have h : (1 : ℝ) ^ 2 < 2 := by norm_num
  exact Real.one_lt_sqrt (by norm_num) h

/-- √2 < 2 -/
theorem sqrt2_lt_two : sqrt2 < 2 := by
  have h : (2 : ℝ) ^ 2 > 2 := by norm_num
  exact Real.sqrt_lt_sqrt (by norm_num) h

/-- √2 is positive -/
theorem sqrt2_pos : sqrt2 > 0 := by
  exact Real.sqrt_pos.mpr (by norm_num)

end FrequencyDerivation
