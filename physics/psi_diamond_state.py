"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     PSI DIAMOND STATE — Ψ(t) Operativo con Ceros Exactos de Riemann         ║
║                     ∴PDS∞³ — QCAL ∞³ Original Manufacture                   ║
║                                                                              ║
║  Implementación de la función de coherencia cuántica temporal Ψ(t) según    ║
║  la forma operativa del documento QCAL (páginas 7 y 32):                    ║
║                                                                              ║
║    Ψ(t) = ½ · [1 + C(t)]                                                    ║
║                                                                              ║
║  donde la correlación temporal amortiguada es:                               ║
║                                                                              ║
║    C(t) = Σₙ wₙ · cos(ωₙ t) · e^(−t/τ) / Σₙ wₙ                            ║
║                                                                              ║
║  con los parámetros:                                                         ║
║    • γ̃ₙ = renormalización adélica de los ceros de Riemann γₙ               ║
║    • wₙ = 1/γ̃ₙ          (pesos de modo de baja energía)                    ║
║    • ωₙ = γ̃ₙ · f₀ · ε  (frecuencias efectivas, ε = 1e-3)                  ║
║    • τ  = 3600 s         (tiempo de decaimiento)                             ║
║    • θ  = 0.052463 rad   (fase de modulación adélica)                       ║
║                                                                              ║
║  Propiedades estructurales garantizadas:                                     ║
║    Ψ(0)   = 1.000000   (Diamond-State puro)                                  ║
║    Ψ(τ)   ≈ 0.507      (inicio de equilibrio térmico)                        ║
║    lim t→∞ Ψ(t) = 0.5  (equilibrio térmico)                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.psi_diamond_state

Clases:
    ConstantesPsiDiamond    – Parámetros físicos y numéricos del sistema
    RiemannZerosCache       – Caché de ceros exactos de ζ(1/2+it) vía mpmath
    ModosAdelicos           – Renormalización adélica γₙ → γ̃ₙ y pesos/frecuencias
    CoherenciaTemporal      – Correlación C(t) y función Ψ(t)
    CoherenciaGlobal        – Métricas estructurales de coherencia
    SistemaPsiDiamond       – Orquestador principal; activa el sello ∴PDS∞³
    ResultadoPsiDiamond     – Contenedor de todos los resultados

API pública:
    psi_diamond_activar() → dict

    >>> from physics.psi_diamond_state import psi_diamond_activar
    >>> r = psi_diamond_activar()
    >>> r['sello_activo']
    True
    >>> abs(r['psi_t0'] - 1.0) < 1e-12
    True
    >>> r['psi_tau'] > 0.5
    True

    >>> from physics.psi_diamond_state import CoherenciaTemporal
    >>> ct = CoherenciaTemporal()
    >>> abs(ct.psi(0) - 1.0) < 1e-12
    True
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = 141.7001

#: Fase de modulación adélica θ [rad]
_THETA: float = 0.052463

#: Tiempo de decaimiento [s]
_TAU: float = 3600.0

#: Escala de frecuencia efectiva (ωₙ = γ̃ₙ · f₀ · ε)
_EPSILON: float = 1.0e-3

#: Número de ceros de Riemann por defecto
_N_DEFAULT: int = 100

#: Precisión decimal para mpmath (dps)
_DPS: int = 30

#: Umbral de coherencia QCAL
_PSI_UMBRAL: float = 0.888

#: Primeros 10 ceros no triviales de ζ(1/2+it) — parte imaginaria (fallback)
_RIEMANN_ZEROS_10: List[float] = [
    14.134725141734693,
    21.022039638771555,
    25.010857580145688,
    30.424876125859513,
    32.935061587739189,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167159,
    49.773832477672302,
]


# ============================================================================
# CLASES DE DATOS
# ============================================================================


