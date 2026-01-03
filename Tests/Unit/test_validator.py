"""
Unit tests for validator
"""

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / 'API' / 'Python'))

from qc_llm import CoherenceValidator

def test_validator_initialization():
    """Test validator initialization"""
    validator = CoherenceValidator()
    assert validator.frequency == 141.7001
    assert validator.version == "1.0.0"

def test_analyze():
    """Test analyze method"""
    validator = CoherenceValidator()
    text = "This is test text."
    
    result = validator.analyze(text)
    
    assert "coherence" in result
    assert "frequency" in result
    assert "version" in result

def test_empty_text_raises():
    """Test that empty text raises ValueError"""
    validator = CoherenceValidator()
    
    with pytest.raises(ValueError):
        validator.analyze("")

def test_whitespace_only_raises():
    """Test that whitespace-only raises ValueError"""
    validator = CoherenceValidator()
    
    with pytest.raises(ValueError):
        validator.analyze("   \n  \t  ")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
