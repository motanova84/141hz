#!/usr/bin/env python3
"""
Tests for Unified Noetic Quantum Gravity Theory module.

Tests the cyclic relationship:
    Number (ζ) → Geometry (CY) → Frequency (f₀) → Consciousness (Ψ)
                → Gravity (G) → Spectrum (λn) → Number (ζ)
"""

import os
import sys
import unittest
import json

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from teoria_unificada_141hz import (
    UnifiedTheory,
    UnifiedTheoryConstants,
    RiemannZetaComponent,
    CalabiYauComponent,
    FrequencyComponent,
    ConsciousnessComponent,
    GravityComponent,
    SpectrumComponent,
    CondensedMatterComponent,
    F0, PHI, GAMMA, c, pi
)


class TestUnifiedTheoryConstants(unittest.TestCase):
    """Test fundamental constants."""
    
    def setUp(self):
        self.constants = UnifiedTheoryConstants()
    
    def test_fundamental_frequency(self):
        """Test fundamental frequency value."""
        self.assertAlmostEqual(self.constants.f0, 141.7001, places=4)
        self.assertAlmostEqual(self.constants.f0_uncertainty, 0.0016, places=4)
    
    def test_angular_frequency(self):
        """Test angular frequency calculation."""
        expected = 2 * pi * self.constants.f0
        self.assertAlmostEqual(self.constants.omega_0, expected, places=4)
    
    def test_wavelength(self):
        """Test wavelength λ = c/f₀."""
        expected_km = c / self.constants.f0 / 1000
        self.assertAlmostEqual(self.constants.lambda_psi / 1000, expected_km, places=2)
    
    def test_yukawa_range(self):
        """Test Yukawa correction range R = c/(2πf₀) ≈ 336 km."""
        expected_km = c / (2 * pi * self.constants.f0) / 1000
        self.assertAlmostEqual(self.constants.R_psi / 1000, expected_km, places=2)
        # Check it matches the problem statement value
        self.assertAlmostEqual(self.constants.R_psi / 1000, 336.24, delta=0.5)


class TestRiemannZetaComponent(unittest.TestCase):
    """Test Riemann zeta zeros connection."""
    
    def setUp(self):
        self.zeta = RiemannZetaComponent()
    
    def test_first_zero(self):
        """Test first Riemann zero."""
        self.assertAlmostEqual(self.zeta.RIEMANN_ZEROS_TN[0], 14.134725, places=4)
    
    def test_overtone_frequency(self):
        """Test overtone frequency calculation f_n = t_n × f₀."""
        f1 = self.zeta.riemann_overtone_frequency(1)
        expected = 14.134725 * F0
        self.assertAlmostEqual(f1, expected, places=2)
    
    def test_get_all_overtones(self):
        """Test getting all overtones."""
        overtones = self.zeta.get_all_overtones()
        self.assertEqual(len(overtones), 20)
        self.assertEqual(overtones[0]["n"], 1)
        self.assertAlmostEqual(overtones[0]["t_n"], 14.134725, places=4)
    
    def test_invalid_zero_index(self):
        """Test error handling for invalid index."""
        with self.assertRaises(ValueError):
            self.zeta.riemann_overtone_frequency(0)
        with self.assertRaises(ValueError):
            self.zeta.riemann_overtone_frequency(100)


class TestCalabiYauComponent(unittest.TestCase):
    """Test Calabi-Yau geometry component."""
    
    def setUp(self):
        self.cy = CalabiYauComponent()
    
    def test_compactification_parameters(self):
        """Test compactification parameters."""
        params = self.cy.compactification_parameters()
        self.assertEqual(params["manifold"], "Quintic in CP⁴")
        self.assertIn("R_psi_km", params)
        self.assertAlmostEqual(params["R_psi_km"], 336.24, delta=0.5)


class TestFrequencyComponent(unittest.TestCase):
    """Test frequency component."""
    
    def setUp(self):
        self.freq = FrequencyComponent()
    
    def test_frequency_properties(self):
        """Test frequency properties."""
        props = self.freq.get_frequency_properties()
        self.assertAlmostEqual(props["f0_Hz"], F0, places=4)
        self.assertAlmostEqual(props["period_s"], 1/F0, places=6)
    
    def test_harmonics(self):
        """Test harmonic frequencies."""
        harmonics = self.freq.harmonics(5)
        self.assertEqual(len(harmonics), 5)
        self.assertEqual(harmonics[0]["n"], 1)
        self.assertAlmostEqual(harmonics[0]["f_Hz"], F0, places=4)
        self.assertAlmostEqual(harmonics[1]["f_Hz"], 2*F0, places=4)
    
    def test_golden_harmonics(self):
        """Test golden ratio harmonics."""
        harmonics = self.freq.golden_harmonics(2)
        # Should include n=-2, -1, 0, 1, 2
        self.assertEqual(len(harmonics), 5)


class TestConsciousnessComponent(unittest.TestCase):
    """Test consciousness field component."""
    
    def setUp(self):
        self.consciousness = ConsciousnessComponent()
    
    def test_coherence_field_equation(self):
        """Test coherence field equation."""
        eq = self.consciousness.coherence_field_equation()
        self.assertIn("equation", eq)
        self.assertIn("∂²Ψ/∂t²", eq["equation"])
    
    def test_information_integration(self):
        """Test information integration metric."""
        result = self.consciousness.information_integration(A_eff=0.95)
        self.assertIn("Psi", result)
        self.assertEqual(result["coherence_level"], "maximum")
    
    def test_decoherence_time_extension(self):
        """Test decoherence time extension prediction."""
        tau_0 = 1e-6  # 1 microsecond
        result = self.consciousness.decoherence_time_extension(tau_0)
        
        # At f₀, should have maximum enhancement
        self.assertGreater(result["enhancement_factor"], 10)
        self.assertTrue(result["falsifiable"])
        
        # With detuning, enhancement should decrease
        result_detuned = self.consciousness.decoherence_time_extension(
            tau_0, f_drive=F0 + 10
        )
        self.assertLess(
            result_detuned["enhancement_factor"],
            result["enhancement_factor"]
        )


