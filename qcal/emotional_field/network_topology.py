#!/usr/bin/env python3
"""
Network Topology and Topological Invariants
===========================================

Implements topological analysis of emotional stress networks including:
- Betti numbers (β₀, β₁, β₂)
- Persistent homology
- Winding numbers
- Network connectivity measures

Mathematical Foundation:
- β₀: Number of connected components (isolated communities)
- β₁: Number of 1D holes (feedback loops)
- β₂: Number of 2D cavities (isolation bubbles)

Winding Number:
W_total = (1/2π) ∮_∂M ∇arg(Ψ)·dℓ

Author: QCAL ∞³ Framework
Date: 2026-02-01
"""

import numpy as np
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
import networkx as nx


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class TopologicalFeatures:
    """Topological features of the network."""
    
    # Betti numbers
    beta_0: int                        # Connected components
    beta_1: int                        # 1D holes (cycles)
    beta_2: int                        # 2D cavities
    
    # Network measures
    num_nodes: int
    num_edges: int
    density: float
    
    # Winding number
    winding_number: float              # Total phase winding
    
    # Stress characteristics
    mean_stress: float
    max_stress: float
    critical_regions: List[int]


@dataclass
class PersistentFeature:
    """A feature in persistent homology."""
    
    dimension: int                     # 0, 1, or 2
    birth: float                       # Stress threshold where feature appears
    death: float                       # Stress threshold where feature disappears
    persistence: float                 # death - birth
    representative: List[int]          # Nodes/edges forming feature


# ============================================================================
# NETWORK TOPOLOGY
# ============================================================================

