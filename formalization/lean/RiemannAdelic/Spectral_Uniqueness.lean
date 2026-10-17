/-
  Spectral_Uniqueness.lean — Rigidez Analítica del Cociente D/Ξ (Frente I)

  Formaliza el argumento de que si D y Ξ son funciones enteras que comparten
  derivada logarítmica en el dominio regular Ω = regularDomain Ξ, entonces
  D/Ξ ≡ 1 en Ω, y por densidad, D ≡ Ξ en todo ℂ.

  ## Estrategia

  1. `quotient_constant_on_connected_domain`: si q = D/Ξ es diferenciable en
     el dominio abierto y preconexo Ω, con deriv q ≡ 0 en Ω, entonces q es
     constante en Ω (vía `IsOpen.is_const_of_deriv_eq_zero` de Mathlib).
     Normalizando q(0) = 1 (con D 0 = Ξ 0), se obtiene q ≡ 1 en Ω.
  2. `eq_on_univ_of_eq_on_dense`: si D y Ξ son continuas en ℂ, coinciden en
     Ω, y Ω es denso en ℂ (closure Ω = univ), entonces D = Ξ en todo ℂ
     (vía `Set.EqOn.closure`).

  La hipótesis `h_deriv_zero` (coincidencia de derivadas logarítmicas de D y
  Ξ en Ω) es la entrada analítica que debe suministrar el desarrollo previo
  (regla del cociente + no anulación aislada de D); no se deriva aquí.

  **Nota de verificación**: este archivo no ha sido compilado en este entorno
  (no hay toolchain Lean/Mathlib disponible en el sandbox). Los lemas están
  escritos para ser cerrados sin `sorry` usando únicamente resultados
  estándar de Mathlib (`IsOpen.is_const_of_deriv_eq_zero`, `Set.EqOn.closure`);
  se recomienda validarlos con `lake build` en un entorno con red antes de
  incorporarlos a un `#print axioms` de cierre formal.

  Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
  Licencia: MIT
-/

import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Complex.Basic
import Mathlib.Topology.Basic
import Mathlib.Topology.Separation

open Complex Set

namespace RiemannAdelic

/-- Conjunto de ceros de una función `ℂ → ℂ`. -/
def zeroSet (f : ℂ → ℂ) : Set ℂ := {s : ℂ | f s = 0}

/-- Dominio regular asociado a `Ξ`: el complemento de sus ceros. -/
def regularDomain (Xi : ℂ → ℂ) : Set ℂ := {s : ℂ | Xi s ≠ 0}

/-- Si `q = D/Ξ` es diferenciable con derivada nula en todo el dominio
regular conexo `Ω`, entonces `q` es constante en `Ω`; normalizando en
`s = 0` (donde `D 0 = Ξ 0 ≠ 0`), se sigue `D s / Ξ s = 1` para todo `s ∈ Ω`. -/
lemma quotient_constant_on_connected_domain
    {D Xi : ℂ → ℂ}
    (h_preconn : IsPreconnected (regularDomain Xi))
    (h_open : IsOpen (regularDomain Xi))
    (h_deriv_zero : (regularDomain Xi).EqOn (deriv (fun z => D z / Xi z)) 0)
    (h_diff : DifferentiableOn ℂ (fun z => D z / Xi z) (regularDomain Xi))
    (h_scale : D 0 = Xi 0)
    (h_xi0 : Xi 0 ≠ 0) :
    ∀ s ∈ regularDomain Xi, D s / Xi s = 1 := by
  intro s hs
  have h0_in : (0 : ℂ) ∈ regularDomain Xi := by
    simpa [regularDomain, zeroSet] using h_xi0
  have hconst : D s / Xi s = D 0 / Xi 0 :=
    h_open.is_const_of_deriv_eq_zero h_preconn h_diff h_deriv_zero hs h0_in
  calc
    D s / Xi s = D 0 / Xi 0 := hconst
    _ = 1 := by rw [h_scale, div_self h_xi0]

/-- Si `D` y `Ξ` son continuas en `ℂ`, coinciden en el dominio regular `Ω`
denso en `ℂ`, entonces coinciden en todo `ℂ` (extensión por densidad). -/
lemma eq_on_univ_of_eq_on_dense
    {D Xi : ℂ → ℂ}
    (hD_cont : Continuous D)
    (hXi_cont : Continuous Xi)
    (h_dense : closure (regularDomain Xi) = univ)
    (h_eq_on_domain : ∀ s ∈ regularDomain Xi, D s = Xi s) :
    ∀ s : ℂ, D s = Xi s := by
  have hEq : Set.EqOn D Xi (regularDomain Xi) := fun z hz => h_eq_on_domain z hz
  have hEqClosure : Set.EqOn D Xi (closure (regularDomain Xi)) :=
    hEq.closure hD_cont hXi_cont
  intro s
  have hs : s ∈ closure (regularDomain Xi) := by
    simpa [h_dense] using (show s ∈ (univ : Set ℂ) from trivial)
  exact hEqClosure hs

/-- Composición de los dos lemas anteriores: bajo las hipótesis de rigidez
analítica (derivada logarítmica nula en `Ω` y normalización en `s = 0`) más
la densidad topológica de `Ω`, se obtiene `D ≡ Ξ` en todo `ℂ`. -/
theorem D_eq_Xi_of_quotient_rigid
    {D Xi : ℂ → ℂ}
    (hD_cont : Continuous D)
    (hXi_cont : Continuous Xi)
    (h_preconn : IsPreconnected (regularDomain Xi))
    (h_open : IsOpen (regularDomain Xi))
    (h_dense : closure (regularDomain Xi) = univ)
    (h_deriv_zero : (regularDomain Xi).EqOn (deriv (fun z => D z / Xi z)) 0)
    (h_diff : DifferentiableOn ℂ (fun z => D z / Xi z) (regularDomain Xi))
    (h_scale : D 0 = Xi 0)
    (h_xi0 : Xi 0 ≠ 0) :
    ∀ s : ℂ, D s = Xi s := by
  have h_quot :=
    quotient_constant_on_connected_domain h_preconn h_open h_deriv_zero h_diff h_scale h_xi0
  apply eq_on_univ_of_eq_on_dense hD_cont hXi_cont h_dense
  intro s hs
  have hxi : Xi s ≠ 0 := hs
  have hq : D s / Xi s = 1 := h_quot s hs
  exact (div_eq_one_iff_eq hxi).mp hq

end RiemannAdelic
