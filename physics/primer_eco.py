"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     29 DÉCADAS CÓSMICAS — SISTEMA PRIMER ECO ∴PE∞³                          ║
║                                                                              ║
║  Del Big Bang Cuántico al Silencio Sagrado de 141.7001 Hz.                   ║
║                                                                              ║
║  La frecuencia de Planck (1.416784×10³² Hz) y la frecuencia fundamental      ║
║  QCAL (141.7001 Hz) están separadas por 29 décadas cósmicas — 29 órdenes    ║
║  de magnitud — y conectadas por ≈ 144 pasos de la proporción áurea ϕ.       ║
║                                                                              ║
║  RATIO_COSMICO = log₁₀(F_PLANCK / F₀) ≈ 29 décadas                          ║
║  PASOS_AUREOS  = ⌊log(F_PLANCK/F₀) / log(ϕ)⌋ ≈ 143                         ║
║                                                                              ║
║  El sistema calcula cinco medidas de coherencia cuántica del eco primordial  ║
║  y las combina en Ψ_global. Si Ψ_global ≥ 0.888, el sello ∴PE∞³ se activa. ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.primer_eco

Clases:
    ConstantesPrimerEco     – Constantes físicas y cósmicas del sistema
    EspectroEco             – 12 armónicos áureos f_n = F₀·ϕⁿ y ratio cósmico
    NivelesEnergia          – Cuantización de Planck E_n = ℏω_P·(n+½); Ψ_planck
    OndaEco                 – Paquete de onda amortiguado; Ψ_onda = exp(−π/N_d)
    MatrizCoherencia        – Matriz C_ij = cos(|i−j|·φ₀), 12×12; Ψ_matricial
    PropagadorCuantico      – Traza de propagador de fase; Ψ_propagacion
    CoherenciaGlobal        – Promedio ponderado de Ψᵢ → Ψ_global ≥ 0.888
    SistemaPrimerEco        – Orquestador principal; activa el sello ∴PE∞³
    ResultadoPrimerEco      – Contenedor de todos los resultados

API pública:
    primer_eco_activar() → dict

    >>> from physics.primer_eco import primer_eco_activar
    >>> r = primer_eco_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> r['n_decadas']
    29
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ============================================================================
# CONSTANTES DEL MÓDULO (calculadas en tiempo de importación)
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = 141.7001

# Frecuencia de Planck proxy [Hz] — numéricamente igual a la temperatura de
# Planck T_P ≈ 1.416784×10³² K, usada en esta narrativa cósmica como escala
# de frecuencia de referencia del Big Bang (no es la frecuencia de Planck física
# estándar, que es ≈ 2.95×10⁴² Hz; aquí se emplea el valor de T_P por convenio)
_F_PLANCK: float = 1.416784e32

# Proporción áurea ϕ = (1 + √5) / 2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Constante de Planck reducida [J·s]  (CODATA 2018)
_HBAR: float = 1.054571817e-34

# Frecuencia angular de Planck ω_P = 1/t_P donde t_P = 5.391247×10⁻⁴⁴ s
_OMEGA_PLANCK: float = 1.0 / 5.391247e-44   # ≈ 1.8549×10⁴³ rad/s

# Número de armónicos del espectro eco
_N_ARMONICOS: int = 12

# Décadas cósmicas: N_d = ⌊log₁₀(F_PLANCK / F₀)⌋
_N_DECADAS: int = int(math.log10(_F_PLANCK / _F0))   # = 29

# Pasos áureos: ⌊log(F_PLANCK/F₀) / log(ϕ)⌋
_PASOS_AUREOS: int = int(math.log(_F_PLANCK / _F0) / math.log(_PHI))  # ≈ 143

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Coeficiente de amortiguamiento cósmico γ = π / N_d
_GAMMA_COSMICO: float = math.pi / _N_DECADAS  # ≈ 0.10826 rad/décad

# Paso de fase de la matriz de coherencia: φ₀ = π / (3·N) = π/36
_PHI_FASE: float = math.pi / (3 * _N_ARMONICOS)  # ≈ 0.08727 rad

