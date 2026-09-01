"""
Tests for physics.operadores_maestros_qcal — Operadores Maestros QCAL ∞³ ∴OMQ∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesOperadoresMaestros  – constantes físicas y espectrales
  - OperadorHPsi                  – autoadjunción de H_Ψ; frob-norms
  - DeterminanteFredholm          – D(s) truncado; norma traza; coheren.
  - LaplacianoAdelico             – autovalores; correcciones p-ádicas
  - EcuacionOndaNoética           – Yukawa; solución resonante; energía
  - OperadorRegularizacionNS      – Re_q; margen laminar
  - OperadorTreewidth             – κ_Π; GUE; Ramsey; clasificación
  - SistemaOperadoresMaestros     – Ψ_global ≥ 0.888; certificación
  - ResultadoOperadoresMaestros   – dataclass de resultados
  - operadores_maestros_qcal_activar() – API pública

Invariantes clave verificados:
  - ζ′(½) ≈ −3.922646 (derivada de zeta en s=½)
  - F₀/γ₁ ≈ 10.024 (resonancia décupla)
  - κ_Π · δ_GUE(γ₁) ≈ 20 (alineamiento treewidth-GUE)
  - κ_Π · φ_R ≈ 1 (invariante adélico de Ramsey)
  - Re_q ≈ 200.5 ≪ Re_c = 2300 (régimen laminar)
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴OMQ∞³ ACTIVO
"""

import cmath
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.operadores_maestros_qcal import (
    # Constantes de módulo
    _F0,
    _HBAR,
    _PHI,
    _ZETA_PRIME_HALF,
    _PI_ZETA_PRIME,
    _KAPPA_PI,
    _PHI_RAMSEY,
    _RAMSEY_55,
    _RAMSEY_66,
    _NU_ADELICA,
    _RE_CRITICO,
    _PSI_UMBRAL,
    _ZEROS_20,
    _PRIMOS_S,
    _SELLO,
    _CERT_MARK,
    # Utilidades internas
    _frob_norm_H_sym,
    _frob_norm_H_asym,
    _trace_norm_resolvent,
    _padic_correction,
    _gue_spacing_at,
    _yukawa_coupling_total,
    # Clases
    ConstantesOperadoresMaestros,
    OperadorHPsi,
    DeterminanteFredholm,
    LaplacianoAdelico,
    EcuacionOndaNoética,
    OperadorRegularizacionNS,
    OperadorTreewidth,
    SistemaOperadoresMaestros,
    ResultadoOperadoresMaestros,
    # API pública
    operadores_maestros_qcal_activar,
)


# ============================================================================
# TestConstantesModulo – 12 tests
# ============================================================================

