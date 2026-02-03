#!/usr/bin/env python3
"""
Validate environmental API integration with QCAL biological model.

This script verifies that the API clients integrate correctly with the
existing QCAL biological model framework.

Author: José Manuel Mota Burruezo
Date: January 31, 2026
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np


def test_api_client_imports():
    """Test that API clients can be imported."""
    print("Testing API client imports...")
    try:
        from modules.quantum_biology.apis import NOAAClient, NASAPowerClient
        print("  ✓ Successfully imported NOAAClient")
        print("  ✓ Successfully imported NASAPowerClient")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_integration_imports():
    """Test that integration functions can be imported."""
    print("\nTesting integration function imports...")
    try:
        from modules.quantum_biology.environmental_integration import (
            create_environmental_cycles_from_nasa_power,
            create_environmental_cycles_from_noaa,
            get_multi_location_environmental_data
        )
        print("  ✓ Successfully imported integration functions")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_nasa_power_client_initialization():
    """Test NASA POWER client can be initialized."""
    print("\nTesting NASA POWER client initialization...")
    try:
        from modules.quantum_biology.apis import NASAPowerClient
        client = NASAPowerClient()
        print("  ✓ NASA POWER client initialized successfully")
        print(f"  ✓ Base URL: {client.BASE_URL}")
        return True
    except Exception as e:
        print(f"  ✗ Initialization failed: {e}")
        return False


def test_noaa_client_error_handling():
    """Test NOAA client error handling without token."""
    print("\nTesting NOAA client error handling...")
    try:
        from modules.quantum_biology.apis import NOAAClient
        
        # Clear token if set
        old_token = os.environ.get("NOAA_API_TOKEN")
        if old_token:
            del os.environ["NOAA_API_TOKEN"]
        
        try:
            client = NOAAClient()
            print("  ✗ Expected ValueError but client initialized")
            result = False
        except ValueError as e:
            if "NOAA API token required" in str(e):
                print("  ✓ Correctly raises ValueError without token")
                print(f"  ✓ Error message: {str(e)[:60]}...")
                result = True
            else:
                print(f"  ✗ Wrong error message: {e}")
                result = False
        
        # Restore token
        if old_token:
            os.environ["NOAA_API_TOKEN"] = old_token
        
        return result
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_data_format():
    """Test that synthetic fallback data has correct format."""
    print("\nTesting data format compatibility...")
    try:
        # Import original function for comparison
        from modules.quantum_biology.core.qcal_biological_model import (
            create_environmental_cycles
        )
        
        # Test original function
        time, signal = create_environmental_cycles(duration_years=1, dt_hours=24)
        
        print(f"  ✓ Synthetic data shape: {time.shape}, {signal.shape}")
        print(f"  ✓ Time range: {time[0]:.0f} to {time[-1]:.0f} seconds")
        print(f"  ✓ Signal range: [{signal.min():.3f}, {signal.max():.3f}]")
        
        # Verify expected format
        assert isinstance(time, np.ndarray), "Time must be numpy array"
        assert isinstance(signal, np.ndarray), "Signal must be numpy array"
        assert len(time) == len(signal), "Time and signal must have same length"
        assert time[0] == 0, "Time should start at 0"
        
        print("  ✓ Data format is compatible with QCAL model")
        return True
    except Exception as e:
        print(f"  ✗ Format test failed: {e}")
        return False


def test_spectral_field_integration():
    """Test integration with SpectralField class."""
    print("\nTesting SpectralField integration...")
    try:
        from modules.quantum_biology.core.qcal_biological_model import (
            create_environmental_cycles, SpectralField
        )
        
        # Generate synthetic data
        time, signal = create_environmental_cycles(duration_years=1)
        
        # Create spectral field
        field = SpectralField.from_environmental_data(time, signal, n_components=5)
        
        print(f"  ✓ Created SpectralField with {len(field.frequencies)} components")
        print(f"  ✓ Frequency range: {field.frequencies.min():.6f} to {field.frequencies.max():.6f} rad/s")
        
        # Check that field can be evaluated
        test_time = np.linspace(0, 3600, 10)
        field_values = field.evaluate(test_time)
        
        print(f"  ✓ Field evaluated at {len(test_time)} points")
        print(f"  ✓ Field is complex: {np.iscomplexobj(field_values)}")
        
        return True
    except Exception as e:
        print(f"  ✗ Integration test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("=" * 70)
    print("Environmental API Integration Validation")
    print("=" * 70)
    print()
    
    tests = [
        test_api_client_imports,
        test_integration_imports,
        test_nasa_power_client_initialization,
        test_noaa_client_error_handling,
        test_data_format,
        test_spectral_field_integration,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 70)
    print("Validation Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All validation tests passed!")
        print("\nNext steps:")
        print("  1. Set NOAA_API_TOKEN environment variable (optional)")
        print("  2. Run: python examples/nasa_power_example.py")
        print("  3. Use API clients in your QCAL biological model code")
        print("\nSee: docs/ENVIRONMENTAL_APIS_README.md for detailed usage")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        print("\nPlease review the errors above and ensure all dependencies are installed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
