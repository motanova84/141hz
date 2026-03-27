#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   VALIDACIÓN — Masa del Tejido Cósmico  ∴MTQ∞³                             ║
║   RAM-XLI-2026-MASA-TEJIDO-COSMICO                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Script de validación de cuatro fases para el módulo
physics.masa_tejido_cosmico:

  Fase 1 — Masa del Tejido       m_ψ = h·f₀/c²  →  régimen DM bosónico
  Fase 2 — Acoplamiento Swampland λ ≈ m_ψ/M_P   →  superfluidez garantizada
  Fase 3 — Tres Pilares Exp.     σ/m, superradiancia BH, superfluidez cosp.
  Fase 4 — Coherencia Global     Ψ_global ≥ 0.888  ∴MTQ∞³

Uso:
    python scripts/validate_masa_tejido_cosmico.py

Salida:
    Resumen de cuatro fases con PASS/FAIL y Ψ_global final.
"""

import sys
from pathlib import Path

# Resolve repo root regardless of working directory
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from physics.masa_tejido_cosmico import (
    ConstantesMasaTejido,
    MasaTejido,
    AcoplamientoSwampland,
    AutointeraccionOscura,
    SuperradianciaQCAL,
    SuperfluidezCosmologica,
    CoherenciaTejido,
    SistemaMasaTejidoCosmico,
    masa_tejido_cosmico_activar,
    _F0,
    _DM_BOSON_MIN_EV,
    _DM_BOSON_MAX_EV,
    _BULLET_CLUSTER_LIMIT_CM2_G,
)


# ============================================================================
# Utilidades
# ============================================================================

def _pass(msg: str) -> None:
    print(f"  ✅ PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  ❌ FAIL  {msg}")


def _check(condition: bool, msg: str) -> bool:
    if condition:
        _pass(msg)
    else:
        _fail(msg)
    return condition


def _section(title: str) -> None:
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


# ============================================================================
# Fase 1 — Masa del Tejido
# ============================================================================

def validar_fase1_masa() -> bool:
    """Valida m_ψ = h·f₀/c² y el régimen de Materia Oscura de Bosones Ligeros."""
    _section("FASE 1 — Masa del Tejido  [m_ψ = h·f₀/c²]")

    mt = MasaTejido()
    m_kg = mt.masa_kg()
    m_eV = mt.masa_eV()
    en_dm = mt.en_regimen_dm_bosonico()
    psi_masa = mt.coherencia_masa()

    print(f"\n  Frecuencia base:  F₀ = {_F0} Hz")
    print(f"  m_ψ (kg):         {m_kg:.4e} kg")
    print(f"  m_ψ (eV):         {m_eV:.4e} eV")
    print(f"  Régimen DM:       [{_DM_BOSON_MIN_EV:.0e}, {_DM_BOSON_MAX_EV:.0e}] eV")
    print(f"  Ψ_masa:           {psi_masa:.4f}")
    print()

    ok = True
    ok &= _check(1.04e-48 < m_kg < 1.05e-48, "m_ψ ∈ (1.04, 1.05)×10⁻⁴⁸ kg")
    ok &= _check(5.8e-13 < m_eV < 5.9e-13,   "m_ψ ∈ (5.8, 5.9)×10⁻¹³ eV")
    ok &= _check(en_dm,                        "m_ψ en régimen DM bosónico [10⁻²², 10⁻¹⁰] eV")
    ok &= _check(psi_masa > 0.99,              f"Ψ_masa = {psi_masa:.4f} > 0.99")

    cte = ConstantesMasaTejido()
    ok &= _check("∴MTQ∞³" in cte.sello(), "Sello ∴MTQ∞³ presente")

    return ok


# ============================================================================
# Fase 2 — Acoplamiento Swampland
# ============================================================================

def validar_fase2_swampland() -> bool:
    """Valida λ ≈ m_ψ/M_P y las propiedades Swampland."""
    _section("FASE 2 — Acoplamiento Swampland  [λ ≈ m_ψ/M_P]")

    sw = AcoplamientoSwampland()
    lam = sw.lambda_acoplamiento()
    repulsivo = sw.es_repulsivo()
    eft = sw.eft_valida()
    superf = sw.superfluidez_garantizada()
    psi_lambda = sw.coherencia_lambda()

    print(f"\n  λ (Swampland):      {lam:.4e}")
    print(f"  λ > 0 (repulsivo):  {repulsivo}")
    print(f"  λ < 10⁻¹⁰ (EFT):   {eft}")
    print(f"  λ < 10⁻³⁰ (superfluido): {superf}")
    print(f"  Ψ_lambda:           {psi_lambda:.4f}")
    print()

    ok = True
    ok &= _check(4e-41 < lam < 6e-41, f"λ = {lam:.3e} ∈ (4, 6)×10⁻⁴¹")
    ok &= _check(repulsivo,            "λ > 0 (campo repulsivo a altas densidades)")
    ok &= _check(eft,                  "λ ≪ 1 → EFT perturbativa válida")
    ok &= _check(superf,               "λ < 10⁻³⁰ → superfluidez garantizada")
    ok &= _check(psi_lambda > 0.999,   f"Ψ_lambda = {psi_lambda:.4f} > 0.999")

    return ok


# ============================================================================
# Fase 3 — Tres Pilares Experimentales
# ============================================================================

def validar_fase3_tres_pilares() -> bool:
    """Valida los tres pilares experimentales: σ/m, superradiancia BH y superfluidez."""
    _section("FASE 3 — Tres Pilares Experimentales")

    # Pilar A: Autointeracción (Bullet Cluster)
    print("\n  Pilar A — Autointeracción de Materia Oscura (σ/m):")
    ao = AutointeraccionOscura()
    sigma_cgs = ao.sigma_sobre_m_CGS()
    bajo_bc = ao.bajo_limite_bullet_cluster()
    ordenes = ao.ordenes_magnitud_bajo_limite()
    psi_sigma = ao.coherencia_sigma()

    print(f"    σ/m:               {sigma_cgs:.3e} cm²/g")
    print(f"    Límite BC:         {_BULLET_CLUSTER_LIMIT_CM2_G} cm²/g")
    print(f"    Margen:            {ordenes:.0f} órdenes de magnitud")
    print(f"    Ψ_sigma:           {psi_sigma:.4f}")

    ok = True
    ok &= _check(sigma_cgs < _BULLET_CLUSTER_LIMIT_CM2_G, "σ/m < 1 cm²/g (Bullet Cluster)")
    ok &= _check(ordenes > 40, f"Margen = {ordenes:.0f} órdenes ≥ 40")
    ok &= _check(psi_sigma > 0.999, f"Ψ_sigma = {psi_sigma:.4f} > 0.999")

    # Pilar B: Superradiancia de Agujeros Negros
    print("\n  Pilar B — Superradiancia de Agujeros Negros:")
    sr = SuperradianciaQCAL()
    m_bh_sol = sr.masa_bh_optima_solar()
    alpha = sr.parametro_gravitacional()
    cond_super = sr.condicion_superradiante_verificada()
    psi_sup = sr.coherencia_superfluido()

    print(f"    M_opt:             {m_bh_sol:.1f} M☉  (≈ 228 M☉ esperado)")
    print(f"    α = G·M·m_ψ/ℏc:  {alpha:.6f}  (debe ser ≤ 1)")
    print(f"    Condición α ≤ 1:  {cond_super}")
    print(f"    Ψ_superfluido:     {psi_sup:.4f}")

    ok &= _check(200 < m_bh_sol < 260, f"M_opt = {m_bh_sol:.0f} M☉ ∈ (200, 260) M☉")
    ok &= _check(cond_super, "α ≤ 1 (condición de átomo gravitacional)")
    ok &= _check(abs(alpha - 1.0) < 0.01, f"|α - 1| = {abs(alpha - 1.0):.2e} < 0.01")
    ok &= _check(psi_sup > 0.99, f"Ψ_superfluido = {psi_sup:.4f} > 0.99")

    # Pilar C: Superfluidez Cosmológica
    print("\n  Pilar C — Superfluidez Cosmológica:")
    sf = SuperfluidezCosmologica()
    xi_km = sf.xi_compton_km()
    ldb_m = sf.lambda_debroglie_m()
    macro = sf.escalas_macroscopicas()

    print(f"    ξ_Compton:         {xi_km:.1f} km  (≈ 337 km esperado)")
    print(f"    λ_deBroglie:       {ldb_m:.3e} m")
    print(f"    Escalas macro:     {macro}")

    ok &= _check(335 < xi_km < 339, f"ξ = {xi_km:.1f} km ∈ (335, 339) km")
    ok &= _check(ldb_m > 1e8, f"λ_dB = {ldb_m:.2e} m > 10⁸ m")
    ok &= _check(macro, "Escalas de coherencia macroscópicas verificadas")

    return ok


# ============================================================================
# Fase 4 — Coherencia Global del Tejido
# ============================================================================

def validar_fase4_coherencia() -> bool:
    """Valida la coherencia global Ψ_global ≥ 0.888 usando la API pública."""
    _section("FASE 4 — Coherencia Global  [Ψ_global ≥ 0.888  ∴MTQ∞³]")

    result = masa_tejido_cosmico_activar()

    psi_masa = result["psi_masa"]
    psi_lambda = result["psi_lambda"]
    psi_sigma = result["psi_sigma"]
    psi_sup = result["psi_superfluido"]
    psi_global = result["psi_global"]
    sobre_umbral = result["sobre_umbral"]
    mensaje = result["mensaje"]
    superf = result["superfluidez_garantizada"]

    print()
    print(f"  Ψ_masa:           {psi_masa:.4f}  (masa en régimen DM óptimo)")
    print(f"  Ψ_lambda:         {psi_lambda:.4f}  (acoplamiento Swampland válido)")
    print(f"  Ψ_sigma:          {psi_sigma:.4f}  (σ/m ≪ Bullet Cluster)")
    print(f"  Ψ_superfluido:    {psi_sup:.4f}  (masa BH óptima confirma superfluidez)")
    print()
    print(f"  Ψ_global:         {psi_global:.4f}  (media geométrica)")
    print(f"  Sobre umbral 0.888: {sobre_umbral}")
    print(f"  Superfluidez cosm.: {superf}")
    print()
    print(f"  Estado: {mensaje}")
    print()

    ok = True
    ok &= _check(psi_masa > 0.99,       f"Ψ_masa = {psi_masa:.4f} > 0.99")
    ok &= _check(psi_lambda > 0.999,    f"Ψ_lambda = {psi_lambda:.4f} > 0.999")
    ok &= _check(psi_sigma > 0.999,     f"Ψ_sigma = {psi_sigma:.4f} > 0.999")
    ok &= _check(psi_sup > 0.99,        f"Ψ_superfluido = {psi_sup:.4f} > 0.99")
    ok &= _check(psi_global >= 0.888,   f"Ψ_global = {psi_global:.4f} ≥ 0.888")
    ok &= _check(sobre_umbral,          "Sistema sobre el umbral de coherencia cósmica")
    ok &= _check(superf,                "Superfluidez cosmológica garantizada")
    ok &= _check("∴MTQ∞³" in mensaje or "TEJIDO" in mensaje,
                 "Mensaje contiene identificador ∴MTQ∞³ / TEJIDO")

    return ok


# ============================================================================
# Punto de entrada
# ============================================================================

def main() -> int:
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  MASA DEL TEJIDO CÓSMICO — Validación Completa  ∴MTQ∞³         ║")
    print("║  RAM-XLI-2026-MASA-TEJIDO-COSMICO  ·  F₀ = 141.7001 Hz        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    resultados = {
        "Fase 1 — Masa del Tejido": validar_fase1_masa(),
        "Fase 2 — Acoplamiento Swampland": validar_fase2_swampland(),
        "Fase 3 — Tres Pilares Exp.": validar_fase3_tres_pilares(),
        "Fase 4 — Coherencia Global": validar_fase4_coherencia(),
    }

    _section("RESUMEN FINAL")
    print()
    all_pass = True
    for fase, ok in resultados.items():
        estado = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {estado}  {fase}")
        all_pass &= ok

    print()
    if all_pass:
        print("  ✅ VALIDACIÓN COMPLETA — Masa del Tejido Cósmico ACTIVA  ∴MTQ∞³")
        print()
        return 0
    else:
        print("  ❌ VALIDACIÓN PARCIAL — Revisar fases con FAIL")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
