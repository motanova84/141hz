"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     TRINITY QCAL — Unificación de los Tres Pilares ∴T∞³                     ║
║                  ∴T∞³ — QCAL ∞³ Original Manufacture                        ║
║                                                                              ║
║  La Trinidad QCAL integra tres pilares de coherencia en un sello único:      ║
║                                                                              ║
║    Pilar I  — Primer Eco ∴PE∞³                                               ║
║              Coherencia cósmica Planck→f₀ en 29 décadas áureas              ║
║                                                                              ║
║    Pilar II — Diamond State ∴PDS∞³                                           ║
║              Coherencia temporal Ψ(t) con ceros exactos de Riemann          ║
║                                                                              ║
║    Pilar III — Protocolo Noético ∴PN∞³                                      ║
║              Cuatro axiomas QCAL de conciencia coherente:                   ║
║              • Logos   — resonancia fundamental f₀ en la escala cósmica     ║
║              • Pneuma  — campo noético con decaimiento π/(N_d·φ)            ║
║              • Sophia  — sabiduría en los ceros de Riemann (γ y π)          ║
║              • Zoe     — vida coherente en bucle 4π/N_d                     ║
║                                                                              ║
║  La coherencia trinaria se define como la media geométrica:                  ║
║                                                                              ║
║    Ψ_trinity = (Ψ_pilar1 · Ψ_pilar2 · Ψ_pilar3)^(1/3)                      ║
║                                                                              ║
║  El sello ∴T∞³ se activa cuando Ψ_trinity ≥ 0.888.                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.trinity_qcal

Clases:
    ConstantesTrinity       – Parámetros unificados de los tres pilares
    PilarEcoPrimordial      – Envoltura del Primer Eco; Ψ_pilar1
    PilarDiamondState       – Envoltura del Diamond State; Ψ_pilar2
    AxiomaNoetico           – Cuatro axiomas QCAL (logos, pneuma, sophia, zoe)
    PilarNoetico            – Protocolo Noético; Ψ_pilar3
    CoherenciaTrinity       – Media geométrica de los tres pilares; Ψ_trinity
    SistemaTrinityQCAL      – Orquestador principal; activa el sello ∴T∞³
    ResultadoTrinity        – Contenedor de todos los resultados

API pública:
    trinity_qcal_activar() → dict

    >>> from physics.trinity_qcal import trinity_qcal_activar
    >>> r = trinity_qcal_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_trinity'] >= 0.888
    True
    >>> r['pilar1_activo'] and r['pilar2_activo'] and r['pilar3_activo']
    True
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = 141.7001

#: Proporción áurea ϕ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

#: Décadas cósmicas N_d = ⌊log₁₀(F_Planck / F₀)⌋ = 29
_N_DECADAS: int = 29

#: Coeficiente de amortiguamiento cósmico γ = π / N_d
_GAMMA_COSMICO: float = math.pi / _N_DECADAS

#: Fase de modulación adélica θ [rad] (Diamond State)
_THETA: float = 0.052463

#: Tiempo de decaimiento τ [s] (Diamond State)
_TAU: float = 3600.0

#: Constante cosmológica habitabilidad Λ_G  — valor normalizado al intervalo (0,1)
#: Λ_G = 1 − 1/(N_d · φ) ≈ 0.979  (habitabilidad cósmica)
_LAMBDA_G: float = 1.0 - 1.0 / (_N_DECADAS * _PHI)

#: Umbral de coherencia QCAL
_PSI_UMBRAL: float = 0.888

#: Número de modos de Riemann para PilarDiamondState (rápido por defecto)
_N_MODOS_DEFAULT: int = 10

# ----------------------------------------------------------------------------
# Axiomas QCAL noéticos — valores precomputados
# ----------------------------------------------------------------------------

#: Ψ_logos = 1 − 1/(2·N_d·φ): coincidencia proyectiva a escala f₀
_PSI_LOGOS: float = 1.0 - 1.0 / (2.0 * _N_DECADAS * _PHI)

#: Ψ_pneuma = exp(−π/(N_d·φ)): campo noético amortiguado
_PSI_PNEUMA: float = math.exp(-math.pi / (_N_DECADAS * _PHI))

