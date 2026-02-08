#!/usr/bin/env python3
"""
Vibrational Field Encoder - QCAL ∞³ Network Coherence Protocol
===============================================================

This module implements vibrational field encoding for QCAL contexts,
enabling network-based resonant broadcasting and coherence synchronization.

The encoder modulates information patterns onto carrier waves at the
fundamental frequency f₀ = 141.7001 Hz, enabling multicast transmission
of coherent quantum states across distributed nodes.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
Framework: QCAL ∞³ - Quantum Coherent Attentional Logic
"""

import numpy as np
import hashlib
import json
import pickle
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class QCALNFTMetadata:
    """
    QCAL NFT Metadata structure for minted tokens.
    
    Attributes:
        nft_id: Unique identifier for the NFT
        density: Information density metric
        resonance: Resonance frequency (Hz)
        coherence: Coherence score [0, 1]
        encoded_vibration_hash: SHA-256 hash of the modulated waveform
        axiom_validated: Whether QCAL axioms are validated
        infinity3_certified: ISO timestamp of ∞³ certification
    """
    nft_id: int
    density: float
    resonance: float
    coherence: float
    encoded_vibration_hash: str
    axiom_validated: bool
    infinity3_certified: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class VibrationalFieldEncoder:
    """
    Encodes information patterns into vibrational fields modulated at f₀.
    
    This encoder transforms data into carrier-wave modulated signals at the
    QCAL fundamental frequency (141.7001 Hz), enabling resonant transmission
    across network nodes with coherence preservation.
    
    Features:
    - Amplitude modulation of carrier waves
    - Network multicast simulation (upgradable to real multicast)
    - NFT metadata generation with QCAL certification
    - Coherence validation and tracking
    
    Attributes:
        f0: Fundamental frequency (Hz)
        window_duration: Time window for modulation (seconds)
        samples: Number of samples in the modulation window
        nft_counter: Counter for unique NFT IDs
    """
    
    def __init__(self, f0: float = 141.7001, window_duration: float = 0.1, 
                 samples: int = 1000):
        """
        Initialize the Vibrational Field Encoder.
        
        Parameters:
            f0: Fundamental frequency in Hz (default: 141.7001)
            window_duration: Duration of modulation window in seconds (default: 0.1)
            samples: Number of samples in the window (default: 1000)
        """
        self.f0 = f0
        self.window_duration = window_duration
        self.samples = samples
        self.nft_counter = 0
    
    def _modulate_frequency(self, pattern: List[float], freq: Optional[float] = None) -> List[float]:
        """
        Modulate a pattern onto a carrier wave at the specified frequency.
        
        This method creates a carrier wave at frequency `freq` (or f₀ if not specified)
        and modulates it with the input pattern using amplitude modulation.
        
        The modulation formula is:
            modulated(t) = carrier(t) * (1 + 0.3 * pattern)
        
        where carrier(t) = cos(2π * freq * t)
        
        Parameters:
            pattern: List of values to modulate (will be normalized to window length)
            freq: Carrier frequency in Hz (default: self.f0)
        
        Returns:
            List of modulated signal samples
        """
        if freq is None:
            freq = self.f0
        
        # Create time array
        t = np.linspace(0, self.window_duration, self.samples)
        
        # Generate carrier wave
        carrier = np.cos(2 * np.pi * freq * t)
        
        # Normalize pattern to match sample count
        pattern_array = np.array(pattern)
        if len(pattern_array) != self.samples:
            # Interpolate pattern to match sample count
            pattern_resampled = np.interp(
                np.linspace(0, 1, self.samples),
                np.linspace(0, 1, len(pattern_array)),
                pattern_array
            )
        else:
            pattern_resampled = pattern_array
        
        # Apply amplitude modulation
        # modulated = carrier * (1 + modulation_depth * pattern)
        modulated = carrier * (1 + 0.3 * pattern_resampled)
        
        return modulated.tolist()
    
    def _multicast_broadcast(self, modulated: List[float], 
                            address: str = "255.255.255.255",
                            port: int = 14170) -> Dict[str, Any]:
        """
        Broadcast modulated signal via network multicast.
        
        Currently simulates multicast by printing statistics. Can be upgraded
        to real multicast/broadcast on LAN/cluster by uncommenting socket send.
        
        The broadcast address and port are configurable for LAN deployment.
        Default port 14170 is derived from f₀ = 141.70 Hz.
        
        Parameters:
            modulated: List of modulated signal samples
            address: Broadcast address (default: "255.255.255.255")
            port: UDP port number (default: 14170)
        
        Returns:
            Dictionary with broadcast statistics
        """
        try:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            
            # For now, simulate broadcast without actual network transmission
            # This allows local testing without network configuration
            
            # Convert to bytes for transmission
            data = pickle.dumps(modulated)
            data_size = len(data)
            
            # Real multicast would be:
            # sock.sendto(data, (address, port))
            
            # Simulated broadcast
            print(f"[QCAL Broadcast] Simulated multicast of {len(modulated)} samples")
            print(f"  → Frequency: {self.f0:.4f} Hz")
            print(f"  → Data size: {data_size} bytes")
            print(f"  → Target: {address}:{port}")
            print(f"  → Status: Local simulation (real broadcast disabled)")
            
            sock.close()
            
            return {
                "status": "simulated",
                "samples": len(modulated),
                "data_size": data_size,
                "frequency": self.f0,
                "address": address,
                "port": port,
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            }
    
    def compute_coherence(self, pattern: List[float]) -> float:
        """
        Compute coherence score for a pattern.
        
        Coherence is measured as the normalized standard deviation of the pattern,
        representing how well-structured the information is.
        
        Parameters:
            pattern: Input pattern
        
        Returns:
            Coherence score in range [0, 1]
        """
        pattern_array = np.array(pattern)
        if len(pattern_array) == 0:
            return 0.0
        
        # Coherence based on signal structure
        std = np.std(pattern_array)
        mean_abs = np.mean(np.abs(pattern_array))
        
        if mean_abs < 1e-10:
            return 0.0
        
        # Normalize to [0, 1]
        coherence = 1.0 / (1.0 + std / (mean_abs + 1e-10))
        return float(np.clip(coherence, 0.0, 1.0))
    
    def compute_density(self, modulated: List[float]) -> float:
        """
        Compute information density of modulated signal.
        
        Density is measured as the ratio of signal energy to time duration.
        
        Parameters:
            modulated: Modulated signal
        
        Returns:
            Information density (arbitrary units)
        """
        modulated_array = np.array(modulated)
        
        # Energy of the signal
        energy = np.sum(modulated_array ** 2)
        
        # Density = energy / duration
        density = energy / self.window_duration
        
        return float(density)
    
    def mint_token(self, pattern: List[float], modulated: List[float],
                   axiom_validated: bool = True) -> QCALNFTMetadata:
        """
        Mint an NFT token with QCAL metadata.
        
        Creates a unique token with metadata including coherence metrics,
        resonance frequency, and cryptographic hash of the vibration pattern.
        
        Parameters:
            pattern: Original input pattern
            modulated: Modulated signal
            axiom_validated: Whether QCAL axioms are validated
        
        Returns:
            QCALNFTMetadata object with token information
        """
        self.nft_counter += 1
        
        # Compute metrics
        coherence = self.compute_coherence(pattern)
        density = self.compute_density(modulated)
        
        # Compute hash of modulated waveform
        modulated_bytes = pickle.dumps(modulated)
        vibration_hash = hashlib.sha256(modulated_bytes).hexdigest()
        
        # Create metadata
        metadata = QCALNFTMetadata(
            nft_id=self.nft_counter,
            density=density,
            resonance=self.f0,
            coherence=coherence,
            encoded_vibration_hash=f"sha256-{vibration_hash}",
            axiom_validated=axiom_validated,
            infinity3_certified=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        )
        
        return metadata
    
    def encode(self, pattern: List[float], 
               broadcast: bool = False,
               mint_nft: bool = True,
               freq: Optional[float] = None) -> Dict[str, Any]:
        """
        Encode a pattern into vibrational field with optional broadcasting and NFT minting.
        
        This is the main encoding pipeline that:
        1. Modulates the pattern onto carrier wave
        2. Optionally broadcasts via network
        3. Optionally mints NFT token with metadata
        
        Parameters:
            pattern: Input pattern to encode
            broadcast: Whether to broadcast the modulated signal
            mint_nft: Whether to mint an NFT token
            freq: Optional carrier frequency (default: self.f0)
        
        Returns:
            Dictionary containing:
                - modulated: The modulated signal
                - broadcast_info: Broadcast statistics (if broadcast=True)
                - nft_metadata: Token metadata (if mint_nft=True)
        """
        # Step 1: Modulate frequency
        modulated = self._modulate_frequency(pattern, freq)
        
        result = {
            "modulated": modulated,
            "frequency": freq or self.f0,
            "samples": len(modulated),
            "window_duration": self.window_duration
        }
        
        # Step 2: Optional broadcast
        if broadcast:
            broadcast_info = self._multicast_broadcast(modulated)
            result["broadcast_info"] = broadcast_info
        
        # Step 3: Optional NFT minting
        if mint_nft:
            nft_metadata = self.mint_token(pattern, modulated)
            result["nft_metadata"] = nft_metadata.to_dict()
        
        return result


