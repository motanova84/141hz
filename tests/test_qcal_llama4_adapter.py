#!/usr/bin/env python3
"""
test_qcal_llama4_adapter.py - Tests for QCAL Llama 4 Adapter

Tests the QCAL_Llama4 adapter class structure and interface.
Note: Actual model loading tests require the model to be present.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class TestQCALLlama4Adapter:
    """Test suite for QCAL_Llama4 adapter."""
    
    def test_import_module(self):
        """Test that the adapter module can be imported."""
        try:
            import qcal_llama4_adapter
            assert hasattr(qcal_llama4_adapter, 'QCAL_Llama4')
        except ImportError as e:
            print(f"Warning: Could not import module: {e}")
            return False
        return True
    
    def test_class_exists(self):
        """Test that QCAL_Llama4 class is defined."""
        try:
            from qcal_llama4_adapter import QCAL_Llama4
            assert QCAL_Llama4 is not None
        except ImportError as e:
            print(f"Warning: Could not import class: {e}")
            return False
        return True
    
    def test_class_structure(self):
        """Test that QCAL_Llama4 has required methods."""
        try:
            from qcal_llama4_adapter import QCAL_Llama4
            
            # Check that class has required methods
            assert hasattr(QCAL_Llama4, '__init__')
            assert hasattr(QCAL_Llama4, 'evaluate')
            
            # Check that methods are callable
            assert callable(getattr(QCAL_Llama4, '__init__'))
            assert callable(getattr(QCAL_Llama4, 'evaluate'))
            
        except ImportError as e:
            print(f"Warning: Could not test structure: {e}")
            return False
        return True
    
    def test_initialization_parameters(self):
        """Test that initialization accepts correct parameters."""
        try:
            from qcal_llama4_adapter import QCAL_Llama4
        except ImportError:
            print("Warning: Could not import for parameter test")
            return False
        
        # Mock AutoTokenizer and AutoModelForCausalLM
        with patch('qcal_llama4_adapter.AutoTokenizer') as mock_tokenizer, \
             patch('qcal_llama4_adapter.AutoModelForCausalLM') as mock_model:
            
            # Setup mocks
            mock_tokenizer.from_pretrained.return_value = MagicMock()
            mock_model.from_pretrained.return_value = MagicMock()
            
            # Test with default parameters
            adapter = QCAL_Llama4()
            assert adapter.model_path == "./models/llama4"
            assert adapter.max_tokens == 300
            
            # Test with custom parameters
            adapter = QCAL_Llama4(model_path="./custom/path", max_tokens=500)
            assert adapter.model_path == "./custom/path"
            assert adapter.max_tokens == 500
        
        return True
    
    def test_evaluate_method_signature(self):
        """Test that evaluate method has correct signature."""
        try:
            from qcal_llama4_adapter import QCAL_Llama4
        except ImportError:
            print("Warning: Could not import for signature test")
            return False
        
        with patch('qcal_llama4_adapter.AutoTokenizer') as mock_tokenizer, \
             patch('qcal_llama4_adapter.AutoModelForCausalLM') as mock_model:
            
            # Setup mocks
            mock_tokenizer_instance = MagicMock()
            mock_model_instance = MagicMock()
            mock_model_instance.device = 'cpu'
            mock_model_instance.generate.return_value = [[1, 2, 3]]
            
            mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
            mock_model.from_pretrained.return_value = mock_model_instance
            
            mock_tokenizer_instance.return_value = MagicMock(to=lambda x: MagicMock())
            mock_tokenizer_instance.decode.return_value = "Test response"
            
            # Create adapter and test evaluate
            adapter = QCAL_Llama4()
            result = adapter.evaluate("Test prompt")
            
            # Check that result is a string
            assert isinstance(result, str)
            assert result == "Test response"
        
        return True
    
    def test_model_loading_parameters(self):
        """Test that model is loaded with correct parameters."""
        try:
            from qcal_llama4_adapter import QCAL_Llama4
        except ImportError:
            print("Warning: Could not import for loading test")
            return False
        
        with patch('qcal_llama4_adapter.AutoTokenizer') as mock_tokenizer, \
             patch('qcal_llama4_adapter.AutoModelForCausalLM') as mock_model, \
             patch('qcal_llama4_adapter.torch') as mock_torch:
            
            mock_torch.float16 = 'float16'
            mock_tokenizer.from_pretrained.return_value = MagicMock()
            mock_model.from_pretrained.return_value = MagicMock()
            
            # Create adapter
            adapter = QCAL_Llama4(model_path="./test/path")
            
            # Check that model was loaded with correct parameters
            mock_model.from_pretrained.assert_called_once()
            call_args = mock_model.from_pretrained.call_args
            
            assert call_args[0][0] == "./test/path"
            assert 'torch_dtype' in call_args[1]
            assert call_args[1]['torch_dtype'] == 'float16'
            assert 'device_map' in call_args[1]
            assert call_args[1]['device_map'] == "auto"
        
        return True


def run_tests():
    """Run all tests and report results."""
    print("="*70)
    print("QCAL Llama 4 Adapter Tests")
    print("="*70)
    print()
    
    test_suite = TestQCALLlama4Adapter()
    tests = [
        ("Import module", test_suite.test_import_module),
        ("Class exists", test_suite.test_class_exists),
        ("Class structure", test_suite.test_class_structure),
        ("Initialization parameters", test_suite.test_initialization_parameters),
        ("Evaluate method signature", test_suite.test_evaluate_method_signature),
        ("Model loading parameters", test_suite.test_model_loading_parameters),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✓ {test_name}")
                passed += 1
            else:
                print(f"✗ {test_name}")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print()
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