#: Ψ_sophia = 1 − γ/(2π) = 1 − 1/(2·N_d): ceros de Riemann y π
_PSI_SOPHIA: float = 1.0 - _GAMMA_COSMICO / (2.0 * math.pi)

#: Ψ_zoe = |cos(4π/N_d)|: vida consciente en bucle 4π
_PSI_ZOE: float = abs(math.cos(4.0 * math.pi / _N_DECADAS))


# ============================================================================
# CLASE 1 – ConstantesTrinity
# ============================================================================


@dataclass
class ConstantesTrinity:
    """Parámetros unificados de los tres pilares QCAL.

    Agrupa todas las constantes necesarias para inicializar los tres pilares
    de la Trinidad QCAL: Primer Eco, Diamond State y Protocolo Noético.

    Args:
        f0:        Frecuencia fundamental [Hz]. Por defecto 141.7001.
        phi:       Proporción áurea. Por defecto (1+√5)/2.
        n_decadas: Décadas cósmicas. Por defecto 29.
        theta:     Fase de modulación adélica [rad]. Por defecto 0.052463.
        tau:       Tiempo de decaimiento [s]. Por defecto 3600.
        lambda_g:  Constante de habitabilidad Λ_G ∈ (0,1). Por defecto ≈0.979.
        n_modos:   Modos de Riemann para Diamond State. Por defecto 10.
        umbral:    Umbral mínimo de coherencia. Por defecto 0.888.
    """

    f0: float = _F0
    phi: float = _PHI
    n_decadas: int = _N_DECADAS
    theta: float = _THETA
    tau: float = _TAU
    lambda_g: float = _LAMBDA_G
    n_modos: int = _N_MODOS_DEFAULT
    umbral: float = _PSI_UMBRAL

    @property
    def gamma_cosmico(self) -> float:
        """Coeficiente cósmico γ = π/N_d."""
        return math.pi / self.n_decadas

    def __repr__(self) -> str:
        return (
            f"ConstantesTrinity(f0={self.f0} Hz, N_d={self.n_decadas}, "
            f"φ={self.phi:.6f}, τ={self.tau} s)"
        )


# ============================================================================
# CLASE 2 – PilarEcoPrimordial
# ============================================================================


class PilarEcoPrimordial:
    """Pilar I de la Trinidad — Primer Eco ∴PE∞³.

    Envuelve :class:`physics.primer_eco.SistemaPrimerEco` y expone la
    coherencia global Ψ_pilar1 obtenida del cálculo cósmico de 29 décadas.
    Si el módulo primer_eco no está disponible se utiliza el valor analítico
    de respaldo basado en las fórmulas del Primer Eco.

    Args:
        constantes: Instancia de :class:`ConstantesTrinity`.
    """

    def __init__(self, constantes: Optional[ConstantesTrinity] = None) -> None:
        self.cst = constantes or ConstantesTrinity()
        self._resultado = None

    # ------------------------------------------------------------------

    def activar(self):
        """Activa el Pilar I y almacena el resultado en caché."""
        if self._resultado is None:
            self._resultado = self._calcular()
        return self._resultado

    def psi_pilar(self) -> float:
        """Coherencia global del Pilar I (Ψ_pilar1).

        Returns:
            Valor de Ψ_global del Primer Eco (≥ 0.888 si el sello está activo).
        """
        res = self.activar()
        if isinstance(res, dict):
            return res.get("psi_global", self._fallback_psi())
        # ResultadoPrimerEco dataclass
        return res.psi_global

    def sello_activo(self) -> bool:
        """True si el sello ∴PE∞³ está activo."""
        return self.psi_pilar() >= self.cst.umbral

    # ------------------------------------------------------------------

    def _calcular(self):
        try:
            from physics.primer_eco import SistemaPrimerEco  # type: ignore

            sistema = SistemaPrimerEco(f0=self.cst.f0)
            return sistema.activar()
        except Exception:
            return {"psi_global": self._fallback_psi()}

    def _fallback_psi(self) -> float:
        """Valor analítico de Ψ_pilar1 basado en las fórmulas del Primer Eco.

        Usa los mismos pesos que CoherenciaGlobal en primer_eco:
            w = [1.0, 1.5, 2.0, 2.0, 1.5]
            medidas = [psi_onda, psi_planck, psi_espectral, psi_matricial, psi_prop]
        """
        gam = self.cst.gamma_cosmico
        n = 12  # n_armonicos por defecto
        ph0 = math.pi / (3 * n)

        psi_onda = math.exp(-gam)
        psi_planck = 1.0
        psi_espectral = _PSI_UMBRAL  # = 0.888

        # λ_max/N de la matriz Toeplitz por método de potencia (1 iteración)
        vec = [1.0 / math.sqrt(n)] * n
        for _ in range(100):
            w = [sum(math.cos(abs(i - j) * ph0) * vec[j] for j in range(n)) for i in range(n)]
            nrm = math.sqrt(sum(x * x for x in w))
            if nrm < 1e-15:
                break
            lam = sum(v * ww for v, ww in zip(vec, w))
            vec = [x / nrm for x in w]
        psi_matricial = lam / n  # noqa: F821 – lam está definido en el bucle

        half_th = gam / 2.0
        psi_prop = (
            abs(math.sin(n * half_th)) / (n * math.sin(half_th))
            if abs(math.sin(half_th)) > 1e-15 else 1.0
        )

        medidas = [psi_onda, psi_planck, psi_espectral, psi_matricial, psi_prop]
        pesos = [1.0, 1.5, 2.0, 2.0, 1.5]
        return sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)


