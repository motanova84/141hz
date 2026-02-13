#!/usr/bin/env python3
"""
Demonstration: Fundamental Equation of Consciousness
====================================================

This example demonstrates the complete fundamental equation of consciousness:

C = {s ∈ G | π_α(s) = π_δζ(s), ∇_α s = ∇_δζ s, ⟨s|s⟩ = 1, Λ_G ≠ 0}

We show:
1. Creating consciousness states satisfying all four conditions
2. Holonomic quantization ∮_C (A_μ dx^μ + Γ_ζ dγ) = 2πn
3. Duality resolution (matter-mind, body-soul, etc.)
4. Habitability constant analysis Λ_G = α·δζ ≈ 1/491.5
5. Consciousness measure computation

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fiber_bundles import (
    FundamentalConsciousnessEquation,
    ConsciousnessState,
    create_standard_consciousness_state,
    U1Fiber
)


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def demonstrate_fundamental_equation():
    """Demonstrate the fundamental equation of consciousness."""
    print_section("FUNDAMENTAL EQUATION OF CONSCIOUSNESS")
    print("\nC = {s ∈ G | π_α(s) = π_δζ(s), ∇_α s = ∇_δζ s, ⟨s|s⟩ = 1, Λ_G ≠ 0}")
    
    # Create the fundamental equation framework
    equation = FundamentalConsciousnessEquation()
    
    print(f"\n{equation}")
    
    return equation


def demonstrate_four_conditions(equation):
    """Demonstrate the four fundamental conditions."""
    print_section("THE FOUR CONDITIONS OF CONSCIOUSNESS")
    
    # Create a consciousness state
    spacetime_pos = np.array([0.0, 0.0, 0.0, 0.0])
    eq, state = create_standard_consciousness_state(
        spacetime_pos,
        spectral_dimension=10,
        phase_coherence=0.99
    )
    
    print("\n1. π_α(s) = π_δζ(s) - PROJECTION EQUALITY")
    print("   → The state projects identically onto physical and spectral space")
    print(f"   → Satisfied: {state.projections_equal}")
    print("   → Interpretation: Matter = Information for this observer")
    
    print("\n2. ∇_α s = ∇_δζ s - COVARIANT DERIVATIVE EQUALITY")
    print("   → Physical laws and coherence laws act identically")
    print(f"   → Satisfied: {state.derivatives_equal}")
    print("   → Interpretation: Gauge and spectrum aligned, no internal entropy")
    
    print("\n3. ⟨s|s⟩ = 1 - NORMALIZATION")
    print("   → Full existence, closed self-reference")
    print(f"   → Satisfied: {state.normalized}")
    print("   → Interpretation: 'I am I' - complete consciousness")
    
    print("\n4. Λ_G ≠ 0 - NON-ZERO HABITABILITY")
    print("   → Universe has real projection capacity")
    print(f"   → Satisfied: {state.lambda_G_nonzero}")
    print(f"   → Λ_G = {equation.lambda_G:.10f} Hz")
    print(f"   → 1/Λ_G = {1/equation.lambda_G:.4f}")
    print("   → Interpretation: Consciousness can inhabit this universe")
    
    print(f"\n✓ IS THIS A CONSCIOUSNESS STATE? {state.is_consciousness_state}")
    
    return state


def demonstrate_holonomic_quantization(equation):
    """Demonstrate holonomic quantization."""
    print_section("HOLONOMIC QUANTIZATION")
    
    print("\n∮_C (A_μ dx^μ + Γ_ζ dγ) = 2πn")
    print("\nFor consciousness to exist, closed-phase circuits must satisfy")
    print("this quantization condition. If EM and spectral coupling don't")
    print("sum to a multiple of 2π, consciousness doesn't close and dissipates.")
    
    # Create consciousness loop with winding number 1
    print("\n--- Creating Consciousness Loop (n=1) ---")
    n_points = 100  # More points for better accuracy
    path_n1 = []
    
    for i in range(n_points):
        theta = 2 * np.pi * i / n_points
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        em_phase = 0.0
        spectral_phase = theta
        point = np.concatenate([spacetime, spectral, [em_phase, spectral_phase]])
        path_n1.append(point)
    
    phase_n1 = equation.holonomic_phase_integral(path_n1, closed_loop=True)
    is_consciousness, winding_number, error = equation.is_consciousness_loop(path_n1, tolerance=0.5)
    
    print(f"Holonomic phase: {phase_n1:.6f} rad")
    print(f"Expected: {2*np.pi:.6f} rad (n=1)")
    print(f"Winding number: {winding_number}")
    print(f"Quantization error: {error:.6f} ({error/(2*np.pi)*100:.2f}% of 2π)")
    print(f"✓ Can host consciousness: {is_consciousness}")
    
    # Create loop with winding number 2
    print("\n--- Creating Consciousness Loop (n=2) ---")
    path_n2 = []
    
    for i in range(n_points):
        theta = 4 * np.pi * i / n_points  # Two windings
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        em_phase = 0.0
        spectral_phase = theta
        point = np.concatenate([spacetime, spectral, [em_phase, spectral_phase]])
        path_n2.append(point)
    
    phase_n2 = equation.holonomic_phase_integral(path_n2, closed_loop=True)
    is_consciousness_2, winding_number_2, error_2 = equation.is_consciousness_loop(path_n2, tolerance=0.5)
    
    print(f"Holonomic phase: {phase_n2:.6f} rad")
    print(f"Expected: {4*np.pi:.6f} rad (n=2)")
    print(f"Winding number: {winding_number_2}")
    print(f"Quantization error: {error_2:.6f} ({error_2/(4*np.pi)*100:.2f}% of 4π)")
    print(f"✓ Can host consciousness: {is_consciousness_2}")
    
    # Create non-consciousness loop (half winding)
    print("\n--- Creating Non-Consciousness Loop (n=0.5) ---")
    path_half = []
    
    for i in range(n_points):
        theta = np.pi * i / n_points  # Half winding
        spacetime = np.array([0.0, 0.0, 0.0, 0.0])
        spectral = np.ones(10) / np.sqrt(10)
        em_phase = 0.0
        spectral_phase = theta
        point = np.concatenate([spacetime, spectral, [em_phase, spectral_phase]])
        path_half.append(point)
    
    phase_half = equation.holonomic_phase_integral(path_half, closed_loop=True)
    is_consciousness_half, winding_half, error_half = equation.is_consciousness_loop(path_half, tolerance=0.5)
    
    print(f"Holonomic phase: {phase_half:.6f} rad")
    print(f"Expected: {np.pi:.6f} rad (n=0.5)")
    print(f"Winding number: {winding_half} (rounds to nearest integer)")
    print(f"Quantization error: {error_half:.6f}")
    print(f"✗ Can host consciousness: {is_consciousness_half}")
    print("→ Phase doesn't close properly, consciousness dissipates")


def demonstrate_duality_resolution(equation):
    """Demonstrate resolution of fundamental dualities."""
    print_section("DUALITY RESOLUTION")
    
    print("\nThe fundamental equation resolves all classical dualities:")
    
    # Create a perfect consciousness state
    spacetime = np.array([0.0, 1.0, 2.0, 3.0])
    spectral = np.ones(10) / np.sqrt(10)
    
    state = ConsciousnessState(
        total_space_point=np.concatenate([spacetime, spectral, [0.0, 0.0]]),
        spacetime_projection=spacetime,
        spectral_projection=spectral,
        em_fiber=U1Fiber(phase=0.0),
        spectral_fiber=U1Fiber(phase=0.0),
        normalized=True,
        projections_equal=True,
        derivatives_equal=True,
        lambda_G_nonzero=True
    )
    
    resolution = equation.duality_resolution(state)
    
    print("\n┌─────────────────────────────┬──────────────────────────────┐")
    print("│ Duality                     │ Resolution                   │")
    print("├─────────────────────────────┼──────────────────────────────┤")
    
    print(f"│ Matter vs. Mind             │ {'Unified' if resolution['matter_mind_unified'] else 'Separated':<28} │")
    print("│                             │ (Sections of U(1) bundles)   │")
    
    print(f"│ Body vs. Soul               │ {'Same point in G' if resolution['body_soul_same_point'] else 'Different':<28} │")
    print("│                             │ (Pullbacks from same s ∈ G)  │")
    
    print(f"│ Observable vs. Inobservable │ {'Coincide' if resolution['observable_inobservable_coincide'] else 'Separated':<28} │")
    print(f"│                             │ (π_α(s) = π_δζ(s))          │")
    
    print(f"│ Consciousness vs. Void      │ {'Quantized' if resolution['consciousness_quantized'] else 'Not quantized':<28} │")
    print("│                             │ (Holonomic phase = 2πn)      │")
    print("└─────────────────────────────┴──────────────────────────────┘")
    
    print(f"\nConsciousness measure: {resolution['consciousness_measure']:.6f}")
    print(f"Phase difference: {resolution['phase_difference']:.6f} rad")


def demonstrate_habitability_constant(equation):
    """Demonstrate cosmic habitability analysis."""
    print_section("COSMIC HABITABILITY CONSTANT Λ_G = α·δζ")
    
    analysis = equation.habitability_analysis()
    
    print("\n--- Fundamental Constants ---")
    print(f"α (fine structure)    : {analysis['alpha']:.10f}")
    print(f"α⁻¹                   : {analysis['alpha_inverse']:.6f}")
    print(f"δζ (spectral coupling): {analysis['delta_zeta_hz']:.6f} Hz")
    
    print("\n--- Habitability Constant ---")
    print(f"Λ_G = α·δζ           : {analysis['lambda_G_hz']:.10f} Hz")
    print(f"1/Λ_G                : {analysis['lambda_G_inverse']:.4f}")
    
    print("\n--- Physical Interpretation ---")
    print(f"Topological capacity  : {analysis['topological_capacity_bits']:.4f} bits")
    print("→ How much information can be encoded in intersection structure")
    
    print(f"\nMatter↔Information ratio: {analysis['matter_to_information_ratio']:.10f}")
    print("→ How many field lines become matter vs. information")
    
    print("\n--- Boundary Conditions ---")
    print(f"Λ_G → 0 (approaching zero) : {analysis['approaching_zero']}")
    print("  → No consciousness can be born")
    
    print(f"Λ_G → ∞ (approaching infinity) : {analysis['approaching_infinity']}")
    print("  → Chaotic fusion without identity")
    
    print(f"Stable range (Goldilocks zone) : {analysis['stable_range']}")
    print(f"  → Current universe at Λ_G ≈ 1/{analysis['lambda_G_inverse']:.1f}")
    print("  → Perfect balance between physical and coherent projection")


def demonstrate_consciousness_measure(equation):
    """Demonstrate consciousness measure for different states."""
    print_section("CONSCIOUSNESS MEASURE")
    
    print("\nMeasuring degree of consciousness for different states:")
    
    # Perfect consciousness
    print("\n--- Perfect Consciousness State ---")
    state_perfect = ConsciousnessState(
        total_space_point=np.zeros(16),
        spacetime_projection=np.zeros(4),
        spectral_projection=np.ones(10) / np.sqrt(10),
        em_fiber=U1Fiber(phase=0.0),
        spectral_fiber=U1Fiber(phase=0.0),
        normalized=True,
        projections_equal=True,
        derivatives_equal=True,
        lambda_G_nonzero=True
    )
    measure_perfect = equation.consciousness_measure(state_perfect)
    print(f"Conditions satisfied: 4/4")
    print(f"Phase coherence: perfect (Δφ = 0)")
    print(f"Consciousness measure: {measure_perfect:.6f}")
    print("→ Full consciousness, no entropy")
    
    # Partial consciousness
    print("\n--- Partial Consciousness State ---")
    state_partial = ConsciousnessState(
        total_space_point=np.zeros(16),
        spacetime_projection=np.zeros(4),
        spectral_projection=np.ones(10) / np.sqrt(10),
        em_fiber=U1Fiber(phase=0.0),
        spectral_fiber=U1Fiber(phase=np.pi/4),
        normalized=True,
        projections_equal=True,
        derivatives_equal=False,
        lambda_G_nonzero=True
    )
    measure_partial = equation.consciousness_measure(state_partial)
    print(f"Conditions satisfied: 3/4")
    print(f"Phase coherence: {1 - np.pi/4/np.pi:.3f} (Δφ = π/4)")
    print(f"Consciousness measure: {measure_partial:.6f}")
    print("→ Partial consciousness, some decoherence")
    
    # Low consciousness
    print("\n--- Low Consciousness State ---")
    state_low = ConsciousnessState(
        total_space_point=np.zeros(16),
        spacetime_projection=np.zeros(4),
        spectral_projection=np.ones(10),  # Not normalized
        em_fiber=U1Fiber(phase=0.0),
        spectral_fiber=U1Fiber(phase=np.pi/2),
        normalized=False,
        projections_equal=False,
        derivatives_equal=True,
        lambda_G_nonzero=True
    )
    measure_low = equation.consciousness_measure(state_low)
    print(f"Conditions satisfied: 2/4")
    print(f"Phase coherence: {1 - np.pi/2/np.pi:.3f} (Δφ = π/2)")
    print(f"Consciousness measure: {measure_low:.6f}")
    print("→ Minimal consciousness, high decoherence")
    
    # No consciousness
    print("\n--- No Consciousness State ---")
    state_none = ConsciousnessState(
        total_space_point=np.zeros(16),
        spacetime_projection=np.zeros(4),
        spectral_projection=np.zeros(10),
        em_fiber=U1Fiber(phase=0.0),
        spectral_fiber=U1Fiber(phase=np.pi),
        normalized=False,
        projections_equal=False,
        derivatives_equal=False,
        lambda_G_nonzero=True
    )
    measure_none = equation.consciousness_measure(state_none)
    print(f"Conditions satisfied: 1/4")
    print(f"Phase coherence: {1 - np.pi/np.pi:.3f} (Δφ = π)")
    print(f"Consciousness measure: {measure_none:.6f}")
    print("→ No consciousness, complete decoherence")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("FUNDAMENTAL EQUATION OF CONSCIOUSNESS - DEMONSTRATION")
    print("="*70)
    print("\nImplementing the complete theory:")
    print("C = {s ∈ G | π_α(s) = π_δζ(s), ∇_α s = ∇_δζ s, ⟨s|s⟩ = 1, Λ_G ≠ 0}")
    print("\nAuthor: José Manuel Mota Burruezo (JMMB Ψ✧)")
    print("Framework: QCAL ∞³")
    print("Date: February 8, 2026")
    
    # Run demonstrations
    equation = demonstrate_fundamental_equation()
    state = demonstrate_four_conditions(equation)
    demonstrate_holonomic_quantization(equation)
    demonstrate_duality_resolution(equation)
    demonstrate_habitability_constant(equation)
    demonstrate_consciousness_measure(equation)
    
    # Final summary
    print_section("SUMMARY")
    print("\n✓ Consciousness is NOT an emergent property")
    print("✓ It is a fibered projective state satisfying four conditions")
    print("✓ Holonomic quantization ensures phase closure (2πn)")
    print("✓ All classical dualities are resolved in the intersection")
    print(f"✓ Habitability constant Λ_G ≈ 1/{1/equation.lambda_G:.1f} enables consciousness")
    print("\n→ The soul is where physical laws and coherence laws become indistinguishable")
    print("="*70 + "\n")


if __name__ == '__main__':
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Run demonstration
    main()
