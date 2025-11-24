#!/usr/bin/env python3
"""
Example: Optimized Multi-Event Analysis with GPU and Compression
==================================================================

This example demonstrates the computational optimization features:
1. GPU-accelerated spectral analysis (with CPU fallback)
2. Compressed data storage
3. Parallel processing for multiple events
4. HPC job script generation

Usage:
    python scripts/example_optimized_analysis.py --events GW150914 GW151226
    python scripts/example_optimized_analysis.py --catalog GWTC-3 --use-gpu --n-jobs 4
"""

import argparse
import numpy as np
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gw_141hz_tools.spectral_analysis_optimized import SpectralAnalyzer
from gw_141hz_tools.compressed_io import DataManager
from gw_141hz_tools.hpc_support import HPCManager, SlurmJobGenerator


def generate_simulated_data(event: str, sample_rate: float = 4096.0) -> dict:
    """
    Generate simulated GW data for demonstration.
    
    In production, this would download real data from GWOSC.
    """
    duration = 4.0  # seconds
    n_samples = int(sample_rate * duration)
    t = np.arange(n_samples) / sample_rate
    
    # Simulated noise
    noise = np.random.randn(n_samples) * 1e-21
    
    # Add 141.7 Hz signal with varying amplitude based on "event"
    hash_val = hash(event) % 100
    amplitude = (5 + hash_val / 10) * 1e-21
    signal = amplitude * np.sin(2 * np.pi * 141.7 * t) * np.exp(-t / 0.5)
    
    data = noise + signal
    
    return {
        'event': event,
        'data': data,
        'sample_rate': sample_rate,
        'gps_start': 1126259462.0 + hash_val,
        'duration': duration
    }


