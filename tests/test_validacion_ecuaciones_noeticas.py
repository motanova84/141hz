#!/usr/bin/env python3
"""
Tests Completos para Validación de Ecuaciones Noéticas
========================================================

Suite de 29+ tests que validan todas las propiedades de las ecuaciones:

1. m_eff = hf/c² → Energía relativista
2. m_noesis = α/f con α = hf₀²/c² → Detención vibracional  
3. m(f) = hf₀/c² = m_min → Masa noética constante

Cobertura de tests:
- Análisis dimensional (tests 1-3)
- Precisión numérica (tests 4-8)
- Complementariedad (tests 9-12)
- Implementación Python/NumPy (tests 13-17)
- Predicciones físicas (tests 18-22)
- Integración QCAL (tests 23-27)
- Edge cases (tests 28-29+)

Autor: José Manuel Mota Burruezo
Fecha: Febrero 2026
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.dual_mass import (
    DualMassPerspective,
    effective_mass,
    noetic_mass,
    unified_mass,
    H_PLANCK,
    C_LIGHT,
    F0_HZ
)
from qcal.constants import M_MIN_NOETIC, ALPHA_NOETIC


# ============================================================================
# TEST GROUP 1: ANÁLISIS DIMENSIONAL (Tests 1-3)
# ============================================================================

class TestAnalisisDimensional:
    """Tests de análisis dimensional."""
    
    def test_01_m_eff_dimensional_units(self):
        """Test 1: m_eff tiene unidades de kg."""
        dmp = DualMassPerspective()
        m_eff = dmp.effective_mass(F0_HZ)
        
        # Should be positive mass in kg
        assert m_eff > 0
        # Order of magnitude check for f₀ ≈ 141.7 Hz
        assert 1e-50 < m_eff < 1e-46
    
    def test_02_m_noesis_dimensional_units(self):
        """Test 2: m_noesis tiene unidades de kg."""
        dmp = DualMassPerspective()
        m_noesis = dmp.noetic_mass(F0_HZ)
        
        # Should be positive mass in kg
        assert m_noesis > 0
        # Order of magnitude check
        assert 1e-50 < m_noesis < 1e-46
    
    def test_03_m_dual_dimensional_units(self):
        """Test 3: m(f) tiene unidades de kg."""
        dmp = DualMassPerspective()
        m_dual = dmp.unified_mass(F0_HZ)
        
        # Should be positive mass in kg
        assert m_dual > 0
        # Order of magnitude check
        assert 1e-50 < m_dual < 1e-46


# ============================================================================
# TEST GROUP 2: PRECISIÓN NUMÉRICA (Tests 4-8)
# ============================================================================

class TestPrecisionNumerica:
    """Tests de precisión numérica con errores < 10⁻¹⁰."""
    
    def test_04_m_eff_numerical_precision(self):
        """Test 4: m_eff calculada con error < 10⁻¹⁰."""
        dmp = DualMassPerspective()
        
        # Calculate with formula
        m_eff = dmp.effective_mass(F0_HZ)
        
        # Calculate expected value
        expected = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        
        # Relative error
        rel_error = abs(m_eff - expected) / expected
        assert rel_error < 1e-10
    
    def test_05_m_noesis_numerical_precision(self):
        """Test 5: m_noesis calculada con error < 10⁻¹⁰."""
        dmp = DualMassPerspective()
        
        # Calculate with formula
        m_noesis = dmp.noetic_mass(F0_HZ)
        
        # Calculate expected value
        alpha = H_PLANCK * (F0_HZ ** 2) / (C_LIGHT ** 2)
        expected = alpha / F0_HZ
        
        # Relative error
        rel_error = abs(m_noesis - expected) / expected
        assert rel_error < 1e-10
    
    def test_06_m_dual_numerical_precision(self):
        """Test 6: m(f) calculada con error < 10⁻¹⁰."""
        dmp = DualMassPerspective()
        
        # Calculate with formula
        m_dual = dmp.unified_mass(F0_HZ)
        
        # Calculate expected value
        expected = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        
        # Relative error
        rel_error = abs(m_dual - expected) / expected
        assert rel_error < 1e-10
    
    def test_07_alpha_constant_precision(self):
        """Test 7: Constante α calculada con error < 10⁻¹⁰."""
        dmp = DualMassPerspective()
        
        # Calculate alpha
        alpha = dmp.alpha
        
        # Expected value
        expected = H_PLANCK * (F0_HZ ** 2) / (C_LIGHT ** 2)
        
        # Relative error
        rel_error = abs(alpha - expected) / expected
        assert rel_error < 1e-10
    
    def test_08_m_min_precision(self):
        """Test 8: Masa mínima calculada con error < 10⁻¹⁰."""
        dmp = DualMassPerspective()
        
        # Calculate m_min
        m_min = dmp.m_min
        
        # Expected value
        expected = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        
        # Relative error
        rel_error = abs(m_min - expected) / expected
        assert rel_error < 1e-10


# ============================================================================
# TEST GROUP 3: COMPLEMENTARIEDAD (Tests 9-12)
# ============================================================================

class TestComplementariedad:
    """Tests de complementariedad r_eff · r_noesis = 1."""
    
    def test_09_complementarity_at_f0(self):
        """Test 9: r_eff · r_noesis = 1 en f₀."""
        dmp = DualMassPerspective()
        r_eff, r_noesis = dmp.mass_ratio(F0_HZ)
        
        product = r_eff * r_noesis
        assert abs(product - 1.0) < 1e-10
    
    def test_10_complementarity_high_frequency(self):
        """Test 10: r_eff · r_noesis = 1 para f >> f₀."""
        dmp = DualMassPerspective()
        f_high = F0_HZ * 1000
        r_eff, r_noesis = dmp.mass_ratio(f_high)
        
        product = r_eff * r_noesis
        assert abs(product - 1.0) < 1e-10
    
    def test_11_complementarity_low_frequency(self):
        """Test 11: r_eff · r_noesis = 1 para f << f₀."""
        dmp = DualMassPerspective()
        f_low = F0_HZ / 1000
        r_eff, r_noesis = dmp.mass_ratio(f_low)
        
        product = r_eff * r_noesis
        assert abs(product - 1.0) < 1e-10
    
    def test_12_complementarity_array(self):
        """Test 12: r_eff · r_noesis = 1 para array de frecuencias."""
        dmp = DualMassPerspective()
        frequencies = np.logspace(-1, 6, 100)
        r_eff, r_noesis = dmp.mass_ratio(frequencies)
        
        products = r_eff * r_noesis
        assert np.all(np.abs(products - 1.0) < 1e-10)


# ============================================================================
# TEST GROUP 4: IMPLEMENTACIÓN PYTHON/NUMPY (Tests 13-17)
# ============================================================================

class TestImplementacionPythonNumpy:
    """Tests de implementación en Python y NumPy."""
    
    def test_13_scalar_inputs(self):
        """Test 13: Funciones aceptan entradas escalares."""
        dmp = DualMassPerspective()
        
        m_eff = dmp.effective_mass(100.0)
        m_noesis = dmp.noetic_mass(100.0)
        m_dual = dmp.unified_mass(100.0)
        
        assert isinstance(m_eff, float)
        assert isinstance(m_noesis, float)
        assert isinstance(m_dual, float)
    
    def test_14_numpy_array_inputs(self):
        """Test 14: Funciones aceptan arrays de NumPy."""
        dmp = DualMassPerspective()
        frequencies = np.array([10.0, 100.0, 1000.0])
        
        m_eff = dmp.effective_mass(frequencies)
        m_noesis = dmp.noetic_mass(frequencies)
        m_dual = dmp.unified_mass(frequencies)
        
        assert isinstance(m_eff, np.ndarray)
        assert isinstance(m_noesis, np.ndarray)
        assert isinstance(m_dual, np.ndarray)
        assert len(m_eff) == len(frequencies)
    
    def test_15_numpy_broadcasting(self):
        """Test 15: Funciones soportan broadcasting de NumPy."""
        dmp = DualMassPerspective()
        frequencies = np.linspace(1, 1000, 100)
        
        m_eff = dmp.effective_mass(frequencies)
        m_noesis = dmp.noetic_mass(frequencies)
        
        # Should work element-wise
        assert m_eff.shape == frequencies.shape
        assert m_noesis.shape == frequencies.shape
    
    def test_16_convenience_functions(self):
        """Test 16: Funciones de conveniencia funcionan correctamente."""
        m_eff = effective_mass(F0_HZ)
        m_noesis = noetic_mass(F0_HZ)
        m_dual = unified_mass()
        
        assert abs(m_eff - m_noesis) / m_eff < 1e-10
        assert abs(m_eff - m_dual) / m_eff < 1e-10
    
    def test_17_dmp_class_consistency(self):
        """Test 17: Clase DualMassPerspective es consistente."""
        dmp1 = DualMassPerspective()
        dmp2 = DualMassPerspective(f0=F0_HZ)
        
        # Should have same parameters
        assert dmp1.f0 == dmp2.f0
        assert dmp1.m_min == dmp2.m_min
        assert dmp1.alpha == dmp2.alpha


# ============================================================================
# TEST GROUP 5: PREDICCIONES FÍSICAS (Tests 18-22)
# ============================================================================

class TestPrediccionesFisicas:
    """Tests de predicciones físicas para límites extremos."""
    
    def test_18_high_frequency_m_eff_dominates(self):
        """Test 18: Para f >> f₀, m_eff >> m_min."""
        dmp = DualMassPerspective()
        f_high = F0_HZ * 1e6
        
        m_eff = dmp.effective_mass(f_high)
        assert m_eff > dmp.m_min
        assert m_eff / dmp.m_min > 1e5  # Much larger
    
    def test_19_high_frequency_m_noesis_vanishes(self):
        """Test 19: Para f >> f₀, m_noesis << m_min."""
        dmp = DualMassPerspective()
        f_high = F0_HZ * 1e6
        
        m_noesis = dmp.noetic_mass(f_high)
        assert m_noesis < dmp.m_min
        assert dmp.m_min / m_noesis > 1e5  # Much smaller
    
    def test_20_low_frequency_m_eff_vanishes(self):
        """Test 20: Para f << f₀, m_eff << m_min."""
        dmp = DualMassPerspective()
        f_low = F0_HZ / 1e6
        
        m_eff = dmp.effective_mass(f_low)
        assert m_eff < dmp.m_min
        assert dmp.m_min / m_eff > 1e5  # Much smaller
    
    def test_21_low_frequency_m_noesis_dominates(self):
        """Test 21: Para f << f₀, m_noesis >> m_min."""
        dmp = DualMassPerspective()
        f_low = F0_HZ / 1e6
        
        m_noesis = dmp.noetic_mass(f_low)
        assert m_noesis > dmp.m_min
        assert m_noesis / dmp.m_min > 1e5  # Much larger
    
    def test_22_equilibrium_at_f0(self):
        """Test 22: En f₀, m_eff = m_noesis = m_dual."""
        dmp = DualMassPerspective()
        
        m_eff = dmp.effective_mass(F0_HZ)
        m_noesis = dmp.noetic_mass(F0_HZ)
        m_dual = dmp.unified_mass(F0_HZ)
        
        assert abs(m_eff - m_noesis) / m_eff < 1e-10
        assert abs(m_eff - m_dual) / m_eff < 1e-10
        assert abs(m_noesis - m_dual) / m_noesis < 1e-10


# ============================================================================
# TEST GROUP 6: INTEGRACIÓN QCAL (Tests 23-27)
# ============================================================================

class TestIntegracionQCAL:
    """Tests de integración con constantes QCAL."""
    
    def test_23_f0_matches_qcal_constant(self):
        """Test 23: f₀ coincide con F0_HZ de qcal.constants."""
        dmp = DualMassPerspective()
        assert dmp.f0 == F0_HZ
        assert abs(dmp.f0 - 141.70001) < 1e-10
    
    def test_24_m_min_matches_qcal_constant(self):
        """Test 24: m_min coincide con M_MIN_NOETIC."""
        dmp = DualMassPerspective()
        rel_error = abs(dmp.m_min - M_MIN_NOETIC) / M_MIN_NOETIC
        assert rel_error < 1e-10
    
    def test_25_alpha_matches_qcal_constant(self):
        """Test 25: α coincide con ALPHA_NOETIC."""
        dmp = DualMassPerspective()
        rel_error = abs(dmp.alpha - ALPHA_NOETIC) / ALPHA_NOETIC
        assert rel_error < 1e-10
    
    def test_26_alpha_formula_correct(self):
        """Test 26: α = h·f₀²/c² se cumple."""
        dmp = DualMassPerspective()
        expected_alpha = H_PLANCK * (F0_HZ ** 2) / (C_LIGHT ** 2)
        rel_error = abs(dmp.alpha - expected_alpha) / expected_alpha
        assert rel_error < 1e-10
    
    def test_27_m_min_formula_correct(self):
        """Test 27: m_min = h·f₀/c² se cumple."""
        dmp = DualMassPerspective()
        expected_m_min = H_PLANCK * F0_HZ / (C_LIGHT ** 2)
        rel_error = abs(dmp.m_min - expected_m_min) / expected_m_min
        assert rel_error < 1e-10


# ============================================================================
# TEST GROUP 7: EDGE CASES Y CASOS ESPECIALES (Tests 28-29+)
# ============================================================================

class TestEdgeCases:
    """Tests de casos extremos y condiciones de frontera."""
    
    def test_28_m_dual_constant_independence(self):
        """Test 28: m_dual es independiente de f (siempre constante)."""
        dmp = DualMassPerspective()
        
        frequencies = [0.1, 1.0, 10.0, 100.0, 1000.0, 1e6]
        masses = [dmp.unified_mass(f) for f in frequencies]
        
        # All should be exactly equal
        assert all(m == dmp.m_min for m in masses)
    
    def test_29_unification_identity(self):
        """Test 29: m_dual = m_eff × (f₀/f) = m_noesis × (f/f₀)."""
        dmp = DualMassPerspective()
        
        test_frequencies = [1.0, 10.0, F0_HZ, 100.0, 1000.0]
        
        for f in test_frequencies:
            m_eff = dmp.effective_mass(f)
            m_noesis = dmp.noetic_mass(f)
            m_dual = dmp.unified_mass(f)
            
            # Test identity 1: m_dual = m_eff × (f₀/f)
            identity1 = m_eff * (dmp.f0 / f)
            assert abs(m_dual - identity1) / m_dual < 1e-10
            
            # Test identity 2: m_dual = m_noesis × (f/f₀)
            identity2 = m_noesis * (f / dmp.f0)
            assert abs(m_dual - identity2) / m_dual < 1e-10
    
    def test_30_get_constants_returns_correct_dict(self):
        """Test 30: get_constants() retorna diccionario correcto."""
        dmp = DualMassPerspective()
        const = dmp.get_constants()
        
        assert 'f0' in const
        assert 'm_min' in const
        assert 'alpha' in const
        assert 'h' in const
        assert 'c' in const
        assert 'c2' in const
        
        assert const['f0'] == dmp.f0
        assert const['m_min'] == dmp.m_min
        assert const['alpha'] == dmp.alpha
    
    def test_31_mass_ratio_symmetry(self):
        """Test 31: r_eff(f) = 1/r_noesis(f)."""
        dmp = DualMassPerspective()
        
        test_frequencies = np.logspace(0, 3, 50)
        r_eff, r_noesis = dmp.mass_ratio(test_frequencies)
        
        # r_eff should be inverse of r_noesis
        inverse_ratios = 1.0 / r_noesis
        assert np.allclose(r_eff, inverse_ratios, rtol=1e-10)
    
    def test_32_custom_f0_initialization(self):
        """Test 32: Inicialización con f₀ personalizado funciona."""
        custom_f0 = 100.0
        dmp = DualMassPerspective(f0=custom_f0)
        
        assert dmp.f0 == custom_f0
        assert dmp.m_min == H_PLANCK * custom_f0 / (C_LIGHT ** 2)
        
        # At custom f₀, masses should equilibrate
        m_eff = dmp.effective_mass(custom_f0)
        m_noesis = dmp.noetic_mass(custom_f0)
        assert abs(m_eff - m_noesis) / m_eff < 1e-10


# ============================================================================
# PARAMETRIZED TESTS FOR COMPREHENSIVE COVERAGE
# ============================================================================

class TestParametrizedValidations:
    """Tests parametrizados para cobertura comprehensiva."""
    
    @pytest.mark.parametrize("frequency", [
        1.0, 10.0, 50.0, 100.0, F0_HZ, 200.0, 500.0, 1000.0
    ])
    def test_33_all_masses_positive(self, frequency):
        """Test 33: Todas las masas son positivas para cualquier f > 0."""
        dmp = DualMassPerspective()
        
        m_eff = dmp.effective_mass(frequency)
        m_noesis = dmp.noetic_mass(frequency)
        m_dual = dmp.unified_mass(frequency)
        
        assert m_eff > 0
        assert m_noesis > 0
        assert m_dual > 0
    
    @pytest.mark.parametrize("frequency", [
        0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0
    ])
    def test_34_complementarity_holds_everywhere(self, frequency):
        """Test 34: Complementariedad se cumple para todo f."""
        dmp = DualMassPerspective()
        r_eff, r_noesis = dmp.mass_ratio(frequency)
        
        product = r_eff * r_noesis
        assert abs(product - 1.0) < 1e-10
    
    @pytest.mark.parametrize("f_ratio", [
        0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0, 1000.0
    ])
    def test_35_scaling_relationships(self, f_ratio):
        """Test 35: Relaciones de escala correctas."""
        dmp = DualMassPerspective()
        f = f_ratio * dmp.f0
        
        m_eff = dmp.effective_mass(f)
        m_noesis = dmp.noetic_mass(f)
        
        # m_eff should scale as f
        assert abs(m_eff / dmp.m_min - f_ratio) / f_ratio < 1e-10
        
        # m_noesis should scale as 1/f
        assert abs(m_noesis / dmp.m_min - 1/f_ratio) / (1/f_ratio) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
