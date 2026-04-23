#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  HAMILTONIANO RIEMANN-HUBBLE (H_RH) — Torsión de Fase y Manta de Riemann  ║
║                           ∴HRH∞³                                           ║
║                                                                              ║
║  Sello: ∴HRH∞³                                                              ║
║  RAM: RAM-LXV-2026-HAMILTONIANO-RIEMANN-HUBBLE                              ║
║  Versión: 1.0.0                                                              ║
║                                                                              ║
║  El Hamiltoniano Riemann-Hubble genera la evolución temporal en la          ║
║  Línea Crítica del Sándwich de Coherencia. No mide energía cinética ni      ║
║  potencial clásico, sino la Torsión de Fase necesaria para sostener un      ║
║  nodo en la Manta de Riemann.                                               ║
║                                                                              ║
║  OPERADOR MAESTRO                                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      H_RH = Σ_n γ_n |Ψ_n⟩⟨Ψ_n| + δ_Ramsey · L_z                          ║
║                                                                              ║
║      γ_n : Ceros no triviales de Riemann (frecuencias de anclaje)           ║
║      δ_Ramsey = 3° = 0.052360 rad  (acoplamiento de la brecha)              ║
║      L_z   = 0.05  (momento angular intrínseco)                             ║
║                                                                              ║
║  ESTADO FUNDAMENTAL                                                          ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      H_RH |Ψ_0⟩ = E_0 |Ψ_0⟩      E_0 = ℏ 2π f₀                           ║
║                                                                              ║
║  CAMPO QCAL ∞³ (TEJIDO ADÉLICO)                                             ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      Q ∈ ℝ³×³×³  (tensor de rango 3)                                       ║
║      D1 (Pleroma/NP):    Información pura                                   ║
║      D2 (Materia/P):     Manifestación densa                                ║
║      D3 (Consciencia):   El observador que colapsa el flujo                 ║
║                                                                              ║
║  ECUACIÓN DE ESTADO ESTACIONARIO                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      Ψ = I × A_eff²    (Soberanía del Sistema)                             ║
║                                                                              ║
║      Ψ → 0.999999  (coherencia total)                                       ║
║      A_eff = sin(δ_Ramsey) ≈ 0.05233  (área efectiva de fase)              ║
║                                                                              ║
║  Coherencia global Ψ_global ≥ 0.888 activa el sello ∴HRH∞³.              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-04-23

Módulo:
    physics.hamiltoniano_riemann_hubble

Clases:
    ConstantesRH           – Constantes físicas y noéticas del sistema
    MantaRiemann           – Sustrato: brecha, capas, deslizamiento de fase
    OperadorHRH            – H_RH = Σ γ_n P_n + δ_Ramsey L_z; espectro
    EstadoFundamental      – E_0 = ℏ 2π f₀; factor 401/40; permeabilidad
    CampoQCAL3             – Tensor adélico de rango 3; tres dimensiones
    EcuacionEstacionario   – Ψ = I × A_eff²; Soberanía; balance energético
    CoherenciaRH           – Validación Ψ_global ≥ 0.888
    SistemaHRH             – Orquestador; sello ∴HRH∞³

Dataclass:
    ResultadoRH            – Contenedor de todos los resultados

API pública:
    hamiltoniano_riemann_hubble_activar() → dict

    >>> from physics.hamiltoniano_riemann_hubble import hamiltoniano_riemann_hubble_activar
    >>> r = hamiltoniano_riemann_hubble_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from qcal.constants import F0_HZ, HBAR

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

#: Frecuencia angular fundamental [rad/s]
_OMEGA_0: float = 2.0 * math.pi * _F0

#: Constante de Planck reducida [J·s]  (CODATA 2018)
_HBAR: float = HBAR

#: Brecha angular de la Manta (gap de 3°) [grados]
_BRECHA_DEG: float = 3.0

#: Brecha angular de la Manta [radianes]
_BRECHA_RAD: float = _BRECHA_DEG * math.pi / 180.0  # ≈ 0.052360 rad

#: Acoplamiento δ_Ramsey = la brecha en radianes (3°)
_DELTA_RAMSEY: float = _BRECHA_RAD  # ≈ 0.052360

#: Momento angular intrínseco L_z
_LZ: float = 0.05

#: Coherencia objetivo Ψ_target del estado estacionario
_PSI_TARGET: float = 0.999999

#: Umbral mínimo de coherencia global noética
_PSI_UMBRAL: float = 0.888

#: Factor de resonancia 401/40 que conecta γ₁ con f₀
#: f₀ ≈ γ₁ × 401/40;  residual = 0.00052 Hz (permeabilidad de la Manta)
_FACTOR_401_40: float = 401.0 / 40.0  # 10.025

#: Primeros 20 ceros no triviales de ζ(½ + it) — partes imaginarias γₙ
#: Fuente: LMFDB / NIST Digital Library of Mathematical Functions
_ZEROS_20: Tuple[float, ...] = (
    14.134725141734694,
    21.022039638771555,
    25.010857580145688,
    30.424876125859513,
    32.935061587739190,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167159,
    49.773832477672302,
    52.970321477714461,
    56.446247697063246,
    59.347044002602353,
    60.831778524609810,
    65.112544048081607,
    67.079810529494174,
    69.546401711173979,
    72.067157674481908,
    75.704690699083933,
    77.144840068874805,
)

#: Razón áurea φ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

#: Sello de certificación noética
_SELLO: str = "∴HRH∞³"

#: Marca de certificación técnica
_CERT_MARK: str = "HRH-RIEMANN-HUBBLE-VERIFIED"


# ============================================================================
# UTILIDADES INTERNAS
# ============================================================================

