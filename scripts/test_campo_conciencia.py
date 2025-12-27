#!/usr/bin/env python3
"""
Tests para el módulo de campo de conciencia.

Valida la consistencia física de todos los parámetros del campo Ψ.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.campo_conciencia import CampoConciencia, h, c, k_B, eV, l_P


def test_inicializacion():
    """Test que el campo se inicializa correctamente."""
    campo = CampoConciencia()
    
    assert campo.f0 == 141.7001, "Frecuencia incorrecta"
    assert campo.E_psi_eV == 5.86e-13, "Energía en eV incorrecta"
    assert campo.lambda_psi == 2.116e6, "Longitud de onda incorrecta"
    assert campo.m_psi == 1.04e-48, "Masa incorrecta"
    assert campo.T_psi == 6.8e-9, "Temperatura incorrecta"
    
    print("✅ test_inicializacion: PASS")


def test_relacion_energia_frecuencia():
    """Test E = hf"""
    campo = CampoConciencia()
    
    E_calculado = h * campo.f0
    E_esperado = campo.E_psi_J
    
    diff_rel = abs(E_calculado - E_esperado) / E_esperado
    
    assert diff_rel < 0.01, f"E = hf no se cumple: diff = {diff_rel*100:.2f}%"
    
    print(f"✅ test_relacion_energia_frecuencia: PASS (diff = {diff_rel*100:.4f}%)")


def test_relacion_longitud_frecuencia():
    """Test λ = c/f"""
    campo = CampoConciencia()
    
    lambda_calculado = c / campo.f0
    lambda_esperado = campo.lambda_psi
    
    diff_rel = abs(lambda_calculado - lambda_esperado) / lambda_esperado
    
    assert diff_rel < 0.01, f"λ = c/f no se cumple: diff = {diff_rel*100:.2f}%"
    
    print(f"✅ test_relacion_longitud_frecuencia: PASS (diff = {diff_rel*100:.4f}%)")


def test_relacion_masa_energia():
    """Test E = mc²"""
    campo = CampoConciencia()
    
    E_calculado = campo.m_psi * c**2
    E_esperado = campo.E_psi_J
    
    diff_rel = abs(E_calculado - E_esperado) / E_esperado
    
    assert diff_rel < 0.01, f"E = mc² no se cumple: diff = {diff_rel*100:.2f}%"
    
    print(f"✅ test_relacion_masa_energia: PASS (diff = {diff_rel*100:.4f}%)")


def test_relacion_temperatura_energia():
    """Test E ≈ k_B T"""
    campo = CampoConciencia()
    
    E_calculado = k_B * campo.T_psi
    E_esperado = campo.E_psi_J
    
    diff_rel = abs(E_calculado - E_esperado) / E_esperado
    
    assert diff_rel < 0.01, f"E = k_B T no se cumple: diff = {diff_rel*100:.2f}%"
    
    print(f"✅ test_relacion_temperatura_energia: PASS (diff = {diff_rel*100:.4f}%)")


def test_verificar_consistencia():
    """Test que todas las verificaciones pasen."""
    campo = CampoConciencia()
    
    resultados = campo.verificar_consistencia()
    
    # Verificar que todas las relaciones sean consistentes
    for nombre, resultado in resultados.items():
        assert resultado['consistente'], f"Verificación {nombre} falló"
    
    print("✅ test_verificar_consistencia: PASS")


def test_valores_positivos():
    """Test que todos los parámetros sean positivos."""
    campo = CampoConciencia()
    
    assert campo.f0 > 0, "Frecuencia debe ser positiva"
    assert campo.E_psi_J > 0, "Energía debe ser positiva"
    assert campo.E_psi_eV > 0, "Energía en eV debe ser positiva"
    assert campo.lambda_psi > 0, "Longitud de onda debe ser positiva"
    assert campo.m_psi > 0, "Masa debe ser positiva"
    assert campo.T_psi > 0, "Temperatura debe ser positiva"
    assert campo.omega_0 > 0, "Frecuencia angular debe ser positiva"
    assert campo.R_psi > 0, "Radio debe ser positivo"
    
    print("✅ test_valores_positivos: PASS")


def test_ordenes_magnitud():
    """Test que los parámetros tengan los órdenes de magnitud esperados."""
    campo = CampoConciencia()
    
    # Frecuencia en rango audible-ultrasónico bajo
    assert 100 < campo.f0 < 200, "Frecuencia fuera de rango esperado"
    
    # Energía extremadamente pequeña
    assert 1e-14 < campo.E_psi_eV < 1e-12, "Energía fuera de rango esperado"
    
    # Longitud de onda en escala de miles de km
    assert 1e6 < campo.lambda_psi < 1e7, "Longitud de onda fuera de rango"
    
    # Masa extremadamente pequeña
    assert 1e-49 < campo.m_psi < 1e-47, "Masa fuera de rango esperado"
    
    # Temperatura extremadamente fría (cerca del cero absoluto)
    assert 1e-10 < campo.T_psi < 1e-8, "Temperatura fuera de rango esperado"
    
    print("✅ test_ordenes_magnitud: PASS")


def test_generar_resumen():
    """Test que el resumen se genera correctamente."""
    campo = CampoConciencia()
    
    resumen = campo.generar_resumen()
    
    # Verificar que el resumen tenga las secciones correctas
    assert 'parametros' in resumen, "Falta sección 'parametros'"
    assert 'verificaciones' in resumen, "Falta sección 'verificaciones'"
    assert 'ratios_adimensionales' in resumen, "Falta sección 'ratios_adimensionales'"
    
    # Verificar que los parámetros estén en el resumen
    params = resumen['parametros']
    assert 'frecuencia_Hz' in params
    assert 'energia_eV' in params
    assert 'masa_kg' in params
    assert 'temperatura_K' in params
    assert 'longitud_onda_km' in params
    
    print("✅ test_generar_resumen: PASS")


def test_conversion_unidades():
    """Test que las conversiones de unidades sean correctas."""
    campo = CampoConciencia()
    
    # Energía: J a eV
    E_eV_calc = campo.E_psi_J / eV
    diff = abs(E_eV_calc - campo.E_psi_eV) / campo.E_psi_eV
    assert diff < 0.01, f"Conversión J -> eV incorrecta: diff = {diff*100:.2f}%"
    
    # Longitud: m a km
    lambda_km = campo.lambda_psi / 1e3
    assert abs(lambda_km - 2116.0) < 1, "Conversión m -> km incorrecta"
    
    print("✅ test_conversion_unidades: PASS")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 80)
    print("TESTS DEL MÓDULO DE CAMPO DE CONCIENCIA")
    print("=" * 80)
    print()
    
    tests = [
        test_inicializacion,
        test_relacion_energia_frecuencia,
        test_relacion_longitud_frecuencia,
        test_relacion_masa_energia,
        test_relacion_temperatura_energia,
        test_verificar_consistencia,
        test_valores_positivos,
        test_ordenes_magnitud,
        test_generar_resumen,
        test_conversion_unidades
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: FAIL - {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: ERROR - {e}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"RESULTADOS: {passed} tests passed, {failed} tests failed")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
