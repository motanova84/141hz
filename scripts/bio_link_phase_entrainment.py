#!/usr/bin/env python3
"""
Bio-Link Phase Entrainment – Sincronía Simbiótica GW-Bio
=========================================================

Genera los cuatro estímulos del ensayo de Sincronía Simbiótica:

  A – Patrón GW-eco transpuesto (firma de fase del eco post-merger de
      GW150914 escalada a la banda Gamma cerebral, 35–45 Hz)
  B – Control espectral: mismo espectro de potencia que A, fases aleatorias
      (phase-scrambled)
  C – Silencio (cero)
  D – Tono Gamma puro 40 Hz (control positivo)

Analiza una señal EEG (sintética o cargada desde archivo) y calcula:

  • G(t)  – Genesis Score: coherencia espectral instantánea entre el
            estímulo y la respuesta EEG en la banda Gamma alta (35–45 Hz)
  • PLV   – Phase Locking Value: coherencia de fase entre estímulo y EEG

Protocolo de seguridad básico:
  - Volumen de estímulo limitado a amplitud normalizada ≤ 0.5
  - Sin parpadeo visual rápido (solo estímulo de audio/eléctrico)
  - Advertencia para historial de epilepsia fotosensible (no aplica en
    modo audio, pero se registra en metadatos)

Uso:
    python bio_link_phase_entrainment.py
    python bio_link_phase_entrainment.py --stimulus A --eeg-file path/to/eeg.npy
    python bio_link_phase_entrainment.py --all-stimuli --output-dir results/

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import argparse
import json
import sys
import warnings
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Tuple

import numpy as np
from scipy.signal import butter, filtfilt, hilbert

# ---------------------------------------------------------------------------
# Physical / physiological constants
# ---------------------------------------------------------------------------

# GW150914 post-merger echo parameters
ECHO_FREQ_ASTRO_HZ = 315.0       # Hz – nominal echo frequency in the >300 Hz band
ECHO_DELAY_S = 0.020             # s  – post-merger echo delay

# Bio-link frequency scaling
GAMMA_CENTER_HZ = 40.0           # Hz – target gamma frequency
GAMMA_BAND_HZ = (35.0, 45.0)     # Hz – gamma band
CIRCADIAN_REF_HZ = 1.0 / 86400  # Hz – circadian rhythm reference

# Scale factor: bring ECHO_FREQ_ASTRO_HZ → GAMMA_CENTER_HZ
FREQ_SCALE_FACTOR = GAMMA_CENTER_HZ / ECHO_FREQ_ASTRO_HZ

# EEG simulation parameters
EEG_FS = 512                     # Hz – sample rate
EEG_DURATION_S = 10.0            # s  – stimulus duration
EEG_NOISE_AMP = 2e-6             # V  – background EEG noise amplitude

# Safety limits
MAX_STIMULUS_AMP = 0.5           # normalised amplitude ceiling

# Genesis Score / PLV analysis window
ANALYSIS_WINDOW_S = 1.0          # s  – sliding window for G(t) and PLV


# ---------------------------------------------------------------------------
# Stimulus generators
# ---------------------------------------------------------------------------

def stimulus_A(
    fs: int = EEG_FS,
    duration: float = EEG_DURATION_S,
    max_amp: float = MAX_STIMULUS_AMP,
) -> np.ndarray:
    """
    Stimulus A – GW-echo phase transposed to Gamma band.

    Takes the phase structure of the GW150914 post-merger echo (exponentially
    damped oscillation at ECHO_FREQ_ASTRO_HZ with ECHO_DELAY_S onset) and
    transposes it to the Gamma band by applying FREQ_SCALE_FACTOR, preserving
    the exact phase relationship.

    Parameters
    ----------
    fs : int
        Sample rate in Hz.
    duration : float
        Stimulus duration in seconds.
    max_amp : float
        Peak amplitude (safety ceiling, normalised units).

    Returns
    -------
    np.ndarray
        Stimulus waveform of length ``int(duration * fs)``.
    """
    N = int(duration * fs)
    t = np.arange(N) / fs

    # Echo onset after ECHO_DELAY_S
    mask_echo = t >= ECHO_DELAY_S
    s = np.zeros(N)

    dt_echo = t[mask_echo] - ECHO_DELAY_S
    # Quality factor Q ~ 8  → τ = Q / (π * f)
    q = 8.0
    tau = q / (np.pi * GAMMA_CENTER_HZ)
    envelope = np.exp(-dt_echo / tau)

    # Phase: use the exact phase offset from the astro domain
    astro_phase_at_echo = 2 * np.pi * ECHO_FREQ_ASTRO_HZ * ECHO_DELAY_S
    bio_phase = 2 * np.pi * GAMMA_CENTER_HZ * dt_echo + astro_phase_at_echo

    s[mask_echo] = envelope * np.cos(bio_phase)

    # Safety normalisation
    peak = np.max(np.abs(s))
    if peak > 0:
        s *= max_amp / peak

    return s


def stimulus_B(
    stim_a: Optional[np.ndarray] = None,
    fs: int = EEG_FS,
    duration: float = EEG_DURATION_S,
    max_amp: float = MAX_STIMULUS_AMP,
    seed: int = 42,
) -> np.ndarray:
    """
    Stimulus B – Phase-scrambled control.

    Same power spectrum as stimulus A but with randomised phases.  This
    controls for any spectral effect, isolating the role of the original
    phase structure.

    Parameters
    ----------
    stim_a : np.ndarray or None
        Precomputed stimulus A.  If None, it is generated internally.
    fs, duration, max_amp : see :func:`stimulus_A`.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Phase-scrambled waveform.
    """
    if stim_a is None:
        stim_a = stimulus_A(fs=fs, duration=duration, max_amp=max_amp)

    rng = np.random.default_rng(seed)

    fft_a = np.fft.rfft(stim_a)
    magnitudes = np.abs(fft_a)
    random_phases = rng.uniform(0, 2 * np.pi, size=len(fft_a))
    fft_scrambled = magnitudes * np.exp(1j * random_phases)

    s = np.fft.irfft(fft_scrambled, n=len(stim_a))

    # Safety normalisation
    peak = np.max(np.abs(s))
    if peak > 0:
        s *= max_amp / peak

    return s


def stimulus_C(
    fs: int = EEG_FS,
    duration: float = EEG_DURATION_S,
) -> np.ndarray:
    """
    Stimulus C – Silence (zero signal).

    Parameters
    ----------
    fs, duration : see :func:`stimulus_A`.

    Returns
    -------
    np.ndarray
        Array of zeros.
    """
    return np.zeros(int(duration * fs))


def stimulus_D(
    fs: int = EEG_FS,
    duration: float = EEG_DURATION_S,
    freq: float = GAMMA_CENTER_HZ,
    max_amp: float = MAX_STIMULUS_AMP,
) -> np.ndarray:
    """
    Stimulus D – Pure 40 Hz gamma tone (positive control).

    Parameters
    ----------
    fs, duration, max_amp : see :func:`stimulus_A`.
    freq : float
        Gamma tone frequency in Hz (default: 40 Hz).

    Returns
    -------
    np.ndarray
        Sinusoidal waveform at *freq* Hz.
    """
    N = int(duration * fs)
    t = np.arange(N) / fs
    s = max_amp * np.sin(2 * np.pi * freq * t)
    return s


# ---------------------------------------------------------------------------
# EEG loader / simulator
# ---------------------------------------------------------------------------

def load_eeg(
    file_path: Optional[str],
    fs: int = EEG_FS,
    duration: float = EEG_DURATION_S,
    stimulus: Optional[np.ndarray] = None,
    seed: int = 7,
) -> Tuple[np.ndarray, float]:
    """
    Load or synthesise an EEG signal for phase-entrainment analysis.

    If *file_path* is given and exists, tries to load it (.npy or .npz).
    Otherwise generates a synthetic EEG with realistic background noise and
    an embedded gamma response entrained to *stimulus* (if provided).

    Parameters
    ----------
    file_path : str or None
        Path to EEG file.
    fs : int
        Sample rate in Hz.
    duration : float
        Target duration in seconds.
    stimulus : np.ndarray or None
        When generating synthetic EEG, adds a weak phase-locked gamma
        component entrained to this stimulus.
    seed : int
        Random seed for the synthetic generator.

    Returns
    -------
    eeg : np.ndarray
        EEG signal array.
    actual_fs : float
        Actual sample rate (equals *fs* for synthetic data).
    """
    if file_path and Path(file_path).exists():
        data = np.load(file_path, allow_pickle=True)
        if hasattr(data, "files"):
            if "eeg" in data.files:
                eeg = data["eeg"].astype(float)
            elif "signal" in data.files:
                eeg = data["signal"].astype(float)
            else:
                eeg = data[list(data.files)[0]].astype(float)
            loaded_fs = float(data.get("fs", fs))
        else:
            eeg = np.asarray(data, dtype=float)
            loaded_fs = float(fs)

        if eeg.ndim > 1:
            eeg = eeg[0] if eeg.shape[0] < eeg.shape[1] else eeg[:, 0]
        return eeg, loaded_fs

    # Synthetic EEG
    N = int(duration * fs)
    t = np.arange(N) / fs
    rng = np.random.default_rng(seed)

    # Background noise (pink-ish)
    white = rng.standard_normal(N) * EEG_NOISE_AMP
    b, a = butter(2, 80.0 / (fs / 2), btype="low")
    eeg = filtfilt(b, a, white)

    # Gamma background (spontaneous)
    gamma_bg = 0.2 * EEG_NOISE_AMP * np.sin(2 * np.pi * GAMMA_CENTER_HZ * t
                                             + rng.uniform(0, 2 * np.pi))
    eeg += gamma_bg

    # Entrained gamma component (weak coupling to stimulus)
    if stimulus is not None:
        N_s = min(N, len(stimulus))
        coupling = 0.3
        b_g, a_g = butter(4, [GAMMA_BAND_HZ[0] / (fs / 2),
                               GAMMA_BAND_HZ[1] / (fs / 2)], btype="band")
        stim_gamma = filtfilt(b_g, a_g, np.pad(stimulus[:N_s], (0, max(0, N - N_s))))
        peak = np.max(np.abs(stim_gamma))
        if peak > 0:
            eeg += coupling * EEG_NOISE_AMP * stim_gamma / peak

    return eeg, float(fs)


# ---------------------------------------------------------------------------
# Analysis metrics: G(t) and PLV
# ---------------------------------------------------------------------------

def _bandpass(sig: np.ndarray, fmin: float, fmax: float, fs: float) -> np.ndarray:
    b, a = butter(4, [fmin / (fs / 2), fmax / (fs / 2)], btype="band")
    return filtfilt(b, a, sig)


def compute_genesis_score(
    stimulus: np.ndarray,
    eeg: np.ndarray,
    fs: float = EEG_FS,
    fmin: float = GAMMA_BAND_HZ[0],
    fmax: float = GAMMA_BAND_HZ[1],
    window_s: float = ANALYSIS_WINDOW_S,
    overlap: float = 0.9,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute G(t) – Genesis Score (sliding cross-coherence in Gamma band).

    G(t) measures the instantaneous spectral coherence between the stimulus
    envelope and the EEG power in the Gamma band, in short overlapping windows.

    Parameters
    ----------
    stimulus : np.ndarray
        Stimulus waveform.
    eeg : np.ndarray
        EEG signal.
    fs : float
        Sample rate in Hz.
    fmin, fmax : float
        Gamma band boundaries (Hz).
    window_s : float
        Window length in seconds.
    overlap : float
        Fractional overlap between windows.

    Returns
    -------
    t_g : np.ndarray
        Time stamps (seconds).
    G : np.ndarray
        G(t) values in [0, 1].
    """
    nperseg = int(window_s * fs)
    step = max(1, int(nperseg * (1 - overlap)))

    N = min(len(stimulus), len(eeg))
    n_steps = max(1, (N - nperseg) // step + 1)

    t_g = np.empty(n_steps)
    G = np.empty(n_steps)

    # Band-pass EEG and stimulus to gamma band
    eeg_bp = _bandpass(eeg[:N], fmin, fmax, fs)
    stim_bp = _bandpass(stimulus[:N], fmin, fmax, fs)

    for k in range(n_steps):
        i0 = k * step
        i1 = i0 + nperseg
        w = np.hanning(nperseg)

        se = eeg_bp[i0:i1] * w
        ss = stim_bp[i0:i1] * w

        fft_e = np.fft.rfft(se)
        fft_s = np.fft.rfft(ss)

        cross = np.abs(fft_e * fft_s.conj())
        denom = np.sqrt(np.sum(np.abs(fft_e) ** 2) * np.sum(np.abs(fft_s) ** 2)
                        + 1e-60)
        G[k] = float(np.sum(cross) / denom)
        t_g[k] = (i0 + nperseg / 2) / fs

    return t_g, G


def compute_plv(
    stimulus: np.ndarray,
    eeg: np.ndarray,
    fs: float = EEG_FS,
    fmin: float = GAMMA_BAND_HZ[0],
    fmax: float = GAMMA_BAND_HZ[1],
) -> float:
    """
    Compute PLV – Phase Locking Value between stimulus and EEG.

    PLV = |mean(exp(i·(φ_stim − φ_eeg)))| where phases are extracted via
    the Hilbert transform of the band-passed signals.

    Parameters
    ----------
    stimulus : np.ndarray
        Stimulus waveform.
    eeg : np.ndarray
        EEG signal.
    fs : float
        Sample rate in Hz.
    fmin, fmax : float
        Frequency band for phase extraction (Hz).

    Returns
    -------
    float
        PLV in [0, 1].
    """
    N = min(len(stimulus), len(eeg))
    stim_bp = _bandpass(stimulus[:N], fmin, fmax, fs)
    eeg_bp = _bandpass(eeg[:N], fmin, fmax, fs)

    phi_stim = np.angle(hilbert(stim_bp))
    phi_eeg = np.angle(hilbert(eeg_bp))

    plv = float(np.abs(np.mean(np.exp(1j * (phi_stim - phi_eeg)))))
    return plv


# ---------------------------------------------------------------------------
# Compare A vs B  (key test: does phase structure matter?)
# ---------------------------------------------------------------------------

def compare_A_vs_B(
    plv_A: float,
    plv_B: float,
    G_mean_A: float,
    G_mean_B: float,
) -> dict:
    """
    Summarise A vs B comparison.

    If A > B consistently, this is evidence that the phase structure of the
    GW echo (not just its power spectrum) drives the entrainment effect.

    Parameters
    ----------
    plv_A, plv_B : float
        Phase Locking Values for stimuli A and B.
    G_mean_A, G_mean_B : float
        Mean Genesis Scores for stimuli A and B.

    Returns
    -------
    dict
        Comparison summary with effect sizes.
    """
    delta_plv = plv_A - plv_B
    delta_G = G_mean_A - G_mean_B
    return {
        "PLV_A": plv_A,
        "PLV_B": plv_B,
        "delta_PLV": delta_plv,
        "G_mean_A": G_mean_A,
        "G_mean_B": G_mean_B,
        "delta_G": delta_G,
        "A_greater_B_PLV": bool(delta_plv > 0),
        "A_greater_B_G": bool(delta_G > 0),
        "phase_structure_effect": bool(delta_plv > 0 and delta_G > 0),
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_phase_entrainment(
    stimulus_label: str = "all",
    eeg_file: Optional[str] = None,
    output_dir: Path = Path("."),
    verbose: bool = True,
) -> dict:
    """
    Full bio-link phase-entrainment analysis pipeline.

    Generates stimuli A, B, C, D (or a single one if *stimulus_label* is
    given), synthesises / loads an EEG signal, computes G(t) and PLV for each
    stimulus, and writes a JSON results file.

    Parameters
    ----------
    stimulus_label : str
        Which stimulus to analyse: ``'A'``, ``'B'``, ``'C'``, ``'D'``, or
        ``'all'`` (default).
    eeg_file : str or None
        Path to an EEG file (.npy or .npz).  If None, uses synthetic EEG.
    output_dir : Path
        Directory for output files.
    verbose : bool
        Print progress information.

    Returns
    -------
    dict
        Analysis results including G(t) statistics, PLV, and A vs B comparison.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fs = EEG_FS
    duration = EEG_DURATION_S

    if verbose:
        print("=" * 60)
        print("  Bio-Link Phase Entrainment – GW150914 Eco Transpuesto")
        print("=" * 60)
        if eeg_file is None:
            print("  ⚠  EEG: usando datos sintéticos (fallback)")
        print(f"  Estímulo(s): {stimulus_label}")
        print()

    # Safety note
    if verbose:
        print("  📋 PROTOCOLO DE SEGURIDAD:")
        print("     • Amplitud normalizada ≤ 0.5")
        print("     • Sin parpadeo visual rápido (sólo estímulo auditivo/eléctrico)")
        print("     • No usar con historial de epilepsia fotosensible")
        print()

    # Generate all stimuli
    stim_A = stimulus_A(fs=fs, duration=duration)
    stim_B = stimulus_B(stim_a=stim_A, fs=fs, duration=duration)
    stim_C = stimulus_C(fs=fs, duration=duration)
    stim_D = stimulus_D(fs=fs, duration=duration)

    stimuli = {"A": stim_A, "B": stim_B, "C": stim_C, "D": stim_D}

    if stimulus_label.upper() != "ALL" and stimulus_label.upper() in stimuli:
        stimuli = {stimulus_label.upper(): stimuli[stimulus_label.upper()]}

    results_per_stimulus = {}

    for label, stim in stimuli.items():
        if verbose:
            print(f"  [Estímulo {label}] Cargando EEG ...")
        eeg, actual_fs = load_eeg(
            eeg_file, fs=fs, duration=duration, stimulus=stim
        )

        if verbose:
            print(f"  [Estímulo {label}] Calculando G(t) y PLV ...")
        t_g, G = compute_genesis_score(stim, eeg, fs=actual_fs)
        plv = compute_plv(stim, eeg, fs=actual_fs)

        results_per_stimulus[label] = {
            "PLV": plv,
            "G_mean": float(np.mean(G)),
            "G_max": float(np.max(G)),
            "G_std": float(np.std(G)),
            "G_t_sample": G[:20].tolist(),   # first 20 values for compactness
            "t_sample": t_g[:20].tolist(),
        }

        if verbose:
            print(f"     PLV       = {plv:.4f}")
            print(f"     G(t) mean = {np.mean(G):.4f}")
            print(f"     G(t) max  = {np.max(G):.4f}")

    # A vs B comparison (if both computed)
    ab_comparison = None
    if "A" in results_per_stimulus and "B" in results_per_stimulus:
        ab_comparison = compare_A_vs_B(
            plv_A=results_per_stimulus["A"]["PLV"],
            plv_B=results_per_stimulus["B"]["PLV"],
            G_mean_A=results_per_stimulus["A"]["G_mean"],
            G_mean_B=results_per_stimulus["B"]["G_mean"],
        )
        if verbose:
            print()
            print("  COMPARACIÓN A vs B (estructura de fase vs espectro):")
            print(f"     ΔPLV (A−B)  = {ab_comparison['delta_PLV']:+.4f}")
            print(f"     ΔG   (A−B)  = {ab_comparison['delta_G']:+.4f}")
            print(f"     Efecto fase : {ab_comparison['phase_structure_effect']}")

    results = {
        "event": "GW150914_echo_transposed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "fs": fs,
            "duration_s": duration,
            "gamma_band_hz": list(GAMMA_BAND_HZ),
            "gamma_center_hz": GAMMA_CENTER_HZ,
            "echo_freq_astro_hz": ECHO_FREQ_ASTRO_HZ,
            "freq_scale_factor": FREQ_SCALE_FACTOR,
            "echo_delay_s": ECHO_DELAY_S,
            "eeg_source": eeg_file or "synthetic",
            "max_stimulus_amplitude": MAX_STIMULUS_AMP,
        },
        "safety": {
            "amplitude_normalised": True,
            "max_amplitude": MAX_STIMULUS_AMP,
            "no_visual_flicker": True,
            "photosensitive_epilepsy_warning": True,
        },
        "stimuli": results_per_stimulus,
        "A_vs_B_comparison": ab_comparison,
    }

    out_file = output_dir / "bio_link_phase_entrainment_results.json"
    out_file.write_text(json.dumps(results, indent=2))

    if verbose:
        print()
        print(f"  Resultados guardados en: {out_file}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bio-Link Phase Entrainment: G(t) y PLV para estímulos GW-eco"
    )
    parser.add_argument(
        "--stimulus",
        default="all",
        choices=["A", "B", "C", "D", "all"],
        help="Estímulo a analizar (default: all)",
    )
    parser.add_argument(
        "--all-stimuli",
        action="store_true",
        help="Analizar todos los estímulos A, B, C, D (equivalente a --stimulus all)",
    )
    parser.add_argument(
        "--eeg-file", default=None, metavar="FILE",
        help="Ruta a archivo EEG (.npy o .npz); si no se indica, usa datos sintéticos",
    )
    parser.add_argument(
        "--output-dir", default=".", metavar="DIR",
        help="Directorio para resultados (default: .)",
    )
    parser.add_argument("--quiet", action="store_true",
                        help="Suprimir salida detallada")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    label = "all" if args.all_stimuli else args.stimulus
    run_phase_entrainment(
        stimulus_label=label,
        eeg_file=args.eeg_file,
        output_dir=Path(args.output_dir),
        verbose=not args.quiet,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
