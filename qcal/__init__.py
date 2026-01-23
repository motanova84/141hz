"""
QCAL - Quantum Coherence Analysis for LLMs
Based on Ψ = I × A_eff² and f₀ = 141.7001 Hz

This module provides tools for evaluating LLM outputs using quantum coherence metrics
and QCAL Token Compression achieving ~1000:1 ratio.
"""

from .coherence import psi_score, strich_rate, compute_intention, compute_effectiveness
from .metrics import kl_divergence, snr, repetition_rate, semantic_density
from .ecuacion_viva import EcuacionViva

# Token compression modules (new)
try:
    from .token_compressor import (
        EmissionAxiom,
        AdelicEncoder,
        NoeticCollapser,
        QCALTokenCompressor
    )
    from .udp_vibrational_field import (
        VibrationalPacket,
        VibrationalFieldEncoder,
        UDPMulticastTransmitter,
        UDPMulticastReceiver,
        QCALVibrationalTransport
    )
    TOKEN_COMPRESSION_AVAILABLE = True
except ImportError:
    TOKEN_COMPRESSION_AVAILABLE = False

# Text encoding module
try:
    from .text_encoder import QCALTextEncoder
    TEXT_ENCODER_AVAILABLE = True
except ImportError:
    TEXT_ENCODER_AVAILABLE = False

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
    "EcuacionViva",
]

# Add token compression exports if available
if TOKEN_COMPRESSION_AVAILABLE:
    __all__.extend([
        "EmissionAxiom",
        "AdelicEncoder",
        "NoeticCollapser",
        "QCALTokenCompressor",
        "VibrationalPacket",
        "VibrationalFieldEncoder",
        "UDPMulticastTransmitter",
        "UDPMulticastReceiver",
        "QCALVibrationalTransport"
    ])

# Add text encoder exports if available
if TEXT_ENCODER_AVAILABLE:
    __all__.extend([
        "QCALTextEncoder"
    ])

# Fundamental constants
F0 = 141.7001  # Hz - Universal frequency
PHI = 1.618033988749895  # Golden ratio
ZETA_PRIME_HALF = -1.460  # ζ'(1/2) (approximate)
KAPPA_PI = 2.5782  # Topological constant κ_Π
PSI_RESONANCE = 0.923  # Noetic resonance Ψ
