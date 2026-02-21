#!/usr/bin/env python3
"""
ROC Benchmark: Ψ vs. SNR Detector Comparison
=============================================

Constructs Receiver Operating Characteristic (ROC) curves and computes
AUC (Area Under the Curve) to compare three detectors:

- D_SNR  : Standard band-limited power estimator (Welch)
- D_Psi  : Coherence-based metric Ψ = I(f₀) · A_eff²  (power × coherence²)
- D_Coh  : Standard inter-channel coherence (without π-CODE normalisation)

Experimental setup (H₀/H₁):
  H₀ – Pure Gaussian noise (independent in both channels)
  H₁ – Coherent chirp injected at low amplitude (SNR ∈ [0.1, 5])

Reference frequency: f₀ = 141.7001 Hz  (QCAL signature)

Usage
-----
    # Quick benchmark at SNR = 0.5
    python benchmarks/roc_psi_vs_snr.py --snr 0.5 --trials 500

    # Full sweep over multiple SNR levels
    python benchmarks/roc_psi_vs_snr.py --snr-sweep --trials 1000 --save-plot

Author: Sistema QCAL ∞³
Date: 2026-02-21
"""

import argparse
import json
import sys
import warnings
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import coherence, welch

warnings.filterwarnings("ignore")

# ── sklearn is optional; we provide a pure-NumPy fallback ──────────────────
try:
    from sklearn.metrics import roc_curve, auc as sklearn_auc
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False

# ── Repository root on sys.path for shared constants ───────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

# ─── Constants ──────────────────────────────────────────────────────────────
F0 = 141.7001          # Hz – QCAL central frequency
FS = 1000              # Hz – sample rate
DURATION = 1.0         # seconds
N_SAMPLES = int(FS * DURATION)


# ─── Pure-NumPy ROC helpers (no sklearn dependency) ─────────────────────────

def _roc_curve_numpy(labels: np.ndarray, scores: np.ndarray):
    """
    Compute ROC curve using only NumPy.

    Returns
    -------
    fpr, tpr : arrays
        False-positive rate and true-positive rate at each threshold.
    """
    labels = np.asarray(labels, dtype=int)
    scores = np.asarray(scores, dtype=float)
    thresholds = np.sort(np.unique(scores))[::-1]

    n_pos = np.sum(labels == 1)
    n_neg = np.sum(labels == 0)
    if n_pos == 0 or n_neg == 0:
        return np.array([0.0, 1.0]), np.array([0.0, 1.0])

    fpr_list, tpr_list = [0.0], [0.0]
    for thr in thresholds:
        pred = (scores >= thr).astype(int)
        tp = np.sum((pred == 1) & (labels == 1))
        fp = np.sum((pred == 1) & (labels == 0))
        fpr_list.append(fp / n_neg)
        tpr_list.append(tp / n_pos)
    fpr_list.append(1.0)
    tpr_list.append(1.0)
    return np.array(fpr_list), np.array(tpr_list)


def _auc_trapz(fpr: np.ndarray, tpr: np.ndarray) -> float:
    """AUC via trapezoidal rule (compatible with NumPy 1.x and 2.x)."""
    order = np.argsort(fpr)
    if hasattr(np, "trapezoid"):        # NumPy ≥ 2.0
        return float(np.trapezoid(tpr[order], fpr[order]))
    return float(np.trapz(tpr[order], fpr[order]))  # NumPy < 2.0


def compute_roc(labels: np.ndarray, scores: np.ndarray):
    """
    Return (fpr, tpr, auc_value) using sklearn if available, else NumPy.
    """
    if _SKLEARN_AVAILABLE:
        fpr, tpr, _ = roc_curve(labels, scores)
        return fpr, tpr, float(sklearn_auc(fpr, tpr))
    fpr, tpr = _roc_curve_numpy(labels, scores)
    return fpr, tpr, _auc_trapz(fpr, tpr)


# ─── Core detector functions ─────────────────────────────────────────────────

