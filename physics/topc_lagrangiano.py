#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lagrangiano del Sistema TOPC acoplado al Electromagnetismo
===========================================================
Derivación de la Señal Medible — Birrefringencia Oscilatoria
inducida por el campo escalar ψ sobre un haz láser coherente

Frecuencia Base:          f₀ = 141.7001 Hz  (Amor Irreversible A²)
Frecuencia Manifestación: f₈₈₈ = 888 Hz    (∞³ Coherencia Final)
Sello:                    ∴TOPC∞³
RAM:                      RAM-XLII-2026-TOPC-LAGRANGIANO

Lagrangiano
-----------
El campo escalar complejo ψ representa el condensado del tejido piloto
coherente acoplado al electromagnetismo en un fondo gravitatorio g_μν::

    ℒ = √(−g) [ R/(16πG)
              + ½ ∂_μψ* ∂^μψ − (½ m_ψ² |ψ|² + λ/4 |ψ|⁴)   [ℒ_tejido]
              − ¼ F_μν F^μν                                   [ℒ_EM]
              − (g_aγγ/4) Re(ψ) F_μν F̃^μν ]                 [ℒ_int]

Parámetros Derivados
--------------------
    m_ψ  = h f₀ / c²  ≈ 5.86 × 10⁻¹³ eV    (Masa de Resonancia)
    λ    ≈ m_ψ / M_P  ≈ 4.8 × 10⁻⁴¹         (Auto-interacción)
    g_aγγ ≈ α/(2π f_a)                       (Acoplamiento Fotónico)

Observable Principal — Birrefringencia Oscilatoria
--------------------------------------------------
La oscilación del campo ψ a f₀ induce rotación de polarización en un haz
láser coherente que recorre la distancia L::

    Δθ(t) ≈ [½ g_aγγ ψ₀ ω₀ L] · sin(2π f₀ t)

con una banda lateral Doppler sidérea en Δf_sid ≈ 10⁻³ f₀.
Para L = 100 km y ρ_DM = 0.3 GeV cm⁻³ la amplitud es ~10⁻¹⁹ rad.

Clases
------
  ConstantesTopc       → constantes físicas del sistema TOPC
  LagrangianoTopc      → componentes ℒ_tejido, ℒ_EM, ℒ_int
  CampoEscalarPsi      → condensado ψ(t) = ψ₀ cos(2πf₀t)
  EcuacionFoton        → Maxwell modificado por ℒ_int
  BirrefringenciaCircular → índices n_L/R y Δn = n_L − n_R
  DesfasePolarizacion  → observable Δθ(t), amplitud ∼10⁻¹⁹ rad
  CoherenciaTopc       → calcula Ψ_global del sistema
  SistemaTopc          → orquestador principal

API pública
-----------
  topc_lagrangiano_activar() → resultado completo

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto Consciencia Cuántica QCAL ∞³
Fecha: 2026-03
RAM: RAM-XLII-2026-TOPC-LAGRANGIANO
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

# ============================================================================
# CONSTANTES — importadas desde SSOT qcal.constants
# ============================================================================

try:
    from qcal.constants import F0_HZ, HBAR, C, F888_HZ
except ImportError:  # pragma: no cover
    # Fallback defensivo para entornos donde qcal no está instalado.
    # Los valores reproducen exactamente las constantes de qcal/constants.py
    # para garantizar coherencia con el resto del framework QCAL ∞³.
    F0_HZ: float = 141.7001
    HBAR: float = 1.054571817e-34
    C: float = 299792458.0
    F888_HZ: float = 888.0

# ============================================================================
# CONSTANTES FÍSICAS DERIVADAS (CODATA 2018)
# ============================================================================

# Constante de Newton
G_NEWTON: float = 6.67430e-11        # m³ kg⁻¹ s⁻² — Constante de Newton

# Constante de Planck
H_PLANCK: float = 6.62607015e-34     # J·s  — Constante de Planck

# Factor de conversión electronvoltio → julio
EV_A_J: float = 1.602176634e-19      # J eV⁻¹

# Masa de Planck: M_P = √(ℏ c / G)
M_PLANCK_KG: float = math.sqrt(HBAR * C / G_NEWTON)   # ≈ 2.176×10⁻⁸ kg

# Constante de estructura fina (adimensional)
ALFA_EM: float = 1.0 / 137.035999084

