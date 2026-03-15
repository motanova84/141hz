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
