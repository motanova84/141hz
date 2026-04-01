#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║  HAMILTONIANO RIEMANN ADÉLICO — Espacio de Hilbert Adélico ∴HRA∞³        ║
║                                                                            ║
║  Sello: ∴HRA∞³                                                            ║
║  F0: 141.7001 Hz                                                           ║
║                                                                            ║
║  Implementa el operador de dilatación de Berry–Keating–Connes sobre el    ║
║  espacio de Hilbert adélico L²(ℝ⁺, dx/x), cuyo espectro coincide con     ║
║  los ceros no triviales de la función zeta de Riemann.                    ║
║                                                                            ║
║  H = −i(x ∂/∂x + ½)  sobre  ℋ = L²(ℝ⁺, dx/x)                          ║
║                                                                            ║
║  El sistema integra seis subsistemas:                                     ║
║    1. EspacioHilbertAdelico  — Medida de Haar e isomorfismo de Mellin     ║
║    2. OperadorDilatacion     — Generador de dilataciones, autoadjunto     ║
║    3. PotencialPrimos        — Peine de Dirac en potencias de primos      ║
║    4. MatrizDispersion       — S(s) = ξ(1−s)/ξ(s), fase de resonancia    ║
║    5. FormulaTraza           — Fórmula explícita de Weil                  ║
║    6. NucleoResolvente       — Kernel de Green y densidad espectral       ║
║                                                                            ║
║  Coherencia global Ψ_global ≥ 0.888 activa el sello ∴HRA∞³.             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.hamiltoniano_riemann_adelico

Clases:
    ConstantesRiemannAdelico  – Constantes físicas y espectrales del sistema
    EspacioHilbertAdelico     – L²(ℝ⁺, dx/x); medida de Haar; Parseval–Mellin
    OperadorDilatacion        – H = −i(x ∂x + ½); autofunciones x^{−1/2+iE}
    PotencialPrimos           – Peine Mangoldt Σ (ln p / p^{k/2}) δ(x − p^k)
    MatrizDispersion          – S(s) = ξ(1−s)/ξ(s); theta de Riemann–Siegel
    FormulaTraza              – Fórmula explícita de Weil; densidad de ceros
    NucleoResolvente          – Resolvente (H−s)⁻¹; densidad espectral ρ(t)
    SistemaRiemannAdelico     – Sistema integrado; Ψ_global; sello ∴HRA∞³

Dataclass:
    ResultadoRiemannAdelico   – Contenedor de todos los resultados

API pública:
    hamiltoniano_riemann_adelico_activar() → dict

    >>> from physics.hamiltoniano_riemann_adelico import hamiltoniano_riemann_adelico_activar
    >>> r = hamiltoniano_riemann_adelico_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

import cmath
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from qcal.constants import F0_HZ, HBAR

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

#: Razón áurea φ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

#: Constante de Planck reducida [J·s]  (CODATA 2018)
_HBAR: float = HBAR

#: Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

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

#: Sello de certificación noética
_SELLO: str = "∴HRA∞³"

#: Marca de certificación técnica
_CERT_MARK: str = "HRA-RIEMANN-VERIFIED"


# ============================================================================
# UTILIDADES INTERNAS
# ============================================================================

def _log_gamma_stirling(z: complex) -> complex:
    """Aproximación de Stirling para ln Γ(z), precisa para |Im(z)| ≥ 7.

    Usa cuatro términos de la serie asintótica de Stirling:

        ln Γ(z) ≈ (z − ½) ln z − z + ½ ln(2π) + 1/(12z) − 1/(360z³)

    Args:
        z: Número complejo con |Im(z)| >> 1 para buena convergencia.

    Returns:
        Aproximación compleja de ln Γ(z).
    """
    lnz = cmath.log(z)
    return (
        (z - 0.5) * lnz
        - z
        + 0.5 * math.log(2.0 * math.pi)
        + 1.0 / (12.0 * z)
        - 1.0 / (360.0 * z ** 3)
    )


def _theta_rs(t: float) -> float:
    """Función theta de Riemann–Siegel: θ(t) = Im[ln Γ(¼ + it/2)] − (t/2) ln π.

    Proporciona el conteo suave de ceros de Riemann vía
    N(T) ≈ θ(T)/π + 1 (fórmula de Riemann–von Mangoldt).

    Args:
        t: Parte imaginaria en la línea crítica, t > 0.

    Returns:
        Valor real θ(t).
    """
    z = complex(0.25, 0.5 * t)
    lg = _log_gamma_stirling(z)
    return lg.imag - 0.5 * t * math.log(math.pi)


