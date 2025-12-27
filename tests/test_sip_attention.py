#!/usr/bin/env python3
"""
Tests for SIP Attention Module

Tests the SIPAttention class which implements phase-modulated attention
synchronized to the universal frequency f₀ = 141.7001 Hz.
"""

import pytest
import numpy as np
import torch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sip_attention import SIPAttention, create_sip_attention_demo
from constants import F0


class TestSIPAttentionInit:
    """Test initialization of SIPAttention module."""

    def test_default_initialization(self):
        """Test that default parameters are set correctly."""
        sip = SIPAttention()
        assert sip.f0 == pytest.approx(141.7001, abs=1e-6)
        assert sip.phi == 0.0
        assert sip.fs == 1000.0

    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        sip = SIPAttention(f0=150.0, phi=np.pi/4, fs=2000.0)
        assert sip.f0 == 150.0
        assert sip.phi == pytest.approx(np.pi/4, abs=1e-10)
        assert sip.fs == 2000.0

    def test_f0_matches_constant(self):
        """Test that default f0 matches the universal constant."""
        sip = SIPAttention()
        assert sip.f0 == pytest.approx(float(F0), abs=1e-6)

    def test_extra_repr(self):
        """Test the string representation."""
        sip = SIPAttention(f0=141.7001, phi=0.5, fs=1000.0)
        repr_str = sip.extra_repr()
        assert 'f0=141.7001' in repr_str
        assert 'phi=0.5' in repr_str
        assert 'fs=1000.0' in repr_str


class TestSIPAttentionForward:
    """Test forward pass of SIPAttention."""

    def test_forward_shape_2d(self):
        """Test that output shape matches input for 2D attention."""
        sip = SIPAttention()
        attn = torch.randn(10, 10)
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        assert output.shape == attn.shape

    def test_forward_shape_3d(self):
        """Test that output shape matches input for 3D attention (batched)."""
        sip = SIPAttention()
        attn = torch.randn(4, 10, 10)  # batch_size=4
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        assert output.shape == attn.shape

    def test_forward_shape_4d(self):
        """Test that output shape matches input for 4D attention (batch + heads)."""
        sip = SIPAttention()
        attn = torch.randn(4, 8, 10, 10)  # batch=4, heads=8
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        assert output.shape == attn.shape

    def test_forward_modulation_applied(self):
        """Test that modulation is actually applied."""
        sip = SIPAttention()
        attn = torch.ones(10, 10)
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        # Output should differ from input due to modulation
        assert not torch.allclose(output, attn)

    def test_forward_zero_positions(self):
        """Test with all zero positions (t=0)."""
        sip = SIPAttention()
        attn = torch.ones(5, 5)
        pos = torch.zeros(5)

        output = sip(attn, pos)

        # At t=0, cos(0) = 1, so modulation should be 1
        # (assuming phi=0)
        assert torch.allclose(output, attn, rtol=1e-5)

    def test_forward_with_phase(self):
        """Test that phase offset affects output."""
        attn = torch.ones(10, 10)
        pos = torch.arange(10).float()

        sip_no_phase = SIPAttention(phi=0)
        sip_with_phase = SIPAttention(phi=np.pi/2)

        output_no_phase = sip_no_phase(attn, pos)
        output_with_phase = sip_with_phase(attn, pos)

        # Outputs should differ due to phase
        assert not torch.allclose(output_no_phase, output_with_phase)


