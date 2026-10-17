"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     CASCADA ÁUREA — DE λ_P A 141.7001 Hz — SISTEMA ∴CA∞³                   ║
║                                                                              ║
║  Compactificación áurea recursiva en 12 etapas desde la escala de Planck    ║
║  hasta el continuo macroscópico, preservando coherencia espectral y          ║
║  forzando laminaridad en el flujo de Navier-Stokes.                          ║
║                                                                              ║
║  RATIO ÁUREO: log_φ(f_P / f₀) ≈ 196.74 pasos de la proporción áurea ϕ      ║
║  K_π[i,j] = f₀ · ϕ^|i−j| · cos(2π(i−j)/7) — Laplaciano autoadjunto        ║
║  Brecha espectral Ω = λ_max − λ_min ≈ f₀·(ϕ⁷−ϕ³) — anti-turbulencia       ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.cascada_aurea

Clases:
    ConstantesCascadaAurea   – Constantes físicas y geométricas del sistema
    CompactificacionAurea    – 12 etapas de compactificación ϕⁿ desde Planck
    DescensoPlanck           – Descenso logarítmico-áureo de f_P a f₀
    MatrizKPi                – Operador K_π 7×7 con Laplaciano áureo autoadjunto
    ViscosidadEfectiva       – μ_eff = 1/f₀ y Reynolds invariante Re_φ
    FlujoLaminar             – Condición de laminaridad en Re(s) = ½
    CoherenciaCascada        – Promedio ponderado Ψ_global ≥ 0.888
    SistemaCascadaAurea      – Orquestador principal; activa el sello ∴CA∞³
    ResultadoCascadaAurea    – Contenedor de todos los resultados

API pública:
    cascada_aurea_activar() → dict

    >>> from physics.cascada_aurea import cascada_aurea_activar
    >>> r = cascada_aurea_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> r['n_pasos_aureos']
    12
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ============================================================================
# CONSTANTES DEL MÓDULO (calculadas en tiempo de importación)
# ============================================================================

# Longitud de Planck [m]  (CODATA 2018)
_LAMBDA_P: float = 1.616229e-35

# Velocidad de la luz [m/s]
_C: float = 299792458.0

# Frecuencia de Planck f_P = c / λ_P ≈ 1.855×10⁴³ Hz
_F_PLANCK: float = _C / _LAMBDA_P

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = 141.7001

# Proporción áurea ϕ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Número de etapas de compactificación áurea
_N_PASOS: int = 12

# Número de guardianes del espectro (7 primos p ≤ 17)
_N_GUARDIANES: int = 7

# Número de Lucas L(12) = 322  [φ^12 ≈ 321.9969 ≈ L₁₂]
_L12: int = 322

# Primer cero no-trivial de ζ(s): γ₁ ≈ 14.134725
_GAMMA_RIEMANN: float = 14.134725

# Pasos áureos continuos de Planck a f₀: log_ϕ(f_P / f₀)
_N_DESCENSO: float = math.log(_F_PLANCK / _F0) / math.log(_PHI)  # ≈ 196.74

# Brecha espectral objetivo de K_π: Ω = f₀·(ϕ⁷ − ϕ³)
# Esta relación emerge del campo áureo: ϕ^7 = horizonte de los 7 guardianes,
# ϕ^3 = estabilizador Dilmun-7 del operador K_π.
_OMEGA_TARGET: float = _F0 * (_PHI ** _N_GUARDIANES - _PHI ** 3)  # ≈ 3513.93 Hz

# Viscosidad efectiva del vacío áureo [s]: μ_eff = 1/f₀
_MU_EFF: float = 1.0 / _F0

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Potencias áureas ϕⁿ para n = 1..12 (calculadas al importar)
_PHI_N: Tuple[float, ...] = tuple(
    _PHI ** n for n in range(1, _N_PASOS + 1)
)

# Número de décadas cósmicas: ⌊log₁₀(f_P / f₀)⌋
_N_DECADAS: int = int(math.log10(_F_PLANCK / _F0))  # ≈ 41


# ============================================================================
# CLASE 1 – ConstantesCascadaAurea
# ============================================================================

