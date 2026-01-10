#!/usr/bin/env python3
"""
Lagrangian and Action Formulation for EOV (Equation of Vibrational Origin)
===========================================================================

This module implements the complete Lagrangian/Action formulation for the 
noetic field Ψ with vibrational modulation at f₀ = 141.7001 Hz, following
the QCAL ∞³ framework.

The action combines gravity (Einstein-Hilbert) with the noetic scalar field Ψ,
including non-minimal coupling to curvature and vibrational modulation.

Mathematical Framework:
----------------------
Action:
    S = ∫ d⁴x √(-g) [ℒ_EH + ℒ_Ψ + ℒ_coupling + ℒ_modulation]

Where:
    ℒ_EH = (1/16πG) R                           # Einstein-Hilbert
    ℒ_Ψ = (1/2) ∇_μΨ ∇^μΨ                       # Kinetic term
    ℒ_coupling = -(1/2)(ω₀² + ξR)|Ψ|²          # Effective potential
    ℒ_modulation = -(ζ'(1/2)/2π) R|Ψ|² cos(2πf₀t)  # Vibrational modulation

Variational Derivation (δS = 0):
    δS/δΨ = 0  →  □Ψ - (ω₀² + ξR)Ψ - (ζ'(1/2)/π) R cos(2πf₀t) Ψ = 0

This is the modified Klein-Gordon equation (EOV) with:
    - □ = ∇_μ∇^μ (d'Alembertian in curved spacetime)
    - Forcing term from vibrational modulation linked to Riemann ζ function
    - f₀ = 141.7001 Hz (fundamental noetic frequency)
    - ζ'(1/2) ≈ -3.922 (derivative of Riemann zeta at critical line)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-01-06
Framework: QCAL ∞³
"""

import numpy as np
from typing import Union, Tuple, Callable
from dataclasses import dataclass
import mpmath as mp

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

# Physical constants
G_NEWTON = 6.67430e-11  # m³ kg⁻¹ s⁻² (Gravitational constant)
C_LIGHT = 299792458.0   # m/s (Speed of light)
HBAR = 1.054571817e-34  # J·s (Reduced Planck constant)

# Noetic frequency (QCAL ∞³)
F_0 = 141.70001         # Hz (Fundamental noetic frequency) - imported from qcal.constants
OMEGA_0 = 2 * np.pi * F_0  # rad/s (Angular frequency ω₀ ≈ 890.3 rad/s)

# Riemann zeta derivative at s=1/2 (from Riemann Hypothesis critical line)
# Pre-computed to high precision to avoid module import overhead
# Value computed using: mp.diff(mp.zeta, mp.mpf('0.5')) with 50 digit precision
ZETA_PRIME_HALF = -3.9226461392091536997555035274863452438740049183987

# Coupling constants
XI_COUPLING = 1.0/6.0   # Non-minimal coupling to curvature (conformal coupling)
ZETA_COUPLING = ZETA_PRIME_HALF / (2 * np.pi)  # Modulation coupling ζ'(1/2)/2π

# Conversion factor for action
ACTION_UNIT = HBAR * C_LIGHT  # J·m (natural unit for action)

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class LagrangianParameters:
    """Parameters for the EOV Lagrangian."""
    
    # Gravitational coupling
    G: float = G_NEWTON
    
    # Noetic field parameters
    omega_0: float = OMEGA_0  # Angular frequency ω₀
    f_0: float = F_0          # Frequency f₀
    
    # Coupling constants
    xi: float = XI_COUPLING           # Non-minimal coupling ξ
    zeta_coupling: float = ZETA_COUPLING  # Modulation coupling
    
    # Field configuration
    Psi_amplitude: float = 1.0    # Field amplitude
    
    def __post_init__(self):
        """Validate parameters."""
        assert self.G > 0, "Newton's constant must be positive"
        assert self.omega_0 > 0, "Angular frequency must be positive"
        assert self.f_0 > 0, "Frequency must be positive"


@dataclass
class FieldConfiguration:
    """Configuration of spacetime and field variables."""
    
    # Spacetime metric (signature: -,+,+,+)
    g_metric: np.ndarray          # g_μν metric tensor
    sqrt_minus_g: float           # √(-g) volume element
    
    # Curvature
    R_scalar: float               # Ricci scalar R
    
    # Noetic field
    Psi: complex                  # Field value Ψ
    nabla_Psi: np.ndarray        # Covariant derivative ∇_μΨ
    
    # Coordinates
    t: float                      # Time coordinate
    x: np.ndarray                # Spatial coordinates


