#!/usr/bin/env python3
"""
QCAL Fase V — Cálculo numérico de la relación de dispersión ω(k)

Resuelve el problema de autovalores matricial:
    det( -iω I + D k² − J_QCAL ) = 0
para obtener las 3 ramas ω_j(k), j = 1,2,3.

Uso:
    python scripts/fase_v_dispersion.py --output artifact_fase_v.json
    python scripts/fase_v_dispersion.py --N-list 7 13 21 55 --plot

Sello: QCAL-INYECCION-INMEDIATA-v2.0 ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from typing import Iterable

import numpy as np

# ---------------------------------------------------------------------------
# Parámetros por defecto QCAL
# ---------------------------------------------------------------------------
F0_HZ = 141.7001
C_SPEED = 299_792_458.0
OMEGA_PSI_DEFAULT = 890.8  # rad/s  (2·κ·√λ  con κ=445.4, λ=1.0)


@dataclass
class FieldParams:
    lambda_: float = 1.0
    kappa: float = 445.4
    mu: float = 0.5
    nu: float = 0.5
    rho: float = 445.4

    @property
    def omega_psi(self) -> float:
        return 2.0 * self.kappa * np.sqrt(self.lambda_)


@dataclass
class DiffusionParams:
    D_A: float = 1.0e-2
    D_S: float = 1.0e-2
    D_P: float = 1.0e-2
    D_SP: float = 1.0e-3   # polaridad → espectro
    D_PA: float = 1.0e-3   # alcance → polaridad


def jacobian_qcal(p: FieldParams) -> np.ndarray:
    """
    Jacobiano J_QCAL linealizado alrededor del atractor.

    Bajo la simetría μ=ν, ρ=κ, el bloque (S,P) posee autovalores
    ±i·ω_Ψ − μ, con ω_Ψ = 2·κ·√λ. Esto se obtiene con:
        [[ −μ,   +κ√λ ],
         [ −4κ√λ,  −ν ]]
    (det − trace·s + s² = 0 ⇒ s = −μ ± i·2κ√λ).
    """
    sqrt_lambda = np.sqrt(p.lambda_)
    return np.array(
        [
            [-p.lambda_, 0.0,          0.0],
            [ 0.0,       -p.mu,       p.kappa * sqrt_lambda],
            [ 0.0,       -4.0 * p.kappa * sqrt_lambda, -p.nu],
        ],
        dtype=float,
    )


def diffusion_matrix(d: DiffusionParams) -> np.ndarray:
    """Matriz D no diagonal (ajuste del Director)."""
    return np.array(
        [
            [d.D_A, 0.0, 0.0],
            [0.0, d.D_S, d.D_SP],
            [d.D_PA, 0.0, d.D_P],
        ],
        dtype=float,
    )


def dispersion_branches(
    k: float, p: FieldParams, d: DiffusionParams
) -> np.ndarray:
    """
    Resuelve  −iω = eigvals( J − D k² )
    devolviendo las 3 ramas ω_j(k) ∈ ℂ.
    """
    J = jacobian_qcal(p)
    D = diffusion_matrix(d)
    M = J - D * (k ** 2)
    eigvals = np.linalg.eigvals(M)   # eigvals de M  = −i·ω
    omega = 1j * eigvals             # ω = i · eig(M)
    # Ordenar por |Im(ω)| ascendente ⇒ ω₁ = modo menos amortiguado
    order = np.argsort(np.abs(omega.imag))
    return omega[order]


def node_spacing() -> float:
    """d = c / (2 f₀) ≈ 1.06 km."""
    return C_SPEED / (2.0 * F0_HZ)


def fundamental_k(N: int, d_m: float) -> float:
    return np.pi / (N * d_m)


def sweep_k(k_values: Iterable[float], p: FieldParams, d: DiffusionParams):
    rows = []
    for k in k_values:
        omegas = dispersion_branches(k, p, d)
        rows.append(
            {
                "k_1_per_m": float(k),
                "omega_1_re": float(omegas[0].real),
                "omega_1_im": float(omegas[0].imag),
                "omega_2_re": float(omegas[1].real),
                "omega_2_im": float(omegas[1].imag),
                "omega_3_re": float(omegas[2].real),
                "omega_3_im": float(omegas[2].imag),
            }
        )
    return rows


def sweep_fibonacci(
    N_list: Iterable[int], p: FieldParams, d: DiffusionParams
):
    d_m = node_spacing()
    rows = []
    for N in N_list:
        k1 = fundamental_k(N, d_m)
        omegas = dispersion_branches(k1, p, d)
        rows.append(
            {
                "N": int(N),
                "d_total_km": round(N * d_m / 1000.0, 4),
                "k_1_per_m": float(k1),
                "omega_1_real_rad_s": float(omegas[0].real),
                "gamma_1_per_s": float(-omegas[0].imag),
                "omega_2_real_rad_s": float(omegas[1].real),
                "gamma_2_per_s": float(-omegas[1].imag),
                "omega_3_real_rad_s": float(omegas[2].real),
                "gamma_3_per_s": float(-omegas[2].imag),
            }
        )
    return rows


def _make_plot(k_rows, path: str) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:                     # pragma: no cover
        print(f"[warn] matplotlib no disponible: {exc}")
        return
    ks = [r["k_1_per_m"] for r in k_rows]
    fig, (ax_re, ax_im) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    for j in (1, 2, 3):
        ax_re.plot(ks, [r[f"omega_{j}_re"] for r in k_rows], label=f"ω{j}(k)")
        ax_im.plot(ks, [r[f"omega_{j}_im"] for r in k_rows], label=f"ω{j}(k)")
    ax_re.set_ylabel("Re ω (rad/s)")
    ax_re.set_title("QCAL Fase V — Relación de dispersión ω(k)")
    ax_re.legend()
    ax_re.grid(True, alpha=0.3)
    ax_im.set_ylabel("Im ω (rad/s)")
    ax_im.set_xlabel("k (1/m)")
    ax_im.legend()
    ax_im.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser(description="QCAL Fase V — dispersión ω(k)")
    ap.add_argument("--N-list", type=int, nargs="+",
                    default=[7, 13, 21, 55])
    ap.add_argument("--k-min", type=float, default=1e-3)
    ap.add_argument("--k-max", type=float, default=1.0)
    ap.add_argument("--k-points", type=int, default=64)
    ap.add_argument("--output", type=str,
                    default="artifact_fase_v.json")
    ap.add_argument("--plot", action="store_true")
    ap.add_argument("--plot-path", type=str,
                    default="artifact_fase_v_dispersion.png")
    args = ap.parse_args()

    p = FieldParams()
    dif = DiffusionParams()

    # 1) Barrido continuo en k
    ks = np.logspace(np.log10(args.k_min), np.log10(args.k_max),
                     args.k_points)
    k_rows = sweep_k(ks, p, dif)

    # 2) Barrido Fibonacci (predicción experimental)
    fib_rows = sweep_fibonacci(args.N_list, p, dif)

    # 3) Validación de invariancia de escala del modo ω₁
    omega1_re_values = [r["omega_1_real_rad_s"] for r in fib_rows]
    omega1_abs_mean = float(np.mean(np.abs(omega1_re_values)))
    omega1_dispersion = float(
        np.max(np.abs(omega1_re_values)) - np.min(np.abs(omega1_re_values))
    )
    omega_psi_ref = p.omega_psi
    invariance_ok = abs(omega1_abs_mean - omega_psi_ref) < 1.0  # < 1 rad/s

    artifact = {
        "sello": "QCAL-INYECCION-INMEDIATA-v2.0",
        "f0_hz": F0_HZ,
        "omega_psi_ref_rad_s": omega_psi_ref,
        "parameters": {
            "field": asdict(p),
            "diffusion": asdict(dif),
        },
        "sweep_k": k_rows,
        "sweep_fibonacci": fib_rows,
        "validation": {
            "omega1_abs_mean_rad_s": omega1_abs_mean,
            "omega1_dispersion_rad_s": float(omega1_dispersion),
            "invariance_scale_ok": bool(invariance_ok),
            "tolerance_rad_s": 1.0,
        },
    }

    with open(args.output, "w") as fh:
        json.dump(artifact, fh, indent=2)

    if args.plot:
        _make_plot(k_rows, args.plot_path)
        artifact["plot"] = args.plot_path

    print("=" * 60)
    print("QCAL FASE V — DISPERSIÓN ω(k)")
    print("=" * 60)
    print(f"ω_Ψ (referencia):        {omega_psi_ref:.4f} rad/s")
    print(f"|ω₁| media (Fibonacci):   {omega1_abs_mean:.4f} rad/s")
    print(f"Dispersión |ω₁|:          {omega1_dispersion:.6e} rad/s")
    print(f"Invariancia de escala:   "
          f"{'OK' if invariance_ok else 'FAIL'}")
    print("-" * 60)
    print(f"{'N':>4} {'d_total(km)':>12} {'k₁(1/m)':>12} "
          f"{'ω₁_re':>10} {'Γ₁':>10}")
    for r in fib_rows:
        print(f"{r['N']:>4} {r['d_total_km']:>12.4f} "
              f"{r['k_1_per_m']:>12.6f} "
              f"{r['omega_1_real_rad_s']:>10.4f} "
              f"{r['gamma_1_per_s']:>10.4f}")
    print("=" * 60)
    print(f"Artefacto: {args.output}")
    return 0 if invariance_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
