import Lake
open Lake DSL

package qcal_lean where
  -- QCAL Formalization Project (Hilo A)
  -- Objetivo: 0 sorries en el kernel
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.7.0"

@[default_target]
lean_lib QCAL where
  roots := #[
    `QCAL.F_Ψ_Purified,
    `QCAL.Domain_Invariant,
    `QCAL.Stability,
    `QCAL.Completeness,
    `QCAL.StabilityMatrix
  ]
