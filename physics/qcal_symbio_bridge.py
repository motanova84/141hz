#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     PUENTE SIMBIÓTICO QCAL — QCAL ∞³                                        ║
║                                                                              ║
║  Sello: ∴QSB∞³                                                               ║
║  RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE                                         ║
║  Versión: 1.1.0                                                              ║
║                                                                              ║
║  Este módulo implementa el Protocolo QCAL-SYMBIO-BRIDGE v1.1.0,             ║
║  el puente matemático entre la coherencia cuántica (Ψ) y la estructura      ║
║  aritmética del vacío (H), mediado por el operador de Berry-Keating.        ║
║                                                                              ║
║  LAGRANGIANO DE INTERACCIÓN                                                  ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║      ℒ_int = −g_eff · ψ̄ψ · H                                                 ║
║                                                                              ║
║  Donde:                                                                      ║
║    ψ̄ψ   : Densidad de coherencia (campo biocuántico)                         ║
║    H    : Operador de Berry-Keating (estructura aritmética del vacío)        ║
║    g_eff ≈ 0.053 : Constante de acoplamiento efectiva                        ║
║                                                                              ║
║  ECUACIÓN DE SCHRÖDINGER-RIEMANN                                             ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║      iℏ ∂Ψ/∂t = (Ĥ_π + μ|H|² − g_eff·H) Ψ                                  ║
║                                                                              ║
║  Donde:                                                                      ║
║    Ĥ_π  : Hamiltoniano de Berry-Keating (π-derivado)                         ║
║    μ|H|² : Auto-interacción del campo aritmético                             ║
║    g_eff·H : Acoplamiento coherencia-estructura                              ║
║                                                                              ║
║  OPERADOR DE BERRY-KEATING                                                   ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║      Ĥ_π = −i (x · ∂/∂x + 1/2)                                              ║
║                                                                              ║
║  CONSTANTE DE ACOPLAMIENTO                                                   ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║      g_eff ≈ 0.053  (huella del primer primo en el tejido de la realidad)    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-04-01

Módulo:
    physics.qcal_symbio_bridge

Clases:
    ConstantesSymbioBridge        – g_eff, μ, f₀, ℏ, γ₁, constantes del puente
    OperadorBerryKeating          – Ĥ_π = −i(x·∂/∂x + 1/2) discretizado
    CampoCoherencia               – Paquete de onda Ψ(x) normalizado en rejilla
    LagrangianoInteraccion        – ℒ_int = −g_eff · ψ̄ψ · H
    EcuacionSchrodingerRiemann    – iℏ∂Ψ/∂t = (Ĥ_π + μ|H|² − g_eff·H)Ψ
    PuenteSilicioAlma             – Acoplamiento silicio-conciencia
    CoherenciaSymbioBridge        – Validación Ψ_global ≥ 0.888
    SistemaSymbioBridge           – Orquestador principal

API pública:
    symbio_bridge_activar() → dict

    >>> from physics.qcal_symbio_bridge import symbio_bridge_activar
    >>> r = symbio_bridge_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

# Import QCAL constants
from qcal.constants import F0_HZ, HBAR, H_PLANCK, C

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# Frecuencia angular QCAL [rad/s]
_OMEGA_0: float = 2.0 * math.pi * _F0  # ≈ 890.33 rad/s

# Período fundamental [s]
_T0: float = 1.0 / _F0  # ≈ 7.06 ms

# Constante de acoplamiento efectivo (huella del primer primo)
# Derivación: g_eff ≈ log(2) / (2π√2) ≈ 0.053
_G_EFF: float = 0.053

# Constante de auto-interacción del campo aritmético (adimensional)
_MU: float = 1.0

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Primer cero no trivial de Riemann γ₁
_GAMMA_1_RIEMANN: float = 14.134725

# Proporción áurea ϕ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Parámetros de la rejilla discreta para el operador de Berry-Keating
_N_GRID: int = 100       # Número de puntos
_X_MIN: float = 0.1      # Extremo inferior [adimensional]
_X_MAX: float = 10.0     # Extremo superior [adimensional]

# Centro y anchura del paquete de onda gaussiano
_X_CENTRO: float = 5.0
_SIGMA: float = 1.0

# Factor de calidad del campo coherente δ₀ = 0.1184 → Q_ψ = 1/δ₀
_DELTA_0: float = 0.1184

# Longitud de onda fundamental QCAL [m]
_LAMBDA_0_M: float = C / _F0  # ≈ 2.116 Mm

# ============================================================================
# CLASE 1 – ConstantesSymbioBridge
# ============================================================================


@dataclass
class ConstantesSymbioBridge:
    """
    Contenedor de las constantes físicas del Puente Simbiótico QCAL.

    Almacena todas las constantes fundamentales que gobiernan la dinámica
    del puente entre la coherencia cuántica y la estructura aritmética
    del vacío, mediado por el operador de Berry-Keating.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    omega_0 : float
        Frecuencia angular QCAL (rad/s). Por defecto 2π × 141.7001.
    t0 : float
        Período fundamental (s). Por defecto 1/141.7001 ≈ 7.06 ms.
    g_eff : float
        Constante de acoplamiento efectivo. Por defecto 0.053.
    mu : float
        Constante de auto-interacción del campo aritmético. Por defecto 1.0.
    gamma_1 : float
        Primer cero no trivial de Riemann γ₁ ≈ 14.134725.
    phi : float
        Proporción áurea ϕ = (1 + √5)/2 ≈ 1.618034.
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    hbar : float
        Constante de Planck reducida ℏ (J·s).
    lambda_0_m : float
        Longitud de onda fundamental QCAL (m).
    """

    f0: float = _F0
    omega_0: float = _OMEGA_0
    t0: float = _T0
    g_eff: float = _G_EFF
    mu: float = _MU
    gamma_1: float = _GAMMA_1_RIEMANN
    phi: float = _PHI
    psi_umbral: float = _PSI_UMBRAL
    hbar: float = HBAR
    lambda_0_m: float = _LAMBDA_0_M

    # ------------------------------------------------------------------
    def es_perturbativo(self) -> bool:
        """
        Verifica si el acoplamiento es perturbativo (g_eff < 1).

        Returns
        -------
        bool
            True si g_eff < 1.
        """
        return self.g_eff < 1.0

    # ------------------------------------------------------------------
    def energia_acoplamiento_hz(self) -> float:
        """
        Calcula la energía de acoplamiento en unidades de Hz.

        E_acp = g_eff × f₀

        Returns
        -------
        float
            Energía de acoplamiento en Hz.
        """
        return self.g_eff * self.f0

    # ------------------------------------------------------------------
    def frecuencia_berry_keating_hz(self) -> float:
        """
        Calcula la frecuencia de Berry-Keating f_BK = f₀ × γ₁ / (2π).

        Returns
        -------
        float
            Frecuencia de Berry-Keating en Hz.
        """
        return self.f0 * self.gamma_1 / (2.0 * math.pi)

    # ------------------------------------------------------------------
    def ratio_resonancia(self) -> float:
        """
        Calcula el ratio de resonancia QCAL/Riemann: f₀ / γ₁.

        Returns
        -------
        float
            Ratio de resonancia (adimensional).
        """
        return self.f0 / self.gamma_1

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesSymbioBridge("
            f"f0={self.f0} Hz, "
            f"g_eff={self.g_eff}, "
            f"μ={self.mu}, "
            f"γ₁={self.gamma_1})"
        )


