"""
╔════════════════════════════════════════════════════════════════════════════╗
║           Navier-Stokes QCAL Constants - Fluid Dynamics Parameters         ║
║         Fundamental constants for quantum coherent fluid analysis           ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math

# ═══════════════════════════════════════════════════════════════════════
# FUNDAMENTAL QCAL FREQUENCY
# ═══════════════════════════════════════════════════════════════════════

F0 = 141.7001  # Hz
OMEGA_0 = 2 * math.pi * F0  # rad/s
T0 = 1.0 / F0  # seconds

# ═══════════════════════════════════════════════════════════════════════
# MEDIUM-SPECIFIC AMPLITUDE CALIBRATIONS
# ═══════════════════════════════════════════════════════════════════════

A_VACIO = 8.9   # Satisfies both parabolic (γ > 0) and Riccati-Besov (Δ > 0)
A_AGUA = 7.0    # Satisfies Riccati-Besov (Δ > 0) - PRIMARY CONDITION
A_AIRE = 200.0  # Calibrated for air viscosity

# ═══════════════════════════════════════════════════════════════════════
# MEDIUM VISCOSITIES
# ═══════════════════════════════════════════════════════════════════════

NU_VACIO = 0.0      # No viscosity in vacuum
NU_AGUA = 1.0e-6    # Water kinematic viscosity (m²/s)
NU_AIRE = 1.5e-5    # Air kinematic viscosity (m²/s) at 20°C

# ═══════════════════════════════════════════════════════════════════════
# QFT COUPLING COEFFICIENTS (derived from Quantum Field Theory)
# ═══════════════════════════════════════════════════════════════════════

ALPHA_QFT = 0.1184   # Primary coupling
BETA_QFT = 0.382     # Secondary coupling ≈ 1/φ²
GAMMA_QFT = 0.577    # Tertiary coupling ≈ γ_Euler

# ═══════════════════════════════════════════════════════════════════════
# PARABOLIC AND RICCATI-BESOV CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

GAMMA_PARABOLIC = 0.1         # Parabolic condition (γ > 0)
DELTA_RICCATI_BESOV = ALPHA_QFT  # Riccati-Besov condition (Δ > 0)