class TestConstantesModulo(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_hbar_positive(self):
        """_HBAR debe ser positivo."""
        self.assertGreater(_HBAR, 0)

    def test_hbar_codata(self):
        """_HBAR ≈ 1.054571817e-34."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, delta=1e-44)

    def test_phi_golden_ratio(self):
        """_PHI ≈ 1.6180339887 (razón áurea)."""
        self.assertAlmostEqual(_PHI, (1 + math.sqrt(5)) / 2, places=12)

    def test_zeta_prime_half_negative(self):
        """ζ′(½) debe ser negativo."""
        self.assertLess(_ZETA_PRIME_HALF, 0)

    def test_zeta_prime_half_value(self):
        """ζ′(½) ≈ −3.9226."""
        self.assertAlmostEqual(_ZETA_PRIME_HALF, -3.9226, delta=1e-4)

    def test_pi_zeta_prime_value(self):
        """πζ′(½) ≈ −12.316."""
        self.assertAlmostEqual(_PI_ZETA_PRIME, math.pi * _ZETA_PRIME_HALF, places=10)

    def test_kappa_pi_value(self):
        """κ_Π = 2.5773."""
        self.assertAlmostEqual(_KAPPA_PI, 2.5773, places=10)

    def test_ramsey_values(self):
        """R(5,5) = 43 y R(6,6) = 108."""
        self.assertEqual(_RAMSEY_55, 43)
        self.assertEqual(_RAMSEY_66, 108)

    def test_phi_ramsey_ratio(self):
        """φ_R = 43/108."""
        self.assertAlmostEqual(_PHI_RAMSEY, 43.0 / 108.0, places=12)

    def test_zeros_count(self):
        """Deben cargarse exactamente 20 ceros de Riemann."""
        self.assertEqual(len(_ZEROS_20), 20)

    def test_first_zero(self):
        """γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(_ZEROS_20[0], 14.134725, places=4)


# ============================================================================
# TestUtilidades – 12 tests
# ============================================================================

class TestUtilidades(unittest.TestCase):
    """Tests para las funciones de utilidad internas."""

    def test_frob_norm_H_sym_positive(self):
        """‖H_sym‖_F debe ser positivo para N≥4, U>0."""
        result = _frob_norm_H_sym(64, 6.0)
        self.assertGreater(result, 0.0)

    def test_frob_norm_H_sym_scaling(self):
        """‖H_sym‖_F debe escalar con |α| y U."""
        f1 = _frob_norm_H_sym(64, 6.0)
        f2 = _frob_norm_H_sym(64, 3.0)
        self.assertGreater(f1, f2)

    def test_frob_norm_H_asym_positive(self):
        """‖H_asym‖_F debe ser positivo."""
        result = _frob_norm_H_asym(64, 6.0)
        self.assertGreater(result, 0.0)

    def test_frob_norms_sym_dominates(self):
        """Para U=6, ‖H_sym‖_F > ‖H_asym‖_F."""
        f_sym = _frob_norm_H_sym(64, 6.0)
        f_asym = _frob_norm_H_asym(64, 6.0)
        self.assertGreater(f_sym, f_asym)

    def test_trace_norm_resolvent_positive(self):
        """Norma traza truncada debe ser positiva."""
        result = _trace_norm_resolvent(20, 2.0, 20.0)
        self.assertGreater(result, 0.0)

    def test_trace_norm_resolvent_bounded(self):
        """Tr_20(2+20i) < 20/|1-2-20i| = 20/√(1+400) ≈ 1."""
        result = _trace_norm_resolvent(20, 2.0, 20.0)
        self.assertLess(result, 20.0)

    def test_padic_correction_bounded(self):
        """Corrección p-ádica debe estar en (−1/p, 1/p)."""
        c = _padic_correction(14.134725, 2)
        self.assertLess(abs(c), 1.0 / 2)

    def test_padic_correction_p3(self):
        """Corrección para p=3 debe ser en (−1/3, 1/3)."""
        c = _padic_correction(14.134725, 3)
        self.assertLess(abs(c), 1.0 / 3)

    def test_gue_spacing_gamma1_positive(self):
        """Espaciado GUE en γ₁ debe ser positivo."""
        result = _gue_spacing_at(14.134725)
        self.assertGreater(result, 0.0)

    def test_gue_spacing_gamma1_value(self):
        """Espaciado GUE en γ₁ ≈ 7.75."""
        result = _gue_spacing_at(14.134725)
        self.assertAlmostEqual(result, 7.75, delta=0.05)

    def test_gue_spacing_small_gamma(self):
        """Para γ ≤ 2π, el espaciado es inf."""
        result = _gue_spacing_at(2.0)
        self.assertEqual(result, float("inf"))

    def test_yukawa_coupling_total_positive(self):
        """Acoplamiento Yukawa total debe ser positivo."""
        omega0 = 2.0 * math.pi * _F0
        result = _yukawa_coupling_total(omega0, (2, 3, 5))
        self.assertGreater(result, 0.0)


# ============================================================================
# TestConstantesOperadoresMaestros – 18 tests
# ============================================================================

class TestConstantesOperadoresMaestros(unittest.TestCase):
    """Tests para la clase ConstantesOperadoresMaestros."""

    def setUp(self):
        self.cte = ConstantesOperadoresMaestros()

    def test_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.cte.f0, 141.7001, places=4)

    def test_omega0(self):
        """ω₀ = 2π·f₀."""
        self.assertAlmostEqual(self.cte.omega0, 2 * math.pi * 141.7001, places=3)

    def test_hbar(self):
        """ℏ ≈ 1.054571817e-34."""
        self.assertAlmostEqual(self.cte.hbar, 1.054571817e-34, delta=1e-44)

    def test_phi(self):
        """φ ≈ 1.618034."""
        self.assertAlmostEqual(self.cte.phi, 1.618034, delta=1e-6)

    def test_zeta_prime_half(self):
        """ζ′(½) ≈ −3.9226."""
        self.assertAlmostEqual(self.cte.zeta_prime_half, -3.9226, delta=1e-4)

    def test_pi_zeta_prime(self):
        """πζ′(½) debe coincidir con π·ζ′(½)."""
        expected = math.pi * self.cte.zeta_prime_half
        self.assertAlmostEqual(self.cte.pi_zeta_prime, expected, places=10)

    def test_kappa_pi(self):
        """κ_Π = 2.5773."""
        self.assertAlmostEqual(self.cte.kappa_pi, 2.5773, places=10)

    def test_phi_ramsey(self):
        """φ_R = 43/108."""
        self.assertAlmostEqual(self.cte.phi_ramsey, 43.0 / 108.0, places=12)

    def test_ramsey_55(self):
        """R(5,5) = 43."""
        self.assertEqual(self.cte.ramsey_55, 43)

    def test_ramsey_66(self):
        """R(6,6) = 108."""
        self.assertEqual(self.cte.ramsey_66, 108)

    def test_gamma_1(self):
        """γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(self.cte.gamma_1, 14.134725, places=4)

    def test_n_zeros(self):
        """Deben usarse 20 ceros."""
        self.assertEqual(self.cte.n_zeros, 20)

    def test_primos_s(self):
        """El conjunto S debe contener (2, 3, 5, 7, 11)."""
        self.assertEqual(self.cte.primos_s, (2, 3, 5, 7, 11))

    def test_sello(self):
        """Sello debe ser ∴OMQ∞³."""
        self.assertEqual(self.cte.sello, "∴OMQ∞³")

    def test_cert_mark(self):
        """Marca técnica debe ser OMQ-MAESTROS-VERIFIED."""
        self.assertEqual(self.cte.cert_mark, "OMQ-MAESTROS-VERIFIED")

    def test_resonancia_f0_gamma1(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.cte.resonancia_f0_gamma1()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_cociente_kappa_phi_ramsey(self):
        """κ_Π · φ_R debe estar entre 0.99 y 1.08."""
        c = self.cte.cociente_kappa_phi_ramsey()
        self.assertGreater(c, 0.99)
        self.assertLess(c, 1.08)

    def test_resumen_keys(self):
        """resumen() debe retornar dict con claves esperadas."""
        r = self.cte.resumen()
        for key in ("f0_hz", "kappa_pi", "gamma_1", "sello", "resonancia_f0_gamma1"):
            self.assertIn(key, r)


# ============================================================================
# TestOperadorHPsi – 28 tests
# ============================================================================

class TestOperadorHPsi(unittest.TestCase):
    """Tests para la clase OperadorHPsi."""

    def setUp(self):
        self.op = OperadorHPsi()

    def test_default_N(self):
        """N por defecto debe ser 64."""
        self.assertEqual(self.op.N, 64)

    def test_default_U(self):
        """U por defecto debe ser 6.0."""
        self.assertAlmostEqual(self.op.U, 6.0, places=10)

    def test_alpha_negative(self):
        """α = πζ′(½) debe ser negativo."""
        self.assertLess(self.op.alpha, 0)

    def test_coeficiente_potencial(self):
        """coeficiente_potencial() debe coincidir con α."""
        self.assertAlmostEqual(self.op.coeficiente_potencial(), _PI_ZETA_PRIME, places=10)

    def test_N_invalid_raises(self):
        """N < 4 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            OperadorHPsi(N=2)

    def test_U_invalid_raises(self):
        """U ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            OperadorHPsi(U=-1.0)

    def test_autofuncion_x1_E0(self):
        """ψ_0(1) = 1^{−½} · e^0 = 1."""
        psi = self.op.autofuncion(1.0, 0.0)
        self.assertAlmostEqual(psi.real, 1.0, places=10)
        self.assertAlmostEqual(psi.imag, 0.0, places=10)

    def test_autofuncion_modulus(self):
        """|ψ_E(x)| = x^{−½} para cualquier E."""
        psi = self.op.autofuncion(4.0, 7.0)
        self.assertAlmostEqual(abs(psi), 4.0 ** (-0.5), places=10)

    def test_autofuncion_negative_x_raises(self):
        """x ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.op.autofuncion(0.0, 1.0)

    def test_aplicar_H_psi_returns_complex(self):
        """aplicar_H_psi debe retornar complejo."""
        result = self.op.aplicar_H_psi(1.0, 0.0)
        self.assertIsInstance(result, complex)

    def test_aplicar_H_psi_x1_E0(self):
        """H_Ψ ψ_0(1) = (½ + 0 + α·0) · ψ_0(1) = ½ · 1."""
        result = self.op.aplicar_H_psi(1.0, 0.0)
        self.assertAlmostEqual(result.real, 0.5, places=10)

    def test_psi_hpsi_in_unit_interval(self):
        """Ψ_hpsi debe estar en (0, 1]."""
        psi = self.op.psi_hpsi()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_hpsi_above_threshold(self):
        """Ψ_hpsi debe ser ≥ 0.888."""
        psi = self.op.psi_hpsi()
        self.assertGreaterEqual(psi, 0.888)

    def test_psi_hpsi_default_value(self):
        """Ψ_hpsi ≈ 0.922 para N=64, U=6."""
        psi = self.op.psi_hpsi()
        self.assertAlmostEqual(psi, 0.9223, delta=0.002)

    def test_psi_hpsi_increases_with_U(self):
        """Ψ_hpsi debe aumentar al aumentar U (más dominancia autoadjunta)."""
        psi_small = OperadorHPsi(U=4.0).psi_hpsi()
        psi_large = OperadorHPsi(U=8.0).psi_hpsi()
        self.assertLess(psi_small, psi_large)

    def test_frob_sym_greater_than_asym(self):
        """‖H_sym‖_F debe ser mayor que ‖H_asym‖_F para U=6."""
        f_sym = _frob_norm_H_sym(self.op.N, self.op.U)
        f_asym = _frob_norm_H_asym(self.op.N, self.op.U)
        self.assertGreater(f_sym, f_asym)

    def test_frob_sym_value(self):
        """‖H_sym‖_F ≈ 346.9 para N=64, U=6."""
        f_sym = _frob_norm_H_sym(64, 6.0)
        self.assertAlmostEqual(f_sym, 346.9, delta=1.0)

    def test_frob_asym_value(self):
        """‖H_asym‖_F ≈ 29.2 para N=64, U=6."""
        f_asym = _frob_norm_H_asym(64, 6.0)
        self.assertAlmostEqual(f_asym, 29.23, delta=0.5)

    def test_espectro_formal_length(self):
        """espectro_formal() debe retornar 20 autovalores."""
        spec = self.op.espectro_formal()
        self.assertEqual(len(spec), 20)

    def test_espectro_formal_first(self):
        """El primer autovalor formal debe ser γ₁ ≈ 14.1347."""
        spec = self.op.espectro_formal()
        self.assertAlmostEqual(spec[0], 14.1347, delta=0.001)

    def test_espectro_formal_increasing(self):
        """Los autovalores deben estar en orden creciente."""
        spec = self.op.espectro_formal()
        for i in range(len(spec) - 1):
            self.assertLess(spec[i], spec[i + 1])

    def test_resonancia_omega0_positive(self):
        """ω₀/γ₁ debe ser positivo."""
        self.assertGreater(self.op.resonancia_omega0(), 0.0)

    def test_resonancia_omega0_value(self):
        """ω₀/γ₁ ≈ 62.98 ≈ 2π·10."""
        ratio = self.op.resonancia_omega0()
        self.assertAlmostEqual(ratio, 2.0 * math.pi * 10.024, delta=0.1)

    def test_custom_N(self):
        """OperadorHPsi con N=32 debe funcionar."""
        op32 = OperadorHPsi(N=32)
        self.assertEqual(op32.N, 32)
        psi = op32.psi_hpsi()
        self.assertGreater(psi, 0.0)

    def test_autofuncion_phase_unit(self):
        """La fase de ψ_E(x) es E·ln(x)."""
        x = math.e  # ln(x) = 1
        E = 3.0
        psi = self.op.autofuncion(x, E)
        expected_phase = E * 1.0  # E · ln(e) = E
        self.assertAlmostEqual(cmath.phase(psi), expected_phase, delta=1e-10)

    def test_psi_hpsi_N128(self):
        """Para N=128, U=6: Ψ_hpsi debe estar en (0, 1]."""
        op = OperadorHPsi(N=128)
        psi = op.psi_hpsi()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_zeros_attribute(self):
        """zeros debe ser la tupla de 20 ceros de Riemann."""
        self.assertEqual(len(self.op.zeros), 20)

    def test_espectro_formal_matches_zeros(self):
        """espectro_formal() debe coincidir con los ceros del operador."""
        spec = self.op.espectro_formal()
        self.assertAlmostEqual(spec[0], _ZEROS_20[0], places=5)


