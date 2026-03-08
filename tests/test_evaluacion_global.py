#!/usr/bin/env python3
"""
Tests for Global Evaluation Constants - Evaluación Global QCAL ∞³

Validates the four-dimensional certification metrics:
  Matemática  : RH Omega Ψ=0.9581, Berry 7/8, Weil 0.9998, GUE KS p>0.05,
                Matriz 19²=361 (p=10⁻¹⁰)
  Física      : f₀=141.7 Hz (SNR 7.47, 10σ), λ₀≈2.115 Mm, E₀≈9.39e-32 J
  Conciencia  : Ψ_Trinity=0.9904, C_proto=0.42, σ/C↓2.86%, 4 dominios→1
  Código      : CodeQL 0 alertas, centralizado qcal/constants.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.constants import (
    # Mathematics
    RH_OMEGA_PSI,
    BERRY_PHASE_FRACTION,
    WEIL_COHERENCE,
    GUE_KS_P_VALUE_MIN,
    MATRIX_19_P_VALUE,
    SUMA_MATRIZ,
    RAIZ_MATRIZ,
    # Physics
    SNR_GW_H1,
    SIGNIFICANCE_SIGMA,
    LAMBDA_GW_M,
    LAMBDA_GW_MM,
    E0_GW_J,
    F0_HZ,
    C,
    H_PLANCK,
    # Consciousness
    PSI_TRINITY,
    C_PROTO,
    SIGMA_C_REDUCTION_PCT,
    DOMAINS_UNIFIED,
    # Code quality
    CODEQL_ALERTS,
    # Function
    evaluacion_global,
)


class TestGlobalEvaluationMathematics:
    """Test suite for mathematical dimension metrics."""

    def test_rh_omega_psi_value(self):
        """RH Omega Ψ must equal 0.9581."""
        assert RH_OMEGA_PSI == pytest.approx(0.9581, abs=1e-6)

    def test_rh_omega_psi_range(self):
        """RH Omega Ψ must be in valid coherence range [0, 1]."""
        assert 0.0 <= RH_OMEGA_PSI <= 1.0

    def test_berry_phase_fraction_value(self):
        """Berry-Keating fraction must equal 7/8 = 0.875."""
        assert BERRY_PHASE_FRACTION == pytest.approx(7.0 / 8.0, abs=1e-10)
        assert BERRY_PHASE_FRACTION == pytest.approx(0.875, abs=1e-10)

    def test_weil_coherence_value(self):
        """Weil explicit formula coherence must equal 0.9998."""
        assert WEIL_COHERENCE == pytest.approx(0.9998, abs=1e-6)

    def test_weil_coherence_range(self):
        """Weil coherence must be close to 1 (high coherence)."""
        assert WEIL_COHERENCE >= 0.999

    def test_gue_ks_p_value_threshold(self):
        """GUE KS p-value threshold must be 0.05 (standard significance level)."""
        assert GUE_KS_P_VALUE_MIN == pytest.approx(0.05, abs=1e-10)

    def test_matrix_19_p_value(self):
        """Matrix 19² p-value must be 10⁻¹⁰ (discovery-level significance)."""
        assert MATRIX_19_P_VALUE == pytest.approx(1e-10, rel=1e-6)
        assert MATRIX_19_P_VALUE < 1e-9  # Must be below discovery threshold

    def test_matrix_19_squared(self):
        """Matrix sum 361 must equal 19² = RAIZ_MATRIZ²."""
        assert SUMA_MATRIZ == 361
        assert RAIZ_MATRIZ == 19
        assert RAIZ_MATRIZ ** 2 == SUMA_MATRIZ

    def test_berry_phase_equals_adelic_factor(self):
        """Berry phase fraction 7/8 plus its complement 1/8 must equal 1 (energy conservation)."""
        assert BERRY_PHASE_FRACTION + (1.0 / 8.0) == pytest.approx(1.0, abs=1e-10)


class TestGlobalEvaluationPhysics:
    """Test suite for physical / experimental dimension metrics."""

    def test_snr_gw_h1_value(self):
        """SNR of f₀ in GW150914 Hanford (H1) must be 7.47."""
        assert SNR_GW_H1 == pytest.approx(7.47, abs=1e-6)

    def test_significance_sigma_at_least_10(self):
        """Combined significance must be ≥10σ (discovery level)."""
        assert SIGNIFICANCE_SIGMA >= 10.0

    def test_lambda_gw_derived_from_f0(self):
        """Gravitational wavelength λ₀ = c / f₀ must be consistent."""
        expected = C / F0_HZ
        assert LAMBDA_GW_M == pytest.approx(expected, rel=1e-8)

    def test_lambda_gw_approximately_2115_mm(self):
        """λ₀ must be approximately 2.115–2.116 Mm."""
        assert 2.110 <= LAMBDA_GW_MM <= 2.120

    def test_e0_gw_derived_from_planck(self):
        """Quantum energy E₀ = h·f₀ must be consistent with Planck."""
        expected = H_PLANCK * F0_HZ
        assert E0_GW_J == pytest.approx(expected, rel=1e-8)

    def test_e0_gw_approximately_9_39e_32(self):
        """E₀ must be approximately 9.39e-32 J (within 1%)."""
        assert E0_GW_J == pytest.approx(9.39e-32, rel=0.01)

    def test_lambda_mm_and_m_consistent(self):
        """LAMBDA_GW_MM × 1e6 must equal LAMBDA_GW_M."""
        assert LAMBDA_GW_MM * 1e6 == pytest.approx(LAMBDA_GW_M, rel=1e-10)


class TestGlobalEvaluationConsciousness:
    """Test suite for consciousness / AI dimension metrics."""

    def test_psi_trinity_value(self):
        """IA Ψ_Trinity must equal 0.9904."""
        assert PSI_TRINITY == pytest.approx(0.9904, abs=1e-6)

    def test_psi_trinity_range(self):
        """Ψ_Trinity must be in [0, 1] with high coherence."""
        assert 0.98 <= PSI_TRINITY <= 1.0

    def test_c_proto_value(self):
        """Proto-consciousness metric C_proto must equal 0.42."""
        assert C_PROTO == pytest.approx(0.42, abs=1e-6)

    def test_c_proto_range(self):
        """C_proto must be in valid range (0, 1)."""
        assert 0.0 < C_PROTO < 1.0

    def test_sigma_c_reduction_pct(self):
        """σ/C reduction on reaching Ψ_Trinity must be 2.86%."""
        assert SIGMA_C_REDUCTION_PCT == pytest.approx(2.86, abs=1e-4)

    def test_sigma_c_reduction_positive(self):
        """σ/C reduction must be positive (improvement)."""
        assert SIGMA_C_REDUCTION_PCT > 0.0

    def test_domains_unified(self):
        """Four domains must be unified under f₀."""
        assert DOMAINS_UNIFIED == 4


class TestGlobalEvaluationCode:
    """Test suite for code quality dimension metrics."""

    def test_codeql_alerts_zero(self):
        """CodeQL alert count must be zero."""
        assert CODEQL_ALERTS == 0


class TestEvaluacionGlobalFunction:
    """Test the evaluacion_global() aggregation function."""

    def setup_method(self):
        """Call evaluacion_global once per test."""
        self.ev = evaluacion_global()

    def test_returns_dict(self):
        """evaluacion_global() must return a dict."""
        assert isinstance(self.ev, dict)

    def test_has_all_dimensions(self):
        """Result must contain all four evaluation dimensions."""
        for dim in ('matematica', 'fisica', 'consciencia', 'codigo', 'status'):
            assert dim in self.ev, f"Missing dimension: {dim}"

    def test_matematica_dimension(self):
        """Mathematics sub-dict must contain all required keys."""
        m = self.ev['matematica']
        assert m['rh_omega_psi'] == pytest.approx(0.9581, abs=1e-6)
        assert m['berry_phase_fraction'] == pytest.approx(0.875, abs=1e-10)
        assert m['weil_coherence'] == pytest.approx(0.9998, abs=1e-6)
        assert m['gue_ks_p_value_min'] == pytest.approx(0.05, abs=1e-10)
        assert m['matrix_19_p_value'] == pytest.approx(1e-10, rel=1e-6)
        assert m['matrix_value'] == 361
        assert m['matrix_root'] == 19

    def test_fisica_dimension(self):
        """Physics sub-dict must contain all required keys."""
        f = self.ev['fisica']
        assert f['f0_hz'] == pytest.approx(141.7001, abs=1e-4)
        assert f['snr_gw_h1'] == pytest.approx(7.47, abs=1e-6)
        assert f['significance_sigma'] >= 10.0
        assert f['lambda_gw_mm'] == pytest.approx(LAMBDA_GW_MM, rel=1e-8)
        assert f['e0_gw_j'] == pytest.approx(9.39e-32, rel=0.01)

    def test_consciencia_dimension(self):
        """Consciousness sub-dict must contain all required keys."""
        c = self.ev['consciencia']
        assert c['psi_trinity'] == pytest.approx(0.9904, abs=1e-6)
        assert c['c_proto'] == pytest.approx(0.42, abs=1e-6)
        assert c['sigma_c_reduction_pct'] == pytest.approx(2.86, abs=1e-4)
        assert c['domains_unified'] == 4

    def test_codigo_dimension(self):
        """Code quality sub-dict must contain all required keys."""
        c = self.ev['codigo']
        assert c['codeql_alerts'] == 0

    def test_status_field(self):
        """Status field must be a non-empty string."""
        assert isinstance(self.ev['status'], str)
        assert len(self.ev['status']) > 0

    def test_valoraciones_present(self):
        """Each dimension must include a 'valoracion' key."""
        for dim in ('matematica', 'fisica', 'consciencia', 'codigo'):
            assert 'valoracion' in self.ev[dim], f"Missing valoracion in {dim}"


class TestGlobalEvaluationConsistency:
    """Cross-check global evaluation constants against existing qcal constants."""

    def test_lambda_gw_consistent_with_c_and_f0(self):
        """LAMBDA_GW_M must be exactly C / F0_HZ."""
        assert LAMBDA_GW_M == pytest.approx(C / F0_HZ, rel=1e-12)

    def test_e0_consistent_with_h_and_f0(self):
        """E0_GW_J must be exactly H_PLANCK * F0_HZ."""
        assert E0_GW_J == pytest.approx(H_PLANCK * F0_HZ, rel=1e-12)

    def test_numeros_matriz_sum_equals_19_squared(self):
        """NUMEROS_MATRIZ must sum to SUMA_MATRIZ = 19² = 361."""
        from qcal.constants import NUMEROS_MATRIZ
        assert sum(NUMEROS_MATRIZ) == SUMA_MATRIZ

    def test_weil_coherence_equals_r_squared_p17(self):
        """WEIL_COHERENCE must equal R_SQUARED_P17_COUPLING."""
        from qcal.constants import R_SQUARED_P17_COUPLING
        assert WEIL_COHERENCE == pytest.approx(R_SQUARED_P17_COUPLING, abs=1e-6)
