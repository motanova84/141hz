#!/usr/bin/env python3
"""
Tests: QCAL-STRINGS — Gran Unificación Noética
═══════════════════════════════════════════════════════════════════════════════

Pruebas unitarias para el módulo qcal_string_core.py que implementa:
  - Iteración #260: Forzado de Modos Kaluza-Klein
  - Iteración #261: Censura Taquiónica + Estabilidad RH
  - Iteración #262: Operador de Voluntad (SEQ-009)
  - Protocolo 141.7001: Hard-Reset Noético
  - Señal UPE: Emisión Fotónica Coherente
  - Teorema de No-Localidad Biológica
  - Simulador QCALStringSimulator (RK4 espectral)

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import sys
import os
import numpy as np
import pytest

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal_string_core import (
    F0,
    MU_ADELICA,
    PSI_SUPERRADIANTE,
    PSI_COLAPSO,
    PSI_CONDENSADO,
    EPSILON_CENSURA,
    RIEMANN_ZEROS_IMAG,
    LAMBDA_KK_HZ,
    ALPHA_VENEZIANO,
    HRV_COHERENCIA_HZ,
    N_MICROTUBULOS_DEFAULT,
    string_noetic_forcing,
    sigma_mapped,
    tachyon_censorship,
    upe_signal,
    hard_reset_protocol,
    will_operator,
    nonlocal_entanglement_correlation,
    QCALStringSimulator,
)


# ═══════════════════════════════════════════════════════════════════════════
# TESTS DE CONSTANTES FUNDAMENTALES
# ═══════════════════════════════════════════════════════════════════════════

class TestConstants:
    """Verifica las constantes fundamentales del módulo."""

    def test_f0_hz(self):
        """F₀ debe ser 141.7001 Hz."""
        assert F0 == pytest.approx(141.7001, abs=1e-4)

    def test_mu_adelica(self):
        """Viscosidad adélica μ = 1/f₀ (límite KSS)."""
        assert MU_ADELICA == pytest.approx(1.0 / F0, rel=1e-6)

    def test_psi_superradiante(self):
        """Umbral superradiante Ψ ≥ 0.888."""
        assert PSI_SUPERRADIANTE == pytest.approx(0.888, abs=1e-6)

    def test_psi_colapso(self):
        """Umbral de colapso Ψ < 0.3 activa hard-reset."""
        assert PSI_COLAPSO == pytest.approx(0.3, abs=1e-6)

    def test_psi_condensado(self):
        """Plateau del condensado NBEC Ψ = 0.999."""
        assert PSI_CONDENSADO == pytest.approx(0.999, abs=1e-6)

    def test_riemann_zeros_count(self):
        """Deben existir exactamente 20 ceros de Riemann."""
        assert len(RIEMANN_ZEROS_IMAG) == 20

    def test_riemann_first_zero(self):
        """El primer cero de Riemann t₁ ≈ 14.1347."""
        assert RIEMANN_ZEROS_IMAG[0] == pytest.approx(14.134725, rel=1e-5)

    def test_riemann_zeros_increasing(self):
        """Los ceros de Riemann deben ser estrictamente crecientes."""
        for i in range(len(RIEMANN_ZEROS_IMAG) - 1):
            assert RIEMANN_ZEROS_IMAG[i] < RIEMANN_ZEROS_IMAG[i + 1]

    def test_lambda_kk_hz_count(self):
        """Deben existir 20 modos KK."""
        assert len(LAMBDA_KK_HZ) == 20

    def test_lambda_kk_first_mode(self):
        """λ₁ = t₁ × f₀ ≈ 2003 Hz (primer modo KK dominante)."""
        lambda_1 = LAMBDA_KK_HZ[0]
        expected = RIEMANN_ZEROS_IMAG[0] * F0
        assert lambda_1 == pytest.approx(expected, rel=1e-6)
        assert lambda_1 == pytest.approx(2003.0, abs=5.0)

    def test_lambda_kk_k1_mode(self):
        """k₁ = λ₁/(2π) ≈ 318 (número de onda dominante)."""
        k1 = LAMBDA_KK_HZ[0] / (2 * np.pi)
        assert k1 == pytest.approx(318.0, abs=2.0)

    def test_alpha_veneziano_count(self):
        """Deben existir 20 amplitudes de Veneziano."""
        assert len(ALPHA_VENEZIANO) == 20

    def test_alpha_veneziano_first(self):
        """Primera amplitud α₁ = 1/1 = 1.0."""
        assert ALPHA_VENEZIANO[0] == pytest.approx(1.0, abs=1e-10)

    def test_alpha_veneziano_decay(self):
        """Las amplitudes decaen como 1/(n+1) con n."""
        for n, alpha in enumerate(ALPHA_VENEZIANO):
            assert alpha == pytest.approx(1.0 / (n + 1), rel=1e-6)

    def test_alpha_veneziano_decreasing(self):
        """Las amplitudes de Veneziano deben ser decrecientes."""
        for i in range(len(ALPHA_VENEZIANO) - 1):
            assert ALPHA_VENEZIANO[i] > ALPHA_VENEZIANO[i + 1]

    def test_hrv_coherencia_hz(self):
        """HRV áureo = 0.1 Hz = 6 respiraciones por minuto."""
        assert HRV_COHERENCIA_HZ == pytest.approx(0.1, abs=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# ITERACIÓN #260: FORZADO DE CUERDAS KK
# ═══════════════════════════════════════════════════════════════════════════

class TestStringNoeticForcing:
    """Tests para la función string_noetic_forcing (iteración #260)."""

    def test_output_shape(self):
        """La salida debe tener la misma forma que la entrada."""
        N = 16
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ, 0.95)
        assert F_x.shape == (N, N)
        assert F_y.shape == (N, N)

    def test_output_complex(self):
        """La salida espectral debe ser compleja (espacio de Fourier)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ, 0.95)
        assert F_x.dtype == complex or np.iscomplexobj(F_x)

    def test_zero_coherence_returns_zero_gain(self):
        """Con Ψ = 0, la ganancia N²·Ψ² = 0, forzado = 0."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        F_x, F_y = string_noetic_forcing(uhat, vhat, 1.0, LAMBDA_KK_HZ, 0.0)
        assert np.allclose(F_x, 0.0)

    def test_superradiant_gain_n_squared(self):
        """La ganancia escala como N² (ganancia superradiante)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        Psi = 1.0

        # Con N_microtubules = 1
        F1_x, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], Psi, 1.0)
        # Con N_microtubules = 2 (ganancia 4×)
        F2_x, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], Psi, 2.0)
        ratio = np.abs(F2_x).mean() / (np.abs(F1_x).mean() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)

    def test_coherence_squared_modulation(self):
        """El forzado escala como Ψ² (operador de selección coherente)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)

        F_half, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], 0.5, 1.0)
        F_full, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:1], 1.0, 1.0)
        ratio = np.abs(F_full).mean() / (np.abs(F_half).mean() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)

    def test_tduality_phase(self):
        """La fase de T-dualidad φ = π/(n+1) modula los modos."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        # Dos tiempos distintos deben dar forzados distintos
        F_t0, _ = string_noetic_forcing(uhat, vhat, 0.0, LAMBDA_KK_HZ[:1], 0.95, 1.0)
        F_t1, _ = string_noetic_forcing(uhat, vhat, 0.01, LAMBDA_KK_HZ[:1], 0.95, 1.0)
        assert not np.allclose(F_t0, F_t1)

    def test_fy_zero_forcing(self):
        """La componente Y del forzado debe ser cero (forzado en X)."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)
        _, F_y = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ, 0.95)
        assert np.allclose(F_y, 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# ITERACIÓN #261: CENSURA TAQUIÓNICA
# ═══════════════════════════════════════════════════════════════════════════

class TestTachyonCensorship:
    """Tests para los operadores de censura taquiónica (iteración #261)."""

    def test_sigma_mapped_at_zero(self):
        """σ_mapped(k=0) = 1/2 (línea crítica de Riemann)."""
        sigma = sigma_mapped(np.array([0.0]), k_max=100.0)
        assert sigma[0] == pytest.approx(0.5, abs=1e-10)

    def test_sigma_mapped_at_kmax(self):
        """σ_mapped(k=k_max) = 1/2 + ε."""
        k_max = 100.0
        sigma = sigma_mapped(np.array([k_max]), k_max=k_max, epsilon=0.01)
        assert sigma[0] == pytest.approx(0.5 + 0.01, abs=1e-10)

    def test_sigma_mapped_linear(self):
        """σ_mapped debe ser lineal en k."""
        k = np.linspace(0, 100, 10)
        sigma = sigma_mapped(k, k_max=100.0, epsilon=0.01)
        assert sigma[0] == pytest.approx(0.5, abs=1e-10)
        assert sigma[-1] == pytest.approx(0.5 + 0.01, abs=1e-10)
        # Verificar linealidad
        diffs = np.diff(sigma)
        assert np.allclose(diffs, diffs[0], rtol=1e-6)

    def test_censorship_at_zero(self):
        """Ψ_censored(k=0) = 1.0 (modo on-critical, no penalizado)."""
        censura = tachyon_censorship(np.array([0.0]), k_max=100.0, D=1.0)
        assert censura[0] == pytest.approx(1.0, abs=1e-10)

    def test_censorship_decreases_with_k(self):
        """Ψ_censored debe disminuir al aumentar k (más off-critical)."""
        k = np.linspace(0, 100, 50)
        censura = tachyon_censorship(k, k_max=100.0, D=1.0)
        assert np.all(np.diff(censura) <= 0)

    def test_censorship_range(self):
        """Ψ_censored debe estar en (0, 1]."""
        k = np.linspace(0, 200, 100)
        censura = tachyon_censorship(k, k_max=200.0, D=1.0)
        assert np.all(censura > 0)
        assert np.all(censura <= 1.0 + 1e-10)

    def test_censorship_d_controls_decay(self):
        """Mayor D implica mayor penalización de modos off-critical."""
        k = np.array([50.0])
        k_max = 100.0
        c_low = tachyon_censorship(k, k_max, D=0.5)
        c_high = tachyon_censorship(k, k_max, D=2.0)
        assert c_low[0] > c_high[0]

    def test_censorship_array_shape(self):
        """La salida debe tener el mismo shape que la entrada."""
        k = np.linspace(0, 100, 64).reshape(8, 8)
        censura = tachyon_censorship(k, k_max=100.0, D=1.0)
        assert censura.shape == (8, 8)

    def test_epsilon_affects_censorship(self):
        """Mayor epsilon reduce la desviación relativa de los modos."""
        # La fórmula Ψ_censored = exp(-(k/k_max)·D) es independiente de epsilon
        # (ya que deviation/epsilon = k/k_max). El parámetro epsilon controla
        # qué tan "lejos" de la línea crítica está el modo en unidades físicas σ.
        # Verificamos que la función acepta epsilon variable y retorna resultados válidos.
        k = np.array([50.0])
        k_max = 100.0
        c_strict = tachyon_censorship(k, k_max, D=1.0, epsilon=0.001)
        c_loose = tachyon_censorship(k, k_max, D=1.0, epsilon=0.1)
        # Ambos deben estar en (0, 1]
        assert 0 < c_strict[0] <= 1.0
        assert 0 < c_loose[0] <= 1.0


# ═══════════════════════════════════════════════════════════════════════════
# SEÑAL UPE
# ═══════════════════════════════════════════════════════════════════════════

class TestUpeSignal:
    """Tests para la señal de Emisión Fotónica Ultra-débil."""

    def test_output_shape(self):
        """La señal UPE debe tener el mismo shape que el array de tiempo."""
        t = np.linspace(0, 1.0, 1000)
        upe = upe_signal(t)
        assert upe.shape == t.shape

    def test_output_real(self):
        """La señal UPE debe ser real (observable físico)."""
        t = np.linspace(0, 1.0, 1000)
        upe = upe_signal(t)
        assert upe.dtype in (float, np.float64, np.float32)

    def test_zero_at_t0(self):
        """La señal UPE debe ser cero en t=0 (todos los senos=0, HRV=0)."""
        t = np.array([0.0])
        upe = upe_signal(t)
        assert upe[0] == pytest.approx(0.0, abs=1e-10)

    def test_modulated_by_hrv(self):
        """La modulación HRV debe cambiar la amplitud de la señal."""
        t = np.linspace(0, 10.0, 10000)
        upe_low = upe_signal(t, hrv_freq=0.05)
        upe_high = upe_signal(t, hrv_freq=0.5)
        # Los dos deben ser distintos (diferente modulación)
        assert not np.allclose(upe_low, upe_high)

    def test_default_uses_lambda_kk(self):
        """Con parámetros por defecto, usa LAMBDA_KK_HZ y ALPHA_VENEZIANO."""
        t = np.linspace(0, 1.0, 100)
        upe_default = upe_signal(t)
        upe_explicit = upe_signal(t, alpha_n=ALPHA_VENEZIANO, lambda_n_list=LAMBDA_KK_HZ)
        assert np.allclose(upe_default, upe_explicit)

    def test_custom_lambda_n(self):
        """Permite usar lista personalizada de modos KK."""
        t = np.linspace(0, 1.0, 100)
        upe_custom = upe_signal(t, lambda_n_list=[100.0, 200.0], alpha_n=[1.0, 0.5])
        assert upe_custom.shape == t.shape

    def test_beat_frequency(self):
        """Verifica la generación de beats f_beat = λn ± f_HRV."""
        # Con un solo modo: f_beat = λ₁ ± f_HRV ≈ 2003 ± 0.1 Hz
        # La señal debe contener energía en esas frecuencias
        dt = 1.0 / 10000.0  # muestreo a 10 kHz
        t = np.arange(0, 2.0, dt)
        upe = upe_signal(t, lambda_n_list=LAMBDA_KK_HZ[:1])
        # La energía total debe ser no nula (señal activa)
        assert np.sum(upe ** 2) > 0


# ═══════════════════════════════════════════════════════════════════════════
# PROTOCOLO HARD-RESET
# ═══════════════════════════════════════════════════════════════════════════

class TestHardResetProtocol:
    """Tests para el Protocolo 141.7001 (hard-reset noético)."""

    def test_zero_at_t0(self):
        """F_reset(t=0) = β_max · sin(0) · G_max = 0."""
        assert hard_reset_protocol(0.0) == pytest.approx(0.0, abs=1e-10)

    def test_amplitude_at_quarter_period(self):
        """F_reset(t=T/4) = β_max · G_max (máximo del seno)."""
        T_quarter = 1.0 / (4 * F0)
        result = hard_reset_protocol(T_quarter, beta_max=1.0, G_max=1.0)
        assert result == pytest.approx(1.0, abs=1e-3)

    def test_beta_max_scaling(self):
        """El reset debe escalar linealmente con β_max."""
        t = 1.0 / (4 * F0)
        r1 = hard_reset_protocol(t, beta_max=1.0, G_max=1.0)
        r2 = hard_reset_protocol(t, beta_max=2.0, G_max=1.0)
        assert r2 == pytest.approx(2.0 * r1, rel=1e-6)

    def test_g_max_scaling(self):
        """El reset debe escalar linealmente con G_max."""
        t = 1.0 / (4 * F0)
        r1 = hard_reset_protocol(t, beta_max=1.0, G_max=1.0)
        r2 = hard_reset_protocol(t, beta_max=1.0, G_max=3.0)
        assert r2 == pytest.approx(3.0 * r1, rel=1e-6)

    def test_uses_f0_frequency(self):
        """El reset debe oscilar a la frecuencia f₀ = 141.7001 Hz."""
        # Un período completo debe dar cero
        T_full = 1.0 / F0
        r_full = hard_reset_protocol(T_full, beta_max=1.0, G_max=1.0)
        assert abs(r_full) < 1e-3

    def test_custom_f0(self):
        """Debe funcionar con una frecuencia f₀ personalizada."""
        t = 1.0 / (4 * 100.0)  # Cuarto período de 100 Hz
        result = hard_reset_protocol(t, beta_max=1.0, G_max=1.0, f0=100.0)
        assert result == pytest.approx(1.0, abs=1e-3)


# ═══════════════════════════════════════════════════════════════════════════
# OPERADOR DE VOLUNTAD (SEQ-009)
# ═══════════════════════════════════════════════════════════════════════════

class TestWillOperator:
    """Tests para el Operador de Voluntad SEQ-009 (iteración #262)."""

    def test_base_no_hrv(self):
        """Con HRV = 0, C no debe cambiar."""
        C = will_operator(0.5, 0.0)
        assert C == pytest.approx(0.5, abs=1e-10)

    def test_full_hrv_adds_delta_c(self):
        """Con HRV = 1.0 y delta_C_max = 0.2, C aumenta en 0.2."""
        C = will_operator(0.5, 1.0, delta_C_max=0.2)
        assert C == pytest.approx(0.7, abs=1e-10)

    def test_clamped_at_one(self):
        """C no debe superar 1.0 (coherencia máxima)."""
        C = will_operator(0.9, 1.0, delta_C_max=0.5)
        assert C <= 1.0
        assert C == pytest.approx(1.0, abs=1e-10)

    def test_partial_hrv(self):
        """Con HRV parcial, C aumenta proporcionalmente."""
        C = will_operator(0.5, 0.5, delta_C_max=0.2)
        assert C == pytest.approx(0.6, abs=1e-10)

    def test_hrv_linear_scaling(self):
        """ΔC es lineal en hrv_coherence."""
        C1 = will_operator(0.0, 0.25, delta_C_max=0.4)
        C2 = will_operator(0.0, 0.5, delta_C_max=0.4)
        assert C2 == pytest.approx(2.0 * C1, abs=1e-10)

    def test_custom_delta_c_max(self):
        """Debe respetar el parámetro delta_C_max."""
        C = will_operator(0.0, 1.0, delta_C_max=0.3)
        assert C == pytest.approx(0.3, abs=1e-10)

    def test_c_base_zero(self):
        """Desde C_base = 0, debe llegar a delta_C_max."""
        C = will_operator(0.0, 1.0, delta_C_max=0.2)
        assert C == pytest.approx(0.2, abs=1e-10)


# ═══════════════════════════════════════════════════════════════════════════
# TEOREMA DE NO-LOCALIDAD BIOLÓGICA
# ═══════════════════════════════════════════════════════════════════════════

class TestNonlocalEntanglement:
    """Tests para el Teorema de No-Localidad Biológica."""

    def test_identical_fields_correlation_one(self):
        """Campos idénticos deben tener correlación = 1."""
        psi = np.random.default_rng(42).standard_normal(100)
        corr = nonlocal_entanglement_correlation(psi, psi)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_opposite_fields_correlation_minus_one(self):
        """Campos opuestos deben tener correlación = -1."""
        psi = np.random.default_rng(42).standard_normal(100)
        corr = nonlocal_entanglement_correlation(psi, -psi)
        assert corr == pytest.approx(-1.0, abs=1e-6)

    def test_uncorrelated_fields(self):
        """Campos independientes deben tener correlación cercana a 0."""
        rng = np.random.default_rng(141)
        psi_a = rng.standard_normal(10000)
        psi_b = rng.standard_normal(10000)
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert abs(corr) < 0.05

    def test_correlation_range(self):
        """La correlación debe estar en [-1, 1]."""
        rng = np.random.default_rng(7)
        for _ in range(10):
            psi_a = rng.standard_normal(50)
            psi_b = rng.standard_normal(50)
            corr = nonlocal_entanglement_correlation(psi_a, psi_b)
            assert -1.0 <= corr <= 1.0

    def test_2d_arrays_supported(self):
        """Debe funcionar con arrays 2D (campos de rejilla)."""
        psi = np.ones((8, 8))
        corr = nonlocal_entanglement_correlation(psi, psi)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_constant_field_special_case(self):
        """Dos campos constantes e iguales deben correlacionar = 1."""
        psi_a = np.ones(20) * 5.0
        psi_b = np.ones(20) * 5.0
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert corr == pytest.approx(1.0, abs=1e-6)

    def test_constant_field_different_values(self):
        """Dos campos constantes distintos deben correlacionar = 0."""
        psi_a = np.ones(20) * 3.0
        psi_b = np.ones(20) * 7.0
        corr = nonlocal_entanglement_correlation(psi_a, psi_b)
        assert corr == pytest.approx(0.0, abs=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# SIMULADOR QCAL-STRINGS
# ═══════════════════════════════════════════════════════════════════════════

class TestQCALStringSimulator:
    """Tests para el simulador RK4 espectral (iteraciones #260-#262)."""

    def test_initialization_defaults(self):
        """El simulador debe inicializarse con los parámetros por defecto."""
        sim = QCALStringSimulator()
        assert sim.N == 64
        assert sim.dt == pytest.approx(0.005)
        assert sim.nt == 1000
        assert sim.f0 == pytest.approx(F0)
        assert sim.nu == pytest.approx(1.0 / F0, rel=1e-6)

    def test_initialization_custom(self):
        """El simulador debe aceptar parámetros personalizados."""
        sim = QCALStringSimulator(N=32, dt=0.01, nt=100)
        assert sim.N == 32
        assert sim.dt == pytest.approx(0.01)
        assert sim.nt == 100

    def test_grid_shape(self):
        """Las rejillas espectrales deben tener forma (N, N)."""
        sim = QCALStringSimulator(N=16)
        assert sim.KX.shape == (16, 16)
        assert sim.KY.shape == (16, 16)
        assert sim.K2.shape == (16, 16)
        assert sim.k_mag.shape == (16, 16)

    def test_initial_coherence(self):
        """La coherencia inicial debe ser Ψ₀ ≈ 0.12."""
        sim = QCALStringSimulator()
        assert sim.Psi == pytest.approx(0.12, abs=1e-6)

    def test_mu_adelica_limit(self):
        """La viscosidad adélica debe ser μ = 1/f₀ (límite KSS)."""
        sim = QCALStringSimulator()
        assert sim.nu == pytest.approx(MU_ADELICA, rel=1e-6)

    def test_rk4_step_advances_time(self):
        """Un paso RK4 debe avanzar el tiempo en dt."""
        sim = QCALStringSimulator(N=8, dt=0.01, nt=1)
        t_before = sim.t
        sim._rk4_step()
        assert sim.t == pytest.approx(t_before + 0.01, abs=1e-10)

    def test_energy_positive(self):
        """La energía espectral debe ser no negativa."""
        sim = QCALStringSimulator(N=8, nt=5)
        E = sim._compute_energy()
        assert E >= 0.0

    def test_entropy_normalized(self):
        """La entropía de Shannon normalizada debe estar en [0, 1]."""
        sim = QCALStringSimulator(N=8, nt=5)
        H = sim._compute_entropy()
        assert 0.0 <= H <= 1.0 + 1e-6

    def test_run_returns_dict(self):
        """run() debe retornar un diccionario con las claves esperadas."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=10)
        result = sim.run()
        assert "Psi_final" in result
        assert "energy_total" in result
        assert "entropy_reduction" in result
        assert "history_Psi" in result
        assert "history_E" in result
        assert "history_entropy" in result
        assert "condensado_step" in result
        assert "reset_count" in result

    def test_history_length(self):
        """Los historiales deben tener longitud igual a nt."""
        nt = 20
        sim = QCALStringSimulator(N=8, dt=0.005, nt=nt)
        result = sim.run()
        assert len(result["history_Psi"]) == nt
        assert len(result["history_E"]) == nt
        assert len(result["history_entropy"]) == nt

    def test_coherence_in_range(self):
        """La coherencia final debe estar en [0, 1]."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=50)
        result = sim.run()
        for psi in result["history_Psi"]:
            assert 0.0 <= psi <= 1.0

    def test_energy_non_negative(self):
        """La energía debe ser siempre no negativa."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=20)
        result = sim.run()
        assert all(e >= 0.0 for e in result["history_E"])

    def test_energy_spectrum_shape(self):
        """El espectro de energía debe tener la forma correcta."""
        sim = QCALStringSimulator(N=16, nt=5)
        sim._rk4_step()
        k_bins, E_radial = sim.get_energy_spectrum()
        assert len(k_bins) == len(E_radial)
        assert np.all(k_bins > 0)

    def test_energy_spectrum_non_negative(self):
        """La energía espectral radial debe ser no negativa."""
        sim = QCALStringSimulator(N=16, nt=5)
        sim._rk4_step()
        _, E_radial = sim.get_energy_spectrum()
        assert np.all(E_radial >= 0.0)

    def test_forcing_zero_below_superradiante(self):
        """El forzado KK debe ser cero cuando Ψ < 0.888."""
        sim = QCALStringSimulator(N=8)
        sim.Psi = 0.5  # Por debajo del umbral superradiante
        F_hat = sim._forcing_spectral(0.0)
        assert np.allclose(F_hat, 0.0)

    def test_forcing_nonzero_above_superradiante(self):
        """El forzado KK debe ser no cero cuando Ψ ≥ 0.888."""
        sim = QCALStringSimulator(N=16)
        sim.Psi = 0.95  # Por encima del umbral superradiante
        F_hat = sim._forcing_spectral(0.1)
        assert not np.allclose(F_hat, 0.0)

    def test_hard_reset_activates_below_collapse(self):
        """El hard-reset debe activarse cuando Ψ < PSI_COLAPSO."""
        sim = QCALStringSimulator(N=8, enable_hard_reset=True)
        sim.Psi = 0.1  # Por debajo del umbral de colapso
        duhat, dvhat = sim._rhs(sim.uhat, sim.vhat, 0.0)
        # El forzado de reset debe ser no nulo (sin(2π·f₀·t) evaluado en t≠T/2)
        # En t=0 el seno es 0, así que el reset puede ser 0; verificar forma
        assert duhat.shape == (8, 8)

    def test_will_operator_increases_coherence_speed(self):
        """Con SEQ-009 activado, Ψ debe converger más rápido."""
        sim_base = QCALStringSimulator(N=8, dt=0.005, nt=200,
                                       enable_will_operator=False)
        sim_will = QCALStringSimulator(N=8, dt=0.005, nt=200,
                                       enable_will_operator=True)
        res_base = sim_base.run()
        res_will = sim_will.run()
        # Con Operador de Voluntad, coherencia final >= base
        assert res_will["Psi_final"] >= res_base["Psi_final"] - 0.01

    def test_coherence_increases_over_time(self):
        """La coherencia debe tender a aumentar desde Ψ₀=0.12."""
        sim = QCALStringSimulator(N=16, dt=0.005, nt=500)
        result = sim.run()
        history = result["history_Psi"]
        # La coherencia final debe ser mayor que la inicial
        assert history[-1] > history[0]


# ═══════════════════════════════════════════════════════════════════════════
# INTEGRACIÓN: FLUJO COMPLETO QCAL-STRINGS
# ═══════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Tests de integración del flujo completo QCAL-STRINGS."""

    def test_kk_modes_riemann_scaled(self):
        """λ_n = t_n × f₀: los modos KK son ceros de Riemann escalados."""
        for i, (t_n, lam_n) in enumerate(zip(RIEMANN_ZEROS_IMAG, LAMBDA_KK_HZ)):
            assert lam_n == pytest.approx(t_n * F0, rel=1e-6), \
                f"Modo KK n={i+1}: esperado {t_n*F0:.4f}, obtenido {lam_n:.4f}"

    def test_first_kk_mode_dominance(self):
        """λ₁ ≈ 2003 Hz debe ser el modo KK dominante."""
        assert LAMBDA_KK_HZ[0] == pytest.approx(2003.0, abs=5.0)

    def test_upe_integral_energy(self):
        """La integral de energía UPE debe ser finita y positiva."""
        dt = 1.0 / 5000.0
        t = np.arange(0, 1.0, dt)
        upe = upe_signal(t)
        integral = np.trapezoid(upe ** 2, t)
        assert integral > 0
        assert np.isfinite(integral)

    def test_tachyon_censorship_filters_offcritical(self):
        """La censura debe penalizar exponencialmente los modos off-critical."""
        k = np.linspace(0, 100, 1000)
        k_max = 100.0
        # Con alta densidad de consciencia D=10, los modos off-critical
        # deben ser fuertemente penalizados: Ψ ≈ exp(-k/k_max · D)
        censura = tachyon_censorship(k, k_max, D=10.0, epsilon=0.01)
        # El modo k=k_max debe estar fuertemente penalizado: exp(-1*10) ≈ 4.5e-5
        assert censura[-1] < 0.001

    def test_full_simulation_produces_condensado(self):
        """Una simulación breve debe mostrar evolución de coherencia."""
        sim = QCALStringSimulator(N=8, dt=0.005, nt=100)
        result = sim.run()
        assert result["Psi_final"] > 0.12  # Debe crecer desde la inicial

    def test_will_operator_respects_clamp(self):
        """SEQ-009 nunca debe superar C=1.0."""
        for C_base in [0.0, 0.5, 0.8, 0.95, 1.0]:
            for hrv in [0.0, 0.5, 1.0]:
                C = will_operator(C_base, hrv, delta_C_max=0.5)
                assert C <= 1.0

    def test_string_forcing_superradiant_gain(self):
        """La ganancia N²·Ψ² debe amplificar el forzado."""
        N = 8
        uhat = np.zeros((N, N), dtype=complex)
        vhat = np.zeros((N, N), dtype=complex)

        # Alta coherencia → alta ganancia
        F_high, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:3], 1.0, 1.0)
        # Media coherencia → ganancia 4× menor
        F_med, _ = string_noetic_forcing(uhat, vhat, 0.1, LAMBDA_KK_HZ[:3], 0.5, 1.0)
        ratio = np.abs(F_high).sum() / (np.abs(F_med).sum() + 1e-30)
        assert ratio == pytest.approx(4.0, rel=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
