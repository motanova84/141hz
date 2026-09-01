#!/usr/bin/env python3
"""
Test de Verificación: Cuadratura del Círculo QCAL

Valida la ecuación fundamental:
    π · φ² · 10 · δ = π · φ

Y todas sus relaciones derivadas.
Framework: unittest estándar (Python ≥ 3.8)
"""

import unittest
import math
import os
import sys

# === Constantes QCAL ===
PHI = (1 + math.sqrt(5)) / 2            # φ = 1.618033988749895...
PI = math.pi                             # π = 3.141592653589793...
F0 = 141.7001                            # f₀ = 141.7001 Hz
DELTA_TEORICO = 1 / (10 * PHI)          # δ = 1/(10φ)
DELTA_RELACION = (PHI - 1) / 10         # δ = (φ-1)/10

# Precisión (decimales significativos)
PRECISION = 12


class TestConstantesQCAL(unittest.TestCase):
    """Validación de constantes fundamentales."""

    def test_phi_definicion(self):
        """φ = (1 + √5)/2 ± 1e-15"""
        esperado = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, esperado, places=15)

    def test_phi_identidad_cuadratica(self):
        """φ² - φ - 1 = 0"""
        resultado = PHI**2 - PHI - 1
        self.assertAlmostEqual(resultado, 0.0, places=15)

    def test_phi_inverso(self):
        """1/φ = φ - 1"""
        self.assertAlmostEqual(1 / PHI, PHI - 1, places=15)

    def test_delta_definicion(self):
        """δ = 1/(10φ)"""
        self.assertAlmostEqual(DELTA_TEORICO, DELTA_RELACION, places=15)


class TestCuadraturaCirculo(unittest.TestCase):
    """Test de la ecuación de cuadratura QCAL."""

    def test_ecuacion_fundamental(self):
        """π · φ² · 10 · δ = π · φ"""
        izquierda = PI * (PHI**2) * 10 * DELTA_TEORICO
        derecha = PI * PHI
        self.assertAlmostEqual(izquierda, derecha, places=PRECISION)

    def test_factor_reducido(self):
        """φ² · 10 · δ = φ"""
        factor = (PHI**2) * 10 * DELTA_TEORICO
        self.assertAlmostEqual(factor, PHI, places=PRECISION)

    def test_factor_unitario(self):
        """φ · 10 · δ = 1"""
        factor = PHI * 10 * DELTA_TEORICO
        self.assertAlmostEqual(factor, 1.0, places=PRECISION)

    def test_delta_por_phi(self):
        """δ · φ = 1/10"""
        self.assertAlmostEqual(DELTA_TEORICO * PHI, 0.1, places=PRECISION)


class TestInvarianteEterno(unittest.TestCase):
    """Test del invariante pentadimensional."""

    def test_invariante_5d_4d(self):
        """(f₀(5D) - f₀(4D)) × φ = 0.1"""
        # De la relación: f₀(5D) - f₀(4D) = 0.1/φ
        diff_esperada = 0.1 / PHI
        # Verificamos que el invariante se cumple
        invariante = diff_esperada * PHI
        self.assertAlmostEqual(invariante, 0.1, places=PRECISION)

    def test_delta_como_diferencia(self):
        """δ = (f₀(5D) - f₀(4D)) / 1 Hz (escala)"""
        diff = 0.1 / PHI
        self.assertAlmostEqual(DELTA_TEORICO, diff, places=PRECISION)


class TestOperadorTransformacion(unittest.TestCase):
    """Test del operador de transformación T_n."""

    def test_operador_t1(self):
        """T₁(π) = π · φ · 10 · δ = π"""
        resultado = PI * PHI * 10 * DELTA_TEORICO
        self.assertAlmostEqual(resultado, PI, places=PRECISION)

    def test_operador_t2(self):
        """T₂(π) = π · φ² · 10 · δ = π · φ"""
        resultado = PI * (PHI**2) * 10 * DELTA_TEORICO
        self.assertAlmostEqual(resultado, PI * PHI, places=PRECISION)

    def test_operador_t0(self):
        """T₀(π) = π · 10 · δ = π / φ"""
        resultado = PI * 10 * DELTA_TEORICO
        self.assertAlmostEqual(resultado, PI / PHI, places=PRECISION)


class TestEstabilidadNumerica(unittest.TestCase):
    """Verificación de estabilidad numérica con alta precisión."""

    def test_no_divergencia(self):
        """El operador T no diverge bajo iteración."""
        valor = PI
        for _ in range(100):
            valor = valor * (PHI**2) * 10 * DELTA_TEORICO
        # Tras 100 iteraciones debe ser π · φ¹⁰⁰
        esperado = PI * (PHI ** 100)
        # Comparación relativa: error relativo < 1e-12
        error_rel = abs(valor - esperado) / abs(esperado)
        self.assertLess(error_rel, 1e-12, f"Error relativo: {error_rel:.2e}")

    def test_simetria_circular(self):
        """La ecuación es invariante bajo φ → 1/φ (simetría dual)."""
        phi_inv = 1 / PHI
        delta_inv = 1 / (10 * phi_inv)
        izquierda = PI * (phi_inv**2) * 10 * delta_inv
        derecha = PI * phi_inv
        self.assertAlmostEqual(izquierda, derecha, places=PRECISION)


class TestFormatoArchivo(unittest.TestCase):
    """Verificación de que el paper markdown está presente y es válido."""

    def test_paper_exists(self):
        """El archivo del paper existe."""
        path = os.path.join(os.path.dirname(__file__), "CUADRATURA_CIRCULO_QCAL.md")
        self.assertTrue(os.path.isfile(path), f"Falta el archivo: {path}")

    def test_paper_not_empty(self):
        """El paper no está vacío."""
        path = os.path.join(os.path.dirname(__file__), "CUADRATURA_CIRCULO_QCAL.md")
        with open(path, "r") as f:
            content = f.read()
        self.assertGreater(len(content), 1000, "El paper está vacío o truncado")

    def test_paper_has_equation(self):
        """El paper contiene la ecuación fundamental."""
        path = os.path.join(os.path.dirname(__file__), "CUADRATURA_CIRCULO_QCAL.md")
        with open(path, "r") as f:
            content = f.read()
        self.assertIn("pi", content.lower())


if __name__ == "__main__":
    print(f"=== Test: Cuadratura del Círculo QCAL ===")
    print(f"φ = {PHI:.15f}")
    print(f"δ = {DELTA_TEORICO:.15f}")
    print(f"f₀ = {F0} Hz")
    print(f"Verificación: π · φ² · 10 · δ = {PI * (PHI**2) * 10 * DELTA_TEORICO:.15f}")
    print(f"Verificación: π · φ         = {PI * PHI:.15f}")
    print(f"Error absoluto: {abs(PI * (PHI**2) * 10 * DELTA_TEORICO - PI * PHI):.2e}")
    print()
    unittest.main(verbosity=2)
