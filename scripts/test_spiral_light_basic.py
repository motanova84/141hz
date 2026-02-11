#!/usr/bin/env python3
"""
Simple test runner for spiral light geometry (no pytest required)
"""

import sys
from pathlib import Path
import traceback

sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.spiral_light_geometry import (
    SpiralLightGeometry,
    SpiralPathParams,
    WaveFunctionParams,
    CoherenceMaximality,
    generate_spiral_path,
    calculate_interference
)
from qcal.constants import F0_HZ
import numpy as np


def test_prime_generation():
    """Test prime number generation"""
    print("Testing prime generation...", end=" ")
    geometry = SpiralLightGeometry()
    primes = geometry.get_primes(10)
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert list(primes) == expected, f"Expected {expected}, got {list(primes)}"
    print("✓")


def test_zeta_zeros():
    """Test Riemann zeta zero calculation"""
    print("Testing zeta zero calculation...", end=" ")
    geometry = SpiralLightGeometry(precision=30)
    zeros = geometry.get_zeta_zeros(3)
    # First zero should be approximately 14.134725
    assert abs(zeros[0] - 14.134725) < 0.001
    assert len(zeros) == 3
    print("✓")


def test_spiral_path():
    """Test spiral path generation"""
    print("Testing spiral path generation...", end=" ")
    t, x, y = generate_spiral_path(duration=0.01, dt=1e-4, prime_index=1)
    assert len(t) == len(x) == len(y)
    assert len(t) > 0
    # Check radius increases (expansion)
    r = np.sqrt(x**2 + y**2)
    assert r[-1] > r[0]
    print("✓")


def test_wave_function():
    """Test wave function generation"""
    print("Testing wave function...", end=" ")
    geometry = SpiralLightGeometry()
    x = np.linspace(-1e-6, 1e-6, 50)
    psi = geometry.wave_function(x, 0.001)
    # Check normalization
    norm = np.sqrt(np.sum(np.abs(psi)**2))
    assert abs(norm - 1.0) < 0.1
    assert psi.dtype == complex
    print("✓")


def test_interference():
    """Test interference pattern"""
    print("Testing interference pattern...", end=" ")
    intensity = calculate_interference(size=32, extent=1e-6, t=0.001)
    assert intensity.shape == (32, 32)
    assert np.all(intensity >= 0)
    print("✓")


def test_coherence():
    """Test coherence measure"""
    print("Testing coherence measure...", end=" ")
    coherence = CoherenceMaximality()
    # Coherent wave function
    psi = np.exp(1j * 0.5) * np.ones(100, dtype=complex)
    psi /= np.sqrt(len(psi))
    C = coherence.coherence_measure(psi, reference_phase=0.5)
    assert 0 <= C <= 1
    assert C > 0.99  # Should be nearly 1 for coherent state
    print("✓")


def test_spectral_frequencies():
    """Test spectral frequencies from zeta zeros"""
    print("Testing spectral frequencies...", end=" ")
    geometry = SpiralLightGeometry()
    frequencies = geometry.zeta_spectral_frequencies(5)
    # First frequency should be approximately f₀
    assert abs(frequencies[0] - F0_HZ) < 1
    assert len(frequencies) == 5
    print("✓")


def test_prime_phase():
    """Test prime phase modulation"""
    print("Testing prime phase modulation...", end=" ")
    geometry = SpiralLightGeometry()
    phi_1 = geometry.prime_phase_modulation(1)
    phi_2 = geometry.prime_phase_modulation(2)
    # Phases should be different
    assert phi_1 != phi_2
    # First prime phase should be 2π (log(2)/log(2) = 1)
    assert abs(phi_1 - 2 * np.pi) < 1e-10
    print("✓")


def main():
    """Run all tests"""
    print("=" * 60)
    print("SPIRAL LIGHT GEOMETRY - BASIC TESTS")
    print("=" * 60)
    print()
    
    tests = [
        test_prime_generation,
        test_zeta_zeros,
        test_spiral_path,
        test_wave_function,
        test_interference,
        test_coherence,
        test_spectral_frequencies,
        test_prime_phase,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED")
            print(f"  Error: {e}")
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        return 1
    
    print()
    print("✓ All basic tests passed!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
