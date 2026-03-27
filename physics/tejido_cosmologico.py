r"""
Tejido Cosmológico: From Frequency to Energy
=============================================

Translates the fundamental frequency f₀ = 141.7001 Hz to the language of
rest energy and derives key cosmological properties of the quantum fabric (ψ-field).

Physical Framework:
-------------------
I. Fabric Mass (De la Frecuencia a la Energía):
   m_ψ = h·f₀ / c²  ≈  5.86 × 10⁻¹³ eV/c²

   Cosmological context (dark matter mass regimes):
   - Ultra-light   < 10⁻²²  eV: small-scale structure conflicts ❌
   - Light   10⁻²² – 10⁻¹⁰  eV: boson dark matter ✅
   - m_ψ falls in the optimal light-boson dark matter window.

II. Swampland Coupling (Tensión Superficial):
   λ ≈ m_ψ / M_P  ≈  4.8 × 10⁻⁴¹
   λ ~ 10⁻⁴¹  →  guaranteed superfluidity
   λ > 0        →  repulsive at high density (prevents singularities)
   λ ≪ 1        →  valid effective field theory (quantum corrections controlled)

III. Experimental Verification:
   A. Self-interaction (Bullet Cluster):
      σ/m = λ² ℏ² / (16π m_ψ² c)  ≪  1 cm²/g   (observational limit)
      The fabric is practically transparent to itself — perfect superfluid.

   B. Black Hole Superradiance:
      Superradiance occurs when ω < ω_sr = Ω_H (for azimuthal mode m=1).
      Optimal BH mass: M_opt = ℏ c / (G m_ψ) ≈ 228 M_sun (IMBH regime).
      Gravitational fine-structure: α = G M m_ψ / (ℏ c)  ~  O(1) at M_opt.

References:
-----------
- Swampland Distance Conjecture: Ooguri & Vafa (2006)
- Ultralight dark matter: Hui et al. (2017)
- Superradiance: Arvanitaki & Dubovsky (2011)
- f₀ = 141.7001 Hz (QCAL fundamental frequency)

Author: José Manuel Mota Burruezo
License: MIT
"""

import math
from dataclasses import dataclass
from typing import Dict

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.constants import (
    F0_HZ,
    H_PLANCK,
    HBAR,
    C,
    EV_TO_J,
    M_PLANCK_KG,
    M_QCAL_KG,
    M_QCAL_EV_C2,
)

# ---------------------------------------------------------------------------
# Physical constants used internally
# ---------------------------------------------------------------------------
_G = 6.67430e-11          # m³ kg⁻¹ s⁻² - Newton constant
_M_SUN_KG = 1.98892e30   # kg - Solar mass
_CM2_PER_M2 = 1e4        # 1 m² = 10⁴ cm²
_G_PER_KG = 1e3          # 1 kg = 10³ g
_M2_KG_TO_CM2_G = _CM2_PER_M2 / _G_PER_KG  # 10 (m²/kg) → (cm²/g)

# Bullet Cluster observational upper limit on DM self-interaction
BULLET_CLUSTER_LIMIT_CM2_G = 1.0   # cm²/g

# Dark-matter mass regime boundaries (eV/c²)
DM_ULTRALIGHT_MAX_EV = 1e-22
DM_LIGHT_MAX_EV = 1e-10
DM_INTERMEDIATE_MAX_EV = 1e2


# ---------------------------------------------------------------------------
# Section I: Fabric mass from frequency
# ---------------------------------------------------------------------------

def masa_tejido_kg() -> float:
    """Return the fabric particle mass m_ψ = h·f₀/c² in kilograms.

    Returns
    -------
    float
        m_ψ in kg  (~1.04 × 10⁻⁴⁸ kg).
    """
    return M_QCAL_KG


def masa_tejido_eV() -> float:
    """Return the fabric particle mass m_ψ = h·f₀/c² in eV/c².

    Returns
    -------
    float
        m_ψ in eV/c²  (~5.86 × 10⁻¹³ eV/c²).
    """
    return M_QCAL_EV_C2


def energia_tejido_J() -> float:
    """Return the fabric quantum energy E_ψ = h·f₀ in joules.

    Returns
    -------
    float
        E_ψ in J  (~9.39 × 10⁻³² J).
    """
    return H_PLANCK * F0_HZ


def energia_tejido_eV() -> float:
    """Return the fabric quantum energy E_ψ = h·f₀ in electronvolts.

    Returns
    -------
    float
        E_ψ in eV  (~5.86 × 10⁻¹³ eV).
    """
    return energia_tejido_J() / EV_TO_J