def analyze_single_event(
    event: str,
    use_gpu: bool = False,
    save_compressed: bool = True,
    output_dir: str = 'results/optimized'
) -> dict:
    """
    Analyze a single GW event with optimized methods.
    
    Parameters
    ----------
    event : str
        Event name
    use_gpu : bool
        Use GPU acceleration
    save_compressed : bool
        Save results with compression
    output_dir : str
        Output directory
        
    Returns
    -------
    results : dict
        Analysis results
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {event}")
    print(f"{'='*60}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate/load data
    print("1. Loading data...")
    event_data = generate_simulated_data(event)
    data = event_data['data']
    sample_rate = event_data['sample_rate']
    
    # Save compressed data (optional)
    if save_compressed:
        print("2. Saving compressed data...")
        dm = DataManager()
        data_path = os.path.join(output_dir, f'{event}_data.h5')
        dm.save_timeseries(
            data,
            data_path,
            sample_rate,
            event_data['gps_start'],
            metadata={'event': event, 'duration': event_data['duration']}
        )
    
    # Analyze with optimized spectral analyzer
    print("3. Running spectral analysis...")
    analyzer = SpectralAnalyzer(use_gpu=use_gpu, n_jobs=1)
    
    # Compute FFT
    freqs, power = analyzer.compute_fft(data, sample_rate)
    
    # Find 141.7 Hz peak
    result = analyzer.find_peaks(freqs, power, target_freq=141.7, freq_range=2.0)
    
    # Compute PSD
    freqs_psd, psd = analyzer.compute_psd(data, sample_rate, nperseg=512)
    
    # Compile results (convert numpy types to Python types for JSON)
    results = {
        'event': event,
        'timestamp': datetime.now().isoformat(),
        'gpu_used': bool(analyzer.use_gpu),
        'detection': {
            'detected': bool(result['detected']),
            'peak_freq': float(result['peak_freq']),
            'snr': float(result['snr']),
            'threshold': float(result['threshold'])
        },
        'data_size_mb': float(data.nbytes / 1e6),
        'n_samples': int(len(data)),
        'sample_rate': float(sample_rate)
    }
    
    print("\n4. Results:")
    print(f"   - Detected: {result['detected']}")
    print(f"   - Peak frequency: {result['peak_freq']:.2f} Hz")
    print(f"   - SNR: {result['snr']:.2f}")
    print(f"   - GPU used: {analyzer.use_gpu}")
    
    # Save results
    if save_compressed:
        print("\n5. Saving results...")
        dm = DataManager()
        results_path = os.path.join(output_dir, f'{event}_results.npz')
        dm.save_compressed_numpy(
            results_path,
            freqs=freqs[:1000],  # Save subset
            power=power[:1000],
            peak_freq=np.array([result['peak_freq']]),
            snr=np.array([result['snr']])
        )
        
        # Also save JSON summary
        json_path = os.path.join(output_dir, f'{event}_summary.json')
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"   Saved to {json_path}")
    
    return results


def analyze_multiple_events(
    events: list,
    use_gpu: bool = False,
    n_jobs: int = 1,
    output_dir: str = 'results/optimized'
) -> dict:
    """
    Analyze multiple events with parallel processing.
    
    Parameters
    ----------
    events : list of str
        List of event names
    use_gpu : bool
        Use GPU acceleration
    n_jobs : int
        Number of parallel jobs
    output_dir : str
        Output directory
        
    Returns
    -------
    summary : dict
        Summary of all results
    """
    print(f"\n{'='*70}")
    print(f"MULTI-EVENT ANALYSIS: {len(events)} events")
    print(f"{'='*70}")
    print(f"Configuration:")
    print(f"  - GPU: {use_gpu}")
    print(f"  - Parallel jobs: {n_jobs}")
    print(f"  - Output: {output_dir}")
    
    if n_jobs > 1:
        # Parallel processing
        print(f"\nProcessing {len(events)} events in parallel...")
        from joblib import Parallel, delayed
        
        results = Parallel(n_jobs=n_jobs)(
            delayed(analyze_single_event)(
                event, use_gpu, True, output_dir
            ) for event in events
        )
    else:
        # Sequential processing
        print(f"\nProcessing {len(events)} events sequentially...")
        results = [
            analyze_single_event(event, use_gpu, True, output_dir)
            for event in events
        ]
    
    # Aggregate results
    n_detected = sum(1 for r in results if r['detection']['detected'])
    mean_snr = np.mean([r['detection']['snr'] for r in results])
    
    summary = {
        'n_events': len(events),
        'n_detected': n_detected,
        'detection_rate': n_detected / len(events),
        'mean_snr': mean_snr,
        'events': events,
        'individual_results': results,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save summary
    summary_path = os.path.join(output_dir, 'multi_event_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Events processed: {len(events)}")
    print(f"Detections: {n_detected}/{len(events)} ({n_detected/len(events)*100:.1f}%)")
    print(f"Mean SNR: {mean_snr:.2f}")
    print(f"\nResults saved to {output_dir}/")
    
    return summary


def generate_hpc_scripts(
    catalog: str = 'GWTC-3',
    use_gpu: bool = False,
    output_dir: str = 'hpc_jobs'
) -> None:
    """
    Generate HPC job scripts for large-scale processing.
    
    Parameters
    ----------
    catalog : str
        Catalog name (GWTC-1, GWTC-3, etc.)
    use_gpu : bool
        Generate GPU job scripts
    output_dir : str
        Output directory for scripts
    """
    print(f"\n{'='*70}")
    print(f"GENERATING HPC JOB SCRIPTS FOR {catalog}")
    print(f"{'='*70}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get event list
    manager = HPCManager()
    events = manager._get_catalog_events(catalog)
    
    print(f"\nCatalog: {catalog}")
    print(f"Events: {len(events)}")
    
    # Create Slurm job generator
    if use_gpu:
        slurm = SlurmJobGenerator(
            partition='gpu',
            time_limit='04:00:00',
            cpus_per_task=8,
            memory='64G',
            gpu=True
        )
        script_name = f'job_{catalog.lower()}_gpu.sh'
    else:
        slurm = SlurmJobGenerator(
            partition='normal',
            time_limit='08:00:00',
            cpus_per_task=16,
            memory='32G',
            gpu=False
        )
        script_name = f'job_{catalog.lower()}_cpu.sh'
    
    # Generate array job for all events
    script_path = os.path.join(output_dir, script_name)
    slurm.generate_array_job(
        job_name=f'{catalog.lower()}_141hz',
        script_path=script_path,
        output_dir='results/hpc_output',
        python_script='scripts/example_optimized_analysis.py',
        events=events
    )
    
    print(f"\nGenerated: {script_path}")
    print(f"\nTo submit: sbatch {script_path}")
    
    # Generate single-event example
    single_script = os.path.join(output_dir, f'job_{catalog.lower()}_single_example.sh')
    slurm.generate_job_script(
        job_name=f'{events[0]}_141hz',
        script_path=single_script,
        output_dir='results/hpc_output',
        python_script='scripts/example_optimized_analysis.py',
        arguments=f'--events {events[0]} {"--use-gpu" if use_gpu else ""}',
        conda_env='gw_analysis',
        modules=['python/3.11'] + (['cuda/12.0'] if use_gpu else [])
    )
    
    print(f"Generated: {single_script}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Optimized gravitational wave analysis example'
    )
    parser.add_argument(
        '--events',
        nargs='+',
        help='Event names to analyze'
    )
    parser.add_argument(
        '--catalog',
        choices=['GWTC-1', 'GWTC-2', 'GWTC-3', 'GWTC-4'],
        help='Analyze entire catalog'
    )
    parser.add_argument(
        '--use-gpu',
        action='store_true',
        help='Use GPU acceleration'
    )
    parser.add_argument(
        '--n-jobs',
        type=int,
        default=1,
        help='Number of parallel jobs (default: 1)'
    )
    parser.add_argument(
        '--output-dir',
        default='results/optimized',
        help='Output directory (default: results/optimized)'
    )
    parser.add_argument(
        '--generate-hpc-scripts',
        action='store_true',
        help='Generate HPC job scripts'
    )
    
    args = parser.parse_args()
    
    # Generate HPC scripts
    if args.generate_hpc_scripts:
        catalog = args.catalog or 'GWTC-3'
        generate_hpc_scripts(catalog, args.use_gpu)
        return
    
    # Get event list
    if args.catalog:
        manager = HPCManager()
        events = manager._get_catalog_events(args.catalog)
        print(f"Processing {args.catalog}: {len(events)} events")
    elif args.events:
        events = args.events
    else:
        # Default: analyze a few test events
        events = ['GW150914', 'GW151226', 'GW170814']
        print("No events specified, using default test events")
    
    # Run analysis
    if len(events) == 1:
        # Single event
        analyze_single_event(
            events[0],
            use_gpu=args.use_gpu,
            save_compressed=True,
            output_dir=args.output_dir
        )
    else:
        # Multiple events
        analyze_multiple_events(
            events,
            use_gpu=args.use_gpu,
            n_jobs=args.n_jobs,
            output_dir=args.output_dir
        )


if __name__ == "__main__":
    main()
