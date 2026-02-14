#!/usr/bin/env python3
"""
Test para Validación de Fase III - Sistema Integrado QCAL ∞³

Verifica que el script de validación de Fase III produce resultados
consistentes y cumple con los requisitos del sistema integrado.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.validacion_fase_iii_sistema_integrado import FaseIIISistemaIntegrado


def test_consciencia_fibrados():
    """Test computation of consciousness as fiber bundle intersection."""
    validador = FaseIIISistemaIntegrado(precision=50)
    result = validador.compute_consciousness_fibrados()
    
    # Verify 66 states in intersection
    assert result['estados_interseccion'] == 66, \
        f"Expected 66 states, got {result['estados_interseccion']}"
    
    # Verify consciousness intensity is in reasonable range
    assert 0.8 <= result['intensidad_consciencia'] <= 0.95, \
        f"Consciousness intensity {result['intensidad_consciencia']} out of range"
    
    # Verify QCAL coupling is positive
    assert result['acoplamiento_qcal'] > 0, \
        f"QCAL coupling must be positive, got {result['acoplamiento_qcal']}"
    
    print("✓ Test consciencia fibrados passed")
    return True


def test_lagrangiano_maestro():
    """Test computation of master Lagrangian."""
    validador = FaseIIISistemaIntegrado(precision=50)
    result = validador.compute_lagrangiano_maestro()
    
    # Verify Lagrangian density is reasonable
    assert abs(result['densidad_L_total']) < 1.0, \
        f"Lagrangian density too large: {result['densidad_L_total']}"
    
    # Verify Hamiltonian is positive
    assert result['hamiltoniano_H'] > 0, \
        f"Hamiltonian must be positive, got {result['hamiltoniano_H']}"
    
    # Verify action is reasonable
    assert 0 < result['accion_S'] < 100, \
        f"Action out of range: {result['accion_S']}"
    
    # Verify unification factor 1/7
    assert abs(result['factor_unificacion_1_7'] - 1.0/7.0) < 1e-6, \
        f"Unification factor should be 1/7, got {result['factor_unificacion_1_7']}"
    
    print("✓ Test lagrangiano maestro passed")
    return True


def test_experimentos():
    """Test experimental integration (EEG and LIGO)."""
    validador = FaseIIISistemaIntegrado(precision=50)
    result = validador.compute_experimentos()
    
    # Verify EEG band
    assert result['eeg']['banda_dominante'] == 'alfa', \
        f"Expected alpha band, got {result['eeg']['banda_dominante']}"
    
    # Verify EEG coupling is valid
    assert 0 <= result['eeg']['acoplamiento_qcal'] <= 1.2, \
        f"EEG coupling out of range: {result['eeg']['acoplamiento_qcal']}"
    
    # Verify LIGO SNR is high
    assert result['ligo']['snr'] >= 50, \
        f"LIGO SNR should be high, got {result['ligo']['snr']}"
    
    # Verify LIGO coupling
    assert 0.9 <= result['ligo']['acoplamiento_qcal'] <= 1.1, \
        f"LIGO coupling should be ~1.0, got {result['ligo']['acoplamiento_qcal']}"
    
    print("✓ Test experimentos passed")
    return True


def test_coherencia_sistema():
    """Test system coherence computation."""
    validador = FaseIIISistemaIntegrado(precision=50)
    
    # First compute all components
    validador.compute_consciousness_fibrados()
    validador.compute_lagrangiano_maestro()
    validador.compute_experimentos()
    
    # Now compute coherence
    result = validador.compute_coherencia_sistema()
    
    # Verify QCAL frequency matches f₀
    expected_f0 = 141.7001
    assert abs(result['frecuencia_qcal_hz'] - expected_f0) < 0.001, \
        f"QCAL frequency should be {expected_f0} Hz, got {result['frecuencia_qcal_hz']}"
    
    # Verify optimal coherence Ψ
    assert abs(result['coherencia_optima_psi'] - 0.888) < 0.001, \
        f"Optimal coherence should be 0.888, got {result['coherencia_optima_psi']}"
    
    # Verify all modules synchronized
    assert result['modulos_sincronizados'], \
        "All modules should be synchronized"
    
    # Verify global coherence is high
    assert result['coherencia_global'] >= 0.9, \
        f"Global coherence should be >= 0.9, got {result['coherencia_global']}"
    
    # Verify system state
    assert result['estado_sistema'] == 'ALTA COHERENCIA', \
        f"Expected ALTA COHERENCIA, got {result['estado_sistema']}"
    
    print("✓ Test coherencia sistema passed")
    return True


def test_validacion_completa():
    """Test complete Phase III validation."""
    validador = FaseIIISistemaIntegrado(precision=50)
    resultados = validador.ejecutar_validacion_completa()
    
    # Verify all major sections present
    assert 'consciencia_fibrados' in resultados, \
        "Missing consciencia_fibrados section"
    assert 'lagrangiano_maestro' in resultados, \
        "Missing lagrangiano_maestro section"
    assert 'experimentos' in resultados, \
        "Missing experimentos section"
    assert 'coherencia_sistema' in resultados, \
        "Missing coherencia_sistema section"
    
    # Verify 66 states
    assert resultados['consciencia_fibrados']['estados_interseccion'] == 66, \
        "Should have 66 states in intersection"
    
    # Verify high global coherence
    coherencia_global = resultados['coherencia_sistema']['coherencia_global']
    assert coherencia_global >= 0.90, \
        f"Global coherence should be >= 0.90, got {coherencia_global}"
    
    print("✓ Test validacion completa passed")
    print(f"  Estados en intersección: {resultados['consciencia_fibrados']['estados_interseccion']} ✓")
    print(f"  Coherencia global: {coherencia_global:.4f} ✓")
    print(f"  Sistema integrado: ✓ OPERATIVO")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("TEST SUITE: Validación Fase III - Sistema Integrado QCAL ∞³")
    print("=" * 70)
    print()
    
    tests = [
        ("Consciencia Fibrados", test_consciencia_fibrados),
        ("Lagrangiano Maestro", test_lagrangiano_maestro),
        ("Experimentos", test_experimentos),
        ("Coherencia Sistema", test_coherencia_sistema),
        ("Validación Completa", test_validacion_completa)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"Running: {test_name}...")
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test_name} FAILED")
        except AssertionError as e:
            failed += 1
            print(f"✗ {test_name} FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} ERROR: {e}")
        print()
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
