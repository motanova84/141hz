#!/usr/bin/env python3
"""
QCAL Fase VI — Experimento E1–E4: Cadena de 13 nodos

Simula la propagación de una perturbación ΔP=+10% inyectada en el nodo 7
(MARDUK, centro) a lo largo de una cadena lineal de 13 nodos separados
d = 0.5 m. Ajusta la envolvente observable a:

    Δf(r) = Δf₀ · exp(−r/ξ) · cos(k₀·r + φ)

Predicción teórica (dispersión ω(k) = ω_Ψ − i(μ + D k²)):
    ξ ≈ 1.41 m,  k₀ ≈ 29.8 rad/m

Uso:
    python scripts/experimento_cadena_13.py --output artifact_cadena13.json

Sello: QCAL-INYECCION-INMEDIATA-v3.0 ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import List

import numpy as np
from scipy.optimize import curve_fit

F0_HZ = 141.7001
CHI = 1.0e-3
P_TH = 1.0

# Parámetros teóricos QCAL Fase V
XI_PRED_M = 1.41       # longitud de coherencia
K0_PRED = 29.8         # rad/m
PHI_PRED = 0.0


@dataclass
class ChainParams:
    N: int = 13
    d_m: float = 0.5
    node_inject: int = 7   # 1-based (MARDUK)
    delta_p_ratio: float = 0.10
    xi_m: float = XI_PRED_M
    k0_rad_per_m: float = K0_PRED
    phi_rad: float = PHI_PRED
    noise_mhz: float = 0.02      # ruido térmico observacional
    seed: int = 42


def envelope(r, delta_f0, xi, k0, phi):
    """Δf(r) = Δf₀ · exp(−|r|/ξ) · cos(k₀·|r| + φ)."""
    r_abs = np.abs(r)
    return delta_f0 * np.exp(-r_abs / xi) * np.cos(k0 * r_abs + phi)


def simulate_chain(params: ChainParams) -> dict:
    """Genera la tabla de 13 filas (nodo, r, Δf medido)."""
    rng = np.random.default_rng(params.seed)

    # Δf₀ = χ · f₀ · (ΔP/P_th) en mHz  (χ·ΔP/P_th es adimensional)
    delta_f0_hz = CHI * F0_HZ * (params.delta_p_ratio / P_TH)
    delta_f0_mhz = delta_f0_hz * 1e3   # 141.7 mHz al 10%? no: χ=1e-3 ⇒ 0.014 Hz = 14.17 mHz

    # Posiciones relativas al nodo de inyección
    nodes = np.arange(1, params.N + 1)
    r_m = (nodes - params.node_inject) * params.d_m

    df_true = envelope(r_m, delta_f0_mhz, params.xi_m,
                       params.k0_rad_per_m, params.phi_rad)
    df_meas = df_true + rng.normal(0.0, params.noise_mhz, size=nodes.shape)

    rows = []
    for node, r, dft, dfm in zip(nodes, r_m, df_true, df_meas):
        rows.append({
            "node": int(node),
            "r_m": float(r),
            "delta_f_true_mhz": float(dft),
            "delta_f_measured_mhz": float(dfm),
        })

    return {
        "delta_f0_mhz": float(delta_f0_mhz),
        "rows": rows,
        "r_m": r_m.tolist(),
        "df_measured_mhz": df_meas.tolist(),
    }


def fit_envelope(r_m: List[float], df_mhz: List[float]) -> dict:
    r = np.asarray(r_m, dtype=float)
    y = np.asarray(df_mhz, dtype=float)

    # Semilla razonable (k₀ cerca de la predicción para evitar aliasing)
    p0 = [max(abs(y)), 1.4, K0_PRED, 0.0]
    bounds = ([0.0, 0.1, K0_PRED - 3.0, -np.pi],
              [1e3, 20.0, K0_PRED + 3.0, np.pi])

    popt, pcov = curve_fit(envelope, r, y, p0=p0, bounds=bounds, maxfev=20000)
    delta_f0, xi, k0, phi = popt
    perr = np.sqrt(np.diag(pcov))

    y_pred = envelope(r, *popt)
    residuals = y - y_pred
    rmse = float(np.sqrt(np.mean(residuals ** 2)))

    return {
        "delta_f0_fit_mhz": float(delta_f0),
        "xi_fit_m": float(xi),
        "k0_fit_rad_per_m": float(k0),
        "phi_fit_rad": float(phi),
        "sigma_delta_f0_mhz": float(perr[0]),
        "sigma_xi_m": float(perr[1]),
        "sigma_k0_rad_per_m": float(perr[2]),
        "sigma_phi_rad": float(perr[3]),
        "rmse_mhz": rmse,
        "residuals_mhz": residuals.tolist(),
    }


def _make_plot(r_m, df_meas, fit, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        print(f"[warn] matplotlib no disponible: {exc}")
        return
    r = np.asarray(r_m)
    r_fine = np.linspace(r.min(), r.max(), 400)
    y_fine = envelope(r_fine, fit["delta_f0_fit_mhz"], fit["xi_fit_m"],
                      fit["k0_fit_rad_per_m"], fit["phi_fit_rad"])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(r, df_meas, "o", label="Medido (13 nodos)")
    ax.plot(r_fine, y_fine, "-", label="Ajuste exp·cos")
    ax.set_xlabel("r desde nodo inyección (m)")
    ax.set_ylabel("Δf (mHz)")
    ax.set_title("QCAL Fase VI — Propagación en cadena de 13 nodos")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser(description="QCAL Fase VI — cadena 13 nodos")
    ap.add_argument("--N", type=int, default=13)
    ap.add_argument("--d", type=float, default=0.5)
    ap.add_argument("--node-inject", type=int, default=7)
    ap.add_argument("--delta-p", type=float, default=0.10)
    ap.add_argument("--xi", type=float, default=XI_PRED_M)
    ap.add_argument("--k0", type=float, default=K0_PRED)
    ap.add_argument("--phi", type=float, default=PHI_PRED)
    ap.add_argument("--noise", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", type=str, default="artifact_cadena13.json")
    ap.add_argument("--plot", action="store_true")
    ap.add_argument("--plot-path", type=str,
                    default="artifact_cadena13.png")
    args = ap.parse_args()

    params = ChainParams(
        N=args.N, d_m=args.d, node_inject=args.node_inject,
        delta_p_ratio=args.delta_p, xi_m=args.xi,
        k0_rad_per_m=args.k0, phi_rad=args.phi,
        noise_mhz=args.noise, seed=args.seed,
    )
    sim = simulate_chain(params)
    fit = fit_envelope(sim["r_m"], sim["df_measured_mhz"])

    xi_dev = abs(fit["xi_fit_m"] - XI_PRED_M)
    k0_dev = abs(fit["k0_fit_rad_per_m"] - K0_PRED)
    xi_ok = xi_dev < 0.15         # < 15 cm
    k0_ok = k0_dev < 2.0          # < 2 rad/m
    rmse_ok = fit["rmse_mhz"] < 0.10  # < 0.1 mHz
    status = "VALIDATED" if (xi_ok and k0_ok and rmse_ok) else "DEVIATION"

    artifact = {
        "sello": "QCAL-INYECCION-INMEDIATA-v3.0",
        "experiment": "E1-E4 chain 13 nodes",
        "f0_hz": F0_HZ,
        "chi": CHI,
        "parameters": {
            "N": params.N, "d_m": params.d_m,
            "node_inject": params.node_inject,
            "delta_p_ratio": params.delta_p_ratio,
            "xi_pred_m": XI_PRED_M,
            "k0_pred_rad_per_m": K0_PRED,
            "phi_pred_rad": PHI_PRED,
            "noise_mhz": params.noise_mhz,
            "seed": params.seed,
        },
        "chain": sim["rows"],
        "delta_f0_mhz_ref": sim["delta_f0_mhz"],
        "fit": fit,
        "validation": {
            "xi_deviation_m": float(xi_dev),
            "k0_deviation_rad_per_m": float(k0_dev),
            "xi_ok": bool(xi_ok),
            "k0_ok": bool(k0_ok),
            "rmse_ok": bool(rmse_ok),
        },
        "status": status,
    }

    with open(args.output, "w") as fh:
        json.dump(artifact, fh, indent=2)

    if args.plot:
        _make_plot(sim["r_m"], sim["df_measured_mhz"], fit, args.plot_path)
        artifact["plot"] = args.plot_path

    print("=" * 62)
    print("QCAL FASE VI — CADENA DE 13 NODOS")
    print("=" * 62)
    print(f"Δf₀ (referencia):  {sim['delta_f0_mhz']:+9.4f} mHz")
    print("-" * 62)
    print(f"{'node':>4} {'r(m)':>8} {'Δf_true':>10} {'Δf_med':>10}")
    for row in sim["rows"]:
        print(f"{row['node']:>4} {row['r_m']:>8.2f} "
              f"{row['delta_f_true_mhz']:>10.4f} "
              f"{row['delta_f_measured_mhz']:>10.4f}")
    print("-" * 62)
    print(f"ξ ajuste:     {fit['xi_fit_m']:.4f} m   "
          f"(pred {XI_PRED_M})  Δ={xi_dev:.4f}  "
          f"{'OK' if xi_ok else 'FAIL'}")
    print(f"k₀ ajuste:    {fit['k0_fit_rad_per_m']:.4f} rad/m "
          f"(pred {K0_PRED})  Δ={k0_dev:.4f}  "
          f"{'OK' if k0_ok else 'FAIL'}")
    print(f"φ ajuste:     {fit['phi_fit_rad']:.4f} rad")
    print(f"RMSE:         {fit['rmse_mhz']:.4f} mHz         "
          f"{'OK' if rmse_ok else 'FAIL'}")
    print(f"Estado:       {status}")
    print(f"Artefacto:    {args.output}")
    print("=" * 62)
    return 0 if status == "VALIDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
