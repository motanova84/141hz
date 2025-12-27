#!/usr/bin/env python3
"""
Generate synthetic multi-detector gravitational wave data

This script generates coherent signals across multiple detectors (H1, L1, V1)
accounting for:
- Detector antenna patterns
- Time delays due to Earth geometry
- Detector-specific noise characteristics

Author: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from datetime import datetime


# Detector locations (approximate, in Earth-centered coordinates)
DETECTOR_LOCATIONS = {
    'H1': {'lat': 46.45, 'lon': -119.41, 'name': 'LIGO Hanford'},
    'L1': {'lat': 30.56, 'lon': -90.77, 'name': 'LIGO Livingston'},
    'V1': {'lat': 43.63, 'lon': 10.50, 'name': 'Virgo'}
}


def calculate_time_delay(detector1, detector2, ra, dec):
    """
    Calculate time delay between two detectors for a source at (RA, Dec)
    
    Simplified calculation based on detector separation and source direction
    
    Args:
        detector1: First detector code ('H1', 'L1', or 'V1')
        detector2: Second detector code
        ra: Right ascension (radians)
        dec: Declination (radians)
        
    Returns:
        Time delay in seconds (positive if signal arrives at detector1 first)
    """
    # Earth radius in meters
    R_earth = 6.371e6
    c = 299792458  # Speed of light (m/s)
    
    # Get detector positions
    loc1 = DETECTOR_LOCATIONS[detector1]
    loc2 = DETECTOR_LOCATIONS[detector2]
    
    # Convert to radians
    lat1, lon1 = np.radians(loc1['lat']), np.radians(loc1['lon'])
    lat2, lon2 = np.radians(loc2['lat']), np.radians(loc2['lon'])
    
    # Detector positions (simplified Cartesian approximation)
    x1 = R_earth * np.cos(lat1) * np.cos(lon1)
    y1 = R_earth * np.cos(lat1) * np.sin(lon1)
    z1 = R_earth * np.sin(lat1)
    
    x2 = R_earth * np.cos(lat2) * np.cos(lon2)
    y2 = R_earth * np.cos(lat2) * np.sin(lon2)
    z2 = R_earth * np.sin(lat2)
    
    # Source direction (unit vector)
    src_x = np.cos(dec) * np.cos(ra)
    src_y = np.cos(dec) * np.sin(ra)
    src_z = np.sin(dec)
    
    # Baseline vector
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    
    # Time delay = (baseline · source) / c
    delay = (dx * src_x + dy * src_y + dz * src_z) / c
    
    return delay


def antenna_response(detector, ra, dec, psi=0):
    """
    Calculate simplified antenna response for a detector
    
    Note: This is a simplified model for demonstration purposes.
    For accurate antenna patterns, use proper detector tensor calculations
    as documented in LIGO-T0900288 (Detector Response to Gravitational Waves).
    
    Args:
        detector: Detector code ('H1', 'L1', or 'V1')
        ra: Right ascension (radians)
        dec: Declination (radians)
        psi: Polarization angle (radians)
        
    Returns:
        (F_plus, F_cross): Antenna pattern functions
    """
    # Simplified antenna response (not accurate, but illustrative)
    # Real calculation requires detector tensor and source direction
    
    loc = DETECTOR_LOCATIONS[detector]
    lat = np.radians(loc['lat'])
    
    # Simplified model
    cos_theta = np.sin(lat) * np.sin(dec) + np.cos(lat) * np.cos(dec)
    
    # Plus polarization
    F_plus = 0.5 * (1 + cos_theta**2)
    
    # Cross polarization
    F_cross = cos_theta
    
    return F_plus, F_cross


def generate_base_signal(times, frequency=141.7, amplitude=1e-21):
    """
    Generate base gravitational wave signal
    
    Args:
        times: Time array
        frequency: Signal frequency (Hz)
        amplitude: Signal amplitude
        
    Returns:
        Signal time series (h_plus, h_cross)
    """
    # Simple monochromatic signal with envelope
    duration = times[-1] - times[0]
    merger_time = duration / 2
    
    # Gaussian envelope
    envelope = np.exp(-(times - merger_time)**2 / (2 * 0.05**2))
    
    # Plus polarization (dominant)
    phase = 2 * np.pi * frequency * (times - merger_time)
    h_plus = amplitude * envelope * np.sin(phase)
    
    # Cross polarization (phase shifted)
    h_cross = amplitude * envelope * np.cos(phase) * 0.5
    
    return h_plus, h_cross


def generate_detector_signal(times, detector, ra, dec, frequency=141.7,
                            reference_detector='H1', noise_level=1e-21, seed=42):
    """
    Generate signal for a specific detector
    
    Args:
        times: Time array (relative to reference detector)
        detector: Detector code
        ra: Right ascension (radians)
        dec: Declination (radians)
        frequency: Signal frequency (Hz)
        reference_detector: Reference detector for time delays
        noise_level: RMS noise level
        seed: Random seed (different for each detector)
        
    Returns:
        Detector strain time series
    """
    # Calculate time delay relative to reference
    if detector != reference_detector:
        delay = calculate_time_delay(reference_detector, detector, ra, dec)
    else:
        delay = 0
    
    # Shift time array
    times_shifted = times - delay
    
    # Generate base signal
    h_plus, h_cross = generate_base_signal(times_shifted, frequency)
    
    # Apply antenna response
    F_plus, F_cross = antenna_response(detector, ra, dec)
    
    # Detector strain (linear combination)
    signal = F_plus * h_plus + F_cross * h_cross
    
    # Add noise
    np.random.seed(seed)
    noise = np.random.normal(0, noise_level, len(times))
    
    strain = signal + noise
    
    return strain, delay


def save_detector_data(filename, times, strain, detector, metadata):
    """
    Save detector data to HDF5
    
    Args:
        filename: Output filename
        times: Time array
        strain: Strain data
        detector: Detector code
        metadata: Metadata dictionary
    """
    gps_start = 1126259446  # GW150914 GPS time
    
    with h5py.File(filename, 'w') as f:
        # Strain group
        strain_group = f.create_group('strain')
        strain_group.create_dataset('Strain', data=strain)
        strain_group.create_dataset('Xstart', data=gps_start)
        strain_group.create_dataset('Xspacing', data=1.0/metadata['sample_rate'])
        
        # Attributes
        strain_group.attrs['name'] = f'{detector}:SYNTHETIC-MULTIDET'
        strain_group.attrs['channel'] = f'{detector}:SYNTHETIC-STRAIN'
        strain_group.attrs['detector'] = detector
        strain_group.attrs['epoch'] = gps_start
        strain_group.attrs['sample_rate'] = metadata['sample_rate']
        
        # Metadata
        meta_group = f.create_group('metadata')
        params_group = meta_group.create_group('parameters')
        
        for key, value in metadata.items():
            if isinstance(value, str):
                params_group.create_dataset(key, data=value)
            else:
                params_group.create_dataset(key, data=value)


def main():
    parser = argparse.ArgumentParser(
        description='Generate synthetic multi-detector GW data'
    )
    parser.add_argument('--detectors', type=str, default='H1,L1,V1',
                       help='Comma-separated detector list (default: H1,L1,V1)')
    parser.add_argument('--ra', type=float, default=1.95,
                       help='Right ascension in radians (default: 1.95, like GW150914)')
    parser.add_argument('--dec', type=float, default=-1.27,
                       help='Declination in radians (default: -1.27, like GW150914)')
    parser.add_argument('--frequency', type=float, default=141.7,
                       help='Signal frequency in Hz (default: 141.7)')
    parser.add_argument('--duration', type=float, default=32,
                       help='Signal duration in seconds (default: 32)')
    parser.add_argument('--sample-rate', type=int, default=4096,
                       help='Sample rate in Hz (default: 4096)')
    parser.add_argument('--noise-level', type=float, default=1e-21,
                       help='Noise level (default: 1e-21)')
    parser.add_argument('--output-dir', type=str, default='data/synthetic',
                       help='Output directory (default: data/synthetic)')
    
    args = parser.parse_args()
    
    # Parse detectors
    detectors = [d.strip() for d in args.detectors.split(',')]
    
    # Validate detectors
    for det in detectors:
        if det not in DETECTOR_LOCATIONS:
            print(f"❌ Unknown detector: {det}")
            print(f"   Available: {', '.join(DETECTOR_LOCATIONS.keys())}")
            return
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("SYNTHETIC MULTI-DETECTOR SIGNAL GENERATOR")
    print("=" * 70)
    print(f"\nDetectors: {', '.join(detectors)}")
    print(f"Sky position: RA={args.ra:.3f} rad, Dec={args.dec:.3f} rad")
    print(f"Frequency: {args.frequency} Hz")
    print(f"Duration: {args.duration} s")
    print(f"Sample rate: {args.sample_rate} Hz")
    print(f"\nCalculating time delays...")
    
    # Time array (reference detector time)
    n_samples = int(args.duration * args.sample_rate)
    times = np.linspace(0, args.duration, n_samples)
    
    # Reference detector (first in list)
    ref_detector = detectors[0]
    
    # Generate for each detector
    for i, detector in enumerate(detectors):
        print(f"\nGenerating data for {detector} ({DETECTOR_LOCATIONS[detector]['name']})...")
        
        # Generate signal
        strain, delay = generate_detector_signal(
            times, detector, args.ra, args.dec,
            frequency=args.frequency,
            reference_detector=ref_detector,
            noise_level=args.noise_level,
            seed=42 + i  # Different seed for each detector
        )
        
        print(f"  Time delay relative to {ref_detector}: {delay*1000:.2f} ms")
        
        # Metadata
        metadata = {
            'detector': detector,
            'duration': args.duration,
            'sample_rate': args.sample_rate,
            'frequency': args.frequency,
            'ra': args.ra,
            'dec': args.dec,
            'time_delay': delay,
            'reference_detector': ref_detector,
            'noise_level': args.noise_level,
            'generation_time': datetime.now().isoformat()
        }
        
        # Save
        filename = output_dir / f'{detector}-multidetector.hdf5'
        save_detector_data(filename, times, strain, detector, metadata)
        print(f"  Saved to: {filename}")
    
    print("\n✅ Multi-detector data generation complete!")
    print(f"\nTo analyze coherence:")
    print(f"  python scripts/analisis_coherencia_multidetector.py \\")
    for detector in detectors:
        print(f"    --{detector.lower()} {output_dir / f'{detector}-multidetector.hdf5'} \\")


if __name__ == '__main__':
    main()
