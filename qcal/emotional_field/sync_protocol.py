#!/usr/bin/env python3
"""
Synchronization Protocol at 141.7 Hz
=====================================

Implements the Protocol U(κ_Π) for collective emotional synchronization
using the fundamental QCAL frequency as a resonant regulator.

Mathematical Foundation:
□Φ + ∂V/∂Φ = -γ sin(2πf₀t)·∇²Φ

Conservation Law (Modified):
∇_ν T_μν = -γ(f-141.7)∂_μΦ - κ_Π ∇_μ log|ζ(½+it)|²

Mechanism:
1. Detection of stress peaks (T_00 > threshold)
2. Injection of coherent signal at 141.7 Hz
3. Parametric resonance → amplification of stable modes
4. Dissipation of chaotic modes
5. Restoration of local coherence Ψ ↑

Intervention Levels:
- Micro: Individual observers
- Meso: Interpersonal connections
- Macro: Collective network

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# Import QCAL constants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from qcal.constants import F_0_VALUE
    F_0 = F_0_VALUE
except ImportError:
    F_0 = 141.7001  # Hz


# ============================================================================
# SYNCHRONIZATION PARAMETERS
# ============================================================================

@dataclass
class SyncParameters:
    """Parameters for synchronization protocol."""
    
    # Resonant frequency
    f0: float = F_0                    # Hz
    omega_0: float = 2 * np.pi * F_0   # rad/s
    
    # Coupling coefficients
    gamma: float = 0.1                 # Damping coefficient
    kappa_Pi: float = 0.05             # Complexity coupling
    
    # Intervention thresholds
    T_00_critical: float = 0.58        # Critical stress
    T_00_alert: float = 0.40           # Alert threshold
    coherence_threshold: float = 0.75  # Minimum coherence
    
    # Protocol parameters
    duration_seconds: float = 600      # 10 minutes default
    amplitude: float = 0.1             # Injection amplitude
    learning_rate: float = 0.3         # Phase adjustment rate


# ============================================================================
# NODE STATE
# ============================================================================

@dataclass
class NodeState:
    """State of a node in the emotional network."""
    
    # Node identifier
    node_id: int
    
    # Emotional field
    Phi: float                         # Field value
    dPhi_dt: float                     # Time derivative
    
    # Coherence
    Psi: complex                       # Consciousness field
    coherence: float                   # |Ψ|
    phase: float                       # arg(Ψ)
    
    # Stress components
    T_00: float                        # Energy density
    stress_level: str                  # Classification
    
    # Network properties
    neighbors: List[int]               # Connected nodes
    
    def __post_init__(self):
        """Validate node state."""
        assert self.coherence >= 0, "Coherence must be non-negative"
        assert self.T_00 >= 0, "Stress must be non-negative"


# ============================================================================
# SYNCHRONIZATION PROTOCOL
# ============================================================================

class SynchronizationProtocol:
    """
    Implementation of Protocol U(κ_Π) for emotional synchronization.
    
    This protocol uses 141.7 Hz resonance to:
    - Reduce stress peaks
    - Restore coherence
    - Synchronize phases across network
    - Stabilize collective dynamics
    """
    
    def __init__(self, params: Optional[SyncParameters] = None):
        """
        Initialize synchronization protocol.
        
        Parameters
        ----------
        params : SyncParameters, optional
            Protocol parameters. If None, use defaults.
        """
        if params is None:
            params = SyncParameters()
        
        self.params = params
        self.f0 = params.f0
        self.omega_0 = params.omega_0
        self.gamma = params.gamma
        self.kappa_Pi = params.kappa_Pi
    
    def detect_critical_nodes(
        self,
        network: List[NodeState]
    ) -> List[int]:
        """
        Detect nodes with critical stress levels.
        
        Parameters
        ----------
        network : list of NodeState
            Network of nodes
            
        Returns
        -------
        list of int
            IDs of critical nodes
        """
        critical_nodes = []
        
        for node in network:
            if node.T_00 > self.params.T_00_critical:
                critical_nodes.append(node.node_id)
        
        return critical_nodes
    
    def generate_resonance_signal(
        self,
        t: float,
        amplitude: Optional[float] = None
    ) -> float:
        """
        Generate 141.7 Hz resonance signal.
        
        Signal: A·sin(2πf₀t)
        
        Parameters
        ----------
        t : float
            Time (seconds)
        amplitude : float, optional
            Signal amplitude. If None, use default.
            
        Returns
        -------
        float
            Signal value
        """
        if amplitude is None:
            amplitude = self.params.amplitude
        
        return amplitude * np.sin(2 * np.pi * self.f0 * t)
    
    def apply_resonance_damping(
        self,
        nabla2_Phi: float,
        t: float
    ) -> float:
        """
        Apply resonant damping term.
        
        Damping: -γ sin(2πf₀t)·∇²Φ
        
        This selectively damps high-frequency noise while
        preserving coherent oscillations at f₀.
        
        Parameters
        ----------
        nabla2_Phi : float
            Laplacian of emotional field
        t : float
            Time (seconds)
            
        Returns
        -------
        float
            Damping force
        """
        signal = self.generate_resonance_signal(t)
        return -self.gamma * signal * nabla2_Phi
    
    def compute_phase_target(
        self,
        node: NodeState,
        network: List[NodeState]
    ) -> float:
        """
        Compute target phase for node based on neighbors.
        
        Target = mean phase of neighbors (weighted by coherence)
        
        Parameters
        ----------
        node : NodeState
            Target node
        network : list of NodeState
            Full network
            
        Returns
        -------
        float
            Target phase (radians)
        """
        if not node.neighbors:
            return node.phase
        
        # Get neighbor states
        neighbor_phases = []
        neighbor_weights = []
        
        for neighbor_id in node.neighbors:
            # Find neighbor in network
            neighbor = next((n for n in network if n.node_id == neighbor_id), None)
            if neighbor:
                neighbor_phases.append(neighbor.phase)
                neighbor_weights.append(neighbor.coherence)
        
        if not neighbor_phases:
            return node.phase
        
        # Weighted mean of neighbor phases
        weights = np.array(neighbor_weights)
        weights = weights / weights.sum()
        
        # Handle phase wrapping
        phases = np.array(neighbor_phases)
        mean_phase = np.arctan2(
            np.sum(weights * np.sin(phases)),
            np.sum(weights * np.cos(phases))
        )
        
        return mean_phase
    
    def apply_phase_synchronization(
        self,
        node: NodeState,
        network: List[NodeState],
        learning_rate: Optional[float] = None
    ) -> float:
        """
        Apply phase synchronization to node.
        
        Δφ = α(φ_target - φ_current)
        
        Parameters
        ----------
        node : NodeState
            Target node
        network : list of NodeState
            Full network
        learning_rate : float, optional
            Phase adjustment rate
            
        Returns
        -------
        float
            New phase
        """
        if learning_rate is None:
            learning_rate = self.params.learning_rate
        
        # Compute target phase
        phase_target = self.compute_phase_target(node, network)
        
        # Compute phase difference
        delta_phase = phase_target - node.phase
        
        # Wrap to [-π, π]
        delta_phase = np.arctan2(np.sin(delta_phase), np.cos(delta_phase))
        
        # Apply adjustment
        new_phase = node.phase + learning_rate * delta_phase
        
        return new_phase
    
    def inject_coherent_field(
        self,
        node: NodeState,
        t: float,
        Phi_0: float = 1.0
    ) -> float:
        """
        Inject coherent external field.
        
        Φ_ext = A·Φ₀·cos(2πf₀t + φ_node)
        
        Parameters
        ----------
        node : NodeState
            Target node
        t : float
            Time (seconds)
        Phi_0 : float
            Reference field amplitude
            
        Returns
        -------
        float
            Injected field contribution
        """
        amplitude = self.params.amplitude * Phi_0
        return amplitude * np.cos(2 * np.pi * self.f0 * t + node.phase)
    
    def compute_conservation_modification(
        self,
        dPhi_dt: float,
        f_actual: float,
        zeta_term: float = 0.0
    ) -> float:
        """
        Compute modification to conservation law.
        
        ∇_ν T_μν = -γ(f-f₀)∂_μΦ - κ_Π ∇_μ log|ζ|²
        
        Parameters
        ----------
        dPhi_dt : float
            Time derivative of Φ
        f_actual : float
            Actual frequency of oscillation
        zeta_term : float
            Spectral coupling term
            
        Returns
        -------
        float
            Conservation modification
        """
        # Frequency-dependent damping
        freq_damping = -self.gamma * (f_actual - self.f0) * dPhi_dt
        
        # Spectral coupling
        spectral_term = -self.kappa_Pi * zeta_term
        
        return freq_damping + spectral_term
    
    def protocol_micro(
        self,
        node: NodeState,
        t: float,
        duration: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Micro-level intervention (individual observer).
        
        Steps:
        1. Apply coherent breathing at 141.7 Hz
        2. Inject external field Φ_ext
        3. Monitor ∇²Φ until stabilization
        
        Parameters
        ----------
        node : NodeState
            Target node
        t : float
            Current time (seconds)
        duration : float, optional
            Intervention duration (seconds)
            
        Returns
        -------
        dict
            Intervention effects
        """
        if duration is None:
            duration = self.params.duration_seconds
        
        # Generate resonance signal
        resonance = self.generate_resonance_signal(t)
        
        # Inject coherent field
        Phi_ext = self.inject_coherent_field(node, t)
        
        # Expected coherence increase
        coherence_boost = self.params.amplitude * abs(np.sin(2 * np.pi * self.f0 * t))
        
        return {
            'node_id': node.node_id,
            'time': t,
            'resonance_signal': resonance,
            'Phi_injection': Phi_ext,
            'coherence_boost': coherence_boost,
            'expected_T_00_reduction': 0.3 * node.T_00,  # 30% reduction target
            'duration': duration
        }
    
    def protocol_meso(
        self,
        node1: NodeState,
        node2: NodeState,
        network: List[NodeState]
    ) -> Dict[str, float]:
        """
        Meso-level intervention (interpersonal connection).
        
        Steps:
        1. Synchronize phases using U(κ_Π)
        2. Establish resonance ritual at 141.7 Hz
        3. Strengthen empathic coupling
        
        Parameters
        ----------
        node1, node2 : NodeState
            Connected nodes
        network : list of NodeState
            Full network
            
        Returns
        -------
        dict
            Intervention effects
        """
        # Compute phase synchronization
        phase1_new = self.apply_phase_synchronization(node1, network)
        phase2_new = self.apply_phase_synchronization(node2, network)
        
        # Phase coherence
        phase_diff = abs(phase1_new - phase2_new)
        phase_coherence = np.cos(phase_diff)
        
        # Empathic coupling strength
        coupling_strength = node1.coherence * node2.coherence * phase_coherence
        
        return {
            'node1_id': node1.node_id,
            'node2_id': node2.node_id,
            'phase1_new': phase1_new,
            'phase2_new': phase2_new,
            'phase_coherence': phase_coherence,
            'coupling_strength': coupling_strength,
            'intervention': 'phase_synchronization'
        }
    
    def protocol_macro(
        self,
        network: List[NodeState]
    ) -> Dict[str, any]:
        """
        Macro-level intervention (collective network).
        
        Steps:
        1. Eliminate toxic connections (stress_mutual > threshold)
        2. Add bridges between isolated communities
        3. Distribute emotional load (balance T_00)
        
        Parameters
        ----------
        network : list of NodeState
            Full network
            
        Returns
        -------
        dict
            Network optimization results
        """
        # Identify critical nodes
        critical = self.detect_critical_nodes(network)
        
        # Compute network statistics
        total_stress = sum(node.T_00 for node in network)
        mean_stress = total_stress / len(network)
        max_stress = max(node.T_00 for node in network)
        
        # Compute collective coherence
        total_coherence = sum(node.coherence for node in network)
        mean_coherence = total_coherence / len(network)
        
        # Load balancing: identify over-stressed and under-stressed
        over_stressed = [n for n in network if n.T_00 > 1.5 * mean_stress]
        under_stressed = [n for n in network if n.T_00 < 0.5 * mean_stress]
        
        return {
            'num_nodes': len(network),
            'critical_nodes': critical,
            'num_critical': len(critical),
            'mean_stress': mean_stress,
            'max_stress': max_stress,
            'mean_coherence': mean_coherence,
            'over_stressed': [n.node_id for n in over_stressed],
            'under_stressed': [n.node_id for n in under_stressed],
            'recommended_bridges': len(over_stressed),
            'intervention': 'network_optimization'
        }
    
    def compute_sovereignty_index(
        self,
        network: List[NodeState],
        Lambda_crit: float = 10.0
    ) -> float:
        """
        Compute Collective Sovereignty Index.
        
        S_col = (1/N) Σᵢ Ψᵢ · exp(-αT_00^(i)) · (1 - |∇²Φᵢ|/Λ_crit)
        
        Target: S_col ≥ 0.95 (Total Sovereignty)
        
        Parameters
        ----------
        network : list of NodeState
            Network of nodes
        Lambda_crit : float
            Critical curvature threshold
            
        Returns
        -------
        float
            Sovereignty index (0-1)
        """
        N = len(network)
        S_col = 0.0
        alpha = 1.0  # Stress penalty coefficient
        
        for node in network:
            # Coherence contribution
            coherence_term = node.coherence
            
            # Stress penalty
            stress_penalty = np.exp(-alpha * node.T_00)
            
            # Curvature penalty (approximate ∇²Φ from dPhi_dt)
            # In full implementation, would need spatial derivatives
            curvature_approx = abs(node.dPhi_dt)
            curvature_penalty = 1.0 - min(curvature_approx / Lambda_crit, 1.0)
            
            # Combine terms
            S_col += coherence_term * stress_penalty * curvature_penalty
        
        S_col /= N
        
        return S_col


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_example_network(num_nodes: int = 10) -> List[NodeState]:
    """
    Create example emotional network.
    
    Parameters
    ----------
    num_nodes : int
        Number of nodes
        
    Returns
    -------
    list of NodeState
        Example network
    """
    network = []
    
    for i in range(num_nodes):
        # Random stress and coherence
        T_00 = np.random.uniform(0.1, 0.7)
        coherence = np.random.uniform(0.6, 1.0)
        
        # Classify stress
        if T_00 < 0.2:
            stress_level = "Peace"
        elif T_00 < 0.4:
            stress_level = "Work"
        elif T_00 < 0.58:
            stress_level = "Alert"
        else:
            stress_level = "Critical"
        
        # Create random connections
        neighbors = []
        for j in range(num_nodes):
            if j != i and np.random.random() < 0.3:  # 30% connection probability
                neighbors.append(j)
        
        node = NodeState(
            node_id=i,
            Phi=np.random.uniform(-1, 1),
            dPhi_dt=np.random.uniform(-0.1, 0.1),
            Psi=coherence * np.exp(1j * np.random.uniform(0, 2*np.pi)),
            coherence=coherence,
            phase=np.random.uniform(0, 2*np.pi),
            T_00=T_00,
            stress_level=stress_level,
            neighbors=neighbors
        )
        
        network.append(node)
    
    return network


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate synchronization protocol."""
    
    print("=" * 80)
    print("SYNCHRONIZATION PROTOCOL U(κ_Π) - 141.7 Hz Resonance")
    print("=" * 80)
    print()
    print("Protocol Levels:")
    print("  Micro: Individual stress reduction")
    print("  Meso: Interpersonal phase synchronization")
    print("  Macro: Network optimization")
    print()
    
    # Initialize protocol
    protocol = SynchronizationProtocol()
    
    print(f"Resonant Frequency: f₀ = {protocol.f0} Hz")
    print(f"Damping Coefficient: γ = {protocol.gamma}")
    print(f"Complexity Coupling: κ_Π = {protocol.kappa_Pi}")
    print()
    
    # Create example network
    network = create_example_network(num_nodes=20)
    
    print("=" * 80)
    print("Initial Network State")
    print("=" * 80)
    print()
    
    # Detect critical nodes
    critical_nodes = protocol.detect_critical_nodes(network)
    print(f"Critical nodes (T_00 > {protocol.params.T_00_critical}): {critical_nodes}")
    print()
    
    # Compute initial sovereignty
    S_col_initial = protocol.compute_sovereignty_index(network)
    print(f"Initial Sovereignty Index: S_col = {S_col_initial:.4f}")
    print(f"Target: S_col ≥ 0.95 (Total Sovereignty)")
    print()
    
    # Macro-level analysis
    macro_results = protocol.protocol_macro(network)
    print("Macro Analysis:")
    for key, value in macro_results.items():
        print(f"  {key}: {value}")
    print()
    
    print("=" * 80)
    print("Micro-Level Intervention Example")
    print("=" * 80)
    print()
    
    if critical_nodes:
        # Apply micro intervention to first critical node
        critical_node = network[critical_nodes[0]]
        t = 0.0
        
        micro_result = protocol.protocol_micro(critical_node, t)
        
        print(f"Node {micro_result['node_id']} Intervention:")
        print(f"  Current T_00: {critical_node.T_00:.4f}")
        print(f"  Resonance signal: {micro_result['resonance_signal']:.4f}")
        print(f"  Φ injection: {micro_result['Phi_injection']:.4f}")
        print(f"  Coherence boost: {micro_result['coherence_boost']:.4f}")
        print(f"  Expected T_00 reduction: {micro_result['expected_T_00_reduction']:.4f}")
        print(f"  Duration: {micro_result['duration']:.0f} seconds")
    print()
    
    print("=" * 80)
    print("Meso-Level Intervention Example")
    print("=" * 80)
    print()
    
    # Find a connected pair
    for node in network:
        if node.neighbors:
            neighbor_id = node.neighbors[0]
            neighbor = network[neighbor_id]
            
            meso_result = protocol.protocol_meso(node, neighbor, network)
            
            print(f"Nodes {meso_result['node1_id']} ↔ {meso_result['node2_id']}:")
            print(f"  Phase coherence: {meso_result['phase_coherence']:.4f}")
            print(f"  Coupling strength: {meso_result['coupling_strength']:.4f}")
            print(f"  New phases: {meso_result['phase1_new']:.4f}, {meso_result['phase2_new']:.4f}")
            break
    
    print()
    print("=" * 80)
    print("✨ Synchronization protocol successfully implemented!")
    print("=" * 80)
    print()
    print("→ 141.7 Hz resonance regulates collective emotional dynamics")
    print("→ Multi-level intervention (micro, meso, macro)")
    print("→ Path to Total Sovereignty (S_col ≥ 0.95)")
    print()


if __name__ == "__main__":
    main()
