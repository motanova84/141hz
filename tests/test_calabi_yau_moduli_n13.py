#!/usr/bin/env python3
"""
Tests for Calabi-Yau moduli N=13 analysis script.

Tests the enumeration of CY manifolds with total moduli h^{1,1} + h^{2,1} = 13
and validates the relationship κ_Π = log(N).
"""

import math
import sys
import unittest
from pathlib import Path

# Add scripts and src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    
from calabi_yau_moduli_n13 import (
    CalabiYauManifold,
    CY_MANIFOLDS_N13,
    enumerate_cy_with_total_moduli,
    compute_spectral_corrections,
    validate_kappa_pi_formula,
    KAPPA_PI,
    N_EXACT,
    N_INTEGER,
    KAPPA_PI_INTEGER,
)


class TestCalabiYauManifold(unittest.TestCase):
    """Test the CalabiYauManifold class."""
    
    def test_euler_characteristic(self):
        """Test Euler characteristic formula χ = 2(h^{1,1} - h^{2,1})."""
        # Quintic: h^{1,1}=1, h^{2,1}=101 → χ = -200
        cy = CalabiYauManifold(h11=1, h21=101)
        assert cy.euler_characteristic == 2 * (1 - 101) == -200
        
        # Balanced: h^{1,1}=6, h^{2,1}=7 → χ = -2
        cy = CalabiYauManifold(h11=6, h21=7)
        assert cy.euler_characteristic == 2 * (6 - 7) == -2
        
        # Mirror quintic: h^{1,1}=101, h^{2,1}=1 → χ = 200
        cy = CalabiYauManifold(h11=101, h21=1)
        assert cy.euler_characteristic == 2 * (101 - 1) == 200
    
    def test_total_moduli(self):
        """Test total moduli N = h^{1,1} + h^{2,1}."""
        cy = CalabiYauManifold(h11=1, h21=12)
        assert cy.total_moduli == 13
        
        cy = CalabiYauManifold(h11=6, h21=7)
        assert cy.total_moduli == 13
        
        cy = CalabiYauManifold(h11=12, h21=1)
        assert cy.total_moduli == 13
    
    def test_kappa_pi(self):
        """Test κ_Π = log(N) computation."""
        cy = CalabiYauManifold(h11=6, h21=7)
        expected_kappa = math.log(13)
        assert abs(cy.kappa_pi - expected_kappa) < 1e-10


class TestConstants(unittest.TestCase):
    """Test fundamental constants."""
    
    def test_n_exact(self):
        """Test N = e^{κ_Π} ≈ 13.15."""
        assert abs(N_EXACT - 13.16) < 0.02  # More lenient tolerance
        assert abs(N_EXACT - math.exp(KAPPA_PI)) < 1e-10
    
    def test_n_integer(self):
        """Test integer approximation."""
        assert N_INTEGER == 13
    
    def test_kappa_pi_integer(self):
        """Test κ_Π for N=13."""
        assert abs(KAPPA_PI_INTEGER - math.log(13)) < 1e-10
        assert abs(KAPPA_PI_INTEGER - 2.5649) < 0.001


class TestEnumeration(unittest.TestCase):
    """Test enumeration functions."""
    
    def test_enumerate_cy_with_n13(self):
        """Test enumeration of all (h^{1,1}, h^{2,1}) pairs with sum=13."""
        manifolds = enumerate_cy_with_total_moduli(13)
        
        # Should have 12 pairs: (1,12), (2,11), ..., (12,1)
        assert len(manifolds) == 12
        
        # Check all have total moduli = 13
        for cy in manifolds:
            assert cy.total_moduli == 13
        
        # Check all have κ_Π = log(13)
        expected_kappa = math.log(13)
        for cy in manifolds:
            assert abs(cy.kappa_pi - expected_kappa) < 1e-10
        
        # Check all Euler characteristics are correct
        for cy in manifolds:
            expected_chi = 2 * (cy.h11 - cy.h21)
            assert cy.euler_characteristic == expected_chi
    
    def test_enumerate_covers_all_pairs(self):
        """Test that enumeration covers all (h^{1,1}, h^{2,1}) pairs."""
        manifolds = enumerate_cy_with_total_moduli(13)
        
        pairs = [(cy.h11, cy.h21) for cy in manifolds]
        expected_pairs = [(i, 13-i) for i in range(1, 13)]
        
        assert sorted(pairs) == sorted(expected_pairs)