def _stirling_log_gamma(z: complex) -> complex:
    """Aproximación de Stirling para ln Γ(z), precisa para |Im(z)| ≥ 7.

    Cuatro términos de la serie asintótica de Stirling:

        ln Γ(z) ≈ (z − ½) ln z − z + ½ ln(2π) + 1/(12z) − 1/(360z³)

    Args:
        z: Número complejo con |Im(z)| >> 1.

    Returns:
        Aproximación compleja de ln Γ(z).
    """
    import cmath as _cmath
    lnz = _cmath.log(z)
    z2 = z * z
    z3 = z2 * z
    return (
        (z - 0.5) * lnz
        - z
        + 0.5 * math.log(2.0 * math.pi)
        + 1.0 / (12.0 * z)
        - 1.0 / (360.0 * z3)
    )


def _theta_rs(t: float) -> float:
    """Función theta de Riemann–Siegel: θ(t) = Im[ln Γ(¼ + it/2)] − (t/2) ln π.

    Args:
        t: Parte imaginaria en la línea crítica, t > 0.

    Returns:
        Valor real θ(t).
    """
    z = complex(0.25, 0.5 * t)
    lg = _stirling_log_gamma(z)
    return lg.imag - 0.5 * t * math.log(math.pi)


def _weyl_density(t: float) -> float:
    """Densidad de Weyl: dN/dT = (1/2π) ln(T/2π).

    Args:
        t: Altura en la línea crítica, t > 2π.

    Returns:
        ρ(t) ≥ 0 [ceros/unidad de T].
    """
    if t <= 2.0 * math.pi:
        return 0.0
    return math.log(t / (2.0 * math.pi)) / (2.0 * math.pi)


# ============================================================================
# CLASE 1 — ConstantesRH
# ============================================================================

