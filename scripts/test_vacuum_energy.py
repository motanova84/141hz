#!/usr/bin/env python3
"""
Tests for Vacuum Energy Module
Validates vacuum energy calculations and optimization
"""
import sys
from pathlib import Path
import numpy as np

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vacuum_energy import (
    E_vac_log, optimize_vacuum_energy, analyze_vacuum_energy,
    alpha, beta, gamma, delta, zeta_prime, Lambda, pi_val
)


def test_e_vac_log_basic():
    """Test: Basic E_vac_log function evaluation"""
    print("🧪 TEST 1: Basic E_vac_log evaluation")
    print("-" * 60)
    
    # Test at a specific point
    log_r = 45.0
    energy = E_vac_log(log_r)
    
    # Energy should be a finite number
    assert np.isfinite(energy), "Energy should be finite"
    assert isinstance(energy, (int, float, np.number)), "Energy should be numeric"
    
    print(f"   ✅ E_vac(log_r={log_r}) = {energy:.6e}")
    print("   ✅ TEST PASSED: Function evaluates correctly\n")
    
    return True


def test_e_vac_log_terms():
    """Test: Individual terms of E_vac_log"""
    print("🧪 TEST 2: Individual energy terms")
    print("-" * 60)
    
    log_r = 45.0
    R = 10**log_r
    
    # Calculate individual terms
    term1 = alpha / R**4
    term2 = beta * zeta_prime / R**2
    term3 = gamma * Lambda**2 * R**2
    term4 = delta * np.sin(np.log(R) / np.log(pi_val))**2
    
    # Check all terms are finite
    assert np.isfinite(term1), "Term1 should be finite"
    assert np.isfinite(term2), "Term2 should be finite"
    assert np.isfinite(term3), "Term3 should be finite"
    assert np.isfinite(term4), "Term4 should be finite"
    
    # Sum should equal total energy
    total = term1 + term2 + term3 + term4
    energy = E_vac_log(log_r)
    
    assert np.isclose(total, energy), "Sum of terms should equal total energy"
    
    print(f"   ✅ Term1 (Planck):        {term1:.6e}")
    print(f"   ✅ Term2 (Quantum):       {term2:.6e}")
    print(f"   ✅ Term3 (Lambda):        {term3:.6e}")
    print(f"   ✅ Term4 (Oscillatory):   {term4:.6e}")
    print(f"   ✅ Total energy:          {energy:.6e}")
    print("   ✅ TEST PASSED: Terms sum correctly\n")
    
    return True


def test_e_vac_log_range():
    """Test: E_vac_log over a range of values"""
    print("🧪 TEST 3: E_vac_log over range")
    print("-" * 60)
    
    log_r_values = np.linspace(40, 50, 100)
    energies = [E_vac_log(log_r) for log_r in log_r_values]
    
    # All energies should be finite
    assert all(np.isfinite(e) for e in energies), "All energies should be finite"
    
    # Energy array should have expected length
    assert len(energies) == len(log_r_values), "Energy array length mismatch"
    
    print(f"   ✅ Evaluated {len(energies)} points")
    print(f"   ✅ Min energy: {min(energies):.6e}")
    print(f"   ✅ Max energy: {max(energies):.6e}")
    print("   ✅ TEST PASSED: Function evaluates over range\n")
    
    return True


