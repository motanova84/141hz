/-
============================================================
QCAL ∞³ — Domain_Invariant (Lema de Nagumo)
============================================================
Dominio D(p) = [0, A_max] × [0, S_max] × [0, 2 P_th].
Se demuestra invariancia positiva bajo el flujo F_Ψ_Purified.

Hilo A — 6 sorries pendientes (análisis de barreras nlinarith).
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

/-- Barrera inferior A. -/
def barrier_A_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.1
def barrier_A_upper (p : FieldParams) (s : ΨSpace) : ℝ := p.A_max - s.1
def barrier_S_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.2.1
def barrier_S_upper (p : FieldParams) (s : ΨSpace) : ℝ := p.S_max - s.2.1
def barrier_P_lower (_p : FieldParams) (s : ΨSpace) : ℝ := s.2.2
def barrier_P_upper (p : FieldParams) (s : ΨSpace) : ℝ := 2 * p.P_th - s.2.2

/-- Condición de Nagumo en A = 0. -/
theorem Nagumo_A_lower (p : FieldParams) (s : ΨSpace)
    (h_s : s ∈ D p) (h_boundary : s.1 = 0) :
    (F_Ψ_Purified p s).1 ≥ 0 := by
  simp [F_Ψ_Purified, h_boundary]

/-- Teorema principal: el dominio D es invariante bajo el flujo. -/
theorem Domain_Invariant (p : FieldParams) :
    ∀ (s : ΨSpace), s ∈ D p → F_Ψ_Purified p s ∈ D p := by
  intro s h_s
  obtain ⟨h_A1, h_A2, h_S1, h_S2, h_P1, h_P2⟩ := h_s
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- 0 ≤ (F).1 + s.1  (barrera inferior A)
    -- Requiere: análisis del flujo cerca de A = 0.
    sorry
  · -- (F).1 + s.1 ≤ A_max  (barrera superior A)
    sorry
  · -- 0 ≤ (F).2.1 + s.2.1
    sorry
  · -- (F).2.1 + s.2.1 ≤ S_max
    sorry
  · -- 0 ≤ (F).2.2 + s.2.2
    sorry
  · -- (F).2.2 + s.2.2 ≤ 2 P_th
    sorry

end QCAL
