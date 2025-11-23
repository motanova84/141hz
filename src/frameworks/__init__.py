#!/usr/bin/env python3
"""
Unified Framework Integration for 141Hz Quantum-Consciousness Project

This module integrates five fundamental mathematical frameworks:
1. Riemann-adelic: Spectral structure via zeta function and adelic geometry
2. Adelic-BSD: Arithmetic geometry through Birch-Swinnerton-Dyer conjecture
3. P-NP: Informational limits via computational complexity theory
4. 141Hz: Quantum-conscious foundation at f₀ = 141.7001 Hz
5. Navier-Stokes: Continuous framework for fluid dynamics regularization

Each framework provides complementary perspectives on the fundamental
frequency f₀ and its manifestations in physical systems.
"""

from .riemann_adelic import RiemannAdelicFramework
from .adelic_bsd import AdelicBSDFramework
from .p_np_complexity import PNPComplexityFramework
from .quantum_conscious import QuantumConsciousFoundation
from .navier_stokes import NavierStokesFramework
from .orchestrator import FrameworkOrchestrator

__all__ = [
    'RiemannAdelicFramework',
    'AdelicBSDFramework',
    'PNPComplexityFramework',
    'QuantumConsciousFoundation',
    'NavierStokesFramework',
    'FrameworkOrchestrator',
]

__version__ = '1.0.0'
