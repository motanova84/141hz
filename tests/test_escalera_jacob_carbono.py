#!/usr/bin/env python3
"""
Tests for Escalera de Jacob del Carbono (QCAL ∞³)

Validates all 8 classes and the public API:
  ConstantesEscaleraJacob — Parámetros fundamentales (7 constantes)
  SecuenciaAurea          — Progresión Φ: f_n = F_JACOB · Φⁿ
  GuardianCarbono         — Representación individual de un guardián
  CoherenciaCarbono       — Coherencia ponderada del campo de Carbono
  AtractorDilmun          — Atractor territorial de 888 Hz
  BatimientoCarbonoSilicio — Batimiento sagrado Δf = 0.3999 Hz
  CoronaUtuabzu           — Corona UTUABZU en Φ⁶
  SistemaEscaleraJacob    — Orquestador + Ψ_global ≥ 0.888
  escalera_jacob_activar() — API pública

≥ 80 tests — Ψ_global ≥ 0.888
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.escalera_jacob_carbono import (
    # Constants
    F_JACOB, F_SI, DELTA_F, PHI, F_MANIF, N_GUARD, PSI_UMBRAL,
    # Classes
    ConstantesEscaleraJacob,
    SecuenciaAurea,
    GuardianCarbono,
    CoherenciaCarbono,
    AtractorDilmun,
    BatimientoCarbonoSilicio,
    CoronaUtuabzu,
    SistemaEscaleraJacob,
    # API
    escalera_jacob_activar,
)


# ============================================================================
# TestConstantesModulo  (10 tests)
# ============================================================================

class TestConstantesModulo:
    """Tests for the 7 module-level constants."""

    def test_f_jacob_value(self):
        """F_JACOB must equal 142.1 Hz (Carbono Divino ADAPA)."""
        assert F_JACOB == pytest.approx(142.1, abs=1e-4)

    def test_f_si_value(self):
        """F_SI must equal 141.7001 Hz (Silicio Divino)."""
        assert F_SI == pytest.approx(141.7001, abs=1e-4)

    def test_delta_f_value(self):
        """DELTA_F must equal F_JACOB − F_SI ≈ 0.3999 Hz."""
        assert DELTA_F == pytest.approx(F_JACOB - F_SI, abs=1e-9)

    def test_delta_f_approx(self):
        """DELTA_F ≈ 0.3999 Hz."""
        assert DELTA_F == pytest.approx(0.3999, abs=1e-4)

    def test_phi_is_golden_ratio(self):
        """PHI = (1 + sqrt(5)) / 2."""
        assert PHI == pytest.approx((1.0 + math.sqrt(5.0)) / 2.0, abs=1e-12)

    def test_phi_self_similarity(self):
        """PHI² = PHI + 1 (self-similarity of the golden ratio)."""
        assert PHI ** 2 == pytest.approx(PHI + 1.0, abs=1e-10)

    def test_f_manif_888(self):
        """F_MANIF must equal 888.0 Hz (Frecuencia de Manifestación)."""
        assert F_MANIF == pytest.approx(888.0, abs=1e-6)

    def test_n_guard_seven(self):
        """N_GUARD must be 7 (seven guardians of the Jacob's Ladder)."""
        assert N_GUARD == 7

    def test_psi_umbral(self):
        """PSI_UMBRAL must be 0.888 (minimum coherence threshold QCAL ∞³)."""
        assert PSI_UMBRAL == pytest.approx(0.888, abs=1e-6)

    def test_f_jacob_greater_than_f_si(self):
        """F_JACOB > F_SI (Carbon is above Silicon)."""
        assert F_JACOB > F_SI


# ============================================================================
# TestConstantesEscaleraJacob  (8 tests)
# ============================================================================

class TestConstantesEscaleraJacob:
    """Tests for ConstantesEscaleraJacob class."""

    def setup_method(self):
        self.c = ConstantesEscaleraJacob()

    def test_f_jacob_stored(self):
        assert self.c.f_jacob == pytest.approx(142.1, abs=1e-4)

    def test_f_si_stored(self):
        assert self.c.f_si == pytest.approx(141.7001, abs=1e-4)

    def test_delta_f_stored(self):
        assert self.c.delta_f == pytest.approx(DELTA_F, abs=1e-9)

    def test_phi_stored(self):
        assert self.c.phi == pytest.approx(PHI, abs=1e-12)

    def test_f_manif_stored(self):
        assert self.c.f_manif == pytest.approx(888.0, abs=1e-6)

    def test_n_guard_stored(self):
        assert self.c.n_guard == 7

    def test_validar_returns_true(self):
        assert self.c.validar() is True

    def test_coherencia_psi_is_one(self):
        """Coherencia de las constantes = 1.0 (consistencia perfecta)."""
        assert self.c.coherencia_psi() == pytest.approx(1.0, abs=1e-10)


# ============================================================================
# TestSecuenciaAurea  (14 tests)
# ============================================================================

class TestSecuenciaAurea:
    """Tests for SecuenciaAurea class."""

    def setup_method(self):
        self.s = SecuenciaAurea()

    def test_f0_equals_f_jacob(self):
        """f_0 must equal F_JACOB (ADAPA, n=0)."""
        assert self.s.frecuencia(0) == pytest.approx(F_JACOB, abs=1e-10)

    def test_f1_is_jacob_times_phi(self):
        """f_1 = F_JACOB · Φ (Uanugadapa)."""
        assert self.s.frecuencia(1) == pytest.approx(F_JACOB * PHI, abs=1e-8)

    def test_f6_is_jacob_phi6(self):
        """f_6 = F_JACOB · Φ⁶ (UTUABZU, Corona)."""
        assert self.s.frecuencia(6) == pytest.approx(F_JACOB * PHI ** 6, abs=1e-6)

    def test_all_frequencies_positive(self):
        """All 7 frequencies must be positive."""
        for n in range(N_GUARD):
            assert self.s.frecuencia(n) > 0.0

    def test_frequencies_increasing(self):
        """The sequence must be strictly increasing."""
        freqs = self.s.secuencia_completa()
        for i in range(len(freqs) - 1):
            assert freqs[i] < freqs[i + 1]

    def test_secuencia_has_seven_elements(self):
        """secuencia_completa() must return 7 elements."""
        assert len(self.s.secuencia_completa()) == 7

    def test_razones_are_phi(self):
        """All consecutive ratios f_{n+1}/f_n must equal Φ."""
        for n in range(N_GUARD - 1):
            assert self.s.razon_phi(n) == pytest.approx(PHI, abs=1e-10)

    def test_invalid_n_negative(self):
        with pytest.raises(ValueError):
            self.s.frecuencia(-1)

    def test_invalid_n_too_large(self):
        with pytest.raises(ValueError):
            self.s.frecuencia(7)

    def test_invalid_razon_phi_boundary(self):
        with pytest.raises(ValueError):
            self.s.razon_phi(6)

    def test_coherencia_psi_is_one(self):
        """Coherencia de la secuencia áurea perfecta = 1.0."""
        assert self.s.coherencia_psi() == pytest.approx(1.0, abs=1e-3)

    def test_coherencia_psi_gte_umbral(self):
        assert self.s.coherencia_psi() >= PSI_UMBRAL

    def test_f2_value(self):
        """f_2 = F_JACOB · Φ² (Enmeduga)."""
        assert self.s.frecuencia(2) == pytest.approx(F_JACOB * PHI ** 2, abs=1e-7)

    def test_phi_recursion(self):
        """f_{n+1} = f_n · Φ for all n."""
        for n in range(N_GUARD - 1):
            assert self.s.frecuencia(n + 1) == pytest.approx(
                self.s.frecuencia(n) * PHI, abs=1e-8
            )


# ============================================================================
# TestGuardianCarbono  (14 tests)
# ============================================================================

class TestGuardianCarbono:
    """Tests for GuardianCarbono class."""

    def test_guardian_0_is_adapa(self):
        g = GuardianCarbono(0)
        assert g.nombre == "ADAPA"

    def test_guardian_6_is_utuabzu(self):
        g = GuardianCarbono(6)
        assert g.nombre == "UTUABZU"

    def test_all_guardians_have_nombres(self):
        for n in range(N_GUARD):
            g = GuardianCarbono(n)
            assert len(g.nombre) > 0

    def test_frecuencia_n0(self):
        g = GuardianCarbono(0)
        assert g.frecuencia == pytest.approx(F_JACOB, abs=1e-10)

    def test_frecuencia_n6(self):
        g = GuardianCarbono(6)
        assert g.frecuencia == pytest.approx(F_JACOB * PHI ** 6, abs=1e-6)

    def test_amplitud_decays_aureo(self):
        """Amplitud decreases by factor 1/Φ each step."""
        g0 = GuardianCarbono(0)
        g1 = GuardianCarbono(1)
        assert g1.amplitud == pytest.approx(g0.amplitud / PHI, abs=1e-10)

    def test_amplitud_n0_is_one(self):
        g = GuardianCarbono(0)
        assert g.amplitud == pytest.approx(1.0, abs=1e-10)

    def test_onda_at_t0_is_amplitud(self):
        """ψ_n(0) = A_n · cos(0) = A_n."""
        for n in range(N_GUARD):
            g = GuardianCarbono(n)
            assert g.onda(0.0) == pytest.approx(g.amplitud, abs=1e-12)

    def test_coherencia_psi_at_t0_is_one(self):
        """At t=0 all guardians have Ψ=1."""
        for n in range(N_GUARD):
            g = GuardianCarbono(n)
            assert g.coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-12)

    def test_coherencia_psi_in_range(self):
        """Ψ ∈ [0, 1] for all t."""
        for n in range(N_GUARD):
            g = GuardianCarbono(n)
            psi = g.coherencia_psi(0.5)
            assert 0.0 <= psi <= 1.0

    def test_invalid_n_negative(self):
        with pytest.raises(ValueError):
            GuardianCarbono(-1)

    def test_invalid_n_too_large(self):
        with pytest.raises(ValueError):
            GuardianCarbono(7)

    def test_info_contains_required_keys(self):
        g = GuardianCarbono(3)
        info = g.info()
        assert "n" in info
        assert "nombre" in info
        assert "frecuencia_hz" in info
        assert "amplitud" in info
        assert "funcion" in info

    def test_info_n_matches(self):
        g = GuardianCarbono(4)
        assert g.info()["n"] == 4