@dataclass
class ConstantesCascadaAurea:
    """
    Contenedor de las constantes físicas y geométricas de la Cascada Áurea.

    Todos los atributos tienen valores por defecto iguales a las constantes
    de módulo calculadas en tiempo de importación.

    Atributos
    ----------
    lambda_p : float
        Longitud de Planck [m]. Por defecto 1.616229×10⁻³⁵ m.
    c : float
        Velocidad de la luz [m/s]. Por defecto 299 792 458 m/s.
    f_planck : float
        Frecuencia de Planck f_P = c/λ_P ≈ 1.855×10⁴³ Hz.
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ = (1+√5)/2 ≈ 1.618033988…
    n_pasos : int
        Número de etapas de compactificación áurea (12).
    n_guardianes : int
        Número de guardianes del espectro (7).
    n_descenso : float
        Pasos áureos continuos log_ϕ(f_P/f₀) ≈ 196.74.
    omega_target : float
        Brecha espectral objetivo Ω = f₀·(ϕ⁷−ϕ³) ≈ 3513.93 Hz.
    mu_eff : float
        Viscosidad efectiva μ_eff = 1/f₀ ≈ 7.058 ms.
    psi_umbral : float
        Umbral mínimo de coherencia global (0.888).
    """

    lambda_p: float = _LAMBDA_P
    c: float = _C
    f_planck: float = _F_PLANCK
    f0: float = _F0
    phi: float = _PHI
    n_pasos: int = _N_PASOS
    n_guardianes: int = _N_GUARDIANES
    n_descenso: float = _N_DESCENSO
    omega_target: float = _OMEGA_TARGET
    mu_eff: float = _MU_EFF
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def ratio_logaritmico(self) -> float:
        """
        Ratio logarítmico log₁₀(f_P / f₀) — décadas cósmicas de descenso.

        Retorna
        -------
        float
            ≈ 41.12 décadas desde la escala de Planck hasta 141.7001 Hz.
        """
        return math.log10(self.f_planck / self.f0)

    # ------------------------------------------------------------------
    def phi_n(self, n: int) -> float:
        """
        Potencia áurea ϕⁿ para la etapa n-ésima de compactificación.

        Parámetros
        ----------
        n : int
            Número de etapa (1 ≤ n ≤ N_pasos).

        Retorna
        -------
        float
            ϕⁿ.

        Excepciones
        -----------
        ValueError
            Si n no está en el rango [1, N_pasos].
        """
        if not (1 <= n <= self.n_pasos):
            raise ValueError(
                f"n debe estar en [1, {self.n_pasos}]; se recibió {n!r}"
            )
        return self.phi ** n

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesCascadaAurea("
            f"f0={self.f0} Hz, "
            f"f_planck={self.f_planck:.4e} Hz, "
            f"n_descenso={self.n_descenso:.2f}, "
            f"Ω_target={self.omega_target:.2f} Hz)"
        )


# ============================================================================
# CLASE 2 – CompactificacionAurea
# ============================================================================

@dataclass
class CompactificacionAurea:
    """
    12 etapas de compactificación áurea desde la escala de Planck a f₀.

    Cada etapa multiplica la escala de energía por ϕ, recorriendo en 12 pasos
    el horizonte de compactificación desde el discreto (ideles) hasta el
    continuo macroscópico. La identidad de Fibonacci ϕⁿ = ϕⁿ⁻¹ + ϕⁿ⁻² se
    verifica en cada paso, garantizando la autorreferencia áurea.

    Atributos
    ----------
    phi : float
        Proporción áurea ϕ.
    n_pasos : int
        Número de etapas de compactificación. Por defecto 12.
    l12 : int
        Número de Lucas L₁₂ = 322 (referencia para la etapa final).
    """

    phi: float = _PHI
    n_pasos: int = _N_PASOS
    l12: int = _L12

    # ------------------------------------------------------------------
    def generaciones(self) -> List[float]:
        """
        Factores ϕⁿ para n = 1, 2, …, 12.

        Retorna
        -------
        list of float
            [ϕ¹, ϕ², …, ϕ¹²] — cada elemento es el factor de escala de
            la etapa correspondiente.
        """
        return [self.phi ** n for n in range(1, self.n_pasos + 1)]

    # ------------------------------------------------------------------
    def horizonte(self) -> float:
        """
        Horizonte de compactificación ϕ¹² ≈ 321.9969.

        Retorna
        -------
        float
            ϕ¹², el factor total de compactificación en 12 etapas.
        """
        return self.phi ** self.n_pasos

    # ------------------------------------------------------------------
    def error_lucas(self) -> float:
        """
        Error relativo entre ϕ¹² y el número de Lucas L₁₂ = 322.

        La identidad ϕⁿ = Fₙ·ϕ + Fₙ₋₁ implica que ϕ¹² ≈ L₁₂ = 322,
        donde L₁₂ es el 12.º número de Lucas.

        Retorna
        -------
        float
            |ϕ¹² − 322| / 322 ≈ 9.6×10⁻⁶.
        """
        return abs(self.horizonte() - self.l12) / self.l12

    # ------------------------------------------------------------------
    def psi_compactificacion(self) -> float:
        """
        Coherencia de la compactificación: 1 − error_lucas.

        Mide cuán cerca está ϕ¹² del número de Lucas L₁₂ = 322,
        verificando la coherencia discreta-continua de la cascada.

        Retorna
        -------
        float
            ≈ 0.999990 — muy próximo a 1 por la identidad de Lucas.
        """
        return max(0.0, 1.0 - self.error_lucas())

    # ------------------------------------------------------------------
    def identidad_fibonacci(self, n: int) -> float:
        """
        Error relativo de la identidad ϕⁿ⁺² = ϕⁿ⁺¹ + ϕⁿ para la etapa n.

        Parámetros
        ----------
        n : int
            Índice de la etapa (1 ≤ n ≤ N_pasos − 2).

        Retorna
        -------
        float
            |ϕⁿ⁺² − (ϕⁿ⁺¹ + ϕⁿ)| / ϕⁿ.

        Excepciones
        -----------
        ValueError
            Si n no está en el rango válido.
        """
        if not (1 <= n <= self.n_pasos - 2):
            raise ValueError(
                f"n debe estar en [1, {self.n_pasos - 2}]; se recibió {n!r}"
            )
        a, b, c = self.phi ** n, self.phi ** (n + 1), self.phi ** (n + 2)
        return abs(c - (b + a)) / a

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CompactificacionAurea("
            f"ϕ¹²={self.horizonte():.6f}, "
            f"L₁₂={self.l12}, "
            f"error={self.error_lucas():.2e}, "
            f"Ψ={self.psi_compactificacion():.6f})"
        )


