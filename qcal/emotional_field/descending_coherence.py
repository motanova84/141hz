#!/usr/bin/env python3
"""
Descending Coherence Propagator
================================

Implements the hierarchical cascade mechanism where collective coherence
at macro level influences meso and micro levels through downward causation.

Mathematical Foundation:
-----------------------
Coherence exists at three hierarchical levels:
1. Macro (Collective): Ψ_col = (1/N) Σᵢ Ψᵢ
2. Meso (Groups): Ψ_group_j = (1/n_j) Σᵢ∈G_j Ψᵢ  
3. Micro (Individual): Ψᵢ

Descending Coherence Equations:
-------------------------------
∂Ψᵢ/∂t = -γᵢ(Ψᵢ - Ψ_target) + ηᵢ·sin(2πf₀t)

Where Ψ_target cascades from macro → meso → micro:

Ψ_target(i) = α_macro·Ψ_col + α_meso·Ψ_group(i) + α_micro·Ψᵢ(local)

Coupling Coefficients:
--------------------
- α_macro: Strength of collective field influence (0.3-0.5)
- α_meso: Strength of group field influence (0.3-0.4)  
- α_micro: Individual autonomy (0.2-0.4)
- Normalization: α_macro + α_meso + α_micro = 1.0

Constraints: α_macro + α_meso + α_micro = 1.0

Downward Causation Mechanism:
---------------------------
Higher-level coherence creates an "attractor field" that biases
lower-level dynamics without removing individual agency.

T_μν constraint: Collective stress states (T_00^col) influence
individual stress tolerance via modified potential:

V_eff(Φᵢ) = V(Φᵢ) - β·T_00^col·Φᵢ²

This creates a "coherence pressure" from collective to individual.

Author: QCAL ∞³ Framework
Date: 2026-02-13
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import sys
import os

# Add parent paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from qcal.constants import F_0_VALUE
    F_0 = F_0_VALUE
except ImportError:
    F_0 = 141.7001  # Hz


# ============================================================================
# HIERARCHICAL LEVEL DEFINITIONS
# ============================================================================

class CoherenceLevel(Enum):
    """Hierarchical levels of coherence."""
    MICRO = "individual"      # Single node/observer
    MESO = "group"           # Small communities (5-50 nodes)
    MACRO = "collective"     # Global network (all nodes)


# ============================================================================
# DESCENDING COHERENCE PARAMETERS
# ============================================================================

@dataclass
class DescendingCoherenceParameters:
    """Parameters for descending coherence cascade."""
    
    # Fundamental frequency
    f0: float = F_0
    omega_0: float = 2 * np.pi * F_0
    
    # Coupling coefficients (must sum to 1.0)
    alpha_macro: float = 0.4    # Collective influence
    alpha_meso: float = 0.35    # Group influence  
    alpha_micro: float = 0.25   # Individual autonomy
    
    # Damping coefficients
    gamma_individual: float = 0.5     # Individual relaxation rate
    gamma_group: float = 0.3          # Group relaxation rate
    gamma_collective: float = 0.1     # Collective relaxation rate
    
    # Resonance amplitudes
    eta_individual: float = 0.1       # Individual resonance strength
    eta_group: float = 0.15           # Group resonance strength
    eta_collective: float = 0.2       # Collective resonance strength
    
    # Downward causation strength
    beta_pressure: float = 0.2        # Coherence pressure coefficient
    
    # Stress-coherence coupling
    stress_coherence_coupling: float = 0.3
    
    # Group detection parameters
    min_group_size: int = 5
    max_group_size: int = 50
    
    def validate(self):
        """Validate that coupling coefficients sum to 1.0."""
        total = self.alpha_macro + self.alpha_meso + self.alpha_micro
        if not np.isclose(total, 1.0, atol=1e-6):
            raise ValueError(
                f"Coupling coefficients must sum to 1.0, got {total:.6f}"
            )


# ============================================================================
# GROUP STRUCTURE
# ============================================================================

@dataclass
class CoherenceGroup:
    """A meso-level group within the network."""
    
    group_id: int
    member_ids: Set[int] = field(default_factory=set)
    coherence: complex = 0.0 + 0.0j
    phase: float = 0.0
    stress_level: float = 0.0
    
    def add_member(self, node_id: int):
        """Add a node to this group."""
        self.member_ids.add(node_id)
    
    def size(self) -> int:
        """Return number of members."""
        return len(self.member_ids)
    
    def compute_coherence(self, node_coherences: Dict[int, complex]) -> complex:
        """Compute group coherence as average of member coherences."""
        if not self.member_ids:
            return 0.0 + 0.0j
        
        total = sum(node_coherences.get(nid, 0.0+0.0j) for nid in self.member_ids)
        self.coherence = total / len(self.member_ids)
        self.phase = np.angle(self.coherence)
        return self.coherence


# ============================================================================
# NODE STATE WITH HIERARCHY
# ============================================================================

@dataclass
class HierarchicalNodeState:
    """Node state with hierarchical coherence information."""
    
    # Node identifier
    node_id: int
    
    # Micro-level (individual)
    Psi_individual: complex          # Individual coherence field
    coherence_micro: float           # |Ψ_individual|
    phase_micro: float               # arg(Ψ_individual)
    
    # Meso-level (group membership)
    group_id: Optional[int] = None   # Which group this node belongs to
    Psi_group: complex = 0.0 + 0.0j  # Group coherence
    coherence_meso: float = 0.0      # |Ψ_group|
    phase_meso: float = 0.0          # arg(Ψ_group)
    
    # Macro-level (collective)
    Psi_collective: complex = 0.0 + 0.0j  # Global coherence
    coherence_macro: float = 0.0          # |Ψ_collective|
    phase_macro: float = 0.0              # arg(Ψ_collective)
    
    # Target coherence (from cascade)
    Psi_target: complex = 0.0 + 0.0j
    
    # Stress information
    T_00: float = 0.0                # Individual stress
    T_00_group: float = 0.0          # Group stress
    T_00_collective: float = 0.0     # Collective stress
    
    # Network properties
    neighbors: List[int] = field(default_factory=list)


# ============================================================================
# DESCENDING COHERENCE PROPAGATOR
# ============================================================================

class DescendingCoherencePropagator:
    """
    Implements the hierarchical coherence cascade mechanism.
    
    This class manages the flow of coherence from collective (macro) level
    down through group (meso) level to individual (micro) level.
    """
    
    def __init__(self, params: Optional[DescendingCoherenceParameters] = None):
        """
        Initialize the propagator.
        
        Args:
            params: Descending coherence parameters. If None, uses defaults.
        """
        self.params = params or DescendingCoherenceParameters()
        self.params.validate()
        
        self.groups: Dict[int, CoherenceGroup] = {}
        self.node_states: Dict[int, HierarchicalNodeState] = {}
        
        self.collective_coherence: complex = 0.0 + 0.0j
        self.collective_stress: float = 0.0
        
        self.time: float = 0.0
    
    def detect_groups(
        self, 
        node_ids: List[int],
        connections: Dict[int, List[int]],
        stress_levels: Dict[int, float]
    ) -> Dict[int, CoherenceGroup]:
        """
        Detect meso-level groups using community detection.
        
        Simple implementation: groups are connected components with size
        constraints. In production, use more sophisticated methods like
        Louvain or spectral clustering.
        
        Args:
            node_ids: List of all node IDs
            connections: Adjacency list {node_id: [neighbor_ids]}
            stress_levels: Stress at each node {node_id: T_00}
        
        Returns:
            Dictionary of {group_id: CoherenceGroup}
        """
        visited = set()
        groups = {}
        group_id = 0
        
        def dfs_component(start_node: int, current_group: Set[int]):
            """Depth-first search to find connected component."""
            stack = [start_node]
            
            while stack and len(current_group) < self.params.max_group_size:
                node = stack.pop()
                if node in visited:
                    continue
                
                visited.add(node)
                current_group.add(node)
                
                # Add unvisited neighbors
                for neighbor in connections.get(node, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        # Find connected components
        for node_id in node_ids:
            if node_id in visited:
                continue
            
            component = set()
            dfs_component(node_id, component)
            
            # Only create groups of valid size
            if self.params.min_group_size <= len(component) <= self.params.max_group_size:
                group = CoherenceGroup(group_id=group_id, member_ids=component)
                groups[group_id] = group
                group_id += 1
            elif len(component) > self.params.max_group_size:
                # Split large components into multiple groups
                members = list(component)
                for i in range(0, len(members), self.params.max_group_size):
                    chunk = set(members[i:i + self.params.max_group_size])
                    if len(chunk) >= self.params.min_group_size:
                        group = CoherenceGroup(group_id=group_id, member_ids=chunk)
                        groups[group_id] = group
                        group_id += 1
        
        self.groups = groups
        return groups
    
    def compute_collective_coherence(
        self,
        node_coherences: Dict[int, complex]
    ) -> complex:
        """
        Compute macro-level collective coherence.
        
        Args:
            node_coherences: Individual coherences {node_id: Ψᵢ}
        
        Returns:
            Collective coherence Ψ_col
        """
        if not node_coherences:
            self.collective_coherence = 0.0 + 0.0j
            return self.collective_coherence
        
        total = sum(node_coherences.values())
        self.collective_coherence = total / len(node_coherences)
        return self.collective_coherence
    
    def compute_group_coherences(
        self,
        node_coherences: Dict[int, complex]
    ) -> Dict[int, complex]:
        """
        Compute meso-level group coherences.
        
        Args:
            node_coherences: Individual coherences {node_id: Ψᵢ}
        
        Returns:
            Group coherences {group_id: Ψ_group}
        """
        group_coherences = {}
        
        for group_id, group in self.groups.items():
            coherence = group.compute_coherence(node_coherences)
            group_coherences[group_id] = coherence
        
        return group_coherences
    
    def compute_target_coherence(
        self,
        node_id: int,
        Psi_individual: complex,
        group_id: Optional[int],
        Psi_group: complex,
        Psi_collective: complex
    ) -> complex:
        """
        Compute target coherence for a node via descending cascade.
        
        Ψ_target = α_macro·Ψ_col + α_meso·Ψ_group + α_micro·Ψᵢ
        
        Args:
            node_id: Node identifier
            Psi_individual: Individual coherence Ψᵢ
            group_id: Group membership (None if ungrouped)
            Psi_group: Group coherence Ψ_group
            Psi_collective: Collective coherence Ψ_col
        
        Returns:
            Target coherence Ψ_target
        """
        # Macro contribution
        macro_contrib = self.params.alpha_macro * Psi_collective
        
        # Meso contribution (if node is in a group)
        if group_id is not None and group_id in self.groups:
            meso_contrib = self.params.alpha_meso * Psi_group
        else:
            # No group: redistribute meso weight to macro and micro
            macro_contrib *= (1.0 + self.params.alpha_meso / 2)
            meso_contrib = 0.0
        
        # Micro contribution (individual autonomy)
        micro_contrib = self.params.alpha_micro * Psi_individual
        
        # Total target
        Psi_target = macro_contrib + meso_contrib + micro_contrib
        
        return Psi_target
    
    def propagate_coherence(
        self,
        node_coherences: Dict[int, complex],
        stress_levels: Dict[int, float],
        dt: float
    ) -> Dict[int, complex]:
        """
        Propagate coherence for one time step via descending cascade.
        
        Dynamics:
        dΨᵢ/dt = -γᵢ(Ψᵢ - Ψ_target) + ηᵢ·sin(2πf₀t)·exp(iφᵢ)
        
        Args:
            node_coherences: Current individual coherences {node_id: Ψᵢ}
            stress_levels: Current stress levels {node_id: T_00}
            dt: Time step (seconds)
        
        Returns:
            Updated coherences {node_id: Ψᵢ(t+dt)}
        """
        # Compute collective coherence (macro)
        Psi_col = self.compute_collective_coherence(node_coherences)
        
        # Compute group coherences (meso)
        group_coherences = self.compute_group_coherences(node_coherences)
        
        # Compute collective stress
        self.collective_stress = np.mean(list(stress_levels.values())) if stress_levels else 0.0
        
        # Update each node
        updated_coherences = {}
        
        for node_id, Psi_i in node_coherences.items():
            # Get node's group
            group_id = None
            Psi_group = 0.0 + 0.0j
            for gid, group in self.groups.items():
                if node_id in group.member_ids:
                    group_id = gid
                    Psi_group = group_coherences.get(gid, 0.0+0.0j)
                    break
            
            # Compute target coherence via cascade
            Psi_target = self.compute_target_coherence(
                node_id, Psi_i, group_id, Psi_group, Psi_col
            )
            
            # Relaxation dynamics: dΨ/dt = -γ(Ψ - Ψ_target)
            T_00 = stress_levels.get(node_id, 0.0)
            
            # Stress modulates relaxation rate (higher stress → slower relaxation)
            gamma_eff = self.params.gamma_individual * (1.0 - self.params.stress_coherence_coupling * T_00)
            gamma_eff = max(0.01, gamma_eff)  # Prevent negative/zero
            
            # Resonance drive at f₀
            resonance_drive = self.params.eta_individual * np.sin(2 * np.pi * self.params.f0 * self.time)
            phase_i = np.angle(Psi_i) if abs(Psi_i) > 1e-10 else 0.0
            resonance_contrib = resonance_drive * np.exp(1j * phase_i)
            
            # Update equation
            dPsi_dt = -gamma_eff * (Psi_i - Psi_target) + resonance_contrib
            Psi_new = Psi_i + dPsi_dt * dt
            
            updated_coherences[node_id] = Psi_new
            
            # Update node state
            if node_id not in self.node_states:
                self.node_states[node_id] = HierarchicalNodeState(
                    node_id=node_id,
                    Psi_individual=Psi_new,
                    coherence_micro=abs(Psi_new),
                    phase_micro=np.angle(Psi_new)
                )
            else:
                state = self.node_states[node_id]
                state.Psi_individual = Psi_new
                state.coherence_micro = abs(Psi_new)
                state.phase_micro = np.angle(Psi_new)
                state.group_id = group_id
                state.Psi_group = Psi_group
                state.coherence_meso = abs(Psi_group)
                state.phase_meso = np.angle(Psi_group)
                state.Psi_collective = Psi_col
                state.coherence_macro = abs(Psi_col)
                state.phase_macro = np.angle(Psi_col)
                state.Psi_target = Psi_target
                state.T_00 = T_00
                state.T_00_collective = self.collective_stress
        
        # Advance time
        self.time += dt
        
        return updated_coherences
    
    def get_hierarchy_info(self, node_id: int) -> Dict[str, any]:
        """
        Get hierarchical coherence information for a specific node.
        
        Args:
            node_id: Node identifier
        
        Returns:
            Dictionary with micro/meso/macro coherence info
        """
        if node_id not in self.node_states:
            return {
                "node_id": node_id,
                "error": "Node state not found"
            }
        
        state = self.node_states[node_id]
        
        return {
            "node_id": node_id,
            "micro": {
                "coherence": state.coherence_micro,
                "phase": state.phase_micro,
                "Psi": state.Psi_individual
            },
            "meso": {
                "group_id": state.group_id,
                "coherence": state.coherence_meso,
                "phase": state.phase_meso,
                "Psi": state.Psi_group
            },
            "macro": {
                "coherence": state.coherence_macro,
                "phase": state.phase_macro,
                "Psi": state.Psi_collective
            },
            "target": {
                "Psi": state.Psi_target,
                "coherence": abs(state.Psi_target)
            },
            "stress": {
                "individual": state.T_00,
                "collective": state.T_00_collective
            }
        }
    
    def compute_coherence_alignment(self) -> Dict[str, float]:
        """
        Compute how well individual coherences align with targets.
        
        Returns:
            Dictionary with alignment metrics
        """
        if not self.node_states:
            return {
                "mean_alignment": 0.0,
                "std_alignment": 0.0,
                "min_alignment": 0.0,
                "max_alignment": 0.0
            }
        
        alignments = []
        for state in self.node_states.values():
            # Alignment = |Ψᵢ · Ψ_target*| / (|Ψᵢ| |Ψ_target|)
            if abs(state.Psi_individual) > 1e-10 and abs(state.Psi_target) > 1e-10:
                dot_product = np.real(state.Psi_individual * np.conj(state.Psi_target))
                norm_product = abs(state.Psi_individual) * abs(state.Psi_target)
                alignment = dot_product / norm_product
                alignments.append(alignment)
        
        if not alignments:
            return {
                "mean_alignment": 0.0,
                "std_alignment": 0.0,
                "min_alignment": 0.0,
                "max_alignment": 0.0
            }
        
        return {
            "mean_alignment": float(np.mean(alignments)),
            "std_alignment": float(np.std(alignments)),
            "min_alignment": float(np.min(alignments)),
            "max_alignment": float(np.max(alignments))
        }
    
    def get_summary(self) -> Dict[str, any]:
        """
        Get summary of current cascade state.
        
        Returns:
            Dictionary with summary information
        """
        return {
            "time": self.time,
            "num_nodes": len(self.node_states),
            "num_groups": len(self.groups),
            "collective_coherence": abs(self.collective_coherence),
            "collective_phase": np.angle(self.collective_coherence),
            "collective_stress": self.collective_stress,
            "alignment_metrics": self.compute_coherence_alignment(),
            "parameters": {
                "alpha_macro": self.params.alpha_macro,
                "alpha_meso": self.params.alpha_meso,
                "alpha_micro": self.params.alpha_micro,
                "f0": self.params.f0
            }
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_example_cascade(
    num_nodes: int = 50,
    num_groups: int = 5,
    initial_coherence: float = 0.5
) -> Tuple[DescendingCoherencePropagator, Dict[int, complex], Dict[int, List[int]]]:
    """
    Create an example hierarchical network for testing.
    
    Args:
        num_nodes: Total number of nodes
        num_groups: Number of groups to create
        initial_coherence: Initial coherence magnitude
    
    Returns:
        Tuple of (propagator, initial_coherences, connections)
    """
    propagator = DescendingCoherencePropagator()
    
    # Create initial coherences with random phases
    coherences = {}
    for i in range(num_nodes):
        phase = np.random.uniform(0, 2*np.pi)
        coherences[i] = initial_coherence * np.exp(1j * phase)
    
    # Create group structure (ring of groups)
    nodes_per_group = num_nodes // num_groups
    connections = {}
    
    for i in range(num_nodes):
        neighbors = []
        group_id = i // nodes_per_group
        
        # Connect within group
        group_start = group_id * nodes_per_group
        group_end = min(group_start + nodes_per_group, num_nodes)
        
        for j in range(group_start, group_end):
            if j != i and abs(j - i) <= 3:  # Local connections
                neighbors.append(j)
        
        # Connect to next group
        if (i + 1) % nodes_per_group == 0 and i + 1 < num_nodes:
            neighbors.append(i + 1)
        
        connections[i] = neighbors
    
    return propagator, coherences, connections


if __name__ == "__main__":
    """Demonstration of descending coherence cascade."""
    
    print("=" * 70)
    print("QCAL ∞³ Descending Coherence Propagator")
    print("=" * 70)
    print()
    
    # Create example network
    print("Creating hierarchical network...")
    propagator, coherences, connections = create_example_cascade(
        num_nodes=50,
        num_groups=5,
        initial_coherence=0.5
    )
    
    # Detect groups
    stress_levels = {i: 0.3 + 0.2 * np.random.random() for i in range(50)}
    groups = propagator.detect_groups(
        list(range(50)),
        connections,
        stress_levels
    )
    
    print(f"✓ Detected {len(groups)} groups")
    print()
    
    # Simulate cascade evolution
    print("Simulating coherence cascade...")
    dt = 0.01  # 10 ms time steps
    num_steps = 100
    
    for step in range(num_steps):
        coherences = propagator.propagate_coherence(coherences, stress_levels, dt)
        
        if step % 20 == 0:
            summary = propagator.get_summary()
            alignment = summary["alignment_metrics"]["mean_alignment"]
            coh_col = summary["collective_coherence"]
            print(f"  Step {step:3d}: Ψ_col = {coh_col:.4f}, Alignment = {alignment:.4f}")
    
    print()
    
    # Final summary
    print("Final State:")
    print("-" * 70)
    summary = propagator.get_summary()
    print(f"Collective coherence: {summary['collective_coherence']:.4f}")
    print(f"Collective stress: {summary['collective_stress']:.4f}")
    print(f"Number of groups: {summary['num_groups']}")
    print(f"Mean alignment: {summary['alignment_metrics']['mean_alignment']:.4f}")
    print()
    
    # Example node hierarchy
    print("Example Node Hierarchy (Node 0):")
    print("-" * 70)
    info = propagator.get_hierarchy_info(0)
    print(f"Micro (Individual):")
    print(f"  Coherence: {info['micro']['coherence']:.4f}")
    print(f"  Phase: {info['micro']['phase']:.4f} rad")
    print(f"Meso (Group {info['meso']['group_id']}):")
    print(f"  Coherence: {info['meso']['coherence']:.4f}")
    print(f"  Phase: {info['meso']['phase']:.4f} rad")
    print(f"Macro (Collective):")
    print(f"  Coherence: {info['macro']['coherence']:.4f}")
    print(f"  Phase: {info['macro']['phase']:.4f} rad")
    print(f"Target Coherence: {info['target']['coherence']:.4f}")
    print()
    
    print("=" * 70)
    print("✓ Descending coherence cascade demonstration complete")
    print("=" * 70)
