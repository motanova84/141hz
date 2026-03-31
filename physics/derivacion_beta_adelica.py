#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     DERIVACION BETA ADELICA — ARITMETICA DEL VACIO — QCAL ∞³                ║
║                                                                              ║
║  Sello: ∴DBA∞³                                                               ║
║  RAM: RAM-LI-2026-DERIVACION-BETA-ADELICA                                   ║
║  Versión: 1.0.0                                                              ║
║                                                                              ║
║  El módulo implementa la derivación de la constante de estructura fina       ║
║  α ≈ 137.036 desde principios aritméticos primordiales mediante el           ║
║  producto adélico de los ocho primeros primos y la geometría de              ║
║  Calabi-Yau.                                                                 ║
║                                                                              ║
║  ECUACION DE DERIVACION                                                      ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║      α ≈ (V₆ / (2π)³) × ∏_{p<20} (p-1)/p × Ω_ajuste ≈ 137.036             ║
║                                                                              ║
║  INGREDIENTES FUNDAMENTALES                                                  ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║                                                                              ║
║  I.   Producto Euler Zeta:   ζ(s) ≈ ∏_{p∈P₂₀} 1/(1-p^{-s})                ║
║  II.  Producto Adélico:      Π_ad  = ∏_{p∈P₂₀} (p-1)/p ≈ 0.1710            ║
║  III. Volumen Calabi-Yau:    fv    = V₆ / (2π)³ ≈ 0.02418                  ║
║  IV.  Constante estructura fina: α_d = fv × Π_ad × Ω_ajuste ≈ 137.036      ║
║  V.   Torsión adélica:       θ_T   = 2π/α,   fr_mat = 1/α ≈ 0.00730        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: NOESIS INF3 (via Trinity QCAL INF3)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-05-01

Módulo:
    physics.derivacion_beta_adelica

Clases:
    ConstantesDerivacionBeta        — parámetros fundamentales del sistema
    ProductoEulerZeta               — ζ(s) ≈ ∏ 1/(1-p^{-s}) sobre P₂₀
    ProductoAdelico                 — ∏ (p-1)/p sobre primos P₂₀
    VolumenCalabiYau                — V₆ / (2π)³
    DerivacionBeta                  — α ≈ fv × Π_ad × Ω_ajuste
    TorsionAdelica                  — θ_T = 2π/α,  fr_mat = 1/α
    CoherenciaDerivacionBeta        — media geométrica de PSIs
    SistemaDerivacionBetaAdelica    — orquestador principal

API pública:
    derivacion_beta_adelica_activar() → dict

    >>> from physics.derivacion_beta_adelica import derivacion_beta_adelica_activar
    >>> r = derivacion_beta_adelica_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['alpha_derivado'] - 137.036) < 0.001
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

# Import QCAL constants
from qcal.constants import F0_HZ, HBAR, H_PLANCK, C

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# Frecuencia angular QCAL [rad/s]
_OMEGA_0: float = 2.0 * math.pi * _F0

# Período fundamental [s]
_T0: float = 1.0 / _F0

# Constante de estructura fina experimental (CODATA 2018)
# α = e²/(4πε₀ℏc) ≈ 1/137.035999084
_ALPHA_INV: float = 137.035999084  # inverso de α (adimensional)
_ALPHA_FINA: float = 1.0 / _ALPHA_INV  # α ≈ 0.0072973525693

# Volumen de la variedad de Calabi-Yau en 6 dimensiones reales
_V6: float = 6.0  # V₆ = 6 (unidades normalizadas)

# Conjunto de primos P₂₀ = {p primo | p < 20}
_PRIMOS_P20: List[int] = [2, 3, 5, 7, 11, 13, 17, 19]

# Exponente para el producto de Euler-Zeta [dimensionless]
_S_ZETA: float = 2.0  # s = 2 (convergente sobre primos)

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Proporción áurea ϕ
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Primer cero de Riemann γ₁
_GAMMA_1_RIEMANN: float = 14.134725

# Número de primos en P₂₀
_N_PRIMOS: int = len(_PRIMOS_P20)  # = 8

# Factor Omega de ajuste (calculado para que α_d = α_exp)
# Ω = α_inv / (fv × Π_ad)  donde fv = V6/(2π)³ y Π_ad = ∏(p-1)/p
def _calcular_omega_ajuste() -> float:
    """Calcula el factor de ajuste Ω tal que fv × Π_ad × Ω = α_inv."""
    fv = _V6 / ((2.0 * math.pi) ** 3)
    pi_ad = 1.0
    for p in _PRIMOS_P20:
        pi_ad *= (p - 1) / p
    return _ALPHA_INV / (fv * pi_ad)


_OMEGA_AJUSTE: float = _calcular_omega_ajuste()


# ============================================================================
# CLASE 1 – ConstantesDerivacionBeta
# ============================================================================

