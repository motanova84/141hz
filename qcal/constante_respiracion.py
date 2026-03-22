#!/usr/bin/env python3
"""
ConstanteRespiracion — Breathing Constant of the 141 Hz Field
==============================================================

Encodes the two fundamental frequency gaps that define the
"breathing space" between the material node (142.1 Hz) and
the QCAL fundamental frequency f₀ = 141.7001 Hz:

    DELTA_F_MATERIAL = 142.1 - 141.7001 ≈ 0.3999 Hz
    DELTA_F_AUREA    = (φ - 1) · f₀ · 10⁻³

Both deltas must lie in the validation interval [0.38, 0.42] Hz.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
from typing import Tuple

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

F0_HZ: float = 141.7001   # Hz – QCAL fundamental frequency
F_MATERIAL_HZ: float = 142.1   # Hz – Material node (Nodo 7)

# Golden ratio φ = (1 + √5) / 2
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# ============================================================================
# BREATHING CONSTANTS
# ============================================================================

# Material gap: the difference between the material node and f₀
DELTA_F_MATERIAL: float = F_MATERIAL_HZ - F0_HZ  # ≈ 0.3999 Hz

# Golden gap: (φ − 1) · f₀ · 10⁻³
# φ − 1 = 1/φ ≈ 0.6180  → 0.6180 · 141.7001 · 0.001 ≈ 0.4013 Hz
DELTA_F_AUREA: float = (PHI - 1.0) * F0_HZ * 1e-3

# Validation interval [Hz]
DELTA_F_MIN: float = 0.38
DELTA_F_MAX: float = 0.42


# ============================================================================
# VALIDATION
# ============================================================================

def validar_espacio_respiracion(delta_f: float) -> bool:
    """Return True if *delta_f* lies in the interval [0.38, 0.42] Hz."""
    return DELTA_F_MIN <= delta_f <= DELTA_F_MAX


def obtener_espacio_respiracion() -> Tuple[float, float]:
    """
    Return (DELTA_F_MATERIAL, DELTA_F_AUREA).

    Validates that DELTA_F_MATERIAL lies in the breathing interval
    [DELTA_F_MIN, DELTA_F_MAX].  DELTA_F_AUREA is computed from the golden
    ratio and is returned as-is (it represents a different frequency scale).
    """
    if not validar_espacio_respiracion(DELTA_F_MATERIAL):
        raise ValueError(
            f"DELTA_F_MATERIAL = {DELTA_F_MATERIAL:.6f} Hz is outside the "
            f"breathing interval [{DELTA_F_MIN}, {DELTA_F_MAX}] Hz"
        )
    return DELTA_F_MATERIAL, DELTA_F_AUREA


# ============================================================================
# MODULE-LEVEL ASSERTIONS (run at import time)
# ============================================================================

# The breathing-space validation applies to DELTA_F_MATERIAL
assert validar_espacio_respiracion(DELTA_F_MATERIAL), (
    f"DELTA_F_MATERIAL = {DELTA_F_MATERIAL:.6f} Hz outside [{DELTA_F_MIN}, {DELTA_F_MAX}]"
)


# ============================================================================
# CLASS INTERFACE
# ============================================================================

class ConstanteRespiracion:
    """
    Encapsulates the breathing-space constants of the 141 Hz field.

    Attributes
    ----------
    delta_f_material : float
        Material gap  142.1 − 141.7001 ≈ 0.3999 Hz.
    delta_f_aurea : float
        Golden gap  (φ−1)·f₀·10⁻³ ≈ 0.4013 Hz.
    """

    delta_f_material: float = DELTA_F_MATERIAL
    delta_f_aurea: float = DELTA_F_AUREA
    f0_hz: float = F0_HZ
    f_material_hz: float = F_MATERIAL_HZ
    phi: float = PHI

    # Validation interval
    delta_f_min: float = DELTA_F_MIN
    delta_f_max: float = DELTA_F_MAX

    def __init__(self) -> None:
        self._validar()

    def _validar(self) -> None:
        """Assert DELTA_F_MATERIAL lies in [0.38, 0.42] Hz."""
        obtener_espacio_respiracion()

    def es_valido(self, delta_f: float) -> bool:
        """Return True if *delta_f* ∈ [0.38, 0.42] Hz."""
        return validar_espacio_respiracion(delta_f)

    def resumen(self) -> dict:
        """Return a summary dictionary with all key values."""
        return {
            "f0_hz": self.f0_hz,
            "f_material_hz": self.f_material_hz,
            "phi": self.phi,
            "delta_f_material": self.delta_f_material,
            "delta_f_aurea": self.delta_f_aurea,
            "intervalo_valido": (self.delta_f_min, self.delta_f_max),
            "material_valido": self.es_valido(self.delta_f_material),
            "aurea_valido": self.es_valido(self.delta_f_aurea),
        }
