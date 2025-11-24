#!/usr/bin/env python3
"""
Análisis de datos IGETS para detección de 141.7 Hz

Este script descarga y analiza datos de gravímetros terrestres del servicio
IGETS (International Geodynamics and Earth Tide Service) buscando la señal
característica a 141.7 Hz predicha por la teoría Noésica de Gravedad Cuántica.

Procedimiento:
1. Descarga archivo IGETS en formato texto comprimido (.gz)
2. Descomprime y parsea los datos (tiempo, gravedad en µGal)
3. Calcula frecuencia de muestreo
4. Filtra tendencias lentas
5. Análisis espectral mediante método de Welch
6. Visualización de la banda 120-160 Hz
7. Cálculo de SNR (Signal-to-Noise Ratio)

Referencia:
- IGETS: https://isdcftp.gfz-potsdam.de/igets/
- Predicción teórica: PAPER.md sección 7.2.2
"""

import urllib.request
import gzip
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
import os
import argparse


def descargar_datos_igets(url, fname):
    """
    Descarga archivo IGETS desde GFZ Potsdam.

    Args:
        url (str): URL del archivo IGETS
        fname (str): Nombre del archivo local

    Returns:
        str: Ruta al archivo descargado
    """
    print(f"[INFO] Descargando datos IGETS desde: {url}")
    urllib.request.urlretrieve(url, fname)
    print(f"[OK] Archivo IGETS descargado: {fname}")
    return fname


def descomprimir_archivo(fname_gz, fname_txt):
    """
    Descomprime archivo .gz

    Args:
        fname_gz (str): Archivo comprimido
        fname_txt (str): Archivo destino

    Returns:
        str: Ruta al archivo descomprimido
    """
    print(f"[INFO] Descomprimiendo {fname_gz}...")
    with gzip.open(fname_gz, 'rb') as f_in:
        with open(fname_txt, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"[OK] Archivo descomprimido: {fname_txt}")
    return fname_txt


def leer_datos_gravimetro(fname_txt):
    """
    Lee datos del gravímetro (tiempo, gravedad).

    Args:
        fname_txt (str): Archivo de texto con datos

    Returns:
        tuple: (tiempo, gravedad, frecuencia_muestreo)
    """
    print(f"[INFO] Leyendo datos de {fname_txt}...")
    data = np.loadtxt(fname_txt)
    t = data[:, 0]  # segundos desde inicio
    g = data[:, 1]  # gravedad [µGal]

    # Calcular frecuencia de muestreo
    dt = np.median(np.diff(t))
    fs = 1.0 / dt

    print(f"[INFO] Frecuencia de muestreo: {fs:.3f} Hz")
    print(f"[INFO] Número de puntos: {len(g)}")
    print(f"[INFO] Duración: {t[-1] - t[0]:.2f} segundos")

    return t, g, fs


def filtrar_tendencia(g):
    """
    Elimina tendencia lenta (valor medio).

    Args:
        g (array): Serie temporal de gravedad

    Returns:
        array: Datos filtrados
    """
    print("[INFO] Filtrando tendencia lenta...")
    g_filtered = g - np.mean(g)
    return g_filtered


def analisis_espectral(g, fs, nperseg=8192):
    """
    Análisis espectral usando método de Welch.

    Args:
        g (array): Serie temporal de gravedad
        fs (float): Frecuencia de muestreo [Hz]
        nperseg (int): Longitud de segmento para Welch

    Returns:
        tuple: (frecuencias, densidad_espectral_potencia)
    """
    print(f"[INFO] Realizando análisis espectral (Welch, nperseg={nperseg})...")
    f, Pxx = welch(g, fs, nperseg=nperseg, scaling='density')
    return f, Pxx


