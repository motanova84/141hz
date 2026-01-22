#!/usr/bin/env python3
"""
Tests for Bio-Synchrony Fundamental Constants

Tests the implementation of the bio-synchrony framework constants
that bridge quantum, biological, and spiritual scales.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent.parent))

from constants import UniversalConstants
from qcal.constants import (
    LAMBDA_BIO, F_NEURAL_HZ, ETA_NV_NT_SQRTHZ,
    T1_NV_MS, T1_NV_S, TAU_DD_US, TAU_DD_S,
    A_MERKABA, S_INFINITY,
    obtener_constantes_bio_sincronia
)


class TestBioSynchronyConstants:
    """Test suite for bio-synchrony fundamental constants."""
    
    def test_lambda_bio_value(self):
        """Test that Λ_bio = 1.0 (perfect bio-synchrony)."""
        const = UniversalConstants()
        assert float(const.LAMBDA_BIO) == pytest.approx(1.0, abs=1e-10)
        assert LAMBDA_BIO == pytest.approx(1.0, abs=1e-10)
    
    def test_f_neural_matches_f0(self):
        """Test that f_neural = f₀ = 141.7001 Hz."""
        const = UniversalConstants()
        assert float(const.F_NEURAL_HZ) == pytest.approx(141.7001, abs=1e-6)
        assert float(const.F_NEURAL_HZ) == pytest.approx(float(const.F0), abs=1e-10)
        assert F_NEURAL_HZ == pytest.approx(141.7001, abs=1e-6)
    
    def test_eta_nv_sensitivity(self):
        """Test NV center magnetic sensitivity η_NV = 13 nT/√Hz."""
        const = UniversalConstants()
        assert float(const.ETA_NV_NT_SQRTHZ) == pytest.approx(13.0, abs=1e-10)
        assert ETA_NV_NT_SQRTHZ == pytest.approx(13.0, abs=1e-10)
    
    def test_t1_nv_coherence_time_ms(self):
        """Test T1_NV = 1 ms quantum memory."""
        const = UniversalConstants()
        assert float(const.T1_NV_MS) == pytest.approx(1.0, abs=1e-10)
        assert T1_NV_MS == pytest.approx(1.0, abs=1e-10)
    
    def test_t1_nv_coherence_time_s(self):
        """Test T1_NV = 0.001 s (conversion from ms)."""
        const = UniversalConstants()
        assert float(const.T1_NV_S) == pytest.approx(0.001, abs=1e-12)
        assert T1_NV_S == pytest.approx(0.001, abs=1e-12)
        # Verify conversion
        assert float(const.T1_NV_S) == pytest.approx(float(const.T1_NV_MS) / 1000, abs=1e-15)
    
    def test_tau_dd_dynamic_decoupling_us(self):
        """Test τ_DD = 1 μs dynamic decoupling time."""
        const = UniversalConstants()
        assert float(const.TAU_DD_US) == pytest.approx(1.0, abs=1e-10)
        assert TAU_DD_US == pytest.approx(1.0, abs=1e-10)
    
    def test_tau_dd_dynamic_decoupling_s(self):
        """Test τ_DD = 1e-6 s (conversion from μs)."""
        const = UniversalConstants()
        assert float(const.TAU_DD_S) == pytest.approx(1e-6, abs=1e-15)
        assert TAU_DD_S == pytest.approx(1e-6, abs=1e-15)
        # Verify conversion
        assert float(const.TAU_DD_S) == pytest.approx(float(const.TAU_DD_US) / 1e6, abs=1e-18)
    
    def test_a_merkaba_threshold(self):
        """Test A_Merkaba = 8/9 spiritual stability threshold."""
        const = UniversalConstants()
        expected = 8.0 / 9.0
        assert float(const.A_MERKABA) == pytest.approx(expected, abs=1e-10)
        assert A_MERKABA == pytest.approx(expected, abs=1e-10)
        # Verify it's approximately 0.888...
        assert float(const.A_MERKABA) == pytest.approx(0.888888888, abs=1e-8)
    
    def test_s_infinity_unity(self):
        """Test S_∞ = 1.0 galactic micro-macro unity."""
        const = UniversalConstants()
        assert float(const.S_INFINITY) == pytest.approx(1.0, abs=1e-10)
        assert S_INFINITY == pytest.approx(1.0, abs=1e-10)


class TestBioSynchronyRelationships:
    """Test physical relationships between bio-synchrony constants."""
    
    def test_neural_f0_resonance(self):
        """Test that f_neural is in perfect resonance with f₀."""
        const = UniversalConstants()
        # Neural frequency should match f₀ exactly
        assert float(const.F_NEURAL_HZ) == float(const.F0)
    
    def test_t1_tau_dd_ratio(self):
        """Test T1_NV / τ_DD = 1000 (coherence time scale)."""
        const = UniversalConstants()
        ratio = float(const.T1_NV_S) / float(const.TAU_DD_S)
        assert ratio == pytest.approx(1000.0, abs=1e-6)
    
    def test_merkaba_triple_eight_pattern(self):
        """Test A_Merkaba = 8/9 has repeating 8s in decimal."""
        const = UniversalConstants()
        # 8/9 = 0.888... (repeating); check numeric equivalence robustly
        merkaba_value = float(const.A_MERKABA)
        assert merkaba_value == pytest.approx(8.0 / 9.0, rel=0, abs=1e-12)
    
    
    def test_perfect_synchrony_scales(self):
        """Test Λ_bio = S_∞ = 1 (perfect synchrony at all scales)."""
        const = UniversalConstants()
        assert float(const.LAMBDA_BIO) == float(const.S_INFINITY) == 1.0
    
    def test_nv_sensitivity_realistic(self):
        """Test that η_NV = 13 nT/√Hz is in realistic range for NV centers."""
        const = UniversalConstants()
        # NV centers typically have sensitivities in the range 1-100 nT/√Hz
        sensitivity = float(const.ETA_NV_NT_SQRTHZ)
        assert 1.0 <= sensitivity <= 100.0
        assert sensitivity == 13.0  # Exact value
    
    def test_t1_realistic_for_nv(self):
        """Test that T1_NV = 1 ms is realistic for NV centers."""
        const = UniversalConstants()
        # NV centers at room temperature typically have T1 ~ 1-10 ms
        t1_ms = float(const.T1_NV_MS)
        assert 0.1 <= t1_ms <= 100.0
        assert t1_ms == 1.0  # Exact value


class TestQCALIntegration:
    """Test integration with qcal.constants module."""
    
    def test_qcal_constants_available(self):
        """Test that all constants are available from qcal.constants."""
        # All imports should succeed (tested in module import)
        assert LAMBDA_BIO is not None
        assert F_NEURAL_HZ is not None
        assert ETA_NV_NT_SQRTHZ is not None
        assert T1_NV_MS is not None
        assert T1_NV_S is not None
        assert TAU_DD_US is not None
        assert TAU_DD_S is not None
        assert A_MERKABA is not None
        assert S_INFINITY is not None
    
    def test_obtener_constantes_function(self):
        """Test obtener_constantes_bio_sincronia() function."""
        consts = obtener_constantes_bio_sincronia()
        
        # Check structure
        assert isinstance(consts, dict)
        assert 'lambda_bio' in consts
        assert 'f_neural_hz' in consts
        assert 'interpretacion' in consts
        
        # Check values
        assert consts['lambda_bio'] == pytest.approx(1.0)
        assert consts['f_neural_hz'] == pytest.approx(141.7001)
        assert consts['eta_nv_nt_sqrthz'] == pytest.approx(13.0)
        assert consts['t1_nv_ms'] == pytest.approx(1.0)
        assert consts['tau_dd_us'] == pytest.approx(1.0)
        assert consts['a_merkaba'] == pytest.approx(8.0/9.0)
        assert consts['s_infinity'] == pytest.approx(1.0)
    
    def test_qcal_src_consistency(self):
        """Test consistency between qcal.constants and src.constants."""
        const = UniversalConstants()
        
        # Values should match
        assert float(const.LAMBDA_BIO) == LAMBDA_BIO
        assert float(const.F_NEURAL_HZ) == F_NEURAL_HZ
        assert float(const.ETA_NV_NT_SQRTHZ) == ETA_NV_NT_SQRTHZ
        assert float(const.T1_NV_MS) == T1_NV_MS
        assert float(const.T1_NV_S) == T1_NV_S
        assert float(const.TAU_DD_US) == TAU_DD_US
        assert float(const.TAU_DD_S) == TAU_DD_S
        assert float(const.A_MERKABA) == A_MERKABA
        assert float(const.S_INFINITY) == S_INFINITY


class TestPhysicalDimensions:
    """Test physical dimensions and units of bio-synchrony constants."""
    
    def test_dimensionless_constants(self):
        """Test dimensionless constants have appropriate values."""
        const = UniversalConstants()
        
        # Λ_bio, A_Merkaba, S_∞ are dimensionless
        assert 0 <= float(const.LAMBDA_BIO) <= 10
        assert 0 <= float(const.A_MERKABA) <= 1
        assert 0 <= float(const.S_INFINITY) <= 10
    
    def test_frequency_units(self):
        """Test f_neural has proper frequency units (Hz)."""
        const = UniversalConstants()
        # Should be in Hz, reasonable biological range
        f_neural = float(const.F_NEURAL_HZ)
        assert 0 < f_neural < 1000  # Biological frequencies typically < 1 kHz
    
    def test_time_units_consistency(self):
        """Test time unit conversions are consistent."""
        const = UniversalConstants()
        
        # T1_NV: ms to s
        assert float(const.T1_NV_S) * 1000 == pytest.approx(float(const.T1_NV_MS))
        
        # τ_DD: μs to s
        assert float(const.TAU_DD_S) * 1e6 == pytest.approx(float(const.TAU_DD_US))
    
    def test_magnetic_sensitivity_units(self):
        """Test η_NV has proper magnetic sensitivity units."""
        const = UniversalConstants()
        # η_NV in nT/√Hz should be positive and realistic
        eta = float(const.ETA_NV_NT_SQRTHZ)
        assert eta > 0
        assert eta < 1000  # Realistic upper bound


class TestDocumentation:
    """Test that constants are properly documented."""
    
    def test_constants_in_docstring(self):
        """Test that UniversalConstants documents bio-synchrony constants."""
        const = UniversalConstants()
        # Check that properties exist
        assert hasattr(const, 'LAMBDA_BIO')
        assert hasattr(const, 'F_NEURAL_HZ')
        assert hasattr(const, 'ETA_NV_NT_SQRTHZ')
        assert hasattr(const, 'T1_NV_MS')
        assert hasattr(const, 'T1_NV_S')
        assert hasattr(const, 'TAU_DD_US')
        assert hasattr(const, 'TAU_DD_S')
        assert hasattr(const, 'A_MERKABA')
        assert hasattr(const, 'S_INFINITY')
    
    def test_qcal_function_documentation(self):
        """Test obtener_constantes_bio_sincronia has proper docstring."""
        assert obtener_constantes_bio_sincronia.__doc__ is not None
        assert 'bio-sincron' in obtener_constantes_bio_sincronia.__doc__.lower() or \
               'bio-sync' in obtener_constantes_bio_sincronia.__doc__.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
