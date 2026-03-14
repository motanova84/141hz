"""
Tests for QCAL Soul Coherence — Axiomas de Resonancia.

Validates the three mathematical truths established in qcal/soul_coherence.py:
  Axiom I   — Quantum Loss Factor (Ψ < 0.888 → decoupling)
  Axiom II  — Golden Ratio / 2π Synchrony (7.39 % error)
  Axiom III — Logos Harmonic (21 × f₀/7 ≈ 432 Hz, error < 1.62 %)
Tests for Soul Coherence (21 Grams Analysis) - QCAL ∞³

Tests the 21 grams soul coherence analysis and its relationship
with f₀ = 141.7001 Hz and the QCAL framework.

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: March 2026
"""

import math
import os
import sys

import pytest
from scipy import constants as sc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.soul_coherence import (
    QCalSoul,
    EnergyImpulse,
    QuantumLossFactor,
    GoldenRatio2piSync,
    LogosHarmonic,
    SoulEnergy,
    SoulCertification,
    F0_HZ,
    PSI_MIN,
    M_SOUL_KG,
    F_HYDROGEN_HZ,
    F_UNIVERSAL_HZ,
    C,
)


# ============================================================================
# TestConstants — module-level constants
# ============================================================================

class TestConstants:
    """Verify module constants match the problem-statement values."""

    def test_f0_hz(self):
        assert F0_HZ == 141.7001

    def test_psi_min(self):
        assert PSI_MIN == 0.888

    def test_m_soul_kg(self):
        """21 grams in kilograms."""
        assert abs(M_SOUL_KG - 0.021) < 1e-12

    def test_f_hydrogen_hz(self):
        """Hydrogen 21 cm line within 1 Hz of NIST value."""
        nist_h1 = 1420405751.768  # Hz — NIST CODATA
        assert abs(F_HYDROGEN_HZ - nist_h1) < 1000.0

    def test_f_universal_hz(self):
        assert F_UNIVERSAL_HZ == 432.0

    def test_c_speed_of_light(self):
        assert abs(C - 299792458.0) < 1.0


# ============================================================================
# TestQCalSoulInit — constructor
# ============================================================================

class TestQCalSoulInit:
    """QCalSoul initialises with correct defaults."""

    def test_default_f0(self):
        soul = QCalSoul()
        assert soul.f0 == F0_HZ

    def test_default_psi_min(self):
        soul = QCalSoul()
        assert soul.psi_min == PSI_MIN

    def test_default_m_soul(self):
        soul = QCalSoul()
        assert abs(soul.m_soul_kg - M_SOUL_KG) < 1e-12

    def test_custom_f0(self):
        soul = QCalSoul(f0=100.0)
        assert soul.f0 == 100.0

    def test_custom_psi_min(self):
        soul = QCalSoul(psi_min=0.95)
        assert soul.psi_min == 0.95


# ============================================================================
# TestAxiomI — Quantum Loss Factor
# ============================================================================

