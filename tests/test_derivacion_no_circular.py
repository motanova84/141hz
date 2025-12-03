#!/usr/bin/env python3
"""
Tests for Non-Circular Derivation of f₀ = 141.7001 Hz

This module tests the implementation of the non-circular derivation
ensuring no circularity in the reasoning (f₀ is not used as input).

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: December 2025
License: MIT
"""

import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from derivacion_no_circular_f0 import DerivacionNoCircular


class TestDerivacionNoCircular:
    """Test suite for non-circular derivation."""
    
    @pytest.fixture
    def derivacion(self):
        """Create a derivation instance."""
        return DerivacionNoCircular()
    
    def test_constants_initialized(self, derivacion):
        """Test that all fundamental constants are initialized."""
        assert float(derivacion.c) == pytest.approx(2.99792458e8, rel=1e-6)
        assert float(derivacion.l_P) == pytest.approx(1.616255e-35, rel=1e-3)
        assert float(derivacion.m_P) == pytest.approx(2.176e-8, rel=1e-2)
        assert float(derivacion.Lambda_Q) == pytest.approx(4.12e-22, rel=1e-2)
    
    def test_phi_golden_ratio(self, derivacion):
        """Test golden ratio calculation."""
        phi = float(derivacion.phi)
        assert phi == pytest.approx(1.618033988749895, rel=1e-10)
        # φ² = φ + 1
        assert phi ** 2 == pytest.approx(phi + 1, rel=1e-10)
    
    def test_G_Y_no_circular_calculation(self, derivacion):
        """Test that G_Y is calculated without using f₀."""
        G_Y = derivacion.calcular_G_Y_no_circular()
        
        # G_Y should be positive
        assert float(G_Y) > 0
        
        # G_Y = (m_P / Λ_Q)^(1/3)
        expected = (float(derivacion.m_P) / float(derivacion.Lambda_Q)) ** (1/3)
        assert float(G_Y) == pytest.approx(expected, rel=1e-6)
        
        # G_Y should be around 3.7×10⁴
        assert 1e4 < float(G_Y) < 1e5
    
    def test_G_Y_does_not_use_f0(self, derivacion):
        """Verify G_Y calculation doesn't depend on f₀."""
        # Store original f0_target
        original_f0 = derivacion.f0_target
        
        # Calculate G_Y with original f0
        G_Y_1 = derivacion.calcular_G_Y_no_circular()
        
        # Modify f0_target
        from mpmath import mp
        derivacion.f0_target = mp.mpf("1000.0")
        
        # Calculate G_Y again
        G_Y_2 = derivacion.calcular_G_Y_no_circular()
        
        # G_Y should be identical (no dependency on f0)
        assert float(G_Y_1) == float(G_Y_2)
        
        # Restore original
        derivacion.f0_target = original_f0
    
    def test_R_Psi_from_vacuum(self, derivacion):
        """Test R_Ψ derivation from vacuum energy."""
        R_data = derivacion.calcular_R_Psi_desde_vacio()
        
        # All components should be positive
        assert float(R_data["R_phys"]) > 0
        assert float(R_data["R_Psi_base"]) > 0
        assert float(R_data["R_Psi"]) > 0
        
        # Corrections should be positive
        assert float(R_data["corr_adelic"]) > 0
        assert float(R_data["corr_pi"]) > 0
        assert float(R_data["corr_phi"]) > 0
        
        # R_Ψ should be large (target is ~10^47)
        assert float(R_data["R_Psi"]) > 1e40
    
    def test_R_Psi_does_not_use_f0(self, derivacion):
        """Verify R_Ψ calculation doesn't depend on f₀."""
        from mpmath import mp
        
        # Store original f0_target
        original_f0 = derivacion.f0_target
        
        # Calculate R_Ψ with original f0
        R_data_1 = derivacion.calcular_R_Psi_desde_vacio()
        
        # Modify f0_target
        derivacion.f0_target = mp.mpf("500.0")
        
        # Calculate R_Ψ again
        R_data_2 = derivacion.calcular_R_Psi_desde_vacio()
        
        # R_Ψ should be identical (no dependency on f0)
        assert float(R_data_1["R_Psi"]) == float(R_data_2["R_Psi"])
        
        # Restore original
        derivacion.f0_target = original_f0
    
    def test_p17_spectral_minimum(self, derivacion):
        """Test that p=17 is identified as spectral minimum."""
        result = derivacion.verificar_p17_minimo_espectral()
        
        # p=17 should be the optimal prime
        assert result["primo_optimo"] == 17
        
        # All equilibrium values should be positive
        for p, val in result["equilibrios"].items():
            assert val > 0
    
    def test_G_components(self, derivacion):
        """Test calculation of G factor components."""
        G_data = derivacion.calcular_componentes_G()
        
        # All components should be positive
        assert float(G_data["A_p"]) > 0
        assert float(G_data["F_zeta"]) > 0
        assert float(G_data["Factor_K"]) > 0
        assert float(G_data["F_fractal"]) > 0
        assert float(G_data["G_Y"]) > 0
        assert float(G_data["G_partial"]) > 0
        assert float(G_data["G_final"]) > 0
    
    def test_f0_calculation(self, derivacion):
        """Test f₀ calculation produces a positive result."""
        f0_data = derivacion.calcular_f0()
        
        # f₀ should be positive
        assert float(f0_data["f0_calculado"]) > 0
        
        # Error percentage should be defined
        assert f0_data["error_relativo_percent"] >= 0
    
    def test_non_circularity_verification(self, derivacion):
        """Test the non-circularity verification method."""
        verificacion = derivacion.verificar_no_circularidad()
        
        # All circularity checks should be False (no circularity)
        assert verificacion["G_Y_usa_f0"] == False
        assert verificacion["R_Psi_usa_f0"] == False
        assert verificacion["algún_paso_usa_f0"] == False
        
        # Genuine emergence should be True
        assert verificacion["emergencia_genuina"] == True
    
    def test_complete_derivation_runs(self, derivacion):
        """Test that the complete derivation executes without errors."""
        # This should not raise any exceptions
        resultado = derivacion.ejecutar_derivacion_completa()
        
        # Result should contain all expected sections
        assert "constantes" in resultado
        assert "G_Y" in resultado
        assert "componentes_G" in resultado
        assert "R_Psi_data" in resultado
        assert "p17_minimo" in resultado
        assert "f0_resultado" in resultado
        assert "verificacion_no_circular" in resultado


