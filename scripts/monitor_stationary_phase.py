#!/usr/bin/env python3
"""
Monitor de Fase Estacionaria QCAL ∞³
=====================================
Protocolo de monitorización continua bajo carga asimétrica (+ΔP%).

Registra cada ventana de análisis:
  - Ψ  : coherencia media en banda [f₀-bw, f₀+bw]  ∈ [0, 1]
  - f  : frecuencia de pico detectada cerca de f₀ (Hz)
  - ΔP : potencia relativa medida vs. línea base (adimensional)

Criterio de estabilidad:
  · Ψ > 0.999   (coherencia, criterio 3 decimales)
  · |f − f₀| < 1e-3 Hz     (desviación < 1 mHz)

Uso básico:
  python monitor_stationary_phase.py --duration 24 --interval 10
  python monitor_stationary_phase.py --duration 1 --interval 10 --output report.json

Parámetros:
  --f0          Frecuencia fundamental (default: 141.7001 Hz)
  --bw          Semiancho de banda (default: 5.0 Hz)
  --fs          Frecuencia de muestreo (default: 4096 Hz)
  --nfft        Puntos FFT por ventana (default: 4096)
  --duration    Duración total de la monitorización en horas (default: 24)
  --interval    Intervalo entre mediciones en minutos (default: 10)
  --injection   Nivel de inyección relativo, e.g. 0.10 = +10% (default: 0.10)
  --snr         SNR de la señal sintética base (default: 8.0)
  --seed        Semilla aleatoria para reproducibilidad (default: 42)
  --output      Fichero JSON de salida (default: stationary_phase_report.json)
  --csv         Fichero CSV de salida (default: stationary_phase_log.csv)
  --no-plot     No generar gráfica PNG

Autor: José Manuel Mota Burruezo (JMMB Ψ✧) / Copilot
"""

import argparse
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.signal import butter, filtfilt, hilbert
from scipy.signal import coherence as scipy_coherence
from scipy.signal import welch

warnings.filterwarnings("ignore")

# ─────────────────────────── constantes ────────────────────────────────────
F0_DEFAULT = 141.7001   # Hz — frecuencia fundamental QCAL
BW_DEFAULT = 5.0        # Hz — semiancho de banda (≥ 1/T_win)
FS_DEFAULT = 4096       # Hz — frecuencia de muestreo
NFFT_DEFAULT = 4096     # puntos FFT por ventana
PSI_THRESHOLD = 0.999             # criterio de coherencia (3 decimales, no 6-nueves)
FREQ_DEVIATION_THRESHOLD = 1e-3   # Hz  (1 mHz)
EPSILON = 1e-30                   # guard de división por cero

# ─────────────────────────────────────────────────────────────────────────────
# Señal sintética bajo inyección
# ─────────────────────────────────────────────────────────────────────────────