def calcular_snr(f, Pxx, f_signal=141.7, signal_bandwidth=1.0,
                 noise_band_low=130, noise_band_high=140):
    """
    Calcula la relación señal-ruido (SNR).

    Args:
        f (array): Frecuencias
        Pxx (array): Densidad espectral de potencia
        f_signal (float): Frecuencia central de la señal [Hz]
        signal_bandwidth (float): Ancho de banda de la señal [Hz]
        noise_band_low (float): Límite inferior banda de ruido [Hz]
        noise_band_high (float): Límite superior banda de ruido [Hz]

    Returns:
        float: SNR
    """
    # Banda de señal
    signal_band = (f > f_signal - signal_bandwidth/2) & \
                  (f < f_signal + signal_bandwidth/2)

    # Banda de ruido
    noise_band = (f > noise_band_low) & (f < noise_band_high)

    # Calcular SNR
    signal_power = np.mean(Pxx[signal_band])
    noise_power = np.mean(Pxx[noise_band])
    snr = signal_power / noise_power

    print(f"[INFO] Potencia señal (banda {f_signal-signal_bandwidth/2:.1f}-"
          f"{f_signal+signal_bandwidth/2:.1f} Hz): {signal_power:.2e} µGal²/Hz")
    print(f"[INFO] Potencia ruido (banda {noise_band_low}-{noise_band_high} Hz): "
          f"{noise_power:.2e} µGal²/Hz")

    return snr


def visualizar_espectro(f, Pxx, f_signal=141.7,
                        band_low=120, band_high=160,
                        output_file='igets_spectrum_141hz.png'):
    """
    Visualiza el espectro en la banda de interés.

    Args:
        f (array): Frecuencias
        Pxx (array): Densidad espectral de potencia
        f_signal (float): Frecuencia de la señal [Hz]
        band_low (float): Límite inferior de visualización [Hz]
        band_high (float): Límite superior de visualización [Hz]
        output_file (str): Nombre del archivo de salida
    """
    # Seleccionar banda de interés
    band = (f > band_low) & (f < band_high)

    plt.figure(figsize=(9, 4))
    plt.semilogy(f[band], Pxx[band])
    plt.axvline(f_signal, color='r', linestyle='--',
                label=f'{f_signal} Hz (predicción teórica)')
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("PSD [µGal²/Hz]")
    plt.legend()
    plt.title(f"IGETS Gravímetro – Espectro {band_low}–{band_high} Hz")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_file, dpi=150)
    print(f"[OK] Espectro guardado en: {output_file}")

    # También mostrar si es interactivo
    if os.environ.get('DISPLAY'):
        plt.show()
    plt.close()


def main():
    """Función principal del análisis IGETS."""
    parser = argparse.ArgumentParser(
        description='Analizar datos IGETS para detección de 141.7 Hz'
    )
    parser.add_argument(
        '--url',
        default='https://isdcftp.gfz-potsdam.de/igets/level1/CA/'
                'CA_L1_20200101_20200131.txt.gz',
        help='URL del archivo IGETS'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directorio para archivos de salida'
    )
    parser.add_argument(
        '--nperseg',
        type=int,
        default=8192,
        help='Longitud de segmento para Welch'
    )
    parser.add_argument(
        '--freq-target',
        type=float,
        default=141.7,
        help='Frecuencia objetivo [Hz]'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("ANÁLISIS IGETS - DETECCIÓN 141.7 Hz")
    print("=" * 70)
    print(f"Frecuencia objetivo: {args.freq_target} Hz")
    print(f"URL: {args.url}")
    print("=" * 70)

    # Nombres de archivos
    fname_gz = os.path.join(args.output_dir,
                            os.path.basename(args.url))
    fname_txt = fname_gz.replace('.gz', '')

    # 1. Descargar datos
    descargar_datos_igets(args.url, fname_gz)

    # 2. Descomprimir
    descomprimir_archivo(fname_gz, fname_txt)

    # 3. Leer datos
    t, g, fs = leer_datos_gravimetro(fname_txt)

    # 4. Filtrar tendencia
    g_filtered = filtrar_tendencia(g)

    # 5. Análisis espectral
    f, Pxx = analisis_espectral(g_filtered, fs, nperseg=args.nperseg)

    # 6. Visualizar
    output_plot = os.path.join(args.output_dir, 'igets_spectrum_141hz.png')
    visualizar_espectro(f, Pxx, f_signal=args.freq_target,
                        output_file=output_plot)

    # 7. Calcular SNR
    snr = calcular_snr(f, Pxx, f_signal=args.freq_target)

    print("=" * 70)
    print(f"[RESULTADO] SNR ≈ {snr:.2f}")
    print("=" * 70)

    # Limpiar archivos temporales si se desea
    # os.remove(fname_gz)
    # os.remove(fname_txt)

    return snr


if __name__ == "__main__":
    main()