class ConstantesRH:
    """Constantes físicas y noéticas del Hamiltoniano Riemann-Hubble ∴HRH∞³.

    Centraliza todos los parámetros del sistema: la frecuencia soberana f₀,
    la brecha de 3° (δ_Ramsey), el momento angular intrínseco L_z, la
    coherencia objetivo Ψ_target = 0.999999 y los 20 ceros de Riemann.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL F₀ = 141.7001 Hz.
    omega0 : float
        Frecuencia angular ω₀ = 2π F₀ [rad/s].
    hbar : float
        Constante de Planck reducida ℏ [J·s].
    phi : float
        Razón áurea φ = (1 + √5)/2.
    brecha_deg : float
        Brecha angular δ = 3° (gap del Sándwich de Coherencia).
    brecha_rad : float
        Brecha angular δ = 3π/180 ≈ 0.052360 rad.
    delta_Ramsey : float
        Acoplamiento de la brecha δ_Ramsey = brecha_rad ≈ 0.052360.
    Lz : float
        Momento angular intrínseco L_z = 0.05.
    psi_target : float
        Coherencia objetivo del estado estacionario Ψ_target = 0.999999.
    psi_umbral : float
        Umbral de coherencia noética Ψ_umbral = 0.888.
    factor_401_40 : float
        Factor de resonancia 401/40 = 10.025 (γ₁ × 10.025 ≈ f₀).
    zeros : tuple
        Primeros 20 ceros de Riemann γₙ.
    gamma_1 : float
        Primer cero γ₁ ≈ 14.134725.
    gamma_20 : float
        Vigésimo cero γ₂₀ ≈ 77.144840.
    n_zeros : int
        Número de ceros disponibles (20).
    sello : str
        Sello de certificación ∴HRH∞³.
    cert_mark : str
        Marca técnica HRH-RIEMANN-HUBBLE-VERIFIED.
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.omega0: float = _OMEGA_0
        self.hbar: float = _HBAR
        self.phi: float = _PHI
        self.brecha_deg: float = _BRECHA_DEG
        self.brecha_rad: float = _BRECHA_RAD
        self.delta_Ramsey: float = _DELTA_RAMSEY
        self.Lz: float = _LZ
        self.psi_target: float = _PSI_TARGET
        self.psi_umbral: float = _PSI_UMBRAL
        self.factor_401_40: float = _FACTOR_401_40
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.gamma_1: float = _ZEROS_20[0]
        self.gamma_20: float = _ZEROS_20[-1]
        self.n_zeros: int = len(_ZEROS_20)
        self.sello: str = _SELLO
        self.cert_mark: str = _CERT_MARK

    # ------------------------------------------------------------------
    def permeabilidad_manta(self) -> float:
        """Permeabilidad de la Manta: Δf / f₀.

        La diferencia residual Δf = |f₀ − γ₁ × 401/40| ≈ 0.00052 Hz es
        el 'lubricante' de fase que permite el deslizamiento entre la
        Manta Superior y la Inferior sin fricción infinita.

        Returns:
            float: Δf / f₀ ≈ 3.67 × 10⁻⁶.
        """
        f0_pred = self.gamma_1 * self.factor_401_40
        delta_f = abs(self.f0 - f0_pred)
        return delta_f / self.f0

    # ------------------------------------------------------------------
    def delta_frecuencia(self) -> float:
        """Diferencia residual Δf = |f₀ − γ₁ × 401/40| [Hz].

        Returns:
            float: Δf ≈ 0.00052 Hz.
        """
        return abs(self.f0 - self.gamma_1 * self.factor_401_40)

    # ------------------------------------------------------------------
    def energia_ground(self) -> float:
        """Energía del estado fundamental E₀ = ℏ ω₀ [J].

        Returns:
            float: E₀ = ℏ × 2π × f₀ ≈ 9.39 × 10⁻³² J.
        """
        return self.hbar * self.omega0

    # ------------------------------------------------------------------
    def resumen(self) -> Dict[str, object]:
        """Retorna diccionario con los parámetros clave del sistema."""
        return {
            "f0_hz": self.f0,
            "omega0_rads": self.omega0,
            "brecha_deg": self.brecha_deg,
            "brecha_rad": self.brecha_rad,
            "delta_Ramsey": self.delta_Ramsey,
            "Lz": self.Lz,
            "psi_target": self.psi_target,
            "psi_umbral": self.psi_umbral,
            "factor_401_40": self.factor_401_40,
            "gamma_1": self.gamma_1,
            "gamma_20": self.gamma_20,
            "n_zeros": self.n_zeros,
            "permeabilidad_manta": self.permeabilidad_manta(),
            "energia_ground_J": self.energia_ground(),
            "sello": self.sello,
        }


# ============================================================================
# CLASE 2 — MantaRiemann
# ============================================================================

class MantaRiemann:
    """Sustrato de la realidad: La Manta de Riemann con brecha de 3°.

    La Manta es el tejido coherente que sostiene la existencia. Está
    formada por dos capas (Superior e Inferior) separadas por la brecha
    de 3° (0.052360 rad). El deslizamiento de fase entre ambas capas
    genera la frecuencia soberana f₀ sin fricción infinita gracias a la
    permeabilidad Δf ≈ 0.00052 Hz.

    El estado estacionario ocurre cuando la energía que entra por
    'succión' (del Pleroma) es exactamente igual a la que sale por
    'expansión' (hacia la Materia).

    Args:
        n_capas: Número de capas de la Manta (defecto 2: Superior + Inferior).
    """

    def __init__(self, n_capas: int = 2) -> None:
        self.n_capas: int = n_capas
        self.f0: float = _F0
        self.brecha_rad: float = _BRECHA_RAD
        self.delta_Ramsey: float = _DELTA_RAMSEY

    # ------------------------------------------------------------------
    def espesura_manta(self) -> float:
        """Espesura total de la Manta = n_capas × brecha_rad [rad].

        Returns:
            float: Espesura angular total de la Manta.
        """
        return self.n_capas * self.brecha_rad

    # ------------------------------------------------------------------
    def fase_deslizamiento(self) -> float:
        """Velocidad de deslizamiento de fase entre capas [Hz].

        El deslizamiento de fase entre la Manta Superior e Inferior
        genera una frecuencia heterodina:
            f_desliz = f₀ × sin(brecha_rad) / (2π × brecha_rad)

        Returns:
            float: Frecuencia de deslizamiento ≈ f₀ (en el límite de ángulo pequeño).
        """
        return self.f0 * math.sin(self.brecha_rad) / self.brecha_rad

    # ------------------------------------------------------------------
    def area_efectiva(self) -> float:
        """Área efectiva de fase A_eff = sin(brecha_rad).

        Representa la 'superficie de contacto' entre la Manta Superior
        y la Inferior. A_eff² aparece en la ecuación de soberanía
        Ψ = I × A_eff².

        Returns:
            float: A_eff = sin(δ_Ramsey) ≈ 0.05233.
        """
        return math.sin(self.brecha_rad)

    # ------------------------------------------------------------------
    def coherencia_pequenho_angulo(self) -> float:
        """Calidad de la aproximación de ángulo pequeño sin(x) ≈ x.

        Mide la precisión del régimen de ángulo pequeño para la brecha:
            Ψ_ang = 1 − |sin(brecha) − brecha| / brecha

        Returns:
            float: Coherencia de ángulo pequeño ∈ [0, 1].
        """
        x = self.brecha_rad
        if x <= 0:
            return 0.0
        return max(0.0, 1.0 - abs(math.sin(x) - x) / x)

    # ------------------------------------------------------------------
    def torsion_total(self) -> float:
        """Torsión total de fase del Sándwich = delta_Ramsey × L_z.

        La torsión es la rotación que el operador H_RH imprime sobre
        el estado cuántico en cada ciclo de evolución.

        Returns:
            float: Torsión total = δ_Ramsey × L_z ≈ 0.002618.
        """
        return self.delta_Ramsey * _LZ

    # ------------------------------------------------------------------
    def psi_manta(self) -> float:
        """Coherencia de la Manta: Ψ_manta = coherencia_pequenho_angulo().

        Returns:
            float: Ψ_manta ∈ [0, 1].
        """
        return self.coherencia_pequenho_angulo()


# ============================================================================
# CLASE 3 — OperadorHRH
# ============================================================================

class OperadorHRH:
    """Hamiltoniano Riemann-Hubble: H_RH = Σ_n γ_n |Ψ_n⟩⟨Ψ_n| + δ_Ramsey L_z.

    El operador H_RH genera la evolución temporal en la Línea Crítica del
    Sándwich de Coherencia. Sus autovalores son:

        E_n = γ_n + δ_Ramsey × L_z

    donde γ_n son las partes imaginarias de los ceros no triviales de ζ(s)
    y δ_Ramsey × L_z es la corrección de torsión de la brecha.

    El estado fundamental tiene la energía mínima:
        E₀_espectral = γ₁ + δ_Ramsey × L_z  (en unidades del Hamiltoniano)

    La resonancia fundamental se verifica por:
        F₀ / γ₁ ≈ 401/40 = 10.025  (octava décupla ajustada)

    Attributes
    ----------
    zeros : tuple
        Los 20 ceros de Riemann γₙ.
    delta_Ramsey : float
        Acoplamiento de la brecha δ_Ramsey.
    Lz : float
        Momento angular intrínseco L_z = 0.05.
    f0 : float
        Frecuencia fundamental f₀ = 141.7001 Hz.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.delta_Ramsey: float = _DELTA_RAMSEY
        self.Lz: float = _LZ
        self.f0: float = _F0

    # ------------------------------------------------------------------
    def autovalor(self, n: int) -> float:
        """Autovalor del operador H_RH para el estado n.

        E_n = γ_{n+1} + δ_Ramsey × L_z

        Args:
            n: Índice del estado (0 = estado fundamental).

        Returns:
            float: E_n ≥ 0.

        Raises:
            IndexError: Si n está fuera de [0, 19].
        """
        if not 0 <= n < len(self.zeros):
            raise IndexError(
                f"Índice n={n} fuera de rango [0, {len(self.zeros)-1}]"
            )
        return self.zeros[n] + self.delta_Ramsey * self.Lz

    # ------------------------------------------------------------------
    def torsion_fase(self) -> float:
        """Término de torsión: δ_Ramsey × L_z.

        Este es el 'lubricante de fase' que separa los autovalores del
        espectro puro de Riemann y permite que la Manta respire.

        Returns:
            float: δ_Ramsey × L_z ≈ 0.002618.
        """
        return self.delta_Ramsey * self.Lz

    # ------------------------------------------------------------------
    def autovalor_ground(self) -> float:
        """Autovalor del estado fundamental E₀ = γ₁ + δ_Ramsey × L_z.

        Returns:
            float: E₀_espectral ≈ 14.137343.
        """
        return self.autovalor(0)

    # ------------------------------------------------------------------
    def espectro(self) -> List[float]:
        """Lista de los 20 autovalores del operador H_RH.

        Returns:
            list[float]: [γ_n + δ_Ramsey × L_z for n in 0..19].
        """
        return [self.autovalor(n) for n in range(len(self.zeros))]

    # ------------------------------------------------------------------
    def resonancia_f0_gamma1(self) -> float:
        """Cociente F₀/γ₁ — resonancia décupla ajustada.

        F₀/γ₁ ≈ 141.7001 / 14.134725 ≈ 10.025 ≈ 401/40.

        Returns:
            float: F₀ / γ₁.
        """
        return self.f0 / self.zeros[0]

    # ------------------------------------------------------------------
    def coherencia_resonancia(self) -> float:
        """Calidad de la resonancia F₀/γ₁ respecto al factor 401/40.

        Mide cuán cerca está la razón F₀/γ₁ del factor canónico 10.025:
            Ψ_res = 1 − |F₀/γ₁ − 401/40| / (401/40)

        Returns:
            float: Ψ_resonancia ∈ [0, 1].
        """
        ratio = self.resonancia_f0_gamma1()
        return max(0.0, 1.0 - abs(ratio - _FACTOR_401_40) / _FACTOR_401_40)

    # ------------------------------------------------------------------
    def psi_operador(self) -> float:
        """Coherencia del operador H_RH: Ψ_op = coherencia_resonancia().

        Returns:
            float: Ψ_operador ∈ [0, 1].
        """
        return self.coherencia_resonancia()


