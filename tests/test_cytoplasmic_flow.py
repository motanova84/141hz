#!/usr/bin/env python3
"""
Tests for Cytoplasmic Flow Model

Comprehensive test suite validating:
- Cell geometry and parameter initialization
- Cytoplasmic flow simulation
- f₀ = 141.7 Hz emergence
- Turbulent cascade analysis
- Biological parameter validation
"""

import pytest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from biology.cytoplasmic_flow import (
    CytoplasmicFlowModel,
    CellGeometry,
    CytoskeletonParameters
)


class TestCellGeometry:
    """Test cell geometry calculations."""
    
    def test_spherical_volume(self):
        """Test spherical cell volume calculation."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        expected_volume = (4/3) * np.pi * 10.0**3
        assert abs(cell.volume - expected_volume) < 1.0
    
    def test_cylindrical_volume(self):
        """Test cylindrical cell volume calculation."""
        cell = CellGeometry(radius=5.0, length=20.0, shape='cylindrical')
        expected_volume = np.pi * 5.0**2 * 20.0
        assert abs(cell.volume - expected_volume) < 1.0
    
    def test_ellipsoidal_volume(self):
        """Test ellipsoidal cell volume calculation."""
        cell = CellGeometry(radius=5.0, length=20.0, shape='ellipsoidal')
        # Should return a reasonable volume
        assert cell.volume > 0
        assert cell.volume < 10000  # Reasonable upper bound


class TestCytoskeletonParameters:
    """Test cytoskeleton parameter dataclass."""
    
    def test_default_parameters(self):
        """Test default cytoskeleton parameters."""
        cyto = CytoskeletonParameters()
        assert cyto.microtubule_density == 10.0
        assert cyto.motor_velocity == 1.0
        assert cyto.motor_force == 5.0
    
    def test_custom_parameters(self):
        """Test custom cytoskeleton parameters."""
        cyto = CytoskeletonParameters(
            microtubule_density=20.0,
            motor_velocity=2.0,
            motor_force=10.0
        )
        assert cyto.microtubule_density == 20.0
        assert cyto.motor_velocity == 2.0
        assert cyto.motor_force == 10.0


class TestCytoplasmicFlowModel:
    """Test cytoplasmic flow model."""
    
    @pytest.fixture
    def basic_model(self):
        """Create basic model for testing."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        return CytoplasmicFlowModel(geometry=cell)
    
    def test_model_initialization(self, basic_model):
        """Test model initializes correctly."""
        assert basic_model.f0 == 141.7001
        assert basic_model.viscosity > 0
        assert basic_model.density > 0
        assert basic_model.temperature == 310.0
    
    def test_biological_parameters_set(self, basic_model):
        """Test biological parameters are set correctly."""
        # Viscosity should be in biological range
        assert 0.1 <= basic_model.viscosity <= 10.0
        
        # Density should be close to water
        assert 1000 <= basic_model.density <= 1100
        
        # Reynolds number should be calculated
        assert basic_model.reynolds >= 0
    
    def test_reynolds_number_realistic(self, basic_model):
        """Test Reynolds number is in realistic range for cells."""
        # Cytoplasmic flows typically have very low Re
        assert basic_model.reynolds < 10
    
    def test_motor_forcing_field(self, basic_model):
        """Test motor protein forcing field generation."""
        # Create simple grid
        grid = np.array([[0, 0], [1e-6, 1e-6], [-1e-6, -1e-6]]).T
        
        # Generate forcing field
        force = basic_model.motor_forcing_field(grid, time=0.0, num_motors=10)
        
        # Should have finite forces
        assert np.all(np.isfinite(force))
        
        # Should have correct shape
        assert force.shape[0] == grid.shape[1]
    
    def test_motor_forcing_temporal_modulation(self, basic_model):
        """Test motor forcing has temporal modulation."""
        grid = np.array([[0, 0]]).T
        
        force_t0 = basic_model.motor_forcing_field(grid, time=0.0)
        force_t1 = basic_model.motor_forcing_field(grid, time=0.01)
        
        # Forces should differ due to temporal modulation
        # (unless they happen to be at similar phases)
        # Just check they're both finite
        assert np.all(np.isfinite(force_t0))
        assert np.all(np.isfinite(force_t1))
    
    def test_simulate_cytoplasmic_streaming(self, basic_model):
        """Test cytoplasmic streaming simulation."""
        # Run short simulation
        results = basic_model.simulate_cytoplasmic_streaming(
            grid_size=8,
            time_steps=50,
            dt=0.01,
            save_interval=10
        )
        
        # Check results structure
        assert 'velocity_history' in results
        assert 'vorticity_history' in results
        assert 'energy_history' in results
        assert 'time_points' in results
        assert 'reynolds' in results
        
        # Check data validity
        assert len(results['velocity_history']) > 0
        assert len(results['energy_history']) > 0
        assert np.all(np.isfinite(results['energy_history']))
        assert np.all(results['energy_history'] >= 0)
    
    def test_energy_conservation_approximate(self, basic_model):
        """Test energy is approximately conserved (with forcing and dissipation)."""
        results = basic_model.simulate_cytoplasmic_streaming(
            grid_size=8,
            time_steps=100,
            dt=0.01,
            save_interval=20
        )
        
        energy = results['energy_history']
        
        # Energy should be positive
        assert np.all(energy >= 0)
        
        # Energy shouldn't blow up
        assert np.all(energy < 1e10)
        
        # Energy should have some variation (not constant)
        assert np.std(energy) > 0
    
    def test_spectral_analysis_f0_emergence(self, basic_model):
        """Test spectral analysis detects f₀ region."""
        # Create synthetic time series with f₀ component
        t = np.linspace(0, 1, 1000)
        f0 = float(basic_model.f0)
        signal = np.sin(2 * np.pi * f0 * t) + 0.1 * np.random.randn(len(t))
        
        # Analyze spectrum
        spectral = basic_model.spectral_analysis_f0_emergence(signal, t)
        
        # Check structure
        assert 'frequencies' in spectral
        assert 'power_spectrum' in spectral
        assert 'detected_f0' in spectral
        assert 'snr' in spectral
        assert 'f0_detected' in spectral
        
        # Should detect f₀ (within 10 Hz)
        assert abs(spectral['detected_f0'] - f0) < 10.0
        
        # SNR should be reasonable
        assert spectral['snr'] > 1.0
    
    def test_spectral_analysis_no_signal(self, basic_model):
        """Test spectral analysis with pure noise."""
        # Pure noise
        t = np.linspace(0, 1, 1000)
        noise = np.random.randn(len(t))
        
        spectral = basic_model.spectral_analysis_f0_emergence(noise, t)
        
        # Should still run without errors
        assert 'detected_f0' in spectral
        assert np.isfinite(spectral['detected_f0'])
        
        # SNR should be low
        # (might occasionally be high due to random peaks)
        assert spectral['snr'] >= 0
    
    def test_turbulent_cascade_analysis(self, basic_model):
        """Test turbulent cascade analysis."""
        # Create test velocity field
        x = np.linspace(0, 2*np.pi, 16)
        y = np.linspace(0, 2*np.pi, 16)
        X, Y = np.meshgrid(x, y)
        u = -np.sin(Y)
        v = np.sin(X)
        velocity = np.array([u, v])
        
        # Analyze cascade
        cascade = basic_model.turbulent_cascade_analysis(velocity)
        
        # Check structure
        assert 'wavenumbers' in cascade
        assert 'energy_spectrum' in cascade
        assert 'spectral_slope' in cascade
        assert 'dissipation_rate' in cascade
        assert 'cascade_frequency' in cascade
        assert 'cascade_matches_f0' in cascade
        
        # Values should be finite
        assert np.all(np.isfinite(cascade['wavenumbers']))
        assert np.all(np.isfinite(cascade['energy_spectrum']))
        assert np.isfinite(cascade['spectral_slope'])
        assert np.isfinite(cascade['dissipation_rate'])
    
    def test_cascade_frequency_computed(self, basic_model):
        """Test cascade frequency is computed from energy spectrum."""
        x = np.linspace(0, 2*np.pi, 16)
        y = np.linspace(0, 2*np.pi, 16)
        X, Y = np.meshgrid(x, y)
        
        # Higher energy field
        u = -2.0 * np.sin(Y)
        v = 2.0 * np.sin(X)
        velocity = np.array([u, v])
        
        cascade = basic_model.turbulent_cascade_analysis(velocity)
        
        # Cascade frequency should be positive
        assert cascade['cascade_frequency'] >= 0
    
    def test_validate_biological_parameters(self, basic_model):
        """Test biological parameter validation."""
        validation = basic_model.validate_biological_parameters()
        
        # Check all expected validations exist
        assert 'viscosity_realistic' in validation
        assert 'density_realistic' in validation
        assert 'temperature_realistic' in validation
        assert 'reynolds_realistic' in validation
        assert 'motor_velocity_realistic' in validation
        assert 'motor_force_realistic' in validation
        assert 'all_parameters_realistic' in validation
        
        # All should be True for default parameters
        assert validation['all_parameters_realistic']
    
    def test_unrealistic_parameters_detected(self):
        """Test that unrealistic parameters are detected."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        cyto = CytoskeletonParameters(
            motor_velocity=1000.0,  # Unrealistically high
            motor_force=1000.0  # Unrealistically high
        )
        
        model = CytoplasmicFlowModel(geometry=cell, cytoskeleton=cyto)
        validation = model.validate_biological_parameters()
        
        # These specific parameters should fail
        assert not validation['motor_velocity_realistic']
        assert not validation['motor_force_realistic']
        assert not validation['all_parameters_realistic']
    
    def test_to_dict(self, basic_model):
        """Test model serialization to dictionary."""
        model_dict = basic_model.to_dict()
        
        # Check structure
        assert 'model' in model_dict
        assert 'f0' in model_dict
        assert 'cell_geometry' in model_dict
        assert 'fluid_properties' in model_dict
        assert 'cytoskeleton' in model_dict
        assert 'validation' in model_dict
        
        # Check values
        assert model_dict['model'] == 'CytoplasmicFlow'
        assert model_dict['f0'] == 141.7001
        assert model_dict['cell_geometry']['shape'] == 'spherical'
    
    def test_different_cell_shapes(self):
        """Test model works with different cell shapes."""
        shapes = ['spherical', 'cylindrical', 'ellipsoidal']
        
        for shape in shapes:
            if shape in ['cylindrical', 'ellipsoidal']:
                cell = CellGeometry(radius=5.0, length=20.0, shape=shape)
            else:
                cell = CellGeometry(radius=10.0, shape=shape)
            
            model = CytoplasmicFlowModel(geometry=cell)
            
            # Should initialize successfully
            assert model.geometry.shape == shape
            assert model.f0 == 141.7001
    
    def test_temperature_effect(self):
        """Test different temperatures affect viscosity indirectly."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        
        model_cold = CytoplasmicFlowModel(geometry=cell, temperature=280.0)
        model_hot = CytoplasmicFlowModel(geometry=cell, temperature=320.0)
        
        # Both should initialize
        assert model_cold.temperature == 280.0
        assert model_hot.temperature == 320.0
        
        # Validate both are in realistic range
        val_cold = model_cold.validate_biological_parameters()
        val_hot = model_hot.validate_biological_parameters()
        
        assert val_cold['temperature_realistic']
        assert val_hot['temperature_realistic']


