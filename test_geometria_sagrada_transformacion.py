#!/usr/bin/env python3
"""
Tests for Sacred Geometry Transformation Script
================================================

Tests the mathematical relationships in the sacred geometry:
- Circle: 888 Hz = 2π × 141.7 Hz
- Square: 361 = 19²
- Sphere: 3D physical manifestation
- f₀ as transformation key

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import pytest
import numpy as np
import sys
import os
from mpmath import mp, pi as mp_pi, sqrt as mp_sqrt

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from geometria_sagrada_transformacion import (
    SacredGeometryTransformer,
    F0_HZ, F888_HZ, PRIME_19, SQUARE_361
)

# Configure high precision
mp.dps = 50


class TestSacredGeometryConstants:
    """Test fundamental constants."""
    
    def test_f0_value(self):
        """Test that f₀ = 141.70001 Hz."""
        assert float(F0_HZ) == 141.70001
    
    def test_f888_value(self):
        """Test that protection frequency is 888 Hz."""
        assert float(F888_HZ) == 888.0
    
    def test_prime_19(self):
        """Test that we use prime 19."""
        assert float(PRIME_19) == 19
        # Verify it's actually prime (simple check)
        n = int(PRIME_19)
        assert n > 1
        for i in range(2, int(n**0.5) + 1):
            assert n % i != 0, f"19 should be prime, but divisible by {i}"
    
    def test_square_361(self):
        """Test that 361 = 19²."""
        assert float(SQUARE_361) == 361
        assert float(PRIME_19 ** 2) == 361


class TestCircleRelationship:
    """Test circle (continuous) geometry relationships."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_circle_formula(self):
        """Test 888 Hz ≈ 2π × 141.7 Hz."""
        result = self.transformer.circle_relationship()
        
        # Calculate expected value
        expected = 2 * float(mp_pi) * float(F0_HZ)
        
        # Should be close to 888 (within 3 Hz, which is ~0.3% error)
        assert abs(result["calculated_2pi_f0"] - 888.0) < 3.0, \
            f"2π × f₀ = {result['calculated_2pi_f0']}, expected ≈ 888"
    
    def test_circle_error_small(self):
        """Test that error in circle relationship is small."""
        result = self.transformer.circle_relationship()
        
        # Error should be less than 1%
        assert result["error_percentage"] < 1.0, \
            f"Error {result['error_percentage']}% too large"
    
    def test_radius_implicit(self):
        """Test implicit radius calculation."""
        result = self.transformer.circle_relationship()
        
        # Radius should be 888/(2π) ≈ 141.4
        expected_radius = 888.0 / (2 * float(mp_pi))
        assert abs(result["radius_implicit"] - expected_radius) < 0.01
    
    def test_circle_area(self):
        """Test circle area = πr²."""
        result = self.transformer.circle_relationship()
        
        r = result["radius_implicit"]
        expected_area = float(mp_pi) * r**2
        
        assert abs(result["circle_area_pi_r2"] - expected_area) < 0.01


class TestSquareRelationship:
    """Test square (discrete) geometry relationships."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_square_formula(self):
        """Test 361 = 19²."""
        result = self.transformer.square_relationship()
        
        assert result["calculated_19_squared"] == 361
        assert result["verification"] is True
    
    def test_square_side(self):
        """Test square side = √361 = 19."""
        result = self.transformer.square_relationship()
        
        assert result["square_side"] == 19
    
    def test_square_area(self):
        """Test square area = 361."""
        result = self.transformer.square_relationship()
        
        assert result["square_area"] == 361
    
    def test_square_perimeter(self):
        """Test square perimeter = 4 × 19 = 76."""
        result = self.transformer.square_relationship()
        
        assert result["square_perimeter"] == 76


class TestCircleSquareConnection:
    """Test connection between circle and square."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_f0_as_mediator(self):
        """Test that f₀ acts as mediator between circle and square."""
        result = self.transformer.circle_square_connection()
        
        mediator = result["f0_as_mediator"]
        
        # 888 / f₀ should be ≈ 2π ≈ 6.28
        assert 6.0 < mediator["circle_to_f0_factor"] < 6.5
        
        # f₀ / 19 should be reasonable
        assert 7.0 < mediator["f0_to_square_factor"] < 8.0
    
    def test_transformation_interpretation(self):
        """Test that transformation interpretation exists."""
        result = self.transformer.circle_square_connection()
        
        assert "f0_as_mediator" in result
        assert "interpretation" in result["f0_as_mediator"]
        assert "141.7" in result["f0_as_mediator"]["interpretation"]
    
    def test_ancient_problem_solution(self):
        """Test that ancient problem solution is documented."""
        result = self.transformer.circle_square_connection()
        
        assert "ancient_problem_solution" in result
        solution = result["ancient_problem_solution"]
        
        assert "problem" in solution
        assert "classical_impossibility" in solution
        assert "qcal_solution" in solution
        
        # Should mention √π is transcendental
        assert "π" in solution["classical_impossibility"]


