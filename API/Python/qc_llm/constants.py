"""
Constants for QC-LLM

Centralized constants for the quantum coherence framework
"""

# Fundamental frequency
F0 = 141.7001  # Hz

# DOI for citation
DOI = "10.5281/zenodo.17379721"

# Mathematical constants used in derivation
GOLDEN_RATIO = 1.618033988749895  # φ
EULER_MASCHERONI = 0.5772156649015329  # γ
ZETA_PRIME_HALF = -1.4603545088095868  # ζ'(1/2)
SQRT_TWO = 1.41421356237  # √2
SCALE_FACTOR = 16.195  # k

# Computation constants
DEFAULT_QUANTUM_ENTROPY = 0.5  # Default value when entropy computation fails
EPSILON_ZERO_PROTECTION = 1e-10  # Small value to prevent log(0) errors

# Coherence thresholds
THRESHOLD_HIGH = 0.8  # High coherence threshold
THRESHOLD_MODERATE = 0.6  # Moderate coherence threshold
THRESHOLD_LOW = 0.4  # Low coherence threshold

# Weights for coherence computation
WEIGHT_FREQUENCY_ALIGNMENT = 0.6
WEIGHT_QUANTUM_ENTROPY = 0.4

# Repository information
GITHUB_REPO = "https://github.com/motanova84/141hz"
AUTHOR = "José Manuel Mota Burruezo"
AUTHOR_EMAIL = "institutoconsciencia@proton.me"

# Derivation formula
DERIVATION_FORMULA = "f₀ = √2 × f_ref where f_ref = |ζ'(1/2)| × φ³"

# Version
VERSION = "1.0.0"