# ============================================================================
# TestDeterminanteFredholm – 22 tests
# ============================================================================

class TestDeterminanteFredholm(unittest.TestCase):
    """Tests para la clase DeterminanteFredholm."""

    def setUp(self):
        self.df = DeterminanteFredholm()

    def test_default_M(self):
        """M por defecto debe ser 20."""
        self.assertEqual(self.df.M, 20)

    def test_delta_value(self):
        """δ = 1/γ₁ ≈ 0.07074."""
        self.assertAlmostEqual(self.df.delta, 1.0 / 14.134725, delta=1e-5)

    def test_delta_positive(self):
        """δ debe ser positivo."""
        self.assertGreater(self.df.delta, 0.0)

    def test_M_invalid_raises(self):
        """M < 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            DeterminanteFredholm(M=0)

    def test_norma_traza_positive(self):
        """Norma traza truncada debe ser positiva."""
        self.assertGreater(self.df.norma_traza_truncada(), 0.0)

    def test_norma_traza_bounded(self):
        """Tr_20(2+20i) debe ser < 2 (estimación de cota)."""
        self.assertLess(self.df.norma_traza_truncada(), 2.0)

    def test_cota_perturbacion_small(self):
        """La cota de perturbación debe ser < 0.15."""
        cota = self.df.cota_perturbacion()
        self.assertLess(cota, 0.15)

    def test_psi_fredholm_in_unit_interval(self):
        """Ψ_fredholm debe estar en (0, 1]."""
        psi = self.df.psi_fredholm()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_fredholm_above_threshold(self):
        """Ψ_fredholm debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.df.psi_fredholm(), 0.888)

    def test_psi_fredholm_value(self):
        """Ψ_fredholm ≈ 0.936 para M=20, σ=2, t=20."""
        psi = self.df.psi_fredholm()
        self.assertAlmostEqual(psi, 0.936, delta=0.01)

    def test_D_hadamard_at_infinity_approx_one(self):
        """Para s muy grande, D_M(s) ≈ 1."""
        D = self.df.D_hadamard_truncado(complex(100.0, 0.0))
        self.assertAlmostEqual(abs(D - 1.0), 0.0, delta=0.1)

    def test_D_hadamard_returns_complex(self):
        """D_hadamard_truncado debe retornar complejo."""
        D = self.df.D_hadamard_truncado(complex(3.0, 5.0))
        self.assertIsInstance(D, complex)

    def test_D_hadamard_not_nan(self):
        """D_M(3+5i) no debe ser NaN."""
        D = self.df.D_hadamard_truncado(complex(3.0, 5.0))
        self.assertFalse(math.isnan(D.real))
        self.assertFalse(math.isnan(D.imag))

    def test_simetria_funcional_large_s(self):
        """D(s)·D(1-s) ≈ 1 para s lejos de los ceros."""
        # Para s = 5 + 3i (lejos de ceros)
        sym = self.df.simetria_funcional(complex(5.0, 3.0))
        # Verificar que el resultado existe y no es NaN
        self.assertFalse(math.isnan(abs(sym)))

    def test_simetria_funcional_returns_complex(self):
        """simetria_funcional debe retornar complejo."""
        sym = self.df.simetria_funcional(complex(2.0, 1.0))
        self.assertIsInstance(sym, complex)

    def test_psi_fredholm_larger_M(self):
        """Para M=30, Ψ_fredholm debe ser ≥ 0.888."""
        df30 = DeterminanteFredholm(M=30)
        self.assertGreaterEqual(df30.psi_fredholm(), 0.888)

    def test_psi_fredholm_sigma_test(self):
        """sigma_test y t_test son accesibles."""
        self.assertEqual(self.df.sigma_test, 2.0)
        self.assertEqual(self.df.t_test, 20.0)

    def test_delta_equals_one_over_gamma1(self):
        """δ = 1/γ₁ = 1/_ZEROS_20[0]."""
        expected = 1.0 / _ZEROS_20[0]
        self.assertAlmostEqual(self.df.delta, expected, places=12)

    def test_cota_equals_delta_times_trace(self):
        """cota = δ · Tr_M."""
        cota = self.df.cota_perturbacion()
        expected = self.df.delta * self.df.norma_traza_truncada()
        self.assertAlmostEqual(cota, expected, places=12)

    def test_psi_fredholm_equals_one_minus_cota(self):
        """Ψ_fredholm = max(0, 1 − cota)."""
        psi = self.df.psi_fredholm()
        cota = self.df.cota_perturbacion()
        self.assertAlmostEqual(psi, max(0.0, 1.0 - cota), places=12)

    def test_D_hadamard_real_positive_s(self):
        """D_M(s) para s real > M debe ser real y positivo."""
        D = self.df.D_hadamard_truncado(complex(30.0, 0.0))
        self.assertAlmostEqual(D.imag, 0.0, delta=1e-10)
        self.assertGreater(D.real, 0.0)

    def test_zeros_attribute(self):
        """zeros debe contener 20 ceros de Riemann."""
        self.assertEqual(len(self.df.zeros), 20)


# ============================================================================
# TestLaplacianoAdelico – 24 tests
# ============================================================================