# Densidad de materia oscura local (valor astrofísico estándar)
RHO_DM_GEV_CM3: float = 0.3          # GeV cm⁻³
RHO_DM_SI: float = (
    RHO_DM_GEV_CM3
    * 1.0e9 * EV_A_J   # GeV → J
    / (1.0e-2) ** 3    # cm⁻³ → m⁻³
    / C**2             # J m⁻³ → kg m⁻³  (ρ = u/c²)
)  # ≈ 5.35×10⁻²⁶ kg m⁻³

# Masa de resonancia del campo ψ: m_ψ = h f₀ / c²
M_PSI_KG: float = H_PLANCK * F0_HZ / C**2    # ≈ 1.046×10⁻⁴⁸ kg
M_PSI_EV: float = M_PSI_KG * C**2 / EV_A_J   # ≈ 5.86×10⁻¹³ eV

# Acoplamiento de auto-interacción: λ ≈ m_ψ / M_P
LAMBDA_SELF: float = M_PSI_KG / M_PLANCK_KG   # ≈ 4.8×10⁻⁴¹

# Constante de decaimiento axiónica por defecto — escala GUT (≈ 6.3×10¹⁵ GeV).
# Este valor produce g_aγγ ≈ 1.84×10⁻¹⁹ GeV⁻¹ y reproduce la amplitud
# de rotación de polarización esperada ~10⁻¹⁹ rad para L = 100 km.
F_A_EV: float = 6.32e24              # eV  (≈ 6.3×10¹⁵ GeV, escala GUT)

# Acoplamiento fotónico: g_aγγ ≈ α / (2π f_a)  con f_a en GeV
G_AGG: float = ALFA_EM / (2.0 * math.pi * F_A_EV * 1.0e-9)   # GeV⁻¹

# Amplitud del campo ψ₀ desde la densidad DM en unidades eV
_OMEGA_PSI: float = 2.0 * math.pi * F0_HZ            # rad s⁻¹
PSI0_EV: float = math.sqrt(
    2.0 * RHO_DM_GEV_CM3 * 1.0e9    # GeV cm⁻³ → eV cm⁻³
    / (5.06773e4) ** 3               # cm⁻³ → (eV)³  (1 cm⁻¹ = 5.068×10⁴ eV)
) / M_PSI_EV

# Frecuencia angular del campo ψ
OMEGA_0: float = 2.0 * math.pi * F0_HZ               # rad s⁻¹  (≈ 890.3 rad s⁻¹)

# Fracción de modulación Doppler sidérea: Δf_sid / f₀ ≈ 10⁻³
FRACCION_DOPPLER_SIDEREO: float = 1.0e-3
PERIODO_SIDEREO_S: float = 86164.1                    # s (día sidéreo)

# Longitud de brazo de referencia del interferómetro
L_REF_M: float = 100.0e3             # 100 km

# Amplitud de señal esperada para L = L_REF con g_aγγ por defecto
AMPLITUD_ESPERADA_RAD: float = 1.0e-19               # rad

# Sello de coherencia TOPC
SELLO_TOPC: str = "∴TOPC∞³"
RAM_TOPC: str = "RAM-XLII-2026-TOPC-LAGRANGIANO"


# ============================================================================
# CLASE 1 — ConstantesTopc
# ============================================================================

