#!/usr/bin/env python3
"""
Test suite for experimental_detection_protocol.py

Validates the experimental detection protocol implementation for f₀ = 141.7 Hz.
"""

import unittest
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import experimental_detection_protocol as edp


# Test constants
MAX_EXPECTED_LAMBDA_F0_MPC = 1e-10  # Maximum expected wavelength in Mpc for f₀
MAX_EXPECTED_MODULATION = 0.002  # Maximum expected 0.2% modulation in correlation function
FLOAT_COMPARISON_PLACES = 15  # Decimal places for float comparison (reasonable for numerical precision)


class TestQuantumResonator(unittest.TestCase):
    """Test cases for QuantumResonator class."""

    def test_initialization(self):
        """Test that QuantumResonator initializes correctly."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=0.015
        )

        self.assertEqual(resonator.f_resonance, 141.7001)
        self.assertEqual(resonator.Q_factor, 1e9)
        self.assertEqual(resonator.temperature, 0.015)
        self.assertEqual(resonator.f0_target, edp.F0_TARGET)
        self.assertAlmostEqual(resonator.bandwidth, 141.7001 / 1e9, places=12)

    def test_coupling_strength(self):
        """Test coupling strength calculation."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=0.015
        )
        
        g = resonator.coupling_strength()
        self.assertGreater(g, 0)
        self.assertIsInstance(g, float)
        
        # Coupling strength should be on the order of ~10^-14 to 10^-10
        self.assertGreater(g, 1e-15)
        self.assertLess(g, 1e-9)

    def test_thermal_noise_zero_temp(self):
        """Test thermal noise at zero temperature."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=0.0
        )
        
        n_th = resonator.thermal_noise()
        self.assertEqual(n_th, 0)

    def test_thermal_noise_finite_temp(self):
        """Test thermal noise at finite temperature."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=1.0
        )
        
        n_th = resonator.thermal_noise()
        self.assertGreater(n_th, 0)
        self.assertIsInstance(n_th, float)

    def test_signal_to_noise_ratio(self):
        """Test SNR calculation."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=0.015
        )
        
        snr_1s = resonator.signal_to_noise_ratio(1.0)
        snr_10s = resonator.signal_to_noise_ratio(10.0)
        snr_100s = resonator.signal_to_noise_ratio(100.0)
        
        # SNR should increase with integration time (proportional to sqrt(t))
        self.assertGreater(snr_10s, snr_1s)
        self.assertGreater(snr_100s, snr_10s)
        
        # Check approximate scaling: SNR(10t) ≈ sqrt(10) * SNR(t)
        ratio = snr_10s / snr_1s
        self.assertGreater(ratio, 2.5)  # sqrt(10) ≈ 3.16
        self.assertLess(ratio, 4.0)

    def test_optimal_detuning_on_resonance(self):
        """Test detuning when perfectly on resonance."""
        resonator = edp.QuantumResonator(
            f_resonance=141.7001,  # Exactly f₀
            Q_factor=1e9,
            temperature=0.015
        )
        
        detuning = resonator.optimal_detuning()
        self.assertAlmostEqual(detuning, 0.0, places=6)

    def test_optimal_detuning_off_resonance(self):
        """Test detuning when off resonance."""
        resonator = edp.QuantumResonator(
            f_resonance=142.0,  # Slightly off f₀
            Q_factor=1e9,
            temperature=0.015
        )
        
        detuning = resonator.optimal_detuning()
        expected_detuning = 142.0 - 141.7001
        self.assertAlmostEqual(detuning, expected_detuning, places=6)

    def test_is_on_resonance(self):
        """Test resonance checking."""
        # Perfectly on resonance
        resonator_on = edp.QuantumResonator(
            f_resonance=141.7001,
            Q_factor=1e9,
            temperature=0.015
        )
        self.assertTrue(resonator_on.is_on_resonance())
        
        # Slightly off resonance but within bandwidth
        resonator_near = edp.QuantumResonator(
            f_resonance=141.7001 + 1e-10,  # Very small detuning
            Q_factor=1e9,
            temperature=0.015
        )
        self.assertTrue(resonator_near.is_on_resonance())
        
        # Far off resonance
        resonator_off = edp.QuantumResonator(
            f_resonance=150.0,
            Q_factor=1e9,
            temperature=0.015
        )
        self.assertFalse(resonator_off.is_on_resonance())


class TestResonatorDesigns(unittest.TestCase):
    """Test cases for specific resonator design functions."""

    def test_design_superconducting_cavity(self):
        """Test superconducting cavity design."""
        resonator = edp.design_superconducting_cavity()
        
        self.assertIsInstance(resonator, edp.QuantumResonator)
        self.assertEqual(resonator.f_resonance, 141.7001)
        self.assertEqual(resonator.Q_factor, 1e9)
        self.assertEqual(resonator.temperature, 0.015)
        self.assertTrue(resonator.is_on_resonance())

    def test_design_optomechanical_cavity(self):
        """Test optomechanical cavity design."""
        resonator = edp.design_optomechanical_cavity()
        
        self.assertIsInstance(resonator, edp.QuantumResonator)
        self.assertEqual(resonator.f_resonance, 141.7001)
        self.assertEqual(resonator.Q_factor, 1e7)
        self.assertEqual(resonator.temperature, 1.0)
        self.assertTrue(resonator.is_on_resonance())


class TestDESIDataAnalysis(unittest.TestCase):
    """Test cases for DESIDataAnalysis class."""

    def test_initialization(self):
        """Test that DESIDataAnalysis initializes correctly."""
        desi = edp.DESIDataAnalysis()

        self.assertEqual(desi.f0, edp.F0_TARGET)
        self.assertEqual(desi.c, 299792458.0)
        self.assertEqual(desi.H0, 67.4)

    def test_frequency_to_scale(self):
        """Test frequency to cosmological scale conversion."""
        desi = edp.DESIDataAnalysis()

        lambda_f0 = desi.frequency_to_scale(141.7001)

        # Scale should be very small compared to BAO scale
        self.assertGreater(lambda_f0, 0)
        self.assertLess(lambda_f0, MAX_EXPECTED_LAMBDA_F0_MPC)

        # Check dimensional consistency
        expected_meters = desi.c / 141.7001
        expected_Mpc = expected_meters / 3.086e22
        self.assertAlmostEqual(lambda_f0, expected_Mpc, places=FLOAT_COMPARISON_PLACES)

    def test_predicted_bao_scale(self):
        """Test BAO scale prediction."""
        desi = edp.DESIDataAnalysis()
        
        r_BAO_std, lambda_f0, epsilon = desi.predicted_bao_scale()
        
        # Check BAO scale
        self.assertEqual(r_BAO_std, 147.09)
        
        # Check lambda_f0 is positive and small
        self.assertGreater(lambda_f0, 0)
        self.assertLess(lambda_f0, 1e-10)
        
        # Check modulation amplitude
        self.assertEqual(epsilon, 1e-3)

    def test_search_in_power_spectrum(self):
        """Test power spectrum search functionality."""
        desi = edp.DESIDataAnalysis()
        
        # Should run without errors (no return value expected)
        desi.search_in_power_spectrum()

    def test_correlation_function_analysis(self):
        """Test correlation function analysis."""
        desi = edp.DESIDataAnalysis()
        
        r, xi_std, xi_psi = desi.correlation_function_analysis()
        
        # Check output arrays
        self.assertEqual(len(r), 1000)
        self.assertEqual(len(xi_std), 1000)
        self.assertEqual(len(xi_psi), 1000)
        
        # Check that r is in correct range
        self.assertGreater(r.min(), 0.009)
        self.assertLess(r.max(), 1100)
        
        # Check that xi values are positive (power law)
        self.assertTrue(np.all(xi_std > 0))
        self.assertTrue(np.all(xi_psi > 0))
        
        # Check that modulation is small
        relative_diff = np.abs((xi_psi - xi_std) / xi_std)
        self.assertLess(relative_diff.max(), MAX_EXPECTED_MODULATION)

    def test_correlation_function_artifact(self):
        """Test that correlation function creates artifact."""
        # Clean up any existing artifact
        artifact_path = Path('artifacts/desi_correlation_function.png')
        if artifact_path.exists():
            artifact_path.unlink()
        
        desi = edp.DESIDataAnalysis()
        desi.correlation_function_analysis()
        
        # Check that artifact was created
        self.assertTrue(artifact_path.exists())


class TestCompleteProtocol(unittest.TestCase):
    """Test cases for complete detection protocol."""

    def test_complete_detection_protocol(self):
        """Test that complete protocol runs without errors."""
        # This should run the entire protocol and generate all outputs
        try:
            edp.complete_detection_protocol()
            success = True
        except Exception as e:
            success = False
            print(f"Error in complete_detection_protocol: {e}")
        
        self.assertTrue(success)

    def test_protocol_creates_artifacts(self):
        """Test that protocol creates expected artifacts."""
        edp.complete_detection_protocol()
        
        # Check for correlation function plot
        artifact_path = Path('artifacts/desi_correlation_function.png')
        self.assertTrue(artifact_path.exists())


if __name__ == '__main__':
    # Create artifacts directory if it doesn't exist
    Path('artifacts').mkdir(exist_ok=True)
    
    # Run tests
    unittest.main()
