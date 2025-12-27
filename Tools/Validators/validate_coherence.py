#!/usr/bin/env python3
"""
Validate Coherence Implementation

Validates the QC-LLM coherence validator implementation
"""

import sys
from pathlib import Path

# Add API to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "API" / "Python"))

from qc_llm import QC_LLM, F0

def test_basic_validation():
    """Test basic coherence validation"""
    validator = QC_LLM()
    
    # Test with simple text
    result = validator.validate("Test quantum coherence validation")
    
    assert "coherence" in result
    assert "frequency_alignment" in result
    assert "quantum_entropy" in result
    assert "recommendation" in result
    
    assert 0 <= result["coherence"] <= 1
    assert 0 <= result["frequency_alignment"] <= 1
    assert 0 <= result["quantum_entropy"] <= 1
    
    print("✅ Basic validation test passed")

def test_frequency():
    """Test frequency constant"""
    assert F0 == 141.7001
    assert QC_LLM.get_frequency() == 141.7001
    print("✅ Frequency constant test passed")

def test_batch_validation():
    """Test batch validation"""
    validator = QC_LLM()
    
    texts = [
        "First text to validate",
        "Second text to validate",
        "Third text to validate"
    ]
    
    results = validator.batch_validate(texts)
    
    assert len(results) == len(texts)
    for result in results:
        assert "coherence" in result
    
    print("✅ Batch validation test passed")

def test_empty_text():
    """Test empty text handling"""
    validator = QC_LLM()
    
    try:
        validator.validate("")
        assert False, "Should raise error for empty text"
    except ValueError:
        print("✅ Empty text handling test passed")

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("QC-LLM Coherence Validation Tests")
    print("=" * 60)
    print(f"Fundamental Frequency: f₀ = {F0} Hz\n")
    
    tests = [
        test_frequency,
        test_basic_validation,
        test_batch_validation,
        test_empty_text
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