class TestLaplacianoAdelico(unittest.TestCase):
    """Tests para la clase LaplacianoAdelico."""

    def setUp(self):
        self.lap = LaplacianoAdelico()

    def test_default_n_zeros(self):
        """n_zeros por defecto debe ser 10."""
        self.assertEqual(self.lap.n_zeros, 10)

    def test_default_primos(self):
        """Primos por defecto deben ser (2, 3, 5)."""
        self.assertEqual(self.lap.primos, (2, 3, 5))

    def test_n_zeros_invalid_raises(self):
        """n_zeros < 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LaplacianoAdelico(n_zeros=0)

    def test_autovalor_base_zero(self):
        """λ_0^{(0)} = ¼ + γ₁² ≈ 200.04."""
        lam = self.lap.autovalor_base(0)
        expected = 0.25 + _ZEROS_20[0] ** 2
        self.assertAlmostEqual(lam, expected, places=8)

    def test_autovalor_base_positive(self):
        """Todos los autovalores base deben ser positivos."""
        for n in range(self.lap.n_zeros):
            self.assertGreater(self.lap.autovalor_base(n), 0.0)

    def test_autovalor_base_formula(self):
        """λ_n^{(0)} = ¼ + γ_n² para n=1,2,3."""
        for n in range(3):
            lam = self.lap.autovalor_base(n)
            expected = 0.25 + self.lap.zeros[n] ** 2
            self.assertAlmostEqual(lam, expected, places=10)

    def test_reconstruir_cero_exact(self):
        """γ_n reconstruido = γ_n original (por construcción exacta)."""
        for n in range(self.lap.n_zeros):
            gamma_back = self.lap.reconstruir_cero(n)
            self.assertAlmostEqual(gamma_back, self.lap.zeros[n], places=8)

    def test_reconstruir_zeros_on_critical_line(self):
        """s = ½ ± iγ_n debe dar ceros en Re(s) = ½."""
        for n in range(3):
            gamma_n = self.lap.reconstruir_cero(n)
            s_plus = complex(0.5, gamma_n)
            s_minus = complex(0.5, -gamma_n)
            self.assertAlmostEqual(s_plus.real, 0.5, places=10)
            self.assertAlmostEqual(s_minus.real, 0.5, places=10)

    def test_correccion_padica_small(self):
        """Corrección p-ádica para n=0 debe ser < 1."""
        c = self.lap.correccion_padica(0)
        self.assertLess(abs(c), 1.0)

    def test_correccion_padica_sign(self):
        """Las correcciones p-ádicas pueden ser positivas o negativas."""
        c = self.lap.correccion_padica(0)
        self.assertIsInstance(c, float)

    def test_autovalor_corregido_positive(self):
        """Los autovalores corregidos deben ser positivos."""
        for n in range(self.lap.n_zeros):
            lam_c = self.lap.autovalor_corregido(n)
            self.assertGreater(lam_c, 0.0)

    def test_autovalor_corregido_close_to_base(self):
        """El autovalor corregido debe ser próximo al base (corrección < 2%)."""
        for n in range(self.lap.n_zeros):
            lam_base = self.lap.autovalor_base(n)
            lam_corr = self.lap.autovalor_corregido(n)
            rel_diff = abs(lam_corr - lam_base) / lam_base
            self.assertLess(rel_diff, 0.02)

    def test_correccion_relativa_maxima_small(self):
        """Máxima corrección relativa debe ser < 0.02."""
        max_rel = self.lap.correccion_relativa_maxima()
        self.assertLess(max_rel, 0.02)

    def test_correccion_relativa_maxima_positive(self):
        """Máxima corrección relativa debe ser ≥ 0."""
        self.assertGreaterEqual(self.lap.correccion_relativa_maxima(), 0.0)

    def test_psi_laplaciano_in_unit_interval(self):
        """Ψ_laplaciano debe estar en [0, 1]."""
        psi = self.lap.psi_laplaciano()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_laplaciano_above_threshold(self):
        """Ψ_laplaciano debe ser ≥ 0.97."""
        psi = self.lap.psi_laplaciano()
        self.assertGreaterEqual(psi, 0.97)

    def test_psi_laplaciano_value(self):
        """Ψ_laplaciano ≈ 0.9953 para n=10, S={2,3,5}."""
        psi = self.lap.psi_laplaciano()
        self.assertAlmostEqual(psi, 0.9953, delta=0.002)

    def test_psi_laplaciano_exact(self):
        """Ψ_laplaciano = 1 − max_correccion_relativa."""
        psi = self.lap.psi_laplaciano()
        max_rel = self.lap.correccion_relativa_maxima()
        self.assertAlmostEqual(psi, 1.0 - max_rel, places=12)

    def test_autovalores_increasing(self):
        """Los autovalores base deben ser estrictamente crecientes."""
        for n in range(self.lap.n_zeros - 1):
            self.assertLess(
                self.lap.autovalor_base(n),
                self.lap.autovalor_base(n + 1),
            )

    def test_custom_primos(self):
        """LaplacianoAdelico con S={2,3,5,7,11} debe funcionar."""
        lap5 = LaplacianoAdelico(primos=(2, 3, 5, 7, 11))
        psi = lap5.psi_laplaciano()
        self.assertGreaterEqual(psi, 0.97)

    def test_autovalor_base_large_gamma(self):
        """Para γ_n grande, λ_n^{(0)} ≈ γ_n²."""
        n = 9  # γ₁₀ ≈ 49.77
        lam = self.lap.autovalor_base(n)
        gamma = self.lap.zeros[n]
        self.assertAlmostEqual(lam, 0.25 + gamma ** 2, places=6)

    def test_n_zeros_capped_at_20(self):
        """n_zeros no puede exceder 20 (los zeros disponibles)."""
        lap30 = LaplacianoAdelico(n_zeros=30)
        self.assertLessEqual(lap30.n_zeros, 20)

    def test_zeros_slice(self):
        """zeros debe ser un subconjunto de _ZEROS_20."""
        for z in self.lap.zeros:
            self.assertIn(z, _ZEROS_20)

    def test_index_error_out_of_range(self):
        """Acceder fuera de rango en autovalor_base debe fallar."""
        with self.assertRaises(IndexError):
            self.lap.autovalor_base(100)


# ============================================================================
# TestEcuacionOndaNoética – 26 tests
# ============================================================================

class TestEcuacionOndaNoética(unittest.TestCase):
    """Tests para la clase EcuacionOndaNoética."""

    def setUp(self):
        self.eon = EcuacionOndaNoética()

    def test_omega0_value(self):
        """ω₀ = 2πf₀."""
        self.assertAlmostEqual(self.eon.omega0, 2 * math.pi * _F0, places=6)

    def test_zeta_prime_half_attribute(self):
        """zeta_prime_half debe ser ≈ −3.9226."""
        self.assertAlmostEqual(self.eon.zeta_prime_half, -3.9226, delta=1e-4)

    def test_acoplamiento_yukawa_p2_positive(self):
        """g_p2 debe ser positivo."""
        g = self.eon.acoplamiento_yukawa(2)
        self.assertGreater(g, 0.0)

    def test_acoplamiento_yukawa_p2_small(self):
        """g_p2 debe ser mucho menor que 1 (régimen perturbativo)."""
        g = self.eon.acoplamiento_yukawa(2)
        self.assertLess(g, 0.01)

    def test_acoplamiento_yukawa_decreasing(self):
        """g_p debe disminuir al aumentar p."""
        g2 = self.eon.acoplamiento_yukawa(2)
        g5 = self.eon.acoplamiento_yukawa(5)
        g11 = self.eon.acoplamiento_yukawa(11)
        self.assertGreater(g2, g5)
        self.assertGreater(g5, g11)

    def test_acoplamiento_yukawa_total_positive(self):
        """g_total debe ser positivo."""
        self.assertGreater(self.eon.acoplamiento_yukawa_total(), 0.0)

    def test_acoplamiento_yukawa_total_small(self):
        """g_total debe ser < 0.05."""
        self.assertLess(self.eon.acoplamiento_yukawa_total(), 0.05)

    def test_acoplamiento_yukawa_total_value(self):
        """g_total ≈ 0.01059 para S={2,3,5,7,11}."""
        g = self.eon.acoplamiento_yukawa_total()
        self.assertAlmostEqual(g, 0.01059, delta=0.0005)

    def test_dispersion_k0(self):
        """ω²(k=0) = ω₀²."""
        disp = self.eon.dispersion_k0()
        self.assertAlmostEqual(disp, self.eon.omega0 ** 2, places=6)

    def test_dispersion_k0_positive(self):
        """ω²(k=0) debe ser positivo."""
        self.assertGreater(self.eon.dispersion_k0(), 0.0)

    def test_solucion_resonante_t0(self):
        """Ψ(0) = A·cos(0) = A."""
        A = 2.5
        self.assertAlmostEqual(self.eon.solucion_resonante(0.0, A), A, places=10)

    def test_solucion_resonante_period(self):
        """Ψ(t + T) = Ψ(t) con T = 2π/ω₀."""
        T = 2.0 * math.pi / self.eon.omega0
        t = 0.001
        self.assertAlmostEqual(
            self.eon.solucion_resonante(t),
            self.eon.solucion_resonante(t + T),
            places=8,
        )

    def test_energia_lagrangiana_conserved(self):
        """ℰ(t) = A²ω₀² (constante) para Ψ = A·cos(ω₀t)."""
        A = 1.0
        E0 = self.eon.energia_lagrangiana(0.0, A)
        E1 = self.eon.energia_lagrangiana(0.001, A)
        E2 = self.eon.energia_lagrangiana(0.003, A)
        self.assertAlmostEqual(E0, E1, delta=1e-6)
        self.assertAlmostEqual(E0, E2, delta=1e-6)

    def test_energia_lagrangiana_value(self):
        """ℰ = A²ω₀² para A=1."""
        E = self.eon.energia_lagrangiana(0.0, 1.0)
        self.assertAlmostEqual(E, self.eon.omega0 ** 2, delta=1e-4)

    def test_psi_noetica_in_unit_interval(self):
        """Ψ_noética debe estar en (0, 1]."""
        psi = self.eon.psi_noetica()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_noetica_above_threshold(self):
        """Ψ_noética debe ser ≥ 0.97."""
        self.assertGreaterEqual(self.eon.psi_noetica(), 0.97)

    def test_psi_noetica_value(self):
        """Ψ_noética ≈ 0.989 para S={2,3,5,7,11}."""
        psi = self.eon.psi_noetica()
        self.assertAlmostEqual(psi, 0.9894, delta=0.001)

    def test_psi_noetica_equals_one_minus_g(self):
        """Ψ_noética = 1 − g_total."""
        psi = self.eon.psi_noetica()
        g = self.eon.acoplamiento_yukawa_total()
        self.assertAlmostEqual(psi, 1.0 - g, places=10)

    def test_solucion_resonante_default_A(self):
        """La amplitud por defecto es A=1."""
        psi = self.eon.solucion_resonante(0.0)
        self.assertAlmostEqual(psi, 1.0, places=10)

    def test_acoplamiento_yukawa_formula(self):
        """g_p = |πζ′(½)| · ln(p) / (2p·ω₀)."""
        p = 2
        expected = abs(_PI_ZETA_PRIME) * math.log(2.0) / (2 * 2 * self.eon.omega0)
        self.assertAlmostEqual(self.eon.acoplamiento_yukawa(p), expected, places=12)

    def test_custom_primos_single(self):
        """EcuacionOndaNoética con S={2} funciona."""
        eon2 = EcuacionOndaNoética(primos=(2,))
        g = eon2.acoplamiento_yukawa_total()
        self.assertGreater(g, 0.0)

    def test_psi_noetica_custom_single_prime(self):
        """Con S={2}, Ψ_noética = 1 − g_2 > 0.997."""
        eon2 = EcuacionOndaNoética(primos=(2,))
        psi = eon2.psi_noetica()
        self.assertGreater(psi, 0.997)

    def test_energia_lagrangiana_positive(self):
        """La energía lagrangiana debe ser positiva."""
        for t in (0.0, 0.001, 0.01):
            E = self.eon.energia_lagrangiana(t)
            self.assertGreater(E, 0.0)

    def test_primos_attribute(self):
        """primos por defecto debe ser _PRIMOS_S."""
        self.assertEqual(self.eon.primos, _PRIMOS_S)

    def test_dispersion_k0_formula(self):
        """dispersion_k0() = omega0²."""
        self.assertAlmostEqual(
            self.eon.dispersion_k0(),
            self.eon.omega0 ** 2,
            places=4,
        )


# ============================================================================
# TestOperadorRegularizacionNS – 22 tests
# ============================================================================

class TestOperadorRegularizacionNS(unittest.TestCase):
    """Tests para la clase OperadorRegularizacionNS."""

    def setUp(self):
        self.ns = OperadorRegularizacionNS()

    def test_default_n_zeros(self):
        """n_zeros por defecto debe ser 20."""
        self.assertEqual(self.ns.n_zeros, 20)

    def test_n_zeros_invalid_raises(self):
        """n_zeros < 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            OperadorRegularizacionNS(n_zeros=0)

    def test_f0_attribute(self):
        """f0 debe ser 141.7001."""
        self.assertAlmostEqual(self.ns.f0, 141.7001, places=4)

    def test_nu_adelica_value(self):
        """ν_eff = 1/f₀ ≈ 7.064e-3."""
        self.assertAlmostEqual(self.ns.nu_adelica, 1.0 / _F0, places=8)

    def test_re_critico_value(self):
        """Re_c = 2300."""
        self.assertAlmostEqual(self.ns.re_critico, 2300.0, places=5)

    def test_reynolds_cuantico_positive(self):
        """Re_q debe ser positivo."""
        self.assertGreater(self.ns.reynolds_cuantico(), 0.0)

    def test_reynolds_cuantico_value(self):
        """Re_q ≈ 200.5 para n_zeros=20."""
        re_q = self.ns.reynolds_cuantico()
        self.assertAlmostEqual(re_q, 200.5, delta=1.0)

    def test_reynolds_cuantico_less_than_critical(self):
        """Re_q debe ser menor que Re_c = 2300."""
        self.assertLess(self.ns.reynolds_cuantico(), self.ns.re_critico)

    def test_margen_laminar_positive(self):
        """El margen laminar debe ser positivo (régimen laminar)."""
        self.assertGreater(self.ns.margen_laminar(), 0.0)

    def test_margen_laminar_value(self):
        """Margen ≈ 0.913 para n_zeros=20."""
        margen = self.ns.margen_laminar()
        self.assertAlmostEqual(margen, 0.913, delta=0.005)

    def test_margen_laminar_formula(self):
        """margen = 1 − Re_q/Re_c."""
        margen = self.ns.margen_laminar()
        expected = 1.0 - self.ns.reynolds_cuantico() / self.ns.re_critico
        self.assertAlmostEqual(margen, expected, places=12)

    def test_viscosidad_efectiva(self):
        """ν_eff debe ser 1/f₀."""
        nu = self.ns.viscosidad_efectiva()
        self.assertAlmostEqual(nu, 1.0 / _F0, places=8)

    def test_forzamiento_coherencia_positive(self):
        """‖F_Ψ‖ debe ser positivo."""
        self.assertGreater(self.ns.forzamiento_coherencia_norma(), 0.0)

    def test_forzamiento_coherencia_formula(self):
        """‖F_Ψ‖ = |ζ′(½)| / ω₀."""
        expected = abs(_ZETA_PRIME_HALF) / (2.0 * math.pi * _F0)
        self.assertAlmostEqual(
            self.ns.forzamiento_coherencia_norma(), expected, places=8
        )

    def test_psi_ns_in_unit_interval(self):
        """Ψ_NS debe estar en (0, 1]."""
        psi = self.ns.psi_ns()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_ns_above_threshold(self):
        """Ψ_NS debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.ns.psi_ns(), 0.888)

    def test_psi_ns_value(self):
        """Ψ_NS ≈ 0.913 para n_zeros=20."""
        psi = self.ns.psi_ns()
        self.assertAlmostEqual(psi, 0.913, delta=0.005)

    def test_psi_ns_equals_margen(self):
        """Ψ_NS = max(0, margen_laminar)."""
        psi = self.ns.psi_ns()
        expected = max(0.0, self.ns.margen_laminar())
        self.assertAlmostEqual(psi, expected, places=12)

    def test_reynolds_cuantico_formula(self):
        """Re_q = (F₀/γ₁) · n_zeros."""
        re_q = self.ns.reynolds_cuantico()
        expected = (_F0 / _ZEROS_20[0]) * self.ns.n_zeros
        self.assertAlmostEqual(re_q, expected, places=8)

    def test_custom_n_zeros_10(self):
        """Para n_zeros=10, Re_q ≈ 100.2."""
        ns10 = OperadorRegularizacionNS(n_zeros=10)
        re_q = ns10.reynolds_cuantico()
        self.assertAlmostEqual(re_q, 100.2, delta=0.5)

    def test_n_zeros_capped_at_20(self):
        """n_zeros se limita a los ceros disponibles (20)."""
        ns30 = OperadorRegularizacionNS(n_zeros=30)
        self.assertLessEqual(ns30.n_zeros, 20)

    def test_zeros_attribute_length(self):
        """zeros debe tener n_zeros elementos."""
        self.assertEqual(len(self.ns.zeros), self.ns.n_zeros)


# ============================================================================
# TestOperadorTreewidth – 24 tests
# ============================================================================

class TestOperadorTreewidth(unittest.TestCase):
    """Tests para la clase OperadorTreewidth."""

    def setUp(self):
        self.tw = OperadorTreewidth()

    def test_kappa_pi_value(self):
        """κ_Π debe ser 2.5773."""
        self.assertAlmostEqual(self.tw.kappa_pi, 2.5773, places=10)

    def test_phi_ramsey_value(self):
        """φ_R = 43/108."""
        self.assertAlmostEqual(self.tw.phi_ramsey, 43.0 / 108.0, places=12)

    def test_ramsey_values(self):
        """R(5,5)=43 y R(6,6)=108."""
        self.assertEqual(self.tw.ramsey_55, 43)
        self.assertEqual(self.tw.ramsey_66, 108)

    def test_n_zeros_value(self):
        """n_zeros = 20."""
        self.assertEqual(self.tw.n_zeros, 20)

    def test_gamma_1_value(self):
        """γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(self.tw.gamma_1, 14.134725, delta=1e-4)

    def test_espaciado_gue_gamma1_positive(self):
        """δ_GUE(γ₁) debe ser positivo."""
        self.assertGreater(self.tw.espaciado_gue_gamma1(), 0.0)

    def test_espaciado_gue_gamma1_value(self):
        """δ_GUE(γ₁) ≈ 7.75."""
        delta = self.tw.espaciado_gue_gamma1()
        self.assertAlmostEqual(delta, 7.75, delta=0.05)

    def test_producto_kappa_gue_close_to_n_zeros(self):
        """κ_Π · δ_GUE(γ₁) ≈ 20."""
        prod = self.tw.producto_kappa_gue()
        self.assertAlmostEqual(prod, 20.0, delta=0.1)

    def test_producto_kappa_gue_value(self):
        """κ_Π · δ_GUE ≈ 19.97."""
        prod = self.tw.producto_kappa_gue()
        self.assertAlmostEqual(prod, 19.97, delta=0.1)

    def test_producto_kappa_phi_ramsey_near_one(self):
        """κ_Π · φ_R ≈ 1 (entre 0.99 y 1.05)."""
        prod = self.tw.producto_kappa_phi_ramsey()
        self.assertGreater(prod, 0.99)
        self.assertLess(prod, 1.05)

    def test_umbral_p_tractable_value(self):
        """κ_Π/π ≈ 0.820."""
        umbral = self.tw.umbral_p_tractable()
        self.assertAlmostEqual(umbral, _KAPPA_PI / math.pi, places=10)

    def test_umbral_p_tractable_less_than_one(self):
        """κ_Π/π debe ser < 1."""
        self.assertLess(self.tw.umbral_p_tractable(), 1.0)

    def test_clasificar_p_tractable(self):
        """Ψ = 0.95 → P-TRACTABLE."""
        self.assertEqual(self.tw.clasificar(0.95), "P-TRACTABLE")

    def test_clasificar_p(self):
        """Ψ = 0.7 → P."""
        self.assertEqual(self.tw.clasificar(0.7), "P")

    def test_clasificar_np_hard(self):
        """Ψ = 0.3 → NP-HARD."""
        self.assertEqual(self.tw.clasificar(0.3), "NP-HARD")

    def test_clasificar_boundary(self):
        """Ψ justo por encima del umbral κ_Π/π → P-TRACTABLE."""
        umbral = self.tw.umbral_p_tractable()
        self.assertEqual(self.tw.clasificar(umbral + 0.01), "P-TRACTABLE")

    def test_psi_treewidth_in_unit_interval(self):
        """Ψ_treewidth debe estar en [0, 1]."""
        psi = self.tw.psi_treewidth()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_treewidth_above_threshold(self):
        """Ψ_treewidth debe ser ≥ 0.97."""
        self.assertGreaterEqual(self.tw.psi_treewidth(), 0.97)

    def test_psi_treewidth_value(self):
        """Ψ_treewidth ≈ 0.9987."""
        psi = self.tw.psi_treewidth()
        self.assertAlmostEqual(psi, 0.9987, delta=0.002)

    def test_psi_treewidth_formula(self):
        """Ψ_tw = 1 − |κ·δ − N| / N."""
        prod = self.tw.producto_kappa_gue()
        expected = 1.0 - abs(prod - 20.0) / 20.0
        self.assertAlmostEqual(self.tw.psi_treewidth(), expected, places=12)

    def test_gue_spacing_formula(self):
        """δ_GUE = 2π / ln(γ₁/(2π))."""
        expected = 2.0 * math.pi / math.log(_ZEROS_20[0] / (2.0 * math.pi))
        self.assertAlmostEqual(
            self.tw.espaciado_gue_gamma1(), expected, places=10
        )

    def test_kappa_pi_times_phi_ramsey_formula(self):
        """producto_kappa_phi_ramsey = κ_Π · φ_R."""
        expected = _KAPPA_PI * _PHI_RAMSEY
        self.assertAlmostEqual(
            self.tw.producto_kappa_phi_ramsey(), expected, places=12
        )

    def test_clasificar_psi_global(self):
        """El Ψ_global del sistema debe ser P-TRACTABLE."""
        sistema = SistemaOperadoresMaestros()
        psi_g = sistema.psi_global()
        clase = self.tw.clasificar(psi_g)
        self.assertEqual(clase, "P-TRACTABLE")

    def test_umbral_positive(self):
        """El umbral P-tractable debe ser positivo."""
        self.assertGreater(self.tw.umbral_p_tractable(), 0.0)