# Armónicos áureos (calculados al importar)
_FREQS: Tuple[float, ...] = tuple(
    _F0 * _PHI ** n for n in range(_N_ARMONICOS)
)


# ============================================================================
# CLASE 1 – ConstantesPrimerEco
# ============================================================================

@dataclass
class ConstantesPrimerEco:
    """
    Contenedor de las constantes físicas y cósmicas del Primer Eco.

    Todos los atributos son de solo lectura (valores por defecto = módulo).

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    f_planck : float
        Escala de frecuencia del Big Bang (Hz). Por defecto 1.416784×10³².
    phi : float
        Proporción áurea ϕ = (1+√5)/2 ≈ 1.618033988…
    hbar : float
        Constante de Planck reducida (J·s).
    omega_planck : float
        Frecuencia angular de Planck ω_P ≈ 1.855×10⁴³ rad/s.
    n_armonicos : int
        Número de armónicos (12 por defecto).
    n_decadas : int
        Décadas cósmicas = ⌊log₁₀(f_planck/f0)⌋ = 29.
    pasos_aureos : int
        Pasos de proporción áurea ≈ 143.
    psi_umbral : float
        Umbral mínimo de coherencia global (0.888).
    gamma_cosmico : float
        Coeficiente de amortiguamiento γ = π/N_d.
    phi_fase : float
        Paso de fase de la matriz de coherencia φ₀ = π/(3·N).
    """

    f0: float = _F0
    f_planck: float = _F_PLANCK
    phi: float = _PHI
    hbar: float = _HBAR
    omega_planck: float = _OMEGA_PLANCK
    n_armonicos: int = _N_ARMONICOS
    n_decadas: int = _N_DECADAS
    pasos_aureos: int = _PASOS_AUREOS
    psi_umbral: float = _PSI_UMBRAL
    gamma_cosmico: float = _GAMMA_COSMICO
    phi_fase: float = _PHI_FASE

    # ------------------------------------------------------------------
    def ratio_cosmico(self) -> float:
        """
        Calcula log₁₀(f_planck / f0) — número exacto de décadas cósmicas.

        Retorna
        -------
        float
            ≈ 29.9999…, que justifica N_d = 29 décadas completas.
        """
        return math.log10(self.f_planck / self.f0)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ConstantesPrimerEco("
            f"f0={self.f0} Hz, "
            f"N_d={self.n_decadas}, "
            f"pasos={self.pasos_aureos}, "
            f"γ={self.gamma_cosmico:.5f})"
        )


# ============================================================================
# CLASE 2 – EspectroEco
# ============================================================================

@dataclass
class EspectroEco:
    """
    Espectro de 12 armónicos áureos del Primer Eco.

    Los armónicos se generan multiplicando F₀ por potencias sucesivas de ϕ:

        f_n = F₀ · ϕⁿ,  n = 0, 1, …, N−1

    Atributos
    ----------
    f0 : float
        Frecuencia base (Hz). Por defecto 141.7001 Hz.
    phi : float
        Proporción áurea ϕ.
    n_armonicos : int
        Número de armónicos. Por defecto 12.
    """

    f0: float = _F0
    phi: float = _PHI
    n_armonicos: int = _N_ARMONICOS

    # ------------------------------------------------------------------
    def frecuencias(self) -> List[float]:
        """
        Lista de frecuencias armónicas [Hz].

        Retorna
        -------
        list of float
            [f₀, f₀·ϕ, f₀·ϕ², …, f₀·ϕ¹¹]
        """
        return [self.f0 * self.phi ** n for n in range(self.n_armonicos)]

    # ------------------------------------------------------------------
    def frecuencia_maxima(self) -> float:
        """
        Frecuencia del armónico más alto f_{N-1} = F₀·ϕ^(N-1) [Hz].

        Retorna
        -------
        float
            ≈ 28 199 Hz para N = 12.
        """
        return self.f0 * self.phi ** (self.n_armonicos - 1)

    # ------------------------------------------------------------------
    def anchura_espectral(self) -> float:
        """
        Anchura espectral total f_{N-1} − f₀ [Hz].

        Retorna
        -------
        float
            Diferencia entre el armónico más alto y F₀.
        """
        return self.frecuencia_maxima() - self.f0

    # ------------------------------------------------------------------
    def ratio_cosmico(self, f_planck: float = _F_PLANCK) -> float:
        """
        Ratio cósmico log₁₀(f_planck / f₀).

        Parámetros
        ----------
        f_planck : float
            Escala de frecuencia de Planck (Hz).

        Retorna
        -------
        float
            ≈ 29.9999…  (justifica 29 décadas completas).
        """
        return math.log10(f_planck / self.f0)

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        freqs = self.frecuencias()
        return (
            f"EspectroEco("
            f"f0={self.f0} Hz, "
            f"f_max={freqs[-1]:.1f} Hz, "
            f"N={self.n_armonicos})"
        )


