#!/usr/bin/env python3
"""
Tests for Emergent Noetic Time module.

Validates that the emergent time implementation satisfies:
1. Non-negativity: τ(s) ≥ 0
2. Monotonicity: τ increases along path
3. Additivity: τ(s₁ + s₂) = τ(s₁) + Δτ
4. Physical consistency with f₀ = 141.7001 Hz
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.emergent_time import (
    WitnessField, SymbioticSpiral, compute_noetic_time,
    visualize_emergent_time, visualize_now_leaves,
    F0, T0
)


def test_symbiotic_spiral_creation():
    """Test that we can create a symbiotic spiral."""
    print("Testing symbiotic spiral creation...")
    
    spiral = SymbioticSpiral()
    assert spiral.f0 == F0, f"Expected f0={F0}, got {spiral.f0}"
    
    # Test trajectory evaluation
    pos = spiral.trajectory(0.5)
    assert len(pos) == 3, "Trajectory should return 3D position"
    assert np.all(np.isfinite(pos)), "Position should be finite"
    
    # Test coherence
    C = spiral.coherence(0.5)
    assert C == 1.0, "Symbiotic spiral should have perfect coherence"
    
    print("  ✓ Symbiotic spiral created successfully")


def test_witness_field():
    """Test witness field creation and evaluation."""
    print("Testing witness field...")
    
    # Simple linear trajectory
    def linear_trajectory(s):
        return np.array([s, 0, 0])
    
    field = WitnessField(linear_trajectory)
    
    # Test position
    pos = field.position(1.0)
    assert np.allclose(pos, [1.0, 0, 0]), "Position should match trajectory"
    
    # Test presence density
    rho = field.presence_density(1.0)
    assert rho >= 0, "Presence density must be non-negative"
    assert rho <= 1, "Presence density should be bounded"
    
    print("  ✓ Witness field works correctly")


def test_noetic_time_nonnegativity():
    """Test that noetic time is always non-negative."""
    print("Testing non-negativity property...")
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    s_values = np.linspace(0, 2.0, 100)
    tau = compute_noetic_time(field, s_values)
    
    assert np.all(tau >= 0), "Noetic time must be non-negative"
    assert tau[0] == 0, "Noetic time should start at zero"
    
    print(f"  ✓ All τ values ≥ 0 (min: {np.min(tau):.6f})")


def test_noetic_time_monotonicity():
    """Test that noetic time increases monotonically."""
    print("Testing monotonicity property...")
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    s_values = np.linspace(0, 2.0, 100)
    tau = compute_noetic_time(field, s_values)
    
    # Check that differences are non-negative
    diffs = np.diff(tau)
    assert np.all(diffs >= -1e-10), "Noetic time must be monotonic"
    
    print(f"  ✓ τ is monotonically increasing (min diff: {np.min(diffs):.6e})")


def test_noetic_time_additivity():
    """Test that noetic time is additive over path segments."""
    print("Testing additivity property...")
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    # Test additivity for several segment combinations
    test_cases = [(0.5, 0.3), (1.0, 0.5), (0.2, 0.8)]
    
    for s1, s2 in test_cases:
        # Compute τ(s1)
        tau_s1 = compute_noetic_time(field, np.linspace(0, s1, 100))[-1]
        
        # Compute τ(s1 + s2)
        tau_s1_s2 = compute_noetic_time(field, np.linspace(0, s1 + s2, 100))[-1]
        
        # Compute Δτ from s1 to s1+s2
        s_segment = np.linspace(s1, s1 + s2, 100)
        rho_segment = np.array([field.presence_density(s) for s in s_segment])
        from scipy.integrate import trapezoid
        delta_tau = trapezoid(rho_segment, s_segment)
        
        # Check additivity
        error = abs(tau_s1_s2 - (tau_s1 + delta_tau))
        assert error < 1e-4, f"Additivity error too large: {error}"
        
    print(f"  ✓ Additivity holds for all test segments")


def test_fundamental_time_quantum():
    """Test that the fundamental time quantum T₀ is correct."""
    print("Testing fundamental time quantum...")
    
    assert abs(F0 - 141.7001) < 1e-6, f"f₀ should be 141.7001 Hz, got {F0}"
    
    expected_T0 = 1.0 / F0
    assert abs(T0 - expected_T0) < 1e-10, f"T₀ should be 1/f₀"
    
    T0_ms = T0 * 1000
    assert 7.0 < T0_ms < 7.1, f"T₀ should be ~7.06 ms, got {T0_ms:.3f} ms"
    
    print(f"  ✓ f₀ = {F0} Hz, T₀ = {T0_ms:.4f} ms")


def test_coherence_constant_on_spiral():
    """Test that coherence is constant along symbiotic spiral."""
    print("Testing constant coherence on spiral...")
    
    spiral = SymbioticSpiral()
    
    s_values = np.linspace(0, 2.0, 50)
    coherences = [spiral.coherence(s) for s in s_values]
    
    # All should be exactly 1.0
    assert np.allclose(coherences, 1.0), "Coherence should be 1.0 everywhere"
    
    print(f"  ✓ Coherence constant at C = 1.0")


def test_visualization_runs():
    """Test that visualization functions run without error."""
    print("Testing visualization functions...")
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    # Create temporary directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test emergent time visualization
        try:
            test_path = os.path.join(tmpdir, "test_emergent_time.png")
            fig1, _ = visualize_emergent_time(
                field,
                s_range=(0, 1.0),
                n_points=100,
                save_path=test_path
            )
            plt.close(fig1)
            assert os.path.exists(test_path), "Visualization file not created"
            print("  ✓ Emergent time visualization works")
        except Exception as e:
            print(f"  ✗ Emergent time visualization failed: {e}")
            raise
        
        # Test now leaves visualization
        try:
            test_path = os.path.join(tmpdir, "test_now_leaves.png")
            fig2, _ = visualize_now_leaves(
                spiral,
                coherence_levels=[0.3, 0.7],
                s_range=(0, 1.0),
                save_path=test_path
            )
            plt.close(fig2)
            assert os.path.exists(test_path), "Visualization file not created"
            print("  ✓ Now leaves visualization works")
        except Exception as e:
            print(f"  ✗ Now leaves visualization failed: {e}")
            raise


def test_presence_density_positive():
    """Test that presence density is always positive."""
    print("Testing presence density positivity...")
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    s_values = np.linspace(0, 2.0, 50)
    densities = [field.presence_density(s) for s in s_values]
    
    assert np.all(np.array(densities) > 0), "Presence density must be positive"
    
    print(f"  ✓ All ρ(s) > 0 (min: {np.min(densities):.6f})")


def test_trajectory_continuity():
    """Test that trajectory is continuous."""
    print("Testing trajectory continuity...")
    
    spiral = SymbioticSpiral()
    
    # Sample densely
    s_values = np.linspace(0, 1.0, 1000)
    positions = np.array([spiral.trajectory(s) for s in s_values])
    
    # Check continuity by verifying small steps have small position changes
    diffs = np.diff(positions, axis=0)
    norms = np.linalg.norm(diffs, axis=1)
    
    # Maximum step size (allowing for exponential growth and rotation)
    max_step = np.max(norms)
    
    # Should have smooth growth (check median step vs max step)
    median_step = np.median(norms)
    
    # Max step shouldn't be orders of magnitude larger than median
    assert max_step < 100 * median_step, f"Trajectory has discontinuity: max step {max_step}, median {median_step}"
    
    print(f"  ✓ Trajectory is continuous (max step: {max_step:.6f})")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("EMERGENT NOETIC TIME - TEST SUITE")
    print("=" * 70 + "\n")
    
    tests = [
        test_symbiotic_spiral_creation,
        test_witness_field,
        test_noetic_time_nonnegativity,
        test_noetic_time_monotonicity,
        test_noetic_time_additivity,
        test_fundamental_time_quantum,
        test_coherence_constant_on_spiral,
        test_presence_density_positive,
        test_trajectory_continuity,
        test_visualization_runs,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ FAILED: {e}")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
