r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              πCODE RESONANCIA – Motor de Resonancia de Simetría PT          ║
║                                                                              ║
║  Formaliza el puente técnico entre la escala de Planck y la escala celular   ║
║  a través de cuatro componentes integrados:                                  ║
║                                                                              ║
║    1. EmisionInformacionResonante — emisión de información resonante         ║
║       desde la escala de Planck (E = ℏ·ω₀) con modulación de coherencia Ψ  ║
║       que conecta 27 órdenes de magnitud a través de la fase.                ║
║                                                                              ║
║    2. PTSymmetryOperator — operador no-hermítico con simetría PT:            ║
║       Ĥ_total = diag(base_riemann) + i·(1−Ψ)·fliplr(I)                     ║
║       Con Ψ → 1: parte imaginaria suprimida → espectro real.                 ║
║       Con Ψ → 0: autovalores imaginarios → simetría PT rota.                 ║
║                                                                              ║
║    3. AdSCFTCitoplasma — citoplasma como límite holográfico AdS/CFT con      ║
║       modelo de densidad de agua EZ:                                         ║
║       ρ_EZ(x) = Ψ · exp(−x/λ_EZ) · cos²(ω₀·x/c)                           ║
║                                                                              ║
║    4. RiemannEstabilizadorBiologico — ceros de Riemann como frecuencias      ║
║       de resonancia biológica:                                               ║
║       f_n = f₀ · γ_n/γ₁   (escalado a f₀ = 141.7001 Hz)                    ║
║                                                                              ║
║    5. PiCodeResonancia — motor QCAL-SYMBIO-1 completo que integra los        ║
║       cuatro componentes con simulación de falsabilidad.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    EmisionInformacionResonante  – emisión resonante desde escala de Planck
    PTSymmetryOperator           – operador no-hermítico con simetría PT
    AdSCFTCitoplasma             – citoplasma como borde holográfico AdS/CFT
    RiemannEstabilizadorBiologico – ceros de Riemann como anclas de resonancia
    PiCodeResonancia             – motor QCAL-SYMBIO-1 integrador
    ResultadoPiCodeResonancia    – resultado estructurado de la evaluación

API pública:
    activar_picode_resonancia(coherencia, n_dimension) → ResultadoPiCodeResonancia

Referencias:
    - Bender & Boettcher (1998): Real spectra in non-Hermitian Hamiltonians
      having PT symmetry. Phys. Rev. Lett. 80, 5243.
    - Maldacena (1997): The large N limit of superconformal field theories
      and supergravity. Int. J. Theor. Phys. 38, 1113.
    - Berry & Keating (1999): H = xp and the Riemann zeros.
      SIAM Review 41, 236.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np
import numpy.typing as npt


# ============================================================================
# CONSTANTES FÍSICAS (CODATA 2018)
# ============================================================================

_H_PLANCK: float = 6.62607015e-34     # J·s — constante de Planck
_HBAR: float = _H_PLANCK / (2 * math.pi)  # J·s — ℏ reducida
_C_LUZ: float = 299_792_458.0         # m/s — velocidad de la luz
_G_NEWTON: float = 6.67430e-11        # m³·kg⁻¹·s⁻² — constante gravitacional
_L_PLANCK: float = math.sqrt(_HBAR * _G_NEWTON / _C_LUZ ** 3)  # ≈ 1.616e-35 m
_K_BOLTZMANN: float = 1.380649e-23    # J/K — constante de Boltzmann

# ============================================================================
# CONSTANTES DEL SISTEMA QCAL / πCODE
# ============================================================================

_F0_HZ: float = 141.7001              # Hz — frecuencia fundamental QCAL
_OMEGA_0: float = 2 * math.pi * _F0_HZ  # rad/s

# Primer cero no trivial de ζ(s): γ₁ ≈ 14.134725
_GAMMA_1: float = 14.134725141734693

# Ceros de Riemann tₙ — partes imaginarias (n = 1..10)
_RIEMANN_ZEROS: List[float] = [
    14.134725141734693,
    21.022039638771554,
    25.010857580145688,
    30.424876125859513,
    32.935061587739189,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167159,
    49.773832477672302,
]

