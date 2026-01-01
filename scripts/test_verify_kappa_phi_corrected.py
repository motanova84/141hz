#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_verify_kappa_phi_corrected.py

Tests unitarios para verify_kappa_phi_corrected.py

Autor: JMMB Ψ✧ ∞³
"""

import math
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from verify_kappa_phi_corrected import KappaPhiVerifier


class TestKappaPhiVerifier(unittest.TestCase):
    """Tests para KappaPhiVerifier."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.verifier = KappaPhiVerifier()
    
    def test_golden_ratio_property(self):
        """Test: φ² = φ + 1."""
        phi = self.verifier.phi
        phi_sq = phi ** 2
        phi_plus_one = phi + 1
        
        self.assertAlmostEqual(phi_sq, phi_plus_one, places=10,
                              msg="φ² debe ser igual a φ + 1")
    
    def test_kappa_pi_normalization(self):
        """Test: κ_Π(φ²) = 1."""
        kappa = self.verifier.kappa_pi(self.verifier.phi_sq)
        self.assertAlmostEqual(kappa, 1.0, places=10,
                              msg="κ_Π(φ²) debe ser exactamente 1")
    
    def test_spectral_correction(self):
        """Test: ΔN = ln(φ²)/(2π)."""
        delta_N = self.verifier.spectral_correction()
        expected = math.log(self.verifier.phi_sq) / (2 * math.pi)
        
        self.assertAlmostEqual(delta_N, expected, places=12,
                              msg="Corrección espectral incorrecta")
    
    def test_N_effective(self):
        """Test: N_eff = φ²^(2.5773) ≈ 11.947."""
        N_eff = self.verifier.N_effective()
        expected = self.verifier.phi_sq ** 2.5773
        
        self.assertAlmostEqual(N_eff, expected, places=10,
                              msg="N_eff debe ser φ²^(2.5773)")
    
    def test_millennium_constant(self):
        """Test: κ_Π(N_eff) = 2.5773 exactamente."""
        N_eff = self.verifier.N_effective()
        kappa = self.verifier.kappa_pi(N_eff)
        
        self.assertAlmostEqual(kappa, 2.5773, places=10,
                              msg="κ_Π(N_eff) debe ser exactamente 2.5773")
    
    def test_kappa_pi_at_12(self):
        """Test: κ_Π(12) ≈ 2.5819."""
        kappa = self.verifier.kappa_pi(12.0)
        self.assertAlmostEqual(kappa, 2.5819, delta=0.01,
                              msg="κ_Π(12) debe ser aproximadamente 2.5819")
    
    def test_kappa_pi_at_13(self):
        """Test: κ_Π(13) ≈ 2.6651."""
        kappa = self.verifier.kappa_pi(13.0)
        self.assertAlmostEqual(kappa, 2.6651, delta=0.01,
                              msg="κ_Π(13) debe ser aproximadamente 2.6651")
    
    def test_kappa_pi_monotonic(self):
        """Test: κ_Π es estrictamente creciente."""
        test_points = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
        
        for i in range(len(test_points) - 1):
            x = test_points[i]
            y = test_points[i + 1]
            kappa_x = self.verifier.kappa_pi(x)
            kappa_y = self.verifier.kappa_pi(y)
            
            self.assertLess(kappa_x, kappa_y,
                          msg=f"κ_Π debe ser creciente: κ_Π({x}) < κ_Π({y})")
    
    def test_kappa_pi_positive_input(self):
        """Test: κ_Π requiere N > 0."""
        with self.assertRaises(ValueError):
            self.verifier.kappa_pi(0)
        
        with self.assertRaises(ValueError):
            self.verifier.kappa_pi(-1)
    
    def test_calabi_yau_varieties(self):
        """Test: Variedades CY con N ≈ 13 tienen κ_Π ≈ 2.5773."""
        varieties = [
            (6, 7),   # N = 13
            (7, 6),   # N = 13
            (5, 8),   # N = 13
            (8, 5),   # N = 13
            (3, 10),  # N = 13
        ]
        
        for h11, h21 in varieties:
            N = h11 + h21
            kappa = self.verifier.kappa_pi(N)
            error = abs(kappa - 2.5773)
            
            self.assertLess(error, 0.1,
                          msg=f"κ_Π({N}) debe estar cerca de 2.5773 para variedad ({h11},{h21})")
    
    def test_phi_value(self):
        """Test: φ = (1 + √5)/2 ≈ 1.618033988749895."""
        expected = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(self.verifier.phi, expected, places=12,
                              msg="Valor de φ incorrecto")
    
    def test_phi_sq_value(self):
        """Test: φ² ≈ 2.618033988749895."""
        expected = self.verifier.phi ** 2
        self.assertAlmostEqual(self.verifier.phi_sq, expected, places=12,
                              msg="Valor de φ² incorrecto")
    
    def test_fundamental_properties(self):
        """Test de integración: propiedades fundamentales."""
        result = self.verifier.verify_fundamental_properties()
        self.assertTrue(result, msg="Propiedades fundamentales fallaron")
    
    def test_effective_value(self):
        """Test de integración: valor efectivo."""
        result = self.verifier.verify_effective_value()
        self.assertTrue(result, msg="Verificación de N_eff falló")
    
    def test_millennium_constant_verification(self):
        """Test de integración: constante milenaria."""
        result = self.verifier.verify_millennium_constant()
        self.assertTrue(result, msg="Verificación de constante milenaria falló")
    
    def test_comparison_values(self):
        """Test de integración: valores de comparación."""
        result = self.verifier.verify_comparison_values()
        self.assertTrue(result, msg="Verificación de valores de comparación falló")
    
    def test_monotonicity_verification(self):
        """Test de integración: monotonía."""
        result = self.verifier.verify_monotonicity()
        self.assertTrue(result, msg="Verificación de monotonía falló")


class TestKappaPhiMathematicalProperties(unittest.TestCase):
    """Tests de propiedades matemáticas avanzadas."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.verifier = KappaPhiVerifier()
    
    def test_logarithm_change_of_base(self):
        """Test: κ_Π(N) = log_φ²(N) = ln(N)/ln(φ²)."""
        N = 13.148698354
        
        # Método directo
        kappa_direct = self.verifier.kappa_pi(N)
        
        # Método explícito
        kappa_explicit = math.log(N) / math.log(self.verifier.phi_sq)
        
        self.assertAlmostEqual(kappa_direct, kappa_explicit, places=12,
                              msg="Cambio de base logarítmico incorrecto")
    
    def test_spectral_correction_formula(self):
        """Test: ΔN = ln(φ²)/(2π) es exacto."""
        delta_N_computed = self.verifier.spectral_correction()
        delta_N_explicit = math.log(self.verifier.phi_sq) / (2 * math.pi)
        
        self.assertAlmostEqual(delta_N_computed, delta_N_explicit, places=12,
                              msg="Fórmula de corrección espectral incorrecta")
    
    def test_N_effective_composition(self):
        """Test: N_eff = φ²^(2.5773)."""
        N_eff = self.verifier.N_effective()
        N_eff_composed = self.verifier.phi_sq ** 2.5773
        
        self.assertAlmostEqual(N_eff, N_eff_composed, places=12,
                              msg="N_eff debe ser φ²^(2.5773)")


def run_tests(verbose=True):
    """Ejecuta todos los tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestKappaPhiVerifier))
    suite.addTests(loader.loadTestsFromTestCase(TestKappaPhiMathematicalProperties))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests(verbose=True)
    sys.exit(0 if success else 1)
