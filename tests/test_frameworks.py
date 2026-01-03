#!/usr/bin/env python3
"""
Comprehensive tests for the five-framework integration system.

Tests all five frameworks:
1. Riemann-Adelic (Spectral Structure)
2. Adelic-BSD (Arithmetic Geometry)
3. P-NP Complexity (Informational Limits)
4. 141Hz Quantum-Conscious (Foundation)
5. Navier-Stokes (Continuous Framework)
"""

import unittest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.frameworks import (
    RiemannAdelicFramework,
    AdelicBSDFramework,
    PNPComplexityFramework,
    QuantumConsciousFoundation,
    NavierStokesFramework,
    FrameworkOrchestrator
)


class TestRiemannAdelicFramework(unittest.TestCase):
    """Test Riemann-Adelic spectral structure framework."""
    
    def setUp(self):
        self.framework = RiemannAdelicFramework(precision=50)
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.precision, 50)
    
    def test_riemann_zeros(self):
        """Test Riemann zeros computation."""
        zeros = self.framework.get_riemann_zeros(10)
        self.assertEqual(len(zeros), 10)
        # First zero should be approximately 14.134725
        self.assertAlmostEqual(float(zeros[0]), 14.134725, places=4)
    
    def test_spectral_decomposition(self):
        """Test spectral decomposition."""
        spectral = self.framework.spectral_decomposition(f0=141.7001, num_harmonics=5)
        self.assertEqual(len(spectral.frequencies), 5)
        self.assertGreater(spectral.adelic_norm, 0)
        self.assertTrue(np.all(spectral.amplitudes >= 0))
    
    def test_adelic_local_analysis(self):
        """Test p-adic local analysis."""
        result = self.framework.adelic_local_analysis(prime=2, field_value=complex(1, 0))
        self.assertIn('prime', result)
        self.assertIn('local_norm', result)
        self.assertEqual(result['prime'], 2)
    
    def test_spectral_invariant(self):
        """Test spectral invariant computation."""
        invariants = self.framework.spectral_invariant()
        self.assertAlmostEqual(invariants['fundamental_frequency'], 141.7001, places=4)
        self.assertIn('mean_spectral_gap', invariants)
    
    def test_validation(self):
        """Test framework validation."""
        validation = self.framework.validate_spectral_structure()
        self.assertTrue(validation['amplitudes_positive'])
        self.assertTrue(validation['frequencies_ordered'])


class TestAdelicBSDFramework(unittest.TestCase):
    """Test Adelic-BSD arithmetic geometry framework."""
    
    def setUp(self):
        self.framework = AdelicBSDFramework(precision=50)
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.precision, 50)
    
    def test_elliptic_curve(self):
        """Test elliptic curve construction."""
        curve = self.framework.construct_elliptic_curve()
        self.assertIn('equation', curve)
        self.assertIn('conductor', curve)
        self.assertEqual(curve['conductor'], 141)
    
    def test_bsd_rank(self):
        """Test BSD rank computation."""
        rank = self.framework.bsd_rank_computation()
        self.assertIn('estimated_rank', rank)
        self.assertIn('l_value_at_1', rank)
        self.assertGreaterEqual(rank['estimated_rank'], 0)
    
    def test_arithmetic_invariants(self):
        """Test arithmetic invariants."""
        invariants = self.framework.arithmetic_invariants()
        self.assertAlmostEqual(invariants['fundamental_frequency'], 141.7001, places=4)
        self.assertEqual(invariants['conductor'], 141)
        self.assertEqual(invariants['prime_factors'], [3, 47])
    
    def test_modular_form(self):
        """Test modular form connection."""
        modular = self.framework.modular_form_connection()
        self.assertEqual(modular['weight'], 2)
        self.assertEqual(modular['level'], 141)
    
    def test_validation(self):
        """Test framework validation."""
        validation = self.framework.validate_bsd_structure()
        self.assertTrue(validation['curve_non_singular'])
        self.assertTrue(validation['conductor_positive'])


