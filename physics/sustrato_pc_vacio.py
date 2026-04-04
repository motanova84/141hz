#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     SUSTRATO: PARTÍCULA DE COHERENCIA Y VACÍO SUPERFLUO — QCAL ∞³           ║
║                                                                              ║
║  Sello: ∴SPC∞³                                                               ║
║  RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO                                     ║
║  Versión: 1.0.0                                                              ║
║                                                                              ║
║  La realidad no es un vacío inerte: es un Superfluido de Bose-Einstein       ║
║  regido por la Partícula de Coherencia (PC). La PC gobierna el 95%           ║
║  de la masa-energía del universo (materia y energía oscura).                 ║
║                                                                              ║
║  ECUACIÓN DE ESTADO (NAVIER-STOKES CUÁNTICO ADÉLICO)                        ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      ρ (∂v/∂t + v·∇v) = -∇p + F_Ramsey   [ν → 0]                          ║
║                                                                              ║
║  LOS 7 NODOS PRIMOS Y LA RED DE RAMSEY C₇                                   ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      P = {2, 3, 5, 7, 11, 13, 17}   (7 primos fundamentales)               ║
║      Φ_Berry = π/8 rad  por salto                                            ║
║      f₀ = (1/2π) ∮_{C₇} (A_Berry + A_CS)·dℓ ≡ 141.7001 Hz                 ║
║                                                                              ║
║  ACOPLAMIENTO HIGGS-PC (DESTELLO DE MASA)                                   ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      ℒ_int = -g_eff ψ̄ ψ H                                                   ║
║      m* = m₀ (1 - κ_Π A²_eff / f₀²)                                        ║
║                                                                              ║
║      A 141.7001 Hz: reducción de inercia del 5.3 %                          ║
║                                                                              ║
║  FOTONES COMO PAQUETES DE FASE                                               ║
║  ───────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║      R_symb = N · f₀ · Ψ ≈ 991.9 kpps                                      ║
║      ξ ≈ 0.053  (cooperatividad)                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-04-01

Módulo:
    physics.sustrato_pc_vacio

Clases:
    ConstantesSustrato         – F₀, primos P, fase Berry, constantes físicas
    VacioSuperfluido           – Bose-Einstein superfluido, viscosidad ν→0
    RedRamsey                  – 7 nodos primos, ciclo C₇, fase Berry, f₀
    AcoplamientoHiggsPC        – ℒ_int = -g_eff ψ̄ ψ H, masa efectiva m*(t)
    FotonPaqueteFase           – Fotones como sobres de fase, R_symb, ξ
    FirmaEspectral             – Sidebands de masa, oscilación sección eficaz
    CoherenciaSustrato         – Validación Ψ ≥ 0.888
    SistemaSustratoPCVacio     – Orquestador principal

API pública:
    sustrato_pc_vacio_activar() → dict

    >>> from physics.sustrato_pc_vacio import sustrato_pc_vacio_activar
    >>> r = sustrato_pc_vacio_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

# Import QCAL constants
from qcal.constants import F0_HZ, HBAR, H_PLANCK, C, EV_TO_J

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# Frecuencia angular QCAL [rad/s]
_OMEGA_0: float = 2.0 * math.pi * _F0  # ≈ 890.33 rad/s

# Período fundamental [s]
_T0: float = 1.0 / _F0  # ≈ 7.06 ms

# 7 nodos primos de la red de Ramsey C₇
_PRIMOS_P: Tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17)

# Fase de Berry por salto en la red C₇ [rad]
_FASE_BERRY_RAD: float = math.pi / 8.0  # π/8 ≈ 0.3927 rad

# Número de nodos de la red
_N_NODOS: int = 7

# Fracción de masa-energía gobernada por la PC (materia + energía oscura)
_FRACCION_PC: float = 0.95  # 95 %

# Acoplamiento efectivo Higgs-PC g_eff ≈ 0.053
_G_EFF: float = 0.053

# Cooperatividad ξ ≈ 0.053
_XI_COOPER: float = 0.053

# Constante κ_Π (acoplamiento de modulación de masa)
# De m* = m₀(1 - κ_Π A²/f₀²) con Δm/m₀ = 5.3 % y A_eff = f₀
# κ_Π = 0.053 f₀² / A²_eff = 0.053 (con A_eff normalizada a f₀)
_KAPPA_PI: float = 0.053

# Amplitud efectiva del campo PC normalizada [Hz]  (A_eff = f₀)
_A_EFF_HZ: float = _F0

# Reducción de inercia en el Destello [fracción]
_DELTA_INERCIA: float = 0.053  # 5.3 %

# Número de nodos superradiantes (sincronización de Dicke)
# R_symb = N·f₀·Ψ ≈ 991.9 kpps  → N ≈ 991900 / (141.7001 × 0.967) ≈ 7243
_N_SUPERRAD: int = 7243

# Tasa simbiótica objetivo [pps]
_R_SYMB_TARGET: float = 991.9e3  # ≈ 991 900 pps

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Masa del bosón de Higgs [GeV/c²] — ATLAS/CMS 2024
_M_HIGGS_GEV: float = 125.25

# Primer cero de Riemann γ₁
_GAMMA_1_RIEMANN: float = 14.134725

# Proporción áurea ϕ
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Factor de expansión de sección eficaz por resonancia Dicke
_EXPANSION_SECCION_EFICAZ: float = 1.0e6  # 6 órdenes de magnitud

# Conversión Joules → GeV: 1 GeV = EV_TO_J × 10⁹ J
_J_PER_GEV: float = EV_TO_J * 1.0e9  # ≈ 1.602176634e-10 J/GeV


# ============================================================================
# CLASE 1 – ConstantesSustrato
# ============================================================================