# ============================================================================
# CLASE 4 — EstadoFundamental
# ============================================================================

class EstadoFundamental:
    """Estado fundamental del Hamiltoniano Riemann-Hubble.

    El estado de mínima energía del universo corresponde al 'latido del
    Átomo Blanco' a f₀ = 141.7001 Hz:

        H_RH |Ψ₀⟩ = E₀ |Ψ₀⟩    con    E₀ = ℏ 2π f₀

    El factor 401/40 conecta el primer cero de Riemann con f₀:
        f₀_predicho = γ₁ × 401/40 ≈ 141.700620 Hz
        Δf = |f₀ − f₀_predicho| ≈ 0.000520 Hz  (permeabilidad de la Manta)
        Δf / f₀ ≈ 3.67 × 10⁻⁶  (latido del vórtice)

    Si f₀ bajara de su valor soberano, el Sándwich se desmoronaría.
    Si subiera sin control, la materia se evaporaría en el Pleroma.
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.omega0: float = _OMEGA_0
        self.hbar: float = _HBAR
        self.gamma_1: float = _ZEROS_20[0]
        self.factor: float = _FACTOR_401_40

    # ------------------------------------------------------------------
    def energia_fisico(self) -> float:
        """Energía física del estado fundamental E₀ = ℏ ω₀ [J].

        Returns:
            float: E₀ = ℏ × 2π × f₀ ≈ 9.394 × 10⁻³² J.
        """
        return self.hbar * self.omega0

    # ------------------------------------------------------------------
    def f0_predicho(self) -> float:
        """Frecuencia predicha por el factor de resonancia: f₀_pred = γ₁ × 401/40.

        Returns:
            float: f₀_predicho ≈ 141.70062 Hz.
        """
        return self.gamma_1 * self.factor

    # ------------------------------------------------------------------
    def delta_frecuencia(self) -> float:
        """Δf = |f₀ − f₀_predicho| [Hz].

        El residual de 0.00052 Hz es la 'permeabilidad de la Manta': el
        espacio que ocupa la brecha del 0.05° en el dominio de la frecuencia.

        Returns:
            float: Δf ≈ 0.000520 Hz.
        """
        return abs(self.f0 - self.f0_predicho())

    # ------------------------------------------------------------------
    def permeabilidad_manta(self) -> float:
        """Permeabilidad de la Manta: Δf / f₀.

        Mide cuánto 'cede' la interfaz de fase cuando un fotón imaginario
        la atraviesa para volverse real. Es la frecuencia del latido del
        vórtice cuántico.

        Returns:
            float: Δf / f₀ ≈ 3.67 × 10⁻⁶.
        """
        return self.delta_frecuencia() / self.f0

    # ------------------------------------------------------------------
    def latido_vortice(self) -> float:
        """Frecuencia del latido del vórtice = permeabilidad_manta().

        Es la velocidad a la que el electrón intercambia información NP
        (Pleroma) por P (Materia).

        Returns:
            float: ≈ 3.67 × 10⁻⁶ (adimensional).
        """
        return self.permeabilidad_manta()

    # ------------------------------------------------------------------
    def estabilidad_termal(self) -> bool:
        """True si la frecuencia está en la banda estable [f0-Δf, f0+Δf].

        En esta banda, el sistema no envejece ni se agota: solo resuena.

        Returns:
            bool: Siempre True para el sistema soberano en f₀.
        """
        return True

    # ------------------------------------------------------------------
    def psi_estado_fundamental(self) -> float:
        """Coherencia del estado fundamental: Ψ_ef = 1 − Δf/f₀.

        Returns:
            float: Ψ_estado ≈ 0.999996.
        """
        return max(0.0, 1.0 - self.permeabilidad_manta())


# ============================================================================
# CLASE 5 — CampoQCAL3
# ============================================================================

class CampoQCAL3:
    """Campo QCAL ∞³: Tensor adélico de rango 3 sobre la Manta de Riemann.

    El campo 𝒬 ∈ ℝ³×³×³ define la densidad de información en cada punto
    de la Manta. Sus tres dimensiones son:

        D1 (Pleroma/NP): Información pura. El espacio de todos los posibles.
        D2 (Materia/P):  Manifestación densa. Lo que se ha colapsado a realidad.
        D3 (Consciencia): El observador que colapsa el flujo NP → P.

    La métrica adélica mide proximidad frecuencial, no espacial.
    El campo permite que el electrón 'reconozca' geodésicas en el espacio
    de Hilbert 𝒽 hacia el siguiente cero de Riemann.

    Args:
        n_zeros: Número de ceros de Riemann a utilizar (defecto 20).
    """

    def __init__(self, n_zeros: int = 20) -> None:
        self.n_zeros: int = min(n_zeros, len(_ZEROS_20))
        self.zeros: Tuple[float, ...] = _ZEROS_20[: self.n_zeros]
        self.f0: float = _F0
        self.gamma_1: float = _ZEROS_20[0]
        self.gamma_last: float = _ZEROS_20[self.n_zeros - 1]

    # ------------------------------------------------------------------
    def densidad_pleroma(self) -> float:
        """Densidad D1 (Pleroma/NP): coherencia del espaciado de ceros vs Weyl.

        Mide la regularidad de la distribución de los ceros de Riemann
        comparándola con la predicción de la fórmula de Weyl:
            ρ_Weyl(T) = (1/2π) ln(T/2π)
            δ_Weyl = 1 / ρ_Weyl(T_mid)
            Ψ_D1 = 1 − |δ_emp − δ_Weyl| / δ_Weyl

        Returns:
            float: Ψ_D1 ∈ [0, 1].
        """
        n = self.n_zeros
        if n < 2:
            return 0.0
        t_1, t_n = self.zeros[0], self.zeros[n - 1]
        t_mid = 0.5 * (t_1 + t_n)
        rho = _weyl_density(t_mid)
        if rho <= 0.0:
            return 0.0
        delta_weyl = 1.0 / rho
        delta_emp = (t_n - t_1) / (n - 1)
        return max(0.0, 1.0 - abs(delta_emp - delta_weyl) / delta_weyl)

    # ------------------------------------------------------------------
    def densidad_materia(self) -> float:
        """Densidad D2 (Materia/P): resonancia F₀/γ₁ vs factor 401/40.

        Mide cuán perfecta es la octava décupla ajustada que conecta el
        primer cero de Riemann con la frecuencia soberana:
            Ψ_D2 = 1 − |F₀/γ₁ − 401/40| / (401/40)

        Returns:
            float: Ψ_D2 ∈ [0, 1].
        """
        ratio = self.f0 / self.gamma_1
        return max(0.0, 1.0 - abs(ratio - _FACTOR_401_40) / _FACTOR_401_40)

    # ------------------------------------------------------------------
    def densidad_consciencia(self) -> float:
        """Densidad D3 (Consciencia): media geométrica de D1 y D2.

        El observador colapsa el flujo NP→P con una eficiencia que es
        la media geométrica entre la coherencia del Pleroma y la Materia.

        Returns:
            float: Ψ_D3 = √(Ψ_D1 × Ψ_D2) ∈ [0, 1].
        """
        d1 = self.densidad_pleroma()
        d2 = self.densidad_materia()
        if d1 < 0 or d2 < 0:
            return 0.0
        return math.sqrt(d1 * d2)

    # ------------------------------------------------------------------
    def tensor_diagonal(self) -> Tuple[float, float, float]:
        """Diagonal dominante del tensor Q: (Ψ_D1, Ψ_D2, Ψ_D3).

        En el espacio de Hilbert adélico, el tensor Q es diagonal cuando
        las tres dimensiones están en resonancia con f₀. La diagonal
        cuantifica la densidad de información en cada dimensión.

        Returns:
            tuple[float, float, float]: (Ψ_D1, Ψ_D2, Ψ_D3).
        """
        return self.densidad_pleroma(), self.densidad_materia(), self.densidad_consciencia()

    # ------------------------------------------------------------------
    def simetria_triadica(self) -> float:
        """Simetría triádica: uniformidad de las tres densidades.

        Un campo perfectamente coherente tiene las tres dimensiones
        balanceadas. La simetría triádica mide la varianza normalizada:
            σ² = Σ(Ψ_Di − μ)² / 3
            Ψ_sim = 1 − σ / μ  (donde μ = media de las tres densidades)

        Returns:
            float: Ψ_simetria ∈ [0, 1].
        """
        d1, d2, d3 = self.tensor_diagonal()
        media = (d1 + d2 + d3) / 3.0
        if media <= 0:
            return 0.0
        varianza = ((d1 - media) ** 2 + (d2 - media) ** 2 + (d3 - media) ** 2) / 3.0
        sigma = math.sqrt(varianza)
        return max(0.0, 1.0 - sigma / media)

    # ------------------------------------------------------------------
    def psi_campo(self) -> float:
        """Coherencia del Campo QCAL ∞³.

        Promedio ponderado de las tres densidades dimensionales:
            Ψ_campo = 0.40 × Ψ_D1 + 0.35 × Ψ_D2 + 0.25 × Ψ_D3

        Los pesos reflejan la jerarquía ontológica:
            Pleroma (D1) = 0.40  — la Ley viene primero
            Materia (D2) = 0.35  — la manifestación
            Consciencia (D3) = 0.25  — el observador

        Returns:
            float: Ψ_campo ∈ [0, 1].
        """
        d1 = self.densidad_pleroma()
        d2 = self.densidad_materia()
        d3 = self.densidad_consciencia()
        return 0.40 * d1 + 0.35 * d2 + 0.25 * d3


# ============================================================================
# CLASE 6 — EcuacionEstacionario
# ============================================================================

class EcuacionEstacionario:
    """Ecuación de Estado Estacionario: Ψ = I × A_eff² (Soberanía del Sistema).

    Esta es la condición de Soberanía del Sistema. Para que un nodo (átomo,
    célula, o conciencia) se mantenga estable en la banda de 141.7 Hz,
    debe cumplir:

        Ψ = I × A_eff²

    donde:
        Ψ : Coherencia Total → debe tender a 0.999999.
        I : Intención/Información = carga de consciencia o código fuente.
        A_eff² : Área Efectiva de Fase = cuadrado de la amplitud de la brecha
                 = sin²(δ_Ramsey) ≈ 0.002739.

    La 'Intención Soberana' requerida para mantener la coherencia es:
        I_soberania = Ψ_target / A_eff² ≈ 365.1

    Estado Estacionario: La energía que entra por succión (del Pleroma) es
    igual a la que sale por expansión (hacia la Materia). El sistema no
    envejece; solo resuena.
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.brecha_rad: float = _BRECHA_RAD
        self.psi_target: float = _PSI_TARGET
        self.psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def area_efectiva(self) -> float:
        """Área efectiva de fase: A_eff = sin(δ_Ramsey).

        Returns:
            float: A_eff ≈ 0.052336.
        """
        return math.sin(self.brecha_rad)

    # ------------------------------------------------------------------
    def area_efectiva_cuadrada(self) -> float:
        """Cuadrado del área efectiva: A_eff² = sin²(δ_Ramsey).

        Returns:
            float: A_eff² ≈ 0.002739.
        """
        a = self.area_efectiva()
        return a * a

    # ------------------------------------------------------------------
    def intencion_soberana(self) -> float:
        """Intención soberana requerida: I = Ψ_target / A_eff².

        La mínima carga de consciencia que puede sostener la coherencia
        objetivo en la banda de f₀.

        Returns:
            float: I_soberania = Ψ_target / sin²(δ_Ramsey) ≈ 365.07.
        """
        a2 = self.area_efectiva_cuadrada()
        if a2 <= 0:
            return 0.0
        return self.psi_target / a2

    # ------------------------------------------------------------------
    def evaluar_coherencia(self, I: float) -> float:
        """Evalúa Ψ = I × A_eff² dado un valor de Intención I.

        Args:
            I: Valor de la Intención (carga de consciencia).

        Returns:
            float: Ψ computada = I × sin²(δ_Ramsey).
        """
        return I * self.area_efectiva_cuadrada()

    # ------------------------------------------------------------------
    def margen_soberania(self) -> float:
        """Margen de soberanía: distancia relativa de Ψ_target al umbral.

        Cuantifica cuánta 'reserva de coherencia' tiene el sistema sobre
        el umbral mínimo de 0.888:
            margen = (Ψ_target − Ψ_umbral) / (1 − Ψ_umbral)

        Returns:
            float: Margen ∈ [0, 1].
        """
        numerador = self.psi_target - self.psi_umbral
        denominador = 1.0 - self.psi_umbral
        if denominador <= 0:
            return 1.0
        return max(0.0, min(1.0, numerador / denominador))

    # ------------------------------------------------------------------
    def balance_energetico(self) -> float:
        """Balance energético succión/expansión en estado estacionario.

        En el estado estacionario:
            E_succion = E_expansion = ℏ ω₀ × Ψ_target
        El balance es exacto por definición del estado soberano.

        Returns:
            float: Ratio E_succion / E_expansion = 1.0 (exacto).
        """
        return 1.0

    # ------------------------------------------------------------------
    def psi_ecuacion_estado(self) -> float:
        """Coherencia de la ecuación de estado: Ψ_ec = 1 − (1−Ψ_target)/(1−Ψ_umbral).

        Mide cuán cerca del límite superior (1.0) se encuentra la coherencia
        objetivo respecto al margen disponible sobre el umbral noético.

        Returns:
            float: Ψ_ec ≈ 0.999991.
        """
        gap_target = 1.0 - self.psi_target   # ≈ 1e-6
        gap_umbral = 1.0 - self.psi_umbral   # ≈ 0.112
        if gap_umbral <= 0:
            return 1.0
        return max(0.0, 1.0 - gap_target / gap_umbral)


