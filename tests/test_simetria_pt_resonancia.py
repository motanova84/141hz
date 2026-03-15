#!/usr/bin/env python3
"""
Tests for physics.simetria_pt_resonancia

Validates the PT-symmetry resonance simulation (Protocolo QCAL-SYMBIO-1):
- Non-Hermitian operator with PT symmetry produces real eigenvalues at Ψ → 1.
- Eigenvalue stability collapses to the Riemann critical line under high coherence.
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.simetria_pt_resonancia import (
    BaseRiemann,
    EspectroEigenvalores,
    MotorResonanciaPT,
    OperadorPT,
    ResultadoResonanciaPT,
    activar_protocolo_qcal_symbio_1,
    simular_resonancia_pt,
)


class TestBaseRiemann(unittest.TestCase):
    """Tests for BaseRiemann spectral proxy."""

    def test_shape(self):
        """Generated array must have exactly n elements."""
        b = BaseRiemann(50, semilla=0)
        self.assertEqual(b.valores.shape, (50,))

    def test_ordenado(self):
        """Values must be sorted in ascending order."""
        b = BaseRiemann(100, semilla=42)
        self.assertTrue(np.all(b.valores[:-1] <= b.valores[1:]))

    def test_diagonal_shape(self):
        """como_diagonal() must return an N×N matrix."""
        b = BaseRiemann(10, semilla=1)
        d = b.como_diagonal()
        self.assertEqual(d.shape, (10, 10))

    def test_diagonal_values(self):
        """Diagonal entries must match the sorted values array."""
        b = BaseRiemann(10, semilla=2)
        d = b.como_diagonal()
        np.testing.assert_array_equal(np.diag(d), b.valores)

    def test_n_invalido(self):
        """n < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            BaseRiemann(0)

    def test_reproducibilidad(self):
        """Same seed must produce identical values."""
        b1 = BaseRiemann(30, semilla=99)
        b2 = BaseRiemann(30, semilla=99)
        np.testing.assert_array_equal(b1.valores, b2.valores)

    def test_semillas_distintas(self):
        """Different seeds should produce different values (with overwhelming probability)."""
        b1 = BaseRiemann(30, semilla=1)
        b2 = BaseRiemann(30, semilla=2)
        self.assertFalse(np.array_equal(b1.valores, b2.valores))


class TestOperadorPT(unittest.TestCase):
    """Tests for OperadorPT non-Hermitian Hamiltonian."""

    def setUp(self):
        self.base = BaseRiemann(10, semilla=0)

    def test_shape(self):
        """Constructed matrix must be N×N."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        self.assertEqual(h.shape, (10, 10))

    def test_dtype_complejo(self):
        """Matrix must have complex dtype."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        self.assertTrue(np.iscomplexobj(h))

    def test_diagonal_real_igual_base(self):
        """Real part of diagonal must match the Riemann base values."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        np.testing.assert_allclose(np.diag(h).real, self.base.valores)

    def test_parte_imaginaria_suprimida_con_coherencia_1(self):
        """At coherencia=1.0 the imaginary part must be exactly zero."""
        op = OperadorPT(self.base, coherencia=1.0)
        h = op.construir()
        np.testing.assert_array_equal(h.imag, np.zeros((10, 10)))

    def test_parte_imaginaria_no_nula_coherencia_baja(self):
        """At coherencia=0.5 the imaginary part must not be all zero."""
        op = OperadorPT(self.base, coherencia=0.5)
        h = op.construir()
        self.assertFalse(np.allclose(h.imag, 0))

    def test_coherencia_invalida_negativa(self):
        """Negative coherence must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=-0.1)

    def test_coherencia_invalida_cero(self):
        """coherencia=0 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=0.0)

    def test_coherencia_invalida_mayor_uno(self):
        """coherencia > 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=1.001)

    def test_antidiagonal_imaginaria(self):
        """Imaginary coupling must follow fliplr(eye) × (1 − Ψ) pattern."""
        op = OperadorPT(self.base, coherencia=0.9)
        h = op.construir()
        expected_imag = np.fliplr(np.eye(10)) * 0.1
        np.testing.assert_allclose(h.imag, expected_imag)