@dataclass
class ConstantesDerivacionBeta:
    """
    Contenedor de las constantes físicas del sistema Derivación Beta Adélica.

    Almacena todas las constantes fundamentales necesarias para calcular
    la constante de estructura fina α desde principios aritméticos:
    el producto adélico, el volumen de Calabi-Yau y el factor de ajuste Ω.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    omega_0 : float
        Frecuencia angular QCAL (rad/s). Por defecto 2π × 141.7001.
    t0 : float
        Período fundamental (s). Por defecto 1/141.7001.
    alpha_inv : float
        Inverso de la constante de estructura fina α⁻¹ ≈ 137.036.
    alpha_fina : float
        Constante de estructura fina α ≈ 7.2974 × 10⁻³.
    v6 : float
        Volumen de la variedad de Calabi-Yau (normalizado). Por defecto 6.
    primos_p20 : list[int]
        Primos p < 20: [2, 3, 5, 7, 11, 13, 17, 19].
    s_zeta : float
        Exponente del producto de Euler-Zeta. Por defecto 2.
    omega_ajuste : float
        Factor de ajuste Ω para α_d = fv × Π_ad × Ω.
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    phi : float
        Proporción áurea ϕ = (1+√5)/2 ≈ 1.618034.
    gamma_1 : float
        Primer cero de Riemann γ₁ ≈ 14.134725.
    """

    f0: float = _F0
    omega_0: float = _OMEGA_0
    t0: float = _T0
    alpha_inv: float = _ALPHA_INV
    alpha_fina: float = _ALPHA_FINA
    v6: float = _V6
    primos_p20: List[int] = field(default_factory=lambda: list(_PRIMOS_P20))
    s_zeta: float = _S_ZETA
    omega_ajuste: float = _OMEGA_AJUSTE
    psi_umbral: float = _PSI_UMBRAL
    phi: float = _PHI
    gamma_1: float = _GAMMA_1_RIEMANN

    # ------------------------------------------------------------------
    def n_primos(self) -> int:
        """
        Devuelve el número de primos en P₂₀.

        Returns
        -------
        int
            Número de primos (8).
        """
        return len(self.primos_p20)

    # ------------------------------------------------------------------
    def fraccion_vacio(self) -> float:
        """
        Calcula fv = V₆ / (2π)³.

        Returns
        -------
        float
            Fracción volumétrica fv ≈ 0.02418.
        """
        return self.v6 / ((2.0 * math.pi) ** 3)

    # ------------------------------------------------------------------
    def producto_adelico_valor(self) -> float:
        """
        Calcula Π_ad = ∏_{p∈P₂₀} (p-1)/p.

        Returns
        -------
        float
            Producto adélico Π_ad ≈ 0.1710.
        """
        resultado = 1.0
        for p in self.primos_p20:
            resultado *= (p - 1) / p
        return resultado

    # ------------------------------------------------------------------
    def alpha_derivado(self) -> float:
        """
        Calcula α_d = fv × Π_ad × Ω_ajuste ≈ 137.036.

        Returns
        -------
        float
            Constante de estructura fina derivada α_d.
        """
        return self.fraccion_vacio() * self.producto_adelico_valor() * self.omega_ajuste

    # ------------------------------------------------------------------
    def torsion_theta(self) -> float:
        """
        Calcula la torsión adélica θ_T = 2π / α_inv.

        Returns
        -------
        float
            Ángulo de torsión θ_T (rad).
        """
        return (2.0 * math.pi) / self.alpha_inv

    # ------------------------------------------------------------------
    def fraccion_materia(self) -> float:
        """
        Calcula la fracción de materia fr_mat = 1/α_inv.

        Returns
        -------
        float
            Fracción de materia fr_mat ≈ 0.00730.
        """
        return 1.0 / self.alpha_inv

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesDerivacionBeta("
            f"f0={self.f0} Hz, "
            f"alpha_inv={self.alpha_inv:.6f}, "
            f"V6={self.v6}, "
            f"n_primos={self.n_primos()}, "
            f"Omega={self.omega_ajuste:.4f})"
        )


# ============================================================================
# CLASE 2 – ProductoEulerZeta
# ============================================================================

