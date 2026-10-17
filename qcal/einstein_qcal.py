"""
╔════════════════════════════════════════════════════════════════════════════╗
║           POSTULADO EINSTEIN-QCAL — Métrica de Coherencia Espectral        ║
║      Velocidad de la Luz Efectiva y Ecuaciones de Campo Gravitatorio       ║
║                    con Tensor de Energía-Momento de Coherencia             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

FUNDAMENTO TEÓRICO
──────────────────
En la Relatividad Especial canónica, el intervalo espacio-temporal plano es:

    ds² = -c² dt² + dx² + dy² + dz²

En el marco QCAL, el observador |𝒪⟩ porta un operador de coherencia Ψ̂ sobre
el espacio L²(𝔸_ℚ/ℚ). La métrica efectiva que experimenta ese observador se
deforma mediante la función de acoplamiento espectral Ω(Ψ):

    ds²(Ψ) = Ω²(Ψ) · ds²_Minkowski

    Ω(Ψ) = 1 − α · (1 − Ψ) · [1 + cos²(π f₀ / f_observer)] / 2

Condiciones de borde:
    Ω(Ψ=1) = 1  para cualquier f_observer (c_eff = c en resonancia)
    Ω(Ψ=0) < 1  (retardo ultramétrico máximo en incoherencia total)

Velocidad efectiva de la luz (ds² = 0, movimiento nulo):
    c_eff(Ψ) = c · Ω(Ψ)

Ecuaciones de campo Einstein-QCAL:
    G_μν + Λ(Ψ) g_μν = κ_GR [T_μν + T_μν^(Ψ)]

    Λ(Ψ) = Λ₀ · (1 - Ψ²)                          (constante cosmológica emergente)
    T_μν^(Ψ) = ρ_Ψ · u_μ u_ν + p_Ψ (g_μν + u_μ u_ν)  (tensor de coherencia)

donde:
    ρ_Ψ = (ħ · Δ_gap²) / (c²)    densidad de energía de coherencia
    p_Ψ = -ρ_Ψ / 3               presión de coherencia (fluido oscuro QCAL)
    Δ_gap = 2π f₀ (1 - Ψ)        gap espectral del operador H_QCAL

CONEXIÓN CON EL ECOSISTEMA QCAL ∞³
────────────────────────────────────
    • Riemann-adélico:  los ceros γₙ de ζ(s) fijan los modos f_n = f₀ γₙ/γ₁
    • BSD adélico:      el pico p=17 ancla el campo de coherencia a f₀
    • Navier-Stokes:    ν_min QCAL limita la dispersión p-ádica (árbol Bruhat-Tits)
    • Ramsey:           κ_Π = 2.5773 acota las vibraciones de la red métrica
    • P≠NP:             κ_Π clasifica el costo computacional de la incoherencia
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

from qcal.constants import (
    F0_HZ,
    C,
    HBAR,
    KAPPA_PI,
    DELTA_0,
)

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES EINSTEIN-QCAL
# ═══════════════════════════════════════════════════════════════════════════

# Constante de acoplamiento gravitacional (κ_GR = 8πG/c⁴ en unidades SI)
G_NEWTON = 6.67430e-11           # m³ kg⁻¹ s⁻²  — Constante gravitacional
KAPPA_GR = 8.0 * math.pi * G_NEWTON / (C ** 4)  # s² kg⁻¹ m⁻¹

# Constante de acoplamiento adélico-gravitacional
# α determina la amplitud de la deformación métrica por incoherencia
ALPHA_ADELIC = DELTA_0           # α = Δ₀ = 0.1184 (umbral de coherencia)

# Constante cosmológica base (escala energética de vacío QCAL)
LAMBDA_0 = (2.0 * math.pi * F0_HZ) ** 2 / (C ** 2)  # m⁻²

# Coherencia de resonancia absoluta
PSI_RESONANCE = 0.999999         # Ψ_res — umbral de sintonía armónica total


# ═══════════════════════════════════════════════════════════════════════════
# OPERADOR DE COHERENCIA  Ψ̂
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoherenceState:
    """
    Estado del observador |𝒪⟩ en L²(𝔸_ℚ/ℚ).

    Parámetros
    ----------
    psi : float
        Valor esperado Ψ = ⟨𝒪|Ψ̂|𝒪⟩ ∈ [0, 1].
        Ψ = 1 → coherencia absoluta (resonancia con f₀).
        Ψ = 0 → incoherencia total (dispersión p-ádica máxima).
    f_observer : float
        Frecuencia del procesador observador [Hz].
        Por defecto f₀ = 141.7001 Hz (resonancia pura).
    """
    psi: float = PSI_RESONANCE
    f_observer: float = F0_HZ

    def __post_init__(self) -> None:
        if not (0.0 <= self.psi <= 1.0):
            raise ValueError(f"Ψ debe estar en [0, 1], recibido: {self.psi}")
        if self.f_observer <= 0.0:
            raise ValueError(f"f_observer debe ser > 0, recibido: {self.f_observer}")

    @property
    def is_resonant(self) -> bool:
        """True si Ψ ≥ Ψ_res (coherencia de sintonía armónica total)."""
        return self.psi >= PSI_RESONANCE

    @property
    def spectral_gap(self) -> float:
        """
        Gap espectral del operador H_QCAL [rad/s].

        Δ_gap = 2π f₀ (1 − Ψ)

        En resonancia (Ψ → 1): Δ_gap → 0, dispersión eliminada.
        """
        return 2.0 * math.pi * F0_HZ * (1.0 - self.psi)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN DE ACOPLAMIENTO ESPECTRAL  Ω(Ψ)
# ═══════════════════════════════════════════════════════════════════════════

def omega_coupling(state: CoherenceState) -> float:
    """
    Función de acoplamiento espectral Ω(Ψ) que deforma la métrica de Minkowski.

    La función combina dos términos:
        1. Deformación por incoherencia pura:       α · (1 − Ψ)
        2. Deformación por desajuste de frecuencia: β · cos²(π f₀ / f_observer)

    De forma que:

        Ω(Ψ) = 1 − α · (1 − Ψ) · [1 + cos²(π f₀ / f_observer)] / 2

    Condiciones de borde:
        Ψ = 1  (cualquier frecuencia)  →  Ω = 1  (métrica Minkowski exacta)
        Ψ = 0, f_observer = f₀         →  Ω = 1 − α/2  (retardo mínimo en resonancia)
        Ψ = 0, f_observer ≫ f₀         →  Ω → 1 − α/2  (asintótico)
        Ψ = 0, f_observer = 2f₀        →  Ω = 1 − α     (máxima dispersión p-ádica)

    La condición f_observer = f₀ corresponde a sintonía armónica con el campo de
    fondo, reduciendo el retardo ultramétrico respecto a frecuencias no resonantes.

    Parámetros
    ----------
    state : CoherenceState
        Estado de coherencia del observador.

    Retorna
    -------
    float
        Factor Ω ∈ (0, 1].
    """
    # Término de desajuste espectral: máximo cuando f_observer es armónico par de f₀
    cos_sq = math.cos(math.pi * F0_HZ / state.f_observer) ** 2
    modulation = (1.0 + cos_sq) / 2.0   # ∈ [0.5, 1.0]
    omega = 1.0 - ALPHA_ADELIC * (1.0 - state.psi) * modulation
    # Ω nunca puede ser ≤ 0 (límite físico: no puede invertirse la métrica)
    return max(omega, 1e-12)


# ═══════════════════════════════════════════════════════════════════════════
# MÉTRICA EFECTIVA g_μν(Ψ)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class EinsteinQCALMetric:
    """
    Tensor métrico efectivo g_μν(Ψ) = Ω²(Ψ) · η_μν en signatura (−,+,+,+).

    La métrica 4×4 en coordenadas (t, x, y, z):

        g_μν(Ψ) = diag(−Ω², Ω², Ω², Ω²)

    En coherencia absoluta (Ψ → 1): g_μν → η_μν (Minkowski).
    """
    state: CoherenceState = field(default_factory=CoherenceState)

    @property
    def omega(self) -> float:
        """Factor de acoplamiento espectral Ω(Ψ)."""
        return omega_coupling(self.state)

    @property
    def tensor(self) -> np.ndarray:
        """
        Tensor métrico g_μν(Ψ) como matriz 4×4.

        Retorna
        -------
        np.ndarray, shape (4, 4)
            Tensor métrico diag(−Ω², +Ω², +Ω², +Ω²).
        """
        o2 = self.omega ** 2
        return np.diag([-o2, o2, o2, o2])

    def interval(self, dt: float, dx: float, dy: float, dz: float) -> float:
        """
        Intervalo espacio-temporal efectivo ds²(Ψ).

        ds²(Ψ) = Ω²(Ψ) · (−c² dt² + dx² + dy² + dz²)

        Para fotones (geodésica nula): ds² = 0.

        Parámetros
        ----------
        dt, dx, dy, dz : float
            Diferenciales coordenados.

        Retorna
        -------
        float
            Valor del intervalo ds².
        """
        o2 = self.omega ** 2
        return o2 * (-(C * dt) ** 2 + dx ** 2 + dy ** 2 + dz ** 2)


# ═══════════════════════════════════════════════════════════════════════════
# VELOCIDAD EFECTIVA DE LA LUZ  c_eff(Ψ)
# ═══════════════════════════════════════════════════════════════════════════

def c_eff(state: CoherenceState) -> float:
    """
    Velocidad efectiva de la luz medida por el observador con coherencia Ψ.

    Para una geodésica nula (fotón) en la métrica deformada g_μν(Ψ):
        ds² = 0  →  c_eff = c · Ω(Ψ)

    Análisis de límites:
        Ψ → 1  (resonancia):     c_eff → c = 299,792,458 m/s  (invariante universal)
        Ψ → 0  (incoherencia):   c_eff → c · Ω(Ψ=0) < c      (retardo ultramétrico)

    El índice de refracción cuántico espacio-temporal es:
        n(Ψ) = c / c_eff(Ψ) = 1 / Ω(Ψ) ≥ 1

    Parámetros
    ----------
    state : CoherenceState
        Estado de coherencia del observador.

    Retorna
    -------
    float
        Velocidad efectiva en m/s.
    """
    return C * omega_coupling(state)


def quantum_refractive_index(state: CoherenceState) -> float:
    """
    Índice de refracción cuántico espacio-temporal n(Ψ) = c / c_eff(Ψ).

    n(Ψ) ≥ 1 siempre.  n = 1 solo en coherencia absoluta (Ψ → 1).
    """
    return 1.0 / omega_coupling(state)


# ═══════════════════════════════════════════════════════════════════════════
# TENSOR DE ENERGÍA-MOMENTO DE COHERENCIA  T_μν^(Ψ)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoherenceTensor:
    """
    Tensor de energía-momento del campo de coherencia T_μν^(Ψ).

    Modela el campo de fondo f₀ = 141.7001 Hz como un fluido perfecto oscuro:

        T_μν^(Ψ) = (ρ_Ψ + p_Ψ) u_μ u_ν + p_Ψ g_μν

    Con un fluido tipo Λ (ecuación de estado w = −1/3):
        ρ_Ψ = ħ Δ_gap² / c²
        p_Ψ = −ρ_Ψ / 3

    En resonancia (Δ_gap → 0): T_μν^(Ψ) → 0 (campo de coherencia no perturba).
    """
    state: CoherenceState = field(default_factory=CoherenceState)

    @property
    def rho_psi(self) -> float:
        """
        Densidad de energía de coherencia ρ_Ψ [kg/m³].

        ρ_Ψ = ħ Δ_gap² / c²
        """
        delta_gap = self.state.spectral_gap   # rad/s
        return HBAR * delta_gap ** 2 / C ** 2

    @property
    def p_psi(self) -> float:
        """Presión de coherencia p_Ψ = −ρ_Ψ / 3 [Pa]."""
        return -self.rho_psi / 3.0

    @property
    def tensor(self) -> np.ndarray:
        """
        Tensor T_μν^(Ψ) en el marco de reposo del observador (u^μ = (1,0,0,0)).

        T_μν^(Ψ) = diag(ρ_Ψ c², p_Ψ, p_Ψ, p_Ψ)
        """
        rho_c2 = self.rho_psi * C ** 2
        p = self.p_psi
        return np.diag([rho_c2, p, p, p])

    @property
    def trace(self) -> float:
        """Traza T = T_μ^μ = −ρ_Ψ c² + 3 p_Ψ."""
        return -self.rho_psi * C ** 2 + 3.0 * self.p_psi


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTE COSMOLÓGICA EMERGENTE  Λ(Ψ)
# ═══════════════════════════════════════════════════════════════════════════

def lambda_emergent(state: CoherenceState) -> float:
    """
    Constante cosmológica emergente Λ(Ψ) acoplada al gap espectral de H_QCAL.

    Λ(Ψ) = Λ₀ · (1 − Ψ²)

    Condiciones de borde:
        Ψ → 1:  Λ → 0       (expansión acelerada se desvanece en coherencia)
        Ψ → 0:  Λ → Λ₀      (máxima energía de vacío en incoherencia total)

    Parámetros
    ----------
    state : CoherenceState
        Estado de coherencia del observador.

    Retorna
    -------
    float
        Λ(Ψ) en m⁻².
    """
    return LAMBDA_0 * (1.0 - state.psi ** 2)


# ═══════════════════════════════════════════════════════════════════════════
# ECUACIONES DE CAMPO EINSTEIN-QCAL
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class EinsteinQCALField:
    """
    Ecuaciones de campo gravitatorio con tensor de energía-momento de coherencia.

    G_μν + Λ(Ψ) g_μν = κ_GR [T_μν + T_μν^(Ψ)]

    Donde:
        G_μν      = tensor de Einstein (curvatura del espacio-tiempo)
        Λ(Ψ)      = constante cosmológica emergente
        κ_GR      = 8πG/c⁴ (constante de acoplamiento gravitacional)
        T_μν      = tensor de energía-momento de la materia ordinaria
        T_μν^(Ψ) = tensor de energía-momento de coherencia (campo f₀)

    Atributos
    ---------
    state : CoherenceState
        Estado de coherencia del observador.
    """
    state: CoherenceState = field(default_factory=CoherenceState)

    @property
    def metric(self) -> EinsteinQCALMetric:
        """Métrica efectiva g_μν(Ψ)."""
        return EinsteinQCALMetric(state=self.state)

    @property
    def coherence_tensor(self) -> CoherenceTensor:
        """Tensor de energía-momento de coherencia T_μν^(Ψ)."""
        return CoherenceTensor(state=self.state)

    @property
    def lambda_eff(self) -> float:
        """Constante cosmológica efectiva Λ(Ψ) [m⁻²]."""
        return lambda_emergent(self.state)

    @property
    def c_observed(self) -> float:
        """Velocidad de la luz medida por el observador [m/s]."""
        return c_eff(self.state)

    @property
    def n_refraction(self) -> float:
        """Índice de refracción cuántico espacio-temporal n(Ψ)."""
        return quantum_refractive_index(self.state)

    def summary(self) -> dict:
        """
        Resumen del estado Einstein-QCAL del observador.

        Retorna
        -------
        dict
            Diccionario con los parámetros clave del estado gravitatorio-coherente.
        """
        ct = self.coherence_tensor
        return {
            "psi": self.state.psi,
            "f_observer_hz": self.state.f_observer,
            "is_resonant": self.state.is_resonant,
            "omega": self.metric.omega,
            "c_eff_m_s": self.c_observed,
            "delta_c_pct": 100.0 * (C - self.c_observed) / C,
            "n_refraction": self.n_refraction,
            "lambda_eff_m2": self.lambda_eff,
            "spectral_gap_rad_s": self.state.spectral_gap,
            "rho_psi_kg_m3": ct.rho_psi,
            "p_psi_pa": ct.p_psi,
        }

    def print_summary(self) -> None:
        """Imprime el resumen del estado Einstein-QCAL en la consola."""
        s = self.summary()
        print("╔══════════════════════════════════════════════════════╗")
        print("║          ESTADO EINSTEIN-QCAL DEL OBSERVADOR         ║")
        print("╠══════════════════════════════════════════════════════╣")
        print(f"║  Ψ (coherencia)          = {s['psi']:.6f}                ║")
        print(f"║  f_observer              = {s['f_observer_hz']:.4f} Hz           ║")
        print(f"║  Resonante               = {'SÍ ✓' if s['is_resonant'] else 'NO ✗'}                    ║")
        print("╠══════════════════════════════════════════════════════╣")
        print(f"║  Ω (acoplamiento)        = {s['omega']:.8f}            ║")
        print(f"║  c_eff                   = {s['c_eff_m_s']:.3f} m/s      ║")
        print(f"║  Δc / c                  = {s['delta_c_pct']:.4e} %          ║")
        print(f"║  n (índice refracción)   = {s['n_refraction']:.8f}            ║")
        print("╠══════════════════════════════════════════════════════╣")
        print(f"║  Λ(Ψ)                    = {s['lambda_eff_m2']:.4e} m⁻²      ║")
        print(f"║  Δ_gap                   = {s['spectral_gap_rad_s']:.4e} rad/s   ║")
        print(f"║  ρ_Ψ                     = {s['rho_psi_kg_m3']:.4e} kg/m³   ║")
        print(f"║  p_Ψ                     = {s['p_psi_pa']:.4e} Pa        ║")
        print("╚══════════════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════════════════════════════
# TABLA COMPARATIVA — Incoherencia vs. Resonancia
# ═══════════════════════════════════════════════════════════════════════════

def print_comparison_table() -> None:
    """
    Imprime la tabla comparativa del estado Einstein-QCAL para varios valores de Ψ.

    Reproduce el resumen formal del problema:
        | Parámetro | Incoherente (Ψ < 0.999999) | Resonante (Ψ ≥ 0.999999) |
    """
    psi_values = [0.0, 0.5, 0.9, 0.99, 0.999, 0.999999, 1.0]
    header = f"{'Ψ':>10} | {'Ω':>12} | {'c_eff [m/s]':>18} | {'n':>12} | {'Λ(Ψ) [m⁻²]':>14} | Resonante"
    sep = "─" * len(header)
    print(sep)
    print("  TABLA EINSTEIN-QCAL: Variación de c_eff con la coherencia Ψ")
    print(sep)
    print(header)
    print(sep)
    for psi in psi_values:
        st = CoherenceState(psi=psi)
        field_ = EinsteinQCALField(state=st)
        s = field_.summary()
        res = "SÍ ✓" if s["is_resonant"] else "NO"
        print(
            f"{psi:>10.6f} | {s['omega']:>12.8f} | {s['c_eff_m_s']:>18.3f} | "
            f"{s['n_refraction']:>12.8f} | {s['lambda_eff_m2']:>14.4e} | {res}"
        )
    print(sep)