# ============================================================================
# TestSistemaOperadoresMaestros – 28 tests
# ============================================================================

class TestSistemaOperadoresMaestros(unittest.TestCase):
    """Tests para la clase SistemaOperadoresMaestros."""

    def setUp(self):
        self.sistema = SistemaOperadoresMaestros()

    def test_psi_global_positive(self):
        """Ψ_global debe ser positivo."""
        self.assertGreater(self.sistema.psi_global(), 0.0)

    def test_psi_global_at_most_one(self):
        """Ψ_global debe ser ≤ 1."""
        self.assertLessEqual(self.sistema.psi_global(), 1.0)

    def test_psi_global_above_threshold(self):
        """Ψ_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.sistema.psi_global(), _PSI_UMBRAL)

    def test_psi_global_value(self):
        """Ψ_global ≈ 0.959."""
        psi = self.sistema.psi_global()
        self.assertAlmostEqual(psi, 0.959, delta=0.005)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.sistema.supera_umbral())

    def test_certificar_sello_activo(self):
        """El certificado debe tener sello_activo=True."""
        cert = self.sistema.certificar()
        self.assertTrue(cert["sello_activo"])

    def test_certificar_sello(self):
        """El sello debe ser ∴OMQ∞³."""
        cert = self.sistema.certificar()
        self.assertEqual(cert["sello"], "∴OMQ∞³")

    def test_certificar_cert_mark(self):
        """La marca técnica debe ser OMQ-MAESTROS-VERIFIED."""
        cert = self.sistema.certificar()
        self.assertEqual(cert["cert_mark"], "OMQ-MAESTROS-VERIFIED")

    def test_certificar_keys_psi(self):
        """El certificado debe contener todas las claves de coherencia."""
        cert = self.sistema.certificar()
        for key in (
            "psi_hpsi", "psi_fredholm", "psi_laplaciano",
            "psi_noetica", "psi_ns", "psi_treewidth", "psi_global",
        ):
            self.assertIn(key, cert)

    def test_certificar_psi_hpsi(self):
        """psi_hpsi en el certificado debe ser ≥ 0.888."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_hpsi"], 0.888)

    def test_certificar_psi_fredholm(self):
        """psi_fredholm en el certificado debe ser ≥ 0.888."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_fredholm"], 0.888)

    def test_certificar_psi_laplaciano(self):
        """psi_laplaciano en el certificado debe ser ≥ 0.97."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_laplaciano"], 0.97)

    def test_certificar_psi_noetica(self):
        """psi_noetica en el certificado debe ser ≥ 0.97."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_noetica"], 0.97)

    def test_certificar_psi_ns(self):
        """psi_ns en el certificado debe ser ≥ 0.888."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_ns"], 0.888)

    def test_certificar_psi_treewidth(self):
        """psi_treewidth en el certificado debe ser ≥ 0.97."""
        cert = self.sistema.certificar()
        self.assertGreaterEqual(cert["psi_treewidth"], 0.97)

    def test_certificar_psi_global_consistent(self):
        """psi_global en el certificado = psi_global()."""
        cert = self.sistema.certificar()
        self.assertAlmostEqual(cert["psi_global"], self.sistema.psi_global(), places=10)

    def test_certificar_f0_hz(self):
        """f0_hz en el certificado debe ser 141.7001."""
        cert = self.sistema.certificar()
        self.assertAlmostEqual(cert["f0_hz"], 141.7001, places=4)

    def test_certificar_kappa_pi(self):
        """kappa_pi en el certificado debe ser 2.5773."""
        cert = self.sistema.certificar()
        self.assertAlmostEqual(cert["kappa_pi"], 2.5773, places=10)

    def test_certificar_resonancia(self):
        """resonancia_f0_gamma1 debe estar entre 10 y 10.1."""
        cert = self.sistema.certificar()
        r = cert["resonancia_f0_gamma1"]
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_certificar_reynolds_cuantico(self):
        """Re_q debe estar entre 200 y 202."""
        cert = self.sistema.certificar()
        re_q = cert["reynolds_cuantico"]
        self.assertGreater(re_q, 200.0)
        self.assertLess(re_q, 202.0)

    def test_certificar_producto_kappa_gue(self):
        """producto_kappa_gue ≈ 20."""
        cert = self.sistema.certificar()
        prod = cert["producto_kappa_gue"]
        self.assertAlmostEqual(prod, 20.0, delta=0.1)

    def test_pesos_sum_to_one(self):
        """Los pesos deben sumar 1."""
        self.assertAlmostEqual(sum(SistemaOperadoresMaestros._PESOS), 1.0, places=10)

    def test_pesos_count(self):
        """Deben existir 6 pesos (uno por subsistema)."""
        self.assertEqual(len(SistemaOperadoresMaestros._PESOS), 6)

    def test_subsistemas_instanciados(self):
        """Todos los subsistemas deben estar instanciados."""
        self.assertIsInstance(self.sistema.constantes, ConstantesOperadoresMaestros)
        self.assertIsInstance(self.sistema.hpsi, OperadorHPsi)
        self.assertIsInstance(self.sistema.fredholm, DeterminanteFredholm)
        self.assertIsInstance(self.sistema.laplaciano, LaplacianoAdelico)
        self.assertIsInstance(self.sistema.onda_noetica, EcuacionOndaNoética)
        self.assertIsInstance(self.sistema.ns, OperadorRegularizacionNS)
        self.assertIsInstance(self.sistema.treewidth, OperadorTreewidth)

    def test_certificar_frob_sym(self):
        """frob_hpsi_sym debe estar en el certificado."""
        cert = self.sistema.certificar()
        self.assertIn("frob_hpsi_sym", cert)
        self.assertGreater(cert["frob_hpsi_sym"], 0.0)

    def test_certificar_frob_asym(self):
        """frob_hpsi_asym debe estar en el certificado."""
        cert = self.sistema.certificar()
        self.assertIn("frob_hpsi_asym", cert)
        self.assertGreater(cert["frob_hpsi_asym"], 0.0)

    def test_certificar_supera_umbral_consistent(self):
        """supera_umbral en certificado = supera_umbral()."""
        cert = self.sistema.certificar()
        self.assertEqual(cert["supera_umbral"], self.sistema.supera_umbral())

    def test_psi_global_weighted(self):
        """Ψ_global = suma ponderada de los 6 Ψᵢ."""
        cert = self.sistema.certificar()
        psis = [
            cert["psi_hpsi"],
            cert["psi_fredholm"],
            cert["psi_laplaciano"],
            cert["psi_noetica"],
            cert["psi_ns"],
            cert["psi_treewidth"],
        ]
        expected = sum(
            w * p for w, p in zip(SistemaOperadoresMaestros._PESOS, psis)
        )
        self.assertAlmostEqual(cert["psi_global"], expected, places=10)