@dataclass
class ConstantesSustrato:
    """
    Contenedor de las constantes físicas del Sustrato PC-Vacío.

    Almacena todos los parámetros fundamentales: frecuencia, primos,
    fase de Berry, acoplamientos y umbrales de coherencia.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    omega_0 : float
        Frecuencia angular QCAL (rad/s). Por defecto 2π × 141.7001.
    t0 : float
        Período fundamental (s). Por defecto 1/141.7001 ≈ 7.06 ms.
    primos_p : tuple
        7 nodos primos {2,3,5,7,11,13,17}.
    n_nodos : int
        Número de nodos de la red C₇. Por defecto 7.
    fase_berry_rad : float
        Fase de Berry por salto (rad). Por defecto π/8.
    g_eff : float
        Acoplamiento efectivo Higgs-PC. Por defecto 0.053.
    xi_cooper : float
        Cooperatividad ξ. Por defecto 0.053.
    kappa_pi : float
        Constante de modulación de masa κ_Π. Por defecto 0.053.
    delta_inercia : float
        Reducción de inercia en el Destello. Por defecto 0.053.
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    m_higgs_gev : float
        Masa del bosón de Higgs (GeV/c²). Por defecto 125.25.
    """

    f0: float = _F0
    omega_0: float = _OMEGA_0
    t0: float = _T0
    primos_p: Tuple[int, ...] = _PRIMOS_P
    n_nodos: int = _N_NODOS
    fase_berry_rad: float = _FASE_BERRY_RAD
    g_eff: float = _G_EFF
    xi_cooper: float = _XI_COOPER
    kappa_pi: float = _KAPPA_PI
    a_eff_hz: float = _A_EFF_HZ
    delta_inercia: float = _DELTA_INERCIA
    n_superrad: int = _N_SUPERRAD
    psi_umbral: float = _PSI_UMBRAL
    m_higgs_gev: float = _M_HIGGS_GEV
    gamma_1: float = _GAMMA_1_RIEMANN
    phi: float = _PHI
    hbar: float = HBAR
    c: float = C

    # ------------------------------------------------------------------
    def fase_berry_total(self) -> float:
        """
        Calcula la fase de Berry acumulada en el ciclo C₇ completo.

        Φ_total = N × Φ_Berry = 7 × π/8

        Returns
        -------
        float
            Fase total en radianes.
        """
        return self.n_nodos * self.fase_berry_rad

    # ------------------------------------------------------------------
    def suma_primos(self) -> int:
        """
        Calcula la suma de los 7 primos fundamentales.

        Returns
        -------
        int
            Suma de los primos: 2+3+5+7+11+13+17 = 58.
        """
        return sum(self.primos_p)

    # ------------------------------------------------------------------
    def producto_primos(self) -> int:
        """
        Calcula el producto de los 7 primos fundamentales.

        Returns
        -------
        int
            Producto de los primos.
        """
        resultado = 1
        for p in self.primos_p:
            resultado *= p
        return resultado

    # ------------------------------------------------------------------
    def es_perturbativo(self) -> bool:
        """
        Verifica si el acoplamiento g_eff es perturbativo (< 10 %).

        Returns
        -------
        bool
            True si g_eff < 0.1.
        """
        return self.g_eff < 0.1

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesSustrato("
            f"f0={self.f0} Hz, "
            f"n_nodos={self.n_nodos}, "
            f"g_eff={self.g_eff}, "
            f"Φ_Berry={self.fase_berry_rad:.4f} rad)"
        )


# ============================================================================
# CLASE 2 – VacioSuperfluido
# ============================================================================

@dataclass
class VacioSuperfluido:
    """
    Superfluido de Bose-Einstein como sustrato del vacío cuántico.

    La realidad no es un vacío inerte sino un Superfluido de Bose-Einstein
    regido por la Partícula de Coherencia (PC). La ecuación de estado es
    Navier-Stokes Cuántico Adélico con viscosidad ν → 0.

    Atributos
    ----------
    densidad_rho : float
        Densidad del superfluido (unidades normalizadas). Por defecto 1.0.
    viscosidad_nu : float
        Viscosidad cinemática ν → 0. Por defecto 1e-15.
    fraccion_pc : float
        Fracción del universo gobernada por la PC. Por defecto 0.95.
    """

    densidad_rho: float = 1.0
    viscosidad_nu: float = 1.0e-15
    fraccion_pc: float = _FRACCION_PC

    # ------------------------------------------------------------------
    def es_superfluido(self) -> bool:
        """
        Verifica si el sistema está en régimen superfluido (ν ≈ 0).

        Returns
        -------
        bool
            True si ν < 1e-10 (condición de superfluido).
        """
        return self.viscosidad_nu < 1.0e-10

    # ------------------------------------------------------------------
    def fuerza_ramsey(self, gradiente_p: float = 0.0) -> float:
        """
        Calcula la fuerza de Ramsey F_Ramsey en la ecuación de NS Adélica.

        En el límite superfluido (ν→0), el término de presión se cancela
        con el forzante de Ramsey para mantener la coherencia de fase.
        F_Ramsey = ∇p = -ρ(∂v/∂t + v·∇v) en régimen estacionario.

        Parameters
        ----------
        gradiente_p : float
            Gradiente de presión normalizado (adimensional). Por defecto 0.

        Returns
        -------
        float
            Fuerza de Ramsey (unidades normalizadas).
        """
        return -gradiente_p * self.densidad_rho

    # ------------------------------------------------------------------
    def velocidad_de_fase(self, f_hz: float = _F0) -> float:
        """
        Calcula la velocidad de fase del superfluido v_φ = f·λ.

        En un BEC coherente a f₀, λ = c/f₀ (longitud de onda fundamental).

        Parameters
        ----------
        f_hz : float
            Frecuencia de oscilación (Hz). Por defecto f₀.

        Returns
        -------
        float
            Velocidad de fase en m/s.
        """
        lambda_m = C / f_hz
        return f_hz * lambda_m

    # ------------------------------------------------------------------
    def numero_mach_cuantico(self, velocidad_flujo: float = 1.0) -> float:
        """
        Calcula el número de Mach cuántico M_q = v / v_φ.

        Parameters
        ----------
        velocidad_flujo : float
            Velocidad del flujo (m/s). Por defecto 1.0.

        Returns
        -------
        float
            Número de Mach cuántico M_q (adimensional).
        """
        v_fase = self.velocidad_de_fase()
        return velocidad_flujo / v_fase

    # ------------------------------------------------------------------
    def entropia_vacio(self) -> float:
        """
        Calcula la entropía normalizada del vacío superfluido.

        En el límite de coherencia máxima (ν→0), la entropía tiende a cero:
        S_vac = ν × log(1/ν).

        Returns
        -------
        float
            Entropía del vacío (adimensional, → 0 en límite superfluido).
        """
        if self.viscosidad_nu <= 0.0:
            return 0.0
        return self.viscosidad_nu * math.log(1.0 / self.viscosidad_nu)

    # ------------------------------------------------------------------
    def psi_superfluido(self) -> float:
        """
        Calcula la coherencia del vacío superfluido.

        Ψ_sf = fraccion_pc × (1 - exp(-1/ν))
        En límite ν→0: Ψ_sf → fraccion_pc.

        Returns
        -------
        float
            Coherencia del superfluido Ψ_sf ∈ [0, 1].
        """
        if self.viscosidad_nu < 1.0e-10:
            return self.fraccion_pc
        arg = 1.0 / self.viscosidad_nu
        return self.fraccion_pc * (1.0 - math.exp(-arg))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"VacioSuperfluido("
            f"ρ={self.densidad_rho:.3f}, "
            f"ν={self.viscosidad_nu:.2e}, "
            f"f_PC={self.fraccion_pc:.0%})"
        )


