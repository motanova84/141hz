#!/usr/bin/env python3
"""
Análisis de SNR esperada para GW200129 a 141.7 Hz

Este script calcula la relación señal-ruido (SNR) esperada para el evento
GW200129_065458 en la frecuencia objetivo de 141.7 Hz, utilizando los
factores efectivos angulares obtenidos por QCAL para cada detector.

Configuración:
- Evento: GW200129_065458
- GPS Time: 1264316116.4
- Frecuencia objetivo: 141.7 Hz
- Detectores: H1, L1, V1
- h_rss supuesto: 1e-22

Factores efectivos QCAL a 141.7 Hz:
- H1: 0.2140
- L1: 0.3281
- V1: 0.8669

Requiere:
    - pycbc >= 2.0.0
    - gwpy >= 3.0.0
    - numpy >= 1.21.0
    - matplotlib >= 3.5.0

Uso:
    python scripts/analizar_gw200129_snr.py

Salida:
    - Imprime SNR esperada para cada detector
    - Opcionalmente guarda resultados en results/gw200129_snr_analysis.json
"""

import os
import sys
import json
import numpy as np

# Verificar que las librerías necesarias están disponibles
try:
    from gwpy.timeseries import TimeSeries as GWTimeSeries
except ImportError:
    print("❌ Error: gwpy no está instalado")
    print("   Instalar con: pip install gwpy")
    sys.exit(1)


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

EVENT_NAME = "GW200129_065458"
EVENT_TIME = 1264316116.4  # GPS del evento GW200129
F0 = 141.7                 # Frecuencia objetivo en Hz
H_RSS = 1e-22              # Supuesto h_rss de la señal
IFO_LIST = ['H1', 'L1', 'V1']  # Detectores a evaluar

# Factores efectivos angulares obtenidos por QCAL a 141.7 Hz
EFF_FACTORS = {
    'H1': 0.2140,
    'L1': 0.3281,
    'V1': 0.8669,
}


# ============================================================================
# FUNCIONES
# ============================================================================

def get_psd(detector, gps_time, duration=32, fftlength=4, delta_f=1.0/4):
    """
    Obtiene el PSD (Power Spectral Density) para un detector en un tiempo dado.

    Args:
        detector (str): Nombre del detector ('H1', 'L1', 'V1')
        gps_time (float): Tiempo GPS del evento
        duration (int): Duración de la ventana de datos en segundos (default: 32)
        fftlength (int): Longitud de FFT en segundos (default: 4)
        delta_f (float): Resolución en frecuencia (default: 1/4 Hz)

    Returns:
        FrequencySeries: PSD del detector, o None si hay error
    """
    try:
        # Descargar datos alrededor del evento
        start_time = gps_time - duration // 2
        end_time = gps_time + duration // 2

        print(f"   Descargando datos de {detector} [{start_time} - {end_time}]...")
        strain = GWTimeSeries.fetch_open_data(
            detector,
            start_time,
            end_time,
            cache=True
        )

        # Remuestrear a 4096 Hz
        print("   Remuestreando a 4096 Hz...")
        strain = strain.resample(4096)

        # Calcular PSD
        print(f"   Calculando PSD (fftlength={fftlength}s)...")
        psd = strain.psd(fftlength=fftlength, overlap=2, window='hann')

        # Interpolar PSD
        print("   Interpolando PSD (delta_f={} Hz)...".format(delta_f))
        psd = psd.interpolate(delta_f)

        return psd

    except Exception as e:
        print(f"   ❌ Error al obtener PSD de {detector}: {e}")
        return None


def calculate_snr(F_eff, h_rss, Sn_f0):
    """
    Calcula la SNR esperada usando la fórmula:
    SNR = (F_eff * h_rss) / sqrt(Sn(f0))

    Args:
        F_eff (float): Factor efectivo angular del detector
        h_rss (float): Amplitud de la señal (h_rss)
        Sn_f0 (float): PSD en la frecuencia objetivo

    Returns:
        float: SNR calculada
    """
    return (F_eff * h_rss) / np.sqrt(Sn_f0)


def main():
    """Función principal que ejecuta el análisis de SNR para GW200129"""

    print("=" * 70)
    print(f"🌌 Análisis de SNR esperada para {EVENT_NAME}")
    print("=" * 70)
    print(f"📍 GPS Time: {EVENT_TIME}")
    print(f"📍 Frecuencia objetivo: {F0} Hz")
    print(f"📍 h_rss supuesto: {H_RSS}")
    print(f"📍 Detectores: {', '.join(IFO_LIST)}")
    print("=" * 70)

    # Crear directorio de salida si no existe
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)

    # Diccionario para almacenar resultados
    results = {}

    # Procesar cada detector
    for ifo in IFO_LIST:
        print(f"\n🔬 Procesando detector {ifo}...")
        print("-" * 70)

        F_eff = EFF_FACTORS[ifo]
        print(f"   Factor efectivo QCAL (F_eff): {F_eff}")

        # Obtener PSD
        psd = get_psd(ifo, EVENT_TIME)

        if psd is None:
            print(f"   ⚠️  No se pudo obtener PSD para {ifo}")
            results[ifo] = {
                'F_eff': F_eff,
                'Sn_f0': None,
                'SNR': None,
                'error': 'No se pudo obtener PSD'
            }
            continue

        # Interpolar PSD en f0
        try:
            Sn_f0 = psd.value_at(F0)
            print(f"   PSD en {F0} Hz: {Sn_f0:.2e} Hz⁻¹")

            # Calcular SNR
            snr = calculate_snr(F_eff, H_RSS, Sn_f0)
            print(f"   ✅ SNR esperada a {F0} Hz en {ifo}: {snr:.2f}")

            # Almacenar resultados
            results[ifo] = {
                'F_eff': F_eff,
                'Sn_f0': float(Sn_f0),
                'SNR': float(snr),
                'error': None
            }

        except Exception as e:
            print(f"   ❌ Error calculando SNR para {ifo}: {e}")
            results[ifo] = {
                'F_eff': F_eff,
                'Sn_f0': None,
                'SNR': None,
                'error': str(e)
            }

    # Resumen de resultados
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)

    successful_detections = []
    for ifo, data in results.items():
        if data['SNR'] is not None:
            print(f"{ifo}: SNR = {data['SNR']:.2f}")
            successful_detections.append(data['SNR'])
        else:
            print(f"{ifo}: {data['error']}")

    if successful_detections:
        print(f"\nSNR promedio: {np.mean(successful_detections):.2f}")
        print(f"SNR máxima: {np.max(successful_detections):.2f}")
        print(f"SNR mínima: {np.min(successful_detections):.2f}")

    # Guardar resultados en JSON
    output_file = os.path.join(output_dir, 'gw200129_snr_analysis.json')
    output_data = {
        'event': EVENT_NAME,
        'gps_time': EVENT_TIME,
        'frequency': F0,
        'h_rss': H_RSS,
        'results': results
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n📁 Resultados guardados en: {output_file}")
    print("=" * 70)

    return results


if __name__ == '__main__':
    try:
        results = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
