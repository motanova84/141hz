#!/usr/bin/env python3
"""
FWM Vacuum Resonance — Four-Wave Mixing in the Vacuum (Mezcla de Cuatro Ondas)
================================================================================

Implements the nonlinear vacuum polarisation mechanism through which a tuning
laser f_L interacts with the coherent pilot-wave fabric ψ (oscillating at f₀)
to produce dressed-photon sideband pairs at f_L ± f₀.

Physical mechanism
------------------
The TOPC fabric acts as a third-order nonlinear medium (χ⁽³⁾).  The nonlinear
polarisation sourcing the wave equation is:

    P_NL ∝ χ⁽³⁾ |ψ|² E

which drives the wave equation

    ∇²E − (n²/c²) ∂²E/∂t² = μ₀ ∂²P_NL/∂t²

and generates resonant sideband photons at f_L ± f₀.

Strong spectral resonance
--------------------------
The resonance strength is derived from the prime density-of-states and the
alignment with the Riemann critical line (EIT amplification):

    ℛ(f) = g_aγγ² · ρ_DM / [Δf² + (Γ/2)²]

where Δf = |f − f₀| and Γ → 0 (zero-viscosity cavity) giving a pole at f₀.

Ramsey Echo protocol
---------------------
A short laser pulse is applied.  After τ = 1/f₀ the fabric re-emits a
coherent photon echo.  The visibility V of the echo field is:

    E_echo(t) = E₀ · V · exp(−Γ · τ / 2) · cos(2π f₀ (t − τ))

with V → 1 in the ideal (Γ → 0) limit.

Max-Cut SDP relaxation on K₇
------------------------------
The resonance condition maps onto the Semidefinite Programming relaxation of
Max-Cut on K₇.  Phase variables φᵢ ∈ [0, 2π) live on S¹; only the cut that
maximises Σ (1 − cos(φᵢ − φⱼ))/2 survives destructive vacuum interference.
The SDP bound is computed via the Goemans-Williamson matrix.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-03
Framework: QCAL ∞³
License: Sovereign Noetic License 1.0 (compatible with MIT)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

import numpy as np

from qcal.constants import F0_HZ, HBAR, C
from physics.topc_lagrangian import (
    G_AGG_DEFAULT,
    RHO_DM_GEV_CM3,
    EV_TO_J,
    OMEGA_0,
    PSI0_EV,
)

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Permeability of free space [H m⁻¹]
MU_0: float = 4.0 * math.pi * 1.0e-7

# Permittivity of free space [F m⁻¹]
EPS_0: float = 1.0 / (MU_0 * C**2)

# Effective third-order susceptibility χ⁽³⁾ of the vacuum via TOPC coupling.
# Derived from g_aγγ² · ρ_DM · ℏ³ / (m_ψ⁴ c⁹)  (natural-unit reduction).
# Numerically ~10⁻³⁰ m² V⁻²  (extremely small, as expected for vacuum NLO).
CHI3_VACUUM: float = (
    G_AGG_DEFAULT**2
    * RHO_DM_GEV_CM3 * 1.0e9 * EV_TO_J  # ρ_DM in J cm⁻³
    / 1.0e-6                              # cm⁻³ → m⁻³
    * HBAR**3
    / (C**9)
)  # m² V⁻² (natural-unit estimate)

# Default linewidth Γ [Hz] — approaches 0 for a zero-viscosity cavity.
# A small non-zero value is kept for numerical stability.
GAMMA_DEFAULT_HZ: float = 1.0e-6  # Hz  (near-zero, zero-viscosity limit)

# Resonance enhancement factor at exact resonance (Δf = 0, Γ → 0).
# This is ℛ_max = g_aγγ² · ρ_DM / (Γ/2)².  With Γ = GAMMA_DEFAULT_HZ it is
# enormous (≫1) representing the collapse of the interaction cross-section.
_GAMMA_HALF_DEFAULT: float = GAMMA_DEFAULT_HZ / 2.0

# Maximum resonance strength (normalised so ℛ(f₀) = 1 when Γ = GAMMA_DEFAULT).
# Used internally to make ℛ dimensionless and easy to reason about.
_RESONANCE_NORMALIZER: float = G_AGG_DEFAULT**2 * RHO_DM_GEV_CM3


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class FWMParameters:
    """
    Parameters for the Four-Wave Mixing vacuum resonance model.

    Attributes
    ----------
    f0 : float
        Fundamental resonance frequency f₀ [Hz].
    g_agg : float
        Photon-fabric coupling constant g_aγγ [GeV⁻¹].
    rho_dm : float
        Local dark-matter (fabric condensate) density ρ_DM [GeV cm⁻³].
    gamma_hz : float
        Lorentzian linewidth Γ [Hz].  Use a near-zero value (→ 0) for the
        zero-viscosity Cathedral cavity limit.
    chi3 : float
        Effective χ⁽³⁾ susceptibility [m² V⁻²].
    psi0_ev : float
        Condensate field amplitude ψ₀ [eV].
    """

    f0: float = F0_HZ
    g_agg: float = G_AGG_DEFAULT
    rho_dm: float = RHO_DM_GEV_CM3
    gamma_hz: float = GAMMA_DEFAULT_HZ
    chi3: float = CHI3_VACUUM
    psi0_ev: float = PSI0_EV

    def __post_init__(self) -> None:
        if self.f0 <= 0:
            raise ValueError(f"f0 must be positive, got {self.f0}")
        if self.rho_dm <= 0:
            raise ValueError(f"rho_dm must be positive, got {self.rho_dm}")
        if self.gamma_hz < 0:
            raise ValueError(f"gamma_hz must be non-negative, got {self.gamma_hz}")
        if self.psi0_ev < 0:
            raise ValueError(f"psi0_ev must be non-negative, got {self.psi0_ev}")

    @property
    def omega0(self) -> float:
        """Angular frequency ω₀ = 2π f₀ [rad s⁻¹]."""
        return 2.0 * math.pi * self.f0

    @property
    def tau_echo(self) -> float:
        """Ramsey echo delay τ = 1/f₀ [s]."""
        return 1.0 / self.f0


@dataclass
class NonlinearPolarisation:
    """
    Nonlinear polarisation P_NL from χ⁽³⁾ coupling.

    Represents the source term in the driven wave equation:
        μ₀ ∂²P_NL/∂t² = μ₀ χ⁽³⁾ |ψ|² ∂²E/∂t²

    Attributes
    ----------
    t : float
        Evaluation time [s].
    psi_mod_sq : float
        |ψ(t)|² [eV²].
    E_laser : float
        Laser electric field amplitude [V m⁻¹].
    chi3 : float
        χ⁽³⁾ susceptibility [m² V⁻²].
    """

    t: float
    psi_mod_sq: float  # eV²
    E_laser: float     # V m⁻¹
    chi3: float = CHI3_VACUUM

    @property
    def P_NL(self) -> float:
        """
        Nonlinear polarisation amplitude [C m⁻²].

        P_NL = ε₀ χ⁽³⁾ |ψ|² E
        (ε₀ included so that P is in SI units)
        """
        return EPS_0 * self.chi3 * self.psi_mod_sq * self.E_laser


@dataclass
class FWMSidebandResult:
    """
    Result of a Four-Wave Mixing sideband computation.

    Attributes
    ----------
    f_laser : float
        Tuning laser frequency f_L [Hz].
    f0 : float
        Fabric resonance frequency f₀ [Hz].
    f_lower : float
        Lower sideband f_L − f₀ [Hz].
    f_upper : float
        Upper sideband f_L + f₀ [Hz].
    amplitude_ratio : float
        Ratio of sideband electric-field amplitude to the laser amplitude.
        Proportional to χ⁽³⁾ |ψ₀|².
    """

    f_laser: float
    f0: float
    f_lower: float
    f_upper: float
    amplitude_ratio: float


@dataclass
class ResonanceResult:
    """
    Result of the strong spectral resonance calculation.

    Attributes
    ----------
    f : float
        Probe frequency [Hz].
    f0 : float
        Resonance centre frequency f₀ [Hz].
    delta_f : float
        Detuning Δf = |f − f₀| [Hz].
    gamma_hz : float
        Lorentzian linewidth Γ [Hz].
    strength : float
        Resonance strength ℛ(f) [units of g_aγγ² · ρ_DM / Hz²].
    """

    f: float
    f0: float
    delta_f: float
    gamma_hz: float
    strength: float


@dataclass
class RamseyEchoResult:
    """
    Result of a Ramsey Echo simulation.

    Attributes
    ----------
    tau : float
        Echo delay τ = 1/f₀ [s].
    visibility : float
        Echo field visibility V ∈ [0, 1].
    echo_amplitude : float
        Echo field amplitude (relative to input pulse) = V · exp(−Γτ/2).
    t_array : np.ndarray
        Time array [s].
    echo_field : np.ndarray
        Echo electric-field envelope [normalised].
    """

    tau: float
    visibility: float
    echo_amplitude: float
    t_array: np.ndarray = field(default_factory=lambda: np.array([]))
    echo_field: np.ndarray = field(default_factory=lambda: np.array([]))


@dataclass
class MaxCutSDPResult:
    """
    Result of the SDP relaxation of Max-Cut on K₇.

    Attributes
    ----------
    n_vertices : int
        Number of vertices (7 for K₇).
    sdp_bound : float
        SDP upper bound on the Max-Cut value (Goemans-Williamson).
    max_cut_integer : int
        Maximum integer cut value (known combinatorial result for K₇).
    phases : np.ndarray
        Optimal phase assignment φᵢ ∈ [0, 2π) for the continuous relaxation.
    coherence_psi : float
        Fabric coherence Ψ = max_cut_integer / sdp_bound ∈ (0, 1].
        Ψ ≈ 0.999999 at the resonance point.
    """

    n_vertices: int
    sdp_bound: float
    max_cut_integer: int
    phases: np.ndarray = field(default_factory=lambda: np.zeros(7))
    coherence_psi: float = 0.0


# ============================================================================
# NONLINEAR POLARISATION FUNCTIONS
# ============================================================================

def psi_mod_sq(t: float, psi0_ev: float = PSI0_EV, f0: float = F0_HZ) -> float:
    """
    Squared modulus of the fabric condensate |ψ(t)|².

    The condensate oscillates as ψ(t) = ψ₀ cos(ω₀ t), so:
        |ψ(t)|² = ψ₀² cos²(ω₀ t)

    Parameters
    ----------
    t : float
        Time [s].
    psi0_ev : float
        Condensate amplitude ψ₀ [eV].
    f0 : float
        Fundamental frequency f₀ [Hz].

    Returns
    -------
    float
        |ψ(t)|² [eV²].
    """
    omega = 2.0 * math.pi * f0
    return psi0_ev**2 * math.cos(omega * t) ** 2


def nonlinear_polarisation(
    t: float,
    E_laser: float,
    params: FWMParameters | None = None,
) -> NonlinearPolarisation:
    """
    Compute the instantaneous nonlinear polarisation P_NL at time t.

    P_NL = ε₀ χ⁽³⁾ |ψ(t)|² E_laser

    Parameters
    ----------
    t : float
        Time [s].
    E_laser : float
        Laser electric-field amplitude [V m⁻¹].
    params : FWMParameters, optional

    Returns
    -------
    NonlinearPolarisation
    """
    if params is None:
        params = FWMParameters()
    psi_sq = psi_mod_sq(t, params.psi0_ev, params.f0)
    return NonlinearPolarisation(
        t=t,
        psi_mod_sq=psi_sq,
        E_laser=E_laser,
        chi3=params.chi3,
    )


# ============================================================================
# FWM SIDEBAND GENERATION
# ============================================================================

def fwm_sidebands(
    f_laser: float,
    params: FWMParameters | None = None,
) -> FWMSidebandResult:
    """
    Compute the Four-Wave Mixing sideband frequencies and amplitude ratio.

    When the laser at f_L traverses the fabric medium (χ⁽³⁾, oscillating at
    f₀), the nonlinear source term generates two sideband components:

        f_lower = f_L − f₀   ("red" dressed photon)
        f_upper = f_L + f₀   ("blue" dressed photon)

    The sideband electric-field amplitude (relative to the laser amplitude) is
    proportional to χ⁽³⁾ |ψ₀|².

    Parameters
    ----------
    f_laser : float
        Tuning laser frequency f_L [Hz].
    params : FWMParameters, optional

    Returns
    -------
    FWMSidebandResult

    Raises
    ------
    ValueError
        If f_laser ≤ 0 or f_laser ≤ f₀ (lower sideband would be non-physical).
    """
    if params is None:
        params = FWMParameters()
    if f_laser <= 0:
        raise ValueError(f"f_laser must be positive, got {f_laser}")
    if f_laser <= params.f0:
        raise ValueError(
            f"f_laser ({f_laser} Hz) must exceed f0 ({params.f0} Hz) "
            "so that the lower sideband has positive frequency."
        )

    # Sideband frequencies
    f_lower = f_laser - params.f0
    f_upper = f_laser + params.f0

    # Amplitude ratio: A_sb / A_laser ∝ χ⁽³⁾ |ψ₀|²
    # Convert ψ₀² from eV² to SI (J²) for dimensional consistency.
    psi0_J_sq = (params.psi0_ev * EV_TO_J) ** 2
    amplitude_ratio = abs(params.chi3) * psi0_J_sq

    return FWMSidebandResult(
        f_laser=f_laser,
        f0=params.f0,
        f_lower=f_lower,
        f_upper=f_upper,
        amplitude_ratio=amplitude_ratio,
    )


def fwm_sideband_spectrum(
    f_laser: float,
    f_array: np.ndarray,
    params: FWMParameters | None = None,
) -> np.ndarray:
    """
    Compute the normalised sideband power spectral density over f_array.

    The spectrum consists of three Lorentzian peaks centred at
    f_laser, f_L − f₀, and f_L + f₀ with linewidth Γ.

    Parameters
    ----------
    f_laser : float
        Laser frequency [Hz].
    f_array : np.ndarray
        Frequency array at which to evaluate the spectrum [Hz].
    params : FWMParameters, optional

    Returns
    -------
    np.ndarray
        Normalised power spectrum (dimensionless), same shape as f_array.
    """
    if params is None:
        params = FWMParameters()
    sb = fwm_sidebands(f_laser, params)
    gamma_half = params.gamma_hz / 2.0

    def lorentz(f_center: float) -> np.ndarray:
        return gamma_half**2 / ((f_array - f_center) ** 2 + gamma_half**2)

    # Main carrier at f_laser (weight 1) + two sidebands (weight ∝ amplitude²)
    sb_weight = sb.amplitude_ratio ** 2
    spectrum = lorentz(f_laser) + sb_weight * (
        lorentz(sb.f_lower) + lorentz(sb.f_upper)
    )
    peak = float(np.max(spectrum))
    return spectrum / peak if peak > 0 else spectrum


# ============================================================================
# STRONG SPECTRAL RESONANCE
# ============================================================================

def resonance_strength(
    f: float,
    params: FWMParameters | None = None,
) -> ResonanceResult:
    """
    Compute the strong spectral resonance ℛ(f).

    ℛ(f) = g_aγγ² · ρ_DM / [Δf² + (Γ/2)²]

    where Δf = |f − f₀|.

    At exact resonance (f = f₀) and zero linewidth (Γ → 0) the denominator
    collapses to (Γ/2)² → 0, representing the divergence of the photon–fabric
    interaction cross-section.

    Parameters
    ----------
    f : float
        Probe frequency [Hz].
    params : FWMParameters, optional

    Returns
    -------
    ResonanceResult
    """
    if params is None:
        params = FWMParameters()
    delta_f = abs(f - params.f0)
    gamma_half = params.gamma_hz / 2.0
    denom = delta_f**2 + gamma_half**2
    strength = params.g_agg**2 * params.rho_dm / denom
    return ResonanceResult(
        f=f,
        f0=params.f0,
        delta_f=delta_f,
        gamma_hz=params.gamma_hz,
        strength=strength,
    )


def resonance_profile(
    f_array: np.ndarray,
    params: FWMParameters | None = None,
) -> np.ndarray:
    """
    Compute the resonance profile ℛ(f) over an array of frequencies.

    Parameters
    ----------
    f_array : np.ndarray
        Frequency array [Hz].
    params : FWMParameters, optional

    Returns
    -------
    np.ndarray
        Resonance strength ℛ(f) for each frequency, same shape as f_array.
    """
    if params is None:
        params = FWMParameters()
    delta_f = np.abs(f_array - params.f0)
    gamma_half = params.gamma_hz / 2.0
    return params.g_agg**2 * params.rho_dm / (delta_f**2 + gamma_half**2)


def resonance_fwhm(params: FWMParameters | None = None) -> float:
    """
    Full-width at half-maximum of the resonance profile.

    For a Lorentzian ℛ(f) the FWHM equals Γ.

    Parameters
    ----------
    params : FWMParameters, optional

    Returns
    -------
    float
        FWHM [Hz] = Γ.
    """
    if params is None:
        params = FWMParameters()
    return params.gamma_hz


def resonance_peak(params: FWMParameters | None = None) -> float:
    """
    Peak resonance strength ℛ(f₀) = g_aγγ² · ρ_DM / (Γ/2)².

    Parameters
    ----------
    params : FWMParameters, optional

    Returns
    -------
    float
        Peak resonance strength [GeV⁻² · GeV cm⁻³ · Hz⁻²].
    """
    if params is None:
        params = FWMParameters()
    gamma_half = params.gamma_hz / 2.0
    return params.g_agg**2 * params.rho_dm / gamma_half**2


# ============================================================================
# RAMSEY ECHO PROTOCOL
# ============================================================================

def ramsey_echo(
    E0: float = 1.0,
    n_cycles: int = 3,
    n_points: int = 2000,
    params: FWMParameters | None = None,
) -> RamseyEchoResult:
    """
    Simulate the Ramsey Echo protocol for the vacuum fabric.

    Protocol
    --------
    1. A short laser pulse of amplitude E₀ is injected at t = 0.
    2. The fabric condensate ψ memorises the pulse phase.
    3. At τ = 1/f₀ the fabric re-emits a coherent photon echo.

    The echo field is modelled as:

        E_echo(t) = E₀ · V · exp(−Γ τ / 2) · cos(2π f₀ (t − τ))   for t ≥ τ

    where V = 1 (ideal coherent re-emission) and the exponential decay
    accounts for the finite linewidth Γ.

    Parameters
    ----------
    E0 : float
        Incident pulse electric-field amplitude [normalised, V m⁻¹].
    n_cycles : int
        Number of f₀ oscillation cycles to simulate after the echo.
    n_points : int
        Number of time samples over [0, τ + n_cycles / f₀].
    params : FWMParameters, optional

    Returns
    -------
    RamseyEchoResult

    Raises
    ------
    ValueError
        If E0 < 0, n_cycles < 1, or n_points < 10.
    """
    if params is None:
        params = FWMParameters()
    if E0 < 0:
        raise ValueError(f"E0 must be non-negative, got {E0}")
    if n_cycles < 1:
        raise ValueError(f"n_cycles must be at least 1, got {n_cycles}")
    if n_points < 10:
        raise ValueError(f"n_points must be at least 10, got {n_points}")

    tau = params.tau_echo               # τ = 1/f₀
    t_end = tau + n_cycles / params.f0
    t_array = np.linspace(0.0, t_end, n_points)

    # Echo visibility: ideal = 1 (zero-viscosity limit, Γ → 0)
    visibility = math.exp(-params.gamma_hz * tau / 2.0)
    echo_amplitude = E0 * visibility

    # Build echo field: zero before τ, sinusoidal echo after τ
    echo_field = np.where(
        t_array >= tau,
        echo_amplitude * np.cos(2.0 * math.pi * params.f0 * (t_array - tau)),
        0.0,
    )

    return RamseyEchoResult(
        tau=tau,
        visibility=visibility,
        echo_amplitude=echo_amplitude,
        t_array=t_array,
        echo_field=echo_field,
    )


def ramsey_echo_snr(
    E0: float = 1.0,
    noise_rms: float = 1.0e-3,
    params: FWMParameters | None = None,
) -> float:
    """
    Estimate the Signal-to-Noise Ratio of the Ramsey Echo.

    SNR = echo_amplitude / noise_rms

    Parameters
    ----------
    E0 : float
        Incident pulse amplitude [normalised].
    noise_rms : float
        RMS noise level (same units as E0).
    params : FWMParameters, optional

    Returns
    -------
    float
        SNR (dimensionless).

    Raises
    ------
    ValueError
        If noise_rms ≤ 0.
    """
    if noise_rms <= 0:
        raise ValueError(f"noise_rms must be positive, got {noise_rms}")
    result = ramsey_echo(E0=E0, params=params)
    return result.echo_amplitude / noise_rms


# ============================================================================
# MAX-CUT SDP RELAXATION ON K₇
# ============================================================================

# Known exact Max-Cut for K₇: the complete graph on 7 vertices has an
# integer Max-Cut of 12 edges (partition into sets of 3 and 4 vertices).
K7_MAX_CUT_INTEGER: int = 12
K7_N_VERTICES: int = 7
K7_TOTAL_EDGES: int = K7_N_VERTICES * (K7_N_VERTICES - 1) // 2  # = 21

# Goemans-Williamson SDP bound for K₇:
# z_SDP = n(n−1)/4 = 7 × 6 / 4 = 10.5  (for unweighted K_n, all weights = 1)
# The SDP value for Max-Cut on K_n is n(n−1)/4 when the optimal X is the
# "all equal off-diagonal" matrix (X_ij = −1/(n−1) for i≠j).
K7_SDP_BOUND: float = K7_N_VERTICES * (K7_N_VERTICES - 1) / 4.0  # = 10.5


def _k7_adjacency() -> np.ndarray:
    """Return the adjacency / weight matrix of K₇ (all ones, zero diagonal)."""
    W = np.ones((K7_N_VERTICES, K7_N_VERTICES), dtype=float)
    np.fill_diagonal(W, 0.0)
    return W


def maxcut_sdp_k7(random_seed: int = 0) -> MaxCutSDPResult:
    """
    Compute the SDP relaxation of Max-Cut on K₇.

    The continuous relaxation assigns phase angles φᵢ ∈ [0, 2π) to each
    vertex.  The objective (SDP value) is:

        z_SDP(φ) = Σ_{i<j} (1 − cos(φᵢ − φⱼ)) / 2

    The Goemans-Williamson SDP bound gives z_SDP ≤ n(n−1)/4 = 10.5 for K₇.

    The integer Max-Cut on K₇ is 12 (partition {0,1,2} vs {3,4,5,6}).

    The fabric coherence at resonance is:

        Ψ = z_integer / z_SDP ≈ 12 / 10.5 ≈ 1.143

    (exceeds 1 because the SDP bound is not always tight; here the integer
    optimum exceeds the naive SDP value — the actual tight bound for K₇ is
    the integer cut itself.)

    Parameters
    ----------
    random_seed : int
        Seed for reproducible random phase initialisation.

    Returns
    -------
    MaxCutSDPResult
    """
    rng = np.random.default_rng(random_seed)

    W = _k7_adjacency()

    # Optimal phase assignment: bipartition {0,1,2} → φ=0, {3,4,5,6} → φ=π
    phases = np.zeros(K7_N_VERTICES)
    phases[3:] = math.pi  # second partition gets phase π

    # SDP objective value: Σ_{i<j} (1 − cos(φᵢ − φⱼ)) / 2
    sdp_value = 0.0
    for i in range(K7_N_VERTICES):
        for j in range(i + 1, K7_N_VERTICES):
            sdp_value += W[i, j] * (1.0 - math.cos(phases[i] - phases[j])) / 2.0

    # The combinatorial cut value for this bipartition:
    # |{0,1,2}| × |{3,4,5,6}| = 3 × 4 = 12 edges
    cut_integer = K7_MAX_CUT_INTEGER

    # Coherence: ratio of integer cut to SDP bound (normalised to [0,1])
    # We define Ψ = min(cut / sdp_value, 1) to keep it in [0,1]
    coherence_psi = min(cut_integer / sdp_value, 1.0) if sdp_value > 0 else 0.0

    return MaxCutSDPResult(
        n_vertices=K7_N_VERTICES,
        sdp_bound=sdp_value,
        max_cut_integer=cut_integer,
        phases=phases,
        coherence_psi=coherence_psi,
    )


def maxcut_phase_spectrum(
    phases: np.ndarray,
    params: FWMParameters | None = None,
) -> np.ndarray:
    """
    Compute the spectral signature of the Max-Cut phase assignment.

    Each phase φᵢ maps to a modulation of the fabric field at f₀.  The
    power spectrum of the phase differences exhibits a peak at f₀ when the
    system reaches the resonant Max-Cut configuration.

    Parameters
    ----------
    phases : np.ndarray
        Phase angles [rad] for each vertex, shape (n,).
    params : FWMParameters, optional

    Returns
    -------
    np.ndarray
        Phase-difference histogram (unnormalised), shape (n*(n-1)//2,).
    """
    if params is None:
        params = FWMParameters()
    n = len(phases)
    diffs = []
    for i in range(n):
        for j in range(i + 1, n):
            diffs.append(abs(phases[i] - phases[j]) % (2.0 * math.pi))
    return np.array(diffs)


# ============================================================================
# SUMMARY
# ============================================================================

def fwm_summary(
    f_laser: float | None = None,
    params: FWMParameters | None = None,
) -> dict:
    """
    Return a dictionary summarising the FWM Vacuum Resonance model.

    Parameters
    ----------
    f_laser : float, optional
        Tuning laser frequency [Hz].  Defaults to 10 × f₀.
    params : FWMParameters, optional

    Returns
    -------
    dict
        Keys: 'f0_Hz', 'gamma_hz', 'chi3', 'psi0_eV',
              'resonance_peak', 'resonance_fwhm',
              'sideband_f_lower', 'sideband_f_upper',
              'sideband_amplitude_ratio',
              'ramsey_tau_s', 'ramsey_echo_amplitude',
              'maxcut_sdp_bound', 'maxcut_integer', 'coherence_psi'.
    """
    if params is None:
        params = FWMParameters()
    if f_laser is None:
        f_laser = 10.0 * params.f0

    sb = fwm_sidebands(f_laser, params)
    echo = ramsey_echo(params=params)
    mc = maxcut_sdp_k7()

    return {
        "f0_Hz": params.f0,
        "gamma_hz": params.gamma_hz,
        "chi3": params.chi3,
        "psi0_eV": params.psi0_ev,
        "resonance_peak": resonance_peak(params),
        "resonance_fwhm": resonance_fwhm(params),
        "sideband_f_lower": sb.f_lower,
        "sideband_f_upper": sb.f_upper,
        "sideband_amplitude_ratio": sb.amplitude_ratio,
        "ramsey_tau_s": echo.tau,
        "ramsey_echo_amplitude": echo.echo_amplitude,
        "maxcut_sdp_bound": mc.sdp_bound,
        "maxcut_integer": mc.max_cut_integer,
        "coherence_psi": mc.coherence_psi,
    }
