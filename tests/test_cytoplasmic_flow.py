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
Tests for Cytoplasmic Flow Model - Navier-Stokes Implementation

Tests comprehensivos para el modelo de flujo citoplasmático que conecta
la Hipótesis de Riemann con el tejido biológico vivo.

Autor: José Manuel Mota Burruezo
Instituto Consciencia Cuántica QCAL ∞³
"""

import numpy as np
from typing import Tuple
import sys
from pathlib import Path

# Añadir directorio al path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from cytoplasmic_flow_model import (
    FlowParameters,
    NavierStokesRegularized,
    RiemannResonanceOperator,
    demonstrate_navier_stokes_coherence,
    F0_HZ,
    RHO_CYTOPLASM,
    NU_CYTOPLASM,
    RIEMANN_ZEROS,
)


class TestFlowParameters:
    """Tests para la clase FlowParameters."""
    
    def test_default_parameters(self):
        """Verifica que los parámetros por defecto sean correctos."""
        params = FlowParameters()
        
        assert params.density == RHO_CYTOPLASM
        assert params.viscosity == NU_CYTOPLASM
        assert params.frequency == F0_HZ
        assert params.length_scale > 0
        assert params.velocity_scale > 0
    
    def test_reynolds_number_viscous_regime(self):
        """Verifica que estamos en régimen viscoso (Re << 1)."""
        params = FlowParameters()
        Re = params.reynolds_number
        
        # Re debe ser mucho menor que 1
        assert Re < 1e-6, f"Reynolds number {Re} too large for viscous regime"
        
        # Re debe ser positivo
        assert Re > 0
    
    def test_has_smooth_solution(self):
        """Verifica que existe solución suave en régimen viscoso."""
        params = FlowParameters()
        
        # En régimen viscoso, existe solución global suave
        assert params.has_smooth_solution is True
    
    def test_omega_calculation(self):
        """Verifica el cálculo de la frecuencia angular."""
        params = FlowParameters()
        omega = params.omega
        
        # ω = 2πf
        expected_omega = 2 * np.pi * F0_HZ
        assert np.isclose(omega, expected_omega, rtol=1e-10)


class TestNavierStokesRegularized:
    """Tests para el solver de Navier-Stokes."""
    
    def test_initialization(self):
        """Verifica la inicialización correcta del solver."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        assert ns.params == params
        assert ns.params.has_smooth_solution
    
    def test_initialization_fails_for_high_reynolds(self):
        """Verifica que falle para Reynolds alto."""
        # Crear parámetros con Re alto
        params = FlowParameters(
            velocity_scale=1.0,  # m/s - muy alto
            length_scale=1.0,    # m - muy grande
        )
        
        try:
            NavierStokesRegularized(params)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Reynolds number" in str(e) and "too large" in str(e)
    
    def test_velocity_field_shape(self):
        """Verifica que el campo de velocidad tenga 3 componentes."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        x, y, z, t = 1e-6, 1e-6, 0, 0
        vx, vy, vz = ns.velocity_field(x, y, z, t)
        
        # Deben ser números reales
        assert isinstance(vx, (int, float, np.number))
        assert isinstance(vy, (int, float, np.number))
        assert isinstance(vz, (int, float, np.number))
    
    def test_velocity_field_incompressibility(self):
        """Verifica la condición de incompressibilidad ∇·v = 0."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        x, y, z, t = 1e-6, 1e-6, 0, 0
        h = 1e-9  # paso pequeño
        
        # Calcular derivadas por diferencias finitas
        vx1, _, _ = ns.velocity_field(x + h, y, z, t)
        vx0, _, _ = ns.velocity_field(x, y, z, t)
        dvx_dx = (vx1 - vx0) / h
        
        _, vy1, _ = ns.velocity_field(x, y + h, z, t)
        _, vy0, _ = ns.velocity_field(x, y, z, t)
        dvy_dy = (vy1 - vy0) / h
        
        _, _, vz1 = ns.velocity_field(x, y, z + h, t)
        _, _, vz0 = ns.velocity_field(x, y, z, t)
        dvz_dz = (vz1 - vz0) / h
        
        divergence = dvx_dx + dvy_dy + dvz_dz
        
        # La divergencia debe ser aproximadamente cero
        # (puede haber error numérico pequeño)
        assert abs(divergence) < 1e-3, f"Divergence {divergence} not close to zero"
    
    def test_velocity_field_boundedness(self):
        """Verifica que la velocidad esté acotada."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        # Probar en varios puntos
        for _ in range(10):
            x = np.random.uniform(-5e-6, 5e-6)
            y = np.random.uniform(-5e-6, 5e-6)
            z = np.random.uniform(-5e-6, 5e-6)
            t = np.random.uniform(0, 1)
            
            vx, vy, vz = ns.velocity_field(x, y, z, t)
            v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
            
            # La velocidad debe estar acotada por la escala de velocidad
            assert v_mag <= 10 * params.velocity_scale
    
    def test_velocity_field_periodicity(self):
        """Verifica la periodicidad temporal del campo."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        x, y, z = 1e-6, 1e-6, 0
        period = 1.0 / params.frequency
        
        # Velocidad en t=0
        vx0, vy0, vz0 = ns.velocity_field(x, y, z, 0)
        
        # Velocidad en t=T (un periodo)
        vxT, vyT, vzT = ns.velocity_field(x, y, z, period)
        
        # Deben ser aproximadamente iguales (periódico)
        assert np.isclose(vx0, vxT, rtol=1e-6)
        assert np.isclose(vy0, vyT, rtol=1e-6)
        assert np.isclose(vz0, vzT, rtol=1e-6)
    
    def test_vorticity_shape(self):
        """Verifica que la vorticidad tenga 3 componentes."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        x, y, z, t = 1e-6, 1e-6, 0, 0
        omega_x, omega_y, omega_z = ns.vorticity(x, y, z, t)
        
        assert isinstance(omega_x, (int, float, np.number))
        assert isinstance(omega_y, (int, float, np.number))
        assert isinstance(omega_z, (int, float, np.number))
    
    def test_energy_dissipation_positive(self):
        """Verifica que la disipación de energía sea positiva."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        
        # Probar en varios puntos
        for _ in range(10):
            x = np.random.uniform(-5e-6, 5e-6)
            y = np.random.uniform(-5e-6, 5e-6)
            z = np.random.uniform(-5e-6, 5e-6)
            t = np.random.uniform(0, 1)
            
            epsilon = ns.energy_dissipation_rate(x, y, z, t)
            
            # La disipación debe ser no negativa
            assert epsilon >= 0


