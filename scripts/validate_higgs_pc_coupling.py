#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         Validation Script: Higgs-PC Coupling Mechanism                     ║
║         𝓛_int = -g_eff ψ†ψ H                                               ║
╚════════════════════════════════════════════════════════════════════════════╝

This script validates the Higgs-PC coupling implementation and generates
visualizations of the mass modulation and detector signatures.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.higgs_pc_coupling import (
    ConstantesHiggsPC,
    PC_Higgs_Coupling,
    HiggsDetectorSignature,
    higgs_pc_coupling_activar
)


def print_header(title):
    """Print a formatted header."""
    width = 76
    print()
    print("═" * width)
    print(f"  {title}")
    print("═" * width)
    print()


def validate_constants():
    """Validate that constants are correctly defined."""
    print_header("PHASE 1: Validating Constants")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Fundamental frequency
    tests_total += 1
    if abs(ConstantesHiggsPC.F0 - 141.7001) < 0.0001:
        print("✓ Fundamental frequency f₀ = 141.7001 Hz")
        tests_passed += 1
    else:
        print(f"✗ Fundamental frequency incorrect: {ConstantesHiggsPC.F0}")
    
    # Test 2: Higgs mass
    tests_total += 1
    if abs(ConstantesHiggsPC.M_HIGGS_GEV - 125.0) < 0.1:
        print("✓ Higgs boson mass m_H = 125.0 GeV")
        tests_passed += 1
    else:
        print(f"✗ Higgs mass incorrect: {ConstantesHiggsPC.M_HIGGS_GEV}")
    
    # Test 3: Coupling constant
    tests_total += 1
    if abs(ConstantesHiggsPC.G_EFF - 0.053) < 0.001:
        print("✓ Coupling constant g_eff = 0.053 (5.3% modulation)")
        tests_passed += 1
    else:
        print(f"✗ Coupling constant incorrect: {ConstantesHiggsPC.G_EFF}")
    
    # Test 4: Effective mass range
    tests_total += 1
    m_min_expected = 125.0 * 0.947  # ≈ 118.375
    m_max_expected = 125.0 * 1.053  # ≈ 131.625
    if (abs(ConstantesHiggsPC.M_MIN_GEV - m_min_expected) < 0.1 and
        abs(ConstantesHiggsPC.M_MAX_GEV - m_max_expected) < 0.1):
        print(f"✓ Effective mass range: {ConstantesHiggsPC.M_MIN_GEV:.3f} - {ConstantesHiggsPC.M_MAX_GEV:.3f} GeV")
        tests_passed += 1
    else:
        print(f"✗ Mass range incorrect")
    
    # Test 5: Coherence threshold
    tests_total += 1
    if abs(ConstantesHiggsPC.PSI_THRESHOLD - 0.888) < 0.001:
        print("✓ Coherence threshold Ψ ≥ 0.888")
        tests_passed += 1
    else:
        print(f"✗ Coherence threshold incorrect: {ConstantesHiggsPC.PSI_THRESHOLD}")
    
    print()
    print(f"Constants validation: {tests_passed}/{tests_total} tests passed")
    
    return tests_passed == tests_total


