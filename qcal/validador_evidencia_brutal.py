#!/usr/bin/env python3
"""
ValidadorEvidenciaBrutal — Brutal Evidence Validator via Riemann Correlation
=============================================================================

Diagonalizes H_ε, rescales the lowest eigenvalues to match the scale of
the known Riemann zeta zeros, computes the Pearson correlation coefficient ρ,
and converts it to a coherence measure

    Ψ = (1 + |ρ|) / 2

A perfect alignment with the Riemann spectrum gives |ρ| = 1 → Ψ = 1.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
"""

from typing import List, Optional, Tuple

import numpy as np
from scipy import stats

from .operador_h_epsilon_dvr import OperadorHEpsilonDVR

# ============================================================================
# Known imaginary parts of non-trivial Riemann zeta zeros (LMFDB / standard)
# ============================================================================

RIEMANN_ZEROS_KNOWN: List[float] = [
    14.134725141734693790,  # t₁
    21.022039638771554993,  # t₂
    25.010857580145688763,  # t₃
    30.424876125859513210,  # t₄
    32.935061587739189691,  # t₅
    37.586178158825671257,  # t₆
    40.918719012147495187,  # t₇
    43.327073280914999519,  # t₈
    48.005150881167159727,  # t₉
    49.773832477672302181,  # t₁₀
]


# ============================================================================
# VALIDATOR
# ============================================================================

class ValidadorEvidenciaBrutal:
    """
    Validates the spectral evidence of the prime Hamiltonian H_ε against
    the imaginary parts of the known Riemann zeta zeros.

    Workflow
    --------
    1. Build and diagonalize H_ε via OperadorHEpsilonDVR.
    2. Select the *n_zeros* lowest positive eigenvalues.
    3. Rescale them linearly so their mean matches the mean of the
       reference Riemann zeros (pure affine normalization).
    4. Compute Pearson correlation ρ between rescaled eigenvalues and zeros.
    5. Return Ψ = (1 + |ρ|) / 2.

    Parameters
    ----------
    operador :
        A pre-configured OperadorHEpsilonDVR instance.  If None, a default
        operator is built with n_basis=100 (faster for validation).
    riemann_zeros :
        Reference Riemann zeros to compare against.
        Defaults to the first 10 known zeros.
    n_zeros :
        How many eigenvalue/zero pairs to compare.
    """

    def __init__(
        self,
        operador: Optional[OperadorHEpsilonDVR] = None,
        riemann_zeros: Optional[List[float]] = None,
        n_zeros: int = 10,
    ) -> None:
        if operador is None:
            operador = OperadorHEpsilonDVR(n_basis=100)
        self.operador = operador

        self.riemann_zeros: np.ndarray = np.array(
            riemann_zeros if riemann_zeros is not None else RIEMANN_ZEROS_KNOWN,
            dtype=float,
        )
        self.n_zeros = min(n_zeros, len(self.riemann_zeros))

        # Results (populated after calling validar())
        self.eigenvalues: Optional[np.ndarray] = None
        self.eigenvalues_rescalados: Optional[np.ndarray] = None
        self.correlacion_pearson: Optional[float] = None
        self.psi: Optional[float] = None

    # ------------------------------------------------------------------
    # DIAGONALIZATION
    # ------------------------------------------------------------------

    def diagonalizar(self) -> np.ndarray:
        """
        Diagonalize H_ε and return the sorted eigenvalues.

        Returns
        -------
        np.ndarray
            All eigenvalues sorted in ascending order.
        """
        H = self.operador.H  # triggers construir() if needed
        eigenvalues = np.linalg.eigvalsh(H)
        self.eigenvalues = np.sort(eigenvalues)
        return self.eigenvalues

    # ------------------------------------------------------------------
    # RESCALING
    # ------------------------------------------------------------------

    def _rescalar(self, evals: np.ndarray) -> np.ndarray:
        """
        Affine rescaling: map *evals* so that their mean equals the mean
        of the reference Riemann zeros and the standard deviation matches.

        This is a pure normalization that preserves the correlation structure.
        """
        zeros_ref = self.riemann_zeros[: self.n_zeros]
        mu_evals = np.mean(evals)
        std_evals = np.std(evals)
        mu_zeros = np.mean(zeros_ref)
        std_zeros = np.std(zeros_ref)

        if std_evals < 1e-15:
            return np.full_like(evals, mu_zeros)

        rescaled = (evals - mu_evals) / std_evals * std_zeros + mu_zeros
        return rescaled

    # ------------------------------------------------------------------
    # CORRELATION & PSI
    # ------------------------------------------------------------------

    def calcular_correlacion(self) -> float:
        """
        Compute Pearson ρ between the rescaled eigenvalues and Riemann zeros.

        Returns
        -------
        float
            Pearson correlation coefficient in [−1, 1].
        """
        if self.eigenvalues is None:
            self.diagonalizar()

        # Select n_zeros lowest eigenvalues
        evals = self.eigenvalues[: self.n_zeros]
        zeros_ref = self.riemann_zeros[: self.n_zeros]

        self.eigenvalues_rescalados = self._rescalar(evals)

        rho, _ = stats.pearsonr(self.eigenvalues_rescalados, zeros_ref)
        self.correlacion_pearson = float(rho)
        return self.correlacion_pearson

    def calcular_psi(self) -> float:
        """
        Compute coherence Ψ = (1 + |ρ|) / 2.

        Returns
        -------
        float
            Ψ ∈ [0.5, 1.0].
        """
        if self.correlacion_pearson is None:
            self.calcular_correlacion()
        self.psi = (1.0 + abs(self.correlacion_pearson)) / 2.0
        return self.psi

    # ------------------------------------------------------------------
    # FULL PIPELINE
    # ------------------------------------------------------------------

    def validar(self) -> dict:
        """
        Run the full validation pipeline.

        Returns
        -------
        dict with keys:
            eigenvalues, eigenvalues_rescalados, riemann_zeros,
            correlacion_pearson, psi.
        """
        self.diagonalizar()
        self.calcular_correlacion()
        self.calcular_psi()

        return {
            "eigenvalues": self.eigenvalues,
            "eigenvalues_rescalados": self.eigenvalues_rescalados,
            "riemann_zeros": self.riemann_zeros[: self.n_zeros],
            "correlacion_pearson": self.correlacion_pearson,
            "psi": self.psi,
        }
