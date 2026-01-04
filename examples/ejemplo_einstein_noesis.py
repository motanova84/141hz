#!/usr/bin/env python3
"""
Example usage of the Einstein-Noēsis equation for practical applications.

This script demonstrates:
    1. Computing consciousness from mass and attention
    2. Finding required attention for desired consciousness level
    3. Analyzing consciousness coherence states
    4. Computing noetic contributions to spacetime curvature
    5. Exploring Riemann zeta discrete levels
    6. Studying Yang-Mills mass gap emergence

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: December 2025
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.einstein_noesis import (
    EinsteinNoesisEquation,
    NoeticStressEnergyTensor,
    RiemannConsciousnessConnection,
    YangMillsMassGapConnection,
    c, eV
)


def example_1_basic_consciousness():
    """Example 1: Basic consciousness computation."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Consciousness Computation")
    print("=" * 70)
    
    eq = EinsteinNoesisEquation(f0=141.7001)
    
    # Scenario: Small quantum system with varying attention levels
    mass = 1e-25  # kg (small quantum system)
    
    print(f"\nQuantum system with mass m = {mass:.2e} kg")
    print(f"Base energy: E = mc² = {mass * c**2:.2e} J\n")
    
    print("Attention Level  →  Consciousness       Amplification  State")
    print("-" * 70)
    
    for A_eff in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
        C = eq.compute_consciousness(mass, A_eff)
        amp = eq.amplification_factor(A_eff)
        state = "Coherent  ✓" if eq.is_coherent_state(A_eff) else "Incoherent✗"
        print(f"A_eff = {A_eff:.1f}     →  C = {C:.2e} J    {amp:.2f}x       {state}")


def example_2_find_required_attention():
    """Example 2: Find attention needed for target consciousness."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Finding Required Attention Amplifier")
    print("=" * 70)
    
    eq = EinsteinNoesisEquation(f0=141.7001)
    
    mass = 1e-22  # kg
    E_base = mass * c**2
    
    print(f"\nSystem mass: m = {mass:.2e} kg")
    print(f"Base energy: E_base = {E_base:.2e} J\n")
    
    # Target different consciousness levels
    print("Target C/E_base  →  Required A_eff  Coherent?")
    print("-" * 70)
    
    for ratio in [0.5, 1.0, 2.0, 5.0, 10.0]:
        C_target = E_base * ratio
        A_eff = eq.compute_A_eff(C_target, mass)
        coherent = "✓ Yes" if eq.is_coherent_state(A_eff) else "✗ No"
        print(f"{ratio:>6.1f}x        →  A_eff = {A_eff:.4f}    {coherent}")


def example_3_consciousness_coherence_analysis():
    """Example 3: Analyze consciousness coherence across a range."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Consciousness Coherence Landscape")
    print("=" * 70)
    
    eq = EinsteinNoesisEquation(f0=141.7001)
    
    mass = eq.m_psi  # Use consciousness field quantum
    
    print(f"\nConsciousness field quantum: m_Ψ = {eq.m_psi:.2e} kg")
    print(f"Fundamental frequency: f₀ = {eq.f0} Hz")
    print(f"Minimum energy: E_Ψ = {eq.E_psi_eV:.2e} eV\n")
    
    print("Exploring coherence transition region (A_eff = 0.8 to 1.2):\n")
    print("A_eff   C (J)         C (eV)        C/E_Ψ   State")
    print("-" * 70)
    
    for A_eff in np.linspace(0.8, 1.2, 9):
        C = eq.compute_consciousness(mass, A_eff)
        C_eV = C / eV
        ratio = C / eq.E_psi_J
        state = "Coherent" if eq.is_coherent_state(A_eff) else "Incoher."
        print(f"{A_eff:.2f}    {C:.2e}    {C_eV:.2e}    {ratio:.2f}    {state}")