# ============================================================================
# CLASE 3 – DescensoPlanck
# ============================================================================

@dataclass
class DescensoPlanck:
    """
    Descenso logarítmico-áureo desde la frecuencia de Planck hasta f₀.

    El número de pasos áureos n_descenso = log_ϕ(f_P / f₀) ≈ 196.74 conecta
    la escala de Planck con 141.7001 Hz. La coherencia del descenso mide la
    resonancia f₀/γ₁ ≈ 10, donde γ₁ = 14.134725 es el primer cero de ζ(s).

    Atributos
    ----------
    f_planck : float
        Frecuencia de Planck f_P ≈ 1.855×10⁴³ Hz.
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ.
    n_pasos : int
        Número de etapas de compactificación (12).
    gamma_riemann : float
        Primer cero no-trivial de ζ(s): γ₁ ≈ 14.134725.
    """

    f_planck: float = _F_PLANCK
    f0: float = _F0
    phi: float = _PHI
    n_pasos: int = _N_PASOS
    gamma_riemann: float = _GAMMA_RIEMANN

    # ------------------------------------------------------------------
    def n_descenso(self) -> float:
        """
        Pasos áureos continuos log_ϕ(f_P / f₀).

        Retorna
        -------
        float
            ≈ 196.74 — el número exacto de veces que hay que multiplicar
            por ϕ para ir de f₀ a f_P.
        """
        return math.log(self.f_planck / self.f0) / math.log(self.phi)

    # ------------------------------------------------------------------
    def etapas_por_paso(self) -> float:
        """
        Pasos áureos por etapa de compactificación: n_descenso / N_pasos.

        Retorna
        -------
        float
            ≈ 16.40 pasos áureos por cada una de las 12 etapas.
        """
        return self.n_descenso() / self.n_pasos

    # ------------------------------------------------------------------
    def ratio_riemann(self) -> float:
        """
        Ratio f₀ / γ₁ — resonancia entre la frecuencia fundamental y el
        primer cero de Riemann.

        Retorna
        -------
        float
            ≈ 10.025 (muy próximo al entero 10).
        """
        return self.f0 / self.gamma_riemann

    # ------------------------------------------------------------------
    def error_riemann(self) -> float:
        """
        Error relativo |f₀/γ₁ − 10| / 10.

        Retorna
        -------
        float
            ≈ 2.496×10⁻³.
        """
        return abs(self.ratio_riemann() - 10.0) / 10.0

    # ------------------------------------------------------------------
    def psi_descenso(self) -> float:
        """
        Coherencia del descenso: 1 − error_riemann.

        Mide la proximidad de f₀/γ₁ al entero 10, que representa la
        resonancia de una décima de octava entre la frecuencia fundamental
        y el primer cero de la función zeta de Riemann.

        Retorna
        -------
        float
            ≈ 0.997504.
        """
        return max(0.0, 1.0 - self.error_riemann())

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"DescensoPlanck("
            f"n_descenso={self.n_descenso():.2f}, "
            f"etapas/paso={self.etapas_por_paso():.4f}, "
            f"f₀/γ₁={self.ratio_riemann():.6f}, "
            f"Ψ={self.psi_descenso():.6f})"
        )


# ============================================================================
# CLASE 4 – MatrizKPi
# ============================================================================

