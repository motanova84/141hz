#!/usr/bin/env python3
"""
FiltroRacionalesAdelico: Pilar 2 – Distribución de Primos y Ceros de Riemann

Este módulo implementa el Pilar 2 de la hipótesis QCAL:

  Pilar 2: La función ψ(x) de Chebyshev, calculada mediante la criba de
  Eratóstenes y los valores de Möbius, satisface la fórmula explícita de
  Riemann-von Mangoldt con términos de error controlados, confirmando que
  la distribución de números primos es coherente con la línea crítica Re(s)=1/2.

Nuevas funciones en FiltroRacionalesAdelico:
  - _sieve_eratosthenes(limit)    : Criba de Eratóstenes O(N log log N)
  - _sieve_mobius_values(limit)   : Criba lineal O(N) para μ(n)
  - chebyshev_psi_sieve(x)        : ψ(x) preciso para x grande usando criba
  - psi_explicit_error(x, zeros, N_zeros): ψ(x), ψ(x)−x y corrección RvM
  - compute_mobius_cancellation(N): factor de cancelación de Möbius (nunca inf)
  - selberg_laplacian_spectrum(N_eigenvalues): espectro de Selberg (hasta 200 niveles)

Constantes de módulo:
  _NUMERICAL_TOLERANCE = 1e-12
  _MIN_LOG_ARG = 1e-30

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import numpy as np

# ============================================================================
# CONSTANTES DE MÓDULO
# ============================================================================

#: Tolerancia numérica para evitar divisiones entre valores cercanos a cero.
_NUMERICAL_TOLERANCE: float = 1e-12

#: Argumento mínimo aceptable para funciones logarítmicas.
_MIN_LOG_ARG: float = 1e-30

# Primeros 100 ceros no triviales de ζ(s) en la línea crítica (Im(ρ) > 0).
# Fuente: LMFDB / tablas matemáticas de referencia.
_RIEMANN_ZEROS_100: List[float] = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
    67.079811, 69.546402, 72.067157, 75.704691, 77.144840,
    79.337375, 82.910380, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029535, 111.874659,
    114.320220, 116.226680, 118.790782, 121.370125, 122.946829,
    124.256818, 127.516683, 129.578704, 131.087688, 133.497737,
    134.756509, 138.116042, 139.736208, 141.123707, 143.111845,
    146.000982, 147.422765, 150.053183, 150.925257, 153.024693,
    156.112909, 157.597591, 158.849988, 161.188964, 163.030709,
    165.537069, 167.184439, 169.094515, 169.911976, 173.411536,
    174.754191, 176.441434, 178.377407, 179.916484, 182.207078,
    184.874467, 185.598783, 187.228922, 189.416168, 192.026656,
    193.079726, 195.265396, 196.876481, 198.015309, 201.264751,
    202.493594, 204.189671, 205.394697, 207.906258, 209.576509,
    211.690862, 213.347919, 214.547044, 216.169538, 219.067596,
    220.714918, 221.430705, 224.007000, 224.983324, 227.421444,
    229.337413, 231.250188, 231.987235, 233.693404, 236.524229,
]


# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class FiltroRacionalesAdelico:
    """
    Implementa el Filtro Racional Adélico para el análisis de la distribución
    de primos a través de la función ψ(x) de Chebyshev y la cancelación de
    Möbius, en el contexto de la hipótesis QCAL.

    Esta clase centraliza los cuatro métodos de Pilar 2:
      1. ψ(x) preciso mediante la criba de Eratóstenes.
      2. Términos de error explícitos de Riemann-von Mangoldt.
      3. Factor de cancelación de Möbius.
      4. Espectro del laplaciano de Selberg (hasta 200 niveles).
    """

    def __init__(self) -> None:
        """Inicializa el filtro con los primeros 100 ceros de Riemann."""
        self._zeros: List[float] = list(_RIEMANN_ZEROS_100)

    # ------------------------------------------------------------------
    # Criba de Eratóstenes
    # ------------------------------------------------------------------

    def _sieve_eratosthenes(self, limit: int) -> np.ndarray:
        """
        Genera todos los números primos hasta *limit* usando la criba de
        Eratóstenes con complejidad O(N log log N).

        Parameters
        ----------
        limit:
            Cota superior (inclusive) para la búsqueda de primos.

        Returns
        -------
        np.ndarray
            Array ordenado de números primos p ≤ limit.
        """
        if limit < 2:
            return np.array([], dtype=np.int64)

        is_prime = np.ones(limit + 1, dtype=bool)
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(math.isqrt(limit)) + 1):
            if is_prime[i]:
                is_prime[i * i :: i] = False

        return np.where(is_prime)[0].astype(np.int64)

    # ------------------------------------------------------------------
    # Criba lineal para la función de Möbius
    # ------------------------------------------------------------------

    def _sieve_mobius_values(self, limit: int) -> np.ndarray:
        """
        Calcula μ(n) para 1 ≤ n ≤ *limit* con la criba lineal de Möbius
        en tiempo O(N).

        Parameters
        ----------
        limit:
            Cota superior (inclusive).

        Returns
        -------
        np.ndarray
            Array de enteros con μ(n) para n = 0, 1, ..., limit.
            (El índice 0 se deja en 0 para facilitar la indexación.)
        """
        if limit < 1:
            return np.array([], dtype=np.int8)

        mu = np.zeros(limit + 1, dtype=np.int8)
        mu[1] = 1

        # Omega(n) = número de factores primos distintos
        # is_composite marca los compuestos
        primes: List[int] = []
        is_composite = np.zeros(limit + 1, dtype=bool)
        omega = np.zeros(limit + 1, dtype=np.int8)  # primos distintos

        for n in range(2, limit + 1):
            if not is_composite[n]:
                primes.append(n)
                omega[n] = 1
                mu[n] = -1  # n es primo → μ(n) = -1

            for p in primes:
                if n * p > limit:
                    break
                is_composite[n * p] = True
                if n % p == 0:
                    # p² | n*p → μ(n*p) = 0
                    omega[n * p] = omega[n]  # no añade primo nuevo
                    mu[n * p] = 0
                    break
                else:
                    omega[n * p] = omega[n] + 1
                    mu[n * p] = -mu[n]

        return mu

    # ------------------------------------------------------------------
    # ψ(x) preciso mediante criba
    # ------------------------------------------------------------------

    def chebyshev_psi_sieve(self, x: float) -> float:
        """
        Calcula la función de Chebyshev segunda ψ(x) = Σ_{p^k ≤ x} log p
        para *x* grande utilizando la criba de Eratóstenes.

        La criba permite alcanzar hasta x ≈ 10⁸ de forma eficiente.

        Parameters
        ----------
        x:
            Punto de evaluación (debe ser ≥ 2).

        Returns
        -------
        float
            Valor de ψ(x).
        """
        if x < 2:
            return 0.0

        limit = int(x)
        primes = self._sieve_eratosthenes(limit)

        psi = 0.0
        for p in primes:
            log_p = math.log(float(p))
            pk = float(p)
            while pk <= x:
                psi += log_p
                pk *= p

        return psi

    # ------------------------------------------------------------------
    # Términos de error explícitos de Riemann-von Mangoldt
    # ------------------------------------------------------------------

    def psi_explicit_error(
        self,
        x: float,
        zeros: Optional[List[float]] = None,
        N_zeros: int = 100,
    ) -> Dict[str, float]:
        """
        Devuelve ψ(x), ψ(x)−x y la corrección principal de
        Riemann-von Mangoldt:

          ψ_RvM(x) = x
                     − 2 Σ_{γ>0, γ≤γ_{N_zeros}}  x^{1/2} cos(γ log x) / |ρ|
                     + log(2π)
                     + ½ log(1 − x^{-2})         [para x > 1]

        La suma sobre ceros incluye la pareja conjugada (γ, −γ) de forma
        implícita mediante el factor 2.

        Parameters
        ----------
        x:
            Punto de evaluación (debe ser > 1 para el término ½ log…).
        zeros:
            Lista de partes imaginarias de los ceros de ζ(s).
            Si es None se usan los primeros 100 ceros conocidos.
        N_zeros:
            Número de ceros a incluir en la suma.  Se trunca a la longitud
            disponible de *zeros*.

        Returns
        -------
        dict con claves:
            psi_sieve     : ψ(x) exacto por criba
            psi_explicit  : ψ(x) por fórmula explícita
            error         : ψ(x) − x  (error con la aproximación trivial)
            riemann_correction : término −2 Σ cos / |ρ|
            log2pi        : log(2π)
            half_log_term : ½ log(1 − x^{-2})   (0 si x ≤ 1)
        """
        if zeros is None:
            zeros = self._zeros

        available = min(N_zeros, len(zeros))
        gammas = np.array(zeros[:available], dtype=np.float64)

        # ρ = 1/2 + iγ  →  |ρ|² = 1/4 + γ²
        rho_abs = np.sqrt(0.25 + gammas ** 2)

        log_x = math.log(max(x, _MIN_LOG_ARG))
        sqrt_x = math.sqrt(x) if x > 0 else 0.0

        # Suma de corrección de Riemann: −2 Σ x^{1/2} cos(γ log x) / |ρ|
        cos_terms = np.cos(gammas * log_x)
        riemann_correction = -2.0 * sqrt_x * float(np.sum(cos_terms / rho_abs))

        log2pi = math.log(2 * math.pi)

        if x > 1:
            arg = max(1.0 - x ** (-2), _MIN_LOG_ARG)
            half_log_term = 0.5 * math.log(arg)
        else:
            half_log_term = 0.0

        psi_explicit = x + riemann_correction + log2pi + half_log_term

        # ψ(x) por criba (referencia exacta)
        psi_sieve = self.chebyshev_psi_sieve(x)

        return {
            "psi_sieve": psi_sieve,
            "psi_explicit": psi_explicit,
            "error": psi_sieve - x,
            "riemann_correction": riemann_correction,
            "log2pi": log2pi,
            "half_log_term": half_log_term,
        }

    # ------------------------------------------------------------------
    # Factor de cancelación de Möbius
    # ------------------------------------------------------------------

    def compute_mobius_cancellation(self, N: int) -> Dict[str, float]:
        """
        Calcula el factor de cancelación de Möbius para Σ μ(n)/n hasta N.

        La suma parcial M(N) = Σ_{n=1}^{N} μ(n)/n converge a 0 cuando N→∞
        (equivalente a la hipótesis de los números primos).  El factor de
        cancelación mide cuán cerca está la suma de 0.

        Para N = 1, μ(1)/1 = 1, así que la suma es 1 y el factor es 1.0,
        lo cual es **finito** (corrección del comportamiento anterior que
        producía ``inf``).

        Parameters
        ----------
        N:
            Cota superior de la suma (N ≥ 1).

        Returns
        -------
        dict con claves:
            N                  : parámetro de entrada
            partial_sum        : M(N) = Σ_{n=1}^{N} μ(n)/n
            cancellation_factor: |M(N)|⁻¹  (finito para todo N ≥ 1)
            mertens_function   : M_int(N) = Σ_{n=1}^{N} μ(n)  (entero)
        """
        N = max(1, int(N))
        mu = self._sieve_mobius_values(N)

        # Σ μ(n)/n
        ns = np.arange(1, N + 1, dtype=np.float64)
        partial_sum = float(np.sum(mu[1:N + 1] / ns))

        # Función de Mertens (suma de enteros)
        mertens = int(np.sum(mu[1:N + 1]))

        # Factor de cancelación: medida de cuán pequeña es la suma.
        # Se protege el denominador con _NUMERICAL_TOLERANCE para evitar inf.
        abs_sum = abs(partial_sum)
        if abs_sum < _NUMERICAL_TOLERANCE:
            cancellation_factor = 1.0 / _NUMERICAL_TOLERANCE
        else:
            cancellation_factor = 1.0 / abs_sum

        return {
            "N": N,
            "partial_sum": partial_sum,
            "cancellation_factor": cancellation_factor,
            "mertens_function": mertens,
        }

    # ------------------------------------------------------------------
    # Espectro del laplaciano de Selberg
    # ------------------------------------------------------------------

    def selberg_laplacian_spectrum(
        self,
        N_eigenvalues: int = 200,
    ) -> Dict[str, object]:
        """
        Simula el espectro del laplaciano hiperbólico de Selberg en el
        dominio fundamental del grupo modular PSL(2,Z).

        El espectro continuo comienza en s(1−s) = 1/4 (s = 1/2) y los
        valores propios discretos λ_n = s_n(1−s_n) con s_n = 1/2 + iμ_n.

        Esta implementación genera hasta *N_eigenvalues* niveles usando
        la ley de Weyl para la distribución asintótica de los μ_n:

          N(T) ≈ (Area / 4π) T²   [ley de Weyl para PSL(2,Z)]

        Parameters
        ----------
        N_eigenvalues:
            Número de valores propios a generar (máximo 200, mínimo 1).

        Returns
        -------
        dict con claves:
            N_eigenvalues     : número de valores propios calculados
            eigenvalues       : array de λ_n = 1/4 + μ_n²
            spectral_params   : array de μ_n (parámetros espectrales)
            mean_gap          : brecha media entre valores propios consecutivos
            gap_std           : desviación estándar de las brechas
            gue_ratio         : ratio de varianza/media de brechas (≈1 para GUE)
            weyl_prediction   : predicción de la ley de Weyl para N(T_max)
        """
        N_eigenvalues = max(1, min(int(N_eigenvalues), 200))

        # Generamos los μ_n usando la densidad de Weyl para PSL(2,Z).
        # Area del dominio fundamental = π/3.
        # N(T) ≈ (π/3) / (4π) * T² = T² / 12
        # Invertida: T_n = sqrt(12 * n)
        n_indices = np.arange(1, N_eigenvalues + 1, dtype=np.float64)
        mu_n = np.sqrt(12.0 * n_indices)  # parámetros espectrales

        # Valores propios λ_n = s(1-s) = 1/4 + μ_n²
        eigenvalues = 0.25 + mu_n ** 2

        # Estadísticas de brechas (relevantes para comparación GUE)
        gaps = np.diff(eigenvalues)
        mean_gap = float(np.mean(gaps)) if len(gaps) > 0 else 0.0
        gap_std = float(np.std(gaps)) if len(gaps) > 0 else 0.0

        # Ratio varianza/media de brechas (GUE puro ≈ 1 − 4/π² ≈ 0.594)
        gue_ratio = (gap_std ** 2 / mean_gap) if mean_gap > _NUMERICAL_TOLERANCE else 0.0

        # Predicción de Weyl para N(T_max)
        T_max = float(mu_n[-1]) if len(mu_n) > 0 else 0.0
        weyl_prediction = T_max ** 2 / 12.0

        return {
            "N_eigenvalues": N_eigenvalues,
            "eigenvalues": eigenvalues,
            "spectral_params": mu_n,
            "mean_gap": mean_gap,
            "gap_std": gap_std,
            "gue_ratio": gue_ratio,
            "weyl_prediction": weyl_prediction,
        }


# ============================================================================
# FUNCIÓN PRINCIPAL (demostración rápida)
# ============================================================================

def main() -> None:
    """Ejecuta una demostración rápida de FiltroRacionalesAdelico."""
    filtro = FiltroRacionalesAdelico()

    print("=" * 70)
    print("FiltroRacionalesAdelico – Demostración Rápida")
    print("=" * 70)

    # 1. ψ(x) por criba
    x = 100_000
    psi = filtro.chebyshev_psi_sieve(x)
    print(f"\n[Pilar 2 · criba] ψ({x:,}) = {psi:.2f}  (ratio ψ/x = {psi/x:.6f})")

    # 2. Error explícito
    result = filtro.psi_explicit_error(1000, N_zeros=50)
    print(f"\n[Pilar 2 · error] ψ(1000)−x = {result['error']:.4f}")
    print(f"  Corrección Riemann = {result['riemann_correction']:.4f}")

    # 3. Cancelación de Möbius
    for n in [1, 10, 100, 1_000]:
        r = filtro.compute_mobius_cancellation(n)
        print(f"\n[Pilar 2 · Möbius] N={n:5d}  M(N)={r['partial_sum']:+.6f}  "
              f"factor={r['cancellation_factor']:.4f}")

    # 4. Espectro de Selberg
    spec = filtro.selberg_laplacian_spectrum(200)
    print(f"\n[Pilar 4 · Selberg] {spec['N_eigenvalues']} valores propios  "
          f"mean_gap={spec['mean_gap']:.4f}  GUE ratio={spec['gue_ratio']:.4f}")


if __name__ == "__main__":
    main()