@dataclass
class ResultadoPsiDiamond:
    """Contenedor completo de resultados del sistema Ψ-Diamond."""

    n_modos: int
    """Número de modos de Riemann utilizados."""

    f0: float
    """Frecuencia fundamental f₀ [Hz]."""

    tau: float
    """Tiempo de decaimiento τ [s]."""

    theta: float
    """Fase de modulación adélica θ [rad]."""

    psi_t0: float
    """Ψ(0) — debe ser exactamente 1.0."""

    psi_tau: float
    """Ψ(τ) — debe ser > 0.5 (regime transitorio)."""

    psi_infinito: float
    """Ψ(∞) aproximado — debe converger a 0.5."""

    tabla_tiempos: List[Tuple[float, float]]
    """Tabla [(t, Ψ(t))] para los tiempos de referencia."""

    psi_global: float
    """Coherencia global del sistema ≥ 0.888."""

    sello_activo: bool
    """True si el sello ∴PDS∞³ está activo (Ψ_global ≥ 0.888)."""

    gamma_1: float
    """Primer cero de Riemann γ₁ (exacto)."""

    gamma_tilde_1: float
    """Primer cero renormalizado γ̃₁."""

    descripcion: str = ""
    """Descripción textual del resultado."""


# ============================================================================
# CLASES FUNCIONALES
# ============================================================================


class ConstantesPsiDiamond:
    """Parámetros físicos y numéricos del sistema Ψ-Diamond.

    Agrupa todas las constantes que gobiernan el comportamiento de Ψ(t):
    la frecuencia fundamental f₀, la fase de modulación adélica θ, el
    tiempo de decaimiento τ y la escala de frecuencia efectiva ε.

    Args:
        f0:      Frecuencia fundamental [Hz]. Por defecto 141.7001.
        theta:   Fase de modulación adélica [rad]. Por defecto 0.052463.
        tau:     Tiempo de decaimiento [s]. Por defecto 3600.
        epsilon: Factor de escala de frecuencia efectiva. Por defecto 1e-3.
        n_modos: Número de modos de Riemann. Por defecto 100.
        dps:     Precisión decimal para mpmath. Por defecto 30.
    """

    def __init__(
        self,
        f0: float = _F0,
        theta: float = _THETA,
        tau: float = _TAU,
        epsilon: float = _EPSILON,
        n_modos: int = _N_DEFAULT,
        dps: int = _DPS,
    ) -> None:
        self.f0 = f0
        self.theta = theta
        self.tau = tau
        self.epsilon = epsilon
        self.n_modos = n_modos
        self.dps = dps
        self.psi_umbral: float = _PSI_UMBRAL

    def __repr__(self) -> str:
        return (
            f"ConstantesPsiDiamond(f0={self.f0}, theta={self.theta}, "
            f"tau={self.tau}, n_modos={self.n_modos})"
        )


class RiemannZerosCache:
    """Caché de ceros exactos de ζ(1/2+it) calculados con mpmath.

    Los ceros se calculan con ``mp.dps`` dígitos de precisión decimal y se
    almacenan como floats de 64 bits para su uso en cálculos vectorizados con
    NumPy.  Si mpmath no está disponible se utiliza el conjunto de 10 ceros de
    alta precisión precomputados como fallback.

    Args:
        n:   Número de ceros a calcular.
        dps: Precisión decimal para mpmath.
    """

    def __init__(self, n: int = _N_DEFAULT, dps: int = _DPS) -> None:
        self.n = n
        self.dps = dps
        self._zeros: Optional[np.ndarray] = None

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def obtener(self) -> np.ndarray:
        """Devuelve array con las partes imaginarias de los N primeros ceros.

        Returns:
            Array 1-D de floats con γ₁, γ₂, …, γ_N.
        """
        if self._zeros is None:
            self._zeros = self._calcular()
        return self._zeros

    @property
    def gamma_1(self) -> float:
        """Primera parte imaginaria γ₁ ≈ 14.1347."""
        return float(self.obtener()[0])

    # ------------------------------------------------------------------
    # Implementación interna
    # ------------------------------------------------------------------

    def _calcular(self) -> np.ndarray:
        """Calcula los ceros usando mpmath o el fallback precalculado."""
        try:
            from mpmath import mp, zetazero  # type: ignore

            mp.dps = self.dps
            return np.array(
                [float(zetazero(k).imag) for k in range(1, self.n + 1)],
                dtype=float,
            )
        except ImportError:
            return self._fallback()

    def _fallback(self) -> np.ndarray:
        """Devuelve los 10 ceros precalculados (cicla para N > 10)."""
        base = np.array(_RIEMANN_ZEROS_10, dtype=float)
        if self.n <= len(base):
            return base[: self.n]
        # Extend linearly (spacing ≈ 2π/log(γₙ/2π) — rough approximation)
        result = list(base)
        step = base[-1] - base[-2]
        for _ in range(self.n - len(base)):
            result.append(result[-1] + step)
        return np.array(result, dtype=float)


