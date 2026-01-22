#!/usr/bin/env python3
"""
Electromagnetic Gauge Bundle (π_α: G → 𝓜^3,1)
==============================================

This module implements the electromagnetic gauge fiber bundle with:
- Base manifold: 𝓜^3,1 (Minkowski spacetime)
- Fiber: U(1) gauge group
- Coupling: α ≈ 1/137.036 (fine structure constant)

The electromagnetic bundle represents the gauge structure underlying
electromagnetism, with U(1) phase transformations at each spacetime point.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

import numpy as np
from typing import Tuple, Callable, Optional
import mpmath as mp

from .principal_bundle import PrincipalFiberBundle, U1Fiber

# Set precision for calculations
mp.dps = 50


class ElectromagneticGaugeBundle(PrincipalFiberBundle):
    """
    Electromagnetic gauge principal bundle π_α: G → 𝓜^3,1.
    
    Represents the U(1) gauge structure of electromagnetism over
    Minkowski spacetime.
    
    Mathematical Structure:
    ----------------------
    - Base: 𝓜^3,1 = ℝ^(3,1) (Minkowski spacetime with signature (-,+,+,+))
    - Fiber: U(1) = {e^(iα) : α ∈ [0, 2π)}
    - Projection: π_α(x^μ, e^(iα)) = x^μ
    - Coupling: α ≈ 1/137.036 (fine structure constant)
    
    Physical Interpretation:
    -----------------------
    The electromagnetic bundle encodes:
    - Local U(1) gauge freedom (phase transformations)
    - Electromagnetic gauge potential A_μ (connection)
    - Electromagnetic field strength F_μν (curvature)
    - Charge quantization and gauge invariance
    
    Attributes
    ----------
    alpha : float
        Fine structure constant α ≈ 1/137.036
    spacetime_metric : np.ndarray
        Minkowski metric η_μν with signature (-,+,+,+)
    """
    
    # Fine structure constant (CODATA 2022)
    ALPHA = mp.mpf("7.2973525693e-3")  # ≈ 1/137.036
    ALPHA_INVERSE = 1 / ALPHA  # ≈ 137.036
    
    # Speed of light (m/s, exact)
    C_LIGHT = mp.mpf("299792458")
    
    # Elementary charge (C, exact since 2019 redefinition)
    E_CHARGE = mp.mpf("1.602176634e-19")
    
    # Reduced Planck constant (J·s, exact)
    H_BAR = mp.mpf("1.054571817e-34")
    
    # Permittivity of free space (F/m)
    EPSILON_0 = mp.mpf("8.8541878128e-12")
    
    def __init__(self, connection: Optional[Callable] = None):
        """
        Initialize electromagnetic gauge bundle.
        
        Parameters
        ----------
        connection : Optional[Callable]
            Gauge potential A_μ. If None, uses vacuum (zero) connection.
        """
        # Minkowski spacetime has dimension 4 (t, x, y, z)
        base_dimension = 4
        
        # Projection: π_α(x^μ, e^(iα)) = x^μ
        # For a point in total space (spacetime point, fiber element),
        # projection returns just the spacetime point
        def projection(total_space_point):
            if isinstance(total_space_point, tuple):
                return total_space_point[0]  # Return spacetime coordinates
            return total_space_point
        
        # Initialize parent class
        super().__init__(
            name="Electromagnetic Gauge Bundle (π_α)",
            base_dimension=base_dimension,
            projection=projection,
            connection=connection
        )
        
        self.alpha = float(self.ALPHA)
        
        # Minkowski metric η_μν with signature (-,+,+,+)
        self.spacetime_metric = np.diag([-1.0, 1.0, 1.0, 1.0])
    
    def gauge_transformation(
        self,
        fiber: U1Fiber,
        gauge_function: Callable[[np.ndarray], float]
    ) -> U1Fiber:
        """
        Apply gauge transformation to fiber element.
        
        Under a gauge transformation Λ(x), the fiber transforms as:
        e^(iα) → e^(iα) · e^(iΛ(x))
        
        Parameters
        ----------
        fiber : U1Fiber
            Initial fiber element
        gauge_function : Callable
            Gauge function Λ: M → ℝ
        
        Returns
        -------
        U1Fiber
            Transformed fiber element
        """
        # In this simplified model, we apply the transformation directly
        # In a full implementation, would need the spacetime point
        return fiber  # Placeholder - needs spacetime point context
    
    def electromagnetic_field_strength(
        self,
        point: np.ndarray,
        mu: int,
        nu: int,
        epsilon: float = 1e-8
    ) -> float:
        """
        Compute electromagnetic field strength tensor F_μν.
        
        F_μν = ∂_μ A_ν - ∂_ν A_μ
        
        This is the curvature of the U(1) bundle.
        
        Parameters
        ----------
        point : np.ndarray
            Spacetime point x^μ
        mu, nu : int
            Spacetime indices (0=time, 1,2,3=space)
        epsilon : float
            Step size for numerical derivatives
        
        Returns
        -------
        float
            Field strength F_μν at point
        """
        if self.connection is None:
            return 0.0
        
        # Compute ∂_μ A_ν
        point_mu_plus = point.copy()
        point_mu_plus[mu] += epsilon
        
        point_mu_minus = point.copy()
        point_mu_minus[mu] -= epsilon
        
        tangent_nu = np.zeros_like(point)
        tangent_nu[nu] = 1.0
        
        A_nu_plus = self.connection(point_mu_plus, tangent_nu)
        A_nu_minus = self.connection(point_mu_minus, tangent_nu)
        
        d_mu_A_nu = (A_nu_plus - A_nu_minus) / (2 * epsilon)
        
        # Compute ∂_ν A_μ
        point_nu_plus = point.copy()
        point_nu_plus[nu] += epsilon
        
        point_nu_minus = point.copy()
        point_nu_minus[nu] -= epsilon
        
        tangent_mu = np.zeros_like(point)
        tangent_mu[mu] = 1.0
        
        A_mu_plus = self.connection(point_nu_plus, tangent_mu)
        A_mu_minus = self.connection(point_nu_minus, tangent_mu)
        
        d_nu_A_mu = (A_mu_plus - A_mu_minus) / (2 * epsilon)
        
        # F_μν = ∂_μ A_ν - ∂_ν A_μ
        return d_mu_A_nu - d_nu_A_mu
    
    def create_constant_electric_field(self, E_field: np.ndarray) -> Callable:
        """
        Create connection for constant electric field.
        
        For constant electric field E⃗ = (E_x, E_y, E_z),
        gauge potential is A_μ = (-E⃗·r⃗, 0, 0, 0) in temporal gauge.
        
        Parameters
        ----------
        E_field : np.ndarray
            Electric field vector (E_x, E_y, E_z)
        
        Returns
        -------
        Callable
            Connection 1-form A_μ
        """
        def connection(point: np.ndarray, tangent: np.ndarray) -> float:
            # point = (t, x, y, z)
            # A_0 = -E⃗·r⃗, A_i = 0
            if tangent[0] != 0:  # Time component
                spatial_pos = point[1:]
                return -np.dot(E_field, spatial_pos) * tangent[0]
            return 0.0
        
        self.connection = connection
        return connection
    
    def create_constant_magnetic_field(self, B_field: np.ndarray) -> Callable:
        """
        Create connection for constant magnetic field.
        
        For constant magnetic field B⃗ = (B_x, B_y, B_z),
        use vector potential A⃗ = ½(B⃗ × r⃗) in symmetric gauge.
        
        Parameters
        ----------
        B_field : np.ndarray
            Magnetic field vector (B_x, B_y, B_z)
        
        Returns
        -------
        Callable
            Connection 1-form A_μ
        """
        def connection(point: np.ndarray, tangent: np.ndarray) -> float:
            # point = (t, x, y, z)
            # A⃗ = ½(B⃗ × r⃗)
            spatial_pos = point[1:]
            vector_potential = 0.5 * np.cross(B_field, spatial_pos)
            
            # A_0 = 0 (Coulomb gauge), A_i from vector potential
            spatial_tangent = tangent[1:]
            return np.dot(vector_potential, spatial_tangent)
        
        self.connection = connection
        return connection
    
    def lorentz_force(
        self,
        point: np.ndarray,
        charge: float,
        velocity: np.ndarray
    ) -> np.ndarray:
        """
        Compute Lorentz force F = q(E + v × B) at a point.
        
        Parameters
        ----------
        point : np.ndarray
            Spacetime point (t, x, y, z)
        charge : float
            Particle charge (in units of elementary charge)
        velocity : np.ndarray
            3-velocity (v_x, v_y, v_z)
        
        Returns
        -------
        np.ndarray
            Force vector (F_x, F_y, F_z)
        """
        if self.connection is None:
            return np.zeros(3)
        
        # Extract electric field E_i = -∂_0 A_i - ∂_i A_0
        E = np.zeros(3)
        for i in range(1, 4):
            E[i-1] = -self.electromagnetic_field_strength(point, 0, i)
        
        # Extract magnetic field B_i = ε_ijk ∂_j A_k
        B = np.zeros(3)
        B[0] = self.electromagnetic_field_strength(point, 2, 3)  # F_23
        B[1] = self.electromagnetic_field_strength(point, 3, 1)  # F_31
        B[2] = self.electromagnetic_field_strength(point, 1, 2)  # F_12
        
        # Lorentz force: F = q(E + v × B)
        q = charge * float(self.E_CHARGE)
        return q * (E + np.cross(velocity, B))
    
    def __repr__(self) -> str:
        return (
            f"ElectromagneticGaugeBundle(α={self.alpha:.10f}, "
            f"α⁻¹={float(self.ALPHA_INVERSE):.6f}, "
            f"base=𝓜^(3,1))"
        )
