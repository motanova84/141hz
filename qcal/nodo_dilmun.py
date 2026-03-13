#!/usr/bin/env python3
"""
NodoDilmun — Node 7 Anchor at 142.1 Hz
========================================

Anchors the QCAL system state to 142.1 Hz (the material "Nodo Dilmun", Node 7)
and computes the coherence between an input frequency and the anchor via

    Ψ = cos²(π · δf / f_ancla)

where  δf = |f - f_ancla|.

When  f = f₀ = 141.7001 Hz  and  f_ancla = 142.1 Hz:

    δf = 0.3999 Hz
    Ψ  = cos²(π · 0.3999 / 142.1)
       ≈ cos²(0.008835)
       ≈ 0.99992

This value is ≈ 0.9999, confirming near-perfect coherence between
the fundamental frequency and the material anchor node.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
from typing import Optional

# ============================================================================
# CONSTANTS
# ============================================================================

# Anchor frequency — Material Node 7
F_ANCLA_HZ: float = 142.1   # Hz

# QCAL fundamental frequency
F0_HZ: float = 141.7001   # Hz

# Node identifier
NODO_ID: int = 7
NODO_NOMBRE: str = "Dilmun"

# Expected Ψ at f₀
_PSI_F0_EXPECTED: float = math.cos(math.pi * abs(F0_HZ - F_ANCLA_HZ) / F_ANCLA_HZ) ** 2


# ============================================================================
# CORE FORMULA
# ============================================================================

def calcular_psi(f_hz: float, f_ancla: float = F_ANCLA_HZ) -> float:
    """
    Return the coherence Ψ = cos²(π · δf / f_ancla).

    Parameters
    ----------
    f_hz :
        Input frequency in Hz.
    f_ancla :
        Anchor frequency in Hz (default: 142.1 Hz).

    Returns
    -------
    float
        Ψ ∈ [0, 1].
    """
    delta_f = abs(f_hz - f_ancla)
    return math.cos(math.pi * delta_f / f_ancla) ** 2


# ============================================================================
# NODE CLASS
# ============================================================================

class NodoDilmun:
    """
    Node 7 — Dilmun anchor at 142.1 Hz.

    Computes the coherence Ψ between any input frequency and the
    material anchor via the cosine-squared formula:

        Ψ(f) = cos²(π · |f − f_ancla| / f_ancla)

    At f = f₀ = 141.7001 Hz the result is Ψ ≈ 0.9999.

    Parameters
    ----------
    f_ancla :
        Anchor frequency in Hz.  Defaults to 142.1 Hz (Nodo 7).
    umbral_psi :
        Minimum acceptable coherence.  Defaults to 0.999.
    """

    nodo_id: int = NODO_ID
    nodo_nombre: str = NODO_NOMBRE

    def __init__(
        self,
        f_ancla: float = F_ANCLA_HZ,
        umbral_psi: float = 0.999,
    ) -> None:
        self.f_ancla = f_ancla
        self.umbral_psi = umbral_psi

    # ------------------------------------------------------------------

    def psi(self, f_hz: float) -> float:
        """Return Ψ = cos²(π · δf / f_ancla) for frequency *f_hz*."""
        return calcular_psi(f_hz, self.f_ancla)

    def delta_f(self, f_hz: float) -> float:
        """Return |f_hz − f_ancla| in Hz."""
        return abs(f_hz - self.f_ancla)

    def es_coherente(self, f_hz: float) -> bool:
        """Return True if Ψ(f_hz) ≥ umbral_psi."""
        return self.psi(f_hz) >= self.umbral_psi

    def estado(self, f_hz: Optional[float] = None) -> dict:
        """
        Return a summary of the node state for *f_hz*.

        If *f_hz* is None, uses F0_HZ = 141.7001 Hz.
        """
        if f_hz is None:
            f_hz = F0_HZ
        psi_val = self.psi(f_hz)
        return {
            "nodo_id": self.nodo_id,
            "nodo_nombre": self.nodo_nombre,
            "f_ancla_hz": self.f_ancla,
            "f_entrada_hz": f_hz,
            "delta_f_hz": self.delta_f(f_hz),
            "psi": psi_val,
            "umbral_psi": self.umbral_psi,
            "coherente": psi_val >= self.umbral_psi,
        }