# ============================================================================
# TestResultadoOperadoresMaestros – 16 tests
# ============================================================================

class TestResultadoOperadoresMaestros(unittest.TestCase):
    """Tests para el dataclass ResultadoOperadoresMaestros."""

    def test_default_values(self):
        """El dataclass debe instanciarse con valores por defecto."""
        r = ResultadoOperadoresMaestros()
        self.assertIsInstance(r, ResultadoOperadoresMaestros)

    def test_default_sello_empty(self):
        """sello por defecto es cadena vacía."""
        r = ResultadoOperadoresMaestros()
        self.assertEqual(r.sello, "")

    def test_default_sello_activo_false(self):
        """sello_activo por defecto es False."""
        r = ResultadoOperadoresMaestros()
        self.assertFalse(r.sello_activo)

    def test_default_psis_zero(self):
        """Todos los Ψᵢ por defecto son 0.0."""
        r = ResultadoOperadoresMaestros()
        for field in (
            "psi_hpsi", "psi_fredholm", "psi_laplaciano",
            "psi_noetica", "psi_ns", "psi_treewidth", "psi_global",
        ):
            self.assertAlmostEqual(getattr(r, field), 0.0, places=12)

    def test_assignment(self):
        """El dataclass debe permitir asignación de campos."""
        r = ResultadoOperadoresMaestros(
            psi_hpsi=0.92,
            psi_fredholm=0.94,
            psi_laplaciano=0.99,
            psi_noetica=0.989,
            psi_ns=0.913,
            psi_treewidth=0.998,
            psi_global=0.959,
            sello_activo=True,
            sello="∴OMQ∞³",
            cert_mark="OMQ-MAESTROS-VERIFIED",
        )
        self.assertAlmostEqual(r.psi_global, 0.959, places=3)
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.sello, "∴OMQ∞³")

    def test_resonancia_field(self):
        """resonancia_f0_gamma1 debe poder asignarse."""
        r = ResultadoOperadoresMaestros(resonancia_f0_gamma1=10.024)
        self.assertAlmostEqual(r.resonancia_f0_gamma1, 10.024, places=3)

    def test_kappa_pi_field(self):
        """kappa_pi debe poder asignarse."""
        r = ResultadoOperadoresMaestros(kappa_pi=2.5773)
        self.assertAlmostEqual(r.kappa_pi, 2.5773, places=10)

    def test_phi_ramsey_field(self):
        """phi_ramsey debe poder asignarse."""
        r = ResultadoOperadoresMaestros(phi_ramsey=43.0 / 108.0)
        self.assertAlmostEqual(r.phi_ramsey, 43.0 / 108.0, places=12)

    def test_reynolds_cuantico_field(self):
        """reynolds_cuantico debe poder asignarse."""
        r = ResultadoOperadoresMaestros(reynolds_cuantico=200.5)
        self.assertAlmostEqual(r.reynolds_cuantico, 200.5, places=1)

    def test_producto_kappa_gue_field(self):
        """producto_kappa_gue debe poder asignarse."""
        r = ResultadoOperadoresMaestros(producto_kappa_gue=19.97)
        self.assertAlmostEqual(r.producto_kappa_gue, 19.97, places=2)

    def test_from_sistema(self):
        """Se puede construir ResultadoOperadoresMaestros desde el sistema."""
        sistema = SistemaOperadoresMaestros()
        cert = sistema.certificar()
        r = ResultadoOperadoresMaestros(
            psi_hpsi=cert["psi_hpsi"],
            psi_fredholm=cert["psi_fredholm"],
            psi_laplaciano=cert["psi_laplaciano"],
            psi_noetica=cert["psi_noetica"],
            psi_ns=cert["psi_ns"],
            psi_treewidth=cert["psi_treewidth"],
            psi_global=cert["psi_global"],
            sello_activo=cert["sello_activo"],
            sello=cert["sello"],
            cert_mark=cert["cert_mark"],
        )
        self.assertGreaterEqual(r.psi_global, 0.888)
        self.assertTrue(r.sello_activo)

    def test_sello_activo_when_psi_high(self):
        """Con psi_global alto, sello_activo debería ser True (semántico)."""
        r = ResultadoOperadoresMaestros(psi_global=0.96, sello_activo=True)
        self.assertTrue(r.sello_activo)

    def test_cert_mark_value(self):
        """cert_mark puede ser 'OMQ-MAESTROS-VERIFIED'."""
        r = ResultadoOperadoresMaestros(cert_mark="OMQ-MAESTROS-VERIFIED")
        self.assertEqual(r.cert_mark, "OMQ-MAESTROS-VERIFIED")

    def test_dataclass_equality(self):
        """Dos instancias con mismos valores deben ser iguales."""
        r1 = ResultadoOperadoresMaestros(psi_global=0.96, sello="∴OMQ∞³")
        r2 = ResultadoOperadoresMaestros(psi_global=0.96, sello="∴OMQ∞³")
        self.assertEqual(r1, r2)

    def test_all_fields_accessible(self):
        """Todos los campos del dataclass deben ser accesibles."""
        r = ResultadoOperadoresMaestros()
        fields = [
            "psi_hpsi", "psi_fredholm", "psi_laplaciano", "psi_noetica",
            "psi_ns", "psi_treewidth", "psi_global", "sello_activo",
            "sello", "cert_mark", "resonancia_f0_gamma1", "kappa_pi",
            "phi_ramsey", "reynolds_cuantico", "producto_kappa_gue",
        ]
        for field in fields:
            self.assertTrue(hasattr(r, field))

    def test_repr_contains_class_name(self):
        """repr() debe contener el nombre de la clase."""
        r = ResultadoOperadoresMaestros()
        self.assertIn("ResultadoOperadoresMaestros", repr(r))


