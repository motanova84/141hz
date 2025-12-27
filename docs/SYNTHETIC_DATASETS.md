# Synthetic Datasets Documentation

This document provides comprehensive documentation for generating and using synthetic gravitational wave datasets for testing, validation, and development.

## Table of Contents

1. [Overview](#overview)
2. [Dataset Types](#dataset-types)
3. [Quick Start](#quick-start)
4. [Detailed Usage](#detailed-usage)
5. [Validation](#validation)
6. [Use Cases](#use-cases)

## Overview

Synthetic datasets are crucial for:

- **Testing**: Validate algorithms with known signals
- **Development**: Work without internet/GWOSC access
- **CI/CD**: Fast automated testing
- **Education**: Understand signal characteristics
- **Benchmarking**: Compare implementations

All synthetic datasets are:
- ✅ HDF5 format compatible with GWPy
- ✅ Reproducible (fixed random seeds)
- ✅ Documented with generation parameters
- ✅ Validated for physical realism

## Dataset Types

### 1. Simple 141.7 Hz Signal

**Purpose**: Basic validation of 141.7 Hz detection

**Generation**:
```bash
python scripts/generar_datos_prueba.py
```

**Parameters**:
- Frequency: 141.7 Hz (exact)
- Duration: 32 seconds
- Sample rate: 4096 Hz
- SNR: ~2.0
- Noise: Gaussian white noise

**Output**: `data/raw/H1-GW150914-32s.hdf5`

**Use Case**: Quick validation that analysis pipeline detects 141.7 Hz component

**Expected Results**:
```python
# After running analysis
detected_frequency = 141.7 ± 0.1 Hz
snr = 2.0 ± 0.2
confidence = > 95%
```

### 2. Full Merger Signal

**Purpose**: Realistic BBH merger with 141.7 Hz ringdown

**Generation**:
```bash
python scripts/synthetic_datasets/generate_merger_signal.py \
    --mass1 36 \
    --mass2 29 \
    --distance 410 \
    --frequency-ringdown 141.7 \
    --output data/synthetic/merger_141hz.hdf5
```

**Parameters**:
- Primary mass: 36 M☉
- Secondary mass: 29 M☉
- Luminosity distance: 410 Mpc
- Ringdown frequency: 141.7 Hz
- Includes: Inspiral + Merger + Ringdown

**Signal Components**:
1. **Inspiral** (t < 0): Chirp signal, frequency increases
2. **Merger** (t = 0): Peak amplitude
3. **Ringdown** (t > 0): Damped sinusoid at 141.7 Hz

**Use Case**: Full pipeline testing including parameter estimation

### 3. Multi-Detector Network

**Purpose**: Coherent signal across H1, L1, V1

**Generation**:
```bash
python scripts/synthetic_datasets/generate_multidetector.py \
    --detectors H1,L1,V1 \
    --ra 1.95 \
    --dec -1.27 \
    --frequency 141.7
```

**Parameters**:
- Detectors: H1 (Hanford), L1 (Livingston), V1 (Virgo)
- Sky position: (RA=1.95, Dec=-1.27) rad
- Time delays: Calculated from detector geometry
- Antenna patterns: Detector-specific response

**Output Files**:
- `data/synthetic/H1-multidetector.hdf5`
- `data/synthetic/L1-multidetector.hdf5`
- `data/synthetic/V1-multidetector.hdf5`

**Use Case**: Testing coherent multi-detector analysis and sky localization

### 4. Noisy Realistic Data

**Purpose**: Data with instrumental artifacts

**Generation**:
```bash
python scripts/synthetic_datasets/generate_with_glitches.py \
    --glitch-rate 0.1 \
    --glitch-types blip,tomte
```

**Includes**:
- Blip glitches (common transient noise)
- Tomte glitches (violin modes)
- Power line harmonics (60 Hz, 120 Hz)
- Non-stationary noise

**Use Case**: Test robustness of analysis to instrumental artifacts

### 5. Parameter Sweep Datasets

**Purpose**: Systematic variation of parameters

**Generation**:
```bash
python scripts/synthetic_datasets/generate_parameter_sweep.py \
    --parameter frequency \
    --range 130,150 \
    --steps 20
```

**Creates**: 20 datasets with frequencies from 130-150 Hz

**Use Case**: Validate frequency resolution and detection threshold

## Quick Start

### Generate Basic Dataset

```bash
# 1. Generate simple 141.7 Hz signal
python scripts/generar_datos_prueba.py

# 2. Verify generation
ls -lh data/raw/H1-GW150914-32s.hdf5

# 3. Test with analysis
python scripts/analizar_ringdown.py

# 4. Check results
cat results/figures/analysis_summary.txt
```

### Generate Full Merger

```bash
# Generate realistic merger
python scripts/synthetic_datasets/generate_merger_signal.py \
    --mass1 36 \
    --mass2 29 \
    --frequency-ringdown 141.7 \
    --target-snr 10

# Validate signal quality
python scripts/validate_synthetic_data.py \
    --input data/synthetic/merger_141hz.hdf5

# Run full analysis
python scripts/analizar_gw250114.py \
    --data data/synthetic/merger_141hz.hdf5
```

## Detailed Usage

### Customizing Signal Parameters

#### Frequency Adjustment

```python
# scripts/synthetic_datasets/generate_merger_signal.py

# Modify ringdown frequency
ringdown_frequency = 141.7  # Hz

# Adjust chirp parameters
f_low = 20  # Hz (starting frequency)
f_high = 500  # Hz (ending frequency)
```

#### Noise Configuration

```python
# Noise level
noise_amplitude = 1e-18  # Realistic LIGO strain

# PSD from file
from gwpy.timeseries import TimeSeries
psd_file = "data/reference/LIGO_O2_PSD.txt"
noise = TimeSeries.read(psd_file)
```

#### Signal Strength

```python
# Distance (affects amplitude)
distance = 410  # Mpc (GW150914-like)
distance = 100  # Mpc (stronger signal)
distance = 1000  # Mpc (weaker signal)

# SNR targeting
target_snr = 25
# Code automatically scales amplitude
```

### Format Specification

All synthetic datasets use this HDF5 structure:

```
dataset.hdf5
├── strain/
│   ├── Strain [array]          # Time series data
│   ├── Xstart [float]          # GPS start time
│   └── Xspacing [float]        # Time step (1/sample_rate)
└── metadata/
    ├── parameters [group]       # Generation parameters
    │   ├── frequency [float]
    │   ├── snr [float]
    │   └── ...
    └── injections [group]       # Injected signals (if any)
        ├── time [float]
        ├── frequency [float]
        └── amplitude [float]
```

### Reading Synthetic Data

```python
import h5py
from gwpy.timeseries import TimeSeries

# Method 1: Using GWPy (recommended)
data = TimeSeries.read('data/synthetic/signal.hdf5', format='hdf5')

# Method 2: Direct HDF5
with h5py.File('data/synthetic/signal.hdf5', 'r') as f:
    strain = f['strain/Strain'][:]
    t0 = f['strain/Xstart'][()]
    dt = f['strain/Xspacing'][()]
    
# Get metadata
with h5py.File('data/synthetic/signal.hdf5', 'r') as f:
    injected_freq = f['metadata/parameters/frequency'][()]
    injected_snr = f['metadata/parameters/snr'][()]
```

## Validation

### Automatic Validation

```bash
# Validate all synthetic datasets
python scripts/validate_synthetic_data.py --all

# Validate specific file
python scripts/validate_synthetic_data.py \
    --input data/synthetic/merger_141hz.hdf5
```

### Validation Checks

1. **Format Validation**
   - ✓ HDF5 structure correct
   - ✓ Required fields present
   - ✓ Data types correct

2. **Physical Validation**
   - ✓ Sample rate appropriate (≥ 2 × max frequency)
   - ✓ Duration sufficient for analysis
   - ✓ Amplitude physically reasonable

3. **Signal Validation**
   - ✓ Injected signal recoverable
   - ✓ SNR matches specification
   - ✓ Frequency content as expected

4. **Noise Validation**
   - ✓ PSD realistic for detector
   - ✓ Stationarity within bounds
   - ✓ No obvious artifacts

### Manual Validation

```python
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries

# Load data
data = TimeSeries.read('data/synthetic/signal.hdf5')

# Plot time series
plt.figure(figsize=(12, 4))
plt.plot(data.times.value, data.value)
plt.xlabel('Time (s)')
plt.ylabel('Strain')
plt.title('Synthetic Signal')
plt.savefig('validation_timeseries.png')

# Plot spectrum
asd = data.asd(fftlength=4)
plt.figure(figsize=(12, 6))
plt.loglog(asd.frequencies.value, asd.value)
plt.xlabel('Frequency (Hz)')
plt.ylabel('ASD (strain/√Hz)')
plt.title('Amplitude Spectral Density')
plt.xlim(10, 500)
plt.savefig('validation_asd.png')
```

## Use Cases

### 1. Algorithm Development

**Scenario**: Developing new 141.7 Hz detection algorithm

```bash
# Generate test dataset
python scripts/generar_datos_prueba.py

# Develop algorithm
vim my_new_algorithm.py

# Test algorithm
python my_new_algorithm.py --data data/raw/H1-GW150914-32s.hdf5

# Verify detection
# Expected: frequency = 141.7 ± 0.1 Hz
```

### 2. CI/CD Testing

**Scenario**: Automated testing in GitHub Actions

```yaml
# .github/workflows/test.yml
- name: Generate synthetic data
  run: python scripts/generar_datos_prueba.py

- name: Run analysis
  run: python scripts/analizar_ringdown.py

- name: Verify results
  run: |
    python -c "
    import json
    with open('results/analysis_results.json') as f:
        r = json.load(f)
    assert 141.6 < r['peak_frequency'] < 141.8
    print('✅ Detection verified')
    "
```

### 3. Parameter Estimation Studies

**Scenario**: Study parameter estimation accuracy

```bash
# Generate datasets with varying SNR
for snr in 5 10 15 20 25 30; do
    python scripts/synthetic_datasets/generate_merger_signal.py \
        --target-snr $snr \
        --output data/synthetic/merger_snr${snr}.hdf5
done

# Run parameter estimation on each
python scripts/parameter_estimation_study.py \
    --input-dir data/synthetic/ \
    --output results/pe_accuracy.json
```

### 4. Multi-Detector Coherence

**Scenario**: Test coherence analysis

```bash
# Generate multi-detector data
python scripts/synthetic_datasets/generate_multidetector.py

# Run coherence analysis
python scripts/analisis_coherencia_multidetector.py \
    --h1 data/synthetic/H1-multidetector.hdf5 \
    --l1 data/synthetic/L1-multidetector.hdf5 \
    --v1 data/synthetic/V1-multidetector.hdf5

# Expected: coherence > 0.8 at 141.7 Hz
```

### 5. Robustness Testing

**Scenario**: Test robustness to glitches

```bash
# Generate data with glitches
python scripts/synthetic_datasets/generate_with_glitches.py \
    --glitch-rate 0.2

# Run analysis
python scripts/analizar_ringdown.py \
    --data data/synthetic/with_glitches.hdf5 \
    --robust-mode

# Should still detect 141.7 Hz despite glitches
```

## Best Practices

### Random Seeds

Always use fixed random seeds for reproducibility:

```python
import numpy as np
np.random.seed(42)  # Fixed seed for reproducibility
```

### Documentation

Document generation parameters in HDF5 metadata:

```python
with h5py.File(output_file, 'w') as f:
    # Save data
    f.create_dataset('strain/Strain', data=strain)
    
    # Save parameters
    params = f.create_group('metadata/parameters')
    params['frequency'] = 141.7
    params['snr'] = 2.0
    params['seed'] = 42
    params['generation_date'] = datetime.now().isoformat()
```

### Version Control

Add reference results to git:

```bash
# Generate reference dataset
python scripts/generar_datos_prueba.py

# Analyze and save results
python scripts/analizar_ringdown.py
cp results/analysis_results.json data/reference/baseline_results.json

# Commit reference results
git add data/reference/baseline_results.json
git commit -m "Add baseline reference results"
```

### Testing

Always include synthetic data tests:

```python
# tests/test_synthetic_data.py
import unittest

class TestSyntheticData(unittest.TestCase):
    def test_simple_signal_generation(self):
        """Test basic signal generation"""
        # Generate
        subprocess.run(['python', 'scripts/generar_datos_prueba.py'])
        
        # Verify file exists
        self.assertTrue(Path('data/raw/H1-GW150914-32s.hdf5').exists())
        
        # Verify format
        data = TimeSeries.read('data/raw/H1-GW150914-32s.hdf5')
        self.assertEqual(data.sample_rate.value, 4096)
```

## Troubleshooting

### Common Issues

#### "HDF5 format error"

```bash
# Verify file integrity
h5dump -H data/synthetic/signal.hdf5

# Regenerate if corrupted
rm data/synthetic/signal.hdf5
python scripts/synthetic_datasets/generate_merger_signal.py
```

#### "Signal not detected"

```bash
# Check SNR of injected signal
python scripts/validate_synthetic_data.py --input data/synthetic/signal.hdf5

# If SNR too low, regenerate with higher SNR
python scripts/synthetic_datasets/generate_merger_signal.py --target-snr 10
```

#### "Memory error"

```bash
# Reduce duration or sample rate
python scripts/generar_datos_prueba.py --duration 16 --sample-rate 2048
```

## References

1. **GWPy Documentation**: https://gwpy.github.io/
2. **GWOSC Tutorials**: https://gwosc.org/tutorials/
3. **PyCBC Documentation**: https://pycbc.org/
4. **LIGO Data Format**: https://dcc.ligo.org/

## Contributing

To add new synthetic dataset types:

1. Create generation script in `scripts/synthetic_datasets/`
2. Document parameters and use cases here
3. Add validation tests
4. Update CI/CD workflows if needed

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

**Last Updated**: 2025-11-05  
**Maintained by**: José Manuel Mota Burruezo (JMMB)
