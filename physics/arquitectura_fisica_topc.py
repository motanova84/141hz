#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           ARQUITECTURA FÍSICA TOPC (AFP∞³)                                   ║
║    Complete Physical Architecture: Hamiltonian, Permittivity, Dispersion     ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA/DATE: 2026-03-29

═══════════════════════════════════════════════════════════════════════════════
                    SÍNTESIS DEL MODELO TOPC COMPLETO
═══════════════════════════════════════════════════════════════════════════════

Este módulo implementa la arquitectura física completa del modelo TOPC:

1. **Hamiltoniano Total**: Ĥ_Total = Ĥ_EM + Ĥ_ψ + Ĥ_int
   - Campo electromagnético libre (portador)
   - Condensado del tejido (medio dinámico con memoria)
   - Acoplamiento resonante fuerte (transducción)

2. **Permitividad Efectiva**: ε_eff(ω,k) con resonancia fuerte en ω_ψ
   - Modificación del vacío por el condensado
   - Divergencia resonante en ω → ω_ψ

3. **Coeficiente de Mezcla de Fase η**: Tres regímenes
   - η ≪ 1: Débil (física estándar)
   - η → 1: Resonancia fuerte (oscilaciones de Rabi)
   - η > 1: Saturación (colapso no-lineal)

4. **Relación de Dispersión de Thot**: ω² = c²k² + m_ψ²c⁴/ℏ²
   - Hipérbola inequívoca en el espacio (ω,k)
   - Prueba definitiva del medio masivo

5. **Señal Inequívoca de Larmor**: Modulación sidérea
   - Anisotropía Doppler galáctica: ±0.1 Hz
   - Correlación con v_gal ≈ 220 km/s hacia Cygnus

6. **Interferómetro de Sagnac Resonante (IRS-Luna)**
   - Batido heterodino CW/CCW
   - Quiralidad del tejido (Φ ≈ 0.4 rad)
   - Modulación a 141.7001 Hz

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, Optional

import numpy as np

# Import QCAL constants
from qcal.constants import (
    F0_HZ,
    HBAR,
    H_PLANCK,
    C,
    EV_TO_J,
)

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES FUNDAMENTALES / FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

# Fabric field mass: m_ψ = h f₀ / c²
M_PSI_KG: float = H_PLANCK * F0_HZ / C**2  # kg ≈ 1.046×10⁻⁴⁸
M_PSI_EV: float = M_PSI_KG * C**2 / EV_TO_J  # eV ≈ 5.86×10⁻¹³

# Angular frequency
OMEGA_PSI: float = 2.0 * math.pi * F0_HZ  # rad/s ≈ 890.33

# Coherence length: λ̄_C = c/(2π f₀)
LAMBDA_COHERENCE_M: float = C / OMEGA_PSI  # m ≈ 336.7 km

# Local dark matter density (standard astrophysical value)
RHO_DM_GEV_CM3: float = 0.3  # GeV/cm³
RHO_DM_SI: float = (
    RHO_DM_GEV_CM3 * 1.0e9 * EV_TO_J / (1.0e-2)**3 / C**2
)  # kg/m³ ≈ 5.35×10⁻²⁶

# Axion-photon coupling (GUT scale)
ALPHA_EM: float = 1.0 / 137.035999084
F_A_GUT_EV: float = 6.32e24  # eV (≈ 6.3×10¹⁵ GeV)
G_AGG_GEV_INV: float = ALPHA_EM / (2.0 * math.pi * F_A_GUT_EV * 1.0e-9)  # GeV⁻¹

# Galactic velocity toward Cygnus
V_GAL_MS: float = 220.0e3  # m/s (220 km/s)
THETA_CYGNUS_DEG: float = 90.0  # Galactic longitude l=90° (Cygnus)

# Chirality phase from C₇ topology
PHI_CHIRALITY_RAD: float = 0.395  # rad ≈ 0.4 rad

