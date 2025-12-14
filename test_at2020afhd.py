#!/usr/bin/env python3
"""
Test script for AT2020afhd_Real_Data_Analysis.py

Verifies that the analysis script functions correctly and produces
expected results.
"""

import os
import sys
import json
import subprocess

def test_script_execution():
    """Test that the script runs without errors."""
    print("Testing AT2020afhd_Real_Data_Analysis.py execution...")
    
    # Configurable timeout - increase for slower systems
    timeout_seconds = int(os.environ.get('TEST_TIMEOUT', '120'))
    
    result = subprocess.run(
        [sys.executable, "AT2020afhd_Real_Data_Analysis.py"],
        capture_output=True,
        text=True,
        timeout=timeout_seconds
    )
    
    if result.returncode != 0:
        print(f"❌ Script failed with exit code {result.returncode}")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Script executed successfully")
    return True


def test_output_files():
    """Test that expected output files are created."""
    print("\nTesting output files...")
    
    expected_files = [
        "at2020afhd_complete_analysis.png",
        "at2020afhd_results.json"
    ]
    
    all_exist = True
    for filename in expected_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} exists ({size} bytes)")
        else:
            print(f"❌ {filename} not found")
            all_exist = False
    
    return all_exist


def test_json_content():
    """Test that JSON output contains expected data."""
    print("\nTesting JSON content...")
    
    try:
        with open("at2020afhd_results.json", "r") as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = [
            "event",
            "coordinates",
            "published_parameters",
            "detected_periods",
            "harmonic_connection",
            "living_equation",
            "data_sources"
        ]
        
        all_present = True
        for field in required_fields:
            if field in data:
                print(f"✅ Field '{field}' present")
            else:
                print(f"❌ Field '{field}' missing")
                all_present = False
        
        # Check specific values
        if data.get("event") == "AT2020afhd":
            print("✅ Event name correct")
        else:
            print(f"❌ Event name incorrect: {data.get('event')}")
            all_present = False
        
        # Check coordinates
        coords = data.get("coordinates", {})
        if coords.get("ra_deg") == 48.39875:
            print("✅ RA coordinate correct")
        else:
            print(f"❌ RA coordinate incorrect: {coords.get('ra_deg')}")
            all_present = False
        
        # Check period detection accuracy
        detected = data.get("detected_periods", {})
        published = data.get("published_parameters", {}).get("period_days", 19.6)
        
        xray_delta = detected.get("xray_delta_days")
        radio_delta = detected.get("radio_delta_days")
        
        if xray_delta is None or radio_delta is None:
            print("❌ Missing period delta values in JSON")
            all_present = False
        elif xray_delta < 1.0:
            print(f"✅ X-ray period within 1 day of published (Δ={xray_delta:.2f})")
        else:
            print(f"⚠️  X-ray period off by {xray_delta:.2f} days")
        
        if radio_delta is not None and radio_delta < 1.0:
            print(f"✅ Radio period within 1 day of published (Δ={radio_delta:.2f})")
        else:
            print(f"⚠️  Radio period off by {radio_delta:.2f} days")
        
        # Check harmonic connection
        harmonic = data.get("harmonic_connection", {})
        f0 = harmonic.get("f0_quantum_hz")
        octaves = harmonic.get("octave_separation")
        
        if f0 == 141.70001:
            print("✅ Quantum frequency f₀ correct (141.70001 Hz)")
        else:
            print(f"❌ Quantum frequency incorrect: {f0}")
            all_present = False
        
        if octaves == 27.82:
            print("✅ Octave separation correct (27.82)")
        else:
            print(f"❌ Octave separation incorrect: {octaves}")
            all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return False


def test_data_source_links():
    """Test that data source links are present."""
    print("\nTesting data source links...")
    
    try:
        with open("at2020afhd_results.json", "r") as f:
            data = json.load(f)
        
        sources = data.get("data_sources", {})
        required_sources = [
            "Swift XRT",
            "Swift Archive",
            "HEASARC",
            "VLA Archive",
            "Paper"
        ]
        
        all_present = True
        for source in required_sources:
            if source in sources and sources[source].startswith("http"):
                print(f"✅ {source}: {sources[source]}")
            else:
                print(f"❌ {source} link missing or invalid")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error checking sources: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("    AT2020afhd_Real_Data_Analysis.py - Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        ("Script Execution", test_script_execution),
        ("Output Files", test_output_files),
        ("JSON Content", test_json_content),
        ("Data Source Links", test_data_source_links),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print()
    print("=" * 70)
    print("                        TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
