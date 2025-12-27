#!/usr/bin/env python3
"""
Validation Script for Universal Constants Emergence

This script demonstrates the emergence of Planck's constant (ℏ) and electron
charge (e) as geometric manifestations of the vibrational field at f₀ = 141.7001 Hz.

Usage:
    python validate_universal_constants.py [--save-json FILE] [--format text|json]

Author: José Manuel Mota Burruezo Ψ ✧ ∞³
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from universal_constants_derivation import UniversalConstantsEmergence

def main():
    """Run demonstration and display results."""
    parser = argparse.ArgumentParser(
        description="Demonstrate emergence of universal constants from QCAL ∞³"
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--save", type=str, metavar="FILE",
        help="Save results to file"
    )
    
    args = parser.parse_args()
    
    # Create demonstration instance
    demo = UniversalConstantsEmergence()
    
    if args.format == "json":
        results = demo.full_demonstration()
        output = json.dumps(results, indent=2)
        print(output)
        
        if args.save:
            with open(args.save, 'w') as f:
                f.write(output)
            print(f"\n✓ Results saved to: {args.save}", file=sys.stderr)
    else:
        output = demo.generate_report()
        print(output)
        
        if args.save:
            with open(args.save, 'w') as f:
                f.write(output)
            print(f"\n✓ Results saved to: {args.save}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
