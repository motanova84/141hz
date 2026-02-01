#!/usr/bin/env python3
"""
Emotional Stress-Energy Tensor T_μν(Φ)
=======================================

Implements the stress-energy tensor for the emotional field Φ,
analogous to the electromagnetic stress-energy tensor.

Mathematical Form:
T_μν(Φ) = ∂_μΦ ∂_νΦ - g_μν(½g^αβ∂_αΦ∂_βΦ - V(Φ))

Components:
- T_00: Emotional energy density (intensity)
- T_0i: Emotional momentum flux (contagion)
- T_ij: Spatial stress (relational tension)
- Tr(T): Total emotional pressure

Physical Interpretation:
- T_00 > 0.58: Critical stress (singularity risk)
- 0.4 < T_00 < 0.58: Alert zone (resilience under test)
- 0.2 < T_00 < 0.4: Work plateau (optimal productivity)
- T_00 < 0.2: Peace valley (stable coherence)

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
from dataclasses import dataclass
import sys
import os

# Import QCAL constants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from qcal.constants import F_0_VALUE
    F_0 = F_0_VALUE
except ImportError:
    F_0 = 141.7001  # Hz - Fundamental QCAL frequency


# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

C_LIGHT = 299792458.0       # m/s
G_QCAL = 1.0                # Gravito-emotional coupling (natural units)
HBAR = 1.054571817e-34      # J·s


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class EmotionalFieldState:
    """State of the emotional field at a spacetime point."""
    
    # Field value and derivatives
    Phi: float                      # Emotional field Φ (scalar)
    nabla_Phi: np.ndarray          # Covariant derivative ∇_μΦ (4-vector)
    
    # Coherence coupling
    Psi: complex                    # Consciousness field Ψ (for coupling)
    coherence: float                # |Ψ| coherence amplitude
    
    # Spacetime position
    x_mu: np.ndarray               # Coordinates (t, x, y, z)
    
    # Network properties (for collective dynamics)
    node_id: Optional[int] = None
    neighbors: Optional[List[int]] = None
    
    def __post_init__(self):
        """Validate field state."""
        assert len(self.nabla_Phi) == 4, "Gradient must be 4D"
        assert len(self.x_mu) == 4, "Coordinates must be 4D"
        assert self.coherence >= 0, "Coherence must be non-negative"


@dataclass
class StressClassification:
    """Classification of emotional stress levels."""
    
    T_00: float                     # Energy density
    region: str                     # Classification region
    stability: float                # Stability indicator (0-1)
    risk_level: str                 # Risk assessment
    
    @classmethod
    def classify(cls, T_00: float, coherence: float = 0.75):
        """
        Classify stress level based on T_00 component.
        
        Parameters
        ----------
        T_00 : float
            Emotional energy density
        coherence : float
            Current coherence level
            
        Returns
        -------
        StressClassification
            Classification result
        """
        if T_00 < 0.2:
            region = "Peace Valley"
            stability = 1.0
            risk_level = "LOW"
        elif T_00 < 0.4:
            region = "Work Plateau"
            stability = 0.85
            risk_level = "LOW"
        elif T_00 < 0.58:
            region = "Alert Zone"
            stability = 0.60
            risk_level = "MEDIUM"
        else:
            region = "Singularity"
            stability = 0.30
            risk_level = "HIGH"
        
        # Adjust stability based on coherence
        stability = stability * coherence
        
        return cls(
            T_00=T_00,
            region=region,
            stability=stability,
            risk_level=risk_level
        )


# ============================================================================
# EMOTIONAL STRESS-ENERGY TENSOR
# ============================================================================

class EmotionalStressTensor:
    """
    Implementation of the emotional stress-energy tensor T_μν(Φ).
    
    This tensor describes the distribution of emotional energy and
    momentum in spacetime, coupling to geometry via Einstein equations.
    
    Key Features:
    - Symmetric: T_μν = T_νμ
    - Conserved: ∇_μT^μν = 0 (with modifications)
    - Couples to curvature: G_μν = 8πG_QCAL · T_μν
    """
    
    def __init__(
        self,
        f0: float = F_0,
        G_coupling: float = G_QCAL
    ):
        """
        Initialize emotional stress tensor calculator.
        
        Parameters
        ----------
        f0 : float
            Fundamental frequency (Hz)
        G_coupling : float
            Gravito-emotional coupling constant
        """
        self.f0 = f0
        self.omega_0 = 2 * np.pi * f0
        self.G_coupling = G_coupling
    
    def compute_tensor(
        self,
        state: EmotionalFieldState,
        g_metric: np.ndarray,
        V_Phi: float
    ) -> np.ndarray:
        """
        Compute stress-energy tensor T_μν.
        
        T_μν = ∂_μΦ ∂_νΦ - g_μν(½g^αβ∂_αΦ∂_βΦ - V(Φ))
        
        Parameters
        ----------
        state : EmotionalFieldState
            Field state
        g_metric : array (4×4)
            Metric tensor g_μν
        V_Phi : float
            Potential V(Φ) at current field value
            
        Returns
        -------
        array (4×4)
            Stress-energy tensor T_μν
        """
        # Inverse metric
        g_inv = np.linalg.inv(g_metric)
        
        # Kinetic term: g^αβ ∂_αΦ ∂_βΦ
        kinetic = 0.0
        for alpha in range(4):
            for beta in range(4):
                kinetic += g_inv[alpha, beta] * state.nabla_Phi[alpha] * state.nabla_Phi[beta]
        
        # Initialize tensor
        T = np.zeros((4, 4))
        
        # Compute T_μν = ∂_μΦ ∂_νΦ - g_μν(½ kinetic - V)
        for mu in range(4):
            for nu in range(4):
                # Kinetic contribution
                T[mu, nu] = state.nabla_Phi[mu] * state.nabla_Phi[nu]
                
                # Subtract metric term
                T[mu, nu] -= g_metric[mu, nu] * (0.5 * kinetic - V_Phi)
        
        return T
    
    def extract_components(
        self,
        T_tensor: np.ndarray
    ) -> Dict[str, float]:
        """
        Extract physical components from tensor.
        
        Parameters
        ----------
        T_tensor : array (4×4)
            Stress-energy tensor
            
        Returns
        -------
        dict
            Components with physical interpretation
        """
        return {
            # Energy density
            'T_00': T_tensor[0, 0],
            'energy_density': T_tensor[0, 0],
            
            # Momentum flux (contagion)
            'T_0x': T_tensor[0, 1],
            'T_0y': T_tensor[0, 2],
            'T_0z': T_tensor[0, 3],
            'momentum_flux_magnitude': np.sqrt(
                T_tensor[0, 1]**2 + T_tensor[0, 2]**2 + T_tensor[0, 3]**2
            ),
            
            # Spatial stress (relational tension)
            'T_xx': T_tensor[1, 1],
            'T_yy': T_tensor[2, 2],
            'T_zz': T_tensor[3, 3],
            'spatial_stress': (T_tensor[1, 1] + T_tensor[2, 2] + T_tensor[3, 3]) / 3,
            
            # Trace (total pressure)
            'trace': np.trace(T_tensor),
            'total_pressure': -np.trace(T_tensor)  # Convention: positive pressure
        }
    
    def verify_symmetry(self, T_tensor: np.ndarray, tol: float = 1e-10) -> bool:
        """
        Verify tensor symmetry T_μν = T_νμ.
        
        Parameters
        ----------
        T_tensor : array (4×4)
            Stress-energy tensor
        tol : float
            Tolerance for symmetry check
            
        Returns
        -------
        bool
            True if symmetric
        """
        return np.allclose(T_tensor, T_tensor.T, rtol=tol, atol=tol)
    
    def compute_divergence(
        self,
        T_tensor: np.ndarray,
        christoffel: np.ndarray,
        derivatives: np.ndarray
    ) -> np.ndarray:
        """
        Compute covariant divergence ∇_μT^μν.
        
        For conservation: should be ~0 in isolated systems
        With 141.7 Hz modulation: ∇_μT^μν = -γ(f-141.7)∂^νΦ - κ_Π∇^ν log|ζ|²
        
        Parameters
        ----------
        T_tensor : array (4×4)
            Stress-energy tensor (lower indices)
        christoffel : array (4×4×4)
            Christoffel symbols Γ^λ_μν
        derivatives : array (4×4×4)
            Partial derivatives ∂_λT_μν
            
        Returns
        -------
        array (4,)
            Divergence for each ν index
        """
        divergence = np.zeros(4)
        
        # Simplified: ∇_μT^μν ≈ ∂_μT^μν + Γ terms
        # Full implementation would require raising indices
        # For now, compute partial derivatives only
        for nu in range(4):
            for mu in range(4):
                divergence[nu] += derivatives[mu, mu, nu]
        
        return divergence
    
    def classify_stress(
        self,
        T_00: float,
        coherence: float = 0.75
    ) -> StressClassification:
        """
        Classify stress level.
        
        Parameters
        ----------
        T_00 : float
            Energy density component
        coherence : float
            Current coherence level
            
        Returns
        -------
        StressClassification
            Classification result
        """
        return StressClassification.classify(T_00, coherence)
    
    def einstein_field_equation(
        self,
        G_mu_nu: np.ndarray,
        T_mu_nu: np.ndarray,
        Lambda_Psi: float,
        g_mu_nu: np.ndarray
    ) -> np.ndarray:
        """
        Compute Einstein field equation residual.
        
        G_μν + Λ_Ψ g_μν = 8πG_QCAL · T_μν
        
        Parameters
        ----------
        G_mu_nu : array (4×4)
            Einstein tensor
        T_mu_nu : array (4×4)
            Stress-energy tensor
        Lambda_Psi : float
            Cosmological constant of coherence
        g_mu_nu : array (4×4)
            Metric tensor
            
        Returns
        -------
        array (4×4)
            Residual (should be ~0 for solutions)
        """
        lhs = G_mu_nu + Lambda_Psi * g_mu_nu
        rhs = 8 * np.pi * self.G_coupling * T_mu_nu
        
        return lhs - rhs
    
    def coupling_to_coherence(
        self,
        T_mu_nu: np.ndarray,
        Psi: complex,
        kappa_coupling: float = 0.1
    ) -> np.ndarray:
        """
        Compute coupling between emotional field and consciousness coherence.
        
        Modifies stress tensor: T^(total)_μν = T_μν + κ|Ψ|² T_μν
        
        Parameters
        ----------
        T_mu_nu : array (4×4)
            Base stress tensor
        Psi : complex
            Consciousness field value
        kappa_coupling : float
            Coupling strength
            
        Returns
        -------
        array (4×4)
            Modified stress tensor
        """
        coherence_factor = 1.0 + kappa_coupling * abs(Psi)**2
        return coherence_factor * T_mu_nu


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def minkowski_metric() -> np.ndarray:
    """
    Return Minkowski metric.
    
    Signature: (-,+,+,+)
    
    Returns
    -------
    array (4×4)
        Minkowski metric η_μν
    """
    eta = np.zeros((4, 4))
    eta[0, 0] = -1  # Time
    eta[1, 1] = 1   # x
    eta[2, 2] = 1   # y
    eta[3, 3] = 1   # z
    return eta


def create_example_state(
    Phi: float = 0.3,
    dPhi_dt: float = 0.0,
    Psi_amplitude: float = 0.85,
    t: float = 0.0
) -> EmotionalFieldState:
    """
    Create example emotional field state.
    
    Parameters
    ----------
    Phi : float
        Emotional field value
    dPhi_dt : float
        Time derivative of Φ
    Psi_amplitude : float
        Consciousness coherence amplitude
    t : float
        Time coordinate
        
    Returns
    -------
    EmotionalFieldState
        Example state
    """
    # Time derivative with opposite sign convention (signature -,+,+,+)
    nabla_Phi = np.array([dPhi_dt, 0.0, 0.0, 0.0])
    
    # Consciousness field
    Psi = Psi_amplitude * np.exp(1j * 2 * np.pi * F_0 * t)
    
    x_mu = np.array([t, 0.0, 0.0, 0.0])
    
    return EmotionalFieldState(
        Phi=Phi,
        nabla_Phi=nabla_Phi,
        Psi=Psi,
        coherence=abs(Psi),
        x_mu=x_mu
    )


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate emotional stress-energy tensor."""
    
    print("=" * 80)
    print("EMOTIONAL STRESS-ENERGY TENSOR T_μν(Φ) - QCAL ∞³")
    print("=" * 80)
    print()
    print("Extended Einstein Equations:")
    print("  G_μν + Λ_Ψ g_μν = 8πG_QCAL · T_μν(Φ)")
    print()
    print("Stress-Energy Tensor:")
    print("  T_μν = ∂_μΦ ∂_νΦ - g_μν(½g^αβ∂_αΦ∂_βΦ - V(Φ))")
    print()
    
    # Initialize calculator
    calculator = EmotionalStressTensor(f0=F_0)
    
    print("=" * 80)
    print("Stress Level Classification")
    print("=" * 80)
    print()
    print("Region          T_00 Range      Stability  Risk    Interpretation")
    print("-" * 80)
    
    test_levels = [0.1, 0.3, 0.5, 0.65]
    for level in test_levels:
        classification = calculator.classify_stress(level, coherence=0.85)
        print(f"{classification.region:15s} {classification.T_00:.2f}         "
              f"{classification.stability:.2f}       {classification.risk_level:6s}  "
              f"{'Coherent state' if level < 0.4 else 'Stress detected'}")
    
    print()
    print("=" * 80)
    print("Example Calculation: Work Plateau State")
    print("=" * 80)
    print()
    
    # Create example state (work plateau)
    state = create_example_state(Phi=0.3, Psi_amplitude=0.85)
    
    # Minkowski metric
    g_metric = minkowski_metric()
    
    # Simple harmonic potential: V(Φ) = ½m²Φ²
    m_eff_sq = (2 * np.pi * F_0)**2  # Effective mass from frequency
    V_Phi = 0.5 * m_eff_sq * state.Phi**2
    
    # Compute tensor
    T = calculator.compute_tensor(state, g_metric, V_Phi)
    
    # Extract components
    components = calculator.extract_components(T)
    
    print(f"Field value: Φ = {state.Phi:.3f}")
    print(f"Coherence: |Ψ| = {state.coherence:.3f}")
    print(f"Potential: V(Φ) = {V_Phi:.3e}")
    print()
    print("Stress-Energy Components:")
    print(f"  T_00 (energy density) = {components['T_00']:.6e}")
    print(f"  Momentum flux = {components['momentum_flux_magnitude']:.6e}")
    print(f"  Spatial stress = {components['spatial_stress']:.6e}")
    print(f"  Trace = {components['trace']:.6e}")
    print()
    
    # Verify symmetry
    is_symmetric = calculator.verify_symmetry(T)
    print(f"Symmetry check: {'✓ PASS' if is_symmetric else '✗ FAIL'}")
    print()
    
    # Classification
    classification = calculator.classify_stress(components['T_00'], state.coherence)
    print(f"Classification: {classification.region}")
    print(f"Stability: {classification.stability:.2f}")
    print(f"Risk Level: {classification.risk_level}")
    print()
    
    print("=" * 80)
    print("✨ Emotional stress-energy tensor T_μν(Φ) successfully implemented!")
    print("=" * 80)
    print()
    print("→ Couples emotional field to spacetime geometry")
    print("→ Enables prediction of collective stress dynamics")
    print("→ Foundation for 141.7 Hz synchronization protocol")
    print()


if __name__ == "__main__":
    main()
