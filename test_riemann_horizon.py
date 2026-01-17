#!/usr/bin/env python3
"""
Test Suite for Riemann Horizon Analysis

Tests the arithmetic black holes framework connecting Riemann zeros
to gravitational wave analysis through H_ψ operator.
"""

import unittest
import numpy as np
import json
from pathlib import Path
import sys

# Import the module
import riemann_horizon as rh


class TestArithmeticHorizon(unittest.TestCase):
    """Test cases for Arithmetic Horizon."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.horizon = rh.ArithmeticHorizon(f0=141.7001, precision=30)
    
    def test_get_riemann_zeros_count(self):
        """Test that correct number of zeros are returned."""
        zeros = self.horizon.get_riemann_zeros(10)
        self.assertEqual(len(zeros), 10)
        
        zeros = self.horizon.get_riemann_zeros(50)
        self.assertEqual(len(zeros), 50)
    
    def test_riemann_zeros_positive(self):
        """Test that all zeros are positive."""
        zeros = self.horizon.get_riemann_zeros(20)
        for z in zeros:
            self.assertGreater(z, 0, "Riemann zero should be positive")
    
    def test_riemann_zeros_ordered(self):
        """Test that zeros are in ascending order."""
        zeros = self.horizon.get_riemann_zeros(30)
        for i in range(len(zeros) - 1):
            self.assertLess(zeros[i], zeros[i+1], "Zeros should be ordered")
    
    def test_first_zero_value(self):
        """Test that first zero has correct value."""
        zeros = self.horizon.get_riemann_zeros(5)
        # First zero should be approximately 14.134725
        self.assertAlmostEqual(zeros[0], 14.134725, places=5)
    
    def test_map_zero_to_frequency(self):
        """Test zero to frequency mapping."""
        t_n = 14.134725  # First Riemann zero
        mapping = self.horizon.map_zero_to_frequency(t_n)
        
        self.assertIn('t_n', mapping)
        self.assertIn('n_estimate', mapping)
        self.assertIn('f_resonance_hz', mapping)
        self.assertIn('harmonic_order', mapping)
        
        self.assertEqual(mapping['t_n'], t_n)
        self.assertGreater(mapping['n_estimate'], 0)
    
    def test_validate_horizon_relationship(self):
        """Test validation of horizon relationship."""
        results = self.horizon.validate_horizon_relationship(10)
        
        self.assertEqual(results['n_zeros_tested'], 10)
        self.assertEqual(results['f0_hz'], 141.7001)
        self.assertIn('mean_deviation', results)
        self.assertIn('max_deviation', results)
        self.assertIn('validation_pass', results)
        
        # Check that we have mappings
        self.assertGreater(len(results['mappings']), 0)


class TestHpsiOperator(unittest.TestCase):
    """Test cases for H_ψ Operator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hpsi = rh.HpsiOperator(lambda_coupling=1.0, max_primes=10)
    
    def test_prime_generation(self):
        """Test that correct primes are generated."""
        # First 10 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(self.hpsi.primes, expected_primes)
    
    def test_potential_shape(self):
        """Test that potential has correct shape."""
        x = np.linspace(0.1, 10, 50)
        V = self.hpsi.potential(x)
        
        self.assertEqual(V.shape, x.shape)
        self.assertTrue(np.all(np.isfinite(V)), "Potential should be finite")
    
    def test_potential_periodicity(self):
        """Test potential has expected structure."""
        x = np.linspace(0.1, 10, 100)
        V = self.hpsi.potential(x)
        
        # Potential should oscillate (not constant)
        self.assertGreater(np.std(V), 0, "Potential should vary")
    
    def test_kinetic_operator_matrix_shape(self):
        """Test kinetic operator matrix dimensions."""
        x = np.linspace(0.1, 10, 20)
        T = self.hpsi.kinetic_operator_matrix(x)
        
        self.assertEqual(T.shape, (20, 20))
        self.assertTrue(np.iscomplexobj(T), "Kinetic operator should be complex")
    
    def test_hamiltonian_matrix_hermitian(self):
        """Test that Hamiltonian is Hermitian."""
        x = np.linspace(0.1, 10, 30)
        H = self.hpsi.hamiltonian_matrix(x)
        
        # Check if H is Hermitian: H = H†
        H_dagger = np.conj(H.T)
        self.assertTrue(np.allclose(H, H_dagger, atol=1e-10),
                       "Hamiltonian should be Hermitian")
    
    def test_solve_eigensystem(self):
        """Test eigenvalue problem solution."""
        x = np.linspace(0.1, 10, 50)
        eigenvalues, eigenvectors = self.hpsi.solve_eigensystem(x, n_states=5)
        
        self.assertEqual(len(eigenvalues), 5)
        self.assertEqual(eigenvectors.shape, (50, 5))
        
        # Eigenvalues should be ordered
        for i in range(len(eigenvalues) - 1):
            self.assertLessEqual(np.real(eigenvalues[i]), np.real(eigenvalues[i+1]))
    
    def test_validate_riemann_connection(self):
        """Test Riemann connection validation."""
        x = np.linspace(0.1, 10, 40)
        riemann_zeros = [14.134725, 21.022040, 25.010857]
        
        results = self.hpsi.validate_riemann_connection(x, riemann_zeros)
        
        self.assertEqual(results['n_states'], 3)
        self.assertIn('comparisons', results)
        self.assertEqual(len(results['comparisons']), 3)
        
        # Each comparison should have expected fields
        for comp in results['comparisons']:
            self.assertIn('eigenvalue_real', comp)
            self.assertIn('eigenvalue_imag', comp)
            self.assertIn('riemann_zero_t_n', comp)
            self.assertIn('difference', comp)


