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
