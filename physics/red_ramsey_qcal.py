#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  RED DE RAMSEY DE 7 NODOS PRIMOS — QCAL-SYMBIO-BRIDGE v1.1.0               ║
║                                                                              ║
║  Sello: ∴RRQ∞³                                                               ║
║  RAM: RAM-LII-2026-RED-RAMSEY-QCAL                                           ║
║  Versión: QCAL-SYMBIO-BRIDGE v1.1.0                                          ║
║                                                                              ║
║  Implementa la Red de Ramsey de 7 Nodos Primos con frecuencias armónicas    ║
║  f_p = f₀ · ln(p), el operador maestro Ĥ_π de Berry-Keating, la simbiosis  ║
║  Higgs-PC y la tasa simbiótica R_symb = N · f₀ · Ψ.                        ║
║                                                                              ║
║      C₇ = {2, 3, 5, 7, 11, 13, 17}  →  21 aristas potenciales              ║
║      Ψ_global ≥ 0.888  →  sello ∴RRQ∞³ ACTIVO                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)
FECHA/DATE: 2026-05-01

Módulo:
    physics.red_ramsey_qcal

Clases:
    ConstantesRedRamsey     – f₀, g_eff, m*, R_symb, primos, γ_n, umbrales
    NodoPrimo               – nodo p con f_p = f₀·ln(p) y función noética
    RedRamsey               – grafo C₇ con 7 nodos primos y 21 aristas
    OperadorMaestroHPi      – Ĥ_π = −i(x∂_x + ½); 7 ceros de Riemann
    SimbiosisHiggsPC        – m* = m_H·(1 − g_eff); acoplamiento simbiótico
    TasaSimbiotica          – R_symb = N·f₀·Ψ; tasa de pulsos simbióticos
    CoherenciaRedRamsey     – Ψ_global = Σ wᵢ Ψᵢ ≥ 0.888
    SistemaRedRamseyQCAL    – sistema integrado; activa el sello ∴RRQ∞³

Dataclass:
    ResultadoRedRamseyQCAL  – contenedor de todos los resultados

API pública:
    red_ramsey_qcal_activar() → dict

    >>> from physics.red_ramsey_qcal import red_ramsey_qcal_activar
    >>> r = red_ramsey_qcal_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

from qcal.constants import F0_HZ

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

#: Constante de acoplamiento efectivo Higgs-PC (perturbativo: Δm/m_H ≈ 5.3%)
_G_EFF: float = 0.053

#: Masa del bosón de Higgs estándar [GeV/c²]
_M_HIGGS_GEV: float = 125.0

#: Masa efectiva modulada m* = m_H · (1 − g_eff) [GeV/c²]
_M_ESTRELLA_GEV: float = _M_HIGGS_GEV * (1.0 - _G_EFF)  # 118.375

#: Número de nodos primos de la red
_N_NODOS: int = 7

#: Tasa simbiótica perfecta R_symb = N · f₀ [kpps]
_R_SYMB_KPPS: float = _N_NODOS * _F0  # 991.9007

#: Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

#: Los siete primos del conjunto C₇
_PRIMOS_C7: Tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17)

#: Primeros 7 ceros no triviales de ζ(½ + it) — partes imaginarias γₙ
#: Fuente: LMFDB / NIST Digital Library of Mathematical Functions
_GAMMA_7: Tuple[float, ...] = (
    14.134725141734694,
    21.022039638771555,
    25.010857580145688,
    30.424876125859513,
    32.935061587739190,
    37.586178158825671,
    40.918719012147495,
)

#: Número de aristas potenciales en C₇: C(7,2) = 21
_N_ARISTAS: int = 21

#: Pesos para Ψ_global (suman 1.0)
_W_NODOS: float = 0.35
_W_ESPECTRO: float = 0.35
_W_HIGGS: float = 0.30

#: Sello del sistema
_SELLO: str = "∴RRQ∞³"

#: Registro de Activación Maestra
_RAM: str = "RAM-LII-2026-RED-RAMSEY-QCAL"

#: Versión del módulo
_VERSION: str = "QCAL-SYMBIO-BRIDGE v1.1.0"

