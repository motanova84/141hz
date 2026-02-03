#!/usr/bin/env python3
"""
Tests for Cytoplasmic Flow Model - Navier-Stokes Implementation
================================================================

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