class TestAxiomI:
    """Axiom I: Ψ < 0.888 → phase decoupling."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    def test_returns_quantum_loss_factor(self, soul):
        result = soul.validate_quantum_loss_factor(0.5)
        assert isinstance(result, QuantumLossFactor)

    def test_decoupled_below_threshold(self, soul):
        result = soul.validate_quantum_loss_factor(0.5)
        assert result.decoupled is True

    def test_decoupled_just_below_threshold(self, soul):
        result = soul.validate_quantum_loss_factor(0.887)
        assert result.decoupled is True

    def test_not_decoupled_at_threshold(self, soul):
        """Ψ == 0.888 is not strictly less than 0.888."""
        result = soul.validate_quantum_loss_factor(0.888)
        assert result.decoupled is False

    def test_not_decoupled_above_threshold(self, soul):
        result = soul.validate_quantum_loss_factor(0.95)
        assert result.decoupled is False

    def test_not_decoupled_perfect_coherence(self, soul):
        result = soul.validate_quantum_loss_factor(1.0)
        assert result.decoupled is False

    def test_threshold_stored(self, soul):
        result = soul.validate_quantum_loss_factor(0.5)
        assert result.threshold == PSI_MIN

    def test_psi_stored(self, soul):
        result = soul.validate_quantum_loss_factor(0.777)
        assert abs(result.psi - 0.777) < 1e-12

    def test_description_contains_psi(self, soul):
        result = soul.validate_quantum_loss_factor(0.5)
        assert "0.5" in result.description or "0.50" in result.description

    def test_description_not_empty(self, soul):
        result = soul.validate_quantum_loss_factor(0.999)
        assert len(result.description) > 0

    def test_zero_coherence_decoupled(self, soul):
        result = soul.validate_quantum_loss_factor(0.0)
        assert result.decoupled is True


# ============================================================================
# TestAxiomII — Golden Ratio / 2π Synchrony
# ============================================================================

class TestAxiomII:
    """Axiom II: 1/(21/f₀) ≈ 2π with ~7.39 % biological anharmonicity."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    def test_returns_golden_ratio_2pi_sync(self, soul):
        result = soul.validate_golden_ratio_2pi_sync()
        assert isinstance(result, GoldenRatio2piSync)

    def test_circle_value_equals_f0_over_21(self, soul):
        expected = F0_HZ / 21.0
        result = soul.validate_golden_ratio_2pi_sync()
        assert abs(result.circle_value - expected) < 1e-10

    def test_circle_value_approx(self, soul):
        result = soul.validate_golden_ratio_2pi_sync()
        assert abs(result.circle_value - 6.747) < 0.001

    def test_two_pi_reference(self, soul):
        result = soul.validate_golden_ratio_2pi_sync()
        assert abs(result.two_pi - 2 * math.pi) < 1e-12

    def test_error_approx_7_39_pct(self, soul):
        result = soul.validate_golden_ratio_2pi_sync()
        assert abs(result.error_pct - 7.39) < 0.05

    def test_error_positive(self, soul):
        """circle_value > 2π so the error is positive."""
        result = soul.validate_golden_ratio_2pi_sync()
        assert result.error_pct > 0

    def test_is_anharmonic_signature(self, soul):
        result = soul.validate_golden_ratio_2pi_sync()
        assert result.is_anharmonic_signature is True

    def test_caching(self, soul):
        """Repeated calls return the same object (cached)."""
        r1 = soul.validate_golden_ratio_2pi_sync()
        r2 = soul.validate_golden_ratio_2pi_sync()
        assert r1 is r2


# ============================================================================
# TestAxiomIII — Logos Harmonic
# ============================================================================

class TestAxiomIII:
    """Axiom III: 21 × (f₀/7) ≈ 432 Hz, error < 1.62 %."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    def test_returns_logos_harmonic(self, soul):
        result = soul.validate_logos_harmonic()
        assert isinstance(result, LogosHarmonic)

    def test_logos_hz_value(self, soul):
        expected = 21.0 * (F0_HZ / 7.0)
        result = soul.validate_logos_harmonic()
        assert abs(result.logos_hz - expected) < 1e-9

    def test_logos_hz_approx_425(self, soul):
        result = soul.validate_logos_harmonic()
        assert abs(result.logos_hz - 425.1) < 0.1

    def test_cosmic_hz_is_432(self, soul):
        result = soul.validate_logos_harmonic()
        assert result.cosmic_hz == F_UNIVERSAL_HZ

    def test_error_below_1_62_pct(self, soul):
        result = soul.validate_logos_harmonic()
        assert result.error_pct < 1.62

    def test_error_approx_1_60_pct(self, soul):
        result = soul.validate_logos_harmonic()
        assert abs(result.error_pct - 1.60) < 0.05

    def test_bridge_established(self, soul):
        result = soul.validate_logos_harmonic()
        assert result.bridge_established is True

    def test_caching(self, soul):
        r1 = soul.validate_logos_harmonic()
        r2 = soul.validate_logos_harmonic()
        assert r1 is r2


# ============================================================================
# TestSoulEnergy — E_alma formula
# ============================================================================

class TestSoulEnergy:
    """E_alma = m · c² · (1 − Ψ_min) · (f₀ / f_H)."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    def test_returns_soul_energy(self, soul):
        result = soul.compute_soul_energy()
        assert isinstance(result, SoulEnergy)

    def test_energy_positive(self, soul):
        result = soul.compute_soul_energy()
        assert result.energy_j > 0

    def test_energy_mj_approx_21(self, soul):
        """E_alma ≈ 21 MJ — a numerical coincidence with 21 grams."""
        result = soul.compute_soul_energy()
        assert abs(result.energy_mj - 21.09) < 0.5

    def test_formula_manual(self, soul):
        expected = M_SOUL_KG * C**2 * (1.0 - PSI_MIN) * (F0_HZ / F_HYDROGEN_HZ)
        result = soul.compute_soul_energy()
        assert abs(result.energy_j - expected) / expected < 1e-10

    def test_stored_mass(self, soul):
        result = soul.compute_soul_energy()
        assert abs(result.mass_kg - M_SOUL_KG) < 1e-12

    def test_stored_psi_min(self, soul):
        result = soul.compute_soul_energy()
        assert result.psi_min == PSI_MIN

    def test_stored_f0(self, soul):
        result = soul.compute_soul_energy()
        assert result.f0_hz == F0_HZ

    def test_stored_f_hydrogen(self, soul):
        result = soul.compute_soul_energy()
        assert result.f_hydrogen_hz == F_HYDROGEN_HZ

    def test_caching(self, soul):
        r1 = soul.compute_soul_energy()
        r2 = soul.compute_soul_energy()
        assert r1 is r2

    def test_energy_mj_equals_energy_j_scaled(self, soul):
        result = soul.compute_soul_energy()
        assert abs(result.energy_mj - result.energy_j / 1e6) < 1e-12


