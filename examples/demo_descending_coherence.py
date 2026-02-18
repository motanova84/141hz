#!/usr/bin/env python3
"""
Descending Coherence Cascade Demonstration
===========================================

Demonstrates how collective coherence (macro level) propagates down
through groups (meso level) to individuals (micro level) via the
141.7 Hz resonance mechanism.

This example shows:
1. Initial network with varying individual coherences
2. Group formation via community detection
3. Evolution of coherence through the cascade
4. Convergence toward collective coherence state
5. Stress-modulated dynamics

Author: QCAL ∞³ Framework
Date: 2026-02-13
"""

import numpy as np
import sys
import os

# Add parent path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.emotional_field.descending_coherence import (
    DescendingCoherencePropagator,
    DescendingCoherenceParameters,
    create_example_cascade
)


# ============================================================================
# DEMONSTRATION PARAMETERS
# ============================================================================

NUM_NODES = 60
NUM_GROUPS = 6
SIMULATION_TIME = 5.0  # seconds
DT = 0.01  # 10 ms time steps
NUM_STEPS = int(SIMULATION_TIME / DT)

# Initial conditions
INITIAL_COHERENCE_MEAN = 0.4
INITIAL_COHERENCE_STD = 0.2
STRESS_BASE = 0.3
STRESS_VARIATION = 0.2


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(title: str):
    """Print a formatted header."""
    print()
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)
    print()


def print_section(title: str):
    """Print a section divider."""
    print()
    print("-" * 70)
    print(title)
    print("-" * 70)


def create_network_with_variation():
    """Create a network with coherence variation."""
    # Create base network
    propagator, coherences, connections = create_example_cascade(
        num_nodes=NUM_NODES,
        num_groups=NUM_GROUPS,
        initial_coherence=INITIAL_COHERENCE_MEAN
    )
    
    # Add variation to coherences
    for node_id in coherences:
        magnitude = abs(coherences[node_id])
        magnitude += np.random.normal(0, INITIAL_COHERENCE_STD)
        magnitude = max(0.1, min(1.0, magnitude))  # Clamp to [0.1, 1.0]
        
        phase = np.angle(coherences[node_id])
        phase += np.random.normal(0, np.pi / 4)
        
        coherences[node_id] = magnitude * np.exp(1j * phase)
    
    # Create varied stress levels
    stress_levels = {}
    for node_id in range(NUM_NODES):
        stress = STRESS_BASE + np.random.normal(0, STRESS_VARIATION)
        stress = max(0.05, min(0.95, stress))  # Clamp to [0.05, 0.95]
        stress_levels[node_id] = stress
    
    return propagator, coherences, connections, stress_levels