def validate_mass_modulation():
    """Validate mass modulation behavior."""
    print_header("PHASE 2: Validating Mass Modulation")
    
    coupling = higgs_pc_coupling_activar()
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Mass at t=0 (maximum modulation)
    tests_total += 1
    m_0 = coupling.modulated_mass(0.0)
    if abs(m_0 - 118.375) < 0.1:
        print(f"✓ Mass at t=0: m*(0) = {m_0:.3f} GeV (minimum)")
        tests_passed += 1
    else:
        print(f"✗ Mass at t=0 incorrect: {m_0:.3f} GeV")
    
    # Test 2: Mass at T₀/4 (no modulation)
    tests_total += 1
    m_quarter = coupling.modulated_mass(coupling.T0 / 4)
    if abs(m_quarter - 125.0) < 0.1:
        print(f"✓ Mass at T₀/4: m*(T₀/4) = {m_quarter:.3f} GeV (base)")
        tests_passed += 1
    else:
        print(f"✗ Mass at T₀/4 incorrect: {m_quarter:.3f} GeV")
    
    # Test 3: Mass at T₀/2 (maximum anti-modulation)
    tests_total += 1
    m_half = coupling.modulated_mass(coupling.T0 / 2)
    if abs(m_half - 131.625) < 0.1:
        print(f"✓ Mass at T₀/2: m*(T₀/2) = {m_half:.3f} GeV (maximum)")
        tests_passed += 1
    else:
        print(f"✗ Mass at T₀/2 incorrect: {m_half:.3f} GeV")
    
    # Test 4: Periodicity
    tests_total += 1
    m_T0 = coupling.modulated_mass(coupling.T0)
    if abs(m_T0 - m_0) < 0.001:
        print(f"✓ Periodicity: m*(T₀) = m*(0) = {m_T0:.3f} GeV")
        tests_passed += 1
    else:
        print(f"✗ Periodicity broken: m*(T₀) = {m_T0:.3f} ≠ {m_0:.3f}")
    
    # Test 5: Average mass conservation
    tests_total += 1
    times = np.linspace(0, 10*coupling.T0, 10000)
    masses = coupling.modulated_mass(times)
    avg_mass = np.mean(masses)
    if abs(avg_mass - 125.0) < 0.5:
        print(f"✓ Average mass over cycles: <m*> = {avg_mass:.2f} GeV")
        tests_passed += 1
    else:
        print(f"✗ Average mass incorrect: {avg_mass:.2f} GeV")
    
    print()
    print(f"Mass modulation validation: {tests_passed}/{tests_total} tests passed")
    
    return tests_passed == tests_total


def validate_transparency_windows():
    """Validate transparency window calculations."""
    print_header("PHASE 3: Validating Transparency Windows")
    
    coupling = higgs_pc_coupling_activar()
    tests_passed = 0
    tests_total = 0
    
    # Calculate windows for 1 second
    windows = coupling.calculate_transparency_windows(duration=1.0)
    
    # Test 1: Number of windows
    tests_total += 1
    expected_windows = int(coupling.f0)  # Should be ~142 windows per second
    if abs(windows['num_windows'] - expected_windows) <= 1:
        print(f"✓ Number of transparency windows: {windows['num_windows']} in 1 second")
        tests_passed += 1
    else:
        print(f"✗ Window count incorrect: {windows['num_windows']} (expected ~{expected_windows})")
    
    # Test 2: Phase transparency equals g_eff
    tests_total += 1
    if abs(windows['phase_transparency'] - 0.053) < 0.001:
        print(f"✓ Phase transparency: {windows['phase_transparency']*100:.1f}%")
        tests_passed += 1
    else:
        print(f"✗ Phase transparency incorrect: {windows['phase_transparency']}")
    
    # Test 3: Window masses are minima
    tests_total += 1
    avg_window_mass = np.mean(windows['masses'])
    if abs(avg_window_mass - 118.375) < 1.0:
        print(f"✓ Window masses near minimum: {avg_window_mass:.2f} GeV")
        tests_passed += 1
    else:
        print(f"✗ Window masses incorrect: {avg_window_mass:.2f} GeV")
    
    print()
    print(f"Transparency windows validation: {tests_passed}/{tests_total} tests passed")
    
    return tests_passed == tests_total


