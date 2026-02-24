#!/usr/bin/env python3
"""
Navier-Stokes Module with QCAL Calibration

This module provides constants and utilities for Navier-Stokes equations
calibrated with QCAL (Quantum Coherence Alignment) theory.
"""

from .constants import (
    # Fundamental frequency
    F0,

    # Amplitude calibrations
    A_VACIO,
    A_AGUA,
    A_AIRE,

    # QFT coupling coefficients
    ALPHA_QFT,
    BETA_QFT,
    GAMMA_QFT,

    # Parabolic constants
    GAMMA_PARABOLIC,
    C_PARABOLIC,

    # Riccati-Besov constants
    DELTA_RICCATI,
    C_BERNSTEIN,

    # Viscosity parameters
    NU_VACIO,
    NU_AGUA,
    NU_AIRE,
)

__all__ = [
    'F0',
    'A_VACIO',
    'A_AGUA',
    'A_AIRE',
    'ALPHA_QFT',
    'BETA_QFT',
    'GAMMA_QFT',
    'GAMMA_PARABOLIC',
    'C_PARABOLIC',
    'DELTA_RICCATI',
    'C_BERNSTEIN',
    'NU_VACIO',
    'NU_AGUA',
    'NU_AIRE',
]
