#!/usr/bin/env python3
"""
Test script for computational optimization modules.

Tests:
- Spectral analysis with CPU/GPU
- Compressed data I/O
- HPC job generation
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_spectral_analyzer():
    """Test SpectralAnalyzer class."""
    print("\n" + "="*60)
    print("Testing Spectral Analyzer")
    print("="*60)
    
    try:
        from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
        
        # Generate test data
        sample_rate = 4096.0
        duration = 1.0
        n_samples = int(sample_rate * duration)
        t = np.arange(n_samples) / sample_rate
        
        # Simulated GW signal with 141.7 Hz component
        noise = np.random.randn(n_samples) * 1e-21
        signal = 5e-21 * np.sin(2 * np.pi * 141.7 * t)
        data = noise + signal
        
        # Test CPU analyzer
        print("\n1. CPU Analysis")
        analyzer_cpu = SpectralAnalyzer(use_gpu=False, n_jobs=1)
        freqs, power = analyzer_cpu.compute_fft(data, sample_rate)
        print(f"   ✓ FFT computed: {len(freqs)} frequency bins")
        
        # Test peak finding
        result = analyzer_cpu.find_peaks(freqs, power, target_freq=141.7)
        print(f"   ✓ Peak detection: {result['detected']}")
        print(f"     - Peak freq: {result['peak_freq']:.2f} Hz")
        print(f"     - SNR: {result['snr']:.2f}")
        
        # Test PSD computation
        freqs_psd, psd = analyzer_cpu.compute_psd(data, sample_rate, nperseg=256)
        print(f"   ✓ PSD computed: {len(freqs_psd)} frequency bins")
        
        # Test GPU analyzer (if available)
        print("\n2. GPU Analysis (if available)")
        analyzer_gpu = SpectralAnalyzer(use_gpu=True, n_jobs=1)
        if analyzer_gpu.use_gpu:
            freqs_gpu, power_gpu = analyzer_gpu.compute_fft(data, sample_rate)
            print(f"   ✓ GPU FFT computed: {len(freqs_gpu)} frequency bins")
        else:
            print("   ℹ GPU not available (expected)")
        
        print("\n✅ Spectral Analyzer tests PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Spectral Analyzer tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_manager():
    """Test DataManager class."""
    print("\n" + "="*60)
    print("Testing Data Manager")
    print("="*60)
    
    try:
        from gw_141hz_tools.compressed_io import DataManager
        import tempfile
        
        dm = DataManager(default_compression='gzip', default_compression_level=5)
        
        # Generate test data
        sample_rate = 4096.0
        duration = 1.0
        n_samples = int(sample_rate * duration)
        data = np.random.randn(n_samples) * 1e-21
        gps_start = 1126259462.0
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test HDF5 save/load
            print("\n1. HDF5 Compression")
            h5_path = os.path.join(tmpdir, 'test_data.h5')
            dm.save_timeseries(
                data, h5_path, sample_rate, gps_start,
                metadata={'detector': 'H1', 'event': 'TEST'}
            )
            print(f"   ✓ Saved to HDF5")
            
            loaded_data, metadata = dm.load_timeseries(h5_path)
            assert len(loaded_data) == len(data), "Data length mismatch"
            assert metadata['detector'] == 'H1', "Metadata mismatch"
            print(f"   ✓ Loaded from HDF5")
            print(f"   ✓ Metadata preserved")
            
            # Test compressed NumPy
            print("\n2. Compressed NumPy")
            npz_path = os.path.join(tmpdir, 'test_data.npz')
            dm.save_compressed_numpy(
                npz_path,
                data=data,
                freqs=np.arange(100),
                power=np.random.rand(100)
            )
            print(f"   ✓ Saved compressed NumPy")
            
            loaded_arrays = dm.load_compressed_numpy(npz_path)
            assert 'data' in loaded_arrays, "Missing data array"
            assert 'freqs' in loaded_arrays, "Missing freqs array"
            print(f"   ✓ Loaded compressed NumPy")
            
            # Test compression comparison
            print("\n3. Compression Comparison")
            results = dm.estimate_compression_savings(
                data[:10000],  # Use smaller sample for speed
                compressions=['gzip', 'lzf', None]
            )
            assert 'gzip' in results, "Missing gzip results"
            print(f"   ✓ Compression comparison completed")
        
        print("\n✅ Data Manager tests PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Data Manager tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hpc_manager():
    """Test HPCManager and SlurmJobGenerator classes."""
    print("\n" + "="*60)
    print("Testing HPC Manager")
    print("="*60)
    
    try:
        from gw_141hz_tools.hpc_support import HPCManager, SlurmJobGenerator
        import tempfile
        
        # Test HPCManager
        print("\n1. HPC Manager Initialization")
        manager = HPCManager(use_dask=False, n_workers=2)
        print(f"   ✓ Manager initialized")
        
        # Test catalog event listing
        print("\n2. Catalog Event Listing")
        events_gwtc1 = manager._get_catalog_events('GWTC-1')
        assert len(events_gwtc1) == 11, f"Expected 11 GWTC-1 events, got {len(events_gwtc1)}"
        print(f"   ✓ GWTC-1: {len(events_gwtc1)} events")
        
        events_gwtc3 = manager._get_catalog_events('GWTC-3')
        print(f"   ✓ GWTC-3: {len(events_gwtc3)} events")
        
        # Test Slurm job generation
        print("\n3. Slurm Job Generation")
        slurm = SlurmJobGenerator(
            partition='normal',
            time_limit='01:00:00',
            cpus_per_task=4
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, 'test_job.sh')
            slurm.generate_job_script(
                job_name='test_analysis',
                script_path=script_path,
                output_dir=tmpdir,
                python_script='test.py',
                arguments='--test'
            )
            
            assert os.path.exists(script_path), "Job script not created"
            print(f"   ✓ Job script created")
            
            # Verify script content
            with open(script_path, 'r') as f:
                content = f.read()
                assert '#SBATCH --job-name=test_analysis' in content
                assert '#SBATCH --cpus-per-task=4' in content
                print(f"   ✓ Job script validated")
            
            # Test array job generation
            array_script = os.path.join(tmpdir, 'test_array.sh')
            slurm.generate_array_job(
                job_name='test_array',
                script_path=array_script,
                output_dir=tmpdir,
                python_script='test.py',
                events=['GW150914', 'GW151226']
            )
            
            assert os.path.exists(array_script), "Array job script not created"
            print(f"   ✓ Array job script created")
        
        # Cleanup
        manager.shutdown()
        
        print("\n✅ HPC Manager tests PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ HPC Manager tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Integration test combining all modules."""
    print("\n" + "="*60)
    print("Testing Integration")
    print("="*60)
    
    try:
        from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
        from gw_141hz_tools.compressed_io import DataManager
        import tempfile
        
        # Generate test data
        sample_rate = 4096.0
        duration = 2.0
        n_samples = int(sample_rate * duration)
        t = np.arange(n_samples) / sample_rate
        
        noise = np.random.randn(n_samples) * 1e-21
        signal = 5e-21 * np.sin(2 * np.pi * 141.7 * t)
        data = noise + signal
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save data with compression
            print("\n1. Save compressed data")
            dm = DataManager()
            data_path = os.path.join(tmpdir, 'test_integrated.h5')
            dm.save_timeseries(data, data_path, sample_rate, 1126259462.0)
            print("   ✓ Data saved")
            
            # Load and analyze
            print("\n2. Load and analyze")
            loaded_data, metadata = dm.load_timeseries(data_path)
            print("   ✓ Data loaded")
            
            analyzer = SpectralAnalyzer(use_gpu=False)
            result = analyzer.compute_snr_141hz(loaded_data, sample_rate)
            
            print(f"   ✓ Analysis completed")
            print(f"     - Detected: {result['detected']}")
            print(f"     - Peak: {result['peak_freq']:.2f} Hz")
            print(f"     - SNR: {result['snr']:.2f}")
            
            # Save results
            print("\n3. Save results")
            results_dict = {
                'event': 'TEST',
                'peak_freq': result['peak_freq'],
                'snr': result['snr'],
                'detected': result['detected']
            }
            
            results_path = os.path.join(tmpdir, 'results.npz')
            dm.save_compressed_numpy(
                results_path,
                peak_freq=np.array([result['peak_freq']]),
                snr=np.array([result['snr']])
            )
            print("   ✓ Results saved")
        
        print("\n✅ Integration test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("COMPUTATIONAL OPTIMIZATION MODULE TESTS")
    print("="*70)
    
    results = {
        'Spectral Analyzer': test_spectral_analyzer(),
        'Data Manager': test_data_manager(),
        'HPC Manager': test_hpc_manager(),
        'Integration': test_integration()
    }
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:25s}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