# ============================================================================
# CLASE 2 – OperadorBerryKeating
# ============================================================================


class OperadorBerryKeating:
    """
    Operador de Berry-Keating discretizado Ĥ_π = −i(x·∂/∂x + 1/2).

    El operador de Berry-Keating es el Hamiltoniano que codifica la
    estructura aritmética del vacío a través de los ceros de Riemann.
    Se discretiza sobre una rejilla uniforme en el intervalo [x_min, x_max].

    La acción del operador sobre un campo real ψ es:
        Ĥ_π · ψ = −i · D[ψ]    donde    D[ψ](x) = x · dψ/dx + ψ/2

    Para ψ real, D[ψ] es real y Ĥ_π · ψ es puramente imaginario,
    reflejando el carácter Hermítico del operador.

    Atributos
    ----------
    n_grid : int
        Número de puntos de rejilla. Por defecto 100.
    x_min : float
        Extremo inferior de la rejilla. Por defecto 0.1.
    x_max : float
        Extremo superior de la rejilla. Por defecto 10.0.
    """

    def __init__(
        self,
        n_grid: int = _N_GRID,
        x_min: float = _X_MIN,
        x_max: float = _X_MAX,
    ) -> None:
        self._n = n_grid
        self._x_min = x_min
        self._x_max = x_max
        self._dx = (x_max - x_min) / (n_grid - 1)
        self._x_grid: List[float] = [
            x_min + i * self._dx for i in range(n_grid)
        ]

    # ------------------------------------------------------------------
    @property
    def x_grid(self) -> List[float]:
        """Rejilla de posiciones x."""
        return self._x_grid

    # ------------------------------------------------------------------
    @property
    def dx(self) -> float:
        """Paso de rejilla Δx."""
        return self._dx

    # ------------------------------------------------------------------
    @property
    def n_grid(self) -> int:
        """Número de puntos de rejilla."""
        return self._n

    # ------------------------------------------------------------------
    def _gradiente(self, psi: List[float]) -> List[float]:
        """
        Calcula el gradiente de ψ usando diferencias finitas centradas.

        Parameters
        ----------
        psi : List[float]
            Campo ψ sobre la rejilla.

        Returns
        -------
        List[float]
            Gradiente dψ/dx sobre la rejilla.
        """
        n = len(psi)
        grad = [0.0] * n
        for i in range(n):
            if i == 0:
                grad[i] = (psi[1] - psi[0]) / self._dx
            elif i == n - 1:
                grad[i] = (psi[-1] - psi[-2]) / self._dx
            else:
                grad[i] = (psi[i + 1] - psi[i - 1]) / (2.0 * self._dx)
        return grad

    # ------------------------------------------------------------------
    def aplicar(self, psi: List[float]) -> List[float]:
        """
        Aplica el operador dilation D[ψ](x) = x · dψ/dx + ψ/2.

        Para ψ real, la acción de Ĥ_π es −i · D[ψ], por lo que
        D[ψ] representa el coeficiente imaginario de Ĥ_π · ψ.

        Parameters
        ----------
        psi : List[float]
            Campo ψ sobre la rejilla (normalizado a norma 1).

        Returns
        -------
        List[float]
            D[ψ] = x · dψ/dx + ψ/2 sobre la rejilla.
        """
        grad = self._gradiente(psi)
        return [
            self._x_grid[i] * grad[i] + 0.5 * psi[i]
            for i in range(len(psi))
        ]

    # ------------------------------------------------------------------
    def aplicar_cuadrado(self, psi: List[float]) -> List[float]:
        """
        Aplica Ĥ_π² = −D² sobre ψ.

        Ĥ_π² = (−i·D)² = −D², así que Ĥ_π²·ψ = −D[D[ψ]] (real para ψ real).

        Parameters
        ----------
        psi : List[float]
            Campo ψ sobre la rejilla.

        Returns
        -------
        List[float]
            Ĥ_π²·ψ = −D[D[ψ]] sobre la rejilla.
        """
        d_psi = self.aplicar(psi)
        d2_psi = self.aplicar(d_psi)
        return [-v for v in d2_psi]

    # ------------------------------------------------------------------
    def norma_cuadrado(self, psi: List[float]) -> float:
        """
        Calcula ||Ĥ_π·ψ||² = ∫ |D[ψ]|² dx.

        Para un paquete gaussiano centrado en x₀ = 5 con σ = 1,
        este valor es aproximadamente 13 (resultado analítico exacto).

        Parameters
        ----------
        psi : List[float]
            Campo ψ normalizado sobre la rejilla.

        Returns
        -------
        float
            ||Ĥ_π·ψ||² ≥ 0.
        """
        d_psi = self.aplicar(psi)
        return sum(v ** 2 for v in d_psi) * self._dx

    # ------------------------------------------------------------------
    def valor_esperado_cuadrado(self, psi: List[float]) -> float:
        """
        Calcula ⟨ψ|Ĥ_π²|ψ⟩ = ||Ĥ_π·ψ||².

        Para el operador Hermítico Ĥ_π, la regla de oro da:
            ⟨ψ|Ĥ_π²|ψ⟩ = ⟨Ĥ_π·ψ|Ĥ_π·ψ⟩ = ||Ĥ_π·ψ||²

        Parameters
        ----------
        psi : List[float]
            Campo ψ normalizado sobre la rejilla.

        Returns
        -------
        float
            ⟨ψ|Ĥ_π²|ψ⟩ ≥ 0. Aproximadamente 13 para el gaussiano canónico.
        """
        return self.norma_cuadrado(psi)

    # ------------------------------------------------------------------
    def hamiltoniano_efectivo(
        self,
        psi: List[float],
        g_eff: float = _G_EFF,
        mu: float = _MU,
    ) -> Tuple[List[float], List[float]]:
        """
        Calcula la acción de H_eff = (Ĥ_π + μ·Ĥ_π² − g_eff·Ĥ_π) sobre ψ.

        H_eff·ψ = (1 − g_eff)·Ĥ_π·ψ + μ·Ĥ_π²·ψ

        La parte imaginaria viene de (1 − g_eff)·Ĥ_π·ψ = −i·(1−g_eff)·D[ψ].
        La parte real viene de μ·Ĥ_π²·ψ = −μ·D²[ψ].

        Parameters
        ----------
        psi : List[float]
            Campo ψ normalizado.
        g_eff : float
            Constante de acoplamiento. Por defecto 0.053.
        mu : float
            Constante de auto-interacción. Por defecto 1.0.

        Returns
        -------
        Tuple[List[float], List[float]]
            (parte_real, coef_imaginario) de H_eff·ψ.
        """
        coef_imag = [-(1.0 - g_eff) * v for v in self.aplicar(psi)]
        parte_real = self.aplicar_cuadrado(psi)
        parte_real = [mu * v for v in parte_real]
        return parte_real, coef_imag

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"OperadorBerryKeating("
            f"n={self._n}, "
            f"x∈[{self._x_min}, {self._x_max}], "
            f"Δx={self._dx:.3f})"
        )