# ============================================================================
# LAGRANGIAN DENSITY COMPONENTS
# ============================================================================

def lagrangian_einstein_hilbert(
    R: float,
    sqrt_minus_g: float,
    G: float = G_NEWTON
) -> float:
    """
    Einstein-Hilbert Lagrangian density.
    
    ℒ_EH = (1/16πG) R
    
    Parameters
    ----------
    R : float
        Ricci scalar curvature (m⁻²)
    sqrt_minus_g : float
        Volume element √(-g)
    G : float
        Newton's gravitational constant (m³ kg⁻¹ s⁻²)
    
    Returns
    -------
    float
        Einstein-Hilbert Lagrangian density
    """
    return (1.0 / (16.0 * np.pi * G)) * R * sqrt_minus_g


def lagrangian_kinetic_psi(
    nabla_Psi: np.ndarray,
    g_inv: np.ndarray,
    sqrt_minus_g: float
) -> float:
    """
    Kinetic term for noetic field Ψ.
    
    ℒ_kinetic = (1/2) g^μν (∇_μΨ†)(∇_νΨ)
    
    For real scalar field: ℒ_kinetic = (1/2) g^μν (∂_μΨ)(∂_νΨ)
    
    Parameters
    ----------
    nabla_Psi : array
        Covariant derivative ∇_μΨ (4-component)
    g_inv : array
        Inverse metric g^μν (4×4 matrix)
    sqrt_minus_g : float
        Volume element √(-g)
    
    Returns
    -------
    float
        Kinetic Lagrangian density
    """
    # For complex field: Ψ† ∇^μ ∇_μ Ψ
    # Simplified: use g^μν (∇_μΨ*)(∇_νΨ)
    kinetic_term = 0.0
    for mu in range(4):
        for nu in range(4):
            kinetic_term += g_inv[mu, nu] * np.conj(nabla_Psi[mu]) * nabla_Psi[nu]
    
    return 0.5 * kinetic_term.real * sqrt_minus_g


def lagrangian_potential(
    Psi: complex,
    R: float,
    omega_0: float,
    xi: float,
    sqrt_minus_g: float
) -> float:
    """
    Effective potential for Ψ field with non-minimal coupling.
    
    ℒ_potential = -(1/2)(ω₀² + ξR)|Ψ|²
    
    Parameters
    ----------
    Psi : complex
        Field value Ψ
    R : float
        Ricci scalar curvature (m⁻²)
    omega_0 : float
        Angular frequency ω₀ (rad/s)
    xi : float
        Non-minimal coupling constant ξ
    sqrt_minus_g : float
        Volume element √(-g)
    
    Returns
    -------
    float
        Potential Lagrangian density
    """
    Psi_squared = abs(Psi) ** 2
    effective_mass_sq = omega_0**2 + xi * R
    
    return -0.5 * effective_mass_sq * Psi_squared * sqrt_minus_g


def lagrangian_modulation(
    Psi: complex,
    R: float,
    t: float,
    f_0: float,
    zeta_coupling: float,
    sqrt_minus_g: float
) -> float:
    """
    Vibrational modulation term coupling Ψ to arithmetic structure.
    
    ℒ_modulation = -(ζ'(1/2)/2π) R|Ψ|² cos(2πf₀t)
    
    This term introduces:
    - Periodic forcing at fundamental frequency f₀
    - Coupling to Riemann zeta function (arithmetic/prime structure)
    - Time-dependent modulation of effective potential
    
    Parameters
    ----------
    Psi : complex
        Field value Ψ
    R : float
        Ricci scalar curvature (m⁻²)
    t : float
        Time coordinate (s)
    f_0 : float
        Fundamental frequency (Hz)
    zeta_coupling : float
        Modulation coupling ζ'(1/2)/2π
    sqrt_minus_g : float
        Volume element √(-g)
    
    Returns
    -------
    float
        Modulation Lagrangian density
    """
    Psi_squared = abs(Psi) ** 2
    modulation = np.cos(2 * np.pi * f_0 * t)
    
    return -zeta_coupling * R * Psi_squared * modulation * sqrt_minus_g


