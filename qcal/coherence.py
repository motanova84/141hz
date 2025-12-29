"""
Coherence metrics for QCAL-LLM evaluation.
Implements Ψ = I × A_eff² where:
- I: Information content (intention, purpose)
- A_eff: Attentional effectiveness
"""

import re
from typing import Dict, List, Optional
from collections import Counter

# Fundamental constants
F0 = 141.7001  # Hz
PHI = 1.618033988749895


def compute_intention(text: str) -> float:
    """
    Calculate intention metric I from text.
    
    Proxies for intention:
    - Keywords related to purpose: "intención", "propósito", "objetivo"
    - Keywords related to causality: "porque", "debido", "causa", "razón"
    - Logical connectors: "∴", "therefore", "por tanto"
    
    Args:
        text: Input text to analyze
        
    Returns:
        Intention score (higher = more intentional)
    """
    text_lower = text.lower()
    
    # Intention keywords (weighted)
    intention_keywords = {
        'intención': 3.0,
        'intencion': 3.0,
        'propósito': 3.0,
        'proposito': 3.0,
        'objetivo': 2.5,
        'meta': 2.0,
        'finalidad': 2.5,
    }
    
    # Causal keywords
    causal_keywords = {
        'porque': 1.5,
        'debido': 1.5,
        'causa': 2.0,
        'razón': 1.5,
        'razon': 1.5,
        'por tanto': 2.0,
        'therefore': 2.0,
        '∴': 3.0,
        'así que': 1.5,
        'por eso': 1.5,
    }
    
    # Calculate weighted score
    score = 0.0
    
    # Count intention keywords
    for keyword, weight in intention_keywords.items():
        score += text_lower.count(keyword) * weight
    
    # Count causal keywords
    for keyword, weight in causal_keywords.items():
        score += text_lower.count(keyword) * weight
    
    # Bonus for question marks (implies purposeful inquiry)
    score += text.count('?') * 0.5
    
    # Normalize by text length (but don't penalize too much)
    words = len(text.split())
    if words > 0:
        score = score * (1 + (words / 100) ** 0.5)
    
    return max(score, 0.1)  # Minimum baseline


def compute_effectiveness(text: str) -> float:
    """
    Calculate attentional effectiveness A_eff from text.
    
    A_eff = unique_words / total_words
    
    This measures lexical diversity, which correlates with:
    - Reduced repetition
    - Higher semantic density
    - More effective information transmission
    
    Args:
        text: Input text to analyze
        
    Returns:
        Effectiveness score between 0 and 1
    """
    words = text.split()
    if len(words) == 0:
        return 0.0
    
    unique_words = len(set(words))
    total_words = len(words)
    
    # Basic lexical diversity
    a_eff = unique_words / (total_words + 1e-6)
    
    # Bonus for longer texts (they maintain diversity)
    if total_words > 50:
        a_eff *= 1.1
    
    # Penalty for very short texts
    if total_words < 10:
        a_eff *= 0.8
    
    return min(a_eff, 1.0)  # Cap at 1.0


def psi_score(text: str, version: str = "standard") -> float:
    """
    Calculate Ψ coherence score.
    
    Standard formula: Ψ = I × A_eff²
    
    Args:
        text: Input text to analyze
        version: "standard" or "enhanced" (default: "standard")
        
    Returns:
        Ψ coherence score (typically 0-20 range, higher is better)
    """
    I = compute_intention(text)
    A_eff = compute_effectiveness(text)
    
    if version == "enhanced":
        # Enhanced version with F0 modulation
        # Ψ_enhanced = I × A_eff² × (1 + ∴_rate × PHI)
        strich = strich_rate(text)
        psi = I * (A_eff ** 2) * (1 + strich * PHI)
    else:
        # Standard version
        psi = I * (A_eff ** 2)
    
    return psi


def strich_rate(text: str) -> float:
    """
    Calculate ∴-rate (strich rate) - frequency of logical connectors.
    
    Args:
        text: Input text to analyze
        
    Returns:
        ∴-rate (logical connectors per 100 words)
    """
    # Logical connectors to count
    connectors = ['∴', 'therefore', 'por tanto', 'thus', 'hence', 'consequently']
    
    count = 0
    text_lower = text.lower()
    
    for connector in connectors:
        count += text_lower.count(connector)
    
    # Normalize per 100 words
    words = len(text.split())
    if words == 0:
        return 0.0
    
    return (count / words) * 100


def analyze_text(text: str) -> Dict[str, float]:
    """
    Comprehensive text analysis with all coherence metrics.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with all metrics
    """
    return {
        'psi_standard': psi_score(text, version="standard"),
        'psi_enhanced': psi_score(text, version="enhanced"),
        'intention': compute_intention(text),
        'effectiveness': compute_effectiveness(text),
        'strich_rate': strich_rate(text),
        'word_count': len(text.split()),
        'char_count': len(text),
    }


def evaluate_coherence(text: str, threshold: float = 5.0) -> Dict[str, any]:
    """
    Evaluate if text meets coherence threshold for QCAL validation.
    
    Args:
        text: Input text to analyze
        threshold: Minimum Ψ score required (default: 5.0)
        
    Returns:
        Dictionary with evaluation results
    """
    metrics = analyze_text(text)
    psi = metrics['psi_standard']
    
    passes = psi >= threshold
    
    return {
        **metrics,
        'passes_threshold': passes,
        'threshold': threshold,
        'status': '✓ COHERENTE' if passes else '✗ NO COHERENTE',
        'recommendation': (
            'Alta coherencia vibracional' if psi >= 8.0 else
            'Coherencia suficiente' if psi >= 5.0 else
            'Coherencia insuficiente - mejorar I o A_eff'
        )
    }