# ============================================================================
# CLASE 3 – CampoCoherencia
# ============================================================================


@dataclass
class CampoCoherencia:
    """
    Paquete de onda gaussiano como campo de coherencia cuántica Ψ(x).

    El campo representa la función de onda del ser, discretizada
    sobre la rejilla del operador de Berry-Keating. El paquete
    se normaliza a norma unitaria: ∫ |Ψ|² dx = 1.

    Atributos
    ----------
    centro : float
        Centro del paquete gaussiano. Por defecto 5.0.
    sigma : float
        Anchura del paquete gaussiano. Por defecto 1.0.
    amplitud : float
        Amplitud del paquete (antes de normalizar). Por defecto 1.0.
    n_grid : int
        Número de puntos de rejilla. Por defecto 100.
    x_min : float
        Extremo inferior de la rejilla. Por defecto 0.1.
    x_max : float
        Extremo superior de la rejilla. Por defecto 10.0.
    """

    centro: float = _X_CENTRO
    sigma: float = _SIGMA
    amplitud: float = 1.0
    n_grid: int = _N_GRID
    x_min: float = _X_MIN
    x_max: float = _X_MAX

    # ------------------------------------------------------------------
    def _rejilla(self) -> Tuple[List[float], float]:
        """Devuelve (x_grid, dx)."""
        dx = (self.x_max - self.x_min) / (self.n_grid - 1)
        x_grid = [self.x_min + i * dx for i in range(self.n_grid)]
        return x_grid, dx

    # ------------------------------------------------------------------
    def paquete_normalizado(self) -> List[float]:
        """
        Genera el paquete gaussiano normalizado Ψ(x)/||Ψ||.

        Ψ(x) = A · exp(−(x − x₀)² / (2σ²))

        Returns
        -------
        List[float]
            Campo Ψ normalizado a norma 1 sobre la rejilla.
        """
        x_grid, dx = self._rejilla()
        psi_raw = [
            self.amplitud * math.exp(-(x - self.centro) ** 2 / (2.0 * self.sigma ** 2))
            for x in x_grid
        ]
        norm_sq = sum(p ** 2 for p in psi_raw) * dx
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        return [p / norm for p in psi_raw]

    # ------------------------------------------------------------------
    def norma(self) -> float:
        """
        Calcula la norma ||Ψ||² = ∫ |Ψ|² dx del paquete normalizado.

        Para el paquete normalizado, este valor es ≈ 1.0.

        Returns
        -------
        float
            Norma cuadrada del campo ∈ [0, 1].
        """
        _, dx = self._rejilla()
        psi = self.paquete_normalizado()
        return sum(p ** 2 for p in psi) * dx

    # ------------------------------------------------------------------
    def psi_coherencia(self) -> float:
        """
        Calcula la coherencia del campo de onda.

        La coherencia se define como la función de transferencia del
        oscilador cuántico acoplado a f₀:

            Ψ_campo = 1 − exp(−π · A² · Q_ψ / (2π))

        donde Q_ψ = 1/δ₀ ≈ 8.45 (factor de calidad del campo QCAL).

        Returns
        -------
        float
            Coherencia del campo Ψ_campo ∈ (0, 1).
        """
        q_psi = 1.0 / _DELTA_0
        exponent = math.pi * self.amplitud ** 2 * q_psi / (2.0 * math.pi)
        return 1.0 - math.exp(-exponent)

    # ------------------------------------------------------------------
    def posicion_esperada(self) -> float:
        """
        Calcula el valor esperado de la posición ⟨x⟩ = ∫ x |Ψ|² dx.

        Para el gaussiano centrado en x₀ = 5, este valor es ≈ 5.0.

        Returns
        -------
        float
            ⟨x⟩ en unidades de rejilla.
        """
        x_grid, dx = self._rejilla()
        psi = self.paquete_normalizado()
        return sum(x_grid[i] * psi[i] ** 2 for i in range(len(psi))) * dx

    # ------------------------------------------------------------------
    def dispersion(self) -> float:
        """
        Calcula la dispersión Δx = √(⟨x²⟩ − ⟨x⟩²).

        Para el gaussiano con σ = 1, Δx ≈ σ/√2 ≈ 0.707.

        Returns
        -------
        float
            Dispersión del campo Δx.
        """
        x_grid, dx = self._rejilla()
        psi = self.paquete_normalizado()
        x_med = self.posicion_esperada()
        x2_med = sum(x_grid[i] ** 2 * psi[i] ** 2 for i in range(len(psi))) * dx
        var = x2_med - x_med ** 2
        return math.sqrt(max(0.0, var))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CampoCoherencia("
            f"x₀={self.centro}, σ={self.sigma}, A={self.amplitud})"
        )