@dataclass
class ConstantesTopc:
    """
    Constantes físicas del sistema TOPC.

    Agrupa todas las constantes derivadas del Lagrangiano TOPC y proporciona
    métodos de validación y resumen.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental f₀ [Hz]. Por defecto F0_HZ = 141.7001 Hz.
    f888 : float
        Frecuencia de manifestación [Hz]. Por defecto F888_HZ = 888 Hz.
    rho_dm : float
        Densidad local de materia oscura ρ_DM [GeV cm⁻³]. Por defecto 0.3.
    f_a_ev : float
        Constante de decaimiento axiónica f_a [eV]. Por defecto F_A_EV.
    L_m : float
        Longitud de brazo del interferómetro L [m]. Por defecto 100 km.
    """

    f0: float = field(default_factory=lambda: F0_HZ)
    f888: float = field(default_factory=lambda: F888_HZ)
    rho_dm: float = RHO_DM_GEV_CM3
    f_a_ev: float = field(default_factory=lambda: F_A_EV)
    L_m: float = L_REF_M

    def __post_init__(self) -> None:
        if self.f0 <= 0:
            raise ValueError(f"f0 debe ser positivo, se recibió {self.f0}")
        if self.f888 <= 0:
            raise ValueError(f"f888 debe ser positivo, se recibió {self.f888}")
        if self.rho_dm <= 0:
            raise ValueError(f"rho_dm debe ser positivo, se recibió {self.rho_dm}")
        if self.f_a_ev <= 0:
            raise ValueError(f"f_a_ev debe ser positivo, se recibió {self.f_a_ev}")
        if self.L_m <= 0:
            raise ValueError(f"L_m debe ser positivo, se recibió {self.L_m}")

    # ------------------------------------------------------------------
    # Propiedades derivadas
    # ------------------------------------------------------------------

    @property
    def omega0(self) -> float:
        """ω₀ = 2π f₀  [rad s⁻¹]."""
        return 2.0 * math.pi * self.f0

    @property
    def m_psi_ev(self) -> float:
        """Masa de resonancia m_ψ = h f₀ / c²  [eV]."""
        return H_PLANCK * self.f0 / C**2 * C**2 / EV_A_J

    @property
    def lambda_self(self) -> float:
        """Acoplamiento de auto-interacción λ ≈ m_ψ / M_P (adimensional)."""
        m_psi_kg = H_PLANCK * self.f0 / C**2
        return m_psi_kg / M_PLANCK_KG

    @property
    def g_agg(self) -> float:
        """Constante de acoplamiento fotónico g_aγγ ≈ α/(2π f_a)  [GeV⁻¹]."""
        return ALFA_EM / (2.0 * math.pi * self.f_a_ev * 1.0e-9)

    @property
    def psi0_ev(self) -> float:
        """Amplitud del campo ψ₀ derivada de ρ_DM  [eV]."""
        rho_ev4_nat = (
            self.rho_dm * 1.0e9       # GeV cm⁻³ → eV cm⁻³
            / (5.06773e4) ** 3        # cm⁻³ → eV³ (ℏ=c=1)
        )
        return math.sqrt(2.0 * rho_ev4_nat) / self.m_psi_ev

    def resumen(self) -> Dict[str, Any]:
        """Devuelve un diccionario con las constantes principales del sistema."""
        return {
            "f0_Hz": self.f0,
            "f888_Hz": self.f888,
            "omega0_rad_s": self.omega0,
            "m_psi_eV": self.m_psi_ev,
            "lambda_self": self.lambda_self,
            "g_agg_GeV-1": self.g_agg,
            "psi0_eV": self.psi0_ev,
            "rho_dm_GeV_cm3": self.rho_dm,
            "L_m": self.L_m,
            "sello": SELLO_TOPC,
            "ram": RAM_TOPC,
        }


# ============================================================================
# CLASE 2 — LagrangianoTopc
# ============================================================================

