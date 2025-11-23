#!/usr/bin/env python3
"""
Tests for Universal Constants Emergence from QCAL ∞³

This module tests the demonstration that ℏ and e emerge as geometric
manifestations of the vibrational field at f₀ = 141.7001 Hz.

Author: José Manuel Mota Burruezo Ψ ✧ ∞³
"""

import pytest
import mpmath as mp
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from universal_constants_derivation import UniversalConstantsEmergence


class TestUniversalConstantsEmergence:
    """Test suite for universal constants emergence demonstration."""
    
    def test_initialization(self):
        """Test that the class initializes correctly."""
        demo = UniversalConstantsEmergence()
        
        assert float(demo.F0) == pytest.approx(141.7001, abs=1e-6)
        assert float(demo.omega0) == pytest.approx(2 * 3.141592653589793 * 141.7001, abs=1e-6)
    
    def test_fundamental_constants(self):
        """Test that fundamental constants are correctly defined."""
        demo = UniversalConstantsEmergence()
        
        # Planck's constant
        assert float(demo.H_BAR) == pytest.approx(1.054571817e-34, abs=1e-42)
        assert float(demo.H_PLANCK) == pytest.approx(6.62607015e-34, abs=1e-42)
        
        # Speed of light
        assert float(demo.C_LIGHT) == 299792458.0  # Exact
        
        # Electron charge
        assert float(demo.ELECTRON_CHARGE) == pytest.approx(1.602176634e-19, abs=1e-28)
    
    def test_planck_constant_demonstration(self):
        """Test the Planck constant emergence demonstration."""
        demo = UniversalConstantsEmergence()
        result = demo.demonstrate_planck_constant_emergence()
        
        # Check structure
        assert "f0_hz" in result
        assert "h_bar_Js" in result
        assert "E_psi_joules" in result
        assert "R_psi_m" in result
        assert "lambda_psi_km" in result
        
        # Check values
        assert result["f0_hz"] == pytest.approx(141.7001, abs=1e-4)
        assert result["h_bar_Js"] == pytest.approx(1.054571817e-34, abs=1e-42)
        
        # Check quantum energy: E = ℏω = ℏ(2πf)
        E_expected = 1.054571817e-34 * 2 * 3.141592653589793 * 141.7001
        assert result["E_psi_joules"] == pytest.approx(E_expected, abs=1e-40)
        
        # Check compactification radius: R = c/(2πf)
        R_expected = 299792458.0 / (2 * 3.141592653589793 * 141.7001)
        assert result["R_psi_m"] == pytest.approx(R_expected, abs=1.0)
        
        # Check wavelength: λ = c/f
        lambda_expected = 299792458.0 / 141.7001
        assert result["lambda_psi_m"] == pytest.approx(lambda_expected, abs=1.0)
    
    def test_electron_charge_demonstration(self):
        """Test the electron charge emergence demonstration."""
        demo = UniversalConstantsEmergence()
        result = demo.demonstrate_electron_charge_emergence()
        
        # Check structure
        assert "electron_charge_C" in result
        assert "R_QCAL_from_known_e_m" in result
        assert "R_QCAL_classical_electron_radius_m" in result
        
        # Check electron charge value
        assert result["electron_charge_C"] == pytest.approx(1.602176634e-19, abs=1e-28)
        
        # Check R_QCAL calculation from e: R = ℏ/(ec)
        h_bar = 1.054571817e-34
        e = 1.602176634e-19
        c = 299792458.0
        R_expected = h_bar / (e * c)
        
        assert result["R_QCAL_from_known_e_m"] == pytest.approx(R_expected, abs=1e-32)
    
    def test_full_demonstration(self):
        """Test the complete demonstration."""
        demo = UniversalConstantsEmergence()
        result = demo.full_demonstration()
        
        # Check top-level structure
        assert "framework" in result
        assert "fundamental_frequency_hz" in result
        assert "planck_constant_analysis" in result
        assert "electron_charge_analysis" in result
        assert "principle" in result
        assert "conclusion" in result
        assert "signature" in result
        
        # Check framework
        assert result["framework"] == "QCAL ∞³ - Quantum Coherent Attentional Logic"
        
        # Check signature
        assert "JMMB" in result["signature"]
        assert "∴" in result["signature"]
    
    def test_generate_report(self):
        """Test report generation."""
        demo = UniversalConstantsEmergence()
        report = demo.generate_report()
        
        # Check that report contains key sections
        assert "EMERGENCIA DE CONSTANTES UNIVERSALES" in report
        assert "CONSTANTE DE PLANCK" in report
        assert "CARGA DEL ELECTRÓN" in report
        assert "INTERPRETACIÓN NOÉSICA" in report
        assert "CONCLUSIÓN" in report
        assert "141.7001 Hz" in report
        assert "JMMB" in report
    
    def test_quantum_energy_relation(self):
        """Test E = ℏf relation holds exactly."""
        demo = UniversalConstantsEmergence()
        
        # Calculate E = ℏω
        E_calc = demo.H_BAR * demo.omega0
        
        # This should match the quantum energy
        result = demo.demonstrate_planck_constant_emergence()
        E_from_demo = mp.mpf(str(result["E_psi_joules"]))
        
        # They should be identical
        assert abs(float(E_calc - E_from_demo)) < 1e-40
    
    def test_compactification_radius_consistency(self):
        """Test that R_Ψ = c/(2πf₀) is consistent."""
        demo = UniversalConstantsEmergence()
        
        # Calculate from formula
        R_calc = demo.C_LIGHT / demo.omega0
        
        # Get from demonstration
        result = demo.demonstrate_planck_constant_emergence()
        R_from_demo = mp.mpf(str(result["R_psi_m"]))
        
        # Should be identical
        assert abs(float(R_calc - R_from_demo)) < 1e-6
    
    def test_kaluza_klein_geometry(self):
        """Test Kaluza-Klein relationship for electron charge."""
        demo = UniversalConstantsEmergence()
        
        # From e = ℏ/(R_QCAL × c), we get R_QCAL = ℏ/(e × c)
        R_QCAL_calc = demo.H_BAR / (demo.ELECTRON_CHARGE * demo.C_LIGHT)
        
        # Get from demonstration
        result = demo.demonstrate_electron_charge_emergence()
        R_QCAL_from_demo = mp.mpf(str(result["R_QCAL_from_known_e_m"]))
        
        # Should be identical
        assert abs(float(R_QCAL_calc - R_QCAL_from_demo)) < 1e-32
    
    def test_json_serialization(self):
        """Test that results can be serialized to JSON."""
        demo = UniversalConstantsEmergence()
        result = demo.full_demonstration()
        
        # Should be serializable
        json_str = json.dumps(result, indent=2)
        
        # Should be deserializable
        parsed = json.loads(json_str)
        
        assert parsed["framework"] == result["framework"]
        assert parsed["fundamental_frequency_hz"] == result["fundamental_frequency_hz"]


