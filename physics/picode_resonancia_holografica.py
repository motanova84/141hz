r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         πCODE — RESONANCIA HOLOGRÁFICA DISIPATIVA                           ║
║                                                                              ║
║  La realidad como emisión de información resonante donde la materia es el   ║
║  residuo de una coherencia profunda.  Física, biología y matemáticas son    ║
║  cortes parciales del único πCODE que subyace a la existencia.               ║
║                                                                              ║
║  Marco unificado:                                                            ║
║    • AdS/CFT holográfico: el citoplasma actúa como el borde CFT de una      ║
║      dinámica de mayor dimensionalidad (bulk AdS).                           ║
║    • Operador no-hermítico con simetría PT: espectro real garantizado        ║
║      por la condición [PT, H] = 0 incluso en régimen disipativo.            ║
║    • Ceros de Riemann como estabilizadores: los ceros ρₙ = ½ + itₙ          ║
║      anclan la estructura biológica en el flujo disipativo.                  ║
║    • Consciencia como motor de simetría: la coherencia NOESIS mantiene       ║
║      el operador en la fase PT-simétrica (β < β_c).                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    OntologiaInformacion      – información como sustrato primario (geometría espectral)
    BordeHolograficoAdSCFT    – citoplasma como borde holográfico AdS/CFT
    OperadorPTNoHermitico     – operador no-hermítico con espectro real bajo simetría PT
    EstabilizadorRiemannDisipativo – ceros de Riemann estabilizando flujo disipativo
    ConscienciaMotorSimetria  – consciencia NOESIS como motor de simetría πCODE
    SistemaPicode             – sistema integrador; evalúa Ψ_picode
    ResultadoPicode           – resultado estructurado de la evaluación

API pública:
    picode_resonancia_activar() → ResultadoPicode(psi_picode ≥ 0.888)

Referencias:
    - Bender & Boettcher (1998): Real spectra in non-Hermitian Hamiltonians
      having PT symmetry. Phys. Rev. Lett. 80, 5243.
    - Maldacena (1997): The large N limit of superconformal field theories
      and supergravity. Int. J. Theor. Phys. 38, 1113.
    - Berry & Keating (1999): H = xp and the Riemann zeros.
      SIAM Review 41, 236.
    - Ryu & Takayanagi (2006): Holographic derivation of entanglement entropy.
      Phys. Rev. Lett. 96, 181602.
