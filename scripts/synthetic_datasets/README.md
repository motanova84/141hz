# Synthetic Dataset Generators

This directory contains scripts for generating synthetic gravitational wave datasets for testing and validation.

## Quick Start

### Generate Simple Signal
```bash
python scripts/generar_datos_prueba.py
```
Output: `data/raw/H1-GW150914-32s.hdf5`

### Generate Full Merger Signal
```bash
python scripts/synthetic_datasets/generate_merger_signal.py --target-snr 10
```
Output: `data/synthetic/merger_141hz.hdf5`

### Generate Multi-Detector Data
```bash
python scripts/synthetic_datasets/generate_multidetector.py
```
Outputs: `data/synthetic/{H1,L1,V1}-multidetector.hdf5`

### Generate Data with Glitches
```bash
python scripts/synthetic_datasets/generate_with_glitches.py --glitch-rate 0.2
```
Output: `data/synthetic/with_glitches.hdf5`

### Generate Parameter Sweep
```bash
# Frequency sweep
python scripts/synthetic_datasets/generate_parameter_sweep.py \
    --parameter frequency --range 130,150 --steps 20

# SNR sweep
python scripts/synthetic_datasets/generate_parameter_sweep.py \
    --parameter snr --range 2,20 --steps 10

# Duration sweep
python scripts/synthetic_datasets/generate_parameter_sweep.py \
    --parameter duration --range 8,64 --steps 8
```
Outputs: `data/synthetic/sweep/*.hdf5` + manifest.json

## Validation

Validate any synthetic dataset:
```bash
python scripts/validate_synthetic_data.py --input data/synthetic/merger_141hz.hdf5
```

Validate all synthetic datasets:
```bash
python scripts/validate_synthetic_data.py --all
```

## Available Generators

| Script | Description | Key Parameters |
|--------|-------------|----------------|
| `generate_merger_signal.py` | Full BBH merger with ringdown | `--mass1`, `--mass2`, `--frequency-ringdown`, `--target-snr` |
| `generate_multidetector.py` | Multi-detector coherent signals | `--detectors`, `--ra`, `--dec` |
| `generate_with_glitches.py` | Signals with instrumental artifacts | `--glitch-rate`, `--glitch-types` |
| `generate_parameter_sweep.py` | Systematic parameter variations | `--parameter`, `--range`, `--steps` |

## Documentation

For comprehensive documentation, see: [docs/SYNTHETIC_DATASETS.md](../../docs/SYNTHETIC_DATASETS.md)

## Use Cases

### Testing Detection Algorithms
```bash
# Generate test signal
python generate_merger_signal.py --target-snr 5

# Test your algorithm
python your_algorithm.py --data data/synthetic/merger_141hz.hdf5
```

### Studying Detection Thresholds
```bash
# Generate SNR sweep
python generate_parameter_sweep.py --parameter snr --range 1,10 --steps 20

# Analyze all datasets
for file in data/synthetic/sweep/*.hdf5; do
    python scripts/analizar_ringdown.py --data $file
done
```

### Testing Robustness to Glitches
```bash
# Generate noisy data
python generate_with_glitches.py --glitch-rate 0.5

# Test robust analysis
python scripts/analizar_ringdown.py --data data/synthetic/with_glitches.hdf5 --robust
```

## Notes

- All generators use fixed random seeds by default (seed=42) for reproducibility
- Datasets are saved in GWPy-compatible HDF5 format
- Metadata is embedded in each file for full traceability
- Generated files are excluded from git (see `.gitignore`)

## Contributing

To add a new generator:
1. Create script in this directory
2. Follow the naming convention: `generate_*.py`
3. Include `--help` documentation
4. Add validation support
5. Update this README and docs/SYNTHETIC_DATASETS.md
6. Add tests if appropriate

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.
