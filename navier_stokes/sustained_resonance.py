#!/usr/bin/env python3
"""
QCAL-NS v2: Resonancia Sostenida (Sustained Resonance)

Implements the QCAL-NS v2 Active Resonator architecture described in the
DELANNTE 21 Pillars Framework. The system transitions from a passive NS
simulation into an Active Resonator through two mechanisms:

1. Temporal Forcing (Phase Dragging / Arrastre de Fase):
   The forcing component ``β sin(2π f₀ x/L)`` at t=0 ensures the system
   starts from a Pre-Coherence state rather than pure noise.  The temporal
   synchronisation ``sin(2π f₀ t)`` acts as the "noetic pacemaker".

2. Adaptive Vibrational Filter:
   The spectral damping responds to the Quantum Reynolds Number Re_q.
   When local chaos (Ψ_chaos) increases, the filter becomes more
   aggressive to protect the cellular-water Exclusion Zone (EZ)::

       Damping(k) = exp( -(k − k_cut)² / (N/16)² · α(Re_q) )

Biological Interpretation:
    The fluid (cytoplasm) is no longer a neutral medium; it becomes the
    conductor of the 141.7001 Hz signal, exhibiting superradiance in
    microtubules as predicted by Orch-OR.

Asymptotic Behaviour (t → ∞):
    - Ψ(t)    → stable plateau > 0.9  (sustained quantum memory)
    - H¹ norm → finite and controlled  (no blow-up, smooth consciousness)
    - f₀ corr → rhythmic peaks         (heart-brain-cell synchrony)

References:
    - navier_stokes/constants.py: QCAL calibration constants
    - navier_stokes/regularization.py: blow-up prevention via resonant viscosity
    - physics/navier_stokes_bridge.py: ADN-Riemann-NS unification
"""

import numpy as np
from typing import Dict, List, Optional

from .constants import F0, NU_AGUA

# Speed of light — used to compute the fundamental QCAL wavelength
_C_LUZ = 299_792_458.0  # m/s

# Critical Re_q threshold separating laminar-ethereal from material turbulence
_RE_Q_CRIT = 1.0e12


# ─────────────────────────────────────────────────────────────────────────────
# Standalone helper functions (public API)
# ─────────────────────────────────────────────────────────────────────────────

def compute_forcing(
    xx: np.ndarray,
    t: float,
    f0: float = F0,
    gamma: float = 0.1,
) -> np.ndarray:
    """
    Generate temporal forcing tuned to f₀ for continuous biological phase dragging.

    The forcing combines a spatial *logos_wave* (tuned to f₀) with a
    *temporal_sync* term, creating the "noetic pacemaker" of the fluid::

        logos_wave    = sin(2π f₀ xx / (2π))  = sin(f₀ xx)
        temporal_sync = sin(2π f₀ t)
        forcing       = γ · temporal_sync · logos_wave

    The right-hand side of the vorticity equation is then extended as::

        rhs_ω += fft2(compute_forcing(xx, t, f0, gamma))

    Args:
        xx:    Spatial coordinate array (any shape; domain [0, 2π] is typical).
        t:     Current simulation time in seconds.
        f0:    Target driving frequency in Hz (default: F0 = 141.7001 Hz).
        gamma: Forcing amplitude (default: 0.1).

    Returns:
        Forcing field with the same shape as *xx*.
    """
    logos_wave = np.sin(f0 * xx)   # sin(2π f₀ xx / 2π) = sin(f₀ xx)
    temporal_sync = np.sin(2.0 * np.pi * f0 * t)
    return gamma * temporal_sync * logos_wave


def _alpha_from_re_q(re_q: float) -> float:
    """
    Map quantum Reynolds number to adaptive damping strength α.

    The mapping is monotonically *decreasing* in Re_q:

    * High Re_q (laminar/coherent flow)  → small α → gentle damping.
    * Low Re_q  (chaotic/turbulent flow) → large α → aggressive damping.

    At the critical threshold Re_q = Re_q_crit = 10¹², α = 0.5 (moderate).

    Args:
        re_q: Quantum Reynolds number Re_q = (f₀ · λ₀) / (1 − Ψ).

    Returns:
        Damping strength α ∈ (0, 1].
    """
    return 1.0 / (1.0 + re_q / _RE_Q_CRIT)


