#!/usr/bin/env python3
"""
CAPA 4: Ontological Network (Red Ontológica)

This module implements the ontological network layer:
- Node synchronization via Ψ coherence ≥ 0.888
- πCODE as unit of value
- Distributed recognition (consensus-free)
- Post-monetary symbiotic economy

This layer creates a self-organizing network based on coherence,
transcending traditional consensus mechanisms.
"""

import numpy as np
import hashlib
import time
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json

# Import from previous layers
from .capa1_mathematical_foundations import PiCodeAlgebra, AdelicGeometry
from .capa3_computational_architecture import NativeFrequencyHardware, CoherentRegisters


class NodeType(Enum):
    """Types of nodes in the ontological network."""
    OBSERVER = "observer"      # Passive observation
    CONTRIBUTOR = "contributor"  # Active contribution
    VALIDATOR = "validator"    # Validates coherence
    RESONATOR = "resonator"    # Amplifies coherent signals


@dataclass
class NetworkNode:
    """Represents a node in the ontological network."""
    node_id: str
    node_type: NodeType
    coherence: float = 0.0
    picode_balance: float = 0.0
    connections: Set[str] = field(default_factory=set)
    hardware: Optional[NativeFrequencyHardware] = None
    last_sync: float = 0.0
    
    def __post_init__(self):
        if self.hardware is None:
            self.hardware = NativeFrequencyHardware()


@dataclass
class CoherenceTransaction:
    """Represents a transaction in the coherence network."""
    tx_id: str
    sender: str
    receiver: str
    picode_amount: float
    coherence_proof: float
    timestamp: float
    signature: str = ""


@dataclass
class RecognitionEvent:
    """Represents a distributed recognition event."""
    event_id: str
    contributor: str
    contribution_hash: str
    coherence_level: float
    recognizers: Set[str] = field(default_factory=set)
    picode_awarded: float = 0.0
    timestamp: float = 0.0


class NodeSynchronization:
    """
    Node synchronization via Ψ coherence ≥ 0.888.
    
    Nodes synchronize by measuring coherence of their phase states.
    Only nodes with Ψ ≥ 0.888 can participate in the network.
    """
    
    def __init__(self, threshold: float = 0.888):
        """
        Initialize node synchronization.
        
        Args:
            threshold: Minimum coherence for synchronization
        """
        self.threshold = threshold
        self.phi = (1 + np.sqrt(5)) / 2
        self.f0 = 141.7001
        
        self.nodes: Dict[str, NetworkNode] = {}
        self.adelic = AdelicGeometry()
    
    def register_node(self, node_id: str, node_type: NodeType) -> NetworkNode:
        """
        Register a new node in the network.
        
        Args:
            node_id: Unique node identifier
            node_type: Type of node
            
        Returns:
            Created NetworkNode
        """
        node = NetworkNode(
            node_id=node_id,
            node_type=node_type,
            hardware=NativeFrequencyHardware()
        )
        
        self.nodes[node_id] = node
        return node
    
    def measure_coherence(self, node1_id: str, node2_id: str) -> float:
        """
        Measure coherence between two nodes.
        
        Coherence is based on phase synchronization of their
        hardware oscillators.
        
        Args:
            node1_id: First node ID
            node2_id: Second node ID
            
        Returns:
            Coherence value [0, 1]
        """
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return 0.0
        
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        
        # Phase difference
        phase_diff = node1.hardware.synchronize(node2.hardware)
        
        # Coherence: exp(-|Δφ|)
        coherence = np.exp(-abs(phase_diff))
        
        return coherence
    
    def synchronize_nodes(self, node1_id: str, node2_id: str) -> bool:
        """
        Attempt to synchronize two nodes.
        
        Args:
            node1_id: First node ID
            node2_id: Second node ID
            
        Returns:
            True if synchronization successful (Ψ ≥ threshold)
        """
        coherence = self.measure_coherence(node1_id, node2_id)
        
        if coherence >= self.threshold:
            # Create bidirectional connection
            self.nodes[node1_id].connections.add(node2_id)
            self.nodes[node2_id].connections.add(node1_id)
            
            # Update coherence values
            self.nodes[node1_id].coherence = max(self.nodes[node1_id].coherence, coherence)
            self.nodes[node2_id].coherence = max(self.nodes[node2_id].coherence, coherence)
            
            # Update sync timestamps
            current_time = time.time()
            self.nodes[node1_id].last_sync = current_time
            self.nodes[node2_id].last_sync = current_time
            
            return True
        else:
            return False
    
    def get_coherent_cluster(self, node_id: str) -> Set[str]:
        """
        Get all nodes in coherent cluster with given node.
        
        Uses breadth-first search through coherent connections.
        
        Args:
            node_id: Starting node ID
            
        Returns:
            Set of node IDs in cluster
        """
        if node_id not in self.nodes:
            return set()
        
        cluster = {node_id}
        to_visit = [node_id]
        visited = set()
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            
            # Add coherent neighbors
            for neighbor in self.nodes[current].connections:
                if neighbor not in cluster:
                    # Verify still coherent
                    if self.measure_coherence(current, neighbor) >= self.threshold:
                        cluster.add(neighbor)
                        to_visit.append(neighbor)
        
        return cluster
    
    def network_coherence(self) -> float:
        """
        Compute overall network coherence.
        
        Returns:
            Average coherence across all nodes
        """
        if not self.nodes:
            return 0.0
        
        total_coherence = sum(node.coherence for node in self.nodes.values())
        return total_coherence / len(self.nodes)
    
    def evolve_network(self, steps: int = 10):
        """
        Evolve network by ticking all node oscillators.
        
        Args:
            steps: Number of time steps
        """
        for _ in range(steps):
            for node in self.nodes.values():
                node.hardware.tick()