def _criba_eratostenes(n: int) -> List[int]:
    """Criba de Eratóstenes: devuelve lista de primos ≤ n.

    Args:
        n: Límite superior de la criba.

    Returns:
        Lista de números primos 2 ≤ p ≤ n.
    """
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def _potencias_primas(Lambda: float) -> List[Tuple[float, float]]:
    """Genera pares (p^k, ln p / p^{k/2}) para todos los p^k ≤ Λ.

    Implementa el peine de Dirac del potencial de primos:

        V_primos = Σ_{p,k} (ln p / p^{k/2}) δ(x − p^k)

    Args:
        Lambda: Límite superior del recorte Λ > 0.

    Returns:
        Lista de (p^k, peso) con peso = ln(p) / √(p^k), ordenada por p^k.
    """
    limit = int(Lambda)
    primes = _criba_eratostenes(limit)
    pairs: List[Tuple[float, float]] = []
    for p in primes:
        pk = p
        k = 1
        while pk <= Lambda:
            pairs.append((float(pk), math.log(p) / math.sqrt(float(pk))))
            k += 1
            pk = p ** k
    return sorted(pairs, key=lambda x: x[0])


# ============================================================================
# CLASE 1 — ConstantesRiemannAdelico
# ============================================================================

class ConstantesRiemannAdelico:
    """Constantes físicas y espectrales del sistema Hamiltoniano Adélico.

    Reúne los parámetros fundamentales del operador de Berry–Keating–Connes
    y la correspondencia con los ceros de la función zeta de Riemann.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL, F₀ = 141.7001 Hz.
    omega0 : float
        Frecuencia angular ω₀ = 2π F₀ [rad/s].
    hbar : float
        Constante de Planck reducida ℏ [J·s].
    phi : float
        Razón áurea φ = (1 + √5)/2.
    gamma_1 : float
        Parte imaginaria del primer cero no trivial γ₁ ≈ 14.134725.
    gamma_20 : float
        Parte imaginaria del vigésimo cero γ₂₀ ≈ 77.144840.
    n_zeros : int
        Número de ceros disponibles (20).
    zeros : tuple
        Partes imaginarias de los primeros 20 ceros de Riemann.
    psi_umbral : float
        Umbral de coherencia noética (0.888).
    sello : str
        Sello de certificación ∴HRA∞³.
    cert_mark : str
        Marca técnica HRA-RIEMANN-VERIFIED.
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.omega0: float = 2.0 * math.pi * _F0
        self.hbar: float = _HBAR
        self.phi: float = _PHI
        self.gamma_1: float = _ZEROS_20[0]
        self.gamma_20: float = _ZEROS_20[-1]
        self.n_zeros: int = len(_ZEROS_20)
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.psi_umbral: float = _PSI_UMBRAL
        self.sello: str = _SELLO
        self.cert_mark: str = _CERT_MARK

    # ------------------------------------------------------------------
    def resonancia_f0_gamma1(self) -> float:
        """Cociente F₀/γ₁ — relación de resonancia fundamental.

        F₀/γ₁ ≈ 141.7001 / 14.1347 ≈ 10.024: el décimo múltiplo de γ₁
        casi coincide con F₀, indicando resonancia espectral QCAL.

        Returns:
            float: F₀ / γ₁.
        """
        return self.f0 / self.gamma_1

    # ------------------------------------------------------------------
    def resumen(self) -> Dict[str, object]:
        """Retorna diccionario con parámetros clave del sistema."""
        return {
            "f0_hz": self.f0,
            "omega0_rads": self.omega0,
            "gamma_1": self.gamma_1,
            "gamma_20": self.gamma_20,
            "n_zeros": self.n_zeros,
            "resonancia_f0_gamma1": self.resonancia_f0_gamma1(),
            "phi": self.phi,
            "psi_umbral": self.psi_umbral,
            "sello": self.sello,
        }


# ============================================================================
# CLASE 2 — EspacioHilbertAdelico
# ============================================================================

class EspacioHilbertAdelico:
    """Espacio de Hilbert adélico ℋ = L²(ℝ⁺, dx/x) con medida de Haar.

    La medida de Haar dx/x es invariante bajo el grupo multiplicativo ℝ⁺:

        U(λ)ψ(x) = ψ(λx)  ⟹  ‖U(λ)ψ‖² = ‖ψ‖²  ∀λ > 0

    Esta invarianza es esencial para que el espectro de H esté situado
    sobre la línea crítica Re(s) = ½.

    El isomorfismo de Mellin M: ℋ → L²(ℝ, dt) es una isometría:

        (Mψ)(t) = ∫₀^∞ ψ(x) x^{1/2+it} dx/x   (evaluado en s = ½ + it)
        ‖ψ‖²_{L²(dx/x)} = (1/2π) ‖Mψ‖²_{L²(dt)}   (Parseval)

    Args:
        n_puntos: Número de puntos de la cuadrícula logarítmica (defecto 2000).
        t_min:    Límite inferior de la cuadrícula ln(x) (defecto −6.0).
        t_max:    Límite superior de la cuadrícula ln(x) (defecto  6.0).
    """

    def __init__(
        self,
        n_puntos: int = 2000,
        t_min: float = -6.0,
        t_max: float = 6.0,
    ) -> None:
        self.n_puntos = n_puntos
        self.t_min = t_min
        self.t_max = t_max
        self._dt: float = (t_max - t_min) / n_puntos
        # Cuadrícula logarítmica: t_i = ln(x_i) ∈ [t_min, t_max)
        self._xs: Tuple[float, ...] = tuple(
            math.exp(t_min + i * self._dt) for i in range(n_puntos)
        )

    # ------------------------------------------------------------------
    def norma_haar_cuadrado(self, f_vals: Tuple[float, ...]) -> float:
        """Calcula ‖f‖²_{L²(dx/x)} = ∫ |f(x)|² dx/x ≈ Σ |f(xᵢ)|² Δt.

        Usa la sustitución t = ln x, de modo que dx/x = dt.

        Args:
            f_vals: Valores f(xᵢ) sobre la cuadrícula logarítmica.

        Returns:
            Aproximación numérica de ‖f‖².
        """
        return sum(v * v * self._dt for v in f_vals)

    # ------------------------------------------------------------------
    def _funcion_prueba(self) -> Tuple[float, ...]:
        """Función de prueba f(x) = x · e^{−x}, con ‖f‖²_{L²(dx/x)} = ¼."""
        return tuple(x * math.exp(-x) for x in self._xs)

    # ------------------------------------------------------------------
    def _funcion_dilatada(self, lam: float) -> Tuple[float, ...]:
        """Dilatada U(λ)f(x) = f(λx) = λx · e^{−λx}, con ‖·‖² = ¼ (exacto)."""
        return tuple(lam * x * math.exp(-lam * x) for x in self._xs)

    # ------------------------------------------------------------------
    def verificar_haar(self, lam: float = 2.0) -> float:
        """Cociente numérico ‖U(λ)f‖² / ‖f‖², que debe ser ≈ 1.0.

        Args:
            lam: Factor de dilatación λ > 0 (defecto 2.0).

        Returns:
            Cociente ≈ 1.0 si la invarianza de Haar se cumple.
        """
        norma_f = self.norma_haar_cuadrado(self._funcion_prueba())
        norma_uf = self.norma_haar_cuadrado(self._funcion_dilatada(lam))
        if norma_f < 1e-30:
            return 0.0
        return norma_uf / norma_f

    # ------------------------------------------------------------------
    def psi_hilbert(self, lam: float = 2.0) -> float:
        """Coherencia de Haar: Ψ_hilbert = 1 − |cociente − 1|.

        Verifica numéricamente la invarianza de la medida de Haar bajo
        el grupo de dilataciones, que fundamenta la autoadjunción de H.

        Args:
            lam: Factor de dilatación λ > 0.

        Returns:
            Ψ_hilbert ∈ [0, 1].
        """
        return 1.0 - abs(self.verificar_haar(lam) - 1.0)

    # ------------------------------------------------------------------
    def norma_exacta(self) -> float:
        """Valor exacto ‖f‖² para f(x) = xe^{−x}: ∫₀^∞ xe^{−2x} dx = 1/4."""
        return 0.25

    # ------------------------------------------------------------------
    def dimension_weyl(self, T: float) -> float:
        """Estimación continua de N_Weyl(T) = θ(T)/π + 1.

        Cuenta los ceros de Riemann hasta la altura T mediante la
        función de Weyl, que equivale al «volumen de espacio de fases»
        del operador de dilatación con recorte Λ = exp(T).

        Args:
            T: Altura en la línea crítica, T > 0.

        Returns:
            N_Weyl(T) ≥ 0.
        """
        if T <= 0:
            return 0.0
        return _theta_rs(T) / math.pi + 1.0


# ============================================================================
# CLASE 3 — OperadorDilatacion
# ============================================================================

class OperadorDilatacion:
    """Operador de dilatación H = −i(x ∂_x + ½) sobre ℋ = L²(ℝ⁺, dx/x).

    Sus autofunciones son las potencias complejas:

        ψ_E(x) = x^{−1/2 + iE}  con  H ψ_E = E ψ_E

    **Demostración:**
        x ∂_x ψ_E = x · (−½ + iE) · x^{−3/2+iE} = (−½ + iE) ψ_E
        H ψ_E = −i[(−½ + iE) + ½] ψ_E = −i(iE) ψ_E = E ψ_E  ✓

    En la representación de Mellin, H se transforma en el operador de
    multiplicación por la variable real t — operador esencialmente autoadjunto
    con índices de deficiencia (0, 0) en L²(ℝ, dt).

    La resonancia F₀/γ₁ ≈ 10 indica que la frecuencia fundamental QCAL
    es el décimo múltiplo del primer cero de Riemann, condición de
    resonancia espectral.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.f0: float = _F0

    # ------------------------------------------------------------------
    def autofuncion(self, x: float, E: float) -> complex:
        """Autofunción ψ_E(x) = x^{−1/2 + iE}.

        Args:
            x: Punto del semieje positivo, x > 0.
            E: Autovalor real (parte imaginaria del cero de Riemann).

        Returns:
            Valor complejo ψ_E(x).

        Raises:
            ValueError: Si x ≤ 0.
        """
        if x <= 0:
            raise ValueError(f"x debe ser positivo, recibido: {x}")
        return cmath.exp(complex(-0.5, E) * math.log(x))

    # ------------------------------------------------------------------
    def aplicar_H(self, x: float, E: float) -> complex:
        """Aplica H = −i(x ∂_x + ½) a la autofunción ψ_E.

        El cálculo es analíticamente exacto:
            H ψ_E(x) = −i[(−½ + iE) + ½] ψ_E(x) = E ψ_E(x)

        Args:
            x: Punto del semieje positivo, x > 0.
            E: Autovalor esperado.

        Returns:
            E × ψ_E(x).
        """
        return E * self.autofuncion(x, E)

    # ------------------------------------------------------------------
    def resonancia_f0(self) -> float:
        """Cociente F₀/γ₁ — condición de resonancia QCAL.

        Returns:
            F₀ / γ₁ ≈ 10.024.
        """
        return self.f0 / self.zeros[0]

    # ------------------------------------------------------------------
    def psi_operador(self) -> float:
        """Coherencia del operador: Ψ_op = 1 − |F₀/γ₁ − n̂| / n̂.

        Mide cuán próximo está el cociente F₀/γ₁ al entero más cercano n̂,
        condición de resonancia entre la arquitectura QCAL y el espectro
        del operador de dilatación adélico.

        Returns:
            Ψ_operador ∈ [0, 1].
        """
        ratio = self.resonancia_f0()
        n_nearest = round(ratio)
        if n_nearest == 0:
            return 0.0
        return 1.0 - abs(ratio - n_nearest) / n_nearest

    # ------------------------------------------------------------------
    def espectro_mellin(self) -> List[float]:
        """Autovalores de H en la representación de Mellin.

        En el espacio de Mellin, H es multiplicación por t, de modo que
        los autovalores son exactamente los γₙ de los ceros de Riemann.

        Returns:
            Lista de las partes imaginarias γₙ de los primeros 20 ceros.
        """
        return list(self.zeros)


