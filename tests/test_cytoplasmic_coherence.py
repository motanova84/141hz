#!/usr/bin/env python3
"""
Tests for Cytoplasmic Flow Coherence Model

Tests validate:
1. Coherence length calculation (ξ ≈ 1.06 μm)
2. Harmonic frequency generation (fₙ = n × f₀)
3. Hermitian operator properties
4. Spectral simulation and analysis

Author: José Manuel Mota Burruezo
Date: January 31, 2026
"""

import sys
import os
import unittest
import numpy as np

# Add qcal module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from qcal.constants import (
        F0_HZ, OMEGA_0, KAPPA_PI, NU_CYTOPLASM_M2_S,
        XI_COHERENCE_M, XI_COHERENCE_UM, CELLULAR_SCALE_UM,
        COHERENCE_SCALE_MATCH, SUPERFLUID_COHERENCE_THRESHOLD,
        harmonic_frequency, temporal_scale,
        calcular_coherencia_citoplasmática,
        F1_HZ, F2_HZ, F3_HZ
    )
    CONSTANTS_AVAILABLE = True
except ImportError:
    CONSTANTS_AVAILABLE = False


class TestCytoplasmicCoherenceConstants(unittest.TestCase):
    """Test suite for cytoplasmic coherence constants."""
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_coherence_length_scale(self):
        """Test that coherence length ξ ≈ 1 μm."""
        self.assertAlmostEqual(XI_COHERENCE_UM, 1.06, delta=0.1,
                              msg="Coherence length should be ~1.06 μm")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_coherence_length_matches_cellular_scale(self):
        """Test that ξ ≈ L (coherence at cellular scale)."""
        error = abs(XI_COHERENCE_UM - CELLULAR_SCALE_UM) / CELLULAR_SCALE_UM
        self.assertLess(error, 0.15, 
                       msg="Coherence length should match cellular scale within 15%")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_coherence_length_calculation(self):
        """Test coherence length formula ξ = √(ν/ω)."""
        expected_xi = np.sqrt(NU_CYTOPLASM_M2_S / OMEGA_0)
        self.assertAlmostEqual(XI_COHERENCE_M, expected_xi, places=12,
                              msg="Coherence length calculation should match formula")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_harmonic_frequencies(self):
        """Test harmonic frequency generation fₙ = n × f₀."""
        # Test first 6 harmonics
        for n in range(1, 7):
            fn = harmonic_frequency(n)
            expected = n * F0_HZ
            self.assertAlmostEqual(fn, expected, places=5,
                                  msg=f"Harmonic {n} should be {expected} Hz")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_temporal_scales(self):
        """Test temporal scales τₙ = 1/fₙ."""
        for n in range(1, 7):
            tau_n = temporal_scale(n)
            expected = 1.0 / (n * F0_HZ)
            self.assertAlmostEqual(tau_n, expected, places=8,
                                  msg=f"Temporal scale {n} should be {expected} s")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_predefined_harmonics(self):
        """Test predefined harmonic constants."""
        self.assertAlmostEqual(F1_HZ, 141.70001, places=5)
        self.assertAlmostEqual(F2_HZ, 283.40002, places=5)
        self.assertAlmostEqual(F3_HZ, 425.10003, places=4)
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_kappa_pi_constant(self):
        """Test that κ_Π = 2.5773."""
        self.assertAlmostEqual(KAPPA_PI, 2.5773, places=4,
                              msg="Wave number κ_Π should be 2.5773")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_superfluid_threshold(self):
        """Test superfluid coherence threshold is reasonable."""
        self.assertGreater(SUPERFLUID_COHERENCE_THRESHOLD, 0.9,
                          msg="Superfluid threshold should be >90%")
        self.assertLess(SUPERFLUID_COHERENCE_THRESHOLD, 1.0,
                       msg="Superfluid threshold should be <100%")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "qcal.constants not available")
    def test_calcular_coherencia_function(self):
        """Test calcular_coherencia_citoplasmática() function."""
        result = calcular_coherencia_citoplasmática()
        
        # Check required keys
        self.assertIn('kappa_pi', result)
        self.assertIn('xi_um', result)
        self.assertIn('harmonics_hz', result)
        self.assertIn('temporal_scales_s', result)
        self.assertIn('interpretacion', result)
        
        # Check values
        self.assertAlmostEqual(result['kappa_pi'], KAPPA_PI, places=4)
        self.assertAlmostEqual(result['xi_um'], XI_COHERENCE_UM, places=3)
        
        # Check harmonics list
        harmonics = result['harmonics_hz']
        self.assertEqual(len(harmonics), 6, msg="Should have 6 harmonics")
        self.assertAlmostEqual(harmonics[0], F0_HZ, places=5)
        self.assertAlmostEqual(harmonics[1], 2*F0_HZ, places=5)


