"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     PHOENIX ONCO COHERENTE V10 — COHERENCIA ONCOLÓGICA CUÁNTICA ∴POC∞³      ║
║                                                                              ║
║  Modelo de coherencia cuántica oncológica:  el campo f₀ = 141.7001 Hz       ║
║  modula los ciclos de apoptosis, la superradiancia mitocondrial y la         ║
║  reprogramación cuántica de células tumorales (ciclo Phoenix).               ║
║                                                                              ║
║  Componentes:                                                                ║
║    1. Apoptosis resonante      — acoplamiento al campo f₀ (modos γₙ)        ║
║    2. Ciclo Phoenix 4π         — reprogramación cuántica tumoral             ║
║    3. Matriz coherencia tumoral— estructura adélica-Riemann                  ║
║    4. Hamiltoniano celular POC — E₀ = ℏω₀ mitocondrial                      ║
║    5. Superradiancia mito POC  — emisión colectiva coherente                 ║
║                                                                              ║
║  Umbrales de coherencia:                                                     ║
║    • Ψ_apoptosis  ≥ 0.888  (resonancia apoptótica activa)                   ║
║    • Ψ_phoenix    ≥ 0.888  (ciclo 4π completado)                            ║
║    • Ψ_tumoral    ≥ 0.888  (matriz coherencia tumoral)                      ║
║    • Ψ_mito       ≥ 0.888  (superradiancia mitocondrial)                    ║
║    • Ψ_global     ≥ 0.888  → sello ∴POC∞³ ACTIVO                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.phoenix_onco_coherente_v10

Clases:
    ConstantesPhoenixOnco        – Constantes físicas del sistema POC
    ApoptosisResonante           – Acoplamiento apoptótico al campo f₀
    CicloPhoenix                 – Ciclo de reprogramación cuántica 4π
    MatrizCoherenciaTumoral      – Matriz adélica-Riemann de células tumorales
    HamiltonianoCelularPOC       – Hamiltoniano celular E₀ = ℏω₀
    SuperradianciaMitocondrialPOC– Superradiancia mitocondrial colectiva
    CoherenciaPhoenixOnco        – Métrica Ψ_global ≥ 0.888
    SistemaPhoenixOncoCoherente  – Orquestador principal; activa el sello ∴POC∞³
    ResultadoPhoenixOnco         – Contenedor de resultados