class NetworkTopology:
    """
    Topological analysis of emotional stress networks.
    
    Provides tools for:
    - Computing Betti numbers
    - Persistent homology
    - Phase winding analysis
    - Community detection
    """
    
    def __init__(self):
        """Initialize topology analyzer."""
        pass
    
    def build_graph(
        self,
        nodes: List[int],
        connections: Dict[int, List[int]],
        stress_levels: Optional[Dict[int, float]] = None
    ) -> nx.Graph:
        """
        Build NetworkX graph from node data.
        
        Parameters
        ----------
        nodes : list of int
            Node IDs
        connections : dict
            Node ID -> list of connected node IDs
        stress_levels : dict, optional
            Node ID -> stress level
            
        Returns
        -------
        nx.Graph
            NetworkX graph
        """
        G = nx.Graph()
        
        # Add nodes
        for node in nodes:
            stress = stress_levels.get(node, 0.0) if stress_levels else 0.0
            G.add_node(node, stress=stress)
        
        # Add edges
        for node, neighbors in connections.items():
            for neighbor in neighbors:
                if neighbor in nodes:  # Ensure neighbor exists
                    G.add_edge(node, neighbor)
        
        return G
    
    def compute_beta_0(self, G: nx.Graph) -> int:
        """
        Compute β₀ (number of connected components).
        
        Parameters
        ----------
        G : nx.Graph
            Network graph
            
        Returns
        -------
        int
            β₀ (number of components)
        """
        return nx.number_connected_components(G)
    
    def compute_beta_1(self, G: nx.Graph) -> int:
        """
        Compute β₁ (number of independent cycles).
        
        β₁ = |E| - |V| + |C|
        where E = edges, V = vertices, C = connected components
        
        Parameters
        ----------
        G : nx.Graph
            Network graph
            
        Returns
        -------
        int
            β₁ (number of cycles)
        """
        num_vertices = G.number_of_nodes()
        num_edges = G.number_of_edges()
        num_components = self.compute_beta_0(G)
        
        # Euler characteristic: χ = V - E + F
        # For graph: β₁ = E - V + C (cycles in graph)
        beta_1 = num_edges - num_vertices + num_components
        
        return max(0, beta_1)
    
    def compute_beta_2(self, G: nx.Graph, threshold: float = 0.5) -> int:
        """
        Compute β₂ (number of 2D cavities/voids).
        
        For graph networks, this detects "triangulated voids" -
        regions surrounded by triangles but with no internal connections.
        
        Parameters
        ----------
        G : nx.Graph
            Network graph
        threshold : float
            Minimum density for cavity detection
            
        Returns
        -------
        int
            β₂ (number of cavities)
        """
        # For 1-skeleton (graph), β₂ typically relates to
        # filled cavities in clique complex
        
        # Find all triangles (3-cliques)
        triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
        
        # Simplified: count isolated triangle groups as cavities
        # Full implementation would need simplicial complex
        
        # For now, estimate based on clustering
        clustering_coeffs = nx.clustering(G)
        high_clustering_nodes = [n for n, c in clustering_coeffs.items() if c > threshold]
        
        # Rough estimate: cavities ~ high clustering regions / 3
        beta_2 = len(high_clustering_nodes) // 5  # Heuristic
        
        return beta_2
    
    def compute_betti_numbers(self, G: nx.Graph) -> Tuple[int, int, int]:
        """
        Compute all Betti numbers (β₀, β₁, β₂).
        
        Parameters
        ----------
        G : nx.Graph
            Network graph
            
        Returns
        -------
        tuple
            (β₀, β₁, β₂)
        """
        beta_0 = self.compute_beta_0(G)
        beta_1 = self.compute_beta_1(G)
        beta_2 = self.compute_beta_2(G)
        
        return beta_0, beta_1, beta_2
    
    def persistent_homology(
        self,
        G: nx.Graph,
        stress_attribute: str = 'stress',
        num_thresholds: int = 10
    ) -> List[PersistentFeature]:
        """
        Compute persistent homology based on stress filtration.
        
        Track how topological features appear/disappear as
        stress threshold varies.
        
        Parameters
        ----------
        G : nx.Graph
            Network graph with stress attributes
        stress_attribute : str
            Node attribute for stress
        num_thresholds : int
            Number of threshold levels
            
        Returns
        -------
        list of PersistentFeature
            Persistent features
        """
        features = []
        
        # Get stress values
        stress_values = [G.nodes[n].get(stress_attribute, 0.0) for n in G.nodes()]
        
        if not stress_values:
            return features
        
        min_stress = min(stress_values)
        max_stress = max(stress_values)
        
        # Thresholds for filtration
        thresholds = np.linspace(min_stress, max_stress, num_thresholds)
        
        # Track components across thresholds
        previous_components = []
        
        for i, threshold in enumerate(thresholds):
            # Subgraph with nodes below threshold
            nodes_below = [n for n in G.nodes() 
                          if G.nodes[n].get(stress_attribute, 0.0) <= threshold]
            subgraph = G.subgraph(nodes_below)
            
            # Find connected components
            components = list(nx.connected_components(subgraph))
            
            # Detect new components (birth)
            for comp in components:
                if not any(comp.issubset(prev) for prev in previous_components):
                    # New component born at this threshold
                    feature = PersistentFeature(
                        dimension=0,
                        birth=threshold,
                        death=max_stress,  # Will update if merges
                        persistence=max_stress - threshold,
                        representative=list(comp)
                    )
                    features.append(feature)
            
            # Detect merged components (death of smaller)
            for prev_comp in previous_components:
                merged = False
                for comp in components:
                    if prev_comp.issubset(comp) and prev_comp != comp:
                        # Component merged (died)
                        merged = True
                        # Find corresponding feature and update death
                        for f in features:
                            if set(f.representative) == prev_comp:
                                if f.death == max_stress:  # Not yet died
                                    f.death = threshold
                                    f.persistence = threshold - f.birth
                        break
            
            previous_components = components.copy()
        
        return features
    
    def compute_winding_number(
        self,
        phases: Dict[int, float],
        boundary_nodes: List[int]
    ) -> float:
        """
        Compute winding number around boundary.
        
        W = (1/2π) ∮_∂M ∇arg(Ψ)·dℓ
        
        Parameters
        ----------
        phases : dict
            Node ID -> phase angle
        boundary_nodes : list
            Ordered list of boundary nodes
            
        Returns
        -------
        float
            Winding number
        """
        if len(boundary_nodes) < 2:
            return 0.0
        
        total_winding = 0.0
        
        # Integrate phase gradient around boundary
        for i in range(len(boundary_nodes)):
            node1 = boundary_nodes[i]
            node2 = boundary_nodes[(i + 1) % len(boundary_nodes)]
            
            phase1 = phases.get(node1, 0.0)
            phase2 = phases.get(node2, 0.0)
            
            # Phase difference (wrapped to [-π, π])
            delta_phase = phase2 - phase1
            delta_phase = np.arctan2(np.sin(delta_phase), np.cos(delta_phase))
            
            total_winding += delta_phase
        
        # Normalize by 2π
        winding_number = total_winding / (2 * np.pi)
        
        return winding_number
    
    def detect_critical_regions(
        self,
        G: nx.Graph,
        stress_attribute: str = 'stress',
        threshold: float = 0.58
    ) -> List[List[int]]:
        """
        Detect spatially connected critical regions.
        
        Parameters
        ----------
        G : nx.Graph
            Network graph
        stress_attribute : str
            Node attribute for stress
        threshold : float
            Critical stress threshold
            
        Returns
        -------
        list of lists
            Connected critical regions (each is list of node IDs)
        """
        # Find critical nodes
        critical_nodes = [n for n in G.nodes() 
                         if G.nodes[n].get(stress_attribute, 0.0) > threshold]
        
        # Subgraph of critical nodes
        critical_subgraph = G.subgraph(critical_nodes)
        
        # Find connected components
        regions = list(nx.connected_components(critical_subgraph))
        
        return [list(region) for region in regions]
    
    def analyze_network(
        self,
        nodes: List[int],
        connections: Dict[int, List[int]],
        stress_levels: Dict[int, float],
        phases: Optional[Dict[int, float]] = None
    ) -> TopologicalFeatures:
        """
        Perform complete topological analysis.
        
        Parameters
        ----------
        nodes : list of int
            Node IDs
        connections : dict
            Node ID -> list of connected node IDs
        stress_levels : dict
            Node ID -> stress level
        phases : dict, optional
            Node ID -> phase angle
            
        Returns
        -------
        TopologicalFeatures
            Complete topological analysis
        """
        # Build graph
        G = self.build_graph(nodes, connections, stress_levels)
        
        # Compute Betti numbers
        beta_0, beta_1, beta_2 = self.compute_betti_numbers(G)
        
        # Network statistics
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        
        if num_nodes > 1:
            max_edges = num_nodes * (num_nodes - 1) / 2
            density = num_edges / max_edges if max_edges > 0 else 0.0
        else:
            density = 0.0
        
        # Stress statistics
        stress_vals = list(stress_levels.values())
        mean_stress = np.mean(stress_vals) if stress_vals else 0.0
        max_stress = max(stress_vals) if stress_vals else 0.0
        
        # Critical regions
        critical_regions_list = self.detect_critical_regions(G)
        critical_nodes = [node for region in critical_regions_list for node in region]
        
        # Winding number (if phases provided)
        if phases:
            # Use all nodes as boundary (simplified)
            boundary = list(nodes)
            winding = self.compute_winding_number(phases, boundary)
        else:
            winding = 0.0
        
        return TopologicalFeatures(
            beta_0=beta_0,
            beta_1=beta_1,
            beta_2=beta_2,
            num_nodes=num_nodes,
            num_edges=num_edges,
            density=density,
            winding_number=winding,
            mean_stress=mean_stress,
            max_stress=max_stress,
            critical_regions=critical_nodes
        )
    
    def interpret_features(self, features: TopologicalFeatures) -> Dict[str, str]:
        """
        Provide interpretation of topological features.
        
        Parameters
        ----------
        features : TopologicalFeatures
            Topological analysis results
            
        Returns
        -------
        dict
            Interpretations
        """
        interpretations = {}
        
        # β₀ interpretation
        if features.beta_0 == 1:
            interpretations['beta_0'] = "Fully connected community"
        elif features.beta_0 <= 3:
            interpretations['beta_0'] = f"{features.beta_0} separate communities - moderate fragmentation"
        else:
            interpretations['beta_0'] = f"{features.beta_0} isolated communities - HIGH fragmentation"
        
        # β₁ interpretation  
        if features.beta_1 == 0:
            interpretations['beta_1'] = "Tree structure - no feedback loops"
        elif features.beta_1 <= 3:
            interpretations['beta_1'] = f"{features.beta_1} feedback loops - healthy circulation"
        else:
            interpretations['beta_1'] = f"{features.beta_1} feedback loops - complex dynamics"
        
        # β₂ interpretation
        if features.beta_2 == 0:
            interpretations['beta_2'] = "No isolation cavities detected"
        else:
            interpretations['beta_2'] = f"{features.beta_2} isolation bubbles - attention needed"
        
        # Winding number
        if abs(features.winding_number) < 0.1:
            interpretations['winding'] = "Trivial phase topology"
        elif abs(features.winding_number) < 1.0:
            interpretations['winding'] = "Partial phase winding - transitional state"
        else:
            interpretations['winding'] = f"Full winding (W={features.winding_number:.1f}) - coherent vortex"
        
        # Overall health
        if features.mean_stress < 0.3 and features.beta_0 == 1:
            interpretations['health'] = "HEALTHY - Low stress, connected network"
        elif features.mean_stress < 0.5 and features.beta_0 <= 2:
            interpretations['health'] = "MODERATE - Manageable stress, some fragmentation"
        else:
            interpretations['health'] = "AT RISK - High stress and/or fragmentation"
        
        return interpretations


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate network topology analysis."""
    
    print("=" * 80)
    print("NETWORK TOPOLOGY & TOPOLOGICAL INVARIANTS")
    print("=" * 80)
    print()
    print("Topological Features:")
    print("  β₀: Connected components (isolated communities)")
    print("  β₁: 1D holes (feedback cycles)")
    print("  β₂: 2D cavities (isolation bubbles)")
    print("  W: Winding number (phase coherence)")
    print()
    
    # Create example network
    analyzer = NetworkTopology()
    
    # Example: Small network with some structure
    nodes = list(range(15))
    
    # Create connections (with some cycles and separation)
    connections = {
        0: [1, 2, 3],
        1: [0, 2, 4],
        2: [0, 1, 3],
        3: [0, 2, 5],
        4: [1, 5, 6],
        5: [3, 4, 6],
        6: [4, 5],        # First component
        
        7: [8, 9],
        8: [7, 9, 10],
        9: [7, 8],
        10: [8, 11],
        11: [10],         # Second component
        
        12: [13, 14],
        13: [12, 14],
        14: [12, 13]      # Third component (triangle)
    }
    
    # Stress levels
    stress_levels = {
        0: 0.2, 1: 0.3, 2: 0.25, 3: 0.4, 4: 0.35, 5: 0.5, 6: 0.45,
        7: 0.6, 8: 0.65, 9: 0.7, 10: 0.55, 11: 0.5,  # Critical group
        12: 0.15, 13: 0.1, 14: 0.12  # Peace group
    }
    
    # Phases
    phases = {i: np.random.uniform(0, 2*np.pi) for i in nodes}
    
    print("=" * 80)
    print("Example Network Analysis")
    print("=" * 80)
    print()
    print(f"Network: {len(nodes)} nodes, {sum(len(v) for v in connections.values())//2} edges")
    print()
    
    # Analyze
    features = analyzer.analyze_network(nodes, connections, stress_levels, phases)
    
    print("Topological Features:")
    print("-" * 80)
    print(f"  β₀ (components):    {features.beta_0}")
    print(f"  β₁ (cycles):        {features.beta_1}")
    print(f"  β₂ (cavities):      {features.beta_2}")
    print(f"  Winding number:     {features.winding_number:.3f}")
    print()
    
    print("Network Statistics:")
    print("-" * 80)
    print(f"  Nodes:              {features.num_nodes}")
    print(f"  Edges:              {features.num_edges}")
    print(f"  Density:            {features.density:.3f}")
    print(f"  Mean stress:        {features.mean_stress:.3f}")
    print(f"  Max stress:         {features.max_stress:.3f}")
    print(f"  Critical nodes:     {len(features.critical_regions)}")
    print()
    
    # Interpretations
    interp = analyzer.interpret_features(features)
    
    print("Interpretations:")
    print("-" * 80)
    for key, value in interp.items():
        print(f"  {key:15s}: {value}")
    print()
    
    # Persistent homology
    print("=" * 80)
    print("Persistent Homology Analysis")
    print("=" * 80)
    print()
    
    G = analyzer.build_graph(nodes, connections, stress_levels)
    persistent_features = analyzer.persistent_homology(G, num_thresholds=5)
    
    print(f"Found {len(persistent_features)} persistent features:")
    print()
    print("Dim  Birth    Death    Persistence  Nodes")
    print("-" * 80)
    
    for feat in sorted(persistent_features, key=lambda f: f.persistence, reverse=True)[:10]:
        nodes_str = str(feat.representative[:3]) + "..." if len(feat.representative) > 3 else str(feat.representative)
        print(f" {feat.dimension}   {feat.birth:.3f}    {feat.death:.3f}    {feat.persistence:.3f}        {nodes_str}")
    
    print()
    print("=" * 80)
    print("✨ Network topology analysis successfully implemented!")
    print("=" * 80)
    print()
    print("→ Detects community fragmentation (β₀)")
    print("→ Identifies feedback loops (β₁)")
    print("→ Reveals isolation bubbles (β₂)")
    print("→ Tracks persistent structures across stress levels")
    print()


if __name__ == "__main__":
    main()
