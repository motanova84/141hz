#!/usr/bin/env python3
"""
Tests para FiltroRacionalesAdelico (Pilar 2).

Valida:
  1. _sieve_eratosthenes – criba O(N log log N)
  2. _sieve_mobius_values – criba lineal de Möbius
  3. chebyshev_psi_sieve  – ψ(x) preciso
  4. psi_explicit_error   – términos de error explícitos
  5. compute_mobius_cancellation – nunca devuelve inf
  6. selberg_laplacian_spectrum – 100-200 valores propios, clave mean_gap

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026
"""

import math
import os
import sys
from pathlib import Path

import numpy as np
import pytest

# Añadir scripts/ al path
sys.path.insert(0, str(Path(__file__).parent))

from filtro_racionales_adelico import (
    FiltroRacionalesAdelico,
    _NUMERICAL_TOLERANCE,
    _MIN_LOG_ARG,
    _RIEMANN_ZEROS_100,
)


# ============================================================================
# TESTS: CONSTANTES DE MÓDULO
# ============================================================================

class TestModuleConstants:
    """Verifica que las constantes de módulo tienen los valores correctos."""

    def test_numerical_tolerance_value(self):
        assert _NUMERICAL_TOLERANCE == 1e-12

    def test_min_log_arg_value(self):
        assert _MIN_LOG_ARG == 1e-30

    def test_riemann_zeros_count(self):
        assert len(_RIEMANN_ZEROS_100) == 100

    def test_first_riemann_zero(self):
        assert abs(_RIEMANN_ZEROS_100[0] - 14.134725) < 1e-4

    def test_zeros_ascending(self):
        for i in range(len(_RIEMANN_ZEROS_100) - 1):
            assert _RIEMANN_ZEROS_100[i] < _RIEMANN_ZEROS_100[i + 1]


# ============================================================================
# TESTS: CRIBA DE ERATÓSTENES
# ============================================================================

class TestSieveEratosthenes:
    """Verifica la criba de Eratóstenes."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_small_limit(self):
        primes = self.f._sieve_eratosthenes(10)
        assert list(primes) == [2, 3, 5, 7]

    def test_limit_zero_or_one(self):
        assert len(self.f._sieve_eratosthenes(0)) == 0
        assert len(self.f._sieve_eratosthenes(1)) == 0

    def test_first_10_primes(self):
        primes = self.f._sieve_eratosthenes(30)
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in expected:
            assert p in primes

    def test_no_composites(self):
        primes = self.f._sieve_eratosthenes(50)
        primes_set = set(int(p) for p in primes)
        for composite in [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 25]:
            assert composite not in primes_set

    def test_count_primes_up_to_100(self):
        # π(100) = 25
        primes = self.f._sieve_eratosthenes(100)
        assert len(primes) == 25

    def test_count_primes_up_to_1000(self):
        # π(1000) = 168
        primes = self.f._sieve_eratosthenes(1000)
        assert len(primes) == 168

    def test_returns_ndarray(self):
        primes = self.f._sieve_eratosthenes(20)
        assert isinstance(primes, np.ndarray)

    def test_all_primes_positive(self):
        primes = self.f._sieve_eratosthenes(100)
        assert np.all(primes > 0)


# ============================================================================
# TESTS: CRIBA LINEAL DE MÖBIUS
# ============================================================================

class TestSieveMobiusValues:
    """Verifica la criba lineal de μ(n)."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_mu_1_is_1(self):
        mu = self.f._sieve_mobius_values(10)
        assert mu[1] == 1

    def test_mu_primes_is_minus1(self):
        mu = self.f._sieve_mobius_values(20)
        for p in [2, 3, 5, 7, 11, 13, 17, 19]:
            assert mu[p] == -1, f"μ({p}) debería ser -1, got {mu[p]}"

    def test_mu_prime_squared_is_0(self):
        # p² → μ = 0
        mu = self.f._sieve_mobius_values(50)
        for p2 in [4, 9, 25, 49]:
            assert mu[p2] == 0, f"μ({p2}) debería ser 0, got {mu[p2]}"

    def test_mu_squarefree_semiprimes(self):
        # p·q → μ = 1
        mu = self.f._sieve_mobius_values(30)
        # 6 = 2·3 → μ = 1
        assert mu[6] == 1
        # 10 = 2·5 → μ = 1
        assert mu[10] == 1
        # 15 = 3·5 → μ = 1
        assert mu[15] == 1

    def test_mu_three_primes(self):
        # 30 = 2·3·5 → μ = -1
        mu = self.f._sieve_mobius_values(30)
        assert mu[30] == -1

    def test_mu_values_in_valid_range(self):
        mu = self.f._sieve_mobius_values(100)
        valid = {-1, 0, 1}
        for v in mu[1:]:
            assert int(v) in valid

    def test_limit_zero_or_less(self):
        mu = self.f._sieve_mobius_values(0)
        assert len(mu) == 0


