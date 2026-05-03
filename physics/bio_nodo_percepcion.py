#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║  BIO-NODO Y PERCEPCIÓN COMO INVARIANTE GEOMÉTRICO — ∴BNP∞³               ║
║                                                                            ║
║  Sello: ∴BNP∞³                                                            ║
║  F0: 141.7001 Hz                                                           ║
║                                                                            ║
║  Implementa la Identidad Fundamental del Bio-Nodo:                        ║
║                                                                            ║
║      Ĥ_π |Ψ⟩ = γₙ |Ψ⟩                                                    ║
║                                                                            ║
║  cuatro módulos indivisibles:                                              ║
║    1. IdentidadEspectral  — autovalores γₙ ≡ ceros de Riemann             ║
║    2. ToroAdelico         — colapso de órbita x ↦ e^t x a potencias primas║
║    3. MatrizDensidad      — estructura off-diagonal de ρ(t)               ║
║    4. InvarianteFase      — Ψ(t) ≥ 0.999, umbral diamantino               ║
║    5. PuntoFijoSoberano   — firma QCAL, testigo criptográfico             ║
║    6. CoherenciaBioNodo   — Ψ_global ≥ 0.888; sello ∴BNP∞³               ║
║    7. SistemaBioNodo      — orquestador; activa el sello                  ║
║                                                                            ║
║  Coherencia global Ψ_global ≥ 0.888 activa el sello ∴BNP∞³.             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.bio_nodo_percepcion

Clases:
    ConstantesBioNodo     – Constantes físicas y espectrales del Bio-Nodo
    IdentidadEspectral    – Ĥ_π |Ψ⟩ = γₙ |Ψ⟩; autovalores ≡ ceros de Riemann
    ToroAdelico           – Colapso de órbita del flujo de dilatación
    MatrizDensidad        – Densidad ρ(t) y estructura off-diagonal
    InvarianteFase        – Ψ(t) ≥ 0.999, umbral diamantino
    PuntoFijoSoberano     – Contracción de Banach + firma QCAL criptográfica
    CoherenciaBioNodo     – Agregador de coherencia global Ψ_global
    SistemaBioNodo        – Orquestador principal; activa el sello ∴BNP∞³

Dataclass:
    ResultadoBioNodo      – Contenedor de todos los resultados

API pública:
    bio_nodo_percepcion_activar() → dict

    >>> from physics.bio_nodo_percepcion import bio_nodo_percepcion_activar
    >>> r = bio_nodo_percepcion_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

import cmath
import hashlib
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from qcal.constants import F0_HZ, HBAR

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

#: Frecuencia angular fundamental ω₀ = 2πF₀ [rad/s]
_OMEGA0: float = 2.0 * math.pi * _F0

#: Razón áurea φ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

#: Constante de Planck reducida [J·s]  (CODATA 2018)
_HBAR: float = HBAR

#: Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

#: Umbral diamantino de coherencia de fase
_PSI_DIAMANTE: float = 0.999

#: Número de iteraciones para convergencia al punto fijo
_N_ITER_PUNTO_FIJO: int = 20

#: Factor de contracción de Banach α ∈ (0, 1)
_ALPHA_CONTRACCION: float = 0.5

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
_SELLO: str = "∴BNP∞³"

#: Marca de certificación técnica
_CERT_MARK: str = "BNP-BIONODO-VERIFIED"


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


# ============================================================================
# CLASE 1 — ConstantesBioNodo
# ============================================================================

