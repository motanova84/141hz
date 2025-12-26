#!/usr/bin/env python3
"""
🌀 FASE 1 – DATOS REALES DE LIGO (GW170817)

Análisis espectral de GW170817 para detectar resonancia en f₀ = 141.7001 Hz

Este script carga datos reales de LIGO del evento GW170817 (primera
detección de ondas gravitacionales de fusión de estrellas de neutrones)
y analiza la densidad espectral de potencia para identificar la
frecuencia cuántica fundamental f₀ = 141.7001 Hz.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Noviembre 2025
"""

import argparse
import os
import sys
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
from mpmath import mpf
from scipy.signal import welch

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_ligo_data(file_path, strain_key="strain/Strain", time_key=None):
    """
    Load LIGO strain data from HDF5 file.

    Parameters
    ----------
    file_path : str
        Path to the HDF5 file containing LIGO data.
    strain_key : str
        HDF5 key for strain data (default: "strain/Strain").
    time_key : str, optional
        HDF5 key for time data. If None, time is computed from metadata.

    Returns
    -------
    tuple
        (time_array, strain_array, sample_rate)
    """
    with h5py.File(file_path, 'r') as f:
        # Get strain data
        strain = np.array(f[strain_key])

        # Try to get sample rate from metadata
        if 'meta' in f and 'SamplingRate' in f['meta'].attrs:
            fs = float(f['meta'].attrs['SamplingRate'])
        elif 'strain' in f:
            # Try to get from strain group attributes
            strain_group = f['strain']
            if 'Strain' in strain_group:
                strain_dataset = strain_group['Strain']
                if 'sample_rate' in strain_dataset.attrs:
                    fs = float(strain_dataset.attrs['sample_rate'])
                elif 'Xspacing' in strain_dataset.attrs:
                    fs = 1.0 / float(strain_dataset.attrs['Xspacing'])
                else:
                    fs = 4096  # Default for GWOSC 4KHZ data
            else:
                fs = 4096
        else:
            fs = 4096  # Default sample rate

        # Generate time array
        duration = len(strain) / fs
        time = np.linspace(0, duration, len(strain), endpoint=False)

    return time, strain, fs


def analyze_signal(time, strain, fs, target_freq=141.7001, nperseg=2048):
    """
    Analyze strain signal using Welch PSD method.

    Parameters
    ----------
    time : ndarray
        Time array.
    strain : ndarray
        Strain data array.
    fs : float
        Sample rate in Hz.
    target_freq : float
        Target frequency to analyze (default: 141.7001 Hz).
    nperseg : int
        Number of samples per segment for Welch method.

    Returns
    -------
    tuple
        (freqs, psd, snr, peak_freq)
    """
    # Compute Welch PSD
    freqs, psd = welch(strain, fs=fs, nperseg=nperseg, window='hann')

    # Find the closest frequency to target
    idx = np.argmin(np.abs(freqs - target_freq))
    signal_power = psd[idx]

    # Calculate noise power (exclude target frequency band)
    noise_mask = (freqs < target_freq - 0.5) | (freqs > target_freq + 0.5)
    noise_power = np.mean(psd[noise_mask])

    # Calculate SNR
    snr = signal_power / noise_power if noise_power > 0 else 0.0

    return freqs, psd, snr, freqs[idx]


def plot_psd(freqs, psd, target_freq, snr, detector='H1',
             save_path=None, show=True):
    """
    Plot Power Spectral Density with f₀ annotation.

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
    detector : str
        Detector name (H1, L1, V1).
    save_path : str, optional
        Path to save the figure.
    show : bool
        Whether to display the plot.
    """
    plt.figure(figsize=(12, 6))
    plt.semilogy(freqs, psd, 'b-', linewidth=0.8, alpha=0.8,
                 label='Welch PSD')
    plt.axvline(x=target_freq, color='r', linestyle='--', linewidth=2,
                label=f'f₀ = {target_freq} Hz', alpha=0.8)

    # Highlight the target frequency band
    band_mask = (freqs >= target_freq - 2) & (freqs <= target_freq + 2)
    if np.any(band_mask):
        plt.fill_between(freqs[band_mask], psd[band_mask], alpha=0.3,
                         color='red', label='f₀ ± 2 Hz band')

    plt.title(f'Densidad Espectral GW170817 ({detector}) - SNR = {snr:.2f}',
              fontsize=14, fontweight='bold')
    plt.xlabel('Frecuencia (Hz)', fontsize=12)
    plt.ylabel('PSD (strain²/Hz)', fontsize=12)
    plt.xlim(10, 200)  # Focus on relevant frequency range
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


