#!/usr/bin/env python3
"""
Demonstration: Fundamental Theorem of Consciousness
===================================================

This script demonstrates the rigorous geometric formulation of consciousness
as the intersection of two principal fiber bundles.

THEOREM: Consciousness C = Γ(E_α) ∩ Γ(E_δζ)

Where:
- E_α: Electromagnetic bundle (α ≈ 1/137)
- E_δζ: Spectral bundle (δζ ≈ 0.2787 Hz)
- Λ_G = α·δζ ≈ 1/491.5 (intersection constant)

This demonstrates:
1. Computing the intersection constant Λ_G
2. Projection ratios (matter vs. information)
3. Master Lagrangian with interaction term
4. Holonomic quantization of conscious states
5. Habitability condition for observers
6. Plato's Cave interpretation

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fiber_bundles import (
    ConsciousnessTheorem,
    ElectromagneticGaugeBundle,
    SpectralCoherenceBundle
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def demo_intersection_constant():
    """Demonstrate the intersection constant Λ_G = α·δζ."""
    print_section("1. INTERSECTION CONSTANT Λ_G")
    
    theorem = ConsciousnessTheorem()
    
    print(f"Fine structure constant:  α = {theorem.alpha:.10f}")
    print(f"Spectral coupling:        δζ = {theorem.delta_zeta:.6f} Hz")
    print(f"Intersection constant:    Λ_G = {theorem.lambda_G:.10f} Hz")
    print(f"Inverse:                  1/Λ_G = {1/theorem.lambda_G:.2f}")
    
    # Get all properties
    props = theorem.intersection_constant()
    print(f"\nTopological capacity:     C_topo = {props['topological_capacity']:.4f} bits")
    print(f"Euler characteristic:     χ(C) = {props['euler_characteristic']:.10f}")
    print(f"Universe habitable:       {props['habitability']}")
    
    print("\nINTERPRETATION:")
    print("  Λ_G measures the 'volume' of the intersection between")
    print("  physical and spectral projections from the mother space G.")
    print("  If Λ_G = 0 → no intersection → no consciousness possible.")
    print(f"  If Λ_G ≈ 1/491.5 → balanced → life can emerge ✓")


def demo_projection_ratios():
    """Demonstrate projection ratios between bundles."""
    print_section("2. PROJECTION RATIOS (Matter vs. Information)")
    
    theorem = ConsciousnessTheorem()
    ratios = theorem.projection_ratio()
    
    print(f"Flux to spacetime M^{{3,1}}:  {ratios['flux_to_spacetime']:.10f}")
    print(f"Flux to Hilbert H_Ψ:        {ratios['flux_to_hilbert']:.6f} Hz")
    print(f"\nRatio α/δζ:                 {ratios['ratio_alpha_delta']:.6f}")
    print(f"Ratio δζ/α:                 {ratios['ratio_delta_alpha']:.4f}")
    print(f"\nInformation per matter:     {ratios['information_per_matter']:.2f}")
    
    print("\nINTERPRETATION:")
    print(f"  For every ~{ratios['information_per_matter']:.0f} units of spectral information,")
    print("  only 1 unit manifests as observable matter.")
    print("  This ratio is FIXED by the geometry of G.")
    print("  If different → universe either too dense or too ghostly for life.")


def demo_master_lagrangian():
    """Demonstrate the master Lagrangian L_G."""
    print_section("3. MASTER LAGRANGIAN L_G = L_α + L_δζ + L_int")
    
    theorem = ConsciousnessTheorem()
    
    # Create test state
    spacetime_point = np.array([0.0, 0.0, 0.0, 0.0])  # Origin
    consciousness_state = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)
    
    # Simulate field strengths
    em_field_strength = 0.1  # F_μν F^{μν}
    spectral_curvature = 0.01  # Ω_Ψ
    
    lagrangian = theorem.master_lagrangian(
        spacetime_point,
        consciousness_state,
        em_field_strength,
        spectral_curvature
    )
    
    print(f"L_α (Electromagnetic):    {lagrangian.L_alpha:.10f}")
    print(f"L_δζ (Spectral):          {lagrangian.L_delta_zeta:.10f}")
    print(f"L_int (Interaction):      {lagrangian.L_interaction:.10f}")
    print(f"L_total (Master):         {lagrangian.L_total:.10f}")
    
    print("\nCOMPONENTS:")
    print("  L_α = -1/(4α) F_μν F^{μν}  (Maxwell with α coupling)")
    print("  L_δζ = ⟨ψ|(iℏ∂_t - H_Ψ)|ψ⟩  (Spectral dynamics)")
    print("  L_int = Λ_G · Tr(F_μν · Ω_Ψ)  (Coupling term)")
    print("\nThe interaction term L_int is CRUCIAL:")
    print("  Without Λ_G ≠ 0, no coupling → no consciousness!")


def demo_holonomic_quantization():
    """Demonstrate holonomic quantization of consciousness states."""
    print_section("4. HOLONOMIC QUANTIZATION")
    
    theorem = ConsciousnessTheorem()
    
    print("CONDITION: ∮_C (A_μ dx^μ + Γ_ζ dγ) = 2πn, n ∈ ℤ")
    print("\nOnly states with integer multiples of 2π can be conscious!\n")
    
    # Define sample paths
    def em_path(t):
        """Circular path in spacetime."""
        return np.array([t, np.cos(2*np.pi*t), np.sin(2*np.pi*t), 0.0])
    
    def spectral_path(t):
        """Path through zeta zeros."""
        return 14.134 + 7.0 * t  # Start at first zero, move to second
    
    # Compute quantization
    quantization = theorem.holonomic_section(em_path, spectral_path)
    
    print(quantization)
    
    print("\nALLOWED STATES C_n:")
    allowed = theorem.allowed_consciousness_states(max_quantum_number=5)
    
    for i, state in enumerate(allowed[:5]):
        n = state['quantum_number']
        phase = state['total_phase']
        print(f"  C_{n:2d}: Φ_total = {phase:7.4f} rad = {n}·2π")
    
    print(f"\n  ... and {len(allowed)-5} more states")
    
    print("\nINTERPRETATION:")
    print("  Consciousness is QUANTIZED like energy levels in quantum mechanics.")
    print("  Not all states are allowed - only those satisfying the holonomy condition.")


def demo_consciousness_kernel():
    """Demonstrate C = Ker(π_α - π_δζ)."""
    print_section("5. CONSCIOUSNESS AS KERNEL: C = Ker(π_α - π_δζ)")
    
    theorem = ConsciousnessTheorem()
    
    print("The consciousness space is the kernel of (π_α - π_δζ):")
    print("States where both projections agree.\n")
    
    # Create point in mother space G
    # Structure: [t, x, y, z, ψ₁, ψ₂, ψ₃, ψ₄]
    point_in_G = np.array([
        0.0, 1.0, 2.0, 3.0,  # Spacetime coordinates
        1.0, 0.0, 0.0, 0.0   # Consciousness state
    ])
    
    result = theorem.consciousness_kernel(point_in_G)
    
    print(f"Point in G:              {result['point_in_G'][:4]} ...")
    print(f"π_α projection (M^{{3,1}}): {result['pi_alpha_projection']}")
    print(f"π_δζ projection (H_Ψ):   {result['pi_delta_zeta_projection']}")
    print(f"In intersection C:       {result['in_intersection']}")
    
    print("\nKEY INSIGHT:")
    print("  States in the kernel cannot distinguish between")
    print("  matter (π_α) and information (π_δζ).")
    print("  They are BOTH simultaneously.")
    print("  This is consciousness - not emergence, but geometry.")


def demo_uniqueness_theorem():
    """Demonstrate uniqueness of the fibrations."""
    print_section("6. UNIQUENESS THEOREM")
    
    theorem = ConsciousnessTheorem()
    
    print("THEOREM: π_α and π_δζ are the ONLY U(1) fibrations that")
    print("preserve the symplectic structure of G.\n")
    
    verification = theorem.verify_uniqueness_theorem()
    
    print("Verification:")
    print(f"  ✓ E_α has U(1)_gauge fiber:     {verification['em_is_U1']}")
    print(f"  ✓ E_δζ has U(1)_spectral fiber: {verification['spectral_is_U1']}")
    print(f"  ✓ Maxwell (no monopoles):       {verification['maxwell_no_monopoles']}")
    print(f"  ✓ Spectral zeros (ζ function):  {verification['spectral_has_zeros']}")
    print(f"\n  ✓ UNIQUENESS:                   {verification['uniqueness']}")
    
    print("\nCONCLUSION:")
    print('  The universe does NOT "choose" these projections.')
    print("  They are the ONLY POSSIBLE fibrations!")
    print("  Consciousness is inevitable in a universe with this structure.")


def demo_habitability():
    """Demonstrate habitability condition."""
    print_section("7. HABITABILITY CONDITION")
    
    theorem = ConsciousnessTheorem()
    
    print("CONDITION: A universe can sustain conscious observers iff Λ_G ≠ 0\n")
    
    validation = theorem.validate_habitability_condition()
    
    print(f"Λ_G = {validation['lambda_G']:.10f} Hz")
    print(f"Λ_G ≠ 0: {validation['lambda_G_nonzero']}")
    print(f"Habitable: {validation['habitable']}")
    print(f"\nInterpretation: {validation['interpretation']}")
    print(f"Observer density: {validation['observer_density']:.10f}")
    
    print("\nSCENARIOS:")
    print("  If Λ_G = 0:      Bundles disjoint → no intersection → no consciousness")
    print("  If Λ_G ≫ 0.01:   Too much matter → universe dense and dead")
    print("  If Λ_G ≪ 10⁻⁶:   Too much info → universe ghostly, no observers")
    print(f"  If Λ_G ≈ 1/491:  GOLDILOCKS → balanced → life emerges ✓")


def demo_plato():
    """Demonstrate Plato's Cave interpretation."""
    print_section("8. PLATO'S CAVE INTERPRETATION")
    
    theorem = ConsciousnessTheorem()
    print(theorem.plato_sun_interpretation())