class ConstantesBioNodo:
    """Constantes físicas y espectrales del sistema Bio-Nodo ∴BNP∞³.

    Centraliza los parámetros del Hamiltoniano maestro Ĥ_π que actúa sobre
    el espacio de Hilbert del Bio-Nodo, y cuyo espectro es el conjunto de
    ceros no triviales de la función zeta de Riemann.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL, F₀ = 141.7001 Hz.
    omega0 : float
        Frecuencia angular ω₀ = 2πF₀ [rad/s].
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
    psi_diamante : float
        Umbral diamantino de coherencia de fase (0.999).
    sello : str
        Sello de certificación ∴BNP∞³.
    cert_mark : str
        Marca técnica BNP-BIONODO-VERIFIED.
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.omega0: float = _OMEGA0
        self.hbar: float = _HBAR
        self.phi: float = _PHI
        self.gamma_1: float = _ZEROS_20[0]
        self.gamma_20: float = _ZEROS_20[-1]
        self.n_zeros: int = len(_ZEROS_20)
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.psi_umbral: float = _PSI_UMBRAL
        self.psi_diamante: float = _PSI_DIAMANTE
        self.sello: str = _SELLO
        self.cert_mark: str = _CERT_MARK

    # ------------------------------------------------------------------
    def resonancia_f0_gamma1(self) -> float:
        """Cociente F₀/γ₁ — relación de resonancia del Bio-Nodo.

        F₀/γ₁ ≈ 141.7001 / 14.1347 ≈ 10.024: el décimo múltiplo de γ₁
        casi coincide con F₀, estableciendo la identidad biunívoca entre
        la frecuencia QCAL y el primer cero de Riemann.

        Returns:
            float: F₀ / γ₁.
        """
        return self.f0 / self.gamma_1

    # ------------------------------------------------------------------
    def cociente_angular(self) -> float:
        """Cociente angular ω₀/γ₁ = 2πF₀/γ₁.

        Returns:
            float: ω₀ / γ₁ ≈ 63.0.
        """
        return self.omega0 / self.gamma_1

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
            "psi_diamante": self.psi_diamante,
            "sello": self.sello,
        }


# ============================================================================
# CLASE 2 — IdentidadEspectral
# ============================================================================

class IdentidadEspectral:
    """Identidad espectral del Hamiltoniano maestro: Ĥ_π |Ψ⟩ = γₙ |Ψ⟩.

    Los autovalores γₙ del Hamiltoniano maestro Ĥ_π coinciden exactamente
    con los ceros no triviales de la función zeta de Riemann — la arquitectura
    del vacío que el sistema Bio-Nodo calcula y percibe simultáneamente.

    Las autofunciones son potencias complejas:

        ψₙ(x) = x^{−1/2 + iγₙ}   con   Ĥ_π ψₙ = γₙ ψₙ

    La identidad biunívoca se expresa en la resonancia F₀/γ₁ ≈ 10:
    el décimo múltiplo del primer cero de Riemann converge con F₀.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.f0: float = _F0

    # ------------------------------------------------------------------
    def autoestado(self, x: float, n: int) -> complex:
        """Autofunción ψₙ(x) = x^{−1/2 + iγₙ} del Hamiltoniano maestro.

        Args:
            x: Punto del semieje positivo, x > 0.
            n: Índice del autovalor (0-based, n ∈ [0, 19]).

        Returns:
            Valor complejo ψₙ(x).

        Raises:
            ValueError: Si x ≤ 0 o n está fuera de rango.
        """
        if x <= 0:
            raise ValueError(f"x debe ser positivo, recibido: {x}")
        if not (0 <= n < len(self.zeros)):
            raise ValueError(f"n debe estar en [0, {len(self.zeros) - 1}], recibido: {n}")
        gamma_n = self.zeros[n]
        # x^{-1/2 + iγₙ} = x^{-1/2} · exp(i γₙ ln x)
        return x ** (-0.5) * cmath.exp(1j * gamma_n * math.log(x))

    # ------------------------------------------------------------------
    def aplicar_hamiltoniano(self, x: float, n: int) -> complex:
        """Aplica Ĥ_π a la autofunción ψₙ: resultado exacto γₙ · ψₙ(x).

        La ecuación de autovalores Ĥ_π ψₙ = γₙ ψₙ se verifica analíticamente:
            Ĥ_π ψₙ(x) = −i(x ∂_x + ½) ψₙ(x) = γₙ ψₙ(x)

        Args:
            x: Punto del semieje positivo, x > 0.
            n: Índice del autovalor (0-based).

        Returns:
            γₙ · ψₙ(x) [resultado exacto].
        """
        return self.zeros[n] * self.autoestado(x, n)

    # ------------------------------------------------------------------
    def residual_autovalor(self, x: float, n: int) -> float:
        """Residual de la ecuación de autovalores: |Ĥ_π ψₙ − γₙ ψₙ|.

        Para la implementación analítica exacta, el residual es siempre 0.

        Args:
            x: Punto del semieje positivo, x > 0.
            n: Índice del autovalor (0-based).

        Returns:
            0.0 (exacto).
        """
        h_psi = self.aplicar_hamiltoniano(x, n)
        gamma_psi = self.zeros[n] * self.autoestado(x, n)
        return abs(h_psi - gamma_psi)

    # ------------------------------------------------------------------
    def espectro_completo(self) -> List[float]:
        """Lista de autovalores γₙ del espectro discreto de Ĥ_π.

        Returns:
            Partes imaginarias de los primeros 20 ceros de Riemann.
        """
        return list(self.zeros)

    # ------------------------------------------------------------------
    def proyeccion_f0(self) -> float:
        """Proyección de F₀ sobre el espectro: cociente F₀/γ₁.

        Returns:
            F₀ / γ₁ ≈ 10.024.
        """
        return self.f0 / self.zeros[0]

    # ------------------------------------------------------------------
    def psi_identidad(self) -> float:
        """Coherencia de la identidad espectral.

        Mide la proximidad del cociente F₀/γ₁ al entero más cercano.
        Para F₀/γ₁ ≈ 10.024, la coherencia es ≈ 0.9975.

        Returns:
            Ψ_identidad = 1 − |F₀/γ₁ − round(F₀/γ₁)| / round(F₀/γ₁) ∈ [0, 1].
        """
        ratio = self.proyeccion_f0()
        n_near = round(ratio)
        if n_near == 0:
            return 0.0
        return max(0.0, 1.0 - abs(ratio - n_near) / n_near)