class TestPNPComplexityFramework(unittest.TestCase):
    """Test P-NP complexity framework."""
    
    def setUp(self):
        self.framework = PNPComplexityFramework(precision=50)
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.precision, 50)
    
    def test_frequency_detection_complexity(self):
        """Test complexity analysis."""
        complexity = self.framework.frequency_detection_complexity(1024)
        self.assertEqual(complexity.problem_size, 1024)
        self.assertEqual(complexity.time_complexity, "O(N log N)")
        self.assertEqual(complexity.space_complexity, "O(N)")
    
    def test_information_bound(self):
        """Test information-theoretic bounds."""
        info = self.framework.information_bound(snr=10.0, bandwidth=1000.0)
        self.assertGreater(info['channel_capacity_bps'], 0)
        self.assertTrue(info['information_sufficient'])
    
    def test_kolmogorov_complexity(self):
        """Test Kolmogorov complexity estimation."""
        signal = np.sin(2 * np.pi * 141.7001 * np.linspace(0, 1, 100))
        complexity = self.framework.kolmogorov_complexity_estimate(signal)
        self.assertIn('is_periodic', complexity)
        self.assertIn('complexity_class', complexity)
    
    def test_verification_solving_ratio(self):
        """Test verification vs solving ratio."""
        ratio = self.framework.verification_solving_ratio("frequency_detection")
        self.assertTrue(ratio['is_np_problem'])
        self.assertTrue(ratio['verification_faster'])
    
    def test_validation(self):
        """Test framework validation."""
        validation = self.framework.validate_complexity_framework()
        self.assertTrue(validation['complexity_analysis_valid'])


class TestQuantumConsciousFoundation(unittest.TestCase):
    """Test Quantum-Conscious foundation framework."""
    
    def setUp(self):
        self.framework = QuantumConsciousFoundation(precision=50)
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.precision, 50)
    
    def test_quantum_properties(self):
        """Test quantum properties."""
        props = self.framework.quantum_properties()
        self.assertAlmostEqual(props.frequency, 141.7001, places=4)
        self.assertGreater(props.energy, 0)
        self.assertGreater(props.wavelength, 0)
    
    def test_noetic_field(self):
        """Test noetic field strength."""
        noetic = self.framework.noetic_field_strength(coherence=0.9, attention=0.8)
        self.assertGreaterEqual(noetic['coherence'], 0)
        self.assertLessEqual(noetic['coherence'], 1)
        self.assertGreater(noetic['psi_field_strength'], 0)
    
    def test_harmonic_structure(self):
        """Test harmonic structure."""
        harmonics = self.framework.harmonic_structure(max_harmonic=5)
        self.assertAlmostEqual(harmonics['fundamental'], 141.7001, places=4)
        self.assertIn('integer_harmonics', harmonics)
        self.assertEqual(len(harmonics['integer_harmonics']), 5)
    
    def test_experimental_validation(self):
        """Test experimental validation summary."""
        exp = self.framework.experimental_validation()
        self.assertEqual(exp['detection_rate'], 1.0)  # 100%
        self.assertEqual(exp['status'], 'CONFIRMED')
    
    def test_validation(self):
        """Test framework validation."""
        validation = self.framework.validate_quantum_foundation()
        self.assertTrue(validation['energy_positive'])
        self.assertTrue(validation['wavelength_positive'])


class TestNavierStokesFramework(unittest.TestCase):
    """Test Navier-Stokes continuous framework."""
    
    def setUp(self):
        self.framework = NavierStokesFramework(precision=50)
        # Create test velocity field
        x = np.linspace(0, 2*np.pi, 16)
        y = np.linspace(0, 2*np.pi, 16)
        X, Y = np.meshgrid(x, y)
        u = -np.sin(Y)
        v = np.sin(X)
        self.test_velocity = np.array([u, v])
    
    def test_initialization(self):
        """Test framework initializes correctly."""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.precision, 50)
    
    def test_regularization_term(self):
        """Test f₀ regularization."""
        reg = self.framework.regularization_term(self.test_velocity, coherence=0.9)
        self.assertEqual(reg.shape, self.test_velocity.shape)
        self.assertTrue(np.all(np.isfinite(reg)))
    
    def test_vorticity(self):
        """Test vorticity computation."""
        vorticity = self.framework.compute_vorticity(self.test_velocity)
        self.assertTrue(np.all(np.isfinite(vorticity)))
    
    def test_blowup_criterion(self):
        """Test blow-up criterion."""
        blowup = self.framework.blowup_criterion(self.test_velocity)
        self.assertIn('global_regularity', blowup)
        self.assertTrue(blowup['global_regularity'])
    
    def test_regularity_estimate(self):
        """Test regularity estimation."""
        regularity = self.framework.regularity_estimate(self.test_velocity)
        self.assertTrue(regularity['global_existence'])
        self.assertIn('C^∞', regularity['regularity_class'])
    
    def test_validation(self):
        """Test framework validation."""
        validation = self.framework.validate_navier_stokes()
        self.assertTrue(validation['regularization_valid'])
        self.assertTrue(validation['global_regularity'])