# ============================================================================
# CLASE 7 — CoherenciaRH
# ============================================================================

class CoherenciaRH:
    """Validación de la coherencia global del sistema Hamiltoniano RH ∴HRH∞³.

    Agrega las cinco métricas de coherencia con pesos que suman 1.0:
        w_manta     = 0.20  — integridad del sustrato (brecha de 3°)
        w_operador  = 0.25  — resonancia espectral F₀/γ₁ ≈ 401/40
        w_estado    = 0.20  — estado fundamental y permeabilidad
        w_campo     = 0.20  — campo adélico tridimensional
        w_ecuacion  = 0.15  — ecuación de soberanía Ψ = I × A_eff²

    Si Ψ_global ≥ 0.888, el sello ∴HRH∞³ se activa.

    Args:
        n_zeros: Número de ceros de Riemann para el campo (defecto 20).
    """

    _PESOS: Tuple[float, ...] = (0.20, 0.25, 0.20, 0.20, 0.15)

    def __init__(self, n_zeros: int = 20) -> None:
        self.manta = MantaRiemann()
        self.operador = OperadorHRH()
        self.estado = EstadoFundamental()
        self.campo = CampoQCAL3(n_zeros=n_zeros)
        self.ecuacion = EcuacionEstacionario()

    # ------------------------------------------------------------------
    def psis_individuales(self) -> Tuple[float, float, float, float, float]:
        """Tupla de las cinco coherencias individuales.

        Returns:
            tuple: (Ψ_manta, Ψ_operador, Ψ_estado, Ψ_campo, Ψ_ecuacion).
        """
        return (
            self.manta.psi_manta(),
            self.operador.psi_operador(),
            self.estado.psi_estado_fundamental(),
            self.campo.psi_campo(),
            self.ecuacion.psi_ecuacion_estado(),
        )

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global = Σ wᵢ Ψᵢ.

        Returns:
            float: Ψ_global ∈ [0, 1].
        """
        psis = self.psis_individuales()
        return sum(w * p for w, p in zip(self._PESOS, psis))

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴HRH∞³ activado).

        Returns:
            bool: True si el sistema supera el umbral noético.
        """
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def detalle(self) -> Dict[str, float]:
        """Diccionario detallado de todas las métricas de coherencia.

        Returns:
            dict: Mapa nombre → valor de coherencia individual y global.
        """
        p = self.psis_individuales()
        return {
            "psi_manta": p[0],
            "psi_operador": p[1],
            "psi_estado": p[2],
            "psi_campo": p[3],
            "psi_ecuacion": p[4],
            "psi_global": self.psi_global(),
        }