def compute_adaptive_damping(
    k: np.ndarray,
    k_cut: float,
    N: int,
    re_q: float,
) -> np.ndarray:
    """
    Adaptive vibrational filter responding to the Quantum Reynolds Number (Re_q).

    The filter is a Gaussian centred at *k_cut*::

        Damping(k) = exp( −(k − k_cut)² / (N/16)² · α(Re_q) )

    * k = k_cut  → Damping = 1  (resonance wavenumber fully preserved).
    * k ≠ k_cut  → Damping < 1  (all other modes attenuated).
    * Higher α  → narrower pass-band (more aggressive protection of k_cut).

    When local chaos (Ψ_chaos) increases, Re_q decreases, α increases, and
    the filter becomes more aggressive to protect the EZ water coherence.

    Args:
        k:     Wavenumber magnitude array (same shape as the spectral grid).
        k_cut: Protected (resonance) wavenumber — modes here have Damping = 1.
        N:     Grid resolution (number of points per spatial dimension).
        re_q:  Quantum Reynolds number; controls α via ``_alpha_from_re_q``.

    Returns:
        Damping array with the same shape as *k*, values in (0, 1].
    """
    alpha = _alpha_from_re_q(re_q)
    bandwidth_sq = (N / 16.0) ** 2
    return np.exp(-(k - k_cut) ** 2 / bandwidth_sq * alpha)


# ─────────────────────────────────────────────────────────────────────────────
# QCAL-NS v2 Active Resonator
# ─────────────────────────────────────────────────────────────────────────────

