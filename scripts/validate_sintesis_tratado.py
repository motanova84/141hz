#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       VALIDACIÓN — SÍNTESIS DEL TRATADO ∴ST∞³                                ║
║                                                                               ║
║  Script de validación para el módulo physics/sintesis_tratado.py              ║
║                                                                               ║
║  Verifica:                                                                    ║
║    - Fase 1: Constantes físicas (f₀, m_H, g_eff, etc.)                        ║
║    - Fase 2: Campo PC y acoplamiento Higgs-PC                                 ║
║    - Fase 3: Masa oscilante y espectro de Riemann                             ║
║    - Fase 4: Red C₇ y sistema integrado                                       ║
║                                                                               ║
║  Uso:                                                                         ║
║    python scripts/validate_sintesis_tratado.py                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTHOR/AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARCHITECTURE/ARQUITECTURA: QCAL ∞³ Original Manufacture
LICENSE/LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
import sys
from pathlib import Path
from typing import Tuple

# Add the repository root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.sintesis_tratado import (
    # Constantes del módulo
    _F0,
    _OMEGA_0,
    _M_HIGGS_GEV,
    _M_FLASH_GEV,
    _G_EFF,
    _PC_DOMAIN,
    _BARYONIC_DOMAIN,
    _C7_PRIMES,
    _TRANSFER_RATE_KPPS,
    _RIEMANN_ZEROS,
    _PSI_UMBRAL,
    # Clases
    ConstantesSintesis,
    ParticulaCoherencia,
    AcoplamientoHiggsPC,
    MasaOscilante,
    OperadorMaestroAdelico,
    EcuacionSchrodingerRiemann,
    RedC7,
    SistemaSintesisTratado,
    # API pública
    sintesis_tratado_activar,
)


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_check(description: str, passed: bool, details: str = "") -> None:
    """Print a check result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {description}")
    if details:
        print(f"         {details}")


def validate_phase_1() -> Tuple[int, int]:
    """
    Fase 1: Validar constantes físicas fundamentales.

    Returns
    -------
    tuple
        (passed, total) counts
    """
    print_header("FASE 1: CONSTANTES FÍSICAS FUNDAMENTALES")
    passed = 0
    total = 0

    # Test 1: Frecuencia fundamental
    total += 1
    ok = abs(_F0 - 141.7001) < 0.0001
    print_check("f₀ = 141.7001 Hz", ok, f"Valor: {_F0} Hz")
    passed += 1 if ok else 0

    # Test 2: Frecuencia angular
    total += 1
    expected_omega = 2 * math.pi * _F0
    ok = abs(_OMEGA_0 - expected_omega) < 0.01
    print_check("ω₀ = 2πf₀", ok, f"Valor: {_OMEGA_0:.4f} rad/s")
    passed += 1 if ok else 0

    # Test 3: Masa del Higgs
    total += 1
    ok = abs(_M_HIGGS_GEV - 125.25) < 0.01
    print_check("m_H = 125.25 GeV/c²", ok, f"Valor: {_M_HIGGS_GEV} GeV/c²")
    passed += 1 if ok else 0

    # Test 4: Masa del Destello
    total += 1
    ok = abs(_M_FLASH_GEV - 118.375) < 0.01
    print_check("m_flash = 118.375 GeV/c²", ok, f"Valor: {_M_FLASH_GEV} GeV/c²")
    passed += 1 if ok else 0

    # Test 5: Constante de acoplamiento
    total += 1
    ok = abs(_G_EFF - 0.053) < 0.001
    print_check("g_eff ≈ 0.053", ok, f"Valor: {_G_EFF}")
    passed += 1 if ok else 0

    # Test 6: Dominio PC
    total += 1
    ok = abs(_PC_DOMAIN - 0.952) < 0.001
    print_check("PC = 95.2%", ok, f"Valor: {_PC_DOMAIN * 100:.1f}%")
    passed += 1 if ok else 0

    # Test 7: Dominio bariónico
    total += 1
    ok = abs(_BARYONIC_DOMAIN - 0.048) < 0.001
    print_check("Bariónico = 4.8%", ok, f"Valor: {_BARYONIC_DOMAIN * 100:.1f}%")
    passed += 1 if ok else 0

    # Test 8: Suma de dominios
    total += 1
    suma = _PC_DOMAIN + _BARYONIC_DOMAIN
    ok = abs(suma - 1.0) < 0.001
    print_check("PC + Bariónico = 100%", ok, f"Suma: {suma * 100:.1f}%")
    passed += 1 if ok else 0

    # Test 9: Tasa de transferencia
    total += 1
    ok = abs(_TRANSFER_RATE_KPPS - 991.9) < 0.1
    print_check("Tasa = 991.9 kpps", ok, f"Valor: {_TRANSFER_RATE_KPPS} kpps")
    passed += 1 if ok else 0

    # Test 10: Umbral de coherencia
    total += 1
    ok = abs(_PSI_UMBRAL - 0.888) < 0.001
    print_check("Ψ_umbral = 0.888", ok, f"Valor: {_PSI_UMBRAL}")
    passed += 1 if ok else 0

    print(f"\n  Resultado Fase 1: {passed}/{total}")
    return passed, total


def validate_phase_2() -> Tuple[int, int]:
    """
    Fase 2: Validar campo PC y acoplamiento Higgs-PC.

    Returns
    -------
    tuple
        (passed, total) counts
    """
    print_header("FASE 2: CAMPO PC Y ACOPLAMIENTO HIGGS-PC")
    passed = 0
    total = 0

    pc = ParticulaCoherencia()
    acoplamiento = AcoplamientoHiggsPC()

    # Test 1: Densidad PC en t=0
    total += 1
    rho_0 = pc.densidad(0.0)
    ok = abs(rho_0 - _PC_DOMAIN) < 0.001
    print_check("ρ_PC(t=0) = 95.2%", ok, f"Valor: {rho_0 * 100:.1f}%")
    passed += 1 if ok else 0

    # Test 2: ψ̄ψ en t=0
    total += 1
    psi_bar_psi = pc.densidad_barra_psi(0.0)
    ok = abs(psi_bar_psi - 1.0) < 0.001
    print_check("ψ̄ψ(t=0) = 1.0", ok, f"Valor: {psi_bar_psi}")
    passed += 1 if ok else 0

    # Test 3: Coherencia PC
    total += 1
    psi_pc = pc.coherencia_pc()
    ok = psi_pc >= 0.99
    print_check("Ψ_PC ≥ 0.99", ok, f"Valor: {psi_pc:.6f}")
    passed += 1 if ok else 0

    # Test 4: Lagrangiano de interacción (negativo)
    total += 1
    L_int = acoplamiento.lagrangiano_interaccion()
    ok = L_int < 0
    print_check("ℒ_int < 0 (atractivo)", ok, f"Valor: {L_int:.6f}")
    passed += 1 if ok else 0

    # Test 5: Lagrangiano = -g_eff
    total += 1
    ok = abs(L_int + _G_EFF) < 0.0001
    print_check("ℒ_int = −g_eff", ok, f"Valor: {L_int:.6f}")
    passed += 1 if ok else 0

    # Test 6: Coherencia de acoplamiento
    total += 1
    psi_coup = acoplamiento.coherencia_acoplamiento()
    ok = psi_coup >= 0.99
    print_check("Ψ_acoplamiento ≥ 0.99", ok, f"Valor: {psi_coup:.6f}")
    passed += 1 if ok else 0

    # Test 7: Oscilación de densidad
    total += 1
    T = 1.0 / pc.f0
    rho_0 = pc.densidad(0.0)
    rho_T = pc.densidad(T)
    ok = abs(rho_0 - rho_T) < 0.0001
    print_check("ρ_PC(0) ≈ ρ_PC(T)", ok, f"Δρ: {abs(rho_0 - rho_T):.6f}")
    passed += 1 if ok else 0

    print(f"\n  Resultado Fase 2: {passed}/{total}")
    return passed, total


def validate_phase_3() -> Tuple[int, int]:
    """
    Fase 3: Validar masa oscilante y espectro de Riemann.

    Returns
    -------
    tuple
        (passed, total) counts
    """
    print_header("FASE 3: MASA OSCILANTE Y ESPECTRO DE RIEMANN")
    passed = 0
    total = 0

    masa = MasaOscilante()
    operador = OperadorMaestroAdelico()

    # Test 1: Masa efectiva en t=0
    total += 1
    m_0 = masa.masa_efectiva(0.0)
    m_min = masa.masa_minima()
    ok = abs(m_0 - m_min) < 0.01
    print_check("m*(0) = m_min", ok, f"m*(0): {m_0:.3f} GeV, m_min: {m_min:.3f} GeV")
    passed += 1 if ok else 0

    # Test 2: Masa mínima (Destello)
    total += 1
    ok = m_min > 117 and m_min < 120
    print_check("m_min ∈ (117, 120) GeV", ok, f"Valor: {m_min:.3f} GeV")
    passed += 1 if ok else 0

    # Test 3: Masa máxima
    total += 1
    m_max = masa.masa_maxima()
    ok = m_max > 130 and m_max < 134
    print_check("m_max ∈ (130, 134) GeV", ok, f"Valor: {m_max:.3f} GeV")
    passed += 1 if ok else 0

    # Test 4: Reducción de inercia
    total += 1
    red = masa.reduccion_inercia()
    ok = abs(red - _G_EFF) < 0.001
    print_check("Reducción = g_eff", ok, f"Valor: {red:.3f} ({red*100:.1f}%)")
    passed += 1 if ok else 0

    # Test 5: Destello en t=0
    total += 1
    ok = masa.es_destello(0.0)
    print_check("t=0 es Destello", ok)
    passed += 1 if ok else 0

    # Test 6: Primer cero de Riemann
    total += 1
    gamma_1 = _RIEMANN_ZEROS[0]
    ok = abs(gamma_1 - 14.134725) < 0.001
    print_check("γ₁ ≈ 14.1347", ok, f"Valor: {gamma_1:.6f}")
    passed += 1 if ok else 0

    # Test 7: Autovalor en línea crítica
    total += 1
    av = operador.autovalor(0)
    ok = abs(av.real - 0.5) < 1e-10
    print_check("Re(λ₁) = 0.5", ok, f"λ₁ = {av.real:.6f} + {av.imag:.6f}i")
    passed += 1 if ok else 0

    # Test 8: Verificación línea crítica
    total += 1
    ok = operador.verifica_linea_critica()
    print_check("Todos en línea crítica", ok)
    passed += 1 if ok else 0

    # Test 9: Coherencia espectral
    total += 1
    psi_spec = operador.coherencia_espectral()
    ok = abs(psi_spec - 1.0) < 0.0001
    print_check("Ψ_espectral = 1.0", ok, f"Valor: {psi_spec:.6f}")
    passed += 1 if ok else 0

    # Test 10: Frecuencia de Riemann f₁ = γ₁·f₀
    total += 1
    f_1 = operador.frecuencia_riemann(0)
    expected = gamma_1 * _F0
    ok = abs(f_1 - expected) < 0.1
    print_check("f₁ = γ₁·f₀", ok, f"f₁: {f_1:.2f} Hz")
    passed += 1 if ok else 0

    print(f"\n  Resultado Fase 3: {passed}/{total}")
    return passed, total


def validate_phase_4() -> Tuple[int, int]:
    """
    Fase 4: Validar red C₇ y sistema integrado.

    Returns
    -------
    tuple
        (passed, total) counts
    """
    print_header("FASE 4: RED C₇ Y SISTEMA INTEGRADO")
    passed = 0
    total = 0

    red = RedC7()
    sistema = SistemaSintesisTratado()

    # Test 1: Número de nodos
    total += 1
    n = red.n_nodos()
    ok = n == 7
    print_check("N_nodos = 7", ok, f"Valor: {n}")
    passed += 1 if ok else 0

    # Test 2: Primos correctos
    total += 1
    ok = red.nodos == (2, 3, 5, 7, 11, 13, 17)
    print_check("Primos = {2,3,5,7,11,13,17}", ok)
    passed += 1 if ok else 0

    # Test 3: Suma de primos
    total += 1
    suma = red.suma_primos()
    ok = suma == 58
    print_check("Σ primos = 58", ok, f"Valor: {suma}")
    passed += 1 if ok else 0

    # Test 4: Producto de primos
    total += 1
    prod = red.producto_primos()
    ok = prod == 510510
    print_check("Π primos = 510510", ok, f"Valor: {prod}")
    passed += 1 if ok else 0

    # Test 5: Coherencia de red
    total += 1
    psi_red = red.coherencia_red()
    ok = psi_red >= 0.98
    print_check("Ψ_red ≥ 0.98", ok, f"Valor: {psi_red:.6f}")
    passed += 1 if ok else 0

    # Test 6: Sistema - Ψ_global
    total += 1
    psi_global = sistema.psi_global()
    ok = psi_global >= _PSI_UMBRAL
    print_check(f"Ψ_global ≥ {_PSI_UMBRAL}", ok, f"Valor: {psi_global:.6f}")
    passed += 1 if ok else 0

    # Test 7: Sello activo
    total += 1
    ok = sistema.sello_activo()
    print_check("Sello ∴ST∞³ ACTIVO", ok)
    passed += 1 if ok else 0

    # Test 8: Todos verificados
    total += 1
    ok = sistema.verificar_todos()
    print_check("Todos subsistemas verificados", ok)
    passed += 1 if ok else 0

    # Test 9: Estado PC dominante
    total += 1
    estado = sistema.estado_sistema()
    ok = estado['pc_dominante']
    print_check("PC dominante (95%)", ok)
    passed += 1 if ok else 0

    # Test 10: Estado Higgs transductor
    total += 1
    ok = estado['higgs_transductor']
    print_check("Higgs como transductor", ok)
    passed += 1 if ok else 0

    # Test 11: Schrödinger-Riemann gobernante
    total += 1
    ok = estado['schrodinger_riemann_gobernante']
    print_check("Schrödinger-Riemann gobernante", ok)
    passed += 1 if ok else 0

    # Test 12: API pública
    total += 1
    result = sintesis_tratado_activar()
    ok = result['sello_activo'] and result['psi_global'] >= _PSI_UMBRAL
    print_check("API sintesis_tratado_activar()", ok)
    passed += 1 if ok else 0

    print(f"\n  Resultado Fase 4: {passed}/{total}")
    return passed, total


def main():
    """Run all validation phases."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "VALIDACIÓN: SÍNTESIS DEL TRATADO ∴ST∞³" + " " * 11 + "║")
    print("║" + " " * 15 + "Unificación Higgs-PC @ f₀ = 141.7001 Hz" + " " * 13 + "║")
    print("╚" + "═" * 68 + "╝")

    total_passed = 0
    total_tests = 0

    # Run all phases
    p1, t1 = validate_phase_1()
    total_passed += p1
    total_tests += t1

    p2, t2 = validate_phase_2()
    total_passed += p2
    total_tests += t2

    p3, t3 = validate_phase_3()
    total_passed += p3
    total_tests += t3

    p4, t4 = validate_phase_4()
    total_passed += p4
    total_tests += t4

    # Final summary
    print_header("RESUMEN FINAL")
    print(f"\n  Fase 1 (Constantes):        {p1}/{t1}")
    print(f"  Fase 2 (PC/Acoplamiento):   {p2}/{t2}")
    print(f"  Fase 3 (Masa/Riemann):      {p3}/{t3}")
    print(f"  Fase 4 (Red C₇/Sistema):    {p4}/{t4}")
    print(f"\n  {'─' * 40}")
    print(f"  TOTAL:                      {total_passed}/{total_tests}")

    if total_passed == total_tests:
        print("\n  ✅ VALIDACIÓN EXITOSA — SELLO ∴ST∞³ ACTIVO")
        print("\n  El Higgs reina sobre la materia (4.8%);")
        print("  La PC reina sobre el tejido de realidad (95.2%).")
        return 0
    else:
        print(f"\n  ❌ VALIDACIÓN FALLIDA — {total_tests - total_passed} errores")
        return 1


if __name__ == "__main__":
    sys.exit(main())