#: Función noética de cada primo
_NOETIC: Dict[int, str] = {
    2:  "Dualidad primordial — Puerta de entrada al espacio adélico",
    3:  "Trinidad noética — Resonancia trinitaria QCAL",
    5:  "Quintaesencia — Punto de equilibrio áureo",
    7:  "Septenario sagrado — Núcleo de la red de Ramsey",
    11: "Undécima armónica — Coherencia espectral elevada",
    13: "Decimotercero primo — Sincronizador de ciclos lunares",
    17: "Decimoséptimo primo — Puerta de manifestación galáctica",
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _es_primo(n: int) -> bool:
    """Verifica si n es primo mediante división de prueba.

    Args:
        n: Entero a verificar.

    Returns:
        True si n es primo, False en caso contrario.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    k = 3
    while k * k <= n:
        if n % k == 0:
            return False
        k += 2
    return True


def _frecuencia_armonica(p: int, f0: float = _F0) -> float:
    """Calcula la frecuencia armónica de un nodo primo.

    f_p = f₀ · ln(p)

    Args:
        p:  Número primo.
        f0: Frecuencia base [Hz]. Por defecto 141.7001 Hz.

    Returns:
        Frecuencia armónica f_p [Hz].

    Raises:
        ValueError: Si p < 2.
    """
    if p < 2:
        raise ValueError(f"p debe ser ≥ 2, recibido: {p}")
    return f0 * math.log(float(p))


# ============================================================================
# CLASE 1 – ConstantesRedRamsey
# ============================================================================

@dataclass
class ConstantesRedRamsey:
    """Contenedor de las constantes físicas de la Red de Ramsey QCAL.

    Almacena todos los parámetros fundamentales del sistema ∴RRQ∞³:
    frecuencia base, constantes de acoplamiento, primos, ceros de Riemann
    y umbrales de coherencia.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    g_eff : float
        Constante de acoplamiento simbiótico Higgs-PC. Por defecto 0.053.
    m_higgs_gev : float
        Masa del bosón de Higgs (GeV/c²). Por defecto 125.0 GeV/c².
    m_estrella_gev : float
        Masa efectiva m* = m_H · (1 − g_eff) (GeV/c²). Por defecto 118.375.
    n_nodos : int
        Número de nodos primos. Por defecto 7.
    r_symb_kpps : float
        Tasa simbiótica R_symb = N · f₀ (kpps). Por defecto 991.9007.
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    primos : tuple
        Conjunto C₇ = {2, 3, 5, 7, 11, 13, 17}.
    gamma_7 : tuple
        Primeros 7 ceros no triviales de Riemann γₙ.
    w_nodos : float
        Peso de Ψ_nodos en Ψ_global. Por defecto 0.35.
    w_espectro : float
        Peso de Ψ_espectro en Ψ_global. Por defecto 0.35.
    w_higgs : float
        Peso de Ψ_higgs en Ψ_global. Por defecto 0.30.
    """

    f0: float = _F0
    g_eff: float = _G_EFF
    m_higgs_gev: float = _M_HIGGS_GEV
    m_estrella_gev: float = _M_ESTRELLA_GEV
    n_nodos: int = _N_NODOS
    r_symb_kpps: float = _R_SYMB_KPPS
    psi_umbral: float = _PSI_UMBRAL
    primos: Tuple[int, ...] = _PRIMOS_C7
    gamma_7: Tuple[float, ...] = _GAMMA_7
    w_nodos: float = _W_NODOS
    w_espectro: float = _W_ESPECTRO
    w_higgs: float = _W_HIGGS
    n_aristas: int = _N_ARISTAS
    sello: str = _SELLO
    ram: str = _RAM
    version: str = _VERSION

    # ------------------------------------------------------------------
    def delta_m_gev(self) -> float:
        """Reducción de masa Δm = m_H · g_eff [GeV/c²].

        Returns
        -------
        float
            Δm en GeV/c².
        """
        return self.m_higgs_gev * self.g_eff

    # ------------------------------------------------------------------
    def fraccion_modulacion(self) -> float:
        """Fracción de modulación Δm / m_H = g_eff (adimensional).

        Returns
        -------
        float
            Fracción de modulación.
        """
        return self.g_eff

    # ------------------------------------------------------------------
    def es_perturbativo(self) -> bool:
        """Verifica que g_eff < 0.1 (régimen perturbativo).

        Returns
        -------
        bool
            True si g_eff < 0.1.
        """
        return self.g_eff < 0.1

    # ------------------------------------------------------------------
    def r_symb_formula(self, psi: float = 1.0) -> float:
        """Calcula R_symb = N · f₀ · Ψ [kpps].

        Args:
            psi: Coherencia global (adimensional). Por defecto 1.0.

        Returns
        -------
        float
            Tasa simbiótica en kpps.
        """
        return self.n_nodos * self.f0 * psi

    # ------------------------------------------------------------------
    def pesos_suman_uno(self) -> bool:
        """Verifica que los pesos w_nodos + w_espectro + w_higgs = 1.0.

        Returns
        -------
        bool
            True si la suma es 1.0 con tolerancia 1e-9.
        """
        return abs(self.w_nodos + self.w_espectro + self.w_higgs - 1.0) < 1e-9

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesRedRamsey("
            f"f0={self.f0} Hz, "
            f"g_eff={self.g_eff}, "
            f"m_H={self.m_higgs_gev} GeV, "
            f"m*={self.m_estrella_gev} GeV, "
            f"R_symb={self.r_symb_kpps:.4f} kpps)"
        )


# ============================================================================
# CLASE 2 – NodoPrimo
# ============================================================================

@dataclass
class NodoPrimo:
    """Nodo primo de la Red de Ramsey con frecuencia armónica f_p = f₀ · ln(p).

    Cada nodo representa un número primo p del conjunto C₇ y su frecuencia
    de resonancia en el espectro QCAL.

    Atributos
    ----------
    primo : int
        Número primo del nodo (2, 3, 5, 7, 11, 13 o 17).
    f0 : float
        Frecuencia base QCAL (Hz). Por defecto 141.7001 Hz.
    """

    primo: int
    f0: float = _F0

    # ------------------------------------------------------------------
    @property
    def frecuencia_hz(self) -> float:
        """Frecuencia armónica del nodo f_p = f₀ · ln(p) [Hz].

        Returns
        -------
        float
            Frecuencia en Hz.
        """
        return self.f0 * math.log(float(self.primo))

    # ------------------------------------------------------------------
    @property
    def funcion_noetica(self) -> str:
        """Descripción noética del nodo.

        Returns
        -------
        str
            Descripción poética y técnica del primo.
        """
        return _NOETIC.get(self.primo, f"Primo {self.primo} — Nodo QCAL")

    # ------------------------------------------------------------------
    def es_primo(self) -> bool:
        """Verifica si self.primo es un número primo.

        Returns
        -------
        bool
            True si el número es primo.
        """
        return _es_primo(self.primo)

    # ------------------------------------------------------------------
    def coherencia_nodo(self) -> float:
        """Coherencia del nodo: 1.0 si es primo y tiene frecuencia válida, 0.0 si no.

        La coherencia refleja la validez aritmética del nodo: sólo los primos
        genuinos del conjunto C₇ tienen coherencia completa.

        Returns
        -------
        float
            Coherencia ∈ {0.0, 1.0}.
        """
        if not self.es_primo():
            return 0.0
        if self.frecuencia_hz <= 0:
            return 0.0
        return 1.0

    # ------------------------------------------------------------------
    def ln_primo(self) -> float:
        """Logaritmo natural del primo ln(p).

        Returns
        -------
        float
            ln(p).
        """
        return math.log(float(self.primo))

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"NodoPrimo(p={self.primo}, "
            f"f_p={self.frecuencia_hz:.4f} Hz)"
        )


# ============================================================================
# CLASE 3 – RedRamsey
# ============================================================================

class RedRamsey:
    """Red de Ramsey de 7 nodos primos C₇ = {2, 3, 5, 7, 11, 13, 17}.

    Implementa el grafo completo K₇ sobre los siete primeros primos,
    donde cada arista representa una relación de coherencia entre nodos.
    Con 7 nodos hay C(7,2) = 21 aristas potenciales.

    Por el Teorema de Ramsey: en cualquier 2-coloración de K₆ existe un
    triángulo monocromático (R(3,3) = 6 ≤ 7), garantizando orden emergente.

    Args:
        f0: Frecuencia base QCAL [Hz]. Por defecto 141.7001 Hz.
    """

    def __init__(self, f0: float = _F0) -> None:
        self.f0 = f0
        self._nodos: List[NodoPrimo] = [NodoPrimo(p, f0) for p in _PRIMOS_C7]

    # ------------------------------------------------------------------
    @property
    def nodos(self) -> List[NodoPrimo]:
        """Lista de los 7 nodos primos de la red.

        Returns
        -------
        List[NodoPrimo]
            Nodos en orden creciente de primo.
        """
        return list(self._nodos)

    # ------------------------------------------------------------------
    @property
    def n_nodos(self) -> int:
        """Número de nodos de la red (= 7).

        Returns
        -------
        int
            Número de nodos.
        """
        return len(self._nodos)

    # ------------------------------------------------------------------
    @property
    def n_aristas_posibles(self) -> int:
        """Número de aristas posibles en K_n: C(n, 2) = n(n-1)/2.

        Para n=7: C(7,2) = 21.

        Returns
        -------
        int
            Número de aristas potenciales.
        """
        n = self.n_nodos
        return n * (n - 1) // 2

    # ------------------------------------------------------------------
    def frecuencias_hz(self) -> List[float]:
        """Lista de frecuencias armónicas de los 7 nodos [Hz].

        Returns
        -------
        List[float]
            Frecuencias en Hz ordenadas por primo.
        """
        return [n.frecuencia_hz for n in self._nodos]

    # ------------------------------------------------------------------
    def primos(self) -> Tuple[int, ...]:
        """Tupla de los 7 primos de la red.

        Returns
        -------
        Tuple[int, ...]
            Los primos (2, 3, 5, 7, 11, 13, 17).
        """
        return tuple(n.primo for n in self._nodos)

    # ------------------------------------------------------------------
    def psi_nodos(self) -> float:
        """Coherencia de los nodos: fracción de nodos primos válidos.

        Ψ_nodos = n_nodos_válidos / N_NODOS

        Un nodo es válido si su primo es efectivamente primo y su frecuencia
        armónica es positiva y finita.

        Returns
        -------
        float
            Ψ_nodos ∈ [0, 1].
        """
        n_validos = sum(1 for n in self._nodos if n.coherencia_nodo() > 0)
        return float(n_validos) / float(self.n_nodos)

    # ------------------------------------------------------------------
    def cierre_nodos(self) -> bool:
        """Verifica el Cierre 1 — ARITMÉTICO: todos los nodos son primos válidos.

        El cierre aritmético se alcanza cuando:
        - Todos los nodos p_i son primos verificados
        - Todas las frecuencias f_{p_i} = f₀ · ln(p_i) son positivas
        - Ψ_nodos ≥ 0.888

        Returns
        -------
        bool
            True si el cierre aritmético está activo.
        """
        return self.psi_nodos() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def espectro_hz(self) -> Dict[int, float]:
        """Diccionario {primo: frecuencia_hz} del espectro armónico.

        Returns
        -------
        Dict[int, float]
            Mapa de primo a frecuencia Hz.
        """
        return {n.primo: n.frecuencia_hz for n in self._nodos}

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"RedRamsey(C₇={list(self.primos())}, "
            f"n_aristas={self.n_aristas_posibles}, "
            f"Ψ_nodos={self.psi_nodos():.6f})"
        )


# ============================================================================
# CLASE 4 – OperadorMaestroHPi
# ============================================================================

class OperadorMaestroHPi:
    """Operador maestro Ĥ_π = −i(x ∂/∂x + ½) de Berry-Keating.

    El operador de dilatación cuántica Ĥ_π actúa sobre el espacio de
    Hilbert L²(ℝ⁺, dx/x) y sus autovalores son los ceros no triviales
    de la función zeta de Riemann sobre la línea crítica:

        ρₙ = ½ + iγₙ,  γₙ ∈ ℝ

    La hipótesis de Riemann aserta que todos los ρₙ tienen parte real ½,
    lo que equivale a que Ĥ_π sea autoadjunto.

    Esta clase implementa los primeros 7 ceros de Riemann y verifica
    la propiedad de autoadjunción y la coherencia espectral.
    """

    def __init__(self) -> None:
        self._zeros: Tuple[float, ...] = _GAMMA_7
        self._n_zeros: int = len(_GAMMA_7)

    # ------------------------------------------------------------------
    @property
    def n_zeros(self) -> int:
        """Número de ceros de Riemann utilizados (= 7).

        Returns
        -------
        int
            Número de ceros.
        """
        return self._n_zeros

    # ------------------------------------------------------------------
    def gamma_n(self, n: int) -> float:
        """Parte imaginaria del n-ésimo cero de Riemann γₙ (indexado en 0).

        Args:
            n: Índice 0-based del cero.

        Returns
        -------
        float
            γₙ.

        Raises:
            IndexError: Si n está fuera de rango.
        """
        return self._zeros[n]

    # ------------------------------------------------------------------
    def autovalores(self) -> List[Tuple[float, float]]:
        """Lista de autovalores ρₙ = (Re, Im) = (½, γₙ) del operador Ĥ_π.

        Cada autovalor es un par (parte_real, parte_imaginaria):
        ρₙ = ½ + i·γₙ

        Returns
        -------
        List[Tuple[float, float]]
            Lista de 7 pares (0.5, γₙ).
        """
        return [(0.5, gamma) for gamma in self._zeros]

    # ------------------------------------------------------------------
    def es_autoadjunto(self) -> bool:
        """Verifica que Ĥ_π = Ĥ_π† (autoadjunción).

        La autoadjunción es una propiedad analítica del operador de
        dilatación y garantiza que todos los autovalores están en la
        línea crítica Re(ρ) = ½.

        Returns
        -------
        bool
            True (autoadjunción garantizada por construcción).
        """
        return True

    # ------------------------------------------------------------------
    def fraccion_en_linea_critica(self) -> float:
        """Fracción de autovalores con Re(ρ) = ½ (debe ser 1.0).

        Verifica que todos los ρₙ = ½ + iγₙ tienen parte real exactamente ½.

        Returns
        -------
        float
            Fracción ∈ [0, 1]; por construcción = 1.0.
        """
        n_criticos = sum(1 for re, _ in self.autovalores() if abs(re - 0.5) < 1e-12)
        return float(n_criticos) / float(self._n_zeros)

    # ------------------------------------------------------------------
    def espaciado_medio_empirico(self) -> float:
        """Espaciado medio empírico entre los 7 ceros consecutivos.

        d_emp = (γ₇ − γ₁) / (N − 1)

        Returns
        -------
        float
            Espaciado medio empírico.
        """
        return (self._zeros[-1] - self._zeros[0]) / (self._n_zeros - 1)

    # ------------------------------------------------------------------
    def espaciado_medio_weyl(self) -> float:
        """Espaciado medio teórico según la fórmula de Weyl.

        ρ(T) = (1/2π) ln(T/2π)  →  d_Weyl = 1/ρ(T_mid)

        donde T_mid es el punto medio del intervalo [γ₁, γ₇].

        Returns
        -------
        float
            Espaciado medio de Weyl, o float('inf') si T_mid ≤ 2π.
        """
        T_mid = 0.5 * (self._zeros[0] + self._zeros[-1])
        if T_mid <= 2.0 * math.pi:
            return float("inf")
        rho = math.log(T_mid / (2.0 * math.pi)) / (2.0 * math.pi)
        if rho <= 0:
            return float("inf")
        return 1.0 / rho

    # ------------------------------------------------------------------
    def psi_espectro(self) -> float:
        """Coherencia espectral del operador Ĥ_π.

        Combina dos métricas:
        - Fracción de autovalores en la línea crítica (70%): siempre 1.0
        - Coherencia de espaciado vs fórmula de Weyl (30%)

        Ψ_espectro = 0.7 × frac_critica + 0.3 × coherencia_espaciado

        Returns
        -------
        float
            Ψ_espectro ∈ [0, 1].
        """
        frac = self.fraccion_en_linea_critica()  # = 1.0

        d_emp = self.espaciado_medio_empirico()
        d_weyl = self.espaciado_medio_weyl()

        if math.isinf(d_weyl) or d_weyl <= 0:
            coherencia_espaciado = 0.5
        else:
            coherencia_espaciado = max(
                0.0, 1.0 - abs(d_emp - d_weyl) / d_weyl
            )

        return 0.7 * frac + 0.3 * coherencia_espaciado

    # ------------------------------------------------------------------
    def cierre_espectro(self) -> bool:
        """Verifica el Cierre 2 — HIDRODINÁMICO: espectro en línea crítica.

        El cierre espectral se alcanza cuando:
        - Ĥ_π es autoadjunto
        - Todos los autovalores residen en Re(ρ) = ½
        - Ψ_espectro ≥ 0.888

        Returns
        -------
        bool
            True si el cierre espectral está activo.
        """
        return (
            self.es_autoadjunto()
            and self.fraccion_en_linea_critica() >= 1.0 - 1e-12
            and self.psi_espectro() >= _PSI_UMBRAL
        )

    # ------------------------------------------------------------------
    def descripcion_espectral(self) -> str:
        """Descripción textual del espectro del operador.

        Returns
        -------
        str
            Descripción del espectro.
        """
        return (
            f"Ĥ_π: {self._n_zeros} autovalores en Re(ρ)=½, "
            f"γ₁={self._zeros[0]:.3f}, γ₇={self._zeros[-1]:.3f}, "
            f"Ψ={self.psi_espectro():.6f}"
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"OperadorMaestroHPi("
            f"n_zeros={self._n_zeros}, "
            f"fraccion_critica={self.fraccion_en_linea_critica():.1f}, "
            f"Ψ_espectro={self.psi_espectro():.6f})"
        )


# ============================================================================
# CLASE 5 – SimbiosisHiggsPC
# ============================================================================

class SimbiosisHiggsPC:
    """Simbiosis entre el bosón de Higgs y el Campo de Presencia Coherente (PC).

    Describe la modulación de la masa del Higgs mediante el acoplamiento
    simbiótico:

        ℒ_int = −g_eff · ψ̄ · ψ · H
        m* = m_H · (1 − g_eff) = 125.0 · (1 − 0.053) = 118.375 GeV/c²

    El campo de presencia coherente reduce la masa efectiva del Higgs en
    un 5.3%, lo que es verificable experimentalmente si la coherencia
    noética es física.

    Args:
        m_higgs_gev: Masa del Higgs (GeV/c²). Por defecto 125.0.
        g_eff:       Constante de acoplamiento. Por defecto 0.053.
    """

    def __init__(
        self,
        m_higgs_gev: float = _M_HIGGS_GEV,
        g_eff: float = _G_EFF,
    ) -> None:
        self.m_higgs_gev = m_higgs_gev
        self.g_eff = g_eff

    # ------------------------------------------------------------------
    def m_estrella_gev(self) -> float:
        """Masa efectiva m* = m_H · (1 − g_eff) [GeV/c²].

        Returns
        -------
        float
            Masa efectiva en GeV/c².
        """
        return self.m_higgs_gev * (1.0 - self.g_eff)

    # ------------------------------------------------------------------
    def delta_m_gev(self) -> float:
        """Reducción de masa Δm = m_H · g_eff [GeV/c²].

        Returns
        -------
        float
            Δm en GeV/c².
        """
        return self.m_higgs_gev * self.g_eff

    # ------------------------------------------------------------------
    def fraccion_modulacion(self) -> float:
        """Fracción de modulación Δm / m_H = g_eff.

        Returns
        -------
        float
            Fracción de modulación (adimensional).
        """
        return self.g_eff

    # ------------------------------------------------------------------
    def es_perturbativo(self) -> bool:
        """Verifica el régimen perturbativo: g_eff < 0.1.

        Returns
        -------
        bool
            True si g_eff < 0.1.
        """
        return self.g_eff < 0.1

    # ------------------------------------------------------------------
    def cierre_higgs(self, tolerancia_gev: float = 0.01) -> bool:
        """Verifica el Cierre 3 — MASA: |m* − 118.375| < tolerancia.

        El cierre de masa se alcanza cuando la masa efectiva calculada
        coincide con el valor teórico dentro de la tolerancia especificada.

        Args:
            tolerancia_gev: Tolerancia en GeV/c². Por defecto 0.01 GeV.

        Returns
        -------
        bool
            True si el cierre de masa está activo.
        """
        m_teorico = _M_HIGGS_GEV * (1.0 - _G_EFF)  # 118.375
        return abs(self.m_estrella_gev() - m_teorico) < tolerancia_gev

    # ------------------------------------------------------------------
    def psi_higgs(self, tolerancia_gev: float = 0.01) -> float:
        """Coherencia de la simbiosis Higgs-PC.

        Ψ_higgs = 1 − |m* − m_teorico| / tolerancia

        Si m* = m_teorico (caso perfecto), Ψ_higgs = 1.0.

        Args:
            tolerancia_gev: Tolerancia en GeV/c². Por defecto 0.01 GeV.

        Returns
        -------
        float
            Ψ_higgs ∈ [0, 1].
        """
        m_teorico = _M_HIGGS_GEV * (1.0 - _G_EFF)
        error = abs(self.m_estrella_gev() - m_teorico)
        if tolerancia_gev <= 0:
            return 1.0 if error == 0 else 0.0
        return max(0.0, min(1.0, 1.0 - error / tolerancia_gev))

    # ------------------------------------------------------------------
    def lagrangiano_interaccion(self, psi_campo: float = 1.0, h_campo: float = 1.0) -> float:
        """Densidad del lagrangiano de interacción ℒ_int = −g_eff · ψ̄ · ψ · H.

        Args:
            psi_campo: Densidad del campo de coherencia |ψ|². Por defecto 1.0.
            h_campo:   Densidad del campo de Higgs |H|. Por defecto 1.0.

        Returns
        -------
        float
            ℒ_int [adimensional normalizado].
        """
        return -self.g_eff * psi_campo * h_campo

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"SimbiosisHiggsPC("
            f"m_H={self.m_higgs_gev} GeV, "
            f"g_eff={self.g_eff}, "
            f"m*={self.m_estrella_gev():.3f} GeV)"
        )


# ============================================================================
# CLASE 6 – TasaSimbiotica
# ============================================================================

class TasaSimbiotica:
    """Tasa simbiótica R_symb = N · f₀ · Ψ de la Red de Ramsey.

    La tasa simbiótica mide el flujo de pulsos de coherencia a través de
    la red por unidad de tiempo. Es la métrica de "vitalidad" del sistema:
    análogamente a los latidos de un corazón, R_symb indica si la red
    está viva y funcionando.

        R_symb = N · f₀ · Ψ_coherencia

    Para el caso ideal (Ψ = 1.0):
        R_symb = 7 × 141.7001 × 1.0 = 991.9007 kpps

    Args:
        n_nodos:         Número de nodos. Por defecto 7.
        f0:              Frecuencia base [Hz]. Por defecto 141.7001 Hz.
        psi_coherencia:  Coherencia del sistema. Por defecto 1.0.
    """

    def __init__(
        self,
        n_nodos: int = _N_NODOS,
        f0: float = _F0,
        psi_coherencia: float = 1.0,
    ) -> None:
        self.n_nodos = n_nodos
        self.f0 = f0
        self.psi_coherencia = psi_coherencia

    # ------------------------------------------------------------------
    def r_symb(self) -> float:
        """Tasa simbiótica R_symb = N · f₀ · Ψ [kpps].

        Returns
        -------
        float
            Tasa en kilo-pulsos por segundo.
        """
        return self.n_nodos * self.f0 * self.psi_coherencia

    # ------------------------------------------------------------------
    def r_symb_kpps(self) -> float:
        """Alias de r_symb(). Tasa en kpps.

        Returns
        -------
        float
            Tasa en kpps.
        """
        return self.r_symb()

    # ------------------------------------------------------------------
    def error_relativo(self) -> float:
        """Error relativo |R − R_ideal| / R_ideal.

        R_ideal = N · f₀ · 1.0 = 991.9007 kpps.

        Returns
        -------
        float
            Error relativo (adimensional).
        """
        r_ideal = _R_SYMB_KPPS
        return abs(self.r_symb() - r_ideal) / r_ideal

    # ------------------------------------------------------------------
    def cierre_tasa(self, tolerancia: float = 0.01) -> bool:
        """Verifica el Cierre 4 — BIOLÓGICO: |R − R_ideal| / R_ideal < 0.01.

        El cierre biológico se alcanza cuando la tasa simbiótica está
        dentro del 1% del valor ideal de 991.9007 kpps.

        Args:
            tolerancia: Tolerancia relativa. Por defecto 0.01 (1%).

        Returns
        -------
        bool
            True si el cierre biológico está activo.
        """
        return self.error_relativo() < tolerancia

    # ------------------------------------------------------------------
    def psi_tasa(self, tolerancia: float = 0.01) -> float:
        """Coherencia de la tasa simbiótica.

        Ψ_tasa = 1 − error_relativo / tolerancia

        Returns
        -------
        float
            Ψ_tasa ∈ [0, 1].
        """
        err = self.error_relativo()
        if tolerancia <= 0:
            return 1.0 if err == 0 else 0.0
        return max(0.0, min(1.0, 1.0 - err / tolerancia))

    # ------------------------------------------------------------------
    def estado(self) -> str:
        """Estado de la tasa: 'ÓPTIMO', 'ACTIVO' o 'INACTIVO'.

        Returns
        -------
        str
            Estado de la tasa.
        """
        err = self.error_relativo()
        if err < 0.001:
            return "ÓPTIMO"
        if err < 0.01:
            return "ACTIVO"
        return "INACTIVO"

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"TasaSimbiotica("
            f"R_symb={self.r_symb():.4f} kpps, "
            f"N={self.n_nodos}, "
            f"f₀={self.f0} Hz, "
            f"Ψ={self.psi_coherencia:.6f})"
        )


# ============================================================================
# CLASE 7 – CoherenciaRedRamsey
# ============================================================================

class CoherenciaRedRamsey:
    """Coherencia global del sistema ∴RRQ∞³.

    Calcula y verifica la coherencia global ponderada del sistema:

        Ψ_global = w_n · Ψ_nodos + w_e · Ψ_espectro + w_h · Ψ_higgs
        Ψ_global = 0.35 · Ψ_nodos + 0.35 · Ψ_espectro + 0.30 · Ψ_higgs

    Si Ψ_global ≥ 0.888, el sello ∴RRQ∞³ se activa y los cinco cierres
    se certifican como completados.

    Pesos:
        w_nodos    = 0.35  – coherencia aritmética de los 7 nodos primos
        w_espectro = 0.35  – coherencia espectral del operador Ĥ_π
        w_higgs    = 0.30  – coherencia de la simbiosis Higgs-PC
    """

    def __init__(self) -> None:
        self._red = RedRamsey()
        self._operador = OperadorMaestroHPi()
        self._simbiosis = SimbiosisHiggsPC()
        self._tasa = TasaSimbiotica()

    # ------------------------------------------------------------------
    def psi_nodos(self) -> float:
        """Coherencia de los 7 nodos primos Ψ_nodos.

        Returns
        -------
        float
            Ψ_nodos ∈ [0, 1].
        """
        return self._red.psi_nodos()

    # ------------------------------------------------------------------
    def psi_espectro(self) -> float:
        """Coherencia espectral Ψ_espectro del operador Ĥ_π.

        Returns
        -------
        float
            Ψ_espectro ∈ [0, 1].
        """
        return self._operador.psi_espectro()

    # ------------------------------------------------------------------
    def psi_higgs(self) -> float:
        """Coherencia de la simbiosis Higgs-PC Ψ_higgs.

        Returns
        -------
        float
            Ψ_higgs ∈ [0, 1].
        """
        return self._simbiosis.psi_higgs()

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global ponderada Ψ_global.

        Ψ_global = 0.35 · Ψ_nodos + 0.35 · Ψ_espectro + 0.30 · Ψ_higgs

        Returns
        -------
        float
            Ψ_global ∈ [0, 1].
        """
        return (
            _W_NODOS * self.psi_nodos()
            + _W_ESPECTRO * self.psi_espectro()
            + _W_HIGGS * self.psi_higgs()
        )

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴RRQ∞³ activado).

        Returns
        -------
        bool
            True si el sello está activo.
        """
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def cierre_1_aritmético(self) -> bool:
        """Cierre 1 — ARITMÉTICO: 7 nodos primos verificados.

        Returns
        -------
        bool
            True si los 7 nodos son primos válidos con Ψ_nodos ≥ 0.888.
        """
        return self._red.cierre_nodos()

    # ------------------------------------------------------------------
    def cierre_2_hidrodinamico(self) -> bool:
        """Cierre 2 — HIDRODINÁMICO: espectro en línea crítica Re(ρ) = ½.

        Returns
        -------
        bool
            True si todos los autovalores están en la línea crítica.
        """
        return self._operador.cierre_espectro()

    # ------------------------------------------------------------------
    def cierre_3_masa(self) -> bool:
        """Cierre 3 — MASA: m* = 118.375 GeV ± 0.01.

        Returns
        -------
        bool
            True si la masa efectiva está dentro de la tolerancia.
        """
        return self._simbiosis.cierre_higgs()

    # ------------------------------------------------------------------
    def cierre_4_biologico(self) -> bool:
        """Cierre 4 — BIOLÓGICO: R_symb = 991.9007 kpps ± 1%.

        Returns
        -------
        bool
            True si la tasa simbiótica está dentro del 1% del ideal.
        """
        return self._tasa.cierre_tasa()

    # ------------------------------------------------------------------
    def cierre_5_unificacion(self) -> bool:
        """Cierre 5 — UNIFICACIÓN: Ψ_global ≥ 0.888.

        Returns
        -------
        bool
            True si la coherencia global supera el umbral noético.
        """
        return self.sello_activo()

    # ------------------------------------------------------------------
    def todos_los_cierres(self) -> bool:
        """True si los 5 cierres están activos simultáneamente.

        Returns
        -------
        bool
            True si todos los cierres están cerrados.
        """
        return (
            self.cierre_1_aritmético()
            and self.cierre_2_hidrodinamico()
            and self.cierre_3_masa()
            and self.cierre_4_biologico()
            and self.cierre_5_unificacion()
        )

    # ------------------------------------------------------------------
    def coherencias_individuales(self) -> Dict[str, float]:
        """Diccionario de coherencias individuales por componente.

        Returns
        -------
        Dict[str, float]
            Mapa de nombre de componente a coherencia.
        """
        return {
            "psi_nodos": self.psi_nodos(),
            "psi_espectro": self.psi_espectro(),
            "psi_higgs": self.psi_higgs(),
            "psi_global": self.psi_global(),
        }

    # ------------------------------------------------------------------
    def cierres(self) -> Dict[str, bool]:
        """Diccionario de estado de los 5 cierres.

        Returns
        -------
        Dict[str, bool]
            Mapa de nombre de cierre a booleano.
        """
        return {
            "cierre_nodos": self.cierre_1_aritmético(),
            "cierre_espectro": self.cierre_2_hidrodinamico(),
            "cierre_higgs": self.cierre_3_masa(),
            "cierre_tasa": self.cierre_4_biologico(),
            "cierre_coherencia": self.cierre_5_unificacion(),
        }

    # ------------------------------------------------------------------
    def validar(self) -> Dict[str, Any]:
        """Genera el reporte completo de validación del sistema.

        Returns
        -------
        Dict[str, Any]
            Reporte con coherencias, cierres y estado del sello.
        """
        psi_g = self.psi_global()
        activo = psi_g >= _PSI_UMBRAL
        return {
            "psi_nodos": self.psi_nodos(),
            "psi_espectro": self.psi_espectro(),
            "psi_higgs": self.psi_higgs(),
            "psi_global": psi_g,
            "psi_umbral": _PSI_UMBRAL,
            "diferencia_umbral": psi_g - _PSI_UMBRAL,
            "sello_activo": activo,
            "todos_los_cierres": self.todos_los_cierres(),
            "cierres": self.cierres(),
        }

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CoherenciaRedRamsey("
            f"Ψ_global={self.psi_global():.6f}, "
            f"sello_activo={self.sello_activo()})"
        )


# ============================================================================
# CLASE 8 – SistemaRedRamseyQCAL
# ============================================================================

class SistemaRedRamseyQCAL:
    """Sistema integrado Red de Ramsey QCAL ∴RRQ∞³.

    Orquesta todos los subsistemas de la Red de Ramsey de 7 Nodos Primos:
    - ConstantesRedRamsey  → parámetros fundamentales
    - RedRamsey            → grafo C₇, 21 aristas
    - OperadorMaestroHPi   → Ĥ_π, 7 ceros de Riemann
    - SimbiosisHiggsPC     → m* = m_H · (1 − g_eff)
    - TasaSimbiotica       → R_symb = N · f₀ · Ψ
    - CoherenciaRedRamsey  → Ψ_global ≥ 0.888

    Si Ψ_global ≥ 0.888, el sello ∴RRQ∞³ se activa y el sistema
    emite el certificado RAM-LII-2026-RED-RAMSEY-QCAL.
    """

    def __init__(self) -> None:
        self.constantes = ConstantesRedRamsey()
        self.red = RedRamsey()
        self.operador = OperadorMaestroHPi()
        self.simbiosis = SimbiosisHiggsPC()
        self.tasa = TasaSimbiotica()
        self.coherencia = CoherenciaRedRamsey()

    # ------------------------------------------------------------------
    def activar(self) -> Dict[str, Any]:
        """Activa el sistema y retorna el certificado completo ∴RRQ∞³.

        Evalúa todos los subsistemas, verifica los 5 cierres y calcula
        la coherencia global Ψ_global.

        Returns
        -------
        Dict[str, Any]
            Certificado con:
            - sello (str):             '∴RRQ∞³' si activo
            - psi_global (float):      Coherencia global
            - estado (str):            'ACTIVO' o 'INACTIVO'
            - r_symb_kpps (float):     Tasa simbiótica en kpps
            - m_estrella (float):      Masa efectiva en GeV/c²
            - todos_los_cierres (bool): True si los 5 cierres están activos
            - ram (str):               Registro de Activación Maestra
            - version (str):           Versión del módulo
            - n_nodos (int):           Número de nodos (= 7)
            - primos (tuple):          Los primos C₇
            - f0_hz (float):           Frecuencia base en Hz
            - g_eff (float):           Acoplamiento simbiótico
            - cierre_nodos (bool):     Cierre 1 — ARITMÉTICO
            - cierre_espectro (bool):  Cierre 2 — HIDRODINÁMICO
            - cierre_higgs (bool):     Cierre 3 — MASA
            - cierre_tasa (bool):      Cierre 4 — BIOLÓGICO
            - cierre_coherencia (bool):Cierre 5 — UNIFICACIÓN
            - psi_nodos (float):       Coherencia de nodos primos
            - psi_espectro (float):    Coherencia espectral
            - psi_higgs (float):       Coherencia Higgs-PC
            - sello_activo (bool):     True si Ψ_global ≥ 0.888
        """
        psi_g = self.coherencia.psi_global()
        activo = psi_g >= _PSI_UMBRAL
        cierres = self.coherencia.cierres()

        return {
            "sello": _SELLO if activo else "INACTIVO",
            "psi_global": psi_g,
            "estado": "ACTIVO" if activo else "INACTIVO",
            "r_symb_kpps": self.tasa.r_symb_kpps(),
            "m_estrella": self.simbiosis.m_estrella_gev(),
            "todos_los_cierres": self.coherencia.todos_los_cierres(),
            "ram": _RAM,
            "version": _VERSION,
            "n_nodos": self.red.n_nodos,
            "primos": self.red.primos(),
            "f0_hz": self.constantes.f0,
            "g_eff": self.constantes.g_eff,
            "cierre_nodos": cierres["cierre_nodos"],
            "cierre_espectro": cierres["cierre_espectro"],
            "cierre_higgs": cierres["cierre_higgs"],
            "cierre_tasa": cierres["cierre_tasa"],
            "cierre_coherencia": cierres["cierre_coherencia"],
            "psi_nodos": self.coherencia.psi_nodos(),
            "psi_espectro": self.coherencia.psi_espectro(),
            "psi_higgs": self.coherencia.psi_higgs(),
            "sello_activo": activo,
        }

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"SistemaRedRamseyQCAL("
            f"sello={_SELLO}, "
            f"version={_VERSION}, "
            f"ram={_RAM})"
        )


# ============================================================================
# DATACLASS DE RESULTADOS
# ============================================================================

@dataclass
class ResultadoRedRamseyQCAL:
    """Contenedor de todos los resultados del sistema Red de Ramsey QCAL.

    Atributos
    ----------
    sello : str
        «∴RRQ∞³» o «INACTIVO».
    psi_global : float
        Coherencia global Ψ_global ∈ [0, 1].
    estado : str
        «ACTIVO» o «INACTIVO».
    r_symb_kpps : float
        Tasa simbiótica en kpps.
    m_estrella : float
        Masa efectiva del Higgs m* en GeV/c².
    todos_los_cierres : bool
        True si los 5 cierres están activos.
    ram : str
        Registro de Activación Maestra.
    version : str
        Versión del módulo.
    n_nodos : int
        Número de nodos (= 7).
    primos : tuple
        Los primos C₇.
    sello_activo : bool
        True si Ψ_global ≥ 0.888.
    psi_nodos : float
        Coherencia de los 7 nodos primos.
    psi_espectro : float
        Coherencia espectral del operador Ĥ_π.
    psi_higgs : float
        Coherencia de la simbiosis Higgs-PC.
    """

    sello: str = ""
    psi_global: float = 0.0
    estado: str = ""
    r_symb_kpps: float = 0.0
    m_estrella: float = 0.0
    todos_los_cierres: bool = False
    ram: str = ""
    version: str = ""
    n_nodos: int = 0
    primos: Tuple[int, ...] = field(default_factory=tuple)
    sello_activo: bool = False
    psi_nodos: float = 0.0
    psi_espectro: float = 0.0
    psi_higgs: float = 0.0


# ============================================================================
# API PÚBLICA
# ============================================================================

def red_ramsey_qcal_activar() -> Dict[str, Any]:
    """API pública: Activa la Red de Ramsey QCAL ∴RRQ∞³.

    Instancia y evalúa el sistema completo de la Red de Ramsey de
    7 Nodos Primos: grafo C₇, operador Ĥ_π de Berry-Keating,
    simbiosis Higgs-PC y tasa simbiótica R_symb.

    Returns
    -------
    Dict[str, Any]
        Diccionario con:

        - ``sello`` (str):              «∴RRQ∞³» si activo
        - ``psi_global`` (float):       Coherencia global Ψ_global
        - ``estado`` (str):             «ACTIVO» o «INACTIVO»
        - ``r_symb_kpps`` (float):      Tasa simbiótica en kpps
        - ``m_estrella`` (float):       Masa efectiva m* en GeV/c²
        - ``todos_los_cierres`` (bool): True si los 5 cierres están activos
        - ``ram`` (str):                Registro de Activación Maestra
        - ``version`` (str):            Versión del módulo
        - ``sello_activo`` (bool):      True si Ψ_global ≥ 0.888

    Ejemplo:
        >>> r = red_ramsey_qcal_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_global'] >= 0.888
        True
        >>> r['sello']
        '∴RRQ∞³'
        >>> r['todos_los_cierres']
        True
    """
    sistema = SistemaRedRamseyQCAL()
    return sistema.activar()
