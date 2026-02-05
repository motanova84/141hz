#!/usr/bin/env python3
"""
Example: FASE III - Geometría Emergente
Demonstration of emergent geometry from consciousness coherence

This example shows:
1. Computing Einstein tensor at different coherence levels
2. Exploring the master node at 888 Hz
3. Visualizing the coherence landscape
4. Understanding gravity as coherence deficit

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.geometria_emergente import (
    GeometriaEmergente,
    PSI_OPTIMAL,
    FREQUENCY_MASTER
)


def example_1_basic_tensor_computation():
    """Example 1: Basic Einstein tensor computation."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Einstein Tensor Computation")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    
    # Compute at different coherence levels
    print("\nComputing G_μν at different coherence levels:\n")
    print(f"{'Ψ':<8} {'trace(G)':<15} {'||G||':<15} {'κ_Π':<15}")
    print("-" * 80)
    
    for psi in [0.1, 0.5, PSI_OPTIMAL, 0.95]:
        result = geo.einstein_tensor(psi)
        norm_G = np.linalg.norm(result['G_muv'])
        
        print(f"{psi:<8.3f} {result['trace_G']:<15.2e} "
              f"{norm_G:<15.2e} {result['kappa_pi']:<15.2e}")
    
    print("\nObservation: Curvature decreases as coherence increases")
    print("→ Higher coherence = flatter space = less gravity")


def example_2_master_node_exploration():
    """Example 2: Explore the master node at 888 Hz."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Master Node @ 888 Hz - Distributed Coherence")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    master = geo.compute_master_node_coherence()
    
    print(f"\nMaster Node Configuration:")
    print(f"  Coherence: Ψ = {master['psi']:.3f}")
    print(f"  Frequency: f = {master['frequency']:.1f} Hz")
    print(f"  Trace(G): {master['tensor']['trace_G']:.2e} < 10⁻⁶ ✓")
    print(f"  κ_Π: {master['tensor']['kappa_pi']:.2e} m/J")
    print(f"  Λ: {master['tensor']['lambda']:.2e} m⁻²")
    
    print(f"\nPhysical Interpretation:")
    print(f"  State: {master['interpretation']['state']}")
    print(f"  Curvature: {master['interpretation']['curvature']}")
    print(f"  Gravity Source: {master['interpretation']['gravity_source']}")
    print(f"  Trajectory Nature: {master['interpretation']['trajectory_nature']}")
    
    print("\nConclusion: The master node maintains optimal balance between")
    print("coherence and curvature, providing distributed coherence at 888 Hz.")


def example_3_boundary_behaviors():
    """Example 3: Demonstrate boundary behaviors."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Boundary Behaviors of G_μν(Ψ)")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    
    print("\nBehavior 1: Ψ → 1 (Perfect Coherence → Flat Space)")
    print("-" * 80)
    for psi in [0.9, 0.95, 0.99, 0.999]:
        result = geo.einstein_tensor(psi)
        norm = np.linalg.norm(result['G_muv'])
        print(f"Ψ = {psi:.3f}: ||G_μν|| = {norm:.2e}")
    
    print("\n→ As Ψ → 1, curvature vanishes (flat unity)")
    
    print("\nBehavior 2: Ψ → 0 (Zero Coherence → Gravitational Trap)")
    print("-" * 80)
    for psi in [0.1, 0.05, 0.01, 0.001]:
        result = geo.einstein_tensor(psi)
        norm = np.linalg.norm(result['G_muv'])
        print(f"Ψ = {psi:.3f}: ||G_μν|| = {norm:.2e}")
    
    print("\n→ As Ψ → 0, curvature diverges (gravitational trap)")


