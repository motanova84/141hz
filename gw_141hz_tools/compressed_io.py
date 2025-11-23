#!/usr/bin/env python3
"""
Compressed Data I/O Module
===========================

Efficient data storage and loading with compression support for large-scale
gravitational wave analysis.

Supported formats:
- HDF5 with gzip/lzf compression
- Zarr for chunked array storage
- Parquet for structured results
- NumPy compressed (.npz)

Usage:
    from gw_141hz_tools.compressed_io import DataManager
    
    dm = DataManager()
    dm.save_timeseries(data, 'data.h5', compression='gzip', compression_level=5)
    data = dm.load_timeseries('data.h5')
"""

import numpy as np
import h5py
import os
from typing import Optional, Dict, Any, Union
import warnings
import json

# Try to import optional compression libraries
try:
    import zarr
    ZARR_AVAILABLE = True
except ImportError:
    ZARR_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class DataManager:
    """
    Manager for efficient data storage with compression.
    
    Parameters
    ----------
    default_compression : str, optional
        Default compression algorithm ('gzip', 'lzf', None)
    default_compression_level : int, optional
        Compression level for gzip (0-9, default: 5)
    """
    
    def __init__(
        self,
        default_compression: str = 'gzip',
        default_compression_level: int = 5
    ):
        self.default_compression = default_compression
        self.default_compression_level = default_compression_level
        
        print(f"Data Manager initialized:")
        print(f"  - HDF5: ✓ (compression: {default_compression})")
        print(f"  - Zarr: {'✓' if ZARR_AVAILABLE else '✗'}")
        print(f"  - Parquet: {'✓' if PANDAS_AVAILABLE else '✗'}")
    
    def save_timeseries(
        self,
        data: np.ndarray,
        filepath: str,
        sample_rate: float,
        gps_start: float,
        metadata: Optional[Dict[str, Any]] = None,
        compression: Optional[str] = None,
        compression_level: Optional[int] = None,
        chunks: bool = True
    ) -> None:
        """
        Save time series data to HDF5 with compression.
        
        Parameters
        ----------
        data : ndarray
            Time series data
        filepath : str
            Output file path
        sample_rate : float
            Sample rate in Hz
        gps_start : float
            GPS start time
        metadata : dict, optional
            Additional metadata to store
        compression : str, optional
            Compression algorithm ('gzip', 'lzf', None)
        compression_level : int, optional
            Compression level for gzip (0-9)
        chunks : bool, optional
            Use chunked storage (default: True)
        """
        if compression is None:
            compression = self.default_compression
        if compression_level is None:
            compression_level = self.default_compression_level
        
        # Determine chunk size
        chunk_size = min(2**16, len(data)) if chunks else None
        
        # Prepare compression options
        compression_opts = None
        if compression == 'gzip':
            compression_opts = compression_level
        
        with h5py.File(filepath, 'w') as f:
            # Store strain data
            dset = f.create_dataset(
                'strain/Strain',
                data=data,
                compression=compression,
                compression_opts=compression_opts,
                chunks=(chunk_size,) if chunks else None
            )
            
            # Store metadata
            meta_group = f.create_group('meta')
            meta_group.create_dataset('GPSstart', data=gps_start)
            meta_group.create_dataset('SampleRate', data=sample_rate)
            meta_group.create_dataset('Duration', data=len(data) / sample_rate)
            
            if metadata:
                for key, value in metadata.items():
                    if isinstance(value, (int, float, str)):
                        meta_group.create_dataset(key, data=value)
                    elif isinstance(value, dict):
                        # Store dict as JSON string
                        meta_group.create_dataset(
                            key, 
                            data=json.dumps(value),
                            dtype=h5py.string_dtype()
                        )
        
        # Report compression ratio
        original_size = data.nbytes
        compressed_size = os.path.getsize(filepath)
        ratio = original_size / compressed_size
        
        print(f"Saved {filepath}:")
        print(f"  Original: {original_size / 1e6:.2f} MB")
        print(f"  Compressed: {compressed_size / 1e6:.2f} MB")
        print(f"  Ratio: {ratio:.2f}x")
    
    def load_timeseries(
        self,
        filepath: str,
        load_metadata: bool = True
    ) -> Union[np.ndarray, tuple]:
        """
        Load time series data from HDF5.
        
        Parameters
        ----------
        filepath : str
            Input file path
        load_metadata : bool, optional
            Return metadata along with data (default: True)
            
        Returns
        -------
        data : ndarray or tuple
            If load_metadata=False, returns data array
            If load_metadata=True, returns (data, metadata) tuple
        """
        with h5py.File(filepath, 'r') as f:
            data = f['strain/Strain'][:]
            
            if load_metadata:
                meta = {}
                meta_group = f['meta']
                for key in meta_group.keys():
                    value = meta_group[key][()]
                    # Try to parse JSON strings
                    if isinstance(value, bytes):
                        try:
                            value = json.loads(value.decode())
                        except (json.JSONDecodeError, ValueError):
                            value = value.decode()
                    meta[key] = value
                
                return data, meta
            else:
                return data
    
    def save_to_zarr(
        self,
        data: np.ndarray,
        filepath: str,
        chunks: Optional[tuple] = None,
        compression: str = 'blosc',
        compression_level: int = 5
    ) -> None:
        """
        Save data to Zarr format for chunked array storage.
        
        Parameters
        ----------
        data : ndarray
            Data to save
        filepath : str
            Output directory path
        chunks : tuple, optional
            Chunk shape (default: auto)
        compression : str, optional
            Compression algorithm (default: 'blosc')
        compression_level : int, optional
            Compression level (default: 5)
        """
        if not ZARR_AVAILABLE:
            raise ImportError(
                "Zarr not available. Install with: pip install zarr"
            )
        
        # Determine chunks automatically if not specified
        if chunks is None:
            chunks = min(2**16, len(data))
        
        # Create Zarr array
        z = zarr.open(
            filepath,
            mode='w',
            shape=data.shape,
            dtype=data.dtype,
            chunks=chunks,
            compressor=zarr.Blosc(
                cname='zstd',
                clevel=compression_level,
                shuffle=zarr.Blosc.SHUFFLE
            )
        )
        
        # Write data
        z[:] = data
        
        # Report compression
        original_size = data.nbytes
        compressed_size = sum(
            os.path.getsize(os.path.join(filepath, f))
            for f in os.listdir(filepath)
            if os.path.isfile(os.path.join(filepath, f))
        )
        ratio = original_size / compressed_size
        
        print(f"Saved Zarr to {filepath}:")
        print(f"  Original: {original_size / 1e6:.2f} MB")
        print(f"  Compressed: {compressed_size / 1e6:.2f} MB")
        print(f"  Ratio: {ratio:.2f}x")
    
    def load_from_zarr(self, filepath: str) -> np.ndarray:
        """
        Load data from Zarr format.
        
        Parameters
        ----------
        filepath : str
            Input directory path
            
        Returns
        -------
        data : ndarray
            Loaded data
        """
        if not ZARR_AVAILABLE:
            raise ImportError(
                "Zarr not available. Install with: pip install zarr"
            )
        
        z = zarr.open(filepath, mode='r')
        return z[:]
    
    def save_results_parquet(
        self,
        results: Dict[str, Any],
        filepath: str,
        compression: str = 'snappy'
    ) -> None:
        """
        Save analysis results to Parquet format.
        
        Parameters
        ----------
        results : dict
            Results dictionary (must be flat structure)
        filepath : str
            Output file path
        compression : str, optional
            Compression algorithm ('snappy', 'gzip', 'brotli')
        """
        if not PANDAS_AVAILABLE:
            raise ImportError(
                "Pandas not available. Install with: pip install pandas pyarrow"
            )
        
        # Convert to DataFrame
        df = pd.DataFrame([results])
        
        # Save to Parquet
        df.to_parquet(filepath, compression=compression, index=False)
        
        # Report size
        size = os.path.getsize(filepath)
        print(f"Saved results to {filepath} ({size / 1e3:.2f} KB)")
    
    def load_results_parquet(self, filepath: str) -> Dict[str, Any]:
        """
        Load analysis results from Parquet format.
        
        Parameters
        ----------
        filepath : str
            Input file path
            
        Returns
        -------
        results : dict
            Results dictionary
        """
        if not PANDAS_AVAILABLE:
            raise ImportError(
                "Pandas not available. Install with: pip install pandas pyarrow"
            )
        
        df = pd.read_parquet(filepath)
        return df.iloc[0].to_dict()
    
    def save_compressed_numpy(
        self,
        filepath: str,
        **arrays: np.ndarray
    ) -> None:
        """
        Save multiple arrays to compressed NumPy format.
        
        Parameters
        ----------
        filepath : str
            Output file path
        **arrays : dict of ndarray
            Named arrays to save
        """
        np.savez_compressed(filepath, **arrays)
        
        # Report size
        size = os.path.getsize(filepath)
        total_size = sum(arr.nbytes for arr in arrays.values())
        ratio = total_size / size
        
        print(f"Saved compressed NumPy to {filepath}:")
        print(f"  Original: {total_size / 1e6:.2f} MB")
        print(f"  Compressed: {size / 1e6:.2f} MB")
        print(f"  Ratio: {ratio:.2f}x")
    
    def load_compressed_numpy(self, filepath: str) -> Dict[str, np.ndarray]:
        """
        Load arrays from compressed NumPy format.
        
        Parameters
        ----------
        filepath : str
            Input file path
            
        Returns
        -------
        arrays : dict of ndarray
            Dictionary of loaded arrays
        """
        data = np.load(filepath)
        return {key: data[key] for key in data.files}
    
    def estimate_compression_savings(
        self,
        data: np.ndarray,
        compressions: list = ['gzip', 'lzf', None]
    ) -> Dict[str, dict]:
        """
        Estimate compression savings for different algorithms.
        
        Parameters
        ----------
        data : ndarray
            Sample data
        compressions : list, optional
            Compression algorithms to test
            
        Returns
        -------
        results : dict
            Compression statistics for each algorithm
        """
        import tempfile
        import time
        
        results = {}
        original_size = data.nbytes
        
        print(f"\nTesting compression on {original_size / 1e6:.2f} MB data...")
        print("="*50)
        
        for compression in compressions:
            with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                # Time the write
                start = time.time()
                with h5py.File(tmp_path, 'w') as f:
                    f.create_dataset(
                        'data',
                        data=data,
                        compression=compression,
                        compression_opts=5 if compression == 'gzip' else None
                    )
                write_time = time.time() - start
                
                # Get compressed size
                compressed_size = os.path.getsize(tmp_path)
                ratio = original_size / compressed_size
                
                # Time the read
                start = time.time()
                with h5py.File(tmp_path, 'r') as f:
                    _ = f['data'][:]
                read_time = time.time() - start
                
                results[compression or 'none'] = {
                    'compressed_size_mb': compressed_size / 1e6,
                    'compression_ratio': ratio,
                    'write_time_s': write_time,
                    'read_time_s': read_time
                }
                
                print(f"{compression or 'none':8s}: "
                      f"{compressed_size / 1e6:6.2f} MB  "
                      f"{ratio:5.2f}x  "
                      f"W:{write_time:5.3f}s  "
                      f"R:{read_time:5.3f}s")
                
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        
        return results


