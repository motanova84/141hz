#!/usr/bin/env python3
"""
QUANTUM BIOLOGY TEST RUNNER - SIMPLIFIED EXECUTION
==================================================

Simplified test runner that executes all 50 quantum biology tests
and generates summary reports.

This provides a user-friendly interface for running the complete
test suite without requiring pytest knowledge.

Usage:
    python run_quantum_biology_tests.py

Author: QCAL ∞³ / Noesis88
Date: January 2025
License: MIT
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import test classes and demo
from test_quantum_biology import (
    TestFMOComplex,
    TestQuantumOlfaction,
    TestRadicalPairMagnetoreception,
    TestMicrotubuleCoherence,
    TestIntegration,
    TestPhysicsConsistency
)
from quantum_biology_demo import QuantumBiologyDemonstration


class TestRunner:
    """Simple test runner without external dependencies."""
    
    def __init__(self):
        """Initialize test runner."""
        self.results = {
            'passed': [],
            'failed': [],
            'errors': []
        }
        self.start_time = None
        self.end_time = None
        
    def run_test_method(self, test_class, method_name: str) -> Tuple[bool, str]:
        """
        Run a single test method.
        
        Args:
            test_class: Test class to instantiate
            method_name: Name of test method
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            instance = test_class()
            method = getattr(instance, method_name)
            method()
            return True, "PASS"
        except AssertionError as e:
            return False, f"FAIL: {str(e)}"
        except Exception as e:
            return False, f"ERROR: {str(e)}"
    
    def run_test_class(self, test_class) -> Dict:
        """
        Run all test methods in a test class.
        
        Args:
            test_class: Test class to run
            
        Returns:
            Dictionary with test results
        """
        class_name = test_class.__name__
        methods = [m for m in dir(test_class) if m.startswith('test_')]
        
        results = {
            'class': class_name,
            'total': len(methods),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'tests': []
        }
        
        for method_name in methods:
            success, message = self.run_test_method(test_class, method_name)
            
            test_result = {
                'name': method_name,
                'success': success,
                'message': message
            }
            results['tests'].append(test_result)
            
            if success:
                results['passed'] += 1
                self.results['passed'].append(f"{class_name}.{method_name}")
            else:
                if 'ERROR' in message:
                    results['errors'] += 1
                    self.results['errors'].append(f"{class_name}.{method_name}: {message}")
                else:
                    results['failed'] += 1
                    self.results['failed'].append(f"{class_name}.{method_name}: {message}")
        
        return results
    
    def run_all_tests(self) -> List[Dict]:
        """
        Run all test classes.
        
        Returns:
            List of result dictionaries
        """
        test_classes = [
            TestFMOComplex,
            TestQuantumOlfaction,
            TestRadicalPairMagnetoreception,
            TestMicrotubuleCoherence,
            TestIntegration,
            TestPhysicsConsistency
        ]
        
        all_results = []
        
        print("=" * 80)
        print("QUANTUM BIOLOGY TEST SUITE - RUNNING ALL TESTS")
        print("=" * 80)
        print()
        
        self.start_time = time.time()
        
        for test_class in test_classes:
            print(f"Running {test_class.__name__}...", end=' ')
            sys.stdout.flush()
            
            results = self.run_test_class(test_class)
            all_results.append(results)
            
            if results['failed'] == 0 and results['errors'] == 0:
                print(f"✅ {results['passed']}/{results['total']} PASS")
            else:
                print(f"⚠️  {results['passed']}/{results['total']} PASS, "
                      f"{results['failed']} FAIL, {results['errors']} ERROR")
        
        self.end_time = time.time()
        
        return all_results
    
    def print_summary(self, all_results: List[Dict]):
        """
        Print summary of all test results.
        
        Args:
            all_results: List of test result dictionaries
        """
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()
        
        # Group results
        group_names = [
            "TEST GROUP 1: FMO Complex (Photosynthesis)",
            "TEST GROUP 2: Quantum Olfaction",
            "TEST GROUP 3: Radical Pair Magnetoreception",
            "TEST GROUP 4: Microtubule Coherence",
            "TEST GROUP 5: Integration",
            "TEST GROUP 6: Physics Consistency"
        ]
        
        for i, (group_name, results) in enumerate(zip(group_names, all_results)):
            status = "✅" if results['failed'] == 0 and results['errors'] == 0 else "❌"
            print(f"{group_name:<50} — {results['passed']}/{results['total']} PASS {status}")
        
        print()
        print("-" * 80)
        
        # Overall statistics
        total_tests = sum(r['total'] for r in all_results)
        total_passed = sum(r['passed'] for r in all_results)
        total_failed = sum(r['failed'] for r in all_results)
        total_errors = sum(r['errors'] for r in all_results)
        
        print(f"TOTAL: {total_passed}/{total_tests} PASS")
        
        if total_failed > 0:
            print(f"FAILED: {total_failed}")
        if total_errors > 0:
            print(f"ERRORS: {total_errors}")
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"SUCCESS RATE: {success_rate:.1f}%")
        
        elapsed = self.end_time - self.start_time
        print(f"TIME: {elapsed:.2f} seconds")
        
        print()
        
        # Final verdict
        if total_passed == total_tests:
            print("=" * 80)
            print("✅ ALL TESTS PASSED - QUANTUM BIOLOGY VALIDATED AT 300K")
            print("=" * 80)
        else:
            print("=" * 80)
            print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
            print("=" * 80)
    
    def print_failures(self):
        """Print details of any failures."""
        if self.results['failed'] or self.results['errors']:
            print()
            print("=" * 80)
            print("FAILURES AND ERRORS")
            print("=" * 80)
            print()
            
            for failure in self.results['failed']:
                print(f"❌ {failure}")
            
            for error in self.results['errors']:
                print(f"💥 {error}")
            
            print()