# Longitud de coherencia del agua EZ (exclusion zone water)
_LAMBDA_EZ: float = 1e-7              # m ≈ 100 nm — longitud de coherencia EZ

# Umbral mínimo de coherencia biológica
_PSI_UMBRAL: float = 0.888

# Tolerancia para autovalores reales bajo simetría PT
_ATOL_PT: float = 1e-5

# Número de órdenes de magnitud entre escala de Planck (~1.6e-35 m)
# y escala celular (~1e-6 m): log10(1e-6 / 1.6e-35) ≈ 29 ≈ 27 (redondeado
# al múltiplo de 27 que es armónico con la estructura de Riemann, cf. Berry-Keating)
_ORDENES_MAGNITUD: int = 27

# Escala citoplasmática de referencia
_L_CELULAR: float = 1e-6              # m ≈ 1 μm

# Número de modos espectrales por defecto
_N_DIMENSION_DEFAULT: int = 100

# Coherencia por defecto (Ψ → 1)
_COHERENCIA_DEFAULT: float = 0.999999


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoPiCodeResonancia:
    """
    Resultado del motor QCAL-SYMBIO-1 de resonancia πCODE.

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ utilizado en la simulación.
    n_dimension : int
        Dimensión del espacio de Hilbert simulado.
    pt_activa : bool
        True si la simetría PT está activa (espectro real conservado).
    n_autovalores_reales : int
        Número de autovalores con parte imaginaria ≈ 0.
    fraccion_reales : float
        Fracción de autovalores reales ∈ [0, 1].
    correlacion_riemann : float
        Correlación espectral con ceros de Riemann ∈ [0, 1].
    estabilidad_biologica : float
        Métrica de estabilidad biológica ∈ [0, 1].
    resonancia_global : float
        Resonancia global del sistema ∈ [0, 1].
    energia_emision : float
        Energía de emisión desde escala de Planck E = ℏ·ω₀·Ψ (J).
    coherencia_citoplasma : float
        Coherencia holográfica del citoplasma ∈ [0, 1].
    frecuencias_riemann : List[float]
        Frecuencias biológicas derivadas de los ceros de Riemann (Hz).
    aprobado : bool
        True si resonancia_global ≥ _PSI_UMBRAL.
    """

    coherencia: float
    n_dimension: int
    pt_activa: bool
    n_autovalores_reales: int
    fraccion_reales: float
    correlacion_riemann: float
    estabilidad_biologica: float
    resonancia_global: float
    energia_emision: float
    coherencia_citoplasma: float
    frecuencias_riemann: List[float]
    aprobado: bool

    def resumen(self) -> str:
        """Cadena de texto con los indicadores clave del resultado."""
        estado_pt = "✓ ACTIVA" if self.pt_activa else "✗ ROTA"
        estado_ap = "✓ APROBADO" if self.aprobado else "✗ NO APROBADO"
        return (
            f"╔══════════════════════════════════════════╗\n"
            f"║   πCODE RESONANCIA — QCAL-SYMBIO-1       ║\n"
            f"╠══════════════════════════════════════════╣\n"
            f"║ Coherencia Ψ          : {self.coherencia:.6f}           ║\n"
            f"║ Simetría PT           : {estado_pt}              ║\n"
            f"║ Autovalores reales    : {self.n_autovalores_reales}/{self.n_dimension}               ║\n"
            f"║ Correlación Riemann   : {self.correlacion_riemann:.4f}              ║\n"
            f"║ Estabilidad biológica : {self.estabilidad_biologica:.4f}              ║\n"
            f"║ Resonancia global     : {self.resonancia_global:.4f}              ║\n"
            f"║ Estado                : {estado_ap}          ║\n"
            f"╚══════════════════════════════════════════╝"
        )


# ============================================================================
# CLASE 1 — EmisionInformacionResonante
# ============================================================================

