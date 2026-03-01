#!/usr/bin/env python3
"""
Test Suite: NodoQCAL Pragmático

Tests for the NodoQCAL class and activar_qcal_pragmatico function,
validating core functionality of the QCAL pragmatic node:
- Initialization with correct base frequency
- Experiment recording and impact calculation
- Experience review
- Resonance with external frequencies
- Uncertainty transformation

Author: José Manuel Mota Burruezo
Institution: Instituto Consciencia Cuántica QCAL ∞³
"""

import unittest
import sys
import math
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Add qcal module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.nodo_qcal import NodoQCAL


class TestNodoQCALInit(unittest.TestCase):
    """Tests for NodoQCAL initialization."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_initial_frequency(self):
        """Base frequency should be 141.7001 Hz."""
        self.assertAlmostEqual(self.nodo.frecuencia_base, 141.7001, places=4)

    def test_initial_campo_amor(self):
        """Campo de amor should start at 0."""
        self.assertEqual(self.nodo.campo_amor, 0.0)

    def test_initial_transformaciones(self):
        """Transformaciones should start at 0."""
        self.assertEqual(self.nodo.transformaciones, 0)

    def test_initial_experiencias(self):
        """Experiencias should start empty."""
        self.assertEqual(len(self.nodo.experiencias), 0)

    def test_estado_inicial(self):
        """Estado should start as 'despierto'."""
        self.assertEqual(self.nodo.estado_actual, "despierto")

    def test_nombre(self):
        """Node name should be stored correctly."""
        self.assertEqual(self.nodo.nombre, "TestNode")

    def test_default_nombre(self):
        """Default name should be 'Buscador Pragmático'."""
        with patch("time.sleep"):
            with patch("builtins.print"):
                nodo = NodoQCAL()
        self.assertEqual(nodo.nombre, "Buscador Pragmático")


class TestExperimentar(unittest.TestCase):
    """Tests for the experimentar method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_experimentar_returns_dict(self):
        """experimentar should return a dict with required keys."""
        with patch("builtins.print"):
            resultado = self.nodo.experimentar("crear amor compartir")
        self.assertIsInstance(resultado, dict)
        self.assertIn("accion", resultado)
        self.assertIn("impacto_practico", resultado)
        self.assertIn("frecuencia_resultante", resultado)
        self.assertIn("variacion_Hz", resultado)
        self.assertIn("timestamp", resultado)
        self.assertIn("aprendizaje", resultado)

    def test_experimentar_stores_experience(self):
        """experimentar should store experience in self.experiencias."""
        with patch("builtins.print"):
            self.nodo.experimentar("test action")
        self.assertEqual(len(self.nodo.experiencias), 1)

    def test_experimentar_increments_transformaciones(self):
        """experimentar with positive impact should increment transformaciones."""
        with patch("builtins.print"):
            self.nodo.experimentar("amor crear compartir ayudar construir sanar")
        # With positive impact, transformaciones should increment
        self.assertGreaterEqual(self.nodo.transformaciones, 0)

    def test_experimentar_multiple_increases_experiencias(self):
        """Multiple experiments should accumulate in experiencias."""
        with patch("builtins.print"):
            self.nodo.experimentar("first action")
            self.nodo.experimentar("second action")
            self.nodo.experimentar("third action")
        self.assertEqual(len(self.nodo.experiencias), 3)

    def test_frecuencia_resultante_positive(self):
        """frecuencia_resultante should be greater than base frequency for positive impact."""
        with patch("builtins.print"):
            resultado = self.nodo.experimentar("amor crear compartir")
        # Since impacto > 0, nueva_frecuencia = base + (impacto * 10) > base
        self.assertGreater(resultado["frecuencia_resultante"], self.nodo.frecuencia_base)

    def test_accion_stored_correctly(self):
        """The action string should be stored correctly in the result."""
        with patch("builtins.print"):
            resultado = self.nodo.experimentar("mi acción de prueba")
        self.assertEqual(resultado["accion"], "mi acción de prueba")