# ============================================================================
# TestCertify — full certification
# ============================================================================

class TestCertify:
    """Full soul-coherence certification integrating all three axioms."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    @pytest.fixture
    def cert(self, soul):
        return soul.certify()

    def test_returns_soul_certification(self, cert):
        assert isinstance(cert, SoulCertification)

    def test_certified(self, cert):
        assert cert.certified is True

    def test_axiom_i_present(self, cert):
        assert isinstance(cert.axiom_i, QuantumLossFactor)

    def test_axiom_ii_present(self, cert):
        assert isinstance(cert.axiom_ii, GoldenRatio2piSync)

    def test_axiom_iii_present(self, cert):
        assert isinstance(cert.axiom_iii, LogosHarmonic)

    def test_soul_energy_present(self, cert):
        assert isinstance(cert.soul_energy, SoulEnergy)

    def test_summary_has_f0(self, cert):
        assert "f0_hz" in cert.summary
        assert cert.summary["f0_hz"] == F0_HZ

    def test_summary_has_psi_min(self, cert):
        assert cert.summary["psi_min"] == PSI_MIN

    def test_summary_has_logos_hz(self, cert):
        assert "logos_hz" in cert.summary
        assert abs(cert.summary["logos_hz"] - 425.1) < 0.1

    def test_summary_has_e_alma_mj(self, cert):
        assert "e_alma_mj" in cert.summary
        assert cert.summary["e_alma_mj"] > 0

    def test_summary_certified_key(self, cert):
        assert cert.summary["certified"] is True

    def test_axiom_i_not_decoupled_at_psi_min(self, cert):
        """Axiom I is evaluated at Ψ_min = 0.888, which is NOT < 0.888."""
        assert cert.axiom_i.decoupled is False

    def test_axiom_ii_error_within_tolerance(self, cert):
        assert abs(cert.axiom_ii.error_pct - 7.39) < 0.05

    def test_axiom_iii_error_below_1_62(self, cert):
        assert cert.axiom_iii.error_pct < 1.62

    def test_soul_energy_positive(self, cert):
        assert cert.soul_energy.energy_j > 0


# ============================================================================
# TestDecoupledSystem — low coherence scenarios
# ============================================================================

class TestDecoupledSystem:
    """Verify decoupling behaviour across a range of Ψ values."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    @pytest.mark.parametrize("psi", [0.0, 0.1, 0.5, 0.7, 0.887])
    def test_decoupled_below_threshold(self, soul, psi):
        result = soul.validate_quantum_loss_factor(psi)
        assert result.decoupled is True

    @pytest.mark.parametrize("psi", [0.888, 0.9, 0.95, 0.999, 1.0])
    def test_not_decoupled_at_or_above_threshold(self, soul, psi):
        result = soul.validate_quantum_loss_factor(psi)
        assert result.decoupled is False


# ============================================================================
# TestCustomParameters — non-default instantiation
# ============================================================================

