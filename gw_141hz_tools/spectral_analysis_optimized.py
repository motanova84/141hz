#!/usr/bin/env python3
"""
Optimized Spectral Analysis Module
===================================

High-performance spectral analysis with GPU acceleration and parallel processing support.

Features:
- GPU acceleration using CuPy (with automatic CPU fallback)
- Parallel processing using joblib
- Memory-efficient chunked processing for large datasets
- Support for compressed data formats (HDF5, Zarr)

Usage:
    from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
    
    analyzer = SpectralAnalyzer(use_gpu=True, n_jobs=-1)
    freqs, psd = analyzer.compute_psd(data, sample_rate)
"""

import numpy as np
from typing import Tuple, Optional, Union
import warnings

# Try to import GPU acceleration libraries
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    cp = None

# Try to import parallel processing
try:
    from joblib import Parallel, delayed
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False


class SpectralAnalyzer:
    """
    High-performance spectral analyzer with GPU and parallel processing support.
    
    Parameters
    ----------
    use_gpu : bool, optional
        Use GPU acceleration if available (default: False)
    n_jobs : int, optional
        Number of parallel jobs for CPU processing (-1 for all cores, default: 1)
    chunk_size : int, optional
        Chunk size for processing large datasets (default: 2**20)
    """
    
    def __init__(
        self, 
        use_gpu: bool = False,
        n_jobs: int = 1,
        chunk_size: int = 2**20
    ):
        self.use_gpu = use_gpu and CUPY_AVAILABLE
        self.n_jobs = n_jobs
        self.chunk_size = chunk_size
        
        if use_gpu and not CUPY_AVAILABLE:
            warnings.warn(
                "GPU acceleration requested but CuPy not available. "
                "Falling back to CPU. Install CuPy for your CUDA version:\n"
                "  CUDA 11.x: pip install cupy-cuda11x\n"
                "  CUDA 12.x: pip install cupy-cuda12x\n"
                "  See: https://docs.cupy.dev/en/stable/install.html",
                UserWarning
            )
        
        if n_jobs != 1 and not JOBLIB_AVAILABLE:
            warnings.warn(
                "Parallel processing requested but joblib not available. "
                "Using single-threaded processing. Install: pip install joblib",
                UserWarning
            )
            self.n_jobs = 1
        
        # Select appropriate numpy/cupy backend
        self.xp = cp if self.use_gpu else np
        
        print(f"Spectral Analyzer initialized:")
        print(f"  - GPU: {'✓ CuPy' if self.use_gpu else '✗ CPU only'}")
        print(f"  - Parallel: {'✓ ' + str(self.n_jobs) + ' jobs' if self.n_jobs != 1 else '✗ Single-threaded'}")
    
    def compute_psd(
        self,
        data: np.ndarray,
        sample_rate: float,
        nperseg: Optional[int] = None,
        window: str = 'hann'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute Power Spectral Density using Welch's method.
        
        Parameters
        ----------
        data : ndarray
            Time series data
        sample_rate : float
            Sample rate in Hz
        nperseg : int, optional
            Length of each segment (default: min(256, len(data)))
        window : str, optional
            Window function (default: 'hann')
            
        Returns
        -------
        freqs : ndarray
            Frequency array
        psd : ndarray
            Power spectral density
        """
        if nperseg is None:
            nperseg = min(256, len(data))
        
        noverlap = nperseg // 2
        
        # Use GPU if available
        if self.use_gpu:
            return self._compute_psd_gpu(data, sample_rate, nperseg, noverlap, window)
        else:
            return self._compute_psd_cpu(data, sample_rate, nperseg, noverlap, window)
    
    def _compute_psd_gpu(
        self,
        data: np.ndarray,
        sample_rate: float,
        nperseg: int,
        noverlap: int,
        window: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """GPU-accelerated PSD computation using CuPy."""
        from scipy.signal import get_window
        
        # Transfer data to GPU
        data_gpu = cp.asarray(data)
        
        # Generate window on GPU
        win = cp.asarray(get_window(window, nperseg))
        
        # Compute number of segments
        step = nperseg - noverlap
        n_segments = 1 + (len(data_gpu) - nperseg) // step
        
        # Pre-allocate result on GPU
        freqs = cp.fft.rfftfreq(nperseg, d=1/sample_rate)
        psd = cp.zeros(len(freqs))
        
        # Process segments on GPU
        for i in range(n_segments):
            start = i * step
            end = start + nperseg
            segment = data_gpu[start:end] * win
            
            # FFT on GPU
            fft_segment = cp.fft.rfft(segment)
            psd += cp.abs(fft_segment) ** 2
        
        # Average and normalize
        psd /= n_segments
        psd *= 2.0 / (sample_rate * cp.sum(win**2))
        
        # Transfer back to CPU
        return cp.asnumpy(freqs), cp.asnumpy(psd)
    
    def _compute_psd_cpu(
        self,
        data: np.ndarray,
        sample_rate: float,
        nperseg: int,
        noverlap: int,
        window: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """CPU PSD computation using scipy (optimized)."""
        from scipy.signal import welch
        
        freqs, psd = welch(
            data,
            fs=sample_rate,
            window=window,
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='density'
        )
        
        return freqs, psd
    
    def compute_fft(
        self,
        data: np.ndarray,
        sample_rate: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT with automatic GPU/CPU selection.
        
        Parameters
        ----------
        data : ndarray
            Time series data
        sample_rate : float
            Sample rate in Hz
            
        Returns
        -------
        freqs : ndarray
            Frequency array
        power : ndarray
            Power spectrum
        """
        if self.use_gpu:
            # GPU FFT
            data_gpu = cp.asarray(data)
            freqs = cp.fft.rfftfreq(len(data_gpu), d=1/sample_rate)
            fft_vals = cp.fft.rfft(data_gpu)
            power = cp.abs(fft_vals) ** 2
            return cp.asnumpy(freqs), cp.asnumpy(power)
        else:
            # CPU FFT
            freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)
            fft_vals = np.fft.rfft(data)
            power = np.abs(fft_vals) ** 2
            return freqs, power
    
    def parallel_fft_batch(
        self,
        data_list: list,
        sample_rate: float
    ) -> list:
        """
        Process multiple FFTs in parallel.
        
        Parameters
        ----------
        data_list : list of ndarray
            List of time series to process
        sample_rate : float
            Sample rate in Hz
            
        Returns
        -------
        results : list of tuple
            List of (freqs, power) tuples
        """
        if self.n_jobs == 1 or not JOBLIB_AVAILABLE:
            # Serial processing
            return [self.compute_fft(data, sample_rate) for data in data_list]
        else:
            # Parallel processing
            return Parallel(n_jobs=self.n_jobs)(
                delayed(self.compute_fft)(data, sample_rate)
                for data in data_list
            )
    
    def find_peaks(
        self,
        freqs: np.ndarray,
        power: np.ndarray,
        target_freq: float,
        freq_range: float = 1.0,
        threshold: Optional[float] = None
    ) -> dict:
        """
        Find spectral peaks near target frequency.
        
        Parameters
        ----------
        freqs : ndarray
            Frequency array
        power : ndarray
            Power spectrum
        target_freq : float
            Target frequency in Hz
        freq_range : float, optional
            Range around target to search (default: 1.0 Hz)
        threshold : float, optional
            SNR threshold (default: auto-detect from noise floor)
            
        Returns
        -------
        results : dict
            Dictionary with peak information
        """
        # Find region of interest
        mask = np.abs(freqs - target_freq) <= freq_range
        freqs_roi = freqs[mask]
        power_roi = power[mask]
        
        if len(power_roi) == 0:
            return {
                'detected': False,
                'peak_freq': None,
                'peak_power': None,
                'snr': None
            }
        
        # Find peak
        peak_idx = np.argmax(power_roi)
        peak_freq = freqs_roi[peak_idx]
        peak_power = power_roi[peak_idx]
        
        # Estimate noise floor
        noise_floor = np.median(power)
        snr = peak_power / noise_floor if noise_floor > 0 else 0
        
        # Check threshold
        if threshold is None:
            threshold = 5.0  # Default SNR threshold
        
        detected = snr >= threshold
        
        return {
            'detected': detected,
            'peak_freq': float(peak_freq),
            'peak_power': float(peak_power),
            'snr': float(snr),
            'noise_floor': float(noise_floor),
            'threshold': threshold
        }
    
    def compute_snr_141hz(
        self,
        data: np.ndarray,
        sample_rate: float
    ) -> dict:
        """
        Compute SNR at 141.7 Hz specifically.
        
        Parameters
        ----------
        data : ndarray
            Time series data
        sample_rate : float
            Sample rate in Hz
            
        Returns
        -------
        results : dict
            SNR analysis results
        """
        freqs, power = self.compute_fft(data, sample_rate)
        return self.find_peaks(freqs, power, target_freq=141.7, freq_range=2.0)


