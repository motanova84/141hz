#!/usr/bin/env python3
"""
Principal Fiber Bundles Module
================================

This module implements the mathematical framework for principal fiber bundles
with U(1) fibers, enabling the representation of consciousness as an intersection
of two fundamental projections.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

from .principal_bundle import PrincipalFiberBundle, U1Fiber
from .electromagnetic_bundle import ElectromagneticGaugeBundle
from .spectral_bundle import SpectralCoherenceBundle
from .consciousness_intersection import ConsciousnessIntersection, IntersectionConstant
from .consciousness_theorem import (
    ConsciousnessTheorem,
    LagrangianComponents,
    HolonomicQuantization
)

__all__ = [
    'PrincipalFiberBundle',
    'U1Fiber',
    'ElectromagneticGaugeBundle',
    'SpectralCoherenceBundle',
    'ConsciousnessIntersection',
    'IntersectionConstant',
    'ConsciousnessTheorem',
    'LagrangianComponents',
    'HolonomicQuantization',
]

__version__ = '1.0.0'