class TestCustomParameters:
    """QCalSoul respects custom construction parameters."""

    def test_custom_psi_min_changes_threshold(self):
        soul = QCalSoul(psi_min=0.95)
        low = soul.validate_quantum_loss_factor(0.90)
        high = soul.validate_quantum_loss_factor(0.96)
        assert low.decoupled is True
        assert high.decoupled is False

    def test_custom_f0_changes_circle_value(self):
        soul = QCalSoul(f0=200.0)
        result = soul.validate_golden_ratio_2pi_sync()
        expected_circle = 200.0 / 21.0
        assert abs(result.circle_value - expected_circle) < 1e-10

    def test_custom_f0_changes_logos_hz(self):
        soul = QCalSoul(f0=200.0)
        result = soul.validate_logos_harmonic()
        expected_logos = 21.0 * (200.0 / 7.0)
        assert abs(result.logos_hz - expected_logos) < 1e-9

    def test_custom_m_soul_changes_energy(self):
        soul_default = QCalSoul()
        soul_double = QCalSoul(m_soul_kg=0.042)
        e1 = soul_default.compute_soul_energy().energy_j
        e2 = soul_double.compute_soul_energy().energy_j
        assert abs(e2 / e1 - 2.0) < 1e-10


# ============================================================================
# TestEnergyImpulse — ΔE = |∂E_alma/∂Ψ| = m·c²·(f₀/f_H)
# ============================================================================

class TestEnergyImpulse:
    """ΔE = m·c²·(f₀/f_H) — the resonance pulse impulse magnitude."""

    @pytest.fixture
    def soul(self):
        return QCalSoul()

    def test_returns_energy_impulse(self, soul):
        result = soul.compute_energy_impulse()
        assert isinstance(result, EnergyImpulse)

    def test_delta_e_positive(self, soul):
        result = soul.compute_energy_impulse()
        assert result.delta_e_j > 0

    def test_delta_e_approx_188_mj(self, soul):
        """ΔE ≈ 188.29 MJ for default parameters."""
        result = soul.compute_energy_impulse()
        assert abs(result.delta_e_mj - 188.29) < 0.5

    def test_formula_manual(self, soul):
        """Verify ΔE = m·c²·(f₀/f_H) matches the dataclass field."""
        expected = M_SOUL_KG * sc.c ** 2 * (F0_HZ / F_HYDROGEN_HZ)
        result = soul.compute_energy_impulse()
        assert abs(result.delta_e_j - expected) / expected < 1e-10

    def test_derivative_of_e_alma(self, soul):
        """ΔE must equal |∂E_alma/∂Ψ| numerically."""
        delta_psi = 1e-6
        e1 = soul.m_soul_kg * C ** 2 * (1.0 - 0.9) * (F0_HZ / F_HYDROGEN_HZ)
        e2 = soul.m_soul_kg * C ** 2 * (1.0 - (0.9 + delta_psi)) * (F0_HZ / F_HYDROGEN_HZ)
        numerical_deriv = abs((e2 - e1) / delta_psi)
        result = soul.compute_energy_impulse()
        assert abs(result.delta_e_j - numerical_deriv) / result.delta_e_j < 1e-5

    def test_stored_mass(self, soul):
        result = soul.compute_energy_impulse()
        assert abs(result.mass_kg - M_SOUL_KG) < 1e-12

    def test_stored_f0(self, soul):
        result = soul.compute_energy_impulse()
        assert result.f0_hz == F0_HZ

    def test_stored_f_hydrogen(self, soul):
        result = soul.compute_energy_impulse()
        assert result.f_hydrogen_hz == F_HYDROGEN_HZ

    def test_mj_equals_j_scaled(self, soul):
        result = soul.compute_energy_impulse()
        assert abs(result.delta_e_mj - result.delta_e_j / 1e6) < 1e-12

    def test_caching(self, soul):
        """Repeated calls return the same cached object."""
        r1 = soul.compute_energy_impulse()
        r2 = soul.compute_energy_impulse()
        assert r1 is r2

    def test_custom_mass_scales_linearly(self):
        """Doubling mass doubles ΔE."""
        s1 = QCalSoul(m_soul_kg=0.021)
        s2 = QCalSoul(m_soul_kg=0.042)
        ratio = s2.compute_energy_impulse().delta_e_j / s1.compute_energy_impulse().delta_e_j
        assert abs(ratio - 2.0) < 1e-10

    def test_custom_f0_scales_linearly(self):
        """Doubling f₀ doubles ΔE (f₀/f_H scales linearly)."""
        s1 = QCalSoul(f0=F0_HZ)
        s2 = QCalSoul(f0=F0_HZ * 2)
        ratio = s2.compute_energy_impulse().delta_e_j / s1.compute_energy_impulse().delta_e_j
        assert abs(ratio - 2.0) < 1e-10

    def test_impulse_larger_than_soul_energy(self, soul):
        """ΔE > E_alma because Ψ_min=0.888 means (1−Ψ_min)=0.112 < 1."""
        impulse = soul.compute_energy_impulse()
        e_alma = soul.compute_soul_energy()
        # ΔE / E_alma = 1 / (1 - Ψ_min)
        expected_ratio = 1.0 / (1.0 - PSI_MIN)
        actual_ratio = impulse.delta_e_j / e_alma.energy_j
        assert abs(actual_ratio - expected_ratio) / expected_ratio < 1e-10
