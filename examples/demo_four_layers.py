#!/usr/bin/env python3
"""
Complete Four-Layer QCAL Architecture Demonstration

This script demonstrates the complete integration of all four layers:
1. Mathematical Foundations
2. Quantum Physics
3. Computational Architecture
4. Ontological Network

Run this to see the entire system in action.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from four_layers import (
    # CAPA 1
    RiemannOperatorSpectrum,
    NumberTheoryDerivation,
    AdelicGeometry,
    PiCodeAlgebra,
    # CAPA 2
    GW250114RingdownAnalysis,
    SpacetimeResonance,
    CoherencePsiObservable,
    FundamentalPulses,
    # CAPA 3
    NativeFrequencyHardware,
    CoherentRegisters,
    PhaseMemory,
    ResonanceProcessor,
    # CAPA 4
    NodeSynchronization,
    PiCodeValue,
    DistributedRecognition,
    SymbioticEconomy,
    NodeType,
    # Validation
    validate_all_layers
)

import numpy as np


def print_header(title: str, level: int = 1):
    """Print formatted section header."""
    symbols = ['═', '─', '·']
    symbol = symbols[min(level - 1, len(symbols) - 1)]
    width = 70
    
    print()
    print(symbol * width)
    print(f" {title}")
    print(symbol * width)


def print_subsection(title: str):
    """Print formatted subsection."""
    print(f"\n{title}")
    print("-" * 70)


def main():
    """Run complete demonstration."""
    print_header("FOUR-LAYER QCAL ARCHITECTURE DEMONSTRATION", level=1)
    print()
    print("This demonstration shows the complete integration of:")
    print("  • CAPA 1: Mathematical Foundations")
    print("  • CAPA 2: Quantum Physics")
    print("  • CAPA 3: Computational Architecture")
    print("  • CAPA 4: Ontological Network")
    print()
    print("Based on the fundamental frequency f₀ = 141.7001 Hz")
    
    # ========================================================================
    # CAPA 1: MATHEMATICAL FOUNDATIONS
    # ========================================================================
    print_header("CAPA 1: MATHEMATICAL FOUNDATIONS", level=1)
    
    print_subsection("1.1 Riemann Operator Spectrum")
    spectrum = RiemannOperatorSpectrum(precision=50)
    freq_data = spectrum.fundamental_frequency()
    
    print(f"First eigenvalue λ₀: {freq_data['lambda_0']}")
    print(f"Universal constant C: {float(freq_data['C_universal']):.2f}")
    print(f"Derived frequency f₀: {float(freq_data['f0_complete']):.4f} Hz")
    print(f"Measured frequency: {float(freq_data['f0_measured']):.4f} Hz")
    print(f"Match: ✓" if abs(float(freq_data['f0_complete']) - 141.7001) < 1.0 else "Match: ✗")
    
    print_subsection("1.2 Number Theory & Golden Ratio")
    number_theory = NumberTheoryDerivation()
    phi = float(number_theory.phi)
    print(f"Golden ratio φ: {phi:.6f}")
    print(f"φ² = {phi**2:.6f}")
    print(f"1/φ = {1/phi:.6f}")
    print(f"φ - 1/φ = {phi - 1/phi:.6f}")
    
    print_subsection("1.3 Adelic Geometry & Coherence")
    adelic = AdelicGeometry()
    psi_f0 = adelic.global_coherence(141.7001)
    threshold = adelic.coherence_threshold()
    
    print(f"Global coherence Ψ at f₀: {float(psi_f0):.6f}")
    print(f"Coherence threshold: {float(threshold):.6f}")
    print(f"Meets threshold: {'✓ YES' if float(psi_f0) >= float(threshold) else '✗ NO'}")
    
    print_subsection("1.4 πCODE Algebra")
    picode_alg = PiCodeAlgebra()
    test_value = 141.7001
    encoded = picode_alg.encode(test_value)
    decoded = picode_alg.decode(encoded)
    
    print(f"Original value: {test_value:.4f}")
    print(f"πCODE encoded: {len([x for x in encoded if abs(x) > 1e-10])} non-zero components")
    print(f"Decoded value: {decoded:.4f}")
    print(f"Encoding accuracy: {abs(decoded - test_value) / test_value * 100:.2f}%")
    
    # ========================================================================
    # CAPA 2: QUANTUM PHYSICS
    # ========================================================================
    print_header("CAPA 2: QUANTUM PHYSICS", level=1)
    
    print_subsection("2.1 GW250114 Ringdown Analysis")
    gw = GW250114RingdownAnalysis()
    t, h = gw.generate_ringdown(duration=0.5)
    detection = gw.detect_141hz_resonance(h)
    
    print(f"Signal duration: {len(t) / gw.sample_rate:.3f} seconds")
    print(f"Sample rate: {gw.sample_rate} Hz")
    print(f"141.7 Hz detected: {'✓ YES' if detection['detected'] else '✗ NO'}")
    if detection['detected']:
        print(f"  Frequency: {detection['frequency']:.2f} Hz")
        print(f"  SNR: {detection['snr']:.2f}")
        print(f"  Deviation: {detection['deviation_from_f0']:.3f} Hz")
    
    print_subsection("2.2 Spacetime Resonance")
    spacetime = SpacetimeResonance()
    wavelength = spacetime.geometric_wavelength()
    energy = spacetime.resonance_energy()
    planck_ratio = spacetime.planck_scale_ratio()
    
    print(f"Geometric wavelength λ: {float(wavelength):.6e} m")
    print(f"Graviton energy E: {float(energy):.6e} J")
    print(f"λ/l_Planck ratio: {float(planck_ratio):.6e}")
    
    # Test black hole resonance
    print("\nBlack hole resonance conditions:")
    for mass in [30, 60, 90, 120]:
        can_resonate = spacetime.resonance_condition(mass)
        status = "✓" if can_resonate else "✗"
        print(f"  {status} {mass} M☉")
    
    print_subsection("2.3 Coherence Ψ as Observable")
    coh_obs = CoherencePsiObservable()
    eigenvalues, eigenvectors = coh_obs.coherence_eigenstates(dim=5)
    
    print(f"Coherence operator eigenvalues:")
    for i, eig in enumerate(eigenvalues):
        meets_threshold = coh_obs.is_coherent(eig)
        status = "✓" if meets_threshold else " "
        print(f"  λ_{i} = {eig:.6f} {status}")
    
    print_subsection("2.4 Fundamental 88s Pulses")
    pulses = FundamentalPulses()
    T_derived = pulses.derive_pulse_period()
    E_pulse = pulses.pulse_energy()
    
    print(f"Derived pulse period: {float(T_derived):.2f} s")
    print(f"Expected period: {float(pulses.T_pulse)} s")
    print(f"Match: {'✓' if abs(float(T_derived) - 88.0) < 10 else '✗'}")
    print(f"Energy per pulse: {float(E_pulse):.6e} J")
    
    # ========================================================================
    # CAPA 3: COMPUTATIONAL ARCHITECTURE
    # ========================================================================
    print_header("CAPA 3: COMPUTATIONAL ARCHITECTURE", level=1)
    
    print_subsection("3.1 Native 141.7 Hz Hardware")
    hw1 = NativeFrequencyHardware()
    hw2 = NativeFrequencyHardware()
    
    print(f"Operating frequency: {hw1.f0} Hz")
    print(f"Clock period: {hw1.clock_period * 1000:.3f} ms")
    print(f"Quality factor Q: {hw1.resonance_quality():.2f}")
    print(f"Power (relative to 1 GHz): {hw1.power_consumption():.2e}")
    
    # Synchronize two hardware units
    for _ in range(20):
        hw1.tick()
        hw2.tick()
    
    synced = hw1.is_synchronized(hw2)
    print(f"\nTwo units synchronized: {'✓ YES' if synced else '✗ NO'}")
    
    print_subsection("3.2 Coherent (Non-Binary) Registers")
    regs = CoherentRegisters(num_registers=8)
    
    # Demonstrate quantum operations
    regs.write(0, 1.0, 0.0)
    regs.write(1, 1.0, np.pi/2)
    regs.superpose(0, 1, 2)
    regs.apply_golden_gate(2)
    
    print("Register operations:")
    for i in range(3):
        amp, phase = regs.read(i)
        print(f"  R{i}: amp={amp:.3f}, φ={phase:.3f} rad ({np.degrees(phase):.1f}°)")
    
    coherence_01 = regs.measure_coherence(0, 1)
    print(f"\nCoherence R0-R1: {coherence_01:.6f}")
    
    print_subsection("3.3 Phase-Based Memory")
    memory = PhaseMemory(capacity=256)
    
    # Test byte encoding/decoding
    test_bytes = [0, 42, 127, 200, 255]
    print("Phase memory byte encoding:")
    for byte_val in test_bytes:
        memory.encode_byte(byte_val, byte_val)
        decoded = memory.decode_byte(byte_val)
        match = "✓" if abs(decoded - byte_val) <= 1 else "✗"
        print(f"  {byte_val:3d} → {decoded:3d} {match}")
    
    print_subsection("3.4 Resonance Processor")
    processor = ResonanceProcessor()
    
    # Demonstrate resonance operations
    processor.registers.write(0, 1.0, np.pi/6)
    processor.registers.write(1, 1.0, np.pi/4)
    processor.resonance_add(0, 1, 2)
    
    stats = processor.get_statistics()
    print("Processor statistics:")
    print(f"  Operations executed: {stats['total_operations']}")
    print(f"  Active registers: {stats['active_registers']}")
    print(f"  Memory usage: {stats['memory_usage']} cells")
    
    # ========================================================================
    # CAPA 4: ONTOLOGICAL NETWORK
    # ========================================================================
    print_header("CAPA 4: ONTOLOGICAL NETWORK", level=1)
    
    print_subsection("4.1 Node Synchronization (Ψ ≥ 0.888)")
    sync = NodeSynchronization(threshold=0.888)
    
    # Create network of nodes
    nodes = [
        ("alice", NodeType.CONTRIBUTOR),
        ("bob", NodeType.VALIDATOR),
        ("charlie", NodeType.RESONATOR),
        ("dave", NodeType.OBSERVER),
    ]
    
    for node_id, node_type in nodes:
        sync.register_node(node_id, node_type)
    
    # Evolve network
    sync.evolve_network(steps=30)
    
    # Attempt synchronizations
    synced_pairs = []
    print("Node synchronization attempts:")
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            id1, id2 = nodes[i][0], nodes[j][0]
            coherence = sync.measure_coherence(id1, id2)
            synced = sync.synchronize_nodes(id1, id2)
            if synced:
                synced_pairs.append((id1, id2))
            status = "✓" if synced else "✗"
            print(f"  {status} {id1:8s} ↔ {id2:8s}: Ψ={coherence:.3f}")
    
    net_coherence = sync.network_coherence()
    print(f"\nNetwork coherence: {net_coherence:.6f}")
    print(f"Synchronized pairs: {len(synced_pairs)}")
    
    print_subsection("4.2 πCODE as Value Unit")
    picode = PiCodeValue()
    
    # Mint πCODE from coherence
    contributions = [
        ("alice", 0.95),
        ("bob", 0.92),
        ("charlie", 0.89),
        ("dave", 0.75)  # Below threshold
    ]
    
    print("πCODE minting from coherence:")
    for node_id, coherence in contributions:
        minted = picode.mint_picode(node_id, coherence)
        balance = picode.get_balance(node_id)
        status = "✓" if minted > 0 else "✗"
        print(f"  {status} {node_id:8s}: Ψ={coherence:.2f} → {minted:8.4f} πCODE (bal: {balance:.4f})")
    
    print(f"\nTotal πCODE supply: {picode.total_supply:.4f}")
    
    # Demonstrate transfer with coherence proof
    if synced_pairs:
        n1, n2 = synced_pairs[0]
        amount = 0.5
        coh_proof = sync.measure_coherence(n1, n2)
        tx = picode.transfer(n1, n2, amount, coh_proof)
        
        if tx:
            print(f"\nπCODE transfer:")
            print(f"  {n1} → {n2}: {amount:.2f} πCODE")
            print(f"  Coherence proof: {coh_proof:.3f}")
            print(f"  Transaction ID: {tx.tx_id[:16]}...")
    
    print_subsection("4.3 Distributed Recognition (No Consensus)")
    recognition = DistributedRecognition(min_recognizers=3)
    
    # Submit contribution
    contribution = {
        "type": "gravitational_wave_analysis",
        "event": "GW250114",
        "frequency": 141.7001,
        "coherence": 0.93,
        "detector": "H1+L1"
    }
    
    event = recognition.submit_contribution("alice", contribution)
    print(f"Contribution submitted: {event.event_id[:16]}...")
    
    # Independent recognizers
    recognizers = [
        ("bob", 0.94),
        ("charlie", 0.91),
        ("dave", 0.89)
    ]
    
    print("\nIndependent recognition:")
    for recognizer_id, score in recognizers:
        recognition.recognize_contribution(event.event_id, recognizer_id, score)
        print(f"  ✓ {recognizer_id:8s} recognizes with Ψ={score:.2f}")
    
    is_recognized = recognition.is_recognized(event.event_id)
    print(f"\n{'✓' if is_recognized else '✗'} Contribution recognized: {is_recognized}")
    print(f"  Final coherence: {event.coherence_level:.3f}")
    print(f"  Recognizers: {len(event.recognizers)}")
    
    if is_recognized:
        awarded = recognition.award_picode(event.event_id, picode)
        print(f"  πCODE awarded: {awarded:.4f}")
    
    print_subsection("4.4 Symbiotic Economy (Value Creation)")
    economy = SymbioticEconomy()
    picode_econ = PiCodeValue()
    
    # Create symbiotic relationships
    symbioses = [
        ("alice", "bob", 0.92),
        ("bob", "charlie", 0.89),
        ("alice", "charlie", 0.90)
    ]
    
    print("Symbiotic relationships:")
    for n1, n2, coh in symbioses:
        success = economy.initiate_symbiosis(n1, n2, coh)
        status = "✓" if success else "✗"
        print(f"  {status} {n1:8s} ⟷ {n2:8s}: Ψ={coh:.2f}")
    
    # Symbiotic interactions (both gain)
    print("\nSymbiotic interactions (mutual value creation):")
    total_created = 0.0
    for n1, n2, _ in symbioses:
        v1, v2 = economy.symbiotic_interaction(n1, n2, picode_econ)
        total_created += v1 + v2
        print(f"  {n1:8s} gains {v1:8.4f} πCODE")
        print(f"  {n2:8s} gains {v2:8.4f} πCODE")
    
    print(f"\nTotal value created: {total_created:.4f} πCODE")
    print("(This is creation, not transfer - the total increased)")
    
    # ========================================================================
    # COMPLETE SYSTEM VALIDATION
    # ========================================================================
    print_header("COMPLETE SYSTEM VALIDATION", level=1)
    
    print("\nValidating all four layers...")
    validation = validate_all_layers()
    
    all_passed = True
    for layer_name, layer_results in validation.items():
        print(f"\n{layer_name.upper()}:")
        for component, passed in layer_results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {component:30s}: {status}")
            if not passed:
                all_passed = False
    
    # Final summary
    print_header("DEMONSTRATION COMPLETE", level=1)
    
    if all_passed:
        print("\n✓ ALL SYSTEMS OPERATIONAL")
        print("\nThe four-layer QCAL architecture is functioning correctly:")
        print("  • Mathematical foundations are sound")
        print("  • Quantum physics components are validated")
        print("  • Computational architecture is working")
        print("  • Ontological network is synchronized")
        print("\nThe system is ready for:")
        print("  - GW250114 analysis at 141.7 Hz")
        print("  - Coherence-based computation")
        print("  - Distributed consensus-free validation")
        print("  - Post-monetary value creation")
    else:
        print("\n⚠ SOME COMPONENTS NEED ATTENTION")
        print("Please review failed validations above.")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
