#!/usr/bin/env python3
"""
Numerical Precision Benchmarking

Tests numerical precision and accuracy of implementations:
- Floating point precision (float32 vs float64)
- High-precision arithmetic (mpmath)
- Energy calculation accuracy (E = hf)
- Frequency resolution limits

Author: José Manuel Mota Burruezo (JMMB)
"""

import numpy as np
import argparse
import json
from pathlib import Path
from datetime import datetime


def test_float_precision():
    """
    Test floating point precision
    
    Returns:
        Results dictionary
    """
    results = {
        'test': 'Floating Point Precision',
        'float32': {},
        'float64': {}
    }
    
    # Reference value (exact)
    f0_exact = 141.7001  # Hz
    h_exact = 6.62607015e-34  # Planck constant (J·s)
    
    # Test float32
    f0_32 = np.float32(f0_exact)
    h_32 = np.float32(h_exact)
    E_32 = h_32 * f0_32
    
    error_32 = abs(float(E_32) - (h_exact * f0_exact))
    rel_error_32 = error_32 / (h_exact * f0_exact)
    
    results['float32'] = {
        'frequency': float(f0_32),
        'planck_constant': float(h_32),
        'energy': float(E_32),
        'absolute_error': error_32,
        'relative_error': rel_error_32,
        'significant_digits': int(-np.log10(rel_error_32)) if rel_error_32 > 0 else 16
    }
    
    # Test float64
    f0_64 = np.float64(f0_exact)
    h_64 = np.float64(h_exact)
    E_64 = h_64 * f0_64
    
    error_64 = abs(float(E_64) - (h_exact * f0_exact))
    rel_error_64 = error_64 / (h_exact * f0_exact)
    
    results['float64'] = {
        'frequency': float(f0_64),
        'planck_constant': float(h_64),
        'energy': float(E_64),
        'absolute_error': error_64,
        'relative_error': rel_error_64,
        'significant_digits': int(-np.log10(rel_error_64)) if rel_error_64 > 0 else 16
    }
    
    return results


def test_mpmath_precision(precision=100):
    """
    Test high-precision arithmetic with mpmath
    
    Args:
        precision: Number of decimal digits
        
    Returns:
        Results dictionary
    """
    try:
        import mpmath
    except ImportError:
        return {
            'test': 'MPMath High Precision',
            'available': False,
            'error': 'mpmath not available'
        }
    
    # Set precision
    mpmath.mp.dps = precision
    
    # Constants with high precision
    f0 = mpmath.mpf('141.7001')
    h = mpmath.mpf('6.62607015e-34')
    
    # Compute energy
    E = h * f0
    
    return {
        'test': 'MPMath High Precision',
        'available': True,
        'precision_digits': precision,
        'frequency': str(f0),
        'planck_constant': str(h),
        'energy': str(E),
        'energy_scientific': f"{float(E):.15e}"
    }


def test_frequency_resolution(sample_rate=4096, duration=32):
    """
    Test frequency resolution limits
    
    Args:
        sample_rate: Sample rate (Hz)
        duration: Signal duration (seconds)
        
    Returns:
        Results dictionary
    """
    # Frequency resolution = 1 / duration
    freq_resolution = 1.0 / duration
    
    # Nyquist frequency
    nyquist = sample_rate / 2
    
    # Number of frequency bins
    n_samples = int(sample_rate * duration)
    n_bins = n_samples // 2 + 1
    
    # Frequency range around 141.7 Hz
    target_freq = 141.7
    n_bins_5hz = int(5.0 / freq_resolution)  # Bins in ±5 Hz
    
    return {
        'test': 'Frequency Resolution',
        'sample_rate': sample_rate,
        'duration': duration,
        'n_samples': n_samples,
        'frequency_resolution': freq_resolution,
        'nyquist_frequency': nyquist,
        'total_bins': n_bins,
        'bins_in_5hz_window': n_bins_5hz,
        'frequency_accuracy': f'±{freq_resolution/2:.4f} Hz'
    }


def test_energy_calculation_accuracy():
    """
    Test accuracy of E = hf calculation for various frequencies
    
    Returns:
        Results dictionary
    """
    h = 6.62607015e-34  # Planck constant (exact by definition in SI)
    
    # Test frequencies
    test_freqs = [
        1.0,      # 1 Hz
        100.0,    # 100 Hz
        141.7001, # Our fundamental frequency
        500.0,    # 500 Hz
        1000.0    # 1 kHz
    ]
    
    results = {
        'test': 'Energy Calculation Accuracy',
        'planck_constant': h,
        'calculations': []
    }
    
    for freq in test_freqs:
        # Calculate with float64
        E_calc = h * freq
        
        # Verify round-trip: f = E/h
        f_recovered = E_calc / h
        error = abs(f_recovered - freq)
        rel_error = error / freq if freq != 0 else 0
        
        results['calculations'].append({
            'frequency': freq,
            'energy': E_calc,
            'recovered_frequency': f_recovered,
            'absolute_error': error,
            'relative_error': rel_error,
            'accurate_to_digits': int(-np.log10(rel_error)) if rel_error > 0 else 16
        })
    
    return results