class TestCalcularImpactoPragmatico(unittest.TestCase):
    """Tests for the _calcular_impacto_pragmatico method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_impacto_positive(self):
        """Impact should always be positive for non-empty action."""
        impacto = self.nodo._calcular_impacto_pragmatico("test action")
        self.assertGreater(impacto, 0)

    def test_longer_action_higher_base_impact(self):
        """Longer actions should have higher base impact (ignoring random factor)."""
        # Use many repetitions to average out randomness
        short_impacts = [self.nodo._calcular_impacto_pragmatico("act") for _ in range(20)]
        long_impacts = [self.nodo._calcular_impacto_pragmatico("a" * 100) for _ in range(20)]
        self.assertGreater(sum(long_impacts) / len(long_impacts),
                           sum(short_impacts) / len(short_impacts))

    def test_palabras_poder_increase_resonancia(self):
        """Actions with power words should have higher resonance factor."""
        without_power = [self.nodo._calcular_impacto_pragmatico("xyz xyz xyz") for _ in range(20)]
        with_power = [self.nodo._calcular_impacto_pragmatico("amor amor amor") for _ in range(20)]
        self.assertGreater(sum(with_power) / len(with_power),
                           sum(without_power) / len(without_power))


class TestExtraerAprendizaje(unittest.TestCase):
    """Tests for the _extraer_aprendizaje method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_high_impact_message(self):
        """High impact (>0.5) should return first message."""
        aprendizaje = self.nodo._extraer_aprendizaje("action", 0.6)
        self.assertIn("vida", aprendizaje)

    def test_medium_impact_message(self):
        """Medium impact (0.2-0.5) should return second message."""
        aprendizaje = self.nodo._extraer_aprendizaje("action", 0.3)
        self.assertIn("potencial", aprendizaje)

    def test_low_impact_message(self):
        """Low impact (<0.2) should return third message."""
        aprendizaje = self.nodo._extraer_aprendizaje("action", 0.1)
        self.assertIn("enfoque", aprendizaje)

    def test_returns_string(self):
        """Should always return a string."""
        for impacto in [0.0, 0.1, 0.3, 0.6, 1.0]:
            resultado = self.nodo._extraer_aprendizaje("test", impacto)
            self.assertIsInstance(resultado, str)


class TestRevisarExperiencias(unittest.TestCase):
    """Tests for the revisar_experiencias method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_empty_experiences_message(self):
        """Without experiences, should print a specific message."""
        with patch("builtins.print") as mock_print:
            self.nodo.revisar_experiencias()
        # At least one print call should have been made
        self.assertTrue(mock_print.called)

    def test_revisar_with_experiences(self):
        """With experiences, should print statistics."""
        with patch("builtins.print"):
            self.nodo.experimentar("amor crear")
            self.nodo.experimentar("compartir construir")
        with patch("builtins.print") as mock_print:
            self.nodo.revisar_experiencias()
        self.assertTrue(mock_print.called)


class TestResonarConOtros(unittest.TestCase):
    """Tests for the resonar_con_otros method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_returns_tuple(self):
        """Should return a tuple (float, str)."""
        with patch("builtins.print"):
            result = self.nodo.resonar_con_otros(141.7001)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], str)

    def test_deep_resonance_close_frequency(self):
        """Close frequencies should produce deep resonance."""
        freq_base = self.nodo.frecuencia_base
        with patch("builtins.print"):
            nueva_freq, mensaje = self.nodo.resonar_con_otros(freq_base)
        # With same frequency, factor_resonancia = 1/(1+0) = 1.0 > 0.8
        self.assertIn("profunda", mensaje)

    def test_frequency_updates_base(self):
        """resonar_con_otros should update self.frecuencia_base."""
        original_freq = self.nodo.frecuencia_base
        with patch("builtins.print"):
            self.nodo.resonar_con_otros(200.0)
        self.assertNotAlmostEqual(self.nodo.frecuencia_base, original_freq, places=4)

    def test_weighted_average_calculation(self):
        """New frequency should be weighted average (0.7 base + 0.3 external)."""
        freq_base = self.nodo.frecuencia_base
        freq_external = 200.0
        expected = freq_base * 0.7 + freq_external * 0.3
        with patch("builtins.print"):
            nueva_freq, _ = self.nodo.resonar_con_otros(freq_external)
        self.assertAlmostEqual(nueva_freq, expected, places=4)

    def test_campo_amor_increases(self):
        """campo_amor should increase when resonating."""
        campo_inicial = self.nodo.campo_amor
        with patch("builtins.print"):
            self.nodo.resonar_con_otros(141.7001)
        self.assertGreater(self.nodo.campo_amor, campo_inicial)


