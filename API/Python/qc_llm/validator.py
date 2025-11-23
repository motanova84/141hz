"""
Main validator class
"""

from typing import Dict
from .metrics import compute_coherence_score, F0

class CoherenceValidator:
    """
    Quantum Coherence Validator
    
    Validates text against the fundamental frequency f₀ = 141.7001 Hz
    """
    
    def __init__(self, frequency: float = F0):
        self.frequency = frequency
        self.version = "1.0.0"
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze text for quantum coherence
        
        Args:
            text: Input text to validate
        
        Returns:
            Dictionary with coherence metrics
        """
        if not text or not text.strip():
            raise ValueError("Empty text provided")
        
        # Compute metrics
        result = compute_coherence_score(text)
        
        # Add metadata
        result["frequency"] = self.frequency
        result["version"] = self.version
        
        return result
    
    def __repr__(self):
        return f"CoherenceValidator(frequency={self.frequency} Hz)"
