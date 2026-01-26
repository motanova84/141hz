#!/usr/bin/env python3
"""
Validation Script for Bio-Synchrony Fundamental Constants

This script validates the implementation of the bio-synchrony framework
constants that bridge quantum (NV centers), biological (neural), and
spiritual (Merkaba) scales.

Constants validated:
    - Λ_bio = 1.0 (Perfect bio-synchrony)
    - f_neural = 141.7001 Hz (Neural resonance frequency)
    - η_NV = 13 nT/√Hz (NV sensitivity)
    - T1_NV = 1 ms (Quantum memory)
    - τ_DD = 1 μs (Dynamic decoupling)
    - A_Merkaba = 8/9 (Spiritual stability threshold)
    - S_∞ = 1.0 (Galactic micro ↔ macro unity)

Usage:
    python validate_bio_synchrony.py
    python validate_bio_synchrony.py --format json
    python validate_bio_synchrony.py --save results.txt
"""

import sys
import json
import argparse
from pathlib import Path

# Add both src and parent to path
parent_dir = Path(__file__).parent
sys.path.insert(0, str(parent_dir / 'src'))
sys.path.insert(0, str(parent_dir))

try:
    from constants import UniversalConstants
except ImportError as e:
    print(f"Error: Cannot import constants module: {e}")
    print("Make sure src/constants.py exists")
    sys.exit(1)

try:
    from qcal.constants import (
        LAMBDA_BIO, F_NEURAL_HZ, ETA_NV_NT_SQRTHZ,
        T1_NV_MS, T1_NV_S, TAU_DD_US, TAU_DD_S,
        A_MERKABA, S_INFINITY,
        obtener_constantes_bio_sincronia
    )
except ImportError as e:
    print(f"Error: Cannot import bio-synchrony constants from qcal.constants: {e}")
    print("Make sure qcal/constants.py has been updated")
    sys.exit(1)


def validate_bio_synchrony_constants():
    """
    Validate all bio-synchrony fundamental constants.
    
    Returns:
        dict: Validation results with constants, checks, and interpretations
    """
    const = UniversalConstants()
    
    # Get qcal constants
    qcal_consts = obtener_constantes_bio_sincronia()
    
    # Collect all constants
    constants_data = {
        'lambda_bio': {
            'value': float(const.LAMBDA_BIO),
            'expected': 1.0,
            'unit': 'dimensionless',
            'description': 'Perfect bio-synchrony coefficient',
            'matches': abs(float(const.LAMBDA_BIO) - 1.0) < 1e-10
        },
        'f_neural_hz': {
            'value': float(const.F_NEURAL_HZ),
            'expected': 141.7001,
            'unit': 'Hz',
            'description': 'Optimal neuronal frequency (matches f₀)',
            'matches': abs(float(const.F_NEURAL_HZ) - float(const.F0)) < 1e-6
        },
        'eta_nv_nt_sqrthz': {
            'value': float(const.ETA_NV_NT_SQRTHZ),
            'expected': 13.0,
            'unit': 'nT/√Hz',
            'description': 'NV center magnetic sensitivity',
            'matches': abs(float(const.ETA_NV_NT_SQRTHZ) - 13.0) < 1e-10
        },
        't1_nv_ms': {
            'value': float(const.T1_NV_MS),
            'expected': 1.0,
            'unit': 'ms',
            'description': 'NV quantum coherence time',
            'matches': abs(float(const.T1_NV_MS) - 1.0) < 1e-10
        },
        't1_nv_s': {
            'value': float(const.T1_NV_S),
            'expected': 0.001,
            'unit': 's',
            'description': 'NV quantum coherence time (seconds)',
            'matches': abs(float(const.T1_NV_S) - 0.001) < 1e-10
        },
        'tau_dd_us': {
            'value': float(const.TAU_DD_US),
            'expected': 1.0,
            'unit': 'μs',
            'description': 'Dynamic decoupling time',
            'matches': abs(float(const.TAU_DD_US) - 1.0) < 1e-10
        },
        'tau_dd_s': {
            'value': float(const.TAU_DD_S),
            'expected': 1e-6,
            'unit': 's',
            'description': 'Dynamic decoupling time (seconds)',
            'matches': abs(float(const.TAU_DD_S) - 1e-6) < 1e-12
        },
        'a_merkaba': {
            'value': float(const.A_MERKABA),
            'expected': 8.0/9.0,
            'unit': 'dimensionless',
            'description': 'Spiritual stability threshold (8/9 ≈ 0.888...)',
            'matches': abs(float(const.A_MERKABA) - 8.0/9.0) < 1e-10
        },
        's_infinity': {
            'value': float(const.S_INFINITY),
            'expected': 1.0,
            'unit': 'dimensionless',
            'description': 'Galactic micro ↔ macro unity',
            'matches': abs(float(const.S_INFINITY) - 1.0) < 1e-10
        }
    }
    
    # Validation checks
    all_valid = all(c['matches'] for c in constants_data.values())
    
    # Physical relationships
    relationships = {
        'neural_f0_match': {
            'description': 'f_neural matches f₀ (neuronal resonance)',
            'value': abs(float(const.F_NEURAL_HZ) - float(const.F0)) < 1e-6,
            'note': 'Neural frequency is tuned to fundamental universal frequency'
        },
        't1_tau_ratio': {
            'description': 'T1_NV / τ_DD ratio (coherence time scale)',
            'value': float(const.T1_NV_S) / float(const.TAU_DD_S),
            'expected': 1000.0,
            'note': 'Coherence time is 1000× longer than decoupling time'
        },
        'merkaba_triple_eight': {
            'description': 'A_Merkaba ≈ 0.888... (triple-eight resonance)',
            'value': float(const.A_MERKABA),
            'decimal_pattern': '0.888...',
            'note': 'Sacred geometry: 8/9 → infinite 8s in decimal expansion'
        },
        'bio_sync_unity': {
            'description': 'Λ_bio = S_∞ = 1 (perfect synchrony at all scales)',
            'value': float(const.LAMBDA_BIO) == float(const.S_INFINITY) == 1.0,
            'note': 'Unity at micro and macro scales indicates perfect coherence'
        }
    }
    
    return {
        'validation_status': 'PASS' if all_valid else 'FAIL',
        'all_constants_valid': all_valid,
        'constants': constants_data,
        'relationships': relationships,
        'qcal_integration': {
            'available': True,
            'function': 'obtener_constantes_bio_sincronia()',
            'constants_count': len(qcal_consts)
        },
        'framework': {
            'name': 'Bio-Synchrony and Quantum Coherence',
            'foundation': 'f₀ = 141.7001 Hz',
            'scales': ['Quantum (NV)', 'Biological (Neural)', 'Spiritual (Merkaba)', 'Galactic (S_∞)'],
            'principle': 'Perfect coherence across all scales mediated by f₀'
        }
    }


