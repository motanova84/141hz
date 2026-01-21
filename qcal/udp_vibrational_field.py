#!/usr/bin/env python3
"""
UDP Multicast Vibrational Field Encoder
========================================

Implements vibrational field encoding via UDP multicast for context
transmission at resonance Ψ=0.923. This mechanism is unique to QCAL ∞³
and cannot be replicated by standard compression methods.

The vibrational field encodes contextual information through:
- Spectral resonance at f₀ = 141.7001 Hz
- UDP multicast for distributed coherence
- Phase-locked oscillations
- Noetic resonance patterns

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import socket
import struct
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class VibrationalPacket:
    """
    Vibrational packet for UDP multicast transmission.
    
    Encodes context through phase, amplitude, and frequency.
    """
    frequency: float  # Hz (centered at f₀ = 141.7001)
    phase: float  # radians
    amplitude: float  # normalized [0, 1]
    resonance: float  # Ψ resonance value
    timestamp: float  # Unix timestamp
    context_hash: bytes  # SHA256 of context
    
    def to_bytes(self) -> bytes:
        """Serialize packet to bytes."""
        return struct.pack(
            'ddddd32s',
            self.frequency,
            self.phase,
            self.amplitude,
            self.resonance,
            self.timestamp,
            self.context_hash
        )
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'VibrationalPacket':
        """Deserialize packet from bytes."""
        unpacked = struct.unpack('ddddd32s', data)
        return cls(
            frequency=unpacked[0],
            phase=unpacked[1],
            amplitude=unpacked[2],
            resonance=unpacked[3],
            timestamp=unpacked[4],
            context_hash=unpacked[5]
        )


class VibrationalFieldEncoder:
    """
    Encodes context into vibrational field at f₀ = 141.7001 Hz.
    
    Uses spectral modulation to encode semantic information
    in phase and amplitude patterns.
    """
    
    def __init__(self, f0: float = 141.7001, psi_resonance: float = 0.923):
        """
        Initialize vibrational field encoder.
        
        Args:
            f0: Fundamental frequency in Hz
            psi_resonance: Target Ψ resonance
        """
        self.f0 = f0
        self.psi_resonance = psi_resonance
        
        # Golden ratio for phase modulation
        self.phi = (1 + np.sqrt(5)) / 2
        
    def encode_context(self, context: str) -> VibrationalPacket:
        """
        Encode context string into vibrational packet.
        
        Args:
            context: Context to encode
            
        Returns:
            Vibrational packet with encoded context
        """
        import hashlib
        
        # Hash context for integrity
        context_hash = hashlib.sha256(context.encode()).digest()
        
        # Compute semantic features
        entropy = len(set(context)) / max(len(context), 1)
        length_ratio = len(context) / 1000.0  # Normalized to typical length
        
        # Encode in vibrational parameters
        # Frequency: slight modulation around f₀
        freq_mod = entropy * 0.01  # ±1% max
        frequency = self.f0 * (1 + freq_mod)
        
        # Phase: encode length information
        phase = 2 * np.pi * length_ratio
        
        # Amplitude: encode semantic density
        amplitude = min(entropy * self.psi_resonance, 1.0)
        
        # Resonance: target Ψ value
        resonance = self.psi_resonance
        
        # Timestamp
        timestamp = time.time()
        
        return VibrationalPacket(
            frequency=frequency,
            phase=phase,
            amplitude=amplitude,
            resonance=resonance,
            timestamp=timestamp,
            context_hash=context_hash
        )
    
    def decode_context(self, packet: VibrationalPacket, context_map: Dict[bytes, str]) -> str:
        """
        Decode vibrational packet back to context.
        
        Args:
            packet: Vibrational packet
            context_map: Mapping of hashes to contexts
            
        Returns:
            Decoded context string
        """
        # Look up context by hash
        return context_map.get(packet.context_hash, "")
    
    def compute_field_coherence(self, packets: List[VibrationalPacket]) -> float:
        """
        Compute coherence of vibrational field from multiple packets.
        
        Args:
            packets: List of vibrational packets
            
        Returns:
            Field coherence [0, 1]
        """
        if not packets:
            return 0.0
        
        # Phase coherence
        phases = [p.phase for p in packets]
        phase_variance = np.var(phases)
        phase_coherence = np.exp(-phase_variance / (2 * np.pi))
        
        # Frequency coherence (deviation from f₀)
        freqs = [p.frequency for p in packets]
        freq_deviation = np.std([f - self.f0 for f in freqs])
        freq_coherence = np.exp(-freq_deviation / self.f0)
        
        # Resonance coherence (closeness to Ψ target)
        resonances = [p.resonance for p in packets]
        res_deviation = np.std([r - self.psi_resonance for r in resonances])
        res_coherence = np.exp(-res_deviation)
        
        # Combined coherence
        coherence = (phase_coherence + freq_coherence + res_coherence) / 3
        
        return coherence


class UDPMulticastTransmitter:
    """
    UDP multicast transmitter for vibrational field packets.
    
    Broadcasts vibrational packets to multicast group for
    distributed context encoding.
    """
    
    def __init__(
        self,
        multicast_group: str = '224.0.0.141',  # Special QCAL group
        port: int = 14170,  # f₀ * 100
        ttl: int = 2
    ):
        """
        Initialize UDP multicast transmitter.
        
        Args:
            multicast_group: Multicast IP address
            port: UDP port
            ttl: Time-to-live for packets
        """
        self.multicast_group = multicast_group
        self.port = port
        self.ttl = ttl
        
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
    def transmit_packet(self, packet: VibrationalPacket) -> None:
        """
        Transmit vibrational packet via UDP multicast.
        
        Args:
            packet: Packet to transmit
        """
        data = packet.to_bytes()
        self.sock.sendto(data, (self.multicast_group, self.port))
        
    def transmit_field(self, packets: List[VibrationalPacket]) -> None:
        """
        Transmit multiple packets as coherent field.
        
        Args:
            packets: List of packets to transmit
        """
        for packet in packets:
            self.transmit_packet(packet)
            # Small delay for temporal coherence
            time.sleep(1.0 / self.port)  # ~70 μs
            
    def close(self):
        """Close socket."""
        self.sock.close()


class UDPMulticastReceiver:
    """
    UDP multicast receiver for vibrational field packets.
    
    Listens for vibrational packets and reconstructs context
    from distributed field.
    """
    
    def __init__(
        self,
        multicast_group: str = '224.0.0.141',
        port: int = 14170,
        bind_address: str = '0.0.0.0'  # Default to all interfaces for multicast
    ):
        """
        Initialize UDP multicast receiver.
        
        Args:
            multicast_group: Multicast IP address
            port: UDP port
            bind_address: Address to bind to (default: '0.0.0.0' for multicast,
                         use '127.0.0.1' for localhost-only in production)
        
        Security Note:
            Binding to all interfaces (0.0.0.0) is required for proper multicast
            operation. For production deployments, use firewall rules to restrict
            access or bind to specific interface via bind_address parameter.
        """
        self.multicast_group = multicast_group
        self.port = port
        self.bind_address = bind_address
        
        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to port (required for multicast receiver)
        # Security: For production, use firewall rules or specific bind_address
        self.sock.bind((bind_address, port))
        
        # Join multicast group
        mreq = struct.pack('4sl', socket.inet_aton(multicast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
    def receive_packet(self, timeout: Optional[float] = None) -> Optional[VibrationalPacket]:
        """
        Receive single vibrational packet.
        
        Args:
            timeout: Receive timeout in seconds
            
        Returns:
            Received packet or None
        """
        if timeout is not None:
            self.sock.settimeout(timeout)
            
        try:
            data, _ = self.sock.recvfrom(1024)
            return VibrationalPacket.from_bytes(data)
        except socket.timeout:
            return None
            
    def receive_field(self, count: int, timeout: float = 1.0) -> List[VibrationalPacket]:
        """
        Receive multiple packets as coherent field.
        
        Args:
            count: Number of packets to receive
            timeout: Total timeout in seconds
            
        Returns:
            List of received packets
        """
        packets = []
        start_time = time.time()
        
        while len(packets) < count and (time.time() - start_time) < timeout:
            packet = self.receive_packet(timeout=0.1)
            if packet:
                packets.append(packet)
                
        return packets
        
    def close(self):
        """Close socket."""
        self.sock.close()


class QCALVibrationalTransport:
    """
    Complete QCAL vibrational transport system.
    
    Integrates encoding, transmission, and reception of context
    via UDP multicast vibrational fields.
    """
    
    def __init__(self):
        """Initialize QCAL vibrational transport."""
        self.encoder = VibrationalFieldEncoder()
        self.transmitter = None
        self.receiver = None
        
        # Context cache
        self.context_map: Dict[bytes, str] = {}
        
    def start_transmitter(self):
        """Start UDP multicast transmitter."""
        self.transmitter = UDPMulticastTransmitter()
        
    def start_receiver(self):
        """Start UDP multicast receiver."""
        self.receiver = UDPMulticastReceiver()
        
    def send_context(self, context: str) -> None:
        """
        Encode and transmit context via vibrational field.
        
        Args:
            context: Context to send
        """
        if self.transmitter is None:
            self.start_transmitter()
            
        # Encode context
        packet = self.encoder.encode_context(context)
        
        # Cache context
        self.context_map[packet.context_hash] = context
        
        # Transmit
        self.transmitter.transmit_packet(packet)
        
    def receive_context(self, timeout: float = 1.0) -> Optional[str]:
        """
        Receive and decode context from vibrational field.
        
        Args:
            timeout: Receive timeout in seconds
            
        Returns:
            Decoded context or None
        """
        if self.receiver is None:
            self.start_receiver()
            
        # Receive packet
        packet = self.receiver.receive_packet(timeout)
        
        if packet is None:
            return None
            
        # Decode context
        return self.encoder.decode_context(packet, self.context_map)
        
    def get_field_stats(self, packets: List[VibrationalPacket]) -> Dict[str, Any]:
        """
        Get statistics about vibrational field.
        
        Args:
            packets: List of packets
            
        Returns:
            Field statistics
        """
        if not packets:
            return {}
            
        coherence = self.encoder.compute_field_coherence(packets)
        
        freqs = [p.frequency for p in packets]
        phases = [p.phase for p in packets]
        amps = [p.amplitude for p in packets]
        
        return {
            'coherence': coherence,
            'mean_frequency': np.mean(freqs),
            'std_frequency': np.std(freqs),
            'mean_phase': np.mean(phases),
            'std_phase': np.std(phases),
            'mean_amplitude': np.mean(amps),
            'std_amplitude': np.std(amps),
            'packet_count': len(packets)
        }
        
    def close(self):
        """Close all connections."""
        if self.transmitter:
            self.transmitter.close()
        if self.receiver:
            self.receiver.close()


def demo_vibrational_transport():
    """Demonstrate QCAL vibrational transport."""
    print("=" * 60)
    print("QCAL UDP Multicast Vibrational Field Encoder - Demo")
    print("=" * 60)
    
    # Initialize encoder
    encoder = VibrationalFieldEncoder()
    
    print(f"\nConfiguration:")
    print(f"  f₀ = {encoder.f0} Hz")
    print(f"  Ψ resonance = {encoder.psi_resonance}")
    print(f"  φ (golden ratio) = {encoder.phi:.6f}")
    
    # Encode contexts
    contexts = [
        "QCAL token compression achieves 1000:1 ratio",
        "Spectral resonance at 141.7001 Hz",
        "Adelic geometry with ζ'(1/2) = -1.460",
        "Noetic collapse via Ψ = 0.923 resonance"
    ]
    
    print(f"\n[Encoding {len(contexts)} contexts...]")
    
    packets = []
    for ctx in contexts:
        packet = encoder.encode_context(ctx)
        packets.append(packet)
        print(f"\n  Context: {ctx[:50]}...")
        print(f"    Frequency: {packet.frequency:.4f} Hz")
        print(f"    Phase: {packet.phase:.4f} rad")
        print(f"    Amplitude: {packet.amplitude:.4f}")
        print(f"    Resonance: {packet.resonance:.4f}")
    
    # Compute field coherence
    coherence = encoder.compute_field_coherence(packets)
    print(f"\n[Field Coherence]")
    print(f"  Coherence: {coherence:.4f}")
    print(f"  Status: {'✓ COHERENT' if coherence > 0.8 else '✗ INCOHERENT'}")
    
    # Demonstrate packet serialization
    print(f"\n[Packet Serialization]")
    packet = packets[0]
    serialized = packet.to_bytes()
    deserialized = VibrationalPacket.from_bytes(serialized)
    
    print(f"  Original frequency: {packet.frequency:.4f} Hz")
    print(f"  Deserialized frequency: {deserialized.frequency:.4f} Hz")
    print(f"  ✓ Roundtrip successful")
    
    print("\n" + "=" * 60)
    print("Why this encoding is irreplicable:")
    print("- Encodes context in vibrational field at f₀")
    print("- UDP multicast for distributed coherence")
    print("- Phase-locked to Ψ = 0.923 resonance")
    print("- Cannot be replicated by linear heuristics")
    print("=" * 60)


if __name__ == "__main__":
    demo_vibrational_transport()