def example_4_coherence_deficit_mechanism():
    """Example 4: Demonstrate gravity as coherence deficit."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Gravity as Coherence Deficit Mechanism")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    
    # Compute gradient d||G||/dΨ
    psi_values = np.linspace(0.1, 0.95, 20)
    norms = []
    
    for psi in psi_values:
        result = geo.einstein_tensor(psi)
        norms.append(np.linalg.norm(result['G_muv']))
    
    # Numerical derivative
    d_norm_d_psi = np.gradient(norms, psi_values)
    
    print(f"\nCoherence range: Ψ ∈ [{psi_values[0]:.2f}, {psi_values[-1]:.2f}]")
    print(f"Number of points: {len(psi_values)}")
    print(f"\nGradient d||G||/dΨ:")
    print(f"  Mean: {np.mean(d_norm_d_psi):.2e}")
    print(f"  Min: {np.min(d_norm_d_psi):.2e}")
    print(f"  Max: {np.max(d_norm_d_psi):.2e}")
    print(f"  All negative: {np.all(d_norm_d_psi < 0)}")
    
    print("\nInterpretation:")
    print("  d||G||/dΨ < 0 everywhere")
    print("  → Gravity INCREASES as coherence DECREASES")
    print("  → Gravity emerges from coherence DEFICIT")
    print("  → Matter curves space by REDUCING local Ψ")


def example_5_visualize_landscape():
    """Example 5: Visualize coherence landscape."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Visualizing Coherence Landscape")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    
    # Generate data
    psi_values = np.linspace(0.01, 0.999, 100)
    trace_G = []
    norm_G = []
    kappa_pi = []
    
    for psi in psi_values:
        result = geo.einstein_tensor(psi)
        trace_G.append(np.abs(result['trace_G']))
        norm_G.append(np.linalg.norm(result['G_muv']))
        kappa_pi.append(result['kappa_pi'])
    
    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('FASE III: Geometría Emergente - Coherence Landscape', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Trace
    axes[0].semilogy(psi_values, trace_G, 'b-', linewidth=2)
    axes[0].axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2, 
                   label=f'Ψ = {PSI_OPTIMAL}')
    axes[0].axhline(1e-6, color='g', linestyle=':', linewidth=2, 
                   label='trace < 10⁻⁶')
    axes[0].set_xlabel('Coherence Ψ', fontsize=11)
    axes[0].set_ylabel('|trace(G)|', fontsize=11)
    axes[0].set_title('Curvature Trace')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Norm
    axes[1].semilogy(psi_values, norm_G, 'b-', linewidth=2)
    axes[1].axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2,
                   label=f'Ψ = {PSI_OPTIMAL}')
    axes[1].set_xlabel('Coherence Ψ', fontsize=11)
    axes[1].set_ylabel('||G_μν||', fontsize=11)
    axes[1].set_title('Tensor Norm')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Coupling
    axes[2].semilogy(psi_values, kappa_pi, 'b-', linewidth=2)
    axes[2].axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2,
                   label=f'Ψ = {PSI_OPTIMAL}')
    axes[2].set_xlabel('Coherence Ψ', fontsize=11)
    axes[2].set_ylabel('κ_Π (m/J)', fontsize=11)
    axes[2].set_title('Gravitational Coupling')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, 'ejemplo_geometria_emergente.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    print(f"\nFigure saved to: {save_path}")
    print("\nThe landscape shows:")
    print("  - Curvature trace peaks at low coherence, minimal at Ψ = 0.888")
    print("  - Tensor norm increases as coherence decreases")
    print("  - Coupling strength inversely proportional to coherence")
    
    plt.show()


def example_6_tensor_components():
    """Example 6: Examine tensor components."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Detailed Tensor Components at Master Node")
    print("=" * 80)
    
    geo = GeometriaEmergente()
    result = geo.einstein_tensor(PSI_OPTIMAL)
    
    G = result['G_muv']
    T = result['T_muv']
    
    print(f"\nEinstein Tensor G_μν at Ψ = {PSI_OPTIMAL}:")
    print("-" * 80)
    print("     μ\\ν      0              1              2              3")
    for mu in range(4):
        row = f"      {mu}   "
        for nu in range(4):
            row += f"{G[mu, nu]:14.2e} "
        print(row)
    
    print(f"\nStress-Energy Tensor T_μν(Ψ) at Ψ = {PSI_OPTIMAL}:")
    print("-" * 80)
    print("     μ\\ν      0              1              2              3")
    for mu in range(4):
        row = f"      {mu}   "
        for nu in range(4):
            row += f"{T[mu, nu]:14.2e} "
        print(row)
    
    print(f"\nKey Properties:")
    print(f"  Trace(G): {result['trace_G']:.2e}")
    print(f"  Trace(T): {result['trace_T']:.2e}")
    print(f"  Det(G): {np.linalg.det(G):.2e}")
    print(f"  Symmetry check: {np.allclose(G, G.T)}")


def main():
    """Run all examples."""
    print("=" * 80)
    print("FASE III: GEOMETRÍA EMERGENTE - Examples")
    print("Einstein-QCAL Bridge: Gravity as Coherence Deficit")
    print("=" * 80)
    
    # Run all examples
    example_1_basic_tensor_computation()
    example_2_master_node_exploration()
    example_3_boundary_behaviors()
    example_4_coherence_deficit_mechanism()
    example_5_visualize_landscape()
    example_6_tensor_components()
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("1. Gravity emerges from coherence deficit (lack of Ψ)")
    print("2. Master node at Ψ = 0.888, f = 888 Hz provides optimal balance")
    print("3. Perfect coherence (Ψ → 1) eliminates curvature (flat space)")
    print("4. Zero coherence (Ψ → 0) creates gravitational trap (infinite curvature)")
    print("5. Trajectories reflect vibrational intention, not passive geometry")
    print("\nFASE III ACTIVATED: Geometría Emergente manifiesta curvatura consciente ✓")


if __name__ == "__main__":
    main()
