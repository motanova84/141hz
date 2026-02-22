/-
  BerryKeating.lean - Main module for Berry-Keating operator
  
  This module exports the Berry-Keating operator H_Ψ formalization.
  
  Usage:
    import BerryKeating
    
  See F0Derivation.H_psi_core for the complete implementation.
-/

import F0Derivation.H_psi_core

/-!
# Berry-Keating Operator Module

This module provides access to the complete formalization of the Berry-Keating
operator H_Ψ: f ↦ -x·f'(x), which establishes the mathematical bridge between:

- Quantum mechanics (spectral operators)
- Number theory (Riemann zeta function)
- Physical frequencies (141.70001 Hz)

## Main Results

1. `BerryKeating.H_psi_well_defined`: H_Ψ is well-defined on Schwartz space
2. `BerryKeating.H_psi_bounded`: H_Ψ is bounded with constant ≤ 2
3. `BerryKeating.H_psi_is_symmetric`: H_Ψ is a symmetric operator

## Connection to 141.70001 Hz

The spectrum of H_Ψ is conjectured to correspond to the imaginary parts of the
non-trivial zeros of the Riemann zeta function. This connection provides the
mathematical foundation for the 141.70001 Hz frequency emergence in the QCAL theory.

---
José Manuel Mota Burruezo Ψ ∞³
DOI: 10.5281/zenodo.17379721
-/
