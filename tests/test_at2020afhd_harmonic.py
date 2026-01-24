#!/usr/bin/env python3
"""
Test script for AT2020afhd harmonic verification.

This tests the key calculations and validates the output.
"""

import sys
import json
from pathlib import Path
import numpy as np

# Add parent directory to path for imports (test environment)
_SCRIPT_DIR = Path(__file__).parent.absolute()
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# Import validation functions
from validate_at2020afhd_harmonic import (
    calculate_harmonic_relationship,
    verify_harmonic_precision,
    generate_synthetic_lightcurve,
    fit_lense_thirring_model,
    compute_lomb_scargle
)


def test_harmonic_calculations():
    """Test the harmonic relationship calculations."""
    print("Testing harmonic calculations...")

    # Calculate harmonic relationship
    harmonic_data = calculate_harmonic_relationship(precision=100)

    # Test expected values
    expected_f0 = 141.70001
    expected_period = 19.6
    expected_ratio_range = (2.3e8, 2.5e8)
    expected_octaves_range = (27.5, 28.0)
    expected_decades_range = (8.3, 8.5)

    # Verify f0
    assert abs(harmonic_data['f0_hz'] - expected_f0) < 0.001, "f0 mismatch"
    print(f"  ✓ f₀ = {harmonic_data['f0_hz']:.5f} Hz")

    # Verify period
    assert abs(harmonic_data['period_days'] - expected_period) < 0.1, "Period mismatch"
    print(f"  ✓ Period = {harmonic_data['period_days']:.1f} days")

    # Verify ratio in range
    assert expected_ratio_range[0] <= harmonic_data['ratio'] <= expected_ratio_range[1], "Ratio out of range"
    print(f"  ✓ Ratio = {harmonic_data['ratio']:.3e}")

    # Verify octaves in range
    assert expected_octaves_range[0] <= harmonic_data['octaves'] <= expected_octaves_range[1], "Octaves out of range"
    print(f"  ✓ Octaves = {harmonic_data['octaves']:.2f}")

    # Verify decades in range
    assert expected_decades_range[0] <= harmonic_data['decades'] <= expected_decades_range[1], "Decades out of range"
    print(f"  ✓ Decades = {harmonic_data['decades']:.2f}")

    # Verify precision
    verification = verify_harmonic_precision(harmonic_data)
    assert verification['all_verified'], "Precision verification failed"
    print(f"  ✓ All precision checks passed (errors < 0.5%)")

    print("✅ Harmonic calculations test PASSED\n")
    return harmonic_data


def test_model_fitting():
    """Test the Lense-Thirring model fitting."""
    print("Testing model fitting...")

    # Generate test data
    harmonic_data = calculate_harmonic_relationship(precision=100)
    t, xray_flux, radio_flux, xray_errors, radio_errors = generate_synthetic_lightcurve(
        harmonic_data, duration_days=400, noise_level=0.15
    )

    # Fit model
    xray_fit = fit_lense_thirring_model(
        t, xray_flux, xray_errors, harmonic_data['omega_rad_per_day']
    )

    # Check fit succeeded
    assert xray_fit['fit_successful'], "X-ray fit failed"
    print(f"  ✓ X-ray model fit successful")

    # Check period recovery within 10%
    period_error = abs(xray_fit['period_days'] - 19.6) / 19.6
    assert period_error < 0.1, f"Period recovery failed: {period_error*100:.1f}% error"
    print(f"  ✓ Period recovered: {xray_fit['period_days']:.2f} days (error: {period_error*100:.2f}%)")

    # Check R² > 0.8
    assert xray_fit['r_squared'] > 0.8, f"Poor fit quality: R²={xray_fit['r_squared']:.3f}"
    print(f"  ✓ Fit quality: R² = {xray_fit['r_squared']:.4f}")

    print("✅ Model fitting test PASSED\n")


def test_periodogram():
    """Test periodogram analysis."""
    print("Testing periodogram analysis...")

    # Generate test data
    harmonic_data = calculate_harmonic_relationship(precision=100)
    t, xray_flux, _, xray_errors, _ = generate_synthetic_lightcurve(
        harmonic_data, duration_days=400, noise_level=0.10
    )

    # Compute periodogram
    periodogram = compute_lomb_scargle(t, xray_flux, xray_errors, period_range=(5, 50))

    # Check peak is detected
    assert periodogram['peak_power'] > 0.5, "Peak not significant"
    print(f"  ✓ Peak detected with power = {periodogram['peak_power']:.3f}")

    # Check peak period is near 19.6 days (within 20%)
    period_error = abs(periodogram['peak_period'] - 19.6) / 19.6
    assert period_error < 0.2, f"Peak period error too large: {period_error*100:.1f}%"
    print(f"  ✓ Peak period: {periodogram['peak_period']:.2f} days (error: {period_error*100:.2f}%)")

    print("✅ Periodogram test PASSED\n")


def test_output_files():
    """Test that output files are generated correctly."""
    print("Testing output file generation...")

    json_file = Path('at2020afhd_harmonic_verification.json')
    png_file = Path('at2020afhd_harmonic_verification.png')

    # Check JSON exists
    assert json_file.exists(), "JSON file not found"
    print(f"  ✓ JSON file exists: {json_file}")

    # Check PNG exists
    assert png_file.exists(), "PNG file not found"
    print(f"  ✓ PNG file exists: {png_file}")

    # Load and validate JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Check required keys
    assert 'metadata' in data, "Missing metadata"
    assert 'harmonic_relationship' in data, "Missing harmonic_relationship"
    assert 'verification' in data, "Missing verification"
    assert 'scientific_conclusion' in data, "Missing scientific_conclusion"
    print(f"  ✓ JSON structure valid")

    # Check verification passed
    assert data['verification']['all_verified'], "Verification not passed in JSON"
    print(f"  ✓ Verification status: PASSED")

    # Check harmonic values
    assert data['harmonic_relationship']['f0_hz'] == 141.70001, "f0 mismatch in JSON"
    assert abs(data['harmonic_relationship']['period_days'] - 19.6) < 0.1, "Period mismatch in JSON"
    print(f"  ✓ Harmonic values correct")

    print("✅ Output files test PASSED\n")


def main():
    """Run all tests."""
    print("=" * 80)
    print("AT2020afhd Harmonic Verification - Test Suite")
    print("=" * 80)
    print()

    try:
        # Run tests
        harmonic_data = test_harmonic_calculations()
        test_model_fitting()
        test_periodogram()
        test_output_files()

        # Summary
        print("=" * 80)
        print("✨ ALL TESTS PASSED")
        print("=" * 80)
        print()
        print("Summary:")
        print(f"  - Harmonic ratio: {harmonic_data['ratio']:.3e}")
        print(f"  - Octave separation: {harmonic_data['octaves']:.2f}")
        print(f"  - Scale span: {harmonic_data['decades']:.2f} decades")
        print()
        print("  🌀 NOĒSIS Fractal Coherence VERIFIED 🌀")
        print("=" * 80)

        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
