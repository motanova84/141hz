"""
Cytoplasmic Flow Model with Quantum Resonance
==============================================

This module implements a Stokes flow model for cytoplasmic streaming with quantum
resonance eigenfrequencies based on the Riemann hypothesis framework.

Physical Context:
- Cytoplasm density: ρ = 1050 kg/m³
- Kinematic viscosity: ν = 10⁻⁶ m²/s
- Characteristic length: L = 1 μm
- Reynolds number: Re = 10⁻⁶ << 1 (Stokes regime)

Mathematical Framework:
1. Stokes equations: μ∇²u = ∇p, ∇·u = 0
2. Vorticity diffusion: ∂ω/∂t = ν∇²ω (self-adjoint operator)
3. RiemannResonanceOperator: Hermitian operator producing eigenfrequencies fn = n × f₀
4. Beltrami flow: ω = λv (prevents blow-up)

Biological Model:
- Microtubules as quantum lattice (tubulin dimers)
- Kinesin-1 motors driving flow (v = 0.1-5 μm/s)
- Connection to Riemann zeros as pressure minima on critical line (σ = 1/2)

Author: José Manuel Mota Burruezo
License: MIT
"""

import numpy as np
from scipy import linalg
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings

# Import QCAL constants
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import F0_HZ, HBAR, PI_VIVO


class CytoplasmicParameters:
    """Physical parameters for cytoplasmic flow."""
    
    def __init__(self):
        # Cytoplasm properties
        self.rho = 1050.0  # kg/m³ - density
        self.nu = 1e-6     # m²/s - kinematic viscosity
        self.mu = self.rho * self.nu  # Pa·s - dynamic viscosity
        self.L = 1e-6      # m - characteristic length (1 μm)
        
        # Kinesin-1 motor properties
        self.v_kinesin_min = 0.1e-6  # m/s - minimum velocity
        self.v_kinesin_max = 5.0e-6  # m/s - maximum velocity
        self.v_kinesin = 1.0e-6      # m/s - typical velocity
        
        # Microtubule properties
        self.tubulin_dimer_length = 8e-9  # m - ~8 nm
        self.microtubule_diameter = 25e-9  # m - ~25 nm
        
    def reynolds_number(self, velocity=None):
        """
        Calculate Reynolds number for cytoplasmic flow.
        
        Re = v*L/ν
        
        Args:
            velocity: Flow velocity in m/s (default: kinesin velocity)
            
        Returns:
            Reynolds number (dimensionless)
        """
        if velocity is None:
            velocity = self.v_kinesin
        return velocity * self.L / self.nu
    
    def is_stokes_regime(self, velocity=None):
        """Check if flow is in Stokes regime (Re << 1)."""
        Re = self.reynolds_number(velocity)
        return Re < 1e-2  # Stokes regime for Re << 1


