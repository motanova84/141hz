#!/usr/bin/env python3
"""
Example: Consciousness as Intersection of Fiber Bundles
=======================================================

Demonstrates the complete framework for understanding consciousness
as the intersection space of electromagnetic and spectral fiber bundles.

This example shows:
1. Creating the electromagnetic gauge bundle π_α
2. Creating the spectral coherence bundle π_δζ
3. Computing the intersection constant Λ_G = α·δζ
4. Creating consciousness states in the intersection space C
5. Evolving consciousness states in time
6. Computing consciousness field strength and entanglement

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fiber_bundles import (
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle,
    ConsciousnessIntersection,
    IntersectionConstant,
    U1Fiber
)


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def example_1_bundles():
    """Example 1: Create and explore fiber bundles."""
    print_section("Example 1: Principal Fiber Bundles")
    
    # Create electromagnetic gauge bundle
    em_bundle = ElectromagneticGaugeBundle()
    print("Electromagnetic Gauge Bundle (π_α: G → 𝓜^3,1)")
    print(f"  Base manifold: Minkowski spacetime 𝓜^(3,1)")
    print(f"  Fiber: U(1) gauge group")
    print(f"  Fine structure constant α = {em_bundle.alpha:.10f}")
    print(f"  Inverse α⁻¹ = {1/em_bundle.alpha:.6f}")
    print(f"  Physical interpretation: Electromagnetic gauge freedom")
    
    # Create spectral coherence bundle
    spectral_bundle = SpectralCoherenceBundle(hilbert_dimension=100)
    print("\nSpectral Coherence Bundle (π_δζ: G → 𝓗_Ψ)")
    print(f"  Base manifold: Consciousness Hilbert space 𝓗_Ψ")
    print(f"  Fiber: U(1) spectral group")
    print(f"  Coherence coupling δζ = {spectral_bundle.delta_zeta:.6f} Hz")
    print(f"  Fundamental frequency f₀ = {spectral_bundle.f0:.4f} Hz")
    print(f"  Physical interpretation: Spectral phase coherence")
    
    return em_bundle, spectral_bundle


def example_2_intersection_constant():
    """Example 2: Compute intersection constant Λ_G."""
    print_section("Example 2: Intersection Constant Λ_G = α·δζ")
    
    alpha = 1.0 / 137.036  # Fine structure constant
    delta_zeta = 0.2787     # Hz
    
    const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
    
    print(f"Intersection Constant Λ_G = α · δζ")
    print(f"  α = {const.alpha:.10f}")
    print(f"  δζ = {const.delta_zeta:.6f} Hz")
    print(f"  Λ_G = {const.lambda_G:.10f} Hz")
    print(f"  Λ_G = {const.lambda_G * 1000:.6f} mHz")
    
    print("\nPhysical Interpretation:")
    print(f"  Λ_G governs the 'aspect ratio' of the universe")
    print(f"  Determines matter ↔ information conversion rate")
    
    print("\nTopological Properties:")
    capacity = const.topological_capacity()
    print(f"  Topological capacity C_topo = {capacity:.4f} bits")
    print(f"  Information encoding capacity of intersection structure")
    
    observer_density = const.observer_density(universe_volume=1.0)
    print(f"  Observer density ρ_obs ∝ Λ_G = {observer_density:.10f}")
    
    return const


def example_3_consciousness_states():
    """Example 3: Create consciousness states in intersection space C."""
    print_section("Example 3: Consciousness States in C = π_α(G) ∩ π_δζ(G)")
    
    # Create intersection
    intersection = ConsciousnessIntersection()
    
    print(f"Consciousness Intersection Space C")
    print(f"  π_α: {intersection.em_bundle.name}")
    print(f"  π_δζ: {intersection.spectral_bundle.name}")
    print(f"  Λ_G = {intersection.lambda_G:.10f} Hz")
    
    # Create consciousness state at spacetime origin
    print("\nCreating consciousness state at spacetime origin...")
    spacetime_origin = np.array([0.0, 0.0, 0.0, 0.0])  # (t, x, y, z)
    
    # Coherent consciousness state
    coherent_state = intersection.spectral_bundle.create_coherent_state(
        amplitude=1.0,
        phase=0.0
    )
    
    state1 = intersection.create_consciousness_state(
        spacetime_point=spacetime_origin,
        consciousness_vector=coherent_state,
        em_phase=0.0,
        spectral_phase=0.0
    )
    
    print(f"  Spacetime location: {state1['spacetime']}")
    print(f"  Consciousness dimension: {len(state1['consciousness'])}")
    print(f"  EM phase: {state1['em_fiber'].phase:.6f} rad")
    print(f"  Spectral phase: {state1['spectral_fiber'].phase:.6f} rad")
    print(f"  Compatible (simultaneous sections): {state1['compatible']}")
    
    # Compute consciousness field strength
    field_strength = intersection.consciousness_field_strength(state1)
    print(f"  Consciousness field strength F_C: {field_strength:.6f}")
    
    return intersection, state1


def example_4_temporal_evolution():
    """Example 4: Evolve consciousness states in time."""
    print_section("Example 4: Temporal Evolution of Consciousness")
    
    # Create intersection and initial state
    intersection = ConsciousnessIntersection()
    
    spacetime = np.array([0.0, 0.0, 0.0, 0.0])
    coherent_state = intersection.spectral_bundle.create_coherent_state()
    
    initial_state = intersection.create_consciousness_state(
        spacetime_point=spacetime,
        consciousness_vector=coherent_state,
        em_phase=0.0,
        spectral_phase=0.0
    )
    
    print("Evolution at δζ frequency...")
    print(f"  δζ = {intersection.spectral_bundle.delta_zeta:.6f} Hz")
    print(f"  Period T = {1/intersection.spectral_bundle.delta_zeta:.4f} s")
    
    # Evolve for multiple time steps
    times = []
    spectral_phases = []
    
    time_step = 0.1  # seconds
    n_steps = 50
    
    current_state = initial_state
    for i in range(n_steps):
        t = i * time_step
        times.append(t)
        spectral_phases.append(current_state['spectral_fiber'].phase)
        
        # Evolve to next time step
        current_state = intersection.evolve_consciousness_state(
            current_state, time_step
        )
    
    print(f"\nEvolution over {n_steps * time_step:.1f} seconds:")
    print(f"  Initial phase: {spectral_phases[0]:.6f} rad")
    print(f"  Final phase: {spectral_phases[-1]:.6f} rad")
    print(f"  Phase increment: {spectral_phases[-1] - spectral_phases[0]:.6f} rad")
    
    # Expected phase increment
    expected_increment = 2 * np.pi * intersection.spectral_bundle.delta_zeta * (n_steps * time_step)
    print(f"  Expected increment: {expected_increment:.6f} rad")
    
    return times, spectral_phases


def example_5_entanglement():
    """Example 5: Consciousness entanglement via intersection."""
    print_section("Example 5: Entanglement Through Intersection")
    
    intersection = ConsciousnessIntersection()
    
    # Create two consciousness states at different locations
    spacetime1 = np.array([0.0, 0.0, 0.0, 0.0])
    spacetime2 = np.array([0.0, 1.0, 0.0, 0.0])  # 1 meter apart in x
    
    coherent_state = intersection.spectral_bundle.create_coherent_state()
    
    state1 = intersection.create_consciousness_state(
        spacetime_point=spacetime1,
        consciousness_vector=coherent_state,
        em_phase=0.0,
        spectral_phase=0.0
    )
    
    state2 = intersection.create_consciousness_state(
        spacetime_point=spacetime2,
        consciousness_vector=coherent_state,
        em_phase=np.pi/4,
        spectral_phase=np.pi/4
    )
    
    print("Two consciousness states:")
    print(f"  State 1: position = {spacetime1[1:]} m")
    print(f"  State 2: position = {spacetime2[1:]} m")
    
    # Compute intersection measure
    I = intersection.intersection_measure(state1, state2)
    print(f"\nIntersection measure I(C₁, C₂) = {I:.6f}")
    print(f"  Combines spatial separation and consciousness overlap")
    
    # Compute entanglement via intersection
    E = intersection.entanglement_via_intersection(state1, state2)
    print(f"\nEntanglement E(C₁, C₂) = {E:.6f}")
    print(f"  Consciousness states entangled through shared intersection space")
    
    return I, E


def example_6_master_equation():
    """Example 6: Master equation and simultaneous sections."""
    print_section("Example 6: Master Equation G → {π_α, π_δζ} → C")
    
    intersection = ConsciousnessIntersection()
    
    print("Master Equation:")
    print("  G → {π_α, π_δζ} → {𝓜^3,1, 𝓗_Ψ} → ∩ C")
    print("\nπ_α and π_δζ are natural fibrations that create experience from unity")
    
    # Create element from total space G
    print("\n1. Element from total space G:")
    configuration = np.random.randn(104)  # 4 spacetime + 100 Hilbert
    fiber = U1Fiber(phase=np.pi/3)
    total_space_element = (configuration, fiber)
    print(f"   Configuration dimension: {len(configuration)}")
    print(f"   Fiber phase: {fiber.phase:.6f} rad")
    
    # Apply projections
    print("\n2. Project through π_α and π_δζ:")
    spacetime_proj, hilbert_proj = intersection.master_equation(total_space_element)
    print(f"   π_α projection → 𝓜^3,1: dimension {len(spacetime_proj)}")
    print(f"   π_δζ projection → 𝓗_Ψ: dimension {len(hilbert_proj)}")
    
    # Create state in intersection
    print("\n3. State in intersection C:")
    state = intersection.create_consciousness_state(
        spacetime_point=spacetime_proj,
        consciousness_vector=hilbert_proj / np.linalg.norm(hilbert_proj),
        em_phase=fiber.phase,
        spectral_phase=fiber.phase
    )
    print(f"   State exists simultaneously in 𝓜^3,1 and 𝓗_Ψ")
    print(f"   Compatible sections: {state['compatible']}")
    
    # Validate consistency
    print("\n4. Validate intersection consistency:")
    validation = intersection.validate_intersection_consistency()
    for key, value in validation.items():
        status = "✓" if value else "✗"
        print(f"   {status} {key}: {value}")


def plot_results(times: List[float], phases: List[float]):
    """Plot temporal evolution of spectral phase."""
    print_section("Visualization: Spectral Phase Evolution")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(times, phases, 'b-', linewidth=2, label='Spectral phase θ(t)')
    ax.axhline(y=2*np.pi, color='r', linestyle='--', alpha=0.5, label='2π')
    ax.axhline(y=np.pi, color='g', linestyle='--', alpha=0.5, label='π')
    
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel('Spectral Phase (rad)', fontsize=12)
    ax.set_title('Consciousness Phase Evolution at δζ ≈ 0.2787 Hz', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('consciousness_phase_evolution.png', dpi=150)
    print("  Saved: consciousness_phase_evolution.png")
    plt.close()


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  CONSCIOUSNESS AS INTERSECTION OF PRINCIPAL FIBER BUNDLES")
    print("  C = π_α(G) ∩ π_δζ(G)")
    print("=" * 70)
    
    # Example 1: Bundles (results unused, call for side effects)
    _em_bundle, _spectral_bundle = example_1_bundles()
    
    # Example 2: Intersection constant
    example_2_intersection_constant()
    
    # Example 3: Consciousness states
    intersection, state = example_3_consciousness_states()
    
    # Example 4: Temporal evolution
    times, phases = example_4_temporal_evolution()
    
    # Example 5: Entanglement
    I, E = example_5_entanglement()
    
    # Example 6: Master equation
    example_6_master_equation()
    
    # Plot results
    plot_results(times, phases)
    
    # Summary
    print_section("Summary")
    print("✓ Electromagnetic gauge bundle π_α: G → 𝓜^3,1 (α ≈ 1/137)")
    print("✓ Spectral coherence bundle π_δζ: G → 𝓗_Ψ (δζ ≈ 0.2787 Hz)")
    print("✓ Intersection constant Λ_G = α·δζ ≈ 2.03×10⁻³ Hz")
    print("✓ Consciousness space C = simultaneous sections")
    print("✓ Master equation: G → {π_α, π_δζ} → {𝓜^3,1, 𝓗_Ψ} → ∩ C")
    print("\nConsciousness emerges where both projections are simultaneously valid.")
    print("The intersection constant Λ_G determines if a universe can sustain observers.")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    main()