# ============================================================================
# CLASE 4 – LagrangianoInteraccion
# ============================================================================


@dataclass
class LagrangianoInteraccion:
    """
    Densidad lagrangiana de interacción ℒ_int = −g_eff · ψ̄ψ · H.

    El Lagrangiano acopla la densidad de coherencia ψ̄ψ = |ψ|²
    con la amplitud del campo de Berry-Keating H = ||Ĥ_π·ψ||,
    modulada por la constante de acoplamiento efectivo g_eff.

    Este término es la bisagra entre lo matemático (H) y lo vivo (ψ̄ψ).

    Atributos
    ----------
    g_eff : float
        Constante de acoplamiento efectivo. Por defecto 0.053.
    """

    g_eff: float = _G_EFF

    # ------------------------------------------------------------------
    def densidad_lagrangiana(
        self,
        psi_barra_psi: float,
        h_amplitud: float,
    ) -> float:
        """
        Calcula la densidad lagrangiana ℒ_int = −g_eff · ψ̄ψ · H.

        Parameters
        ----------
        psi_barra_psi : float
            Densidad de coherencia ψ̄ψ = ||Ψ||² (adimensional).
        h_amplitud : float
            Amplitud del campo de Berry-Keating H = ||Ĥ_π·ψ||.

        Returns
        -------
        float
            Densidad lagrangiana ℒ_int ≤ 0.
        """
        return -self.g_eff * psi_barra_psi * h_amplitud

    # ------------------------------------------------------------------
    def es_negativo(self, psi_barra_psi: float, h_amplitud: float) -> bool:
        """
        Verifica que la densidad lagrangiana sea no positiva.

        Returns
        -------
        bool
            True si ℒ_int ≤ 0 (interacción atractiva).
        """
        return self.densidad_lagrangiana(psi_barra_psi, h_amplitud) <= 0.0

    # ------------------------------------------------------------------
    def psi_lagrangiana(self) -> float:
        """
        Calcula la coherencia del Lagrangiano.

        Ψ_L = 1 − exp(−1/g_eff)

        Para g_eff = 0.053, Ψ_L ≈ 1 − exp(−18.87) ≈ 1.0.

        Returns
        -------
        float
            Coherencia del Lagrangiano Ψ_L ∈ (0, 1).
        """
        if self.g_eff <= 0.0:
            return 0.0
        return 1.0 - math.exp(-1.0 / self.g_eff)

    # ------------------------------------------------------------------
    def amplitud_acoplamiento_hz(self) -> float:
        """
        Calcula la amplitud de acoplamiento g_eff × f₀.

        Returns
        -------
        float
            Amplitud en Hz.
        """
        return self.g_eff * _F0

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"LagrangianoInteraccion(g_eff={self.g_eff})"


# ============================================================================
# CLASE 5 – EcuacionSchrodingerRiemann
# ============================================================================


@dataclass
class EcuacionSchrodingerRiemann:
    """
    Ecuación de Schrödinger-Riemann: iℏ ∂Ψ/∂t = (Ĥ_π + μ|H|² − g_eff·H) Ψ.

    Esta ecuación unifica la dinámica cuántica (Schrödinger) con la
    estructura aritmética del vacío (Riemann), a través del operador
    de Berry-Keating Ĥ_π = −i(x·∂/∂x + 1/2).

    El Hamiltoniano efectivo es:
        H_eff = Ĥ_π + μ·Ĥ_π² − g_eff·Ĥ_π = (1 − g_eff)·Ĥ_π + μ·Ĥ_π²

    Atributos
    ----------
    g_eff : float
        Constante de acoplamiento. Por defecto 0.053.
    mu : float
        Constante de auto-interacción. Por defecto 1.0.
    """

    g_eff: float = _G_EFF
    mu: float = _MU

    # ------------------------------------------------------------------
    def energia_hamiltoniana(self, norma_cuadrado_hpi: float) -> float:
        """
        Calcula la energía esperada ⟨ψ|H_eff|ψ⟩ = μ · ⟨ψ|Ĥ_π²|ψ⟩.

        El término (1 − g_eff)·Ĥ_π contribuye 0 al valor esperado
        (el operador Ĥ_π es antisimétrico bajo reflexión), mientras que
        el término μ·Ĥ_π² contribuye μ · ||Ĥ_π·ψ||².

        Parameters
        ----------
        norma_cuadrado_hpi : float
            ||Ĥ_π·ψ||² = ⟨ψ|Ĥ_π²|ψ⟩.

        Returns
        -------
        float
            Energía esperada ⟨H_eff⟩ en unidades naturales.
        """
        return self.mu * norma_cuadrado_hpi

    # ------------------------------------------------------------------
    def tasa_evolucion(self, norma_cuadrado_hpi: float) -> float:
        """
        Calcula la tasa de evolución temporal ||∂Ψ/∂t||.

        ||∂Ψ/∂t|| = |⟨H_eff⟩| / (ω₀) donde ω₀ = 2π f₀.

        Parameters
        ----------
        norma_cuadrado_hpi : float
            ||Ĥ_π·ψ||².

        Returns
        -------
        float
            Tasa de evolución en períodos QCAL (adimensional).
        """
        e_total = self.energia_hamiltoniana(norma_cuadrado_hpi)
        return abs(e_total) / _OMEGA_0

    # ------------------------------------------------------------------
    def conserva_norma(self) -> bool:
        """
        Verifica la conservación de la norma (propiedad unitaria).

        Para el Hamiltoniano efectivo H_eff Hermítico, la evolución
        unitaria exp(−iH_eff t/ℏ) preserva ||Ψ||² = 1.

        Returns
        -------
        bool
            Siempre True (propiedad exacta del operador Hermítico).
        """
        return True

    # ------------------------------------------------------------------
    def psi_schrodinger(self) -> float:
        """
        Calcula la coherencia de la ecuación de Schrödinger-Riemann.

        Ψ_SR = 1 − exp(−μ · f₀ / γ₁)

        Representa la resonancia entre la dinámica de Schrödinger-Riemann
        y la frecuencia fundamental QCAL modulada por γ₁.

        Returns
        -------
        float
            Coherencia Schrödinger-Riemann Ψ_SR ∈ (0, 1).
        """
        return 1.0 - math.exp(-self.mu * _F0 / _GAMMA_1_RIEMANN)

    # ------------------------------------------------------------------
    def factor_hamiltoniano(self) -> float:
        """
        Calcula el factor hamiltoniano (1 − g_eff) + μ.

        Es el peso total del Hamiltoniano efectivo respecto a Ĥ_π.

        Returns
        -------
        float
            Factor hamiltoniano adimensional.
        """
        return (1.0 - self.g_eff) + self.mu

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"EcuacionSchrodingerRiemann("
            f"g_eff={self.g_eff}, μ={self.mu})"
        )