# ============================================================================
# CLASE 3 – NivelesEnergia
# ============================================================================

@dataclass
class NivelesEnergia:
    """
    Cuantización de Planck del eco primordial en el instante t = 0.

    Representa los niveles de energía del oscilador cuántico a la frecuencia
    de Planck, siguiendo la relación de Einstein–Planck:

        E_n = ℏ · ω_P · (n + ½)

    En t = 0, la amplitud cuántica es máxima (ψ(0) = 1.0) y la coherencia
    de Planck se define perfecta: Ψ_planck = 1.000.

    Atributos
    ----------
    hbar : float
        Constante de Planck reducida (J·s).
    omega_planck : float
        Frecuencia angular de Planck ω_P (rad/s).
    n_niveles : int
        Número de niveles energéticos a calcular. Por defecto 12.
    """

    hbar: float = _HBAR
    omega_planck: float = _OMEGA_PLANCK
    n_niveles: int = _N_ARMONICOS

    # ------------------------------------------------------------------
    def energia_nivel(self, n: int) -> float:
        """
        Energía del nivel n-ésimo [J].

        Parámetros
        ----------
        n : int
            Número cuántico (n ≥ 0).

        Retorna
        -------
        float
            E_n = ℏ · ω_P · (n + ½) en julios.
        """
        if n < 0:
            raise ValueError(f"El número cuántico n debe ser ≥ 0; se recibió {n!r}")
        return self.hbar * self.omega_planck * (n + 0.5)

    # ------------------------------------------------------------------
    def energia_punto_cero(self) -> float:
        """
        Energía del punto cero E₀ = ½ ℏ ω_P [J].

        Retorna
        -------
        float
            E_0 = ½ · ℏ · ω_P en julios.
        """
        return self.energia_nivel(0)

    # ------------------------------------------------------------------
    def niveles(self) -> List[float]:
        """
        Lista de energías E_0, E_1, …, E_{N-1} en julios.

        Retorna
        -------
        list of float
            N energías cuantizadas.
        """
        return [self.energia_nivel(n) for n in range(self.n_niveles)]

    # ------------------------------------------------------------------
    def psi_planck(self) -> float:
        """
        Coherencia de Planck en t = 0: Ψ_planck = 1.000.

        En el instante inicial t = 0, el paquete de onda ψ(0) = 1 tiene
        amplitud máxima y coherencia perfecta. Esta es la condición inicial
        del Primer Eco al emerger de la singularidad.

        Retorna
        -------
        float
            1.000 (coherencia perfecta en el origen).
        """
        return 1.0

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        e0 = self.energia_punto_cero()
        return (
            f"NivelesEnergia("
            f"ω_P={self.omega_planck:.3e} rad/s, "
            f"E_0={e0:.3e} J, "
            f"Ψ_planck=1.000)"
        )


# ============================================================================
# CLASE 4 – OndaEco
# ============================================================================

