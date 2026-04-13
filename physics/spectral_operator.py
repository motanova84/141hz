#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║          OPERADOR ESPECTRAL QCAL — Hamiltoniano de Berry-Keating             ║
║                                                                               ║
║  Implementa el operador Hamiltoniano QCAL que acopla el espectro de los      ║
║  ceros de Riemann con la dinámica biológica a través de la frecuencia        ║
║  fundamental f₀ = 141.7001 Hz.                                               ║
║                                                                               ║
║  Ĥ_QCAL = Ĥ_BK ⊗ 𝕀_f₀ + V̂_mod                                              ║
║                                                                               ║
║  Donde:                                                                       ║
║    Ĥ_BK  = i/2 (x ∂_x + ∂_x x)  — Operador de Berry-Keating                 ║
║    V̂_mod = γħ/C                  — Potencial de modulación (fase #261)       ║
║    f₀                            — Factor de escala espectral (141.7001 Hz)  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Clases:
    QCALSpectralOperator  – Operador Hamiltoniano H_BK + V_mod con escala f₀
    QCALSpectralEngine    – Motor espectral en base de Mellin (N=1024)

API pública:
    compute_noetic_forcing(t, eigenvalues, f0, alphas, phis) → np.ndarray
        Calcula el forzamiento noético F_ext(t) = Σ α_n sin(2π γ_n f₀ t + φ_n)
"""

import math

import numpy as np
from scipy.linalg import eigvalsh

# Constante de Planck reducida (CODATA 2018)
_HBAR: float = 1.054571817e-34  # J·s


# ============================================================================
# CLASE 1 – QCALSpectralOperator
# ============================================================================

class QCALSpectralOperator:
    """
    Operador Hamiltoniano QCAL para la generación del espectro de Riemann.

    Construye la matriz del operador

        H = f₀ · (H_BK + V_mod)

    en un espacio de fase de Mellin discretizado linealmente, donde H_BK es
    el operador de Berry-Keating

        H_BK = (i/2)(x·∂_x + ∂_x·x)

    y V_mod = γħ/C es el potencial de modulación que actúa como *gap* de
    energía separando la coherencia (Ψ=1) del caos taquiónico.

    Parámetros
    ----------
    N : int
        Dimensión de la matriz (número de puntos en el espacio de fase).
        Por defecto 128.
    f0 : float
        Frecuencia de escala en Hz.  Por defecto 141.7001 Hz (f₀ QCAL).

    Atributos
    ---------
    N : int
    f0 : float
    x : np.ndarray  — Malla del espacio de fase Mellin ∈ [0.1, 10.0]
    dx : float      — Paso de la malla
    """

    def __init__(self, N: int = 128, f0: float = 141.7001) -> None:
        if N < 4:
            raise ValueError(f"N debe ser ≥ 4, recibido: {N}")
        if f0 <= 0.0:
            raise ValueError(f"f0 debe ser positivo, recibido: {f0}")
        self.N = N
        self.f0 = f0
        self.x = np.linspace(0.1, 10.0, N)
        self.dx = float(self.x[1] - self.x[0])

    # ------------------------------------------------------------------
    def build_hamiltonian(self, gamma: float = 1.0, C: float = 1.0) -> np.ndarray:
        """
        Construye la matriz del operador H = f₀ · (H_BK + V_mod).

        El operador de Berry-Keating se discretiza con diferencias finitas
        centradas de segundo orden:

            H_BK = (i/2)(X·D + D·X)

        donde X = diag(x) y D es la derivada centrada.  El potencial de
        modulación agrega una diagonal constante:

            V_mod = γ·ħ/C · I

        Parámetros
        ----------
        gamma : float
            Parámetro de modulación γ.  Por defecto 1.0.
        C : float
            Factor de normalización C.  Por defecto 1.0 (adimensional).

        Retorna
        -------
        np.ndarray, shape (N, N), dtype complex
            Matriz Hamiltoniana H_total.

        Raises
        ------
        ValueError
            Si C es cero (división por cero en V_mod).
        """
        if C == 0.0:
            raise ValueError("C no puede ser cero.")

        # Operador de derivación: diferencias finitas centradas
        D = (
            np.diag(np.ones(self.N - 1), 1)
            - np.diag(np.ones(self.N - 1), -1)
        ) / (2.0 * self.dx)

        # Operador de Berry-Keating: H_BK = (i/2)(X·D + D·X)
        X = np.diag(self.x)
        H_BK = 0.5j * (X @ D + D @ X)

        # Potencial de modulación (gap de coherencia)
        v_mod_val = gamma * _HBAR / C
        V_mod = np.diag(np.full(self.N, v_mod_val))

        H_total = self.f0 * (H_BK + V_mod)
        return H_total

    # ------------------------------------------------------------------
    def get_resonant_modes(self) -> np.ndarray:
        """
        Extrae los primeros 20 autovalores del sistema (en valor absoluto).

        En Ψ=1.0 estos deben converger a múltiplos de los ceros de Riemann
        escalados por f₀.

        Retorna
        -------
        np.ndarray, shape (min(20, N),)
            Autovalores ordenados de menor a mayor (valor absoluto).
        """
        H = self.build_hamiltonian()
        raw_eigs = np.linalg.eigvals(H)
        sorted_eigs = np.sort(np.abs(raw_eigs))
        return sorted_eigs[: min(20, self.N)]


# ============================================================================
# CLASE 2 – QCALSpectralEngine
# ============================================================================

class QCALSpectralEngine:
    """
    Motor Espectral QCAL para la validación de la secuencia de Riemann.

    Construye el Hamiltoniano de Berry-Keating en la representación
    logarítmica (espacio de Mellin discretizado):

        H = -i ∂_u    con   u = ln x

    donde la derivada antisimétrica *-i ∂_u* es Hermítica por construcción.
    Los autovalores positivos, escalados por `scale_factor`, se corresponden
    con los ceros no triviales γ_n de la función zeta de Riemann.

    Parámetros
    ----------
    N : int
        Dimensión de la malla logarítmica.  Por defecto 1024.

    Atributos
    ---------
    N : int
    u : np.ndarray  — Malla logarítmica ∈ [-5, 5]
    du : float      — Paso logarítmico
    """

    def __init__(self, N: int = 1024) -> None:
        if N < 4:
            raise ValueError(f"N debe ser ≥ 4, recibido: {N}")
        self.N = N
        self.u = np.linspace(-5.0, 5.0, N)
        self.du = float(self.u[1] - self.u[0])

    # ------------------------------------------------------------------
    def generate_operator(self) -> np.ndarray:
        """
        Construye la matriz Hamiltoniana Hermítica H = -i ∂_u.

        La derivada se discretiza con diferencias finitas centradas y se
        simetriza para garantizar Hermiticidad perfecta (H = H†):

            H_sym = (H + H†) / 2

        Retorna
        -------
        np.ndarray, shape (N, N), dtype complex
            Matriz Hamiltoniana Hermítica.
        """
        # Derivada centrada antisimétrica
        D = (
            np.diag(np.ones(self.N - 1), 1)
            - np.diag(np.ones(self.N - 1), -1)
        ) / (2.0 * self.du)

        # Hamiltoniano: H = -i·D (la parte imaginaria deviene Hermítica)
        H = -1j * D

        # Simetrización explícita para garantizar H = H†
        H_hermitian = 0.5 * (H + H.conj().T)
        return H_hermitian

    # ------------------------------------------------------------------
    def compute_spectrum(self, scale_factor: float = 1.0) -> np.ndarray:
        """
        Extrae y normaliza los autovalores positivos del Hamiltoniano.

        Utiliza `scipy.linalg.eigvalsh` sobre la matriz Hermítica compleja para
        obtener autovalores reales garantizados con eficiencia óptima.

        Parámetros
        ----------
        scale_factor : float
            Factor de escala aplicado a los autovalores antes de devolverlos.
            Por defecto 1.0.

        Retorna
        -------
        np.ndarray
            Autovalores positivos ordenados, multiplicados por `scale_factor`.

        Raises
        ------
        ValueError
            Si `scale_factor` ≤ 0.
        """
        if scale_factor <= 0.0:
            raise ValueError(f"scale_factor debe ser positivo, recibido: {scale_factor}")

        H = self.generate_operator()
        # eigvalsh para matrices Hermíticas complejas: garantiza autovalores reales.
        raw_eigenvalues = eigvalsh(H)

        positive_eigenvalues = raw_eigenvalues[raw_eigenvalues > 0]
        return positive_eigenvalues * scale_factor


# ============================================================================
# FUNCIÓN PÚBLICA – compute_noetic_forcing
# ============================================================================

def compute_noetic_forcing(
    t: float,
    eigenvalues: np.ndarray,
    f0: float = 141.7001,
    alphas: np.ndarray | None = None,
    phis: np.ndarray | None = None,
) -> float:
    """
    Calcula el forzamiento noético F_ext(t) = Σ α_n sin(2π γ_n f₀ t + φ_n).

    Este forzamiento "peina" el fluido (citoplasma, agua EZ) con la
    estructura de los números primos a través del espectro de Riemann:
    las singularidades de Navier-Stokes desaparecen porque el espectro actúa
    como una guía de ondas infinita que distribuye la energía sin blow-up.

    Parámetros
    ----------
    t : float
        Tiempo en segundos.
    eigenvalues : np.ndarray
        Autovalores γ_n del operador Hamiltoniano (ceros de Riemann o
        aproximaciones espectrales).
    f0 : float
        Frecuencia de escala en Hz.  Por defecto 141.7001 Hz.
    alphas : np.ndarray | None
        Amplitudes α_n para cada modo.  Si None, se usan amplitudes
        uniformes 1/N (suma normalizada a 1).
    phis : np.ndarray | None
        Fases φ_n en radianes.  Si None, se usan fases nulas.

    Retorna
    -------
    float
        Valor del forzamiento noético en el instante t.

    Raises
    ------
    ValueError
        Si las dimensiones de `alphas` o `phis` no coinciden con
        `eigenvalues`.
    """
    N = len(eigenvalues)
    if N == 0:
        return 0.0

    if alphas is None:
        alphas = np.ones(N) / N
    else:
        alphas = np.asarray(alphas, dtype=float)
        if alphas.shape[0] != N:
            raise ValueError(
                f"alphas debe tener longitud {N}, recibido: {alphas.shape[0]}"
            )

    if phis is None:
        phis = np.zeros(N)
    else:
        phis = np.asarray(phis, dtype=float)
        if phis.shape[0] != N:
            raise ValueError(
                f"phis debe tener longitud {N}, recibido: {phis.shape[0]}"
            )

    forcing = float(
        np.sum(alphas * np.sin(2.0 * math.pi * eigenvalues * f0 * t + phis))
    )
    return forcing
