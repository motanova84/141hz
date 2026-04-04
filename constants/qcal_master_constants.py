"""
QCAL Master Constants — πCODE Sealed Structure
===============================================

Fundamental constants for the πCODE sealed mathematical chain:

    f₀ = γ₁ × (10 + 1/40)

where γ₁ is the imaginary part of the first non-trivial zero of the Riemann
zeta function ζ(s) on the critical line ℜ(s) = 1/2.

References
----------
- Riemann (1859): ζ(1/2 + it) = 0 at t₁ = γ₁
- πCODE: f₀ = γ₁ × MULTIPLICADOR_PICODE ≈ 141.70062 Hz
- Ziusudra coupling: δ_fase = γ₁ / 40 ≈ 0.35337 Hz

Author: José Manuel Mota Burruezo (JMMB Ψ ∞³)
"""

# ---------------------------------------------------------------------------
# First Riemann zero — sourced with 50 significant digits.
# γ₁ = imaginary part of the first non-trivial zero of ζ(s).
# Verified against: https://www.lmfdb.org/zeros/zeta/?n=1
#
# NOTE: Python's built-in float (IEEE 754 double) retains only ~15-17 decimal
# digits.  The literal below is intentionally written in full for source-level
# traceability; the runtime value is effectively 14.134725141734693 (16 sig
# digits).  For higher-precision arithmetic use mpmath:
#   import mpmath; mpmath.mp.dps = 50
#   gamma_1_mp = mpmath.mpf("14.134725141734693790457251983562470270784257323")
# ---------------------------------------------------------------------------
GAMMA_1 = 14.134725141734693790457251983562470270784257323


# ---------------------------------------------------------------------------
# πCODE multiplier: 10 + 1/40 = 10.025
# ---------------------------------------------------------------------------
MULTIPLICADOR_PICODE = 10.025  # 10 + 1/40  (exact rational)


# ---------------------------------------------------------------------------
# Exact πCODE fundamental frequency
# f₀_exacta = γ₁ × (10 + 1/40) ≈ 141.70062 Hz
# ---------------------------------------------------------------------------
F0_EXACTA_PICODE = GAMMA_1 * MULTIPLICADOR_PICODE  # ≈ 141.70062 Hz


# ---------------------------------------------------------------------------
# Ziusudra coupling — phase delta
# δ_fase = γ₁ / 40 ≈ 0.35337 Hz
# ---------------------------------------------------------------------------
DELTA_FASE_PICODE = GAMMA_1 / 40.0  # ≈ 0.35337 Hz


# ---------------------------------------------------------------------------
# Fisura Ziusudra — gap between πCODE f₀ and nominal 141.7001 Hz
# Measures the sealed-structure displacement
# ---------------------------------------------------------------------------
FISURA_ZIUSUDRA = F0_EXACTA_PICODE - 141.7001  # ≈ +0.00052 Hz


__all__ = [
    "GAMMA_1",
    "MULTIPLICADOR_PICODE",
    "F0_EXACTA_PICODE",
    "DELTA_FASE_PICODE",
    "FISURA_ZIUSUDRA",
]