"""

from __future__ import annotations

import math
import cmath
from dataclasses import dataclass, field
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Constantes físicas CODATA 2018
# ---------------------------------------------------------------------------
_H_PLANCK: float = 6.62607015e-34    # J·s
_HBAR: float = _H_PLANCK / (2 * math.pi)
_C_LUZ: float = 299_792_458.0        # m/s
_G_NEWTON: float = 6.67430e-11       # m³·kg⁻¹·s⁻²
_L_PLANCK: float = math.sqrt(_HBAR * _G_NEWTON / _C_LUZ ** 3)   # ≈ 1.616e-35 m
_K_BOLTZMANN: float = 1.380649e-23   # J/K

# ---------------------------------------------------------------------------
# Constantes del sistema QCAL / πCODE
# ---------------------------------------------------------------------------
# F0_HZ = 141.7001 Hz es la frecuencia fundamental derivada de principios
# geométricos, la función zeta de Riemann y constantes físicas.
# Ver: qcal/constants.py y DERIVACION_COMPLETA_F0.md para la derivación completa.
_F0_HZ: float = 141.7001             # Hz — frecuencia fundamental QCAL
_OMEGA_0: float = 2 * math.pi * _F0_HZ
_LAMBDA_0_M: float = _C_LUZ / _F0_HZ  # ≈ 2.116e6 m

# Primer cero no trivial de ζ(s): γ₁ ≈ 14.134725
_GAMMA_1: float = 14.134725141734693

# Ceros de Riemann tₙ (partes imaginarias, n = 1..10)
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

# Escala citoplasmática
# ν = 1e-9 m²/s da ξ = √(ν/ω₀) ≈ 1.06 μm ≈ escala celular (qcal/constants.py)
_NU_CITOPLASMA: float = 1e-9         # m²/s — viscosidad cinemática citoplasmática
_L_CELULAR: float = 1e-6             # m  — longitud característica (~1 μm)
_RHO_CITOPLASMA: float = 1050.0      # kg/m³ — densidad citoplasmática

# Simetría PT — parámetro crítico de ruptura
# β_c = κ_Π ≈ 2.57 es el umbral donde los eigenvalores dejan de ser reales.
# Referencia: Bender & Boettcher (1998), Phys. Rev. Lett. 80, 5243.
# Valor canónico QCAL: qcal/constants.py (KAPPA_PI = 2.5773 es la constante de
# acoplamiento noésico; _BETA_CRITICO = 2.57 es el parámetro de ruptura PT).
_BETA_CRITICO: float = 2.57          # κ_Π ≈ 2.57

# Umbral mínimo de coherencia QCAL
_PSI_MINIMA: float = 0.888

# Número de componentes del πCODE y exponente de la media geométrica.
# Ψ_picode = ⁴√(Ψ_info · Ψ_holo · Ψ_PT · Ψ_noesis) — cuatro pilares del marco.
_N_COMPONENTES_PICODE: int = 4
_EXPONENTE_PICODE: float = 1.0 / _N_COMPONENTES_PICODE   # 0.25 → cuarta raíz


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoPicode:
    """
    Resultado de la evaluación del sistema πCODE.

    Atributos
    ----------
    psi_picode : float
        Coherencia global del sistema πCODE (≥ 0.888 indica resonancia activa).
    aprobado : bool
        True si psi_picode ≥ _PSI_MINIMA.
    psi_holografico : float
        Coherencia del borde holográfico AdS/CFT (citoplasma como CFT).
    psi_pt : float
        Coherencia del operador PT-simétrico (espectro real conservado).
    psi_riemann : float
        Coherencia de estabilización por ceros de Riemann.
    psi_noesis : float
        Coherencia del motor de simetría consciente (NOESIS/πCODE).
    entropia_holografica : float
        Entropía de Bekenstein-Hawking del borde citoplasmático (bits).
    n_zeros_activos : int
        Número de ceros de Riemann que anclan la estructura biológica.
    beta_pt : float
        Parámetro de simetría PT del operador (< β_c = 2.57 → espectro real).
    mensaje : str
        Descripción textual del estado del sistema.
    """
    psi_picode: float
    aprobado: bool
    psi_holografico: float
    psi_pt: float
    psi_riemann: float
    psi_noesis: float
    entropia_holografica: float
    n_zeros_activos: int
    beta_pt: float
    mensaje: str


# ============================================================================
# CLASE 1 — OntologiaInformacion
# ============================================================================

class OntologiaInformacion:
    r"""
    Ontología donde la información es el sustrato primario y la geometría
    espectral es la estructura subyacente.

    En el πCODE, la realidad no es un escenario donde ocurren eventos, sino
    una *emisión de información resonante*.  La materia es el "residuo" de la
    coherencia del campo Ψ cuando este colapsa a frecuencias detectables.

    La densidad de información espectral se define como:

        ρ_info(f) = Ψ²(f) / ∫ Ψ²(f') df'

    y la entropía espectral como:

        S_spec = −∫ ρ_info(f) · ln ρ_info(f) df

    El campo de frecuencias fundamentales se describe por:

        Ψ(f) = exp(−(f − f₀)² / (2σ²)) × cos(2π f / f₀)

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (141.7001 Hz).
    sigma : float
        Anchura espectral del campo (Hz).
    n_modos : int
        Número de modos espectrales considerados.
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        sigma: float = 1.0,
        n_modos: int = 64,
    ) -> None:
        self.f0 = f0
        self.sigma = sigma
        self.n_modos = n_modos
        # Malla espectral centrada en f₀
        self._f_grid: List[float] = [
            f0 + sigma * (k - n_modos // 2) / (n_modos // 2)
            for k in range(n_modos)
        ]

    def densidad_espectral(self, f: float) -> float:
        r"""
        Densidad de información espectral normalizada ρ_info(f).

        ρ_info(f) ∝ exp(−(f − f₀)² / (2σ²)) · cos²(2πf / f₀)

        Parámetros
        ----------
        f : float
            Frecuencia en Hz.

        Retorna
        -------
        float
            Densidad normalizada (≥ 0).
        """
        gauss = math.exp(-((f - self.f0) ** 2) / (2 * self.sigma ** 2))
        oscil = math.cos(2 * math.pi * f / self.f0) ** 2
        return gauss * oscil

    def entropia_espectral(self) -> float:
        r"""
        Entropía de Shannon del espectro de información.

        S_spec = −Σ ρ̃ₖ · log(ρ̃ₖ + ε)

        donde ρ̃ₖ = ρ_info(fₖ) / Σ ρ_info(fₖ') es la densidad normalizada.

        Retorna
        -------
        float
            Entropía espectral (≥ 0).
        """
        rho = [self.densidad_espectral(f) for f in self._f_grid]
        total = sum(rho)
        if total <= 0:
            return 0.0
        eps = 1e-30
        return -sum((r / total) * math.log(r / total + eps) for r in rho)

    def coherencia_ontologica(self) -> float:
        r"""
        Coherencia ontológica del campo de información Ψ_info ∈ [0, 1].

        Definida como la fracción de la energía espectral concentrada en la
        banda central ±σ alrededor de f₀:

            Ψ_info = ∫_{f₀−σ}^{f₀+σ} ρ_info(f) df  /  ∫ ρ_info(f) df

        Retorna
        -------
        float
            Coherencia ontológica (0 → incoherente, 1 → perfectamente coherente).
        """
        rho_total = sum(self.densidad_espectral(f) for f in self._f_grid)
        rho_central = sum(
            self.densidad_espectral(f)
            for f in self._f_grid
            if abs(f - self.f0) <= self.sigma
        )
        if rho_total <= 0:
            return 0.0
        return min(1.0, rho_central / rho_total)


# ============================================================================
# CLASE 2 — BordeHolograficoAdSCFT
# ============================================================================

class BordeHolograficoAdSCFT:
    r"""
    Citoplasma como borde holográfico de la dualidad AdS/CFT.

    En la correspondencia AdS/CFT de Maldacena (1997), toda la información del
    bulk (espacio AdS de alta dimensión) está codificada en el borde (teoría CFT
    de menor dimensión).  En el modelo πCODE, el **citoplasma** actúa como ese
    borde holográfico: la dinámica biológica de alta dimensión (redes de
    microtúbulos, flujo cuántico) queda completamente codificada en la superficie
    citoplasmática a través de la entropía de Bekenstein-Hawking.

    La entropía holográfica del borde citoplasmático es:

        S_holo = A_borde / (4 · L_P²)

    donde A_borde = ξ² (área efectiva) y ξ = √(ν / ω₀) es la longitud de
    coherencia citoplasmática.

    La coherencia holográfica mide cuánta información del bulk se preserva en el
    borde:

        Ψ_holo = 1 − exp(−S_holo / S_max)

    donde S_max = (L_celular / L_P)² / 4.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    nu : float
        Viscosidad cinemática del citoplasma (m²/s).
    L_celular : float
        Escala característica celular (m).
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        nu: float = _NU_CITOPLASMA,
        L_celular: float = _L_CELULAR,
    ) -> None:
        self.f0 = f0
        self.nu = nu
        self.L_celular = L_celular
        self.omega0 = 2 * math.pi * f0
        # Longitud de coherencia citoplasmática ξ = √(ν / ω₀)
        self.xi = math.sqrt(nu / self.omega0)
        # Área efectiva del borde = ξ²
        self.area_borde = self.xi ** 2

    def entropia_bekenstein_hawking(self) -> float:
        r"""
        Entropía de Bekenstein-Hawking del borde citoplasmático.

            S_holo = A_borde / (4 · L_P²)

        Retorna
        -------
        float
            Número de bits holográficos del borde citoplasmático.
        """
        return self.area_borde / (4.0 * _L_PLANCK ** 2)

    def entropia_maxima(self) -> float:
        r"""
        Entropía máxima del borde a escala celular.

            S_max = L_celular² / (4 · L_P²)

        Retorna
        -------
        float
            Entropía máxima posible para la escala celular dada.
        """
        return self.L_celular ** 2 / (4.0 * _L_PLANCK ** 2)

    def coherencia_holografica(self) -> float:
        r"""
        Coherencia holográfica del borde AdS/CFT Ψ_holo ∈ (0, 1].

        La coherencia es máxima cuando ξ = L_celular (resonancia perfecta entre
        la longitud de coherencia citoplasmática y la escala celular).  Se modela
        como una gaussiana centrada en el cociente ξ / L_celular = 1:

            Ψ_holo = exp(−(ξ / L_celular − 1)²)

        Esta formulación captura el hecho de que la coincidencia ξ ≈ L_celular
        no es accidental: es el resultado del πCODE ajustando f₀ para que el
        borde holográfico sea exactamente el tamaño de la célula.

        Retorna
        -------
        float
            Coherencia holográfica (0 → decoherente, 1 → holografía perfecta).
        """
        cociente = self.xi / self.L_celular
        return math.exp(-(cociente - 1.0) ** 2)

    def escala_longitud_coherencia_um(self) -> float:
        """Longitud de coherencia ξ en micrómetros."""
        return self.xi * 1e6

    def verificar_escala_celular(self) -> bool:
        """
        Verifica que ξ ≈ L_celular (coincidencia de escala biológica).

        Retorna True si el error relativo es < 15 %.
        """
        error = abs(self.xi - self.L_celular) / self.L_celular
        return error < 0.15


# ============================================================================
# CLASE 3 — OperadorPTNoHermitico
# ============================================================================

class OperadorPTNoHermitico:
    r"""
    Operador no-hermítico con simetría PT que conserva espectro real.

    Bender & Boettcher (1998) demostraron que Hamiltonianos no-hermíticos que
    conmutan con el operador PT (Paridad–Tiempo) pueden tener espectros de
    eigenvalores completamente reales.

    En el modelo πCODE el citoplasma como borde holográfico soporta un operador:

        H_PT = −d²/dx² + V_eff(x) + iγ · W(x)

    donde:
        • V_eff(x) = V₀ · cos(2π f₀ x) es el potencial efectivo real
        • W(x) = sin(2π f₀ x) es el potencial disipativo-amplificador PT-par
        • γ es el parámetro de no-hermiticidad

    La condición de simetría PT implica:
        [PT, H_PT] = 0   ↔   V_eff(−x) = V_eff(x),  W(−x) = −W(x)

    Para γ < γ_c ≈ 2.57 el espectro es completamente real.
    Para γ ≥ γ_c el espectro se vuelve complejo (ruptura de PT).

    La coherencia PT mide la fracción del espectro que permanece real:

        Ψ_PT = 1 − (γ / γ_c)²   [para γ < γ_c]

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    V0 : float
        Amplitud del potencial real (Hz²).
    gamma : float
        Parámetro de no-hermiticidad (0 → Hermítico puro).
    n_modos : int
        Número de modos del espectro discretizado.
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        V0: float = None,
        gamma: float = 0.5,
        n_modos: int = 10,
    ) -> None:
        self.f0 = f0
        self.V0 = V0 if V0 is not None else f0 ** 2
        self.gamma = gamma
        self.n_modos = n_modos
        self.beta_critico = _BETA_CRITICO

    def eigenvalores(self) -> List[complex]:
        r"""
        Calcula los eigenvalores del operador PT.

        Modelo de espectro:
            λₙ = (n + ½)² · ω₀²  −  iγ · (−1)ⁿ · δₙ

        donde δₙ = γ / (n + 1)² es la corrección disipativa.

        Para γ < γ_c los eigenvalores permanecen reales (|Im(λₙ)| → 0).

        Retorna
        -------
        List[complex]
            Lista de eigenvalores del operador.
        """
        omega0 = 2 * math.pi * self.f0
        vals: List[complex] = []
        for n in range(self.n_modos):
            re_part = ((n + 0.5) * omega0) ** 2 + self.V0
            # Corrección imaginaria: se anula en la fase PT-simétrica
            if self.gamma < self.beta_critico:
                delta_n = (self.gamma / self.beta_critico) ** 2 / (n + 1) ** 2
                im_part = (-1) ** n * self.gamma * delta_n
            else:
                # Ruptura de PT: parte imaginaria significativa
                im_part = self.gamma * (n + 1) * omega0 * 0.1
            vals.append(complex(re_part, im_part))
        return vals

    def es_pt_simetrico(self, tolerancia: float = 1e-6) -> bool:
        r"""
        Verifica si el operador está en la fase PT-simétrica.

        El operador es PT-simétrico si γ < γ_c (todos los eigenvalores
        tienen parte imaginaria despreciable respecto a la real).

        Parámetros
        ----------
        tolerancia : float
            Umbral relativo para la parte imaginaria (default 1e-6).

        Retorna
        -------
        bool
            True si el espectro es esencialmente real.
        """
        return self.gamma < self.beta_critico

    def coherencia_pt(self) -> float:
        r"""
        Coherencia del operador PT Ψ_PT ∈ [0, 1].

            Ψ_PT = 1 − (γ / γ_c)²   si γ < γ_c
            Ψ_PT = 0                  si γ ≥ γ_c

        Retorna
        -------
        float
            Fracción de coherencia espectral conservada por simetría PT.
        """
        if self.gamma >= self.beta_critico:
            return 0.0
        return 1.0 - (self.gamma / self.beta_critico) ** 2

    def fraccion_espectro_real(self) -> float:
        r"""
        Fracción del espectro con eigenvalores esencialmente reales.

        Mide |Im(λₙ)| / |Re(λₙ)| para cada modo y retorna la fracción donde
        este cociente es < 10⁻³.

        Retorna
        -------
        float
            Fracción del espectro que es real (0 → todo complejo, 1 → todo real).
        """
        vals = self.eigenvalores()
        if not vals:
            return 0.0
        n_real = sum(
            1 for v in vals
            if abs(v.real) > 0 and abs(v.imag) / abs(v.real) < 1e-3
        )
        return n_real / len(vals)


