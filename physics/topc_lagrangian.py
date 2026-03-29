#!/usr/bin/env python3
"""
TOPC Lagrangian — Tejido de Onda Piloto Coherente (Coherent Pilot Wave Fabric)
===============================================================================

Implements the action of the Coherent Pilot Wave Fabric (TOPC) coupled to
electromagnetism in a gravitational background g_μν.  The complex scalar
field ψ represents the fabric condensate.

Lagrangian density (in units with √(−g) factored out):

    ℒ = R / (16πG)
        + ½ ∂_μψ* ∂^μψ  −  (½ m_ψ² |ψ|²  +  λ/4 |ψ|⁴)   [ℒ_fabric]
        −  ¼ F_μν F^μν                                       [ℒ_EM]
        −  (g_aγγ/4) Re(ψ) F_μν F̃^μν                        [ℒ_int]

Derived parameters
------------------
m_ψ  = h f₀ / c²  ≈ 5.86 × 10⁻¹³ eV   (resonance mass)
λ    ≈ m_ψ / M_P  ≈ 4.8 × 10⁻⁴¹        (self-interaction coupling)
g_aγγ ≈ α / (2π f_a)                    (photonic coupling constant)

Primary observable — Oscillatory Birefringence
-----------------------------------------------
The ψ-field oscillation at f₀ induces polarisation rotation in a coherent
laser beam travelling distance L:

    Δθ(t) ≈ ½ g_aγγ ψ₀ ω₀ L · sin(2π f₀ t)

with a sidereal Doppler side-band at Δf_sid ≈ 10⁻³ f₀.

For L = 100 km and local DM density ρ_DM = 0.3 GeV cm⁻³ the amplitude is
~10⁻¹⁹ rad.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-03
Framework: QCAL ∞³
License: Sovereign Noetic License 1.0 (compatible with MIT)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from qcal.constants import F0_HZ, HBAR, C

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

# Physical constants (CODATA 2018)
G_NEWTON: float = 6.67430e-11      # m³ kg⁻¹ s⁻² — Newton's constant
H_PLANCK: float = 6.62607015e-34   # J·s          — Planck constant
EV_TO_J: float  = 1.602176634e-19  # J eV⁻¹       — electron-volt to Joule
M_PLANCK_KG: float = math.sqrt(HBAR * C / G_NEWTON)  # ≈ 2.176×10⁻⁸ kg

# Fine structure constant (dimensionless)
ALPHA_EM: float = 1.0 / 137.035999084

# Local dark-matter density (standard astrophysical value)
RHO_DM_GEV_CM3: float = 0.3        # GeV cm⁻³
RHO_DM_SI: float = (
    RHO_DM_GEV_CM3
    * 1.0e9 * EV_TO_J   # GeV → J
    / (1.0e-2) ** 3      # cm⁻³ → m⁻³
    / C**2               # J/m³ → kg/m³  (ρ = u/c²)
)  # ≈ 5.35×10⁻²⁶ kg m⁻³

# ψ-field resonance mass: m_ψ = h f₀ / c²
M_PSI_KG: float = H_PLANCK * F0_HZ / C**2   # ≈ 1.046×10⁻⁴⁸ kg
M_PSI_EV: float = M_PSI_KG * C**2 / EV_TO_J  # ≈ 5.86×10⁻¹³ eV

# Self-interaction coupling: λ ≈ m_ψ / M_P
LAMBDA_SELF: float = M_PSI_KG / M_PLANCK_KG  # ≈ 4.8×10⁻⁴¹

# Default axion decay constant — GUT scale (≈ 6.3×10¹⁵ GeV = 6.3×10²⁴ eV).
# This value yields g_aγγ ≈ 1.84×10⁻¹⁹ GeV⁻¹ and reproduces the
# expected ~10⁻¹⁹ rad polarisation-rotation amplitude for L = 100 km.
F_A_DEFAULT_EV: float = 6.32e24   # eV  (≈ 6.3×10¹⁵ GeV, GUT scale)

# Photonic coupling constant: g_aγγ ≈ α / (2π f_a)
# f_a in GeV → multiply F_A_DEFAULT_EV by 1e-9
G_AGG_DEFAULT: float = ALPHA_EM / (2.0 * math.pi * F_A_DEFAULT_EV * 1.0e-9)  # GeV⁻¹ → SI later

# ψ₀ from local DM density: ρ_DM = m_ψ² ψ₀² / 2  (non-relativistic condensate)
# ψ₀² = 2 ρ_DM / m_ψ²  [SI:  kg m⁻³ / (kg² s⁻²) ≡ m⁻³ s² / kg = 1/kg·m]
# Keep ψ₀ in units where m_ψ is expressed in kg and ρ in kg m⁻³
_OMEGA_PSI: float = 2.0 * math.pi * F0_HZ    # rad s⁻¹   ω_ψ = 2π f₀
PSI0_SI: float = math.sqrt(2.0 * RHO_DM_SI) / (_OMEGA_PSI * M_PSI_KG / HBAR)
# Equivalent form via Klein-Gordon: ρ = ½ m_ψ² ψ₀² / ℏ²  (natural-unit convention)
# Using ψ in SI-natural units: [ψ] = eV  so ψ₀ = √(2ρ_DM) / m_ψ
PSI0_EV: float = math.sqrt(2.0 * RHO_DM_GEV_CM3 * 1.0e9) / M_PSI_EV  # eV

# Angular frequency of ψ oscillation
OMEGA_0: float = 2.0 * math.pi * F0_HZ   # rad s⁻¹ (≈ 890.3 rad s⁻¹)

# Sidereal Doppler modulation amplitude: Δf_sid / f₀ ≈ 10⁻³
# (Earth orbital + galactic streaming contribution)
SIDEREAL_DOPPLER_FRACTION: float = 1.0e-3   # dimensionless
SIDEREAL_PERIOD_S: float = 86164.1          # s (sidereal day)

# Reference interferometer arm length
L_REF_M: float = 100.0e3  # 100 km

# Expected signal amplitude for L = L_REF with default g_aγγ
# Δθ_amp = ½ g_aγγ ψ₀ ω₀ L  (see below for precise computation)
EXPECTED_AMPLITUDE_RAD: float = 1.0e-19   # rad


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class TOPCParameters:
    """
    Parameters for the TOPC Lagrangian.

    Attributes
    ----------
    f0 : float
        Fundamental frequency f₀ [Hz].  Defaults to F0_HZ = 141.7001 Hz.
    m_psi_ev : float
        ψ-field resonance mass m_ψ [eV].  Defaults to M_PSI_EV.
    lambda_self : float
        Self-interaction coupling λ (dimensionless).
    g_agg : float
        Photon-axion coupling constant g_aγγ [GeV⁻¹].  Defaults to G_AGG_DEFAULT.
    f_a_ev : float
        Axion decay constant f_a [eV].  Defaults to F_A_DEFAULT_EV.
    rho_dm : float
        Local dark-matter density ρ_DM [GeV cm⁻³].  Defaults to 0.3.
    L_m : float
        Interferometer arm length L [m].  Defaults to 100 km.
    """

    f0: float = F0_HZ
    m_psi_ev: float = M_PSI_EV
    lambda_self: float = LAMBDA_SELF
    g_agg: float = G_AGG_DEFAULT          # GeV⁻¹
    f_a_ev: float = F_A_DEFAULT_EV
    rho_dm: float = RHO_DM_GEV_CM3       # GeV cm⁻³
    L_m: float = L_REF_M

    def __post_init__(self) -> None:
        if self.f0 <= 0:
            raise ValueError(f"f0 must be positive, got {self.f0}")
        if self.m_psi_ev <= 0:
            raise ValueError(f"m_psi_ev must be positive, got {self.m_psi_ev}")
        if self.lambda_self < 0:
            raise ValueError(f"lambda_self must be non-negative, got {self.lambda_self}")
        if self.rho_dm <= 0:
            raise ValueError(f"rho_dm must be positive, got {self.rho_dm}")
        if self.L_m <= 0:
            raise ValueError(f"L_m must be positive, got {self.L_m}")

    @property
    def omega0(self) -> float:
        """Angular frequency ω₀ = 2π f₀ [rad s⁻¹]."""
        return 2.0 * math.pi * self.f0

    @property
    def psi0_ev(self) -> float:
        """
        ψ₀ field amplitude [eV] from local DM density.

        ρ_DM = ½ m_ψ² ψ₀²  →  ψ₀ = √(2 ρ_DM) / m_ψ
        (working in natural units eV throughout)
        """
        rho_ev4 = self.rho_dm * 1.0e9         # GeV cm⁻³ → eV cm⁻³
        # convert cm⁻³ to eV³ using (1 cm⁻¹ = 5.068×10⁴ eV in ℏ=c=1)
        cm_to_inv_eV = 5.06773e4              # cm⁻¹ = 5.068×10⁴ eV
        rho_ev4_nat = rho_ev4 / cm_to_inv_eV**3  # eV⁴ in natural units
        return math.sqrt(2.0 * rho_ev4_nat) / self.m_psi_ev  # eV


@dataclass
class FieldState:
    """
    Instantaneous state of the TOPC fabric field ψ at time t.

    The field oscillates as:
        ψ(t) = ψ₀ cos(ω₀ t)   (real part; Im(ψ) carries the conjugate)
    """

    t: float              # s   — coordinate time
    psi_re: float         # eV  — Re(ψ) = ψ₀ cos(ω₀ t)
    psi_im: float = 0.0   # eV  — Im(ψ) = 0 for the coherent condensate
    dpsi_dt: float = 0.0  # eV s⁻¹ — ∂_t ψ (used in signal derivation)

    @property
    def psi_mod_sq(self) -> float:
        """|ψ|² = Re(ψ)² + Im(ψ)²  [eV²]."""
        return self.psi_re**2 + self.psi_im**2


# ============================================================================
# LAGRANGIAN DENSITY COMPONENTS
# ============================================================================

def lagrangian_gravity(
    R: float,
    sqrt_minus_g: float = 1.0,
    G: float = G_NEWTON,
) -> float:
    """
    Einstein-Hilbert Lagrangian density component (gravity sector).

    ℒ_EH = √(−g) · R / (16π G)

    Parameters
    ----------
    R : float
        Ricci scalar curvature [m⁻²].
    sqrt_minus_g : float
        Volume factor √(−g), dimensionless.  1.0 for flat Minkowski.
    G : float
        Newton's gravitational constant [m³ kg⁻¹ s⁻²].

    Returns
    -------
    float
        Einstein-Hilbert Lagrangian density [kg m⁻¹ s⁻²] = [Pa].
    """
    return sqrt_minus_g * R / (16.0 * math.pi * G)


def lagrangian_fabric(
    dpsi_dt: float,
    grad_psi_sq: float,
    psi_mod_sq: float,
    m_psi_ev: float = M_PSI_EV,
    lambda_self: float = LAMBDA_SELF,
    sqrt_minus_g: float = 1.0,
) -> float:
    """
    Fabric (pilot wave condensate) Lagrangian density.

    ℒ_fabric = √(−g) · [½ (∂_t ψ*)( ∂_t ψ) − ½ |∇ψ|²
                        − ½ m_ψ² |ψ|²  −  λ/4 |ψ|⁴]

    Working in natural units where ψ is in eV, time derivatives in eV·s⁻¹, etc.
    The factor ½ on the gradient comes from the Minkowski metric signature (−,+,+,+).

    Parameters
    ----------
    dpsi_dt : float
        Time derivative ∂_t ψ  [eV s⁻¹].
    grad_psi_sq : float
        Squared spatial gradient |∇ψ|²  [eV² m⁻²].
    psi_mod_sq : float
        |ψ|²  [eV²].
    m_psi_ev : float
        Resonance mass m_ψ  [eV].  Angular: m_ψ ω = m_ψ c² / ℏ.
    lambda_self : float
        Self-interaction coupling λ (dimensionless in natural units).
    sqrt_minus_g : float
        Volume factor √(−g).

    Returns
    -------
    float
        Fabric Lagrangian density (natural units, eV⁴).
    """
    kinetic = 0.5 * dpsi_dt**2
    gradient = -0.5 * grad_psi_sq
    mass_term = -0.5 * m_psi_ev**2 * psi_mod_sq
    self_int = -(lambda_self / 4.0) * psi_mod_sq**2
    return sqrt_minus_g * (kinetic + gradient + mass_term + self_int)


def lagrangian_em(
    F_sq: float,
    sqrt_minus_g: float = 1.0,
) -> float:
    """
    Maxwell Lagrangian density.

    ℒ_EM = −√(−g) · ¼ F_μν F^μν

    Parameters
    ----------
    F_sq : float
        Contracted EM field tensor F_μν F^μν  [V² m⁻²] or natural units.
    sqrt_minus_g : float
        Volume factor √(−g).

    Returns
    -------
    float
        EM Lagrangian density (same units as F_sq / 4).
    """
    return -sqrt_minus_g * 0.25 * F_sq


def lagrangian_interaction(
    psi_re: float,
    F_dual: float,
    g_agg: float = G_AGG_DEFAULT,
    sqrt_minus_g: float = 1.0,
) -> float:
    """
    Photon–fabric interaction Lagrangian density (axion-like coupling).

    ℒ_int = −√(−g) · (g_aγγ/4) Re(ψ) F_μν F̃^μν

    The dual F̃^μν = ½ ε^μναβ F_αβ (Levi-Civita contracted).

    Parameters
    ----------
    psi_re : float
        Real part of the fabric field Re(ψ)  [eV].
    F_dual : float
        Chern-Pontryagin density F_μν F̃^μν  [V² m⁻²] or natural units.
    g_agg : float
        Photonic coupling constant g_aγγ  [GeV⁻¹].
    sqrt_minus_g : float
        Volume factor √(−g).

    Returns
    -------
    float
        Interaction Lagrangian density.
    """
    return -sqrt_minus_g * (g_agg / 4.0) * psi_re * F_dual


def lagrangian_total(
    R: float,
    dpsi_dt: float,
    grad_psi_sq: float,
    psi_re: float,
    psi_mod_sq: float,
    F_sq: float,
    F_dual: float,
    params: TOPCParameters | None = None,
    sqrt_minus_g: float = 1.0,
) -> float:
    """
    Full TOPC Lagrangian density.

    ℒ = ℒ_EH + ℒ_fabric + ℒ_EM + ℒ_int

    Parameters
    ----------
    R : float
        Ricci scalar  [m⁻²].
    dpsi_dt : float
        ∂_t ψ  [eV s⁻¹].
    grad_psi_sq : float
        |∇ψ|²  [eV² m⁻²].
    psi_re : float
        Re(ψ)  [eV].
    psi_mod_sq : float
        |ψ|²  [eV²].
    F_sq : float
        F_μν F^μν.
    F_dual : float
        F_μν F̃^μν  (Pontryagin density).
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.
    sqrt_minus_g : float
        Volume factor √(−g).

    Returns
    -------
    float
        Total Lagrangian density.
    """
    if params is None:
        params = TOPCParameters()

    L_eh = lagrangian_gravity(R, sqrt_minus_g)
    L_fab = lagrangian_fabric(
        dpsi_dt, grad_psi_sq, psi_mod_sq,
        m_psi_ev=params.m_psi_ev,
        lambda_self=params.lambda_self,
        sqrt_minus_g=sqrt_minus_g,
    )
    L_em = lagrangian_em(F_sq, sqrt_minus_g)
    L_int = lagrangian_interaction(psi_re, F_dual, g_agg=params.g_agg, sqrt_minus_g=sqrt_minus_g)
    return L_eh + L_fab + L_em + L_int


# ============================================================================
# SIGNAL DERIVATION — OSCILLATORY BIREFRINGENCE
# ============================================================================

def refractive_indices(
    dpsi_dt: float,
    omega_photon: float,
    g_agg: float = G_AGG_DEFAULT,
) -> Tuple[float, float]:
    """
    Circular-polarisation refractive indices induced by the TOPC field.

    The interaction ℒ_int modifies Maxwell equations so that left (L) and
    right (R) circular polarisation modes propagate with distinct indices:

        n_{L/R} ≈ 1 ± g_aγγ ψ̇ / (2 ω)

    Parameters
    ----------
    dpsi_dt : float
        Time derivative ∂_t ψ  (same units as g_agg·ω denominator).
    omega_photon : float
        Angular frequency of the probe laser ω  [rad s⁻¹].
    g_agg : float
        Photonic coupling constant g_aγγ.

    Returns
    -------
    (n_L, n_R) : tuple of float
        Left and right circular refractive indices.
    """
    if omega_photon <= 0:
        raise ValueError(f"omega_photon must be positive, got {omega_photon}")
    delta_n = g_agg * dpsi_dt / (2.0 * omega_photon)
    return 1.0 + delta_n, 1.0 - delta_n


def polarisation_rotation(
    t: float,
    L: float,
    params: TOPCParameters | None = None,
) -> float:
    """
    Polarisation rotation angle Δθ(t) induced by the TOPC condensate.

    For the coherent oscillation ψ(t) = ψ₀ cos(ω₀ t) integrating over
    the interferometer arm length L gives:

        Δθ(t) = ½ g_aγγ ψ₀ ω₀ L · sin(2π f₀ t)

    Parameters
    ----------
    t : float
        Coordinate time  [s].
    L : float
        Interferometer arm length  [m].
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.

    Returns
    -------
    float
        Polarisation rotation Δθ(t)  [rad].
    """
    if params is None:
        params = TOPCParameters()
    amplitude = polarisation_amplitude(L, params)
    return amplitude * math.sin(2.0 * math.pi * params.f0 * t)


def polarisation_amplitude(
    L: float,
    params: TOPCParameters | None = None,
) -> float:
    """
    Peak amplitude of the polarisation rotation signal.

    Δθ_amp = ½ g_aγγ ψ₀ ω₀ L

    Parameters
    ----------
    L : float
        Interferometer arm length  [m].
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.

    Returns
    -------
    float
        Peak amplitude  [rad].
    """
    if params is None:
        params = TOPCParameters()
    # ψ₀ in natural units (eV); g_agg in GeV⁻¹; ω₀ in rad s⁻¹
    # The combination g_agg [GeV⁻¹] × ψ₀ [eV] is dimensionless when
    # g_agg is expressed in eV⁻¹ (factor 1e9 conversion)
    g_agg_inv_eV = params.g_agg * 1.0e-9   # GeV⁻¹ → eV⁻¹
    psi0 = params.psi0_ev                   # eV
    omega0 = params.omega0                  # rad s⁻¹
    # Δθ_amp = ½ g_aγγ [eV⁻¹] · ψ₀ [eV] · ω₀ [rad s⁻¹] · L [m] / c [m s⁻¹]
    # The factor c converts the spatial integral ∫dz to time: L/c is the light-travel time
    return 0.5 * g_agg_inv_eV * psi0 * omega0 * L / C


def polarisation_rotation_with_doppler(
    t: float,
    L: float,
    params: TOPCParameters | None = None,
    doppler_fraction: float = SIDEREAL_DOPPLER_FRACTION,
    sidereal_period: float = SIDEREAL_PERIOD_S,
) -> float:
    """
    Polarisation rotation with sidereal Doppler side-band modulation.

    The TOPC field velocity relative to Earth varies with the sidereal day,
    producing a frequency modulation Δf_sid ≈ doppler_fraction × f₀:

        f(t) = f₀ · [1 + doppler_fraction · cos(2π t / T_sid)]

    This is incorporated as a slowly-varying instantaneous frequency.

    Parameters
    ----------
    t : float
        Coordinate time  [s].
    L : float
        Interferometer arm length  [m].
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.
    doppler_fraction : float
        Fractional Doppler amplitude Δf / f₀.  Defaults to 10⁻³.
    sidereal_period : float
        Sidereal period  [s].  Defaults to 86164.1 s.

    Returns
    -------
    float
        Polarisation rotation Δθ(t) including Doppler modulation  [rad].
    """
    if params is None:
        params = TOPCParameters()
    amplitude = polarisation_amplitude(L, params)
    # Instantaneous frequency modulation
    freq_mod = params.f0 * (
        1.0 + doppler_fraction * math.cos(2.0 * math.pi * t / sidereal_period)
    )
    return amplitude * math.sin(2.0 * math.pi * freq_mod * t)


# ============================================================================
# FABRIC FIELD EVOLUTION
# ============================================================================

def psi_coherent(t: float, psi0: float, f0: float = F0_HZ) -> float:
    """
    Coherent condensate field value at time t.

        ψ(t) = ψ₀ cos(2π f₀ t)

    Parameters
    ----------
    t : float
        Time  [s].
    psi0 : float
        Field amplitude  [eV or any consistent unit].
    f0 : float
        Oscillation frequency  [Hz].

    Returns
    -------
    float
        Re(ψ(t)).
    """
    return psi0 * math.cos(2.0 * math.pi * f0 * t)


def dpsi_coherent_dt(t: float, psi0: float, f0: float = F0_HZ) -> float:
    """
    Time derivative of the coherent condensate.

        ∂_t ψ(t) = −ψ₀ ω₀ sin(2π f₀ t)

    Parameters
    ----------
    t : float
        Time  [s].
    psi0 : float
        Field amplitude (same units as ψ₀).
    f0 : float
        Oscillation frequency  [Hz].

    Returns
    -------
    float
        ∂_t ψ(t).
    """
    omega0 = 2.0 * math.pi * f0
    return -psi0 * omega0 * math.sin(omega0 * t)


def compute_field_state(
    t: float, params: TOPCParameters | None = None
) -> FieldState:
    """
    Compute the TOPC field state at time t.

    Parameters
    ----------
    t : float
        Time  [s].
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.

    Returns
    -------
    FieldState
    """
    if params is None:
        params = TOPCParameters()
    psi0 = params.psi0_ev
    psi_re = psi_coherent(t, psi0, params.f0)
    dpsi_dt = dpsi_coherent_dt(t, psi0, params.f0)
    return FieldState(t=t, psi_re=psi_re, psi_im=0.0, dpsi_dt=dpsi_dt)


# ============================================================================
# SIGNAL TIME SERIES
# ============================================================================

def signal_time_series(
    t_array: np.ndarray,
    L: float,
    params: TOPCParameters | None = None,
    include_doppler: bool = False,
) -> np.ndarray:
    """
    Compute the polarisation rotation time series Δθ(t) over t_array.

    Parameters
    ----------
    t_array : np.ndarray
        Array of time samples  [s].
    L : float
        Interferometer arm length  [m].
    params : TOPCParameters, optional
        Model parameters.  Uses defaults if None.
    include_doppler : bool
        If True, include sidereal Doppler side-band.

    Returns
    -------
    np.ndarray
        Δθ(t)  [rad], same shape as t_array.
    """
    if params is None:
        params = TOPCParameters()
    amplitude = polarisation_amplitude(L, params)
    if include_doppler:
        freq_mod = params.f0 * (
            1.0
            + SIDEREAL_DOPPLER_FRACTION
            * np.cos(2.0 * np.pi * t_array / SIDEREAL_PERIOD_S)
        )
        return amplitude * np.sin(2.0 * np.pi * freq_mod * t_array)
    return amplitude * np.sin(2.0 * np.pi * params.f0 * t_array)


# ============================================================================
# SUMMARY
# ============================================================================

def topc_summary(params: TOPCParameters | None = None) -> dict:
    """
    Return a dictionary summarising TOPC model parameters and predictions.

    Parameters
    ----------
    params : TOPCParameters, optional

    Returns
    -------
    dict
        Keys: 'f0_Hz', 'm_psi_eV', 'lambda_self', 'g_agg_inv_GeV',
              'psi0_eV', 'omega0_rad_s', 'L_m', 'amplitude_rad'.
    """
    if params is None:
        params = TOPCParameters()
    return {
        "f0_Hz": params.f0,
        "m_psi_eV": params.m_psi_ev,
        "lambda_self": params.lambda_self,
        "g_agg_inv_GeV": params.g_agg,
        "psi0_eV": params.psi0_ev,
        "omega0_rad_s": params.omega0,
        "L_m": params.L_m,
        "amplitude_rad": polarisation_amplitude(params.L_m, params),
    }
