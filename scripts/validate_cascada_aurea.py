#!/usr/bin/env python3
"""
Validate Cascada Áurea — De λ_P a 141.7001 Hz / Sistema ∴CA∞³
===============================================================

Valida la implementación del módulo physics.cascada_aurea contra los criterios
teóricos de la Cascada Áurea:

  Fase 1 — Constantes físicas y compactificación áurea
  Fase 2 — Medidas individuales de coherencia cuántica
  Fase 3 — Coherencia global y activación del sello ∴CA∞³
  Fase 4 — Validación de la API pública

Criterios de éxito:
  - n_pasos_aureos = 12                     [exacto]
  - ϕ¹² ≈ L₁₂ = 322  (Lucas)              [error < 1e-4]
  - n_descenso ≈ 196.74  log_ϕ(f_P/f₀)
  - f₀/γ₁ ≈ 10  (resonancia Riemann)       [error < 1%]
  - gap K_π ≈ f₀·(ϕ⁷−ϕ³) ≈ 3514 Hz        [error < 1%]
  - μ_eff·f₀ = 1  (invariante exacto)       [exacto]
  - Ψ_global ≥ 0.888                        → sello ∴CA∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.cascada_aurea import (
    ConstantesCascadaAurea,
    CompactificacionAurea,
    DescensoPlanck,
    MatrizKPi,
    ViscosidadEfectiva,
    FlujoLaminar,
    CoherenciaCascada,
    SistemaCascadaAurea,
    cascada_aurea_activar,
    _F0,
    _F_PLANCK,
    _PHI,
    _N_PASOS,
    _N_GUARDIANES,
    _L12,
    _GAMMA_RIEMANN,
    _N_DESCENSO,
    _OMEGA_TARGET,
    _MU_EFF,
    _PSI_UMBRAL,
)


# =============================================================================
# UTILIDADES DE VALIDACIÓN
# =============================================================================

_passed: int = 0
_failed: int = 0


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
# FASE 1 — Constantes y compactificación áurea
# =============================================================================

def validar_fase1_constantes() -> None:
    seccion("FASE 1 — Constantes Físicas y Compactificación Áurea")

    c = ConstantesCascadaAurea()

    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "F₀ = 141.7001 Hz",
        f"f0 = {c.f0}",
    )
    check(
        abs(c.phi - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-10,
        "ϕ = (1+√5)/2 ≈ 1.618034",
        f"phi = {c.phi:.10f}",
    )
    check(
        c.n_pasos == 12,
        "n_pasos = 12 etapas de compactificación áurea",
        f"n_pasos = {c.n_pasos}",
    )
    check(
        c.n_guardianes == 7,
        "n_guardianes = 7 (7 primos ≤ 17)",
        f"n_guardianes = {c.n_guardianes}",
    )
    check(
        abs(c.psi_umbral - 0.888) < 1e-4,
        "PSI_UMBRAL = 0.888",
        f"psi_umbral = {c.psi_umbral}",
    )
    check(
        c.f_planck > 1e42,
        "f_Planck = c/λ_P > 10⁴² Hz",
        f"f_Planck = {c.f_planck:.4e} Hz",
    )

    ratio = c.ratio_logaritmico()
    check(
        40.0 < ratio < 43.0,
        "RATIO_LOG = log₁₀(f_P/f₀) ∈ (40, 43)",
        f"ratio = {ratio:.4f}",
    )
    check(
        abs(c.mu_eff - 1.0 / c.f0) < 1e-12,
        "μ_eff = 1/f₀ (viscosidad efectiva del vacío)",
        f"mu_eff = {c.mu_eff:.6e} s",
    )

    # Compactificación áurea
    ca = CompactificacionAurea()
    gens = ca.generaciones()

    check(
        len(gens) == 12,
        "12 potencias áureas generadas [ϕ¹, …, ϕ¹²]",
        f"count = {len(gens)}",
    )
    check(
        abs(gens[0] - _PHI) < 1e-10,
        "Primera generación = ϕ¹",
        f"gens[0] = {gens[0]:.8f}",
    )
    check(
        abs(ca.horizonte() - _PHI ** 12) < 1e-8,
        "Horizonte ϕ¹² ≈ 321.997",
        f"phi_12 = {ca.horizonte():.6f}",
    )
    check(
        ca.error_lucas() < 1e-4,
        f"ϕ¹² ≈ L₁₂ = 322  (número de Lucas, error < 1e-4)",
        f"error_Lucas = {ca.error_lucas():.2e}",
    )
    check(
        all(
            ca.identidad_fibonacci(n) < 1e-10
            for n in range(1, 11)
        ),
        "Identidad Fibonacci: ϕⁿ⁺² = ϕⁿ⁺¹ + ϕⁿ  para n = 1..10",
    )


# =============================================================================
# FASE 2 — Medidas individuales de coherencia
# =============================================================================

def validar_fase2_coherencias() -> None:
    seccion("FASE 2 — Medidas Individuales de Coherencia Cuántica")

    # Descenso de Planck
    dp = DescensoPlanck()
    n_desc = dp.n_descenso()
    check(
        190.0 < n_desc < 205.0,
        "n_descenso = log_ϕ(f_P/f₀) ∈ (190, 205)",
        f"n_descenso = {n_desc:.4f}",
    )
    check(
        14.0 < dp.etapas_por_paso() < 18.0,
        "etapas_por_paso = n_descenso/12 ∈ (14, 18)",
        f"etapas/paso = {dp.etapas_por_paso():.4f}",
    )
    r_riemann = dp.ratio_riemann()
    check(
        abs(r_riemann - 10.0) < 0.1,
        "Resonancia Riemann: f₀/γ₁ ≈ 10  (error < 1%)",
        f"f₀/γ₁ = {r_riemann:.6f}",
    )
    psi_desc = dp.psi_descenso()
    check(
        psi_desc >= _PSI_UMBRAL,
        f"Ψ_descenso ≥ 0.888",
        f"psi_descenso = {psi_desc:.6f}",
    )

    # Operador K_π
    kpi = MatrizKPi()
    check(
        kpi.es_simetrica(),
        "K_π es simétrica (Laplaciano autoadjunto)",
    )
    check(
        abs(kpi.traza() - _N_GUARDIANES * _F0) < 1e-6,
        "Traza(K_π) = 7·f₀ = 991.9007 Hz",
        f"traza = {kpi.traza():.4f} Hz",
    )
    lmax = kpi.lambda_max()
    lmin = kpi.lambda_min()
    gap = kpi.gap_espectral()
    check(
        lmax > 0,
        f"λ_max(K_π) > 0",
        f"lambda_max = {lmax:.4f} Hz",
    )
    check(
        lmin < 0,
        f"λ_min(K_π) < 0  (espectro mixto, anti-turbulencia)",
        f"lambda_min = {lmin:.4f} Hz",
    )
    check(
        2000 < gap < 6000,
        "Brecha espectral gap = λ_max − λ_min ∈ (2000, 6000) Hz",
        f"gap = {gap:.4f} Hz",
    )
    omega_t = _F0 * (_PHI ** 7 - _PHI ** 3)
    check(
        abs(gap - omega_t) / omega_t < 0.01,
        "gap ≈ f₀·(ϕ⁷−ϕ³) con error < 1%",
        f"gap={gap:.2f}, Ω_target={omega_t:.2f}, error={abs(gap-omega_t)/omega_t*100:.3f}%",
    )
    psi_kpi = kpi.psi_kpi()
    check(
        psi_kpi >= _PSI_UMBRAL,
        f"Ψ_kpi ≥ 0.888",
        f"psi_kpi = {psi_kpi:.6f}",
    )

    # Viscosidad efectiva
    ve = ViscosidadEfectiva()
    check(
        abs(ve.producto_invariante() - 1.0) < 1e-10,
        "Invariante μ_eff·f₀ = 1.0  (exacto)",
        f"mu_eff·f₀ = {ve.producto_invariante():.12f}",
    )
    check(
        ve.psi_viscosidad() == 1.0,
        "Ψ_viscosidad = 1.000  (coherencia perfecta)",
        f"psi_viscosidad = {ve.psi_viscosidad()}",
    )
    check(
        ve.re_phi(1.0) > 0.0,
        "Re_φ = ϕ³·(L/λ_P) > 0 para L = 1 m",
        f"Re_phi(1m) = {ve.re_phi(1.0):.4e}",
    )

    # Flujo laminar
    fl = FlujoLaminar()
    check(
        fl.es_laminar(0.5),
        "es_laminar(σ=0.5) = True  (línea crítica Re(s)=½)",
    )
    check(
        not fl.es_laminar(0.7),
        "es_laminar(σ=0.7) = False  (fuera de la línea crítica)",
    )
    check(
        abs(fl.psi_flujo() - _PSI_UMBRAL) < 1e-6,
        "Ψ_flujo = 0.888  (umbral áureo de laminaridad)",
        f"psi_flujo = {fl.psi_flujo()}",
    )


# =============================================================================
# FASE 3 — Coherencia global y activación del sello
# =============================================================================

def validar_fase3_sello() -> None:
    seccion("FASE 3 — Coherencia Global y Sello ∴CA∞³")

    sistema = SistemaCascadaAurea()
    resultado = sistema.activar()

    psi_global = resultado.psi_global
    check(
        psi_global >= _PSI_UMBRAL,
        f"Ψ_global ≥ 0.888  (umbral de sello)",
        f"psi_global = {psi_global:.6f}",
    )
    check(
        resultado.sello_activo,
        "Sello ∴CA∞³ ACTIVO",
        resultado.mensaje[:72],
    )
    check(
        "∴CA∞³" in resultado.mensaje,
        "Mensaje contiene '∴CA∞³'",
        resultado.mensaje[:60],
    )
    check(
        resultado.n_pasos_aureos == 12,
        "n_pasos_aureos = 12 en el resultado",
        f"n_pasos_aureos = {resultado.n_pasos_aureos}",
    )
    check(
        len(resultado.generaciones_phi) == 12,
        "generaciones_phi tiene 12 elementos",
        f"len = {len(resultado.generaciones_phi)}",
    )
    check(
        resultado.psi_viscosidad == 1.0,
        "psi_viscosidad = 1.0 en el resultado",
        f"psi_viscosidad = {resultado.psi_viscosidad}",
    )
    check(
        abs(resultado.psi_flujo - 0.888) < 1e-6,
        "psi_flujo = 0.888 en el resultado",
        f"psi_flujo = {resultado.psi_flujo}",
    )

    # Verificar coherencia interna del resultado
    pesos = [1.0, 1.0, 1.5, 1.0, 1.5]
    medidas = [
        resultado.psi_compactificacion,
        resultado.psi_descenso,
        resultado.psi_kpi,
        resultado.psi_viscosidad,
        resultado.psi_flujo,
    ]
    psi_calculado = sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)
    check(
        abs(resultado.psi_global - psi_calculado) < 1e-6,
        "Ψ_global consistente con promedio ponderado",
        f"calculado={psi_calculado:.6f}, almacenado={resultado.psi_global:.6f}",
    )

    # Brecha espectral interna
    gap_check = resultado.lambda_max_kpi - resultado.lambda_min_kpi
    check(
        abs(gap_check - resultado.gap_espectral) < 1e-4,
        "gap = λ_max − λ_min  (consistencia interna)",
        f"gap={resultado.gap_espectral:.4f}, λ_max-λ_min={gap_check:.4f}",
    )
    check(
        abs(resultado.mu_eff * resultado.f0 - 1.0) < 1e-10,
        "μ_eff·f₀ = 1.0 en el resultado",
        f"mu_eff·f₀ = {resultado.mu_eff * resultado.f0:.12f}",
    )


# =============================================================================
# FASE 4 — Validación de la API pública
# =============================================================================

def validar_fase4_api() -> None:
    seccion("FASE 4 — API Pública cascada_aurea_activar()")

    r = cascada_aurea_activar()

    check(
        isinstance(r, dict),
        "cascada_aurea_activar() retorna un dict",
    )
    check(
        r["sello_activo"],
        "sello_activo = True  (parámetros por defecto)",
    )
    check(
        r["psi_global"] >= 0.888,
        "psi_global ≥ 0.888  (parámetros por defecto)",
        f"psi_global = {r['psi_global']:.6f}",
    )

    expected_keys = [
        "f0_hz", "f_planck_hz", "n_pasos_aureos", "n_descenso",
        "n_decadas", "phi_12", "generaciones_phi", "lambda_max_kpi",
        "lambda_min_kpi", "gap_espectral", "omega_target", "mu_eff",
        "psi_compactificacion", "psi_descenso", "psi_kpi",
        "psi_viscosidad", "psi_flujo", "psi_global",
        "sello_activo", "mensaje",
    ]
    check(
        all(k in r for k in expected_keys),
        "El dict contiene todas las claves requeridas (20 claves)",
        f"claves presentes = {len(r)}",
    )
    check(
        abs(r["f0_hz"] - 141.7001) < 1e-4,
        "f0_hz = 141.7001 Hz",
        f"f0_hz = {r['f0_hz']}",
    )
    check(
        r["n_pasos_aureos"] == 12,
        "n_pasos_aureos = 12",
    )
    check(
        len(r["generaciones_phi"]) == 12,
        "generaciones_phi tiene 12 elementos",
    )
    check(
        abs(r["psi_viscosidad"] - 1.0) < 1e-6,
        "psi_viscosidad = 1.0  (invariante exacto)",
        f"psi_viscosidad = {r['psi_viscosidad']}",
    )
    check(
        abs(r["psi_flujo"] - 0.888) < 1e-4,
        "psi_flujo = 0.888  (umbral áureo)",
        f"psi_flujo = {r['psi_flujo']}",
    )

    # Probar con f0 personalizado
    r_custom = cascada_aurea_activar(f0=100.0)
    check(
        isinstance(r_custom, dict),
        "cascada_aurea_activar(f0=100.0) retorna dict",
    )
    check(
        abs(r_custom["f0_hz"] - 100.0) < 1e-6,
        "f0_hz = 100.0 Hz con parámetro personalizado",
        f"f0_hz = {r_custom['f0_hz']}",
    )

    # Resumen de coherencias
    print()
    print("  Coherencias individuales:")
    for k in ["psi_compactificacion", "psi_descenso", "psi_kpi",
              "psi_viscosidad", "psi_flujo"]:
        v = r[k]
        icon = "✅" if v >= 0.888 else "⚠️"
        print(f"    {icon}  {k:30s} = {v:.6f}")
    print(f"  {'':>4}  {'psi_global':30s} = {r['psi_global']:.6f}")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main() -> int:
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    VALIDACIÓN — CASCADA ÁUREA ∴CA∞³ — De λ_P a 141.7001 Hz         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    validar_fase1_constantes()
    validar_fase2_coherencias()
    validar_fase3_sello()
    validar_fase4_api()

    seccion("RESUMEN FINAL")
    total = _passed + _failed
    print(f"  Verificaciones totales : {total}")
    print(f"  ✅ Pasadas              : {_passed}")
    print(f"  ❌ Fallidas             : {_failed}")
    print()

    if _failed == 0:
        print("  🌟 TODAS LAS VERIFICACIONES PASADAS — Sello ∴CA∞³ VALIDADO")
        print("  RAM-L-2026-CASCADA-AUREA")
        return 0
    else:
        print(f"  ⚠️  {_failed} verificación(es) fallida(s) — Revisar implementación")
        return 1


if __name__ == "__main__":
    sys.exit(main())