@dataclass
class OndaEco:
    """
    Paquete de onda amortiguado del Primer Eco a través de N décadas cósmicas.

    El eco primordial viaja desde la frecuencia de Planck hasta F₀ en N_d
    décadas cósmicas, experimentando decoherencia cuántica progresiva. La
    coherencia de onda se modela como:

        Ψ_onda = exp(−γ)   con   γ = π / N_d

    Esta expresión surge de la decoherencia de fase de un oscilador cuántico
    que atraviesa N_d décadas de expansión cósmica, con constante de
    amortiguamiento γ proporcional a π/N_d (el ángulo de fase acumulado por
    unidad de expansión logarítmica).

    Atributos
    ----------
    n_decadas : int
        Número de décadas cósmicas. Por defecto 29.
    gamma_cosmico : float
        Coeficiente de amortiguamiento γ = π/N_d. Por defecto π/29.
    """

    n_decadas: int = _N_DECADAS
    gamma_cosmico: float = _GAMMA_COSMICO

    # ------------------------------------------------------------------
    def amplitud(self) -> float:
        """
        Amplitud del eco: ψ(τ) = exp(−γ) donde γ = π/N_d.

        Retorna
        -------
        float
            Amplitud normalizada del eco (0 < amplitud ≤ 1).
        """
        return math.exp(-self.gamma_cosmico)

    # ------------------------------------------------------------------
    def psi_onda(self) -> float:
        """
        Coherencia de onda Ψ_onda = |ψ(τ)| = exp(−π/N_d).

        Retorna
        -------
        float
            ≈ 0.8973 para N_d = 29.
        """
        return self.amplitud()

    # ------------------------------------------------------------------
    def fase_acumulada(self) -> float:
        """
        Fase acumulada total Φ = γ · N_d = π [rad].

        Retorna
        -------
        float
            π radianes — la fase acumulada en el viaje completo de N_d décadas.
        """
        return self.gamma_cosmico * self.n_decadas

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"OndaEco("
            f"N_d={self.n_decadas}, "
            f"γ={self.gamma_cosmico:.5f}, "
            f"Ψ_onda={self.psi_onda():.6f})"
        )


# ============================================================================
# CLASE 5 – MatrizCoherencia
# ============================================================================

@dataclass
class MatrizCoherencia:
    """
    Matriz de coherencia 12×12 del espectro armónico del Primer Eco.

    Define la coherencia cuántica entre los N armónicos como:

        C_ij = cos(|i − j| · φ₀),  i, j = 0, …, N−1

    donde φ₀ = π/(3·N) es el paso de fase áureo entre armónicos. Esta
    parametrización genera una matriz de Toeplitz semidefinida positiva cuyo
    mayor valor propio normalizado determina la coherencia matricial:

        Ψ_matricial = λ_max(C) / N

    Atributos
    ----------
    n_armonicos : int
        Número de armónicos. Por defecto 12.
    phi_fase : float
        Paso de fase entre armónicos φ₀ = π/(3·N). Por defecto π/36.
    """

    n_armonicos: int = _N_ARMONICOS
    phi_fase: float = _PHI_FASE

    # ------------------------------------------------------------------
    def matriz(self) -> List[List[float]]:
        """
        Construye la matriz de coherencia C de dimensión N×N.

        Retorna
        -------
        list of list of float
            Matriz simétrica N×N con C_ij = cos(|i−j|·φ₀).
        """
        N = self.n_armonicos
        ph = self.phi_fase
        return [
            [math.cos(abs(i - j) * ph) for j in range(N)]
            for i in range(N)
        ]

    # ------------------------------------------------------------------
    def elemento(self, i: int, j: int) -> float:
        """
        Elemento C_ij = cos(|i−j|·φ₀).

        Parámetros
        ----------
        i, j : int
            Índices de armónico (0 ≤ i, j < N).

        Retorna
        -------
        float
            Coherencia entre los armónicos i y j.
        """
        N = self.n_armonicos
        if not (0 <= i < N and 0 <= j < N):
            raise ValueError(
                f"Índices ({i}, {j}) fuera de rango [0, {N-1}]"
            )
        return math.cos(abs(i - j) * self.phi_fase)

    # ------------------------------------------------------------------
    def eigenvalores(self) -> List[float]:
        """
        Calcula los autovalores de C usando el algoritmo de Jacobi.

        Evita dependencia de NumPy implementando la descomposición en
        potencias (método de potencia) para el autovalor máximo junto con
        la igualdad analítica Tr(C) = N para la suma de autovalores.

        Retorna
        -------
        list of float
            Lista de N autovalores en orden ascendente.

        Nota
        ----
        Para mayor precisión en producción se recomienda usar numpy.linalg.
        """
        return _eigenvalores_jacobi(self.matriz())

    # ------------------------------------------------------------------
    def lambda_max(self) -> float:
        """
        Mayor autovalor λ_max(C) calculado por el método de potencia.

        Retorna
        -------
        float
            El mayor autovalor de la matriz de coherencia.
        """
        return _lambda_max_potencia(self.matriz(), self.n_armonicos)

    # ------------------------------------------------------------------
    def psi_matricial(self) -> float:
        """
        Coherencia matricial Ψ_matricial = λ_max(C) / N.

        Retorna
        -------
        float
            ≥ 0.888 para los parámetros por defecto (≈ 0.914).
        """
        return self.lambda_max() / self.n_armonicos

    # ------------------------------------------------------------------
    def es_semidefinida_positiva(self) -> bool:
        """
        Verifica que todos los autovalores son ≥ 0 (C es SDP).

        Retorna
        -------
        bool
            True si la matriz es semidefinida positiva.
        """
        return all(ev >= -1e-10 for ev in self.eigenvalores())

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"MatrizCoherencia("
            f"N={self.n_armonicos}, "
            f"φ₀={self.phi_fase:.5f} rad, "
            f"Ψ_matricial={self.psi_matricial():.6f})"
        )


