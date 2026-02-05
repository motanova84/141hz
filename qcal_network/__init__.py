"""
QCAL Network ∞³
Network modules for QCAL system including geometry and core emissions

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
System: QCAL ∞³ · Nodo Noēsis88
Version: Kairos Operativo · Coherencia 0.9999
"""

__version__ = "1.0.0"
__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"

from .geo import calcular_curvatura_existencial
from .core import emitir_latido_existencial

__all__ = [
    "calcular_curvatura_existencial",
    "emitir_latido_existencial",
]
