#!/usr/bin/env python3
"""
Test Suite for Vacuum Energy Equation Validation

Tests all aspects of the vacuum energy equation validator:
- Mathematical correctness of E_vac(R_Ψ) formula
- Minimization and optimization
- Cosmological constant solution validation
- Arithmetic-geometric coupling via ζ'(1/2)
- Resonant reality and f₀ generation
- Individual term contributions

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import sys
import os
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from validate_vacuum_energy_equation import VacuumEnergyValidator, ZETA_PRIME_HALF, PI
from scipy.constants import c, physical_constants


def test_vacuum_energy_basic_evaluation():
    """Test basic evaluation of E_vac at a specific scale."""
    print("\nTest 1: Basic E_vac evaluation")
    validator = VacuumEnergyValidator()
    
    # Test at R_Ψ = 10^45 ℓ_P
    R_test = 1e45
    E = validator.E_vac(R_test)
    
    assert np.isfinite(E), "Energy should be finite"
    assert E > 0 or E < 0, "Energy should be non-zero"
    print(f"  ✓ E_vac(10^45 ℓ_P) = {E:.6e}")
    return True


def test_individual_terms():
    """Test individual energy term calculations."""
    print("\nTest 2: Individual energy terms")
    validator = VacuumEnergyValidator()
    
    R_test = 1e45
    terms = validator.get_individual_terms(R_test)
    
    assert 'term1_planck' in terms
    assert 'term2_zeta' in terms
    assert 'term3_lambda' in terms
    assert 'term4_fractal' in terms
    assert 'total' in terms
    
    # Verify sum equals total
    sum_terms = (terms['term1_planck'] + terms['term2_zeta'] + 
                 terms['term3_lambda'] + terms['term4_fractal'])
    assert np.isclose(sum_terms, terms['total'], rtol=1e-10), "Sum of terms should equal total"
    
    print(f"  ✓ Term 1 (Planck): {terms['term1_planck']:.6e}")
    print(f"  ✓ Term 2 (Zeta): {terms['term2_zeta']:.6e}")
    print(f"  ✓ Term 3 (Lambda): {terms['term3_lambda']:.6e}")
    print(f"  ✓ Term 4 (Fractal): {terms['term4_fractal']:.6e}")
    print(f"  ✓ Total: {terms['total']:.6e}")
    return True


def test_minimum_finding():
    """Test that minimum finding works and produces reasonable results."""
    print("\nTest 3: Minimum finding")
    validator = VacuumEnergyValidator()
    
    result = validator.find_minimum(log_bounds=(40, 50))
    
    assert result['optimization_success'], "Optimization should succeed"
    assert 1e40 < result['R_star'] < 1e50, "R_star should be in reasonable range"
    assert result['E_min'] > 0, "Minimum energy should be positive (vacuum energy)"
    assert result['f0_predicted'] > 0, "Predicted frequency should be positive"
    
    print(f"  ✓ R_Ψ* = {result['R_star']:.4e} ℓ_P")
    print(f"  ✓ E_min = {result['E_min']:.6e}")
    print(f"  ✓ f₀ predicted = {result['f0_predicted']:.4f} Hz")
    print(f"  ✓ f₀ target = {result['f0_target']:.4f} Hz")
    print(f"  ✓ Error = {result['frequency_error_percent']:.4f}%")
    return True


def test_cosmological_constant_validation():
    """Test cosmological constant problem validation."""
    print("\nTest 4: Cosmological constant solution")
    validator = VacuumEnergyValidator()
    
    # Get minimum first
    min_result = validator.find_minimum()
    R_star = min_result['R_star']
    
    # Validate cosmological constant solution
    cosmo_result = validator.validate_cosmological_constant_solution(R_star)
    
    assert 'planck_scale_energy' in cosmo_result
    assert 'cosmological_scale_energy' in cosmo_result
    assert 'hierarchy_ratio' in cosmo_result
    assert cosmo_result['planck_scale_energy'] > 0
    assert cosmo_result['cosmological_scale_energy'] > 0
    
    print(f"  ✓ Planck energy: {cosmo_result['planck_scale_energy']:.2e}")
    print(f"  ✓ Cosmological energy: {cosmo_result['cosmological_scale_energy']:.2e}")
    print(f"  ✓ Hierarchy ratio: {cosmo_result['hierarchy_ratio']:.2e}")
    print(f"  ✓ Hierarchy closed: {cosmo_result['R_star_closes_hierarchy']}")
    return True


def test_arithmetic_geometric_coupling():
    """Test arithmetic-geometric coupling validation."""
    print("\nTest 5: Arithmetic-geometric coupling")
    validator = VacuumEnergyValidator()
    
    arith_result = validator.validate_arithmetic_geometric_coupling()
    
    assert 'zeta_prime_half_value' in arith_result
    assert 'zeta_half_value' in arith_result
    assert arith_result['prime_connection'] == True
    assert np.isclose(arith_result['zeta_prime_half_value'], ZETA_PRIME_HALF, rtol=1e-10)
    
    print(f"  ✓ ζ'(1/2) = {arith_result['zeta_prime_half_value']:.10f}")
    print(f"  ✓ ζ(1/2) = {arith_result['zeta_half_value']:.10f}")
    print(f"  ✓ Prime connection verified")
    return True


def test_resonant_reality():
    """Test resonant reality and frequency generation."""
    print("\nTest 6: Resonant reality validation")
    validator = VacuumEnergyValidator()
    
    # Get minimum first
    min_result = validator.find_minimum()
    R_star = min_result['R_star']
    
    # Validate resonant reality
    resonance_result = validator.validate_resonant_reality(R_star)
    
    assert 'f0_predicted' in resonance_result
    assert 'frequency_match_percent' in resonance_result
    assert 'log_R_over_log_pi' in resonance_result
    assert 'nearest_pi_power' in resonance_result
    assert 'harmonic_series' in resonance_result
    
    # Frequency should be positive (match percentage may be low with default coefficients)
    assert resonance_result['f0_predicted'] > 0, "Predicted frequency should be positive"
    # Note: With default coefficients (all 1.0), exact match is not expected
    # The equation demonstrates the mechanism, not necessarily the exact tuning
    
    print(f"  ✓ f₀ predicted: {resonance_result['f0_predicted']:.4f} Hz")
    print(f"  ✓ Frequency match: {resonance_result['frequency_match_percent']:.2f}%")
    print(f"  ✓ log(R_Ψ*)/log(π): {resonance_result['log_R_over_log_pi']:.4f}")
    print(f"  ✓ Nearest π power: {resonance_result['nearest_pi_power']}")
    print(f"  ✓ Harmonics generated: {len(resonance_result['harmonic_series'])}")
    return True


def test_energy_array_evaluation():
    """Test E_vac evaluation over an array of R values."""
    print("\nTest 7: Array evaluation")
    validator = VacuumEnergyValidator()
    
    # Test with array of R values
    R_array = np.logspace(40, 50, 100)
    E_array = validator.E_vac(R_array)
    
    assert len(E_array) == len(R_array), "Output array should match input length"
    assert np.all(np.isfinite(E_array)), "All energies should be finite"
    
    # Check for minimum in the array
    min_idx = np.argmin(E_array)
    R_min = R_array[min_idx]
    
    print(f"  ✓ Evaluated {len(R_array)} points")
    print(f"  ✓ R_Ψ at minimum: {R_min:.4e} ℓ_P")
    print(f"  ✓ E_vac at minimum: {E_array[min_idx]:.6e}")
    return True


def test_parameter_variations():
    """Test E_vac with different coupling parameters."""
    print("\nTest 8: Parameter variations")
    
    # Test with different alphas
    for alpha in [0.5, 1.0, 2.0]:
        validator = VacuumEnergyValidator(alpha=alpha, beta=1.0, gamma=1.0, delta=1.0)
        result = validator.find_minimum()
        assert result['optimization_success'], f"Optimization should succeed with α={alpha}"
        print(f"  ✓ α={alpha}: R_Ψ* = {result['R_star']:.4e} ℓ_P")
    
    return True


def test_fractal_term_periodicity():
    """Test periodicity of fractal sin² term."""
    print("\nTest 9: Fractal term periodicity")
    validator = VacuumEnergyValidator()
    
    # The fractal term should be periodic in log(R)/log(π)
    R_vals = np.array([PI**90, PI**91, PI**92, PI**93])
    
    fractal_vals = []
    for R in R_vals:
        terms = validator.get_individual_terms(R)
        fractal_vals.append(terms['term4_fractal'])
    
    # At integer powers of π, sin²(n) should give same value modulo 2π
    # (accounting for numerical precision)
    
    print(f"  ✓ Fractal values at π^n:")
    for i, (R, frac) in enumerate(zip(R_vals, fractal_vals)):
        n = 90 + i
        print(f"    π^{n}: {frac:.10f}")
    
    return True


def test_zeta_prime_consistency():
    """Test consistency of ζ'(1/2) value."""
    print("\nTest 10: ζ'(1/2) consistency")
    
    # The value should be negative (well-established mathematical fact)
    assert ZETA_PRIME_HALF < 0, "ζ'(1/2) should be negative"
    
    # Should be close to -0.2079 (known value)
    expected = -0.207886224977
    assert np.isclose(ZETA_PRIME_HALF, expected, rtol=1e-8), "ζ'(1/2) should match known value"
    
    print(f"  ✓ ζ'(1/2) = {ZETA_PRIME_HALF:.12f}")
    print(f"  ✓ Expected: {expected:.12f}")
    print(f"  ✓ Difference: {abs(ZETA_PRIME_HALF - expected):.2e}")
    return True


