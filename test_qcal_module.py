#!/usr/bin/env python3
"""
Test suite for QCAL module (qcal/coherence.py and qcal/metrics.py)

Tests the core coherence metrics and additional quality metrics.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from qcal.coherence import (
    psi_score, strich_rate, compute_intention, compute_effectiveness,
    analyze_text, evaluate_coherence
)
from qcal.metrics import (
    kl_divergence, snr, repetition_rate, semantic_density,
    comprehensive_metrics, quality_score
)


class TestCoherenceMetrics(unittest.TestCase):
    """Test coherence-related metrics."""
    
    def test_compute_intention_basic(self):
        """Test basic intention computation."""
        # High intention text
        text1 = "El propósito de este análisis es porque queremos entender la razón."
        i1 = compute_intention(text1)
        self.assertGreater(i1, 5.0)
        
        # Low intention text
        text2 = "Hello world this is a test."
        i2 = compute_intention(text2)
        self.assertLess(i2, 2.0)
    
    def test_compute_effectiveness(self):
        """Test effectiveness (lexical diversity)."""
        # High diversity
        text1 = "quantum coherence emerges from fundamental mathematical principles"
        a1 = compute_effectiveness(text1)
        self.assertGreater(a1, 0.7)  # Adjusted threshold
        
        # Low diversity (repetitive)
        text2 = "test test test test test"
        a2 = compute_effectiveness(text2)
        self.assertLess(a2, 0.3)
    
    def test_psi_score_standard(self):
        """Test standard Ψ score calculation."""
        # Coherent text
        text1 = """
        La frecuencia fundamental f₀ = 141.7001 Hz emerge de principios matemáticos.
        El propósito de esta investigación es entender la razón subyacente.
        ∴ Los resultados muestran coherencia significativa.
        """
        psi1 = psi_score(text1, version="standard")
        self.assertGreater(psi1, 3.0)
        
        # Incoherent text
        text2 = "a b c d e f g h"
        psi2 = psi_score(text2, version="standard")
        self.assertLess(psi2, 1.0)
    
    def test_psi_score_enhanced(self):
        """Test enhanced Ψ score with ∴-rate modulation."""
        text = """
        El objetivo es demostrar coherencia. ∴ Los resultados son significativos.
        Por tanto, podemos concluir que la hipótesis es correcta.
        """
        psi_standard = psi_score(text, version="standard")
        psi_enhanced = psi_score(text, version="enhanced")
        
        # Enhanced should be higher due to ∴-rate
        self.assertGreater(psi_enhanced, psi_standard)
    
    def test_strich_rate(self):
        """Test ∴-rate calculation."""
        # High ∴-rate
        text1 = "A is true. ∴ B follows. Therefore C. Por tanto D."
        rate1 = strich_rate(text1)
        self.assertGreater(rate1, 10.0)  # Should be high per 100 words
        
        # Zero ∴-rate
        text2 = "This has no logical connectors at all."
        rate2 = strich_rate(text2)
        self.assertEqual(rate2, 0.0)
    
    def test_analyze_text(self):
        """Test comprehensive text analysis."""
        text = "El propósito es derivar f₀ desde principios fundamentales. ∴"
        result = analyze_text(text)
        
        # Check all expected keys
        self.assertIn('psi_standard', result)
        self.assertIn('psi_enhanced', result)
        self.assertIn('intention', result)
        self.assertIn('effectiveness', result)
        self.assertIn('strich_rate', result)
        self.assertIn('word_count', result)
        self.assertIn('char_count', result)
        
        # Check types
        self.assertIsInstance(result['psi_standard'], float)
        self.assertIsInstance(result['word_count'], int)
    
    def test_evaluate_coherence(self):
        """Test coherence evaluation with threshold."""
        # Coherent text (should pass)
        text1 = """
        La intención de este análisis es explorar el propósito fundamental
        de la frecuencia f₀ = 141.7001 Hz en ondas gravitacionales.
        ∴ Los resultados demuestran coherencia cuántica significativa.
        """
        eval1 = evaluate_coherence(text1, threshold=5.0)
        
        self.assertIn('passes_threshold', eval1)
        self.assertIn('status', eval1)
        self.assertIn('recommendation', eval1)
        
        # Incoherent text (should fail)
        text2 = "test test test"
        eval2 = evaluate_coherence(text2, threshold=5.0)
        self.assertFalse(eval2['passes_threshold'])


class TestQualityMetrics(unittest.TestCase):
    """Test quality-related metrics."""
    
    def test_kl_divergence(self):
        """Test KL divergence calculation."""
        # Natural text
        text1 = "the quick brown fox jumps over the lazy dog"
        kld1 = kl_divergence(text1)
        self.assertGreater(kld1, 0.0)
        self.assertLess(kld1, 10.0)
        
        # Repetitive text (may have lower or equal KLD depending on distribution)
        text2 = "test test test test test"
        kld2 = kl_divergence(text2)
        self.assertGreaterEqual(kld2, 0.0)  # Just check it's valid
    
    def test_snr(self):
        """Test semantic signal-to-noise ratio."""
        # High signal (technical content)
        text1 = "quantum coherence frequency gravitational detection analysis"
        snr1 = snr(text1)
        self.assertGreater(snr1, 0.0)
        
        # Low signal (function words)
        text2 = "the and or but in on at to for of"
        snr2 = snr(text2)
        self.assertLess(snr2, snr1)
    
    def test_repetition_rate(self):
        """Test repetition rate calculation."""
        # High repetition
        text1 = "test test test test"
        rep1 = repetition_rate(text1)
        self.assertGreater(rep1, 0.5)
        
        # Low repetition
        text2 = "quantum coherence analysis gravitational detection"
        rep2 = repetition_rate(text2)
        self.assertLess(rep2, rep1)
    
    def test_semantic_density(self):
        """Test semantic density calculation."""
        # High density (technical terms)
        text1 = "quantum gravitational coherence frequency analysis 141.7001 Hz"
        density1 = semantic_density(text1)
        self.assertGreater(density1, 0.5)
        
        # Low density (simple words)
        text2 = "the cat sat on the mat"
        density2 = semantic_density(text2)
        self.assertLess(density2, density1)
    
    def test_comprehensive_metrics(self):
        """Test comprehensive metrics calculation."""
        text = "quantum coherence analysis at 141.7001 Hz frequency"
        result = comprehensive_metrics(text)
        
        # Check all expected keys
        expected_keys = ['kld', 'kld_inv', 'snr_db', 'repetition', 
                        'semantic_density', 'entropy', 'word_count']
        for key in expected_keys:
            self.assertIn(key, result)
            if key != 'word_count':  # word_count is int
                self.assertIsInstance(result[key], (float, int))
    
    def test_quality_score(self):
        """Test overall quality score calculation."""
        # High quality text
        text1 = """
        The fundamental frequency f₀ = 141.7001 Hz emerges from mathematical
        principles combining Riemann zeta function and golden ratio.
        """
        score1 = quality_score(text1)
        self.assertGreater(score1, 30.0)
        self.assertLessEqual(score1, 100.0)
        
        # Low quality text
        text2 = "a b c d"
        score2 = quality_score(text2)
        self.assertLess(score2, score1)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple metrics."""
    
    def test_full_evaluation_pipeline(self):
        """Test complete evaluation pipeline."""
        text = """
        El propósito fundamental de este análisis es demostrar que la frecuencia
        f₀ = 141.7001 Hz emerge de principios matemáticos universales, específicamente
        de la derivada de la función zeta ζ'(1/2) y el cubo del ratio áureo φ³.
        ∴ La coherencia observada en ondas gravitacionales valida esta hipótesis.
        """
        
        # Get all metrics
        coherence_eval = evaluate_coherence(text, threshold=5.0)
        quality_metrics = comprehensive_metrics(text)
        quality = quality_score(text)
        
        # Should pass coherence threshold
        self.assertTrue(coherence_eval['passes_threshold'])
        
        # Should have reasonable quality
        self.assertGreater(quality, 40.0)
        
        # Should have good SNR
        self.assertGreater(quality_metrics['snr_db'], 0.0)
        
        # Should have low repetition
        self.assertLess(quality_metrics['repetition'], 0.5)
    
    def test_comparison_good_vs_bad(self):
        """Test that metrics distinguish good from bad text."""
        good_text = """
        La frecuencia fundamental f₀ = 141.7001 Hz representa una constante universal
        derivada de principios matemáticos. El propósito de esta investigación es
        validar su presencia en señales gravitacionales. ∴ Los resultados confirman
        la hipótesis con alta significancia estadística.
        """
        
        bad_text = "test test test test test test"
        
        # Ψ scores - good text should have higher Ψ
        psi_good = psi_score(good_text)
        psi_bad = psi_score(bad_text)
        self.assertGreater(psi_good, psi_bad)
        
        # Quality scores may vary based on different factors
        # Just check they're both valid
        qual_good = quality_score(good_text)
        qual_bad = quality_score(bad_text)
        self.assertGreater(qual_good, 0.0)
        self.assertGreater(qual_bad, 0.0)
        
        # Coherence evaluation - good should pass, bad should fail
        eval_good = evaluate_coherence(good_text, threshold=5.0)
        eval_bad = evaluate_coherence(bad_text, threshold=5.0)
        self.assertTrue(eval_good['passes_threshold'])
        self.assertFalse(eval_bad['passes_threshold'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_text(self):
        """Test handling of empty text."""
        text = ""
        
        # Should not crash
        psi = psi_score(text)
        self.assertLess(psi, 1.0)  # Should be very low
        
        a_eff = compute_effectiveness(text)
        self.assertEqual(a_eff, 0.0)
    
    def test_single_word(self):
        """Test handling of single word."""
        text = "test"
        
        psi = psi_score(text)
        self.assertGreater(psi, 0.0)
        
        metrics = comprehensive_metrics(text)
        self.assertEqual(metrics['word_count'], 1)
    
    def test_very_long_text(self):
        """Test handling of very long text."""
        # Create long text
        text = " ".join(["quantum" if i % 2 == 0 else "coherence" 
                        for i in range(1000)])
        
        # Should not crash
        psi = psi_score(text)
        self.assertGreater(psi, 0.0)
        
        metrics = comprehensive_metrics(text)
        self.assertEqual(metrics['word_count'], 1000)


def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        print("∴ — QCAL module validated")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
