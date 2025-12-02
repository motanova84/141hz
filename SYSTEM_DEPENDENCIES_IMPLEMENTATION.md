# System Dependencies Implementation

## Overview

This document describes the implementation of system-level dependencies required for numba, python-igraph, and numexpr packages to work correctly in GitHub Actions CI/CD environments.

## Problem Statement

The issue identified three packages that require system-level dependencies or special configuration:

1. **numba** - Requires llvmlite and native LLVM compilers
2. **python-igraph** - Requires libigraph as a binary dependency
3. **numexpr** - Can fail if it doesn't detect CPU properly in virtual runners

## Solution Implemented

### 1. System Package Installation

Added system package installation steps to both GitHub Actions workflows:

**Packages installed:**
- `libigraph-dev` - Development headers for igraph library
- `libigraph3t64` - Runtime library for igraph
- `llvm-dev` - LLVM development tools for numba/llvmlite
- `build-essential` - Essential build tools (gcc, g++, make)
- `gfortran` - Fortran compiler for scientific computing

**Modified workflows:**
- `.github/workflows/analyze.yml` - CI/CD Tests and Analysis workflow
- `.github/workflows/production-qcal.yml` - QCAL Production Cycle workflow

### 2. Python Package Requirements

Added the following packages to `requirements.txt`:

```txt
# Performance and optimization packages
numba>=0.56.0
llvmlite>=0.39.0
python-igraph>=0.10.0
numexpr>=2.8.0
```

### 3. Environment Variables for numexpr

Added environment variables to help numexpr detect CPU features correctly in virtual environments:

```yaml
env:
  NUMEXPR_MAX_THREADS: 4
  NUMEXPR_NUM_THREADS: 2
```

These variables are set in all steps that run Python code to ensure consistent behavior.

## Workflow Changes Detail

### analyze.yml (CI/CD Workflow)

#### Test Job
- Added system dependencies installation after Python setup
- Added NUMEXPR environment variables to:
  - Dependency installation step
  - Unit tests execution
  - Pytest execution

#### Analysis Job
- Added system dependencies installation after Python setup
- Added NUMEXPR environment variables to:
  - Dependency installation step
  - Data download step
  - Validation pipeline execution

### production-qcal.yml (Production Workflow)

- Added system dependencies installation after Python 3.11 setup
- Added NUMEXPR environment variables to:
  - Dependency installation step
  - Core validation step
  - Results aggregation step

## Testing

Created a comprehensive test script (`scripts/test_performance_packages.py`) that validates:

1. **llvmlite** - Can be imported successfully
2. **numba** - JIT compilation works with both scalars and arrays
3. **python-igraph** - Graph creation and operations work correctly
4. **numexpr** - Numerical computations work and CPU cores are detected

### Test Results

All tests passed successfully:

```
✅ llvmlite 0.45.1 - Imported successfully
✅ numba 0.62.1 - JIT compilation works correctly
✅ python-igraph 0.11.9 - Graph operations work correctly
✅ numexpr 2.14.1 - Computation works, detected 4 cores
```

## Benefits

1. **numba/llvmlite**: Enables JIT compilation for performance-critical numerical code
2. **python-igraph**: Provides efficient graph algorithms for network analysis
3. **numexpr**: Accelerates numerical array operations with proper CPU feature detection
4. **Consistency**: All packages work reliably across different CI/CD runs
5. **Reproducibility**: Results are consistent across different environments

## Usage in Project

These packages can now be used throughout the project for:

- **numba**: Accelerating computationally intensive loops and numerical functions
- **python-igraph**: Network analysis and graph algorithms
- **numexpr**: Fast array operations, especially useful with pandas and numpy

Example usage:

```python
import numba
import numpy as np

@numba.jit(nopython=True)
def fast_computation(x):
    return x**2 + 2*x + 1

result = fast_computation(np.arange(1000000))
```

## Maintenance Notes

1. System packages are installed at the OS level using `apt-get`
2. Python packages use semantic versioning (>=) to allow updates
3. Environment variables ensure consistent CPU detection
4. Test script should be run when updating package versions

## Related Files

- `.github/workflows/analyze.yml` - Main CI/CD workflow
- `.github/workflows/production-qcal.yml` - Production workflow
- `requirements.txt` - Python package requirements
- `scripts/test_performance_packages.py` - Validation test script

## References

- [numba documentation](https://numba.pydata.org/)
- [llvmlite documentation](https://llvmlite.readthedocs.io/)
- [python-igraph documentation](https://igraph.org/python/)
- [numexpr documentation](https://numexpr.readthedocs.io/)
