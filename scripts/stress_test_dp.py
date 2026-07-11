#!/usr/bin/env python3
"""
QCAL Fase V — Stress test escalonado y test de simetría

Ejecuta la secuencia:
    Paso 1..5: ΔP = 4, 8, 12, 16, 20 %      (rampa +20 %)
    Paso 6:    ΔP = −10 %                    (simetría / histéresis)
    Paso 7:    ΔP = +10 %                    (retorno)

Verifica:
    · Linealidad: R² del ajuste Δf vs ΔP ≥ 0.999999
    · Ψ mínima ≥ 0.999990 en todos los pasos
    · Simetría: Δf(−10%) = −Δf(+10%) dentro de tolerancia

Uso:
    python scripts/stress_test_dp.py --output stress_report.json

Sello: QCAL-INYECCION-INMEDIATA-v2.0 ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SIMULATOR = REPO_ROOT / "scripts" / "protocolo_perturbacion_dp.py"

F0_HZ = 141.7001
CHI = 1.0e-3
PSI_THRESHOLD = 0.999990


def run_step(delta_p: float, workdir: Path,
             chi: float = CHI, seed: int = 42) -> dict:
    """Invoca el simulador v1.1 en subproceso y devuelve el artefacto."""
    tag = f"{delta_p:+.4f}".replace(".", "p").replace("+", "pos_").replace(
        "-", "neg_")
    out = workdir / f"artifact_{tag}.json"
    cmd = [
        sys.executable,
        str(SIMULATOR),
        "--delta-p", f"{delta_p}",
        "--chi", f"{chi}",
        "--f0", f"{F0_HZ}",
        "--p-th", "1.0",
        "--seed", f"{seed}",
        "--output", str(out),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"simulator failed for ΔP={delta_p}: {proc.stderr}"
        )
    with open(out) as fh:
        return json.load(fh)


def linear_r_squared(xs: List[float], ys: List[float]) -> float:
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if len(x) < 2:
        return float("nan")
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0


def main() -> int:
    ap = argparse.ArgumentParser(description="QCAL Fase V — stress + simetría")
    ap.add_argument("--output", type=str, default="stress_report.json")
    ap.add_argument("--chi", type=float, default=CHI)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ramp", type=float, nargs="+",
                    default=[0.04, 0.08, 0.12, 0.16, 0.20])
    ap.add_argument("--symmetry", type=float, nargs="+",
                    default=[-0.10, 0.10])
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)

        steps = []
        # Fase A: rampa positiva
        for i, dp in enumerate(args.ramp, start=1):
            art = run_step(dp, workdir, chi=args.chi, seed=args.seed)
            steps.append(
                {
                    "phase": "ramp",
                    "step": i,
                    "delta_p_ratio": dp,
                    "delta_f_predicted_mhz": art["delta_f_predicted_mhz"],
                    "delta_f_measured_mhz": art["delta_f_measured_mhz"],
                    "psi": art["coherencia_psi"],
                    "status": art["status"],
                }
            )

        # Fase B: simetría (signo inverso y retorno)
        for dp in args.symmetry:
            art = run_step(dp, workdir, chi=args.chi, seed=args.seed)
            steps.append(
                {
                    "phase": "symmetry",
                    "delta_p_ratio": dp,
                    "delta_f_predicted_mhz": art["delta_f_predicted_mhz"],
                    "delta_f_measured_mhz": art["delta_f_measured_mhz"],
                    "psi": art["coherencia_psi"],
                    "status": art["status"],
                }
            )

    # ---------- Análisis ----------
    ramp_dp = [s["delta_p_ratio"] for s in steps if s["phase"] == "ramp"]
    ramp_df = [s["delta_f_measured_mhz"] for s in steps if s["phase"] == "ramp"]
    r2 = linear_r_squared(ramp_dp, ramp_df)

    psi_min = min(s["psi"] for s in steps)
    psi_ok = psi_min >= PSI_THRESHOLD

    # Simetría: Δf(−10%) = −Δf(+10%)
    sym_pairs = {round(s["delta_p_ratio"], 4): s["delta_f_measured_mhz"]
                 for s in steps if s["phase"] == "symmetry"}
    dp_neg = sym_pairs.get(-0.10)
    dp_pos = sym_pairs.get(0.10)
    sym_dev_mhz = (
        abs(dp_neg + dp_pos)
        if (dp_neg is not None and dp_pos is not None)
        else float("nan")
    )
    sym_ok = np.isfinite(sym_dev_mhz) and sym_dev_mhz < 0.05

    report = {
        "sello": "QCAL-INYECCION-INMEDIATA-v2.0",
        "f0_hz": F0_HZ,
        "chi": args.chi,
        "psi_threshold": PSI_THRESHOLD,
        "steps": steps,
        "analysis": {
            "linearity_r_squared": r2,
            "linearity_ok": bool(r2 >= 0.999999),
            "psi_min": psi_min,
            "psi_ok": bool(psi_ok),
            "symmetry_delta_f_neg_mhz": dp_neg,
            "symmetry_delta_f_pos_mhz": dp_pos,
            "symmetry_deviation_mhz": (
                float(sym_dev_mhz) if np.isfinite(sym_dev_mhz) else None
            ),
            "symmetry_ok": bool(sym_ok),
        },
        "status": (
            "VALIDATED"
            if (r2 >= 0.999999 and psi_ok and sym_ok)
            else "DEVIATION"
        ),
    }

    with open(args.output, "w") as fh:
        json.dump(report, fh, indent=2)

    # ---------- Impresión ----------
    print("=" * 62)
    print("QCAL FASE V — STRESS TEST + SIMETRÍA")
    print("=" * 62)
    for s in steps:
        marker = "✅" if s["psi"] >= PSI_THRESHOLD else "❌"
        print(f"  [{s['phase']:>8}] ΔP={s['delta_p_ratio']:+.2%}  "
              f"Δf_pred={s['delta_f_predicted_mhz']:+9.4f} mHz  "
              f"Δf_med={s['delta_f_measured_mhz']:+9.4f} mHz  "
              f"Ψ={s['psi']:.6f} {marker}")
    print("-" * 62)
    print(f"Linealidad R²:            {r2:.9f}  "
          f"{'OK' if r2 >= 0.999999 else 'FAIL'}")
    print(f"Ψ mínima:                 {psi_min:.6f}  "
          f"{'OK' if psi_ok else 'FAIL'}")
    if np.isfinite(sym_dev_mhz):
        print(f"Simetría |Δf(-)+Δf(+)|:   {sym_dev_mhz:.6f} mHz  "
              f"{'OK' if sym_ok else 'FAIL'}")
    print(f"Estado global:            {report['status']}")
    print(f"Artefacto:                {args.output}")
    print("=" * 62)

    return 0 if report["status"] == "VALIDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
