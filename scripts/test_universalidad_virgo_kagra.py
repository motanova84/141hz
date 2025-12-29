#!/usr/bin/env python3
"""
Test de Universalidad de 141.7 Hz en Virgo y KAGRA
===================================================

Este script analiza múltiples eventos de ondas gravitacionales para detectar
señales consistentes en la banda de frecuencia de 141.7 Hz usando los
detectores Virgo (V1) y KAGRA (K1).

El análisis incluye:
- Descarga de datos de V1 (y K1 cuando esté disponible) desde GWOSC
- Filtrado de banda pasante alrededor de 141.7 Hz (141.4-142.0 Hz)
- Cálculo de SNR (Signal-to-Noise Ratio)
- Generación de resultados en JSON
- Visualización comparativa

Eventos analizados: GW170814, GW170817, GW170818, GW170823

Nota: KAGRA (K1) comenzó operaciones en 2020, por lo que no hay datos
disponibles para estos eventos de 2017. El script está preparado para
incluir K1 cuando se analicen eventos posteriores a 2020.
"""

from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import json
import numpy as np
import sys
import os


# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
events = {
    "GW170814": [1186741850, 1186741882],
    "GW170817": [1187008882, 1187008914],
    "GW170818": [1187058327, 1187058359],
    "GW170823": [1187529256, 1187529288],
}

target_band = [141.4, 142.0]
target_freq = 141.7
snr_threshold = 5.0


def calculate_snr(data, band):
    """
    Calcula el SNR (Signal-to-Noise Ratio) de una serie temporal.

    Args:
        data: TimeSeries de gwpy
        band: Lista con [freq_min, freq_max] para el filtro de banda

    Returns:
        float: Valor de SNR calculado como max(abs(señal)) / std(señal)
    """
    data_band = data.bandpass(*band)
    snr = np.max(np.abs(data_band.value)) / np.std(data_band.value)
    return snr


def analyze_event_virgo(name, start, end, band):
    """
    Analiza un evento gravitacional para el detector Virgo (V1).

    Args:
        name: Nombre del evento (e.g., 'GW170814')
        start: Tiempo GPS de inicio
        end: Tiempo GPS de fin
        band: Lista con [freq_min, freq_max] para el filtro

    Returns:
        dict: Resultados del análisis con SNR de V1, o error
    """
    try:
        v1 = TimeSeries.fetch_open_data('V1', start, end, cache=True)
        snr_v1 = calculate_snr(v1, band)
        return {"V1": snr_v1}
    except Exception as e:
        return {"error": str(e)}


def analyze_event_kagra(name, start, end, band):
    """
    Analiza un evento gravitacional para el detector KAGRA (K1).

    Args:
        name: Nombre del evento (e.g., 'GW200105')
        start: Tiempo GPS de inicio
        end: Tiempo GPS de fin
        band: Lista con [freq_min, freq_max] para el filtro

    Returns:
        dict: Resultados del análisis con SNR de K1, o error
    """
    try:
        k1 = TimeSeries.fetch_open_data('K1', start, end, cache=True)
        snr_k1 = calculate_snr(k1, band)
        return {"K1": snr_k1}
    except Exception as e:
        return {"error": str(e)}


def main():
    """
    Ejecuta el análisis de universalidad completo.
    """
    print("=" * 70)
    print("🌌 TEST DE UNIVERSALIDAD: 141.7 Hz en Virgo y KAGRA")
    print("=" * 70)
    print()
    print(f"Banda de frecuencia: {target_band[0]}-{target_band[1]} Hz")
    print(f"Frecuencia objetivo: {target_freq} Hz")
    print(f"Umbral de SNR: {snr_threshold}")
    print(f"Eventos a analizar: {len(events)}")
    print()

    results = {}
    snr_v1 = []
    labels = []

    # ===============================
    # BUCLE DE ANÁLISIS - VIRGO
    # ===============================
    print("🔍 Analizando Virgo (V1)...")
    print("-" * 70)

    for i, (name, (start, end)) in enumerate(events.items(), 1):
        print(f"[{i}/{len(events)}] ⏳ Analizando {name} (Virgo)...")

        result = analyze_event_virgo(name, start, end, target_band)
        results[name] = {"V1": result}

        if "error" not in result:
            snr_v1.append(result["V1"])
            labels.append(name)
            print(f"         ✅ Virgo SNR @{target_freq} Hz = {result['V1']:.2f}")
        else:
            print(f"         ⚠️ Error en {name}: {result['error']}")
        print()

    # ===============================
    # ANÁLISIS OPCIONAL - KAGRA
    # ===============================
    # Nota: KAGRA comenzó operaciones en 2020, estos eventos son de 2017
    print()
    print("🔍 Verificando disponibilidad de KAGRA (K1)...")
    print("-" * 70)
    print("⚠️  KAGRA no estaba operacional durante estos eventos (2017)")
    print("    KAGRA comenzó observaciones en 2020")
    print("    Para eventos posteriores a 2020, incluir análisis K1")
    print()

    # ===============================
    # GUARDAR RESULTADOS
    # ===============================
    output_json = "universalidad_virgo_kagra_results.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Resultados guardados en: {output_json}")

    # ===============================
    # VISUALIZAR RESULTADOS
    # ===============================
    if len(labels) > 0:
        plt.figure(figsize=(8, 5))
        plt.bar(labels, snr_v1, color='gold')
        plt.axhline(snr_threshold, color='red', linestyle='--',
                    label=f'SNR={snr_threshold}')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("SNR (Virgo)")
        plt.title("141.7 Hz Detection Test – Virgo (V1)")
        plt.legend()
        plt.tight_layout()

        output_png = "universalidad_virgo_kagra.png"
        plt.savefig(output_png, dpi=150)
        print(f"📊 Visualización guardada en: {output_png}")

        # No usar plt.show() en modo no interactivo
        if os.environ.get('DISPLAY'):
            plt.show()
    else:
        print("⚠️ No se pudo generar visualización (sin datos exitosos)")

    # ===============================
    # RESUMEN ESTADÍSTICO
    # ===============================
    print()
    print("=" * 70)
    print("📊 RESUMEN ESTADÍSTICO")
    print("=" * 70)
    print(f"Eventos analizados exitosamente: {len(labels)}/{len(events)}")

    if len(labels) > 0:
        print()
        print(f"Virgo (V1) SNR - Media: {np.mean(snr_v1):.2f}, "
              f"Desv. Est: {np.std(snr_v1):.2f}")

        # Contar eventos sobre umbral
        v1_above = sum(1 for s in snr_v1 if s >= snr_threshold)
        print()
        print(f"Eventos con SNR ≥ {snr_threshold}:")
        print(f"  Virgo (V1): {v1_above}/{len(labels)} "
              f"({100 * v1_above / len(labels):.1f}%)")

        print()
        print("Resultados finales (V1):")
        for name, snr_val in zip(labels, snr_v1):
            print(f"  {name}: {snr_val:.2f}")

    print()
    print("=" * 70)
    print("✅ Análisis completado. Archivos generados:")
    print(f"  - {output_json}")
    if len(labels) > 0:
        print(f"  - {output_png}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