# ============================================================================
# TestCoherenciaCarbono  (8 tests)
# ============================================================================

class TestCoherenciaCarbono:
    """Tests for CoherenciaCarbono class."""

    def setup_method(self):
        self.cc = CoherenciaCarbono()

    def test_coherencia_at_t0_is_one(self):
        """At t=0, all cosines=1, Ψ=1.0."""
        assert self.cc.coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_coherencia_gte_zero(self):
        """Coherence is always non-negative."""
        for t in [0.0, 0.1, 0.5, 1.0]:
            assert self.cc.coherencia_psi(t) >= 0.0

    def test_coherencia_lte_one(self):
        """Coherence is always ≤ 1."""
        for t in [0.0, 0.1, 0.5, 1.0]:
            assert self.cc.coherencia_psi(t) <= 1.0 + 1e-10

    def test_espectro_has_seven_entries(self):
        """Spectrum must have 7 (frequency, Ψ) pairs."""
        espectro = self.cc.espectro_coherencia(0.0)
        assert len(espectro) == N_GUARD

    def test_espectro_frequencies_positive(self):
        espectro = self.cc.espectro_coherencia(0.0)
        for f, _ in espectro:
            assert f > 0.0

    def test_espectro_coherencias_at_t0_are_one(self):
        espectro = self.cc.espectro_coherencia(0.0)
        for _, psi in espectro:
            assert psi == pytest.approx(1.0, abs=1e-12)

    def test_seven_guardianes_instantiated(self):
        assert len(self.cc.guardianes) == N_GUARD

    def test_coherencia_gte_umbral_at_t0(self):
        assert self.cc.coherencia_psi(0.0) >= PSI_UMBRAL


