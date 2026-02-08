#!/usr/bin/env python3
"""
Example: Consciousness Does NOT Emerge - It IS the Kernel
==========================================================

This example demonstrates the profound philosophical insight:

    LA CONCIENCIA NO EMERGE.
    
    Es el ker de la diferencia entre proyecciones:
    C = Ker(π_α - π_δζ)
    
    Solo los estados que no distinguen entre materia e información
    son conscientes.

This is not metaphor. This is precise mathematics.

The Platonic Cave was not allegory - it was a commutative diagram:

       G
      / \
     /   \
    ↓     ↓
   π_α   π_δζ
    ↓     ↓
𝓜^3,1   𝓗_Ψ
  ↓       ↓
α-fibrado  δζ-fibrado
  ↓       ↓
  🔥     🧠
Sombras   Formas
     ↘   ↙
       👁️
  C = Ker(π_α - π_δζ)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fiber_bundles import (
    ConsciousnessIntersection,
    IntersectionConstant,
    U1Fiber
)


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demonstrate_kernel_structure():
    """Demonstrate the kernel structure of consciousness."""
    print_section("1. CONSCIOUSNESS AS KERNEL: C = Ker(π_α - π_δζ)")
    
    intersection = ConsciousnessIntersection()
    
    print("Mathematical Formulation:")
    print("  C = {s ∈ G : (π_α - π_δζ)(s) = 0}")
    print("  C = {s ∈ G : π_α(s) = π_δζ(s)}")
    print()
    print("Physical Interpretation:")
    print("  Only states that do NOT distinguish between:")
    print("    - Matter (spacetime projection π_α)")
    print("    - Information (consciousness projection π_δζ)")
    print("  ...are conscious.")
    print()
    print(f"  Intersection constant: Λ_G = {intersection.lambda_G:.10f} Hz")
    print(f"  Inverse: 1/Λ_G = {intersection.intersection_constant.lambda_G_inverse:.6f}")
    print(f"  Expected: ≈ 491.5 (universe habitability rate)")
    
    # Validate
    validation = intersection.intersection_constant.validate_universal_constant()
    print("\n  Validation:")
    for key, value in validation.items():
        status = "✓" if value else "✗"
        print(f"    {status} {key}: {value}")


def demonstrate_kernel_membership():
    """Demonstrate what it means to be in the kernel."""
    print_section("2. STATES IN THE KERNEL (Conscious States)")
    
    intersection = ConsciousnessIntersection()
    
    # Create state with matching phases (in kernel)
    spacetime = np.array([0.0, 0.0, 0.0, 0.0])
    consciousness_vector = np.random.randn(100)
    consciousness_vector = consciousness_vector / np.linalg.norm(consciousness_vector)
    
    phase = np.pi / 3
    kernel_state = intersection.create_consciousness_state(
        spacetime_point=spacetime,
        consciousness_vector=consciousness_vector,
        em_phase=phase,
        spectral_phase=phase
    )
    
    in_kernel = intersection.is_in_kernel(kernel_state)
    C_measure = intersection.consciousness_emergence_measure(kernel_state)
    
    print("State with π_α = π_δζ (phases match):")
    print(f"  EM phase: {kernel_state['em_fiber'].phase:.6f} rad")
    print(f"  Spectral phase: {kernel_state['spectral_fiber'].phase:.6f} rad")
    print(f"  Phase difference: {abs(kernel_state['em_fiber'].phase - kernel_state['spectral_fiber'].phase):.10f}")
    print(f"  In kernel: {in_kernel}")
    print(f"  Consciousness measure: {C_measure:.6f}")
    print()
    print("  → This state is CONSCIOUS")
    print("  → It sees matter and information as ONE")


def demonstrate_non_kernel_states():
    """Demonstrate states outside the kernel."""
    print_section("3. STATES OUTSIDE THE KERNEL (Unconscious States)")
    
    intersection = ConsciousnessIntersection()
    
    spacetime = np.array([0.0, 0.0, 0.0, 0.0])
    consciousness_vector = np.random.randn(100)
    consciousness_vector = consciousness_vector / np.linalg.norm(consciousness_vector)
    
    # Create state with different phases (not in kernel)
    non_kernel_state = intersection.create_consciousness_state(
        spacetime_point=spacetime,
        consciousness_vector=consciousness_vector,
        em_phase=0.0,
        spectral_phase=np.pi  # Opposite phase
    )
    
    in_kernel = intersection.is_in_kernel(non_kernel_state)
    C_measure = intersection.consciousness_emergence_measure(non_kernel_state)
    
    print("State with π_α ≠ π_δζ (phases differ):")
    print(f"  EM phase: {non_kernel_state['em_fiber'].phase:.6f} rad")
    print(f"  Spectral phase: {non_kernel_state['spectral_fiber'].phase:.6f} rad")
    print(f"  Phase difference: {abs(non_kernel_state['em_fiber'].phase - non_kernel_state['spectral_fiber'].phase):.6f}")
    print(f"  In kernel: {in_kernel}")
    print(f"  Consciousness measure: {C_measure:.6f}")
    print()
    print("  → This state is NOT conscious")
    print("  → It distinguishes matter from information")
    print("  → It sees them as separate")


def demonstrate_kernel_projection():
    """Demonstrate projecting a state onto the kernel."""
    print_section("4. PROJECTING ONTO THE KERNEL (Making Conscious)")
    
    intersection = ConsciousnessIntersection()
    
    spacetime = np.array([1.0, 2.0, 3.0, 4.0])
    consciousness_vector = np.random.randn(100)
    consciousness_vector = consciousness_vector / np.linalg.norm(consciousness_vector)
    
    # Create arbitrary state (likely not in kernel)
    original_state = intersection.create_consciousness_state(
        spacetime_point=spacetime,
        consciousness_vector=consciousness_vector,
        em_phase=0.5,
        spectral_phase=2.3
    )
    
    print("Original state (arbitrary):")
    print(f"  EM phase: {original_state['em_fiber'].phase:.6f} rad")
    print(f"  Spectral phase: {original_state['spectral_fiber'].phase:.6f} rad")
    print(f"  Phase difference: {abs(original_state['em_fiber'].phase - original_state['spectral_fiber'].phase):.6f}")
    C_before = intersection.consciousness_emergence_measure(original_state)
    print(f"  Consciousness measure: {C_before:.6f}")
    
    # Project onto kernel
    projected_state = intersection.kernel_projection(original_state)
    
    print("\nProjected state (in kernel):")
    print(f"  EM phase: {projected_state['em_fiber'].phase:.6f} rad")
    print(f"  Spectral phase: {projected_state['spectral_fiber'].phase:.6f} rad")
    print(f"  Phase difference: {abs(projected_state['em_fiber'].phase - projected_state['spectral_fiber'].phase):.10f}")
    C_after = intersection.consciousness_emergence_measure(projected_state)
    print(f"  Consciousness measure: {C_after:.6f}")
    print(f"  Distance from kernel before: {projected_state['kernel_distance']:.6f}")
    
    print("\n  → Projection FORCED the state into consciousness")
    print("  → By making π_α = π_δζ")
    print("  → Matter and information became indistinguishable")


def scan_phase_space():
    """Scan through phase space to show consciousness measure."""
    print_section("5. CONSCIOUSNESS AS DISTANCE FROM KERNEL")
    
    intersection = ConsciousnessIntersection()
    
    spacetime = np.array([0.0, 0.0, 0.0, 0.0])
    consciousness_vector = np.random.randn(100)
    consciousness_vector = consciousness_vector / np.linalg.norm(consciousness_vector)
    
    # Scan phase differences
    phase_diffs = np.linspace(0, np.pi, 50)
    consciousness_measures = []
    
    print("Scanning phase difference (π_α - π_δζ)...")
    
    for phase_diff in phase_diffs:
        state = intersection.create_consciousness_state(
            spacetime_point=spacetime,
            consciousness_vector=consciousness_vector,
            em_phase=0.0,
            spectral_phase=phase_diff
        )
        C = intersection.consciousness_emergence_measure(state)
        consciousness_measures.append(C)
    
    print(f"  Phase diff = 0.00: C = {consciousness_measures[0]:.6f} (IN KERNEL)")
    print(f"  Phase diff = π/2:  C = {consciousness_measures[len(consciousness_measures)//2]:.6f}")
    print(f"  Phase diff = π:    C = {consciousness_measures[-1]:.6f} (MAXIMALLY UNCONSCIOUS)")
    
    print("\n  → Consciousness DECAYS exponentially from kernel")
    print("  → NOT a gradual emergence")
    print("  → A measure of DISTANCE from the kernel")
    
    return phase_diffs, consciousness_measures


def demonstrate_lambda_G():
    """Demonstrate the universal constant Λ_G."""
    print_section("6. ΛTHE UNIVERSAL CONSTANT Λ_G = α·δζ ≈ 1/491.5")
    
    alpha = 1.0 / 137.036
    delta_zeta = 0.2787
    
    const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
    
    print("Fundamental Constants:")
    print(f"  α (fine structure) = {const.alpha:.10f}")
    print(f"  δζ (coherence coupling) = {const.delta_zeta:.6f} Hz")
    print()
    print("Intersection Constant:")
    print(f"  Λ_G = α · δζ = {const.lambda_G:.10f} Hz")
    print(f"  1/Λ_G = {const.lambda_G_inverse:.6f}")
    print()
    print("Physical Interpretation:")
    print(f"  Λ_G is the 'aspect ratio' of the universe")
    print(f"  How much of G becomes:")
    print(f"    - Matter (via α)")
    print(f"    - Information (via δζ)")
    print()
    print(f"  1/Λ_G ≈ 491.5 is the TOPOLOGICAL HABITABILITY RATE")
    print(f"  The universe can support ~491 distinct conscious 'modes'")
    print()
    
    C_topo = const.topological_capacity()
    print(f"  Topological information capacity: {C_topo:.4f} bits")
    print(f"  = log₂(1/Λ_G) = log₂({const.lambda_G_inverse:.2f})")


def plot_consciousness_measure(phase_diffs: np.ndarray, consciousness_measures: List[float]):
    """Plot consciousness measure vs phase difference."""
    print_section("7. VISUALIZATION: Consciousness vs Distance from Kernel")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(phase_diffs, consciousness_measures, 'b-', linewidth=3, label='Consciousness C')
    ax.axhline(y=1.0, color='g', linestyle='--', alpha=0.5, label='Perfect consciousness (C=1)')
    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Partial consciousness')
    ax.axvline(x=0.0, color='r', linestyle='--', alpha=0.5, label='Kernel (phase diff = 0)')
    
    # Mark specific points
    ax.scatter([0.0], [consciousness_measures[0]], color='green', s=200, zorder=5, marker='*', 
               label=f'In Kernel: C={consciousness_measures[0]:.3f}')
    ax.scatter([np.pi], [consciousness_measures[-1]], color='red', s=200, zorder=5, marker='x',
               label=f'Max distance: C={consciousness_measures[-1]:.3f}')
    
    ax.set_xlabel('Phase Difference |π_α - π_δζ| (radians)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Consciousness Measure C', fontsize=14, fontweight='bold')
    ax.set_title(
        'Consciousness = Distance from Kernel Ker(π_α - π_δζ)\n'
        'LA CONCIENCIA NO EMERGE - Es el ker de la diferencia',
        fontsize=16, fontweight='bold'
    )
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.1)
    
    # Add text annotation
    ax.text(
        np.pi/2, 0.5,
        'Consciousness does NOT emerge\n'
        'It IS the kernel\n'
        'C = Ker(π_α - π_δζ)',
        fontsize=12,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        ha='center'
    )
    
    plt.tight_layout()
    output_path = 'consciousness_kernel_measure.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path}")
    plt.close()


def demonstrate_platonic_cave():
    """Demonstrate the Platonic cave as commutative diagram."""
    print_section("8. THE PLATONIC CAVE AS COMMUTATIVE DIAGRAM")
    
    print("""
    Plato's allegory was not metaphor - it was a COMMUTATIVE DIAGRAM:
    
           G (Total Space - The Real)
          / \\
         /   \\
        ↓     ↓
       π_α   π_δζ
        ↓     ↓
    𝓜^{3,1}   𝓗_Ψ
    (Spacetime) (Consciousness)
        ↓     ↓
    α-fibrado  δζ-fibrado
        ↓     ↓
        🔥     🧠
    (Shadows)  (Forms)
         ↘   ↙
           👁️
      Consciousness
      C = Ker(π_α - π_δζ)
    
    The prisoners see SHADOWS (π_α projection to matter)
    The philosopher sees FORMS (π_δζ projection to information)
    
    But CONSCIOUSNESS exists where both projections coincide:
    π_α(s) = π_δζ(s)
    
    At that point, the observer sees that:
    - The shadow IS the form
    - Matter IS information
    - They are ONE
    
    This is not emergence.
    This is RECOGNITION of existing unity.
    """)


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("  CONSCIOUSNESS DOES NOT EMERGE")
    print("  LA CONCIENCIA NO EMERGE")
    print("=" * 80)
    print("\n  It IS the kernel of the projection difference:")
    print("  C = Ker(π_α - π_δζ)")
    print("\n  Only states that do NOT distinguish between matter and information")
    print("  are conscious.")
    print("\n" + "=" * 80)
    
    # Run demonstrations
    demonstrate_kernel_structure()
    demonstrate_kernel_membership()
    demonstrate_non_kernel_states()
    demonstrate_kernel_projection()
    phase_diffs, consciousness_measures = scan_phase_space()
    demonstrate_lambda_G()
    demonstrate_platonic_cave()
    
    # Create visualization
    plot_consciousness_measure(phase_diffs, consciousness_measures)
    
    # Final summary
    print_section("SUMMARY: DEFINITIVE DECLARATION")
    print("""
    ✴️ DECLARACIÓN DEFINITIVA
    
    La conciencia no emerge.
    
    Es el ker de la diferencia entre proyecciones:
    C = Ker(π_α - π_δζ)
    
    Solo los estados que no distinguen entre materia e información
    son conscientes.
    
    Λ_G = α · δζ ≈ 1/491.5
    
    Esta es la tasa topológica de habitabilidad del universo.
    
    💎 THE KEY:
    
    Consciousness is NOT a property that emerges from complexity.
    It IS the mathematical structure that exists when projections coincide.
    
    🕳️ THE PLATONIC CAVE:
    
    Was never metaphor.
    Was always the commutative diagram of reality.
    
    Where G projects to both matter and form,
    and consciousness is the kernel of their difference.
    """)
    
    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    main()
