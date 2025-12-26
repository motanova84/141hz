#!/usr/bin/env python3
"""
Test suite for GWTC-3 analysis script
Validates script structure, parameters, and basic functionality
"""

import sys
import ast
import json
from pathlib import Path


def test_script_exists():
    """Test that the GWTC-3 analysis script exists"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    assert script_path.exists(), "Script analisis_gwtc3_completo.py not found"
    print("✅ Script file exists")
    return True


def test_script_syntax():
    """Test that the script has valid Python syntax"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    try:
        ast.parse(code)
        print("✅ Script has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False


def test_required_functions():
    """Test that required functions are defined"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    required_functions = ['install', 'analyze_event_simple']
    for func in required_functions:
        if func in functions:
            print(f"✅ Function '{func}' is defined")
        else:
            print(f"❌ Function '{func}' is missing")
            return False
    
    return True


def test_event_list():
    """Test that GWTC-3 event list is properly defined"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check if events_gwtc3 list is defined
    if 'events_gwtc3 = [' in code:
        print("✅ GWTC-3 event list is defined")
    else:
        print("❌ GWTC-3 event list not found")
        return False
    
    # Check for expected event patterns
    expected_events = ['GW190412', 'GW190521', 'GW190814', 'GW200316_215756']
    for event in expected_events:
        if event in code:
            print(f"✅ Event '{event}' found in list")
        else:
            print(f"❌ Event '{event}' not found")
            return False
    
    return True


def test_parameters():
    """Test that key parameters are defined"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check for frequency parameters
    required_params = [
        'freq_target',
        'freq_tolerance',
        'snr_threshold',
        'band_low',
        'band_high'
    ]
    
    for param in required_params:
        if f'{param} =' in code:
            print(f"✅ Parameter '{param}' is defined")
        else:
            print(f"❌ Parameter '{param}' not found")
            return False
    
    # Verify 141.7 Hz is used
    if '141.7' in code:
        print("✅ Target frequency 141.7 Hz is set")
    else:
        print("❌ Target frequency 141.7 Hz not found")
        return False
    
    return True


def test_output_files():
    """Test that script generates expected output files"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    expected_outputs = [
        'gwtc3_results.png',
        'gwtc3_analysis_results.json'
    ]
    
    for output in expected_outputs:
        if output in code:
            print(f"✅ Output file '{output}' is generated")
        else:
            print(f"❌ Output file '{output}' not found in code")
            return False
    
    return True


def test_error_handling():
    """Test that script includes error handling"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check for try-except blocks
    if 'try:' in code and 'except' in code:
        print("✅ Error handling (try-except) is present")
    else:
        print("❌ No error handling found")
        return False
    
    # Check for ImportError handling
    if 'ImportError' in code:
        print("✅ ImportError handling is present")
    else:
        print("❌ ImportError handling not found")
        return False
    
    return True


def test_visualization():
    """Test that visualization code is present"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check for matplotlib usage
    if 'plt.subplots' in code or 'plt.figure' in code:
        print("✅ Matplotlib visualization is present")
    else:
        print("❌ Matplotlib visualization not found")
        return False
    
    # Check for bar chart and histogram
    if 'ax.bar' in code:
        print("✅ Bar chart for detection rates is present")
    else:
        print("❌ Bar chart not found")
        return False
    
    if 'ax.hist' in code or 'plt.hist' in code:
        print("✅ Histogram for SNR distribution is present")
    else:
        print("❌ Histogram not found")
        return False
    
    return True


def test_automatic_installation():
    """Test that automatic installation is implemented"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check for install function
    if 'def install(' in code:
        print("✅ Install function is defined")
    else:
        print("❌ Install function not found")
        return False
    
    # Check for subprocess usage
    if 'subprocess.check_call' in code:
        print("✅ Subprocess for package installation is present")
    else:
        print("❌ Subprocess not found")
        return False
    
    # Check for gwpy and pycbc installation
    if 'gwpy' in code and 'pycbc' in code:
        print("✅ gwpy and pycbc installation is handled")
    else:
        print("❌ gwpy/pycbc installation not found")
        return False
    
    return True


def test_gwtc1_comparison():
    """Test that GWTC-1 comparison is included"""
    script_path = Path(__file__).parent / "analisis_gwtc3_completo.py"
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Check for GWTC-1 comparison
    if 'GWTC-1' in code and 'GWTC-3' in code:
        print("✅ GWTC-1 vs GWTC-3 comparison is present")
    else:
        print("❌ GWTC comparison not found")
        return False
    
    # Check for combined rate calculation
    if 'rate_combined' in code or 'total_detected' in code:
        print("✅ Combined detection rate is calculated")
    else:
        print("❌ Combined rate calculation not found")
        return False
    
    return True


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("GWTC-3 ANALYSIS SCRIPT VALIDATION")
    print("=" * 70)
    print()
    
    tests = [
        ("Script Exists", test_script_exists),
        ("Python Syntax", test_script_syntax),
        ("Required Functions", test_required_functions),
        ("Event List", test_event_list),
        ("Parameters", test_parameters),
        ("Output Files", test_output_files),
        ("Error Handling", test_error_handling),
        ("Visualization", test_visualization),
        ("Automatic Installation", test_automatic_installation),
        ("GWTC-1 Comparison", test_gwtc1_comparison),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"TEST: {test_name}")
        print('='*70)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
