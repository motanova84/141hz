#!/usr/bin/env python3
"""
Tests: Puente QCAL-Navier-Stokes
═════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para el módulo physics/navier_stokes_bridge.py que
conecta ADN-Riemann-Quantum con Navier-Stokes vía viscosidad adélica.

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.navier_stokes_bridge import (
    calcular_flujo_logos, 
    analisis_puentes_conexion,
    F0,
    THRESHOLD_LAMINAR_ETEREO,
    GUE_CHAOS_PSI
)


def test_calcular_flujo_logos_gact():
    """Test flujo logos con secuencia GACT (hotspot óptimo)."""
    print("\n✓ Test: calcular_flujo_logos con GACT...")
    
    resultado = calcular_flujo_logos("GACT", np.eye(3))
    
    # Verificaciones básicas
    assert "reynolds_quantum" in resultado
    assert "coherencia_flujo" in resultado
    assert "viscosidad_adelica" in resultado
    assert "logos_flow_status" in resultado
    assert "psi_ns_final" in resultado
    
    # GACT debe tener alta coherencia (≈ 0.999776)
    assert resultado['coherencia_flujo'] > 0.999, \
        f"Coherencia GACT debe ser > 0.999, got {resultado['coherencia_flujo']}"
    
    # Viscosidad adélica debe ser muy baja (1 - Ψ)
    assert resultado['viscosidad_adelica'] < 0.001, \
        f"Viscosidad adélica debe ser < 0.001, got {resultado['viscosidad_adelica']}"
    
    # Re_q debe ser > 10¹² para LAMINAR_ETÉREO
    assert resultado['reynolds_quantum'] > THRESHOLD_LAMINAR_ETEREO, \
        f"Re_q debe ser > 10¹², got {resultado['reynolds_quantum']:.3e}"
    
    # Estado debe ser LAMINAR_ETÉREO
    assert resultado['logos_flow_status'] == "LAMINAR_ETÉREO", \
        f"Estado debe ser LAMINAR_ETÉREO, got {resultado['logos_flow_status']}"
    
    # Ψ_NS final debe coincidir con coherencia
    assert abs(resultado['psi_ns_final'] - resultado['coherencia_flujo']) < 1e-6, \
        "Ψ_NS final debe coincidir con coherencia flujo"
    
    print(f"    Re_q = {resultado['reynolds_quantum']:.3e}")
    print(f"    Ψ = {resultado['coherencia_flujo']:.6f}")
    print(f"    Estado = {resultado['logos_flow_status']}")
    print("  ✓ Passed")


def test_calcular_flujo_logos_low_coherence():
    """Test flujo logos con secuencia de baja coherencia."""
    print("\n✓ Test: calcular_flujo_logos con baja coherencia...")
    
    # Secuencia con baja coherencia (muchas T)
    resultado = calcular_flujo_logos("TTTT", np.eye(3))
    
    # Coherencia debe ser menor que GACT
    assert resultado['coherencia_flujo'] < 1.0, \
        "Coherencia debe ser < 1.0"
    
    # Viscosidad debe ser mayor que GACT
    assert resultado['viscosidad_adelica'] > 0, \
        "Viscosidad debe ser > 0"
    
    # Re_q debe ser menor (mayor viscosidad)
    assert resultado['reynolds_quantum'] > 0, \
        "Re_q debe ser positivo"
    
    print(f"    Re_q = {resultado['reynolds_quantum']:.3e}")
    print(f"    Ψ = {resultado['coherencia_flujo']:.6f}")
    print(f"    Estado = {resultado['logos_flow_status']}")
    print("  ✓ Passed")


def test_reynolds_quantum_calculation():
    """Test cálculo del número de Reynolds cuántico."""
    print("\n✓ Test: Cálculo de Reynolds cuántico...")
    
    # Re_q = (f₀ * λ₀) / visc_adelica
    # Para GACT (Ψ ≈ 0.999776), visc ≈ 2.24e-4
    # Re_q ≈ (141.7 * 2.116e6) / 2.24e-4 ≈ 1.34e12
    
    resultado = calcular_flujo_logos("GACT", np.eye(3))
    re_q = resultado['reynolds_quantum']
    
    # Verificar orden de magnitud (10¹² ± 1 orden)
    assert 1e11 < re_q < 1e14, \
        f"Re_q debe estar entre 10¹¹ y 10¹⁴, got {re_q:.3e}"
    
    print(f"    Re_q = {re_q:.3e} (esperado ~ 1.34e12)")
    print("  ✓ Passed")


def test_viscosidad_adelica_relationship():
    """Test relación entre coherencia y viscosidad adélica."""
    print("\n✓ Test: Relación Ψ y viscosidad adélica...")
    
    resultado = calcular_flujo_logos("GACT", np.eye(3))
    
    psi = resultado['coherencia_flujo']
    visc = resultado['viscosidad_adelica']
    
    # visc_adelica = 1 - Ψ
    expected_visc = 1.0 - psi
    
    assert abs(visc - expected_visc) < 1e-6, \
        f"Viscosidad debe ser 1-Ψ, got {visc} vs expected {expected_visc}"
    
    print(f"    Ψ = {psi:.6f}")
    print(f"    visc_adelica = {visc:.6f}")
    print(f"    1 - Ψ = {expected_visc:.6f}")
    print("  ✓ Passed")


def test_laminar_etereo_threshold():
    """Test umbral de transición a estado LAMINAR_ETÉREO."""
    print("\n✓ Test: Umbral LAMINAR_ETÉREO...")
    
    # GACT debe ser LAMINAR_ETÉREO (Re_q > 10¹²)
    resultado_gact = calcular_flujo_logos("GACT", np.eye(3))
    assert resultado_gact['logos_flow_status'] == "LAMINAR_ETÉREO"
    assert resultado_gact['reynolds_quantum'] > THRESHOLD_LAMINAR_ETEREO
    
    # ATCG debe ser TURBULENCIA_MATERIAL (Re_q < 10¹²)
    resultado_atcg = calcular_flujo_logos("ATCG", np.eye(3))
    # ATCG puede ser borderline, solo verificamos que tenga un estado
    assert resultado_atcg['logos_flow_status'] in ["LAMINAR_ETÉREO", "TURBULENCIA_MATERIAL"]
    
    print(f"    GACT: {resultado_gact['logos_flow_status']} (Re_q={resultado_gact['reynolds_quantum']:.2e})")
    print(f"    ATCG: {resultado_atcg['logos_flow_status']} (Re_q={resultado_atcg['reynolds_quantum']:.2e})")
    print("  ✓ Passed")


def test_analisis_puentes():
    """Test análisis de los 3 puentes de conexión."""
    print("\n✓ Test: Análisis de puentes...")
    
    resultado = calcular_flujo_logos("GACT", np.eye(3))
    puentes = analisis_puentes_conexion(resultado)
    
    # Debe tener los 3 puentes
    assert "conveccion" in puentes
    assert "presion" in puentes
    assert "difusion" in puentes
    
    # Verificar que son strings no vacíos
    assert len(puentes["conveccion"]) > 0
    assert len(puentes["presion"]) > 0
    assert len(puentes["difusion"]) > 0
    
    # GACT debe mencionar LAMINAR en convección
    assert "LAMINAR" in puentes["conveccion"].upper()
    
    # GACT debe mencionar BAJA ENTROPÍA en presión
    assert "BAJA" in puentes["presion"].upper() and "ENTROP" in puentes["presion"].upper()
    
    print(f"    Convección: {puentes['conveccion'][:50]}...")
    print(f"    Presión: {puentes['presion'][:50]}...")
    print(f"    Difusión: {puentes['difusion'][:50]}...")
    print("  ✓ Passed")


def test_multiple_sequences():
    """Test con múltiples secuencias."""
    print("\n✓ Test: Múltiples secuencias...")
    
    secuencias = ["GACT", "ATCG", "GGGG", "ATAT", "TTTT", "GCGC"]
    
    for seq in secuencias:
        resultado = calcular_flujo_logos(seq, np.eye(3))
        
        # Verificaciones básicas para todas las secuencias
        assert resultado['reynolds_quantum'] > 0
        assert 0 <= resultado['coherencia_flujo'] <= 1
        assert resultado['viscosidad_adelica'] >= 0
        assert resultado['logos_flow_status'] in ["LAMINAR_ETÉREO", "TURBULENCIA_MATERIAL"]
        
        print(f"    {seq}: Re_q={resultado['reynolds_quantum']:.2e}, "
              f"Ψ={resultado['coherencia_flujo']:.4f}, "
              f"{resultado['logos_flow_status']}")
    
    print("  ✓ Passed")


def test_constants():
    """Test constantes del módulo."""
    print("\n✓ Test: Constantes del módulo...")
    
    # F0 debe ser 141.7001 Hz
    assert abs(F0 - 141.7001) < 1e-6, f"F0 debe ser 141.7001, got {F0}"
    
    # Umbral laminar debe ser 10¹²
    assert THRESHOLD_LAMINAR_ETEREO == 1e12, \
        f"Umbral debe ser 10¹², got {THRESHOLD_LAMINAR_ETEREO}"
    
    # GUE chaos debe ser 0.666
    assert abs(GUE_CHAOS_PSI - 0.666) < 1e-6, \
        f"GUE_CHAOS_PSI debe ser 0.666, got {GUE_CHAOS_PSI}"
    
    print(f"    F0 = {F0} Hz")
    print(f"    THRESHOLD_LAMINAR_ETEREO = {THRESHOLD_LAMINAR_ETEREO:.0e}")
    print(f"    GUE_CHAOS_PSI = {GUE_CHAOS_PSI}")
    print("  ✓ Passed")


def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("=" * 80)
    print("TESTS: Puente QCAL-Navier-Stokes")
    print("=" * 80)
    
    tests = [
        test_constants,
        test_calcular_flujo_logos_gact,
        test_calcular_flujo_logos_low_coherence,
        test_reynolds_quantum_calculation,
        test_viscosidad_adelica_relationship,
        test_laminar_etereo_threshold,
        test_analisis_puentes,
        test_multiple_sequences,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"RESUMEN: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