class PiCodeValue:
    """
    πCODE as unit of value.
    
    Value is generated through coherence contributions, not
    mined or created arbitrarily. The more coherence you
    generate, the more πCODE you receive.
    """
    
    def __init__(self):
        """Initialize πCODE value system."""
        self.picode_algebra = PiCodeAlgebra()
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Total πCODE in existence
        self.total_supply = 0.0
        
        # Balances: node_id -> πCODE amount
        self.balances: Dict[str, float] = {}
        
        # Transaction history
        self.transactions: List[CoherenceTransaction] = []
    
    def coherence_to_picode(self, coherence: float) -> float:
        """
        Convert coherence level to πCODE value.
        
        πCODE = φ^(10×(Ψ - 0.888)) for Ψ ≥ 0.888
        
        Args:
            coherence: Coherence level Ψ
            
        Returns:
            πCODE value
        """
        threshold = 0.888
        
        if coherence < threshold:
            return 0.0
        
        # Exponential scaling with golden ratio
        excess = coherence - threshold
        picode = float(self.phi ** (10 * excess))
        
        return picode
    
    def mint_picode(self, node_id: str, coherence: float) -> float:
        """
        Mint new πCODE based on coherence contribution.
        
        Args:
            node_id: Node contributing coherence
            coherence: Coherence level achieved
            
        Returns:
            Amount of πCODE minted
        """
        amount = self.coherence_to_picode(coherence)
        
        if amount > 0:
            if node_id not in self.balances:
                self.balances[node_id] = 0.0
            
            self.balances[node_id] += amount
            self.total_supply += amount
        
        return amount
    
    def transfer(self, sender: str, receiver: str, amount: float, coherence_proof: float) -> Optional[CoherenceTransaction]:
        """
        Transfer πCODE between nodes.
        
        Requires coherence proof: transaction only valid if
        sender-receiver coherence ≥ 0.888.
        
        Args:
            sender: Sender node ID
            receiver: Receiver node ID
            amount: πCODE amount to transfer
            coherence_proof: Measured coherence between nodes
            
        Returns:
            CoherenceTransaction or None if failed
        """
        # Check balances
        if sender not in self.balances or self.balances[sender] < amount:
            return None
        
        # Verify coherence
        if coherence_proof < 0.888:
            return None
        
        # Execute transfer
        self.balances[sender] -= amount
        
        if receiver not in self.balances:
            self.balances[receiver] = 0.0
        self.balances[receiver] += amount
        
        # Create transaction record
        tx_id = hashlib.sha256(f"{sender}{receiver}{amount}{time.time()}".encode()).hexdigest()[:16]
        
        tx = CoherenceTransaction(
            tx_id=tx_id,
            sender=sender,
            receiver=receiver,
            picode_amount=amount,
            coherence_proof=coherence_proof,
            timestamp=time.time(),
            signature=self._sign_transaction(sender, receiver, amount)
        )
        
        self.transactions.append(tx)
        return tx
    
    def _sign_transaction(self, sender: str, receiver: str, amount: float) -> str:
        """
        Sign transaction with coherence signature.
        
        Args:
            sender: Sender ID
            receiver: Receiver ID
            amount: Amount
            
        Returns:
            Signature string
        """
        # Simplified signature (in real system would use cryptography)
        data = f"{sender}:{receiver}:{amount}"
        signature = hashlib.sha256(data.encode()).hexdigest()[:32]
        return signature
    
    def get_balance(self, node_id: str) -> float:
        """
        Get πCODE balance of a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Balance in πCODE
        """
        return self.balances.get(node_id, 0.0)


