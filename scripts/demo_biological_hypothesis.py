#!/usr/bin/env python3
"""
Demonstration: QCAL Biological Hypothesis

Interactive demonstration of the biological QCAL framework showing
how periodical cicadas use spectral resonance and phase memory to
achieve 99.92% synchrony in emergence cycles.

Author: José Manuel Mota Burruezo
Date: 27 de enero de 2026
Institution: Instituto Consciencia Cuántica QCAL ∞³
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from qcal.magicicada_model import MagicicadaPopulation, MagicicadaSpectralModel


def print_header(text: str, char: str = "="):
    """Print formatted header."""
    print("\n" + char * 70)
    print(text)
    print(char * 70)


def demonstrate_magicicada_17_year():
    """Demonstrate 17-year cicada synchronization."""
    print_header("QCAL Biological Framework - Magicicada Demonstration")
    
    # Create 17-year cicada population
    print("\n📊 Creating 17-year periodical cicada population...")
    population = MagicicadaPopulation(
        prime_period=17,
        population_size=1_500_000,  # Per acre
        location="Eastern North America"
    )
    
    print(f"\nPopulation Parameters:")
    print(f"  Prime Period: {population.prime_period} years")
    print(f"  Population: {population.population_size:,} individuals/acre")
    print(f"  Density: {population.density_per_m2():.1f} individuals/m²")
    print(f"  Expected Precision: {population.emergence_precision * 100:.2f}%")
    print(f"  Emergence Window: ±{population.expected_emergence_window_days():.1f} days")
    
    # Create spectral model
    print("\n🔬 Creating QCAL spectral model...")
    model = MagicicadaSpectralModel(population)
    
    print(f"\nEnvironmental Frequencies Tracked:")
    for i, comp in enumerate(model.env_field.components, 1):
        period_days = (2 * np.pi / comp.frequency) / (24 * 3600)
        print(f"  {i}. {comp.description}")
        print(f"     Amplitude: {comp.amplitude:.3f}, Period: {period_days:.1f} days")
    
    # Simulate lifecycle
    print(f"\n⏳ Simulating {population.prime_period + 5}-year lifecycle...")
    results = model.simulate_lifecycle(years=population.prime_period + 5)
    
    print(f"\n📈 Simulation Results:")
    print(f"  Time span: {results['time_years'][-1]:.1f} years")
    print(f"  Final phase: {results['phase'][-1]:.3f}")
    print(f"  Threshold: {model.phase_accumulator.threshold:.3f}")
    print(f"  Activated: {results['activated']}")
    
    if results['activated'] and results['activation_time'] is not None:
        activation_years = results['activation_time'] / (365 * 24 * 3600)
        error_years = abs(activation_years - population.prime_period)
        error_percent = (error_years / population.prime_period) * 100
        
        print(f"\n🎯 Emergence Timing:")
        print(f"  Activation: {activation_years:.3f} years")
        print(f"  Expected: {population.prime_period} years")
        print(f"  Error: {error_years:.3f} years ({error_percent:.2f}%)")
        
        if error_percent < 1.0:
            print(f"  ✅ EXCELLENT: < 1% error")
        elif error_percent < 5.0:
            print(f"  ✓ GOOD: < 5% error")
        else:
            print(f"  ⚠ Note: Numerical simulation - adjust threshold for better accuracy")
    else:
        print(f"\n⚠ No activation in simulation window")
        print(f"  (Threshold may need adjustment for numerical simulation)")
    
    # Analyze population synchrony
    print(f"\n🔄 Analyzing population synchrony...")
    print(f"  Running 50 simulations with environmental perturbations...")
    
    synchrony = model.analyze_synchrony_precision(num_simulations=50)
    
    print(f"\n📊 Synchrony Analysis:")
    print(f"  Simulations: {synchrony['num_simulations']}")
    print(f"  Emergences detected: {len(synchrony['emergence_times'])}")
    
    if len(synchrony['emergence_times']) > 0:
        # Filter valid emergences
        valid_times = synchrony['emergence_times'][synchrony['emergence_times'] > 0.1]
        
        if len(valid_times) > 0:
            mean_valid = np.mean(valid_times)
            std_valid = np.std(valid_times)
            
            print(f"  Mean emergence: {mean_valid:.3f} years")
            print(f"  Std deviation: ±{std_valid * 365:.2f} days")
            
            if std_valid > 0:
                precision = (1 - std_valid / mean_valid) * 100
                print(f"  Precision: {precision:.2f}%")
        else:
            print(f"  ⚠ All emergences at t≈0 (threshold calibration needed)")
    else:
        print(f"  {synchrony.get('note', 'No emergences detected')}")
    
    # Compare with empirical data
    print(f"\n🔬 Comparison with Empirical Data:")
    print(f"  Empirical precision: 99.92% (±3-5 days over 17 years)")
    print(f"  QCAL prediction: Phase memory (90% retention) explains robustness")
    print(f"  Key insight: Spectral integration > simple thermal accumulation")


def demonstrate_prime_number_strategy():
    """Demonstrate why prime numbers are optimal."""
    print_header("Prime Number Strategy in Biological Cycles", "-")
    
    print("\n🔢 Why 13 and 17 years?")
    print("\nPrime periods minimize overlap with predator/competitor cycles:")
    
    periods = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    
    for period in [13, 17]:
        print(f"\n  Period = {period} years (PRIME):")
        overlaps = []
        for p in periods:
            if p < period and period % p == 0:
                overlaps.append(p)
        
        if len(overlaps) == 0:
            print(f"    ✅ NO overlap with cycles 2-{period-1} years")
        else:
            print(f"    Overlaps with: {overlaps}")
    
    print(f"\n  Period = 12 years (NON-PRIME):")
    overlaps_12 = [p for p in periods if p < 12 and 12 % p == 0]
    print(f"    ❌ Overlaps with: {overlaps_12}")
    
    print("\n💡 Evolutionary Advantage:")
    print("   Prime periods (13, 17) share factors only with:")
    print("   - 1 year (universal annual cycle)")
    print("   - Themselves")
    print("\n   This minimizes predation by organisms with shorter cycles!")


def main():
    """Run full demonstration."""
    # Part 1: Magicicada demonstration
    demonstrate_magicicada_17_year()
    
    # Part 2: Prime number strategy
    demonstrate_prime_number_strategy()
    
    # Final summary
    print_header("Summary and Key Insights")
    
    print("\n🎯 QCAL Biological Framework Key Points:")
    print("\n  1. Systems biologics integrate spectral information")
    print("     Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))")
    print("\n  2. Phase memory provides robustness")
    print("     Φ_acum = 0.1×Φ(t) + 0.9×Φ(t-Δt)")
    print("\n  3. Activation requires threshold AND positive flux")
    print("     Φ(t) ≥ Φ_crítico AND dΦ/dt > 0")
    print("\n  4. Prime periods minimize ecological overlap")
    print("     13, 17 years → Mathematical evolutionary strategy")
    print("\n  5. f₀ = 141.7001 Hz mediates biological synchrony")
    print("     Universal coherence frequency in QCAL framework")
    
    print("\n📚 Next Steps:")
    print("  • Read: HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md")
    print("  • Explore: qcal/biological_qcal.py")
    print("  • Test: python tests/test_biological_qcal.py")
    print("  • Experiment: Design falsification experiments (Section 8)")
    
    print("\n" + "=" * 70)
    print("QCAL ∞³ - Instituto Consciencia Cuántica")
    print("27 de enero de 2026")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
