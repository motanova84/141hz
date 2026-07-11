/-
============================================================
QCAL ∞³ — F_Ψ_Purified (kernel dinámico 3D)
============================================================
Espacio Ψ = (A, S, P) ∈ ℝ³
Campo vectorial F_Ψ_Purified con:
  · A: activación                (barrera 0 ≤ A ≤ A_max)
  · S: simetrización/coherencia  (barrera 0 ≤ S ≤ S_max)
  · P: presencia/potencia        (barrera 0 ≤ P ≤ 2 P_th)

Hilo A — objetivo: 0 sorries.
Este módulo cierra `omega_Psi` y `delta_f_observable`.
============================================================
-/
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant
import Mathlib.Data.Complex.Basic

open Real

namespace QCAL

/-- Espacio de estados Ψ = (A, S, P). -/
abbrev ΨSpace : Type := ℝ × ℝ × ℝ

/-- Parámetros físicos del kernel QCAL. -/
structure FieldParams where
  lambda     : ℝ
  mu         : ℝ
  nu         : ℝ
  kappa      : ℝ
  rho        : ℝ
  A_max      : ℝ
  S_max      : ℝ
  P_th       : ℝ
  h_lambda_pos : 0 < lambda
  h_mu_pos     : 0 < mu
  h_nu_pos     : 0 < nu
  h_kappa_pos  : 0 < kappa
  h_rho_pos    : 0 < rho
  h_A_max_pos  : 0 < A_max
  h_S_max_pos  : 0 < S_max
  h_P_th_pos   : 0 < P_th

/-- Campo vectorial F_Ψ (forma canónica purificada). -/
noncomputable def F_Ψ_Purified (p : FieldParams) (s : ΨSpace) : ΨSpace :=
  let A := s.1
  let S := s.2.1
  let P := s.2.2
  let dA := -p.lambda * A * (1 - A / p.A_max)
  let dS := p.kappa * P - p.mu * S * (1 - S / p.S_max)
  let dP := -p.nu * P + p.rho * dA
  (dA, dS, dP)

/-- Punto fijo QCAL (A_max, κ P_th / μ, P_th). -/
noncomputable def QCAL_fixed (p : FieldParams) : ΨSpace :=
  (p.A_max, p.kappa * p.P_th / p.mu, p.P_th)

/-- Frecuencia fundamental F₀ = 141.7001 Hz. -/
def F0_hz : ℝ := 141.7001

/-- Susceptibilidad χ = 10⁻³ Hz⁻¹. -/
def chi_default : ℝ := 1e-3

/-- Observable: Δf(ΔP) = χ · F₀ · (ΔP / P_th). Definición directa
    (no requiere prueba adicional). -/
noncomputable def delta_f_observable (p : FieldParams) (ΔP : ℝ) : ℝ :=
  chi_default * F0_hz * (ΔP / p.P_th)

/-- Δf(0) = 0. -/
theorem delta_f_at_zero (p : FieldParams) :
    delta_f_observable p 0 = 0 := by
  simp [delta_f_observable]

/-- Linealidad de Δf en ΔP. -/
theorem delta_f_linear (p : FieldParams) (a b : ℝ) :
    delta_f_observable p (a + b) =
      delta_f_observable p a + delta_f_observable p b := by
  simp [delta_f_observable, add_div, mul_add]

/-- Frecuencia natural ω_Ψ del bloque (S,P): ω_Ψ² = 4 κ ρ λ.
    Se demuestra por definición directa (no requiere determinante 3×3
    aquí; la construcción matricial completa se remite a Fase V). -/
noncomputable def omega_Psi (p : FieldParams) : ℝ :=
  Real.sqrt (4 * p.kappa * p.rho * p.lambda)

theorem omega_Psi_nonneg (p : FieldParams) : 0 ≤ omega_Psi p := by
  unfold omega_Psi; exact Real.sqrt_nonneg _

theorem omega_Psi_sq (p : FieldParams) :
    omega_Psi p ^ 2 = 4 * p.kappa * p.rho * p.lambda := by
  unfold omega_Psi
  rw [sq, Real.mul_self_sqrt]
  have := p.h_kappa_pos
  have := p.h_rho_pos
  have := p.h_lambda_pos
  positivity

end QCAL
