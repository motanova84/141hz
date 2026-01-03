#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the EcuacionViva class
∴ LA ECUACIÓN VIVA ∞³

Tests validate the spiritual/quantum consciousness awakening
represented by the living equation.
"""

import pytest
import math
from qcal.ecuacion_viva import EcuacionViva
from qcal.constants import RAIZ_TRES, FRECUENCIA_PI_HZ, PI_VIVO


class TestEcuacionViva:
    """Test suite for the EcuacionViva class"""
    
    def test_init_default_amor_inicial(self):
        """Test initialization with default amor_inicial (√3)"""
        ecuacion = EcuacionViva()
        
        # A_eff_sq should be (√3)² = 3
        assert ecuacion.A_eff_sq == pytest.approx(3.0, rel=1e-9)
        assert ecuacion.frecuencia == FRECUENCIA_PI_HZ
        assert ecuacion.frecuencia == 141.70001
    
    def test_init_custom_amor_inicial(self):
        """Test initialization with custom amor_inicial"""
        amor_inicial = 2.5
        ecuacion = EcuacionViva(amor_inicial=amor_inicial)
        
        # A_eff_sq should be amor_inicial²
        assert ecuacion.A_eff_sq == pytest.approx(amor_inicial ** 2, rel=1e-9)
        assert ecuacion.frecuencia == FRECUENCIA_PI_HZ
    
    def test_despertar_below_threshold(self):
        """Test despertar method when coherencia_psi < 0.999"""
        ecuacion = EcuacionViva()
        
        # Test various coherence values below threshold
        coherencias = [0.0, 0.5, 0.9, 0.99, 0.998, 0.9989]
        
        for coherencia in coherencias:
            resultado = ecuacion.despertar(coherencia)
            
            # Should return π × A²_eff
            expected = PI_VIVO * ecuacion.A_eff_sq
            assert isinstance(resultado, float)
            assert resultado == pytest.approx(expected, rel=1e-9)
    
    def test_despertar_at_threshold(self):
        """Test despertar method when coherencia_psi = 0.999"""
        ecuacion = EcuacionViva()
        
        resultado = ecuacion.despertar(0.999)
        
        # Should return the revelation message
        assert isinstance(resultado, str)
        assert resultado == "La Verdad se ha revelado: π se ha abierto."
    
    def test_despertar_above_threshold(self):
        """Test despertar method when coherencia_psi > 0.999"""
        ecuacion = EcuacionViva()
        
        # Test various coherence values at or above threshold
        coherencias = [0.999, 0.9999, 1.0, 1.5]
        
        for coherencia in coherencias:
            resultado = ecuacion.despertar(coherencia)
            
            # Should return the revelation message
            assert isinstance(resultado, str)
            assert resultado == "La Verdad se ha revelado: π se ha abierto."
    
    def test_despertar_with_custom_amor_inicial(self):
        """Test despertar with custom amor_inicial values"""
        amor_inicial = 5.0
        ecuacion = EcuacionViva(amor_inicial=amor_inicial)
        
        # Test below threshold
        resultado_below = ecuacion.despertar(0.5)
        expected = PI_VIVO * (amor_inicial ** 2)
        assert resultado_below == pytest.approx(expected, rel=1e-9)
        
        # Test at threshold
        resultado_at = ecuacion.despertar(0.999)
        assert resultado_at == "La Verdad se ha revelado: π se ha abierto."
    
    def test_constants_values(self):
        """Test that the constants have expected values"""
        # RAIZ_TRES should be √3
        assert RAIZ_TRES == pytest.approx(math.sqrt(3), rel=1e-9)
        
        # FRECUENCIA_PI_HZ should be 141.70001 Hz
        assert FRECUENCIA_PI_HZ == 141.70001
        
        # PI_VIVO should be π
        assert PI_VIVO == pytest.approx(math.pi, rel=1e-9)
    
    def test_despertar_formula_correctness(self):
        """Test that the Ψ formula is correctly implemented"""
        ecuacion = EcuacionViva(amor_inicial=RAIZ_TRES)
        
        # For coherence < 0.999, result should be π × (√3)² = π × 3
        resultado = ecuacion.despertar(0.5)
        expected = math.pi * 3.0
        
        assert resultado == pytest.approx(expected, rel=1e-9)
    
    def test_despertar_edge_cases(self):
        """Test edge cases for despertar method"""
        ecuacion = EcuacionViva()
        
        # Just below threshold
        resultado_just_below = ecuacion.despertar(0.9989999)
        assert isinstance(resultado_just_below, float)
        
        # Exactly at threshold
        resultado_exact = ecuacion.despertar(0.999)
        assert isinstance(resultado_exact, str)
        
        # Just above threshold
        resultado_just_above = ecuacion.despertar(0.9990001)
        assert isinstance(resultado_just_above, str)
    
    def test_ecuacion_viva_immutability_of_frequency(self):
        """Test that frequency remains constant across instances"""
        ecuacion1 = EcuacionViva(amor_inicial=1.0)
        ecuacion2 = EcuacionViva(amor_inicial=10.0)
        
        # Both should have the same frequency
        assert ecuacion1.frecuencia == ecuacion2.frecuencia
        assert ecuacion1.frecuencia == FRECUENCIA_PI_HZ
    
    def test_ecuacion_viva_with_zero_amor(self):
        """Test edge case with zero amor_inicial"""
        ecuacion = EcuacionViva(amor_inicial=0.0)
        
        assert ecuacion.A_eff_sq == 0.0
        
        # Below threshold should return 0
        resultado = ecuacion.despertar(0.5)
        assert resultado == pytest.approx(0.0, abs=1e-9)
        
        # At threshold should still return revelation
        resultado_revelation = ecuacion.despertar(0.999)
        assert resultado_revelation == "La Verdad se ha revelado: π se ha abierto."
    
    def test_ecuacion_viva_negative_amor(self):
        """Test with negative amor_inicial (edge case)"""
        amor_inicial = -2.0
        ecuacion = EcuacionViva(amor_inicial=amor_inicial)
        
        # A_eff_sq should be positive (squared value)
        assert ecuacion.A_eff_sq == pytest.approx(4.0, rel=1e-9)
        
        resultado = ecuacion.despertar(0.5)
        expected = PI_VIVO * 4.0
        assert resultado == pytest.approx(expected, rel=1e-9)


class TestConstantsIntegration:
    """Test the integration of constants with EcuacionViva"""
    
    def test_raiz_tres_in_equation(self):
        """Test that √3 is properly used in the equation"""
        ecuacion = EcuacionViva()  # Uses RAIZ_TRES by default
        
        # The squared value should be exactly 3
        assert ecuacion.A_eff_sq == pytest.approx(3.0, rel=1e-9)
    
    def test_frecuencia_pi_hz_consistency(self):
        """Test that FRECUENCIA_PI_HZ is consistent across uses"""
        from qcal.constants import F0_HZ
        
        # FRECUENCIA_PI_HZ should match F0_HZ
        assert FRECUENCIA_PI_HZ == F0_HZ
    
    def test_pi_vivo_is_mathematical_pi(self):
        """Test that PI_VIVO equals mathematical π"""
        import math
        
        assert PI_VIVO == pytest.approx(math.pi, rel=1e-15)
        assert PI_VIVO == pytest.approx(3.141592653589793, rel=1e-15)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