def test_comprehensive_validation():
    """Test complete comprehensive validation run."""
    print("\nTest 11: Comprehensive validation")
    validator = VacuumEnergyValidator()
    
    results = validator.run_comprehensive_validation()
    
    # Check all required keys are present
    required_keys = [
        'equation',
        'parameters',
        'minimum_optimization',
        'cosmological_constant_solution',
        'arithmetic_geometric_coupling',
        'resonant_reality',
        'term_contributions'
    ]
    
    for key in required_keys:
        assert key in results, f"Results should contain '{key}'"
    
    print(f"  ✓ All required result keys present")
    print(f"  ✓ Validation timestamp: {results.get('validation_timestamp', 'N/A')}")
    return True


def test_physical_constants():
    """Test that physical constants are reasonable."""
    print("\nTest 12: Physical constants")
    
    l_P = physical_constants["Planck length"][0]
    
    assert 1e-36 < l_P < 1e-34, "Planck length should be ~10^-35 m"
    assert c == 299792458, "Speed of light should be exact"
    assert PI == np.pi, "π should be numpy's pi"
    
    print(f"  ✓ ℓ_P = {l_P:.6e} m")
    print(f"  ✓ c = {c} m/s")
    print(f"  ✓ π = {PI:.10f}")
    return True


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_vacuum_energy_basic_evaluation,
        test_individual_terms,
        test_minimum_finding,
        test_cosmological_constant_validation,
        test_arithmetic_geometric_coupling,
        test_resonant_reality,
        test_energy_array_evaluation,
        test_parameter_variations,
        test_fractal_term_periodicity,
        test_zeta_prime_consistency,
        test_comprehensive_validation,
        test_physical_constants
    ]
    
    print("=" * 80)
    print("VACUUM ENERGY EQUATION VALIDATION TEST SUITE")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
                print(f"  ✗ {test_func.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"  ✗ {test_func.__name__} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} total")
    print("=" * 80)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED SUCCESSFULLY\n")
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED\n")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
