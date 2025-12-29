# QCAL Package Structure - Implementation Notes

## Overview

This implementation adds a complete QCAL (Quantum Coherence Analysis for gravitational waves at 141.7 Hz) package structure to the repository as specified in the problem statement.

## Package Structure

```
src/qcal/               # New QCAL signal processing package
├── __init__.py         # Package initialization
├── __main__.py         # CLI entry point with Click
└── analyze.py          # Signal analysis functions

tests/                  # New QCAL-specific tests
├── test_cli.py         # CLI tests
├── test_signal_band_141hz.py  # Signal analysis tests
└── test_hashes.py      # Basic validation tests

repro/GWTC-1/          # Reproducibility environment
├── requirements.in     # Direct dependencies
├── env.lock           # Locked dependencies with hashes
├── Makefile           # Build automation
└── run.sh             # Execution script
```

## Known Issue: Package Naming Conflict

⚠️ **Important**: There is a naming conflict with the existing `qcal` package in the repository root.

### Current Situation

- **Existing package**: `qcal/` (root level) - Quantum Coherence Analysis for LLMs
  - Purpose: Evaluating LLM outputs using quantum coherence metrics
  - Based on Ψ = I × A_eff² and f₀ = 141.7001 Hz
  
- **New package**: `src/qcal/` - Signal analysis for gravitational waves
  - Purpose: Reproducible coherence analysis of GW events at 141.7 Hz
  - CLI tool for catalog analysis (GWTC-1, O4)

### Resolution Options

1. **Rename the new package** (Recommended for production):
   - `qcal-gw` or `qcal-signal` or `gw-qcal`
   - Update `pyproject.qcal.toml` and `src/` directory accordingly

2. **Rename the existing package**:
   - `qcal-llm` for the LLM coherence analysis
   - Requires more extensive refactoring

3. **Keep as-is for demonstration**:
   - Use `run_qcal_tests.sh` which temporarily renames the root package
   - Document the conflict clearly

### Testing Workaround

The included `run_qcal_tests.sh` script handles the conflict by:
1. Temporarily renaming `qcal/` to `qcal_llm_backup/`
2. Running tests with `PYTHONPATH=src/`
3. Restoring the original `qcal/` directory

## Usage

### Running Tests

```bash
./run_qcal_tests.sh
```

### Using the CLI (with workaround)

```bash
# Option 1: Use PYTHONPATH
PYTHONPATH=src python3 -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1

# Option 2: Temporarily rename root qcal
mv qcal qcal_llm_backup
python3 -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1
mv qcal_llm_backup qcal
```

### Installation (requires resolution of naming conflict)

Once the naming conflict is resolved:

```bash
pip install -e .
qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts
```

## Reproducibility

Generate deterministic environment with hashed dependencies:

```bash
cd repro/GWTC-1
pip-compile --generate-hashes requirements.in -o env.lock
./run.sh
```

## Files Created

- `pyproject.qcal.toml` - Package configuration (setuptools-based)
- `README_QCAL.md` - QCAL-specific documentation
- `CITATION_QCAL.cff` - Citation metadata
- `DATASET_CARD.md` - Data provenance information
- `run_qcal_tests.sh` - Test runner handling package conflicts

## Future Work

1. Resolve package naming conflict
2. Set up CI/CD workflows for automated testing
3. Publish to PyPI once naming is resolved
4. Add GitHub workflows for reproducibility validation
5. Expand test coverage
6. Add integration tests with real GW data