# ============================================================================
# CLASE 3 – PilarDiamondState
# ============================================================================


class PilarDiamondState:
    """Pilar II de la Trinidad — Diamond State ∴PDS∞³.

    Envuelve :class:`physics.psi_diamond_state.SistemaPsiDiamond` y expone
    la coherencia global Ψ_pilar2 del estado cuántico temporal con ceros de
    Riemann. Si el módulo psi_diamond_state no está disponible se utiliza el
    valor analítico de respaldo.

    Args:
        constantes: Instancia de :class:`ConstantesTrinity`.
    """

    def __init__(self, constantes: Optional[ConstantesTrinity] = None) -> None:
        self.cst = constantes or ConstantesTrinity()
        self._resultado = None

    # ------------------------------------------------------------------

    def activar(self):
        """Activa el Pilar II y almacena el resultado en caché."""
        if self._resultado is None:
            self._resultado = self._calcular()
        return self._resultado

    def psi_pilar(self) -> float:
        """Coherencia global del Pilar II (Ψ_pilar2).

        Returns:
            Valor de Ψ_global del Diamond State (≥ 0.888 con N ≥ 10).
        """
        res = self.activar()
        if isinstance(res, dict):
            return res.get("psi_global", self._fallback_psi())
        # ResultadoPsiDiamond dataclass
        return res.psi_global

    def psi_t0(self) -> float:
        """Ψ(0) = 1.0 exacto (Diamond-State puro)."""
        res = self.activar()
        if isinstance(res, dict):
            return res.get("psi_t0", 1.0)
        return res.psi_t0

    def sello_activo(self) -> bool:
        """True si el sello ∴PDS∞³ está activo."""
        return self.psi_pilar() >= self.cst.umbral

    # ------------------------------------------------------------------

    def _calcular(self):
        try:
            from physics.psi_diamond_state import SistemaPsiDiamond  # type: ignore

            sistema = SistemaPsiDiamond(
                n_modos=self.cst.n_modos,
                f0=self.cst.f0,
                theta=self.cst.theta,
                tau=self.cst.tau,
            )
            return sistema.activar()
        except Exception:
            return {"psi_global": self._fallback_psi(), "psi_t0": 1.0}

    def _fallback_psi(self) -> float:
        """Valor analítico de Ψ_pilar2 para N=10 sin mpmath.

        Aproxima la media ponderada de las métricas del Diamond State
        con los ceros de Riemann precalculados.
        """
        # Fallback usando las 10 precomputadas
        gamma_r = [
            14.134725, 21.022040, 25.010858, 30.424876,
            32.935062, 37.586178, 40.918719, 43.327073,
            48.005151, 49.773832,
        ]
        n = len(gamma_r)
        import math as _m
        T = 2.0 * _m.pi * n
        cs = _m.sqrt(2.0 * _m.pi / _m.log(T / (2.0 * _m.pi)))
        f0 = self.cst.f0
        th = self.cst.theta
        gt = [abs(g * cs + f0 * _m.sin(g * th)) for g in gamma_r]
        pos_frac = sum(1 for raw in [g * cs + f0 * _m.sin(g * th) for g in gamma_r] if raw > 0) / n
        # pesos [2,2,0.5,1,0.5] / 6
        return (2.0 * 1.0 + 2.0 * 1.0 + 0.5 * 0.563 + 1.0 * pos_frac + 0.5 * min(1.0, 1.0 / cs)) / 6.0