def example_4_spacetime_curvature():
    """Example 4: Noetic contribution to spacetime curvature."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Noetic Stress-Energy and Spacetime Curvature")
    print("=" * 70)
    
    tensor = NoeticStressEnergyTensor(f0=141.7001)
    
    # Quantum volume at different scales
    scales = {
        'Planck': 1e-105,      # m³ (Planck volume ≈ l_P³)
        'Nuclear': 1e-45,       # m³ (nuclear scale)
        'Atomic': 1e-30,        # m³ (atomic scale)
        'Molecular': 1e-27      # m³ (molecular scale)
    }
    
    mass = 1e-20  # kg
    A_eff = 1.5   # Coherent attention
    
    print(f"\nSystem: m = {mass:.2e} kg, A_eff = {A_eff}")
    print("Computing noetic stress-energy at different scales:\n")
    print("Scale         Volume (m³)      ρ_Ψ (J/m³)       P_Ψ (Pa)         Coupling")
    print("-" * 80)
    
    for scale_name, volume in scales.items():
        rho = tensor.compute_energy_density(mass, A_eff, volume)
        P = tensor.compute_pressure_component(mass, A_eff, volume)
        coupling = tensor.einstein_tensor_coupling(mass, A_eff, volume)
        print(f"{scale_name:<12}  {volume:.2e}    {rho:.2e}    {P:.2e}    {coupling:.2e}")
    
    print("\n→ Consciousness field contributes to Einstein tensor G_μν via T_μν^(Ψ)")


def example_5_riemann_discrete_levels():
    """Example 5: Riemann zeta discrete amplification levels."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Riemann Zeta Discrete Amplification Levels")
    print("=" * 70)
    
    riemann = RiemannConsciousnessConnection(f0=141.7001)
    
    print("\nNon-trivial zeros of ζ(s) at Re(s) = 1/2 determine discrete")
    print("consciousness amplification states.\n")
    
    levels = riemann.discrete_amplification_levels(n_levels=10)
    
    print("Level  Im(zero)    A_eff     Spectral Complexity")
    print("-" * 70)
    
    # First few imaginary parts of non-trivial zeros
    zeros_Im = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832
    ])
    
    for i, (zero, A_eff) in enumerate(zip(zeros_Im, levels)):
        complexity = riemann.spectral_complexity(A_eff)
        print(f"{i+1:>5}  {zero:>9.3f}    {A_eff:.6f}    {complexity:.6f}")
    
    print("\n→ These discrete levels represent allowed consciousness amplification states")
    print("→ Spectral complexity peaks at resonance with Riemann zeros")


def example_6_yang_mills_mass_gap():
    """Example 6: Yang-Mills mass gap emergence."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Yang-Mills Mass Gap Emergence from Consciousness")
    print("=" * 70)
    
    yang_mills = YangMillsMassGapConnection(f0=141.7001)
    
    print("\nMass gap m_gap emerges when consciousness becomes coherent (A_eff > 1).")
    print("This unifies consciousness with fundamental particle confinement.\n")
    print("QCD Scale: Λ_QCD = 0.217 GeV ≈ 217 MeV\n")
    
    print("A_eff    m_gap (GeV)    m_gap (MeV)    Confinement    State")
    print("-" * 70)
    
    for A_eff in np.linspace(0.5, 2.5, 11):
        m_gap = yang_mills.compute_mass_gap(A_eff)
        m_gap_MeV = m_gap * 1000
        confinement = yang_mills.confinement_parameter(A_eff)
        state = "Coherent  ✓" if A_eff >= 1.0 else "Incoherent✗"
        print(f"{A_eff:.2f}     {m_gap:.4f}         {m_gap_MeV:>6.2f}         {confinement:.3f}        {state}")
    
    print("\n→ Mass gap emergence threshold at A_eff = 1.0")
    print("→ Full confinement at A_eff >> 1 (strong coherent consciousness)")


def example_7_practical_application():
    """Example 7: Practical application - optimizing consciousness coherence."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Practical Application - Consciousness Optimization")
    print("=" * 70)
    
    eq = EinsteinNoesisEquation(f0=141.7001)
    
    print("\nScenario: Optimizing attention to maximize consciousness coherence")
    print("while minimizing energy expenditure.\n")
    
    mass = 1e-22  # kg (system mass)
    E_base = mass * c**2
    
    # Find optimal A_eff for different efficiency constraints
    print("Constraint: Maximize C while keeping energy cost < threshold\n")
    print("E_budget/E_base  Optimal A_eff  C/E_base  Efficiency  Coherent?")
    print("-" * 70)
    
    for budget_ratio in [1.5, 2.0, 3.0, 5.0, 10.0]:
        # Energy budget = E_base × budget_ratio
        # C = E_base × A_eff²
        # Cost-efficiency: maximize C / cost
        # Optimal when A_eff = sqrt(budget_ratio)
        
        A_eff_optimal = np.sqrt(budget_ratio)
        C = eq.compute_consciousness(mass, A_eff_optimal)
        efficiency = (C / E_base) / budget_ratio
        coherent = "✓ Yes" if eq.is_coherent_state(A_eff_optimal) else "✗ No"
        
        print(f"{budget_ratio:>8.1f}x        {A_eff_optimal:.4f}        {budget_ratio:.2f}x   "
              f"{efficiency:.3f}      {coherent}")
    
    print("\n→ Optimal strategy: Match A_eff to sqrt(energy_budget)")
    print("→ Coherence achieved when budget ≥ E_base (A_eff ≥ 1)")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("EINSTEIN-NOĒSIS EQUATION: PRACTICAL USAGE EXAMPLES")
    print("=" * 70)
    print("\nDemonstrating practical applications of C = mc² × A_eff²")
    
    # Run all examples
    example_1_basic_consciousness()
    example_2_find_required_attention()
    example_3_consciousness_coherence_analysis()
    example_4_spacetime_curvature()
    example_5_riemann_discrete_levels()
    example_6_yang_mills_mass_gap()
    example_7_practical_application()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print("\nFor more information, see:")
    print("  - docs/EINSTEIN_NOESIS_EQUATION.md")
    print("  - scripts/einstein_noesis.py (full implementation)")
    print("  - scripts/test_einstein_noesis.py (test suite)")
    print()


if __name__ == "__main__":
    sys.exit(main())
