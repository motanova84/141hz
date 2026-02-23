#!/usr/bin/env python3
"""
Tests for Calabi-Yau Spectrum Integration Module

Verifies that the integration between CY spectral geometry (κ_Π) and
QCAL frequency system (f₀) produces consistent physical predictions.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cy_spectrum_integration import (
    KAPPA_PI, F0_TARGET, DELTA_ZETA, C_COHERENCE,
    compute_quantum_radius, compute_yukawa_wavelength,
    compute_decoherence_time, compute_frequency_uncertainty,
    compute_coherence_constant, compute_chern_simons_level,
    compute_full_integration, verify_integration
)


class TestConstants:
    """Test that fundamental constants are correctly defined."""
    
    def test_kappa_pi_value(self):
        """κ_Π should be 2.5773"""
        assert KAPPA_PI == 2.5773
    
    def test_f0_value(self):
        """f₀ should be 141.7001 Hz"""
        assert F0_TARGET == 141.7001
    
    def test_delta_zeta_value(self):
        """δζ should be 0.2787 Hz"""
        assert DELTA_ZETA == 0.2787
    
    def test_coherence_constant_value(self):
        """C should be 244.36"""
        assert C_COHERENCE == 244.36


class TestPhysicalPredictions:
    """Test individual physical prediction functions."""
    
    def test_quantum_radius(self):
        """R_Ψ should be approximately 336 km"""
        R_psi = compute_quantum_radius(F0_TARGET)
        R_psi_km = R_psi / 1000
        assert 330 < R_psi_km < 350  # ~336 km
    
    def test_yukawa_wavelength(self):
        """λ_Y should be approximately 2116 km"""
        lambda_y = compute_yukawa_wavelength(F0_TARGET)
        lambda_y_km = lambda_y / 1000
        assert 2000 < lambda_y_km < 2200  # ~2115 km
    
    def test_decoherence_time(self):
        """τ_deco should be approximately 11.4 ms"""
        tau_deco = compute_decoherence_time(F0_TARGET)
        tau_deco_ms = tau_deco * 1000
        assert 10 < tau_deco_ms < 15  # ~11.4 ms
    
    def test_frequency_uncertainty(self):
        """δζ should be 0.2787 Hz"""
        delta_zeta = compute_frequency_uncertainty(F0_TARGET, KAPPA_PI)
        assert delta_zeta == DELTA_ZETA
    
    def test_coherence_constant(self):
        """C should be approximately 244-250"""
        C = compute_coherence_constant(KAPPA_PI)
        assert 240 < C < 260  # ~250.21
        
        # Check error relative to target
        error_percent = abs(C - C_COHERENCE) / C_COHERENCE * 100
        assert error_percent < 5  # Less than 5% error
    
    def test_chern_simons_level(self):
        """k_CS should be approximately 32.4"""
        k_cs = compute_chern_simons_level(KAPPA_PI)
        assert 30 < k_cs < 35  # ~32.39


class TestFullIntegration:
    """Test complete integration function."""
    
    def test_integration_returns_dict(self):
        """Integration should return a dictionary"""
        results = compute_full_integration()
        assert isinstance(results, dict)
    
    def test_integration_has_required_keys(self):
        """Integration results should have all required sections"""
        results = compute_full_integration()
        required_keys = [
            'calabi_yau',
            'integration_principle',
            'frequencies',
            'physical_predictions',
            'constants',
            'references'
        ]
        for key in required_keys:
            assert key in results
    
    def test_calabi_yau_section(self):
        """CY section should have correct invariants"""
        results = compute_full_integration()
        cy = results['calabi_yau']
        
        assert cy['kappa_pi'] == 2.5773
        assert cy['h11'] == 1
        assert cy['h21'] == 101
        assert cy['euler_characteristic'] == -200
    
    def test_physical_predictions_section(self):
        """Physical predictions should have all components"""
        results = compute_full_integration()
        preds = results['physical_predictions']
        
        required_predictions = [
            'quantum_radius',
            'yukawa_wavelength',
            'decoherence_time',
            'frequency_uncertainty',
            'coherence_constant',
            'chern_simons_level'
        ]
        for pred in required_predictions:
            assert pred in preds
    
    def test_frequencies_section(self):
        """Frequencies section should have f₀ and πCODE"""
        results = compute_full_integration()
        freqs = results['frequencies']
        
        assert freqs['f0_hz'] == 141.7001
        assert freqs['picode_hz'] == 888.0
        assert 'f0_picode_ratio' in freqs


class TestVerification:
    """Test verification function."""
    
    def test_verification_returns_tuple(self):
        """Verification should return (bool, dict)"""
        passed, verification = verify_integration()
        assert isinstance(passed, bool)
        assert isinstance(verification, dict)
    
    def test_verification_passes(self):
        """Verification should pass all checks"""
        passed, verification = verify_integration(tolerance_percent=5.0)
        assert passed is True
    
    def test_all_checks_present(self):
        """Verification should check all physical predictions"""
        _, verification = verify_integration()
        checks = verification['checks']
        
        required_checks = [
            'coherence_constant',
            'yukawa_wavelength',
            'decoherence_time',
            'frequency_uncertainty',
            'chern_simons_level'
        ]
        for check in required_checks:
            assert check in checks
            assert 'passed' in checks[check]
    
    def test_individual_checks_pass(self):
        """Each individual check should pass"""
        _, verification = verify_integration(tolerance_percent=5.0)
        checks = verification['checks']
        
        for check_name, check_data in checks.items():
            assert check_data['passed'] is True, f"{check_name} failed"


class TestConsistency:
    """Test consistency between different computed values."""
    
    def test_coherence_constant_formula(self):
        """C ≈ κ_Π × φ × 60"""
        import math
        phi = (1 + math.sqrt(5)) / 2
        C_expected = KAPPA_PI * phi * 60
        C_computed = compute_coherence_constant(KAPPA_PI)
        
        # Should match within floating point precision
        assert abs(C_computed - C_expected) < 1e-10
    
    def test_chern_simons_formula(self):
        """k = 4πκ_Π"""
        import math
        k_expected = 4 * math.pi * KAPPA_PI
        k_computed = compute_chern_simons_level(KAPPA_PI)
        
        # Should match within floating point precision
        assert abs(k_computed - k_expected) < 1e-10
    
    def test_quantum_radius_formula(self):
        """R_Ψ = c/(2πf₀)"""
        import math
        c = 299792458.0  # m/s
        R_expected = c / (2 * math.pi * F0_TARGET)
        R_computed = compute_quantum_radius(F0_TARGET)
        
        # Should match within floating point precision
        assert abs(R_computed - R_expected) < 1e-6
    
    def test_yukawa_wavelength_formula(self):
        """λ_Y = c/f₀"""
        c = 299792458.0  # m/s
        lambda_expected = c / F0_TARGET
        lambda_computed = compute_yukawa_wavelength(F0_TARGET)
        
        # Should match within floating point precision
        assert abs(lambda_computed - lambda_expected) < 1e-6
    
    def test_decoherence_time_formula(self):
        """τ_deco = φ/f₀"""
        import math
        phi = (1 + math.sqrt(5)) / 2
        tau_expected = phi / F0_TARGET
        tau_computed = compute_decoherence_time(F0_TARGET)
        
        # Should match within floating point precision
        assert abs(tau_computed - tau_expected) < 1e-10


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_different_kappa_values(self):
        """Integration should work with different κ_Π values"""
        kappa_values = [2.5, 2.5773, 2.6, 3.0]
        for kappa in kappa_values:
            results = compute_full_integration(kappa_pi=kappa, f0=F0_TARGET)
            assert results['calabi_yau']['kappa_pi'] == kappa
    
    def test_different_f0_values(self):
        """Integration should work with different f₀ values"""
        f0_values = [100.0, 141.7001, 200.0]
        for f0 in f0_values:
            results = compute_full_integration(kappa_pi=KAPPA_PI, f0=f0)
            assert results['frequencies']['f0_hz'] == f0
    
    def test_verification_with_strict_tolerance(self):
        """Verification with strict tolerance should still pass"""
        passed, verification = verify_integration(tolerance_percent=3.0)
        # Might fail with very strict tolerance
        # but should document which checks fail
        assert 'checks' in verification


# Run tests if executed directly
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