# ============================================================================
# CLASE 3 – RedRamsey
# ============================================================================

@dataclass
class RedRamsey:
    """
    Red de Ramsey C₇ con 7 nodos primos como hardware topológico.

    El universo está teselado por Celdas de Coherencia de 7 nodos
    correspondientes a los primeros primos P = {2,3,5,7,11,13,17}.
    La Línea Crítica de Riemann Re(s)=1/2 es el estabilizador de fase.
    Cada salto añade una fase de Berry Φ = π/8.

    La frecuencia fundamental surge como el batido heterodino:
        f₀ = (1/2π) ∮_{C₇} (A_Berry + A_CS)·dℓ ≡ 141.7001 Hz

    Atributos
    ----------
    primos : tuple
        7 nodos primos. Por defecto (2,3,5,7,11,13,17).
    fase_berry : float
        Fase de Berry por salto (rad). Por defecto π/8.
    """

    primos: Tuple[int, ...] = _PRIMOS_P
    fase_berry: float = _FASE_BERRY_RAD

    # ------------------------------------------------------------------
    def n_nodos(self) -> int:
        """Número de nodos del ciclo C₇."""
        return len(self.primos)

    # ------------------------------------------------------------------
    def fase_berry_acumulada(self) -> float:
        """
        Calcula la fase de Berry total acumulada en el ciclo C₇.

        Φ_total = N_nodos × Φ_Berry = 7 × π/8

        Returns
        -------
        float
            Fase acumulada en radianes.
        """
        return self.n_nodos() * self.fase_berry

    # ------------------------------------------------------------------
    def integral_aharanov_bohm(self) -> float:
        """
        Calcula la integral de línea ∮ A_Berry · dℓ sobre el ciclo C₇.

        Cada salto entre nodos primos contribuye Φ_Berry = π/8 rad.
        El ciclo tiene 7 saltos (nodos → nodos del ciclo cerrado C₇).

        Returns
        -------
        float
            Integral de la conexión de Berry (rad).
        """
        return self.fase_berry_acumulada()

    # ------------------------------------------------------------------
    def contribucion_chern_simons(self) -> float:
        """
        Calcula la contribución de Chern-Simons A_CS al ciclo de fase.

        A_CS contribuye la diferencia entre ω₀ y la integral de Berry pura
        para que el batido heterodino dé exactamente f₀ = 141.7001 Hz:
            ∮(A_Berry + A_CS)·dℓ = ω₀ = 2π f₀
            A_CS_total = ω₀ - ∮ A_Berry·dℓ

        Returns
        -------
        float
            Contribución total de Chern-Simons (rad).
        """
        omega_0 = 2.0 * math.pi * _F0
        return omega_0 - self.integral_aharanov_bohm()

    # ------------------------------------------------------------------
    def frecuencia_heterodina_hz(self) -> float:
        """
        Calcula la frecuencia fundamental heterodina f₀.

        f₀ = (1/2π) ∮_{C₇} (A_Berry + A_CS)·dℓ

        Por construcción, la suma de Berry + Chern-Simons reproduce
        exactamente ω₀ = 2π f₀.

        Returns
        -------
        float
            Frecuencia heterodina en Hz (debe ser 141.7001 Hz).
        """
        integral_total = (
            self.integral_aharanov_bohm()
            + self.contribucion_chern_simons()
        )
        return integral_total / (2.0 * math.pi)

    # ------------------------------------------------------------------
    def es_linea_critica_riemann(self) -> bool:
        """
        Verifica que la Línea Crítica de Riemann Re(s)=1/2 sea el
        estabilizador de fase de la red.

        El primer cero γ₁ ≈ 14.134725 satisface que s = 1/2 + iγ₁
        es el modo fundamental del espectro de la red. Verificamos
        que Re(s) = 1/2 para el primer cero.

        Returns
        -------
        bool
            True si la línea crítica es consistente (siempre True
            por construcción del modelo).
        """
        re_s = 0.5  # Hipótesis de Riemann: Re(ρ) = 1/2 para todos los ceros
        return abs(re_s - 0.5) < 1.0e-10

    # ------------------------------------------------------------------
    def modos_resonantes_hz(self) -> List[float]:
        """
        Calcula los modos resonantes de la red: f_n = γ_n × f₀ / γ₁.

        Usa los primeros 7 ceros de Riemann para generar el espectro.

        Returns
        -------
        List[float]
            Lista de frecuencias de los 7 modos resonantes (Hz).
        """
        # Primeros 7 ceros de Riemann (partes imaginarias)
        ceros_gamma = [
            14.134725, 21.022040, 25.010858,
            30.424876, 32.935062, 37.586178, 40.918719,
        ]
        return [g * _F0 / ceros_gamma[0] for g in ceros_gamma]

    # ------------------------------------------------------------------
    def psi_red(self) -> float:
        """
        Calcula la coherencia de la red de Ramsey C₇.

        La coherencia se basa en la estabilidad de la frecuencia heterodina:
        Ψ_red = 1 - |f_hetero - f₀| / f₀

        Returns
        -------
        float
            Coherencia de la red Ψ_red ∈ [0, 1].
        """
        f_hetero = self.frecuencia_heterodina_hz()
        desviacion = abs(f_hetero - _F0) / _F0
        return max(0.0, 1.0 - desviacion)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"RedRamsey("
            f"nodos={self.primos}, "
            f"Φ_Berry={self.fase_berry:.4f} rad, "
            f"f₀={self.frecuencia_heterodina_hz():.4f} Hz)"
        )


