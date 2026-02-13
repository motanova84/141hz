#!/usr/bin/env python3
"""
Master Lagrangian for QCAL ∞³
=============================

L[Ψ,Φ] = 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²) - V_eff(Ψ,Φ) + κ_Π · R_CY

This module implements the complete Master Lagrangian integrating:
1. Consciousness field dynamics (Ψ)
2. Informational geometry (Φ)
3. Living Calabi-Yau structure coupling (κ_Π · R_CY)

Components:
-----------
1. **Kinetic Term**: 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²)
   - Standard Klein-Gordon kinetic energy for scalar field Ψ
   - Relativistic wave equation form

2. **Effective Potential**: V_eff(Ψ,Φ)
   - Couples consciousness field Ψ to informational geometry Φ
   - Includes self-interaction and geometry-induced terms
   - V_eff = V₀|Ψ|² + ξ₁ Φ|Ψ|² + ξ₂ |Ψ|⁴

3. **Calabi-Yau Coupling**: κ_Π · R_CY
   - κ_Π ≈ 2.5773 (fundamental coupling constant)
   - R_CY: mean curvature of living Calabi-Yau fiber bundle
   - Provides geometric forcing at f₀ = 141.7001 Hz

Testable Predictions:
--------------------
1. Soliton solutions with stability conditions
2. Spectral analysis peaks at f₀ = 141.7001 Hz
3. EEG resonance patterns
4. Gravitational wave coupling signatures

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass
import mpmath as mp

# Import QCAL modules
try:
    from qcal.constants import F0_HZ, KAPPA_PI, C, HBAR, H_PLANCK
except ImportError:
    # Fallback constants
    F0_HZ = 141.7001
    KAPPA_PI = 2.5773
    C = 299792458.0
    HBAR = 1.054571817e-34
    H_PLANCK = 6.62607015e-34

try:
    from .calabi_yau_curvature import CalabiYauCurvature, create_calabi_yau_curvature
except ImportError:
    from calabi_yau_curvature import CalabiYauCurvature, create_calabi_yau_curvature

# Set precision
mp.dps = 50


@dataclass
class MasterLagrangianParameters:
    """
    Parameters for the Master Lagrangian.
    
    Attributes
    ----------
    c : float
        Speed of light (m/s)
    hbar : float
        Reduced Planck constant (J·s)
    kappa_pi : float
        Calabi-Yau coupling constant (dimensionless)
    V0 : float
        Potential energy scale (J/m³)
    xi1 : float
        Geometry-field coupling strength (dimensionless)
    xi2 : float
        Self-interaction coupling (dimensionless)
    f0 : float
        Fundamental frequency (Hz)
    """
    c: float = C
    hbar: float = HBAR
    kappa_pi: float = KAPPA_PI
    V0: float = H_PLANCK * F0_HZ  # Energy scale from f₀
    xi1: float = 1.0  # Geometry coupling
    xi2: float = 0.1  # Self-interaction
    f0: float = F0_HZ


@dataclass
class FieldConfiguration:
    """
    Field and geometry configuration for Master Lagrangian.
    
    Attributes
    ----------
    Psi : complex
        Consciousness field value Ψ
    dPsi_dt : complex
        Time derivative ∂Ψ/∂t
    nabla_Psi : np.ndarray
        Spatial gradient ∇Ψ (3-component)
    Phi : float
        Informational geometry field Φ
    nabla_Phi : np.ndarray
        Spatial gradient of Φ
    R_CY : float
        Calabi-Yau curvature R_CY(t)
    t : float
        Time coordinate (s)
    x : np.ndarray
        Spatial coordinates (m)
    """
    Psi: complex
    dPsi_dt: complex
    nabla_Psi: np.ndarray
    Phi: float
    nabla_Phi: np.ndarray
    R_CY: float
    t: float
    x: np.ndarray


# ============================================================================
# LAGRANGIAN COMPONENTS
# ============================================================================

def kinetic_term(
    dPsi_dt: complex,
    nabla_Psi: np.ndarray,
    c: float = C
) -> float:
    """
    Compute kinetic term: 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²).
    
    This is the standard relativistic kinetic energy for a scalar field.
    
    Parameters
    ----------
    dPsi_dt : complex
        Time derivative ∂Ψ/∂t
    nabla_Psi : np.ndarray
        Spatial gradient ∇Ψ (3-component)
    c : float
        Speed of light (m/s)
    
    Returns
    -------
    float
        Kinetic energy density (J/m³)
    """
    # |∂Ψ/∂t|²
    time_term = abs(dPsi_dt) ** 2
    
    # |∇Ψ|² = |∇_x Ψ|² + |∇_y Ψ|² + |∇_z Ψ|²
    space_term = np.sum(np.abs(nabla_Psi) ** 2)
    
    # Kinetic term
    L_kin = 0.5 * (time_term - c**2 * space_term)
    
    return L_kin


def effective_potential(
    Psi: complex,
    Phi: float,
    V0: float,
    xi1: float,
    xi2: float
) -> float:
    """
    Compute effective potential: V_eff(Ψ,Φ).
    
    V_eff = V₀|Ψ|² + ξ₁ Φ|Ψ|² + ξ₂ |Ψ|⁴
    
    Components:
    - V₀|Ψ|²: Mass term / harmonic potential
    - ξ₁ Φ|Ψ|²: Coupling between consciousness field and geometry
    - ξ₂ |Ψ|⁴: Self-interaction (quartic term)
    
    Parameters
    ----------
    Psi : complex
        Consciousness field value
    Phi : float
        Informational geometry field
    V0 : float
        Potential energy scale (J/m³)
    xi1 : float
        Geometry-field coupling
    xi2 : float
        Self-interaction coupling
    
    Returns
    -------
    float
        Effective potential energy density (J/m³)
    """
    Psi_squared = abs(Psi) ** 2
    Psi_fourth = Psi_squared ** 2
    
    # Three components
    V_mass = V0 * Psi_squared
    V_coupling = xi1 * Phi * Psi_squared
    V_self = xi2 * Psi_fourth
    
    V_eff = V_mass + V_coupling + V_self
    
    return V_eff


def calabi_yau_coupling(
    R_CY: float,
    kappa_pi: float = KAPPA_PI
) -> float:
    """
    Compute Calabi-Yau curvature coupling: κ_Π · R_CY.
    
    This term couples the consciousness field to the living Calabi-Yau
    geometry, providing geometric forcing at f₀ = 141.7001 Hz.
    
    Parameters
    ----------
    R_CY : float
        Calabi-Yau mean curvature (m⁻²)
    kappa_pi : float
        Coupling constant κ_Π ≈ 2.5773
    
    Returns
    -------
    float
        Calabi-Yau coupling term (m⁻²)
    """
    return kappa_pi * R_CY


def master_lagrangian(
    config: FieldConfiguration,
    params: MasterLagrangianParameters
) -> float:
    """
    Compute total Master Lagrangian density.
    
    L[Ψ,Φ] = L_kin - V_eff + L_CY
           = 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²) - V_eff(Ψ,Φ) + κ_Π · R_CY
    
    Parameters
    ----------
    config : FieldConfiguration
        Field and geometry configuration
    params : MasterLagrangianParameters
        Physical parameters
    
    Returns
    -------
    float
        Total Lagrangian density (J/m³)
    """
    # Kinetic term
    L_kin = kinetic_term(config.dPsi_dt, config.nabla_Psi, params.c)
    
    # Effective potential (negative sign in Lagrangian)
    V_eff = effective_potential(
        config.Psi, config.Phi, params.V0, params.xi1, params.xi2
    )
    
    # Calabi-Yau coupling
    L_CY = calabi_yau_coupling(config.R_CY, params.kappa_pi)
    
    # Total Lagrangian
    L_total = L_kin - V_eff + L_CY
    
    return L_total


# ============================================================================
# ACTION FUNCTIONAL
# ============================================================================

def action_functional(
    field_history: list,
    params: MasterLagrangianParameters,
    dx: float,
    dt: float
) -> float:
    """
    Compute action integral S = ∫ d⁴x L[Ψ,Φ].
    
    Parameters
    ----------
    field_history : list of FieldConfiguration
        Time evolution of fields
    params : MasterLagrangianParameters
        Physical parameters
    dx : float
        Spatial discretization (m)
    dt : float
        Time discretization (s)
    
    Returns
    -------
    float
        Total action S (J·s)
    """
    action = 0.0
    d4x = dx**3 * dt  # Spacetime volume element
    
    for config in field_history:
        L = master_lagrangian(config, params)
        action += L * d4x
    
    return action


# ============================================================================
# EQUATIONS OF MOTION
# ============================================================================

def equation_of_motion_psi(
    config: FieldConfiguration,
    params: MasterLagrangianParameters,
    d2Psi_dt2: complex,
    laplacian_Psi: complex
) -> complex:
    """
    Equation of motion for Ψ from δS/δΨ = 0.
    
    Derived from variational principle:
    ∂²Ψ/∂t² - c²∇²Ψ + ∂V_eff/∂Ψ* = 0
    
    Where:
    ∂V_eff/∂Ψ* = V₀Ψ + ξ₁ΦΨ + 2ξ₂|Ψ|²Ψ
    
    Parameters
    ----------
    config : FieldConfiguration
        Current field configuration
    params : MasterLagrangianParameters
        Physical parameters
    d2Psi_dt2 : complex
        Second time derivative ∂²Ψ/∂t²
    laplacian_Psi : complex
        Laplacian ∇²Ψ
    
    Returns
    -------
    complex
        Left-hand side of equation (should be ≈0 for solutions)
    """
    # Kinetic part: ∂²Ψ/∂t² - c²∇²Ψ
    kinetic = d2Psi_dt2 - params.c**2 * laplacian_Psi
    
    # Potential derivative
    Psi_squared = abs(config.Psi) ** 2
    dV_dPsi = (
        params.V0 * config.Psi
        + params.xi1 * config.Phi * config.Psi
        + 2 * params.xi2 * Psi_squared * config.Psi
    )
    
    # Equation of motion: □Ψ + ∂V/∂Ψ* = 0
    eom = kinetic + dV_dPsi
    
    return eom


# ============================================================================
# SOLITON SOLUTIONS
# ============================================================================

def soliton_ansatz(
    x: np.ndarray,
    t: float,
    amplitude: float,
    width: float,
    velocity: float,
    f0: float = F0_HZ
) -> complex:
    """
    Soliton ansatz for Ψ field.
    
    Ψ(x,t) = A sech[(x - vt)/w] exp(i2πf₀t)
    
    Parameters
    ----------
    x : np.ndarray
        Spatial coordinates
    t : float
        Time
    amplitude : float
        Soliton amplitude A
    width : float
        Soliton width w
    velocity : float
        Soliton velocity v
    f0 : float
        Carrier frequency (default: 141.7001 Hz)
    
    Returns
    -------
    complex
        Soliton field value
    """
    # Center of soliton
    xi = (x[0] - velocity * t) / width
    
    # Soliton envelope
    envelope = amplitude / np.cosh(xi)
    
    # Phase oscillation at f₀
    phase = np.exp(1j * 2 * np.pi * f0 * t)
    
    return envelope * phase


def soliton_stability_criterion(
    params: MasterLagrangianParameters,
    curvature: CalabiYauCurvature
) -> Tuple[bool, float]:
    """
    Check soliton stability condition.
    
    For stable soliton solutions, we require:
    ω² = c²k² + m_eff²
    
    where m_eff² = V₀ - κ_Π⟨R_CY⟩
    
    Stability requires m_eff² > 0.
    
    Parameters
    ----------
    params : MasterLagrangianParameters
        Lagrangian parameters
    curvature : CalabiYauCurvature
        Calabi-Yau curvature object
    
    Returns
    -------
    is_stable : bool
        Whether soliton is stable
    m_eff_squared : float
        Effective mass squared (s⁻²)
    """
    # Time-averaged R_CY (static component)
    R_CY_avg = curvature.R_static
    
    # Effective mass squared
    m_eff_sq = params.V0 / params.hbar**2 - params.kappa_pi * R_CY_avg / params.hbar**2
    
    is_stable = m_eff_sq > 0
    
    return is_stable, m_eff_sq


# ============================================================================
# SPECTRAL ANALYSIS
# ============================================================================

def spectral_analysis_psi(
    Psi_history: np.ndarray,
    t_array: np.ndarray,
    expected_f0: float = F0_HZ
) -> Tuple[np.ndarray, np.ndarray, float, bool]:
    """
    Perform spectral analysis on Ψ field evolution.
    
    Verifies that Ψ oscillates at f₀ = 141.7001 Hz.
    
    Parameters
    ----------
    Psi_history : np.ndarray
        Time series of Ψ values
    t_array : np.ndarray
        Time array (s)
    expected_f0 : float
        Expected fundamental frequency (Hz)
    
    Returns
    -------
    frequencies : np.ndarray
        Frequency array (Hz)
    power_spectrum : np.ndarray
        Power spectral density
    peak_frequency : float
        Frequency of maximum power
    matches_f0 : bool
        Whether peak is within 0.01 Hz of f₀
    """
    # FFT
    fft_result = np.fft.fft(Psi_history)
    dt = t_array[1] - t_array[0]
    frequencies = np.fft.fftfreq(len(t_array), dt)
    
    # Power spectrum (positive frequencies only)
    positive_mask = frequencies > 0
    frequencies = frequencies[positive_mask]
    power_spectrum = np.abs(fft_result[positive_mask]) ** 2
    
    # Find peak
    peak_idx = np.argmax(power_spectrum)
    peak_frequency = frequencies[peak_idx]
    
    # Check if matches f₀
    matches_f0 = abs(peak_frequency - expected_f0) < 0.01
    
    return frequencies, power_spectrum, peak_frequency, matches_f0


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate Master Lagrangian formulation."""
    print("=" * 70)
    print("Master Lagrangian - QCAL ∞³")
    print("=" * 70)
    print()
    print("L[Ψ,Φ] = 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²) - V_eff(Ψ,Φ) + κ_Π · R_CY")
    print()
    
    # Create parameters
    params = MasterLagrangianParameters()
    
    print("Parameters:")
    print(f"  κ_Π = {params.kappa_pi}")
    print(f"  f₀ = {params.f0} Hz")
    print(f"  V₀ = {params.V0:.6e} J/m³")
    print(f"  ξ₁ = {params.xi1}")
    print(f"  ξ₂ = {params.xi2}")
    print()
    
    # Create Calabi-Yau curvature (Quintic)
    curvature = create_calabi_yau_curvature(h11=1, h21=101)
    
    print("Calabi-Yau (Quintic):")
    print(f"  h¹¹ = {curvature.h11}")
    print(f"  h²¹ = {curvature.h21}")
    print(f"  χ = {curvature.euler_characteristic}")
    print(f"  R_static = {curvature.R_static:.6e} m⁻²")
    print()
    
    # Test field configuration
    t = 0.0
    x = np.array([0.0, 0.0, 0.0])
    Psi = 1.0 + 0.0j
    dPsi_dt = 1j * 2 * np.pi * F0_HZ  # Oscillating at f₀
    nabla_Psi = np.array([0.0, 0.0, 0.0], dtype=complex)
    Phi = 1.0
    nabla_Phi = np.array([0.0, 0.0, 0.0])
    R_CY = curvature.R_CY(t)
    
    config = FieldConfiguration(
        Psi=Psi, dPsi_dt=dPsi_dt, nabla_Psi=nabla_Psi,
        Phi=Phi, nabla_Phi=nabla_Phi, R_CY=R_CY,
        t=t, x=x
    )
    
    # Compute Lagrangian
    L = master_lagrangian(config, params)
    
    print("Test Configuration (t=0):")
    print(f"  Ψ = {config.Psi}")
    print(f"  ∂Ψ/∂t = {config.dPsi_dt:.6e}")
    print(f"  Φ = {config.Phi}")
    print(f"  R_CY = {config.R_CY:.6e} m⁻²")
    print()
    print(f"Master Lagrangian: L = {L:.6e} J/m³")
    print()
    
    # Check soliton stability
    is_stable, m_eff_sq = soliton_stability_criterion(params, curvature)
    
    print("Soliton Stability:")
    print(f"  m_eff² = {m_eff_sq:.6e} s⁻²")
    print(f"  Stable: {is_stable}")
    print()
    
    print("=" * 70)
    print("✨ Master Lagrangian formulation complete - QCAL ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