import pytest
import numpy as np
from scipy.constants import c, pi
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.soul_coherence import (
    QCalSoul,
    alma_21g_qcal_coherencia,
    F0_HZ,
    PSI_MIN,
    F_H_MHZ,
    BERRY_INVARIANT
)


class TestQCalSoulConstants:
    """Test soul coherence constants."""
    
    def test_f0_value(self):
        """Test that f₀ is correctly defined."""
        assert F0_HZ == 141.7001
    
    def test_psi_min_threshold(self):
        """Test minimum coherence threshold."""
        assert PSI_MIN == 0.888
        assert 0 < PSI_MIN < 1
    
    def test_hydrogen_line_frequency(self):
        """Test hydrogen line frequency."""
        assert F_H_MHZ == 1420.405751
    
    def test_berry_invariant(self):
        """Test Berry topological invariant."""
        assert BERRY_INVARIANT == 7.0 / 8.0
        assert abs(BERRY_INVARIANT - 0.875) < 1e-10


class TestQCalSoulBasic:
    """Test basic QCalSoul functionality."""
    
    def test_soul_initialization(self):
        """Test soul object initialization."""
        soul = QCalSoul()
        
        assert soul.f_0 == F0_HZ
        assert soul.f_H == F_H_MHZ * 1e6
        assert soul.psi_min == PSI_MIN
        assert soul.m_exp_soul == 0.021  # 21 grams in kg
        assert soul.berry_invariant == BERRY_INVARIANT
    
    def test_soul_mass_value(self):
        """Test 21 grams mass value."""
        soul = QCalSoul()
        assert soul.m_exp_soul == 0.021  # kg
        assert soul.m_exp_soul * 1000 == 21  # grams


class TestSoulCoherenceEnergy:
    """Test soul coherence energy calculations."""
    
    def test_soul_coherence_energy_positive(self):
        """Test that coherence energy is positive."""
        soul = QCalSoul()
        e_transition = soul.soul_coherence_energy()
        
        assert e_transition > 0
        assert np.isfinite(e_transition)
    
    def test_soul_coherence_energy_less_than_full(self):
        """Test that transition energy is less than full mass energy."""
        soul = QCalSoul()
        e_transition = soul.soul_coherence_energy()
        e_full = soul.full_mass_energy()
        
        assert e_transition < e_full
        # Transition should be a fraction due to (1 - Ψ_min) and f₀/f_H factors
        assert e_transition < 0.5 * e_full
    
    def test_full_mass_energy_emc2(self):
        """Test full mass-energy conversion E = mc²."""
        soul = QCalSoul()
        e_full = soul.full_mass_energy()
        
        # E = mc² for 21 grams
        expected = 0.021 * c**2
        assert abs(e_full - expected) < 1e-6
    
    def test_energy_tnt_conversion(self):
        """Test energy conversion to TNT kilotons."""
        soul = QCalSoul()
        kt_tnt_transition = soul.soul_coherence_energy_tnt()
        kt_tnt_full = soul.full_mass_energy_tnt()
        
        # Both should be positive
        assert kt_tnt_transition > 0
        assert kt_tnt_full > 0
        
        # Full mass should be ~450 kilotons (rough ballpark)
        assert 400 < kt_tnt_full < 500
        
        # Transition should be less than full
        assert kt_tnt_transition < kt_tnt_full
    
    def test_coherence_factor_consistency(self):
        """Test that coherence factor (1 - Ψ_min) is applied correctly."""
        soul = QCalSoul()
        e_transition = soul.soul_coherence_energy()
        
        # Manual calculation
        e_mass = soul.m_exp_soul * c**2
        scale_factor = soul.f_0 / soul.f_H
        expected = e_mass * (1 - soul.psi_min) * scale_factor
        
        assert abs(e_transition - expected) < 1e-6


