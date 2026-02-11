#!/usr/bin/env python3
"""
Test Script for Spiral Light Path Theory
==========================================

Standalone test script that can be run directly or via test runner.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import numpy as np

# Import the test module
from tests.test_spiral_light_path import (
    TestSpiralParameters,
    TestSpiralLightPath,
    TestDemonstrationFunctions,
    TestFalsifiablePredictions,
    TestEdgeCases
)


def main():
    """Run all spiral light path tests."""
    print("=" * 70)
    print("SPIRAL LIGHT PATH THEORY - TEST SUITE")
    print("=" * 70)
    print("\nTesting the framework where light travels in logarithmic")
    print("spirals modulated by Riemann zeta zeros and prime numbers.")
    print(f"Fundamental frequency: f₀ = 141.7001 Hz")
    print("=" * 70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSpiralParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestSpiralLightPath))
    suite.addTests(loader.loadTestsFromTestCase(TestDemonstrationFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestFalsifiablePredictions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED")
        print("\nKey validations:")
        print("  ✓ Riemann zeta zeros on critical line Re(s) = 1/2")
        print("  ✓ Prime modulation of spiral phases")
        print("  ✓ Spiral trajectory calculations")
        print("  ✓ Interference pattern projections")
        print("  ✓ Observer projection on critical line")
        print("  ✓ Evolution operator construction")
        print("=" * 70)
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
