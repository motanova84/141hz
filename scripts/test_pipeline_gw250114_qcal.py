#!/usr/bin/env python3
"""
Test script for pipeline_gw250114_qcal.py
Tests all components of the GW250114 QCAL analysis pipeline.
"""

import sys
import os
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pipeline_gw250114_qcal import (
    load_gw_data,
    generate_simulated_gw250114_data,
    bandpass_filter,
    normalize_strain,
    spectral_analysis,
    qcal_metric,
    noetic_field_projection,
    main_pipeline
)


def test_generate_simulated_data():
    """Test simulated data generation."""
    print("Testing simulated data generation...")
    
    fs = 4096
    duration = 32
    t, strain_h1, strain_l1 = generate_simulated_gw250114_data(fs=fs, duration=duration)
    
    # Check dimensions
    assert len(t) == len(strain_h1) == len(strain_l1)
    assert len(t) == int(fs * duration)
    
    # Check time array
    assert t[0] == 0
    assert abs(t[-1] - (duration - 1/fs)) < 1e-6
    
    # Check strain is not all zeros
    assert np.std(strain_h1) > 0
    assert np.std(strain_l1) > 0
    
    print("  ✅ Simulated data generation OK")


def test_bandpass_filter():
    """Test bandpass filtering."""
    print("Testing bandpass filter...")
    
    fs = 4096
    t = np.arange(0, 1, 1/fs)
    
    # Create test signal with multiple frequencies
    signal = (np.sin(2 * np.pi * 50 * t) +      # 50 Hz (should be filtered out)
              np.sin(2 * np.pi * 141.7 * t) +    # 141.7 Hz (should pass)
              np.sin(2 * np.pi * 200 * t))       # 200 Hz (should be filtered out)
    
    # Apply bandpass filter
    filtered = bandpass_filter(signal, fs, lowcut=130, highcut=150, order=4)
    
    # Check output is not all zeros
    assert np.std(filtered) > 0
    
    # Check filtered signal has same length
    assert len(filtered) == len(signal)
    
    print("  ✅ Bandpass filter OK")


def test_normalize_strain():
    """Test strain normalization."""
    print("Testing strain normalization...")
    
    # Create test data with known statistics
    data = np.random.normal(loc=100, scale=10, size=1000)
    
    normalized = normalize_strain(data)
    
    # Check output has same length
    assert len(normalized) == len(data)
    
    # Check normalization is reasonable (median ≈ 0)
    assert abs(np.median(normalized)) < 0.5
    
    print("  ✅ Strain normalization OK")


def test_spectral_analysis():
    """Test spectral analysis."""
    print("Testing spectral analysis...")
    
    fs = 4096
    duration = 4
    t = np.arange(0, duration, 1/fs)
    
    # Create signal with known frequency
    signal = np.sin(2 * np.pi * 141.7 * t)
    
    # Perform spectral analysis
    f, t_spec, mag, band_power = spectral_analysis(signal, fs, target_freq=141.7, df=0.5)
    
    # Check outputs
    assert len(f) > 0
    assert len(t_spec) > 0
    assert mag.shape == (len(f), len(t_spec))
    assert len(band_power) == len(t_spec)
    
    # Check frequency range
    assert np.min(f) >= 0
    assert np.max(f) <= fs / 2
    
    # Check that 141.7 Hz is in the frequency array
    assert np.min(np.abs(f - 141.7)) < 1.0  # Within 1 Hz
    
    print("  ✅ Spectral analysis OK")


def test_qcal_metric():
    """Test QCAL metric calculation."""
    print("Testing QCAL metric...")
    
    # Create test band power
    band_power = np.array([0.1, 0.5, 1.0, 0.8, 0.3])
    
    # Calculate QCAL metric
    Psi = qcal_metric(band_power, intensity=1.0, coherence=1.0)
    
    # Check output
    assert len(Psi) == len(band_power)
    assert np.all(Psi >= 0)  # Should be non-negative
    assert np.max(Psi) <= 1.0  # Should be <= 1 when intensity=coherence=1
    
    # Check that max occurs where band_power is max
    assert np.argmax(Psi) == np.argmax(band_power)
    
    print("  ✅ QCAL metric OK")


def test_noetic_field_projection():
    """Test noetic field projection."""
    print("Testing noetic field projection...")
    
    # Create test QCAL metric
    t_spec = np.linspace(0, 10, 100)
    Psi = np.sin(2 * np.pi * 0.1 * t_spec) ** 2  # Oscillating Psi
    
    # Calculate field metrics
    field_metrics = noetic_field_projection(Psi, t_spec)
    
    # Check required keys
    required_keys = ['Phi_mean', 'Phi_max', 'Phi_std', 'kappa_pi', 
                     'Lambda_C_inf', 'T_noetic_mean', 'coherence_level']
    for key in required_keys:
        assert key in field_metrics, f"Missing key: {key}"
    
    # Check values are reasonable
    assert field_metrics['Phi_mean'] >= 0
    assert field_metrics['Phi_max'] >= field_metrics['Phi_mean']
    assert field_metrics['kappa_pi'] > 0
    assert field_metrics['coherence_level'] in ['LOW', 'MODERATE', 'HIGH']
    
    print("  ✅ Noetic field projection OK")


def test_main_pipeline():
    """Test complete pipeline execution."""
    print("Testing complete pipeline...")
    
    # Run with simulated data
    output_dir = 'results/test_gw250114_qcal'
    results = main_pipeline(filename=None, fs=4096, output_dir=output_dir)
    
    # Check results structure
    assert 'metadata' in results
    assert 'detection' in results
    assert 'qcal_metric' in results
    assert 'noetic_field' in results
    assert 'output_files' in results
    
    # Check metadata
    assert results['metadata']['target_frequency'] == 141.7
    assert results['metadata']['sample_rate'] == 4096
    
    # Check detection results
    assert 'frequency_detected' in results['detection']
    assert 'resonance_detected' in results['detection']
    assert 'snr' in results['detection']
    
    # Check QCAL metrics
    assert 'Psi_max' in results['qcal_metric']
    assert 'Psi_mean' in results['qcal_metric']
    assert results['qcal_metric']['Psi_max'] >= 0
    
    # Check noetic field
    assert 'Phi_mean' in results['noetic_field']
    assert 'Lambda_C_inf' in results['noetic_field']
    
    # Check output files were created
    assert os.path.exists(results['output_files']['visualization'])
    assert os.path.exists(os.path.join(output_dir, 'analysis_results.json'))
    
    print("  ✅ Complete pipeline OK")


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("RUNNING TESTS FOR pipeline_gw250114_qcal.py")
    print("=" * 80)
    print()
    
    tests = [
        test_generate_simulated_data,
        test_bandpass_filter,
        test_normalize_strain,
        test_spectral_analysis,
        test_qcal_metric,
        test_noetic_field_projection,
        test_main_pipeline
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
