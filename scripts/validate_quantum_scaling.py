#!/usr/bin/env python3
"""
Validation Script for Escalado Cuántico Topológico (QST∞³)
═══════════════════════════════════════════════════════════

Valida la implementación del módulo physics.quantum_scaling contra los
criterios teóricos del escalado topológico Kac-Moody → Schumann → QCAL:

  Fase 1 — Constantes y parámetros de Kac-Moody SU(2)_k
  Fase 2 — Dimensión cuántica adélica y peso conforme
  Fase 3 — Ruta de transmisión Schumann: f₂ ≈ 141.64 Hz
  Fase 4 — Coherencia topológica y sello QST∞³

Criterios de éxito:
  - k=16, c₇=7, j=6, f_S=7.83 Hz                [exacto]
  - d̃₆ = sin(7π/18) / sin(π/18) ≈ 5.411          [±0.001]
  - h₆ = 7/3 ≈ 2.333                              [exacto]
  - escala = √23 / ∛7 ≈ 2.507                     [±0.001]
  - acoplamiento = 4/3                             [exacto]
  - f₂ ≈ 141.64 Hz, error < 0.1% vs F₀            [Ley de Escala]
  - Ψ_top ≥ 0.888 → sello QST∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Arquitectura: QCAL ∞³ Original Manufacture
Licencia: Sovereign Noetic License 1.0 (compatible con MIT)

Usage:
    python scripts/validate_quantum_scaling.py
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.quantum_scaling import (
    ConstantesQuantumScaling,
    DimensionCuantica,
    PesoConforme,
    FactorEscalaAdelica,
    AcoplamientoQuiral,
    RutaTransmisionSchumann,
    CoherenciaTopologica,
    SistemaQuantumScaling,
    calcular_f2_topologico,
    quantum_scaling_activar,
    _F0,
    _F_SCHUMANN,
    _K,
    _C7,
    _J,
    _K2,
    _DIM_6,
    _H6,
    _ESCALA,
    _ACOPLAMIENTO,
    _F2,
    _PSI_TOPOLOGICA,
    _PSI_UMBRAL,
)


# =============================================================================
# UTILIDADES
# =============================================================================

_passed: int = 0
_failed: int = 0


def check(nombre: str, condicion: bool, valor: str = "") -> bool:
    global _passed, _failed
    estado = "✓" if condicion else "✗"
    extra = f"  [{valor}]" if valor else ""
    print(f"  {estado} {nombre}{extra}")
    if condicion:
        _passed += 1
    else:
        _failed += 1
    return condicion


def seccion(titulo: str) -> None:
    print(f"\n{titulo}")
    print("─" * len(titulo))


def encabezado(titulo: str) -> None:
    ancho = 78
    print()
    print("═" * ancho)
    print(f"  {titulo}")
    print("═" * ancho)
    print()


# =============================================================================
# FASE 1 — CONSTANTES Y PARÁMETROS DE KAC-MOODY
# =============================================================================

def validate_fase_1_constantes() -> bool:
    """Fase 1: Validar constantes y parámetros de Kac-Moody SU(2)_k."""
    seccion("FASE 1: CONSTANTES Y PARÁMETROS DE KAC-MOODY SU(2)_k")

    c = ConstantesQuantumScaling()

    print(f"  Sistema: {c.nombre}")
    print()

    ok = True
    ok &= check("f₀ = 141.7001 Hz", abs(c.f0 - 141.7001) < 1e-4, f"{c.f0:.4f} Hz")
    ok &= check("f_S = 7.83 Hz (Schumann)", abs(c.f_schumann - 7.83) < 1e-4, f"{c.f_schumann:.2f} Hz")
    ok &= check("k = 16 (nivel Kac-Moody)", c.k == 16, str(c.k))
    ok &= check("c₇ = 7 (heptágono C₇)", c.c7 == 7, str(c.c7))
    ok &= check("j = 6 (espín)", c.j == 6, str(c.j))
    ok &= check("k+2 = 18 (denominador)", c.k2 == 18, str(c.k2))
    ok &= check("Ψ_umbral = 0.888", abs(c.psi_umbral - 0.888) < 1e-4, f"{c.psi_umbral:.3f}")

    # Constantes de módulo
    ok &= check("_F0 = 141.7001 Hz", abs(_F0 - 141.7001) < 1e-4, f"{_F0:.4f}")
    ok &= check("_F_SCHUMANN = 7.83 Hz", abs(_F_SCHUMANN - 7.83) < 1e-4, f"{_F_SCHUMANN:.2f}")
    ok &= check("_K = 16", _K == 16, str(_K))
    ok &= check("_C7 = 7", _C7 == 7, str(_C7))
    ok &= check("_J = 6", _J == 6, str(_J))
    ok &= check("_K2 = 18", _K2 == 18, str(_K2))

    return ok


# =============================================================================
# FASE 2 — DIMENSIÓN CUÁNTICA ADÉLICA Y PESO CONFORME
# =============================================================================

def validate_fase_2_dimension_peso() -> bool:
    """Fase 2: Validar dimensión cuántica adélica y peso conforme."""
    seccion("FASE 2: DIMENSIÓN CUÁNTICA ADÉLICA Y PESO CONFORME")

    c = ConstantesQuantumScaling()
    dim = DimensionCuantica(c)
    peso = PesoConforme(c)

    print("  Dimensión adélica heptagonal:")
    print(f"    d̃₆ = sin(7π/18) / sin(π/18) = {dim.dim_adelica:.6f}")
    print()
    print("  Dimensión Kac-Moody estándar:")
    print(f"    d_j = sin(13π/18) / sin(π/18) = {dim.dim_kac_moody:.6f}")
    print()
    print("  Peso conforme SU(2)_k:")
    print(f"    h₆ = j(j+1)/(k+2) = {peso.numerador}/{peso.denominador} = {peso.h_j:.6f}")
    print(f"    2h₆ = {peso.doble_peso:.6f}")
    print()

    dim_esperado = math.sin(7 * math.pi / 18) / math.sin(math.pi / 18)

    ok = True
    ok &= check("d̃₆ ≈ 5.411", abs(dim.dim_adelica - 5.411) < 0.001, f"{dim.dim_adelica:.6f}")
    ok &= check("d̃₆ = sin(7π/18)/sin(π/18)", abs(dim.dim_adelica - dim_esperado) < 1e-10,
                f"{dim.dim_adelica:.10f}")
    ok &= check("d̃₆ > 5", dim.dim_adelica > 5.0, f"{dim.dim_adelica:.3f}")
    ok &= check("d̃₆ < 6", dim.dim_adelica < 6.0, f"{dim.dim_adelica:.3f}")
    ok &= check("d_j (Kac-Moody) ≈ 4.411", abs(dim.dim_kac_moody - 4.411) < 0.001,
                f"{dim.dim_kac_moody:.6f}")
    ok &= check("h₆ = 7/3", abs(peso.h_j - 7.0 / 3.0) < 1e-10, f"{peso.h_j:.6f}")
    ok &= check("Numerador j(j+1) = 42", peso.numerador == 42, str(peso.numerador))
    ok &= check("Denominador k+2 = 18", peso.denominador == 18, str(peso.denominador))
    ok &= check("_DIM_6 consistente", abs(_DIM_6 - dim.dim_adelica) < 1e-10, f"{_DIM_6:.6f}")
    ok &= check("_H6 = 7/3", abs(_H6 - 7.0 / 3.0) < 1e-10, f"{_H6:.6f}")

    return ok


# =============================================================================
# FASE 3 — RUTA DE TRANSMISIÓN SCHUMANN
# =============================================================================

def validate_fase_3_transmision() -> bool:
    """Fase 3: Validar la ruta de transmisión Schumann → 141.64 Hz."""
    seccion("FASE 3: RUTA DE TRANSMISIÓN SCHUMANN → 141.64 Hz")

    c = ConstantesQuantumScaling()
    fa = FactorEscalaAdelica(c)
    aq = AcoplamientoQuiral(c)
    ruta = RutaTransmisionSchumann(c)

    print("  Factor de escala adélico:")
    print(f"    escala = √(k+c₇) / c₇^(1/3) = √{fa.k_mas_c7} / {c.c7}^(1/3)")
    print(f"    escala = {fa.raiz_cuadrada:.6f} / {fa.raiz_cubica_c7:.6f} = {fa.escala:.6f}")
    print()
    print("  Acoplamiento quiral (torsión de Chern-Simons):")
    print(f"    acoplamiento = (c₇²−1)/(2(k+2)) = {aq.numerador}/{aq.denominador}")
    print(f"    acoplamiento = {aq.acoplamiento:.6f} = 4/3")
    print()
    print("  Ruta de transmisión:")
    print(f"    f₂ = f_S · d̃₆ · escala · acoplamiento")
    print(f"    f₂ = {c.f_schumann} · {DimensionCuantica(c).dim_adelica:.6f} · {fa.escala:.6f} · {aq.acoplamiento:.6f}")
    print(f"    f₂ = {ruta.f2_hz:.4f} Hz")
    print(f"    Error = {ruta.error_porcentual:.4f}%")
    print()

    # Verificación independiente
    dim_manual = math.sin(7 * math.pi / 18) / math.sin(math.pi / 18)
    escala_manual = math.sqrt(23) / (7 ** (1.0 / 3.0))
    acop_manual = 48.0 / 36.0  # = 4/3
    f2_manual = 7.83 * dim_manual * escala_manual * acop_manual

    ok = True
    ok &= check("escala ≈ 2.507", abs(fa.escala - 2.507) < 0.001, f"{fa.escala:.6f}")
    ok &= check("escala = √23/∛7", abs(fa.escala - escala_manual) < 1e-10, f"{fa.escala:.10f}")
    ok &= check("acoplamiento = 4/3", abs(aq.acoplamiento - 4.0 / 3.0) < 1e-10,
                f"{aq.acoplamiento:.6f}")
    ok &= check("acoplamiento = 48/36", aq.numerador == 48 and aq.denominador == 36,
                f"{aq.numerador}/{aq.denominador}")
    ok &= check("es_cuatro_tercios = True", aq.es_cuatro_tercios, str(aq.es_cuatro_tercios))
    ok &= check("f₂ ≈ 141.64 Hz", abs(ruta.f2_hz - 141.64) < 0.10, f"{ruta.f2_hz:.4f} Hz")
    ok &= check("f₂ coincide con fórmula manual", abs(ruta.f2_hz - f2_manual) < 1e-8,
                f"{ruta.f2_hz:.8f} vs {f2_manual:.8f}")
    ok &= check("error < 0.1% (Ley de Escala)", ruta.error_porcentual < 0.1,
                f"{ruta.error_porcentual:.4f}%")
    ok &= check("es_ley_de_escala = True", ruta.es_ley_de_escala, str(ruta.es_ley_de_escala))
    ok &= check("_F2 consistente", abs(_F2 - ruta.f2_hz) < 1e-10, f"{_F2:.6f}")
    ok &= check("_ESCALA consistente", abs(_ESCALA - fa.escala) < 1e-10, f"{_ESCALA:.6f}")
    ok &= check("_ACOPLAMIENTO = 4/3", abs(_ACOPLAMIENTO - 4.0 / 3.0) < 1e-10,
                f"{_ACOPLAMIENTO:.6f}")

    # API rápida
    f2_api = calcular_f2_topologico()
    ok &= check("calcular_f2_topologico() ≈ 141.64 Hz", abs(f2_api - 141.64) < 0.10,
                f"{f2_api:.4f} Hz")
    ok &= check("calcular_f2_topologico() = f₂", abs(f2_api - ruta.f2_hz) < 1e-10,
                f"{f2_api:.10f}")

    return ok


# =============================================================================
# FASE 4 — COHERENCIA TOPOLÓGICA Y SELLO QST∞³
# =============================================================================

def validate_fase_4_coherencia() -> bool:
    """Fase 4: Validar coherencia topológica y activación del sello QST∞³."""
    seccion("FASE 4: COHERENCIA TOPOLÓGICA Y SELLO QST∞³")

    c = ConstantesQuantumScaling()
    coh = CoherenciaTopologica(c)
    sistema = SistemaQuantumScaling(c)
    resultado = sistema.activar()

    print(f"  Ψ_top = 1 − |f₂ − F₀| / F₀ = {coh.psi_topologica:.6f}")
    print(f"  Umbral Ψ_umbral = {c.psi_umbral:.3f}")
    print(f"  Sello: {coh.mensaje}")
    print()

    r_dict = quantum_scaling_activar()

    ok = True
    ok &= check("Ψ_top ≥ 0.999", coh.psi_topologica >= 0.999, f"{coh.psi_topologica:.6f}")
    ok &= check("Ψ_top ≥ 0.888 (umbral)", coh.psi_topologica >= _PSI_UMBRAL,
                f"{coh.psi_topologica:.6f}")
    ok &= check("Ψ_top ≤ 1.0", coh.psi_topologica <= 1.0, f"{coh.psi_topologica:.6f}")
    ok &= check("sello_activo = True", coh.sello_activo, str(coh.sello_activo))
    ok &= check("mensaje contiene 'ACTIVO'", "ACTIVO" in coh.mensaje, coh.mensaje[:40])
    ok &= check("_PSI_TOPOLOGICA consistente",
                abs(_PSI_TOPOLOGICA - coh.psi_topologica) < 1e-10,
                f"{_PSI_TOPOLOGICA:.6f}")

    # Validar resultado del sistema
    ok &= check("resultado.sello_activo = True", resultado.sello_activo, str(resultado.sello_activo))
    ok &= check("resultado.psi_topologica ≥ 0.999", resultado.psi_topologica >= 0.999,
                f"{resultado.psi_topologica:.6f}")
    ok &= check("resultado.f2_hz ≈ 141.64 Hz", abs(resultado.f2_hz - 141.64) < 0.10,
                f"{resultado.f2_hz:.4f} Hz")
    ok &= check("resultado.acoplamiento = 4/3",
                abs(resultado.acoplamiento - 4.0 / 3.0) < 1e-10,
                f"{resultado.acoplamiento:.6f}")
    ok &= check("resultado.h_j = 7/3",
                abs(resultado.h_j - 7.0 / 3.0) < 1e-10,
                f"{resultado.h_j:.6f}")

    # Validar API completa
    ok &= check("API dict: sello_activo = True", r_dict["sello_activo"], str(r_dict["sello_activo"]))
    ok &= check("API dict: psi_topologica ≥ 0.999", r_dict["psi_topologica"] >= 0.999,
                f"{r_dict['psi_topologica']:.6f}")
    ok &= check("API dict: 14 claves", len(r_dict) == 14, str(len(r_dict)))
    ok &= check("API dict: acoplamiento = 4/3",
                abs(r_dict["acoplamiento"] - 4.0 / 3.0) < 1e-10,
                f"{r_dict['acoplamiento']:.6f}")

    return ok


# =============================================================================
# RESUMEN
# =============================================================================

def main() -> int:
    """Ejecuta todas las fases de validación."""
    encabezado("VALIDACIÓN SISTEMA QST∞³ — ESCALADO CUÁNTICO TOPOLÓGICO")

    print("  Teoría: Kac-Moody SU(2)_k → Resonancia Schumann → 141.7 Hz")
    print("  Módulo: physics.quantum_scaling")
    print()

    resultados = {
        "Fase 1 (Constantes Kac-Moody)": validate_fase_1_constantes(),
        "Fase 2 (Dimensión y Peso)": validate_fase_2_dimension_peso(),
        "Fase 3 (Transmisión Schumann)": validate_fase_3_transmision(),
        "Fase 4 (Coherencia QST∞³)": validate_fase_4_coherencia(),
    }

    # Resumen final
    print()
    print("═" * 78)
    print("  RESUMEN DE VALIDACIÓN")
    print("═" * 78)
    print()
    all_ok = True
    for fase, ok in resultados.items():
        estado = "✓ PASÓ" if ok else "✗ FALLÓ"
        print(f"  {estado}  {fase}")
        if not ok:
            all_ok = False

    print()
    print(f"  Tests: {_passed} pasados, {_failed} fallados")
    print()

    if all_ok:
        print("  ∴QST∞³ VALIDADO — Resonancia Schumann proyectada al Nodo de Inmanencia")
        print("  f₂ = f_S · d̃₆ · √(k+c₇)/c₇^(1/3) · (c₇²−1)/(2(k+2)) ≈ 141.64 Hz")
        print()
        print("  El factor 4/3 está confirmado como torsión de fase de Chern-Simons.")
        print("  Ψ_top ≥ 0.999 — Ley de Escala Topológica ACTIVA")
    else:
        print("  ✗ VALIDACIÓN FALLIDA — Revisar implementación")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