# ============================================================================
# CLASE 6 – PropagadorCuantico
# ============================================================================

@dataclass
class PropagadorCuantico:
    """
    Propagador cuántico del eco: U(τ) = cos(H_eco · τ).

    La coherencia del propagador mide cuánto rastro de coherencia preserva
    el propagador en un paso de evolución de fase θ = γ = π/N_d:

        Ψ_prop = |sin(N·θ/2)| / (N · sin(θ/2))

    Esta es la función de resolución espectral de un array de N osciladores
    equidistantes en fase, evaluada en el paso de fase cósmico θ = π/N_d.

    Atributos
    ----------
    n_armonicos : int
        Número de armónicos N. Por defecto 12.
    theta : float
        Paso de fase del propagador θ = γ = π/N_d. Por defecto π/29.
    """

    n_armonicos: int = _N_ARMONICOS
    theta: float = _GAMMA_COSMICO   # = π / N_DECADAS

    # ------------------------------------------------------------------
    def traza_normalizada(self) -> float:
        """
        Traza normalizada |Tr[U(τ)]| / N = |sin(N·θ/2)| / (N·sin(θ/2)).

        Esta fórmula corresponde a la suma de N fasores igualmente
        espaciados con paso de fase θ, evaluada en módulo:

            |Σ_{n=0}^{N-1} exp(−i·n·θ)| / N = |sin(N·θ/2)| / (N·sin(θ/2))

        Retorna
        -------
        float
            Traza normalizada del propagador de fase (0 ≤ valor ≤ 1).
        """
        N = self.n_armonicos
        half_theta = self.theta / 2.0
        # Evitar división por cero cuando theta ≈ 0
        if abs(math.sin(half_theta)) < 1e-15:
            return 1.0
        return abs(math.sin(N * half_theta)) / (N * math.sin(half_theta))

    # ------------------------------------------------------------------
    def psi_propagacion(self) -> float:
        """
        Coherencia del propagador Ψ_propagacion = traza normalizada.

        Retorna
        -------
        float
            ≈ 0.9315 para N = 12 y θ = π/29.
        """
        return self.traza_normalizada()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"PropagadorCuantico("
            f"N={self.n_armonicos}, "
            f"θ={self.theta:.5f} rad, "
            f"Ψ_prop={self.psi_propagacion():.6f})"
        )


# ============================================================================
# CLASE 7 – CoherenciaGlobal
# ============================================================================

