"""QCAL v3.1 research models.

These routines are deliberately model-level utilities. They do not claim to
prove RH, derive alpha from adelic geometry, or establish a biological effect.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

F0_HZ = 141.7001
F_B_HZ = 0.00052
ALPHA_INV_REFERENCE = 137.035999


@dataclass(frozen=True)
class AdelicParameters:
    f0_hz: float = F0_HZ
    f_b_hz: float = F_B_HZ
    alpha_inv_reference: float = ALPHA_INV_REFERENCE
    kappa_b: float = 0.0  # dimensionless coupling; must be specified independently


def adelic_period(f_hz: float) -> float:
    """Return period in seconds for a strictly positive frequency."""
    if f_hz <= 0:
        raise ValueError("frequency must be positive")
    return 1.0 / f_hz


def dirac_dilation_symbol(xi: np.ndarray | float) -> np.ndarray:
    """Fourier symbol of D=-i d/du on L2(R,du): multiplication by xi.

    This is the archimedean dilation generator after u=log(x). Its spectrum
    is continuous, so this function must not be interpreted as a zeta-zero
    generator.
    """
    return np.asarray(xi, dtype=float)


def phase_coupling(
    gamma: np.ndarray,
    alpha: float,
    f0_hz: float = F0_HZ,
    kappa_b: float = 0.0,
) -> np.ndarray:
    """Phenomenological phase coupling used for sensitivity studies only.

    The function is intentionally explicit about its status: `gamma` may be
    supplied from an external zeta-zero dataset, but no inverse problem or
    convergence to alpha is implied.
    """
    gamma = np.asarray(gamma, dtype=float)
    phase = 2.0 * np.pi * gamma * alpha
    return np.sin(phase) * kappa_b * (f0_hz / 100.0)


def alpha_flow(
    alpha0: float,
    gamma: np.ndarray,
    *,
    target_alpha: float = 1.0 / ALPHA_INV_REFERENCE,
    f0_hz: float = F0_HZ,
    kappa_b: float = 0.0,
    coherence0: float = 0.95,
    steps: int = 1000,
    relaxation: float = 0.05,
) -> tuple[np.ndarray, np.ndarray]:
    """Run a transparent phenomenological alpha flow.

    The target alpha is an externally supplied reference. Therefore this
    routine tests numerical stability of a chosen model; it does not derive
    alpha from first principles.
    """
    if steps <= 0 or relaxation < 0:
        raise ValueError("steps must be positive and relaxation non-negative")
    if not (0.0 <= coherence0 <= 1.0):
        raise ValueError("coherence0 must lie in [0,1]")

    a = float(alpha0)
    psi = float(coherence0)
    alphas = np.empty(steps + 1)
    psis = np.empty(steps + 1)
    alphas[0], psis[0] = a, psi

    for k in range(steps):
        correction = float(np.mean(phase_coupling(gamma, a, f0_hz, kappa_b)))
        a += relaxation * psi * (target_alpha - a) + (1.0 - psi) * correction
        psi += 0.01 * (1.0 - psi)
        alphas[k + 1], psis[k + 1] = a, psi

    return alphas, psis


def lockin_at_frequency(signal: np.ndarray, fs_hz: float, target_hz: float) -> dict[str, float]:
    """Estimate amplitude/phase at a target frequency by complex projection.

    This is preferable to treating a single Welch bin as a detection criterion
    when the record is short relative to the target period.
    """
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or x.size < 8:
        raise ValueError("signal must be a one-dimensional record with >=8 samples")
    if fs_hz <= 0 or target_hz <= 0:
        raise ValueError("fs_hz and target_hz must be positive")

    t = np.arange(x.size) / fs_hz
    z = np.mean((x - np.mean(x)) * np.exp(-2j * np.pi * target_hz * t))
    amplitude = 2.0 * abs(z)
    phase = float(np.angle(z))
    return {"frequency_hz": float(target_hz), "amplitude": float(amplitude), "phase_rad": phase}


def required_cycles(cycles: float = 5.0, f_hz: float = F_B_HZ) -> float:
    """Minimum acquisition duration in seconds for the requested cycles."""
    if cycles <= 0 or f_hz <= 0:
        raise ValueError("cycles and frequency must be positive")
    return cycles / f_hz
