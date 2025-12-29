# Computational Optimization Guide

This guide covers the performance optimization features for large-scale gravitational wave analysis.

## Overview

Three main optimization areas:

1. **GPU Acceleration** - Speed up spectral analysis with CUDA/CuPy
2. **Compressed Storage** - Efficient data formats for large datasets
3. **HPC/Cloud Support** - Distributed processing for GWTC-3/GWTC-4 catalogs

## Quick Start

### Basic Usage

```python
from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
from gw_141hz_tools.compressed_io import DataManager

# Create analyzer (auto-detects GPU)
analyzer = SpectralAnalyzer(use_gpu=True, n_jobs=4)

# Load compressed data
dm = DataManager()
data, metadata = dm.load_timeseries('event_data.h5')

# Analyze
freqs, power = analyzer.compute_fft(data, sample_rate=4096)
result = analyzer.find_peaks(freqs, power, target_freq=141.7)

# Save compressed results
dm.save_compressed_numpy('results.npz', freqs=freqs, power=power)
```

### Command-Line Examples

```bash
# Single event analysis
python scripts/example_optimized_analysis.py --events GW150914

# Multiple events with parallel processing
python scripts/example_optimized_analysis.py \
  --events GW150914 GW151226 GW170814 \
  --n-jobs 4

# Analyze entire catalog
python scripts/example_optimized_analysis.py \
  --catalog GWTC-3 \
  --n-jobs 8

# GPU acceleration (if available)
python scripts/example_optimized_analysis.py \
  --catalog GWTC-3 \
  --use-gpu
```

## GPU Acceleration

### Installation

For CUDA 12.x:
```bash
pip install cupy-cuda12x
```

For CUDA 11.x:
```bash
pip install cupy-cuda11x
```

### Usage

```python
from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer

# GPU-accelerated analyzer
analyzer = SpectralAnalyzer(use_gpu=True)

# Automatic CPU fallback if GPU unavailable
analyzer = SpectralAnalyzer(use_gpu=True)  # Falls back to CPU gracefully
```

### Performance Benchmarks

Typical speedups for FFT operations:

| Data Size | CPU (numpy) | GPU (CuPy) | Speedup |
|-----------|-------------|------------|---------|
| 2^20 samples | 0.15s | 0.02s | 7.5x |
| 2^22 samples | 0.60s | 0.05s | 12x |
| 2^24 samples | 2.40s | 0.15s | 16x |

Run benchmark:
```python
from gw_141hz_tools.spectral_analysis_optimized import benchmark_performance
benchmark_performance(data_size=2**20, n_trials=5)
```

## Compressed Storage

### Supported Formats

1. **HDF5** - Standard format with gzip/lzf compression
2. **Zarr** - Chunked arrays for large datasets
3. **Parquet** - Structured results storage
4. **NumPy compressed** - Simple .npz format

### Compression Comparison

| Method | Ratio | Write Speed | Read Speed | Use Case |
|--------|-------|-------------|------------|----------|
| gzip (level 5) | 2-3x | Fast | Fast | General purpose |
| lzf | 1.5-2x | Very Fast | Very Fast | Real-time processing |
| None | 1x | Fastest | Fastest | High-performance I/O |

### Usage Examples

```python
from gw_141hz_tools.compressed_io import DataManager

dm = DataManager(default_compression='gzip', default_compression_level=5)

# Save time series with compression
dm.save_timeseries(
    data,
    'event.h5',
    sample_rate=4096,
    gps_start=1126259462.0,
    metadata={'detector': 'H1', 'event': 'GW150914'},
    compression='gzip',
    compression_level=5
)

# Load compressed data
data, metadata = dm.load_timeseries('event.h5')

# Zarr format for very large datasets
dm.save_to_zarr(data, 'event.zarr', chunks=(2**16,))
data = dm.load_from_zarr('event.zarr')

# Compare compression methods
results = dm.estimate_compression_savings(data)
```

### Typical Compression Ratios

For GW strain data:
- Raw data: ~100 MB/event (32s at 4096 Hz)
- gzip level 5: ~40 MB (2.5x compression)
- lzf: ~60 MB (1.7x compression)

## HPC and Cloud Support

### Slurm Job Generation

Generate job scripts for HPC clusters:

```python
from gw_141hz_tools.hpc_support import SlurmJobGenerator

# Create job generator
slurm = SlurmJobGenerator(
    partition='normal',
    time_limit='08:00:00',
    cpus_per_task=16,
    memory='32G'
)

# Single event job
slurm.generate_job_script(
    job_name='gw150914_141hz',
    script_path='jobs/gw150914.sh',
    output_dir='results/hpc',
    python_script='scripts/analizar_ringdown.py',
    arguments='--event GW150914',
    conda_env='gw_analysis'
)

# Array job for multiple events
events = ['GW150914', 'GW151226', 'GW170814']
slurm.generate_array_job(
    job_name='gwtc1_analysis',
    script_path='jobs/gwtc1_array.sh',
    output_dir='results/hpc',
    python_script='scripts/example_optimized_analysis.py',
    events=events
)
```

