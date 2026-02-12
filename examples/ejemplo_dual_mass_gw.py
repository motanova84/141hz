#!/usr/bin/env python3
"""
Example: Dual Mass Perspective Applied to Gravitational Waves

This example demonstrates how to apply the dual mass perspective framework
to gravitational wave events, showing the complementarity between energy
and detention perspectives.
"""

import numpy as np
import sys
from pathlib import Path

# Add qcal to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.dual_mass import DualMassPerspective, calculate_dual_mass_spectrum


def analyze_gw_event(event_name: str, peak_freq: float, bandwidth: tuple = None):
    """
    Analyze a gravitational wave event using dual mass perspective.
    
    Parameters
    ----------
    event_name : str
        Name of the GW event (e.g., "GW150914")
    peak_freq : float
        Peak frequency of the event (Hz)
    bandwidth : tuple, optional
        (min_freq, max_freq) for the event bandwidth
    """
    print("=" * 70)
    print(f"Dual Mass Analysis: {event_name}")
    print("=" * 70)
    print()
    
    dmp = DualMassPerspective()
    
    # Calculate at peak frequency
    m_eff_peak = dmp.effective_mass(peak_freq)
    m_noesis_peak = dmp.noetic_mass(peak_freq)
    m_dual = dmp.unified_mass(peak_freq)
    r_eff, r_noesis = dmp.mass_ratio(peak_freq)
    
    print(f"Peak Frequency: {peak_freq:.2f} Hz")
    print(f"Reference f₀:   {dmp.f0:.5f} Hz")
    print(f"Frequency Ratio: f/f₀ = {peak_freq/dmp.f0:.4f}")
    print()
    
    print("Mass Perspectives at Peak:")
    print(f"  m_eff (traditional):  {m_eff_peak:.6e} kg")
    print(f"  m_noesis (detention): {m_noesis_peak:.6e} kg")
    print(f"  m_dual (unified):     {m_dual:.6e} kg")
    print()
    
    print("Mass Ratios to Minimal Noetic Mass:")
    print(f"  r_eff = m_eff/m_min    = {r_eff:.4f}")
    print(f"  r_noesis = m_noesis/m_min = {r_noesis:.4f}")
    print(f"  Product: r_eff × r_noesis = {r_eff * r_noesis:.10f}")
    print()
    
    # Interpret the physics
    if peak_freq > dmp.f0:
        print("Physical Interpretation:")
        print(f"  • Peak frequency is {peak_freq/dmp.f0:.2f}x above f₀")
        print("  • Energy-rich regime (m_eff dominant)")
        print("  • Low detention (highly dynamic)")
    elif peak_freq < dmp.f0:
        print("Physical Interpretation:")
        print(f"  • Peak frequency is {dmp.f0/peak_freq:.2f}x below f₀")
        print("  • Detention-rich regime (m_noesis dominant)")
        print("  • High detention (more static-like)")
    else:
        print("Physical Interpretation:")
        print("  • Peak frequency equals f₀ (RESONANCE!)")
        print("  • Perfect equilibrium between perspectives")
        print("  • m_eff = m_noesis = m_dual")
    
    print()
    
    # Analyze bandwidth if provided
    if bandwidth is not None:
        min_freq, max_freq = bandwidth
        print(f"Bandwidth Analysis: [{min_freq:.1f} - {max_freq:.1f}] Hz")
        
        # Calculate at extremes
        m_eff_min = dmp.effective_mass(min_freq)
        m_eff_max = dmp.effective_mass(max_freq)
        m_noesis_min = dmp.noetic_mass(min_freq)
        m_noesis_max = dmp.noetic_mass(max_freq)
        
        print(f"  At {min_freq:.1f} Hz:")
        print(f"    m_eff = {m_eff_min:.6e} kg")
        print(f"    m_noesis = {m_noesis_min:.6e} kg")
        print(f"  At {max_freq:.1f} Hz:")
        print(f"    m_eff = {m_eff_max:.6e} kg")
        print(f"    m_noesis = {m_noesis_max:.6e} kg")
        print()
        
        # Check if f₀ is in the bandwidth
        if min_freq <= dmp.f0 <= max_freq:
            print(f"  ⭐ f₀ = {dmp.f0:.5f} Hz is within the bandwidth!")
            print("     This event spans the resonance frequency.")
        else:
            print(f"  f₀ = {dmp.f0:.5f} Hz is outside the bandwidth")
    
    print()


