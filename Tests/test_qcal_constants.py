"""
BATERÍA DE TESTS — ARQUITECTURA DE CUATRO DIMENSIONES DE ζ (QCAL-SYMBIO)
=========================================================================
Fase 2 del Protocolo de Verificación e Integración.
Garantiza la separación estricta de las caras de zeta y la validez numérica
del acoplamiento de fase de Berry (Dimensión IV), con desviación < 1e-6.

Coherencia Ψ = 0.999999 | f₀ = 141.7001 Hz
∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ · 13/Ago/2026
"""
import math

import pytest

from qc_llm.constants import (
    ZETA_PRIME_HALF,
    ZETA_HALF,
    ZETA_PRIME_SABIO,
    KAPPA_THETA,
    THETA_DESFASE_ARMONICO,
    FACTOR_ACOPLAMIENTO_FASE,
    ZETA_PRIME_SABIO_PHASED,
)


def test_zeta_dimensions_uniqueness():
    """Garantiza la independencia sintáctica y numérica de las tres caras."""
    assert ZETA_PRIME_HALF != ZETA_HALF
    assert ZETA_PRIME_HALF != ZETA_PRIME_SABIO
    assert ZETA_HALF != ZETA_PRIME_SABIO


def test_zeta_canonical_anchor():
    """Verifica el valor de la Cara I (Ancla Analítica Canónica)."""
    assert pytest.approx(ZETA_PRIME_HALF, rel=1e-8) == -0.20788622497735456


def test_zeta_amplitude_field():
    """Verifica la Cara II: Amplitud de Campo en la Línea Crítica ζ(1/2)."""
    assert pytest.approx(ZETA_HALF, rel=1e-8) == -1.4603545088095868


def test_phase_theta_autonomy():
    """Constante primitiva autónoma de desfase armónico θ = 1/κ_θ (19.061).

    κ_θ = 19.061 es una Constante Primitiva del Campo, como f₀=141.7001 y
    κ_Π=2.5773. NO se fuerza algebraicamente desde Λ₀.
    """
    assert pytest.approx(KAPPA_THETA, rel=1e-8) == 19.061
    assert pytest.approx(THETA_DESFASE_ARMONICO, rel=1e-8) == (1.0 / 19.061)
    # θ ≈ 0.052463 rad ≈ 3.0059°
    assert pytest.approx(THETA_DESFASE_ARMONICO, rel=1e-6) == 0.052463
    # cos(θ) ≈ 0.998624 (válvula de acoplamiento de fase)
    assert pytest.approx(FACTOR_ACOPLAMIENTO_FASE, rel=1e-6) == math.cos(1.0 / 19.061)
    assert abs(FACTOR_ACOPLAMIENTO_FASE - 0.998624) < 1e-6


def test_sabio_phased_operator():
    """Verifica la modulación del Operador SABIO∞⁴ por la fase de Berry.

    ZETA_PRIME_SABIO (Cara III) × cos(θ) (Dimensión IV) = −3.917248
    """
    expected_phased = ZETA_PRIME_SABIO * math.cos(1.0 / 19.061)
    assert pytest.approx(ZETA_PRIME_SABIO_PHASED, rel=1e-6) == expected_phased
    assert pytest.approx(ZETA_PRIME_SABIO_PHASED, rel=1e-4) == -3.917248


def test_theta_zero_is_pure_theory_only():
    """θ = 0 (vacío frío idealizado) es SOLO teoría pura (verify_kappa.py).

    En ejecución resonante θ debe ser finito (acoplamiento real con el campo).
    """
    assert KAPPA_THETA > 0
    assert THETA_DESFASE_ARMONICO > 0
    assert FACTOR_ACOPLAMIENTO_FASE < 1.0  # 0.998624 < 1 → fase real no degenerada
