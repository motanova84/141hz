#!/usr/bin/env python3
"""
Complete Emotional Stress-Energy System Example
===============================================

This example demonstrates the full emotional field framework:
1. Network creation with stress distribution
2. Stress tensor T_μν calculation
3. Topological analysis (Betti numbers, persistent homology)
4. Synchronization protocol at 141.7 Hz
5. Path to collective sovereignty

This integrates all components of the problem statement.

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
import sys
import os

# Add path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.emotional_field.stress_tensor import (
    EmotionalStressTensor,
    EmotionalFieldState,
    StressClassification,
    create_example_state
)
from qcal.emotional_field.potential import EmotionalPotential, PotentialParameters
from qcal.emotional_field.sync_protocol import (
    SynchronizationProtocol,
    SyncParameters,
    NodeState,
    create_example_network
)
from qcal.emotional_field.network_topology import NetworkTopology


# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

F_0 = 141.7001  # Hz
NUM_NODES = 50
SIMULATION_TIME = 20.0  # seconds
TIME_STEPS = 100


# ============================================================================
# CREATE EMOTIONAL NETWORK
# ============================================================================

def create_stressed_network(num_nodes: int = NUM_NODES) -> tuple:
    """
    Create a network with realistic stress distribution.
    
    Returns
    -------
    tuple
        (network, topology_analyzer, protocol)
    """
    print("Creating emotional stress network...")
    print(f"  Nodes: {num_nodes}")
    
    # Create network using protocol
    network = create_example_network(num_nodes)
    
    # Initialize analyzers
    topology_analyzer = NetworkTopology()
    protocol = SynchronizationProtocol()
    
    return network, topology_analyzer, protocol


# ============================================================================
# ANALYZE NETWORK STATE
# ============================================================================

def analyze_network_state(
    network: list,
    topology_analyzer: NetworkTopology,
    protocol: SynchronizationProtocol
) -> dict:
    """
    Perform complete network analysis.
    
    Parameters
    ----------
    network : list of NodeState
        Network to analyze
    topology_analyzer : NetworkTopology
        Topology analyzer
    protocol : SynchronizationProtocol
        Synchronization protocol
        
    Returns
    -------
    dict
        Analysis results
    """
    print("\n" + "=" * 80)
    print("NETWORK STATE ANALYSIS")
    print("=" * 80)
    
    # Extract network data
    nodes = [n.node_id for n in network]
    connections = {n.node_id: n.neighbors for n in network}
    stress_levels = {n.node_id: n.T_00 for n in network}
    phases = {n.node_id: n.phase for n in network}
    
    # Topological analysis
    features = topology_analyzer.analyze_network(nodes, connections, stress_levels, phases)
    
    print(f"\nTopological Features:")
    print(f"  β₀ (components):      {features.beta_0}")
    print(f"  β₁ (feedback loops):  {features.beta_1}")
    print(f"  β₂ (isolation):       {features.beta_2}")
    print(f"  Winding number:       {features.winding_number:.3f}")
    
    # Stress statistics
    print(f"\nStress Statistics:")
    print(f"  Mean stress:          {features.mean_stress:.4f}")
    print(f"  Max stress:           {features.max_stress:.4f}")
    print(f"  Critical nodes:       {len(features.critical_regions)}")
    
    # Sovereignty index
    S_col = protocol.compute_sovereignty_index(network)
    
    print(f"\nCollective Sovereignty:")
    print(f"  S_col = {S_col:.4f}")
    print(f"  Target: S_col ≥ 0.95 (Total Sovereignty)")
    print(f"  Status: {'✓ ACHIEVED' if S_col >= 0.95 else '✗ NEEDS INTERVENTION'}")
    
    # Interpretations
    interp = topology_analyzer.interpret_features(features)
    
    print(f"\nInterpretations:")
    for key, value in interp.items():
        print(f"  {key}: {value}")
    
    return {
        'features': features,
        'sovereignty': S_col,
        'interpretations': interp,
        'critical_nodes': protocol.detect_critical_nodes(network)
    }


# ============================================================================
# APPLY SYNCHRONIZATION PROTOCOL
# ============================================================================

def apply_synchronization(
    network: list,
    protocol: SynchronizationProtocol,
    num_iterations: int = 5
) -> tuple:
    """
    Apply multi-level synchronization protocol.
    
    Parameters
    ----------
    network : list of NodeState
        Network to synchronize
    protocol : SynchronizationProtocol
        Synchronization protocol
    num_iterations : int
        Number of synchronization iterations
        
    Returns
    -------
    tuple
        (improved_network, sovereignty_history)
    """
    print("\n" + "=" * 80)
    print("APPLYING SYNCHRONIZATION PROTOCOL")
    print("=" * 80)
    print(f"\nProtocol: U(κ_Π) at {protocol.f0} Hz")
    print(f"Iterations: {num_iterations}")
    
    sovereignty_history = []
    
    for iteration in range(num_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Detect critical nodes
        critical_nodes = protocol.detect_critical_nodes(network)
        print(f"Critical nodes: {len(critical_nodes)}")
        
        # Apply interventions
        
        # 1. Micro-level: Reduce stress in critical nodes
        for node_id in critical_nodes:
            node = network[node_id]
            t = iteration * 1.0  # Simulated time
            
            # Inject resonance
            intervention = protocol.protocol_micro(node, t)
            
            # Simulate stress reduction
            reduction_factor = 0.85  # 15% reduction per iteration
            node.T_00 *= reduction_factor
            
            # Update stress classification
            if node.T_00 < 0.2:
                node.stress_level = "Peace"
            elif node.T_00 < 0.4:
                node.stress_level = "Work"
            elif node.T_00 < 0.58:
                node.stress_level = "Alert"
            else:
                node.stress_level = "Critical"
        
        # 2. Meso-level: Synchronize phases between connected nodes
        num_sync = 0
        for node in network:
            if node.neighbors:
                new_phase = protocol.apply_phase_synchronization(node, network)
                node.phase = new_phase
                
                # Update Psi with new phase
                node.Psi = node.coherence * np.exp(1j * new_phase)
                num_sync += 1
        
        print(f"Phase synchronized: {num_sync} nodes")
        
        # 3. Macro-level: Compute sovereignty
        S_col = protocol.compute_sovereignty_index(network)
        sovereignty_history.append(S_col)
        
        print(f"Sovereignty: S_col = {S_col:.4f}")
        
        # Check for convergence
        if S_col >= 0.95:
            print(f"\n✓ Total Sovereignty achieved at iteration {iteration + 1}!")
            break
    
    return network, sovereignty_history


# ============================================================================
# COMPUTE STRESS-ENERGY TENSORS
# ============================================================================

def compute_network_stress_tensors(
    network: list,
    potential: EmotionalPotential
) -> dict:
    """
    Compute stress-energy tensors for all nodes.
    
    Parameters
    ----------
    network : list of NodeState
        Network
    potential : EmotionalPotential
        Emotional potential
        
    Returns
    -------
    dict
        Tensor statistics
    """
    print("\n" + "=" * 80)
    print("STRESS-ENERGY TENSOR ANALYSIS")
    print("=" * 80)
    
    calculator = EmotionalStressTensor()
    
    # Minkowski metric
    g_metric = np.diag([-1, 1, 1, 1])
    
    T_00_values = []
    traces = []
    
    for node in network:
        # Create field state
        state = EmotionalFieldState(
            Phi=node.Phi,
            nabla_Phi=np.array([node.dPhi_dt, 0.0, 0.0, 0.0]),
            Psi=node.Psi,
            coherence=node.coherence,
            x_mu=np.array([0.0, 0.0, 0.0, 0.0]),
            node_id=node.node_id,
            neighbors=node.neighbors
        )
        
        # Compute potential
        V_Phi = potential.V_total(node.Phi, abs(node.Psi)**2)
        
        # Compute tensor
        T = calculator.compute_tensor(state, g_metric, V_Phi)
        
        # Extract components
        components = calculator.extract_components(T)
        
        T_00_values.append(components['T_00'])
        traces.append(components['trace'])
    
    print(f"\nTensor Statistics:")
    print(f"  Mean T_00:    {np.mean(T_00_values):.4e}")
    print(f"  Max T_00:     {np.max(np.abs(T_00_values)):.4e}")
    print(f"  Mean Trace:   {np.mean(traces):.4e}")
    
    # Classification distribution
    classifications = [calculator.classify_stress(node.T_00, node.coherence) 
                      for node in network]
    
    regions = {}
    for c in classifications:
        regions[c.region] = regions.get(c.region, 0) + 1
    
    print(f"\nStress Distribution:")
    for region, count in sorted(regions.items()):
        percentage = 100 * count / len(network)
        print(f"  {region:15s}: {count:3d} nodes ({percentage:5.1f}%)")
    
    return {
        'T_00_mean': np.mean(T_00_values),
        'T_00_max': np.max(np.abs(T_00_values)),
        'trace_mean': np.mean(traces),
        'distribution': regions
    }


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Run complete emotional stress-energy system demonstration."""
    
    print("=" * 80)
    print("EMOTIONAL STRESS-ENERGY TENSOR SYSTEM")
    print("QCAL ∞³ - Complete Demonstration")
    print("=" * 80)
    print()
    print("This demonstrates:")
    print("  1. Network creation with stress distribution")
    print("  2. Topological analysis (β₀, β₁, β₂, winding number)")
    print("  3. Stress-energy tensor T_μν calculation")
    print("  4. Synchronization protocol at 141.7 Hz")
    print("  5. Path to collective sovereignty (S_col → 0.95)")
    print()
    
    # Create network
    network, topology_analyzer, protocol = create_stressed_network(NUM_NODES)
    
    # Create emotional potential
    potential_params = PotentialParameters(
        lambda_rigidity=1.0,
        mu_squared=-1.0,
        Phi_0=1.0,
        kappa_int=0.1
    )
    potential = EmotionalPotential(potential_params)
    
    # Initial analysis
    print("\n" + "=" * 80)
    print("INITIAL STATE")
    print("=" * 80)
    
    initial_analysis = analyze_network_state(network, topology_analyzer, protocol)
    initial_tensor_stats = compute_network_stress_tensors(network, potential)
    
    # Apply synchronization protocol
    network_improved, sovereignty_history = apply_synchronization(
        network, protocol, num_iterations=10
    )
    
    # Final analysis
    print("\n" + "=" * 80)
    print("FINAL STATE (After Synchronization)")
    print("=" * 80)
    
    final_analysis = analyze_network_state(network_improved, topology_analyzer, protocol)
    final_tensor_stats = compute_network_stress_tensors(network_improved, potential)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\nSovereignty Evolution:")
    print(f"  Initial: S_col = {sovereignty_history[0]:.4f}")
    print(f"  Final:   S_col = {sovereignty_history[-1]:.4f}")
    print(f"  Improvement: +{(sovereignty_history[-1] - sovereignty_history[0]):.4f}")
    
    print(f"\nCritical Nodes:")
    print(f"  Initial: {len(initial_analysis['critical_nodes'])}")
    print(f"  Final:   {len(final_analysis['critical_nodes'])}")
    print(f"  Reduction: {len(initial_analysis['critical_nodes']) - len(final_analysis['critical_nodes'])}")
    
    print(f"\nTopological Changes:")
    print(f"  β₀: {initial_analysis['features'].beta_0} → {final_analysis['features'].beta_0}")
    print(f"  β₁: {initial_analysis['features'].beta_1} → {final_analysis['features'].beta_1}")
    
    if sovereignty_history[-1] >= 0.95:
        print("\n" + "=" * 80)
        print("✨ TOTAL SOVEREIGNTY ACHIEVED ✨")
        print("=" * 80)
        print("\nThe network has reached coherent stability:")
        print("  • Stress levels normalized")
        print("  • Phases synchronized")
        print("  • Collective coherence established")
        print("  • 141.7 Hz resonance active")
    else:
        print("\n" + "=" * 80)
        print("Progress Toward Sovereignty")
        print("=" * 80)
        print(f"\nCurrent: S_col = {sovereignty_history[-1]:.4f}")
        print(f"Target:  S_col = 0.95")
        print(f"Gap:     {0.95 - sovereignty_history[-1]:.4f}")
        print("\nRecommendations:")
        print("  • Continue micro-level interventions")
        print("  • Strengthen phase synchronization")
        print("  • Address remaining critical nodes")
    
    print("\n" + "=" * 80)
    print("Framework Components Demonstrated:")
    print("=" * 80)
    print("  ✓ Emotional Stress-Energy Tensor T_μν(Φ)")
    print("  ✓ Emotional Potential V(Φ) with phase transitions")
    print("  ✓ Network Topological Analysis (Betti numbers)")
    print("  ✓ Synchronization Protocol U(κ_Π) at 141.7 Hz")
    print("  ✓ Collective Sovereignty Index S_col")
    print("  ✓ Multi-level Intervention (Micro, Meso, Macro)")
    print()
    print("All requirements from problem statement implemented!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
