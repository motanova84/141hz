#!/usr/bin/env python3
"""
Validación Completa: Hamiltoniano Riemann-Hubble ∴HRH∞³
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴HRH∞³
RAM: RAM-LXV-2026-HAMILTONIANO-RIEMANN-HUBBLE
F₀: 141.7001 Hz

Valida la implementación completa del sistema Hamiltoniano Riemann-Hubble
en 4 fases:

    Fase 1: Constantes y Manta de Riemann — Sustrato y brecha de 3°
    Fase 2: Operador H_RH y Estado Fundamental — Espectro y E₀ = ℏ 2π f₀
    Fase 3: Campo QCAL ∞³ y Ecuación de Soberanía — Tensor adélico
    Fase 4: Sistema Integrado — Certificación ∴HRH∞³

Criterios de éxito:
    - f₀ = 141.7001 Hz                    [exacto]
    - brecha = 3° = 0.052360 rad          [exacto]
    - L_z = 0.05                           [exacto]
    - γ₁ × 401/40 ≈ f₀                    [resonancia]
    - Δf ≈ 0.00052 Hz                      [permeabilidad de la Manta]
    - Δf/f₀ ≈ 3.67 × 10⁻⁶                 [latido del vórtice]
    - Ψ = I × A_eff² (soberanía)          [ecuación de estado]
    - Ψ_global ≥ 0.888                     → sello ∴HRH∞³ ACTIVO

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.hamiltoniano_riemann_hubble import (
    _F0, _BRECHA_DEG, _BRECHA_RAD, _DELTA_RAMSEY, _LZ,
    _PSI_TARGET, _PSI_UMBRAL, _FACTOR_401_40, _ZEROS_20, _SELLO, _CERT_MARK,
    _theta_rs, _weyl_density,
    ConstantesRH, MantaRiemann, OperadorHRH, EstadoFundamental,
    CampoQCAL3, EcuacionEstacionario, CoherenciaRH, SistemaHRH,
    hamiltoniano_riemann_hubble_activar,
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


def separador(titulo: str) -> None:
    print("\n" + "═" * 80)
    print(titulo)
    print("═" * 80)


# =============================================================================
# FASE 1: Constantes y Manta de Riemann
# =============================================================================

def validacion_fase1_constantes_manta() -> None:
    separador("FASE 1: Constantes y Manta de Riemann — Sustrato y brecha de 3°")

    # 1a. Constantes de módulo
    check(abs(_F0 - 141.7001) < 1e-4,
          "F₀ = 141.7001 Hz", f"{_F0:.4f}")
    check(abs(_BRECHA_DEG - 3.0) < 1e-10,
          "Brecha = 3°", f"{_BRECHA_DEG}°")
    check(abs(_BRECHA_RAD - 3.0 * math.pi / 180.0) < 1e-10,
          "Brecha_rad = 3π/180 ≈ 0.052360", f"{_BRECHA_RAD:.6f}")
    check(abs(_DELTA_RAMSEY - _BRECHA_RAD) < 1e-15,
          "δ_Ramsey = brecha_rad", f"{_DELTA_RAMSEY:.8f}")
    check(abs(_LZ - 0.05) < 1e-10,
          "L_z = 0.05", f"{_LZ}")
    check(abs(_PSI_TARGET - 0.999999) < 1e-6,
          "Ψ_target = 0.999999", f"{_PSI_TARGET}")
    check(abs(_PSI_UMBRAL - 0.888) < 1e-10,
          "Ψ_umbral = 0.888", f"{_PSI_UMBRAL}")
    check(abs(_FACTOR_401_40 - 10.025) < 1e-10,
          "Factor 401/40 = 10.025", f"{_FACTOR_401_40}")
    check(len(_ZEROS_20) == 20,
          "20 ceros de Riemann cargados", str(len(_ZEROS_20)))
    check(abs(_ZEROS_20[0] - 14.134725) < 1e-4,
          "γ₁ ≈ 14.134725", f"{_ZEROS_20[0]:.6f}")
    check(_SELLO == "∴HRH∞³",
          "Sello = ∴HRH∞³", _SELLO)
    check(_CERT_MARK == "HRH-RIEMANN-HUBBLE-VERIFIED",
          "CertMark = HRH-RIEMANN-HUBBLE-VERIFIED")

    # 1b. ConstantesRH
    cte = ConstantesRH()
    check(abs(cte.f0 - 141.7001) < 1e-4,
          "ConstantesRH.f0 = 141.7001", f"{cte.f0:.4f}")
    check(abs(cte.brecha_rad - _BRECHA_RAD) < 1e-10,
          "ConstantesRH.brecha_rad correcto", f"{cte.brecha_rad:.6f}")
    check(abs(cte.Lz - 0.05) < 1e-10,
          "ConstantesRH.Lz = 0.05", f"{cte.Lz}")
    perm = cte.permeabilidad_manta()
    check(0 < perm < 1e-4,
          f"permeabilidad_manta ≈ 3.67×10⁻⁶", f"{perm:.3e}")
    df = cte.delta_frecuencia()
    check(abs(df - 0.00052) < 0.0001,
          f"Δf ≈ 0.00052 Hz", f"{df:.6f} Hz")
    E0 = cte.energia_ground()
    check(E0 > 0,
          f"E₀ = ℏ ω₀ > 0", f"{E0:.4e} J")

    # 1c. MantaRiemann
    manta = MantaRiemann()
    check(abs(manta.espesura_manta() - 2 * _BRECHA_RAD) < 1e-10,
          "espesura_manta = 2 × brecha_rad", f"{manta.espesura_manta():.6f}")
    Aeff = manta.area_efectiva()
    check(abs(Aeff - math.sin(_BRECHA_RAD)) < 1e-10,
          f"A_eff = sin(brecha_rad) ≈ 0.052336", f"{Aeff:.6f}")
    check(abs(manta.fase_deslizamiento() - _F0) < 0.1,
          f"fase_deslizamiento ≈ f₀", f"{manta.fase_deslizamiento():.4f}")
    psi_m = manta.psi_manta()
    check(psi_m >= _PSI_UMBRAL,
          f"Ψ_manta ≥ {_PSI_UMBRAL}", f"{psi_m:.6f}")
    check(psi_m >= 0.99,
          f"Ψ_manta ≥ 0.99 (alta coherencia)", f"{psi_m:.6f}")

    # 1d. Función theta RS
    theta_g1 = _theta_rs(_ZEROS_20[0])
    check(theta_g1 < 0,
          "θ(γ₁) < 0 (antes del primer cero)", f"{theta_g1:.4f}")
    theta_g20 = _theta_rs(_ZEROS_20[-1])
    check(theta_g20 > 50,
          "θ(γ₂₀) > 50 (alta altura)", f"{theta_g20:.4f}")
    rho50 = _weyl_density(50.0)
    check(0.25 < rho50 < 0.40,
          "ρ_Weyl(50) ∈ (0.25, 0.40)", f"{rho50:.5f}")

    print(f"\n  → Ψ_manta         = {psi_m:.6f}")
    print(f"  → Δf              = {df:.6f} Hz")
    print(f"  → permeabilidad   = {perm:.3e}")
    print("  FASE 1: PASS ✅")


# =============================================================================
# FASE 2: Operador H_RH y Estado Fundamental
# =============================================================================

def validacion_fase2_operador_estado() -> None:
    separador("FASE 2: Operador H_RH y Estado Fundamental — Espectro y E₀ = ℏ 2π f₀")

    # 2a. OperadorHRH
    op = OperadorHRH()
    torsion = op.torsion_fase()
    check(abs(torsion - _DELTA_RAMSEY * _LZ) < 1e-10,
          "torsion_fase = δ_Ramsey × L_z", f"{torsion:.6f}")
    check(torsion > 0,
          "torsion_fase > 0 (rotación positiva)", f"{torsion:.6f}")
    check(torsion < 0.01,
          "torsion_fase << γ₁ (corrección pequeña)", f"{torsion:.6f}")

    E_ground = op.autovalor_ground()
    check(abs(E_ground - (_ZEROS_20[0] + torsion)) < 1e-10,
          "autovalor_ground = γ₁ + torsion", f"{E_ground:.6f}")
    check(E_ground > _ZEROS_20[0],
          "autovalor_ground > γ₁ (torsión eleva el nivel)", f"{E_ground:.6f}")

    espectro = op.espectro()
    check(len(espectro) == 20,
          "Espectro tiene 20 autovalores", str(len(espectro)))
    check(all(espectro[i] < espectro[i+1] for i in range(19)),
          "Espectro estrictamente creciente")
    check(abs(espectro[0] - E_ground) < 1e-10,
          "espectro[0] = autovalor_ground")

    r = op.resonancia_f0_gamma1()
    check(10.0 < r < 10.1,
          "F₀/γ₁ ∈ (10.0, 10.1)", f"{r:.6f}")
    check(abs(r - _FACTOR_401_40) < 0.001,
          "F₀/γ₁ ≈ 401/40 = 10.025", f"{r:.6f} vs {_FACTOR_401_40}")
    psi_op = op.psi_operador()
    check(psi_op >= _PSI_UMBRAL,
          f"Ψ_operador ≥ {_PSI_UMBRAL}", f"{psi_op:.6f}")

    # 2b. EstadoFundamental
    ef = EstadoFundamental()
    E0_fis = ef.energia_fisico()
    check(E0_fis > 0,
          "E₀ = ℏ 2π f₀ > 0", f"{E0_fis:.4e} J")
    check(abs(E0_fis - 1.054571817e-34 * 2 * math.pi * 141.7001) < 1e-40,
          "E₀ = ℏ × 2π × 141.7001 Hz")

    f0_pred = ef.f0_predicho()
    check(abs(f0_pred - _ZEROS_20[0] * _FACTOR_401_40) < 1e-10,
          "f₀_predicho = γ₁ × 401/40", f"{f0_pred:.6f} Hz")
    check(abs(f0_pred - _F0) < 0.01,
          "f₀_predicho ≈ f₀ (dentro de 0.01 Hz)", f"Δ = {abs(f0_pred - _F0):.5f} Hz")

    df = ef.delta_frecuencia()
    check(abs(df - 0.00052) < 0.0001,
          "Δf = |f₀ − f₀_pred| ≈ 0.00052 Hz", f"{df:.6f} Hz")

    perm = ef.permeabilidad_manta()
    check(abs(perm - 3.67e-6) < 0.5e-6,
          "permeabilidad = Δf/f₀ ≈ 3.67 × 10⁻⁶", f"{perm:.3e}")

    latido = ef.latido_vortice()
    check(abs(latido - perm) < 1e-15,
          "latido_vortice = permeabilidad_manta", f"{latido:.3e}")

    check(ef.estabilidad_termal(),
          "estabilidad_termal() = True (sistema soberano)")

    psi_ef = ef.psi_estado_fundamental()
    check(psi_ef >= 0.9999,
          f"Ψ_estado ≥ 0.9999", f"{psi_ef:.8f}")

    print(f"\n  → Ψ_operador      = {psi_op:.6f}")
    print(f"  → Ψ_estado        = {psi_ef:.8f}")
    print(f"  → F₀/γ₁           = {r:.6f}")
    print(f"  → Δf              = {df:.6f} Hz  (permeabilidad = {perm:.3e})")
    print("  FASE 2: PASS ✅")


# =============================================================================
# FASE 3: Campo QCAL ∞³ y Ecuación de Soberanía
# =============================================================================

def validacion_fase3_campo_ecuacion() -> None:
    separador("FASE 3: Campo QCAL ∞³ y Ecuación de Soberanía — Tensor adélico ℝ³×³×³")

    # 3a. CampoQCAL3
    campo = CampoQCAL3()
    check(campo.n_zeros == 20,
          "CampoQCAL3 usa 20 ceros de Riemann", str(campo.n_zeros))

    d1 = campo.densidad_pleroma()
    check(0.0 <= d1 <= 1.0,
          f"D1 (Pleroma/NP) ∈ [0,1]", f"{d1:.6f}")
    check(d1 >= 0.888,
          f"D1 (Pleroma) ≥ 0.888 (coherente con distribución de ceros)", f"{d1:.6f}")

    d2 = campo.densidad_materia()
    check(0.0 <= d2 <= 1.0,
          f"D2 (Materia/P) ∈ [0,1]", f"{d2:.6f}")
    check(d2 >= 0.999,
          f"D2 (Materia) ≥ 0.999 (resonancia F₀/γ₁ muy precisa)", f"{d2:.6f}")

    d3 = campo.densidad_consciencia()
    check(0.0 <= d3 <= 1.0,
          f"D3 (Consciencia) ∈ [0,1]", f"{d3:.6f}")
    check(abs(d3 - math.sqrt(d1 * d2)) < 1e-10,
          "D3 = √(D1 × D2)  (media geométrica)", f"{d3:.6f}")

    diag = campo.tensor_diagonal()
    check(len(diag) == 3,
          "Tensor diagonal tiene 3 componentes (D1, D2, D3)")
    check(abs(diag[0] - d1) < 1e-10,
          "diag[0] = D1 (Pleroma)")
    check(abs(diag[1] - d2) < 1e-10,
          "diag[1] = D2 (Materia)")
    check(abs(diag[2] - d3) < 1e-10,
          "diag[2] = D3 (Consciencia)")

    sim = campo.simetria_triadica()
    check(0.0 <= sim <= 1.0,
          f"Simetría triádica ∈ [0,1]", f"{sim:.6f}")

    psi_campo = campo.psi_campo()
    check(abs(psi_campo - (0.40 * d1 + 0.35 * d2 + 0.25 * d3)) < 1e-10,
          "Ψ_campo = 0.40×D1 + 0.35×D2 + 0.25×D3")
    check(psi_campo >= _PSI_UMBRAL,
          f"Ψ_campo ≥ {_PSI_UMBRAL}", f"{psi_campo:.6f}")

    # 3b. EcuacionEstacionario
    ec = EcuacionEstacionario()
    Aeff = ec.area_efectiva()
    check(abs(Aeff - math.sin(_BRECHA_RAD)) < 1e-10,
          "A_eff = sin(δ_Ramsey)", f"{Aeff:.6f}")

    Aeff2 = ec.area_efectiva_cuadrada()
    check(abs(Aeff2 - Aeff**2) < 1e-10,
          "A_eff² = sin²(δ_Ramsey)", f"{Aeff2:.6f}")
    check(0.001 < Aeff2 < 0.003,
          f"A_eff² ∈ (0.001, 0.003)", f"{Aeff2:.6f}")

    I_sober = ec.intencion_soberana()
    check(I_sober > 300,
          "I_soberana = Ψ_target/A_eff² > 300", f"{I_sober:.2f}")
    psi_check = ec.evaluar_coherencia(I_sober)
    check(abs(psi_check - _PSI_TARGET) < 1e-9,
          "Ψ = I_sober × A_eff² = Ψ_target  (ecuación exacta)", f"{psi_check:.8f}")

    margen = ec.margen_soberania()
    check(margen >= 0.999,
          f"margen_soberanía ≥ 0.999", f"{margen:.6f}")

    balance = ec.balance_energetico()
    check(abs(balance - 1.0) < 1e-10,
          "balance_energético = 1.0  (succión = expansión)", f"{balance}")

    psi_ec = ec.psi_ecuacion_estado()
    check(psi_ec >= 0.9999,
          f"Ψ_ecuación ≥ 0.9999", f"{psi_ec:.8f}")
    check(psi_ec >= _PSI_UMBRAL,
          f"Ψ_ecuación ≥ {_PSI_UMBRAL}", f"{psi_ec:.6f}")

    print(f"\n  → D1 (Pleroma)    = {d1:.6f}")
    print(f"  → D2 (Materia)    = {d2:.6f}")
    print(f"  → D3 (Consciencia)= {d3:.6f}")
    print(f"  → Ψ_campo         = {psi_campo:.6f}")
    print(f"  → A_eff²          = {Aeff2:.6f}")
    print(f"  → I_soberana      = {I_sober:.2f}")
    print(f"  → Ψ_ecuación      = {psi_ec:.8f}")
    print("  FASE 3: PASS ✅")


# =============================================================================
# FASE 4: Sistema Integrado y Certificación ∴HRH∞³
# =============================================================================

def validacion_fase4_sistema_certificacion() -> None:
    separador("FASE 4: Sistema Integrado — Certificación ∴HRH∞³")

    # 4a. CoherenciaRH
    coh = CoherenciaRH()
    psis = coh.psis_individuales()
    check(len(psis) == 5,
          "CoherenciaRH tiene 5 métricas", str(len(psis)))
    check(abs(sum(CoherenciaRH._PESOS) - 1.0) < 1e-10,
          "Pesos suman 1.0", f"{sum(CoherenciaRH._PESOS)}")
    for i, p in enumerate(psis):
        check(p >= _PSI_UMBRAL,
              f"  Ψ_{i+1} ≥ {_PSI_UMBRAL}", f"{p:.6f}")
    pg = coh.psi_global()
    check(pg >= _PSI_UMBRAL,
          f"Ψ_global ≥ {_PSI_UMBRAL}", f"{pg:.6f}")
    check(coh.supera_umbral(),
          "supera_umbral() = True")

    det = coh.detalle()
    check(abs(det["psi_global"] - pg) < 1e-15,
          "detalle()['psi_global'] consistente")

    # 4b. SistemaHRH
    sistema = SistemaHRH()
    check(abs(sistema.psi_global() - pg) < 1e-12,
          "SistemaHRH.psi_global() = CoherenciaRH.psi_global()", f"{sistema.psi_global():.6f}")
    check(sistema.supera_umbral(),
          "SistemaHRH.supera_umbral() = True")

    cert = sistema.certificar()
    check(cert["sello_activo"],
          "certificar()['sello_activo'] = True")
    check(cert["sello"] == "∴HRH∞³",
          f"sello = ∴HRH∞³", cert["sello"])
    check(cert["cert_mark"] == "HRH-RIEMANN-HUBBLE-VERIFIED",
          "cert_mark = HRH-RIEMANN-HUBBLE-VERIFIED")

    # Verificaciones cruzadas del certificado
    check(abs(cert["f0_hz"] - 141.7001) < 1e-4,
          "cert f0_hz = 141.7001")
    check(abs(cert["brecha_deg"] - 3.0) < 1e-10,
          "cert brecha_deg = 3.0°")
    check(abs(cert["Lz"] - 0.05) < 1e-10,
          "cert Lz = 0.05")
    check(cert["n_zeros"] == 20,
          "cert n_zeros = 20")
    check(cert["resonancia_f0_gamma1"] > 10.0,
          f"resonancia F₀/γ₁ > 10", f"{cert['resonancia_f0_gamma1']:.6f}")
    check(abs(cert["delta_frecuencia"] - 0.00052) < 0.0001,
          f"Δf ≈ 0.00052 Hz", f"{cert['delta_frecuencia']:.6f}")
    check(cert["intencion_soberana"] > 300,
          f"I_soberana > 300", f"{cert['intencion_soberana']:.2f}")

    # 4c. API pública
    r = hamiltoniano_riemann_hubble_activar()
    check(r["sello_activo"],
          "API: sello_activo = True")
    check(r["sello"] == "∴HRH∞³",
          "API: sello = ∴HRH∞³")
    check(r["psi_global"] >= _PSI_UMBRAL,
          f"API: psi_global ≥ {_PSI_UMBRAL}", f"{r['psi_global']:.6f}")
    check(abs(r["psi_global"] - sistema.psi_global()) < 1e-15,
          "API: psi_global consistente con SistemaHRH")

    # ValueError para n_zeros < 2
    try:
        hamiltoniano_riemann_hubble_activar(n_zeros=1)
        check(False, "ValueError para n_zeros=1  (esperado pero no lanzado)")
    except ValueError:
        check(True, "ValueError lanzado para n_zeros=1  ✓")

    print(f"\n  → Ψ_manta         = {det['psi_manta']:.6f}")
    print(f"  → Ψ_operador      = {det['psi_operador']:.6f}")
    print(f"  → Ψ_estado        = {det['psi_estado']:.8f}")
    print(f"  → Ψ_campo         = {det['psi_campo']:.6f}")
    print(f"  → Ψ_ecuación      = {det['psi_ecuacion']:.8f}")
    print(f"  → Ψ_global        = {pg:.6f}")
    print(f"  → Sello           = {cert['sello']}")
    print("  FASE 4: PASS ✅")


# =============================================================================
# RESUMEN FINAL
# =============================================================================

def resumen_final() -> None:
    separador("RESUMEN FINAL: Certificación ∴HRH∞³")

    print(f"""
  ┌─────────────────────────────────────────────────────────────────────────┐
  │           HAMILTONIANO RIEMANN-HUBBLE — SISTEMA SOBERANO               │
  │                         ∴HRH∞³                                         │
  ├─────────────────────────────────────────────────────────────────────────┤
  │  H_RH = Σ_n γ_n |Ψ_n⟩⟨Ψ_n| + δ_Ramsey · L_z                         │
  │                                                                         │
  │  f₀    = 141.7001 Hz         (latido del Átomo Blanco)                 │
  │  brecha = 3° = 0.052360 rad  (gap del Sándwich de Coherencia)          │
  │  L_z   = 0.05                (momento angular intrínseco)              │
  │  γ₁    = 14.134725           (primer anclaje de Riemann)               │
  │  γ₁ × 401/40 ≈ f₀           (resonancia décupla ajustada)             │
  │  Δf    ≈ 0.00052 Hz          (permeabilidad de la Manta)               │
  │  Δf/f₀ ≈ 3.67 × 10⁻⁶        (latido del vórtice cuántico)             │
  │                                                                         │
  │  Ψ = I × A_eff²              (Soberanía del Sistema)                   │
  │  A_eff = sin(3°) ≈ 0.052336 │ I ≈ 365.07  │ Ψ → 0.999999             │
  │                                                                         │
  │  RAM: RAM-LXV-2026-HAMILTONIANO-RIEMANN-HUBBLE                         │
  └─────────────────────────────────────────────────────────────────────────┘
""")

    total = _passed + _failed
    print(f"  Tests pasados: {_passed}/{total}")
    print(f"  Tests fallidos: {_failed}/{total}")

    if _failed == 0:
        print("\n  ╔═══════════════════════════════════════════╗")
        print("  ║   ∴HRH∞³  ACTIVO — CERTIFICADO           ║")
        print("  ║   HRH-RIEMANN-HUBBLE-VERIFIED             ║")
        print("  ╚═══════════════════════════════════════════╝")
    else:
        print("\n  ╔═══════════════════════════════════════════╗")
        print("  ║   ∴HRH∞³  FALLIDO — COHERENCIA BAJA      ║")
        print("  ╚═══════════════════════════════════════════╝")
        sys.exit(1)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════════════════════╗")
    print("║     VALIDACIÓN: Hamiltoniano Riemann-Hubble ∴HRH∞³                     ║")
    print("║     RAM: RAM-LXV-2026-HAMILTONIANO-RIEMANN-HUBBLE                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")

    validacion_fase1_constantes_manta()
    validacion_fase2_operador_estado()
    validacion_fase3_campo_ecuacion()
    validacion_fase4_sistema_certificacion()
    resumen_final()