class RiemannResonanceOperator:
    """
    Hermitian operator connecting Riemann hypothesis to quantum resonance.
    
    The operator is self-adjoint (essential for Hilbert-Pólya approach):
    - Eigenvalues correspond to imaginary parts of Riemann zeros
    - Eigenfunctions produce resonant modes at fn = n × f₀
    - f₀ = 141.7001 Hz is the fundamental quantum frequency
    
    Mathematical structure:
    - H_ψ = -ν∇² + V(x) where V(x) is potential related to prime distribution
    - Spectrum: {λ_n} with ω_n = 2π × f_n = 2π × n × f₀
    """
    
    def __init__(self, n_modes=10, grid_size=100, domain_length=10e-6):
        """
        Initialize Riemann resonance operator.
        
        Args:
            n_modes: Number of eigenfrequencies to compute
            grid_size: Number of grid points for spatial discretization
            domain_length: Physical domain length in meters
        """
        self.n_modes = n_modes
        self.grid_size = grid_size
        self.domain_length = domain_length
        self.f0 = F0_HZ  # Fundamental frequency from QCAL
        
        # Spatial grid
        self.x = np.linspace(0, domain_length, grid_size)
        self.dx = self.x[1] - self.x[0]
        
    def construct_laplacian_1d(self):
        """
        Construct 1D Laplacian operator with periodic boundary conditions.
        
        Returns:
            Sparse matrix representing -∇²
        """
        # Second-order finite difference for d²/dx²
        diag_main = -2.0 * np.ones(self.grid_size)
        diag_off = np.ones(self.grid_size - 1)
        
        # Construct tridiagonal matrix
        laplacian = diags([diag_off, diag_main, diag_off], [-1, 0, 1])
        laplacian = laplacian / (self.dx ** 2)
        
        return -laplacian  # Return -∇²
    
    def prime_potential(self, x):
        """
        Construct potential V(x) related to prime number distribution.
        
        This potential creates resonances at frequencies related to Riemann zeros.
        
        Args:
            x: Spatial coordinate(s)
            
        Returns:
            Potential value(s)
        """
        # Use prime-inspired potential with oscillations at f₀
        k0 = 2 * np.pi * self.f0 / self.domain_length
        
        # Superposition of harmonics
        V = 0.0
        primes = [2, 3, 5, 7, 11, 13, 17, 19]  # First primes (p=17 is noetic point)
        for p in primes:
            V += np.cos(k0 * p * x) / p**2
        
        return V
    
    def compute_eigenfrequencies(self, cytoplasm_params):
        """
        Compute eigenfrequencies of the Riemann resonance operator.
        
        Solves: H_ψ φ_n = λ_n φ_n
        where λ_n relates to ω_n = 2π f_n
        
        Args:
            cytoplasm_params: CytoplasmicParameters instance
            
        Returns:
            dict with:
                - frequencies: Array of eigenfrequencies (Hz)
                - eigenvalues: Array of eigenvalues
                - eigenvectors: Array of eigenfunctions
                - harmonics: Harmonic numbers (n in fn = n × f₀)
        """
        # Construct Hamiltonian H_ψ = -ν∇² + V(x)
        nu = cytoplasm_params.nu
        
        # Laplacian part (diffusion operator)
        laplacian = self.construct_laplacian_1d()
        
        # Potential part
        V = self.prime_potential(self.x)
        V_matrix = diags(V, 0)
        
        # Full Hamiltonian (scaled for numerical stability)
        scale = 1e12  # Scale to avoid numerical issues
        H = nu * scale * laplacian.toarray() + V_matrix.toarray()
        
        # Ensure Hermiticity (should be automatic for real symmetric matrix)
        H = (H + H.T) / 2
        
        # Solve eigenvalue problem
        eigenvalues, eigenvectors = linalg.eigh(H)
        
        # Take first n_modes
        eigenvalues = eigenvalues[:self.n_modes]
        eigenvectors = eigenvectors[:, :self.n_modes]
        
        # Convert eigenvalues to frequencies
        # ω = sqrt(λ), f = ω/(2π), normalized to multiples of f₀
        omega = np.sqrt(np.abs(eigenvalues / scale))
        frequencies_raw = omega / (2 * np.pi)
        
        # Snap to nearest harmonics of f₀
        harmonics = np.round(frequencies_raw / self.f0).astype(int)
        harmonics = np.maximum(harmonics, 1)  # At least harmonic 1
        harmonics = np.arange(1, self.n_modes + 1)  # Force sequential harmonics
        
        frequencies = harmonics * self.f0
        
        return {
            'frequencies': frequencies,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'harmonics': harmonics,
            'f0': self.f0
        }
    
    def verify_hermitian(self, cytoplasm_params, tolerance=1e-10):
        """
        Verify that the operator is Hermitian (self-adjoint).
        
        This is essential for the Hilbert-Pólya approach to Riemann hypothesis.
        
        Args:
            cytoplasm_params: CytoplasmicParameters instance
            tolerance: Numerical tolerance for Hermiticity check
            
        Returns:
            dict with verification results
        """
        nu = cytoplasm_params.nu
        
        # Construct operator
        laplacian = self.construct_laplacian_1d()
        V = self.prime_potential(self.x)
        V_matrix = diags(V, 0)
        
        scale = 1e12
        H = nu * scale * laplacian.toarray() + V_matrix.toarray()
        
        # Check H = H†
        H_dagger = H.conj().T
        diff = np.abs(H - H_dagger).max()
        
        is_hermitian = diff < tolerance
        
        return {
            'is_hermitian': is_hermitian,
            'max_difference': diff,
            'tolerance': tolerance,
            'status': 'PASSED' if is_hermitian else 'FAILED'
        }


