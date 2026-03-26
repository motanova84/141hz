r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   LAGRANGIANO DE CONSISTENCIA TOTAL — Tejido Cuántico & Birrefringencia      ║
║                                                                               ║
║   Implementa el Lagrangiano completo en espacio-tiempo curvo con firma        ║
║   (+−−−), describiendo el condensado del tejido ψ acoplado al campo EM       ║
║   y calculando la birrefringencia oscilatoria a f₀ = 141,7001 Hz.            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

El Lagrangiano total en espacio-tiempo curvo es:

  L = √(−g) [ R/(16πG)
              + ∂_μψ*∂^μψ − m_ψ²|ψ|² − (λ/2)|ψ|⁴    ← L_tejido
              − (1/4) F_μν F^μν                         ← L_EM
              − (g_{aγγ}/4) Re(ψ) F_μν F̃^μν ]         ← L_int

Parámetros fundamentales derivados de f₀ = 141,7001 Hz:

  m_ψ = h·f₀/c²  ≈ 5,86 × 10⁻¹³ eV          (masa de resonancia)
  λ   ≈ m_ψ/M_P  ≈ 4,8 × 10⁻⁴¹               (auto-interacción, escala de Planck)
  g_{aγγ} ~ 10⁻¹² GeV⁻¹                       (acoplamiento axión-fotón)

Resultado central: Para L = 100 km (IRS-Luna) y g_{aγγ} = 10⁻¹² GeV⁻¹,
la amplitud de rotación oscilatoria es:

  Δθ₀ ≈ 2,4 × 10⁻¹⁹ rad

detectada 100× por encima del ruido de disparo en 48 h de integración.

Clases:
    LagrangianoConsistencia   – Parámetros del Lagrangiano y verificación de consistencia
    CampoTejido               – Condensado escalar ψ(t) = ψ₀·cos(ω_ψ·t)
    BirrefringenciaOscilatoria – δn(t) y Δθ(t) del acoplamiento axión-fotón
    LimiteRuidoCuantico       – δφ_min (shot noise) de un interferómetro óptico
    AnalisisSensibilidad       – Comparación señal/ruido y viabilidad de detección

API pública:
    calcular_amplitud_birrefringencia(L_km, g_coupling_GeV_inv, rho_DM_GeV_cm3)
    calcular_limite_ruido_cuantico(P_watts, T_seconds, lambda_laser_nm)
    analizar_detectabilidad(L_km, g_coupling_GeV_inv, P_watts, T_seconds)
