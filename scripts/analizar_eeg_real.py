#!/usr/bin/env python3
"""
🧠 FASE 2 – ANÁLISIS DE DATOS EEG REALES

Análisis espectral de señales EEG para detectar resonancia en f₀ = 141.7001 Hz

Este script carga datos EEG reales (formato EDF o arrays NumPy) y
analiza la densidad espectral de potencia para identificar la
frecuencia cuántica fundamental f₀ = 141.7001 Hz.

Fuentes de datos compatibles:
- PhysioNet EEG Motor Movement
- Kaggle EEG datasets
- Cualquier archivo EDF con frecuencia de muestreo ≥ 256 Hz

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
"""

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, welch

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_eeg_edf(file_path, channel=0):
    """
    Load EEG data from EDF file using pyedflib.

    Parameters
    ----------
    file_path : str
        Path to the EDF file.
    channel : int
        Channel index to read (default: 0).

    Returns
    -------
    tuple
        (time_array, signal, sample_rate)
    """
    try:
        import pyedflib
    except ImportError:
        raise ImportError(
            "pyedflib is required for EDF file reading. "
            "Install with: pip install pyedflib"
        )

    f = pyedflib.EdfReader(file_path)
    try:
        signal = f.readSignal(channel)
        fs = f.getSampleFrequency(channel)
        labels = f.getSignalLabels()
        print(f"Canal cargado: {labels[channel] if labels else channel}")
    finally:
        f._close()

    time = np.linspace(0, len(signal) / fs, len(signal), endpoint=False)
    return time, signal, fs


def load_eeg_numpy(file_path, fs=256):
    """
    Load EEG data from NumPy file.

    Parameters
    ----------
    file_path : str
        Path to .npy or .npz file.
    fs : float
        Sample rate in Hz (default: 256).

    Returns
    -------
    tuple
        (time_array, signal, sample_rate)
    """
    data = np.load(file_path)
    if hasattr(data, 'files'):
        # Handle .npz files
        if 'signal' in data:
            signal = data['signal']
        elif 'eeg' in data:
            signal = data['eeg']
        else:
            # Use first array
            key = list(data.keys())[0]
            signal = data[key]
        if 'fs' in data:
            fs = float(data['fs'])
    else:
        signal = data

    # If signal is 2D, take first channel
    if signal.ndim > 1:
        signal = signal[0] if signal.shape[0] < signal.shape[1] else signal[:, 0]

    time = np.linspace(0, len(signal) / fs, len(signal), endpoint=False)
    return time, signal, fs


def generate_synthetic_eeg(fs=512, duration=60, target_freq=141.7001):
    """
    Generate synthetic EEG data with embedded f₀ signal.

    Parameters
    ----------
    fs : float
        Sample rate in Hz.
    duration : float
        Duration in seconds.
    target_freq : float
        Target frequency to embed.

    Returns
    -------
    tuple
        (time_array, signal, sample_rate)
    """
    n_samples = int(fs * duration)
    time = np.linspace(0, duration, n_samples, endpoint=False)

    np.random.seed(42)

    # Base EEG-like noise (1/f pink noise approximation)
    white_noise = np.random.normal(0, 1, n_samples)

    # Create pink noise by filtering
    b, a = butter(2, 0.1, btype='high', fs=fs)
    pink_noise = filtfilt(b, a, white_noise)

    # Add typical EEG bands
    # Alpha (8-12 Hz)
    alpha = 0.5 * np.sin(2 * np.pi * 10 * time)
    # Beta (12-30 Hz)
    beta = 0.3 * np.sin(2 * np.pi * 20 * time)
    # Gamma (30-100 Hz)
    gamma = 0.2 * np.sin(2 * np.pi * 40 * time)

    # Add weak signal at target frequency (simulating f₀ resonance)
    f0_signal = 0.1 * np.sin(2 * np.pi * target_freq * time)

    # Combine
    signal = pink_noise + alpha + beta + gamma + f0_signal

    # Normalize to microvolt range
    signal = signal * 10  # ~10 µV typical

    return time, signal, fs


