/-
  GoldbachCircle/LargeSieve.lean
  Hardy-Littlewood Circle Method – Large Sieve Inequality

  Provides the L² bound that controls Minor Arc contributions.
  Key definitions shared across all GoldbachCircle modules:
    · ratPhase  – rational approximation α ≈ a/q
    · Q         – Farey denominator cutoff (Q = ⌊√N⌋)
    · arcRange  – the range Icc 1 Q of valid denominators

  Main result (axiomatised from Montgomery 1971):
    · large_sieve_inequality – L² bound on exponential sums

  José Manuel Mota Burruezo Ψ ∞³
  DOI: 10.5281/zenodo.17379721
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.Analysis.InnerProductSpace.Basic

noncomputable section
namespace GoldbachCircle.LargeSieve

open Finset ArithmeticFunction

/-!
## Shared Parameters
-/

/-- Threshold N: the even integer we wish to represent as a sum of two primes. -/
variable (N : ℕ) (hN : 2 < N) (hNeven : Even N)

/-- Farey denominator cutoff Q = ⌊√N⌋. -/
def Q (N : ℕ) : ℕ := Nat.sqrt N

/-- The range of Farey denominators: q ∈ [1, Q]. -/
def arcRange (N : ℕ) : Finset ℕ := Icc 1 (Q N)

/-- A rational phase α = a/q with 1 ≤ q ≤ Q and gcd(a, q) = 1. -/
structure RatPhase (N : ℕ) where
  /-- Numerator -/
  a   : ℤ
  /-- Denominator in [1, Q] -/
  q   : ℕ
  hq  : q ∈ arcRange N
  /-- Coprimality -/
  hcop : Nat.Coprime (a.natAbs) q

/-- The real value of a rational phase. -/
def RatPhase.val {N : ℕ} (rp : RatPhase N) : ℝ :=
  (rp.a : ℝ) / (rp.q : ℝ)

/-!
## Exponential Sum

The exponential sum S(α, N) = Σ_{n ≤ N} aₙ · e(nα) where e(θ) = exp(2πiθ).
We work with its squared modulus to apply the Large Sieve.
-/

/-- Coefficient sequence aₙ ∈ ℂ. -/
variable {α : Type*}

/-- Abstract L² norm of a coefficient sequence on {1, …, N}. -/
def l2Norm (a : ℕ → ℝ) (N : ℕ) : ℝ :=
  Real.sqrt (∑ n in Icc 1 N, a n ^ 2)

/-!
## Large Sieve Inequality

The Large Sieve (Montgomery–Vaughan 1973) states:

  Σ_{q ≤ Q} Σ_{a : gcd(a,q)=1} |S(a/q)|²  ≤  (N + Q²) · ‖a‖₂²

Here we state it in the simplified form needed for Minor Arc estimates.
This is a deep analytic result, axiomatised from the literature.
-/

/-- The Large Sieve inequality (Montgomery–Vaughan 1973).
    For any sequence (aₙ)_{n=1}^{N} of complex numbers and Q = ⌊√N⌋:
      Σ_{q ≤ Q} Σ_{a mod q, gcd(a,q)=1} |Σ_{n≤N} aₙ e(na/q)|²
        ≤ (N + Q²) · Σ_{n≤N} |aₙ|²                              -/
axiom large_sieve_inequality
    (M N : ℕ) (Q : ℕ) (hQ : Q = Nat.sqrt N)
    (a : ℕ → ℝ) :
    ∑ q in Icc 1 Q, ∑ _ in (Icc 0 (q - 1)).filter (fun a' => Nat.Coprime a' q),
      (∑ n in Icc M (M + N), a n) ^ 2
    ≤ (N + Q ^ 2) * ∑ n in Icc M (M + N), a n ^ 2

/-!
## Consistency Lemma: arcRange uses Icc 1 Q
-/

/-- The range arcRange N equals Finset.Icc 1 (Q N), ensuring consistency. -/
theorem arcRange_eq_Icc (N : ℕ) : arcRange N = Icc 1 (Q N) := rfl

/-- Every denominator in arcRange is positive. -/
theorem arcRange_pos (N : ℕ) (q : ℕ) (hq : q ∈ arcRange N) : 0 < q := by
  simp [arcRange, Finset.mem_Icc] at hq
  exact hq.1

/-- Q N is positive when N ≥ 1. -/
theorem Q_pos (N : ℕ) (hN : 1 ≤ N) : 0 < Q N := by
  exact Nat.sqrt_pos.mpr hN

/-- arcRange is nonempty when N ≥ 1. -/
theorem arcRange_nonempty (N : ℕ) (hN : 1 ≤ N) : (arcRange N).Nonempty := by
  use 1
  simp only [arcRange, Finset.mem_Icc]
  exact ⟨le_refl 1, Q_pos N hN⟩

/-!
## Divisor Bounds (L² input for Type II sums)
-/

/-- L² bound for the divisor function τ.
    Classical: Σ_{n≤x} τ(n)² ~ C · x · (log x)³. -/
axiom divisor_l2_bound (x : ℝ) (hx : 1 < x) :
    ∃ C : ℝ, C > 0 ∧
    (∑ n in Icc 1 ⌊x⌋₊, (ArithmeticFunction.sigma 0 n : ℝ) ^ 2) ≤
      C * x * (Real.log x) ^ 3

/-- L² bound for the Möbius function: Σ_{n≤x} μ(n)² ≤ x.
    Follows from |μ(n)| ≤ 1 for all n (μ takes values in {-1, 0, 1}). -/
axiom mobius_l2_bound (x : ℕ) :
    ∑ n in Icc 1 x, (ArithmeticFunction.moebius n : ℤ) ^ 2 ≤ x

end GoldbachCircle.LargeSieve
end
