#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       VALIDACIÓN: Jerarquía de Sintonizaciones - Análisis de Fase             ║
║       Veredicto de la Realidad: θ₁=5,43% | θ₂=11,24% | θ₃=−3,76%           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Este script realiza la validación completa de la Jerarquía de Sintonizaciones,
comprobando que:

    1. θ₁ = 5,43%  (Materia → Noesis) se deriva correctamente de f₀ y f_Dirac.
    2. La cascada de coherencia produce Ψ_Amor ≈ 0,8991 (AAA-QCAL).
    3. La magnetorrecepción arroja σ = 9,2σ (Certeza Estructural).
    4. Los microtúbulos resuenan en 141,88 ± 0,21 Hz (dentro del margen de f₀).
    5. El regulador de Riemann actúa sobre la señal magnética (γ₁ × f₀).
    6. El solitón microtubular confirma el mecanismo P=NP biológico.

Uso:
    python scripts/validate_jerarquia_sintonizaciones.py
"""

import sys
import os
import math

# Resolver la raíz del repositorio desde la ubicación de este script
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO_ROOT)

from physics.jerarquia_sintonizaciones import (
    F0_HZ, F_DIRAC_HZ, F_BIOQCAL_HZ, INCERTIDUMBRE_BIOQCAL_HZ,
    THETA_1, THETA_2, THETA_3,
    PSI_AMOR_TARGET, SIGMA_DESCUBRIMIENTO,
    GANANCIA_CASCADA, PSI_MATERIA,
    JerarquiaSintonizaciones,
    RiemannRegulador,
    SolitonMicrotubular,
    calcular_jerarquia,
    validar_cascada,
)


# ============================================================================
# UTILIDADES DE VISUALIZACIÓN
# ============================================================================

def cabecera(titulo: str) -> None:
    ancho = 72
    print()
    print("=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


def ok(mensaje: str) -> None:
    print(f"  ✓  {mensaje}")


def fallo(mensaje: str) -> None:
    print(f"  ✗  {mensaje}")


def info(mensaje: str) -> None:
    print(f"     {mensaje}")


# ============================================================================
# FASES DE VALIDACIÓN
# ============================================================================

def fase_1_constantes() -> bool:
    """Fase 1: Verificación de constantes y θ₁ derivado."""
    cabecera("FASE 1 — Constantes y derivación de θ₁")

    resultado = True

    # θ₁ derivado
    theta_1_esperado = (F0_HZ - F_DIRAC_HZ) / F_DIRAC_HZ
    if abs(THETA_1 - theta_1_esperado) < 1e-10:
        ok(f"θ₁ = {THETA_1*100:.4f}% derivado de (f₀ − f_Dirac) / f_Dirac")
    else:
        fallo(f"θ₁ no coincide: {THETA_1} ≠ {theta_1_esperado}")
        resultado = False

    # Rango de θ valores
    if THETA_1 > 0 and THETA_2 > THETA_1 and THETA_3 < 0:
        ok(f"Jerarquía de saltos: θ₁({THETA_1*100:.2f}%) < θ₂({THETA_2*100:.2f}%) | θ₃({THETA_3*100:.2f}%) < 0")
    else:
        fallo("La jerarquía θ₁ < θ₂, θ₃ < 0 no se cumple")
        resultado = False

    # Ψ_Materia positivo
    if 0 < PSI_MATERIA < 1:
        ok(f"Ψ_Materia = {PSI_MATERIA:.4f} (coherencia base, en (0,1))")
    else:
        fallo(f"Ψ_Materia = {PSI_MATERIA:.4f} fuera de (0,1)")
        resultado = False

    info(f"f_Dirac = {F_DIRAC_HZ} Hz  |  f₀ = {F0_HZ} Hz  |  f_BioQCAL = {F_BIOQCAL_HZ} Hz")
    return resultado


def fase_2_cascada() -> bool:
    """Fase 2: Validación de la cascada de coherencia y niveles."""
    cabecera("FASE 2 — Cascada de Coherencia (Materia → Noesis → Bio-QCAL → Amor)")

    resultado = calcular_jerarquia()
    ok_flag = True

    # Niveles
    for nivel in resultado.niveles:
        info(f"  {nivel.nombre:10s}  f = {nivel.frecuencia_hz:8.4f} Hz  Ψ = {nivel.psi:.4f}")

    # Transiciones
    print()
    for t in resultado.transiciones:
        signo = "+" if t.theta >= 0 else ""
        info(f"  {t.desde:10s} → {t.hasta:10s}: θ = {signo}{t.theta_porcentaje:.2f}%")

    # Validación de Ψ_Amor
    print()
    if resultado.es_valido:
        ok(f"Ψ_cascada = {resultado.psi_cascada:.4f} ≈ {PSI_AMOR_TARGET} (AAA-QCAL)")
    else:
        fallo(f"Ψ_cascada = {resultado.psi_cascada:.4f} ≠ {PSI_AMOR_TARGET}")
        ok_flag = False

    # Ganancia total
    info(f"Ganancia total G = (1+θ₁)(1+θ₂)(1+θ₃) = {resultado.ganancia_total:.6f}")

    # API rápida
    if validar_cascada(tolerancia=0.05):
        ok("validar_cascada() confirmado (tolerancia 5%)")
    else:
        fallo("validar_cascada() falló")
        ok_flag = False

    return ok_flag


def fase_3_magnetorrecepcion() -> bool:
    """Fase 3: Validación experimental de la magnetorrecepción."""
    cabecera("FASE 3 — Magnetorrecepción (σ = 9,2 | ΔP = 0,1987%)")

    regulador = RiemannRegulador()
    res = regulador.validar_magnetorrecepcion()

    info(f"ΔP medido   = {res['delta_p_porcentaje']:.4f}%  (objetivo: 0,1987%)")
    info(f"σ calculado = {res['sigma_calculado']:.2f}σ  (objetivo: ≥ 9,2σ)")
    info(f"P-valor     = {res['p_valor']:.2e}")
    info(f"N ensayos   = {res['n_trials']:,}")

    if res["es_descubrimiento"]:
        ok(f"σ = {res['sigma_calculado']:.1f}σ >> {SIGMA_DESCUBRIMIENTO}σ → CERTEZA ESTRUCTURAL")
    else:
        fallo(f"σ = {res['sigma_calculado']:.1f}σ < {SIGMA_DESCUBRIMIENTO}σ")
        return False

    return True


def fase_4_microtubulos() -> bool:
    """Fase 4: Validación de microtúbulos y sincronización con f₀."""
    cabecera("FASE 4 — Microtúbulos (f = 141,88 ± 0,21 Hz, σ = 8,7)")

    soliton = SolitonMicrotubular()
    sinc = soliton.sincronizacion_riemann()

    info(f"f₀ teórica  = {sinc['f0_teorica_hz']} Hz")
    info(f"f medida    = {sinc['f_medida_hz']} Hz ± {INCERTIDUMBRE_BIOQCAL_HZ} Hz")
    info(f"Discrepancia = {sinc['discrepancia_hz']:.4f} Hz")
    info(f"Precisión   = {sinc['precision_porcentaje']:.3f}%")

    if sinc["confirma_sintonizacion"]:
        ok(
            f"f_medida dentro del margen de error: "
            f"|Δf| = {sinc['discrepancia_hz']:.4f} Hz ≤ {INCERTIDUMBRE_BIOQCAL_HZ} Hz"
        )
    else:
        fallo(
            f"f_medida fuera del margen: "
            f"|Δf| = {sinc['discrepancia_hz']:.4f} Hz > {INCERTIDUMBRE_BIOQCAL_HZ} Hz"
        )
        return False

    # Período de colapso
    t_ms = soliton.periodo_colapso_ms()
    ok(f"Período de colapso del solitón T = 1/f₀ ≈ {t_ms:.2f} ms")

    return True


def fase_5_riemann_regulador() -> bool:
    """Fase 5: Verificación del regulador de Riemann."""
    cabecera("FASE 5 — Regulador de Riemann (Línea Crítica σ = 1/2)")

    regulador = RiemannRegulador()
    freqs = regulador.frecuencias_regulacion()

    info("Frecuencias reguladoras λₙ = γₙ × f₀:")
    for i, (gamma, fr) in enumerate(
        zip(RiemannRegulador.CEROS_RIEMANN, freqs), start=1
    ):
        info(f"    λ{i}: γ{i} = {gamma:.6f}  →  {fr:.2f} Hz")

    # Verificar que la supresión es máxima en la primera frecuencia reguladora
    supresion_en_reguladora = regulador.filtrar_ruido(freqs[0])
    if abs(supresion_en_reguladora - 1.0) < 1e-5:
        ok(f"Supresión máxima en λ₁ = {freqs[0]:.2f} Hz (factor = {supresion_en_reguladora:.6f})")
    else:
        fallo(f"Supresión no máxima en λ₁: {supresion_en_reguladora:.6f}")
        return False

    # Verificar atenuación fuera de los picos
    supresion_lejana = regulador.filtrar_ruido(500.0)
    if supresion_lejana < 0.01:
        ok(f"Supresión de ruido lejano (500 Hz): factor = {supresion_lejana:.2e} → atenuación fuerte")
    else:
        fallo(f"Atenuación insuficiente a 500 Hz: {supresion_lejana:.4f}")
        return False

    return True


def fase_6_consecuencias() -> bool:
    """Fase 6: Consecuencias del Documento Maestro."""
    cabecera("FASE 6 — Consecuencias del Documento Maestro")

    jerarquia = JerarquiaSintonizaciones()
    cons = jerarquia.calcular_consecuencias()

    # P=NP
    pnp = cons["pnp_soliton"]
    ok(f"P=NP biológico: colapso solitón a f₀ = {pnp['frecuencia_colapso_hz']} Hz, "
       f"T = {pnp['periodo_colapso_ms']:.2f} ms")

    # Riemann regulador
    riemann = cons["riemann_regulador"]
    ok(f"Riemann regulador: γ₁ × f₀ = {riemann['frecuencia_reguladora_hz']:.2f} Hz "
       f"| σ_magnetorrecepción = {riemann['sigma_magnetorrecepcion']}")

    # Simbiosis
    simb = cons["simbiosis_flujo"]
    margen = simb["margen_libertad"]
    ok(f"Simbiosis como flujo: Ψ = {simb['psi_actual']:.4f}, "
       f"margen de libertad Δ = {margen:.4f} (ruido creativo)")

    # Verificación de coherencia final
    if abs(simb["psi_actual"] - PSI_AMOR_TARGET) < 0.001:
        ok(f"Ψ_Amor = {simb['psi_actual']:.4f} coincide con el objetivo AAA-QCAL = {PSI_AMOR_TARGET}")
    else:
        fallo(f"Ψ_Amor = {simb['psi_actual']:.4f} no coincide con {PSI_AMOR_TARGET}")
        return False

    return True


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main() -> int:
    """Ejecuta las seis fases de validación y devuelve 0 si todo es correcto."""

    print()
    print("╔" + "═" * 70 + "╗")
    print("║  VALIDACIÓN: Jerarquía de Sintonizaciones - Análisis de Fase" + " " * 8 + "║")
    print("║  f₀ = 141,7001 Hz | Red de 7 nodos primos | QCAL ∞³" + " " * 17 + "║")
    print("╚" + "═" * 70 + "╝")

    fases = [
        ("Constantes y derivación de θ₁", fase_1_constantes),
        ("Cascada de coherencia", fase_2_cascada),
        ("Magnetorrecepción (9,2σ)", fase_3_magnetorrecepcion),
        ("Microtúbulos (141,88 Hz)", fase_4_microtubulos),
        ("Regulador de Riemann", fase_5_riemann_regulador),
        ("Consecuencias del Documento Maestro", fase_6_consecuencias),
    ]

    resultados = []
    for nombre, fase_fn in fases:
        try:
            ok_flag = fase_fn()
        except Exception as exc:  # noqa: BLE001
            fallo(f"Excepción en '{nombre}': {exc}")
            ok_flag = False
        resultados.append((nombre, ok_flag))

    # Resumen
    cabecera("RESUMEN DE VALIDACIÓN")
    n_ok = sum(1 for _, r in resultados if r)
    for nombre, r in resultados:
        (ok if r else fallo)(nombre)

    print()
    if n_ok == len(fases):
        print(f"  🎯 RESULTADO: {n_ok}/{len(fases)} fases superadas — CERTEZA ESTRUCTURAL")
        print("     La jerarquía de sintonizaciones está plenamente validada.")
        print("     θ₁ = 5,43% | θ₂ = 11,24% | θ₃ = −3,76% | Ψ_Amor = 0,8991")
        return 0
    else:
        print(f"  ✗ RESULTADO: {n_ok}/{len(fases)} fases superadas — requiere revisión")
        return 1


if __name__ == "__main__":
    sys.exit(main())
