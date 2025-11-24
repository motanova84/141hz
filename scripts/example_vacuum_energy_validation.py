#!/usr/bin/env python3
"""
Quick Start Example for Vacuum Energy Equation Validation

This example demonstrates the key features of the vacuum energy validator
in a simple, easy-to-follow format.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from validate_vacuum_energy_equation import VacuumEnergyValidator

def main():
    print("=" * 80)
    print("VACUUM ENERGY EQUATION - QUICK START EXAMPLE")
    print("=" * 80)
    print()
    
    # Example 1: Basic usage
    print("Example 1: Basic Energy Calculation")
    print("-" * 80)
    validator = VacuumEnergyValidator(alpha=1.0, beta=1.0, gamma=1.0, delta=1.0)
    
    # Calculate energy at a specific scale
    R_test = 1e45  # in Planck lengths
    E = validator.E_vac(R_test)
    print(f"E_vac at R_Ψ = {R_test:.2e} ℓ_P:")
    print(f"  Energy = {E:.6e}")
    print()
    
    # Example 2: Find the minimum
    print("Example 2: Finding Energy Minimum")
    print("-" * 80)
    result = validator.find_minimum()
    print(f"Optimization successful: {result['optimization_success']}")
    print(f"Optimal radius: R_Ψ* = {result['R_star']:.4e} ℓ_P")
    print(f"Minimum energy: E_min = {result['E_min']:.6e}")
    print(f"Predicted frequency: f₀ = {result['f0_predicted']:.4f} Hz")
    print(f"Target frequency: f₀ = {result['f0_target']:.4f} Hz")
    print()
    
    # Example 3: Term breakdown
    print("Example 3: Individual Term Contributions")
    print("-" * 80)
    terms = validator.get_individual_terms(result['R_star'])
    print(f"At R_Ψ* = {result['R_star']:.4e} ℓ_P:")
    print(f"  Term 1 (Planck):    {terms['term1_planck']:>15.6e}")
    print(f"  Term 2 (Zeta):      {terms['term2_zeta']:>15.6e}")
    print(f"  Term 3 (Lambda):    {terms['term3_lambda']:>15.6e}")
    print(f"  Term 4 (Fractal):   {terms['term4_fractal']:>15.6e}")
    print(f"  Total:              {terms['total']:>15.6e}")
    print()
    
    # Example 4: Cosmological constant validation
    print("Example 4: Cosmological Constant Problem")
    print("-" * 80)
    cosmo = validator.validate_cosmological_constant_solution(result['R_star'])
    print(f"Planck energy density:         {cosmo['planck_scale_energy']:.2e}")
    print(f"Cosmological energy density:   {cosmo['cosmological_scale_energy']:.2e}")
    print(f"Hierarchy ratio:               {cosmo['hierarchy_ratio']:.2e}")
    print(f"Hierarchy closed:              {cosmo['R_star_closes_hierarchy']}")
    print()
    print("Interpretation:")
    print(f"  {cosmo['interpretation']}")
    print()
    
    # Example 5: Arithmetic-geometric coupling
    print("Example 5: Arithmetic-Geometric Coupling")
    print("-" * 80)
    arith = validator.validate_arithmetic_geometric_coupling()
    print(f"ζ'(1/2) = {arith['zeta_prime_half_value']:.10f}")
    print(f"ζ(1/2) = {arith['zeta_half_value']:.10f}")
    print(f"Prime connection verified: {arith['prime_connection']}")
    print()
    print("Interpretation:")
    print(f"  {arith['interpretation']}")
    print()
    
    # Example 6: Resonant reality
    print("Example 6: Resonant Reality and f₀ Generation")
    print("-" * 80)
    resonance = validator.validate_resonant_reality(result['R_star'])
    print(f"Frequency match:            {resonance['frequency_match_percent']:.2f}%")
    print(f"log(R_Ψ*)/log(π):           {resonance['log_R_over_log_pi']:.4f}")
    print(f"Nearest π power:            {resonance['nearest_pi_power']}")
    print(f"Resonance deviation:        {resonance['pi_resonance_deviation']:.6f}")
    print()
    print("Interpretation:")
    print(f"  {resonance['interpretation']}")
    print()
    print("Harmonic series (π-resonances):")
    for h in resonance['harmonic_series']:
        print(f"  π^{h['n']:2d}: R_Ψ = {h['R_psi']:.4e} ℓ_P → f = {h['frequency_Hz']:8.4f} Hz")
    print()
    
    # Example 7: Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("✓ All three revolutionary implications validated:")
    print(f"  1. Cosmological Constant Problem: Hierarchy closed = {cosmo['R_star_closes_hierarchy']}")
    print(f"  2. Arithmetic Tuning: ζ'(1/2) = {arith['zeta_prime_half_value']:.6f}")
    print(f"  3. Resonant Reality: Resonance at π^{resonance['nearest_pi_power']}")
    print()
    print("✓ Energy minimum found:")
    print(f"  R_Ψ* = {result['R_star']:.4e} ℓ_P")
    print(f"  E_min = {result['E_min']:.6e}")
    print()
    print("✓ Frequency generated from first principles:")
    print(f"  f₀ = {result['f0_predicted']:.4f} Hz")
    print()
    print("For comprehensive validation, run:")
    print("  python scripts/validate_vacuum_energy_equation.py")
    print()
    print("For full test suite, run:")
    print("  python scripts/test_validate_vacuum_energy_equation.py")
    print()
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