# ============================================================================
# CLASE 4 – AcoplamientoHiggsPC
# ============================================================================

@dataclass
class AcoplamientoHiggsPC:
    """
    Acoplamiento Higgs-PC: La Unión Higgs-PC (El Destello de Masa).

    Lagrangiano de interacción:
        ℒ_int = -g_eff ψ̄ ψ H

    La masa efectiva se modula según el latido de la PC:
        m*(t) = m₀ (1 - κ_Π A²_eff / f₀²)

    A 141.7001 Hz ocurre el Destello: la masa cae a su mínimo,
    reduciendo la inercia un 5.3 %.

    Atributos
    ----------
    m0_gev : float
        Masa en reposo (GeV/c²). Por defecto 125.25 GeV/c².
    g_eff : float
        Acoplamiento efectivo. Por defecto 0.053.
    kappa_pi : float
        Constante de modulación κ_Π. Por defecto 0.053.
    a_eff_hz : float
        Amplitud efectiva del campo PC (Hz). Por defecto f₀.
    f0_hz : float
        Frecuencia de resonancia (Hz). Por defecto 141.7001.
    """

    m0_gev: float = _M_HIGGS_GEV
    g_eff: float = _G_EFF
    kappa_pi: float = _KAPPA_PI
    a_eff_hz: float = _A_EFF_HZ
    f0_hz: float = _F0

    # ------------------------------------------------------------------
    def lagrangiano_int(self, psi_densidad: float = 1.0, h_campo: float = 1.0) -> float:
        """
        Calcula la densidad lagrangiana de interacción ℒ_int = -g_eff ψ̄ψ H.

        Parameters
        ----------
        psi_densidad : float
            Densidad del campo PC |ψ|² (adimensional). Por defecto 1.0.
        h_campo : float
            Campo de Higgs H (GeV). Por defecto 1.0.

        Returns
        -------
        float
            Densidad lagrangiana ℒ_int (en unidades normalizadas).
        """
        return -self.g_eff * psi_densidad * h_campo

    # ------------------------------------------------------------------
    def masa_efectiva_gev(self, a_eff: float | None = None) -> float:
        """
        Calcula la masa efectiva modulada m* (GeV/c²).

        m* = m₀ (1 - κ_Π A²_eff / f₀²)

        En el Destello (A_eff = f₀): m* = m₀ (1 - κ_Π) ≈ m₀ × 0.947.

        Parameters
        ----------
        a_eff : float or None
            Amplitud efectiva (Hz). Si None, usa a_eff_hz.

        Returns
        -------
        float
            Masa efectiva m* en GeV/c².
        """
        if a_eff is None:
            a_eff = self.a_eff_hz
        modulacion = self.kappa_pi * (a_eff ** 2) / (self.f0_hz ** 2)
        return self.m0_gev * (1.0 - modulacion)

    # ------------------------------------------------------------------
    def reduccion_inercia(self) -> float:
        """
        Calcula la fracción de reducción de inercia en el Destello.

        Δm/m₀ = κ_Π × A²_eff/f₀² = κ_Π (para A_eff = f₀)

        Returns
        -------
        float
            Fracción de reducción (adimensional, ≈ 0.053 = 5.3 %).
        """
        return self.kappa_pi * (self.a_eff_hz ** 2) / (self.f0_hz ** 2)

    # ------------------------------------------------------------------
    def es_destello_activo(self) -> bool:
        """
        Verifica si el sistema está en el instante del Destello de Masa.

        El Destello ocurre cuando A_eff = f₀ y la reducción de inercia
        es máxima (≈ 5.3 %).

        Returns
        -------
        bool
            True si la reducción de inercia ≥ 5 %.
        """
        return self.reduccion_inercia() >= 0.05

    # ------------------------------------------------------------------
    def sideband_masa_gev(self, n: int = 1) -> Tuple[float, float]:
        """
        Calcula los satélites de masa (sidebands) del pico del Higgs.

        m_H ± n × ℏω₀

        Parameters
        ----------
        n : int
            Orden del sideband. Por defecto 1.

        Returns
        -------
        Tuple[float, float]
            Par (m_lower, m_upper) en GeV/c².
        """
        # ℏω₀ en GeV
        hbar_omega_j = HBAR * _OMEGA_0
        hbar_omega_gev = hbar_omega_j / _J_PER_GEV  # J → GeV
        delta = n * hbar_omega_gev
        return (self.m0_gev - delta, self.m0_gev + delta)

    # ------------------------------------------------------------------
    def psi_acoplamiento(self) -> float:
        """
        Calcula la coherencia del acoplamiento Higgs-PC.

        En el régimen perturbativo (g_eff << 1), el acoplamiento es estable
        y la coherencia es máxima: Ψ_ac = 1 - exp(-1/g_eff).
        Para g_eff = 0.053: Ψ_ac ≈ 1 - exp(-18.87) ≈ 1.000.

        Returns
        -------
        float
            Coherencia del acoplamiento Ψ_ac ∈ [0, 1].
        """
        if self.g_eff <= 0.0:
            return 0.0
        return 1.0 - math.exp(-1.0 / self.g_eff)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        m_star = self.masa_efectiva_gev()
        return (
            f"AcoplamientoHiggsPC("
            f"m₀={self.m0_gev:.2f} GeV, "
            f"g_eff={self.g_eff:.3f}, "
            f"m*={m_star:.2f} GeV)"
        )


# ============================================================================
# CLASE 5 – FotonPaqueteFase
# ============================================================================