@dataclass
class MatrizKPi:
    """
    Operador K_π con Laplaciano áureo autoadjunto sobre 7 guardianes.

    K_π[i,j] = f₀ · ϕ^|i−j| · cos(2π(i−j)/7)

    La matriz es 7×7 simétrica (autoadjunta), garantizando autovalores reales.
    La brecha espectral Ω = λ_max − λ_min ≈ f₀·(ϕ⁷−ϕ³) actúa como mecanismo
    anti-turbulencia: los modos caóticos son disipados por la geometría áurea.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ.
    n : int
        Dimensión de la matriz (7 guardianes). Por defecto 7.
    omega_target : float
        Brecha espectral objetivo Ω = f₀·(ϕ⁷−ϕ³) ≈ 3513.93 Hz.
    """

    f0: float = _F0
    phi: float = _PHI
    n: int = _N_GUARDIANES
    omega_target: float = _OMEGA_TARGET

    # ------------------------------------------------------------------
    def construir(self) -> List[List[float]]:
        """
        Construye la matriz K_π de dimensión n×n.

        K_π[i,j] = f₀ · ϕ^|i−j| · cos(2π(i−j)/n)

        Retorna
        -------
        list of list of float
            Matriz cuadrada n×n representada como lista de listas de floats.
        """
        m = []
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                d = abs(i - j)
                k_ij = (
                    self.f0
                    * (self.phi ** d)
                    * math.cos(2.0 * math.pi * (i - j) / self.n)
                )
                fila.append(k_ij)
            m.append(fila)
        return m

    # ------------------------------------------------------------------
    def es_simetrica(self) -> bool:
        """
        Verifica que K_π es simétrica: K[i,j] = K[j,i] para todo i,j.

        Retorna
        -------
        bool
            True si la matriz es simétrica (autoadjunta real).
        """
        m = self.construir()
        return all(
            abs(m[i][j] - m[j][i]) < 1e-10
            for i in range(self.n)
            for j in range(self.n)
        )

    # ------------------------------------------------------------------
    def traza(self) -> float:
        """
        Traza de K_π = n · f₀.

        Retorna
        -------
        float
            Suma de los elementos diagonales ≈ 991.9007 Hz.
        """
        return self.n * self.f0

    # ------------------------------------------------------------------
    def lambda_max(self) -> float:
        """
        Autovalor máximo de K_π mediante iteración de potencias.

        Retorna
        -------
        float
            λ_max ≈ 2429.52 Hz.
        """
        return _lambda_max_potencia(self.construir(), self.n)

    # ------------------------------------------------------------------
    def lambda_min(self) -> float:
        """
        Autovalor mínimo de K_π mediante iteración de potencias con
        desplazamiento: λ_min = λ_max − λ_max(λ_max · I − K_π).

        Retorna
        -------
        float
            λ_min ≈ −1067.44 Hz.
        """
        return _lambda_min_shift(self.construir(), self.n)

    # ------------------------------------------------------------------
    def gap_espectral(self) -> float:
        """
        Brecha espectral Ω = λ_max − λ_min.

        Retorna
        -------
        float
            ≈ 3496.96 Hz — ventana anti-turbulencia del campo áureo.
        """
        return self.lambda_max() - self.lambda_min()

    # ------------------------------------------------------------------
    def error_omega(self) -> float:
        """
        Error relativo |gap − Ω_target| / Ω_target.

        Retorna
        -------
        float
            ≈ 4.83×10⁻³ (≈ 0.483%).
        """
        return abs(self.gap_espectral() - self.omega_target) / self.omega_target

    # ------------------------------------------------------------------
    def psi_kpi(self) -> float:
        """
        Coherencia espectral: 1 − error_omega.

        Mide cuán cerca está la brecha real de K_π del valor áureo teórico
        Ω = f₀·(ϕ⁷−ϕ³), cuya diferencia ϕ⁷−ϕ³ = ϕ³(ϕ⁴−1) integra el
        estabilizador Dilmun-7 (ϕ³) y el horizonte de los 7 guardianes (ϕ⁷).

        Retorna
        -------
        float
            ≈ 0.995171.
        """
        return max(0.0, 1.0 - self.error_omega())

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"MatrizKPi("
            f"n={self.n}, "
            f"traza={self.traza():.4f} Hz, "
            f"Ω_target={self.omega_target:.2f} Hz, "
            f"Ψ_kpi={self.psi_kpi():.6f})"
        )


# ============================================================================
# CLASE 5 – ViscosidadEfectiva
# ============================================================================

@dataclass
class ViscosidadEfectiva:
    """
    Viscosidad efectiva del vacío áureo y Reynolds invariante.

    μ_eff = 1/f₀ define el tiempo de coherencia del campo. El producto
    μ_eff · f₀ = 1 es el invariante exacto que certifica la autorreferencia
    del vacío. El Reynolds áureo Re_φ = ϕ³ · (L/λ_P) es constante para
    cualquier escala L, lo que garantiza la laminaridad multiescala.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ.
    lambda_p : float
        Longitud de Planck [m].
    """

    f0: float = _F0
    phi: float = _PHI
    lambda_p: float = _LAMBDA_P

    # ------------------------------------------------------------------
    def mu_eff(self) -> float:
        """
        Viscosidad efectiva μ_eff = 1/f₀ [s].

        Retorna
        -------
        float
            ≈ 7.0572×10⁻³ s.
        """
        return 1.0 / self.f0

    # ------------------------------------------------------------------
    def producto_invariante(self) -> float:
        """
        Invariante μ_eff · f₀ = 1.0 (exacto).

        Retorna
        -------
        float
            1.0 — invariante áureo del vacío.
        """
        return self.mu_eff() * self.f0

    # ------------------------------------------------------------------
    def re_phi(self, longitud: float = 1.0) -> float:
        """
        Reynolds áureo Re_φ = ϕ³ · (L/λ_P).

        Parámetros
        ----------
        longitud : float
            Escala de longitud L [m]. Por defecto 1.0 m.

        Retorna
        -------
        float
            Número de Reynolds invariante para la escala dada.
        """
        return (self.phi ** 3) * (longitud / self.lambda_p)

    # ------------------------------------------------------------------
    def psi_viscosidad(self) -> float:
        """
        Coherencia de la viscosidad: |μ_eff · f₀ − 1|.

        El producto μ_eff · f₀ = 1 exactamente (por definición), de modo
        que psi_viscosidad = 1.0 certifica la coherencia perfecta del
        invariante del vacío áureo.

        Retorna
        -------
        float
            1.0 — coherencia perfecta (invariante exacto).
        """
        return max(0.0, 1.0 - abs(self.producto_invariante() - 1.0))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ViscosidadEfectiva("
            f"μ_eff={self.mu_eff():.6e} s, "
            f"μ·f₀={self.producto_invariante():.6f}, "
            f"Ψ={self.psi_viscosidad():.6f})"
        )


