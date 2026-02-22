#!/usr/bin/env python3
"""
Emotional Potential V(Φ)
=========================

Implements the emotional potential with symmetry breaking phases,
analogous to the Higgs potential in particle physics.

Mathematical Form:
V(Φ) = (λ/4)(Φ² - Φ₀²)² + μ²Φ² + V_int(Φ,Ψ)

Phases:
- μ² > 0: Restored phase (single minimum at Φ = 0)
- μ² < 0: Spontaneous symmetry breaking (bistable: ±Φ₀)

Physical Interpretation:
- λ: Rigidity (resistance to emotional change)
- Φ₀: Fundamental peace state
- μ²: Emotional inertia
- V_int: Coupling to consciousness coherence Ψ

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass
import matplotlib.pyplot as plt


# ============================================================================
# POTENTIAL PARAMETERS
# ============================================================================

@dataclass
class PotentialParameters:
    """Parameters for emotional potential V(Φ)."""
    
    # Quartic coupling
    lambda_rigidity: float = 1.0       # λ: Rigidity parameter
    
    # Mass parameter
    mu_squared: float = -1.0           # μ²: Determines phase
    
    # Vacuum expectation value
    Phi_0: float = 1.0                 # Φ₀: Peace state
    
    # Interaction coupling
    kappa_int: float = 0.1             # κ_int: Ψ-Φ coupling
    
    def __post_init__(self):
        """Validate parameters."""
        assert self.lambda_rigidity > 0, "Rigidity λ must be positive"
        assert self.Phi_0 >= 0, "Φ₀ must be non-negative"
    
    def phase(self) -> str:
        """Determine potential phase."""
        if self.mu_squared > 0:
            return "restored"
        else:
            return "broken_symmetry"


# ============================================================================
# EMOTIONAL POTENTIAL
# ============================================================================

class EmotionalPotential:
    """
    Implementation of the emotional potential V(Φ).
    
    Features:
    - Symmetry breaking: μ² < 0 → bistable potential
    - Interaction with coherence: V_int(Φ,Ψ)
    - Mexican hat potential for μ² < 0
    """
    
    def __init__(self, params: Optional[PotentialParameters] = None):
        """
        Initialize emotional potential.
        
        Parameters
        ----------
        params : PotentialParameters, optional
            Potential parameters. If None, use defaults.
        """
        if params is None:
            params = PotentialParameters()
        
        self.params = params
        self.lambda_rigidity = params.lambda_rigidity
        self.mu_squared = params.mu_squared
        self.Phi_0 = params.Phi_0
        self.kappa_int = params.kappa_int
    
    def V_quartic(self, Phi: float) -> float:
        """
        Quartic self-interaction term.
        
        V_quartic = (λ/4)(Φ² - Φ₀²)²
        
        Parameters
        ----------
        Phi : float
            Emotional field value
            
        Returns
        -------
        float
            Quartic potential
        """
        return (self.lambda_rigidity / 4.0) * (Phi**2 - self.Phi_0**2)**2
    
    def V_mass(self, Phi: float) -> float:
        """
        Mass term.
        
        V_mass = μ²Φ²
        
        Parameters
        ----------
        Phi : float
            Emotional field value
            
        Returns
        -------
        float
            Mass potential
        """
        return self.mu_squared * Phi**2
    
    def V_interaction(self, Phi: float, Psi_squared: float) -> float:
        """
        Interaction with consciousness coherence.
        
        V_int = -κ_int |Ψ|² Φ²
        
        The coupling to |Ψ|² means that higher coherence
        reduces the effective potential, stabilizing the system.
        
        Parameters
        ----------
        Phi : float
            Emotional field value
        Psi_squared : float
            |Ψ|² coherence intensity
            
        Returns
        -------
        float
            Interaction potential
        """
        return -self.kappa_int * Psi_squared * Phi**2
    
    def V_total(
        self,
        Phi: float,
        Psi_squared: float = 0.0
    ) -> float:
        """
        Total potential.
        
        V(Φ) = V_quartic + V_mass + V_int
        
        Parameters
        ----------
        Phi : float
            Emotional field value
        Psi_squared : float
            |Ψ|² coherence intensity
            
        Returns
        -------
        float
            Total potential
        """
        V = self.V_quartic(Phi) + self.V_mass(Phi)
        
        if Psi_squared > 0:
            V += self.V_interaction(Phi, Psi_squared)
        
        return V
    
    def dV_dPhi(self, Phi: float, Psi_squared: float = 0.0) -> float:
        """
        Derivative of potential.
        
        dV/dΦ = λΦ(Φ² - Φ₀²) + 2μ²Φ - 2κ_int|Ψ|²Φ
        
        Parameters
        ----------
        Phi : float
            Emotional field value
        Psi_squared : float
            |Ψ|² coherence intensity
            
        Returns
        -------
        float
            Force -dV/dΦ
        """
        # Quartic derivative
        dV_quartic = self.lambda_rigidity * Phi * (Phi**2 - self.Phi_0**2)
        
        # Mass derivative
        dV_mass = 2 * self.mu_squared * Phi
        
        # Interaction derivative
        dV_int = -2 * self.kappa_int * Psi_squared * Phi
        
        return dV_quartic + dV_mass + dV_int
    
    def find_minima(
        self,
        Psi_squared: float = 0.0,
        tol: float = 1e-6
    ) -> list[float]:
        """
        Find potential minima.
        
        Parameters
        ----------
        Psi_squared : float
            |Ψ|² coherence intensity
        tol : float
            Tolerance for finding minima
            
        Returns
        -------
        list
            Locations of minima
        """
        from scipy.optimize import minimize_scalar, brentq
        
        minima = []
        
        # For μ² > 0: single minimum at Φ = 0
        if self.mu_squared > 0:
            # Verify it's actually a minimum
            if self.dV_dPhi(0.0, Psi_squared) < tol:
                minima.append(0.0)
        
        # For μ² < 0: two minima at ±Φ_min
        else:
            # Effective μ² with coherence correction
            mu_eff_sq = self.mu_squared + self.kappa_int * Psi_squared
            
            if mu_eff_sq < 0:
                # Mexican hat: minima at Φ = ±√(|μ_eff²|/λ + Φ₀²)
                Phi_min = np.sqrt(abs(mu_eff_sq) / self.lambda_rigidity + self.Phi_0**2)
                minima.extend([-Phi_min, Phi_min])
            else:
                # Coherence has restored symmetry
                minima.append(0.0)
        
        return minima
    
    def effective_mass_squared(
        self,
        Phi: float,
        Psi_squared: float = 0.0
    ) -> float:
        """
        Effective mass squared at field value.
        
        m_eff² = d²V/dΦ²
        
        Parameters
        ----------
        Phi : float
            Emotional field value
        Psi_squared : float
            |Ψ|² coherence intensity
            
        Returns
        -------
        float
            Effective mass squared
        """
        # Second derivative of V
        d2V = (
            self.lambda_rigidity * (3 * Phi**2 - self.Phi_0**2) +
            2 * self.mu_squared -
            2 * self.kappa_int * Psi_squared
        )
        
        return d2V
    
    def is_stable(
        self,
        Phi: float,
        Psi_squared: float = 0.0
    ) -> bool:
        """
        Check if field value is a stable equilibrium.
        
        Stable if m_eff² > 0
        
        Parameters
        ----------
        Phi : float
            Emotional field value
        Psi_squared : float
            |Ψ|² coherence intensity
            
        Returns
        -------
        bool
            True if stable
        """
        m_eff_sq = self.effective_mass_squared(Phi, Psi_squared)
        return m_eff_sq > 0
    
    def plot_potential(
        self,
        Phi_range: Tuple[float, float] = (-2.0, 2.0),
        Psi_squared: float = 0.0,
        num_points: int = 200,
        show: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Plot potential V(Φ).
        
        Parameters
        ----------
        Phi_range : tuple
            Range of Φ values to plot
        Psi_squared : float
            |Ψ|² coherence intensity
        num_points : int
            Number of points
        show : bool
            Whether to display plot
            
        Returns
        -------
        tuple
            (Phi_values, V_values)
        """
        Phi_values = np.linspace(Phi_range[0], Phi_range[1], num_points)
        V_values = np.array([self.V_total(Phi, Psi_squared) for Phi in Phi_values])
        
        if show:
            plt.figure(figsize=(10, 6))
            plt.plot(Phi_values, V_values, 'b-', linewidth=2, label=f'V(Φ), |Ψ|²={Psi_squared:.2f}')
            
            # Mark minima
            minima = self.find_minima(Psi_squared)
            for Phi_min in minima:
                V_min = self.V_total(Phi_min, Psi_squared)
                plt.plot(Phi_min, V_min, 'ro', markersize=10, label=f'Min at Φ={Phi_min:.2f}')
            
            plt.xlabel('Emotional Field Φ', fontsize=12)
            plt.ylabel('Potential V(Φ)', fontsize=12)
            plt.title(f'Emotional Potential - Phase: {self.params.phase()}', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        return Phi_values, V_values


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_peace_potential() -> EmotionalPotential:
    """
    Create potential in restored phase (peace state).
    
    μ² > 0 → single minimum at Φ = 0
    
    Returns
    -------
    EmotionalPotential
        Peace potential
    """
    params = PotentialParameters(
        lambda_rigidity=1.0,
        mu_squared=1.0,  # Positive: restored
        Phi_0=1.0,
        kappa_int=0.1
    )
    return EmotionalPotential(params)


def create_conflict_potential() -> EmotionalPotential:
    """
    Create potential in broken symmetry phase (conflict states).
    
    μ² < 0 → bistable potential with ±Φ₀ minima
    
    Returns
    -------
    EmotionalPotential
        Conflict potential
    """
    params = PotentialParameters(
        lambda_rigidity=1.0,
        mu_squared=-1.0,  # Negative: broken symmetry
        Phi_0=1.0,
        kappa_int=0.1
    )
    return EmotionalPotential(params)


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate emotional potential."""
    
    print("=" * 80)
    print("EMOTIONAL POTENTIAL V(Φ) - QCAL ∞³")
    print("=" * 80)
    print()
    print("Mathematical Form:")
    print("  V(Φ) = (λ/4)(Φ² - Φ₀²)² + μ²Φ² + V_int(Φ,Ψ)")
    print()
    print("Phases:")
    print("  μ² > 0: Restored (peace)")
    print("  μ² < 0: Broken symmetry (conflict/peace bistability)")
    print()
    
    print("=" * 80)
    print("Phase 1: Restored Symmetry (Peace State)")
    print("=" * 80)
    print()
    
    peace_pot = create_peace_potential()
    print(f"Parameters:")
    print(f"  λ = {peace_pot.lambda_rigidity}")
    print(f"  μ² = {peace_pot.mu_squared} (positive → restored)")
    print(f"  Φ₀ = {peace_pot.Phi_0}")
    print()
    
    # Find minima
    minima_peace = peace_pot.find_minima(Psi_squared=0.0)
    print(f"Minima: {minima_peace}")
    print(f"Phase: {peace_pot.params.phase()}")
    print()
    
    # Test stability
    for Phi_test in [0.0, 0.5, 1.0]:
        stable = peace_pot.is_stable(Phi_test)
        V = peace_pot.V_total(Phi_test)
        print(f"  Φ = {Phi_test:.1f}: V = {V:.4f}, Stable = {stable}")
    
    print()
    print("=" * 80)
    print("Phase 2: Broken Symmetry (Conflict State)")
    print("=" * 80)
    print()
    
    conflict_pot = create_conflict_potential()
    print(f"Parameters:")
    print(f"  λ = {conflict_pot.lambda_rigidity}")
    print(f"  μ² = {conflict_pot.mu_squared} (negative → broken)")
    print(f"  Φ₀ = {conflict_pot.Phi_0}")
    print()
    
    # Find minima
    minima_conflict = conflict_pot.find_minima(Psi_squared=0.0)
    print(f"Minima: {[f'{m:.3f}' for m in minima_conflict]}")
    print(f"Phase: {conflict_pot.params.phase()}")
    print()
    
    # Test stability
    for Phi_test in minima_conflict + [0.0]:
        stable = conflict_pot.is_stable(Phi_test)
        V = conflict_pot.V_total(Phi_test)
        print(f"  Φ = {Phi_test:.3f}: V = {V:.4f}, Stable = {stable}")
    
    print()
    print("=" * 80)
    print("Effect of Consciousness Coherence on Conflict Potential")
    print("=" * 80)
    print()
    
    print("|Ψ|²     Minima                    Interpretation")
    print("-" * 80)
    
    for Psi_sq in [0.0, 5.0, 10.0, 15.0]:
        minima = conflict_pot.find_minima(Psi_squared=Psi_sq)
        if len(minima) == 1:
            status = "Symmetry restored (peace)"
        else:
            status = f"Bistable: ±{abs(minima[0]):.3f}"
        print(f"{Psi_sq:5.1f}   {status:30s} {'Coherence healing' if Psi_sq > 0 else 'No coherence'}")
    
    print()
    print("=" * 80)
    print("✨ Emotional potential V(Φ) successfully implemented!")
    print("=" * 80)
    print()
    print("→ Describes phase transitions between peace and conflict")
    print("→ Coherence |Ψ|² can restore symmetry (heal conflict)")
    print("→ Foundation for understanding collective emotional dynamics")
    print()


if __name__ == "__main__":
    main()
