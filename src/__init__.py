"""
Utilities for the 141 Hz analysis project.

This module provides core functionality for analyzing the universal constant
f₀ = 141.7001 ± 0.0016 Hz and the Noetic Coherent Force.

The dual spectral constant framework establishes:
- C_PRIMARY = 629.83: Primary spectral residue (structure)
- C_COHERENCE = 244.36: Derived coherence constant (form)

Both constants emerge from the H_Ψ operator and combine to produce f₀.
"""

from .constants import (
    UniversalConstants,
    CONSTANTS,
    F0,
    F0_UNCERTAINTY,
    ZETA_PRIME_HALF,
    PHI,
    GAMMA,
    H_PLANCK,
    H_BAR,
    C_LIGHT,
    E_PSI,
    E_PSI_EV,
    LAMBDA_PSI,
    R_PSI,
    M_PSI,
    T_PSI,
    # Spectral constants (Dual-Constant Framework)
    LAMBDA_0,
    LAMBDA_MEAN,
    C_PRIMARY,
    C_COHERENCE,
    COHERENCE_FACTOR,
)

from .noetic_force import (
    NoeticField,
    NoeticForce,
    NoeticForceDetection,
    summarize_noetic_force,
)

# Note: qcal_llm_core has encoding issues with Unicode subscripts
# Import it only if needed, not at module level
# from .qcal_llm_core import QCALLLMCore

from .spectral_origin import (
    SpectralOrigin,
    derive_f0_from_spectral,
    get_spectral_constants,
)

from .calabi_yau_invariant import (
    CalabiYauQuintic,
    LaplacianSpectrum,
    get_k_pi,
    verify_k_pi_invariant,
    get_invariant_summary,
    K_PI,
    K_PI_EXPECTED,
    MU_1,
    MU_2,
    NOETIC_PRIME,
)

from .noetic_consciousness_axiom import (
    NoeticConsciousnessAxiom,
    StateVector,
    ProjectionSpace,
    ConsciousnessState,
    create_axiom_validator,
    verify_state,
)

__all__ = [
    # Constants
    'UniversalConstants',
    'CONSTANTS',
    'F0',
    'F0_UNCERTAINTY',
    'ZETA_PRIME_HALF',
    'PHI',
    'GAMMA',
    'H_PLANCK',
    'H_BAR',
    'C_LIGHT',
    'E_PSI',
    'E_PSI_EV',
    'LAMBDA_PSI',
    'R_PSI',
    'M_PSI',
    'T_PSI',
    # Spectral Constants (Dual-Constant Framework)
    'LAMBDA_0',
    'LAMBDA_MEAN',
    'C_PRIMARY',
    'C_COHERENCE',
    'COHERENCE_FACTOR',
    # Spectral origin constants
    'LAMBDA_0',
    'LANGLE_LAMBDA',
    'C_PRIMARIA',
    'C_COHERENCIA',
    'GAMMA',
    'SpectralOrigin',
    'derive_f0_from_spectral',
    'get_spectral_constants',
    # Calabi-Yau Invariant k_Π
    'CalabiYauQuintic',
    'LaplacianSpectrum',
    'get_k_pi',
    'verify_k_pi_invariant',
    'get_invariant_summary',
    'K_PI',
    'K_PI_EXPECTED',
    'MU_1',
    'MU_2',
    'NOETIC_PRIME',
    # Noetic Force
    'NoeticField',
    'NoeticForce',
    'NoeticForceDetection',
    'summarize_noetic_force',
    # Noetic Consciousness Axiom
    'NoeticConsciousnessAxiom',
    'StateVector',
    'ProjectionSpace',
    'ConsciousnessState',
    'create_axiom_validator',
    'verify_state',
    # QCAL LLM Core (import separately if needed)
    # 'QCALLLMCore',
    # SIP Attention
    'SIPAttention',
    'create_sip_attention_demo',
]