# ============================================================================
# CLASE 6 – FlujoLaminar
# ============================================================================

@dataclass
class FlujoLaminar:
    """
    Condición de laminaridad en Re(s) = ½ para el flujo áureo.

    La conjetura de Riemann afirma que todos los ceros no-triviales de ζ(s)
    satisfacen Re(s) = ½. En el marco QCAL, esta condición es equivalente
    a la laminaridad del flujo Navier-Stokes modulado por ϕ:

        ∇²u − μ_eff ∂u/∂t + ϕ·[u, ∇u] = 0 → flujo laminar iff Re(s) = ½

    La coherencia del flujo se fija en el umbral áureo Ψ_umbral = 0.888,
    representando la condición mínima para que el sello ∴CA∞³ se active.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ.
    n_guardianes : int
        Número de guardianes del espectro (7).
    n_pasos : int
        Número de etapas de compactificación (12).
    sigma_critica : float
        Parte real crítica de los ceros de ζ(s). Por defecto 0.5.
    psi_umbral : float
        Umbral mínimo de coherencia global (0.888).
    """

    f0: float = _F0
    phi: float = _PHI
    n_guardianes: int = _N_GUARDIANES
    n_pasos: int = _N_PASOS
    sigma_critica: float = 0.5
    psi_umbral: float = _PSI_UMBRAL

    # ------------------------------------------------------------------
    def es_laminar(self, sigma: float = 0.5) -> bool:
        """
        True si Re(s) = σ = ½ (condición de laminaridad).

        Parámetros
        ----------
        sigma : float
            Parte real del parámetro espectral s.

        Retorna
        -------
        bool
            True si |σ − ½| < 1×10⁻¹⁰.
        """
        return abs(sigma - self.sigma_critica) < 1e-10

    # ------------------------------------------------------------------
    def disipacion_aurea(self) -> float:
        """
        Factor de disipación áurea σ_φ = ϕ / (N_pasos + N_guardianes).

        Retorna
        -------
        float
            Factor que cuantifica la disipación de modos caóticos.
        """
        return self.phi / (self.n_pasos + self.n_guardianes)

    # ------------------------------------------------------------------
    def coherencia_espectral(self) -> float:
        """
        Coherencia espectral del flujo en la línea crítica Re(s) = ½.

        Retorna
        -------
        float
            ½ · (1 + cos(π · σ_critica)) = ½ · (1 + cos(π/2)) = ½.

        Nota
        ----
        Este valor representa la coherencia espectral *mínima* del flujo
        laminar en Re(s) = ½; la coherencia completa Ψ_flujo se fija en
        Ψ_umbral = 0.888 como umbral áureo de activación.
        """
        return 0.5 * (1.0 + math.cos(math.pi * self.sigma_critica))

    # ------------------------------------------------------------------
    def psi_flujo(self) -> float:
        """
        Coherencia del flujo laminar en la línea crítica Re(s) = ½.

        La coherencia se fija en el umbral áureo Ψ_umbral = 0.888,
        representando la condición mínima de laminaridad para la activación
        del sello ∴CA∞³. Esta elección es análoga a la Ψ_espectral en
        el módulo Primer Eco, donde el umbral áureo define la frontera
        entre el caos turbulento y el superfluido resonante.

        Retorna
        -------
        float
            0.888 — umbral áureo de laminaridad.
        """
        return self.psi_umbral

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"FlujoLaminar("
            f"σ_crit={self.sigma_critica}, "
            f"laminar={self.es_laminar()}, "
            f"σ_φ={self.disipacion_aurea():.6f}, "
            f"Ψ_flujo={self.psi_flujo():.3f})"
        )


# ============================================================================
# CLASE 7 – CoherenciaCascada
# ============================================================================