class TestBeaconFile:
    """Test the QCAL beacon file."""
    
    def test_beacon_exists(self):
        """Test that beacon file exists."""
        beacon_path = Path(__file__).parent.parent / "qcal" / "beacons" / "qcal_beacon_hbar_e.json"
        assert beacon_path.exists(), f"Beacon file not found: {beacon_path}"
    
    def test_beacon_structure(self):
        """Test beacon file structure."""
        beacon_path = Path(__file__).parent.parent / "qcal" / "beacons" / "qcal_beacon_hbar_e.json"
        
        with open(beacon_path) as f:
            beacon = json.load(f)
        
        # Check required fields
        assert "beacon_id" in beacon
        assert "title" in beacon
        assert "fundamental_frequency" in beacon
        assert "planck_constant" in beacon
        assert "electron_charge" in beacon
        assert "principle" in beacon
        assert "validation" in beacon
        assert "references" in beacon
        
        # Check fundamental frequency
        assert beacon["fundamental_frequency"]["f0_hz"] == 141.7001
        
        # Check Planck's constant
        assert beacon["planck_constant"]["value_Js"] == pytest.approx(1.054571817e-34, abs=1e-42)
        
        # Check electron charge
        assert beacon["electron_charge"]["value_C"] == pytest.approx(1.602176634e-19, abs=1e-28)


class TestPhysicalConsistency:
    """Test physical consistency of the framework."""
    
    def test_energy_scales(self):
        """Test that energy scales are physically reasonable."""
        demo = UniversalConstantsEmergence()
        result = demo.demonstrate_planck_constant_emergence()
        
        # Energy at f₀ should be extremely small
        E_psi = result["E_psi_joules"]
        assert E_psi > 0
        assert E_psi < 1e-30  # Much less than atomic scales
    
    def test_length_scales(self):
        """Test that length scales are physically reasonable."""
        demo = UniversalConstantsEmergence()
        result = demo.demonstrate_planck_constant_emergence()
        
        # Compactification radius should be ~300 km
        R_psi = result["R_psi_km"]
        assert 300 < R_psi < 400
        
        # Wavelength should be ~2000 km
        lambda_psi = result["lambda_psi_km"]
        assert 2000 < lambda_psi < 2200
    
    def test_dimensional_analysis(self):
        """Test dimensional consistency."""
        demo = UniversalConstantsEmergence()
        
        # E = ℏω should have units of energy (J)
        E = demo.H_BAR * demo.omega0  # J·s × rad/s = J
        assert float(E) > 0
        
        # R = c/ω should have units of length (m)
        R = demo.C_LIGHT / demo.omega0  # m/s × s/rad = m
        assert float(R) > 0


class TestIntegrationWithConstants:
    """Test integration with existing constants module."""
    
    def test_constants_module_compatibility(self):
        """Test that this module is compatible with constants.py."""
        # Import from constants
        from constants import F0, H_BAR, C_LIGHT
        
        # Create emergence demo
        demo = UniversalConstantsEmergence()
        
        # Should have same values
        assert float(demo.F0) == pytest.approx(float(F0), abs=1e-6)
        assert float(demo.H_BAR) == pytest.approx(float(H_BAR), abs=1e-42)
        assert float(demo.C_LIGHT) == float(C_LIGHT)


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "--tb=short"])