def benchmark_compression(data_size: int = 2**20) -> None:
    """
    Benchmark different compression methods.
    
    Parameters
    ----------
    data_size : int
        Size of test data
    """
    print(f"\n{'='*60}")
    print(f"Compression Benchmark")
    print(f"{'='*60}")
    
    # Generate realistic GW data (mostly noise with some signal)
    sample_rate = 4096.0
    t = np.arange(data_size) / sample_rate
    
    # Simulate GW strain data
    noise = np.random.randn(data_size) * 1e-21
    signal = 1e-20 * np.sin(2 * np.pi * 141.7 * t) * np.exp(-t / 0.1)
    data = noise + signal
    
    dm = DataManager()
    results = dm.estimate_compression_savings(
        data,
        compressions=['gzip', 'lzf', None]
    )
    
    print(f"\n{'='*60}")
    print("Recommendation:")
    
    # Find best compression based on ratio and time
    best = max(
        results.items(),
        key=lambda x: x[1]['compression_ratio'] / (x[1]['write_time_s'] + 0.1)
    )
    print(f"  Best overall: {best[0]} "
          f"({best[1]['compression_ratio']:.2f}x in "
          f"{best[1]['write_time_s']:.3f}s)")


if __name__ == "__main__":
    # Run benchmark
    benchmark_compression()
