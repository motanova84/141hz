#!/usr/bin/env python3
"""
Demostración del Análisis Multi-evento de SNR
==============================================

Este script demuestra el funcionamiento del análisis multi-evento de SNR
usando datos sintéticos, sin requerir conectividad a GWOSC.

Genera señales simuladas de ondas gravitacionales con:
- Frecuencia objetivo de 141.7 Hz
- Ruido gaussiano
- SNR variables para diferentes "eventos"
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os

# Simular la estructura de eventos del script real
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
}

snr_threshold = 5.0
target_freq = 141.7


def generate_synthetic_signal(duration=32, sample_rate=4096, target_freq=141.7, snr_target=10.0):
    """
    Genera una señal sintética de onda gravitacional.
    
    Args:
        duration: Duración en segundos
        sample_rate: Tasa de muestreo en Hz
        target_freq: Frecuencia objetivo en Hz
        snr_target: SNR objetivo de la señal
    
    Returns:
        tuple: (tiempo, señal) - Arrays numpy con tiempo y señal
    """
    n_samples = duration * sample_rate
    t = np.linspace(0, duration, n_samples)
    
    # Generar señal sinusoidal con frecuencia objetivo
    # Simular un "chirp" simplificado con amplitud decreciente
    amplitude = np.exp(-t / 10) * 0.1  # Decaimiento exponencial
    signal = amplitude * np.sin(2 * np.pi * target_freq * t)
    
    # Agregar ruido gaussiano
    noise_std = np.std(signal) / snr_target
    noise = np.random.normal(0, noise_std, n_samples)
    
    data = signal + noise
    
    return t, data


def calculate_synthetic_snr(data):
    """
    Calcula el SNR de una señal sintética.
    Similar al método usado en el script real.
    
    Args:
        data: Array numpy con la señal
    
    Returns:
        float: Valor de SNR
    """
    snr = np.max(np.abs(data)) / np.std(data)
    return snr


def main():
    """
    Ejecuta la demostración del análisis multi-evento.
    """
    print("=" * 70)
    print("🎬 DEMOSTRACIÓN: Análisis Multi-evento de SNR en 141.7 Hz")
    print("=" * 70)
    print()
    print("⚠️  NOTA: Esta es una demostración con datos sintéticos")
    print("    Para análisis con datos reales, ejecutar:")
    print("    make multi-event-snr")
    print()
    print(f"Frecuencia objetivo: {target_freq} Hz")
    print(f"Umbral de SNR: {snr_threshold}")
    print(f"Eventos a simular: {len(events)}")
    print()

    # Fijar semilla para reproducibilidad
    np.random.seed(42)

    results = {}
    snr_h1 = []
    snr_l1 = []
    labels = []

    # Simular análisis de cada evento
    for i, (name, (start, end)) in enumerate(events.items(), 1):
        print(f"[{i}/{len(events)}] ⏳ Simulando {name}...")
        
        # Generar SNR sintéticos con variación realista
        # SNR típicos varían entre 5 y 15
        base_snr_h1 = 7.0 + (i % 5) * 1.5 + np.random.uniform(-1, 1)
        base_snr_l1 = 6.5 + (i % 5) * 1.3 + np.random.uniform(-1, 1)
        
        # Generar señales sintéticas
        _, signal_h1 = generate_synthetic_signal(snr_target=base_snr_h1)
        _, signal_l1 = generate_synthetic_signal(snr_target=base_snr_l1)
        
        # Calcular SNR
        snr1 = calculate_synthetic_snr(signal_h1)
        snr2 = calculate_synthetic_snr(signal_l1)
        
        results[name] = {"H1": snr1, "L1": snr2}
        snr_h1.append(snr1)
        snr_l1.append(snr2)
        labels.append(name)
        
        print(f"         ✅ H1 SNR = {snr1:.2f}, L1 SNR = {snr2:.2f}")

    print()

    # Guardar resultados
    output_json = "demo_multi_event_results.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Resultados guardados en: {output_json}")

    # Crear visualización
    x = np.arange(len(labels))
    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.15, snr_h1, width=0.3, label="H1", alpha=0.8, color='steelblue')
    plt.bar(x + 0.15, snr_l1, width=0.3, label="L1", alpha=0.8, color='coral')
    plt.axhline(snr_threshold, color='r', linestyle='--', linewidth=2, label=f'SNR={snr_threshold}')
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.ylabel("SNR @ 141.7 Hz", fontsize=12)
    plt.title(f"SNR por Evento (H1 vs L1) — Banda {target_freq} Hz\n(Datos Sintéticos - Demostración)", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    output_png = "demo_multi_event_analysis.png"
    plt.savefig(output_png, dpi=150)
    print(f"📊 Visualización guardada en: {output_png}")

    # No mostrar en entorno no interactivo
    if os.environ.get('DISPLAY'):
        plt.show()

    # Resumen estadístico
    print()
    print("=" * 70)
    print("📊 RESUMEN ESTADÍSTICO")
    print("=" * 70)
    print(f"Eventos simulados: {len(labels)}/{len(events)}")
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
    print("✅ Demostración completada. Archivos generados:")
    print(f"  - {output_json}")
    print(f"  - {output_png}")
    print()
    print("💡 Para análisis con datos reales de GWOSC:")
    print("   python3 scripts/multi_event_snr_analysis.py")
    print("   o")
    print("   make multi-event-snr")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