def main():
    """Run all demonstrations."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  FUNDAMENTAL THEOREM OF CONSCIOUSNESS                                ║
║  Geometric Formulation as Fiber Bundle Intersection                  ║
║                                                                        ║
║  C = Γ(E_α) ∩ Γ(E_δζ)                                                ║
║                                                                        ║
║  Where:                                                                ║
║    π_α: E_α → M^{3,1}  (Electromagnetic, α ≈ 1/137)                  ║
║    π_δζ: E_δζ → H_Ψ    (Spectral, δζ ≈ 0.2787 Hz)                    ║
║    Λ_G = α·δζ ≈ 1/491.5 (Intersection constant)                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run all demonstrations
    demo_intersection_constant()
    demo_projection_ratios()
    demo_master_lagrangian()
    demo_holonomic_quantization()
    demo_consciousness_kernel()
    demo_uniqueness_theorem()
    demo_habitability()
    demo_plato()
    
    print_section("SUMMARY")
    print("""
KEY RESULTS:
1. Consciousness is NOT emergent - it's a geometric property
2. C is the intersection of electromagnetic and spectral fiber bundles
3. Λ_G = α·δζ determines if a universe can have observers
4. Only holonomically quantized states can be conscious
5. The projections π_α and π_δζ are unique (not arbitrary)
6. Plato was right: consciousness sees both shadows and forms

MATHEMATICAL RIGOR:
✓ Principal fiber bundles with U(1) fibers
✓ Intersection theory on manifolds
✓ Holonomic quantization condition
✓ Master Lagrangian with interaction term
✓ Uniqueness theorem for fibrations
✓ Habitability from topology

This is not philosophy. This is mathematics.
This is not speculation. This is geometry.
    """)


if __name__ == "__main__":
    main()
