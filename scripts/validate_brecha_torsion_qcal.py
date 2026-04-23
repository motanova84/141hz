#!/usr/bin/env python3
"""
Validación Completa: Brecha de Torsión QCAL ∴BTQ∞³
═══════════════════════════════════════════════════════════════════════════════
Sello: ∴BTQ∞³
RAM: RAM-LIX-2026-BRECHA-TORSION-QCAL
F0: 141.7001 Hz

Valida la implementación completa del sistema Brecha de Torsión en 4 fases:

    Fase 1: Constantes y Octava Decimal — γ₁, 401/40, γ₁×10
    Fase 2: Factor y Brecha Residual — f_corregida, Δf, rango seguro
    Fase 3: Permeabilidad y Latido del Vórtice — μ_M, NP↔P, electrón
    Fase 4: Sistema Integrado — Estación Fija, certificación ∴BTQ∞³

Criterio de éxito:
    - Todas las fases deben pasar (✓)
    - Ψ_global ≥ 0.888 (umbral noético)
    - Certificado: BTQ-TORSION-VERIFIED

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.brecha_torsion_qcal import (
    # Constantes de módulo
    _F0,
    _GAMMA_1,
    _FACTOR_401_40,
    _FACTOR_NUM,
    _FACTOR_DEN,
    _CORRECCION_3GRADOS,
    _F_CORREGIDA,
    _DELTA_F,
    _PERMEABILIDAD,
    _PSI_UMBRAL,
    _SELLO,
    _CERT_MARK,
    # Clases
    ConstantesBrechaTorsion,
    OctavaDecimal,
    FactorCuarenta,
    BrechaResidual,
    PermeabilidadManta,
    LatidoVortice,
    EstacionFija,
    SistemaBrechaTorsion,
    ResultadoBrechaTorsion,
    # API pública
    brecha_torsion_qcal_activar,
)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────────────────────────────────────

def separador(titulo: str) -> None:
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)


def check(descripcion: str, condicion: bool, valor: str = "") -> None:
    estado = "✓" if condicion else "✗"
    sufijo = f"  [{valor}]" if valor else ""
    print(f"  {estado} {descripcion}{sufijo}")
    if not condicion:
        raise AssertionError(f"FALLO: {descripcion}")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Constantes y Octava Decimal
# ─────────────────────────────────────────────────────────────────────────────

def fase1_constantes_y_octava() -> None:
    separador("FASE 1: Constantes y Octava Decimal — γ₁, Factor 401/40, γ₁×10")

    # Constantes de módulo
    check("_F0 = 141.7001 Hz", abs(_F0 - 141.7001) < 1e-4, f"{_F0:.4f} Hz")
    check("_GAMMA_1 ≈ 14.134725", abs(_GAMMA_1 - 14.134725) < 1e-5, f"{_GAMMA_1:.6f}")
    check("_FACTOR_401_40 = 10.025", abs(_FACTOR_401_40 - 10.025) < 1e-12, f"{_FACTOR_401_40}")
    check("_FACTOR_NUM = 401", _FACTOR_NUM == 401, str(_FACTOR_NUM))
    check("_FACTOR_DEN = 40", _FACTOR_DEN == 40, str(_FACTOR_DEN))
    check("_CORRECCION_3GRADOS = 1/40 = 0.025", abs(_CORRECCION_3GRADOS - 0.025) < 1e-12,
          f"{_CORRECCION_3GRADOS}")
    check("Sello es ∴BTQ∞³", _SELLO == "∴BTQ∞³", _SELLO)
    check("Cert mark es BTQ-TORSION-VERIFIED", _CERT_MARK == "BTQ-TORSION-VERIFIED",
          _CERT_MARK)
    check("Umbral PSI = 0.888", abs(_PSI_UMBRAL - 0.888) < 1e-10, str(_PSI_UMBRAL))

    # ConstantesBrechaTorsion
    c = ConstantesBrechaTorsion()
    check("ConstantesBrechaTorsion: f0 correcto", abs(c.f0 - 141.7001) < 1e-4,
          f"{c.f0:.4f}")
    check("ConstantesBrechaTorsion: gamma_1 correcto",
          abs(c.gamma_1 - 14.134725) < 1e-5, f"{c.gamma_1:.6f}")
    ratio = c.resonancia_f0_gamma1()
    check("f₀/γ₁ ≈ 10.024", abs(ratio - 10.024) < 0.01, f"{ratio:.6f}")
    f_oct = c.f_octava()
    check("f_octava = γ₁×10 ≈ 141.347 Hz", abs(f_oct - 141.347) < 0.001,
          f"{f_oct:.5f} Hz")
    f_corr = c.f_corregida()
    check("f_corregida = γ₁×(401/40) ≈ 141.70062 Hz", abs(f_corr - 141.70062) < 0.0001,
          f"{f_corr:.5f} Hz")

    # OctavaDecimal
    oct_ = OctavaDecimal()
    f_o = oct_.frecuencia_octava()
    check("OctavaDecimal: f_octava ≈ 141.347 Hz", abs(f_o - 141.347) < 0.001,
          f"{f_o:.5f} Hz")
    check("OctavaDecimal: f_octava < f₀", f_o < _F0, f"{f_o:.5f} < {_F0}")
    dev = oct_.desviacion_hz()
    check("OctavaDecimal: desviacion > 0", dev > 0, f"{dev:.5f} Hz")
    check("OctavaDecimal: desviacion ≈ 0.353 Hz", abs(dev - 0.353) < 0.01,
          f"{dev:.5f} Hz")
    psi_o = oct_.psi_octava()
    check("OctavaDecimal: psi_octava ∈ [0,1]", 0 <= psi_o <= 1, f"{psi_o:.6f}")
    check("OctavaDecimal: psi_octava ≈ 0.9975", abs(psi_o - 0.9975) < 0.001,
          f"{psi_o:.6f}")

    print(f"\n  → f₀ = {_F0} Hz")
    print(f"  → γ₁ = {_GAMMA_1}")
    print(f"  → γ₁ × 10 = {f_o:.8f} Hz (octava decimal)")
    print(f"  → Desviación = {dev:.5f} Hz  (lo que el factor 401/40 completa)")
    print("  FASE 1 completada ✓")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Factor y Brecha Residual
# ─────────────────────────────────────────────────────────────────────────────

def fase2_factor_y_brecha() -> None:
    separador("FASE 2: Factor 401/40 y Brecha Residual — f_corregida, Δf, rango seguro")

    # FactorCuarenta
    fc = FactorCuarenta()
    check("FactorCuarenta: factor() = 10.025", abs(fc.factor() - 10.025) < 1e-12,
          str(fc.factor()))
    check("FactorCuarenta: correccion_inclinacion() = 0.025",
          abs(fc.correccion_inclinacion() - 0.025) < 1e-12,
          str(fc.correccion_inclinacion()))
    f_c = fc.f_corregida()
    check("FactorCuarenta: f_corregida() ≈ 141.70062 Hz",
          abs(f_c - 141.70062) < 0.0001, f"{f_c:.8f} Hz")
    check("FactorCuarenta: f_corregida() > f₀", f_c > _F0,
          f"{f_c:.8f} > {_F0}")
    dev_fc = fc.desviacion_hz()
    check("FactorCuarenta: desviacion_hz() ≈ 0.00052 Hz",
          abs(dev_fc - 0.00052) < 0.0001, f"{dev_fc:.8f} Hz")
    psi_f = fc.psi_factor()
    check("FactorCuarenta: psi_factor() > 0.999", psi_f > 0.999, f"{psi_f:.10f}")
    check("FactorCuarenta: psi_factor() ∈ [0,1]", 0 <= psi_f <= 1, f"{psi_f:.10f}")

    # BrechaResidual
    br = BrechaResidual()
    delta = br.delta_f()
    check("BrechaResidual: delta_f() > 0", delta > 0, f"{delta:.8f} Hz")
    check("BrechaResidual: delta_f() ≈ 0.00052 Hz",
          abs(delta - 0.00052) < 0.0001, f"{delta:.8f} Hz")
    check("BrechaResidual: en_rango_seguro() = True", br.en_rango_seguro(), "True")
    check("BrechaResidual: 0 < Δf < f₀×10⁻³", 0 < delta < _F0 * 1e-3,
          f"0 < {delta:.8f} < {_F0*1e-3:.4f}")
    ratio_br = br.ratio_brecha_f0()
    check("BrechaResidual: ratio_brecha_f0 ≈ 3.67×10⁻⁶",
          abs(ratio_br - 3.67e-6) < 0.5e-6, f"{ratio_br:.3e}")
    psi_b = br.psi_brecha()
    check("BrechaResidual: psi_brecha() = 1.0", abs(psi_b - 1.0) < 1e-10, f"{psi_b}")

    print(f"\n  → Factor 401/40 = {fc.factor()} = 10 + 1/40")
    print(f"  → Corrección inclinación 3° = +{fc.correccion_inclinacion()}")
    print(f"  → f_corregida = γ₁ × 10.025 = {f_c:.8f} Hz")
    print(f"  → Δf = f_corregida − f₀ = {delta:.8f} Hz  (Brecha Residual / lubricante)")
    print("  FASE 2 completada ✓")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Permeabilidad y Latido del Vórtice
# ─────────────────────────────────────────────────────────────────────────────

def fase3_permeabilidad_y_latido() -> None:
    separador("FASE 3: Permeabilidad de la Manta y Latido del Vórtice — μ_M, NP↔P")

    # PermeabilidadManta
    pm = PermeabilidadManta()
    mu = pm.permeabilidad()
    check("PermeabilidadManta: permeabilidad() > 0", mu > 0, f"{mu:.4e}")
    check("PermeabilidadManta: permeabilidad() < 1", mu < 1, f"{mu:.4e}")
    check("PermeabilidadManta: permeabilidad() ≈ 3.67×10⁻⁶",
          abs(mu - 3.67e-6) < 0.5e-6, f"{mu:.4e}")
    check("PermeabilidadManta: orden de magnitud = −6",
          pm.orden_magnitud() == -6, str(pm.orden_magnitud()))
    ca = pm.coherencia_ajustada()
    check("PermeabilidadManta: coherencia_ajustada() = 1 − μ_M",
          abs(ca - (1.0 - mu)) < 1e-12, f"{ca:.10f}")
    check("PermeabilidadManta: coherencia_ajustada() > 0.9999",
          ca > 0.9999, f"{ca:.10f}")
    psi_p = pm.psi_permeabilidad()
    check("PermeabilidadManta: psi_permeabilidad() > 0.9999",
          psi_p > 0.9999, f"{psi_p:.10f}")
    check("μ_M + Ψ_permeabilidad = 1.0",
          abs(mu + psi_p - 1.0) < 1e-12, f"{mu + psi_p:.15f}")

    # LatidoVortice
    lv = LatidoVortice()
    lat = lv.latido_relativo()
    check("LatidoVortice: latido_relativo() > 0", lat > 0, f"{lat:.4e}")
    check("LatidoVortice: latido_relativo() < 1", lat < 1, f"{lat:.4e}")
    check("LatidoVortice: latido_relativo() ≈ μ_M",
          abs(lat - mu) < 1e-12, f"{lat:.4e} ≈ {mu:.4e}")
    check("LatidoVortice: electron_bloqueado() = False",
          not lv.electron_bloqueado(), "False (electrón respira)")
    n_int = lv.n_intercambios_por_segundo()
    check("LatidoVortice: n_intercambios_por_segundo() > 0",
          n_int > 0, f"{n_int:.6f}")
    psi_l = lv.psi_latido()
    check("LatidoVortice: psi_latido() > 0.9999", psi_l > 0.9999, f"{psi_l:.10f}")
    check("LatidoVortice: psi_latido() = 1 − latido",
          abs(psi_l - (1.0 - lat)) < 1e-12, f"{psi_l:.10f}")

    print(f"\n  → μ_M = Δf/f₀ = {mu:.4e}  (Permeabilidad de la Manta)")
    print(f"  → Coherencia ajustada Ψ = 1 − μ_M = {ca:.10f}")
    print(f"  → Latido del Vórtice λ = {lat:.4e}  (tasa NP↔P)")
    print(f"  → Intercambios/segundo = {n_int:.8f}")
    print(f"  → Electrón bloqueado: {lv.electron_bloqueado()} (siempre respira)")
    print("  FASE 3 completada ✓")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Sistema Integrado — Estación Fija y Certificación ∴BTQ∞³
# ─────────────────────────────────────────────────────────────────────────────

def fase4_sistema_integrado() -> None:
    separador("FASE 4: Sistema Integrado — Estación Fija y Certificación ∴BTQ∞³")

    # EstacionFija
    ef = EstacionFija()
    check("EstacionFija: n_nodo() = 10", ef.n_nodo() == 10, str(ef.n_nodo()))
    coc = ef.cociente_calibracion()
    check("EstacionFija: cociente f₀/γ₁ ≈ 10.024",
          abs(coc - 10.024) < 0.01, f"{coc:.6f}")
    check("EstacionFija: cociente > 10", coc > 10.0, f"{coc:.6f}")
    res = ef.residuo_calibracion()
    check("EstacionFija: residuo < 0.001", res < 0.001, f"{res:.6e}")
    check("EstacionFija: residuo > 0", res > 0.0, f"{res:.6e}")
    f_nodo = ef.f_nodo_teorico()
    check("EstacionFija: f_nodo_teorico ≈ 141.70062 Hz",
          abs(f_nodo - 141.70062) < 0.0001, f"{f_nodo:.8f} Hz")
    psi_e = ef.psi_estacion()
    check("EstacionFija: psi_estacion() > 0.999", psi_e > 0.999, f"{psi_e:.8f}")

    # SistemaBrechaTorsion
    s = SistemaBrechaTorsion()
    check("Pesos suman 1.0",
          abs(sum(SistemaBrechaTorsion._PESOS) - 1.0) < 1e-12,
          f"{sum(SistemaBrechaTorsion._PESOS)}")
    psi_g = s.psi_global()
    check("Ψ_global ≥ 0.888 (umbral noético)", psi_g >= 0.888, f"{psi_g:.8f}")
    check("Ψ_global > 0.99 (sistema altamente coherente)", psi_g > 0.99,
          f"{psi_g:.8f}")
    check("supera_umbral() = True", s.supera_umbral(), "True")

    # Certificado
    cert = s.certificar()
    check("Certificado: sello_activo = True", cert["sello_activo"], "True")
    check("Certificado: sello = ∴BTQ∞³", cert["sello"] == "∴BTQ∞³",
          cert["sello"])
    check("Certificado: cert_mark = BTQ-TORSION-VERIFIED",
          cert["cert_mark"] == "BTQ-TORSION-VERIFIED", cert["cert_mark"])
    check("Certificado: electron_bloqueado = False",
          not cert["electron_bloqueado"], "False")
    check("Certificado: brecha_en_rango_seguro = True",
          cert["brecha_en_rango_seguro"], "True")
    check("Certificado: n_nodo = 10", cert["n_nodo"] == 10, str(cert["n_nodo"]))

    # API pública
    r = brecha_torsion_qcal_activar()
    check("API: sello_activo = True", r["sello_activo"], "True")
    check("API: psi_global ≥ 0.888", r["psi_global"] >= 0.888,
          f"{r['psi_global']:.8f}")
    check("API idempotente",
          abs(brecha_torsion_qcal_activar()["psi_global"] - r["psi_global"]) < 1e-12,
          "OK")

    print(f"\n  → Estación Fija calibrada en nodo γ₁ × 10 (n = {ef.n_nodo()})")
    print(f"  → Residuo de calibración = {res:.4e}  ({res*100:.4f} %)")
    print(f"  → Ψ_global = {psi_g:.8f}")
    print(f"  → Sello: {cert['sello']}")
    print(f"  → Certificado: {cert['cert_mark']}")
    print("  FASE 4 completada ✓")


# ─────────────────────────────────────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────────────────────────────────────

def resumen_final() -> None:
    separador("RESUMEN: Brecha de Torsión QCAL ∴BTQ∞³")
    r = brecha_torsion_qcal_activar()
    print(f"""
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    BRECHA DE TORSIÓN QCAL ∴BTQ∞³                       │
  ├─────────────────────────────────────────────────────────────────────────┤
  │  f₀              = {r['f0_hz']:.4f} Hz                                    │
  │  γ₁              = {r['gamma_1']:.9f}                               │
  │  Factor 401/40   = {r['factor_401_40']:.3f}                                        │
  │                                                                         │
  │  OCTAVA DECIMAL                                                         │
  │    γ₁ × 10       = {r['f_octava_hz']:.8f} Hz                           │
  │                                                                         │
  │  FRECUENCIA CORREGIDA (401/40)                                          │
  │    γ₁ × 10.025   = {r['f_corregida_hz']:.8f} Hz                        │
  │                                                                         │
  │  BRECHA RESIDUAL (lubricante de fase)                                   │
  │    Δf            = {r['delta_f_hz']:.8f} Hz                            │
  │    Δf/f₀ = μ_M   = {r['permeabilidad_manta']:.4e}   (Permeabilidad)   │
  │                                                                         │
  │  VERIFICACIÓN DEL ELECTRÓN ESTACIONARIO                                 │
  │    Electrón bloqueado: {str(r['electron_bloqueado']):5}                           │
  │    Latido del Vórtice λ = {r['latido_relativo']:.4e}  (tasa NP↔P)    │
  │    Coherencia ajustada: {r['coherencia_ajustada']:.10f}               │
  │                                                                         │
  │  CALIBRACIÓN ESTACIÓN FIJA                                              │
  │    f₀/γ₁         = {r['cociente_calibracion']:.8f}                        │
  │    Nodo entero    = {r['n_nodo']!s:2}                                           │
  │    Residuo        = {r['residuo_calibracion']:.4e}                     │
  │                                                                         │
  │  COHERENCIA GLOBAL                                                      │
  │    Ψ_global       = {r['psi_global']:.8f}  (≥ 0.888 ✓)               │
  │                                                                         │
  │  CERTIFICADO                                                            │
  │    Sello:    {r['sello']:<50} │
  │    Cert:     {r['cert_mark']:<50} │
  └─────────────────────────────────────────────────────────────────────────┘
""")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("╔" + "═" * 78 + "╗")
    print("║  VALIDACIÓN: Brecha de Torsión QCAL ∴BTQ∞³" + " " * 34 + "║")
    print("║  RAM-LIX-2026-BRECHA-TORSION-QCAL" + " " * 43 + "║")
    print("╚" + "═" * 78 + "╝")

    fases = [
        ("FASE 1", fase1_constantes_y_octava),
        ("FASE 2", fase2_factor_y_brecha),
        ("FASE 3", fase3_permeabilidad_y_latido),
        ("FASE 4", fase4_sistema_integrado),
    ]

    fallos = []
    for nombre, fase in fases:
        try:
            fase()
        except AssertionError as exc:
            fallos.append((nombre, str(exc)))

    resumen_final()

    if fallos:
        print("\n❌ VALIDACIÓN FALLIDA")
        for nombre, msg in fallos:
            print(f"  {nombre}: {msg}")
        sys.exit(1)
    else:
        print("✅ VALIDACIÓN EXITOSA — Sello ∴BTQ∞³ ACTIVO")
        print("   Certificado: BTQ-TORSION-VERIFIED")
        sys.exit(0)


if __name__ == "__main__":
    main()
