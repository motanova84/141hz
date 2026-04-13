import Lake
open Lake DSL

package «f0derivation» where
  -- add package configuration options here

lean_lib «F0Derivation» where
  -- add library configuration options here

@[default_target]
lean_exe «f0derivation» where
  root := `Main
  -- Enables the use of the Lean interpreter by the executable (e.g.,
  -- `runFrontend`) at the expense of increased binary size on Linux.
  -- Remove this line if you do not need such functionality.
  supportInterpreter := true
package f0derivation where
  -- Project metadata
  version := v!"0.1.0"
  keywords := #["mathematics", "physics", "zeta-function", "golden-ratio"]
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib F0Derivation where
  -- Source files
  roots := #[`F0Derivation]
  globs := #[.submodules `F0Derivation]

lean_lib Invariants where
  -- Calabi-Yau spectral invariants
  roots := #[`Invariants]

lean_lib KappaPhi where
  -- κ_Π = 2.5773 corrected formalization
  roots := #[`KappaPhi]

lean_lib BerryKeating where
  -- Berry-Keating operator H_Ψ formalization
  roots := #[`BerryKeating]

lean_lib QCAL_SYNC_BRIDGE where
  -- Harmonic validation: f_base → f₀ → f_high
  roots := #[`QCAL_SYNC_BRIDGE]

lean_lib Noesis88 where
  -- Deductive chains and asymptotic stability
  roots := #[`Noesis88]
  globs := #[.submodules `Noesis88]

lean_lib EmergentTime where
  -- Emergent noetic time formalization
  roots := #[`F0Derivation.EmergentTime]
lean_lib TiempoNoetico where
  -- RAM-XVIII: Temporal emergence as noetic structure
  roots := #[`TiempoNoetico]

lean_lib MicrotubuleCoherence where
  -- Orch-OR theory: Quantum consciousness in microtubules
  roots := #[`MicrotubuleCoherence]
  -- Teorema de la Carne Resonante: Biological consciousness at f₀
  roots := #[`MicrotubuleCoherence]
lean_lib GoldbachCircle where
  -- Hardy-Littlewood Circle Method: Large Sieve + Vaughan + Minor Arcs
  -- Main theorem: goldbach_existence_structural
  roots := #[`GoldbachCircle]
  globs := #[.submodules `GoldbachCircle]

lean_lib PicodePT where
  -- πCODE PT Non-Hermitian Operator: AdS/CFT + Riemann stabilizer
  -- Proves spectral reality under γ < γ_c = 2.57 (Bender-Boettcher 1998)
  srcDir := "../../physics"
  roots := #[`PicodePT]

lean_lib OperadorAutoadjuntoH where
  -- SC-1/SC-2/SC-3: Self-adjoint operator H on adelic L²(Σ)
  -- Weil trace formula, Weierstrass product Δ(s), Paley-Wiener identity Δ(s) = ξ(s)
  srcDir := "../../physics"
  roots := #[`OperadorAutoadjuntoH]