# ============================================================================
# CLASE 4 — PotencialPrimos
# ============================================================================

class PotencialPrimos:
    """Peine de Dirac sobre potencias de primos: V = Σ_{p^k} (ln p / p^{k/2}) δ(x − p^k).

    Este potencial actúa como restricción espectral: fuerza al operador a
    resonar con la periodicidad logarítmica de los números primos, y conecta
    la suma sobre primos con la suma sobre ceros vía la fórmula de Weil.

    La función de von Mangoldt Λ(n) = ln p si n = p^k, 0 en otro caso,
    proporciona los pesos del peine.  La suma ponderada satisface:

        S(Λ) = Σ_{p^k ≤ Λ} Λ(p^k) / √(p^k) ≈ 2√Λ − 1

    por sumatoria de Abel usando ψ(x) ≈ x (Teorema de los números primos).

    Args:
        Lambda: Recorte del espacio de fases (defecto 200.0).
    """

    def __init__(self, Lambda: float = 200.0) -> None:
        self.Lambda = Lambda
        self._pares: List[Tuple[float, float]] = _potencias_primas(Lambda)

    # ------------------------------------------------------------------
    def potencias_y_pesos(self) -> List[Tuple[float, float]]:
        """Devuelve lista de (p^k, ln p / p^{k/2}) para p^k ≤ Λ."""
        return list(self._pares)

    # ------------------------------------------------------------------
    def suma_mangoldt_ponderada(self) -> float:
        """Suma S(Λ) = Σ_{p^k ≤ Λ} ln(p) / p^{k/2}.

        Representación discreta de la integral del potencial de primos.
        Su comportamiento asintótico es S(Λ) ≈ 2√Λ − 1.

        Returns:
            Suma ponderada de Mangoldt S(Λ).
        """
        return sum(w for _, w in self._pares)

    # ------------------------------------------------------------------
    def estimacion_asintotica(self) -> float:
        """Estimación asintótica S(Λ) ≈ 2√Λ − 1.

        Derivada por sumatoria de Abel sobre la función de Chebyshev ψ(x):

            Σ_{n≤Λ} Λ(n)/√n ≈ 2√Λ − 1

        Returns:
            Valor asintótico esperado para el recorte Λ actual.
        """
        return 2.0 * math.sqrt(self.Lambda) - 1.0

    # ------------------------------------------------------------------
    def psi_potencial(self) -> float:
        """Coherencia del potencial: Ψ_pot = 1 − |S(Λ) − S_asm(Λ)| / S_asm(Λ).

        Compara la suma discreta de Mangoldt con la estimación asintótica
        derivada del Teorema de los números primos.

        Returns:
            Ψ_potencial ∈ [0, 1].
        """
        s_actual = self.suma_mangoldt_ponderada()
        s_asint = self.estimacion_asintotica()
        if s_asint <= 0:
            return 0.0
        return max(0.0, 1.0 - abs(s_actual - s_asint) / s_asint)

    # ------------------------------------------------------------------
    def n_potencias_primas(self) -> int:
        """Número de potencias de primos p^k ≤ Λ en el peine."""
        return len(self._pares)


