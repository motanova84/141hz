#!/usr/bin/env python3
"""
Análisis ASD (Amplitude Spectral Density) en 141.7 Hz para GW150914
Incluye controles de validación y comparación con ruido de fondo
"""
from gwpy.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def analyze_asd_141hz():
    """
    Analiza la ASD en 141.7 Hz con controles de validación

    Returns:
        dict: Resultados del análisis incluyendo SNR, frecuencia detectada, etc.
    """
    output_dir = '../results/figures'
    os.makedirs(output_dir, exist_ok=True)

    archivo_h1 = '../data/raw/H1-GW150914-32s.hdf5'

    print("🔍 Análisis ASD en 141.7 Hz para GW150914")
    print("=" * 60)

    if not os.path.exists(archivo_h1):
        print(f"❌ Error: No se encuentra el archivo {archivo_h1}")
        print("   Ejecute primero: python scripts/descargar_datos.py")
        return None

    try:
        # Cargar datos de H1
        print("⏳ Cargando datos de Hanford (H1)...")
        data = TimeSeries.read(archivo_h1)
        print(f"✅ Datos cargados: {len(data)} muestras a {data.sample_rate} Hz")

        # Tiempo del merger (1126259462.423 GPS)
        merger_time = 1126259462.423
        merger_index = int((merger_time - data.t0.value) * data.sample_rate.value)

        # Segmento del ringdown (primeros 50 ms post-merger)
        ringdown_start = merger_index
        ringdown_end = merger_index + int(0.05 * data.sample_rate.value)
        ringdown = data[ringdown_start:ringdown_end]

        # Segmento de control (antes del merger, mismo tamaño)
        control_start = merger_index - len(ringdown) - 1000
        control_end = merger_index - 1000
        control = data[control_start:control_end]

        print(f"   Ringdown: {len(ringdown)} muestras ({len(ringdown)/data.sample_rate.value*1000:.1f} ms)")
        print(f"   Control: {len(control)} muestras (ruido de fondo)")

        # Calcular ASD para ambos segmentos
        print("\n📊 Calculando ASD (Amplitude Spectral Density)...")
        asd_ringdown = ringdown.asd(fftlength=0.01, overlap=0.005)
        asd_control = control.asd(fftlength=0.01, overlap=0.005)

        # Frecuencia objetivo
        target_freq = 141.7

        # Análisis del ringdown
        freq_idx = np.argmin(np.abs(asd_ringdown.frequencies.value - target_freq))
        detected_freq = asd_ringdown.frequencies.value[freq_idx]
        asd_ringdown_value = asd_ringdown.value[freq_idx]

        # Análisis del control
        asd_control_value = asd_control.value[freq_idx]

        # Calcular SNR en banda estrecha
        freq_mask = (asd_ringdown.frequencies.value >= 130) & (asd_ringdown.frequencies.value <= 160)
        # Excluir banda ±1 Hz alrededor de la frecuencia objetivo para estimar el ruido de fondo
        noise_mask = freq_mask & ((asd_ringdown.frequencies.value < target_freq - 1) | (asd_ringdown.frequencies.value > target_freq + 1))
        noise_floor_ringdown = np.median(asd_ringdown.value[noise_mask])
        noise_floor_control = np.median(asd_control.value[noise_mask])

        snr_ringdown = asd_ringdown_value / noise_floor_ringdown
        snr_control = asd_control_value / noise_floor_control

        # Ratio de señal vs control
        signal_ratio = asd_ringdown_value / asd_control_value

        print("\n✅ Resultados del Análisis ASD:")
        print(f"   Frecuencia objetivo: {target_freq} Hz")
        print(f"   Frecuencia detectada: {detected_freq:.2f} Hz")
        print(f"   Diferencia: {abs(detected_freq - target_freq):.3f} Hz")
        print(f"\n   ASD Ringdown (señal): {asd_ringdown_value:.2e} 1/√Hz")
        print(f"   ASD Control (ruido): {asd_control_value:.2e} 1/√Hz")
        print(f"   Ratio señal/control: {signal_ratio:.2f}x")
        print(f"\n   SNR Ringdown: {snr_ringdown:.2f}")
        print(f"   SNR Control: {snr_control:.2f}")

        # Crear gráficos de diagnóstico
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Subplot 1: Comparación ASD ringdown vs control
        ax1 = axes[0, 0]
        ax1.semilogy(asd_ringdown.frequencies.value, asd_ringdown.value, 'b-',
                     label='Ringdown (post-merger)', alpha=0.8)
        ax1.semilogy(asd_control.frequencies.value, asd_control.value, 'gray',
                     label='Control (pre-merger)', alpha=0.6)
        ax1.axvline(target_freq, color='r', linestyle='--', linewidth=2, label='141.7 Hz objetivo')
        ax1.set_xlim(130, 160)
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('ASD (1/√Hz)')
        ax1.set_title('ASD: Ringdown vs Control')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Subplot 2: Zoom en 141.7 Hz
        ax2 = axes[0, 1]
        zoom_mask = (asd_ringdown.frequencies.value >= 140) & (asd_ringdown.frequencies.value <= 143)
        ax2.semilogy(asd_ringdown.frequencies.value[zoom_mask], asd_ringdown.value[zoom_mask],
                     'b-', linewidth=2, label='Ringdown', marker='o')
        ax2.semilogy(asd_control.frequencies.value[zoom_mask], asd_control.value[zoom_mask],
                     'gray', linewidth=2, label='Control', marker='s', alpha=0.6)
        ax2.axvline(target_freq, color='r', linestyle='--', linewidth=2, label='141.7 Hz')
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('ASD (1/√Hz)')
        ax2.set_title('Zoom: 140-143 Hz')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Subplot 3: Serie temporal ringdown
        ax3 = axes[1, 0]
        times_ringdown = ringdown.times.value - ringdown.times.value[0]
        ax3.plot(times_ringdown * 1000, ringdown.value, 'b-', alpha=0.8)
        ax3.set_xlabel('Tiempo post-merger (ms)')
        ax3.set_ylabel('Strain')
        ax3.set_title('Serie Temporal: Ringdown')
        ax3.grid(True, alpha=0.3)

        # Subplot 4: Serie temporal control
        ax4 = axes[1, 1]
        times_control = control.times.value - control.times.value[0]
        ax4.plot(times_control * 1000, control.value, 'gray', alpha=0.8)
        ax4.set_xlabel('Tiempo (ms)')
        ax4.set_ylabel('Strain')
        ax4.set_title('Serie Temporal: Control (ruido)')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = os.path.join(output_dir, 'asd_141hz_analisis.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"\n💾 Gráficos guardados en {output_file}")

        # Validación de resultados
        print("\n🔬 Validación de Resultados:")
        if abs(detected_freq - target_freq) < 0.5:
            print("   ✅ Frecuencia detectada dentro del rango esperado")
        else:
            print("   ⚠️  Frecuencia detectada fuera del rango esperado")

        if signal_ratio > 1.2:
            print("   ✅ Señal superior al ruido de fondo (ratio > 1.2x)")
        else:
            print("   ⚠️  Señal similar al ruido de fondo")

        if snr_ringdown > snr_control:
            print("   ✅ SNR del ringdown superior al control")
        else:
            print("   ⚠️  SNR del ringdown no superior al control")

        results = {
            'target_freq': target_freq,
            'detected_freq': detected_freq,
            'asd_ringdown': asd_ringdown_value,
            'asd_control': asd_control_value,
            'signal_ratio': signal_ratio,
            'snr_ringdown': snr_ringdown,
            'snr_control': snr_control,
            'output_file': output_file
        }

        return results

    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Función principal"""
    results = analyze_asd_141hz()

    if results:
        print("\n" + "=" * 60)
        print("✅ Análisis ASD completado exitosamente")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ Análisis ASD falló")
        return 1


if __name__ == "__main__":
    sys.exit(main())
