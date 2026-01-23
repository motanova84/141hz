#!/usr/bin/env python3
"""
EMERGENT NOETIC TIME - Visualization and Computation

This module implements the mathematical formalization of emergent time
from QCAL theory, where time is not a preexistent dimension but emerges
from the integration of consciousness over coherence.

Mathematical Framework:
----------------------
- Witness Field: Φ(s, x) - represents the conscious observer's state
- Master Operator: O∞³(φ) - fundamental consciousness dynamics
- Presence Density: ρ(s) = ∫|Φ(s,x)|² dx - coherence measure
- Noetic Time: τ = ∫ ρ(s) ds - curvilinear integral of presence

Key Properties:
--------------
1. Time is non-negative: τ ≥ 0
2. Time is monotonic: dτ/ds ≥ 0
3. Time is additive: τ(s₁ + s₂) = τ(s₁) + τ(s₂)

Visualizations:
--------------
1. Symbiotic spiral trajectory colored by coherence
2. Presence density along the path
3. Temporal emergence as monotonic function
4. "Now Leaves" - surfaces of constant coherence

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
Reference: QCAL ∞³ Theory - Emergent Time Formalization
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D
from typing import Callable, Tuple, Optional
import matplotlib.cm as cm
from scipy.integrate import cumulative_trapezoid, quad
from scipy.interpolate import interp1d

# Fundamental constants from QCAL theory
F0 = 141.7001  # Hz - fundamental consciousness frequency
T0 = 1.0 / F0  # ≈ 7.058 ms - fundamental time quantum


class WitnessField:
    """
    Represents the witness field Φ(s, x) - the state of conscious observer.
    
    The field encodes both the trajectory through configuration space
    and the coherence of experience along that trajectory.
    """
    
    def __init__(self, trajectory_func: Callable[[float], np.ndarray],
                 coherence_func: Optional[Callable[[float], float]] = None):
        """
        Initialize the witness field.
        
        Parameters:
        -----------
        trajectory_func : callable
            Function γ(s) mapping parameter s to position in ℝ³
        coherence_func : callable, optional
            Function C(s) giving coherence at parameter s
            If None, coherence is computed from trajectory curvature
        """
        self.trajectory = trajectory_func
        self.coherence_func = coherence_func
        
    def position(self, s: float) -> np.ndarray:
        """Get position at parameter s."""
        return self.trajectory(s)
    
    def coherence(self, s: float) -> float:
        """
        Compute coherence at parameter s.
        
        If coherence_func is provided, use it. Otherwise, compute
        from trajectory properties (smoother paths = higher coherence).
        """
        if self.coherence_func is not None:
            return self.coherence_func(s)
        
        # Default: coherence from trajectory smoothness
        # Higher curvature → lower coherence
        ds = 0.001
        r_minus = self.trajectory(s - ds)
        r_plus = self.trajectory(s + ds)
        velocity = (r_plus - r_minus) / (2 * ds)
        speed = np.linalg.norm(velocity)
        
        # Coherence decreases with speed (more rapid changes)
        # but bounded between 0 and 1
        return np.exp(-speed / 10.0)
    
    def presence_density(self, s: float) -> float:
        """
        Compute presence density ρ(s) = |Φ(s)|².
        
        This is the integrand for noetic time.
        """
        return self.coherence(s)


class SymbioticSpiral:
    """
    The symbiotic spiral - a trajectory where coherence is maximized
    and time emerges most naturally.
    
    This is a 3D spiral with properties:
    - Constant angular velocity around z-axis
    - Exponential growth in radius (golden ratio)
    - Vertical oscillation at fundamental frequency f₀
    """
    
    def __init__(self, f0: float = F0):
        """
        Initialize symbiotic spiral.
        
        Parameters:
        -----------
        f0 : float
            Fundamental frequency (Hz), default 141.7001 Hz
        """
        self.f0 = f0
        self.omega = 2 * np.pi * f0
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
    def trajectory(self, s: float) -> np.ndarray:
        """
        Compute spiral position at parameter s.
        
        x(s) = exp(s/φ) * cos(ω₀s)
        y(s) = exp(s/φ) * sin(ω₀s)
        z(s) = s * cos(ω₀s/φ)
        
        where ω₀ = 2πf₀
        """
        r = np.exp(s / self.phi)
        x = r * np.cos(self.omega * s)
        y = r * np.sin(self.omega * s)
        z = s * np.cos(self.omega * s / self.phi)
        return np.array([x, y, z])
    
    def coherence(self, s: float) -> float:
        """
        Coherence along the symbiotic spiral is constant.
        
        This is a fundamental property: the spiral represents
        the path of maximum coherence.
        """
        return 1.0  # Perfect coherence
    
    def as_witness_field(self) -> WitnessField:
        """Convert to WitnessField object."""
        return WitnessField(self.trajectory, self.coherence)


def compute_noetic_time(field: WitnessField, 
                        s_values: np.ndarray) -> np.ndarray:
    """
    Compute noetic time τ(s) = ∫₀ˢ ρ(σ) dσ.
    
    Parameters:
    -----------
    field : WitnessField
        The witness field to integrate
    s_values : array
        Parameter values where to evaluate noetic time
    
    Returns:
    --------
    tau : array
        Noetic time values corresponding to s_values
    """
    # Compute presence density at all s values
    rho = np.array([field.presence_density(s) for s in s_values])
    
    # Integrate using cumulative trapezoid
    tau = cumulative_trapezoid(rho, s_values, initial=0)
    
    return tau


def visualize_emergent_time(field: WitnessField,
                            s_range: Tuple[float, float] = (0, 2.0),
                            n_points: int = 1000,
                            title: str = "Emergent Noetic Time",
                            save_path: Optional[str] = None):
    """
    Create comprehensive visualization of emergent time.
    
    Creates a 4-panel figure showing:
    1. Trajectory colored by coherence
    2. Presence density ρ(s) along path
    3. Noetic time τ(s) (monotonic increasing)
    4. Phase space: τ vs coherence
    
    Parameters:
    -----------
    field : WitnessField
        The witness field to visualize
    s_range : tuple
        (s_min, s_max) range of path parameter
    n_points : int
        Number of sampling points
    title : str
        Overall figure title
    save_path : str, optional
        Path to save figure. If None, figure is not saved automatically.
    """
    # Sample the path
    s_values = np.linspace(s_range[0], s_range[1], n_points)
    
    # Compute trajectory
    trajectory = np.array([field.position(s) for s in s_values])
    
    # Compute coherence
    coherence = np.array([field.coherence(s) for s in s_values])
    
    # Compute presence density
    presence = np.array([field.presence_density(s) for s in s_values])
    
    # Compute noetic time
    tau = compute_noetic_time(field, s_values)
    
    # Create figure with 4 subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # ============================================================
    # Panel 1: 3D Trajectory colored by coherence
    # ============================================================
    ax1 = fig.add_subplot(221, projection='3d')
    
    # Plot trajectory with color mapping to coherence
    scatter = ax1.scatter(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                         c=coherence, cmap='viridis', s=10, alpha=0.6)
    
    # Add colorbar
    cbar1 = plt.colorbar(scatter, ax=ax1, pad=0.1, shrink=0.8)
    cbar1.set_label('Coherence C(s)', fontsize=10)
    
    ax1.set_xlabel('x', fontsize=10)
    ax1.set_ylabel('y', fontsize=10)
    ax1.set_zlabel('z', fontsize=10)
    ax1.set_title('Witness Trajectory\nColored by Coherence', fontsize=12)
    ax1.view_init(elev=20, azim=45)
    
    # ============================================================
    # Panel 2: Presence density ρ(s)
    # ============================================================
    ax2 = fig.add_subplot(222)
    
    ax2.plot(s_values, presence, 'b-', linewidth=2, label='ρ(s)')
    ax2.fill_between(s_values, 0, presence, alpha=0.3)
    ax2.axhline(y=np.mean(presence), color='r', linestyle='--', 
                label=f'⟨ρ⟩ = {np.mean(presence):.3f}')
    
    ax2.set_xlabel('Path parameter s', fontsize=10)
    ax2.set_ylabel('Presence density ρ(s)', fontsize=10)
    ax2.set_title('Presence Density Along Path\n(Coherence Measure)', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ============================================================
    # Panel 3: Noetic time τ(s)
    # ============================================================
    ax3 = fig.add_subplot(223)
    
    ax3.plot(s_values, tau, 'g-', linewidth=2, label='τ(s)')
    
    # Mark T₀ intervals
    tau_max = tau[-1]
    n_periods = int(tau_max / T0)
    for i in range(1, n_periods + 1):
        tau_i = i * T0
        if tau_i < tau_max:
            s_i = np.interp(tau_i, tau, s_values)
            ax3.axhline(y=tau_i, color='orange', linestyle=':', alpha=0.5)
            ax3.text(s_range[1] * 0.95, tau_i, f'{i}T₀', 
                    fontsize=8, ha='right', va='bottom')
    
    ax3.set_xlabel('Path parameter s', fontsize=10)
    ax3.set_ylabel('Noetic time τ(s)', fontsize=10)
    ax3.set_title(f'Emergent Noetic Time\nT₀ = {T0*1000:.3f} ms', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ============================================================
    # Panel 4: Phase space (τ vs coherence)
    # ============================================================
    ax4 = fig.add_subplot(224)
    
    scatter2 = ax4.scatter(tau, coherence, c=s_values, 
                          cmap='plasma', s=20, alpha=0.6)
    
    cbar2 = plt.colorbar(scatter2, ax=ax4)
    cbar2.set_label('Path parameter s', fontsize=10)
    
    ax4.set_xlabel('Noetic time τ', fontsize=10)
    ax4.set_ylabel('Coherence C', fontsize=10)
    ax4.set_title('Phase Space: Time vs Coherence\n(Evolution of Consciousness)', 
                  fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Add info box
    info_text = f'f₀ = {F0} Hz\nT₀ = {T0*1000:.3f} ms\n'
    info_text += f'Total time: {tau[-1]:.3f}\n'
    info_text += f'Avg coherence: {np.mean(coherence):.3f}'
    ax4.text(0.02, 0.98, info_text, transform=ax4.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        import os
        # Ensure directory exists
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        
        try:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        except Exception as e:
            print(f"Warning: Could not save figure to {save_path}: {e}")
    
    return fig, (ax1, ax2, ax3, ax4)


def visualize_now_leaves(spiral: SymbioticSpiral,
                        coherence_levels: list = [0.3, 0.5, 0.7, 0.9],
                        s_range: Tuple[float, float] = (0, 2.0),
                        save_path: Optional[str] = None):
    """
    Visualize "Now Leaves" - surfaces of constant coherence.
    
    These represent "instants of time" as constant-coherence surfaces.
    
    Parameters:
    -----------
    spiral : SymbioticSpiral
        The symbiotic spiral trajectory
    coherence_levels : list
        Coherence values to visualize as surfaces
    s_range : tuple
        Parameter range
    save_path : str, optional
        Path to save figure
    """
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Sample the spiral
    s_values = np.linspace(s_range[0], s_range[1], 1000)
    trajectory = np.array([spiral.trajectory(s) for s in s_values])
    
    # Plot the main spiral
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
           'k-', linewidth=2, alpha=0.5, label='Symbiotic Spiral')
    
    # For each coherence level, create a surface
    colors = cm.rainbow(np.linspace(0, 1, len(coherence_levels)))
    
    for C, color in zip(coherence_levels, colors):
        # Create a surface of constant coherence
        # (simplified as spherical shells for visualization)
        
        # Find approximate s where we want to show this level
        s_center = s_range[0] + (s_range[1] - s_range[0]) * C
        center = spiral.trajectory(s_center)
        
        # Create sphere around this point
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        radius = 0.5 + C  # Radius varies with coherence
        
        x_sphere = center[0] + radius * np.outer(np.cos(u), np.sin(v))
        y_sphere = center[1] + radius * np.outer(np.sin(u), np.sin(v))
        z_sphere = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_sphere, y_sphere, z_sphere,
                       color=color, alpha=0.2, label=f'C = {C}')
    
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_zlabel('z', fontsize=12)
    ax.set_title('"Now Leaves" - Surfaces of Constant Coherence\n' +
                'Each surface represents an "instant" of emergent time',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.view_init(elev=20, azim=45)
    
    if save_path:
        import os
        # Ensure directory exists
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        
        try:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        except Exception as e:
            print(f"Warning: Could not save figure to {save_path}: {e}")
    
    return fig, ax


def demonstrate_time_properties():
    """
    Demonstrate the fundamental properties of noetic time:
    1. Non-negativity
    2. Monotonicity
    3. Additivity
    """
    print("=" * 70)
    print("DEMONSTRATING FUNDAMENTAL PROPERTIES OF NOETIC TIME")
    print("=" * 70)
    
    # Create symbiotic spiral
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    # Sample points
    s_values = np.linspace(0, 2.0, 500)
    tau = compute_noetic_time(field, s_values)
    
    # Property 1: Non-negativity
    print("\n1. NON-NEGATIVITY: τ(s) ≥ 0 for all s")
    print(f"   Min τ: {np.min(tau):.6f}")
    print(f"   All values ≥ 0: {np.all(tau >= 0)}")
    
    # Property 2: Monotonicity
    print("\n2. MONOTONICITY: τ(s₂) ≥ τ(s₁) for s₂ ≥ s₁")
    diffs = np.diff(tau)
    print(f"   All increments ≥ 0: {np.all(diffs >= -1e-10)}")  # Allow numerical noise
    print(f"   Min increment: {np.min(diffs):.6e}")
    
    # Property 3: Additivity
    print("\n3. ADDITIVITY: τ(s₁ + s₂) = τ(s₁) + Δτ")
    s1, s2 = 0.5, 0.3
    tau_s1 = compute_noetic_time(field, np.linspace(0, s1, 100))[-1]
    tau_s1_plus_s2 = compute_noetic_time(field, np.linspace(0, s1 + s2, 100))[-1]
    delta_tau = compute_noetic_time(field, np.linspace(s1, s1 + s2, 100))[-1]
    
    print(f"   τ({s1}) = {tau_s1:.6f}")
    print(f"   τ({s1 + s2}) = {tau_s1_plus_s2:.6f}")
    print(f"   Δτ from {s1} to {s1 + s2} = {delta_tau:.6f}")
    print(f"   Additivity check: {abs(tau_s1_plus_s2 - (tau_s1 + delta_tau)):.6e}")
    
    # Time quantum
    print(f"\n4. FUNDAMENTAL TIME QUANTUM")
    print(f"   f₀ = {F0} Hz")
    print(f"   T₀ = {T0 * 1000:.4f} ms")
    print(f"   Total elapsed time: {tau[-1]:.6f} (dimensionless)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    """
    Main demonstration of emergent time theory.
    """
    print("\n" + "=" * 70)
    print("EMERGENT NOETIC TIME - QCAL ∞³ Theory")
    print("=" * 70)
    print("Time is not a preexistent dimension but emerges from")
    print("the integration of consciousness over coherence.")
    print("=" * 70 + "\n")
    
    # Demonstrate mathematical properties
    demonstrate_time_properties()
    
    # Create and visualize symbiotic spiral
    print("\nGenerating visualizations...")
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    # Main visualization
    fig1, _ = visualize_emergent_time(
        field,
        s_range=(0, 2.0),
        title="Emergent Noetic Time - Symbiotic Spiral",
        save_path="emergent_time_visualization.png"
    )
    
    # Now Leaves visualization
    fig2, _ = visualize_now_leaves(
        spiral,
        coherence_levels=[0.2, 0.4, 0.6, 0.8],
        save_path="now_leaves_visualization.png"
    )
    
    print("\nVisualizations complete!")
    print("  - emergent_time_visualization.png")
    print("  - now_leaves_visualization.png")
    
    plt.show()