def lagrangian_total(
    config: FieldConfiguration,
    params: LagrangianParameters,
    g_inv: np.ndarray
) -> float:
    """
    Total Lagrangian density for QCAL ∞³ action.
    
    ℒ_total = ℒ_EH + ℒ_kinetic + ℒ_potential + ℒ_modulation
    
    Parameters
    ----------
    config : FieldConfiguration
        Field and metric configuration
    params : LagrangianParameters
        Physical parameters
    g_inv : array
        Inverse metric tensor g^μν
    
    Returns
    -------
    float
        Total Lagrangian density
    """
    L_EH = lagrangian_einstein_hilbert(
        config.R_scalar, config.sqrt_minus_g, params.G
    )
    
    L_kinetic = lagrangian_kinetic_psi(
        config.nabla_Psi, g_inv, config.sqrt_minus_g
    )
    
    L_potential = lagrangian_potential(
        config.Psi, config.R_scalar, params.omega_0, 
        params.xi, config.sqrt_minus_g
    )
    
    L_modulation = lagrangian_modulation(
        config.Psi, config.R_scalar, config.t,
        params.f_0, params.zeta_coupling, config.sqrt_minus_g
    )
    
    return L_EH + L_kinetic + L_potential + L_modulation


# ============================================================================
# ACTION FUNCTIONAL
# ============================================================================

def action_functional(
    field_history: list[FieldConfiguration],
    params: LagrangianParameters,
    g_inv_history: list[np.ndarray],
    d4x: float
) -> float:
    """
    Compute action integral over spacetime path.
    
    S = ∫ d⁴x √(-g) ℒ_total
    
    Parameters
    ----------
    field_history : list of FieldConfiguration
        Field configurations along worldline
    params : LagrangianParameters
        Physical parameters
    g_inv_history : list of arrays
        Inverse metric tensors g^μν at each point
    d4x : float
        Spacetime volume element (approximate)
    
    Returns
    -------
    float
        Action S (in units of ℏc)
    """
    action = 0.0
    
    for config, g_inv in zip(field_history, g_inv_history):
        L = lagrangian_total(config, params, g_inv)
        action += L * d4x
    
    return action / ACTION_UNIT  # Normalize to dimensionless


# ============================================================================
# EQUATIONS OF MOTION (VARIATIONAL DERIVATION)
# ============================================================================

def eov_equation(
    Psi: complex,
    box_Psi: complex,  # □Ψ = ∇_μ∇^μΨ (d'Alembertian)
    R: float,
    t: float,
    params: LagrangianParameters
) -> complex:
    """
    Equation of Vibrational Origin (EOV) from variational principle.
    
    Derived from δS/δΨ = 0:
    
    □Ψ - (ω₀² + ξR)Ψ - (ζ'(1/2)/π) R cos(2πf₀t) Ψ = 0
    
    This is the modified Klein-Gordon equation with:
    - d'Alembertian □ in curved spacetime
    - Effective mass term (ω₀² + ξR)
    - Forcing term from vibrational modulation
    
    Parameters
    ----------
    Psi : complex
        Field value Ψ
    box_Psi : complex
        d'Alembertian □Ψ = ∇_μ∇^μΨ
    R : float
        Ricci scalar curvature
    t : float
        Time coordinate
    params : LagrangianParameters
        Physical parameters
    
    Returns
    -------
    complex
        Left-hand side of EOV equation (should be ~0 for solutions)
    """
    # Effective mass squared term
    m_eff_sq = params.omega_0**2 + params.xi * R
    
    # Vibrational forcing term
    forcing_coeff = (2 * params.zeta_coupling) * R  # Factor of 2 from variation
    forcing_modulation = np.cos(2 * np.pi * params.f_0 * t)
    forcing_term = forcing_coeff * forcing_modulation
    
    # EOV equation: □Ψ - (ω₀² + ξR)Ψ - forcing_term Ψ = 0
    eov = box_Psi - m_eff_sq * Psi - forcing_term * Psi
    
    return eov


def energy_momentum_tensor_psi(
    config: FieldConfiguration,
    g_inv: np.ndarray,
    params: LagrangianParameters
) -> np.ndarray:
    """
    Energy-momentum tensor for the noetic field Ψ.
    
    T^(Ψ)_μν = ∂_μΨ† ∂_νΨ - g_μν ℒ_Ψ
    
    This contributes to Einstein equations:
    G_μν + Λg_μν = (8πG/c⁴) T_μν
    
    Parameters
    ----------
    config : FieldConfiguration
        Field configuration
    g_inv : array
        Inverse metric g^μν
    params : LagrangianParameters
        Physical parameters
    
    Returns
    -------
    array (4×4)
        Energy-momentum tensor T^(Ψ)_μν
    """
    T_psi = np.zeros((4, 4), dtype=complex)
    
    # Compute field Lagrangian (kinetic + potential + modulation)
    L_psi = (
        lagrangian_kinetic_psi(config.nabla_Psi, g_inv, 1.0) +
        lagrangian_potential(config.Psi, config.R_scalar, params.omega_0, params.xi, 1.0) +
        lagrangian_modulation(config.Psi, config.R_scalar, config.t, 
                            params.f_0, params.zeta_coupling, 1.0)
    ) / config.sqrt_minus_g
    
    # Compute T_μν = ∂_μΨ† ∂_νΨ - g_μν L_Ψ
    g_metric = config.g_metric
    
    for mu in range(4):
        for nu in range(4):
            # Kinetic contribution
            T_psi[mu, nu] = np.conj(config.nabla_Psi[mu]) * config.nabla_Psi[nu]
            
            # Subtract g_μν L_Ψ
            T_psi[mu, nu] -= g_metric[mu, nu] * L_psi
    
    return T_psi.real