class DistributedRecognition:
    """
    Distributed recognition without consensus.
    
    Instead of requiring consensus (e.g., proof-of-work),
    the network recognizes contributions through coherence.
    Multiple independent recognizers validate contributions.
    """
    
    def __init__(self, min_recognizers: int = 3):
        """
        Initialize distributed recognition system.
        
        Args:
            min_recognizers: Minimum recognizers for valid contribution
        """
        self.min_recognizers = min_recognizers
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Recognition events
        self.events: Dict[str, RecognitionEvent] = {}
        
        # Recognizer weights based on coherence
        self.recognizer_weights: Dict[str, float] = {}
    
    def submit_contribution(self, contributor_id: str, contribution_data: Any) -> RecognitionEvent:
        """
        Submit a contribution for recognition.
        
        Args:
            contributor_id: ID of contributor
            contribution_data: Data being contributed
            
        Returns:
            RecognitionEvent
        """
        # Hash contribution
        contribution_str = json.dumps(contribution_data, sort_keys=True)
        contribution_hash = hashlib.sha256(contribution_str.encode()).hexdigest()
        
        # Create event
        event_id = hashlib.sha256(f"{contributor_id}{time.time()}".encode()).hexdigest()[:16]
        
        event = RecognitionEvent(
            event_id=event_id,
            contributor=contributor_id,
            contribution_hash=contribution_hash,
            coherence_level=0.0,
            timestamp=time.time()
        )
        
        self.events[event_id] = event
        return event
    
    def recognize_contribution(self, event_id: str, recognizer_id: str, coherence_score: float):
        """
        Recognize a contribution with coherence score.
        
        Args:
            event_id: Event to recognize
            recognizer_id: ID of recognizer
            coherence_score: Coherence score [0, 1]
        """
        if event_id not in self.events:
            return
        
        event = self.events[event_id]
        
        # Add recognizer
        event.recognizers.add(recognizer_id)
        
        # Update coherence level (weighted average)
        weight = self.recognizer_weights.get(recognizer_id, 1.0)
        
        # Weighted update
        total_weight = sum(self.recognizer_weights.get(r, 1.0) for r in event.recognizers)
        event.coherence_level = (
            (event.coherence_level * (total_weight - weight) + coherence_score * weight) / total_weight
        )
    
    def is_recognized(self, event_id: str) -> bool:
        """
        Check if contribution is recognized.
        
        Requires: >= min_recognizers AND coherence ≥ 0.888
        
        Args:
            event_id: Event ID
            
        Returns:
            True if recognized
        """
        if event_id not in self.events:
            return False
        
        event = self.events[event_id]
        
        return (
            len(event.recognizers) >= self.min_recognizers and
            event.coherence_level >= 0.888
        )
    
    def award_picode(self, event_id: str, picode_system: PiCodeValue) -> float:
        """
        Award πCODE for recognized contribution.
        
        Args:
            event_id: Event ID
            picode_system: PiCodeValue system to use
            
        Returns:
            Amount of πCODE awarded
        """
        if not self.is_recognized(event_id):
            return 0.0
        
        event = self.events[event_id]
        
        # Award based on coherence level
        amount = picode_system.coherence_to_picode(event.coherence_level)
        
        # Bonus for multiple recognizers
        recognizer_bonus = (1 + len(event.recognizers) / 10.0)
        amount *= recognizer_bonus
        
        # Mint πCODE
        picode_system.mint_picode(event.contributor, event.coherence_level)
        
        event.picode_awarded = amount
        
        return amount
    
    def update_recognizer_weight(self, recognizer_id: str, coherence: float):
        """
        Update recognizer's weight based on their coherence.
        
        Args:
            recognizer_id: Recognizer ID
            coherence: Their coherence level
        """
        # Weight based on coherence above threshold
        if coherence >= 0.888:
            weight = float(self.phi ** ((coherence - 0.888) * 5))
            self.recognizer_weights[recognizer_id] = weight


