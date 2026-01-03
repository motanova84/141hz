#!/usr/bin/env python3
"""
Example: Using the Vacuum Energy Module
Demonstrates various use cases and capabilities
"""
import numpy as np
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vacuum_energy import E_vac_log, optimize_vacuum_energy, analyze_vacuum_energy


def example_1_basic_calculation():
    """Example 1: Basic energy calculation at specific scales"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Energy Calculation")
    print("=" * 70)
    print()
    
    # Calculate energy at different radius scales
    scales = [40, 42, 45, 48, 50]
    
    print("Energy at different radius scales:")
    print(f"{'log(R/ℓ_P)':<15} {'R/ℓ_P':<20} {'Energy':<15}")
    print("-" * 50)
    
    for log_r in scales:
        energy = E_vac_log(log_r)
        R = 10**log_r
        print(f"{log_r:<15.1f} {R:<20.2e} {energy:<15.6e}")
    
    print()


def example_2_find_minimum():
    """Example 2: Find minimum energy configuration"""
    print("=" * 70)
    print("EXAMPLE 2: Find Minimum Energy")
    print("=" * 70)
    print()
    
    # Optimize in default range
    print("Finding minimum energy in range log(R) ∈ [40, 50]...")
    result = optimize_vacuum_energy(bounds=(40, 50))
    
    print(f"\nOptimization Results:")
    print(f"  Status:           {result.success}")
    print(f"  Optimal log(R):   {result.x:.6f}")
    print(f"  Minimum energy:   {result.fun:.6e}")
    print(f"  Iterations:       {result.nfev if hasattr(result, 'nfev') else 'N/A'}")
    
    # Calculate radius in different units
    R_planck = 10**result.x
    print(f"\n  Optimal radius:")
    print(f"    In Planck units: {R_planck:.6e} ℓ_P")
    
    print()


def example_3_compare_ranges():
    """Example 3: Compare optimization in different ranges"""
    print("=" * 70)
    print("EXAMPLE 3: Compare Different Search Ranges")
    print("=" * 70)
    print()
    
    ranges = [
        (40, 45, "Small radii"),
        (45, 50, "Large radii"),
        (42, 48, "Mid-range"),
        (40, 50, "Full range")
    ]
    
    print(f"{'Range':<20} {'Description':<15} {'Optimal log(R)':<20} {'Min Energy':<15}")
    print("-" * 70)
    
    for low, high, desc in ranges:
        result = optimize_vacuum_energy(bounds=(low, high))
        print(f"[{low}, {high}]"  + " " * (20 - len(f"[{low}, {high}]")) + 
              f"{desc:<15} {result.x:<20.6f} {result.fun:<15.6e}")
    
    print()


def example_4_detailed_analysis():
    """Example 4: Detailed analysis with term breakdown"""
    print("=" * 70)
    print("EXAMPLE 4: Detailed Analysis with Term Breakdown")
    print("=" * 70)
    print()
    
    # Perform full analysis
    analysis = analyze_vacuum_energy()
    details = analysis['analysis']
    
    print("Complete Energy Analysis at Optimum:")
    print()
    print(f"Optimal Configuration:")
    print(f"  log(R/ℓ_P):       {details['log_r_opt']:.8f}")
    print(f"  R/ℓ_P:            {details['R_opt']:.6e}")
    print(f"  Total energy:     {details['E_min']:.6e}")
    print()
    
    print("Individual Term Contributions:")
    print(f"  Planck (α/R⁴):    {details['term1_planck']:.6e}")
    print(f"  Quantum (βζ'/R²): {details['term2_quantum']:.6e}")
    print(f"  Lambda (γΛ²R²):   {details['term3_lambda']:.6e}")
    print(f"  Oscillatory:      {details['term4_oscillatory']:.6e}")
    print()
    
    # Calculate relative importance
    total_abs = sum(abs(v) for k, v in details.items() 
                   if k.startswith('term'))
    
    if total_abs > 0:
        print("Relative Importance (by absolute magnitude):")
        for term_name, key in [
            ("Planck", "term1_planck"),
            ("Quantum", "term2_quantum"),
            ("Lambda", "term3_lambda"),
            ("Oscillatory", "term4_oscillatory")
        ]:
            percentage = abs(details[key]) / total_abs * 100
            print(f"  {term_name:<15} {percentage:>6.2f}%")
    
    print()


def example_5_energy_scan():
    """Example 5: Scan energy across range"""
    print("=" * 70)
    print("EXAMPLE 5: Energy Scan Across Range")
    print("=" * 70)
    print()
    
    # Scan across range
    log_r_values = np.linspace(40, 50, 21)  # 21 points
    
    print("Energy scan results:")
    print(f"{'log(R)':<12} {'Energy':<18} {'Relative to min':<20}")
    print("-" * 50)
    
    # Get minimum for comparison
    result_min = optimize_vacuum_energy(bounds=(40, 50))
    E_min = result_min.fun
    
    for log_r in log_r_values:
        energy = E_vac_log(log_r)
        relative = (energy - E_min) / E_min if E_min != 0 else 0
        print(f"{log_r:<12.2f} {energy:<18.6e} {relative:+.6e}")
    
    print()
    print(f"Minimum occurs at log(R) = {result_min.x:.6f}")
    print()


def example_6_custom_calculation():
    """Example 6: Custom calculation with explanation"""
    print("=" * 70)
    print("EXAMPLE 6: Understanding the Calculation")
    print("=" * 70)
    print()
    
    # Choose a specific point
    log_r = 45.0
    R = 10**log_r
    
    print(f"Calculating energy at log(R) = {log_r}")
    print(f"This corresponds to R = 10^{log_r} = {R:.6e} Planck lengths")
    print()
    
    # Import parameters
    from vacuum_energy import alpha, beta, gamma, delta, zeta_prime, Lambda, pi_val
    
    print("Parameters:")
    print(f"  α (alpha):      {alpha}")
    print(f"  β (beta):       {beta}")
    print(f"  γ (gamma):      {gamma}")
    print(f"  δ (delta):      {delta}")
    print(f"  ζ' (zeta'):     {zeta_prime}")
    print(f"  Λ (Lambda):     {Lambda}")
    print(f"  π (pi):         {pi_val:.6f}")
    print()
    
    # Calculate each term step by step
    print("Step-by-step calculation:")
    
    term1 = alpha / R**4
    print(f"  1. Planck term:        α/R⁴ = {alpha}/{R:.2e}⁴ = {term1:.6e}")
    
    term2 = beta * zeta_prime / R**2
    print(f"  2. Quantum term:       βζ'/R² = {beta}×{zeta_prime}/{R:.2e}² = {term2:.6e}")
    
    term3 = gamma * Lambda**2 * R**2
    print(f"  3. Lambda term:        γΛ²R² = {gamma}×{Lambda}²×{R:.2e}² = {term3:.6e}")
    
    log_R_natural = np.log(R)
    log_pi = np.log(pi_val)
    sin_arg = log_R_natural / log_pi
    term4 = delta * np.sin(sin_arg)**2
    print(f"  4. Oscillatory term:   δsin²(ln(R)/ln(π)) = {delta}×sin²({sin_arg:.2f}) = {term4:.6e}")
    
    total = term1 + term2 + term3 + term4
    print()
    print(f"Total energy: {total:.6e}")
    
    # Verify with function
    energy_func = E_vac_log(log_r)
    print(f"Function result: {energy_func:.6e}")
    print(f"Match: {'✓' if np.isclose(total, energy_func) else '✗'}")
    print()


def main():
    """Run all examples"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "VACUUM ENERGY MODULE EXAMPLES" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    examples = [
        example_1_basic_calculation,
        example_2_find_minimum,
        example_3_compare_ranges,
        example_4_detailed_analysis,
        example_5_energy_scan,
        example_6_custom_calculation
    ]
    
    for example in examples:
        example()
    
    print("=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    print()
    print("For more information, see:")
    print("  • Documentation: docs/VACUUM_ENERGY.md")
    print("  • Tests: scripts/test_vacuum_energy.py")
    print("  • Visualization: scripts/visualize_vacuum_energy.py")
    print()


if __name__ == "__main__":
    main()