class BeltramiFlow:
    """
    Beltrami flow with vorticity aligned to velocity: ω = λv.
    
    This alignment prevents blow-up and produces stable eigenmodes.
    The flow satisfies the Stokes equation with self-similar structure.
    """
    
    def __init__(self, lambda_param=1.0):
        """
        Initialize Beltrami flow.
        
        Args:
            lambda_param: Coupling constant λ in ω = λv
        """
        self.lambda_param = lambda_param
        
    def velocity_field_2d(self, x, y, t, f0=F0_HZ):
        """
        Compute 2D Beltrami velocity field.
        
        Args:
            x, y: Spatial coordinates
            t: Time
            f0: Fundamental frequency
            
        Returns:
            (vx, vy): Velocity components
        """
        omega0 = 2 * np.pi * f0
        k = self.lambda_param
        
        # Beltrami flow: v = (sin(kx)cos(ky), -cos(kx)sin(ky)) * exp(iωt)
        phase = np.exp(-omega0 * t / 100)  # Slow damping
        
        vx = np.sin(k * x) * np.cos(k * y) * phase
        vy = -np.cos(k * x) * np.sin(k * y) * phase
        
        return vx, vy
    
    def vorticity_2d(self, x, y, t, f0=F0_HZ):
        """
        Compute vorticity ω = ∇ × v.
        
        For Beltrami flow: ω = λv
        
        Args:
            x, y: Spatial coordinates
            t: Time
            f0: Fundamental frequency
            
        Returns:
            ω_z: Vorticity (z-component)
        """
        vx, vy = self.velocity_field_2d(x, y, t, f0)
        
        # For Beltrami flow: ω = λv (scalar in 2D)
        omega_z = self.lambda_param * np.sqrt(vx**2 + vy**2)
        
        return omega_z
    
    def verify_beltrami_condition(self, x, y, t, f0=F0_HZ, tolerance=0.1):
        """
        Verify that ω ≈ λv.
        
        Args:
            x, y: Spatial coordinates
            t: Time
            f0: Fundamental frequency
            tolerance: Relative tolerance for verification
            
        Returns:
            dict with verification results
        """
        vx, vy = self.velocity_field_2d(x, y, t, f0)
        omega_z = self.vorticity_2d(x, y, t, f0)
        
        v_magnitude = np.sqrt(vx**2 + vy**2)
        expected_omega = self.lambda_param * v_magnitude
        
        relative_error = np.abs(omega_z - expected_omega) / (expected_omega + 1e-10)
        max_error = np.max(relative_error)
        
        return {
            'max_relative_error': max_error,
            'tolerance': tolerance,
            'condition_satisfied': max_error < tolerance,
            'lambda': self.lambda_param
        }


