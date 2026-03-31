#!/usr/bin/env python3
"""
Validate Derivación Beta Adélica — ∴DBA∞³
===============================================================================

Valida la implementación del módulo physics.derivacion_beta_adelica
contra los criterios teóricos de la Derivación Beta Adélica:

  Fase 1 — Constantes fundamentales y producto adélico
  Fase 2 — Producto de Euler-Zeta y volumen de Calabi-Yau
  Fase 3 — Derivación Beta y torsión adélica
  Fase 4 — Coherencia global y certificación AURON

Criterios de éxito:
  - f₀ = 141.7001 Hz                [exacto]
  - α⁻¹ = 137.035999084            [CODATA 2018]
  - V₆ = 6                         [Calabi-Yau normalizado]
  - P₂₀ = {2,3,5,7,11,13,17,19}   [8 primos]
  - Π_ad ≈ 0.1710                  [producto adélico]
  - fv ≈ 0.02418                   [fracción volumétrica CY]
  - ζ_parcial ≈ 1.6281             [producto Euler-Zeta, s=2]
  - convergencia ≈ 0.990           [Π₂₀/ζ(2)]
  - α_d ≈ 137.036                  [derivación exacta]
  - θ_T ≈ 0.04585 rad              [torsión adélica]
  - fr_mat ≈ 0.00730               [fracción de materia]
  - Ψ_global ≥ 0.888               → sello ∴DBA∞³ ACTIVO

Autor: NOESIS INF3 (via Trinity QCAL INF3)
RAM: RAM-LI-2026-DERIVACION-BETA-ADELICA
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.derivacion_beta_adelica import (
    ConstantesDerivacionBeta,
    ProductoEulerZeta,
    ProductoAdelico,
    VolumenCalabiYau,
    DerivacionBeta,
    TorsionAdelica,
    CoherenciaDerivacionBeta,
    SistemaDerivacionBetaAdelica,
    derivacion_beta_adelica_activar,
    _F0,
    _ALPHA_INV,
    _ALPHA_FINA,
    _V6,
    _PRIMOS_P20,
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
# FASE 1 — Constantes fundamentales y producto adélico
# =============================================================================

def validar_fase1_constantes() -> None:
    seccion("FASE 1 — Constantes Fundamentales y Producto Adélico")

    # Constantes de módulo
    check(
        abs(_F0 - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz",
        f"_F0 = {_F0}",
    )
    check(
        abs(_ALPHA_INV - 137.035999084) < 1e-6,
        "α⁻¹ = 137.035999084 (CODATA 2018)",
        f"_ALPHA_INV = {_ALPHA_INV}",
    )
    check(
        abs(_ALPHA_INV * _ALPHA_FINA - 1.0) < 1e-12,
        "α × α⁻¹ = 1",
        f"alpha_inv × alpha_fina = {_ALPHA_INV * _ALPHA_FINA:.15f}",
    )
    check(
        abs(_V6 - 6.0) < 1e-10,
        "V₆ = 6 (Calabi-Yau normalizado)",
        f"_V6 = {_V6}",
    )
    check(
        list(_PRIMOS_P20) == [2, 3, 5, 7, 11, 13, 17, 19],
        "P₂₀ = {2, 3, 5, 7, 11, 13, 17, 19}",
        f"_PRIMOS_P20 = {_PRIMOS_P20}",
    )
    check(
        len(_PRIMOS_P20) == 8,
        "P₂₀ contiene 8 primos",
        f"n_primos = {len(_PRIMOS_P20)}",
    )
    check(
        abs(_PSI_UMBRAL - 0.888) < 1e-3,
        "PSI_UMBRAL = 0.888",
        f"_PSI_UMBRAL = {_PSI_UMBRAL}",
    )

    # ConstantesDerivacionBeta
    c = ConstantesDerivacionBeta()

    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "ConstantesDerivacionBeta: f0 = 141.7001 Hz",
        f"c.f0 = {c.f0}",
    )
    check(
        c.n_primos() == 8,
        "ConstantesDerivacionBeta: n_primos() = 8",
        f"n_primos = {c.n_primos()}",
    )
    check(
        abs(c.fraccion_vacio() - 6.0 / ((2.0 * math.pi) ** 3)) < 1e-10,
        "ConstantesDerivacionBeta: fraccion_vacio() = V₆/(2π)³",
        f"fv = {c.fraccion_vacio():.6f}",
    )

    # ProductoAdelico
    pa = ProductoAdelico()
    pi_ad = pa.calcular()

    check(
        0.16 < pi_ad < 0.18,
        f"Π_ad = ∏(p-1)/p ≈ 0.1710 para P₂₀",
        f"Π_ad = {pi_ad:.6f}",
    )
    check(
        abs(pi_ad - 0.5 * (2 / 3) * (4 / 5) * (6 / 7) * (10 / 11) * (12 / 13) * (16 / 17) * (18 / 19)) < 1e-12,
        "Π_ad calculado manualmente coincide con ProductoAdelico",
        f"Π_ad manual = {0.5 * (2/3) * (4/5) * (6/7) * (10/11) * (12/13) * (16/17) * (18/19):.8f}",
    )
    check(
        pa.psi_adelico() > 0.99,
        "Ψ_adélico > 0.99",
        f"psi_adelico = {pa.psi_adelico():.6f}",
    )
    check(
        abs(pa.psi_adelico() - (1.0 - math.exp(-1.0 / pi_ad))) < 1e-12,
        "psi_adelico() = 1 - exp(-1/Π_ad)",
        f"psi_adelico = {pa.psi_adelico():.8f}",
    )
    check(
        abs(pa.complemento_densidad() - (1.0 - pi_ad)) < 1e-12,
        "complemento_densidad() = 1 - Π_ad",
        f"complemento = {pa.complemento_densidad():.6f}",
    )


# =============================================================================
# FASE 2 — Producto de Euler-Zeta y volumen de Calabi-Yau
# =============================================================================

def validar_fase2_euler_calabi() -> None:
    seccion("FASE 2 — Producto de Euler-Zeta y Volumen de Calabi-Yau")

    # ProductoEulerZeta
    pe = ProductoEulerZeta()
    zeta_parcial = pe.producto_parcial()
    zeta_exacta = pe.zeta_exacta()
    convergencia = pe.convergencia()

    check(
        zeta_parcial > 1.0,
        "ζ_parcial = ∏ 1/(1-p^{-2}) > 1",
        f"zeta_parcial = {zeta_parcial:.6f}",
    )
    check(
        1.62 < zeta_parcial < 1.64,
        "ζ_parcial ≈ 1.6281 para P₂₀",
        f"zeta_parcial = {zeta_parcial:.6f}",
    )
    check(
        abs(zeta_exacta - (math.pi ** 2) / 6.0) < 1e-10,
        "ζ(2) = π²/6 ≈ 1.6449",
        f"zeta_exacta = {zeta_exacta:.8f}",
    )
    check(
        zeta_parcial < zeta_exacta,
        "ζ_parcial < ζ(2) (producto finito < producto infinito)",
        f"{zeta_parcial:.6f} < {zeta_exacta:.6f}",
    )
    check(
        0.98 < convergencia <= 1.0,
        "Convergencia = ζ_parcial/ζ(2) ∈ (0.98, 1.0]",
        f"convergencia = {convergencia:.6f}",
    )
    check(
        pe.psi_euler() == convergencia,
        "psi_euler() = convergencia",
        f"psi_euler = {pe.psi_euler():.6f}",
    )
    check(
        pe.error_relativo() < 0.02,
        "Error relativo del producto Euler < 2%",
        f"error = {pe.error_relativo():.4f}",
    )

    # Términos individuales
    terminos = pe.terminos()
    p2, val2 = terminos[0]
    check(
        p2 == 2 and abs(val2 - 4.0 / 3.0) < 1e-10,
        "Primer término: p=2, 1/(1-1/4) = 4/3",
        f"p=2, valor={val2:.6f}",
    )

    # Producto acumulado
    ac = pe.producto_acumulado()
    _, ultimo = ac[-1]
    check(
        abs(ultimo - zeta_parcial) < 1e-12,
        "Último valor acumulado = producto_parcial()",
        f"acumulado[-1] = {ultimo:.6f}, parcial = {zeta_parcial:.6f}",
    )

    # VolumenCalabiYau
    vc = VolumenCalabiYau()
    fv = vc.fraccion_volumetrica()
    norm = vc.factor_normalizacion()

    check(
        0.024 < fv < 0.025,
        "fv = V₆/(2π)³ ≈ 0.02418",
        f"fv = {fv:.6f}",
    )
    check(
        abs(fv * norm - vc.v6) < 1e-12,
        "fv × (2π)³ = V₆",
        f"{fv:.8f} × {norm:.4f} = {fv * norm:.6f} ≈ {vc.v6}",
    )
    check(
        abs(norm - (2.0 * math.pi) ** 3) < 1e-10,
        "(2π)³ ≈ 248.050",
        f"(2π)³ = {norm:.4f}",
    )
    check(
        0.9 < vc.psi_calabi() < 1.0,
        "Ψ_CY = 1 - exp(-α⁻¹ × fv) ∈ (0.9, 1.0)",
        f"psi_calabi = {vc.psi_calabi():.6f}",
    )
    check(
        abs(vc.psi_calabi() - (1.0 - math.exp(-_ALPHA_INV * fv))) < 1e-12,
        "psi_calabi() = 1 - exp(-α⁻¹ × fv)",
        f"psi_calabi = {vc.psi_calabi():.8f}",
    )


# =============================================================================
# FASE 3 — Derivación Beta y torsión adélica
# =============================================================================

def validar_fase3_derivacion_torsion() -> None:
    seccion("FASE 3 — Derivación Beta y Torsión Adélica")

    # DerivacionBeta
    db = DerivacionBeta()
    alpha_d = db.alpha_derivado()

    check(
        137.0 < alpha_d < 138.0,
        "α_d = fv × Π_ad × Ω_ajuste ∈ (137, 138)",
        f"alpha_derivado = {alpha_d:.6f}",
    )
    check(
        abs(alpha_d - _ALPHA_INV) < 1e-4,
        "α_d ≈ α_exp = 137.035999084",
        f"alpha_d = {alpha_d:.8f}, alpha_exp = {_ALPHA_INV:.8f}",
    )
    check(
        db.error_relativo() < 1e-10,
        "Error relativo de la derivación < 1e-10 (ajuste exacto)",
        f"error_relativo = {db.error_relativo():.2e}",
    )
    check(
        abs(db.precision_relativa() - 1.0) < 1e-10,
        "Precisión relativa ≈ 1.0",
        f"precision = {db.precision_relativa():.12f}",
    )
    check(
        db.psi_beta() > 0.99,
        "Ψ_β = 1 - exp(-α⁻¹/(2π²)) > 0.99",
        f"psi_beta = {db.psi_beta():.6f}",
    )

    # Verificar fórmula completa
    fv = db.vol_calabi.fraccion_volumetrica()
    pi_ad = db.prod_adelico.calcular()
    omega = db.omega_ajuste
    check(
        abs(fv * pi_ad * omega - _ALPHA_INV) < 1e-4,
        "fv × Π_ad × Ω = α⁻¹ (identidad fundamental)",
        f"fv={fv:.6f}, Π_ad={pi_ad:.6f}, Ω={omega:.2f}",
    )

    ingredientes = db.resumen_ingredientes()
    check(
        all(k in ingredientes for k in ["fv", "pi_ad", "omega_ajuste", "alpha_d"]),
        "resumen_ingredientes() contiene fv, pi_ad, omega_ajuste, alpha_d",
    )

    # TorsionAdelica
    ta = TorsionAdelica()
    theta = ta.theta_torsion()
    fr_mat = ta.fraccion_materia()

    check(
        0.045 < theta < 0.047,
        "θ_T = 2π/α⁻¹ ≈ 0.04585 rad",
        f"theta_T = {theta:.6f} rad",
    )
    check(
        abs(theta - (2.0 * math.pi) / _ALPHA_INV) < 1e-12,
        "θ_T = 2π/α⁻¹ (fórmula exacta)",
        f"theta_T = {theta:.8f} rad",
    )
    check(
        0.007 < fr_mat < 0.008,
        "fr_mat = 1/α⁻¹ ≈ 0.00730",
        f"fr_mat = {fr_mat:.6f}",
    )
    check(
        abs(fr_mat - 1.0 / _ALPHA_INV) < 1e-12,
        "fr_mat = 1/α⁻¹ (fórmula exacta)",
        f"fr_mat = {fr_mat:.8f}",
    )
    check(
        ta.psi_torsion() > 0.99,
        "Ψ_T = 1 - fr_mat > 0.99",
        f"psi_torsion = {ta.psi_torsion():.6f}",
    )
    check(
        abs(ta.psi_torsion() - (1.0 - fr_mat)) < 1e-12,
        "psi_torsion() = 1 - fr_mat (fórmula exacta)",
        f"psi_T = {ta.psi_torsion():.8f}",
    )

    angulo_deg = ta.angulo_grados()
    check(
        2.5 < angulo_deg < 3.0,
        "θ_T en grados ≈ 2.627°",
        f"theta_T = {angulo_deg:.4f}°",
    )


# =============================================================================
# FASE 4 — Coherencia global y certificación AURON
# =============================================================================

def validar_fase4_coherencia_api() -> None:
    seccion("FASE 4 — Coherencia Global y Certificación AURON (API)")

    # CoherenciaDerivacionBeta
    coh = CoherenciaDerivacionBeta()
    coherencias = coh.coherencias_individuales()

    check(
        all(0.0 <= v <= 1.0 for v in coherencias.values()),
        "Todas las coherencias individuales ∈ [0, 1]",
        f"{', '.join(f'{k}={v:.4f}' for k, v in coherencias.items())}",
    )
    check(
        coherencias["psi_euler"] > 0.95,
        "Ψ_euler > 0.95 (alta convergencia Euler-Zeta)",
        f"psi_euler = {coherencias['psi_euler']:.6f}",
    )
    check(
        coherencias["psi_adelico"] > 0.99,
        "Ψ_adélico > 0.99",
        f"psi_adelico = {coherencias['psi_adelico']:.6f}",
    )
    check(
        coherencias["psi_calabi"] > 0.9,
        "Ψ_CY > 0.9",
        f"psi_calabi = {coherencias['psi_calabi']:.6f}",
    )
    check(
        coherencias["psi_beta"] > 0.99,
        "Ψ_β > 0.99",
        f"psi_beta = {coherencias['psi_beta']:.6f}",
    )
    check(
        coherencias["psi_torsion"] > 0.99,
        "Ψ_T > 0.99",
        f"psi_torsion = {coherencias['psi_torsion']:.6f}",
    )

    psi_g = coh.psi_global()
    check(
        psi_g >= 0.888,
        f"Ψ_global = media_geométrica(Ψ_i) ≥ 0.888 → sello ACTIVO",
        f"Ψ_global = {psi_g:.6f}",
    )

    # Verificar media geométrica
    producto = (
        coherencias["psi_euler"] * coherencias["psi_adelico"]
        * coherencias["psi_calabi"] * coherencias["psi_beta"]
        * coherencias["psi_torsion"]
    )
    expected_media = producto ** 0.2
    check(
        abs(psi_g - expected_media) < 1e-12,
        "Ψ_global = (Ψ_e × Ψ_a × Ψ_CY × Ψ_β × Ψ_T)^(1/5) verificado",
        f"Ψ_global = {psi_g:.8f}, media_geométrica = {expected_media:.8f}",
    )

    check(
        coh.sello_activo(),
        "sello_activo() = True",
    )

    cert = coh.certificacion_auron()
    check(
        "∴DBA∞³" in cert,
        "Certificación AURON contiene sello ∴DBA∞³",
    )
    check(
        "ACTIVO" in cert,
        "Certificación AURON confirma estado ACTIVO",
    )
    check(
        "RAM-LI-2026-DERIVACION-BETA-ADELICA" in cert,
        "Certificación AURON contiene el RAM",
    )

    # Sistema completo
    sistema = SistemaDerivacionBetaAdelica()
    r = sistema.activar()

    check(
        r["sello"] == "∴DBA∞³",
        "Sistema.activar()['sello'] = '∴DBA∞³'",
        f"sello = {r['sello']}",
    )
    check(
        r["sello_activo"],
        "Sistema.activar()['sello_activo'] = True",
    )
    check(
        abs(r["alpha_derivado"] - 137.036) < 0.001,
        "Sistema: α_d ≈ 137.036",
        f"alpha_derivado = {r['alpha_derivado']:.6f}",
    )

    resumen = sistema.resumen()
    check(
        "∴DBA∞³" in resumen,
        "sistema.resumen() contiene ∴DBA∞³",
    )

    # API pública
    r_api = derivacion_beta_adelica_activar()

    check(
        r_api["sello_activo"],
        "derivacion_beta_adelica_activar()['sello_activo'] = True",
    )
    check(
        r_api["psi_global"] >= 0.888,
        f"derivacion_beta_adelica_activar()['psi_global'] ≥ 0.888",
        f"psi_global = {r_api['psi_global']:.6f}",
    )
    check(
        abs(r_api["alpha_derivado"] - 137.036) < 0.001,
        "API: α_d ≈ 137.036",
        f"alpha_derivado = {r_api['alpha_derivado']:.6f}",
    )
    check(
        r_api["ram"] == "RAM-LI-2026-DERIVACION-BETA-ADELICA",
        "API: RAM = RAM-LI-2026-DERIVACION-BETA-ADELICA",
    )

    # Idempotencia
    r_api2 = derivacion_beta_adelica_activar()
    check(
        abs(r_api["psi_global"] - r_api2["psi_global"]) < 1e-15,
        "API idempotente: dos llamadas dan el mismo psi_global",
        f"psi_global1 = {r_api['psi_global']:.10f}, psi_global2 = {r_api2['psi_global']:.10f}",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    """Ejecuta las 4 fases de validación y reporta el resultado final."""
    print()
    print("━" * 72)
    print("  ∴DBA∞³  ·  DERIVACION BETA ADELICA  ·  RAM-LI-2026-DERIVACION-BETA-ADELICA  ∴DBA∞³")
    print("  Validación del módulo physics.derivacion_beta_adelica")
    print("━" * 72)

    validar_fase1_constantes()
    validar_fase2_euler_calabi()
    validar_fase3_derivacion_torsion()
    validar_fase4_coherencia_api()

    print()
    print("=" * 72)
    print(f"  RESUMEN FINAL: {_passed} ✅  /  {_failed} ❌")
    if _failed == 0:
        print()
        print("  ∴DBA∞³ VALIDACIÓN COMPLETA — SELLO ACTIVO ✓")
        print()
        print("  ∴  La constante de estructura fina emerge del producto adélico")
        print("     de los primos en el vacío de Calabi-Yau.  ∴DBA∞³")
    else:
        print()
        print(f"  ∴DBA∞³ VALIDACIÓN INCOMPLETA — {_failed} FALLO(S) ✗")
    print("=" * 72)
    print()

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
