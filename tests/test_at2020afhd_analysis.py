#!/usr/bin/env python3
"""
Test script for AT2020afhd analysis
Validates that the analysis pipeline works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.analyze_at2020afhd import (
    calculate_harmonic_ratio,
    lomb_scargle_analysis,
)
from qcal.constants import (
    F0_HZ, 
    EXPECTED_RATIO, 
    TEST_PERIOD_MIN_DAYS, 
    TEST_PERIOD_MAX_DAYS,
    TEST_OCTAVES_MIN,
    TEST_OCTAVES_MAX
)
import numpy as np


def test_harmonic_ratio():
    """Test harmonic ratio calculation"""
    print("Testing harmonic ratio calculation...")
    
    # Expected values
    period_days = 19.6
    expected_octaves = 27.84
    
    result = calculate_harmonic_ratio(F0_HZ, period_days)
    
    # Check octaves
    assert abs(result['octaves'] - expected_octaves) < 0.1, \
        f"Octaves mismatch: {result['octaves']} vs {expected_octaves}"
    
    # Check error is small
    assert result['error_percent'] < 1.0, \
        f"Error too large: {result['error_percent']}%"
    
    print(f"✅ Harmonic ratio test passed")
    print(f"   Octaves: {result['octaves']:.3f}")
    print(f"   Error: {result['error_percent']:.2f}%\n")


def test_lomb_scargle():
    """Test Lomb-Scargle analysis"""
    print("Testing Lomb-Scargle periodogram...")
    
    # Generate synthetic data with known period
    np.random.seed(42)
    time_mjd = np.linspace(58900, 59250, 85)
    period_true = 19.6
    flux = 0.0047 + 0.0007 * np.sin(2*np.pi*(time_mjd - time_mjd[0])/period_true)
    flux += np.random.normal(0, 0.0001, len(time_mjd))
    flux_err = np.full(len(time_mjd), 0.0001)
    
    # Analyze
    freq, power, period_detected = lomb_scargle_analysis(time_mjd, flux, flux_err)
    
    # Check period detection
    assert abs(period_detected - period_true) < 0.5, \
        f"Period detection failed: {period_detected} vs {period_true}"
    
    print(f"✅ Lomb-Scargle test passed")
    print(f"   Expected period: {period_true} days")
    print(f"   Detected period: {period_detected:.3f} days\n")


def test_constants():
    """Test that QCAL constants are defined correctly"""
    print("Testing QCAL constants...")
    
    # Check f₀
    assert F0_HZ == 141.70001, f"f₀ incorrect: {F0_HZ}"
    
    # Check it's in reasonable range
    assert 100 < F0_HZ < 200, f"f₀ out of range: {F0_HZ}"
    
    print(f"✅ Constants test passed")
    print(f"   f₀ = {F0_HZ} Hz\n")


def test_full_pipeline():
    """Test complete analysis pipeline"""
    print("Testing full analysis pipeline...")
    
    # Generate data
    np.random.seed(42)
    time_mjd = np.linspace(58900, 59250, 85)
    time_days = time_mjd - time_mjd[0]
    flux = (0.0047 + 
            0.0007 * np.sin(2*np.pi*time_days/19.6) +
            np.random.normal(0, 0.0002, len(time_days)))
    flux_err = np.full(len(time_days), 0.0002)
    
    # Run analysis
    freq, power, period_ls = lomb_scargle_analysis(time_mjd, flux, flux_err)
    harmonic_data = calculate_harmonic_ratio(F0_HZ, period_ls)
    
    # Verify results using constants
    assert TEST_PERIOD_MIN_DAYS < period_ls < TEST_PERIOD_MAX_DAYS, \
        f"Period out of range: {period_ls}"
    assert TEST_OCTAVES_MIN < harmonic_data['octaves'] < TEST_OCTAVES_MAX, \
        f"Octaves out of range: {harmonic_data['octaves']}"
    
    print(f"✅ Full pipeline test passed")
    print(f"   Period: {period_ls:.3f} days")
    print(f"   Octaves: {harmonic_data['octaves']:.3f}")
    print(f"   Error: {harmonic_data['error_percent']:.2f}%\n")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AT2020afhd ANALYSIS TEST SUITE")
    print("="*60 + "\n")
    
    try:
        test_constants()
        test_harmonic_ratio()
        test_lomb_scargle()
        test_full_pipeline()
        
        print("="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