class TestGravityComponent(unittest.TestCase):
    """Test gravity component."""
    
    def setUp(self):
        self.gravity = GravityComponent()
    
    def test_yukawa_correction(self):
        """Test Yukawa correction calculation."""
        # At Earth-Moon distance
        r = 384400e3  # meters
        correction = self.gravity.yukawa_correction(r)
        
        self.assertIn("lambda_yukawa_km", correction)
        self.assertAlmostEqual(correction["lambda_yukawa_km"], 336.24, delta=0.5)
    
    def test_llr_prediction(self):
        """Test Lunar Laser Ranging prediction."""
        llr = self.gravity.llr_prediction()
        self.assertEqual(llr["experiment"], "Lunar Laser Ranging (LLR)")
        self.assertAlmostEqual(llr["lambda_yukawa_km"], 336.24, delta=0.5)
    
    def test_gravitational_wave_prediction(self):
        """Test GW prediction."""
        gw = self.gravity.gravitational_wave_prediction()
        self.assertAlmostEqual(gw["frequency_Hz"], F0, places=4)
        self.assertIn("LIGO Hanford", gw["detectors"])


class TestSpectrumComponent(unittest.TestCase):
    """Test spectral origin component."""
    
    def setUp(self):
        self.spectrum = SpectrumComponent()
    
    def test_spectral_derivation(self):
        """Test spectral derivation of f₀."""
        derivation = self.spectrum.spectral_derivation()
        
        self.assertIn("f0_derived_Hz", derivation)
        self.assertIn("f0_target_Hz", derivation)
        
        # Error should be small (within a few percent)
        self.assertLess(derivation["error_percent"], 5.0)


class TestCondensedMatterComponent(unittest.TestCase):
    """Test condensed matter predictions."""
    
    def setUp(self):
        self.cm = CondensedMatterComponent()
    
    def test_stm_prediction(self):
        """Test STM resonance prediction."""
        stm = self.cm.stm_prediction()
        
        self.assertEqual(stm["material"], "Bi₂Se₃ (topological insulator)")
        self.assertAlmostEqual(
            stm["prediction"]["voltage_mV"], 141.7, delta=0.1
        )
        self.assertEqual(stm["conditions"]["temperature"], "4 K")


class TestUnifiedTheory(unittest.TestCase):
    """Test unified theory integration."""
    
    def setUp(self):
        self.theory = UnifiedTheory()
    
    def test_cyclic_relationship(self):
        """Test cyclic relationship structure."""
        cycle = self.theory.cyclic_relationship()
        
        self.assertEqual(len(cycle["cycle"]), 7)
        self.assertEqual(cycle["cycle"][0], "Number (ζ)")
        self.assertEqual(cycle["cycle"][-1], "Number (ζ)")
    
    def test_all_falsifiable_predictions(self):
        """Test all falsifiable predictions."""
        predictions = self.theory.all_falsifiable_predictions()
        
        self.assertIn("gravitational_waves", predictions)
        self.assertIn("yukawa_correction", predictions)
        self.assertIn("quantum_coherence", predictions)
        self.assertIn("condensed_matter", predictions)
        self.assertIn("riemann_overtones", predictions)
    
    def test_riemann_hypothesis_connection(self):
        """Test RH connection."""
        rh = self.theory.riemann_hypothesis_connection()
        
        self.assertIn("first_10_overtones_kHz", rh)
        self.assertEqual(len(rh["first_10_overtones_kHz"]), 10)
        self.assertIn("LISA", rh["detectors"])
        self.assertIn("TianQin", rh["detectors"])
    
    def test_generate_report(self):
        """Test report generation."""
        report = self.theory.generate_report()
        
        self.assertIn("title", report)
        self.assertIn("fundamental_frequency", report)
        self.assertIn("cyclic_relationship", report)
        self.assertIn("falsifiable_predictions", report)
        self.assertIn("riemann_hypothesis", report)
    
    def test_json_serialization(self):
        """Test that report is JSON serializable."""
        report = self.theory.generate_report()
        # Should not raise
        json_str = json.dumps(report, default=str)
        self.assertIsInstance(json_str, str)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency checks."""
    
    def test_energy_frequency_relation(self):
        """Test E = hf relation."""
        constants = UnifiedTheoryConstants()
        h = 6.62607015e-34  # Planck constant
        expected_E = h * constants.f0
        self.assertAlmostEqual(constants.E_psi_J, expected_E, places=40)
    
    def test_wavelength_frequency_relation(self):
        """Test λ = c/f relation."""
        constants = UnifiedTheoryConstants()
        expected_lambda = c / constants.f0
        self.assertAlmostEqual(constants.lambda_psi, expected_lambda, places=2)
    
    def test_mass_energy_equivalence(self):
        """Test E = mc² relation."""
        constants = UnifiedTheoryConstants()
        expected_m = constants.E_psi_J / (c**2)
        self.assertAlmostEqual(constants.m_psi, expected_m, places=50)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
