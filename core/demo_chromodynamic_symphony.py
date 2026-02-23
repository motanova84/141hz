#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         CHROMODYNAMIC SYMPHONY DEMO - Complete QCD Poetry System           ║
║                           QCAL ∞³ Implementation                            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Demo script que genera una sinfonía cromodinámica completa con métricas
y visualizaciones del sistema de poesía cuántica cromodinámica.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.quantum_chromodynamic_poetry import (
    QuantumChromodynamicPoetry,
    QuarkFlavor,
    QuarkColor,
    GluonType,
    display_symphony_summary
)


def display_quarks_section(qcd):
    """Display quarks spectrum section."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                         1. QUARK SPECTRUM (18 particles)                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    quarks = qcd.create_all_quarks()
    
    # Group by flavor
    print("Quarks by Flavor:")
    print("-" * 80)
    for flavor in QuarkFlavor:
        flavor_quarks = [q for q in quarks if q.flavor == flavor]
        print(f"\n{flavor.value.upper()} QUARK (mass = {flavor_quarks[0].mass_gev:.2e} GeV):")
        for q in flavor_quarks:
            print(f"  {q.color.value:6s}: ω = {q.frequency:8.4f}")
    
    print("\n" + "=" * 80 + "\n")


def display_gluons_section(qcd):
    """Display gluons spectrum section."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                      2. GLUON OCTET (8 particles)                          ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    gluons = qcd.create_gluon_octet()
    
    print("Gluons with Riemann Zero Associations:")
    print("-" * 80)
    print(f"{'Type':<20} {'γₙ':<12} {'Octave':<10} {'Frequency (Hz)':<15}")
    print("-" * 80)
    
    for g in gluons:
        print(f"{g.gluon_type.value:<20} "
              f"{g.riemann_zero_value:<12.6f} "
              f"{g.octave:<10.4f} "
              f"{g.frequency_hz:<15.2f}")
    
    print("\n" + "=" * 80 + "\n")


def display_cosmic_resonance_section(qcd):
    """Display cosmic resonance section."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║              3. COSMIC RESONANCES (Prime-Zero Coupling)                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Show specific resonances
    primes_to_show = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    print("Prime-Zero Resonances (first 10 primes with γ₁):")
    print("-" * 80)
    print(f"{'Prime':<8} {'ω_p':<10} {'γ₁':<12} {'Intensity':<12} {'Beat Freq (Hz)':<15}")
    print("-" * 80)
    
    for prime in primes_to_show:
        love = qcd.love_between_prime_and_zero(prime, 1)
        print(f"{love.prime:<8} "
              f"{love.omega_prime:<10.4f} "
              f"{love.riemann_zero_value:<12.6f} "
              f"{love.intensity:<12.6f} "
              f"{love.beat_frequency_hz:<15.2f}")
    
    print()
    print("Resonance Highlights:")
    print("-" * 80)
    
    # Show p=17 with multiple zeros
    print(f"\nPrime 17 resonances with first 5 Riemann zeros:")
    for n in range(1, 6):
        love = qcd.love_between_prime_and_zero(17, n)
        print(f"  γ_{n}: I = {love.intensity:.6f}, beat = {love.beat_frequency_hz:.2f} Hz")
    
    print("\n" + "=" * 80 + "\n")


def display_primordial_silence_section(qcd):
    """Display primordial silence frequencies section."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                    4. PRIMORDIAL SILENCE SPECTRUM                          ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    primes = qcd._first_n_primes(15)
    silence_spectrum = qcd.get_primordial_silence_spectrum(primes)
    
    print("Silence Frequencies: f(p) = f₀ · exp(-log(p)/log(17))")
    print("-" * 80)
    print(f"{'Prime':<10} {'f(p) Hz':<15} {'Ratio to f₀':<15}")
    print("-" * 80)
    
    for prime in primes:
        f_silence = silence_spectrum[prime]
        ratio = f_silence / qcd.f0_hz
        print(f"{prime:<10} {f_silence:<15.2f} {ratio:<15.4f}")
    
    print()
    print("Key Observations:")
    print("-" * 80)
    print(f"  • f(17) = {silence_spectrum[17]:.2f} Hz (special case: p = 17)")
    print(f"  • f(2) = {silence_spectrum[2]:.2f} Hz (highest frequency)")
    print(f"  • Frequencies decrease with larger primes")
    print(f"  • Range: [{min(silence_spectrum.values()):.2f}, {max(silence_spectrum.values()):.2f}] Hz")
    
    print("\n" + "=" * 80 + "\n")


