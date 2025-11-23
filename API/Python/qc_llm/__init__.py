"""
QC-LLM: Quantum Coherence Library for Language Models
Author: José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)

Public API for quantum coherence validation in LLM outputs.
"""

__version__ = "1.0.0"
__author__ = "José Manuel Mota Burruezo"
__email__ = "motanova84@gmail.com"

from .validator import CoherenceValidator
from .metrics import (
    compute_frequency_alignment,
    compute_quantum_entropy,
    compute_coherence_score,
    compute_coherence,  # New main function from problem statement
    F0
)
from .core import QCALLLMCore

__all__ = [
    "CoherenceValidator",
    "compute_frequency_alignment",
    "compute_quantum_entropy",
    "compute_coherence_score",
    "compute_coherence",  # New main function
    "F0",
    "QC_LLM",
    "QCALLLMCore"
]

class QC_LLM:
    """
    Main class for Quantum Coherence validation
    
    Example:
        >>> from qc_llm import QC_LLM
        >>> validator = QC_LLM()
        >>> result = validator.validate("Your text here")
        >>> print(f"Coherence: {result['coherence']:.2%}")
    """
    
    def __init__(self, model_name: str = "default"):
        self.model = model_name
        self.validator = CoherenceValidator()
    
    def validate(self, text: str) -> dict:
        """Validate quantum coherence of text"""
        return self.validator.analyze(text)
    
    def batch_validate(self, texts: list) -> list:
        """Validate multiple texts"""
        return [self.validate(t) for t in texts]
    
    @staticmethod
    def get_frequency() -> float:
        """Get fundamental frequency"""
        return F0