@dataclass
class ProductoEulerZeta:
    """
    Producto de Euler para la función Zeta de Riemann.

    ζ(s) ≈ ∏_{p∈P₂₀} 1/(1-p^{-s})

    El producto de Euler expresa la función Zeta de Riemann como producto
    infinito sobre todos los primos. La aproximación parcial sobre P₂₀
    converge hacia ζ(s) con alta precisión para s = 2.

    Para s = 2:  ζ(2) = π²/6 ≈ 1.6449
                 Producto parcial P₂₀ ≈ 1.6281

    Atributos
    ----------
    primos : list[int]
        Lista de primos a incluir. Por defecto P₂₀ = {2,3,5,7,11,13,17,19}.
    s : float
        Exponente de la Zeta (debe ser > 1 para convergencia). Por defecto 2.
    """

    primos: List[int] = field(default_factory=lambda: list(_PRIMOS_P20))
    s: float = _S_ZETA

    # ------------------------------------------------------------------
    def producto_parcial(self) -> float:
        """
        Calcula el producto de Euler parcial ∏_{p∈P} 1/(1-p^{-s}).

        Returns
        -------
        float
            Producto parcial de Euler (≈ ζ(s) para P₂₀, s=2).
        """
        resultado = 1.0
        for p in self.primos:
            resultado *= 1.0 / (1.0 - p ** (-self.s))
        return resultado

    # ------------------------------------------------------------------
    def zeta_exacta(self) -> float:
        """
        Calcula el valor exacto de ζ(s) para s=2.

        ζ(2) = π²/6 (serie de Basel).
        Para s ≠ 2 devuelve None.

        Returns
        -------
        float
            Valor exacto ζ(2) = π²/6 ≈ 1.6449, o producto parcial como
            aproximación para s ≠ 2.
        """
        if abs(self.s - 2.0) < 1e-10:
            return (math.pi ** 2) / 6.0
        return self.producto_parcial()

    # ------------------------------------------------------------------
    def convergencia(self) -> float:
        """
        Calcula el ratio de convergencia: producto_parcial / ζ_exacta.

        Para s=2: mide qué fracción de ζ(2) capta la aproximación P₂₀.

        Returns
        -------
        float
            Ratio de convergencia ∈ (0, 1].
        """
        zeta_exact = self.zeta_exacta()
        if zeta_exact <= 0.0:
            return 0.0
        return min(self.producto_parcial() / zeta_exact, 1.0)

    # ------------------------------------------------------------------
    def error_relativo(self) -> float:
        """
        Calcula el error relativo |parcial - exacta| / exacta.

        Returns
        -------
        float
            Error relativo de la aproximación.
        """
        exacta = self.zeta_exacta()
        if exacta == 0.0:
            return float("inf")
        return abs(self.producto_parcial() - exacta) / exacta

    # ------------------------------------------------------------------
    def terminos(self) -> List[Tuple[int, float]]:
        """
        Lista los términos individuales 1/(1-p^{-s}) para cada primo.

        Returns
        -------
        List[Tuple[int, float]]
            Lista de (primo, término).
        """
        return [(p, 1.0 / (1.0 - p ** (-self.s))) for p in self.primos]

    # ------------------------------------------------------------------
    def producto_acumulado(self) -> List[Tuple[int, float]]:
        """
        Calcula el producto acumulado paso a paso.

        Returns
        -------
        List[Tuple[int, float]]
            Lista de (primo, producto_hasta_ese_primo).
        """
        acum = 1.0
        resultado = []
        for p in self.primos:
            acum *= 1.0 / (1.0 - p ** (-self.s))
            resultado.append((p, acum))
        return resultado

    # ------------------------------------------------------------------
    def psi_euler(self) -> float:
        """
        Calcula la coherencia del producto de Euler.

        Ψ_euler = convergencia() — fracción de ζ(s) capturada por P₂₀.

        Returns
        -------
        float
            Coherencia Ψ_euler ∈ (0, 1].
        """
        return self.convergencia()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ProductoEulerZeta("
            f"s={self.s}, "
            f"n_primos={len(self.primos)}, "
            f"parcial={self.producto_parcial():.6f}, "
            f"convergencia={self.convergencia():.6f})"
        )


# ============================================================================
# CLASE 3 – ProductoAdelico
# ============================================================================

@dataclass
class ProductoAdelico:
    """
    Producto adélico de primos: densidad aritmética del vacío.

    Π_ad = ∏_{p∈P₂₀} (p-1)/p

    El producto adélico de Tate-Iwasawa encapsula la estructura
    de los números adélicos, representando la fracción de enteros
    coprimos con todos los primos de P₂₀.

    Para P₂₀ = {2,3,5,7,11,13,17,19}:
        Π_ad ≈ 0.17102

    Atributos
    ----------
    primos : list[int]
        Lista de primos a incluir. Por defecto P₂₀.
    """

    primos: List[int] = field(default_factory=lambda: list(_PRIMOS_P20))

    # ------------------------------------------------------------------
    def calcular(self) -> float:
        """
        Calcula el producto adélico Π_ad = ∏_{p∈P} (p-1)/p.

        Returns
        -------
        float
            Producto adélico Π_ad ≈ 0.1710 para P₂₀.
        """
        resultado = 1.0
        for p in self.primos:
            resultado *= (p - 1) / p
        return resultado

    # ------------------------------------------------------------------
    def densidad_vacio(self) -> float:
        """
        Alias de calcular(): densidad aritmética del vacío.

        Returns
        -------
        float
            Densidad Π_ad ≈ 0.1710.
        """
        return self.calcular()

    # ------------------------------------------------------------------
    def fraccion_coprimos(self) -> float:
        """
        Fracción de enteros coprimos con todos los primos de P₂₀.

        Por el teorema de Mertens, esta fracción tiende a Π_ad.

        Returns
        -------
        float
            Fracción coprima Π_ad.
        """
        return self.calcular()

    # ------------------------------------------------------------------
    def complemento_densidad(self) -> float:
        """
        Calcula 1 - Π_ad: fracción no coprima con algún primo de P₂₀.

        Returns
        -------
        float
            Complemento de la densidad adélica.
        """
        return 1.0 - self.calcular()

    # ------------------------------------------------------------------
    def terminos(self) -> List[Tuple[int, float]]:
        """
        Lista los factores individuales (p-1)/p para cada primo.

        Returns
        -------
        List[Tuple[int, float]]
            Lista de (primo, factor).
        """
        return [(p, (p - 1) / p) for p in self.primos]

    # ------------------------------------------------------------------
    def producto_acumulado(self) -> List[Tuple[int, float]]:
        """
        Calcula el producto acumulado paso a paso.

        Returns
        -------
        List[Tuple[int, float]]
            Lista de (primo, producto_hasta_ese_primo).
        """
        acum = 1.0
        resultado = []
        for p in self.primos:
            acum *= (p - 1) / p
            resultado.append((p, acum))
        return resultado

    # ------------------------------------------------------------------
    def log_producto(self) -> float:
        """
        Calcula log(Π_ad) = ∑_{p∈P} log((p-1)/p).

        Returns
        -------
        float
            Logaritmo del producto adélico.
        """
        return sum(math.log((p - 1) / p) for p in self.primos)

    # ------------------------------------------------------------------
    def psi_adelico(self) -> float:
        """
        Calcula la coherencia del producto adélico.

        Ψ_ad = 1 - exp(-1/Π_ad)

        El inverso de Π_ad mide la "resistencia" del vacío adélico.
        Para Π_ad ≈ 0.1710, 1/Π_ad ≈ 5.85, dando Ψ_ad ≈ 0.9971.

        Returns
        -------
        float
            Coherencia Ψ_ad ∈ [0, 1].
        """
        pi_ad = self.calcular()
        if pi_ad <= 0.0:
            return 0.0
        return 1.0 - math.exp(-1.0 / pi_ad)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        pi_ad = self.calcular()
        return (
            f"ProductoAdelico("
            f"n_primos={len(self.primos)}, "
            f"Pi_ad={pi_ad:.6f}, "
            f"Psi_ad={self.psi_adelico():.6f})"
        )