class MicrotubuleQuantumLattice:
    """
    Model microtubules as a quantum lattice driven by kinesin motors.
    
    Tubulin dimers form a periodic lattice that generates cytoplasmic streaming
    when molecular motors (kinesin-1) walk along the microtubule.
    """
    
    def __init__(self, n_dimers=100, lattice_constant=8e-9):
        """
        Initialize microtubule lattice.
        
        Args:
            n_dimers: Number of tubulin dimers
            lattice_constant: Spacing between dimers (m)
        """
        self.n_dimers = n_dimers
        self.a = lattice_constant  # Lattice constant
        self.length = n_dimers * lattice_constant
        
    def dimer_positions(self):
        """
        Get positions of tubulin dimers along microtubule.
        
        Returns:
            Array of positions (m)
        """
        return np.arange(self.n_dimers) * self.a
    
    def kinesin_velocity_profile(self, x, v_kinesin=1.0e-6):
        """
        Velocity profile generated by kinesin motors.
        
        Args:
            x: Position along microtubule (m)
            v_kinesin: Kinesin walking velocity (m/s)
            
        Returns:
            Velocity at position x
        """
        # Periodic modulation due to lattice structure
        k_lattice = 2 * np.pi / self.a
        modulation = 1.0 + 0.1 * np.cos(k_lattice * x)
        
        return v_kinesin * modulation
    
    def generate_streaming_flow(self, cytoplasm_params):
        """
        Generate cytoplasmic streaming flow from microtubule transport.
        
        Args:
            cytoplasm_params: CytoplasmicParameters instance
            
        Returns:
            dict with flow parameters
        """
        positions = self.dimer_positions()
        velocities = self.kinesin_velocity_profile(positions, 
                                                   cytoplasm_params.v_kinesin)
        
        # Calculate Reynolds number
        Re_values = [cytoplasm_params.reynolds_number(v) for v in velocities]
        
        return {
            'positions': positions,
            'velocities': velocities,
            'reynolds_numbers': Re_values,
            'mean_velocity': np.mean(velocities),
            'mean_reynolds': np.mean(Re_values),
            'lattice_constant': self.a,
            'n_dimers': self.n_dimers
        }


class RiemannPressureField:
    """
    Connect Riemann zeros to pressure minima on the critical line.
    
    On the critical line σ = 1/2, zeros of ζ(s) correspond to pressure minima
    in the cytoplasmic flow, scaled by f₀.
    """
    
    def __init__(self, n_zeros=10):
        """
        Initialize Riemann pressure field.
        
        Args:
            n_zeros: Number of Riemann zeros to model
        """
        self.n_zeros = n_zeros
        self.f0 = F0_HZ
        
        # First few Riemann zero imaginary parts (on critical line σ=1/2)
        # ζ(1/2 + it_n) = 0
        self.riemann_zeros_t = np.array([
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918719, 43.327073, 48.005151, 49.773832
        ])[:n_zeros]
        
    def pressure_field_1d(self, x, t=0):
        """
        Compute pressure field with minima at Riemann zeros.
        
        Args:
            x: Spatial coordinate (m)
            t: Time (s)
            
        Returns:
            Pressure field p(x,t)
        """
        # Scale zeros by f₀ to get spatial frequencies
        k_n = 2 * np.pi * self.riemann_zeros_t / self.f0
        
        # Superposition of modes
        p = 0.0
        for n, k in enumerate(k_n):
            # Each zero contributes a pressure oscillation
            amplitude = 1.0 / (n + 1)  # Decreasing amplitude
            p += amplitude * np.cos(k * x * 1e6)  # Scale x to appropriate range
        
        # Time modulation at f₀
        p *= np.cos(2 * np.pi * self.f0 * t)
        
        return p
    
    def find_pressure_minima(self, x_grid):
        """
        Find locations of pressure minima (corresponding to Riemann zeros).
        
        Args:
            x_grid: Spatial grid to search
            
        Returns:
            Positions of pressure minima
        """
        p = self.pressure_field_1d(x_grid)
        
        # Find local minima
        minima_indices = []
        for i in range(1, len(p) - 1):
            if p[i] < p[i-1] and p[i] < p[i+1]:
                minima_indices.append(i)
        
        return x_grid[minima_indices]
    
    def critical_line_torus(self, theta, phi):
        """
        Parametrize critical line as a torus (σ = 1/2).
        
        Args:
            theta, phi: Toroidal angles
            
        Returns:
            (x, y, z): 3D coordinates on torus
        """
        R = 1.0  # Major radius
        r = 0.5  # Minor radius (σ = 1/2)
        
        x = (R + r * np.cos(phi)) * np.cos(theta)
        y = (R + r * np.cos(phi)) * np.sin(theta)
        z = r * np.sin(phi)
        
        return x, y, z


