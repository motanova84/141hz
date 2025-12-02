"""
Dyadic Analysis Module

Implements scale-dependent dissipation analysis using Littlewood-Paley decomposition
for the Navier-Stokes equations.
"""

from .riccati_dyadic import (
    RiccatiParameters,
    dyadic_riccati_coefficient,
    find_dissipative_scale,
    verify_dyadic_analysis
)

__all__ = [
    "RiccatiParameters",
    "dyadic_riccati_coefficient",
    "find_dissipative_scale",
    "verify_dyadic_analysis"
]
