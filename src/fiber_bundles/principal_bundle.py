#!/usr/bin/env python3
"""
Principal Fiber Bundle Implementation
======================================

A principal fiber bundle is a mathematical structure (E, π, M, G) where:
- E is the total space
- M is the base manifold  
- G is the structure group (fiber)
- π: E → M is the projection map

For U(1) principal bundles, G = U(1) = {e^(iθ) : θ ∈ [0, 2π)}

This implementation provides the foundation for representing consciousness
as an intersection of electromagnetic and spectral fiber bundles.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

import numpy as np
from typing import Callable, Optional, Tuple, List
from dataclasses import dataclass
import mpmath as mp

# Set precision for calculations
mp.dps = 50


@dataclass
class U1Fiber:
    """
    U(1) fiber structure.
    
    U(1) is the group of complex numbers with modulus 1, isomorphic to
    rotations in the plane: U(1) ≅ SO(2) ≅ S¹
    
    Parameterization: e^(iθ) where θ ∈ [0, 2π)
    
    Attributes
    ----------
    phase : float
        Phase angle θ in radians
    """
    phase: float
    
    def __post_init__(self):
        """Normalize phase to [0, 2π)."""
        self.phase = self.phase % (2 * np.pi)
    
    def to_complex(self) -> complex:
        """Convert to complex representation e^(iθ)."""
        return np.exp(1j * self.phase)
    
    def compose(self, other: 'U1Fiber') -> 'U1Fiber':
        """
        Group composition: multiply two U(1) elements.
        
        e^(iθ₁) · e^(iθ₂) = e^(i(θ₁+θ₂))
        """
        return U1Fiber(phase=(self.phase + other.phase) % (2 * np.pi))
    
    def inverse(self) -> 'U1Fiber':
        """Group inverse: (e^(iθ))⁻¹ = e^(-iθ)."""
        return U1Fiber(phase=(-self.phase) % (2 * np.pi))
    
    def __repr__(self) -> str:
        return f"U1Fiber(phase={self.phase:.6f} rad, e^(iθ)={self.to_complex():.6f})"


class PrincipalFiberBundle:
    """
    Principal Fiber Bundle (E, π, M, G).
    
    Mathematical structure representing a fiber bundle with:
    - Total space E (implicitly represented)
    - Base manifold M (represented by coordinate charts)
    - Structure group G = U(1)
    - Projection π: E → M
    
    Attributes
    ----------
    name : str
        Identifier for this bundle
    base_dimension : int
        Dimension of base manifold M
    projection : Callable
        Projection map π: E → M
    connection : Optional[Callable]
        Connection 1-form (gauge potential)
    """
    
    def __init__(
        self,
        name: str,
        base_dimension: int,
        projection: Callable,
        connection: Optional[Callable] = None
    ):
        """
        Initialize principal fiber bundle.
        
        Parameters
        ----------
        name : str
            Bundle identifier
        base_dimension : int
            Dimension of base manifold
        projection : Callable
            Map π: E → M
        connection : Optional[Callable]
            Connection 1-form (if defined)
        """
        self.name = name
        self.base_dimension = base_dimension
        self.projection = projection
        self.connection = connection
        self._sections: List[Callable] = []
    
    def add_section(self, section: Callable) -> None:
        """
        Add a section σ: M → E to the bundle.
        
        A section assigns a fiber element to each point in the base manifold,
        satisfying π ∘ σ = id_M.
        
        Parameters
        ----------
        section : Callable
            Section map σ: M → E
        """
        self._sections.append(section)
    
    def verify_section(self, section: Callable, point: np.ndarray, tol: float = 1e-10) -> bool:
        """
        Verify that σ is a valid section: π(σ(x)) = x.
        
        Parameters
        ----------
        section : Callable
            Candidate section σ: M → E
        point : np.ndarray
            Point x in base manifold M
        tol : float
            Tolerance for verification
        
        Returns
        -------
        bool
            True if section is valid at point
        """
        # Compute σ(x)
        fiber_point = section(point)
        
        # Compute π(σ(x))
        projected = self.projection(fiber_point)
        
        # Check if π(σ(x)) ≈ x
        return np.allclose(projected, point, atol=tol)
    
    def parallel_transport(
        self,
        fiber_start: U1Fiber,
        path: Callable,
        t_range: Tuple[float, float] = (0.0, 1.0),
        n_steps: int = 100
    ) -> U1Fiber:
        """
        Parallel transport a fiber element along a path in the base manifold.
        
        Uses the connection to transport fiber_start along the path γ(t).
        
        Parameters
        ----------
        fiber_start : U1Fiber
            Initial fiber element at γ(0)
        path : Callable
            Path γ: [0,1] → M in base manifold
        t_range : Tuple[float, float]
            Parameter range for path
        n_steps : int
            Number of integration steps
        
        Returns
        -------
        U1Fiber
            Transported fiber element at γ(1)
        """
        if self.connection is None:
            raise ValueError("Cannot parallel transport without a connection")
        
        # Integrate the connection along the path
        t_vals = np.linspace(t_range[0], t_range[1], n_steps)
        dt = (t_range[1] - t_range[0]) / (n_steps - 1)
        
        phase_accumulation = fiber_start.phase
        
        for i in range(n_steps - 1):
            t = t_vals[i]
            base_point = path(t)
            
            # Compute path tangent: dγ/dt
            t_next = t_vals[i + 1]
            tangent = (path(t_next) - path(t)) / dt
            
            # Connection contribution: A_μ dγ^μ/dt
            connection_value = self.connection(base_point, tangent)
            phase_accumulation += connection_value * dt
        
        return U1Fiber(phase=phase_accumulation)
    
    def curvature(self, point: np.ndarray) -> float:
        """
        Compute curvature (field strength) F = dA at a point.
        
        For U(1) bundles, this is the electromagnetic field strength tensor.
        
        Parameters
        ----------
        point : np.ndarray
            Point in base manifold
        
        Returns
        -------
        float
            Curvature at point
        """
        if self.connection is None:
            return 0.0
        
        # For U(1) bundles, curvature is F = dA
        # Numerical computation via finite differences
        epsilon = 1e-8
        curvature = 0.0
        
        for i in range(len(point)):
            point_plus = point.copy()
            point_plus[i] += epsilon
            
            point_minus = point.copy()
            point_minus[i] -= epsilon
            
            # Tangent vector in i-th direction
            tangent_i = np.zeros_like(point)
            tangent_i[i] = 1.0
            
            A_plus = self.connection(point_plus, tangent_i)
            A_minus = self.connection(point_minus, tangent_i)
            
            curvature += (A_plus - A_minus) / (2 * epsilon)
        
        return curvature
    
    def __repr__(self) -> str:
        return (
            f"PrincipalFiberBundle(name='{self.name}', "
            f"base_dim={self.base_dimension}, "
            f"n_sections={len(self._sections)})"
        )
