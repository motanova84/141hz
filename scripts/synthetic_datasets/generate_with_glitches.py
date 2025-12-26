#!/usr/bin/env python3
"""
Generate synthetic GW data with instrumental glitches

This script adds realistic glitch artifacts to synthetic signals:
- Blip glitches (short transients)
- Tomte glitches (violin mode oscillations)
- Power line harmonics

Author: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from datetime import datetime


def generate_blip_glitch(times, glitch_time, amplitude=5e-21, duration=0.01):
    """
    Generate a blip glitch (short transient)
    
    Args:
        times: Time array
        glitch_time: Time of glitch occurrence
        amplitude: Glitch amplitude
        duration: Glitch duration (seconds)
        
    Returns:
        Glitch time series
    """
    # Gaussian envelope
    width = duration / 4
    envelope = amplitude * np.exp(-(times - glitch_time)**2 / (2 * width**2))
    
    # High-frequency oscillation
    freq = 200  # Hz
    phase = 2 * np.pi * freq * (times - glitch_time)
    
    return envelope * np.sin(phase)


def generate_tomte_glitch(times, glitch_time, amplitude=3e-21, frequency=500):
    """
    Generate a tomte glitch (violin mode)
    
    Args:
        times: Time array
        glitch_time: Time of glitch occurrence
        amplitude: Glitch amplitude
        frequency: Oscillation frequency (Hz)
        
    Returns:
        Glitch time series
    """
    # Exponentially damped oscillation
    tau = 0.1  # Damping time
    mask = times >= glitch_time
    
    glitch = np.zeros_like(times)
    t_glitch = times[mask] - glitch_time
    
    envelope = amplitude * np.exp(-t_glitch / tau)
    phase = 2 * np.pi * frequency * t_glitch
    
    glitch[mask] = envelope * np.sin(phase)
    
    return glitch


def generate_power_line_harmonics(times, fundamental=60, amplitudes=None):
    """
    Generate power line harmonics
    
    Args:
        times: Time array
        fundamental: Fundamental frequency (Hz) - 60 Hz for US/North America, 50 Hz for Europe
        amplitudes: List of amplitudes for harmonics (default: decaying)
        
    Returns:
        Power line noise time series
    """
    if amplitudes is None:
        # Default: 3 harmonics with decaying amplitude
        amplitudes = [1e-21, 0.5e-21, 0.25e-21]
    
    noise = np.zeros_like(times)
    
    for n, amp in enumerate(amplitudes, 1):
        freq = n * fundamental
        noise += amp * np.sin(2 * np.pi * freq * times)
    
    return noise


def generate_signal_with_glitches(duration=32, sample_rate=4096, signal_freq=141.7,
                                  glitch_rate=0.1, seed=42):
    """
    Generate signal with glitches
    
    Args:
        duration: Signal duration (seconds)
        sample_rate: Sample rate (Hz)
        signal_freq: GW signal frequency (Hz)
        glitch_rate: Average glitches per second
        seed: Random seed
        
    Returns:
        times, strain, metadata
    """
    np.random.seed(seed)
    
    # Time array
    n_samples = int(duration * sample_rate)
    times = np.linspace(0, duration, n_samples)
    
    # Base signal (similar to merger ringdown)
    merger_time = duration / 2
    envelope = np.exp(-(times - merger_time)**2 / (2 * 0.05**2))
    signal = 2e-21 * envelope * np.sin(2 * np.pi * signal_freq * (times - merger_time))
    
    # Gaussian noise
    noise = np.random.normal(0, 1e-21, n_samples)
    
    # Add glitches
    n_glitches = int(glitch_rate * duration)
    glitch_times = np.random.uniform(0, duration, n_glitches)
    
    glitches = np.zeros_like(times)
    glitch_list = []
    
    for glitch_time in glitch_times:
        # Randomly choose glitch type
        glitch_type = np.random.choice(['blip', 'tomte'])
        
        if glitch_type == 'blip':
            glitch = generate_blip_glitch(times, glitch_time)
            glitch_list.append({'time': glitch_time, 'type': 'blip'})
        else:
            glitch = generate_tomte_glitch(times, glitch_time)
            glitch_list.append({'time': glitch_time, 'type': 'tomte'})
        
        glitches += glitch
    
    # Add power line harmonics
    power_line = generate_power_line_harmonics(times)
    
    # Combine all
    total_strain = signal + noise + glitches + power_line
    
    metadata = {
        'duration': duration,
        'sample_rate': sample_rate,
        'n_samples': n_samples,
        'signal_frequency': signal_freq,
        'glitch_rate': glitch_rate,
        'n_glitches': n_glitches,
        'glitches': glitch_list,
        'seed': seed,
        'generation_time': datetime.now().isoformat()
    }
    
    return times, total_strain, metadata


def save_to_hdf5(filename, times, strain, metadata, gps_start=1126259446):
    """
    Save to HDF5 file
    
    Args:
        filename: Output filename
        times: Time array
        strain: Strain data
        metadata: Metadata dictionary
        gps_start: GPS start time
    """
    with h5py.File(filename, 'w') as f:
        # Strain group
        strain_group = f.create_group('strain')
        strain_group.create_dataset('Strain', data=strain)
        strain_group.create_dataset('Xstart', data=gps_start)
        strain_group.create_dataset('Xspacing', data=1.0/metadata['sample_rate'])
        
        # Attributes
        strain_group.attrs['name'] = 'H1:SYNTHETIC-WITH-GLITCHES'
        strain_group.attrs['channel'] = 'H1:SYNTHETIC-STRAIN'
        strain_group.attrs['epoch'] = gps_start
        strain_group.attrs['sample_rate'] = metadata['sample_rate']
        
        # Metadata
        meta_group = f.create_group('metadata')
        params_group = meta_group.create_group('parameters')
        
        for key, value in metadata.items():
            if key == 'glitches':
                # Save glitch information separately
                continue
            elif isinstance(value, str):
                params_group.create_dataset(key, data=value)
            else:
                params_group.create_dataset(key, data=value)
        
        # Save glitch information
        if metadata.get('glitches'):
            glitch_group = meta_group.create_group('glitches')
            for i, glitch in enumerate(metadata['glitches']):
                g = glitch_group.create_group(f'glitch_{i}')
                g.create_dataset('time', data=glitch['time'])
                g.create_dataset('type', data=glitch['type'])


def main():
    parser = argparse.ArgumentParser(
        description='Generate synthetic GW data with instrumental glitches'
    )
    parser.add_argument('--duration', type=float, default=32,
                       help='Signal duration in seconds (default: 32)')
    parser.add_argument('--sample-rate', type=int, default=4096,
                       help='Sample rate in Hz (default: 4096)')
    parser.add_argument('--frequency', type=float, default=141.7,
                       help='Signal frequency in Hz (default: 141.7)')
    parser.add_argument('--glitch-rate', type=float, default=0.1,
                       help='Average glitches per second (default: 0.1)')
    parser.add_argument('--glitch-types', type=str, default='blip,tomte',
                       help='Comma-separated glitch types (default: blip,tomte)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    parser.add_argument('--output', type=str,
                       default='data/synthetic/with_glitches.hdf5',
                       help='Output filename')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("SYNTHETIC DATA GENERATOR WITH GLITCHES")
    print("=" * 70)
    print(f"\nParameters:")
    print(f"  Duration:         {args.duration} s")
    print(f"  Sample rate:      {args.sample_rate} Hz")
    print(f"  Signal frequency: {args.frequency} Hz")
    print(f"  Glitch rate:      {args.glitch_rate} per second")
    print(f"  Expected glitches: ~{int(args.glitch_rate * args.duration)}")
    print(f"  Random seed:      {args.seed}")
    print(f"\nGenerating signal with glitches...")
    
    # Generate
    times, strain, metadata = generate_signal_with_glitches(
        duration=args.duration,
        sample_rate=args.sample_rate,
        signal_freq=args.frequency,
        glitch_rate=args.glitch_rate,
        seed=args.seed
    )
    
    print(f"  Generated {metadata['n_glitches']} glitches:")
    for glitch in metadata['glitches']:
        print(f"    - {glitch['type']} at t={glitch['time']:.2f}s")
    
    # Save
    print(f"\nSaving to: {args.output}")
    save_to_hdf5(args.output, times, strain, metadata)
    
    print("\n✅ Generation complete!")
    print(f"\nOutput file: {args.output}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
    print("\nThis dataset includes:")
    print("  - GW signal at 141.7 Hz")
    print("  - Gaussian noise")
    print(f"  - {metadata['n_glitches']} instrumental glitches")
    print("  - Power line harmonics (60, 120, 180 Hz)")
    print("\nUse for testing robustness of analysis pipelines.")


if __name__ == '__main__':
    main()