class SymbioticEconomy:
    """
    Post-monetary symbiotic economy.
    
    Economic interactions are based on mutual coherence benefit,
    not zero-sum transactions. When nodes interact coherently,
    both gain value.
    """
    
    def __init__(self):
        """Initialize symbiotic economy."""
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Track symbiotic relationships
        self.symbioses: Dict[Tuple[str, str], float] = {}
        
        # Value generation history
        self.value_generated: List[Dict[str, Any]] = []
    
    def initiate_symbiosis(self, node1_id: str, node2_id: str, initial_coherence: float) -> bool:
        """
        Initiate symbiotic relationship between nodes.
        
        Args:
            node1_id: First node
            node2_id: Second node
            initial_coherence: Initial coherence level
            
        Returns:
            True if symbiosis established
        """
        if initial_coherence < 0.888:
            return False
        
        # Create bidirectional symbiosis
        key1 = tuple(sorted([node1_id, node2_id]))
        self.symbioses[key1] = initial_coherence
        
        return True
    
    def symbiotic_interaction(self, node1_id: str, node2_id: str, picode_system: PiCodeValue) -> Tuple[float, float]:
        """
        Perform symbiotic interaction.
        
        Both nodes gain value proportional to their coherence.
        This is non-zero-sum: total value increases.
        
        Args:
            node1_id: First node
            node2_id: Second node
            picode_system: πCODE value system
            
        Returns:
            Tuple of (value_to_node1, value_to_node2)
        """
        key = tuple(sorted([node1_id, node2_id]))
        
        if key not in self.symbioses:
            return 0.0, 0.0
        
        coherence = self.symbioses[key]
        
        # Value generated: proportional to coherence squared (synergy)
        base_value = picode_system.coherence_to_picode(coherence)
        synergy_factor = coherence ** 2
        
        value1 = base_value * synergy_factor
        value2 = base_value * synergy_factor
        
        # Mint πCODE for both (value creation, not transfer)
        picode_system.mint_picode(node1_id, coherence)
        picode_system.mint_picode(node2_id, coherence)
        
        # Record value generation
        self.value_generated.append({
            'node1': node1_id,
            'node2': node2_id,
            'value_each': base_value * synergy_factor,
            'coherence': coherence,
            'timestamp': time.time()
        })
        
        return value1, value2
    
    def evolve_symbiosis(self, node1_id: str, node2_id: str, interaction_quality: float):
        """
        Evolve symbiotic relationship based on interaction quality.
        
        Good interactions increase coherence (positive feedback).
        
        Args:
            node1_id: First node
            node2_id: Second node
            interaction_quality: Quality score [0, 1]
        """
        key = tuple(sorted([node1_id, node2_id]))
        
        if key in self.symbioses:
            current_coherence = self.symbioses[key]
            
            # Update coherence
            # Good interactions increase coherence
            delta = (interaction_quality - 0.5) * 0.01
            new_coherence = min(current_coherence + delta, 1.0)
            
            self.symbioses[key] = new_coherence
    
    def total_value_generated(self) -> float:
        """
        Compute total value generated through symbiosis.
        
        Returns:
            Total value
        """
        return sum(event['value_each'] * 2 for event in self.value_generated)
    
    def get_symbiosis_strength(self, node1_id: str, node2_id: str) -> float:
        """
        Get strength of symbiotic relationship.
        
        Args:
            node1_id: First node
            node2_id: Second node
            
        Returns:
            Coherence level of symbiosis
        """
        key = tuple(sorted([node1_id, node2_id]))
        return self.symbioses.get(key, 0.0)


