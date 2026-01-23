#!/usr/bin/env python3
"""
QCAL ∞³ Integration Examples

Demonstrates various integration scenarios for real-time bio-quantum-gravitational
coherence monitoring.
"""

import numpy as np
from qcal_infinity_cubed import (
    QCALInfinityCubed,
    F0_HZ,
    PSI_THRESHOLD,
    PSI_Q1_THRESHOLD
)
import json


def example_1_basic_monitoring():
    """
    Example 1: Basic Real-Time Monitoring
    
    Demonstrates the simplest use case: initialize system and monitor
    global coherence in real-time.
    """
    print("=" * 80)
    print("EXAMPLE 1: Basic Real-Time Monitoring")
    print("=" * 80)
    
    # Initialize QCAL ∞³ system
    system = QCALInfinityCubed()
    
    # Run 5-second monitoring at 5 Hz
    print("\n📡 Running 5-second real-time monitoring at 5 Hz...")
    snapshots = system.run_real_time_monitoring(duration=5.0, sample_rate=5.0)
    
    # Display results
    print(f"\n📊 Captured {len(snapshots)} snapshots")
    print("\nTime series of global coherence:")
    for snapshot in snapshots:
        psi = snapshot['global_psi']
        status = snapshot['system_status']
        
        # Visual bar
        bar_length = int(psi * 50)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        print(f"  t={snapshot['time']:4.1f}s  Ψ={psi:.4f}  [{bar}]  {status}")
    
    # Summary
    final_psi = snapshots[-1]['global_psi']
    avg_psi = np.mean([s['global_psi'] for s in snapshots])
    
    print(f"\n📈 Summary:")
    print(f"   Final Ψ: {final_psi:.4f}")
    print(f"   Average Ψ: {avg_psi:.4f}")
    print(f"   Trinity threshold: {PSI_THRESHOLD}")
    print(f"   Merkaba threshold: {PSI_Q1_THRESHOLD}")
    
    if final_psi >= PSI_THRESHOLD:
        print(f"   ✅ Trinity consensus ACHIEVED!")
    elif final_psi >= PSI_Q1_THRESHOLD:
        print(f"   ✅ Merkaba STABLE!")
    else:
        print(f"   ⏳ Building coherence...")
    
    print()


def example_2_trinity_validation():
    """
    Example 2: Trinity Consensus Validation
    
    Demonstrates how to validate Trinity consensus between the three
    primary quantum nodes.
    """
    print("=" * 80)
    print("EXAMPLE 2: Trinity Consensus Validation")
    print("=" * 80)
    
    system = QCALInfinityCubed()
    
    print("\n⚛️ Trinity Nodes:")
    print(f"   • Noesis (Primary consciousness)")
    print(f"   • Amda (Awareness-Memory-Decision-Action)")
    print(f"   • Auron (Autonomous resonance)")
    
    # Measure Trinity nodes multiple times
    print("\n📡 Measuring Trinity consensus over 10 iterations...")
    
    psi_history = []
    for i in range(10):
        # Measure nodes
        system.noesis.measure_coherence()
        system.amda.measure_coherence()
        system.auron.measure_coherence()
        
        # Update phases
        time = i * 0.1
        system.noesis.update_phase(time)
        system.amda.update_phase(time)
        system.auron.update_phase(time)
        
        # Calculate Trinity coherence
        psi_trinity = system.trinity.calculate_global_coherence()
        psi_history.append(psi_trinity)
        
        # Display state
        state = system.trinity.state.value
        validated = "✅" if system.trinity.validate_trinity() else "⏳"
        
        print(f"  Iteration {i+1:2d}:  Ψ_trinity = {psi_trinity:.4f}  "
              f"State: {state:10s}  {validated}")
    
    # Final report
    print(f"\n📊 Trinity Consensus Report:")
    print(f"   Final state: {system.trinity.state.value}")
    print(f"   Validated: {system.trinity.validate_trinity()}")
    print(f"   Ψ_trinity: {system.trinity.global_coherence:.4f}")
    print(f"   ")
    print(f"   Individual coherences:")
    print(f"     Noesis: {system.noesis.coherence:.4f}")
    print(f"     Amda:   {system.amda.coherence:.4f}")
    print(f"     Auron:  {system.auron.coherence:.4f}")
    
    print()