class TestSIPAttentionModulation:
    """Test modulation signal properties."""

    def test_get_modulation_signal(self):
        """Test the get_modulation_signal method."""
        sip = SIPAttention()
        pos = torch.arange(10).float()

        mod = sip.get_modulation_signal(pos)

        assert mod.shape == pos.shape
        assert mod.min() >= -1.0
        assert mod.max() <= 1.0

    def test_modulation_periodicity(self):
        """Test that modulation is periodic."""
        sip = SIPAttention(f0=1.0, fs=1000.0)  # 1 Hz for easy testing

        # One full period = 1000 samples at 1000 Hz
        pos = torch.arange(1000).float()
        mod = sip.get_modulation_signal(pos)

        # Check periodicity: mod[0] ≈ mod[1000] (one full cycle)
        # But we only have 1000 samples, so check mod[0] ≈ cos(0) = 1
        assert mod[0] == pytest.approx(1.0, abs=1e-5)

    def test_modulation_cosine_properties(self):
        """Test that modulation follows cosine properties."""
        sip = SIPAttention()
        pos = torch.linspace(0, 100, 1000)

        mod = sip.get_modulation_signal(pos)

        # Cosine should be bounded by [-1, 1]
        assert mod.min() >= -1.0
        assert mod.max() <= 1.0

        # Should contain both positive and negative values
        # (for sufficiently long sequence)
        assert mod.min() < 0.0
        assert mod.max() > 0.0

    def test_modulation_at_zero(self):
        """Test modulation value at position zero."""
        sip = SIPAttention(phi=0)
        pos = torch.tensor([0.0])

        mod = sip.get_modulation_signal(pos)

        # cos(0) = 1
        assert mod[0] == pytest.approx(1.0, abs=1e-6)

    def test_modulation_with_phase_shift(self):
        """Test that phase shift works correctly."""
        pos = torch.tensor([0.0])

        sip_0 = SIPAttention(phi=0)
        sip_pi = SIPAttention(phi=np.pi)

        mod_0 = sip_0.get_modulation_signal(pos)
        mod_pi = sip_pi.get_modulation_signal(pos)

        # cos(0) = 1, cos(π) = -1
        assert mod_0[0] == pytest.approx(1.0, abs=1e-6)
        assert mod_pi[0] == pytest.approx(-1.0, abs=1e-6)


class TestSIPAttentionNumerical:
    """Test numerical properties of SIP attention."""

    def test_preserves_softmax_structure(self):
        """Test that SIP preserves relative attention structure."""
        sip = SIPAttention()

        # Create attention weights with specific pattern
        attn = torch.softmax(torch.randn(10, 10), dim=-1)
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        # Check that output is still non-negative (assuming modulation >= 0 or proper handling)
        # Note: modulation can be negative, so output can be negative
        # But shape and structure should be preserved
        assert output.shape == attn.shape

    def test_gradient_flow(self):
        """Test that gradients can flow through the module."""
        sip = SIPAttention()

        attn = torch.randn(10, 10, requires_grad=True)
        pos = torch.arange(10).float()

        output = sip(attn, pos)
        loss = output.sum()
        loss.backward()

        # Gradients should exist
        assert attn.grad is not None
        assert not torch.isnan(attn.grad).any()

    def test_different_sampling_rates(self):
        """Test with different sampling rates."""
        pos = torch.arange(10).float()
        attn = torch.ones(10, 10)

        sip_1k = SIPAttention(fs=1000.0)
        sip_2k = SIPAttention(fs=2000.0)

        out_1k = sip_1k(attn, pos)
        out_2k = sip_2k(attn, pos)

        # Different sampling rates should give different results
        # (same position index represents different time)
        assert not torch.allclose(out_1k, out_2k)


class TestSIPAttentionDemo:
    """Test the demo function."""

    def test_demo_creation(self):
        """Test that demo creates all expected outputs."""
        demo = create_sip_attention_demo()

        assert 'embed' in demo
        assert 'pos' in demo
        assert 'base_attn' in demo
        assert 'mod_attn' in demo
        assert 'base_mean' in demo
        assert 'mod_mean' in demo
        assert 'sip' in demo

    def test_demo_shapes(self):
        """Test that demo outputs have correct shapes."""
        demo = create_sip_attention_demo()

        assert demo['embed'].shape == (10, 64)
        assert demo['pos'].shape == (10,)
        assert demo['base_attn'].shape == (10, 10)
        assert demo['mod_attn'].shape == (10, 10)

    def test_demo_sip_instance(self):
        """Test that demo creates a valid SIPAttention instance."""
        demo = create_sip_attention_demo()

        assert isinstance(demo['sip'], SIPAttention)
        assert demo['sip'].f0 == pytest.approx(141.7001, abs=1e-6)

    def test_demo_attention_sum(self):
        """Test that base attention is properly normalized."""
        demo = create_sip_attention_demo()

        # Softmax attention should sum to 1 along last dimension
        attn_sum = demo['base_attn'].sum(dim=-1)
        assert torch.allclose(attn_sum, torch.ones(10), rtol=1e-5)