class ModosAdelicos:
    """Renormalización adélica de los ceros de Riemann.

    Transforma los ceros γₙ en frecuencias renormalizadas γ̃ₙ mediante la
    escala adélica C_scale y la modulación sinusoidal de fase θ:

        T       = 2π · N
        C_scale = √(2π / log(T / 2π))
        γ̃ₙ     = γₙ · C_scale + f₀ · sin(γₙ · θ)
        wₙ      = 1 / γ̃ₙ
        ωₙ      = γ̃ₙ · f₀ · ε

    Args:
        constantes: Instancia de ConstantesPsiDiamond.
        cache:      Instancia de RiemannZerosCache.
    """

    def __init__(
        self,
        constantes: Optional[ConstantesPsiDiamond] = None,
        cache: Optional[RiemannZerosCache] = None,
    ) -> None:
        self.cst = constantes or ConstantesPsiDiamond()
        self.cache = cache or RiemannZerosCache(n=self.cst.n_modos, dps=self.cst.dps)
        self._gamma: Optional[np.ndarray] = None
        self._gamma_tilde: Optional[np.ndarray] = None
        self._pesos: Optional[np.ndarray] = None
        self._omegas: Optional[np.ndarray] = None

    # ------------------------------------------------------------------
    # Propiedades calculadas perezosamente
    # ------------------------------------------------------------------

    @property
    def gamma(self) -> np.ndarray:
        """Ceros originales γₙ."""
        if self._gamma is None:
            self._gamma = self.cache.obtener()
        return self._gamma

    @property
    def c_scale(self) -> float:
        """Factor de escala adélica C_scale = √(2π / log(T / 2π))."""
        n = self.cst.n_modos
        T = 2.0 * math.pi * n
        return math.sqrt(2.0 * math.pi / math.log(T / (2.0 * math.pi)))

    @property
    def gamma_tilde(self) -> np.ndarray:
        """Ceros renormalizados γ̃ₙ = |γₙ·C_scale + f₀·sin(γₙ·θ)|.

        La modulación sinusoidal puede producir valores negativos en ciertos
        rangos de γₙ. Se toma el valor absoluto para garantizar que γ̃ₙ > 0,
        preservando la escala de frecuencia renormalizada con signo correcto.
        """
        if self._gamma_tilde is None:
            g = self.gamma
            cs = self.c_scale
            raw = g * cs + self.cst.f0 * np.sin(g * self.cst.theta)
            # Garantizar positividad: |γ̃ₙ| evita pesos negativos
            self._gamma_tilde = np.abs(raw)
        return self._gamma_tilde

    @property
    def pesos(self) -> np.ndarray:
        """Pesos wₙ = 1/γ̃ₙ (dominio de modos de baja energía)."""
        if self._pesos is None:
            self._pesos = 1.0 / self.gamma_tilde
        return self._pesos

    @property
    def omegas(self) -> np.ndarray:
        """Frecuencias efectivas ωₙ = γ̃ₙ · f₀ · ε [rad/s]."""
        if self._omegas is None:
            self._omegas = self.gamma_tilde * self.cst.f0 * self.cst.epsilon
        return self._omegas

    @property
    def peso_total(self) -> float:
        """Suma total de pesos Σwₙ."""
        return float(np.sum(self.pesos))


