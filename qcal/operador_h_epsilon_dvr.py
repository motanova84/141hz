#!/usr/bin/env python3
"""
OperadorHEpsilonDVR — Discrete-Variable-Representation Hamiltonian H_ε
=======================================================================

Constructs the one-dimensional Hamiltonian

    H_ε = H_cin + V_primos(ε)

using a cosine (even-parity) DVR basis over L²[−L, L]:

Basis functions:
    φₙ(x) = (1/√L) · cos(nπx / L),   n = 0, 1, …, N−1

Kinetic matrix (diagonal in momentum space):
    (H_cin)ₙₙ = (nπ/L)² / (2m)     with m = 1 (natural units)

Prime potential:
    V_primos(ε, x) = ε · Σₚ Λ(p) · exp(−(x−log p)² / (2σ²))

where Λ(p) is the von Mangoldt function evaluated at prime powers p^k
and the sum is truncated at |x − log p| > GAUSSIAN_CUTOFF_SIGMA · σ.

The potential matrix is constructed in position space via Gauss–Legendre
quadrature on the DVR grid.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
from typing import Optional

import numpy as np

# ============================================================================
# CONSTANTS
# ============================================================================

# Gaussian cutoff: contributions beyond this many σ are set to zero
GAUSSIAN_CUTOFF_SIGMA: float = 5.0

# Default DVR parameters
DEFAULT_N_BASIS: int = 200       # number of cosine basis functions
DEFAULT_L: float = math.log(100.0)  # box half-length in log-space (≈ 4.605)
DEFAULT_SIGMA: float = 0.5       # Gaussian smoothing width (log-space)
DEFAULT_EPSILON: float = 1.0     # coupling strength ε


# ============================================================================
# HELPER: von Mangoldt function Λ(n)
# ============================================================================

def _lambda_mangoldt(n: int) -> float:
    """
    Return the von Mangoldt function Λ(n).

        Λ(n) = log(p)  if n = p^k for some prime p and integer k ≥ 1
        Λ(n) = 0       otherwise
    """
    if n < 2:
        return 0.0
    # Find the smallest prime factor
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            # p divides n; check if n is a perfect power of p
            m = n
            while m % p == 0:
                m //= p
            if m == 1:
                return math.log(p)
            else:
                return 0.0
    # n itself is prime
    return math.log(n)


# ============================================================================
# PRIME POTENTIAL
# ============================================================================

def construir_potencial_primos(
    x_grid: np.ndarray,
    sigma: float = DEFAULT_SIGMA,
    cutoff_sigma: float = GAUSSIAN_CUTOFF_SIGMA,
    n_mangoldt: int = 200,
) -> np.ndarray:
    """
    Evaluate the von Mangoldt prime potential on *x_grid*.

    V(x) = Σₙ₌₂^{n_mangoldt} Λ(n) · exp(−(x − log n)² / (2σ²))

    Terms with |x − log n| > cutoff_sigma · σ are skipped.

    Parameters
    ----------
    x_grid :
        1-D array of positions (in log-space, i.e. x = log p).
    sigma :
        Gaussian smoothing width.
    cutoff_sigma :
        Truncation threshold in units of σ.
    n_mangoldt :
        Upper limit of the Mangoldt sum.

    Returns
    -------
    np.ndarray
        Potential evaluated at each grid point.
    """
    v = np.zeros(len(x_grid))
    two_sigma2 = 2.0 * sigma * sigma
    cutoff = cutoff_sigma * sigma

    for n in range(2, n_mangoldt + 1):
        lam = _lambda_mangoldt(n)
        if lam == 0.0:
            continue
        log_n = math.log(n)
        for i, x in enumerate(x_grid):
            dx = x - log_n
            if abs(dx) <= cutoff:
                v[i] += lam * math.exp(-dx * dx / two_sigma2)
    return v


# ============================================================================
# DVR COSINE BASIS HAMILTONIAN
# ============================================================================

class OperadorHEpsilonDVR:
    """
    DVR Hamiltonian  H_ε = H_cin + ε · V_primos  on L²[−L, L].

    The cosine (even-parity) basis functions are

        φₙ(x) = (1/√L) · cos(nπx / L),   n = 0, 1, …, N−1

    The matrix elements are computed on a uniform position grid and
    the Hamiltonian matrix is assembled for exact diagonalization.

    Parameters
    ----------
    n_basis :
        Number of cosine basis functions.
    L :
        Box half-length.
    sigma :
        Gaussian smoothing width for V_primos.
    epsilon :
        Coupling constant ε.
    n_grid :
        Number of quadrature points for potential matrix elements.
        Defaults to 4 · n_basis for accuracy.
    n_mangoldt :
        Upper limit of von Mangoldt sum.
    cutoff_sigma :
        Truncation of Gaussian at this many σ.
    """

    def __init__(
        self,
        n_basis: int = DEFAULT_N_BASIS,
        L: float = DEFAULT_L,
        sigma: float = DEFAULT_SIGMA,
        epsilon: float = DEFAULT_EPSILON,
        n_grid: Optional[int] = None,
        n_mangoldt: int = 200,
        cutoff_sigma: float = GAUSSIAN_CUTOFF_SIGMA,
    ) -> None:
        self.n_basis = n_basis
        self.L = L
        self.sigma = sigma
        self.epsilon = epsilon
        self.n_grid = n_grid if n_grid is not None else 4 * n_basis
        self.n_mangoldt = n_mangoldt
        self.cutoff_sigma = cutoff_sigma

        self._H: Optional[np.ndarray] = None

    # ------------------------------------------------------------------
    # Kinetic part (diagonal in basis)
    # ------------------------------------------------------------------

    def _matriz_cinetica(self) -> np.ndarray:
        """
        Return the diagonal kinetic matrix H_cin.

        (H_cin)ₙₙ = (nπ/L)² / 2
        """
        n_arr = np.arange(self.n_basis, dtype=float)
        k_n = n_arr * math.pi / self.L
        return np.diag(k_n ** 2 / 2.0)

    # ------------------------------------------------------------------
    # Potential part
    # ------------------------------------------------------------------

    def _matriz_potencial(self) -> np.ndarray:
        """
        Return the potential matrix V_primos in the cosine basis.

        V_{mn} = ε · ∫₋ₗᴸ φₘ(x) · V(x) · φₙ(x) dx

        computed via Gauss–Legendre quadrature.
        """
        # Quadrature points and weights on [−L, L]
        xi, wi = np.polynomial.legendre.leggauss(self.n_grid)
        x_grid = self.L * xi          # map [−1, 1] → [−L, L]
        weights = self.L * wi         # Jacobian

        # Evaluate V(x) on the quadrature grid
        V_x = construir_potencial_primos(
            x_grid,
            sigma=self.sigma,
            cutoff_sigma=self.cutoff_sigma,
            n_mangoldt=self.n_mangoldt,
        )

        # Basis functions evaluated at quadrature points: shape (n_basis, n_grid)
        n_arr = np.arange(self.n_basis, dtype=float)
        # φₙ(x) = (1/√L) · cos(nπx/L)
        phi = np.cos(np.outer(n_arr * math.pi / self.L, x_grid)) / math.sqrt(self.L)

        # V_{mn} = ε · Σ_i w_i · φ_m(x_i) · V(x_i) · φ_n(x_i)
        # Use einsum for efficiency
        V_mat = self.epsilon * np.einsum("mi,i,i,ni->mn", phi, weights, V_x, phi)
        return V_mat

    # ------------------------------------------------------------------
    # Full Hamiltonian
    # ------------------------------------------------------------------

    def construir(self) -> np.ndarray:
        """
        Assemble and return the full Hamiltonian matrix H_ε.

        Returns
        -------
        np.ndarray, shape (n_basis, n_basis)
        """
        H_cin = self._matriz_cinetica()
        V_mat = self._matriz_potencial()
        self._H = H_cin + V_mat
        return self._H

    @property
    def H(self) -> np.ndarray:
        """Cached Hamiltonian matrix (calls ``construir`` if needed)."""
        if self._H is None:
            self.construir()
        return self._H  # type: ignore[return-value]