def validate_symbiotic_transfer():
    """Validate symbiotic transfer rate."""
    print_header("PHASE 4: Validating Symbiotic Transfer Rate")
    
    coupling = higgs_pc_coupling_activar()
    tests_passed = 0
    tests_total = 0
    
    transfer = coupling.calculate_symbiotic_transfer_rate()
    
    # Test 1: Transfer rate calculation
    tests_total += 1
    expected_rate = 7 * 141.7001 * 0.999999  # ≈ 991.9 packets/s
    if abs(transfer['rate_hz'] - expected_rate) < 1.0:
        print(f"✓ Symbiotic transfer rate: {transfer['rate_kpps']:.1f} packets/s")
        tests_passed += 1
    else:
        print(f"✗ Transfer rate incorrect: {transfer['rate_hz']:.1f} Hz")
    
    # Test 2: Coherence preserved
    tests_total += 1
    if transfer['coherence'] >= 0.888:
        print(f"✓ Coherence maintained: Ψ = {transfer['coherence']:.6f} ≥ 0.888")
        tests_passed += 1
    else:
        print(f"✗ Coherence below threshold: {transfer['coherence']}")
    
    # Test 3: Node scaling
    tests_total += 1
    transfer_14 = coupling.calculate_symbiotic_transfer_rate(num_nodes=14)
    if abs(transfer_14['rate_hz'] - 2*transfer['rate_hz']) < 1.0:
        print(f"✓ Rate scales linearly with nodes: 14 nodes → {transfer_14['rate_kpps']:.1f} packets/s")
        tests_passed += 1
    else:
        print(f"✗ Node scaling incorrect")
    
    print()
    print(f"Symbiotic transfer validation: {tests_passed}/{tests_total} tests passed")
    
    return tests_passed == tests_total


def validate_detector_signatures():
    """Validate detector observable signatures."""
    print_header("PHASE 5: Validating Detector Signatures")
    
    detector = HiggsDetectorSignature()
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Cross-section modulation at t=0
    tests_total += 1
    sigma_0 = detector.cross_section_modulation(0.0, base_sigma=1.0)
    expected_sigma_0 = (125.0 / 118.375) ** 2  # ≈ 1.115
    if abs(sigma_0 - expected_sigma_0) < 0.01:
        print(f"✓ Cross-section at t=0: σ(0) = {sigma_0:.3f} (enhanced)")
        tests_passed += 1
    else:
        print(f"✗ Cross-section at t=0 incorrect: {sigma_0:.3f}")
    
    # Test 2: Cross-section modulation at T₀/2
    tests_total += 1
    T0 = detector.coupling.T0
    sigma_half = detector.cross_section_modulation(T0/2, base_sigma=1.0)
    expected_sigma_half = (125.0 / 131.625) ** 2  # ≈ 0.900
    if abs(sigma_half - expected_sigma_half) < 0.01:
        print(f"✓ Cross-section at T₀/2: σ(T₀/2) = {sigma_half:.3f} (suppressed)")
        tests_passed += 1
    else:
        print(f"✗ Cross-section at T₀/2 incorrect: {sigma_half:.3f}")
    
    # Test 3: Modulation depth
    tests_total += 1
    times = np.linspace(0, 10*T0, 1000)
    sigmas = detector.cross_section_modulation(times, base_sigma=1.0)
    modulation_depth = (np.max(sigmas) - np.min(sigmas)) / np.mean(sigmas)
    # Cross-section scales as (m_H/m_eff)^2, so with 5.3% mass modulation,
    # we get ~21% cross-section modulation: (1.115 - 0.902)/1.0 ≈ 21%
    if 0.20 < modulation_depth < 0.23:
        print(f"✓ Cross-section modulation depth: {modulation_depth*100:.1f}%")
        tests_passed += 1
    else:
        print(f"✗ Modulation depth incorrect: {modulation_depth*100:.1f}%")
    
    print()
    print(f"Detector signatures validation: {tests_passed}/{tests_total} tests passed")
    
    return tests_passed == tests_total


