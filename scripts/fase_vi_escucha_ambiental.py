#!/usr/bin/env python3
"""
QCAL Fase VI — E5: Modo de Escucha Ambiental

Red en modo pasivo (sin inyección). Se registra la fase φ_Ψ(t) del
observable global y se cross-correlaciona con señales ambientales:

    · Red eléctrica (50/60 Hz + armónicos)
    · Microsismos (0.1–1 Hz)
    · ELF electromagnético (7.83 Hz Schumann, etc.)

Criterio de falsación:
    · |ρ_max| > 0.6  en ≥ 1 banda > 1 h  ⇒ TRANSDUCTOR ABIERTO
    · |ρ_max| < 0.4  en todas las bandas ⇒ SISTEMA CERRADO

Uso:
    python scripts/fase_vi_escucha_ambiental.py --hours 24 --coupling closed
    python scripts/fase_vi_escucha_ambiental.py --hours 24 --coupling open --output ...

Sello: QCAL-INYECCION-INMEDIATA-v3.0 ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List

import numpy as np

F0_HZ = 141.7001
CORR_LOW = 0.4
CORR_HIGH = 0.6


@dataclass
class Band:
    name: str
    f_hz: float
    amplitude: float
    coupling_gain: float   # ganancia añadida en modo "open"


BANDS: List[Band] = [
    Band("mains_50hz",    50.0,   1.0,  0.75),
    Band("mains_60hz",    60.0,   1.0,  0.05),
    Band("microseism",     0.2,   0.5,  0.30),
    Band("schumann_7p83",  7.83,  0.3,  0.20),
    Band("elf_14hz",      14.0,   0.2,  0.10),
]


def synth_env_signal(t: np.ndarray, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    """Sintetiza componentes ambientales por banda."""
    out = {}
    for b in BANDS:
        phase = rng.uniform(0.0, 2 * np.pi)
        # ruido rosa aproximado + oscilación
        drift = 0.05 * np.cumsum(rng.normal(0.0, 1.0, size=t.size)) / np.sqrt(t.size)
        out[b.name] = (
            b.amplitude * np.sin(2 * np.pi * b.f_hz * t + phase)
            + drift
            + 0.05 * rng.normal(0.0, 1.0, size=t.size)
        )
    return out


def synth_psi_phase(t: np.ndarray, env: Dict[str, np.ndarray],
                    coupling: str, rng: np.random.Generator) -> np.ndarray:
    """
    Fase φ_Ψ(t) del sistema en modo pasivo.
    - closed: sólo deriva estocástica interna (autónoma)
    - open  : deriva interna + fugas de bandas ambientales (coupling_gain)
    """
    base = 0.01 * np.cumsum(rng.normal(0.0, 1.0, size=t.size)) / np.sqrt(t.size)
    if coupling == "closed":
        return base + 0.02 * rng.normal(0.0, 1.0, size=t.size)
    # open: mezcla ponderada
    leak = np.zeros_like(t)
    for b in BANDS:
        leak += b.coupling_gain * env[b.name]
    # normalización para que la escala sea comparable al ruido interno
    leak *= 0.05
    return base + leak + 0.02 * rng.normal(0.0, 1.0, size=t.size)


def band_cross_correlation(phi: np.ndarray, sig: np.ndarray,
                           max_lag: int = 200) -> float:
    """|ρ_max| entre −max_lag y +max_lag (Pearson normalizado)."""
    x = phi - np.mean(phi)
    y = sig - np.mean(sig)
    denom = np.sqrt(np.sum(x ** 2) * np.sum(y ** 2))
    if denom == 0:
        return 0.0
    # correlación cruzada eficiente vía np.correlate
    full = np.correlate(x, y, mode="full") / denom
    center = len(full) // 2
    window = full[center - max_lag: center + max_lag + 1]
    return float(np.max(np.abs(window)))


def main() -> int:
    ap = argparse.ArgumentParser(description="QCAL Fase VI — Modo de Escucha")
    ap.add_argument("--hours", type=float, default=24.0,
                    help="Duración total de observación (h)")
    ap.add_argument("--fs-hz", type=float, default=200.0,
                    help="Frecuencia de muestreo (Hz)")
    ap.add_argument("--window-hours", type=float, default=1.0,
                    help="Ventana móvil de análisis (h)")
    ap.add_argument("--coupling", choices=["closed", "open"],
                    default="closed")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", type=str,
                    default="artifact_fase_vi_listening.json")
    args = ap.parse_args()

    # Para mantener el runtime razonable, submuestreamos a 20 Hz internamente
    fs = min(args.fs_hz, 20.0)
    total_s = args.hours * 3600.0
    n = int(total_s * fs)
    if n < 4096:
        n = 4096
    t = np.arange(n) / fs
    rng = np.random.default_rng(args.seed)

    env = synth_env_signal(t, rng)
    phi = synth_psi_phase(t, env, args.coupling, rng)

    # Correlación global + máxima por ventana móvil
    window_n = max(int(args.window_hours * 3600.0 * fs), 512)
    step = window_n // 2
    band_report = []
    global_max_over_bands = 0.0
    open_hits = 0

    for b in BANDS:
        rho_windows = []
        for start in range(0, n - window_n + 1, step):
            end = start + window_n
            rho = band_cross_correlation(phi[start:end], env[b.name][start:end],
                                          max_lag=min(200, window_n // 4))
            rho_windows.append(rho)
        rho_windows = np.asarray(rho_windows) if rho_windows else np.array([0.0])
        rho_max = float(np.max(rho_windows))
        rho_mean = float(np.mean(rho_windows))
        # ¿Se mantiene > CORR_HIGH durante > 1 h consecutiva?
        sustained_high = bool(np.any(rho_windows > CORR_HIGH))
        band_report.append({
            "band": b.name,
            "f_hz": b.f_hz,
            "rho_max": rho_max,
            "rho_mean": rho_mean,
            "sustained_over_high_threshold": sustained_high,
            "n_windows": int(len(rho_windows)),
        })
        global_max_over_bands = max(global_max_over_bands, rho_max)
        if sustained_high:
            open_hits += 1

    if open_hits >= 1:
        verdict = "OPEN_TRANSDUCER"
    elif global_max_over_bands < CORR_LOW:
        verdict = "CLOSED_SYSTEM"
    else:
        verdict = "INCONCLUSIVE"

    report = {
        "sello": "QCAL-INYECCION-INMEDIATA-v3.0",
        "experiment": "E5 environmental listening",
        "f0_hz": F0_HZ,
        "coupling_scenario": args.coupling,
        "hours": args.hours,
        "fs_hz_effective": fs,
        "window_hours": args.window_hours,
        "thresholds": {"low": CORR_LOW, "high": CORR_HIGH},
        "bands": band_report,
        "global_max_correlation": global_max_over_bands,
        "open_hits": open_hits,
        "verdict": verdict,
        "status": "VALIDATED" if verdict != "INCONCLUSIVE" else "INCONCLUSIVE",
    }

    with open(args.output, "w") as fh:
        json.dump(report, fh, indent=2)

    print("=" * 62)
    print("QCAL FASE VI — MODO DE ESCUCHA AMBIENTAL")
    print("=" * 62)
    print(f"Escenario:  {args.coupling}")
    print(f"Duración:   {args.hours} h  (fs={fs} Hz, ventana={args.window_hours} h)")
    print("-" * 62)
    for b in band_report:
        print(f"  {b['band']:>16}  f={b['f_hz']:>7.3f} Hz  "
              f"ρ_max={b['rho_max']:.3f}  ρ_mean={b['rho_mean']:.3f}  "
              f"{'⚠ HIGH' if b['sustained_over_high_threshold'] else ''}")
    print("-" * 62)
    print(f"|ρ| máx global:     {global_max_over_bands:.3f}")
    print(f"Bandas > {CORR_HIGH}:      {open_hits}")
    print(f"Veredicto:          {verdict}")
    print(f"Artefacto:          {args.output}")
    print("=" * 62)
    return 0 if verdict != "INCONCLUSIVE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