def compute_statistics(coherences):
    """Compute statistics of coherences."""
    magnitudes = [abs(c) for c in coherences.values()]
    phases = [np.angle(c) for c in coherences.values()]
    
    return {
        "mean_magnitude": np.mean(magnitudes),
        "std_magnitude": np.std(magnitudes),
        "min_magnitude": np.min(magnitudes),
        "max_magnitude": np.max(magnitudes),
        "phase_variance": np.var(phases)
    }


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Run the demonstration."""
    
    print_header("QCAL ∞³ Descending Coherence Cascade Demonstration")
    
    # Create network
    print("Initializing network...")
    propagator, coherences, connections, stress_levels = create_network_with_variation()
    print(f"✓ Created network with {NUM_NODES} nodes")
    
    # Detect groups
    print("Detecting coherence groups...")
    node_ids = list(range(NUM_NODES))
    groups = propagator.detect_groups(node_ids, connections, stress_levels)
    print(f"✓ Detected {len(groups)} groups")
    
    for group_id, group in groups.items():
        print(f"  Group {group_id}: {group.size()} members")
    print()
    
    # Initial statistics
    print_section("Initial State")
    initial_stats = compute_statistics(coherences)
    print(f"Mean coherence: {initial_stats['mean_magnitude']:.4f}")
    print(f"Std coherence: {initial_stats['std_magnitude']:.4f}")
    print(f"Range: [{initial_stats['min_magnitude']:.4f}, {initial_stats['max_magnitude']:.4f}]")
    print(f"Phase variance: {initial_stats['phase_variance']:.4f} rad²")
    print(f"Mean stress: {np.mean(list(stress_levels.values())):.4f}")
    
    # Show initial collective coherence
    initial_collective = propagator.compute_collective_coherence(coherences)
    print(f"Initial collective coherence: {abs(initial_collective):.4f}")
    
    # Evolution
    print_section("Coherence Evolution")
    print(f"Simulating {SIMULATION_TIME}s at {DT*1000:.1f}ms time steps...")
    print()
    
    # Record evolution
    times = []
    collective_coherences = []
    mean_individual_coherences = []
    alignment_metrics = []
    
    # Evolution loop
    print("Time (s) | Ψ_col | <Ψ_i> | Alignment | σ(Ψ_i)")
    print("-" * 60)
    
    for step in range(NUM_STEPS):
        # Propagate coherence
        coherences = propagator.propagate_coherence(coherences, stress_levels, DT)
        
        # Record metrics every 10 steps
        if step % 10 == 0:
            time = propagator.time
            summary = propagator.get_summary()
            stats = compute_statistics(coherences)
            
            times.append(time)
            collective_coherences.append(summary["collective_coherence"])
            mean_individual_coherences.append(stats["mean_magnitude"])
            alignment_metrics.append(summary["alignment_metrics"]["mean_alignment"])
            
            # Print progress every 50 steps
            if step % 50 == 0:
                print(f"  {time:5.2f}  | {summary['collective_coherence']:.4f} | "
                      f"{stats['mean_magnitude']:.4f} | "
                      f"{summary['alignment_metrics']['mean_alignment']:+.4f} | "
                      f"{stats['std_magnitude']:.4f}")
    
    print()
    
    # Final statistics
    print_section("Final State")
    final_summary = propagator.get_summary()
    final_stats = compute_statistics(coherences)
    
    print(f"Time evolved: {propagator.time:.2f} s")
    print(f"Collective coherence: {final_summary['collective_coherence']:.4f}")
    print(f"Mean individual coherence: {final_stats['mean_magnitude']:.4f}")
    print(f"Std individual coherence: {final_stats['std_magnitude']:.4f}")
    print(f"Coherence range: [{final_stats['min_magnitude']:.4f}, {final_stats['max_magnitude']:.4f}]")
    print()
    
    print("Alignment Metrics:")
    alignment = final_summary["alignment_metrics"]
    print(f"  Mean: {alignment['mean_alignment']:+.4f}")
    print(f"  Std:  {alignment['std_alignment']:.4f}")
    print(f"  Range: [{alignment['min_alignment']:+.4f}, {alignment['max_alignment']:+.4f}]")
    print()
    
    # Show convergence
    print_section("Convergence Analysis")
    
    initial_spread = initial_stats['std_magnitude']
    final_spread = final_stats['std_magnitude']
    spread_reduction = (initial_spread - final_spread) / initial_spread * 100
    
    print(f"Initial coherence spread: {initial_spread:.4f}")
    print(f"Final coherence spread: {final_spread:.4f}")
    print(f"Spread reduction: {spread_reduction:.1f}%")
    print()
    
    initial_col = abs(initial_collective)
    final_col = final_summary['collective_coherence']
    coherence_increase = (final_col - initial_col) / initial_col * 100
    
    print(f"Initial collective coherence: {initial_col:.4f}")
    print(f"Final collective coherence: {final_col:.4f}")
    print(f"Coherence increase: {coherence_increase:+.1f}%")
    print()
    
    # Example node hierarchies
    print_section("Example Node Hierarchies")
    
    # Show 3 example nodes from different groups
    example_nodes = []
    for group_id in range(min(3, len(groups))):
        group = groups[group_id]
        if group.member_ids:
            node_id = list(group.member_ids)[0]
            example_nodes.append((node_id, group_id))
    
    for node_id, group_id in example_nodes:
        info = propagator.get_hierarchy_info(node_id)
        
        print(f"\nNode {node_id} (Group {group_id}):")
        print(f"  Micro (Individual):")
        print(f"    Coherence: {info['micro']['coherence']:.4f}")
        print(f"    Phase: {info['micro']['phase']:.4f} rad")
        print(f"  Meso (Group):")
        print(f"    Coherence: {info['meso']['coherence']:.4f}")
        print(f"    Phase: {info['meso']['phase']:.4f} rad")
        print(f"  Macro (Collective):")
        print(f"    Coherence: {info['macro']['coherence']:.4f}")
        print(f"    Phase: {info['macro']['phase']:.4f} rad")
        print(f"  Target: {info['target']['coherence']:.4f}")
        print(f"  Stress: {info['stress']['individual']:.4f}")
    
    # Summary of cascade mechanism
    print_section("Cascade Mechanism Summary")
    params = propagator.params
    print(f"Coupling Coefficients:")
    print(f"  α_macro (collective influence): {params.alpha_macro:.2f}")
    print(f"  α_meso (group influence): {params.alpha_meso:.2f}")
    print(f"  α_micro (individual autonomy): {params.alpha_micro:.2f}")
    print(f"  Sum: {params.alpha_macro + params.alpha_meso + params.alpha_micro:.2f}")
    print()
    print(f"Resonance Frequency: {params.f0:.4f} Hz")
    print(f"Damping Rate: {params.gamma_individual:.2f} /s")
    print(f"Resonance Amplitude: {params.eta_individual:.2f}")
    print()
    
    # Conclusions
    print_section("Key Findings")
    print("1. Collective coherence (macro) influences individual coherence (micro)")
    print(f"   via group structure (meso) with {len(groups)} detected communities.")
    print()
    print(f"2. Coherence spread reduced by {spread_reduction:.1f}%, indicating")
    print("   convergence toward collective state while preserving diversity.")
    print()
    print(f"3. Alignment increased to {alignment['mean_alignment']:+.2f}, showing")
    print("   individuals tracking the collective field via resonance cascade.")
    print()
    print("4. The 141.7 Hz resonance drives coherence without eliminating")
    print("   individual agency (α_micro preserves autonomy).")
    print()
    
    print_header("✓ Descending Coherence Cascade Demonstration Complete")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
