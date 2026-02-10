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
# Spectral embedding modules (new)
try:
    from .spectral_embedding import SpectralEmbedding
    from .dataset import DatasetGenerator
    from .embedding_comparison import (
        BaselineEmbedding,
        Word2VecEmbedding,
        EmbeddingEvaluator
    )
    SPECTRAL_EMBEDDING_AVAILABLE = True
except ImportError:
    SPECTRAL_EMBEDDING_AVAILABLE = False

# Dual mass perspective module (new)
try:
    from .dual_mass import (
        DualMassPerspective,
        effective_mass,
        noetic_mass,
        unified_mass,
        calculate_dual_mass_spectrum
    )
    DUAL_MASS_AVAILABLE = True
except ImportError:
    DUAL_MASS_AVAILABLE = False

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

# Add spectral embedding exports if available
if SPECTRAL_EMBEDDING_AVAILABLE:
    __all__.extend([
        "SpectralEmbedding",
        "DatasetGenerator",
        "BaselineEmbedding",
        "Word2VecEmbedding",
        "EmbeddingEvaluator"
    ])

# Unified theory modules
try:
    from .unified_theory import (
        UnifiedTheoryConstants,
        RiemannZetaComponent,
        CalabiYauComponent,
        FrequencyComponent,
        ConsciousnessComponent,
        GravityComponent,
        SpectrumComponent,
        CondensedMatterComponent,
        UnifiedTheory
    )
    UNIFIED_THEORY_AVAILABLE = True
except ImportError:
    UNIFIED_THEORY_AVAILABLE = False

# Add unified theory exports if available
if UNIFIED_THEORY_AVAILABLE:
    __all__.extend([
        "UnifiedTheoryConstants",
        "RiemannZetaComponent",
        "CalabiYauComponent",
        "FrequencyComponent",
        "ConsciousnessComponent",
        "GravityComponent",
        "SpectrumComponent",
        "CondensedMatterComponent",
        "UnifiedTheory"
    ])

# Add dual mass exports if available
if DUAL_MASS_AVAILABLE:
    __all__.extend([
        "DualMassPerspective",
        "effective_mass",
        "noetic_mass",
        "unified_mass",
        "calculate_dual_mass_spectrum"
    ])

# Dimensional analysis module
try:
    from .dimensional_analysis_psi import (
        DimensionalQuantity,
        validate_aeff_dimensionless,
        validate_psi_formula,
        validate_limit_behavior,
        compare_to_physics_coupling_factors,
        complete_dimensional_validation,
        print_validation_report
    )
    DIMENSIONAL_ANALYSIS_AVAILABLE = True
except ImportError:
    DIMENSIONAL_ANALYSIS_AVAILABLE = False

# Add dimensional analysis exports if available
if DIMENSIONAL_ANALYSIS_AVAILABLE:
    __all__.extend([
        "DimensionalQuantity",
        "validate_aeff_dimensionless",
        "validate_psi_formula",
        "validate_limit_behavior",
        "compare_to_physics_coupling_factors",
        "complete_dimensional_validation",
        "print_validation_report"
    ])

# Local Node Simulation modules
try:
    from .local_node_simulation import (
        LocalNodeSimulation,
        NodeState
    )
    LOCAL_NODE_SIMULATION_AVAILABLE = True
except ImportError:
    LOCAL_NODE_SIMULATION_AVAILABLE = False

# Add local node simulation exports if available
if LOCAL_NODE_SIMULATION_AVAILABLE:
    __all__.extend([
        "LocalNodeSimulation",
        "NodeState"
    ])

# Spiral Light Path modules
try:
    from .spiral_light_path import (
        SpiralLightPath,
        SpiralParameters
    )
    SPIRAL_LIGHT_PATH_AVAILABLE = True
except ImportError:
    SPIRAL_LIGHT_PATH_AVAILABLE = False

# Add spiral light path exports if available
if SPIRAL_LIGHT_PATH_AVAILABLE:
    __all__.extend([
        "SpiralLightPath",
        "SpiralParameters"
    ])

# Cosmic parameters module
try:
    from .cosmic_parameters import (
        CurrentUniverseParameters,
        CosmicEpoch,
        CosmicTimeline,
        CURRENT_UNIVERSE,
        COSMIC_TIMELINE,
        get_universe_age,
        get_cmb_temperature,
        get_epoch,
        print_timeline
    )
    COSMIC_PARAMETERS_AVAILABLE = True
except ImportError:
    COSMIC_PARAMETERS_AVAILABLE = False

# Add cosmic parameters exports if available
if COSMIC_PARAMETERS_AVAILABLE:
    __all__.extend([
        "CurrentUniverseParameters",
        "CosmicEpoch",
        "CosmicTimeline",
        "CURRENT_UNIVERSE",
        "COSMIC_TIMELINE",
        "get_universe_age",
        "get_cmb_temperature",
        "get_epoch",
        "print_timeline"
    ])

# Fundamental constants
F0 = 141.7001  # Hz - Universal frequency
PHI = 1.618033988749895  # Golden ratio
ZETA_PRIME_HALF = -1.460  # ζ'(1/2) (approximate)
KAPPA_PI = 2.5782  # Topological constant κ_Π
PSI_RESONANCE = 0.923  # Noetic resonance Ψ