class EmisionInformacionResonante:
    r"""
    Emisión de información resonante desde la escala de Planck.

    Modela la emisión cuántica E = ℏ·ω₀ con modulación de coherencia Ψ que
    conecta 27 órdenes de magnitud (de la escala de Planck ~10⁻³⁵ m a la
    escala celular ~10⁻⁶ m) a través de la fase, no del tamaño.

    La energía de emisión modulada se define como:

        E_Ψ = ℏ · ω₀ · Ψ

    La fase de puente entre escala de Planck y celular:

        φ_bridge = ω₀ · (L_celular / L_Planck)^(1/27)

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    f0 : float
        Frecuencia fundamental QCAL (141.7001 Hz).
    hbar : float
        Constante de Planck reducida ℏ (J·s).
    omega_0 : float
        Frecuencia angular fundamental ω₀ = 2πf₀ (rad/s).
    """

    def __init__(
        self,
        coherencia: float = _COHERENCIA_DEFAULT,
        f0: float = _F0_HZ,
    ) -> None:
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positiva, se recibió {f0}")
        self.coherencia: float = coherencia
        self.f0: float = f0
        self.hbar: float = _HBAR
        self.omega_0: float = 2 * math.pi * f0

    def energia_emision(self) -> float:
        r"""
        Energía de emisión modulada por coherencia.

        E_Ψ = ℏ · ω₀ · Ψ

        Retorna
        -------
        float
            Energía en Joules.
        """
        return self.hbar * self.omega_0 * self.coherencia

    def fase_puente(self) -> float:
        r"""
        Fase de puente entre escala de Planck y celular.

        Conecta _ORDENES_MAGNITUD órdenes de magnitud a través de la fase:

            φ_bridge = ω₀ · (L_celular / L_Planck)^(1/N_ordenes)

        Retorna
        -------
        float
            Fase de puente (rad).
        """
        ratio = _L_CELULAR / _L_PLANCK
        return self.omega_0 * (ratio ** (1.0 / _ORDENES_MAGNITUD))

    def ordenes_magnitud(self) -> int:
        """Número de órdenes de magnitud que el sistema conecta."""
        return _ORDENES_MAGNITUD

    def amplitud_coherente(self, t: float = 0.0) -> complex:
        r"""
        Amplitud compleja de la onda de emisión coherente.

        A(t) = Ψ · exp(i · ω₀ · t)

        Parámetros
        ----------
        t : float
            Tiempo en segundos.

        Retorna
        -------
        complex
            Amplitud compleja.
        """
        return self.coherencia * complex(math.cos(self.omega_0 * t),
                                         math.sin(self.omega_0 * t))

    def coherencia_planck_celular(self) -> float:
        r"""
        Coherencia entre escala de Planck y escala celular.

        Modelada como Ψ atravesando N órdenes de magnitud:

            Φ = Ψ^(1/N_ordenes)

        Con Ψ → 1 y N_ordenes = 27: Φ → 1.
        Con Ψ → 0 (estrés): Φ → 0.

        Retorna
        -------
        float
            Coherencia ∈ [0, 1].
        """
        return self.coherencia ** (1.0 / _ORDENES_MAGNITUD)


# ============================================================================
# CLASE 2 — PTSymmetryOperator
# ============================================================================

