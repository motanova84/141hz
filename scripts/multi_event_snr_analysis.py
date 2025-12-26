#!/usr/bin/env python3
"""
Análisis Multi-evento de SNR en 141.7 Hz
=========================================

Este script analiza múltiples eventos de ondas gravitacionales para detectar
señales consistentes en la banda de frecuencia de 141.7 Hz.

El análisis incluye:
- Descarga de datos de H1 y L1 desde GWOSC
- Filtrado de banda pasante alrededor de 141.7 Hz (140.7-142.7 Hz)
- Cálculo de SNR (Signal-to-Noise Ratio)
- Generación de resultados en JSON
- Visualización comparativa entre detectores

Eventos analizados: GW150914, GW151012, GW151226, GW170104, GW170608,
                   GW170729, GW170809, GW170814, GW170817, GW170818, GW170823, GW200129_065458
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
    "GW150914": [1126259462, 1126259494],
    "GW151012": [1128678900, 1128678932],
    "GW151226": [1135136350, 1135136382],
    "GW170104": [1167559936, 1167559968],
    "GW170608": [1180922440, 1180922472],
    "GW170729": [1185389806, 1185389838],
    "GW170809": [1186302508, 1186302540],
    "GW170814": [1186741850, 1186741882],
    "GW170817": [1187008882, 1187008914],
    "GW170818": [1187058327, 1187058359],
    "GW170823": [1187529256, 1187529288],
    "GW200129_065458": [1264316100, 1264316132],
}

snr_threshold = 5.0
target_band = [140.7, 142.7]
target_freq = 141.7


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


def analyze_event(name, start, end, band):
    """
    Analiza un evento gravitacional individual.
    
    Args:
        name: Nombre del evento (e.g., 'GW150914')
        start: Tiempo GPS de inicio
        end: Tiempo GPS de fin
        band: Lista con [freq_min, freq_max] para el filtro
    
    Returns:
        dict: Resultados del análisis con SNR de H1 y L1, o error
    """
    try:
        h1 = TimeSeries.fetch_open_data('H1', start, end, cache=True)
        l1 = TimeSeries.fetch_open_data('L1', start, end, cache=True)

        snr_h1 = calculate_snr(h1, band)
        snr_l1 = calculate_snr(l1, band)

        return {"H1": snr_h1, "L1": snr_l1}
    except Exception as e:
        return {"error": str(e)}


def main():
    """
    Ejecuta el análisis multi-evento completo.
    """
    print("=" * 70)
    print("🌌 ANÁLISIS MULTI-EVENTO DE SNR EN 141.7 Hz")
    print("=" * 70)
    print()
    print(f"Banda de frecuencia: {target_band[0]}-{target_band[1]} Hz")
    print(f"Frecuencia objetivo: {target_freq} Hz")
    print(f"Umbral de SNR: {snr_threshold}")
    print(f"Eventos a analizar: {len(events)}")
    print()

    results = {}
    snr_h1 = []
    snr_l1 = []
    labels = []

    # ===============================
    # BUCLE DE ANÁLISIS
    # ===============================
    for i, (name, (start, end)) in enumerate(events.items(), 1):
        print(f"[{i}/{len(events)}] ⏳ Analizando {name}...")
        
        result = analyze_event(name, start, end, target_band)
        results[name] = result
        
        if "error" not in result:
            snr_h1.append(result["H1"])
            snr_l1.append(result["L1"])
            labels.append(name)
            print(f"         ✅ H1 SNR = {result['H1']:.2f}, L1 SNR = {result['L1']:.2f}")
        else:
            print(f"         ⚠️ Error: {result['error']}")
        print()

    # ===============================
    # GUARDAR RESULTADOS
    # ===============================
    output_json = "multi_event_results.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Resultados guardados en: {output_json}")

    # ===============================
    # VISUALIZAR RESULTADOS
    # ===============================
    if len(labels) > 0:
        x = np.arange(len(labels))
        plt.figure(figsize=(12, 6))
        plt.bar(x - 0.15, snr_h1, width=0.3, label="H1")
        plt.bar(x + 0.15, snr_l1, width=0.3, label="L1")
        plt.axhline(snr_threshold, color='r', linestyle='--', label=f'SNR={snr_threshold}')
        plt.xticks(x, labels, rotation=45)
        plt.ylabel("SNR @ 141.7 Hz")
        plt.title(f"SNR por Evento (H1 vs L1) — Banda {target_freq} Hz")
        plt.legend()
        plt.tight_layout()
        
        output_png = "multi_event_analysis.png"
        plt.savefig(output_png)
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
        print(f"H1 SNR - Media: {np.mean(snr_h1):.2f}, Desv. Est: {np.std(snr_h1):.2f}")
        print(f"L1 SNR - Media: {np.mean(snr_l1):.2f}, Desv. Est: {np.std(snr_l1):.2f}")
        
        # Contar eventos sobre umbral
        h1_above = sum(1 for s in snr_h1 if s >= snr_threshold)
        l1_above = sum(1 for s in snr_l1 if s >= snr_threshold)
        print()
        print(f"Eventos con SNR ≥ {snr_threshold}:")
        print(f"  H1: {h1_above}/{len(labels)} ({100*h1_above/len(labels):.1f}%)")
        print(f"  L1: {l1_above}/{len(labels)} ({100*l1_above/len(labels):.1f}%)")

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