@dataclass
class LagrangianoTopc:
    """
    Componentes del Lagrangiano TOPC.

    Calcula las densidades lagrangianas individuales::

        ℒ_gravedad = R / (16π G)
        ℒ_tejido   = ½ |∂ψ|² − ½ m_ψ² |ψ|² − λ/4 |ψ|⁴
        ℒ_EM       = −¼ F_μν F^μν
        ℒ_int      = −(g_aγγ/4) Re(ψ) F_μν F̃^μν

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def densidad_gravedad(self, R_escalar: float = 0.0) -> float:
        """
        Densidad lagrangiana gravitatoria.

            ℒ_gravedad = R / (16π G)

        Parámetros
        ----------
        R_escalar : float
            Escalar de curvatura de Ricci R [m⁻²]. Cero en espacio plano.

        Devuelve
        --------
        float
            ℒ_gravedad  [m⁻² / (m³ kg⁻¹ s⁻²)] en unidades SI.
        """
        return R_escalar / (16.0 * math.pi * G_NEWTON)

    def densidad_tejido(
        self,
        psi_re: float,
        psi_im: float,
        dpsi_dt: float,
        dpsi_dz: float = 0.0,
    ) -> float:
        """
        Densidad lagrangiana del tejido ψ::

            ℒ_tejido = ½ (∂_t ψ)² − ½ (∂_z ψ)²
                     − ½ ω₀² |ψ|² − λ/4 |ψ|⁴

        Trabajando con ψ en eV y t en segundos: la masa del campo ψ aparece
        como ω₀² (con ω₀ = m_ψ c²/ℏ en rad s⁻¹), de modo que el término de
        masa −½ ω₀² |ψ|² tiene las mismas unidades que el término cinético
        ½ (∂_t ψ)², ambos en eV² s⁻².

        Parámetros
        ----------
        psi_re : float
            Re(ψ)  [eV].
        psi_im : float
            Im(ψ)  [eV].
        dpsi_dt : float
            ∂_t ψ  [eV s⁻¹].
        dpsi_dz : float
            ∂_z ψ  [eV m⁻¹]. Cero para ψ uniforme espacialmente.

        Devuelve
        --------
        float
            ℒ_tejido  [eV² s⁻²].
        """
        mod_sq = psi_re**2 + psi_im**2                         # |ψ|²  [eV²]
        lam = self.constantes.lambda_self                      # adimensional
        omega0 = self.constantes.omega0                        # rad s⁻¹

        cinetico = 0.5 * dpsi_dt**2 - 0.5 * dpsi_dz**2        # [eV² s⁻²]
        # masa: −½ ω₀² |ψ|²  con ω₀² en s⁻²  →  [eV² s⁻²]
        potencial = -(0.5 * omega0**2 * mod_sq + lam / 4.0 * mod_sq**2)
        return cinetico + potencial

    def densidad_em(self, E_sq: float = 0.0, B_sq: float = 0.0) -> float:
        """
        Densidad lagrangiana electromagnética::

            ℒ_EM = −¼ F_μν F^μν = ½ (E² − c² B²) / c²

        Parámetros
        ----------
        E_sq : float
            |E|²  [V² m⁻²].
        B_sq : float
            |B|²  [T²].

        Devuelve
        --------
        float
            ℒ_EM  [J m⁻³].
        """
        epsilon0 = 8.8541878128e-12   # F m⁻¹
        return 0.5 * epsilon0 * (E_sq - C**2 * B_sq)

    def densidad_interaccion(
        self,
        psi_re: float,
        F_dual: float = 0.0,
    ) -> float:
        """
        Densidad lagrangiana de interacción axión-fotón::

            ℒ_int = −(g_aγγ/4) Re(ψ) F_μν F̃^μν

        Parámetros
        ----------
        psi_re : float
            Re(ψ)  [eV].
        F_dual : float
            F_μν F̃^μν = 4 E·B / c²  [T² = kg² A⁻² s⁻⁴].

        Devuelve
        --------
        float
            ℒ_int  [eV · GeV⁻¹ · T²].
        """
        g_agg_inv_eV = self.constantes.g_agg * 1.0e-9   # GeV⁻¹ → eV⁻¹
        return -(g_agg_inv_eV / 4.0) * psi_re * F_dual

    def densidad_total(
        self,
        psi_re: float,
        psi_im: float,
        dpsi_dt: float,
        R_escalar: float = 0.0,
        E_sq: float = 0.0,
        B_sq: float = 0.0,
        F_dual: float = 0.0,
    ) -> float:
        """
        Densidad lagrangiana total::

            ℒ = ℒ_gravedad + ℒ_tejido + ℒ_EM + ℒ_int

        Devuelve
        --------
        float
            Suma de componentes (unidades mixtas; útil para verificación de signo).
        """
        return (
            self.densidad_gravedad(R_escalar)
            + self.densidad_tejido(psi_re, psi_im, dpsi_dt)
            + self.densidad_em(E_sq, B_sq)
            + self.densidad_interaccion(psi_re, F_dual)
        )


# ============================================================================
# CLASE 3 — CampoEscalarPsi
# ============================================================================

@dataclass
class CampoEscalarPsi:
    """
    Condensado del campo escalar ψ(t) = ψ₀ cos(2π f₀ t).

    El campo ψ representa el tejido piloto coherente en el fondo TOPC.
    Oscila armónicamente con la frecuencia fundamental f₀.

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def psi(self, t: float) -> float:
        """
        Valor del campo en el tiempo t.

            ψ(t) = ψ₀ cos(2π f₀ t)

        Parámetros
        ----------
        t : float
            Tiempo  [s].

        Devuelve
        --------
        float
            Re(ψ(t))  [eV].
        """
        return self.constantes.psi0_ev * math.cos(2.0 * math.pi * self.constantes.f0 * t)

    def dpsi_dt(self, t: float) -> float:
        """
        Derivada temporal del campo.

            ∂_t ψ(t) = −ψ₀ ω₀ sin(2π f₀ t)

        Parámetros
        ----------
        t : float
            Tiempo  [s].

        Devuelve
        --------
        float
            ∂_t ψ(t)  [eV s⁻¹].
        """
        omega0 = self.constantes.omega0
        return -self.constantes.psi0_ev * omega0 * math.sin(omega0 * t)

    def energia_cinetica(self, t: float) -> float:
        """
        Energía cinética ½ (∂_t ψ)²  [eV² s⁻²].
        """
        dpsi = self.dpsi_dt(t)
        return 0.5 * dpsi**2

    def energia_potencial(self, t: float) -> float:
        """
        Energía potencial ½ ω₀² ψ²  [eV² s⁻²].

        En la aproximación armónica m_ψ → ω₀/c² · eV.
        """
        omega0 = self.constantes.omega0
        psi_val = self.psi(t)
        return 0.5 * omega0**2 * psi_val**2

    def energia_total(self, t: float) -> float:
        """
        Energía total E = E_cin + E_pot  [eV² s⁻²].  Debe ser constante (harmónica).
        """
        return self.energia_cinetica(t) + self.energia_potencial(t)

    def serie_temporal(self, t_array: np.ndarray) -> np.ndarray:
        """
        Devuelve ψ(t) evaluado en t_array  [eV].
        """
        omega0 = self.constantes.omega0
        return self.constantes.psi0_ev * np.cos(omega0 * t_array)

    def derivada_temporal_serie(self, t_array: np.ndarray) -> np.ndarray:
        """
        Devuelve ∂_t ψ(t) evaluado en t_array  [eV s⁻¹].
        """
        omega0 = self.constantes.omega0
        return -self.constantes.psi0_ev * omega0 * np.sin(omega0 * t_array)


