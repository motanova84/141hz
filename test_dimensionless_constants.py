#!/usr/bin/env python3
"""
Tests for Dimensionless Constants Core Module
==============================================

Tests that validate the principle: "Lo único que importa son las constantes adimensionales"

Author: José Manuel Mota Burruezo
License: MIT
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dimensionless_constants_core import (
    ALPHA, ALPHA_INV, PHI, PHI_INV,
    ALPHA_S, ALPHA_W, ALPHA_G,
    MASS_RATIO_PROTON_ELECTRON,
    FACTOR_1_7,
    KAPPA_PI, DELTA_0,
    es_adimensional,
    calcular_alpha_efectivo,
    calcular_jerarquia_masas,
    calcular_acoplamientos_unificados,
    calcular_numeros_fundamentales,
    calcular_137_como_centro,
    validar_principio_adimensional,
)


class TestConstantesBasicas:
    """Tests para constantes básicas adimensionales."""
    
    def test_alpha_valor(self):
        """Test que α ≈ 1/137."""
        assert 0.007 < ALPHA < 0.008
        assert 137.0 < ALPHA_INV < 137.1
        
        # Verificar relación α × (1/α) = 1
        assert abs(ALPHA * ALPHA_INV - 1.0) < 1e-10
    
    def test_phi_valor(self):
        """Test que φ = (1+√5)/2."""
        import math
        phi_calculado = (1 + math.sqrt(5)) / 2
        assert abs(PHI - phi_calculado) < 1e-14
        
        # Verificar relación φ × (1/φ) = 1
        assert abs(PHI * PHI_INV - 1.0) < 1e-14
    
    def test_alpha_s_fuerte(self):
        """Test constante fuerte α_s ≈ 1."""
        assert ALPHA_S == 1.0
    
    def test_alpha_w_debil(self):
        """Test constante débil α_w ≈ 1/30."""
        assert abs(ALPHA_W - 1.0/30.0) < 1e-10
    
    def test_alpha_g_gravedad(self):
        """Test constante gravitacional α_G ≈ 10⁻³⁸."""
        assert 1e-39 < ALPHA_G < 1e-37


class TestJerarquiasMasa:
    """Tests para jerarquías de masa adimensionales."""
    
    def test_ratio_proton_electron(self):
        """Test m_p/m_e ≈ 1836."""
        assert 1836.0 < MASS_RATIO_PROTON_ELECTRON < 1837.0
    
    def test_todas_jerarquias(self):
        """Test todas las jerarquías de masa."""
        jerarquias = calcular_jerarquia_masas()
        
        # Verificar que todas son > 1 (más pesado que electrón)
        assert all(ratio > 1.0 for ratio in jerarquias.values())
        
        # Verificar valores conocidos
        assert 1836.0 < jerarquias['proton_electron'] < 1837.0
        assert 206.0 < jerarquias['muon_electron'] < 207.0
        assert 3477.0 < jerarquias['tau_electron'] < 3478.0
    
    def test_jerarquia_tau_muon(self):
        """Test que m_τ/m_μ = (m_τ/m_e) / (m_μ/m_e)."""
        jerarquias = calcular_jerarquia_masas()
        
        tau_muon_calculado = jerarquias['tau_electron'] / jerarquias['muon_electron']
        tau_muon_directo = jerarquias['tau_muon']
        
        assert abs(tau_muon_calculado - tau_muon_directo) < 0.01


class TestAcoplamientos:
    """Tests para constantes de acoplamiento."""
    
    def test_acoplamientos_fuerzas(self):
        """Test constantes de acoplamiento de las 4 fuerzas."""
        acoplamientos = calcular_acoplamientos_unificados()
        
        # Verificar que están en orden correcto: fuerte > débil > EM > gravedad
        # (α_W ≈ 1/30 > α_EM ≈ 1/137)
        assert acoplamientos['fuerte'] > acoplamientos['debil']
        assert acoplamientos['debil'] > acoplamientos['electromagnetica']
        assert acoplamientos['electromagnetica'] > acoplamientos['gravitacional']
    
    def test_ratio_fuerte_em(self):
        """Test α_s/α_EM ≈ 137."""
        acoplamientos = calcular_acoplamientos_unificados()
        ratio = acoplamientos['ratio_fuerte_EM']
        
        # α_s / α_EM ≈ 1 / (1/137) = 137
        assert 135.0 < ratio < 140.0
    
    def test_ratio_em_debil(self):
        """Test α_EM/α_W."""
        acoplamientos = calcular_acoplamientos_unificados()
        ratio = acoplamientos['ratio_EM_debil']
        
        # α_EM / α_W ≈ (1/137) / (1/30) ≈ 30/137 ≈ 0.219
        assert 0.2 < ratio < 0.25


class TestAlphaEfectivo:
    """Tests para α efectivo a diferentes escalas."""
    
    def test_alpha_baja_energia(self):
        """Test α a baja energía ≈ α(0)."""
        alpha_low = calcular_alpha_efectivo(0.001)  # 1 MeV
        # α runs, so allow for small difference
        assert abs(alpha_low - ALPHA) < 1e-4
    
    def test_alpha_escala_z(self):
        """Test α aumenta a escala electrodébil."""
        alpha_z = calcular_alpha_efectivo(91.2)  # Masa del Z
        
        # α debería aumentar ≈ 7% en escala electrodébil
        assert alpha_z > ALPHA
        assert alpha_z < ALPHA * 1.1
    
    def test_alpha_monotono(self):
        """Test α aumenta monótonamente con la energía."""
        energias = [0.001, 0.1, 1.0, 10.0, 91.2]
        alphas = [calcular_alpha_efectivo(E) for E in energias]
        
        # Verificar que aumenta
        for i in range(len(alphas) - 1):
            assert alphas[i+1] > alphas[i]


class TestNumerosFundamentales:
    """Tests para números fundamentales."""
    
    def test_numeros_matematicos(self):
        """Test números fundamentales π, e, φ."""
        import math
        
        nums = calcular_numeros_fundamentales()
        
        assert abs(nums['pi'] - math.pi) < 1e-14
        assert abs(nums['e'] - math.e) < 1e-14
        assert abs(nums['phi'] - PHI) < 1e-14
    
    def test_raices_cuadradas(self):
        """Test √2, √3, √5."""
        import math
        
        nums = calcular_numeros_fundamentales()
        
        assert abs(nums['sqrt_2'] - math.sqrt(2)) < 1e-14
        assert abs(nums['sqrt_3'] - math.sqrt(3)) < 1e-14
        assert abs(nums['sqrt_5'] - math.sqrt(5)) < 1e-14
    
    def test_euler_mascheroni(self):
        """Test constante de Euler γ ≈ 0.5772."""
        nums = calcular_numeros_fundamentales()
        gamma = nums['euler_mascheroni']
        
        assert 0.577 < gamma < 0.578


class TestCentro137:
    """Tests para 137 como centro de la red."""
    
    def test_alpha_inverso_137(self):
        """Test 1/α ≈ 137."""
        centro = calcular_137_como_centro()
        assert 137.0 < centro['alpha_inverso'] < 137.1
    
    def test_relaciones_con_137(self):
        """Test relaciones con el número 137."""
        centro = calcular_137_como_centro()
        
        # Verificar que los ratios tienen valores razonables
        assert centro['ratio_proton_137'] > 10.0
        assert centro['ratio_R_psi_137'] > 2.0
        assert centro['alpha_z_sobre_alpha'] > 1.0


class TestValidacionPrincipio:
    """Tests para validación del principio adimensional."""
    
    def test_validar_principio(self):
        """Test validación del principio fundamental."""
        validacion = validar_principio_adimensional(precision=50)
        
        # Verificar que el principio es válido
        assert validacion['principio_valido']
        assert validacion['alpha_adimensional']
        assert validacion['jerarquias_masa']
        assert validacion['f0_de_adimensionales']
    
    def test_mensaje_validacion(self):
        """Test mensaje de validación."""
        validacion = validar_principio_adimensional()
        
        assert 'PRINCIPIO VALIDADO' in validacion['mensaje']
        assert 'adimensionales' in validacion['mensaje'].lower()
    
    def test_f0_emerge_adimensionales(self):
        """Test que f₀ emerge de constantes adimensionales."""
        validacion = validar_principio_adimensional()
        
        # Verificar que hay una combinación adimensional
        assert 'combinacion_adimensional' in validacion
        assert validacion['combinacion_adimensional'] > 0
        
        # Verificar que el factor dimensional es razonable
        assert 'factor_dimensional' in validacion
        # El factor puede variar dependiendo de la formulación exacta
        assert 1 < validacion['factor_dimensional'] < 1000


class TestConstantesQCAL:
    """Tests para constantes QCAL adimensionales."""
    
    def test_factor_1_7(self):
        """Test factor 1/7."""
        assert abs(FACTOR_1_7 - 1.0/7.0) < 1e-15
        
        # Verificar período decimal
        # 1/7 = 0.142857142857... (período de 6 dígitos)
        decimal = FACTOR_1_7 * 10000000  # Multiplicar para ver dígitos
        periodo = int(decimal) % 1000000
        assert periodo == 142857 or periodo == 428571  # Período circular
    
    def test_kappa_pi(self):
        """Test κ_π adimensional."""
        assert KAPPA_PI > 2.5
        assert KAPPA_PI < 2.6
    
    def test_delta_0(self):
        """Test δ₀ umbral de coherencia."""
        assert DELTA_0 > 0.11
        assert DELTA_0 < 0.12
    
    def test_q_psi_factor_calidad(self):
        """Test Q_Ψ = 1/δ₀."""
        from dimensionless_constants_core import Q_PSI, DELTA_0
        assert abs(Q_PSI * DELTA_0 - 1.0) < 1e-10


class TestAdimensionalidad:
    """Tests para verificar adimensionalidad."""
    
    def test_es_adimensional(self):
        """Test función es_adimensional."""
        # Constantes adimensionales
        assert es_adimensional(ALPHA)
        assert es_adimensional(PHI)
        assert es_adimensional(MASS_RATIO_PROTON_ELECTRON)
        
        # Números finitos
        assert es_adimensional(1.0)
        assert es_adimensional(137.0)
        assert es_adimensional(0.0)
    
    def test_infinitos_no_adimensionales(self):
        """Test que infinitos no son adimensionales."""
        import math
        assert not es_adimensional(math.inf)
        assert not es_adimensional(-math.inf)
        assert not es_adimensional(math.nan)


class TestIntegracion:
    """Tests de integración."""
    
    def test_todas_constantes_disponibles(self):
        """Test que todas las constantes están disponibles."""
        # Verificar que no hay errores al importar
        from dimensionless_constants_core import (
            ALPHA, PHI, ALPHA_S, ALPHA_W, ALPHA_G,
            MASS_RATIO_PROTON_ELECTRON,
            FACTOR_1_7, KAPPA_PI, DELTA_0,
        )
        
        # Verificar que son números
        assert isinstance(ALPHA, float)
        assert isinstance(PHI, float)
        assert isinstance(MASS_RATIO_PROTON_ELECTRON, float)
    
    def test_funciones_disponibles(self):
        """Test que todas las funciones están disponibles."""
        # Verificar que se pueden llamar sin errores
        jerarquias = calcular_jerarquia_masas()
        acoplamientos = calcular_acoplamientos_unificados()
        numeros = calcular_numeros_fundamentales()
        centro = calcular_137_como_centro()
        
        # Verificar que retornan diccionarios
        assert isinstance(jerarquias, dict)
        assert isinstance(acoplamientos, dict)
        assert isinstance(numeros, dict)
        assert isinstance(centro, dict)


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v"])
