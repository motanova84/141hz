# Omega ∞³ Developer Guide

## Extending the Omega System

This guide explains how to extend Omega ∞³ with custom models, validators, and hypothesis generators.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Adding Custom Validators](#adding-custom-validators)
3. [Creating Hypothesis Models](#creating-hypothesis-models)
4. [Integrating External Data Sources](#integrating-external-data-sources)
5. [Writing Omega-Compatible Tests](#writing-omega-compatible-tests)
6. [Best Practices](#best-practices)

## Architecture Overview

Omega ∞³ is built on a modular architecture with six layers:

```
┌─────────────────────────────────────────────────────────────┐
│ Ω1 Auto-Ingestion    │  Event detection & data ingestion   │
├─────────────────────────────────────────────────────────────┤
│ Ω2 Auto-Analysis     │  GPU-accelerated validation         │
├─────────────────────────────────────────────────────────────┤
│ Ω3 Auto-Publication  │  NFT metadata & permanent storage   │
├─────────────────────────────────────────────────────────────┤
│ Ω4 Auto-Validation   │  Multi-detector replication         │
├─────────────────────────────────────────────────────────────┤
│ Ω5 Auto-Hypothesis   │  Prediction generation              │
├─────────────────────────────────────────────────────────────┤
│ Ω6 Auto-Defense      │  Data integrity & security          │
└─────────────────────────────────────────────────────────────┘
```

### Core Modules

- `omega_auto.py` - Ω2 validation engine
- `omega_hypothesis.py` - Ω5 prediction generator
- `demo_omega_integration.py` - Full pipeline demo

## Adding Custom Validators

### Step 1: Create Your Validator Function

```python
# custom_validator.py
from omega_auto import omega_psd, omega_snr, compute_ipfs_hash
import numpy as np

def validate_custom_frequency(strain: np.ndarray, fs: int, 
                              target_freq: float) -> dict:
    """
    Custom validator for any target frequency.
    
    Args:
        strain: Time series data
        fs: Sampling frequency
        target_freq: Target frequency to validate
        
    Returns:
        Validation results with SNR and metadata
    """
    # Compute PSD
    freqs, psd = omega_psd(strain, fs)
    
    # Calculate SNR around target
    snr = omega_snr(freqs, psd, f0=target_freq, df=0.5)
    
    # Create results
    results = {
        "target_frequency_hz": target_freq,
        "snr": snr,
        "detected": snr > 5.0,
        "method": "custom-validator"
    }
    
    # Add integrity hash (Ω6 Auto-Defense)
    results["ipfs_hash"] = compute_ipfs_hash(results)
    
    return results
```

### Step 2: Integrate with Omega Pipeline

```python
# integration_example.py
from omega_auto import omega_validate
from custom_validator import validate_custom_frequency

# Use existing Omega infrastructure
event_results = omega_validate("GW150914", use_real_data=False)

# Add custom validation
print(f"Custom validation: {validate_custom_frequency(...)}")
```

## Creating Hypothesis Models

### Step 1: Define Your Model Function

```python
# custom_hypothesis.py
from typing import List, Dict
from datetime import datetime

def generate_logarithmic_harmonics(f0: float, n_harmonics: int = 10) -> List[Dict]:
    """
    Generate logarithmic scale harmonics: f_n = f_0 / log(n+2)
    
    Args:
        f0: Base frequency
        n_harmonics: Number of predictions
        
    Returns:
        List of harmonic predictions
    """
    import numpy as np
    
    harmonics = []
    for n in range(n_harmonics):
        f_n = f0 / np.log(n + 2)
        harmonics.append({
            "n": n,
            "frequency_hz": round(f_n, 6),
            "formula": f"f_0 / log({n+2})",
            "hypothesis": f"Logarithmic harmonic mode n={n}",
            "predicted_by": "logarithmic-model",
            "timestamp": datetime.now().isoformat(),
            "testable": True
        })
    return harmonics
```

### Step 2: Integrate with Omega Hypothesis System

```python
# Add to omega_hypothesis.py or use separately
from omega_hypothesis import generate_hypothesis_catalog
from custom_hypothesis import generate_logarithmic_harmonics

# Generate standard catalog
catalog = generate_hypothesis_catalog(141.7001)

# Add your custom model
catalog["models"]["logarithmic"] = generate_logarithmic_harmonics(141.7001, 10)
```

## Integrating External Data Sources

### Example: EEG Data Integration

```python
# omega_eeg.py
import numpy as np
from omega_auto import omega_psd, omega_snr

def analyze_eeg_for_resonance(eeg_data: np.ndarray, 
                               sampling_rate: int,
                               target_freq: float = 141.7001) -> dict:
    """
    Analyze EEG data for resonance at target frequency.
    
    Args:
        eeg_data: EEG time series (channels × time)
        sampling_rate: EEG sampling rate (Hz)
        target_freq: Target frequency to detect
        
    Returns:
        Analysis results per channel
    """
    results = {
        "target_frequency_hz": target_freq,
        "sampling_rate_hz": sampling_rate,
        "channels": []
    }
    
    for ch_idx, channel_data in enumerate(eeg_data):
        # Compute PSD for this channel
        freqs, psd = omega_psd(channel_data, sampling_rate)
        
        # Calculate SNR
        snr = omega_snr(freqs, psd, target_freq, df=0.5)
        
        results["channels"].append({
            "channel": ch_idx,
            "snr": round(snr, 2),
            "detected": snr > 3.0  # Lower threshold for EEG
        })
    
    return results
```

### Example: CMB Data Integration

```python
# omega_cmb.py
from omega_auto import omega_snr
import numpy as np

def analyze_cmb_power_spectrum(ell: np.ndarray, 
                                cl: np.ndarray,
                                target_mode: int = 142) -> dict:
    """
    Analyze CMB power spectrum for resonance.
    
    Args:
        ell: Multipole moments
        cl: Power spectrum C_ell
        target_mode: Target multipole mode
        
    Returns:
        CMB analysis results
    """
    # Find power near target mode
    mask = np.abs(ell - target_mode) < 5
    signal_power = np.mean(cl[mask])
    noise_power = np.median(cl)
    
    snr = signal_power / noise_power
    
    return {
        "target_mode": target_mode,
        "signal_power": float(signal_power),
        "noise_power": float(noise_power),
        "snr": float(snr),
        "detected": snr > 1.5
    }
```

## Writing Omega-Compatible Tests

### Test Template

```python
# test_custom_module.py
import unittest
import numpy as np
from custom_module import custom_function

class TestCustomModule(unittest.TestCase):
    """Tests for custom Omega extension."""
    
    def test_basic_functionality(self):
        """Test basic operation."""
        result = custom_function(test_data)
        self.assertIsNotNone(result)
        self.assertIn("ipfs_hash", result)
    
    def test_data_integrity(self):
        """Test Ω6 data integrity."""
        result1 = custom_function(test_data)
        result2 = custom_function(test_data)
        # Same input = same hash
        self.assertEqual(result1["ipfs_hash"], result2["ipfs_hash"])
    
    def test_nft_metadata(self):
        """Test Ω3 NFT metadata generation."""
        result = custom_function(test_data)
        if "nft_metadata" in result:
            metadata = result["nft_metadata"]
            self.assertEqual(metadata["@context"], "https://schema.org")
            self.assertIn("variableMeasured", metadata)

if __name__ == "__main__":
    unittest.main()
```

## Best Practices

### 1. Always Include Integrity Hashing (Ω6)

```python
from omega_auto import compute_ipfs_hash

def my_analysis_function(data):
    results = {"key": "value"}
    results["ipfs_hash"] = compute_ipfs_hash(results)
    return results
```

### 2. Generate NFT-Compatible Metadata (Ω3)

```python
from omega_auto import generate_nft_metadata

def my_validation_function(event):
    results = validate(event)
    results["nft_metadata"] = generate_nft_metadata(event, results)
    return results
```

### 3. Use JAX for GPU Acceleration When Available

```python
try:
    import jax.numpy as jnp
    from jax import jit
    JAX_AVAILABLE = True
except ImportError:
    import numpy as jnp
    JAX_AVAILABLE = False

@jit if JAX_AVAILABLE else lambda x: x
def compute_intensive_operation(data):
    return jnp.fft.rfft(data)
```

### 4. Make Predictions Testable and Falsifiable

```python
def generate_prediction():
    return {
        "hypothesis": "Clear statement of prediction",
        "frequency_hz": 123.456,
        "testable": True,
        "falsifiable": True,
        "test_method": "PSD analysis with SNR > 5.0",
        "dataset": "GWTC-4 or O5 observations",
        "confidence": "medium"  # low, medium, high
    }
```

### 5. Include Timestamps and Provenance

```python
from datetime import datetime

def create_result():
    return {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "generated_by": "omega-custom-module",
        "source_code": "https://github.com/motanova84/141hz"
    }
```

### 6. Follow the Omega Naming Convention

- `omega_*.py` - Core Omega modules
- `test_omega_*.py` - Test files
- `demo_omega_*.py` - Demonstration scripts

### 7. Write Comprehensive Documentation

```python
def my_function(param1: type, param2: type) -> type:
    """
    One-line summary.
    
    Longer description explaining the Omega layer this relates to
    (Ω1-Ω6) and the scientific purpose.
    
    Args:
        param1: Description with units
        param2: Description with constraints
        
    Returns:
        Description of return value structure
        
    Example:
        >>> result = my_function(data, 141.7001)
        >>> print(result["snr"])
        15.23
    """
    pass
```

## Advanced: Creating a Complete Omega Layer Extension

### Example: Ω7 Auto-Discovery Layer

```python
# omega_discovery.py
"""
Ω7 Auto-Discovery Layer
========================

Automatically discovers new resonance frequencies from data
without prior hypotheses.
"""

import numpy as np
from typing import List, Dict
from omega_auto import omega_psd, compute_ipfs_hash
from datetime import datetime

def discover_resonances(strain: np.ndarray, 
                       fs: int,
                       threshold: float = 5.0) -> List[Dict]:
    """
    Ω7 Auto-Discovery: Find unexpected resonances.
    
    Args:
        strain: Time series data
        fs: Sampling frequency
        threshold: SNR threshold for detection
        
    Returns:
        List of discovered resonances
    """
    # Compute PSD
    freqs, psd = omega_psd(strain, fs)
    
    # Find peaks above threshold
    mean_psd = np.mean(psd)
    std_psd = np.std(psd)
    threshold_psd = mean_psd + threshold * std_psd
    
    peaks = []
    for i in range(1, len(psd)-1):
        if psd[i] > threshold_psd and psd[i] > psd[i-1] and psd[i] > psd[i+1]:
            peaks.append({
                "frequency_hz": round(float(freqs[i]), 6),
                "power": float(psd[i]),
                "snr": float(psd[i] / mean_psd),
                "discovered_at": datetime.now().isoformat(),
                "discovery_method": "omega-7-peak-detection"
            })
    
    # Add integrity hash
    for peak in peaks:
        peak["ipfs_hash"] = compute_ipfs_hash(peak)
    
    return peaks
```

## Contributing Your Extensions

1. Fork the repository
2. Create a feature branch: `git checkout -b omega-feature-name`
3. Add your extension following the patterns above
4. Write tests with >80% coverage
5. Update documentation
6. Submit a pull request

## Questions and Support

- GitHub Issues: https://github.com/motanova84/141hz/issues
- Documentation: [OMEGA_INFINITY_README.md](OMEGA_INFINITY_README.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**"The Omega system grows stronger with every contribution."**

🌌 Ω∞³ - Infinitely extensible, eternally autonomous
