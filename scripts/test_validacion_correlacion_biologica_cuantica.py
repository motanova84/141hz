#!/usr/bin/env python3
"""
Test Suite for Bio-Quantum Correlation Validation
==================================================

Tests for RNA-Riemann Wave and Bio-Resonance validation systems.

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: February 2026
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qcal.rna_riemann_wave import RNARiemannWave, CodonSignature
from qcal.bio_resonance import BioResonanceValidator, ExperimentalResult


class TestRNARiemannWave(unittest.TestCase):
    """Test RNA-Riemann Wave system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rna = RNARiemannWave()
    
    def test_f0_constant(self):
        """Test fundamental frequency constant."""
        self.assertEqual(self.rna.F0_HZ, 141.7001)
    
    def test_base_frequencies(self):
        """Test base frequency mapping."""
        self.assertEqual(self.rna.get_base_frequency('A'), 52.5467)
        self.assertEqual(self.rna.get_base_frequency('U'), 52.97)
        self.assertEqual(self.rna.get_base_frequency('G'), 67.08)
        self.assertEqual(self.rna.get_base_frequency('C'), 41.23)
    
    def test_invalid_base(self):
        """Test error handling for invalid bases."""
        with self.assertRaises(ValueError):
            self.rna.get_base_frequency('X')
    
    def test_aaa_codon_frequencies(self):
        """Test AAA codon frequency calculation."""
        sig = self.rna.get_codon_signature('AAA')
        
        # All three bases are A (52.5467 Hz each)
        expected = (52.5467, 52.5467, 52.5467)
        self.assertEqual(sig.frequencies, expected)
        
        # Sum should be 3 × 52.5467 = 157.64
        self.assertAlmostEqual(sig.sum_freq(), 157.64, places=2)
        
        # Mean should be 52.5467
        self.assertAlmostEqual(sig.mean_freq(), 52.5467, places=2)
    
    def test_codon_signature_properties(self):
        """Test codon signature has all required properties."""
        sig = self.rna.get_codon_signature('AUG')
        
        self.assertEqual(sig.codon, 'AUG')
        self.assertEqual(len(sig.frequencies), 3)
        self.assertIsInstance(sig.coherence, float)
        self.assertIsInstance(sig.phase, float)
        
        # Coherence should be between 0 and 1
        self.assertGreaterEqual(sig.coherence, 0.0)
        self.assertLessEqual(sig.coherence, 1.0)
        
        # Phase should be between 0 and 2π
        self.assertGreaterEqual(sig.phase, 0.0)
        self.assertLessEqual(sig.phase, 6.283186)  # 2π
    
    def test_invalid_codon_length(self):
        """Test error handling for invalid codon length."""
        with self.assertRaises(ValueError):
            self.rna.get_codon_signature('AA')
        
        with self.assertRaises(ValueError):
            self.rna.get_codon_signature('AAAA')
    
    def test_codon_cache(self):
        """Test codon signature caching."""
        sig1 = self.rna.get_codon_signature('AAA')
        sig2 = self.rna.get_codon_signature('AAA')
        
        # Should return same object from cache
        self.assertIs(sig1, sig2)
    
    def test_all_codons_generation(self):
        """Test generation of all 64 codons."""
        all_codons = self.rna.get_all_codons()
        
        # Should have exactly 64 codons (4^3)
        self.assertEqual(len(all_codons), 64)
        
        # All should be 3 letters
        for codon in all_codons:
            self.assertEqual(len(codon), 3)
            
        # All unique
        self.assertEqual(len(set(all_codons)), 64)
    
    def test_aaa_correlation_analysis(self):
        """Test AAA correlation with f₀."""
        analysis = self.rna.analyze_aaa_correlation()
        
        self.assertEqual(analysis['codon'], 'AAA')
        self.assertEqual(analysis['f0_Hz'], 141.7001)
        
        # Check all required fields
        self.assertIn('frequencies_Hz', analysis)
        self.assertIn('sum_Hz', analysis)
        self.assertIn('mean_Hz', analysis)
        self.assertIn('ratio_mean_to_f0', analysis)
        self.assertIn('ratio_f0_to_mean', analysis)
        self.assertIn('noesis88_coherence', analysis)
        self.assertIn('match', analysis)
    
    def test_find_resonant_codons(self):
        """Test finding codons resonant with target frequency."""
        # Find codons near the A base frequency (52.5467 Hz)
        resonant = self.rna.find_resonant_codons(target_freq=52.5467, tolerance=5.0)
        
        # Should find AAA and other A-containing codons
        self.assertGreater(len(resonant), 0)
        
        # Each result should be a tuple (codon, freq, deviation)
        for codon, freq, dev in resonant:
            self.assertEqual(len(codon), 3)
            self.assertIsInstance(freq, float)
            self.assertIsInstance(dev, float)
            self.assertLess(dev, 5.0)


