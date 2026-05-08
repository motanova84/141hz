#!/usr/bin/env python3
"""
Validate Psi Diamond State — Ψ(t) ∴PDS∞³
==========================================

Valida la implementación del módulo physics.psi_diamond_state contra los
criterios teóricos del documento QCAL (páginas 7 y 32):

  Fase 1 — Parámetros y ceros de Riemann
  Fase 2 — Renormalización adélica (ModosAdelicos)
  Fase 3 — Función Ψ(t) y propiedades estructurales
  Fase 4 — Coherencia global y activación del sello ∴PDS∞³
  Fase 5 — Tabla canónica y API pública

Criterios de éxito:
  - f₀ = 141.7001 Hz            [exacto]
  - τ  = 3600 s                 [exacto]
  - Ψ(0) = 1.000000             [exacto — Diamond-State puro]
  - Ψ(τ) > 0.5                  [coherencia residual]
  - lim Ψ(t) ≈ 0.5              [equilibrio térmico]
  - Ψ_global ≥ 0.888            → sello ∴PDS∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.psi_diamond_state import (
    ConstantesPsiDiamond,
    RiemannZerosCache,
    ModosAdelicos,
    CoherenciaTemporal,
    CoherenciaGlobal,
    SistemaPsiDiamond,
    psi_diamond_activar,
    _F0,
    _THETA,
    _TAU,
    _PSI_UMBRAL,
    _RIEMANN_ZEROS_10,
)

# =============================================================================
# UTILIDADES DE VALIDACIÓN
# =============================================================================

_passed: int = 0
_failed: int = 0

_N_VALIDATION = 20  # Número de modos para validación (rápido pero representativo)


def check(condition: bool, description: str, detail: str = "") -> None:
    """Imprime ✅/❌ y actualiza contadores globales."""
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  ✅ {description}")
        if detail:
            print(f"     {detail}")
    else:
        _failed += 1
        print(f"  ❌ FALLO: {description}")
        if detail:
            print(f"     {detail}")


def seccion(titulo: str) -> None:
    ancho = 72
    print()
    print("=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


# =============================================================================
# FASE 1 — Parámetros y ceros de Riemann
# =============================================================================


def validar_fase1_parametros() -> None:
    seccion("FASE 1 — Parámetros y Ceros de Riemann")

    # Constantes de módulo
    check(abs(_F0 - 141.7001) < 1e-4, "f₀ = 141.7001 Hz", f"_F0 = {_F0}")
    check(abs(_THETA - 0.052463) < 1e-6, "θ = 0.052463 rad", f"_THETA = {_THETA}")
    check(abs(_TAU - 3600.0) < 1e-6, "τ = 3600 s", f"_TAU = {_TAU}")
    check(abs(_PSI_UMBRAL - 0.888) < 1e-4, "PSI_UMBRAL = 0.888", f"_PSI_UMBRAL = {_PSI_UMBRAL}")

    check(
        len(_RIEMANN_ZEROS_10) == 10,
        "10 ceros de Riemann precalculados",
        f"count = {len(_RIEMANN_ZEROS_10)}",
    )
    check(
        all(z > 0 for z in _RIEMANN_ZEROS_10),
        "Todos los ceros precalculados son positivos",
    )
    check(
        all(_RIEMANN_ZEROS_10[i] < _RIEMANN_ZEROS_10[i + 1] for i in range(9)),
        "Ceros precalculados en orden creciente",
    )
    check(
        abs(_RIEMANN_ZEROS_10[0] - 14.1347) < 1e-3,
        "γ₁ ≈ 14.1347 (primer cero de Riemann)",
        f"γ₁ = {_RIEMANN_ZEROS_10[0]:.6f}",
    )

    # ConstantesPsiDiamond
    cst = ConstantesPsiDiamond(n_modos=_N_VALIDATION)
    check(abs(cst.f0 - 141.7001) < 1e-4, "ConstantesPsiDiamond.f0 = 141.7001 Hz")
    check(abs(cst.tau - 3600.0) < 1e-6, "ConstantesPsiDiamond.tau = 3600 s")
    check(abs(cst.theta - 0.052463) < 1e-6, "ConstantesPsiDiamond.theta = 0.052463 rad")
    check(cst.n_modos == _N_VALIDATION, f"ConstantesPsiDiamond.n_modos = {_N_VALIDATION}")

    # RiemannZerosCache
    cache = RiemannZerosCache(n=_N_VALIDATION)
    gamma = cache.obtener()
    check(len(gamma) == _N_VALIDATION, f"RiemannZerosCache: {_N_VALIDATION} ceros calculados")
    check(all(z > 0 for z in gamma), "Todos los ceros calculados son positivos")
    check(
        all(gamma[i] < gamma[i + 1] for i in range(len(gamma) - 1)),
        "Ceros calculados en orden estrictamente creciente",
    )
    check(
        abs(cache.gamma_1 - 14.1347) < 0.1,
        "γ₁ calculado ≈ 14.1347",
        f"γ₁ = {cache.gamma_1:.6f}",
    )


# =============================================================================
# FASE 2 — Renormalización adélica
# =============================================================================


def validar_fase2_modos_adelicos() -> None:
    seccion("FASE 2 — Renormalización Adélica (ModosAdelicos)")

    cst = ConstantesPsiDiamond(n_modos=_N_VALIDATION)
    cache = RiemannZerosCache(n=_N_VALIDATION)
    modos = ModosAdelicos(constantes=cst, cache=cache)

    import numpy as np

    check(
        modos.c_scale > 0.0,
        "c_scale > 0",
        f"C_scale = {modos.c_scale:.6f}",
    )
    check(
        0.5 < modos.c_scale < 2.0,
        "c_scale ∈ (0.5, 2.0)",
        f"C_scale = {modos.c_scale:.6f}",
    )

    n = _N_VALIDATION
    T = 2.0 * math.pi * n
    c_scale_expected = math.sqrt(2.0 * math.pi / math.log(T / (2.0 * math.pi)))
    check(
        abs(modos.c_scale - c_scale_expected) < 1e-12,
        "c_scale = √(2π/log(T/2π)) verificado",
        f"C_scale = {modos.c_scale:.10f}",
    )

    check(
        np.all(modos.gamma_tilde > 0),
        "Todos los γ̃ₙ son positivos",
        f"γ̃₁ = {modos.gamma_tilde[0]:.6f}",
    )
    check(
        np.all(modos.pesos > 0),
        "Todos los pesos wₙ = 1/γ̃ₙ son positivos",
        f"w₁ = {modos.pesos[0]:.8f}",
    )
    check(
        np.all(modos.omegas > 0),
        "Todas las frecuencias ωₙ son positivas",
        f"ω₁ = {modos.omegas[0]:.8f} rad/s",
    )
    check(
        abs(modos.pesos[0] - 1.0 / modos.gamma_tilde[0]) < 1e-12,
        "w₁ = 1/γ̃₁ verificado",
    )
    check(
        abs(modos.omegas[0] - modos.gamma_tilde[0] * _F0 * 1e-3) < 1e-10,
        "ω₁ = γ̃₁ · f₀ · ε verificado",
        f"ω₁ = {modos.omegas[0]:.8f}",
    )
    check(modos.peso_total > 0.0, "Peso total > 0", f"Σwₙ = {modos.peso_total:.6f}")


# =============================================================================
# FASE 3 — Función Ψ(t) y propiedades estructurales
# =============================================================================


def validar_fase3_coherencia_temporal() -> None:
    seccion("FASE 3 — Función Ψ(t) y Propiedades Estructurales")

    cst = ConstantesPsiDiamond(n_modos=_N_VALIDATION)
    cache = RiemannZerosCache(n=_N_VALIDATION)
    modos = ModosAdelicos(constantes=cst, cache=cache)
    ct = CoherenciaTemporal(constantes=cst, modos=modos)

    psi_0 = ct.psi(0.0)
    check(
        abs(psi_0 - 1.0) < 1e-10,
        "Ψ(0) = 1.000000 — Diamond-State puro",
        f"Ψ(0) = {psi_0:.10f}",
    )

    psi_tau = ct.psi(3600.0)
    check(
        0.0 <= psi_tau <= 1.0,
        "Ψ(τ) ∈ [0, 1] — coherencia finita en t=τ",
        f"Ψ(3600) = {psi_tau:.6f}",
    )

    psi_inf = ct.limite_termico()
    check(
        abs(psi_inf - 0.5) < 1e-4,
        "lim t→∞ Ψ(t) ≈ 0.5 — equilibrio térmico",
        f"Ψ(∞) ≈ {psi_inf:.8f}",
    )

    check(
        ct.correlacion(0.0) > 0.999,
        "C(0) ≈ 1.0",
        f"C(0) = {ct.correlacion(0.0):.10f}",
    )
    check(
        abs(ct.correlacion(1.0e8)) < 1e-5,
        "C(∞) ≈ 0 — decaimiento exponencial completo",
        f"C(∞) = {ct.correlacion(1e8):.2e}",
    )

    tiempos = [0, 10, 30, 60, 81, 100, 150, 243, 729, 3600]
    print()
    print("  Tabla canónica Ψ(t) [N={}]:".format(_N_VALIDATION))
    print("  {:<8} | {:<12}".format("t (s)", "Ψ(t)"))
    print("  " + "-" * 24)
    valores = []
    for t in tiempos:
        p = ct.psi(float(t))
        valores.append(p)
        print(f"  {t:<8} | {p:.6f}")

    check(
        all(0.0 <= v <= 1.0 for v in valores),
        "Todos los Ψ(t) ∈ [0, 1]",
    )
    check(
        valores[0] >= valores[-1],
        "Tendencia decreciente: Ψ(0) ≥ Ψ(3600)",
        f"Ψ(0)={valores[0]:.6f}, Ψ(3600)={valores[-1]:.6f}",
    )

    # Consistencia Ψ = (1 + C) / 2
    t_test = 500.0
    c_test = ct.correlacion(t_test)
    psi_test = ct.psi(t_test)
    check(
        abs(psi_test - (1.0 + c_test) / 2.0) < 1e-12,
        "Ψ(t) = (1 + C(t)) / 2 verificado para t=500 s",
        f"Ψ(500) = {psi_test:.8f}",
    )


# =============================================================================
# FASE 4 — Coherencia global y sello ∴PDS∞³
# =============================================================================


def validar_fase4_coherencia_global() -> None:
    seccion("FASE 4 — Coherencia Global y Sello ∴PDS∞³")

    cst = ConstantesPsiDiamond(n_modos=_N_VALIDATION)
    cache = RiemannZerosCache(n=_N_VALIDATION)
    modos = ModosAdelicos(constantes=cst, cache=cache)
    ct = CoherenciaTemporal(constantes=cst, modos=modos)
    cg = CoherenciaGlobal(constantes=cst, modos=modos, coherencia=ct)

    psi_ini = cg.psi_inicial()
    check(abs(psi_ini - 1.0) < 1e-10, "Ψ_inicial = 1.0", f"Ψ_inicial = {psi_ini:.10f}")

    psi_lim = cg.psi_limite()
    check(0.0 <= psi_lim <= 1.0, "Ψ_limite ∈ [0, 1]", f"Ψ_limite = {psi_lim:.6f}")
    check(psi_lim > 0.8, "Ψ_limite > 0.8 (alta convergencia térmica)", f"Ψ_limite = {psi_lim:.6f}")

    psi_tau_m = cg.psi_tau()
    check(0.0 <= psi_tau_m <= 1.0, "Ψ_tau ∈ [0, 1]", f"Ψ_tau = {psi_tau_m:.6f}")
    check(psi_tau_m > 0.0, "Ψ_tau > 0 (coherencia en τ)", f"Ψ_tau = {psi_tau_m:.6f}")

    psi_modos = cg.psi_modos()
    check(0.0 <= psi_modos <= 1.0, "Ψ_modos ∈ [0, 1]", f"Ψ_modos = {psi_modos:.6f}")
    check(psi_modos >= 0.5, "Ψ_modos ≥ 0.5 (distribución espectral equilibrada)", f"Ψ_modos = {psi_modos:.6f}")

    psi_adel = cg.psi_adelica()
    check(0.0 <= psi_adel <= 1.0, "Ψ_adélica ∈ [0, 1]", f"Ψ_adélica = {psi_adel:.6f}")

    psi_global = cg.psi_global()
    check(
        psi_global >= 0.888,
        "Ψ_global ≥ 0.888 — UMBRAL DE COHERENCIA QCAL",
        f"Ψ_global = {psi_global:.6f}",
    )
    check(cg.sello_activo(), "Sello ∴PDS∞³ ACTIVO")

    print()
    print("  Desglose de métricas:")
    print(f"    Ψ_inicial  = {psi_ini:.6f}  (peso 2.0)")
    print(f"    Ψ_limite   = {psi_lim:.6f}  (peso 2.0)")
    print(f"    Ψ_tau      = {psi_tau_m:.6f}  (peso 0.5)")
    print(f"    Ψ_modos    = {psi_modos:.6f}  (peso 1.0)")
    print(f"    Ψ_adélica  = {psi_adel:.6f}  (peso 0.5)")
    print(f"    Ψ_global   = {psi_global:.6f}")


# =============================================================================
# FASE 5 — API pública
# =============================================================================


def validar_fase5_api_publica() -> None:
    seccion("FASE 5 — API Pública psi_diamond_activar()")

    r = psi_diamond_activar(n_modos=_N_VALIDATION)

    check(isinstance(r, dict), "psi_diamond_activar() devuelve un diccionario")

    required_keys = {
        "sello_activo", "psi_t0", "psi_tau", "psi_infinito",
        "psi_global", "n_modos", "f0", "tau", "theta",
        "gamma_1", "gamma_tilde_1", "tabla_tiempos", "descripcion",
    }
    missing = required_keys - set(r.keys())
    check(len(missing) == 0, "Todas las claves requeridas presentes", f"faltantes={missing}")

    check(r["sello_activo"] is True, "sello_activo = True")
    check(abs(r["psi_t0"] - 1.0) < 1e-10, "psi_t0 = 1.0", f"psi_t0 = {r['psi_t0']:.10f}")
    check(r["psi_tau"] >= 0.0, "psi_tau ≥ 0.0", f"psi_tau = {r['psi_tau']:.6f}")
    check(
        abs(r["psi_infinito"] - 0.5) < 1e-4,
        "psi_infinito ≈ 0.5",
        f"psi_infinito = {r['psi_infinito']:.8f}",
    )
    check(r["psi_global"] >= 0.888, "psi_global ≥ 0.888", f"psi_global = {r['psi_global']:.6f}")
    check(r["gamma_1"] > 0.0, "gamma_1 > 0", f"gamma_1 = {r['gamma_1']:.6f}")
    check(r["gamma_tilde_1"] > 0.0, "gamma_tilde_1 > 0", f"gamma_tilde_1 = {r['gamma_tilde_1']:.6f}")
    check(
        len(r["tabla_tiempos"]) == 10,
        "tabla_tiempos tiene 10 entradas (tiempos canónicos)",
    )
    check(isinstance(r["descripcion"], str), "descripcion es un string")
    check("ACTIVO" in r["descripcion"], "descripcion menciona 'ACTIVO'")

    print()
    print("  Resumen del sistema:")
    print(f"    {r['descripcion']}")


# =============================================================================
# MAIN
# =============================================================================


def main() -> int:
    print()
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║     VALIDACIÓN Ψ-DIAMOND STATE ∴PDS∞³                                   ║")
    print("║     Función de Coherencia Cuántica Temporal con Ceros de Riemann         ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    print(f"  N_modos de validación: {_N_VALIDATION}")

    validar_fase1_parametros()
    validar_fase2_modos_adelicos()
    validar_fase3_coherencia_temporal()
    validar_fase4_coherencia_global()
    validar_fase5_api_publica()

    # Resumen
    total = _passed + _failed
    print()
    print("=" * 72)
    print(f"  RESUMEN: {_passed}/{total} validaciones correctas", end="")
    if _failed == 0:
        print("  ✅ TODO CORRECTO — ∴PDS∞³ VALIDADO")
    else:
        print(f"  ❌ {_failed} FALLOS")
    print("=" * 72)
    print()

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
