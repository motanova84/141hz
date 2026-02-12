#!/usr/bin/env python3
"""
Tests para Verificación de Convergencia y Constantes Fundamentales

Tests unitarios para:
- QuantumFrequencyCalculator
- verify_fundamental_constants
- plot_convergence_analysis
"""

import sys
import os
import unittest
import numpy as np
import pandas as pd

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from verificacion_convergencia import (
    QuantumFrequencyCalculator,
    verify_fundamental_constants,
    plot_convergence_analysis
)


class TestQuantumFrequencyCalculator(unittest.TestCase):
    """Tests para QuantumFrequencyCalculator"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.calculator = QuantumFrequencyCalculator(precision=30)
    
    def test_initialization(self):
        """Test inicialización del calculador"""
        self.assertEqual(self.calculator.precision, 30)
        self.assertIsNotNone(self.calculator.phi)
        self.assertIsNotNone(self.calculator.gamma)
        self.assertAlmostEqual(float(self.calculator.f0_target), 141.7001, places=4)
    
    def test_phi_value(self):
        """Test valor de phi (razón áurea)"""
        phi = float(self.calculator.phi)
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(phi, expected_phi, places=10)
    
    def test_gamma_value(self):
        """Test valor de gamma (constante de Euler)"""
        gamma = float(self.calculator.gamma)
        # Valor conocido de la constante de Euler-Mascheroni
        expected_gamma = 0.5772156649015329
        self.assertAlmostEqual(gamma, expected_gamma, places=10)
    
    def test_calculate_frequency_from_primes(self):
        """Test cálculo de frecuencia usando primos"""
        freq = self.calculator.calculate_frequency_from_primes(100)
        freq_float = float(freq)
        
        # La frecuencia debe estar cerca del objetivo
        self.assertGreater(freq_float, 140.0)
        self.assertLess(freq_float, 143.0)
        self.assertAlmostEqual(freq_float, 141.7001, delta=1.0)
    
    def test_calculate_gradient_magnitude(self):
        """Test cálculo de magnitud del gradiente"""
        # |∇Ξ(1)| ≈ √N
        n = 100
        magnitude = self.calculator.calculate_gradient_magnitude(n)
        expected = np.sqrt(n)
        
        self.assertAlmostEqual(magnitude, expected, places=5)
    
    def test_convergence_analysis_structure(self):
        """Test estructura del DataFrame de convergencia"""
        # Usar valores pequeños para test rápido
        df = self.calculator.convergence_analysis(max_primes=1000, step=500)
        
        # Verificar estructura
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # 500, 1000
        
        # Verificar columnas
        expected_columns = ['n_primes', 'frequency', 'error_rel',
                           'magnitude', 'sqrt_n', 'ratio']
        for col in expected_columns:
            self.assertIn(col, df.columns)
    
    def test_convergence_analysis_values(self):
        """Test valores del análisis de convergencia"""
        df = self.calculator.convergence_analysis(max_primes=1000, step=500)
        
        # Verificar que n_primes aumenta
        self.assertTrue(df['n_primes'].is_monotonic_increasing)
        
        # Verificar que frecuencias están en rango razonable
        self.assertTrue((df['frequency'] > 140).all())
        self.assertTrue((df['frequency'] < 143).all())
        
        # Verificar que error_rel es positivo
        self.assertTrue((df['error_rel'] >= 0).all())
        
        # Verificar que magnitude ≈ sqrt_n
        for idx, row in df.iterrows():
            self.assertAlmostEqual(row['magnitude'], row['sqrt_n'], places=5)
        
        # Verificar que ratio ≈ 1
        self.assertTrue((df['ratio'] > 0.99).all())
        self.assertTrue((df['ratio'] < 1.01).all())
    
    def test_convergence_with_different_steps(self):
        """Test convergencia con diferentes pasos"""
        df1 = self.calculator.convergence_analysis(max_primes=2000, step=1000)
        df2 = self.calculator.convergence_analysis(max_primes=2000, step=500)
        
        # df2 debe tener más puntos
        self.assertGreater(len(df2), len(df1))


class TestVerifyFundamentalConstants(unittest.TestCase):
    """Tests para verify_fundamental_constants"""
    
    def test_verify_constants_returns_dict(self):
        """Test que verify_fundamental_constants retorna un diccionario"""
        result = verify_fundamental_constants()
        self.assertIsInstance(result, dict)
    
    def test_verify_constants_structure(self):
        """Test estructura del resultado"""
        result = verify_fundamental_constants()

        expected_keys = ['phi_calculated', 'phi_expected',
                        'gamma_calculated', 'gamma_expected',
                        'phi_property_1', 'phi_property_2',
                        'all_verified']
        
        for key in expected_keys:
            self.assertIn(key, result)
    
    def test_phi_verification(self):
        """Test verificación de phi"""
        result = verify_fundamental_constants()
        
        # Phi debe ser correcto
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(result['phi_calculated'], expected_phi, places=10)
        self.assertAlmostEqual(result['phi_expected'], expected_phi, places=10)
    
    def test_gamma_verification(self):
        """Test verificación de gamma"""
        result = verify_fundamental_constants()
        
        # Gamma debe estar en el rango correcto
        self.assertGreater(result['gamma_calculated'], 0.577)
        self.assertLess(result['gamma_calculated'], 0.578)
    
    def test_phi_properties(self):
        """Test propiedades algebraicas de phi"""
        result = verify_fundamental_constants()
        
        # φ² - φ - 1 debe ser ≈ 0
        self.assertAlmostEqual(result['phi_property_1'], 0.0, places=10)
        
        # 1/φ - (φ - 1) debe ser ≈ 0
        self.assertAlmostEqual(result['phi_property_2'], 0.0, places=10)
    
    def test_all_verified_is_true(self):
        """Test que todas las verificaciones pasan"""
        result = verify_fundamental_constants()
        self.assertTrue(result['all_verified'])


class TestPlotConvergenceAnalysis(unittest.TestCase):
    """Tests para plot_convergence_analysis"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.calculator = QuantumFrequencyCalculator(precision=30)
        # Crear DataFrame de prueba
        self.df = self.calculator.convergence_analysis(max_primes=1000, step=500)
    
    def test_plot_accepts_dataframe(self):
        """Test que plot_convergence_analysis acepta DataFrame"""
        try:
            # No mostramos el plot en tests, solo verificamos que no falla
            import matplotlib
            matplotlib.use('Agg')  # Backend sin GUI para tests
            plot_convergence_analysis(self.df)
        except Exception as e:
            self.fail(f"plot_convergence_analysis falló con excepción: {e}")
    
    def test_plot_with_empty_dataframe(self):
        """Test comportamiento con DataFrame vacío"""
        empty_df = pd.DataFrame(columns=['n_primes', 'frequency', 'error_rel',
                                         'magnitude', 'sqrt_n', 'ratio'])
        
        # Debe fallar o manejar graciosamente
        import matplotlib
        matplotlib.use('Agg')
        
        # Esperamos que falle o maneje el caso vacío
        try:
            plot_convergence_analysis(empty_df)
        except (ValueError, IndexError, KeyError):
            # Es esperado que falle con DataFrame vacío
            pass


