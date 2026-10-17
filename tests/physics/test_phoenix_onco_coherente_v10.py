"""
Tests for physics.phoenix_onco_coherente_v10 — Sistema Phoenix Onco Coherente ∴POC∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesPhoenixOnco         – constantes físicas del sistema POC
  - ApoptosisResonante            – acoplamiento apoptótico al campo f₀
  - CicloPhoenix                  – ciclo de reprogramación cuántica 4π
  - MatrizCoherenciaTumoral       – matriz adélica-Riemann de células tumorales
  - HamiltonianoCelularPOC        – hamiltoniano celular E₀ = ℏω₀
  - SuperradianciaMitocondrialPOC – superradiancia mitocondrial colectiva
  - CoherenciaPhoenixOnco         – Ψ_global ≥ 0.888
  - SistemaPhoenixOncoCoherente   – orquestador con activar()
  - ResultadoPhoenixOnco          – dataclass de resultados
  - phoenix_onco_coherente_v10_activar() – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - φ = (1+√5)/2 ≈ 1.6180339887
  - κ_Π ≈ 2.5773
  - 10 ceros de Riemann γₙ (γ₁ ≈ 14.1347)
  - 10 números primos para la estructura adélica
  - Ψ_global ≥ 0.888 → sello ∴POC∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.phoenix_onco_coherente_v10 import (
    # Constantes de módulo
    _F0,
    _OMEGA0,
    _GAMMAS,
    _PRIMOS,
    _PHI,
    _KAPPA_PI,
    _TAU_MITO_S,
    _T0_S,
    _N_CELULAS,
    _PSI_UMBRAL,
    _THETA_PHOENIX_DEG,
    _THETA_PHOENIX_RAD,
    _E_APO,
    _N_MODOS_TUMORAL,
    _SELLO,
    _F_ARMONICOS,
    _F_MITO,
    _DELTA_F_TUMORAL,
    # Clases
    ConstantesPhoenixOnco,
    ApoptosisResonante,
    CicloPhoenix,
    MatrizCoherenciaTumoral,
    HamiltonianoCelularPOC,
    SuperradianciaMitocondrialPOC,
    CoherenciaPhoenixOnco,
    SistemaPhoenixOncoCoherente,
    ResultadoPhoenixOnco,
    # API pública
    phoenix_onco_coherente_v10_activar,
)


# ============================================================================
# TestModuleConstants – 22 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_omega0_derived(self):
        expected = 2.0 * math.pi * _F0
        self.assertAlmostEqual(_OMEGA0, expected, places=5)

    def test_gammas_count(self):
        self.assertEqual(len(_GAMMAS), 10)

    def test_gamma1_value(self):
        self.assertAlmostEqual(_GAMMAS[0], 14.1347251417347, places=5)

    def test_gammas_ascending(self):
        for i in range(len(_GAMMAS) - 1):
            self.assertLess(_GAMMAS[i], _GAMMAS[i + 1])

    def test_primos_count(self):
        self.assertEqual(len(_PRIMOS), 10)

    def test_primos_first(self):
        self.assertEqual(_PRIMOS[0], 2)
        self.assertEqual(_PRIMOS[1], 3)
        self.assertEqual(_PRIMOS[2], 5)

    def test_phi_value(self):
        self.assertAlmostEqual(_PHI, (1 + math.sqrt(5)) / 2, places=10)

    def test_phi_greater_than_one(self):
        self.assertGreater(_PHI, 1.0)

    def test_kappa_pi_value(self):
        self.assertAlmostEqual(_KAPPA_PI, 2.5773, places=4)

    def test_tau_mito_s(self):
        self.assertAlmostEqual(_TAU_MITO_S, 100.0e-15, places=25)

    def test_t0_derived(self):
        self.assertAlmostEqual(_T0_S, 1.0 / _F0, places=15)

    def test_n_celulas(self):
        self.assertEqual(_N_CELULAS, 10)

    def test_psi_umbral(self):
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_theta_phoenix_deg(self):
        self.assertAlmostEqual(_THETA_PHOENIX_DEG, 3.00052, places=4)

    def test_theta_phoenix_rad_derived(self):
        expected = _THETA_PHOENIX_DEG * math.pi / 180.0
        self.assertAlmostEqual(_THETA_PHOENIX_RAD, expected, places=10)

    def test_e_apo_positive(self):
        self.assertGreater(_E_APO, 0)

    def test_n_modos_tumoral(self):
        self.assertEqual(_N_MODOS_TUMORAL, 7)

    def test_sello_string(self):
        self.assertIn("POC", _SELLO)
        self.assertIn("∞³", _SELLO)

    def test_f_armonicos_count(self):
        self.assertEqual(len(_F_ARMONICOS), 10)

    def test_f_armonicos_first(self):
        # f_n = f₀ × γₙ / γ₁ → primer armónico = f₀
        self.assertAlmostEqual(_F_ARMONICOS[0], _F0, places=4)

    def test_f_mito_derived(self):
        expected = _F0 * _PHI ** 2
        self.assertAlmostEqual(_F_MITO, expected, places=4)


# ============================================================================
# TestConstantesPhoenixOnco – 12 tests
# ============================================================================

class TestConstantesPhoenixOnco(unittest.TestCase):
    """Tests para ConstantesPhoenixOnco."""

    def setUp(self):
        self.c = ConstantesPhoenixOnco()

    def test_f0_default(self):
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_phi_default(self):
        self.assertAlmostEqual(self.c.phi, (1 + math.sqrt(5)) / 2, places=10)

    def test_kappa_pi_default(self):
        self.assertAlmostEqual(self.c.kappa_pi, 2.5773, places=4)

    def test_tau_mito_s_default(self):
        self.assertAlmostEqual(self.c.tau_mito_s, 100e-15, places=25)

    def test_n_celulas_default(self):
        self.assertEqual(self.c.n_celulas, 10)

    def test_psi_umbral_default(self):
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_omega0(self):
        expected = 2.0 * math.pi * 141.7001
        self.assertAlmostEqual(self.c.omega0(), expected, places=3)

    def test_t0(self):
        expected = 1.0 / 141.7001
        self.assertAlmostEqual(self.c.t0(), expected, places=10)

    def test_e_apoptosis_positive(self):
        self.assertGreater(self.c.e_apoptosis(), 0)

    def test_f_mito(self):
        expected = 141.7001 * ((1 + math.sqrt(5)) / 2) ** 2
        self.assertAlmostEqual(self.c.f_mito(), expected, places=4)

    def test_es_valido_default(self):
        self.assertTrue(self.c.es_valido())

    def test_es_valido_bad_f0(self):
        c = ConstantesPhoenixOnco(f0=-1.0)
        self.assertFalse(c.es_valido())


# ============================================================================
# TestApoptosisResonante – 16 tests
# ============================================================================

class TestApoptosisResonante(unittest.TestCase):
    """Tests para ApoptosisResonante."""

    def setUp(self):
        self.apo = ApoptosisResonante()

    def test_f0_default(self):
        self.assertAlmostEqual(self.apo.f0, 141.7001, places=4)

    def test_gammas_count(self):
        self.assertEqual(len(self.apo.gammas), 10)

    def test_f_armonicos_count(self):
        self.assertEqual(len(self.apo._f_armonicos), 10)

    def test_f_armonicos_first_equals_f0(self):
        self.assertAlmostEqual(self.apo._f_armonicos[0], _F0, places=4)

    def test_f_armonicos_ascending(self):
        for i in range(len(self.apo._f_armonicos) - 1):
            self.assertLess(self.apo._f_armonicos[i], self.apo._f_armonicos[i + 1])

    def test_amplitud_modo_t0(self):
        # En t=0: A_n(0) = exp(0) × cos(0) = 1.0
        a = self.apo.amplitud_modo(0, 0.0)
        self.assertAlmostEqual(a, 1.0, places=10)

    def test_amplitud_modo_decays(self):
        # Para t > 0 con amortiguamiento, la amplitud disminuye
        a0 = abs(self.apo.amplitud_modo(0, 0.0))
        a1 = abs(self.apo.amplitud_modo(0, 1.0))
        self.assertLessEqual(a1, a0)

    def test_amplitud_total_at_t0(self):
        total = self.apo.amplitud_total(0.0)
        # En t=0, todos los cosenos = 1, suma = 10
        self.assertAlmostEqual(total, 10.0, places=8)

    def test_energia_apoptotica_at_t0(self):
        # E = mean(A_n(0)²) = mean(1²) = 1.0
        e = self.apo.energia_apoptotica()
        self.assertAlmostEqual(e, 1.0, places=8)

    def test_psi_apoptosis_range(self):
        psi = self.apo.psi_apoptosis()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_apoptosis_threshold(self):
        psi = self.apo.psi_apoptosis()
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_amortiguamiento_default(self):
        self.assertAlmostEqual(self.apo.amortiguamiento, 0.05, places=4)

    def test_custom_f0(self):
        apo = ApoptosisResonante(f0=200.0)
        self.assertAlmostEqual(apo.f0, 200.0, places=4)
        self.assertAlmostEqual(apo._f_armonicos[0], 200.0, places=4)

    def test_all_amplitudes_t0_equals_one(self):
        for n in range(len(self.apo.gammas)):
            self.assertAlmostEqual(self.apo.amplitud_modo(n, 0.0), 1.0, places=8)

    def test_psi_apoptosis_small_damping(self):
        apo = ApoptosisResonante(amortiguamiento=0.01)
        psi = apo.psi_apoptosis()
        self.assertGreaterEqual(psi, 0.0)

    def test_psi_apoptosis_larger_damping(self):
        apo1 = ApoptosisResonante(amortiguamiento=0.01)
        apo2 = ApoptosisResonante(amortiguamiento=0.10)
        # Menor amortiguamiento → mayor psi
        self.assertGreaterEqual(apo1.psi_apoptosis(), apo2.psi_apoptosis())


# ============================================================================
# TestCicloPhoenix – 18 tests
# ============================================================================

class TestCicloPhoenix(unittest.TestCase):
    """Tests para CicloPhoenix."""

    def setUp(self):
        self.phoenix = CicloPhoenix()

    def test_f0_default(self):
        self.assertAlmostEqual(self.phoenix.f0, 141.7001, places=4)

    def test_theta_rad_default(self):
        self.assertAlmostEqual(self.phoenix.theta_rad, _THETA_PHOENIX_RAD, places=8)

    def test_n_ciclos_default(self):
        self.assertEqual(self.phoenix.n_ciclos, 10)

    def test_fase_acumulada_positive(self):
        self.assertGreater(self.phoenix.fase_acumulada(), 0)

    def test_fase_acumulada_formula(self):
        expected = 10 * 4.0 * math.pi * math.sin(_THETA_PHOENIX_RAD)
        self.assertAlmostEqual(self.phoenix.fase_acumulada(), expected, places=8)

    def test_coherencia_ciclo_range(self):
        c = self.phoenix.coherencia_ciclo()
        self.assertGreaterEqual(c, 0.0)
        self.assertLessEqual(c, 1.0)

    def test_psi_phoenix_range(self):
        psi = self.phoenix.psi_phoenix()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_phoenix_formula(self):
        c = self.phoenix.coherencia_ciclo()
        expected = (1.0 + c) / 2.0
        self.assertAlmostEqual(self.phoenix.psi_phoenix(), expected, places=10)

    def test_psi_phoenix_threshold(self):
        psi = self.phoenix.psi_phoenix()
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_completado(self):
        self.assertTrue(self.phoenix.completado())

    def test_custom_n_ciclos(self):
        p1 = CicloPhoenix(n_ciclos=1)
        p10 = CicloPhoenix(n_ciclos=10)
        # Más ciclos → fase diferente (no necesariamente monotona)
        self.assertNotAlmostEqual(p1.fase_acumulada(), p10.fase_acumulada(), places=3)

    def test_zero_ciclos(self):
        p = CicloPhoenix(n_ciclos=0)
        self.assertAlmostEqual(p.fase_acumulada(), 0.0, places=10)

    def test_coherencia_ciclo_with_zero_theta(self):
        p = CicloPhoenix(theta_rad=0.0)
        # sin(0) = 0, fase = 0, cos(0/(4π)) = 1, sin_theta = 0
        self.assertAlmostEqual(p.coherencia_ciclo(), 1.0, places=8)

    def test_psi_phoenix_with_zero_theta(self):
        p = CicloPhoenix(theta_rad=0.0)
        self.assertAlmostEqual(p.psi_phoenix(), 1.0, places=8)

    def test_theta_deg_in_radians(self):
        expected_rad = 3.00052 * math.pi / 180.0
        self.assertAlmostEqual(_THETA_PHOENIX_RAD, expected_rad, places=8)

    def test_sin_theta_small(self):
        # sin(3°) ≈ 0.0524, should be small
        self.assertLess(abs(math.sin(_THETA_PHOENIX_RAD)), 0.1)

    def test_coherencia_ciclo_bounded_by_cos(self):
        c = self.phoenix.coherencia_ciclo()
        # bounded by (1 - |sin(theta)|) ≤ 1
        max_c = 1.0 - abs(math.sin(self.phoenix.theta_rad))
        self.assertLessEqual(c, max_c + 1e-10)

    def test_psi_phoenix_at_least_half(self):
        psi = self.phoenix.psi_phoenix()
        self.assertGreaterEqual(psi, 0.5)


# ============================================================================
# TestMatrizCoherenciaTumoral – 20 tests
# ============================================================================

class TestMatrizCoherenciaTumoral(unittest.TestCase):
    """Tests para MatrizCoherenciaTumoral."""

    def setUp(self):
        self.mat = MatrizCoherenciaTumoral()

    def test_n_modos_default(self):
        self.assertEqual(self.mat.n_modos, 7)

    def test_kappa_pi_default(self):
        self.assertAlmostEqual(self.mat.kappa_pi, _KAPPA_PI, places=4)

    def test_gammas_count(self):
        self.assertEqual(len(self.mat._gammas), 7)

    def test_primos_count(self):
        self.assertEqual(len(self.mat._primos), 7)

    def test_elemento_diagonal_decay_is_one(self):
        # Elemento diagonal: decay = exp(-|i-i|/κ_Π) = exp(0) = 1
        for i in range(self.mat.n_modos):
            cos_term = math.cos(self.mat._gammas[i] * math.log(self.mat._primos[i]) / (2 * math.pi))
            expected = cos_term * 1.0
            self.assertAlmostEqual(self.mat.elemento(i, i), expected, places=8)

    def test_elemento_off_diagonal_decays(self):
        # |M[0,1]| < |M[0,0]| expected due to decay factor
        # Actually: M[0,1] = cos(...) × exp(-1/κ_Π), so ratio = exp(-1/κ_Π)
        # (when both cos-terms are comparable magnitude)
        # Just verify the decay factor is applied
        decay_factor = math.exp(-1.0 / _KAPPA_PI)
        m00_cos = math.cos(_GAMMAS[0] * math.log(_PRIMOS[0]) / (2 * math.pi))
        m01_cos = math.cos(_GAMMAS[0] * math.log(_PRIMOS[1]) / (2 * math.pi))
        expected_m01 = m01_cos * decay_factor
        self.assertAlmostEqual(self.mat.elemento(0, 1), expected_m01, places=8)

    def test_elemento_symmetry(self):
        # The matrix is NOT symmetric in general (γᵢ ≠ γⱼ in cos term)
        # But |i-j| decay IS symmetric
        # Verify the decay part is symmetric
        for i in range(self.mat.n_modos):
            for j in range(self.mat.n_modos):
                decay_ij = math.exp(-abs(i - j) / self.mat.kappa_pi)
                decay_ji = math.exp(-abs(j - i) / self.mat.kappa_pi)
                self.assertAlmostEqual(decay_ij, decay_ji, places=10)

    def test_traza_finite(self):
        traza = self.mat.traza()
        self.assertTrue(math.isfinite(traza))

    def test_norma_frobenius_positive(self):
        nf = self.mat.norma_frobenius()
        self.assertGreater(nf, 0.0)

    def test_norma_frobenius_finite(self):
        nf = self.mat.norma_frobenius()
        self.assertTrue(math.isfinite(nf))

    def test_norma_frobenius_bounded(self):
        # Max norm: all elements = 1, n_modos × n_modos elements → sqrt(n_modos²) = n_modos
        nf = self.mat.norma_frobenius()
        max_norm = float(self.mat.n_modos)
        self.assertLessEqual(nf, max_norm + 1e-10)

    def test_psi_tumoral_range(self):
        psi = self.mat.psi_tumoral()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_tumoral_threshold(self):
        psi = self.mat.psi_tumoral()
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_psi_tumoral_formula(self):
        nf = self.mat.norma_frobenius()
        expected = 1.0 - math.exp(-nf)
        self.assertAlmostEqual(self.mat.psi_tumoral(), expected, places=10)

    def test_custom_n_modos(self):
        mat = MatrizCoherenciaTumoral(n_modos=5)
        self.assertEqual(mat.n_modos, 5)
        psi = mat.psi_tumoral()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_custom_kappa_pi(self):
        mat1 = MatrizCoherenciaTumoral(kappa_pi=1.0)
        mat2 = MatrizCoherenciaTumoral(kappa_pi=10.0)
        # Larger kappa_pi → slower decay → larger off-diagonal elements → larger norm
        self.assertGreaterEqual(mat2.norma_frobenius(), mat1.norma_frobenius())

    def test_diagonal_elements_bounded(self):
        for i in range(self.mat.n_modos):
            m = self.mat.elemento(i, i)
            self.assertLessEqual(abs(m), 1.0 + 1e-10)

    def test_off_diagonal_smaller_than_diagonal_magnitude(self):
        # Off-diagonal elements are multiplied by exp(-|i-j|/κ_Π) < 1
        for i in range(self.mat.n_modos):
            for j in range(self.mat.n_modos):
                if i != j:
                    decay = math.exp(-abs(i - j) / self.mat.kappa_pi)
                    self.assertLessEqual(decay, 1.0)

    def test_n_modos_primos_match(self):
        self.assertEqual(len(self.mat._gammas), self.mat.n_modos)
        self.assertEqual(len(self.mat._primos), self.mat.n_modos)

    def test_norma_frobenius_gt_sqrt_n(self):
        # Since |cos(...)| ≈ 0.5 on average and decay ≤ 1,
        # ||M||_F ≥ sqrt(n_modos × avg_diag²) > 0
        nf = self.mat.norma_frobenius()
        self.assertGreater(nf, 0.5)

    def test_elemento_range(self):
        for i in range(self.mat.n_modos):
            for j in range(self.mat.n_modos):
                m = self.mat.elemento(i, j)
                self.assertGreaterEqual(m, -1.0 - 1e-10)
                self.assertLessEqual(m, 1.0 + 1e-10)


# ============================================================================
# TestHamiltonianoCelularPOC – 16 tests
# ============================================================================

class TestHamiltonianoCelularPOC(unittest.TestCase):
    """Tests para HamiltonianoCelularPOC."""

    def setUp(self):
        self.ham = HamiltonianoCelularPOC()

    def test_f0_default(self):
        self.assertAlmostEqual(self.ham.f0, 141.7001, places=4)

    def test_phi_default(self):
        self.assertAlmostEqual(self.ham.phi, (1 + math.sqrt(5)) / 2, places=10)

    def test_kappa_pi_default(self):
        self.assertAlmostEqual(self.ham.kappa_pi, _KAPPA_PI, places=4)

    def test_omega0_derived(self):
        expected = 2.0 * math.pi * 141.7001
        self.assertAlmostEqual(self.ham._omega0, expected, places=3)

    def test_energia_cero_finite(self):
        e0 = self.ham.energia_cero()
        self.assertTrue(math.isfinite(e0))

    def test_energia_cero_negative_or_small(self):
        # E₀ = ℏω₀/2 − g²/(ℏω₀): ground state energy can be slightly below ℏω₀/2
        from qcal.constants import HBAR
        hbar_omega = HBAR * self.ham._omega0
        e0 = self.ham.energia_cero()
        # Should be < ℏω₀/2 (coupling lowers the ground state)
        self.assertLess(e0, hbar_omega / 2.0)

    def test_gap_energetico_positive(self):
        gap = self.ham.gap_energetico()
        self.assertGreater(gap, 0.0)

    def test_gap_energetico_less_than_hbar_omega(self):
        from qcal.constants import HBAR
        hbar_omega = HBAR * self.ham._omega0
        gap = self.ham.gap_energetico()
        self.assertLess(gap, hbar_omega)

    def test_psi_hamiltoniano_range(self):
        psi = self.ham.psi_hamiltoniano()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_hamiltoniano_threshold(self):
        psi = self.ham.psi_hamiltoniano()
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_psi_hamiltoniano_formula(self):
        from qcal.constants import HBAR
        hbar_omega = HBAR * self.ham._omega0
        g_onco = hbar_omega * self.ham.phi / (2.0 * math.pi * self.ham.kappa_pi)
        ratio = abs(g_onco / (hbar_omega / 2.0))
        psi_raw = 1.0 - ratio
        expected = (1.0 + psi_raw) / 2.0
        self.assertAlmostEqual(self.ham.psi_hamiltoniano(), min(max(expected, 0), 1), places=8)

    def test_weak_coupling_large_psi(self):
        # With large kappa_pi, coupling is weaker → psi closer to 1
        ham_strong = HamiltonianoCelularPOC(kappa_pi=0.5)
        ham_weak = HamiltonianoCelularPOC(kappa_pi=100.0)
        self.assertGreater(ham_weak.psi_hamiltoniano(), ham_strong.psi_hamiltoniano())

    def test_custom_f0(self):
        ham = HamiltonianoCelularPOC(f0=200.0)
        self.assertAlmostEqual(ham.f0, 200.0, places=4)

    def test_gap_is_real(self):
        gap = self.ham.gap_energetico()
        self.assertIsInstance(gap, float)

    def test_e0_is_real(self):
        e0 = self.ham.energia_cero()
        self.assertIsInstance(e0, float)

    def test_g_onco_small_compared_to_hbar_omega(self):
        # g_onco ≪ ℏω₀ (weak coupling regime)
        from qcal.constants import HBAR
        hbar_omega = HBAR * self.ham._omega0
        g_onco = hbar_omega * self.ham.phi / (2.0 * math.pi * self.ham.kappa_pi)
        self.assertLess(g_onco, hbar_omega)


# ============================================================================
# TestSuperradianciaMitocondrialPOC – 16 tests
# ============================================================================

class TestSuperradianciaMitocondrialPOC(unittest.TestCase):
    """Tests para SuperradianciaMitocondrialPOC."""

    def setUp(self):
        self.sr = SuperradianciaMitocondrialPOC()

    def test_f0_default(self):
        self.assertAlmostEqual(self.sr.f0, 141.7001, places=4)

    def test_phi_default(self):
        self.assertAlmostEqual(self.sr.phi, _PHI, places=8)

    def test_tau_mito_default(self):
        self.assertAlmostEqual(self.sr.tau_mito_s, 100e-15, places=25)

    def test_n_celulas_default(self):
        self.assertEqual(self.sr.n_celulas, 10)

    def test_f_mito_derived(self):
        expected = _F0 * _PHI ** 2
        self.assertAlmostEqual(self.sr._f_mito, expected, places=4)

    def test_tasa_espontanea_positive(self):
        self.assertGreater(self.sr.tasa_espontanea(), 0.0)

    def test_tasa_superradiante_positive(self):
        self.assertGreater(self.sr.tasa_superradiante(), 0.0)

    def test_tasa_superradiante_formula(self):
        expected = self.sr.tasa_espontanea() * self.sr.n_celulas ** 2
        self.assertAlmostEqual(self.sr.tasa_superradiante(), expected, places=3)

    def test_psi_mito_range(self):
        psi = self.sr.psi_mito()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_mito_threshold(self):
        psi = self.sr.psi_mito()
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_psi_mito_formula(self):
        t0 = 1.0 / self.sr.f0
        gamma_sr = self.sr.tasa_superradiante()
        x = self.sr.n_celulas * gamma_sr * t0
        expected = x / (1.0 + x)
        self.assertAlmostEqual(self.sr.psi_mito(), min(max(expected, 0), 1), places=6)

    def test_intensidad_superradiante(self):
        intensidad = self.sr.intensidad_superradiante()
        self.assertAlmostEqual(intensidad, float(self.sr.n_celulas), places=4)

    def test_more_celulas_higher_gamma_sr(self):
        sr5 = SuperradianciaMitocondrialPOC(n_celulas=5)
        sr10 = SuperradianciaMitocondrialPOC(n_celulas=10)
        self.assertGreater(sr10.tasa_superradiante(), sr5.tasa_superradiante())

    def test_custom_n_celulas(self):
        sr = SuperradianciaMitocondrialPOC(n_celulas=5)
        self.assertEqual(sr.n_celulas, 5)

    def test_tasa_espontanea_formula(self):
        expected = 1.0 / (4.0 * math.pi * self.sr.tau_mito_s * self.sr._f_mito)
        self.assertAlmostEqual(self.sr.tasa_espontanea(), expected, places=2)

    def test_psi_mito_approaches_one_large_n(self):
        sr = SuperradianciaMitocondrialPOC(n_celulas=1000)
        psi = sr.psi_mito()
        self.assertGreater(psi, 0.999)


# ============================================================================
# TestCoherenciaPhoenixOnco – 14 tests
# ============================================================================

class TestCoherenciaPhoenixOnco(unittest.TestCase):
    """Tests para CoherenciaPhoenixOnco."""

    def setUp(self):
        self.coh = CoherenciaPhoenixOnco()

    def test_psi_umbral_default(self):
        self.assertAlmostEqual(self.coh.psi_umbral, 0.888, places=3)

    def test_calcular_mean_of_five(self):
        psi = self.coh.calcular(0.9, 0.9, 0.9, 0.9, 0.9)
        self.assertAlmostEqual(psi, 0.9, places=10)

    def test_calcular_zeros(self):
        psi = self.coh.calcular(0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertAlmostEqual(psi, 0.0, places=10)

    def test_calcular_ones(self):
        psi = self.coh.calcular(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(psi, 1.0, places=10)

    def test_calcular_asymmetric(self):
        psi = self.coh.calcular(1.0, 0.8, 0.8, 0.8, 0.8)
        expected = (1.0 + 0.8 + 0.8 + 0.8 + 0.8) / 5.0
        self.assertAlmostEqual(psi, expected, places=10)

    def test_sello_activo_above_threshold(self):
        self.assertTrue(self.coh.sello_activo(0.9))
        self.assertTrue(self.coh.sello_activo(0.888))
        self.assertTrue(self.coh.sello_activo(1.0))

    def test_sello_activo_below_threshold(self):
        self.assertFalse(self.coh.sello_activo(0.887))
        self.assertFalse(self.coh.sello_activo(0.0))

    def test_sello_activo_exact_threshold(self):
        self.assertTrue(self.coh.sello_activo(0.888))

    def test_custom_threshold(self):
        coh = CoherenciaPhoenixOnco(psi_umbral=0.5)
        self.assertTrue(coh.sello_activo(0.6))
        self.assertFalse(coh.sello_activo(0.4))

    def test_calcular_positive(self):
        psi = self.coh.calcular(0.9, 0.95, 0.93, 0.99, 0.90)
        self.assertGreater(psi, 0.0)

    def test_calcular_formula(self):
        args = (0.90, 0.91, 0.94, 0.99, 0.90)
        expected = sum(args) / 5.0
        self.assertAlmostEqual(self.coh.calcular(*args), expected, places=10)

    def test_weighted_equal(self):
        # All weights are equal (20% each)
        psi1 = self.coh.calcular(1.0, 0.0, 0.5, 0.5, 0.5)
        psi2 = self.coh.calcular(0.5, 0.5, 0.5, 0.5, 0.5)
        # First: (1+0+0.5+0.5+0.5)/5 = 0.5; Second: 0.5 — equal
        self.assertAlmostEqual(psi1, psi2, places=10)

    def test_sello_threshold_boundary(self):
        self.assertFalse(self.coh.sello_activo(0.8879))
        self.assertTrue(self.coh.sello_activo(0.8880))

    def test_calcular_returns_float(self):
        psi = self.coh.calcular(0.9, 0.9, 0.9, 0.9, 0.9)
        self.assertIsInstance(psi, float)


# ============================================================================
# TestSistemaPhoenixOncoCoherente – 16 tests
# ============================================================================

class TestSistemaPhoenixOncoCoherente(unittest.TestCase):
    """Tests para SistemaPhoenixOncoCoherente."""

    def setUp(self):
        self.sistema = SistemaPhoenixOncoCoherente()
        self.resultado = self.sistema.activar()

    def test_sello_activo(self):
        self.assertTrue(self.resultado.sello_activo)

    def test_sello_string(self):
        self.assertEqual(self.resultado.sello, _SELLO)

    def test_psi_global_threshold(self):
        self.assertGreaterEqual(self.resultado.psi_global, _PSI_UMBRAL)

    def test_psi_global_range(self):
        self.assertGreaterEqual(self.resultado.psi_global, 0.0)
        self.assertLessEqual(self.resultado.psi_global, 1.0)

    def test_psi_apoptosis_range(self):
        self.assertGreaterEqual(self.resultado.psi_apoptosis, 0.0)
        self.assertLessEqual(self.resultado.psi_apoptosis, 1.0)

    def test_psi_phoenix_range(self):
        self.assertGreaterEqual(self.resultado.psi_phoenix, 0.0)
        self.assertLessEqual(self.resultado.psi_phoenix, 1.0)

    def test_psi_tumoral_range(self):
        self.assertGreaterEqual(self.resultado.psi_tumoral, 0.0)
        self.assertLessEqual(self.resultado.psi_tumoral, 1.0)

    def test_psi_mito_range(self):
        self.assertGreaterEqual(self.resultado.psi_mito, 0.0)
        self.assertLessEqual(self.resultado.psi_mito, 1.0)

    def test_psi_hamiltoniano_range(self):
        self.assertGreaterEqual(self.resultado.psi_hamiltoniano, 0.0)
        self.assertLessEqual(self.resultado.psi_hamiltoniano, 1.0)

    def test_f0_in_resultado(self):
        self.assertAlmostEqual(self.resultado.f0, 141.7001, places=4)

    def test_f_mito_in_resultado(self):
        self.assertAlmostEqual(self.resultado.f_mito, _F_MITO, places=4)

    def test_f_armonicos_count(self):
        self.assertEqual(len(self.resultado.f_armonicos), 10)

    def test_traza_tumoral_finite(self):
        self.assertTrue(math.isfinite(self.resultado.traza_tumoral))

    def test_intensidad_sr(self):
        self.assertAlmostEqual(self.resultado.intensidad_sr, 10.0, places=4)

    def test_energia_cero_finite(self):
        self.assertTrue(math.isfinite(self.resultado.energia_cero))

    def test_fase_phoenix_positive(self):
        self.assertGreater(self.resultado.fase_phoenix, 0.0)


# ============================================================================
# TestResultadoPhoenixOnco – 12 tests
# ============================================================================

class TestResultadoPhoenixOnco(unittest.TestCase):
    """Tests para ResultadoPhoenixOnco dataclass."""

    def test_default_sello_activo_false(self):
        r = ResultadoPhoenixOnco()
        self.assertFalse(r.sello_activo)

    def test_default_sello_string(self):
        r = ResultadoPhoenixOnco()
        self.assertEqual(r.sello, _SELLO)

    def test_default_psi_global_zero(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.psi_global, 0.0, places=10)

    def test_default_f0(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.f0, _F0, places=4)

    def test_default_f_mito(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.f_mito, _F_MITO, places=4)

    def test_default_f_armonicos(self):
        r = ResultadoPhoenixOnco()
        self.assertEqual(len(r.f_armonicos), 10)

    def test_custom_sello_activo(self):
        r = ResultadoPhoenixOnco(sello_activo=True, psi_global=0.95)
        self.assertTrue(r.sello_activo)
        self.assertAlmostEqual(r.psi_global, 0.95, places=4)

    def test_all_psi_fields_default_zero(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.psi_apoptosis, 0.0, places=10)
        self.assertAlmostEqual(r.psi_phoenix, 0.0, places=10)
        self.assertAlmostEqual(r.psi_tumoral, 0.0, places=10)
        self.assertAlmostEqual(r.psi_mito, 0.0, places=10)
        self.assertAlmostEqual(r.psi_hamiltoniano, 0.0, places=10)

    def test_f_armonicos_first_is_f0(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.f_armonicos[0], _F0, places=4)

    def test_default_traza_tumoral_zero(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.traza_tumoral, 0.0, places=10)

    def test_default_intensidad_sr_zero(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.intensidad_sr, 0.0, places=10)

    def test_default_fase_phoenix_zero(self):
        r = ResultadoPhoenixOnco()
        self.assertAlmostEqual(r.fase_phoenix, 0.0, places=10)


# ============================================================================
# TestAPIPublic – 18 tests
# ============================================================================

class TestAPIPublic(unittest.TestCase):
    """Tests para la API pública phoenix_onco_coherente_v10_activar()."""

    def setUp(self):
        self.r = phoenix_onco_coherente_v10_activar()

    def test_returns_dict(self):
        self.assertIsInstance(self.r, dict)

    def test_sello_activo_true(self):
        self.assertTrue(self.r["sello_activo"])

    def test_sello_string(self):
        self.assertEqual(self.r["sello"], "∴POC∞³")

    def test_psi_global_threshold(self):
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_psi_global_range(self):
        self.assertGreaterEqual(self.r["psi_global"], 0.0)
        self.assertLessEqual(self.r["psi_global"], 1.0)

    def test_f0_value(self):
        self.assertAlmostEqual(self.r["f0"], 141.7001, places=4)

    def test_f_mito_value(self):
        expected = 141.7001 * ((1 + math.sqrt(5)) / 2) ** 2
        self.assertAlmostEqual(self.r["f_mito"], expected, places=4)

    def test_f_armonicos_count(self):
        self.assertEqual(len(self.r["f_armonicos"]), 10)

    def test_f_armonicos_first_is_f0(self):
        self.assertAlmostEqual(self.r["f_armonicos"][0], 141.7001, places=4)

    def test_all_keys_present(self):
        expected_keys = {
            "sello_activo", "sello", "psi_global", "psi_apoptosis",
            "psi_phoenix", "psi_tumoral", "psi_mito", "psi_hamiltoniano",
            "f0", "f_mito", "f_armonicos", "traza_tumoral",
            "intensidad_sr", "energia_cero", "fase_phoenix",
        }
        self.assertEqual(set(self.r.keys()), expected_keys)

    def test_invalid_f0_raises(self):
        with self.assertRaises(ValueError):
            phoenix_onco_coherente_v10_activar(f0=-1.0)

    def test_invalid_n_ciclos_raises(self):
        with self.assertRaises(ValueError):
            phoenix_onco_coherente_v10_activar(n_ciclos=0)

    def test_invalid_n_celulas_raises(self):
        with self.assertRaises(ValueError):
            phoenix_onco_coherente_v10_activar(n_celulas=0)

    def test_custom_n_ciclos(self):
        r = phoenix_onco_coherente_v10_activar(n_ciclos=5)
        self.assertIsInstance(r["psi_global"], float)

    def test_custom_n_celulas(self):
        r = phoenix_onco_coherente_v10_activar(n_celulas=5)
        self.assertAlmostEqual(r["intensidad_sr"], 5.0, places=4)

    def test_intensidad_sr_equals_n_celulas(self):
        self.assertAlmostEqual(self.r["intensidad_sr"], 10.0, places=4)

    def test_fase_phoenix_positive(self):
        self.assertGreater(self.r["fase_phoenix"], 0.0)

    def test_energia_cero_finite(self):
        self.assertTrue(math.isfinite(self.r["energia_cero"]))


if __name__ == "__main__":
    unittest.main()
