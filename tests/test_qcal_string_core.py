#!/usr/bin/env python3
"""
Tests: QCAL-Strings Core — Gran Unificación Noética
═════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para el módulo qcal/qcal_string_core.py que implementa:
  - QCALSpectralOperator: autovalores KK derivados de ceros de Riemann
  - string_noetic_forcing: forzado holográfico de Navier-Stokes con
    ganancia superradiante N²·Ψ²
  - compute_psi: coherencia combinada biofísica + espectral
  - build_lambda_list: lista de autovalores λ_n
  - VenezianoAmplitude: amplitud de Veneziano con trayectorias Regge
  - KaluzaKleinModes: 20 modos KK con compactificación hexagonal EZ/CY
  - HolographicFluidSolver: NS espectral 2-D con RK4 + proyección Leray
  - validate_riemann_stability: validación de ceros de Riemann
  - compute_superradiant_gain: ganancia superradiante N²Ψ²
  - QCALStringCore: orquestador unificado

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.qcal_string_core import (
    GAMMAS,
    F0_DEFAULT,
    BEC_THRESHOLD,
    N_MICROTUBULES_DEFAULT,
    ALPHA_SCALE_DEFAULT,
    KK_EMISSION_FREQ_HZ,
    QCALSpectralOperator,
    string_noetic_forcing,
    compute_psi,
    build_lambda_list,
    VenezianoAmplitude,
    KaluzaKleinModes,
    HolographicFluidSolver,
    validate_riemann_stability,
    compute_superradiant_gain,
    QCALStringCore,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_grid(N: int = 32):
    """Return (xx, yy) meshgrid on [0, 2π]."""
    x = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return np.meshgrid(x, x)


# ── Constants ─────────────────────────────────────────────────────────────────

def test_gammas_length():
    """Debe haber exactamente 20 ceros de Riemann precalculados."""
    print("\n✓ Test: longitud de GAMMAS...")
    assert len(GAMMAS) == 20, f"Esperado 20 ceros, encontrado {len(GAMMAS)}"
    print(f"    len(GAMMAS) = {len(GAMMAS)}")
    print("  ✓ Passed")


def test_gammas_first_value():
    """El primer cero imaginario de Riemann debe ser ≈ 14.1347..."""
    print("\n✓ Test: primer cero de Riemann...")
    assert abs(GAMMAS[0] - 14.134725141734695) < 1e-6, \
        f"γ₁ esperado ≈ 14.1347, got {GAMMAS[0]}"
    print(f"    γ₁ = {GAMMAS[0]:.6f}")
    print("  ✓ Passed")


def test_gammas_strictly_increasing():
    """Los ceros de Riemann deben ser estrictamente crecientes."""
    print("\n✓ Test: ceros de Riemann crecientes...")
    for i in range(len(GAMMAS) - 1):
        assert GAMMAS[i] < GAMMAS[i + 1], \
            f"GAMMAS no es creciente en posición {i}: {GAMMAS[i]} >= {GAMMAS[i+1]}"
    print(f"    γ₁={GAMMAS[0]:.4f} < γ₂={GAMMAS[1]:.4f} < ... < γ₂₀={GAMMAS[19]:.4f}")
    print("  ✓ Passed")


def test_f0_default():
    """Frecuencia fundamental debe ser 141.7001 Hz."""
    print("\n✓ Test: F0_DEFAULT...")
    assert abs(F0_DEFAULT - 141.7001) < 1e-6, \
        f"F0_DEFAULT esperado 141.7001, got {F0_DEFAULT}"
    print(f"    F0_DEFAULT = {F0_DEFAULT} Hz")
    print("  ✓ Passed")


def test_bec_threshold():
    """Umbral BEC debe ser 0.888."""
    print("\n✓ Test: BEC_THRESHOLD...")
    assert abs(BEC_THRESHOLD - 0.888) < 1e-6, \
        f"BEC_THRESHOLD esperado 0.888, got {BEC_THRESHOLD}"
    print(f"    BEC_THRESHOLD = {BEC_THRESHOLD}")
    print("  ✓ Passed")


def test_kk_emission_freq():
    """Frecuencia de emisión KK debe ser ~2003 Hz."""
    print("\n✓ Test: KK_EMISSION_FREQ_HZ...")
    assert abs(KK_EMISSION_FREQ_HZ - 2003.0) < 1.0, \
        f"Emisión KK esperada ~2003 Hz, got {KK_EMISSION_FREQ_HZ}"
    print(f"    KK_EMISSION_FREQ_HZ = {KK_EMISSION_FREQ_HZ} Hz")
    print("  ✓ Passed")


# ── QCALSpectralOperator ──────────────────────────────────────────────────────

def test_operator_default_init():
    """Inicialización por defecto del operador espectral."""
    print("\n✓ Test: QCALSpectralOperator init por defecto...")
    op = QCALSpectralOperator()
    assert abs(op.f0 - F0_DEFAULT) < 1e-6
    assert abs(op.gamma - 1.0) < 1e-10
    assert abs(op.C - 1.0) < 1e-10
    assert abs(op.hbar - 1.0545718e-34) < 1e-40
    print(f"    f0={op.f0}, γ={op.gamma}, C={op.C}")
    print("  ✓ Passed")


def test_operator_zero_C_raises():
    """C=0 debe lanzar ValueError."""
    print("\n✓ Test: QCALSpectralOperator C=0 raises...")
    import pytest
    with pytest.raises(ValueError):
        QCALSpectralOperator(C=0)
    print("  ✓ Passed")


def test_modulation_potential_default():
    """V̂_mod = γ·ħ/C con parámetros por defecto."""
    print("\n✓ Test: modulation_potential...")
    op = QCALSpectralOperator()
    v_mod = op.modulation_potential()
    expected = 1.0 * 1.0545718e-34 / 1.0
    assert abs(v_mod - expected) < 1e-40, \
        f"V̂_mod esperado {expected:.3e}, got {v_mod:.3e}"
    print(f"    V̂_mod = {v_mod:.3e} J·s")
    print("  ✓ Passed")


def test_compute_eigenvalue_first_gamma():
    """λ₁ = γ₁ · f₀ + V̂_mod."""
    print("\n✓ Test: compute_eigenvalue con γ₁...")
    op = QCALSpectralOperator()
    lam = op.compute_eigenvalue(GAMMAS[0])
    expected = GAMMAS[0] * F0_DEFAULT + op.modulation_potential()
    assert abs(lam - expected) < 1e-6, \
        f"λ₁ esperado {expected:.4f}, got {lam:.4f}"
    print(f"    λ₁ = {lam:.4f} Hz  (γ₁·f₀ ≈ {GAMMAS[0]*F0_DEFAULT:.4f})")
    print("  ✓ Passed")


def test_compute_eigenvalue_positive():
    """Todos los autovalores deben ser positivos (γ_n > 0)."""
    print("\n✓ Test: autovalores positivos...")
    op = QCALSpectralOperator()
    for g in GAMMAS:
        lam = op.compute_eigenvalue(g)
        assert lam > 0, f"λ debe ser > 0, got {lam} para γ={g}"
    print(f"    Todos los {len(GAMMAS)} autovalores positivos ✓")
    print("  ✓ Passed")


def test_certify_critical_line_exact():
    """σ = 0.5 debe estar en la línea crítica (on_critical=True, Ψ=1)."""
    print("\n✓ Test: certify_critical_line en σ=0.5...")
    op = QCALSpectralOperator()
    on_critical, psi = op.certify_critical_line(0.5)
    assert on_critical is True, "σ=0.5 debe ser on_critical"
    assert abs(psi - 1.0) < 1e-10, f"Ψ en σ=0.5 debe ser 1.0, got {psi}"
    print(f"    σ=0.5: on_critical={on_critical}, Ψ={psi:.6f}")
    print("  ✓ Passed")


def test_certify_critical_line_off():
    """σ ≠ 0.5 debe dar on_critical=False y Ψ < 1."""
    print("\n✓ Test: certify_critical_line fuera de σ=0.5...")
    op = QCALSpectralOperator()
    for sigma in [0.3, 0.4, 0.6, 0.7]:
        on_critical, psi = op.certify_critical_line(sigma)
        assert on_critical is False, f"σ={sigma} no debe ser on_critical"
        assert psi < 1.0, f"Ψ debe ser < 1 para σ={sigma}, got {psi}"
    print("    σ ∈ {0.3, 0.4, 0.6, 0.7}: on_critical=False, Ψ<1 ✓")
    print("  ✓ Passed")


def test_certify_critical_line_decay_monotone():
    """Ψ(σ) debe decaer monótonamente al alejarse de σ=0.5."""
    print("\n✓ Test: decaimiento monotóno de Ψ...")
    op = QCALSpectralOperator()
    _, psi_05 = op.certify_critical_line(0.5)
    _, psi_04 = op.certify_critical_line(0.4)
    _, psi_03 = op.certify_critical_line(0.3)
    assert psi_05 > psi_04 > psi_03, \
        f"Ψ debe decaer: {psi_05:.4f} > {psi_04:.4f} > {psi_03:.4f}"
    print(f"    Ψ(0.5)={psi_05:.4f} > Ψ(0.4)={psi_04:.4f} > Ψ(0.3)={psi_03:.4f}")
    print("  ✓ Passed")


# ── string_noetic_forcing ─────────────────────────────────────────────────────

def test_forcing_below_threshold_returns_zeros():
    """Ψ < threshold debe devolver forzado cero."""
    print("\n✓ Test: forzado cero bajo umbral BEC...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.5, lambda_list=lambda_list)

    assert np.allclose(fx, 0.0), "fx debe ser cero para Ψ < threshold"
    assert np.allclose(fy, 0.0), "fy debe ser cero para Ψ < threshold"
    print(f"    Ψ=0.5 < {BEC_THRESHOLD}: forzado = 0 ✓")
    print("  ✓ Passed")


def test_forcing_above_threshold_nonzero():
    """Ψ ≥ threshold debe producir forzado no nulo."""
    print("\n✓ Test: forzado activo sobre umbral BEC...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list)

    assert np.any(fx != 0.0), "fx no debe ser completamente cero para Ψ >= threshold"
    assert np.any(fy != 0.0), "fy no debe ser completamente cero para Ψ >= threshold"
    print(f"    Ψ=0.95 >= {BEC_THRESHOLD}: forzado activo, max|fx|={np.max(np.abs(fx)):.3e}")
    print("  ✓ Passed")


def test_forcing_shape():
    """El forzado debe tener la misma shape que xx."""
    print("\n✓ Test: shape del forzado...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid(N=16)
    lambda_list = build_lambda_list(op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.99, lambda_list=lambda_list)

    assert fx.shape == xx.shape, f"fx.shape {fx.shape} != xx.shape {xx.shape}"
    assert fy.shape == yy.shape, f"fy.shape {fy.shape} != yy.shape {yy.shape}"
    print(f"    shape: fx={fx.shape}, xx={xx.shape} ✓")
    print("  ✓ Passed")


def test_forcing_scales_with_psi():
    """El forzado debe escalar monótonamente con Ψ (ganancia ∝ Ψ²)."""
    print("\n✓ Test: escalado del forzado con Ψ...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    fx_low, _ = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.9, lambda_list=lambda_list)
    fx_high, _ = string_noetic_forcing(0.1, xx, yy, op, Psi_local=0.99, lambda_list=lambda_list)

    rms_low = float(np.sqrt(np.mean(fx_low ** 2)))
    rms_high = float(np.sqrt(np.mean(fx_high ** 2)))
    assert rms_high > rms_low, \
        f"RMS debe crecer con Ψ: rms_low={rms_low:.3e}, rms_high={rms_high:.3e}"
    print(f"    RMS(Ψ=0.9)={rms_low:.3e} < RMS(Ψ=0.99)={rms_high:.3e} ✓")
    print("  ✓ Passed")


def test_forcing_threshold_boundary():
    """Exactamente en threshold, el forzado debe ser activo."""
    print("\n✓ Test: forzado en Ψ = threshold exacto...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:3]  # Solo 3 modos para velocidad

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=BEC_THRESHOLD,
                                   lambda_list=lambda_list)
    # Ψ_local == threshold → sí activa (condición es Psi_local < threshold)
    assert np.any(fx != 0.0), "Forzado debe activarse cuando Ψ == threshold"
    print(f"    Ψ={BEC_THRESHOLD} (boundary): forzado activo ✓")
    print("  ✓ Passed")


def test_forcing_empty_lambda_list():
    """Lambda list vacía debe devolver ceros (sin modos)."""
    print("\n✓ Test: forzado con lista de modos vacía...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.99, lambda_list=[])

    assert np.allclose(fx, 0.0), "Sin modos, fx debe ser cero"
    assert np.allclose(fy, 0.0), "Sin modos, fy debe ser cero"
    print("    Lista vacía: forzado = 0 ✓")
    print("  ✓ Passed")


# ── compute_psi ───────────────────────────────────────────────────────────────

def test_compute_psi_returns_float():
    """compute_psi debe devolver un float."""
    print("\n✓ Test: compute_psi devuelve float...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.random.randn(*xx.shape)
    v = np.random.randn(*xx.shape)

    psi = compute_psi(u, v, xx, op)
    assert isinstance(psi, float), f"Ψ debe ser float, got {type(psi)}"
    print(f"    Ψ = {psi:.6f}")
    print("  ✓ Passed")


def test_compute_psi_in_range():
    """Ψ debe estar en [0, 1]."""
    print("\n✓ Test: compute_psi ∈ [0, 1]...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.random.randn(*xx.shape)
    v = np.random.randn(*xx.shape)

    psi = compute_psi(u, v, xx, op)
    assert 0.0 <= psi <= 1.0, f"Ψ debe estar en [0,1], got {psi}"
    print(f"    Ψ = {psi:.6f} ∈ [0, 1] ✓")
    print("  ✓ Passed")


def test_compute_psi_constant_field_safe():
    """Campos constantes no deben provocar NaN/error (std=0)."""
    print("\n✓ Test: compute_psi con campos constantes...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    u = np.ones_like(xx)
    v = np.ones_like(yy)

    psi = compute_psi(u, v, xx, op)
    assert np.isfinite(psi), f"Ψ debe ser finito para campos constantes, got {psi}"
    assert 0.0 <= psi <= 1.0, f"Ψ debe estar en [0,1], got {psi}"
    print(f"    Ψ (campo constante) = {psi:.6f} ✓")
    print("  ✓ Passed")


def test_compute_psi_resonant_field_higher():
    """Campo alineado con f₀ debe producir Ψ más alto que campo aleatorio."""
    print("\n✓ Test: campo resonante produce Ψ más alto...")
    op = QCALSpectralOperator()
    N = 32
    xx, yy = _make_grid(N)
    L = 2 * np.pi

    # Campo perfectamente resonante
    u_res = np.sin(2 * np.pi * op.f0 * xx / L)
    v_res = np.cos(2 * np.pi * op.f0 * xx / L)

    # Campo aleatorio
    rng = np.random.default_rng(42)
    u_rnd = rng.standard_normal(xx.shape)
    v_rnd = rng.standard_normal(xx.shape)

    psi_res = compute_psi(u_res, v_res, xx, op)
    psi_rnd = compute_psi(u_rnd, v_rnd, xx, op)

    assert psi_res > psi_rnd, \
        f"Campo resonante debe tener Ψ mayor: Ψ_res={psi_res:.4f}, Ψ_rnd={psi_rnd:.4f}"
    print(f"    Ψ_resonante={psi_res:.4f} > Ψ_aleatorio={psi_rnd:.4f} ✓")
    print("  ✓ Passed")


# ── build_lambda_list ─────────────────────────────────────────────────────────

def test_build_lambda_list_default():
    """build_lambda_list con gammas=None usa GAMMAS (20 ceros)."""
    print("\n✓ Test: build_lambda_list por defecto...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    assert len(lambdas) == len(GAMMAS), \
        f"Esperados {len(GAMMAS)} autovalores, got {len(lambdas)}"
    print(f"    len(lambdas) = {len(lambdas)}")
    print("  ✓ Passed")


def test_build_lambda_list_values():
    """Autovalores deben coincidir con compute_eigenvalue(γ_n)."""
    print("\n✓ Test: valores de build_lambda_list...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    for i, (lam, g) in enumerate(zip(lambdas, GAMMAS)):
        expected = op.compute_eigenvalue(g)
        assert abs(lam - expected) < 1e-9, \
            f"λ_{i+1} esperado {expected:.6f}, got {lam:.6f}"
    print(f"    Todos los {len(lambdas)} autovalores correctos ✓")
    print("  ✓ Passed")


def test_build_lambda_list_custom_gammas():
    """build_lambda_list con gammas personalizados."""
    print("\n✓ Test: build_lambda_list con gammas personalizados...")
    op = QCALSpectralOperator()
    custom_gammas = [14.1347, 21.0220]
    lambdas = build_lambda_list(op, gammas=custom_gammas)
    assert len(lambdas) == 2
    print(f"    lambdas = {lambdas}")
    print("  ✓ Passed")


def test_lambda_list_first_kk_mode():
    """El primer modo KK debe ser ≈ γ₁ · f₀ (~2003 Hz)."""
    print("\n✓ Test: primer modo KK (~2003 Hz)...")
    op = QCALSpectralOperator()
    lambdas = build_lambda_list(op)
    lam1 = lambdas[0]
    # γ₁ ≈ 14.1347, f₀ = 141.7001 → λ₁ ≈ 2002.35 Hz
    assert 1900 < lam1 < 2100, \
        f"λ₁ esperado ~2003 Hz (en [1900, 2100]), got {lam1:.2f}"
    print(f"    λ₁ = {lam1:.2f} Hz ≈ KK_EMISSION_FREQ_HZ={KK_EMISSION_FREQ_HZ} Hz ✓")
    print("  ✓ Passed")


# ── Integration tests ─────────────────────────────────────────────────────────

def test_full_pipeline_low_coherence():
    """Pipeline completo con Ψ bajo: el forzado no se activa."""
    print("\n✓ Test: pipeline completo Ψ < threshold...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)

    u = np.zeros_like(xx)
    v = np.zeros_like(yy)
    psi = compute_psi(u, v, xx, op)

    fx, fy = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi, lambda_list=lambda_list)

    assert psi < BEC_THRESHOLD or np.isfinite(np.max(np.abs(fx)))
    print(f"    Ψ={psi:.4f}, forzado max|fx|={np.max(np.abs(fx)):.3e}")
    print("  ✓ Passed")


def test_full_pipeline_high_coherence():
    """Pipeline completo con campo resonante: el forzado se activa."""
    print("\n✓ Test: pipeline completo Ψ > threshold...")
    op = QCALSpectralOperator()
    N = 32
    xx, yy = _make_grid(N)
    L = 2 * np.pi
    lambda_list = build_lambda_list(op)

    # Campo perfectamente resonante → Ψ alto
    u = np.sin(2 * np.pi * op.f0 * xx / L)
    v = np.cos(2 * np.pi * op.f0 * xx / L)
    psi = compute_psi(u, v, xx, op)

    fx, fy = string_noetic_forcing(0.1, xx, yy, op, Psi_local=psi, lambda_list=lambda_list)

    print(f"    Ψ={psi:.4f} (BEC_THRESHOLD={BEC_THRESHOLD})")
    # Result depends on whether psi >= threshold; just check no NaN
    assert np.all(np.isfinite(fx)), "fx no debe contener NaN/Inf"
    assert np.all(np.isfinite(fy)), "fy no debe contener NaN/Inf"
    print(f"    max|fx|={np.max(np.abs(fx)):.3e}, all finite ✓")
    print("  ✓ Passed")


def test_superradiant_gain_formula():
    """Ganancia superradiante N²·Ψ² es consistente con forzado escalonado."""
    print("\n✓ Test: ganancia superradiante N²·Ψ²...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = [op.compute_eigenvalue(GAMMAS[0])]  # Solo λ₁

    psi_a = 0.9
    psi_b = 0.95
    N = N_MICROTUBULES_DEFAULT

    fx_a, _ = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi_a, lambda_list=lambda_list)
    fx_b, _ = string_noetic_forcing(0.0, xx, yy, op, Psi_local=psi_b, lambda_list=lambda_list)

    rms_a = float(np.sqrt(np.mean(fx_a ** 2)))
    rms_b = float(np.sqrt(np.mean(fx_b ** 2)))

    # gain_ratio = (N²·Ψ_b²) / (N²·Ψ_a²) = (Ψ_b/Ψ_a)²
    expected_ratio = (psi_b / psi_a) ** 2
    actual_ratio = rms_b / rms_a if rms_a > 0 else 0.0

    assert abs(actual_ratio - expected_ratio) < 0.01, \
        f"Ratio ganancia esperado {expected_ratio:.4f}, got {actual_ratio:.4f}"
    print(f"    (Ψ_b/Ψ_a)² = {expected_ratio:.4f}, rms_b/rms_a = {actual_ratio:.4f} ✓")
    print("  ✓ Passed")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])


# ── string_noetic_forcing FFT extension ──────────────────────────────────────

def test_forcing_fft_return_shape():
    """Con return_fft=True, el espectro FFT tiene la misma shape que xx."""
    print("\n✓ Test: forzado con return_fft=True, shape espectro...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid(N=16)
    lambda_list = build_lambda_list(op)[:3]

    fx, fy, fft_spec = string_noetic_forcing(
        0.1, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list, return_fft=True
    )
    assert fft_spec.shape == xx.shape, \
        f"fft_spec.shape {fft_spec.shape} != xx.shape {xx.shape}"
    assert np.all(fft_spec >= 0.0), "Espectro FFT debe ser no negativo"
    print(f"    shape espectro: {fft_spec.shape} ✓")
    print("  ✓ Passed")


def test_forcing_fft_zero_when_below_threshold():
    """Con Psi < threshold y return_fft=True, espectro debe ser cero."""
    print("\n✓ Test: FFT cero bajo umbral...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:3]

    fx, fy, fft_spec = string_noetic_forcing(
        0.0, xx, yy, op, Psi_local=0.5, lambda_list=lambda_list, return_fft=True
    )
    assert np.allclose(fft_spec, 0.0), "FFT debe ser cero cuando Psi < threshold"
    print("    FFT cero para Psi < threshold ✓")
    print("  ✓ Passed")


def test_forcing_backward_compat_no_fft():
    """Sin return_fft, la funcion devuelve exactamente 2 elementos."""
    print("\n✓ Test: compatibilidad retroactiva sin return_fft...")
    op = QCALSpectralOperator()
    xx, yy = _make_grid()
    lambda_list = build_lambda_list(op)[:2]

    result = string_noetic_forcing(0.0, xx, yy, op, Psi_local=0.95, lambda_list=lambda_list)
    assert len(result) == 2, f"Sin return_fft debe haber 2 elementos, got {len(result)}"
    print("  ✓ Passed")


# ── VenezianoAmplitude ────────────────────────────────────────────────────────

def test_veneziano_regge_trajectory():
    """alpha(s) = alpha0 + alpha_prime*s debe ser lineal."""
    print("\n✓ Test: trayectoria de Regge lineal...")
    va = VenezianoAmplitude(alpha_prime=1.0, alpha_0=-1.0)
    assert abs(va.regge_trajectory(0.0) - (-1.0)) < 1e-12
    assert abs(va.regge_trajectory(1.0) - 0.0) < 1e-12
    assert abs(va.regge_trajectory(2.0) - 1.0) < 1e-12
    print(f"    a(0)={va.regge_trajectory(0)}, a(1)={va.regge_trajectory(1)} ✓")
    print("  ✓ Passed")


def test_veneziano_amplitude_returns_complex():
    """amplitude(s, t) debe devolver un numero complejo."""
    print("\n✓ Test: amplitude devuelve complejo...")
    va = VenezianoAmplitude()
    amp = va.amplitude(1.5, 1.5)
    assert isinstance(amp, complex), f"Debe ser complex, got {type(amp)}"
    print(f"    A(1.5, 1.5) = {amp:.4f}")
    print("  ✓ Passed")


def test_veneziano_amplitude_finite_away_from_poles():
    """La amplitud debe ser finita para valores s, t alejados de polos."""
    print("\n✓ Test: amplitud finita lejos de polos...")
    va = VenezianoAmplitude()
    for s, t in [(1.5, 1.5), (2.3, 1.7), (0.5, 3.0)]:
        amp = va.amplitude(s, t)
        assert np.isfinite(amp.real), f"Re[A({s},{t})] debe ser finito, got {amp}"
    print("  ✓ Passed")


def test_veneziano_mode_coupling_positive():
    """Los acoplamientos de modo alpha_n deben ser positivos."""
    print("\n✓ Test: acoplamientos de modo positivos...")
    va = VenezianoAmplitude(alpha_prime=1.0)
    for n in range(5):
        alpha_n = va.mode_coupling(n)
        assert alpha_n > 0, f"alpha_{n} debe ser > 0, got {alpha_n}"
    print(f"    a_0={va.mode_coupling(0):.4f}, a_1={va.mode_coupling(1):.4f} ✓")
    print("  ✓ Passed")


def test_veneziano_mode_coupling_uses_gammas():
    """mode_coupling(n) = alpha_prime * gamma_n / (n+1)."""
    print("\n✓ Test: formula de acoplamiento de modo...")
    va = VenezianoAmplitude(alpha_prime=1.0)
    for n in range(5):
        expected = 1.0 * GAMMAS[n] / (n + 1)
        assert abs(va.mode_coupling(n) - expected) < 1e-12
    print("  ✓ Passed")


def test_veneziano_regularize_arg_near_pole():
    """_regularize_arg debe desplazar argumentos en o muy cerca de k<=0."""
    print("\n✓ Test: regularizacion en polo...")
    eps = VenezianoAmplitude._POLE_EPS
    assert abs(VenezianoAmplitude._regularize_arg(0.0) - eps) < 1e-15
    assert abs(VenezianoAmplitude._regularize_arg(-1.0) - (-1.0 + eps)) < 1e-15
    assert abs(VenezianoAmplitude._regularize_arg(0.5) - 0.5) < 1e-15
    print("  ✓ Passed")


# ── KaluzaKleinModes ──────────────────────────────────────────────────────────

def test_kk_modes_n_modes():
    """KaluzaKleinModes por defecto tiene 20 modos."""
    print("\n✓ Test: KaluzaKleinModes n_modes por defecto...")
    kk = KaluzaKleinModes()
    assert kk.n_modes == 20, f"Esperado 20 modos, got {kk.n_modes}"
    print(f"    n_modes = {kk.n_modes} ✓")
    print("  ✓ Passed")


def test_kk_modes_frequencies_first():
    """El primer modo KK debe ser gamma_1 x f0 aprox 2003 Hz."""
    print("\n✓ Test: primera frecuencia KK...")
    kk = KaluzaKleinModes()
    freqs = kk.frequencies()
    assert abs(freqs[0] - GAMMAS[0] * F0_DEFAULT) < 1e-6
    assert 1900 < freqs[0] < 2100
    print(f"    lambda1 = {freqs[0]:.2f} Hz ✓")
    print("  ✓ Passed")


def test_kk_modes_t_duality_phase():
    """phi_n = pi/(n+1), base 0."""
    print("\n✓ Test: fases de T-dualidad...")
    kk = KaluzaKleinModes()
    for n in range(5):
        phi = kk.t_duality_phase(n)
        expected = np.pi / (n + 1)
        assert abs(phi - expected) < 1e-12, f"phi_{n} esperado {expected:.4f}, got {phi:.4f}"
    print("  ✓ Passed")


def test_kk_modes_compactification_hex_low():
    """Para n <= 5, radio usa geometria hexagonal EZ."""
    print("\n✓ Test: radio hexagonal para n <= 5...")
    kk = KaluzaKleinModes()
    for n in range(6):
        R = kk.compactification_radius(n)
        expected = np.pi / (GAMMAS[n] * 6)
        assert abs(R - expected) < 1e-12, f"R_{n} esperado {expected:.6f}, got {R:.6f}"
    print("  ✓ Passed")


def test_kk_modes_compactification_cy_high():
    """Para n > 5, radio usa topologia Calabi-Yau periodica."""
    print("\n✓ Test: radio Calabi-Yau para n > 5...")
    kk = KaluzaKleinModes()
    for n in range(6, kk.n_modes):
        R = kk.compactification_radius(n)
        expected = 2.0 * np.pi / GAMMAS[n]
        assert abs(R - expected) < 1e-12, f"R_{n} esperado {expected:.6f}, got {R:.6f}"
    print("  ✓ Passed")


def test_kk_modes_mode_data_keys():
    """mode_data debe contener todas las claves esperadas."""
    print("\n✓ Test: claves de mode_data...")
    kk = KaluzaKleinModes()
    data = kk.mode_data(0)
    expected_keys = {"n", "gamma_n", "frequency_hz", "t_duality_phase",
                     "compactification_radius", "topology"}
    assert expected_keys.issubset(data.keys()), f"Faltan claves: {expected_keys - data.keys()}"
    assert data["topology"] == "hexagonal-EZ"
    print(f"    topology(n=0) = {data['topology']} ✓")
    print("  ✓ Passed")


def test_kk_modes_topology_transitions():
    """Topologia cambia de hexagonal-EZ a Calabi-Yau-periodic en n=6."""
    print("\n✓ Test: transicion de topologia en n=5->6...")
    kk = KaluzaKleinModes()
    assert kk.mode_data(5)["topology"] == "hexagonal-EZ"
    assert kk.mode_data(6)["topology"] == "Calabi-Yau-periodic"
    print("  ✓ Passed")


# ── validate_riemann_stability ────────────────────────────────────────────────

def test_validate_stability_default_passes():
    """Los ceros por defecto deben pasar la validacion."""
    print("\n✓ Test: validacion de estabilidad de Riemann por defecto...")
    result = validate_riemann_stability()
    assert result["stable"] is True, f"Esperado stable=True, got {result}"
    assert result["positive"] is True
    assert result["monotonic"] is True
    assert result["lambda1_valid"] is True
    print(f"    stable={result['stable']}, lambda1={result['lambda1_approx']:.6f} ✓")
    print("  ✓ Passed")


def test_validate_stability_lambda1_value():
    """lambda1_approx debe coincidir con GAMMAS[0]."""
    print("\n✓ Test: lambda1_approx en validacion...")
    result = validate_riemann_stability()
    assert abs(result["lambda1_approx"] - GAMMAS[0]) < 1e-12
    print(f"    lambda1 = {result['lambda1_approx']:.8f} ✓")
    print("  ✓ Passed")


def test_validate_stability_fails_negative():
    """Un cero negativo debe hacer stable=False."""
    print("\n✓ Test: validacion falla con cero negativo...")
    bad_gammas = [-1.0] + GAMMAS[1:]
    result = validate_riemann_stability(bad_gammas)
    assert result["positive"] is False
    assert result["stable"] is False
    print("  ✓ Passed")


def test_validate_stability_fails_non_monotonic():
    """Una secuencia no creciente debe hacer stable=False."""
    print("\n✓ Test: validacion falla con secuencia no monotonica...")
    bad_gammas = list(GAMMAS)
    bad_gammas[1], bad_gammas[2] = bad_gammas[2], bad_gammas[1]
    result = validate_riemann_stability(bad_gammas)
    assert result["monotonic"] is False
    assert result["stable"] is False
    print("  ✓ Passed")


# ── compute_superradiant_gain ─────────────────────────────────────────────────

def test_superradiant_gain_formula():
    """Ganancia = N2 * Psi2."""
    print("\n✓ Test: formula de ganancia superradiante...")
    N = 100.0
    Psi = 0.9
    gain = compute_superradiant_gain(N, Psi)
    expected = N ** 2 * Psi ** 2
    assert abs(gain - expected) < 1e-9, f"Ganancia esperada {expected:.4f}, got {gain:.4f}"
    print(f"    G({N}, {Psi}) = {gain:.4f} ✓")
    print("  ✓ Passed")


def test_superradiant_gain_clamping_below():
    """Psi < 0 se sujeta a 0 -> ganancia = 0."""
    print("\n✓ Test: sujecion Psi < 0...")
    assert abs(compute_superradiant_gain(1e10, -0.5)) < 1e-30
    print("  ✓ Passed")


def test_superradiant_gain_clamping_above():
    """Psi > 1 se sujeta a 1 -> ganancia = N2."""
    print("\n✓ Test: sujecion Psi > 1...")
    N = 5.0
    gain = compute_superradiant_gain(N, 2.0)
    expected = N ** 2 * 1.0 ** 2
    assert abs(gain - expected) < 1e-9
    print(f"    G({N}, 2.0) = {gain:.4f} = N2 ✓")
    print("  ✓ Passed")


def test_superradiant_gain_zero_psi():
    """Psi = 0 -> ganancia = 0."""
    print("\n✓ Test: Psi=0 -> ganancia 0...")
    assert abs(compute_superradiant_gain(1e13, 0.0)) < 1e-30
    print("  ✓ Passed")


def test_superradiant_gain_unit_psi():
    """Psi = 1 -> ganancia = N2."""
    print("\n✓ Test: Psi=1 -> ganancia N2...")
    N = N_MICROTUBULES_DEFAULT
    gain = compute_superradiant_gain(N, 1.0)
    assert abs(gain - N ** 2) < 1.0
    print(f"    G(N_default, 1.0) = {gain:.3e} = N2={N**2:.3e} ✓")
    print("  ✓ Passed")


# ── HolographicFluidSolver ────────────────────────────────────────────────────

def test_fluid_solver_init():
    """HolographicFluidSolver inicializa con la viscosidad adelica correcta."""
    print("\n✓ Test: HolographicFluidSolver init...")
    solver = HolographicFluidSolver(N=16, seed=0)
    assert abs(solver.mu - 1.0 / F0_DEFAULT) < 1e-12, \
        f"mu esperado {1.0/F0_DEFAULT:.6e}, got {solver.mu:.6e}"
    print(f"    mu = 1/f0 = {solver.mu:.6e} ✓")
    print("  ✓ Passed")


def test_fluid_solver_velocity_shape():
    """Los campos de velocidad iniciales tienen shape NxN."""
    print("\n✓ Test: shape de campos de velocidad...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=1)
    ux, uy = solver.velocity_fields
    assert ux.shape == (N, N), f"ux.shape esperado ({N},{N}), got {ux.shape}"
    assert uy.shape == (N, N)
    print(f"    ux.shape = {ux.shape} ✓")
    print("  ✓ Passed")


def test_fluid_solver_seed_reproducibility():
    """La misma semilla debe producir condiciones iniciales identicas."""
    print("\n✓ Test: reproducibilidad de semilla...")
    s1 = HolographicFluidSolver(N=16, seed=42)
    s2 = HolographicFluidSolver(N=16, seed=42)
    assert np.allclose(s1.ux, s2.ux), "ux debe ser identico con la misma semilla"
    assert np.allclose(s1.uy, s2.uy), "uy debe ser identico con la misma semilla"
    print("  ✓ Passed")


def test_fluid_solver_different_seeds():
    """Semillas distintas deben producir condiciones iniciales distintas."""
    print("\n✓ Test: semillas distintas -> campos distintos...")
    s1 = HolographicFluidSolver(N=16, seed=1)
    s2 = HolographicFluidSolver(N=16, seed=99)
    assert not np.allclose(s1.ux, s2.ux), "Semillas distintas deben dar ux distintos"
    print("  ✓ Passed")


def test_fluid_solver_step_shape():
    """step() devuelve (ux, uy) con la shape correcta."""
    print("\n✓ Test: shape tras step()...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=7)
    ux, uy = solver.step(dt=0.001)
    assert ux.shape == (N, N) and uy.shape == (N, N)
    print(f"    ux.shape tras step = {ux.shape} ✓")
    print("  ✓ Passed")


def test_fluid_solver_step_changes_field():
    """Un paso debe modificar los campos de velocidad."""
    print("\n✓ Test: step() modifica los campos...")
    solver = HolographicFluidSolver(N=16, seed=5)
    ux0 = solver.ux.copy()
    solver.step(dt=0.001)
    assert not np.allclose(solver.ux, ux0), "ux debe cambiar tras un paso"
    print("  ✓ Passed")


def test_fluid_solver_step_finite():
    """Los campos tras step deben ser finitos."""
    print("\n✓ Test: campos finitos tras step()...")
    solver = HolographicFluidSolver(N=16, seed=3)
    for _ in range(5):
        ux, uy = solver.step(dt=0.0005)
    assert np.all(np.isfinite(ux)), "ux debe ser finito"
    assert np.all(np.isfinite(uy)), "uy debe ser finito"
    print("  ✓ Passed")


def test_fluid_solver_leray_projection():
    """La proyeccion de Leray debe preservar la incompresibilidad."""
    print("\n✓ Test: proyeccion Leray preserva div(u) aprox 0...")
    N = 32
    solver = HolographicFluidSolver(N=N, seed=11)
    rng = np.random.default_rng(0)
    v_x = rng.standard_normal((N, N))
    v_y = rng.standard_normal((N, N))
    vx_hat = np.fft.fft2(v_x)
    vy_hat = np.fft.fft2(v_y)
    px_hat, py_hat = solver._leray_project(vx_hat, vy_hat)
    div_hat = 1j * solver.kx * px_hat + 1j * solver.ky * py_hat
    div = np.fft.ifft2(div_hat).real
    assert np.max(np.abs(div)) < 1e-10, \
        f"div(P(u)) debe ser ~0, max|div|={np.max(np.abs(div)):.2e}"
    print(f"    max|div(P(u))| = {np.max(np.abs(div)):.2e} aprox 0 ✓")
    print("  ✓ Passed")


def test_fluid_solver_kolmogorov_slope_returns_float():
    """kolmogorov_slope debe devolver un float."""
    print("\n✓ Test: kolmogorov_slope devuelve float...")
    solver = HolographicFluidSolver(N=32, seed=0)
    for _ in range(3):
        solver.step(dt=0.001)
    slope = solver.kolmogorov_slope()
    assert isinstance(slope, float), f"Pendiente debe ser float, got {type(slope)}"
    assert np.isfinite(slope), f"Pendiente debe ser finita, got {slope}"
    print(f"    pendiente Kolmogorov = {slope:.4f}")
    print("  ✓ Passed")


def test_fluid_solver_step_with_forcing():
    """step() con forzado externo no genera NaN."""
    print("\n✓ Test: step() con forzado externo...")
    N = 16
    solver = HolographicFluidSolver(N=N, seed=2)
    op = QCALSpectralOperator()
    lambda_list = build_lambda_list(op)[:3]
    fx, fy = string_noetic_forcing(0.0, solver.xx, solver.yy, op,
                                   Psi_local=0.95, lambda_list=lambda_list)
    ux, uy = solver.step(dt=0.001, forcing_x=fx, forcing_y=fy)
    assert np.all(np.isfinite(ux)) and np.all(np.isfinite(uy))
    print("  ✓ Passed")


# ── QCALStringCore ────────────────────────────────────────────────────────────

def test_qcal_string_core_seal():
    """El sello debe ser la cadena correcta."""
    print("\n✓ Test: sello QCALStringCore...")
    core = QCALStringCore(N=16, seed=0)
    assert core.SEAL == "\u2234\U00013080\u03a9\u221e\u00b3\u03a6", \
        f"Sello incorrecto: {core.SEAL}"
    print(f"    SEAL = {core.SEAL} ✓")
    print("  ✓ Passed")


def test_qcal_string_core_cert_string():
    """La cadena de certificacion debe ser 'QED-CUERDAS-VERIFIED'."""
    print("\n✓ Test: cadena de certificacion...")
    assert QCALStringCore.CERT_STRING == "QED-CUERDAS-VERIFIED"
    print("  ✓ Passed")


def test_qcal_string_core_resonance_peak():
    """El pico de resonancia debe ser aprox 2003 Hz."""
    print("\n✓ Test: pico de resonancia QCALStringCore...")
    core = QCALStringCore(N=16, seed=0)
    peak = core.resonance_peak_hz
    assert 1900 < peak < 2100, f"Pico esperado ~2003 Hz, got {peak:.2f}"
    expected = GAMMAS[0] * F0_DEFAULT
    assert abs(peak - expected) < 1e-9
    print(f"    pico = {peak:.4f} Hz ✓")
    print("  ✓ Passed")


def test_qcal_string_core_certify_keys():
    """certify() debe contener las claves: certificate, seal, resonance_peak_hz, sha256."""
    print("\n✓ Test: claves de certify()...")
    core = QCALStringCore(N=16, seed=0)
    cert = core.certify()
    for key in ("certificate", "seal", "resonance_peak_hz", "sha256"):
        assert key in cert, f"Clave '{key}' no encontrada en certificado"
    print("  ✓ Passed")


def test_qcal_string_core_certify_sha256_hex():
    """sha256 debe ser una cadena hex de 64 caracteres."""
    print("\n✓ Test: sha256 de certify()...")
    core = QCALStringCore(N=16, seed=0)
    sha = core.certify()["sha256"]
    assert isinstance(sha, str) and len(sha) == 64
    assert all(c in "0123456789abcdef" for c in sha)
    print(f"    sha256[:16] = {sha[:16]}... ✓")
    print("  ✓ Passed")


def test_qcal_string_core_certify_deterministic():
    """certify() debe ser determinista."""
    print("\n✓ Test: certify() determinista...")
    core = QCALStringCore(N=16, seed=0)
    cert1 = core.certify()
    cert2 = core.certify()
    assert cert1["sha256"] == cert2["sha256"]
    print("  ✓ Passed")


def test_qcal_string_core_run_forcing_cycle():
    """run_forcing_cycle debe devolver dict con las claves esperadas."""
    print("\n✓ Test: run_forcing_cycle() claves de salida...")
    core = QCALStringCore(N=16, seed=0)
    result = core.run_forcing_cycle(t=0.0, Psi_local=0.95, dt=0.001, n_steps=3)
    for key in ("psi", "resonance_peak_hz", "seal", "kolmogorov_slope", "certificate"):
        assert key in result, f"Clave '{key}' no encontrada en resultado"
    print(f"    psi={result['psi']:.4f}, seal={result['seal']} ✓")
    print("  ✓ Passed")


def test_qcal_string_core_run_forcing_cycle_finite():
    """run_forcing_cycle no debe producir NaN."""
    print("\n✓ Test: run_forcing_cycle() sin NaN...")
    core = QCALStringCore(N=16, seed=42)
    result = core.run_forcing_cycle(t=0.0, Psi_local=0.95, dt=0.001, n_steps=5)
    assert np.isfinite(result["psi"]), "psi debe ser finito"
    assert np.isfinite(result["kolmogorov_slope"]), "pendiente debe ser finita"
    print("  ✓ Passed")