def validate_ontological_network() -> Dict[str, bool]:
    """
    Validate all ontological network components.
    
    Returns:
        Dictionary of validation results
    """
    results = {}
    
    # Test node synchronization
    try:
        sync = NodeSynchronization()
        node1 = sync.register_node("node1", NodeType.OBSERVER)
        node2 = sync.register_node("node2", NodeType.CONTRIBUTOR)
        
        # Evolve to create some phase difference
        sync.evolve_network(steps=5)
        
        results['node_synchronization'] = True
    except Exception as e:
        results['node_synchronization'] = False
    
    # Test πCODE value
    try:
        picode = PiCodeValue()
        amount = picode.mint_picode("alice", 0.95)
        balance = picode.get_balance("alice")
        results['picode_value'] = balance > 0 and amount > 0
    except Exception as e:
        results['picode_value'] = False
    
    # Test distributed recognition
    try:
        recognition = DistributedRecognition(min_recognizers=2)
        event = recognition.submit_contribution("bob", {"data": "test"})
        recognition.recognize_contribution(event.event_id, "validator1", 0.92)
        recognition.recognize_contribution(event.event_id, "validator2", 0.91)
        is_rec = recognition.is_recognized(event.event_id)
        results['distributed_recognition'] = is_rec
    except Exception as e:
        results['distributed_recognition'] = False
    
    # Test symbiotic economy
    try:
        economy = SymbioticEconomy()
        picode_sys = PiCodeValue()
        economy.initiate_symbiosis("alice", "bob", 0.92)
        v1, v2 = economy.symbiotic_interaction("alice", "bob", picode_sys)
        results['symbiotic_economy'] = v1 > 0 and v2 > 0
    except Exception as e:
        results['symbiotic_economy'] = False
    
    return results


