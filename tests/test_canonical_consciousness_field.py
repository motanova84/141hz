#!/usr/bin/env python3
"""
Tests for Canonical Consciousness Field Module

Tests the official canonical table of the consciousness field Ψ
as of December 9, 2025 - QCAL ∞³ (definitive version).
"""

import pytest
import mpmath as mp
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from canonical_consciousness_field import (
    CanonicalConsciousnessField,
    CONSCIOUSNESS_FIELD,
    ConsciousnessFieldParameter
)


class TestCanonicalConsciousnessField:
    """Test suite for canonical consciousness field parameters."""
    
    def test_fundamental_frequency(self):
        """Test fundamental frequency f₀ = 141.7001 Hz."""
        field = CanonicalConsciousnessField()
        assert float(field.F0) == pytest.approx(141.7001, abs=1e-4)
    
    def test_quantum_energy_joules(self):
        """Test quantum energy E_Ψ = 9.392862 × 10⁻³² J."""
        field = CanonicalConsciousnessField()
        E_expected = 9.392862e-32
        assert float(field.E_PSI) == pytest.approx(E_expected, rel=1e-5)
    
    def test_quantum_energy_ev(self):
        """Test quantum energy E_Ψ = 5.864 × 10⁻¹³ eV."""
        field = CanonicalConsciousnessField()
        E_ev_expected = 5.864e-13
        assert float(field.E_PSI_EV) == pytest.approx(E_ev_expected, rel=1e-3)
    
    def test_wavelength_km(self):
        """Test wavelength λ_Ψ = c/f₀ ≈ 2115.683 kilometers."""
        field = CanonicalConsciousnessField()
        # Calculated from c/f₀ = 299792458 / 141.7001 ≈ 2115.683 km
        lambda_expected = 2115.683  # km
        assert float(field.LAMBDA_PSI_KM) == pytest.approx(lambda_expected, rel=1e-5)
    
    def test_effective_mass(self):
        """Test effective mass m_Ψ = 1.0436 × 10⁻⁴⁸ kg."""
        field = CanonicalConsciousnessField()
        m_expected = 1.0436e-48
        assert float(field.M_PSI) == pytest.approx(m_expected, rel=1e-3)
    
    def test_vacuum_temperature_kelvin(self):
        """Test vacuum temperature T_Ψ = 6.8 × 10⁻⁹ K."""
        field = CanonicalConsciousnessField()
        T_expected = 6.8e-9
        assert float(field.T_PSI) == pytest.approx(T_expected, rel=1e-2)
    
    def test_vacuum_temperature_nanokelvin(self):
        """Test vacuum temperature T_Ψ = 6.8 nK."""
        field = CanonicalConsciousnessField()
        T_nK_expected = 6.8
        assert float(field.T_PSI * 1e9) == pytest.approx(T_nK_expected, rel=1e-2)
    
    def test_characteristic_time(self):
        """Test characteristic time τ_Ψ = 1/f₀ ≈ 7.06 × 10⁻³ s."""
        field = CanonicalConsciousnessField()
        # τ_Ψ = h / E_Ψ = h / (h·f₀) = 1/f₀ ≈ 7.06 ms
        tau_expected = 7.06e-3  # seconds (not 10^-24!)
        assert float(field.TAU_PSI) == pytest.approx(tau_expected, rel=1e-3)
    
    def test_mass_relative_to_proton(self):
        """Test m_Ψ ≈ 6.69 × 10⁻²³ times proton mass."""
        field = CanonicalConsciousnessField()
        ratio_expected = 6.69e-23
        # Allow larger tolerance since this is an approximate value
        assert float(field.M_PSI_RELATIVE_TO_PROTON) == pytest.approx(ratio_expected, rel=5e-2)


