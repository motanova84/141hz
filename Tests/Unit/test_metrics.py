"""
Unit tests for metrics module
"""

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / 'API' / 'Python'))

from qc_llm.metrics import (
    compute_frequency_alignment,
    compute_quantum_entropy,
    compute_coherence_score,
    F0
)

def test_f0_value():
    """Test fundamental frequency constant"""
    assert F0 == 141.7001
    assert isinstance(F0, float)

def test_frequency_alignment():
    """Test frequency alignment computation"""
    text = "This is a test text for coherence validation."
    score = compute_frequency_alignment(text)
    
    assert 0 <= score <= 1
    assert isinstance(score, float)

def test_quantum_entropy():
    """Test quantum entropy computation"""
    text = "Quantum coherence in language models represents fundamental principles."
    entropy = compute_quantum_entropy(text)
    
    assert 0 <= entropy <= 1
    assert isinstance(entropy, float)

def test_coherence_score():
    """Test complete coherence score"""
    text = "The fundamental frequency f₀ = 141.7001 Hz emerges from mathematical principles."
    result = compute_coherence_score(text)
    
    assert "coherence" in result
    assert "frequency_alignment" in result
    assert "quantum_entropy" in result
    assert "recommendation" in result
    
    assert 0 <= result["coherence"] <= 1

def test_empty_text():
    """Test handling of empty text"""
    entropy = compute_quantum_entropy("")
    assert entropy == 0.0

def test_single_word():
    """Test single word input"""
    score = compute_coherence_score("test")
    assert isinstance(score, dict)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