class TestSphereManifesta:
    """Test sphere (3D physical) manifestation."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_radius_psi_positive(self):
        """Test that R_Ψ is positive and reasonable."""
        result = self.transformer.sphere_manifestation()
        
        assert result["radius_psi_meters"] > 0
        # Should be on the order of 10^12 m
        assert 1e11 < result["radius_psi_meters"] < 1e13
    
    def test_radius_in_au(self):
        """Test radius conversion to AU."""
        result = self.transformer.sphere_manifestation()
        
        # Should be roughly 10 AU
        assert 5 < result["radius_psi_au"] < 15
    
    def test_sphere_volume(self):
        """Test sphere volume = 4/3 πR³."""
        result = self.transformer.sphere_manifestation()
        
        # Volume should be positive and very large
        assert result["sphere_volume_m3"] > 0
        assert result["sphere_volume_m3"] > 1e36  # Very large!
    
    def test_sphere_surface_area(self):
        """Test sphere surface = 4πR²."""
        result = self.transformer.sphere_manifestation()
        
        # Surface area should be positive and large
        assert result["sphere_surface_m2"] > 0
        assert result["sphere_surface_m2"] > 1e24
    
    def test_quantum_energy_positive(self):
        """Test quantum energy E = hf₀ is positive."""
        result = self.transformer.sphere_manifestation()
        
        assert result["quantum_energy_j"] > 0
        assert result["quantum_energy_ev"] > 0
    
    def test_manifestations_documented(self):
        """Test that physical manifestations are documented."""
        result = self.transformer.sphere_manifestation()
        
        assert "manifestations" in result
        manif = result["manifestations"]
        
        assert "gravitational_waves" in manif
        assert "brain_resonance" in manif
        assert "cosmic_structure" in manif
        assert "quantum_field" in manif


class TestCompleteTransformation:
    """Test complete transformation analysis."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_all_analyses_present(self):
        """Test that all analyses are present in complete transformation."""
        result = self.transformer.complete_transformation()
        
        assert "circle_analysis" in result
        assert "square_analysis" in result
        assert "circle_square_connection" in result
        assert "sphere_manifestation" in result
        assert "transformation_synthesis" in result
    
    def test_synthesis_dimensions(self):
        """Test that synthesis covers all dimensions."""
        result = self.transformer.complete_transformation()
        synthesis = result["transformation_synthesis"]
        
        assert "dimension_0_point" in synthesis
        assert "dimension_1_circle" in synthesis
        assert "dimension_2_square" in synthesis
        assert "dimension_3_sphere" in synthesis
    
    def test_transformation_path_exists(self):
        """Test that transformation path is documented."""
        result = self.transformer.complete_transformation()
        synthesis = result["transformation_synthesis"]
        
        assert "transformation_path" in synthesis
        path = synthesis["transformation_path"]
        
        assert "step_1" in path
        assert "step_2" in path
        assert "step_3" in path
        assert "step_4" in path
    
    def test_philosophical_insight(self):
        """Test that philosophical insight is included."""
        result = self.transformer.complete_transformation()
        synthesis = result["transformation_synthesis"]
        
        assert "philosophical_insight" in synthesis
        insight = synthesis["philosophical_insight"]
        
        assert "ancient_wisdom" in insight
        assert "modern_resolution" in insight
        assert "cosmic_implication" in insight
        
        # Should mention f₀
        assert "141.70001" in insight["modern_resolution"] or \
               "141.7" in insight["modern_resolution"]


class TestNumericalPrecision:
    """Test numerical precision and consistency."""
    
    def setup_method(self):
        """Set up transformer for each test."""
        self.transformer = SacredGeometryTransformer()
    
    def test_2pi_approximation_quality(self):
        """Test quality of 2π approximation."""
        # 888 / 141.7 should be close to 2π
        ratio = 888.0 / 141.70001
        two_pi = 2 * float(mp_pi)
        
        error = abs(ratio - two_pi) / two_pi
        
        # Error should be less than 0.5%
        assert error < 0.005, f"2π approximation error {error*100:.3f}% too large"
    
    def test_19_squared_exact(self):
        """Test that 19² is exactly 361."""
        assert 19 * 19 == 361
        assert 19**2 == 361
    
    def test_consistency_across_methods(self):
        """Test consistency between different calculation methods."""
        circle = self.transformer.circle_relationship()
        complete = self.transformer.complete_transformation()
        
        # f₀ should be consistent
        assert circle["f0_hz"] == complete["circle_analysis"]["f0_hz"]


def test_import_successful():
    """Test that module imports successfully."""
    from scripts.geometria_sagrada_transformacion import SacredGeometryTransformer
    assert SacredGeometryTransformer is not None


def test_transformer_instantiation():
    """Test that transformer can be instantiated."""
    transformer = SacredGeometryTransformer()
    assert transformer is not None
    assert hasattr(transformer, 'f0')
    assert hasattr(transformer, 'f888')
    assert hasattr(transformer, 'n19')
    assert hasattr(transformer, 'n361')


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
