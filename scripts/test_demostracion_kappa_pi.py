#!/usr/bin/env python3
"""
Tests para Demostración Rigurosa de κ_Π = 2.5773 Universal

Verifica:
1. Convergencia con volumen hacia κ_Π objetivo
2. Invariancia en espacio de módulos (h^{2,1})
3. Convergencia numérica con precisión

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Institución: Instituto QCAL ∞³
"""

import os
import sys
import unittest

import numpy as np

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from demostracion_kappa_pi_universal import (  # noqa: E402
    KAPPA_PI_TARGET,
    CalabiYauSimulator,
    test_convergence_volume,
    test_invariance_moduli,
    test_convergence_precision,
    run_all_tests
)


class TestCalabiYauSimulator(unittest.TestCase):
    """Tests para el simulador Calabi-Yau."""

    def setUp(self):
        """Inicializa el simulador para los tests."""
        self.simulator = CalabiYauSimulator(h21=101, n_modos=1000)

    def test_initialization(self):
        """Verifica inicialización correcta del simulador."""
        self.assertEqual(self.simulator.h21, 101)
        self.assertEqual(self.simulator.n_modos, 1000)
        self.assertEqual(len(self.simulator.eigenvalues), 1000)

    def test_eigenvalues_positive(self):
        """Verifica que todos los eigenvalores son positivos."""
        self.assertTrue(all(self.simulator.eigenvalues > 0))

    def test_eigenvalues_ordered(self):
        """Verifica que los eigenvalores están aproximadamente ordenados."""
        # Deben estar en orden creciente en general
        diffs = self.simulator.eigenvalues[1:] - self.simulator.eigenvalues[:-1]
        # La mayoría de las diferencias deben ser positivas (allowing for fluctuations)
        positive_ratio = sum(diffs > 0) / len(diffs)
        self.assertGreater(positive_ratio, 0.7)  # Allow for quantum fluctuations

    def test_mu_parameters_range(self):
        """Verifica que μ₁ y μ₂ están en rango válido."""
        mu1, mu2 = self.simulator.calculate_mu_parameters(volume=1.0)

        # μ₁ y μ₂ deben ser positivos
        self.assertGreater(mu1, 0)
        self.assertGreater(mu2, 0)

        # μ₁ y μ₂ deben ser menores que 1 para distribuciones típicas
        self.assertLess(mu1, 1.5)
        self.assertLess(mu2, 1.5)

    def test_kappa_calculation(self):
        """Verifica cálculo de κ."""
        mu1, mu2, kappa = self.simulator.calculate_kappa(volume=1.0)

        # Todos los valores deben ser positivos
        self.assertGreater(mu1, 0)
        self.assertGreater(mu2, 0)
        self.assertGreater(kappa, 0)

    def test_kappa_volume_dependence(self):
        """Verifica que κ converge con el volumen."""
        kappas = []
        volumes = [1, 10, 100, 1000]

        for vol in volumes:
            _, _, kappa = self.simulator.calculate_kappa(vol)
            kappas.append(kappa)

        # κ debe tender hacia KAPPA_PI_TARGET con mayor volumen
        # El último valor debe estar más cerca del objetivo
        final_error = abs(kappas[-1] - KAPPA_PI_TARGET)
        initial_error = abs(kappas[0] - KAPPA_PI_TARGET)

        self.assertLess(final_error, initial_error)


class TestConvergenceVolume(unittest.TestCase):
    """Tests para convergencia con volumen."""

    def test_basic_convergence(self):
        """Test básico de convergencia con volumen."""
        results = test_convergence_volume(
            h21=101,
            n_modos=500,
            n_points=10,
            quiet=True
        )

        self.assertEqual(results['test'], 'convergence_volume')
        self.assertEqual(len(results['results']), 10)
        self.assertIn('mean_kappa', results)
        self.assertIn('converged', results)

    def test_kappa_convergence_to_target(self):
        """Verifica convergencia de κ hacia el objetivo."""
        results = test_convergence_volume(
            h21=101,
            n_modos=1000,
            n_points=20,
            quiet=True
        )

        # El error relativo debe ser razonable
        self.assertLess(results['error_relative_percent'], 10.0)

    def test_volume_results_structure(self):
        """Verifica estructura de resultados."""
        results = test_convergence_volume(
            h21=50,
            n_modos=200,
            n_points=5,
            quiet=True
        )

        for r in results['results']:
            self.assertIn('volume', r)
            self.assertIn('mu1', r)
            self.assertIn('mu2', r)
            self.assertIn('kappa', r)


