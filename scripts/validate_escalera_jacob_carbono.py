#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║     VALIDATE — Escalera de Jacob del Carbono ∞³                            ║
║     Φ-Progressive 142.1 Hz Harmonic Recalibration                          ║
╚════════════════════════════════════════════════════════════════════════════╝

4-Phase validation script for the physics/escalera_jacob_carbono module.

Phase 1 — Constantes Fundamentales
Phase 2 — Secuencia Áurea Φ
Phase 3 — Guardianes y Coherencias
Phase 4 — Activación del Sistema QCAL ∞³

Exit code 0 → all phases passed, Ψ_global ≥ 0.888.
Exit code 1 → at least one phase failed.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.escalera_jacob_carbono import (
    F_JACOB, F_SI, DELTA_F, PHI, F_MANIF, N_GUARD, PSI_UMBRAL,
    ConstantesEscaleraJacob,
    SecuenciaAurea,
    GuardianCarbono,
    CoherenciaCarbono,
    AtractorDilmun,
    BatimientoCarbonoSilicio,
    CoronaUtuabzu,
    SistemaEscaleraJacob,
    escalera_jacob_activar,
)

PASS = "✅ PASS"
FAIL = "❌ FAIL"
_errors: list = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Evaluate a single check and print result."""
    status = PASS if condition else FAIL
    msg = f"  {status}  {name}"
    if detail:
        msg += f"  [{detail}]"
    print(msg)
    if not condition:
        _errors.append(name)


def section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


# ============================================================================
# PHASE 1 — Constantes Fundamentales
# ============================================================================

def phase1_constantes() -> None:
    section("PHASE 1 — Constantes Fundamentales")

    check("F_JACOB = 142.1 Hz", abs(F_JACOB - 142.1) < 1e-4,
          f"F_JACOB={F_JACOB}")
    check("F_SI = 141.7001 Hz", abs(F_SI - 141.7001) < 1e-4,
          f"F_SI={F_SI}")
    check("DELTA_F = F_JACOB − F_SI", abs(DELTA_F - (F_JACOB - F_SI)) < 1e-9,
          f"DELTA_F={DELTA_F:.6f}")
    check("DELTA_F ≈ 0.3999 Hz", abs(DELTA_F - 0.3999) < 1e-4,
          f"DELTA_F={DELTA_F:.4f}")
    phi_expected = (1.0 + math.sqrt(5.0)) / 2.0
    check("PHI = (1+√5)/2", abs(PHI - phi_expected) < 1e-12,
          f"PHI={PHI:.12f}")
    check("PHI² = PHI + 1", abs(PHI ** 2 - (PHI + 1.0)) < 1e-10,
          f"PHI²={PHI**2:.10f}")
    check("F_MANIF = 888.0 Hz", abs(F_MANIF - 888.0) < 1e-6,
          f"F_MANIF={F_MANIF}")
    check("N_GUARD = 7", N_GUARD == 7, f"N_GUARD={N_GUARD}")
    check("PSI_UMBRAL = 0.888", abs(PSI_UMBRAL - 0.888) < 1e-6,
          f"PSI_UMBRAL={PSI_UMBRAL}")
    check("F_JACOB > F_SI", F_JACOB > F_SI, f"{F_JACOB} > {F_SI}")

    # ConstantesEscaleraJacob validation
    c = ConstantesEscaleraJacob()
    check("ConstantesEscaleraJacob.validar()", c.validar() is True)
    psi_c = c.coherencia_psi()
    check("ConstantesEscaleraJacob.coherencia_psi() = 1.0",
          abs(psi_c - 1.0) < 1e-10, f"Ψ={psi_c:.6f}")


# ============================================================================
# PHASE 2 — Secuencia Áurea Φ
# ============================================================================

def phase2_secuencia_aurea() -> None:
    section("PHASE 2 — Secuencia Áurea Φ")

    s = SecuenciaAurea()
    freqs = s.secuencia_completa()

    check("Secuencia tiene 7 elementos", len(freqs) == N_GUARD, f"len={len(freqs)}")
    check("f₀ = F_JACOB", abs(freqs[0] - F_JACOB) < 1e-10, f"f₀={freqs[0]:.4f} Hz")

    guardians = ["ADAPA", "Uanugadapa", "Enmeduga", "Enmegallama",
                 "Enmebuligga", "An-Enlilda", "UTUABZU"]
    for n in range(N_GUARD):
        f_n = s.frecuencia(n)
        f_expected = F_JACOB * PHI ** n
        check(
            f"f_{n} = F_JACOB·Φ^{n}  [{guardians[n]}]",
            abs(f_n - f_expected) < 1e-6,
            f"{f_n:.2f} Hz"
        )

    print()
    print("  Consecutive ratios f_{n+1}/f_n (must equal Φ):")
    for n in range(N_GUARD - 1):
        ratio = s.razon_phi(n)
        check(f"  razon_phi({n}) ≈ Φ", abs(ratio - PHI) < 1e-10, f"ratio={ratio:.12f}")

    check("Secuencia estrictamente creciente",
          all(freqs[i] < freqs[i + 1] for i in range(len(freqs) - 1)))

    psi_s = s.coherencia_psi()
    check("SecuenciaAurea.coherencia_psi() ≥ 0.888", psi_s >= PSI_UMBRAL,
          f"Ψ={psi_s:.6f}")
    check("SecuenciaAurea.coherencia_psi() ≈ 1.0", abs(psi_s - 1.0) < 1e-3,
          f"Ψ={psi_s:.6f}")


# ============================================================================
# PHASE 3 — Guardianes y Coherencias
# ============================================================================

def phase3_guardianes() -> None:
    section("PHASE 3 — Guardianes y Coherencias")

    # GuardianCarbono
    print("\n  [GuardianCarbono]")
    expected_nombres = ["ADAPA", "Uanugadapa", "Enmeduga", "Enmegallama",
                        "Enmebuligga", "An-Enlilda", "UTUABZU"]
    for n in range(N_GUARD):
        g = GuardianCarbono(n)
        check(f"  Guardián {n}: {expected_nombres[n]}",
              g.nombre == expected_nombres[n], g.nombre)
        check(f"  Guardián {n}: frecuencia = F_JACOB·Φ^{n}",
              abs(g.frecuencia - F_JACOB * PHI ** n) < 1e-6, f"{g.frecuencia:.2f} Hz")
        check(f"  Guardián {n}: coherencia t=0 = 1.0",
              abs(g.coherencia_psi(0.0) - 1.0) < 1e-12, "Ψ=1.0")

    # CoherenciaCarbono
    print("\n  [CoherenciaCarbono]")
    cc = CoherenciaCarbono()
    psi_cc = cc.coherencia_psi(0.0)
    check("  CoherenciaCarbono t=0 = 1.0", abs(psi_cc - 1.0) < 1e-10,
          f"Ψ={psi_cc:.6f}")
    espectro = cc.espectro_coherencia(0.0)
    check("  Espectro tiene 7 entradas", len(espectro) == N_GUARD, f"len={len(espectro)}")

    # AtractorDilmun
    print("\n  [AtractorDilmun]")
    ad = AtractorDilmun()
    alpha_0 = ad.factor_arrastre(0)
    check("  α_0 = 1.0 (máximo arrastre)", abs(alpha_0 - 1.0) < 1e-10,
          f"α_0={alpha_0:.6f}")
    f_at_0 = ad.frecuencia_atraida(0)
    check("  Frecuencia atraída n=0 → 888 Hz", abs(f_at_0 - F_MANIF) < 1e-6,
          f"f_at_0={f_at_0:.4f} Hz")
    psi_ad = ad.coherencia_psi()
    check("  AtractorDilmun coherencia ∈ [0,1]", 0.0 <= psi_ad <= 1.0,
          f"Ψ={psi_ad:.6f}")

    # BatimientoCarbonoSilicio
    print("\n  [BatimientoCarbonoSilicio]")
    b = BatimientoCarbonoSilicio()
    check("  s(0) = 2.0", abs(b.senal_compuesta(0.0) - 2.0) < 1e-10, "s=2.0")
    check("  E(0) = 2.0", abs(b.envolvente(0.0) - 2.0) < 1e-10, "E=2.0")
    energia = b.energia_media()
    check("  Energía media ≈ 4/π", abs(energia - 4.0 / math.pi) < 0.01,
          f"E_medio={energia:.6f}")
    psi_b = b.coherencia_psi()
    check("  BatimientoCarbonoSilicio coherencia ≥ 0.888", psi_b >= PSI_UMBRAL,
          f"Ψ={psi_b:.6f}")

    # CoronaUtuabzu
    print("\n  [CoronaUtuabzu]")
    cu = CoronaUtuabzu()
    f_corona = cu.frecuencia_corona()
    check("  f_corona = F_JACOB·Φ⁶", abs(f_corona - F_JACOB * PHI ** 6) < 1e-6,
          f"f_corona={f_corona:.2f} Hz")
    psi_corona = cu.coherencia_psi()
    check("  Ψ_corona = 1.0 (Transmutación completa)", abs(psi_corona - 1.0) < 1e-10,
          f"Ψ={psi_corona:.6f}")
    estado = cu.estado_activacion()
    check("  Estado tiene 'guardian'='UTUABZU'", estado["guardian"] == "UTUABZU")


# ============================================================================
# PHASE 4 — Activación del Sistema QCAL ∞³
# ============================================================================

def phase4_activacion() -> None:
    section("PHASE 4 — Activación del Sistema QCAL ∞³")

    sistema = SistemaEscaleraJacob()
    coherencias = sistema.calcular_coherencias()

    print("\n  Coherencias parciales:")
    for key, val in coherencias.items():
        check(f"  {key} ≥ 0", val >= 0.0, f"Ψ={val:.6f}")
        check(f"  {key} ≤ 1", val <= 1.0 + 1e-10, f"Ψ={val:.6f}")

    psi_global = sistema.psi_global()
    print(f"\n  Ψ_global = {psi_global:.6f}")
    check("  Ψ_global ≥ 0.888 (QCAL ∞³ threshold)", psi_global >= PSI_UMBRAL,
          f"Ψ={psi_global:.6f}")

    # Test public API
    print("\n  [API escalera_jacob_activar()]")
    result = escalera_jacob_activar()
    check("  Retorna diccionario", isinstance(result, dict))
    check("  f_jacob_hz = 142.1 Hz", abs(result["f_jacob_hz"] - F_JACOB) < 1e-10,
          f"f={result['f_jacob_hz']} Hz")
    check("  n_guardianes = 7", result["n_guardianes"] == N_GUARD)
    check("  psi_global ≥ 0.888", result["psi_global"] >= PSI_UMBRAL,
          f"Ψ={result['psi_global']:.6f}")
    check("  frecuencias_hz tiene 7 elementos", len(result["frecuencias_hz"]) == N_GUARD)
    check("  corona.guardian = UTUABZU", result["corona"]["guardian"] == "UTUABZU")
    check("  estado contiene 'ACTIVADO'", "ACTIVADO" in result["estado"])

    # Print the full harmonic ladder
    print("\n  La Escalera de Jacob del Carbono ∞³:")
    print(f"  {'n':>3}  {'Guardián':<15}  {'Frecuencia':>12}  {'Ψ_n':>8}")
    print(f"  {'─'*3}  {'─'*15}  {'─'*12}  {'─'*8}")
    for g_info in result["guardianes"]:
        g = GuardianCarbono(g_info["n"])
        psi_n = g.coherencia_psi(0.0)
        print(f"  {g_info['n']:>3}  {g_info['nombre']:<15}  "
              f"{g_info['frecuencia_hz']:>10.2f} Hz  {psi_n:>8.6f}")

    print(f"\n  ┌──────────────────────────────────────────────────────┐")
    print(f"  │  Ψ_global = {psi_global:.6f}                               │")
    print(f"  │  Estado:   {result['estado']:<42}│")
    print(f"  └──────────────────────────────────────────────────────┘")


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   VALIDATE — Escalera de Jacob del Carbono ∞³                      ║")
    print("║   Φ-Progressive 142.1 Hz Harmonic Recalibration                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    phase1_constantes()
    phase2_secuencia_aurea()
    phase3_guardianes()
    phase4_activacion()

    print(f"\n{'═' * 70}")
    if _errors:
        print(f"  ❌  {len(_errors)} check(s) failed:")
        for err in _errors:
            print(f"       • {err}")
        print(f"{'═' * 70}\n")
        return 1
    else:
        print(f"  ✅  All checks passed — Escalera de Jacob del Carbono ACTIVADA ∞³")
        print(f"{'═' * 70}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