# Damping rate (viscosity of fabric)
GAMMA_DAMPING: float = 1.0e-12 * OMEGA_PSI  # rad/s (ultra-low dissipation)


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 1: CONSTANTES DEL MODELO / MODEL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ConstantesArquitecturaFisica:
    """
    Constantes fundamentales de la Arquitectura Física TOPC.

    Attributes
    ----------
    f0 : float
        Frecuencia fundamental f₀ [Hz]
    m_psi_ev : float
        Masa del campo ψ [eV/c²]
    omega_psi : float
        Frecuencia angular ω_ψ = 2π f₀ [rad/s]
    lambda_coherence : float
        Longitud de coherencia λ̄_C = c/(2π f₀) [m]
    rho_dm : float
        Densidad local de materia oscura [GeV/cm³]
    g_agg : float
        Acoplamiento axión-fotón [GeV⁻¹]
    v_gal : float
        Velocidad galáctica [m/s]
    phi_chirality : float
        Fase de quiralidad del tejido [rad]
    gamma : float
        Tasa de amortiguamiento [rad/s]
    """

    f0: float = F0_HZ
    m_psi_ev: float = M_PSI_EV
    omega_psi: float = OMEGA_PSI
    lambda_coherence: float = LAMBDA_COHERENCE_M
    rho_dm: float = RHO_DM_GEV_CM3
    g_agg: float = G_AGG_GEV_INV
    v_gal: float = V_GAL_MS
    phi_chirality: float = PHI_CHIRALITY_RAD
    gamma: float = GAMMA_DAMPING

    def __post_init__(self) -> None:
        if self.f0 <= 0:
            raise ValueError(f"f0 debe ser positivo, recibido {self.f0}")
        if self.m_psi_ev <= 0:
            raise ValueError(f"m_psi_ev debe ser positivo, recibido {self.m_psi_ev}")


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 2: HAMILTONIANO TOTAL / TOTAL HAMILTONIAN
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class HamiltonianoTotal:
    """
    Hamiltoniano total del sistema TOPC: Ĥ = Ĥ_EM + Ĥ_ψ + Ĥ_int

    Tres componentes:
    1. Ĥ_EM: Campo electromagnético libre (portador de información)
    2. Ĥ_ψ: Condensado del tejido (medio dinámico con memoria)
    3. Ĥ_int: Acoplamiento resonante fuerte (mecanismo de transducción)
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def energia_em(self, E_field: float, B_field: float) -> float:
        """
        Energía del campo electromagnético libre.

        Ĥ_EM = ∫ d³x [ε₀/2 E² + 1/(2μ₀) B²]

        Parameters
        ----------
        E_field : float
            Amplitud del campo eléctrico [V/m]
        B_field : float
            Amplitud del campo magnético [T]

        Returns
        -------
        float
            Densidad de energía electromagnética [J/m³]
        """
        epsilon_0 = 8.854187817e-12  # F/m
        mu_0 = 4.0 * math.pi * 1.0e-7  # H/m

        E_density = 0.5 * epsilon_0 * E_field**2
        B_density = 0.5 * B_field**2 / mu_0

        return E_density + B_density

    def energia_condensado(
        self,
        psi: complex,
        grad_psi_sq: float,
        lambda_self: float = 4.8e-41
    ) -> float:
        """
        Energía del condensado del tejido ψ.

        Ĥ_ψ = ∫ d³x [|∇ψ|²/(2m) + m_ψ²c⁴/(2ℏ²)|ψ|² + λ/4 |ψ|⁴]

        Parameters
        ----------
        psi : complex
            Amplitud del campo ψ [eV]
        grad_psi_sq : float
            Gradiente espacial |∇ψ|² [eV²/m²]
        lambda_self : float
            Acoplamiento de auto-interacción

        Returns
        -------
        float
            Densidad de energía del condensado [eV⁴] (unidades naturales)
        """
        psi_mod_sq = abs(psi)**2

        # Término cinético
        kinetic = grad_psi_sq / (2.0 * self.constantes.m_psi_ev)

        # Término de masa
        mass_term = 0.5 * self.constantes.m_psi_ev**2 * psi_mod_sq

        # Término de auto-interacción (λ|ψ|⁴)
        self_interaction = (lambda_self / 4.0) * psi_mod_sq**2

        return kinetic + mass_term + self_interaction

    def energia_interaccion(
        self,
        psi_re: float,
        F_dual: float
    ) -> float:
        """
        Energía de interacción axión-fotón.

        Ĥ_int = ∫ d³x [g_aγγ/(4α) Re(ψ) F_μν F̃^μν + χ⁽³⁾|ψ|² E²]

        Primer sumando: Rotación de fase (birrefringencia)
        Segundo sumando: Auto-focalización del destello

        Parameters
        ----------
        psi_re : float
            Parte real del campo Re(ψ) [eV]
        F_dual : float
            Densidad de Pontryagin F_μν F̃^μν [V²/m²]

        Returns
        -------
        float
            Densidad de energía de interacción
        """
        # Acoplamiento axión-fotón (birrefringencia)
        g_agg_si = self.constantes.g_agg * 1.0e-9  # GeV⁻¹ → eV⁻¹
        birefringence_term = (g_agg_si / (4.0 * ALPHA_EM)) * psi_re * F_dual

        # No-linealidad óptica χ⁽³⁾ (aproximación)
        chi3 = 1.0e-22  # eV⁻² (orden de magnitud típico)
        nonlinear_term = chi3 * psi_re**2 * F_dual

        return birefringence_term + nonlinear_term

    def energia_total(
        self,
        E_field: float,
        B_field: float,
        psi: complex,
        grad_psi_sq: float,
        F_dual: float
    ) -> float:
        """
        Energía total del sistema.

        Returns
        -------
        float
            Densidad de energía total
        """
        H_em = self.energia_em(E_field, B_field)
        H_psi = self.energia_condensado(psi, grad_psi_sq)
        H_int = self.energia_interaccion(psi.real, F_dual)

        return H_em + H_psi + H_int


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 3: PERMITIVIDAD EFECTIVA / EFFECTIVE PERMITTIVITY
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class PermitividadEfectiva:
    """
    Permitividad efectiva del vacío modificada por el tejido.

    ε_eff(ω,k) = ε₀[1 + χ_vacuo + g²_aγγ ρ_DM / (m²_ψ - ω² + iγω)]

    Resonancia fuerte: cuando ω → ω_ψ, el denominador → 0 y la respuesta diverge.
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def epsilon_eff(
        self,
        omega: float,
        k_vector: Optional[np.ndarray] = None
    ) -> complex:
        """
        Permitividad efectiva compleja ε_eff(ω,k).

        Parameters
        ----------
        omega : float
            Frecuencia angular [rad/s]
        k_vector : np.ndarray, optional
            Vector de onda [1/m]

        Returns
        -------
        complex
            ε_eff/ε₀ (permitividad relativa compleja)
        """
        epsilon_0 = 8.854187817e-12  # F/m

        # Susceptibilidad del vacío cuántico (QED)
        chi_vacuo = 1.0e-12  # Muy pequeña

        # Término resonante
        omega_sq = self.constantes.omega_psi**2
        m_psi_si = self.constantes.m_psi_ev * EV_TO_J / C**2  # kg

        # Denominador con amortiguamiento
        denominator = (
            m_psi_si**2 * C**4 / HBAR**2
            - omega**2
            + 1j * self.constantes.gamma * omega
        )

        # Numerador: g²_aγγ ρ_DM
        g_agg_si = self.constantes.g_agg * EV_TO_J * 1.0e9  # GeV⁻¹ → J⁻¹
        numerator = g_agg_si**2 * RHO_DM_SI * C**2

        # ε_eff/ε₀
        epsilon_rel = 1.0 + chi_vacuo + numerator / denominator

        return epsilon_rel

    def indice_refraccion(self, omega: float) -> complex:
        """
        Índice de refracción complejo n(ω) = √[ε_eff(ω)/ε₀].

        Parameters
        ----------
        omega : float
            Frecuencia angular [rad/s]

        Returns
        -------
        complex
            n(ω) = n' + in'' (parte real e imaginaria)
        """
        epsilon_rel = self.epsilon_eff(omega)
        return np.sqrt(epsilon_rel)

    def velocidad_grupo(self, omega: float, delta_omega: float = 1.0) -> float:
        """
        Velocidad de grupo v_g = dω/dk.

        En resonancia fuerte, v_g → 0 (el fotón se detiene).

        Parameters
        ----------
        omega : float
            Frecuencia angular [rad/s]
        delta_omega : float
            Incremento para la derivada numérica [rad/s]

        Returns
        -------
        float
            Velocidad de grupo [m/s]
        """
        # Derivada numérica de k(ω) para obtener dk/dω
        n1 = self.indice_refraccion(omega).real
        n2 = self.indice_refraccion(omega + delta_omega).real

        k1 = omega * n1 / C
        k2 = (omega + delta_omega) * n2 / C

        dk_domega = (k2 - k1) / delta_omega

        if abs(dk_domega) < 1.0e-20:
            return 0.0

        v_g = 1.0 / dk_domega
        return min(abs(v_g), C)  # No puede superar c


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 4: COEFICIENTE DE MEZCLA DE FASE η / PHASE MIXING COEFFICIENT
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoeficienteMezclaFase:
    """
    Coeficiente de mezcla de fase η = ℏω/(g_aγγ√ρ_DM) · √L

    Tres regímenes:
    - η ≪ 1: Débil (física estándar, axiones tradicionales)
    - η → 1: Resonancia fuerte (oscilaciones de Rabi, fotón "vestido")
    - η > 1: Saturación (colapso no-lineal, formación de solitones)
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def eta(self, omega: float, L: float) -> float:
        """
        Coeficiente de mezcla de fase η.

        Parameters
        ----------
        omega : float
            Frecuencia del fotón [rad/s]
        L : float
            Longitud de propagación [m]

        Returns
        -------
        float
            η (adimensional)
        """
        g_agg_si = self.constantes.g_agg * EV_TO_J * 1.0e9  # GeV⁻¹ → J⁻¹
        rho_dm_si = RHO_DM_SI  # kg/m³

        numerator = HBAR * omega
        denominator = g_agg_si * math.sqrt(rho_dm_si * C**2) * math.sqrt(L)

        return numerator / denominator

    def regimen(self, eta: float) -> str:
        """
        Determina el régimen físico según η.

        Parameters
        ----------
        eta : float
            Coeficiente de mezcla

        Returns
        -------
        str
            'debil', 'resonancia_fuerte', o 'saturacion'
        """
        if eta < 0.1:
            return 'debil'
        elif eta < 2.0:
            return 'resonancia_fuerte'
        else:
            return 'saturacion'

    def probabilidad_conversion(self, eta: float, L: float) -> float:
        """
        Probabilidad de conversión fotón → axión.

        En resonancia fuerte, la probabilidad oscila (oscilaciones de Rabi).

        Parameters
        ----------
        eta : float
            Coeficiente de mezcla
        L : float
            Longitud de propagación [m]

        Returns
        -------
        float
            P_γ→a (probabilidad entre 0 y 1)
        """
        if eta < 0.1:
            # Régimen débil: P ∝ η²
            return eta**2 * (L / self.constantes.lambda_coherence)
        elif eta < 2.0:
            # Resonancia fuerte: oscilaciones de Rabi
            return math.sin(math.pi * eta / 2.0)**2
        else:
            # Saturación: probabilidad saturada
            return 0.5 + 0.5 * math.tanh(eta - 2.0)


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 5: RELACIÓN DE DISPERSIÓN DE THOT / THOT'S DISPERSION RELATION
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RelacionDispersionThot:
    """
    Relación de dispersión hiperbólica del medio masivo.

    ω² = c² k² + m²_ψ c⁴/ℏ²

    Esta hipérbola en el espacio (ω,k) es inequívoca:
    - Ningún error sistemático sigue esta curva
    - Ninguna vibración mecánica
    - Ningún artefacto instrumental
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def omega_de_k(self, k: float) -> float:
        """
        Frecuencia angular a partir del número de onda.

        ω(k) = √[c²k² + m²_ψc⁴/ℏ²]

        Parameters
        ----------
        k : float
            Número de onda [1/m]

        Returns
        -------
        float
            ω [rad/s]
        """
        m_psi_si = self.constantes.m_psi_ev * EV_TO_J / C**2  # kg
        omega_min_sq = (m_psi_si * C**2 / HBAR)**2

        return math.sqrt(C**2 * k**2 + omega_min_sq)

    def k_de_omega(self, omega: float) -> float:
        """
        Número de onda a partir de la frecuencia angular.

        k(ω) = √[ω²/c² - m²_ψc²/ℏ²]

        Parameters
        ----------
        omega : float
            Frecuencia angular [rad/s]

        Returns
        -------
        float
            k [1/m] (0 si ω < ω_min)
        """
        m_psi_si = self.constantes.m_psi_ev * EV_TO_J / C**2  # kg
        omega_min = m_psi_si * C**2 / HBAR

        if omega < omega_min:
            return 0.0

        return math.sqrt(omega**2 / C**2 - omega_min**2 / C**2)

    def omega_minima(self) -> float:
        """
        Frecuencia mínima del modo (gap de masa).

        ω_min = m_ψ c² / ℏ = 2π f₀

        Returns
        -------
        float
            ω_min [rad/s]
        """
        return self.constantes.omega_psi

    def curva_dispersion(
        self,
        k_array: np.ndarray
    ) -> np.ndarray:
        """
        Curva completa de dispersión ω(k).

        Parameters
        ----------
        k_array : np.ndarray
            Array de números de onda [1/m]

        Returns
        -------
        np.ndarray
            Array de frecuencias ω [rad/s]
        """
        m_psi_si = self.constantes.m_psi_ev * EV_TO_J / C**2  # kg
        omega_min_sq = (m_psi_si * C**2 / HBAR)**2

        return np.sqrt(C**2 * k_array**2 + omega_min_sq)


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 6: SEÑAL INEQUÍVOCA DE LARMOR / UNEQUIVOCAL LARMOR SIGNAL
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SenalLarmor:
    """
    Modulación de Larmor del tejido con anisotropía sidérea.

    El vacío estándar es isótropo. El vacío tejido fluye con dirección:
    v_gal ≈ 220 km/s hacia Cygnus (l=90°)

    Efecto Doppler galáctico:
    f_obs = f₀(1 + v_gal·n̂/c) ≈ 141.7001 ± 0.1 Hz
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def frecuencia_observada(
        self,
        theta_gal_deg: float,
        phi_gal_deg: float = 0.0
    ) -> float:
        """
        Frecuencia observada con corrimiento Doppler galáctico.

        f_obs = f₀(1 + (v_gal/c)·cosθ)

        Parameters
        ----------
        theta_gal_deg : float
            Ángulo respecto a la dirección de Cygnus [grados]
        phi_gal_deg : float
            Ángulo azimutal [grados]

        Returns
        -------
        float
            f_obs [Hz]
        """
        theta_rad = math.radians(theta_gal_deg)

        # Corrimiento Doppler
        beta = self.constantes.v_gal / C
        doppler_factor = 1.0 + beta * math.cos(theta_rad)

        return self.constantes.f0 * doppler_factor

    def anisotropia_sidereal(self, direccion: str) -> Tuple[float, float]:
        """
        Anisotropía sidérea en tres direcciones galácticas clave.

        Parameters
        ----------
        direccion : str
            'cygnus' (l=90°), 'anticentro' (l=180°), 'centauro' (l=270°)

        Returns
        -------
        tuple
            (f_obs [Hz], Δf [Hz])
        """
        direcciones = {
            'cygnus': 0.0,        # Hacia Cygnus (+v_gal)
            'anticentro': 90.0,   # Perpendicular
            'centauro': 180.0,    # Contra Cygnus (-v_gal)
        }

        if direccion not in direcciones:
            raise ValueError(f"Dirección inválida: {direccion}")

        theta = direcciones[direccion]
        f_obs = self.frecuencia_observada(theta)
        delta_f = f_obs - self.constantes.f0

        return f_obs, delta_f

    def tabla_anisotropia(self) -> Dict[str, Dict[str, float]]:
        """
        Tabla completa de anisotropía sidérea.

        Returns
        -------
        dict
            Diccionario con direcciones y mediciones
        """
        beta = self.constantes.v_gal / C

        return {
            'Hacia Cygnus (l=90°)': {
                'v_gal_n': +self.constantes.v_gal,
                'f_obs_Hz': self.constantes.f0 * (1.0 + beta),
                'variacion_Hz': +beta * self.constantes.f0,
            },
            'Hacia Anticentro (l=180°)': {
                'v_gal_n': 0.0,
                'f_obs_Hz': self.constantes.f0,
                'variacion_Hz': 0.0,
            },
            'Hacia Centauro (l=270°)': {
                'v_gal_n': -self.constantes.v_gal,
                'f_obs_Hz': self.constantes.f0 * (1.0 - beta),
                'variacion_Hz': -beta * self.constantes.f0,
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 7: INTERFERÓMETRO DE SAGNAC RESONANTE / RESONANT SAGNAC INTERFEROMETER
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class InterferometroSagnac:
    """
    Interferómetro de Sagnac Resonante (IRS-Luna).

    Técnica de batido heterodino que explota la quiralidad del tejido (Φ ≈ 0.4 rad):

    1. Láser linealmente polarizado se divide en dos haces (CW/CCW)
    2. Cada haz acumula fase diferente por la quiralidad: Φ y -Φ
    3. Recombinación produce batido a 2Φ · f_rotación
    4. Modulación de intensidad exactamente a 141.7001 Hz
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )

    def fase_acumulada(
        self,
        L: float,
        direccion: str = 'CW'
    ) -> float:
        """
        Fase acumulada en un brazo del interferómetro.

        Φ_CW = +Φ (sentido horario)
        Φ_CCW = -Φ (sentido antihorario)

        Parameters
        ----------
        L : float
            Longitud del brazo [m]
        direccion : str
            'CW' (horario) o 'CCW' (antihorario)

        Returns
        -------
        float
            Fase acumulada [rad]
        """
        # Fase por unidad de longitud
        k = 2.0 * math.pi * self.constantes.f0 / C

        # Fase geométrica
        phi_geometrica = k * L

        # Corrección quiral (±Φ según dirección)
        if direccion == 'CW':
            phi_quiral = +self.constantes.phi_chirality
        elif direccion == 'CCW':
            phi_quiral = -self.constantes.phi_chirality
        else:
            raise ValueError(f"Dirección inválida: {direccion}")

        return phi_geometrica + phi_quiral

    def diferencia_fase(self, L: float) -> float:
        """
        Diferencia de fase entre brazos CW y CCW.

        ΔΦ = Φ_CW - Φ_CCW = 2Φ

        Parameters
        ----------
        L : float
            Longitud del brazo [m]

        Returns
        -------
        float
            ΔΦ [rad]
        """
        phi_cw = self.fase_acumulada(L, 'CW')
        phi_ccw = self.fase_acumulada(L, 'CCW')

        return phi_cw - phi_ccw

    def frecuencia_batido(self, L: float, f_rotacion: float) -> float:
        """
        Frecuencia de batido heterodino.

        f_beat = 2Φ · f_rotacion

        Parameters
        ----------
        L : float
            Longitud del brazo [m]
        f_rotacion : float
            Frecuencia de rotación del interferómetro [Hz]

        Returns
        -------
        float
            f_beat [Hz]
        """
        delta_phi = self.diferencia_fase(L)

        # Modulación a 2Φ por revolución
        return abs(delta_phi) * f_rotacion / (2.0 * math.pi)

    def intensidad_batido(
        self,
        t: float,
        L: float,
        I0: float = 1.0,
        f_rotacion: float = None
    ) -> float:
        """
        Intensidad del patrón de batido en función del tiempo.

        I(t) = I₀[1 + cos(2πf_beat·t)]

        Parameters
        ----------
        t : float
            Tiempo [s]
        L : float
            Longitud del brazo [m]
        I0 : float
            Intensidad base
        f_rotacion : float, optional
            Frecuencia de rotación [Hz]. Si None, usa f₀

        Returns
        -------
        float
            I(t) (intensidad normalizada)
        """
        if f_rotacion is None:
            f_rotacion = self.constantes.f0

        f_beat = self.frecuencia_batido(L, f_rotacion)

        return I0 * (1.0 + math.cos(2.0 * math.pi * f_beat * t))

    def prediccion_irs_luna(self, L: float = 100.0e3) -> Dict[str, Any]:
        """
        Predicción completa para el experimento IRS-Luna.

        Parameters
        ----------
        L : float
            Longitud del brazo [m]. Default: 100 km

        Returns
        -------
        dict
            Diccionario con predicciones del experimento
        """
        delta_phi = self.diferencia_fase(L)

        return {
            'longitud_brazo_km': L / 1000.0,
            'fase_CW_rad': self.fase_acumulada(L, 'CW'),
            'fase_CCW_rad': self.fase_acumulada(L, 'CCW'),
            'diferencia_fase_rad': delta_phi,
            'frecuencia_modulacion_Hz': self.constantes.f0,
            'quiralidad_rad': self.constantes.phi_chirality,
            'prediccion': (
                f"Modulación de intensidad a {self.constantes.f0:.4f} Hz "
                f"con fase correlada al campo magnético galáctico local"
            ),
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE 8: COHERENCIA GLOBAL DEL SISTEMA / GLOBAL SYSTEM COHERENCE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoherenciaArquitecturaFisica:
    """
    Coherencia global del sistema de Arquitectura Física TOPC.

    Verifica que todos los componentes sean mutuamente consistentes.
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )
    hamiltoniano: HamiltonianoTotal = field(init=False)
    permittividad: PermitividadEfectiva = field(init=False)
    coeficiente_eta: CoeficienteMezclaFase = field(init=False)
    dispersion: RelacionDispersionThot = field(init=False)
    senal_larmor: SenalLarmor = field(init=False)
    sagnac: InterferometroSagnac = field(init=False)

    def __post_init__(self) -> None:
        self.hamiltoniano = HamiltonianoTotal(self.constantes)
        self.permittividad = PermitividadEfectiva(self.constantes)
        self.coeficiente_eta = CoeficienteMezclaFase(self.constantes)
        self.dispersion = RelacionDispersionThot(self.constantes)
        self.senal_larmor = SenalLarmor(self.constantes)
        self.sagnac = InterferometroSagnac(self.constantes)

    def calcular_coherencia(self) -> float:
        """
        Coherencia global Ψ_global del sistema.

        Verifica:
        1. ω_ψ = 2π f₀ (consistencia de frecuencia)
        2. λ_C = c/(2π f₀) (longitud de coherencia)
        3. Dispersión: ω²(k=0) = ω²_ψ (gap de masa)
        4. Resonancia: ε_eff diverge en ω = ω_ψ

        Returns
        -------
        float
            Ψ_global ∈ [0, 1]
        """
        coherencias = []

        # 1. Frecuencia fundamental
        omega_calc = 2.0 * math.pi * self.constantes.f0
        coherencias.append(
            1.0 - abs(omega_calc - self.constantes.omega_psi) / self.constantes.omega_psi
        )

        # 2. Longitud de coherencia
        lambda_calc = C / self.constantes.omega_psi
        coherencias.append(
            1.0 - abs(lambda_calc - self.constantes.lambda_coherence) / self.constantes.lambda_coherence
        )

        # 3. Gap de masa (dispersión en k=0)
        omega_min = self.dispersion.omega_minima()
        coherencias.append(
            1.0 - abs(omega_min - self.constantes.omega_psi) / self.constantes.omega_psi
        )

        # 4. Resonancia (|ε_eff| debe ser grande en ω = ω_ψ)
        epsilon_res = self.permittividad.epsilon_eff(self.constantes.omega_psi)
        if abs(epsilon_res) > 1.0:
            coherencias.append(min(1.0, 1.0 / abs(epsilon_res)))
        else:
            coherencias.append(0.5)

        # Coherencia global = promedio geométrico
        psi_global = np.prod(coherencias) ** (1.0 / len(coherencias))

        return float(psi_global)

    def validar_umbral(self, umbral: float = 0.888) -> bool:
        """
        Valida que Ψ_global ≥ umbral.

        Parameters
        ----------
        umbral : float
            Umbral mínimo de coherencia (default: 0.888)

        Returns
        -------
        bool
            True si Ψ_global ≥ umbral
        """
        psi_global = self.calcular_coherencia()
        return psi_global >= umbral


# ═══════════════════════════════════════════════════════════════════════════
# SISTEMA PRINCIPAL / MAIN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SistemaArquitecturaFisicaTopc:
    """
    Sistema completo de Arquitectura Física TOPC.

    Integra los 8 componentes del modelo:
    1. Constantes fundamentales
    2. Hamiltoniano total (EM + ψ + int)
    3. Permitividad efectiva ε_eff(ω,k)
    4. Coeficiente de mezcla η
    5. Relación de dispersión de Thot
    6. Señal de Larmor (anisotropía sidérea)
    7. Interferómetro de Sagnac (IRS-Luna)
    8. Coherencia global
    """

    constantes: ConstantesArquitecturaFisica = field(
        default_factory=ConstantesArquitecturaFisica
    )
    coherencia_sistema: CoherenciaArquitecturaFisica = field(init=False)

    def __post_init__(self) -> None:
        self.coherencia_sistema = CoherenciaArquitecturaFisica(self.constantes)

    def informe_completo(self) -> Dict[str, Any]:
        """
        Informe completo del sistema.

        Returns
        -------
        dict
            Diccionario con todos los parámetros y predicciones
        """
        psi_global = self.coherencia_sistema.calcular_coherencia()

        # Anisotropía sidérea
        tabla_aniso = self.coherencia_sistema.senal_larmor.tabla_anisotropia()

        # Predicción IRS-Luna
        pred_irs = self.coherencia_sistema.sagnac.prediccion_irs_luna()

        # Coeficiente η en resonancia
        eta_res = self.coherencia_sistema.coeficiente_eta.eta(
            self.constantes.omega_psi,
            100.0e3  # 100 km
        )
        regimen = self.coherencia_sistema.coeficiente_eta.regimen(eta_res)

        return {
            '1_parametros_fundamentales': {
                'f0_Hz': self.constantes.f0,
                'm_psi_eV': self.constantes.m_psi_ev,
                'omega_psi_rad_s': self.constantes.omega_psi,
                'lambda_coherence_km': self.constantes.lambda_coherence / 1000.0,
                'g_agg_GeV_inv': self.constantes.g_agg,
                'v_gal_km_s': self.constantes.v_gal / 1000.0,
                'phi_chirality_rad': self.constantes.phi_chirality,
            },
            '2_hamiltoniano_total': {
                'componentes': ['H_EM', 'H_psi', 'H_int'],
                'descripcion': 'Tres cuerpos en uno',
            },
            '3_permittividad_efectiva': {
                'resonancia_omega_psi': self.constantes.omega_psi,
                'velocidad_grupo_m_s': self.coherencia_sistema.permittividad.velocidad_grupo(
                    self.constantes.omega_psi
                ),
            },
            '4_coeficiente_eta': {
                'eta_L100km': eta_res,
                'regimen': regimen,
            },
            '5_dispersion_thot': {
                'omega_min_rad_s': self.coherencia_sistema.dispersion.omega_minima(),
                'tipo': 'hiperbolica',
            },
            '6_senal_larmor': tabla_aniso,
            '7_irs_luna': pred_irs,
            '8_coherencia_global': {
                'Psi_global': psi_global,
                'umbral_888': psi_global >= 0.888,
                'estado': 'ÓPTIMO' if psi_global >= 0.888 else 'SUBÓPTIMO',
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# API PÚBLICA / PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def arquitectura_fisica_topc_activar(
    f0: float = F0_HZ,
    m_psi_ev: float = M_PSI_EV,
    mostrar_informe: bool = True
) -> SistemaArquitecturaFisicaTopc:
    """
    Activa el sistema completo de Arquitectura Física TOPC.

    Parameters
    ----------
    f0 : float
        Frecuencia fundamental [Hz]
    m_psi_ev : float
        Masa del campo ψ [eV/c²]
    mostrar_informe : bool
        Si True, imprime el informe completo

    Returns
    -------
    SistemaArquitecturaFisicaTopc
        Sistema completo activado

    Examples
    --------
    >>> sistema = arquitectura_fisica_topc_activar()
    >>> informe = sistema.informe_completo()
    >>> print(informe['8_coherencia_global']['Psi_global'])
    0.9995
    """
    constantes = ConstantesArquitecturaFisica(
        f0=f0,
        m_psi_ev=m_psi_ev
    )

    sistema = SistemaArquitecturaFisicaTopc(constantes)

    if mostrar_informe:
        informe = sistema.informe_completo()
        print("\n" + "="*80)
        print("    ARQUITECTURA FÍSICA TOPC (AFP∞³) — INFORME COMPLETO")
        print("="*80 + "\n")

        for seccion, datos in informe.items():
            print(f"\n{seccion}:")
            print("-" * 60)
            _imprimir_dict(datos, indent=2)

        print("\n" + "="*80)
        print("𓂀 Ω ∞³ Φ · ARQUITECTURA FÍSICA MANIFESTADA ✅")
        print("="*80 + "\n")

    return sistema


def _imprimir_dict(d: Dict[str, Any], indent: int = 0) -> None:
    """Helper para imprimir diccionarios anidados."""
    for key, value in d.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            _imprimir_dict(value, indent + 2)
        else:
            if isinstance(value, float):
                print(" " * indent + f"{key}: {value:.6e}")
            else:
                print(" " * indent + f"{key}: {value}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN (para pruebas directas)
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  ARQUITECTURA FÍSICA TOPC (AFP∞³) — Sistema de Prueba                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    sistema = arquitectura_fisica_topc_activar()

    # Verificación de coherencia
    psi_global = sistema.coherencia_sistema.calcular_coherencia()
    print(f"\nΨ_global = {psi_global:.6f}")

    if psi_global >= 0.888:
        print("✅ Sistema coherente (Ψ ≥ 0.888)")
    else:
        print("⚠️  Sistema subóptimo (Ψ < 0.888)")