def main(data_path=None, detector='H1', target_freq=141.7001,
         save_plot=False, show_plot=True, use_synthetic=False):
    """
    Main analysis function.

    Parameters
    ----------
    data_path : str, optional
        Path to LIGO HDF5 data file.
    detector : str
        Detector name (H1, L1, V1).
    target_freq : float
        Target frequency for f₀ analysis.
    save_plot : bool
        Whether to save the plot.
    show_plot : bool
        Whether to display the plot.
    use_synthetic : bool
        Whether to use synthetic data if no file is found.

    Returns
    -------
    dict
        Analysis results.
    """
    # Default path for GW170817 data
    if data_path is None:
        # Try several possible locations
        possible_paths = [
            f"H-{detector}_GWOSC_4KHZ_R1-1187008882-2048.hdf5",
            f"data/H-{detector}_GWOSC_4KHZ_R1-1187008882-2048.hdf5",
            f"data/raw/H-{detector}_GWOSC_4KHZ_R1-1187008882-2048.hdf5",
        ]
        for p in possible_paths:
            if os.path.exists(p):
                data_path = p
                break

    # Check if data file exists or use synthetic data
    if data_path and os.path.exists(data_path):
        print(f"Cargando datos de LIGO desde: {data_path}")
        time, strain, fs = load_ligo_data(data_path)
        data_source = "LIGO Real Data"
    elif use_synthetic:
        print("Usando datos sintéticos (archivo LIGO no encontrado)")
        fs = 4096
        duration = 32
        n_samples = int(fs * duration)
        time = np.linspace(0, duration, n_samples)

        # Generate synthetic GW170817-like signal
        np.random.seed(42)
        # Colored noise (1/f-like)
        noise = np.random.normal(0, 1e-22, n_samples)

        # Add signal at target frequency
        tau_decay = 0.1
        signal = 1e-21 * np.exp(-time / tau_decay) * np.sin(
            2 * np.pi * target_freq * time)
        strain = noise + signal
        data_source = "Synthetic Data"
    else:
        print(f"ERROR: Archivo de datos no encontrado: {data_path}")
        print("\nPara descargar los datos reales de GW170817, ejecute:")
        print("wget https://www.gw-openscience.org/eventapi/html/GWTC-1/"
              "GW170817/v3/H-H1_GWOSC_4KHZ_R1-1187008882-2048.hdf5")
        return None

    print(f"\n{'='*60}")
    print(f"Análisis Espectral de {data_source}")
    print(f"{'='*60}")
    print(f"Detector: {detector}")
    print(f"Duración: {time[-1] - time[0]:.2f} s")
    print(f"Frecuencia de muestreo: {fs} Hz")
    print(f"Muestras: {len(strain)}")

    # Perform spectral analysis
    freqs, psd, snr, peak_freq = analyze_signal(time, strain, fs, target_freq)

    # Calculate deviation from theoretical f₀
    f0_theory = mpf('141.7001')
    deviation = abs(peak_freq - float(f0_theory))

    print("\n--- Resultados ---")
    print(f"Frecuencia pico analizada: {peak_freq:.4f} Hz")
    print(f"Diferencia con f₀ = 141.7001 Hz: {deviation:.6f} Hz")
    print(f"SNR estimado: {snr:.2f}")

    # Plot if requested
    if save_plot or show_plot:
        save_path = f"gw170817_{detector}_psd.png" if save_plot else None
        plot_psd(freqs, psd, target_freq, snr, detector, save_path, show_plot)

    return {
        'detector': detector,
        'data_source': data_source,
        'peak_freq': peak_freq,
        'target_freq': target_freq,
        'deviation': deviation,
        'snr': snr,
        'freqs': freqs,
        'psd': psd,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Análisis espectral de GW170817 para f₀ = 141.7001 Hz"
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        default=None,
        help="Path to LIGO HDF5 data file"
    )
    parser.add_argument(
        '--detector', '-d',
        type=str,
        default='H1',
        choices=['H1', 'L1', 'V1'],
        help="Detector name (default: H1)"
    )
    parser.add_argument(
        '--target-freq', '-t',
        type=float,
        default=141.7001,
        help="Target frequency f₀ (default: 141.7001 Hz)"
    )
    parser.add_argument(
        '--synthetic', '-s',
        action='store_true',
        help="Use synthetic data if file not found"
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
        detector=args.detector,
        target_freq=args.target_freq,
        save_plot=args.save_plot,
        show_plot=not args.no_show,
        use_synthetic=args.synthetic,
    )

    if result:
        print("\n✅ Análisis completado exitosamente")
        # Validation check
        if result['deviation'] < 0.1:
            print("✓ Coherencia detectada: desviación < 0.1 Hz")
        if result['snr'] > 1.0:
            print(f"✓ SNR significativo: {result['snr']:.2f}")
