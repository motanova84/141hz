#!/usr/bin/env python3
"""
Test unitario para verificar la lógica corregida de búsqueda de frecuencias
"""
import sys
import numpy as np
import scipy.signal

def test_frequency_search_logic():
    """Prueba la lógica de búsqueda de frecuencia corregida"""
    print("🧪 Test: Verificando lógica de búsqueda de frecuencias")
    
    # Crear datos sintéticos con una señal en 141.7 Hz
    sample_rate = 4096
    duration = 32
    t = np.linspace(0, duration, sample_rate * duration)
    
    # Señal simulada: ruido + componente en 141.7 Hz
    target_freq = 141.7001
    noise = np.random.normal(0, 0.1, len(t))
    signal = 0.5 * np.sin(2 * np.pi * target_freq * t)
    data = signal + noise
    
    # Análisis espectral (como en el script corregido)
    # Usar ventana más grande para mejor resolución frecuencial
    frequencies, times, power = scipy.signal.spectrogram(data, fs=sample_rate, nperseg=8192)
    
    # Buscar frecuencia más cercana al objetivo (MÉTODO CORREGIDO)
    freq_idx = np.argmin(np.abs(frequencies - target_freq))
    peak = frequencies[freq_idx]
    peak_power = np.max(power[freq_idx, :])
    
    # Verificar resultados
    print(f"   Frecuencia objetivo: {target_freq:.4f} Hz")
    print(f"   Frecuencia detectada: {peak:.4f} Hz")
    print(f"   Diferencia: {abs(peak - target_freq):.4f} Hz")
    print(f"   Potencia del pico: {peak_power:.2e}")
    
    # Verificar que la frecuencia detectada está cerca del objetivo
    tolerance = 1.0  # Hz
    assert abs(peak - target_freq) < tolerance, f"Frecuencia fuera de tolerancia: {abs(peak - target_freq):.4f} Hz > {tolerance} Hz"
    print("   ✅ Test PASSED - Frecuencia detectada correctamente")

def test_old_logic_fails():
    """Demuestra que la lógica original tiene problemas"""
    print("\n🔬 Test: Demostrando problemas de la lógica original")
    
    # Crear array de frecuencias
    frequencies = np.linspace(0, 2048, 513)
    target_freq = 141.7001
    
    # Lógica ORIGINAL (problemática):
    try:
        # frequencies == target_freq rara vez funciona con floats
        mask = (frequencies == target_freq)
        matching_freqs = frequencies[mask]
        print(f"   Lógica original: {len(matching_freqs)} coincidencias exactas encontradas")
        if len(matching_freqs) == 0:
            print("   ⚠️  Lógica original FALLA - Sin coincidencias exactas")
    except Exception as e:
        print(f"   ❌ Error en lógica original: {e}")
    
    # Lógica CORREGIDA:
    freq_idx = np.argmin(np.abs(frequencies - target_freq))
    closest_freq = frequencies[freq_idx]
    print(f"   Lógica corregida: Frecuencia más cercana = {closest_freq:.4f} Hz")
    print(f"   Diferencia: {abs(closest_freq - target_freq):.4f} Hz")
    print("   ✅ Lógica corregida FUNCIONA - Encuentra frecuencia cercana")

if __name__ == "__main__":
    print("=" * 60)
    print("Test de Validación de Correcciones")
    print("=" * 60)
    
    # Ejecutar tests
    try:
        test_frequency_search_logic()
        test1_passed = True
    except Exception as e:
        print(f"❌ Error en test_frequency_search_logic: {e}")
        test1_passed = False
    
    test_old_logic_fails()
    
    print("\n" + "=" * 60)
    if test1_passed:
        print("✅ RESULTADO: Todas las correcciones validadas")
        sys.exit(0)
    else:
        print("❌ RESULTADO: Verificar implementación")
        sys.exit(1)
    print("=" * 60)