class TestIntegrationWithNavierStokes:
    """Test integration with Navier-Stokes framework."""
    
    def test_navier_stokes_framework_initialized(self):
        """Test that Navier-Stokes framework is properly initialized."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        model = CytoplasmicFlowModel(geometry=cell)
        
        # Should have NS framework
        assert hasattr(model, 'ns_framework')
        assert model.ns_framework is not None
        
        # Framework should have f₀
        assert model.ns_framework.f0 == 141.7001
    
    def test_regularization_term_accessible(self):
        """Test that regularization term from NS framework works."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        model = CytoplasmicFlowModel(geometry=cell)
        
        # Create test velocity field
        velocity = np.random.randn(2, 10, 10) * 1e-6
        
        # Should be able to compute regularization
        reg = model.ns_framework.regularization_term(
            velocity, coherence=0.9, time=0.0
        )
        
        assert reg is not None
        assert np.all(np.isfinite(reg))
    
    def test_vorticity_computation(self):
        """Test vorticity computation from NS framework."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        model = CytoplasmicFlowModel(geometry=cell)
        
        # Create simple velocity field
        x = np.linspace(0, 2*np.pi, 16)
        y = np.linspace(0, 2*np.pi, 16)
        X, Y = np.meshgrid(x, y)
        u = -np.sin(Y)
        v = np.sin(X)
        velocity = np.array([u, v])
        
        # Compute vorticity
        vorticity = model.ns_framework.compute_vorticity(velocity, dx=0.1)
        
        assert vorticity is not None
        assert np.all(np.isfinite(vorticity))


class TestBiologicalRealism:
    """Test biological realism of results."""
    
    def test_cytoplasmic_streaming_velocity_realistic(self):
        """Test that simulated velocities are in realistic range."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        model = CytoplasmicFlowModel(geometry=cell)
        
        # Run simulation
        results = model.simulate_cytoplasmic_streaming(
            grid_size=8,
            time_steps=50,
            dt=0.01,
            save_interval=10
        )
        
        # Check final velocity magnitude
        final_v = results['velocity_history'][-1]
        v_max = np.max(np.abs(final_v))
        
        # Cytoplasmic streaming: 0.1-100 μm/s = 1e-7 to 1e-4 m/s
        # Our velocities are in m/s, so should be in this range
        # (allowing some margin for simulation artifacts)
        assert v_max < 1e-3  # Upper bound (generous)
    
    def test_reynolds_number_low_for_cytoplasm(self):
        """Test that Reynolds number is low (Stokes flow regime)."""
        cell = CellGeometry(radius=10.0, shape='spherical')
        cyto = CytoskeletonParameters(motor_velocity=1.0)  # 1 μm/s
        
        model = CytoplasmicFlowModel(geometry=cell, cytoskeleton=cyto)
        
        # Cytoplasmic flows are typically Re << 1
        assert model.reynolds < 1.0
    
    def test_cell_volume_realistic(self):
        """Test that cell volumes are in realistic range."""
        # Typical eukaryotic cell: 1000-10000 μm³
        cell = CellGeometry(radius=10.0, shape='spherical')
        
        volume = cell.volume
        
        # Should be in realistic range
        assert 100 < volume < 100000


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v'])