class TestIntegration(unittest.TestCase):
    """Tests de integración"""
    
    def test_full_workflow(self):
        """Test flujo completo: calcular -> analizar -> verificar"""
        # Crear calculador
        calculator = QuantumFrequencyCalculator(precision=30)
        
        # Calcular frecuencia
        freq = calculator.calculate_frequency_from_primes(100)
        self.assertGreater(float(freq), 140.0)
        
        # Análisis de convergencia
        df = calculator.convergence_analysis(max_primes=1000, step=500)
        self.assertGreater(len(df), 0)
        
        # Verificar constantes
        result = verify_fundamental_constants()
        self.assertTrue(result['all_verified'])
    
    def test_precision_consistency(self):
        """Test consistencia con diferentes precisiones"""
        calc30 = QuantumFrequencyCalculator(precision=30)
        calc50 = QuantumFrequencyCalculator(precision=50)
        
        freq30 = float(calc30.calculate_frequency_from_primes(100))
        freq50 = float(calc50.calculate_frequency_from_primes(100))
        
        # Deben ser muy similares (no exactamente iguales por precisión)
        self.assertAlmostEqual(freq30, freq50, places=5)


def run_tests():
    """Ejecutar todos los tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumFrequencyCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestVerifyFundamentalConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestPlotConvergenceAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
