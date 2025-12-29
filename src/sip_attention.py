#!/usr/bin/env python3
"""
SIP Attention Module - Spatially-Invariant Phase Attention

This module implements a phase-modulated attention mechanism based on the
universal constant f₀ = 141.7001 Hz. The SIPAttention layer modulates
standard attention weights with a cosine phase term synchronized to f₀.

The modulation formula is:
    mod = cos(2π * f₀ * t + φ)

where:
    - f₀ is the fundamental frequency (default: 141.7001 Hz)
    - t is the temporal position (in seconds)
    - φ is the phase offset (default: 0)

This creates coherence-boosted attention patterns that align with the
universal frequency detected in gravitational wave data.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import torch
import torch.nn as nn


class SIPAttention(nn.Module):
    """
    Spatially-Invariant Phase Attention Module.

    Modulates attention weights with a cosine phase term synchronized
    to the universal frequency f₀ = 141.7001 Hz.

    Parameters
    ----------
    f0 : float, optional
        Fundamental frequency in Hz. Default: 141.7001 Hz
    phi : float, optional
        Phase offset in radians. Default: 0
    fs : float, optional
        Sampling frequency in Hz. Default: 1000 Hz (1 kHz)

    Attributes
    ----------
    f0 : float
        The fundamental modulation frequency
    phi : float
        The phase offset
    fs : float
        The sampling frequency for time conversion

    Examples
    --------
    >>> import torch
    >>> # Create simple attention weights
    >>> attn = torch.softmax(torch.randn(10, 10), dim=-1)
    >>> pos = torch.arange(10).float()
    >>>
    >>> # Apply SIP modulation
    >>> sip = SIPAttention()
    >>> mod_attn = sip(attn, pos)
    >>>
    >>> print(f"Original mean: {attn.mean():.4f}")
    >>> print(f"Modulated mean: {mod_attn.mean():.4f}")
    """

    def __init__(self, f0: float = 141.7001, phi: float = 0, fs: float = 1000.0):
        """
        Initialize the SIPAttention module.

        Parameters
        ----------
        f0 : float, optional
            Fundamental frequency in Hz (default: 141.7001)
        phi : float, optional
            Phase offset in radians (default: 0)
        fs : float, optional
            Sampling frequency in Hz (default: 1000.0)
        """
        super().__init__()
        self.f0 = f0
        self.phi = phi
        self.fs = fs

    def forward(self, attn_weights: torch.Tensor, positions: torch.Tensor) -> torch.Tensor:
        """
        Apply phase modulation to attention weights.

        Parameters
        ----------
        attn_weights : torch.Tensor
            Attention weight matrix of shape (seq_len, seq_len) or
            (batch, seq_len, seq_len) or (batch, heads, seq_len, seq_len)
        positions : torch.Tensor
            Position indices for temporal modulation, shape (seq_len,)
            Positions are converted to time via t = positions / fs

        Returns
        -------
        torch.Tensor
            Phase-modulated attention weights with the same shape as input

        Notes
        -----
        The modulation is applied as:
            output = attn_weights * mod.unsqueeze(-1)
        where:
            mod = cos(2π * f₀ * t + φ)
            t = positions / fs
        """
        # Convert positions to time (in seconds)
        t = positions / self.fs

        # Calculate phase modulation: cos(2π * f₀ * t + φ)
        mod = torch.cos(2 * np.pi * self.f0 * t + self.phi)

        # Apply modulation by broadcasting along the last dimension
        # mod shape: (seq_len,) -> unsqueeze to (seq_len, 1) for broadcasting
        modulated_attn = attn_weights * mod.unsqueeze(-1)

        return modulated_attn

    def get_modulation_signal(self, positions: torch.Tensor) -> torch.Tensor:
        """
        Get the raw modulation signal for given positions.

        Parameters
        ----------
        positions : torch.Tensor
            Position indices, shape (seq_len,)

        Returns
        -------
        torch.Tensor
            Modulation signal values, shape (seq_len,)
        """
        t = positions / self.fs
        return torch.cos(2 * np.pi * self.f0 * t + self.phi)

    def extra_repr(self) -> str:
        """
        Extra representation string for the module.

        Returns
        -------
        str
            String representation showing f0, phi, and fs parameters
        """
        return f'f0={self.f0}, phi={self.phi}, fs={self.fs}'


def create_sip_attention_demo() -> dict:
    """
    Create a demonstration of SIPAttention with toy data.

    Returns
    -------
    dict
        Dictionary containing:
        - 'embed': Random embeddings
        - 'pos': Position indices
        - 'base_attn': Base attention weights
        - 'mod_attn': Modulated attention weights
        - 'base_mean': Mean of base attention
        - 'mod_mean': Mean of modulated attention
        - 'sip': The SIPAttention module
    """
    # Create toy embeddings
    embed = torch.randn(10, 64)  # 10 tokens, 64-dim embeddings

    # Create position indices
    pos = torch.arange(10).float()

    # Create base attention weights (using random similarity scores)
    base_attn = torch.softmax(torch.randn(10, 10), dim=-1)

    # Apply SIP modulation
    sip = SIPAttention()
    mod_attn = sip(base_attn, pos)

    return {
        'embed': embed,
        'pos': pos,
        'base_attn': base_attn,
        'mod_attn': mod_attn,
        'base_mean': base_attn.mean().item(),
        'mod_mean': mod_attn.mean().item(),
        'sip': sip
    }


if __name__ == "__main__":
    """Run a simple demo of SIPAttention."""
    print("="*70)
    print("SIP Attention Demo - Phase-Modulated Attention at f₀ = 141.7001 Hz")
    print("="*70)

    demo = create_sip_attention_demo()

    print(f"\nBase attention mean (CQR sim): {demo['base_mean']:.6f}")
    print(f"SIP-modulated attention mean:   {demo['mod_mean']:.6f}")
    print(f"\nModulation factor: {demo['mod_mean']/demo['base_mean']:.6f}")

    # Show the modulation signal
    print(f"\nSIP Module: {demo['sip']}")
    print(f"Position range: {demo['pos'].min():.0f} to {demo['pos'].max():.0f}")

    # Get modulation values
    mod_signal = demo['sip'].get_modulation_signal(demo['pos'])
    print(f"Modulation signal range: [{mod_signal.min():.4f}, {mod_signal.max():.4f}]")

    print("\n✅ SIP Attention demonstration complete!")
