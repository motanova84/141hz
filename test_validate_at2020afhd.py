#!/usr/bin/env python3
"""
Test script for AT2020afhd validation
"""

import os
import sys
import tempfile
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import validation functions
from validate_at2020afhd import (
    calculate_harmonic_cascade,
    find_period_from_lsp,
    fit_psi_model,
    F0_QCAL,
    PUBLISHED_PERIOD,
    EXPECTED_OCTAVES
)


def test_harmonic_cascade():
    """Test harmonic cascade calculation."""
    print("Testing harmonic cascade calculation...")
    
    # Test with expected period
    cascade = calculate_harmonic_cascade(PUBLISHED_PERIOD)
    
    assert 'f_frame_hz' in cascade
    assert 'ratio' in cascade
    assert 'octaves' in cascade
    
    # Check octaves is close to expected
    assert abs(cascade['octaves'] - EXPECTED_OCTAVES) < 0.01
    
    # Check error is small (< 1%)
    assert cascade['error_ratio'] < 1.0
    
    print(f"  ✓ Octaves: {cascade['octaves']:.3f} (expected: {EXPECTED_OCTAVES})")
    print(f"  ✓ Error: {cascade['error_ratio']:.3f}%")


def test_period_detection():
    """Test period detection from LSP."""
    print("\nTesting period detection...")
    
    # Generate mock LSP with peak at 19.6 days
    period = np.linspace(10, 40, 1000)
    peak_period = 19.6
    sigma = 0.5
    power = 100 * np.exp(-0.5 * ((period - peak_period) / sigma)**2)
    power += np.random.normal(0, 2, len(period))
    power = np.maximum(power, 0)
    
    # Detect period
    detected, max_power = find_period_from_lsp(period, power)
    
    # Should be within 1% of expected
    error_percent = abs(detected - peak_period) / peak_period * 100
    assert error_percent < 1.0
    
    print(f"  ✓ Detected: {detected:.3f} days (expected: {peak_period})")
    print(f"  ✓ Error: {error_percent:.3f}%")


def test_psi_model_fit():
    """Test Ψ model fitting."""
    print("\nTesting Ψ model fit...")
    
    # Generate mock sinusoidal data
    t = np.linspace(0, 200, 100)
    period = 19.6
    omega = 2 * np.pi / period
    amplitude = 0.1
    phase = 1.5
    offset = 1.0
    
    # Generate data
    flux = offset + amplitude * np.sin(omega * t + phase)
    flux += np.random.normal(0, 0.01, len(t))
    error = np.full(len(t), 0.01)
    
    # Fit model
    fit_result = fit_psi_model(t, flux, error, period)
    
    assert fit_result['success']
    assert fit_result['r_squared'] > 0.7
    
    # Period should be close
    period_error = abs(fit_result['period'] - period) / period * 100
    assert period_error < 10
    
    print(f"  ✓ Fitted period: {fit_result['period']:.2f} days")
    print(f"  ✓ R²: {fit_result['r_squared']:.3f}")
    print(f"  ✓ χ²_red: {fit_result['chi2_red']:.2f}")


def test_constants():
    """Test that constants are correct."""
    print("\nTesting constants...")
    
    assert F0_QCAL == 141.70001
    assert PUBLISHED_PERIOD == 19.6
    assert EXPECTED_OCTAVES == 27.84
    
    print(f"  ✓ f₀ = {F0_QCAL} Hz")
    print(f"  ✓ Published period = {PUBLISHED_PERIOD} days")
    print(f"  ✓ Expected octaves = {EXPECTED_OCTAVES}")


def test_full_workflow():
    """Test full workflow with mock data."""
    print("\nTesting full workflow...")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "at2020afhd"
        data_dir.mkdir()
        
        # Generate mock LSP
        period = np.linspace(10, 40, 1000)
        peak_period = 19.6
        sigma = 0.5
        power = 100 * np.exp(-0.5 * ((period - peak_period) / sigma)**2)
        power += np.random.normal(0, 3, len(period))
        power = np.maximum(power, 0)
        np.savetxt(data_dir / "LSP.txt", np.column_stack([period, power]))
        
        # Generate mock X-ray
        t = np.linspace(0, 200, 85)
        omega = 2 * np.pi / 19.6
        flux = 1.0 + 0.05 * np.sin(omega * t + 1.5)
        flux += np.random.normal(0, 0.01, len(t))
        error = np.full(len(t), 0.01)
        np.savetxt(data_dir / "data_lc_NEW_gti.txt", np.column_stack([t, flux, error]))
        
        # Generate mock Radio
        t = np.linspace(0, 200, 45)
        flux = 1.0 + 0.4 * np.sin(omega * t + 3.0)
        flux += np.random.normal(0, 0.05, len(t))
        error = np.full(len(t), 0.05)
        np.savetxt(data_dir / "all_radio_lc.txt", np.column_stack([t, flux, error]))
        
        print(f"  ✓ Created mock data in {data_dir}")
        
        # Load and test
        from validate_at2020afhd import load_lsp_data, load_light_curves
        
        period, power = load_lsp_data(str(data_dir))
        assert period is not None
        assert len(period) == 1000
        
        xray_data, radio_data = load_light_curves(str(data_dir))
        assert xray_data[0] is not None
        assert radio_data[0] is not None
        assert len(xray_data[0]) == 85
        assert len(radio_data[0]) == 45
        
        print(f"  ✓ Loaded mock data successfully")


def main():
    """Run all tests."""
    print("=" * 70)
    print("AT2020afhd Validation Tests")
    print("=" * 70)
    
    try:
        test_constants()
        test_harmonic_cascade()
        test_period_detection()
        test_psi_model_fit()
        test_full_workflow()
        
        print("\n" + "=" * 70)
        print("✅ All tests PASSED")
        print("=" * 70)
        return 0
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Test FAILED: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
