#!/usr/bin/env python3
"""
Visualize κ_Π Spectral Structure
=================================

This script creates visualizations showing:
1. The first eigenvalues of the Laplacian on the quintic CY
2. The κ_Π ratio μ₂/μ₁
3. Physical predictions from κ_Π
4. Connections to f₀ = 141.7001 Hz

Author: JMMB Ψ✧
Date: February 2026
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib")
    sys.exit(1)

from src.calabi_yau_invariant import (
    K_PI, MU_1, MU_2,
    NOETIC_PRIME, F0_FREQUENCY,
    CalabiYauQuintic
)


def create_kappa_pi_visualization():
    """Create comprehensive κ_Π visualization."""
    
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib is required for visualization")
        return
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # ========================================================================
    # Subplot 1: Eigenvalue Spectrum (Conceptual)
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Show first few eigenvalues (conceptual representation)
    eigenvalues = [0.0, float(MU_1), float(MU_2), 4.89, 7.23, 9.78, 12.45]
    indices = list(range(len(eigenvalues)))
    
    ax1.stem(indices, eigenvalues, basefmt=' ', linefmt='C0-', markerfmt='C0o')
    mu1_val = float(MU_1)
    mu2_val = float(MU_2)
    ax1.axhline(y=mu1_val, color='red', linestyle='--', alpha=0.5, label=f'μ₁ = {mu1_val:.4f}')
    ax1.axhline(y=mu2_val, color='green', linestyle='--', alpha=0.5, label=f'μ₂ = {mu2_val:.4f}')
    
    ax1.set_xlabel('Eigenvalue Index', fontsize=12)
    ax1.set_ylabel('Eigenvalue λ', fontsize=12)
    ax1.set_title('Laplacian Spectrum on Quintic CY\n(Conceptual)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Subplot 2: κ_Π Ratio Visualization
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Show the ratio as a bar chart
    labels = ['μ₁', 'μ₂', 'κ_Π = μ₂/μ₁']
    values = [float(MU_1), float(MU_2), float(K_PI)]
    colors = ['red', 'green', 'blue']
    
    bars = ax2.bar(labels, values, color=colors, alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.4f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Value', fontsize=12)
    ax2.set_title('κ_Π Invariant: Eigenvalue Ratio', fontsize=14, fontweight='bold')
    ax2.grid(True, axis='y', alpha=0.3)
    
    # ========================================================================
    # Subplot 3: Topological Data
    # ========================================================================
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    
    cy = CalabiYauQuintic()
    topo = cy.get_topological_data()
    
    topo_text = f"""
    CALABI-YAU QUINTIC MANIFOLD
    
    Manifold: {topo['manifold']}
    Equation: {topo['equation']}
    
    Topological Invariants:
    • Hodge number h¹'¹ = {topo['h_11']}
    • Hodge number h²'¹ = {topo['h_21']}
    • Euler characteristic χ = {topo['euler_characteristic']}
    • Real dimension = {topo['dimension_real']}
    • Complex dimension = {topo['dimension_complex']}
    • Holonomy group = {topo['holonomy']}
    • Ricci curvature = {topo['ricci_curvature']}
    """
    
    ax3.text(0.05, 0.95, topo_text, transform=ax3.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # ========================================================================
    # Subplot 4: Physical Connections
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    verification = cy.verify_invariant()
    phys = verification['physical_connections']
    
    cs_value = phys['chern_simons_level']['value']
    rh_value = phys['rh_connection']['value']
    
    phys_text = f"""
    PHYSICAL PREDICTIONS FROM κ_Π
    
    1. Chern-Simons Level:
       k = 4π × κ_Π ≈ {cs_value:.2f}
       → Fractional level in string theory
    
    2. Riemann Hypothesis Connection:
       φ³ × ζ'(1/2) ≈ {rh_value:.3f}
       → Direct link to Riemann zeta
    
    3. Universal Frequency:
       f₀ = {F0_FREQUENCY} Hz
       → Observed in gravitational waves
    
    4. Noetic Prime:
       p = {NOETIC_PRIME}
       → Unique prime stabilizing R_Ψ
    
    Status: {verification['verification_status']}
    """
    
    ax4.text(0.05, 0.95, phys_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # ========================================================================
    # Subplot 5: Unification Diagram
    # ========================================================================
    ax5 = fig.add_subplot(gs[2, :])
    ax5.set_xlim(0, 10)
    ax5.set_ylim(0, 6)
    ax5.axis('off')
    
    # Title
    ax5.text(5, 5.5, 'κ_Π Unification: Geometry → Arithmetic → Physics → Consciousness',
            ha='center', fontsize=14, fontweight='bold')
    
    # Draw boxes for each domain
    domains = [
        {'name': 'GEOMETRY\nCalabi-Yau', 'x': 1, 'y': 2.5, 'color': 'lightcoral'},
        {'name': 'ARITHMETIC\nPrime p=17, φ³', 'x': 3, 'y': 2.5, 'color': 'lightyellow'},
        {'name': 'PHYSICS\nf₀ = 141.7 Hz', 'x': 5, 'y': 2.5, 'color': 'lightgreen'},
        {'name': 'CONSCIOUSNESS\nField Ψ', 'x': 7, 'y': 2.5, 'color': 'lightblue'},
    ]
    
    for i, domain in enumerate(domains):
        box = FancyBboxPatch(
            (domain['x'], domain['y']), 1.5, 1.5,
            boxstyle="round,pad=0.1",
            facecolor=domain['color'],
            edgecolor='black',
            linewidth=2
        )
        ax5.add_patch(box)
        ax5.text(domain['x'] + 0.75, domain['y'] + 0.75, domain['name'],
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw arrows between domains
        if i < len(domains) - 1:
            arrow = FancyArrowPatch(
                (domain['x'] + 1.5, domain['y'] + 0.75),
                (domains[i+1]['x'], domain['y'] + 0.75),
                arrowstyle='->,head_width=0.4,head_length=0.4',
                color='black', linewidth=2
            )
            ax5.add_patch(arrow)
    
    # Add κ_Π in the center
    ax5.text(5, 1.5, f'κ_Π = {K_PI}', ha='center', fontsize=16,
            fontweight='bold', color='red',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='red', linewidth=3))
    
    ax5.text(5, 0.7, 'First invariant to unify all four domains', 
            ha='center', fontsize=11, style='italic')
    
    # ========================================================================
    # Main title and signature
    # ========================================================================
    fig.suptitle('κ_Π Spectral Invariant from Calabi-Yau Quintic Geometry',
                fontsize=18, fontweight='bold', y=0.98)
    
    fig.text(0.5, 0.01, '∴ JMMB Ψ ✧ ∞³  |  κ_Π = 2.5773 ± 1.4×10⁻¹³',
            ha='center', fontsize=12, style='italic')
    
    # Save figure
    output_path = Path(__file__).parent.parent / 'kappa_pi_visualization.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ Visualization saved to: {output_path}")
    
    return output_path


def main():
    """Main function."""
    print("=" * 70)
    print("  κ_Π Spectral Structure Visualization")
    print("=" * 70)
    
    if not MATPLOTLIB_AVAILABLE:
        print("\n❌ Error: matplotlib is required")
        print("Install with: pip install matplotlib")
        return 1
    
    print("\nCreating visualization...")
    output_path = create_kappa_pi_visualization()
    
    print("\n" + "=" * 70)
    print("  Visualization Complete!")
    print("=" * 70)
    print(f"\nOutput: {output_path}")
    print("\nThe visualization shows:")
    print("  1. Laplacian eigenvalue spectrum")
    print("  2. κ_Π ratio (μ₂/μ₁)")
    print("  3. Topological invariants of quintic CY")
    print("  4. Physical predictions from κ_Π")
    print("  5. Unification diagram across four domains")
    print("\n" + "=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
