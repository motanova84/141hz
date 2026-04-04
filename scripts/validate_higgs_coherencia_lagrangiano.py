#!/usr/bin/env python3
"""
Validate Higgs-Coherencia Lagrangiano — ∴HCL∞³
===============================================================================

Valida la implementación del módulo physics.higgs_coherencia_lagrangiano
contra los criterios teóricos del Lagrangiano de Interacción Higgs-Coherencia:

  Fase 1 — Constantes fundamentales y campos
  Fase 2 — Lagrangiano de interacción y masa modulada
  Fase 3 — Antena ADN-Z y coherencia global
  Fase 4 — Validación de la API pública y certificación AURON

Criterios de éxito:
  - f₀ = 141.7001 Hz                [exacto]
  - m_H = 125.25 GeV/c²            [exacto]
  - g_eff = 0.053                   [perturbativo: < 10%]
  - μ_ψH = 0.025 GeV²              [orden de magnitud]
  - Δm = m_H × g_eff ≈ 6.64 GeV/c² [calculado]
  - m_min ≈ 118.61 GeV/c²          [calculado]
  - m_max ≈ 131.89 GeV/c²          [calculado]
  - T ≈ 7.06 ms                     [período de modulación]
  - Q_DNA ~ 6.22 × 10¹⁴            [factor de calidad ADN-Z]
  - Ψ_global ≥ 0.888               → sello ∴HCL∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVII-2026-HIGGS-COHERENCE
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.higgs_coherencia_lagrangiano import (
    ConstantesHiggsCoherencia,
    CampoHiggs,
    CampoCoherencia,
    LagrangianoInteraccion,
    MasaEfectivaModulada,
    AntenaDNAZ,
    CoherenciaHiggsCoherencia,
    SistemaHiggsCoherenciaLagrangiano,
    higgs_coherencia_activar,
    _F0,
    _M_HIGGS_GEV,
    _G_EFF,
    _MU_PSI_H_GEV2,
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
# FASE 1 — Constantes fundamentales y campos
# =============================================================================

def validar_fase1_constantes() -> None:
    seccion("FASE 1 — Constantes Fundamentales y Campos")

    # Constantes
    c = ConstantesHiggsCoherencia()

    check(
        abs(c.f0 - 141.7001) < 1e-4,
        "f₀ = 141.7001 Hz",
        f"f0 = {c.f0}",
    )
    check(
        abs(c.m_higgs_gev - 125.25) < 0.01,
        "m_H = 125.25 GeV/c²",
        f"m_higgs_gev = {c.m_higgs_gev}",
    )
    check(
        abs(c.g_eff - 0.053) < 1e-3,
        "g_eff = 0.053",
        f"g_eff = {c.g_eff}",
    )
    check(
        c.g_eff < 0.1,
        "g_eff < 0.1 (perturbativo)",
        f"g_eff = {c.g_eff} < 0.1 ✓",
    )
    check(
        abs(c.mu_psi_h_gev2 - 0.025) < 1e-3,
        "μ_ψH = 0.025 GeV²",
        f"mu_psi_h_gev2 = {c.mu_psi_h_gev2}",
    )
    check(
        abs(c.psi_umbral - 0.888) < 1e-3,
        "PSI_UMBRAL = 0.888",
        f"psi_umbral = {c.psi_umbral}",
    )
    check(
        abs(c.phi - (1 + math.sqrt(5)) / 2) < 1e-10,
        "ϕ = (1+√5)/2 (proporción áurea)",
        f"phi = {c.phi:.10f}",
    )
    check(
        c.es_perturbativa(),
        "Modulación perturbativa (Δm/m_H < 10%)",
    )

    # Amplitud de modulación
    delta_m = c.amplitud_modulacion_gev()
    check(
        abs(delta_m - 6.64) < 0.1,
        f"Δm = m_H × g_eff ≈ 6.64 GeV/c²",
        f"delta_m = {delta_m:.2f} GeV/c²",
    )

    # Campo de Higgs
    h = CampoHiggs()
    check(
        abs(h.vev_gev - 246.22) < 0.01,
        "VEV Higgs = 246.22 GeV",
        f"vev_gev = {h.vev_gev}",
    )
    check(
        h.densidad_vacio() > 0,
        "Densidad de vacío |H|² > 0",
        f"densidad_vacio = {h.densidad_vacio():.2f} GeV²",
    )
    check(
        0 < h.psi_campo() <= 1,
        "Coherencia campo Higgs Ψ_H ∈ (0, 1]",
        f"psi_campo = {h.psi_campo():.6f}",
    )

    # Campo de coherencia
    psi = CampoCoherencia()
    check(
        abs(psi.frecuencia_hz - 141.7001) < 1e-4,
        "Frecuencia campo ψ = 141.7001 Hz",
        f"frecuencia_hz = {psi.frecuencia_hz}",
    )
    check(
        abs(psi.densidad_promedio() - 1.0) < 1e-10,
        "Densidad promedio ⟨|ψ|²⟩ = A² = 1",
        f"densidad_promedio = {psi.densidad_promedio()}",
    )
    check(
        psi.corriente_noesica(0) > 0,
        "Corriente noésica j > 0",
        f"j = {psi.corriente_noesica(0):.2f} rad·s⁻¹",
    )


# =============================================================================
# FASE 2 — Lagrangiano de interacción y masa modulada
# =============================================================================

def validar_fase2_lagrangiano() -> None:
    seccion("FASE 2 — Lagrangiano de Interacción y Masa Modulada")

    # Lagrangiano
    L = LagrangianoInteraccion()

    check(
        L.termino_portal(0.0) < 0,
        "Término portal < 0 (acoplamiento atractivo)",
        f"L_portal = {L.termino_portal(0.0):.4e}",
    )
    check(
        L.termino_efectivo(0.0) < 0,
        "Término efectivo < 0",
        f"L_efectivo = {L.termino_efectivo(0.0):.4e}",
    )
    check(
        L.densidad_lagrangiana(0.0) < 0,
        "Densidad lagrangiana ℒ_int < 0",
        f"L_total = {L.densidad_lagrangiana(0.0):.4e}",
    )
    check(
        L.es_perturbativo(),
        "Acoplamiento perturbativo (g_eff < 1)",
    )
    check(
        L.psi_lagrangiano() > 0.9,
        "Coherencia Lagrangiano Ψ_L > 0.9",
        f"psi_lagrangiano = {L.psi_lagrangiano():.6f}",
    )

    # Acción efectiva
    accion = L.accion_efectiva(0.01)
    check(
        math.isfinite(accion),
        "Acción efectiva finita",
        f"S = {accion:.6e}",
    )

    # Masa efectiva modulada
    m = MasaEfectivaModulada()

    check(
        abs(m.m_higgs_gev - 125.25) < 0.01,
        "Masa base m_H = 125.25 GeV/c²",
        f"m_higgs_gev = {m.m_higgs_gev}",
    )
    check(
        abs(m.frecuencia_hz - 141.7001) < 1e-4,
        "Frecuencia modulación f = 141.7001 Hz",
        f"frecuencia_hz = {m.frecuencia_hz}",
    )

    m_min = m.masa_minima()
    m_max = m.masa_maxima()
    check(
        abs(m_min - 118.61) < 0.1,
        "Masa mínima m_min ≈ 118.61 GeV/c²",
        f"m_min = {m_min:.2f} GeV/c²",
    )
    check(
        abs(m_max - 131.89) < 0.1,
        "Masa máxima m_max ≈ 131.89 GeV/c²",
        f"m_max = {m_max:.2f} GeV/c²",
    )

    delta_m = m.amplitud_modulacion()
    check(
        abs(delta_m - 6.64) < 0.1,
        "Amplitud Δm ≈ 6.64 GeV/c²",
        f"delta_m = {delta_m:.2f} GeV/c²",
    )

    T = m.periodo_s()
    T_ms = T * 1000
    check(
        abs(T_ms - 7.06) < 0.1,
        "Período T ≈ 7.06 ms",
        f"T = {T_ms:.2f} ms",
    )

    check(
        m.fraccion_modulacion() < 0.1,
        "Fracción Δm/m_H < 10% (perturbativa)",
        f"fraccion = {m.fraccion_modulacion():.3f} = {m.fraccion_modulacion()*100:.1f}%",
    )

    check(
        m.psi_modulacion() > 0.9,
        "Coherencia modulación Ψ_m > 0.9",
        f"psi_modulacion = {m.psi_modulacion():.6f}",
    )

    # Verificar periodicidad
    t = 0.001
    m_t = m.masa_efectiva(t)
    m_t_T = m.masa_efectiva(t + T)
    check(
        abs(m_t - m_t_T) < 1e-8,
        "Periodicidad: m*(t+T) = m*(t)",
        f"Δm = {abs(m_t - m_t_T):.2e}",
    )


# =============================================================================
# FASE 3 — Antena ADN-Z y coherencia global
# =============================================================================

def validar_fase3_coherencia() -> None:
    seccion("FASE 3 — Antena ADN-Z y Coherencia Global")

    # Antena ADN-Z
    dna = AntenaDNAZ()

    check(
        abs(dna.pitch_m - 34e-10) < 1e-15,
        "Pitch ADN-Z = 34 Å",
        f"pitch = {dna.pitch_m * 1e10:.1f} Å",
    )
    check(
        abs(dna.radio_m - 9e-10) < 1e-15,
        "Radio ADN-Z = 9 Å",
        f"radio = {dna.radio_m * 1e10:.1f} Å",
    )
    check(
        abs(dna.frecuencia_resonancia_hz - 141.7001) < 1e-4,
        "Frecuencia resonancia = 141.7001 Hz",
        f"f_res = {dna.frecuencia_resonancia_hz}",
    )

    lambda_res = dna.longitud_onda_resonancia_m()
    lambda_km = lambda_res / 1000
    check(
        abs(lambda_km - 2116) < 10,
        "Longitud de onda λ ≈ 2116 km",
        f"λ = {lambda_km:.0f} km",
    )

    Q = dna.factor_calidad()
    check(
        Q > 1e14,
        "Factor de calidad Q ~ 10¹⁴",
        f"Q = {Q:.2e}",
    )

    check(
        dna.psi_antena() > 0.5,
        "Coherencia antena Ψ_antena > 0.5",
        f"psi_antena = {dna.psi_antena():.6f}",
    )

    # Coherencia del sistema
    coherencia = CoherenciaHiggsCoherencia()
    coherencias = coherencia.coherencias_individuales()

    print("\n  Coherencias individuales:")
    for nombre, valor in coherencias.items():
        print(f"    {nombre} = {valor:.6f}")

    check(
        all(0 <= v <= 1 for v in coherencias.values()),
        "Todas las coherencias ∈ [0, 1]",
    )

    psi_global = coherencia.psi_global()
    check(
        psi_global >= 0.888,
        f"Ψ_global ≥ 0.888",
        f"psi_global = {psi_global:.6f}",
    )

    check(
        coherencia.sello_activo(),
        "Sello ∴HCL∞³ ACTIVO",
    )

    validacion = coherencia.validar()
    check(
        validacion['sello_activo'],
        "Validación confirma sello activo",
    )
    check(
        validacion['diferencia_umbral'] >= 0,
        f"Diferencia sobre umbral ≥ 0",
        f"Δ = {validacion['diferencia_umbral']:.6f}",
    )


# =============================================================================
# FASE 4 — API pública y certificación AURON
# =============================================================================

def validar_fase4_api() -> None:
    seccion("FASE 4 — API Pública y Certificación AURON")

    # Sistema completo
    sistema = SistemaHiggsCoherenciaLagrangiano()
    resultado = sistema.activar()

    check(
        resultado['sello'] == '∴HCL∞³',
        "Sello = '∴HCL∞³'",
    )
    check(
        resultado['ram'] == 'RAM-XLVII-2026-HIGGS-COHERENCE',
        "RAM = 'RAM-XLVII-2026-HIGGS-COHERENCE'",
    )
    check(
        resultado['version'] == '1.0.0',
        "Versión = '1.0.0'",
    )
    check(
        resultado['sello_activo'],
        "Sistema activado correctamente",
    )
    check(
        resultado['perturbativo'],
        "Régimen perturbativo confirmado",
    )

    # API pública
    api_resultado = higgs_coherencia_activar()

    check(
        isinstance(api_resultado, dict),
        "higgs_coherencia_activar() retorna dict",
    )
    check(
        abs(api_resultado['f0_hz'] - 141.7001) < 1e-4,
        "API: f0_hz = 141.7001 Hz",
    )
    check(
        abs(api_resultado['m_higgs_gev'] - 125.25) < 0.01,
        "API: m_higgs_gev = 125.25 GeV/c²",
    )
    check(
        api_resultado['sello_activo'],
        "API: sello_activo = True",
    )
    check(
        api_resultado['psi_global'] >= 0.888,
        f"API: psi_global ≥ 0.888",
        f"psi_global = {api_resultado['psi_global']:.6f}",
    )

    # Certificación AURON
    coherencia = CoherenciaHiggsCoherencia()
    cert = coherencia.certificacion_auron()

    check(
        "AURON" in cert,
        "Certificación contiene 'AURON'",
    )
    check(
        "ACTIVO" in cert,
        "Certificación indica 'ACTIVO'",
    )
    check(
        "∴HCL∞³" in cert,
        "Certificación contiene sello '∴HCL∞³'",
    )
    check(
        "RAM-XLVII-2026-HIGGS-COHERENCE" in cert,
        "Certificación contiene RAM correcto",
    )

    # Verificar todas las claves de la API
    expected_keys = {
        'sello', 'ram', 'version', 'f0_hz', 'm_higgs_gev', 'g_eff',
        'mu_psi_h_gev2', 'delta_m_gev', 'm_min_gev', 'm_max_gev',
        'fraccion_modulacion', 'periodo_s', 'periodo_ms', 'q_factor_dna',
        'lambda_resonancia_m', 'lambda_resonancia_km', 'L_total',
        'L_portal', 'L_efectivo', 'coherencias', 'psi_global',
        'psi_umbral', 'sello_activo', 'perturbativo', 'certificacion'
    }
    api_keys = set(api_resultado.keys())
    check(
        expected_keys.issubset(api_keys),
        "API contiene todas las claves esperadas",
        f"Claves: {len(api_keys)} (esperadas: {len(expected_keys)})",
    )


# =============================================================================
# RESUMEN FINAL
# =============================================================================

def imprimir_resumen() -> None:
    global _passed, _failed
    total = _passed + _failed
    porcentaje = (_passed / total * 100) if total > 0 else 0

    seccion("RESUMEN FINAL — Validación ∴HCL∞³")

    print(f"\n  Total de validaciones: {total}")
    print(f"  ✅ Pasadas: {_passed}")
    print(f"  ❌ Fallidas: {_failed}")
    print(f"  Porcentaje: {porcentaje:.1f}%")

    if _failed == 0:
        print("\n" + "=" * 72)
        print("  ∴HCL∞³ CERTIFICACIÓN AURON — VALIDACIÓN COMPLETA")
        print("=" * 72)
        print("  Estado: ✅ TODAS LAS VALIDACIONES PASADAS")
        print("  Sello: ∴HCL∞³ ACTIVO")
        print("  RAM: RAM-XLVII-2026-HIGGS-COHERENCE")
        print("  Versión: 1.0.0")
        print("=" * 72)
    else:
        print("\n  ⚠️ ADVERTENCIA: Algunas validaciones fallaron")

    print()


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def main() -> int:
    """Ejecuta todas las validaciones y retorna código de salida."""
    print("\n" + "=" * 72)
    print("  VALIDACIÓN — LAGRANGIANO HIGGS-COHERENCIA QCAL ∞³")
    print("  Sello: ∴HCL∞³ | RAM: RAM-XLVII-2026-HIGGS-COHERENCE")
    print("=" * 72)

    validar_fase1_constantes()
    validar_fase2_lagrangiano()
    validar_fase3_coherencia()
    validar_fase4_api()

    imprimir_resumen()

    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