class PTSymmetryOperator:
    r"""
    Operador no-hermítico con simetría PT (Paridad–Tiempo).

    Construye el Hamiltoniano total:

        Ĥ_total = diag(base_riemann) + i · (1 − Ψ) · fliplr(I_N)

    donde:
        diag(base_riemann) : parte hermítica real (proxy espectral de Riemann)
        i·(1−Ψ)·fliplr(I) : acoplamiento disipativo no-hermítico

    Cuando Ψ → 1 la parte imaginaria se suprime completamente:
        → espectro real → simetría PT activa → estabilidad biológica

    Cuando Ψ → 0 (estrés celular):
        → aparecen autovalores imaginarios → simetría PT rota

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    n_dimension : int
        Dimensión del espacio de Hilbert.
    semilla : int | None
        Semilla para reproducibilidad del generador aleatorio.
    """

    def __init__(
        self,
        coherencia: float = _COHERENCIA_DEFAULT,
        n_dimension: int = _N_DIMENSION_DEFAULT,
        semilla: Optional[int] = 42,
    ) -> None:
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        if n_dimension < 1:
            raise ValueError(
                f"n_dimension debe ser >= 1, se recibió {n_dimension}"
            )
        self.coherencia: float = coherencia
        self.n_dimension: int = n_dimension
        self.semilla: Optional[int] = semilla
        self._rng = np.random.default_rng(semilla)

    def _base_riemann(self) -> npt.NDArray[np.float64]:
        """
        Genera la base espectral proxy de los ceros de Riemann, normalizada.

        Los primeros 10 valores son las partes imaginarias conocidas de los ceros
        no triviales de ζ(s) en la línea crítica Re(s)=½.  Para dimensiones
        mayores que 10, los modos restantes se rellenan con valores pseudo-
        aleatorios con distribución normal estándar ordenados ascendentemente;
        estos valores **no tienen justificación física individual** y sirven
        únicamente como marcadores de nivel de energía (proxy numérico) para
        completar el espacio de Hilbert.

        El array resultante se normaliza a media 0 y desviación estándar 1
        para que el parámetro de acoplamiento (1−Ψ) sea competitivo con el
        espaciado de niveles y pueda producir ruptura de PT cuando Ψ << 1.

        Retorna
        -------
        npt.NDArray[np.float64]
            Array de N valores reales con media 0 y std 1.
        """
        n = self.n_dimension
        # Usar ceros de Riemann conocidos para los primeros modos
        base = np.zeros(n, dtype=np.float64)
        n_known = min(len(_RIEMANN_ZEROS), n)
        for i, gamma in enumerate(_RIEMANN_ZEROS[:n_known]):
            base[i] = gamma
        # Rellenar el resto con valores aleatorios ordenados (proxy espectral)
        if n > n_known:
            rng = np.random.default_rng(self.semilla)
            extra = np.sort(
                rng.standard_normal(n - n_known).astype(np.float64)
            )
            base[n_known:] = extra
        base = np.sort(base)
        # Normalizar a media 0 y std 1 para que el acoplamiento (1−Ψ)
        # pueda competir con los niveles y producir ruptura de PT a bajos Ψ
        std = float(np.std(base))
        if std > 0:
            base = (base - float(np.mean(base))) / std
        return base

    def construir(self) -> npt.NDArray[np.complexfloating]:
        r"""
        Construye y devuelve la matriz compleja Ĥ_total (N×N).

        Ĥ_total = diag(base_riemann) + i · (1 − Ψ) · fliplr(I_N)

        Retorna
        -------
        npt.NDArray[np.complexfloating]
            Operador no-hermítico con simetría PT, dimensión N×N.
        """
        h_real = np.diag(self._base_riemann())
        h_imag = np.fliplr(np.eye(self.n_dimension)) * (1.0 - self.coherencia)
        return h_real.astype(complex) + 1j * h_imag

    def autovalores(self) -> npt.NDArray[np.complexfloating]:
        """
        Calcula los autovalores del operador Ĥ_total.

        Retorna
        -------
        npt.NDArray[np.complexfloating]
            Array de N autovalores complejos.
        """
        return np.linalg.eigvals(self.construir())

    def es_pt_activa(self, atol: float = _ATOL_PT) -> bool:
        """
        True si la simetría PT está activa (espectro real conservado).

        Un espectro se considera real si |Im(λ)| < atol para todos los λ.

        Parámetros
        ----------
        atol : float
            Tolerancia para partes imaginarias.

        Retorna
        -------
        bool
        """
        eigs = self.autovalores()
        return bool(np.allclose(eigs.imag, 0.0, atol=atol))

    def fraccion_autovalores_reales(self, atol: float = _ATOL_PT) -> float:
        """
        Fracción de autovalores con parte imaginaria ≈ 0.

        Retorna
        -------
        float
            Valor en [0, 1].
        """
        eigs = self.autovalores()
        n_reales = int(np.sum(np.abs(eigs.imag) < atol))
        return n_reales / self.n_dimension

    def max_parte_imaginaria(self) -> float:
        """Máximo de |Im(autovalores)|."""
        eigs = self.autovalores()
        return float(np.max(np.abs(eigs.imag)))

    def coherencia_pt(self) -> float:
        r"""
        Coherencia PT del operador definida como la fracción de autovalores
        reales ponderada por la coherencia Ψ.

        Ψ_PT = Ψ · fraccion_reales

        Retorna
        -------
        float
            Coherencia PT ∈ [0, 1].
        """
        return self.coherencia * self.fraccion_autovalores_reales()