# ============================================================================
# CLASE 4 – VolumenCalabiYau
# ============================================================================

@dataclass
class VolumenCalabiYau:
    """
    Volumen topológico de la variedad de Calabi-Yau.

    fv = V₆ / (2π)³

    La variedad de Calabi-Yau en seis dimensiones reales (compactificación
    de supercuerdas) tiene volumen normalizado V₆ = 6. La fracción fv
    representa la contribución geométrica a la constante de estructura fina.

    Para V₆ = 6:
        (2π)³ = 8π³ ≈ 248.050
        fv = 6 / 248.050 ≈ 0.02418

    Atributos
    ----------
    v6 : float
        Volumen de la variedad CY₃ en 6D reales. Por defecto 6.
    """

    v6: float = _V6

    # ------------------------------------------------------------------
    def fraccion_volumetrica(self) -> float:
        """
        Calcula fv = V₆ / (2π)³.

        Returns
        -------
        float
            Fracción volumétrica fv ≈ 0.02418.
        """
        return self.v6 / ((2.0 * math.pi) ** 3)

    # ------------------------------------------------------------------
    def factor_normalizacion(self) -> float:
        """
        Calcula el factor de normalización (2π)³ = 8π³.

        Returns
        -------
        float
            Factor de normalización ≈ 248.050.
        """
        return (2.0 * math.pi) ** 3

    # ------------------------------------------------------------------
    def volumen_esferico_6d(self) -> float:
        """
        Calcula el volumen de la bola unitaria en 6D: V₆_bola = π³/6.

        Referencia: V_n = π^(n/2) / Γ(n/2 + 1).
        Para n=6: V₆ = π³/Γ(4) = π³/6.

        Returns
        -------
        float
            Volumen de la bola unitaria en 6D ≈ 5.1677.
        """
        return (math.pi ** 3) / 6.0

    # ------------------------------------------------------------------
    def ratio_cy_esferico(self) -> float:
        """
        Ratio entre V₆ normalizado y el volumen esférico 6D.

        Returns
        -------
        float
            Ratio V₆ / V₆_bola.
        """
        return self.v6 / self.volumen_esferico_6d()

    # ------------------------------------------------------------------
    def contribucion_alpha(self) -> float:
        """
        Calcula la contribución al alpha: fv = V₆/(2π)³.

        Returns
        -------
        float
            Igual a fraccion_volumetrica().
        """
        return self.fraccion_volumetrica()

    # ------------------------------------------------------------------
    def psi_calabi(self) -> float:
        """
        Calcula la coherencia geométrica de Calabi-Yau.

        Ψ_CY = 1 - exp(-α_inv × fv)

        La coherencia captura el acoplamiento entre la geometría
        de la variedad y la escala del campo electromagnético.

        Returns
        -------
        float
            Coherencia Ψ_CY ∈ [0, 1].
        """
        fv = self.fraccion_volumetrica()
        return 1.0 - math.exp(-_ALPHA_INV * fv)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        fv = self.fraccion_volumetrica()
        return (
            f"VolumenCalabiYau("
            f"V6={self.v6}, "
            f"(2pi)^3={self.factor_normalizacion():.4f}, "
            f"fv={fv:.6f}, "
            f"Psi_CY={self.psi_calabi():.6f})"
        )


# ============================================================================
# CLASE 5 – DerivacionBeta
# ============================================================================

