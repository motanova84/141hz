#!/usr/bin/env python3
"""
Tests para la Ecuación Maestra de la Abundancia Coherente
==========================================================

Verifica el comportamiento de AbundanciaCoherente y las funciones
de la API pública definidas en qcal/abundancia_coherente.py.

ECUACIÓN MAESTRA:
    A = lim        ( I(t) · f₀ )  =  ∞
         Ψ→1.0   ─────────────────
                  |ζ'(1/2)| · eff

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: Marzo 2026
MARCO: QCAL ∞³
"""

import math
import unittest
from typing import List

from qcal.abundancia_coherente import (
    AbundanciaCoherente,
    ResultadoAbundancia,
    PerfilAbundancia,
    ABS_ZETA_PRIME_HALF,
    PSI_MAX,
    PSI_PLENA_COHERENCIA,
    abundancia,
    limite_abundancia_infinito,
)
from qcal.constants import F0_HZ


class TestConstantes(unittest.TestCase):
    """Verifica las constantes del módulo."""

    def test_abs_zeta_prime_positive(self):
        """
        |ζ'(1/2)| debe ser un número positivo.
        ζ'(1/2) ≈ −3.9226…, por lo que el valor absoluto es ≈ 3.9226.
        """
        self.assertGreater(ABS_ZETA_PRIME_HALF, 0.0)

    def test_abs_zeta_prime_known_value(self):
        """|ζ'(1/2)| debe coincidir con el valor precalculado ≈ 3.9226."""
        self.assertAlmostEqual(ABS_ZETA_PRIME_HALF, 3.9226, places=3)

    def test_psi_max_unity(self):
        """PSI_MAX debe ser exactamente 1.0."""
        self.assertEqual(PSI_MAX, 1.0)

    def test_psi_plena_coherencia_range(self):
        """PSI_PLENA_COHERENCIA debe estar en (0, 1)."""
        self.assertGreater(PSI_PLENA_COHERENCIA, 0.0)
        self.assertLess(PSI_PLENA_COHERENCIA, 1.0)

    def test_f0_hz_from_qcal_constants(self):
        """F0_HZ importado de qcal.constants debe ser 141.7001 Hz."""
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)


class TestAbundanciaCoherenteInit(unittest.TestCase):
    """Verifica la inicialización de AbundanciaCoherente."""

    def test_default_init(self):
        """La instancia por defecto usa F0_HZ y el valor precomputado."""
        sistema = AbundanciaCoherente(alta_precision=False)
        self.assertAlmostEqual(sistema.f0, F0_HZ, places=4)
        self.assertAlmostEqual(sistema.abs_zeta_prime, ABS_ZETA_PRIME_HALF, places=6)

    def test_custom_f0(self):
        """Se puede usar una frecuencia personalizada."""
        sistema = AbundanciaCoherente(f0=432.0, alta_precision=False)
        self.assertAlmostEqual(sistema.f0, 432.0, places=6)

    def test_invalid_f0_raises(self):
        """f0 ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AbundanciaCoherente(f0=0.0)
        with self.assertRaises(ValueError):
            AbundanciaCoherente(f0=-1.0)

    def test_alta_precision_compatible(self):
        """La instancia con alta_precision=True debe tener |ζ'(1/2)| consistente."""
        sistema = AbundanciaCoherente(alta_precision=True, precision_dps=30)
        self.assertAlmostEqual(sistema.abs_zeta_prime, ABS_ZETA_PRIME_HALF, places=3)