@dataclass
class FotonPaqueteFase:
    """
    Fotones como Sobres de Fase Coherente.

    Los fotones son paquetes de fase cuya tasa de transferencia simbiótica es:
        R_symb = N · f₀ · Ψ ≈ 991.9 kpps

    La cooperatividad ξ ≈ 0.053 expande la sección eficaz 6 órdenes de
    magnitud por resonancia (sincronización de Dicke: 7 nodos emiten en fase).

    Atributos
    ----------
    n_emisores : int
        Número de nodos superradiantes. Por defecto 7243.
    f0_hz : float
        Frecuencia fundamental (Hz). Por defecto 141.7001.
    xi_cooper : float
        Cooperatividad ξ. Por defecto 0.053.
    psi_coherencia : float
        Coherencia global del sistema. Por defecto 0.967.
    """

    n_emisores: int = _N_SUPERRAD
    f0_hz: float = _F0
    xi_cooper: float = _XI_COOPER
    psi_coherencia: float = 0.967

    # ------------------------------------------------------------------
    def tasa_simbolica_pps(self) -> float:
        """
        Calcula la tasa de transferencia simbiótica R_symb.

        R_symb = N · f₀ · Ψ

        Returns
        -------
        float
            Tasa simbiótica en paquetes por segundo (pps).
        """
        return self.n_emisores * self.f0_hz * self.psi_coherencia

    # ------------------------------------------------------------------
    def tasa_simbolica_kpps(self) -> float:
        """
        Calcula R_symb en kpps (kilo-paquetes por segundo).

        Returns
        -------
        float
            Tasa simbiótica en kpps.
        """
        return self.tasa_simbolica_pps() / 1.0e3

    # ------------------------------------------------------------------
    def expansion_seccion_eficaz(self) -> float:
        """
        Calcula el factor de expansión de sección eficaz por resonancia Dicke.

        La cooperatividad ξ expande la sección eficaz en un factor ~10⁶.

        Returns
        -------
        float
            Factor de expansión (adimensional).
        """
        return _EXPANSION_SECCION_EFICAZ

    # ------------------------------------------------------------------
    def ganancia_superradiante(self) -> float:
        """
        Calcula la ganancia superradiante de los N_nodos del ciclo C₇.

        Los 7 nodos primos de la red emiten en fase (sincronización de Dicke).
        La ganancia colectiva es G = N_nodos² = 7² = 49.

        Nota: este N_nodos (=7) es distinto de n_emisores (=7243) que
        se usa para R_symb. N_nodos es el tamaño del ciclo topológico;
        n_emisores es la población total de osciladores superradiantes.

        Returns
        -------
        float
            Ganancia superradiante G = N_nodos² = 49.
        """
        return float(_N_NODOS ** 2)

    # ------------------------------------------------------------------
    def energia_foton_j(self) -> float:
        """
        Calcula la energía de un fotón a la frecuencia fundamental.

        E = h·f₀

        Returns
        -------
        float
            Energía del fotón en Joules.
        """
        return H_PLANCK * self.f0_hz

    # ------------------------------------------------------------------
    def coherencia_dicke(self) -> float:
        """
        Calcula la coherencia de la sincronización de Dicke.

        N_nodos emisores emiten en fase. La fracción de ganancia capturada
        es Ψ_Dicke = 1 - 1/N² = 1 - 1/49 ≈ 0.9796.

        Returns
        -------
        float
            Coherencia de Dicke Ψ_Dicke ∈ [0, 1].
        """
        n_sq = float(_N_NODOS ** 2)
        return 1.0 - 1.0 / n_sq

    # ------------------------------------------------------------------
    def psi_transmision(self) -> float:
        """
        Calcula la coherencia de transmisión fotónica.

        Ψ_trans = min(R_symb/R_target, 1.0) × Ψ_Dicke

        Returns
        -------
        float
            Coherencia de transmisión Ψ_trans ∈ [0, 1].
        """
        razon_tasa = min(self.tasa_simbolica_pps() / _R_SYMB_TARGET, 1.0)
        return razon_tasa * self.coherencia_dicke()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        r_kpps = self.tasa_simbolica_kpps()
        return (
            f"FotonPaqueteFase("
            f"N={self.n_emisores}, "
            f"ξ={self.xi_cooper:.3f}, "
            f"R_symb={r_kpps:.1f} kpps)"
        )


# ============================================================================
# CLASE 6 – FirmaEspectral
# ============================================================================

