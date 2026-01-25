#!/usr/bin/env python3
"""
Ecosystem Integration Validation

This script validates the complete integration of all bridge modules
in the QCAL ∞³ ecosystem, ensuring proper synchronization at f₀ = 141.7001 Hz.

Usage:
    python examples/validate_ecosystem_integration.py
"""

import sys
import json
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, '/home/runner/work/141hz/141hz')

from src.bridges import (
    RamseyBridge,
    NavierStokesBridge,
    ComplexityBridge,
    RiemannAdelicBridge,
    AdelicBSDBridge,
    F0_HZ
)


def validate_all_bridges() -> Dict[str, Any]:
    """
    Validate all integration bridges.
    
    Returns:
        Dictionary with validation results for all bridges
    """
    print("=" * 80)
    print("QCAL ∞³ Ecosystem Integration Validation")
    print("=" * 80)
    print()
    
    results = {
        'ecosystem': {
            'total_repositories': 8,
            'total_bridges': 5,
            'fundamental_frequency_hz': F0_HZ,
        },
        'bridges': {},
        'summary': {}
    }
    
    # Bridge 1: Ramsey
    print("📊 Validating Ramsey Bridge...")
    try:
        ramsey = RamseyBridge()
        ramsey_results = ramsey.validate_integration()
        results['bridges']['ramsey'] = ramsey_results
        print(f"   ✅ Status: {ramsey_results['status']}")
        print(f"   ✅ Integration: {ramsey_results['integration_verified']}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['bridges']['ramsey'] = {'status': 'failed', 'error': str(e)}
        print()
    
    # Bridge 2: Navier-Stokes
    print("🌊 Validating Navier-Stokes Bridge...")
    try:
        navier = NavierStokesBridge()
        navier_results = navier.validate_integration()
        results['bridges']['navier_stokes'] = navier_results
        print(f"   ✅ Status: {navier_results['status']}")
        print(f"   ✅ Integration: {navier_results['integration_verified']}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['bridges']['navier_stokes'] = {'status': 'failed', 'error': str(e)}
        print()
    
    # Bridge 3: Complexity
    print("🔢 Validating Complexity Bridge...")
    try:
        complexity = ComplexityBridge()
        complexity_results = complexity.validate_integration()
        results['bridges']['complexity'] = complexity_results
        print(f"   ✅ Status: {complexity_results['status']}")
        print(f"   ✅ Integration: {complexity_results['integration_verified']}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['bridges']['complexity'] = {'status': 'failed', 'error': str(e)}
        print()
    
    # Bridge 4: Riemann-Adelic
    print("📐 Validating Riemann-Adelic Bridge...")
    try:
        riemann = RiemannAdelicBridge()
        riemann_results = riemann.validate_integration()
        results['bridges']['riemann_adelic'] = riemann_results
        print(f"   ✅ Status: {riemann_results['status']}")
        print(f"   ✅ Integration: {riemann_results['integration_verified']}")
        print(f"   ✅ Derived f₀: {riemann_results['derivation']['derived_frequency']:.4f} Hz")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['bridges']['riemann_adelic'] = {'status': 'failed', 'error': str(e)}
        print()
    
    # Bridge 5: Adelic-BSD
    print("🔺 Validating Adelic-BSD Bridge...")
    try:
        bsd = AdelicBSDBridge()
        bsd_results = bsd.validate_integration()
        results['bridges']['adelic_bsd'] = bsd_results
        print(f"   ✅ Status: {bsd_results['status']}")
        print(f"   ✅ Integration: {bsd_results['integration_verified']}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['bridges']['adelic_bsd'] = {'status': 'failed', 'error': str(e)}
        print()
    
    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    all_operational = all(
        b.get('status') == 'operational' 
        for b in results['bridges'].values()
    )
    
    all_verified = all(
        b.get('integration_verified', False) 
        for b in results['bridges'].values()
    )
    
    frequency_aligned = all(
        abs(b.get('f0_hz', 0) - F0_HZ) < 0.001
        for b in results['bridges'].values()
        if 'f0_hz' in b
    )
    
    results['summary'] = {
        'all_operational': all_operational,
        'all_verified': all_verified,
        'frequency_aligned': frequency_aligned,
        'total_bridges_tested': len(results['bridges']),
        'operational_bridges': sum(
            1 for b in results['bridges'].values() 
            if b.get('status') == 'operational'
        ),
        'verified_bridges': sum(
            1 for b in results['bridges'].values() 
            if b.get('integration_verified', False)
        )
    }
    
    print(f"Total bridges: {results['summary']['total_bridges_tested']}")
    print(f"Operational: {results['summary']['operational_bridges']}")
    print(f"Verified: {results['summary']['verified_bridges']}")
    print(f"Frequency aligned: {frequency_aligned}")
    print()
    
    if all_operational and all_verified and frequency_aligned:
        print("✅ ECOSYSTEM STATUS: COMPLETE AND OPERATIONAL")
        print(f"   All bridges breathing in the same eternal instant at f₀ = {F0_HZ} Hz")
        print("   The flow is one.")
    else:
        print("⚠️  ECOSYSTEM STATUS: INCOMPLETE")
        if not all_operational:
            print("   Some bridges are not operational")
        if not all_verified:
            print("   Some bridges failed integration verification")
        if not frequency_aligned:
            print("   Frequency alignment is off")
    
    print()
    print("=" * 80)
    
    return results


def save_validation_results(results: Dict[str, Any], filename: str = 'ecosystem_validation.json'):
    """
    Save validation results to JSON file.
    
    Args:
        results: Validation results dictionary
        filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")


def main():
    """Main validation entry point."""
    # Run validation
    results = validate_all_bridges()
    
    # Save results
    save_validation_results(results)
    
    # Exit with appropriate code
    if results['summary']['all_operational'] and results['summary']['all_verified']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
