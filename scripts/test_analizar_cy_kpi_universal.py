#!/usr/bin/env python3
"""
Tests para el análisis del invariante espectral k_Π en variedades Calabi-Yau.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Diciembre 2025
"""

import math
import sys
import unittest
from pathlib import Path

# Añadir el directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from analizar_cy_kpi_universal import (
    CalabiYauQuintic,
    analyze_kpi_universality,
    compute_kpi,
    generate_random_cy_data,
    simulate_cy_laplacian_spectrum,
)


class TestCalabiYauQuintic(unittest.TestCase):
    """Tests para la clase CalabiYauQuintic."""

    def test_default_hodge_numbers(self):
        """Verifica números de Hodge por defecto para quíntica."""
        cy = CalabiYauQuintic(seed=1)
        self.assertEqual(cy.h11, 1)
        self.assertEqual(cy.h21, 101)
        self.assertEqual(cy.chi, -200)

    def test_hodge_variation(self):
        """Verifica variación en h21."""
        cy = CalabiYauQuintic(seed=1, h21_variation=10)
        self.assertEqual(cy.h21, 111)
        self.assertEqual(cy.chi, -220)

    def test_spectrum_generation(self):
        """Verifica que se genera un espectro válido."""
        cy = CalabiYauQuintic(seed=42)
        spectrum = cy.laplacian_spectrum()
        self.assertIsInstance(spectrum, list)
        self.assertGreater(len(spectrum), 0)
        self.assertTrue(all(lam > 0 for lam in spectrum))


class TestSpectralInvariant(unittest.TestCase):
    """Tests para el cálculo del invariante k_Π."""

    def test_compute_kpi_basic(self):
        """Verifica cálculo básico de k_Π."""
        spectrum = [1.0, 2.0, 3.0, 4.0]
        # μ₁ = (1+2+3+4)/4 = 2.5
        # μ₂ = (1+4+9+16)/4 = 7.5
        # k_Π = 7.5/2.5 = 3.0
        k_pi = compute_kpi(spectrum)
        self.assertAlmostEqual(k_pi, 3.0, places=10)

    def test_compute_kpi_empty(self):
        """Verifica manejo de espectro vacío."""
        k_pi = compute_kpi([])
        self.assertTrue(math.isnan(k_pi))

    def test_compute_kpi_single(self):
        """Verifica espectro con un solo elemento."""
        spectrum = [5.0]
        # μ₁ = 5, μ₂ = 25
        # k_Π = 25/5 = 5
        k_pi = compute_kpi(spectrum)
        self.assertAlmostEqual(k_pi, 5.0, places=10)

    def test_kpi_universality(self):
        """Verifica que k_Π es aproximadamente universal."""
        K_PI_UNIVERSAL = 2.5773
        tolerance = 0.3  # Tolerancia para simulación

        results = []
        for seed in range(1, 11):
            spectrum = simulate_cy_laplacian_spectrum(1, 101, seed)
            k_pi = compute_kpi(spectrum)
            results.append(k_pi)

        mean_kpi = sum(results) / len(results)
        # Verificar que el promedio está cerca del valor universal
        self.assertAlmostEqual(mean_kpi, K_PI_UNIVERSAL, delta=tolerance)


class TestDataGeneration(unittest.TestCase):
    """Tests para generación de datos."""

    def test_generate_random_cy_data(self):
        """Verifica generación de datos CY aleatorios."""
        results = generate_random_cy_data(n_samples=5, seed_start=100)
        self.assertGreater(len(results), 0)

        for seed, h11, h21, k_pi, n_eig in results:
            self.assertEqual(h11, 1)
            self.assertGreater(h21, 0)
            self.assertGreater(k_pi, 0)
            self.assertGreater(n_eig, 0)


class TestAnalysis(unittest.TestCase):
    """Tests para análisis estadístico."""

    def test_analyze_kpi_universality(self):
        """Verifica análisis de universalidad."""
        # Datos sintéticos con k_pi constante
        data = [[50, 2.5773], [60, 2.5770], [70, 2.5775], [80, 2.5772]]
        analysis = analyze_kpi_universality(data)

        self.assertIn('slope', analysis)
        self.assertIn('intercept', analysis)
        self.assertIn('r_squared', analysis)
        self.assertIn('mean_kpi', analysis)

        # Pendiente debe ser muy pequeña
        self.assertLess(abs(analysis['slope']), 0.01)

        # Intercepto debe estar cerca de 2.5773
        self.assertAlmostEqual(analysis['intercept'], 2.5773, delta=0.01)


if __name__ == "__main__":
    unittest.main()
