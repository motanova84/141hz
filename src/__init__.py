"""
Utilities for the 141 Hz analysis project.

This module provides core functionality for analyzing the universal constant
f₀ = 141.7001 ± 0.0016 Hz and the Noetic Coherent Force.
"""

from .constants import (
    UniversalConstants,
    CONSTANTS,
    F0,
    F0_UNCERTAINTY,
    ZETA_PRIME_HALF,
    PHI,
    H_PLANCK,
    H_BAR,
    C_LIGHT,
    E_PSI,
    E_PSI_EV,
    LAMBDA_PSI,
    R_PSI,
    M_PSI,
    T_PSI,
)

from .noetic_force import (
    NoeticField,
    NoeticForce,
    NoeticForceDetection,
    summarize_noetic_force,
)

from .qcal_llm_core import (
    QCALLLMCore,
)

__all__ = [
    # Constants
    'UniversalConstants',
    'CONSTANTS',
    'F0',
    'F0_UNCERTAINTY',
    'ZETA_PRIME_HALF',
    'PHI',
    'H_PLANCK',
    'H_BAR',
    'C_LIGHT',
    'E_PSI',
    'E_PSI_EV',
    'LAMBDA_PSI',
    'R_PSI',
    'M_PSI',
    'T_PSI',
    # Noetic Force
    'NoeticField',
    'NoeticForce',
    'NoeticForceDetection',
    'summarize_noetic_force',
    # QCAL LLM Core
    'QCALLLMCore',
    # SIP Attention
    'SIPAttention',
    'create_sip_attention_demo',
]
