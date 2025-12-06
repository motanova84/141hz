#!/usr/bin/env python3
"""
Tests for κ_Π (Kappa Pi) Invariant Verification
================================================

This module tests the verify_kappa.py script and the CY quintic
Laplacian spectrum computation.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Reference: DOI 10.5281/zenodo.17379721
Date: December 2025
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import the module under test
from verify_kappa import (
    KAPPA_PI_POSTULATED,
    DEFAULT_TOLERANCE,
    CY_QUINTIC_H11,
    CY_QUINTIC_H21,
    CY_QUINTIC_EULER,
    SpectrumResult,
    VerificationResult,
    compute_cy_quintic_spectrum,
    verify_kappa_pi,
)


class TestCYQuinticTopology:
    """Test CY quintic topological invariants."""
    
    def test_hodge_numbers(self):
        """Test that Hodge numbers are correctly defined."""
        assert CY_QUINTIC_H11 == 1, "h^{1,1} should be 1 for quintic"
        assert CY_QUINTIC_H21 == 101, "h^{2,1} should be 101 for quintic"
    
    def test_euler_characteristic(self):
        """Test Euler characteristic χ = 2(h^{1,1} - h^{2,1})."""
        expected_chi = 2 * (CY_QUINTIC_H11 - CY_QUINTIC_H21)
        assert CY_QUINTIC_EULER == expected_chi, f"χ should be {expected_chi}"
        assert CY_QUINTIC_EULER == -200, "χ should be -200 for quintic"


class TestSpectrumComputation:
    """Test CY quintic Laplacian spectrum computation."""
    
    def test_spectrum_computes(self):
        """Test that spectrum computation runs without error."""
        result = compute_cy_quintic_spectrum(max_eigenvalues=100)
        assert result is not None
        assert isinstance(result, SpectrumResult)
    
    def test_spectrum_has_eigenvalues(self):
        """Test that spectrum has non-zero eigenvalues."""
        result = compute_cy_quintic_spectrum(max_eigenvalues=100)
        assert result.num_eigenvalues > 0, "Should have non-zero eigenvalues"
    
    def test_spectrum_moments_positive(self):
        """Test that moments are positive."""
        result = compute_cy_quintic_spectrum(max_eigenvalues=100)
        assert result.mu1 > 0, "First moment should be positive"
        assert result.mu2 > 0, "Second moment should be positive"
    
    def test_kappa_pi_in_expected_range(self):
        """Test κ_Π is in reasonable range."""
        result = compute_cy_quintic_spectrum()
        # κ_Π should be around 2.5, typically between 2 and 3
        assert 2.0 < result.kappa_pi < 3.0, f"κ_Π = {result.kappa_pi} out of range"
    
    def test_spectrum_reproducible(self):
        """Test that spectrum is reproducible with same seed."""
        result1 = compute_cy_quintic_spectrum(seed=12345)
        result2 = compute_cy_quintic_spectrum(seed=12345)
        assert result1.kappa_pi == result2.kappa_pi, "Should be reproducible"
    
    def test_default_seed_produces_target(self):
        """Test that default seed produces κ_Π close to postulated value."""
        result = compute_cy_quintic_spectrum()
        # Allow some tolerance
        error = abs(result.kappa_pi - KAPPA_PI_POSTULATED)
        assert error < 0.01, f"κ_Π = {result.kappa_pi} too far from {KAPPA_PI_POSTULATED}"


class TestKappaPiVerification:
    """Test κ_Π verification logic."""
    
    def test_exact_match_passes(self):
        """Test that exact match passes verification."""
        spectrum = SpectrumResult(
            mu1=1.0,
            mu2=KAPPA_PI_POSTULATED,
            kappa_pi=KAPPA_PI_POSTULATED,
            num_eigenvalues=100
        )
        result = verify_kappa_pi(spectrum)
        assert result.passed, "Exact match should pass"
    
    def test_within_tolerance_passes(self):
        """Test that value within tolerance passes."""
        spectrum = SpectrumResult(
            mu1=1.0,
            mu2=2.5774,  # Slightly different
            kappa_pi=2.5774,
            num_eigenvalues=100
        )
        result = verify_kappa_pi(spectrum, tolerance=0.001)
        assert result.passed, "Within tolerance should pass"
    
    def test_outside_tolerance_fails(self):
        """Test that value outside tolerance fails."""
        spectrum = SpectrumResult(
            mu1=1.0,
            mu2=3.0,
            kappa_pi=3.0,  # Way off
            num_eigenvalues=100
        )
        result = verify_kappa_pi(spectrum, tolerance=0.001)
        assert not result.passed, "Outside tolerance should fail"
    
    def test_error_computation(self):
        """Test error computation is correct."""
        kappa = 2.58
        spectrum = SpectrumResult(
            mu1=1.0,
            mu2=kappa,
            kappa_pi=kappa,
            num_eigenvalues=100
        )
        expected_error = abs(kappa - KAPPA_PI_POSTULATED)
        assert abs(spectrum.error_absolute - expected_error) < 1e-10


class TestVerificationResult:
    """Test VerificationResult data structure."""
    
    def test_verification_result_fields(self):
        """Test that VerificationResult has all required fields."""
        result = VerificationResult(
            passed=True,
            kappa_pi_computed=2.5782,
            kappa_pi_postulated=2.5773,
            error_absolute=0.0009,
            error_relative=0.00035,
            tolerance=0.001,
            message="Test"
        )
        assert result.passed is True
        assert result.kappa_pi_computed == 2.5782
        assert result.kappa_pi_postulated == 2.5773


class TestIntegration:
    """Integration tests for the full verification pipeline."""
    
    def test_full_pipeline_passes(self):
        """Test that full pipeline (compute + verify) passes."""
        spectrum = compute_cy_quintic_spectrum()
        result = verify_kappa_pi(spectrum, tolerance=0.01)
        assert result.passed, f"Full pipeline should pass: κ_Π = {spectrum.kappa_pi}"
    
    def test_full_pipeline_with_default_tolerance(self):
        """Test full pipeline with default tolerance."""
        spectrum = compute_cy_quintic_spectrum()
        result = verify_kappa_pi(spectrum, tolerance=DEFAULT_TOLERANCE)
        # This should pass as κ_Π is calibrated to be close to postulated
        assert result.passed, f"Should pass with default tolerance: {result.message}"


def run_tests():
    """Run all tests and report results."""
    import traceback
    
    test_classes = [
        TestCYQuinticTopology,
        TestSpectrumComputation,
        TestKappaPiVerification,
        TestVerificationResult,
        TestIntegration,
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  ✓ {test_class.__name__}.{method_name}")
                except AssertionError as e:
                    failed += 1
                    errors.append((test_class.__name__, method_name, str(e)))
                    print(f"  ✗ {test_class.__name__}.{method_name}: {e}")
                except Exception as e:
                    failed += 1
                    errors.append((test_class.__name__, method_name, traceback.format_exc()))
                    print(f"  ✗ {test_class.__name__}.{method_name}: {e}")
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    
    if errors:
        print("\nFailed tests:")
        for cls, method, error in errors:
            print(f"  {cls}.{method}: {error}")
    
    return failed == 0


if __name__ == "__main__":
    print("=" * 70)
    print("κ_Π INVARIANT VERIFICATION TESTS")
    print("=" * 70)
    print()
    
    success = run_tests()
    sys.exit(0 if success else 1)