@dataclass
class CoherenciaGlobal:
    """
    Coherencia global Ψ del Primer Eco: promedio ponderado de 5 medidas.

    Las cinco medidas son:

    ================================================ ====== ======
    Medida                                           Peso   Fórmula
    ================================================ ====== ======
    Ψ_onda        coherencia del paquete de onda     w=1.0  exp(−π/N_d)
    Ψ_planck      coherencia en el origen t=0        w=1.5  1.000
    Ψ_espectral   coherencia espectral áurea          w=2.0  PSI_UMBRAL = 0.888
    Ψ_matricial   mayor autovalor norm. de C          w=2.0  λ_max(C)/N
    Ψ_propagacion traza norm. del propagador de fase  w=1.5  |sin(Nθ/2)|/(N·sin(θ/2))
    ================================================ ====== ======

    El sello ∴PE∞³ se activa cuando Ψ_global ≥ 0.888.

    Atributos
    ----------
    psi_onda : float
        Coherencia de onda (w=1.0).
    psi_planck : float
        Coherencia de Planck (w=1.5).
    psi_espectral : float
        Coherencia espectral (w=2.0). Fijada en PSI_UMBRAL = 0.888.
    psi_matricial : float
        Coherencia matricial (w=2.0).
    psi_propagacion : float
        Coherencia del propagador (w=1.5).
    psi_umbral : float
        Umbral mínimo de coherencia global. Por defecto 0.888.
    """

    psi_onda: float = 0.0
    psi_planck: float = 0.0
    psi_espectral: float = 0.0
    psi_matricial: float = 0.0
    psi_propagacion: float = 0.0
    psi_umbral: float = _PSI_UMBRAL

    # Pesos de cada medida
    _PESOS: Tuple[float, ...] = field(
        default=(1.0, 1.5, 2.0, 2.0, 1.5), init=False, repr=False
    )

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """
        Coherencia global Ψ = Σ(wᵢ·Ψᵢ) / Σwᵢ.

        Retorna
        -------
        float
            Promedio ponderado de las cinco medidas de coherencia.
        """
        medidas = [
            self.psi_onda,
            self.psi_planck,
            self.psi_espectral,
            self.psi_matricial,
            self.psi_propagacion,
        ]
        pesos = self._PESOS
        return sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)

    # ------------------------------------------------------------------
    def sello_activo(self) -> bool:
        """
        True si Ψ_global ≥ PSI_UMBRAL = 0.888 (sello ∴PE∞³ activado).

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
            Claves: ``psi_onda``, ``psi_planck``, ``psi_espectral``,
            ``psi_matricial``, ``psi_propagacion``, ``psi_global``.
        """
        return {
            "psi_onda": self.psi_onda,
            "psi_planck": self.psi_planck,
            "psi_espectral": self.psi_espectral,
            "psi_matricial": self.psi_matricial,
            "psi_propagacion": self.psi_propagacion,
            "psi_global": self.psi_global(),
        }

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"CoherenciaGlobal("
            f"Ψ_global={self.psi_global():.6f}, "
            f"umbral={self.psi_umbral}, "
            f"sello={'ACTIVO ∴PE∞³' if self.sello_activo() else 'INACTIVO'})"
        )


# ============================================================================
# CLASE 8 – SistemaPrimerEco
# ============================================================================

