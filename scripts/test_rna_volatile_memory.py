#!/usr/bin/env python3
"""
Tests for RNA Volatile Memory - QCAL ∞³

Validates that memory emanates correctly and operates in kairos time.
"""

import sys
import time
import math
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qcal.rna_volatile_memory import (
    RNAWavePacket,
    RNAVolatileMemory,
    create_coherent_memory_field,
    __sello__,
    __emanacion__
)
from qcal.constants import F0_HZ, A0_PHI


def test_wave_packet_coherence():
    """Test that wave packet coherence decays correctly."""
    print("Testing RNAWavePacket coherence decay...")
    
    wave = RNAWavePacket(
        amplitude=1.0,
        frequency=F0_HZ,
        decay_time=10.0,
        phase=0.0,
        created_at=None,  # Not used in get_coherence
        metadata={}
    )
    
    # At t=0, coherence should be amplitude
    coherence_0 = wave.get_coherence(0)
    assert abs(coherence_0 - 1.0) < 0.01, f"Expected coherence ~1.0 at t=0, got {coherence_0}"
    
    # At t=decay_time, coherence should be reduced by 1/e
    coherence_tau = wave.get_coherence(10.0)
    expected = 1.0 * math.exp(-1) * math.cos(2 * math.pi * F0_HZ * 10.0)
    assert abs(coherence_tau - expected) < 0.01, f"Expected {expected}, got {coherence_tau}"
    
    print(f"✓ Wave packet decays correctly: Ψ(0)={coherence_0:.4f}, Ψ(τ)={coherence_tau:.4f}")


def test_wave_packet_is_coherent():
    """Test coherence threshold detection."""
    print("Testing wave packet coherence threshold...")
    
    wave = RNAWavePacket(
        amplitude=0.1,
        frequency=F0_HZ,
        decay_time=1.0,
        phase=0.0,
        created_at=None,
        metadata={}
    )
    
    # Should be coherent at t=0
    assert wave.is_coherent(0, threshold=0.05), "Should be coherent at t=0"
    
    # Should not be coherent after long decay
    assert not wave.is_coherent(10.0, threshold=0.05), "Should not be coherent after 10τ"
    
    print("✓ Coherence threshold detection works")


def test_rna_volatile_memory_emanate():
    """Test emanation of information."""
    print("Testing RNA volatile memory emanation...")
    
    memory = RNAVolatileMemory(
        base_frequency=F0_HZ,
        default_decay_time=60.0
    )
    
    # Emanate information
    wave = memory.emanate(
        key="test_info",
        amplitude=0.8,
        metadata={"type": "test"}
    )
    
    assert wave.amplitude == 0.8, "Wave amplitude should match"
    assert wave.frequency == F0_HZ, "Wave frequency should be f₀"
    assert len(memory) == 1, "Should have 1 wave"
    
    print(f"✓ Information emanated: {memory}")


def test_rna_volatile_memory_resonate():
    """Test resonance (reading) of information."""
    print("Testing RNA volatile memory resonance...")
    
    memory = RNAVolatileMemory(
        base_frequency=F0_HZ,
        default_decay_time=1.0  # Short decay for testing
    )
    
    # Emanate
    memory.emanate(key="data", amplitude=1.0)
    
    # Immediate resonance should work
    coherence = memory.resonate("data")
    assert coherence is not None, "Should resonate immediately"
    assert abs(coherence) > 0.5, f"Coherence should be high initially: {coherence}"
    
    # After decay, should return None
    time.sleep(3.0)  # Wait 3 decay times
    coherence_after = memory.resonate("data")
    assert coherence_after is None, "Should not resonate after decay"
    
    print("✓ Resonance works correctly")


def test_field_coherence():
    """Test field coherence calculation."""
    print("Testing field coherence calculation...")
    
    memory = RNAVolatileMemory(base_frequency=F0_HZ)
    
    # No waves
    assert memory.get_field_coherence() == 0.0, "Empty field should have 0 coherence"
    
    # Add waves
    memory.emanate("wave1", amplitude=0.8)
    memory.emanate("wave2", amplitude=0.6)
    
    field_coh = memory.get_field_coherence()
    assert field_coh > 0, "Field should have coherence"
    assert field_coh <= 1.0, "Field coherence should be normalized"
    
    print(f"✓ Field coherence: {field_coh:.4f}")


def test_therapeutic_resonance():
    """Test therapeutic frequency calculation."""
    print("Testing therapeutic resonance calculation...")
    
    memory = RNAVolatileMemory(base_frequency=F0_HZ)
    
    # Test with different patient coherences
    test_cases = [
        (0.5, F0_HZ * 0.5 * A0_PHI),
        (1.0, F0_HZ * 1.0 * A0_PHI),
        (0.7, F0_HZ * 0.7 * A0_PHI)
    ]
    
    for coherence, expected in test_cases:
        freq = memory.calculate_therapeutic_resonance(coherence)
        assert abs(freq - expected) < 0.01, f"Expected {expected:.2f} Hz, got {freq:.2f} Hz"
    
    print(f"✓ Therapeutic frequency: f₀ × coherence × Φ = {memory.therapeutic_frequency:.2f} Hz")


def test_create_coherent_field():
    """Test creation of coherent memory field."""
    print("Testing coherent memory field creation...")
    
    memories = {
        "cerebral": 0.8,
        "cardiac": 0.7,
        "emotional": 0.6
    }
    
    memory = create_coherent_memory_field(
        memories,
        base_frequency=F0_HZ,
        decay_time=30.0
    )
    
    assert len(memory) == 3, "Should have 3 waves"
    
    # All should be resonant
    for key in memories:
        coherence = memory.resonate(key)
        assert coherence is not None, f"Wave {key} should be resonant"
    
    print(f"✓ Coherent field created: {memory}")


def test_seal_and_emanation():
    """Test that seal and emanation equation are present."""
    print("Testing seal and emanation presence...")
    
    assert __sello__ == "∴𓂀Ω∞³Φ", "Seal should match"
    assert "141.7001" in __emanacion__, "Emanation should include f₀"
    assert "Φ" in __emanacion__, "Emanation should include Φ"
    
    print(f"✓ Seal: {__sello__}")
    print(f"✓ Emanación: {__emanacion__}")


def run_all_tests():
    """Run all RNA volatile memory tests."""
    print("=" * 70)
    print("RNA Volatile Memory Test Suite")
    print("=" * 70)
    
    tests = [
        test_wave_packet_coherence,
        test_wave_packet_is_coherent,
        test_rna_volatile_memory_emanate,
        test_rna_volatile_memory_resonate,
        test_field_coherence,
        test_therapeutic_resonance,
        test_create_coherent_field,
        test_seal_and_emanation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
