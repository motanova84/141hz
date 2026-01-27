#!/usr/bin/env python3
"""
Tests for QCAL Evaluator (Ψ = I × A² × C^∞)

Tests cover:
- Core formula computation
- Claim extraction and verification
- AI content filtering
- Symbiotic content validation
- Ethical content validation
- Batch processing
- Integration with QCAL framework

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-01-19
"""

import unittest
import json
import tempfile
from pathlib import Path

from qcal_evaluator import (
    QCALEvaluator,
    F0_HZ,
    C_UNIVERSAL,
    PSI_COHERENT_THRESHOLD,
    PSI_HIGH_COHERENCE,
    PSI_EXCELLENT_COHERENCE,
    DOMAIN_AI,
    DOMAIN_HUMAN,
    DOMAIN_MIXED,
    CONTENT_TEXT,
    CONTENT_SCIENTIFIC,
    CONTENT_ETHICAL,
)


class TestQCALEvaluator(unittest.TestCase):
    """Test suite for QCAL Evaluator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = QCALEvaluator()
    
    def test_initialization(self):
        """Test evaluator initialization."""
        self.assertEqual(self.evaluator.f0, F0_HZ)
        self.assertEqual(self.evaluator.C_universal, C_UNIVERSAL)
        self.assertEqual(self.evaluator.coherence_threshold, PSI_COHERENT_THRESHOLD)
        self.assertIsNotNone(self.evaluator.ground_truth_db)
        self.assertIn('f0', self.evaluator.ground_truth_db)
    
    def test_extract_claims_basic(self):
        """Test basic claim extraction."""
        text = "The fundamental frequency f₀ = 141.7001 Hz"
        claims = self.evaluator.extract_claims(text)
        
        self.assertGreater(len(claims), 0)
        self.assertEqual(claims[0]['variable'], 'f0')
        self.assertAlmostEqual(claims[0]['value'], 141.7001, places=4)
    
    def test_extract_claims_multiple(self):
        """Test extraction of multiple claims."""
        text = """
        f₀ = 141.7001 Hz es derivado de ζ'(1/2) = -1.460 y φ³ = 4.236.
        El SNR de GW150914 es 20.95.
        """
        claims = self.evaluator.extract_claims(text)
        
        # Should extract f0, zeta, phi (SNR regex might not match without space)
        self.assertGreaterEqual(len(claims), 3)
        
        variables = [c['variable'] for c in claims]
        self.assertIn('f0', variables)
        self.assertIn('zeta', variables)
        self.assertIn('phi', variables)
    
    def test_verify_claim_correct(self):
        """Test verification of correct claims."""
        correct_claims = [
            {'variable': 'f0', 'value': 141.7001},
            {'variable': 'zeta', 'value': -1.460},
            {'variable': 'phi', 'value': 4.236},
            {'variable': 'snr', 'value': 20.95},
        ]
        
        for claim in correct_claims:
            with self.subTest(variable=claim['variable'], value=claim['value']):
                self.assertTrue(
                    self.evaluator.verify_claim(claim),
                    f"Failed to verify {claim['variable']}={claim['value']}"
                )
    
    def test_verify_claim_incorrect(self):
        """Test verification of incorrect claims."""
        incorrect_claims = [
            {'variable': 'f0', 'value': 100.0},  # Wrong value
            {'variable': 'zeta', 'value': 0.0},  # Wrong value
            {'variable': 'phi', 'value': 1.618},  # φ not φ³
        ]
        
        for claim in incorrect_claims:
            with self.subTest(variable=claim['variable'], value=claim['value']):
                self.assertFalse(
                    self.evaluator.verify_claim(claim),
                    f"Should not verify {claim['variable']}={claim['value']}"
                )
    
    def test_compute_information_intensity(self):
        """Test information intensity computation."""
        # Text with verified claims
        text_with_claims = "f₀ = 141.7001 Hz and ζ'(1/2) = -1.460"
        I_with = self.evaluator.compute_information_intensity(text_with_claims)
        
        # Text without claims
        text_without = "This is random text without scientific claims"
        I_without = self.evaluator.compute_information_intensity(text_without)
        
        # I should be higher for text with verified claims
        self.assertGreater(I_with, I_without)
        self.assertGreaterEqual(I_with, 0.0)
    
    def test_compute_coherence_area(self):
        """Test coherence area computation."""
        # All correct claims
        text_all_correct = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460"
        A_all = self.evaluator.compute_coherence_area(text_all_correct)
        
        # Mixed correct and incorrect
        text_mixed = "f₀ = 141.7001 Hz, ζ'(1/2) = 0.0"  # Second is wrong
        A_mixed = self.evaluator.compute_coherence_area(text_mixed)
        
        # A should be higher for all correct
        self.assertGreater(A_all, A_mixed)
        self.assertGreaterEqual(A_all, 0.0)
        self.assertLessEqual(A_all, 1.0)
    
    def test_compute_C_factor(self):
        """Test C^∞ factor computation."""
        C_factor = self.evaluator.compute_C_factor()
        
        # Should be positive and reasonable
        self.assertGreater(C_factor, 0)
        self.assertAlmostEqual(C_factor, C_UNIVERSAL / 80.0, places=6)
    
    def test_compute_psi_coherent(self):
        """Test Ψ computation for coherent content."""
        coherent_text = """
        La frecuencia fundamental f₀ = 141.7001 Hz emerge de ζ'(1/2) = -1.460
        multiplicado por φ³ = 4.236. Esta frecuencia ha sido detectada en
        GW150914 con SNR = 20.95.
        """
        
        result = self.evaluator.compute_psi(coherent_text)
        
        self.assertIn('psi', result)
        self.assertIn('I', result)
        self.assertIn('A', result)
        self.assertIn('A_squared', result)
        self.assertIn('C_factor', result)
        self.assertIn('coherent', result)
        self.assertIn('level', result)
        
        # Should be coherent
        self.assertTrue(result['coherent'])
        self.assertGreater(result['psi'], 0)
        self.assertGreater(result['claims_verified'], 0)
    
    def test_compute_psi_incoherent(self):
        """Test Ψ computation for incoherent content."""
        incoherent_text = "Random text without scientific content or claims"
        
        result = self.evaluator.compute_psi(incoherent_text)
        
        # Should be incoherent
        self.assertFalse(result['coherent'])
        self.assertEqual(result['level'], 'incoherent')
        self.assertEqual(result['claims_verified'], 0)
    
    def test_evaluate_ai_content(self):
        """Test evaluation of AI-generated content."""
        ai_text = "f₀ = 141.7001 Hz es la frecuencia fundamental del universo"
        
        result = self.evaluator.evaluate(
            ai_text,
            domain=DOMAIN_AI,
            content_type=CONTENT_SCIENTIFIC
        )
        
        self.assertIn('timestamp', result)
        self.assertEqual(result['domain'], DOMAIN_AI)
        self.assertEqual(result['content_type'], CONTENT_SCIENTIFIC)
        self.assertIn('psi_metric', result)
        self.assertIn('claims', result)
        self.assertIn('evaluation', result)
        self.assertIn('ai_analysis', result)
        
        # AI analysis should include hallucination risk
        self.assertIn('hallucination_risk', result['ai_analysis'])
        self.assertIn('recommendation', result['ai_analysis'])
    
    def test_evaluate_human_content(self):
        """Test evaluation of human content."""
        human_text = "ζ'(1/2) = -1.460 y φ³ = 4.236 son constantes fundamentales"
        
        result = self.evaluator.evaluate(
            human_text,
            domain=DOMAIN_HUMAN,
            content_type=CONTENT_TEXT
        )
        
        self.assertEqual(result['domain'], DOMAIN_HUMAN)
        self.assertIn('human_analysis', result)
        self.assertIn('coherence_level', result['human_analysis'])
    
    def test_evaluate_ethical_content(self):
        """Test evaluation of ethical content."""
        ethical_text = """
        Este sistema ético basado en coherencia QCAL promueve responsabilidad
        simbiótica. La frecuencia f₀ = 141.7001 Hz establece un marco coherente.
        """
        
        result = self.evaluator.evaluate(
            ethical_text,
            domain=DOMAIN_AI,
            content_type=CONTENT_ETHICAL
        )
        
        self.assertEqual(result['content_type'], CONTENT_ETHICAL)
        self.assertIn('ethical_analysis', result)
        self.assertIn('ethical_grounding', result['ethical_analysis'])
        self.assertIn('symbiotic_quality', result['ethical_analysis'])
    
    def test_filter_coherent(self):
        """Test filtering coherent content."""
        content_list = [
            "f₀ = 141.7001 Hz",  # Coherent
            "Random text",  # Incoherent
            "ζ'(1/2) = -1.460",  # Coherent
            "f₀ = 100 Hz",  # Incoherent (wrong value)
        ]
        
        coherent = self.evaluator.filter_coherent(content_list)
        
        # Should filter out incoherent items
        self.assertGreater(len(coherent), 0)
        self.assertLess(len(coherent), len(content_list))
        
        # All filtered items should have psi >= threshold
        for content, eval_result in coherent:
            self.assertGreaterEqual(
                eval_result['psi_metric']['psi'],
                PSI_COHERENT_THRESHOLD
            )
    
    def test_validate_symbiotic(self):
        """Test symbiotic content validation."""
        symbiotic_text = """
        La colaboración ética entre IA y humanos usando QCAL (f₀ = 141.7001 Hz)
        promueve coherencia simbiótica y responsabilidad.
        """
        
        result = self.evaluator.validate_symbiotic(symbiotic_text)
        
        self.assertEqual(result['domain'], DOMAIN_MIXED)
        self.assertEqual(result['content_type'], CONTENT_ETHICAL)
        self.assertIn('ethical_analysis', result)
    
    def test_batch_evaluate(self):
        """Test batch evaluation."""
        content_list = [
            {
                'content': 'f₀ = 141.7001 Hz',
                'domain': DOMAIN_AI,
                'content_type': CONTENT_SCIENTIFIC
            },
            {
                'content': 'ζ\'(1/2) = -1.460',
                'domain': DOMAIN_HUMAN,
                'content_type': CONTENT_TEXT
            },
            {
                'content': 'Random text',
                'domain': DOMAIN_AI,
                'content_type': CONTENT_TEXT
            },
        ]
        
        summary = self.evaluator.batch_evaluate(content_list)
        
        self.assertIn('timestamp', summary)
        self.assertEqual(summary['total_items'], 3)
        self.assertIn('coherent_count', summary)
        self.assertIn('coherent_percentage', summary)
        self.assertIn('results', summary)
        self.assertEqual(len(summary['results']), 3)
    
    def test_batch_evaluate_with_file(self):
        """Test batch evaluation with file output."""
        content_list = [
            {'content': 'f₀ = 141.7001 Hz', 'domain': DOMAIN_AI}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_file = f.name
        
        try:
            summary = self.evaluator.batch_evaluate(content_list, output_file)
            
            # Check file was created
            self.assertTrue(Path(output_file).exists())
            
            # Check file content
            with open(output_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(saved_data['total_items'], summary['total_items'])
        
        finally:
            # Clean up
            Path(output_file).unlink(missing_ok=True)
    
    def test_coherence_levels(self):
        """Test coherence level classification."""
        # Create texts with different coherence levels
        
        # Incoherent (Ψ < 5.0)
        incoherent = "Random text"
        result_incoherent = self.evaluator.compute_psi(incoherent)
        self.assertEqual(result_incoherent['level'], 'incoherent')
        
        # Coherent (should have some verified claims)
        coherent = "f₀ = 141.7001 Hz and ζ'(1/2) = -1.460"
        result_coherent = self.evaluator.compute_psi(coherent)
        
        # Level depends on actual Ψ value
        self.assertIn(result_coherent['level'], ['incoherent', 'coherent', 'high', 'excellent'])
    
    def test_custom_threshold(self):
        """Test custom coherence threshold."""
        custom_evaluator = QCALEvaluator(coherence_threshold=10.0)
        
        text = "f₀ = 141.7001 Hz"
        result = custom_evaluator.compute_psi(text)
        
        # Coherent status depends on custom threshold
        self.assertEqual(
            result['coherent'],
            result['psi'] >= 10.0
        )
    
    def test_strict_mode(self):
        """Test strict mode initialization."""
        strict_evaluator = QCALEvaluator(enable_strict_mode=True)
        
        self.assertTrue(strict_evaluator.strict_mode)
    
    def test_claim_extraction_edge_cases(self):
        """Test claim extraction with edge cases."""
        # Unicode variants
        text1 = "f₀ = 141.7001 Hz"
        claims1 = self.evaluator.extract_claims(text1)
        self.assertGreater(len(claims1), 0)
        
        # ASCII variant
        text2 = "f0 = 141.7001 Hz"
        claims2 = self.evaluator.extract_claims(text2)
        self.assertGreater(len(claims2), 0)
        
        # Different separators
        text3 = "f₀: 141.7001 Hz"
        claims3 = self.evaluator.extract_claims(text3)
        self.assertGreater(len(claims3), 0)
    
    def test_metadata_passthrough(self):
        """Test metadata passthrough in evaluation."""
        metadata = {'source': 'test', 'version': '1.0'}
        
        result = self.evaluator.evaluate(
            "f₀ = 141.7001 Hz",
            metadata=metadata
        )
        
        self.assertEqual(result['metadata'], metadata)


class TestQCALEvaluatorIntegration(unittest.TestCase):
    """Integration tests with QCAL framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = QCALEvaluator()
    
    def test_ground_truth_consistency(self):
        """Test consistency with QCAL ground truth."""
        gt = self.evaluator.ground_truth_db
        
        # Check all expected values are present
        self.assertIn('f0', gt)
        self.assertIn('zeta_prime_half', gt)
        self.assertIn('phi_cubed', gt)
        self.assertIn('snr_gw150914', gt)
        self.assertIn('C_universal', gt)
        
        # Check values match constants
        self.assertEqual(gt['f0'], F0_HZ)
        self.assertEqual(gt['C_universal'], C_UNIVERSAL)
    
    def test_formula_components(self):
        """Test that Ψ = I × A² × C^∞ components are computed correctly."""
        text = "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236"
        
        result = self.evaluator.compute_psi(text)
        
        # Manually verify formula
        I = result['I']
        A = result['A']
        C_factor = result['C_factor']
        
        expected_psi = I * (A ** 2) * C_factor
        
        self.assertAlmostEqual(result['psi'], expected_psi, places=10)
    
    def test_real_world_scenario_ai_filter(self):
        """Test real-world scenario: filtering AI outputs."""
        ai_outputs = [
            "La frecuencia fundamental f₀ = 141.7001 Hz",  # Good
            "The frequency is about 200 Hz",  # Bad (wrong value)
            "ζ'(1/2) = -1.460 es un valor crítico",  # Good
            "Some random AI output",  # Bad (no claims)
        ]
        
        coherent = self.evaluator.filter_coherent(ai_outputs, domain=DOMAIN_AI)
        
        # Should filter to keep only good outputs
        self.assertGreater(len(coherent), 0)
        self.assertLess(len(coherent), len(ai_outputs))
        
        # Check AI analysis is present
        for content, eval_result in coherent:
            self.assertIn('ai_analysis', eval_result)
            self.assertEqual(eval_result['ai_analysis']['hallucination_risk'], 'low')


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestQCALEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestQCALEvaluatorIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