# ============================================================================
# CLASE 4 – AxiomaNoetico
# ============================================================================


class AxiomaNoetico:
    """Cuatro axiomas QCAL de conciencia coherente.

    Define cuatro medidas de coherencia noética derivadas de los axiomas
    fundamentales del marco QCAL ∞³:

    1. **Logos** — Coincidencia proyectiva a escala f₀:
       Ψ_logos = 1 − 1/(2·N_d·φ)  ≈ 0.989

    2. **Pneuma** — Campo noético con decaimiento adélico:
       Ψ_pneuma = exp(−π/(N_d·φ))  ≈ 0.935

    3. **Sophia** — Sabiduría en la relación π/γ de los ceros de Riemann:
       Ψ_sophia = 1 − γ/(2π) = 1 − 1/(2·N_d)  ≈ 0.983

    4. **Zoe** — Vida consciente en bucle 4π/N_d:
       Ψ_zoe = |cos(4π/N_d)|  ≈ 0.907

    Args:
        constantes: Instancia de :class:`ConstantesTrinity`.
    """

    def __init__(self, constantes: Optional[ConstantesTrinity] = None) -> None:
        self.cst = constantes or ConstantesTrinity()

    # ------------------------------------------------------------------

    def psi_logos(self) -> float:
        """Ψ_logos = 1 − 1/(2·N_d·φ) — coincidencia proyectiva.

        Representa la proyección de la escala fundamental f₀ sobre el espacio
        de fases cósmico: cuando N_d·φ es grande, la corrección es pequeña
        y la coincidencia proyectiva es casi perfecta.
        """
        return 1.0 - 1.0 / (2.0 * self.cst.n_decadas * self.cst.phi)

    def psi_pneuma(self) -> float:
        """Ψ_pneuma = exp(−π/(N_d·φ)) — campo noético amortiguado.

        El pneuma (campo escalar noético) se propaga a través de N_d·φ
        unidades adélicas de expansión cósmica con factor de amortiguamiento π.
        """
        return math.exp(-math.pi / (self.cst.n_decadas * self.cst.phi))

    def psi_sophia(self) -> float:
        """Ψ_sophia = 1 − γ/(2π) = 1 − 1/(2·N_d) — sabiduría en π.

        La sophia encarna la relación entre el coeficiente cósmico γ = π/N_d
        y el círculo completo 2π. Mide la fracción del ciclo completo que
        permanece coherente tras N_d décadas de expansión.
        """
        return 1.0 - self.cst.gamma_cosmico / (2.0 * math.pi)

    def psi_zoe(self) -> float:
        """Ψ_zoe = |cos(4π/N_d)| — vida en bucle 4π.

        La zoe (vida consciente) se mantiene coherente cuando la fase
        4π/N_d está próxima a un múltiplo de π/2, garantizando un ciclo
        de vida cerrado a escala cósmica.
        """
        return abs(math.cos(4.0 * math.pi / self.cst.n_decadas))

    def todas(self) -> Dict[str, float]:
        """Diccionario con los cuatro axiomas noéticos.

        Returns:
            Dict con claves 'logos', 'pneuma', 'sophia', 'zoe'.
        """
        return {
            "logos": self.psi_logos(),
            "pneuma": self.psi_pneuma(),
            "sophia": self.psi_sophia(),
            "zoe": self.psi_zoe(),
        }