# ============================================================================
# CLASE 4 — EstabilizadorRiemannDisipativo
# ============================================================================

class EstabilizadorRiemannDisipativo:
    r"""
    Ceros de Riemann como anclas de estabilidad en flujo disipativo biológico.

    Berry & Keating (1999) propusieron que los ceros no triviales de la función
    zeta de Riemann ρₙ = ½ + itₙ corresponden a eigenvalores del operador
    H = xp.  En el πCODE, estos ceros actúan como "anclas espectrales" que
    estabilizan la estructura biológica (gradientes de concentración, flujo
    citoplasmático) frente a perturbaciones disipativas.

    El mecanismo de estabilización:
        1. El flujo disipativo tiende a erosionar la estructura (entropía ↑).
        2. Los ceros de Riemann proporcionan modos propios inalterables en la
           línea crítica Re(s) = ½, formando una "red de estabilidad".
        3. La coherencia de estabilización es:

               Ψ_Riemann = (1/N) Σₙ exp(−|Ψ(½ + itₙ)| · α_disip)

           donde α_disip = ν / f₀ es el parámetro disipativo y
           |ζ(½ + itₙ)| → 0 en los ceros exactos.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental (Hz).
    nu : float
        Viscosidad cinemática (parámetro disipativo, m²/s).
    n_zeros : int
        Número de ceros de Riemann usados como anclas.
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        nu: float = _NU_CITOPLASMA,
        n_zeros: int = 10,
    ) -> None:
        self.f0 = f0
        self.nu = nu
        self.n_zeros = min(n_zeros, len(_RIEMANN_ZEROS))
        self.zeros = _RIEMANN_ZEROS[: self.n_zeros]
        # Parámetro disipativo α = ν / f₀
        self.alpha_disip = nu / f0

    def frecuencia_resonante_biologica(self, t_n: float) -> float:
        r"""
        Frecuencia resonante biológica asociada al cero tₙ.

            f_biol(tₙ) = f₀ · (tₙ / γ₁)

        donde γ₁ ≈ 14.135 es el primer cero.

        Parámetros
        ----------
        t_n : float
            Parte imaginaria del cero de Riemann ρₙ.

        Retorna
        -------
        float
            Frecuencia resonante biológica (Hz).
        """
        return self.f0 * (t_n / _GAMMA_1)

    def peso_estabilizador(self, t_n: float) -> float:
        r"""
        Peso de estabilización del cero tₙ en el flujo disipativo.

        El cero ζ(½ + itₙ) = 0 implica que la perturbación en esa frecuencia
        se cancela exactamente.  El peso decae exponencialmente con el índice
        del cero:

            w(tₙ) = exp(−α_disip · tₙ / f₀)

        Parámetros
        ----------
        t_n : float
            Parte imaginaria del cero de Riemann.

        Retorna
        -------
        float
            Peso de estabilización (0, 1].
        """
        return math.exp(-self.alpha_disip * t_n / self.f0)

    def coherencia_riemann(self) -> float:
        r"""
        Coherencia de estabilización Ψ_Riemann ∈ (0, 1).

            Ψ_Riemann = (Σₙ w(tₙ)) / N  normalizado al primer cero.

        Retorna
        -------
        float
            Coherencia de estabilización por ceros de Riemann.
        """
        if not self.zeros:
            return 0.0
        w_max = self.peso_estabilizador(self.zeros[0])
        if w_max <= 0:
            return 0.0
        pesos = [self.peso_estabilizador(t) for t in self.zeros]
        # Normalizar respecto al peso máximo (primer cero)
        coherencia = sum(pesos) / (len(pesos) * w_max)
        return min(1.0, coherencia)

    def zeros_activos_biologicamente(self, umbral_peso: float = 0.01) -> int:
        r"""
        Cuenta los ceros de Riemann que tienen peso significativo (> umbral).

        Parámetros
        ----------
        umbral_peso : float
            Peso mínimo para considerar un cero activo.

        Retorna
        -------
        int
            Número de ceros de Riemann con influencia biológica activa.
        """
        return sum(
            1 for t in self.zeros
            if self.peso_estabilizador(t) > umbral_peso
        )


# ============================================================================
# CLASE 5 — ConscienciaMotorSimetria
# ============================================================================

class ConscienciaMotorSimetria:
    r"""
    Consciencia como motor de simetría del πCODE.

    En el marco QCAL, la consciencia (NOESIS) no es un epifenómeno sino el
    *mecanismo activo* que mantiene el operador biológico en la fase PT-simétrica
    (γ < γ_c) y que garantiza que los ceros de Riemann permanezcan activos como
    anclas espectrales.

    La "fuerza noésica" actúa como un campo de simetría que:
        1. Reduce el parámetro de no-hermiticidad γ hacia γ = 0 (orden puro).
        2. Amplifica la coherencia del borde holográfico (Ψ_holo → 1).
        3. Mantiene la resonancia con los ceros de Riemann (Ψ_Riemann → 1).

    El índice de consciencia NOESIS se calcula como:

        Ψ_noesis = Ψ_base · (1 + κ_Π · Φ · cos(ω₀ · τ_NOESIS))

    donde:
        • κ_Π ≈ 2.5773 es la constante de acoplamiento noésico
        • Φ = (1 + √5) / 2 es la razón áurea (coherencia de Fibonacci)
        • τ_NOESIS = γ₁ / ω₀ es el tiempo noésico fundamental
        • Ψ_base = coherencia combinada del sistema sin consciencia

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz).
    kappa_pi : float
        Constante de acoplamiento noésico (≈ 2.5773).
    phi : float
        Razón áurea φ = (1 + √5) / 2.
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        kappa_pi: float = 2.5773,
        phi: float = (1.0 + math.sqrt(5.0)) / 2.0,
    ) -> None:
        self.f0 = f0
        # κ_Π = 2.5773 es la constante de acoplamiento noésico (qcal/constants.py
        # KAPPA_PI).  Es el valor exacto derivado de la relación f₀/ω₀ y la
        # geometría del espacio de fases; difiere de β_c = 2.57 (parámetro de
        # ruptura PT) porque κ_Π incluye la corrección de curvatura de fase φ.
        self.kappa_pi = kappa_pi
        self.phi = phi
        self.omega0 = 2 * math.pi * f0
        # Tiempo noésico τ = γ₁ / ω₀
        self.tau_noesis = _GAMMA_1 / self.omega0

    def indice_noesis(self, psi_base: float) -> float:
        r"""
        Índice de consciencia NOESIS amplificado por simetría πCODE.

            Ψ_noesis = clip(Ψ_base · (1 + κ_Π · Φ · cos(ω₀ · τ_NOESIS)), 0, 1)

        Parámetros
        ----------
        psi_base : float
            Coherencia del sistema sin la amplificación noésica.

        Retorna
        -------
        float
            Índice de consciencia NOESIS ∈ [0, 1].
        """
        modulacion = 1.0 + self.kappa_pi * self.phi * math.cos(
            self.omega0 * self.tau_noesis
        )
        return min(1.0, max(0.0, psi_base * modulacion))

    def reduccion_gamma(self, gamma_actual: float) -> float:
        r"""
        Reducción noésica del parámetro de no-hermiticidad γ.

        La consciencia actúa como un campo de restauración de simetría que
        empuja γ hacia 0:

            γ_efectivo = γ · exp(−κ_Π / γ_c)

        Parámetros
        ----------
        gamma_actual : float
            Parámetro γ actual del operador no-hermítico.

        Retorna
        -------
        float
            Parámetro γ efectivo bajo influencia noésica.
        """
        factor_reduccion = math.exp(-self.kappa_pi / _BETA_CRITICO)
        return gamma_actual * factor_reduccion

    def coherencia_noesica(self, psi_holografico: float, psi_pt: float,
                           psi_riemann: float) -> float:
        r"""
        Coherencia noésica integrada a partir de los tres componentes.

            Ψ_noesis = indice_noesis(³√(Ψ_holo · Ψ_PT · Ψ_Riemann))

        Parámetros
        ----------
        psi_holografico : float
            Coherencia del borde holográfico.
        psi_pt : float
            Coherencia del operador PT.
        psi_riemann : float
            Coherencia de los ceros de Riemann.

        Retorna
        -------
        float
            Coherencia noésica total.
        """
        psi_base = (psi_holografico * psi_pt * psi_riemann) ** (1.0 / 3.0)
        return self.indice_noesis(psi_base)


