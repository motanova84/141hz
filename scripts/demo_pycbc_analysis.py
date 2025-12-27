#!/usr/bin/env python3
"""
Demostración del flujo de análisis de GW150914 con PyCBC
Este script muestra cómo funciona el análisis sin necesidad de descargar datos reales.

Uso:
    python scripts/demo_pycbc_analysis.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os


def generar_datos_simulados():
    """Genera datos simulados de GW150914 para demostración"""
    print("📊 Generando datos simulados de GW150914...")
    
    # Tiempo GPS del evento
    gps_time = 1126259462.4
    
    # Generar ventana temporal
    dt = 1.0 / 4096  # Sample rate
    t_start = gps_time - 0.19
    t_end = gps_time + 0.05
    times = np.arange(t_start, t_end, dt)
    
    # Generar señal simulada (chirp gravitacional simplificado)
    # Frecuencia aumenta con el tiempo (inspiraling)
    f0 = 35  # Hz inicial
    f1 = 250  # Hz final
    
    # Chirp rate
    k = (f1 - f0) / (times[-1] - times[0])
    
    # Generar señal
    phase = 2 * np.pi * (f0 * (times - times[0]) + 0.5 * k * (times - times[0])**2)
    
    # Amplitud exponencial (merger)
    t_merger = gps_time
    amplitude = np.exp(-((times - t_merger) / 0.01)**2)
    
    # Señal H1
    strain_h1 = amplitude * np.sin(phase)
    
    # Señal L1 (invertida y desplazada)
    strain_l1 = -amplitude * np.sin(phase)
    shift_samples = int(0.007 / dt)
    strain_l1 = np.roll(strain_l1, shift_samples)
    
    # Añadir ruido
    noise_level = 0.3
    strain_h1 += np.random.normal(0, noise_level, len(times))
    strain_l1 += np.random.normal(0, noise_level, len(times))
    
    return times, strain_h1, strain_l1


def aplicar_filtrado_simulado(strain):
    """Simula el efecto del filtrado y blanqueado"""
    print("   Aplicando filtros y blanqueado simulados...")
    
    # Normalizar
    strain = strain / np.std(strain)
    
    # Simular blanqueado (aplanar espectro)
    from scipy import signal
    b, a = signal.butter(4, [35/(4096/2), 300/(4096/2)], btype='band')
    strain_filtered = signal.filtfilt(b, a, strain)
    
    return strain_filtered


def main():
    """Función principal de demostración"""
    print("🌌 Demostración: Análisis de GW150914 con PyCBC")
    print("=" * 60)
    print()
    print("ℹ️  Este script demuestra el flujo del análisis sin descargar datos reales")
    print()
    
    # Generar datos simulados
    times, strain_h1, strain_l1 = generar_datos_simulados()
    print(f"   ✅ {len(times)} muestras generadas")
    print()
    
    # Procesar H1
    print("📡 Procesando detector H1...")
    strain_h1_filtered = aplicar_filtrado_simulado(strain_h1)
    print("   ✅ H1 procesado")
    print()
    
    # Procesar L1
    print("📡 Procesando detector L1...")
    strain_l1_filtered = aplicar_filtrado_simulado(strain_l1)
    print("   ✅ L1 procesado")
    print()
    
    # Crear gráfica
    print("📊 Generando gráfica...")
    plt.figure(figsize=(12, 6))
    
    plt.plot(times, strain_h1_filtered, label='H1 (Hanford)', alpha=0.8)
    plt.plot(times, strain_l1_filtered, label='L1 (Livingston)', alpha=0.8)
    
    plt.xlim(1126259462.21, 1126259462.45)
    plt.ylim(-150, 150)
    plt.xlabel("GPS Time (s)")
    plt.ylabel("Smoothed-Whitened Strain (simulated)")
    plt.title("GW150914 Gravitational Wave Signal (Demo with Simulated Data)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Añadir anotación
    plt.axvline(x=1126259462.4, color='red', linestyle='--', alpha=0.5, label='Merger')
    plt.text(1126259462.4, 120, 'Merger', ha='center', color='red')
    
    # Guardar
    output_dir = 'results/figures'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'gw150914_pycbc_demo.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    
    print(f"   ✅ Gráfica guardada en: {output_file}")
    print()
    print("🔍 Comparación con análisis real:")
    print("   - Datos simulados: Chirp simplificado + ruido gaussiano")
    print("   - Análisis real: Datos de GWOSC + PyCBC completo")
    print("   - Similitudes: Forma general del chirp, timing del merger")
    print("   - Diferencias: Ruido, detalles finos de la señal")
    print()
    print("💡 Para ejecutar el análisis real:")
    print("   make pycbc-analysis")
    print("   o")
    print("   python scripts/analizar_gw150914_pycbc.py")
    print()
    print("✅ Demostración completada")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Demostración interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