# ============================================================================
# CLASE 4 — EcuacionFoton
# ============================================================================

@dataclass
class EcuacionFoton:
    """
    Ecuaciones de Maxwell modificadas por el término de interacción ℒ_int.

    De ℒ_int, la modificación de las ecuaciones de Maxwell para un haz
    propagándose en la dirección z::

        (∂_t² − ∂_z²) E ≈ −g_aγγ ψ̇ (∇ × E)

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def fuente_maxwell(self, dpsi_dt: float, curl_E: float) -> float:
        """
        Término fuente en las ecuaciones de Maxwell modificadas.

            fuente = −g_aγγ [eV⁻¹] × ψ̇ [eV s⁻¹] × (∇ × E)

        Parámetros
        ----------
        dpsi_dt : float
            ∂_t ψ  [eV s⁻¹].
        curl_E : float
            (∇ × E)  [V m⁻²].

        Devuelve
        --------
        float
            Término fuente de Maxwell  [V m⁻² s⁻¹].
        """
        g_agg_inv_eV = self.constantes.g_agg * 1.0e-9   # GeV⁻¹ → eV⁻¹
        return -g_agg_inv_eV * dpsi_dt * curl_E

    def verificar_dispersion(self, omega_foton: float, k_foton: float) -> float:
        """
        Verifica la relación de dispersión modificada.

        En el vacío (sin ℒ_int): ω² = c² k².
        Con ℒ_int aparece una pequeña corrección proporcional a g_aγγ ψ̇.

        Devuelve
        --------
        float
            Desviación (ω² − c² k²) / ω²  (adimensional).
        """
        return (omega_foton**2 - (C * k_foton) ** 2) / max(omega_foton**2, 1.0e-300)


# ============================================================================
# CLASE 5 — BirrefringenciaCircular
# ============================================================================

@dataclass
class BirrefringenciaCircular:
    """
    Birrefringencia circular inducida por el campo ψ.

    El acoplamiento ℒ_int rompe la simetría entre modos de polarización
    circular L y R, dando lugar a índices de refracción distintos::

        n_{L/R} ≈ 1 ± g_aγγ ψ̇ / (2ω)

    La diferencia Δn = n_L − n_R es el efecto de birrefringencia.

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def indices_refraccion(
        self,
        dpsi_dt: float,
        omega_foton: float,
    ) -> tuple[float, float]:
        """
        Índices de refracción para modos L y R.

            n_L = 1 + g_aγγ ψ̇ / (2ω)
            n_R = 1 − g_aγγ ψ̇ / (2ω)

        Parámetros
        ----------
        dpsi_dt : float
            ∂_t ψ  [eV s⁻¹].
        omega_foton : float
            Frecuencia angular del fotón ω  [rad s⁻¹].

        Devuelve
        --------
        tuple[float, float]
            (n_L, n_R).
        """
        g_agg_inv_eV = self.constantes.g_agg * 1.0e-9   # GeV⁻¹ → eV⁻¹
        delta_n = g_agg_inv_eV * dpsi_dt / (2.0 * max(omega_foton, 1.0e-300))
        return 1.0 + delta_n, 1.0 - delta_n

    def diferencia_indices(
        self,
        dpsi_dt: float,
        omega_foton: float,
    ) -> float:
        """
        Diferencia de índices Δn = n_L − n_R.

            Δn = g_aγγ ψ̇ / ω

        Parámetros
        ----------
        dpsi_dt : float
            ∂_t ψ  [eV s⁻¹].
        omega_foton : float
            Frecuencia angular del fotón ω  [rad s⁻¹].

        Devuelve
        --------
        float
            Δn (adimensional).
        """
        n_L, n_R = self.indices_refraccion(dpsi_dt, omega_foton)
        return n_L - n_R

    def longitud_coherencia(self, omega_foton: float) -> float:
        """
        Longitud de coherencia del efecto: L_coh = c / (Δn · ω).

        Parámetros
        ----------
        omega_foton : float
            Frecuencia angular del fotón ω  [rad s⁻¹].

        Devuelve
        --------
        float
            L_coh  [m].
        """
        campo = CampoEscalarPsi(self.constantes)
        dpsi_max = self.constantes.psi0_ev * self.constantes.omega0
        dn = self.diferencia_indices(dpsi_max, omega_foton)
        if abs(dn) < 1.0e-300:
            return math.inf
        return C / (abs(dn) * max(omega_foton, 1.0e-300))