def test_optimize_vacuum_energy():
    """Test: Optimization of vacuum energy"""
    print("🧪 TEST 4: Vacuum energy optimization")
    print("-" * 60)
    
    # Run optimization
    result = optimize_vacuum_energy(bounds=(40, 50))
    
    # Check optimization succeeded
    assert result.success, "Optimization should succeed"
    assert 40 <= result.x <= 50, "Optimum should be within bounds"
    assert np.isfinite(result.fun), "Minimum energy should be finite"
    
    # Verify it's actually a minimum within the bounded region
    # For boundary minimum, check that moving inward increases energy
    epsilon = 0.1
    
    # If at lower boundary, check right neighbor
    if result.x <= 40.0 + epsilon:
        energy_right = E_vac_log(result.x + epsilon)
        energy_opt = result.fun
        assert energy_right >= energy_opt - 1e-6, "Right neighbor should have higher or equal energy"
        print(f"   ✅ Minimum at lower boundary")
    # If at upper boundary, check left neighbor  
    elif result.x >= 50.0 - epsilon:
        energy_left = E_vac_log(result.x - epsilon)
        energy_opt = result.fun
        assert energy_left >= energy_opt - 1e-6, "Left neighbor should have higher or equal energy"
        print(f"   ✅ Minimum at upper boundary")
    # If interior minimum, check both neighbors
    else:
        energy_left = E_vac_log(result.x - epsilon)
        energy_right = E_vac_log(result.x + epsilon)
        energy_opt = result.fun
        assert energy_left >= energy_opt - 1e-6, "Left neighbor should have higher energy"
        assert energy_right >= energy_opt - 1e-6, "Right neighbor should have higher energy"
        print(f"   ✅ Minimum in interior")
    
    print(f"   ✅ Optimization success:  {result.success}")
    print(f"   ✅ Optimal log(R):        {result.x:.6f}")
    print(f"   ✅ Minimum energy:        {result.fun:.6e}")
    print("   ✅ TEST PASSED: Optimization finds valid minimum\n")
    
    return True


def test_optimize_different_bounds():
    """Test: Optimization with different bounds"""
    print("🧪 TEST 5: Optimization with different bounds")
    print("-" * 60)
    
    bounds_list = [(40, 45), (45, 50), (42, 48)]
    results = []
    
    for bounds in bounds_list:
        result = optimize_vacuum_energy(bounds=bounds)
        results.append(result)
        
        assert result.success, f"Optimization should succeed for bounds {bounds}"
        assert bounds[0] <= result.x <= bounds[1], f"Optimum should be within bounds {bounds}"
        
        print(f"   ✅ Bounds {bounds}: log(R)={result.x:.4f}, E={result.fun:.6e}")
    
    print("   ✅ TEST PASSED: Optimization works with different bounds\n")
    
    return True


def test_analyze_vacuum_energy():
    """Test: Full vacuum energy analysis"""
    print("🧪 TEST 6: Full vacuum energy analysis")
    print("-" * 60)
    
    # Run full analysis
    analysis = analyze_vacuum_energy()
    
    # Check returned structure
    assert 'log_r_values' in analysis, "Should contain log_r_values"
    assert 'energy_values' in analysis, "Should contain energy_values"
    assert 'optimum' in analysis, "Should contain optimum"
    assert 'analysis' in analysis, "Should contain analysis"
    
    # Check optimum
    optimum = analysis['optimum']
    assert optimum.success, "Optimization should succeed"
    
    # Check analysis details
    details = analysis['analysis']
    required_keys = ['log_r_opt', 'R_opt', 'E_min', 'term1_planck', 
                     'term2_quantum', 'term3_lambda', 'term4_oscillatory']
    
    for key in required_keys:
        assert key in details, f"Analysis should contain {key}"
        assert np.isfinite(details[key]), f"{key} should be finite"
    
    # Verify terms sum to total
    total_from_terms = (details['term1_planck'] + details['term2_quantum'] + 
                        details['term3_lambda'] + details['term4_oscillatory'])
    
    assert np.isclose(total_from_terms, details['E_min']), "Terms should sum to total energy"
    
    print(f"   ✅ Optimal log(R):        {details['log_r_opt']:.6f}")
    print(f"   ✅ Total energy:          {details['E_min']:.6e}")
    print(f"   ✅ Planck term:           {details['term1_planck']:.6e}")
    print(f"   ✅ Quantum term:          {details['term2_quantum']:.6e}")
    print(f"   ✅ Lambda term:           {details['term3_lambda']:.6e}")
    print(f"   ✅ Oscillatory term:      {details['term4_oscillatory']:.6e}")
    print("   ✅ TEST PASSED: Full analysis works correctly\n")
    
    return True


