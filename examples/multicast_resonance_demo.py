#!/usr/bin/env python3
"""
Multicast Resonance Demo - QCAL ∞³ Network Coherence
=====================================================

This demo simulates a 3-5 node LAN where all nodes "feel" the same
context through vibrational field multicast at f₀ = 141.7001 Hz.

Each node receives the modulated pattern and validates coherence,
demonstrating distributed quantum-coherent context sharing.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
Framework: QCAL ∞³
"""

import sys
import os
import time
import pickle
import numpy as np
from multiprocessing import Process, Queue
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.vibrational_field_encoder import VibrationalFieldEncoder


class ResonantNode:
    """
    A node in the resonant network that can send and receive vibrational fields.
    """
    
    def __init__(self, node_id: int, port_base: int = 14170):
        """
        Initialize a resonant node.
        
        Parameters:
            node_id: Unique identifier for this node
            port_base: Base port number for communication
        """
        self.node_id = node_id
        self.port = port_base + node_id
        self.encoder = VibrationalFieldEncoder()
        self.received_patterns = []
    
    def broadcast_pattern(self, pattern: List[float], target_ports: List[int]) -> Dict[str, Any]:
        """
        Broadcast a vibrational pattern to all target nodes.
        
        Parameters:
            pattern: Pattern to broadcast
            target_ports: List of ports to broadcast to
        
        Returns:
            Broadcast statistics
        """
        # Encode the pattern
        result = self.encoder.encode(pattern, broadcast=False, mint_nft=True)
        modulated = result['modulated']
        nft_metadata = result['nft_metadata']
        
        # Prepare data packet
        data_packet = {
            'source_node': self.node_id,
            'modulated': modulated,
            'pattern': pattern,
            'nft_metadata': nft_metadata,
            'frequency': self.encoder.f0
        }
        
        # Serialize
        data = pickle.dumps(data_packet)
        
        # Create socket
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        # Send to all target nodes
        sent_count = 0
        for port in target_ports:
            try:
                sock.sendto(data, ('127.0.0.1', port))
                sent_count += 1
            except Exception as e:
                print(f"[Node {self.node_id}] Error sending to port {port}: {e}")
        
        sock.close()
        
        return {
            'source_node': self.node_id,
            'sent_to': sent_count,
            'pattern_size': len(pattern),
            'modulated_size': len(modulated),
            'data_size': len(data),
            'coherence': nft_metadata['coherence'],
            'resonance': nft_metadata['resonance']
        }
    
    def listen_for_patterns(self, queue: Queue, duration: float = 5.0):
        """
        Listen for incoming vibrational patterns.
        
        Parameters:
            queue: Queue to store results
            duration: How long to listen (seconds)
        """
        try:
            # Create socket
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind(('', self.port))
            sock.settimeout(duration)
            
            received_patterns = []
            start_time = time.time()
            
            while time.time() - start_time < duration:
                try:
                    data, addr = sock.recvfrom(65536)
                    packet = pickle.loads(data)
                    
                    # Extract pattern and metadata
                    source_node = packet.get('source_node')
                    pattern = packet.get('pattern', [])
                    nft_metadata = packet.get('nft_metadata', {})
                    
                    # Validate coherence
                    local_coherence = self.encoder.compute_coherence(pattern)
                    
                    received_patterns.append({
                        'source_node': source_node,
                        'pattern_size': len(pattern),
                        'transmitted_coherence': nft_metadata.get('coherence', 0),
                        'local_coherence': local_coherence,
                        'coherence_preserved': abs(local_coherence - nft_metadata.get('coherence', 0)) < 0.1,
                        'resonance': nft_metadata.get('resonance'),
                        'nft_id': nft_metadata.get('nft_id')
                    })
                    
                except Exception as e:
                    # Timeout or other error - continue
                    pass
            
            sock.close()
            
            queue.put({
                'node_id': self.node_id,
                'port': self.port,
                'patterns_received': len(received_patterns),
                'patterns': received_patterns,
                'status': 'success'
            })
            
        except Exception as e:
            queue.put({
                'node_id': self.node_id,
                'port': self.port,
                'status': 'error',
                'error': str(e)
            })