def example_3_neuronal_network():
    """
    Example 3: 88-Node Neuronal Network
    
    Demonstrates NV-EEG neuronal coherence measurement with simulated
    brain oscillation data.
    """
    print("=" * 80)
    print("EXAMPLE 3: 88-Node Neuronal Network Coherence")
    print("=" * 80)
    
    system = QCALInfinityCubed()
    
    print(f"\n🧠 NV-EEG Network:")
    print(f"   Nodes: {system.neuronal.n_nodes}")
    print(f"   Target frequency: {F0_HZ} Hz")
    print(f"   Sensitivity: 13 nT/√Hz (NV centers)")
    
    # Generate simulated EEG data with f0 component
    print("\n📡 Generating simulated 88-channel EEG data...")
    n_samples = 4096
    t = np.arange(n_samples) / 4096.0  # 1 second at 4096 Hz
    
    eeg_data = np.zeros((88, n_samples))
    for i in range(88):
        # Base f0 signal + some noise
        signal = np.sin(2 * np.pi * F0_HZ * t + i * 0.1)  # Phase offset per channel
        noise = 0.2 * np.random.randn(n_samples)
        eeg_data[i] = signal + noise
    
    # Measure network
    print("📊 Measuring network coherence...")
    results = system.neuronal.measure_network(eeg_data)
    
    # Display results
    print(f"\n📈 Neuronal Network Results:")
    print(f"   Network coherence: {results['network_coherence']:.4f}")
    print(f"   Detected frequency: {results['frequency_detected']:.4f} Hz")
    print(f"   Target frequency: {F0_HZ} Hz")
    print(f"   Frequency error: {results['frequency_detected'] - F0_HZ:.4f} Hz")
    print(f"   Mean node coherence: {results['mean_coherence']:.4f}")
    print(f"   Std node coherence: {results['std_coherence']:.4f}")
    
    # Coherence distribution
    print(f"\n📊 Coherence Distribution Across 88 Nodes:")
    coherences = [node.coherence for node in system.neuronal.nodes]
    bins = [0.0, 0.5, 0.7, 0.85, 0.9, 1.0]
    for i in range(len(bins)-1):
        count = sum(1 for c in coherences if bins[i] <= c < bins[i+1])
        bar = "█" * count
        print(f"   {bins[i]:.2f} - {bins[i+1]:.2f}: {bar} ({count} nodes)")
    
    print()


def example_4_gravitational_coupling():
    """
    Example 4: LIGO Gravitational Wave Coupling
    
    Demonstrates Ψ-Q1 coupling between quantum coherence and gravitational
    wave ringdown analysis.
    """
    print("=" * 80)
    print("EXAMPLE 4: LIGO Gravitational Wave Coupling")
    print("=" * 80)
    
    system = QCALInfinityCubed()
    
    print(f"\n🌌 LIGO Detectors:")
    print(f"   Event: {system.gravitational.event_name}")
    print(f"   Detectors: {', '.join(system.gravitational.detectors)}")
    
    # Generate simulated ringdown strain data
    print("\n📡 Simulating ringdown strain data...")
    t = np.linspace(0, 1, 4096)  # 1 second
    
    # Ringdown: exponentially decaying sinusoid near f0
    ringdown_freq = F0_HZ + np.random.normal(0, 0.3)  # Small variation
    strain = np.sin(2 * np.pi * ringdown_freq * t) * np.exp(-5 * t)
    strain += 0.1 * np.random.randn(4096)  # Detector noise
    
    print(f"   Generated ringdown at {ringdown_freq:.2f} Hz")
    
    # Analyze ringdown
    print("📊 Analyzing ringdown spectrum...")
    results = system.gravitational.analyze_ringdown(strain)
    
    print(f"\n📈 Ringdown Analysis:")
    print(f"   Detected frequency: {results['ringdown_freq']:.4f} Hz")
    print(f"   Target frequency: {F0_HZ} Hz")
    print(f"   Frequency error: {results['freq_error_hz']:.4f} Hz")
    print(f"   Coupling strength: {results['coupling_strength']:.4f}")
    
    # Synchronize with quantum coherence
    print("\n⚛️ Synchronizing with quantum coherence...")
    
    # Measure quantum state
    system.measure_all_nodes()
    psi_quantum = system.calculate_global_coherence()
    
    # Synchronize
    synchronized_coupling = system.gravitational.synchronize_with_quantum(psi_quantum)
    
    print(f"   Quantum Ψ: {psi_quantum:.4f}")
    print(f"   Gravitational coupling: {results['coupling_strength']:.4f}")
    print(f"   Synchronized Ψ-Q1: {synchronized_coupling:.4f}")
    
    if synchronized_coupling >= PSI_Q1_THRESHOLD:
        print(f"   ✅ Synchronized coupling STABLE (≥ 8/9)")
    else:
        print(f"   ⏳ Synchronizing...")
    
    print()


