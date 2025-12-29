"""
GW 141Hz Analysis Tools
=======================

Optimized tools for gravitational wave analysis with focus on 141.7 Hz detection.

Modules:
- spectral_analysis_optimized: GPU-accelerated spectral analysis
- compressed_io: Efficient data storage with compression
- hpc_support: HPC and cloud computing utilities
- antenna: Antenna pattern calculations
- noise: Noise modeling
- offsource: Off-source analysis
"""

__version__ = "1.0.0"

# Optional imports with graceful fallback
try:
    from .spectral_analysis_optimized import SpectralAnalyzer, benchmark_performance
except ImportError:
    SpectralAnalyzer = None
    benchmark_performance = None

try:
    from .compressed_io import DataManager, benchmark_compression
except ImportError:
    DataManager = None
    benchmark_compression = None

try:
    from .hpc_support import HPCManager, SlurmJobGenerator
except ImportError:
    HPCManager = None
    SlurmJobGenerator = None

__all__ = [
    'SpectralAnalyzer',
    'DataManager',
    'HPCManager',
    'SlurmJobGenerator',
    'benchmark_performance',
    'benchmark_compression',
]