class TestCytoplasmicFlowModel(unittest.TestCase):
    """Test suite for cytoplasmic flow model implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            # Import here to avoid issues if module not available
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
            from validate_cytoplasmic_coherence import CytoplasmicFlowModel
            self.model = CytoplasmicFlowModel()
            self.model_available = True
        except ImportError:
            self.model_available = False
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_coherence_length_calculation_in_model(self):
        """Test model calculates correct coherence length."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        xi_um = self.model.coherence_length_um()
        self.assertAlmostEqual(xi_um, 1.06, delta=0.1,
                              msg="Model coherence length should be ~1.06 μm")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_scale_match_verification(self):
        """Test scale match verification method."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        result = self.model.verify_scale_match()
        
        self.assertIn('xi_um', result)
        self.assertIn('error_percent', result)
        self.assertIn('match', result)
        self.assertIn('status', result)
        
        # Should match within 15%
        self.assertLess(result['error_percent'], 15.0)
        self.assertTrue(result['match'])
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_harmonic_spectrum_generation(self):
        """Test harmonic spectrum generation."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        harmonics, amplitudes = self.model.generate_harmonic_spectrum(num_harmonics=6)
        
        # Check shape
        self.assertEqual(len(harmonics), 6)
        self.assertEqual(len(amplitudes), 6)
        
        # Check frequencies
        for n, fn in enumerate(harmonics, 1):
            expected = n * F0_HZ
            self.assertAlmostEqual(fn, expected, delta=0.1)
        
        # Check amplitudes are decreasing
        for i in range(len(amplitudes) - 1):
            self.assertGreaterEqual(amplitudes[i], amplitudes[i+1],
                                   msg="Amplitudes should decrease with n")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_hermitian_operator_check(self):
        """Test hermitian operator verification."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        # Create a hermitian matrix
        size = 5
        H = np.random.randn(size, size) + 1j * np.random.randn(size, size)
        H = (H + H.conj().T) / 2  # Make hermitian
        
        is_hermitian = self.model.is_hermitian_operator(H)
        self.assertTrue(is_hermitian, msg="Hermitian matrix should be detected")
        
        # Create a non-hermitian matrix
        H_non = np.random.randn(size, size) + 1j * np.random.randn(size, size)
        is_hermitian = self.model.is_hermitian_operator(H_non)
        self.assertFalse(is_hermitian, msg="Non-hermitian matrix should be detected")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_flow_operator_construction(self):
        """Test flow operator is hermitian for healthy cells."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        operator, properties = self.model.construct_flow_operator(size=10)
        
        # Check properties
        self.assertTrue(properties['is_hermitian'],
                       msg="Flow operator should be hermitian")
        self.assertTrue(properties['eigenvalues_real'],
                       msg="Eigenvalues should be real")
        
        # Check eigenvalues are positive
        eigenvalues = properties['eigenvalues']
        self.assertTrue(np.all(eigenvalues > 0),
                       msg="Eigenvalues should be positive")
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Model not available")
    def test_cytoplasmic_flow_simulation(self):
        """Test cytoplasmic flow simulation."""
        if not self.model_available:
            self.skipTest("Model not available")
        
        t, flow = self.model.simulate_cytoplasmic_flow(
            duration_s=0.5,
            fs=5000.0,
            noise_level=0.05,
            coherence=0.95
        )
        
        # Check shape
        expected_samples = int(0.5 * 5000)
        self.assertEqual(len(t), expected_samples)
        self.assertEqual(len(flow), expected_samples)
        
        # Check normalization
        self.assertAlmostEqual(np.max(np.abs(flow)), 1.0, places=1,
                              msg="Flow should be normalized to [-1, 1]")


class TestValidationIntegration(unittest.TestCase):
    """Integration tests for validation workflow."""
    
    @unittest.skipUnless(CONSTANTS_AVAILABLE, "Constants not available")
    def test_coherence_validation_workflow(self):
        """Test complete coherence validation can be executed."""
        # This is a smoke test - just verify imports and basic execution
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
            from validate_cytoplasmic_coherence import CellularCoherenceValidator
            
            validator = CellularCoherenceValidator()
            
            # Should be able to create validator
            self.assertIsNotNone(validator)
            self.assertIsNotNone(validator.model)
            
        except ImportError as e:
            self.skipTest(f"Validation module not available: {e}")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCytoplasmicCoherenceConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestCytoplasmicFlowModel))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
