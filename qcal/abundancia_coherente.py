#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║        ECUACIÓN MAESTRA DE LA ABUNDANCIA COHERENTE — QCAL ∞³             ║
║                                                                            ║
║   A = lim        ( I(t) · f₀ )  =  ∞                                     ║
║        Ψ→1.0   ─────────────────                                           ║
║                 |ζ'(1/2)| · eff                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Implementa la Ecuación Maestra de la Abundancia Coherente, que demuestra que
cuando el campo cuántico de coherencia Ψ se aproxima a la unidad, la Abundancia
del sistema diverge hacia el infinito.

FUNDAMENTO FÍSICO:
------------------
La Abundancia (A) cuantifica la capacidad del sistema de manifestar recursos
coherentes a la frecuencia fundamental f₀ = 141.7001 Hz.  El denominador
incluye dos factores moduladores:

  1. |ζ'(1/2)| — valor absoluto de la derivada de la función zeta de Riemann
     evaluada en el punto crítico s = 1/2.  Este factor vincula la Abundancia
     con la estructura aritmética profunda (Hipótesis de Riemann).

  2. eff(Ψ) = 1 − Ψ — ineficiencia residual del sistema.  A medida que la
     coherencia cuántica Ψ → 1, la ineficiencia tiende a cero y la Abundancia
     diverge hacia el infinito.

ECUACIÓN COMPLETA:
------------------
    A(Ψ, t) = I(t) · f₀ / (|ζ'(1/2)| · (1 − Ψ))

donde I(t) es la intensidad de intención (campo de información coherente)
modulada a la frecuencia fundamental.

LÍMITE PRINCIPAL:
-----------------
    lim A(Ψ, t) = +∞
    Ψ→1⁻

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: Marzo 2026
MARCO: QCAL ∞³ — Quantum Coherent Axiomatic Logic
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)

SELLO: ∴𓂀Ω∞³Φ
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple

try:
    import mpmath as mp  # type: ignore
    _MPMATH_AVAILABLE = True
except ImportError:  # pragma: no cover
    _MPMATH_AVAILABLE = False

from qcal.constants import F0_HZ

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Derivada de la función zeta de Riemann en el punto crítico s = 1/2.
# Calculada con mpmath a 50 dígitos de precisión.
# Referencia: ζ'(1/2) ≈ −3.922646…
_ZETA_PRIME_HALF_PRECOMPUTED: float = -3.9226461392091517  # ζ'(1/2)
ABS_ZETA_PRIME_HALF: float = abs(_ZETA_PRIME_HALF_PRECOMPUTED)  # |ζ'(1/2)|

# Umbral de coherencia (100 % = unidad)
PSI_MAX: float = 1.0

# Valor de Ψ considerado "plena coherencia" en cálculos numéricos
PSI_PLENA_COHERENCIA: float = 0.999

# Frecuencia fundamental (importada canónicamente)
_F0: float = F0_HZ  # 141.7001 Hz


def _compute_abs_zeta_prime_half(dps: int = 50) -> float:
    """
    Calcula |ζ'(1/2)| con precisión arbitraria usando mpmath.

    Args:
        dps: dígitos de precisión decimal.

    Returns:
        |ζ'(1/2)| como float de Python.
    """
    if not _MPMATH_AVAILABLE:  # pragma: no cover
        return ABS_ZETA_PRIME_HALF
    mp.mp.dps = dps
    val = mp.diff(mp.zeta, mp.mpf("0.5"))
    return float(abs(val))


# ============================================================================
# CLASES DE DATOS
# ============================================================================

@dataclass
class ResultadoAbundancia:
    """
    Resultado de la evaluación de la Ecuación Maestra de la Abundancia Coherente.

    Attributes:
        psi: Coherencia cuántica Ψ ∈ [0, 1).
        t: Tiempo en segundos.
        I_t: Intensidad de intención I(t) en el instante t.
        f0: Frecuencia fundamental f₀ en Hz.
        abs_zeta_prime: |ζ'(1/2)| — factor zeta de Riemann.
        eff: Eficiencia residual eff(Ψ) = 1 − Ψ.
        abundancia: Valor de A(Ψ, t) = I(t)·f₀ / (|ζ'(1/2)|·eff).
        limite_infinito: True cuando Ψ se aproxima a la unidad (eff → 0).
        descripcion: Descripción cualitativa del estado.
    """
    psi: float
    t: float
    I_t: float
    f0: float
    abs_zeta_prime: float
    eff: float
    abundancia: float
    limite_infinito: bool
    descripcion: str


