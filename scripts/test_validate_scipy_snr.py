#!/usr/bin/env python3
"""
Test for validate_scipy_snr_141hz.py
Tests the scipy-based filtering and SNR calculation functions.
"""

import sys
import numpy as np

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False

# Add scripts directory to path
sys.path.insert(0, 'scripts')

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location("validate_scipy_snr_141hz",
                                               "scripts/validate_scipy_snr_141hz.py")
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)


def test_butter_filter_safe_highpass():
    """Test Butterworth highpass filter."""
    fs = 4096
    test_signal = np.random.randn(fs * 4)
    filtered = validate_module.butter_filter_safe(test_signal, fs, 20, btype='highpass')
    assert filtered.shape == test_signal.shape
    assert not np.all(filtered == test_signal)  # Should be different


def test_butter_filter_safe_bandpass():
    """Test Butterworth bandpass filter."""
    fs = 4096
    test_signal = np.random.randn(fs * 4)
    filtered = validate_module.butter_filter_safe(test_signal, fs, 140.7, 142.7, btype='bandpass')
    assert filtered.shape == test_signal.shape
    assert not np.all(filtered == test_signal)


def test_butter_filter_safe_invalid_type():
    """Test that invalid filter type raises error."""
    if not HAS_PYTEST:
        return  # Skip this test without pytest
    fs = 4096
    test_signal = np.random.randn(fs * 4)
    with pytest.raises(ValueError):
        validate_module.butter_filter_safe(test_signal, fs, 20, btype='lowpass')


def test_scipy_notch():
    """Test notch filter for power line harmonics."""
    fs = 4096
    test_signal = np.random.randn(fs * 4)
    filtered = validate_module.scipy_notch(test_signal, fs)
    assert filtered.shape == test_signal.shape


def test_simple_detrend_taper():
    """Test detrending and tapering."""
    test_signal = np.random.randn(1000)
    processed = validate_module.simple_detrend_taper(test_signal)
    assert processed.shape == test_signal.shape
    # After tapering, edges should be attenuated
    assert abs(processed[0]) < abs(test_signal[0]) or abs(processed[-1]) < abs(test_signal[-1])


def test_calculate_snr():
    """Test SNR calculation."""
    fs = 4096
    dur = 32
    gps_center = 1126259462
    test_signal = np.random.randn(fs * dur)
    snr_t, noise_rms = validate_module.calculate_snr(test_signal, fs, gps_center, dur)
    assert isinstance(snr_t, float)
    assert isinstance(noise_rms, float)
    assert snr_t >= 0
    assert noise_rms >= 0


def test_calculate_snr_with_signal():
    """Test SNR calculation with injected signal."""
    fs = 4096
    dur = 32
    gps_center = 1126259462

    # Create noise
    test_signal = np.random.randn(fs * dur) * 0.01

    # Create time array
    t = np.linspace(gps_center - dur/2, gps_center + dur/2, len(test_signal))

    # Inject a signal at the center
    signal_mask = (t >= gps_center - 1) & (t <= gps_center + 1)
    test_signal[signal_mask] += 0.1 * np.sin(2 * np.pi * 141.7 * (t[signal_mask] - gps_center))

    snr_t, noise_rms = validate_module.calculate_snr(test_signal, fs, gps_center, dur)
    assert snr_t > 1.0  # Should detect the injected signal


def test_events_dict():
    """Test that EVENTS dictionary is properly defined."""
    assert hasattr(validate_module, 'EVENTS')
    assert len(validate_module.EVENTS) == 9
    assert "GW150914" in validate_module.EVENTS
    assert "GW170817" in validate_module.EVENTS


def test_detector_list():
    """Test that detector list is properly defined."""
    assert hasattr(validate_module, 'DET_LIST')
    assert "H1" in validate_module.DET_LIST
    assert "L1" in validate_module.DET_LIST


if __name__ == "__main__":
    # Run tests manually if pytest not available
    print("Running manual tests...")
    test_butter_filter_safe_highpass()
    print("✓ test_butter_filter_safe_highpass passed")

    test_butter_filter_safe_bandpass()
    print("✓ test_butter_filter_safe_bandpass passed")

    test_scipy_notch()
    print("✓ test_scipy_notch passed")

    test_simple_detrend_taper()
    print("✓ test_simple_detrend_taper passed")

    test_calculate_snr()
    print("✓ test_calculate_snr passed")

    test_calculate_snr_with_signal()
    print("✓ test_calculate_snr_with_signal passed")

    test_events_dict()
    print("✓ test_events_dict passed")

    test_detector_list()
    print("✓ test_detector_list passed")

    print("\n✅ All tests passed!")
