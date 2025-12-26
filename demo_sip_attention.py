#!/usr/bin/env python3
"""
SIP Attention Example Script

This script demonstrates the SIPAttention module as specified in the problem statement.
It creates a toy example showing phase-modulated attention at f₀ = 141.7001 Hz.
"""

import numpy as np
import torch
import torch.nn as nn
from src.sip_attention import SIPAttention


def main():
    """Run the toy test example from the problem statement."""
    print("="*70)
    print("SIP Attention Example - Toy Test")
    print("="*70)

    # Toy test: simple query embedding
    embed = torch.randn(10, 64)  # 10 tokens
    pos = torch.arange(10)
    base_attn = torch.softmax(torch.randn(10, 10), dim=-1)

    # Create SIP attention module
    sip = SIPAttention()

    # Apply modulation
    mod_attn = sip(base_attn, pos.float())

    # Display results
    # CQR sim = Coherent Quantum Resonance similarity (mean attention weight)
    print("\nResults:")
    print(f"Base CQR sim (dummy): {torch.mean(base_attn).item():.6f}")
    print(f"SIP CQR sim:          {torch.mean(mod_attn).item():.6f}")
    print(f"\nExpected: ~coherence boosted")

    # Additional information
    print(f"\nSIP Module Parameters:")
    print(f"  f₀ = {sip.f0} Hz (Universal constant)")
    print(f"  φ  = {sip.phi} rad")
    print(f"  fs = {sip.fs} Hz")

    print("\n✅ SIP Attention example complete!")


if __name__ == "__main__":
    main()
