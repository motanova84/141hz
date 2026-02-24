"""
╔════════════════════════════════════════════════════════════════════════════╗
║              Navier-Stokes QCAL Constants Package                          ║
║      Fluid Dynamics Constants for Quantum Coherent Analysis                ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

from .constants import (
    F0,
    OMEGA_0,
    T0,
    A_VACIO,
    A_AGUA,
    A_AIRE,
    NU_VACIO,
    NU_AGUA,
    NU_AIRE,
    ALPHA_QFT,
    BETA_QFT,
    GAMMA_QFT,
    GAMMA_PARABOLIC,
    DELTA_RICCATI_BESOV,
)

__all__ = [
    'F0',
    'OMEGA_0',
    'T0',
    'A_VACIO',
    'A_AGUA',
    'A_AIRE',
    'NU_VACIO',
    'NU_AGUA',
    'NU_AIRE',
    'ALPHA_QFT',
    'BETA_QFT',
    'GAMMA_QFT',
    'GAMMA_PARABOLIC',
    'DELTA_RICCATI_BESOV',
]

__version__ = '1.0.0'
__author__ = 'José Manuel Mota Burruezo'