# ============================================================================
# CLASE 6 — DesfasePolarizacion
# ============================================================================

@dataclass
class DesfasePolarizacion:
    """
    Observable: desfase de polarización Δθ(t).

    Un haz linealmente polarizado experimenta una rotación al atravesar
    la distancia L::

        Δθ(t) = ½ g_aγγ ∫₀ᴸ ∂_t ψ(z,t) dz

    Para ψ(t) = ψ₀ cos(2π f₀ t) (campo uniforme):

        Δθ(t) ≈ [½ g_aγγ ψ₀ ω₀ L] · sin(2π f₀ t)

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def amplitud(self, L: Optional[float] = None) -> float:
        """
        Amplitud del desfase de polarización.

            Δθ_amp = ½ g_aγγ [eV⁻¹] × ψ₀ [eV] × ω₀ [rad s⁻¹] × L [m] / c [m s⁻¹]

        Parámetros
        ----------
        L : float, optional
            Longitud de brazo  [m]. Si es None, usa constantes.L_m.

        Devuelve
        --------
        float
            Amplitud Δθ_amp  [rad].
        """
        if L is None:
            L = self.constantes.L_m
        g_agg_inv_eV = self.constantes.g_agg * 1.0e-9   # GeV⁻¹ → eV⁻¹
        psi0 = self.constantes.psi0_ev
        omega0 = self.constantes.omega0
        return 0.5 * g_agg_inv_eV * psi0 * omega0 * L / C

    def desfase(self, t: float, L: Optional[float] = None) -> float:
        """
        Desfase de polarización en el tiempo t.

            Δθ(t) = Δθ_amp · sin(2π f₀ t)

        Parámetros
        ----------
        t : float
            Tiempo  [s].
        L : float, optional
            Longitud de brazo  [m].

        Devuelve
        --------
        float
            Δθ(t)  [rad].
        """
        amp = self.amplitud(L)
        return amp * math.sin(2.0 * math.pi * self.constantes.f0 * t)

    def desfase_con_doppler(
        self,
        t: float,
        L: Optional[float] = None,
        fraccion_doppler: float = FRACCION_DOPPLER_SIDEREO,
        periodo_sidereo: float = PERIODO_SIDEREO_S,
    ) -> float:
        """
        Desfase con modulación Doppler sidérea.

        La velocidad del campo ψ relativa a la Tierra varía con el día
        sidéreo, produciendo una modulación de frecuencia::

            f(t) = f₀ · [1 + Δ · cos(2π t / T_sid)]

        Parámetros
        ----------
        t : float
            Tiempo  [s].
        L : float, optional
            Longitud de brazo  [m].
        fraccion_doppler : float
            Amplitud fraccional Doppler Δf / f₀.
        periodo_sidereo : float
            Período sidéreo  [s].

        Devuelve
        --------
        float
            Δθ(t) incluyendo modulación Doppler  [rad].
        """
        amp = self.amplitud(L)
        freq_mod = self.constantes.f0 * (
            1.0 + fraccion_doppler * math.cos(2.0 * math.pi * t / periodo_sidereo)
        )
        return amp * math.sin(2.0 * math.pi * freq_mod * t)

    def serie_temporal(
        self,
        t_array: np.ndarray,
        L: Optional[float] = None,
        incluir_doppler: bool = False,
    ) -> np.ndarray:
        """
        Serie temporal Δθ(t) sobre t_array  [rad].

        Parámetros
        ----------
        t_array : np.ndarray
            Muestras de tiempo  [s].
        L : float, optional
            Longitud de brazo  [m].
        incluir_doppler : bool
            Si True, incluye la banda lateral Doppler sidérea.

        Devuelve
        --------
        np.ndarray
            Δθ(t)  [rad], misma forma que t_array.
        """
        amp = self.amplitud(L)
        omega0 = self.constantes.omega0
        if incluir_doppler:
            freq_mod = self.constantes.f0 * (
                1.0
                + FRACCION_DOPPLER_SIDEREO
                * np.cos(2.0 * np.pi * t_array / PERIODO_SIDEREO_S)
            )
            return amp * np.sin(2.0 * np.pi * freq_mod * t_array)
        return amp * np.sin(omega0 * t_array)


# ============================================================================
# CLASE 7 — CoherenciaTopc
# ============================================================================

@dataclass
class CoherenciaTopc:
    """
    Coherencia global del sistema TOPC.

    Calcula el parámetro de coherencia Ψ_global que mide la sincronización
    entre la frecuencia fundamental f₀ y la frecuencia de manifestación f₈₈₈::

        Ψ_global = cos²(π · |f₀ - f₈₈₈/n| / f₀)

    donde n = round(f₈₈₈ / f₀) es el harmónico más cercano de f₀ a f₈₈₈.

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    @property
    def harmonico_888(self) -> int:
        """Harmónico entero más cercano de f₀ a f₈₈₈."""
        return round(self.constantes.f888 / self.constantes.f0)

    @property
    def psi_global(self) -> float:
        """
        Parámetro de coherencia global Ψ_global ∈ [0, 1].

            Ψ_global = cos²(π · δf / f₀)

        donde δf = |f₀ - f₈₈₈ / n| es la desviación respecto al harmónico.
        """
        n = self.harmonico_888
        f_arm = self.constantes.f888 / n if n > 0 else self.constantes.f888
        delta_f = abs(self.constantes.f0 - f_arm)
        arg = math.pi * delta_f / self.constantes.f0
        return math.cos(arg) ** 2

    @property
    def coherencia_sello(self) -> str:
        """Cadena de sello de coherencia TOPC."""
        return SELLO_TOPC

    def evaluar_coherencia(self) -> Dict[str, Any]:
        """
        Evaluación completa de la coherencia del sistema.

        Devuelve
        --------
        dict
            Claves: 'f0_Hz', 'f888_Hz', 'harmonico', 'f_harmonico_Hz',
                    'delta_f_Hz', 'psi_global', 'coherente', 'sello'.
        """
        n = self.harmonico_888
        f_arm = self.constantes.f888 / n if n > 0 else self.constantes.f888
        delta_f = abs(self.constantes.f0 - f_arm)
        psi = self.psi_global
        return {
            "f0_Hz": self.constantes.f0,
            "f888_Hz": self.constantes.f888,
            "harmonico": n,
            "f_harmonico_Hz": f_arm,
            "delta_f_Hz": delta_f,
            "psi_global": psi,
            "coherente": psi >= 0.5,
            "sello": SELLO_TOPC,
        }


