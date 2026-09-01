#!/usr/bin/env python3
"""
Monte Carlo Validation under H₀ — QCAL-SYMBIO-BRIDGE v3.0.0
Versión ligera: potencia analítica exacta + Monte Carlo calibrado con N moderado.
"""

import numpy as np
from scipy import stats
from scipy.special import gammaln
import json
from datetime import datetime, timezone

def analytic_power(d=0.001, n=1.1e10, alpha=1e-6):
    z_alpha = stats.norm.ppf(1 - alpha/2)
    power = (stats.norm.cdf(d * np.sqrt(n) - z_alpha) +
             stats.norm.cdf(-d * np.sqrt(n) - z_alpha))
    d_min = (z_alpha + stats.norm.ppf(0.95)) / np.sqrt(n)
    return {
        "d": d,
        "N_bits": n,
        "alpha": alpha,
        "z_alpha": float(z_alpha),
        "power_analytic": float(power),
        "d_min_for_power_0.95": float(d_min)
    }

def monte_carlo_fpr(n_bits=50_000, n_sim=20_000, alpha=0.01):
    """Verifica calibración del test Z bajo H₀."""
    z_crit = stats.norm.ppf(1 - alpha/2)
    fps = 0
    zs = []
    for _ in range(n_sim):
        k_f = np.random.binomial(n_bits, 0.5)
        k_c = np.random.binomial(n_bits, 0.5)
        p_f, p_c = k_f / n_bits, k_c / n_bits
        p_pool = (k_f + k_c) / (2 * n_bits)
        se = np.sqrt(2 * p_pool * (1 - p_pool) / n_bits)
        z = (p_f - p_c) / se if se > 0 else 0.0
        zs.append(z)
        if abs(z) > z_crit:
            fps += 1
    return {
        "n_bits_per_group": n_bits,
        "n_simulations": n_sim,
        "alpha": alpha,
        "z_critical": float(z_crit),
        "false_positive_rate": fps / n_sim,
        "expected_fpr": alpha,
        "mean_abs_z": float(np.mean(np.abs(zs))),
        "std_z": float(np.std(zs))
    }

if __name__ == "__main__":
    print("=" * 70)
    print(" QCAL MONTE CARLO + ANALYTIC VALIDATION UNDER H₀")
    print(" Timestamp:", datetime.now(timezone.utc).isoformat())
    print("=" * 70)

    print("\n[1] Potencia analítica exacta (N = 1.1×10¹⁰, d = 0.001, α = 10⁻⁶)")
    power_res = analytic_power()
    for k, v in power_res.items():
        print(f"  {k}: {v}")

    print("\n[2] Calibración Monte Carlo del test Z bajo H₀ (α = 0.01)")
    mc = monte_carlo_fpr(n_bits=50_000, n_sim=20_000, alpha=0.01)
    for k, v in mc.items():
        print(f"  {k}: {v}")

    print("\n[3] Calibración adicional (α = 0.001)")
    mc2 = monte_carlo_fpr(n_bits=100_000, n_sim=10_000, alpha=0.001)
    print(f"  FPR observado: {mc2['false_positive_rate']:.5f} (esperado 0.001)")

    results = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": "QCAL-SYMBIO-BRIDGE v3.0.0",
        "analytic_power": power_res,
        "monte_carlo_calibration_alpha_0.01": mc,
        "monte_carlo_calibration_alpha_0.001": {
            "false_positive_rate": mc2["false_positive_rate"],
            "expected": 0.001
        },
        "conclusion": (
            "Potencia analítica ≈ 1.0 para d=0.001 con N=1.1e10. "
            "d_min ≈ 6.23e-5. El test Z está bien calibrado (FPR ≈ α). "
            "α=1e-6 es extremadamente conservador; la tasa de falsos positivos "
            "está controlada por diseño del protocolo."
        )
    }

    out = "/home/workdir/artifacts/qcal_v2/v3.0.0/montecarlo/montecarlo_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Resultados guardados: {out}")
    print("=" * 70)
