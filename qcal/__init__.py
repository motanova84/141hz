"""
QCAL - Quantum Coherence Analysis for LLMs
Based on Ψ = I × A_eff² and f₀ = 141.7001 Hz

This module provides tools for evaluating LLM outputs using quantum coherence metrics.
"""

from .coherence import psi_score, strich_rate, compute_intention, compute_effectiveness
from .metrics import kl_divergence, snr, repetition_rate, semantic_density

__version__ = "1.0.0"
__all__ = [
    "psi_score",
    "strich_rate",
    "compute_intention",
    "compute_effectiveness",
    "kl_divergence",
    "snr",
    "repetition_rate",
    "semantic_density",
]

# Fundamental constants
F0 = 141.7001  # Hz - Universal frequency
PHI = 1.618033988749895  # Golden ratio
ZETA_PRIME_HALF = -1.460  # ζ'(1/2)
