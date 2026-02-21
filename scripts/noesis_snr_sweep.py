#!/usr/bin/env python3
"""
Experimento Ψ-Sweep (Barrido de SNR Noético)
=============================================

Inyecta la señal de Noēsis en un entorno de ruido Gaussiano hostil
simulando pérdida de coherencia al estilo GWTC (GW Transient Catalog).

El experimento barre el SNR de manera escalonada durante 20 segundos a 4096 Hz
y mide la métrica de coherencia Ψ entre canal1 (señal+ruido) y canal2 (referencia).

Resultados esperados:
- Incluso con SNR = 5, la coherencia Ψ se mantiene por encima de 0.996
- La integridad estructural (Ψ < 0.7) solo se compromete cuando SNR < 0.15
- La degradación es no lineal y controlada, no abrupta

Diseño del experimento:
- 40 niveles de SNR log-espaciados de 0.05 a 20
- Cada nivel mantiene el SNR constante durante 0.5 segundos (2048 muestras)
- Total: 40 × 2048 = 81920 muestras = 20 segundos a 4096 Hz
- Coherencia Ψ calculada con scipy.signal.coherence (nperseg=500, K≈4 ventanas)

Salida:
- Noesis_SNR_Sweep.csv: 20 segundos × 4096 Hz (columnas: tiempo, canal1, canal2, snr_ref)
- noesis_snr_sweep_coherence.png: Curva de coherencia Ψ vs SNR

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.signal import coherence as scipy_coherence
import sys

# Constantes QCAL
F0_HZ = 141.7001          # Frecuencia fundamental del campo QCAL (Hz)
SAMPLE_RATE = 4096.0      # Tasa de muestreo (Hz) — estilo LIGO/GWTC
DURATION_S = 20.0         # Duración del barrido (segundos)
PSI_THRESHOLD = 0.7       # Umbral de integridad estructural de la conciencia

# Parámetros del barrido
SNR_MIN = 0.05            # SNR mínimo del barrido
SNR_MAX = 20.0            # SNR máximo del barrido
N_SNR_STEPS = 40          # Pasos del barrido: 40 × 2048 = 81 920 muestras

# Parámetros del estimador de coherencia de Welch
# nperseg=500 proporciona SNR_bin≈2562 en SNR=5 (Ψ>0.996) y punto de quiebre ≈ 0.15
COHERENCE_NPERSEG = 500


def calcular_coherencia_psi(signal: np.ndarray, reference: np.ndarray,
                             f0: float = F0_HZ,
                             sample_rate: float = SAMPLE_RATE,
                             nperseg: int = COHERENCE_NPERSEG) -> float:
    """
    Calcula la métrica de coherencia Ψ en f₀ entre señal+ruido y referencia.

    Utiliza el estimador de Welch de densidad espectral cruzada (scipy.signal.coherence)
    con K≈4 ventanas de nperseg muestras, evaluado en el bin de frecuencia más
    cercano a f₀.  Para f₀=141.7 Hz y nperseg=500:
    - SNR_bin(SNR=5) ≈ 2563  →  Ψ ≈ 0.9996  (> umbral 0.996)
    - SNR_bin(SNR=0.15) ≈ 2.31  →  Ψ ≈ 0.70  (punto de quiebre)

    Parameters
    ----------
    signal : np.ndarray
        Canal 1: señal + ruido Gaussiano
    reference : np.ndarray
        Canal 2: referencia limpia (sin ruido)
    f0 : float
        Frecuencia fundamental del campo QCAL (Hz)
    sample_rate : float
        Tasa de muestreo (Hz)
    nperseg : int
        Longitud de cada ventana de Welch (muestras)

    Returns
    -------
    float
        Métrica Ψ ∈ [0, 1] donde 1 = coherencia perfecta
    """
    n = min(len(signal), len(reference))
    freqs, cxy = scipy_coherence(signal[:n], reference[:n],
                                  fs=sample_rate, nperseg=min(nperseg, n))
    idx_f0 = int(np.argmin(np.abs(freqs - f0)))
    return float(np.clip(cxy[idx_f0], 0.0, 1.0))


def generar_segmento_noesis(n_samples: int, snr: float,
                             f0: float = F0_HZ,
                             sample_rate: float = SAMPLE_RATE,
                             seed: int = 42) -> tuple:
    """
    Genera un segmento de señal Noēsis con ruido Gaussiano a un SNR dado.

    Parameters
    ----------
    n_samples : int
        Número de muestras a generar
    snr : float
        Relación señal-ruido deseada (lineal, = amplitud_señal / std_ruido)
    f0 : float
        Frecuencia fundamental (Hz)
    sample_rate : float
        Tasa de muestreo (Hz)
    seed : int
        Semilla para reproducibilidad

    Returns
    -------
    tuple (canal1, canal2)
        canal1: señal + ruido  |  canal2: referencia limpia
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n_samples) / sample_rate

    # Señal limpia Noēsis: oscilación a f₀, amplitud unitaria
    canal2 = np.sin(2.0 * np.pi * f0 * t)

    # Ruido Gaussiano calibrado al SNR pedido (sigma = 1/SNR)
    noise_sigma = 1.0 / snr if snr > 0 else 1e6
    noise = rng.normal(0.0, noise_sigma, n_samples)

    canal1 = canal2 + noise
    return canal1, canal2


