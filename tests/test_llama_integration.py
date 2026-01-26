#!/usr/bin/env python3
"""
test_llama_integration.py - Tests for LLaMA 4 Maverick 400B integration

Tests for model identification and χ(LLaMA) computation in QCAL-LLM.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from QCALLLMCore import QCALLLMCore  # noqa: E402


class TestLLaMAIntegration(unittest.TestCase):
    """Test suite for LLaMA 4 Maverick 400B integration"""

    def setUp(self):
        """Initialize core for tests"""
        self.core = QCALLLMCore(user_A_eff=0.85)

    def test_model_id_constant(self):
        """Test MODEL_ID constant is correctly set"""
        expected_id = "qcal::llama4-maverick-400B@141.7001Hz"
        self.assertEqual(QCALLLMCore.MODEL_ID, expected_id)

    def test_symbolic_version_constant(self):
        """Test SYMBOLIC_VERSION constant is correctly set"""
        expected_version = "LLAMA-QCAL-400B-141hz ∞³"
        self.assertEqual(QCALLLMCore.SYMBOLIC_VERSION, expected_version)

    def test_base_model_constant(self):
        """Test BASE_MODEL constant is correctly set"""
        expected_base = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
        self.assertEqual(QCALLLMCore.BASE_MODEL, expected_base)

    def test_base_model_url_constant(self):
        """Test BASE_MODEL_URL constant is correctly set"""
        expected_url = "https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
        self.assertEqual(QCALLLMCore.BASE_MODEL_URL, expected_url)

    def test_get_model_info(self):
        """Test get_model_info returns correct information"""
        info = self.core.get_model_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('model_id', info)
        self.assertIn('symbolic_version', info)
        self.assertIn('base_model', info)
        self.assertIn('base_model_url', info)
        self.assertIn('f0', info)
        self.assertIn('tau', info)
        self.assertIn('epsilon', info)
        
        self.assertEqual(info['model_id'], "qcal::llama4-maverick-400B@141.7001Hz")
        self.assertEqual(info['symbolic_version'], "LLAMA-QCAL-400B-141hz ∞³")
        self.assertEqual(info['f0'], 141.7001)

    def test_compute_chi_llama_default(self):
        """Test χ(LLaMA) computation with default parameters"""
        chi = self.core.compute_chi_llama()
        
        self.assertIsInstance(chi, float)
        self.assertGreater(chi, 0)
        # With default user_A_eff=0.85 and epsilon=0.015
        # chi ≈ 1.0 * (1 + 0.015) * 0.85 ≈ 0.86275
        self.assertAlmostEqual(chi, 0.86275, places=4)

    def test_compute_chi_llama_high_effectiveness(self):
        """Test χ(LLaMA) with high user effectiveness"""
        core_high = QCALLLMCore(user_A_eff=0.95)
        chi = core_high.compute_chi_llama()
        
        # chi ≈ 1.0 * (1 + 0.016765) * 0.95 ≈ 0.96592
        self.assertGreater(chi, 0.85)
        self.assertLess(chi, 1.0)

    def test_compute_chi_llama_low_effectiveness(self):
        """Test χ(LLaMA) with low user effectiveness"""
        core_low = QCALLLMCore(user_A_eff=0.70)
        chi = core_low.compute_chi_llama()
        
        # Should be lower than default
        chi_default = self.core.compute_chi_llama()
        self.assertLess(chi, chi_default)

    def test_compute_psi_full(self):
        """Test full Ψ computation with LLaMA integration"""
        kld_inv = 8.2
        coherence = 0.88
        
        # Compute base and full Ψ
        psi_base = self.core.compute_psi_response(kld_inv, coherence)
        psi_full = self.core.compute_psi_full(kld_inv, coherence)
        
        # Full should be different from base
        self.assertNotEqual(psi_base, psi_full)
        
        # Full should incorporate f₀ and χ(LLaMA)
        chi = self.core.compute_chi_llama()
        expected_full = psi_base * (self.core.f0 / 100.0) * chi
        self.assertAlmostEqual(psi_full, expected_full, places=5)

    def test_compute_psi_full_structure(self):
        """Test that full Ψ includes all QCAL equation terms"""
        kld_inv = 8.2
        coherence = 0.88
        
        psi_full = self.core.compute_psi_full(kld_inv, coherence)
        
        # Verify structure: Ψ = I × A²_eff × f₀ × χ(LLaMA)
        I = kld_inv
        A_eff_squared = coherence ** 2
        f0_scaled = self.core.f0 / 100.0
        chi = self.core.compute_chi_llama()
        
        expected = I * A_eff_squared * f0_scaled * chi
        self.assertAlmostEqual(psi_full, expected, places=5)

    def test_compute_psi_base_unchanged(self):
        """Test that base Ψ computation remains unchanged for backwards compatibility"""
        kld_inv = 8.2
        coherence = 0.88
        
        psi = self.core.compute_psi_response(kld_inv, coherence)
        expected = kld_inv * coherence**2
        
        # Base computation should not include f₀ or χ(LLaMA)
        self.assertAlmostEqual(psi, expected, places=5)

    def test_model_info_includes_frequency(self):
        """Test that model info includes the fundamental frequency"""
        info = self.core.get_model_info()
        
        self.assertEqual(info['f0'], 141.7001)
        # The frequency should be part of the MODEL_ID
        self.assertIn('141.7001Hz', info['model_id'])


class TestNoesisQCALLLMCore(unittest.TestCase):
    """Test suite for noesis-qcal-llm version"""

    def setUp(self):
        """Initialize noesis core for tests"""
        # Import the noesis version
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'noesis-qcal-llm'))
        try:
            from QCALLLMCore import QCALLLMCore as NoesisCore
            self.core = NoesisCore(user_A_eff=0.85)
            self.has_noesis = True
        except ImportError:
            self.has_noesis = False
            self.skipTest("Noesis QCAL-LLM not available")

    def test_noesis_model_constants(self):
        """Test that noesis version has same model constants"""
        if not self.has_noesis:
            return
        
        from QCALLLMCore import QCALLLMCore as NoesisCore
        
        self.assertEqual(NoesisCore.MODEL_ID, "qcal::llama4-maverick-400B@141.7001Hz")
        self.assertEqual(NoesisCore.SYMBOLIC_VERSION, "LLAMA-QCAL-400B-141hz ∞³")

    def test_noesis_has_methods(self):
        """Test that noesis version has new methods"""
        if not self.has_noesis:
            return
        
        self.assertTrue(hasattr(self.core, 'get_model_info'))
        self.assertTrue(hasattr(self.core, 'compute_chi_llama'))
        self.assertTrue(hasattr(self.core, 'compute_psi_full'))


if __name__ == '__main__':
    unittest.main()