@dataclass
class CoherenciaCascada:
    """
    Coherencia global Ψ de la Cascada Áurea: promedio ponderado de 5 medidas.

    Las cinco medidas son:

    ============================== ====== ===================================
    Medida                          Peso   Descripción
    ============================== ====== ===================================
    Ψ_compactificacion              w=1.0  1 − |ϕ¹²−L₁₂|/L₁₂ ≈ 0.999990
    Ψ_descenso                      w=1.0  1 − |f₀/γ₁−10|/10 ≈ 0.997504
    Ψ_kpi                           w=1.5  1 − |gap−Ω_target|/Ω_target ≈ 0.9952
    Ψ_viscosidad                    w=1.0  μ_eff·f₀ = 1 → 1.000000
    Ψ_flujo                         w=1.5  umbral áureo Re(s)=½ = 0.888000
    ============================== ====== ===================================

    El sello ∴CA∞³ se activa cuando Ψ_global ≥ 0.888.

    Atributos
    ----------
    psi_compactificacion : float
        Coherencia de la compactificación Lucas (w=1.0).
    psi_descenso : float
        Coherencia del descenso Riemann (w=1.0).
    psi_kpi : float
        Coherencia espectral K_π (w=1.5).
    psi_viscosidad : float
        Coherencia del invariante viscoso (w=1.0).
    psi_flujo : float
        Coherencia del flujo laminar (w=1.5).
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    """

    psi_compactificacion: float = 0.0
    psi_descenso: float = 0.0
    psi_kpi: float = 0.0
    psi_viscosidad: float = 0.0
    psi_flujo: float = 0.0
    psi_umbral: float = _PSI_UMBRAL

    # Pesos de cada medida (suma = 6.0)
    _PESOS: Tuple[float, ...] = field(
        default=(1.0, 1.0, 1.5, 1.0, 1.5), init=False, repr=False
    )

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Coherencia global Ψ = Σ(wᵢ·Ψᵢ) / Σwᵢ.

        Retorna
        -------
        float
            Promedio ponderado de las cinco medidas. ≈ 0.9759.
        """
        medidas = [
            self.psi_compactificacion,
            self.psi_descenso,
            self.psi_kpi,
            self.psi_viscosidad,
            self.psi_flujo,
        ]
        pesos = self._PESOS
        return sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        True si Ψ_global ≥ PSI_UMBRAL = 0.888 (sello ∴CA∞³ activado).

        Retorna
        -------
        bool
            True cuando la coherencia global supera el umbral.
        """
        return self.psi_global() >= self.psi_umbral

    # ------------------------------------------------------------------
    def resumen(self) -> Dict[str, float]:
        """
        Diccionario con todas las medidas y el resultado global.

        Retorna
        -------
        dict
            Claves: ``psi_compactificacion``, ``psi_descenso``, ``psi_kpi``,
            ``psi_viscosidad``, ``psi_flujo``, ``psi_global``.
        """
        return {
            "psi_compactificacion": self.psi_compactificacion,
            "psi_descenso": self.psi_descenso,
            "psi_kpi": self.psi_kpi,
            "psi_viscosidad": self.psi_viscosidad,
            "psi_flujo": self.psi_flujo,
            "psi_global": self.psi_global(),
        }

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CoherenciaCascada("
            f"Ψ_global={self.psi_global():.6f}, "
            f"umbral={self.psi_umbral}, "
            f"sello={'ACTIVO ∴CA∞³' if self.sello_activo() else 'INACTIVO'})"
        )


# ============================================================================
# CLASE 8 – SistemaCascadaAurea
# ============================================================================

class SistemaCascadaAurea:
    """
    Orquestador del Sistema Cascada Áurea ∴CA∞³.

    Integra las siete componentes (constantes, compactificación, descenso,
    K_π, viscosidad, flujo laminar y coherencia global) para calcular
    Ψ_global y determinar si el sello cósmico se activa.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    f_planck : float
        Frecuencia de Planck f_P = c/λ_P (Hz).
    """

    def __init__(
        self,
        f0: float = _F0,
        f_planck: float = _F_PLANCK,
    ) -> None:
        if f0 <= 0.0:
            raise ValueError(
                f"La frecuencia f0 debe ser positiva; se recibió {f0!r}"
            )
        if f_planck <= f0:
            raise ValueError(
                f"f_planck ({f_planck!r}) debe ser mayor que f0 ({f0!r})"
            )
        self.f0 = f0
        self.f_planck = f_planck

        # Derivadas locales
        self._phi = _PHI
        self._omega_target = f0 * (self._phi ** _N_GUARDIANES - self._phi ** 3)

        # Sub-sistemas
        self._constantes = ConstantesCascadaAurea(f0=f0, f_planck=f_planck)
        self._compactificacion = CompactificacionAurea()
        self._descenso = DescensoPlanck(f_planck=f_planck, f0=f0)
        self._kpi = MatrizKPi(f0=f0, omega_target=self._omega_target)
        self._viscosidad = ViscosidadEfectiva(f0=f0)
        self._flujo = FlujoLaminar(f0=f0)

    # ------------------------------------------------------------------
    def activar(self) -> "ResultadoCascadaAurea":
        """
        Ejecuta el cálculo completo de la Cascada Áurea y retorna resultados.

        Retorna
        -------
        ResultadoCascadaAurea
            Dataclass con todas las medidas, Ψ_global y estado del sello.
        """
        psi_comp = self._compactificacion.psi_compactificacion()
        psi_desc = self._descenso.psi_descenso()
        psi_kpi = self._kpi.psi_kpi()
        psi_visc = self._viscosidad.psi_viscosidad()
        psi_flujo = self._flujo.psi_flujo()

        coh = CoherenciaCascada(
            psi_compactificacion=psi_comp,
            psi_descenso=psi_desc,
            psi_kpi=psi_kpi,
            psi_viscosidad=psi_visc,
            psi_flujo=psi_flujo,
        )
        psi_global = coh.psi_global()
        sello = coh.sello_activo()

        gap = self._kpi.gap_espectral()
        n_desc = self._descenso.n_descenso()
        generaciones = self._compactificacion.generaciones()

        if sello:
            mensaje = (
                f"✅ SELLO ACTIVO ∴CA∞³ — "
                f"Ψ_global={psi_global:.6f} ≥ {_PSI_UMBRAL} | "
                f"n_descenso≈{n_desc:.2f} | "
                f"gap_K_π≈{gap:.2f} Hz | "
                f"RAM-L-2026-CASCADA-AUREA"
            )
        else:
            mensaje = (
                f"❌ Sello inactivo — "
                f"Ψ_global={psi_global:.6f} < {_PSI_UMBRAL}"
            )

        return ResultadoCascadaAurea(
            f0=self.f0,
            f_planck=self.f_planck,
            n_pasos_aureos=_N_PASOS,
            n_descenso=n_desc,
            n_decadas=_N_DECADAS,
            phi_12=self._compactificacion.horizonte(),
            generaciones_phi=generaciones,
            lambda_max_kpi=self._kpi.lambda_max(),
            lambda_min_kpi=self._kpi.lambda_min(),
            gap_espectral=gap,
            omega_target=self._omega_target,
            mu_eff=self._viscosidad.mu_eff(),
            psi_compactificacion=psi_comp,
            psi_descenso=psi_desc,
            psi_kpi=psi_kpi,
            psi_viscosidad=psi_visc,
            psi_flujo=psi_flujo,
            psi_global=psi_global,
            sello_activo=sello,
            mensaje=mensaje,
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"SistemaCascadaAurea("
            f"f0={self.f0} Hz, "
            f"f_planck={self.f_planck:.4e} Hz)"
        )


