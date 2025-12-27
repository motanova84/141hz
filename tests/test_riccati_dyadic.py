#!/usr/bin/env python3
"""
Test Suite for Dyadic Riccati Coefficient Analysis

This test suite validates the mathematical implementation of scale-dependent
dissipation analysis for Navier-Stokes equations.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'computational-tests'))

from DyadicAnalysis import (
    RiccatiParameters,
    dyadic_riccati_coefficient,
    find_dissipative_scale,
    verify_dyadic_analysis
)


class TestRiccatiParameters:
    """Test RiccatiParameters dataclass."""
    
    def test_default_parameters(self):
        """Test default parameter initialization."""
        params = RiccatiParameters()
        assert params.ν == 1e-3
        assert params.C_BKM == 2.0
        assert params.logK == 1.0
        assert params.dimension == 3
    
    def test_invalid_viscosity(self):
        """Test that negative viscosity raises error."""
        with pytest.raises(ValueError):
            RiccatiParameters(ν=-0.1)
    
    def test_invalid_dimension(self):
        """Test that invalid dimension raises error."""
        with pytest.raises(ValueError):
            RiccatiParameters(dimension=4)


class TestDyadicRiccatiCoefficient:
    """Test dyadic Riccati coefficient calculations."""
    
    def test_coefficient_sign_change(self):
        """Test that coefficient becomes negative at high scales."""
        params = RiccatiParameters()
        δ_star = 0.0253
        
        # Low scale should be positive (stretching dominates)
        α_low = dyadic_riccati_coefficient(0, δ_star, params)
        assert α_low > 0, "Low scale should have positive coefficient"
        
        # High scale should be negative (dissipation dominates)
        α_high = dyadic_riccati_coefficient(10, δ_star, params)
        assert α_high < 0, "High scale should have negative coefficient"
    
    def test_scale_dependence(self):
        """Test that dissipation grows exponentially with scale."""
        params = RiccatiParameters()
        δ_star = 0.0253
        
        α_6 = dyadic_riccati_coefficient(6, δ_star, params)
        α_8 = dyadic_riccati_coefficient(8, δ_star, params)
        
        # α should decrease rapidly (become more negative)
        assert α_8 < α_6
        assert abs(α_8) > 4 * abs(α_6)  # Roughly 2^4 factor
    
    def test_invalid_scale(self):
        """Test that invalid scale raises error."""
        params = RiccatiParameters()
        δ_star = 0.0253
        
        with pytest.raises(ValueError):
            dyadic_riccati_coefficient(-2, δ_star, params)
    
    def test_invalid_regularization(self):
        """Test that invalid δ* raises error."""
        params = RiccatiParameters()
        
        with pytest.raises(ValueError):
            dyadic_riccati_coefficient(0, -0.1, params)
        
        with pytest.raises(ValueError):
            dyadic_riccati_coefficient(0, 1.5, params)


class TestFindDissipativeScale:
    """Test dissipative scale finder."""
    
    def test_finds_dissipative_scale(self):
        """Test that dissipative scale is found."""
        params = RiccatiParameters()
        δ_qcal = 1 / (4 * np.pi**2)
        
        j_d = find_dissipative_scale(δ_qcal, params)
        assert j_d > 0, "Should find dissipative scale"
        assert j_d < 15, "Dissipative scale should be reasonable"
    
    def test_quantum_calibration(self):
        """Test with quantum calibration parameters."""
        params = RiccatiParameters(ν=1e-3)
        δ_qcal = 1 / (4 * np.pi**2)  # ≈ 0.0253
        
        j_d = find_dissipative_scale(δ_qcal, params)
        
        # Should be around j = 7-8 for these parameters
        assert 5 <= j_d <= 10, f"Expected j_d around 7, got {j_d}"
        
        # Verify it's actually dissipative at that scale
        α_jd = dyadic_riccati_coefficient(j_d, δ_qcal, params)
        assert α_jd < 0, "Coefficient should be negative at dissipative scale"
    
    def test_viscosity_dependence(self):
        """Test that higher viscosity gives lower dissipative scale."""
        δ_qcal = 1 / (4 * np.pi**2)
        
        params_low = RiccatiParameters(ν=1e-4)
        params_high = RiccatiParameters(ν=1e-2)
        
        j_d_low = find_dissipative_scale(δ_qcal, params_low)
        j_d_high = find_dissipative_scale(δ_qcal, params_high)
        
        assert j_d_high < j_d_low, "Higher viscosity should give lower j_d"


class TestVerifyDyadicAnalysis:
    """Test full dyadic analysis verification."""
    
    def test_verification_returns_dict(self):
        """Test that verification returns proper dictionary."""
        results = verify_dyadic_analysis(verbose=False)
        
        assert isinstance(results, dict)
        assert "δ_star" in results
        assert "j_dissipative" in results
        assert "α_coefficients" in results
        assert "status" in results
    
    def test_verification_passes(self):
        """Test that verification passes with default parameters."""
        results = verify_dyadic_analysis(verbose=False)
        
        assert results["status"] == "PASS"
        assert results["j_dissipative"] > 0
    
    def test_custom_parameters(self):
        """Test verification with custom parameters."""
        params = RiccatiParameters(ν=1e-3, C_BKM=2.5)
        δ_star = 0.03
        
        results = verify_dyadic_analysis(
            δ_star=δ_star,
            params=params,
            verbose=False
        )
        
        assert results["δ_star"] == δ_star
        assert results["viscosity_ν"] == params.ν
        assert results["C_BKM"] == params.C_BKM


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