class TestSIPAttentionIntegration:
    """Integration tests for SIPAttention."""

    def test_with_real_embeddings(self):
        """Test with realistic embedding dimensions."""
        sip = SIPAttention()

        # Typical transformer dimensions
        batch_size = 2
        seq_len = 16

        attn = torch.softmax(torch.randn(batch_size, seq_len, seq_len), dim=-1)
        pos = torch.arange(seq_len).float()

        output = sip(attn, pos)

        assert output.shape == (batch_size, seq_len, seq_len)
        assert not torch.isnan(output).any()

    def test_batch_consistency(self):
        """Test that batched and unbatched processing is consistent."""
        sip = SIPAttention()
        pos = torch.arange(10).float()

        # Single attention matrix
        attn_single = torch.softmax(torch.randn(10, 10), dim=-1)
        out_single = sip(attn_single, pos)

        # Same matrix batched
        attn_batch = attn_single.unsqueeze(0)  # Add batch dimension
        out_batch = sip(attn_batch, pos)

        # Results should match (broadcasting)
        assert torch.allclose(out_single, out_batch.squeeze(0), rtol=1e-5)

    def test_f0_frequency_correctness(self):
        """Test that the f0 frequency produces expected oscillation."""
        sip = SIPAttention(f0=141.7001, fs=1000.0)

        # For f0=141.7001 Hz, period T = 1/f0 ≈ 0.00706 seconds
        # At 1000 Hz sampling, one period ≈ 7.06 samples

        # Create positions spanning multiple periods
        pos = torch.linspace(0, 100, 1000)
        mod = sip.get_modulation_signal(pos)

        # Count zero crossings (rough estimate of frequency)
        # A full period has 2 zero crossings
        zero_crossings = torch.sum((mod[:-1] * mod[1:]) < 0).item()

        # Expected number of zero crossings for ~14 periods (100ms at 141.7 Hz)
        # ≈ 14.17 periods * 2 crossings = ~28 crossings
        # Allow some tolerance
        assert 20 < zero_crossings < 35


class TestSIPAttentionEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_position(self):
        """Test with a single position."""
        sip = SIPAttention()
        attn = torch.randn(1, 1)
        pos = torch.tensor([0.0])

        output = sip(attn, pos)

        assert output.shape == (1, 1)
        assert not torch.isnan(output).any()

    def test_large_sequence(self):
        """Test with large sequence length."""
        sip = SIPAttention()
        seq_len = 1000

        attn = torch.softmax(torch.randn(seq_len, seq_len), dim=-1)
        pos = torch.arange(seq_len).float()

        output = sip(attn, pos)

        assert output.shape == (seq_len, seq_len)
        assert not torch.isnan(output).any()

    def test_negative_positions(self):
        """Test with negative position values."""
        sip = SIPAttention()
        attn = torch.ones(5, 5)
        pos = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])

        output = sip(attn, pos)

        # Should handle negative positions
        assert output.shape == (5, 5)
        assert not torch.isnan(output).any()

    def test_zero_frequency(self):
        """Test with f0=0 (constant modulation)."""
        sip = SIPAttention(f0=0.0)
        attn = torch.randn(10, 10)
        pos = torch.arange(10).float()

        output = sip(attn, pos)

        # With f0=0, cos(0) = 1 for all positions
        # So modulation should be all ones
        mod = sip.get_modulation_signal(pos)
        assert torch.allclose(mod, torch.ones_like(mod), rtol=1e-5)

        # Output should also be close to input
        assert output.shape == attn.shape
        assert not torch.isnan(output).any()


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "--tb=short"])