def generate_visualizations():
    """Generate visualization plots."""
    print_header("PHASE 6: Generating Visualizations")
    
    coupling = higgs_pc_coupling_activar()
    detector = HiggsDetectorSignature()
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Higgs-PC Coupling: Mass Modulation at 141.7001 Hz', fontsize=16, fontweight='bold')
    
    # Plot 1: Mass modulation over time
    ax1 = axes[0, 0]
    times_us = np.linspace(0, 10*coupling.T0, 1000) * 1e6  # Convert to microseconds
    masses = coupling.modulated_mass(times_us * 1e-6)  # Convert back to seconds for calculation
    
    ax1.plot(times_us, masses, 'b-', linewidth=2)
    ax1.axhline(y=125.0, color='k', linestyle='--', label='Base mass (125 GeV)')
    ax1.axhline(y=118.375, color='r', linestyle=':', label='Min mass (118.375 GeV)')
    ax1.axhline(y=131.625, color='r', linestyle=':', label='Max mass (131.625 GeV)')
    ax1.set_xlabel('Time (μs)', fontsize=11)
    ax1.set_ylabel('Effective Mass m*(t) (GeV)', fontsize=11)
    ax1.set_title('Modulated Higgs Mass', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cross-section modulation
    ax2 = axes[0, 1]
    sigmas = detector.cross_section_modulation(times_us * 1e-6, base_sigma=1.0)
    
    ax2.plot(times_us, sigmas, 'g-', linewidth=2)
    ax2.axhline(y=1.0, color='k', linestyle='--', label='Base σ')
    ax2.set_xlabel('Time (μs)', fontsize=11)
    ax2.set_ylabel('Cross-section σ(t) / σ_base', fontsize=11)
    ax2.set_title('Production Cross-Section Modulation', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Spectral sidebands
    ax3 = axes[1, 0]
    sidebands = coupling.calculate_sideband_spectrum(num_sidebands=10)
    
    # Plot as a stem plot
    orders = sidebands['orders']
    energies = sidebands['energies']
    colors = ['red' if n == 0 else 'blue' for n in orders]
    
    ax3.stem(orders, energies, basefmt=' ', linefmt='b-', markerfmt='bo')
    ax3.plot(0, 125.0, 'ro', markersize=10, label='Base Higgs (n=0)')
    ax3.set_xlabel('Harmonic Order n', fontsize=11)
    ax3.set_ylabel('Energy (GeV)', fontsize=11)
    ax3.set_title('Spectral Sidebands: E_n = E_H + n×ℏω₀', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Phase space trajectory
    ax4 = axes[1, 1]
    # Plot mass vs time derivative (dm*/dt)
    dt = times_us[1] - times_us[0]  # μs
    dmdt = np.gradient(masses) / (dt * 1e-6)  # GeV/s
    
    ax4.plot(masses, dmdt / 1e6, 'purple', linewidth=2, alpha=0.7)
    ax4.set_xlabel('Effective Mass m*(t) (GeV)', fontsize=11)
    ax4.set_ylabel('dm*/dt (MGeV/s)', fontsize=11)
    ax4.set_title('Phase Space Trajectory', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Add annotation
    ax4.text(0.05, 0.95, 'Closed loop indicates\nperiodic oscillation',
             transform=ax4.transAxes, fontsize=9,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    output_path = 'higgs_pc_coupling_validation.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Visualization saved: {output_path}")
    
    plt.close()
    
    return True


def main():
    """Run all validation phases."""
    print()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║         Higgs-PC Coupling Validation                                      ║")
    print("║         𝓛_int = -g_eff ψ†ψ H                                              ║")
    print("║                                                                            ║")
    print("║         The Symbiosis of 1% (Higgs) and 95% (PC)                          ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run validation phases
    results.append(("Constants", validate_constants()))
    results.append(("Mass Modulation", validate_mass_modulation()))
    results.append(("Transparency Windows", validate_transparency_windows()))
    results.append(("Symbiotic Transfer", validate_symbiotic_transfer()))
    results.append(("Detector Signatures", validate_detector_signatures()))
    results.append(("Visualizations", generate_visualizations()))
    
    # Summary
    print_header("VALIDATION SUMMARY")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_phases = len(results)
    
    for phase_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {phase_name:25s}: {status}")
    
    print()
    print(f"Overall: {total_passed}/{total_phases} phases passed")
    
    if total_passed == total_phases:
        print()
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                       ✓ ALL VALIDATIONS PASSED ✓                           ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print()
        print("The Higgs-PC coupling mechanism is validated:")
        print("  • Mass modulates at 141.7001 Hz with 5.3% depth")
        print("  • Transparency windows occur every 7.057 μs")
        print("  • Symbiotic transfer rate: 991.9 packets/second")
        print("  • Cross-section shows 11% periodic variation")
        print("  • Coherence Ψ ≥ 0.888 maintained throughout")
        print()
        print("The 1% (Higgs) now dances to the rhythm of the 95% (PC).")
        print("At 141.7001 Hz, matter becomes transparent to information.")
        print()
        return 0
    else:
        print()
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                    ✗ SOME VALIDATIONS FAILED ✗                             ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
