#!/usr/bin/env python3
"""
Test Suite: ConstanteRespiracion, OperadorHEpsilonDVR,
            ValidadorEvidenciaBrutal, NodoDilmun

Validates the four components introduced for the 142.1 Hz / 141.7001 Hz
frequency-space analysis.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Make sure qcal package is importable
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.constante_respiracion import (
    DELTA_F_AUREA,
    DELTA_F_MATERIAL,
    DELTA_F_MAX,
    DELTA_F_MIN,
    F0_HZ,
    F_MATERIAL_HZ,
    PHI,
    ConstanteRespiracion,
    obtener_espacio_respiracion,
    validar_espacio_respiracion,
)
from qcal.nodo_dilmun import (
    F_ANCLA_HZ,
    NODO_ID,
    NODO_NOMBRE,
    NodoDilmun,
    calcular_psi,
)
from qcal.operador_h_epsilon_dvr import (
    DEFAULT_N_BASIS,
    GAUSSIAN_CUTOFF_SIGMA,
    OperadorHEpsilonDVR,
    _lambda_mangoldt,
    construir_potencial_primos,
)
from qcal.validador_evidencia_brutal import (
    RIEMANN_ZEROS_KNOWN,
    ValidadorEvidenciaBrutal,
)


# ===========================================================================
# ConstanteRespiracion
# ===========================================================================


class TestConstanteRespiracion:
    """Tests for the breathing-space constants."""

    def test_f0_value(self):
        """F0_HZ must equal 141.7001 Hz."""
        assert abs(F0_HZ - 141.7001) < 1e-7

    def test_f_material_value(self):
        """F_MATERIAL_HZ must equal 142.1 Hz."""
        assert abs(F_MATERIAL_HZ - 142.1) < 1e-7

    def test_delta_f_material_approx(self):
        """DELTA_F_MATERIAL ≈ 0.3999 Hz."""
        assert abs(DELTA_F_MATERIAL - 0.3999) < 1e-4

    def test_delta_f_material_in_interval(self):
        """DELTA_F_MATERIAL must be in [0.38, 0.42]."""
        assert DELTA_F_MIN <= DELTA_F_MATERIAL <= DELTA_F_MAX

    def test_delta_f_aurea_formula(self):
        """DELTA_F_AUREA = (φ−1)·f₀·10⁻³."""
        expected = (PHI - 1.0) * F0_HZ * 1e-3
        assert abs(DELTA_F_AUREA - expected) < 1e-12

    def test_delta_f_aurea_value(self):
        """DELTA_F_AUREA ≈ 0.0876 Hz (golden-ratio scale)."""
        assert abs(DELTA_F_AUREA - 0.08757) < 1e-4

    def test_validar_espacio_respiracion_true(self):
        """Values within [0.38, 0.42] pass validation."""
        assert validar_espacio_respiracion(0.38)
        assert validar_espacio_respiracion(0.40)
        assert validar_espacio_respiracion(0.42)

    def test_validar_espacio_respiracion_false(self):
        """Values outside [0.38, 0.42] fail validation."""
        assert not validar_espacio_respiracion(0.37)
        assert not validar_espacio_respiracion(0.43)

    def test_obtener_espacio_respiracion(self):
        """obtener_espacio_respiracion returns (DELTA_F_MATERIAL, DELTA_F_AUREA)."""
        mat, aurea = obtener_espacio_respiracion()
        assert mat == DELTA_F_MATERIAL
        assert aurea == DELTA_F_AUREA

    def test_clase_instancia(self):
        """ConstanteRespiracion instantiates without error."""
        cr = ConstanteRespiracion()
        assert cr.delta_f_material == DELTA_F_MATERIAL
        assert cr.delta_f_aurea == DELTA_F_AUREA

    def test_clase_resumen(self):
        """ConstanteRespiracion.resumen() contains expected keys."""
        cr = ConstanteRespiracion()
        r = cr.resumen()
        for key in ("delta_f_material", "delta_f_aurea", "material_valido", "aurea_valido"):
            assert key in r
        assert r["material_valido"] is True
        # aurea_valido reflects whether DELTA_F_AUREA is in [0.38, 0.42]
        # (it is NOT, by design — it lives on a different scale)
        assert r["aurea_valido"] is False

    def test_phi_golden_ratio(self):
        """PHI equals the golden ratio (1+√5)/2."""
        assert abs(PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-12


# ===========================================================================
# OperadorHEpsilonDVR
# ===========================================================================


class TestOperadorHEpsilonDVR:
    """Tests for the DVR Hamiltonian builder."""

    def test_gaussian_cutoff_sigma(self):
        """GAUSSIAN_CUTOFF_SIGMA must equal 5.0."""
        assert GAUSSIAN_CUTOFF_SIGMA == 5.0

    def test_lambda_mangoldt_prime(self):
        """Λ(p) = log(p) for primes."""
        for p in (2, 3, 5, 7, 11, 13):
            assert abs(_lambda_mangoldt(p) - math.log(p)) < 1e-12

    def test_lambda_mangoldt_prime_power(self):
        """Λ(p^k) = log(p) for prime powers."""
        assert abs(_lambda_mangoldt(4) - math.log(2)) < 1e-12   # 2²
        assert abs(_lambda_mangoldt(8) - math.log(2)) < 1e-12   # 2³
        assert abs(_lambda_mangoldt(9) - math.log(3)) < 1e-12   # 3²

    def test_lambda_mangoldt_composite(self):
        """Λ(n) = 0 for composite non-prime-power integers."""
        for n in (6, 10, 12, 15, 30):
            assert _lambda_mangoldt(n) == 0.0

    def test_lambda_mangoldt_one(self):
        """Λ(1) = 0."""
        assert _lambda_mangoldt(1) == 0.0

    def test_potencial_primos_shape(self):
        """construir_potencial_primos returns array of same length as x_grid."""
        x = np.linspace(0, 5, 50)
        v = construir_potencial_primos(x, sigma=0.5, cutoff_sigma=5.0)
        assert v.shape == x.shape

    def test_potencial_primos_nonneg(self):
        """Prime potential is non-negative."""
        x = np.linspace(0.0, 5.0, 100)
        v = construir_potencial_primos(x, sigma=0.5)
        assert np.all(v >= 0.0)

    def test_potencial_primos_peak_near_log2(self):
        """Prime potential is elevated near x = log(2) ≈ 0.693."""
        x = np.linspace(0.0, 2.0, 500)
        v = construir_potencial_primos(x, sigma=0.2)
        # log(2) ≈ 0.693: check that V is larger near log(2) than far away
        log2 = math.log(2)
        idx_log2 = np.argmin(np.abs(x - log2))
        idx_far = np.argmin(np.abs(x - 0.0))  # x=0, far from any prime
        assert v[idx_log2] > v[idx_far]

    def test_hamiltonian_shape(self):
        """H has shape (n_basis, n_basis)."""
        op = OperadorHEpsilonDVR(n_basis=20, n_mangoldt=30, n_grid=40)
        H = op.construir()
        assert H.shape == (20, 20)

    def test_hamiltonian_symmetric(self):
        """H must be symmetric (for eigvalsh to be exact)."""
        op = OperadorHEpsilonDVR(n_basis=20, n_mangoldt=30, n_grid=40)
        H = op.construir()
        assert np.allclose(H, H.T, atol=1e-12)

    def test_kinetic_diagonal(self):
        """Without potential (ε=0) H equals the diagonal kinetic matrix."""
        op = OperadorHEpsilonDVR(n_basis=10, epsilon=0.0, n_mangoldt=30, n_grid=20)
        H = op.construir()
        # Off-diagonal elements should be zero
        off_diag = H - np.diag(np.diag(H))
        assert np.allclose(off_diag, 0.0, atol=1e-10)

    def test_eigenvalues_increasing(self):
        """Eigenvalues of H_cin (ε=0) are non-negative and non-decreasing."""
        op = OperadorHEpsilonDVR(n_basis=10, epsilon=0.0, n_mangoldt=30, n_grid=20)
        H = op.construir()
        evals = np.linalg.eigvalsh(H)
        assert np.all(evals >= -1e-10)  # non-negative
        assert np.all(np.diff(evals) >= -1e-10)  # non-decreasing

    def test_cached_H_property(self):
        """Accessing .H twice returns the same array."""
        op = OperadorHEpsilonDVR(n_basis=10, n_mangoldt=20, n_grid=20)
        H1 = op.H
        H2 = op.H
        assert H1 is H2


# ===========================================================================
# ValidadorEvidenciaBrutal
# ===========================================================================


class TestValidadorEvidenciaBrutal:
    """Tests for the spectral evidence validator."""

    @pytest.fixture(scope="class")
    def validador(self):
        """Shared validator with a small fast operator."""
        op = OperadorHEpsilonDVR(n_basis=50, n_mangoldt=60, n_grid=80)
        return ValidadorEvidenciaBrutal(operador=op, n_zeros=10)

    def test_riemann_zeros_known_count(self):
        """RIEMANN_ZEROS_KNOWN should have at least 10 entries."""
        assert len(RIEMANN_ZEROS_KNOWN) >= 10

    def test_riemann_zeros_ascending(self):
        """Known Riemann zeros must be in ascending order."""
        zeros = RIEMANN_ZEROS_KNOWN
        for i in range(len(zeros) - 1):
            assert zeros[i] < zeros[i + 1]

    def test_riemann_zero_first(self):
        """First Riemann zero ≈ 14.1347."""
        assert abs(RIEMANN_ZEROS_KNOWN[0] - 14.134725) < 1e-4

    def test_diagonalizar_returns_sorted(self, validador):
        """diagonalizar() returns eigenvalues in ascending order."""
        evals = validador.diagonalizar()
        assert np.all(np.diff(evals) >= -1e-10)

    def test_eigenvalues_count(self, validador):
        """Number of eigenvalues equals n_basis."""
        validador.diagonalizar()
        assert len(validador.eigenvalues) == validador.operador.n_basis

    def test_correlacion_in_range(self, validador):
        """Pearson ρ must lie in [−1, 1]."""
        validador.calcular_correlacion()
        assert -1.0 <= validador.correlacion_pearson <= 1.0

    def test_psi_formula(self, validador):
        """Ψ = (1 + |ρ|) / 2 must be in [0.5, 1.0]."""
        validador.calcular_psi()
        rho = validador.correlacion_pearson
        expected_psi = (1.0 + abs(rho)) / 2.0
        assert abs(validador.psi - expected_psi) < 1e-12
        assert 0.5 <= validador.psi <= 1.0

    def test_validar_returns_dict(self, validador):
        """validar() returns a dict with required keys."""
        result = validador.validar()
        for key in ("eigenvalues", "eigenvalues_rescalados", "riemann_zeros",
                    "correlacion_pearson", "psi"):
            assert key in result

    def test_psi_above_half(self, validador):
        """Ψ ≥ 0.5 (always true by definition)."""
        validador.validar()
        assert validador.psi >= 0.5


# ===========================================================================
# NodoDilmun
# ===========================================================================


class TestNodoDilmun:
    """Tests for the Dilmun anchor node."""

    def test_anchor_frequency(self):
        """F_ANCLA_HZ must equal 142.1 Hz."""
        assert abs(F_ANCLA_HZ - 142.1) < 1e-7

    def test_nodo_id(self):
        """Node identifier is 7."""
        assert NODO_ID == 7

    def test_nodo_nombre(self):
        """Node name is 'Dilmun'."""
        assert NODO_NOMBRE == "Dilmun"

    def test_psi_at_anchor(self):
        """Ψ = 1 when f = f_ancla (zero detuning)."""
        assert abs(calcular_psi(F_ANCLA_HZ, F_ANCLA_HZ) - 1.0) < 1e-12

    def test_psi_at_f0(self):
        """Ψ ≈ 0.9999 at f₀ = 141.7001 Hz."""
        psi_val = calcular_psi(141.7001, 142.1)
        assert abs(psi_val - 0.9999) < 1e-3

    def test_psi_nonneg(self):
        """Ψ is non-negative for any input frequency."""
        for f in np.linspace(100.0, 200.0, 50):
            assert calcular_psi(f, F_ANCLA_HZ) >= 0.0

    def test_psi_at_most_one(self):
        """Ψ ≤ 1 for any frequency."""
        for f in np.linspace(100.0, 200.0, 50):
            assert calcular_psi(f, F_ANCLA_HZ) <= 1.0 + 1e-12

    def test_nodo_instancia(self):
        """NodoDilmun instantiates correctly."""
        nodo = NodoDilmun()
        assert abs(nodo.f_ancla - F_ANCLA_HZ) < 1e-7
        assert nodo.nodo_id == 7
        assert nodo.nodo_nombre == "Dilmun"

    def test_nodo_psi_method(self):
        """nodo.psi(f) delegates to calcular_psi."""
        nodo = NodoDilmun()
        assert abs(nodo.psi(141.7001) - calcular_psi(141.7001)) < 1e-12

    def test_nodo_es_coherente_f0(self):
        """f₀ is coherent at threshold 0.999."""
        nodo = NodoDilmun(umbral_psi=0.999)
        assert nodo.es_coherente(141.7001)

    def test_nodo_no_coherente_far(self):
        """A frequency far from anchor is not coherent."""
        nodo = NodoDilmun(umbral_psi=0.999)
        assert not nodo.es_coherente(200.0)

    def test_nodo_estado_keys(self):
        """estado() returns dict with required keys."""
        nodo = NodoDilmun()
        estado = nodo.estado()
        for key in ("nodo_id", "nodo_nombre", "f_ancla_hz", "f_entrada_hz",
                    "delta_f_hz", "psi", "coherente"):
            assert key in estado

    def test_nodo_estado_default_f(self):
        """estado() uses F0_HZ = 141.7001 by default."""
        nodo = NodoDilmun()
        estado = nodo.estado()
        assert abs(estado["f_entrada_hz"] - 141.7001) < 1e-7

    def test_delta_f_method(self):
        """delta_f returns |f - f_ancla|."""
        nodo = NodoDilmun()
        assert abs(nodo.delta_f(141.7001) - abs(141.7001 - 142.1)) < 1e-7
