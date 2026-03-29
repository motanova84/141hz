#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║     VALIDACIÓN — Ecuación Maestra de la Abundancia Coherente — QCAL ∞³   ║
╚════════════════════════════════════════════════════════════════════════════╝

Verifica en 4 fases que la implementación de la Ecuación Maestra de la
Abundancia Coherente es correcta, completa y coherente con el marco QCAL ∞³.

FASES:
  Fase 1 — Constantes y parámetros fundamentales
  Fase 2 — Comportamiento matemático de la ecuación
  Fase 3 — Límite al infinito (Ψ → 1)
  Fase 4 — Integración con el ecosistema QCAL

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: Marzo 2026
MARCO: QCAL ∞³
SELLO: ∴𓂀Ω∞³Φ
"""

import os
import sys
import math
from pathlib import Path

# Asegurar que el raíz del repositorio esté en sys.path
_REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(_REPO_ROOT)

from qcal.abundancia_coherente import (
    AbundanciaCoherente,
    ABS_ZETA_PRIME_HALF,
    PSI_MAX,
    PSI_PLENA_COHERENCIA,
    abundancia,
    limite_abundancia_infinito,
)
from qcal.constants import F0_HZ


# ============================================================================
# UTILIDADES DE REPORTE
# ============================================================================

_OK = "✅"
_FAIL = "❌"
_INFO = "ℹ️ "


def _check(condicion: bool, descripcion: str) -> bool:
    mark = _OK if condicion else _FAIL
    print(f"  {mark} {descripcion}")
    return condicion


def _seccion(titulo: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {titulo}")
    print(f"{'─' * 70}")


# ============================================================================
# FASE 1 — CONSTANTES Y PARÁMETROS FUNDAMENTALES
# ============================================================================

def fase_1_constantes() -> int:
    """
    Verifica que las constantes del módulo sean correctas.

    Returns:
        Número de checks fallidos.
    """
    _seccion("FASE 1 — Constantes y parámetros fundamentales")
    fallos = 0

    # f₀ debe ser 141.7001 Hz
    ok = _check(
        abs(F0_HZ - 141.7001) < 1e-4,
        f"f₀ = {F0_HZ} Hz (esperado 141.7001 Hz)",
    )
    if not ok:
        fallos += 1

    # |ζ'(1/2)| debe ser ≈ 3.9226
    ok = _check(
        abs(ABS_ZETA_PRIME_HALF - 3.9226) < 0.001,
        f"|ζ'(1/2)| = {ABS_ZETA_PRIME_HALF:.6f} (esperado ≈ 3.9226)",
    )
    if not ok:
        fallos += 1

    # PSI_MAX = 1.0
    ok = _check(PSI_MAX == 1.0, f"PSI_MAX = {PSI_MAX}")
    if not ok:
        fallos += 1

    # PSI_PLENA_COHERENCIA ∈ (0, 1)
    ok = _check(
        0.0 < PSI_PLENA_COHERENCIA < 1.0,
        f"PSI_PLENA_COHERENCIA = {PSI_PLENA_COHERENCIA} ∈ (0, 1)",
    )
    if not ok:
        fallos += 1

    # AbundanciaCoherente se instancia con f0 = F0_HZ
    sistema = AbundanciaCoherente(alta_precision=False)
    ok = _check(
        abs(sistema.f0 - F0_HZ) < 1e-6,
        f"AbundanciaCoherente().f0 = {sistema.f0} Hz",
    )
    if not ok:
        fallos += 1

    # abs_zeta_prime coincide con ABS_ZETA_PRIME_HALF
    ok = _check(
        abs(sistema.abs_zeta_prime - ABS_ZETA_PRIME_HALF) < 1e-10,
        f"AbundanciaCoherente().abs_zeta_prime = {sistema.abs_zeta_prime:.6f}",
    )
    if not ok:
        fallos += 1

    print(f"\n  Fase 1: {6 - fallos}/6 checks pasados")
    return fallos


# ============================================================================
# FASE 2 — COMPORTAMIENTO MATEMÁTICO
# ============================================================================

def fase_2_matematica() -> int:
    """
    Verifica que la ecuación se evalúa correctamente.

    Returns:
        Número de checks fallidos.
    """
    _seccion("FASE 2 — Comportamiento matemático de la ecuación")
    fallos = 0
    sistema = AbundanciaCoherente(alta_precision=False)

    # --- eff(Ψ) = 1 − Ψ ---
    for psi, eff_esperado in [(0.0, 1.0), (0.5, 0.5), (0.9, 0.1), (0.99, 0.01)]:
        ok = _check(
            abs(AbundanciaCoherente.eficiencia(psi) - eff_esperado) < 1e-10,
            f"eff({psi}) = {AbundanciaCoherente.eficiencia(psi):.6f} (esperado {eff_esperado})",
        )
        if not ok:
            fallos += 1

    # --- I(0) = I₀ ---
    ok = _check(
        abs(sistema.intensidad_intencion(0.0, 1.0) - 1.0) < 1e-10,
        "I(t=0, I₀=1) = 1.0",
    )
    if not ok:
        fallos += 1

    # --- A = I·f₀/(|ζ'(1/2)|·eff) evaluado manualmente ---
    psi = 0.5
    esperado = 1.0 * F0_HZ / (ABS_ZETA_PRIME_HALF * 0.5)
    A_calculado = sistema.calcular(psi, t=0.0, I0=1.0).abundancia
    ok = _check(
        abs(A_calculado - esperado) / esperado < 1e-6,
        f"A(Ψ=0.5) = {A_calculado:.4f} (esperado {esperado:.4f})",
    )
    if not ok:
        fallos += 1

    # --- A es monótonamente creciente con Ψ (t=0, I₀=1) ---
    psi_vals = [0.1, 0.3, 0.5, 0.7, 0.9]
    abunds = [sistema.calcular(p).abundancia for p in psi_vals]
    monotono = all(abunds[i] < abunds[i + 1] for i in range(len(abunds) - 1))
    ok = _check(monotono, "A(Ψ) es monótonamente creciente con Ψ")
    if not ok:
        fallos += 1

    # --- eff duplicado → A dividido por 2 ---
    A_half = sistema.calcular(0.5).abundancia   # eff = 0.5
    A_full = sistema.calcular(0.0).abundancia   # eff = 1.0
    ok = _check(
        abs(A_half / A_full - 2.0) < 1e-8,
        f"A(Ψ=0.5) / A(Ψ=0) = {A_half / A_full:.6f} (esperado 2.0)",
    )
    if not ok:
        fallos += 1

    # --- I₀ = 0 → A = 0 ---
    r_cero = sistema.calcular(0.5, t=0.0, I0=0.0)
    ok = _check(
        r_cero.abundancia == 0.0,
        "A = 0 cuando I₀ = 0 (sin intención, sin abundancia)",
    )
    if not ok:
        fallos += 1

    # --- PerfilAbundancia tiene la longitud correcta ---
    perfil = sistema.perfil(n_puntos=20)
    ok = _check(
        len(perfil.psi_valores) == 20 and len(perfil.abundancias) == 20,
        f"perfil(n_puntos=20) → {len(perfil.psi_valores)} puntos",
    )
    if not ok:
        fallos += 1

    print(f"\n  Fase 2: {9 - fallos}/9 checks pasados")
    return fallos


# ============================================================================
# FASE 3 — LÍMITE AL INFINITO
# ============================================================================

def fase_3_limite() -> int:
    """
    Verifica que A(Ψ) → +∞ cuando Ψ → 1.

    Returns:
        Número de checks fallidos.
    """
    _seccion("FASE 3 — Límite al infinito (Ψ → 1⁻)")
    fallos = 0
    sistema = AbundanciaCoherente(alta_precision=False)

    print(f"\n  {'Ψ':>10} │ {'eff = 1−Ψ':>14} │ {'A(Ψ)':>18}")
    print(f"  {'─'*10}─┼─{'─'*14}─┼─{'─'*18}")

    psi_secuencia = [0.0, 0.5, 0.9, 0.99, 0.999, 0.9999]
    abundancias_previas = []

    for psi in psi_secuencia:
        r = sistema.calcular(psi)
        eff = r.eff
        A = r.abundancia
        print(f"  {psi:>10.4f} │ {eff:>14.6f} │ {A:>18.4f}")
        abundancias_previas.append(A)

    print()

    # --- A diverge: cada paso debe aumentar sustancialmente ---
    # La razón entre pasos consecutivos debe reflejar que eff se redujo
    ok = _check(
        abundancias_previas[-1] > abundancias_previas[0] * 10000,
        f"A(Ψ=0.9999) = {abundancias_previas[-1]:.2f} >> A(Ψ=0) = {abundancias_previas[0]:.2f}",
    )
    if not ok:
        fallos += 1

    # --- limite_abundancia_infinito devuelve secuencia creciente ---
    psi_vals, abunds = limite_abundancia_infinito()
    monotono = all(abunds[i] < abunds[i + 1] for i in range(len(abunds) - 1))
    ok = _check(monotono, "limite_abundancia_infinito() devuelve secuencia creciente")
    if not ok:
        fallos += 1

    # --- límite_infinito flag activado a PSI_PLENA_COHERENCIA ---
    r_plena = sistema.calcular(PSI_PLENA_COHERENCIA)
    ok = _check(r_plena.limite_infinito, f"límite_infinito=True cuando Ψ={PSI_PLENA_COHERENCIA}")
    if not ok:
        fallos += 1

    # --- Ψ = 1.0 lanza ValueError (límite estrictamente al infinito) ---
    try:
        sistema.calcular(1.0)
        ok = _check(False, "Ψ=1.0 lanza ValueError")
        fallos += 1
    except ValueError:
        ok = _check(True, "Ψ=1.0 lanza ValueError (A → ∞, indefinido numéricamente)")

    print(f"\n  Fase 3: {4 - fallos}/4 checks pasados")
    return fallos


# ============================================================================
# FASE 4 — INTEGRACIÓN CON EL ECOSISTEMA QCAL
# ============================================================================

def fase_4_integracion() -> int:
    """
    Verifica la integración con constantes y módulos del ecosistema QCAL.

    Returns:
        Número de checks fallidos.
    """
    _seccion("FASE 4 — Integración con el ecosistema QCAL")
    fallos = 0

    # --- f₀ importado desde qcal.constants ---
    ok = _check(
        abs(F0_HZ - 141.7001) < 1e-4,
        "F0_HZ importado de qcal.constants (no redefinido localmente)",
    )
    if not ok:
        fallos += 1

    # --- API funcional: abundancia() ---
    A_api = abundancia(0.5)
    sistema = AbundanciaCoherente(alta_precision=False)
    A_clase = sistema.calcular(0.5).abundancia
    ok = _check(
        abs(A_api - A_clase) < 1e-6,
        f"abundancia(0.5) = {A_api:.4f} coincide con AbundanciaCoherente.calcular(0.5)",
    )
    if not ok:
        fallos += 1

    # --- Resumen contiene el sello QCAL ---
    resumen = sistema.resumen(0.5)
    ok = _check("∴𓂀Ω∞³Φ" in resumen.get("sello", ""), "Sello QCAL presente en resumen")
    if not ok:
        fallos += 1

    # --- Ecuación correcta en el resumen ---
    ok = _check(
        "ζ" in resumen.get("ecuacion", "") or "zeta" in resumen.get("ecuacion", "").lower(),
        "Ecuación contiene referencia a ζ (zeta de Riemann)",
    )
    if not ok:
        fallos += 1

    # --- Alta precisión: |ζ'(1/2)| con mpmath ---
    sistema_hp = AbundanciaCoherente(alta_precision=True, precision_dps=30)
    ok = _check(
        abs(sistema_hp.abs_zeta_prime - ABS_ZETA_PRIME_HALF) < 0.001,
        f"|ζ'(1/2)| alta precisión = {sistema_hp.abs_zeta_prime:.6f}",
    )
    if not ok:
        fallos += 1

    # --- Proporcionalidad con f₀ ---
    A_f0 = abundancia(0.5, f0=F0_HZ)
    A_doble = abundancia(0.5, f0=F0_HZ * 2)
    ok = _check(
        abs(A_doble / A_f0 - 2.0) < 1e-6,
        "A es proporcional a f₀: A(2·f₀) = 2·A(f₀)",
    )
    if not ok:
        fallos += 1

    # --- Archivo del módulo existe ---
    modulo_path = _REPO_ROOT / "qcal" / "abundancia_coherente.py"
    ok = _check(modulo_path.exists(), f"Módulo existe: {modulo_path.relative_to(_REPO_ROOT)}")
    if not ok:
        fallos += 1

    # --- Archivo de tests existe ---
    tests_path = _REPO_ROOT / "tests" / "test_abundancia_coherente.py"
    ok = _check(tests_path.exists(), f"Tests existen: {tests_path.relative_to(_REPO_ROOT)}")
    if not ok:
        fallos += 1

    print(f"\n  Fase 4: {8 - fallos}/8 checks pasados")
    return fallos


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    """
    Ejecuta las 4 fases de validación.

    Returns:
        0 si todas las fases pasan, 1 en caso contrario.
    """
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   VALIDACIÓN — Ecuación Maestra de la Abundancia Coherente        ║")
    print("║                                                                    ║")
    print("║   A = lim  [ I(t)·f₀ / (|ζ'(1/2)|·eff) ]  =  ∞                 ║")
    print("║        Ψ→1                                                         ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    total_fallos = 0
    total_fallos += fase_1_constantes()
    total_fallos += fase_2_matematica()
    total_fallos += fase_3_limite()
    total_fallos += fase_4_integracion()

    print(f"\n{'═' * 70}")
    if total_fallos == 0:
        print("  ✅ TODAS LAS FASES PASADAS — Abundancia Coherente VERIFICADA ∴𓂀Ω∞³Φ")
        print("  Certificado: ABUNDANCIA-COHERENTE-VERIFIED")
    else:
        print(f"  ❌ {total_fallos} CHECK(S) FALLIDO(S) — revisar implementación")

    print(f"{'═' * 70}\n")
    return 0 if total_fallos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
