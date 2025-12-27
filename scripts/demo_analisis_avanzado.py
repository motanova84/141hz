#!/usr/bin/env python3
"""
Demo: Análisis Estadístico Avanzado con GW150914
Demuestra el uso de las tres funciones del problem statement con datos reales
"""
import sys
import numpy as np
from gwpy.timeseries import TimeSeries
import warnings
warnings.filterwarnings('ignore')

# Importar funciones del módulo de análisis avanzado
from analisis_estadistico_avanzado import (
    analisis_significancia_estadistica,
    compute_coherence_h1_l1,
    exclude_instrumental_artifacts,
    ejecutar_analisis_completo
)


def load_gw150914_data():
    """Cargar datos de GW150914 desde GWOSC"""
    print("📡 Descargando datos de GW150914 desde GWOSC...")
    
    try:
        # Parámetros del evento GW150914
        merger_time = 1126259462.423
        start = merger_time - 16  # 32 segundos de datos
        end = merger_time + 16
        
        # Descargar datos de ambos detectores
        print("   Descargando H1...")
        h1_data = TimeSeries.fetch_open_data('H1', start, end, sample_rate=4096)
        
        print("   Descargando L1...")
        l1_data = TimeSeries.fetch_open_data('L1', start, end, sample_rate=4096)
        
        print(f"   ✅ Datos cargados: {len(h1_data)} muestras a {h1_data.sample_rate} Hz")
        
        return h1_data, l1_data, merger_time
        
    except Exception as e:
        print(f"   ❌ Error cargando datos: {e}")
        print("   💡 Verificar conectividad a internet")
        return None, None, None


def preprocess_data(data):
    """Preprocesamiento estándar de datos LIGO"""
    print("   Aplicando preprocesamiento...")
    # Filtros estándar
    data = data.highpass(20)  # Remover ruido de baja frecuencia
    data = data.notch(60)     # Remover línea de 60 Hz
    data = data.notch(120)    # Remover armónico de 120 Hz
    
    return data


def extract_ringdown(data, merger_time, duration=0.5):
    """Extraer segmento de ringdown post-merger"""
    print(f"   Extrayendo ringdown (duración: {duration}s)...")
    ringdown_start = merger_time + 0.01  # 10 ms post-merger
    ringdown_end = ringdown_start + duration
    
    ringdown = data.crop(ringdown_start, ringdown_end)
    return ringdown


def main():
    """Ejecutar demo completo"""
    print("=" * 70)
    print("🌌 DEMO: ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 70)
    print("Evento: GW150914")
    print("Frecuencia objetivo: 141.7001 Hz")
    print("=" * 70)
    print()
    
    # Intentar cargar datos reales
    h1_data, l1_data, merger_time = load_gw150914_data()
    
    if h1_data is None or l1_data is None:
        print("\n⚠️  No se pudieron cargar datos reales de GWOSC")
        print("💡 Ejecutando con datos sintéticos para demostración...")
        
        # Generar datos sintéticos
        fs = 4096
        duration = 2  # segundos
        t = np.linspace(0, duration, int(fs * duration))
        
        # Señal de prueba: modo en 141.7 Hz
        f0 = 141.7001
        signal_h1 = 1e-21 * np.exp(-np.pi * f0 * t / 8.5) * np.sin(2 * np.pi * f0 * t)
        noise_h1 = np.random.normal(0, 2e-22, len(t))
        h1_data = signal_h1 + noise_h1
        
        signal_l1 = 0.7e-21 * np.exp(-np.pi * f0 * t / 8.5) * np.sin(2 * np.pi * f0 * t + np.pi/4)
        noise_l1 = np.random.normal(0, 2e-22, len(t))
        l1_data = signal_l1 + noise_l1
        
        # Ejecutar análisis completo
        print()
        resultados = ejecutar_analisis_completo(h1_data, l1_data, f0, fs)
        
    else:
        print("\n✅ Datos reales cargados exitosamente")
        print()
        
        # Preprocesar datos
        print("🔧 Preprocesando datos...")
        h1_processed = preprocess_data(h1_data)
        l1_processed = preprocess_data(l1_data)
        
        # Extraer ringdown
        h1_ringdown = extract_ringdown(h1_processed, merger_time, duration=0.5)
        l1_ringdown = extract_ringdown(l1_processed, merger_time, duration=0.5)
        
        print("   ✅ Preprocesamiento completado")
        print()
        
        # Ejecutar análisis completo
        f0 = 141.7001
        fs = h1_ringdown.sample_rate.value
        
        resultados = ejecutar_analisis_completo(
            h1_ringdown, 
            l1_ringdown, 
            f0, 
            fs
        )
    
    # Mostrar resultados finales
    print()
    print("=" * 70)
    print("🎯 CONCLUSIÓN")
    print("=" * 70)
    
    if resultados['validacion_exitosa']:
        print("✅ Validación exitosa: cumple al menos 3 de 4 criterios")
    else:
        print("⚠️  Validación parcial: revisar criterios no cumplidos")
    
    print()
    print("📊 Detalles:")
    print(f"   • Criterios cumplidos: {resultados['criterios_cumplidos']}/{resultados['total_criterios']}")
    
    if resultados['significancia']['passed']:
        print("   • ✅ Significancia estadística (p < 10⁻⁶)")
    else:
        print("   • ❌ Significancia estadística no cumplida")
    
    if resultados['coherencia']['coherent']:
        print("   • ✅ Coherencia multisitio (coherence > 0.5)")
    else:
        print("   • ❌ Coherencia multisitio no cumplida")
    
    if resultados['sistemáticos']['passed']:
        print("   • ✅ Exclusión de sistemáticos")
    else:
        print("   • ❌ Exclusión de sistemáticos no cumplida")
    
    print()
    print("=" * 70)
    print("💡 NOTA:")
    print("Los criterios de validación son muy estrictos (p < 10⁻⁶, coherence > 0.5).")
    print("Con datos sintéticos, es normal que no todos se cumplan.")
    print("Con datos reales de alta calidad, los criterios deberían mejorar.")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
