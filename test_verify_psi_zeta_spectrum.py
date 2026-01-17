#!/usr/bin/env python3
"""
Test suite for verify_psi_zeta_spectrum.py

Tests the spectral verification of Ψ = I⋅A²⋅C^∞ ⊗ ζ(½+i⋅t)
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from verify_psi_zeta_spectrum import (
    ZetaCriticalLine,
    PsiZetaOperator
)


def test_zeta_critical_line():
    """Test Riemann zeta function evaluation on critical line."""
    print("Testing ZetaCriticalLine...")
    
    # Test at a non-zero point
    t = 20.0
    zeta_val = ZetaCriticalLine.evaluate(t, precision=30)
    
    assert isinstance(zeta_val, complex), "Zeta should return complex value"
    assert abs(zeta_val) > 0, "Zeta at t=20 should be non-zero"
    print(f"  ζ(1/2 + 20i) = {zeta_val.real:.6f} + {zeta_val.imag:.6f}i ✓")
    
    # Test at first Riemann zero
    t_zero = 14.134725
    zeta_zero = ZetaCriticalLine.evaluate(t_zero, precision=30)
    
    assert abs(zeta_zero) < 1e-5, f"Zeta at first zero should be ~0, got {abs(zeta_zero)}"
    print(f"  ζ(1/2 + 14.134725i) ≈ 0 ✓")
    
    # Test zeros list
    zeros = ZetaCriticalLine.get_zeros(max_t=100.0, limit=10)
    
    assert len(zeros) == 10, f"Should get 10 zeros, got {len(zeros)}"
    assert zeros[0] == 14.134725, "First zero should be correct"
    print(f"  Got {len(zeros)} Riemann zeros ✓")
    
    print("✅ ZetaCriticalLine tests passed\n")


def test_psi_zeta_operator_initialization():
    """Test operator initialization."""
    print("Testing PsiZetaOperator initialization...")
    
    op = PsiZetaOperator(grid_size=50, domain_size=10.0, t_zeta=20.0)
    
    assert op.grid_size == 50
    assert op.domain_size == 10.0
    assert op.t_zeta == 20.0
    assert len(op.x) == 50
    print(f"  Grid size: {op.grid_size} ✓")
    print(f"  Domain size: {op.domain_size} ✓")
    
    print("✅ Operator initialization tests passed\n")


def test_potential_components():
    """Test potential computation."""
    print("Testing potential components...")
    
    op = PsiZetaOperator(grid_size=50)
    
    # Test Laplacian
    laplacian = op.compute_laplacian_matrix()
    assert laplacian.shape == (50, 50), "Laplacian should be NxN matrix"
    print(f"  Laplacian shape: {laplacian.shape} ✓")
    
    # Test noetic potential
    V_psi = op.compute_noetic_potential()
    assert len(V_psi) == 50, "Potential should have N points"
    assert V_psi.min() >= 0, "Potential should be non-negative (harmonic well)"
    print(f"  Noetic potential range: [{V_psi.min():.6f}, {V_psi.max():.6f}] ✓")
    
    # Test zeta modulation
    zeta_mod = op.compute_zeta_modulation()
    assert len(zeta_mod) == 50, "Zeta modulation should have N points"
    print(f"  Zeta modulation range: [{zeta_mod.min():.6f}, {zeta_mod.max():.6f}] ✓")
    
    print("✅ Potential component tests passed\n")


def test_hamiltonian_spectrum():
    """Test Hamiltonian and spectrum computation."""
    print("Testing Hamiltonian spectrum...")
    
    op = PsiZetaOperator(grid_size=50)
    
    # Build Hamiltonian
    H = op.build_hamiltonian()
    assert H.shape == (50, 50), "Hamiltonian should be NxN"
    
    # Check Hermiticity
    is_hermitian = np.allclose(H, H.T)
    assert is_hermitian, "Hamiltonian should be symmetric (Hermitian for real values)"
    print(f"  Hamiltonian is Hermitian ✓")
    
    # Compute spectrum
    eigenvalues, eigenvectors = op.compute_spectrum(n_eigenvalues=10)
    
    assert len(eigenvalues) == 10, "Should get 10 eigenvalues"
    assert all(eigenvalues[i] <= eigenvalues[i+1] for i in range(9)), "Eigenvalues should be ordered"
    assert eigenvalues[0] > 0, "Ground state should have positive energy"
    
    print(f"  Ground state λ₀ = {eigenvalues[0]:.10f} ✓")
    print(f"  First excited λ₁ = {eigenvalues[1]:.10f} ✓")
    print(f"  Spectral gap Δλ = {eigenvalues[1] - eigenvalues[0]:.10f} ✓")
    
    # Check eigenvector normalization
    psi_0 = eigenvectors[:, 0]
    norm = np.linalg.norm(psi_0)
    assert abs(norm - 1.0) < 1e-10, f"Ground state should be normalized, got norm={norm}"
    print(f"  Ground state normalized: ||ψ₀|| = {norm:.10f} ✓")
    
    print("✅ Hamiltonian spectrum tests passed\n")


def test_spectral_verification():
    """Test complete spectral verification."""
    print("Testing spectral verification...")
    
    op = PsiZetaOperator(grid_size=100, t_zeta=20.0)
    
    results = op.verify_spectral_structure()
    
    # Check required fields
    required_fields = [
        'lambda_0', 'C_derived', 'eigenvalues', 'spectral_gaps',
        't_zeta', 'zeta_value', 'riemann_zeros'
    ]
    
    for field in required_fields:
        assert field in results, f"Results should contain '{field}'"
    
    print(f"  All required fields present ✓")
    print(f"  λ₀ = {results['lambda_0']:.10f}")
    print(f"  C = {results['C_derived']:.6f}")
    print(f"  |ζ(1/2+20i)| = {results['zeta_value']['magnitude']:.6f}")
    print(f"  Number of eigenvalues: {len(results['eigenvalues'])}")
    print(f"  Number of Riemann zeros: {len(results['riemann_zeros'])}")
    
    print("✅ Spectral verification tests passed\n")


def test_tensor_product_analysis():
    """Test tensor product analysis."""
    print("Testing tensor product analysis...")
    
    op = PsiZetaOperator(grid_size=100, t_zeta=20.0)
    
    results = op.tensor_product_analysis()
    
    # Check required fields
    required_fields = [
        'psi_norm', 'A_squared', 'information_entropy',
        'tensor_product_norm', 'coupling_strength', 'formula'
    ]
    
    for field in required_fields:
        assert field in results, f"Results should contain '{field}'"
    
    # Check physical constraints
    assert abs(results['psi_norm'] - 1.0) < 1e-10, "Wavefunction should be normalized"
    assert results['A_squared'] > 0, "Effective area should be positive"
    assert results['information_entropy'] > 0, "Entropy should be positive"
    assert results['coupling_strength'] >= 0, "Coupling should be non-negative"
    
    print(f"  ||Ψ|| = {results['psi_norm']:.10f} ✓")
    print(f"  A² = {results['A_squared']:.6f} ✓")
    print(f"  H(I) = {results['information_entropy']:.6f} ✓")
    print(f"  Coupling = {results['coupling_strength']:.6f} ✓")
    print(f"  Formula: {results['formula']} ✓")
    
    print("✅ Tensor product analysis tests passed\n")


def test_zeta_at_different_t_values():
    """Test behavior at different t values including zeros."""
    print("Testing zeta function at different t values...")
    
    # Test at several points
    test_points = [
        (0.0, "t=0 (on real axis)", False),
        (10.0, "t=10 (away from zeros)", False),
        (14.134725, "t=14.134725 (first zero)", True),
        (21.022040, "t=21.022040 (second zero)", True),
        (30.0, "t=30 (between zeros)", False)
    ]
    
    for t, description, is_zero in test_points:
        op = PsiZetaOperator(grid_size=50, t_zeta=t)
        results = op.verify_spectral_structure()
        
        zeta_mag = results['zeta_value']['magnitude']
        print(f"  {description}: |ζ| = {zeta_mag:.6f}", end="")
        
        # Zeros should have magnitude close to 0
        if is_zero:
            assert zeta_mag < 1e-3, f"Should be near zero, got {zeta_mag}"
            print(" (zero) ✓")
        else:
            print(" ✓")
    
    print("✅ Multi-t value tests passed\n")


def run_all_tests():
    """Run all test suites."""
    print("=" * 70)
    print("🧪 Running Test Suite: verify_psi_zeta_spectrum.py")
    print("=" * 70)
    print()
    
    tests = [
        test_zeta_critical_line,
        test_psi_zeta_operator_initialization,
        test_potential_components,
        test_hamiltonian_spectrum,
        test_spectral_verification,
        test_tensor_product_analysis,
        test_zeta_at_different_t_values
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {test.__name__}")
            print(f"   Exception: {e}\n")
            failed += 1
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
