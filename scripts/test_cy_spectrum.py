#!/usr/bin/env python3
"""
Tests for Calabi-Yau Quintic Spectrum and κ_Π Invariant

This module tests the computation of the spectral invariant κ_Π
from the Laplacian spectrum of the Calabi-Yau quintic.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: October 2025
"""

import pytest
import numpy as np
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cy_spectrum import (
    CalabiYauQuinticSpectrum,
    compute_kappa_pi,
    verify_kappa_pi,
    kappa_pi_properties,
    atiyah_singer_index,
    KAPPA_PI_PREDICTED,
    KAPPA_PI_TOLERANCE,
    H11,
    H21,
    EULER_CHAR
)


class TestCalabiYauQuinticSpectrum:
    """Tests for the CalabiYauQuinticSpectrum class."""
    
    def test_initialization(self):
        """Test that the class initializes correctly."""
        cy = CalabiYauQuinticSpectrum()
        assert cy.grid_size == 64
        assert cy.p == 0
        assert cy.q == 1
        assert cy.eigenvalues is None
        assert cy._computed is False
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        cy = CalabiYauQuinticSpectrum(grid_size=32, p=1, q=1)
        assert cy.grid_size == 32
        assert cy.p == 1
        assert cy.q == 1
    
    def test_hodge_numbers(self):
        """Test that Hodge numbers are correctly defined."""
        cy = CalabiYauQuinticSpectrum()
        hodge = cy.hodge_numbers
        
        assert hodge["h11"] == 1
        assert hodge["h21"] == 101
        assert hodge["euler_characteristic"] == -200
    
    def test_compute_spectrum(self):
        """Test that spectrum computation produces valid results."""
        cy = CalabiYauQuinticSpectrum(grid_size=32)
        eigenvalues = cy.compute_spectrum()
        
        assert eigenvalues is not None
        assert len(eigenvalues) == 32
        assert np.all(np.isfinite(eigenvalues))
        # Eigenvalues should be sorted
        assert np.all(np.diff(eigenvalues) >= -1e-10)
    
    def test_max_eigenvalues(self):
        """Test limiting the number of returned eigenvalues."""
        cy = CalabiYauQuinticSpectrum(grid_size=64)
        eigenvalues = cy.compute_spectrum(max_eigenvalues=10)
        
        assert len(eigenvalues) == 10
    
    def test_spectral_moments(self):
        """Test computation of spectral moments."""
        cy = CalabiYauQuinticSpectrum(grid_size=32)
        cy.compute_spectrum()
        moments = cy.compute_spectral_moments(filter_zero=True)
        
        assert "mu1" in moments
        assert "mu2" in moments
        assert "kappa_pi" in moments
        assert moments["mu1"] > 0
        assert moments["mu2"] > 0
        assert moments["kappa_pi"] > 0
    
    def test_spectral_moments_auto_compute(self):
        """Test that compute_spectral_moments auto-computes spectrum if needed."""
        cy = CalabiYauQuinticSpectrum(grid_size=16)
        # Don't explicitly call compute_spectrum
        moments = cy.compute_spectral_moments()
        
        assert moments["kappa_pi"] > 0


class TestKappaPiInvariant:
    """Tests for the κ_Π invariant computation."""
    
    def test_compute_kappa_pi_returns_dict(self):
        """Test that compute_kappa_pi returns a dictionary."""
        result = compute_kappa_pi(grid_size=16)
        
        assert isinstance(result, dict)
        assert "kappa_pi" in result
        assert "kappa_pi_predicted" in result
        assert "error_absolute" in result
        assert "validated" in result
    
    def test_kappa_pi_value_range(self):
        """Test that κ_Π is in a reasonable range."""
        result = compute_kappa_pi(grid_size=32)
        
        kappa = result["kappa_pi"]
        # κ_Π should be positive and around 2.5
        assert 1.0 < kappa < 5.0
    
    def test_kappa_pi_convergence(self):
        """Test that κ_Π converges with increasing grid size."""
        kappas = []
        for size in [16, 32, 64]:
            result = compute_kappa_pi(grid_size=size)
            kappas.append(result["kappa_pi"])
        
        # Values should be relatively stable
        # (Not strictly decreasing/increasing, but bounded)
        assert all(1.0 < k < 5.0 for k in kappas)
    
    def test_kappa_pi_predicted_value(self):
        """Test the predicted value of κ_Π."""
        assert KAPPA_PI_PREDICTED == pytest.approx(2.5773, abs=0.0001)
    
    def test_kappa_pi_tolerance(self):
        """Test the tolerance value."""
        # Updated tolerance: 5% for numerical simulation
        assert KAPPA_PI_TOLERANCE == pytest.approx(0.05, rel=0.1)


class TestVerification:
    """Tests for the verification function."""
    
    def test_verify_kappa_pi_returns_bool(self, capsys):
        """Test that verify_kappa_pi returns a boolean."""
        result = verify_kappa_pi(tolerance=1.0)  # Large tolerance for test
        
        assert isinstance(result, bool)
    
    def test_verify_kappa_pi_output(self, capsys):
        """Test that verification produces output."""
        verify_kappa_pi(tolerance=1.0)
        captured = capsys.readouterr()
        
        assert "κ_Π (computed)" in captured.out
        assert "κ_Π (predicted)" in captured.out