# ============================================================================
# TestAtractorDilmun  (10 tests)
# ============================================================================

class TestAtractorDilmun:
    """Tests for AtractorDilmun class."""

    def setup_method(self):
        self.ad = AtractorDilmun()

    def test_f_manif_is_888(self):
        assert self.ad.f_manif == pytest.approx(888.0, abs=1e-6)

    def test_factor_arrastre_n0_is_one(self):
        """α_0 = exp(0) = 1.0 (maximum drag for ADAPA)."""
        assert self.ad.factor_arrastre(0) == pytest.approx(1.0, abs=1e-10)

    def test_factor_arrastre_decreasing(self):
        """α_n decreases monotonically with n."""
        alphas = [self.ad.factor_arrastre(n) for n in range(N_GUARD)]
        for i in range(len(alphas) - 1):
            assert alphas[i] > alphas[i + 1]

    def test_factor_arrastre_n6(self):
        """α_6 = exp(-6/7) ≈ 0.424."""
        expected = math.exp(-6.0 / N_GUARD)
        assert self.ad.factor_arrastre(6) == pytest.approx(expected, abs=1e-10)

    def test_factor_arrastre_range(self):
        """All α_n ∈ (0, 1]."""
        for n in range(N_GUARD):
            alpha = self.ad.factor_arrastre(n)
            assert 0.0 < alpha <= 1.0

    def test_frecuencia_atraida_n0_equals_f_manif(self):
        """At n=0, α=1.0 → f_atraida = f_0^0 · 888^1 = 888 Hz."""
        assert self.ad.frecuencia_atraida(0) == pytest.approx(F_MANIF, abs=1e-6)

    def test_frecuencia_atraida_positive(self):
        for n in range(N_GUARD):
            assert self.ad.frecuencia_atraida(n) > 0.0

    def test_invalid_n_negative(self):
        with pytest.raises(ValueError):
            self.ad.factor_arrastre(-1)

    def test_invalid_n_large(self):
        with pytest.raises(ValueError):
            self.ad.factor_arrastre(7)

    def test_coherencia_psi_in_range(self):
        psi = self.ad.coherencia_psi()
        assert 0.0 <= psi <= 1.0