# ============================================================================
# CLASE 8 — SistemaTopc
# ============================================================================

@dataclass
class SistemaTopc:
    """
    Orquestador principal del sistema TOPC.

    Coordina todos los subsistemas (campo, Lagrangiano, birrefringencia,
    señal observable y coherencia global) y produce el resultado integrado.

    Parámetros
    ----------
    constantes : ConstantesTopc
        Constantes físicas del sistema TOPC.
    """

    constantes: ConstantesTopc = field(default_factory=ConstantesTopc)

    def __post_init__(self) -> None:
        self._lagrangiano = LagrangianoTopc(self.constantes)
        self._campo = CampoEscalarPsi(self.constantes)
        self._foton = EcuacionFoton(self.constantes)
        self._birrefringencia = BirrefringenciaCircular(self.constantes)
        self._desfase = DesfasePolarizacion(self.constantes)
        self._coherencia = CoherenciaTopc(self.constantes)

    # ------------------------------------------------------------------
    # Acceso a subsistemas
    # ------------------------------------------------------------------

    @property
    def lagrangiano(self) -> LagrangianoTopc:
        """Componentes del Lagrangiano TOPC."""
        return self._lagrangiano

    @property
    def campo(self) -> CampoEscalarPsi:
        """Campo escalar ψ(t)."""
        return self._campo

    @property
    def foton(self) -> EcuacionFoton:
        """Ecuaciones de Maxwell modificadas."""
        return self._foton

    @property
    def birrefringencia(self) -> BirrefringenciaCircular:
        """Birrefringencia circular n_L/R."""
        return self._birrefringencia

    @property
    def desfase(self) -> DesfasePolarizacion:
        """Observable Δθ(t)."""
        return self._desfase

    @property
    def coherencia(self) -> CoherenciaTopc:
        """Coherencia global Ψ_global."""
        return self._coherencia

    # ------------------------------------------------------------------
    # Métodos de alto nivel
    # ------------------------------------------------------------------

    def calcular_estado(self, t: float) -> Dict[str, Any]:
        """
        Calcula el estado completo del sistema TOPC en el tiempo t.

        Parámetros
        ----------
        t : float
            Tiempo  [s].

        Devuelve
        --------
        dict
            Estado completo: campo ψ, Lagrangiano, birrefringencia, señal.
        """
        psi_val = self._campo.psi(t)
        dpsi = self._campo.dpsi_dt(t)
        amp_señal = self._desfase.amplitud()
        delta_theta = self._desfase.desfase(t)

        # Índices de refracción para láser verde (532 nm)
        omega_laser = 2.0 * math.pi * C / 532.0e-9
        n_L, n_R = self._birrefringencia.indices_refraccion(dpsi, omega_laser)

        # Densidades lagrangianas
        l_tejido = self._lagrangiano.densidad_tejido(psi_val, 0.0, dpsi)
        l_int = self._lagrangiano.densidad_interaccion(psi_val)

        coh = self._coherencia.evaluar_coherencia()

        return {
            "t_s": t,
            "psi_eV": psi_val,
            "dpsi_dt_eV_s": dpsi,
            "L_tejido": l_tejido,
            "L_int": l_int,
            "n_L": n_L,
            "n_R": n_R,
            "delta_n": n_L - n_R,
            "amplitud_delta_theta_rad": amp_señal,
            "delta_theta_rad": delta_theta,
            "psi_global": coh["psi_global"],
            "coherente": coh["coherente"],
            "sello": SELLO_TOPC,
            "ram": RAM_TOPC,
        }

    def activar(self) -> Dict[str, Any]:
        """
        Activación completa del sistema TOPC.

        Produce el resultado integrado evaluado en t = 1 / f₀ (un período).

        Devuelve
        --------
        dict
            Resultado completo del sistema TOPC.
        """
        t_ref = 1.0 / self.constantes.f0     # un período completo
        estado = self.calcular_estado(t_ref)

        # Verificaciones de consistencia física
        amplitud = self._desfase.amplitud()
        orden_magnitud_correcto = 1.0e-21 < amplitud < 1.0e-17

        resultado = {
            **estado,
            "constantes": self.constantes.resumen(),
            "coherencia": self._coherencia.evaluar_coherencia(),
            "amplitud_orden_correcto": orden_magnitud_correcto,
            "f0_Hz": self.constantes.f0,
            "f888_Hz": self.constantes.f888,
            "L_m": self.constantes.L_m,
            "sistema": "TOPC Lagrangiano ∴TOPC∞³",
            "estado": "ACTIVADO",
        }
        return resultado