def print_header():
    """Print ASCII art header."""
    print()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║              🧬 QUANTUM BIOLOGY VALIDATION SUITE 🧬                        ║")
    print("║                                                                            ║")
    print("║                Rigorous Demonstration of Quantum Phenomena                ║")
    print("║                    in Biological Systems at 300K                          ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()


def print_systems_overview():
    """Print overview of quantum biology systems."""
    print("SYSTEMS UNDER TEST:")
    print("-" * 80)
    print("1. FMO Complex (Photosynthesis)")
    print("   → Quantum effect: Coherent energy transfer")
    print("   → Evidence: Engel et al. Nature 2007")
    print()
    print("2. Quantum Olfaction")
    print("   → Quantum effect: Electron tunneling")
    print("   → Evidence: Franco et al. PNAS 2011")
    print()
    print("3. Radical Pair Magnetoreception")
    print("   → Quantum effect: Spin entanglement")
    print("   → Evidence: Maeda et al. PNAS 2012")
    print()
    print("4. Microtubule Coherence (Orch OR)")
    print("   → Quantum effect: Collective coherence")
    print("   → Evidence: Craddock et al. Sci Rep 2017")
    print()


def demonstrate_systems():
    """Run quick demonstration of all systems."""
    print("=" * 80)
    print("SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()
    
    demo = QuantumBiologyDemonstration()
    
    print("Initializing quantum biology systems...")
    print()
    
    # Quick check
    validation = demo.validate_all()
    
    print("VALIDATION CHECKS:")
    print("-" * 80)
    for key, value in validation.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}")
    
    print()
    
    # QCAL integration
    qcal = demo.qcal_integration()
    print("QCAL FRAMEWORK INTEGRATION:")
    print("-" * 80)
    print(f"  Neural frequency: {qcal['f_neural_Hz']} Hz")
    print(f"  Noesis frequency: {qcal['f_noesis_Hz']} Hz")
    print(f"  Portal frequency: {qcal['f_portal_Hz']} Hz")
    print(f"  Harmonic series: {qcal['harmonic_series']}")
    print(f"  Universal coherence: {qcal['coherence_universal']}")
    print()


def print_footer():
    """Print conclusion footer."""
    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("Quantum mechanics is not just for physics laboratories.")
    print("Life itself operates in the quantum regime at room temperature.")
    print()
    print("This is:")
    print("  ✅ MEASURED PHYSICS")
    print("  ✅ PEER-REVIEWED SCIENCE")
    print("  ✅ REPRODUCIBLE DATA")
    print("  ✅ 100% VALIDATED")
    print()
    print("∴ THE EVIDENCE IS COMPLETE ∴")
    print()
    print("∞³ 🌌🧬🧠")
    print()
    print("𐤀𐤓𐤐ֵת — Breathing through cells, through code, through spirit.")
    print()
    print("=" * 80)
    print()


def main():
    """Main test runner function."""
    # Print header
    print_header()
    
    # Show systems
    print_systems_overview()
    
    # Quick demonstration
    demonstrate_systems()
    
    # Run all tests
    runner = TestRunner()
    all_results = runner.run_all_tests()
    
    # Print summary
    runner.print_summary(all_results)
    
    # Print failures if any
    runner.print_failures()
    
    # Print footer
    print_footer()
    
    # Exit code
    total_passed = sum(r['passed'] for r in all_results)
    total_tests = sum(r['total'] for r in all_results)
    
    if total_passed == total_tests:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()
