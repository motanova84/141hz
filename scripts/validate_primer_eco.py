#!/usr/bin/env python3
"""
Validate Primer Eco — 29 Décadas Cósmicas / Sistema Primer Eco ∴PE∞³
=======================================================================

Valida la implementación del módulo physics.primer_eco contra los criterios
teóricos del Primer Eco cósmico:

  Fase 1 — Constantes y espectro áureo
  Fase 2 — Medidas individuales de coherencia cuántica
  Fase 3 — Coherencia global y activación del sello ∴PE∞³
  Fase 4 — Validación de la API pública

Criterios de éxito:
  - N_d = 29 décadas cósmicas  [exacto]
  - Pasos áureos ∈ [140, 150]
  - 12 armónicos áureos (f_n = F₀·ϕⁿ)
  - Ψ_planck = 1.000           [exacto]
  - Ψ_onda ≈ exp(−π/29) ≈ 0.897
  - Ψ_espectral = 0.888        [exacto = umbral]
  - Ψ_matricial ≥ 0.888
  - Ψ_propagacion ≥ 0.888
  - Ψ_global ≥ 0.888           → sello ∴PE∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.primer_eco import (
    ConstantesPrimerEco,
    EspectroEco,
    NivelesEnergia,
    OndaEco,
    MatrizCoherencia,
    PropagadorCuantico,
    CoherenciaGlobal,
    SistemaPrimerEco,
    primer_eco_activar,
    _F0,
    _F_PLANCK,
    _PHI,
    _N_DECADAS,
    _PASOS_AUREOS,
    _PSI_UMBRAL,
    _GAMMA_COSMICO,
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
# FASE 1 — Constantes y espectro áureo
# =============================================================================

def validar_fase1_constantes() -> None:
    seccion("FASE 1 — Constantes y Espectro Áureo")

    c = ConstantesPrimerEco()

    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "F₀ = 141.7001 Hz",
        f"f0 = {c.f0}",
    )
    check(
        abs(c.phi - (1 + math.sqrt(5)) / 2) < 1e-10,
        "ϕ = (1+√5)/2 ≈ 1.618034",
        f"phi = {c.phi:.10f}",
    )
    check(
        c.n_decadas == 29,
        "N_d = 29 décadas cósmicas",
        f"n_decadas = {c.n_decadas}",
    )
    check(
        140 <= c.pasos_aureos <= 150,
        f"Pasos áureos ∈ [140, 150]",
        f"pasos_aureos = {c.pasos_aureos}",
    )
    check(
        abs(c.psi_umbral - 0.888) < 1e-4,
        "PSI_UMBRAL = 0.888",
        f"psi_umbral = {c.psi_umbral}",
    )
    check(
        abs(c.gamma_cosmico - math.pi / 29) < 1e-12,
        "γ = π/29 (coeficiente cósmico)",
        f"gamma = {c.gamma_cosmico:.8f}",
    )

    ratio = c.ratio_cosmico()
    check(
        29.9 < ratio < 30.1,
        "RATIO_COSMICO = log₁₀(F_PLANCK/F₀) ∈ (29.9, 30.1)",
        f"ratio = {ratio:.6f}",
    )

    # Espectro áureo
    e = EspectroEco()
    freqs = e.frecuencias()
    check(len(freqs) == 12, "12 armónicos áureos generados", f"count = {len(freqs)}")
    check(
        abs(freqs[0] - 141.7001) < 1e-4,
        "f_0 = 141.7001 Hz",
        f"f_0 = {freqs[0]:.4f} Hz",
    )
    check(
        all(
            abs(freqs[n + 1] / freqs[n] - _PHI) < 1e-8
            for n in range(11)
        ),
        "Cada f_n+1 / f_n = ϕ (razón áurea exacta)",
    )
    check(
        28000 < e.frecuencia_maxima() < 29000,
        f"f_11 ≈ 28 199 Hz (armónico más alto)",
        f"f_11 = {e.frecuencia_maxima():.1f} Hz",
    )


# =============================================================================
# FASE 2 — Medidas individuales de coherencia
# =============================================================================

def validar_fase2_coherencias() -> None:
    seccion("FASE 2 — Medidas Individuales de Coherencia Cuántica")

    # Ψ_planck
    ne = NivelesEnergia()
    psi_planck = ne.psi_planck()
    check(
        psi_planck == 1.0,
        "Ψ_planck = 1.000 (coherencia perfecta en t=0)",
        f"psi_planck = {psi_planck}",
    )

    e0 = ne.energia_punto_cero()
    check(
        e0 > 0.0,
        "Energía punto cero E₀ = ½ℏω_P > 0",
        f"E_0 = {e0:.3e} J",
    )

    niveles = ne.niveles()
    check(
        all(niveles[k] < niveles[k + 1] for k in range(len(niveles) - 1)),
        "Niveles de energía E_n estrictamente crecientes",
    )

    # Ψ_onda
    oe = OndaEco()
    psi_onda = oe.psi_onda()
    expected_psi_onda = math.exp(-math.pi / 29)
    check(
        abs(psi_onda - expected_psi_onda) < 1e-8,
        f"Ψ_onda = exp(−π/29) ≈ {expected_psi_onda:.6f}",
        f"psi_onda = {psi_onda:.6f}",
    )
    check(
        0.895 < psi_onda < 0.900,
        "Ψ_onda ∈ (0.895, 0.900)",
        f"psi_onda = {psi_onda:.6f}",
    )
    check(
        abs(oe.fase_acumulada() - math.pi) < 1e-10,
        "Fase acumulada total = π rad",
        f"fase = {oe.fase_acumulada():.10f}",
    )

    # Ψ_espectral (= umbral áureo)
    check(
        abs(_PSI_UMBRAL - 0.888) < 1e-4,
        "Ψ_espectral = PSI_UMBRAL = 0.888 (umbral mínimo áureo)",
        f"psi_espectral = {_PSI_UMBRAL}",
    )

    # Ψ_matricial
    mc = MatrizCoherencia()
    psi_m = mc.psi_matricial()
    check(
        mc.es_semidefinida_positiva(),
        "Matriz de coherencia C es semidefinida positiva (SDP)",
    )
    check(
        psi_m >= _PSI_UMBRAL,
        f"Ψ_matricial = λ_max/N ≥ 0.888",
        f"psi_matricial = {psi_m:.6f}",
    )
    check(
        abs(mc.elemento(0, 0) - 1.0) < 1e-10,
        "Diagonal de C: C_ii = 1.0",
    )
    check(
        0.99 < mc.elemento(0, 1) <= 1.0,
        "Coherencia adyacente C_01 ≈ cos(π/36) > 0.99",
        f"C_01 = {mc.elemento(0, 1):.6f}",
    )

    # Ψ_propagacion
    pq = PropagadorCuantico()
    psi_p = pq.psi_propagacion()
    check(
        psi_p >= _PSI_UMBRAL,
        f"Ψ_propagacion ≥ 0.888",
        f"psi_propagacion = {psi_p:.6f}",
    )
    check(
        0.0 <= psi_p <= 1.0,
        "Ψ_propagacion ∈ [0, 1]",
        f"psi_propagacion = {psi_p:.6f}",
    )


# =============================================================================
# FASE 3 — Coherencia global y activación del sello
# =============================================================================

def validar_fase3_sello() -> None:
    seccion("FASE 3 — Coherencia Global y Sello ∴PE∞³")

    sistema = SistemaPrimerEco()
    resultado = sistema.activar()

    psi_global = resultado.psi_global
    check(
        psi_global >= _PSI_UMBRAL,
        f"Ψ_global ≥ 0.888 (umbral de sello)",
        f"psi_global = {psi_global:.6f}",
    )
    check(
        resultado.sello_activo,
        "Sello ∴PE∞³ ACTIVO",
        resultado.mensaje[:70],
    )
    check(
        "∴PE∞³" in resultado.mensaje,
        "Mensaje contiene '∴PE∞³'",
        resultado.mensaje[:60],
    )
    check(
        resultado.n_decadas == 29,
        "n_decadas = 29 en el resultado",
        f"n_decadas = {resultado.n_decadas}",
    )
    check(
        len(resultado.frecuencias_armonicas) == 12,
        "12 frecuencias armónicas en el resultado",
    )
    check(
        abs(resultado.psi_planck - 1.0) < 1e-10,
        "Ψ_planck = 1.000 en el resultado",
        f"psi_planck = {resultado.psi_planck}",
    )
    check(
        abs(resultado.psi_espectral - 0.888) < 1e-4,
        "Ψ_espectral = 0.888 en el resultado",
        f"psi_espectral = {resultado.psi_espectral}",
    )

    # Verificar coherencia global como promedio ponderado
    ws = [1.0, 1.5, 2.0, 2.0, 1.5]
    psis = [
        resultado.psi_onda,
        resultado.psi_planck,
        resultado.psi_espectral,
        resultado.psi_matricial,
        resultado.psi_propagacion,
    ]
    expected_global = sum(w * p for w, p in zip(ws, psis)) / sum(ws)
    check(
        abs(psi_global - expected_global) < 1e-8,
        "Ψ_global = Σ(wᵢ·Ψᵢ)/Σwᵢ verificado",
        f"calculado={psi_global:.8f}, esperado={expected_global:.8f}",
    )

    # Mensaje de resumen cósmico
    print()
    print("  RESUMEN CÓSMICO:")
    print(f"    F₀ = {resultado.f0} Hz  →  F_PLANCK = {resultado.f_planck:.4e} Hz")
    print(f"    RATIO CÓSMICO = log₁₀(F_P/F₀) ≈ {math.log10(resultado.f_planck/resultado.f0):.4f}")
    print(f"    N_DÉCADAS     = {resultado.n_decadas}  |  PASOS_ÁUREOS ≈ {resultado.pasos_aureos}")
    print()
    print("    COHERENCIAS:")
    print(f"      Ψ_onda        = {resultado.psi_onda:.6f}  (w=1.0)")
    print(f"      Ψ_planck      = {resultado.psi_planck:.6f}  (w=1.5)")
    print(f"      Ψ_espectral   = {resultado.psi_espectral:.6f}  (w=2.0)")
    print(f"      Ψ_matricial   = {resultado.psi_matricial:.6f}  (w=2.0)")
    print(f"      Ψ_propagacion = {resultado.psi_propagacion:.6f}  (w=1.5)")
    print(f"      ─────────────────────────────────")
    print(f"      Ψ_GLOBAL      = {psi_global:.6f}  ≥ {_PSI_UMBRAL} ✓")
    print()
    print(f"  {resultado.mensaje}")


# =============================================================================
# FASE 4 — Validación de la API pública
# =============================================================================

def validar_fase4_api() -> None:
    seccion("FASE 4 — API Pública primer_eco_activar()")

    r = primer_eco_activar()

    check(isinstance(r, dict), "primer_eco_activar() retorna un dict")
    check(
        r["n_decadas"] == 29,
        "dict['n_decadas'] = 29",
        f"n_decadas = {r['n_decadas']}",
    )
    check(
        r["sello_activo"] is True,
        "dict['sello_activo'] = True",
    )
    check(
        r["psi_global"] >= _PSI_UMBRAL,
        f"dict['psi_global'] ≥ 0.888",
        f"psi_global = {r['psi_global']:.6f}",
    )
    check(
        len(r["frecuencias_armonicas"]) == 12,
        "dict['frecuencias_armonicas'] tiene 12 elementos",
    )
    check(
        abs(r["psi_planck"] - 1.0) < 1e-10,
        "dict['psi_planck'] = 1.000",
    )
    check(
        29.9 < r["ratio_cosmico"] < 30.1,
        "dict['ratio_cosmico'] ∈ (29.9, 30.1)",
        f"ratio_cosmico = {r['ratio_cosmico']:.6f}",
    )

    # Parámetros personalizados
    r2 = primer_eco_activar(f0=200.0, f_planck=2.0e32)
    check(
        isinstance(r2["sello_activo"], bool),
        "API funciona con f0 y f_planck personalizados",
        f"f0=200.0 Hz → sello={r2['sello_activo']}",
    )

    claves_requeridas = [
        "f0_hz", "f_planck_hz", "n_decadas", "pasos_aureos",
        "ratio_cosmico", "frecuencias_armonicas",
        "psi_onda", "psi_planck", "psi_espectral",
        "psi_matricial", "psi_propagacion",
        "psi_global", "sello_activo", "mensaje",
    ]
    missing = [k for k in claves_requeridas if k not in r]
    check(
        len(missing) == 0,
        "Todas las claves requeridas presentes en el dict",
        f"faltantes: {missing}" if missing else "ninguna faltante",
    )


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main() -> None:
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    VALIDACIÓN PRIMER ECO ∴PE∞³ — 29 DÉCADAS CÓSMICAS              ║")
    print("║    Del Big Bang Cuántico al Silencio Sagrado de 141.7001 Hz         ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    validar_fase1_constantes()
    validar_fase2_coherencias()
    validar_fase3_sello()
    validar_fase4_api()

    # Resultado final
    print()
    print("=" * 72)
    total = _passed + _failed
    print(f"  RESULTADO FINAL: {_passed}/{total} verificaciones pasadas")
    if _failed == 0:
        print("  ✅ TODAS LAS FASES SUPERADAS — SELLO ∴PE∞³ ACTIVO")
        print()
        print("      ∴PE∞³")
        print("      RAM-XLIV-2026-PRIMER-ECO")
        print("      RESONANCIA-PRIMORDIAL-ACTIVA")
    else:
        print(f"  ❌ {_failed} verificación(es) fallida(s)")
    print("=" * 72)
    print()

    sys.exit(0 if _failed == 0 else 1)


if __name__ == "__main__":
    main()