# ============================================================================
# API PÚBLICA
# ============================================================================

def topc_lagrangiano_activar(
    f0: Optional[float] = None,
    rho_dm: float = RHO_DM_GEV_CM3,
    L_m: float = L_REF_M,
    f_a_ev: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Activa el sistema TOPC Lagrangiano completo.

    Función de API pública que instancia el orquestador ``SistemaTopc``
    con los parámetros dados y devuelve el resultado integrado.

    Parámetros
    ----------
    f0 : float, optional
        Frecuencia fundamental f₀ [Hz]. Por defecto F0_HZ = 141.7001 Hz.
    rho_dm : float
        Densidad local de materia oscura ρ_DM [GeV cm⁻³]. Por defecto 0.3.
    L_m : float
        Longitud de brazo del interferómetro L [m]. Por defecto 100 km.
    f_a_ev : float, optional
        Constante de decaimiento axiónica f_a [eV]. Por defecto F_A_EV (escala GUT).

    Devuelve
    --------
    dict
        Resultado completo del sistema TOPC con todos los observables,
        constantes derivadas y parámetro de coherencia Ψ_global.

    Ejemplo
    -------
    >>> resultado = topc_lagrangiano_activar()
    >>> print(resultado["estado"])
    'ACTIVADO'
    >>> print(resultado["sello"])
    '∴TOPC∞³'
    """
    constantes = ConstantesTopc(
        f0=f0 if f0 is not None else F0_HZ,
        rho_dm=rho_dm,
        L_m=L_m,
        f_a_ev=f_a_ev if f_a_ev is not None else F_A_EV,
    )
    sistema = SistemaTopc(constantes)
    return sistema.activar()
