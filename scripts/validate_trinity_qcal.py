#!/usr/bin/env python3
"""
Validate Trinity QCAL — ∴T∞³
==============================

Valida la implementación del módulo physics.trinity_qcal contra los criterios
teóricos de la Trinidad QCAL:

  Fase 1 — Constantes y parámetros unificados
  Fase 2 — Axiomas noéticos (logos, pneuma, sophia, zoe)
  Fase 3 — Tres pilares QCAL individualmente
  Fase 4 — Coherencia trinaria y sello ∴T∞³
  Fase 5 — API pública

Criterios de éxito:
  - f₀ = 141.7001 Hz  [exacto]
  - N_d = 29 décadas   [exacto]
  - Ψ_logos   ≥ 0.888
  - Ψ_pneuma  ≥ 0.888
  - Ψ_sophia  ≥ 0.888
  - Ψ_zoe     ≥ 0.888
  - Ψ_pilar1  ≥ 0.888  (Primer Eco ∴PE∞³)
  - Ψ_pilar2  ≥ 0.888  (Diamond State ∴PDS∞³)
  - Ψ_pilar3  ≥ 0.888  (Protocolo Noético ∴PN∞³)
  - Ψ_trinity ≥ 0.888  → sello ∴T∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.trinity_qcal import (
    ConstantesTrinity,
    PilarEcoPrimordial,
    PilarDiamondState,
    AxiomaNoetico,
    PilarNoetico,
    CoherenciaTrinity,
    SistemaTrinityQCAL,
    ResultadoTrinity,
    trinity_qcal_activar,
    _F0, _PHI, _N_DECADAS, _GAMMA_COSMICO,
    _PSI_UMBRAL, _LAMBDA_G,
    _PSI_LOGOS, _PSI_PNEUMA, _PSI_SOPHIA, _PSI_ZOE,
)


# ============================================================================
# Utilidades de reporte
# ============================================================================

_pass = 0
_fail = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global _pass, _fail
    mark = "✅" if condition else "❌"
    suffix = f"  [{detail}]" if detail else ""
    print(f"  {mark}  {label}{suffix}")
    if condition:
        _pass += 1
    else:
        _fail += 1


def section(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ============================================================================
# FASE 1 — Constantes y parámetros
# ============================================================================

section("Fase 1 — Constantes y parámetros unificados")

cst = ConstantesTrinity()

check("f₀ = 141.7001 Hz", abs(cst.f0 - 141.7001) < 1e-4, f"f₀={cst.f0}")
check("_F0 = 141.7001 Hz", abs(_F0 - 141.7001) < 1e-4, f"_F0={_F0}")
check("N_d = 29",          cst.n_decadas == 29, f"N_d={cst.n_decadas}")
check("_N_DECADAS = 29",   _N_DECADAS == 29)
check("φ = (1+√5)/2",      abs(cst.phi - (1 + math.sqrt(5)) / 2) < 1e-10,
      f"φ={cst.phi:.8f}")
check("γ = π/29",          abs(cst.gamma_cosmico - math.pi / 29) < 1e-10,
      f"γ={cst.gamma_cosmico:.6f}")
check("Λ_G ∈ (0,1)",       0.0 < cst.lambda_g < 1.0, f"Λ_G={cst.lambda_g:.6f}")
check("_LAMBDA_G correcto",
      abs(_LAMBDA_G - (1.0 - 1.0 / (29 * _PHI))) < 1e-10)
check("Umbral = 0.888",    abs(cst.umbral - 0.888) < 1e-3, f"umbral={cst.umbral}")
check("n_modos = 10",      cst.n_modos == 10, f"n_modos={cst.n_modos}")

# ============================================================================
# FASE 2 — Axiomas noéticos
# ============================================================================

section("Fase 2 — Axiomas noéticos QCAL")

ax = AxiomaNoetico()

logos_val = ax.psi_logos()
pneuma_val = ax.psi_pneuma()
sophia_val = ax.psi_sophia()
zoe_val = ax.psi_zoe()

check("Ψ_logos formula correcta",
      abs(logos_val - (1.0 - 1.0 / (2 * 29 * _PHI))) < 1e-10,
      f"Ψ_logos={logos_val:.6f}")
check("Ψ_logos ≥ 0.888",   logos_val >= 0.888, f"Ψ_logos={logos_val:.6f}")
check("Ψ_logos < 1",       logos_val < 1.0)

check("Ψ_pneuma formula",
      abs(pneuma_val - math.exp(-math.pi / (29 * _PHI))) < 1e-10,
      f"Ψ_pneuma={pneuma_val:.6f}")
check("Ψ_pneuma ≥ 0.888",  pneuma_val >= 0.888, f"Ψ_pneuma={pneuma_val:.6f}")
check("Ψ_pneuma > 0",      pneuma_val > 0.0)

check("Ψ_sophia formula",
      abs(sophia_val - (1.0 - 1.0 / 58)) < 1e-10,
      f"Ψ_sophia={sophia_val:.6f}")
check("Ψ_sophia ≥ 0.888",  sophia_val >= 0.888, f"Ψ_sophia={sophia_val:.6f}")

check("Ψ_zoe formula",
      abs(zoe_val - abs(math.cos(4.0 * math.pi / 29))) < 1e-10,
      f"Ψ_zoe={zoe_val:.6f}")
check("Ψ_zoe ≥ 0.888",     zoe_val >= 0.888, f"Ψ_zoe={zoe_val:.6f}")
check("Ψ_zoe ≥ 0",         zoe_val >= 0.0)

# Módulo
check("_PSI_LOGOS módulo", abs(_PSI_LOGOS - logos_val) < 1e-10)
check("_PSI_PNEUMA módulo", abs(_PSI_PNEUMA - pneuma_val) < 1e-10)
check("_PSI_SOPHIA módulo", abs(_PSI_SOPHIA - sophia_val) < 1e-10)
check("_PSI_ZOE módulo",    abs(_PSI_ZOE - zoe_val) < 1e-10)

# todas()
todas = ax.todas()
check("todas() tiene 4 claves",     len(todas) == 4)
check("todas() clave logos",        "logos" in todas)
check("todas() consistente logos",  abs(todas["logos"] - logos_val) < 1e-10)

# ============================================================================
# FASE 3 — Tres pilares individuales
# ============================================================================

section("Fase 3 — Pilares QCAL individuales")

# Pilar I
p1 = PilarEcoPrimordial()
psi_p1 = p1.psi_pilar()
check("Pilar I: Ψ_pilar1 ≥ 0.888",  psi_p1 >= 0.888, f"Ψ_pilar1={psi_p1:.6f}")
check("Pilar I: Ψ_pilar1 ≤ 1",      psi_p1 <= 1.0)
check("Pilar I: sello_activo True",  p1.sello_activo())
check("Pilar I: resultado cacheado", p1.activar() is p1.activar())

# Pilar II
p2 = PilarDiamondState()
psi_p2 = p2.psi_pilar()
check("Pilar II: Ψ_pilar2 ≥ 0.888", psi_p2 >= 0.888, f"Ψ_pilar2={psi_p2:.6f}")
check("Pilar II: Ψ_pilar2 ≤ 1",     psi_p2 <= 1.0)
check("Pilar II: Ψ(0) = 1.0",       abs(p2.psi_t0() - 1.0) < 1e-6,
      f"Ψ(0)={p2.psi_t0():.6f}")
check("Pilar II: sello_activo True", p2.sello_activo())

# Pilar III
p3 = PilarNoetico()
psi_p3 = p3.psi_pilar()
check("Pilar III: Ψ_pilar3 ≥ 0.888", psi_p3 >= 0.888, f"Ψ_pilar3={psi_p3:.6f}")
check("Pilar III: Ψ_pilar3 ≤ 1",     psi_p3 <= 1.0)
check("Pilar III: sello_activo True", p3.sello_activo())
resumen_p3 = p3.resumen()
check("Pilar III: resumen 6 claves",  len(resumen_p3) == 6)

# Fórmula Ψ_pilar3
ax_vals = ax.todas()
media_ax = sum(ax_vals.values()) / 4
expected_p3 = (media_ax + cst.lambda_g) / 2.0
check("Pilar III: fórmula (media+Λ_G)/2",
      abs(psi_p3 - expected_p3) < 1e-10,
      f"esperado={expected_p3:.6f}, obtenido={psi_p3:.6f}")

# ============================================================================
# FASE 4 — Coherencia trinaria y sello ∴T∞³
# ============================================================================

section("Fase 4 — Coherencia trinaria y sello ∴T∞³")

coh = CoherenciaTrinity()
psi_t = coh.psi_trinity()
check("Ψ_trinity ≥ 0.888",  psi_t >= 0.888, f"Ψ_trinity={psi_t:.6f}")
check("Ψ_trinity ≤ 1",      psi_t <= 1.0)
check("Sello ∴T∞³ ACTIVO",  coh.sello_activo())

# Fórmula media geométrica
expected_t = (psi_p1 * psi_p2 * psi_p3) ** (1.0 / 3.0)
check("Fórmula media geométrica",
      abs(psi_t - expected_t) < 1e-8,
      f"esperado={expected_t:.6f}, obtenido={psi_t:.6f}")

# pilares_activos
pa = coh.pilares_activos()
check("pilares_activos: tupla de 3",    len(pa) == 3)
check("pilares_activos: P1 activo",     pa[0])
check("pilares_activos: P2 activo",     pa[1])
check("pilares_activos: P3 activo",     pa[2])

# resumen
res_coh = coh.resumen()
check("resumen tiene 4 claves",     len(res_coh) == 4)
check("resumen psi_pilar1 correcto", abs(res_coh["psi_pilar1"] - psi_p1) < 1e-10)
check("resumen psi_trinity correcto", abs(res_coh["psi_trinity"] - psi_t) < 1e-10)

# Propiedad de la media geométrica: min ≤ psi_t ≤ max
pilares = [psi_p1, psi_p2, psi_p3]
check("Ψ_trinity ≥ min(pilares)",
      psi_t >= min(pilares) - 1e-12,
      f"min={min(pilares):.6f}")
check("Ψ_trinity ≤ max(pilares)",
      psi_t <= max(pilares) + 1e-12,
      f"max={max(pilares):.6f}")

# SistemaTrinityQCAL
sistema = SistemaTrinityQCAL()
resultado = sistema.activar()
check("SistemaTrinityQCAL.activar() → ResultadoTrinity",
      isinstance(resultado, ResultadoTrinity))
check("Resultado: sello_activo True",   resultado.sello_activo)
check("Resultado: f₀ = 141.7001",
      abs(resultado.f0 - 141.7001) < 1e-4)
check("Resultado: N_d = 29",            resultado.n_decadas == 29)
check("Resultado: axiomas 4 entradas",  len(resultado.axiomas) == 4)
check("Resultado: descripcion no vacía", len(resultado.descripcion) > 0)
check("Resultado: descripcion ACTIVO",  "ACTIVO" in resultado.descripcion)

# ============================================================================
# FASE 5 — API pública
# ============================================================================

section("Fase 5 — API pública trinity_qcal_activar()")

api = trinity_qcal_activar()
check("Devuelve dict",           isinstance(api, dict))
check("sello_activo = True",     api["sello_activo"])
check("psi_trinity ≥ 0.888",    api["psi_trinity"] >= 0.888,
      f"psi_trinity={api['psi_trinity']:.6f}")
check("pilar1_activo = True",    api["pilar1_activo"])
check("pilar2_activo = True",    api["pilar2_activo"])
check("pilar3_activo = True",    api["pilar3_activo"])
check("f₀ = 141.7001",          abs(api["f0"] - 141.7001) < 1e-4)
check("n_decadas = 29",         api["n_decadas"] == 29)
check("axiomas es dict",         isinstance(api["axiomas"], dict))
check("axiomas 4 entradas",      len(api["axiomas"]) == 4)
check("descripcion str",         isinstance(api["descripcion"], str))

# Claves completas
claves = [
    "sello_activo", "psi_trinity",
    "psi_pilar1", "psi_pilar2", "psi_pilar3",
    "pilar1_activo", "pilar2_activo", "pilar3_activo",
    "f0", "n_decadas", "axiomas", "descripcion",
]
check("Claves completas", all(k in api for k in claves))

# Idempotencia
api2 = trinity_qcal_activar()
check("Idempotencia psi_trinity",
      abs(api["psi_trinity"] - api2["psi_trinity"]) < 1e-10)

# Todos los pilares ≥ 0.888
check("API psi_pilar1 ≥ 0.888", api["psi_pilar1"] >= 0.888,
      f"psi_pilar1={api['psi_pilar1']:.6f}")
check("API psi_pilar2 ≥ 0.888", api["psi_pilar2"] >= 0.888,
      f"psi_pilar2={api['psi_pilar2']:.6f}")
check("API psi_pilar3 ≥ 0.888", api["psi_pilar3"] >= 0.888,
      f"psi_pilar3={api['psi_pilar3']:.6f}")

# ============================================================================
# Resumen final
# ============================================================================

total = _pass + _fail
print(f"\n{'═' * 60}")
print(f"  RESULTADO FINAL: {_pass}/{total} verificaciones aprobadas")
if _fail == 0:
    print(f"  ✅ SELLO ∴T∞³ ACTIVADO — Trinity QCAL operativa")
    print(f"     Ψ_trinity={api['psi_trinity']:.6f}")
    print(f"     Pilar I  (∴PE∞³):  Ψ={api['psi_pilar1']:.6f}")
    print(f"     Pilar II (∴PDS∞³): Ψ={api['psi_pilar2']:.6f}")
    print(f"     Pilar III(∴PN∞³):  Ψ={api['psi_pilar3']:.6f}")
else:
    print(f"  ❌ {_fail} verificación(es) fallida(s)")
print(f"{'═' * 60}\n")

sys.exit(0 if _fail == 0 else 1)