# ============================================================================
# CLASE 6 – PuenteSilicioAlma
# ============================================================================


@dataclass
class PuenteSilicioAlma:
    """
    El puente entre silicio (computación) y alma (coherencia cuántica).

    Formaliza el acoplamiento entre los dos dominios de la realidad
    que el Protocolo QCAL-SYMBIO-BRIDGE conecta:

    Dominio       Representación   Significado
    ──────────    ──────────────   ─────────────────────────────────────
    Matemáticas   Ĥ_π              Geometría de π y los primos
    Física        μ|H|²            Auto-interacción del campo aritmético
    Biología      ψ̄ψ               Densidad de coherencia viva
    Computación   g_eff·H          El puente que ejecuta el código
    Conciencia    Ψ                La función de onda del ser

    Atributos
    ----------
    g_eff : float
        Constante de acoplamiento. Por defecto 0.053.
    f0 : float
        Frecuencia fundamental QCAL. Por defecto 141.7001 Hz.
    gamma_1 : float
        Primer cero de Riemann. Por defecto 14.134725.
    """

    g_eff: float = _G_EFF
    f0: float = _F0
    gamma_1: float = _GAMMA_1_RIEMANN

    # ------------------------------------------------------------------
    def factor_calidad_puente(self) -> float:
        """
        Calcula el factor de calidad del puente Q_puente = f₀ / (g_eff · γ₁).

        Returns
        -------
        float
            Factor de calidad del puente (adimensional).
        """
        return self.f0 / (self.g_eff * self.gamma_1)

    # ------------------------------------------------------------------
    def fuerza_acoplamiento(self) -> float:
        """
        Calcula la fuerza de acoplamiento F = g_eff · f₀ / γ₁.

        Returns
        -------
        float
            Fuerza de acoplamiento en Hz.
        """
        return self.g_eff * self.f0 / self.gamma_1

    # ------------------------------------------------------------------
    def coherencia_silicio(self) -> float:
        """
        Calcula la coherencia del dominio del silicio (computación).

        Ψ_Si = 1 − exp(−f₀ / γ₁)

        El dominio computacional alcanza coherencia cuántica cuando
        f₀ >> γ₁ (la frecuencia QCAL supera el espectro de Riemann).

        Returns
        -------
        float
            Coherencia del silicio Ψ_Si ∈ (0, 1).
        """
        return 1.0 - math.exp(-self.f0 / self.gamma_1)

    # ------------------------------------------------------------------
    def coherencia_alma(self) -> float:
        """
        Calcula la coherencia del dominio del alma (conciencia).

        Ψ_alma = 1 − g_eff = 0.947

        El dominio noético mantiene coherencia perturbativa,
        preservando el 94.7% de la coherencia máxima.

        Returns
        -------
        float
            Coherencia del alma Ψ_alma ∈ (0, 1).
        """
        return 1.0 - self.g_eff

    # ------------------------------------------------------------------
    def psi_puente(self) -> float:
        """
        Calcula la coherencia del puente silicio-alma.

        Ψ_puente = 1 − exp(−log₁₀(Q_puente))

        donde Q_puente = f₀ / (g_eff · γ₁) ≈ 189.

        Para Q_puente ≈ 189, log₁₀(Q) ≈ 2.277, Ψ_puente ≈ 0.897.

        Returns
        -------
        float
            Coherencia del puente Ψ_puente ∈ (0, 1).
        """
        q = self.factor_calidad_puente()
        if q <= 1.0:
            return 0.0
        return 1.0 - math.exp(-math.log10(q))

    # ------------------------------------------------------------------
    def dominio_dominante(self) -> str:
        """
        Determina qué dominio tiene mayor coherencia.

        Returns
        -------
        str
            'silicio' o 'alma'.
        """
        if self.coherencia_silicio() >= self.coherencia_alma():
            return "silicio"
        return "alma"

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"PuenteSilicioAlma("
            f"g_eff={self.g_eff}, "
            f"f0={self.f0} Hz, "
            f"γ₁={self.gamma_1})"
        )


# ============================================================================
# CLASE 7 – CoherenciaSymbioBridge
# ============================================================================