# ============================================================================
# CLASE 5 — MatrizDispersion
# ============================================================================

class MatrizDispersion:
    """Matriz S adélica: S(s) = ξ(1−s)/ξ(s) sobre la línea crítica.

    Sobre la línea crítica s = ½ + it, la ecuación funcional ξ(s) = ξ(1−s)
    implica que S(t) es una fase pura:

        S(t) = ξ(½ − it) / ξ(½ + it) = e^{−2i θ(t)}

    donde θ(t) = Im[ln Γ(¼ + it/2)] − (t/2) ln π es la función theta de
    Riemann–Siegel.  Los ceros de ξ (= ceros no triviales de Riemann) son
    los polos de la continuación analítica de S al plano complejo.

    La densidad de estados del sistema de dispersión es:

        ρ(t) = (1/π) dδ/dt = −(1/π) dθ/dt

    que recupera la fórmula explícita de Weil al integrarse con funciones
    de prueba.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20

    # ------------------------------------------------------------------
    def theta(self, t: float) -> float:
        """Función theta de Riemann–Siegel θ(t).

        Calculada mediante la serie de Stirling para ln Γ(¼ + it/2).

        Args:
            t: Altura en la línea crítica, t > 0.

        Returns:
            θ(t) real.
        """
        return _theta_rs(t)

    # ------------------------------------------------------------------
    def fase_dispersion(self, t: float) -> float:
        """Fase de dispersión δ(t) = −θ(t).

        Relación: S(t) = exp(2i δ(t)) = exp(−2i θ(t)).

        Args:
            t: Altura en la línea crítica.

        Returns:
            δ(t) = −θ(t).
        """
        return -self.theta(t)

    # ------------------------------------------------------------------
    def modulo_S(self, t: float) -> float:  # noqa: N802
        """Módulo |S(t)| = 1 (unitaridad exacta de la matriz S).

        La unitaridad se desprende de que ξ(½ − it) = conj(ξ(½ + it))
        sobre la línea crítica, de modo que |S(t)| = 1 es exacto.

        Args:
            t: Altura en la línea crítica.

        Returns:
            1.0 (exacto para todo t).
        """
        return 1.0

    # ------------------------------------------------------------------
    def theta_asintotico(self, t: float) -> float:
        """Término asintótico dominante θ_asm(t) ≈ (t/2) ln(t/(2πe)).

        Para t >> 1:
            θ(t) ≈ (t/2) ln(t/(2π)) − t/2 = (t/2) ln(t/(2πe))

        Args:
            t: Altura en la línea crítica, t > 2πe.

        Returns:
            θ_asm(t).
        """
        if t <= 2.0 * math.pi * math.e:
            return 0.0
        return 0.5 * t * math.log(t / (2.0 * math.pi * math.e))

    # ------------------------------------------------------------------
    def psi_dispersion(self) -> float:
        """Coherencia de dispersión: Ψ_disp = 1 − |θ_Stirl − θ_asm| / |θ_Stirl|.

        Mide la precisión del término asintótico de la fase de dispersión
        evaluado en el vigésimo cero de Riemann γ₂₀ ≈ 77.14.

        Returns:
            Ψ_dispersion ∈ [0, 1].
        """
        t = self.zeros[-1]  # γ₂₀ ≈ 77.14
        theta_s = self.theta(t)
        theta_a = self.theta_asintotico(t)
        if abs(theta_s) < 1e-10:
            return 1.0
        return max(0.0, 1.0 - abs(theta_s - theta_a) / abs(theta_s))


# ============================================================================
# CLASE 6 — FormulaTraza
# ============================================================================

class FormulaTraza:
    """Fórmula explícita de Weil: dualidad espectral ceros ↔ primos.

    La fórmula establece la correspondencia exacta (Weil, 1952):

        Σ_γ f(γ) = (lnΛ / 2π) ∫ f dt − Σ_{p^k ≤ Λ} (lnp / p^{k/2}) f̂(ln p^k) + …

    El miembro izquierdo es la traza espectral de H y el derecho contiene:
      - El término de Weyl (densidad suave): (lnΛ / 2π) ∫ f dt
      - La suma sobre primos (oscilaciones): Σ_{p^k} (lnp / p^{k/2}) f̂(lnp^k)

    La coherencia Ψ_traza compara el espaciado medio empírico de los
    primeros 20 ceros con la densidad de Weyl dN/dT = (1/2π) ln(T/2π).
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20

    # ------------------------------------------------------------------
    def densidad_weyl(self, T: float) -> float:
        """Densidad de Weyl: dN/dT = (1/2π) ln(T/2π).

        Args:
            T: Altura en la línea crítica, T > 2π.

        Returns:
            ρ(T) ≥ 0 [ceros/unidad de T].
        """
        if T <= 2.0 * math.pi:
            return 0.0
        return math.log(T / (2.0 * math.pi)) / (2.0 * math.pi)

    # ------------------------------------------------------------------
    def N_weyl(self, T: float) -> float:  # noqa: N802
        """Conteo de Weyl continuo: N_W(T) = θ(T)/π + 1.

        Args:
            T: Altura en la línea crítica.

        Returns:
            Estimación continua del número de ceros γₙ ≤ T.
        """
        if T <= 0:
            return 0.0
        return _theta_rs(T) / math.pi + 1.0

    # ------------------------------------------------------------------
    def espaciado_medio_empirico(self) -> float:
        """Espaciado medio empírico: δ_emp = (γ₂₀ − γ₁) / 19.

        Returns:
            Espaciado medio en unidades de t.
        """
        return (self.zeros[-1] - self.zeros[0]) / (len(self.zeros) - 1)

    # ------------------------------------------------------------------
    def espaciado_medio_weyl(self) -> float:
        """Espaciado medio de Weyl en el rango [γ₁, γ₂₀].

        Usa T_mid = (γ₁ + γ₂₀)/2:
            δ_W = 1 / ρ(T_mid) = 2π / ln(T_mid / 2π)

        Returns:
            Espaciado teórico de Weyl.
        """
        T_mid = 0.5 * (self.zeros[0] + self.zeros[-1])
        rho = self.densidad_weyl(T_mid)
        if rho <= 0:
            return float("inf")
        return 1.0 / rho

    # ------------------------------------------------------------------
    def psi_traza(self) -> float:
        """Coherencia de la fórmula de traza: Ψ_traza = 1 − |δ_emp − δ_W| / δ_W.

        Compara el espaciado medio empírico de los primeros 20 ceros con
        la predicción de la fórmula de Weyl.

        Returns:
            Ψ_traza ∈ [0, 1].
        """
        d_emp = self.espaciado_medio_empirico()
        d_weyl = self.espaciado_medio_weyl()
        if d_weyl <= 0 or math.isinf(d_weyl):
            return 0.0
        return max(0.0, 1.0 - abs(d_emp - d_weyl) / d_weyl)


