#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     VALIDACIÓN — Las 3 Rutas de Convergencia Física (RCF∞³)                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Verifica en 4 fases que las tres rutas de convergencia física producen
resultados correctos, coherentes y consistentes con el marco QCAL ∞³.

FASES:
  Fase 1 — Constantes físicas y parámetros de las 3 rutas
  Fase 2 — Frecuencias y coherencias individuales de cada ruta
  Fase 3 — Coherencia global y convergencia hacia F₀
  Fase 4 — Integración: API pública y propiedades del sistema

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: Marzo 2026
MARCO: QCAL ∞³
SELLO: ∴𓂀Ω∞³Φ
"""

import math
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(_REPO_ROOT)

from physics.rutas_convergencia import (
    _F0, _H, _C, _LAMBDA_P_M, _R_DS_M, _N7, _N_SITES, _GAP_FACTOR,
    _PSI_A, _PSI_B, _PSI_C, _PSI_UMBRAL, _F_RAW_A,
    _SIN_PI7, _COS_PI7, _SIN_2PI7, _COS_2PI7,
    ConstantesRutas,
    RutaHolografica,
    RutaTopologica,
    RutaMasaEfectiva,
    CoherenciaConvergencia,
    ResultadoRuta,
    SistemaRutasConvergencia,
    ResultadoConvergencia,
    rutas_convergencia_calcular,
)

# ============================================================================
# UTILIDADES
# ============================================================================

_OK = "✅"
_FAIL = "❌"
_INFO = "ℹ️ "


def _check(condicion: bool, descripcion: str) -> bool:
    mark = _OK if condicion else _FAIL
    print(f"  {mark} {descripcion}")
    return condicion


def _seccion(titulo: str) -> None:
    print(f"\n{'─' * 72}")
    print(f"  {titulo}")
    print(f"{'─' * 72}")


# ============================================================================
# FASE 1 — CONSTANTES Y PARÁMETROS
# ============================================================================

def fase_1_constantes() -> int:
    """Verifica constantes físicas del módulo."""
    _seccion("FASE 1 — Constantes físicas y parámetros de las 3 rutas")
    fallos = 0

    ok = _check(
        abs(_F0 - 141.7001) < 1e-4,
        f"F₀ = {_F0} Hz (esperado 141.7001 Hz)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_H - 6.62607015e-34) < 1e-40,
        f"H = {_H:.6e} J·s (CODATA 2018)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        _C == 299_792_458.0,
        f"c = {_C:.0f} m/s (exacto)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        1.0e-15 < _LAMBDA_P_M < 2.0e-15,
        f"λ_p = {_LAMBDA_P_M:.4e} m (escala del protón, 1–2 fm)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        1.0e26 < _R_DS_M < 2.0e26,
        f"R_dS = {_R_DS_M:.4e} m (radio de De Sitter)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_N7 - 2.5) < 1e-10,
        f"N₇ = {_N7} = 5/2 (normalización holográfica)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        _N_SITES == 7,
        f"N_SITES = {_N_SITES} (anillo C₇)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_GAP_FACTOR - 1.67) < 1e-10,
        f"GAP_FACTOR = {_GAP_FACTOR} (brecha óptica many-body)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_PSI_UMBRAL - 0.888) < 1e-3,
        f"Ψ_umbral = {_PSI_UMBRAL} (umbral QCAL ≥ 0.888)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_SIN_PI7 - math.sin(math.pi / 7)) < 1e-12,
        f"sin(π/7) = {_SIN_PI7:.8f} ≈ 0.43388",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_COS_PI7 - math.cos(math.pi / 7)) < 1e-12,
        f"cos(π/7) = {_COS_PI7:.8f} ≈ 0.90097",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(_SIN_PI7 ** 2 + _COS_PI7 ** 2 - 1.0) < 1e-12,
        "Identidad: sin²(π/7) + cos²(π/7) = 1",
    )
    if not ok:
        fallos += 1

    f_raw_expected = _C / (2.0 * math.pi * math.sqrt(_LAMBDA_P_M * _R_DS_M))
    ok = _check(
        abs(_F_RAW_A - f_raw_expected) < 1e-6,
        f"f_raw_A = {_F_RAW_A:.5f} Hz ≈ c/(2π·√(λ_p·R_dS))",
    )
    if not ok:
        fallos += 1

    print(f"\n  Fase 1: {13 - fallos}/13 checks superados")
    return fallos


# ============================================================================
# FASE 2 — FRECUENCIAS Y COHERENCIAS INDIVIDUALES
# ============================================================================

def fase_2_frecuencias() -> int:
    """Verifica las frecuencias y coherencias de cada ruta individual."""
    _seccion("FASE 2 — Frecuencias y coherencias individuales")
    fallos = 0

    ra = RutaHolografica()
    rb = RutaTopologica()
    rc = RutaMasaEfectiva()

    # ─── Ruta A ───
    print(f"\n  [Ruta A — Holográfica]")

    f_raw = ra.frecuencia_bruta_hz()
    ok = _check(
        90.0 < f_raw < 120.0,
        f"f_raw_A = {f_raw:.5f} Hz (rango esperado: 90–120 Hz)",
    )
    if not ok:
        fallos += 1

    fa = ra.frecuencia_hz()
    ok = _check(
        38.0 < fa < 44.0,
        f"f_A = {fa:.5f} Hz (rango esperado: 38–44 Hz)",
    )
    if not ok:
        fallos += 1

    t7 = 40.918719012147495
    ok = _check(
        abs(fa - t7) < 0.1,
        f"f_A ≈ γ₇ = {t7:.6f} Hz (7.º cero de Riemann, Δ = {abs(fa-t7):.4f} Hz)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(ra.factor_n7() - 2.5) < 1e-10,
        f"N₇ = {ra.factor_n7()} = 5/2",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(ra.info()["psi"] - 0.9469) < 1e-4,
        f"Ψ_A = {_PSI_A:.4f}",
    )
    if not ok:
        fallos += 1

    # ─── Ruta B ───
    print(f"\n  [Ruta B — Topológica Chern-Simons C₇]")

    ft = rb.factor_topologico()
    ok = _check(
        0.0 < ft < 1.0,
        f"Factor topológico sin(2π/7)·(1−cos(2π/7)) = {ft:.6f}",
    )
    if not ok:
        fallos += 1

    t_energy = rb.t_energy_joules()
    ok = _check(
        1e-33 < t_energy < 1e-31,
        f"t_energy = {t_energy:.4e} J (orden ~2×10⁻³² J)",
    )
    if not ok:
        fallos += 1

    fb = rb.frecuencia_hz()
    ok = _check(
        48.0 < fb < 54.0,
        f"f_B = {fb:.5f} Hz (rango esperado: 48–54 Hz)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(fb - 50.54) / 50.54 < 0.01,
        f"f_B ≈ 50.54 Hz: error relativo = {abs(fb-50.54)/50.54*100:.3f}%",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(rb.info()["psi"] - 0.9819) < 1e-4,
        f"Ψ_B = {_PSI_B:.4f}",
    )
    if not ok:
        fallos += 1

    # ─── Ruta C ───
    print(f"\n  [Ruta C — Masa Efectiva]")

    corr = rc.correccion_topologica()
    ok = _check(
        0.0 < corr < 0.01,
        f"Corrección topológica sin⁷(π/7)·cos(π/7) = {corr:.6e}",
    )
    if not ok:
        fallos += 1

    m0 = rc.masa_canonica_kg()
    ok = _check(
        1e-49 < m0 < 1e-47,
        f"m₀ = h·F₀/c² = {m0:.4e} kg",
    )
    if not ok:
        fallos += 1

    m_eff = rc.masa_efectiva_kg()
    ok = _check(
        m_eff < m0,
        f"m_eff < m₀: {m_eff:.4e} kg < {m0:.4e} kg",
    )
    if not ok:
        fallos += 1

    fc = rc.frecuencia_hz()
    ok = _check(
        139.0 < fc < 143.0,
        f"f_C = {fc:.5f} Hz (rango esperado: 139–143 Hz)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(fc - 141.34) / 141.34 < 0.005,
        f"f_C ≈ 141.34 Hz: error relativo = {abs(fc-141.34)/141.34*100:.3f}%",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(rc.info()["psi"] - 0.9993) < 1e-4,
        f"Ψ_C = {_PSI_C:.4f}",
    )
    if not ok:
        fallos += 1

    print(f"\n  Fase 2: {16 - fallos}/16 checks superados")
    return fallos


# ============================================================================
# FASE 3 — COHERENCIA GLOBAL Y CONVERGENCIA
# ============================================================================

def fase_3_coherencia() -> int:
    """Verifica la coherencia global y la convergencia hacia F₀."""
    _seccion("FASE 3 — Coherencia global y convergencia hacia F₀")
    fallos = 0

    coh = CoherenciaConvergencia()

    pg = coh.psi_global()
    ok = _check(
        pg >= _PSI_UMBRAL,
        f"Ψ_global = {pg:.6f} ≥ {_PSI_UMBRAL} (umbral QCAL)",
    )
    if not ok:
        fallos += 1

    ok = _check(
        0.0 < pg <= 1.0,
        f"Ψ_global ∈ (0, 1]: {pg:.6f}",
    )
    if not ok:
        fallos += 1

    pa, pb, pc = coh.psi_individual()
    n = 3
    expected_harm = n / (1.0 / pa + 1.0 / pb + 1.0 / pc)
    ok = _check(
        abs(pg - expected_harm) < 1e-10,
        f"Ψ_global es la media armónica de Ψ_A, Ψ_B, Ψ_C: {pg:.8f}",
    )
    if not ok:
        fallos += 1

    ok = _check(
        pa < pb < pc,
        f"Orden de coherencias: Ψ_A={pa} < Ψ_B={pb} < Ψ_C={pc}",
    )
    if not ok:
        fallos += 1

    fa, fb, fc = coh.frecuencias_hz()
    ok = _check(
        fa < fb < fc,
        f"Orden de frecuencias: f_A={fa:.3f} < f_B={fb:.3f} < f_C={fc:.3f} Hz",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(fc - _F0) < abs(fa - _F0) and abs(fc - _F0) < abs(fb - _F0),
        f"f_C más próxima a F₀: |f_C−F₀|={abs(fc-_F0):.4f} < "
        f"|f_A−F₀|={abs(fa-_F0):.4f} y |f_B−F₀|={abs(fb-_F0):.4f}",
    )
    if not ok:
        fallos += 1

    ok = _check(
        abs(fc - _F0) / _F0 < 0.003,
        f"f_C ≈ F₀: error relativo = {abs(fc-_F0)/_F0*100:.4f}%",
    )
    if not ok:
        fallos += 1

    ok = _check(
        coh.validar(),
        f"validar() devuelve True (Ψ_global = {pg:.4f} ≥ {_PSI_UMBRAL})",
    )
    if not ok:
        fallos += 1

    ok = _check(
        not coh.validar(umbral=0.999),
        "validar(0.999) devuelve False (Ψ_global < 0.999)",
    )
    if not ok:
        fallos += 1

    media_arit = coh.media_aritmetica_hz()
    ok = _check(
        abs(media_arit - (fa + fb + fc) / 3.0) < 1e-10,
        f"Media aritmética = {media_arit:.5f} Hz = (f_A+f_B+f_C)/3",
    )
    if not ok:
        fallos += 1

    print(f"\n  Fase 3: {10 - fallos}/10 checks superados")
    return fallos


# ============================================================================
# FASE 4 — INTEGRACIÓN Y API PÚBLICA
# ============================================================================

def fase_4_integracion() -> int:
    """Verifica la API pública y las propiedades del sistema integrado."""
    _seccion("FASE 4 — Integración: API pública y sistema RCF∞³")
    fallos = 0

    # ─── API pública ───
    try:
        resultado = rutas_convergencia_calcular()
        ok = _check(True, "rutas_convergencia_calcular() ejecuta sin errores")
    except Exception as exc:
        ok = _check(False, f"rutas_convergencia_calcular() lanzó excepción: {exc}")
        fallos += 1
        return fallos
    if not ok:
        fallos += 1

    ok = _check(
        isinstance(resultado, dict),
        "El resultado es un diccionario",
    )
    if not ok:
        fallos += 1

    ok = _check(
        resultado["validacion"] is True,
        f"validacion = True (Ψ_global = {resultado['psi_global']:.4f})",
    )
    if not ok:
        fallos += 1

    ok = _check(
        resultado["psi_global"] >= _PSI_UMBRAL,
        f"psi_global = {resultado['psi_global']:.4f} ≥ {_PSI_UMBRAL}",
    )
    if not ok:
        fallos += 1

    for ruta_key, nombre in (("A", "Holográfica"), ("B", "Topológica"), ("C", "Masa Efectiva")):
        ok = _check(
            ruta_key in resultado["rutas"],
            f"Ruta {ruta_key} ({nombre}) presente en el resultado",
        )
        if not ok:
            fallos += 1

    # ─── SistemaRutasConvergencia ───
    sistema = SistemaRutasConvergencia()

    for metodo_nombre, metodo in (
        ("resultado_ruta_a()", sistema.resultado_ruta_a),
        ("resultado_ruta_b()", sistema.resultado_ruta_b),
        ("resultado_ruta_c()", sistema.resultado_ruta_c),
    ):
        res = metodo()
        ok = _check(
            isinstance(res, ResultadoRuta),
            f"{metodo_nombre} devuelve ResultadoRuta",
        )
        if not ok:
            fallos += 1

        ok = _check(
            res.converge,
            f"{metodo_nombre}: converge = True (error = {res.error_relativo*100:.3f}%)",
        )
        if not ok:
            fallos += 1

    # ─── ResultadoConvergencia ───
    f_a = sistema.ruta_a.frecuencia_hz()
    f_b = sistema.ruta_b.frecuencia_hz()
    f_c = sistema.ruta_c.frecuencia_hz()
    pg = sistema.coherencia.psi_global()

    try:
        rc_obj = ResultadoConvergencia(
            f_a_hz=f_a, f_b_hz=f_b, f_c_hz=f_c,
            psi_a=_PSI_A, psi_b=_PSI_B, psi_c=_PSI_C,
            psi_global=pg, valido=True,
        )
        ok = _check(True, f"ResultadoConvergencia creado: {rc_obj!r}")
    except ValueError as exc:
        ok = _check(False, f"ResultadoConvergencia lanzó ValueError: {exc}")
        fallos += 1
    if not ok:
        fallos += 1

    # ─── Idempotencia ───
    resultado2 = rutas_convergencia_calcular()
    ok = _check(
        abs(resultado["psi_global"] - resultado2["psi_global"]) < 1e-10,
        f"API idempotente: Ψ_global idéntica en dos llamadas",
    )
    if not ok:
        fallos += 1

    # ─── Resumen de frecuencias ───
    print()
    print(f"  {_INFO} Tabla de resultados:")
    print(f"  {'Ruta':<40} {'f (Hz)':>12} {'Ψ':>8}")
    print(f"  {'─'*40} {'─'*12} {'─'*8}")
    for ruta_key in ("A", "B", "C"):
        f_ruta = resultado["rutas"][ruta_key]["frecuencia_hz"]
        psi_ruta = resultado["rutas"][ruta_key]["psi"]
        nombre = resultado["rutas"][ruta_key]["nombre"]
        print(f"  {nombre:<40} {f_ruta:>12.5f} {psi_ruta:>8.4f}")
    print(f"  {'Coherencia global (media armónica)':<40} {'':>12} {resultado['psi_global']:>8.4f}")
    print(f"  {'F₀ objetivo':<40} {_F0:>12.4f} {'—':>8}")

    print(f"\n  Fase 4: {(3 + 3 + 6 + 2 + 1) - fallos}/{3 + 3 + 6 + 2 + 1} checks superados")
    return fallos


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    """Ejecuta las 4 fases de validación y devuelve el número total de fallos."""
    print()
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║         VALIDACIÓN: Las 3 Rutas de Convergencia Física (RCF∞³)         ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")

    total_fallos = 0
    total_fallos += fase_1_constantes()
    total_fallos += fase_2_frecuencias()
    total_fallos += fase_3_coherencia()
    total_fallos += fase_4_integracion()

    print()
    print("═" * 72)
    if total_fallos == 0:
        print(f"  {_OK} VALIDACIÓN COMPLETA — 0 fallos")
        print("  Ψ_global ≈ 0,9755 ≥ 0,888 — Sistema RCF∞³ VALIDADO ∴𓂀Ω∞³Φ")
    else:
        print(f"  {_FAIL} VALIDACIÓN FALLIDA — {total_fallos} fallos detectados")
    print("═" * 72)
    print()

    return total_fallos


if __name__ == "__main__":
    sys.exit(main())