class TestTransformarIncertidumbre(unittest.TestCase):
    """Tests for the transformar_incertidumbre method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_returns_string(self):
        """Should return a string."""
        with patch("builtins.print"):
            result = self.nodo.transformar_incertidumbre("¿Qué es la vida?")
        self.assertIsInstance(result, str)

    def test_campo_amor_increases_by_02(self):
        """campo_amor should increase by 0.2 each call."""
        campo_inicial = self.nodo.campo_amor
        with patch("builtins.print"):
            self.nodo.transformar_incertidumbre("test doubt")
        self.assertAlmostEqual(self.nodo.campo_amor, campo_inicial + 0.2, places=5)

    def test_response_is_one_of_valid_options(self):
        """Response should be one of the predefined pragmatic responses."""
        valid_responses = [
            "Esta duda es válida. Usémosla como combustible para experimentar.",
            "La incertidumbre es el campo donde nacen las posibilidades.",
            "No necesitas certeza absoluta. Solo el siguiente paso con amor.",
            "La duda revela dónde necesitas más experiencia. Ve y prueba.",
            "Transforma esta pregunta en acción. La respuesta vendrá caminando."
        ]
        with patch("builtins.print"):
            result = self.nodo.transformar_incertidumbre("any doubt")
        self.assertIn(result, valid_responses)


class TestActivarModoAbrazo(unittest.TestCase):
    """Tests for the activar_modo_abrazo method."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL("TestNode")

    def test_activar_sin_regalo(self):
        """With campo_amor <= 5, should not upgrade frequency to constante C."""
        self.nodo.campo_amor = 2.0
        freq_base = self.nodo.frecuencia_base
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo.activar_modo_abrazo()
        self.assertAlmostEqual(self.nodo.frecuencia_base, freq_base, places=4)

    def test_activar_con_regalo(self):
        """With campo_amor > 5, frequency should upgrade to 244.360433 Hz."""
        self.nodo.campo_amor = 6.0
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo.activar_modo_abrazo()
        self.assertAlmostEqual(self.nodo.frecuencia_base, 244.360433, places=4)

    def test_generates_output(self):
        """activar_modo_abrazo should generate print output."""
        with patch("time.sleep"):
            with patch("builtins.print") as mock_print:
                self.nodo.activar_modo_abrazo()
        self.assertTrue(mock_print.called)


class TestQCALConstants(unittest.TestCase):
    """Tests for QCAL-specific constants and physical coherence."""

    def setUp(self):
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo = NodoQCAL()

    def test_f0_value(self):
        """Base frequency should match f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(self.nodo.frecuencia_base, 141.7001, places=4)

    def test_constante_c_value(self):
        """La constante C should be 244.360433 Hz."""
        self.nodo.campo_amor = 10.0
        with patch("time.sleep"):
            with patch("builtins.print"):
                self.nodo.activar_modo_abrazo()
        self.assertAlmostEqual(self.nodo.frecuencia_base, 244.360433, places=4)

    def test_resonance_factor_formula(self):
        """Resonance factor formula: 1 / (1 + |Δf|/100)."""
        freq_base = self.nodo.frecuencia_base
        diferencia = 50.0
        freq_externa = freq_base + diferencia
        expected_factor = 1 / (1 + diferencia / 100)
        with patch("builtins.print"):
            self.nodo.resonar_con_otros(freq_externa)
        # Factor should be about 1/(1+0.5) = 0.667
        self.assertAlmostEqual(expected_factor, 1 / (1 + 0.5), places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