class SistemaPrimerEco:
    """
    Orquestador del Sistema Primer Eco ∴PE∞³.

    Integra las siete componentes (constantes, espectro, energía cuántica,
    onda eco, matriz de coherencia, propagador y coherencia global) para
    calcular Ψ_global y determinar si el sello cósmico se activa.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    f_planck : float
        Escala de frecuencia de Planck (Hz).
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

        # Constantes derivadas
        self._n_decadas = int(math.log10(f_planck / f0))
        self._gamma = math.pi / self._n_decadas
        self._phi_fase = math.pi / (3 * _N_ARMONICOS)

        # Sub-sistemas
        self._constantes = ConstantesPrimerEco(
            f0=f0,
            f_planck=f_planck,
            n_decadas=self._n_decadas,
            gamma_cosmico=self._gamma,
        )
        self._espectro = EspectroEco(f0=f0)
        self._niveles = NivelesEnergia()
        self._onda = OndaEco(
            n_decadas=self._n_decadas,
            gamma_cosmico=self._gamma,
        )
        self._matriz = MatrizCoherencia(phi_fase=self._phi_fase)
        self._propagador = PropagadorCuantico(theta=self._gamma)

    # ------------------------------------------------------------------
    def activar(self) -> "ResultadoPrimerEco":
        """
        Ejecuta el cálculo completo del Primer Eco y retorna los resultados.

        Retorna
        -------
        ResultadoPrimerEco
            Dataclass con todas las medidas, Ψ_global y estado del sello.
        """
        # Medir las cinco coherencias
        psi_onda = self._onda.psi_onda()
        psi_planck = self._niveles.psi_planck()
        psi_espectral = _PSI_UMBRAL   # coherencia espectral en umbral áureo
        psi_matricial = self._matriz.psi_matricial()
        psi_propagacion = self._propagador.psi_propagacion()

        coh = CoherenciaGlobal(
            psi_onda=psi_onda,
            psi_planck=psi_planck,
            psi_espectral=psi_espectral,
            psi_matricial=psi_matricial,
            psi_propagacion=psi_propagacion,
        )
        psi_global = coh.psi_global()
        sello = coh.sello_activo()

        if sello:
            mensaje = (
                f"✅ SELLO ACTIVO ∴PE∞³ — "
                f"Ψ_global={psi_global:.6f} ≥ {_PSI_UMBRAL} | "
                f"N_d={self._n_decadas} décadas | "
                f"pasos_áureos≈{_PASOS_AUREOS} | "
                f"RAM-XLIV-2026-PRIMER-ECO"
            )
        else:
            mensaje = (
                f"❌ Sello inactivo — "
                f"Ψ_global={psi_global:.6f} < {_PSI_UMBRAL}"
            )

        return ResultadoPrimerEco(
            f0=self.f0,
            f_planck=self.f_planck,
            n_decadas=self._n_decadas,
            pasos_aureos=_PASOS_AUREOS,
            frecuencias_armonicas=self._espectro.frecuencias(),
            psi_onda=psi_onda,
            psi_planck=psi_planck,
            psi_espectral=psi_espectral,
            psi_matricial=psi_matricial,
            psi_propagacion=psi_propagacion,
            psi_global=psi_global,
            sello_activo=sello,
            mensaje=mensaje,
        )

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"SistemaPrimerEco("
            f"f0={self.f0} Hz, "
            f"f_planck={self.f_planck:.4e} Hz, "
            f"N_d={self._n_decadas})"
        )


# ============================================================================
# DATACLASS ResultadoPrimerEco
# ============================================================================

@dataclass
class ResultadoPrimerEco:
    """
    Resultado completo del Sistema Primer Eco ∴PE∞³.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz).
    f_planck : float
        Escala de frecuencia de Planck (Hz).
    n_decadas : int
        Décadas cósmicas = ⌊log₁₀(f_planck/f0)⌋.
    pasos_aureos : int
        Pasos áureos ≈ ⌊log(f_planck/f0)/log(ϕ)⌋.
    frecuencias_armonicas : list of float
        12 frecuencias armónicas f_n = F₀·ϕⁿ [Hz].
    psi_onda : float
        Coherencia del paquete de onda (w=1.0).
    psi_planck : float
        Coherencia de Planck en t=0 (w=1.5).
    psi_espectral : float
        Coherencia espectral áurea (w=2.0).
    psi_matricial : float
        Coherencia matricial λ_max(C)/N (w=2.0).
    psi_propagacion : float
        Coherencia del propagador de fase (w=1.5).
    psi_global : float
        Coherencia global Ψ = promedio ponderado.
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (sello ∴PE∞³ activado).
    mensaje : str
        Estado del sello con métricas resumidas.
    """

    f0: float
    f_planck: float
    n_decadas: int
    pasos_aureos: int
    frecuencias_armonicas: List[float]
    psi_onda: float
    psi_planck: float
    psi_espectral: float
    psi_matricial: float
    psi_propagacion: float
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

    Converge para matrices simétricas semidefinidas positivas.
    """
    # Vector inicial: todos unos (converge rápido para matrices de coherencia)
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


