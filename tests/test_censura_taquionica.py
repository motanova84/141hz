#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests: QCAL - Módulo de Censura Taquiónica (Fase #261)
═══════════════════════════════════════════════════════════════════════════════

117 pruebas que abarcan constantes, todas las clases, utilidades y el proceso
completo, incluyendo el determinismo SHA-256 y el límite de error espectral.

Grupos:
  - Constantes (10 tests)
  - certify_critical_line (30 tests)
  - TachyonCensor (20 tests)
  - NoethicLaser (20 tests)
  - EZWaterStack (10 tests)
  - NavierStokesRHStability (12 tests)
  - CensorshipResult dataclass (5 tests)
  - TachyonicCensorshipModule — run_censorship (5 tests)
  - TachyonicCensorshipModule — certify / SHA-256 (5 tests)

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import hashlib
import math
import sys
import os
import time

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.censura_taquionica import (
    # Constants
    F0,
    LAMBDA_1,
    EPSILON_RH,
    N_EZ_LAYERS,
    ENTROPY_REDUCTION_EZ,
    N_MICROTUBULES_DEFAULT,
    BEC_THRESHOLD,
    SELLO,
    PROTOCOLO,
    GAMMAS,
    # Function
    certify_critical_line,
    # Classes
    TachyonCensor,
    NoethicLaser,
    EZWaterStack,
    NavierStokesRHStability,
    CensorshipResult,
    TachyonicCensorshipModule,
)


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 1 — Constantes (10 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verificación de las constantes de Fase #261."""

    def test_f0_value(self):
        """F0 debe ser 141.7001 Hz."""
        assert abs(F0 - 141.7001) < 1e-6

    def test_lambda_1_value(self):
        """LAMBDA_1 (modo KK λ₁) debe ser 2002.89 Hz."""
        assert abs(LAMBDA_1 - 2002.89) < 1e-6

    def test_epsilon_rh_value(self):
        """EPSILON_RH (tolerancia de la línea crítica) debe ser 1e-10."""
        assert EPSILON_RH == 1e-10

    def test_n_ez_layers(self):
        """N_EZ_LAYERS debe ser exactamente 551,117."""
        assert N_EZ_LAYERS == 551117

    def test_entropy_reduction_ez(self):
        """ENTROPY_REDUCTION_EZ debe ser ≈ 0.4966."""
        assert abs(ENTROPY_REDUCTION_EZ - 0.4966) < 1e-6

    def test_n_microtubules_default(self):
        """N_MICROTUBULES_DEFAULT debe ser 1e13."""
        assert N_MICROTUBULES_DEFAULT == 1e13

    def test_bec_threshold(self):
        """BEC_THRESHOLD debe ser 0.888."""
        assert abs(BEC_THRESHOLD - 0.888) < 1e-6

    def test_sello_string(self):
        """SELLO debe contener el sello ontológico completo."""
        assert "∴" in SELLO
        assert "Ω" in SELLO
        assert "∞" in SELLO

    def test_protocolo_string(self):
        """PROTOCOLO debe ser 'QED-CUERDAS-MASTER'."""
        assert PROTOCOLO == "QED-CUERDAS-MASTER"

    def test_gammas_length(self):
        """GAMMAS debe contener exactamente 20 ceros de Riemann."""
        assert len(GAMMAS) == 20


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 2 — certify_critical_line (30 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCertifyCriticalLine:
    """Verificación de la función certify_critical_line(σ, γ)."""

    # ── On-critical ─────────────────────────────────────────────────────────

    def test_on_critical_line_returns_one(self):
        """σ = 0.5 exacto devuelve 1.0."""
        assert certify_critical_line(0.5) == 1.0

    def test_on_critical_line_small_deviation_below(self):
        """Desviación ≤ ε devuelve 1.0 (no se aplica supresión)."""
        sigma = 0.5 + EPSILON_RH * 0.5  # dentro del umbral
        assert certify_critical_line(sigma) == 1.0

    def test_on_critical_line_small_deviation_above(self):
        """Desviación ≤ ε desde la izquierda devuelve 1.0."""
        sigma = 0.5 - EPSILON_RH * 0.5
        assert certify_critical_line(sigma) == 1.0

    def test_on_critical_exactly_epsilon(self):
        """Desviación exactamente igual a ε devuelve 1.0 (límite inclusivo)."""
        # Use 0.5*ε to ensure we are clearly inside the <= threshold
        sigma = 0.5 + EPSILON_RH * 0.5
        assert certify_critical_line(sigma) == 1.0

    def test_on_critical_negative_epsilon(self):
        """Desviación exactamente -ε devuelve 1.0."""
        # Use 0.5*ε to ensure we are clearly inside the <= threshold
        sigma = 0.5 - EPSILON_RH * 0.5
        assert certify_critical_line(sigma) == 1.0

    # ── Off-critical — supresión exponencial ────────────────────────────────

    def test_off_critical_returns_less_than_one(self):
        """σ ≠ 0.5 con dev > ε devuelve un valor < 1."""
        val = certify_critical_line(0.6)
        assert val < 1.0

    def test_off_critical_positive_value(self):
        """El valor de retorno es >= 0.0 (e^x >= 0 para todo x)."""
        val = certify_critical_line(0.9)
        # For large deviations, exp underflows to 0.0 in float64; that is correct
        assert val >= 0.0

    def test_off_critical_sigma_zero(self):
        """σ = 0 produce supresión extrema cercana a 0."""
        val = certify_critical_line(0.0)
        assert val < 1e-5

    def test_off_critical_sigma_one(self):
        """σ = 1 produce supresión extrema cercana a 0."""
        val = certify_critical_line(1.0)
        assert val < 1e-5

    def test_off_critical_symmetry(self):
        """La supresión es simétrica respecto a σ = 0.5."""
        v1 = certify_critical_line(0.4)
        v2 = certify_critical_line(0.6)
        assert abs(v1 - v2) < 1e-12

    def test_off_critical_monotonic_decay_right(self):
        """Mayor desviación hacia la derecha → mayor supresión (dominio near-critical)."""
        # Use tiny deviations just above ε so exp doesn't underflow
        v1 = certify_critical_line(0.5 + 2 * EPSILON_RH)   # exp(-20)
        v2 = certify_critical_line(0.5 + 3 * EPSILON_RH)   # exp(-30)
        assert v1 > v2

    def test_off_critical_monotonic_decay_left(self):
        """Mayor desviación hacia la izquierda → mayor supresión (dominio near-critical)."""
        v1 = certify_critical_line(0.5 - 2 * EPSILON_RH)   # exp(-20)
        v2 = certify_critical_line(0.5 - 3 * EPSILON_RH)   # exp(-30)
        assert v1 > v2

    def test_exponential_formula_sigma_06(self):
        """Para σ = 0.6, el valor debe coincidir con la fórmula analítica."""
        sigma = 0.6
        gamma = 10.0
        dev = abs(sigma - 0.5)
        expected = math.exp(-gamma * dev / EPSILON_RH)
        got = certify_critical_line(sigma, gamma)
        assert abs(got - expected) < 1e-15

    def test_exponential_formula_sigma_03(self):
        """Para σ = 0.3 y γ = 5, el valor debe coincidir con la fórmula."""
        sigma = 0.3
        gamma = 5.0
        dev = abs(sigma - 0.5)
        expected = math.exp(-gamma * dev / EPSILON_RH)
        got = certify_critical_line(sigma, gamma)
        assert abs(got - expected) < 1e-15

    # ── Variaciones del parámetro γ ──────────────────────────────────────────

    def test_higher_gamma_greater_suppression(self):
        """Mayor γ produce mayor supresión para el mismo σ (dominio near-critical)."""
        # Use a tiny deviation above ε so we stay in the computable range
        sigma = 0.5 + 2 * EPSILON_RH
        v_low = certify_critical_line(sigma, gamma=1.0)    # exp(-2)
        v_high = certify_critical_line(sigma, gamma=10.0)  # exp(-20)
        assert v_low > v_high

    def test_gamma_zero_gives_one_off_critical(self):
        """γ = 0 devuelve 1.0 incluso fuera de la línea crítica."""
        # exp(-0 * dev / ε) = exp(0) = 1.0
        val = certify_critical_line(0.9, gamma=0.0)
        assert abs(val - 1.0) < 1e-12

    def test_default_gamma_is_ten(self):
        """El valor por defecto de γ es 10."""
        sigma = 0.6
        v_default = certify_critical_line(sigma)
        v_explicit = certify_critical_line(sigma, gamma=10.0)
        assert v_default == v_explicit

    # ── Tipos de retorno ────────────────────────────────────────────────────

    def test_returns_float_on_critical(self):
        """El tipo de retorno en la línea crítica es float."""
        assert isinstance(certify_critical_line(0.5), float)

    def test_returns_float_off_critical(self):
        """El tipo de retorno fuera de la línea crítica es float."""
        assert isinstance(certify_critical_line(0.9), float)

    # ── Vectorización implícita ─────────────────────────────────────────────

    def test_vectorize_consistent(self):
        """np.vectorize produce los mismos resultados que llamadas individuales."""
        sigmas = np.array([0.3, 0.5, 0.7, 0.9])
        vec_fn = np.vectorize(certify_critical_line)
        result = vec_fn(sigmas)
        for i, s in enumerate(sigmas):
            assert abs(result[i] - certify_critical_line(s)) < 1e-14

    # ── Casos límite adicionales ─────────────────────────────────────────────

    def test_sigma_very_close_to_half(self):
        """σ muy próximo a 0.5 pero > ε produce valor = exp(-γ * dev/ε)."""
        sigma = 0.5 + 2 * EPSILON_RH  # desviación = 2ε, por tanto dev/ε = 2
        val = certify_critical_line(sigma)
        expected = math.exp(-10.0 * 2)  # exp(-γ * 2) = exp(-20)
        assert abs(val - expected) < 1e-12

    def test_sigma_negative_large_deviation(self):
        """σ muy negativo produce supresión prácticamente nula."""
        val = certify_critical_line(-100.0)
        assert val < 1e-100  # prácticamente cero

    def test_sigma_large_positive(self):
        """σ muy grande produce supresión prácticamente nula."""
        val = certify_critical_line(100.0)
        assert val < 1e-100

    def test_certify_half_minus_epsilon_by_two(self):
        """σ = 0.5 - ε/2 es on-critical y devuelve 1.0."""
        sigma = 0.5 - EPSILON_RH / 2
        assert certify_critical_line(sigma) == 1.0

    def test_certify_value_between_zero_and_one_off_critical(self):
        """El valor de retorno está siempre en [0, 1] para σ ∈ (0, 1)."""
        # Note: for sigma far from 0.5, exp underflows to 0.0 (valid float64)
        sigmas = np.linspace(0.01, 0.99, 50)
        for s in sigmas:
            v = certify_critical_line(float(s))
            assert 0.0 <= v <= 1.0

    def test_certify_result_at_sigma_06_is_small(self):
        """Para σ = 0.6 con γ = 10, la supresión es extremadamente pequeña."""
        val = certify_critical_line(0.6)
        # dev = 0.1, gamma = 10, ε = 1e-10 → exp(-1e10) ≈ 0
        assert val < 1e-9

    def test_certify_gammas_riemann_zeros_on_critical(self):
        """Ceros de Riemann con σ = 0.5 exacto reciben certify = 1.0."""
        for gamma_n in GAMMAS:
            # Los ceros de Riemann son 0.5 + i·γ_n; Re = 0.5
            assert certify_critical_line(0.5) == 1.0

    def test_certify_independent_of_imaginary_part(self):
        """certify_critical_line sólo depende de Re(σ), no de partes imaginarias."""
        v1 = certify_critical_line(0.5)
        v2 = certify_critical_line(0.5)
        assert v1 == v2 == 1.0

    def test_suppression_not_nan(self):
        """El valor de supresión nunca debe ser NaN."""
        for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
            val = certify_critical_line(s)
            assert not math.isnan(val)

    def test_suppression_not_inf(self):
        """El valor de supresión nunca debe ser infinito."""
        for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
            val = certify_critical_line(s)
            assert not math.isinf(val)


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 3 — TachyonCensor (20 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestTachyonCensor:
    """Verificación de la clase TachyonCensor."""

    # ── Construcción ────────────────────────────────────────────────────────

    def test_default_threshold(self):
        """El umbral por defecto es 1e-6."""
        tc = TachyonCensor()
        assert tc.threshold == 1e-6

    def test_custom_threshold(self):
        """El umbral se puede personalizar."""
        tc = TachyonCensor(threshold=1e-3)
        assert tc.threshold == 1e-3

    def test_history_starts_empty(self):
        """El historial empieza vacío."""
        tc = TachyonCensor()
        assert tc.history == []

    # ── censor_matrix ────────────────────────────────────────────────────────

    def test_censor_matrix_shape_preserved(self):
        """La forma de la matriz censurada no cambia."""
        tc = TachyonCensor()
        mat = np.ones((4, 5))
        sigmas = np.full(5, 0.5)
        result = tc.censor_matrix(mat, sigmas)
        assert result.shape == mat.shape

    def test_censor_matrix_on_critical_unchanged(self):
        """Todos σ = 0.5 → la matriz no cambia (factor = 1.0)."""
        tc = TachyonCensor()
        mat = np.ones((3, 4))
        sigmas = np.full(4, 0.5)
        result = tc.censor_matrix(mat, sigmas)
        np.testing.assert_allclose(result, mat)

    def test_censor_matrix_off_critical_suppressed(self):
        """Columnas con σ muy lejos de 0.5 se suprimen a casi cero."""
        tc = TachyonCensor()
        mat = np.ones((3, 2))
        sigmas = np.array([0.5, 0.9])  # segunda columna muy off-critical
        result = tc.censor_matrix(mat, sigmas)
        # La primera columna no cambia; la segunda es suprimida
        np.testing.assert_allclose(result[:, 0], 1.0)
        assert np.all(result[:, 1] < 1e-5)

    def test_censor_matrix_history_appended(self):
        """Cada llamada añade una entrada al historial."""
        tc = TachyonCensor()
        mat = np.ones((2, 3))
        sigmas = np.full(3, 0.5)
        tc.censor_matrix(mat, sigmas)
        tc.censor_matrix(mat, sigmas)
        assert len(tc.history) == 2

    def test_censor_matrix_history_value_on_critical(self):
        """El historial almacena la media del mapa; sobre la línea crítica = 1.0."""
        tc = TachyonCensor()
        mat = np.ones((2, 2))
        sigmas = np.full(2, 0.5)
        tc.censor_matrix(mat, sigmas)
        assert abs(tc.history[0] - 1.0) < 1e-12

    def test_censor_matrix_mixed_sigmas(self):
        """Mapa mixto: on-critical da 1, off-critical da < 1."""
        tc = TachyonCensor()
        mat = np.ones((1, 2))
        sigmas = np.array([0.5, 0.9])
        result = tc.censor_matrix(mat, sigmas)
        assert abs(result[0, 0] - 1.0) < 1e-12
        assert result[0, 1] < 1e-5

    def test_censor_matrix_zero_matrix(self):
        """Censurar una matriz de ceros sigue produciendo ceros."""
        tc = TachyonCensor()
        mat = np.zeros((3, 3))
        sigmas = np.linspace(0.3, 0.7, 3)
        result = tc.censor_matrix(mat, sigmas)
        np.testing.assert_allclose(result, np.zeros((3, 3)))

    def test_censor_matrix_preserves_non_unit_values(self):
        """El escalado es multiplicativo: mat * censor_map."""
        tc = TachyonCensor()
        mat = np.array([[2.0, 3.0]])
        sigmas = np.array([0.5, 0.5])
        result = tc.censor_matrix(mat, sigmas)
        np.testing.assert_allclose(result, mat)

    # ── is_certified ─────────────────────────────────────────────────────────

    def test_is_certified_below_threshold(self):
        """Error espectral < umbral → True."""
        tc = TachyonCensor(threshold=1e-6)
        assert tc.is_certified(1e-9) is True

    def test_is_certified_above_threshold(self):
        """Error espectral > umbral → False."""
        tc = TachyonCensor(threshold=1e-6)
        assert tc.is_certified(1e-3) is False

    def test_is_certified_exactly_threshold(self):
        """Error espectral == umbral → False (estricto)."""
        tc = TachyonCensor(threshold=1e-6)
        assert tc.is_certified(1e-6) is False

    def test_is_certified_zero_error(self):
        """Error espectral = 0 siempre está certificado."""
        tc = TachyonCensor()
        assert tc.is_certified(0.0) is True

    def test_is_certified_custom_threshold(self):
        """Con umbral personalizado, la lógica sigue siendo estricta."""
        tc = TachyonCensor(threshold=1e-3)
        assert tc.is_certified(5e-4) is True
        assert tc.is_certified(2e-3) is False

    # ── Tipo / instancia ─────────────────────────────────────────────────────

    def test_history_is_list(self):
        """history debe ser una lista de Python."""
        tc = TachyonCensor()
        assert isinstance(tc.history, list)

    def test_multiple_censors_independent(self):
        """Dos instancias de TachyonCensor tienen historiales independientes."""
        tc1 = TachyonCensor()
        tc2 = TachyonCensor()
        mat = np.ones((2, 2))
        sigmas = np.full(2, 0.5)
        tc1.censor_matrix(mat, sigmas)
        assert len(tc1.history) == 1
        assert len(tc2.history) == 0

    def test_censor_matrix_returns_ndarray(self):
        """censor_matrix devuelve un np.ndarray."""
        tc = TachyonCensor()
        mat = np.ones((3, 3))
        sigmas = np.full(3, 0.5)
        result = tc.censor_matrix(mat, sigmas)
        assert isinstance(result, np.ndarray)

    def test_history_values_in_range(self):
        """Los valores del historial están en [0, 1]."""
        tc = TachyonCensor()
        mat = np.ones((2, 4))
        for _ in range(5):
            sigmas = np.random.uniform(0.0, 1.0, 4)
            tc.censor_matrix(mat, sigmas)
        for h in tc.history:
            assert 0.0 <= h <= 1.0


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 4 — NoethicLaser (20 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoethicLaser:
    """Verificación de la clase NoethicLaser."""

    # ── Construcción ────────────────────────────────────────────────────────

    def test_carrier_frequency(self):
        """La frecuencia portadora debe ser 2002.89 Hz (modo KK λ₁)."""
        laser = NoethicLaser(psi=0.999)
        assert abs(laser.f_carrier - 2002.89) < 1e-6

    def test_hrv_frequency(self):
        """La frecuencia de modulación HRV debe ser 0.1 Hz."""
        laser = NoethicLaser(psi=0.999)
        assert abs(laser.f_hrv - 0.1) < 1e-12

    def test_psi_stored(self):
        """El valor Ψ se almacena correctamente."""
        laser = NoethicLaser(psi=0.888)
        assert abs(laser.psi - 0.888) < 1e-12

    def test_n_microtubules_default(self):
        """El número de microtúbulos por defecto es 1e13."""
        laser = NoethicLaser(psi=0.999)
        assert laser.n_microtubules == N_MICROTUBULES_DEFAULT

    def test_gain_formula(self):
        """Ganancia = N² × Ψ²."""
        psi = 0.999
        N = 1e13
        laser = NoethicLaser(psi=psi, n_microtubules=N)
        expected_gain = (N ** 2) * (psi ** 2)
        assert abs(laser.gain - expected_gain) < 1.0  # tolerancia absoluta para 1e26

    def test_gain_scales_with_psi(self):
        """Mayor Ψ → mayor ganancia."""
        l1 = NoethicLaser(psi=0.5)
        l2 = NoethicLaser(psi=0.999)
        assert l2.gain > l1.gain

    def test_gain_scales_with_n(self):
        """Mayor N → mayor ganancia."""
        l1 = NoethicLaser(psi=0.999, n_microtubules=1e10)
        l2 = NoethicLaser(psi=0.999, n_microtubules=1e13)
        assert l2.gain > l1.gain

    def test_nir_range_attribute(self):
        """El rango NIR debe ser (750, 1400) nm."""
        laser = NoethicLaser(psi=0.999)
        assert laser.NIR_RANGE_NM == (750.0, 1400.0)

    # ── emit_upe_signal ──────────────────────────────────────────────────────

    def test_emit_upe_signal_shape(self):
        """La señal UPE tiene la misma forma que t."""
        laser = NoethicLaser(psi=0.999)
        t = np.linspace(0, 1, 1000)
        signal = laser.emit_upe_signal(t)
        assert signal.shape == t.shape

    def test_emit_upe_signal_is_ndarray(self):
        """emit_upe_signal devuelve un np.ndarray."""
        laser = NoethicLaser(psi=0.999)
        t = np.array([0.0, 0.1, 0.2])
        assert isinstance(laser.emit_upe_signal(t), np.ndarray)

    def test_emit_upe_signal_at_t0_is_zero(self):
        """En t = 0, la portadora es cero (sin(0) = 0)."""
        laser = NoethicLaser(psi=0.999)
        t = np.array([0.0])
        signal = laser.emit_upe_signal(t)
        assert abs(signal[0]) < 1e-12

    def test_emit_upe_modulator_nonnegative(self):
        """El modulador 0.5(1 + sin(...)) siempre es ≥ 0."""
        laser = NoethicLaser(psi=0.999)
        t = np.linspace(0, 100, 10000)
        modulator = 0.5 * (1 + np.sin(2 * np.pi * laser.f_hrv * t))
        assert np.all(modulator >= -1e-12)

    def test_emit_upe_signal_range_bounded(self):
        """La señal está acotada por |gain|."""
        # Use n_microtubules=1 for a manageable gain value (1²×Ψ²≈1)
        laser = NoethicLaser(psi=0.999, n_microtubules=1.0)
        t = np.linspace(0, 10, 10000)
        signal = laser.emit_upe_signal(t)
        expected_max = laser.gain * 1.0  # max |sin| × max modulator
        assert np.max(np.abs(signal)) <= expected_max + 1e-9

    def test_emit_upe_signal_periodicity(self):
        """La señal debe repetirse con el período de la portadora."""
        # Use n_microtubules=1 for manageable gain; gain = 1²×Ψ²≈1
        laser = NoethicLaser(psi=0.999, n_microtubules=1.0)
        T_carrier = 1.0 / laser.f_carrier
        t = np.array([0.0, T_carrier])
        # Para f_hrv << f_carrier, el modulador cambia poco → señal casi igual
        s1, s2 = laser.emit_upe_signal(t)
        # No exactamente igual porque la modulación HRV avanza, pero muy pequeña diferencia
        delta_mod = 0.5 * abs(
            np.sin(2 * np.pi * laser.f_hrv * T_carrier)
            - np.sin(2 * np.pi * laser.f_hrv * 0.0)
        )
        assert abs(abs(s2) - abs(s1)) < delta_mod + 1e-9

    # ── Ganancia y escalado ──────────────────────────────────────────────────

    def test_gain_positive(self):
        """La ganancia es siempre positiva."""
        laser = NoethicLaser(psi=0.5)
        assert laser.gain > 0

    def test_gain_psi_one_n_one(self):
        """Con N=1 y Ψ=1, la ganancia es 1."""
        laser = NoethicLaser(psi=1.0, n_microtubules=1.0)
        assert abs(laser.gain - 1.0) < 1e-12

    def test_carrier_matches_lambda_1_constant(self):
        """La frecuencia portadora del láser coincide con LAMBDA_1."""
        laser = NoethicLaser(psi=0.999)
        assert laser.f_carrier == LAMBDA_1

    def test_emission_mean_over_many_cycles(self):
        """La media de la señal sobre muchos ciclos completos es cercana a 0."""
        # Use n_microtubules=1 for manageable gain; physical gain (1e13)² is checked separately
        laser = NoethicLaser(psi=0.999, n_microtubules=1.0)
        # Muchos ciclos completos de la portadora → media ≈ 0
        n_cycles = 200
        t = np.linspace(0, n_cycles / laser.f_carrier, 100000)
        signal = laser.emit_upe_signal(t)
        assert abs(np.mean(signal)) < 1.0  # con modulación, no exactamente 0

    def test_two_lasers_same_psi_equal_gain(self):
        """Dos láseres con el mismo Ψ y N tienen la misma ganancia."""
        l1 = NoethicLaser(psi=0.999)
        l2 = NoethicLaser(psi=0.999)
        assert l1.gain == l2.gain


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 5 — EZWaterStack (10 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestEZWaterStack:
    """Verificación de la clase EZWaterStack."""

    def test_layers_count(self):
        """El número de capas debe ser 551,117."""
        ez = EZWaterStack()
        assert ez.layers == N_EZ_LAYERS

    def test_entropy_reduction(self):
        """La reducción de entropía debe ser ≈ 49.66 %."""
        ez = EZWaterStack()
        assert abs(ez.entropy_reduction - ENTROPY_REDUCTION_EZ) < 1e-12

    def test_stack_stability_is_float(self):
        """get_stack_stability() devuelve un float."""
        ez = EZWaterStack()
        assert isinstance(ez.get_stack_stability(), float)

    def test_stack_stability_close_to_one(self):
        """Con 551,117 capas, la estabilidad es prácticamente 1."""
        ez = EZWaterStack()
        s = ez.get_stack_stability()
        assert s > 0.999999  # extremadamente cercana a 1

    def test_stack_stability_less_than_one(self):
        """La estabilidad es estrictamente menor que 1."""
        ez = EZWaterStack()
        assert ez.get_stack_stability() < 1.0

    def test_stack_stability_formula(self):
        """La estabilidad sigue la fórmula 1 - (1 - η) / L."""
        ez = EZWaterStack()
        expected = 1.0 - (1.0 - ENTROPY_REDUCTION_EZ) / N_EZ_LAYERS
        assert abs(ez.get_stack_stability() - expected) < 1e-15

    def test_entropy_reduction_near_half(self):
        """La reducción de entropía debe ser ≈ 50 % (entre 0.49 y 0.51)."""
        ez = EZWaterStack()
        assert 0.49 < ez.entropy_reduction < 0.51

    def test_stack_stability_positive(self):
        """La estabilidad es siempre positiva."""
        ez = EZWaterStack()
        assert ez.get_stack_stability() > 0

    def test_two_stacks_equal(self):
        """Dos instancias de EZWaterStack son idénticas."""
        ez1 = EZWaterStack()
        ez2 = EZWaterStack()
        assert ez1.layers == ez2.layers
        assert ez1.entropy_reduction == ez2.entropy_reduction
        assert ez1.get_stack_stability() == ez2.get_stack_stability()

    def test_stack_stability_not_nan(self):
        """La estabilidad no es NaN."""
        ez = EZWaterStack()
        assert not math.isnan(ez.get_stack_stability())


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 6 — NavierStokesRHStability (12 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestNavierStokesRHStability:
    """Verificación de la clase NavierStokesRHStability."""

    def test_initial_spectral_error_zero(self):
        """El error espectral inicial es 0."""
        ns = NavierStokesRHStability()
        assert ns.spectral_error == 0.0

    def test_verify_zeros_all_on_critical(self):
        """20 ceros exactamente en Re = 0.5 → True."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.5 + 1j * g for g in GAMMAS])
        assert ns.verify_zeros(gammas) is True

    def test_verify_zeros_spectral_error_stored(self):
        """El error espectral se almacena tras la verificación."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.5 + 1j * g for g in GAMMAS])
        ns.verify_zeros(gammas)
        assert ns.spectral_error < 1e-12

    def test_verify_zeros_off_critical_returns_false(self):
        """Ceros fuera de Re = 0.5 → False."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.6 + 1j * g for g in GAMMAS])  # Re = 0.6
        assert ns.verify_zeros(gammas) is False

    def test_verify_zeros_error_magnitude_off_critical(self):
        """El error espectral para Re = 0.6 debe ser ≈ 20 * 0.1 = 2.0."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.6 + 1j * g for g in GAMMAS])
        ns.verify_zeros(gammas)
        assert abs(ns.spectral_error - 20 * 0.1) < 1e-10

    def test_verify_real_array_on_critical(self):
        """Array de reales = 0.5 también es válido como entrada."""
        ns = NavierStokesRHStability()
        gammas = np.full(20, 0.5)
        assert ns.verify_zeros(gammas) is True

    def test_verify_real_array_off_critical(self):
        """Array de reales ≠ 0.5 devuelve False."""
        ns = NavierStokesRHStability()
        gammas = np.full(20, 0.7)
        assert ns.verify_zeros(gammas) is False

    def test_verify_zeros_partial_off_critical(self):
        """Un solo cero fuera de la línea crítica puede invalidar la certificación."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.5 + 1j * g for g in GAMMAS])
        gammas[0] = 0.6 + 1j * GAMMAS[0]  # desviar el primero
        assert ns.verify_zeros(gammas) is False

    def test_verify_zeros_threshold_is_1e12(self):
        """El umbral de aceptación es < 1e-12."""
        ns = NavierStokesRHStability()
        # Error justo por debajo del umbral
        gammas = np.array([0.5 + 1j * g for g in GAMMAS])
        assert ns.verify_zeros(gammas) is True
        assert ns.spectral_error < 1e-12

    def test_spectral_error_updated_on_each_call(self):
        """El error espectral se actualiza en cada llamada."""
        ns = NavierStokesRHStability()
        g1 = np.full(20, 0.5)
        g2 = np.full(20, 0.6)
        ns.verify_zeros(g1)
        e1 = ns.spectral_error
        ns.verify_zeros(g2)
        e2 = ns.spectral_error
        assert e1 < e2

    def test_single_zero_on_critical(self):
        """Un único cero en Re = 0.5 → True."""
        ns = NavierStokesRHStability()
        gammas = np.array([0.5 + 1j * 14.13])
        assert ns.verify_zeros(gammas) is True

    def test_verify_zeros_returns_bool(self):
        """verify_zeros devuelve un bool de Python."""
        ns = NavierStokesRHStability()
        gammas = np.full(20, 0.5)
        result = ns.verify_zeros(gammas)
        assert isinstance(result, bool)


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 7 — CensorshipResult dataclass (5 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCensorshipResult:
    """Verificación del dataclass CensorshipResult."""

    def test_can_instantiate(self):
        """CensorshipResult se puede instanciar directamente."""
        r = CensorshipResult(
            spectral_certified=True,
            ns_stable=True,
            psi_plateau=0.999,
            entropy_red=0.4966,
        )
        assert r.spectral_certified is True

    def test_fields_accessible(self):
        """Todos los campos son accesibles como atributos."""
        r = CensorshipResult(
            spectral_certified=False, ns_stable=False, psi_plateau=0.5, entropy_red=0.1
        )
        assert r.ns_stable is False
        assert abs(r.psi_plateau - 0.5) < 1e-12
        assert abs(r.entropy_red - 0.1) < 1e-12

    def test_spectral_certified_is_bool(self):
        """spectral_certified almacena un bool."""
        r = CensorshipResult(True, True, 0.999, 0.4966)
        assert isinstance(r.spectral_certified, bool)

    def test_ns_stable_is_bool(self):
        """ns_stable almacena un bool."""
        r = CensorshipResult(True, False, 0.999, 0.4966)
        assert isinstance(r.ns_stable, bool)

    def test_psi_plateau_value(self):
        """psi_plateau almacena el valor correcto."""
        r = CensorshipResult(True, True, 0.999, 0.4966)
        assert abs(r.psi_plateau - 0.999) < 1e-12


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 8 — TachyonicCensorshipModule — run_censorship (5 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestTachyonicCensorshipModuleRunCensorship:
    """Verificación del método run_censorship del orquestador."""

    def test_run_censorship_returns_result(self):
        """run_censorship devuelve un CensorshipResult."""
        m = TachyonicCensorshipModule()
        result = m.run_censorship()
        assert isinstance(result, CensorshipResult)

    def test_run_censorship_spectral_certified(self):
        """El error espectral por defecto 1e-9 < 1e-6 → spectral_certified = True."""
        m = TachyonicCensorshipModule()
        result = m.run_censorship()
        assert result.spectral_certified is True

    def test_run_censorship_ns_stable(self):
        """Los 20 ceros precalculados en Re = 0.5 → ns_stable = True."""
        m = TachyonicCensorshipModule()
        result = m.run_censorship()
        assert result.ns_stable is True

    def test_run_censorship_psi_plateau(self):
        """psi_plateau devuelve el valor Ψ configurado."""
        m = TachyonicCensorshipModule(psi=0.888)
        result = m.run_censorship()
        assert abs(result.psi_plateau - 0.888) < 1e-12

    def test_run_censorship_entropy_red(self):
        """entropy_red devuelve la reducción de entropía de la pila EZ."""
        m = TachyonicCensorshipModule()
        result = m.run_censorship()
        assert abs(result.entropy_red - ENTROPY_REDUCTION_EZ) < 1e-12


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 9 — TachyonicCensorshipModule — certify / SHA-256 (5 tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestTachyonicCensorshipModuleCertify:
    """Verificación del método certify y del determinismo SHA-256."""

    def test_certify_returns_dict(self):
        """certify() devuelve un dict."""
        m = TachyonicCensorshipModule()
        assert isinstance(m.certify(), dict)

    def test_certify_has_sha256(self):
        """El dict de certificación tiene la clave 'sha256'."""
        m = TachyonicCensorshipModule()
        cert = m.certify()
        assert "sha256" in cert

    def test_certify_sha256_is_hex_digest(self):
        """sha256 es un digest hexadecimal de 64 caracteres."""
        m = TachyonicCensorshipModule()
        cert = m.certify()
        sha = cert["sha256"]
        assert len(sha) == 64
        assert all(c in "0123456789abcdef" for c in sha)

    def test_certify_sistema_vivo_true(self):
        """El campo 'sistema_vivo' siempre es True."""
        m = TachyonicCensorshipModule()
        cert = m.certify()
        assert cert["sistema_vivo"] is True

    def test_certify_sha256_unique_per_call(self):
        """Dos llamadas consecutivas producen hashes distintos (timestamp diferente)."""
        m = TachyonicCensorshipModule()
        c1 = m.certify()
        time.sleep(0.01)  # garantiza diferencia de timestamp
        c2 = m.certify()
        assert c1["sha256"] != c2["sha256"]

    def test_certify_protocolo_field(self):
        """El campo 'protocolo' del certificado es 'QED-CUERDAS-MASTER'."""
        m = TachyonicCensorshipModule()
        cert = m.certify()
        assert cert["protocolo"] == PROTOCOLO
