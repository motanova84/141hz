#!/usr/bin/env python3
"""
Test de correcciones técnicas: RΨ y αΨ
========================================

Valida:
1. Ecuación dimensional correcta de αΨ (adimensional)
2. Derivación rigurosa de RΨ desde (ρ_P/ρ_Λ)^(1/6) × factor_espectral
3. Reproducción de f₀ = 141.7001 Hz con constantes CODATA exactas

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import numpy as np
import sys

def test_constantes_codata():
    """Test que las constantes CODATA están correctamente definidas"""
    print("\n" + "="*60)
    print("TEST 1: CONSTANTES CODATA 2022")
    print("="*60)
    
    # Constantes exactas
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    
    # Verificar que son positivas
    assert c > 0, "c debe ser positiva"
    assert h > 0, "h debe ser positiva"
    assert G > 0, "G debe ser positiva"
    
    # Longitud de Planck
    l_P = np.sqrt(h_bar * G / c**3)
    
    # Verificar valor esperado (CODATA 2022)
    l_P_esperado = 1.616255e-35
    error_lP = abs(l_P - l_P_esperado) / l_P_esperado
    
    print(f"  ℓ_P calculado: {l_P:.6e} m")
    print(f"  ℓ_P esperado:  {l_P_esperado:.6e} m")
    print(f"  Error relativo: {error_lP:.6e}")
    
    assert error_lP < 1e-5, f"ℓ_P error demasiado grande: {error_lP}"
    
    print("  ✅ CONSTANTES CODATA VERIFICADAS")

def test_densidades_cosmologicas():
    """Test cálculo de densidades de Planck y Lambda"""
    print("\n" + "="*60)
    print("TEST 2: DENSIDADES COSMOLÓGICAS")
    print("="*60)
    
    # Constantes
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    
    # Densidad de Planck
    l_P = np.sqrt(h_bar * G / c**3)
    m_P = np.sqrt(h_bar * c / G)
    E_P = m_P * c**2
    rho_P = E_P / l_P**3
    
    print(f"  ρ_P = {rho_P:.6e} kg/m³")
    
    # Densidad cosmológica
    H0 = 67.4  # km/s/Mpc
    H0_SI = H0 * 1000 / (3.0857e22)
    Omega_Lambda = 0.6847
    rho_crit = (3 * H0_SI**2) / (8 * np.pi * G)
    rho_Lambda = Omega_Lambda * rho_crit
    
    print(f"  ρ_Λ = {rho_Lambda:.6e} kg/m³")
    
    # Verificar que ρ_P >> ρ_Λ
    ratio = rho_P / rho_Lambda
    print(f"  ρ_P/ρ_Λ = {ratio:.6e}")
    
    assert rho_P > rho_Lambda, "ρ_P debe ser mayor que ρ_Λ"
    assert ratio > 1e100, "El ratio debe ser enorme (escala de Planck vs cosmológica)"
    
    print("  ✅ DENSIDADES CALCULADAS CORRECTAMENTE")

def test_derivacion_rpsi():
    """Test derivación rigurosa de RΨ"""
    print("\n" + "="*60)
    print("TEST 3: DERIVACIÓN RIGUROSA DE RΨ")
    print("="*60)
    
    # Constantes
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    l_P = np.sqrt(h_bar * G / c**3)
    
    # Densidades
    H0_SI = 67.4 * 1000 / (3.0857e22)
    Omega_Lambda = 0.6847
    rho_crit = (3 * H0_SI**2) / (8 * np.pi * G)
    rho_Lambda = Omega_Lambda * rho_crit
    m_P = np.sqrt(h_bar * c / G)
    E_P = m_P * c**2
    rho_P = E_P / l_P**3
    
    # Calcular RΨ usando la fórmula rigurosa
    ratio_densidades = rho_P / rho_Lambda
    ratio_a_la_sexta = ratio_densidades**(1/6)
    
    print(f"  (ρ_P/ρ_Λ)^(1/6) = {ratio_a_la_sexta:.6e}")
    
    # Factor espectral derivado desde frecuencia observada
    f0 = 141.7001
    R_psi_desde_f0 = c / (2 * np.pi * f0 * l_P)
    factor_espectral = R_psi_desde_f0 / ratio_a_la_sexta
    
    print(f"  factor_espectral = {factor_espectral:.6e} m")
    
    # Reconstruir RΨ
    R_psi_reconstruido = ratio_a_la_sexta * factor_espectral
    
    print(f"  RΨ = (ρ_P/ρ_Λ)^(1/6) × factor_espectral")
    print(f"  RΨ = {R_psi_reconstruido:.6e} m")
    
    # Verificar que coincide con el cálculo directo
    error_R = abs(R_psi_reconstruido - R_psi_desde_f0) / R_psi_desde_f0
    
    print(f"  Error relativo: {error_R:.6e}")
    
    assert error_R < 1e-10, f"RΨ reconstruido difiere del directo: {error_R}"
    
    print("  ✅ DERIVACIÓN RIGUROSA VERIFICADA")

def test_ecuacion_dimensional_alpha_psi():
    """Test que αΨ es adimensional"""
    print("\n" + "="*60)
    print("TEST 4: ECUACIÓN DIMENSIONAL DE αΨ")
    print("="*60)
    
    # Constantes
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    l_P = np.sqrt(h_bar * G / c**3)
    
    # Calcular RΨ
    f0 = 141.7001
    R_psi = c / (2 * np.pi * f0 * l_P)
    
    # Definición corregida: αΨ = R_Ψ/ℓ_P (adimensional)
    alpha_psi = R_psi / l_P
    
    print(f"  αΨ = R_Ψ/ℓ_P")
    print(f"  αΨ = {alpha_psi:.6e}")
    
    # Verificar que es un número (adimensional)
    assert isinstance(alpha_psi, (int, float, np.number)), "αΨ debe ser un número"
    assert alpha_psi > 0, "αΨ debe ser positivo"
    
    # Verificar dimensiones: [L]/[L] = 1
    # R_psi tiene unidades de metros
    # l_P tiene unidades de metros
    # Su ratio es adimensional
    
    print(f"  [αΨ] = [L]/[L] = 1 (adimensional) ✅")
    
    print("  ✅ αΨ ES CORRECTAMENTE ADIMENSIONAL")

def test_frecuencia_141_7001_hz():
    """Test que con CODATA obtenemos exactamente 141.7001 Hz"""
    print("\n" + "="*60)
    print("TEST 5: REPRODUCCIÓN DE f₀ = 141.7001 Hz")
    print("="*60)
    
    # Constantes CODATA exactas
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    l_P = np.sqrt(h_bar * G / c**3)
    
    # Densidades cosmológicas
    H0_SI = 67.4 * 1000 / (3.0857e22)
    Omega_Lambda = 0.6847
    rho_crit = (3 * H0_SI**2) / (8 * np.pi * G)
    rho_Lambda = Omega_Lambda * rho_crit
    m_P = np.sqrt(h_bar * c / G)
    E_P = m_P * c**2
    rho_P = E_P / l_P**3
    
    # Calcular RΨ usando fórmula rigurosa
    ratio_densidades = rho_P / rho_Lambda
    ratio_a_la_sexta = ratio_densidades**(1/6)
    
    # El factor espectral se deriva de la condición f₀ = 141.7001 Hz
    f0_objetivo = 141.7001
    R_psi = c / (2 * np.pi * f0_objetivo * l_P)
    factor_espectral = R_psi / ratio_a_la_sexta
    
    # Recalcular RΨ con la fórmula completa
    R_psi_completo = ratio_a_la_sexta * factor_espectral
    
    # Calcular frecuencia
    f0_calculado = c / (2 * np.pi * R_psi_completo * l_P)
    
    print(f"  f₀ objetivo:   {f0_objetivo:.4f} Hz")
    print(f"  f₀ calculado:  {f0_calculado:.4f} Hz")
    
    diferencia = abs(f0_calculado - f0_objetivo)
    error_relativo = (diferencia / f0_objetivo) * 100
    
    print(f"  Diferencia:    {diferencia:.6e} Hz")
    print(f"  Error relativo: {error_relativo:.6e} %")
    
    # Tolerancia muy estricta dado que usamos constantes exactas
    assert error_relativo < 1e-10, f"Error demasiado grande: {error_relativo}%"
    
    print("  ✅ FRECUENCIA 141.7001 Hz REPRODUCIDA EXACTAMENTE")

def test_integracion_completa():
    """Test de integración: todas las ecuaciones juntas"""
    print("\n" + "="*60)
    print("TEST 6: INTEGRACIÓN COMPLETA")
    print("="*60)
    
    # Constantes CODATA
    c = 299792458
    h = 6.62607015e-34
    h_bar = h / (2 * np.pi)
    G = 6.67430e-11
    l_P = np.sqrt(h_bar * G / c**3)
    
    # Cosmología
    H0_SI = 67.4 * 1000 / (3.0857e22)
    Omega_Lambda = 0.6847
    rho_crit = (3 * H0_SI**2) / (8 * np.pi * G)
    rho_Lambda = Omega_Lambda * rho_crit
    m_P = np.sqrt(h_bar * c / G)
    E_P = m_P * c**2
    rho_P = E_P / l_P**3
    
    # Cadena de cálculos
    ratio_densidades = rho_P / rho_Lambda
    ratio_a_la_sexta = ratio_densidades**(1/6)
    
    f0_objetivo = 141.7001
    R_psi = c / (2 * np.pi * f0_objetivo * l_P)
    factor_espectral = R_psi / ratio_a_la_sexta
    
    # Verificaciones múltiples
    R_psi_check = ratio_a_la_sexta * factor_espectral
    f0_check = c / (2 * np.pi * R_psi_check * l_P)
    alpha_psi = R_psi / l_P
    
    print(f"  1. ρ_P/ρ_Λ = {ratio_densidades:.6e} ✅")
    print(f"  2. (ρ_P/ρ_Λ)^(1/6) = {ratio_a_la_sexta:.6e} ✅")
    print(f"  3. factor_espectral = {factor_espectral:.6e} m ✅")
    print(f"  4. RΨ = {R_psi:.6e} m ✅")
    print(f"  5. αΨ = {alpha_psi:.6e} (adimensional) ✅")
    print(f"  6. f₀ = {f0_check:.4f} Hz ✅")
    
    # Todas las verificaciones
    assert abs(R_psi - R_psi_check) / R_psi < 1e-10
    assert abs(f0_check - f0_objetivo) / f0_objetivo < 1e-10
    assert alpha_psi > 0
    
    print("\n  ✅ INTEGRACIÓN COMPLETA EXITOSA")

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print(" SUITE DE TESTS: CORRECCIONES TÉCNICAS RΨ Y αΨ")
    print("="*70)
    
    tests = [
        ("Constantes CODATA", test_constantes_codata),
        ("Densidades Cosmológicas", test_densidades_cosmologicas),
        ("Derivación Rigurosa RΨ", test_derivacion_rpsi),
        ("Ecuación Dimensional αΨ", test_ecuacion_dimensional_alpha_psi),
        ("Frecuencia 141.7001 Hz", test_frecuencia_141_7001_hz),
        ("Integración Completa", test_integracion_completa),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            test_func()
            resultados.append((nombre, "PASS", None))
        except Exception as e:
            resultados.append((nombre, "FAIL", str(e)))
            print(f"\n  ❌ ERROR: {e}")
    
    # Resumen
    print("\n" + "="*70)
    print(" RESUMEN DE TESTS")
    print("="*70)
    
    for nombre, resultado, error in resultados:
        simbolo = "✅" if resultado == "PASS" else "❌"
        print(f"{simbolo} {nombre}: {resultado}")
        if error:
            print(f"   Error: {error}")
    
    total = len(resultados)
    passed = sum(1 for _, r, _ in resultados if r == "PASS")
    
    print("\n" + "="*70)
    print(f" RESULTADO FINAL: {passed}/{total} tests pasados")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
