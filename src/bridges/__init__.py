#!/usr/bin/env python3
"""
Cross-Repository Integration Bridges for QCAL ∞³ Ecosystem

This module provides integration bridges that connect quantum-internet-qcal
with all repositories in the QCAL ecosystem, enabling seamless data flow
and synchronization at f₀ = 141.7001 Hz.

Bridges:
    1. RamseyBridge: Graph theory for entangled network topology
    2. NavierStokesBridge: Fluid dynamics for decoherence suppression
    3. ComplexityBridge: Quantum algorithm analysis
    4. RiemannAdelicBridge: Mathematical frequency derivation
    5. AdelicBSDBridge: Spectral parameter calibration

All bridges maintain frequency synchronization and quantum coherence.
"""

from .ramsey_bridge import RamseyBridge
from .navier_stokes_bridge import NavierStokesBridge
from .complexity_bridge import ComplexityBridge
from .riemann_adelic_bridge import RiemannAdelicBridge
from .adelic_bsd_bridge import AdelicBSDBridge

__all__ = [
    'RamseyBridge',
    'NavierStokesBridge',
    'ComplexityBridge',
    'RiemannAdelicBridge',
    'AdelicBSDBridge',
]

__version__ = '1.0.0'

# Ecosystem configuration
ECOSYSTEM_REPOSITORIES = {
    'quantum-internet-qcal': 'https://github.com/qcal/quantum-internet-qcal',
    'ramsey-theory': 'https://github.com/qcal/ramsey-theory',
    'navier-stokes': 'https://github.com/qcal/navier-stokes',
    'complexity-theory': 'https://github.com/qcal/complexity-theory',
    'riemann-adelic': 'https://github.com/qcal/riemann-adelic',
    'adelic-bsd': 'https://github.com/qcal/adelic-bsd',
    '141hz': 'https://github.com/motanova84/141hz',
    'consciousness-field': 'https://github.com/qcal/consciousness-field',
}

# Fundamental frequency
F0_HZ = 141.7001
