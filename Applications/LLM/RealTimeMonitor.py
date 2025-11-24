"""
Real-Time Coherence Monitor

Monitors quantum coherence in streaming text outputs
"""

import numpy as np
from typing import List, Optional, Dict
from collections import deque
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "API" / "Python"))
from qc_llm import QC_LLM, F0

class RealTimeMonitor:
    """
    Real-time quantum coherence monitor for streaming text
    
    Usage:
        >>> monitor = RealTimeMonitor(window_size=100)
        >>> for chunk in text_stream:
        ...     score = monitor.update(chunk)
        ...     print(f"Current coherence: {score:.2%}")
    """
    
    def __init__(self, window_size: int = 100, frequency: float = F0):
        """
        Initialize monitor
        
        Args:
            window_size: Number of recent chunks to track
            frequency: Target coherence frequency
        """
        self.window_size = window_size
        self.frequency = frequency
        self.validator = QC_LLM()
        
        # Rolling window of recent chunks
        self.text_buffer = deque(maxlen=window_size)
        self.coherence_history = deque(maxlen=window_size)
    
    def update(self, text_chunk: str) -> float:
        """
        Update monitor with new text chunk
        
        Args:
            text_chunk: New text to analyze
            
        Returns:
            Current coherence score
        """
        self.text_buffer.append(text_chunk)
        
        # Analyze combined recent text
        combined_text = " ".join(self.text_buffer)
        result = self.validator.validate(combined_text)
        
        coherence = result["coherence"]
        self.coherence_history.append(coherence)
        
        return coherence
    
    def get_statistics(self) -> Dict:
        """
        Get coherence statistics over history
        
        Returns:
            Dictionary with statistics
        """
        if not self.coherence_history:
            return {
                "mean": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "trend": "stable"
            }
        
        history = np.array(list(self.coherence_history))
        
        # Compute trend (simple: last vs first)
        if len(history) > 1:
            if history[-1] > history[0] + 0.05:
                trend = "improving"
            elif history[-1] < history[0] - 0.05:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return {
            "mean": float(np.mean(history)),
            "std": float(np.std(history)),
            "min": float(np.min(history)),
            "max": float(np.max(history)),
            "trend": trend,
            "samples": len(history)
        }
    
    def reset(self):
        """Reset monitor state"""
        self.text_buffer.clear()
        self.coherence_history.clear()
    
    def is_coherent(self, threshold: float = 0.80) -> bool:
        """
        Check if current coherence exceeds threshold
        
        Args:
            threshold: Minimum coherence threshold
            
        Returns:
            True if coherent, False otherwise
        """
        if not self.coherence_history:
            return False
        return self.coherence_history[-1] >= threshold
    
    def get_alert_status(self, low_threshold: float = 0.60) -> str:
        """
        Get alert status based on coherence
        
        Returns:
            Alert level: "good", "warning", or "critical"
        """
        if not self.coherence_history:
            return "unknown"
        
        current = self.coherence_history[-1]
        
        if current >= 0.80:
            return "good"
        elif current >= low_threshold:
            return "warning"
        else:
            return "critical"
