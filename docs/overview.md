# QCAL Overview

## What is QCAL?

QCAL (Quantum Coherence Analysis for LLMs) is an open-source framework for detecting and validating coherence in the 141.7 Hz frequency band of gravitational wave data. It provides:

- **Detection**: Spectral analysis tools to identify the f₀ = 141.7001 Hz component in GW events
- **Validation**: Statistical validation using quantum radio (r_ψ), quantum energy (E_cuántica), and discrete symmetry
- **CLI**: Command-line interface for reproducible analysis
- **Pipelines**: Automated workflows for multi-event analysis

## Core Features

### 1. High-Precision Detection

QCAL uses Power Spectral Density (PSD) analysis with arbitrary precision arithmetic (via `mpmath`) to detect spectral features at 141.7001 Hz with sub-Hz resolution.

Key capabilities:
- Multi-detector support (H1, L1, V1, KAGRA)
- Configurable frequency bands and precision levels
- SNR calculation and statistical significance testing
- Automated data download from GWOSC

### 2. Three-Pillar Validation

All detections are validated using three independent criteria:

1. **Quantum Radio (r_ψ)**: Ratio between coherent and vacuum energy
2. **Quantum Energy (E_cuántica)**: Energy density at f₀
3. **Discrete Symmetry**: Phase coherence across detectors

### 3. Reproducible Pipelines

QCAL includes pre-configured pipelines for:
- GWTC-1 catalog analysis (11 events)
- O4 catalog analysis (5+ events)
- Custom event analysis
- Multi-detector coherence validation

### 4. Scientific Rigor

- All results include confidence intervals and p-values
- Reproducible workflows with versioned dependencies
- Comprehensive logging and artifact generation
- DOI-referenced validation protocols

## Architecture

```
qcal/
├── __init__.py          # Core module exports
├── coherence.py         # Ψ = I × A_eff² metrics
└── metrics.py           # Statistical metrics (KL, SNR, etc.)

scripts/
├── analisis_catalogo_o4.py
├── validacion_gwtc1_tridetector.py
└── test_*.py

docs/
├── overview.md          # This file
├── cli.md               # CLI usage
├── validation.md        # Validation protocols
└── roadmap.md           # Development roadmap
```

## Key Results

### GWTC-1 Validation (11 events)
- **H1**: 11/11 detected (100%), SNR = 21.38 ± 6.38
- **L1**: 11/11 detected (100%), SNR = 15.00 ± 8.12
- **V1**: 3/3 detected (100%), SNR = 8.17 ± 0.36
- **Combined significance**: >10σ (p < 10⁻²⁵)

### O4 Catalog (5 events)
- Mean Δf: -0.6261 Hz ± 0.6186 Hz
- p-value: 0.0864
- Relative power: +1.71 dB over baseline
- 100% detection rate within tolerance

## Scientific References

- **Main DOI**: [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)
- **Formal Verification**: [10.5281/zenodo.17379721](https://doi.org/10.5281/zenodo.17379721)
- **GWOSC**: [https://gwosc.org](https://gwosc.org)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run GWTC-1 validation
qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts

# Run O4 analysis
python3 scripts/analisis_catalogo_o4.py

# View results
ls artifacts/
```

## License

QCAL is released under the MIT License. See [LICENSE](../LICENSE) for details.

## Citation

If you use QCAL in your research, please cite:

```bibtex
@software{qcal2025,
  author = {Mota Burruezo, José Manuel},
  title = {QCAL: Quantum Coherence Analysis for LLMs and Gravitational Waves},
  year = {2025},
  url = {https://github.com/motanova84/141hz},
  doi = {10.5281/zenodo.17445017}
}
```