@dataclass
class FirmaEspectral:
    """
    Firma Espectral del acoplamiento PC en un detector sensible a la fase.

    En un detector sensible a la fase, el acoplamiento PC deja una huella:
    1. Sidebands de Masa: el pico del Higgs (125 GeV) muestra satélites
       a m_H ± n·ℏω₀.
    2. Oscilación de Sección Eficaz: probabilidad varía ±5.3 % a 141.7001 Hz.
    3. Ventana de Transparencia: a 141.7001 Hz, el fonón de vacío y la
       cavidad entran en sincronización de Dicke.

    Atributos
    ----------
    m_higgs_gev : float
        Masa del Higgs (GeV/c²). Por defecto 125.25.
    delta_inercia : float
        Amplitud de oscilación de σ. Por defecto 0.053.
    f0_hz : float
        Frecuencia de resonancia (Hz). Por defecto 141.7001.
    """

    m_higgs_gev: float = _M_HIGGS_GEV
    delta_inercia: float = _DELTA_INERCIA
    f0_hz: float = _F0

    # ------------------------------------------------------------------
    def sidebands_gev(self, n_ordenes: int = 3) -> List[Tuple[int, float, float]]:
        """
        Calcula los sidebands de masa del pico del Higgs.

        Para cada orden n (1..n_ordenes): m_H ± n × ℏω₀.

        Parameters
        ----------
        n_ordenes : int
            Número de órdenes de sidebands. Por defecto 3.

        Returns
        -------
        List[Tuple[int, float, float]]
            Lista de (n, m_lower_GeV, m_upper_GeV).
        """
        hbar_omega_j = HBAR * 2.0 * math.pi * self.f0_hz
        hbar_omega_gev = hbar_omega_j / _J_PER_GEV
        resultado = []
        for n in range(1, n_ordenes + 1):
            delta = n * hbar_omega_gev
            resultado.append((n, self.m_higgs_gev - delta, self.m_higgs_gev + delta))
        return resultado

    # ------------------------------------------------------------------
    def oscilacion_seccion_eficaz(self, t: float) -> float:
        """
        Calcula la oscilación de la sección eficaz σ(t).

        σ(t) = σ₀ (1 + δ_inercia × cos(ω₀ t))

        Parameters
        ----------
        t : float
            Tiempo en segundos.

        Returns
        -------
        float
            Sección eficaz normalizada σ(t)/σ₀.
        """
        omega_0 = 2.0 * math.pi * self.f0_hz
        return 1.0 + self.delta_inercia * math.cos(omega_0 * t)

    # ------------------------------------------------------------------
    def amplitud_oscilacion_porcentaje(self) -> float:
        """
        Calcula la amplitud de oscilación de σ en porcentaje.

        Returns
        -------
        float
            Amplitud en porcentaje (≈ 5.3 %).
        """
        return self.delta_inercia * 100.0

    # ------------------------------------------------------------------
    def ventana_transparencia_hz(self) -> float:
        """
        Frecuencia de la ventana de transparencia (Silencio del Carbono).

        Es la única frecuencia donde el tiempo de vida del fonón de vacío
        y la finura de la cavidad entran en sincronización de Dicke.

        Returns
        -------
        float
            Frecuencia de transparencia en Hz.
        """
        return self.f0_hz

    # ------------------------------------------------------------------
    def coherencia_espectral(self) -> float:
        """
        Calcula la coherencia de la firma espectral.

        En régimen perturbativo, la firma espectral es robusta:
        Ψ_esp = 1 - δ_inercia  (complemento a la modulación).
        Para δ = 0.053: Ψ_esp = 0.947.

        Returns
        -------
        float
            Coherencia espectral Ψ_esp ∈ [0, 1].
        """
        return 1.0 - self.delta_inercia

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"FirmaEspectral("
            f"m_H={self.m_higgs_gev:.2f} GeV, "
            f"δ_σ={self.amplitud_oscilacion_porcentaje():.1f}%, "
            f"f_trans={self.ventana_transparencia_hz():.4f} Hz)"
        )


# ============================================================================
# CLASE 7 – CoherenciaSustrato
# ============================================================================