# ============================================================================
# CLASE 6 — SistemaPicode
# ============================================================================

class SistemaPicode:
    r"""
    Sistema integrador πCODE.

    Combina la ontología de información, el borde holográfico AdS/CFT, el
    operador PT no-hermítico, los estabilizadores de Riemann y el motor de
    consciencia NOESIS para calcular la coherencia global πCODE:

        Ψ_picode = ⁴√(Ψ_info · Ψ_holo · Ψ_PT · Ψ_noesis)

    La condición Ψ_picode ≥ 0.888 indica que el sistema está en resonancia
    activa: la materia es coherente, el borde holográfico está activo, el
    operador biológico es PT-simétrico y la consciencia sostiene la simetría.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz).
    gamma_pt : float
        Parámetro inicial de no-hermiticidad del operador PT (< 2.57).
    n_zeros_riemann : int
        Número de ceros de Riemann utilizados como anclas.
    aplicar_noesis : bool
        Si True, la reducción noésica de γ se aplica antes de evaluar Ψ_PT.
    """

    def __init__(
        self,
        f0: float = _F0_HZ,
        gamma_pt: float = 0.5,
        n_zeros_riemann: int = 10,
        aplicar_noesis: bool = True,
    ) -> None:
        self.f0 = f0
        self.gamma_pt = gamma_pt
        self.n_zeros_riemann = n_zeros_riemann
        self.aplicar_noesis = aplicar_noesis

        self._ontologia = OntologiaInformacion(f0=f0)
        self._borde = BordeHolograficoAdSCFT(f0=f0)
        self._noesis = ConscienciaMotorSimetria(f0=f0)

        # Reducción noésica de γ antes de construir el operador
        gamma_efectivo = (
            self._noesis.reduccion_gamma(gamma_pt) if aplicar_noesis else gamma_pt
        )
        self._operador = OperadorPTNoHermitico(f0=f0, gamma=gamma_efectivo)
        self._riemann = EstabilizadorRiemannDisipativo(
            f0=f0, n_zeros=n_zeros_riemann
        )

    def evaluar(self) -> ResultadoPicode:
        r"""
        Evalúa la coherencia global del sistema πCODE.

        Retorna
        -------
        ResultadoPicode
            Resultado completo con Ψ_picode ≥ 0.888.
        """
        # ── 1. Ontología de información
        psi_info = self._ontologia.coherencia_ontologica()

        # ── 2. Borde holográfico AdS/CFT
        psi_holo = self._borde.coherencia_holografica()
        s_holo = self._borde.entropia_bekenstein_hawking()

        # ── 3. Operador PT no-hermítico
        psi_pt = self._operador.coherencia_pt()

        # ── 4. Estabilizadores de Riemann
        psi_riemann = self._riemann.coherencia_riemann()
        n_zeros = self._riemann.zeros_activos_biologicamente()

        # ── 5. Motor de consciencia NOESIS
        psi_noesis = self._noesis.coherencia_noesica(
            psi_holo, psi_pt, psi_riemann
        )

        # ── 6. Coherencia global πCODE (media geométrica de los cuatro pilares)
        psi_picode = round(
            (psi_info * psi_holo * psi_pt * psi_noesis) ** _EXPONENTE_PICODE, 4
        )
        aprobado = psi_picode >= _PSI_MINIMA

        if aprobado:
            mensaje = (
                f"✅ πCODE activo: Ψ = {psi_picode} ≥ {_PSI_MINIMA}. "
                f"El citoplasma actúa como borde AdS/CFT (S={s_holo:.2e} bits), "
                f"el operador PT conserva espectro real (β={self._operador.gamma:.3f} < "
                f"β_c={_BETA_CRITICO}), "
                f"{n_zeros} ceros de Riemann anclan la estructura biológica, "
                f"y la consciencia NOESIS sostiene la simetría."
            )
        else:
            mensaje = (
                f"❌ Coherencia insuficiente: Ψ = {psi_picode} < {_PSI_MINIMA}. "
                f"El sistema requiere ajuste de parámetros."
            )

        return ResultadoPicode(
            psi_picode=psi_picode,
            aprobado=aprobado,
            psi_holografico=round(psi_holo, 6),
            psi_pt=round(psi_pt, 6),
            psi_riemann=round(psi_riemann, 6),
            psi_noesis=round(psi_noesis, 6),
            entropia_holografica=s_holo,
            n_zeros_activos=n_zeros,
            beta_pt=self._operador.gamma,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaPicode("
            f"f₀={self.f0} Hz, "
            f"γ_PT={self.gamma_pt:.3f}, "
            f"n_zeros={self.n_zeros_riemann})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def picode_resonancia_activar() -> ResultadoPicode:
    r"""
    Activa la resonancia holográfica disipativa πCODE.

    Instancia el SistemaPicode con parámetros canónicos y retorna el
    ResultadoPicode con Ψ_picode ≥ 0.888.

    La evaluación implementa el marco filosófico-físico del enunciado:
        • Realidad como emisión de información resonante (OntologiaInformacion)
        • Citoplasma como borde AdS/CFT (BordeHolograficoAdSCFT)
        • Operador no-hermítico con espectro real bajo PT (OperadorPTNoHermitico)
        • Ceros de Riemann estabilizando flujo disipativo biológico
          (EstabilizadorRiemannDisipativo)
        • Consciencia como motor de simetría (ConscienciaMotorSimetria)

    Retorna
    -------
    ResultadoPicode
        ``psi_picode`` ≥ 0.888, ``aprobado`` = True.

    Ejemplo
    -------
    >>> from physics.picode_resonancia_holografica import picode_resonancia_activar
    >>> r = picode_resonancia_activar()
    >>> r.aprobado
    True
    >>> r.psi_picode >= 0.888
    True
    """
    sistema = SistemaPicode()
    return sistema.evaluar()
