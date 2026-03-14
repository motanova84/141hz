#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for πCODE Frequency Verification.

Validates the sealed mathematical chain f₀ = γ₁ × (10 + 1/40),
the verificar_frecuencia() helper, and the full holographic structure
defined in core/zeta_holo_f0.py.

Author: JMMB Ψ✧ (motanova84)
Instituto de Conciencia Cuántica (ICQ) – QCAL ∞³
"""

import math
import os
import sys
import pytest

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.qcal_master_constants import (
    GAMMA_1,
    MULTIPLICADOR_PICODE,
    F0_EXACTA_PICODE,
    DELTA_FASE_PICODE,
    FISURA_ZIUSUDRA,
)
from scripts.verifica_frecuencia import (
    verificar_frecuencia,
    f_esperada,
)
from core.zeta_holo_f0 import (
    SuperficieZeta,
    VolumenConsciente,
    HologramaZeta,
    EstadoCoherencia,
    verificar_estructura_picode,
    F0_NOMINAL_HZ,
)


# ---------------------------------------------------------------------------
# Constants sanity
# ---------------------------------------------------------------------------
class TestPiCodeConstants:
    """Tests for the πCODE master constants."""

    def test_gamma_1_value(self):
        """γ₁ must be the first Riemann zero ≈ 14.1347."""
        assert GAMMA_1 == pytest.approx(14.134725141734693, rel=1e-10)

    def test_multiplicador_picode(self):
        """MULTIPLICADOR_PICODE == 10 + 1/40 == 10.025 (exact)."""
        assert MULTIPLICADOR_PICODE == pytest.approx(10 + 1 / 40, abs=1e-15)

    def test_f0_exacta_derivation(self):
        """F0_EXACTA_PICODE == GAMMA_1 × MULTIPLICADOR_PICODE."""
        assert F0_EXACTA_PICODE == pytest.approx(GAMMA_1 * MULTIPLICADOR_PICODE, rel=1e-12)

    def test_f0_exacta_approx_value(self):
        """F0_EXACTA_PICODE ≈ 141.700 Hz (within 1 Hz of nominal)."""
        assert abs(F0_EXACTA_PICODE - 141.7001) < 1.0

    def test_delta_fase_derivation(self):
        """DELTA_FASE_PICODE == GAMMA_1 / 40."""
        assert DELTA_FASE_PICODE == pytest.approx(GAMMA_1 / 40.0, rel=1e-12)

    def test_delta_fase_approx_value(self):
        """DELTA_FASE_PICODE ≈ 0.35337 Hz."""
        assert DELTA_FASE_PICODE == pytest.approx(0.35337, abs=1e-4)

    def test_fisura_ziusudra_derivation(self):
        """FISURA_ZIUSUDRA == F0_EXACTA_PICODE - 141.7001."""
        assert FISURA_ZIUSUDRA == pytest.approx(F0_EXACTA_PICODE - 141.7001, abs=1e-10)

    def test_fisura_ziusudra_positive(self):
        """πCODE f₀ is above the nominal 141.7001 Hz → fisura > 0."""
        assert FISURA_ZIUSUDRA > 0.0

    def test_fisura_ziusudra_small(self):
        """Fisura is sub-millihertz in magnitude."""
        assert abs(FISURA_ZIUSUDRA) < 0.01


# ---------------------------------------------------------------------------
# verifica_frecuencia()
# ---------------------------------------------------------------------------
class TestVerificarFrecuencia:
    """Tests for scripts.verifica_frecuencia.verificar_frecuencia()."""

    def test_f_esperada_equals_f0_exacta(self):
        """f_esperada must equal F0_EXACTA_PICODE."""
        assert f_esperada == pytest.approx(F0_EXACTA_PICODE, rel=1e-12)

    def test_exact_frequency_passes(self):
        """Exact f_esperada must always verify."""
        assert verificar_frecuencia(f_esperada) is True

    def test_frequency_within_default_tolerance(self):
        """Frequency within 1e-4 relative tolerance must verify."""
        delta = f_esperada * 1e-4  # exactly at the boundary
        assert verificar_frecuencia(f_esperada + delta * 0.99) is True
        assert verificar_frecuencia(f_esperada - delta * 0.99) is True

    def test_frequency_at_boundary(self):
        """Frequency exactly at boundary (tolerancia=1e-4) must verify."""
        delta = f_esperada * 1e-4
        assert verificar_frecuencia(f_esperada + delta) is True

    def test_frequency_outside_default_tolerance(self):
        """Frequency outside 1e-4 relative tolerance must not verify."""
        delta = f_esperada * 1e-4 * 1.01  # just over the boundary
        assert verificar_frecuencia(f_esperada + delta) is False

    def test_nominal_f0_passes_default_tolerance(self):
        """Nominal 141.7001 Hz is within the default 1e-4 tolerance."""
        # |141.7001 - F0_EXACTA_PICODE| / F0_EXACTA_PICODE ≈ 3.7e-6 << 1e-4
        assert verificar_frecuencia(F0_NOMINAL_HZ) is True

    def test_clearly_wrong_frequency_fails(self):
        """A frequency far from f₀ must not verify."""
        assert verificar_frecuencia(100.0) is False
        assert verificar_frecuencia(200.0) is False
        assert verificar_frecuencia(0.0) is False

    def test_custom_tight_tolerance(self):
        """Tight tolerance rejects a frequency just outside it."""
        tolerancia = 1e-6
        delta = f_esperada * tolerancia * 1.1  # 10% over tight threshold
        assert verificar_frecuencia(f_esperada + delta, tolerancia=tolerancia) is False

    def test_returns_bool(self):
        """Return type must be bool."""
        result = verificar_frecuencia(f_esperada)
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# SuperficieZeta
# ---------------------------------------------------------------------------
class TestSuperficieZeta:
    """Tests for core.zeta_holo_f0.SuperficieZeta."""

    def test_default_uses_f0_exacta(self):
        sup = SuperficieZeta()
        assert sup.f0 == pytest.approx(F0_EXACTA_PICODE, rel=1e-12)

    def test_lambda_m(self):
        """λ = c / f₀  (≈ 2.115683 × 10⁶ m)."""
        sup = SuperficieZeta()
        expected = 299_792_458.0 / F0_EXACTA_PICODE
        assert sup.lambda_m == pytest.approx(expected, rel=1e-10)

    def test_lambda_mm(self):
        """λ in Mm ≈ 2.116 Mm."""
        sup = SuperficieZeta()
        assert 2.0 < sup.lambda_mm < 2.2

    def test_area_efectiva(self):
        """Effective area = 4π λ² (positive)."""
        sup = SuperficieZeta()
        expected = 4.0 * math.pi * sup.lambda_m ** 2
        assert sup.area_efectiva_m2 == pytest.approx(expected, rel=1e-10)

    def test_bits_bekenstein_positive(self):
        """Bekenstein-Hawking bit count must be large and positive."""
        sup = SuperficieZeta()
        assert sup.bits_bekenstein > 1e60

    def test_resumen_keys(self):
        """resumen() must return the expected keys."""
        sup = SuperficieZeta()
        keys = set(sup.resumen().keys())
        assert {"f0_hz", "lambda_m", "lambda_mm", "area_efectiva_m2", "bits_bekenstein"} <= keys


# ---------------------------------------------------------------------------
# VolumenConsciente
# ---------------------------------------------------------------------------
class TestVolumenConsciente:
    """Tests for core.zeta_holo_f0.VolumenConsciente."""

    def test_simbiosis_silicio_carbono(self):
        vol = VolumenConsciente(psi=0.9999)
        assert vol.estado == EstadoCoherencia.SIMBIOSIS_SILICIO_CARBONO

    def test_coherencia_alta(self):
        vol = VolumenConsciente(psi=0.999)
        assert vol.estado == EstadoCoherencia.COHERENCIA_ALTA

    def test_resonancia_activa(self):
        vol = VolumenConsciente(psi=0.95)
        assert vol.estado == EstadoCoherencia.RESONANCIA_ACTIVA

    def test_calibrando(self):
        vol = VolumenConsciente(psi=0.5)
        assert vol.estado == EstadoCoherencia.CALIBRANDO

    def test_perfect_coherence_is_simbiosis(self):
        vol = VolumenConsciente(psi=1.0)
        assert vol.estado == EstadoCoherencia.SIMBIOSIS_SILICIO_CARBONO

    def test_es_coherente_default(self):
        assert VolumenConsciente(psi=0.95).es_coherente() is True
        assert VolumenConsciente(psi=0.5).es_coherente() is False

    def test_invalid_psi_raises(self):
        with pytest.raises(ValueError):
            VolumenConsciente(psi=1.1)
        with pytest.raises(ValueError):
            VolumenConsciente(psi=-0.1)


# ---------------------------------------------------------------------------
# HologramaZeta
# ---------------------------------------------------------------------------
class TestHologramaZeta:
    """Tests for core.zeta_holo_f0.HologramaZeta."""

    def test_initialization(self):
        holo = HologramaZeta(psi=0.999)
        assert holo.f0 == pytest.approx(F0_EXACTA_PICODE, rel=1e-12)
        assert holo.gamma_1 == pytest.approx(GAMMA_1, rel=1e-12)
        assert holo.delta_fase == pytest.approx(DELTA_FASE_PICODE, rel=1e-12)
        assert holo.fisura == pytest.approx(FISURA_ZIUSUDRA, abs=1e-10)

    def test_resumen_keys(self):
        holo = HologramaZeta(psi=0.999)
        keys = set(holo.resumen().keys())
        expected = {
            "f0_hz", "gamma_1", "delta_fase_hz", "fisura_ziusudra_hz",
            "psi", "estado_coherencia", "lambda_mm", "bits_bekenstein",
        }
        assert expected <= keys

    def test_analisis_fft_rebote_lunar(self):
        holo = HologramaZeta(psi=0.999)
        result = holo.analisis_fft_rebote_lunar()
        # Peak should be near f₀ + δ_fase
        assert result["f_pico_hz"] == pytest.approx(F0_EXACTA_PICODE + DELTA_FASE_PICODE, rel=1e-10)
        # Modulation == δ_fase
        assert result["f_modulacion_hz"] == pytest.approx(DELTA_FASE_PICODE, rel=1e-10)
        # Lunar round-trip delay ≈ 2.56 s
        assert 2.5 < result["retardo_lunar_s"] < 2.7
        # Coherence after rebound is ≤ original Ψ
        assert result["coherencia_rebote"] <= 0.999

    def test_surface_volume_duality(self):
        """The surface λ_{mm} must match the SuperficieZeta independently."""
        holo = HologramaZeta(psi=1.0)
        sup = SuperficieZeta(f0=F0_EXACTA_PICODE)
        assert holo.superficie.lambda_mm == pytest.approx(sup.lambda_mm, rel=1e-10)


# ---------------------------------------------------------------------------
# verificar_estructura_picode()
# ---------------------------------------------------------------------------
class TestVerificarEstructuraPiCode:
    """Tests for the sealed πCODE chain validator."""

    def test_returns_true(self):
        assert verificar_estructura_picode() is True

    def test_tight_tolerance(self):
        assert verificar_estructura_picode(tolerancia_relativa=1e-10) is True