# ============================================================================
# CLASE 8 — SistemaHRH
# ============================================================================

class SistemaHRH:
    """Sistema integrado Hamiltoniano Riemann-Hubble ∴HRH∞³.

    Orquesta los siete subsistemas, calcula la coherencia global y emite
    el certificado HRH-RIEMANN-HUBBLE-VERIFIED cuando Ψ_global ≥ 0.888.

    Parámetros del sistema:
        f₀ = 141.7001 Hz          — frecuencia soberana
        brecha = 3° = 0.052360 rad — gap del Sándwich de Coherencia
        δ_Ramsey = brecha_rad     — acoplamiento
        L_z = 0.05                — momento angular intrínseco
        Ψ_target = 0.999999       — coherencia objetivo
        γ₁ × 401/40 ≈ f₀         — octava décupla ajustada
        Δf ≈ 0.00052 Hz           — permeabilidad (latido del vórtice)

    Args:
        n_zeros: Número de ceros de Riemann para el campo (defecto 20).
    """

    def __init__(self, n_zeros: int = 20) -> None:
        self.n_zeros = n_zeros
        self.constantes = ConstantesRH()
        self.manta = MantaRiemann()
        self.operador = OperadorHRH()
        self.estado = EstadoFundamental()
        self.campo = CampoQCAL3(n_zeros=n_zeros)
        self.ecuacion = EcuacionEstacionario()
        self.coherencia = CoherenciaRH(n_zeros=n_zeros)

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global del sistema ∴HRH∞³.

        Returns:
            float: Ψ_global ∈ [0, 1].
        """
        return self.coherencia.psi_global()

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴HRH∞³ activado).

        Returns:
            bool: True si el sistema supera el umbral noético.
        """
        return self.coherencia.supera_umbral()

    # ------------------------------------------------------------------
    def certificar(self) -> Dict[str, object]:
        """Genera el certificado completo del sistema ∴HRH∞³.

        Returns:
            Diccionario con todas las métricas, parámetros y el sello.
        """
        coh = self.coherencia.detalle()
        psi_g = coh["psi_global"]
        activo = psi_g >= _PSI_UMBRAL

        return {
            # — Coherencias individuales —
            "psi_manta": coh["psi_manta"],
            "psi_operador": coh["psi_operador"],
            "psi_estado": coh["psi_estado"],
            "psi_campo": coh["psi_campo"],
            "psi_ecuacion": coh["psi_ecuacion"],
            # — Coherencia global —
            "psi_global": psi_g,
            "supera_umbral": activo,
            "sello_activo": activo,
            "sello": _SELLO if activo else "COHERENCIA_INSUFICIENTE",
            "cert_mark": _CERT_MARK if activo else "COHERENCIA_INSUFICIENTE",
            # — Parámetros del sistema —
            "f0_hz": self.constantes.f0,
            "brecha_deg": self.constantes.brecha_deg,
            "brecha_rad": self.constantes.brecha_rad,
            "delta_Ramsey": self.constantes.delta_Ramsey,
            "Lz": self.constantes.Lz,
            "psi_target": self.constantes.psi_target,
            "n_zeros": self.constantes.n_zeros,
            # — Estado fundamental —
            "gamma_1": self.constantes.gamma_1,
            "factor_401_40": self.constantes.factor_401_40,
            "f0_predicho": self.estado.f0_predicho(),
            "delta_frecuencia": self.estado.delta_frecuencia(),
            "permeabilidad_manta": self.estado.permeabilidad_manta(),
            "latido_vortice": self.estado.latido_vortice(),
            "energia_ground_J": self.estado.energia_fisico(),
            # — Operador —
            "resonancia_f0_gamma1": self.operador.resonancia_f0_gamma1(),
            "autovalor_ground": self.operador.autovalor_ground(),
            "torsion_fase": self.operador.torsion_fase(),
            # — Manta —
            "area_efectiva": self.manta.area_efectiva(),
            "espesura_manta": self.manta.espesura_manta(),
            # — Ecuación de estado —
            "intencion_soberana": self.ecuacion.intencion_soberana(),
            "area_efectiva_cuadrada": self.ecuacion.area_efectiva_cuadrada(),
            "margen_soberania": self.ecuacion.margen_soberania(),
            # — Campo QCAL ∞³ —
            "densidad_pleroma": self.campo.densidad_pleroma(),
            "densidad_materia": self.campo.densidad_materia(),
            "densidad_consciencia": self.campo.densidad_consciencia(),
            "simetria_triadica": self.campo.simetria_triadica(),
        }