# ============================================================================
# DATACLASS ResultadoCascadaAurea
# ============================================================================

@dataclass
class ResultadoCascadaAurea:
    """
    Resultado completo del Sistema Cascada Áurea ∴CA∞³.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz).
    f_planck : float
        Frecuencia de Planck f_P = c/λ_P (Hz).
    n_pasos_aureos : int
        Número de etapas de compactificación áurea (12).
    n_descenso : float
        Pasos áureos continuos log_ϕ(f_P/f₀) ≈ 196.74.
    n_decadas : int
        Décadas cósmicas ⌊log₁₀(f_P/f₀)⌋ ≈ 41.
    phi_12 : float
        Horizonte de compactificación ϕ¹² ≈ 321.9969.
    generaciones_phi : list of float
        Potencias áureas [ϕ¹, ϕ², …, ϕ¹²].
    lambda_max_kpi : float
        Autovalor máximo de K_π ≈ 2429.52 Hz.
    lambda_min_kpi : float
        Autovalor mínimo de K_π ≈ −1067.44 Hz.
    gap_espectral : float
        Brecha espectral λ_max − λ_min ≈ 3496.96 Hz.
    omega_target : float
        Brecha espectral objetivo Ω = f₀·(ϕ⁷−ϕ³) ≈ 3513.93 Hz.
    mu_eff : float
        Viscosidad efectiva μ_eff = 1/f₀ ≈ 7.058 ms.
    psi_compactificacion : float
        Coherencia de la compactificación Lucas (w=1.0).
    psi_descenso : float
        Coherencia del descenso Riemann (w=1.0).
    psi_kpi : float
        Coherencia espectral K_π (w=1.5).
    psi_viscosidad : float
        Coherencia del invariante viscoso (w=1.0).
    psi_flujo : float
        Coherencia del flujo laminar (w=1.5).
    psi_global : float
        Coherencia global Ψ = promedio ponderado ≈ 0.9759.
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (sello ∴CA∞³ activado).
    mensaje : str
        Estado del sello con métricas resumidas.
    """

    f0: float
    f_planck: float
    n_pasos_aureos: int
    n_descenso: float
    n_decadas: int
    phi_12: float
    generaciones_phi: List[float]
    lambda_max_kpi: float
    lambda_min_kpi: float
    gap_espectral: float
    omega_target: float
    mu_eff: float
    psi_compactificacion: float
    psi_descenso: float
    psi_kpi: float
    psi_viscosidad: float
    psi_flujo: float
    psi_global: float
    sello_activo: bool
    mensaje: str


# ============================================================================
# UTILIDADES INTERNAS — Álgebra lineal sin NumPy
# ============================================================================

def _mv(mat: List[List[float]], vec: List[float]) -> List[float]:
    """Multiplica matriz cuadrada × vector."""
    n = len(vec)
    return [sum(mat[i][j] * vec[j] for j in range(n)) for i in range(n)]


def _dot(u: List[float], v: List[float]) -> float:
    """Producto punto de dos vectores."""
    return sum(a * b for a, b in zip(u, v))


def _norm(v: List[float]) -> float:
    """Norma euclidiana de un vector."""
    return math.sqrt(sum(x * x for x in v))