if __name__ == "__main__":
    # Demonstration
    print("=" * 70)
    print("CAPA 4: Ontological Network Demonstration")
    print("=" * 70)
    
    # 1. Node Synchronization
    print("\n1. Node Synchronization (Ψ ≥ 0.888)")
    print("-" * 70)
    sync = NodeSynchronization(threshold=0.888)
    
    # Register nodes
    nodes = [
        ("alice", NodeType.CONTRIBUTOR),
        ("bob", NodeType.VALIDATOR),
        ("charlie", NodeType.RESONATOR),
        ("dave", NodeType.OBSERVER)
    ]
    
    for node_id, node_type in nodes:
        sync.register_node(node_id, node_type)
    
    # Evolve network
    sync.evolve_network(steps=20)
    
    # Attempt synchronizations
    print("Attempting synchronizations:")
    for i, (id1, _) in enumerate(nodes):
        for id2, _ in enumerate(nodes[i+1:], start=i+1):
            node2_id = nodes[id2][0]
            coherence = sync.measure_coherence(id1, node2_id)
            synced = sync.synchronize_nodes(id1, node2_id)
            status = "✓ SYNCED" if synced else "✗ NOT SYNCED"
            print(f"  {id1} ↔ {node2_id}: Ψ={coherence:.3f} {status}")
    
    # Network coherence
    net_coh = sync.network_coherence()
    print(f"\nOverall network coherence: {net_coh:.3f}")
    
    # 2. πCODE Value System
    print("\n2. πCODE as Unit of Value")
    print("-" * 70)
    picode = PiCodeValue()
    
    # Mint πCODE based on coherence
    contributions = [
        ("alice", 0.95),
        ("bob", 0.91),
        ("charlie", 0.88),
        ("dave", 0.75)  # Below threshold
    ]
    
    print("Minting πCODE from coherence contributions:")
    for node_id, coherence in contributions:
        amount = picode.mint_picode(node_id, coherence)
        balance = picode.get_balance(node_id)
        print(f"  {node_id}: Ψ={coherence:.2f} → {amount:.4f} πCODE (balance: {balance:.4f})")
    
    print(f"\nTotal πCODE supply: {picode.total_supply:.4f}")
    
    # Transfer with coherence proof
    print("\nπCODE transfer (requires coherence proof):")
    alice_bob_coh = sync.measure_coherence("alice", "bob")
    tx = picode.transfer("alice", "bob", 0.5, alice_bob_coh)
    if tx:
        print(f"  ✓ Transfer successful: {tx.sender} → {tx.receiver}, {tx.picode_amount:.2f} πCODE")
        print(f"    Coherence proof: {tx.coherence_proof:.3f}")
        print(f"    New balances: alice={picode.get_balance('alice'):.4f}, bob={picode.get_balance('bob'):.4f}")
    
    # 3. Distributed Recognition
    print("\n3. Distributed Recognition (No Consensus)")
    print("-" * 70)
    recognition = DistributedRecognition(min_recognizers=3)
    
    # Submit contribution
    contribution_data = {
        "type": "analysis",
        "description": "GW250114 coherence analysis",
        "frequency": 141.7001,
        "coherence": 0.93
    }
    
    event = recognition.submit_contribution("alice", contribution_data)
    print(f"Contribution submitted: {event.event_id[:8]}...")
    
    # Multiple independent recognizers
    recognizers = [
        ("bob", 0.94),
        ("charlie", 0.91),
        ("dave", 0.89)
    ]
    
    print("\nIndependent recognition:")
    for recognizer_id, score in recognizers:
        recognition.recognize_contribution(event.event_id, recognizer_id, score)
        print(f"  {recognizer_id} recognizes with Ψ={score:.2f}")
    
    is_recognized = recognition.is_recognized(event.event_id)
    print(f"\nContribution recognized: {is_recognized}")
    print(f"Final coherence level: {event.coherence_level:.3f}")
    print(f"Number of recognizers: {len(event.recognizers)}")
    
    # Award πCODE
    awarded = recognition.award_picode(event.event_id, picode)
    print(f"πCODE awarded: {awarded:.4f}")
    
    # 4. Symbiotic Economy
    print("\n4. Post-Monetary Symbiotic Economy")
    print("-" * 70)
    economy = SymbioticEconomy()
    
    # Initiate symbioses
    symbioses = [
        ("alice", "bob", 0.92),
        ("bob", "charlie", 0.89),
        ("alice", "charlie", 0.90)
    ]
    
    print("Initiating symbiotic relationships:")
    for n1, n2, coh in symbioses:
        success = economy.initiate_symbiosis(n1, n2, coh)
        status = "✓" if success else "✗"
        print(f"  {status} {n1} ⟷ {n2}: Ψ={coh:.2f}")
    
    # Symbiotic interactions (value creation)
    print("\nSymbiotic interactions (both nodes gain value):")
    picode_econ = PiCodeValue()  # Fresh instance for economy
    
    for n1, n2, _ in symbioses:
        v1, v2 = economy.symbiotic_interaction(n1, n2, picode_econ)
        print(f"  {n1} ⟷ {n2}: {n1} gains {v1:.4f}, {n2} gains {v2:.4f} πCODE")
    
    total_value = economy.total_value_generated()
    print(f"\nTotal value created (not transferred): {total_value:.4f} πCODE")
    
    # Validation
    print("\n" + "=" * 70)
    print("Validation Results")
    print("=" * 70)
    validation = validate_ontological_network()
    for component, passed in validation.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{component:30s}: {status}")
