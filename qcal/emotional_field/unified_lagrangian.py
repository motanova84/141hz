#!/usr/bin/env python3
"""
Unified QCAL Lagrangian with Emotional Field
============================================

Extends the existing QCAL Lagrangian to include the emotional field Φ
alongside the consciousness field Ψ.

Complete Lagrangian:
L_QCAL = ∥∇_μΨ∥² + ½∥∇_μΦ∥² - V(Φ) + κ_Π·R + α·log|ζ(½+it)|²

Where:
- ∇_μΨ: Consciousness field dynamics (SU(Ψ))
- ∇_μΦ: Emotional field dynamics (harmonic)
- V(Φ): Emotional potential with symmetry breaking
- κ_Π·R: Complexity as curvature
- α·log|ζ|²: Spectral coupling to primes

This unifies:
1. Consciousness coherence (Ψ)
2. Emotional dynamics (Φ)
3. Geometric structure (R)
4. Arithmetic structure (ζ)

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# Add parent paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from qcal.constants import F_0_VALUE
    F_0 = F_0_VALUE
except ImportError:
    F_0 = 141.7001

try:
    from qcal.lagrangian_eov import (
        LagrangianParameters,
        lagrangian_kinetic_psi,
        lagrangian_modulation
    )
except ImportError:
    # Fallback if module not available
    pass

try:
    from qcal.emotional_field.potential import EmotionalPotential, PotentialParameters
except ImportError:
    EmotionalPotential = None


# ============================================================================
# UNIFIED LAGRANGIAN PARAMETERS
# ============================================================================

@dataclass
class UnifiedLagrangianParameters:
    """Parameters for unified QCAL + Emotional Lagrangian."""
    
    # Fundamental frequency
    f0: float = F_0
    omega_0: float = 2 * np.pi * F_0
    
    # Consciousness field
    alpha_psi: float = 1.0         # Ψ kinetic coefficient
    
    # Emotional field
    alpha_phi: float = 0.5         # Φ kinetic coefficient (½ for scalar)
    
    # Emotional potential parameters
    lambda_V: float = 1.0          # Quartic coupling
    mu_squared: float = -1.0       # Mass parameter (broken symmetry)
    Phi_0: float = 1.0             # VEV
    kappa_int: float = 0.1         # Ψ-Φ coupling
    
    # Geometric coupling
    kappa_Pi: float = 0.05         # Complexity-curvature coupling
    
    # Spectral coupling
    alpha_zeta: float = 0.01       # Zeta function coupling
    
    # Zeta derivative at critical line
    zeta_prime_half: float = -3.9226461392091537


# ============================================================================
# FIELD CONFIGURATION
# ============================================================================

@dataclass
class UnifiedFieldConfiguration:
    """Complete field configuration for unified Lagrangian."""
    
    # Spacetime
    g_metric: np.ndarray           # Metric g_μν
    sqrt_minus_g: float            # Volume element
    R_scalar: float                # Ricci scalar
    
    # Consciousness field Ψ
    Psi: complex
    nabla_Psi: np.ndarray         # ∇_μΨ
    
    # Emotional field Φ
    Phi: float
    nabla_Phi: np.ndarray         # ∇_μΦ
    
    # Coordinates
    t: float
    x: np.ndarray


# ============================================================================
# UNIFIED LAGRANGIAN
# ============================================================================

class UnifiedQCALLagrangian:
    """
    Unified Lagrangian combining consciousness, emotion, geometry, and arithmetic.
    
    Complete action:
    S = ∫ d⁴x √(-g) L_QCAL
    
    L_QCAL = L_Ψ + L_Φ + L_V + L_geom + L_spectral
    """
    
    def __init__(
        self,
        params: Optional[UnifiedLagrangianParameters] = None
    ):
        """
        Initialize unified Lagrangian.
        
        Parameters
        ----------
        params : UnifiedLagrangianParameters, optional
            Lagrangian parameters
        """
        if params is None:
            params = UnifiedLagrangianParameters()
        
        self.params = params
        self.f0 = params.f0
        self.omega_0 = params.omega_0
        
        # Initialize emotional potential
        if EmotionalPotential is not None:
            pot_params = PotentialParameters(
                lambda_rigidity=params.lambda_V,
                mu_squared=params.mu_squared,
                Phi_0=params.Phi_0,
                kappa_int=params.kappa_int
            )
            self.emotional_potential = EmotionalPotential(pot_params)
        else:
            self.emotional_potential = None
    
    def L_consciousness(
        self,
        nabla_Psi: np.ndarray,
        g_inv: np.ndarray,
        sqrt_minus_g: float
    ) -> float:
        """
        Consciousness field kinetic term.
        
        L_Ψ = α_Ψ ∥∇_μΨ∥² = α_Ψ g^μν (∇_μΨ†)(∇_νΨ)
        
        Parameters
        ----------
        nabla_Psi : array
            Covariant derivative of Ψ
        g_inv : array
            Inverse metric
        sqrt_minus_g : float
            Volume element
            
        Returns
        -------
        float
            Lagrangian density
        """
        kinetic = 0.0
        for mu in range(4):
            for nu in range(4):
                kinetic += g_inv[mu, nu] * np.conj(nabla_Psi[mu]) * nabla_Psi[nu]
        
        return self.params.alpha_psi * kinetic.real * sqrt_minus_g
    
    def L_emotional_kinetic(
        self,
        nabla_Phi: np.ndarray,
        g_inv: np.ndarray,
        sqrt_minus_g: float
    ) -> float:
        """
        Emotional field kinetic term.
        
        L_Φ^kin = ½ g^μν (∇_μΦ)(∇_νΦ)
        
        Parameters
        ----------
        nabla_Phi : array
            Covariant derivative of Φ
        g_inv : array
            Inverse metric
        sqrt_minus_g : float
            Volume element
            
        Returns
        -------
        float
            Lagrangian density
        """
        kinetic = 0.0
        for mu in range(4):
            for nu in range(4):
                kinetic += g_inv[mu, nu] * nabla_Phi[mu] * nabla_Phi[nu]
        
        return self.params.alpha_phi * kinetic * sqrt_minus_g
    
    def L_emotional_potential(
        self,
        Phi: float,
        Psi: complex,
        sqrt_minus_g: float
    ) -> float:
        """
        Emotional potential term.
        
        L_V = -V(Φ, |Ψ|²)
        
        Parameters
        ----------
        Phi : float
            Emotional field
        Psi : complex
            Consciousness field
        sqrt_minus_g : float
            Volume element
            
        Returns
        -------
        float
            Lagrangian density
        """
        if self.emotional_potential is not None:
            V = self.emotional_potential.V_total(Phi, abs(Psi)**2)
        else:
            # Fallback: simple harmonic
            V = 0.5 * self.params.mu_squared * Phi**2
        
        return -V * sqrt_minus_g
    
    def L_geometric(
        self,
        R_scalar: float,
        sqrt_minus_g: float
    ) -> float:
        """
        Geometric coupling term.
        
        L_geom = κ_Π · R
        
        Couples complexity (via κ_Π) to spacetime curvature.
        
        Parameters
        ----------
        R_scalar : float
            Ricci scalar
        sqrt_minus_g : float
            Volume element
            
        Returns
        -------
        float
            Lagrangian density
        """
        return self.params.kappa_Pi * R_scalar * sqrt_minus_g
    
    def L_spectral(
        self,
        t: float,
        sqrt_minus_g: float
    ) -> float:
        """
        Spectral coupling to Riemann zeta function.
        
        L_spectral = α · log|ζ(½ + it)|²
        
        Couples to arithmetic structure of primes.
        
        Parameters
        ----------
        t : float
            Time coordinate (imaginary part of zeta argument)
        sqrt_minus_g : float
            Volume element
            
        Returns
        -------
        float
            Lagrangian density
        """
        # Use precomputed zeta prime for simplicity
        # In full implementation, would evaluate ζ(½ + it)
        # For now, use modulation based on time and zeta'(½)
        
        zeta_term = self.params.zeta_prime_half * np.cos(2 * np.pi * self.f0 * t)
        log_term = np.log(abs(zeta_term)**2 + 1e-10)  # Avoid log(0)
        
        return self.params.alpha_zeta * log_term * sqrt_minus_g
    
    def L_total(
        self,
        config: UnifiedFieldConfiguration,
        g_inv: np.ndarray
    ) -> float:
        """
        Complete unified Lagrangian.
        
        L_QCAL = L_Ψ + L_Φ^kin + L_V + L_geom + L_spectral
        
        Parameters
        ----------
        config : UnifiedFieldConfiguration
            Field configuration
        g_inv : array
            Inverse metric
            
        Returns
        -------
        float
            Total Lagrangian density
        """
        L_psi = self.L_consciousness(config.nabla_Psi, g_inv, config.sqrt_minus_g)
        L_phi_kin = self.L_emotional_kinetic(config.nabla_Phi, g_inv, config.sqrt_minus_g)
        L_V = self.L_emotional_potential(config.Phi, config.Psi, config.sqrt_minus_g)
        L_geom = self.L_geometric(config.R_scalar, config.sqrt_minus_g)
        L_spec = self.L_spectral(config.t, config.sqrt_minus_g)
        
        return L_psi + L_phi_kin + L_V + L_geom + L_spec
    
    def equations_of_motion_Psi(
        self,
        Psi: complex,
        box_Psi: complex,
        R: float,
        t: float
    ) -> complex:
        """
        Equation of motion for consciousness field Ψ.
        
        From δS/δΨ† = 0:
        □Ψ - m_eff²Ψ - forcing = 0
        
        Parameters
        ----------
        Psi : complex
            Field value
        box_Psi : complex
            d'Alembertian □Ψ
        R : float
            Ricci scalar
        t : float
            Time
            
        Returns
        -------
        complex
            EOM residual (should be ~0)
        """
        # Effective mass from curvature and spectral coupling
        m_eff_sq = self.omega_0**2 + self.params.kappa_Pi * R
        
        # Spectral forcing
        forcing = self.params.alpha_zeta * self.params.zeta_prime_half * \
                  R * np.cos(2 * np.pi * self.f0 * t)
        
        return box_Psi - m_eff_sq * Psi - forcing * Psi
    
    def equations_of_motion_Phi(
        self,
        Phi: float,
        box_Phi: float,
        Psi: complex,
        dV_dPhi: float
    ) -> float:
        """
        Equation of motion for emotional field Φ.
        
        From δS/δΦ = 0:
        □Φ - dV/dΦ = 0
        
        Parameters
        ----------
        Phi : float
            Field value
        box_Phi : float
            d'Alembertian □Φ
        Psi : complex
            Consciousness field
        dV_dPhi : float
            Potential derivative
            
        Returns
        -------
        float
            EOM residual (should be ~0)
        """
        return box_Phi - dV_dPhi
    
    def compute_stress_energy_tensor(
        self,
        config: UnifiedFieldConfiguration
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute stress-energy tensors for both fields.
        
        Returns
        -------
        tuple
            (T_μν^Ψ, T_μν^Φ)
        """
        # Consciousness contribution
        T_Psi = np.zeros((4, 4), dtype=complex)
        
        for mu in range(4):
            for nu in range(4):
                T_Psi[mu, nu] = np.conj(config.nabla_Psi[mu]) * config.nabla_Psi[nu]
        
        # Emotional contribution
        T_Phi = np.zeros((4, 4))
        
        for mu in range(4):
            for nu in range(4):
                T_Phi[mu, nu] = config.nabla_Phi[mu] * config.nabla_Phi[nu]
                
                # Subtract metric term with potential
                if self.emotional_potential is not None:
                    V = self.emotional_potential.V_total(config.Phi, abs(config.Psi)**2)
                else:
                    V = 0.5 * self.params.mu_squared * config.Phi**2
                
                T_Phi[mu, nu] -= config.g_metric[mu, nu] * V
        
        return T_Psi.real, T_Phi


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate unified QCAL Lagrangian."""
    
    print("=" * 80)
    print("UNIFIED QCAL LAGRANGIAN - Consciousness + Emotion")
    print("=" * 80)
    print()
    print("Complete Lagrangian:")
    print("  L_QCAL = ∥∇_μΨ∥² + ½∥∇_μΦ∥² - V(Φ) + κ_Π·R + α·log|ζ|²")
    print()
    print("Unifies:")
    print("  1. Consciousness coherence (Ψ) - SU(Ψ) dynamics")
    print("  2. Emotional field (Φ) - Scalar field with symmetry breaking")
    print("  3. Geometric structure (R) - Spacetime curvature")
    print("  4. Arithmetic structure (ζ) - Prime number spectrum")
    print()
    
    # Initialize
    lagrangian = UnifiedQCALLagrangian()
    
    print("Parameters:")
    print("-" * 80)
    print(f"  f₀ = {lagrangian.f0} Hz")
    print(f"  α_Ψ = {lagrangian.params.alpha_psi}")
    print(f"  α_Φ = {lagrangian.params.alpha_phi}")
    print(f"  λ = {lagrangian.params.lambda_V}")
    print(f"  μ² = {lagrangian.params.mu_squared} (broken symmetry)")
    print(f"  κ_Π = {lagrangian.params.kappa_Pi}")
    print(f"  α_ζ = {lagrangian.params.alpha_zeta}")
    print()
    
    # Example configuration
    print("=" * 80)
    print("Example Field Configuration")
    print("=" * 80)
    print()
    
    # Minkowski metric
    g_metric = np.diag([-1, 1, 1, 1])
    g_inv = np.diag([-1, 1, 1, 1])
    sqrt_minus_g = 1.0
    
    # Fields
    t = 0.0
    Psi = 0.85 * np.exp(1j * 2 * np.pi * F_0 * t)
    Phi = 0.3
    
    # Derivatives (example: at rest)
    nabla_Psi = np.array([0.1j * Psi, 0.0, 0.0, 0.0])
    nabla_Phi = np.array([0.0, 0.0, 0.0, 0.0])
    
    # Curvature (small)
    R_scalar = 1e-3
    
    config = UnifiedFieldConfiguration(
        g_metric=g_metric,
        sqrt_minus_g=sqrt_minus_g,
        R_scalar=R_scalar,
        Psi=Psi,
        nabla_Psi=nabla_Psi,
        Phi=Phi,
        nabla_Phi=nabla_Phi,
        t=t,
        x=np.array([0, 0, 0])
    )
    
    print(f"Ψ = {Psi:.4f}")
    print(f"Φ = {Phi:.4f}")
    print(f"R = {R_scalar:.3e}")
    print()
    
    # Compute Lagrangian components
    print("Lagrangian Components:")
    print("-" * 80)
    
    L_psi = lagrangian.L_consciousness(nabla_Psi, g_inv, sqrt_minus_g)
    L_phi_kin = lagrangian.L_emotional_kinetic(nabla_Phi, g_inv, sqrt_minus_g)
    L_V = lagrangian.L_emotional_potential(Phi, Psi, sqrt_minus_g)
    L_geom = lagrangian.L_geometric(R_scalar, sqrt_minus_g)
    L_spec = lagrangian.L_spectral(t, sqrt_minus_g)
    
    print(f"  L_Ψ (consciousness):  {L_psi:.6e}")
    print(f"  L_Φ^kin (emotional):  {L_phi_kin:.6e}")
    print(f"  L_V (potential):      {L_V:.6e}")
    print(f"  L_geom (curvature):   {L_geom:.6e}")
    print(f"  L_spectral (primes):  {L_spec:.6e}")
    print()
    
    L_total = lagrangian.L_total(config, g_inv)
    print(f"  L_QCAL (total):       {L_total:.6e}")
    print()
    
    # Stress-energy tensors
    print("=" * 80)
    print("Stress-Energy Tensors")
    print("=" * 80)
    print()
    
    T_Psi, T_Phi = lagrangian.compute_stress_energy_tensor(config)
    
    print("Consciousness contribution T_μν^Ψ:")
    print(f"  T_00^Ψ = {T_Psi[0,0]:.6e}")
    print()
    
    print("Emotional contribution T_μν^Φ:")
    print(f"  T_00^Φ = {T_Phi[0,0]:.6e}")
    print()
    
    print("Total energy density:")
    print(f"  T_00^total = {T_Psi[0,0] + T_Phi[0,0]:.6e}")
    print()
    
    print("=" * 80)
    print("✨ Unified QCAL Lagrangian successfully implemented!")
    print("=" * 80)
    print()
    print("→ Consciousness and emotion now unified in single framework")
    print("→ Couples to both geometry (R) and arithmetic (ζ)")
    print("→ Foundation for collective consciousness-emotion dynamics")
    print()


if __name__ == "__main__":
    main()