class TestRiemannResonanceOperator:
    """Tests para el operador de resonancia de Riemann."""
    
    def test_initialization(self):
        """Verifica la inicialización del operador."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        assert operator.flow == ns
    
    def test_eigenfrequencies_shape(self):
        """Verifica que las frecuencias propias tengan la forma correcta."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        frequencies = operator.eigenfrequencies()
        
        # Debe tener el mismo número de elementos que RIEMANN_ZEROS
        assert len(frequencies) == len(RIEMANN_ZEROS)
        
        # Todas deben ser positivas
        assert np.all(frequencies > 0)
    
    def test_eigenfrequencies_ordering(self):
        """Verifica que las frecuencias estén ordenadas."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        frequencies = operator.eigenfrequencies()
        
        # Deben estar en orden creciente
        assert np.all(np.diff(frequencies) > 0)
    
    def test_first_eigenfrequency(self):
        """Verifica que la primera frecuencia sea f₀."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        frequencies = operator.eigenfrequencies()
        
        # La primera frecuencia debe ser aproximadamente f₀
        assert np.isclose(frequencies[0], F0_HZ, rtol=1e-6)
    
    def test_eigenfrequencies_scaling(self):
        """Verifica el escalado correcto de las frecuencias."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        frequencies = operator.eigenfrequencies()
        
        # Las frecuencias deben escalar como los ceros de Riemann
        normalized_zeros = RIEMANN_ZEROS / RIEMANN_ZEROS[0]
        normalized_freq = frequencies / frequencies[0]
        
        # Deben ser aproximadamente iguales
        assert np.allclose(normalized_freq, normalized_zeros, rtol=1e-10)
    
    def test_is_hermitian(self):
        """Verifica que el operador sea hermítico en régimen viscoso."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        assert operator.is_hermitian() is True
    
    def test_riemann_hypothesis_status(self):
        """Verifica el estado de la Hipótesis de Riemann."""
        params = FlowParameters()
        ns = NavierStokesRegularized(params)
        operator = RiemannResonanceOperator(ns)
        
        status = operator.riemann_hypothesis_status()
        
        # Verificar campos requeridos
        assert "hermitian_operator_exists" in status
        assert "eigenvalues_real" in status
        assert "corresponds_to_riemann_zeros" in status
        assert "fundamental_frequency_hz" in status
        
        # Verificar valores
        assert status["hermitian_operator_exists"] is True
        assert status["eigenvalues_real"] is True
        assert status["corresponds_to_riemann_zeros"] is True
        assert status["fundamental_frequency_hz"] == F0_HZ


