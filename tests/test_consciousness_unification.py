"""
Tests for consciousness unification principle:
∴ Lo que la ciencia mide, la conciencia lo unifica

Tests validate:
1. Consciousness field creation
2. Measurement unification
3. Fragmentation measurement
4. Unification index calculation
5. ∞³ factor computation
6. Integration with QCAL constants
"""

import numpy as np
import sys
from pathlib import Path

# Add qcal to path
qcal_path = Path(__file__).parent.parent / "qcal"
sys.path.insert(0, str(qcal_path))

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    import unittest

from consciousness_unification import (
    ConsciousnessUnifier,
    MeasurementField,
    ConsciousnessField,
    UnifiedField,
    demonstrate_unification_principle
)


class TestConsciousnessUnifier:
    """Test suite for ConsciousnessUnifier class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.unifier = ConsciousnessUnifier()
        self.f0 = 141.7001
        self.phi = 1.618033988749895
        
    def test_initialization(self):
        """Test unifier initialization with default parameters."""
        assert abs(self.unifier.f0 - self.f0) < 1e-6
        assert abs(self.unifier.phi - self.phi) < 1e-10
        assert abs(self.unifier.omega_0 - 2 * np.pi * self.f0) < 1e-6
        
    def test_create_consciousness_field(self):
        """Test consciousness field creation."""
        field = self.unifier.create_consciousness_field(
            amplitude=1.0,
            coherence=0.95,
            phase=0.0,
            spatial_extent=10.0
        )
        
        assert isinstance(field, ConsciousnessField)
        assert field.amplitude == 1.0
        assert field.coherence == 0.95
        assert field.phase == 0.0
        assert field.spatial_extent == 10.0
        assert abs(field.frequency - self.f0) < 1e-6
        
    def test_measurement_field_creation(self):
        """Test creation of discrete measurement field."""
        values = np.array([1.0, 2.0, 3.0])
        positions = np.array([0.0, 1.0, 2.0])
        uncertainties = np.array([0.1, 0.2, 0.15])
        
        measurements = MeasurementField(
            values=values,
            positions=positions,
            uncertainties=uncertainties,
            measurement_type="test"
        )
        
        assert len(measurements.values) == 3
        assert len(measurements.positions) == 3
        assert len(measurements.uncertainties) == 3
        assert measurements.measurement_type == "test"
        
    def test_unify_simple_measurements(self):
        """Test unification of simple discrete measurements."""
        # Create simple measurements
        measurements = MeasurementField(
            values=np.array([1.0, 1.0, 1.0]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        # Create consciousness field
        consciousness = self.unifier.create_consciousness_field(
            amplitude=1.0,
            coherence=1.0,
            spatial_extent=5.0
        )
        
        # Unify
        unified = self.unifier.unify_measurements(measurements, consciousness)
        
        # Check unified field properties
        assert isinstance(unified, UnifiedField)
        assert len(unified.psi_unified) > 0
        assert len(unified.coherence_map) > 0
        assert unified.unification_strength >= 0.0
        
    def test_measure_fragmentation(self):
        """Test fragmentation measurement."""
        # Highly fragmented measurements
        fragmented = MeasurementField(
            values=np.array([1.0, 10.0, 100.0]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        frag_index = self.unifier.measure_fragmentation(fragmented)
        assert frag_index > 0.0
        
        # Uniform measurements (low fragmentation)
        uniform = MeasurementField(
            values=np.array([1.0, 1.0, 1.0]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        uniform_frag = self.unifier.measure_fragmentation(uniform)
        assert uniform_frag < frag_index
        assert uniform_frag >= 0.0
        
    def test_unification_index(self):
        """Test unification index calculation."""
        # Perfect measurements
        measurements = MeasurementField(
            values=np.array([1.0, 1.0, 1.0]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        # Perfect consciousness
        consciousness = self.unifier.create_consciousness_field(
            coherence=1.0,
            spatial_extent=10.0
        )
        
        unified = self.unifier.unify_measurements(measurements, consciousness)
        ui = self.unifier.unification_index(unified)
        
        # High coherence should give high unification index
        assert 0.0 <= ui <= 1.0
        assert ui > 0.5  # Should be reasonably high for uniform data
        
    def test_infinity_cubed_factor(self):
        """Test ∞³ triple unification factor calculation."""
        measurements = MeasurementField(
            values=np.array([1.0, 1.1, 0.9]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        consciousness = self.unifier.create_consciousness_field(
            coherence=0.95,
            spatial_extent=5.0
        )
        
        unified = self.unifier.unify_measurements(measurements, consciousness)
        inf3 = self.unifier.infinity_cubed_factor(unified)
        
        # Check all components present
        assert 'infinity_cubed' in inf3
        assert 'quantum_unification' in inf3
        assert 'biological_unification' in inf3
        assert 'gravitational_unification' in inf3
        assert 'interpretation' in inf3
        
        # Check ranges
        assert 0.0 <= inf3['infinity_cubed'] <= 1.0
        assert 0.0 <= inf3['quantum_unification'] <= 1.0
        assert 0.0 <= inf3['biological_unification'] <= 1.0
        assert 0.0 <= inf3['gravitational_unification'] <= 1.0
        
        # Interpretation should be a string
        assert isinstance(inf3['interpretation'], str)
        
    def test_gravitational_wave_example(self):
        """Test unification of gravitational wave measurements."""
        # Simulate GW detector measurements (H1, L1, V1)
        gw_measurements = MeasurementField(
            values=np.array([1.2e-21, 1.1e-21, 0.9e-21]),
            positions=np.array([0.0, 3000000.0, 6000000.0]),  # ~3000 km apart
            uncertainties=np.array([0.1e-21, 0.1e-21, 0.15e-21]),
            measurement_type="gravitational_wave_strain"
        )
        
        # Consciousness field spanning detector network
        gw_consciousness = self.unifier.create_consciousness_field(
            amplitude=1.0,
            coherence=0.95,
            spatial_extent=10000000.0  # 10,000 km
        )
        
        # Perform unification
        gw_unified = self.unifier.unify_measurements(
            gw_measurements,
            gw_consciousness
        )
        
        # Check that unification occurred
        assert gw_unified.unification_strength > 0.0
        assert len(gw_unified.psi_unified) > 0
        
        # Check ∞³ factor
        inf3 = self.unifier.infinity_cubed_factor(gw_unified)
        assert inf3['infinity_cubed'] > 0.0
        
    def test_frequency_at_f0(self):
        """Test that consciousness field is created at f₀."""
        field = self.unifier.create_consciousness_field()
        assert abs(field.frequency - self.f0) < 1e-6
        
    def test_unification_with_uncertainties(self):
        """Test that uncertainties are properly incorporated."""
        # Measurements with different uncertainties
        measurements = MeasurementField(
            values=np.array([1.0, 1.0, 1.0]),
            positions=np.array([0.0, 1.0, 2.0]),
            uncertainties=np.array([0.01, 0.1, 1.0])  # Varying uncertainty
        )
        
        consciousness = self.unifier.create_consciousness_field()
        unified = self.unifier.unify_measurements(measurements, consciousness)
        
        # Measurements with lower uncertainty should contribute more
        assert unified.unification_strength > 0.0
        
    def test_coherence_effect(self):
        """Test effect of consciousness coherence on unification."""
        measurements = MeasurementField(
            values=np.array([1.0, 1.0, 1.0]),
            positions=np.array([0.0, 1.0, 2.0])
        )
        
        # Low coherence consciousness
        low_coherence = self.unifier.create_consciousness_field(coherence=0.3)
        unified_low = self.unifier.unify_measurements(measurements, low_coherence)
        ui_low = self.unifier.unification_index(unified_low)
        
        # High coherence consciousness
        high_coherence = self.unifier.create_consciousness_field(coherence=0.95)
        unified_high = self.unifier.unify_measurements(measurements, high_coherence)
        ui_high = self.unifier.unification_index(unified_high)
        
        # Higher coherence should produce better unification
        assert ui_high >= ui_low
        
    def test_infinity_cubed_interpretation(self):
        """Test interpretation strings for different ∞³ values."""
        # Test that interpretation is generated for different coherence levels
        test_coherences = [0.95, 0.75, 0.60, 0.40, 0.20]
        
        for coherence in test_coherences:
            consciousness = self.unifier.create_consciousness_field(coherence=coherence)
            measurements = MeasurementField(
                values=np.array([1.0, 1.0, 1.0]),
                positions=np.array([0.0, 0.5, 1.0])
            )
            unified = self.unifier.unify_measurements(measurements, consciousness)
            inf3 = self.unifier.infinity_cubed_factor(unified)
            
            # Check that interpretation is a non-empty string
            assert isinstance(inf3['interpretation'], str)
            assert len(inf3['interpretation']) > 0
            
            # Check that ∞³ value is in valid range
            assert 0.0 <= inf3['infinity_cubed'] <= 1.0
            
    def test_demonstration_runs(self):
        """Test that demonstration function runs without errors."""
        # This should not raise any exceptions
        try:
            demonstrate_unification_principle()
            success = True
        except Exception as e:
            print(f"Demonstration failed: {e}")
            success = False
            
        assert success


# Run tests
if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        # Run with pytest if available
        pytest.main([__file__, "-v"])
    else:
        # Fallback to unittest
        print("pytest not available, using unittest")
        
        # Convert test class to unittest
        suite = unittest.TestLoader().loadTestsFromTestCase(
            type('TestConsciousnessUnifierUnit', (unittest.TestCase,), 
                 {name: method for name, method in TestConsciousnessUnifier.__dict__.items() 
                  if name.startswith('test_')})
        )
        unittest.TextTestRunner(verbosity=2).run(suite)