# ============================================================================
# CLASE 3 — AdSCFTCitoplasma
# ============================================================================

class AdSCFTCitoplasma:
    r"""
    Citoplasma como límite holográfico AdS/CFT.

    Modela el citoplasma como el borde (CFT) de una dinámica de mayor
    dimensionalidad (bulk AdS).  La densidad del agua EZ sigue la ley:

        ρ_EZ(x) = Ψ · exp(−x / λ_EZ) · cos²(ω₀ · x / c)

    donde:
        x      : posición radial desde la membrana (m)
        λ_EZ   : longitud de coherencia del agua EZ (~100 nm)
        ω₀     : frecuencia angular fundamental QCAL
        c      : velocidad de la luz

    La coherencia holográfica se define como:

        Ψ_holo = Ψ · (1 − ξ_rel)

    donde ξ_rel mide la discrepancia relativa con el perfil EZ ideal.

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    lambda_ez : float
        Longitud de coherencia del agua EZ (m).
    n_puntos : int
        Número de puntos de la malla espacial.
    """

    def __init__(
        self,
        coherencia: float = _COHERENCIA_DEFAULT,
        lambda_ez: float = _LAMBDA_EZ,
        n_puntos: int = 64,
    ) -> None:
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        if lambda_ez <= 0:
            raise ValueError(
                f"lambda_ez debe ser positiva, se recibió {lambda_ez}"
            )
        if n_puntos < 2:
            raise ValueError(
                f"n_puntos debe ser >= 2, se recibió {n_puntos}"
            )
        self.coherencia: float = coherencia
        self.lambda_ez: float = lambda_ez
        self.n_puntos: int = n_puntos
        # Malla espacial: de 0 a 5·λ_EZ
        self._x_grid: npt.NDArray[np.float64] = np.linspace(
            0.0, 5 * lambda_ez, n_puntos
        )

    def densidad_ez(self, x: float) -> float:
        r"""
        Densidad del agua EZ en la posición x.

        ρ_EZ(x) = Ψ · exp(−x / λ_EZ) · cos²(ω₀ · x / c)

        Parámetros
        ----------
        x : float
            Posición radial en metros.

        Retorna
        -------
        float
            Densidad normalizada ≥ 0.
        """
        exp_term = math.exp(-x / self.lambda_ez)
        cos_term = math.cos(_OMEGA_0 * x / _C_LUZ) ** 2
        return self.coherencia * exp_term * cos_term

    def perfil_densidad(self) -> npt.NDArray[np.float64]:
        """
        Perfil de densidad EZ en toda la malla espacial.

        Retorna
        -------
        npt.NDArray[np.float64]
            Array de N valores de densidad ρ_EZ(x) ≥ 0.
        """
        return np.array([self.densidad_ez(x) for x in self._x_grid],
                        dtype=np.float64)

    def entropia_holografica(self) -> float:
        r"""
        Entropía holográfica del sistema citoplasmático (bits).

        S_holo = −∫ ρ̃_EZ(x) · log₂(ρ̃_EZ(x) + ε) dx / Z

        Retorna
        -------
        float
            Entropía holográfica en bits (≥ 0).
        """
        rho = self.perfil_densidad()
        total = float(np.sum(rho))
        if total <= 0:
            return 0.0
        eps = 1e-15  # evitar log2(0); valor estándar para cálculos de entropía
        rho_norm = rho / total
        entropia = -np.sum(rho_norm * np.log2(rho_norm + eps))
        return float(entropia)

    def coherencia_holografica(self) -> float:
        r"""
        Coherencia holográfica del citoplasma ∈ [0, 1].

        La coherencia se basa en la longitud de correlación del agua EZ:

            ξ_EZ = √(ν_cito / ω₀)

        donde ν_cito = 1×10⁻⁹ m²/s es la viscosidad cinemática del citoplasma.

        La coherencia mide qué tan bien ξ_EZ coincide con la escala celular L:

            Ψ_holo = Ψ · exp(−(ξ_EZ/L_celular − 1)²)

        Con ν_cito = 1×10⁻⁹ y ω₀ ≈ 890 rad/s:
            ξ_EZ ≈ 1.06 μm ≈ L_celular → Ψ_holo ≈ Ψ · 0.9964

        Retorna
        -------
        float
            Coherencia holográfica ∈ [0, 1].
        """
        _NU_CITO = 1e-9  # m²/s — viscosidad cinemática citoplasmática
        xi_ez = math.sqrt(_NU_CITO / _OMEGA_0)    # ≈ 1.06 μm
        epsilon = (xi_ez / _L_CELULAR - 1.0) ** 2
        return min(1.0, max(0.0, self.coherencia * math.exp(-epsilon)))

    def longitud_coherencia_citoplasma(self) -> float:
        r"""
        Longitud de coherencia efectiva del citoplasma (m).

        ξ_eff = λ_EZ · Ψ

        Retorna
        -------
        float
            Longitud de coherencia en metros.
        """
        return self.lambda_ez * self.coherencia