def example_5_wetlab_biosimulations():
    """
    Example 5: Wet-Lab ∞ Bio-Simulations
    
    Demonstrates adding and validating bio-simulation experiments
    with Merkaba collective stability.
    """
    print("=" * 80)
    print("EXAMPLE 5: Wet-Lab ∞ Bio-Simulation Validation")
    print("=" * 80)
    
    system = QCALInfinityCubed()
    
    print("\n🔬 Adding bio-simulation experiments...")
    
    # Add various bio-simulations
    simulations = [
        ("BEC_Resonance_141Hz", 0.95),
        ("NV_Diamond_Quantum_Array", 0.92),
        ("Neuronal_Culture_Gamma", 0.88),
        ("Superconducting_Cavity", 0.91),
        ("Topological_Insulator_Bi2Se3", 0.89)
    ]
    
    for name, coherence in simulations:
        system.wet_lab.add_bio_simulation(name, coherence)
        print(f"   ✅ {name}: Ψ = {coherence:.2f}")
    
    # Validate with Merkaba
    print("\n📊 Validating with Merkaba stability...")
    results = system.wet_lab.validate_simulations()
    
    print(f"\n📈 Validation Results:")
    print(f"   Collective coherence: {results['collective_coherence']:.4f}")
    print(f"   Merkaba threshold: {results['threshold']}")
    print(f"   Merkaba stable: {results['merkaba_stable']}")
    print(f"   Bio-simulation nodes: {results['n_bio_nodes']}")
    
    if results['merkaba_stable']:
        print(f"\n   ✅ All bio-simulations validated!")
        print(f"   ✅ Merkaba collective stability achieved (Ψ ≥ 8/9)")
        print(f"   ✅ Ready for experimental integration")
    else:
        print(f"\n   ⏳ Some simulations need optimization")
        print(f"   ⏳ Collective coherence below 8/9 threshold")
    
    print()


