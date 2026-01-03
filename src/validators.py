#!/usr/bin/env python3
"""
Validation Classes for V5 Coronacion
=====================================

This module provides modular validation classes for the V5 coronacion
validation pipeline with improved error handling.

Author: José Manuel Mota Burruezo (JMMB)
"""

from pathlib import Path
from typing import Dict, Any

try:
    import mpmath as mp
except ImportError:
    raise ImportError(
        "mpmath is required for high-precision calculations. "
        "Install with: pip install mpmath"
    )

# Try relative imports first, fall back for compatibility
try:
    from . import exceptions
    from . import utils
except ImportError:
    import exceptions
    import utils


class QuantumFrequencyValidator:
    """Validator for quantum frequency calculations."""
    
    def __init__(self, precision: int = 30):
        """
        Initialize the validator.
        
        Args:
            precision: Number of decimal places for calculations
            
        Raises:
            PrecisionError: If precision is invalid
        """
        if precision < 10:
            raise exceptions.PrecisionError(
                required_precision=precision,
                message="Precision must be at least 10 decimal places"
            )
        
        self.precision = precision
        self.logger = utils.setup_logging()
        mp.dps = precision
        
        # Constants
        self.f0_observed = mp.mpf("141.7001")
        self.c = mp.mpf("299792458")
        self.h = mp.mpf("6.62607015e-34")
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate the fundamental quantum frequency f₀ = 141.7001 Hz.
        
        Returns:
            dict: Validation results with frequency and precision details
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            self.logger.info(f"Validating quantum frequency with precision={self.precision}")
            
            # Calculate R_Ψ from observed frequency
            R_psi = self.c / (2 * mp.pi * self.f0_observed)
            
            # Calculate quantum energy E_Ψ = hf₀
            E_psi = self.h * self.f0_observed
            
            # Validate symmetry: R_Ψ ↔ 1/R_Ψ
            R_psi_inverse = 1 / R_psi
            symmetry_ratio = R_psi * R_psi_inverse
            
            deviation = abs(float(symmetry_ratio) - 1.0)
            status = "PASS" if deviation < 1e-10 else "FAIL"
            
            if status == "FAIL":
                raise exceptions.ValidationError(
                    validation_name="quantum_frequency",
                    expected=1.0,
                    actual=float(symmetry_ratio),
                    message=f"Symmetry check failed with deviation {deviation}"
                )
            
            return {
                "f0_hz": float(self.f0_observed),
                "R_psi_m": float(R_psi),
                "E_psi_joules": float(E_psi),
                "symmetry_check": float(symmetry_ratio),
                "precision_digits": self.precision,
                "status": status
            }
            
        except ValidationError:
            raise
        except Exception as e:
            raise exceptions.ValidationError(
                validation_name="quantum_frequency",
                message=f"Unexpected error during validation: {str(e)}"
            )


class CompactificationRadiusValidator:
    """Validator for quantum compactification radius."""
    
    def __init__(self, precision: int = 30):
        """
        Initialize the validator.
        
        Args:
            precision: Number of decimal places for calculations
        """
        if precision < 10:
            raise exceptions.PrecisionError(
                required_precision=precision,
                message="Precision must be at least 10 decimal places"
            )
        
        self.precision = precision
        self.logger = utils.setup_logging()
        mp.dps = precision
        
        # Constants
        self.c = mp.mpf("299792458")
        self.f0 = mp.mpf("141.7001")
        self.R_psi_min = mp.mpf("336000")
        self.R_psi_max = mp.mpf("337000")
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate the quantum compactification radius R_Ψ.
        
        Returns:
            dict: Validation results for compactification radius
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            self.logger.info(f"Validating compactification radius with precision={self.precision}")
            
            # Calculate R_Ψ
            R_psi = self.c / (2 * mp.pi * self.f0)
            
            # Check range
            in_range = self.R_psi_min <= R_psi <= self.R_psi_max
            status = "PASS" if in_range else "FAIL"
            
            if status == "FAIL":
                raise exceptions.ValidationError(
                    validation_name="compactification_radius",
                    expected=f"[{float(self.R_psi_min)}, {float(self.R_psi_max)}]",
                    actual=float(R_psi),
                    message=f"R_Ψ = {float(R_psi)} m is outside expected range"
                )
            
            return {
                "R_psi_calculated": float(R_psi),
                "R_psi_min_expected": float(self.R_psi_min),
                "R_psi_max_expected": float(self.R_psi_max),
                "in_expected_range": in_range,
                "precision_digits": self.precision,
                "status": status
            }
            
        except ValidationError:
            raise
        except Exception as e:
            raise exceptions.ValidationError(
                validation_name="compactification_radius",
                message=f"Unexpected error during validation: {str(e)}"
            )


