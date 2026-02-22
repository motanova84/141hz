#!/usr/bin/env python3
"""
Unit Tests for QCAL Biological Framework

Tests the mathematical implementation of the QCAL biological hypothesis,
including spectral field theory, phase accumulation, and biological
resonance mechanisms.

Author: José Manuel Mota Burruezo
Date: 27 de enero de 2026
Institution: Instituto Consciencia Cuántica QCAL ∞³
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add qcal module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.biological_qcal import (
    SpectralComponent,
    EnvironmentalSpectralField,
    BiologicalFilter,
    PhaseAccumulator,
    QCALBiologicalSystem,
    create_annual_cycle_field,
    create_cicada_filter
)


class TestSpectralComponent(unittest.TestCase):
    """Test SpectralComponent class."""
    
    def test_component_creation(self):
        """Test creating a spectral component."""
        comp = SpectralComponent(
            amplitude=1.0,
            frequency=2*np.pi,  # 1 Hz
            phase=0.0,
            description="Test component"
        )
        
        self.assertEqual(comp.amplitude, 1.0)
        self.assertEqual(comp.frequency, 2*np.pi)
        self.assertEqual(comp.phase, 0.0)
    
    def test_component_evaluation(self):
        """Test evaluating component at specific times."""
        comp = SpectralComponent(
            amplitude=2.0,
            frequency=2*np.pi,  # 1 Hz
            phase=0.0
        )
        
        t = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        values = comp.evaluate(t)
        
        # Check that we get complex values
        self.assertTrue(np.iscomplexobj(values))
        
        # At t=0, should be amplitude * e^(i*0) = amplitude
        self.assertAlmostEqual(np.abs(values[0]), 2.0, places=6)
        
        # Check periodicity at t=1 (one full cycle)
        self.assertAlmostEqual(np.abs(values[0] - values[4]), 0.0, places=6)


class TestEnvironmentalSpectralField(unittest.TestCase):
    """Test EnvironmentalSpectralField class."""
    
    def test_empty_field(self):
        """Test empty field evaluates to zero."""
        field = EnvironmentalSpectralField()
        t = np.linspace(0, 10, 100)
        psi = field.evaluate(t)
        
        self.assertTrue(np.allclose(psi, 0.0))
    
    def test_single_component_field(self):
        """Test field with single component."""
        field = EnvironmentalSpectralField()
        field.add_component(amplitude=1.0, frequency=2*np.pi, phase=0.0)
        
        t = np.array([0.0, 0.5, 1.0])
        psi = field.evaluate(t)
        
        # Check complex output
        self.assertTrue(np.iscomplexobj(psi))
        
        # Check periodicity
        self.assertAlmostEqual(np.abs(psi[0] - psi[2]), 0.0, places=6)
    
    def test_multiple_components_superposition(self):
        """Test superposition of multiple components."""
        field = EnvironmentalSpectralField()
        field.add_component(amplitude=1.0, frequency=2*np.pi, phase=0.0)
        field.add_component(amplitude=0.5, frequency=4*np.pi, phase=0.0)
        
        t = np.linspace(0, 2, 100)
        psi = field.evaluate(t)
        
        # Field should not be zero
        self.assertFalse(np.allclose(psi, 0.0))
        
        # Check that magnitude is reasonable (sum of amplitudes)
        max_magnitude = np.max(np.abs(psi))
        self.assertLessEqual(max_magnitude, 1.5 + 0.1)  # 1.0 + 0.5 + tolerance
    
    def test_power_spectrum(self):
        """Test power spectrum computation."""
        field = EnvironmentalSpectralField()
        field.add_component(amplitude=1.0, frequency=2*np.pi*10, phase=0.0)  # 10 Hz
        
        t = np.linspace(0, 1, 1000)
        freqs, power = field.power_spectrum(t)
        
        # Should have positive frequencies
        self.assertTrue(np.all(freqs >= 0))
        
        # Power should peak near 10 Hz
        peak_idx = np.argmax(power)
        peak_freq = freqs[peak_idx]
        self.assertAlmostEqual(peak_freq, 10.0, places=0)


class TestBiologicalFilter(unittest.TestCase):
    """Test BiologicalFilter class."""
    
    def test_default_filter(self):
        """Test default filter (all-pass)."""
        bio_filter = BiologicalFilter()
        omega = np.linspace(0, 2*np.pi*100, 1000)
        H = bio_filter.frequency_response(omega)
        
        # Default should be all-pass (ones)
        self.assertTrue(np.allclose(H, 1.0))
    
    def test_resonant_filter(self):
        """Test filter with resonant frequencies."""
        bio_filter = BiologicalFilter(
            center_frequencies=[10.0],  # Hz
            bandwidths=[1.0]  # Hz
        )
        
        omega = np.linspace(0, 2*np.pi*100, 10000)
        H = bio_filter.frequency_response(omega)
        
        # Response should peak near 10 Hz
        freqs = omega / (2*np.pi)
        peak_idx = np.argmax(np.abs(H))
        peak_freq = freqs[peak_idx]
        
        self.assertAlmostEqual(peak_freq, 10.0, places=1)
    
    def test_multiple_resonances(self):
        """Test filter with multiple resonant peaks."""
        bio_filter = BiologicalFilter(
            center_frequencies=[10.0, 50.0],  # Hz
            bandwidths=[2.0, 5.0]  # Hz
        )
        
        omega = np.linspace(0, 2*np.pi*100, 10000)
        H = bio_filter.frequency_response(omega)
        
        # Should have non-zero response
        self.assertFalse(np.allclose(H, 0.0))


class TestPhaseAccumulator(unittest.TestCase):
    """Test PhaseAccumulator class."""
    
    def test_phase_accumulation(self):
        """Test basic phase accumulation."""
        phase_acc = PhaseAccumulator(threshold=10.0, memory_alpha=0.1)
        
        # Simple increasing signal
        t = np.linspace(0, 20, 100)
        signal = np.ones(100, dtype=complex)
        
        phase = phase_acc.accumulate_phase(signal, t)
        
        # Phase should increase monotonically
        self.assertTrue(np.all(np.diff(phase) >= 0))
    
    def test_activation_threshold(self):
        """Test activation threshold detection."""
        phase_acc = PhaseAccumulator(threshold=5.0, memory_alpha=0.1)
        
        # Create phase that crosses threshold
        t = np.linspace(0, 10, 100)
        phase = np.linspace(0, 10, 100)
        
        activated, activation_time = phase_acc.check_activation(phase, t)
        
        # Should activate when crossing 5.0
        self.assertTrue(activated)
        self.assertIsNotNone(activation_time)
        self.assertLess(activation_time, 10.0)
        self.assertGreater(activation_time, 0.0)
    
    def test_no_activation_below_threshold(self):
        """Test that no activation occurs below threshold."""
        phase_acc = PhaseAccumulator(threshold=10.0, memory_alpha=0.1)
        
        t = np.linspace(0, 10, 100)
        phase = np.linspace(0, 5, 100)  # Max phase = 5 < threshold
        
        activated, activation_time = phase_acc.check_activation(phase, t)
        
        self.assertFalse(activated)
        self.assertIsNone(activation_time)
    
    def test_phase_memory(self):
        """Test phase memory retention."""
        phase_acc = PhaseAccumulator(threshold=10.0, memory_alpha=0.1)
        
        # First phase
        phase1 = np.array([1.0, 2.0, 3.0])
        phase_acc.phase_history.append(phase1)
        
        # Second phase (with memory applied)
        phase2 = np.array([2.0, 3.0, 4.0])
        memorized = phase_acc.apply_memory(phase2)
        
        # Memorized should be weighted average
        expected = 0.1 * phase2 + 0.9 * phase1
        np.testing.assert_array_almost_equal(memorized, expected)


class TestQCALBiologicalSystem(unittest.TestCase):
    """Test complete QCAL biological system."""
    
    def test_system_creation(self):
        """Test creating complete system."""
        env_field = create_annual_cycle_field()
        bio_filter = create_cicada_filter(prime_period=17)
        phase_acc = PhaseAccumulator(threshold=17.0, memory_alpha=0.1)
        
        system = QCALBiologicalSystem(env_field, bio_filter, phase_acc)
        
        self.assertIsNotNone(system)
        self.assertEqual(system.env_field, env_field)
        self.assertEqual(system.bio_filter, bio_filter)
        self.assertEqual(system.phase_accumulator, phase_acc)
    
    def test_system_simulation(self):
        """Test running simulation."""
        env_field = create_annual_cycle_field()
        bio_filter = create_cicada_filter(prime_period=13)
        phase_acc = PhaseAccumulator(threshold=5.0, memory_alpha=0.1)
        
        system = QCALBiologicalSystem(env_field, bio_filter, phase_acc)
        
        # Simulate 10 years
        t = np.linspace(0, 10 * 365 * 24 * 3600, 1000)
        results = system.simulate(t, apply_memory=True)
        
        # Check results structure
        self.assertIn('time', results)
        self.assertIn('environmental_field', results)
        self.assertIn('filtered_field', results)
        self.assertIn('phase', results)
        self.assertIn('activated', results)
        self.assertIn('activation_time', results)
        
        # Results should have correct shapes
        self.assertEqual(len(results['environmental_field']), len(t))
        self.assertEqual(len(results['phase']), len(t))


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_create_annual_cycle_field(self):
        """Test creating annual cycle field."""
        field = create_annual_cycle_field(f0=141.7001)
        
        # Should have multiple components
        self.assertGreater(len(field.components), 0)
        
        # Should include QCAL frequency
        has_qcal = any("141.7001" in comp.description or "QCAL" in comp.description 
                      for comp in field.components)
        self.assertTrue(has_qcal)
    
    def test_create_cicada_filter(self):
        """Test creating cicada filter."""
        filter_13 = create_cicada_filter(prime_period=13)
        filter_17 = create_cicada_filter(prime_period=17)
        
        # Should have resonant frequencies
        self.assertGreater(len(filter_13.center_frequencies), 0)
        self.assertGreater(len(filter_17.center_frequencies), 0)
        
        # Different periods should have different filters
        self.assertNotEqual(filter_13.center_frequencies, filter_17.center_frequencies)


class TestMathematicalConsistency(unittest.TestCase):
    """Test mathematical consistency of QCAL framework."""
    
    def test_spectral_field_linearity(self):
        """Test linearity of spectral field superposition."""
        field1 = EnvironmentalSpectralField()
        field1.add_component(amplitude=1.0, frequency=2*np.pi, phase=0.0)
        
        field2 = EnvironmentalSpectralField()
        field2.add_component(amplitude=2.0, frequency=2*np.pi, phase=0.0)
        
        field_combined = EnvironmentalSpectralField()
        field_combined.add_component(amplitude=3.0, frequency=2*np.pi, phase=0.0)
        
        t = np.linspace(0, 1, 100)
        
        psi1 = field1.evaluate(t)
        psi2 = field2.evaluate(t)
        psi_combined = field_combined.evaluate(t)
        
        # Linearity: ψ₁ + ψ₂ = ψ_combined
        np.testing.assert_array_almost_equal(psi1 + psi2, psi_combined)
    
    def test_phase_monotonicity(self):
        """Test that phase accumulation is monotonically increasing."""
        phase_acc = PhaseAccumulator(threshold=10.0, memory_alpha=0.1)
        
        t = np.linspace(0, 20, 100)
        signal = np.ones(100, dtype=complex) * 0.5  # Constant positive signal
        
        phase = phase_acc.accumulate_phase(signal, t)
        
        # Phase should increase monotonically (or stay constant)
        differences = np.diff(phase)
        self.assertTrue(np.all(differences >= -1e-10))  # Allow tiny numerical errors
    
    def test_frequency_conservation(self):
        """Test frequency conservation in spectral analysis."""
        # Create field with known frequency
        field = EnvironmentalSpectralField()
        f_test = 5.0  # Hz
        field.add_component(amplitude=1.0, frequency=2*np.pi*f_test, phase=0.0)
        
        # Sample at Nyquist rate
        fs = 20.0  # Hz (> 2 * f_test)
        t = np.linspace(0, 10, int(10 * fs))
        
        freqs, power = field.power_spectrum(t)
        
        # Peak should be at f_test
        peak_idx = np.argmax(power)
        peak_freq = freqs[peak_idx]
        
        # Allow 10% tolerance due to discretization
        self.assertAlmostEqual(peak_freq, f_test, delta=f_test * 0.1)


# ============================================================================
# Test Runner
# ============================================================================

def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSpectralComponent))
    suite.addTests(loader.loadTestsFromTestCase(TestEnvironmentalSpectralField))
    suite.addTests(loader.loadTestsFromTestCase(TestBiologicalFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseAccumulator))
    suite.addTests(loader.loadTestsFromTestCase(TestQCALBiologicalSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestMathematicalConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("QCAL Biological Framework - Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