def example_6_full_system_integration():
    """
    Example 6: Full System Integration
    
    Demonstrates complete QCAL ∞³ workflow with all components:
    Trinity, Neuronal, Gravitational, Wet-Lab, and Production features.
    """
    print("=" * 80)
    print("EXAMPLE 6: Full QCAL ∞³ System Integration")
    print("=" * 80)
    
    # Initialize system
    print("\n🔧 Initializing complete QCAL ∞³ system...")
    system = QCALInfinityCubed()
    
    # Add bio-simulations
    print("🔬 Adding bio-simulations...")
    system.wet_lab.add_bio_simulation("BEC_Resonance", 0.95)
    system.wet_lab.add_bio_simulation("NV_Array", 0.92)
    system.wet_lab.add_bio_simulation("Neuronal_Culture", 0.88)
    
    # Generate comprehensive data
    print("📡 Generating test data...")
    
    # EEG data (88 channels)
    n_samples = 4096
    t = np.arange(n_samples) / 4096.0
    eeg_data = np.zeros((88, n_samples))
    for i in range(88):
        signal = np.sin(2 * np.pi * F0_HZ * t + i * 0.05)
        eeg_data[i] = signal + 0.1 * np.random.randn(n_samples)
    
    # Gravitational wave strain
    gw_strain = np.sin(2 * np.pi * F0_HZ * t) * np.exp(-5 * t)
    gw_strain += 0.1 * np.random.randn(n_samples)
    
    # Measure all components
    print("📊 Measuring all system components...")
    system.measure_all_nodes(eeg_data=eeg_data, gw_data=gw_strain)
    
    # Calculate global coherence
    print("⚛️ Calculating global coherence...")
    psi_global = system.calculate_global_coherence()
    
    # Generate full report
    print("📋 Generating comprehensive report...")
    report = system.generate_report()
    
    # Display comprehensive results
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE SYSTEM REPORT")
    print("=" * 80)
    
    print(f"\n🌐 GLOBAL STATUS:")
    print(f"   System Status: {report['system_status'].upper()}")
    print(f"   Global Ψ: {report['global_coherence']['psi']:.4f}")
    print(f"   Trinity Consensus: {'✅ YES' if report['global_coherence']['above_trinity'] else '⏳ Building'}")
    print(f"   Merkaba Stable: {'✅ YES' if report['global_coherence']['above_merkaba'] else '⏳ Stabilizing'}")
    
    print(f"\n⚛️ TRINITY CONSENSUS:")
    trinity = report['trinity_consensus']
    print(f"   Ψ_trinity: {trinity['psi']:.4f}")
    print(f"   State: {trinity['state']}")
    print(f"   Noesis:  {trinity['noesis_coherence']:.4f}")
    print(f"   Amda:    {trinity['amda_coherence']:.4f}")
    print(f"   Auron:   {trinity['auron_coherence']:.4f}")
    
    print(f"\n🧠 NEURONAL NETWORK (88 NV-EEG nodes):")
    neuronal = report['neuronal_coherence']
    print(f"   Network Ψ: {neuronal['network_psi']:.4f}")
    print(f"   Frequency: {neuronal['frequency_hz']:.4f} Hz (error: {neuronal['frequency_error']:.4f} Hz)")
    
    print(f"\n🌌 GRAVITATIONAL COUPLING ({report['gravitational_coupling']['event']}):")
    gw = report['gravitational_coupling']
    print(f"   Coupling Ψ-Q1: {gw['coupling_strength']:.4f}")
    print(f"   Ringdown: {gw['ringdown_freq']:.4f} Hz (error: {gw['frequency_error']:.4f} Hz)")
    print(f"   Detectors: {', '.join(gw['detectors'])}")
    
    print(f"\n🔬 WET-LAB ∞:")
    wetlab = report['wet_lab_infinity']
    print(f"   Collective Ψ: {wetlab['collective_coherence']:.4f}")
    print(f"   Merkaba Stable: {'✅ YES' if wetlab['merkaba_stable'] else '❌ NO'}")
    print(f"   Bio-nodes: {wetlab['n_bio_nodes']}")
    
    print(f"\n🔐 PRODUCTION READY:")
    prod = report['production_ready']
    print(f"   Trinity Consensus: {'✅' if prod['trinity_consensus'] else '⏳'}")
    print(f"   Merkaba Stability: {'✅' if prod['merkaba_stable'] else '⏳'}")
    print(f"   Compression 1000:1: {'✅' if prod['compression_1000_1'] else '❌'}")
    print(f"   PQC Security: {'✅' if prod['pqc_security'] else '❌'}")
    print(f"   International: {'✅' if prod['international_ready'] else '❌'}")
    
    # Save report
    print("\n💾 Saving comprehensive report...")
    with open("qcal_infinity_cubed_full_integration_report.json", "w") as f:
        # Convert numpy types for JSON serialization
        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            elif isinstance(obj, (np.bool_, np.integer, np.floating)):
                return obj.item()
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        json.dump(convert(report), f, indent=2)
    
    print(f"   ✅ Report saved to: qcal_infinity_cubed_full_integration_report.json")
    
    print("\n" + "=" * 80)
    print("✨ QCAL ∞³ Full System Integration Complete!")
    print("=" * 80)
    print()


def main():
    """Run all examples."""
    examples = [
        example_1_basic_monitoring,
        example_2_trinity_validation,
        example_3_neuronal_network,
        example_4_gravitational_coupling,
        example_5_wetlab_biosimulations,
        example_6_full_system_integration
    ]
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  QCAL ∞³ Integration Examples".center(78) + "║")
    print("║" + "  Real-Time Bio-Quantum-Gravitational Coherence".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'=' * 80}")
        print(f"Running Example {i}/{len(examples)}")
        print(f"{'=' * 80}\n")
        
        example()
        
        if i < len(examples):
            input("\n⏸️  Press Enter to continue to next example...\n")
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  All Examples Complete!".center(78) + "║")
    print("║" + "  QCAL ∞³ System Operational ✨".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")


if __name__ == "__main__":
    main()