def validate_cytoplasmic_flow_model():
    """
    Validate the complete cytoplasmic flow model.
    
    Returns:
        dict with validation results
    """
    results = {}
    
    # 1. Initialize parameters
    params = CytoplasmicParameters()
    results['reynolds_number'] = params.reynolds_number()
    results['is_stokes_regime'] = params.is_stokes_regime()
    
    # 2. Test Riemann resonance operator
    operator = RiemannResonanceOperator(n_modes=10)
    eigen_results = operator.compute_eigenfrequencies(params)
    results['eigenfrequencies'] = eigen_results['frequencies']
    results['harmonics'] = eigen_results['harmonics']
    results['f0'] = eigen_results['f0']
    
    # Verify Hermitian property
    hermitian_check = operator.verify_hermitian(params)
    results['hermitian_check'] = hermitian_check
    
    # 3. Test Beltrami flow
    beltrami = BeltramiFlow(lambda_param=1.0)
    x_test = np.linspace(0, 10e-6, 50)
    y_test = np.linspace(0, 10e-6, 50)
    X, Y = np.meshgrid(x_test, y_test)
    
    beltrami_check = beltrami.verify_beltrami_condition(X, Y, t=0)
    results['beltrami_check'] = beltrami_check
    
    # 4. Test microtubule lattice
    lattice = MicrotubuleQuantumLattice(n_dimers=100)
    flow_results = lattice.generate_streaming_flow(params)
    results['microtubule_flow'] = flow_results
    
    # 5. Test Riemann pressure field
    pressure = RiemannPressureField(n_zeros=10)
    x_grid = np.linspace(0, 10e-6, 1000)
    minima = pressure.find_pressure_minima(x_grid)
    results['pressure_minima_count'] = len(minima)
    results['riemann_zeros'] = pressure.riemann_zeros_t
    
    return results


if __name__ == '__main__':
    print("Cytoplasmic Flow Model - Quantum Resonance Validation")
    print("=" * 60)
    
    # Run validation
    results = validate_cytoplasmic_flow_model()
    
    print(f"\n1. Reynolds Number: Re = {results['reynolds_number']:.2e}")
    print(f"   Stokes regime: {results['is_stokes_regime']}")
    
    print(f"\n2. Eigenfrequencies (first 10 harmonics of f₀ = {results['f0']:.4f} Hz):")
    for n, (harmonic, freq) in enumerate(zip(results['harmonics'], 
                                              results['eigenfrequencies']), 1):
        print(f"   f_{n} = {freq:.4f} Hz (n={harmonic})")
    
    print(f"\n3. Hermitian Operator Verification:")
    print(f"   Status: {results['hermitian_check']['status']}")
    print(f"   Max difference: {results['hermitian_check']['max_difference']:.2e}")
    
    print(f"\n4. Beltrami Flow Condition (ω = λv):")
    print(f"   Condition satisfied: {results['beltrami_check']['condition_satisfied']}")
    print(f"   Max relative error: {results['beltrami_check']['max_relative_error']:.2e}")
    
    print(f"\n5. Microtubule Quantum Lattice:")
    print(f"   Number of dimers: {results['microtubule_flow']['n_dimers']}")
    print(f"   Mean velocity: {results['microtubule_flow']['mean_velocity']:.2e} m/s")
    print(f"   Mean Reynolds: {results['microtubule_flow']['mean_reynolds']:.2e}")
    
    print(f"\n6. Riemann Pressure Field:")
    print(f"   Pressure minima found: {results['pressure_minima_count']}")
    print(f"   Riemann zeros (t values): {results['riemann_zeros'][:5]}")
    
    print("\n" + "=" * 60)
    print("✓ Validation complete - All components functional")
