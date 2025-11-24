"""
Core metrics for quantum coherence computation
"""

import numpy as np
from typing import Dict, List, Optional
import warnings

# Fundamental constant
F0 = 141.7001  # Hz
from typing import Dict, List
from .constants import (
    F0, DEFAULT_QUANTUM_ENTROPY, EPSILON_ZERO_PROTECTION,
    THRESHOLD_HIGH, THRESHOLD_MODERATE, THRESHOLD_LOW,
    WEIGHT_FREQUENCY_ALIGNMENT, WEIGHT_QUANTUM_ENTROPY
)

# Normalization constants for frequency alignment
# These map abstract mathematical frequencies to observable physical scales
FREQ_NORMALIZATION_FACTOR = 1000.0  # Maps f₀ (Hz) to embedding domain (normalized units)
# Explanation: BERT embeddings have dimensionless indices. To relate the physical
# frequency f₀ = 141.7001 Hz to embedding space, we scale by 1000 to get
# a normalized target frequency ~0.142, which is in the typical range of
# FFT frequencies for text sequences of 10-100 tokens.

ALIGNMENT_SENSITIVITY = 10.0  # Exponential decay rate for frequency mismatch
# Explanation: This controls how sharply alignment score decreases with
# frequency distance. Value of 10 means that a mismatch of 0.1 normalized
# units gives exp(-1) ≈ 0.37 alignment. Chosen empirically to balance
# sensitivity to f₀ while tolerating small deviations.

# Try to import transformers, but make it optional for basic functionality
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    warnings.warn(
        "Transformers not available. Install with: pip install transformers torch>=2.6.0\n"
        "Falling back to basic coherence computation.",
        ImportWarning
    )

def compute_frequency_alignment(text: str, target_freq: float = F0, use_bert: bool = True) -> float:
    """
    Compute alignment with target frequency using BERT embeddings and FFT
    
    Args:
        text: Input text to analyze
        target_freq: Target frequency (default: f₀ = 141.7001 Hz)
        use_bert: Whether to use BERT embeddings (requires transformers)
    
    Returns:
        Alignment score [0, 1]
    """
    if not text or not text.strip():
        return 0.0
    
    # Use BERT-based analysis if available and requested
    if use_bert and TRANSFORMERS_AVAILABLE:
        return _compute_bert_frequency_alignment(text, target_freq)
    else:
        # Fallback to basic token-based analysis
        return _compute_basic_frequency_alignment(text, target_freq)

def _compute_bert_frequency_alignment(text: str, target_freq: float) -> float:
    """
    Compute frequency alignment using BERT embeddings and FFT (as per problem statement)
    
    Implementation based on problem statement specification:
    - Use BERT embeddings
    - Apply FFT for spectral analysis
    - Find peak closest to f₀ = 141.7001 Hz
    """
    try:
        # Initialize BERT model (using smaller model for efficiency)
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        model = AutoModel.from_pretrained("bert-base-uncased")
        
        # Tokenize and embed text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = model(**inputs)
            # Get mean of last hidden state
            embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        
        # Spectral analysis using FFT
        n = len(embeddings[0])
        if n < 2:
            return 0.0
            
        freqs = np.fft.fftfreq(n, d=1.0)
        fft_vals = np.fft.fft(embeddings[0])
        
        # Normalize target frequency to embedding domain
        # f₀ = 141.7001 Hz maps to normalized frequency
        normalized_f0 = target_freq / FREQ_NORMALIZATION_FACTOR
        
        # Find peak closest to f₀
        freq_distances = np.abs(freqs - normalized_f0)
        peak_idx = np.argmin(freq_distances)
        
        # Compute frequency alignment as exponential decay
        freq_alignment = np.exp(-freq_distances[peak_idx])
        
        return float(np.clip(freq_alignment, 0, 1))
        
    except Exception as e:
        warnings.warn(f"BERT analysis failed: {e}. Falling back to basic analysis.")
        return _compute_basic_frequency_alignment(text, target_freq)

