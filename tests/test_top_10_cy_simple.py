#!/usr/bin/env python3
"""
Simple tests for Top 10 Calabi-Yau Varieties Script
(without pytest dependency)
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from top_10_cy_varieties import (
    compute_alpha_beta,
    compute_kappa_pi,
    generate_cy_table,
    CY_DATABASE
)


def test_quintic_alpha_beta():
    """Test α and β for the quintic CY (h¹¹=1, h²¹=101)."""
    alpha, beta = compute_alpha_beta(1, 101)
    
    assert 0.380 <= alpha <= 0.390, f"Alpha {alpha} not in range [0.380, 0.390]"
    assert 0.239 <= beta <= 0.249, f"Beta {beta} not in range [0.239, 0.249]"
    print("✓ test_quintic_alpha_beta passed")


def test_alpha_increases_with_h11():
    """Test that α increases as h¹¹ increases."""
    alpha1, _ = compute_alpha_beta(1, 101)
    alpha2, _ = compute_alpha_beta(5, 65)
    alpha3, _ = compute_alpha_beta(12, 48)
    
    assert alpha1 <= alpha2 <= alpha3, f"Alpha not increasing: {alpha1}, {alpha2}, {alpha3}"
    print("✓ test_alpha_increases_with_h11 passed")


def test_quintic_kappa_pi():
    """Test κ_Π for the quintic CY."""
    alpha, beta = compute_alpha_beta(1, 101)
    kappa_pi = compute_kappa_pi(alpha, beta, 1, 101)
    
    assert 1.650 <= kappa_pi <= 1.670, f"Kappa_pi {kappa_pi} not in range [1.650, 1.670]"
    print("✓ test_quintic_kappa_pi passed")


def test_kappa_pi_decreases_with_alpha():
    """Test that κ_Π decreases as α increases."""
    alpha1, beta1 = compute_alpha_beta(1, 101)
    alpha2, beta2 = compute_alpha_beta(5, 65)
    alpha3, beta3 = compute_alpha_beta(12, 48)
    
    kappa1 = compute_kappa_pi(alpha1, beta1, 1, 101)
    kappa2 = compute_kappa_pi(alpha2, beta2, 5, 65)
    kappa3 = compute_kappa_pi(alpha3, beta3, 12, 48)
    
    assert kappa1 >= kappa2, f"Kappa not decreasing: {kappa1} < {kappa2}"
    assert kappa2 >= kappa3, f"Kappa not decreasing: {kappa2} < {kappa3}"
    print("✓ test_kappa_pi_decreases_with_alpha passed")


def test_generate_top_10():
    """Test generating top 10 varieties."""
    results = generate_cy_table(CY_DATABASE, top_n=10)
    
    assert len(results) == 10, f"Expected 10 results, got {len(results)}"
    assert results[0]["id"] == "CY-001", f"First ID should be CY-001, got {results[0]['id']}"
    assert results[9]["id"] == "CY-010", f"Last ID should be CY-010, got {results[9]['id']}"
    print("✓ test_generate_top_10 passed")


def test_euler_characteristic():
    """Test that χ = 2(h¹¹ - h²¹) for all entries."""
    results = generate_cy_table(CY_DATABASE, top_n=10)
    
    for entry in results:
        expected_chi = 2 * (entry["h11"] - entry["h21"])
        assert entry["chi"] == expected_chi, \
            f"Chi mismatch for {entry['id']}: {entry['chi']} != {expected_chi}"
    print("✓ test_euler_characteristic passed")


def test_database_has_at_least_10():
    """Test that database has at least 10 varieties."""
    assert len(CY_DATABASE) >= 10, f"Database has only {len(CY_DATABASE)} varieties"
    print("✓ test_database_has_at_least_10 passed")


def test_kappa_pi_decreasing_trend():
    """Test that κ_Π generally decreases in the top 10 list."""
    results = generate_cy_table(CY_DATABASE, top_n=10)
    
    kappa_values = [r["kappa_pi"] for r in results]
    
    # Check that the first value is larger than the last
    assert kappa_values[0] >= kappa_values[-1], \
        f"First kappa {kappa_values[0]} < last kappa {kappa_values[-1]}"
    
    # Check that most consecutive pairs show decrease
    decreasing_pairs = sum(1 for i in range(len(kappa_values)-1)
                          if kappa_values[i] >= kappa_values[i+1])
    
    # At least 70% of pairs should show decrease
    expected_min = 0.7 * (len(kappa_values) - 1)
    assert decreasing_pairs >= expected_min, \
        f"Only {decreasing_pairs} decreasing pairs, expected at least {expected_min}"
    print("✓ test_kappa_pi_decreasing_trend passed")


def main():
    """Run all tests."""
    print("=" * 70)
    print("Running tests for Top 10 CY Varieties")
    print("=" * 70)
    print()
    
    tests = [
        test_quintic_alpha_beta,
        test_alpha_increases_with_h11,
        test_quintic_kappa_pi,
        test_kappa_pi_decreases_with_alpha,
        test_generate_top_10,
        test_euler_characteristic,
        test_database_has_at_least_10,
        test_kappa_pi_decreasing_trend,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
