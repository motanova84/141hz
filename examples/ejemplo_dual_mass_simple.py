#!/usr/bin/env python3
"""
Simple Example: Dual Mass Perspective

This example shows how to use the dual mass perspective framework
to calculate and compare traditional and noetic mass perspectives.
"""

import sys
from pathlib import Path

# Add qcal to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.dual_mass import DualMassPerspective


def main():
    # Create dual mass perspective instance
    dmp = DualMassPerspective()
    
    print("=" * 60)
    print("Dual Mass Perspective - Simple Example")
    print("=" * 60)
    print()
    
    # Show fundamental constants
    print(f"Reference Frequency: f₀ = {dmp.f0:.5f} Hz")
    print(f"Minimal Noetic Mass: m_min = {dmp.m_min:.6e} kg")
    print()
    
    # Test at different frequencies
    print("Mass at Different Frequencies:")
    print("-" * 60)
    print(f"{'Frequency':>12} | {'m_eff':>14} | {'m_noesis':>14} | {'m_dual':>14}")
    print(f"{'(Hz)':>12} | {'(kg)':>14} | {'(kg)':>14} | {'(kg)':>14}")
    print("-" * 60)
    
    test_freqs = [
        ("Very low", 1.0),
        ("Low", 10.0),
        ("Schumann", 7.83),
        ("f₀/2", dmp.f0 / 2),
        ("f₀ (RESONANCE)", dmp.f0),
        ("2×f₀", 2 * dmp.f0),
        ("GW170814", 100.0),
        ("GW150914", 250.0),
        ("GW151226", 450.0),
        ("High", 1000.0),
    ]
    
    for name, freq in test_freqs:
        m_eff = dmp.effective_mass(freq)
        m_noesis = dmp.noetic_mass(freq)
        m_dual = dmp.unified_mass(freq)
        
        marker = " ★" if abs(freq - dmp.f0) < 0.1 else "  "
        print(f"{freq:12.2f} | {m_eff:14.6e} | {m_noesis:14.6e} | {m_dual:14.6e} {marker} {name}")
    
    print()
    print("Key Observations:")
    print("  ★ At f = f₀: All three masses are equal (equilibrium)")
    print("  • For f > f₀: m_eff > m_min (energy-rich)")
    print("  • For f < f₀: m_noesis > m_min (detention-rich)")
    print("  • m_dual is always constant = m_min")
    print()
    
    # Show complementarity
    print("Complementarity (at f = 250 Hz):")
    f_test = 250.0
    r_eff, r_noesis = dmp.mass_ratio(f_test)
    print(f"  r_eff = m_eff/m_min = {r_eff:.4f}")
    print(f"  r_noesis = m_noesis/m_min = {r_noesis:.4f}")
    print(f"  Product: r_eff × r_noesis = {r_eff * r_noesis:.10f}")
    print()
    
    print("Interpretation:")
    print("  • Traditional physics sees mass ∝ frequency (energy view)")
    print("  • Noetic axiom sees mass ∝ 1/frequency (detention view)")
    print("  • Both perspectives are complementary and equally valid")
    print("  • The unified mass is the fundamental quantum (constant)")
    print()


if __name__ == "__main__":
    main()