def regimen_materia_oscura() -> str:
    """Return the dark-matter mass regime that m_ψ falls into.

    Returns
    -------
    str
        One of 'ultra-ligero', 'ligero', 'intermedio', 'pesado'.
    """
    m_eV = masa_tejido_eV()
    if m_eV < DM_ULTRALIGHT_MAX_EV:
        return "ultra-ligero"
    if m_eV < DM_LIGHT_MAX_EV:
        return "ligero"
    if m_eV < DM_INTERMEDIATE_MAX_EV:
        return "intermedio"
    return "pesado"


# ---------------------------------------------------------------------------
# Section II: Swampland coupling constant λ
# ---------------------------------------------------------------------------

def acoplamiento_swampland() -> float:
    """Compute the Swampland coupling λ = m_ψ / M_P.

    Derived from the Swampland Distance Conjecture: in quantum gravity,
    only scalar fields satisfying specific coupling bounds are consistent.
    λ sets the self-interaction strength of the ψ-field.

    Returns
    -------
    float
        λ (dimensionless)  (~4.8 × 10⁻⁴¹).
    """
    return M_QCAL_KG / M_PLANCK_KG


# ---------------------------------------------------------------------------
# Section III-A: Dark-matter self-interaction
# ---------------------------------------------------------------------------

def seccion_eficaz_autointeraccion() -> float:
    """Compute the DM self-interaction cross section σ in m².

    Uses the low-energy scalar self-interaction formula:
        σ = λ² ℏ² / (16π m_ψ² c)

    This is the leading-order s-wave cross section for a massive scalar
    with dimensionless coupling λ, valid when the de Broglie wavelength
    is much larger than the Compton wavelength (non-relativistic limit).

    Returns
    -------
    float
        σ in m².
    """
    lam = acoplamiento_swampland()
    m = M_QCAL_KG
    return (lam ** 2 * HBAR ** 2) / (16.0 * math.pi * m ** 2 * C)


def sigma_sobre_masa_cm2_g() -> float:
    """Compute the DM self-interaction ratio σ/m in cm²/g.

    Comparing with the Bullet Cluster observational upper limit of
    σ/m < 1 cm²/g provides the tightest constraint on DM self-interaction.

    Returns
    -------
    float
        σ/m in cm²/g.
    """
    sigma = seccion_eficaz_autointeraccion()
    m = M_QCAL_KG
    return (sigma / m) * _M2_KG_TO_CM2_G


def margen_bullet_cluster() -> float:
    """Return the ratio (Bullet Cluster limit) / (predicted σ/m).

    A value >> 1 means the prediction is safely below the observational
    constraint (i.e., the fabric is consistent with dark-matter observations).

    Returns
    -------
    float
        BULLET_CLUSTER_LIMIT_CM2_G / sigma_sobre_masa_cm2_g().
    """
    sm = sigma_sobre_masa_cm2_g()
    if sm == 0.0:
        return float("inf")
    return BULLET_CLUSTER_LIMIT_CM2_G / sm


# ---------------------------------------------------------------------------
# Section III-B: Black-hole superradiance
# ---------------------------------------------------------------------------

def masa_bh_optima_kg() -> float:
    """Return the optimal BH mass for superradiant growth of the ψ-field.

    The condition α = G·M·m_ψ/(ℏ·c) ≈ 1 maximises the superradiance rate.
    Solving for M gives M_opt = ℏ·c / (G·m_ψ).

    Returns
    -------
    float
        M_opt in kg  (~4.5 × 10³² kg ≈ 228 M_sun).
    """
    return (HBAR * C) / (_G * M_QCAL_KG)


def masa_bh_optima_masas_solares() -> float:
    """Return the optimal BH mass for superradiance in solar masses.

    Returns
    -------
    float
        M_opt in M_sun  (~228 M_sun — intermediate-mass BH regime).
    """
    return masa_bh_optima_kg() / _M_SUN_KG


def parametro_alfa_gravitacional(mass_bh_kg: float) -> float:
    """Compute the gravitational fine-structure parameter α.

    α = G · M_BH · m_ψ / (ℏ · c)

    Superradiance is efficient when α ~ O(1).  For α ≪ 1 the wave is
    nearly free; for α ≫ 1 the wave is tightly bound and growth is slow.

    Parameters
    ----------
    mass_bh_kg : float
        Black-hole mass in kilograms.

    Returns
    -------
    float
        α (dimensionless).
    """
    if mass_bh_kg <= 0:
        raise ValueError("mass_bh_kg must be positive")
    return (_G * mass_bh_kg * M_QCAL_KG) / (HBAR * C)


def frecuencia_compton_tejido() -> float:
    """Return the Compton frequency of the fabric particle: ω_C = m_ψ c²/ℏ.

    For superradiance the mode frequency ω must satisfy ω < ω_C (sub-Compton).

    Returns
    -------
    float
        ω_C in rad/s.
    """
    return (M_QCAL_KG * C ** 2) / HBAR


