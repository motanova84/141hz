# Quick Start Guide: Synthetic Datasets & Benchmarking

This guide helps you quickly get started with the new synthetic dataset generation and benchmarking tools.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Or install minimal requirements
pip install numpy scipy h5py matplotlib
```

## 5-Minute Quick Start

### 1. Generate Your First Synthetic Dataset

```bash
# Generate a simple 141.7 Hz signal (takes ~1 second)
python scripts/generar_datos_prueba.py

# Output: data/raw/H1-GW150914-32s.hdf5
```

### 2. Validate the Dataset

```bash
# Check if the dataset is valid
python scripts/validate_synthetic_data.py \
    --input data/raw/H1-GW150914-32s.hdf5 \
    --expected-freq 141.7

# Should see: ✅ VALIDATION PASSED
```

### 3. Run a Quick Benchmark

```bash
# Test numerical precision (takes ~5 seconds)
python scripts/benchmark_numerical_precision.py

# Output: results/benchmark/numerical_precision.json
# Shows: float64 gives 16 digits accuracy ✅
```

### 4. Generate Comparison Plots

```bash
# Visualize all benchmark results
python scripts/visualize_benchmarks.py --all

# Output: results/benchmark/plots/*.png
```

**Congratulations!** You've just generated synthetic data, validated it, benchmarked the analysis, and visualized the results. 🎉

## Common Use Cases

### Use Case 1: Test Your Analysis Algorithm

```bash
# 1. Generate test data with known signal
python scripts/synthetic_datasets/generate_merger_signal.py \
    --frequency-ringdown 141.7 \
    --target-snr 10

# 2. Run your analysis
python your_analysis_script.py \
    --data data/synthetic/merger_141hz.hdf5

# 3. Verify you detected 141.7 Hz (± 0.5 Hz)
```

### Use Case 2: Study Detection Threshold

```bash
# 1. Generate SNR sweep (2 to 20, 10 steps)
python scripts/synthetic_datasets/generate_parameter_sweep.py \
    --parameter snr \
    --range 2,20 \
    --steps 10

# 2. Analyze each dataset
for file in data/synthetic/sweep/*.hdf5; do
    python scripts/analizar_ringdown.py --data $file
done

# 3. Find minimum detectable SNR
```

### Use Case 3: Test Robustness to Noise

```bash
# 1. Generate noisy data with glitches
python scripts/synthetic_datasets/generate_with_glitches.py \
    --glitch-rate 0.3

# 2. Test your analysis pipeline
python scripts/analizar_ringdown.py \
    --data data/synthetic/with_glitches.hdf5

# 3. Verify detection works despite glitches
```

### Use Case 4: Benchmark Performance

```bash
# 1. Run GW analysis benchmark
python scripts/benchmark_gw_analysis.py --snr 10

# 2. Run precision benchmark  
python scripts/benchmark_numerical_precision.py

# 3. Generate comparison plots
python scripts/visualize_benchmarks.py --all

# 4. View results
ls results/benchmark/plots/
# gw_analysis_comparison.png
# numerical_precision_comparison.png
```

### Use Case 5: Multi-Detector Analysis

```bash
# 1. Generate coherent multi-detector signals
python scripts/synthetic_datasets/generate_multidetector.py \
    --detectors H1,L1,V1

# 2. Run multi-detector analysis
python scripts/analisis_coherencia_multidetector.py \
    --h1 data/synthetic/H1-multidetector.hdf5 \
    --l1 data/synthetic/L1-multidetector.hdf5 \
    --v1 data/synthetic/V1-multidetector.hdf5

# 3. Check coherence at 141.7 Hz
```

## Command Reference

### Dataset Generation

| Command | Description | Output |
|---------|-------------|--------|
| `generar_datos_prueba.py` | Simple 141.7 Hz signal | `data/raw/*.hdf5` |
| `generate_merger_signal.py` | Full BBH merger | `data/synthetic/merger_141hz.hdf5` |
| `generate_multidetector.py` | Multi-detector network | `data/synthetic/{H1,L1,V1}-*.hdf5` |
| `generate_with_glitches.py` | Noisy data with artifacts | `data/synthetic/with_glitches.hdf5` |
| `generate_parameter_sweep.py` | Parameter variations | `data/synthetic/sweep/*.hdf5` |

### Validation

| Command | Description | Output |
|---------|-------------|--------|
| `validate_synthetic_data.py --input FILE` | Validate one file | Terminal output |
| `validate_synthetic_data.py --all` | Validate all in data/synthetic/ | Summary report |

### Benchmarking

| Command | Description | Output |
|---------|-------------|--------|
| `benchmark_gw_analysis.py` | Framework comparison | `results/benchmark/gw_analysis_benchmark.json` |
| `benchmark_numerical_precision.py` | Precision testing | `results/benchmark/numerical_precision.json` |
| `benchmark_quantum_solvers.py` | Quantum solver comparison | `results/benchmark_results.json` |
| `visualize_benchmarks.py --all` | Generate all plots | `results/benchmark/plots/*.png` |

## Tips & Tricks

### Faster Testing
```bash
# Use shorter duration for quick tests
python generate_merger_signal.py --duration 8
```

### Higher Precision
```bash
# Generate with higher SNR for easier detection
python generate_merger_signal.py --target-snr 20
```

### Reproducibility
```bash
# Use fixed seed for reproducible results
python generate_merger_signal.py --seed 42
```

### Batch Processing
```bash
# Process all sweep files at once
for file in data/synthetic/sweep/*.hdf5; do
    echo "Processing $file..."
    python your_script.py --data $file
done
```

### CI/CD Integration
```bash
# Headless mode (no plots)
export HEADLESS_MODE=1
python scripts/benchmark_gw_analysis.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
# Install all requirements
pip install -r requirements.txt
```

### "File not found: data/synthetic/"
```bash
# Directory created automatically on first use
# Or create manually:
mkdir -p data/synthetic
```

### "Validation failed"
```bash
# Check the specific error message
# Common issues:
# - File format incorrect → regenerate dataset
# - SNR too low → increase with --target-snr
# - Sample rate too low → increase with --sample-rate
```

### Benchmarks show "Not available"
```bash
# Some frameworks are optional
# Install with:
pip install gwpy  # For GWPy
pip install pycbc  # For PyCBC
pip install mpmath  # For high precision
```

## Getting Help

- **Comprehensive Guide**: [docs/SYNTHETIC_DATASETS.md](docs/SYNTHETIC_DATASETS.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Benchmarking**: [BENCHMARKING.md](BENCHMARKING.md)
- **Issues**: [GitHub Issues](https://github.com/motanova84/141hz/issues)

## Next Steps

1. ✅ **Read** [docs/SYNTHETIC_DATASETS.md](docs/SYNTHETIC_DATASETS.md) for comprehensive documentation
2. ✅ **Explore** different dataset types for your use case
3. ✅ **Benchmark** your analysis against standard frameworks
4. ✅ **Contribute** by improving generators or adding new ones

**Happy testing!** 🚀