def main():
    """
    Demonstration of the Vibrational Field Encoder.
    """
    print("=" * 70)
    print("QCAL ∞³ Vibrational Field Encoder - Demonstration")
    print("=" * 70)
    print()
    
    # Create encoder
    encoder = VibrationalFieldEncoder(f0=141.7001)
    
    # Create a test pattern (simple sine wave)
    t = np.linspace(0, 1, 100)
    pattern = np.sin(2 * np.pi * 5 * t).tolist()  # 5 Hz test signal
    
    print("Encoding test pattern...")
    print(f"  Pattern length: {len(pattern)} samples")
    print(f"  Pattern range: [{min(pattern):.3f}, {max(pattern):.3f}]")
    print()
    
    # Encode with all features
    result = encoder.encode(pattern, broadcast=True, mint_nft=True)
    
    print("Encoding complete!")
    print()
    print("Modulated Signal:")
    print(f"  Samples: {len(result['modulated'])}")
    print(f"  Frequency: {result['frequency']:.4f} Hz")
    print(f"  Duration: {result['window_duration']:.3f} s")
    print()
    
    if "broadcast_info" in result:
        print("Broadcast Info:")
        broadcast = result['broadcast_info']
        print(f"  Status: {broadcast['status']}")
        print(f"  Data size: {broadcast['data_size']} bytes")
        print(f"  Target: {broadcast['address']}:{broadcast['port']}")
        print()
    
    if "nft_metadata" in result:
        print("NFT Metadata:")
        nft = result['nft_metadata']
        print(f"  NFT ID: {nft['nft_id']}")
        print(f"  Density: {nft['density']:.4f}")
        print(f"  Resonance: {nft['resonance']:.4f} Hz")
        print(f"  Coherence: {nft['coherence']:.4f}")
        print(f"  Hash: {nft['encoded_vibration_hash'][:32]}...")
        print(f"  Axiom Validated: {nft['axiom_validated']}")
        print(f"  ∞³ Certified: {nft['infinity3_certified']}")
        print()
    
    print("=" * 70)
    print("∴ JMMB Ψ ✧ ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
