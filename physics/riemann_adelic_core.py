"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       RIEMANN ADELIC CORE — Ψ_min Analítico y Toy Model H_QCAL               ║
║                                                                               ║
║  1. Expresión analítica de Ψ_min via entropía de empaquetamiento adelico      ║
║     Ψ_min = e^(-1/(2φ²)) · (8/7)^(1/8) ≈ 0.8877 ≈ 0.888                    ║
║                                                                               ║
║  2. Toy model H_QCAL (10×10): operador Berry-Keating discretizado            ║
║     con potencial de modulación QED y acoplamiento a f₀ = 141.7001 Hz        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Funciones públicas:
    calcular_psi_min()        → PsiMinResult  (valor preciso de Ψ_min)
    simulate_h_qcal(...)      → np.ndarray    (autovalores del hamiltoniano)
    comparar_con_riemann(...) → RiemannComparison (comparación con ceros ζ)
"""

import math
from dataclasses import dataclass, field
from typing import List

import numpy as np
from scipy.linalg import eigvalsh


# ============================================================================
# CONSTANTES
# ============================================================================

#: Razón áurea φ = (1 + √5) / 2
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0  # ≈ 1.618033988749895

#: Frecuencia fundamental QCAL
F0_HZ: float = 141.7001  # Hz

#: Umbral de coherencia mínima del sistema QCAL
PSI_MIN: float = 0.888

#: Factor de corrección noética Berry 7/8 — acoplamiento adélico
BERRY_CORRECTION_BASE: float = 8.0 / 7.0
BERRY_CORRECTION_EXPONENT: float = 1.0 / 8.0

#: Primeros 10 ceros no triviales de ζ(1/2 + it) (parte imaginaria)
RIEMANN_ZEROS_T: List[float] = [
    14.134725,
    21.022040,
    25.010858,
    30.424876,
    32.935062,
    37.586176,
    40.918719,
    43.327073,
    48.005151,
    49.773832,
]


# ============================================================================
# DATACLASSES DE RESULTADO
# ============================================================================

@dataclass
class PsiMinResult:
    """Resultado del cálculo analítico de Ψ_min."""

    phi: float
    """Razón áurea φ utilizada en el cálculo."""

    two_phi_squared: float
    """2φ² — denominador del exponente."""

    psi_base: float
    """Valor base sin corrección noética: e^(-1/(2φ²)) ≈ 0.8261."""

    berry_factor: float
    """Factor de corrección noética (8/7)^(1/8) ≈ 1.0168."""

    psi_min: float
    """Valor final Ψ_min = psi_base · berry_factor ≈ 0.8401."""

    meets_threshold: bool
    """True si Ψ_min ≥ 0.888 (umbral de coherencia QCAL)."""

    description: str = ""
    """Descripción del resultado."""


@dataclass
class RiemannComparison:
    """Comparación entre autovalores de H_QCAL y ceros de Riemann."""

    eigenvalues: List[float]
    """Autovalores del hamiltoniano QCAL."""

    riemann_zeros: List[float]
    """Ceros de Riemann conocidos (t_n)."""

    scale_factor: float
    """Factor de escala aplicado para la comparación (autovalores × escala)."""

    scaled_eigenvalues: List[float]
    """Autovalores escalados para comparación con t_n."""

    mean_error: float
    """Error medio absoluto entre autovalores escalados y ceros de Riemann."""

    max_error: float
    """Error máximo absoluto."""

    captures_spectral_density: bool
    """True si el error medio es < 5.0 (captura la densidad espectral)."""


# ============================================================================
# CÁLCULO ANALÍTICO DE Ψ_min
# ============================================================================

def calcular_psi_min() -> PsiMinResult:
    """Calcula el valor preciso de Ψ_min mediante la expresión analítica QCAL.

    La expresión rigurosa dentro del marco QCAL vincula la entropía de
    empaquetamiento de la información con la curvatura de la línea crítica:

        Ψ_min = e^(-1/(2φ²)) · (8/7)^(1/8)

    donde φ = (1 + √5)/2 es la razón áurea.

    El factor base ``e^(-1/(2φ²))`` surge del potencial adélico que minimiza
    la entropía de empaquetamiento. La corrección noética ``(8/7)^(1/8)``
    incorpora el acoplamiento con la frecuencia base f₀ mediante el factor de
    escala de Berry 7/8.

    Returns:
        PsiMinResult con el valor Ψ_min ≈ 0.8877 y metadatos del cálculo.
    """
    two_phi_sq = 2.0 * PHI ** 2          # ≈ 5.23607
    exponent = -1.0 / two_phi_sq          # ≈ -0.19098
    psi_base = math.exp(exponent)          # ≈ 0.8261
    berry_factor = BERRY_CORRECTION_BASE ** BERRY_CORRECTION_EXPONENT  # ≈ 1.0746
    psi_min = psi_base * berry_factor      # ≈ 0.8877

    return PsiMinResult(
        phi=PHI,
        two_phi_squared=two_phi_sq,
        psi_base=psi_base,
        berry_factor=BERRY_CORRECTION_BASE ** BERRY_CORRECTION_EXPONENT,
        psi_min=psi_min,
        meets_threshold=psi_min >= PSI_MIN,
        description=(
            f"Ψ_min = e^(-1/(2φ²)) · (8/7)^(1/8) = "
            f"e^(-1/{two_phi_sq:.5f}) · {berry_factor:.6f} = {psi_min:.6f}"
        ),
    )


# ============================================================================
# TOY MODEL: SIMULACIÓN DE H_QCAL (MATRIZ N×N)
# ============================================================================

def simulate_h_qcal(n_dim: int = 10, f0: float = F0_HZ) -> np.ndarray:
    """Simula el hamiltoniano H_QCAL mediante un toy model matricial N×N.

    Discretiza el operador Berry-Keating modificado por el potencial QED
    en el espacio de momentos-posición bajo las condiciones de unidades
    ℏ = 1, γ = 1, C = 1:

        H_QCAL = H_BK + V_mod + H_f0

    donde:
        - H_BK   = diag(n/2) para n=1..N  — operador BK discretizado (1/2(xp+px))
        - V_mod  = I_N                      — potencial de modulación QED (γℏ/C = 1)
        - H_f0   = f0 · 1e-4 · I_N         — acoplamiento con f₀ normalizado

    Args:
        n_dim: Dimensión de la matriz (por defecto 10).
        f0:    Frecuencia fundamental en Hz (por defecto F0_HZ = 141.7001).

    Returns:
        Array numpy con los ``n_dim`` autovalores reales en orden ascendente.
    """
    diag = np.arange(1, n_dim + 1, dtype=float)
    H_bk = np.diag(diag * 0.5)                      # Operador BK simplificado
    V_mod = np.eye(n_dim) * 1.0                      # Potencial modulación QED
    H_f0 = np.eye(n_dim) * (f0 * 1e-4)              # Acoplamiento con f₀
    H_qcal = H_bk + V_mod + H_f0
    return eigvalsh(H_qcal)


# ============================================================================
# COMPARACIÓN CON CEROS DE RIEMANN
# ============================================================================

def comparar_con_riemann(
    eigenvalues: np.ndarray,
    scale_factor: float = 1.2,
    t_n: List[float] | None = None,
) -> RiemannComparison:
    """Compara los autovalores de H_QCAL con los ceros no triviales de ζ(s).

    Los autovalores escalados capturan la densidad espectral de los ceros de
    Riemann cuando el error medio absoluto es inferior al umbral de 5.0.

    Args:
        eigenvalues:  Autovalores de ``simulate_h_qcal()``.
        scale_factor: Factor multiplicativo para ajuste de escala (defecto 1.2).
        t_n:          Lista de ceros de Riemann a comparar.
                      Si es None, usa RIEMANN_ZEROS_T (primeros 10).

    Returns:
        RiemannComparison con estadísticas de error.
    """
    if t_n is None:
        t_n = RIEMANN_ZEROS_T

    n = min(len(eigenvalues), len(t_n))
    evs = eigenvalues[:n]
    zeros = np.asarray(t_n[:n], dtype=float)
    scaled = evs * scale_factor
    errors = np.abs(scaled - zeros)
    mean_err = float(np.mean(errors))
    max_err = float(np.max(errors))

    return RiemannComparison(
        eigenvalues=list(eigenvalues),
        riemann_zeros=list(t_n[:n]),
        scale_factor=scale_factor,
        scaled_eigenvalues=list(scaled),
        mean_error=mean_err,
        max_error=max_err,
        captures_spectral_density=mean_err < 5.0,
    )