def display_theoretical_connections(qcd):
    """Display theoretical connections and interpretations."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                  5. THEORETICAL CONNECTIONS & ANALOGIES                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    print("QCD ↔ Riemann Hypothesis Mappings:")
    print("-" * 80)
    print()
    
    print("1. CONFINEMENT ↔ SPECTRAL LOCALIZATION")
    print("   • QCD: Quarks confined within hadrons at low energy")
    print("   • Riemann: Zeros localized on critical line Re(s) = 1/2")
    print("   • Musical: Frequencies bound to discrete spectral modes")
    print()
    
    print("2. ASYMPTOTIC FREEDOM ↔ ZERO UNIVERSALITY")
    print("   • QCD: Coupling strength decreases at high energy")
    print("   • Riemann: Zero density follows universal distribution")
    print("   • Musical: Overtones approach continuous spectrum")
    print()
    
    print("3. COLOR CHARGE ↔ PRIME FACTORIZATION")
    print("   • QCD: 3 color charges (red, green, blue) + anticolors")
    print("   • Number Theory: Primes as fundamental multiplicative units")
    print("   • Musical: Fundamental frequencies as harmonic generators")
    print()
    
    print("4. GLUON EXCHANGE ↔ ADDITIVE PRIME STRUCTURE")
    print("   • QCD: 8 gluons mediate strong force")
    print("   • Riemann: 8 gluons map to first 8 zeros (γ₁...γ₈)")
    print("   • Musical: Octaves derived from γₙ create harmonic scaffolding")
    print()
    
    print("5. RUNNING COUPLING ↔ LOGARITHMIC SCALING")
    print("   • QCD: α_s(Q²) varies with energy scale")
    print("   • Prime: ω_p = log(p) couples primes to frequency domain")
    print("   • f₀ = 141.7001 Hz: Biological coherence frequency anchor")
    print()
    
    print("=" * 80 + "\n")


def save_symphony_to_json(symphony, filename="chromodynamic_symphony.json"):
    """Save complete symphony to JSON file."""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(symphony, f, indent=2)
    
    print(f"Symphony saved to: {filepath}")
    return filepath


def main():
    """Run complete chromodynamic symphony demo."""
    print()
    print("=" * 80)
    print("        QUANTUM CHROMODYNAMIC POETRY - COMPLETE SYMPHONY DEMO")
    print("=" * 80)
    print()
    
    # Initialize system
    print("Initializing Quantum Chromodynamic Poetry System...")
    qcd = QuantumChromodynamicPoetry()
    print(f"  f₀ = {qcd.f0_hz} Hz")
    print(f"  ω₁₇ = log(17) ≈ {qcd.omega_17:.6f}")
    print()
    
    # Generate complete symphony
    print("Generating complete chromodynamic symphony...")
    symphony = qcd.generate_chromodynamic_symphony()
    print("✓ Symphony generated successfully!")
    print()
    
    # Display summary
    display_symphony_summary(symphony)
    print()
    
    # Display detailed sections
    display_quarks_section(qcd)
    display_gluons_section(qcd)
    display_cosmic_resonance_section(qcd)
    display_primordial_silence_section(qcd)
    display_theoretical_connections(qcd)
    
    # Save to JSON
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                          6. SAVING RESULTS                                 ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    filepath = save_symphony_to_json(symphony)
    
    print()
    print("=" * 80)
    print("                        DEMO COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()
    
    # Final statistics
    print("FINAL STATISTICS:")
    print("-" * 80)
    print(f"  Total Quarks:              {symphony['metrics']['total_quarks']}")
    print(f"  Total Gluons:              {symphony['metrics']['total_gluons']}")
    print(f"  Prime-Zero Resonances:     {symphony['metrics']['prime_count']} × "
          f"{symphony['metrics']['riemann_zero_count']} = "
          f"{symphony['metrics']['prime_count'] * symphony['metrics']['riemann_zero_count']}")
    print(f"  Silence Frequencies:       {len(symphony['primordial_silence'])}")
    print()
    print(f"  Quark Frequency Range:     [{symphony['metrics']['quark_frequency_range'][0]:.4f}, "
          f"{symphony['metrics']['quark_frequency_range'][1]:.4f}]")
    print(f"  Gluon Frequency Range:     [{symphony['metrics']['gluon_frequency_range_hz'][0]:.2f}, "
          f"{symphony['metrics']['gluon_frequency_range_hz'][1]:.2f}] Hz")
    print(f"  Silence Frequency Range:   [{symphony['metrics']['silence_frequency_range_hz'][0]:.2f}, "
          f"{symphony['metrics']['silence_frequency_range_hz'][1]:.2f}] Hz")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