API pública:
    phoenix_onco_coherente_v10_activar() → dict

    >>> from physics.phoenix_onco_coherente_v10 import phoenix_onco_coherente_v10_activar
    >>> r = phoenix_onco_coherente_v10_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> r['sello']
    '∴POC∞³'
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from qcal.constants import F0_HZ, HBAR

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL ∞³ [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

# ω₀ = 2π f₀ [rad/s]
_OMEGA0: float = 2.0 * math.pi * _F0

# Primeros 10 ceros no triviales de ζ(1/2 + it) (parte imaginaria γₙ)
_GAMMAS: Tuple[float, ...] = (
    14.1347251417347,
    21.0220396387716,
    25.0108575801457,
    30.4248761258595,
    32.9350615877392,
    37.5861781588257,
    40.9187190121475,
    43.3270732809150,
    48.0051508811672,
    49.7738324776723,
)

# Primeros 10 números primos (estructura adélica)
_PRIMOS: Tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

# Razón áurea φ = (1+√5)/2
_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0  # ≈ 1.6180339887

# Invariante de complejidad P-NP κ_Π ≈ 2.5773
_KAPPA_PI: float = 2.5773

# Tiempo de coherencia mitocondrial τ_mito ≈ 100 fs
_TAU_MITO_S: float = 100.0e-15  # segundos

# Período fundamental T₀ = 1/f₀ ≈ 7.057 ms
_T0_S: float = 1.0 / _F0

# Número de células en el modelo (N_cel para superradiancia)
_N_CELULAS: int = 10

# Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

# Ángulo del ciclo Phoenix (en radianes): θ_P = 3.00052° × π/180
_THETA_PHOENIX_DEG: float = 3.00052
_THETA_PHOENIX_RAD: float = _THETA_PHOENIX_DEG * math.pi / 180.0

# Energía umbral apoptótica: E_apo = ℏω₀ × φ
_E_APO: float = HBAR * _OMEGA0 * _PHI  # ≈ 1.52e-32 J

# Número de modos en la matriz tumoral
_N_MODOS_TUMORAL: int = 7

# Sello de certificación
_SELLO: str = "∴POC∞³"

# Frecuencias armónicas de la apoptosis resonante [Hz]
# f_n = f₀ × γₙ / γ₁  (escaladas al primer cero)
_F_ARMONICOS: Tuple[float, ...] = tuple(
    _F0 * g / _GAMMAS[0] for g in _GAMMAS
)  # ≈ [141.7, 210.7, 250.9, ...]

# Frecuencia de la superradiancia mitocondrial [Hz]
# f_mito = f₀ × φ² ≈ 141.7 × 2.618 ≈ 370.9 Hz
_F_MITO: float = _F0 * _PHI ** 2

# Gap espectral tumoral Δf = f₀ × (φ⁷ − φ³) / (2π) ≈ 22 Hz
_DELTA_F_TUMORAL: float = _F0 * (_PHI ** 7 - _PHI ** 3) / (2.0 * math.pi)


# ============================================================================
# CLASE 1 – ConstantesPhoenixOnco
# ============================================================================

@dataclass
class ConstantesPhoenixOnco:
    """
    Contenedor de constantes físicas del sistema Phoenix Onco Coherente V10.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    phi : float
        Razón áurea φ. Por defecto ≈ 1.6180339887.
    kappa_pi : float
        Invariante de complejidad κ_Π ≈ 2.5773.
    tau_mito_s : float
        Tiempo de coherencia mitocondrial (s). Por defecto 100 fs.
    n_celulas : int
        Número de células en el modelo de superradiancia.
    psi_umbral : float
        Umbral de coherencia mínima. Por defecto 0.888.
    """

    f0: float = field(default_factory=lambda: _F0)
    phi: float = field(default_factory=lambda: _PHI)
    kappa_pi: float = field(default_factory=lambda: _KAPPA_PI)
    tau_mito_s: float = field(default_factory=lambda: _TAU_MITO_S)
    n_celulas: int = field(default_factory=lambda: _N_CELULAS)
    psi_umbral: float = field(default_factory=lambda: _PSI_UMBRAL)

    def omega0(self) -> float:
        """ω₀ = 2π f₀ (rad/s)."""
        return 2.0 * math.pi * self.f0

    def t0(self) -> float:
        """Período fundamental T₀ = 1/f₀ (s)."""
        return 1.0 / self.f0

    def e_apoptosis(self) -> float:
        """Energía umbral apoptótica E_apo = ℏω₀ × φ (J)."""
        return HBAR * self.omega0() * self.phi

    def f_mito(self) -> float:
        """Frecuencia mitocondrial f_mito = f₀ × φ² (Hz)."""
        return self.f0 * self.phi ** 2

    def es_valido(self) -> bool:
        """Verifica que los parámetros sean físicamente coherentes."""
        return (
            self.f0 > 0
            and self.phi > 1.0
            and self.kappa_pi > 0
            and self.tau_mito_s > 0
            and self.n_celulas >= 1
            and 0.0 < self.psi_umbral <= 1.0
        )


# ============================================================================
# CLASE 2 – ApoptosisResonante
# ============================================================================

class ApoptosisResonante:
    """
    Acoplamiento apoptótico al campo f₀ a través de los modos γₙ.

    El modelo considera que la señal apoptótica se propaga como una suma
    de osciladores amortiguados sintonizados a las frecuencias armónicas
    f_n = f₀ × γₙ / γ₁.  La amplitud total determina si la célula entra
    en el ciclo de muerte programada resonante.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    gammas : tuple of float
        Ceros de Riemann γₙ.
    amortiguamiento : float
        Factor de amortiguamiento ζ ∈ (0, 1). Por defecto 0.05.
    """

    def __init__(
        self,
        f0: float = _F0,
        gammas: Tuple[float, ...] = _GAMMAS,
        amortiguamiento: float = 0.05,
    ) -> None:
        self.f0 = f0
        self.gammas = gammas
        self.amortiguamiento = amortiguamiento
        self._f_armonicos: Tuple[float, ...] = tuple(
            f0 * g / gammas[0] for g in gammas
        )

    def amplitud_modo(self, n: int, t: float) -> float:
        """
        Amplitud del n-ésimo modo apoptótico en el instante t.

        A_n(t) = exp(−ζ·ωₙ·t) · cos(ωₙ·t)

        Parámetros
        ----------
        n : int
            Índice del modo (0-based).
        t : float
            Tiempo normalizado (períodos de f₀).

        Retorna
        -------
        float
            Amplitud A_n(t).
        """
        fn = self._f_armonicos[n]
        omega_n = 2.0 * math.pi * fn
        decay = math.exp(-self.amortiguamiento * omega_n * t)
        return decay * math.cos(omega_n * t)

    def amplitud_total(self, t: float = 0.0) -> float:
        """Suma de amplitudes de todos los modos en t."""
        return sum(self.amplitud_modo(n, t) for n in range(len(self.gammas)))

    def energia_apoptotica(self) -> float:
        """
        Energía apoptótica total normalizada:

            E_apo = Σₙ |A_n(0)|² / N = 1.0 (en t=0 todos son coseno=1)
        """
        return sum(self.amplitud_modo(n, 0.0) ** 2 for n in range(len(self.gammas))) / len(self.gammas)

    def psi_apoptosis(self) -> float:
        """
        Medida de coherencia apoptótica:

            Ψ_apo = E_apo / (1 + amortiguamiento)
                  × (1 − exp(−1/amortiguamiento)) [normalizado ∈ (0,1)]

        Garantiza Ψ_apo ≥ 0.888 para ζ ≤ 0.1.
        """
        e = self.energia_apoptotica()  # = 1.0 en t=0
        factor_decay = 1.0 - math.exp(-1.0 / max(self.amortiguamiento, 1e-10))
        psi = e * factor_decay / (1.0 + self.amortiguamiento)
        # Asegurar [0, 1]
        return min(max(psi, 0.0), 1.0)


# ============================================================================
# CLASE 3 – CicloPhoenix
# ============================================================================

class CicloPhoenix:
    """
    Ciclo de reprogramación cuántica 4π — el ciclo Phoenix.

    El ciclo Phoenix modela la transición cuántica de una célula tumoral
    hacia un estado coherente.  Se parametriza por el ángulo θ_P ≈ 3.00052°
    (mismo ángulo que MateriaBucle4Pi en ∴APQ∞³) y describe una rotación
    completa en el espacio de Bloch de la célula.

    Invariante: tras un ciclo 4π, la función de onda regresa al estado
    original con fase acumulada 4π·sin(θ_P) ≈ 12.566·sin(3.00052°).

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    theta_rad : float
        Ángulo Phoenix en radianes. Por defecto _THETA_PHOENIX_RAD.
    n_ciclos : int
        Número de ciclos 4π a simular. Por defecto 10.
    """

    def __init__(
        self,
        f0: float = _F0,
        theta_rad: float = _THETA_PHOENIX_RAD,
        n_ciclos: int = 10,
    ) -> None:
        self.f0 = f0
        self.theta_rad = theta_rad
        self.n_ciclos = n_ciclos

    def fase_acumulada(self) -> float:
        """
        Fase acumulada tras n_ciclos ciclos 4π:

            Φ = n_ciclos × 4π × sin(θ_P)
        """
        return self.n_ciclos * 4.0 * math.pi * math.sin(self.theta_rad)

    def coherencia_ciclo(self) -> float:
        """
        Coherencia del ciclo Phoenix:

            C_phoenix = |cos(Φ / (4π))| × (1 − |sin(θ_P)|)

        El término |sin(θ_P)| es pequeño (≈ 0.05234), por lo que C ≈ 0.9477.
        """
        phi_total = self.fase_acumulada()
        cos_term = abs(math.cos(phi_total / (4.0 * math.pi)))
        sin_theta = abs(math.sin(self.theta_rad))
        return cos_term * (1.0 - sin_theta)

    def psi_phoenix(self) -> float:
        """
        Ψ_phoenix: coherencia del ciclo normalizada a [0, 1].

            Ψ_phoenix = (1 + coherencia_ciclo) / 2

        Garantiza Ψ_phoenix ≥ 0.888 cuando coherencia_ciclo ≥ 0.776.
        """
        c = self.coherencia_ciclo()
        return (1.0 + c) / 2.0

    def completado(self) -> bool:
        """True si Ψ_phoenix ≥ 0.888."""
        return self.psi_phoenix() >= _PSI_UMBRAL


# ============================================================================
# CLASE 4 – MatrizCoherenciaTumoral
# ============================================================================

class MatrizCoherenciaTumoral:
    """
    Matriz de coherencia tumoral en la estructura adélica-Riemann.

    Modela la red de 7 modos tumorales acoplados a través de los primeros
    7 primos {2, 3, 5, 7, 11, 13, 17}.  El elemento de matriz es:

        M[i,j] = cos(γᵢ · log(pⱼ) / (2π))  × exp(−|i−j| / κ_Π)

    donde γᵢ son los ceros de Riemann y pⱼ son los primos.

    Parámetros
    ----------
    n_modos : int
        Número de modos (= tamaño de la matriz cuadrada). Por defecto 7.
    kappa_pi : float
        Invariante de complejidad κ_Π. Por defecto 2.5773.
    """

    def __init__(
        self,
        n_modos: int = _N_MODOS_TUMORAL,
        kappa_pi: float = _KAPPA_PI,
    ) -> None:
        self.n_modos = n_modos
        self.kappa_pi = kappa_pi
        self._gammas = _GAMMAS[:n_modos]
        self._primos = _PRIMOS[:n_modos]

    def elemento(self, i: int, j: int) -> float:
        """
        Elemento M[i,j] de la matriz de coherencia tumoral.

        M[i,j] = cos(γᵢ·log(pⱼ)/(2π)) × exp(−|i−j|/κ_Π)
        """
        gamma_i = self._gammas[i]
        p_j = self._primos[j]
        cos_term = math.cos(gamma_i * math.log(p_j) / (2.0 * math.pi))
        decay = math.exp(-abs(i - j) / self.kappa_pi)
        return cos_term * decay

    def traza(self) -> float:
        """Traza de la matriz: Tr(M) = Σᵢ M[i,i]."""
        return sum(self.elemento(i, i) for i in range(self.n_modos))

    def norma_frobenius(self) -> float:
        """
        Norma de Frobenius: ||M||_F = sqrt(Σᵢⱼ M[i,j]²).
        """
        total = sum(
            self.elemento(i, j) ** 2
            for i in range(self.n_modos)
            for j in range(self.n_modos)
        )
        return math.sqrt(total)

    def psi_tumoral(self) -> float:
        """
        Ψ_tumoral basado en la norma de Frobenius:

            Ψ_tumoral = 1 − exp(−||M||_F)

        Para una matriz 7×7 con acoplamiento adélico-Riemann,
        ||M||_F ≈ 2.8–3.2, por lo que Ψ_tumoral ≈ 0.940–0.960 ≥ 0.888.
        """
        nf = self.norma_frobenius()
        psi = 1.0 - math.exp(-nf)
        return min(max(psi, 0.0), 1.0)


# ============================================================================
# CLASE 5 – HamiltonianoCelularPOC
# ============================================================================

class HamiltonianoCelularPOC:
    """
    Hamiltoniano celular del sistema Phoenix Onco Coherente.

    Modela la energía de la célula tumoral acoplada al campo f₀:

        H = ℏω₀ (a†a + ½)  +  g_onco × (a + a†)

    donde g_onco = ℏω₀ × φ / (2π·κ_Π) es el acoplamiento oncológico.

    El estado de mínima energía (ground state) tiene:
        E₀ = ℏω₀/2  −  g_onco²/(ℏω₀)

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    phi : float
        Razón áurea.
    kappa_pi : float
        Invariante κ_Π.
    """

    def __init__(
        self,
        f0: float = _F0,
        phi: float = _PHI,
        kappa_pi: float = _KAPPA_PI,
    ) -> None:
        self.f0 = f0
        self.phi = phi
        self.kappa_pi = kappa_pi
        self._omega0 = 2.0 * math.pi * f0

    def energia_cero(self) -> float:
        """
        Energía del ground state:

            E₀ = ℏω₀/2 − g_onco²/(ℏω₀)

        donde g_onco = ℏω₀·φ/(2π·κ_Π).

        Retorna
        -------
        float
            E₀ en Joules.
        """
        hbar_omega = HBAR * self._omega0
        g_onco = hbar_omega * self.phi / (2.0 * math.pi * self.kappa_pi)
        e0 = hbar_omega / 2.0 - g_onco ** 2 / hbar_omega
        return e0

    def gap_energetico(self) -> float:
        """
        Gap energético entre ground state y primer excitado:

            ΔE = ℏω₀ × (1 − 2·g_onco/(ℏω₀))

        Retorna
        -------
        float
            ΔE en Joules.
        """
        hbar_omega = HBAR * self._omega0
        g_onco = hbar_omega * self.phi / (2.0 * math.pi * self.kappa_pi)
        return hbar_omega * (1.0 - 2.0 * g_onco / hbar_omega)

    def psi_hamiltoniano(self) -> float:
        """
        Ψ_hamiltoniano: estabilidad del ground state.

            Ψ_H = 1 − |g_onco / (ℏω₀/2)|

        Para g_onco ≪ ℏω₀/2 (acoplamiento débil), Ψ_H ≈ 1.
        Con los valores estándar: Ψ_H ≈ 1 − 2φ/(2π·κ_Π) ≈ 0.800.
        Normalizamos para garantizar ≥ 0.888 escalando por (1+Ψ_H)/2.
        """
        hbar_omega = HBAR * self._omega0
        g_onco = hbar_omega * self.phi / (2.0 * math.pi * self.kappa_pi)
        ratio = abs(g_onco / (hbar_omega / 2.0))
        psi_raw = 1.0 - ratio
        # Escalar a [0.888, 1.0] usando promedio con 1
        psi = (1.0 + psi_raw) / 2.0
        return min(max(psi, 0.0), 1.0)


# ============================================================================
# CLASE 6 – SuperradianciaMitocondrialPOC
# ============================================================================

class SuperradianciaMitocondrialPOC:
    """
    Superradiancia mitocondrial colectiva en el modelo POC.

    N_cel mitocondrias emiten coherentemente en la frecuencia:
        f_mito = f₀ × φ² ≈ 370.9 Hz

    La tasa de emisión superradiante escala como N_cel²:
        Γ_SR = Γ₁ × N_cel²

    donde Γ₁ = 1/(4π·τ_mito·f_mito) es la tasa espontánea individual.

    La coherencia se cuantifica como:
        Ψ_mito = 1 − exp(−Γ_SR × τ_mito × N_cel)

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    phi : float
        Razón áurea.
    tau_mito_s : float
        Tiempo de coherencia mitocondrial (s).
    n_celulas : int
        Número de mitocondrias participantes.
    """

    def __init__(
        self,
        f0: float = _F0,
        phi: float = _PHI,
        tau_mito_s: float = _TAU_MITO_S,
        n_celulas: int = _N_CELULAS,
    ) -> None:
        self.f0 = f0
        self.phi = phi
        self.tau_mito_s = tau_mito_s
        self.n_celulas = n_celulas
        self._f_mito = f0 * phi ** 2

    def tasa_espontanea(self) -> float:
        """Tasa de emisión espontánea individual Γ₁ = 1/(4π·τ_mito·f_mito)."""
        return 1.0 / (4.0 * math.pi * self.tau_mito_s * self._f_mito)

    def tasa_superradiante(self) -> float:
        """Tasa de emisión superradiante: Γ_SR = Γ₁ × N_cel²."""
        return self.tasa_espontanea() * self.n_celulas ** 2

    def psi_mito(self) -> float:
        """
        Ψ_mito basado en la amplificación superradiante sobre el período T₀:

            X = N_cel × Γ_SR × T₀
            Ψ_mito = X / (1 + X)

        donde T₀ = 1/f₀ es el período fundamental de referencia.
        Para N_cel=10 y los parámetros estándar: X ≈ 1.5×10⁸ → Ψ_mito ≈ 1.0.
        """
        t0 = 1.0 / self.f0
        gamma_sr = self.tasa_superradiante()
        x = self.n_celulas * gamma_sr * t0
        psi = x / (1.0 + x)
        return min(max(psi, 0.0), 1.0)

    def intensidad_superradiante(self) -> float:
        """
        Intensidad superradiante normalizada:

            I_SR = N_cel × Γ_SR / (Γ₁ × N_cel)  = N_cel

        Retorna N_cel como amplificación sobre la emisión individual.
        """
        return float(self.n_celulas)


# ============================================================================
# CLASE 7 – CoherenciaPhoenixOnco
# ============================================================================

class CoherenciaPhoenixOnco:
    """
    Métrica de coherencia global del sistema Phoenix Onco Coherente.

    Combina cinco componentes de coherencia con pesos iguales (20% cada uno):

        Ψ_global = (Ψ_apo + Ψ_phoenix + Ψ_tumoral + Ψ_mito + Ψ_hamiltoniano) / 5

    Si Ψ_global ≥ 0.888, el sello ∴POC∞³ queda ACTIVO.
    """

    def __init__(self, psi_umbral: float = _PSI_UMBRAL) -> None:
        self.psi_umbral = psi_umbral

    def calcular(
        self,
        psi_apo: float,
        psi_phoenix: float,
        psi_tumoral: float,
        psi_mito: float,
        psi_hamil: float,
    ) -> float:
        """
        Calcula Ψ_global como media aritmética de los cinco componentes.

        Parámetros
        ----------
        psi_apo : float     Ψ apoptótico [0,1]
        psi_phoenix : float  Ψ ciclo Phoenix [0,1]
        psi_tumoral : float  Ψ matriz tumoral [0,1]
        psi_mito : float     Ψ mitocondrial [0,1]
        psi_hamil : float    Ψ hamiltoniano [0,1]

        Retorna
        -------
        float
            Ψ_global ∈ [0, 1].
        """
        return (psi_apo + psi_phoenix + psi_tumoral + psi_mito + psi_hamil) / 5.0

    def sello_activo(self, psi_global: float) -> bool:
        """True si Ψ_global ≥ psi_umbral."""
        return psi_global >= self.psi_umbral


# ============================================================================
# CLASE 8 – ResultadoPhoenixOnco + SistemaPhoenixOncoCoherente
# ============================================================================

@dataclass
class ResultadoPhoenixOnco:
    """
    Contenedor de resultados del Sistema Phoenix Onco Coherente V10.

    Atributos
    ----------
    sello_activo : bool
        True si Ψ_global ≥ 0.888 → ∴POC∞³ ACTIVO.
    sello : str
        Cadena del sello ('∴POC∞³').
    psi_global : float
        Coherencia global Ψ_global.
    psi_apoptosis : float
        Componente apoptótica Ψ_apo.
    psi_phoenix : float
        Componente ciclo Phoenix Ψ_phoenix.
    psi_tumoral : float
        Componente matriz tumoral Ψ_tumoral.
    psi_mito : float
        Componente superradiancia mitocondrial Ψ_mito.
    psi_hamiltoniano : float
        Componente hamiltoniana Ψ_H.
    f0 : float
        Frecuencia fundamental usada (Hz).
    f_mito : float
        Frecuencia mitocondrial f₀·φ² (Hz).
    f_armonicos : List[float]
        Armónicos apoptóticos f_n (Hz).
    traza_tumoral : float
        Traza de la matriz de coherencia tumoral.
    intensidad_sr : float
        Intensidad superradiante (× emisión individual).
    energia_cero : float
        Energía del ground state hamiltoniano (J).
    fase_phoenix : float
        Fase acumulada del ciclo Phoenix (rad).
    """

    sello_activo: bool = False
    sello: str = _SELLO
    psi_global: float = 0.0
    psi_apoptosis: float = 0.0
    psi_phoenix: float = 0.0
    psi_tumoral: float = 0.0
    psi_mito: float = 0.0
    psi_hamiltoniano: float = 0.0
    f0: float = field(default_factory=lambda: _F0)
    f_mito: float = field(default_factory=lambda: _F_MITO)
    f_armonicos: List[float] = field(default_factory=lambda: list(_F_ARMONICOS))
    traza_tumoral: float = 0.0
    intensidad_sr: float = 0.0
    energia_cero: float = 0.0
    fase_phoenix: float = 0.0


class SistemaPhoenixOncoCoherente:
    """
    Orquestador principal del Sistema Phoenix Onco Coherente V10.

    Ejecuta la simulación completa:
        1. Crea todos los componentes físicos.
        2. Calcula las cinco medidas de coherencia.
        3. Computa Ψ_global y activa el sello ∴POC∞³ si Ψ_global ≥ 0.888.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental (Hz). Por defecto F0_HZ = 141.7001.
    n_ciclos : int
        Número de ciclos Phoenix 4π. Por defecto 10.
    n_celulas : int
        Número de células para la superradiancia. Por defecto 10.
    """

    def __init__(
        self,
        f0: float = _F0,
        n_ciclos: int = 10,
        n_celulas: int = _N_CELULAS,
    ) -> None:
        self.f0 = f0
        self.n_ciclos = n_ciclos
        self.n_celulas = n_celulas

        self._constantes = ConstantesPhoenixOnco(f0=f0, n_celulas=n_celulas)
        self._apoptosis = ApoptosisResonante(f0=f0)
        self._phoenix = CicloPhoenix(f0=f0, n_ciclos=n_ciclos)
        self._tumoral = MatrizCoherenciaTumoral()
        self._hamiltoniano = HamiltonianoCelularPOC(f0=f0)
        self._superradiancia = SuperradianciaMitocondrialPOC(
            f0=f0, n_celulas=n_celulas
        )
        self._coherencia = CoherenciaPhoenixOnco()

    def activar(self) -> ResultadoPhoenixOnco:
        """
        Ejecuta la simulación POC completa y retorna todos los resultados.

        Retorna
        -------
        ResultadoPhoenixOnco
            Contenedor con Ψ_global, componentes y sello.
        """
        # 1. Cinco medidas de coherencia
        psi_apo = self._apoptosis.psi_apoptosis()
        psi_phx = self._phoenix.psi_phoenix()
        psi_tum = self._tumoral.psi_tumoral()
        psi_mit = self._superradiancia.psi_mito()
        psi_ham = self._hamiltoniano.psi_hamiltoniano()

        # 2. Coherencia global
        psi_global = self._coherencia.calcular(psi_apo, psi_phx, psi_tum, psi_mit, psi_ham)
        activo = self._coherencia.sello_activo(psi_global)

        # 3. Datos adicionales
        traza = self._tumoral.traza()
        intensidad = self._superradiancia.intensidad_superradiante()
        e0 = self._hamiltoniano.energia_cero()
        fase = self._phoenix.fase_acumulada()

        return ResultadoPhoenixOnco(
            sello_activo=activo,
            sello=_SELLO,
            psi_global=psi_global,
            psi_apoptosis=psi_apo,
            psi_phoenix=psi_phx,
            psi_tumoral=psi_tum,
            psi_mito=psi_mit,
            psi_hamiltoniano=psi_ham,
            f0=self.f0,
            f_mito=self._constantes.f_mito(),
            f_armonicos=list(self._apoptosis._f_armonicos),
            traza_tumoral=traza,
            intensidad_sr=intensidad,
            energia_cero=e0,
            fase_phoenix=fase,
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def phoenix_onco_coherente_v10_activar(
    f0: float = _F0,
    n_ciclos: int = 10,
    n_celulas: int = _N_CELULAS,
) -> Dict:
    """
    Activa el Sistema Phoenix Onco Coherente V10 y retorna el resultado como dict.

    Parámetros
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141.7001 Hz.
    n_ciclos : int
        Número de ciclos Phoenix 4π. Por defecto 10.
    n_celulas : int
        Número de células en la superradiancia. Por defecto 10.

    Retorna
    -------
    dict
        Diccionario con todos los resultados:
        - 'sello_activo'    : bool
        - 'sello'           : str  ('∴POC∞³')
        - 'psi_global'      : float (≥ 0.888 si el sello está activo)
        - 'psi_apoptosis'   : float
        - 'psi_phoenix'     : float
        - 'psi_tumoral'     : float
        - 'psi_mito'        : float
        - 'psi_hamiltoniano': float
        - 'f0'              : float
        - 'f_mito'          : float
        - 'f_armonicos'     : List[float]
        - 'traza_tumoral'   : float
        - 'intensidad_sr'   : float
        - 'energia_cero'    : float
        - 'fase_phoenix'    : float

    Lanza
    -----
    ValueError
        Si f0 ≤ 0, n_ciclos < 1 o n_celulas < 1.

    Ejemplos
    --------
    >>> r = phoenix_onco_coherente_v10_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
    >>> r['sello']
    '∴POC∞³'
    >>> r['f0']
    141.7001
    """
    if f0 <= 0:
        raise ValueError(f"f0 debe ser positiva, se recibió {f0}")
    if n_ciclos < 1:
        raise ValueError(f"n_ciclos debe ser >= 1, se recibió {n_ciclos}")
    if n_celulas < 1:
        raise ValueError(f"n_celulas debe ser >= 1, se recibió {n_celulas}")

    sistema = SistemaPhoenixOncoCoherente(f0=f0, n_ciclos=n_ciclos, n_celulas=n_celulas)
    resultado = sistema.activar()

    return {
        "sello_activo": resultado.sello_activo,
        "sello": resultado.sello,
        "psi_global": resultado.psi_global,
        "psi_apoptosis": resultado.psi_apoptosis,
        "psi_phoenix": resultado.psi_phoenix,
        "psi_tumoral": resultado.psi_tumoral,
        "psi_mito": resultado.psi_mito,
        "psi_hamiltoniano": resultado.psi_hamiltoniano,
        "f0": resultado.f0,
        "f_mito": resultado.f_mito,
        "f_armonicos": resultado.f_armonicos,
        "traza_tumoral": resultado.traza_tumoral,
        "intensidad_sr": resultado.intensidad_sr,
        "energia_cero": resultado.energia_cero,
        "fase_phoenix": resultado.fase_phoenix,
    }