class TestEspectroEigenvalores(unittest.TestCase):
    """Tests for EspectroEigenvalores spectral analysis."""

    def _operador_alta_coherencia(self, n=20, semilla=0):
        base = BaseRiemann(n, semilla=semilla)
        op = OperadorPT(base, coherencia=0.999999)
        return op.construir()

    def _operador_baja_coherencia(self, n=20, semilla=0):
        base = BaseRiemann(n, semilla=semilla)
        op = OperadorPT(base, coherencia=0.5)
        return op.construir()

    def test_numero_autovalores(self):
        """Number of eigenvalues must equal matrix dimension."""
        h = self._operador_alta_coherencia(n=15)
        esp = EspectroEigenvalores(h)
        self.assertEqual(len(esp.autovalores), 15)

    def test_estable_coherencia_alta(self):
        """High coherence operator must be PT-stable (eigenvalues ≈ real)."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertTrue(esp.es_estable())

    def test_inestable_coherencia_baja(self):
        """Low coherence operator must NOT be PT-stable."""
        h = self._operador_baja_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertFalse(esp.es_estable())

    def test_media_imaginaria_cerca_cero_alta_coherencia(self):
        """Mean imaginary part must be < atol for high coherence."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertLess(esp.media_imaginaria(), 1e-5)

    def test_max_imaginario_cerca_cero_alta_coherencia(self):
        """Max imaginary part must be < atol for high coherence."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertLess(esp.max_imaginario(), 1e-5)

    def test_media_imaginaria_no_nula_baja_coherencia(self):
        """Mean imaginary part must be significant for low coherence."""
        h = self._operador_baja_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertGreater(esp.media_imaginaria(), 1e-3)


class TestMotorResonanciaPT(unittest.TestCase):
    """Tests for MotorResonanciaPT integration engine."""

    def test_resultado_tipo(self):
        """ejecutar() must return a ResultadoResonanciaPT instance."""
        motor = MotorResonanciaPT(n_dimension=10, coherencia=0.999999, semilla=0)
        resultado = motor.ejecutar()
        self.assertIsInstance(resultado, ResultadoResonanciaPT)

    def test_n_dimension_invalida(self):
        """n_dimension < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            MotorResonanciaPT(n_dimension=0)

    def test_coherencia_invalida(self):
        """coherencia outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            MotorResonanciaPT(coherencia=1.5)

    def test_estable_alta_coherencia(self):
        """High coherence must produce a stable (PT-symmetric) result."""
        motor = MotorResonanciaPT(n_dimension=50, coherencia=0.999999, semilla=42)
        resultado = motor.ejecutar()
        self.assertTrue(resultado.estable)

    def test_inestable_baja_coherencia(self):
        """Low coherence must produce an unstable result."""
        motor = MotorResonanciaPT(n_dimension=50, coherencia=0.5, semilla=42)
        resultado = motor.ejecutar()
        self.assertFalse(resultado.estable)

    def test_coherencia_reflejada_en_resultado(self):
        """Result must reflect the coherence parameter used."""
        motor = MotorResonanciaPT(n_dimension=10, coherencia=0.95, semilla=0)
        resultado = motor.ejecutar()
        self.assertAlmostEqual(resultado.coherencia, 0.95)

    def test_n_dimension_reflejada(self):
        """Result n_dimension must match the motor parameter."""
        motor = MotorResonanciaPT(n_dimension=30, coherencia=0.999999, semilla=0)
        resultado = motor.ejecutar()
        self.assertEqual(resultado.n_dimension, 30)
        self.assertEqual(len(resultado.autovalores), 30)

    def test_reproducibilidad_con_semilla(self):
        """Same seed must produce identical eigenvalues (order-independent)."""
        r1 = MotorResonanciaPT(n_dimension=20, coherencia=0.999999, semilla=7).ejecutar()
        r2 = MotorResonanciaPT(n_dimension=20, coherencia=0.999999, semilla=7).ejecutar()
        sort_key = lambda a: np.lexsort((a.imag, a.real))
        idx1 = sort_key(r1.autovalores)
        idx2 = sort_key(r2.autovalores)
        np.testing.assert_allclose(
            r1.autovalores[idx1], r2.autovalores[idx2], rtol=1e-12, atol=1e-14
        )

    def test_metricas_imaginarias_positivas(self):
        """media_imaginaria and max_imaginario must be >= 0."""
        resultado = MotorResonanciaPT(n_dimension=20, semilla=0).ejecutar()
        self.assertGreaterEqual(resultado.media_imaginaria, 0.0)
        self.assertGreaterEqual(resultado.max_imaginario, 0.0)

    def test_max_mayor_o_igual_media(self):
        """max_imaginario must be >= media_imaginaria."""
        resultado = MotorResonanciaPT(n_dimension=20, semilla=0).ejecutar()
        self.assertGreaterEqual(resultado.max_imaginario, resultado.media_imaginaria)


class TestResultadoResonanciaPT(unittest.TestCase):
    """Tests for ResultadoResonanciaPT dataclass."""

    def setUp(self):
        self.resultado = MotorResonanciaPT(n_dimension=10, coherencia=0.999999, semilla=0).ejecutar()

    def test_resumen_contiene_coherencia(self):
        """resumen() must include the coherence value."""
        texto = self.resultado.resumen()
        self.assertIn("0.999999", texto)

    def test_resumen_contiene_umbral_biologico(self):
        """resumen() must include the biological threshold check."""
        texto = self.resultado.resumen()
        self.assertIn("Umbral biológico", texto)

    def test_resumen_contiene_estabilidad(self):
        """resumen() must include PT stability status."""
        texto = self.resultado.resumen()
        self.assertIn("Estabilidad", texto)

    def test_resumen_es_cadena(self):
        """resumen() must return a string."""
        self.assertIsInstance(self.resultado.resumen(), str)


class TestSimularResonanciaPT(unittest.TestCase):
    """Tests for the simular_resonancia_pt public API."""

    def test_retorna_array(self):
        """Must return a numpy array."""
        resultado = simular_resonancia_pt(n_dimension=10, coherencia=0.999999, semilla=0)
        self.assertIsInstance(resultado, np.ndarray)

    def test_longitud_array(self):
        """Length of returned array must equal n_dimension."""
        resultado = simular_resonancia_pt(n_dimension=25, coherencia=0.999999, semilla=0)
        self.assertEqual(len(resultado), 25)

    def test_estabilidad_alta_coherencia(self):
        """Eigenvalues must be approximately real at high coherence."""
        autovalores = simular_resonancia_pt(n_dimension=100, coherencia=0.999999, semilla=0)
        self.assertTrue(np.allclose(autovalores.imag, 0, atol=1e-5))

    def test_inestabilidad_baja_coherencia(self):
        """Eigenvalues must have significant imaginary parts at low coherence."""
        autovalores = simular_resonancia_pt(n_dimension=100, coherencia=0.5, semilla=0)
        self.assertFalse(np.allclose(autovalores.imag, 0, atol=1e-5))

    def test_n_dimension_invalida(self):
        """n_dimension < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            simular_resonancia_pt(n_dimension=0)

    def test_coherencia_invalida(self):
        """coherencia outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            simular_resonancia_pt(coherencia=0.0)

    def test_valores_default(self):
        """Default parameters (n=100, Ψ=0.999999) must produce stable spectrum."""
        autovalores = simular_resonancia_pt(semilla=0)
        self.assertEqual(len(autovalores), 100)
        self.assertTrue(np.allclose(autovalores.imag, 0, atol=1e-5))


class TestActivarProtocoloQcalSymbio1(unittest.TestCase):
    """Tests for the activar_protocolo_qcal_symbio_1 public API."""

    def test_retorna_resultado(self):
        """Must return a ResultadoResonanciaPT instance."""
        resultado = activar_protocolo_qcal_symbio_1(n_dimension=10, semilla=0)
        self.assertIsInstance(resultado, ResultadoResonanciaPT)

    def test_estabilidad_default(self):
        """Default call must yield PT stability True."""
        resultado = activar_protocolo_qcal_symbio_1(semilla=0)
        self.assertTrue(resultado.estable)

    def test_coherencia_igual_a_parametro(self):
        """Result coherence must match the parameter passed."""
        resultado = activar_protocolo_qcal_symbio_1(coherencia=0.9999, semilla=0)
        self.assertAlmostEqual(resultado.coherencia, 0.9999)


if __name__ == "__main__":
    unittest.main()