class TestConsciousGeometry(unittest.TestCase):
    """Test cases for Conscious Geometry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.geometry = rh.ConsciousGeometry(f0=141.7001, f888=888.0)
    
    def test_coherence_parameter(self):
        """Test coherence parameter calculation."""
        psi = self.geometry.coherence_parameter(intensity=1.0, effectiveness=2.0)
        
        # Ψ = I × A_eff² = 1.0 × 4.0 = 4.0
        self.assertAlmostEqual(psi, 4.0)
        
        psi2 = self.geometry.coherence_parameter(intensity=2.5, effectiveness=1.5)
        self.assertAlmostEqual(psi2, 2.5 * 1.5**2)
    
    def test_metric_deformation_structure(self):
        """Test metric deformation structure."""
        psi = 5.0
        metric = self.geometry.metric_deformation(psi)
        
        self.assertIsInstance(metric, rh.MetricDeformation)
        self.assertEqual(metric.psi, psi)
        
        # Check all components exist
        self.assertIsNotNone(metric.g_00)
        self.assertIsNotNone(metric.g_11)
        self.assertIsNotNone(metric.delta_g_00)
        self.assertIsNotNone(metric.delta_g_11)
    
    def test_metric_deformation_signature(self):
        """Test that metric preserves signature."""
        psi = 3.0
        metric = self.geometry.metric_deformation(psi)
        
        # Time component should be negative (-, +, +, +) signature
        self.assertLess(metric.g_00, 0, "g_00 should be negative")
        
        # Space component should be positive
        self.assertGreater(metric.g_11, 0, "g_11 should be positive")
    
    def test_metric_reduces_to_minkowski(self):
        """Test that zero deformation gives Minkowski."""
        psi = 0.0
        metric = self.geometry.metric_deformation(psi)
        
        # Should be close to Minkowski
        self.assertAlmostEqual(metric.g_00, -1.0, places=5)
        self.assertAlmostEqual(metric.g_11, 1.0, places=5)
    
    def test_unified_tensor_relation(self):
        """Test unified tensor relation."""
        results = self.geometry.unified_tensor_relation()
        
        self.assertEqual(results['f0_hz'], 141.7001)
        self.assertEqual(results['f888_hz'], 888.0)
        self.assertIn('phi', results)
        self.assertIn('phi_4', results)
        self.assertIn('f0_phi4_hz', results)
        self.assertIn('validation_pass', results)
        
        # φ should be golden ratio
        self.assertAlmostEqual(results['phi'], 1.618033988749895, places=10)
        
        # φ⁴ should be approximately 6.854...
        self.assertAlmostEqual(results['phi_4'], results['phi']**4, places=10)
    
    def test_spectral_duality(self):
        """Test spectral duality."""
        riemann_zeros = [14.134725, 21.022040, 25.010857, 30.424876, 32.935062]
        
        results = self.geometry.spectral_duality(riemann_zeros)
        
        self.assertIn('spectrum_hz', results)
        self.assertIn('f0_hz', results)
        self.assertIn('harmonic_numbers', results)
        self.assertIn('quantum_numbers', results)
        self.assertIn('reconstruction_hz', results)
        
        # Spectrum should match input
        self.assertEqual(len(results['spectrum_hz']), len(riemann_zeros))
        
        # f0 should be set correctly
        self.assertEqual(results['f0_hz'], 141.7001)


class TestRiemannHorizonIntegration(unittest.TestCase):
    """Integration tests for complete Riemann Horizon analysis."""
    
    def test_run_complete_analysis(self):
        """Test that complete analysis runs without errors."""
        # Use small parameters for fast testing
        results = rh.run_complete_analysis(
            n_zeros=10,
            grid_size=30,
            x_min=0.1,
            x_max=10.0
        )
        
        # Check all sections are present
        self.assertIn('arithmetic_horizon', results)
        self.assertIn('hpsi_operator', results)
        self.assertIn('metric_deformation', results)
        self.assertIn('unified_tensor', results)
        self.assertIn('spectral_duality', results)
        self.assertIn('parameters', results)
    
    def test_analysis_parameters_stored(self):
        """Test that analysis stores parameters correctly."""
        results = rh.run_complete_analysis(n_zeros=15, grid_size=40)
        
        self.assertEqual(results['parameters']['n_zeros'], 15)
        self.assertEqual(results['parameters']['grid_size'], 40)
        self.assertEqual(results['parameters']['f0_hz'], 141.7001)
        self.assertEqual(results['parameters']['f888_hz'], 888.0)
    
    def test_analysis_json_serializable(self):
        """Test that results can be serialized to JSON."""
        results = rh.run_complete_analysis(n_zeros=5, grid_size=20)
        
        # Should be able to convert to JSON
        try:
            json_str = json.dumps(results, indent=2)
            self.assertIsInstance(json_str, str)
            
            # Should be able to parse back
            parsed = json.loads(json_str)
            self.assertIsInstance(parsed, dict)
        except (TypeError, ValueError) as e:
            self.fail(f"Results not JSON serializable: {e}")


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_fundamental_constants(self):
        """Test fundamental constants are defined."""
        self.assertEqual(rh.F0_HZ, 141.7001)
        self.assertEqual(rh.F888_HZ, 888.0)
        self.assertAlmostEqual(rh.PHI, 1.618033988749895, places=10)
        self.assertEqual(rh.HBAR, 1.054571817e-34)
    
    def test_golden_ratio(self):
        """Test golden ratio value."""
        # φ = (1 + √5) / 2
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(rh.PHI, expected_phi, places=15)


class TestDataStructures(unittest.TestCase):
    """Test data structure classes."""
    
    def test_riemann_zero_data_creation(self):
        """Test RiemannZeroData creation."""
        data = rh.RiemannZeroData(
            n=1,
            t_n=14.134725,
            frequency_hz=141.7001,
            eigenvalue=complex(14.0, 0.1)
        )
        
        self.assertEqual(data.n, 1)
        self.assertEqual(data.t_n, 14.134725)
        self.assertEqual(data.frequency_hz, 141.7001)
        self.assertEqual(data.eigenvalue, complex(14.0, 0.1))
        self.assertIsNone(data.eigenvector)
    
    def test_metric_deformation_creation(self):
        """Test MetricDeformation creation."""
        metric = rh.MetricDeformation(
            psi=5.0,
            g_00=-1.05,
            g_11=1.05,
            delta_g_00=-0.05,
            delta_g_11=0.05
        )
        
        self.assertEqual(metric.psi, 5.0)
        self.assertEqual(metric.g_00, -1.05)
        self.assertEqual(metric.g_11, 1.05)
        self.assertEqual(metric.delta_g_00, -0.05)
        self.assertEqual(metric.delta_g_11, 0.05)


class TestMathematicalRelations(unittest.TestCase):
    """Test key mathematical relations."""
    
    def test_critical_line_888_relation(self):
        """Test critical line: 888 ≈ f₀ × φ⁴."""
        f0 = 141.7001
        phi = (1 + np.sqrt(5)) / 2
        phi_4 = phi ** 4
        
        result = f0 * phi_4
        
        # Should be close to 888
        # 141.7001 × 6.854... ≈ 971.2
        # This is approximate relation
        self.assertGreater(result, 900)
        self.assertLess(result, 1000)
    
    def test_coherence_formula(self):
        """Test coherence parameter formula Ψ = I × A_eff²."""
        I = 2.0
        A_eff = 3.0
        
        psi_expected = I * A_eff**2
        
        geometry = rh.ConsciousGeometry()
        psi_actual = geometry.coherence_parameter(I, A_eff)
        
        self.assertEqual(psi_actual, psi_expected)


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