class TestEficiencia(unittest.TestCase):
    """Verifica eff(Ψ) = 1 − Ψ."""

    def test_eff_zero_psi(self):
        """Cuando Ψ = 0, eff = 1."""
        self.assertAlmostEqual(AbundanciaCoherente.eficiencia(0.0), 1.0)

    def test_eff_half(self):
        """Cuando Ψ = 0.5, eff = 0.5."""
        self.assertAlmostEqual(AbundanciaCoherente.eficiencia(0.5), 0.5)

    def test_eff_near_one(self):
        """Cuando Ψ → 1, eff → 0."""
        self.assertAlmostEqual(AbundanciaCoherente.eficiencia(0.999), 0.001, places=6)
        self.assertAlmostEqual(AbundanciaCoherente.eficiencia(0.9999), 0.0001, places=7)

    def test_eff_negative_psi_raises(self):
        """Ψ < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AbundanciaCoherente.eficiencia(-0.1)

    def test_eff_psi_one_raises(self):
        """Ψ = 1 debe lanzar ValueError (límite infinito)."""
        with self.assertRaises(ValueError):
            AbundanciaCoherente.eficiencia(1.0)

    def test_eff_psi_greater_than_one_raises(self):
        """Ψ > 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AbundanciaCoherente.eficiencia(1.5)