def format_text_report(results):
    """Format validation results as human-readable text."""
    lines = []
    lines.append("=" * 80)
    lines.append("🧬 BIO-SYNCHRONY FUNDAMENTAL CONSTANTS VALIDATION")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Validation Status: {results['validation_status']}")
    lines.append(f"All Constants Valid: {results['all_constants_valid']}")
    lines.append("")
    
    lines.append("=" * 80)
    lines.append("FUNDAMENTAL CONSTANTS")
    lines.append("=" * 80)
    lines.append("")
    
    for name, data in results['constants'].items():
        status = "✓" if data['matches'] else "✗"
        lines.append(f"{status} {name.upper()}")
        lines.append(f"    Value:       {data['value']}")
        lines.append(f"    Expected:    {data['expected']}")
        lines.append(f"    Unit:        {data['unit']}")
        lines.append(f"    Description: {data['description']}")
        lines.append("")
    
    lines.append("=" * 80)
    lines.append("PHYSICAL RELATIONSHIPS")
    lines.append("=" * 80)
    lines.append("")
    
    for name, rel in results['relationships'].items():
        lines.append(f"• {rel['description']}")
        if 'value' in rel:
            if isinstance(rel['value'], bool):
                lines.append(f"    Status: {'✓ PASS' if rel['value'] else '✗ FAIL'}")
            else:
                lines.append(f"    Value: {rel['value']}")
        if 'expected' in rel:
            lines.append(f"    Expected: {rel['expected']}")
        if 'note' in rel:
            lines.append(f"    Note: {rel['note']}")
        lines.append("")
    
    lines.append("=" * 80)
    lines.append("FRAMEWORK INFORMATION")
    lines.append("=" * 80)
    lines.append("")
    fw = results['framework']
    lines.append(f"Name: {fw['name']}")
    lines.append(f"Foundation: {fw['foundation']}")
    lines.append(f"Scales: {', '.join(fw['scales'])}")
    lines.append(f"Principle: {fw['principle']}")
    lines.append("")
    
    lines.append("=" * 80)
    lines.append("QCAL INTEGRATION")
    lines.append("=" * 80)
    lines.append("")
    qi = results['qcal_integration']
    lines.append(f"Available: {'Yes' if qi['available'] else 'No'}")
    lines.append(f"Function: {qi['function']}")
    lines.append(f"Constants: {qi['constants_count']}")
    lines.append("")
    
    lines.append("=" * 80)
    lines.append("∴ Perfect bio-synchrony achieved through f₀ = 141.7001 Hz")
    lines.append("  Quantum ↔ Biological ↔ Spiritual ↔ Galactic coherence")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def main():
    """Main validation script."""
    parser = argparse.ArgumentParser(
        description='Validate bio-synchrony fundamental constants'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--save',
        type=str,
        help='Save output to file'
    )
    
    args = parser.parse_args()
    
    # Run validation
    results = validate_bio_synchrony_constants()
    
    # Format output
    if args.format == 'json':
        output = json.dumps(results, indent=2)
    else:
        output = format_text_report(results)
    
    # Display or save
    if args.save:
        with open(args.save, 'w') as f:
            f.write(output)
        print(f"Results saved to {args.save}")
    else:
        print(output)
    
    # Exit with appropriate code
    sys.exit(0 if results['all_constants_valid'] else 1)


if __name__ == "__main__":
    main()