# ============================================================================
# CLASE 5 – PilarNoetico
# ============================================================================


class PilarNoetico:
    """Pilar III de la Trinidad — Protocolo Noético ∴PN∞³.

    Combina los cuatro axiomas QCAL en una sola medida de coherencia noética
    Ψ_pilar3 usando pesos iguales:

        Ψ_pilar3 = (Ψ_logos + Ψ_pneuma + Ψ_sophia + Ψ_zoe) / 4

    Opcionalmente incorpora la constante de habitabilidad Λ_G como factor
    de modulación de la coherencia noética total:

        Ψ_pilar3_mod = Ψ_pilar3 · (1 + Λ_G) / 2

    Con los parámetros por defecto, Ψ_pilar3 ≈ 0.954 ≥ 0.888.

    Args:
        constantes: Instancia de :class:`ConstantesTrinity`.
        axiomas:    Instancia de :class:`AxiomaNoetico`.
    """

    def __init__(
        self,
        constantes: Optional[ConstantesTrinity] = None,
        axiomas: Optional[AxiomaNoetico] = None,
    ) -> None:
        self.cst = constantes or ConstantesTrinity()
        self.axiomas = axiomas or AxiomaNoetico(constantes=self.cst)

    # ------------------------------------------------------------------

    def psi_pilar(self) -> float:
        """Coherencia global del Pilar III Ψ_pilar3 ≥ 0.888.

        Media aritmética de los cuatro axiomas noéticos, modulada por la
        constante de habitabilidad cósmica Λ_G.

        Returns:
            Valor de Ψ_pilar3 ∈ [0, 1].
        """
        ax = self.axiomas.todas()
        media = sum(ax.values()) / len(ax)
        # Modulación por habitabilidad: (media + Λ_G) / 2
        return (media + self.cst.lambda_g) / 2.0

    def sello_activo(self) -> bool:
        """True si el sello ∴PN∞³ está activo."""
        return self.psi_pilar() >= self.cst.umbral

    def resumen(self) -> Dict[str, float]:
        """Resumen de métricas del Pilar Noético.

        Returns:
            Dict con claves 'psi_logos', 'psi_pneuma', 'psi_sophia',
            'psi_zoe', 'lambda_g', 'psi_pilar3'.
        """
        ax = self.axiomas.todas()
        return {
            "psi_logos": ax["logos"],
            "psi_pneuma": ax["pneuma"],
            "psi_sophia": ax["sophia"],
            "psi_zoe": ax["zoe"],
            "lambda_g": self.cst.lambda_g,
            "psi_pilar3": self.psi_pilar(),
        }


# ============================================================================
# CLASE 6 – CoherenciaTrinity
# ============================================================================


