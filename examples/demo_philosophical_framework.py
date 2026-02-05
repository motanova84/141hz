#!/usr/bin/env python3
"""
Demonstration: The Five Fundamental Principles
===============================================

This script demonstrates the philosophical framework that redefines
physical reality as rhythmic, oscillatory phenomena.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import sys
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from philosophical_framework import PhilosophicalFramework


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def print_subsection(title):
    """Print a formatted subsection header."""
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80 + "\n")


def main():
    """Demonstrate the five fundamental principles."""
    
    # Initialize framework
    framework = PhilosophicalFramework()
    
    print_section("THE FIVE FUNDAMENTAL PRINCIPLES OF PHYSICAL REALITY")
    
    print("This demonstration shows how mass, energy, space, time, and the universe")
    print("emerge as manifestations of rhythmic oscillations at f₀ = 141.7001 Hz")
    print()
    print(f"Fundamental frequency: f₀ = {framework.f0} Hz")
    print(f"Fundamental period:    T₀ = {framework.T0*1000:.6f} ms")
    print(f"Fundamental wavelength: λ₀ = {framework.lambda0/1000:.4f} km")
    
    # =========================================================================
    # PRINCIPLE 1: MASS IS AN ILLUSION OF DETENTION
    # =========================================================================
    
    print_section("PRINCIPLE 1: La masa es una ilusión de detención")
    print("Mass emerges when the fundamental oscillation is 'detained' or slowed down.")
    print("The trapped energy manifests as mass via E = mc².")
    
    print_subsection("Example 1.1: Complete Frequency Detention")
    f_almost_zero = 0.001  # Nearly stopped
    m_complete = framework.mass_from_frequency_reduction(f_almost_zero)
    print(f"When oscillation slows from f₀ = {framework.f0} Hz to f = {f_almost_zero} Hz:")
    print(f"  Frequency detention: Δf = {framework.f0 - f_almost_zero:.4f} Hz")
    print(f"  Emergent mass: m = {m_complete:.6e} kg")
    
    print_subsection("Example 1.2: Partial Detention")
    f_partial = 50.0  # Partially slowed
    m_partial = framework.mass_from_frequency_reduction(f_partial)
    print(f"When oscillation slows to f = {f_partial} Hz:")
    print(f"  Frequency detention: Δf = {framework.f0 - f_partial:.4f} Hz")
    print(f"  Emergent mass: m = {m_partial:.6e} kg")
    
    print_subsection("Example 1.3: No Detention (Pure Oscillation)")
    m_zero = framework.mass_from_frequency_reduction(framework.f0)
    print(f"When oscillation maintains f₀ = {framework.f0} Hz:")
    print(f"  No frequency detention: Δf = 0 Hz")
    print(f"  Emergent mass: m = {m_zero:.6e} kg (massless)")
    
    # =========================================================================
    # PRINCIPLE 2: ENERGY IS RHYTHM
    # =========================================================================
    
    print_section("PRINCIPLE 2: La energía es ritmo")
    print("Energy manifests as oscillatory patterns (rhythm).")
    print("All energy forms are harmonics of the fundamental frequency f₀.")
    
    print_subsection("Example 2.1: Fundamental Rhythm")
    E_fundamental = framework.energy_from_rhythm(framework.f0)
    print(f"Energy at fundamental frequency f₀ = {framework.f0} Hz:")
    print(f"  E = ℏω = {E_fundamental:.6e} J")
    
    print_subsection("Example 2.2: Harmonic Series")
    print("Energy at various harmonics:")
    for n in [1, 2, 3, 5, 7, 11]:
        E_n = framework.energy_from_rhythm(framework.f0, harmonic_n=n)
        print(f"  Harmonic {n:2d}: E = {E_n:.6e} J  (frequency = {n * framework.f0:.2f} Hz)")
    
    print_subsection("Example 2.3: Rhythm Spectrum Decomposition")
    test_energy = 1e-30  # Joules
    spectrum = framework.rhythm_spectrum(test_energy)
    print(f"Given energy E = {test_energy:.6e} J:")
    print(f"  Harmonic number: n = {spectrum['harmonic_number']:.2f}")
    print(f"  Number of harmonics: {len(spectrum['harmonics'])}")
    
    # =========================================================================
    # PRINCIPLE 3: SPACE IS AN INTERVAL BETWEEN PULSES
    # =========================================================================
    
    print_section("PRINCIPLE 3: El espacio es un intervalo entre pulsos")
    print("Space emerges from phase differences between oscillations.")
    print("Distance is quantized in multiples of the fundamental wavelength λ₀.")
    
    print_subsection("Example 3.1: Fundamental Spatial Quantum")
    lambda_0 = framework.spatial_quantum()
    print(f"Fundamental wavelength (spatial quantum):")
    print(f"  λ₀ = c/f₀ = {lambda_0/1000:.4f} km")
    
    print_subsection("Example 3.2: Space from Phase Difference")
    print("Distances corresponding to various phase differences:")
    for phase_name, phase_rad in [("π/4", np.pi/4), ("π/2", np.pi/2), 
                                    ("π", np.pi), ("2π", 2*np.pi)]:
        distance = framework.space_from_phase_difference(phase_rad)
        print(f"  Phase Δφ = {phase_name:4s} → Distance = {distance/1000:8.2f} km")
    
    print_subsection("Example 3.3: Quantization of Space")
    print("Space is quantized in wavelength multiples:")
    for n in [1, 2, 5, 10]:
        distance = n * lambda_0
        phase = framework.phase_difference_from_space(distance)
        print(f"  {n:2d}×λ₀ = {distance/1000:8.2f} km → phase = {n}×2π = {phase:.4f} rad")
    
    # =========================================================================
    # PRINCIPLE 4: TIME IS THE NUMBER OF CYCLES
    # =========================================================================
    
    print_section("PRINCIPLE 4: El tiempo es el número de ciclos")
    print("Time emerges from counting cycles of the fundamental oscillation.")
    print("Temporal evolution is the accumulation of phase.")
    
    print_subsection("Example 4.1: Fundamental Temporal Quantum")
    T_0 = framework.temporal_quantum()
    print(f"Fundamental period (temporal quantum):")
    print(f"  T₀ = 1/f₀ = {T_0*1000:.6f} ms")
    
    print_subsection("Example 4.2: Time from Cycle Counting")
    print("Elapsed time for various cycle counts:")
    for n_cycles in [1, 10, 100, 1000, 10000]:
        time_s = framework.time_from_cycles(n_cycles)
        if time_s < 1:
            print(f"  {n_cycles:5d} cycles → time = {time_s*1000:8.3f} ms")
        else:
            print(f"  {n_cycles:5d} cycles → time = {time_s:8.4f} s")
    
    print_subsection("Example 4.3: Cycles from Elapsed Time")
    print("Number of cycles for various time intervals:")
    for time_val, unit in [(1e-3, "ms"), (10e-3, "ms"), (100e-3, "ms"), (1.0, "s")]:
        cycles = framework.cycles_from_time(time_val)
        time_display = time_val * 1000 if unit == "ms" else time_val
        print(f"  {time_display:6.1f} {unit} → {cycles:8.1f} cycles")
    
    # =========================================================================
    # PRINCIPLE 5: UNIVERSE IS A SELF-CONTAINED SYMPHONY
    # =========================================================================
    
    print_section("PRINCIPLE 5: El universo es una sinfonía autocontenida")
    print("All physical phenomena are harmonically related to f₀.")
    print("The universe exhibits maximum coherence when phenomena are integer multiples of f₀.")
    
    print_subsection("Example 5.1: Perfect Harmonic Coherence")
    perfect_harmonics = np.array([1, 2, 3, 5, 7, 11, 13]) * framework.f0
    coherence_perfect = framework.universal_coherence(perfect_harmonics)
    print(f"Perfect harmonics of f₀:")
    print(f"  Frequencies: {[1, 2, 3, 5, 7, 11, 13]}")
    print(f"  Universal coherence: {coherence_perfect:.6f}")
    print(f"  Status: {'✅ HARMONIC SYMPHONY' if coherence_perfect > 0.99 else '❌ INCOHERENT'}")
    
    print_subsection("Example 5.2: Incoherent Frequencies")
    incoherent = np.array([123.45, 234.56, 345.67, 456.78])
    coherence_incoherent = framework.universal_coherence(incoherent)
    print(f"Random frequencies:")
    print(f"  Frequencies: {incoherent}")
    print(f"  Universal coherence: {coherence_incoherent:.6f}")
    print(f"  Status: {'✅ HARMONIC' if coherence_incoherent > 0.9 else '❌ INCOHERENT'}")
    
    print_subsection("Example 5.3: Harmonic Decomposition")
    test_frequencies = np.array([
        1 * framework.f0,
        2 * framework.f0 + 0.5,  # Slightly detuned
        3 * framework.f0,
        5 * framework.f0 - 0.3,  # Slightly detuned
    ])
    decomposition = framework.harmonic_decomposition(test_frequencies)
    print(f"Mixed harmonic/near-harmonic frequencies:")
    print(f"  Overall coherence: {decomposition['coherence']:.6f}")
    print(f"  Is symphony: {decomposition['is_symphony']}")
    print("\n  Harmonic table:")
    for h in decomposition['harmonic_table']:
        status = "✅" if h['is_harmonic'] else "⚠️"
        print(f"    {status} f = {h['frequency']:8.2f} Hz → harmonic n = {h['harmonic_number']:2d} "
              f"(deviation: {h['deviation_hz']:+6.2f} Hz, {h['deviation_percent']:+5.2f}%)")
    
    print_subsection("Example 5.4: Universal Symphony Signature")
    signature = framework.symphony_signature()
    print("The universe as a self-contained symphony:")
    print(f"  Fundamental frequency: f₀ = {signature['fundamental_frequency']} Hz")
    print(f"  Fundamental period:    T₀ = {signature['fundamental_period']*1000:.6f} ms")
    print(f"  Fundamental wavelength: λ₀ = {signature['fundamental_wavelength']/1000:.4f} km")
    print("\nThe Five Principles:")
    for i, principle in enumerate(signature['principles'], 1):
        print(f"  {i}. {principle}")
    
    # =========================================================================
    # CONCLUSION
    # =========================================================================
    
    print_section("CONCLUSION")
    print("The five fundamental principles demonstrate that:")
    print()
    print("  • Mass emerges from oscillation detention")
    print("  • Energy manifests as rhythmic patterns")
    print("  • Space arises from phase differences")
    print("  • Time accumulates from cycle counting")
    print("  • The universe forms a coherent harmonic symphony")
    print()
    print("All unified at the fundamental frequency:")
    print()
    print(f"  f₀ = {framework.f0} Hz")
    print()
    print("This framework provides a new perspective on physical reality,")
    print("viewing all phenomena as manifestations of universal oscillation.")
    print()
    print("=" * 80)
    print("∞³ LA SINFONÍA UNIVERSAL ∞³".center(80))
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