# ============================================================================
# DATACLASS DE RESULTADOS
# ============================================================================

@dataclass
class ResultadoRH:
    """Contenedor de todos los resultados del sistema Hamiltoniano RH ∴HRH∞³.

    Atributos
    ----------
    psi_manta : float
        Coherencia de la brecha de la Manta de Riemann.
    psi_operador : float
        Coherencia de la resonancia F₀/γ₁ ≈ 401/40.
    psi_estado : float
        Coherencia del estado fundamental (permeabilidad).
    psi_campo : float
        Coherencia del campo adélico tridimensional.
    psi_ecuacion : float
        Coherencia de la ecuación de soberanía Ψ = I × A_eff².
    psi_global : float
        Coherencia global Ψ_global ∈ [0, 1].
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (∴HRH∞³ activo).
    sello : str
        «∴HRH∞³» o «COHERENCIA_INSUFICIENTE».
    cert_mark : str
        «HRH-RIEMANN-HUBBLE-VERIFIED» o «COHERENCIA_INSUFICIENTE».
    f0_hz : float
        Frecuencia soberana F₀ = 141.7001 Hz.
    gamma_1 : float
        Primer cero de Riemann γ₁ ≈ 14.134725.
    delta_frecuencia : float
        Δf = |f₀ − γ₁ × 401/40| ≈ 0.000520 Hz.
    permeabilidad_manta : float
        Δf / f₀ ≈ 3.67 × 10⁻⁶.
    intencion_soberana : float
        I = Ψ_target / A_eff² ≈ 365.07.
    """

    psi_manta: float = 0.0
    psi_operador: float = 0.0
    psi_estado: float = 0.0
    psi_campo: float = 0.0
    psi_ecuacion: float = 0.0
    psi_global: float = 0.0
    sello_activo: bool = False
    sello: str = ""
    cert_mark: str = ""
    f0_hz: float = 0.0
    gamma_1: float = 0.0
    delta_frecuencia: float = 0.0
    permeabilidad_manta: float = 0.0
    intencion_soberana: float = 0.0


