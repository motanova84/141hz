"""
Quantum Consciousness Module
Implements Orch-OR theory with f₀=141.7001 Hz synchronization
"""

from .microtubule_coherence import (
    MicrotubuleCoherence,
    StructuredWater,
    CoherenceState,
    calculate_thermal_noise_ratio,
    resonance_filter
)

__all__ = [
    'MicrotubuleCoherence',
    'StructuredWater',
    'CoherenceState',
    'calculate_thermal_noise_ratio',
    'resonance_filter'
]
