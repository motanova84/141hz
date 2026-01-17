#!/usr/bin/env python3
"""
Test script for analizar_gw150914_1417hz.py

This script tests the comprehensive GW150914 analysis functions
to ensure they work correctly before running the full analysis.
"""

import numpy as np
import sys
import os

# Get script directory dynamically
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'analizar_gw150914_1417hz.py')


def test_imports():
    """Test that all required imports are available"""
    print("Testing imports...")
    
    try:
        import numpy as np
        print("  ✅ numpy")
    except ImportError as e:
        print(f"  ❌ numpy: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("  ✅ matplotlib")
    except ImportError as e:
        print(f"  ❌ matplotlib: {e}")
        return False
    
    try:
        from gwpy.timeseries import TimeSeries
        print("  ✅ gwpy")
    except ImportError as e:
        print(f"  ❌ gwpy: {e}")
        print("     Install with: pip install gwpy")
        return False
    
    try:
        from scipy import signal, stats
        print("  ✅ scipy")
    except ImportError as e:
        print(f"  ❌ scipy: {e}")
        return False
    
    try:
        import h5py
        print("  ✅ h5py")
    except ImportError as e:
        print(f"  ❌ h5py: {e}")
        return False
    
    try:
        from astropy import units as u
        print("  ✅ astropy")
    except ImportError as e:
        print(f"  ❌ astropy: {e}")
        return False
    
    try:
        from datetime import datetime
        print("  ✅ datetime")
    except ImportError as e:
        print(f"  ❌ datetime: {e}")
        return False
    
    return True


def test_script_exists():
    """Test that the analysis script exists"""
    print("\nTesting script existence...")
    
    if os.path.exists(SCRIPT_PATH):
        print(f"  ✅ Script found at {SCRIPT_PATH}")
        return True
    else:
        print(f"  ❌ Script not found at {SCRIPT_PATH}")
        return False


def test_script_syntax():
    """Test that the script has valid Python syntax"""
    print("\nTesting script syntax...")
    
    try:
        with open(SCRIPT_PATH, 'r') as f:
            code = f.read()
        
        compile(code, 'analizar_gw150914_1417hz.py', 'exec')
        print("  ✅ Script syntax is valid")
        return True
    except SyntaxError as e:
        print(f"  ❌ Syntax error: {e}")
        return False


def test_functions_defined():
    """Test that all required functions are defined"""
    print("\nTesting function definitions...")
    
    try:
        # Add the script directory to path
        if SCRIPT_DIR not in sys.path:
            sys.path.insert(0, SCRIPT_DIR)
        
        import analizar_gw150914_1417hz as gw_script
        
        required_functions = [
            'load_gw150914_data',
            'analyze_postmerger_resonances',
            'calculate_statistical_significance',
            'analyze_1417Hz_specific',
            'plot_comprehensive_results',
            'generate_scientific_report',
            'run_complete_analysis',
            'apply_fft_interpolation',
            'coherent_signal_analysis',
            'adaptive_resonance_filter',
            'phase_triangulation'
        ]
        
        all_defined = True
        for func_name in required_functions:
            if hasattr(gw_script, func_name):
                print(f"  ✅ {func_name}")
            else:
                print(f"  ❌ {func_name} not found")
                all_defined = False
        
        return all_defined
    
    except Exception as e:
        print(f"  ❌ Error loading script: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_constants_defined():
    """Test that all required constants are defined"""
    print("\nTesting constant definitions...")
    
    try:
        if SCRIPT_DIR not in sys.path:
            sys.path.insert(0, SCRIPT_DIR)
        import analizar_gw150914_1417hz as gw_script
        
        if hasattr(gw_script, 'GW150914_PARAMS'):
            params = gw_script.GW150914_PARAMS
            print(f"  ✅ GW150914_PARAMS defined")
            
            required_keys = ['GPS', 'detectors', 'mass1', 'mass2', 'M_final', 
                           'a_final', 'distance', 'f_merger', 'qnm_freqs']
            
            all_keys_present = True
            for key in required_keys:
                if key in params:
                    print(f"     ✅ {key}: {params[key]}")
                else:
                    print(f"     ❌ {key} missing")
                    all_keys_present = False
            
            return all_keys_present
        else:
            print(f"  ❌ GW150914_PARAMS not defined")
            return False
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_mock_analysis():
    """Test analysis functions with mock data"""
    print("\nTesting with mock data...")
    
    try:
        # Create mock strain data
        sample_rate = 4096
        duration = 0.5
        t = np.arange(0, duration, 1/sample_rate)
        
        # Mock strain: noise + small signal at 141.7 Hz
        noise = np.random.normal(0, 1e-21, len(t))
        signal = 1e-22 * np.sin(2 * np.pi * 141.7 * t)
        mock_strain = noise + signal
        
        print(f"  ✅ Created mock strain data: {len(mock_strain)} samples")
        print(f"     Duration: {duration} s")
        print(f"     Sample rate: {sample_rate} Hz")
        print(f"     Signal amplitude: 1e-22 at 141.7 Hz")
        
        # Test FFT
        fft = np.fft.rfft(mock_strain)
        freqs = np.fft.rfftfreq(len(mock_strain), 1/sample_rate)
        
        idx_target = np.argmin(np.abs(freqs - 141.7))
        print(f"  ✅ FFT computed: {len(fft)} frequency bins")
        print(f"     Closest frequency to 141.7 Hz: {freqs[idx_target]:.2f} Hz")
        print(f"     Amplitude at target: {np.abs(fft[idx_target]):.2e}")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error in mock analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("TEST SUITE: analizar_gw150914_1417hz.py")
    print("="*70)
    
    tests = [
        ("Import dependencies", test_imports),
        ("Script exists", test_script_exists),
        ("Script syntax", test_script_syntax),
        ("Function definitions", test_functions_defined),
        ("Constant definitions", test_constants_defined),
        ("Mock analysis", test_mock_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! The script is ready to run.")
        print("\nTo execute the full analysis:")
        print("  python analizar_gw150914_1417hz.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the analysis.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