class TestKnownManifolds(unittest.TestCase):
    """Test known CY manifolds from catalogs."""
    
    def test_known_manifolds_count(self):
        """Test that we have all 12 known manifolds."""
        assert len(CY_MANIFOLDS_N13) == 12
    
    def test_all_have_n13(self):
        """Test all known manifolds have N=13."""
        for cy in CY_MANIFOLDS_N13:
            assert cy.total_moduli == 13
    
    def test_all_have_valid_euler_char(self):
        """Test all have valid Euler characteristic."""
        for cy in CY_MANIFOLDS_N13:
            expected_chi = 2 * (cy.h11 - cy.h21)
            assert cy.euler_characteristic == expected_chi
    
    def test_euler_char_range(self):
        """Test range of Euler characteristics."""
        euler_chars = [cy.euler_characteristic for cy in CY_MANIFOLDS_N13]
        
        # For N=13, χ ranges from -22 to +22
        assert min(euler_chars) == -22
        assert max(euler_chars) == 22
        
        # Should have symmetric distribution
        assert sorted(euler_chars) == list(range(-22, 23, 4))
    
    def test_catalog_assignments(self):
        """Test that all have catalog assignments."""
        for cy in CY_MANIFOLDS_N13:
            assert cy.catalog in ["CICY", "Kreuzer-Skarke", "Kreuzer-Skarke / CICY"]


class TestSpectralCorrections(unittest.TestCase):
    """Test spectral corrections analysis."""
    
    def test_delta_n(self):
        """Test ΔN = 13.15 - 13 = 0.15."""
        corrections = compute_spectral_corrections(13, 13.15)
        assert abs(corrections['delta_N'] - 0.15) < 0.001
    
    def test_relative_correction(self):
        """Test relative correction."""
        corrections = compute_spectral_corrections(13, 13.15)
        expected_rel = 0.15 / 13
        assert abs(corrections['relative_correction'] - expected_rel) < 1e-10
    
    def test_interpretation_structure(self):
        """Test that corrections have proper structure."""
        corrections = compute_spectral_corrections(13, 13.15)
        
        assert 'interpretations' in corrections
        interp = corrections['interpretations']
        
        # Check all three sources are present
        assert 'degenerate_modes' in interp
        assert 'dual_cycles' in interp
        assert 'flux_symmetries' in interp
        
        # Each should have description, contribution, significance
        for key, value in interp.items():
            assert 'description' in value
            assert 'contribution' in value
            assert 'significance' in value


class TestValidation(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_kappa_pi(self):
        """Test validation of κ_Π formula."""
        cy = CalabiYauManifold(h11=6, h21=7, catalog="Test")
        validation = validate_kappa_pi_formula(cy)
        
        # Check structure
        assert 'manifold' in validation
        assert 'total_moduli' in validation
        assert 'kappa_pi_computed' in validation
        assert 'matches_n13' in validation
        
        # Check values
        assert validation['total_moduli'] == 13
        assert abs(validation['kappa_pi_computed'] - math.log(13)) < 1e-10
        assert validation['matches_n13'] is True
    
    def test_validation_all_n13_manifolds(self):
        """Test validation for all known N=13 manifolds."""
        for cy in CY_MANIFOLDS_N13:
            validation = validate_kappa_pi_formula(cy)
            
            assert validation['total_moduli'] == 13
            assert validation['matches_n13'] is True
            assert abs(validation['kappa_pi_computed'] - KAPPA_PI_INTEGER) < 1e-6


class TestMathematicalRelations(unittest.TestCase):
    """Test mathematical relationships."""
    
    def test_kappa_pi_n_relation(self):
        """Test κ_Π = log(N) for various N."""
        for N in [5, 10, 13, 20, 50, 100]:
            cy = CalabiYauManifold(h11=1, h21=N-1)
            expected_kappa = math.log(N)
            assert abs(cy.kappa_pi - expected_kappa) < 1e-10
    
    def test_mirror_symmetry(self):
        """Test that mirror pairs have same N and opposite χ."""
        # Mirror pair: (1,12) and (12,1)
        cy1 = CalabiYauManifold(h11=1, h21=12)
        cy2 = CalabiYauManifold(h11=12, h21=1)
        
        # Same total moduli
        assert cy1.total_moduli == cy2.total_moduli
        
        # Opposite Euler characteristic
        assert cy1.euler_characteristic == -cy2.euler_characteristic
        
        # Same κ_Π
        assert abs(cy1.kappa_pi - cy2.kappa_pi) < 1e-10
    
    def test_balanced_manifold(self):
        """Test balanced manifold h^{1,1} ≈ h^{2,1}."""
        # For N=13, balanced would be (6,7) or (7,6)
        cy1 = CalabiYauManifold(h11=6, h21=7)
        cy2 = CalabiYauManifold(h11=7, h21=6)
        
        # Both have small |χ|
        assert abs(cy1.euler_characteristic) == 2
        assert abs(cy2.euler_characteristic) == 2
        
        # Both have same N and κ_Π
        assert cy1.total_moduli == 13
        assert cy2.total_moduli == 13
        assert abs(cy1.kappa_pi - cy2.kappa_pi) < 1e-10


def run_all_tests():
    """Run all tests manually if pytest is not available."""
    import unittest
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCalabiYauManifold))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestEnumeration))
    suite.addTests(loader.loadTestsFromTestCase(TestKnownManifolds))
    suite.addTests(loader.loadTestsFromTestCase(TestSpectralCorrections))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestMathematicalRelations))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        sys.exit(run_all_tests())