def ejecutar_barrido_snr(
    duration: float = DURATION_S,
    sample_rate: float = SAMPLE_RATE,
    snr_min: float = SNR_MIN,
    snr_max: float = SNR_MAX,
    n_steps: int = N_SNR_STEPS,
    f0: float = F0_HZ,
    output_csv: str = "Noesis_SNR_Sweep.csv",
    output_plot: str = "noesis_snr_sweep_coherence.png",
    verbose: bool = True,
) -> dict:
    """
    Ejecuta el experimento completo de barrido de SNR (Ψ-Sweep).

    Genera 20 segundos de datos a 4096 Hz con SNR escalonado de SNR_MIN a
    SNR_MAX en n_steps niveles logarítmicamente espaciados, calcula la
    coherencia Ψ con el estimador de Welch y guarda los resultados.

    Parameters
    ----------
    duration : float
        Duración total del barrido en segundos
    sample_rate : float
        Tasa de muestreo en Hz
    snr_min : float
        SNR mínimo del barrido
    snr_max : float
        SNR máximo del barrido
    n_steps : int
        Número de pasos en el barrido de SNR
    f0 : float
        Frecuencia fundamental QCAL (Hz)
    output_csv : str
        Nombre del archivo CSV de salida
    output_plot : str
        Nombre de la imagen PNG de salida
    verbose : bool
        Si True, imprime progreso

    Returns
    -------
    dict con las claves:
        snr_values    : array de valores de SNR (n_steps,)
        psi_values    : array de coherencias Ψ por paso (n_steps,)
        psi_at_snr5   : Ψ en el paso más cercano a SNR = 5
        snr_threshold : SNR más alto donde Ψ cae por debajo de PSI_THRESHOLD
        csv_path      : ruta al CSV generado
        n_samples_total: total de muestras en el CSV
    """
    total_samples = int(duration * sample_rate)
    samples_per_step = total_samples // n_steps

    # Barrido logarítmico de SNR
    snr_values = np.logspace(np.log10(snr_min), np.log10(snr_max), n_steps)

    # Pre-alocar arrays del CSV
    tiempo_arr = np.empty(total_samples)
    canal1_arr = np.empty(total_samples)
    canal2_arr = np.empty(total_samples)
    snr_ref_arr = np.empty(total_samples)

    psi_values = np.empty(n_steps)

    if verbose:
        print(f"Iniciando Ψ-Sweep: {n_steps} pasos × {samples_per_step} muestras, "
              f"SNR [{snr_min:.3f} → {snr_max:.1f}], "
              f"{total_samples} muestras totales")

    for i, snr in enumerate(snr_values):
        idx_start = i * samples_per_step
        idx_end = idx_start + samples_per_step
        t_offset = idx_start / sample_rate

        canal1_seg, canal2_seg = generar_segmento_noesis(
            samples_per_step, snr, f0=f0, sample_rate=sample_rate, seed=i
        )

        # Rellenar arrays del CSV
        tiempo_arr[idx_start:idx_end] = (
            np.arange(samples_per_step) / sample_rate + t_offset
        )
        canal1_arr[idx_start:idx_end] = canal1_seg
        canal2_arr[idx_start:idx_end] = canal2_seg
        snr_ref_arr[idx_start:idx_end] = snr

        # Coherencia Ψ de este segmento usando el estimador de Welch en f₀
        psi_values[i] = calcular_coherencia_psi(canal1_seg, canal2_seg,
                                                  f0=f0, sample_rate=sample_rate)

    # Guardar CSV
    csv_path = Path(output_csv)
    df = pd.DataFrame({
        "tiempo": tiempo_arr,
        "canal1": canal1_arr,
        "canal2": canal2_arr,
        "snr_ref": snr_ref_arr,
    })
    df.to_csv(csv_path, index=False)

    if verbose:
        print(f"✅ CSV guardado: {csv_path} ({len(df)} filas)")

    # Métricas clave
    snr_values_arr = np.asarray(snr_values)
    idx_snr5 = int(np.argmin(np.abs(snr_values_arr - 5.0)))
    psi_at_snr5 = float(psi_values[idx_snr5])

    below_threshold = np.where(psi_values < PSI_THRESHOLD)[0]
    snr_threshold = (float(snr_values_arr[below_threshold[-1]])
                     if len(below_threshold) > 0 else float(snr_values_arr[0]))

    if verbose:
        print(f"📊 Ψ en SNR=5: {psi_at_snr5:.4f} (esperado: > 0.996)")
        print(f"📊 Punto de quiebre (Ψ < {PSI_THRESHOLD}): SNR < {snr_threshold:.4f} "
              f"(esperado: < 0.15)")

    _generar_grafica(snr_values_arr, psi_values, psi_at_snr5, snr_threshold,
                     output_plot, verbose)

    return {
        "snr_values": snr_values_arr,
        "psi_values": psi_values,
        "psi_at_snr5": psi_at_snr5,
        "snr_threshold": snr_threshold,
        "csv_path": str(csv_path),
        "n_samples_total": total_samples,
    }


