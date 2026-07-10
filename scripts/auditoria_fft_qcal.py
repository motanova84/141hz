#!/usr/bin/env python3
"""
Auditoría FFT QCAL - Verificación Espectral del Pico en f₀
===========================================================
Carga cualquier dataset de mediciones QCAL y aplica FFT a la serie
temporal de Ψ_emp para verificar la existencia de un pico de potencia
exclusivo en el armónico fundamental f₀ = 141.7001 Hz.

El análisis incluye:
  - Espectro de potencia mediante FFT
  - SNR en f₀ vs. banda de ruido lateral
  - Exportación del espectro como PNG y resumen en JSON
  - Bandera de sesgo: verifica que no existan otros picos dominantes

Uso:
  python auditoria_fft_qcal.py --input data/raw_metrology/qcal_raw_measurements_141_7001hz.csv
  python auditoria_fft_qcal.py --input mis_datos.csv --f_target 141.7001 --banda_hz 10
  python auditoria_fft_qcal.py --help

Diseñado para replicación independiente: todos los parámetros son
configurables; no se asume ninguna constante del modelo QCAL.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
log = logging.getLogger(__name__)

DEFAULT_F_TARGET = 141.7001
DEFAULT_BANDA_HZ = 15.0       # anchura de banda lateral para ruido de fondo
DEFAULT_SAMPLE_RATE = 1.0     # un sample por segundo (serie a 1 Hz)


# ============================================================
# ANÁLISIS ESPECTRAL
# ============================================================

def calcular_espectro(serie: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula el espectro de potencia unilateral de la serie temporal.

    Parámetros
    ----------
    serie : np.ndarray
        Serie temporal de Ψ_emp.
    sample_rate : float
        Frecuencia de muestreo en Hz.

    Retorna
    -------
    frecuencias : np.ndarray
        Vector de frecuencias positivas (Hz).
    potencia : np.ndarray
        Densidad espectral de potencia (unidades²/Hz).
    """
    n = len(serie)
    ventana = np.hanning(n)
    serie_ventana = (serie - serie.mean()) * ventana

    fft_vals = np.fft.rfft(serie_ventana)
    frecuencias = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    # Normalizar por la energía de la ventana
    potencia = (np.abs(fft_vals) ** 2) / (np.sum(ventana ** 2))
    return frecuencias, potencia


def snr_en_objetivo(
    frecuencias: np.ndarray,
    potencia: np.ndarray,
    f_target: float,
    banda_hz: float,
) -> dict:
    """
    Calcula el SNR del pico en f_target respecto al ruido de fondo lateral.

    Parámetros
    ----------
    frecuencias : np.ndarray
    potencia : np.ndarray
    f_target : float
        Frecuencia objetivo (Hz).
    banda_hz : float
        Anchura de la banda lateral para estimación del ruido de fondo.

    Retorna
    -------
    dict con claves:
        f_target, potencia_pico, frecuencia_pico_real,
        ruido_fondo_mediana, snr_lineal, snr_db,
        fraccion_potencia_total, pico_es_dominante
    """
    # Índice del bin más cercano a f_target
    idx_target = int(np.argmin(np.abs(frecuencias - f_target)))
    potencia_pico = float(potencia[idx_target])
    frecuencia_pico_real = float(frecuencias[idx_target])

    # Exclusion zone: use bin width (frequency_resolution) to avoid removing
    # too much or too little spectrum around the peak
    bin_width = float(frecuencias[1] - frecuencias[0]) if len(frecuencias) > 1 else 1.0
    exclusion_hz = max(bin_width, 1.0)  # at least 1 Hz, scales with resolution

    mask_banda = (
        (frecuencias >= f_target - banda_hz) &
        (frecuencias <= f_target + banda_hz) &
        (np.abs(frecuencias - f_target) > exclusion_hz)
    )
    if mask_banda.sum() == 0:
        ruido_fondo = float(np.median(potencia))
    else:
        ruido_fondo = float(np.median(potencia[mask_banda]))

    snr_lineal = potencia_pico / max(ruido_fondo, 1e-30)
    snr_db = float(10.0 * np.log10(snr_lineal)) if snr_lineal > 0 else -np.inf
    fraccion = potencia_pico / max(float(potencia.sum()), 1e-30)

    # El pico es dominante si su SNR supera 10 dB y el máximo global del
    # espectro cae dentro de ±1 bin (= resolución frecuencial) de f_target.
    # Esto evita fallos cuando la portadora cae entre dos bins contiguos.
    bin_width_snr = float(frecuencias[1] - frecuencias[0]) if len(frecuencias) > 1 else 1.0
    idx_global_max = int(np.argmax(potencia))
    freq_global_max = float(frecuencias[idx_global_max])
    pico_es_dominante = bool(
        snr_db >= 10.0 and abs(freq_global_max - f_target) <= bin_width_snr
    )

    return {
        "f_target_hz": f_target,
        "potencia_pico": potencia_pico,
        "frecuencia_pico_real_hz": frecuencia_pico_real,
        "desviacion_hz": abs(frecuencia_pico_real - f_target),
        "ruido_fondo_mediana": ruido_fondo,
        "snr_lineal": snr_lineal,
        "snr_db": snr_db,
        "fraccion_potencia_total": fraccion,
        "pico_es_dominante": pico_es_dominante,
    }


