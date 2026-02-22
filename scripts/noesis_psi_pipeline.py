#!/usr/bin/env python3
"""
Pipeline de Análisis Noésico PSI - "Publication-Ready"
=======================================================
Análisis de resiliencia de fase para f₀ = 141.7001 Hz bajo ruido gaussiano.

Calcula la Métrica Unificada Ψ = I(f₀) × A_eff mediante ventaneo solapado
y produce:
  - noesis_psi_results.csv  : Dataset con estadísticas por bin de SNR
  - noesis_publication_plot.png : Gráfica académica con inset espectral

Parámetros principales:
  f0 = 141.7001 Hz   — Frecuencia de Noēsis
  fs = 4096 Hz       — Frecuencia de muestreo
  bw = 2.0 Hz        — Ancho de banda del filtro paso-banda

Referencia:
  José Manuel Mota Burruezo (JMMB Ψ✧)
  Instituto Conciencia Cuántica
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch, coherence
from scipy.stats import binned_statistic
import warnings
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Parámetros de Noēsis
# ---------------------------------------------------------------------------
F0 = 141.7001          # Hz — frecuencia fundamental
FS = 4096              # Hz — frecuencia de muestreo
BW = 2.0               # Hz — ancho de banda del filtro (±1 Hz alrededor de f₀)
DURATION_S = 60        # s  — duración de la señal sintética
SNR_MIN = 0.1          # SNR mínimo explorado
SNR_MAX = 10.0         # SNR máximo explorado
N_SNR_STEPS = 30       # puntos de SNR en la curva de resiliencia
N_BINS = 8             # bins para el binning estadístico


# ---------------------------------------------------------------------------
# 1. Filtrado Noésico
# ---------------------------------------------------------------------------

def _freq_index(freqs: np.ndarray, target: float) -> int:
    """Devuelve el índice del bin más cercano a `target` en el array `freqs`."""
    return int(np.argmin(np.abs(freqs - target)))


def bandpass_noesis(data: np.ndarray, fs: float = FS,
                    f0: float = F0, bw: float = BW) -> np.ndarray:
    """Aplica filtro paso-banda Butterworth de 4º orden centrado en f₀.

    Args:
        data: Señal de entrada (array 1-D).
        fs:   Frecuencia de muestreo (Hz).
        f0:   Frecuencia central (Hz).
        bw:   Ancho de banda total (Hz).

    Returns:
        Señal filtrada con el mismo shape que `data`.
    """
    nyq = fs / 2.0
    low = (f0 - bw / 2.0) / nyq
    high = (f0 + bw / 2.0) / nyq
    low = max(low, 1e-4)
    high = min(high, 1.0 - 1e-4)
    b, a = butter(4, [low, high], btype='band')
    return filtfilt(b, a, data)


# ---------------------------------------------------------------------------
# 2. Cálculo de la Métrica Unificada Ψ por ventana
# ---------------------------------------------------------------------------

def compute_psi_windows(canal1: np.ndarray, canal2: np.ndarray,
                        fs: float = FS, f0: float = F0,
                        win_s: float = 2.0) -> list:
    """Calcula Ψ = I(f₀) × A_eff en ventanas solapadas al 50 %.

    Args:
        canal1: Primera señal filtrada.
        canal2: Segunda señal filtrada.
        fs:     Frecuencia de muestreo (Hz).
        f0:     Frecuencia objetivo (Hz).
        win_s:  Tamaño de la ventana en segundos.

    Returns:
        Lista de valores Ψ por ventana.
    """
    win = int(win_s * fs)
    step = win // 2
    nperseg = win // 2

    psi_results = []
    for i in range(0, len(canal1) - win, step):
        seg1 = canal1[i:i + win]
        seg2 = canal2[i:i + win]

        # PSD del canal 1 → I(f₀)
        f_w, Pxx = welch(seg1, fs=fs, nperseg=nperseg)
        idx = _freq_index(f_w, f0)

        # Coherencia cruzada → A_eff(f₀)
        f_c, Cxy = coherence(seg1, seg2, fs=fs, nperseg=nperseg)

        psi = float(Pxx[idx] * Cxy[idx])
        psi_results.append(psi)

    return psi_results


# ---------------------------------------------------------------------------
# 3. Generación de señales sintéticas y curva de resiliencia
# ---------------------------------------------------------------------------

def generate_resilience_curve(fs: float = FS, f0: float = F0,
                               duration_s: float = DURATION_S,
                               snr_values: np.ndarray | None = None,
                               rng: np.random.Generator | None = None
                               ) -> pd.DataFrame:
    """Barre un rango de SNR y registra la estadística de Ψ.

    Args:
        fs:         Frecuencia de muestreo (Hz).
        f0:         Frecuencia fundamental (Hz).
        duration_s: Duración de cada realización (s).
        snr_values: Array de valores SNR a evaluar.
        rng:        Generador numpy para reproducibilidad.

    Returns:
        DataFrame con columnas: snr, psi_mean, psi_std, psi_median, n_windows.
    """
    if snr_values is None:
        snr_values = np.logspace(
            np.log10(SNR_MIN), np.log10(SNR_MAX), N_SNR_STEPS
        )
    if rng is None:
        rng = np.random.default_rng(seed=42)

    n_samples = int(duration_s * fs)
    t = np.arange(n_samples) / fs

    rows = []
    for snr in snr_values:
        # Señal coherente en f₀ (idéntica fase en ambos canales)
        signal_amp = 1.0
        noise_std = signal_amp / snr

        sig = signal_amp * np.sin(2 * np.pi * f0 * t)
        noise1 = rng.normal(0, noise_std, n_samples)
        noise2 = rng.normal(0, noise_std, n_samples)

        canal1 = sig + noise1
        canal2 = sig + noise2

        # Filtrar
        xf = bandpass_noesis(canal1, fs, f0)
        yf = bandpass_noesis(canal2, fs, f0)

        # Calcular Ψ por ventana
        psi_list = compute_psi_windows(xf, yf, fs, f0)
        if not psi_list:
            continue

        psi_arr = np.array(psi_list)
        rows.append({
            'snr': snr,
            'psi_mean': float(np.mean(psi_arr)),
            'psi_std': float(np.std(psi_arr)),
            'psi_median': float(np.median(psi_arr)),
            'n_windows': len(psi_arr),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. Estadísticas por bin (binned_statistic)
# ---------------------------------------------------------------------------

def bin_results(df: pd.DataFrame, n_bins: int = N_BINS) -> pd.DataFrame:
    """Agrupa los resultados individuales de Ψ en bins de SNR.

    Args:
        df:     DataFrame con columnas snr y psi_mean.
        n_bins: Número de bins.

    Returns:
        DataFrame binneado con columnas: snr_center, psi_mean_bin, psi_std_bin.
    """
    bin_means, bin_edges, _ = binned_statistic(
        df['snr'], df['psi_mean'], statistic='mean', bins=n_bins
    )
    bin_stds, _, _ = binned_statistic(
        df['snr'], df['psi_mean'], statistic='std', bins=n_bins
    )
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    binned = pd.DataFrame({
        'snr_center': bin_centers,
        'psi_mean_bin': bin_means,
        'psi_std_bin': np.where(np.isnan(bin_stds), 0.0, bin_stds),
    })
    return binned.dropna(subset=['psi_mean_bin']).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 5. Visualización "publication-ready"
# ---------------------------------------------------------------------------

def plot_resilience(df_full: pd.DataFrame, df_binned: pd.DataFrame,
                    output_path: str | Path = 'noesis_publication_plot.png',
                    fs: float = FS, f0: float = F0,
                    snr_threshold: float = 0.20) -> None:
    """Genera la figura académica de la curva de resiliencia de Ψ.

    Incluye un inset espectral que muestra el pico estrecho en f₀.

    Args:
        df_full:        DataFrame completo (por SNR).
        df_binned:      DataFrame binneado.
        output_path:    Ruta de salida para el PNG.
        fs:             Frecuencia de muestreo (Hz).
        f0:             Frecuencia fundamental (Hz).
        snr_threshold:  SNR de referencia para la línea vertical (umbral de coherencia).
    """
    fig, ax_main = plt.subplots(figsize=(9, 6))

    # — Curva continua (puntos individuales) —
    ax_main.plot(
        df_full['snr'], df_full['psi_mean'],
        color='steelblue', linewidth=1.5, alpha=0.5, label='Ψ (por SNR)'
    )

    # — Puntos binneados con barras de error —
    ax_main.errorbar(
        df_binned['snr_center'], df_binned['psi_mean_bin'],
        yerr=df_binned['psi_std_bin'],
        fmt='o', color='navy', capsize=4, markersize=6,
        label='Ψ binneado ± σ'
    )

    # — Línea vertical: SNR de referencia —
    ax_main.axvline(
        x=snr_threshold, color='crimson', linestyle='--', linewidth=1.8,
        label=f'$SNR_s \\approx {snr_threshold:.2f}$'
    )

    ax_main.set_xscale('log')
    ax_main.set_xlabel('SNR de entrada', fontsize=13)
    ax_main.set_ylabel('Ψ = $I(f_0) \\times A_{eff}$', fontsize=13)
    ax_main.set_title(
        f'Curva de Resiliencia de Fase Noésica ($f_0 = {f0}$ Hz)',
        fontsize=14, fontweight='bold'
    )
    ax_main.legend(fontsize=11)
    ax_main.grid(True, which='both', alpha=0.3)

    # — Inset espectral: PSD de la señal sintética en SNR=5 —
    n_samples = int(4 * fs)
    t_inset = np.arange(n_samples) / fs
    rng_inset = np.random.default_rng(seed=99)
    sig_inset = np.sin(2 * np.pi * f0 * t_inset) + rng_inset.normal(0, 0.2, n_samples)
    sig_filtered = bandpass_noesis(sig_inset, fs, f0)
    f_in, Pxx_in = welch(sig_filtered, fs=fs, nperseg=n_samples // 4)

    # Ventana del inset
    ax_inset = fig.add_axes([0.55, 0.45, 0.38, 0.38])
    mask = (f_in >= f0 - 5) & (f_in <= f0 + 5)
    ax_inset.semilogy(f_in[mask], Pxx_in[mask], color='darkorange', linewidth=1.5)
    ax_inset.axvline(x=f0, color='magenta', linestyle=':', linewidth=1.5,
                     label=f'$f_0={f0}$ Hz')
    ax_inset.set_xlabel('Frecuencia (Hz)', fontsize=9)
    ax_inset.set_ylabel('PSD', fontsize=9)
    ax_inset.set_title('Inset espectral', fontsize=9)
    ax_inset.legend(fontsize=8)
    ax_inset.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"📊 Figura guardada en: {output_path}")


# ---------------------------------------------------------------------------
# 6. Pipeline principal
# ---------------------------------------------------------------------------

def run_pipeline(output_dir: str | Path = '.') -> dict:
    """Ejecuta el pipeline completo de análisis Noésico PSI.

    Args:
        output_dir: Directorio de salida para CSV y PNG.

    Returns:
        dict con rutas de archivos generados y estadísticas clave.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / 'noesis_psi_results.csv'
    png_path = output_dir / 'noesis_publication_plot.png'

    print("🌌 PIPELINE NOÉSICO PSI — f₀ = 141.7001 Hz")
    print("=" * 60)

    # Generar curva de resiliencia
    print("⚙️  Calculando curva de resiliencia...")
    snr_values = np.logspace(np.log10(SNR_MIN), np.log10(SNR_MAX), N_SNR_STEPS)
    df_full = generate_resilience_curve(snr_values=snr_values)

    # Binning estadístico
    df_binned = bin_results(df_full)

    # Guardar CSV
    df_full.to_csv(csv_path, index=False)
    print(f"💾 Dataset guardado en: {csv_path}")

    # Estimar SNR de supervivencia: SNR donde psi_mean cae por debajo del 5 % del máximo
    psi_max = df_full['psi_mean'].max()
    threshold = 0.05 * psi_max
    below = df_full[df_full['psi_mean'] < threshold]
    snr_survival = float(below['snr'].min()) if not below.empty else SNR_MIN

    # Generar figura
    plot_resilience(df_full, df_binned, output_path=png_path,
                    snr_threshold=snr_survival)

    print(f"\n📈 SNR de supervivencia estimado: {snr_survival:.3f}")
    print(f"📊 Ventanas analizadas (máx SNR): {int(df_full['n_windows'].max())}")
    print("✅ Pipeline completado.")

    return {
        'csv': str(csv_path),
        'plot': str(png_path),
        'snr_survival': snr_survival,
        'psi_max': float(psi_max),
        'n_snr_points': len(df_full),
    }


def main() -> int:
    """Punto de entrada CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Pipeline Noésico PSI — curva de resiliencia en f₀=141.7001 Hz'
    )
    parser.add_argument(
        '--output-dir', default='.',
        help='Directorio de salida para CSV y PNG (default: directorio actual)'
    )
    args = parser.parse_args()

    results = run_pipeline(output_dir=args.output_dir)
    print(f"\nArchivos generados:")
    for k, v in results.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