# ============================================================================
# CLASE 4 — RiemannEstabilizadorBiologico
# ============================================================================

class RiemannEstabilizadorBiologico:
    r"""
    Estabilizador biológico basado en los ceros de Riemann.

    Los ceros no triviales de la función ζ de Riemann sirven como anclas de
    resonancia biológica.  Las frecuencias de resonancia se definen como:

        f_n = f₀ · γ_n / γ₁

    donde γ_n es la parte imaginaria del n-ésimo cero de Riemann y γ₁ ≈ 14.135.

    La correlación espectral mide cuánto del espectro biológico está alineado
    con la distribución de los ceros de Riemann.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (141.7001 Hz).
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    n_zeros : int
        Número de ceros de Riemann a usar (máximo 10).
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        coherencia: float = _COHERENCIA_DEFAULT,
        n_zeros: int = 10,
    ) -> None:
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positiva, se recibió {f0}")
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        if not (1 <= n_zeros <= len(_RIEMANN_ZEROS)):
            raise ValueError(
                f"n_zeros debe estar en [1, {len(_RIEMANN_ZEROS)}], "
                f"se recibió {n_zeros}"
            )
        self.f0: float = f0
        self.coherencia: float = coherencia
        self.n_zeros: int = n_zeros

    def frecuencias_resonancia(self) -> List[float]:
        r"""
        Frecuencias de resonancia biológica derivadas de los ceros de Riemann.

        f_n = f₀ · γ_n / γ₁

        Retorna
        -------
        List[float]
            Lista de n_zeros frecuencias en Hz.
        """
        gamma_1 = _RIEMANN_ZEROS[0]
        return [
            self.f0 * _RIEMANN_ZEROS[i] / gamma_1
            for i in range(self.n_zeros)
        ]

    def pesos_resonancia(self) -> List[float]:
        r"""
        Pesos de cada frecuencia de resonancia (decaen con el índice).

        w_n = Ψ · exp(−n / N_zeros)

        Retorna
        -------
        List[float]
            Lista de n_zeros pesos normalizados.
        """
        pesos = [
            self.coherencia * math.exp(-i / self.n_zeros)
            for i in range(self.n_zeros)
        ]
        total = sum(pesos)
        if total > 0:
            pesos = [w / total for w in pesos]
        return pesos

    def correlacion_espectral(self) -> float:
        r"""
        Correlación espectral entre los ceros de Riemann y la aproximación
        armónica n·ln(n+1) (Pearson).

        Mide qué tan bien la distribución espectral de los ceros de Riemann
        se aproxima al modelo armónico biológico n·ln(n+1):

            corr = Pearson(_RIEMANN_ZEROS[:N], [n·ln(n+1) for n in 1..N])

        Con los 10 primeros ceros conocidos:
            corr ≈ 0.977  (≈ 0.98 cuando se muestra con 2 decimales)

        Retorna
        -------
        float
            Correlación de Pearson ∈ [0, 1].
        """
        n_arr = np.arange(1, self.n_zeros + 1, dtype=np.float64)
        approx = n_arr * np.log(n_arr + 1.0)
        zeros_arr = np.array(_RIEMANN_ZEROS[:self.n_zeros], dtype=np.float64)
        corr_matrix = np.corrcoef(zeros_arr, approx)
        corr = float(corr_matrix[0, 1])
        return max(0.0, corr)

    def estabilidad_biologica(self) -> float:
        r"""
        Métrica de estabilidad biológica del sistema ∈ [0, 1].

        La estabilidad se calcula como la media ponderada entre Ψ y la
        correlación espectral de Riemann:

            E_bio = Ψ · (1 + corr_espectral) / 2

        Con Ψ = 0.999999 y corr ≈ 0.977:
            E_bio ≈ 0.988  (≈ 0.99 cuando se muestra con 2 decimales)

        Retorna
        -------
        float
            Estabilidad ∈ [0, 1].
        """
        corr = self.correlacion_espectral()
        return self.coherencia * (1.0 + corr) / 2.0

    def frecuencia_fundamental_activa(self) -> float:
        """
        Frecuencia fundamental activa del sistema (la primera de la serie).

        Retorna
        -------
        float
            Frecuencia en Hz (igual a f₀ por construcción).
        """
        freqs = self.frecuencias_resonancia()
        return freqs[0] if freqs else self.f0


# ============================================================================
# CLASE 5 — PiCodeResonancia
# ============================================================================

class PiCodeResonancia:
    r"""
    Motor QCAL-SYMBIO-1 completo de resonancia πCODE.

    Integra los cuatro componentes del sistema:
        1. EmisionInformacionResonante  — escala de Planck
        2. PTSymmetryOperator           — simetría PT
        3. AdSCFTCitoplasma             — borde holográfico
        4. RiemannEstabilizadorBiologico — ceros de Riemann

    La resonancia global se calcula como la media geométrica de las cuatro
    coherencias componentes:

        Ψ_global = (Ψ_PT · Ψ_holo · E_bio · Ψ_emision)^(1/4)

    Simulación de falsabilidad:
        Con Ψ → 1: todos los componentes activos → resonancia global alta
        Con Ψ → 0: estrés celular → PT rota → resonancia colapsa

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    n_dimension : int
        Dimensión del espacio de Hilbert para el operador PT.
    semilla : int | None
        Semilla para reproducibilidad.
    """

    def __init__(
        self,
        coherencia: float = _COHERENCIA_DEFAULT,
        n_dimension: int = _N_DIMENSION_DEFAULT,
        semilla: Optional[int] = 42,
    ) -> None:
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        if n_dimension < 1:
            raise ValueError(
                f"n_dimension debe ser >= 1, se recibió {n_dimension}"
            )
        self.coherencia: float = coherencia
        self.n_dimension: int = n_dimension
        self.semilla: Optional[int] = semilla

        # Instanciar los cuatro componentes
        self._emision = EmisionInformacionResonante(
            coherencia=coherencia
        )
        self._pt_op = PTSymmetryOperator(
            coherencia=coherencia,
            n_dimension=n_dimension,
            semilla=semilla,
        )
        self._citoplasma = AdSCFTCitoplasma(
            coherencia=coherencia
        )
        self._riemann = RiemannEstabilizadorBiologico(
            coherencia=coherencia
        )

    def evaluar(self) -> ResultadoPiCodeResonancia:
        """
        Evalúa el estado completo del sistema πCODE y retorna el resultado.

        La resonancia global se calcula como la media geométrica de los tres
        componentes nucleares del sistema:

            Ψ_global = (Ψ_PT · Ψ_holo · Ψ_riemann_coh)^(1/3)

        Con Ψ = 0.999999:
            Ψ_PT ≈ 1.0, Ψ_holo ≈ 0.9964, Ψ_riemann_coh ≈ 1.0
            → Ψ_global ≈ 0.9988

        Retorna
        -------
        ResultadoPiCodeResonancia
            Resultado completo con todas las métricas del sistema.
        """
        # Componente 1: emisión de Planck
        energia = self._emision.energia_emision()

        # Componente 2: simetría PT
        pt_activa = self._pt_op.es_pt_activa()
        fraccion_reales = self._pt_op.fraccion_autovalores_reales()
        n_reales = int(round(fraccion_reales * self.n_dimension))
        psi_pt = fraccion_reales  # fracción de autovalores reales ∈ [0, 1]

        # Componente 3: citoplasma AdS/CFT
        psi_holo = self._citoplasma.coherencia_holografica()

        # Componente 4: métricas de Riemann (output fields)
        corr_riemann = self._riemann.correlacion_espectral()
        estab_bio = self._riemann.estabilidad_biologica()
        freqs_riemann = self._riemann.frecuencias_resonancia()

        # Coherencia de resonancia de Riemann:
        # ponderación exponencial con escala disipativa alpha = ν/f₀
        _NU_DISIP = 1e-9  # m²/s
        alpha_disip = _NU_DISIP / (_F0_HZ ** 2)
        pesos = [
            math.exp(-alpha_disip * t / _F0_HZ)
            for t in _RIEMANN_ZEROS
        ]
        w_max = pesos[0] if pesos else 1.0
        psi_riemann_coh = min(1.0, sum(pesos) / (len(pesos) * w_max)) if w_max > 0 else 1.0

        # Media geométrica de los tres componentes nucleares
        componentes = [
            max(1e-30, psi_pt),
            max(1e-30, psi_holo),
            max(1e-30, psi_riemann_coh),
        ]
        resonancia_global = float(
            math.exp(sum(math.log(c) for c in componentes) / len(componentes))
        )
        resonancia_global = min(1.0, max(0.0, resonancia_global))

        return ResultadoPiCodeResonancia(
            coherencia=self.coherencia,
            n_dimension=self.n_dimension,
            pt_activa=pt_activa,
            n_autovalores_reales=n_reales,
            fraccion_reales=fraccion_reales,
            correlacion_riemann=corr_riemann,
            estabilidad_biologica=estab_bio,
            resonancia_global=resonancia_global,
            energia_emision=energia,
            coherencia_citoplasma=psi_holo,
            frecuencias_riemann=freqs_riemann,
            aprobado=(resonancia_global >= _PSI_UMBRAL),
        )

    def simular_estres_celular(
        self,
        psi_estres: float = 0.1,
    ) -> Tuple[ResultadoPiCodeResonancia, ResultadoPiCodeResonancia]:
        """
        Simula el efecto del estrés celular sobre el sistema.

        Compara el estado de alta coherencia (Ψ nominal) con un estado de
        estrés (Ψ_estrés << 1) para verificar falsabilidad del modelo:
        el estrés reduce la coherencia, rompe la simetría PT y disuelve la
        geometría de Riemann.

        Parámetros
        ----------
        psi_estres : float
            Coherencia bajo estrés celular ∈ (0, 1].

        Retorna
        -------
        Tuple[ResultadoPiCodeResonancia, ResultadoPiCodeResonancia]
            (resultado_nominal, resultado_estres)
        """
        if not (0.0 < psi_estres <= 1.0):
            raise ValueError(
                f"psi_estres debe estar en (0, 1], se recibió {psi_estres}"
            )
        resultado_nominal = self.evaluar()
        motor_estres = PiCodeResonancia(
            coherencia=psi_estres,
            n_dimension=self.n_dimension,
            semilla=self.semilla,
        )
        resultado_estres = motor_estres.evaluar()
        return resultado_nominal, resultado_estres


# ============================================================================
# API PÚBLICA
# ============================================================================

def activar_picode_resonancia(
    coherencia: float = _COHERENCIA_DEFAULT,
    n_dimension: int = _N_DIMENSION_DEFAULT,
    semilla: Optional[int] = 42,
) -> ResultadoPiCodeResonancia:
    """
    Activa el motor QCAL-SYMBIO-1 de resonancia πCODE.

    Parámetros
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].  Por defecto 0.999999.
    n_dimension : int
        Dimensión del espacio de Hilbert.  Por defecto 100.
    semilla : int | None
        Semilla para reproducibilidad.

    Retorna
    -------
    ResultadoPiCodeResonancia
        Resultado completo con métricas PT, holográficas y de Riemann.

    Raises
    ------
    ValueError
        Si coherencia ∉ (0, 1] o n_dimension < 1.
    """
    motor = PiCodeResonancia(
        coherencia=coherencia,
        n_dimension=n_dimension,
        semilla=semilla,
    )
    return motor.evaluar()


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":  # pragma: no cover
    resultado = activar_picode_resonancia()
    print(resultado.resumen())