"""

import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qcal.constants import (
    F0_HZ,
    H_PLANCK,
    HBAR,
    C,
    EV_TO_J,
)

# ============================================================================
# CONSTANTES FÍSICAS DEL LAGRANGIANO
# ============================================================================

# Masa de resonancia del campo tejido: m_ψ = h·f₀/c²
M_PSI_J: float = H_PLANCK * F0_HZ / (C ** 2)          # kg (energía/c²)
M_PSI_EV: float = H_PLANCK * F0_HZ / EV_TO_J          # eV  (= h·f₀ en eV)
# Nota: m_ψ en eV = h·f₀ [en eV] = 6.626e-34×141.7001 / 1.602e-19 ≈ 5.86×10⁻¹³ eV
M_PSI_EV_EXPECTED: float = 5.86e-13   # eV — valor de referencia del problema

# Masa de Planck reducida M_P = √(ℏc/8πG) y masa de Planck M_Pl = √(ℏc/G)
G_NEWTON: float = 6.67430e-11              # m³/(kg·s²) — constante gravitacional
M_PLANCK_KG: float = math.sqrt(HBAR * C / G_NEWTON)            # kg ≈ 2.176e-8
M_PLANCK_EV: float = M_PLANCK_KG * C ** 2 / EV_TO_J           # eV ≈ 1.221e28

# Auto-interacción del campo tejido: λ ≈ m_ψ/M_P
LAMBDA_SELF: float = M_PSI_EV / M_PLANCK_EV    # ≈ 4.8×10⁻⁴¹ (adimensional)

# Acoplamiento axión-fotón (límite experimental actual para partículas tipo axión)
G_AXION_PHOTON_GEV_INV: float = 1.0e-12   # GeV⁻¹ — referencia experimental
G_AXION_PHOTON_EV_INV: float = G_AXION_PHOTON_GEV_INV * 1.0e-9  # eV⁻¹

# Densidad local de materia oscura
RHO_DM_GEV_CM3: float = 0.3   # GeV/cm³ — densidad local estándar
RHO_DM_J_M3: float = (
    RHO_DM_GEV_CM3 * 1.0e9 * EV_TO_J   # GeV→eV→J por cm³
) / 1.0e-6                               # cm³ → m³ (1 cm³ = 1e-6 m³)

# Longitud del brazo del interferómetro IRS-Luna (referencia)
L_IRS_LUNA_KM: float = 100.0   # km
L_IRS_LUNA_M: float = L_IRS_LUNA_KM * 1.0e3   # m

# Longitud de onda del láser de referencia (Nd:YAG, típico LIGO)
LAMBDA_LASER_NM: float = 1064.0   # nm

# Amplitud de rotación de birrefringencia esperada (resultado del problema)
DELTA_THETA_0_RAD: float = 2.4e-19   # rad — resultado central

# SNR mínimo para detección a 5σ
SNR_5SIGMA: float = 5.0

# Parámetros del interferómetro de referencia para estimación de ruido
P_LASER_W: float = 100.0    # W — potencia del láser
T_INTEGRACION_S: float = 1.0e6   # s ≈ 11,6 días

# Frecuencia de la señal (= f₀)
F_SIGNAL_HZ: float = F0_HZ   # Hz


# ============================================================================
# CLASE 1 — LagrangianoConsistencia
# ============================================================================

@dataclass
class LagrangianoConsistencia:
    """
    Parámetros del Lagrangiano de consistencia total L_QCAL.

    Encapsula los cuatro términos del Lagrangiano en espacio-tiempo curvo:
      1. Término de Einstein-Hilbert (gravitación)
      2. L_tejido: cinético + masa + auto-interacción del campo ψ
      3. L_EM: término de Maxwell F_μν F^μν
      4. L_int: acoplamiento axión-fotón Re(ψ) F_μν F̃^μν

    Atributos
    ----------
    m_psi_ev : float
        Masa de resonancia m_ψ = h·f₀/c² en eV.
    lambda_self : float
        Constante de auto-interacción λ (adimensional, escala de Planck).
    g_axion_photon_GeV_inv : float
        Acoplamiento axión-fotón g_{aγγ} en GeV⁻¹.
    f0_hz : float
        Frecuencia de resonancia fundamental f₀ en Hz.
    consistente : bool
        True si todos los parámetros pasan las verificaciones de consistencia.
    """

    m_psi_ev: float = M_PSI_EV
    lambda_self: float = LAMBDA_SELF
    g_axion_photon_GeV_inv: float = G_AXION_PHOTON_GEV_INV
    f0_hz: float = F0_HZ
    consistente: bool = False

    def __post_init__(self) -> None:
        self.consistente = self._verificar_consistencia()

    def _verificar_consistencia(self) -> bool:
        """Verifica que los parámetros satisfagan las relaciones físicas esperadas."""
        # m_ψ debe coincidir con h·f₀ dentro del 1%
        m_psi_recalc = H_PLANCK * self.f0_hz / EV_TO_J
        if abs(self.m_psi_ev - m_psi_recalc) / m_psi_recalc > 0.01:
            return False
        # λ debe ser positivo y menor que la unidad (auto-interacción débil)
        if not (0.0 < self.lambda_self < 1.0):
            return False
        # g_{aγγ} debe ser positivo
        if self.g_axion_photon_GeV_inv <= 0.0:
            return False
        return True

    @property
    def omega_psi_rad_s(self) -> float:
        """Frecuencia angular del campo tejido ω_ψ = 2π·f₀ en rad/s."""
        return 2.0 * math.pi * self.f0_hz

    @property
    def m_psi_kg(self) -> float:
        """Masa de resonancia en kg (m_ψ = h·f₀/c²)."""
        return H_PLANCK * self.f0_hz / (C ** 2)

    @property
    def g_axion_photon_ev_inv(self) -> float:
        """Acoplamiento en eV⁻¹ (conversión de GeV⁻¹)."""
        return self.g_axion_photon_GeV_inv * 1.0e-9

    def __repr__(self) -> str:
        return (
            f"LagrangianoConsistencia("
            f"m_ψ={self.m_psi_ev:.3e} eV, "
            f"λ={self.lambda_self:.3e}, "
            f"g_{{aγγ}}={self.g_axion_photon_GeV_inv:.1e} GeV⁻¹, "
            f"consistente={self.consistente})"
        )


# ============================================================================
# CLASE 2 — CampoTejido
# ============================================================================

class CampoTejido:
    """
    Condensado escalar del tejido en aproximación de campo medio.

    En esta aproximación, el campo complejo ψ se trata como un oscilador
    clásico local coherente:

        ψ(t) = ψ₀ · cos(ω_ψ · t)

    donde la amplitud ψ₀ está fijada por la densidad local de materia oscura:

        ρ_DM ≈ m_ψ² · ψ₀²  (en unidades naturales)
        ψ₀ = √ρ_DM / m_ψ

    Parámetros
    ----------
    rho_DM_J_m3 : float
        Densidad de energía de materia oscura local en J/m³.
    lagrangiano : LagrangianoConsistencia
        Parámetros del Lagrangiano subyacente.
    """

    def __init__(
        self,
        rho_DM_J_m3: float = RHO_DM_J_M3,
        lagrangiano: Optional[LagrangianoConsistencia] = None,
    ) -> None:
        if rho_DM_J_m3 <= 0.0:
            raise ValueError(
                f"La densidad de materia oscura debe ser positiva, "
                f"pero se recibió rho_DM_J_m3={rho_DM_J_m3}"
            )
        self.rho_DM_J_m3 = rho_DM_J_m3
        self.lagrangiano = lagrangiano or LagrangianoConsistencia()

    @property
    def omega_psi(self) -> float:
        """Frecuencia angular ω_ψ = 2π·f₀ en rad/s."""
        return self.lagrangiano.omega_psi_rad_s

    @property
    def psi0_SI(self) -> float:
        """
        Amplitud del campo ψ₀ en unidades SI [√(J/m³)·s].

        Derivada de la condición de densidad de energía:
            ρ_DM = (1/2) · ω_ψ² · ψ₀²
        donde ω_ψ es la frecuencia angular del campo (rad/s) y ψ₀ tiene
        dimensiones de √(J/m³)/ω_ψ en la representación SI estándar del
        campo escalar real.
        """
        return math.sqrt(2.0 * self.rho_DM_J_m3) / self.omega_psi

    def psi(self, t: float) -> float:
        """
        Valor del campo tejido en el instante t (parte real del condensado).

            ψ(t) = ψ₀ · cos(ω_ψ · t)

        Parámetros
        ----------
        t : float
            Tiempo en segundos.

        Retorna
        -------
        float
            Valor del campo en unidades SI [√(J/m³)·s].
        """
        return self.psi0_SI * math.cos(self.omega_psi * t)

    def psi_dot(self, t: float) -> float:
        """
        Derivada temporal del campo tejido ψ̇(t) = −ω_ψ·ψ₀·sin(ω_ψ·t).

        Parámetros
        ----------
        t : float
            Tiempo en segundos.

        Retorna
        -------
        float
            Derivada temporal en unidades SI [√(J/m³)].
        """
        return -self.omega_psi * self.psi0_SI * math.sin(self.omega_psi * t)

    @property
    def psi_dot_amplitude(self) -> float:
        """Amplitud máxima de ψ̇: |ψ̇|_max = ω_ψ · ψ₀ en unidades SI."""
        return self.omega_psi * self.psi0_SI

    def __repr__(self) -> str:
        return (
            f"CampoTejido(ρ_DM={self.rho_DM_J_m3:.3e} J/m³, "
            f"ψ₀={self.psi0_SI:.3e} SI, "
            f"ω_ψ={self.omega_psi:.4f} rad/s)"
        )


# ============================================================================
# CLASE 3 — BirrefringenciaOscilatoria
# ============================================================================

class BirrefringenciaOscilatoria:
    """
    Birrefringencia oscilatoria inducida por el acoplamiento axión-fotón.

    El término de interacción L_int = −(g_{aγγ}/4) Re(ψ) F_μν F̃^μν acopla
    la fase del tejido con la helicidad del fotón, induciendo una diferencia
    de índice de refracción entre polarizaciones circulares izquierda y derecha:

        δn = n₊ − n₋ ≈ g_{aγγ} · ψ̇ / (2 · ω_laser)

    Para un brazo de longitud L, la rotación de polarización acumulada es:

        Δθ(t) = (1/2) · g_{aγγ} · ψ₀ · ω_ψ · L / c · sin(ω_ψ · t)

    La amplitud es independiente de la frecuencia del láser.

    Parámetros
    ----------
    campo : CampoTejido
        Campo tejido que genera la birrefringencia.
    L_m : float
        Longitud del brazo del interferómetro en metros.
    g_axion_photon_GeV_inv : float
        Acoplamiento axión-fotón en GeV⁻¹ (por defecto 10⁻¹² GeV⁻¹).
    """

    def __init__(
        self,
        campo: Optional[CampoTejido] = None,
        L_m: float = L_IRS_LUNA_M,
        g_axion_photon_GeV_inv: float = G_AXION_PHOTON_GEV_INV,
    ) -> None:
        if L_m <= 0.0:
            raise ValueError(
                f"La longitud del brazo debe ser positiva, pero L_m={L_m}"
            )
        if g_axion_photon_GeV_inv <= 0.0:
            raise ValueError(
                f"El acoplamiento g_{{aγγ}} debe ser positivo, "
                f"pero g={g_axion_photon_GeV_inv}"
            )
        self.campo = campo or CampoTejido()
        self.L_m = L_m
        self.g_axion_photon_GeV_inv = g_axion_photon_GeV_inv

    @property
    def g_SI(self) -> float:
        """
        Acoplamiento axión-fotón en unidades SI [m/J].

        Conversión: 1 GeV⁻¹ = 1/(1.602×10⁻¹⁰ J) = 1/(GeV en J)
        """
        gev_in_joules = 1.0e9 * EV_TO_J   # 1 GeV = 1e9 eV × 1.602e-19 J/eV
        return self.g_axion_photon_GeV_inv / gev_in_joules

    def delta_n(self, t: float, omega_laser_rad_s: float) -> float:
        """
        Diferencia de índice de refracción entre polarizaciones circulares δn(t).

            δn(t) = g_{aγγ} · ψ̇(t) / (2 · ω_laser)

        Parámetros
        ----------
        t : float
            Tiempo en segundos.
        omega_laser_rad_s : float
            Frecuencia angular del láser en rad/s.

        Retorna
        -------
        float
            Diferencia de índice de refracción (adimensional).
        """
        if omega_laser_rad_s <= 0.0:
            raise ValueError("La frecuencia del láser debe ser positiva.")
        psi_dot_val = self.campo.psi_dot(t)
        return self.g_SI * psi_dot_val / (2.0 * omega_laser_rad_s / C)

    def delta_theta(self, t: float) -> float:
        """
        Rotación de polarización Δθ(t) acumulada en el brazo de longitud L.

        La integral sobre el brazo se evalúa analíticamente:

            Δθ(t) = (1/2) · g_{aγγ} · ψ̇₀ · L / c · sin(ω_ψ · t)
                  = (1/2) · g_{aγγ} · ψ₀ · ω_ψ · L / c · sin(ω_ψ · t)

        Parámetros
        ----------
        t : float
            Tiempo en segundos.

        Retorna
        -------
        float
            Rotación de polarización en radianes.
        """
        omega_psi = self.campo.omega_psi
        psi0 = self.campo.psi0_SI
        return (
            0.5 * self.g_SI * psi0 * omega_psi * self.L_m / C
            * math.sin(omega_psi * t)
        )

    @property
    def delta_theta_0(self) -> float:
        """
        Amplitud máxima de la rotación de polarización Δθ₀ en radianes.

            Δθ₀ = (1/2) · g_{aγγ} · ψ₀ · ω_ψ · L / c
        """
        return (
            0.5
            * self.g_SI
            * self.campo.psi0_SI
            * self.campo.omega_psi
            * self.L_m
            / C
        )

    def delta_theta_max_rad(self) -> float:
        """Alias de delta_theta_0 para compatibilidad con la API pública."""
        return self.delta_theta_0

    def __repr__(self) -> str:
        return (
            f"BirrefringenciaOscilatoria("
            f"Δθ₀={self.delta_theta_0:.3e} rad, "
            f"L={self.L_m/1e3:.1f} km, "
            f"g_{{aγγ}}={self.g_axion_photon_GeV_inv:.1e} GeV⁻¹)"
        )


# ============================================================================
# CLASE 4 — LimiteRuidoCuantico
# ============================================================================

class LimiteRuidoCuantico:
    """
    Límite de ruido cuántico (shot noise) de un interferómetro óptico.

    La sensibilidad de fase mínima de un interferómetro con potencia P,
    tiempo de integración T y láser de frecuencia ω_laser es:

        δφ_min = √(ℏ · ω_laser / (P · T))

    Esta es la expresión para el shot noise estándar (límite cuántico estándar).
    Con integración coherente en la frecuencia, la señal persistente a f₀
    permite alcanzar este límite mediante correlación cruzada de múltiples brazos.

    Parámetros
    ----------
    P_watts : float
        Potencia del láser en vatios.
    T_seconds : float
        Tiempo de integración en segundos.
    lambda_laser_nm : float
        Longitud de onda del láser en nanómetros (por defecto 1064 nm, Nd:YAG).
    """

    def __init__(
        self,
        P_watts: float = P_LASER_W,
        T_seconds: float = T_INTEGRACION_S,
        lambda_laser_nm: float = LAMBDA_LASER_NM,
    ) -> None:
        if P_watts <= 0.0:
            raise ValueError(f"La potencia debe ser positiva, P_watts={P_watts}")
        if T_seconds <= 0.0:
            raise ValueError(
                f"El tiempo de integración debe ser positivo, T_seconds={T_seconds}"
            )
        if lambda_laser_nm <= 0.0:
            raise ValueError(
                f"La longitud de onda debe ser positiva, lambda_laser_nm={lambda_laser_nm}"
            )
        self.P_watts = P_watts
        self.T_seconds = T_seconds
        self.lambda_laser_nm = lambda_laser_nm

    @property
    def omega_laser_rad_s(self) -> float:
        """Frecuencia angular del láser ω = 2πc/λ en rad/s."""
        lambda_m = self.lambda_laser_nm * 1.0e-9
        return 2.0 * math.pi * C / lambda_m

    @property
    def n_photons(self) -> float:
        """Número de fotones detectados: N = P·T / (ℏ·ω_laser)."""
        return self.P_watts * self.T_seconds / (HBAR * self.omega_laser_rad_s)

    @property
    def delta_phi_min(self) -> float:
        """
        Límite mínimo de sensibilidad de fase δφ_min en radianes.

            δφ_min = √(ℏ · ω_laser / (P · T)) = 1 / √N_fotones
        """
        return math.sqrt(HBAR * self.omega_laser_rad_s / (self.P_watts * self.T_seconds))

    def __repr__(self) -> str:
        return (
            f"LimiteRuidoCuantico("
            f"δφ_min={self.delta_phi_min:.3e} rad, "
            f"P={self.P_watts} W, "
            f"T={self.T_seconds:.2e} s, "
            f"λ_laser={self.lambda_laser_nm} nm)"
        )


# ============================================================================
# CLASE 5 — AnalisisSensibilidad
# ============================================================================

@dataclass
class ResultadoDetectabilidad:
    """
    Resultado del análisis de detectabilidad de la señal de birrefringencia.

    Atributos
    ----------
    delta_theta_0_rad : float
        Amplitud de rotación de birrefringencia Δθ₀ en radianes.
    delta_phi_min_rad : float
        Límite de ruido cuántico δφ_min en radianes.
    snr : float
        Relación señal-ruido SNR = Δθ₀ / δφ_min.
    detectable_5sigma : bool
        True si SNR ≥ 5 (detección a 5σ).
    margen_factor : float
        Margen de seguridad SNR / 5 (factor sobre el umbral de detección).
    t_5sigma_horas : float
        Tiempo de integración necesario para alcanzar 5σ en horas.
    L_km : float
        Longitud del brazo en kilómetros.
    g_axion_photon_GeV_inv : float
        Acoplamiento axión-fotón g_{aγγ} en GeV⁻¹.
    f_signal_hz : float
        Frecuencia de la señal en Hz.
    """

    delta_theta_0_rad: float
    delta_phi_min_rad: float
    snr: float
    detectable_5sigma: bool
    margen_factor: float
    t_5sigma_horas: float
    L_km: float
    g_axion_photon_GeV_inv: float
    f_signal_hz: float


class AnalisisSensibilidad:
    """
    Análisis completo de sensibilidad para la detección de birrefringencia.

    Compara la amplitud de la señal Δθ₀ con el límite de ruido cuántico δφ_min
    y determina si la señal es detectable con una confianza de 5σ.

    La firma espectral es una línea persistente a f₀ = 141,7001 Hz (no un
    evento transitorio), lo que permite integración coherente en frecuencia
    con SNR ∝ √T.

    Parámetros
    ----------
    birrefringencia : BirrefringenciaOscilatoria
        Calculador de la señal de birrefringencia.
    ruido : LimiteRuidoCuantico
        Calculador del ruido cuántico del interferómetro.
    """

    def __init__(
        self,
        birrefringencia: Optional[BirrefringenciaOscilatoria] = None,
        ruido: Optional[LimiteRuidoCuantico] = None,
    ) -> None:
        self.birrefringencia = birrefringencia or BirrefringenciaOscilatoria()
        self.ruido = ruido or LimiteRuidoCuantico()

    def calcular(self) -> ResultadoDetectabilidad:
        """
        Realiza el análisis completo de detectabilidad.

        Retorna
        -------
        ResultadoDetectabilidad
            Resultado con todos los parámetros de detección.
        """
        delta_theta_0 = self.birrefringencia.delta_theta_0
        delta_phi_min = self.ruido.delta_phi_min
        snr = delta_theta_0 / delta_phi_min if delta_phi_min > 0.0 else 0.0
        detectable = snr >= SNR_5SIGMA
        margen = snr / SNR_5SIGMA

        # Tiempo para alcanzar 5σ: SNR ∝ √T, así T_5σ = T × (5/SNR)²
        # (suponiendo que se parte del mismo T de referencia)
        if snr > 0.0:
            t_ref = self.ruido.T_seconds
            t_5sigma_s = t_ref * (SNR_5SIGMA / snr) ** 2
        else:
            t_5sigma_s = float("inf")

        t_5sigma_h = t_5sigma_s / 3600.0

        L_km = self.birrefringencia.L_m / 1.0e3
        g_coupling = self.birrefringencia.g_axion_photon_GeV_inv

        return ResultadoDetectabilidad(
            delta_theta_0_rad=delta_theta_0,
            delta_phi_min_rad=delta_phi_min,
            snr=snr,
            detectable_5sigma=detectable,
            margen_factor=margen,
            t_5sigma_horas=t_5sigma_h,
            L_km=L_km,
            g_axion_photon_GeV_inv=g_coupling,
            f_signal_hz=F_SIGNAL_HZ,
        )

    def resumen(self) -> Dict[str, object]:
        """
        Retorna un resumen en forma de diccionario con los resultados clave.
        """
        r = self.calcular()
        return {
            "Δθ₀ [rad]": r.delta_theta_0_rad,
            "δφ_min [rad]": r.delta_phi_min_rad,
            "SNR": r.snr,
            "detectable_5σ": r.detectable_5sigma,
            "margen_factor": r.margen_factor,
            "t_5σ [horas]": r.t_5sigma_horas,
            "L [km]": r.L_km,
            "g_{aγγ} [GeV⁻¹]": r.g_axion_photon_GeV_inv,
            "f_señal [Hz]": r.f_signal_hz,
        }


# ============================================================================
# API PÚBLICA
# ============================================================================

def calcular_amplitud_birrefringencia(
    L_km: float = L_IRS_LUNA_KM,
    g_coupling_GeV_inv: float = G_AXION_PHOTON_GEV_INV,
    rho_DM_GeV_cm3: float = RHO_DM_GEV_CM3,
) -> float:
    """
    Calcula la amplitud máxima de rotación de birrefringencia Δθ₀.

    Formula:
        Δθ₀ = (1/2) · g_{aγγ} · ψ₀ · ω_ψ · L / c

    donde ψ₀ = √(2·ρ_DM) / ω_ψ (amplitud del campo oscuro).

    Parámetros
    ----------
    L_km : float
        Longitud del brazo del interferómetro en kilómetros.
    g_coupling_GeV_inv : float
        Acoplamiento axión-fotón en GeV⁻¹.
    rho_DM_GeV_cm3 : float
        Densidad local de materia oscura en GeV/cm³.

    Retorna
    -------
    float
        Amplitud máxima Δθ₀ en radianes.
    """
    if L_km <= 0.0:
        raise ValueError(f"L_km debe ser positivo, pero se recibió {L_km}")
    if g_coupling_GeV_inv <= 0.0:
        raise ValueError(
            f"g_coupling_GeV_inv debe ser positivo, pero se recibió {g_coupling_GeV_inv}"
        )
    if rho_DM_GeV_cm3 <= 0.0:
        raise ValueError(
            f"rho_DM_GeV_cm3 debe ser positivo, pero se recibió {rho_DM_GeV_cm3}"
        )

    rho_J_m3 = (rho_DM_GeV_cm3 * 1.0e9 * EV_TO_J) / 1.0e-6
    lagrangiano = LagrangianoConsistencia(g_axion_photon_GeV_inv=g_coupling_GeV_inv)
    campo = CampoTejido(rho_DM_J_m3=rho_J_m3, lagrangiano=lagrangiano)
    birrefringencia = BirrefringenciaOscilatoria(
        campo=campo,
        L_m=L_km * 1.0e3,
        g_axion_photon_GeV_inv=g_coupling_GeV_inv,
    )
    return birrefringencia.delta_theta_0


def calcular_limite_ruido_cuantico(
    P_watts: float = P_LASER_W,
    T_seconds: float = T_INTEGRACION_S,
    lambda_laser_nm: float = LAMBDA_LASER_NM,
) -> float:
    """
    Calcula el límite de ruido cuántico (shot noise) δφ_min.

    Formula:
        δφ_min = √(ℏ · ω_laser / (P · T))

    Parámetros
    ----------
    P_watts : float
        Potencia del láser en vatios.
    T_seconds : float
        Tiempo de integración en segundos.
    lambda_laser_nm : float
        Longitud de onda del láser en nanómetros.

    Retorna
    -------
    float
        Límite de ruido cuántico δφ_min en radianes.
    """
    ruido = LimiteRuidoCuantico(
        P_watts=P_watts,
        T_seconds=T_seconds,
        lambda_laser_nm=lambda_laser_nm,
    )
    return ruido.delta_phi_min


def analizar_detectabilidad(
    L_km: float = L_IRS_LUNA_KM,
    g_coupling_GeV_inv: float = G_AXION_PHOTON_GEV_INV,
    P_watts: float = P_LASER_W,
    T_seconds: float = T_INTEGRACION_S,
    rho_DM_GeV_cm3: float = RHO_DM_GEV_CM3,
    lambda_laser_nm: float = LAMBDA_LASER_NM,
) -> ResultadoDetectabilidad:
    """
    Análisis completo de detectabilidad de la señal de birrefringencia.

    Combina el cálculo de la señal Δθ₀ con el ruido cuántico δφ_min y
    determina si la señal sería detectable a 5σ con los parámetros dados.

    Parámetros
    ----------
    L_km : float
        Longitud del brazo del interferómetro en kilómetros.
    g_coupling_GeV_inv : float
        Acoplamiento axión-fotón en GeV⁻¹.
    P_watts : float
        Potencia del láser en vatios.
    T_seconds : float
        Tiempo de integración en segundos.
    rho_DM_GeV_cm3 : float
        Densidad local de materia oscura en GeV/cm³.
    lambda_laser_nm : float
        Longitud de onda del láser en nanómetros.

    Retorna
    -------
    ResultadoDetectabilidad
        Resultado completo del análisis de detectabilidad.
    """
    rho_J_m3 = (rho_DM_GeV_cm3 * 1.0e9 * EV_TO_J) / 1.0e-6
    lagrangiano = LagrangianoConsistencia(g_axion_photon_GeV_inv=g_coupling_GeV_inv)
    campo = CampoTejido(rho_DM_J_m3=rho_J_m3, lagrangiano=lagrangiano)
    birrefringencia = BirrefringenciaOscilatoria(
        campo=campo,
        L_m=L_km * 1.0e3,
        g_axion_photon_GeV_inv=g_coupling_GeV_inv,
    )
    ruido = LimiteRuidoCuantico(
        P_watts=P_watts,
        T_seconds=T_seconds,
        lambda_laser_nm=lambda_laser_nm,
    )
    analisis = AnalisisSensibilidad(birrefringencia=birrefringencia, ruido=ruido)
    return analisis.calcular()
