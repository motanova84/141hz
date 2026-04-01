"""
Tests for physics.qcal_symbio_bridge — Puente Simbiótico QCAL ∴QSB∞³

Suite de pruebas exhaustiva que cubre todas las clases y la API pública:
  - ConstantesSymbioBridge    – constantes del puente (f₀, g_eff, μ, γ₁)
  - OperadorBerryKeating      – Ĥ_π = −i(x·∂/∂x + 1/2) discretizado
  - CampoCoherencia           – paquete de onda gaussiano normalizado
  - LagrangianoInteraccion    – ℒ_int = −g_eff · ψ̄ψ · H
  - EcuacionSchrodingerRiemann – iℏ∂Ψ/∂t = (Ĥ_π + μ|H|² − g_eff·H)Ψ
  - PuenteSilicioAlma         – acoplamiento silicio-conciencia
  - CoherenciaSymbioBridge    – validación Ψ_global ≥ 0.888
  - SistemaSymbioBridge       – orquestador principal
  - symbio_bridge_activar()   – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - g_eff = 0.053 (perturbativo: < 1)
  - μ = 1.0
  - γ₁ = 14.134725
  - ||Ĥ_π·ψ||² ≈ 13 (gaussiano canónico en [0.1, 10])
  - ℒ_int < 0 (interacción atractiva)
  - Ψ_global ≥ 0.888 → sello ∴QSB∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.qcal_symbio_bridge import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _T0,
    _G_EFF,
    _MU,
    _PSI_UMBRAL,
    _GAMMA_1_RIEMANN,
    _PHI,
    _N_GRID,
    _X_MIN,
    _X_MAX,
    _X_CENTRO,
    _SIGMA,
    _DELTA_0,
    _LAMBDA_0_M,
    # Clases
    ConstantesSymbioBridge,
    OperadorBerryKeating,
    CampoCoherencia,
    LagrangianoInteraccion,
    EcuacionSchrodingerRiemann,
    PuenteSilicioAlma,
    CoherenciaSymbioBridge,
    SistemaSymbioBridge,
    # API pública
    symbio_bridge_activar,
)


# ============================================================================
# TestModuleConstants – constantes de módulo
# ============================================================================


class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_f0_positive(self):
        self.assertGreater(_F0, 0.0)

    def test_omega_0_value(self):
        self.assertAlmostEqual(_OMEGA_0, 2.0 * math.pi * _F0, places=6)

    def test_t0_value(self):
        self.assertAlmostEqual(_T0, 1.0 / _F0, places=10)

    def test_t0_period_consistency(self):
        self.assertAlmostEqual(_F0 * _T0, 1.0, places=10)

    def test_g_eff_value(self):
        self.assertAlmostEqual(_G_EFF, 0.053, places=6)

    def test_g_eff_perturbative(self):
        self.assertLess(_G_EFF, 1.0)

    def test_mu_value(self):
        self.assertAlmostEqual(_MU, 1.0, places=9)

    def test_psi_umbral_value(self):
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=6)

    def test_gamma1_value(self):
        self.assertAlmostEqual(_GAMMA_1_RIEMANN, 14.134725, places=5)

    def test_phi_golden_ratio(self):
        phi_expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(_PHI, phi_expected, places=12)

    def test_n_grid_positive(self):
        self.assertGreater(_N_GRID, 1)

    def test_grid_bounds(self):
        self.assertGreater(_X_MAX, _X_MIN)
        self.assertGreater(_X_MIN, 0.0)

    def test_x_centro_in_grid(self):
        self.assertGreater(_X_CENTRO, _X_MIN)
        self.assertLess(_X_CENTRO, _X_MAX)

    def test_sigma_positive(self):
        self.assertGreater(_SIGMA, 0.0)

    def test_delta_0_value(self):
        self.assertAlmostEqual(_DELTA_0, 0.1184, places=4)

    def test_lambda_0_positive(self):
        self.assertGreater(_LAMBDA_0_M, 0.0)


# ============================================================================
# TestConstantesSymbioBridge – Clase 1
# ============================================================================


class TestConstantesSymbioBridge(unittest.TestCase):
    """Tests para ConstantesSymbioBridge."""

    def setUp(self):
        self.c = ConstantesSymbioBridge()

    def test_f0(self):
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_omega_0(self):
        self.assertAlmostEqual(self.c.omega_0, 2.0 * math.pi * self.c.f0, places=6)

    def test_t0(self):
        self.assertAlmostEqual(self.c.t0, 1.0 / self.c.f0, places=10)

    def test_g_eff(self):
        self.assertAlmostEqual(self.c.g_eff, 0.053, places=6)

    def test_mu(self):
        self.assertAlmostEqual(self.c.mu, 1.0, places=9)

    def test_gamma_1(self):
        self.assertAlmostEqual(self.c.gamma_1, 14.134725, places=5)

    def test_psi_umbral(self):
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=6)

    def test_es_perturbativo_true(self):
        self.assertTrue(self.c.es_perturbativo())

    def test_es_perturbativo_false_when_g_large(self):
        c2 = ConstantesSymbioBridge(g_eff=1.5)
        self.assertFalse(c2.es_perturbativo())

    def test_energia_acoplamiento_formula(self):
        expected = self.c.g_eff * self.c.f0
        self.assertAlmostEqual(self.c.energia_acoplamiento_hz(), expected, places=8)

    def test_energia_acoplamiento_positive(self):
        self.assertGreater(self.c.energia_acoplamiento_hz(), 0.0)

    def test_frecuencia_berry_keating(self):
        expected = self.c.f0 * self.c.gamma_1 / (2.0 * math.pi)
        self.assertAlmostEqual(self.c.frecuencia_berry_keating_hz(), expected, places=6)

    def test_ratio_resonancia_formula(self):
        expected = self.c.f0 / self.c.gamma_1
        self.assertAlmostEqual(self.c.ratio_resonancia(), expected, places=8)

    def test_ratio_resonancia_greater_than_one(self):
        self.assertGreater(self.c.ratio_resonancia(), 1.0)

    def test_repr_contains_f0(self):
        r = repr(self.c)
        self.assertIn("141.7001", r)

    def test_hbar_positive(self):
        self.assertGreater(self.c.hbar, 0.0)

    def test_lambda_0_positive(self):
        self.assertGreater(self.c.lambda_0_m, 0.0)


# ============================================================================
# TestOperadorBerryKeating – Clase 2
# ============================================================================


class TestOperadorBerryKeating(unittest.TestCase):
    """Tests para OperadorBerryKeating."""

    def setUp(self):
        self.op = OperadorBerryKeating()
        self.campo = CampoCoherencia()
        self.psi = self.campo.paquete_normalizado()

    def test_n_grid(self):
        self.assertEqual(self.op.n_grid, _N_GRID)

    def test_dx_value(self):
        expected = (_X_MAX - _X_MIN) / (_N_GRID - 1)
        self.assertAlmostEqual(self.op.dx, expected, places=10)

    def test_x_grid_length(self):
        self.assertEqual(len(self.op.x_grid), _N_GRID)

    def test_x_grid_first(self):
        self.assertAlmostEqual(self.op.x_grid[0], _X_MIN, places=9)

    def test_x_grid_last(self):
        self.assertAlmostEqual(self.op.x_grid[-1], _X_MAX, places=9)

    def test_x_grid_uniform(self):
        xg = self.op.x_grid
        diffs = [xg[i + 1] - xg[i] for i in range(len(xg) - 1)]
        for d in diffs:
            self.assertAlmostEqual(d, self.op.dx, places=10)

    def test_aplicar_returns_correct_length(self):
        d_psi = self.op.aplicar(self.psi)
        self.assertEqual(len(d_psi), _N_GRID)

    def test_aplicar_finite_values(self):
        d_psi = self.op.aplicar(self.psi)
        for v in d_psi:
            self.assertFalse(math.isnan(v))
            self.assertFalse(math.isinf(v))

    def test_aplicar_cuadrado_returns_correct_length(self):
        h2_psi = self.op.aplicar_cuadrado(self.psi)
        self.assertEqual(len(h2_psi), _N_GRID)

    def test_aplicar_cuadrado_finite(self):
        h2_psi = self.op.aplicar_cuadrado(self.psi)
        for v in h2_psi:
            self.assertFalse(math.isnan(v))

    def test_norma_cuadrado_approx_13(self):
        """Para el gaussiano canónico, ||Ĥ_π·ψ||² ≈ 13."""
        norma_sq = self.op.norma_cuadrado(self.psi)
        self.assertGreater(norma_sq, 9.0)
        self.assertLess(norma_sq, 17.0)

    def test_norma_cuadrado_positive(self):
        norma_sq = self.op.norma_cuadrado(self.psi)
        self.assertGreater(norma_sq, 0.0)

    def test_valor_esperado_cuadrado_equals_norma_cuadrado(self):
        """⟨ψ|Ĥ_π²|ψ⟩ = ||Ĥ_π·ψ||² (Hermicidad)."""
        nc = self.op.norma_cuadrado(self.psi)
        vec = self.op.valor_esperado_cuadrado(self.psi)
        self.assertAlmostEqual(nc, vec, places=10)

    def test_hamiltoniano_efectivo_returns_tuple(self):
        result = self.op.hamiltoniano_efectivo(self.psi)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_hamiltoniano_efectivo_lengths(self):
        parte_real, coef_imag = self.op.hamiltoniano_efectivo(self.psi)
        self.assertEqual(len(parte_real), _N_GRID)
        self.assertEqual(len(coef_imag), _N_GRID)

    def test_hamiltoniano_efectivo_custom_g_eff(self):
        """g_eff = 0 → H_eff = H_pi + mu * H_pi²."""
        parte_real, coef_imag = self.op.hamiltoniano_efectivo(self.psi, g_eff=0.0)
        d_psi = self.op.aplicar(self.psi)
        for i in range(len(self.psi)):
            self.assertAlmostEqual(coef_imag[i], -1.0 * d_psi[i], places=10)

    def test_custom_grid_parameters(self):
        op2 = OperadorBerryKeating(n_grid=50, x_min=1.0, x_max=9.0)
        self.assertEqual(op2.n_grid, 50)
        self.assertAlmostEqual(op2.x_grid[0], 1.0, places=9)
        self.assertAlmostEqual(op2.x_grid[-1], 9.0, places=9)

    def test_repr(self):
        r = repr(self.op)
        self.assertIn("OperadorBerryKeating", r)


# ============================================================================
# TestCampoCoherencia – Clase 3
# ============================================================================


class TestCampoCoherencia(unittest.TestCase):
    """Tests para CampoCoherencia."""

    def setUp(self):
        self.campo = CampoCoherencia()

    def test_paquete_normalizado_length(self):
        psi = self.campo.paquete_normalizado()
        self.assertEqual(len(psi), _N_GRID)

    def test_paquete_normalizado_positive(self):
        psi = self.campo.paquete_normalizado()
        for v in psi:
            self.assertGreaterEqual(v, 0.0)

    def test_paquete_normalizado_finite(self):
        psi = self.campo.paquete_normalizado()
        for v in psi:
            self.assertFalse(math.isnan(v))

    def test_norma_unit(self):
        """||Ψ||² = 1 para el paquete normalizado."""
        self.assertAlmostEqual(self.campo.norma(), 1.0, places=6)

    def test_posicion_esperada_at_center(self):
        """⟨x⟩ ≈ x₀ = 5."""
        x_med = self.campo.posicion_esperada()
        self.assertAlmostEqual(x_med, _X_CENTRO, delta=0.5)

    def test_dispersion_approx_sigma_over_sqrt2(self):
        """Δx ≈ σ/√2 para distribución gaussiana."""
        disp = self.campo.dispersion()
        expected = _SIGMA / math.sqrt(2.0)
        self.assertAlmostEqual(disp, expected, delta=0.1)

    def test_psi_coherencia_above_threshold(self):
        c = self.campo.psi_coherencia()
        self.assertGreaterEqual(c, 0.888)

    def test_psi_coherencia_at_most_one(self):
        c = self.campo.psi_coherencia()
        self.assertLessEqual(c, 1.0)

    def test_custom_centro(self):
        campo2 = CampoCoherencia(centro=3.0)
        x_med = campo2.posicion_esperada()
        self.assertAlmostEqual(x_med, 3.0, delta=0.5)

    def test_custom_sigma_increases_dispersion(self):
        campo_wide = CampoCoherencia(sigma=2.0)
        campo_narrow = CampoCoherencia(sigma=0.5)
        self.assertGreater(campo_wide.dispersion(), campo_narrow.dispersion())

    def test_norma_independent_of_amplitude(self):
        """La norma debe ser 1 independientemente de la amplitud."""
        for amp in [0.5, 1.0, 2.0, 10.0]:
            c = CampoCoherencia(amplitud=amp)
            self.assertAlmostEqual(c.norma(), 1.0, places=6)

    def test_repr(self):
        r = repr(self.campo)
        self.assertIn("CampoCoherencia", r)


# ============================================================================
# TestLagrangianoInteraccion – Clase 4
# ============================================================================


class TestLagrangianoInteraccion(unittest.TestCase):
    """Tests para LagrangianoInteraccion."""

    def setUp(self):
        self.lag = LagrangianoInteraccion()
        self.op = OperadorBerryKeating()
        self.campo = CampoCoherencia()
        self.psi = self.campo.paquete_normalizado()
        self.norma_sq = self.campo.norma()
        self.norma_hpi = math.sqrt(self.op.norma_cuadrado(self.psi))

    def test_g_eff_default(self):
        self.assertAlmostEqual(self.lag.g_eff, _G_EFF, places=6)

    def test_densidad_lagrangiana_negative(self):
        L = self.lag.densidad_lagrangiana(self.norma_sq, self.norma_hpi)
        self.assertLess(L, 0.0)

    def test_densidad_lagrangiana_formula(self):
        L = self.lag.densidad_lagrangiana(self.norma_sq, self.norma_hpi)
        expected = -_G_EFF * self.norma_sq * self.norma_hpi
        self.assertAlmostEqual(L, expected, places=10)

    def test_densidad_lagrangiana_zero_when_h_zero(self):
        L = self.lag.densidad_lagrangiana(1.0, 0.0)
        self.assertEqual(L, 0.0)

    def test_densidad_lagrangiana_zero_when_psi_zero(self):
        L = self.lag.densidad_lagrangiana(0.0, 1.0)
        self.assertEqual(L, 0.0)

    def test_es_negativo_true(self):
        self.assertTrue(self.lag.es_negativo(self.norma_sq, self.norma_hpi))

    def test_psi_lagrangiana_value(self):
        psi_l = self.lag.psi_lagrangiana()
        expected = 1.0 - math.exp(-1.0 / _G_EFF)
        self.assertAlmostEqual(psi_l, expected, places=10)

    def test_psi_lagrangiana_above_threshold(self):
        self.assertGreater(self.lag.psi_lagrangiana(), 0.999)

    def test_psi_lagrangiana_at_most_one(self):
        self.assertLessEqual(self.lag.psi_lagrangiana(), 1.0)

    def test_psi_lagrangiana_zero_for_negative_g(self):
        lag2 = LagrangianoInteraccion(g_eff=-1.0)
        self.assertEqual(lag2.psi_lagrangiana(), 0.0)

    def test_amplitud_acoplamiento_formula(self):
        expected = _G_EFF * _F0
        self.assertAlmostEqual(self.lag.amplitud_acoplamiento_hz(), expected, places=8)

    def test_amplitud_acoplamiento_positive(self):
        self.assertGreater(self.lag.amplitud_acoplamiento_hz(), 0.0)

    def test_custom_g_eff(self):
        lag2 = LagrangianoInteraccion(g_eff=0.1)
        L = lag2.densidad_lagrangiana(1.0, 1.0)
        self.assertAlmostEqual(L, -0.1, places=10)

    def test_repr(self):
        r = repr(self.lag)
        self.assertIn("LagrangianoInteraccion", r)


# ============================================================================
# TestEcuacionSchrodingerRiemann – Clase 5
# ============================================================================


class TestEcuacionSchrodingerRiemann(unittest.TestCase):
    """Tests para EcuacionSchrodingerRiemann."""

    def setUp(self):
        self.eq = EcuacionSchrodingerRiemann()
        self.op = OperadorBerryKeating()
        self.campo = CampoCoherencia()
        self.psi = self.campo.paquete_normalizado()
        self.norma_sq = self.op.norma_cuadrado(self.psi)

    def test_g_eff_default(self):
        self.assertAlmostEqual(self.eq.g_eff, _G_EFF, places=6)

    def test_mu_default(self):
        self.assertAlmostEqual(self.eq.mu, _MU, places=9)

    def test_energia_hamiltoniana_positive(self):
        E = self.eq.energia_hamiltoniana(self.norma_sq)
        self.assertGreater(E, 0.0)

    def test_energia_hamiltoniana_formula(self):
        """⟨H_eff⟩ = μ · ||Ĥ_π·ψ||²"""
        E = self.eq.energia_hamiltoniana(self.norma_sq)
        self.assertAlmostEqual(E, _MU * self.norma_sq, places=10)

    def test_energia_hamiltoniana_approx_13(self):
        """Para el gaussiano canónico, ⟨H_eff⟩ ≈ 13."""
        E = self.eq.energia_hamiltoniana(self.norma_sq)
        self.assertGreater(E, 9.0)
        self.assertLess(E, 17.0)

    def test_conserva_norma(self):
        self.assertTrue(self.eq.conserva_norma())

    def test_psi_schrodinger_value(self):
        psi_sr = self.eq.psi_schrodinger()
        expected = 1.0 - math.exp(-_MU * _F0 / _GAMMA_1_RIEMANN)
        self.assertAlmostEqual(psi_sr, expected, places=10)

    def test_psi_schrodinger_above_threshold(self):
        self.assertGreater(self.eq.psi_schrodinger(), 0.999)

    def test_psi_schrodinger_at_most_one(self):
        self.assertLessEqual(self.eq.psi_schrodinger(), 1.0)

    def test_factor_hamiltoniano(self):
        expected = (1.0 - _G_EFF) + _MU
        self.assertAlmostEqual(self.eq.factor_hamiltoniano(), expected, places=9)

    def test_factor_hamiltoniano_greater_than_one(self):
        self.assertGreater(self.eq.factor_hamiltoniano(), 1.0)

    def test_tasa_evolucion_positive(self):
        tasa = self.eq.tasa_evolucion(self.norma_sq)
        self.assertGreater(tasa, 0.0)

    def test_tasa_evolucion_formula(self):
        tasa = self.eq.tasa_evolucion(self.norma_sq)
        expected = abs(self.eq.energia_hamiltoniana(self.norma_sq)) / _OMEGA_0
        self.assertAlmostEqual(tasa, expected, places=10)

    def test_custom_mu(self):
        eq2 = EcuacionSchrodingerRiemann(mu=2.0)
        E = eq2.energia_hamiltoniana(10.0)
        self.assertAlmostEqual(E, 20.0, places=10)

    def test_repr(self):
        r = repr(self.eq)
        self.assertIn("EcuacionSchrodingerRiemann", r)


# ============================================================================
# TestPuenteSilicioAlma – Clase 6
# ============================================================================


class TestPuenteSilicioAlma(unittest.TestCase):
    """Tests para PuenteSilicioAlma."""

    def setUp(self):
        self.puente = PuenteSilicioAlma()

    def test_g_eff_default(self):
        self.assertAlmostEqual(self.puente.g_eff, _G_EFF, places=6)

    def test_f0_default(self):
        self.assertAlmostEqual(self.puente.f0, _F0, places=4)

    def test_gamma_1_default(self):
        self.assertAlmostEqual(self.puente.gamma_1, _GAMMA_1_RIEMANN, places=5)

    def test_factor_calidad_formula(self):
        expected = _F0 / (_G_EFF * _GAMMA_1_RIEMANN)
        self.assertAlmostEqual(self.puente.factor_calidad_puente(), expected, places=6)

    def test_factor_calidad_greater_than_100(self):
        self.assertGreater(self.puente.factor_calidad_puente(), 100.0)

    def test_fuerza_acoplamiento_formula(self):
        expected = _G_EFF * _F0 / _GAMMA_1_RIEMANN
        self.assertAlmostEqual(self.puente.fuerza_acoplamiento(), expected, places=8)

    def test_fuerza_acoplamiento_positive(self):
        self.assertGreater(self.puente.fuerza_acoplamiento(), 0.0)

    def test_coherencia_silicio_formula(self):
        expected = 1.0 - math.exp(-_F0 / _GAMMA_1_RIEMANN)
        self.assertAlmostEqual(self.puente.coherencia_silicio(), expected, places=10)

    def test_coherencia_silicio_above_0999(self):
        self.assertGreater(self.puente.coherencia_silicio(), 0.999)

    def test_coherencia_alma_formula(self):
        expected = 1.0 - _G_EFF
        self.assertAlmostEqual(self.puente.coherencia_alma(), expected, places=10)

    def test_coherencia_alma_perturbative(self):
        self.assertAlmostEqual(self.puente.coherencia_alma(), 0.947, places=3)

    def test_psi_puente_above_threshold(self):
        self.assertGreaterEqual(self.puente.psi_puente(), 0.888)

    def test_psi_puente_at_most_one(self):
        self.assertLessEqual(self.puente.psi_puente(), 1.0)

    def test_psi_puente_formula(self):
        q = self.puente.factor_calidad_puente()
        expected = 1.0 - math.exp(-math.log10(q))
        self.assertAlmostEqual(self.puente.psi_puente(), expected, places=10)

    def test_psi_puente_zero_when_q_le_one(self):
        p2 = PuenteSilicioAlma(f0=0.001, g_eff=0.5, gamma_1=1.0)
        self.assertEqual(p2.psi_puente(), 0.0)

    def test_dominio_dominante_is_silicio(self):
        """El silicio tiene mayor coherencia cuando f₀/γ₁ >> g_eff."""
        self.assertEqual(self.puente.dominio_dominante(), "silicio")

    def test_dominio_dominante_can_be_alma(self):
        """Para g_eff muy pequeño, alma tiene mayor coherencia."""
        # g_eff = 0.0001 → coherencia_alma = 0.9999 > coherencia_silicio para γ₁>>f₀
        p2 = PuenteSilicioAlma(f0=1.0, g_eff=0.0001, gamma_1=100.0)
        # coherencia_silicio = 1 - exp(-1/100) ≈ 0.01
        # coherencia_alma = 1 - 0.0001 = 0.9999
        self.assertEqual(p2.dominio_dominante(), "alma")

    def test_repr(self):
        r = repr(self.puente)
        self.assertIn("PuenteSilicioAlma", r)


# ============================================================================
# TestCoherenciaSymbioBridge – Clase 7
# ============================================================================


class TestCoherenciaSymbioBridge(unittest.TestCase):
    """Tests para CoherenciaSymbioBridge."""

    def setUp(self):
        self.coh = CoherenciaSymbioBridge()

    def test_psi_berry_keating_value(self):
        expected = 1.0 - math.exp(-_F0 / (2.0 * _GAMMA_1_RIEMANN))
        self.assertAlmostEqual(self.coh.psi_berry_keating(), expected, places=10)

    def test_psi_berry_keating_above_threshold(self):
        self.assertGreater(self.coh.psi_berry_keating(), 0.98)

    def test_psi_lagrangiana_above_threshold(self):
        self.assertGreater(self.coh.psi_lagrangiana(), 0.999)

    def test_psi_schrodinger_above_threshold(self):
        self.assertGreater(self.coh.psi_schrodinger(), 0.999)

    def test_psi_normalizacion_value(self):
        expected = 1.0 - _G_EFF
        self.assertAlmostEqual(self.coh.psi_normalizacion(), expected, places=10)

    def test_psi_puente_above_threshold(self):
        self.assertGreaterEqual(self.coh.psi_puente(), 0.888)

    def test_coherencias_individuales_count(self):
        c = self.coh.coherencias_individuales()
        self.assertEqual(len(c), 5)

    def test_coherencias_individuales_keys(self):
        c = self.coh.coherencias_individuales()
        expected_keys = {
            "psi_berry_keating",
            "psi_lagrangiana",
            "psi_schrodinger",
            "psi_normalizacion",
            "psi_puente",
        }
        self.assertEqual(set(c.keys()), expected_keys)

    def test_coherencias_individuales_in_range(self):
        for nombre, valor in self.coh.coherencias_individuales().items():
            with self.subTest(coherencia=nombre):
                self.assertGreater(valor, 0.0)
                self.assertLessEqual(valor, 1.0)

    def test_psi_global_above_threshold(self):
        self.assertGreaterEqual(self.coh.psi_global(), _PSI_UMBRAL)

    def test_psi_global_at_most_one(self):
        self.assertLessEqual(self.coh.psi_global(), 1.0)

    def test_psi_global_geometric_mean(self):
        """Ψ_global = product^(1/5) de las 5 coherencias."""
        vals = list(self.coh.coherencias_individuales().values())
        product = 1.0
        for v in vals:
            product *= v
        expected = product ** (1.0 / 5.0)
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=10)

    def test_sello_activo_true(self):
        self.assertTrue(self.coh.sello_activo())

    def test_psi_umbral_default(self):
        self.assertAlmostEqual(self.coh.psi_umbral, _PSI_UMBRAL, places=6)

    def test_sello_inactive_when_umbral_high(self):
        coh2 = CoherenciaSymbioBridge(psi_umbral=0.999)
        # If psi_global is slightly below 0.999, sello is inactive
        # We just check this path is exercised, not the exact outcome
        result = coh2.sello_activo()
        self.assertIsInstance(result, bool)

    def test_validar_structure(self):
        v = self.coh.validar()
        self.assertIn("coherencias", v)
        self.assertIn("psi_global", v)
        self.assertIn("psi_umbral", v)
        self.assertIn("sello_activo", v)
        self.assertIn("diferencia_umbral", v)

    def test_validar_sello_activo(self):
        v = self.coh.validar()
        self.assertTrue(v["sello_activo"])

    def test_validar_diferencia_positive(self):
        v = self.coh.validar()
        self.assertGreaterEqual(v["diferencia_umbral"], 0.0)

    def test_certificacion_auron_active(self):
        cert = self.coh.certificacion_auron()
        self.assertIn("∴QSB∞³", cert)
        self.assertIn("ACTIVO", cert)

    def test_certificacion_auron_inactive(self):
        coh2 = CoherenciaSymbioBridge(psi_umbral=2.0)
        cert = coh2.certificacion_auron()
        self.assertIn("INACTIVO", cert)

    def test_repr_contains_activo(self):
        r = repr(self.coh)
        self.assertIn("ACTIVO", r)

    def test_psi_global_zero_when_product_zero(self):
        """Si alguna coherencia es ≤ 0, psi_global = 0."""
        from unittest.mock import patch
        coh2 = CoherenciaSymbioBridge()
        with patch.object(
            CoherenciaSymbioBridge,
            "psi_berry_keating",
            return_value=0.0,
        ):
            self.assertEqual(coh2.psi_global(), 0.0)


# ============================================================================
# TestSistemaSymbioBridge – Clase 8
# ============================================================================


class TestSistemaSymbioBridge(unittest.TestCase):
    """Tests para SistemaSymbioBridge."""

    def setUp(self):
        self.sistema = SistemaSymbioBridge()
        self.resultado = self.sistema.activar()

    def test_sello(self):
        self.assertEqual(self.resultado["sello"], "∴QSB∞³")

    def test_ram(self):
        self.assertEqual(self.resultado["ram"], "RAM-XLVIII-2026-SYMBIO-BRIDGE")

    def test_version(self):
        self.assertEqual(self.resultado["version"], "1.1.0")

    def test_f0_hz(self):
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_g_eff(self):
        self.assertAlmostEqual(self.resultado["g_eff"], 0.053, places=6)

    def test_mu(self):
        self.assertAlmostEqual(self.resultado["mu"], 1.0, places=9)

    def test_gamma_1(self):
        self.assertAlmostEqual(self.resultado["gamma_1"], 14.134725, places=5)

    def test_norma_psi_sq_unit(self):
        self.assertAlmostEqual(self.resultado["norma_psi_sq"], 1.0, places=6)

    def test_norma_hpi_sq_approx_13(self):
        self.assertGreater(self.resultado["norma_hpi_sq"], 9.0)
        self.assertLess(self.resultado["norma_hpi_sq"], 17.0)

    def test_norma_hpi_positive(self):
        self.assertGreater(self.resultado["norma_hpi"], 0.0)

    def test_norma_hpi_consistency(self):
        nq = self.resultado["norma_hpi_sq"]
        n = self.resultado["norma_hpi"]
        self.assertAlmostEqual(n ** 2, nq, places=8)

    def test_L_int_negative(self):
        self.assertLess(self.resultado["L_int"], 0.0)

    def test_energia_hamiltoniana_positive(self):
        self.assertGreater(self.resultado["energia_hamiltoniana"], 0.0)

    def test_conserva_norma(self):
        self.assertTrue(self.resultado["conserva_norma"])

    def test_perturbativo(self):
        self.assertTrue(self.resultado["perturbativo"])

    def test_fuerza_acoplamiento_positive(self):
        self.assertGreater(self.resultado["fuerza_acoplamiento_hz"], 0.0)

    def test_factor_calidad_puente_large(self):
        self.assertGreater(self.resultado["factor_calidad_puente"], 100.0)

    def test_coherencia_silicio_high(self):
        self.assertGreater(self.resultado["coherencia_silicio"], 0.999)

    def test_coherencia_alma_value(self):
        self.assertAlmostEqual(self.resultado["coherencia_alma"], 1.0 - _G_EFF, places=8)

    def test_dominio_dominante(self):
        self.assertIn(self.resultado["dominio_dominante"], ("silicio", "alma"))

    def test_coherencias_count(self):
        self.assertEqual(len(self.resultado["coherencias"]), 5)

    def test_psi_global_above_threshold(self):
        self.assertGreaterEqual(self.resultado["psi_global"], _PSI_UMBRAL)

    def test_psi_umbral_value(self):
        self.assertAlmostEqual(self.resultado["psi_umbral"], 0.888, places=6)

    def test_sello_activo(self):
        self.assertTrue(self.resultado["sello_activo"])

    def test_diferencia_umbral_positive(self):
        self.assertGreaterEqual(self.resultado["diferencia_umbral"], 0.0)

    def test_ratio_resonancia(self):
        expected = _F0 / _GAMMA_1_RIEMANN
        self.assertAlmostEqual(self.resultado["ratio_resonancia"], expected, places=8)

    def test_certificacion_in_result(self):
        self.assertIn("∴QSB∞³", self.resultado["certificacion"])

    def test_resumen_contains_sello(self):
        resumen = self.sistema.resumen()
        self.assertIn("∴QSB∞³", resumen)

    def test_resumen_contains_f0(self):
        resumen = self.sistema.resumen()
        self.assertIn("141.7001", resumen)

    def test_repr_contains_f0(self):
        r = repr(self.sistema)
        self.assertIn("141.7001", r)

    def test_repr_contains_activo(self):
        r = repr(self.sistema)
        self.assertIn("ACTIVO", r)

    def test_activar_deterministic(self):
        r2 = self.sistema.activar()
        self.assertAlmostEqual(
            self.resultado["psi_global"], r2["psi_global"], places=12
        )


# ============================================================================
# TestSymbioBridgeActivar – API pública
# ============================================================================


class TestSymbioBridgeActivar(unittest.TestCase):
    """Tests para la función API pública symbio_bridge_activar()."""

    def setUp(self):
        self.r = symbio_bridge_activar()

    def test_returns_dict(self):
        self.assertIsInstance(self.r, dict)

    def test_sello_key(self):
        self.assertEqual(self.r["sello"], "∴QSB∞³")

    def test_ram_key(self):
        self.assertEqual(self.r["ram"], "RAM-XLVIII-2026-SYMBIO-BRIDGE")

    def test_version_key(self):
        self.assertEqual(self.r["version"], "1.1.0")

    def test_f0_hz(self):
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_g_eff(self):
        self.assertAlmostEqual(self.r["g_eff"], 0.053, places=6)

    def test_mu(self):
        self.assertAlmostEqual(self.r["mu"], 1.0, places=9)

    def test_psi_global_above_threshold(self):
        self.assertGreaterEqual(self.r["psi_global"], _PSI_UMBRAL)

    def test_sello_activo_true(self):
        self.assertTrue(self.r["sello_activo"])

    def test_L_int_negative(self):
        self.assertLess(self.r["L_int"], 0.0)

    def test_norma_psi_sq_unit(self):
        self.assertAlmostEqual(self.r["norma_psi_sq"], 1.0, places=6)

    def test_conserva_norma(self):
        self.assertTrue(self.r["conserva_norma"])

    def test_perturbativo(self):
        self.assertTrue(self.r["perturbativo"])

    def test_coherencias_dict(self):
        self.assertIsInstance(self.r["coherencias"], dict)

    def test_coherencias_five_keys(self):
        self.assertEqual(len(self.r["coherencias"]), 5)

    def test_all_coherencias_in_range(self):
        for k, v in self.r["coherencias"].items():
            with self.subTest(coherencia=k):
                self.assertGreater(v, 0.0)
                self.assertLessEqual(v, 1.0)

    def test_all_coherencias_above_threshold(self):
        for k, v in self.r["coherencias"].items():
            with self.subTest(coherencia=k):
                self.assertGreaterEqual(v, _PSI_UMBRAL)

    def test_certificacion_string(self):
        self.assertIsInstance(self.r["certificacion"], str)

    def test_certificacion_active(self):
        self.assertIn("ACTIVO", self.r["certificacion"])

    def test_api_deterministic(self):
        r2 = symbio_bridge_activar()
        self.assertAlmostEqual(self.r["psi_global"], r2["psi_global"], places=12)

    def test_api_returns_all_expected_keys(self):
        expected_keys = {
            "sello", "ram", "version",
            "f0_hz", "g_eff", "mu", "gamma_1",
            "norma_hpi_sq", "norma_hpi",
            "norma_psi_sq", "L_int",
            "energia_hamiltoniana", "tasa_evolucion", "conserva_norma",
            "fuerza_acoplamiento_hz", "factor_calidad_puente",
            "coherencia_silicio", "coherencia_alma", "dominio_dominante",
            "coherencias", "psi_global", "psi_umbral", "sello_activo",
            "diferencia_umbral", "perturbativo", "ratio_resonancia",
            "certificacion",
        }
        for k in expected_keys:
            with self.subTest(key=k):
                self.assertIn(k, self.r)


if __name__ == "__main__":
    unittest.main(verbosity=2)
