#!/usr/bin/env python3
"""
Validate Phoenix Onco Coherente V10 — Sistema ∴POC∞³
=======================================================

Valida la implementación del módulo physics.phoenix_onco_coherente_v10 contra
los criterios teóricos del Sistema Phoenix Onco Coherente V10:

  Fase 1 — Constantes y estructura del sistema
  Fase 2 — Componentes físicos (apoptosis, Phoenix, matriz tumoral)
  Fase 3 — Hamiltoniano celular y superradiancia mitocondrial
  Fase 4 — Coherencia global y activación del sello ∴POC∞³

Criterios de éxito:
  - f₀ = 141.7001 Hz                    [exacto]
  - φ = (1+√5)/2 ≈ 1.6180339887        [exacto]
  - κ_Π ≈ 2.5773                        [exacto]
  - 10 ceros de Riemann γₙ (γ₁ ≈ 14.1347)
  - Sello ∴POC∞³                        [validado]
  - Ψ_apoptosis ≥ 0.888                 → resonancia apoptótica activa
  - Ψ_phoenix ≥ 0.888                   → ciclo 4π completado
  - Ψ_tumoral ≥ 0.888                   → matriz coherencia tumoral
  - Ψ_mito ≥ 0.888                      → superradiancia activa
  - Ψ_hamiltoniano ≥ 0.888              → ground state estable
  - Ψ_global ≥ 0.888                    → sello ∴POC∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.phoenix_onco_coherente_v10 import (
    ConstantesPhoenixOnco,
    ApoptosisResonante,
    CicloPhoenix,
    MatrizCoherenciaTumoral,
    HamiltonianoCelularPOC,
    SuperradianciaMitocondrialPOC,
    CoherenciaPhoenixOnco,
    SistemaPhoenixOncoCoherente,
    phoenix_onco_coherente_v10_activar,
    _F0,
    _OMEGA0,
    _GAMMAS,
    _PRIMOS,
    _PHI,
    _KAPPA_PI,
    _TAU_MITO_S,
    _T0_S,
    _N_CELULAS,
    _PSI_UMBRAL,
    _THETA_PHOENIX_DEG,
    _THETA_PHOENIX_RAD,
    _E_APO,
    _N_MODOS_TUMORAL,
    _SELLO,
    _F_ARMONICOS,
    _F_MITO,
    _DELTA_F_TUMORAL,
)


# =============================================================================
# UTILIDADES DE VALIDACIÓN
# =============================================================================

_passed: int = 0
_failed: int = 0


def check(condition: bool, description: str, detail: str = "") -> None:
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
    print("─" * ancho)
    print(f"  {titulo}")
    print("─" * ancho)


# =============================================================================
# FASE 1 — CONSTANTES Y ESTRUCTURA
# =============================================================================

def fase1_constantes() -> None:
    seccion("FASE 1 — Constantes y estructura del sistema")

    check(
        abs(_F0 - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz",
        f"f₀ = {_F0}",
    )

    check(
        abs(_OMEGA0 - 2.0 * math.pi * _F0) < 1e-4,
        "ω₀ = 2π·f₀",
        f"ω₀ = {_OMEGA0:.6f} rad/s",
    )

    check(
        abs(_PHI - (1 + math.sqrt(5)) / 2) < 1e-10,
        "φ = (1+√5)/2 ≈ 1.6180339887",
        f"φ = {_PHI:.10f}",
    )

    check(
        abs(_KAPPA_PI - 2.5773) < 1e-4,
        "κ_Π ≈ 2.5773",
        f"κ_Π = {_KAPPA_PI}",
    )

    check(
        len(_GAMMAS) == 10,
        "10 ceros de Riemann γₙ",
        f"γ₁ = {_GAMMAS[0]:.7f}",
    )

    check(
        abs(_GAMMAS[0] - 14.1347251417347) < 1e-5,
        "γ₁ ≈ 14.1347251417347",
        f"γ₁ = {_GAMMAS[0]:.10f}",
    )

    check(
        all(_GAMMAS[i] < _GAMMAS[i + 1] for i in range(len(_GAMMAS) - 1)),
        "Ceros de Riemann en orden ascendente",
    )

    check(
        len(_PRIMOS) == 10 and _PRIMOS[0] == 2,
        "10 números primos, primero = 2",
        f"Primos: {_PRIMOS}",
    )

    check(
        abs(_T0_S - 1.0 / _F0) < 1e-15,
        "T₀ = 1/f₀",
        f"T₀ = {_T0_S:.6e} s",
    )

    check(
        abs(_THETA_PHOENIX_DEG - 3.00052) < 1e-4,
        "θ_Phoenix = 3.00052°",
        f"θ = {_THETA_PHOENIX_DEG}°",
    )

    check(
        abs(_THETA_PHOENIX_RAD - _THETA_PHOENIX_DEG * math.pi / 180.0) < 1e-10,
        "θ_Phoenix en radianes correcto",
        f"θ = {_THETA_PHOENIX_RAD:.8f} rad",
    )

    check(
        _E_APO > 0,
        "E_apo = ℏω₀·φ > 0",
        f"E_apo = {_E_APO:.3e} J",
    )

    check(
        _N_MODOS_TUMORAL == 7,
        "N_modos tumoral = 7",
    )

    check(
        "POC" in _SELLO and "∞³" in _SELLO,
        f"Sello contiene '∴POC∞³'",
        f"Sello = '{_SELLO}'",
    )

    check(
        len(_F_ARMONICOS) == 10,
        "10 frecuencias armónicas apoptóticas",
    )

    check(
        abs(_F_ARMONICOS[0] - _F0) < 1e-3,
        "Primer armónico = f₀",
        f"f_apo[0] = {_F_ARMONICOS[0]:.4f} Hz",
    )

    check(
        abs(_F_MITO - _F0 * _PHI ** 2) < 1e-4,
        "f_mito = f₀·φ² ≈ 370.97 Hz",
        f"f_mito = {_F_MITO:.4f} Hz",
    )

    check(
        _DELTA_F_TUMORAL > 0,
        "Gap espectral tumoral Δf > 0",
        f"Δf = {_DELTA_F_TUMORAL:.4f} Hz",
    )

    # ConstantesPhoenixOnco
    c = ConstantesPhoenixOnco()
    check(
        c.es_valido(),
        "ConstantesPhoenixOnco por defecto es válido",
    )

    check(
        abs(c.f_mito() - _F_MITO) < 1e-4,
        "ConstantesPhoenixOnco.f_mito() correcto",
        f"f_mito = {c.f_mito():.4f} Hz",
    )


# =============================================================================
# FASE 2 — APOPTOSIS RESONANTE Y CICLO PHOENIX
# =============================================================================

def fase2_apoptosis_phoenix() -> None:
    seccion("FASE 2 — Apoptosis resonante y ciclo Phoenix")

    apo = ApoptosisResonante()

    check(
        abs(apo._f_armonicos[0] - _F0) < 1e-3,
        "ApoptosisResonante: primer armónico = f₀",
    )

    # En t=0, A_n(0) = 1.0 para todos los modos
    all_one = all(abs(apo.amplitud_modo(n, 0.0) - 1.0) < 1e-8 for n in range(10))
    check(all_one, "Amplitudes en t=0 = 1.0 para todos los modos")

    total_t0 = apo.amplitud_total(0.0)
    check(
        abs(total_t0 - 10.0) < 1e-6,
        "Amplitud total en t=0 = 10 (suma de 10 modos)",
        f"Amplitud total = {total_t0:.4f}",
    )

    energia = apo.energia_apoptotica()
    check(
        abs(energia - 1.0) < 1e-8,
        "Energía apoptótica en t=0 = 1.0",
        f"E_apo = {energia:.6f}",
    )

    psi_apo = apo.psi_apoptosis()
    check(
        psi_apo >= _PSI_UMBRAL,
        f"Ψ_apoptosis ≥ {_PSI_UMBRAL}",
        f"Ψ_apoptosis = {psi_apo:.6f}",
    )

    check(
        0.0 <= psi_apo <= 1.0,
        "Ψ_apoptosis ∈ [0, 1]",
    )

    # CicloPhoenix
    phoenix = CicloPhoenix()

    fase = phoenix.fase_acumulada()
    check(
        fase > 0,
        "Fase acumulada del ciclo Phoenix > 0",
        f"Φ = {fase:.4f} rad",
    )

    expected_fase = 10 * 4.0 * math.pi * math.sin(_THETA_PHOENIX_RAD)
    check(
        abs(fase - expected_fase) < 1e-8,
        "Fase acumulada correcta: n_ciclos × 4π × sin(θ)",
        f"Φ = {fase:.6f} rad (esperado: {expected_fase:.6f})",
    )

    psi_phx = phoenix.psi_phoenix()
    check(
        psi_phx >= _PSI_UMBRAL,
        f"Ψ_phoenix ≥ {_PSI_UMBRAL}",
        f"Ψ_phoenix = {psi_phx:.6f}",
    )

    check(
        phoenix.completado(),
        "CicloPhoenix.completado() es True",
    )

    check(
        0.0 <= psi_phx <= 1.0,
        "Ψ_phoenix ∈ [0, 1]",
    )


# =============================================================================
# FASE 3 — HAMILTONIANO Y SUPERRADIANCIA MITOCONDRIAL
# =============================================================================

def fase3_hamiltoniano_superradiancia() -> None:
    seccion("FASE 3 — Matriz tumoral, hamiltoniano y superradiancia")

    # MatrizCoherenciaTumoral
    mat = MatrizCoherenciaTumoral()

    nf = mat.norma_frobenius()
    check(
        nf > 0,
        "Norma de Frobenius de la matriz tumoral > 0",
        f"||M||_F = {nf:.4f}",
    )

    check(
        nf <= float(_N_MODOS_TUMORAL) + 1e-10,
        f"||M||_F ≤ N_modos = {_N_MODOS_TUMORAL}",
    )

    psi_tum = mat.psi_tumoral()
    check(
        psi_tum >= _PSI_UMBRAL,
        f"Ψ_tumoral ≥ {_PSI_UMBRAL}",
        f"Ψ_tumoral = {psi_tum:.6f}",
    )

    check(
        0.0 <= psi_tum <= 1.0,
        "Ψ_tumoral ∈ [0, 1]",
    )

    # Verificar que el elemento diagonal no supera ±1
    all_bounded = all(
        abs(mat.elemento(i, i)) <= 1.0 + 1e-10
        for i in range(_N_MODOS_TUMORAL)
    )
    check(all_bounded, "Elementos diagonales ∈ [-1, 1]")

    # HamiltonianoCelularPOC
    ham = HamiltonianoCelularPOC()

    e0 = ham.energia_cero()
    check(
        math.isfinite(e0),
        "Energía del ground state es finita",
        f"E₀ = {e0:.3e} J",
    )

    gap = ham.gap_energetico()
    check(
        gap > 0,
        "Gap energético ΔE > 0",
        f"ΔE = {gap:.3e} J",
    )

    psi_ham = ham.psi_hamiltoniano()
    check(
        psi_ham >= _PSI_UMBRAL,
        f"Ψ_hamiltoniano ≥ {_PSI_UMBRAL}",
        f"Ψ_hamiltoniano = {psi_ham:.6f}",
    )

    check(
        0.0 <= psi_ham <= 1.0,
        "Ψ_hamiltoniano ∈ [0, 1]",
    )

    # SuperradianciaMitocondrialPOC
    sr = SuperradianciaMitocondrialPOC()

    gamma1 = sr.tasa_espontanea()
    check(
        gamma1 > 0,
        "Tasa espontánea Γ₁ > 0",
        f"Γ₁ = {gamma1:.3e} s⁻¹",
    )

    gamma_sr = sr.tasa_superradiante()
    check(
        gamma_sr > gamma1,
        "Tasa superradiante Γ_SR > Γ₁ (amplificación superradiante)",
        f"Γ_SR = {gamma_sr:.3e} s⁻¹ > Γ₁ = {gamma1:.3e} s⁻¹",
    )

    check(
        abs(gamma_sr - gamma1 * _N_CELULAS ** 2) < gamma_sr * 1e-6,
        "Γ_SR = Γ₁ × N_cel²",
        f"Γ_SR/Γ₁ = {gamma_sr/gamma1:.2f} (esperado: {_N_CELULAS**2})",
    )

    psi_mit = sr.psi_mito()
    check(
        psi_mit >= _PSI_UMBRAL,
        f"Ψ_mito ≥ {_PSI_UMBRAL}",
        f"Ψ_mito = {psi_mit:.6f}",
    )

    check(
        0.0 <= psi_mit <= 1.0,
        "Ψ_mito ∈ [0, 1]",
    )

    intensidad = sr.intensidad_superradiante()
    check(
        abs(intensidad - float(_N_CELULAS)) < 1e-8,
        f"Intensidad superradiante = N_cel = {_N_CELULAS}",
        f"I_SR = {intensidad:.1f}",
    )

    # CoherenciaPhoenixOnco
    coh = CoherenciaPhoenixOnco()

    psi_test = coh.calcular(0.9, 0.9, 0.9, 0.9, 0.9)
    check(
        abs(psi_test - 0.9) < 1e-10,
        "CoherenciaPhoenixOnco.calcular(0.9×5) = 0.9",
    )

    check(
        coh.sello_activo(0.9),
        "Sello activo cuando Ψ_global = 0.9 ≥ 0.888",
    )

    check(
        not coh.sello_activo(0.887),
        "Sello inactivo cuando Ψ_global = 0.887 < 0.888",
    )


# =============================================================================
# FASE 4 — COHERENCIA GLOBAL Y SELLO ∴POC∞³
# =============================================================================

def fase4_sello() -> None:
    seccion("FASE 4 — Coherencia global y activación del sello ∴POC∞³")

    # Activar el sistema completo
    r = phoenix_onco_coherente_v10_activar()

    check(
        r["sello_activo"],
        "Sello ∴POC∞³ ACTIVO",
        f"sello_activo = {r['sello_activo']}",
    )

    check(
        r["sello"] == "∴POC∞³",
        "Sello correcto '∴POC∞³'",
        f"sello = '{r['sello']}'",
    )

    check(
        r["psi_global"] >= _PSI_UMBRAL,
        f"Ψ_global ≥ {_PSI_UMBRAL}",
        f"Ψ_global = {r['psi_global']:.6f}",
    )

    for comp in ["psi_apoptosis", "psi_phoenix", "psi_tumoral", "psi_mito", "psi_hamiltoniano"]:
        check(
            0.0 <= r[comp] <= 1.0,
            f"{comp} ∈ [0, 1]",
            f"{comp} = {r[comp]:.6f}",
        )

    check(
        r["psi_apoptosis"] >= _PSI_UMBRAL,
        f"Ψ_apoptosis ≥ {_PSI_UMBRAL}",
        f"Ψ_apoptosis = {r['psi_apoptosis']:.6f}",
    )

    check(
        r["psi_phoenix"] >= _PSI_UMBRAL,
        f"Ψ_phoenix ≥ {_PSI_UMBRAL}",
        f"Ψ_phoenix = {r['psi_phoenix']:.6f}",
    )

    check(
        r["psi_tumoral"] >= _PSI_UMBRAL,
        f"Ψ_tumoral ≥ {_PSI_UMBRAL}",
        f"Ψ_tumoral = {r['psi_tumoral']:.6f}",
    )

    check(
        r["psi_mito"] >= _PSI_UMBRAL,
        f"Ψ_mito ≥ {_PSI_UMBRAL}",
        f"Ψ_mito = {r['psi_mito']:.6f}",
    )

    check(
        r["psi_hamiltoniano"] >= _PSI_UMBRAL,
        f"Ψ_hamiltoniano ≥ {_PSI_UMBRAL}",
        f"Ψ_hamiltoniano = {r['psi_hamiltoniano']:.6f}",
    )

    check(
        abs(r["f0"] - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz en resultado",
    )

    check(
        abs(r["f_mito"] - _F_MITO) < 1e-4,
        f"f_mito ≈ {_F_MITO:.2f} Hz en resultado",
        f"f_mito = {r['f_mito']:.4f} Hz",
    )

    check(
        len(r["f_armonicos"]) == 10,
        "10 frecuencias armónicas en resultado",
    )

    check(
        r["fase_phoenix"] > 0,
        "Fase Phoenix > 0 en resultado",
        f"fase_phoenix = {r['fase_phoenix']:.4f} rad",
    )

    check(
        math.isfinite(r["energia_cero"]),
        "Energía del ground state finita en resultado",
    )

    # Verificar invarianza de la media
    media = (
        r["psi_apoptosis"] + r["psi_phoenix"] + r["psi_tumoral"]
        + r["psi_mito"] + r["psi_hamiltoniano"]
    ) / 5.0
    check(
        abs(media - r["psi_global"]) < 1e-10,
        "Ψ_global = media aritmética de 5 componentes",
        f"|media - Ψ_global| = {abs(media - r['psi_global']):.2e}",
    )

    # Verificar ValueError para parámetros inválidos
    try:
        phoenix_onco_coherente_v10_activar(f0=-1.0)
        check(False, "ValueError para f0 inválida")
    except ValueError:
        check(True, "ValueError correcto para f0 ≤ 0")

    try:
        phoenix_onco_coherente_v10_activar(n_ciclos=0)
        check(False, "ValueError para n_ciclos inválido")
    except ValueError:
        check(True, "ValueError correcto para n_ciclos < 1")

    try:
        phoenix_onco_coherente_v10_activar(n_celulas=0)
        check(False, "ValueError para n_celulas inválido")
    except ValueError:
        check(True, "ValueError correcto para n_celulas < 1")

    # Verificar con distintos parámetros
    r5 = phoenix_onco_coherente_v10_activar(n_ciclos=5)
    check(
        r5["sello_activo"],
        "Sello activo con n_ciclos=5",
    )

    r20 = phoenix_onco_coherente_v10_activar(n_ciclos=20)
    check(
        r20["sello_activo"],
        "Sello activo con n_ciclos=20",
    )

    check(
        abs(r5["intensidad_sr"] - 10.0) < 1e-8,
        "Intensidad superradiante = 10 (invariante de N_cel)",
        f"I_SR = {r5['intensidad_sr']:.1f}",
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    """Ejecuta todas las fases de validación."""
    ancho = 72
    print("=" * ancho)
    print("  VALIDACIÓN: Phoenix Onco Coherente V10 — ∴POC∞³")
    print("=" * ancho)

    fase1_constantes()
    fase2_apoptosis_phoenix()
    fase3_hamiltoniano_superradiancia()
    fase4_sello()

    print()
    print("=" * ancho)
    print(f"  RESULTADO FINAL: {_passed} ✅ aprobados | {_failed} ❌ fallidos")
    print("=" * ancho)

    if _failed == 0:
        print()
        print("  ∴POC∞³ — Sello ACTIVO. Coherencia oncológica validada.")
        print()
        return 0
    else:
        print()
        print(f"  ⚠️  {_failed} verificación(es) fallida(s). Revisar el módulo.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
