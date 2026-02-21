#!/usr/bin/env python3
"""
GW RAC Time Slides - Significancia Estadística mediante Desplazamientos Temporales
===================================================================================

Implementa el análisis de time-slides para estimar la tasa de falsas alarmas (FAR)
y el p-value del eco detectado por el protocolo RAC sobre GW150914.

Algoritmo:
1. Calcula Ψ_band(t) en los datos *originales* → Ψ₀ (estadístico observado).
2. Ejecuta N slides: desplaza L1 en múltiplos de Δt respecto a H1.
3. Recalcula Ψ_band(t) en cada slide → distribución de máximos de fondo.
4. Estima p-value = #{max_slide ≥ Ψ₀} / N y FAR = p-value / T_analysed.

Uso:
    python gw_rac_timeslides.py
    python gw_rac_timeslides.py --n-slides 500 --slide-step 1.0 --output-dir results/

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import List

import numpy as np
from scipy.signal import butter, filtfilt

# Re-use helpers from gw_rac_residuals
sys.path.insert(0, str(Path(__file__).parent))
try:
    from gw_rac_residuals import (
        load_strain,
        _gr_template,
        compute_psi_band,
        GW150914_GPS,
        GW150914_DURATION,
        GW150914_FS,
        HIGH_FREQ_BAND,
        MERGER_REF_TIME,
    )
    _RESIDUALS_AVAILABLE = True
except ImportError:
    _RESIDUALS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_N_SLIDES = 200
DEFAULT_SLIDE_STEP_S = 1.0  # seconds per slide step
DEFAULT_WINDOW_SEC = 0.1
DEFAULT_OVERLAP = 0.9
DEFAULT_COHERENCE_THRESHOLD = 0.70


# ---------------------------------------------------------------------------
# Internal helpers (used when gw_rac_residuals is not importable)
# ---------------------------------------------------------------------------

def _butter_lowpass(data: np.ndarray, cutoff: float, fs: int,
                    order: int = 4) -> np.ndarray:
    b, a = butter(order, cutoff / (fs / 2), btype="low")
    return filtfilt(b, a, data)


def _fallback_strain(detector: str, N: int, fs: int) -> np.ndarray:
    """Minimal fallback noise simulation when gw_rac_residuals is absent."""
    rng = np.random.default_rng({"H1": 0, "L1": 1}.get(detector, 2))
    white = rng.standard_normal(N) * 1e-23
    return _butter_lowpass(white, 500.0, fs)


# ---------------------------------------------------------------------------
# Time-slide engine
# ---------------------------------------------------------------------------

def compute_background(
    h1_residual: np.ndarray,
    l1_residual: np.ndarray,
    fs: int,
    n_slides: int,
    slide_step_s: float,
    fmin: float,
    fmax: float,
    window_sec: float = DEFAULT_WINDOW_SEC,
    overlap: float = DEFAULT_OVERLAP,
    verbose: bool = True,
) -> List[float]:
    """
    Generate the background distribution of max(Ψ_band) via time slides.

    In each slide *k*, L1 is circularly shifted by ``k * slide_step_s * fs``
    samples, breaking any true astrophysical correlation while preserving the
    noise spectral properties.

    Parameters
    ----------
    h1_residual : np.ndarray
        H1 residual strain array.
    l1_residual : np.ndarray
        L1 residual strain array.
    fs : int
        Sample rate in Hz.
    n_slides : int
        Number of time slides to compute.
    slide_step_s : float
        Shift increment per slide in seconds.
    fmin, fmax : float
        Frequency band for Ψ_band (Hz).
    window_sec : float
        Short-time coherence window (s).
    overlap : float
        Fractional overlap of consecutive windows.
    verbose : bool
        Print progress every 10 %.

    Returns
    -------
    List[float]
        Maximum Ψ_band per slide (length = n_slides).
    """
    slide_samples = int(slide_step_s * fs)
    N = len(l1_residual)
    maxima: List[float] = []

    report_every = max(1, n_slides // 10)

    for k in range(1, n_slides + 1):
        shift = k * slide_samples % N
        l1_slid = np.roll(l1_residual, shift)

        _, psi_b = compute_psi_band(
            h1_residual, l1_slid, fs,
            fmin=fmin, fmax=fmax,
            window_sec=window_sec, overlap=overlap,
        )
        maxima.append(float(np.max(psi_b)))

        if verbose and k % report_every == 0:
            pct = 100 * k / n_slides
            print(f"  Slide {k:>4d}/{n_slides}  ({pct:.0f}%)"
                  f"  max(Ψ_band) = {maxima[-1]:.4f}")

    return maxima


def compute_pvalue_far(
    psi_observed: float,
    background_maxima: List[float],
    analysis_duration_s: float,
) -> dict:
    """
    Compute p-value and FAR from the background distribution.

    Parameters
    ----------
    psi_observed : float
        Observed max(Ψ_band) on the real (on-source) data.
    background_maxima : list of float
        Maximum Ψ_band values from each time slide.
    analysis_duration_s : float
        Duration of the analysed on-source window (seconds), used to
        convert p-value → FAR in events per second.

    Returns
    -------
    dict
        ``{'psi_observed', 'p_value', 'FAR_Hz', 'n_slides',
           'background_mean', 'background_std', 'background_max'}``.
    """
    bg = np.array(background_maxima)
    n = len(bg)
    n_exceeding = int(np.sum(bg >= psi_observed))
    p_value = n_exceeding / n if n > 0 else 1.0
    far_hz = p_value / analysis_duration_s if analysis_duration_s > 0 else float("nan")

    return {
        "psi_observed": psi_observed,
        "p_value": p_value,
        "n_exceeding": n_exceeding,
        "n_slides": n,
        "FAR_Hz": far_hz,
        "FAR_per_year": far_hz * 3.156e7 if not np.isnan(far_hz) else float("nan"),
        "background_mean": float(np.mean(bg)),
        "background_std": float(np.std(bg)),
        "background_max": float(np.max(bg)) if n > 0 else float("nan"),
        "background_min": float(np.min(bg)) if n > 0 else float("nan"),
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_timeslide_analysis(
    n_slides: int = DEFAULT_N_SLIDES,
    slide_step_s: float = DEFAULT_SLIDE_STEP_S,
    output_dir: Path = Path("."),
    coherence_threshold: float = DEFAULT_COHERENCE_THRESHOLD,
    verbose: bool = True,
) -> dict:
    """
    Full time-slide pipeline for GW150914 RAC analysis.

    Parameters
    ----------
    n_slides : int
        Number of time slides to run.
    slide_step_s : float
        Shift increment per slide (seconds).
    output_dir : Path
        Directory to write result JSON.
    coherence_threshold : float
        Minimum Ψ_band to flag statistical significance.
    verbose : bool
        Print progress information.

    Returns
    -------
    dict
        Full results dictionary including p-value, FAR and distribution stats.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fs = GW150914_FS if _RESIDUALS_AVAILABLE else 4096
    duration = GW150914_DURATION if _RESIDUALS_AVAILABLE else 32.0
    fmin, fmax = HIGH_FREQ_BAND if _RESIDUALS_AVAILABLE else (300.0, 1000.0)
    gps_start = (GW150914_GPS - MERGER_REF_TIME
                 if _RESIDUALS_AVAILABLE else 1126259462.4 - 0.43)

    if verbose:
        print("=" * 60)
        print("  RAC Time Slides – GW150914")
        print(f"  N slides = {n_slides},  step = {slide_step_s} s")
        print("=" * 60)

    # 1. Load strain
    if verbose:
        print("\n[1/4] Cargando strain H1 y L1 ...")
    if _RESIDUALS_AVAILABLE:
        h1_strain = load_strain("H1", gps_start, duration, fs)
        l1_strain = load_strain("L1", gps_start, duration, fs)
    else:
        N = int(duration * fs)
        h1_strain = _fallback_strain("H1", N, fs)
        l1_strain = _fallback_strain("L1", N, fs)

    N = min(len(h1_strain), len(l1_strain))
    t = np.linspace(0, duration, N, endpoint=False)
    h1_strain = h1_strain[:N]
    l1_strain = l1_strain[:N]

    # 2. Build residuals
    if verbose:
        print("[2/4] Calculando residuales (strain − template GR) ...")
    if _RESIDUALS_AVAILABLE:
        template = _gr_template(t, fs)
        h1_residual = h1_strain - template
        l1_residual = l1_strain - template
    else:
        h1_residual = h1_strain
        l1_residual = l1_strain

    # 3. On-source Ψ_band
    if verbose:
        print("[3/4] Ψ_band en datos originales (on-source) ...")
    _, psi_on = compute_psi_band(
        h1_residual, l1_residual, fs,
        fmin=fmin, fmax=fmax,
        window_sec=DEFAULT_WINDOW_SEC, overlap=DEFAULT_OVERLAP,
    )
    psi_observed = float(np.max(psi_on))
    if verbose:
        print(f"  max(Ψ_band) on-source = {psi_observed:.4f}")

    # 4. Background via time slides
    if verbose:
        print(f"\n[4/4] Ejecutando {n_slides} time slides ...")
    background_maxima = compute_background(
        h1_residual, l1_residual, fs,
        n_slides=n_slides,
        slide_step_s=slide_step_s,
        fmin=fmin, fmax=fmax,
        verbose=verbose,
    )

    # 5. Statistics
    stats = compute_pvalue_far(psi_observed, background_maxima,
                               analysis_duration_s=duration)

    # Build results
    results = {
        "event": "GW150914",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "n_slides": n_slides,
            "slide_step_s": slide_step_s,
            "fs": fs,
            "duration_s": duration,
            "high_freq_band_hz": [fmin, fmax],
            "coherence_threshold": coherence_threshold,
        },
        "statistics": stats,
        "background_distribution": {
            "maxima_sample": background_maxima[:20],   # first 20 for compactness
            "percentile_90": float(np.percentile(background_maxima, 90)),
            "percentile_95": float(np.percentile(background_maxima, 95)),
            "percentile_99": float(np.percentile(background_maxima, 99)),
        },
        "significant": stats["p_value"] < 0.05,
        "gwpy_available": _RESIDUALS_AVAILABLE,
    }

    out_file = output_dir / "gw_rac_timeslides_results.json"
    out_file.write_text(json.dumps(results, indent=2))

    if verbose:
        print("\n" + "=" * 60)
        print("  RESULTADOS")
        print("=" * 60)
        print(f"  Ψ_band on-source (máx)  : {psi_observed:.4f}")
        print(f"  p-value                 : {stats['p_value']:.4f}")
        print(f"  FAR                     : {stats['FAR_Hz']:.2e} Hz")
        print(f"  FAR (por año)           : {stats['FAR_per_year']:.2f}")
        print(f"  Estadísticamente signif.: {results['significant']}")
        print(f"  Resultados en           : {out_file}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="RAC Time Slides: p-value y FAR para GW150914"
    )
    parser.add_argument(
        "--n-slides", type=int, default=DEFAULT_N_SLIDES,
        help=f"Número de time slides (default: {DEFAULT_N_SLIDES})"
    )
    parser.add_argument(
        "--slide-step", type=float, default=DEFAULT_SLIDE_STEP_S, metavar="S",
        help=f"Paso de desplazamiento en segundos (default: {DEFAULT_SLIDE_STEP_S})"
    )
    parser.add_argument(
        "--output-dir", default=".", metavar="DIR",
        help="Directorio para resultados (default: .)"
    )
    parser.add_argument(
        "--coherence-threshold", type=float, default=DEFAULT_COHERENCE_THRESHOLD,
        help=f"Umbral mínimo de coherencia (default: {DEFAULT_COHERENCE_THRESHOLD})"
    )
    parser.add_argument("--quiet", action="store_true",
                        help="Suprimir salida detallada")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    run_timeslide_analysis(
        n_slides=args.n_slides,
        slide_step_s=args.slide_step,
        output_dir=Path(args.output_dir),
        coherence_threshold=args.coherence_threshold,
        verbose=not args.quiet,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
