#!/usr/bin/env python3
"""
Example: QCAL Biological Model with Real Environmental Data

This script demonstrates how to use real environmental data from NASA POWER API
to validate the QCAL biological hypothesis with actual climate observations.

No API key required - uses NASA POWER public API!

Author: José Manuel Mota Burruezo
Date: January 31, 2026
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'quantum_biology'))

import numpy as np
import matplotlib.pyplot as plt
from environmental_integration import create_environmental_cycles_from_nasa_power


def main():
    """Run QCAL biological model with real environmental data."""
    
    print("=" * 70)
    print("QCAL Biological Model - Real Environmental Data Validation")
    print("=" * 70)
    print()
    
    # Configuration
    location_name = "Phoenix, AZ"
    latitude = 33.4484
    longitude = -112.0740
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    parameter = "T2M"  # Temperature at 2 meters
    
    print(f"Location: {location_name}")
    print(f"Coordinates: {latitude}°N, {longitude}°W")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Parameter: {parameter} (Temperature at 2m)")
    print()
    
    # Fetch real environmental data
    print("Fetching real environmental data from NASA POWER API...")
    try:
        time, signal = create_environmental_cycles_from_nasa_power(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            parameter=parameter
        )
        print(f"✓ Successfully retrieved {len(signal)} days of data")
        print()
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        return 1
    
    # Analyze the environmental signal
    print("Environmental Signal Analysis:")
    print(f"  Duration: {len(signal)} days")
    print(f"  Time range: {time[0]:.0f} to {time[-1]:.0f} seconds")
    print(f"  Signal mean: {np.mean(signal):.3f} (normalized)")
    print(f"  Signal std: {np.std(signal):.3f}")
    print(f"  Signal range: [{np.min(signal):.3f}, {np.max(signal):.3f}]")
    print()
    
    # Perform spectral analysis
    print("Spectral Analysis:")
    from scipy import signal as sp_signal
    
    # Compute power spectral density
    sampling_rate = 1.0 / (24 * 3600)  # 1 sample per day, in Hz
    frequencies, psd = sp_signal.periodogram(signal, fs=sampling_rate)
    
    # Convert frequencies to periods (in days)
    periods = 1.0 / (frequencies + 1e-10) / (24 * 3600)
    
    # Find dominant periods
    # Exclude DC component (first element)
    dominant_indices = np.argsort(psd[1:])[-5:] + 1  # Top 5 peaks
    
    print("  Dominant periods:")
    for i, idx in enumerate(dominant_indices[::-1]):
        period_days = periods[idx]
        freq_hz = frequencies[idx]
        power = psd[idx]
        print(f"    {i+1}. Period: {period_days:.1f} days, "
              f"Frequency: {freq_hz*1e6:.2f} μHz, "
              f"Power: {power:.2e}")
    print()
    
    # Check for annual cycle
    annual_freq = 1.0 / (365 * 24 * 3600)  # Hz
    annual_idx = np.argmin(np.abs(frequencies - annual_freq))
    annual_period = periods[annual_idx]
    annual_power = psd[annual_idx]
    
    print(f"  Annual cycle (expected ~365 days):")
    print(f"    Detected period: {annual_period:.1f} days")
    print(f"    Power: {annual_power:.2e}")
    print()
    
    # Create visualizations
    print("Creating visualizations...")
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Plot 1: Environmental signal time series
    time_days = time / (24 * 3600)
    axes[0].plot(time_days, signal, linewidth=0.8)
    axes[0].set_xlabel('Time (days)')
    axes[0].set_ylabel('Normalized Signal')
    axes[0].set_title(f'Environmental Signal: {location_name} ({start_date} to {end_date})')
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Power spectral density
    # Only plot periods from 1 day to 400 days
    valid_indices = (periods >= 1) & (periods <= 400)
    axes[1].semilogy(periods[valid_indices], psd[valid_indices])
    axes[1].set_xlabel('Period (days)')
    axes[1].set_ylabel('Power Spectral Density')
    axes[1].set_title('Power Spectrum of Environmental Signal')
    axes[1].axvline(365, color='r', linestyle='--', alpha=0.5, label='Annual cycle (365 days)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Plot 3: Zoomed-in time series (first 60 days)
    zoom_days = 60
    zoom_indices = time_days <= zoom_days
    axes[2].plot(time_days[zoom_indices], signal[zoom_indices], linewidth=1.2)
    axes[2].set_xlabel('Time (days)')
    axes[2].set_ylabel('Normalized Signal')
    axes[2].set_title(f'Environmental Signal - First {zoom_days} Days (Detail)')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'environmental_data_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization to: {output_file}")
    print()
    
    # Success
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("Next steps:")
    print("  1. Use this data with QCAL biological model")
    print("  2. Compare multiple locations (different climates)")
    print("  3. Test biological synchrony predictions")
    print()
    print("See: docs/ENVIRONMENTAL_APIS_README.md for more information")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