def pico_global(frecuencias: np.ndarray, potencia: np.ndarray) -> dict:
    """Identifica el bin de máxima potencia en todo el espectro."""
    idx_max = int(np.argmax(potencia))
    return {
        "frecuencia_hz": float(frecuencias[idx_max]),
        "potencia": float(potencia[idx_max]),
    }


# ============================================================
# VISUALIZACIÓN
# ============================================================

def guardar_espectro(
    frecuencias: np.ndarray,
    potencia: np.ndarray,
    f_target: float,
    ruta: Path,
    titulo: str = "Espectro de potencia – Ψ_emp",
) -> None:
    """Guarda el espectro de potencia como imagen PNG."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.semilogy(frecuencias, potencia, color="steelblue", linewidth=0.8, label="PSD")
        ax.axvline(f_target, color="crimson", linewidth=1.5,
                   linestyle="--", label=f"f₀ = {f_target} Hz")
        ax.set_xlabel("Frecuencia (Hz)")
        ax.set_ylabel("Potencia (u²/Hz)")
        ax.set_title(titulo)
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(ruta, dpi=150)
        plt.close(fig)
        log.info(f"✅ Espectro guardado: {ruta}")
    except ImportError:
        log.warning("matplotlib no disponible; se omite la imagen del espectro.")


# ============================================================
# CLI
# ============================================================

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Auditoría FFT QCAL – verifica el pico espectral en f₀.\n"
            "Carga un CSV de mediciones y exporta espectro (PNG) + resumen (JSON)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Ruta al CSV de mediciones (debe contener la columna psi_emp_calc).",
    )
    parser.add_argument(
        "--f_target",
        type=float,
        default=DEFAULT_F_TARGET,
        help=f"Frecuencia objetivo del pico esperado en Hz (default: {DEFAULT_F_TARGET}).",
    )
    parser.add_argument(
        "--sample_rate",
        type=float,
        default=DEFAULT_SAMPLE_RATE,
        help=f"Frecuencia de muestreo de la serie temporal en Hz (default: {DEFAULT_SAMPLE_RATE}).",
    )
    parser.add_argument(
        "--banda_hz",
        type=float,
        default=DEFAULT_BANDA_HZ,
        help=(
            f"Anchura de la banda lateral (Hz) para estimar el ruido de fondo "
            f"(default: {DEFAULT_BANDA_HZ})."
        ),
    )
    parser.add_argument(
        "--columna",
        type=str,
        default="psi_emp_calc",
        help="Nombre de la columna de la serie a analizar (default: psi_emp_calc).",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="",
        help=(
            "Directorio de salida para PNG y JSON. "
            "Si se omite, se usa el mismo directorio que el archivo de entrada."
        ),
    )
    parser.add_argument(
        "--sin_imagen",
        action="store_true",
        help="Omitir la exportación del PNG del espectro.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    ruta_entrada = Path(args.input)
    if not ruta_entrada.exists():
        log.error(f"Archivo no encontrado: {ruta_entrada}")
        return 1

    out_dir = Path(args.output_dir) if args.output_dir else ruta_entrada.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = ruta_entrada.stem

    log.info("=" * 60)
    log.info("AUDITORÍA FFT QCAL")
    log.info(f"  Entrada       : {ruta_entrada}")
    log.info(f"  Columna       : {args.columna}")
    log.info(f"  f_target      : {args.f_target} Hz")
    log.info(f"  Sample rate   : {args.sample_rate} Hz")
    log.info(f"  Banda ruido   : ±{args.banda_hz} Hz")
    log.info("=" * 60)

    # Cargar datos
    df = pd.read_csv(ruta_entrada)
    if args.columna not in df.columns:
        log.error(
            f"Columna '{args.columna}' no encontrada. "
            f"Columnas disponibles: {list(df.columns)}"
        )
        return 1

    serie = df[args.columna].dropna().to_numpy(dtype=float)
    n_puntos = len(serie)
    log.info(f"Serie cargada: {n_puntos} puntos")

    if n_puntos < 4:
        log.error("Serie demasiado corta para análisis FFT (mínimo 4 puntos).")
        return 1

    # Espectro
    frecuencias, potencia = calcular_espectro(serie, args.sample_rate)

    # SNR en f_target
    resultado_snr = snr_en_objetivo(frecuencias, potencia, args.f_target, args.banda_hz)
    pico_glob = pico_global(frecuencias, potencia)

    # Detección de discordancia: el máximo global debería coincidir con f_target.
    # Esto detecta si el pico más fuerte del espectro está lejos del objetivo,
    # lo cual indica que f_target no es el modo dominante del sistema.
    # Se usa la resolución frecuencial (bin width) como tolerancia mínima.
    bin_width_check = float(frecuencias[1] - frecuencias[0]) if len(frecuencias) > 1 else 1.0
    tolerancia_check = max(bin_width_check, args.banda_hz)
    pico_fuera_de_objetivo = abs(pico_glob["frecuencia_hz"] - args.f_target) > tolerancia_check

    resumen = {
        "archivo_entrada": str(ruta_entrada),
        "columna_analizada": args.columna,
        "n_puntos": n_puntos,
        "sample_rate_hz": args.sample_rate,
        "f_target_hz": args.f_target,
        "banda_ruido_hz": args.banda_hz,
        "resultado_pico_objetivo": resultado_snr,
        "pico_global_espectro": pico_glob,
        "pico_global_fuera_de_objetivo": pico_fuera_de_objetivo,
        "veredicto": (
            "PICO CONFIRMADO en f₀"
            if resultado_snr["pico_es_dominante"]
            else "PICO NO DOMINANTE – revisar datos o parámetros"
        ),
    }

    # Exportar JSON
    ruta_json = out_dir / f"{stem}_auditoria_fft.json"
    with open(ruta_json, "w", encoding="utf-8") as fp:
        json.dump(resumen, fp, ensure_ascii=False, indent=2)
    log.info(f"✅ Resumen JSON exportado: {ruta_json}")

    # Exportar PNG
    if not args.sin_imagen:
        ruta_png = out_dir / f"{stem}_espectro.png"
        titulo = f"PSD Ψ_emp – f₀={args.f_target} Hz | SNR={resultado_snr['snr_db']:.1f} dB"
        guardar_espectro(frecuencias, potencia, args.f_target, ruta_png, titulo)

    # Reporte en consola
    print("\n── Auditoría FFT QCAL ───────────────────────────────────────")
    print(f"  Archivo                : {ruta_entrada.name}")
    print(f"  Puntos analizados      : {n_puntos}")
    print(f"  f₀ objetivo            : {args.f_target} Hz")
    print(f"  Pico real en           : {resultado_snr['frecuencia_pico_real_hz']:.6f} Hz")
    print(f"  Desviación             : {resultado_snr['desviacion_hz']:.6e} Hz")
    print(f"  SNR                    : {resultado_snr['snr_db']:.2f} dB")
    print(f"  Fracción potencia      : {resultado_snr['fraccion_potencia_total']:.4f}")
    print(f"  Pico dominante         : {resultado_snr['pico_es_dominante']}")
    print(f"  Pico global en         : {pico_glob['frecuencia_hz']:.6f} Hz")
    print(f"  Pico fuera de objetivo : {pico_fuera_de_objetivo}")
    print(f"\n  ▶ VEREDICTO: {resumen['veredicto']}")
    print("─────────────────────────────────────────────────────────────\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