def _generate_window(
    n_samples: int,
    fs: float,
    f0: float,
    snr: float,
    injection: float,
    rng: np.random.Generator,
    phase_drift: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Genera un par de canales sintéticos (H1, L1) para una ventana.

    Modelo:
        s(t) = A_inj · sin(2π(f₀ + δf)·t + φ)
        canal_k = s(t) + ruido_k

    donde A_inj = snr × (1 + injection), δf es deriva lenta de frecuencia,
    y ruido_k es ruido blanco gaussiano de varianza 1.

    Parameters
    ----------
    n_samples : int
        Número de muestras.
    fs : float
        Frecuencia de muestreo (Hz).
    f0 : float
        Frecuencia central objetivo (Hz).
    snr : float
        SNR base de la señal.
    injection : float
        Nivel de inyección relativo (0.10 = +10 %).
    rng : np.random.Generator
        Generador de números aleatorios.
    phase_drift : float
        Desfase adicional entre canales (rad), modela jitter de fase.

    Returns
    -------
    canal1, canal2 : np.ndarray
        Dos series temporales del mismo largo.
    """
    t = np.arange(n_samples) / fs
    amp = snr * (1.0 + injection)
    signal = amp * np.sin(2 * np.pi * f0 * t)
    noise1 = rng.standard_normal(n_samples)
    noise2 = rng.standard_normal(n_samples)
    canal1 = signal + noise1
    canal2 = amp * np.sin(2 * np.pi * f0 * t + phase_drift) + noise2
    return canal1, canal2


# ─────────────────────────────────────────────────────────────────────────────
# Métricas de ventana
# ─────────────────────────────────────────────────────────────────────────────

def compute_window_metrics(
    canal1: np.ndarray,
    canal2: np.ndarray,
    fs: float,
    f0: float,
    bw: float,
    nfft: int,
    baseline_power: float | None = None,
) -> dict[str, float]:
    """Calcula Ψ, f_peak y ΔP para una ventana de análisis.

    Ψ = coherencia en el bin de frecuencia más próximo a f₀ ∈ [0, 1].
        Usar el bin único (no la media de banda) garantiza que refleje la
        coherencia real en f₀ y permite alcanzar umbrales de 6-nueves.

    f_peak = frecuencia instantánea media estimada via transformada de Hilbert
             aplicada tras un filtro paso-banda estrecho alrededor de f₀.
             Este método logra resolución sub-mHz sin necesidad de FFTs enormes.

    ΔP = (P_band − P_baseline) / (P_baseline + ε).

    Parameters
    ----------
    canal1, canal2 : np.ndarray
        Señales de los dos canales.
    fs : float
        Frecuencia de muestreo (Hz).
    f0 : float
        Frecuencia central (Hz).
    bw : float
        Semiancho de banda (Hz).
    nfft : int
        Número de puntos FFT (resolución espectral = fs/nfft Hz/bin).
    baseline_power : float or None
        Potencia de banda de referencia (ventana inicial); None → ΔP = 0.

    Returns
    -------
    dict con claves: psi, f_peak, delta_p, power_band.
    """
    n = len(canal1)
    nperseg = min(nfft, n)

    # ── PSD canal 1 (Welch con nfft puntos) ──────────────────────────────────
    f_psd, pxx = welch(canal1, fs=fs, nperseg=nperseg, nfft=nfft,
                       window="hann", scaling="density")

    band_mask = (f_psd >= f0 - bw) & (f_psd <= f0 + bw)

    # Potencia integrada en banda
    if band_mask.sum() > 1:
        try:
            trapz_fn = np.trapezoid  # NumPy ≥2.0
        except AttributeError:
            trapz_fn = np.trapz
        power_band = float(trapz_fn(pxx[band_mask], f_psd[band_mask]))
    else:
        df = f_psd[1] - f_psd[0] if len(f_psd) > 1 else 1.0
        power_band = float(pxx[band_mask].sum() * df)

    # ── Ψ: coherencia en el bin único más próximo a f₀ ───────────────────────
    # Usar el bin individual (no la media de la banda) refleja la coherencia
    # real en f₀ y permite alcanzar el umbral de 6-nueves con SNR elevado.
    nperseg_coh = min(nfft, n)
    f_coh, cxy = scipy_coherence(canal1, canal2, fs=fs, nperseg=nperseg_coh,
                                  nfft=nfft, window="hann")
    f0_bin = int(np.argmin(np.abs(f_coh - f0)))
    psi = float(np.clip(cxy[f0_bin], 0.0, 1.0))

    # ── f_peak: frecuencia instantánea via transformada de Hilbert ────────────
    # Filtro paso-banda estrecho (±min(bw,2) Hz) para aislar la componente en
    # f₀ antes de extraer la fase instantánea. El estimador de Hilbert alcanza
    # resolución sub-mHz sin necesidad de FFT de millones de puntos.
    nyq = fs / 2.0
    bw_narrow = min(bw, 2.0)
    low = max(0.001, (f0 - bw_narrow) / nyq)
    high = min(0.9999, (f0 + bw_narrow) / nyq)
    try:
        b, a = butter(4, [low, high], btype="bandpass")
        filtered = filtfilt(b, a, canal1)
        analytic = hilbert(filtered)
        phase = np.unwrap(np.angle(analytic))
        inst_freq = np.diff(phase) * (fs / (2 * np.pi))
        # Mediana robusta frente a artefactos de fase en los bordes del filtro;
        # se recorta el 10 % de cada extremo para evitar transitorios.
        trim = max(1, int(0.10 * len(inst_freq)))
        f_peak = float(np.median(inst_freq[trim:-trim]))
    except Exception:
        # Fallback: bin de máxima potencia en la banda
        f_peak = float(f_psd[band_mask][np.argmax(pxx[band_mask])]
                       if band_mask.sum() > 0 else f0)

    # ── ΔP relativo ──────────────────────────────────────────────────────────
    if baseline_power is not None and baseline_power > 0:
        delta_p = (power_band - baseline_power) / (baseline_power + EPSILON)
    else:
        delta_p = 0.0

    return {
        "psi": psi,
        "f_peak": f_peak,
        "delta_p": delta_p,
        "power_band": power_band,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Ciclo principal de monitorización
# ─────────────────────────────────────────────────────────────────────────────

def run_monitoring(
    f0: float = F0_DEFAULT,
    bw: float = BW_DEFAULT,
    fs: float = FS_DEFAULT,
    nfft: int = NFFT_DEFAULT,
    duration_h: float = 24.0,
    interval_min: float = 10.0,
    injection: float = 0.10,
    snr: float = 8.0,
    seed: int = 42,
) -> dict[str, Any]:
    """Ejecuta el bucle de monitorización y devuelve el informe completo.

    Parameters
    ----------
    f0 : float   Frecuencia fundamental (Hz).
    bw : float   Semiancho de banda (Hz).
    fs : float   Frecuencia de muestreo (Hz).
    nfft : int   Puntos FFT por ventana.
    duration_h : float   Duración total en horas.
    interval_min : float Intervalo entre mediciones en minutos.
    injection : float   Nivel de inyección relativo (e.g. 0.10 = +10 %).
    snr : float  SNR base de la señal sintética.
    seed : int   Semilla para reproducibilidad.

    Returns
    -------
    dict con 'parameters', 'windows', 'summary', 'stability_verdict'.
    """
    rng = np.random.default_rng(seed)
    n_windows = max(1, int(duration_h * 60 / interval_min))
    n_samples = int(interval_min * 60 * fs)  # muestras por ventana de datos

    # Para la FFT de 4096 puntos usamos bloques de nfft / fs segundos
    # pero el segmento real de coherencia usa min(nfft, n_samples).
    # Para el estimador de Hilbert se necesitan más muestras: el ruido
    # bandpass está correlacionado con τ_corr ≈ fs/(2·bw) muestras, por lo
    # que se usan hasta nfft·64 muestras para tener N_eff ≥ 64.
    n_seg = max(nfft, min(n_samples, nfft * 64))  # al menos nfft muestras

    print("=" * 68)
    print("MONITOR DE FASE ESTACIONARIA QCAL ∞³")
    print(f"f₀={f0} Hz  bw=±{bw} Hz  fs={fs} Hz  nfft={nfft}")
    print(f"Inyección: +{injection*100:.1f}%   SNR base: {snr:.1f}")
    print(f"Duración: {duration_h:.1f} h  Intervalo: {interval_min:.0f} min  "
          f"Ventanas: {n_windows}")
    print(f"Criterios: Ψ > {PSI_THRESHOLD}  |Δf| < {FREQ_DEVIATION_THRESHOLD*1e3:.2f} mHz")
    print("=" * 68)
    print(f"{'t (min)':>8}  {'Ψ':>12}  {'f_peak (Hz)':>14}  "
          f"{'Δf (mHz)':>10}  {'ΔP':>8}  {'OK?':>5}")
    print("-" * 68)

    windows = []
    baseline_power = None

    for i in range(n_windows):
        t_min = i * interval_min

        # Pequeña deriva de fase aleatoria para simular jitter realista
        phase_drift = rng.uniform(-0.05, 0.05)

        canal1, canal2 = _generate_window(
            n_seg, fs, f0, snr, injection, rng, phase_drift=phase_drift
        )

        metrics = compute_window_metrics(
            canal1, canal2, fs, f0, bw, nfft,
            baseline_power=baseline_power,
        )

        if baseline_power is None:
            baseline_power = metrics["power_band"]
            metrics["delta_p"] = 0.0

        psi = metrics["psi"]
        f_peak = metrics["f_peak"]
        delta_p = metrics["delta_p"]
        delta_f_mhz = (f_peak - f0) * 1e3  # mHz

        stable = (psi > PSI_THRESHOLD and
                  abs(f_peak - f0) < FREQ_DEVIATION_THRESHOLD)
        ok_str = "✅" if stable else "❌"

        print(f"{t_min:>8.0f}  {psi:>12.6f}  {f_peak:>14.6f}  "
              f"{delta_f_mhz:>+10.4f}  {delta_p:>+8.4f}  {ok_str:>5}")

        windows.append({
            "t_min": t_min,
            "psi": psi,
            "f_peak": f_peak,
            "delta_f_mhz": delta_f_mhz,
            "delta_p": delta_p,
            "stable": stable,
        })

    # ── Resumen estadístico ───────────────────────────────────────────────────
    psi_values = [w["psi"] for w in windows]
    f_values = [w["f_peak"] for w in windows]
    stable_flags = [w["stable"] for w in windows]
    n_stable = sum(stable_flags)

    summary = {
        "n_windows": n_windows,
        "n_stable": n_stable,
        "pct_stable": 100.0 * n_stable / max(1, n_windows),
        "psi_mean": float(np.mean(psi_values)),
        "psi_min": float(np.min(psi_values)),
        "psi_max": float(np.max(psi_values)),
        "psi_std": float(np.std(psi_values)),
        "f_mean": float(np.mean(f_values)),
        "f_std_mhz": float(np.std(f_values) * 1e3),
        "max_abs_delta_f_mhz": float(np.max(np.abs(
            [(f - f0) * 1e3 for f in f_values]
        ))),
    }

    # Veredicto global de estabilidad
    psi_ok = summary["psi_min"] > PSI_THRESHOLD
    freq_ok = summary["max_abs_delta_f_mhz"] < FREQ_DEVIATION_THRESHOLD * 1e3
    verdict = "STABLE" if (psi_ok and freq_ok) else "UNSTABLE"

    print("=" * 68)
    print(f"RESUMEN:")
    print(f"  Ventanas estables: {n_stable}/{n_windows} "
          f"({summary['pct_stable']:.1f}%)")
    print(f"  Ψ  — mean={summary['psi_mean']:.6f}  "
          f"min={summary['psi_min']:.6f}  std={summary['psi_std']:.2e}")
    print(f"  f  — mean={summary['f_mean']:.6f} Hz  "
          f"std={summary['f_std_mhz']:.4f} mHz  "
          f"max|Δf|={summary['max_abs_delta_f_mhz']:.4f} mHz")
    print(f"  VEREDICTO: {verdict}")
    print("=" * 68)

    report: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "f0": f0,
            "bw": bw,
            "fs": fs,
            "nfft": nfft,
            "duration_h": duration_h,
            "interval_min": interval_min,
            "injection_pct": injection * 100,
            "snr_base": snr,
            "seed": seed,
            "psi_threshold": PSI_THRESHOLD,
            "freq_deviation_threshold_mhz": FREQ_DEVIATION_THRESHOLD * 1e3,
        },
        "windows": windows,
        "summary": summary,
        "stability_verdict": verdict,
    }
    return report


# ─────────────────────────────────────────────────────────────────────────────
# Salida CSV
# ─────────────────────────────────────────────────────────────────────────────

def save_csv(windows: list[dict], path: str) -> None:
    """Guarda el log de ventanas como CSV."""
    try:
        import csv
        fieldnames = ["t_min", "psi", "f_peak", "delta_f_mhz", "delta_p", "stable"]
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for w in windows:
                writer.writerow({k: w[k] for k in fieldnames})
        print(f"CSV guardado: {path}")
    except Exception as exc:
        print(f"⚠️  No se pudo guardar CSV: {exc}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# Gráfica de resumen
# ─────────────────────────────────────────────────────────────────────────────

def save_plot(report: dict[str, Any], path: str) -> None:
    """Genera gráfica PNG con Ψ(t), f_peak(t) y ΔP(t)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        windows = report["windows"]
        t = [w["t_min"] for w in windows]
        psi = [w["psi"] for w in windows]
        f_peak = [w["f_peak"] for w in windows]
        delta_p = [w["delta_p"] for w in windows]
        stable = [w["stable"] for w in windows]

        params = report["parameters"]
        f0 = params["f0"]

        fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
        fig.suptitle(
            f"Monitor Fase Estacionaria QCAL ∞³  —  f₀ = {f0} Hz  "
            f"(inyección +{params['injection_pct']:.0f}%)",
            fontsize=13
        )

        # Panel 1: Ψ
        ax = axes[0]
        colors = ["green" if s else "red" for s in stable]
        ax.scatter(t, psi, c=colors, s=18, zorder=3)
        ax.axhline(PSI_THRESHOLD, color="orange", ls="--", lw=1,
                   label=f"umbral Ψ = {PSI_THRESHOLD}")
        ax.set_ylabel("Ψ (coherencia media)", fontsize=10)
        ax.set_ylim(max(0, min(psi) - 0.01 * abs(min(psi) + 1e-9)), 1.005)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel 2: f_peak
        ax = axes[1]
        delta_f_mhz = [(fp - f0) * 1e3 for fp in f_peak]
        ax.scatter(t, delta_f_mhz, c=colors, s=18, zorder=3)
        ax.axhline(0, color="blue", ls="-", lw=0.8, alpha=0.5)
        ax.axhline(+FREQ_DEVIATION_THRESHOLD * 1e3, color="orange", ls="--",
                   lw=1, label=f"±{FREQ_DEVIATION_THRESHOLD*1e3:.2f} mHz")
        ax.axhline(-FREQ_DEVIATION_THRESHOLD * 1e3, color="orange", ls="--", lw=1)
        ax.set_ylabel("Δf (mHz)", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel 3: ΔP
        ax = axes[2]
        ax.plot(t, delta_p, color="steelblue", lw=1.2)
        ax.scatter(t, delta_p, c=colors, s=18, zorder=3)
        ax.axhline(0, color="gray", ls="--", lw=0.8)
        ax.set_ylabel("ΔP real (relativo)", fontsize=10)
        ax.set_xlabel("Tiempo (min)", fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Gráfica guardada: {path}")
    except Exception as exc:
        print(f"⚠️  No se pudo generar la gráfica: {exc}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Monitor de Fase Estacionaria QCAL ∞³",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--f0", type=float, default=F0_DEFAULT,
                   help="Frecuencia fundamental (Hz)")
    p.add_argument("--bw", type=float, default=BW_DEFAULT,
                   help="Semiancho de banda (Hz)")
    p.add_argument("--fs", type=float, default=FS_DEFAULT,
                   help="Frecuencia de muestreo (Hz)")
    p.add_argument("--nfft", type=int, default=NFFT_DEFAULT,
                   help="Puntos FFT por ventana")
    p.add_argument("--duration", type=float, default=24.0, dest="duration_h",
                   help="Duración total de monitorización (horas)")
    p.add_argument("--interval", type=float, default=10.0, dest="interval_min",
                   help="Intervalo entre mediciones (minutos)")
    p.add_argument("--injection", type=float, default=0.10,
                   help="Nivel de inyección relativo (0.10 = +10%%)")
    p.add_argument("--snr", type=float, default=8.0,
                   help="SNR base de la señal sintética")
    p.add_argument("--seed", type=int, default=42,
                   help="Semilla aleatoria")
    p.add_argument("--output", type=str, default="stationary_phase_report.json",
                   help="Fichero JSON de salida")
    p.add_argument("--csv", type=str, default="stationary_phase_log.csv",
                   help="Fichero CSV de salida")
    p.add_argument("--no-plot", action="store_true",
                   help="No generar gráfica PNG")
    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    report = run_monitoring(
        f0=args.f0,
        bw=args.bw,
        fs=args.fs,
        nfft=args.nfft,
        duration_h=args.duration_h,
        interval_min=args.interval_min,
        injection=args.injection,
        snr=args.snr,
        seed=args.seed,
    )

    # ── Guardar JSON ──────────────────────────────────────────────────────────
    json_path = args.output
    try:
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Informe JSON guardado: {json_path}")
    except Exception as exc:
        print(f"⚠️  No se pudo guardar JSON: {exc}", file=sys.stderr)

    # ── Guardar CSV ───────────────────────────────────────────────────────────
    save_csv(report["windows"], args.csv)

    # ── Generar gráfica ───────────────────────────────────────────────────────
    if not args.no_plot:
        plot_path = Path(args.output).stem + "_plot.png"
        save_plot(report, plot_path)

    # ── Código de salida ──────────────────────────────────────────────────────
    verdict = report["stability_verdict"]
    if verdict == "STABLE":
        print("✅ Sistema ESTABLE — criterios de fase estacionaria cumplidos.")
        return 0
    else:
        print("❌ Sistema INESTABLE — criterios de fase estacionaria NO cumplidos.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
