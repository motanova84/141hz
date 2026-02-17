"""
Tests for Reloj Compton (Compton Clock) - Derivación de f₀

Valida:
1. Cálculos de frecuencia Compton para partículas fundamentales
2. Derivación del factor de escala cósmico K
3. Ecuación maestra y validación de f₀
4. Precisión de los resultados según el problema statement
"""

import sys
from pathlib import Path

# Add parent directory to path to import reloj_compton
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    import unittest

import reloj_compton as rc


class TestComptonFrequencies:
    """Test suite for Compton frequency calculations."""
    
    def test_electron_compton_frequency(self):
        """Test electron Compton frequency calculation."""
        f_c = rc.frecuencia_compton(rc.M_ELECTRON)
        # Expected: ~1.2356e20 Hz
        assert abs(f_c - 1.2355899638e20) < 1e13
        
    def test_proton_compton_frequency(self):
        """Test proton Compton frequency calculation."""
        f_c = rc.frecuencia_compton(rc.M_PROTON)
        # Expected: ~2.2687e23 Hz
        assert abs(f_c - 2.2687318153e23) < 1e16
        
    def test_neutron_compton_frequency(self):
        """Test neutron Compton frequency calculation."""
        f_c = rc.frecuencia_compton(rc.M_NEUTRON)
        # Expected: ~2.2719e23 Hz
        assert abs(f_c - 2.2718590791e23) < 1e16
        
    def test_planck_compton_frequency(self):
        """Test Planck mass Compton frequency calculation."""
        f_c = rc.frecuencia_compton(rc.M_PLANCK)
        # Expected: ~2.952e42 Hz
        assert f_c > 2.9e42
        assert f_c < 3.0e42
        
    def test_compton_wavelength(self):
        """Test Compton wavelength calculation."""
        lambda_c = rc.longitud_onda_compton(rc.M_ELECTRON)
        # Expected: ~2.426e-12 m
        assert abs(lambda_c - 2.4263102387e-12) < 1e-17


class TestCosmicScaleFactor:
    """Test suite for cosmic scale factor K calculation."""
    
    def test_cosmic_scale_factor_value(self):
        """Test that K is approximately 2.44e8."""
        K, detalles = rc.calcular_factor_escala_cosmico()
        
        # K should be approximately 2.44e8
        assert abs(K - 2.44e8) < 1e6
        
        # Verify it's in reasonable range
        assert K > 2.4e8
        assert K < 2.5e8
        
    def test_cosmic_scale_factor_components(self):
        """Test components of cosmic scale factor."""
        K, detalles = rc.calcular_factor_escala_cosmico()
        
        # Test mass ratio
        assert detalles['ratio_masas'] > 2e22
        assert detalles['ratio_masas'] < 3e22
        
        # Test cubic root of mass ratio
        assert detalles['ratio_masas_cbrt'] > 2.8e7
        assert detalles['ratio_masas_cbrt'] < 2.9e7
        
        # Test phi cubed
        assert abs(detalles['phi_cubed'] - rc.PHI ** 3) < 1e-10
        
        # Test duality factor
        assert detalles['factor_dualidad'] == 2.0
        
    def test_golden_ratio_cubed(self):
        """Test phi cubed value."""
        K, detalles = rc.calcular_factor_escala_cosmico()
        phi_cubed = detalles['phi_cubed']
        
        # φ³ ≈ 4.236068
        assert abs(phi_cubed - 4.236068) < 0.001


class TestMasterEquation:
    """Test suite for master equation and f₀ derivation."""
    
    def test_f0_calculation(self):
        """Test f₀ calculation from master equation."""
        f0_calc, componentes = rc.derivar_f0_ecuacion_maestra()
        
        # f₀ calculated should be approximately 141.5459 Hz
        assert abs(f0_calc - 141.5459) < 0.001
        
    def test_f0_components_present(self):
        """Test that all components are returned."""
        f0_calc, componentes = rc.derivar_f0_ecuacion_maestra()
        
        # Check all required components are present
        assert 'frecuencia_base' in componentes
        assert 'sqrt_ratio_masas' in componentes
        assert 'alpha' in componentes
        assert 'phi' in componentes
        assert 'ratio_escalas' in componentes
        assert 'K' in componentes
        assert 'f0_calculado' in componentes
        
    def test_master_equation_validation(self):
        """Test master equation validation against theoretical f₀."""
        resultados = rc.validar_ecuacion_maestra(verbose=False)
        
        # Check calculated value
        assert abs(resultados['f0_calculado'] - 141.5459) < 0.001
        
        # Check theoretical value
        assert resultados['f0_teorico'] == 141.7001
        
        # Check error is approximately 0.1088%
        assert abs(resultados['error_porcentual'] - 0.1088) < 0.01
        
    def test_error_absolute(self):
        """Test absolute error is within expected range."""
        resultados = rc.validar_ecuacion_maestra(verbose=False)
        
        # Error should be approximately 0.1542 Hz
        assert abs(resultados['error_absoluto'] - 0.1542) < 0.01
        
    def test_error_percentage(self):
        """Test percentage error matches problem statement."""
        resultados = rc.validar_ecuacion_maestra(verbose=False)
        
        # Error percentage should be 0.1088%
        error_pct = resultados['error_porcentual']
        assert error_pct > 0.10
        assert error_pct < 0.12
        
        # More precise: should be very close to 0.1088%
        assert abs(error_pct - 0.1088) < 0.001


