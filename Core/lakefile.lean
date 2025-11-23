import Lake
open Lake DSL

package «QC_LLM_Core» where
  version := "1.0.0"

@[default_target]
lean_lib «FrequencyDerivation» where
  roots := #[`Core.FrequencyDerivation]

require mathlib from git
  "https://github.com/leanprover/mathlib4.git"