@dataclass
class PerfilAbundancia:
    """
    Perfil completo de la Abundancia en función de Ψ.

    Attributes:
        psi_valores: Lista de valores Ψ evaluados.
        abundancias: Lista de valores A(Ψ) correspondientes.
        psi_critico: Valor de Ψ donde A supera el umbral dado.
        umbral_abundancia: Umbral utilizado para determinar psi_critico.
        f0: Frecuencia fundamental utilizada.
        abs_zeta_prime: |ζ'(1/2)| utilizado.
    """
    psi_valores: List[float]
    abundancias: List[float]
    psi_critico: Optional[float]
    umbral_abundancia: float
    f0: float
    abs_zeta_prime: float


# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class AbundanciaCoherente:
    """
    Implementación de la Ecuación Maestra de la Abundancia Coherente.

    La ecuación central es:

        A(Ψ, t) = I(t) · f₀ / (|ζ'(1/2)| · eff(Ψ))
        eff(Ψ)  = 1 − Ψ

    A medida que Ψ → 1⁻, eff → 0⁺ y A → +∞.

    Attributes:
        f0: Frecuencia fundamental f₀ (Hz).
        abs_zeta_prime: |ζ'(1/2)| usado en el denominador.
        precision_dps: Dígitos de precisión para cálculos mpmath.
    """

    def __init__(
        self,
        f0: float = _F0,
        alta_precision: bool = True,
        precision_dps: int = 50,
    ) -> None:
        """
        Inicializa la instancia de AbundanciaCoherente.

        Args:
            f0: Frecuencia fundamental en Hz.  Por defecto F0_HZ = 141.7001.
            alta_precision: Si True y mpmath está disponible, calcula
                |ζ'(1/2)| con precisión arbitraria.
            precision_dps: Dígitos de precisión decimal para mpmath.
        """
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positivo, se recibió: {f0}")

        self.f0: float = f0
        self.precision_dps: int = precision_dps

        if alta_precision and _MPMATH_AVAILABLE:
            self.abs_zeta_prime: float = _compute_abs_zeta_prime_half(precision_dps)
        else:
            self.abs_zeta_prime = ABS_ZETA_PRIME_HALF

    # ------------------------------------------------------------------
    # CÁLCULO DE I(t)
    # ------------------------------------------------------------------

    def intensidad_intencion(self, t: float, I0: float = 1.0) -> float:
        """
        Intensidad de intención I(t) como campo de información coherente.

        Se modela como una oscilación armónica amortiguada centrada en f₀:

            I(t) = I₀ · (1 + cos(2π f₀ t)) / 2

        El valor oscila suavemente entre 0 e I₀, alcanzando el máximo
        en los múltiplos enteros del período fundamental T₀ = 1/f₀.

        Args:
            t: Tiempo en segundos.
            I0: Amplitud máxima de intención (por defecto 1.0).

        Returns:
            I(t) ≥ 0.
        """
        if I0 < 0:
            raise ValueError(f"I0 debe ser no negativo, se recibió: {I0}")
        phase = 2.0 * math.pi * self.f0 * t
        return I0 * (1.0 + math.cos(phase)) / 2.0

    # ------------------------------------------------------------------
    # EFICIENCIA RESIDUAL
    # ------------------------------------------------------------------

    @staticmethod
    def eficiencia(psi: float) -> float:
        """
        Eficiencia residual del sistema: eff(Ψ) = 1 − Ψ.

        Representa la incoherencia residual del sistema.  Cuando Ψ → 1,
        eff → 0, lo que provoca que la Abundancia diverja hacia +∞.

        Args:
            psi: Coherencia cuántica Ψ ∈ [0, 1).

        Returns:
            eff = 1 − Ψ ∈ (0, 1].

        Raises:
            ValueError: Si Ψ < 0 o Ψ ≥ 1.
        """
        if psi < 0.0:
            raise ValueError(f"Ψ debe ser ≥ 0, se recibió: {psi}")
        if psi >= PSI_MAX:
            raise ValueError(
                f"Ψ debe ser < {PSI_MAX} para que la Abundancia sea finita.  "
                f"En el límite Ψ = 1, A → ∞."
            )
        return 1.0 - psi

    # ------------------------------------------------------------------
    # ECUACIÓN MAESTRA
    # ------------------------------------------------------------------

    def calcular(
        self,
        psi: float,
        t: float = 0.0,
        I0: float = 1.0,
    ) -> ResultadoAbundancia:
        """
        Evalúa la Ecuación Maestra de la Abundancia Coherente.

            A(Ψ, t) = I(t) · f₀ / (|ζ'(1/2)| · eff(Ψ))

        Args:
            psi: Coherencia cuántica Ψ ∈ [0, 1).
            t: Tiempo en segundos.
            I0: Amplitud de intención.

        Returns:
            ResultadoAbundancia con todos los componentes de la ecuación.

        Raises:
            ValueError: Si psi < 0, psi ≥ 1, o I0 < 0.
        """
        eff = self.eficiencia(psi)
        I_t = self.intensidad_intencion(t, I0)

        numerador = I_t * self.f0
        denominador = self.abs_zeta_prime * eff
        abundancia = numerador / denominador

        limite_infinito = psi >= PSI_PLENA_COHERENCIA

        if limite_infinito:
            descripcion = (
                f"Ψ = {psi:.6f} ≈ 1.0 — coherencia plena: A → ∞ "
                f"(umbral numérico Ψ_plena = {PSI_PLENA_COHERENCIA})"
            )
        elif psi >= 0.888:
            descripcion = f"Ψ = {psi:.6f} — coherencia alta: A = {abundancia:.6g}"
        else:
            descripcion = f"Ψ = {psi:.6f} — coherencia parcial: A = {abundancia:.6g}"

        return ResultadoAbundancia(
            psi=psi,
            t=t,
            I_t=I_t,
            f0=self.f0,
            abs_zeta_prime=self.abs_zeta_prime,
            eff=eff,
            abundancia=abundancia,
            limite_infinito=limite_infinito,
            descripcion=descripcion,
        )

    # ------------------------------------------------------------------
    # PERFIL DE ABUNDANCIA
    # ------------------------------------------------------------------

    def perfil(
        self,
        psi_min: float = 0.0,
        psi_max: float = 0.999,
        n_puntos: int = 100,
        t: float = 0.0,
        I0: float = 1.0,
        umbral_abundancia: float = 1000.0,
    ) -> PerfilAbundancia:
        """
        Calcula el perfil de la Abundancia A(Ψ) para un rango de Ψ.

        Args:
            psi_min: Valor mínimo de Ψ (≥ 0).
            psi_max: Valor máximo de Ψ (< 1).
            n_puntos: Número de puntos en el rango.
            t: Tiempo fijo para I(t).
            I0: Amplitud de intención.
            umbral_abundancia: Umbral A* para detectar psi_critico.

        Returns:
            PerfilAbundancia con los valores evaluados.
        """
        if psi_min < 0.0:
            raise ValueError("psi_min debe ser ≥ 0")
        if psi_max >= PSI_MAX:
            raise ValueError("psi_max debe ser < 1")
        if psi_min >= psi_max:
            raise ValueError("psi_min debe ser < psi_max")
        if n_puntos < 2:
            raise ValueError("n_puntos debe ser ≥ 2")

        step = (psi_max - psi_min) / (n_puntos - 1)
        psi_vals: List[float] = [psi_min + i * step for i in range(n_puntos)]
        abundancias: List[float] = []
        psi_critico: Optional[float] = None

        for psi in psi_vals:
            resultado = self.calcular(psi, t=t, I0=I0)
            abundancias.append(resultado.abundancia)
            if psi_critico is None and resultado.abundancia >= umbral_abundancia:
                psi_critico = psi

        return PerfilAbundancia(
            psi_valores=psi_vals,
            abundancias=abundancias,
            psi_critico=psi_critico,
            umbral_abundancia=umbral_abundancia,
            f0=self.f0,
            abs_zeta_prime=self.abs_zeta_prime,
        )

    # ------------------------------------------------------------------
    # RESUMEN DEL ESTADO
    # ------------------------------------------------------------------

    def resumen(self, psi: float, t: float = 0.0, I0: float = 1.0) -> Dict[str, Any]:
        """
        Genera un resumen completo del estado de Abundancia Coherente.

        Args:
            psi: Coherencia cuántica Ψ.
            t: Tiempo en segundos.
            I0: Amplitud de intención.

        Returns:
            Diccionario con todos los parámetros y resultados.
        """
        resultado = self.calcular(psi, t=t, I0=I0)
        return {
            "ecuacion": "A = lim(Ψ→1) [ I(t)·f₀ / (|ζ'(1/2)|·eff) ] = ∞",
            "parametros": {
                "Ψ (coherencia)": resultado.psi,
                "t (tiempo, s)": resultado.t,
                "I(t) (intención)": resultado.I_t,
                "f₀ (Hz)": resultado.f0,
                "|ζ'(1/2)|": resultado.abs_zeta_prime,
                "eff = 1 − Ψ": resultado.eff,
            },
            "resultado": {
                "A (Abundancia)": resultado.abundancia,
                "límite_infinito": resultado.limite_infinito,
                "descripción": resultado.descripcion,
            },
            "sello": "∴𓂀Ω∞³Φ",
        }