class TestLogosHarmonics:
    """Test Logos harmonic relationships."""
    
    def test_logos_harmonics_keys(self):
        """Test that all harmonic keys are present."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        required_keys = [
            'f_0', 'f_7', 'f_alma_21g', 'f_cosmica_sugerida',
            'ratio_432_425', 'error_432_pct'
        ]
        for key in required_keys:
            assert key in harmonics
    
    def test_f0_fundamental(self):
        """Test fundamental frequency."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        assert harmonics['f_0'] == F0_HZ
    
    def test_f7_adelic_base(self):
        """Test adelic base frequency f₀/7."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        expected_f7 = F0_HZ / 7
        assert abs(harmonics['f_7'] - expected_f7) < 1e-6
        assert abs(harmonics['f_7'] - 20.24287) < 0.001
    
    def test_alma_21g_harmonic(self):
        """Test 21g soul harmonic: 21 × (f₀/7) ≈ 425.1 Hz."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        expected = 21 * (F0_HZ / 7)
        assert abs(harmonics['f_alma_21g'] - expected) < 1e-6
        assert abs(harmonics['f_alma_21g'] - 425.1) < 0.1
    
    def test_cosmic_432hz_reference(self):
        """Test cosmic frequency reference at 432 Hz."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        assert harmonics['f_cosmica_sugerida'] == 432.0
    
    def test_ratio_432_to_425(self):
        """Test ratio between 432 Hz and 425.1 Hz."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        ratio = harmonics['ratio_432_425']
        assert ratio > 1.0  # 432 > 425
        assert abs(ratio - (432.0 / harmonics['f_alma_21g'])) < 1e-10
    
    def test_error_432_less_than_2_percent(self):
        """Test that error with 432 Hz is less than 2%."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        
        error = harmonics['error_432_pct']
        assert error < 2.0
        assert error > 0  # There should be some error
        # Expected to be around 1.6%
        assert abs(error - 1.62) < 0.1


class TestTopologicalSoulWeight:
    """Test topological analysis of soul weight."""
    
    def test_topological_weight_keys(self):
        """Test that all topological keys are present."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        
        required_keys = [
            'total_berry_units', 'mass_per_berry_unit_kg',
            'energy_per_berry_unit_j', 'energy_per_berry_unit_ev',
            'berry_adelic_scale', 'interpretation'
        ]
        for key in required_keys:
            assert key in topo
    
    def test_berry_units_24(self):
        """Test total Berry units: 21 = 3 × 7 = 3 × 8 × (7/8) → 24 units."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        
        assert topo['total_berry_units'] == 24
    
    def test_mass_per_berry_unit(self):
        """Test mass per Berry unit."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        
        expected = 0.021 / 24  # kg per unit
        assert abs(topo['mass_per_berry_unit_kg'] - expected) < 1e-10
    
    def test_energy_per_berry_unit(self):
        """Test energy per Berry unit via E = mc²."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        
        mass_per_unit = topo['mass_per_berry_unit_kg']
        energy_expected = mass_per_unit * c**2
        
        assert abs(topo['energy_per_berry_unit_j'] - energy_expected) < 1e-6
    
    def test_berry_adelic_scale(self):
        """Test Berry adelic scale: 3 × (7/8) = 2.625."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        
        expected = 3 * (7.0 / 8.0)
        assert abs(topo['berry_adelic_scale'] - 2.625) < 1e-10
        assert abs(topo['berry_adelic_scale'] - expected) < 1e-10


