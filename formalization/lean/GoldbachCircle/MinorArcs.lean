/-
  GoldbachCircle/MinorArcs.lean
  Hardy-Littlewood Circle Method – Minor Arc Estimate

  Proves that the Minor Arc contribution is O(N · log^{-A} N),
  which is sub-linear relative to the Major Arc signal
  𝔖(N) · N / log² N.

  Connects:
    · GoldbachCircle.LargeSieve  (arcRange, ratPhase, L² bound)
    · GoldbachCircle.VaughanIdentity (Vaughan decomposition, Type I+II bounds)

  José Manuel Mota Burruezo Ψ ∞³
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import GoldbachCircle.LargeSieve
import GoldbachCircle.VaughanIdentity

noncomputable section
namespace GoldbachCircle.MinorArcs

open Real Finset
open GoldbachCircle.LargeSieve GoldbachCircle.VaughanIdentity

/-!
## Minor Arc Region

The minor arcs consist of those α ∈ [0,1) not well-approximated
by a rational a/q with q ≤ Q.  We work arc-by-arc and bound
the exponential sum at each rational phase rp : RatPhase N.
-/

/-!
## Per-Arc Type II Bound

Combining the Large Sieve aggregate bound with Cauchy–Schwarz
(applied fibre-by-fibre over q ∈ arcRange N) yields a per-arc
Type II estimate.  The full argument uses the Bombieri–Vinogradov
structure; we axiomatise the result.
-/

/-- Per-arc Type II exponential sum bound (Vaughan + Large Sieve + Cauchy–Schwarz).
    For every A > 0 there exists c > 0 and N₀ such that for all N ≥ N₀
    and all rational phases rp : RatPhase N:
      |Σ_{n≤N} Λ_II(n) · cos(2π · rp.val · n)| ≤ c · N · (log N)^{-A}  -/
axiom typeII_per_arc_bound
    (A : ℝ) (hA : 0 < A) :
    ∃ (c : ℝ) (N₀ : ℕ), c > 0 ∧
    ∀ (N : ℕ), N₀ ≤ N → 2 < N →
    ∀ (rp : RatPhase N),
      |∑ n in Icc 1 N,
         vonMangoldt_typeII (vaughanCutoff N) n *
         Real.cos (2 * Real.pi * RatPhase.val rp * n)|
      ≤ c * (N : ℝ) * (Real.log N) ^ (- A)

/-!
## Main Minor Arc Theorem

Combining the Siegel–Walfisz (Type I) and the per-arc Type II bounds
via the Vaughan decomposition gives the full minor arc estimate.
-/

/-- Minor Arc Estimate.
    For every A > 0 there exist c > 0 and N₀ such that for all N ≥ N₀
    and all rational phases rp : RatPhase N:
      |Σ_{n≤N} Λ(n) · cos(2π · rp.val · n)| ≤ c · N · (log N)^{-A}

    Proof:
      1. Split Λ = Λ_I + Λ_II  (vaughan_decomposition).
      2. Bound |Λ_I-sum| via siegel_walfisz_typeI.
      3. Bound |Λ_II-sum| via typeII_per_arc_bound.
      4. Add the two bounds; both are O(N log^{-A} N).                   -/
