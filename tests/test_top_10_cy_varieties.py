#!/usr/bin/env python3
"""
Tests for Top 10 Calabi-Yau Varieties Script

Tests the generation of the Top 10 CY varieties table with spectral
invariants κ_Π computed from geometric parameters α and β.
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from top_10_cy_varieties import (
    compute_alpha_beta,
    compute_kappa_pi,
    generate_cy_table,
    CY_DATABASE
)


class TestAlphaBetaComputation:
    """Test suite for α and β geometric parameter computation."""

    def test_quintic_alpha_beta(self):
        """Test α and β for the quintic CY (h¹¹=1, h²¹=101)."""
        alpha, beta = compute_alpha_beta(1, 101)
        
        # α should be around 0.385
        assert 0.380 <= alpha <= 0.390
        
        # β should be around 0.244
        assert 0.239 <= beta <= 0.249

    def test_alpha_increases_with_h11(self):
        """Test that α increases as h¹¹ increases."""
        alpha1, _ = compute_alpha_beta(1, 101)
        alpha2, _ = compute_alpha_beta(5, 65)
        alpha3, _ = compute_alpha_beta(12, 48)
        
        # α should increase with h¹¹
        assert alpha1 <= alpha2 <= alpha3

    def test_beta_decreases_with_h11(self):
        """Test that β decreases (or stays similar) as h¹¹ increases."""
        _, beta1 = compute_alpha_beta(1, 101)
        _, beta2 = compute_alpha_beta(5, 65)
        _, beta3 = compute_alpha_beta(12, 48)
        
        # β should decrease or stay similar with increasing h¹¹
        assert beta1 >= beta2 >= beta3 or abs(beta1 - beta3) < 0.01

    def test_alpha_beta_positive(self):
        """Test that α and β are always positive."""
        for h11 in [1, 2, 5, 10, 20]:
            for h21 in [48, 65, 83, 101]:
                alpha, beta = compute_alpha_beta(h11, h21)
                assert alpha > 0
                assert beta > 0


class TestKappaPiComputation:
    """Test suite for κ_Π spectral invariant computation."""

    def test_quintic_kappa_pi(self):
        """Test κ_Π for the quintic CY."""
        alpha, beta = compute_alpha_beta(1, 101)
        kappa_pi = compute_kappa_pi(alpha, beta, 1, 101)
        
        # κ_Π should be around 1.658-1.665
        assert 1.650 <= kappa_pi <= 1.670

    def test_kappa_pi_decreases_with_alpha(self):
        """Test that κ_Π decreases as α increases."""
        # Generate parameters for three varieties with increasing α
        alpha1, beta1 = compute_alpha_beta(1, 101)
        alpha2, beta2 = compute_alpha_beta(5, 65)
        alpha3, beta3 = compute_alpha_beta(12, 48)
        
        kappa1 = compute_kappa_pi(alpha1, beta1, 1, 101)
        kappa2 = compute_kappa_pi(alpha2, beta2, 5, 65)
        kappa3 = compute_kappa_pi(alpha3, beta3, 12, 48)
        
        # κ_Π should decrease as α increases
        assert kappa1 >= kappa2
        assert kappa2 >= kappa3

    def test_kappa_pi_positive(self):
        """Test that κ_Π is always positive."""
        for h11 in [1, 2, 5, 10]:
            for h21 in [48, 65, 83, 101]:
                alpha, beta = compute_alpha_beta(h11, h21)
                kappa_pi = compute_kappa_pi(alpha, beta, h11, h21)
                assert kappa_pi > 0

    def test_kappa_pi_in_expected_range(self):
        """Test that κ_Π values are in expected physical range."""
        # Test a sample of varieties
        for variety in CY_DATABASE[:5]:
            h11 = variety["h11"]
            h21 = variety["h21"]
            alpha, beta = compute_alpha_beta(h11, h21)
            kappa_pi = compute_kappa_pi(alpha, beta, h11, h21)
            
            # κ_Π should be between 1.0 and 2.0 for physical systems
            assert 1.0 <= kappa_pi <= 2.0


class TestTableGeneration:
    """Test suite for table generation."""

    def test_generate_top_10(self):
        """Test generating top 10 varieties."""
        results = generate_cy_table(CY_DATABASE, top_n=10)
        
        assert len(results) == 10
        assert results[0]["id"] == "CY-001"
        assert results[9]["id"] == "CY-010"

    def test_table_structure(self):
        """Test that each table entry has required fields."""
        results = generate_cy_table(CY_DATABASE, top_n=3)
        
        required_fields = ["id", "name", "h11", "h21", "alpha", "beta", 
                          "kappa_pi", "chi"]
        
        for entry in results:
            for field in required_fields:
                assert field in entry

    def test_euler_characteristic(self):
        """Test that χ = 2(h¹¹ - h²¹) for all entries."""
        results = generate_cy_table(CY_DATABASE, top_n=10)
        
        for entry in results:
            expected_chi = 2 * (entry["h11"] - entry["h21"])
            assert entry["chi"] == expected_chi

    def test_kappa_pi_decreasing_trend(self):
        """Test that κ_Π generally decreases in the top 10 list."""
        results = generate_cy_table(CY_DATABASE, top_n=10)
        
        kappa_values = [r["kappa_pi"] for r in results]
        
        # Check that the first value is larger than the last
        assert kappa_values[0] >= kappa_values[-1]
        
        # Check that most consecutive pairs show decrease
        decreasing_pairs = sum(1 for i in range(len(kappa_values)-1)
                              if kappa_values[i] >= kappa_values[i+1])
        
        # At least 70% of pairs should show decrease
        assert decreasing_pairs >= 0.7 * (len(kappa_values) - 1)


class TestCYDatabase:
    """Test suite for CY database integrity."""

    def test_database_not_empty(self):
        """Test that the database is not empty."""
        assert len(CY_DATABASE) > 0

    def test_database_has_at_least_10(self):
        """Test that database has at least 10 varieties."""
        assert len(CY_DATABASE) >= 10

    def test_quintic_in_database(self):
        """Test that the quintic CY is in the database."""
        quintic = [v for v in CY_DATABASE if v["id"] == "CY-001"]
        assert len(quintic) == 1
        assert quintic[0]["h11"] == 1
        assert quintic[0]["h21"] == 101

    def test_all_entries_have_required_fields(self):
        """Test that all database entries have required fields."""
        required_fields = ["id", "name", "h11", "h21"]
        
        for variety in CY_DATABASE:
            for field in required_fields:
                assert field in variety


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