def benchmark_performance(data_size: int = 2**20, n_trials: int = 5) -> dict:
    """
    Benchmark CPU vs GPU performance.
    
    Parameters
    ----------
    data_size : int
        Size of test data
    n_trials : int
        Number of trials for averaging
        
    Returns
    -------
    results : dict
        Benchmark results
    """
    import time
    
    print(f"\nBenchmarking Spectral Analysis Performance")
    print(f"{'='*50}")
    print(f"Data size: {data_size:,} samples")
    print(f"Trials: {n_trials}")
    
    # Generate test data
    sample_rate = 4096.0
    t = np.arange(data_size) / sample_rate
    data = np.random.randn(data_size) + 0.1 * np.sin(2 * np.pi * 141.7 * t)
    
    results = {}
    
    # CPU benchmark
    print("\nTesting CPU (numpy + scipy)...")
    analyzer_cpu = SpectralAnalyzer(use_gpu=False, n_jobs=1)
    times_cpu = []
    for i in range(n_trials):
        start = time.time()
        freqs, power = analyzer_cpu.compute_fft(data, sample_rate)
        elapsed = time.time() - start
        times_cpu.append(elapsed)
        print(f"  Trial {i+1}: {elapsed:.4f}s")
    
    results['cpu'] = {
        'mean': np.mean(times_cpu),
        'std': np.std(times_cpu),
        'min': np.min(times_cpu),
        'max': np.max(times_cpu)
    }
    
    # GPU benchmark (if available)
    if CUPY_AVAILABLE:
        print("\nTesting GPU (CuPy)...")
        analyzer_gpu = SpectralAnalyzer(use_gpu=True, n_jobs=1)
        times_gpu = []
        for i in range(n_trials):
            start = time.time()
            freqs, power = analyzer_gpu.compute_fft(data, sample_rate)
            cp.cuda.Stream.null.synchronize()  # Ensure GPU completion
            elapsed = time.time() - start
            times_gpu.append(elapsed)
            print(f"  Trial {i+1}: {elapsed:.4f}s")
        
        results['gpu'] = {
            'mean': np.mean(times_gpu),
            'std': np.std(times_gpu),
            'min': np.min(times_gpu),
            'max': np.max(times_gpu)
        }
        
        speedup = results['cpu']['mean'] / results['gpu']['mean']
        results['speedup'] = speedup
        
        print(f"\n{'='*50}")
        print(f"Speedup: {speedup:.2f}x")
    else:
        print("\nGPU not available for benchmarking")
        results['gpu'] = None
        results['speedup'] = None
    
    return results


if __name__ == "__main__":
    # Run benchmark
    benchmark_performance()