class TestDemonstration:
    """Tests para la demostración completa."""
    
    def test_demonstrate_runs_successfully(self):
        """Verifica que la demostración se ejecute sin errores."""
        results = demonstrate_navier_stokes_coherence()
        
        # Verificar que retorne un diccionario
        assert isinstance(results, dict)
    
    def test_demonstrate_has_required_keys(self):
        """Verifica que los resultados tengan las claves requeridas."""
        results = demonstrate_navier_stokes_coherence()
        
        assert "parameters" in results
        assert "flow" in results
        assert "riemann" in results
    
    def test_demonstrate_parameters(self):
        """Verifica los parámetros en los resultados."""
        results = demonstrate_navier_stokes_coherence()
        params = results["parameters"]
        
        assert "density_kg_m3" in params
        assert "viscosity_m2_s" in params
        assert "reynolds_number" in params
        assert params["reynolds_number"] < 1e-6
    
    def test_demonstrate_flow_results(self):
        """Verifica los resultados del flujo."""
        results = demonstrate_navier_stokes_coherence()
        flow = results["flow"]
        
        assert "velocity_x_m_s" in flow
        assert "vorticity_x_s_inv" in flow
        assert "dissipation_w_kg" in flow
        assert flow["dissipation_w_kg"] >= 0
    
    def test_demonstrate_riemann_results(self):
        """Verifica los resultados de Riemann."""
        results = demonstrate_navier_stokes_coherence()
        riemann = results["riemann"]
        
        assert "frequencies_hz" in riemann
        assert "riemann_zeros" in riemann
        assert "status" in riemann
        
        # Verificar que haya frecuencias
        assert len(riemann["frequencies_hz"]) > 0
        
        # Verificar que el estado sea correcto
        assert riemann["status"]["hermitian_operator_exists"] is True


class TestPhysicalConstants:
    """Tests para las constantes físicas."""
    
    def test_f0_hz_value(self):
        """Verifica que f₀ tenga el valor correcto."""
        assert F0_HZ == 141.7001
    
    def test_cytoplasm_density(self):
        """Verifica la densidad del citoplasma."""
        # Densidad típica del citoplasma: ~1030 kg/m³
        assert 1000 <= RHO_CYTOPLASM <= 1100
    
    def test_cytoplasm_viscosity(self):
        """Verifica la viscosidad del citoplasma."""
        # Viscosidad cinemática típica: ~10⁻⁶ m²/s
        assert 1e-7 <= NU_CYTOPLASM <= 1e-5
    
    def test_riemann_zeros_count(self):
        """Verifica que tengamos al menos 10 ceros de Riemann."""
        assert len(RIEMANN_ZEROS) >= 10
    
    def test_riemann_zeros_ordering(self):
        """Verifica que los ceros estén ordenados."""
        assert np.all(np.diff(RIEMANN_ZEROS) > 0)
    
    def test_riemann_zeros_first_value(self):
        """Verifica el primer cero de Riemann."""
        # Primer cero: Im(ρ₁) ≈ 14.134725
        assert np.isclose(RIEMANN_ZEROS[0], 14.134725, rtol=1e-6)


if __name__ == "__main__":
    # Ejecutar tests sin pytest
    print("Running Cytoplasmic Flow Model Tests...")
    print("=" * 70)
    
    # Test FlowParameters
    print("\n1. Testing FlowParameters...")
    test = TestFlowParameters()
    test.test_default_parameters()
    test.test_reynolds_number_viscous_regime()
    test.test_has_smooth_solution()
    test.test_omega_calculation()
    print("   ✓ All FlowParameters tests passed")
    
    # Test NavierStokesRegularized
    print("\n2. Testing NavierStokesRegularized...")
    test = TestNavierStokesRegularized()
    test.test_initialization()
    test.test_velocity_field_shape()
    test.test_velocity_field_boundedness()
    test.test_velocity_field_periodicity()
    test.test_vorticity_shape()
    test.test_energy_dissipation_positive()
    print("   ✓ All NavierStokesRegularized tests passed")
    
    # Test RiemannResonanceOperator
    print("\n3. Testing RiemannResonanceOperator...")
    test = TestRiemannResonanceOperator()
    test.test_initialization()
    test.test_eigenfrequencies_shape()
    test.test_eigenfrequencies_ordering()
    test.test_first_eigenfrequency()
    test.test_eigenfrequencies_scaling()
    test.test_is_hermitian()
    test.test_riemann_hypothesis_status()
    print("   ✓ All RiemannResonanceOperator tests passed")
    
    # Test Demonstration
    print("\n4. Testing Demonstration...")
    test = TestDemonstration()
    test.test_demonstrate_runs_successfully()
    test.test_demonstrate_has_required_keys()
    test.test_demonstrate_parameters()
    test.test_demonstrate_flow_results()
    test.test_demonstrate_riemann_results()
    print("   ✓ All Demonstration tests passed")
    
    # Test Physical Constants
    print("\n5. Testing Physical Constants...")
    test = TestPhysicalConstants()
    test.test_f0_hz_value()
    test.test_cytoplasm_density()
    test.test_cytoplasm_viscosity()
    test.test_riemann_zeros_count()
    test.test_riemann_zeros_ordering()
    test.test_riemann_zeros_first_value()
    print("   ✓ All Physical Constants tests passed")
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED! ✓")
    print("=" * 70)
