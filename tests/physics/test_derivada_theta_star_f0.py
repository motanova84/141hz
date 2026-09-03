"""
Tests for physics.derivada_theta_star_f0 — Derivada ∂θ*/∂f₀ y veredicto de pliegue

Pruebas que cubren la API pública del módulo de derivación analítica:
  - prefactor_cinematico()
  - coeficiente_sensibilidad_logaritmica()
  - zeta_chi0_sobre_mpl2_critico()
  - derivar_theta_star_f0()
  - a_osc()
  - delta_phi_1()

Invariantes clave verificados (coinciden con la derivación analítica):
  - (4π H0 √Ω_r0)^0.5 ≈ 5.124e-10 s^-1/2
  - f0^0.5 ≈ 11.9038 s^-1/2
  - K ≈ 4.417e-9
  - ζχ0²/Mpl² crítico ≈ 2.39e10  (≥ 10^10, no perturbativo)
  - El veredicto declara el régimen perturbativo inviable por >10 órdenes
    de magnitud.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.derivada_theta_star_f0 import (
    F0_HZ,
    H0_SI,
    OMEGA_R0,
    LOG_DERIVATIVE_3SIGMA_THRESHOLD,
    prefactor_cinematico,
    coeficiente_sensibilidad_logaritmica,
    zeta_chi0_sobre_mpl2_critico,
    derivar_theta_star_f0,
    a_osc,
    delta_phi_1,
    ResultadoDerivadaThetaStar,
)


class TestPrefactorCinematico(unittest.TestCase):
    def test_valor_esperado(self):
        valor = prefactor_cinematico(H0_SI, OMEGA_R0)
        self.assertAlmostEqual(valor, 5.124e-10, delta=2e-13)

    def test_positivo(self):
        self.assertGreater(prefactor_cinematico(H0_SI, OMEGA_R0), 0.0)


class TestCoeficienteSensibilidad(unittest.TestCase):
    def test_valor_esperado(self):
        k = coeficiente_sensibilidad_logaritmica()
        self.assertAlmostEqual(k, 4.417e-9, delta=2e-12)

    def test_f0_mayor_reduce_k(self):
        k_base = coeficiente_sensibilidad_logaritmica(f0=F0_HZ)
        k_mayor = coeficiente_sensibilidad_logaritmica(f0=F0_HZ * 10)
        self.assertLess(k_mayor, k_base)


class TestZetaCritico(unittest.TestCase):
    def test_valor_esperado(self):
        zeta_c = zeta_chi0_sobre_mpl2_critico()
        self.assertAlmostEqual(zeta_c / 1e10, 2.39, delta=0.05)

    def test_no_perturbativo(self):
        # El acoplamiento requerido debe ser >> 1 (rompe la aproximación
        # perturbativa ζχ0²/Mpl² ≪ 1).
        self.assertGreater(zeta_chi0_sobre_mpl2_critico(), 1e9)


class TestDerivarThetaStarF0(unittest.TestCase):
    def setUp(self):
        self.resultado = derivar_theta_star_f0()

    def test_tipo_resultado(self):
        self.assertIsInstance(self.resultado, ResultadoDerivadaThetaStar)

    def test_ordenes_magnitud_insuficiente(self):
        # El texto original concluye "más de 10 órdenes de magnitud".
        self.assertGreaterEqual(self.resultado.ordenes_magnitud_insuficiente, 10.0)
        self.assertLess(self.resultado.ordenes_magnitud_insuficiente, 11.0)

    def test_veredicto_declara_inviabilidad(self):
        self.assertIn("INVIABLE", self.resultado.veredicto)

    def test_umbral_consistente(self):
        k = coeficiente_sensibilidad_logaritmica()
        esperado = LOG_DERIVATIVE_3SIGMA_THRESHOLD / k
        self.assertAlmostEqual(
            self.resultado.zeta_chi0_sobre_mpl2_critico, esperado, delta=1.0
        )


class TestAOscYDeltaPhi(unittest.TestCase):
    def test_a_osc_positivo_y_pequeno(self):
        valor = a_osc()
        self.assertGreater(valor, 0.0)
        # a_osc debe ser mucho menor que a* (recombinación, ≈9.17e-4)
        self.assertLess(valor, 9.174e-4)

    def test_delta_phi_1_escala_con_delta_f0(self):
        base = delta_phi_1(delta_f0=0.0012, q_hecke=1.0)
        doble = delta_phi_1(delta_f0=0.0024, q_hecke=1.0)
        self.assertAlmostEqual(doble, 2.0 * base, delta=1e-15)

    def test_delta_phi_1_escala_con_q_hecke(self):
        base = delta_phi_1(q_hecke=1.0)
        triple = delta_phi_1(q_hecke=3.0)
        self.assertAlmostEqual(triple, 3.0 * base, delta=1e-15)


if __name__ == "__main__":
    unittest.main()
