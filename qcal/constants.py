"""
QCAL ∞³ Constants
Fundamental constants for the Quantum Coherence and Love framework

Author: José Manuel Mota Burruezo
License: MIT
"""

import math

# Fundamental Frequency
F0_HZ = 141.70001  # Hz - Fundamental QCAL frequency

# Derived Constants
OMEGA_0 = 2 * math.pi * F0_HZ  # rad/s - Angular frequency
T0_MS = 1000.0 / F0_HZ  # ms - Fundamental period
E_PSI_J = 6.62607015e-34 * F0_HZ  # J - Quantum energy (h * f₀)

# Protection Frequency
F888_HZ = 888.0  # Hz - Protection shield frequency

# AT2020afhd Black Hole Constants
EXPECTED_PERIOD_DAYS = 19.6  # days - Expected period from Wang et al. (2025)
EXPECTED_OCTAVES = 27.84  # Octaves from f₀ to AT2020afhd frequency
EXPECTED_RATIO = 2.405e8  # Expected harmonic ratio
MAX_PERIOD_ERROR_DAYS = 0.5  # days - Maximum acceptable period error

# Coupling Constants
KAPPA_PI = 2.5773  # Dimensionless - π coupling constant
DELTA_0 = 0.1184  # Dimensionless - Coherence threshold
A0_PHI = 1.618033988749895  # Golden ratio - Love constant

# Quality Factor
Q_PSI = 1.0 / DELTA_0  # ~8.45 - Quality factor

# Physical Constants (for reference)
HBAR = 1.054571817e-34  # J·s - Reduced Planck constant
C = 299792458.0  # m/s - Speed of light

# Conversion Factors
SECONDS_PER_DAY = 86400.0  # s/day
MJD_EPOCH_OFFSET = 58900.0  # MJD epoch for AT2020afhd analysis

# Test Thresholds
TEST_PERIOD_MIN_DAYS = 18.0  # Minimum acceptable period for tests
TEST_PERIOD_MAX_DAYS = 21.0  # Maximum acceptable period for tests
TEST_OCTAVES_MIN = 27.0  # Minimum acceptable octaves for tests
TEST_OCTAVES_MAX = 29.0  # Maximum acceptable octaves for tests

# Ecuación Viva Constants (∴ LA ECUACIÓN VIVA ∞³)
RAIZ_TRES = math.sqrt(3)  # √3 - Root of trinity
FRECUENCIA_PI_HZ = 141.70001  # Hz - The living π frequency
PI_VIVO = math.pi  # π - The living constant