# ============================================================================
# TESTS: ψ(x) POR CRIBA
# ============================================================================

class TestChebyshevPsiSieve:
    """Verifica chebyshev_psi_sieve."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_psi_2(self):
        # ψ(2) = log 2
        result = self.f.chebyshev_psi_sieve(2)
        assert abs(result - math.log(2)) < 1e-10

    def test_psi_below_2(self):
        assert self.f.chebyshev_psi_sieve(1) == 0.0
        assert self.f.chebyshev_psi_sieve(1.5) == 0.0

    def test_psi_positive(self):
        for x in [10, 100, 1000, 10000]:
            assert self.f.chebyshev_psi_sieve(x) > 0

    def test_psi_over_x_approaches_1(self):
        # Teorema de números primos: ψ(x)/x → 1 cuando x → ∞
        # Para x = 100_000, ratio debe estar en (0.99, 1.01)
        psi = self.f.chebyshev_psi_sieve(100_000)
        ratio = psi / 100_000
        assert 0.99 < ratio < 1.01, f"ψ(x)/x = {ratio:.6f} fuera del rango esperado"

    def test_psi_monotone_increasing(self):
        prev = 0.0
        for x in [10, 100, 1000, 10000]:
            curr = self.f.chebyshev_psi_sieve(x)
            assert curr > prev
            prev = curr

    def test_psi_100(self):
        # Valor conocido ψ(100) ≈ 94.0
        psi = self.f.chebyshev_psi_sieve(100)
        assert 90 < psi < 100, f"ψ(100) = {psi:.4f} fuera del rango"

    def test_psi_includes_prime_powers(self):
        # ψ(8) = log2 + log2 + log2 = 3*log2 ≈ 2.079  (2, 4=2², 8=2³)
        # + log3 ≈ 1.099 + log5 ≈ 1.609 + log7 ≈ 1.946
        psi_8 = self.f.chebyshev_psi_sieve(8)
        expected = 3 * math.log(2) + math.log(3) + math.log(5) + math.log(7)
        assert abs(psi_8 - expected) < 1e-10


# ============================================================================
# TESTS: TÉRMINOS DE ERROR EXPLÍCITOS
# ============================================================================

class TestPsiExplicitError:
    """Verifica psi_explicit_error."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_returns_dict_with_required_keys(self):
        result = self.f.psi_explicit_error(1000)
        required = {
            "psi_sieve", "psi_explicit", "error",
            "riemann_correction", "log2pi", "half_log_term",
        }
        assert required.issubset(result.keys())

    def test_psi_sieve_is_positive(self):
        result = self.f.psi_explicit_error(1000)
        assert result["psi_sieve"] > 0

    def test_log2pi_correct(self):
        result = self.f.psi_explicit_error(1000)
        assert abs(result["log2pi"] - math.log(2 * math.pi)) < 1e-10

    def test_half_log_term_zero_for_x_le_1(self):
        # Para x ≤ 1 la corrección ½ log(1 − x⁻²) no se aplica
        result = self.f.psi_explicit_error(0.5)
        assert result["half_log_term"] == 0.0

    def test_half_log_term_negative_for_x_gt_1(self):
        result = self.f.psi_explicit_error(1000)
        # 1 − x⁻² < 1 → log < 0 → ½ log < 0
        assert result["half_log_term"] < 0

    def test_error_finite(self):
        result = self.f.psi_explicit_error(10000)
        assert math.isfinite(result["error"])
        assert math.isfinite(result["psi_explicit"])

    def test_custom_zeros(self):
        # Se puede pasar una lista personalizada de ceros
        zeros = [14.134725, 21.022040, 25.010858]
        result = self.f.psi_explicit_error(1000, zeros=zeros, N_zeros=3)
        assert "riemann_correction" in result

    def test_N_zeros_truncation(self):
        # Pedir más ceros que los disponibles no rompe nada
        result = self.f.psi_explicit_error(1000, N_zeros=500)
        assert math.isfinite(result["psi_explicit"])

    def test_psi_sieve_matches_chebyshev(self):
        x = 500.0
        direct = self.f.chebyshev_psi_sieve(x)
        via_error = self.f.psi_explicit_error(x)["psi_sieve"]
        assert abs(direct - via_error) < 1e-10


