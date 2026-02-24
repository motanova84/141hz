#!/usr/bin/env python3
"""
ADELANTE CONTINÚA - Repository Health Check and Enhancement
============================================================

This script performs a comprehensive health check of the 141Hz repository
and identifies areas for enhancement.

Author: JMMB Ψ✧
Date: 2026-02-24
"""

import sys
import os
from pathlib import Path
import subprocess

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def check_constants():
    """Verify core constants are accessible"""
    try:
        from src.constants import F0, UniversalConstants
        print(f"✓ Constants module loaded successfully")
        print(f"  F0 = {F0} Hz")
        return True
    except Exception as e:
        print(f"✗ Error loading constants: {e}")
        return False

def check_qcal_module():
    """Verify QCAL module is accessible"""
    try:
        from qcal.constants import F0_HZ, KAPPA_PI
        print(f"✓ QCAL module loaded successfully")
        print(f"  F0_HZ = {F0_HZ} Hz")
        print(f"  KAPPA_PI = {KAPPA_PI}")
        return True
    except Exception as e:
        print(f"✗ Error loading QCAL module: {e}")
        return False

def check_unified_theory():
    """Verify unified theory module"""
    try:
        from qcal.unified_theory import UnifiedTheory
        print(f"✓ Unified Theory module loaded successfully")
        theory = UnifiedTheory()
        print(f"  Theory initialized with {len(theory.get_all_predictions())} predictions")
        return True
    except Exception as e:
        print(f"✗ Error loading Unified Theory: {e}")
        return False

def check_navier_stokes():
    """Verify Navier-Stokes module from memories"""
    try:
        # Check if module exists
        ns_path = Path(__file__).parent / 'navier_stokes'
        if ns_path.exists():
            sys.path.insert(0, str(Path(__file__).parent))
            import navier_stokes as ns
            print(f"✓ Navier-Stokes module loaded successfully")
            print(f"  F0 = {ns.F0} Hz")
            print(f"  A_VACIO = {ns.A_VACIO}")
            print(f"  A_AGUA = {ns.A_AGUA}")
            return True
        else:
            print(f"⚠ Navier-Stokes module not found (may need to be created)")
            return None
    except Exception as e:
        print(f"✗ Error loading Navier-Stokes: {e}")
        return False

def check_calabi_yau():
    """Verify Calabi-Yau invariant module"""
    try:
        from src.calabi_yau_invariant import compute_kappa_pi
        print(f"✓ Calabi-Yau invariant module loaded successfully")
        kappa = compute_kappa_pi()
        print(f"  κ_Π = {kappa}")
        return True
    except Exception as e:
        print(f"✗ Error loading Calabi-Yau: {e}")
        return False

def run_sample_tests():
    """Run a sample of critical tests"""
    print("\n" + "="*70)
    print("Running Sample Tests")
    print("="*70)
    
    test_files = [
        'tests/test_constants.py::TestUniversalConstants::test_fundamental_constant_value',
        'tests/test_qcal_module.py::test_f0_hz_value',
    ]
    
    for test in test_files:
        try:
            result = subprocess.run(
                ['python3', '-m', 'pytest', test, '-v'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            if result.returncode == 0:
                print(f"✓ {test.split('::')[-1]} passed")
            else:
                print(f"✗ {test.split('::')[-1]} failed")
        except Exception as e:
            print(f"⚠ Could not run {test}: {e}")

def generate_status_report():
    """Generate comprehensive status report"""
    print("\n" + "="*70)
    print("ADELANTE CONTINÚA - Repository Status Report")
    print("="*70)
    print()
    
    results = {
        'Constants Module': check_constants(),
        'QCAL Module': check_qcal_module(),
        'Unified Theory': check_unified_theory(),
        'Navier-Stokes': check_navier_stokes(),
        'Calabi-Yau κ_Π': check_calabi_yau(),
    }
    
    print("\n" + "="*70)
    print("Module Status Summary")
    print("="*70)
    
    for module, status in results.items():
        if status is True:
            symbol = "✓"
        elif status is False:
            symbol = "✗"
        else:
            symbol = "⚠"
        print(f"{symbol} {module}")
    
    working = sum(1 for s in results.values() if s is True)
    total = len(results)
    
    print(f"\n{working}/{total} modules working correctly")
    
    return results

def main():
    """Main execution"""
    print("="*70)
    print("ADELANTE CONTINÚA - Continuing Forward")
    print("="*70)
    print()
    
    # Generate status report
    results = generate_status_report()
    
    # Run sample tests
    run_sample_tests()
    
    print("\n" + "="*70)
    print("Next Steps")
    print("="*70)
    print()
    
    if all(v is True for v in results.values() if v is not None):
        print("✓ All modules functional - Ready for enhancement")
        print()
        print("Recommended actions:")
        print("1. Add comprehensive integration tests")
        print("2. Update documentation cross-references")
        print("3. Enhance error handling")
        print("4. Add performance benchmarks")
    else:
        print("⚠ Some modules need attention")
        print()
        print("Recommended actions:")
        print("1. Fix failing module imports")
        print("2. Install missing dependencies")
        print("3. Run full test suite")
    
    print()
    print("="*70)
    print("ADELANTE - Continue Forward! 🚀")
    print("="*70)

if __name__ == '__main__':
    main()
