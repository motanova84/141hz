"""
Parabolic Coercivity Module

Implements the parabolic coercivity lemma and effective damping coefficient
calculations for Navier-Stokes equations.
"""

from .coercivity_lemma import (
    ParabolicCoercivity,
    verify_coercivity_estimates
)

__all__ = [
    "ParabolicCoercivity",
    "verify_coercivity_estimates"
]