class TestIntensidadIntencion(unittest.TestCase):
    """Verifica I(t) = I₀·(1 + cos(2π·f₀·t))/2."""

    def setUp(self):
        self.sistema = AbundanciaCoherente(alta_precision=False)

    def test_I_at_t0_is_I0(self):
        """En t = 0, cos(0) = 1, por tanto I(0) = I₀."""
        I0 = 2.5
        self.assertAlmostEqual(self.sistema.intensidad_intencion(0.0, I0), I0, places=10)

    def test_I_at_half_period(self):
        """En t = T₀/2 = 1/(2·f₀), cos(π) = −1, por tanto I = 0."""
        T0 = 1.0 / self.sistema.f0
        resultado = self.sistema.intensidad_intencion(T0 / 2.0)
        self.assertAlmostEqual(resultado, 0.0, places=10)

    def test_I_at_full_period(self):
        """En t = T₀ = 1/f₀, cos(2π) = 1, por tanto I = I₀."""
        T0 = 1.0 / self.sistema.f0
        self.assertAlmostEqual(self.sistema.intensidad_intencion(T0), 1.0, places=10)

    def test_I_nonnegative(self):
        """I(t) debe ser siempre ≥ 0."""
        for k in range(20):
            t = k * 0.001
            self.assertGreaterEqual(self.sistema.intensidad_intencion(t), 0.0)

    def test_negative_I0_raises(self):
        """I0 < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.sistema.intensidad_intencion(0.0, I0=-1.0)


class TestCalcular(unittest.TestCase):
    """Verifica la ecuación maestra A = I(t)·f₀ / (|ζ'(1/2)|·eff)."""

    def setUp(self):
        self.sistema = AbundanciaCoherente(alta_precision=False)

    def test_resultado_type(self):
        """calcular() debe devolver un ResultadoAbundancia."""
        resultado = self.sistema.calcular(0.5)
        self.assertIsInstance(resultado, ResultadoAbundancia)

    def test_campos_resultado(self):
        """El resultado debe tener todos los campos poblados."""
        r = self.sistema.calcular(0.5, t=0.0, I0=1.0)
        self.assertEqual(r.psi, 0.5)
        self.assertEqual(r.t, 0.0)
        self.assertAlmostEqual(r.I_t, 1.0, places=10)  # t=0 → I=I0=1
        self.assertAlmostEqual(r.f0, F0_HZ, places=4)
        self.assertGreater(r.abs_zeta_prime, 0.0)
        self.assertAlmostEqual(r.eff, 0.5, places=10)
        self.assertGreater(r.abundancia, 0.0)
        self.assertFalse(r.limite_infinito)

    def test_formula_matematica(self):
        """
        A debe coincidir con I(t)·f₀ / (|ζ'(1/2)|·eff) evaluado manualmente.
        """
        psi = 0.6
        t = 0.0
        I0 = 1.0
        r = self.sistema.calcular(psi, t=t, I0=I0)

        # Cálculo manual
        I_t = I0  # t=0 → I = I0
        eff = 1.0 - psi
        esperado = I_t * F0_HZ / (ABS_ZETA_PRIME_HALF * eff)

        self.assertAlmostEqual(r.abundancia, esperado, places=6)

    def test_abundancia_increases_with_psi(self):
        """A debe aumentar monotónicamente con Ψ (para I(t) constante, t=0)."""
        psi_valores = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
        abundancias = [self.sistema.calcular(p).abundancia for p in psi_valores]
        for i in range(len(abundancias) - 1):
            self.assertLess(abundancias[i], abundancias[i + 1])

    def test_abundancia_positiva(self):
        """A debe ser siempre positiva cuando I(t) > 0."""
        for psi in [0.0, 0.25, 0.5, 0.75, 0.9]:
            r = self.sistema.calcular(psi, t=0.0, I0=1.0)
            self.assertGreater(r.abundancia, 0.0)

    def test_limite_infinito_flag(self):
        """limite_infinito debe ser True cuando Ψ ≥ PSI_PLENA_COHERENCIA."""
        r_alta = self.sistema.calcular(PSI_PLENA_COHERENCIA)
        self.assertTrue(r_alta.limite_infinito)

        r_baja = self.sistema.calcular(PSI_PLENA_COHERENCIA - 0.001)
        self.assertFalse(r_baja.limite_infinito)

    def test_psi_invalid_raises(self):
        """Ψ fuera de [0, 1) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.sistema.calcular(-0.1)
        with self.assertRaises(ValueError):
            self.sistema.calcular(1.0)

    def test_descripcion_not_empty(self):
        """La descripción del resultado no debe estar vacía."""
        r = self.sistema.calcular(0.5)
        self.assertIsInstance(r.descripcion, str)
        self.assertGreater(len(r.descripcion), 0)


class TestLimiteInfinito(unittest.TestCase):
    """Verifica que A → +∞ cuando Ψ → 1."""

    def setUp(self):
        self.sistema = AbundanciaCoherente(alta_precision=False)

    def test_abundancia_diverge_as_psi_approaches_one(self):
        """
        A medida que Ψ aumenta hacia 1, A debe divergir hacia +∞.
        Verificamos que A(0.9999) >> A(0.9) >> A(0.5).
        """
        A_medio = self.sistema.calcular(0.5).abundancia
        A_alto = self.sistema.calcular(0.9).abundancia
        A_muy_alto = self.sistema.calcular(0.9999).abundancia

        self.assertGreater(A_alto, A_medio * 5)
        self.assertGreater(A_muy_alto, A_alto * 100)

    def test_ratio_eff_inversely_proportional(self):
        """
        Duplicar eff (bajar Ψ) debe dividir A por 2.
        Si Ψ₁ = 0.5 → eff₁ = 0.5, y Ψ₂ = 0.0 → eff₂ = 1.0 = 2·eff₁,
        entonces A(Ψ₁) = 2 · A(Ψ₂).
        """
        A1 = self.sistema.calcular(0.5).abundancia  # eff = 0.5
        A2 = self.sistema.calcular(0.0).abundancia  # eff = 1.0
        self.assertAlmostEqual(A1 / A2, 2.0, places=10)


class TestPerfil(unittest.TestCase):
    """Verifica el método perfil()."""

    def setUp(self):
        self.sistema = AbundanciaCoherente(alta_precision=False)

    def test_perfil_type(self):
        """perfil() debe devolver un PerfilAbundancia."""
        p = self.sistema.perfil(n_puntos=10)
        self.assertIsInstance(p, PerfilAbundancia)

    def test_perfil_longitud(self):
        """El perfil debe tener n_puntos valores."""
        n = 20
        p = self.sistema.perfil(n_puntos=n)
        self.assertEqual(len(p.psi_valores), n)
        self.assertEqual(len(p.abundancias), n)

    def test_perfil_monotono(self):
        """Las abundancias en el perfil deben ser monótonamente crecientes."""
        p = self.sistema.perfil(n_puntos=10)
        for i in range(len(p.abundancias) - 1):
            self.assertLessEqual(p.abundancias[i], p.abundancias[i + 1])

    def test_perfil_psi_critico(self):
        """psi_critico debe ser el primer valor donde A ≥ umbral."""
        umbral = 500.0
        p = self.sistema.perfil(n_puntos=50, umbral_abundancia=umbral)
        if p.psi_critico is not None:
            idx = p.psi_valores.index(p.psi_critico)
            self.assertGreaterEqual(p.abundancias[idx], umbral)

    def test_perfil_invalid_params(self):
        """Parámetros inválidos deben lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.sistema.perfil(psi_min=-0.1)
        with self.assertRaises(ValueError):
            self.sistema.perfil(psi_max=1.0)
        with self.assertRaises(ValueError):
            self.sistema.perfil(psi_min=0.5, psi_max=0.3)
        with self.assertRaises(ValueError):
            self.sistema.perfil(n_puntos=1)


class TestResumen(unittest.TestCase):
    """Verifica el método resumen()."""

    def setUp(self):
        self.sistema = AbundanciaCoherente(alta_precision=False)

    def test_resumen_keys(self):
        """El resumen debe contener las claves esperadas."""
        r = self.sistema.resumen(0.5)
        self.assertIn("ecuacion", r)
        self.assertIn("parametros", r)
        self.assertIn("resultado", r)
        self.assertIn("sello", r)

    def test_resumen_sello(self):
        """El sello QCAL debe estar presente."""
        r = self.sistema.resumen(0.5)
        self.assertEqual(r["sello"], "∴𓂀Ω∞³Φ")

    def test_resumen_abundancia_positiva(self):
        """La Abundancia en el resumen debe ser positiva."""
        r = self.sistema.resumen(0.5)
        self.assertGreater(r["resultado"]["A (Abundancia)"], 0.0)


class TestAPIFuncional(unittest.TestCase):
    """Verifica las funciones de la API pública."""

    def test_abundancia_scalar(self):
        """abundancia() debe devolver un float positivo."""
        A = abundancia(0.5)
        self.assertIsInstance(A, float)
        self.assertGreater(A, 0.0)

    def test_abundancia_formula(self):
        """
        abundancia(0.5) debe coincidir con I₀·f₀ / (|ζ'(1/2)|·0.5).
        En t=0, I(0) = I₀ = 1.0.
        """
        esperado = 1.0 * F0_HZ / (ABS_ZETA_PRIME_HALF * 0.5)
        self.assertAlmostEqual(abundancia(0.5), esperado, places=4)

    def test_abundancia_invalid_psi(self):
        """abundancia() debe propagar ValueError para Ψ inválido."""
        with self.assertRaises(ValueError):
            abundancia(1.0)
        with self.assertRaises(ValueError):
            abundancia(-0.1)

    def test_limite_abundancia_infinito_default(self):
        """limite_abundancia_infinito() sin args debe devolver dos listas."""
        psi_vals, abunds = limite_abundancia_infinito()
        self.assertIsInstance(psi_vals, list)
        self.assertIsInstance(abunds, list)
        self.assertEqual(len(psi_vals), len(abunds))

    def test_limite_abundancia_infinito_creciente(self):
        """Las abundancias en la secuencia convergente a 1 deben ser crecientes."""
        psi_vals = [0.0, 0.5, 0.9, 0.99, 0.999, 0.9999]
        _, abunds = limite_abundancia_infinito(psi_vals)
        for i in range(len(abunds) - 1):
            self.assertLess(abunds[i], abunds[i + 1])

    def test_limite_abundancia_infinito_custom(self):
        """limite_abundancia_infinito() acepta lista de Ψ personalizada."""
        psi_vals = [0.1, 0.5, 0.9]
        resultados_psi, resultados_a = limite_abundancia_infinito(psi_vals)
        self.assertEqual(resultados_psi, psi_vals)
        self.assertEqual(len(resultados_a), 3)

    def test_abundancia_custom_f0(self):
        """abundancia() debe respetar f0 personalizado."""
        A_default = abundancia(0.5, f0=F0_HZ)
        A_custom = abundancia(0.5, f0=432.0)
        # La razón debe ser proporcional a f0
        ratio_esperado = 432.0 / F0_HZ
        self.assertAlmostEqual(A_custom / A_default, ratio_esperado, places=6)


def run_tests() -> bool:
    """Ejecuta todos los tests y devuelve True si todos pasan."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