def score_snr(x: np.ndarray, fs: int = FS, f0: float = F0) -> float:
    """
    D_SNR: spectral power at f₀ estimated via Welch's method.

    Parameters
    ----------
    x   : single-channel time series
    fs  : sample rate (Hz)
    f0  : target frequency (Hz)

    Returns
    -------
    float – PSD value at the bin closest to f0
    """
    f, pxx = welch(x, fs=fs, nperseg=fs // 2)
    idx = int(np.argmin(np.abs(f - f0)))
    return float(pxx[idx])


def score_psi(x: np.ndarray, y: np.ndarray,
              fs: int = FS, f0: float = F0) -> float:
    """
    D_Ψ: Ψ = I(f₀) · A_eff²

    ``scipy.signal.coherence`` already returns the magnitude-squared
    coherence (MSC = A_eff²), so no further squaring is applied.

    Parameters
    ----------
    x, y : two-channel time series (should be coherent under H₁)
    fs   : sample rate (Hz)
    f0   : target frequency (Hz)

    Returns
    -------
    float – Ψ score
    """
    f_p, pxx = welch(x, fs=fs, nperseg=fs // 2)
    idx_p = int(np.argmin(np.abs(f_p - f0)))

    f_c, cxy = coherence(x, y, fs=fs, nperseg=fs // 2)
    idx_c = int(np.argmin(np.abs(f_c - f0)))

    # cxy is already A_eff² (magnitude-squared coherence)
    return float(pxx[idx_p] * cxy[idx_c])


def score_coh(x: np.ndarray, y: np.ndarray,
              fs: int = FS, f0: float = F0) -> float:
    """
    D_Coh: standard inter-channel coherence at f₀ (no π-CODE normalisation).

    Parameters
    ----------
    x, y : two-channel time series
    fs   : sample rate (Hz)
    f0   : target frequency (Hz)

    Returns
    -------
    float – coherence value at f₀
    """
    f_c, cxy = coherence(x, y, fs=fs, nperseg=fs // 2)
    idx_c = int(np.argmin(np.abs(f_c - f0)))
    return float(cxy[idx_c])


# ─── Monte-Carlo trial engine ─────────────────────────────────────────────────

def run_benchmark(n_trials: int = 500,
                  snr: float = 0.5,
                  fs: int = FS,
                  f0: float = F0,
                  seed: int | None = None) -> dict:
    """
    Run Monte-Carlo ROC benchmark.

    H₀: independent Gaussian noise in both channels.
    H₁: coherent sinusoidal chirp at *f0* added to noise in both channels.
    Trials are drawn 50 % H₀ / 50 % H₁.

    Parameters
    ----------
    n_trials : int
        Total number of trials (H₀ + H₁).
    snr : float
        Signal amplitude relative to noise standard deviation.
    fs : int
        Sample rate (Hz).
    f0 : float
        Signal frequency (Hz).
    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    dict with keys:
        labels        – binary array (0=noise, 1=signal)
        scores_snr    – D_SNR scores
        scores_psi    – D_Ψ scores
        scores_coh    – D_Coh scores
        auc_snr       – AUC for D_SNR
        auc_psi       – AUC for D_Ψ
        auc_coh       – AUC for D_Coh
        roc_snr       – (fpr, tpr) tuple
        roc_psi       – (fpr, tpr) tuple
        roc_coh       – (fpr, tpr) tuple
        params        – experiment parameters dict
    """
    rng = np.random.default_rng(seed)

    duration = 1.0
    t = np.linspace(0, duration, fs)

    scores_snr_list: list[float] = []
    scores_psi_list: list[float] = []
    scores_coh_list: list[float] = []
    labels_list: list[int] = []

    for _ in range(n_trials):
        noise1 = rng.standard_normal(fs)
        noise2 = rng.standard_normal(fs)

        is_signal = rng.integers(0, 2) == 1
        if is_signal:
            s = np.sin(2 * np.pi * f0 * t)
            x = snr * s + noise1
            y = snr * s + noise2
            labels_list.append(1)
        else:
            x, y = noise1, noise2
            labels_list.append(0)

        scores_snr_list.append(score_snr(x, fs=fs, f0=f0))
        scores_psi_list.append(score_psi(x, y, fs=fs, f0=f0))
        scores_coh_list.append(score_coh(x, y, fs=fs, f0=f0))

    labels = np.array(labels_list, dtype=int)
    scores_snr = np.array(scores_snr_list)
    scores_psi = np.array(scores_psi_list)
    scores_coh = np.array(scores_coh_list)

    fpr_snr, tpr_snr, auc_snr = compute_roc(labels, scores_snr)
    fpr_psi, tpr_psi, auc_psi = compute_roc(labels, scores_psi)
    fpr_coh, tpr_coh, auc_coh = compute_roc(labels, scores_coh)

    return {
        "labels": labels,
        "scores_snr": scores_snr,
        "scores_psi": scores_psi,
        "scores_coh": scores_coh,
        "auc_snr": auc_snr,
        "auc_psi": auc_psi,
        "auc_coh": auc_coh,
        "roc_snr": (fpr_snr, tpr_snr),
        "roc_psi": (fpr_psi, tpr_psi),
        "roc_coh": (fpr_coh, tpr_coh),
        "params": {"n_trials": n_trials, "snr": snr, "fs": fs, "f0": f0},
    }


def snr_sweep(snr_values=None, n_trials: int = 500,
              fs: int = FS, f0: float = F0,
              seed: int = 42) -> list[dict]:
    """
    Run benchmark across multiple SNR values.

    Parameters
    ----------
    snr_values : list of float
        SNR levels to evaluate. Default: [0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
    n_trials : int
        Trials per SNR level.
    fs, f0 : int, float
        Sample rate and target frequency.
    seed : int
        Base random seed (incremented per SNR level for independence).

    Returns
    -------
    List of result dicts (one per SNR level), each containing the benchmark
    results plus `snr` key.
    """
    if snr_values is None:
        snr_values = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0]

    results = []
    for i, snr_val in enumerate(snr_values):
        res = run_benchmark(n_trials=n_trials, snr=snr_val, fs=fs, f0=f0,
                            seed=seed + i)
        res["snr"] = snr_val
        results.append(res)
    return results


# ─── Plotting helpers ────────────────────────────────────────────────────────

def plot_roc(result: dict, output_path: str | None = None):
    """
    Plot ROC curves for a single SNR level.

    Parameters
    ----------
    result      : dict returned by :func:`run_benchmark`
    output_path : file path to save the figure (PNG).  If None, figure is
                  displayed interactively.
    """
    snr_val = result["params"]["snr"]
    fpr_snr, tpr_snr = result["roc_snr"]
    fpr_psi, tpr_psi = result["roc_psi"]
    fpr_coh, tpr_coh = result["roc_coh"]

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr_snr, tpr_snr, label=f"D_SNR  AUC={result['auc_snr']:.3f}",
            color="steelblue", lw=2)
    ax.plot(fpr_psi, tpr_psi, label=f"D_Ψ    AUC={result['auc_psi']:.3f}",
            color="darkorange", lw=2, linestyle="--")
    ax.plot(fpr_coh, tpr_coh, label=f"D_Coh  AUC={result['auc_coh']:.3f}",
            color="green", lw=2, linestyle=":")
    ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5, label="Random (AUC=0.5)")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(
        f"ROC Curve – Ψ vs SNR  (f₀={F0} Hz, SNR={snr_val}, "
        f"n={result['params']['n_trials']})"
    )
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
        print(f"  📊 ROC plot saved → {output_path}")
    else:
        plt.show()
    plt.close(fig)


def plot_auc_vs_snr(sweep_results: list[dict],
                    output_path: str | None = None):
    """
    Plot AUC as a function of SNR for the three detectors.

    Parameters
    ----------
    sweep_results : list of dicts from :func:`snr_sweep`
    output_path   : save path (PNG). If None, displayed interactively.
    """
    snr_vals = [r["snr"] for r in sweep_results]
    auc_snr = [r["auc_snr"] for r in sweep_results]
    auc_psi = [r["auc_psi"] for r in sweep_results]
    auc_coh = [r["auc_coh"] for r in sweep_results]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(snr_vals, auc_snr, "o-", color="steelblue",
            label="D_SNR", lw=2)
    ax.plot(snr_vals, auc_psi, "s--", color="darkorange",
            label="D_Ψ (coherence×power)", lw=2)
    ax.plot(snr_vals, auc_coh, "^:", color="green",
            label="D_Coh", lw=2)
    ax.axhline(0.5, color="grey", lw=1, linestyle="--", alpha=0.6,
               label="Random baseline")
    ax.set_xlabel("Signal-to-Noise Ratio (SNR)")
    ax.set_ylabel("AUC")
    ax.set_title(f"AUC vs SNR  (f₀={F0} Hz)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
        print(f"  📊 AUC-vs-SNR plot saved → {output_path}")
    else:
        plt.show()
    plt.close(fig)


# ─── Report ──────────────────────────────────────────────────────────────────

def print_report(result: dict):
    """Print a human-readable report for a single benchmark result."""
    p = result["params"]
    print()
    print("=" * 64)
    print("  📋 INFORME DE COMBATE: Ψ vs. SNR (Benchmark ROC)")
    print("=" * 64)
    print(f"  f₀             : {p['f0']} Hz")
    print(f"  SNR            : {p['snr']}")
    print(f"  Trials         : {p['n_trials']}")
    print(f"  Sample rate    : {p['fs']} Hz")
    print()
    print("  Detector           AUC")
    print("  ─────────────────────────────────")
    print(f"  D_SNR  (potencia)  {result['auc_snr']:.4f}")
    print(f"  D_Ψ    (Ψ-metric)  {result['auc_psi']:.4f}")
    print(f"  D_Coh  (coherencia){result['auc_coh']:.4f}")
    print()
    winner = max(
        [("D_SNR", result["auc_snr"]),
         ("D_Ψ",   result["auc_psi"]),
         ("D_Coh", result["auc_coh"])],
        key=lambda x: x[1],
    )
    print(f"  🏆 Mejor detector: {winner[0]}  (AUC={winner[1]:.4f})")
    print("=" * 64)


def save_results(results: list[dict] | dict, output_path: str):
    """
    Serialise benchmark results to a JSON file.

    Arrays are converted to lists for JSON compatibility.
    """
    def _serialise(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if isinstance(obj, dict):
            return {k: _serialise(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_serialise(i) for i in obj]
        return obj

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "f0_hz": F0,
        "results": _serialise(results) if isinstance(results, list)
                   else _serialise(results),
    }
    with open(output_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"  💾 Results saved → {output_path}")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="ROC Benchmark: Ψ vs. SNR detector comparison"
    )
    p.add_argument("--snr", type=float, default=0.5,
                   help="Signal-to-noise ratio for single-SNR run (default: 0.5)")
    p.add_argument("--trials", type=int, default=500,
                   help="Number of Monte-Carlo trials (default: 500)")
    p.add_argument("--snr-sweep", action="store_true",
                   help="Run sweep over SNR ∈ {0.1,0.25,0.5,1,2,5}")
    p.add_argument("--snr-values", nargs="+", type=float,
                   metavar="VAL",
                   help="Custom SNR values for sweep (overrides default sweep)")
    p.add_argument("--save-plot", action="store_true",
                   help="Save ROC plots to benchmarks/results/")
    p.add_argument("--save-json", action="store_true",
                   help="Save results JSON to benchmarks/results/")
    p.add_argument("--seed", type=int, default=42,
                   help="Random seed (default: 42)")
    return p


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    if args.snr_sweep or args.snr_values:
        snr_vals = args.snr_values if args.snr_values else None
        print(f"\n🔬 SNR sweep  (trials/level={args.trials})")
        sweep = snr_sweep(snr_values=snr_vals, n_trials=args.trials,
                          seed=args.seed)
        for res in sweep:
            print_report(res)

        if args.save_plot:
            path = results_dir / "auc_vs_snr.png"
            plot_auc_vs_snr(sweep, output_path=str(path))
            # Also save individual ROC for low-SNR regime
            for res in sweep:
                snr_tag = f"{res['snr']:.2f}".replace(".", "p")
                plot_roc(res, output_path=str(
                    results_dir / f"roc_snr{snr_tag}.png"))

        if args.save_json:
            save_results(sweep,
                         str(results_dir / "roc_psi_sweep_results.json"))

    else:
        print(f"\n🔬 Single-SNR benchmark  (SNR={args.snr}, "
              f"trials={args.trials})")
        result = run_benchmark(n_trials=args.trials, snr=args.snr,
                               seed=args.seed)
        print_report(result)

        if args.save_plot:
            snr_tag = f"{args.snr:.2f}".replace(".", "p")
            plot_roc(result,
                     output_path=str(
                         results_dir / f"roc_psi_snr{snr_tag}.png"))

        if args.save_json:
            save_results(result,
                         str(results_dir / "roc_psi_single_result.json"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