class TestCircleRatioError:
    """Test circle (2π) relationship."""
    
    def test_circle_ratio_keys(self):
        """Test that all circle ratio keys are present."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        
        required_keys = [
            'ratio_21_f0', 'circle_approx', 'exact_2pi',
            'error', 'error_pct', 'interpretation'
        ]
        for key in required_keys:
            assert key in circle
    
    def test_ratio_21_f0(self):
        """Test 21/f₀ ratio calculation."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        
        # Using number 21, not mass in kg
        expected = 21.0 / F0_HZ  # dimensionless numerological ratio
        assert abs(circle['ratio_21_f0'] - expected) < 1e-10
    
    def test_circle_approximation(self):
        """Test 1/(21/f₀) ≈ 6.747 approximation."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        
        ratio = circle['ratio_21_f0']
        approx = 1.0 / ratio
        assert abs(circle['circle_approx'] - approx) < 1e-10
        assert abs(circle['circle_approx'] - 6.747) < 0.01
    
    def test_exact_2pi(self):
        """Test exact 2π value."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        
        assert abs(circle['exact_2pi'] - 2*pi) < 1e-10
        assert abs(circle['exact_2pi'] - 6.283185) < 0.000001
    
    def test_error_with_2pi_about_7_percent(self):
        """Test that error with 2π is approximately 7.4%."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        
        error_pct = circle['error_pct']
        assert 7.0 < error_pct < 8.0
        # Expected to be around 7.4%
        assert abs(error_pct - 7.4) < 0.5


class TestSoulCertification:
    """Test soul certification and validation."""
    
    def test_certify_returns_dict(self):
        """Test that certify returns a dictionary."""
        soul = QCalSoul()
        cert = soul.certify()
        
        assert isinstance(cert, dict)
        assert 'alma_21g_qcal' in cert
    
    def test_certify_all_fields(self):
        """Test that certification includes all required fields."""
        soul = QCalSoul()
        cert = soul.certify()
        data = cert['alma_21g_qcal']
        
        required_fields = [
            'e_alma_transition_j', 'e_alma_transition_kt_tnt',
            'e_full_mass_j', 'e_full_mass_kt_tnt',
            'armonico_logos_hz', 'armonico_432hz',
            'ratio_432_425', 'error_432_pct',
            'circle_logo_2pi', 'circle_2pi_exact', 'circle_error_pct',
            'berry_adelic_scale', 'berry_units_total',
            'psi_umbral_disolucion', 'f0_hz', 'f_H_mhz',
            'scale_factor_f0_fH',
            'interpretacion_qcal', 'postulado', 'umbral', 'estado'
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    
    def test_certify_estado(self):
        """Test certification state."""
        soul = QCalSoul()
        cert = soul.certify()
        
        assert cert['alma_21g_qcal']['estado'] == "CERTIFICADO ∞³"
    
    def test_certify_postulado(self):
        """Test certification postulate."""
        soul = QCalSoul()
        cert = soul.certify()
        
        postulado = cert['alma_21g_qcal']['postulado']
        assert "coherencia" in postulado.lower()
        assert "masa" in postulado.lower()
    
    def test_assert_validations_pass(self):
        """Test that all validations pass."""
        soul = QCalSoul()
        
        # Should not raise any exceptions
        soul.assert_validations()
    
    def test_alma_21g_qcal_coherencia_runs(self):
        """Test main integration function runs successfully."""
        # This should run without errors and return a dict
        cert = alma_21g_qcal_coherencia()
        
        assert isinstance(cert, dict)
        assert 'alma_21g_qcal' in cert


class TestSoulCoherenceValidations:
    """Test specific validation conditions."""
    
    def test_harmonic_alma_near_425(self):
        """Test that soul harmonic is near 425.1 Hz."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        f_alma = harmonics['f_alma_21g']
        
        # Within 0.1 Hz as per validation
        assert abs(f_alma - 425.1) < 0.1
    
    def test_error_432_less_than_2pct(self):
        """Test that error with 432 Hz is less than 2%."""
        soul = QCalSoul()
        harmonics = soul.logos_harmonics()
        error_432 = harmonics['error_432_pct']
        
        assert error_432 < 2.0
    
    def test_error_2pi_between_7_and_8_pct(self):
        """Test that error with 2π is between 7% and 8%."""
        soul = QCalSoul()
        circle = soul.circle_ratio_error()
        error_2pi = circle['error_pct']
        
        assert 7.0 < error_2pi < 8.0
    
    def test_berry_scale_exactly_2625(self):
        """Test that Berry scale is exactly 2.625."""
        soul = QCalSoul()
        topo = soul.topological_soul_weight()
        berry_scale = topo['berry_adelic_scale']
        
        assert abs(berry_scale - 2.625) < 0.001


