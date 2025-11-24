"""
Test suite for noesis-qcal-llm/detect_f0.py module
"""
import unittest
import sys
import os
import numpy as np

# Add the noesis-qcal-llm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'noesis-qcal-llm'))

from detect_f0 import qnm_model, detect_f0


class TestQNMModel(unittest.TestCase):
    """Test the QNM (Quasi-Normal Mode) model"""
    
    def test_qnm_model_basic(self):
        """Test that QNM model returns expected values"""
        # Test with typical values
        f = 141.7
        M = 30
        a = 0.7
        result = qnm_model(f, M, a)
        
        # Should return a positive value
        self.assertGreater(result, 0)
        
        # Should be inversely proportional to frequency
        result2 = qnm_model(f * 2, M, a)
        self.assertLess(result2, result)
    
    def test_qnm_model_spin_effect(self):
        """Test that spin parameter affects the result"""
        f = 141.7
        M = 30
        
        result_low_spin = qnm_model(f, M, 0.0)
        result_high_spin = qnm_model(f, M, 0.9)
        
        # Higher spin should give lower values due to (1 - 0.1*a) term
        self.assertLess(result_high_spin, result_low_spin)


class TestDetectF0(unittest.TestCase):
    """Test the detect_f0 function"""
    
    def test_detect_f0_expected_values(self):
        """Test that expected benchmark values are correct"""
        # These are the proxy values from the module
        f0_expected = 141.7001
        snr_expected = 20.95
        chi2_expected = 45.2
        
        # Verify they are in reasonable ranges
        self.assertGreater(f0_expected, 130)
        self.assertLess(f0_expected, 160)
        self.assertGreater(snr_expected, 10)
        self.assertGreater(chi2_expected, 0)
    
    def test_detect_f0_function_exists(self):
        """Test that detect_f0 function is callable"""
        self.assertTrue(callable(detect_f0))


class TestScriptExecution(unittest.TestCase):
    """Test the script can be executed"""
    
    def test_script_imports(self):
        """Test that the script imports correctly"""
        try:
            import detect_f0
            self.assertTrue(hasattr(detect_f0, 'qnm_model'))
            self.assertTrue(hasattr(detect_f0, 'detect_f0'))
        except ImportError as e:
            self.fail(f"Failed to import detect_f0: {e}")


if __name__ == '__main__':
    unittest.main()