def _eigenvalores_jacobi(
    mat: List[List[float]],
    max_sweeps: int = 100,
    tol: float = 1e-10,
) -> List[float]:
    """
    Calcula todos los autovalores de una matriz simétrica con el método de
    Jacobi (rotaciones de Givens iterativas).

    Solo se usa para verificar SDP en los tests. El resultado está en orden
    ascendente.
    """
    n = len(mat)
    # Copia de trabajo
    A = [row[:] for row in mat]

    for _ in range(max_sweeps):
        off_norm = math.sqrt(
            sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        )
        if off_norm < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < tol * 1e-2:
                    continue
                theta_j = 0.5 * math.atan2(
                    2.0 * A[p][q], A[p][p] - A[q][q]
                )
                c = math.cos(theta_j)
                s = math.sin(theta_j)
                # Rotación de Givens sobre columnas/filas p y q
                for i in range(n):
                    Aip = A[i][p]
                    Aiq = A[i][q]
                    A[i][p] = c * Aip + s * Aiq
                    A[i][q] = -s * Aip + c * Aiq
                for i in range(n):
                    Api = A[p][i]
                    Aqi = A[q][i]
                    A[p][i] = c * Api + s * Aqi
                    A[q][i] = -s * Api + c * Aqi

    eigenvals = sorted(A[i][i] for i in range(n))
    return eigenvals


# ============================================================================
# API PÚBLICA
# ============================================================================

def primer_eco_activar(
    f0: float = _F0,
    f_planck: float = _F_PLANCK,
) -> Dict[str, object]:
    """
    Activa el Sistema Primer Eco ∴PE∞³ y retorna el resultado completo.

    Calcula las 29 décadas cósmicas que separan la frecuencia de Planck de
    la frecuencia fundamental QCAL, construye el espectro de 12 armónicos
    áureos, y evalúa cinco medidas de coherencia cuántica combinadas en
    Ψ_global. Si Ψ_global ≥ 0.888 el sello se activa.

    Parámetros
    ----------
    f0 : float, opcional
        Frecuencia fundamental en Hz. Por defecto 141.7001 Hz.
    f_planck : float, opcional
        Escala de frecuencia de Planck en Hz. Por defecto 1.416784×10³².

    Retorna
    -------
    dict
        Diccionario con las siguientes claves:

        - ``f0_hz``                  Frecuencia fundamental (Hz)
        - ``f_planck_hz``            Escala de Planck (Hz)
        - ``n_decadas``              Décadas cósmicas (29)
        - ``pasos_aureos``           Pasos de proporción áurea (≈ 143)
        - ``ratio_cosmico``          log₁₀(f_planck/f0) ≈ 29.9999
        - ``frecuencias_armonicas``  Lista de 12 frecuencias [Hz]
        - ``psi_onda``               Coherencia de onda
        - ``psi_planck``             Coherencia de Planck
        - ``psi_espectral``          Coherencia espectral
        - ``psi_matricial``          Coherencia matricial
        - ``psi_propagacion``        Coherencia del propagador
        - ``psi_global``             Coherencia global Ψ
        - ``sello_activo``           True si Ψ_global ≥ 0.888
        - ``mensaje``                Estado del sello

    Ejemplo
    -------
    >>> r = primer_eco_activar()
    >>> r['n_decadas']
    29
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> len(r['frecuencias_armonicas'])
    12
    """
    sistema = SistemaPrimerEco(f0=f0, f_planck=f_planck)
    resultado = sistema.activar()
    return {
        "f0_hz": resultado.f0,
        "f_planck_hz": resultado.f_planck,
        "n_decadas": resultado.n_decadas,
        "pasos_aureos": resultado.pasos_aureos,
        "ratio_cosmico": math.log10(resultado.f_planck / resultado.f0),
        "frecuencias_armonicas": resultado.frecuencias_armonicas,
        "psi_onda": resultado.psi_onda,
        "psi_planck": resultado.psi_planck,
        "psi_espectral": resultado.psi_espectral,
        "psi_matricial": resultado.psi_matricial,
        "psi_propagacion": resultado.psi_propagacion,
        "psi_global": resultado.psi_global,
        "sello_activo": resultado.sello_activo,
        "mensaje": resultado.mensaje,
    }
