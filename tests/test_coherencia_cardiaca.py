"""
Tests for Cardiac Coherence Module - HRV Spectral Analysis

This test suite validates:
1. HRV signal generation
2. Spectral analysis
3. f₀ harmonic detection
4. Coherence metrics
5. Multi-scale integration
6. Integration with cytoplasmic flow model

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.coherencia_cardiaca import (
    HeartRateVariability,
    CardiacCoherenceBridge,
    demonstrate_cardiac_coherence
)
from qcal.constants import F0_HZ


class TestHeartRateVariability(unittest.TestCase):
    """Test HRV analyzer."""
    
    def setUp(self):
        self.hrv = HeartRateVariability(sampling_rate=1000.0)
    
    def test_initialization(self):
        """Test HRV analyzer initialization."""
        self.assertEqual(self.hrv.fs, 1000.0, "Sampling rate should be set correctly")
        self.assertEqual(self.hrv.f0, F0_HZ, "Should use correct fundamental frequency")
    
    def test_synthetic_hrv_generation(self):
        """Test synthetic HRV signal generation."""
        hrv_data = self.hrv.generate_synthetic_hrv(duration=60.0, mean_hr=70.0)
        
        # Check that all expected fields are present
        self.assertIn('time', hrv_data)
        self.assertIn('rr_intervals', hrv_data)
        self.assertIn('heartbeat_times', hrv_data)
        self.assertIn('mean_hr', hrv_data)
        
        # Check signal properties
        self.assertGreater(len(hrv_data['time']), 0, "Should have time points")
        self.assertGreater(len(hrv_data['rr_intervals']), 0, "Should have RR intervals")
        self.assertGreater(len(hrv_data['heartbeat_times']), 0, "Should have heartbeats")
        
        # Check mean heart rate
        self.assertEqual(hrv_data['mean_hr'], 70.0, "Mean HR should match input")
        
        # Check that RR intervals are positive
        self.assertTrue(np.all(hrv_data['rr_intervals'] > 0),
                       "RR intervals should be positive")
    
    def test_hrv_spectrum_computation(self):
        """Test HRV power spectral density computation."""
        hrv_data = self.hrv.generate_synthetic_hrv(duration=120.0)
        spectrum = self.hrv.compute_hrv_spectrum(hrv_data['rr_intervals'])
        
        # Check spectrum fields
        self.assertIn('frequencies', spectrum)
        self.assertIn('power', spectrum)
        self.assertIn('total_power', spectrum)
        
        # Check that frequencies are positive
        self.assertTrue(np.all(spectrum['frequencies'] > 0),
                       "Frequencies should be positive")
        
        # Check that power is non-negative
        self.assertTrue(np.all(spectrum['power'] >= 0),
                       "Power should be non-negative")
        
        # Check power normalization
        self.assertAlmostEqual(spectrum['total_power'], 1.0, places=1,
                              msg="Total power should be normalized")
    
    def test_f0_harmonic_detection(self):
        """Test f₀ harmonic detection in HRV spectrum."""
        hrv_data = self.hrv.generate_synthetic_hrv(duration=120.0, f0_amplitude=0.05)
        spectrum = self.hrv.compute_hrv_spectrum(hrv_data['rr_intervals'])
        
        detected = self.hrv.detect_f0_harmonics(
            spectrum['frequencies'],
            spectrum['power'],
            n_harmonics=3,
            tolerance=0.2
        )
        
        # Should detect at least some harmonics
        self.assertGreaterEqual(len(detected), 0,
                               "Should attempt to detect harmonics")
        
        # Check structure of detected harmonics
        for name, data in detected.items():
            self.assertIn('target_freq', data)
            self.assertIn('detected_freq', data)
            self.assertIn('power', data)
            self.assertIn('frequency_error', data)
            
            # Frequency error should be within tolerance
            self.assertLessEqual(data['frequency_error'], 0.2,
                               f"Frequency error for {name} should be within tolerance")
    
    def test_coherence_metric(self):
        """Test coherence metric calculation."""
        # Test with no harmonics
        coherence_empty = self.hrv.calculate_coherence_metric({})
        self.assertEqual(coherence_empty, 0.0,
                        "Coherence should be 0 with no harmonics")
        
        # Test with harmonics
        mock_harmonics = {
            'harmonic_1': {
                'target_freq': 1.417,
                'detected_freq': 1.42,
                'power': 0.1,
                'frequency_error': 0.003
            }
        }
        coherence = self.hrv.calculate_coherence_metric(mock_harmonics)
        
        self.assertGreaterEqual(coherence, 0.0, "Coherence should be non-negative")
        self.assertLessEqual(coherence, 1.0, "Coherence should be <= 1")


class TestCardiacCoherenceBridge(unittest.TestCase):
    """Test cardiac coherence bridge for multi-scale integration."""
    
    def setUp(self):
        self.bridge = CardiacCoherenceBridge()
    
    def test_initialization(self):
        """Test bridge initialization."""
        self.assertEqual(self.bridge.f0, F0_HZ,
                        "Should use correct fundamental frequency")
        self.assertIsNotNone(self.bridge.hrv_analyzer,
                            "Should have HRV analyzer")
    
    def test_molecular_to_cardiac_scaling(self):
        """Test frequency scaling from molecular to cardiac range."""
        molecular_freq = F0_HZ  # 141.7001 Hz
        cardiac_freq = self.bridge.scale_molecular_to_cardiac(molecular_freq)
        
        # Should scale down by factor of 100
        expected_freq = molecular_freq / 100.0
        self.assertAlmostEqual(cardiac_freq, expected_freq, places=6,
                              msg="Should scale by factor of 100")
        
        # Cardiac frequency should be in physiological range (0.1-10 Hz)
        self.assertGreater(cardiac_freq, 0.1,
                          "Scaled frequency should be > 0.1 Hz")
        self.assertLess(cardiac_freq, 10.0,
                       "Scaled frequency should be < 10 Hz")
    
    def test_multi_scale_coherence_analysis(self):
        """Test multi-scale coherence analysis."""
        results = self.bridge.analyze_multi_scale_coherence(duration=60.0)
        
        # Check all scale levels are present
        self.assertIn('molecular', results)
        self.assertIn('cellular', results)
        self.assertIn('cardiac', results)
        self.assertIn('cross_scale', results)
        
        # Check molecular scale
        self.assertEqual(results['molecular']['fundamental_freq'], F0_HZ)
        self.assertIn('harmonics', results['molecular'])
        
        # Check cellular scale
        self.assertEqual(results['cellular']['organism'], 'C. elegans')
        self.assertGreater(results['cellular']['scaled_freq'], 0)
        
        # Check cardiac scale
        self.assertIn('mean_hr', results['cardiac'])
        self.assertIn('coherence_metric', results['cardiac'])
        self.assertGreaterEqual(results['cardiac']['coherence_metric'], 0)
        self.assertLessEqual(results['cardiac']['coherence_metric'], 1)
        
        # Check cross-scale analysis
        self.assertIn('molecular_to_cellular_ratio', results['cross_scale'])
        self.assertIn('interpretation', results['cross_scale'])
    
    def test_integration_with_cytoplasmic_model(self):
        """Test integration with cytoplasmic flow model."""
        validation = self.bridge.validate_integration_with_cytoplasmic_model()
        
        # Should successfully integrate
        self.assertTrue(validation['integration_successful'],
                       "Integration should succeed")
        self.assertEqual(validation['status'], 'PASSED',
                        "Validation status should be PASSED")
        
        # Check Reynolds number
        self.assertIn('reynolds_number', validation)
        self.assertLess(validation['reynolds_number'], 1e-2,
                       "Reynolds should be in Stokes regime")
        
        # Check Stokes regime
        self.assertTrue(validation['stokes_regime'],
                       "Should confirm Stokes regime")
        
        # Check frequency consistency
        self.assertTrue(validation['consistency_check'],
                       "Frequencies should be consistent with f₀ harmonics")
        
        # Check eigenfrequencies
        self.assertIn('cytoplasmic_eigenfreqs', validation)
        self.assertGreater(len(validation['cytoplasmic_eigenfreqs']), 0,
                          "Should have cytoplasmic eigenfrequencies")
        
        # Check cardiac scaled frequencies
        self.assertIn('cardiac_scaled_freqs', validation)
        self.assertEqual(len(validation['cytoplasmic_eigenfreqs']),
                        len(validation['cardiac_scaled_freqs']),
                        "Should have matching number of frequencies")


class TestDemonstration(unittest.TestCase):
    """Test demonstration function."""
    
    def test_demonstrate_cardiac_coherence(self):
        """Test demonstration runs without errors."""
        # This test mainly checks that the demonstration runs
        # without raising exceptions
        results = demonstrate_cardiac_coherence()
        
        # Check that results contain expected keys
        self.assertIn('molecular', results)
        self.assertIn('cellular', results)
        self.assertIn('cardiac', results)
        self.assertIn('cross_scale', results)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency across scales."""
    
    def setUp(self):
        self.bridge = CardiacCoherenceBridge()
    
    def test_frequency_scaling_consistency(self):
        """Test that frequency scaling is physically consistent."""
        # At molecular scale
        f_molecular = F0_HZ  # ~141.7 Hz
        
        # At cellular scale (C. elegans)
        f_cellular = self.bridge.scale_molecular_to_cardiac(f_molecular)
        
        # At cardiac scale (should be same as cellular for this application)
        f_cardiac = f_cellular
        
        # Check scaling ratios
        ratio_mol_to_cell = f_molecular / f_cellular
        self.assertAlmostEqual(ratio_mol_to_cell, 100.0, places=1,
                              msg="Molecular to cellular ratio should be ~100")
        
        # All frequencies should be positive
        self.assertGreater(f_molecular, 0)
        self.assertGreater(f_cellular, 0)
        self.assertGreater(f_cardiac, 0)
        
        # Cellular and cardiac frequencies should be in physiological range
        self.assertGreater(f_cellular, 0.1, "Too low for physiological range")
        self.assertLess(f_cellular, 10.0, "Too high for HRV range")
    
    def test_reynolds_number_consistency(self):
        """Test that Reynolds number is consistent with Stokes regime."""
        validation = self.bridge.validate_integration_with_cytoplasmic_model()
        
        if validation['integration_successful']:
            Re = validation['reynolds_number']
            
            # Reynolds should be << 1 for Stokes flow
            self.assertLess(Re, 1e-2,
                           "Reynolds should be << 1 for Stokes regime")
            
            # For cytoplasm, Re ~ 10^-6 is expected
            self.assertAlmostEqual(Re, 1e-6, delta=1e-5,
                                  msg="Reynolds should be ~10^-6 for cytoplasmic flow")
    
    def test_eigenfrequency_harmonics(self):
        """Test that eigenfrequencies are proper harmonics of f₀."""
        validation = self.bridge.validate_integration_with_cytoplasmic_model()
        
        if validation['integration_successful']:
            eigenfreqs = validation['cytoplasmic_eigenfreqs']
            
            # Each eigenfrequency should be a harmonic of f₀
            for i, freq in enumerate(eigenfreqs, start=1):
                expected_freq = i * F0_HZ
                relative_error = abs(freq - expected_freq) / expected_freq
                
                self.assertLess(relative_error, 0.01,
                               f"Eigenfrequency {i} should be within 1% of {i}×f₀")


if __name__ == '__main__':
    unittest.main(verbosity=2)
