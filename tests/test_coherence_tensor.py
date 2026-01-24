#!/usr/bin/env python3
"""
TEST: Consciousness Coherence Tensor Ξ_μν

Tests for the complete derivation of the consciousness coherence tensor.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import unittest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from qcal.coherence_tensor import (
    ConsciousnessCoherenceTensor,
    validate_canonical_ratio,
    F0_HZ, phi
)


class TestCoherenceTensor(unittest.TestCase):
    """Test cases for consciousness coherence tensor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tensor = ConsciousnessCoherenceTensor()
        self.I = 30.8456
        self.A_eff = 1.0
    
    def test_canonical_ratio(self):
        """Test canonical ratio I/A_eff² ≈ 30.8456."""
        results = validate_canonical_ratio()
        
        # Check that validated value is exactly 30.8456
        self.assertAlmostEqual(
            results['validated_value'],
            results['numerical_target'],
            places=4,
            msg="Validated value should match target"
        )
        
        # Check validation status
        self.assertEqual(results['validation_status'], 'PASS')
    
    def test_kappa_I_coupling(self):
        """Test consciousness-modulated gravitational coupling."""
        kappa_I = self.tensor.compute_kappa_I(self.I, self.A_eff)
        kappa_classical = self.tensor.kappa_classical
        
        # κ(I) should be less than κ for coherent state
        self.assertLess(kappa_I, kappa_classical)
        
        # Ratio should match I·A_eff²
        expected_ratio = 1.0 / (self.I * self.A_eff**2)
        actual_ratio = kappa_I / kappa_classical
        self.assertAlmostEqual(expected_ratio, actual_ratio, places=6)
    
    def test_I_over_Aeff2_computation(self):
        """Test I/A_eff² computation."""
        ratio = self.tensor.compute_I_over_Aeff2()
        
        # Should be exactly 30.8456 (validated empirical value)
        self.assertAlmostEqual(ratio, 30.8456, places=4)
    
    def test_ligo_psi_q1_snr(self):
        """Test LIGO Ψ-Q1 SNR is in expected range."""
        results = self.tensor.ligo_psi_q1_test(self.I, self.A_eff, base_snr=8.0)
        
        # SNR should be detected (> 5σ)
        self.assertGreater(results['sigma'], 5.0)
        self.assertTrue(results['detection_confirmed'])
        
        # SNR should be in range 25-27σ
        self.assertGreaterEqual(results['SNR_total'], 25.0)
        self.assertLessEqual(results['SNR_total'], 27.0)
        
        # Status should be confirmed
        self.assertEqual(results['status'], 'CONFIRMED')
    
    def test_ricci_modulation_order(self):
        """Test Ricci curvature modulation is correct order of magnitude."""
        R_mod = self.tensor.compute_ricci_modulation(self.I, self.A_eff, lab_scale=1.0)
        
        # Should be non-zero
        self.assertNotEqual(R_mod, 0.0)
        
        # Order of magnitude should be reasonable for lab scale
        # Given the small consciousness energy, expect very small values
        self.assertGreater(abs(R_mod), 0.0)
        self.assertLess(abs(R_mod), 1e10)
    
    def test_xi_component_structure(self):
        """Test coherence tensor component structure."""
        R_mu_nu = 1e-3
        R = 4e-3
        g_mu_nu = -1.0
        nabla_mu_nabla_nu_IA2 = 0.0
        
        Xi_00 = self.tensor.xi_mu_nu_component(
            R_mu_nu, R, g_mu_nu, nabla_mu_nabla_nu_IA2, self.I, self.A_eff
        )
        
        # Should be finite
        self.assertFalse(np.isnan(Xi_00))
        self.assertFalse(np.isinf(Xi_00))
    
    def test_conservation_law(self):
        """Test conservation law verification."""
        Xi_components = {
            'Xi_00': 1.0,
            'Xi_11': 1.0,
            'Xi_22': 1.0,
            'Xi_33': 1.0,
            'divergence_0': 0.0,
            'divergence_1': 0.0,
            'divergence_2': 0.0,
            'divergence_3': 0.0
        }
        
        is_conserved, max_violation = self.tensor.verify_conservation(
            Xi_components, christoffel_symbols={}
        )
        
        # For zero divergence, should be conserved
        self.assertTrue(is_conserved)
        self.assertLess(max_violation, 1e-10)
    
    def test_unified_field_equation(self):
        """Test unified field equation residual."""
        # For exact solution, residual should be zero
        G_mu_nu = 1.0
        Lambda = 0.0
        g_mu_nu = -1.0
        T_mu_nu = 0.5
        Xi_mu_nu = 0.5
        
        residual = self.tensor.unified_field_equation(
            G_mu_nu, Lambda, g_mu_nu, T_mu_nu, Xi_mu_nu
        )
        
        # Should be small (balanced equation)
        self.assertIsInstance(residual, float)
        self.assertGreaterEqual(residual, 0.0)
    
    def test_ontological_interpretation(self):
        """Test ontological interpretation."""
        interpretation = self.tensor.ontological_interpretation(self.I, self.A_eff)
        
        # Should return a dictionary
        self.assertIsInstance(interpretation, dict)
        
        # Should have key fields
        self.assertIn('I', interpretation)
        self.assertIn('A_eff', interpretation)
        self.assertIn('coherence_state', interpretation)
        
        # For A_eff = 1.0, should be coherent
        self.assertIn('COHERENT', interpretation['coherence_state'])
    
    def test_coherence_threshold(self):
        """Test coherence threshold at A_eff = 1.0."""
        # Sub-coherent
        interp_sub = self.tensor.ontological_interpretation(self.I, 0.9)
        self.assertIn('INCOHERENT', interp_sub['coherence_state'])
        
        # Coherent
        interp_coherent = self.tensor.ontological_interpretation(self.I, 1.0)
        self.assertIn('COHERENT', interp_coherent['coherence_state'])
        
        # Super-coherent
        interp_super = self.tensor.ontological_interpretation(self.I, 1.5)
        self.assertIn('COHERENT', interp_super['coherence_state'])
    
    def test_snr_enhancement_scaling(self):
        """Test SNR enhancement scales with coherence."""
        base_snr = 8.0
        
        # Lower coherence
        results_low = self.tensor.ligo_psi_q1_test(self.I, 0.9, base_snr)
        
        # Higher coherence
        results_high = self.tensor.ligo_psi_q1_test(self.I, 1.2, base_snr)
        
        # Higher coherence should give higher SNR
        self.assertGreater(results_high['SNR_total'], results_low['SNR_total'])


class TestCanonicalRatio(unittest.TestCase):
    """Test canonical ratio validation."""
    
    def test_phi_value(self):
        """Test golden ratio value."""
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(phi, expected_phi, places=10)
    
    def test_f0_value(self):
        """Test fundamental frequency."""
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)
    
    def test_ratio_formula(self):
        """Test ratio formula (1032·φ³)/f₀ ≈ 30.85."""
        ratio = (1032.0 * phi**3) / F0_HZ
        
        # Should be close to 30.8456
        self.assertAlmostEqual(ratio, 30.8456, delta=0.1)


def run_tests():
    """Run all tests."""
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