def analyze_eeg(time, signal, fs, target_freq=141.7001, nperseg=1024):
    """
    Analyze EEG signal using Welch PSD method.

    Parameters
    ----------
    time : ndarray
        Time array.
    signal : ndarray
        EEG signal.
    fs : float
        Sample rate in Hz.
    target_freq : float
        Target frequency (default: 141.7001 Hz).
    nperseg : int
        Samples per segment for Welch.

    Returns
    -------
    tuple
        (freqs, psd, snr, peak_freq)
    """
    # Ensure sufficient frequency resolution
    if fs < target_freq * 2:
        print(f"ADVERTENCIA: Frecuencia de muestreo ({fs} Hz) es menor que "
              f"2x frecuencia objetivo ({target_freq} Hz). "
              "Nyquist no se cumple para f₀.")

    # Compute Welch PSD
    freqs, psd = welch(signal, fs=fs, nperseg=min(nperseg, len(signal) // 2),
                       window='hann')

    # Find closest frequency to target
    if target_freq <= freqs[-1]:
        idx = np.argmin(np.abs(freqs - target_freq))
        power = psd[idx]
        peak_freq = freqs[idx]
    else:
        # Target frequency is beyond Nyquist
        idx = -1
        power = 0
        peak_freq = target_freq

    # Calculate noise in surrounding band (excluding ±5 Hz around target)
    if target_freq <= freqs[-1]:
        noise_mask = ((freqs < target_freq - 5) | (freqs > target_freq + 5))
        noise_power = np.mean(psd[noise_mask]) if np.any(noise_mask) else 1.0
    else:
        # Use last 10% of frequencies as noise estimate
        noise_power = np.mean(psd[-len(psd)//10:])

    snr = power / noise_power if noise_power > 0 else 0.0

    return freqs, psd, snr, peak_freq


def plot_eeg_psd(freqs, psd, target_freq, snr, save_path=None, show=True):
    """
    Plot EEG Power Spectral Density with f₀ annotation.

    Parameters
    ----------
    freqs : ndarray
        Frequency array.
    psd : ndarray
        PSD values.
    target_freq : float
        Target frequency (f₀).
    snr : float
        Signal-to-noise ratio.
    save_path : str, optional
        Path to save the figure.
    show : bool
        Whether to display the plot.
    """
    plt.figure(figsize=(12, 6))

    # Plot PSD
    plt.semilogy(freqs, psd, 'b-', linewidth=0.8, alpha=0.8,
                 label='Welch PSD')

    # Mark target frequency if within range
    if target_freq <= freqs[-1]:
        plt.axvline(x=target_freq, color='r', linestyle='--', linewidth=2,
                    label=f'f₀ = {target_freq} Hz', alpha=0.8)

        # Highlight target band
        plt.axvspan(140, 150, color='green', alpha=0.2,
                    label='Banda 140–150 Hz')

    # Mark typical EEG bands
    bands = [
        (1, 4, 'Delta', 'purple'),
        (4, 8, 'Theta', 'blue'),
        (8, 12, 'Alpha', 'cyan'),
        (12, 30, 'Beta', 'green'),
        (30, 100, 'Gamma', 'yellow'),
    ]
    for fmin, fmax, name, color in bands:
        if fmax <= freqs[-1]:
            plt.axvspan(fmin, fmax, color=color, alpha=0.1)

    plt.title(f'Señal EEG Real - PSD (SNR en f₀ = {snr:.2f})',
              fontsize=14, fontweight='bold')
    plt.xlabel('Frecuencia (Hz)', fontsize=12)
    plt.ylabel('PSD (µV²/Hz)', fontsize=12)
    plt.xlim(0, min(freqs[-1], 200))
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figura guardada en: {save_path}")

    if show:
        plt.show()
    else:
        plt.close()


def main(data_path=None, channel=0, target_freq=141.7001, fs=256,
         save_plot=False, show_plot=True, use_synthetic=False):
    """
    Main EEG analysis function.

    Parameters
    ----------
    data_path : str, optional
        Path to EEG data file (EDF or NumPy format).
    channel : int
        Channel to analyze.
    target_freq : float
        Target frequency for f₀ analysis.
    fs : float
        Sample rate (for NumPy files).
    save_plot : bool
        Whether to save the plot.
    show_plot : bool
        Whether to display the plot.
    use_synthetic : bool
        Whether to use synthetic data.

    Returns
    -------
    dict
        Analysis results.
    """
    if data_path and os.path.exists(data_path):
        ext = Path(data_path).suffix.lower()
        print(f"Cargando datos EEG desde: {data_path}")

        if ext == '.edf':
            time, signal, fs = load_eeg_edf(data_path, channel)
            data_source = "EDF Real Data"
        elif ext in ['.npy', '.npz']:
            time, signal, fs = load_eeg_numpy(data_path, fs)
            data_source = "NumPy Data"
        else:
            print(f"Formato no soportado: {ext}")
            return None
    elif use_synthetic:
        print("Usando datos EEG sintéticos")
        time, signal, fs = generate_synthetic_eeg(
            fs=max(512, int(target_freq * 3)),  # Ensure Nyquist
            duration=60,
            target_freq=target_freq
        )
        data_source = "Synthetic EEG"
    else:
        print(f"ERROR: Archivo no encontrado: {data_path}")
        print("\nPara usar datos sintéticos, agregue la opción --synthetic")
        print("\nFuentes de datos EEG reales:")
        print("  - PhysioNet: https://physionet.org/content/eegmmidb/1.0.0/")
        print("  - Kaggle: https://www.kaggle.com/datasets/")
        return None

    print(f"\n{'='*60}")
    print(f"Análisis Espectral de {data_source}")
    print(f"{'='*60}")
    print(f"Duración: {time[-1] - time[0]:.2f} s")
    print(f"Frecuencia de muestreo: {fs} Hz")
    print(f"Muestras: {len(signal)}")
    print(f"Frecuencia Nyquist: {fs/2} Hz")

    # Perform spectral analysis
    freqs, psd, snr, peak_freq = analyze_eeg(time, signal, fs, target_freq)

    # Calculate deviation from theoretical f₀
    if target_freq <= freqs[-1]:
        deviation = abs(peak_freq - target_freq)
        nyquist_ok = True
    else:
        deviation = float('inf')
        nyquist_ok = False
        print(f"\nADVERTENCIA: f₀ = {target_freq} Hz está más allá de "
              f"la frecuencia Nyquist ({fs/2} Hz)")

    print("\n--- Resultados ---")
    if nyquist_ok:
        print(f"Frecuencia pico analizada: {peak_freq:.4f} Hz")
        print(f"Diferencia con f₀ = {target_freq} Hz: {deviation:.4f} Hz")
        print(f"SNR en f₀: {snr:.2f}")
    else:
        print(f"Frecuencia objetivo f₀ = {target_freq} Hz no analizable")
        print(f"Se requiere fs ≥ {target_freq * 2} Hz")

    # Plot if requested
    if save_plot or show_plot:
        save_path = "eeg_real_psd.png" if save_plot else None
        plot_eeg_psd(freqs, psd, target_freq, snr, save_path, show_plot)

    return {
        'data_source': data_source,
        'peak_freq': peak_freq,
        'target_freq': target_freq,
        'deviation': deviation,
        'snr': snr,
        'fs': fs,
        'nyquist_ok': nyquist_ok,
        'freqs': freqs,
        'psd': psd,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Análisis espectral de EEG para f₀ = 141.7001 Hz"
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        default=None,
        help="Path to EEG data file (EDF or NumPy format)"
    )
    parser.add_argument(
        '--channel', '-c',
        type=int,
        default=0,
        help="Channel index to analyze (default: 0)"
    )
    parser.add_argument(
        '--target-freq', '-t',
        type=float,
        default=141.7001,
        help="Target frequency f₀ (default: 141.7001 Hz)"
    )
    parser.add_argument(
        '--sample-rate', '-r',
        type=float,
        default=256,
        help="Sample rate for NumPy files (default: 256 Hz)"
    )
    parser.add_argument(
        '--synthetic', '-s',
        action='store_true',
        help="Use synthetic EEG data"
    )
    parser.add_argument(
        '--save-plot',
        action='store_true',
        help="Save plot to file"
    )
    parser.add_argument(
        '--no-show',
        action='store_true',
        help="Don't display plot"
    )

    args = parser.parse_args()

    result = main(
        data_path=args.file,
        channel=args.channel,
        target_freq=args.target_freq,
        fs=args.sample_rate,
        save_plot=args.save_plot,
        show_plot=not args.no_show,
        use_synthetic=args.synthetic,
    )

    if result:
        print("\n✅ Análisis completado exitosamente")
        if result['nyquist_ok']:
            if result['deviation'] <= 1.0:
                print(f"✓ Coherencia detectada: desviación = {result['deviation']:.4f} Hz ≤ 1 Hz")
            if result['snr'] >= 5:
                print(f"✓ SNR significativo: {result['snr']:.2f} ≥ 5")