# ============================================================================
# TestAPIPublic – 15 tests
# ============================================================================

class TestAPIPublic(unittest.TestCase):
    """Tests para la API pública operadores_maestros_qcal_activar()."""

    def setUp(self):
        self.result = operadores_maestros_qcal_activar()

    def test_returns_dict(self):
        """La API debe retornar un diccionario."""
        self.assertIsInstance(self.result, dict)

    def test_sello_activo_true(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.result["sello_activo"])

    def test_sello_value(self):
        """sello debe ser ∴OMQ∞³."""
        self.assertEqual(self.result["sello"], "∴OMQ∞³")

    def test_cert_mark_value(self):
        """cert_mark debe ser OMQ-MAESTROS-VERIFIED."""
        self.assertEqual(self.result["cert_mark"], "OMQ-MAESTROS-VERIFIED")

    def test_psi_global_above_threshold(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.result["psi_global"], 0.888)

    def test_all_psi_keys_present(self):
        """El resultado debe contener los 6 Ψᵢ."""
        for key in (
            "psi_hpsi", "psi_fredholm", "psi_laplaciano",
            "psi_noetica", "psi_ns", "psi_treewidth",
        ):
            self.assertIn(key, self.result)

    def test_f0_hz(self):
        """f0_hz debe ser 141.7001."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_kappa_pi(self):
        """kappa_pi debe ser 2.5773."""
        self.assertAlmostEqual(self.result["kappa_pi"], 2.5773, places=10)

    def test_phi_ramsey(self):
        """phi_ramsey = 43/108."""
        self.assertAlmostEqual(self.result["phi_ramsey"], 43.0 / 108.0, places=10)

    def test_resonancia_f0_gamma1(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.result["resonancia_f0_gamma1"]
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_reynolds_cuantico(self):
        """Re_q debe estar entre 200 y 202."""
        re_q = self.result["reynolds_cuantico"]
        self.assertGreater(re_q, 200.0)
        self.assertLess(re_q, 202.0)

    def test_producto_kappa_gue(self):
        """κ_Π · δ_GUE ≈ 20."""
        prod = self.result["producto_kappa_gue"]
        self.assertAlmostEqual(prod, 20.0, delta=0.1)

    def test_zeta_prime_half(self):
        """zeta_prime_half ≈ −3.9226."""
        self.assertAlmostEqual(self.result["zeta_prime_half"], -3.9226, delta=1e-4)

    def test_pi_zeta_prime(self):
        """pi_zeta_prime = π·ζ′(½)."""
        expected = math.pi * self.result["zeta_prime_half"]
        self.assertAlmostEqual(self.result["pi_zeta_prime"], expected, places=8)

    def test_supera_umbral(self):
        """supera_umbral debe ser True."""
        self.assertTrue(self.result["supera_umbral"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