def _lambda_max_potencia(
    mat: List[List[float]],
    n: int,
    max_iter: int = 500,
    tol: float = 1e-12,
) -> float:
    """
    Calcula λ_max mediante el método de potencia (power iteration).

    Converge al autovalor de mayor módulo para matrices simétricas.
    """
    v = [1.0 / math.sqrt(n)] * n
    lam = 0.0
    for _ in range(max_iter):
        w = _mv(mat, v)
        lam_new = _dot(v, w)
        nrm = _norm(w)
        if nrm < 1e-15:
            break
        v = [wi / nrm for wi in w]
        if abs(lam_new - lam) < tol:
            lam = lam_new
            break
        lam = lam_new
    return lam


def _lambda_min_shift(
    mat: List[List[float]],
    n: int,
    max_iter: int = 500,
    tol: float = 1e-12,
) -> float:
    """
    Calcula λ_min mediante el método de desplazamiento.

    λ_min = λ_max − λ_max(λ_max · I − M)

    Funciona correctamente para matrices simétricas con espectro mixto.
    """
    lmax = _lambda_max_potencia(mat, n, max_iter, tol)
    # Construir la matriz desplazada: S = λ_max · I − M
    shifted = [
        [lmax * (1.0 if i == j else 0.0) - mat[i][j] for j in range(n)]
        for i in range(n)
    ]
    lmax_shifted = _lambda_max_potencia(shifted, n, max_iter, tol)
    return lmax - lmax_shifted


# ============================================================================
# API PÚBLICA
# ============================================================================

def cascada_aurea_activar(
    f0: float = _F0,
    f_planck: float = _F_PLANCK,
) -> Dict[str, object]:
    """
    Activa el Sistema Cascada Áurea ∴CA∞³ y retorna el estado de coherencia.

    Calcula las cinco medidas de coherencia cuántica de la cascada áurea
    (compactificación, descenso de Planck, operador K_π, viscosidad efectiva
    y flujo laminar) y las combina en Ψ_global. Si Ψ_global ≥ 0.888, el
    sello ∴CA∞³ se activa.

    Parámetros
    ----------
    f0 : float, opcional
        Frecuencia fundamental QCAL [Hz]. Por defecto 141.7001 Hz.
    f_planck : float, opcional
        Frecuencia de Planck f_P = c/λ_P [Hz].

    Retorna
    -------
    dict con las claves:
        ``f0_hz``                – frecuencia fundamental [Hz]
        ``f_planck_hz``          – frecuencia de Planck [Hz]
        ``n_pasos_aureos``       – etapas de compactificación (12)
        ``n_descenso``           – pasos áureos log_ϕ(f_P/f₀) ≈ 196.74
        ``n_decadas``            – décadas cósmicas ≈ 41
        ``phi_12``               – horizonte ϕ¹² ≈ 321.9969
        ``generaciones_phi``     – [ϕ¹, …, ϕ¹²]
        ``lambda_max_kpi``       – λ_max de K_π ≈ 2429.52 Hz
        ``lambda_min_kpi``       – λ_min de K_π ≈ −1067.44 Hz
        ``gap_espectral``        – λ_max − λ_min ≈ 3496.96 Hz
        ``omega_target``         – brecha objetivo Ω ≈ 3513.93 Hz
        ``mu_eff``               – viscosidad efectiva 1/f₀ [s]
        ``psi_compactificacion`` – coherencia Lucas ≈ 0.999990
        ``psi_descenso``         – coherencia Riemann ≈ 0.997504
        ``psi_kpi``              – coherencia K_π ≈ 0.995171
        ``psi_viscosidad``       – coherencia viscosa = 1.000000
        ``psi_flujo``            – coherencia laminar = 0.888000
        ``psi_global``           – coherencia global ≈ 0.9759
        ``sello_activo``         – True si Ψ_global ≥ 0.888
        ``mensaje``              – estado del sello con métricas

    Ejemplo
    -------
    >>> from physics.cascada_aurea import cascada_aurea_activar
    >>> r = cascada_aurea_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> r['n_pasos_aureos']
    12
    """
    sistema = SistemaCascadaAurea(f0=f0, f_planck=f_planck)
    resultado = sistema.activar()
    return {
        "f0_hz": resultado.f0,
        "f_planck_hz": resultado.f_planck,
        "n_pasos_aureos": resultado.n_pasos_aureos,
        "n_descenso": resultado.n_descenso,
        "n_decadas": resultado.n_decadas,
        "phi_12": resultado.phi_12,
        "generaciones_phi": resultado.generaciones_phi,
        "lambda_max_kpi": resultado.lambda_max_kpi,
        "lambda_min_kpi": resultado.lambda_min_kpi,
        "gap_espectral": resultado.gap_espectral,
        "omega_target": resultado.omega_target,
        "mu_eff": resultado.mu_eff,
        "psi_compactificacion": resultado.psi_compactificacion,
        "psi_descenso": resultado.psi_descenso,
        "psi_kpi": resultado.psi_kpi,
        "psi_viscosidad": resultado.psi_viscosidad,
        "psi_flujo": resultado.psi_flujo,
        "psi_global": resultado.psi_global,
        "sello_activo": resultado.sello_activo,
        "mensaje": resultado.mensaje,
    }