class TestPhysicalConstants:
    """Test suite for physical constants."""
    
    def test_planck_constant(self):
        """Test Planck constant value (CODATA 2018)."""
        assert rc.H_PLANCK == 6.62607015e-34
        
    def test_speed_of_light(self):
        """Test speed of light value (exact by definition)."""
        assert rc.C == 299792458.0
        
    def test_fine_structure_constant(self):
        """Test fine structure constant (CODATA 2018)."""
        assert abs(rc.ALPHA_FINE - 7.2973525693e-3) < 1e-13
        
    def test_golden_ratio(self):
        """Test golden ratio value."""
        expected_phi = (1 + (5 ** 0.5)) / 2
        assert abs(rc.PHI - expected_phi) < 1e-15
        
    def test_electron_mass(self):
        """Test electron mass (CODATA 2018)."""
        assert abs(rc.M_ELECTRON - 9.1093837015e-31) < 1e-41
        
    def test_proton_mass(self):
        """Test proton mass (CODATA 2018)."""
        assert abs(rc.M_PROTON - 1.67262192369e-27) < 1e-37
        
    def test_neutron_mass(self):
        """Test neutron mass (CODATA 2018)."""
        assert abs(rc.M_NEUTRON - 1.67492749804e-27) < 1e-37


class TestParticleAnalysis:
    """Test suite for particle analysis function."""
    
    def test_analyze_particles_returns_dict(self):
        """Test that analyze_particles returns a dictionary."""
        resultados = rc.analizar_particulas(verbose=False)
        assert isinstance(resultados, dict)
        
    def test_all_particles_analyzed(self):
        """Test that all particles are analyzed."""
        resultados = rc.analizar_particulas(verbose=False)
        
        assert 'electron' in resultados
        assert 'proton' in resultados
        assert 'neutron' in resultados
        assert 'planck' in resultados
        
    def test_particle_data_structure(self):
        """Test structure of particle data."""
        resultados = rc.analizar_particulas(verbose=False)
        
        for nombre, datos in resultados.items():
            assert 'masa' in datos
            assert 'frecuencia_compton' in datos
            assert 'longitud_onda_compton' in datos
            assert 'energia' in datos
            
            # All values should be positive
            assert datos['masa'] > 0
            assert datos['frecuencia_compton'] > 0
            assert datos['longitud_onda_compton'] > 0
            assert datos['energia'] > 0


class TestIntegration:
    """Integration tests for the complete Compton clock."""
    
    def test_complete_derivation(self):
        """Test complete derivation from particles to f₀."""
        # Get particle frequencies
        particulas = rc.calcular_frecuencias_particulas()
        
        # Get cosmic scale factor
        K, detalles_K = rc.calcular_factor_escala_cosmico()
        
        # Derive f₀
        f0_calc, componentes = rc.derivar_f0_ecuacion_maestra()
        
        # Validate
        assert 'electron' in particulas
        assert K > 2.4e8
        assert abs(f0_calc - 141.5459) < 0.001
        
    def test_validation_matches_problem_statement(self):
        """Test that validation matches problem statement exactly."""
        resultados = rc.validar_ecuacion_maestra(verbose=False)
        
        # From problem statement:
        # f₀ calculado: 141.5459 Hz
        # f₀ teórica: 141.7001 Hz
        # Error: 0.1088%
        
        assert abs(resultados['f0_calculado'] - 141.5459) < 0.0001
        assert resultados['f0_teorico'] == 141.7001
        assert abs(resultados['error_porcentual'] - 0.1088) < 0.0001


# Support for both pytest and unittest
if PYTEST_AVAILABLE:
    # Pytest will discover the test classes automatically
    pass
else:
    # Create unittest test suite
    class TestComptonFrequenciesUnit(unittest.TestCase, TestComptonFrequencies):
        pass
    
    class TestCosmicScaleFactorUnit(unittest.TestCase, TestCosmicScaleFactor):
        pass
    
    class TestMasterEquationUnit(unittest.TestCase, TestMasterEquation):
        pass
    
    class TestPhysicalConstantsUnit(unittest.TestCase, TestPhysicalConstants):
        pass
    
    class TestParticleAnalysisUnit(unittest.TestCase, TestParticleAnalysis):
        pass
    
    class TestIntegrationUnit(unittest.TestCase, TestIntegration):
        pass


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        sys.exit(pytest.main([__file__, "-v"]))
    else:
        unittest.main(verbosity=2)