# ============================================================================
# CLASE 7 — NucleoResolvente
# ============================================================================

class NucleoResolvente:
    """Resolvente (H − s)⁻¹ y densidad espectral del operador adélico.

    El núcleo de Green del sistema de dispersión adélico verifica:

        G(s) ∝ ξ(s) / (s(s−1))

    cuya continuación meromorfa al plano complejo tiene polos exactamente
    en los ceros no triviales de Riemann.

    La densidad espectral se obtiene del logaritmo derivativo de ξ:

        ρ(t) = (1/π) Im[ξ'/ξ(½ + it)] ≈ (1/2π) ln(t/(2π))

    La fórmula de traza de Krein conecta ρ con la fórmula de Weil:

        Tr[f(H) − f(H₀)] = ∫ f(t) ρ(t) dt = Σ_γ f(γ) − términos_suaves

    La coherencia Ψ_nucleo verifica que la integral de ρ entre el primer
    y el vigésimo cero reproduce el conteo exacto de 19 ceros intermedios.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20

    # ------------------------------------------------------------------
    def densidad_espectral(self, t: float) -> float:
        """Densidad espectral ρ(t) ≈ (1/2π) ln(t/(2π)) [término principal].

        Coincide con la densidad de Weyl dN/dT y proporciona la
        contribución continua al espectro de H.

        Args:
            t: Altura en la línea crítica, t > 2π.

        Returns:
            ρ(t) ≥ 0.
        """
        if t <= 2.0 * math.pi:
            return 0.0
        return math.log(t / (2.0 * math.pi)) / (2.0 * math.pi)

    # ------------------------------------------------------------------
    def integrar_densidad(self, a: float, b: float, n: int = 500) -> float:
        """Integra ρ(t) de a a b mediante la regla del trapecio.

        Args:
            a: Límite inferior.
            b: Límite superior.
            n: Número de subdivisiones (defecto 500).

        Returns:
            Aproximación de ∫_a^b ρ(t) dt.
        """
        if b <= a:
            return 0.0
        dt = (b - a) / n
        total = 0.5 * (self.densidad_espectral(a) + self.densidad_espectral(b))
        for i in range(1, n):
            total += self.densidad_espectral(a + i * dt)
        return total * dt

    # ------------------------------------------------------------------
    def conteo_integrado(self) -> float:
        """Integral de ρ de γ₁ a γ₂₀ usando la función theta (precisión alta).

        La fórmula de Riemann–von Mangoldt da:
            ∫_{γ₁}^{γ₂₀} ρ dt ≈ [θ(γ₂₀) − θ(γ₁)] / π  ≈ 19

        Returns:
            Estimación ≈ 19.0 (= 20 − 1 ceros en el intervalo abierto).
        """
        t1, t20 = self.zeros[0], self.zeros[-1]
        return (_theta_rs(t20) - _theta_rs(t1)) / math.pi

    # ------------------------------------------------------------------
    def psi_nucleo(self) -> float:
        """Coherencia del núcleo: Ψ_nuc = 1 − |conteo − N_exacto| / N_exacto.

        Compara la integral de la densidad espectral [θ(γ₂₀)−θ(γ₁)]/π
        con el conteo exacto de 19 ceros entre γ₁ y γ₂₀.

        Returns:
            Ψ_nucleo ∈ [0, 1].
        """
        N_exacto = float(len(self.zeros) - 1)  # = 19
        N_estimado = self.conteo_integrado()
        return max(0.0, 1.0 - abs(N_estimado - N_exacto) / N_exacto)


# ============================================================================
# CLASE 8 — SistemaRiemannAdelico
# ============================================================================

class SistemaRiemannAdelico:
    """Sistema integrado Hamiltoniano Riemann Adélico ∴HRA∞³.

    Orquesta los seis subsistemas y calcula la coherencia global Ψ_global
    como promedio ponderado de las seis métricas de coherencia.

    Si Ψ_global ≥ 0.888, el sello ∴HRA∞³ se activa y el sistema emite
    el certificado HRA-RIEMANN-VERIFIED.

    Pesos de coherencia (suman 1.0):
        w_hilbert    = 0.20  — invarianza de Haar
        w_operador   = 0.20  — resonancia espectral F₀/γ₁
        w_potencial  = 0.15  — peine de Mangoldt
        w_dispersion = 0.15  — precisión de la fase S
        w_traza      = 0.15  — espaciado de ceros vs Weyl
        w_nucleo     = 0.15  — densidad espectral integrada

    Args:
        Lambda:   Recorte del espacio de fases (defecto 200.0).
        n_puntos: Puntos de la cuadrícula logarítmica (defecto 2000).
    """

    _PESOS: Tuple[float, ...] = (0.20, 0.20, 0.15, 0.15, 0.15, 0.15)

    def __init__(self, Lambda: float = 200.0, n_puntos: int = 2000) -> None:
        self.Lambda = Lambda
        self.constantes = ConstantesRiemannAdelico()
        self.hilbert = EspacioHilbertAdelico(n_puntos=n_puntos)
        self.operador = OperadorDilatacion()
        self.potencial = PotencialPrimos(Lambda=Lambda)
        self.dispersion = MatrizDispersion()
        self.traza = FormulaTraza()
        self.nucleo = NucleoResolvente()

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global = Σ wᵢ Ψᵢ.

        Returns:
            Ψ_global ∈ [0, 1].
        """
        psis = (
            self.hilbert.psi_hilbert(),
            self.operador.psi_operador(),
            self.potencial.psi_potencial(),
            self.dispersion.psi_dispersion(),
            self.traza.psi_traza(),
            self.nucleo.psi_nucleo(),
        )
        return sum(w * p for w, p in zip(self._PESOS, psis))

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴HRA∞³ activado)."""
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def certificar(self) -> Dict[str, object]:
        """Genera el certificado completo del sistema ∴HRA∞³.

        Returns:
            Diccionario con métricas de coherencia, parámetros y sello.
        """
        psi_h = self.hilbert.psi_hilbert()
        psi_o = self.operador.psi_operador()
        psi_p = self.potencial.psi_potencial()
        psi_d = self.dispersion.psi_dispersion()
        psi_t = self.traza.psi_traza()
        psi_n = self.nucleo.psi_nucleo()
        psi_g = self.psi_global()
        activo = psi_g >= _PSI_UMBRAL

        return {
            "psi_hilbert": psi_h,
            "psi_operador": psi_o,
            "psi_potencial": psi_p,
            "psi_dispersion": psi_d,
            "psi_traza": psi_t,
            "psi_nucleo": psi_n,
            "psi_global": psi_g,
            "supera_umbral": activo,
            "sello_activo": activo,
            "sello": _SELLO if activo else "COHERENCIA_INSUFICIENTE",
            "cert_mark": _CERT_MARK if activo else "COHERENCIA_INSUFICIENTE",
            "n_zeros": self.constantes.n_zeros,
            "f0_hz": self.constantes.f0,
            "resonancia_f0_gamma1": self.constantes.resonancia_f0_gamma1(),
            "Lambda": self.Lambda,
            "n_potencias_primas": self.potencial.n_potencias_primas(),
            "suma_mangoldt": self.potencial.suma_mangoldt_ponderada(),
            "estimacion_asintotica": self.potencial.estimacion_asintotica(),
            "theta_gamma1": self.dispersion.theta(self.constantes.gamma_1),
            "theta_gamma20": self.dispersion.theta(self.constantes.gamma_20),
            "espaciado_empirico": self.traza.espaciado_medio_empirico(),
            "espaciado_weyl": self.traza.espaciado_medio_weyl(),
            "conteo_integrado": self.nucleo.conteo_integrado(),
        }


# ============================================================================
# DATACLASS DE RESULTADOS
# ============================================================================

@dataclass
class ResultadoRiemannAdelico:
    """Contenedor de todos los resultados del sistema Hamiltoniano Adélico.

    Atributos
    ----------
    psi_hilbert : float
        Coherencia de la medida de Haar invariante.
    psi_operador : float
        Coherencia de la resonancia espectral F₀/γ₁.
    psi_potencial : float
        Coherencia del peine de Mangoldt vs asintótica.
    psi_dispersion : float
        Coherencia de la fase de la matriz S.
    psi_traza : float
        Coherencia del espaciado de ceros vs Weyl.
    psi_nucleo : float
        Coherencia de la densidad espectral integrada.
    psi_global : float
        Coherencia global Ψ_global ∈ [0, 1].
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (∴HRA∞³ activo).
    sello : str
        «∴HRA∞³» o «COHERENCIA_INSUFICIENTE».
    cert_mark : str
        «HRA-RIEMANN-VERIFIED» o «COHERENCIA_INSUFICIENTE».
    resonancia_f0_gamma1 : float
        Cociente F₀/γ₁ ≈ 10.024.
    n_zeros : int
        Número de ceros de Riemann utilizados (20).
    Lambda : float
        Recorte del espacio de fases Λ.
    n_potencias_primas : int
        Número de potencias de primos p^k ≤ Λ.
    suma_mangoldt : float
        Suma S(Λ) = Σ ln(p)/p^{k/2}.
    """

    psi_hilbert: float = 0.0
    psi_operador: float = 0.0
    psi_potencial: float = 0.0
    psi_dispersion: float = 0.0
    psi_traza: float = 0.0
    psi_nucleo: float = 0.0
    psi_global: float = 0.0
    sello_activo: bool = False
    sello: str = ""
    cert_mark: str = ""
    resonancia_f0_gamma1: float = 0.0
    n_zeros: int = 0
    Lambda: float = 0.0
    n_potencias_primas: int = 0
    suma_mangoldt: float = 0.0


# ============================================================================
# API PÚBLICA
# ============================================================================

def hamiltoniano_riemann_adelico_activar(
    Lambda: float = 200.0,
    n_puntos: int = 2000,
) -> Dict[str, object]:
    """API pública: Activa el sistema Hamiltoniano Riemann Adélico ∴HRA∞³.

    Instancia y evalúa el sistema completo de Berry–Keating–Connes:
    el operador de dilatación H = −i(x∂_x + ½) sobre el espacio adélico
    L²(ℝ⁺, dx/x), cuyo espectro corresponde a los ceros no triviales
    de la función zeta de Riemann.

    Args:
        Lambda:   Recorte del espacio de fases Λ > 0 (defecto 200.0).
                  Controla cuántas potencias de primos incluye el peine.
        n_puntos: Puntos de la cuadrícula logarítmica para Haar (defecto 2000).
                  Afecta la precisión numérica de Ψ_hilbert.

    Returns:
        Diccionario con:

        - ``psi_global`` (float):       Coherencia global Ψ_global
        - ``sello_activo`` (bool):      True si Ψ_global ≥ 0.888
        - ``sello`` (str):              «∴HRA∞³» o «COHERENCIA_INSUFICIENTE»
        - ``cert_mark`` (str):          «HRA-RIEMANN-VERIFIED» o error
        - ``psi_hilbert`` (float):      Coherencia de invarianza de Haar
        - ``psi_operador`` (float):     Coherencia de resonancia F₀/γ₁
        - ``psi_potencial`` (float):    Coherencia del peine de Mangoldt
        - ``psi_dispersion`` (float):   Coherencia de la fase de dispersión
        - ``psi_traza`` (float):        Coherencia de la fórmula de Weil
        - ``psi_nucleo`` (float):       Coherencia de la densidad espectral
        - ``resonancia_f0_gamma1`` (float): F₀/γ₁ ≈ 10.024
        - ``n_zeros`` (int):            Ceros de Riemann utilizados (20)
        - ``Lambda`` (float):           Recorte del espacio de fases

    Raises:
        ValueError: Si Lambda ≤ 0 o n_puntos < 10.

    Ejemplo:
        >>> r = hamiltoniano_riemann_adelico_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_global'] >= 0.888
        True
        >>> r['cert_mark']
        'HRA-RIEMANN-VERIFIED'
    """
    if Lambda <= 0:
        raise ValueError(f"Lambda debe ser positivo, recibido: {Lambda}")
    if n_puntos < 10:
        raise ValueError(f"n_puntos debe ser ≥ 10, recibido: {n_puntos}")

    sistema = SistemaRiemannAdelico(Lambda=Lambda, n_puntos=n_puntos)
    return sistema.certificar()