class TestPhysicalConsistency:
    """Test physical consistency of the derivation."""
    
    @pytest.fixture
    def derivacion(self):
        """Create a derivation instance."""
        return DerivacionNoCircular()
    
    def test_planck_mass_scale(self, derivacion):
        """Test that Planck mass is in expected range."""
        m_P = float(derivacion.m_P)
        # Planck mass should be around 2.2×10⁻⁸ kg
        assert 1e-9 < m_P < 1e-7
    
    def test_vacuum_scale_reasonable(self, derivacion):
        """Test that vacuum scale Λ_Q is physically reasonable."""
        Lambda_Q = float(derivacion.Lambda_Q)
        # Λ_Q should be around 10⁻²² kg (meV scale)
        assert 1e-23 < Lambda_Q < 1e-21
    
    def test_R_Psi_cosmological_scale(self, derivacion):
        """Test that R_Ψ is at cosmological scale."""
        R_data = derivacion.calcular_R_Psi_desde_vacio()
        R_Psi = float(R_data["R_Psi"])
        
        # R_Ψ should be extremely large (cosmological hierarchy)
        # Problem statement says ~10^47
        assert R_Psi > 1e40
    
    def test_phi_powers_positive(self, derivacion):
        """Test that powers of φ are positive and reasonable."""
        phi = float(derivacion.phi)
        
        # φ³ should be around 4.236
        assert phi ** 3 == pytest.approx(4.236067977, rel=1e-6)
        
        # φ⁶ should be around 17.94
        assert phi ** 6 == pytest.approx(17.94427191, rel=1e-6)


class TestMathematicalProperties:
    """Test mathematical properties of the derivation."""
    
    @pytest.fixture
    def derivacion(self):
        """Create a derivation instance."""
        return DerivacionNoCircular()
    
    def test_zeta_prime_value(self, derivacion):
        """Test ζ'(1/2) value is correct."""
        zeta_prime = float(derivacion.zeta_prime)
        # ζ'(1/2) ≈ -3.9226
        assert zeta_prime == pytest.approx(-3.9226461392, rel=1e-6)
        assert zeta_prime < 0  # Must be negative
    
    def test_adelic_correction_p17(self, derivacion):
        """Test that 17^(7/2) is calculated correctly."""
        R_data = derivacion.calcular_R_Psi_desde_vacio()
        corr_adelic = float(R_data["corr_adelic"])
        
        expected = 17 ** 3.5
        assert corr_adelic == pytest.approx(expected, rel=1e-6)
    
    def test_pi_cubed(self, derivacion):
        """Test that π³ correction is calculated correctly."""
        from mpmath import pi as mp_pi
        
        R_data = derivacion.calcular_R_Psi_desde_vacio()
        corr_pi = float(R_data["corr_pi"])
        
        expected = float(mp_pi ** 3)
        assert corr_pi == pytest.approx(expected, rel=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