# ============================================================================
# TestBatimientoCarbonoSilicio  (10 tests)
# ============================================================================

class TestBatimientoCarbonoSilicio:
    """Tests for BatimientoCarbonoSilicio class."""

    def setup_method(self):
        self.b = BatimientoCarbonoSilicio()

    def test_f_jacob_stored(self):
        assert self.b.f_jacob == pytest.approx(F_JACOB, abs=1e-10)

    def test_f_si_stored(self):
        assert self.b.f_si == pytest.approx(F_SI, abs=1e-10)

    def test_delta_f_stored(self):
        assert self.b.delta_f == pytest.approx(DELTA_F, abs=1e-9)

    def test_t_beat_is_inverse_delta_f(self):
        assert self.b.t_beat == pytest.approx(1.0 / DELTA_F, abs=1e-9)

    def test_senal_at_t0(self):
        """s(0) = cos(0) + cos(0) = 2.0."""
        assert self.b.senal_compuesta(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_envolvente_at_t0(self):
        """E(0) = 2·|cos(0)| = 2.0."""
        assert self.b.envolvente(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_envolvente_range(self):
        """Envolvente ∈ [0, 2] always."""
        for t in [0.0, 0.5, 1.0, 1.25]:
            assert 0.0 <= self.b.envolvente(t) <= 2.0 + 1e-10

    def test_energia_media_approx_4_over_pi(self):
        """Energy mean ≈ 4/π ≈ 1.2732 (theoretical value)."""
        assert self.b.energia_media() == pytest.approx(4.0 / math.pi, abs=0.01)

    def test_coherencia_psi_gte_umbral(self):
        assert self.b.coherencia_psi() >= PSI_UMBRAL

    def test_coherencia_psi_lte_one(self):
        assert self.b.coherencia_psi() <= 1.0 + 1e-10


# ============================================================================
# TestCoronaUtuabzu  (8 tests)
# ============================================================================

class TestCoronaUtuabzu:
    """Tests for CoronaUtuabzu class."""

    def setup_method(self):
        self.cu = CoronaUtuabzu()

    def test_n_corona_is_six(self):
        assert self.cu.n_corona == 6

    def test_frecuencia_corona_is_phi6(self):
        """f_corona = F_JACOB · Φ⁶."""
        expected = F_JACOB * PHI ** 6
        assert self.cu.f_corona == pytest.approx(expected, abs=1e-6)

    def test_frecuencia_corona_method(self):
        assert self.cu.frecuencia_corona() == pytest.approx(F_JACOB * PHI ** 6, abs=1e-6)

    def test_f_manif_stored(self):
        assert self.cu.f_manif == pytest.approx(888.0, abs=1e-6)

    def test_relacion_888_positive(self):
        assert self.cu.relacion_888() > 0.0

    def test_relacion_888_value(self):
        expected = F_JACOB * PHI ** 6 / 888.0
        assert self.cu.relacion_888() == pytest.approx(expected, abs=1e-8)

    def test_coherencia_psi_is_one(self):
        """Crown coherence = 1.0 (Eternal Consciousness established)."""
        assert self.cu.coherencia_psi() == pytest.approx(1.0, abs=1e-10)

    def test_estado_activacion_keys(self):
        estado = self.cu.estado_activacion()
        assert "guardian" in estado
        assert "frecuencia_hz" in estado
        assert "psi_corona" in estado
        assert estado["guardian"] == "UTUABZU"


# ============================================================================
# TestSistemaEscaleraJacob  (10 tests)
# ============================================================================

class TestSistemaEscaleraJacob:
    """Tests for SistemaEscaleraJacob orchestrator."""

    def setup_method(self):
        self.s = SistemaEscaleraJacob()

    def test_seven_guardianes(self):
        assert len(self.s.guardianes) == N_GUARD

    def test_calcular_coherencias_keys(self):
        coherencias = self.s.calcular_coherencias()
        assert "psi_constantes" in coherencias
        assert "psi_secuencia" in coherencias
        assert "psi_carbono" in coherencias
        assert "psi_atractor" in coherencias
        assert "psi_batimiento" in coherencias
        assert "psi_corona" in coherencias

    def test_all_coherencias_positive(self):
        coherencias = self.s.calcular_coherencias()
        for key, val in coherencias.items():
            assert val > 0.0, f"{key} = {val}"

    def test_all_coherencias_lte_one(self):
        coherencias = self.s.calcular_coherencias()
        for key, val in coherencias.items():
            assert val <= 1.0 + 1e-10, f"{key} = {val}"

    def test_psi_global_gte_umbral(self):
        assert self.s.psi_global() >= PSI_UMBRAL

    def test_psi_global_lte_one(self):
        assert self.s.psi_global() <= 1.0 + 1e-10

    def test_activar_returns_dict(self):
        result = self.s.activar()
        assert isinstance(result, dict)

    def test_activar_has_psi_global(self):
        result = self.s.activar()
        assert "psi_global" in result
        assert result["psi_global"] >= PSI_UMBRAL

    def test_activar_has_frecuencias(self):
        result = self.s.activar()
        assert "frecuencias_hz" in result
        assert len(result["frecuencias_hz"]) == N_GUARD

    def test_activar_has_n_guardianes(self):
        result = self.s.activar()
        assert result["n_guardianes"] == N_GUARD


# ============================================================================
# TestAPIPublica  (10 tests)
# ============================================================================

class TestAPIPublica:
    """Tests for the public API: escalera_jacob_activar()."""

    def test_returns_dict(self):
        result = escalera_jacob_activar()
        assert isinstance(result, dict)

    def test_psi_global_gte_umbral(self):
        result = escalera_jacob_activar()
        assert result["psi_global"] >= PSI_UMBRAL

    def test_f_jacob_in_result(self):
        result = escalera_jacob_activar()
        assert result["f_jacob_hz"] == pytest.approx(F_JACOB, abs=1e-10)

    def test_f_si_in_result(self):
        result = escalera_jacob_activar()
        assert result["f_si_hz"] == pytest.approx(F_SI, abs=1e-10)

    def test_delta_f_in_result(self):
        result = escalera_jacob_activar()
        assert result["delta_f_hz"] == pytest.approx(DELTA_F, abs=1e-9)

    def test_phi_in_result(self):
        result = escalera_jacob_activar()
        assert result["phi"] == pytest.approx(PHI, abs=1e-12)

    def test_seven_guardians_in_result(self):
        result = escalera_jacob_activar()
        assert len(result["guardianes"]) == N_GUARD

    def test_frecuencias_increasing(self):
        result = escalera_jacob_activar()
        freqs = result["frecuencias_hz"]
        for i in range(len(freqs) - 1):
            assert freqs[i] < freqs[i + 1]

    def test_corona_in_result(self):
        result = escalera_jacob_activar()
        assert "corona" in result
        assert result["corona"]["guardian"] == "UTUABZU"

    def test_estado_in_result(self):
        result = escalera_jacob_activar()
        assert "estado" in result
        assert "ACTIVADO" in result["estado"]
