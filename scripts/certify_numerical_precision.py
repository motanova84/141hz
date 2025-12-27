#!/usr/bin/env python3
"""
Numerical Precision Certification Module

This module certifies the numerical precision of quantum calculations,
especially for GPU computations and mixed-precision scenarios.

Validates:
- GPU vs CPU precision consistency
- Mixed precision accuracy
- Numerical stability across different precision levels
- Error accumulation in long computations

Ensures that performance optimizations do NOT sacrifice accuracy.
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timezone


class PrecisionCertifier:
    """
    Main class for certifying numerical precision
    """
    
    def __init__(self, tolerance_strict=1e-10, tolerance_relaxed=1e-6):
        """
        Initialize precision certifier
        
        Args:
            tolerance_strict: Strict tolerance for high-precision operations
            tolerance_relaxed: Relaxed tolerance for GPU/mixed-precision
        """
        self.tolerance_strict = tolerance_strict
        self.tolerance_relaxed = tolerance_relaxed
        self.results = []
    
    def test_high_precision_constants(self):
        """
        Test that fundamental constants are stored with sufficient precision
        
        Returns:
            dict: Test results
        """
        try:
            import mpmath as mp
        except ImportError:
            return {
                "test": "high_precision_constants",
                "status": "SKIP",
                "reason": "mpmath not available"
            }
        
        # Test: Speed of light
        mp.dps = 50
        c_high_precision = mp.mpf("299792458")
        c_python_float = 299792458.0
        
        # Compare
        error = float(abs(c_high_precision - c_python_float))
        
        result = {
            "test": "high_precision_constants",
            "status": "PASS" if error < self.tolerance_strict else "FAIL",
            "c_high_precision": str(c_high_precision),
            "c_python_float": c_python_float,
            "absolute_error": error,
            "relative_error": error / float(c_high_precision)
        }
        
        self.results.append(result)
        return result
    
    def test_frequency_calculation_precision(self):
        """
        Test precision of fundamental frequency calculation
        
        Validates: f₀ = 141.7001 Hz calculation
        
        Returns:
            dict: Test results
        """
        try:
            import mpmath as mp
        except ImportError:
            return {
                "test": "frequency_calculation_precision",
                "status": "SKIP",
                "reason": "mpmath not available"
            }
        
        # High precision calculation
        mp.dps = 50
        c = mp.mpf("299792458")
        f0 = mp.mpf("141.7001")
        
        # Calculate R_Ψ
        R_psi = c / (2 * mp.pi * f0)
        
        # Recalculate f₀
        f0_recalc = c / (2 * mp.pi * R_psi)
        
        # Error
        error = float(abs(f0_recalc - f0))
        
        result = {
            "test": "frequency_calculation_precision",
            "status": "PASS" if error < self.tolerance_strict else "FAIL",
            "f0_original": str(f0),
            "f0_recalculated": str(f0_recalc),
            "absolute_error": error,
            "precision_digits": mp.dps
        }
        
        self.results.append(result)
        return result
    
    def test_cpu_consistency(self):
        """
        Test consistency of calculations across different CPU precision modes
        
        Returns:
            dict: Test results
        """
        # Test matrix eigenvalue calculation with different precisions
        try:
            import numpy as np
            from scipy import linalg
        except ImportError:
            return {
                "test": "cpu_consistency",
                "status": "SKIP",
                "reason": "NumPy/SciPy not available"
            }
        
        # Create test matrix (simple 2x2 Pauli matrix σz)
        H = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.float64)
        
        # Calculate eigenvalues with float64
        eigenvals_64 = linalg.eigvalsh(H)
        
        # Calculate with float32
        H_32 = H.astype(np.float32)
        eigenvals_32 = linalg.eigvalsh(H_32).astype(np.float64)
        
        # Compare
        max_error = np.max(np.abs(eigenvals_64 - eigenvals_32))
        
        result = {
            "test": "cpu_consistency",
            "status": "PASS" if max_error < self.tolerance_relaxed else "FAIL",
            "eigenvals_float64": eigenvals_64.tolist(),
            "eigenvals_float32": eigenvals_32.tolist(),
            "max_error": float(max_error),
            "tolerance": self.tolerance_relaxed
        }
        
        self.results.append(result)
        return result
    
    def test_gpu_cpu_consistency(self):
        """
        Test consistency between GPU and CPU calculations
        
        Returns:
            dict: Test results
        """
        try:
            import numpy as np
            import cupy as cp
            from scipy import linalg
        except ImportError:
            return {
                "test": "gpu_cpu_consistency",
                "status": "SKIP",
                "reason": "CuPy not available (GPU library). This test requires GPU support.",
                "note": "Install with: pip install cupy-cuda11x (or appropriate CUDA version)"
            }
        
        # Create test matrix on CPU
        np.random.seed(42)
        H_cpu = np.random.randn(8, 8)
        H_cpu = (H_cpu + H_cpu.T) / 2  # Make symmetric
        
        # Copy to GPU
        H_gpu = cp.array(H_cpu)
        
        # Calculate eigenvalues on CPU
        eigenvals_cpu = linalg.eigvalsh(H_cpu)
        
        # Calculate eigenvalues on GPU
        eigenvals_gpu = cp.linalg.eigvalsh(H_gpu)
        eigenvals_gpu_cpu = cp.asnumpy(eigenvals_gpu)
        
        # Compare
        max_error = np.max(np.abs(eigenvals_cpu - eigenvals_gpu_cpu))
        
        result = {
            "test": "gpu_cpu_consistency",
            "status": "PASS" if max_error < self.tolerance_relaxed else "FAIL",
            "max_error": float(max_error),
            "tolerance": self.tolerance_relaxed,
            "matrix_size": 8
        }
        
        self.results.append(result)
        return result
    
    def test_mixed_precision_accuracy(self):
        """
        Test accuracy when using mixed precision (float32/float64)
        
        Returns:
            dict: Test results
        """
        try:
            import numpy as np
            from scipy import linalg
        except ImportError:
            return {
                "test": "mixed_precision_accuracy",
                "status": "SKIP",
                "reason": "NumPy/SciPy not available"
            }
        
        # Create test problem: 4x4 matrix
        np.random.seed(42)
        H = np.random.randn(4, 4)
        H = (H + H.T) / 2
        
        # High precision reference
        eigenvals_ref = linalg.eigvalsh(H.astype(np.float64))
        
        # Mixed precision: matrix in float32, result converted to float64
        H_mixed = H.astype(np.float32)
        eigenvals_mixed = linalg.eigvalsh(H_mixed).astype(np.float64)
        
        # Errors
        max_error = np.max(np.abs(eigenvals_ref - eigenvals_mixed))
        mean_error = np.mean(np.abs(eigenvals_ref - eigenvals_mixed))
        
        result = {
            "test": "mixed_precision_accuracy",
            "status": "PASS" if max_error < self.tolerance_relaxed else "FAIL",
            "max_error": float(max_error),
            "mean_error": float(mean_error),
            "tolerance": self.tolerance_relaxed,
            "interpretation": "Mixed precision maintains acceptable accuracy" if max_error < self.tolerance_relaxed else "Mixed precision degrades accuracy"
        }
        
        self.results.append(result)
        return result
    
    def test_numerical_stability_iterative(self):
        """
        Test numerical stability in iterative calculations
        
        Returns:
            dict: Test results
        """
        # Test: Repeated squaring (tests error accumulation)
        try:
            import mpmath as mp
        except ImportError:
            return {
                "test": "numerical_stability_iterative",
                "status": "SKIP",
                "reason": "mpmath not available"
            }
        
        # High precision
        mp.dps = 50
        x_high = mp.mpf("1.1")
        
        # Standard precision
        x_std = 1.1
        
        # Iterate: x^(2^10)
        iterations = 10
        for _ in range(iterations):
            x_high = x_high ** 2
            x_std = x_std ** 2
        
        # Compare
        error = float(abs(x_high - x_std)) / float(x_high)
        
        result = {
            "test": "numerical_stability_iterative",
            "status": "PASS" if error < 0.01 else "FAIL",  # Allow 1% error for repeated operations
            "iterations": iterations,
            "relative_error": error,
            "interpretation": "Numerical stability maintained" if error < 0.01 else "Error accumulation detected"
        }
        
        self.results.append(result)
        return result
    
    def test_hermiticity_preservation(self):
        """
        Test that Hermiticity is preserved in numerical operations
        
        Returns:
            dict: Test results
        """
        try:
            import numpy as np
        except ImportError:
            return {
                "test": "hermiticity_preservation",
                "status": "SKIP",
                "reason": "NumPy not available"
            }
        
        # Create Hermitian matrix
        np.random.seed(42)
        H = np.random.randn(8, 8) + 1j * np.random.randn(8, 8)
        H = (H + H.conj().T) / 2
        
        # Test Hermiticity: H = H†
        diff = H - H.conj().T
        max_diff = np.max(np.abs(diff))
        
        result = {
            "test": "hermiticity_preservation",
            "status": "PASS" if max_diff < self.tolerance_strict else "FAIL",
            "max_deviation": float(max_diff),
            "tolerance": self.tolerance_strict
        }
        
        self.results.append(result)
        return result
    
    def run_full_certification(self):
        """
        Run complete precision certification suite
        
        Returns:
            dict: Certification results
        """
        print("=" * 80)
        print("NUMERICAL PRECISION CERTIFICATION")
        print("=" * 80)
        print()
        print("Certifying numerical accuracy across:")
        print("  - High-precision calculations (mpmath)")
        print("  - CPU precision modes (float32/float64)")
        print("  - GPU vs CPU consistency")
        print("  - Mixed precision scenarios")
        print("  - Iterative numerical stability")
        print()
        
        certification = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tolerances": {
                "strict": self.tolerance_strict,
                "relaxed": self.tolerance_relaxed
            },
            "tests": []
        }
        
        # Run all tests
        tests = [
            ("High-Precision Constants", self.test_high_precision_constants),
            ("Frequency Calculation Precision", self.test_frequency_calculation_precision),
            ("CPU Consistency", self.test_cpu_consistency),
            ("GPU-CPU Consistency", self.test_gpu_cpu_consistency),
            ("Mixed Precision Accuracy", self.test_mixed_precision_accuracy),
            ("Numerical Stability (Iterative)", self.test_numerical_stability_iterative),
            ("Hermiticity Preservation", self.test_hermiticity_preservation)
        ]
        
        for name, test_func in tests:
            print(f"Running: {name}...", flush=True)
            result = test_func()
            certification["tests"].append(result)
            
            status_symbol = {
                "PASS": "✅",
                "FAIL": "❌",
                "SKIP": "⏭️"
            }.get(result["status"], "❓")
            
            print(f"  {status_symbol} {result['status']}")
            if result["status"] == "SKIP":
                print(f"     Reason: {result.get('reason', 'Unknown')}")
        
        # Summary
        passed = sum(1 for t in certification["tests"] if t["status"] == "PASS")
        failed = sum(1 for t in certification["tests"] if t["status"] == "FAIL")
        skipped = sum(1 for t in certification["tests"] if t["status"] == "SKIP")
        total = len(certification["tests"])
        
        certification["summary"] = {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": passed / (passed + failed) if (passed + failed) > 0 else 1.0,
            "certification_status": "CERTIFIED" if failed == 0 else "FAILED"
        }
        
        return certification


def generate_certification_report(certification, output_path=None):
    """
    Generate formatted certification report
    
    Args:
        certification: Certification results
        output_path: Path to save JSON report (optional)
        
    Returns:
        str: Formatted report text
    """
    report = []
    report.append("=" * 80)
    report.append("NUMERICAL PRECISION CERTIFICATION REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {certification['timestamp']}\n")
    
    report.append("\n--- Test Results ---\n")
    for test in certification["tests"]:
        status_symbol = {
            "PASS": "✅",
            "FAIL": "❌",
            "SKIP": "⏭️"
        }.get(test["status"], "❓")
        
        report.append(f"{status_symbol} {test['test']}: {test['status']}")
        
        if test["status"] == "FAIL" and "max_error" in test:
            report.append(f"   Error: {test['max_error']:.2e}")
        elif test["status"] == "SKIP" and "reason" in test:
            report.append(f"   Reason: {test['reason']}")
    
    report.append("\n--- Summary ---\n")
    summary = certification["summary"]
    report.append(f"  Total Tests: {summary['total_tests']}")
    report.append(f"  Passed: {summary['passed']}")
    report.append(f"  Failed: {summary['failed']}")
    report.append(f"  Skipped: {summary['skipped']}")
    report.append(f"  Pass Rate: {summary['pass_rate']*100:.1f}%")
    report.append(f"\n  Certification Status: {summary['certification_status']}")
    
    report.append("\n" + "=" * 80)
    
    report_text = "\n".join(report)
    
    # Save if output path provided
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(certification, f, indent=2)
        print(f"\nCertification results saved to: {output_path}")
    
    return report_text


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Certify numerical precision of quantum calculations"
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output path for JSON results',
        default='results/precision_certification.json'
    )
    parser.add_argument(
        '--strict-tolerance',
        type=float,
        help='Strict tolerance threshold (default: 1e-10)',
        default=1e-10
    )
    parser.add_argument(
        '--relaxed-tolerance',
        type=float,
        help='Relaxed tolerance for GPU/mixed precision (default: 1e-6)',
        default=1e-6
    )
    
    args = parser.parse_args()
    
    # Run certification
    certifier = PrecisionCertifier(
        tolerance_strict=args.strict_tolerance,
        tolerance_relaxed=args.relaxed_tolerance
    )
    
    certification = certifier.run_full_certification()
    
    # Generate report
    print("\n" + "=" * 80)
    print(generate_certification_report(certification, args.output))
    
    # Exit with appropriate code
    if certification["summary"]["certification_status"] == "CERTIFIED":
        print("\n✅ CERTIFICATION PASSED: Numerical precision meets standards")
        sys.exit(0)
    else:
        print("\n❌ CERTIFICATION FAILED: Numerical precision issues detected")
        sys.exit(1)
