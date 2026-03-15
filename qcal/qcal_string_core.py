#!/usr/bin/env python3
"""
QCAL-Strings Core — Gran Unificación Noética
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sello: ∴𓂀Ω∞³
F0: 141.7001 Hz

Eleva el framework QCAL de solver biofísico (microtúbulos + NS adélico)
a un modelo de Gravedad Cuántica Biológica donde la consciencia emerge
como vibraciones de cuerdas compactificadas en la geometría hexagonal
del agua EZ.

Conexiones Teóricas:
    - RH y Cuerdas (Veneziano-Zeta): amplitudes de Veneziano como ratios ζ(s);
      ceros de Riemann (γ_n) como modos Kaluza-Klein (KK) que dictan estabilidad.
    - NS y Dualidad Fluido/Gravedad: NS holográfico con η/s = ħ/(4π k_B);
      μ = 1/f₀ como análogo biológico en fluidos holográficos.
    - Superradiancia: ganancia N²·Ψ² activada post-umbral BEC (Ψ ≥ 0.888).

Forzado Ĥ_strings = Σ α_n sin(2π λ_n t + φ_{n,dual}) · Ψ²
con φ dual de T-dualidad: φ_n = π/(n+1).

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import numpy as np
from typing import List, Tuple, Optional

# ── Riemann zeros (primeros 20 γ_n) ──────────────────────────────────────────
# Computed with mpmath at dps=25; cached for performance.
GAMMAS: List[float] = [
    14.134725141734695,
    21.022039638771556,
    25.010857580145688,
    30.424876125859512,
    32.935061587739190,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167160,
    49.773832477672302,
    52.970321477714461,
    56.446247697063246,
    59.347044002602353,
    60.831778524609809,
    65.112544048081651,
    67.079810529494173,
    69.546401711173979,
    72.067157674481907,
    75.704690699083933,
    77.144840068874805,
]

# ── Module constants ──────────────────────────────────────────────────────────
F0_DEFAULT: float = 141.7001          # Hz — fundamental QCAL frequency
HBAR_DEFAULT: float = 1.0545718e-34   # J·s — reduced Planck constant
BEC_THRESHOLD: float = 0.888          # Ψ threshold for room-temp BEC activation
N_MICROTUBULES_DEFAULT: float = 1e13  # Typical microtubule count per neuron cluster
ALPHA_SCALE_DEFAULT: float = 0.05     # Mode amplitude decay scale
KK_EMISSION_FREQ_HZ: float = 2003.0   # Predicted superradiant emission ~2003 Hz


class QCALSpectralOperator:
    """
    Operador espectral QCAL para modos Kaluza-Klein derivados de la HR.

    Mapea ceros de Riemann (γ_n) a autovalores del hamiltoniano de cuerdas,
    con corrección de potencial de modulación (análogo Casimir de ζ'(1/2)).

    Args:
        gamma: Acoplamiento de modulación (default 1.0).
        C: Constante de escala (default 1.0).
        f0: Frecuencia fundamental QCAL (default 141.7001 Hz).
        hbar: Constante de Planck reducida (default ħ = 1.0545718×10⁻³⁴ J·s).
    """

    def __init__(
        self,
        gamma: float = 1.0,
        C: float = 1.0,
        f0: float = F0_DEFAULT,
        hbar: float = HBAR_DEFAULT,
    ) -> None:
        if C == 0:
            raise ValueError("C must be non-zero (division by C in modulation_potential)")
        self.gamma = gamma
        self.C = C
        self.f0 = f0
        self.hbar = hbar

    def modulation_potential(self) -> float:
        """
        Potencial de modulación: V̂_mod = γ · ħ / C.

        Análogo a la corrección Casimir de ζ'(1/2) en la derivación
        de f₀ desde Type IIB SUGRA + Calabi-Yau quintic.

        Returns:
            Valor del potencial de modulación (float).
        """
        return self.gamma * self.hbar / self.C

    def compute_eigenvalue(self, gamma_n: float) -> float:
        """
        Autovalor del modo KK n-ésimo: λ_n = γ_n · f₀ + V̂_mod.

        Mapea el cero imaginario γ_n de Riemann al autovalor espectral
        del hamiltoniano de cuerdas sobre la línea crítica σ = 1/2.

        Args:
            gamma_n: Parte imaginaria del n-ésimo cero de Riemann (γ_n).

        Returns:
            Autovalor λ_n en Hz.
        """
        return gamma_n * self.f0 + self.modulation_potential()

    def certify_critical_line(self, sigma: float) -> Tuple[bool, float]:
        """
        Certifica si σ está en la línea crítica y devuelve coherencia espectral.

        Métrica Ψ = exp(-|σ - 1/2| · decay) donde decay = γ/C para la escala
        de caída fuera de la línea crítica.  Un cero off-critical (σ ≠ 1/2)
        produce una masa taquiónica imaginaria → decoherencia del sistema.

        Args:
            sigma: Valor del parámetro σ ∈ (0, 1) a certificar.

        Returns:
            (on_critical, psi_spectral):
                on_critical: True si |σ - 1/2| < 1e-10.
                psi_spectral: Coherencia espectral ∈ [0, 1].
        """
        decay = abs(self.gamma / self.C) if self.C != 0 else 1.0
        psi_spectral = float(np.exp(-abs(sigma - 0.5) * decay))
        on_critical = abs(sigma - 0.5) < 1e-10
        return on_critical, psi_spectral


def string_noetic_forcing(
    t: float,
    xx: np.ndarray,
    yy: np.ndarray,
    op: QCALSpectralOperator,
    Psi_local: float,
    lambda_list: List[float],
    N_microtubules: float = N_MICROTUBULES_DEFAULT,
    alpha_scale: float = ALPHA_SCALE_DEFAULT,
    threshold: float = BEC_THRESHOLD,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Forzado de cuerdas noético Ĥ_strings sobre la cuadrícula 2-D de NS.

    Ĥ_strings = Σ_n α_n sin(2π λ_n t + φ_{n,dual}) · Ψ²

    La ganancia superradiante N²·Ψ² se activa únicamente cuando
    Ψ_local ≥ threshold (condensado BEC a temperatura ambiente).
    Los modos satisfacen T-dualidad con fase φ_n = π/(n+1).

    Args:
        t: Tiempo actual de la simulación.
        xx: Malla 2-D de coordenadas x (shape [N, N]).
        yy: Malla 2-D de coordenadas y (shape [N, N]).
        op: Instancia de QCALSpectralOperator.
        Psi_local: Coherencia local Ψ del campo biofísico.
        lambda_list: Lista de autovalores λ_n (de compute_eigenvalue).
        N_microtubules: Número de microtúbulos (default 10¹³).
        alpha_scale: Escala de decaimiento de amplitud modal (default 0.05).
        threshold: Umbral Ψ para activar superradiancia BEC (default 0.888).

    Returns:
        (f_string_x, f_string_y): Forzado espectral en x e y (shape = xx.shape).
    """
    if Psi_local < threshold:
        return np.zeros_like(xx), np.zeros_like(yy)

    L = 2.0 * np.pi
    logos_wave_x = np.sin(2.0 * np.pi * op.f0 * xx / L)
    logos_wave_y = np.cos(2.0 * np.pi * op.f0 * yy / L)

    gain = (N_microtubules ** 2) * (Psi_local ** 2)

    f_string_x = np.zeros_like(xx)
    f_string_y = np.zeros_like(yy)

    for n, lam in enumerate(lambda_list):
        phi_dual = np.pi / (n + 1)          # T-duality phase, decays as 1/n
        alpha_n = alpha_scale / (n + 1)     # Soft amplitude decay
        mode = alpha_n * np.sin(2.0 * np.pi * lam * t + phi_dual)
        f_string_x += mode * logos_wave_x * gain
        f_string_y += mode * logos_wave_y * gain

    return f_string_x, f_string_y


def compute_psi(
    u_phys: np.ndarray,
    v_phys: np.ndarray,
    xx: np.ndarray,
    op: QCALSpectralOperator,
    threshold: float = BEC_THRESHOLD,
    n_sigma_points: int = 11,
) -> float:
    """
    Coherencia combinada biofísica + espectral Ψ(t).

    Ψ = ρ_bio · ρ_spec

    donde:
        ρ_bio  = 0.5 · (|corr(u, sin(2π f₀ x / L))| + |corr(v, cos(2π f₀ x / L))|)
        ρ_spec = mean(psi_spectral(σ)) para σ ∈ linspace(0.4, 0.6, n_sigma_points)

    Args:
        u_phys: Campo de velocidad real u (2-D, physical space).
        v_phys: Campo de velocidad real v (2-D, physical space).
        xx: Malla 2-D de coordenadas x.
        op: Instancia de QCALSpectralOperator.
        threshold: No usado aquí (reservado para futura gating logic).
        n_sigma_points: Número de puntos σ para media espectral (default 11).

    Returns:
        Ψ ∈ [0, 1] — coherencia combinada.
    """
    L = 2.0 * np.pi
    ref_x = np.sin(2.0 * np.pi * op.f0 * xx.flatten() / L)
    ref_y = np.cos(2.0 * np.pi * op.f0 * xx.flatten() / L)

    u_flat = u_phys.flatten()
    v_flat = v_phys.flatten()

    # Correlation matrices; handle degenerate (constant) arrays gracefully
    def _safe_corr(a: np.ndarray, b: np.ndarray) -> float:
        if np.std(a) < 1e-30 or np.std(b) < 1e-30:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    corr_u = _safe_corr(u_flat, ref_x)
    corr_v = _safe_corr(v_flat, ref_y)
    rho_bio = 0.5 * (abs(corr_u) + abs(corr_v))

    sigmas_near = np.linspace(0.4, 0.6, n_sigma_points)
    psi_spec_values = [op.certify_critical_line(float(s))[1] for s in sigmas_near]
    rho_spec = float(np.mean(psi_spec_values))

    return rho_bio * rho_spec


def build_lambda_list(
    op: QCALSpectralOperator,
    gammas: Optional[List[float]] = None,
) -> List[float]:
    """
    Construye la lista de autovalores KK a partir de los ceros de Riemann.

    λ_n = compute_eigenvalue(γ_n) = γ_n · f₀ + V̂_mod

    Args:
        op: Instancia de QCALSpectralOperator.
        gammas: Lista de γ_n. Si es None usa los primeros 20 (GAMMAS).

    Returns:
        Lista de autovalores λ_n.
    """
    if gammas is None:
        gammas = GAMMAS
    return [op.compute_eigenvalue(g) for g in gammas]