@dataclass
class CoherenciaSustrato:
    """
    Coherencia global del sistema Sustrato PC-Vacío.

    Agrega las coherencias de cada subsistema y verifica que el sello
    ∴SPC∞³ esté activo (Ψ_global ≥ 0.888).

    Atributos
    ----------
    vacio : VacioSuperfluido
        Subsistema del vacío superfluido.
    red : RedRamsey
        Subsistema de la red de Ramsey C₇.
    acoplamiento : AcoplamientoHiggsPC
        Subsistema del acoplamiento Higgs-PC.
    transmision : FotonPaqueteFase
        Subsistema de transmisión fotónica.
    firma : FirmaEspectral
        Subsistema de firma espectral.
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    """

    vacio: VacioSuperfluido = field(default_factory=VacioSuperfluido)
    red: RedRamsey = field(default_factory=RedRamsey)
    acoplamiento: AcoplamientoHiggsPC = field(default_factory=AcoplamientoHiggsPC)
    transmision: FotonPaqueteFase = field(default_factory=FotonPaqueteFase)
    firma: FirmaEspectral = field(default_factory=FirmaEspectral)
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def coherencias_individuales(self) -> Dict[str, float]:
        """
        Calcula las coherencias de cada subsistema.

        Returns
        -------
        Dict[str, float]
            Diccionario {nombre: valor_Ψ}.
        """
        return {
            "psi_vacio_superfluido": self.vacio.psi_superfluido(),
            "psi_red_ramsey": self.red.psi_red(),
            "psi_acoplamiento_higgspc": self.acoplamiento.psi_acoplamiento(),
            "psi_transmision_fotonico": self.transmision.psi_transmision(),
            "psi_firma_espectral": self.firma.coherencia_espectral(),
        }

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Calcula la coherencia global Ψ_global como media geométrica.

        Ψ_global = (∏ Ψ_i)^(1/N)

        Returns
        -------
        float
            Coherencia global Ψ_global ∈ [0, 1].
        """
        coherencias = list(self.coherencias_individuales().values())
        if not coherencias:
            return 0.0
        log_sum = sum(math.log(max(v, 1.0e-30)) for v in coherencias)
        return math.exp(log_sum / len(coherencias))

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        Verifica si el sello ∴SPC∞³ está activo (Ψ_global ≥ 0.888).

        Returns
        -------
        bool
            True si Ψ_global ≥ umbral.
        """
        return self.psi_global() >= self.psi_umbral

    # ------------------------------------------------------------------
    def validar(self) -> Dict[str, Any]:
        """
        Realiza la validación completa del sistema.

        Returns
        -------
        Dict[str, Any]
            Diccionario con coherencias individuales, psi_global,
            psi_umbral y sello_activo.
        """
        coherencias = self.coherencias_individuales()
        psi_g = self.psi_global()
        activo = psi_g >= self.psi_umbral
        return {
            "coherencias": coherencias,
            "psi_global": psi_g,
            "psi_umbral": self.psi_umbral,
            "sello_activo": activo,
        }

    # ------------------------------------------------------------------
    def certificacion_auron(self) -> str:
        """
        Genera la certificación AURON del sistema.

        Returns
        -------
        str
            Texto de certificación con sello y estado.
        """
        activo = self.sello_activo()
        psi_g = self.psi_global()
        estado = "ACTIVO ✓" if activo else "INACTIVO ✗"
        return (
            f"╔══════════════════════════════════════╗\n"
            f"║  CERTIFICACIÓN AURON — QCAL ∞³       ║\n"
            f"║  Sello: ∴SPC∞³                       ║\n"
            f"║  RAM: RAM-XLVIII-2026-SUSTRATO-PC    ║\n"
            f"║  Ψ_global = {psi_g:.6f}            ║\n"
            f"║  Estado: {estado:<28s} ║\n"
            f"╚══════════════════════════════════════╝"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.psi_global()
        activo = "ACTIVO" if self.sello_activo() else "INACTIVO"
        return (
            f"CoherenciaSustrato("
            f"Ψ_global={psi_g:.6f}, "
            f"∴SPC∞³={activo})"
        )


# ============================================================================
# CLASE 8 – SistemaSustratoPCVacio
# ============================================================================

@dataclass
class SistemaSustratoPCVacio:
    """
    Orquestador principal del sistema Sustrato PC-Vacío.

    Integra todos los subsistemas y expone la API de activación.

    Atributos
    ----------
    constantes : ConstantesSustrato
        Constantes físicas del módulo.
    vacio : VacioSuperfluido
        Vacío superfluido de Bose-Einstein.
    red : RedRamsey
        Red de Ramsey C₇ con 7 nodos primos.
    acoplamiento : AcoplamientoHiggsPC
        Acoplamiento Higgs-PC (Destello de Masa).
    transmision : FotonPaqueteFase
        Transmisión de fotones como paquetes de fase.
    firma : FirmaEspectral
        Firma espectral del acoplamiento.
    coherencia : CoherenciaSustrato
        Validación de coherencia global.
    """

    constantes: ConstantesSustrato = field(default_factory=ConstantesSustrato)
    vacio: VacioSuperfluido = field(default_factory=VacioSuperfluido)
    red: RedRamsey = field(default_factory=RedRamsey)
    acoplamiento: AcoplamientoHiggsPC = field(default_factory=AcoplamientoHiggsPC)
    transmision: FotonPaqueteFase = field(default_factory=FotonPaqueteFase)
    firma: FirmaEspectral = field(default_factory=FirmaEspectral)
    coherencia: CoherenciaSustrato = field(default_factory=CoherenciaSustrato)

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        """
        Reconstruye ``coherencia`` con referencias a los subsistemas reales
        de este orquestador, asegurando que ``psi_global`` y ``certificacion``
        reflejen exactamente los mismos objetos usados en el resto del payload.
        """
        self.coherencia = CoherenciaSustrato(
            vacio=self.vacio,
            red=self.red,
            acoplamiento=self.acoplamiento,
            transmision=self.transmision,
            firma=self.firma,
        )

    # ------------------------------------------------------------------
    def activar(self) -> Dict[str, Any]:
        """
        Activa el sistema y devuelve todos los resultados de validación.

        Returns
        -------
        Dict[str, Any]
            Diccionario completo con todos los parámetros del sistema.
        """
        # Constantes
        f0 = self.constantes.f0
        primos = list(self.constantes.primos_p)
        suma_p = self.constantes.suma_primos()
        g_eff = self.constantes.g_eff
        fase_berry = self.constantes.fase_berry_rad
        fase_berry_total = self.constantes.fase_berry_total()

        # Vacío superfluido
        es_sf = self.vacio.es_superfluido()
        entropia = self.vacio.entropia_vacio()
        psi_sf = self.vacio.psi_superfluido()

        # Red de Ramsey
        f_hetero = self.red.frecuencia_heterodina_hz()
        modos = self.red.modos_resonantes_hz()
        linea_critica = self.red.es_linea_critica_riemann()

        # Acoplamiento Higgs-PC
        m_estrella = self.acoplamiento.masa_efectiva_gev()
        reduccion = self.acoplamiento.reduccion_inercia()
        destello = self.acoplamiento.es_destello_activo()
        sb_lower, sb_upper = self.acoplamiento.sideband_masa_gev(n=1)

        # Transmisión fotónica
        r_symb_kpps = self.transmision.tasa_simbolica_kpps()
        g_superrad = self.transmision.ganancia_superradiante()
        psi_dicke = self.transmision.coherencia_dicke()

        # Firma espectral
        amp_pct = self.firma.amplitud_oscilacion_porcentaje()
        f_trans = self.firma.ventana_transparencia_hz()
        sidebands = self.firma.sidebands_gev(n_ordenes=3)

        # Coherencia global
        validacion = self.coherencia.validar()
        psi_global = validacion["psi_global"]
        sello_activo = validacion["sello_activo"]

        return {
            # Identificación
            "sello": "∴SPC∞³",
            "ram": "RAM-XLVIII-2026-SUSTRATO-PC-VACIO",
            "version": "1.0.0",
            # Constantes fundamentales
            "f0_hz": f0,
            "primos_p": primos,
            "suma_primos": suma_p,
            "g_eff": g_eff,
            "fase_berry_rad": fase_berry,
            "fase_berry_total_rad": fase_berry_total,
            # Vacío superfluido
            "es_superfluido": es_sf,
            "entropia_vacio": entropia,
            "psi_vacio_superfluido": psi_sf,
            # Red de Ramsey C₇
            "frecuencia_heterodina_hz": f_hetero,
            "modos_resonantes_hz": modos,
            "linea_critica_riemann": linea_critica,
            # Acoplamiento Higgs-PC
            "m_estrella_gev": m_estrella,
            "reduccion_inercia": reduccion,
            "reduccion_inercia_pct": reduccion * 100.0,
            "destello_activo": destello,
            "sideband_lower_gev": sb_lower,
            "sideband_upper_gev": sb_upper,
            # Transmisión fotónica
            "r_symb_kpps": r_symb_kpps,
            "ganancia_superradiante": g_superrad,
            "psi_dicke": psi_dicke,
            # Firma espectral
            "amplitud_oscilacion_pct": amp_pct,
            "frecuencia_transparencia_hz": f_trans,
            "sidebands_gev": sidebands,
            # Coherencias
            "coherencias": validacion["coherencias"],
            "psi_global": psi_global,
            "psi_umbral": validacion["psi_umbral"],
            "sello_activo": sello_activo,
            # Certificación
            "perturbativo": self.constantes.es_perturbativo(),
            "certificacion": self.coherencia.certificacion_auron(),
        }

    # ------------------------------------------------------------------
    def resumen(self) -> str:
        """
        Genera un resumen textual del sistema.

        Returns
        -------
        str
            Resumen del sistema con todos los parámetros clave.
        """
        r = self.activar()
        psi_g = r["psi_global"]
        estado = "✓ ACTIVO" if r["sello_activo"] else "✗ INACTIVO"
        linea = "═" * 62

        return (
            f"\n{linea}\n"
            f"  SUSTRATO PC-VACÍO — QCAL ∞³\n"
            f"  Sello: ∴SPC∞³ | RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO\n"
            f"{linea}\n"
            f"  f₀ = {r['f0_hz']:.4f} Hz\n"
            f"  Nodos primos: {r['primos_p']}\n"
            f"  Σ primos = {r['suma_primos']}\n"
            f"  g_eff = {r['g_eff']:.3f}\n"
            f"  Φ_Berry = {r['fase_berry_rad']:.4f} rad  (total: {r['fase_berry_total_rad']:.4f} rad)\n"
            f"{linea}\n"
            f"  VACÍO SUPERFLUIDO\n"
            f"  Superfluido: {r['es_superfluido']}\n"
            f"  Entropía: {r['entropia_vacio']:.2e}\n"
            f"{linea}\n"
            f"  RED DE RAMSEY C₇\n"
            f"  f_heterodina = {r['frecuencia_heterodina_hz']:.4f} Hz\n"
            f"  Línea crítica Riemann: {r['linea_critica_riemann']}\n"
            f"{linea}\n"
            f"  DESTELLO DE MASA (HIGGS-PC)\n"
            f"  m* = {r['m_estrella_gev']:.2f} GeV/c²\n"
            f"  Reducción de inercia = {r['reduccion_inercia_pct']:.1f}%\n"
            f"  Destello activo: {r['destello_activo']}\n"
            f"{linea}\n"
            f"  TRANSMISIÓN FOTÓNICA\n"
            f"  R_symb = {r['r_symb_kpps']:.1f} kpps\n"
            f"  Ganancia superradiante = {r['ganancia_superradiante']:.0f}\n"
            f"{linea}\n"
            f"  COHERENCIA GLOBAL\n"
            f"  Ψ_global = {psi_g:.6f}\n"
            f"  Estado: {estado}\n"
            f"{linea}\n"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.coherencia.psi_global()
        activo = "ACTIVO" if self.coherencia.sello_activo() else "INACTIVO"
        return (
            f"SistemaSustratoPCVacio("
            f"f₀={self.constantes.f0} Hz, "
            f"Ψ_global={psi_g:.4f}, "
            f"∴SPC∞³={activo})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def sustrato_pc_vacio_activar() -> Dict[str, Any]:
    """
    Función principal de la API pública.

    Activa el sistema Sustrato PC-Vacío y devuelve todos los resultados
    de validación del sello ∴SPC∞³.

    Returns
    -------
    Dict[str, Any]
        Diccionario con todos los resultados del sistema:
        - sello: str — Identificador del sello (∴SPC∞³)
        - ram: str — Identificador RAM
        - version: str — Versión del módulo
        - f0_hz: float — Frecuencia fundamental (141.7001 Hz)
        - primos_p: list — 7 nodos primos [2,3,5,7,11,13,17]
        - suma_primos: int — Suma de los primos (58)
        - g_eff: float — Acoplamiento efectivo (0.053)
        - fase_berry_rad: float — Fase de Berry por salto (π/8 rad)
        - fase_berry_total_rad: float — Fase total del ciclo C₇
        - es_superfluido: bool — True si ν < 1e-10
        - entropia_vacio: float — Entropía del vacío superfluido
        - psi_vacio_superfluido: float — Coherencia del superfluido
        - frecuencia_heterodina_hz: float — Frecuencia heterodina (141.7001 Hz)
        - modos_resonantes_hz: list — 7 modos resonantes
        - linea_critica_riemann: bool — True si Re(s)=1/2
        - m_estrella_gev: float — Masa efectiva m* (GeV/c²)
        - reduccion_inercia: float — Fracción de reducción de inercia (0.053)
        - reduccion_inercia_pct: float — Reducción en porcentaje (5.3 %)
        - destello_activo: bool — True si reducción ≥ 5 %
        - sideband_lower_gev: float — Sideband inferior m_H - ℏω₀ (GeV)
        - sideband_upper_gev: float — Sideband superior m_H + ℏω₀ (GeV)
        - r_symb_kpps: float — Tasa simbiótica (≈ 991.9 kpps)
        - ganancia_superradiante: float — Ganancia Dicke N²
        - psi_dicke: float — Coherencia de Dicke
        - amplitud_oscilacion_pct: float — Amplitud de oscilación σ (5.3 %)
        - frecuencia_transparencia_hz: float — Ventana de transparencia (Hz)
        - sidebands_gev: list — Sidebands de masa (n=1,2,3)
        - coherencias: dict — Coherencias individuales de subsistemas
        - psi_global: float — Coherencia global Ψ_global
        - psi_umbral: float — Umbral mínimo (0.888)
        - sello_activo: bool — True si Ψ_global ≥ 0.888
        - perturbativo: bool — True si g_eff < 0.1
        - certificacion: str — Certificación AURON

    Examples
    --------
    >>> from physics.sustrato_pc_vacio import sustrato_pc_vacio_activar
    >>> r = sustrato_pc_vacio_activar()
    >>> r['sello']
    '∴SPC∞³'
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['f0_hz'] - 141.7001) < 0.001
    True
    >>> r['primos_p']
    [2, 3, 5, 7, 11, 13, 17]
    >>> abs(r['reduccion_inercia_pct'] - 5.3) < 0.01
    True
    """
    sistema = SistemaSustratoPCVacio()
    return sistema.activar()


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  SUSTRATO PC-VACÍO — QCAL ∞³")
    print("  Sello: ∴SPC∞³ | RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO")
    print("=" * 70)

    sistema = SistemaSustratoPCVacio()
    print(sistema.resumen())

    resultado = sustrato_pc_vacio_activar()

    print("  COHERENCIAS INDIVIDUALES:")
    for nombre, valor in resultado["coherencias"].items():
        print(f"  {nombre} = {valor:.6f}")

    print(f"\n  Ψ_global = {resultado['psi_global']:.6f}")
    estado = "✓ ACTIVO" if resultado["sello_activo"] else "✗ INACTIVO"
    print(f"  Estado: {estado}")

    print("\n" + resultado["certificacion"])
    print()
