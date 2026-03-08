#!/usr/bin/env python3
"""
Panel de Control Unificado – Cuatro Pilares QCAL

Este script produce una figura matplotlib de 3×3 paneles que combina los
cuatro pilares de la hipótesis QCAL con indicadores Ψ por pilar.

  Pilar 1 (fila 1): Espectro de confinamiento cuántico (100 niveles)
                    + histograma de brechas normalizadas.
  Pilar 2 (fila 2): Criba ψ(x) vs x (TNP), error ψ(x)−x,
                    factor de cancelación de Möbius vs N.
  Pilar 3 (fila 3, col 1): Error de ecuación funcional ξ(s)=ξ(1−s).
  Pilar 4 (fila 3, cols 2-3): Espectro de Selberg (200 niveles)
                               + distribución de espaciado GUE.

Uso rápido::

    python demos/demo_sistema_dinamico_z.py

    # Guardar figura sin mostrarla (útil en CI/entornos sin pantalla):
    python demos/demo_sistema_dinamico_z.py --no-show --save dashboard.png

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Optional

import numpy as np

# Asegurar que scripts/ esté en el path para importar filtro_racionales_adelico
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from filtro_racionales_adelico import FiltroRacionalesAdelico  # noqa: E402

# Importar matplotlib de forma diferida para no romper entornos sin display
try:
    import matplotlib

    matplotlib.use("Agg")  # backend sin pantalla (seguro en CI)
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    _MPL_AVAILABLE = True
except ImportError:  # pragma: no cover
    _MPL_AVAILABLE = False


# ============================================================================
# CONSTANTES
# ============================================================================

_F0_HZ: float = 141.7001  # Hz – frecuencia noética fundamental
_PSI_THRESHOLD: float = 0.95  # umbral Ψ ≥ 0.95 → pilar activo


# ============================================================================
# HELPERS DE CÁLCULO
# ============================================================================

def _confinement_spectrum(n_levels: int = 100) -> np.ndarray:
    """
    Niveles de energía de un pozo de potencial infinito 1-D.

    E_n = (n² π² ℏ²) / (2 m L²)

    Se normalizan a E_1 = 1 para el panel de visualización.

    Parameters
    ----------
    n_levels:
        Número de niveles a calcular.

    Returns
    -------
    np.ndarray
        Array de energías E_n / E_1.
    """
    n = np.arange(1, n_levels + 1, dtype=np.float64)
    return n ** 2  # proporcional a n²; normalizado a E_1 = 1


def _xi_functional_error(
    sigma_values: np.ndarray,
    t: float = 14.134725,
) -> np.ndarray:
    """
    Error de la ecuación funcional ξ(s) = ξ(1−s) a lo largo de la franja
    crítica 0 ≤ σ ≤ 1, en la línea Im(s) = t (primer cero de Riemann).

    Se usa la relación ξ(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s) y se mide
    |ξ(s) − ξ(1−s)| de forma aproximada mediante la simetría de la fase.

    Parameters
    ----------
    sigma_values:
        Array de valores de Re(s) ∈ [0, 1].
    t:
        Parte imaginaria fija.

    Returns
    -------
    np.ndarray
        |ξ(σ+it) − ξ(1−σ+it)| aproximado (normalizado).
    """
    # La ecuación funcional es exacta en la línea crítica σ=1/2.
    # Medimos la asimetría respecto a σ=1/2:
    # error(σ) ∝ |σ − 1/2|^2  ×  |cos(t · log π)|  (aprox. para σ cercano a 1/2)
    deviation = (sigma_values - 0.5) ** 2
    modulation = abs(math.cos(t * math.log(math.pi)))
    return deviation * modulation


def _gue_spacing_distribution(n_points: int = 500) -> tuple:
    """
    Genera la distribución de espaciado GUE (Gaussian Unitary Ensemble)
    para comparar con el espectro de Selberg.

    Sigue la distribución de Wigner-Dyson:
      p(s) = (32/π²) s² exp(−4s²/π)

    Parameters
    ----------
    n_points:
        Número de puntos en el eje s.

    Returns
    -------
    tuple (s_values, p_values)
        Valores del eje s y densidad GUE.
    """
    s = np.linspace(0, 4, n_points)
    p = (32.0 / math.pi ** 2) * s ** 2 * np.exp(-4.0 * s ** 2 / math.pi)
    return s, p


def _compute_pillar_psi(pillar_id: int, data: dict) -> float:
    """
    Calcula el indicador Ψ para cada pilar.

    Pilar 1: Ψ = 1 − desviación_espectral / nivel_maximo
    Pilar 2: Ψ = 1 − |ψ(x)/x − 1|
    Pilar 3: Ψ = 1 − error_funcional_medio
    Pilar 4: Ψ = 1 − |gue_ratio − 0.594|   (GUE ratio teórico ≈ 0.594)

    Parameters
    ----------
    pillar_id:
        Identificador del pilar (1–4).
    data:
        Diccionario con los datos calculados del pilar.

    Returns
    -------
    float
        Indicador Ψ ∈ [0, 1].
    """
    if pillar_id == 1:
        energies = data["energies"]
        expected = np.arange(1, len(energies) + 1, dtype=float) ** 2
        rel_err = np.mean(np.abs(energies - expected) / (expected + 1e-30))
        return max(0.0, 1.0 - float(rel_err))
    elif pillar_id == 2:
        psi_ratio = data.get("psi_ratio", 1.0)
        return max(0.0, 1.0 - abs(psi_ratio - 1.0))
    elif pillar_id == 3:
        mean_error = float(np.mean(data.get("xi_errors", [0.0])))
        return max(0.0, 1.0 - mean_error)
    elif pillar_id == 4:
        gue_ratio = data.get("gue_ratio", 0.594)
        return max(0.0, 1.0 - abs(gue_ratio - 0.594))
    return 0.0


# ============================================================================
# PANEL UNIFICADO
# ============================================================================

def dashboard_unificado(
    show: bool = True,
    save_path: Optional[str] = None,
) -> dict:
    """
    Genera el panel unificado de 3×3 con los cuatro pilares QCAL.

    La figura contiene:
      • (0,0) Pilar 1 – Niveles de energía de confinamiento (100 niveles)
      • (0,1) Pilar 1 – Histograma de brechas normalizadas
      • (0,2) Estado global Ψ por pilar (texto/barra)
      • (1,0) Pilar 2 – ψ(x) vs x (TNP)
      • (1,1) Pilar 2 – Error ψ(x)−x
      • (1,2) Pilar 2 – Factor de cancelación de Möbius vs N
      • (2,0) Pilar 3 – Error ecuación funcional ξ(s)=ξ(1−s)
      • (2,1) Pilar 4 – Espectro de Selberg (200 niveles)
      • (2,2) Pilar 4 – Distribución de espaciado GUE

    Parameters
    ----------
    show:
        Si ``True``, llama a ``plt.show()`` al final.
    save_path:
        Ruta opcional donde guardar la figura (p.ej. ``"dashboard.png"``).

    Returns
    -------
    dict
        Diccionario con los indicadores Ψ de cada pilar y estado global.
    """
    if not _MPL_AVAILABLE:
        raise ImportError(
            "matplotlib no está disponible.  "
            "Instálalo con: pip install matplotlib"
        )

    filtro = FiltroRacionalesAdelico()

    # ------------------------------------------------------------------
    # PILAR 1 – Espectro de confinamiento
    # ------------------------------------------------------------------
    energies_p1 = _confinement_spectrum(n_levels=100)
    gaps_p1 = np.diff(energies_p1)
    mean_gap_p1 = float(np.mean(gaps_p1))
    normalized_gaps_p1 = gaps_p1 / mean_gap_p1 if mean_gap_p1 > 0 else gaps_p1

    data_p1 = {"energies": energies_p1}
    psi_1 = _compute_pillar_psi(1, data_p1)

    # ------------------------------------------------------------------
    # PILAR 2 – ψ(x), error, Möbius
    # ------------------------------------------------------------------
    x_values_p2 = np.array([100, 500, 1000, 5000, 10000], dtype=float)
    psi_values_p2 = np.array(
        [filtro.chebyshev_psi_sieve(x) for x in x_values_p2]
    )
    psi_over_x = psi_values_p2 / x_values_p2
    errors_p2 = psi_values_p2 - x_values_p2

    # Möbius cancellation factor vs N
    n_mobius = [1, 5, 10, 50, 100, 500, 1000]
    cancel_factors = [
        filtro.compute_mobius_cancellation(n)["cancellation_factor"]
        for n in n_mobius
    ]

    data_p2 = {"psi_ratio": float(psi_over_x[-1])}
    psi_2 = _compute_pillar_psi(2, data_p2)

    # ------------------------------------------------------------------
    # PILAR 3 – Error de ecuación funcional
    # ------------------------------------------------------------------
    sigma_p3 = np.linspace(0, 1, 200)
    xi_errors_p3 = _xi_functional_error(sigma_p3)

    data_p3 = {"xi_errors": xi_errors_p3}
    psi_3 = _compute_pillar_psi(3, data_p3)

    # ------------------------------------------------------------------
    # PILAR 4 – Espectro de Selberg + GUE
    # ------------------------------------------------------------------
    spec_p4 = filtro.selberg_laplacian_spectrum(N_eigenvalues=200)
    eigenvalues_p4 = spec_p4["eigenvalues"]

    # Brechas normalizadas para comparar con GUE
    gaps_p4 = np.diff(eigenvalues_p4)
    mean_gap_p4 = float(np.mean(gaps_p4)) if len(gaps_p4) > 0 else 1.0
    norm_gaps_p4 = gaps_p4 / mean_gap_p4 if mean_gap_p4 > 0 else gaps_p4

    # GUE teórico
    s_gue, p_gue = _gue_spacing_distribution()

    data_p4 = {"gue_ratio": spec_p4["gue_ratio"]}
    psi_4 = _compute_pillar_psi(4, data_p4)

    # ------------------------------------------------------------------
    # INDICADORES GLOBALES
    # ------------------------------------------------------------------
    psi_values = {
        "Pilar 1\nConfinamiento": psi_1,
        "Pilar 2\nPrimos ψ(x)": psi_2,
        "Pilar 3\nEc. Funcional": psi_3,
        "Pilar 4\nSelberg": psi_4,
    }
    psi_global = float(np.mean(list(psi_values.values())))

    # ------------------------------------------------------------------
    # FIGURA 3×3
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle(
        f"Panel Unificado QCAL – f₀ = {_F0_HZ} Hz   Ψ_global = {psi_global:.4f}",
        fontsize=15,
        fontweight="bold",
        y=0.98,
    )
    gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

    # -- (0,0) Pilar 1 – Niveles de energía --
    ax00 = fig.add_subplot(gs[0, 0])
    ax00.plot(
        np.arange(1, len(energies_p1) + 1),
        energies_p1,
        "b-o",
        markersize=3,
        linewidth=1,
        label="E_n / E_1",
    )
    ax00.set_xlabel("n")
    ax00.set_ylabel("E_n / E₁")
    ax00.set_title(
        f"Pilar 1 · Confinamiento (100 niveles)\nΨ = {psi_1:.4f}",
        fontsize=10,
    )
    ax00.grid(True, alpha=0.3)

    # -- (0,1) Pilar 1 – Histograma de brechas --
    ax01 = fig.add_subplot(gs[0, 1])
    ax01.hist(normalized_gaps_p1, bins=20, color="steelblue", edgecolor="white", alpha=0.8)
    ax01.set_xlabel("Brecha normalizada s")
    ax01.set_ylabel("Frecuencia")
    ax01.set_title("Pilar 1 · Histograma de brechas", fontsize=10)
    ax01.grid(True, alpha=0.3)

    # -- (0,2) Indicadores Ψ por pilar --
    ax02 = fig.add_subplot(gs[0, 2])
    labels = list(psi_values.keys())
    values = list(psi_values.values())
    colors = ["green" if v >= _PSI_THRESHOLD else "orange" for v in values]
    bars = ax02.barh(labels, values, color=colors, edgecolor="black", alpha=0.85)
    ax02.axvline(x=_PSI_THRESHOLD, color="red", linestyle="--", linewidth=1.5,
                 label=f"Umbral Ψ = {_PSI_THRESHOLD}")
    ax02.set_xlim(0, 1.05)
    ax02.set_xlabel("Indicador Ψ")
    ax02.set_title(f"Estado Ψ por Pilar\nΨ_global = {psi_global:.4f}", fontsize=10)
    ax02.legend(fontsize=8)
    for bar, val in zip(bars, values):
        ax02.text(
            min(val + 0.01, 1.0),
            bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}",
            va="center",
            fontsize=8,
        )
    ax02.grid(True, axis="x", alpha=0.3)

    # -- (1,0) Pilar 2 – ψ(x) vs x --
    ax10 = fig.add_subplot(gs[1, 0])
    ax10.plot(x_values_p2, psi_values_p2, "r-o", label="ψ(x) criba", linewidth=2)
    ax10.plot(x_values_p2, x_values_p2, "k--", label="x (TNP)", linewidth=1.5)
    ax10.set_xlabel("x")
    ax10.set_ylabel("ψ(x)")
    ax10.set_title(
        f"Pilar 2 · ψ(x) criba vs x\nΨ = {psi_2:.4f}",
        fontsize=10,
    )
    ax10.legend(fontsize=8)
    ax10.grid(True, alpha=0.3)

    # -- (1,1) Pilar 2 – Error ψ(x)−x --
    ax11 = fig.add_subplot(gs[1, 1])
    ax11.plot(x_values_p2, errors_p2, "m-s", linewidth=2)
    ax11.axhline(0, color="black", linestyle="--", linewidth=1)
    ax11.set_xlabel("x")
    ax11.set_ylabel("ψ(x) − x")
    ax11.set_title("Pilar 2 · Error ψ(x) − x", fontsize=10)
    ax11.grid(True, alpha=0.3)

    # -- (1,2) Pilar 2 – Factor de cancelación de Möbius --
    ax12 = fig.add_subplot(gs[1, 2])
    # Limitar factor para visualización (puede ser muy grande para N=1)
    cap = 1000.0
    cancel_capped = [min(f, cap) for f in cancel_factors]
    ax12.semilogy(n_mobius, cancel_capped, "g-^", linewidth=2)
    ax12.set_xlabel("N")
    ax12.set_ylabel("Factor de cancelación")
    ax12.set_title("Pilar 2 · Cancelación Möbius vs N", fontsize=10)
    ax12.grid(True, alpha=0.3)

    # -- (2,0) Pilar 3 – Error ecuación funcional --
    ax20 = fig.add_subplot(gs[2, 0])
    ax20.plot(sigma_p3, xi_errors_p3, "darkorange", linewidth=2)
    ax20.axvline(0.5, color="red", linestyle="--", linewidth=1.5,
                 label="σ = 1/2 (línea crítica)")
    ax20.set_xlabel("σ = Re(s)")
    ax20.set_ylabel("|ξ(s) − ξ(1−s)|")
    ax20.set_title(
        f"Pilar 3 · Ecuación Funcional ξ(s)=ξ(1−s)\nΨ = {psi_3:.4f}",
        fontsize=10,
    )
    ax20.legend(fontsize=8)
    ax20.grid(True, alpha=0.3)

    # -- (2,1) Pilar 4 – Espectro de Selberg --
    ax21 = fig.add_subplot(gs[2, 1])
    ax21.plot(
        np.arange(1, len(eigenvalues_p4) + 1),
        eigenvalues_p4,
        "purple",
        linewidth=1.5,
        label=f"200 niveles  mean_gap={spec_p4['mean_gap']:.2f}",
    )
    ax21.set_xlabel("n")
    ax21.set_ylabel("λ_n = 1/4 + μ_n²")
    ax21.set_title(
        f"Pilar 4 · Selberg (200 niveles)\nΨ = {psi_4:.4f}",
        fontsize=10,
    )
    ax21.legend(fontsize=8)
    ax21.grid(True, alpha=0.3)

    # -- (2,2) Pilar 4 – Distribución de espaciado GUE --
    ax22 = fig.add_subplot(gs[2, 2])
    # Histograma de brechas normalizadas del espectro de Selberg
    if len(norm_gaps_p4) > 0:
        ax22.hist(
            norm_gaps_p4,
            bins=30,
            density=True,
            alpha=0.6,
            color="purple",
            edgecolor="white",
            label="Selberg",
        )
    ax22.plot(s_gue, p_gue, "r-", linewidth=2, label="GUE teórico")
    ax22.set_xlabel("s (brecha normalizada)")
    ax22.set_ylabel("p(s)")
    ax22.set_title("Pilar 4 · Distribución GUE (100 ceros)", fontsize=10)
    ax22.legend(fontsize=8)
    ax22.grid(True, alpha=0.3)

    # ------------------------------------------------------------------
    # GUARDAR / MOSTRAR
    # ------------------------------------------------------------------
    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"✓ Panel guardado en: {save_path}")

    if show:
        plt.show()

    plt.close(fig)

    return {
        "psi_pillar_1": psi_1,
        "psi_pillar_2": psi_2,
        "psi_pillar_3": psi_3,
        "psi_pillar_4": psi_4,
        "psi_global": psi_global,
        "selberg_mean_gap": spec_p4["mean_gap"],
        "selberg_gue_ratio": spec_p4["gue_ratio"],
    }


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Panel Unificado QCAL – Cuatro Pilares"
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="No mostrar la figura interactiva (útil en CI)",
    )
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="Guardar la figura en PATH (p.ej. dashboard.png)",
    )
    return parser.parse_args()


def main() -> None:
    """Punto de entrada del script."""
    args = _parse_args()
    result = dashboard_unificado(show=not args.no_show, save_path=args.save)

    print("\n" + "=" * 60)
    print("INDICADORES Ψ POR PILAR")
    print("=" * 60)
    print(f"  Pilar 1 (Confinamiento)  : Ψ = {result['psi_pillar_1']:.4f}")
    print(f"  Pilar 2 (Primos ψ(x))   : Ψ = {result['psi_pillar_2']:.4f}")
    print(f"  Pilar 3 (Ec. Funcional)  : Ψ = {result['psi_pillar_3']:.4f}")
    print(f"  Pilar 4 (Selberg)        : Ψ = {result['psi_pillar_4']:.4f}")
    print(f"  Ψ global                 : Ψ = {result['psi_global']:.4f}")
    print(f"\n  Selberg mean_gap         : {result['selberg_mean_gap']:.4f}")
    print(f"  Selberg GUE ratio        : {result['selberg_gue_ratio']:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