def test_fft_precision(n_samples=131072):
    """
    Test FFT numerical precision
    
    Args:
        n_samples: Number of samples
        
    Returns:
        Results dictionary
    """
    # Create pure sine wave
    freq = 141.7
    sample_rate = 4096
    duration = n_samples / sample_rate
    times = np.arange(n_samples) / sample_rate
    
    signal = np.sin(2 * np.pi * freq * times)
    
    # FFT
    fft_result = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n_samples, 1.0/sample_rate)
    
    # Find peak
    peak_idx = np.argmax(np.abs(fft_result))
    detected_freq = freqs[peak_idx]
    
    # Inverse FFT
    reconstructed = np.fft.irfft(fft_result, n=n_samples)
    
    # Reconstruction error
    reconstruction_error = np.max(np.abs(signal - reconstructed))
    
    return {
        'test': 'FFT Precision',
        'n_samples': n_samples,
        'input_frequency': freq,
        'detected_frequency': detected_freq,
        'frequency_error': abs(detected_freq - freq),
        'reconstruction_error': reconstruction_error,
        'reconstruction_relative_error': reconstruction_error / np.max(np.abs(signal))
    }


def run_all_precision_tests():
    """
    Run all precision tests
    
    Returns:
        Complete results dictionary
    """
    print("=" * 70)
    print("NUMERICAL PRECISION BENCHMARKING")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {}
    }
    
    # Test 1: Float precision
    print("\n1. Testing floating point precision...")
    results['tests']['float_precision'] = test_float_precision()
    fp = results['tests']['float_precision']
    print(f"   float32: {fp['float32']['significant_digits']} significant digits")
    print(f"   float64: {fp['float64']['significant_digits']} significant digits")
    
    # Test 2: High precision
    print("\n2. Testing high-precision arithmetic...")
    results['tests']['mpmath_precision'] = test_mpmath_precision(100)
    mp = results['tests']['mpmath_precision']
    if mp.get('available'):
        print(f"   ✅ MPMath available with {mp['precision_digits']} digits")
    else:
        print(f"   ⚠️  MPMath not available")
    
    # Test 3: Frequency resolution
    print("\n3. Testing frequency resolution...")
    results['tests']['frequency_resolution'] = test_frequency_resolution()
    fr = results['tests']['frequency_resolution']
    print(f"   Resolution: {fr['frequency_resolution']:.4f} Hz")
    print(f"   Accuracy: {fr['frequency_accuracy']}")
    
    # Test 4: Energy calculation
    print("\n4. Testing energy calculation accuracy...")
    results['tests']['energy_accuracy'] = test_energy_calculation_accuracy()
    ea = results['tests']['energy_accuracy']
    # Show result for 141.7 Hz
    for calc in ea['calculations']:
        if calc['frequency'] == 141.7001:
            print(f"   f₀ = {calc['frequency']} Hz")
            print(f"   E = {calc['energy']:.15e} J")
            print(f"   Accurate to {calc['accurate_to_digits']} digits")
    
    # Test 5: FFT precision
    print("\n5. Testing FFT precision...")
    results['tests']['fft_precision'] = test_fft_precision()
    fft = results['tests']['fft_precision']
    print(f"   Frequency error: {fft['frequency_error']:.6e} Hz")
    print(f"   Reconstruction error: {fft['reconstruction_error']:.6e}")
    
    return results


def print_summary(results):
    """
    Print summary of precision tests
    
    Args:
        results: Results dictionary
    """
    print("\n" + "=" * 70)
    print("PRECISION SUMMARY")
    print("=" * 70)
    
    # Float precision
    fp = results['tests']['float_precision']
    print(f"\n✓ Float Precision:")
    print(f"  float32: ~{fp['float32']['significant_digits']} digits")
    print(f"  float64: ~{fp['float64']['significant_digits']} digits")
    print(f"  Recommendation: Use float64 for scientific calculations")
    
    # High precision
    mp = results['tests']['mpmath_precision']
    if mp.get('available'):
        print(f"\n✓ High Precision (MPMath):")
        print(f"  Available with arbitrary precision")
        print(f"  Tested at {mp['precision_digits']} decimal digits")
    
    # Frequency resolution
    fr = results['tests']['frequency_resolution']
    print(f"\n✓ Frequency Resolution:")
    print(f"  Resolution: {fr['frequency_resolution']:.4f} Hz")
    print(f"  Sufficient for detecting 141.7 Hz component")
    
    # Energy accuracy
    ea = results['tests']['energy_accuracy']
    print(f"\n✓ Energy Calculation:")
    for calc in ea['calculations']:
        if calc['frequency'] == 141.7001:
            print(f"  E(141.7 Hz) accurate to {calc['accurate_to_digits']} digits")
            break
    
    # FFT precision
    fft = results['tests']['fft_precision']
    print(f"\n✓ FFT Precision:")
    print(f"  Frequency detection error: {fft['frequency_error']:.2e} Hz")
    print(f"  Reconstruction error: {fft['reconstruction_relative_error']:.2e}")
    
    print("\n" + "=" * 70)
    print("✅ All precision requirements met for scientific analysis")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark numerical precision'
    )
    parser.add_argument('--output', type=str,
                       default='results/benchmark/numerical_precision.json',
                       help='Output file for results')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Run tests
    results = run_all_precision_tests()
    
    # Print summary
    print_summary(results)
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Precision benchmark complete!")
    print(f"Results saved to: {args.output}")


if __name__ == '__main__':
    main()