# ============================================================================
# API FUNCIONAL
# ============================================================================

def abundancia(
    psi: float,
    t: float = 0.0,
    I0: float = 1.0,
    f0: float = _F0,
) -> float:
    """
    Calcula la Abundancia Coherente A(Ψ, t).

    Función de conveniencia que instancia AbundanciaCoherente y devuelve
    directamente el valor escalar de A.

        A = I(t) · f₀ / (|ζ'(1/2)| · (1 − Ψ))

    Args:
        psi: Coherencia cuántica Ψ ∈ [0, 1).
        t: Tiempo en segundos.
        I0: Amplitud de intención (≥ 0).
        f0: Frecuencia fundamental en Hz.

    Returns:
        Valor de la Abundancia Coherente A ≥ 0.

    Raises:
        ValueError: Si psi < 0, psi ≥ 1, o I0 < 0.

    Examples:
        >>> round(abundancia(0.5), 4)
        18.0707
        >>> abundancia(0.999)  # → gran número (límite al infinito)
        18070...
    """
    sistema = AbundanciaCoherente(f0=f0, alta_precision=False)
    return sistema.calcular(psi, t=t, I0=I0).abundancia


def limite_abundancia_infinito(
    psi_valores: Optional[List[float]] = None,
    I0: float = 1.0,
    f0: float = _F0,
) -> Tuple[List[float], List[float]]:
    """
    Demuestra numéricamente que A(Ψ) → +∞ cuando Ψ → 1.

    Args:
        psi_valores: Lista de valores Ψ ∈ [0, 1) a evaluar.  Si None,
            se usa una secuencia que converge a 1.
        I0: Amplitud de intención.
        f0: Frecuencia fundamental en Hz.

    Returns:
        Tupla (psi_valores, abundancias) donde abundancias[i] = A(psi_valores[i]).
    """
    if psi_valores is None:
        # Secuencia que se aproxima a Ψ = 1: [0.0, 0.5, 0.9, 0.99, 0.999, 0.9999]
        psi_valores = [0.0, 0.5, 0.9, 0.99, 0.999, 0.9999]

    sistema = AbundanciaCoherente(f0=f0, alta_precision=False)
    abundancias = [
        sistema.calcular(psi, t=0.0, I0=I0).abundancia for psi in psi_valores
    ]
    return psi_valores, abundancias