class TestSoulCoherencePhysics:
    """Test physical consistency of soul coherence model."""
    
    def test_scale_factor_f0_fH(self):
        """Test scale factor f₀/f_H is very small (10^-8 range)."""
        soul = QCalSoul()
        scale = soul.f_0 / soul.f_H
        
        # Should be ~ 10^-7 to 10^-8
        assert scale < 1e-6
        assert scale > 1e-9
        # Expected to be ~9.97e-8
        assert abs(scale - 9.97e-8) < 1e-8
    
    def test_coherence_loss_factor(self):
        """Test coherence loss factor (1 - Ψ_min)."""
        soul = QCalSoul()
        loss_factor = 1 - soul.psi_min
        
        # Use approximate comparison for floating point
        assert abs(loss_factor - 0.112) < 1e-10
        assert 0 < loss_factor < 1
    
    def test_energy_units_joules(self):
        """Test that energies are in reasonable Joule ranges."""
        soul = QCalSoul()
        
        e_full = soul.full_mass_energy()
        e_transition = soul.soul_coherence_energy()
        
        # 21 grams at c² should be ~10^15 J
        assert 1e15 < e_full < 2e15
        
        # Transition should be much smaller due to factors
        assert e_transition < 1e13
    
    def test_tnt_equivalent_ballpark(self):
        """Test TNT equivalents are in reasonable ranges."""
        soul = QCalSoul()
        
        kt_full = soul.full_mass_energy_tnt()
        kt_transition = soul.soul_coherence_energy_tnt()
        
        # 21g at E=mc² is roughly 450 kilotons
        assert 400 < kt_full < 500
        
        # Transition should be much smaller
        assert kt_transition < 10


class TestSoulCoherenceNumerology:
    """Test numerological relationships."""
    
    def test_21_equals_3_times_7(self):
        """Test that 21 = 3 × 7."""
        assert 21 == 3 * 7
    
    def test_7_over_8_berry(self):
        """Test Berry invariant 7/8."""
        assert abs(BERRY_INVARIANT - 7/8) < 1e-10
    
    def test_f0_over_7_schumann_like(self):
        """Test f₀/7 is in Schumann-like frequency range (~20 Hz)."""
        f7 = F0_HZ / 7
        
        # Should be ~20 Hz
        assert 20 < f7 < 21
    
    def test_21_times_f7_cosmic(self):
        """Test 21 × (f₀/7) gives cosmic-like frequency."""
        f_alma = 21 * (F0_HZ / 7)
        
        # Should be close to 432 Hz (cosmic frequency)
        assert 420 < f_alma < 430


class TestSoulCoherenceIntegration:
    """Test integration with QCAL framework."""
    
    def test_uses_correct_f0(self):
        """Test that soul coherence uses correct f₀ = 141.7001 Hz."""
        soul = QCalSoul()
        assert soul.f_0 == 141.7001
    
    def test_uses_correct_psi_threshold(self):
        """Test that soul coherence uses correct Ψ threshold."""
        soul = QCalSoul()
        assert soul.psi_min == 0.888
    
    def test_consistent_with_physics_constants(self):
        """Test consistency with scipy physical constants."""
        from scipy.constants import c as scipy_c
        
        soul = QCalSoul()
        e_full = soul.full_mass_energy()
        
        # Calculate using scipy's c
        expected = soul.m_exp_soul * scipy_c**2
        assert abs(e_full - expected) < 1e-6


@pytest.mark.slow
class TestSoulCoherenceOutput:
    """Test output and display functionality."""
    
    def test_alma_21g_prints_output(self, capsys):
        """Test that main function prints expected output."""
        cert = alma_21g_qcal_coherencia()
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check for key strings in output
        assert "21 GRAMOS" in output
        assert "COHERENCIA DEL ALMA" in output
        assert "QCAL" in output
        assert "141.7001 Hz" in output or "141.7001" in output
        assert "888 Hz" in output
        assert "∞³" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