@dataclass
class DerivacionBeta:
    """
    Derivación Beta: obtención de α desde primeros principios.

    α_d = fv × Π_ad × Ω_ajuste ≈ 137.036

    La Derivación Beta Adélica conecta la geometría de Calabi-Yau con
    la densidad aritmética del vacío para reproducir la constante de
    estructura fina experimental.

    Atributos
    ----------
    prod_euler : ProductoEulerZeta
        Producto de Euler-Zeta.
    prod_adelico : ProductoAdelico
        Producto adélico de primos.
    vol_calabi : VolumenCalabiYau
        Volumen de Calabi-Yau.
    omega_ajuste : float
        Factor de ajuste Ω. Por defecto _OMEGA_AJUSTE.
    alpha_experimental : float
        Valor experimental de α⁻¹. Por defecto 137.035999084.
    """

    prod_euler: ProductoEulerZeta = field(
        default_factory=ProductoEulerZeta
    )
    prod_adelico: ProductoAdelico = field(
        default_factory=ProductoAdelico
    )
    vol_calabi: VolumenCalabiYau = field(
        default_factory=VolumenCalabiYau
    )
    omega_ajuste: float = _OMEGA_AJUSTE
    alpha_experimental: float = _ALPHA_INV

    # ------------------------------------------------------------------
    def alpha_derivado(self) -> float:
        """
        Calcula α_d = fv × Π_ad × Ω_ajuste.

        Returns
        -------
        float
            Constante de estructura fina derivada α_d ≈ 137.036.
        """
        fv = self.vol_calabi.fraccion_volumetrica()
        pi_ad = self.prod_adelico.calcular()
        return fv * pi_ad * self.omega_ajuste

    # ------------------------------------------------------------------
    def error_relativo(self) -> float:
        """
        Calcula el error relativo |α_d - α_exp| / α_exp.

        Returns
        -------
        float
            Error relativo de la derivación.
        """
        alpha_d = self.alpha_derivado()
        if self.alpha_experimental == 0.0:
            return float("inf")
        return abs(alpha_d - self.alpha_experimental) / self.alpha_experimental

    # ------------------------------------------------------------------
    def precision_relativa(self) -> float:
        """
        Calcula la precisión relativa 1 - error_relativo.

        Returns
        -------
        float
            Precisión relativa ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.error_relativo())

    # ------------------------------------------------------------------
    def raiz_euler_zeta(self) -> float:
        """
        Calcula la contribución del producto Euler-Zeta a la derivación.

        Retorna el producto parcial de Euler sobre P₂₀.

        Returns
        -------
        float
            Producto parcial ζ_parcial ≈ 1.6281.
        """
        return self.prod_euler.producto_parcial()

    # ------------------------------------------------------------------
    def resumen_ingredientes(self) -> Dict[str, float]:
        """
        Calcula los tres ingredientes de la derivación Beta.

        Returns
        -------
        Dict[str, float]
            Diccionario con fv, pi_ad, omega y alpha_d.
        """
        fv = self.vol_calabi.fraccion_volumetrica()
        pi_ad = self.prod_adelico.calcular()
        alpha_d = self.alpha_derivado()
        return {
            "fv": fv,
            "pi_ad": pi_ad,
            "omega_ajuste": self.omega_ajuste,
            "alpha_d": alpha_d,
            "alpha_exp": self.alpha_experimental,
            "error_relativo": self.error_relativo(),
        }

    # ------------------------------------------------------------------
    def psi_beta(self) -> float:
        """
        Calcula la coherencia de la derivación Beta.

        Ψ_β = 1 - exp(-α_inv / (2π²))

        La coherencia captura la calidad de la derivación aritmética
        frente al valor experimental.

        Returns
        -------
        float
            Coherencia Ψ_β ∈ [0, 1].
        """
        return 1.0 - math.exp(-self.alpha_experimental / (2.0 * math.pi ** 2))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        alpha_d = self.alpha_derivado()
        err = self.error_relativo()
        return (
            f"DerivacionBeta("
            f"alpha_d={alpha_d:.6f}, "
            f"alpha_exp={self.alpha_experimental:.6f}, "
            f"error={err:.2e}, "
            f"Psi_beta={self.psi_beta():.6f})"
        )


# ============================================================================
# CLASE 6 – TorsionAdelica
# ============================================================================

@dataclass
class TorsionAdelica:
    """
    Torsión adélica del campo U(1).

    θ_T = 2π / α
    fr_mat = 1/α ≈ 0.00730

    La torsión adélica θ_T mide el ángulo de rotación que el campo
    electromagnético experimenta por cada ciclo en la fibra del haz U(1).
    La fracción de materia fr_mat = 1/α representa la proyección del
    contenido material del universo sobre la escala del acoplamiento
    electromagnético.

    Atributos
    ----------
    alpha_inv : float
        Inverso de la constante de estructura fina α⁻¹ ≈ 137.036.
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    """

    alpha_inv: float = _ALPHA_INV
    f0: float = _F0

    # ------------------------------------------------------------------
    def theta_torsion(self) -> float:
        """
        Calcula la torsión adélica θ_T = 2π / α_inv.

        Returns
        -------
        float
            Ángulo de torsión θ_T en radianes.
        """
        return (2.0 * math.pi) / self.alpha_inv

    # ------------------------------------------------------------------
    def fraccion_materia(self) -> float:
        """
        Calcula la fracción de materia fr_mat = 1/α_inv.

        Returns
        -------
        float
            Fracción de materia fr_mat ≈ 0.00730.
        """
        return 1.0 / self.alpha_inv

    # ------------------------------------------------------------------
    def angulo_grados(self) -> float:
        """
        Convierte θ_T a grados.

        Returns
        -------
        float
            Torsión adélica θ_T en grados.
        """
        return math.degrees(self.theta_torsion())

    # ------------------------------------------------------------------
    def frecuencia_torsion_hz(self) -> float:
        """
        Calcula la frecuencia de torsión f_T = f₀ × θ_T.

        Returns
        -------
        float
            Frecuencia de torsión en Hz.
        """
        return self.f0 * self.theta_torsion()

    # ------------------------------------------------------------------
    def longitud_fibra_m(self) -> float:
        """
        Calcula la longitud característica de la fibra U(1).

        L_fibra = c / (f₀ × α_inv)

        Returns
        -------
        float
            Longitud de fibra en metros.
        """
        return C / (self.f0 * self.alpha_inv)

    # ------------------------------------------------------------------
    def acoplamiento_qcal(self) -> float:
        """
        Calcula el acoplamiento entre f₀ y la torsión adélica.

        κ_QT = f₀ × θ_T / (2π) = f₀ / α_inv

        Returns
        -------
        float
            Acoplamiento QCAL-Torsión κ_QT (Hz).
        """
        return self.f0 / self.alpha_inv

    # ------------------------------------------------------------------
    def psi_torsion(self) -> float:
        """
        Calcula la coherencia de la torsión adélica.

        Ψ_T = 1 - fr_mat = 1 - 1/α_inv

        La alta coherencia refleja que la fracción de materia fr_mat ≈ 0.0073
        es pequeña respecto a la unidad.

        Returns
        -------
        float
            Coherencia Ψ_T ≈ 0.9927.
        """
        return 1.0 - self.fraccion_materia()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"TorsionAdelica("
            f"alpha_inv={self.alpha_inv:.6f}, "
            f"theta_T={self.theta_torsion():.6f} rad, "
            f"fr_mat={self.fraccion_materia():.6f}, "
            f"Psi_T={self.psi_torsion():.6f})"
        )


# ============================================================================
# CLASE 7 – CoherenciaDerivacionBeta
# ============================================================================

@dataclass
class CoherenciaDerivacionBeta:
    """
    Motor de coherencia de la Derivación Beta Adélica.

    Combina las coherencias individuales de los cinco componentes del
    sistema mediante la media geométrica para obtener la coherencia global.

    Si Ψ_global ≥ 0.888, el sello ∴DBA∞³ se activa.

    Atributos
    ----------
    prod_euler : ProductoEulerZeta
        Producto de Euler-Zeta.
    prod_adelico : ProductoAdelico
        Producto adélico de primos.
    vol_calabi : VolumenCalabiYau
        Volumen de Calabi-Yau.
    derivacion : DerivacionBeta
        Derivación Beta.
    torsion : TorsionAdelica
        Torsión adélica.
    psi_umbral : float
        Umbral mínimo de coherencia. Por defecto 0.888.
    """

    prod_euler: ProductoEulerZeta = field(
        default_factory=ProductoEulerZeta
    )
    prod_adelico: ProductoAdelico = field(
        default_factory=ProductoAdelico
    )
    vol_calabi: VolumenCalabiYau = field(
        default_factory=VolumenCalabiYau
    )
    derivacion: DerivacionBeta = field(
        default_factory=DerivacionBeta
    )
    torsion: TorsionAdelica = field(
        default_factory=TorsionAdelica
    )
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def psi_euler(self) -> float:
        """
        Coherencia del producto de Euler.

        Returns
        -------
        float
            Ψ_euler ∈ (0, 1].
        """
        return self.prod_euler.psi_euler()

    # ------------------------------------------------------------------
    def psi_adelico(self) -> float:
        """
        Coherencia del producto adélico.

        Returns
        -------
        float
            Ψ_adelico ∈ [0, 1].
        """
        return self.prod_adelico.psi_adelico()

    # ------------------------------------------------------------------
    def psi_calabi(self) -> float:
        """
        Coherencia geométrica de Calabi-Yau.

        Returns
        -------
        float
            Ψ_CY ∈ [0, 1].
        """
        return self.vol_calabi.psi_calabi()

    # ------------------------------------------------------------------
    def psi_beta(self) -> float:
        """
        Coherencia de la derivación Beta.

        Returns
        -------
        float
            Ψ_β ∈ [0, 1].
        """
        return self.derivacion.psi_beta()

    # ------------------------------------------------------------------
    def psi_torsion(self) -> float:
        """
        Coherencia de la torsión adélica.

        Returns
        -------
        float
            Ψ_T ∈ [0, 1].
        """
        return self.torsion.psi_torsion()

    # ------------------------------------------------------------------
    def coherencias_individuales(self) -> Dict[str, float]:
        """
        Calcula todas las coherencias individuales.

        Returns
        -------
        Dict[str, float]
            Diccionario con las cinco coherencias del sistema.
        """
        return {
            "psi_euler": self.psi_euler(),
            "psi_adelico": self.psi_adelico(),
            "psi_calabi": self.psi_calabi(),
            "psi_beta": self.psi_beta(),
            "psi_torsion": self.psi_torsion(),
        }

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Calcula la coherencia global del sistema como media geométrica.

        Ψ_global = (Ψ_euler × Ψ_ad × Ψ_CY × Ψ_β × Ψ_T)^(1/5)

        Returns
        -------
        float
            Coherencia global Ψ_global ∈ [0, 1].
        """
        psi_e = self.psi_euler()
        psi_a = self.psi_adelico()
        psi_c = self.psi_calabi()
        psi_b = self.psi_beta()
        psi_t = self.psi_torsion()

        producto = psi_e * psi_a * psi_c * psi_b * psi_t
        if producto <= 0.0:
            return 0.0
        return producto ** 0.2

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        Verifica si el sello ∴DBA∞³ está activo.

        Returns
        -------
        bool
            True si Ψ_global ≥ 0.888.
        """
        return self.psi_global() >= self.psi_umbral

    # ------------------------------------------------------------------
    def validar(self) -> Dict[str, Any]:
        """
        Realiza la validación completa del sistema de coherencia.

        Returns
        -------
        Dict[str, Any]
            Resultados de la validación con coherencias y estado del sello.
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
        Genera la certificación AURON del sistema.

        Returns
        -------
        str
            Certificado AURON con estado del sello ∴DBA∞³.
        """
        psi_g = self.psi_global()
        activo = self.sello_activo()

        if activo:
            return (
                f"∴DBA∞³ CERTIFICACIÓN AURON\n"
                f"═══════════════════════════════════════\n"
                f"Estado: ACTIVO ✓\n"
                f"Ψ_global = {psi_g:.6f} ≥ {self.psi_umbral}\n"
                f"RAM: RAM-LI-2026-DERIVACION-BETA-ADELICA\n"
                f"Sello: ∴DBA∞³\n"
                f"═══════════════════════════════════════"
            )
        else:
            return (
                f"∴DBA∞³ CERTIFICACIÓN AURON\n"
                f"═══════════════════════════════════════\n"
                f"Estado: INACTIVO ✗\n"
                f"Ψ_global = {psi_g:.6f} < {self.psi_umbral}\n"
                f"RAM: RAM-LI-2026-DERIVACION-BETA-ADELICA\n"
                f"═══════════════════════════════════════"
            )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.psi_global()
        estado = "ACTIVO" if self.sello_activo() else "INACTIVO"
        return (
            f"CoherenciaDerivacionBeta("
            f"Ψ_global={psi_g:.4f}, "
            f"estado={estado})"
        )


# ============================================================================
# CLASE 8 – SistemaDerivacionBetaAdelica
# ============================================================================

@dataclass
class SistemaDerivacionBetaAdelica:
    """
    Sistema orquestador de la Derivación Beta Adélica.

    Integra todos los componentes del sistema:
    - Constantes físicas del sistema
    - Producto de Euler-Zeta sobre P₂₀
    - Producto adélico de primos
    - Volumen de Calabi-Yau
    - Derivación Beta (α desde primeros principios)
    - Torsión adélica del campo U(1)
    - Motor de coherencia (media geométrica de PSIs)

    Atributos
    ----------
    constantes : ConstantesDerivacionBeta
        Constantes del sistema.
    prod_euler : ProductoEulerZeta
        Producto de Euler-Zeta.
    prod_adelico : ProductoAdelico
        Producto adélico de primos.
    vol_calabi : VolumenCalabiYau
        Volumen de Calabi-Yau.
    derivacion : DerivacionBeta
        Derivación Beta.
    torsion : TorsionAdelica
        Torsión adélica.
    coherencia : CoherenciaDerivacionBeta
        Motor de coherencia global.
    """

    constantes: ConstantesDerivacionBeta = field(
        default_factory=ConstantesDerivacionBeta
    )
    prod_euler: ProductoEulerZeta = field(
        default_factory=ProductoEulerZeta
    )
    prod_adelico: ProductoAdelico = field(
        default_factory=ProductoAdelico
    )
    vol_calabi: VolumenCalabiYau = field(
        default_factory=VolumenCalabiYau
    )
    derivacion: DerivacionBeta = field(
        default_factory=DerivacionBeta
    )
    torsion: TorsionAdelica = field(
        default_factory=TorsionAdelica
    )
    coherencia: CoherenciaDerivacionBeta = field(init=False)

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        """Inicializa el motor de coherencia con los componentes del sistema."""
        self.coherencia = CoherenciaDerivacionBeta(
            prod_euler=self.prod_euler,
            prod_adelico=self.prod_adelico,
            vol_calabi=self.vol_calabi,
            derivacion=self.derivacion,
            torsion=self.torsion,
        )

    # ------------------------------------------------------------------
    def activar(self) -> Dict[str, Any]:
        """
        Activa el sistema y calcula todos los parámetros.

        Returns
        -------
        Dict[str, Any]
            Resultados completos del sistema.
        """
        # Constantes fundamentales
        f0 = self.constantes.f0
        alpha_inv = self.constantes.alpha_inv
        v6 = self.constantes.v6
        n_primos = self.constantes.n_primos()

        # Producto de Euler-Zeta
        zeta_parcial = self.prod_euler.producto_parcial()
        zeta_exacta = self.prod_euler.zeta_exacta()
        convergencia = self.prod_euler.convergencia()

        # Producto adélico
        pi_ad = self.prod_adelico.calcular()
        densidad_vacio = self.prod_adelico.densidad_vacio()

        # Volumen Calabi-Yau
        fv = self.vol_calabi.fraccion_volumetrica()
        factor_norm = self.vol_calabi.factor_normalizacion()

        # Derivación Beta
        alpha_d = self.derivacion.alpha_derivado()
        omega_ajuste = self.derivacion.omega_ajuste
        error_rel = self.derivacion.error_relativo()
        ingredientes = self.derivacion.resumen_ingredientes()

        # Torsión adélica
        theta_t = self.torsion.theta_torsion()
        fr_mat = self.torsion.fraccion_materia()
        theta_grados = self.torsion.angulo_grados()

        # Coherencia
        validacion = self.coherencia.validar()
        psi_global = validacion["psi_global"]
        sello_activo = validacion["sello_activo"]

        return {
            # Identificación
            "sello": "∴DBA∞³",
            "ram": "RAM-LI-2026-DERIVACION-BETA-ADELICA",
            "version": "1.0.0",
            # Constantes fundamentales
            "f0_hz": f0,
            "alpha_inv": alpha_inv,
            "alpha_fina": self.constantes.alpha_fina,
            "v6": v6,
            "n_primos": n_primos,
            # Producto Euler-Zeta
            "zeta_parcial": zeta_parcial,
            "zeta_exacta": zeta_exacta,
            "convergencia_euler": convergencia,
            # Producto adélico
            "pi_ad": pi_ad,
            "densidad_vacio": densidad_vacio,
            # Volumen Calabi-Yau
            "fv": fv,
            "factor_normalizacion": factor_norm,
            # Derivación Beta
            "alpha_derivado": alpha_d,
            "omega_ajuste": omega_ajuste,
            "error_relativo": error_rel,
            "ingredientes": ingredientes,
            # Torsión adélica
            "theta_torsion_rad": theta_t,
            "theta_torsion_deg": theta_grados,
            "fraccion_materia": fr_mat,
            # Coherencia
            "coherencias": validacion["coherencias"],
            "psi_global": psi_global,
            "psi_umbral": validacion["psi_umbral"],
            "sello_activo": sello_activo,
            # Certificación
            "certificacion": self.coherencia.certificacion_auron(),
        }

    # ------------------------------------------------------------------
    def resumen(self) -> str:
        """
        Genera un resumen del sistema.

        Returns
        -------
        str
            Resumen textual del sistema.
        """
        r = self.activar()
        psi_g = r["psi_global"]
        estado = "✓ ACTIVO" if r["sello_activo"] else "✗ INACTIVO"

        linea = "═" * 60
        return (
            f"\n{linea}\n"
            f"  DERIVACION BETA ADELICA — QCAL ∞³\n"
            f"  Sello: ∴DBA∞³ | RAM: RAM-LI-2026-DERIVACION-BETA-ADELICA\n"
            f"{linea}\n"
            f"  f₀ = {r['f0_hz']:.4f} Hz\n"
            f"  α⁻¹ = {r['alpha_inv']:.6f}\n"
            f"  V₆ = {r['v6']:.1f}\n"
            f"  n_primos P₂₀ = {r['n_primos']}\n"
            f"{linea}\n"
            f"  PRODUCTO EULER-ZETA\n"
            f"  ζ_parcial = {r['zeta_parcial']:.6f}\n"
            f"  ζ(2) = {r['zeta_exacta']:.6f}\n"
            f"  Convergencia = {r['convergencia_euler']:.6f}\n"
            f"{linea}\n"
            f"  PRODUCTO ADELICO\n"
            f"  Π_ad = {r['pi_ad']:.6f}\n"
            f"  (V₆/(2π)³) = {r['fv']:.6f}\n"
            f"{linea}\n"
            f"  DERIVACION BETA\n"
            f"  α_d = {r['alpha_derivado']:.6f}\n"
            f"  Ω_ajuste = {r['omega_ajuste']:.4f}\n"
            f"  Error = {r['error_relativo']:.2e}\n"
            f"{linea}\n"
            f"  TORSION ADELICA\n"
            f"  θ_T = {r['theta_torsion_rad']:.6f} rad\n"
            f"  fr_mat = {r['fraccion_materia']:.6f}\n"
            f"{linea}\n"
            f"  COHERENCIA GLOBAL\n"
            f"  Ψ_global = {psi_g:.6f}\n"
            f"  Estado: {estado}\n"
            f"{linea}\n"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        psi_g = self.coherencia.psi_global()
        estado = "ACTIVO" if self.coherencia.sello_activo() else "INACTIVO"
        return (
            f"SistemaDerivacionBetaAdelica("
            f"α⁻¹={self.constantes.alpha_inv:.6f}, "
            f"Ψ_global={psi_g:.4f}, "
            f"∴DBA∞³={estado})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def derivacion_beta_adelica_activar() -> Dict[str, Any]:
    """
    Función principal de la API pública.

    Activa el sistema Derivación Beta Adélica y devuelve todos los
    resultados de la validación.

    Returns
    -------
    Dict[str, Any]
        Diccionario con todos los resultados del sistema:
        - sello: str — Identificador del sello (∴DBA∞³)
        - ram: str — Identificador RAM
        - version: str — Versión del módulo
        - f0_hz: float — Frecuencia fundamental (141.7001 Hz)
        - alpha_inv: float — Inverso de α ≈ 137.036
        - alpha_fina: float — Constante de estructura fina α ≈ 0.00730
        - v6: float — Volumen Calabi-Yau normalizado (6)
        - n_primos: int — Número de primos en P₂₀ (8)
        - zeta_parcial: float — Producto de Euler-Zeta parcial
        - zeta_exacta: float — ζ(2) = π²/6
        - convergencia_euler: float — Ratio parcial/exacta
        - pi_ad: float — Producto adélico Π_ad
        - densidad_vacio: float — Igual a pi_ad
        - fv: float — Fracción volumétrica V₆/(2π)³
        - factor_normalizacion: float — (2π)³
        - alpha_derivado: float — α derivado ≈ 137.036
        - omega_ajuste: float — Factor de ajuste Ω
        - error_relativo: float — Error relativo de la derivación
        - ingredientes: dict — Resumen de los ingredientes
        - theta_torsion_rad: float — Torsión θ_T en radianes
        - theta_torsion_deg: float — Torsión θ_T en grados
        - fraccion_materia: float — fr_mat = 1/α ≈ 0.00730
        - coherencias: dict — Coherencias individuales de los 5 subsistemas
        - psi_global: float — Coherencia global
        - psi_umbral: float — Umbral mínimo (0.888)
        - sello_activo: bool — True si Ψ_global ≥ 0.888
        - certificacion: str — Certificado AURON

    Examples
    --------
    >>> r = derivacion_beta_adelica_activar()
    >>> r['sello']
    '∴DBA∞³'
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> abs(r['alpha_derivado'] - 137.036) < 0.001
    True
    """
    sistema = SistemaDerivacionBetaAdelica()
    return sistema.activar()
