#!/usr/bin/env python3
"""
Tests for core.validate_weil_spectral_bridge — Puente Espectral Weil-Guinand

Pruebas que cubren la API pública del validador:
  - FormulaExplicitaWeilGuinand   – identidad de Weil-Guinand con par (h, g)
  - OperadorEspectralCalibradoWeyl – calibración de autovalores vía ley de Weyl
  - ejecutar_validacion()          – orquestador combinado
  - resultado_a_dict()             – serialización JSON

Invariantes clave verificados:
  - Error relativo de la fórmula explícita <= 5% (identidad de Weil casi exacta)
  - Tasa de coincidencia espectral (Weyl) >= 90% sobre los primeros 10 ceros
  - lambda_n = 1/4 + gamma_n^2 (relación de Riemann-von Mangoldt)
  - criterio_analitico_numerico == True cuando ambos frentes pasan
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.validate_weil_spectral_bridge import (
    DEFAULT_A_SCALE,
    DEFAULT_MATCH_TARGET_PCT,
    FormulaExplicitaWeilGuinand,
    OperadorEspectralCalibradoWeyl,
    ResultadoFormulaExplicita,
    ResultadoOperadorEspectral,
    ejecutar_validacion,
    resultado_a_dict,
)


class TestFormulaExplicitaWeilGuinand(unittest.TestCase):
    def setUp(self):
        self.formula = FormulaExplicitaWeilGuinand(a_scale=DEFAULT_A_SCALE, precision=30)

    def test_h_is_even(self):
        r = 3.7
        self.assertAlmostEqual(float(self.formula.h(r)), float(self.formula.h(-r)), places=10)

    def test_von_mangoldt_prime(self):
        import mpmath as mp
        self.assertAlmostEqual(float(self.formula._von_mangoldt(7)), float(mp.log(7)), places=10)

    def test_von_mangoldt_prime_power(self):
        import mpmath as mp
        self.assertAlmostEqual(float(self.formula._von_mangoldt(8)), float(mp.log(2)), places=10)

    def test_von_mangoldt_composite_non_prime_power(self):
        self.assertEqual(float(self.formula._von_mangoldt(6)), 0.0)

    def test_evaluar_returns_result(self):
        resultado = self.formula.evaluar(n_zeros_max=50, prime_cutoff=100)
        self.assertIsInstance(resultado, ResultadoFormulaExplicita)

    def test_evaluar_error_within_tolerance(self):
        resultado = self.formula.evaluar(n_zeros_max=50, prime_cutoff=100, tolerancia_pct=5.0)
        self.assertLessEqual(resultado.error_relativo_pct, 5.0)
        self.assertTrue(resultado.passed)

    def test_evaluar_error_near_zero(self):
        # La identidad de Weil-Guinand es exacta; el error numérico residual
        # (truncamiento de ceros y primos) debe ser minúsculo.
        resultado = self.formula.evaluar(n_zeros_max=50, prime_cutoff=100)
        self.assertLess(resultado.error_relativo_pct, 1e-3)


class TestOperadorEspectralCalibradoWeyl(unittest.TestCase):
    def setUp(self):
        self.operador = OperadorEspectralCalibradoWeyl(precision=30)

    def test_calibrar_returns_result(self):
        resultado = self.operador.calibrar(n_check=10)
        self.assertIsInstance(resultado, ResultadoOperadorEspectral)

    def test_lambda_relation(self):
        resultado = self.operador.calibrar(n_check=5)
        for c in resultado.comparaciones:
            self.assertAlmostEqual(c.lambda_n_real, 0.25 + c.gamma_n_real ** 2, places=6)
            self.assertAlmostEqual(c.lambda_n_calibrado, 0.25 + c.gamma_n_calibrado ** 2, places=6)

    def test_eigenvalues_not_confined_to_sub_unit_interval(self):
        # Regresión: el fallo original confinaba los autovalores a [0.25, 4.80].
        # El primer autovalor calibrado debe estar muy por encima de ese rango
        # (lambda_1 ~ 200 según gamma_1 ~ 14.13).
        resultado = self.operador.calibrar(n_check=1)
        self.assertGreater(resultado.comparaciones[0].lambda_n_calibrado, 100.0)

    def test_match_rate_meets_target(self):
        resultado = self.operador.calibrar(n_check=10, target_pct=DEFAULT_MATCH_TARGET_PCT)
        self.assertGreaterEqual(resultado.match_rate_pct, DEFAULT_MATCH_TARGET_PCT)
        self.assertTrue(resultado.passed)


class TestEjecutarValidacion(unittest.TestCase):
    def test_criterio_analitico_numerico_passed(self):
        resultado = ejecutar_validacion(n_zeros_max=50, prime_cutoff=100)
        self.assertTrue(resultado.criterio_analitico_numerico)

    def test_resultado_a_dict_serializable(self):
        import json
        resultado = ejecutar_validacion(n_zeros_max=50, prime_cutoff=100)
        d = resultado_a_dict(resultado)
        # Must be JSON-serializable without error.
        json.dumps(d)
        self.assertIn("formula_explicita_weil_guinand", d)
        self.assertIn("operador_espectral_weyl", d)
        self.assertIn("criterio_analitico_numerico", d)


if __name__ == "__main__":
    unittest.main()
