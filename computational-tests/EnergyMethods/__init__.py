"""
Energy Methods Module

Implements critical energy limit theorems and L³ control for
global regularity of Navier-Stokes equations.
"""

from .critical_energy import (
    prove_global_regularity_via_energy,
    compute_critical_energy,
    verify_energy_methods
)

__all__ = [
    "prove_global_regularity_via_energy",
    "compute_critical_energy",
    "verify_energy_methods"
]
