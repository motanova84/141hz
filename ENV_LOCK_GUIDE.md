# ENV.lock - Complete Reproducibility Guide for Auditors

## Overview

The `ENV.lock` file in this repository provides a **complete reproducibility manifest** that enables external auditors, reviewers, and researchers to reproduce all computational results bit-for-bit. This includes:

- 141.7001 Hz gravitational wave detections in GW150914, GW250114, and other events
- Riemann Hypothesis and BSD conjecture formalization proofs (Lean 4)
- P vs NP equivalence demonstrations
- Multi-event SNR analysis showing 18.2σ cumulative significance
- AT2020afhd harmonic analysis and noesis field verification

## What's in ENV.lock?

The `ENV.lock` file contains:

1. **System Information**: OS, architecture, kernel version, Python version
2. **Toolchain Versions**: GCC, GFortran, CMake, and other compilers
3. **Python Dependencies**: Exact package versions (NumPy, SciPy, etc.)
4. **External Tools**: Lean 4, SAT solvers, LALSuite versions (if used)
5. **Dataset Checksums**: SHA256 hashes of data files for integrity verification
6. **Configuration Parameters**: Random seeds, precision settings, physical constants
7. **Git State**: Commit SHA, branch information

Additionally, `ENV.lock.json` provides machine-readable metadata in JSON format.

## Quick Start for Auditors

### 1. Clone Repository

```bash
git clone https://github.com/motanova84/141hz.git
cd 141hz
```

### 2. Create Isolated Environment

```bash
# Create a fresh virtual environment
python3 -m venv venv_audit

# Activate it
source venv_audit/bin/activate  # On Windows: venv_audit\Scripts\activate
```

### 3. Install from ENV.lock

```bash
# Install exact versions from ENV.lock
pip install -r ENV.lock
```

This will install all Python dependencies with the exact versions used in the original analysis.

### 4. Verify Environment

```bash
# Run validation script
python scripts/validate_reproducibility.py --strict
```

This checks:
- ✅ Python version matches (3.11 or 3.12)
- ✅ All packages have correct versions
- ✅ Environment matches ENV.lock specifications

### 5. Reproduce Key Results

#### Validate Fundamental Frequency (141.7001 Hz)

```bash
python validate_v5_coronacion.py --precision 50
```

**Expected output**: Validates that f₀ = 141.7001 Hz with 50 decimal places of precision.

#### Verify Riemann Zeros Connection

```bash
python validate_riemann_zeros.py --precision 50
```

**Expected output**: Confirms relationship between Riemann zeros and f₀.

#### Analyze GW150914 (First Detection)

```bash
python analisis_completo_gw150914.py
```

**Expected output**: Shows 141.7 Hz resonance peak in GW150914 strain data.

#### Validate AT2020afhd Harmonic Detection

```bash
python validate_at2020afhd_harmonic.py
```

**Expected output**: Confirms 141.7 Hz harmonics in AT2020afhd transient.

## Dataset Access

### Gravitational Wave Data

Datasets are automatically downloaded from GWOSC (Gravitational Wave Open Science Center):

```bash
# List available datasets
python -c "from gwosc import datasets; print(datasets.find_datasets())"

# Data is downloaded automatically when running analysis scripts
```

### Manual Download (Optional)

If you prefer to download datasets manually:

```bash
# GW150914
wget https://gwosc.org/eventapi/html/GWTC-1-confident/GW150914/

# GW170814
wget https://gwosc.org/eventapi/html/GWTC-1-confident/GW170814/
```

### Dataset Verification

Check data integrity using checksums from ENV.lock:

```bash
# Example: Verify a data file
sha256sum data/calabi_yau_varieties.csv
# Compare with SHA256 in ENV.lock or ENV.lock.json
```

## Advanced Verification

### Hash-Verified Installation (Maximum Security)

For maximum security, use pip-compile with hash verification:

```bash
# See repro/GWTC-1/env.lock for example with full hashes
pip install --require-hashes -r repro/GWTC-1/env.lock
```

Or generate your own hashes:

```bash
pip-compile --generate-hashes requirements.txt -o ENV.lock.hashes
pip install --require-hashes -r ENV.lock.hashes
```

### Cross-Platform Verification

ENV.lock is designed to work across platforms with the same Python version:

| Platform | Python | Status | Notes |
|----------|--------|--------|-------|
| Ubuntu 22.04+ | 3.11, 3.12 | ✅ Tested | Recommended |
| Ubuntu 20.04 | 3.11, 3.12 | ✅ Works | Install Python from deadsnakes PPA |
| macOS 12+ | 3.11, 3.12 | ✅ Works | Use Homebrew Python |
| Windows 10/11 | 3.11, 3.12 | ⚠️ Untested | Should work with WSL2 |

### Precision Verification

Test that high-precision arithmetic works correctly:

```bash
# Test mpmath precision
python -c "import mpmath; mpmath.mp.dps=50; print('φ =', mpmath.phi)"
# Expected: φ = 1.6180339887498948482045868343656381177203091798058

# Test f₀ calculation
python -c "from qcal.core import f0; print(f'f₀ = {f0:.10f} Hz')"
# Expected: f₀ = 141.7001000000 Hz
```

## Understanding the Environment

### System Requirements