def condicion_superradiancia(omega: float, omega_horizon: float,
                              modo_azimutal: int = 1) -> bool:
    """Check whether a mode satisfies the superradiance condition.

    A mode with frequency ω and azimuthal number m is superradiant when:
        ω < m · Ω_H   (Zel'dovich-Misner condition)

    Parameters
    ----------
    omega : float
        Mode angular frequency in rad/s.
    omega_horizon : float
        Angular velocity of the BH horizon Ω_H in rad/s.
    modo_azimutal : int, optional
        Azimuthal quantum number m (default 1).

    Returns
    -------
    bool
        True if the mode is in the superradiant regime.
    """
    if modo_azimutal < 1:
        raise ValueError("modo_azimutal must be >= 1")
    return omega < modo_azimutal * omega_horizon


# ---------------------------------------------------------------------------
# Summary dataclass
# ---------------------------------------------------------------------------

@dataclass
class TejidoCosmologico:
    """Container for all cosmological fabric parameters derived from f₀.

    Attributes
    ----------
    f0_hz : float
        Fundamental frequency in Hz.
    masa_kg : float
        Fabric particle mass m_ψ in kg.
    masa_eV : float
        Fabric particle mass m_ψ in eV/c².
    energia_eV : float
        Fabric quantum energy h·f₀ in eV.
    regimen_dm : str
        Dark-matter mass regime classification.
    lambda_swampland : float
        Swampland coupling constant λ (dimensionless).
    sigma_sobre_masa_cm2_g : float
        Self-interaction σ/m in cm²/g.
    margen_bullet_cluster : float
        Safety margin relative to Bullet Cluster limit (>> 1 is good).
    masa_bh_optima_msun : float
        Optimal BH mass for superradiance in M_sun.
    alpha_bh_optimo : float
        Gravitational fine-structure α at optimal BH mass (~1).
    omega_compton_rad_s : float
        Compton frequency of the fabric particle in rad/s.
    """

    f0_hz: float
    masa_kg: float
    masa_eV: float
    energia_eV: float
    regimen_dm: str
    lambda_swampland: float
    sigma_sobre_masa_cm2_g: float
    margen_bullet_cluster: float
    masa_bh_optima_msun: float
    alpha_bh_optimo: float
    omega_compton_rad_s: float


def calcular_tejido() -> TejidoCosmologico:
    """Compute all cosmological fabric parameters and return a summary object.

    Returns
    -------
    TejidoCosmologico
        Dataclass with m_ψ, λ, σ/m, superradiance parameters, etc.
    """
    m_bh_opt_kg = masa_bh_optima_kg()
    return TejidoCosmologico(
        f0_hz=F0_HZ,
        masa_kg=masa_tejido_kg(),
        masa_eV=masa_tejido_eV(),
        energia_eV=energia_tejido_eV(),
        regimen_dm=regimen_materia_oscura(),
        lambda_swampland=acoplamiento_swampland(),
        sigma_sobre_masa_cm2_g=sigma_sobre_masa_cm2_g(),
        margen_bullet_cluster=margen_bullet_cluster(),
        masa_bh_optima_msun=masa_bh_optima_masas_solares(),
        alpha_bh_optimo=parametro_alfa_gravitacional(m_bh_opt_kg),
        omega_compton_rad_s=frecuencia_compton_tejido(),
    )


def resumen_tejido() -> Dict[str, str]:
    """Return a human-readable summary of the cosmological fabric parameters.

    Returns
    -------
    Dict[str, str]
        Dictionary with formatted strings for each key parameter.
    """
    t = calcular_tejido()
    return {
        "f₀":             f"{t.f0_hz} Hz",
        "m_ψ (kg)":       f"{t.masa_kg:.4e} kg",
        "m_ψ (eV/c²)":   f"{t.masa_eV:.4e} eV/c²",
        "E_ψ (eV)":       f"{t.energia_eV:.4e} eV",
        "Régimen DM":     t.regimen_dm,
        "λ (Swampland)":  f"{t.lambda_swampland:.4e}",
        "σ/m":            f"{t.sigma_sobre_masa_cm2_g:.4e} cm²/g",
        "Margen Bullet":  f"{t.margen_bullet_cluster:.2e}× por debajo del límite",
        "M_BH óptima":    f"{t.masa_bh_optima_msun:.1f} M_sun",
        "α_grav óptimo":  f"{t.alpha_bh_optimo:.4f}",
        "ω_Compton":      f"{t.omega_compton_rad_s:.4e} rad/s",
    }
