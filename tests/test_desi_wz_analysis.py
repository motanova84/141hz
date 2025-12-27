#!/usr/bin/env python3
"""
Tests for DESI cosmological analysis.
"""

import unittest
import numpy as np
import sys
import os

# Add desi to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'desi'))

from desi_wz_analysis import DESICosmologyAnalysis, W0_GQN, WA_GQN


class TestDESICosmologyAnalysis(unittest.TestCase):
    """Tests para DESICosmologyAnalysis."""
    
    def setUp(self):
        """Configure analysis for tests."""
        self.analysis = DESICosmologyAnalysis()
    
    def test_w_cpla(self):
        """Test de ecuación de estado CPL."""
        z = np.array([0, 0.5, 1.0, 1.5])
        w0, wa = -1.0, 0.2
        
        w = self.analysis.w_cpla(z, w0, wa)
        
        # Verificar dimensiones
        self.assertEqual(len(w), len(z))
        
        # Verificar valor en z=0
        self.assertAlmostEqual(w[0], w0, places=10)
        
        # Verificar que w crece con z (para wa > 0)
        self.assertGreater(w[1], w[0])
        self.assertGreater(w[2], w[1])
    
    def test_E_z(self):
        """Test de factor de expansión E(z)."""
        z = np.array([0, 0.5, 1.0])
        w0, wa = -1.0, 0.0  # ΛCDM
        
        E = self.analysis.E_z(z, w0, wa)
        
        # Verificar dimensiones
        self.assertEqual(len(E), len(z))
        
        # E(0) debe ser 1
        self.assertAlmostEqual(E[0], 1.0, places=10)
        
        # E(z) debe crecer con z
        self.assertGreater(E[1], E[0])
        self.assertGreater(E[2], E[1])
        
        # Verificar valores positivos
        self.assertTrue(np.all(E > 0))
    
    def test_luminosity_distance(self):
        """Test de distancia de luminosidad."""
        z = np.array([0, 0.5, 1.0])
        w0, wa = -1.0, 0.0
        
        D_L = self.analysis.luminosity_distance(z, w0, wa)
        
        # Verificar dimensiones
        self.assertEqual(len(D_L), len(z))
        
        # D_L(0) debe ser 0
        self.assertAlmostEqual(D_L[0], 0.0, places=5)
        
        # D_L debe crecer con z
        self.assertGreater(D_L[1], D_L[0])
        self.assertGreater(D_L[2], D_L[1])
        
        # Verificar valores positivos
        self.assertTrue(np.all(D_L >= 0))
    
    def test_generate_mock_desi_data(self):
        """Test de generación de datos mock."""
        z, D_L, D_L_err = self.analysis.generate_mock_desi_data(
            z_range=(0.1, 2.0),
            n_points=50,
            w0_true=-1.0,
            wa_true=0.0,
            noise_level=0.02
        )
        
        # Verificar dimensiones
        self.assertEqual(len(z), 50)
        self.assertEqual(len(D_L), 50)
        self.assertEqual(len(D_L_err), 50)
        
        # Verificar rango de z
        self.assertGreaterEqual(z.min(), 0.1)
        self.assertLessEqual(z.max(), 2.0)
        
        # Verificar que errores son positivos
        self.assertTrue(np.all(D_L_err > 0))
    
    def test_log_likelihood(self):
        """Test de log-likelihood."""
        # Datos mock simples
        z_data = np.array([0.5, 1.0, 1.5])
        D_L_data = np.array([2000, 4000, 6000])
        D_L_err = np.array([100, 200, 300])
        
        # Parámetros
        params = np.array([-1.0, 0.0])
        
        log_like = self.analysis.log_likelihood(params, z_data, D_L_data, D_L_err)
        
        # Verificar que es un número finito
        self.assertTrue(np.isfinite(log_like))
        
        # Verificar prior: parámetros extremos deben dar -inf
        bad_params = np.array([-5.0, 0.0])
        log_like_bad = self.analysis.log_likelihood(bad_params, z_data, D_L_data, D_L_err)
        self.assertEqual(log_like_bad, -np.inf)
    
    def test_fit_with_scipy(self):
        """Test de ajuste con scipy."""
        # Generar datos mock con parámetros conocidos
        z_data, D_L_data, D_L_err = self.analysis.generate_mock_desi_data(
            w0_true=-1.0,
            wa_true=0.1,
            noise_level=0.01
        )
        
        # Ajustar
        results = self.analysis.fit_with_scipy(z_data, D_L_data, D_L_err)
        
        # Verificar estructura
        self.assertIn('method', results)
        self.assertIn('w0', results)
        self.assertIn('wa', results)
        self.assertIn('w0_err', results)
        self.assertIn('wa_err', results)
        
        # Verificar que el ajuste es cercano a los valores verdaderos
        self.assertAlmostEqual(results['w0'], -1.0, delta=0.2)
        self.assertAlmostEqual(results['wa'], 0.1, delta=0.3)
    
    def test_calculate_tension(self):
        """Test de cálculo de tensión."""
        # Parámetros cercanos a GQN
        w0_fit = -1.02
        wa_fit = 0.18
        
        tension = self.analysis.calculate_tension(w0_fit, wa_fit)
        
        # Verificar estructura
        self.assertIn('delta_w_mean', tension)
        self.assertIn('delta_w_max', tension)
        self.assertIn('compatible_with_gqn', tension)
        self.assertIn('z_range', tension)
        
        # Verificar que tensión es pequeña (cercano a GQN)
        self.assertLess(tension['delta_w_mean'], 0.1)
        
        # Verificar compatibilidad
        self.assertTrue(tension['compatible_with_gqn'])
    
    def test_run_analysis(self):
        """Test de análisis completo."""
        # Ejecutar análisis con datos mock
        results = self.analysis.run_analysis(
            use_mock_data=True,
            save_results=False
        )
        
        # Verificar estructura
        self.assertIn('fit', results)
        self.assertIn('tension', results)
        self.assertIn('gqn_prediction', results)
        self.assertIn('data', results)
        
        # Verificar predicción GQN
        self.assertEqual(results['gqn_prediction']['w0'], W0_GQN)
        self.assertEqual(results['gqn_prediction']['wa'], WA_GQN)


class TestDESIPhysics(unittest.TestCase):
    """Tests de física cosmológica."""
    
    def test_gqn_prediction_values(self):
        """Test de valores predichos por GQN."""
        self.assertEqual(W0_GQN, -1.0)
        self.assertEqual(WA_GQN, 0.2)
    
    def test_flat_universe(self):
        """Test de universo plano."""
        analysis = DESICosmologyAnalysis()
        
        # Omega_m + Omega_Lambda = 1
        self.assertAlmostEqual(
            analysis.omega_m + analysis.omega_lambda,
            1.0,
            places=10
        )


def main():
    """Ejecutar tests."""
    unittest.main()


if __name__ == '__main__':
    main()
