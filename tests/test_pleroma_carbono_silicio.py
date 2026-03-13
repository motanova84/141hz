#!/usr/bin/env python3
"""
Tests for Pleroma Carbono-Silicio Module

Validates the Carbon-Silicon Pleroma constants and beat (batimiento) functions:
  - Silicon Divine:   f_Si = 141.7001 Hz
  - Carbon Divine:    f_C  = 142.1000 Hz
  - Ziusudra Constant: Δf = 0.3999 Hz
  - Incarnation Tension: κ = f_C/f_Si ≈ 1.002822
  - Sacred Beat Period:  T ≈ 2.5006 s
  - H_Total = H_Riemann + H_Interaccion
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from fisica.pleroma_carbono_silicio import (
    F_SILICIO_DIVINO,
    F_SI,
    F_CARBONO_DIVINO,
    F_C,
    CONSTANTE_ZIUSUDRA,
    DELTA_F_ZIUSUDRA,
    DELTA_F,
    TENSION_ENCARNACION,
    KAPPA_ENCARNACION,
    PERIODO_BATIMIENTO_S,
    FRECUENCIA_BATIMIENTO,
    calcular_batimiento,
    coherencia_psi,
    hamiltoniano_total,
    frecuencia_media_pleroma,
)
from fisica.FRECUENCIAS_SAGRADAS import F0_HZ


class TestFrecuenciasFundamentales:
    """Tests for fundamental Carbon-Silicon frequency constants."""

    def test_silicio_divino_equals_f0(self):
        """Silicon Divine must equal the fundamental f₀ = 141.7001 Hz."""
        assert F_SILICIO_DIVINO == pytest.approx(141.7001, abs=1e-4)
        assert F_SI == pytest.approx(141.7001, abs=1e-4)

    def test_silicio_divino_is_f0(self):
        """F_SILICIO_DIVINO must be the same value as F0_HZ."""
        assert F_SILICIO_DIVINO == F0_HZ

    def test_carbono_divino_value(self):
        """Carbon Divine must be exactly 142.1000 Hz."""
        assert F_CARBONO_DIVINO == pytest.approx(142.1000, abs=1e-4)
        assert F_C == pytest.approx(142.1000, abs=1e-4)

    def test_carbono_greater_than_silicio(self):
        """Carbon frequency must be greater than Silicon (life needs more energy)."""
        assert F_CARBONO_DIVINO > F_SILICIO_DIVINO

    def test_alias_consistency(self):
        """Short aliases must match full names."""
        assert F_SI == F_SILICIO_DIVINO
        assert F_C == F_CARBONO_DIVINO


class TestConstanteZiusudra:
    """Tests for the Ziusudra Constant (Δf = 0.3999 Hz)."""

    def test_delta_f_value(self):
        """Δf must equal exactly 0.3999 Hz."""
        assert CONSTANTE_ZIUSUDRA == pytest.approx(0.3999, abs=1e-9)

    def test_delta_f_is_difference(self):
        """Δf must equal f_C − f_Si."""
        assert CONSTANTE_ZIUSUDRA == pytest.approx(F_CARBONO_DIVINO - F_SILICIO_DIVINO, abs=1e-9)

    def test_delta_f_aliases(self):
        """All Δf aliases must be equal."""
        assert DELTA_F_ZIUSUDRA == CONSTANTE_ZIUSUDRA
        assert DELTA_F == CONSTANTE_ZIUSUDRA
        assert FRECUENCIA_BATIMIENTO == CONSTANTE_ZIUSUDRA

    def test_delta_f_positive(self):
        """Ziusudra constant must be positive."""
        assert CONSTANTE_ZIUSUDRA > 0


class TestTensionEncarnacion:
    """Tests for Incarnation Tension (κ = f_C / f_Si ≈ 1.002822)."""

    def test_tension_value(self):
        """Incarnation tension must be ≈ 1.002822."""
        assert TENSION_ENCARNACION == pytest.approx(1.002822, abs=1e-5)

    def test_tension_is_ratio(self):
        """κ must equal f_C / f_Si."""
        expected = F_CARBONO_DIVINO / F_SILICIO_DIVINO
        assert TENSION_ENCARNACION == pytest.approx(expected, abs=1e-10)

    def test_tension_alias(self):
        """KAPPA_ENCARNACION alias must match."""
        assert KAPPA_ENCARNACION == TENSION_ENCARNACION

    def test_tension_greater_than_one(self):
        """κ > 1 because the Carbon stretches beyond the Silicon geometry."""
        assert TENSION_ENCARNACION > 1.0

    def test_tension_near_one(self):
        """κ must be very close to 1 (small perturbation)."""
        assert abs(TENSION_ENCARNACION - 1.0) < 0.005


class TestPeriodoBatimiento:
    """Tests for the sacred beat period T ≈ 2.5003 s."""

    def test_periodo_value(self):
        """Beat period must be exactly 1/0.3999 ≈ 2.50063 s."""
        assert PERIODO_BATIMIENTO_S == pytest.approx(1.0 / 0.3999, abs=1e-9)

    def test_periodo_is_inverse_of_delta_f(self):
        """T_beat = 1 / Δf."""
        assert PERIODO_BATIMIENTO_S == pytest.approx(1.0 / CONSTANTE_ZIUSUDRA, abs=1e-9)

    def test_periodo_near_2_5_seconds(self):
        """Beat period must be approximately 2.5 seconds."""
        assert 2.4 < PERIODO_BATIMIENTO_S < 2.6


class TestCalcularBatimiento:
    """Tests for the beat simulation function calcular_batimiento(t)."""

    def test_returns_tuple_of_three(self):
        """Function must return a 3-tuple (psi, envolvente, portadora)."""
        result = calcular_batimiento(0.0)
        assert len(result) == 3

    def test_psi_at_zero(self):
        """At t=0, both sinusoids are zero, so Ψ(0) = 0."""
        psi, envolvente, portadora = calcular_batimiento(0.0)
        assert psi == pytest.approx(0.0, abs=1e-10)

    def test_envelope_at_zero_is_maximum(self):
        """At t=0, the beat envelope must be at maximum = 2."""
        _, envolvente, _ = calcular_batimiento(0.0)
        assert envolvente == pytest.approx(2.0, abs=1e-10)

    def test_psi_sum_of_two_sinusoids(self):
        """Ψ(t) = sin(2π·f_Si·t) + sin(2π·f_C·t) for any t."""
        for t in [0.1, 0.5, 1.0, 1.25, 2.5]:
            psi, _, _ = calcular_batimiento(t)
            expected = (math.sin(2 * math.pi * F_SILICIO_DIVINO * t) +
                        math.sin(2 * math.pi * F_CARBONO_DIVINO * t))
            assert psi == pytest.approx(expected, abs=1e-10), f"Failed at t={t}"

    def test_envelope_identity(self):
        """Envelope = 2·|cos(π·Δf·t)|."""
        for t in [0.0, 0.3, 0.625, 1.25]:
            _, envolvente, _ = calcular_batimiento(t)
            expected = 2.0 * abs(math.cos(math.pi * CONSTANTE_ZIUSUDRA * t))
            assert envolvente == pytest.approx(expected, abs=1e-10), f"Failed at t={t}"

    def test_envelope_non_negative(self):
        """Envelope must always be ≥ 0."""
        for t in [i * 0.1 for i in range(50)]:
            _, envolvente, _ = calcular_batimiento(t)
            assert envolvente >= 0.0

    def test_psi_bounded_by_envelope(self):
        """|Ψ(t)| ≤ envelope(t) at all times."""
        for t in [i * 0.05 for i in range(100)]:
            psi, envolvente, _ = calcular_batimiento(t)
            assert abs(psi) <= envolvente + 1e-9, f"Bound violated at t={t}"


class TestCoherenciaPsi:
    """Tests for the normalised coherence function coherencia_psi(t)."""

    def test_max_at_zero(self):
        """Coherence is maximum (1.0) at t=0."""
        assert coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_zero_at_quarter_period(self):
        """Coherence is minimum (0.0) at t = T/2, where T is beat period."""
        t_half = PERIODO_BATIMIENTO_S / 2.0
        assert coherencia_psi(t_half) == pytest.approx(0.0, abs=1e-10)

    def test_max_at_full_period(self):
        """Coherence returns to maximum at t = T (full beat period)."""
        assert coherencia_psi(PERIODO_BATIMIENTO_S) == pytest.approx(1.0, abs=1e-9)

    def test_range_zero_to_one(self):
        """Coherence must always be in [0, 1]."""
        for t in [i * 0.1 for i in range(100)]:
            psi = coherencia_psi(t)
            assert 0.0 <= psi <= 1.0 + 1e-10, f"Out of range at t={t}"

    def test_formula(self):
        """Ψ(t) = |cos(π·Δf·t)|."""
        for t in [0.0, 0.3, 0.625, 1.25, 2.5]:
            expected = abs(math.cos(math.pi * CONSTANTE_ZIUSUDRA * t))
            assert coherencia_psi(t) == pytest.approx(expected, abs=1e-10), f"Failed at t={t}"


class TestHamiltoniano:
    """Tests for the total Hamiltonian H_Total = H_Riemann + H_Interaccion."""

    GAMMA_1 = 14.134725141734693  # First non-trivial Riemann zero

    def test_at_gamma_1_no_perturbation(self):
        """H_Total(γ₁, ε=0) = f_Si + Δf = f_C."""
        result = hamiltoniano_total(self.GAMMA_1, epsilon_termico=0.0)
        # H_Riemann(γ₁) = f_Si · (γ₁/γ₁) = f_Si
        # H_Interaccion = Δf
        # H_Total = f_Si + Δf = f_C
        assert result == pytest.approx(F_CARBONO_DIVINO, abs=1e-6)

    def test_riemann_component_scales_with_gamma(self):
        """H_Riemann scales linearly with γₙ."""
        h1 = hamiltoniano_total(self.GAMMA_1, 0.0)
        h2 = hamiltoniano_total(2 * self.GAMMA_1, 0.0)
        # H_Riemann(2γ₁) = 2·f_Si, so H_Total(2γ₁) = 2·f_Si + Δf
        expected = 2 * F_SILICIO_DIVINO + CONSTANTE_ZIUSUDRA
        assert h2 == pytest.approx(expected, abs=1e-6)

    def test_perturbation_increases_hamiltonian(self):
        """Positive thermal perturbation increases H_Total."""
        h_base = hamiltoniano_total(self.GAMMA_1, 0.0)
        h_perturbed = hamiltoniano_total(self.GAMMA_1, 0.1)
        assert h_perturbed > h_base

    def test_interaction_term_without_perturbation(self):
        """H_Interaccion(ε=0) = Δf exactly."""
        # H_Total = H_Riemann + H_Interaccion
        # H_Riemann(γ₁) = f_Si, H_Interaccion = Δf*(1+0)
        result = hamiltoniano_total(self.GAMMA_1, 0.0)
        h_riemann = F_SILICIO_DIVINO * (self.GAMMA_1 / self.GAMMA_1)
        h_interaccion = CONSTANTE_ZIUSUDRA * 1.0
        assert result == pytest.approx(h_riemann + h_interaccion, abs=1e-10)


class TestFrecuenciaMedia:
    """Tests for the Pleroma centre frequency."""

    def test_media_value(self):
        """Mean frequency must be (f_Si + f_C) / 2."""
        expected = (F_SILICIO_DIVINO + F_CARBONO_DIVINO) / 2.0
        assert frecuencia_media_pleroma() == pytest.approx(expected, abs=1e-10)

    def test_media_between_poles(self):
        """Mean frequency must lie strictly between f_Si and f_C."""
        media = frecuencia_media_pleroma()
        assert F_SILICIO_DIVINO < media < F_CARBONO_DIVINO

    def test_media_approximate_value(self):
        """Mean frequency ≈ 141.9001 Hz."""
        assert frecuencia_media_pleroma() == pytest.approx(141.9001, abs=1e-4)


class TestImportFromFisicaPackage:
    """Verify that constants are accessible via the fisica package."""

    def test_import_via_package(self):
        """All Pleroma constants must be importable from fisica directly."""
        from fisica import (
            F_SILICIO_DIVINO as fsi,
            F_CARBONO_DIVINO as fc,
            CONSTANTE_ZIUSUDRA as dz,
            TENSION_ENCARNACION as te,
            PERIODO_BATIMIENTO_S as pb,
        )
        assert fsi == pytest.approx(141.7001, abs=1e-4)
        assert fc == pytest.approx(142.1000, abs=1e-4)
        assert dz == pytest.approx(0.3999, abs=1e-9)
        assert te == pytest.approx(1.002822, abs=1e-5)
        assert 2.4 < pb < 2.6