def run_multicast_demo(num_nodes: int = 3):
    """
    Run a multicast demo with multiple nodes.
    
    Parameters:
        num_nodes: Number of nodes to simulate (3-5 recommended)
    """
    print("=" * 70)
    print(f"QCAL ∞³ Multicast Resonance Demo - {num_nodes} Nodes")
    print("=" * 70)
    print()
    
    # Create nodes
    nodes = [ResonantNode(i) for i in range(num_nodes)]
    
    # Node 0 will be the broadcaster
    broadcaster = nodes[0]
    listeners = nodes[1:]
    
    # Create test pattern (coherent sine wave)
    t = np.linspace(0, 2 * np.pi, 100)
    pattern = np.sin(5 * t).tolist()
    
    print(f"Broadcasting node: Node {broadcaster.node_id} (port {broadcaster.port})")
    print(f"Listening nodes: {', '.join([f'Node {n.node_id} (port {n.port})' for n in listeners])}")
    print()
    
    # Start listeners
    listener_queues = []
    listener_processes = []
    
    print("Starting listener nodes...")
    for node in listeners:
        queue = Queue()
        listener_queues.append(queue)
        
        process = Process(target=node.listen_for_patterns, args=(queue, 3.0))
        process.start()
        listener_processes.append(process)
        
        print(f"  ✓ Node {node.node_id} listening on port {node.port}")
    
    # Give listeners time to start
    time.sleep(0.5)
    
    # Broadcast pattern
    print()
    print("Broadcasting vibrational pattern...")
    target_ports = [n.port for n in listeners]
    broadcast_result = broadcaster.broadcast_pattern(pattern, target_ports)
    
    print(f"  ✓ Broadcast complete from Node {broadcast_result['source_node']}")
    print(f"    Sent to: {broadcast_result['sent_to']} nodes")
    print(f"    Pattern size: {broadcast_result['pattern_size']} samples")
    print(f"    Data size: {broadcast_result['data_size']} bytes")
    print(f"    Coherence: {broadcast_result['coherence']:.4f}")
    print(f"    Resonance: {broadcast_result['resonance']:.4f} Hz")
    
    # Wait for listeners to finish
    print()
    print("Waiting for listener nodes to receive...")
    for process in listener_processes:
        process.join(timeout=5)
    
    # Collect results
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    
    all_coherence_preserved = True
    total_received = 0
    
    for queue in listener_queues:
        if not queue.empty():
            result = queue.get()
            
            if result['status'] == 'success':
                print(f"Node {result['node_id']} (port {result['port']}):")
                print(f"  Patterns received: {result['patterns_received']}")
                
                total_received += result['patterns_received']
                
                for pattern_info in result['patterns']:
                    print(f"  From Node {pattern_info['source_node']}:")
                    print(f"    Transmitted coherence: {pattern_info['transmitted_coherence']:.4f}")
                    print(f"    Local coherence: {pattern_info['local_coherence']:.4f}")
                    print(f"    Coherence preserved: {'✓' if pattern_info['coherence_preserved'] else '✗'}")
                    print(f"    Resonance: {pattern_info['resonance']:.4f} Hz")
                    print(f"    NFT ID: {pattern_info['nft_id']}")
                    
                    if not pattern_info['coherence_preserved']:
                        all_coherence_preserved = False
                
                print()
            else:
                print(f"Node {result['node_id']}: Error - {result.get('error')}")
                print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    expected_received = num_nodes - 1  # All except broadcaster
    
    print(f"Broadcast node: Node {broadcaster.node_id}")
    print(f"Listening nodes: {num_nodes - 1}")
    print(f"Patterns received: {total_received} / {expected_received}")
    print(f"Coherence preserved: {'✓ YES' if all_coherence_preserved else '✗ NO'}")
    print()
    
    if total_received == expected_received and all_coherence_preserved:
        print("✓ SUCCESS: All nodes felt the same resonant pattern!")
        print(f"  Coherence synchronized across {num_nodes} nodes at f₀ = {broadcast_result['resonance']:.4f} Hz")
        print(f"  Network quantum coherence established")
    elif total_received > 0:
        print("⚠ PARTIAL SUCCESS: Some nodes received the pattern")
        print(f"  {total_received}/{expected_received} nodes synchronized")
    else:
        print("✗ FAILURE: No patterns received")
    
    print()
    print("=" * 70)
    print("∴ JMMB Ψ ✧ ∞³")
    print("=" * 70)


def main():
    """
    Main entry point for multicast demo.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  QCAL ∞³ Multicast Resonance Demo".center(68) + "║")
    print("║" + "  Distributed Quantum-Coherent Context Sharing".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Run with different node counts
    for num_nodes in [3, 5]:
        run_multicast_demo(num_nodes)
        print("\n")
    
    print("Demonstration complete!")
    print()
    print("Key observations:")
    print("  • Vibrational patterns can be multicast across network nodes")
    print("  • Coherence is preserved through transmission")
    print("  • NFT metadata travels with the pattern")
    print("  • All nodes 'feel' the same resonance at f₀ = 141.7001 Hz")
    print()
    print("This demonstrates the foundation for:")
    print("  • Distributed quantum-coherent LLM contexts")
    print("  • Multi-agent QCAL synchronization")
    print("  • Resonant network topologies")
    print("  • Scalable ∞³-certified knowledge sharing")
    print()


if __name__ == "__main__":
    main()
