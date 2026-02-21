#!/usr/bin/env python3
"""
GW RAC Residuals - Escaneo de Residuales de Alta Coherencia (RAC)
=================================================================

Protocolo de Resta de Máscara para GW150914:

1. Carga el strain original de H1 y L1
2. Sustrae el modelo de Relatividad General (Best-Fit Template)
3. Produce los residuales post-sustracción
4. Calcula Ψ(t) (coherencia cruzada H1-L1) y Ψ_band(t) (coherencia en banda)
5. Detecta ecos post-merger en la zona de sombra

Referencia: Abbott et al. 2016 (GW150914), PRL 116, 061102

Uso:
    python gw_rac_residuals.py
    python gw_rac_residuals.py --output-dir results/ --echo-window 0.02

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt

# Try real GWOSC/GWPy data
try:
    from gwpy.timeseries import TimeSeries
    from gwosc import datasets
    GWPY_AVAILABLE = True
except ImportError:
    GWPY_AVAILABLE = False

# ---------------------------------------------------------------------------
# Physical constants for GW150914
# ---------------------------------------------------------------------------

GW150914_GPS = 1126259462.4       # GPS merger time
GW150914_DURATION = 32.0          # s of data around the event
GW150914_FS = 4096                 # Hz sample rate
GW150914_MASS_TOTAL = 66.2        # M_sun (m1+m2)
RINGDOWN_FREQ = 251.0              # Hz  – dominant ringdown frequency
HIGH_FREQ_BAND = (300.0, 1000.0)  # Hz  – "post-merger shadow" band
ECHO_DELAY = 0.020                 # s   – expected echo delay
MERGER_REF_TIME = 0.43             # s   – merger within the 32 s window (approx)

F0_QCAL = 141.7001                 # Hz  – QCAL fundamental


# ---------------------------------------------------------------------------
# Simulated GR template  (chirp + exponential ringdown)
# ---------------------------------------------------------------------------

def _gr_template(t: np.ndarray, fs: float = GW150914_FS) -> np.ndarray:
    """
    Minimal analytic GR template for GW150914.

    Generates a chirp-like inspiral followed by an exponential ringdown at
    RINGDOWN_FREQ.  The amplitude is calibrated to LIGO strain units (~ 10⁻²¹).

    Parameters
    ----------
    t : np.ndarray
        Time array relative to the start of the segment (seconds).
    fs : float
        Sample rate (Hz) – used only to ensure correct timing resolution.

    Returns
    -------
    np.ndarray
        Strain template h(t).
    """
    merger_t = MERGER_REF_TIME
    h = np.zeros_like(t, dtype=float)

    # -- Inspiral phase (t < merger_t) --
    mask_insp = t < merger_t
    dt_insp = merger_t - t[mask_insp]
    # Frequency sweeps from ~35 Hz up to merger_freq as dt → 0
    f_insp = 35.0 + 115.0 * np.clip(1.0 - dt_insp / merger_t, 0, 1) ** 3
    phase_insp = 2 * np.pi * np.cumsum(f_insp) / fs
    amp_insp = 1e-21 * np.clip(1.0 - dt_insp / merger_t, 0.01, 1) ** (2 / 3)
    h[mask_insp] = amp_insp * np.sin(phase_insp)

    # -- Ringdown phase (t >= merger_t) --
    mask_ring = t >= merger_t
    dt_ring = t[mask_ring] - merger_t
    tau = 1.0 / (np.pi * RINGDOWN_FREQ / 10)   # quality factor Q ~ 10
    amp_ring = 1e-21 * np.exp(-dt_ring / tau)
    phase_ring = 2 * np.pi * RINGDOWN_FREQ * dt_ring
    h[mask_ring] = amp_ring * np.cos(phase_ring)

    return h


# ---------------------------------------------------------------------------
# Strain loader  (real GWOSC data with fallback to simulation)
# ---------------------------------------------------------------------------

def load_strain(detector: str, gps_start: float, duration: float,
                fs: int = GW150914_FS) -> np.ndarray:
    """
    Load strain data for *detector* around GW150914.

    Tries to fetch real open data via GWPy; falls back to a realistic
    Gaussian-noise simulation when GWOSC data is unavailable.

    Parameters
    ----------
    detector : str
        Detector label, e.g. ``'H1'`` or ``'L1'``.
    gps_start : float
        GPS start time of the segment.
    duration : float
        Length of segment in seconds.
    fs : int
        Sample rate in Hz.

    Returns
    -------
    np.ndarray
        Strain array with ``int(duration * fs)`` samples.
    """
    if GWPY_AVAILABLE:
        try:
            ts = TimeSeries.fetch_open_data(
                detector, gps_start, gps_start + duration,
                sample_rate=fs, timeout=30
            )
            return ts.value.astype(float)
        except Exception as exc:
            print(f"⚠️  GWOSC fetch failed ({exc}); using simulation.")

    # Fallback: realistic noise + embedded chirp
    rng = np.random.default_rng({"H1": 0, "L1": 1}.get(detector, 2))
    N = int(duration * fs)
    t = np.linspace(0, duration, N, endpoint=False)

    # Colored noise (very rough LIGO ASD approximation)
    white = rng.standard_normal(N) * 1e-23
    # Low-pass shape to mimic LIGO noise
    b, a = butter(4, 500.0 / (fs / 2), btype="low")
    noise = filtfilt(b, a, white)

    # Embed the GR template signal
    h_template = _gr_template(t, fs)
    strain = noise + h_template

    return strain


# ---------------------------------------------------------------------------
# Coherence metric  Ψ(t)
# ---------------------------------------------------------------------------

def compute_psi(
    h1_strain: np.ndarray,
    l1_strain: np.ndarray,
    fs: int = GW150914_FS,
    window_sec: float = 0.1,
    overlap: float = 0.9,
) -> tuple:
    """
    Compute the cross-coherence Ψ(t) between H1 and L1 residuals.

    Uses short-time cross-spectral density normalised by the auto-PSDs
    (standard magnitude-squared coherence), averaged across all positive
    frequencies.

    Parameters
    ----------
    h1_strain : np.ndarray
        H1 strain (or residual) array.
    l1_strain : np.ndarray
        L1 strain (or residual) array.
    fs : int
        Sample rate in Hz.
    window_sec : float
        Short-time window length in seconds.
    overlap : float
        Fractional overlap between windows (0 < overlap < 1).

    Returns
    -------
    t_psi : np.ndarray
        Time stamps of the Ψ(t) samples (seconds from segment start).
    psi : np.ndarray
        Ψ(t) values in [0, 1].
    """
    nperseg = int(window_sec * fs)
    noverlap = int(overlap * nperseg)
    step = nperseg - noverlap

    N = min(len(h1_strain), len(l1_strain))
    n_steps = max(1, (N - nperseg) // step + 1)

    t_psi = np.empty(n_steps)
    psi = np.empty(n_steps)

    for k in range(n_steps):
        i0 = k * step
        i1 = i0 + nperseg
        seg_h1 = h1_strain[i0:i1] * np.hanning(nperseg)
        seg_l1 = l1_strain[i0:i1] * np.hanning(nperseg)

        fft_h1 = np.fft.rfft(seg_h1)
        fft_l1 = np.fft.rfft(seg_l1)

        Sh1 = np.abs(fft_h1) ** 2
        Sl1 = np.abs(fft_l1) ** 2
        Scross = np.abs(fft_h1 * fft_l1.conj())

        denom = np.sqrt(Sh1 * Sl1)
        max_d = np.max(denom)
        if max_d > 0:
            mask = denom > 1e-10 * max_d
            coh = np.where(mask, Scross / np.where(mask, denom, 1.0), 0.0)
        else:
            coh = np.zeros_like(Scross)
        psi[k] = float(np.mean(coh))
        t_psi[k] = (i0 + nperseg / 2) / fs

    return t_psi, psi


def compute_psi_band(
    h1_strain: np.ndarray,
    l1_strain: np.ndarray,
    fs: int = GW150914_FS,
    fmin: float = HIGH_FREQ_BAND[0],
    fmax: float = HIGH_FREQ_BAND[1],
    window_sec: float = 0.1,
    overlap: float = 0.9,
) -> tuple:
    """
    Band-limited coherence Ψ_band(t) restricted to [fmin, fmax] Hz.

    Parameters
    ----------
    h1_strain, l1_strain : np.ndarray
        Input strain or residual arrays.
    fs : int
        Sample rate in Hz.
    fmin, fmax : float
        Frequency band boundaries in Hz.
    window_sec, overlap : float
        Window parameters (see :func:`compute_psi`).

    Returns
    -------
    t_psi : np.ndarray
        Time stamps (seconds from segment start).
    psi_band : np.ndarray
        Band-limited Ψ_band(t) values in [0, 1].
    """
    nperseg = int(window_sec * fs)
    noverlap = int(overlap * nperseg)
    step = nperseg - noverlap

    freqs = np.fft.rfftfreq(nperseg, d=1.0 / fs)
    band_mask = (freqs >= fmin) & (freqs <= fmax)

    N = min(len(h1_strain), len(l1_strain))
    n_steps = max(1, (N - nperseg) // step + 1)

    t_psi = np.empty(n_steps)
    psi_band = np.empty(n_steps)

    for k in range(n_steps):
        i0 = k * step
        i1 = i0 + nperseg
        seg_h1 = h1_strain[i0:i1] * np.hanning(nperseg)
        seg_l1 = l1_strain[i0:i1] * np.hanning(nperseg)

        fft_h1 = np.fft.rfft(seg_h1)
        fft_l1 = np.fft.rfft(seg_l1)

        Sh1_b = np.abs(fft_h1[band_mask]) ** 2
        Sl1_b = np.abs(fft_l1[band_mask]) ** 2
        Scross_b = np.abs(fft_h1[band_mask] * fft_l1[band_mask].conj())

        denom_b = np.sqrt(Sh1_b * Sl1_b)
        if band_mask.any():
            max_d = np.max(denom_b)
            if max_d > 0:
                mask = denom_b > 1e-10 * max_d
                coh_b = np.where(mask, Scross_b / np.where(mask, denom_b, 1.0),
                                 0.0)
            else:
                coh_b = np.zeros_like(Scross_b)
            psi_band[k] = float(np.mean(coh_b))
        else:
            psi_band[k] = 0.0
        t_psi[k] = (i0 + nperseg / 2) / fs

    return t_psi, psi_band


# ---------------------------------------------------------------------------
# Echo detection
# ---------------------------------------------------------------------------

def detect_echo(
    t_psi: np.ndarray,
    psi: np.ndarray,
    merger_time: float = MERGER_REF_TIME,
    echo_window: float = ECHO_DELAY,
    coherence_threshold: float = 0.70,
) -> dict:
    """
    Detect a post-merger coherence echo in Ψ(t).

    Looks for a local maximum of Ψ inside the window
    [merger_time + echo_window/2, merger_time + 3*echo_window] and checks
    whether it exceeds *coherence_threshold*.

    Parameters
    ----------
    t_psi : np.ndarray
        Time stamps of Ψ(t).
    psi : np.ndarray
        Ψ(t) values.
    merger_time : float
        Reference merger time (s from segment start).
    echo_window : float
        Centre of the expected echo delay (s after merger).
    coherence_threshold : float
        Minimum coherence value to flag an echo.

    Returns
    -------
    dict
        ``{'detected': bool, 'echo_time': float, 'echo_psi': float,
           'delay': float}``.
    """
    t_min = merger_time + echo_window / 2
    t_max = merger_time + 3.0 * echo_window

    mask = (t_psi >= t_min) & (t_psi <= t_max)
    if not mask.any():
        return {"detected": False, "echo_time": float("nan"),
                "echo_psi": float("nan"), "delay": float("nan")}

    idx_max = np.argmax(psi[mask])
    echo_t = float(t_psi[mask][idx_max])
    echo_val = float(psi[mask][idx_max])

    detected = echo_val >= coherence_threshold
    return {
        "detected": detected,
        "echo_time": echo_t,
        "echo_psi": echo_val,
        "delay": echo_t - merger_time,
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_rac_analysis(
    output_dir: Path = Path("."),
    echo_window: float = ECHO_DELAY,
    coherence_threshold: float = 0.70,
    verbose: bool = True,
) -> dict:
    """
    Full RAC pipeline for GW150914.

    Steps:
    1. Load H1 and L1 strain.
    2. Compute GR template and subtract → residuals.
    3. Compute Ψ(t) (broadband) and Ψ_band(t) (>300 Hz) on residuals.
    4. Detect post-merger echo.
    5. Save JSON results.

    Parameters
    ----------
    output_dir : Path
        Directory for output files.
    echo_window : float
        Expected echo delay (s after merger peak).
    coherence_threshold : float
        Minimum Ψ to flag echo detection.
    verbose : bool
        Print progress information.

    Returns
    -------
    dict
        Analysis results dictionary.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fs = GW150914_FS
    gps_start = GW150914_GPS - MERGER_REF_TIME
    duration = GW150914_DURATION

    if verbose:
        print("=" * 60)
        print("  RAC: Escaneo de Residuales de Alta Coherencia")
        print("  Evento: GW150914")
        print("=" * 60)

    # 1. Load strain
    if verbose:
        print("\n[1/4] Cargando strain H1 y L1 ...")
    h1_strain = load_strain("H1", gps_start, duration, fs)
    l1_strain = load_strain("L1", gps_start, duration, fs)
    N = min(len(h1_strain), len(l1_strain))
    t = np.linspace(0, duration, N, endpoint=False)
    h1_strain = h1_strain[:N]
    l1_strain = l1_strain[:N]

    # 2. Compute template and residuals
    if verbose:
        print("[2/4] Calculando template GR y residuales ...")
    template = _gr_template(t, fs)
    h1_residual = h1_strain - template
    l1_residual = l1_strain - template

    # 3. Compute Ψ(t) and Ψ_band(t)
    if verbose:
        print("[3/4] Calculando Ψ(t) y Ψ_band(t) sobre residuales ...")
    t_psi, psi = compute_psi(h1_residual, l1_residual, fs)
    t_psi_band, psi_band = compute_psi_band(
        h1_residual, l1_residual, fs,
        fmin=HIGH_FREQ_BAND[0], fmax=HIGH_FREQ_BAND[1]
    )

    # 4. Echo detection (broadband Ψ and band-limited Ψ_band)
    if verbose:
        print("[4/4] Buscando eco post-merger ...")
    echo_broad = detect_echo(t_psi, psi, MERGER_REF_TIME, echo_window,
                             coherence_threshold)
    echo_band = detect_echo(t_psi_band, psi_band, MERGER_REF_TIME, echo_window,
                            coherence_threshold)

    peak_psi = float(np.max(psi))
    peak_psi_band = float(np.max(psi_band))

    results = {
        "event": "GW150914",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "fs": fs,
            "duration": duration,
            "high_freq_band_hz": list(HIGH_FREQ_BAND),
            "echo_window_s": echo_window,
            "coherence_threshold": coherence_threshold,
        },
        "residuals": {
            "N_samples": N,
            "h1_rms": float(np.sqrt(np.mean(h1_residual ** 2))),
            "l1_rms": float(np.sqrt(np.mean(l1_residual ** 2))),
        },
        "psi_broadband": {
            "peak": peak_psi,
            "echo": echo_broad,
        },
        "psi_band": {
            "band_hz": list(HIGH_FREQ_BAND),
            "peak": peak_psi_band,
            "echo": echo_band,
        },
        "gwpy_available": GWPY_AVAILABLE,
    }

    # Save results
    out_file = output_dir / "gw_rac_residuals_results.json"
    out_file.write_text(json.dumps(results, indent=2))

    if verbose:
        print("\n" + "=" * 60)
        print("  RESULTADOS")
        print("=" * 60)
        print(f"  Ψ broadband pico  : {peak_psi:.4f}")
        print(f"  Ψ_band pico       : {peak_psi_band:.4f}")
        print(f"  Eco broadband     : {echo_broad}")
        print(f"  Eco banda alta    : {echo_band}")
        print(f"  Resultados en     : {out_file}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="RAC: Escaneo de Residuales de Alta Coherencia para GW150914"
    )
    parser.add_argument(
        "--output-dir", default=".", metavar="DIR",
        help="Directorio para resultados (default: .)"
    )
    parser.add_argument(
        "--echo-window", type=float, default=ECHO_DELAY, metavar="S",
        help=f"Ventana de eco post-merger en segundos (default: {ECHO_DELAY})"
    )
    parser.add_argument(
        "--coherence-threshold", type=float, default=0.70, metavar="C",
        help="Umbral mínimo de coherencia para detectar eco (default: 0.70)"
    )
    parser.add_argument("--quiet", action="store_true",
                        help="Suprimir salida detallada")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    results = run_rac_analysis(
        output_dir=Path(args.output_dir),
        echo_window=args.echo_window,
        coherence_threshold=args.coherence_threshold,
        verbose=not args.quiet,
    )
    # Return 0 on success; flag non-zero only on unexpected failure
    return 0


if __name__ == "__main__":
    sys.exit(main())
