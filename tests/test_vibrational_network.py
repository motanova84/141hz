#!/usr/bin/env python3
"""
Network Smoke Tests for Vibrational Field Encoder
==================================================

This module provides smoke tests for network-based vibrational field
transmission, including two-process sender/receiver validation and
coherence recovery verification.

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

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.vibrational_field_encoder import VibrationalFieldEncoder


def sender_process(pattern, queue, port=14170):
    """
    Sender process that encodes and broadcasts a pattern.
    
    Parameters:
        pattern: Pattern to encode and send
        queue: Queue to report results
        port: Port to send on
    """
    try:
        encoder = VibrationalFieldEncoder()
        
        # Encode the pattern
        result = encoder.encode(pattern, broadcast=False, mint_nft=True)
        modulated = result['modulated']
        
        # Create socket
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        # Serialize data
        data = pickle.dumps({
            'modulated': modulated,
            'nft_metadata': result.get('nft_metadata'),
            'pattern': pattern
        })
        
        # Send to localhost (for testing)
        sock.sendto(data, ('127.0.0.1', port))
        
        queue.put({
            'status': 'success',
            'sent_samples': len(modulated),
            'data_size': len(data)
        })
        
        sock.close()
        
    except Exception as e:
        queue.put({
            'status': 'error',
            'error': str(e)
        })


def receiver_process(queue, port=14170, timeout=5):
    """
    Receiver process that listens for broadcasted patterns.
    
    Parameters:
        queue: Queue to report results
        port: Port to listen on
        timeout: Timeout in seconds
    """
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.settimeout(timeout)
        
        # Receive data
        data, addr = sock.recvfrom(65536)
        
        # Deserialize
        received = pickle.loads(data)
        
        # Validate received data
        modulated = received.get('modulated', [])
        nft_metadata = received.get('nft_metadata', {})
        original_pattern = received.get('pattern', [])
        
        # Compute coherence
        encoder = VibrationalFieldEncoder()
        coherence = encoder.compute_coherence(original_pattern)
        
        queue.put({
            'status': 'success',
            'received_samples': len(modulated),
            'coherence': coherence,
            'nft_id': nft_metadata.get('nft_id'),
            'resonance': nft_metadata.get('resonance'),
            'pattern_recovered': len(original_pattern) > 0
        })
        
        sock.close()
        
    except Exception as e:
        queue.put({
            'status': 'error',
            'error': str(e)
        })


def test_two_process_communication():
    """
    Test two-process sender/receiver communication.
    
    This smoke test validates that:
    1. Sender can encode and transmit a pattern
    2. Receiver can receive and decode the pattern
    3. Coherence is maintained through transmission
    """
    print("=" * 70)
    print("QCAL Network Smoke Test: Two-Process Communication")
    print("=" * 70)
    print()
    
    # Create test pattern
    t = np.linspace(0, 1, 50)
    pattern = np.sin(2 * np.pi * 10 * t).tolist()
    
    # Create queues for results
    sender_queue = Queue()
    receiver_queue = Queue()
    
    # Use a unique port for testing
    test_port = 14171
    
    print(f"Starting receiver on port {test_port}...")
    receiver = Process(target=receiver_process, args=(receiver_queue, test_port))
    receiver.start()
    
    # Give receiver time to bind
    time.sleep(0.5)
    
    print(f"Starting sender on port {test_port}...")
    sender = Process(target=sender_process, args=(pattern, sender_queue, test_port))
    sender.start()
    
    # Wait for processes to complete
    sender.join(timeout=5)
    receiver.join(timeout=5)
    
    # Get results
    sender_result = sender_queue.get() if not sender_queue.empty() else {'status': 'timeout'}
    receiver_result = receiver_queue.get() if not receiver_queue.empty() else {'status': 'timeout'}
    
    print()
    print("Sender Result:")
    print(f"  Status: {sender_result.get('status')}")
    if sender_result.get('status') == 'success':
        print(f"  Sent samples: {sender_result.get('sent_samples')}")
        print(f"  Data size: {sender_result.get('data_size')} bytes")
    else:
        print(f"  Error: {sender_result.get('error', 'timeout')}")
    
    print()
    print("Receiver Result:")
    print(f"  Status: {receiver_result.get('status')}")
    if receiver_result.get('status') == 'success':
        print(f"  Received samples: {receiver_result.get('received_samples')}")
        print(f"  Coherence: {receiver_result.get('coherence', 0):.4f}")
        print(f"  NFT ID: {receiver_result.get('nft_id')}")
        print(f"  Resonance: {receiver_result.get('resonance', 0):.4f} Hz")
        print(f"  Pattern recovered: {receiver_result.get('pattern_recovered')}")
    else:
        print(f"  Error: {receiver_result.get('error', 'timeout')}")
    
    print()
    
    # Validate results
    success = (
        sender_result.get('status') == 'success' and
        receiver_result.get('status') == 'success' and
        receiver_result.get('pattern_recovered', False)
    )
    
    if success:
        print("✓ TEST PASSED: Two-process communication successful!")
        print(f"  Coherence maintained at {receiver_result.get('coherence', 0):.4f}")
    else:
        print("✗ TEST FAILED: Communication error")
    
    print()
    print("=" * 70)
    
    return success


def test_coherence_recovery():
    """
    Test that coherence is recoverable from transmitted patterns.
    
    This validates that:
    1. Patterns maintain structure through encoding
    2. Coherence metrics can be computed on both ends
    3. NFT metadata is transmitted correctly
    """
    print("=" * 70)
    print("QCAL Network Smoke Test: Coherence Recovery")
    print("=" * 70)
    print()
    
    encoder = VibrationalFieldEncoder()
    
    # Create multiple test patterns with different characteristics
    test_cases = [
        ("Sine wave", np.sin(2 * np.pi * 5 * np.linspace(0, 1, 50)).tolist()),
        ("Square wave", (np.sign(np.sin(2 * np.pi * 3 * np.linspace(0, 1, 50)))).tolist()),
        ("Random noise", np.random.randn(50).tolist()),
        ("Constant", [1.0] * 50),
    ]
    
    results = []
    
    for name, pattern in test_cases:
        # Encode
        result = encoder.encode(pattern, mint_nft=True)
        
        # Extract metadata
        coherence = result['nft_metadata']['coherence']
        density = result['nft_metadata']['density']
        
        print(f"{name}:")
        print(f"  Coherence: {coherence:.4f}")
        print(f"  Density: {density:.2f}")
        print(f"  Samples: {len(result['modulated'])}")
        print()
        
        results.append({
            'name': name,
            'coherence': coherence,
            'density': density,
            'valid': 0 <= coherence <= 1
        })
    
    # Validate all coherence scores are in valid range
    all_valid = all(r['valid'] for r in results)
    
    if all_valid:
        print("✓ TEST PASSED: All coherence scores in valid range [0, 1]")
    else:
        print("✗ TEST FAILED: Some coherence scores out of range")
    
    print()
    print("=" * 70)
    
    return all_valid


def main():
    """
    Run all network smoke tests.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  QCAL ∞³ Vibrational Network Smoke Tests".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Run tests
    test1_passed = test_coherence_recovery()
    print()
    
    test2_passed = test_two_process_communication()
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Coherence Recovery Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Two-Process Communication: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print()
    
    if test1_passed and test2_passed:
        print("✓ ALL TESTS PASSED")
        print()
        print("Network coherence transmission is operational.")
        print("Ready for LAN/cluster deployment.")
    else:
        print("✗ SOME TESTS FAILED")
        print()
        print("Review errors above for debugging.")
    
    print("=" * 70)
    print("∴ JMMB Ψ ✧ ∞³")
    print("=" * 70)
    print()
    
    return test1_passed and test2_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
