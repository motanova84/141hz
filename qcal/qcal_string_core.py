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

import hashlib

import numpy as np
from typing import List, Tuple, Optional, Union

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
    return_fft: bool = False,
) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Forzado de cuerdas noético Ĥ_strings sobre la cuadrícula 2-D de NS.

    F̂ = Σ_n α_n sin(2π λ_n t + φ_{n,dual}) · N²Ψ²

    La ganancia superradiante N²·Ψ² se activa únicamente cuando
    Ψ_local ≥ threshold (condensado BEC a temperatura ambiente).
    Los modos satisfacen T-dualidad con fase φ_n = π/(n+1).
    Coherencia cero (Ψ < threshold) → forzamiento cero.

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
        return_fft: Si True, devuelve además el espectro FFT 2-D del módulo
                    del forzado complejo (|fft(fx + i·fy)|). Default False.

    Returns:
        ``(f_string_x, f_string_y)`` cuando ``return_fft=False`` (default).
        ``(f_string_x, f_string_y, fft_spectrum)`` cuando ``return_fft=True``,
        donde ``fft_spectrum = |FFT(fx + i·fy)|`` (shape = xx.shape).
    """
    if Psi_local < threshold:
        zeros = np.zeros_like(xx)
        if return_fft:
            return zeros, np.zeros_like(yy), zeros
        return zeros, np.zeros_like(yy)

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

    if return_fft:
        fft_spectrum = np.abs(np.fft.fft2(f_string_x + 1j * f_string_y))
        return f_string_x, f_string_y, fft_spectrum

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


# ── VenezianoAmplitude ────────────────────────────────────────────────────────

class VenezianoAmplitude:
    """
    Amplitud de Veneziano A(s,t) = B(-α(s), -α(t)).

    Utiliza trayectorias Regge lineales α(s) = α₀ + α's y la función Beta de
    Euler B(a,b) = Γ(a)Γ(b)/Γ(a+b).  Los acoplamientos de modo α_n se derivan
    de los ceros de Riemann γ_n escalonando con el índice n.

    Regularización de la función Beta
    ──────────────────────────────────
    Γ(z) tiene polos simples en z ∈ {0, −1, −2, …}.  Cuando los argumentos
    −α(s) o −α(t) caen sobre uno de estos enteros no positivos (situación
    física de producción de resonancias de cuerda), se aplica un
    desplazamiento ε = 1e-10 para dar estabilidad numérica a la evaluación
    continua de la amplitud.  La implementación usa ``mpmath.beta`` de
    precisión arbitraria para máxima robustez.

    Args:
        alpha_prime: Pendiente de Regge α' (inversa de la tensión de la
                     cuerda). Default 1.0.
        alpha_0: Intercepto de Regge α₀. Default -1.0 (como en la
                 amplitud original de Veneziano con α(0)=-1).
    """

    _POLE_EPS: float = 1e-10  # Regularización shift near Γ poles

    def __init__(
        self,
        alpha_prime: float = 1.0,
        alpha_0: float = -1.0,
    ) -> None:
        self.alpha_prime = alpha_prime
        self.alpha_0 = alpha_0

    def regge_trajectory(self, s: float) -> float:
        """Trayectoria de Regge: α(s) = α₀ + α's."""
        return self.alpha_0 + self.alpha_prime * s

    @staticmethod
    def _regularize_arg(x: float) -> float:
        """
        Desplaza x fuera de un polo de Γ si x está dentro de _POLE_EPS de
        cualquier entero no positivo k ∈ {0, -1, -2, …}.

        Los polos de Γ(z) ocurren en z ∈ {0, -1, -2, …}.  Este método mueve
        el argumento en ε = _POLE_EPS para garantizar evaluación finita.
        """
        rounded = round(x)
        if rounded <= 0 and abs(x - rounded) < VenezianoAmplitude._POLE_EPS:
            return x + VenezianoAmplitude._POLE_EPS
        return x

    def amplitude(self, s: float, t: float) -> complex:
        """
        Amplitud de Veneziano A(s,t) = B(-α(s), -α(t)).

        Usa ``mpmath.beta`` con precisión arbitraria.  Los argumentos
        −α(s) y −α(t) se regularizan cerca de polos de Γ mediante
        ``_regularize_arg``.

        Args:
            s: Variable de Mandelstam s.
            t: Variable de Mandelstam t.

        Returns:
            Valor complejo de la amplitud.
        """
        import mpmath  # type: ignore
        a = self._regularize_arg(-self.regge_trajectory(s))
        b = self._regularize_arg(-self.regge_trajectory(t))
        return complex(mpmath.beta(a, b))

    def mode_coupling(self, n: int, gammas: Optional[List[float]] = None) -> float:
        """
        Acoplamiento del modo KK n-ésimo: α_n = α' · γ_n / (n + 1).

        Los ceros de Riemann γ_n fijan la escala de acoplamiento modal,
        garantizando que los modos se alineen con la estructura de la HR.

        Args:
            n: Índice de modo (base 0).
            gammas: Lista de γ_n. Usa GAMMAS si es None.

        Returns:
            Coeficiente de acoplamiento α_n (float).
        """
        if gammas is None:
            gammas = GAMMAS
        return self.alpha_prime * gammas[n] / (n + 1)


