#!/usr/bin/env python3
"""
Generate parameter sweep datasets

Creates multiple synthetic datasets with systematic parameter variations.
Useful for studying detection thresholds, frequency resolution, etc.

Author: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from datetime import datetime
import json


def generate_signal(times, frequency, snr, noise_level=1e-21, seed=42):
    """
    Generate simple signal with specified parameters
    
    Args:
        times: Time array
        frequency: Signal frequency (Hz)
        snr: Target SNR
        noise_level: Noise RMS level
        seed: Random seed
        
    Returns:
        Strain data
    """
    np.random.seed(seed)
    
    duration = times[-1] - times[0]
    merger_time = duration / 2
    
    # Signal with envelope
    envelope = np.exp(-(times - merger_time)**2 / (2 * 0.05**2))
    signal = envelope * np.sin(2 * np.pi * frequency * (times - merger_time))
    
    # Noise
    noise = np.random.normal(0, noise_level, len(times))
    
    # Scale signal to achieve target SNR
    signal_power = np.sqrt(np.mean(signal**2))
    noise_power = np.sqrt(np.mean(noise**2))
    current_snr = signal_power / noise_power
    signal = signal * (snr / current_snr)
    
    return signal + noise


def save_dataset(filename, times, strain, parameters, gps_start=1126259446):
    """
    Save dataset to HDF5
    
    Args:
        filename: Output filename
        times: Time array
        strain: Strain data
        parameters: Parameters dictionary
        gps_start: GPS start time
    """
    with h5py.File(filename, 'w') as f:
        # Strain group
        strain_group = f.create_group('strain')
        strain_group.create_dataset('Strain', data=strain)
        strain_group.create_dataset('Xstart', data=gps_start)
        strain_group.create_dataset('Xspacing', data=1.0/parameters['sample_rate'])
        
        # Attributes
        strain_group.attrs['name'] = 'H1:SYNTHETIC-SWEEP'
        strain_group.attrs['channel'] = 'H1:SYNTHETIC-STRAIN'
        strain_group.attrs['epoch'] = gps_start
        strain_group.attrs['sample_rate'] = parameters['sample_rate']
        
        # Metadata
        meta_group = f.create_group('metadata')
        params_group = meta_group.create_group('parameters')
        
        for key, value in parameters.items():
            if isinstance(value, str):
                params_group.create_dataset(key, data=value)
            else:
                params_group.create_dataset(key, data=value)


def generate_frequency_sweep(output_dir, freq_range, n_steps, **kwargs):
    """
    Generate datasets with varying frequency
    
    Args:
        output_dir: Output directory
        freq_range: (f_min, f_max) in Hz
        n_steps: Number of steps
        **kwargs: Other parameters (duration, sample_rate, snr, etc.)
    """
    frequencies = np.linspace(freq_range[0], freq_range[1], n_steps)
    
    print(f"\nGenerating frequency sweep: {freq_range[0]}-{freq_range[1]} Hz, {n_steps} steps")
    
    duration = kwargs.get('duration', 32)
    sample_rate = kwargs.get('sample_rate', 4096)
    snr = kwargs.get('snr', 5.0)
    
    n_samples = int(duration * sample_rate)
    times = np.linspace(0, duration, n_samples)
    
    datasets = []
    
    for i, freq in enumerate(frequencies):
        print(f"  {i+1}/{n_steps}: f = {freq:.2f} Hz", end='\r')
        
        # Generate signal
        strain = generate_signal(times, freq, snr, seed=42+i)
        
        # Parameters
        params = {
            'duration': duration,
            'sample_rate': sample_rate,
            'frequency': freq,
            'snr': snr,
            'sweep_type': 'frequency',
            'sweep_index': i,
            'generation_time': datetime.now().isoformat()
        }
        
        # Save
        filename = output_dir / f'freq_sweep_{i:03d}_f{freq:.2f}Hz.hdf5'
        save_dataset(filename, times, strain, params)
        
        datasets.append({
            'filename': filename.name,
            'frequency': freq,
            'snr': snr
        })
    
    print(f"\n  ✅ Generated {n_steps} frequency sweep datasets")
    return datasets


def generate_snr_sweep(output_dir, snr_range, n_steps, **kwargs):
    """
    Generate datasets with varying SNR
    
    Args:
        output_dir: Output directory
        snr_range: (snr_min, snr_max)
        n_steps: Number of steps
        **kwargs: Other parameters
    """
    snr_values = np.linspace(snr_range[0], snr_range[1], n_steps)
    
    print(f"\nGenerating SNR sweep: {snr_range[0]}-{snr_range[1]}, {n_steps} steps")
    
    duration = kwargs.get('duration', 32)
    sample_rate = kwargs.get('sample_rate', 4096)
    frequency = kwargs.get('frequency', 141.7)
    
    n_samples = int(duration * sample_rate)
    times = np.linspace(0, duration, n_samples)
    
    datasets = []
    
    for i, snr in enumerate(snr_values):
        print(f"  {i+1}/{n_steps}: SNR = {snr:.2f}", end='\r')
        
        # Generate signal
        strain = generate_signal(times, frequency, snr, seed=42+i)
        
        # Parameters
        params = {
            'duration': duration,
            'sample_rate': sample_rate,
            'frequency': frequency,
            'snr': snr,
            'sweep_type': 'snr',
            'sweep_index': i,
            'generation_time': datetime.now().isoformat()
        }
        
        # Save
        filename = output_dir / f'snr_sweep_{i:03d}_snr{snr:.2f}.hdf5'
        save_dataset(filename, times, strain, params)
        
        datasets.append({
            'filename': filename.name,
            'frequency': frequency,
            'snr': snr
        })
    
    print(f"\n  ✅ Generated {n_steps} SNR sweep datasets")
    return datasets


def generate_duration_sweep(output_dir, duration_range, n_steps, **kwargs):
    """
    Generate datasets with varying duration
    
    Args:
        output_dir: Output directory
        duration_range: (duration_min, duration_max) in seconds
        n_steps: Number of steps
        **kwargs: Other parameters
    """
    durations = np.linspace(duration_range[0], duration_range[1], n_steps)
    
    print(f"\nGenerating duration sweep: {duration_range[0]}-{duration_range[1]} s, {n_steps} steps")
    
    sample_rate = kwargs.get('sample_rate', 4096)
    frequency = kwargs.get('frequency', 141.7)
    snr = kwargs.get('snr', 5.0)
    
    datasets = []
    
    for i, duration in enumerate(durations):
        print(f"  {i+1}/{n_steps}: T = {duration:.1f} s", end='\r')
        
        n_samples = int(duration * sample_rate)
        times = np.linspace(0, duration, n_samples)
        
        # Generate signal
        strain = generate_signal(times, frequency, snr, seed=42+i)
        
        # Parameters
        params = {
            'duration': duration,
            'sample_rate': sample_rate,
            'frequency': frequency,
            'snr': snr,
            'sweep_type': 'duration',
            'sweep_index': i,
            'generation_time': datetime.now().isoformat()
        }
        
        # Save
        filename = output_dir / f'duration_sweep_{i:03d}_T{duration:.1f}s.hdf5'
        save_dataset(filename, times, strain, params)
        
        datasets.append({
            'filename': filename.name,
            'frequency': frequency,
            'snr': snr,
            'duration': duration
        })
    
    print(f"\n  ✅ Generated {n_steps} duration sweep datasets")
    return datasets


def main():
    parser = argparse.ArgumentParser(
        description='Generate parameter sweep synthetic datasets'
    )
    parser.add_argument('--parameter', type=str, required=True,
                       choices=['frequency', 'snr', 'duration'],
                       help='Parameter to sweep')
    parser.add_argument('--range', type=str, required=True,
                       help='Range as min,max (e.g., "130,150" for frequency)')
    parser.add_argument('--steps', type=int, default=20,
                       help='Number of steps (default: 20)')
    parser.add_argument('--duration', type=float, default=32,
                       help='Signal duration in seconds (default: 32)')
    parser.add_argument('--sample-rate', type=int, default=4096,
                       help='Sample rate in Hz (default: 4096)')
    parser.add_argument('--frequency', type=float, default=141.7,
                       help='Fixed frequency when not sweeping (default: 141.7)')
    parser.add_argument('--snr', type=float, default=5.0,
                       help='Fixed SNR when not sweeping (default: 5.0)')
    parser.add_argument('--output-dir', type=str,
                       default='data/synthetic/sweep',
                       help='Output directory')
    
    args = parser.parse_args()
    
    # Parse range
    range_parts = args.range.split(',')
    if len(range_parts) != 2:
        parser.error("Range must be in format: min,max")
    
    param_range = (float(range_parts[0]), float(range_parts[1]))
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("PARAMETER SWEEP DATASET GENERATOR")
    print("=" * 70)
    print(f"\nSweeping: {args.parameter}")
    print(f"Range: {param_range[0]} to {param_range[1]}")
    print(f"Steps: {args.steps}")
    print(f"Output directory: {output_dir}")
    
    # Common parameters
    kwargs = {
        'duration': args.duration,
        'sample_rate': args.sample_rate,
        'frequency': args.frequency,
        'snr': args.snr
    }
    
    # Generate sweep
    if args.parameter == 'frequency':
        datasets = generate_frequency_sweep(output_dir, param_range, args.steps, **kwargs)
    elif args.parameter == 'snr':
        datasets = generate_snr_sweep(output_dir, param_range, args.steps, **kwargs)
    elif args.parameter == 'duration':
        datasets = generate_duration_sweep(output_dir, param_range, args.steps, **kwargs)
    
    # Save manifest
    manifest = {
        'parameter': args.parameter,
        'range': param_range,
        'n_datasets': len(datasets),
        'generation_time': datetime.now().isoformat(),
        'datasets': datasets
    }
    
    manifest_file = output_dir / 'sweep_manifest.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Parameter sweep complete!")
    print(f"Generated {len(datasets)} datasets in {output_dir}")
    print(f"Manifest saved to: {manifest_file}")
    print("\nExample analysis:")
    print(f"  for file in {output_dir}/*.hdf5; do")
    print(f"    python scripts/analizar_ringdown.py --data $file")
    print(f"  done")


if __name__ == '__main__':
    main()
