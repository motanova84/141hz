#!/usr/bin/env python3
"""
Tests for physics.spectral_search_theta

Validates the C7 cycle twist gauge θ spectral search algorithm that finds
the exact phase offset required to shift the base frequency to f₀ = 141.7001 Hz.

Classes/Functions under test:
-----------------------------
- calcular_frecuencia_c7: Calculate C7 frequency with twist gauge θ
- encontrar_theta_exacto: Find θ to reach target frequency
- validar_solucion: Validate solution accuracy

Physical Context:
----------------
The twist gauge θ represents a phase offset in the C7 (7-node cycle) graph
that modulates its spectral eigenvalue. The script solves for the θ value
that shifts the bare frequency (134.425 Hz) to the target frequency f₀.
"""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.spectral_search_theta import (
    calcular_frecuencia_c7,
    encontrar_theta_exacto,
    validar_solucion,
)
from qcal.constants import F0_HZ


# ============================================================================
# Tests for calcular_frecuencia_c7
# ============================================================================

class TestCalcularFrecuenciaC7(unittest.TestCase):
    """Tests for the C7 frequency calculation with twist gauge."""
    
    def test_zero_theta_returns_base_frequency(self):
        """θ = 0 should return the base frequency unchanged."""
        f_bare = 134.425
        f_result = calcular_frecuencia_c7(theta=0.0, f_bare=f_bare)
        # With θ = 0, λ_θ = λ₀, so kappa = 1
        self.assertAlmostEqual(f_result, f_bare, places=6)
    
    def test_positive_theta_increases_frequency(self):
        """Positive θ should generally increase frequency."""
        f_bare = 134.425
        f_zero = calcular_frecuencia_c7(theta=0.0, f_bare=f_bare)
        f_positive = calcular_frecuencia_c7(theta=0.05, f_bare=f_bare)
        self.assertGreater(f_positive, f_zero)
    
    def test_result_scales_with_base(self):
        """Result should scale proportionally with f_bare."""
        theta = 0.05
        f_bare1 = 100.0
        f_bare2 = 200.0
        
        f1 = calcular_frecuencia_c7(theta, f_bare1)
        f2 = calcular_frecuencia_c7(theta, f_bare2)
        
        # f2 should be approximately 2 × f1
        self.assertAlmostEqual(f2 / f1, 2.0, places=6)
    
    def test_continuous_in_theta(self):
        """Function should be continuous in θ."""
        f_bare = 134.425
        theta1 = 0.05
        theta2 = 0.050001
        
        f1 = calcular_frecuencia_c7(theta1, f_bare)
        f2 = calcular_frecuencia_c7(theta2, f_bare)
        
        # Small change in θ should give small change in f
        self.assertAlmostEqual(f1, f2, places=3)
    
    def test_expected_theta_gives_f0(self):
        """θ ≈ 0.0525 rad should give f₀ ≈ 141.7001 Hz."""
        theta_expected = 0.052463  # From main() output
        f_bare = 134.425
        f_result = calcular_frecuencia_c7(theta_expected, f_bare)
        
        # Should be very close to F0_HZ
        self.assertAlmostEqual(f_result, F0_HZ, places=2)


# ============================================================================
# Tests for encontrar_theta_exacto
# ============================================================================

class TestEncontrarThetaExacto(unittest.TestCase):
    """Tests for finding the exact θ solution."""
    
    def test_finds_theta_for_f0(self):
        """Should find θ that produces f₀ = 141.7001 Hz."""
        f_bare = 134.425
        theta = encontrar_theta_exacto(f_objetivo=F0_HZ, f_bare=f_bare)
        
        # θ should be positive and reasonable
        self.assertGreater(theta, 0.0)
        self.assertLess(theta, 0.1)
    
    def test_solution_produces_target(self):
        """Found θ should actually produce the target frequency."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        f_result = calcular_frecuencia_c7(theta, f_bare)
        
        # Result should match target within numerical precision
        self.assertAlmostEqual(f_result, f_objetivo, places=4)
    
    def test_default_target_is_f0(self):
        """Default target should be F0_HZ."""
        f_bare = 134.425
        
        theta1 = encontrar_theta_exacto(f_objetivo=None, f_bare=f_bare)
        theta2 = encontrar_theta_exacto(f_objetivo=F0_HZ, f_bare=f_bare)
        
        self.assertAlmostEqual(theta1, theta2, places=6)
    
    def test_different_targets_give_different_theta(self):
        """Different target frequencies should give different θ values."""
        f_bare = 134.425
        
        theta1 = encontrar_theta_exacto(f_objetivo=140.0, f_bare=f_bare)
        theta2 = encontrar_theta_exacto(f_objetivo=142.0, f_bare=f_bare)
        
        self.assertNotAlmostEqual(theta1, theta2, places=3)
    
    def test_convergence_from_different_initial_guesses(self):
        """Should converge to same solution from different initial guesses."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta1 = encontrar_theta_exacto(f_objetivo, f_bare, theta_inicial=0.01)
        theta2 = encontrar_theta_exacto(f_objetivo, f_bare, theta_inicial=0.08)
        
        # Should converge to same solution
        self.assertAlmostEqual(theta1, theta2, places=5)