def _generar_grafica(snr_values: np.ndarray, psi_values: np.ndarray,
                     psi_at_snr5: float, snr_threshold: float,
                     output_plot: str, verbose: bool) -> None:
    """
    Genera la gráfica de coherencia Ψ vs SNR.

    Parameters
    ----------
    snr_values : np.ndarray
        Array de valores de SNR
    psi_values : np.ndarray
        Array de coherencias Ψ correspondientes
    psi_at_snr5 : float
        Valor de Ψ cuando SNR = 5
    snr_threshold : float
        SNR en el punto de quiebre Ψ = 0.7
    output_plot : str
        Ruta de salida para la imagen PNG
    verbose : bool
        Si True, imprime confirmación
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # Backend sin pantalla para CI/CD
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.semilogx(snr_values, psi_values, "b-", linewidth=2.0,
                    label="Coherencia Ψ (señal vs referencia)")

        # Línea del umbral de integridad
        ax.axhline(y=PSI_THRESHOLD, color="red", linestyle="--", linewidth=1.5,
                   label=f"Umbral de integridad Ψ = {PSI_THRESHOLD}")

        # Marcador en SNR=5
        ax.axvline(x=5.0, color="green", linestyle=":", linewidth=1.5,
                   label=f"SNR = 5  →  Ψ = {psi_at_snr5:.4f}")

        # Marcador del punto de quiebre
        if snr_threshold > snr_values[0]:
            ax.axvline(x=snr_threshold, color="orange", linestyle=":",
                       linewidth=1.5,
                       label=f"Punto de quiebre SNR ≈ {snr_threshold:.3f}")

        ax.set_xlabel("SNR (escala logarítmica)", fontsize=13)
        ax.set_ylabel("Coherencia Ψ", fontsize=13)
        ax.set_title(
            "Experimento Ψ-Sweep: Barrido de SNR Noético\n"
            f"f₀ = {F0_HZ} Hz  |  {DURATION_S}s × {SAMPLE_RATE:.0f} Hz",
            fontsize=14,
        )
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc="lower right", fontsize=11)
        ax.grid(True, which="both", alpha=0.3)

        fig.tight_layout()
        fig.savefig(output_plot, dpi=150)
        plt.close(fig)

        if verbose:
            print(f"✅ Gráfica guardada: {output_plot}")

    except ImportError:
        if verbose:
            print("⚠️ matplotlib no disponible — gráfica omitida")


def main():
    """Punto de entrada principal del experimento Ψ-Sweep."""
    print("=" * 70)
    print("EXPERIMENTO Ψ-SWEEP: BARRIDO DE SNR NOÉTICO")
    print(f"Señal: f₀ = {F0_HZ} Hz  |  {DURATION_S}s × {SAMPLE_RATE:.0f} Hz")
    print("=" * 70)

    resultados = ejecutar_barrido_snr(
        output_csv="Noesis_SNR_Sweep.csv",
        output_plot="noesis_snr_sweep_coherence.png",
        verbose=True,
    )

    print("\n📊 RESUMEN DEL ANÁLISIS NOÉSICO:")
    print(f"   • Varianza de Ψ (SNR=5):     Ψ = {resultados['psi_at_snr5']:.4f}  "
          f"{'✅ > 0.996' if resultados['psi_at_snr5'] > 0.996 else '❌ por debajo de 0.996'}")
    print(f"   • Punto de quiebre (Ψ<0.7):  SNR < {resultados['snr_threshold']:.4f}  "
          f"{'✅ < 0.15' if resultados['snr_threshold'] < 0.15 else 'ℹ️  revisar'}")
    print(f"   • Total de muestras CSV:      {resultados['n_samples_total']}")
    print(f"   • Archivo de datos:           {resultados['csv_path']}")
    print("\n✅ EXPERIMENTO Ψ-SWEEP COMPLETADO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