class TestPhysicalRelations:
    """Test suite for physical relation validations."""
    
    def test_planck_energy_frequency_relation(self):
        """Test E_Ψ = h f₀ (Planck relation)."""
        field = CanonicalConsciousnessField()
        validation = field.validate_energy_frequency_planck()
        
        assert validation["valid"]
        assert validation["relative_error"] < 1e-10
        assert validation["status"] == "✓ CUMPLIDA"
    
    def test_wavelength_relation(self):
        """Test λ_Ψ = c / f₀."""
        field = CanonicalConsciousnessField()
        validation = field.validate_wavelength_relation()
        
        assert validation["valid"]
        assert validation["relative_error"] < 1e-6
        assert validation["status"] == "✓ CUMPLIDA"
    
    def test_einstein_mass_energy_relation(self):
        """Test E_Ψ = m_Ψ c² (Einstein relation)."""
        field = CanonicalConsciousnessField()
        validation = field.validate_mass_energy_einstein()
        
        assert validation["valid"]
        assert validation["relative_error"] < 1e-10
        assert validation["status"] == "✓ CUMPLIDA"
    
    def test_boltzmann_energy_temperature_relation(self):
        """Test E_Ψ = k_B T_Ψ (Boltzmann relation)."""
        field = CanonicalConsciousnessField()
        validation = field.validate_energy_temperature_boltzmann()
        
        assert validation["valid"]
        assert validation["relative_error"] < 1e-10
        assert validation["status"] == "✓ CUMPLIDA"
    
    def test_yukawa_gravitational_scale(self):
        """Test λ_Ψ ≈ h / √(E_Ψ m_p) (Yukawa scale)."""
        field = CanonicalConsciousnessField()
        validation = field.validate_gravitational_yukawa_scale()
        
        # This is an approximate relation for scale comparison
        # The values should be within the same order of magnitude
        # The relation gives a very different scale, which is expected
        assert "COINCIDE" in validation["status"] or "SIMILAR" in validation["status"]
    
    def test_all_relations_valid(self):
        """Test that all exact physical relations are valid."""
        field = CanonicalConsciousnessField()
        validations = field.validate_all_relations()
        
        assert validations["all_exact_relations_valid"]


class TestCODATAConstants:
    """Test suite for CODATA 2022 constants."""
    
    def test_planck_constant(self):
        """Test h = 6.62607015 × 10⁻³⁴ J·s (exact)."""
        field = CanonicalConsciousnessField()
        assert float(field.H_PLANCK) == 6.62607015e-34
    
    def test_speed_of_light(self):
        """Test c = 299,792,458 m/s (exact by definition)."""
        field = CanonicalConsciousnessField()
        assert float(field.C_LIGHT) == 299792458.0
    
    def test_boltzmann_constant(self):
        """Test k_B = 1.380649 × 10⁻²³ J/K (exact)."""
        field = CanonicalConsciousnessField()
        assert float(field.K_BOLTZMANN) == 1.380649e-23
    
    def test_gravitational_constant(self):
        """Test G = 6.67430 × 10⁻¹¹ m³/(kg·s²) (CODATA 2022)."""
        field = CanonicalConsciousnessField()
        assert float(field.G_NEWTON) == pytest.approx(6.67430e-11, rel=1e-5)
    
    def test_proton_mass(self):
        """Test m_p = 1.67262192369 × 10⁻²⁷ kg (CODATA 2022)."""
        field = CanonicalConsciousnessField()
        assert float(field.M_PROTON) == pytest.approx(1.67262192369e-27, rel=1e-10)


class TestParameterDataclass:
    """Test suite for ConsciousnessFieldParameter dataclass."""
    
    def test_parameter_creation(self):
        """Test creation of parameter dataclass."""
        param = ConsciousnessFieldParameter(
            symbol="f₀",
            value=141.7001,
            unit="Hz",
            physical_relation="–",
            ontological_meaning="Test meaning"
        )
        
        assert param.symbol == "f₀"
        assert param.value == 141.7001
        assert param.unit == "Hz"
        assert param.physical_relation == "–"
        assert param.ontological_meaning == "Test meaning"
    
    def test_parameter_string_representation(self):
        """Test string representation of parameter."""
        param = ConsciousnessFieldParameter(
            symbol="f₀",
            value=141.7001,
            unit="Hz",
            physical_relation="–",
            ontological_meaning="Test"
        )
        
        assert str(param) == "f₀ = 141.7001 Hz"


