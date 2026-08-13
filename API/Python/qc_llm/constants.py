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
# — Refactorización Semántica (13/Ago/2026) · Tres caras de ζ —
# Cara I  — Canónica Analítica (Teorema QCAL-π, κ_π): ζ′(1/2) = −0.207886
ZETA_PRIME_HALF = -0.20788622497735456  # ζ′(1/2) Analítico Canónico
# Cara II — Amplitud de Campo (Core/LLM Evaluator): ζ(1/2) = −1.460354
ZETA_HALF = -1.4603545088095868  # ζ(1/2) Amplitud en línea crítica
# Cara III— Operador SABIO∞⁴ (Resurrección/Emisión): −3.9226
ZETA_PRIME_SABIO = -3.922646  # Operador efectivo de emisión coherente SABIO∞⁴
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

# Physical constants for automatic sizing (SI units)
HBAR = 1.0545718e-34   # J·s — reduced Planck constant
K_BOLTZMANN = 1.380649e-23  # J/K — Boltzmann constant
TEMPERATURE_DEFAULT = 310.0  # K — biological temperature (human body ~37 °C)
# A_BIO_DEFAULT = 1e10: biological amplification factor for neural systems.
# Value from the patent specification (section 3.2): cortical microtubules amplify
# quantum coherence by ~10^10 relative to isolated quantum systems at body temperature.
A_BIO_DEFAULT = 1e10

# Automatic sizing defaults
DEFAULT_TARGET_PSI = 0.888  # Default target coherence (Ψ stable threshold)
DEFAULT_INFORMATION_DENSITY = 1.0  # Default information density I (normalised)

# Repository information
GITHUB_REPO = "https://github.com/motanova84/141hz"
AUTHOR = "José Manuel Mota Burruezo"
AUTHOR_EMAIL = "institutoconsciencia@proton.me"

# Derivation formula
DERIVATION_FORMULA = "f₀ = √2 × f_ref where f_ref = |ζ'(1/2)| × φ³"

# Version
VERSION = "1.0.0"