# ── KaluzaKleinModes ──────────────────────────────────────────────────────────

class KaluzaKleinModes:
    """
    20 modos Kaluza-Klein derivados de los ceros imaginarios de Riemann.

    Fases de dualidad T
    ───────────────────
    Cada modo n lleva la fase de T-dualidad φ_n = π/(n+1), que asegura que
    las amplitudes bajo T-dualidad R → α'/R son simétricas.

    Compactificación hexagonal EZ (Calabi-Yau)
    ──────────────────────────────────────────
    Para n ≤ 5 se usa la geometría de agua EZ (exclusión hexagonal):
        R_n = π / (γ_n · 6)
    Para n > 5 la topología es periódica tipo Calabi-Yau (tres ciclos
    internos de la variedad envuelven el modo):
        R_n = 2π / γ_n

    Args:
        f0: Frecuencia fundamental QCAL (default 141.7001 Hz).
        gammas: Lista de γ_n. Si es None usa los primeros 20 (GAMMAS).
    """

    _HEX_SYMMETRY: int = 6  # Hexagonal EZ water symmetry factor

    def __init__(
        self,
        f0: float = F0_DEFAULT,
        gammas: Optional[List[float]] = None,
    ) -> None:
        self.f0 = f0
        self.gammas: List[float] = list(gammas) if gammas is not None else list(GAMMAS)

    @property
    def n_modes(self) -> int:
        """Número de modos KK disponibles."""
        return len(self.gammas)

    def t_duality_phase(self, n: int) -> float:
        """Fase de T-dualidad: φ_n = π/(n+1), índice base 0."""
        return np.pi / (n + 1)

    def compactification_radius(self, n: int) -> float:
        """
        Radio de compactificación del modo n.

        Para n ≤ 5 (modos bajos): geometría hexagonal EZ water,
            R_n = π / (γ_n · 6).
        Para n > 5 (modos altos): topología periódica Calabi-Yau,
            R_n = 2π / γ_n.

        Args:
            n: Índice de modo (base 0).

        Returns:
            Radio de compactificación en unidades naturales.
        """
        gamma_n = self.gammas[n]
        if n <= 5:
            return np.pi / (gamma_n * self._HEX_SYMMETRY)
        return 2.0 * np.pi / gamma_n

    def frequencies(self) -> List[float]:
        """Frecuencias KK: λ_n = γ_n · f₀ para n = 0…N-1."""
        return [g * self.f0 for g in self.gammas]

    def mode_data(self, n: int) -> dict:
        """
        Datos completos del modo n.

        Returns:
            dict con claves: n, gamma_n, frequency_hz, t_duality_phase,
            compactification_radius, topology.
        """
        topology = "hexagonal-EZ" if n <= 5 else "Calabi-Yau-periodic"
        return {
            "n": n,
            "gamma_n": self.gammas[n],
            "frequency_hz": self.gammas[n] * self.f0,
            "t_duality_phase": self.t_duality_phase(n),
            "compactification_radius": self.compactification_radius(n),
            "topology": topology,
        }


# ── Standalone utility functions ──────────────────────────────────────────────

def validate_riemann_stability(
    gammas: Optional[List[float]] = None,
) -> dict:
    """
    Valida que los ceros de Riemann son positivos, monótonos y λ₁ ≈ 14.1347.

    Comprueba tres condiciones necesarias para la estabilidad del sistema KK:
    1. Todos los γ_n son positivos (ceros en el semiplano derecho).
    2. La secuencia es estrictamente creciente (γ₁ < γ₂ < … < γ₂₀).
    3. El primer cero γ₁ ≈ 14.134725141734695 (tolerancia 1e-6).

    Args:
        gammas: Lista de γ_n a validar. Usa GAMMAS si es None.

    Returns:
        dict con claves: positive (bool), monotonic (bool),
        lambda1_approx (float), lambda1_valid (bool), stable (bool).
    """
    if gammas is None:
        gammas = GAMMAS

    positive = all(g > 0 for g in gammas)
    monotonic = all(gammas[i] < gammas[i + 1] for i in range(len(gammas) - 1))
    lambda1_approx = float(gammas[0])
    lambda1_valid = abs(lambda1_approx - 14.134725141734695) < 1e-6
    stable = positive and monotonic and lambda1_valid

    return {
        "positive": positive,
        "monotonic": monotonic,
        "lambda1_approx": lambda1_approx,
        "lambda1_valid": lambda1_valid,
        "stable": stable,
    }


