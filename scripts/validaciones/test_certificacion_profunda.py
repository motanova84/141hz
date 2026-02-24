#!/usr/bin/env python3
"""
Test de Certificación Profunda — QCAL ∞³
=========================================

Verifica los umbrales de estado de la nueva fórmula Ψ_evento no saturante:

    psi_raw    = sqrt(ratio)
    psi_evento = psi_raw / (1 + psi_raw)   ∈ (0, 1)

Umbrales de estado:
    CRISTALIZADO : psi_evento ≥ 0.909  ⟺  ratio ≥ 100
    COHERENTE    : psi_evento ≥ 0.888  ⟺  ratio ≥ 62.87
    EMERGENTE    : psi_evento ≥ 0.618  ⟺  ratio ≥ 2.618
    RUIDO        : psi_evento  < 0.618

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
import os

# Añadir la raíz del repo al path para que los imports funcionen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from scripts.validaciones.validar_evento_gw1509141 import (
    generar_certificado_validacion,
    SELLO,
)

import tempfile


# ─────────────────────────────────────────────────────────────────────────────
# Función auxiliar
# ─────────────────────────────────────────────────────────────────────────────


def test_caso(nombre, psi_on, psi_off, estado_esperado):
    """
    Construye un reporte mínimo con los valores dados y verifica el estado.

    Returns True si el estado coincide con el esperado.
    """
    reporte = {
        "modulo": SELLO,
        "evento": "TEST",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "resultados_simulacion": {
            "psi_on_mean": psi_on,
            "psi_off_mean": psi_off,
            "separacion_significativa": True,
            "p_value": 1e-5,
            "ratio_contraste": psi_on / max(psi_off, 1e-30),
        },
    }

    with tempfile.TemporaryDirectory() as tmp:
        cert = generar_certificado_validacion(reporte, tmp)

    estado_obtenido = cert["estado"]
    ok = (estado_obtenido == estado_esperado)

    # Calcular psi_evento esperado para el informe
    ratio = psi_on / max(psi_off, 1e-30)
    psi_raw = math.sqrt(ratio)
    psi_ev = psi_raw / (1.0 + psi_raw)

    emoji = "✅" if ok else "❌"
    print(
        f"  {emoji} [{nombre}]  "
        f"ratio={ratio:.1f}  psi_raw={psi_raw:.3f}  "
        f"psi_evento={psi_ev:.4f}  "
        f"estado={estado_obtenido!r}  esperado={estado_esperado!r}"
    )
    return ok


# ─────────────────────────────────────────────────────────────────────────────
# Suite de tests
# ─────────────────────────────────────────────────────────────────────────────


def main():
    tests_exitosos = 0
    tests_totales = 0

    print("=" * 70)
    print("TEST DE CERTIFICACIÓN PROFUNDA — QCAL ∞³ (fórmula no saturante)")
    print("=" * 70)

    # Test 1: CRISTALIZADO (psi_evento ≥ 0.909  ⟺  ratio ≥ 100)
    # ratio = 1.0 / 1e-30 → enorme → psi_raw → ∞ → psi_evento → 1.0 ≥ 0.909
    tests_totales += 1
    if test_caso("CRISTALIZADO - Máxima coherencia",
                 psi_on=1.0, psi_off=1e-30,
                 estado_esperado="CRISTALIZADO"):
        tests_exitosos += 1

    # Test 2: CRISTALIZADO explícito (ratio = 200 ≥ 100)
    # psi_raw = sqrt(200) ≈ 14.14 → psi_evento = 14.14/15.14 ≈ 0.934 ≥ 0.909
    tests_totales += 1
    if test_caso("CRISTALIZADO - ratio=200",
                 psi_on=2.0, psi_off=0.01,
                 estado_esperado="CRISTALIZADO"):
        tests_exitosos += 1

    # Test 3: COHERENTE (0.888 ≤ psi_evento < 0.909  ⟺  62.87 ≤ ratio < 100)
    # ratio = 70 → psi_raw = sqrt(70) ≈ 8.366 → psi_evento = 8.366/9.366 ≈ 0.893
    tests_totales += 1
    if test_caso("COHERENTE - ratio=70",
                 psi_on=0.70, psi_off=0.01,
                 estado_esperado="COHERENTE"):
        tests_exitosos += 1

    # Test 4: EMERGENTE (0.618 ≤ psi_evento < 0.888  ⟺  2.618 ≤ ratio < 62.87)
    # ratio = 20 → psi_raw ≈ 4.472 → psi_evento ≈ 0.817
    tests_totales += 1
    if test_caso("EMERGENTE - ratio=20",
                 psi_on=0.20, psi_off=0.01,
                 estado_esperado="EMERGENTE"):
        tests_exitosos += 1

    # Test 5: Borde COHERENTE inferior (psi_evento ≈ 0.888  ⟺  ratio ≈ 62.87)
    # psi_raw_borde = 0.888 / (1 - 0.888) ≈ 7.929
    # Se suma 0.01 al psi_raw para estar ligeramente por encima del umbral
    # exacto y evitar fallos por error de redondeo en coma flotante.
    tests_totales += 1
    psi_raw_borde = 0.888 / (1.0 - 0.888)   # ≈ 7.929
    ratio_borde = (psi_raw_borde + 0.01) ** 2  # ligeramente por encima ≈ 63.0
    if test_caso("COHERENTE - Borde inferior",
                 psi_on=ratio_borde, psi_off=1.0,
                 estado_esperado="COHERENTE"):
        tests_exitosos += 1

    # Test 6: RUIDO (psi_evento < 0.618  ⟺  ratio < 2.618)
    # ratio = 1.5 → psi_raw ≈ 1.225 → psi_evento ≈ 0.551 < 0.618
    tests_totales += 1
    if test_caso("RUIDO - ratio=1.5",
                 psi_on=0.15, psi_off=0.10,
                 estado_esperado="RUIDO"):
        tests_exitosos += 1

    # ── Resumen ──────────────────────────────────────────────────────────────
    print("=" * 70)
    print(f"Resultado: {tests_exitosos}/{tests_totales} tests exitosos")

    if tests_exitosos == tests_totales:
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print(f"❌ {tests_totales - tests_exitosos} test(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