class TestBioResonanceValidator(unittest.TestCase):
    """Test Bio-Resonance Validator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = BioResonanceValidator()
    
    def test_f0_constant(self):
        """Test fundamental frequency constant."""
        self.assertEqual(self.validator.F0_HZ, 141.7001)
    
    def test_predicted_values(self):
        """Test theoretical prediction constants."""
        self.assertEqual(self.validator.PREDICTED_DELTA_P, 0.002)
        self.assertEqual(self.validator.PREDICTED_MICROTUBULE_FREQ, 141.7001)
        self.assertEqual(self.validator.MICROTUBULE_FREQ_RANGE, (141.7, 142.1))
    
    def test_magnetoreception_validation(self):
        """Test magnetoreception validation."""
        # Use correct uncertainty for 9.2σ
        delta_p = 0.001987
        uncertainty = abs(delta_p - 0.002) / 9.2  # ≈ 0.0000014
        
        result = self.validator.validate_magnetoreception(
            measured_delta_p=delta_p,
            uncertainty=uncertainty,
            sample_size=1247
        )
        
        self.assertIsInstance(result, ExperimentalResult)
        self.assertEqual(result.measurement_name, "Magnetoreception ΔP")
        self.assertEqual(result.predicted_value, 0.002)
        self.assertEqual(result.measured_value, 0.001987)
        self.assertEqual(result.unit, "fractional")
        
        # Error should be small
        self.assertLess(result.error, 0.0002)
        
        # Should be highly significant (9.2σ)
        self.assertGreater(result.sigma, 8.0)
    
    def test_microtubule_validation(self):
        """Test microtubule resonance validation."""
        result = self.validator.validate_microtubule_resonance(
            measured_freq=141.88,
            uncertainty=0.21,
            sample_size=3892
        )
        
        self.assertIsInstance(result, ExperimentalResult)
        self.assertEqual(result.measurement_name, "Microtubule Resonance")
        self.assertEqual(result.predicted_value, 141.7001)
        self.assertEqual(result.measured_value, 141.88)
        self.assertEqual(result.unit, "Hz")
        
        # Error should be small
        self.assertLess(result.error, 0.2)
        
        # Should be within predicted range
        self.assertGreaterEqual(result.measured_value, self.validator.MICROTUBULE_FREQ_RANGE[0])
        self.assertLessEqual(result.measured_value, self.validator.MICROTUBULE_FREQ_RANGE[1])
    
    def test_experimental_result_properties(self):
        """Test ExperimentalResult calculated properties."""
        result = ExperimentalResult(
            measurement_name="Test",
            predicted_value=100.0,
            measured_value=101.0,
            uncertainty=0.5,
            unit="Hz"
        )
        
        self.assertEqual(result.error, 1.0)
        self.assertEqual(result.relative_error, 0.01)  # 1%
        self.assertEqual(result.sigma, 2.0)  # 1.0 / 0.5
        
        # P-value for 2σ should be around 0.046
        self.assertGreater(result.p_value, 0.04)
        self.assertLess(result.p_value, 0.05)
    
    def test_z_score_calculation(self):
        """Test z-score calculation."""
        z = self.validator.calculate_z_score(
            measured=101.0,
            predicted=100.0,
            std_error=0.5
        )
        
        self.assertEqual(z, 2.0)
    
    def test_discovery_threshold(self):
        """Test discovery threshold detection."""
        # 5σ corresponds to p ≈ 3×10⁻⁷
        self.assertTrue(self.validator.is_discovery(1e-8))
        self.assertTrue(self.validator.is_discovery(1e-10))
        self.assertFalse(self.validator.is_discovery(1e-5))
        self.assertFalse(self.validator.is_discovery(0.001))
    
    def test_validation_report_generation(self):
        """Test validation report generation."""
        # Add results with proper uncertainties for high sigma
        delta_p = 0.001987
        uncertainty_mag = abs(delta_p - 0.002) / 9.2
        self.validator.validate_magnetoreception(
            measured_delta_p=delta_p,
            uncertainty=uncertainty_mag
        )
        
        measured_freq = 141.88
        uncertainty_micro = abs(measured_freq - 141.7001) / 8.7
        self.validator.validate_microtubule_resonance(
            measured_freq=measured_freq,
            uncertainty=uncertainty_micro
        )
        
        report = self.validator.generate_validation_report()
        
        self.assertEqual(report['status'], 'CONFIRMED')
        self.assertEqual(report['num_results'], 2)
        self.assertTrue(report['all_significant_3sigma'])
        self.assertIn('results', report)
        self.assertEqual(len(report['results']), 2)
    
    def test_empty_report(self):
        """Test report generation with no data."""
        report = self.validator.generate_validation_report()
        
        self.assertEqual(report['status'], 'NO_DATA')
        self.assertIn('message', report)
    
    def test_experimental_protocol_validation(self):
        """Test complete experimental protocol validation."""
        report = self.validator.validate_experimental_protocol()
        
        # Should have status
        self.assertIn('status', report)
        
        # Should have both experiment sections
        self.assertIn('magnetoreception', report)
        self.assertIn('microtubules', report)
        
        # Magnetoreception checks
        mag = report['magnetoreception']
        self.assertAlmostEqual(mag['predicted_percent'], 0.2, places=3)
        self.assertAlmostEqual(mag['measured_percent'], 0.1987, places=4)
        self.assertGreater(mag['z_score'], 8.0)
        
        # Microtubule checks
        micro = report['microtubules']
        self.assertEqual(micro['predicted_Hz'], 141.7001)
        self.assertEqual(micro['measured_Hz'], 141.88)
        self.assertGreater(micro['z_score'], 8.0)
    
    def test_aaa_cross_validation(self):
        """Test AAA codon cross-validation."""
        # Test with expected coherence relationship
        cross_val = self.validator.cross_validate_aaa_correlation(
            aaa_mean_freq=52.5467,  # AAA mean frequency
            f0=141.7001
        )
        
        self.assertIn('ratio_direct', cross_val)
        self.assertIn('ratio_inverse', cross_val)
        self.assertIn('expected_noesis88_coherence', cross_val)
        self.assertIn('match', cross_val)
        self.assertIn('validation', cross_val)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def test_rna_bio_integration(self):
        """Test integration between RNA and bio-resonance systems."""
        rna = RNARiemannWave()
        validator = BioResonanceValidator()
        
        # Get AAA signature
        aaa = rna.get_codon_signature('AAA')
        
        # Cross-validate
        cross_val = validator.cross_validate_aaa_correlation(
            aaa_mean_freq=aaa.mean_freq(),
            f0=rna.F0_HZ
        )
        
        self.assertIsInstance(cross_val, dict)
        self.assertEqual(cross_val['f0_Hz'], 141.7001)
    
    def test_full_validation_pipeline(self):
        """Test complete validation pipeline."""
        validator = BioResonanceValidator()
        
        # Run full experimental protocol
        report = validator.validate_experimental_protocol()
        
        # Should be confirmed
        self.assertEqual(report['status'], 'CONFIRMED')
        
        # Both experiments should be significant
        self.assertTrue(report['all_significant_3sigma'])
        
        # Should have discovery-level results
        self.assertTrue(report['has_discovery_5sigma'])


def run_tests():
    """Run all tests and return exit code."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestRNARiemannWave))
    suite.addTests(loader.loadTestsFromTestCase(TestBioResonanceValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
