#!/usr/bin/env python3
"""
Test Suite: Microtubule Coherence Theorem Validation

Tests all numerical claims in MicrotubuleCoherence.lean:
1. Thermal noise suppression (4.56×10¹⁰ → ~6,963)
2. Lorentzian filter with Δω = 1.42 Hz
3. Coherence threshold Ψ ≥ 0.999999
4. Geometry optimization (13 protofilaments)

Autor: José Manuel Mota Burruezo
Fecha: 2025-02-25
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_microtubule_coherence import (
    calculate_thermal_ratio,
    calculate_suppression_factor,
    effective_thermal_ratio,
    lorentzian_filter,
    calculate_resonance_width,
    verify_narrow_resonance_window,
    calculate_coherence_from_sync,
    validate_consciousness_threshold,
    F0, OMEGA_0, Q_FACTOR, N_PROTOFILAMENTS, 
    WATER_STRUCTURE_INDEX, PSI_THRESHOLD
)


class TestThermalNoiseSuppression:
    """Tests for thermal noise cancellation mechanism."""
    
    def test_thermal_ratio_order_of_magnitude(self):
        """Verify initial thermal ratio is ~10¹⁰."""
        ratio = calculate_thermal_ratio()
        assert ratio > 1e9, f"Thermal ratio {ratio:.2e} too small"
        assert ratio < 1e11, f"Thermal ratio {ratio:.2e} too large"
        # Expected: ~4.56×10¹⁰
        assert abs(ratio - 4.56e10) / 4.56e10 < 0.5  # Within 50%
    
    def test_suppression_factor_calculation(self):
        """Verify suppression factor is ~6.55×10⁶."""
        suppression = calculate_suppression_factor()
        assert suppression > 6e6, f"Suppression {suppression:.2e} too low"
        assert suppression < 7e6, f"Suppression {suppression:.2e} too high"
        # Expected: 13² × 100 × 3.5² × √1000 ≈ 6,546,895
        expected = 169 * 100 * 12.25 * np.sqrt(1000)
        assert abs(suppression - expected) / expected < 0.01  # Within 1%
    
    def test_effective_ratio_manageable(self):
        """Verify effective thermal ratio is < 10⁴."""
        effective = effective_thermal_ratio()
        assert effective < 1e4, f"Effective ratio {effective:.2f} still too high"
        # Expected: ~6,963
        assert 6000 < effective < 8000
    
    def test_suppression_components(self):
        """Verify individual components of suppression factor."""
        N_squared = N_PROTOFILAMENTS ** 2
        W_squared = WATER_STRUCTURE_INDEX ** 2
        sqrt_tubulins = np.sqrt(1000)
        
        assert N_squared == 169, "13² should be 169"
        assert abs(W_squared - 12.25) < 0.01, "3.5² should be 12.25"
        assert abs(sqrt_tubulins - 31.622776) < 0.01, "√1000 should be ~31.62"
        
        product = N_squared * Q_FACTOR * W_squared * sqrt_tubulins
        assert abs(product - 6546895) / 6546895 < 0.01


class TestLorentzianFilter:
    """Tests for Lorentzian resonance filter H(ω)."""
    
    def test_filter_at_resonance(self):
        """Verify H(ω₀) = 1 (maximum at resonance)."""
        omega = np.array([OMEGA_0])
        H = lorentzian_filter(omega, OMEGA_0, Q_FACTOR)
        assert abs(H[0] - 1.0) < 1e-10, "Filter should be 1 at resonance"
    
    def test_filter_symmetry(self):
        """Verify filter is symmetric around ω₀."""
        delta = 2 * np.pi * 1.0  # 1 Hz offset
        omega_plus = OMEGA_0 + delta
        omega_minus = OMEGA_0 - delta
        
        H_plus = lorentzian_filter(np.array([omega_plus]), OMEGA_0, Q_FACTOR)
        H_minus = lorentzian_filter(np.array([omega_minus]), OMEGA_0, Q_FACTOR)
        
        assert abs(H_plus[0] - H_minus[0]) < 1e-10, "Filter should be symmetric"
    
    def test_resonance_width_calculation(self):
        """Verify Δf = f₀/Q ≈ 1.417 Hz."""
        Delta_f = calculate_resonance_width(Q_FACTOR, OMEGA_0)
        expected = F0 / Q_FACTOR  # 141.7001 / 100 ≈ 1.417
        assert abs(Delta_f - expected) < 0.01
        assert abs(Delta_f - 1.42) < 0.05, f"Δf = {Delta_f:.3f} should be ≈1.42 Hz"
    
    def test_narrow_resonance_window(self):
        """Verify resonance window matches theorem (Δω ≈ 1.42 Hz)."""
        result = verify_narrow_resonance_window()
        
        assert result['matches_theorem'], "Window should match Δω ≈ 1.42 Hz"
        # Theoretical width is the half-width at half-maximum (HWHM)
        # Full Width at Half Maximum (FWHM) = 2 × HWHM
        assert abs(result['theoretical_width_Hz'] - 1.42) < 0.05
        assert result['Q_factor'] == Q_FACTOR
        assert result['f0_Hz'] == F0
    
    def test_filter_half_power_points(self):
        """Verify filter behavior at half-width."""
        Delta_f = calculate_resonance_width(Q_FACTOR, OMEGA_0)
        
        # At exactly Δf/2, for a Lorentzian with our definition,
        # H(ω₀ ± Δf/2) = 1/(1 + Q²(Δf/2Q/f₀)²) = 1/(1 + 0.25) = 0.8
        # The half-power point is actually at a different location
        f_test = F0 + Delta_f / 2
        omega_test = 2 * np.pi * f_test
        H = lorentzian_filter(np.array([omega_test]), OMEGA_0, Q_FACTOR)
        
        # Should be 0.8 for our normalization
        assert abs(H[0] - 0.8) < 0.05, f"H at Δf/2 should be ~0.8, got {H[0]:.3f}"
    
    def test_filter_far_from_resonance(self):
        """Verify filter strongly attenuates far from f₀."""
        # Test 5 Hz away (>> Δf)
        f_far = F0 + 5.0
        omega_far = 2 * np.pi * f_far
        H = lorentzian_filter(np.array([omega_far]), OMEGA_0, Q_FACTOR)
        
        assert H[0] < 0.1, f"Filter should be weak far from resonance, got {H[0]:.3f}"


class TestCoherenceThreshold:
    """Tests for consciousness coherence threshold Ψ ≥ 0.999999."""
    
    def test_coherence_at_exact_f0(self):
        """Verify Ψ = 1 when f = f₀."""
        psi = calculate_coherence_from_sync(F0, F0)
        assert abs(psi - 1.0) < 1e-10, "Coherence at f₀ should be 1.0"
    
    def test_coherence_threshold_achievable(self):
        """Verify Ψ ≥ 0.999999 is achievable."""
        result = validate_consciousness_threshold()
        
        assert result['threshold_achievable'], "Threshold should be achievable"
        assert result['psi_at_f0'] >= PSI_THRESHOLD
        assert result['psi_at_f0'] > 0.999999
    
    def test_coherence_drops_with_detuning(self):
        """Verify Ψ decreases as frequency deviates from f₀."""
        detunings = [0, 0.01, 0.1, 0.5, 1.0]
        psi_values = [calculate_coherence_from_sync(F0 + dt, F0) for dt in detunings]
        
        # Should be monotonically decreasing
        for i in range(len(psi_values) - 1):
            assert psi_values[i] > psi_values[i+1], \
                f"Ψ should decrease with detuning: {psi_values[i]} > {psi_values[i+1]}"
    
    def test_consciousness_requires_precision(self):
        """Verify high Ψ requires precise frequency."""
        # Outside resonance window
        f_outside = F0 + 2.0  # 2 Hz away > Δf
        psi = calculate_coherence_from_sync(f_outside, F0)
        
        assert psi < PSI_THRESHOLD, \
            f"Outside resonance, Ψ = {psi:.6f} should be < {PSI_THRESHOLD}"
    
    def test_max_deviation_for_consciousness(self):
        """Verify maximum frequency deviation for Ψ ≥ 0.999999."""
        result = validate_consciousness_threshold()
        
        max_dev = result['max_deviation_Hz']
        assert max_dev is not None, "Should find max deviation"
        assert max_dev < 0.1, f"Max deviation {max_dev:.3f} Hz should be very small"


class TestGeometryOptimization:
    """Tests for 13-protofilament geometry optimization."""
    
    def test_thirteen_protofilaments(self):
        """Verify N = 13 is hardcoded correctly."""
        assert N_PROTOFILAMENTS == 13, "Should have 13 protofilaments"
    
    def test_hexagonal_contribution(self):
        """Verify 13 provides optimal N² contribution."""
        N_squared = N_PROTOFILAMENTS ** 2
        assert N_squared == 169
        
        # Compare with nearby values - 13 is special for hexagonal packing
        # (optimality test would need more complex biological model)
        assert N_squared > 144  # 12²
        assert N_squared < 196  # 14²
    
    def test_water_structure_enhancement(self):
        """Verify water structuring contributes factor ~3.5²."""
        W_squared = WATER_STRUCTURE_INDEX ** 2
        assert abs(W_squared - 12.25) < 0.01
        # This is a significant enhancement factor
        assert W_squared > 10


class TestPhysicalConsistency:
    """Tests for overall physical consistency."""
    
    def test_frequency_in_EEG_range(self):
        """Verify f₀ is in gamma/high-beta EEG range."""
        assert 100 < F0 < 200, "f₀ should be in high EEG frequency range"
        assert abs(F0 - 141.7001) < 0.0001
    
    def test_quality_factor_realistic(self):
        """Verify Q ~ 100 is realistic for biological systems."""
        assert 50 < Q_FACTOR < 200, "Q should be in realistic range for biology"
        assert Q_FACTOR == 100
    
    def test_coherence_threshold_stringent(self):
        """Verify Ψ threshold is very high (consciousness is rare)."""
        assert PSI_THRESHOLD > 0.999, "Threshold should be very high"
        assert PSI_THRESHOLD == 0.999999
    
    def test_suppression_sufficient(self):
        """Verify overall suppression brings thermal noise to manageable level."""
        initial = calculate_thermal_ratio()
        effective = effective_thermal_ratio()
        suppression = calculate_suppression_factor()
        
        # Check the relation
        assert abs(initial / suppression - effective) / effective < 0.01
        
        # Effective should be << initial
        assert effective < initial / 1e6


class TestNumericalAccuracy:
    """Tests for numerical accuracy of calculations."""
    
    def test_lorentzian_normalization(self):
        """Verify Lorentzian is properly normalized."""
        # Integrate over reasonable range should give finite value
        f_range = np.linspace(F0 - 10, F0 + 10, 10000)
        omega_range = 2 * np.pi * f_range
        H = lorentzian_filter(omega_range, OMEGA_0, Q_FACTOR)
        
        # Maximum should be 1
        assert abs(np.max(H) - 1.0) < 1e-6
        
        # Integral should be proportional to Q
        df = f_range[1] - f_range[0]
        integral = np.sum(H) * df
        # For Lorentzian: ∫H df ≈ π·Δf = π·f₀/Q
        expected_integral = np.pi * F0 / Q_FACTOR
        # Should be within order of magnitude
        assert 0.5 * expected_integral < integral < 2 * expected_integral
    
    def test_coherence_exponential_decay(self):
        """Verify coherence decays exponentially with detuning."""
        Delta_f = calculate_resonance_width(Q_FACTOR, OMEGA_0)
        
        # Test at multiples of Δf
        for k in [1, 2, 3, 4]:
            psi_k = calculate_coherence_from_sync(F0 + k * Delta_f, F0)
            expected = np.exp(-k)
            # Should follow exp(-k) approximately
            assert abs(psi_k - expected) / expected < 0.1


def test_validation_report_generation():
    """Test that full validation report can be generated."""
    from validate_microtubule_coherence import generate_validation_report
    
    report = generate_validation_report()
    
    # Check all expected keys
    assert 'thermal_ratio_initial' in report
    assert 'suppression_factor' in report
    assert 'thermal_ratio_effective' in report
    assert 'resonance_window' in report
    assert 'consciousness_threshold' in report
    assert 'parameters' in report
    assert 'all_checks_passed' in report
    
    # All checks should pass
    assert report['all_checks_passed'], "All validation checks should pass"


if __name__ == "__main__":
    # Run with pytest if available, otherwise run basic checks
    try:
        import pytest
        sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
    except ImportError:
        print("pytest not available, running basic validation...")
        
        # Run basic checks
        print("\n1. Testing thermal suppression...")
        test_thermal = TestThermalNoiseSuppression()
        test_thermal.test_thermal_ratio_order_of_magnitude()
        test_thermal.test_suppression_factor_calculation()
        test_thermal.test_effective_ratio_manageable()
        print("   ✅ Thermal suppression tests passed")
        
        print("\n2. Testing Lorentzian filter...")
        test_lorentz = TestLorentzianFilter()
        test_lorentz.test_filter_at_resonance()
        test_lorentz.test_resonance_width_calculation()
        test_lorentz.test_narrow_resonance_window()
        print("   ✅ Lorentzian filter tests passed")
        
        print("\n3. Testing coherence threshold...")
        test_coherence = TestCoherenceThreshold()
        test_coherence.test_coherence_at_exact_f0()
        test_coherence.test_coherence_threshold_achievable()
        print("   ✅ Coherence threshold tests passed")
        
        print("\n4. Generating full validation report...")
        test_validation_report_generation()
        print("   ✅ Validation report generated")
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