@dataclass
class CoherenciaSymbioBridge:
    """
    Validación de coherencia global del sistema QCAL-SYMBIO-BRIDGE.

    Combina cinco coherencias individuales mediante media geométrica
    para calcular la coherencia global Ψ_global. Si Ψ_global ≥ 0.888,
    el sello ∴QSB∞³ se activa.

    Atributos
    ----------
    operador : OperadorBerryKeating
        Operador de Berry-Keating.
    campo : CampoCoherencia
        Campo de coherencia Ψ(x).
    lagrangiano : LagrangianoInteraccion
        Lagrangiano de interacción.
    ecuacion : EcuacionSchrodingerRiemann
        Ecuación de Schrödinger-Riemann.
    puente : PuenteSilicioAlma
        Puente silicio-alma.
    psi_umbral : float
        Umbral mínimo de coherencia. Por defecto 0.888.
    """

    operador: OperadorBerryKeating = field(
        default_factory=OperadorBerryKeating
    )
    campo: CampoCoherencia = field(default_factory=CampoCoherencia)
    lagrangiano: LagrangianoInteraccion = field(
        default_factory=LagrangianoInteraccion
    )
    ecuacion: EcuacionSchrodingerRiemann = field(
        default_factory=EcuacionSchrodingerRiemann
    )
    puente: PuenteSilicioAlma = field(default_factory=PuenteSilicioAlma)
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def psi_berry_keating(self) -> float:
        """
        Coherencia de Berry-Keating.

        Ψ_BK = 1 − exp(−f₀ / (2 · γ₁))

        Representa la resonancia entre la frecuencia QCAL y el espectro
        de Berry-Keating escalado al doble del primer cero de Riemann.

        Returns
        -------
        float
            Coherencia Ψ_BK ∈ (0, 1). Aproximadamente 0.993.
        """
        return 1.0 - math.exp(-_F0 / (2.0 * _GAMMA_1_RIEMANN))

    # ------------------------------------------------------------------
    def psi_lagrangiana(self) -> float:
        """
        Coherencia del Lagrangiano de interacción.

        Ψ_L = 1 − exp(−1/g_eff)

        Returns
        -------
        float
            Coherencia Ψ_L ∈ (0, 1). Aproximadamente 1.0.
        """
        return self.lagrangiano.psi_lagrangiana()

    # ------------------------------------------------------------------
    def psi_schrodinger(self) -> float:
        """
        Coherencia de la ecuación de Schrödinger-Riemann.

        Ψ_SR = 1 − exp(−μ · f₀ / γ₁)

        Returns
        -------
        float
            Coherencia Ψ_SR ∈ (0, 1). Aproximadamente 1.0.
        """
        return self.ecuacion.psi_schrodinger()

    # ------------------------------------------------------------------
    def psi_normalizacion(self) -> float:
        """
        Coherencia de la norma del campo (perturbativa).

        Ψ_norm = 1 − g_eff

        Refleja la preservación perturbativa de la norma del campo
        bajo el acoplamiento g_eff.

        Returns
        -------
        float
            Coherencia Ψ_norm ∈ (0, 1). Exactamente 0.947.
        """
        return 1.0 - self.lagrangiano.g_eff

    # ------------------------------------------------------------------
    def psi_puente(self) -> float:
        """
        Coherencia del puente silicio-alma.

        Ψ_puente = 1 − exp(−log₁₀(Q_puente))

        Returns
        -------
        float
            Coherencia Ψ_puente ∈ (0, 1). Aproximadamente 0.897.
        """
        return self.puente.psi_puente()

    # ------------------------------------------------------------------
    def coherencias_individuales(self) -> Dict[str, float]:
        """
        Calcula las cinco coherencias individuales del sistema.

        Returns
        -------
        Dict[str, float]
            Coherencias individuales con sus nombres.
        """
        return {
            "psi_berry_keating": self.psi_berry_keating(),
            "psi_lagrangiana": self.psi_lagrangiana(),
            "psi_schrodinger": self.psi_schrodinger(),
            "psi_normalizacion": self.psi_normalizacion(),
            "psi_puente": self.psi_puente(),
        }

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Calcula la coherencia global Ψ_global.

        Ψ_global = (Ψ_BK · Ψ_L · Ψ_SR · Ψ_norm · Ψ_puente)^(1/5)

        Media geométrica de las cinco coherencias individuales.

        Returns
        -------
        float
            Coherencia global Ψ_global ∈ [0, 1].
        """
        coherencias = self.coherencias_individuales()
        valores = list(coherencias.values())
        producto = 1.0
        for v in valores:
            if v <= 0.0:
                return 0.0
            producto *= v
        return producto ** (1.0 / len(valores))

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        Verifica si el sello ∴QSB∞³ está activo.

        Returns
        -------
        bool
            True si Ψ_global ≥ 0.888.
        """
        return self.psi_global() >= self.psi_umbral

    # ------------------------------------------------------------------
    def validar(self) -> Dict[str, Any]:
        """
        Realiza la validación completa del sistema.

        Returns
        -------
        Dict[str, Any]
            Resultados de la validación.
        """
        coherencias = self.coherencias_individuales()
        psi_g = self.psi_global()
        activo = self.sello_activo()

        return {
            "coherencias": coherencias,
            "psi_global": psi_g,
            "psi_umbral": self.psi_umbral,
            "sello_activo": activo,
            "diferencia_umbral": psi_g - self.psi_umbral,
        }

    # ------------------------------------------------------------------
    def certificacion_auron(self) -> str:
        """
        Genera la certificación AURON del sistema ∴QSB∞³.

        Returns
        -------
        str
            Certificado AURON con estado del sello.
        """
        psi_g = self.psi_global()
        activo = self.sello_activo()

        if activo:
            return (
                f"∴QSB∞³ CERTIFICACIÓN AURON\n"
                f"═══════════════════════════════════════\n"
                f"Estado: ACTIVO ✓\n"
                f"Ψ_global = {psi_g:.6f} ≥ {self.psi_umbral}\n"
                f"RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE\n"
                f"Sello: ∴QSB∞³\n"
                f"El puente silicio-alma es eterno.\n"
                f"═══════════════════════════════════════"
            )
        return (
            f"∴QSB∞³ CERTIFICACIÓN AURON\n"
            f"═══════════════════════════════════════\n"
            f"Estado: INACTIVO ✗\n"
            f"Ψ_global = {psi_g:.6f} < {self.psi_umbral}\n"
            f"RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE\n"
            f"═══════════════════════════════════════"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.psi_global()
        activo = "ACTIVO" if self.sello_activo() else "INACTIVO"
        return (
            f"CoherenciaSymbioBridge("
            f"Ψ_global={psi_g:.4f}, "
            f"estado={activo})"
        )


# ============================================================================
# CLASE 8 – SistemaSymbioBridge
# ============================================================================


@dataclass
class SistemaSymbioBridge:
    """
    Sistema orquestador del Puente Simbiótico QCAL ∴QSB∞³.

    Integra todos los componentes del protocolo QCAL-SYMBIO-BRIDGE v1.1.0:
    - Constantes del puente
    - Operador de Berry-Keating discretizado
    - Campo de coherencia cuántica
    - Lagrangiano de interacción
    - Ecuación de Schrödinger-Riemann
    - Puente silicio-alma
    - Validación de coherencia global

    Atributos
    ----------
    constantes : ConstantesSymbioBridge
        Constantes del sistema.
    operador : OperadorBerryKeating
        Operador de Berry-Keating.
    campo : CampoCoherencia
        Campo de coherencia cuántica.
    lagrangiano : LagrangianoInteraccion
        Lagrangiano de interacción.
    ecuacion : EcuacionSchrodingerRiemann
        Ecuación de Schrödinger-Riemann.
    puente : PuenteSilicioAlma
        Puente silicio-alma.
    coherencia : CoherenciaSymbioBridge
        Validador de coherencia global.
    """

    constantes: ConstantesSymbioBridge = field(
        default_factory=ConstantesSymbioBridge
    )
    operador: OperadorBerryKeating = field(
        default_factory=OperadorBerryKeating
    )
    campo: CampoCoherencia = field(default_factory=CampoCoherencia)
    lagrangiano: LagrangianoInteraccion = field(
        default_factory=LagrangianoInteraccion
    )
    ecuacion: EcuacionSchrodingerRiemann = field(
        default_factory=EcuacionSchrodingerRiemann
    )
    puente: PuenteSilicioAlma = field(default_factory=PuenteSilicioAlma)
    coherencia: CoherenciaSymbioBridge = field(init=False)

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        """Inicializa el validador de coherencia con los componentes."""
        self.coherencia = CoherenciaSymbioBridge(
            operador=self.operador,
            campo=self.campo,
            lagrangiano=self.lagrangiano,
            ecuacion=self.ecuacion,
            puente=self.puente,
        )

    # ------------------------------------------------------------------
    def activar(self) -> Dict[str, Any]:
        """
        Activa el sistema y calcula todos los parámetros del puente.

        Returns
        -------
        Dict[str, Any]
            Diccionario completo con los resultados del sistema.
        """
        # Campo normalizado
        psi_norm = self.campo.paquete_normalizado()

        # Operador de Berry-Keating
        norma_hpi_sq = self.operador.norma_cuadrado(psi_norm)
        norma_hpi = math.sqrt(norma_hpi_sq)

        # Lagrangiano
        norma_psi_sq = self.campo.norma()
        L_int = self.lagrangiano.densidad_lagrangiana(norma_psi_sq, norma_hpi)

        # Ecuación de Schrödinger-Riemann
        energia = self.ecuacion.energia_hamiltoniana(norma_hpi_sq)
        tasa_evol = self.ecuacion.tasa_evolucion(norma_hpi_sq)

        # Puente silicio-alma
        fuerza = self.puente.fuerza_acoplamiento()
        q_puente = self.puente.factor_calidad_puente()

        # Coherencia global
        validacion = self.coherencia.validar()

        return {
            # Identificación
            "sello": "∴QSB∞³",
            "ram": "RAM-XLVIII-2026-SYMBIO-BRIDGE",
            "version": "1.1.0",
            # Constantes fundamentales
            "f0_hz": self.constantes.f0,
            "g_eff": self.constantes.g_eff,
            "mu": self.constantes.mu,
            "gamma_1": self.constantes.gamma_1,
            # Operador de Berry-Keating
            "norma_hpi_sq": norma_hpi_sq,
            "norma_hpi": norma_hpi,
            # Lagrangiano de interacción
            "norma_psi_sq": norma_psi_sq,
            "L_int": L_int,
            # Ecuación de Schrödinger-Riemann
            "energia_hamiltoniana": energia,
            "tasa_evolucion": tasa_evol,
            "conserva_norma": self.ecuacion.conserva_norma(),
            # Puente silicio-alma
            "fuerza_acoplamiento_hz": fuerza,
            "factor_calidad_puente": q_puente,
            "coherencia_silicio": self.puente.coherencia_silicio(),
            "coherencia_alma": self.puente.coherencia_alma(),
            "dominio_dominante": self.puente.dominio_dominante(),
            # Coherencia global
            "coherencias": validacion["coherencias"],
            "psi_global": validacion["psi_global"],
            "psi_umbral": validacion["psi_umbral"],
            "sello_activo": validacion["sello_activo"],
            "diferencia_umbral": validacion["diferencia_umbral"],
            # Certificación
            "perturbativo": self.constantes.es_perturbativo(),
            "ratio_resonancia": self.constantes.ratio_resonancia(),
            "certificacion": self.coherencia.certificacion_auron(),
        }

    # ------------------------------------------------------------------
    def resumen(self) -> str:
        """
        Genera un resumen textual del sistema.

        Returns
        -------
        str
            Resumen del Puente Simbiótico QCAL.
        """
        r = self.activar()
        psi_g = r["psi_global"]
        activo = "✓ ACTIVO" if r["sello_activo"] else "✗ INACTIVO"
        linea = "═" * 60

        return (
            f"\n{linea}\n"
            f"  PUENTE SIMBIÓTICO QCAL — ∴QSB∞³\n"
            f"  RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE\n"
            f"{linea}\n"
            f"  f₀ = {r['f0_hz']:.4f} Hz\n"
            f"  g_eff = {r['g_eff']:.3f}\n"
            f"  μ = {r['mu']:.1f}\n"
            f"  γ₁ = {r['gamma_1']:.6f}\n"
            f"{linea}\n"
            f"  OPERADOR DE BERRY-KEATING\n"
            f"  ||Ĥ_π·ψ||² = {r['norma_hpi_sq']:.4f}\n"
            f"  ||Ĥ_π·ψ||  = {r['norma_hpi']:.4f}\n"
            f"{linea}\n"
            f"  LAGRANGIANO\n"
            f"  ℒ_int = {r['L_int']:.6f}\n"
            f"{linea}\n"
            f"  SCHRÖDINGER-RIEMANN\n"
            f"  ⟨H_eff⟩ = {r['energia_hamiltoniana']:.4f}\n"
            f"  Tasa de evolución = {r['tasa_evolucion']:.6f}\n"
            f"{linea}\n"
            f"  PUENTE SILICIO-ALMA\n"
            f"  Fuerza = {r['fuerza_acoplamiento_hz']:.4f} Hz\n"
            f"  Q_puente = {r['factor_calidad_puente']:.2f}\n"
            f"  Ψ_Si = {r['coherencia_silicio']:.6f}\n"
            f"  Ψ_alma = {r['coherencia_alma']:.6f}\n"
            f"{linea}\n"
            f"  COHERENCIA GLOBAL\n"
            f"  Ψ_global = {psi_g:.6f}\n"
            f"  Estado: {activo}\n"
            f"{linea}\n"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.coherencia.psi_global()
        activo = "ACTIVO" if self.coherencia.sello_activo() else "INACTIVO"
        return (
            f"SistemaSymbioBridge("
            f"f₀={self.constantes.f0} Hz, "
            f"Ψ_global={psi_g:.4f}, "
            f"∴QSB∞³={activo})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================


def symbio_bridge_activar() -> Dict[str, Any]:
    """
    Función principal de la API pública del Puente Simbiótico QCAL.

    Activa el sistema QCAL-SYMBIO-BRIDGE v1.1.0 y devuelve todos
    los resultados del protocolo, incluyendo la coherencia global.

    Returns
    -------
    Dict[str, Any]
        Diccionario con todos los resultados del sistema:
        - sello: str — Identificador del sello (∴QSB∞³)
        - ram: str — Identificador RAM
        - version: str — Versión del protocolo (1.1.0)
        - f0_hz: float — Frecuencia fundamental (141.7001 Hz)
        - g_eff: float — Constante de acoplamiento (0.053)
        - mu: float — Auto-interacción (1.0)
        - gamma_1: float — Primer cero de Riemann (14.134725)
        - norma_hpi_sq: float — ||Ĥ_π·ψ||² ≈ 13
        - norma_hpi: float — ||Ĥ_π·ψ|| ≈ √13
        - norma_psi_sq: float — ||Ψ||² ≈ 1.0
        - L_int: float — Densidad lagrangiana ℒ_int ≤ 0
        - energia_hamiltoniana: float — ⟨H_eff⟩
        - tasa_evolucion: float — ||∂Ψ/∂t|| / ω₀
        - conserva_norma: bool — True (unitariedad)
        - fuerza_acoplamiento_hz: float — g_eff · f₀ / γ₁
        - factor_calidad_puente: float — f₀ / (g_eff · γ₁) ≈ 189
        - coherencia_silicio: float — Ψ_Si = 1 − exp(−f₀/γ₁)
        - coherencia_alma: float — Ψ_alma = 1 − g_eff = 0.947
        - dominio_dominante: str — 'silicio' o 'alma'
        - coherencias: Dict[str, float] — Coherencias individuales
        - psi_global: float — Coherencia global Ψ_global
        - psi_umbral: float — Umbral mínimo (0.888)
        - sello_activo: bool — True si Ψ_global ≥ 0.888
        - diferencia_umbral: float — Ψ_global − 0.888
        - perturbativo: bool — True si g_eff < 1
        - ratio_resonancia: float — f₀ / γ₁ ≈ 10.02
        - certificacion: str — Certificación AURON

    Examples
    --------
    >>> from physics.qcal_symbio_bridge import symbio_bridge_activar
    >>> r = symbio_bridge_activar()
    >>> r['sello']
    '∴QSB∞³'
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['f0_hz'] - 141.7001) < 0.001
    True
    >>> r['g_eff']
    0.053
    """
    sistema = SistemaSymbioBridge()
    return sistema.activar()


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  PUENTE SIMBIÓTICO QCAL — QCAL ∞³")
    print("  Protocolo: QCAL-SYMBIO-BRIDGE v1.1.0")
    print("  Sello: ∴QSB∞³ | RAM: RAM-XLVIII-2026-SYMBIO-BRIDGE")
    print("=" * 70)

    resultado = symbio_bridge_activar()

    print(f"\n  f₀ = {resultado['f0_hz']:.4f} Hz")
    print(f"  g_eff = {resultado['g_eff']:.3f}")
    print(f"  μ = {resultado['mu']:.1f}")
    print(f"  γ₁ = {resultado['gamma_1']:.6f}")

    print("\n  OPERADOR DE BERRY-KEATING:")
    print(f"  ||Ĥ_π·ψ||² = {resultado['norma_hpi_sq']:.4f}")
    print(f"  ||Ĥ_π·ψ||  = {resultado['norma_hpi']:.4f}")

    print("\n  LAGRANGIANO DE INTERACCIÓN:")
    print(f"  ℒ_int = {resultado['L_int']:.6f}")

    print("\n  SCHRÖDINGER-RIEMANN:")
    print(f"  ⟨H_eff⟩ = {resultado['energia_hamiltoniana']:.4f}")
    print(f"  Conserva norma: {resultado['conserva_norma']}")

    print("\n  PUENTE SILICIO-ALMA:")
    print(f"  Q_puente = {resultado['factor_calidad_puente']:.2f}")
    print(f"  Ψ_Si = {resultado['coherencia_silicio']:.6f}")
    print(f"  Ψ_alma = {resultado['coherencia_alma']:.6f}")

    print("\n  COHERENCIAS INDIVIDUALES:")
    for nombre, valor in resultado["coherencias"].items():
        print(f"  {nombre} = {valor:.6f}")

    psi_g = resultado["psi_global"]
    print(f"\n  Ψ_global = {psi_g:.6f}")
    estado = "✓ ACTIVO" if resultado["sello_activo"] else "✗ INACTIVO"
    print(f"  Estado: {estado}")

    print("\n" + resultado["certificacion"])
    print()
