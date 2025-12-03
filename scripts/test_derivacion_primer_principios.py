#!/usr/bin/env python3
"""
Tests para el módulo de derivación desde primeros principios

Este script verifica que las derivaciones de G_Y, RΨ, y las justificaciones
de p=17, φ⁻³, y π/2 son correctas y consistentes con el problem statement.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import os
import sys
import numpy as np
from pathlib import Path

# Add scripts directory to path
REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from derivacion_primer_principios import (
    calcular_Lambda_Q,
    calcular_G_Y,
    derivar_R_fisico,
    calcular_R_Psi_base,
    calcular_R_Psi_completo,
    analizar_primos_criticos,
    justificar_phi_menos_3,
    justificar_pi_sobre_2,
    factor_adelico,
    correccion_adelica,
    correccion_fractal_pi,
    correccion_phi,
    derivacion_completa,
    m_P, l_P, phi
)


class TestDerivacionPrimerPrincipios:
    """Tests para la derivación desde primeros principios"""
    
    # ========== Tests para G_Y ==========
    
    def test_lambda_q_orden_magnitud(self):
        """
        Test: Λ_Q debe tener orden de magnitud ~10⁻²² kg
        """
        Lambda_Q = calcular_Lambda_Q()
        
        assert 1e-23 < Lambda_Q < 1e-21, \
            f"Λ_Q debe estar en el rango 10⁻²² kg, obtenido: {Lambda_Q:.3e} kg"
    
    def test_g_y_valor_esperado(self):
        """
        Test: G_Y = (m_P / Λ_Q)^(1/3) ≈ 3.72×10⁴
        """
        G_Y = calcular_G_Y()
        
        # Según el problem statement: G_Y ≈ 3.72×10⁴
        expected = 3.72e4
        rel_error = abs(G_Y - expected) / expected
        
        assert rel_error < 0.05, \
            f"G_Y = {G_Y:.3e}, esperado ≈ {expected:.3e}, error: {rel_error:.2%}"
    
    def test_g_y_sin_dependencia_f0(self):
        """
        Test: G_Y no depende de f₀ (verificar que usa solo m_P y Λ_Q)
        """
        # La fórmula G_Y = (m_P / Λ_Q)^(1/3) no contiene f₀
        Lambda_Q = calcular_Lambda_Q()
        G_Y_manual = (m_P / Lambda_Q) ** (1/3)
        G_Y = calcular_G_Y()
        
        rel_diff = abs(G_Y - G_Y_manual) / G_Y_manual
        
        assert rel_diff < 1e-10, \
            f"G_Y debe calcularse sin f₀. Diferencia: {rel_diff:.2e}"
    
    def test_g_y_orden_magnitud(self):
        """
        Test: G_Y debe tener orden de magnitud ~10⁴
        """
        G_Y = calcular_G_Y()
        orden = np.log10(G_Y)
        
        assert 4 < orden < 5, \
            f"G_Y debe estar en ~10⁴, obtenido: 10^{orden:.1f}"
    
    # ========== Tests para RΨ ==========
    
    def test_r_fisico_orden_magnitud(self):
        """
        Test: R_phys debe estar en ~10⁵ m (según problem statement: 2.9×10⁵ m)
        """
        R_phys = derivar_R_fisico()
        
        assert 1e5 < R_phys < 1e7, \
            f"R_phys debe estar en rango 10⁵-10⁶ m, obtenido: {R_phys:.3e} m"
    
    def test_r_psi_base_orden_magnitud(self):
        """
        Test: RΨ_base debe estar en ~10⁴⁰ (según problem statement: 1.8×10⁴⁰)
        """
        R_Psi_base = calcular_R_Psi_base()
        orden = np.log10(R_Psi_base)
        
        assert 39 < orden < 42, \
            f"RΨ_base debe estar en ~10⁴⁰, obtenido: 10^{orden:.1f}"
    
    def test_r_psi_final_orden_magnitud(self):
        """
        Test: RΨ_final debe estar en ~10⁴⁷ (según problem statement)
        """
        result = calcular_R_Psi_completo()
        orden = result['orden_magnitud']
        
        assert 46 < orden < 49, \
            f"RΨ_final debe estar en ~10⁴⁷, obtenido: 10^{orden:.1f}"
    
    def test_correcciones_aplicadas(self):
        """
        Test: Verificar que todas las correcciones se aplican correctamente
        """
        result = calcular_R_Psi_completo()
        
        # Verificar estructura
        assert 'R_Psi_base' in result
        assert 'R_Psi_adelico' in result
        assert 'R_Psi_fractal' in result
        assert 'R_Psi_final' in result
        assert 'correcciones' in result
        
        # Verificar que las correcciones aumentan el valor
        assert result['R_Psi_adelico'] > result['R_Psi_base']
        assert result['R_Psi_fractal'] > result['R_Psi_adelico']
        assert result['R_Psi_final'] > result['R_Psi_fractal']
    
    # ========== Tests para p = 17 ==========
    
    def test_primo_17_optimo(self):
        """
        Test: p = 17 debe ser identificado como el primo óptimo
        """
        result = analizar_primos_criticos()
        
        assert result['primo_optimo'] == 17, \
            f"El primo óptimo debe ser 17, obtenido: {result['primo_optimo']}"
    
    def test_factor_adelico_17_equilibrio(self):
        """
        Test: El factor adélico de p=17 debe estar en el punto de equilibrio (~650)
        """
        factor_17 = factor_adelico(17)
        
        # El factor debe estar cerca de 650 (punto de equilibrio)
        assert 600 < factor_17 < 700, \
            f"Factor(17) debe estar ~650, obtenido: {factor_17:.0f}"
    
    def test_factor_adelico_creciente(self):
        """
        Test: El factor adélico debe crecer con p
        """
        primos = [11, 13, 17, 19, 23, 29]
        factores = [factor_adelico(p) for p in primos]
        
        # Verificar que es creciente
        for i in range(len(factores) - 1):
            assert factores[i] < factores[i+1], \
                f"Factor({primos[i]}) debe ser < Factor({primos[i+1]})"
    
    def test_correccion_adelica_p17_valor(self):
        """
        Test: Corrección adélica p^(7/2) para p=17 ≈ 20240
        """
        corr = correccion_adelica(17)
        expected = 17 ** 3.5  # ≈ 20257
        
        rel_error = abs(corr - expected) / expected
        
        assert rel_error < 0.01, \
            f"Corrección adélica = {corr:.0f}, esperado ≈ {expected:.0f}"
    
    # ========== Tests para φ⁻³ ==========
    
    def test_phi_cubed_valor(self):
        """
        Test: φ³ ≈ 4.236
        """
        result = justificar_phi_menos_3()
        phi_cubed = result['phi_cubed']
        expected = phi ** 3
        
        assert abs(phi_cubed - expected) < 1e-6, \
            f"φ³ = {phi_cubed:.6f}, esperado = {expected:.6f}"
    
    def test_base_fractal_valor(self):
        """
        Test: b = π/φ³ ≈ 0.741
        """
        result = justificar_phi_menos_3()
        b_fractal = result['base_fractal']
        expected = np.pi / (phi ** 3)
        
        assert abs(b_fractal - expected) < 1e-6, \
            f"b = {b_fractal:.6f}, esperado = {expected:.6f}"
    
    def test_dimension_efectiva_3(self):
        """
        Test: La dimensión efectiva debe ser 3
        """
        result = justificar_phi_menos_3()
        
        assert result['dimension_efectiva'] == 3, \
            "La dimensión efectiva debe ser 3"
    
    # ========== Tests para π/2 ==========
    
    def test_modo_fundamental_pi_sobre_2(self):
        """
        Test: El modo fundamental debe ser π/2
        """
        result = justificar_pi_sobre_2()
        modo = result['modo_fundamental']
        expected = np.pi / 2
        
        assert abs(modo - expected) < 1e-10, \
            f"Modo fundamental = {modo:.6f}, esperado = {expected:.6f}"
    
    def test_propiedades_satisfechas(self):
        """
        Test: Deben satisfacerse al menos 4 propiedades
        """
        result = justificar_pi_sobre_2()
        propiedades = result['propiedades_satisfechas']
        
        assert len(propiedades) >= 4, \
            f"Deben satisfacerse ≥4 propiedades, obtenidas: {len(propiedades)}"
    
    # ========== Tests para correcciones ==========
    
    def test_correccion_fractal_pi3(self):
        """
        Test: Corrección fractal π³ ≈ 31
        """
        corr = correccion_fractal_pi()
        expected = np.pi ** 3
        
        rel_error = abs(corr - expected) / expected
        
        assert rel_error < 1e-10, \
            f"Corrección fractal = {corr:.2f}, esperado = {expected:.2f}"
    
    def test_correccion_phi6(self):
        """
        Test: Corrección φ⁶ ≈ 17.94
        """
        corr = correccion_phi()
        expected = phi ** 6
        
        rel_error = abs(corr - expected) / expected
        
        assert rel_error < 1e-10, \
            f"Corrección φ⁶ = {corr:.2f}, esperado = {expected:.2f}"
    
    # ========== Tests para derivación completa ==========
    
    def test_derivacion_completa_estructura(self):
        """
        Test: La derivación completa debe contener todas las secciones
        """
        result = derivacion_completa()
        
        required_keys = [
            'constantes_fundamentales',
            'G_Y',
            'R_Psi',
            'primo_p17',
            'phi_exponente',
            'pi_modo',
            'verificacion'
        ]
        
        for key in required_keys:
            assert key in result, f"Falta la sección '{key}' en el resultado"
    
    def test_g_y_sin_circularidad(self):
        """
        Test: G_Y debe estar marcado como sin dependencia de f₀
        """
        result = derivacion_completa()
        
        assert result['G_Y']['sin_dependencia_f0'] == True, \
            "G_Y debe estar marcado como sin dependencia de f₀"
    
    def test_constantes_fundamentales_presentes(self):
        """
        Test: Las constantes fundamentales deben estar presentes
        """
        result = derivacion_completa()
        const = result['constantes_fundamentales']
        
        required = ['m_P_kg', 'l_P_m', 'Lambda_Q_kg', 'hbar_c_Jm', 'zeta_prime_half']
        
        for key in required:
            assert key in const, f"Falta la constante '{key}'"
            assert const[key] != 0, f"La constante '{key}' no debe ser cero"


def run_tests():
    """Ejecutar todos los tests"""
    print("=" * 80)
    print("TESTS DE DERIVACIÓN DESDE PRIMEROS PRINCIPIOS")
    print("=" * 80)
    print()
    
    test_suite = TestDerivacionPrimerPrincipios()
    
    # Obtener todos los métodos de test
    test_methods = [
        method for method in dir(test_suite) 
        if method.startswith('test_')
    ]
    
    passed = 0
    failed = 0
    
    for method_name in sorted(test_methods):
        method = getattr(test_suite, method_name)
        try:
            method()
            print(f"✅ {method_name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {method_name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {method_name}")
            print(f"   Exception: {type(e).__name__}: {e}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"RESULTADOS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(run_tests())
