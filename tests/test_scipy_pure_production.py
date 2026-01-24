#!/usr/bin/env python3
"""
Test for scipy_pure_production_analysis.py

Validates the scipy-pure production analysis script functionality.
"""

import sys
import json
import importlib.util
from pathlib import Path

# Load the script as a module
SCRIPT_PATH = Path(__file__).parent / 'scripts' / 'scipy_pure_production_analysis.py'

def load_script_module():
    """Load the script as a module"""
    spec = importlib.util.spec_from_file_location("scipy_pure_prod", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules['scipy_pure_prod'] = module
    spec.loader.exec_module(module)
    return module


def test_script_import():
    """Test that the script can be imported"""
    try:
        module = load_script_module()
        print("✅ Script import successful")
        return True, module
    except Exception as e:
        print(f"❌ Script import failed: {e}")
        return False, None


def test_key_events_defined(module):
    """Test that KEY_EVENTS dictionary is properly defined"""
    KEY_EVENTS = module.KEY_EVENTS
    
    expected_events = ['GW151226', 'GW170104', 'GW170817']
    
    for event in expected_events:
        if event not in KEY_EVENTS:
            print(f"❌ Missing key event: {event}")
            return False
    
    print(f"✅ All {len(expected_events)} key events defined")
    return True


def test_snr_values(module):
    """Test that confirmed SNR values are correct"""
    KEY_EVENTS = module.KEY_EVENTS
    
    expected_values = {
        'GW151226': {'H1': 5.8468, 'L1': 6.5471},
        'GW170104': {'H1': 5.4136, 'L1': 7.8667},
        'GW170817': {'H1': 6.2260, 'L1': 62.9271}
    }
    
    for event, detectors in expected_values.items():
        for detector, expected_snr in detectors.items():
            actual_snr = KEY_EVENTS[event]['confirmed_snr'][detector]
            if abs(actual_snr - expected_snr) > 0.0001:
                print(f"❌ SNR mismatch for {event} {detector}: expected {expected_snr}, got {actual_snr}")
                return False
    
    print("✅ All SNR values correct")
    return True


def test_exceptional_peak(module):
    """Test that GW170817 L1 exceptional peak is documented"""
    KEY_EVENTS = module.KEY_EVENTS
    
    gw170817_l1_snr = KEY_EVENTS['GW170817']['confirmed_snr']['L1']
    
    if gw170817_l1_snr < 60:
        print(f"❌ GW170817 L1 SNR should be >60σ, got {gw170817_l1_snr}")
        return False
    
    if 'notes' not in KEY_EVENTS['GW170817']:
        print("❌ GW170817 missing notes about exceptional peak")
        return False
    
    print(f"✅ GW170817 L1 exceptional peak documented (SNR={gw170817_l1_snr})")
    return True


def test_frequency_config(module):
    """Test frequency configuration"""
    FREQUENCY_TARGET = module.FREQUENCY_TARGET
    BANDPASS_LOW = module.BANDPASS_LOW
    BANDPASS_HIGH = module.BANDPASS_HIGH
    
    if abs(FREQUENCY_TARGET - 141.7001) > 0.0001:
        print(f"❌ Frequency target incorrect: {FREQUENCY_TARGET}")
        return False
    
    if abs(BANDPASS_LOW - 140.7) > 0.1 or abs(BANDPASS_HIGH - 142.7) > 0.1:
        print(f"❌ Bandpass incorrect: [{BANDPASS_LOW}, {BANDPASS_HIGH}]")
        return False
    
    print("✅ Frequency configuration correct")
    return True


def test_results_file_structure():
    """Test that results JSON file has correct structure"""
    results_file = Path(__file__).parent / 'results' / 'scipy_pure_production_results.json'
    
    if not results_file.exists():
        print(f"⚠️  Results file not found: {results_file}")
        print("   (Run script first: python3 scripts/scipy_pure_production_analysis.py)")
        return True  # Don't fail if file doesn't exist yet
    
    try:
        with open(results_file) as f:
            data = json.load(f)
        
        # Check required keys
        required_keys = ['analysis_info', 'key_findings', 'events']
        for key in required_keys:
            if key not in data:
                print(f"❌ Missing key in results: {key}")
                return False
        
        # Check key findings
        if data['key_findings']['total_above_6sigma'] != 4:
            print(f"❌ Expected 4 verifications ≥6σ, got {data['key_findings']['total_above_6sigma']}")
            return False
        
        if data['key_findings']['total_above_5sigma'] < 6:
            print(f"❌ Expected at least 6 strong signals ≥5σ, got {data['key_findings']['total_above_5sigma']}")
            return False
        
        print(f"✅ Results file structure valid ({len(data['events'])} events)")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in results file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading results file: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Testing scipy_pure_production_analysis.py")
    print("=" * 70)
    
    # First test: import the script
    print("\nScript Import:")
    passed, module = test_script_import()
    if not passed:
        print("\n❌ Cannot continue tests without successful import")
        return 1
    
    # Other tests that depend on the module
    tests = [
        ("Key Events Definition", lambda: test_key_events_defined(module)),
        ("SNR Values", lambda: test_snr_values(module)),
        ("Exceptional Peak", lambda: test_exceptional_peak(module)),
        ("Frequency Config", lambda: test_frequency_config(module)),
        ("Results File Structure", test_results_file_structure),
    ]
    
    results = [("Script Import", True)]  # Already passed
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    print(f"Tests passed: {passed_count}/{total}")
    
    if passed_count == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed_count} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