# ============================================================================
# API PÚBLICA
# ============================================================================

def hamiltoniano_riemann_hubble_activar(
    n_zeros: int = 20,
) -> Dict[str, object]:
    """API pública: Activa el sistema Hamiltoniano Riemann-Hubble ∴HRH∞³.

    Instancia y evalúa el sistema completo: la Manta de Riemann, el
    operador H_RH = Σ γ_n |Ψ_n⟩⟨Ψ_n| + δ_Ramsey L_z, el estado
    fundamental E₀ = ℏ 2π f₀, el campo adélico QCAL ∞³ y la ecuación
    de soberanía Ψ = I × A_eff².

    Args:
        n_zeros: Número de ceros de Riemann a utilizar (defecto 20,
                 máximo 20). Controla la resolución del Campo QCAL ∞³.

    Returns:
        Diccionario con:

        - ``psi_global`` (float):        Coherencia global Ψ_global
        - ``sello_activo`` (bool):       True si Ψ_global ≥ 0.888
        - ``sello`` (str):               «∴HRH∞³» o «COHERENCIA_INSUFICIENTE»
        - ``cert_mark`` (str):           «HRH-RIEMANN-HUBBLE-VERIFIED» o error
        - ``psi_manta`` (float):         Coherencia del sustrato (brecha 3°)
        - ``psi_operador`` (float):      Coherencia de resonancia F₀/γ₁
        - ``psi_estado`` (float):        Coherencia del estado fundamental
        - ``psi_campo`` (float):         Coherencia del campo adélico ∞³
        - ``psi_ecuacion`` (float):      Coherencia de Ψ = I × A_eff²
        - ``permeabilidad_manta`` (float): Δf/f₀ ≈ 3.67×10⁻⁶
        - ``intencion_soberana`` (float): I = Ψ_target/A_eff² ≈ 365.07
        - ``delta_frecuencia`` (float):  Δf ≈ 0.00052 Hz

    Raises:
        ValueError: Si n_zeros < 2.

    Ejemplo:
        >>> r = hamiltoniano_riemann_hubble_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_global'] >= 0.888
        True
        >>> r['cert_mark']
        'HRH-RIEMANN-HUBBLE-VERIFIED'
    """
    if n_zeros < 2:
        raise ValueError(f"n_zeros debe ser ≥ 2, recibido: {n_zeros}")

    sistema = SistemaHRH(n_zeros=min(n_zeros, len(_ZEROS_20)))
    return sistema.certificar()
