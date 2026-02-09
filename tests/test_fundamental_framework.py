#!/usr/bin/env python3
"""
Test for QCAL ∞³ Fundamental Framework Validation

This test ensures that the fundamental framework validation script
runs successfully and all validations pass.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 9 de febrero de 2026
Framework: QCAL ∞³
"""

import sys
import os
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_fundamental_framework_validation():
    """Test that the fundamental framework validation passes"""
    
    # Run the validation script
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'scripts',
        'validate_fundamental_framework.py'
    )
    
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    
    # Check that it exited successfully
    assert result.returncode == 0, f"Validation script failed:\n{result.stdout}\n{result.stderr}"
    
    # Check for success message in output
    assert "MARCO FUNDAMENTAL QCAL ∞³ VALIDADO CORRECTAMENTE" in result.stdout, \
        "Success message not found in output"
    
    # Check that all validations passed
    assert "Total: 6/6 validaciones pasadas" in result.stdout, \
        "Not all validations passed"
    
    print("✅ Fundamental framework validation test PASSED")
    return True


def test_f0_constant():
    """Test that f₀ = 141.7001 Hz exactly"""
    from qcal.constants import F0_HZ
    
    expected = 141.7001
    assert abs(F0_HZ - expected) < 1e-10, \
        f"F0_HZ = {F0_HZ}, expected {expected}"
    
    print(f"✅ f₀ = {F0_HZ} Hz")
    return True


def test_kappa_pi_constant():
    """Test that κ_Π ≈ 2.5773"""
    from qcal.constants import KAPPA_PI
    
    expected = 2.5773
    assert abs(KAPPA_PI - expected) < 1e-4, \
        f"KAPPA_PI = {KAPPA_PI}, expected {expected}"
    
    print(f"✅ κ_Π = {KAPPA_PI}")
    return True


def test_lambda_g_constant():
    """Test that Λ_G ≈ 1/491.7 Hz"""
    from src.fiber_bundles.consciousness_intersection import IntersectionConstant
    
    alpha = 1.0 / 137.036
    delta_zeta = 0.2787
    const = IntersectionConstant(alpha=alpha, delta_zeta=delta_zeta)
    
    expected_inverse = 491.5  # From problem statement
    tolerance = 1.0  # Hz^-1
    
    assert abs(const.lambda_G_inverse - expected_inverse) < tolerance, \
        f"1/Λ_G = {const.lambda_G_inverse}, expected ≈ {expected_inverse}"
    
    print(f"✅ Λ_G = {const.lambda_G:.10f} Hz (1/Λ_G ≈ {const.lambda_G_inverse:.2f})")
    return True


def test_canonical_field():
    """Test canonical consciousness field"""
    from src.canonical_consciousness_field import CanonicalConsciousnessField
    
    field = CanonicalConsciousnessField()
    
    # Check f₀
    assert abs(float(field.F0) - 141.7001) < 1e-10, \
        f"Field F0 = {float(field.F0)}, expected 141.7001"
    
    # Check that derived properties are computed
    assert float(field.E_PSI) > 0, "E_PSI should be positive"
    assert float(field.LAMBDA_PSI_KM) > 0, "LAMBDA_PSI_KM should be positive"
    
    print(f"✅ Canonical field F0 = {float(field.F0)} Hz")
    print(f"   E_Ψ = {float(field.E_PSI):.4e} J")
    print(f"   λ_Ψ = {float(field.LAMBDA_PSI_KM):.3f} km")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 Testing QCAL ∞³ Fundamental Framework")
    print("="*70 + "\n")
    
    tests = [
        ("F0 Constant", test_f0_constant),
        ("Kappa Pi Constant", test_kappa_pi_constant),
        ("Lambda G Constant", test_lambda_g_constant),
        ("Canonical Field", test_canonical_field),
        ("Framework Validation Script", test_fundamental_framework_validation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            print(f"\nTesting {name}...")
            result = test_func()
            results.append((name, True))
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 Test Summary")
    print("="*70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if all(r for _, r in results):
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