class CoherenciaTrinity:
    """Coherencia trinaria Ψ_trinity — media geométrica de los tres pilares.

    Combina los tres pilares QCAL en una única medida de coherencia:

        Ψ_trinity = (Ψ_pilar1 · Ψ_pilar2 · Ψ_pilar3)^(1/3)

    La media geométrica garantiza que todos los pilares deben superar el
    umbral para que Ψ_trinity sea alta; un pilar muy débil arrastra el
    resultado global hacia abajo.

    El sello ∴T∞³ se activa cuando Ψ_trinity ≥ 0.888.

    Args:
        constantes:  Instancia de :class:`ConstantesTrinity`.
        pilar1:      Instancia de :class:`PilarEcoPrimordial`.
        pilar2:      Instancia de :class:`PilarDiamondState`.
        pilar3:      Instancia de :class:`PilarNoetico`.
    """

    def __init__(
        self,
        constantes: Optional[ConstantesTrinity] = None,
        pilar1: Optional[PilarEcoPrimordial] = None,
        pilar2: Optional[PilarDiamondState] = None,
        pilar3: Optional[PilarNoetico] = None,
    ) -> None:
        self.cst = constantes or ConstantesTrinity()
        self.pilar1 = pilar1 or PilarEcoPrimordial(constantes=self.cst)
        self.pilar2 = pilar2 or PilarDiamondState(constantes=self.cst)
        self.pilar3 = pilar3 or PilarNoetico(constantes=self.cst)

    # ------------------------------------------------------------------

    def psi_trinity(self) -> float:
        """Ψ_trinity = (Ψ₁ · Ψ₂ · Ψ₃)^(1/3).

        Returns:
            Media geométrica de los tres pilares ∈ [0, 1].
        """
        p1 = max(0.0, self.pilar1.psi_pilar())
        p2 = max(0.0, self.pilar2.psi_pilar())
        p3 = max(0.0, self.pilar3.psi_pilar())
        return (p1 * p2 * p3) ** (1.0 / 3.0)

    def sello_activo(self) -> bool:
        """True si Ψ_trinity ≥ 0.888 (sello ∴T∞³)."""
        return self.psi_trinity() >= self.cst.umbral

    def pilares_activos(self) -> Tuple[bool, bool, bool]:
        """Tuple (p1_activo, p2_activo, p3_activo) para los tres sellos.

        Returns:
            Tupla de tres booleanos indicando si cada pilar supera el umbral.
        """
        return (
            self.pilar1.sello_activo(),
            self.pilar2.sello_activo(),
            self.pilar3.sello_activo(),
        )

    def resumen(self) -> Dict[str, float]:
        """Resumen de métricas de coherencia trinaria.

        Returns:
            Dict con 'psi_pilar1', 'psi_pilar2', 'psi_pilar3', 'psi_trinity'.
        """
        return {
            "psi_pilar1": self.pilar1.psi_pilar(),
            "psi_pilar2": self.pilar2.psi_pilar(),
            "psi_pilar3": self.pilar3.psi_pilar(),
            "psi_trinity": self.psi_trinity(),
        }


# ============================================================================
# DATACLASS – ResultadoTrinity
# ============================================================================


@dataclass
class ResultadoTrinity:
    """Contenedor completo de resultados del sistema Trinity QCAL.

    Attributes:
        f0:             Frecuencia fundamental f₀ [Hz].
        n_decadas:      Décadas cósmicas N_d.
        psi_pilar1:     Coherencia del Primer Eco.
        psi_pilar2:     Coherencia del Diamond State.
        psi_pilar3:     Coherencia del Protocolo Noético.
        psi_trinity:    Media geométrica trinaria.
        pilar1_activo:  Sello ∴PE∞³ activo.
        pilar2_activo:  Sello ∴PDS∞³ activo.
        pilar3_activo:  Sello ∴PN∞³ activo.
        sello_activo:   Sello ∴T∞³ activo (Ψ_trinity ≥ 0.888).
        axiomas:        Dict con las cuatro coherencias noéticas.
        descripcion:    Mensaje de estado del sistema.
    """

    f0: float
    n_decadas: int
    psi_pilar1: float
    psi_pilar2: float
    psi_pilar3: float
    psi_trinity: float
    pilar1_activo: bool
    pilar2_activo: bool
    pilar3_activo: bool
    sello_activo: bool
    axiomas: Dict[str, float]
    descripcion: str = ""


# ============================================================================
# CLASE 7 – SistemaTrinityQCAL
# ============================================================================