def main():
    """Run analysis for several GW events."""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Dual Mass Perspective: Gravitational Wave Analysis".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # GW150914 - First detection
    analyze_gw_event(
        event_name="GW150914",
        peak_freq=250.0,
        bandwidth=(35, 350)
    )
    
    # GW170814 - First three-detector observation
    analyze_gw_event(
        event_name="GW170814",
        peak_freq=100.0,
        bandwidth=(30, 200)
    )
    
    # GW151226 - Lower mass binary
    analyze_gw_event(
        event_name="GW151226",
        peak_freq=450.0,
        bandwidth=(35, 750)
    )
    
    # Hypothetical event near f₀
    analyze_gw_event(
        event_name="Hypothetical (near f₀)",
        peak_freq=141.70001,
        bandwidth=(100, 200)
    )
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("The dual mass perspective reveals:")
    print()
    print("1. Energy Perspective (m_eff = hf/c²):")
    print("   - Higher frequency GW events have higher 'energy mass'")
    print("   - Traditional physics view (external observer)")
    print()
    print("2. Detention Perspective (m_noesis ∝ 1/f):")
    print("   - Lower frequency GW events have higher 'detention mass'")
    print("   - Noetic axiom view (internal resistance)")
    print()
    print("3. Unified Perspective (m_dual = hf₀/c²):")
    print("   - All events share the same fundamental noetic mass quantum")
    print("   - Independent of frequency (universal constant)")
    print()
    print("4. Resonance at f₀ = 141.70001 Hz:")
    print("   - GW events near this frequency show equilibrium")
    print("   - Both perspectives converge (m_eff = m_noesis)")
    print()
    print("5. Implications:")
    print("   - GW events can be classified by their m_eff/m_noesis ratio")
    print("   - Events spanning f₀ probe both regimes")
    print("   - Potential for detecting noetic resonance effects")
    print()
    
    # Generate spectrum plot data
    print("=" * 70)
    print("SPECTRUM ANALYSIS")
    print("=" * 70)
    print()
    
    freqs = np.logspace(0, 3, 100)  # 1 Hz to 1000 Hz
    spectrum = calculate_dual_mass_spectrum(freqs)
    
    print("Generated dual mass spectrum from 1 Hz to 1000 Hz")
    print(f"Number of frequency points: {len(freqs)}")
    print()
    print("Key frequencies in GW astronomy:")
    gw_freqs = {
        "Stellar BH mergers": (30, 500),
        "Neutron stars": (500, 2000),
        "Supermassive BH": (0.0001, 0.1),
        "LIGO band": (10, 5000),
        "f₀ resonance": (141.70001, 141.70001)
    }
    
    for name, (f_min, f_max) in gw_freqs.items():
        if f_min == f_max:
            f = f_min
            m_eff = spectrum['m_eff'][np.argmin(np.abs(spectrum['frequencies'] - f))]
            print(f"  {name:20s}: f = {f:.5f} Hz")
        else:
            print(f"  {name:20s}: {f_min:.4f} - {f_max:.4f} Hz")
    
    print()
    print("To visualize the spectrum, use:")
    print("  python3 -c \"")
    print("  from qcal.dual_mass import calculate_dual_mass_spectrum")
    print("  import matplotlib.pyplot as plt")
    print("  import numpy as np")
    print("  freqs = np.logspace(0, 3, 200)")
    print("  s = calculate_dual_mass_spectrum(freqs)")
    print("  plt.loglog(s['frequencies'], s['m_eff'], label='m_eff')")
    print("  plt.loglog(s['frequencies'], s['m_noesis'], label='m_noesis')")
    print("  plt.axhline(s['m_min'], ls='--', label='m_dual')")
    print("  plt.axvline(s['f0'], ls=':', label='f₀')")
    print("  plt.legend(); plt.show()\"")
    print()


if __name__ == "__main__":
    main()