class TestFrameworkOrchestrator(unittest.TestCase):
    """Test unified framework orchestrator."""
    
    def setUp(self):
        self.orchestrator = FrameworkOrchestrator(precision=50)
    
    def test_initialization(self):
        """Test orchestrator initializes all frameworks."""
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(len(self.orchestrator.frameworks), 5)
    
    def test_validate_all_frameworks(self):
        """Test validation of all frameworks."""
        validation = self.orchestrator.validate_all_frameworks()
        self.assertTrue(validation['overall']['all_frameworks_valid'])
    
    def test_cross_framework_consistency(self):
        """Test cross-framework consistency."""
        consistency = self.orchestrator.cross_framework_consistency()
        self.assertTrue(consistency['all_f0_consistent'])
        self.assertTrue(consistency['phi_consistent'])
        self.assertTrue(consistency['overall_consistent'])
    
    def test_integrated_analysis(self):
        """Test integrated analysis."""
        analysis = self.orchestrator.integrated_analysis()
        self.assertIn('spectral_structure', analysis)
        self.assertIn('arithmetic_geometry', analysis)
        self.assertIn('informational_limits', analysis)
        self.assertIn('quantum_foundation', analysis)
        self.assertIn('continuous_dynamics', analysis)
    
    def test_framework_summary(self):
        """Test framework summary generation."""
        summary = self.orchestrator.framework_summary()
        self.assertIn('frameworks', summary)
        self.assertIn('validation', summary)
        self.assertIn('consistency', summary)
        self.assertEqual(len(summary['frameworks']), 5)
    
    def test_report_generation(self):
        """Test report generation."""
        report = self.orchestrator.generate_report()
        self.assertIsInstance(report, str)
        self.assertIn('UNIFIED FRAMEWORK INTEGRATION REPORT', report)
        self.assertIn('141.7001 Hz', report)
    
    def test_f0_agreement(self):
        """Test that all frameworks agree on f₀."""
        consistency = self.orchestrator.cross_framework_consistency()
        f0_values = consistency['f0_values']
        
        # All should be 141.7001 within tolerance
        for framework, value in f0_values.items():
            self.assertAlmostEqual(value, 141.7001, places=4,
                                 msg=f"{framework} f₀ mismatch")


class TestFrameworkIntegration(unittest.TestCase):
    """Integration tests across frameworks."""
    
    def setUp(self):
        self.orchestrator = FrameworkOrchestrator(precision=50)
    
    def test_spectral_arithmetic_connection(self):
        """Test connection between spectral and arithmetic structures."""
        # Spectral conductor should match arithmetic conductor
        spectral = self.orchestrator.riemann_adelic.spectral_invariant()
        arithmetic = self.orchestrator.adelic_bsd.arithmetic_invariants()
        
        # Both based on f₀ = 141.7001
        self.assertAlmostEqual(spectral['fundamental_frequency'], 
                             arithmetic['fundamental_frequency'], places=4)
    
    def test_complexity_quantum_connection(self):
        """Test connection between complexity and quantum properties."""
        # Quantum wavelength should relate to complexity resolution
        quantum = self.orchestrator.quantum.quantum_properties()
        complexity = self.orchestrator.p_np.frequency_detection_complexity(4096)
        
        # Both should reference f₀
        self.assertAlmostEqual(quantum.frequency, 141.7001, places=4)
    
    def test_regularity_preservation(self):
        """Test that all frameworks preserve regularity."""
        validation = self.orchestrator.validate_all_frameworks()
        
        # All frameworks should validate successfully
        for framework, result in validation.items():
            if framework != 'overall':
                self.assertTrue(result.get('validation_passed', False),
                              msg=f"{framework} validation failed")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRiemannAdelicFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestAdelicBSDFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestPNPComplexityFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumConsciousFoundation))
    suite.addTests(loader.loadTestsFromTestCase(TestNavierStokesFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