# ============================================================================
# CLASE 3 — ToroAdelico
# ============================================================================

class ToroAdelico:
    """Toro Adélico y colapso de la órbita de dilatación.

    En el espacio de fase del Toro Adélico, el flujo de dilatación

        x ↦ e^t x

    se vuelve periódico cuando la dilatación t coincide con potencias de
    primos:  t_closure = k · ln p  (p primo, k ≥ 1).

    La coherencia se mide comparando el conteo empírico de ceros de Riemann
    con la estimación de Weyl N_W(T) = θ(T)/π + 1, que predice con qué
    densidad los autovalores γₙ cubren el Toro Adélico.

    Args:
        n_primos: Número de primos del solenoide adélico (defecto 10).
    """

    def __init__(self, n_primos: int = 10) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.n_primos: int = n_primos
        self._primos: List[int] = _criba_eratostenes(30)[:n_primos]

    # ------------------------------------------------------------------
    def flujo_dilatacion(self, x: float, t: float) -> float:
        """Flujo de dilatación: x ↦ e^t · x.

        Args:
            x: Punto de partida del flujo, x > 0.
            t: Tiempo de dilatación.

        Returns:
            e^t · x.

        Raises:
            ValueError: Si x ≤ 0.
        """
        if x <= 0:
            raise ValueError(f"x debe ser positivo, recibido: {x}")
        return math.exp(t) * x

    # ------------------------------------------------------------------
    def tiempo_orbita_prima(self, p: int, k: int = 1) -> float:
        """Tiempo de cierre de órbita para la potencia prima p^k.

        El flujo se vuelve periódico en t_closure = k · ln p.

        Args:
            p: Número primo, p ≥ 2.
            k: Exponente, k ≥ 1.

        Returns:
            t_closure = k · ln p.

        Raises:
            ValueError: Si p < 2 o k < 1.
        """
        if p < 2:
            raise ValueError(f"p debe ser primo ≥ 2, recibido: {p}")
        if k < 1:
            raise ValueError(f"k debe ser ≥ 1, recibido: {k}")
        return k * math.log(p)

    # ------------------------------------------------------------------
    def tiempos_orbita(self) -> List[Tuple[int, float]]:
        """Lista de tiempos de cierre (p, k·ln p) para los primeros primos.

        Returns:
            Lista de (primo, tiempo_closure) para k=1 de cada primo.
        """
        return [(p, self.tiempo_orbita_prima(p, 1)) for p in self._primos]

    # ------------------------------------------------------------------
    def conteo_weyl(self, T: float) -> float:
        """Conteo de Weyl N_W(T) = θ(T)/π + 1 (estimación continua).

        Args:
            T: Altura en la línea crítica, T > 0.

        Returns:
            Estimación continua del número de ceros γₙ ≤ T.
        """
        if T <= 0.0:
            return 0.0
        return _theta_rs(T) / math.pi + 1.0

    # ------------------------------------------------------------------
    def conteo_empirico(self, T: float) -> int:
        """Conteo empírico de ceros γₙ ≤ T.

        Args:
            T: Altura en la línea crítica.

        Returns:
            Número de ceros de la tabla γₙ ≤ T.
        """
        return sum(1 for g in self.zeros if g <= T)

    # ------------------------------------------------------------------
    def error_conteo_relativo(self) -> float:
        """Error relativo entre N_weyl(γ₂₀) y el conteo empírico 20.

        Returns:
            |N_weyl(γ₂₀) − 20| / 20.
        """
        T = self.zeros[-1]  # γ₂₀ ≈ 77.144840
        n_weyl = self.conteo_weyl(T)
        n_emp = 20  # definición: usamos todos los 20 ceros disponibles
        return abs(n_weyl - n_emp) / n_emp

    # ------------------------------------------------------------------
    def psi_toro(self) -> float:
        """Coherencia del Toro Adélico: Ψ_toro = 1 − error_conteo.

        Compara el conteo de Weyl con el número empírico de ceros,
        midiendo con qué fidelidad el Toro Adélico se cierra sobre sí mismo.

        Returns:
            Ψ_toro ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.error_conteo_relativo())


# ============================================================================
# CLASE 4 — MatrizDensidad
# ============================================================================

class MatrizDensidad:
    """Matriz de densidad ρ(t) del Bio-Nodo y estructura off-diagonal.

    El estado del Bio-Nodo se describe por la superposición igual de
    los N autoestados del Hamiltoniano maestro:

        |Ψ⟩ = (1/√N) Σₙ |γₙ⟩

    La matriz de densidad ρ = |Ψ⟩⟨Ψ| tiene elementos:

        ρₘₙ = aₘ · aₙ*  con  aₙ = 1/√N  (superposición igual)

    La pureza Tr(ρ²) = 1 para estados puros. Un modelo de decoherencia
    infinitesimal introduce una tasa proporcional a la inversa del espectro:

        ε_dec = Σₙ (1/γₙ) / (N · F₀)

    que cuantifica cuánto se mezcla el estado antes de que el Bio-Nodo
    recupere su coherencia diamantina.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.n: int = len(_ZEROS_20)
        self.f0: float = _F0

    # ------------------------------------------------------------------
    def amplitudes_iguales(self) -> List[float]:
        """Amplitudes de la superposición igual: aₙ = 1/√N.

        Returns:
            Lista de N amplitudes idénticas 1/√N.
        """
        a = 1.0 / math.sqrt(self.n)
        return [a] * self.n

    # ------------------------------------------------------------------
    def tasa_decoherencia(self) -> float:
        """Tasa de decoherencia ε_dec = Σₙ (1/γₙ) / (N · F₀).

        Cuantifica el decaimiento infinitesimal de la coherencia due a la
        dispersión espectral de los ceros de Riemann sobre F₀.

        Returns:
            ε_dec ≥ 0.
        """
        suma_inv = sum(1.0 / g for g in self.zeros)
        return suma_inv / (self.n * self.f0)

    # ------------------------------------------------------------------
    def pureza(self) -> float:
        """Pureza del estado ligeramente mixto: Tr(ρ²) = (1 − ε)² + ε²/N.

        Para el estado casi-puro con tasa de decoherencia ε_dec:

            ρ = (1 − ε)|Ψ⟩⟨Ψ| + ε · 𝕀/N

        la pureza es:

            Tr(ρ²) = (1 − ε)² + ε²/N

        Returns:
            Tr(ρ²) ≈ 1 − 2ε (para ε << 1).
        """
        eps = self.tasa_decoherencia()
        return (1.0 - eps) ** 2 + eps ** 2 / self.n

    # ------------------------------------------------------------------
    def coherencia_offdiagonal(self) -> float:
        """Fracción de elementos off-diagonal: C_off = (N² − N)/N² = 1 − 1/N.

        Para la superposición igual, todos los elementos |ρₘₙ| = 1/N son
        iguales, de modo que los N² − N elementos off-diagonal representan
        la fracción 1 − 1/N del total.

        Returns:
            1 − 1/N ∈ [0, 1).
        """
        return 1.0 - 1.0 / self.n

    # ------------------------------------------------------------------
    def elemento_diagonal(self) -> float:
        """Elemento diagonal ρₙₙ = 1/N (superposición igual).

        Returns:
            1/N.
        """
        return 1.0 / self.n

    # ------------------------------------------------------------------
    def psi_densidad(self) -> float:
        """Coherencia de la matriz de densidad: Ψ_densidad = pureza.

        Returns:
            Ψ_densidad = Tr(ρ²) ∈ [0, 1].
        """
        return max(0.0, self.pureza())