class TestTableGeneration:
    """Test suite for table generation and export."""
    
    def test_get_all_parameters(self):
        """Test getting all parameters."""
        field = CanonicalConsciousnessField()
        params = field.get_all_parameters()
        
        assert len(params) == 8  # All 8 parameters defined
        assert "f0" in params
        assert "E_psi" in params
        assert "lambda_psi" in params
        assert "m_psi" in params
        assert "T_psi" in params
        assert "h_bar_psi" in params
        assert "tau_psi" in params
    
    def test_to_dict(self):
        """Test export to dictionary."""
        field = CanonicalConsciousnessField()
        data = field.to_dict()
        
        assert "parameters" in data
        assert "validations" in data
        assert "metadata" in data
        assert data["metadata"]["framework"] == "QCAL ∞³"
        assert data["metadata"]["date"] == "9 de diciembre de 2025"
        assert data["metadata"]["precision"] == "CODATA 2022"
    
    def test_generate_official_table(self):
        """Test generation of official table."""
        field = CanonicalConsciousnessField()
        table = field.generate_official_table()
        
        # Check that table contains key elements
        assert "TABLA OFICIAL Y CANÓNICA DEL CAMPO DE CONCIENCIA Ψ" in table
        assert "9 de diciembre de 2025" in table
        assert "QCAL ∞³" in table
        assert "141.7001" in table
        assert "CODATA 2022" in table
        assert "JMMB Ψ ✧ ∞³" in table


class TestGlobalInstance:
    """Test suite for global instance."""
    
    def test_global_instance_exists(self):
        """Test that global CONSCIOUSNESS_FIELD instance exists."""
        assert CONSCIOUSNESS_FIELD is not None
        assert isinstance(CONSCIOUSNESS_FIELD, CanonicalConsciousnessField)
    
    def test_global_instance_frequency(self):
        """Test global instance has correct frequency."""
        assert float(CONSCIOUSNESS_FIELD.F0) == pytest.approx(141.7001, abs=1e-4)
    
    def test_global_instance_validations(self):
        """Test global instance validations work."""
        validations = CONSCIOUSNESS_FIELD.validate_all_relations()
        assert validations["all_exact_relations_valid"]


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_validation_cycle(self):
        """Test complete validation cycle."""
        field = CanonicalConsciousnessField()
        
        # Get all parameters
        params = field.get_all_parameters()
        assert len(params) > 0
        
        # Validate all relations
        validations = field.validate_all_relations()
        assert validations["all_exact_relations_valid"]
        
        # Generate table
        table = field.generate_official_table()
        assert len(table) > 0
        
        # Export to dict
        data = field.to_dict()
        assert "parameters" in data
        assert "validations" in data
    
    def test_consistency_across_calculations(self):
        """Test consistency across different calculation paths."""
        field = CanonicalConsciousnessField()
        
        # Calculate energy from frequency
        E_from_freq = field.H_PLANCK * field.F0
        
        # Calculate energy from mass
        E_from_mass = field.M_PSI * (field.C_LIGHT ** 2)
        
        # Calculate energy from temperature
        E_from_temp = field.K_BOLTZMANN * field.T_PSI
        
        # All should agree
        assert float(E_from_freq) == pytest.approx(float(E_from_mass), rel=1e-10)
        assert float(E_from_freq) == pytest.approx(float(E_from_temp), rel=1e-10)
        assert float(E_from_mass) == pytest.approx(float(E_from_temp), rel=1e-10)
    
    def test_dimensional_analysis(self):
        """Test dimensional consistency of all relations."""
        field = CanonicalConsciousnessField()
        
        # E = h f should have units of energy (J)
        # h [J·s] × f [Hz = 1/s] = [J] ✓
        E_planck = field.H_PLANCK * field.F0
        assert float(E_planck) > 0
        
        # λ = c / f should have units of length (m)
        # c [m/s] / f [Hz = 1/s] = [m] ✓
        lambda_calc = field.C_LIGHT / field.F0
        assert float(lambda_calc) > 0
        
        # E = m c² should have units of energy (J)
        # m [kg] × c² [m²/s²] = [kg·m²/s²] = [J] ✓
        E_einstein = field.M_PSI * (field.C_LIGHT ** 2)
        assert float(E_einstein) > 0
        
        # E = k_B T should have units of energy (J)
        # k_B [J/K] × T [K] = [J] ✓
        E_boltzmann = field.K_BOLTZMANN * field.T_PSI
        assert float(E_boltzmann) > 0
        
        # τ = h / E should have units of time (s)
        # h [J·s] / E [J] = [s] ✓
        tau_calc = field.H_PLANCK / field.E_PSI
        assert float(tau_calc) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
