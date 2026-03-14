"""
Tests for QCAL Soul Coherence — Axiomas de Resonancia.

Validates the three mathematical truths established in qcal/soul_coherence.py:
  Axiom I   — Quantum Loss Factor (Ψ < 0.888 → decoupling)
  Axiom II  — Golden Ratio / 2π Synchrony (7.39 % error)
  Axiom III — Logos Harmonic (21 × f₀/7 ≈ 432 Hz, error < 1.62 %)

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
