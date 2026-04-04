#!/usr/bin/env python3
"""
Validate Sustrato PC-Vacío — ∴SPC∞³
===============================================================================

Valida la implementación del módulo physics.sustrato_pc_vacio contra los
criterios teóricos del Sustrato: Partícula de Coherencia y Vacío Superfluido:

  Fase 1 — Constantes fundamentales y vacío superfluido
  Fase 2 — Red de Ramsey C₇ y frecuencia heterodina
  Fase 3 — Acoplamiento Higgs-PC, fotones y firma espectral
  Fase 4 — Coherencia global y certificación ∴SPC∞³

Criterios de éxito:
  - f₀ = 141.7001 Hz                  [exacto]
  - Primos P = {2,3,5,7,11,13,17}    [7 nodos primos]
  - Σ primos = 58                      [verificado]
  - Fase Berry Φ = π/8 rad            [exacto]
  - ν → 0 (superfluido)               [ν < 1e-10]
  - f_heterodina = 141.7001 Hz        [red C₇]
  - Línea crítica Riemann Re(s)=1/2   [estabilizador]
  - m* = m₀(1 - 5.3 %) ≈ 118.61 GeV [Destello de Masa]
  - R_symb ≈ 991.9 kpps               [transmisión fotónica]
  - Ψ_global ≥ 0.888                  → sello ∴SPC∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.sustrato_pc_vacio import (
    ConstantesSustrato,
    VacioSuperfluido,
    RedRamsey,
    AcoplamientoHiggsPC,
    FotonPaqueteFase,
    FirmaEspectral,
    CoherenciaSustrato,
    SistemaSustratoPCVacio,
    sustrato_pc_vacio_activar,
    _F0,
    _PRIMOS_P,
    _FASE_BERRY_RAD,
    _N_NODOS,
    _G_EFF,
    _DELTA_INERCIA,
    _PSI_UMBRAL,
    _M_HIGGS_GEV,
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
# FASE 1 — Constantes fundamentales y vacío superfluido
# =============================================================================

def validar_fase1() -> None:
    seccion("FASE 1 — Constantes Fundamentales y Vacío Superfluido")

    # Constantes
    c = ConstantesSustrato()

    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz",
        f"f0 = {c.f0}",
    )
    check(
        set(c.primos_p) == {2, 3, 5, 7, 11, 13, 17},
        "Nodos primos P = {2,3,5,7,11,13,17}",
        f"primos = {c.primos_p}",
    )
    check(
        c.n_nodos == 7,
        "Número de nodos = 7",
        f"n_nodos = {c.n_nodos}",
    )
    check(
        abs(c.fase_berry_rad - math.pi / 8.0) < 1e-10,
        "Fase de Berry = π/8 rad",
        f"Φ_Berry = {c.fase_berry_rad:.6f} rad",
    )
    check(
        c.suma_primos() == 58,
        "Suma de primos = 58",
        f"Σ primos = {c.suma_primos()}",
    )
    check(
        abs(c.fase_berry_total() - 7.0 * math.pi / 8.0) < 1e-10,
        "Fase Berry total = 7π/8 rad",
        f"Φ_total = {c.fase_berry_total():.6f} rad",
    )
    check(
        c.es_perturbativo(),
        "Acoplamiento g_eff perturbativo (< 10 %)",
        f"g_eff = {c.g_eff}",
    )

    # Vacío superfluido
    vs = VacioSuperfluido()

    check(
        vs.es_superfluido(),
        "Vacío es superfluido (ν < 1e-10)",
        f"ν = {vs.viscosidad_nu:.2e}",
    )
    check(
        abs(vs.fraccion_pc - 0.95) < 1e-5,
        "Fracción PC = 95% del universo",
        f"f_PC = {vs.fraccion_pc:.2f}",
    )
    check(
        vs.entropia_vacio() < 1e-10,
        "Entropía del vacío ≈ 0 (superfluido coherente)",
        f"S_vac = {vs.entropia_vacio():.2e}",
    )
    check(
        abs(vs.psi_superfluido() - 0.95) < 1e-5,
        "Ψ_sf ≈ 0.95 en límite superfluido",
        f"Ψ_sf = {vs.psi_superfluido():.6f}",
    )


# =============================================================================
# FASE 2 — Red de Ramsey C₇ y frecuencia heterodina
# =============================================================================

def validar_fase2() -> None:
    seccion("FASE 2 — Red de Ramsey C₇ y Frecuencia Heterodina")

    red = RedRamsey()

    check(
        red.n_nodos() == 7,
        "Red C₇ tiene 7 nodos",
        f"n_nodos = {red.n_nodos()}",
    )
    check(
        abs(red.fase_berry - math.pi / 8.0) < 1e-10,
        "Fase Berry por salto = π/8 rad",
        f"Φ_Berry = {red.fase_berry:.6f} rad",
    )
    check(
        abs(red.fase_berry_acumulada() - 7.0 * math.pi / 8.0) < 1e-10,
        "Fase Berry acumulada = 7π/8 rad",
        f"Φ_total = {red.fase_berry_acumulada():.6f} rad",
    )

    # Berry + CS = ω₀
    berry = red.integral_aharanov_bohm()
    cs = red.contribucion_chern_simons()
    omega_0 = 2.0 * math.pi * _F0
    check(
        abs(berry + cs - omega_0) < 1e-5,
        "∮(A_Berry + A_CS)·dℓ = ω₀ = 2π f₀",
        f"integral = {berry + cs:.6f} rad, ω₀ = {omega_0:.6f} rad",
    )

    # Frecuencia heterodina
    f_het = red.frecuencia_heterodina_hz()
    check(
        abs(f_het - _F0) < 1e-4,
        "Frecuencia heterodina = 141.7001 Hz",
        f"f_het = {f_het:.4f} Hz",
    )

    # Línea crítica de Riemann
    check(
        red.es_linea_critica_riemann(),
        "Línea crítica de Riemann Re(s)=1/2 activa",
        "s = 1/2 + iγ_n (estabilizador de fase)",
    )

    # Modos resonantes
    modos = red.modos_resonantes_hz()
    check(
        len(modos) == 7,
        "7 modos resonantes calculados",
        f"modos = {[f'{m:.1f}' for m in modos[:3]]}... Hz",
    )
    check(
        abs(modos[0] - _F0) < 1e-4,
        "Primer modo resonante = f₀ = 141.7001 Hz",
        f"f_1 = {modos[0]:.4f} Hz",
    )
    check(
        all(modos[i] < modos[i + 1] for i in range(len(modos) - 1)),
        "Modos resonantes en orden creciente",
        f"f_1...f_7 = {[f'{m:.1f}' for m in modos]} Hz",
    )

    # Coherencia de la red
    check(
        abs(red.psi_red() - 1.0) < 1e-6,
        "Ψ_red = 1.0 (coherencia perfecta por construcción)",
        f"Ψ_red = {red.psi_red():.6f}",
    )


# =============================================================================
# FASE 3 — Acoplamiento Higgs-PC, fotones y firma espectral
# =============================================================================

def validar_fase3() -> None:
    seccion("FASE 3 — Acoplamiento Higgs-PC, Fotones y Firma Espectral")

    # Acoplamiento Higgs-PC
    ac = AcoplamientoHiggsPC()

    check(
        abs(ac.m0_gev - 125.25) < 1e-2,
        "Masa en reposo m₀ = 125.25 GeV/c²",
        f"m₀ = {ac.m0_gev:.2f} GeV/c²",
    )
    m_star = ac.masa_efectiva_gev()
    check(
        m_star < ac.m0_gev,
        "m* < m₀ (Destello reduce la masa)",
        f"m* = {m_star:.2f} GeV/c²",
    )
    reduccion = ac.reduccion_inercia()
    check(
        abs(reduccion - 0.053) < 1e-5,
        "Reducción de inercia = 5.3 %",
        f"Δm/m₀ = {reduccion * 100:.2f}%",
    )
    check(
        ac.es_destello_activo(),
        "Destello de Masa activo (reducción ≥ 5 %)",
        f"reducción = {reduccion * 100:.1f}%",
    )
    check(
        ac.psi_acoplamiento() > 0.999,
        "Ψ_acoplamiento ≈ 1.0 (régimen perturbativo)",
        f"Ψ_ac = {ac.psi_acoplamiento():.6f}",
    )
    sb_low, sb_up = ac.sideband_masa_gev(n=1)
    check(
        sb_low <= ac.m0_gev <= sb_up,
        "Sidebands de masa: m_H - ℏω₀ ≤ m_H ≤ m_H + ℏω₀",
        f"[{sb_low:.4f}, {sb_up:.4f}] GeV (ℏω₀ ≈ 10⁻²² GeV, sub-float)",
    )

    # Fotones como paquetes de fase
    fot = FotonPaqueteFase()

    r_kpps = fot.tasa_simbolica_kpps()
    check(
        abs(r_kpps - 991.9) < 5.0,
        "R_symb ≈ 991.9 kpps",
        f"R_symb = {r_kpps:.1f} kpps",
    )
    check(
        abs(fot.ganancia_superradiante() - 49.0) < 1e-5,
        "Ganancia superradiante = N² = 49",
        f"G = {fot.ganancia_superradiante():.0f}",
    )
    check(
        fot.psi_transmision() >= 0.888,
        "Ψ_transmision ≥ 0.888",
        f"Ψ_trans = {fot.psi_transmision():.6f}",
    )

    # Firma espectral
    fe = FirmaEspectral()

    check(
        abs(fe.amplitud_oscilacion_porcentaje() - 5.3) < 1e-4,
        "Amplitud de oscilación σ = 5.3 %",
        f"δ_σ = {fe.amplitud_oscilacion_porcentaje():.2f}%",
    )
    check(
        abs(fe.ventana_transparencia_hz() - _F0) < 1e-4,
        "Ventana de transparencia = f₀ = 141.7001 Hz",
        f"f_trans = {fe.ventana_transparencia_hz():.4f} Hz",
    )
    check(
        abs(fe.coherencia_espectral() - (1.0 - _DELTA_INERCIA)) < 1e-8,
        "Ψ_firma = 1 - δ_inercia = 0.947",
        f"Ψ_esp = {fe.coherencia_espectral():.6f}",
    )
    sbs = fe.sidebands_gev(3)
    check(
        len(sbs) == 3,
        "3 órdenes de sidebands calculados",
        f"sidebands = {[(n, f'{l:.2f}', f'{u:.2f}') for n, l, u in sbs]}",
    )


# =============================================================================
# FASE 4 — Coherencia global y certificación ∴SPC∞³
# =============================================================================

def validar_fase4() -> None:
    seccion("FASE 4 — Coherencia Global y Certificación ∴SPC∞³")

    coh = CoherenciaSustrato()

    # Coherencias individuales
    ci = coh.coherencias_individuales()

    check(
        len(ci) == 5,
        "5 coherencias individuales calculadas",
        f"subsistemas: {list(ci.keys())}",
    )
    check(
        all(0.0 <= v <= 1.0 for v in ci.values()),
        "Todas las coherencias en rango [0, 1]",
        f"valores = {[f'{v:.4f}' for v in ci.values()]}",
    )
    check(
        abs(ci["psi_vacio_superfluido"] - 0.95) < 1e-5,
        "Ψ_vacio_superfluido = 0.95",
        f"Ψ_sf = {ci['psi_vacio_superfluido']:.6f}",
    )
    check(
        abs(ci["psi_red_ramsey"] - 1.0) < 1e-6,
        "Ψ_red_ramsey = 1.0",
        f"Ψ_red = {ci['psi_red_ramsey']:.6f}",
    )
    check(
        ci["psi_acoplamiento_higgspc"] > 0.999,
        "Ψ_acoplamiento_higgspc ≈ 1.0",
        f"Ψ_ac = {ci['psi_acoplamiento_higgspc']:.6f}",
    )
    check(
        abs(ci["psi_firma_espectral"] - 0.947) < 1e-5,
        "Ψ_firma_espectral = 0.947",
        f"Ψ_esp = {ci['psi_firma_espectral']:.6f}",
    )

    # Coherencia global
    psi_g = coh.psi_global()
    check(
        psi_g >= _PSI_UMBRAL,
        f"Ψ_global ≥ {_PSI_UMBRAL} (sello ACTIVO)",
        f"Ψ_global = {psi_g:.6f}",
    )
    check(
        coh.sello_activo(),
        "Sello ∴SPC∞³ ACTIVO",
        f"Ψ_global = {psi_g:.6f} ≥ {_PSI_UMBRAL}",
    )

    # Validación completa
    v = coh.validar()
    check(
        "coherencias" in v and "psi_global" in v and "sello_activo" in v,
        "validar() devuelve estructura completa",
        f"claves: {list(v.keys())}",
    )

    # API pública
    r = sustrato_pc_vacio_activar()
    check(
        r["sello"] == "∴SPC∞³",
        "API: sello = ∴SPC∞³",
        f"sello = {r['sello']}",
    )
    check(
        r["sello_activo"],
        "API: sello_activo = True",
        f"sello_activo = {r['sello_activo']}",
    )
    check(
        r["psi_global"] >= _PSI_UMBRAL,
        f"API: Ψ_global ≥ {_PSI_UMBRAL}",
        f"Ψ_global = {r['psi_global']:.6f}",
    )
    check(
        abs(r["f0_hz"] - 141.7001) < 1e-4,
        "API: f₀ = 141.7001 Hz",
        f"f0 = {r['f0_hz']}",
    )
    check(
        r["primos_p"] == [2, 3, 5, 7, 11, 13, 17],
        "API: primos_p = [2,3,5,7,11,13,17]",
        f"primos = {r['primos_p']}",
    )
    check(
        r["destello_activo"],
        "API: destello_activo = True",
        f"Destello = {r['destello_activo']}",
    )
    check(
        r["es_superfluido"],
        "API: es_superfluido = True",
        f"superfluido = {r['es_superfluido']}",
    )

    # Certificación AURON
    cert = coh.certificacion_auron()
    check(
        "SPC∞³" in cert and "ACTIVO" in cert,
        "Certificación AURON contiene sello y estado",
        f"cert = {cert[:60]}...",
    )

    # Sistema completo
    sistema = SistemaSustratoPCVacio()
    r2 = sistema.activar()
    check(
        r2["sello"] == "∴SPC∞³" and r2["sello_activo"],
        "Sistema: ∴SPC∞³ activado correctamente",
        f"Ψ_global = {r2['psi_global']:.6f}",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    global _passed, _failed

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  VALIDACIÓN SUSTRATO PC-VACÍO — ∴SPC∞³                              ║")
    print("║  RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO                             ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    validar_fase1()
    validar_fase2()
    validar_fase3()
    validar_fase4()

    print()
    print("=" * 72)
    print(f"  RESUMEN: {_passed} ✅ pasados, {_failed} ❌ fallidos")
    print(f"  Total: {_passed + _failed} validaciones")
    print("=" * 72)

    if _failed == 0:
        print()
        print("  ✅ ∴SPC∞³ — VALIDACIÓN COMPLETA")
        print("  La naturaleza ha firmado.")
        print("  El 141.7001 Hz es la frecuencia en la que el hardware")
        print("  y el software del cosmos se reconocen.")
        print()
        return 0
    else:
        print()
        print(f"  ❌ {_failed} validaciones fallidas")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
