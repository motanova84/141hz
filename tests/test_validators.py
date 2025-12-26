#!/usr/bin/env python3
"""
Tests for Validation Classes Module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from validators import (
    QuantumFrequencyValidator,
    CompactificationRadiusValidator,
    DiscreteSymmetryValidator,
    ValidationOrchestrator
)
from exceptions import ValidationError, PrecisionError


class TestQuantumFrequencyValidator:
    """Test quantum frequency validator."""
    
    def test_basic_validation(self):
        """Test basic quantum frequency validation."""
        validator = QuantumFrequencyValidator(precision=20)
        result = validator.validate()
        
        assert result["status"] == "PASS"
        assert result["f0_hz"] == pytest.approx(141.7001, abs=1e-4)
        assert result["precision_digits"] == 20
        assert "R_psi_m" in result
        assert "E_psi_joules" in result
    
    def test_symmetry_check(self):
        """Test symmetry check passes."""
        validator = QuantumFrequencyValidator(precision=30)
        result = validator.validate()
        
        # Symmetry should be very close to 1.0
        assert result["symmetry_check"] == pytest.approx(1.0, abs=1e-10)
    
    def test_invalid_precision(self):
        """Test that invalid precision raises error."""
        with pytest.raises(PrecisionError):
            QuantumFrequencyValidator(precision=5)


class TestCompactificationRadiusValidator:
    """Test compactification radius validator."""
    
    def test_basic_validation(self):
        """Test basic radius validation."""
        validator = CompactificationRadiusValidator(precision=20)
        result = validator.validate()
        
        assert result["status"] == "PASS"
        assert result["precision_digits"] == 20
        assert result["in_expected_range"] is True
        
        # Check R_Ψ is in expected range (336-337 km)
        R_psi = result["R_psi_calculated"]
        assert 336000 <= R_psi <= 337000
    
    def test_radius_calculation(self):
        """Test radius calculation accuracy."""
        validator = CompactificationRadiusValidator(precision=30)
        result = validator.validate()
        
        # R_Ψ = c/(2πf₀) where c = 299792458 m/s and f₀ = 141.7001 Hz
        # Expected: ~336721.37 m
        assert result["R_psi_calculated"] == pytest.approx(336721.37, abs=1.0)
    
    def test_invalid_precision(self):
        """Test that invalid precision raises error."""
        with pytest.raises(PrecisionError):
            CompactificationRadiusValidator(precision=8)


class TestDiscreteSymmetryValidator:
    """Test discrete symmetry validator."""
    
    def test_basic_validation(self):
        """Test basic symmetry validation."""
        validator = DiscreteSymmetryValidator(precision=20)
        result = validator.validate()
        
        assert result["status"] == "PASS"
        assert result["precision_digits"] == 20
        assert "R_psi" in result
        assert "R_psi_dual" in result
    
    def test_symmetry_product(self):
        """Test that R_Ψ * (1/R_Ψ) = 1."""
        validator = DiscreteSymmetryValidator(precision=30)
        result = validator.validate()
        
        # Product should be exactly 1
        assert result["symmetry_product"] == pytest.approx(1.0, abs=1e-15)
        
        # Deviation should be very small
        assert result["deviation_from_unity"] < 1e-20
    
    def test_dual_relationship(self):
        """Test relationship between R_Ψ and its dual."""
        validator = DiscreteSymmetryValidator(precision=25)
        result = validator.validate()
        
        R_psi = result["R_psi"]
        R_psi_dual = result["R_psi_dual"]
        
        # R_psi_dual should equal 1/R_psi
        assert R_psi_dual == pytest.approx(1.0 / R_psi, rel=1e-10)
    
    def test_invalid_precision(self):
        """Test that invalid precision raises error."""
        with pytest.raises(PrecisionError):
            DiscreteSymmetryValidator(precision=9)


class TestValidationOrchestrator:
    """Test validation orchestrator."""
    
    def test_run_all_validations(self):
        """Test running all validations."""
        orchestrator = ValidationOrchestrator(precision=20)
        results = orchestrator.run_all()
        
        # Check overall structure
        assert "timestamp" in results
        assert "precision_digits" in results
        assert results["precision_digits"] == 20
        assert "validation_suite" in results
        assert results["validation_suite"] == "v5_coronacion"
        
        # Check individual validations
        assert "quantum_frequency" in results
        assert "compactification_radius" in results
        assert "discrete_symmetry" in results
        
        # Check summary
        assert "summary" in results
        assert results["summary"]["tests_run"] == 3
        
        # Check overall status
        assert "overall_status" in results
    
    def test_all_validations_pass(self):
        """Test that all validations pass with valid precision."""
        orchestrator = ValidationOrchestrator(precision=25)
        results = orchestrator.run_all()
        
        # All tests should pass
        assert results["quantum_frequency"]["status"] == "PASS"
        assert results["compactification_radius"]["status"] == "PASS"
        assert results["discrete_symmetry"]["status"] == "PASS"
        
        # Overall status should be PASS
        assert results["overall_status"] == "PASS"
        assert results["summary"]["tests_passed"] == 3
        assert results["summary"]["tests_failed"] == 0
    
    def test_different_precisions(self):
        """Test with different precision values."""
        for precision in [15, 20, 25, 30]:
            orchestrator = ValidationOrchestrator(precision=precision)
            results = orchestrator.run_all()
            
            assert results["precision_digits"] == precision
            assert results["overall_status"] == "PASS"
    
    def test_invalid_precision(self):
        """Test that orchestrator rejects invalid precision."""
        with pytest.raises(PrecisionError):
            ValidationOrchestrator(precision=5)


class TestValidationIntegration:
    """Integration tests for validation system."""
    
    def test_end_to_end_validation(self):
        """Test complete end-to-end validation flow."""
        # Create orchestrator
        orchestrator = ValidationOrchestrator(precision=30)
        
        # Run all validations
        results = orchestrator.run_all()
        
        # Verify complete results structure
        assert isinstance(results, dict)
        assert results["overall_status"] == "PASS"
        
        # Verify quantum frequency results
        qf = results["quantum_frequency"]
        assert qf["f0_hz"] == pytest.approx(141.7001, abs=1e-4)
        assert 9.3e-32 < qf["E_psi_joules"] < 9.4e-32
        
        # Verify compactification radius results
        cr = results["compactification_radius"]
        assert 336000 < cr["R_psi_calculated"] < 337000
        
        # Verify discrete symmetry results
        ds = results["discrete_symmetry"]
        assert ds["deviation_from_unity"] < 1e-20
    
    def test_consistency_across_precisions(self):
        """Test that results are consistent across different precisions."""
        results_20 = ValidationOrchestrator(precision=20).run_all()
        results_30 = ValidationOrchestrator(precision=30).run_all()
        
        # f0 should be the same
        assert (results_20["quantum_frequency"]["f0_hz"] == 
                results_30["quantum_frequency"]["f0_hz"])
        
        # R_Ψ should be very similar (within numerical precision)
        R_psi_20 = results_20["compactification_radius"]["R_psi_calculated"]
        R_psi_30 = results_30["compactification_radius"]["R_psi_calculated"]
        assert R_psi_20 == pytest.approx(R_psi_30, rel=1e-10)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