class DiscreteSymmetryValidator:
    """Validator for discrete R_Ψ ↔ 1/R_Ψ symmetry."""
    
    def __init__(self, precision: int = 30):
        """
        Initialize the validator.
        
        Args:
            precision: Number of decimal places for calculations
        """
        if precision < 10:
            raise exceptions.PrecisionError(
                required_precision=precision,
                message="Precision must be at least 10 decimal places"
            )
        
        self.precision = precision
        self.logger = utils.setup_logging()
        mp.dps = precision
        
        # Constants
        self.c = mp.mpf("299792458")
        self.f0 = mp.mpf("141.7001")
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate the discrete R_Ψ ↔ 1/R_Ψ symmetry.
        
        Returns:
            dict: Validation results for discrete symmetry
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            self.logger.info(f"Validating discrete symmetry with precision={self.precision}")
            
            # Calculate R_Ψ
            R_psi = self.c / (2 * mp.pi * self.f0)
            
            # Test symmetry transformation
            R_psi_dual = 1 / R_psi
            
            # Check that R_Ψ * (1/R_Ψ) = 1
            symmetry_product = R_psi * R_psi_dual
            deviation = abs(symmetry_product - 1)
            
            status = "PASS" if float(deviation) < 1e-20 else "FAIL"
            
            if status == "FAIL":
                raise exceptions.ValidationError(
                    validation_name="discrete_symmetry",
                    expected=1.0,
                    actual=float(symmetry_product),
                    message=f"Symmetry product deviation {float(deviation)} exceeds tolerance"
                )
            
            return {
                "R_psi": float(R_psi),
                "R_psi_dual": float(R_psi_dual),
                "symmetry_product": float(symmetry_product),
                "deviation_from_unity": float(deviation),
                "precision_digits": self.precision,
                "status": status
            }
            
        except ValidationError:
            raise
        except Exception as e:
            raise exceptions.ValidationError(
                validation_name="discrete_symmetry",
                message=f"Unexpected error during validation: {str(e)}"
            )


class ValidationOrchestrator:
    """Orchestrates all validation checks."""
    
    def __init__(self, precision: int = 30):
        """
        Initialize the orchestrator.
        
        Args:
            precision: Number of decimal places for calculations
        """
        self.precision = precision
        self.logger = utils.setup_logging()
        
        # Initialize validators
        self.freq_validator = QuantumFrequencyValidator(precision)
        self.radius_validator = CompactificationRadiusValidator(precision)
        self.symmetry_validator = DiscreteSymmetryValidator(precision)
    
    def run_all(self) -> Dict[str, Any]:
        """
        Run complete validation suite.
        
        Returns:
            dict: Complete validation results
        """
        from datetime import datetime, timezone
        
        self.logger.info("=" * 70)
        self.logger.info(f"VALIDATE V5 CORONACION - Precision: {self.precision} digits")
        self.logger.info("=" * 70)
        
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "precision_digits": self.precision,
            "validation_suite": "v5_coronacion",
        }
        
        # Run quantum frequency validation
        try:
            self.logger.info("🔬 Validating quantum frequency...")
            freq_results = self.freq_validator.validate()
            self.logger.info(f"   ✓ f₀ = {freq_results['f0_hz']} Hz")
            self.logger.info(f"   ✓ Status: {freq_results['status']}")
            results["quantum_frequency"] = freq_results
        except ValidationError as e:
            self.logger.error(f"   ✗ Quantum frequency validation failed: {e}")
            results["quantum_frequency"] = {
                "status": "FAIL",
                "error": str(e),
                "details": e.details
            }
        
        # Run compactification radius validation
        try:
            self.logger.info("🔬 Validating compactification radius...")
            radius_results = self.radius_validator.validate()
            self.logger.info(f"   ✓ R_Ψ = {radius_results['R_psi_calculated']:.2f} m")
            self.logger.info(f"   ✓ Status: {radius_results['status']}")
            results["compactification_radius"] = radius_results
        except ValidationError as e:
            self.logger.error(f"   ✗ Compactification radius validation failed: {e}")
            results["compactification_radius"] = {
                "status": "FAIL",
                "error": str(e),
                "details": e.details
            }
        
        # Run discrete symmetry validation
        try:
            self.logger.info("🔬 Validating discrete symmetry...")
            symmetry_results = self.symmetry_validator.validate()
            self.logger.info(f"   ✓ Symmetry deviation: {symmetry_results['deviation_from_unity']:.2e}")
            self.logger.info(f"   ✓ Status: {symmetry_results['status']}")
            results["discrete_symmetry"] = symmetry_results
        except ValidationError as e:
            self.logger.error(f"   ✗ Discrete symmetry validation failed: {e}")
            results["discrete_symmetry"] = {
                "status": "FAIL",
                "error": str(e),
                "details": e.details
            }
        
        # Calculate summary
        all_statuses = [
            results.get("quantum_frequency", {}).get("status", "FAIL"),
            results.get("compactification_radius", {}).get("status", "FAIL"),
            results.get("discrete_symmetry", {}).get("status", "FAIL")
        ]
        
        tests_passed = sum(1 for status in all_statuses if status == "PASS")
        tests_failed = sum(1 for status in all_statuses if status == "FAIL")
        
        results["overall_status"] = "PASS" if tests_failed == 0 else "FAIL"
        results["summary"] = {
            "tests_run": 3,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed
        }
        
        self.logger.info("=" * 70)
        self.logger.info(f"VALIDATION RESULTS: {results['overall_status']}")
        self.logger.info("=" * 70)
        self.logger.info(f"Tests passed: {tests_passed}/3")
        self.logger.info("=" * 70)
        
        return results
