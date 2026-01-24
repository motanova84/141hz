#!/usr/bin/env python3
"""
Simple Example: Using the Explicit Function f for κ_Π
======================================================

This script demonstrates the basic usage of the explicit function
f(h₁₁, h₂₁) → κ_Π.

Author: JMMB Ψ✧
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kappa_pi_function import (
    kappa_pi_function,
    kappa_pi_ideal,
    get_universal_kappa_pi
)


def main():
    """Simple examples of using the function f."""
    
    print("=" * 70)
    print("SIMPLE EXAMPLE: Explicit Function f for κ_Π")
    print("=" * 70)
    print()
    
    # Example 1: Universal value
    print("Example 1: Universal κ_Π value")
    print("-" * 70)
    kappa_universal = get_universal_kappa_pi()
    print(f"Universal κ_Π = {kappa_universal}")
    print()
    
    # Example 2: Ideal parameters
    print("Example 2: Ideal parameters (α=0.385, β=0.244)")
    print("-" * 70)
    kappa_ideal = kappa_pi_ideal()
    print(f"κ_Π (ideal) = {kappa_ideal:.6f}")
    print()
    
    # Example 3: Quintic Calabi-Yau
    print("Example 3: Quintic Calabi-Yau (h¹¹=1, h²¹=101)")
    print("-" * 70)
    kappa_quintic = kappa_pi_function(1, 101)
    print(f"κ_Π (quintic) = {kappa_quintic:.6f}")
    print()
    
    # Example 4: Different Calabi-Yau manifolds
    print("Example 4: Different Calabi-Yau manifolds")
    print("-" * 70)
    manifolds = [
        ("Small h²¹", 1, 20),
        ("Medium h²¹", 1, 50),
        ("Standard quintic", 1, 101),
        ("Large h²¹", 1, 200),
    ]
    
    print(f"{'Manifold':<20} {'h¹¹':>5} {'h²¹':>6} {'κ_Π':>10}")
    print("-" * 45)
    for name, h11, h21 in manifolds:
        kappa = kappa_pi_function(h11, h21)
        print(f"{name:<20} {h11:5d} {h21:6d} {kappa:10.6f}")
    print()
    
    # Example 5: Detailed output
    print("Example 5: Detailed output for quintic CY")
    print("-" * 70)
    result = kappa_pi_function(1, 101, return_details=True)
    print(f"κ_Π  = {result['kappa_pi']:.6f}")
    print(f"α    = {result['alpha']:.6f}")
    print(f"β    = {result['beta']:.6f}")
    print(f"Z    = {result['Z']:.6f}")
    print(f"h¹¹  = {result['h11']}")
    print(f"h²¹  = {result['h21']}")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print(f"✓ Universal κ_Π = {kappa_universal}")
    print(f"✓ Ideal case κ_Π = {kappa_ideal:.6f}")
    print(f"✓ Quintic CY κ_Π = {kappa_quintic:.6f}")
    print()
    print("The explicit function f(h₁₁, h₂₁) is now available for use!")
    print()


if __name__ == "__main__":
    main()
