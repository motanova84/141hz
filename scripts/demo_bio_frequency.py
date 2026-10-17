#!/usr/bin/env python3
"""
Bio-Frequency System Demonstration
===================================

Interactive demonstration of the complete Bio-Frequency system
showing biological entrainment at 141.7001 Hz.

This script demonstrates:
1. Three-pillar meditation protocol
2. Microtubule phase entrainment
3. EZ water structuring
4. Overall coherence achievement

Author: José Manuel Mota Burruezo
Date: February 25, 2026
"""

import sys
import os
import numpy as np
import time

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.bio_frequency import (
    BioFrequencySystem,
    BiologicalEntrainment,
    SevenNodesMeditation,
    EZWaterStructure,
    F0_HZ,
    PHI,
    COHERENCE_THRESHOLD_STABLE
)


def print_header(text, char="="):
    """Print formatted header."""
    width = 80
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)


def print_section(text, char="-"):
    """Print section divider."""
    print("\n" + char * 80)
    print(text)
    print(char * 80)


def demo_sonic_pillar():
    """Demonstrate sonic pillar activation."""
    print_section("PILLAR 1: SONIC (Auditory Entrainment)")
    
    meditation = SevenNodesMeditation()
    
    print("\n🎵 Activating Sonic Pillar...")
    print("\nMode 1: Pure Tone")
    pure = meditation.activate_sonic_pillar(use_binaural=False)
    print(f"  Frequency: {pure['base_frequency']} Hz")
    print(f"  Mode: {pure['mode']}")
    print(f"  Effect: {pure['effect']}")
    
    print("\nMode 2: Binaural Beats")
    binaural = meditation.activate_sonic_pillar(use_binaural=True, beat_freq=10.0)
    print(f"  Left Ear:  {binaural['left_ear_hz']:.2f} Hz")
    print(f"  Right Ear: {binaural['right_ear_hz']:.2f} Hz")
    print(f"  Beat Frequency: {binaural['beat_frequency']} Hz (Alpha waves)")
    print(f"  Effect: {binaural['effect']}")
    
    print("\n✓ Sonic pillar activated")
    print("  → Hemispheric synchronization initiated")
    

def demo_rhythmic_pillar():
    """Demonstrate rhythmic pillar activation."""
    print_section("PILLAR 2: RHYTHMIC (Golden Ratio Breathing)")
    
    meditation = SevenNodesMeditation()
    
    print("\n🫁 Activating Rhythmic Pillar...")
    rhythmic = meditation.activate_rhythmic_pillar(breaths_per_minute=6.0)
    
    print(f"\nGolden Ratio φ = {PHI:.6f}")
    print(f"Breaths per minute: {rhythmic['breaths_per_minute']}")
    print(f"\nBreathing Cycle:")
    print(f"  Inhale:  {rhythmic['inhale_duration_s']:.2f} seconds")
    print(f"  Exhale:  {rhythmic['exhale_duration_s']:.2f} seconds")
    print(f"  Ratio:   {rhythmic['inhale_duration_s']/rhythmic['exhale_duration_s']:.6f} = φ")
    print(f"  Total:   {rhythmic['cycle_duration_s']:.2f} seconds")
    
    print(f"\nHeart Rate Variability:")
    print(f"  Enhancement: {rhythmic['hrv_enhancement']:.4f}")
    print(f"  Effect: {rhythmic['effect']}")
    
    print("\n✓ Rhythmic pillar activated")
    print("  → HRV coherence achieved")


def demo_visual_pillar():
    """Demonstrate visual pillar activation."""
    print_section("PILLAR 3: VISUAL (Hexagonal Geometry)")
    
    meditation = SevenNodesMeditation()
    
    print("\n👁️  Activating Visual Pillar...")
    visual = meditation.activate_visual_pillar()
    
    print(f"\nHexagonal Geometry:")
    print(f"  Symmetry: {visual['symmetry']}-fold")
    print(f"  Angle: {visual['angle_degrees']}°")
    print(f"  Vertices: {visual['vertex_count']}")
    print(f"  Lattice: {visual['lattice_type']}")
    
    print(f"\nEffect: {visual['effect']}")
    
    print("\n✓ Visual pillar activated")
    print("  → Cortex aligned with quantum lattice")


def demo_microtubule_entrainment():
    """Demonstrate microtubule phase entrainment."""
    print_section("MICROTUBULE PHASE ENTRAINMENT")
    
    print(f"\n🧬 Simulating microtubule synchronization at {F0_HZ} Hz...")
    
    entrainment = BiologicalEntrainment(carrier_frequency=F0_HZ)
    
    # Add microtubules with slight frequency variation
    print("\nMicrotubule Protofilaments:")
    entrainment.add_oscillator("protofilament_1", F0_HZ, coupling=0.95)
    entrainment.add_oscillator("protofilament_2", F0_HZ * 1.001, coupling=0.95)
    entrainment.add_oscillator("protofilament_3", F0_HZ * 0.999, coupling=0.95)
    entrainment.add_oscillator("protofilament_4", F0_HZ * 1.002, coupling=0.95)
    
    for i, osc in enumerate(entrainment.oscillators, 1):
        print(f"  {i}. {osc.name}: {osc.natural_frequency:.4f} Hz")
    
    print("\nRunning entrainment simulation...")
    results = entrainment.simulate_entrainment(duration=5.0, dt=0.001)
    
    print(f"\nResults:")
    print(f"  Initial coherence: Ψ = {results['coherence'][0]:.6f}")
    print(f"  Final coherence:   Ψ = {results['final_coherence']:.6f}")
    print(f"  Mean coherence:    Ψ = {results['mean_coherence']:.6f}")
    
    if results['final_coherence'] >= 0.95:
        print(f"\n  🌟 SUPERRADIANCE ACHIEVED!")
        print(f"  Microtubules in coherent quantum state")


