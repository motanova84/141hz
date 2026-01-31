"""
Tests for Cytoplasmic Flow Model with Quantum Resonance

This test suite validates:
1. Reynolds number calculation in Stokes regime
2. RiemannResonanceOperator eigenfrequencies
3. Hermitian property of the operator
4. Beltrami flow conditions
5. Microtubule quantum lattice
6. Riemann pressure field
7. Integration with cardiac coherence

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.cytoplasmic_flow_model import (
    CytoplasmicParameters,
    RiemannResonanceOperator,
    BeltramiFlow,
    MicrotubuleQuantumLattice,
    RiemannPressureField,
    validate_cytoplasmic_flow_model
)
from qcal.constants import F0_HZ


class TestCytoplasmicParameters(unittest.TestCase):
    """Test cytoplasmic physical parameters."""
    
    def setUp(self):
        self.params = CytoplasmicParameters()
    
    def test_density(self):
        """Test cytoplasm density."""
        self.assertEqual(self.params.rho, 1050.0, "Density should be 1050 kg/m³")
    
    def test_viscosity(self):
        """Test kinematic viscosity."""
        self.assertEqual(self.params.nu, 1e-6, "Viscosity should be 10^-6 m²/s")
    
    def test_reynolds_number(self):
        """Test Reynolds number calculation."""
        Re = self.params.reynolds_number()
        self.assertLess(Re, 1e-2, "Reynolds number should be << 1 (Stokes regime)")
        self.assertAlmostEqual(Re, 1e-6, places=8, 
                              msg="Re should be approximately 10^-6")
    
    def test_stokes_regime(self):
        """Test that flow is in Stokes regime."""
        self.assertTrue(self.params.is_stokes_regime(),
                       "Flow should be in Stokes regime (Re << 1)")
    
    def test_kinesin_velocity_range(self):
        """Test kinesin velocity is in valid range."""
        self.assertGreaterEqual(self.params.v_kinesin, self.params.v_kinesin_min)
        self.assertLessEqual(self.params.v_kinesin, self.params.v_kinesin_max)


class TestRiemannResonanceOperator(unittest.TestCase):
    """Test Riemann resonance operator for eigenfrequencies."""
    
    def setUp(self):
        self.operator = RiemannResonanceOperator(n_modes=10)
        self.params = CytoplasmicParameters()
    
    def test_fundamental_frequency(self):
        """Test that fundamental frequency is f₀."""
        self.assertAlmostEqual(self.operator.f0, F0_HZ, places=4,
                              msg="Fundamental frequency should be 141.7001 Hz")
    
    def test_eigenfrequencies_harmonics(self):
        """Test that eigenfrequencies are harmonics of f₀."""
        results = self.operator.compute_eigenfrequencies(self.params)
        
        frequencies = results['frequencies']
        harmonics = results['harmonics']
        
        # Check that we have the expected number of modes
        self.assertEqual(len(frequencies), self.operator.n_modes,
                        "Should have correct number of eigenfrequencies")
        
        # Check that frequencies are multiples of f₀
        for i, (freq, n) in enumerate(zip(frequencies, harmonics)):
            expected_freq = n * F0_HZ
            self.assertAlmostEqual(freq, expected_freq, places=2,
                                  msg=f"Frequency {i+1} should be {n} × f₀")
    
    def test_hermitian_property(self):
        """Test that operator is Hermitian (self-adjoint)."""
        verification = self.operator.verify_hermitian(self.params, tolerance=1e-10)
        
        self.assertTrue(verification['is_hermitian'],
                       "Operator should be Hermitian for Hilbert-Pólya approach")
        self.assertLess(verification['max_difference'], 1e-10,
                       "Hermitian deviation should be negligible")
        self.assertEqual(verification['status'], 'PASSED',
                        "Hermitian verification should pass")
    
    def test_eigenvalues_real(self):
        """Test that eigenvalues are real (consequence of Hermiticity)."""
        results = self.operator.compute_eigenfrequencies(self.params)
        eigenvalues = results['eigenvalues']
        
        # For a Hermitian operator, eigenvalues should be real
        self.assertTrue(np.all(np.isreal(eigenvalues)),
                       "Eigenvalues of Hermitian operator should be real")


class TestBeltramiFlow(unittest.TestCase):
    """Test Beltrami flow with vorticity alignment."""
    
    def setUp(self):
        self.beltrami = BeltramiFlow(lambda_param=1.0)
    
    def test_velocity_field(self):
        """Test velocity field generation."""
        x = np.linspace(0, 10e-6, 50)
        y = np.linspace(0, 10e-6, 50)
        X, Y = np.meshgrid(x, y)
        
        vx, vy = self.beltrami.velocity_field_2d(X, Y, t=0)
        
        # Velocity should be finite
        self.assertTrue(np.all(np.isfinite(vx)), "vx should be finite")
        self.assertTrue(np.all(np.isfinite(vy)), "vy should be finite")
    
    def test_vorticity_field(self):
        """Test vorticity field generation."""
        x = np.linspace(0, 10e-6, 50)
        y = np.linspace(0, 10e-6, 50)
        X, Y = np.meshgrid(x, y)
        
        omega = self.beltrami.vorticity_2d(X, Y, t=0)
        
        # Vorticity should be finite and non-negative
        self.assertTrue(np.all(np.isfinite(omega)), "Vorticity should be finite")
        self.assertTrue(np.all(omega >= 0), "Vorticity magnitude should be non-negative")
    
    def test_beltrami_condition(self):
        """Test that ω ≈ λv (Beltrami condition)."""
        x = np.linspace(0, 10e-6, 50)
        y = np.linspace(0, 10e-6, 50)
        X, Y = np.meshgrid(x, y)
        
        verification = self.beltrami.verify_beltrami_condition(X, Y, t=0, tolerance=0.1)
        
        self.assertTrue(verification['condition_satisfied'],
                       "Beltrami condition ω = λv should be satisfied")
        self.assertLess(verification['max_relative_error'], 0.1,
                       "Relative error should be small")


class TestMicrotubuleQuantumLattice(unittest.TestCase):
    """Test microtubule quantum lattice model."""
    
    def setUp(self):
        self.lattice = MicrotubuleQuantumLattice(n_dimers=100)
        self.params = CytoplasmicParameters()
    
    def test_lattice_constant(self):
        """Test that lattice constant is ~8 nm (tubulin dimer size)."""
        self.assertAlmostEqual(self.lattice.a, 8e-9, places=10,
                              msg="Lattice constant should be ~8 nm")
    
    def test_dimer_positions(self):
        """Test tubulin dimer positions."""
        positions = self.lattice.dimer_positions()
        
        self.assertEqual(len(positions), self.lattice.n_dimers,
                        "Should have correct number of dimers")
        
        # Check spacing
        spacing = np.diff(positions)
        self.assertTrue(np.allclose(spacing, self.lattice.a),
                       "Dimers should be evenly spaced")
    
    def test_kinesin_velocity(self):
        """Test kinesin velocity profile."""
        positions = self.lattice.dimer_positions()
        velocities = self.lattice.kinesin_velocity_profile(positions)
        
        # Velocities should be positive and in reasonable range
        self.assertTrue(np.all(velocities > 0), "Velocities should be positive")
        self.assertTrue(np.all(velocities < 10e-6),
                       "Velocities should be < 10 μm/s")
    
    def test_streaming_flow(self):
        """Test cytoplasmic streaming flow generation."""
        flow = self.lattice.generate_streaming_flow(self.params)
        
        self.assertIn('mean_velocity', flow)
        self.assertIn('mean_reynolds', flow)
        
        # Check that Reynolds number is in Stokes regime
        self.assertLess(flow['mean_reynolds'], 1e-2,
                       "Mean Reynolds should be in Stokes regime")


class TestRiemannPressureField(unittest.TestCase):
    """Test Riemann pressure field with zeros as minima."""
    
    def setUp(self):
        self.pressure = RiemannPressureField(n_zeros=10)
    
    def test_riemann_zeros(self):
        """Test that we have correct Riemann zeros."""
        # First Riemann zero is at t ≈ 14.134725
        self.assertAlmostEqual(self.pressure.riemann_zeros_t[0], 14.134725, places=4,
                              msg="First Riemann zero should be correct")
        
        # All zeros should be positive
        self.assertTrue(np.all(self.pressure.riemann_zeros_t > 0),
                       "Riemann zeros should be positive")
    
    def test_pressure_field(self):
        """Test pressure field generation."""
        x = np.linspace(0, 10e-6, 1000)
        p = self.pressure.pressure_field_1d(x, t=0)
        
        # Pressure should be finite
        self.assertTrue(np.all(np.isfinite(p)), "Pressure should be finite")
    
    def test_pressure_minima(self):
        """Test that pressure minima exist."""
        x = np.linspace(0, 10e-6, 1000)
        minima = self.pressure.find_pressure_minima(x)
        
        # Should find some minima
        self.assertGreater(len(minima), 0,
                          "Should find pressure minima")
    
    def test_critical_line_torus(self):
        """Test critical line parametrization as torus."""
        theta = np.linspace(0, 2*np.pi, 50)
        phi = np.linspace(0, 2*np.pi, 50)
        Theta, Phi = np.meshgrid(theta, phi)
        
        x, y, z = self.pressure.critical_line_torus(Theta, Phi)
        
        # Coordinates should be finite
        self.assertTrue(np.all(np.isfinite(x)), "x should be finite")
        self.assertTrue(np.all(np.isfinite(y)), "y should be finite")
        self.assertTrue(np.all(np.isfinite(z)), "z should be finite")


class TestFullValidation(unittest.TestCase):
    """Test full model validation."""
    
    def test_complete_validation(self):
        """Test complete cytoplasmic flow model validation."""
        results = validate_cytoplasmic_flow_model()
        
        # Check Reynolds number
        self.assertLess(results['reynolds_number'], 1e-2,
                       "Reynolds should be in Stokes regime")
        self.assertTrue(results['is_stokes_regime'],
                       "Should confirm Stokes regime")
        
        # Check eigenfrequencies
        self.assertIn('eigenfrequencies', results)
        self.assertIn('harmonics', results)
        self.assertEqual(results['f0'], F0_HZ,
                        "Should use correct fundamental frequency")
        
        # Check Hermitian property
        self.assertEqual(results['hermitian_check']['status'], 'PASSED',
                        "Hermitian check should pass")
        
        # Check Beltrami condition
        self.assertTrue(results['beltrami_check']['condition_satisfied'],
                       "Beltrami condition should be satisfied")
        
        # Check microtubule flow
        self.assertIn('microtubule_flow', results)
        self.assertLess(results['microtubule_flow']['mean_reynolds'], 1e-2,
                       "Microtubule flow should be in Stokes regime")
        
        # Check pressure minima
        self.assertGreater(results['pressure_minima_count'], 0,
                          "Should find pressure minima")


if __name__ == '__main__':
    unittest.main(verbosity=2)
