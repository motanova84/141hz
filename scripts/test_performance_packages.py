#!/usr/bin/env python3
"""
Test script to validate that numba, llvmlite, python-igraph, and numexpr
are properly installed and working with system dependencies.
"""

import sys


def test_numba():
    """Test numba with llvmlite"""
    try:
        import numba
        import numpy as np
        
        @numba.jit(nopython=True)
        def test_function(x):
            return x * 2 + 1
        
        # Test with scalar
        result = test_function(5)
        assert result == 11, f"Expected 11, got {result}"
        
        # Test with array
        arr = np.array([1, 2, 3])
        result_arr = test_function(arr)
        expected = np.array([3, 5, 7])
        assert np.array_equal(result_arr, expected), f"Expected {expected}, got {result_arr}"
        
        print(f"✅ numba {numba.__version__} - JIT compilation works correctly")
        return True
    except Exception as e:
        print(f"❌ numba test failed: {e}")
        return False


def test_llvmlite():
    """Test llvmlite"""
    try:
        import llvmlite
        print(f"✅ llvmlite {llvmlite.__version__} - Imported successfully")
        return True
    except Exception as e:
        print(f"❌ llvmlite test failed: {e}")
        return False


def test_igraph():
    """Test python-igraph with libigraph"""
    try:
        import igraph as ig
        
        # Create a simple graph
        g = ig.Graph(edges=[(0, 1), (1, 2), (2, 0)])
        
        assert g.vcount() == 3, f"Expected 3 vertices, got {g.vcount()}"
        assert g.ecount() == 3, f"Expected 3 edges, got {g.ecount()}"
        
        # Test operations
        degrees = g.degree()
        assert degrees == [2, 2, 2], f"Expected [2, 2, 2], got {degrees}"
        
        print(f"✅ python-igraph {ig.__version__} - Graph operations work correctly")
        return True
    except Exception as e:
        print(f"❌ igraph test failed: {e}")
        return False


def test_numexpr():
    """Test numexpr CPU detection"""
    try:
        import numexpr as ne
        import numpy as np
        
        # Test computation
        x = np.arange(1000)
        y = np.arange(1000)
        
        result = ne.evaluate("x**2 + y**2")
        expected = x**2 + y**2
        
        assert np.allclose(result, expected), "Computation mismatch"
        
        # Check thread settings
        max_threads = ne.detect_number_of_cores()
        print(f"✅ numexpr {ne.__version__} - Computation works, detected {max_threads} cores")
        return True
    except Exception as e:
        print(f"❌ numexpr test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("Testing Performance Packages Installation")
    print("=" * 70)
    print()
    
    tests = [
        ("llvmlite", test_llvmlite),
        ("numba", test_numba),
        ("python-igraph", test_igraph),
        ("numexpr", test_numexpr),
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
        print()
    
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20s}: {status}")
    
    print()
    if all_passed:
        print("🎉 All tests passed! System dependencies are properly configured.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