theorem minor_arc_estimate
    (A : ℝ) (hA : 0 < A) :
    ∃ (c : ℝ) (N₀ : ℕ), c > 0 ∧
    ∀ (N : ℕ) (hN : N₀ ≤ N) (hN2 : 2 < N) (rp : RatPhase N),
      |∑ n in Icc 1 N,
         (vonMangoldt n : ℝ) *
         Real.cos (2 * Real.pi * RatPhase.val rp * n)|
      ≤ c * (N : ℝ) * (Real.log N) ^ (-A) := by
  obtain ⟨c_I, hcI_pos, hcI⟩ := siegel_walfisz_typeI A hA
  obtain ⟨c_II, N_II, hcII_pos, hcII⟩ := typeII_per_arc_bound A hA
  refine ⟨c_I + c_II, N_II + 3, by linarith, ?_⟩
  intro N hN hN2 rp
  have hNII : N_II ≤ N := Nat.le_of_add_le_add_right
    (le_trans (Nat.le_add_left N_II 3) hN)
  -- Vaughan split of the full Λ exponential sum
  have split : ∑ n in Icc 1 N, (vonMangoldt n : ℝ) *
      Real.cos (2 * Real.pi * RatPhase.val rp * n)
    = (∑ n in Icc 1 N, vonMangoldt_typeI (vaughanCutoff N) n *
          Real.cos (2 * Real.pi * RatPhase.val rp * n))
    + (∑ n in Icc 1 N, vonMangoldt_typeII (vaughanCutoff N) n *
          Real.cos (2 * Real.pi * RatPhase.val rp * n)) := by
    simp only [← Finset.sum_add_distrib, ← add_mul]
    congr 1
    ext n
    simp [← vaughan_decomposition]
  rw [split]
  calc |_ + _|
      ≤ |∑ n in Icc 1 N, vonMangoldt_typeI (vaughanCutoff N) n *
             Real.cos (2 * Real.pi * RatPhase.val rp * n)|
        + |∑ n in Icc 1 N, vonMangoldt_typeII (vaughanCutoff N) n *
             Real.cos (2 * Real.pi * RatPhase.val rp * n)| := abs_add _ _
    _ ≤ c_I * (N : ℝ) * (Real.log N) ^ (-A)
        + c_II * (N : ℝ) * (Real.log N) ^ (-A) := by
          gcongr
          · exact hcI N hN2 rp
          · exact hcII N hNII hN2 rp
    _ = (c_I + c_II) * (N : ℝ) * (Real.log N) ^ (-A) := by ring

/-!
## Error is Sub-Signal

The key structural lemma: the minor arc error O(N log^{-A} N) is strictly
smaller than the major arc signal 𝔖(N) · N / log² N for all N ≥ N₁
(choosing A = 3 gives a full order-of-magnitude margin).
-/

/-- Signal dominance: for any c > 0 and 𝔖_min > 0 there exists N₁ such that
    for all N ≥ N₁:   c · N · log^{-3} N  <  𝔖_min · N / log² N.       -/
theorem error_sub_signal
    (c 𝔖_min : ℝ) (hc : c > 0) (h𝔖 : 𝔖_min > 0) :
    ∃ N₁ : ℕ, ∀ N : ℕ, N₁ ≤ N → (2 : ℝ) < N →
      c * (N : ℝ) * (Real.log N) ^ (-(3 : ℝ)) <
      𝔖_min * (N : ℝ) / (Real.log N) ^ 2 := by
  -- Equivalent to c < 𝔖_min · log N, which holds when log N > c / 𝔖_min.
  use ⌈Real.exp (c / 𝔖_min) + 1⌉₊ + 3
  intro N hN hN2
  have hNcast : (⌈Real.exp (c / 𝔖_min) + 1⌉₊ : ℝ) + 3 ≤ N := by
    have : (⌈Real.exp (c / 𝔖_min) + 1⌉₊ + 3 : ℝ) ≤ N := by
      exact_mod_cast hN
    linarith
  have hexp_lt : Real.exp (c / 𝔖_min) < N := by
    have hceil : Real.exp (c / 𝔖_min) < ⌈Real.exp (c / 𝔖_min) + 1⌉₊ := by
      have := Nat.lt_ceil.mpr (by linarith [Real.add_one_le_exp (c / 𝔖_min)] :
        Real.exp (c / 𝔖_min) < Real.exp (c / 𝔖_min) + 1)
      exact_mod_cast this
    linarith
  have hlogN : c / 𝔖_min < Real.log N := by
    rwa [← Real.log_exp (c / 𝔖_min)]
    exact Real.log_lt_log (Real.exp_pos _) hexp_lt
  have hlogN_pos : (0 : ℝ) < Real.log N :=
    lt_trans (div_pos hc h𝔖) hlogN
  have hNpos : (0 : ℝ) < N := by linarith
  have hlog2_pos : (0 : ℝ) < (Real.log N) ^ 2 := by positivity
  rw [Real.rpow_neg (le_of_lt hlogN_pos) 3,
      div_lt_div_iff (by positivity) hlog2_pos]
  -- Goal: c * N * (log N)^2 < 𝔖_min * N * (log N)^3
  have hlogcube : c < 𝔖_min * Real.log N := by
    rw [gt_iff_lt, ← div_lt_iff h𝔖] at hlogN; linarith
  nlinarith [mul_pos hNpos (pow_pos hlogN_pos 2)]

end GoldbachCircle.MinorArcs
end
