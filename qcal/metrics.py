"""
Additional metrics for LLM evaluation.
Includes KLD, SNR, repetition rate, and semantic density.
"""

import numpy as np
from typing import Dict, List, Optional
from collections import Counter
import re


def kl_divergence(text: str, reference_distribution: Optional[Dict[str, float]] = None) -> float:
    """
    Calculate Kullback-Leibler divergence for text distribution.
    
    Lower KLD suggests text is closer to reference distribution (e.g., natural language).
    We use inverse KLD (1/KLD) as a quality metric where higher is better.
    
    Args:
        text: Input text to analyze
        reference_distribution: Optional reference distribution (uniform by default)
        
    Returns:
        KL divergence score (lower = closer to reference)
    """
    words = text.lower().split()
    if len(words) == 0:
        return float('inf')
    
    # Calculate empirical distribution
    word_counts = Counter(words)
    total_words = len(words)
    
    # Text distribution P
    p_dist = {word: count / total_words for word, count in word_counts.items()}
    
    # Reference distribution Q (uniform by default)
    if reference_distribution is None:
        # Uniform distribution over vocabulary
        vocab_size = len(word_counts)
        q_dist = {word: 1.0 / vocab_size for word in word_counts.keys()}
    else:
        q_dist = reference_distribution
    
    # Calculate KL divergence: KL(P||Q) = Σ P(x) log(P(x)/Q(x))
    kld = 0.0
    for word in p_dist:
        p_x = p_dist[word]
        q_x = q_dist.get(word, 1e-10)  # Small epsilon for unseen words
        kld += p_x * np.log(p_x / q_x)
    
    return kld


def snr(text: str) -> float:
    """
    Calculate semantic signal-to-noise ratio.
    
    Signal: Content words (nouns, verbs, adjectives)
    Noise: Function words (articles, prepositions, conjunctions)
    
    Args:
        text: Input text to analyze
        
    Returns:
        SNR score (higher = better signal quality)
    """
    # Common function words (noise)
    noise_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can',
        # Spanish function words
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o',
        'pero', 'en', 'de', 'del', 'al', 'por', 'para', 'con', 'sin',
        'es', 'son', 'está', 'están', 'ser', 'estar', 'haber', 'tener',
    }
    
    words = text.lower().split()
    if len(words) == 0:
        return 0.0
    
    # Count signal vs noise
    signal_count = sum(1 for word in words if word not in noise_words and len(word) > 2)
    noise_count = sum(1 for word in words if word in noise_words or len(word) <= 2)
    
    # Calculate SNR (add small epsilon to avoid division by zero)
    snr_value = signal_count / (noise_count + 1e-6)
    
    # Convert to dB scale
    snr_db = 10 * np.log10(snr_value + 1e-6)
    
    return snr_db


def repetition_rate(text: str) -> float:
    """
    Calculate repetition rate (inverse of lexical diversity).
    
    Lower is better (less repetition).
    
    Args:
        text: Input text to analyze
        
    Returns:
        Repetition rate (0 = no repetition, 1 = complete repetition)
    """
    words = text.lower().split()
    if len(words) == 0:
        return 0.0
    
    unique_words = len(set(words))
    total_words = len(words)
    
    # Repetition is inverse of diversity
    repetition = 1.0 - (unique_words / total_words)
    
    return repetition


def semantic_density(text: str) -> float:
    """
    Calculate semantic density of text.
    
    Measures information content per word.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Semantic density score (higher = more information per word)
    """
    words = text.split()
    if len(words) == 0:
        return 0.0
    
    # Count meaningful tokens
    # - Words longer than 3 characters
    # - Technical terms (contain numbers or special characters)
    # - Capitalized words (proper nouns, acronyms)
    
    meaningful_count = 0
    for word in words:
        if len(word) > 3:
            meaningful_count += 1
        if re.search(r'\d', word):
            meaningful_count += 1
        if word[0].isupper() and len(word) > 1:
            meaningful_count += 0.5
    
    density = meaningful_count / len(words)
    
    return density


def entropy(text: str) -> float:
    """
    Calculate Shannon entropy of text.
    
    Higher entropy = more information content.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Shannon entropy in bits
    """
    words = text.lower().split()
    if len(words) == 0:
        return 0.0
    
    # Calculate word frequency distribution
    word_counts = Counter(words)
    total_words = len(words)
    
    # Calculate entropy: H = -Σ p(x) log₂(p(x))
    h = 0.0
    for count in word_counts.values():
        p = count / total_words
        h -= p * np.log2(p)
    
    return h


def comprehensive_metrics(text: str) -> Dict[str, float]:
    """
    Calculate all metrics for comprehensive evaluation.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with all metric scores
    """
    kld_value = kl_divergence(text)
    
    return {
        'kld': kld_value,
        'kld_inv': 1.0 / (kld_value + 1e-6) if kld_value < float('inf') else 0.0,
        'snr_db': snr(text),
        'repetition': repetition_rate(text),
        'semantic_density': semantic_density(text),
        'entropy': entropy(text),
        'word_count': len(text.split()),
    }


def quality_score(text: str, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculate overall quality score from multiple metrics.
    
    Args:
        text: Input text to analyze
        weights: Optional weights for each metric
        
    Returns:
        Normalized quality score (0-100)
    """
    if weights is None:
        weights = {
            'kld_inv': 0.2,
            'snr_db': 0.3,
            'semantic_density': 0.3,
            'entropy': 0.2,
        }
    
    metrics = comprehensive_metrics(text)
    
    # Normalize each metric to 0-1 range
    normalized = {}
    
    # KLD inverse (already roughly 0-1 range for good text)
    normalized['kld_inv'] = min(metrics['kld_inv'], 1.0)
    
    # SNR in dB (typically -10 to +20 dB)
    normalized['snr_db'] = (metrics['snr_db'] + 10) / 30
    normalized['snr_db'] = max(0, min(normalized['snr_db'], 1.0))
    
    # Semantic density (already 0-1 range)
    normalized['semantic_density'] = metrics['semantic_density']
    
    # Entropy (typically 0-10 bits)
    normalized['entropy'] = min(metrics['entropy'] / 10, 1.0)
    
    # Calculate weighted sum
    score = sum(normalized[key] * weights[key] for key in weights)
    
    # Scale to 0-100
    return score * 100