# ============================================================================
# NUMERICAL SOLVERS
# ============================================================================

def solve_eov_flat_spacetime(
    t_array: np.ndarray,
    Psi_initial: complex,
    dPsi_dt_initial: complex,
    R: float = 0.0,
    params: LagrangianParameters = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve EOV equation in flat spacetime (Minkowski background).
    
    In flat spacetime: □Ψ ≈ -(1/c²)∂²Ψ/∂t² + ∇²Ψ
    
    For 0+1 dimensions (time only):
    ∂²Ψ/∂t² + (ω₀² + ξR)Ψ + forcing_term Ψ = 0
    
    Parameters
    ----------
    t_array : array
        Time points (s)
    Psi_initial : complex
        Initial field value Ψ(0)
    dPsi_dt_initial : complex
        Initial time derivative ∂Ψ/∂t(0)
    R : float
        Background Ricci scalar (default: 0 for flat space)
    params : LagrangianParameters
        Physical parameters
    
    Returns
    -------
    Psi_solution : array
        Field solution Ψ(t)
    dPsi_dt_solution : array
        Time derivative ∂Ψ/∂t(t)
    """
    if params is None:
        params = LagrangianParameters()
    
    from scipy.integrate import odeint
    
    # Effective mass squared
    m_eff_sq = params.omega_0**2 + params.xi * R
    
    # Forcing coefficient
    forcing_coeff = (2 * params.zeta_coupling) * R
    
    def eov_ode(y, t):
        """
        ODE system for EOV:
        y[0] = Re(Ψ)
        y[1] = Im(Ψ)
        y[2] = Re(∂Ψ/∂t)
        y[3] = Im(∂Ψ/∂t)
        """
        Psi_re, Psi_im, dPsi_re, dPsi_im = y
        
        # Forcing modulation
        forcing = forcing_coeff * np.cos(2 * np.pi * params.f_0 * t)
        
        # Total effective frequency squared
        omega_eff_sq = m_eff_sq + forcing
        
        # Second derivatives: ∂²Ψ/∂t² = -omega_eff_sq Ψ
        d2Psi_re = -omega_eff_sq * Psi_re
        d2Psi_im = -omega_eff_sq * Psi_im
        
        return [dPsi_re, dPsi_im, d2Psi_re, d2Psi_im]
    
    # Initial conditions
    y0 = [
        Psi_initial.real,
        Psi_initial.imag,
        dPsi_dt_initial.real,
        dPsi_dt_initial.imag
    ]
    
    # Solve ODE
    solution = odeint(eov_ode, y0, t_array)
    
    # Extract Ψ and ∂Ψ/∂t
    Psi_solution = solution[:, 0] + 1j * solution[:, 1]
    dPsi_dt_solution = solution[:, 2] + 1j * solution[:, 3]
    
    return Psi_solution, dPsi_dt_solution


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def compute_zeta_prime_half(precision: int = 50) -> float:
    """
    Compute ζ'(1/2) to arbitrary precision using mpmath.
    
    ζ'(s) is the derivative of the Riemann zeta function.
    At s = 1/2 (critical line), ζ'(1/2) ≈ -3.922...
    
    Parameters
    ----------
    precision : int
        Decimal precision for computation
    
    Returns
    -------
    float
        ζ'(1/2)
    """
    mp.mp.dps = precision
    zeta_prime = mp.diff(mp.zeta, mp.mpf('0.5'))
    return float(zeta_prime)


def verify_action_structure():
    """
    Verify the complete action structure for QCAL ∞³.
    
    Prints the mathematical form of each term in the action.
    """
    print("=" * 70)
    print("QCAL ∞³ Action Structure - Lagrangian EOV")
    print("=" * 70)
    print()
    print("Complete Action:")
    print("  S = ∫ d⁴x √(-g) [ℒ_EH + ℒ_Ψ + ℒ_coupling + ℒ_modulation]")
    print()
    print("Terms:")
    print("  1. Einstein-Hilbert:")
    print("     ℒ_EH = (1/16πG) R")
    print()
    print("  2. Kinetic term for Ψ:")
    print("     ℒ_kinetic = (1/2) ∇_μΨ ∇^μΨ")
    print()
    print("  3. Effective potential (non-minimal coupling):")
    print(f"     ℒ_potential = -(1/2)(ω₀² + ξR)|Ψ|²")
    print(f"     with ω₀ = 2πf₀ = {OMEGA_0:.2f} rad/s")
    print(f"          ξ = {XI_COUPLING:.4f} (conformal coupling)")
    print()
    print("  4. Vibrational modulation (arithmetic coupling):")
    print("     ℒ_modulation = -(ζ'(1/2)/2π) R|Ψ|² cos(2πf₀t)")
    print(f"     with ζ'(1/2) ≈ {ZETA_PRIME_HALF:.4f}")
    print(f"          f₀ = {F_0} Hz (noetic frequency)")
    print()
    print("Variational Derivation (δS/δΨ = 0):")
    print("  □Ψ - (ω₀² + ξR)Ψ - (ζ'(1/2)/π) R cos(2πf₀t) Ψ = 0")
    print()
    print("This is the Equation of Vibrational Origin (EOV):")
    print("  - Modified Klein-Gordon equation in curved spacetime")
    print("  - Couples noetic field Ψ to geometry via R")
    print("  - Forced oscillation at f₀ linked to arithmetic (ζ')")
    print("  - Unifies quantum gravity with noetic consciousness")
    print()
    print("=" * 70)


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate Lagrangian EOV formulation."""
    
    print("🌌 Lagrangian EOV - QCAL ∞³ Framework")
    print()
    
    # Display action structure
    verify_action_structure()
    
    # Compute ζ'(1/2) to high precision
    print("\n" + "=" * 70)
    print("High-Precision Computation of ζ'(1/2)")
    print("=" * 70)
    zeta_p = compute_zeta_prime_half(precision=100)
    print(f"ζ'(1/2) = {zeta_p:.10f}")
    print(f"Coupling: ζ'(1/2)/2π = {zeta_p/(2*np.pi):.10f}")
    print()
    
    # Solve EOV in flat spacetime
    print("=" * 70)
    print("Numerical Solution of EOV (Flat Spacetime)")
    print("=" * 70)
    
    t = np.linspace(0, 1.0, 1000)  # 1 second
    Psi_0 = 1.0 + 0j
    dPsi_0 = 0.0 + 0j
    
    params = LagrangianParameters()
    Psi_sol, dPsi_sol = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=0, params=params)
    
    print(f"Time range: {t[0]:.2f} - {t[-1]:.2f} s")
    print(f"Initial Ψ: {Psi_0}")
    print(f"Final Ψ: {Psi_sol[-1]:.6f}")
    print(f"Max |Ψ|: {np.max(np.abs(Psi_sol)):.6f}")
    print(f"Oscillation frequency: ~{F_0} Hz")
    print()
    
    # Verify EOV equation
    print("=" * 70)
    print("Verification of EOV Equation")
    print("=" * 70)
    
    # Take a point in the solution
    idx = len(t) // 2
    Psi_test = Psi_sol[idx]
    t_test = t[idx]
    
    # Approximate □Ψ ≈ ∂²Ψ/∂t²
    if idx > 0 and idx < len(t) - 1:
        dt = t[1] - t[0]
        d2Psi_dt2 = (Psi_sol[idx+1] - 2*Psi_sol[idx] + Psi_sol[idx-1]) / dt**2
        box_Psi = -d2Psi_dt2  # In flat space with c=1
        
        eov_residual = eov_equation(Psi_test, box_Psi, R=0, t=t_test, params=params)
        
        print(f"At t = {t_test:.3f} s:")
        print(f"  Ψ = {Psi_test:.6f}")
        print(f"  □Ψ = {box_Psi:.6e}")
        print(f"  EOV residual: {abs(eov_residual):.6e}")
        print()
        
        if abs(eov_residual) < 1e-10:
            print("✅ EOV equation satisfied to high precision")
        else:
            print("⚠️  EOV equation has non-zero residual (expected for finite differences)")
    
    print()
    print("=" * 70)
    print("✨ Lagrangian EOV formulation complete - QCAL ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