# ============================================================================
# TESTS: FACTOR DE CANCELACIÓN DE MÖBIUS
# ============================================================================

class TestComputeMobiusCancellation:
    """Verifica compute_mobius_cancellation (nunca devuelve inf)."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_never_inf_for_small_N(self):
        for n in range(1, 20):
            r = self.f.compute_mobius_cancellation(n)
            assert math.isfinite(r["cancellation_factor"]), \
                f"cancellation_factor es inf para N={n}"

    def test_never_inf_for_large_N(self):
        for n in [100, 500, 1000, 5000]:
            r = self.f.compute_mobius_cancellation(n)
            assert math.isfinite(r["cancellation_factor"]), \
                f"cancellation_factor es inf para N={n}"

    def test_N_1_is_finite(self):
        r = self.f.compute_mobius_cancellation(1)
        assert math.isfinite(r["cancellation_factor"])
        assert r["N"] == 1

    def test_partial_sum_is_finite(self):
        for n in [1, 10, 100, 1000]:
            r = self.f.compute_mobius_cancellation(n)
            assert math.isfinite(r["partial_sum"])

    def test_mertens_function_integer(self):
        r = self.f.compute_mobius_cancellation(10)
        assert isinstance(r["mertens_function"], (int, np.integer))

    def test_returns_required_keys(self):
        r = self.f.compute_mobius_cancellation(100)
        for key in ["N", "partial_sum", "cancellation_factor", "mertens_function"]:
            assert key in r

    def test_N_returned_correctly(self):
        for n in [1, 10, 100]:
            r = self.f.compute_mobius_cancellation(n)
            assert r["N"] == n

    def test_cancellation_factor_positive(self):
        for n in [1, 2, 3, 5, 10, 100]:
            r = self.f.compute_mobius_cancellation(n)
            assert r["cancellation_factor"] > 0

    def test_mertens_10(self):
        # M(10) = Σμ(1..10) = 1-1-1+0-1+1-1+0+0+1 = -1
        r = self.f.compute_mobius_cancellation(10)
        assert r["mertens_function"] == -1

    def test_partial_sum_approaches_0(self):
        # Para N grande, Σ μ(n)/n → 0
        r = self.f.compute_mobius_cancellation(10000)
        assert abs(r["partial_sum"]) < 1.0  # Must be small


# ============================================================================
# TESTS: ESPECTRO DE SELBERG
# ============================================================================

class TestSelbergLaplacianSpectrum:
    """Verifica selberg_laplacian_spectrum."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_default_200_eigenvalues(self):
        spec = self.f.selberg_laplacian_spectrum()
        assert spec["N_eigenvalues"] == 200

    def test_returns_required_keys(self):
        spec = self.f.selberg_laplacian_spectrum(100)
        for key in ["N_eigenvalues", "eigenvalues", "spectral_params",
                    "mean_gap", "gap_std", "gue_ratio", "weyl_prediction"]:
            assert key in spec

    def test_eigenvalues_count(self):
        for n in [50, 100, 150, 200]:
            spec = self.f.selberg_laplacian_spectrum(n)
            assert len(spec["eigenvalues"]) == n

    def test_eigenvalues_positive(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert np.all(spec["eigenvalues"] > 0)

    def test_eigenvalues_increasing(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        ev = spec["eigenvalues"]
        assert np.all(ev[1:] > ev[:-1])

    def test_mean_gap_positive(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert spec["mean_gap"] > 0

    def test_mean_gap_is_finite(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert math.isfinite(spec["mean_gap"])

    def test_gue_ratio_finite(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert math.isfinite(spec["gue_ratio"])

    def test_eigenvalues_ge_quarter(self):
        # λ_n = 1/4 + μ_n² ≥ 1/4
        spec = self.f.selberg_laplacian_spectrum(200)
        assert np.all(spec["eigenvalues"] >= 0.25)

    def test_max_eigenvalues_capped_at_200(self):
        spec = self.f.selberg_laplacian_spectrum(500)
        assert spec["N_eigenvalues"] == 200

    def test_min_eigenvalues_is_1(self):
        spec = self.f.selberg_laplacian_spectrum(0)
        assert spec["N_eigenvalues"] == 1

    def test_spectral_params_positive(self):
        spec = self.f.selberg_laplacian_spectrum(100)
        assert np.all(spec["spectral_params"] > 0)

    def test_weyl_prediction_positive(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert spec["weyl_prediction"] > 0

    def test_100_eigenvalues_supported(self):
        spec = self.f.selberg_laplacian_spectrum(100)
        assert spec["N_eigenvalues"] == 100
        assert len(spec["eigenvalues"]) == 100

    def test_gap_std_nonnegative(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert spec["gap_std"] >= 0


# ============================================================================
# TESTS: INTEGRACIÓN
# ============================================================================

class TestIntegration:
    """Tests de integración del módulo completo."""

    def setup_method(self):
        self.f = FiltroRacionalesAdelico()

    def test_pnt_confirmed(self):
        # TNP: ψ(x)/x ≈ 1 para x grande
        x = 100_000
        psi = self.f.chebyshev_psi_sieve(x)
        ratio = psi / x
        assert 0.995 < ratio < 1.005

    def test_mobius_cancellation_for_all_N_finite(self):
        """Regression test: cancellation_factor nunca es inf."""
        import math
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            r = self.f.compute_mobius_cancellation(n)
            assert math.isfinite(r["cancellation_factor"]), \
                f"N={n} → cancellation_factor = {r['cancellation_factor']}"

    def test_selberg_200_levels_with_gap_stats(self):
        spec = self.f.selberg_laplacian_spectrum(200)
        assert spec["N_eigenvalues"] == 200
        assert "mean_gap" in spec
        assert spec["mean_gap"] > 0

    def test_explicit_error_riemann_correction_finite(self):
        result = self.f.psi_explicit_error(10000, N_zeros=100)
        assert math.isfinite(result["riemann_correction"])

    def test_sieve_and_mobius_consistent(self):
        # Los primos p del tamiz deben tener μ(p) = -1
        primes_sieve = set(int(p) for p in self.f._sieve_eratosthenes(50))
        mu = self.f._sieve_mobius_values(50)
        # Verificar que cada primo tiene μ(p) = -1
        for p in primes_sieve:
            assert mu[p] == -1, f"μ({p}) = {mu[p]}, se esperaba -1 (primo)"
        # Verificar que los números con factor cuadrado tienen μ = 0
        for n2 in [4, 9, 25, 36, 49]:
            if n2 <= 50:
                assert mu[n2] == 0, f"μ({n2}) = {mu[n2]}, se esperaba 0"


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def run_all_tests():
    """Ejecuta todos los tests."""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