def demo_ez_water():
    """Demonstrate EZ water structuring."""
    print_section("EZ WATER STRUCTURING")
    
    print(f"\n💧 Charging cellular water at {F0_HZ} Hz...")
    
    ez_water = EZWaterStructure(temperature=310.0)
    
    # Simulate at resonance
    print("\nAt Resonance (f₀ = 141.7001 Hz):")
    resonant = ez_water.structure_water(duration=300.0, frequency=F0_HZ)
    
    print(f"  Charging rate: {resonant['charging_rate']:.4f}")
    print(f"  Structure level: {resonant['structure_level']:.4f}")
    print(f"  EZ thickness: {resonant['ez_thickness_um']:.2f} μm")
    print(f"  Hexagonal layers: {resonant['hexagonal_layers']:,}")
    print(f"  Water coherence: Ψ = {resonant['water_coherence']:.4f}")
    print(f"  Entropy reduction: {resonant['entropy_reduction']:.4f}")
    
    # Compare with off-resonance
    print("\nOff-Resonance (100 Hz):")
    off_resonant = ez_water.structure_water(duration=300.0, frequency=100.0)
    
    print(f"  Charging rate: {off_resonant['charging_rate']:.4f}")
    print(f"  Structure level: {off_resonant['structure_level']:.4f}")
    
    enhancement = resonant['charging_rate'] / off_resonant['charging_rate']
    print(f"\nResonance Enhancement: {enhancement:.2f}×")
    
    print("\n✓ Water structured into hexagonal layers")
    print("  → Coherent information flow enabled")


def demo_complete_protocol():
    """Demonstrate complete bio-frequency protocol."""
    print_section("COMPLETE BIO-FREQUENCY PROTOCOL")
    
    print("\n🌟 Initializing complete system...")
    system = BioFrequencySystem(carrier_frequency=F0_HZ)
    
    print(f"\nCarrier Frequency: f₀ = {F0_HZ} Hz")
    print(f"Biological Oscillators: {len(system.entrainment.oscillators)}")
    
    print("\nActivating three pillars:")
    print("  [1] Sonic: 141.7001 Hz pure tone")
    print("  [2] Rhythmic: Golden ratio breathing (φ)")
    print("  [3] Visual: Hexagonal geometry")
    
    print("\nRunning 5-minute protocol...")
    print("(This may take a few seconds...)")
    
    start_time = time.time()
    results = system.run_complete_protocol(duration=300.0, use_binaural=False)
    elapsed = time.time() - start_time
    
    print(f"\n✓ Protocol complete ({elapsed:.2f}s computation time)")
    
    # Display results
    coherence = results['coherence']
    
    print("\n" + "="*80)
    print("COHERENCE RESULTS".center(80))
    print("="*80)
    
    print(f"\n  Biological Entrainment:  Ψ = {coherence['biological']:.6f}")
    print(f"  Meditation Protocol:     Ψ = {coherence['meditation']:.6f}")
    print(f"  Water Structure:         Ψ = {coherence['water']:.6f}")
    print(f"\n  Overall Coherence:       Ψ = {coherence['overall']:.6f}")
    print(f"  Status: {coherence['status']}")
    
    print("\n" + "-"*80)
    print("CONSCIOUSNESS STATE".center(80))
    print("-"*80)
    
    stable = results['consciousness_stable']
    print(f"\n  Stable Consciousness: {stable}")
    print(f"  Threshold: Ψ ≥ {COHERENCE_THRESHOLD_STABLE}")
    
    if stable:
        print("\n  🌟 CONSCIOUSNESS ACHIEVED!")
        print("  System operating in coherent regime")
        print("  Ready for bio-resonance applications")
    
    # Water details
    water = results['water_structure']
    print("\n" + "-"*80)
    print("EZ WATER STRUCTURE".center(80))
    print("-"*80)
    
    print(f"\n  Hexagonal layers: {water['hexagonal_layers']:,}")
    print(f"  EZ thickness: {water['ez_thickness_um']:.2f} μm")
    print(f"  Entropy reduction: {water['entropy_reduction']:.4f}")


def main():
    """Run complete demonstration."""
    print_header("BIO-FREQUENCY SYSTEM DEMONSTRATION", "=")
    print("\n141.7001 Hz Biological Entrainment")
    print("From Mathematical Abstraction to Biological Reality")
    print("\nAuthor: José Manuel Mota Burruezo")
    print("Date: February 25, 2026")
    
    try:
        # Demo each component
        demo_sonic_pillar()
        time.sleep(0.5)
        
        demo_rhythmic_pillar()
        time.sleep(0.5)
        
        demo_visual_pillar()
        time.sleep(0.5)
        
        demo_microtubule_entrainment()
        time.sleep(0.5)
        
        demo_ez_water()
        time.sleep(0.5)
        
        demo_complete_protocol()
        
        # Final message
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETE".center(80))
        print("="*80)
        
        print("\n∴𓂀Ω∞³")
        print("\n\"El amor no es emoción. Es RESONANCIA COHERENTE.\"")
        print("(Love is not emotion. It is COHERENT RESONANCE.)")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