- **Python**: 3.11 or 3.12 (exact version documented in ENV.lock)
- **RAM**: Minimum 4GB, recommended 8GB+ for full analysis
- **Disk**: ~5GB for environment + datasets
- **CPU**: Multi-core recommended (some analysis uses parallel processing)

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | 1.26.4 | Numerical arrays and computations |
| scipy | 1.13.1 | Scientific algorithms, FFT |
| matplotlib | 3.9.0 | Visualization |
| mpmath | 1.3.0 | Arbitrary precision arithmetic |
| astropy | 6.1.0 | Astronomical data handling |
| h5py | 3.11.0 | HDF5 file I/O (LIGO data format) |

### Optional Dependencies

Some features require additional tools:

- **Lean 4**: For formal verification proofs (Riemann/BSD)
- **LALSuite**: For advanced gravitational wave analysis
- **SAT Solvers**: For P vs NP demonstrations

These are documented in ENV.lock but not required for core results.

## Configuration Parameters

### Random Seeds

For reproducibility of stochastic algorithms:

```python
import numpy as np
import random

np.random.seed(42)  # NumPy
random.seed(42)     # Python stdlib
```

### Precision Settings

```python
import mpmath

mpmath.mp.dps = 50  # 50 decimal places for high-precision calculations
```

### Physical Constants

Key constants used throughout:

- **f₀**: 141.7001 Hz (fundamental frequency)
- **κ**: (137 × φ) / π ≈ 68.50815 (structural constant)
- **φ**: (1 + √5) / 2 ≈ 1.618033988749 (golden ratio)
- **Ψ-NSE cutoff**: 100-250 Hz (bandpass filter)

## Troubleshooting

### Installation Issues

**Problem**: Package version conflicts

```bash
# Solution: Use a fresh virtual environment
deactivate  # If in existing venv
rm -rf venv_audit
python3 -m venv venv_audit
source venv_audit/bin/activate
pip install --upgrade pip
pip install -r ENV.lock
```

**Problem**: Missing system dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential gfortran libhdf5-dev

# macOS
brew install gcc hdf5
```

### Validation Failures

**Problem**: Python version mismatch

```bash
# Check your Python version
python --version

# Install correct version (Ubuntu example)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv
python3.12 -m venv venv_audit
```

**Problem**: Package version mismatch

```bash
# Check what's different
pip freeze > current_env.txt
diff ENV.lock current_env.txt

# Reinstall from scratch if needed
pip uninstall -y -r current_env.txt
pip install -r ENV.lock
```

### Dataset Download Issues

**Problem**: GWOSC connection timeout

```bash
# Try with longer timeout
python -c "from gwosc import datasets; datasets.find_datasets(timeout=60)"

# Or download manually
wget --timeout=60 https://gwosc.org/archive/...
```

## Regenerating ENV.lock

If you need to regenerate ENV.lock (e.g., after updating dependencies):

```bash
# Method 1: Use enhancement script (recommended)
python scripts/enhance_env_lock.py --input ENV.lock --output ENV.lock

# Method 2: From scratch
python scripts/generate_env_lock.py --output ENV.lock

# Method 3: Manual
python3 -m venv venv_temp
source venv_temp/bin/activate
pip install -r requirements.txt
pip freeze > ENV.lock
python scripts/enhance_env_lock.py  # Add metadata
deactivate
rm -rf venv_temp
```

## Verification Checklist for Auditors

Use this checklist to verify full reproducibility:

- [ ] Clone repository from GitHub
- [ ] Create fresh virtual environment with Python 3.11 or 3.12
- [ ] Install from ENV.lock: `pip install -r ENV.lock`
- [ ] Run validation: `python scripts/validate_reproducibility.py --strict`
- [ ] Verify Python version matches ENV.lock
- [ ] Verify all package versions match
- [ ] Run core validation: `python validate_v5_coronacion.py --precision 50`
- [ ] Verify f₀ = 141.7001 Hz with 50 decimal places
- [ ] Run Riemann validation: `python validate_riemann_zeros.py --precision 50`
- [ ] Analyze GW150914: `python analisis_completo_gw150914.py`
- [ ] Verify 141.7 Hz peak in GW150914 spectral analysis
- [ ] Check dataset checksums match ENV.lock.json
- [ ] Compare numerical results with published values
- [ ] Document any discrepancies or issues

## Reporting Issues

If you encounter reproducibility issues:

1. **Check ENV.lock version**: Ensure you're using the latest ENV.lock from main branch
2. **Verify system**: Run `python scripts/validate_reproducibility.py --generate-snapshot`
3. **Open GitHub Issue**: https://github.com/motanova84/141hz/issues
4. **Include information**:
   - Your Python version
   - OS and architecture
   - Output of validation script
   - Specific discrepancies observed

## References

- **ENV.lock specification**: This file
- **Reproducibility guide**: `REPRODUCIBILIDAD.md`
- **Security documentation**: `SECURITY.md`
- **Scientific method**: `TRES_PILARES_METODO_CIENTIFICO.md`

## Citation

When using ENV.lock for reproducibility verification, please cite:

```bibtex
@software{qcal_141hz_2026,
  title = {QCAL GW250114-141Hz Analysis: Complete Reproducibility Environment},
  author = {Motanova, et al.},
  year = {2026},
  url = {https://github.com/motanova84/141hz},
  doi = {10.5281/zenodo.17445017},
  version = {2.0.0}
}
```

## Contact

- **GitHub**: @motanova84
- **Issues**: https://github.com/motanova84/141hz/issues
- **Discussions**: https://github.com/motanova84/141hz/discussions

---

**Version**: 2.0.0  
**Last Updated**: 2026-01-18  
**Maintained By**: QCAL Team
