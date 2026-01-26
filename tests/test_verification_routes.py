#!/usr/bin/env python3
"""
Test script to verify that all three verification routes are properly set up.

This script checks:
1. Empirical Verification - Scripts and data paths exist
2. Formal Verification - Lean 4 files exist
3. Automated Verification - CI/CD and verificador exist
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def test_route_1_empirical():
    """Test Route 1: Empirical Verification (Spectral Analysis)"""
    print(f"\n{BOLD}⚛️  Route 1: Empirical Verification{RESET}")
    print("=" * 60)
    
    checks = []
    
    # Check if scripts exist
    scripts = [
        'scripts/analizar_ringdown.py',
        'multi_event_analysis.py',
        'scripts/descargar_datos.py'
    ]
    
    for script in scripts:
        exists = os.path.exists(script)
        status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
        checks.append(exists)
        print(f"  {status} Script exists: {script}")
    
    # Check if Makefile has required targets
    makefile_exists = os.path.exists('Makefile')
    status = f"{GREEN}✓{RESET}" if makefile_exists else f"{RED}✗{RESET}"
    checks.append(makefile_exists)
    print(f"  {status} Makefile exists")
    
    # Check if results JSON exists (optional - for verification)
    results_json = 'multi_event_final.json'
    exists = os.path.exists(results_json)
    status = f"{GREEN}✓{RESET}" if exists else f"{YELLOW}○{RESET}"
    print(f"  {status} Results file exists (optional): {results_json}")
    
    return all(checks)

def test_route_2_formal():
    """Test Route 2: Formal Verification (Lean 4)"""
    print(f"\n{BOLD}🔢 Route 2: Formal Verification{RESET}")
    print("=" * 60)
    
    checks = []
    
    # Check if Lean formalization directory exists
    lean_dir = 'formalization/lean'
    exists = os.path.exists(lean_dir)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    checks.append(exists)
    print(f"  {status} Lean directory exists: {lean_dir}")
    
    # Check for key Lean files
    lean_files = [
        'formalization/lean/lakefile.lean',
        'formalization/lean/lean-toolchain',
        'formalization/lean/Main.lean',
        'formalization/lean/F0Derivation/Main.lean'
    ]
    
    for lean_file in lean_files:
        exists = os.path.exists(lean_file)
        status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
        checks.append(exists)
        print(f"  {status} Lean file exists: {lean_file}")
    
    # Check if README exists
    readme = 'formalization/lean/README.md'
    exists = os.path.exists(readme)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    checks.append(exists)
    print(f"  {status} Lean README exists: {readme}")
    
    return all(checks)

def test_route_3_automated():
    """Test Route 3: Automated Verification (Ω∞³)"""
    print(f"\n{BOLD}🤖 Route 3: Automated Verification{RESET}")
    print("=" * 60)
    
    checks = []
    
    # Check if CI/CD workflows exist
    workflows = [
        '.github/workflows/analyze.yml',
        '.github/workflows/lean-verification.yml'
    ]
    
    for workflow in workflows:
        exists = os.path.exists(workflow)
        status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
        checks.append(exists)
        print(f"  {status} CI/CD workflow exists: {workflow}")
    
    # Check if verificador script exists
    verificador = 'demo_verificador.py'
    exists = os.path.exists(verificador)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    checks.append(exists)
    print(f"  {status} Verificador script exists: {verificador}")
    
    # Check if GW250114 analyzer exists
    analyzer = 'scripts/analizar_gw250114.py'
    exists = os.path.exists(analyzer)
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    checks.append(exists)
    print(f"  {status} GW250114 analyzer exists: {analyzer}")
    
    return all(checks)

def test_documentation():
    """Test that documentation exists"""
    print(f"\n{BOLD}📖 Documentation{RESET}")
    print("=" * 60)
    
    checks = []
    
    docs = [
        'README.md',
        'VERIFICATION_ROUTES.md',
        'requirements.txt'
    ]
    
    for doc in docs:
        exists = os.path.exists(doc)
        status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
        checks.append(exists)
        print(f"  {status} Documentation exists: {doc}")
    
    return all(checks)

def main():
    """Run all verification route tests"""
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}Testing Verification Routes for 141Hz Repository{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    
    results = []
    
    # Test each route
    results.append(("Route 1 (Empirical)", test_route_1_empirical()))
    results.append(("Route 2 (Formal)", test_route_2_formal()))
    results.append(("Route 3 (Automated)", test_route_3_automated()))
    results.append(("Documentation", test_documentation()))
    
    # Summary
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}Summary{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    
    all_passed = True
    for name, passed in results:
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        all_passed = all_passed and passed
        print(f"  {status} {name}")
    
    print()
    if all_passed:
        print(f"{GREEN}{BOLD}✓ All verification routes are properly configured!{RESET}")
        print(f"\n{BOLD}Next steps:{RESET}")
        print(f"  1. Run 'make setup' to install dependencies")
        print(f"  2. Run 'make analyze' for empirical verification")
        print(f"  3. Run 'cd formalization/lean && lake build' for formal verification")
        print(f"  4. Check GitHub Actions for automated verification")
        return 0
    else:
        print(f"{RED}{BOLD}✗ Some verification routes are missing components{RESET}")
        print(f"  Please check the failed items above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