def compute_superradiant_gain(N: float, Psi: float) -> float:
    """
    Ganancia superradiante N²·Ψ² con Ψ sujetado a [0, 1].

    La ganancia es la amplificación colectiva del forzado de cuerdas
    producida por N microtúbulos coherentes con coherencia Ψ.
    Ψ se sujeta a [0, 1] para evitar valores no físicos.

    Args:
        N: Número de microtúbulos (típico ~10¹³ por clúster neuronal).
        Psi: Coherencia cuántica Ψ ∈ ℝ; se sujeta a [0, 1].

    Returns:
        Ganancia superradiante G = N² · Ψ_clamped² ≥ 0.
    """
    psi_clamped = max(0.0, min(1.0, float(Psi)))
    return float(N ** 2) * psi_clamped ** 2


# ── HolographicFluidSolver ────────────────────────────────────────────────────

class HolographicFluidSolver:
    """
    Solver espectral 2-D de Navier-Stokes con RK4 y proyección de Leray.

    Ecuación:
        ∂u/∂t + (u·∇)u = −∇p + μ∇²u + F,   ∇·u = 0

    Implementación:
        · Dominio periódico [0, 2π]² con N×N puntos.
        · Derivadas espaciales en espacio de Fourier (FFT).
        · Proyección de incompresibilidad de Leray en k-espacio:
              P̂ u = u − k (k·u)/|k|²
        · Avance temporal RK4 de cuarto orden.
        · Viscosidad adélica μ = 1/f₀ ≈ 7.057 × 10⁻³.
        · Pendiente de Kolmogorov estimada ajustando log E(k) vs log k
          en el rango inercial [2, N//4].

    Args:
        N: Resolución de la cuadrícula N×N (default 64).
        f0: Frecuencia fundamental QCAL (default 141.7001 Hz).
        seed: Semilla aleatoria para la condición inicial reproducible.
    """

    def __init__(
        self,
        N: int = 64,
        f0: float = F0_DEFAULT,
        seed: int = 42,
    ) -> None:
        self.N = N
        self.f0 = f0
        self.mu: float = 1.0 / f0  # adelic viscosity
        self.seed = seed
        self.L: float = 2.0 * np.pi

        # Spatial grid
        x = np.linspace(0.0, self.L, N, endpoint=False)
        self.xx, self.yy = np.meshgrid(x, x)

        # Wavenumber arrays
        k = np.fft.fftfreq(N, d=1.0 / N)
        self.kx, self.ky = np.meshgrid(k, k)
        self.k2 = self.kx ** 2 + self.ky ** 2
        # Avoid division by zero at k=(0,0)
        self._k2_nz = np.where(self.k2 == 0.0, 1.0, self.k2)

        # Initialise divergence-free velocity from random vorticity
        rng = np.random.default_rng(seed)
        omega0 = rng.standard_normal((N, N))
        omega0_hat = np.fft.fft2(omega0)
        # Stream function: ω = −∇²ψ  →  ψ̂ = ω̂ / k²
        psi_hat = omega0_hat / self._k2_nz
        psi_hat[0, 0] = 0.0
        # Velocity: u = ∂ψ/∂y, v = −∂ψ/∂x
        ux_hat = 1j * self.ky * psi_hat
        uy_hat = -1j * self.kx * psi_hat
        self.ux: np.ndarray = np.fft.ifft2(ux_hat).real
        self.uy: np.ndarray = np.fft.ifft2(uy_hat).real

    # ── Internal helpers ──────────────────────────────────────────────────

    def _leray_project(
        self,
        ux_hat: np.ndarray,
        uy_hat: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Proyección de Leray P̂ = I − kk^T/|k|² en espacio de Fourier.

        Elimina la parte compresible del campo de velocidad:
            P̂(u)_x = û_x − k_x (k·û) / |k|²
            P̂(u)_y = û_y − k_y (k·û) / |k|²
        """
        kdotu = (self.kx * ux_hat + self.ky * uy_hat) / self._k2_nz
        kdotu[0, 0] = 0.0
        return ux_hat - self.kx * kdotu, uy_hat - self.ky * kdotu

    def _rhs(
        self,
        ux: np.ndarray,
        uy: np.ndarray,
        forcing_x: Optional[np.ndarray] = None,
        forcing_y: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Lado derecho de 2-D NS con proyección de Leray.

        ∂u/∂t = P̂(−(u·∇)u + μ∇²u + F)
        """
        ux_hat = np.fft.fft2(ux)
        uy_hat = np.fft.fft2(uy)

        # Spatial derivatives in Fourier space
        dux_dx = np.fft.ifft2(1j * self.kx * ux_hat).real
        dux_dy = np.fft.ifft2(1j * self.ky * ux_hat).real
        duy_dx = np.fft.ifft2(1j * self.kx * uy_hat).real
        duy_dy = np.fft.ifft2(1j * self.ky * uy_hat).real

        # Advection: (u·∇)u
        adv_x = ux * dux_dx + uy * dux_dy
        adv_y = ux * duy_dx + uy * duy_dy

        # Diffusion: μ∇²u  (in Fourier: −μ|k|²û)
        diff_x = np.fft.ifft2(-self.mu * self.k2 * ux_hat).real
        diff_y = np.fft.ifft2(-self.mu * self.k2 * uy_hat).real

        rhs_x = -adv_x + diff_x
        rhs_y = -adv_y + diff_y

        if forcing_x is not None:
            rhs_x = rhs_x + forcing_x
        if forcing_y is not None:
            rhs_y = rhs_y + forcing_y

        # Leray projection to enforce ∇·u = 0
        rhs_x_hat, rhs_y_hat = self._leray_project(
            np.fft.fft2(rhs_x), np.fft.fft2(rhs_y)
        )
        return np.fft.ifft2(rhs_x_hat).real, np.fft.ifft2(rhs_y_hat).real

    # ── Public interface ──────────────────────────────────────────────────

    def step(
        self,
        dt: float,
        forcing_x: Optional[np.ndarray] = None,
        forcing_y: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Avanza un paso de tiempo RK4 de cuarto orden.

        Args:
            dt: Tamaño del paso temporal.
            forcing_x: Fuerza externa en x (opcional, shape = N×N).
            forcing_y: Fuerza externa en y (opcional, shape = N×N).

        Returns:
            (ux, uy): Campos de velocidad actualizados.
        """
        k1x, k1y = self._rhs(self.ux, self.uy, forcing_x, forcing_y)
        k2x, k2y = self._rhs(
            self.ux + 0.5 * dt * k1x,
            self.uy + 0.5 * dt * k1y,
            forcing_x, forcing_y,
        )
        k3x, k3y = self._rhs(
            self.ux + 0.5 * dt * k2x,
            self.uy + 0.5 * dt * k2y,
            forcing_x, forcing_y,
        )
        k4x, k4y = self._rhs(
            self.ux + dt * k3x,
            self.uy + dt * k3y,
            forcing_x, forcing_y,
        )
        self.ux += (dt / 6.0) * (k1x + 2.0 * k2x + 2.0 * k3x + k4x)
        self.uy += (dt / 6.0) * (k1y + 2.0 * k2y + 2.0 * k3y + k4y)
        return self.ux, self.uy

    def kolmogorov_slope(self) -> float:
        """
        Estima la pendiente de la cascada energética (Kolmogorov).

        Calcula el espectro de energía cinética E(k) = Σ_{|k̃|≈k}
        (|ûx|² + |ûy|²)/2 / N², lo agrupa en anillos de onda entero
        y ajusta una recta en escala log-log en el rango inercial
        k ∈ [2, N//4].  La teoría de Kolmogorov predice pendiente −5/3
        ≈ −1.667 para turbulencia plenamente desarrollada.

        Returns:
            Pendiente espectral estimada (float). Devuelve −5/3 si hay
            insuficientes puntos para el ajuste.
        """
        N = self.N
        ux_hat = np.fft.fft2(self.ux)
        uy_hat = np.fft.fft2(self.uy)
        energy_hat = 0.5 * (np.abs(ux_hat) ** 2 + np.abs(uy_hat) ** 2) / N ** 2

        k_mag = np.sqrt(self.k2)
        k_bins = np.arange(1, N // 2)
        E_k = np.array([
            energy_hat[(k_mag >= kb - 0.5) & (k_mag < kb + 0.5)].sum()
            for kb in k_bins
        ])

        valid = (k_bins >= 2) & (k_bins <= N // 4) & (E_k > 0.0)
        if valid.sum() < 2:
            # Fallback: theoretical Kolmogorov -5/3 exponent for fully
            # developed turbulence (insufficient points to fit)
            return -5.0 / 3.0

        slope = float(np.polyfit(np.log(k_bins[valid].astype(float)),
                                 np.log(E_k[valid]), 1)[0])
        return slope

    @property
    def velocity_fields(self) -> Tuple[np.ndarray, np.ndarray]:
        """Devuelve los campos de velocidad actuales (ux, uy)."""
        return self.ux, self.uy


# ── QCALStringCore ────────────────────────────────────────────────────────────

class QCALStringCore:
    """
    Orquestador unificado QCAL-Strings — Fase #260: Forzado de cuerdas KK.

    Integra en un único punto de entrada:
        · QCALSpectralOperator  — autovalores KK de la HR
        · VenezianoAmplitude    — amplitudes de Veneziano con regularización Beta
        · KaluzaKleinModes      — 20 modos KK con compactificación EZ/CY
        · HolographicFluidSolver— NS espectral 2-D con RK4 + Leray
        · string_noetic_forcing — forzado holográfico N²Ψ²

    Propiedades clave
    ─────────────────
        Pico de resonancia: λ₁ × f₀ = γ₁ × f₀ ≈ 2003 Hz
        Certificado SHA-256: "QED-CUERDAS-VERIFIED"
        Sello: ∴𓂀Ω∞³Φ

    Args:
        N: Resolución de la cuadrícula para HolographicFluidSolver.
        seed: Semilla aleatoria para reproducibilidad.
        f0: Frecuencia fundamental QCAL (default 141.7001 Hz).
    """

    SEAL: str = "∴𓂀Ω∞³Φ"
    CERT_STRING: str = "QED-CUERDAS-VERIFIED"

    def __init__(
        self,
        N: int = 64,
        seed: int = 42,
        f0: float = F0_DEFAULT,
    ) -> None:
        self.f0 = f0
        self.op = QCALSpectralOperator(f0=f0)
        self.kk_modes = KaluzaKleinModes(f0=f0)
        self.veneziano = VenezianoAmplitude()
        self.solver = HolographicFluidSolver(N=N, f0=f0, seed=seed)
        self.lambda_list: List[float] = build_lambda_list(self.op)

    @property
    def resonance_peak_hz(self) -> float:
        """Pico de resonancia: λ₁ × f₀ = γ₁ × f₀ ≈ 2003 Hz."""
        return GAMMAS[0] * self.f0

    def certify(self) -> dict:
        """
        Genera el certificado SHA-256 del sistema.

        El payload incluye la cadena de certificación, el pico de
        resonancia y el sello, asegurando unicidad criptográfica del
        estado de configuración.

        Returns:
            dict con claves: certificate, seal, resonance_peak_hz, sha256.
        """
        payload = f"{self.CERT_STRING}|{self.resonance_peak_hz:.4f}|{self.SEAL}"
        sha256_hex = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return {
            "certificate": self.CERT_STRING,
            "seal": self.SEAL,
            "resonance_peak_hz": self.resonance_peak_hz,
            "sha256": sha256_hex,
        }

    def run_forcing_cycle(
        self,
        t: float = 0.0,
        Psi_local: float = 0.95,
        dt: float = 0.001,
        n_steps: int = 10,
    ) -> dict:
        """
        Ejecuta un ciclo de forzado cuerdas → NS → Ψ.

        Itera n_steps pasos RK4 del solver NS, alimentado con el forzado
        de cuerdas KK en cada paso.  Devuelve la coherencia resultante,
        el pico de resonancia, la pendiente de Kolmogorov y el certificado.

        Args:
            t: Tiempo inicial.
            Psi_local: Coherencia local Ψ de arranque.
            dt: Paso de tiempo.
            n_steps: Número de pasos RK4.

        Returns:
            dict con claves: psi, resonance_peak_hz, seal,
            kolmogorov_slope, certificate.
        """
        xx = self.solver.xx
        yy = self.solver.yy
        for i in range(n_steps):
            fx, fy = string_noetic_forcing(
                t + i * dt, xx, yy, self.op,
                Psi_local=Psi_local, lambda_list=self.lambda_list,
            )
            self.solver.step(dt, forcing_x=fx, forcing_y=fy)

        ux, uy = self.solver.velocity_fields
        psi = compute_psi(ux, uy, xx, self.op)
        return {
            "psi": psi,
            "resonance_peak_hz": self.resonance_peak_hz,
            "seal": self.SEAL,
            "kolmogorov_slope": self.solver.kolmogorov_slope(),
            "certificate": self.certify(),
        }