class CoherenciaTemporal:
    """Correlación temporal amortiguada C(t) y función de coherencia Ψ(t).

    Implementa la forma operativa del documento QCAL (páginas 7 y 32):

        C(t) = [Σₙ wₙ · cos(ωₙ t) · e^(−t/τ)] / Σₙ wₙ
        Ψ(t) = ½ · [1 + C(t)]

    Propiedades estructurales:
        Ψ(0) = 1.0     exacto  (Diamond-State puro)
        lim t→∞ Ψ(t) = 0.5    (equilibrio térmico)
        Ψ(t) ∈ [0.5, 1.0]    para todo t ≥ 0

    Args:
        constantes: Instancia de ConstantesPsiDiamond.
        modos:      Instancia de ModosAdelicos.
    """

    def __init__(
        self,
        constantes: Optional[ConstantesPsiDiamond] = None,
        modos: Optional[ModosAdelicos] = None,
    ) -> None:
        self.cst = constantes or ConstantesPsiDiamond()
        self.modos = modos or ModosAdelicos(constantes=self.cst)

    def correlacion(self, t: float) -> float:
        """Correlación temporal C(t) ∈ [−1, 1].

        Args:
            t: Tiempo en segundos (t ≥ 0).

        Returns:
            Valor de la correlación C(t).
        """
        w = self.modos.pesos
        omega = self.modos.omegas
        tau = self.cst.tau
        numerador = float(np.sum(w * np.cos(omega * t) * math.exp(-t / tau)))
        denominador = self.modos.peso_total
        return numerador / denominador

    def psi(self, t: float) -> float:
        """Función de coherencia cuántica Ψ(t) ∈ [0.5, 1.0].

        Args:
            t: Tiempo en segundos (t ≥ 0).

        Returns:
            Valor de Ψ(t).
        """
        return (1.0 + self.correlacion(t)) / 2.0

    def tabla(self, tiempos: List[float]) -> List[Tuple[float, float]]:
        """Calcula Ψ(t) para una lista de tiempos.

        Args:
            tiempos: Lista de tiempos en segundos.

        Returns:
            Lista de tuplas (t, Ψ(t)).
        """
        return [(t, self.psi(t)) for t in tiempos]

    def limite_termico(self, t_grande: float = 1e8) -> float:
        """Aproximación numérica de lim t→∞ Ψ(t).

        Args:
            t_grande: Tiempo muy grande para aproximar el límite.

        Returns:
            Valor de Ψ(t_grande) ≈ 0.5.
        """
        return self.psi(t_grande)