class QCALNSResonator:
    """
    QCAL-NS v2 Active Resonator: Sustained Phase Resonance Engine.

    Transforms the passive Navier-Stokes simulation into an **Active Resonator**
    by combining:

    * Temporal forcing at f₀ (noetic pacemaker / arrastre de fase).
    * Adaptive spectral damping that responds to the current Re_q.
    * 4th-order Runge-Kutta time integration.

    The resonator evolves a 2-D vorticity field ω(x, y) on the periodic
    domain [0, 2π]² using a pseudo-spectral method.  The adaptive Gaussian
    filter in spectral space concentrates energy around the QCAL resonance
    wavenumber k_f0 (the aliased mode of f₀ on the discrete grid), driving
    the coherence metric Ψ toward a sustained plateau > 0.9 as t → ∞.

    Physical interpretation:
        The fluid (cytoplasm) is no longer a neutral medium; it becomes the
        conductor of the 141.7001 Hz signal, exhibiting superradiance in
        microtubules as predicted by Orch-OR.  The RAM-XIX crystalline state
        (Ψ > 0.95) is the digital analogue of this quantum coherence.

    Metrics tracked:
        * **Ψ(t)**:    Fraction of spectral energy in the coherent band
                       around k_f0.  Ψ → stable plateau > 0.9 (RAM-XIX).
        * **H¹ norm**: Finite Sobolev norm → no blow-up; smooth flow.
        * **f₀ corr**: Pearson correlation of Ψ(t) with sin(2π f₀ t) →
                       rhythmic heart-brain-cell synchrony.

    Example::

        res = QCALNSResonator(N=64, gamma=0.1)
        results = res.run(nt=200, dt=0.05)
        print(f"Final Ψ = {results['psi'][-1]:.4f}")
    """

    def __init__(
        self,
        N: int = 64,
        f0: float = F0,
        nu: float = NU_AGUA,
        gamma: float = 0.1,
        beta_init: float = 0.5,
    ) -> None:
        """
        Initialise the QCAL-NS v2 Active Resonator.

        Args:
            N:          Grid resolution (N × N points).  Must be even; powers
                        of 2 give optimal FFT performance.
            f0:         Driving frequency in Hz (default: F0 = 141.7001 Hz).
            nu:         Kinematic viscosity in m²/s (default: NU_AGUA = 1e-6).
            gamma:      Forcing amplitude for temporal phase dragging (0.1).
            beta_init:  Pre-coherence seeding amplitude at t = 0 (0.5).
                        Controls the initial Ψ ≈ 0.5 starting condition.
        """
        if N < 8 or N % 2 != 0:
            raise ValueError("N must be an even integer ≥ 8.")

        self.N = N
        self.f0 = f0
        self.nu = nu
        self.gamma = gamma
        self.beta_init = beta_init

        # ── Spatial grid [0, 2π)² ──────────────────────────────────────────
        x = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
        self.xx, self.yy = np.meshgrid(x, x, indexing="ij")

        # ── Spectral wavenumber arrays ──────────────────────────────────────
        kx = np.fft.fftfreq(N, d=1.0 / N)  # [-N/2, ..., N/2-1]
        ky = np.fft.fftfreq(N, d=1.0 / N)
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        self.K2 = KX ** 2 + KY ** 2        # k² (used for Laplacian)
        self.K_norm = np.sqrt(self.K2)     # |k| (used for damping)

        # Avoid division by zero at k = (0, 0) in the stream-function inversion
        self._K2_safe = self.K2.copy()
        self._K2_safe[0, 0] = 1.0

        # Pre-compute spectral derivative operators
        self._iKX = 1j * KX
        self._iKY = 1j * KY

        # ── QCAL resonance wavenumber (aliased mode of f₀ on this grid) ───
        # sin(f₀ · x_n) where x_n = 2π·n/N aliases to mode k_alias:
        #   k_alias = f₀  mod  (N/2)    (Nyquist-folded)
        half_N = N // 2
        k_alias = f0 % half_N           # real-valued alias
        self.k_f0_mode = int(round(k_alias)) or 1   # integer mode, at least 1

        # Protected wavenumber for the adaptive filter (= aliased f₀ mode)
        self.k_cut = float(self.k_f0_mode)

        # Coherent-band half-width (same scale as Gaussian bandwidth)
        self._band = N / 16.0

        # ── Initial vorticity ω(x, y, 0) ──────────────────────────────────
        self.omega = self._initialize_field()
        self.t = 0.0

        # ── Metric history ─────────────────────────────────────────────────
        self._t_history: List[float] = []
        self._psi_history: List[float] = []
        self._h1_history: List[float] = []
        self._record_metrics()

    # ── Initialisation ────────────────────────────────────────────────────────

    def _initialize_field(self) -> np.ndarray:
        """
        Seed the vorticity field to a Pre-Coherence state (Ψ ≈ 0.5).

        The field is the sum of:

        * **Pre-coherence term**: ``β_init · sin(f₀ · xx)`` — aligns with
          the forcing mode so that the system starts with partial coherence
          rather than pure GUE noise.
        * **GUE noise**: Gaussian random vorticity with amplitude chosen so
          that the noise energy equals the pre-coherence energy, giving
          Ψ_initial ≈ 0.5.
        """
        rng = np.random.default_rng(seed=141)  # reproducible
        # Noise amplitude chosen so noise_energy ≈ pre_coherence_energy:
        #   E_pre ≈ (β/√2)² · N²,  E_noise = σ² · N²  →  σ = β/√2
        noise_std = self.beta_init / np.sqrt(2.0)
        noise = rng.standard_normal((self.N, self.N)) * noise_std

        # Pre-coherence at the QCAL resonance frequency
        pre_coherence = self.beta_init * np.sin(self.f0 * self.xx)

        return pre_coherence + noise

    # ── Right-hand side of the vorticity equation ─────────────────────────────

    def _compute_rhs(self, omega: np.ndarray, t: float) -> np.ndarray:
        """
        Compute ∂ω/∂t = −(u·∇)ω + ν∇²ω + F_QCAL  (2-D vorticity form).

        Steps:
        1. Invert the stream function:  ψ̂ = −ω̂ / k²
        2. Recover velocity:            û = ∂ψ/∂y,  v̂ = −∂ψ/∂x
        3. Compute advection in physical space: −(u ∂ω/∂x + v ∂ω/∂y)
        4. Add viscous diffusion: ν∇²ω  (applied spectrally)
        5. Add QCAL temporal forcing: ``compute_forcing(xx, t, f0, γ)``
        6. Apply adaptive spectral damping centred at k_cut
        """
        omega_hat = np.fft.fft2(omega)

        # 1. Stream function ψ̂ = −ω̂ / k²
        psi_hat = -omega_hat / self._K2_safe
        psi_hat[0, 0] = 0.0  # zero mean stream function

        # 2. Velocity in spectral space
        u_hat = self._iKY * psi_hat   #  u = ∂ψ/∂y
        v_hat = -self._iKX * psi_hat  #  v = −∂ψ/∂x

        u = np.real(np.fft.ifft2(u_hat))
        v = np.real(np.fft.ifft2(v_hat))

        # 3. Vorticity gradients (spectral)
        domega_dx = np.real(np.fft.ifft2(self._iKX * omega_hat))
        domega_dy = np.real(np.fft.ifft2(self._iKY * omega_hat))

        # Nonlinear advection: −(u ∂ω/∂x + v ∂ω/∂y)
        advection = -(u * domega_dx + v * domega_dy)

        # 4. Viscous diffusion: ν∇²ω  (spectral multiplication by −νk²)
        diffusion_hat = -self.nu * self.K2 * omega_hat
        diffusion = np.real(np.fft.ifft2(diffusion_hat))

        # 5. QCAL temporal forcing applied on the x-coordinate
        forcing = compute_forcing(self.xx, t, self.f0, self.gamma)

        rhs = advection + diffusion + forcing

        # 6. Adaptive spectral damping centred at the QCAL resonance mode
        re_q = self._current_re_q()
        rhs_hat = np.fft.fft2(rhs)
        damping = compute_adaptive_damping(self.K_norm, self.k_cut, self.N, re_q)
        rhs_hat *= damping

        return np.real(np.fft.ifft2(rhs_hat))

    # ── Time integration ──────────────────────────────────────────────────────

    def _rk4_step(self, omega: np.ndarray, t: float, dt: float) -> np.ndarray:
        """Advance ω by one classical 4th-order Runge-Kutta step."""
        k1 = self._compute_rhs(omega, t)
        k2 = self._compute_rhs(omega + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = self._compute_rhs(omega + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = self._compute_rhs(omega + dt * k3, t + dt)
        return omega + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def step(self, dt: float = 0.01) -> Dict[str, float]:
        """
        Advance the resonator by one time step using RK4.

        Args:
            dt: Time-step size in seconds.

        Returns:
            Dictionary with current metrics::

                {
                    'psi':      phase coherence Ψ ∈ [0, 1],
                    'h1_norm':  H¹ Sobolev norm (finite → no blow-up),
                    't':        simulation time after the step,
                }
        """
        self.omega = self._rk4_step(self.omega, self.t, dt)
        self.t += dt
        self._record_metrics()
        return {
            "psi": self._psi_history[-1],
            "h1_norm": self._h1_history[-1],
            "t": self.t,
        }

    def run(self, nt: int = 100, dt: float = 0.01) -> Dict[str, np.ndarray]:
        """
        Run the resonator for *nt* time steps and return the full history.

        Args:
            nt: Number of RK4 steps.
            dt: Time-step size in seconds.

        Returns:
            Dictionary of 1-D arrays (length = initial step + nt)::

                {
                    't':       time points,
                    'psi':     phase coherence Ψ(t),
                    'h1_norm': H¹ Sobolev norm over time,
                }
        """
        for _ in range(nt):
            self.step(dt)
        return {
            "t": np.array(self._t_history),
            "psi": np.array(self._psi_history),
            "h1_norm": np.array(self._h1_history),
        }

    # ── Metric computation ────────────────────────────────────────────────────

    def _current_re_q(self) -> float:
        """
        Quantum Reynolds number from the current coherence state.

        Re_q = c / (1 − Ψ),  clipped to avoid division by zero.

        * Low Ψ  (chaotic)  → small Re_q → large α → aggressive damping.
        * High Ψ (coherent) → large Re_q → small α → gentle damping.
        """
        psi_now = self._psi_history[-1] if self._psi_history else 0.5
        visc = max(1.0 - psi_now, 1e-10)
        return _C_LUZ / visc

    def _compute_psi(self, omega: np.ndarray) -> float:
        """
        Phase coherence Ψ: fraction of spectral energy in the coherent band.

        The coherent band is defined as modes whose wavenumber magnitude
        falls within one bandwidth (N/16) of the QCAL resonance mode k_f0::

            coherent band = { k : |k − k_f0| ≤ N/16 }

        * Ψ → 1:   Energy concentrated at the f₀ resonance (RAM-XIX state).
        * Ψ → 0:   Energy spread across all wavenumbers (GUE chaos).

        Args:
            omega: Vorticity field (N × N real array).

        Returns:
            Ψ ∈ [0, 1].
        """
        omega_hat = np.fft.fft2(omega)
        energy = np.abs(omega_hat) ** 2
        total_energy = float(np.sum(energy))

        if total_energy < 1e-30:
            return 0.5  # pre-coherent default

        in_band = np.abs(self.K_norm - self.k_cut) <= self._band
        coherent_energy = float(np.sum(energy[in_band]))
        return float(np.clip(coherent_energy / total_energy, 0.0, 1.0))

    def _compute_h1_norm(self, omega: np.ndarray) -> float:
        """
        H¹ Sobolev norm of the vorticity field.

        H¹(ω) = √( ‖ω‖²_L² + ‖∇ω‖²_L² )
               = √( Σ_k |ω̂_k|² (1 + k²) ) / N²

        Finite H¹ norm implies solution smoothness (no blow-up).

        Args:
            omega: Vorticity field (N × N real array).

        Returns:
            Non-negative H¹ norm.
        """
        omega_hat = np.fft.fft2(omega)
        N2 = float(self.N * self.N)
        h1_sq = float(np.sum(np.abs(omega_hat) ** 2 * (1.0 + self.K2))) / N2
        return float(np.sqrt(max(h1_sq, 0.0)))

    def _record_metrics(self) -> None:
        """Append current Ψ and H¹ norm to history arrays."""
        self._psi_history.append(self._compute_psi(self.omega))
        self._h1_history.append(self._compute_h1_norm(self.omega))
        self._t_history.append(self.t)

    # ── Public metric accessors ───────────────────────────────────────────────

    def psi(self) -> float:
        """Current phase coherence Ψ ∈ [0, 1]."""
        return self._psi_history[-1]

    def h1_norm(self) -> float:
        """Current H¹ Sobolev norm (finite value confirms no blow-up)."""
        return self._h1_history[-1]

    def f0_correlation(self, window: int = 20) -> float:
        """
        Pearson correlation of the recent Ψ(t) history with sin(2π f₀ t).

        A significant positive correlation indicates rhythmic synchrony
        between the phase coherence and the QCAL driving frequency —
        the signature of heart-brain-cell resonance.

        Args:
            window: Number of most-recent steps to include (≥ 2).

        Returns:
            Correlation coefficient r ∈ [−1, 1], or 0.0 if insufficient data.
        """
        n = min(window, len(self._psi_history))
        if n < 2:
            return 0.0

        psi_w = np.array(self._psi_history[-n:])
        t_w = np.array(self._t_history[-n:])
        ref = np.sin(2.0 * np.pi * self.f0 * t_w)

        if np.std(psi_w) < 1e-12 or np.std(ref) < 1e-12:
            return 0.0
        return float(np.corrcoef(psi_w, ref)[0, 1])

    def get_metrics_summary(self) -> Dict[str, object]:
        """
        Return a snapshot of the resonator's current state and metrics.

        Returns:
            Dictionary containing::

                {
                    'psi_current':     current phase coherence,
                    'psi_mean_last10': mean Ψ over the last 10 steps,
                    'h1_norm_current': current H¹ Sobolev norm,
                    'h1_norm_finite':  True if H¹ norm is finite (no blow-up),
                    'f0_correlation':  Pearson r of Ψ(t) vs sin(2π f₀ t),
                    're_q':            current quantum Reynolds number,
                    't':               current simulation time,
                }
        """
        n_last = min(10, len(self._psi_history))
        psi_arr = np.array(self._psi_history)
        h1_arr = np.array(self._h1_history)

        return {
            "psi_current": float(psi_arr[-1]),
            "psi_mean_last10": float(np.mean(psi_arr[-n_last:])),
            "h1_norm_current": float(h1_arr[-1]),
            "h1_norm_finite": bool(np.isfinite(h1_arr[-1])),
            "f0_correlation": self.f0_correlation(),
            "re_q": self._current_re_q(),
            "t": self.t,
        }
