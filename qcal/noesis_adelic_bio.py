"""NOESIS bridge: adelic spectral, QCAL and PHOENIX biofrequency layers.

This module provides a deterministic computational skeleton for the unified
formalism.  It keeps dimensional quantities explicit: frequencies are Hz,
angular frequencies are rad/s, and the dimensionless bridge coupling is
kappa_B/f0.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

F0_HZ = 141.7001
F_B_HZ = 0.00052
PSI_TARGET = 0.999999
ALPHA_INV_TARGET = 137.035999084


@dataclass(frozen=True)
class QCALConstants:
    f0_hz: float = F0_HZ
    f_b_hz: float = F_B_HZ
    psi_target: float = PSI_TARGET
    alpha_inv_target: float = ALPHA_INV_TARGET

    @property
    def omega0(self) -> float:
        return 2.0 * np.pi * self.f0_hz

    @property
    def omega_b(self) -> float:
        return 2.0 * np.pi * self.f_b_hz

    @property
    def dimensionless_bridge(self) -> float:
        return self.f_b_hz / self.f0_hz


@dataclass(frozen=True)
class AdelicDiracModel:
    """Minimal spectral realization on the logarithmic idelic coordinate.

    For x>0, u=log|x| turns multiplicative dilation into translation.
    The archimedean generator is D_inf=-i d/du.  Finite places enter through
    bounded arithmetic multipliers H_p.  The full self-adjoint candidate is

        H = D_inf + sum_p w_p H_p + g_B V_B,

    with real weights and symmetric V_B.
    """

    prime_weights: tuple[float, ...] = (1.0, 0.5, 1.0 / 3.0)

    def eigenvalue(self, gamma: float, adelic_shift: float = 0.0) -> float:
        arithmetic = float(sum(self.prime_weights)) + adelic_shift
        return gamma + arithmetic


def alpha_flow(
    iterations: int = 1000,
    alpha0: float = 1.0 / 137.0,
    psi0: float = 0.95,
    zeros: np.ndarray | None = None,
) -> dict[str, float]:
    """Deterministic QCAL flow used as a reproducible integration benchmark.

    The zeta ordinates are treated as supplied spectral data.  This routine
    measures convergence of the proposed flow; it does not silently insert
    them as output eigenvalues.
    """
    c = QCALConstants()
    zeros = np.asarray(
        zeros
        if zeros is not None
        else [14.134725141734693, 21.022039638771555,
              25.01085758014569, 30.424876125859513,
              32.93506158773919],
        dtype=float,
    )
    alpha = float(alpha0)
    psi = float(psi0)
    target = 1.0 / c.alpha_inv_target

    for _ in range(iterations):
        spectral = float(np.sum(np.sin(2.0 * np.pi * zeros * alpha)))
        torsion = spectral * c.f_b_hz * (c.f0_hz / 100.0)
        alpha += (target - alpha) * psi + torsion * (1.0 - psi) * 0.1
        psi += (1.0 - psi) * 0.01

    return {
        "alpha": alpha,
        "alpha_inv": 1.0 / alpha,
        "psi": psi,
        "f0_hz": c.f0_hz,
        "f_b_hz": c.f_b_hz,
        "bridge_ratio": c.dimensionless_bridge,
    }


def phoenix_reference(t: np.ndarray, amplitude: float = 1.0) -> np.ndarray:
    """Reference ultra-slow carrier for PHOENIX signal-processing tests."""
    return amplitude * np.sin(2.0 * np.pi * F_B_HZ * np.asarray(t))


def noesis_stress_energy(
    psi: float,
    rho: float,
    gamma: float,
    grad_psi_sq: float = 0.0,
    potential: float = 0.0,
    current_norm: float = 0.0,
) -> dict[str, float]:
    """Scalar effective energy density for the Einstein-QCAL bridge.

    The scalar sector is written as
        rho_N = 1/2 |grad Psi|^2 + V(Psi) + rho_J - gamma(1-Psi)^2.
    It is a bookkeeping model for coupling experiments and simulations.
    """
    rho_j = max(current_norm, 0.0) * max(psi, 0.0)
    dissipative = max(gamma, 0.0) * (1.0 - psi) ** 2
    return {
        "rho_noesis": 0.5 * grad_psi_sq + potential + rho_j - dissipative,
        "rho_classical": float(rho),
        "rho_total": float(rho) + 0.5 * grad_psi_sq + potential + rho_j - dissipative,
        "psi": float(psi),
        "gamma": float(gamma),
    }


__all__ = [
    "QCALConstants", "AdelicDiracModel", "alpha_flow", "phoenix_reference",
    "noesis_stress_energy", "F0_HZ", "F_B_HZ", "PSI_TARGET",
    "ALPHA_INV_TARGET",
]