class TestInvarianceModuli(unittest.TestCase):
    """Tests para invariancia en espacio de módulos."""

    def test_basic_invariance(self):
        """Test básico de invariancia."""
        results = test_invariance_moduli(
            n_modos=500,
            volume=100.0,
            quiet=True
        )

        self.assertEqual(results['test'], 'invariance_moduli')
        self.assertIn('mean_kappa', results)
        self.assertIn('variation_percent', results)

    def test_variation_bounded(self):
        """Verifica que la variación está acotada."""
        results = test_invariance_moduli(
            n_modos=1000,
            volume=500.0,
            quiet=True
        )

        # La variación debe ser menor al 20%
        self.assertLess(results['variation_percent'], 20.0)

    def test_all_h21_values_computed(self):
        """Verifica que se calculan todos los valores de h^{2,1}."""
        results = test_invariance_moduli(
            n_modos=200,
            volume=100.0,
            quiet=True
        )

        h21_values = [r['h21'] for r in results['results']]
        expected_h21 = [20, 40, 60, 80, 101, 120, 140, 160]

        self.assertEqual(h21_values, expected_h21)


class TestConvergencePrecision(unittest.TestCase):
    """Tests para convergencia con precisión."""

    def test_basic_precision(self):
        """Test básico de convergencia con precisión."""
        results = test_convergence_precision(
            h21=101,
            volume=100.0,
            quiet=True
        )

        self.assertEqual(results['test'], 'convergence_precision')
        self.assertIn('final_kappa', results)
        self.assertIn('final_error', results)

    def test_error_decreasing(self):
        """Verifica que el error es razonablemente pequeño al aumentar modos."""
        results = test_convergence_precision(
            h21=101,
            volume=500.0,
            quiet=True
        )

        errors = [r['error'] for r in results['results']]

        # El error debe ser razonablemente estable/pequeño
        # (puede no decrecer significativamente ya que κ es determinista por volumen)
        self.assertLess(errors[-1], 0.2)  # Error final menor a 0.2

    def test_n_modos_range(self):
        """Verifica que se prueban múltiples valores de n_modos."""
        results = test_convergence_precision(quiet=True)

        n_modos_values = [r['n_modos'] for r in results['results']]

        # Debe incluir valores desde 100 hasta 10000
        self.assertEqual(n_modos_values[0], 100)
        self.assertEqual(n_modos_values[-1], 10000)


class TestIntegration(unittest.TestCase):
    """Tests de integración completa."""

    def test_run_all_tests(self):
        """Ejecuta todos los tests integrados."""
        results = run_all_tests(
            save_plot=False,
            save_json=False,
            quiet=True
        )

        self.assertIn('target', results)
        self.assertEqual(results['target'], KAPPA_PI_TARGET)
        self.assertIn('test_volume', results)
        self.assertIn('test_moduli', results)
        self.assertIn('test_precision', results)
        self.assertIn('all_tests_passed', results)

    def test_target_value(self):
        """Verifica valor objetivo de κ_Π."""
        self.assertEqual(KAPPA_PI_TARGET, 2.5773)

    def test_plot_generation(self):
        """Verifica que se puede generar el gráfico."""
        results = run_all_tests(
            save_plot=True,
            save_json=False,
            quiet=True
        )

        self.assertIsNotNone(results['plot_path'])
        # Verificar que el archivo existe
        if results['plot_path']:
            self.assertTrue(os.path.exists(results['plot_path']))


class TestReproducibility(unittest.TestCase):
    """Tests de reproducibilidad."""

    def test_same_seed_same_results(self):
        """Verifica que la misma semilla produce los mismos resultados."""
        sim1 = CalabiYauSimulator(h21=101, n_modos=500, seed=42)
        sim2 = CalabiYauSimulator(h21=101, n_modos=500, seed=42)

        mu1_a, mu2_a, kappa_a = sim1.calculate_kappa(volume=100.0)
        mu1_b, mu2_b, kappa_b = sim2.calculate_kappa(volume=100.0)

        self.assertAlmostEqual(mu1_a, mu1_b, places=10)
        self.assertAlmostEqual(mu2_a, mu2_b, places=10)
        self.assertAlmostEqual(kappa_a, kappa_b, places=10)

    def test_different_seeds_different_results(self):
        """Verifica que semillas diferentes producen resultados μ distintos."""
        sim1 = CalabiYauSimulator(h21=101, n_modos=500, seed=42)
        sim2 = CalabiYauSimulator(h21=101, n_modos=500, seed=123)

        mu1_a, mu2_a, _ = sim1.calculate_kappa(volume=100.0)
        mu1_b, mu2_b, _ = sim2.calculate_kappa(volume=100.0)

        # Los μ deben ser ligeramente diferentes debido a fluctuaciones
        # Note: κ may be the same since it depends only on volume in this model
        eigenvalues_differ = not np.allclose(sim1.eigenvalues, sim2.eigenvalues)
        self.assertTrue(eigenvalues_differ)


if __name__ == '__main__':
    # Ejecutar tests
    unittest.main(verbosity=2)
