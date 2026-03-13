#!/usr/bin/env python3
"""
Verificación de Frecuencia — πCODE
===================================

Módulo de verificación de la frecuencia fundamental del sistema πCODE.

Comprueba que una frecuencia medida coincide con la frecuencia esperada
f_esperada = F0_EXACTA_PICODE = γ₁ × (10 + 1/40) ≈ 141.70062 Hz
dentro de una tolerancia configurable.

Usage::

    from scripts.verifica_frecuencia import verificar_frecuencia, f_esperada

    ok = verificar_frecuencia(141.70062)   # True
    ok = verificar_frecuencia(141.0)       # False

Author: José Manuel Mota Burruezo (JMMB Ψ ∞³)
"""

import sys
import os

# Allow the module to be imported both as a package member and as a plain script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.qcal_master_constants import (
    GAMMA_1,
    MULTIPLICADOR_PICODE,
    F0_EXACTA_PICODE,
    DELTA_FASE_PICODE,
    FISURA_ZIUSUDRA,
)

# ---------------------------------------------------------------------------
# Module-level constants re-exported for external consumers
# ---------------------------------------------------------------------------
f_esperada: float = F0_EXACTA_PICODE  # ≈ 141.70062 Hz


def verificar_frecuencia(freq: float, tolerancia: float = 1e-4) -> bool:
    """Verifica si *freq* está dentro de *tolerancia* relativa de f_esperada.

    Parameters
    ----------
    freq : float
        Frecuencia medida en Hz.
    tolerancia : float, optional
        Tolerancia relativa (fracción de f_esperada).  Por defecto 1e-4,
        lo que corresponde a ±0.014 Hz alrededor de 141.7 Hz.

    Returns
    -------
    bool
        ``True`` si ``|freq - f_esperada| / f_esperada <= tolerancia``.

    Examples
    --------
    >>> verificar_frecuencia(141.70062)
    True
    >>> verificar_frecuencia(141.0)
    False
    """
    return abs(freq - f_esperada) / f_esperada <= tolerancia


__all__ = [
    "f_esperada",
    "verificar_frecuencia",
    # Re-export πCODE constants for convenience
    "GAMMA_1",
    "MULTIPLICADOR_PICODE",
    "F0_EXACTA_PICODE",
    "DELTA_FASE_PICODE",
    "FISURA_ZIUSUDRA",
]