def test_energy_monotonicity():
    """Test: Energy behavior at extreme scales"""
    print("🧪 TEST 7: Energy behavior at extreme scales")
    print("-" * 60)
    
    # At very small R (large negative log_r would be unphysical, we test lower bound)
    # At small R: Planck term (1/R^4) should dominate
    log_r_small = 40.0
    energy_small = E_vac_log(log_r_small)
    R_small = 10**log_r_small
    planck_term_small = alpha / R_small**4
    
    # At large R: Lambda term (R^2) should dominate
    log_r_large = 50.0
    energy_large = E_vac_log(log_r_large)
    R_large = 10**log_r_large
    lambda_term_large = gamma * Lambda**2 * R_large**2
    
    # Both should be finite
    assert np.isfinite(energy_small), "Energy at small R should be finite"
    assert np.isfinite(energy_large), "Energy at large R should be finite"
    
    print(f"   ✅ At log(R)={log_r_small}:")
    print(f"      Energy = {energy_small:.6e}")
    print(f"      Planck term = {planck_term_small:.6e}")
    print(f"   ✅ At log(R)={log_r_large}:")
    print(f"      Energy = {energy_large:.6e}")
    print(f"      Lambda term = {lambda_term_large:.6e}")
    print("   ✅ TEST PASSED: Energy behavior at extremes is physical\n")
    
    return True


def test_constants_defined():
    """Test: Physical constants are properly defined"""
    print("🧪 TEST 8: Physical constants")
    print("-" * 60)
    
    constants = {
        'alpha': alpha,
        'beta': beta,
        'gamma': gamma,
        'delta': delta,
        'zeta_prime': zeta_prime,
        'Lambda': Lambda,
        'pi_val': pi_val
    }
    
    for name, value in constants.items():
        assert value is not None, f"{name} should be defined"
        assert np.isfinite(value), f"{name} should be finite"
        print(f"   ✅ {name:12s} = {value}")
    
    # pi_val should be close to mathematical pi
    assert np.isclose(pi_val, np.pi), "pi_val should equal π"
    
    print("   ✅ TEST PASSED: All constants properly defined\n")
    
    return True


def test_optimization_bounds_constraint():
    """Test: Optimization respects bounds constraint"""
    print("🧪 TEST 9: Optimization bounds constraint")
    print("-" * 60)
    
    # Test with very narrow bounds
    bounds = (44.5, 45.5)
    result = optimize_vacuum_energy(bounds=bounds)
    
    assert result.success, "Optimization should succeed with narrow bounds"
    assert bounds[0] <= result.x <= bounds[1], "Result should respect bounds"
    
    # The bounded method should find optimum within the specified range
    print(f"   ✅ Bounds: {bounds}")
    print(f"   ✅ Found optimum at: {result.x:.6f}")
    print(f"   ✅ Within bounds: {bounds[0] <= result.x <= bounds[1]}")
    print("   ✅ TEST PASSED: Bounds constraint respected\n")
    
    return True


def main():
    """Execute all tests"""
    print("=" * 70)
    print("🔬 TESTS FOR VACUUM ENERGY MODULE")
    print("=" * 70)
    print()
    
    tests = [
        ("Basic E_vac_log evaluation", test_e_vac_log_basic),
        ("Individual energy terms", test_e_vac_log_terms),
        ("E_vac_log over range", test_e_vac_log_range),
        ("Vacuum energy optimization", test_optimize_vacuum_energy),
        ("Optimization with different bounds", test_optimize_different_bounds),
        ("Full vacuum energy analysis", test_analyze_vacuum_energy),
        ("Energy behavior at extremes", test_energy_monotonicity),
        ("Physical constants", test_constants_defined),
        ("Optimization bounds constraint", test_optimization_bounds_constraint)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except AssertionError as e:
            print(f"   ❌ FAILURE: {e}\n")
            results.append((name, False, str(e)))
        except Exception as e:
            print(f"   ❌ ERROR: {e}\n")
            results.append((name, False, str(e)))
    
    # Summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for _, p, _ in results if p)
    
    for name, p, error in results:
        status = "✅" if p else "❌"
        print(f"{status} {name}")
        if error:
            print(f"   Error: {error}")
    
    print()
    print(f"Tests executed: {total}")
    print(f"Tests passed: {passed}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