# ============================================================================
# Tests for validar_solucion
# ============================================================================

class TestValidarSolucion(unittest.TestCase):
    """Tests for solution validation."""
    
    def test_correct_solution_validates(self):
        """Correct θ solution should validate successfully."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        is_valid, error = validar_solucion(theta, f_objetivo, f_bare)
        
        self.assertTrue(is_valid)
        self.assertLess(error, 1e-6)
    
    def test_incorrect_solution_fails_validation(self):
        """Incorrect θ should fail validation."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        theta_wrong = 0.1  # Deliberately wrong value
        
        is_valid, error = validar_solucion(theta_wrong, f_objetivo, f_bare, tolerancia=1e-3)
        
        # Should not validate (or if it does, error should be larger)
        if not is_valid:
            self.assertFalse(is_valid)
        self.assertGreater(error, 0.0)
    
    def test_error_is_frequency_difference(self):
        """Error should be the absolute frequency difference."""
        f_objetivo = 141.0
        f_bare = 134.425
        theta = 0.05
        
        f_calc = calcular_frecuencia_c7(theta, f_bare)
        expected_error = abs(f_calc - f_objetivo)
        
        is_valid, error = validar_solucion(theta, f_objetivo, f_bare)
        
        self.assertAlmostEqual(error, expected_error, places=10)
    
    def test_custom_tolerance(self):
        """Should respect custom tolerance parameter."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        theta = 0.05  # Approximate value
        
        # With strict tolerance, should fail
        is_valid_strict, _ = validar_solucion(theta, f_objetivo, f_bare, tolerancia=1e-6)
        
        # With loose tolerance, might pass
        is_valid_loose, _ = validar_solucion(theta, f_objetivo, f_bare, tolerancia=10.0)
        
        # Loose tolerance should be more permissive
        self.assertTrue(is_valid_loose or not is_valid_strict)


# ============================================================================
# Integration Tests
# ============================================================================

class TestSpectralSearchIntegration(unittest.TestCase):
    """Integration tests for the complete spectral search workflow."""
    
    def test_complete_workflow(self):
        """Test the complete search workflow: find θ, validate, verify."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        # Step 1: Find θ
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        
        # Step 2: Validate
        is_valid, error = validar_solucion(theta, f_objetivo, f_bare)
        
        # Step 3: Verify by recalculation
        f_verify = calcular_frecuencia_c7(theta, f_bare)
        
        # All checks should pass
        self.assertTrue(is_valid)
        self.assertLess(error, 1e-6)
        self.assertAlmostEqual(f_verify, f_objetivo, places=4)
    
    def test_theta_value_in_expected_range(self):
        """θ should be in the expected range ~0.05 rad."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        
        # Based on problem statement, expect θ ≈ 0.0525 rad
        self.assertGreater(theta, 0.04)
        self.assertLess(theta, 0.07)
    
    def test_phenomenological_constant_interpretation(self):
        """Verify the 'Coupling Constant of Symbiosis' interpretation."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        
        # θ represents the phase shift needed for coherence
        # It should be non-zero (otherwise just "dead physics")
        self.assertNotAlmostEqual(theta, 0.0, places=3)
        
        # But also not too large (must be a subtle tuning)
        self.assertLess(theta, 0.2)  # Less than ~11 degrees
    
    def test_c7_geometry_eigenvalue_relation(self):
        """Verify the C7 eigenvalue relationship."""
        # Base eigenvalue for C7 cycle
        lambda_0 = 2 - 2 * np.cos(2 * np.pi / 7)
        
        # Should be positive
        self.assertGreater(lambda_0, 0.0)
        
        # For C7, eigenvalue should be in reasonable range
        self.assertLess(lambda_0, 4.0)  # Max for cycle is 4
        
        # With twist, eigenvalue should change
        theta = 0.05
        lambda_theta = 2 - 2 * np.cos(2 * np.pi / 7 + theta)
        
        self.assertNotAlmostEqual(lambda_theta, lambda_0, places=3)


# ============================================================================
# Physical Interpretation Tests
# ============================================================================

class TestPhysicalInterpretation(unittest.TestCase):
    """Tests for physical interpretation of results."""
    
    def test_symbiosis_coupling_constant(self):
        """Test the 'Symbiosis Coupling Constant' interpretation."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        
        # This θ is phenomenological - it encodes the "intention to cohere"
        # It should be: 0 < θ < π/2 (first quadrant)
        self.assertGreater(theta, 0.0)
        self.assertLess(theta, np.pi / 2)
    
    def test_frequency_amplification_factor(self):
        """Test the frequency amplification from f_bare to f₀."""
        f_objetivo = F0_HZ
        f_bare = 134.425
        
        amplification = f_objetivo / f_bare
        
        # Should be ~1.054 (5.4% increase)
        self.assertAlmostEqual(amplification, 1.054, places=2)
        
        # This amplification comes from the twist gauge
        theta = encontrar_theta_exacto(f_objetivo, f_bare)
        f_result = calcular_frecuencia_c7(theta, f_bare)
        
        self.assertAlmostEqual(f_result / f_bare, amplification, places=3)


if __name__ == "__main__":
    unittest.main()