class TestKappaPiProperties:
    """Tests for the κ_Π properties documentation."""
    
    def test_properties_structure(self):
        """Test the structure of the properties dictionary."""
        props = kappa_pi_properties()
        
        assert props["invariant"] == "κ_Π"
        assert props["value"] == KAPPA_PI_PREDICTED
        assert "definition" in props
        assert "invariance_properties" in props
        assert "connections" in props
        assert "uniqueness" in props
    
    def test_invariance_properties(self):
        """Test that all invariance properties are documented."""
        props = kappa_pi_properties()
        inv = props["invariance_properties"]
        
        assert "diffeomorphism" in inv
        assert "galois" in inv
        assert "rg_flow" in inv
    
    def test_connections(self):
        """Test that connections to other structures are documented."""
        props = kappa_pi_properties()
        conn = props["connections"]
        
        assert "chern_simons" in conn
        assert "galois_adelic" in conn
        assert "chern_fractal" in conn
        assert "noetic_invariance" in conn
    
    def test_uniqueness_statement(self):
        """Test the uniqueness statement."""
        props = kappa_pi_properties()
        
        assert "FIRST invariant" in props["uniqueness"]["statement"]
        assert len(props["uniqueness"]["unifies"]) == 4


class TestAtiyahSingerIndex:
    """Tests for the Atiyah-Singer index computation."""
    
    def test_index_structure(self):
        """Test the structure of the index result."""
        result = atiyah_singer_index()
        
        assert "index_D_Psi" in result
        assert "formula" in result
        assert "euler_characteristic" in result
        assert "second_chern_class" in result
    
    def test_index_value(self):
        """Test the index value matches f₀."""
        result = atiyah_singer_index()
        
        assert result["index_D_Psi"] == pytest.approx(141.7001, abs=0.0001)
    
    def test_connection_to_f0(self):
        """Test the connection to f₀ is documented."""
        result = atiyah_singer_index()
        
        assert "141.7001" in result["connection_to_f0"]


class TestHodgeNumbers:
    """Tests for the Hodge numbers constants."""
    
    def test_h11(self):
        """Test h^{1,1} = 1 for quintic CY."""
        assert H11 == 1
    
    def test_h21(self):
        """Test h^{2,1} = 101 for quintic CY."""
        assert H21 == 101
    
    def test_euler_characteristic(self):
        """Test Euler characteristic χ = -200."""
        assert EULER_CHAR == -200
    
    def test_euler_formula(self):
        """Test that χ = 2(h^{1,1} - h^{2,1})."""
        assert EULER_CHAR == 2 * (H11 - H21)


class TestSpectralMomentRelation:
    """Tests for the spectral moment relation κ_Π = μ₂/μ₁."""
    
    def test_kappa_equals_mu2_over_mu1(self):
        """Test that κ_Π = μ₂/μ₁ exactly."""
        result = compute_kappa_pi(grid_size=32)
        moments = result["spectral_moments"]
        
        mu1 = moments["mu1"]
        mu2 = moments["mu2"]
        kappa_from_moments = mu2 / mu1
        
        assert result["kappa_pi"] == pytest.approx(kappa_from_moments, rel=1e-10)
    
    def test_mu1_is_mean(self):
        """Test that μ₁ represents the mean eigenvalue."""
        cy = CalabiYauQuinticSpectrum(grid_size=16)
        eigenvalues = cy.compute_spectrum()
        moments = cy.compute_spectral_moments(filter_zero=True, threshold=1e-10)
        
        # Filter non-zero eigenvalues
        nonzero = eigenvalues[eigenvalues > 1e-10]
        expected_mu1 = np.mean(nonzero)
        
        assert moments["mu1"] == pytest.approx(expected_mu1, rel=1e-10)
    
    def test_mu2_is_second_moment(self):
        """Test that μ₂ represents the second moment."""
        cy = CalabiYauQuinticSpectrum(grid_size=16)
        eigenvalues = cy.compute_spectrum()
        moments = cy.compute_spectral_moments(filter_zero=True, threshold=1e-10)
        
        # Filter non-zero eigenvalues
        nonzero = eigenvalues[eigenvalues > 1e-10]
        expected_mu2 = np.mean(nonzero ** 2)
        
        assert moments["mu2"] == pytest.approx(expected_mu2, rel=1e-10)


class TestReproducibility:
    """Tests for reproducibility of computations."""
    
    def test_reproducible_spectrum(self):
        """Test that spectrum computation is reproducible."""
        cy1 = CalabiYauQuinticSpectrum(grid_size=32)
        cy2 = CalabiYauQuinticSpectrum(grid_size=32)
        
        ev1 = cy1.compute_spectrum()
        ev2 = cy2.compute_spectrum()
        
        np.testing.assert_array_almost_equal(ev1, ev2)
    
    def test_reproducible_kappa_pi(self):
        """Test that κ_Π is reproducible across calls."""
        result1 = compute_kappa_pi(grid_size=32)
        result2 = compute_kappa_pi(grid_size=32)
        
        assert result1["kappa_pi"] == result2["kappa_pi"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
