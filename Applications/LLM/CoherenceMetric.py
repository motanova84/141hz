"""
Coherence Metric for Language Models

Implements quantum coherence measurement for LLM outputs
based on alignment with f₀ = 141.7001 Hz
"""

import numpy as np
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add API to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "API" / "Python"))

from qc_llm import QC_LLM, F0

class CoherenceMetric:
    """
    Quantum Coherence Metric for LLM Evaluation
    
    Usage:
        >>> metric = CoherenceMetric()
        >>> score = metric.measure("LLM output text here")
        >>> print(f"Coherence: {score:.2%}")
    """
    
    def __init__(self, frequency: float = F0):
        """
        Initialize metric
        
        Args:
            frequency: Target frequency (default: f₀ = 141.7001 Hz)
        """
        self.frequency = frequency
        self.validator = QC_LLM()
    
    def measure(self, text: str) -> float:
        """
        Measure coherence of text
        
        Args:
            text: Input text to measure
            
        Returns:
            Coherence score [0, 1]
        """
        result = self.validator.validate(text)
        return result["coherence"]
    
    def detailed_analysis(self, text: str) -> Dict:
        """
        Perform detailed coherence analysis
        
        Returns:
            Dictionary with all metrics
        """
        return self.validator.validate(text)
    
    def batch_measure(self, texts: List[str]) -> List[float]:
        """
        Measure coherence for multiple texts
        
        Args:
            texts: List of texts
            
        Returns:
            List of coherence scores
        """
        return [self.measure(t) for t in texts]
    
    def compare_outputs(self, outputs: Dict[str, str]) -> Dict[str, float]:
        """
        Compare coherence across multiple model outputs
        
        Args:
            outputs: Dictionary mapping model names to their outputs
            
        Returns:
            Dictionary mapping model names to coherence scores
        """
        return {
            model: self.measure(output)
            for model, output in outputs.items()
        }
    
    def rank_outputs(self, outputs: Dict[str, str]) -> List[tuple]:
        """
        Rank model outputs by coherence
        
        Returns:
            List of (model_name, score) tuples, sorted descending
        """
        scores = self.compare_outputs(outputs)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
