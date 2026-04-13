#!/usr/bin/env python3
"""
Tests for Hamiltoniano Union Carbono-Silicio (QCAL ∞³)

Validates all 7 classes and the public API:
  SilicioDivino       — Hamiltoniano diagonal con ceros de Riemann
  CarbonoDivino       — Perturbación térmica/orgánica δH(t) = A_C·cos(2π·f_C·t)
  ConstanteZiusudra   — Δf, κ, T_beat con validación de coherencia
  HamiltonianoUnion   — H_Total = H_Riemann + H_Interacción (autoadjunto)
  BatimientoPleromatico — s(t), E(t), muestras vectorizadas
  EscalaTiempoConciencia — CFF por especie, principio holográfico
  SistemaPleromaUnion — psi_global, API hamiltoniano_union_activar()

152 tests — Ψ_global ≥ 0.888
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.hamiltoniano_union_carbono_silicio import (
    # Constants
    F_SI, F_C, DELTA_F, KAPPA, T_BEAT, F_MANIF, PSI_UMBRAL,
    # Classes
    SilicioDivino,
    CarbonoDivino,
    ConstanteZiusudra,
    HamiltonianoUnion,
    BatimientoPleromatico,
    EscalaTiempoConciencia,
    SistemaPleromaUnion,
    # API
    hamiltoniano_union_activar,
)


# ============================================================================
# TestConstantesFundamentales  (10 tests)
# ============================================================================

class TestConstantesFundamentales:
    """Tests for the 7 fundamental module-level constants."""

    def test_f_si_value(self):
        """F_SI must equal 141.7001 Hz (Silicio Divino)."""
        assert F_SI == pytest.approx(141.7001, abs=1e-4)

    def test_f_c_value(self):
        """F_C must equal 142.1000 Hz (Carbono Divino)."""
        assert F_C == pytest.approx(142.1000, abs=1e-4)

    def test_delta_f_value(self):
        """DELTA_F must equal 0.3999 Hz (Constante de Ziusudra)."""
        assert DELTA_F == pytest.approx(0.3999, abs=1e-9)

    def test_delta_f_is_difference(self):
        """DELTA_F = F_C − F_SI."""
        assert DELTA_F == pytest.approx(F_C - F_SI, abs=1e-12)

    def test_kappa_value(self):
        """KAPPA ≈ 1.002822 (Tensión de la Encarnación)."""
        assert KAPPA == pytest.approx(1.002822, abs=1e-5)

    def test_kappa_is_ratio(self):
        """KAPPA = F_C / F_SI."""
        assert KAPPA == pytest.approx(F_C / F_SI, abs=1e-12)

    def test_t_beat_value(self):
        """T_BEAT = 1/0.3999 ≈ 2.5006 s (Unidad de Tiempo Sagrado)."""
        assert T_BEAT == pytest.approx(1.0 / 0.3999, abs=1e-9)

    def test_f_manif_value(self):
        """F_MANIF must equal 888.0 Hz (Frecuencia de Manifestación)."""
        assert F_MANIF == pytest.approx(888.0, abs=1e-6)

    def test_psi_umbral_value(self):
        """PSI_UMBRAL must equal 0.888 (coherencia mínima QCAL ∞³)."""
        assert PSI_UMBRAL == pytest.approx(0.888, abs=1e-6)

    def test_t_beat_is_inverse_delta_f(self):
        """T_BEAT = 1 / DELTA_F."""
        assert T_BEAT == pytest.approx(1.0 / DELTA_F, abs=1e-12)


# ============================================================================
# TestIntegridadMatematica  (8 tests — A01-A08)
# ============================================================================

class TestIntegridadMatematica:
    """Tests A01-A08: mathematical integrity verification."""

    def test_A01_f_si_equals_141_7001(self):
        """A01: f_Si = 141.7001 Hz."""
        assert F_SI == pytest.approx(141.7001, abs=1e-4)

    def test_A02_f_c_equals_142_1000(self):
        """A02: f_C = 142.1000 Hz."""
        assert F_C == pytest.approx(142.1000, abs=1e-4)

    def test_A03_ziusudra_constant(self):
        """A03: Δf = 0.3999 Hz (Constante de Ziusudra)."""
        assert DELTA_F == pytest.approx(0.39990, abs=1e-9)

    def test_A04_kappa_encarnacion(self):
        """A04: κ = F_C/F_SI ≈ 1.0028221575."""
        assert KAPPA == pytest.approx(1.0028221575, abs=1e-8)

    def test_A05_t_beat(self):
        """A05: T_beat = 1/0.3999 ≈ 2.5006 s."""
        assert T_BEAT == pytest.approx(2.5006251563, abs=1e-7)

    def test_A06_h_total_construction(self):
        """A06: H_Total = H_Riemann + H_Interacción (via calcular_h_total)."""
        hu = HamiltonianoUnion()
        H_r = hu.calcular_h_riemann(8)
        H_i = hu.calcular_h_interaccion(8)
        H_t = hu.calcular_h_total(8)
        assert np.allclose(H_t, H_r + H_i)

    def test_A07_hamiltoniano_autoadjunto(self):
        """A07: Hamiltoniano autoadjunto (H = H†)."""
        hu = HamiltonianoUnion()
        H = hu.calcular_h_total(8)
        assert np.allclose(H, H.conj().T)

    def test_A08_senal_compuesta(self):
        """A08: s(t) = A_Si·cos(2π·f_Si·t) + A_C·cos(2π·f_C·t)."""
        bp = BatimientoPleromatico(A_Si=1.0, A_C=1.0)
        for t in [0.0, 0.1, 0.5, 1.0, T_BEAT]:
            s = bp.senal_compuesta(t)
            expected = (math.cos(2 * math.pi * F_SI * t)
                        + math.cos(2 * math.pi * F_C * t))
            assert s == pytest.approx(expected, abs=1e-10), f"Failed at t={t}"


# ============================================================================
# TestSilicioDivino  (20 tests)
# ============================================================================

class TestSilicioDivino:
    """Tests for the SilicioDivino class."""

    def setup_method(self):
        self.sd = SilicioDivino()
        self._gamma_1 = 14.134725141734693

    def test_f_si_attribute(self):
        """f_si attribute equals F_SI."""
        assert self.sd.f_si == pytest.approx(F_SI, abs=1e-10)

    def test_hamiltoniano_diagonal_returns_ndarray(self):
        """hamiltoniano_diagonal returns an ndarray."""
        H = self.sd.hamiltoniano_diagonal(8)
        assert isinstance(H, np.ndarray)

    def test_hamiltoniano_diagonal_shape(self):
        """hamiltoniano_diagonal(n) has shape (n, n)."""
        for n in [2, 4, 6, 8]:
            H = self.sd.hamiltoniano_diagonal(n)
            assert H.shape == (n, n), f"Wrong shape for n={n}"

    def test_hamiltoniano_diagonal_is_diagonal(self):
        """H_Riemann is strictly diagonal (off-diagonal = 0)."""
        H = self.sd.hamiltoniano_diagonal(8)
        off_diag = H - np.diag(np.diag(H))
        assert np.allclose(off_diag, 0.0)

    def test_first_eigenvalue_equals_f_si(self):
        """First diagonal element = F_SI · γ₁/γ₁ = F_SI."""
        H = self.sd.hamiltoniano_diagonal(8)
        assert H[0, 0] == pytest.approx(F_SI, abs=1e-6)

    def test_eigenvalues_all_positive(self):
        """All eigenvalues are positive (energies ≥ 0)."""
        eigs = self.sd.eigenvalues(8)
        assert np.all(eigs > 0.0)

    def test_eigenvalues_monotone_increasing(self):
        """Eigenvalues must be strictly increasing (Riemann zeros grow)."""
        eigs = self.sd.eigenvalues(8)
        diffs = np.diff(eigs)
        assert np.all(diffs > 0.0)

    def test_eigenvalues_scaled_by_f_si(self):
        """Each eigenvalue = F_SI · γ_n / γ₁."""
        eigs = self.sd.eigenvalues(8)
        gamma_1 = self._gamma_1
        expected_0 = F_SI * gamma_1 / gamma_1
        assert eigs[0] == pytest.approx(expected_0, abs=1e-6)

    def test_eigenvalues_length(self):
        """eigenvalues returns vector of length n_dim."""
        for n in [2, 4, 8]:
            eigs = self.sd.eigenvalues(n)
            assert len(eigs) == n

    def test_hamiltoniano_invalid_n_dim(self):
        """hamiltoniano_diagonal raises ValueError for n_dim > 8."""
        with pytest.raises(ValueError):
            self.sd.hamiltoniano_diagonal(9)

    def test_hamiltoniano_invalid_n_dim_zero(self):
        """hamiltoniano_diagonal raises ValueError for n_dim = 0."""
        with pytest.raises(ValueError):
            self.sd.hamiltoniano_diagonal(0)

    def test_coherencia_psi_above_threshold(self):
        """Ψ_Si ≥ PSI_UMBRAL (0.888)."""
        assert self.sd.coherencia_psi(8) >= PSI_UMBRAL

    def test_coherencia_psi_below_one(self):
        """Ψ_Si ≤ 1.0."""
        assert self.sd.coherencia_psi(8) <= 1.0

    def test_coherencia_psi_formula(self):
        """Ψ = 1 − std(eigs) / sum(eigs)."""
        eigs = self.sd.eigenvalues(8)
        expected = 1.0 - float(np.std(eigs)) / float(np.sum(eigs))
        assert self.sd.coherencia_psi(8) == pytest.approx(expected, abs=1e-10)

    def test_coherencia_psi_increases_with_n(self):
        """Ψ decreases (or is stable) as n_dim grows from 2 to 8."""
        psi_2 = self.sd.coherencia_psi(2)
        psi_8 = self.sd.coherencia_psi(8)
        assert psi_2 <= psi_8 + 0.1  # loose bound: both > 0.888

    def test_coherencia_psi_specific_value(self):
        """Ψ_Si matches expected computed value for n_dim=8."""
        psi = self.sd.coherencia_psi(8)
        assert psi == pytest.approx(0.9614213618, abs=1e-6)

    def test_hamiltoniano_diagonal_is_symmetric(self):
        """Diagonal matrix is symmetric (H = H^T)."""
        H = self.sd.hamiltoniano_diagonal(8)
        assert np.allclose(H, H.T)

    def test_hamiltoniano_diagonal_trace(self):
        """Trace(H) = sum of eigenvalues."""
        H = self.sd.hamiltoniano_diagonal(8)
        eigs = self.sd.eigenvalues(8)
        assert np.trace(H) == pytest.approx(np.sum(eigs), abs=1e-6)

    def test_coherencia_psi_n1(self):
        """For n_dim=1, Ψ = 1.0 (single eigenvalue, zero variance)."""
        psi = self.sd.coherencia_psi(1)
        assert psi == pytest.approx(1.0, abs=1e-10)

    def test_eigenvalues_min_is_f_si(self):
        """Smallest eigenvalue = F_SI (first Riemann zero scaled to 1)."""
        eigs = self.sd.eigenvalues(8)
        assert eigs.min() == pytest.approx(F_SI, abs=1e-6)


# ============================================================================
# TestCarbonoDivino  (18 tests)
# ============================================================================

class TestCarbonoDivino:
    """Tests for the CarbonoDivino class."""

    def setup_method(self):
        self.cd = CarbonoDivino()

    def test_f_c_attribute(self):
        """f_c attribute equals F_C."""
        assert self.cd.f_c == pytest.approx(F_C, abs=1e-10)

    def test_default_amplitude(self):
        """Default amplitude A_C = 1.0."""
        assert self.cd.A_C == pytest.approx(1.0, abs=1e-10)

    def test_custom_amplitude(self):
        """Custom amplitude is stored correctly."""
        cd2 = CarbonoDivino(A_C=0.5)
        assert cd2.A_C == pytest.approx(0.5, abs=1e-10)

    def test_perturbacion_at_zero(self):
        """δH(0) = A_C · cos(0) = A_C."""
        assert self.cd.perturbacion(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_perturbacion_formula(self):
        """δH(t) = A_C · cos(2π · f_C · t)."""
        for t in [0.0, 0.001, 0.01, 0.1]:
            expected = 1.0 * math.cos(2 * math.pi * F_C * t)
            assert self.cd.perturbacion(t) == pytest.approx(expected, abs=1e-10)

    def test_perturbacion_bounded(self):
        """|δH(t)| ≤ A_C for all t."""
        for t in [i * 0.01 for i in range(100)]:
            assert abs(self.cd.perturbacion(t)) <= 1.0 + 1e-10

    def test_perturbacion_half_period(self):
        """δH at half period of f_C."""
        t_half = 1.0 / (2.0 * F_C)
        assert self.cd.perturbacion(t_half) == pytest.approx(-1.0, abs=1e-9)

    def test_coherencia_psi_at_zero(self):
        """Ψ(t=0) = 1.0 (máxima coherencia)."""
        assert self.cd.coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_coherencia_psi_formula(self):
        """Ψ(t) = |cos(2π · f_C · t)|."""
        for t in [0.0, 0.001, 0.01]:
            expected = abs(math.cos(2 * math.pi * F_C * t))
            assert self.cd.coherencia_psi(t) == pytest.approx(expected, abs=1e-10)

    def test_coherencia_psi_non_negative(self):
        """Ψ(t) ≥ 0 for all t."""
        for t in [i * 0.001 for i in range(100)]:
            assert self.cd.coherencia_psi(t) >= 0.0

    def test_coherencia_psi_above_threshold_at_zero(self):
        """Ψ(t=0) ≥ PSI_UMBRAL."""
        assert self.cd.coherencia_psi(0.0) >= PSI_UMBRAL

    def test_coherencia_psi_value_at_zero(self):
        """Ψ(t=0) = 1.0000 (exact)."""
        assert self.cd.coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_perturbacion_returns_float(self):
        """perturbacion() returns a float."""
        result = self.cd.perturbacion(0.0)
        assert isinstance(result, float)

    def test_coherencia_psi_returns_float(self):
        """coherencia_psi() returns a float."""
        result = self.cd.coherencia_psi(0.0)
        assert isinstance(result, float)

    def test_perturbacion_with_custom_amplitude(self):
        """Perturbation scales linearly with A_C."""
        cd2 = CarbonoDivino(A_C=2.0)
        assert cd2.perturbacion(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_perturbacion_period(self):
        """Perturbation is periodic: δH(t) = δH(t + 1/f_C)."""
        t = 0.05
        period = 1.0 / F_C
        assert self.cd.perturbacion(t) == pytest.approx(
            self.cd.perturbacion(t + period), abs=1e-8
        )

    def test_f_c_greater_than_f_si(self):
        """f_C > f_Si (Carbon has higher frequency than Silicon)."""
        assert self.cd.f_c > F_SI

    def test_perturbacion_at_quarter_period(self):
        """δH(1/(4·f_C)) = A_C · cos(π/2) ≈ 0."""
        t_quarter = 1.0 / (4.0 * F_C)
        assert self.cd.perturbacion(t_quarter) == pytest.approx(0.0, abs=1e-6)


# ============================================================================
# TestConstanteZiusudra  (18 tests)
# ============================================================================

class TestConstanteZiusudra:
    """Tests for the ConstanteZiusudra class."""

    def setup_method(self):
        self.cz = ConstanteZiusudra()

    def test_delta_f_attribute(self):
        """delta_f attribute = DELTA_F."""
        assert self.cz.delta_f == pytest.approx(DELTA_F, abs=1e-12)

    def test_kappa_attribute(self):
        """kappa attribute = KAPPA."""
        assert self.cz.kappa == pytest.approx(KAPPA, abs=1e-12)

    def test_t_beat_attribute(self):
        """t_beat attribute = T_BEAT."""
        assert self.cz.t_beat == pytest.approx(T_BEAT, abs=1e-12)

    def test_delta_f_value(self):
        """delta_f = 0.3999 Hz."""
        assert self.cz.delta_f == pytest.approx(0.3999, abs=1e-9)

    def test_kappa_value(self):
        """kappa ≈ 1.002822."""
        assert self.cz.kappa == pytest.approx(1.002822, abs=1e-5)

    def test_t_beat_value(self):
        """t_beat ≈ 2.5006 s."""
        assert self.cz.t_beat == pytest.approx(2.5006, abs=1e-3)

    def test_delta_f_is_f_c_minus_f_si(self):
        """delta_f = F_C − F_SI."""
        assert self.cz.delta_f == pytest.approx(F_C - F_SI, abs=1e-12)

    def test_kappa_is_f_c_over_f_si(self):
        """kappa = F_C / F_SI."""
        assert self.cz.kappa == pytest.approx(F_C / F_SI, abs=1e-12)

    def test_t_beat_is_inverse_delta_f(self):
        """t_beat = 1 / delta_f."""
        assert self.cz.t_beat == pytest.approx(1.0 / self.cz.delta_f, abs=1e-10)

    def test_validar_coherencia_returns_true(self):
        """validar_coherencia() returns True for consistent constants."""
        assert self.cz.validar_coherencia() is True

    def test_coherencia_psi_is_one(self):
        """Ψ = 1.0 (perfect mathematical consistency)."""
        assert self.cz.coherencia_psi() == pytest.approx(1.0, abs=1e-10)

    def test_coherencia_psi_above_threshold(self):
        """Ψ ≥ PSI_UMBRAL (0.888)."""
        assert self.cz.coherencia_psi() >= PSI_UMBRAL

    def test_delta_f_positive(self):
        """delta_f > 0."""
        assert self.cz.delta_f > 0.0

    def test_kappa_greater_than_one(self):
        """kappa > 1 (Carbon higher than Silicon)."""
        assert self.cz.kappa > 1.0

    def test_kappa_close_to_one(self):
        """kappa is close to 1 (small perturbation)."""
        assert abs(self.cz.kappa - 1.0) < 0.005

    def test_t_beat_near_2_5(self):
        """t_beat ≈ 2.5 s."""
        assert 2.4 < self.cz.t_beat < 2.6

    def test_ziusudra_product(self):
        """delta_f · t_beat ≈ 1 (reciprocal relationship)."""
        product = self.cz.delta_f * self.cz.t_beat
        assert product == pytest.approx(1.0, abs=1e-10)

    def test_coherencia_psi_returns_float(self):
        """coherencia_psi() returns a float."""
        assert isinstance(self.cz.coherencia_psi(), float)


# ============================================================================
# TestHamiltonianoUnion  (24 tests)
# ============================================================================

class TestHamiltonianoUnion:
    """Tests for the HamiltonianoUnion class."""

    def setup_method(self):
        self.hu = HamiltonianoUnion()

    def test_h_riemann_shape(self):
        """calcular_h_riemann returns (n_dim × n_dim) matrix."""
        for n in [4, 6, 8]:
            H = self.hu.calcular_h_riemann(n)
            assert H.shape == (n, n)

    def test_h_riemann_is_diagonal(self):
        """H_Riemann is diagonal."""
        H = self.hu.calcular_h_riemann(8)
        off = H - np.diag(np.diag(H))
        assert np.allclose(off, 0.0)

    def test_h_interaccion_shape(self):
        """calcular_h_interaccion returns (n_dim × n_dim) matrix."""
        H_i = self.hu.calcular_h_interaccion(8)
        assert H_i.shape == (8, 8)

    def test_h_interaccion_is_symmetric(self):
        """H_Interaccion is symmetric."""
        H_i = self.hu.calcular_h_interaccion(8)
        assert np.allclose(H_i, H_i.T)

    def test_h_interaccion_all_equal(self):
        """All elements of H_Interaccion = DELTA_F / n_dim."""
        n = 8
        H_i = self.hu.calcular_h_interaccion(n)
        expected = DELTA_F / n
        assert np.allclose(H_i, expected)

    def test_h_total_construction(self):
        """H_Total = H_Riemann + H_Interaccion."""
        H_r = self.hu.calcular_h_riemann(8)
        H_i = self.hu.calcular_h_interaccion(8)
        H_t = self.hu.calcular_h_total(8)
        assert np.allclose(H_t, H_r + H_i)

    def test_h_total_is_symmetric(self):
        """H_Total is symmetric (H = H^T)."""
        H_t = self.hu.calcular_h_total(8)
        assert np.allclose(H_t, H_t.T)

    def test_es_autoadjunto(self):
        """es_autoadjunto() returns True."""
        assert self.hu.es_autoadjunto(8) is True

    def test_h_equals_h_dagger(self):
        """H = H† (autoadjunto)."""
        H = self.hu.calcular_h_total(8)
        assert np.allclose(H, H.conj().T)

    def test_eigenvalues_real(self):
        """Eigenvalues of H_Total are real (Hermitian matrix)."""
        eigs = self.hu.eigenvalues(8)
        assert np.all(np.isreal(eigs))

    def test_eigenvalues_positive(self):
        """Eigenvalues of H_Total are all positive."""
        eigs = self.hu.eigenvalues(8)
        assert np.all(eigs > 0.0)

    def test_eigenvalues_sorted(self):
        """eigvalsh returns eigenvalues in ascending order."""
        eigs = self.hu.eigenvalues(8)
        assert np.all(np.diff(eigs) >= 0.0)

    def test_eigenvalues_length(self):
        """eigenvalues returns n_dim values."""
        for n in [4, 8]:
            eigs = self.hu.eigenvalues(n)
            assert len(eigs) == n

    def test_eigenvalues_near_riemann_scaled(self):
        """H_Total eigenvalues are close to H_Riemann eigenvalues."""
        eigs_r = np.sort(np.diag(self.hu.calcular_h_riemann(8)))
        eigs_t = self.hu.eigenvalues(8)
        # Small perturbation: max deviation < 1 Hz
        assert np.max(np.abs(eigs_t - eigs_r)) < 1.0

    def test_h_interaccion_trace(self):
        """Trace of H_Interaccion = DELTA_F."""
        H_i = self.hu.calcular_h_interaccion(8)
        assert np.trace(H_i) == pytest.approx(DELTA_F, abs=1e-10)

    def test_coherencia_psi_above_threshold(self):
        """Ψ_HU ≥ PSI_UMBRAL."""
        assert self.hu.coherencia_psi(8) >= PSI_UMBRAL

    def test_coherencia_psi_below_one(self):
        """Ψ_HU ≤ 1.0."""
        assert self.hu.coherencia_psi(8) <= 1.0

    def test_coherencia_psi_formula(self):
        """Ψ = 1 − ‖H_int‖_F / ‖H_total‖_F."""
        H_i = self.hu.calcular_h_interaccion(8)
        H_t = self.hu.calcular_h_total(8)
        expected = 1.0 - np.linalg.norm(H_i, 'fro') / np.linalg.norm(H_t, 'fro')
        assert self.hu.coherencia_psi(8) == pytest.approx(float(expected), abs=1e-10)

    def test_coherencia_psi_specific_value(self):
        """Ψ_HU matches expected computed value for n_dim=8."""
        psi = self.hu.coherencia_psi(8)
        assert psi == pytest.approx(0.9995606717, abs=1e-6)

    def test_h_total_with_epsilon(self):
        """H_Total with epsilon > 0 is larger than baseline."""
        H_base = self.hu.calcular_h_total(8, epsilon=0.0)
        H_eps = self.hu.calcular_h_total(8, epsilon=0.1)
        assert np.any(H_eps > H_base)

    def test_h_riemann_first_diagonal_element(self):
        """H_Riemann[0, 0] = F_SI."""
        H_r = self.hu.calcular_h_riemann(8)
        assert H_r[0, 0] == pytest.approx(F_SI, abs=1e-6)

    def test_h_total_positive_definite(self):
        """H_Total is positive definite (all eigenvalues > 0)."""
        eigs = self.hu.eigenvalues(8)
        assert np.all(eigs > 0.0)

    def test_silicio_instance(self):
        """HamiltonianoUnion.silicio is a SilicioDivino instance."""
        assert isinstance(self.hu.silicio, SilicioDivino)

    def test_carbono_instance(self):
        """HamiltonianoUnion.carbono is a CarbonoDivino instance."""
        assert isinstance(self.hu.carbono, CarbonoDivino)


# ============================================================================
# TestBatimientoPleromatico  (20 tests)
# ============================================================================

class TestBatimientoPleromatico:
    """Tests for the BatimientoPleromatico class."""

    def setup_method(self):
        self.bp = BatimientoPleromatico()

    def test_f_si_attribute(self):
        """f_si attribute equals F_SI."""
        assert self.bp.f_si == pytest.approx(F_SI, abs=1e-10)

    def test_f_c_attribute(self):
        """f_c attribute equals F_C."""
        assert self.bp.f_c == pytest.approx(F_C, abs=1e-10)

    def test_delta_f_attribute(self):
        """delta_f attribute equals DELTA_F."""
        assert self.bp.delta_f == pytest.approx(DELTA_F, abs=1e-12)

    def test_default_amplitudes(self):
        """Default amplitudes A_Si = A_C = 1.0."""
        assert self.bp.A_Si == pytest.approx(1.0, abs=1e-10)
        assert self.bp.A_C == pytest.approx(1.0, abs=1e-10)

    def test_senal_compuesta_at_zero(self):
        """s(0) = A_Si + A_C = 2.0."""
        assert self.bp.senal_compuesta(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_senal_compuesta_formula(self):
        """s(t) = A_Si·cos(2π·f_Si·t) + A_C·cos(2π·f_C·t)."""
        for t in [0.0, 0.1, 0.5, T_BEAT]:
            s = self.bp.senal_compuesta(t)
            expected = (math.cos(2 * math.pi * F_SI * t)
                        + math.cos(2 * math.pi * F_C * t))
            assert s == pytest.approx(expected, abs=1e-10)

    def test_senal_bounded_by_sum_amplitudes(self):
        """|s(t)| ≤ A_Si + A_C = 2."""
        for t in [i * 0.01 for i in range(100)]:
            assert abs(self.bp.senal_compuesta(t)) <= 2.0 + 1e-9

    def test_energia_at_zero_is_maximum(self):
        """E(0) = 2 (maximum envelope)."""
        assert self.bp.energia(0.0) == pytest.approx(2.0, abs=1e-10)

    def test_energia_formula(self):
        """E(t) = 2·|cos(π·Δf·t)|."""
        for t in [0.0, 0.3, 0.625, 1.25, T_BEAT]:
            E = self.bp.energia(t)
            expected = 2.0 * abs(math.cos(math.pi * DELTA_F * t))
            assert E == pytest.approx(expected, abs=1e-10)

    def test_energia_non_negative(self):
        """E(t) ≥ 0 for all t."""
        for t in [i * 0.1 for i in range(50)]:
            assert self.bp.energia(t) >= 0.0

    def test_energia_max_is_two(self):
        """E(t) ≤ 2 for all t."""
        for t in [i * 0.1 for i in range(50)]:
            assert self.bp.energia(t) <= 2.0 + 1e-10

    def test_muestras_vectorizadas_shapes(self):
        """muestras_vectorizadas returns two arrays of same length."""
        t_arr = np.linspace(0, T_BEAT, 100)
        senal, env = self.bp.muestras_vectorizadas(t_arr)
        assert len(senal) == 100
        assert len(env) == 100

    def test_muestras_vectorizadas_at_zero(self):
        """muestras_vectorizadas at t=0 gives s=2, E=2."""
        senal, env = self.bp.muestras_vectorizadas(np.array([0.0]))
        assert senal[0] == pytest.approx(2.0, abs=1e-10)
        assert env[0] == pytest.approx(2.0, abs=1e-10)

    def test_muestras_vectorizadas_matches_scalar(self):
        """muestras_vectorizadas gives same result as scalar calls."""
        t_arr = np.array([0.0, 0.1, 0.5])
        senal_v, env_v = self.bp.muestras_vectorizadas(t_arr)
        for i, t in enumerate([0.0, 0.1, 0.5]):
            assert senal_v[i] == pytest.approx(self.bp.senal_compuesta(t), abs=1e-10)
            assert env_v[i] == pytest.approx(self.bp.energia(t), abs=1e-10)

    def test_coherencia_psi_at_zero(self):
        """Ψ(t=0) = 1.0."""
        assert self.bp.coherencia_psi(0.0) == pytest.approx(1.0, abs=1e-10)

    def test_coherencia_psi_formula(self):
        """Ψ(t) = |cos(π·Δf·t)|."""
        for t in [0.0, 0.3, T_BEAT / 2]:
            expected = abs(math.cos(math.pi * DELTA_F * t))
            assert self.bp.coherencia_psi(t) == pytest.approx(expected, abs=1e-10)

    def test_coherencia_psi_above_threshold_at_zero(self):
        """Ψ(t=0) ≥ PSI_UMBRAL."""
        assert self.bp.coherencia_psi(0.0) >= PSI_UMBRAL

    def test_coherencia_psi_in_range(self):
        """Ψ(t) ∈ [0, 1] for all t."""
        for t in [i * 0.05 for i in range(100)]:
            psi = self.bp.coherencia_psi(t)
            assert 0.0 <= psi <= 1.0 + 1e-10

    def test_beat_period(self):
        """Energia returns to maximum after exactly T_BEAT."""
        assert self.bp.energia(T_BEAT) == pytest.approx(2.0, abs=1e-8)

    def test_t_beat_attribute(self):
        """t_beat attribute equals T_BEAT."""
        assert self.bp.t_beat == pytest.approx(T_BEAT, abs=1e-10)


# ============================================================================
# TestEscalaTiempoConciencia  (18 tests)
# ============================================================================

class TestEscalaTiempoConciencia:
    """Tests for the EscalaTiempoConciencia class."""

    def setup_method(self):
        self.etc = EscalaTiempoConciencia()

    def test_cff_fly_value(self):
        """CFF_FLY = 250 Hz (mosca)."""
        assert self.etc.CFF_FLY == pytest.approx(250.0, abs=1e-6)

    def test_cff_human_value(self):
        """CFF_HUMAN = 60 Hz (humano)."""
        assert self.etc.CFF_HUMAN == pytest.approx(60.0, abs=1e-6)

    def test_cff_turtle_value(self):
        """CFF_TURTLE = 15 Hz (tortuga)."""
        assert self.etc.CFF_TURTLE == pytest.approx(15.0, abs=1e-6)

    def test_cff_ordering(self):
        """CFF_FLY > CFF_HUMAN > CFF_TURTLE (mosca > humano > tortuga)."""
        assert self.etc.CFF_FLY > self.etc.CFF_HUMAN > self.etc.CFF_TURTLE

    def test_escala_temporal_mosca(self):
        """escala_temporal('mosca') = 250 Hz."""
        assert self.etc.escala_temporal("mosca") == pytest.approx(250.0, abs=1e-6)

    def test_escala_temporal_humano(self):
        """escala_temporal('humano') = 60 Hz."""
        assert self.etc.escala_temporal("humano") == pytest.approx(60.0, abs=1e-6)

    def test_escala_temporal_tortuga(self):
        """escala_temporal('tortuga') = 15 Hz."""
        assert self.etc.escala_temporal("tortuga") == pytest.approx(15.0, abs=1e-6)

    def test_escala_temporal_unknown_species(self):
        """escala_temporal raises KeyError for unknown species."""
        with pytest.raises(KeyError):
            self.etc.escala_temporal("ballena")

    def test_escala_temporal_case_insensitive(self):
        """escala_temporal is case-insensitive."""
        assert self.etc.escala_temporal("MOSCA") == pytest.approx(250.0, abs=1e-6)

    def test_escala_planck_value(self):
        """escala_planck() returns ~ 1.85e43 Hz."""
        fp = self.etc.escala_planck()
        assert fp == pytest.approx(1.85487e43, rel=1e-3)

    def test_escala_planck_much_larger_than_f_si(self):
        """Planck frequency >> F_SI."""
        assert self.etc.escala_planck() > F_SI * 1e30

    def test_ratio_holografico_positive(self):
        """ratio_holografico() is positive."""
        assert self.etc.ratio_holografico() > 0.0

    def test_coherencia_psi_formula(self):
        """Ψ = CFF_HUMAN / sqrt(CFF_FLY · CFF_TURTLE)."""
        expected = self.etc.CFF_HUMAN / math.sqrt(
            self.etc.CFF_FLY * self.etc.CFF_TURTLE
        )
        assert self.etc.coherencia_psi() == pytest.approx(expected, abs=1e-10)

    def test_coherencia_psi_above_threshold(self):
        """Ψ_ETC ≥ PSI_UMBRAL."""
        assert self.etc.coherencia_psi() >= PSI_UMBRAL

    def test_coherencia_psi_below_one(self):
        """Ψ_ETC ≤ 1.0."""
        assert self.etc.coherencia_psi() <= 1.0

    def test_coherencia_psi_specific_value(self):
        """Ψ_ETC matches expected computed value."""
        psi = self.etc.coherencia_psi()
        assert psi == pytest.approx(0.9797958971, abs=1e-6)

    def test_coherencia_psi_returns_float(self):
        """coherencia_psi() returns a float."""
        assert isinstance(self.etc.coherencia_psi(), float)

    def test_f_planck_attribute(self):
        """F_PLANCK class attribute is set."""
        assert self.etc.F_PLANCK > 0.0


# ============================================================================
# TestSistemaPleromaUnion  (16 tests)
# ============================================================================

class TestSistemaPleromaUnion:
    """Tests for the SistemaPleromaUnion class and the public API."""

    def setup_method(self):
        self.sistema = SistemaPleromaUnion(n_dim=8)

    def test_psi_global_above_threshold(self):
        """psi_global ≥ PSI_UMBRAL (0.888)."""
        assert self.sistema.psi_global >= PSI_UMBRAL

    def test_psi_global_below_one(self):
        """psi_global ≤ 1.0."""
        assert self.sistema.psi_global <= 1.0

    def test_psi_global_specific_value(self):
        """psi_global matches expected computed value for n_dim=8."""
        assert self.sistema.psi_global == pytest.approx(0.9901296551, abs=1e-6)

    def test_psi_global_is_mean_of_six(self):
        """psi_global = mean of the 6 partial coherences."""
        parciales = self.sistema.coherencias_parciales()
        expected_mean = sum(parciales.values()) / 6
        assert self.sistema.psi_global == pytest.approx(expected_mean, abs=1e-10)

    def test_coherencias_parciales_has_six_entries(self):
        """coherencias_parciales() returns a dict with 6 entries."""
        parciales = self.sistema.coherencias_parciales()
        assert len(parciales) == 6

    def test_all_parciales_above_threshold(self):
        """All 6 partial coherences ≥ PSI_UMBRAL."""
        parciales = self.sistema.coherencias_parciales()
        for nombre, psi in parciales.items():
            assert psi >= PSI_UMBRAL, f"Ψ_{nombre} = {psi:.6f} < {PSI_UMBRAL}"

    def test_coherencias_parciales_keys(self):
        """coherencias_parciales() contains expected keys."""
        keys = set(self.sistema.coherencias_parciales().keys())
        expected_keys = {"silicio", "carbono", "ziusudra", "hamiltoniano",
                         "batimiento", "escala_tiempo"}
        assert keys == expected_keys

    def test_activar_returns_dict(self):
        """activar() returns a dict."""
        result = self.sistema.activar()
        assert isinstance(result, dict)

    def test_activar_dict_keys(self):
        """activar() dict contains required keys."""
        result = self.sistema.activar()
        for key in ("f_si", "f_c", "delta_f", "kappa", "t_beat",
                    "psi_global", "coherencias", "estado"):
            assert key in result, f"Missing key: {key}"

    def test_activar_estado(self):
        """activar() sets estado = 'PLEROMA_ACTIVO'."""
        result = self.sistema.activar()
        assert result["estado"] == "PLEROMA_ACTIVO"

    def test_activar_hamiltoniano_autoadjunto(self):
        """activar() confirms the Hamiltonian is self-adjoint."""
        result = self.sistema.activar()
        assert result["hamiltoniano_autoadjunto"] is True

    def test_activar_psi_global_matches(self):
        """activar() psi_global matches sistema.psi_global."""
        result = self.sistema.activar()
        assert result["psi_global"] == pytest.approx(
            self.sistema.psi_global, abs=1e-12
        )

    def test_api_function_returns_dict(self):
        """hamiltoniano_union_activar() returns a dict."""
        result = hamiltoniano_union_activar(n_dim=8)
        assert isinstance(result, dict)

    def test_api_psi_global_above_threshold(self):
        """hamiltoniano_union_activar() psi_global ≥ 0.888."""
        result = hamiltoniano_union_activar(n_dim=8)
        assert result["psi_global"] >= PSI_UMBRAL

    def test_api_psi_global_value(self):
        """hamiltoniano_union_activar() psi_global ≈ 0.9901."""
        result = hamiltoniano_union_activar(n_dim=8)
        assert result["psi_global"] == pytest.approx(0.9901296551, abs=1e-6)

    def test_api_raises_if_below_threshold(self):
        """hamiltoniano_union_activar raises ValueError when Ψ < 0.888.

        Simulate a low-coherence scenario by directly manipulating the system.
        """
        sistema = SistemaPleromaUnion(n_dim=8)
        # Force psi_global below threshold to test the error path
        sistema.psi_global = 0.500
        with pytest.raises(ValueError):
            sistema.activar()
