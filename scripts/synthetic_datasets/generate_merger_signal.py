#!/usr/bin/env python3
"""
Generate realistic BBH merger synthetic data with 141.7 Hz ringdown

This script generates a synthetic gravitational wave signal that includes:
- Inspiral phase (chirp)
- Merger
- Ringdown at specified frequency (default 141.7 Hz)

Author: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from datetime import datetime


def generate_inspiral(times, m1, m2, f_low=20, f_high=250):
    """
    Generate simplified inspiral chirp signal
    
    Args:
        times: Time array
        m1: Primary mass (solar masses)
        m2: Secondary mass (solar masses)
        f_low: Starting frequency (Hz)
        f_high: Ending frequency (Hz)
        
    Returns:
        Inspiral strain time series
    """
    # Chirp mass
    M = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)
    
    # Simplified chirp (frequency increases with time)
    # f(t) = f_low + (f_high - f_low) * (t/T)^(3/8)
    duration = times[-1] - times[0]
    t_normalized = (times - times[0]) / duration
    
    # Frequency evolution
    frequency = f_low + (f_high - f_low) * t_normalized**(3/8)
    
    # Phase
    phase = 2 * np.pi * np.cumsum(frequency) * (times[1] - times[0])
    
    # Amplitude (increases towards merger)
    amplitude = 1e-21 * (1 + 5 * t_normalized**2)
    
    # Strain
    strain = amplitude * np.sin(phase)
    
    # Window (taper at start)
    window = np.ones_like(times)
    taper_samples = int(0.1 * len(times))
    window[:taper_samples] = np.hanning(2*taper_samples)[:taper_samples]
    
    return strain * window


def generate_merger(times, peak_time, amplitude=5e-21):
    """
    Generate merger burst
    
    Args:
        times: Time array
        peak_time: Time of merger peak
        amplitude: Peak amplitude
        
    Returns:
        Merger strain time series
    """
    # Gaussian envelope centered at merger
    width = 0.005  # 5 ms width
    envelope = amplitude * np.exp(-(times - peak_time)**2 / (2 * width**2))
    
    # High frequency content (~250 Hz)
    frequency = 250  # Hz
    phase = 2 * np.pi * frequency * (times - peak_time)
    
    return envelope * np.sin(phase)


def generate_ringdown(times, start_time, frequency=141.7, tau=0.05, amplitude=3e-21):
    """
    Generate exponentially damped ringdown
    
    Args:
        times: Time array
        start_time: Start of ringdown
        frequency: Ringdown frequency (Hz)
        tau: Damping time (seconds)
        amplitude: Initial amplitude
        
    Returns:
        Ringdown strain time series
    """
    # Only after merger
    mask = times >= start_time
    strain = np.zeros_like(times)
    
    # Damped sinusoid
    t_ringdown = times[mask] - start_time
    envelope = amplitude * np.exp(-t_ringdown / tau)
    phase = 2 * np.pi * frequency * t_ringdown
    
    strain[mask] = envelope * np.sin(phase)
    
    return strain


def generate_noise(times, noise_level=1e-21, seed=42):
    """
    Generate Gaussian noise
    
    Args:
        times: Time array
        noise_level: RMS noise level
        seed: Random seed for reproducibility
        
    Returns:
        Noise time series
    """
    np.random.seed(seed)
    return np.random.normal(0, noise_level, len(times))


def generate_full_signal(duration=32, sample_rate=4096, m1=36, m2=29,
                        ringdown_freq=141.7, target_snr=None, seed=42):
    """
    Generate complete BBH merger signal
    
    Args:
        duration: Signal duration (seconds)
        sample_rate: Sample rate (Hz)
        m1: Primary mass (solar masses)
        m2: Secondary mass (solar masses)
        ringdown_freq: Ringdown frequency (Hz)
        target_snr: Target SNR (if None, use default amplitudes)
        seed: Random seed
        
    Returns:
        times, strain, metadata
    """
    # Time array
    n_samples = int(duration * sample_rate)
    times = np.linspace(0, duration, n_samples)
    
    # Merger at center
    merger_time = duration / 2
    
    # Generate components
    inspiral = generate_inspiral(times, m1, m2)
    merger = generate_merger(times, merger_time)
    ringdown = generate_ringdown(times, merger_time, frequency=ringdown_freq)
    noise = generate_noise(times, seed=seed)
    
    # Combine signal
    signal = inspiral + merger + ringdown
    
    # Scale to target SNR if specified
    if target_snr is not None:
        signal_power = np.sqrt(np.mean(signal**2))
        noise_power = np.sqrt(np.mean(noise**2))
        current_snr = signal_power / noise_power
        scale_factor = target_snr / current_snr
        signal = signal * scale_factor
    
    # Total strain
    total_strain = signal + noise
    
    # Metadata
    metadata = {
        'duration': duration,
        'sample_rate': sample_rate,
        'n_samples': n_samples,
        'm1': m1,
        'm2': m2,
        'ringdown_frequency': ringdown_freq,
        'merger_time': merger_time,
        'seed': seed,
        'generation_time': datetime.now().isoformat()
    }
    
    if target_snr is not None:
        metadata['target_snr'] = target_snr
        metadata['actual_snr'] = target_snr
    
    return times, total_strain, metadata


def save_to_hdf5(filename, times, strain, metadata, gps_start=1126259446):
    """
    Save to HDF5 in GWPy-compatible format
    
    Args:
        filename: Output filename
        times: Time array
        strain: Strain data
        metadata: Metadata dictionary
        gps_start: GPS start time
    """
    with h5py.File(filename, 'w') as f:
        # Create strain group
        strain_group = f.create_group('strain')
        
        # Save data
        strain_group.create_dataset('Strain', data=strain)
        strain_group.create_dataset('Xstart', data=gps_start)
        strain_group.create_dataset('Xspacing', data=1.0/metadata['sample_rate'])
        
        # Attributes
        strain_group.attrs['name'] = 'H1:SYNTHETIC-MERGER'
        strain_group.attrs['channel'] = 'H1:SYNTHETIC-STRAIN'
        strain_group.attrs['epoch'] = gps_start
        strain_group.attrs['sample_rate'] = metadata['sample_rate']
        
        # Metadata group
        meta_group = f.create_group('metadata')
        params_group = meta_group.create_group('parameters')
        
        for key, value in metadata.items():
            if isinstance(value, str):
                params_group.create_dataset(key, data=value)
            else:
                params_group.create_dataset(key, data=value)


def main():
    parser = argparse.ArgumentParser(
        description='Generate synthetic BBH merger signal with 141.7 Hz ringdown'
    )
    parser.add_argument('--mass1', type=float, default=36,
                       help='Primary mass in solar masses (default: 36)')
    parser.add_argument('--mass2', type=float, default=29,
                       help='Secondary mass in solar masses (default: 29)')
    parser.add_argument('--frequency-ringdown', type=float, default=141.7,
                       help='Ringdown frequency in Hz (default: 141.7)')
    parser.add_argument('--duration', type=float, default=32,
                       help='Signal duration in seconds (default: 32)')
    parser.add_argument('--sample-rate', type=int, default=4096,
                       help='Sample rate in Hz (default: 4096)')
    parser.add_argument('--target-snr', type=float, default=None,
                       help='Target SNR (default: None, use physical amplitudes)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for noise (default: 42)')
    parser.add_argument('--output', type=str, default='data/synthetic/merger_141hz.hdf5',
                       help='Output filename')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("SYNTHETIC BBH MERGER SIGNAL GENERATOR")
    print("=" * 70)
    print(f"\nParameters:")
    print(f"  Primary mass (m1):     {args.mass1} M☉")
    print(f"  Secondary mass (m2):   {args.mass2} M☉")
    print(f"  Ringdown frequency:    {args.frequency_ringdown} Hz")
    print(f"  Duration:              {args.duration} s")
    print(f"  Sample rate:           {args.sample_rate} Hz")
    if args.target_snr:
        print(f"  Target SNR:            {args.target_snr}")
    print(f"  Random seed:           {args.seed}")
    print(f"\nGenerating signal...")
    
    # Generate signal
    times, strain, metadata = generate_full_signal(
        duration=args.duration,
        sample_rate=args.sample_rate,
        m1=args.mass1,
        m2=args.mass2,
        ringdown_freq=args.frequency_ringdown,
        target_snr=args.target_snr,
        seed=args.seed
    )
    
    # Save to file
    print(f"Saving to: {args.output}")
    save_to_hdf5(args.output, times, strain, metadata)
    
    print("\n✅ Generation complete!")
    print(f"\nOutput file: {args.output}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
    print("\nTo analyze this data:")
    print(f"  python scripts/analizar_ringdown.py --data {args.output}")


if __name__ == '__main__':
    main()