Submit to Slurm:
```bash
sbatch jobs/gwtc1_array.sh
```

### GPU Jobs

```python
slurm_gpu = SlurmJobGenerator(
    partition='gpu',
    time_limit='04:00:00',
    cpus_per_task=8,
    memory='64G',
    gpu=True
)

slurm_gpu.generate_job_script(
    job_name='gpu_analysis',
    script_path='jobs/gpu_analysis.sh',
    output_dir='results/gpu',
    python_script='scripts/example_optimized_analysis.py',
    arguments='--use-gpu --catalog GWTC-3',
    modules=['cuda/12.0', 'python/3.11']
)
```

### Dask Distributed Computing

For cloud or multi-node processing:

```python
from gw_141hz_tools.hpc_support import HPCManager

# Local cluster
manager = HPCManager(use_dask=True, n_workers=8)

# Or connect to existing cluster
# Set environment: DASK_SCHEDULER_ADDRESS=tcp://scheduler:8786
manager = HPCManager(use_dask=True)

# Process multiple events in parallel
def analyze_event(event_name):
    # Your analysis code
    return results

events = ['GW150914', 'GW151226', 'GW170814']
results = manager.process_event_batch(events, analyze_event)

# Process entire catalog
results = manager.process_gwtc_catalog('GWTC-3', analysis_func=analyze_event)

# Cleanup
manager.shutdown()
```

## GWTC-3 and GWTC-4 Support

### Catalog Processing

```bash
# Generate HPC scripts for GWTC-3
python scripts/example_optimized_analysis.py \
  --generate-hpc-scripts \
  --catalog GWTC-3

# This creates:
# - hpc_jobs/job_gwtc-3_cpu.sh (array job for all events)
# - hpc_jobs/job_gwtc-3_single_example.sh (single event example)
```

### Event Catalogs

Supported catalogs:
- **GWTC-1**: 11 events (O1 + O2)
- **GWTC-2**: 39 events (O3a)
- **GWTC-3**: 32 events (O3b subset)
- **GWTC-4**: Placeholder (awaiting release)

### Example: Process GWTC-3

```python
from gw_141hz_tools.hpc_support import HPCManager

manager = HPCManager(use_dask=True, n_workers=32)

def analyze_141hz(event_name):
    # Download data, analyze 141.7 Hz component
    from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
    analyzer = SpectralAnalyzer(use_gpu=True)
    # ... analysis code ...
    return result

results = manager.process_gwtc_catalog('GWTC-3', analysis_func=analyze_141hz)

print(f"Processed {results['n_events']} events")
print(f"Detection rate: {results['summary']['detection_rate']}")
```

## Best Practices

### Memory Management

For large datasets:
```python
# Use chunked processing
analyzer = SpectralAnalyzer(chunk_size=2**20)

# Use compressed storage
dm = DataManager(default_compression='gzip')
dm.save_timeseries(data, 'event.h5', chunks=True)
```

### Parallel Processing

```python
# CPU parallelization
analyzer = SpectralAnalyzer(use_gpu=False, n_jobs=-1)  # Use all cores

# Process multiple events
from joblib import Parallel, delayed

results = Parallel(n_jobs=8)(
    delayed(analyze_event)(event) for event in events
)
```

### HPC Optimization

**CPU Jobs:**
- Request 16-32 CPUs per job
- Use 32-64 GB memory
- Time limit: 4-8 hours per event

**GPU Jobs:**
- 1 GPU + 8 CPUs
- 64 GB memory
- Time limit: 1-2 hours per event

**Array Jobs:**
- Use for 10+ events
- Automatic parallelization across nodes
- Easier job management

## Troubleshooting

### GPU Issues

```python
# Check if GPU available
import cupy as cp
print(f"GPU available: {cp.cuda.is_available()}")
print(f"Device: {cp.cuda.Device().name}")

# Force CPU fallback
analyzer = SpectralAnalyzer(use_gpu=False)
```

### Memory Errors

```python
# Reduce chunk size
analyzer = SpectralAnalyzer(chunk_size=2**18)  # Smaller chunks

# Use compression to save memory
dm.save_timeseries(data, 'event.h5', compression='gzip')
```

### Slurm Errors

Check job status:
```bash
squeue -u $USER
sacct -j JOBID
cat results/hpc_output/*.err
```

## Performance Tips

1. **Use GPU for large datasets** (>2^20 samples)
2. **Enable compression** for storage (2-3x savings)
3. **Parallelize event processing** with joblib or Dask
4. **Use array jobs** for HPC batch processing
5. **Cache downloaded data** to avoid repeated downloads

## References

- [CuPy Documentation](https://docs.cupy.dev/)
- [Dask Documentation](https://docs.dask.org/)
- [HDF5 Compression](https://docs.h5py.org/en/stable/high/dataset.html#dataset-compression)
- [Slurm Documentation](https://slurm.schedmd.com/)
