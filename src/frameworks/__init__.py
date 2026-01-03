#!/usr/bin/env python3
"""
Unified Framework Integration for 141Hz Quantum-Consciousness Project

This module reveals how the universe expresses its fundamental frequency
f₀ = 141.7001 Hz through five complementary mathematical domains:

1. Riemann-adelic: Spectral structure via zeta function and adelic geometry
2. Adelic-BSD: Arithmetic geometry through Birch-Swinnerton-Dyer conjecture
3. P-NP: Informational limits via computational complexity theory
4. 141Hz: Quantum-conscious foundation at f₀ = 141.7001 Hz
5. Navier-Stokes: Continuous framework for fluid dynamics regularization

Philosophical Note:
    These are not "external models" but rather different mathematical
    languages through which the universe expresses its intrinsic structure.
    
    See: UNIVERSO_AUTOEXPRESION.md for complete philosophical foundation.
"""

from .riemann_adelic import RiemannAdelicFramework
from .adelic_bsd import AdelicBSDFramework
from .p_np_complexity import PNPComplexityFramework
from .quantum_conscious import QuantumConsciousFoundation
from .navier_stokes import NavierStokesFramework
from .orchestrator import UniversalStructureOrchestrator, FrameworkOrchestrator

__all__ = [
    'RiemannAdelicFramework',
    'AdelicBSDFramework',
    'PNPComplexityFramework',
    'QuantumConsciousFoundation',
    'NavierStokesFramework',
    'UniversalStructureOrchestrator',
    'FrameworkOrchestrator',  # Backward compatibility alias
]

__version__ = '1.1.0'  # Updated for philosophical clarity