def _compute_basic_frequency_alignment(text: str, target_freq: float) -> float:
    """
    Basic frequency alignment computation (fallback when BERT unavailable)
    """
    # Tokenize
    tokens = text.split()
    n = len(tokens)
    
    if n < 2:
        return 0.5  # Neutral score for very short text
    
    # Simple spectral analysis based on token positions
    frequencies = np.fft.fftfreq(n, d=1.0)
    
    # Normalize target frequency to text domain
    norm_target = target_freq / FREQ_NORMALIZATION_FACTOR
    
    # Compute alignment based on token distribution
    # This is a simplified version
    token_lengths = np.array([len(t) for t in tokens])
    token_spectrum = np.abs(np.fft.fft(token_lengths))
    
    # Find peak in valid range
    valid_range = max(1, n//2)
    if valid_range > 1:
        peak_idx = np.argmax(token_spectrum[1:valid_range]) + 1  # Skip DC component
        peak_freq = abs(frequencies[peak_idx])
    else:
        peak_freq = 0.1
    
    # Compute alignment using exponential decay
    alignment = np.exp(-abs(peak_freq - norm_target) * ALIGNMENT_SENSITIVITY)
    
    return float(np.clip(alignment, 0, 1))

def compute_quantum_entropy(text: str) -> float:
    """
    Compute quantum entropy of text
    
    Based on token diversity and distribution.
    
    Returns:
        Entropy score [0, 1]
    """
    tokens = text.split()
    if not tokens:
        return 0.0
    
    # Token frequency distribution
    unique_tokens = set(tokens)
    n_unique = len(unique_tokens)
    n_total = len(tokens)
    
    # Shannon entropy
    freq_dist = np.array([tokens.count(t) / n_total for t in unique_tokens])
    entropy = -np.sum(freq_dist * np.log2(freq_dist + EPSILON_ZERO_PROTECTION))
    
    # Normalize to [0, 1]
    max_entropy = np.log2(n_total)
    normalized = entropy / max_entropy if max_entropy > 0 else 0.0
    
    return float(normalized)

def compute_coherence(text: str, use_bert: bool = True) -> dict:
    """
    Compute complete coherence score using BERT embeddings and FFT
    
    This is the main function specified in the problem statement that uses:
    - BERT embeddings for semantic representation
    - FFT for spectral analysis
    - Alignment with f₀ = 141.7001 Hz
    
    Args:
        text: Input text to analyze
        use_bert: Whether to use BERT (requires transformers library)
    
    Returns:
        Dictionary with:
        - coherence: Overall coherence score [0, 1]
        - frequency_alignment: Alignment with f₀ [0, 1]
        - quantum_metric: Token diversity metric [0, 1]
        - recommendation: Quality recommendation string
    """
    if not text or not text.strip():
        return {
            "coherence": 0.0,
            "frequency_alignment": 0.0,
            "quantum_metric": 0.0,
            "recommendation": "INVALID - Empty text"
        }
    
    # Compute frequency alignment (uses BERT + FFT if available)
    freq_align = compute_frequency_alignment(text, F0, use_bert=use_bert)
    
    # Compute quantum metric (as specified in problem statement)
    # quantum_metric = 1.0 - (unique_words / total_words)
    # This measures repetition - higher value means more repetition
    tokens = text.split()
    n_total = len(tokens)
    n_unique = len(set(tokens))
    quantum_metric = 1.0 - (n_unique / n_total) if n_total > 0 else 0.0
    
    # Coherence is the primary metric (as per problem statement)
    # Using FFT peak amplitude normalized by sum
    if TRANSFORMERS_AVAILABLE and use_bert:
        try:
            tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            model = AutoModel.from_pretrained("bert-base-uncased")
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            
            fft_vals = np.fft.fft(embeddings[0])
            
            # Find peak closest to normalized f₀
            n = len(fft_vals)
            freqs = np.fft.fftfreq(n, d=1.0)
            normalized_f0 = F0 / 1000.0
            freq_distances = np.abs(freqs - normalized_f0)
            peak_idx = np.argmin(freq_distances)
            
            # Coherence = |FFT[peak]| / sum(|FFT|) as per problem statement
            coherence = np.abs(fft_vals[peak_idx]) / (np.sum(np.abs(fft_vals)) + 1e-10)
        except Exception as e:
            warnings.warn(f"BERT coherence failed: {e}. Using basic computation.")
            coherence = 0.5 * freq_align + 0.5 * (1.0 - quantum_metric)
    else:
        # Fallback: weighted combination
        coherence = 0.6 * freq_align + 0.4 * (1.0 - quantum_metric)
    
    coherence = float(np.clip(coherence, 0, 1))
    
    # Recommendation thresholds as per problem statement
    if coherence > 0.8:
        recommendation = "HIGH COHERENCE"
    elif coherence > 0.6:
        recommendation = "MODERATE COHERENCE"
    # Weighted average
    coherence = WEIGHT_FREQUENCY_ALIGNMENT * freq_align + WEIGHT_QUANTUM_ENTROPY * entropy
    
    # Recommendation
    if coherence > THRESHOLD_HIGH:
        recommendation = "HIGH COHERENCE - Excellent quality"
    elif coherence > THRESHOLD_MODERATE:
        recommendation = "MODERATE COHERENCE - Good quality"
    elif coherence > THRESHOLD_LOW:
        recommendation = "LOW COHERENCE - Consider rephrasing"
    else:
        recommendation = "LOW COHERENCE - Consider rephrasing"
    
    return {
        "coherence": float(coherence),
        "frequency_alignment": float(freq_align),
        "quantum_metric": float(quantum_metric),
        "recommendation": recommendation
    }

def compute_coherence_score(text: str) -> Dict[str, float]:
    """
    Compute complete coherence score (legacy wrapper)
    
    This maintains backward compatibility while using the new compute_coherence implementation.
    
    Returns:
        Dictionary with:
        - coherence: Overall coherence score
        - frequency_alignment: Alignment with f₀
        - quantum_entropy: Quantum entropy (for compatibility)
        - recommendation: Text recommendation
    """
    result = compute_coherence(text, use_bert=TRANSFORMERS_AVAILABLE)
    
    # Add entropy for backward compatibility
    entropy = compute_quantum_entropy(text)
    result["quantum_entropy"] = entropy
    
    return result
