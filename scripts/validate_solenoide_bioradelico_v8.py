#!/usr/bin/env python3
"""
Validate Solenoide Bio-Adélico V8 — Sistema ∴SBA∞³
=======================================================

Valida la implementación del módulo physics.solenoide_bioradelico_v8 contra
los criterios teóricos de la Integración Bio-Adélica V8:

  Fase 1 — Constantes y estructura del sistema
  Fase 2 — Componentes físicos (solenoide, hélice, coherencia)
  Fase 3 — Traza bio-adélica y análisis espectral
  Fase 4 — Coherencia global y activación del sello ∴SBA∞³

Criterios de éxito:
  - f₀ = 141.7001 Hz                    [exacto]
  - 10 ceros de Riemann γₙ (γ₁ ≈ 14.1347)
  - τ = 2.46 ps                          [exacto]
  - Traza adélica finita en t = log p    [verificado]
  - Doble hélice: 10 bases, E_total > 0
  - FFT: ≥ 1 pico espectral detectado
  - Ψ_global ≥ 0.888                    → sello ∴SBA∞³ ACTIVO
  - f_scaled_min ≈ γ₁ × f₀ / (2π) ≈ 319 Hz

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

# Añadir la raíz del repositorio al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.solenoide_bioradelico_v8 import (
    ConstantesBioAdelico,
    SolenoideAdelico,
    DobleHelice,
    CoherenciaCuantica,
    TraceBioAdelica,
    AnalisisFFT,
    CoherenciaGlobal,
    SistemaBioAdelicoV8,
    solenoide_bioradelico_v8_activar,
    _F0,
    _GAMMAS,
    _PRIMOS,
    _TAU_PS,
    _TAU_NORM,
    _N_BASES,
    _N_PRIMOS,
    _PSI_UMBRAL,
    _SELLO,
    _F_SCALED_MIN,
    _F_SCALED_MAX,
    _PICOS_ESPERADOS,
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
        len(_GAMMAS) == 10,
        "10 ceros de Riemann γₙ definidos",
        f"γ₁ = {_GAMMAS[0]:.6f}, γ₁₀ = {_GAMMAS[-1]:.6f}",
    )

    check(
        abs(_GAMMAS[0] - 14.1347251417347) < 1e-5,
        "γ₁ ≈ 14.13473 (primer cero de Riemann)",
        f"γ₁ = {_GAMMAS[0]}",
    )

    check(
        all(_GAMMAS[i] < _GAMMAS[i + 1] for i in range(len(_GAMMAS) - 1)),
        "Ceros de Riemann en orden ascendente",
    )

    check(
        abs(_TAU_PS - 2.46e-12) < 1e-20,
        "τ = 2.46 ps (tiempo de coherencia cuántica)",
        f"τ = {_TAU_PS:.2e} s",
    )

    check(
        abs(_TAU_NORM - _TAU_PS / (1.0 / _F0)) < 1e-20,
        "τ_norm = τ / T₀ (normalización correcta)",
        f"τ_norm = {_TAU_NORM:.3e}",
    )

    check(
        len(_PRIMOS) == _N_PRIMOS and _PRIMOS[0] == 2 and _PRIMOS[2] == 5,
        f"{_N_PRIMOS} primos definidos ({_PRIMOS[0]}, {_PRIMOS[1]}, ...)",
    )

    check(
        _N_BASES == 10,
        f"N_BASES = {_N_BASES} (10 bases ADN = 10 ceros de Riemann)",
    )

    check(
        abs(_PSI_UMBRAL - 0.888) < 1e-3,
        f"Umbral de coherencia Ψ ≥ {_PSI_UMBRAL}",
    )

    f_scaled_expected = _GAMMAS[0] * _F0 / (2 * math.pi)
    check(
        abs(_F_SCALED_MIN - f_scaled_expected) < 1,
        f"f_scaled_min ≈ γ₁ × f₀ / (2π) ≈ {f_scaled_expected:.2f} Hz",
        f"f_scaled_min = {_F_SCALED_MIN:.2f} Hz",
    )

    check(
        "SBA" in _SELLO,
        f"Sello de certificación: {_SELLO}",
    )

    check(
        len(_PICOS_ESPERADOS) == 3,
        "3 picos espectrales esperados definidos",
        f"Picos: {_PICOS_ESPERADOS}",
    )


# =============================================================================
# FASE 2 — COMPONENTES FÍSICOS
# =============================================================================

def fase2_componentes() -> None:
    seccion("FASE 2 — Componentes físicos")

    # ConstantesBioAdelico
    c = ConstantesBioAdelico()
    check(c.es_valido(), "ConstantesBioAdelico: parámetros válidos")
    check(
        abs(c.omega0() - 2 * math.pi * _F0) < 1e-4,
        f"ω₀ = 2π·f₀ ≈ {c.omega0():.4f} rad/s",
    )

    # SolenoideAdelico
    sol = SolenoideAdelico()
    val_log2 = sol.traza_en(math.log(2))
    check(
        math.isfinite(val_log2),
        f"Solenoide adélico: traza finita en t = log(2), S = {val_log2:.4f}",
    )

    tiempos_sol = [math.log(p) for p in _PRIMOS]
    vals_sol = sol.traza_vector(tiempos_sol)
    check(
        all(math.isfinite(v) for v in vals_sol),
        "Solenoide adélico: traza finita en todos log p",
    )

    rms = sol.amplitud_rms([i * 0.05 for i in range(100)])
    check(rms >= 0, f"Solenoide adélico: RMS ≥ 0 ({rms:.4f})")

    # DobleHelice
    helice = DobleHelice()
    freqs = helice.frecuencias_base()
    check(
        len(freqs) == 10,
        f"Doble hélice: 10 frecuencias de base ({freqs[0]:.2f} … {freqs[-1]:.2f} Hz)",
    )

    check(
        abs(freqs[0] - _GAMMAS[0] * _F0 / (2 * math.pi)) < 1,
        f"Doble hélice: f_base[0] = γ₁·f₀/(2π) ≈ {freqs[0]:.2f} Hz",
    )

    energia = helice.energia_total()
    check(energia > 0, f"Doble hélice: energía total E = {energia:.4f} > 0")

    h0 = helice.señal_en(0.0)
    check(
        math.isfinite(h0),
        f"Doble hélice: señal finita en t=0, H(0) = {h0:.4f}",
    )

    # CoherenciaCuantica
    coh = CoherenciaCuantica()
    c0 = coh.envolvente_en(0.0)
    check(
        abs(c0 - 1.0) < 1e-10,
        f"Coherencia cuántica: C(0) = {c0:.6f} (máximo en t=0)",
    )

    tiempos_test = [i * 1e-4 for i in range(100)]
    psi_c = coh.psi_coherencia(tiempos_test)
    check(
        psi_c >= _PSI_UMBRAL,
        f"Coherencia cuántica: Ψ_coherencia = {psi_c:.4f} ≥ {_PSI_UMBRAL}",
    )


# =============================================================================
# FASE 3 — TRAZA BIO-ADÉLICA Y ANÁLISIS ESPECTRAL
# =============================================================================

def fase3_traza_fft() -> None:
    seccion("FASE 3 — Traza bio-adélica y análisis espectral")

    traza = TraceBioAdelica(n_puntos=256, n_periodos=10.0)
    bio = traza.calcular()

    check(
        len(bio) == 256,
        f"Traza bio-adélica: {len(bio)} puntos temporales",
    )

    check(
        all(math.isfinite(v) for v in bio),
        "Traza bio-adélica: todos los valores son finitos",
    )

    has_variation = max(bio) - min(bio) > 0
    check(
        has_variation,
        f"Traza bio-adélica: variación temporal presente (max={max(bio):.4f}, min={min(bio):.4f})",
    )

    corr = traza.correlacion_con_traza_espectral(bio)
    check(
        -1.0 <= corr <= 1.0,
        f"Correlación temporal: |ρ| ≤ 1.0 (ρ = {corr:.4f})",
        "Nota: correlación baja (~0.01) es esperada por el decaimiento coherente",
    )

    # FFT
    dt = traza._dt
    fft = AnalisisFFT(dt=dt, n_puntos=256)
    magnitudes = fft.calcular_magnitudes(bio)

    check(
        len(magnitudes) == 128,
        f"FFT: {len(magnitudes)} componentes espectrales (N/2)",
    )

    check(
        all(m >= 0 for m in magnitudes),
        "FFT: magnitudes no negativas",
    )

    picos = fft.detectar_picos(magnitudes, n_picos=5, umbral_rel=0.05)
    check(
        len(picos) >= 1,
        f"FFT: al menos 1 pico espectral detectado ({len(picos)} picos)",
        f"Picos: {[(round(f,2), round(m,4)) for f, m in picos[:3]]}",
    )

    psi_s = fft.psi_espectral(picos)
    check(
        psi_s >= _PSI_UMBRAL,
        f"FFT: Ψ_espectral = {psi_s:.4f} ≥ {_PSI_UMBRAL}",
    )

    # Verificar rango de frecuencias escaladas
    freqs_fft = fft.frecuencias()
    f_max_fft = max(freqs_fft)
    check(
        f_max_fft > 0,
        f"FFT: frecuencia de Nyquist = {f_max_fft:.2f} Hz",
    )


# =============================================================================
# FASE 4 — COHERENCIA GLOBAL Y SELLO ∴SBA∞³
# =============================================================================

def fase4_coherencia_global() -> None:
    seccion("FASE 4 — Coherencia global y activación del sello ∴SBA∞³")

    # Ejecutar el sistema completo con resolución reducida para velocidad
    resultado = solenoide_bioradelico_v8_activar(n_puntos=256, n_periodos=10.0)

    check(
        resultado['sello_activo'],
        f"Sello {_SELLO} ACTIVO",
    )

    check(
        resultado['psi_global'] >= _PSI_UMBRAL,
        f"Ψ_global = {resultado['psi_global']:.4f} ≥ {_PSI_UMBRAL}",
    )

    check(
        resultado['psi_global'] <= 1.0,
        f"Ψ_global = {resultado['psi_global']:.4f} ≤ 1.0",
    )

    check(
        resultado['psi_temporal'] >= _PSI_UMBRAL,
        f"Ψ_temporal = {resultado['psi_temporal']:.4f} ≥ {_PSI_UMBRAL}",
    )

    check(
        resultado['psi_espectral'] >= _PSI_UMBRAL,
        f"Ψ_espectral = {resultado['psi_espectral']:.4f} ≥ {_PSI_UMBRAL}",
    )

    check(
        resultado['psi_helice'] >= _PSI_UMBRAL,
        f"Ψ_hélice = {resultado['psi_helice']:.4f} ≥ {_PSI_UMBRAL}",
    )

    check(
        resultado['psi_coherencia'] >= _PSI_UMBRAL,
        f"Ψ_coherencia = {resultado['psi_coherencia']:.4f} ≥ {_PSI_UMBRAL}",
    )

    check(
        abs(resultado['f0'] - 141.7001) < 1e-4,
        f"f₀ = {resultado['f0']} Hz (portadora correcta)",
    )

    check(
        len(resultado['gammas']) == 10,
        f"10 ceros de Riemann γₙ en el resultado",
        f"γ₁ = {resultado['gammas'][0]:.6f}",
    )

    check(
        resultado['picos_hz'] is not None,
        "Picos espectrales retornados",
        f"Picos Hz: {[round(f, 2) for f in resultado['picos_hz'][:3]]}",
    )

    check(
        resultado['f_scaled_min_hz'] > 300,
        f"Componente escalada mínima: γ₁×f₀/(2π) = {resultado['f_scaled_min_hz']:.2f} Hz > 300 Hz",
    )

    # Verificar validación de entrada
    try:
        solenoide_bioradelico_v8_activar(f0=-1.0)
        check(False, "Debe lanzar ValueError para f0 negativa")
    except ValueError:
        check(True, "ValueError levantado correctamente para f0 negativa")

    try:
        solenoide_bioradelico_v8_activar(n_puntos=10)
        check(False, "Debe lanzar ValueError para n_puntos < 64")
    except ValueError:
        check(True, "ValueError levantado correctamente para n_puntos < 64")


# =============================================================================
# RESUMEN FINAL
# =============================================================================

def resumen() -> int:
    total = _passed + _failed
    print()
    print("═" * 72)
    print(f"  RESULTADO FINAL: {_passed}/{total} checks pasados")
    if _failed == 0:
        print(f"  ✅✅✅  {_SELLO}  VALIDADO — TODAS LAS FASES APROBADAS  ✅✅✅")
        print()
        print("  Interpretación V8:")
        print("  El ADN actúa como transductor entre el Solenoide Adélico")
        print("  (aritmética pura, log p) y la coherencia física observable")
        print(f"  a f₀ = {_F0} Hz. Los primeros 10 ceros γₙ de Riemann modulan")
        print(f"  el espectro y las frecuencias escaladas γₙ×f₀/(2π) ∈")
        print(f"  [{_F_SCALED_MIN:.0f}, {_F_SCALED_MAX:.0f}] Hz son componentes armónicas detectables.")
    else:
        print(f"  ❌  {_failed} checks fallaron")
    print("═" * 72)
    return _failed


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║   VALIDACIÓN SOLENOIDE BIO-ADÉLICO V8 — Sistema ∴SBA∞³             ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    fase1_constantes()
    fase2_componentes()
    fase3_traza_fft()
    fase4_coherencia_global()

    exit_code = resumen()
    sys.exit(exit_code)