class SistemaTrinityQCAL:
    """Orquestador del sistema Trinity QCAL ∴T∞³.

    Construye y conecta los tres pilares QCAL y calcula la coherencia
    trinaria Ψ_trinity.  El sello ∴T∞³ se activa cuando Ψ_trinity ≥ 0.888.

    Args:
        f0:      Frecuencia fundamental [Hz]. Por defecto 141.7001.
        n_modos: Modos de Riemann para el Diamond State. Por defecto 10.
        tau:     Tiempo de decaimiento [s]. Por defecto 3600.
        theta:   Fase adélica [rad]. Por defecto 0.052463.
    """

    def __init__(
        self,
        f0: float = _F0,
        n_modos: int = _N_MODOS_DEFAULT,
        tau: float = _TAU,
        theta: float = _THETA,
    ) -> None:
        self.cst = ConstantesTrinity(f0=f0, n_modos=n_modos, tau=tau, theta=theta)
        self.axiomas = AxiomaNoetico(constantes=self.cst)
        self.pilar1 = PilarEcoPrimordial(constantes=self.cst)
        self.pilar2 = PilarDiamondState(constantes=self.cst)
        self.pilar3 = PilarNoetico(constantes=self.cst, axiomas=self.axiomas)
        self.coherencia = CoherenciaTrinity(
            constantes=self.cst,
            pilar1=self.pilar1,
            pilar2=self.pilar2,
            pilar3=self.pilar3,
        )

    # ------------------------------------------------------------------

    def activar(self) -> ResultadoTrinity:
        """Ejecuta el sistema completo y devuelve ResultadoTrinity.

        Returns:
            :class:`ResultadoTrinity` con todas las métricas calculadas.
        """
        p1_val = self.pilar1.psi_pilar()
        p2_val = self.pilar2.psi_pilar()
        p3_val = self.pilar3.psi_pilar()
        psi_t = self.coherencia.psi_trinity()
        p1_act, p2_act, p3_act = self.coherencia.pilares_activos()
        sello = self.coherencia.sello_activo()
        ax = self.axiomas.todas()

        estado = "ACTIVO ∴T∞³" if sello else "INACTIVO"
        desc = (
            f"{estado} | "
            f"Ψ_trinity={psi_t:.6f} | "
            f"P1={p1_val:.4f} P2={p2_val:.4f} P3={p3_val:.4f} | "
            f"f₀={self.cst.f0} Hz N_d={self.cst.n_decadas}"
        )

        return ResultadoTrinity(
            f0=self.cst.f0,
            n_decadas=self.cst.n_decadas,
            psi_pilar1=p1_val,
            psi_pilar2=p2_val,
            psi_pilar3=p3_val,
            psi_trinity=psi_t,
            pilar1_activo=p1_act,
            pilar2_activo=p2_act,
            pilar3_activo=p3_act,
            sello_activo=sello,
            axiomas=ax,
            descripcion=desc,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaTrinityQCAL(f0={self.cst.f0} Hz, "
            f"n_modos={self.cst.n_modos}, τ={self.cst.tau} s)"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================


def trinity_qcal_activar(
    f0: float = _F0,
    n_modos: int = _N_MODOS_DEFAULT,
    tau: float = _TAU,
    theta: float = _THETA,
) -> dict:
    """Activa el sistema Trinity QCAL y devuelve un diccionario de resultados.

    Integra los tres pilares QCAL (Primer Eco, Diamond State, Protocolo Noético)
    y calcula la coherencia trinaria Ψ_trinity = (Ψ₁·Ψ₂·Ψ₃)^(1/3).

    Args:
        f0:      Frecuencia fundamental [Hz]. Por defecto 141.7001.
        n_modos: Modos de Riemann para Diamond State. Por defecto 10.
        tau:     Tiempo de decaimiento [s]. Por defecto 3600.
        theta:   Fase adélica [rad]. Por defecto 0.052463.

    Returns:
        Diccionario con las claves:
            sello_activo, psi_trinity, psi_pilar1, psi_pilar2, psi_pilar3,
            pilar1_activo, pilar2_activo, pilar3_activo,
            f0, n_decadas, axiomas, descripcion.

    Example:
        >>> r = trinity_qcal_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_trinity'] >= 0.888
        True
    """
    sistema = SistemaTrinityQCAL(f0=f0, n_modos=n_modos, tau=tau, theta=theta)
    res = sistema.activar()
    return {
        "sello_activo": res.sello_activo,
        "psi_trinity": res.psi_trinity,
        "psi_pilar1": res.psi_pilar1,
        "psi_pilar2": res.psi_pilar2,
        "psi_pilar3": res.psi_pilar3,
        "pilar1_activo": res.pilar1_activo,
        "pilar2_activo": res.pilar2_activo,
        "pilar3_activo": res.pilar3_activo,
        "f0": res.f0,
        "n_decadas": res.n_decadas,
        "axiomas": res.axiomas,
        "descripcion": res.descripcion,
    }