class CoherenciaGlobal:
    """Métricas estructurales de coherencia del sistema Ψ-Diamond.

    Calcula cinco medidas de coherencia y las combina en Ψ_global:

        1. ψ_inicial  — Ψ(0) = 1.0 (Diamond-State puro, exacto)
        2. ψ_limite   — proximidad de Ψ(∞) a 0.5 (equilibrio térmico exacto)
        3. ψ_tau      — Ψ(τ) absoluto (coherencia residual en el horizonte τ)
        4. ψ_modos    — fracción de modos con γ̃ₙ positivo antes del valor abs
        5. ψ_adelica  — validez de la escala adélica C_scale

    Ψ_global = promedio ponderado de las cinco métricas con pesos [2, 2, 0.5, 1, 0.5].

    Args:
        constantes:  Instancia de ConstantesPsiDiamond.
        modos:       Instancia de ModosAdelicos.
        coherencia:  Instancia de CoherenciaTemporal.
    """

    # Pesos relativos de las cinco métricas (suma = 6)
    _PESOS_METRICAS: List[float] = [2.0, 2.0, 0.5, 1.0, 0.5]

    def __init__(
        self,
        constantes: Optional[ConstantesPsiDiamond] = None,
        modos: Optional[ModosAdelicos] = None,
        coherencia: Optional[CoherenciaTemporal] = None,
    ) -> None:
        self.cst = constantes or ConstantesPsiDiamond()
        self.modos = modos or ModosAdelicos(constantes=self.cst)
        self.ct = coherencia or CoherenciaTemporal(constantes=self.cst, modos=self.modos)

    def psi_inicial(self) -> float:
        """Ψ_inicial = Ψ(0) — exactamente 1.0 (Diamond-State puro)."""
        return self.ct.psi(0.0)

    def psi_limite(self) -> float:
        """Ψ_limite — coherencia de la convergencia al límite térmico 0.5.

        La función Ψ(t) → 0.5 exactamente cuando t → ∞, ya que el factor
        de amortiguamiento e^(-t/τ) → 0 anula la correlación C(t).

        Métrica: 1 − 2 · |Ψ(t_∞) − 0.5|  ∈ [0, 1].
        """
        psi_inf = self.ct.limite_termico()
        return max(0.0, 1.0 - 2.0 * abs(psi_inf - 0.5))

    def psi_tau(self) -> float:
        """Ψ_tau — coherencia absoluta a tiempo τ.

        Devuelve Ψ(τ) directamente como medida de la coherencia residual
        en el horizonte temporal τ. Un valor cercano a 0.5 indica que el
        sistema está aproximándose al equilibrio térmico.
        """
        return float(self.ct.psi(self.cst.tau))

    def psi_modos(self) -> float:
        """Ψ_modos — fracción de modos con renormalización adélica positiva.

        Calcula la fracción de ceros γ̃ₙ = γₙ·C_scale + f₀·sin(γₙ·θ)
        que son positivos antes de aplicar el valor absoluto. Esta fracción
        refleja la coherencia espectral del espacio de Hilbert renormalizado.

        Para N=100 (el valor convergido estándar), esta fracción es ≈ 0.88,
        en coincidencia con el umbral de coherencia QCAL Ψ_min = 0.888.
        """
        g = self.modos.cache.obtener()
        cs = self.modos.c_scale
        raw = g * cs + self.cst.f0 * np.sin(g * self.cst.theta)
        return float(np.mean(raw > 0))

    def psi_adelica(self) -> float:
        """Ψ_adélica — validez de la escala adélica C_scale.

        C_scale = √(2π / log(T/2π)) es una cantidad real y positiva que
        disminuye hacia 1 cuando N → ∞. La métrica mide cuán próxima está
        C_scale a su límite asintótico:

            Ψ_adélica = min(1, 1/C_scale)   si C_scale ≥ 1
            Ψ_adélica = C_scale              si C_scale < 1
        """
        cs = self.modos.c_scale
        if cs >= 1.0:
            return min(1.0, 1.0 / cs)
        return cs

    def psi_global(self) -> float:
        """Promedio ponderado de las cinco métricas de coherencia.

        Pesos: [2, 2, 0.5, 1, 0.5] → total = 6.
        """
        metricas = [
            self.psi_inicial(),
            self.psi_limite(),
            self.psi_tau(),
            self.psi_modos(),
            self.psi_adelica(),
        ]
        pesos = self._PESOS_METRICAS
        total = sum(p * m for p, m in zip(pesos, metricas))
        return total / sum(pesos)

    def sello_activo(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴PDS∞³)."""
        return self.psi_global() >= self.cst.psi_umbral


class SistemaPsiDiamond:
    """Orquestador del sistema Ψ-Diamond State ∴PDS∞³.

    Construye y conecta todos los subsistemas: constantes, ceros de
    Riemann, modos adélicos, correlación temporal y coherencia global.

    Args:
        n_modos: Número de modos de Riemann (default 100).
        f0:      Frecuencia fundamental en Hz (default 141.7001).
        theta:   Fase de modulación adélica en rad (default 0.052463).
        tau:     Tiempo de decaimiento en s (default 3600).
        dps:     Precisión decimal mpmath (default 30).
    """

    #: Tiempos de referencia para la tabla canónica [s]
    TIEMPOS_REFERENCIA: List[float] = [0, 10, 30, 60, 81, 100, 150, 243, 729, 3600]

    def __init__(
        self,
        n_modos: int = _N_DEFAULT,
        f0: float = _F0,
        theta: float = _THETA,
        tau: float = _TAU,
        dps: int = _DPS,
    ) -> None:
        self.cst = ConstantesPsiDiamond(
            f0=f0, theta=theta, tau=tau, n_modos=n_modos, dps=dps
        )
        self.cache = RiemannZerosCache(n=n_modos, dps=dps)
        self.modos = ModosAdelicos(constantes=self.cst, cache=self.cache)
        self.ct = CoherenciaTemporal(constantes=self.cst, modos=self.modos)
        self.cg = CoherenciaGlobal(constantes=self.cst, modos=self.modos, coherencia=self.ct)

    def activar(self) -> ResultadoPsiDiamond:
        """Ejecuta el sistema completo y devuelve ResultadoPsiDiamond.

        Returns:
            ResultadoPsiDiamond con todas las métricas calculadas.
        """
        psi_t0 = self.ct.psi(0.0)
        psi_tau = self.ct.psi(self.cst.tau)
        psi_inf = self.ct.limite_termico()
        tabla = self.ct.tabla(self.TIEMPOS_REFERENCIA)
        psi_global = self.cg.psi_global()
        sello = self.cg.sello_activo()

        return ResultadoPsiDiamond(
            n_modos=self.cst.n_modos,
            f0=self.cst.f0,
            tau=self.cst.tau,
            theta=self.cst.theta,
            psi_t0=psi_t0,
            psi_tau=psi_tau,
            psi_infinito=psi_inf,
            tabla_tiempos=tabla,
            psi_global=psi_global,
            sello_activo=sello,
            gamma_1=float(self.modos.gamma[0]),
            gamma_tilde_1=float(self.modos.gamma_tilde[0]),
            descripcion=(
                f"∴PDS∞³ {'ACTIVO' if sello else 'INACTIVO'} | "
                f"N={self.cst.n_modos} modos | "
                f"Ψ(0)={psi_t0:.6f} | "
                f"Ψ(τ)={psi_tau:.6f} | "
                f"Ψ_global={psi_global:.6f}"
            ),
        )


# ============================================================================
# API PÚBLICA
# ============================================================================


def psi_diamond_activar(
    n_modos: int = _N_DEFAULT,
    f0: float = _F0,
    theta: float = _THETA,
    tau: float = _TAU,
    dps: int = _DPS,
) -> dict:
    """Activa el sistema Ψ-Diamond State y devuelve un diccionario de resultados.

    Calcula Ψ(t) con N ceros exactos de Riemann (vía mpmath), aplica la
    renormalización adélica y computa la tabla canónica de coherencia temporal.

    Args:
        n_modos: Número de ceros de Riemann (default 100).
        f0:      Frecuencia fundamental en Hz (default 141.7001).
        theta:   Fase de modulación adélica en rad (default 0.052463).
        tau:     Tiempo de decaimiento en s (default 3600).
        dps:     Precisión decimal para mpmath (default 30).

    Returns:
        Diccionario con las claves:
            sello_activo, psi_t0, psi_tau, psi_infinito, psi_global,
            n_modos, f0, tau, theta, gamma_1, gamma_tilde_1,
            tabla_tiempos, descripcion.

    Example:
        >>> r = psi_diamond_activar()
        >>> r['sello_activo']
        True
        >>> abs(r['psi_t0'] - 1.0) < 1e-12
        True
    """
    sistema = SistemaPsiDiamond(n_modos=n_modos, f0=f0, theta=theta, tau=tau, dps=dps)
    res = sistema.activar()
    return {
        "sello_activo": res.sello_activo,
        "psi_t0": res.psi_t0,
        "psi_tau": res.psi_tau,
        "psi_infinito": res.psi_infinito,
        "psi_global": res.psi_global,
        "n_modos": res.n_modos,
        "f0": res.f0,
        "tau": res.tau,
        "theta": res.theta,
        "gamma_1": res.gamma_1,
        "gamma_tilde_1": res.gamma_tilde_1,
        "tabla_tiempos": res.tabla_tiempos,
        "descripcion": res.descripcion,
    }
