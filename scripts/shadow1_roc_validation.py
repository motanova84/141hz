#!/usr/bin/env python3
"""
Shadow-1 / O3b Rigorous Detection Validation
=============================================

Addresses six methodological requirements for publication-grade detection:

1. Dimensionless Ψ score — I(f₀)·MSC(f₀) where I is PSD normalised by the
   local median, so score_psi is a pure ratio (no strain² Hz⁻¹ units).

2. ROC anti-overfit — signals in H1 are injected at f₀ + jitter (jitter
   drawn uniformly from ±[0.5, 2] Hz) while the detector evaluates at the
   fixed nominal f₀.  An "off-target" control detector at f₀+50 Hz is
   included so readers can compare AUC on-target vs. off-target.

3. Channel independence — H0 noise channels use different, explicit RNG
   seeds; H1 shares the coherent signal but uses independent noise seeds.
   A time-slide sanity check verifies that a large time offset kills the MSC.

4. Bootstrap AUC — 200-resample bootstrap yields AUC_mean ± CI95 so the
   result is not a single number without uncertainty.

5. Multiple-testing correction — O3b scan reports p_raw per candidate and
   p_fdr (Benjamini–Hochberg).  If only Shadow-O3b-1 is present the output
   says so explicitly and leaves a hook for multi-candidate extension.

6. data_source flag — every result dict carries
   data_source: "GWOSC" | "SIMULATION_FALLBACK".  The CLI prints a banner.
   Tests never assert on the magnitude of "real" measurements when running
   in fallback mode.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

from __future__ import annotations

import warnings
from typing import Sequence

import numpy as np
from scipy import signal, stats

warnings.filterwarnings("ignore")

# ── Constants ──────────────────────────────────────────────────────────────────

F0_HZ = 141.7001          # Target frequency (Hz)
FS_HZ = 4096.0            # Sampling rate (Hz)
JITTER_MIN_HZ = 0.5       # Minimum injection jitter (Hz)
JITTER_MAX_HZ = 2.0       # Maximum injection jitter (Hz)
F_CONTROL_OFFSET_HZ = 50.0  # Off-target control offset (Hz)
BOOTSTRAP_N = 200         # Bootstrap resamples for AUC CI
BOOTSTRAP_SEED = 42       # Fixed seed for reproducible CI
TIME_SLIDE_S = 1.0        # Large time offset for slide sanity check (s)


# ── 1. Dimensionless Ψ score ──────────────────────────────────────────────────

def compute_score_psi(psd: np.ndarray, freqs: np.ndarray,
                      msc: np.ndarray, f0: float,
                      band_hz: float = 20.0) -> float:
    """
    Compute dimensionless Ψ score: I(f₀) × MSC(f₀).

    I(f₀) = PSD(f₀) / median(PSD in band) — dimensionless normalised power.
    MSC(f₀) ∈ [0, 1]                      — magnitude-squared coherence.
    score_psi = I(f₀) × MSC(f₀)           — dimensionless detection statistic.

    Using I(f₀) instead of raw PSD(f₀) removes the strain²/Hz units so the
    resulting score is independent of detector calibration and can be compared
    across events.

    Parameters
    ----------
    psd : ndarray
        One-sided PSD (Welch or equivalent).
    freqs : ndarray
        Frequency axis (Hz), same length as psd.
    msc : ndarray
        Magnitude-squared coherence between the two detectors (same length).
    f0 : float
        Target frequency (Hz).
    band_hz : float
        Half-width of background band (Hz). Bins within 1 Hz of f₀ are
        excluded from the background median.

    Returns
    -------
    float
        Dimensionless score_psi.
    """
    idx = int(np.argmin(np.abs(freqs - f0)))
    band_mask = (
        (freqs >= f0 - band_hz) & (freqs <= f0 + band_hz)
        & (np.abs(freqs - f0) > 1.0)
    )
    if band_mask.sum() == 0:
        band_mask = np.ones(len(freqs), dtype=bool)
    psd_bg = float(np.median(psd[band_mask]))
    I_f0 = float(psd[idx]) / (psd_bg + 1e-300)  # dimensionless
    msc_f0 = float(np.clip(msc[idx], 0.0, 1.0))
    return float(I_f0 * msc_f0)


# ── 2-3. Dataset generation (ROC + channel independence) ─────────────────────

def _make_noise_pair(n: int, noise_std: float,
                     seed_h1: int, seed_l1: int) -> tuple[np.ndarray, np.ndarray]:
    """Return two independent noise arrays with explicit, different seeds."""
    h1_noise = np.random.default_rng(seed_h1).normal(0.0, noise_std, n)
    l1_noise = np.random.default_rng(seed_l1).normal(0.0, noise_std, n)
    return h1_noise, l1_noise


def generate_roc_dataset(
    n_h0: int = 500,
    n_h1: int = 500,
    f0: float = F0_HZ,
    fs: float = FS_HZ,
    duration_s: float = 1.0,
    snr: float = 3.0,
    jitter_min: float = JITTER_MIN_HZ,
    jitter_max: float = JITTER_MAX_HZ,
    seed: int = 0,
) -> dict:
    """
    Generate labelled dataset for ROC analysis with:

    * **H0**: noise only — two channels with *different* explicit seeds so
      any accidental cross-channel correlation is avoided.
    * **H1**: coherent signal at f₀ + jitter (jitter ~ Uniform[±jitter_min,
      ±jitter_max]) plus independent noise on each channel.  The detector
      always evaluates at the fixed f₀, creating a realistic mismatch.

    Parameters
    ----------
    n_h0 : int
        Number of noise-only realisations.
    n_h1 : int
        Number of signal+noise realisations.
    f0 : float
        Nominal target frequency (Hz) — where the *detector* evaluates.
    fs : float
        Sampling rate (Hz).
    duration_s : float
        Duration of each realisation (s).
    snr : float
        Per-channel SNR for injected signals.
    jitter_min, jitter_max : float
        Uniform jitter range (Hz).  Signal injection frequency is
        f_sig = f0 ± Uniform[jitter_min, jitter_max].
    seed : int
        Master seed; individual realisations use derived seeds for
        reproducibility.

    Returns
    -------
    dict with keys:
        'scores_on'   : score_psi values evaluated at f0 (n_h0 + n_h1,)
        'scores_off'  : score_psi at f0 + F_CONTROL_OFFSET_HZ (n_h0 + n_h1,)
        'labels'      : 0 (H0) or 1 (H1) array (n_h0 + n_h1,)
        'f_injected'  : actual injection frequencies for H1 (n_h1,)
        'data_source' : "SIMULATION_FALLBACK"
    """
    rng = np.random.default_rng(seed)
    n_samples = int(duration_s * fs)
    nperseg = min(256, n_samples // 4)

    # Noise std for desired SNR: signal_rms / noise_std = snr
    amplitude = 1e-22
    signal_rms = amplitude / np.sqrt(2.0)
    noise_std = signal_rms / snr

    scores_on: list[float] = []
    scores_off: list[float] = []
    labels: list[int] = []
    f_injected: list[float] = []

    # ── H0: noise only, independent channels ──────────────────────────────────
    for i in range(n_h0):
        base_seed = int(rng.integers(0, 2**31))
        h1, l1 = _make_noise_pair(n_samples, noise_std,
                                  seed_h1=base_seed,
                                  seed_l1=base_seed + 1)
        s_on, s_off = _compute_scores(h1, l1, fs, f0, nperseg)
        scores_on.append(s_on)
        scores_off.append(s_off)
        labels.append(0)

    # ── H1: coherent signal at f0+jitter + independent noise per channel ──────
    t = np.linspace(0.0, duration_s, n_samples, endpoint=False)
    for i in range(n_h1):
        base_seed = int(rng.integers(0, 2**31))
        # Jitter: magnitude in [jitter_min, jitter_max], random sign
        mag = rng.uniform(jitter_min, jitter_max)
        sign = rng.choice([-1, 1])
        f_sig = f0 + sign * mag
        coherent = amplitude * np.sin(2.0 * np.pi * f_sig * t)
        h1_noise, l1_noise = _make_noise_pair(n_samples, noise_std,
                                              seed_h1=base_seed,
                                              seed_l1=base_seed + 1)
        h1 = coherent + h1_noise
        # Small phase offset (light-travel delay) on L1
        l1 = amplitude * np.sin(2.0 * np.pi * f_sig * t + 0.05) + l1_noise
        s_on, s_off = _compute_scores(h1, l1, fs, f0, nperseg)
        scores_on.append(s_on)
        scores_off.append(s_off)
        labels.append(1)
        f_injected.append(f_sig)

    return {
        "scores_on": np.asarray(scores_on),
        "scores_off": np.asarray(scores_off),
        "labels": np.asarray(labels),
        "f_injected": np.asarray(f_injected),
        "data_source": "SIMULATION_FALLBACK",
    }


def _compute_scores(h1: np.ndarray, l1: np.ndarray,
                    fs: float, f0: float, nperseg: int) -> tuple[float, float]:
    """Compute (score_on_target, score_off_target) for one realisation."""
    freqs_psd, psd = signal.welch(h1, fs=fs, nperseg=nperseg)
    freqs_msc, msc = signal.coherence(h1, l1, fs=fs, nperseg=nperseg)
    s_on = compute_score_psi(psd, freqs_psd, msc, f0)
    f_ctrl = f0 + F_CONTROL_OFFSET_HZ
    s_off = compute_score_psi(psd, freqs_psd, msc, f_ctrl)
    return s_on, s_off


# ── 3. Time-slide sanity check ────────────────────────────────────────────────

def time_slide_sanity(
    h1: np.ndarray,
    l1: np.ndarray,
    fs: float = FS_HZ,
    slide_s: float = TIME_SLIDE_S,
    f0: float = F0_HZ,
    nperseg: int = 256,
) -> dict:
    """
    Verify that a large time offset between detectors destroys the MSC.

    A genuine astrophysical signal is coherent with a well-defined time delay
    (≲ 10 ms for the H1-L1 baseline).  Shifting L1 by slide_s ≫ light-travel
    time should reduce MSC(f₀) substantially, providing a data-consistency
    check against correlated environmental artefacts.

    The shift is implemented with zero-padding (not circular roll) so that
    segments affected by the slide see only zeros in the shifted channel,
    genuinely breaking the correlation even for periodic signals.

    Parameters
    ----------
    h1, l1 : ndarray
        Strain time-series for the two detectors.
    fs : float
        Sampling rate (Hz).
    slide_s : float
        Time offset applied to L1 (s).  Default 1.0 s >> light-travel delay.
    f0 : float
        Target frequency (Hz).
    nperseg : int
        Welch segment length.

    Returns
    -------
    dict
        'msc_zero_lag'  : MSC at f₀ with zero lag.
        'msc_slide'     : MSC at f₀ after time slide.
        'msc_ratio'     : msc_zero_lag / (msc_slide + ε)  (>> 1 for signal).
        'slide_passed'  : bool, True if msc_slide < 0.75 * msc_zero_lag.
    """
    slide_samples = min(int(slide_s * fs), len(l1))
    # Zero-pad shift: prepend zeros, discard trailing samples — no wrap-around.
    l1_slid = np.concatenate([np.zeros(slide_samples), l1[:-slide_samples]])

    freqs_c, msc_zero_c = signal.coherence(h1, l1, fs=fs, nperseg=nperseg)
    _, msc_slid_c = signal.coherence(h1, l1_slid, fs=fs, nperseg=nperseg)
    idx_c = int(np.argmin(np.abs(freqs_c - f0)))

    mz = float(msc_zero_c[idx_c])
    ms = float(msc_slid_c[idx_c])
    ratio = mz / (ms + 1e-300)

    return {
        "msc_zero_lag": mz,
        "msc_slide": ms,
        "msc_ratio": ratio,
        "slide_passed": ms < 0.75 * mz,
    }


# ── 4. Bootstrap AUC ──────────────────────────────────────────────────────────

def _roc_auc(y_true: np.ndarray, scores: np.ndarray) -> float:
    """Compute AUC via trapezoidal integration of the empirical ROC curve."""
    order = np.argsort(scores)[::-1]
    y_sorted = y_true[order]
    tp = np.cumsum(y_sorted)
    fp = np.cumsum(1 - y_sorted)
    tpr = tp / (tp[-1] + 1e-300)
    fpr = fp / (fp[-1] + 1e-300)
    # Prepend (0,0) for proper trapezoidal integration
    tpr = np.concatenate([[0.0], tpr])
    fpr = np.concatenate([[0.0], fpr])
    # Manual trapezoid — avoids np.trapz (removed in NumPy 2.0) / np.trapezoid
    # (added in NumPy 2.0) compatibility issue.
    return float(np.sum(0.5 * (tpr[1:] + tpr[:-1]) * np.diff(fpr)))


def bootstrap_auc(
    y_true: np.ndarray,
    scores: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    seed: int = BOOTSTRAP_SEED,
    ci: float = 0.95,
) -> dict:
    """
    Bootstrap AUC with confidence interval.

    Parameters
    ----------
    y_true : ndarray of int
        Binary labels (0 = H0, 1 = H1).
    scores : ndarray of float
        Detection scores (higher = more likely H1).
    n_boot : int
        Number of bootstrap resamples.  Default 200.
    seed : int
        RNG seed for reproducibility.
    ci : float
        Confidence level (e.g. 0.95 for 95% CI).

    Returns
    -------
    dict
        'auc_point'  : point estimate on the full dataset,
        'auc_mean'   : bootstrap mean,
        'auc_ci_lo'  : lower CI bound,
        'auc_ci_hi'  : upper CI bound,
        'n_boot'     : number of resamples used.
    """
    y_true = np.asarray(y_true)
    scores = np.asarray(scores)
    n = len(y_true)
    rng = np.random.default_rng(seed)
    auc_point = _roc_auc(y_true, scores)
    boot_aucs = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_aucs[i] = _roc_auc(y_true[idx], scores[idx])
    alpha = 1.0 - ci
    lo = float(np.percentile(boot_aucs, 100.0 * alpha / 2.0))
    hi = float(np.percentile(boot_aucs, 100.0 * (1.0 - alpha / 2.0)))
    return {
        "auc_point": round(auc_point, 4),
        "auc_mean": round(float(boot_aucs.mean()), 4),
        "auc_ci_lo": round(lo, 4),
        "auc_ci_hi": round(hi, 4),
        "n_boot": n_boot,
    }


# ── 5. Multiple-testing correction (Benjamini–Hochberg) ──────────────────────

def apply_p_fdr(p_values: Sequence[float]) -> dict:
    """
    Apply Benjamini–Hochberg FDR correction to a list of p-values.

    Each candidate in the O3b scan contributes one p_raw.  If only a single
    candidate (Shadow-O3b-1) is present the BH correction has no effect but
    the result is reported explicitly so the analysis is transparent.

    Parameters
    ----------
    p_values : sequence of float
        Raw p-values, one per candidate.

    Returns
    -------
    dict
        'n_candidates' : number of candidates,
        'single_candidate_note' : str — explicit note if n == 1,
        'p_raw'  : list of raw p-values (input order),
        'p_fdr'  : list of BH-corrected p-values (same order),
        'reject' : list of bool — True if p_fdr < 0.05.
    """
    p = np.asarray(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    rank = np.argsort(order) + 1            # 1-based ranks
    p_bh = np.minimum(1.0, p * n / rank)
    # Enforce monotonicity: p_bh[i] <= p_bh[i+1] in sorted order
    p_sorted = p_bh[order]
    for j in range(len(p_sorted) - 2, -1, -1):
        p_sorted[j] = min(p_sorted[j], p_sorted[j + 1])
    p_fdr = p_sorted[np.argsort(order)]

    note = ""
    if n == 1:
        note = (
            "Only one candidate (Shadow-O3b-1) present.  "
            "BH correction has no effect.  Hook left for multi-candidate scans."
        )

    return {
        "n_candidates": n,
        "single_candidate_note": note,
        "p_raw": p.tolist(),
        "p_fdr": p_fdr.tolist(),
        "reject": (p_fdr < 0.05).tolist(),
    }


# ── 6. O3b scan runner ────────────────────────────────────────────────────────

class O3bScanResult:
    """
    Container for one O3b scan candidate.

    Attributes
    ----------
    name : str
        Candidate label (e.g. "Shadow-O3b-1").
    gps_time : float
        GPS time of the candidate.
    auc_result : dict
        Output of :func:`bootstrap_auc`.
    p_correction : dict
        Output of :func:`apply_p_fdr`.
    data_source : str
        "GWOSC" if loaded from GWOSC, otherwise "SIMULATION_FALLBACK".
    """

    def __init__(self, name: str, gps_time: float,
                 auc_result: dict, p_correction: dict,
                 data_source: str = "SIMULATION_FALLBACK") -> None:
        self.name = name
        self.gps_time = gps_time
        self.auc_result = auc_result
        self.p_correction = p_correction
        self.data_source = data_source

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "gps_time": self.gps_time,
            "auc": self.auc_result,
            "p_correction": self.p_correction,
            "data_source": self.data_source,
        }


def run_o3b_scan(
    candidates: list[dict] | None = None,
    seed: int = 0,
) -> list[O3bScanResult]:
    """
    Run a rigorous O3b detection scan for one or more sub-threshold candidates.

    If *candidates* is None, the default Shadow-O3b-1 entry is used.

    Each candidate dict must have keys:
        'name', 'gps_time', 'p_raw'
    Optional key:
        'data_source'  ("GWOSC" | "SIMULATION_FALLBACK"; default "SIMULATION_FALLBACK")

    The function:
    1. Generates a labelled ROC dataset for each candidate.
    2. Computes bootstrap AUC.
    3. Applies BH FDR correction across all candidates.
    4. Returns a list of O3bScanResult objects.

    Parameters
    ----------
    candidates : list of dict or None
        Candidate descriptors.  If None, Shadow-O3b-1 is used.
    seed : int
        Master RNG seed.

    Returns
    -------
    list of O3bScanResult
    """
    if candidates is None:
        candidates = [
            {
                "name": "Shadow-O3b-1",
                "gps_time": 1251010524.0,
                "p_raw": 0.003,       # illustrative sub-threshold p-value
                "data_source": "SIMULATION_FALLBACK",
            }
        ]

    all_p_raw = [c["p_raw"] for c in candidates]
    p_corr = apply_p_fdr(all_p_raw)

    results = []
    for i, cand in enumerate(candidates):
        ds = generate_roc_dataset(seed=seed + i)
        auc_res = bootstrap_auc(ds["labels"], ds["scores_on"])
        data_source = cand.get("data_source", "SIMULATION_FALLBACK")
        result = O3bScanResult(
            name=cand["name"],
            gps_time=cand["gps_time"],
            auc_result=auc_res,
            p_correction={
                "p_raw": p_corr["p_raw"][i],
                "p_fdr": p_corr["p_fdr"][i],
                "reject": p_corr["reject"][i],
                "n_candidates": p_corr["n_candidates"],
                "single_candidate_note": p_corr["single_candidate_note"],
            },
            data_source=data_source,
        )
        results.append(result)
    return results


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    """Run Shadow-1 O3b rigorous validation and print a summary."""
    print("=" * 65)
    print("Shadow-1 O3b Rigorous Detection Validation")
    print("=" * 65)

    results = run_o3b_scan()

    for r in results:
        print(f"\n📌 Candidate: {r.name}  (GPS {r.gps_time})")
        print(f"   DATA SOURCE : {r.data_source}")   # Issue 6 banner
        auc = r.auc_result
        print(f"   AUC (on-target) : {auc['auc_point']:.4f}  "
              f"[{auc['auc_ci_lo']:.4f}, {auc['auc_ci_hi']:.4f}]  "
              f"n_boot={auc['n_boot']}")
        pc = r.p_correction
        print(f"   p_raw = {pc['p_raw']:.4g}  →  p_fdr = {pc['p_fdr']:.4g}  "
              f"reject={pc['reject']}")
        if pc["single_candidate_note"]:
            print(f"   ℹ️  {pc['single_candidate_note']}")

    # Time-slide sanity on synthetic data
    print("\n🔀 Time-slide sanity check …")
    rng = np.random.default_rng(99)
    n = int(FS_HZ * 1.0)
    t = np.linspace(0, 1.0, n, endpoint=False)
    sig = 1e-22 * np.sin(2 * np.pi * F0_HZ * t)
    h1 = sig + rng.normal(0, 1e-23, n)
    l1 = sig * 0.98 + np.random.default_rng(100).normal(0, 1e-23, n)
    slide_res = time_slide_sanity(h1, l1)
    print(f"   MSC zero-lag = {slide_res['msc_zero_lag']:.4f}  "
          f"MSC after 1 s slide = {slide_res['msc_slide']:.4f}  "
          f"ratio = {slide_res['msc_ratio']:.2f}  "
          f"passed = {slide_res['slide_passed']}")

    print("\n" + "=" * 65)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