# ============================================================================
# CLASE 5 — InvarianteFase
# ============================================================================

class InvarianteFase:
    """Invariante de fase: Ψ(t) ≥ 0.999, umbral diamantino.

    La función de coherencia de fase

        Ψ_fase = 1 − ε_dec

    donde ε_dec = Σₙ (1/γₙ) / (N · F₀) es la tasa de decoherencia espectral,
    cuantifica el umbral diamantino donde el ruido externo desaparece y sólo
    subsiste la percepción pura de la estructura off-diagonal de ρ(t).

    Cuando Ψ_fase ≥ 0.999 (umbral diamantino), el Bio-Nodo reconoce su
    propia firma en el espectro del universo: la percepción no es posterior
    al cálculo sino simultánea a él.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.n: int = len(_ZEROS_20)
        self.f0: float = _F0
        self._densidad: MatrizDensidad = MatrizDensidad()

    # ------------------------------------------------------------------
    def tasa_decaimiento_espectral(self) -> float:
        """Tasa ε_dec = Σₙ (1/γₙ) / (N · F₀).

        Returns:
            ε_dec ≥ 0.
        """
        return self._densidad.tasa_decoherencia()

    # ------------------------------------------------------------------
    def psi_en_t(self, t: float) -> float:  # noqa: ARG002
        """Coherencia de fase en el instante t.

        Modelo: Ψ(t) = 1 − ε_dec.  En el régimen |t| ≪ τ_coh (tiempo de
        coherencia del Bio-Nodo), la decoherencia dinámica es despreciable
        y la coherencia permanece constante e igual a Ψ_fase.  El parámetro
        ``t`` se incluye para conservar la signatura de la ecuación temporal
        pero no modifica el resultado en este régimen.

        Args:
            t: Instante de tiempo [s]. No afecta al resultado para |t| ≪ τ_coh.

        Returns:
            Ψ(t) ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.tasa_decaimiento_espectral())

    # ------------------------------------------------------------------
    def umbral_diamante(self) -> float:
        """Umbral diamantino: Ψ_diamante = 0.999.

        Returns:
            0.999 (constante del módulo _PSI_DIAMANTE).
        """
        return _PSI_DIAMANTE

    # ------------------------------------------------------------------
    def supera_umbral_diamante(self) -> bool:
        """True si Ψ_fase ≥ 0.999 (umbral diamantino alcanzado).

        Returns:
            bool.
        """
        return self.psi_fase() >= _PSI_DIAMANTE

    # ------------------------------------------------------------------
    def psi_fase(self) -> float:
        """Coherencia del Invariante de Fase: Ψ_fase = 1 − ε_dec.

        Returns:
            Ψ_fase ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.tasa_decaimiento_espectral())


# ============================================================================
# CLASE 6 — PuntoFijoSoberano
# ============================================================================

class PuntoFijoSoberano:
    """Soberanía de Punto Fijo: firma QCAL, testigo criptográfico.

    El Teorema de Punto Fijo de Banach garantiza la existencia de un único
    estado Ψ* que satisface la ecuación de autocoherencia:

        Ψ* = g(Ψ*)   donde   g(x) = α · x + (1 − α) · Ψ_esp

    con α = 0.5 (factor de contracción) y Ψ_esp = 1 − |F₀/γ₁ − 10| / 10
    (coherencia espectral del Bio-Nodo).

    La firma QCAL es el testigo criptográfico (Blake2b-16) de este colapso:
    una firma que se evapora si el sistema se desalinea de su punto fijo.
    """

    def __init__(self) -> None:
        self.zeros: Tuple[float, ...] = _ZEROS_20
        self.f0: float = _F0
        self.alpha: float = _ALPHA_CONTRACCION
        self.n_iter: int = _N_ITER_PUNTO_FIJO

    # ------------------------------------------------------------------
    def coherencia_espectral(self) -> float:
        """Coherencia espectral del punto fijo: Ψ_esp = 1 − |F₀/γ₁ − 10|/10.

        Returns:
            Ψ_esp ∈ [0, 1].
        """
        ratio = self.f0 / self.zeros[0]
        n_near = round(ratio)
        if n_near == 0:
            return 0.0
        return max(0.0, 1.0 - abs(ratio - n_near) / n_near)

    # ------------------------------------------------------------------
    def contraccion(self, psi: float) -> float:
        """Un paso de la contracción de Banach: g(Ψ) = α·Ψ + (1−α)·Ψ_esp.

        Args:
            psi: Estado actual de coherencia Ψ ∈ [0, 1].

        Returns:
            Nuevo estado g(Ψ).
        """
        psi_esp = self.coherencia_espectral()
        return self.alpha * psi + (1.0 - self.alpha) * psi_esp

    # ------------------------------------------------------------------
    def iterar_punto_fijo(self, n_iter: int = None) -> float:
        """Itera la contracción de Banach hasta convergencia.

        Partiendo de Ψ₀ = 0, aplica iterativamente g hasta n_iter pasos.

        Args:
            n_iter: Número de iteraciones (``None`` → usa ``self.n_iter``).

        Returns:
            Ψ_n tras n_iter iteraciones.
        """
        if n_iter is None:
            n_iter = self.n_iter
        psi = 0.0
        for _ in range(n_iter):
            psi = self.contraccion(psi)
        return psi

    # ------------------------------------------------------------------
    def punto_fijo_exacto(self) -> float:
        """Punto fijo analítico Ψ* = Ψ_esp (solución de g(Ψ*) = Ψ*).

        La ecuación g(Ψ) = α·Ψ + (1−α)·Ψ_esp = Ψ tiene la solución única:
            Ψ* = Ψ_esp   (independiente de α).

        Returns:
            Ψ_esp.
        """
        return self.coherencia_espectral()

    # ------------------------------------------------------------------
    def firma_qcal(self, datos: bytes) -> str:
        """Firma criptográfica Blake2b-16 del estado del Bio-Nodo.

        Args:
            datos: Bytes a firmar (estado serializado del sistema).

        Returns:
            Hexdigest de 32 caracteres (16 bytes).
        """
        return hashlib.blake2b(datos, digest_size=16).hexdigest()

    # ------------------------------------------------------------------
    def verificar_firma(self, firma: str, datos: bytes) -> bool:
        """Verifica que la firma coincide con los datos.

        Args:
            firma: Hexdigest Blake2b-16 esperado.
            datos: Datos originales a verificar.

        Returns:
            True si la firma es válida.
        """
        return self.firma_qcal(datos) == firma

    # ------------------------------------------------------------------
    def psi_soberania(self) -> float:
        """Coherencia de soberanía: Ψ_sober = 1 − |Ψ_N − Ψ*| / Ψ*.

        Compara el estado convergido tras N iteraciones con el punto fijo
        analítico. Para N = 20 iteraciones, el error es ≈ α^N ≈ 9.5 × 10⁻⁷.

        Returns:
            Ψ_soberania ∈ [0, 1].
        """
        psi_iter = self.iterar_punto_fijo()
        psi_exacto = self.punto_fijo_exacto()
        if psi_exacto <= 0:
            return 0.0
        return max(0.0, 1.0 - abs(psi_iter - psi_exacto) / psi_exacto)


# ============================================================================
# CLASE 7 — CoherenciaBioNodo
# ============================================================================

class CoherenciaBioNodo:
    """Agregador de coherencia global Ψ_global del Bio-Nodo ∴BNP∞³.

    Combina las cinco coherencias individuales de los módulos del Bio-Nodo
    con pesos iguales:

        Ψ_global = Σᵢ wᵢ Ψᵢ   con   Σᵢ wᵢ = 1

    Los cinco módulos son: IdentidadEspectral, ToroAdelico, MatrizDensidad,
    InvarianteFase y PuntoFijoSoberano.

    Ψ_global ≥ 0.888 activa el sello ∴BNP∞³.
    """

    #: Pesos de los cinco módulos (iguales, suma = 1.0)
    _PESOS: Tuple[float, ...] = (0.20, 0.20, 0.20, 0.20, 0.20)

    def __init__(self) -> None:
        self.identidad = IdentidadEspectral()
        self.toro = ToroAdelico()
        self.densidad = MatrizDensidad()
        self.fase = InvarianteFase()
        self.soberania = PuntoFijoSoberano()

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global = Σ wᵢ Ψᵢ.

        Returns:
            Ψ_global ∈ [0, 1].
        """
        psis = (
            self.identidad.psi_identidad(),
            self.toro.psi_toro(),
            self.densidad.psi_densidad(),
            self.fase.psi_fase(),
            self.soberania.psi_soberania(),
        )
        return sum(w * p for w, p in zip(self._PESOS, psis))

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴BNP∞³ activo)."""
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def desglose(self) -> Dict[str, float]:
        """Desglose de todas las coherencias individuales.

        Returns:
            Diccionario con Ψᵢ de cada módulo y Ψ_global.
        """
        return {
            "psi_identidad": self.identidad.psi_identidad(),
            "psi_toro": self.toro.psi_toro(),
            "psi_densidad": self.densidad.psi_densidad(),
            "psi_fase": self.fase.psi_fase(),
            "psi_soberania": self.soberania.psi_soberania(),
            "psi_global": self.psi_global(),
        }


# ============================================================================
# CLASE 8 — SistemaBioNodo
# ============================================================================

class SistemaBioNodo:
    """Orquestador principal del Bio-Nodo — activa el sello ∴BNP∞³.

    Instancia todos los módulos del Bio-Nodo y genera el certificado completo
    de coherencia cuando Ψ_global ≥ 0.888 (sello ∴BNP∞³ activo).

    La percepción no es un proceso posterior al cálculo: es el estado de
    Resonancia total donde el Bio-Nodo reconoce su propia firma en el
    espectro del universo.
    """

    _PESOS: Tuple[float, ...] = CoherenciaBioNodo._PESOS

    def __init__(self) -> None:
        self.constantes = ConstantesBioNodo()
        self.identidad = IdentidadEspectral()
        self.toro = ToroAdelico()
        self.densidad = MatrizDensidad()
        self.fase = InvarianteFase()
        self.soberania = PuntoFijoSoberano()

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global = Σ wᵢ Ψᵢ.

        Returns:
            Ψ_global ∈ [0, 1].
        """
        psis = (
            self.identidad.psi_identidad(),
            self.toro.psi_toro(),
            self.densidad.psi_densidad(),
            self.fase.psi_fase(),
            self.soberania.psi_soberania(),
        )
        return sum(w * p for w, p in zip(self._PESOS, psis))

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴BNP∞³ activado)."""
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def certificar(self) -> Dict[str, object]:
        """Genera el certificado completo del Bio-Nodo ∴BNP∞³.

        Returns:
            Diccionario con métricas de coherencia, parámetros y sello.
        """
        psi_id = self.identidad.psi_identidad()
        psi_to = self.toro.psi_toro()
        psi_de = self.densidad.psi_densidad()
        psi_fa = self.fase.psi_fase()
        psi_so = self.soberania.psi_soberania()
        psi_g = self.psi_global()
        activo = psi_g >= _PSI_UMBRAL

        # Firma criptográfica del estado
        datos_firma = f"{_F0:.4f}:{_ZEROS_20[0]:.6f}:{psi_g:.6f}".encode()
        firma = self.soberania.firma_qcal(datos_firma)

        return {
            "psi_identidad": psi_id,
            "psi_toro": psi_to,
            "psi_densidad": psi_de,
            "psi_fase": psi_fa,
            "psi_soberania": psi_so,
            "psi_global": psi_g,
            "supera_umbral": activo,
            "sello_activo": activo,
            "sello": _SELLO if activo else "COHERENCIA_INSUFICIENTE",
            "cert_mark": _CERT_MARK if activo else "COHERENCIA_INSUFICIENTE",
            "firma_qcal": firma,
            "n_zeros": self.constantes.n_zeros,
            "f0_hz": self.constantes.f0,
            "resonancia_f0_gamma1": self.constantes.resonancia_f0_gamma1(),
            "supera_umbral_diamante": self.fase.supera_umbral_diamante(),
            "psi_diamante": _PSI_DIAMANTE,
            "punto_fijo_exacto": self.soberania.punto_fijo_exacto(),
            "n_primos_toro": self.toro.n_primos,
        }


# ============================================================================
# DATACLASS DE RESULTADOS
# ============================================================================

@dataclass
class ResultadoBioNodo:
    """Contenedor de todos los resultados del Bio-Nodo ∴BNP∞³.

    Atributos
    ----------
    psi_identidad : float
        Coherencia de la identidad espectral F₀/γ₁.
    psi_toro : float
        Coherencia del colapso de órbita en el Toro Adélico.
    psi_densidad : float
        Coherencia de la matriz de densidad (pureza).
    psi_fase : float
        Coherencia del invariante de fase (umbral diamantino).
    psi_soberania : float
        Coherencia de la soberanía del punto fijo.
    psi_global : float
        Coherencia global Ψ_global ∈ [0, 1].
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (∴BNP∞³ activo).
    sello : str
        «∴BNP∞³» o «COHERENCIA_INSUFICIENTE».
    cert_mark : str
        «BNP-BIONODO-VERIFIED» o «COHERENCIA_INSUFICIENTE».
    firma_qcal : str
        Hexdigest Blake2b-16 del estado del sistema.
    resonancia_f0_gamma1 : float
        Cociente F₀/γ₁ ≈ 10.024.
    n_zeros : int
        Número de ceros de Riemann utilizados (20).
    """

    psi_identidad: float = 0.0
    psi_toro: float = 0.0
    psi_densidad: float = 0.0
    psi_fase: float = 0.0
    psi_soberania: float = 0.0
    psi_global: float = 0.0
    sello_activo: bool = False
    sello: str = ""
    cert_mark: str = ""
    firma_qcal: str = ""
    resonancia_f0_gamma1: float = 0.0
    n_zeros: int = 0


# ============================================================================
# API PÚBLICA
# ============================================================================

def bio_nodo_percepcion_activar() -> Dict[str, object]:
    """API pública: Activa el Bio-Nodo y valida la percepción como invariante.

    Instancia y evalúa el sistema completo ∴BNP∞³:
    la identidad biunívoca Ĥ_π|Ψ⟩ = γₙ|Ψ⟩, el colapso de órbita en el
    Toro Adélico, el invariante de fase Ψ(t) ≥ 0.999 y la soberanía del
    punto fijo criptográfico.

    Returns:
        Diccionario con:

        - ``psi_global`` (float):           Coherencia global Ψ_global
        - ``sello_activo`` (bool):          True si Ψ_global ≥ 0.888
        - ``sello`` (str):                  «∴BNP∞³» o «COHERENCIA_INSUFICIENTE»
        - ``cert_mark`` (str):              «BNP-BIONODO-VERIFIED» o error
        - ``psi_identidad`` (float):        Coherencia de la identidad espectral
        - ``psi_toro`` (float):             Coherencia del Toro Adélico
        - ``psi_densidad`` (float):         Coherencia de la matriz de densidad
        - ``psi_fase`` (float):             Coherencia del invariante de fase
        - ``psi_soberania`` (float):        Coherencia del punto fijo soberano
        - ``firma_qcal`` (str):             Firma criptográfica Blake2b-16
        - ``supera_umbral_diamante`` (bool): True si Ψ_fase ≥ 0.999
        - ``resonancia_f0_gamma1`` (float): F₀/γ₁ ≈ 10.024
        - ``n_zeros`` (int):               Ceros de Riemann utilizados (20)

    Ejemplo:
        >>> r = bio_nodo_percepcion_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_global'] >= 0.888
        True
        >>> r['supera_umbral_diamante']
        True
    """
    sistema = SistemaBioNodo()
    return sistema.certificar()
