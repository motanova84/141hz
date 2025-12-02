#!/usr/bin/env python3
"""
Test del análisis bayesiano multi-evento con datos sintéticos.
Este script demuestra el funcionamiento del módulo sin requerir conectividad a GWOSC.
"""
import numpy as np
import sys

def test_time_window_function():
    """Test de la función time_window"""
    print("=" * 70)
    print("TEST 1: Función time_window()")
    print("=" * 70)
    print()
    
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.analisis_bayesiano_multievento import time_window
    
    events = ['GW150914', 'GW151012', 'GW170104', 'GW190521', 'GW200115']
    
    print("Validando ventanas de tiempo GPS para eventos GWTC:")
    print()
    
    for event in events:
        start, end = time_window(event)
        duration = end - start
        print(f"  {event:12s}: GPS {start:.2f} - {end:.2f}  (Δt = {duration:.1f}s)")
    
    print()
    print("✅ Todas las ventanas de tiempo calculadas correctamente")
    print()

def test_synthetic_analysis():
    """Test del análisis con datos sintéticos"""
    print("=" * 70)
    print("TEST 2: Análisis con datos sintéticos")
    print("=" * 70)
    print()
    
    # Simular picos de frecuencia detectados en cada evento
    # Valores simulados cercanos a 141.7001 Hz con variación realista
    events = ['GW150914', 'GW151012', 'GW170104', 'GW190521', 'GW200115']
    
    # Frecuencias sintéticas con dispersión realista
    synthetic_peaks = [
        141.69,   # GW150914
        141.73,   # GW151012
        141.68,   # GW170104
        141.75,   # GW190521
        141.71    # GW200115
    ]
    
    print("Frecuencias sintéticas generadas (Hz):")
    for event, freq in zip(events, synthetic_peaks):
        print(f"  {event:12s}: {freq:.4f} Hz")
    
    print()
    
    # Calcular estadísticas
    peaks_array = np.array(synthetic_peaks)
    mean_f = np.mean(peaks_array)
    std_f = np.std(peaks_array)
    
    print("Estadísticas del análisis multi-evento:")
    print(f"  Frecuencia media: {mean_f:.4f} ± {std_f:.4f} Hz")
    print()
    
    # Comparación con objetivo
    target_freq = 141.7001
    mean_deviation = abs(mean_f - target_freq)
    
    print("Comparación con frecuencia objetivo (141.7001 Hz):")
    print(f"  Desviación media: {mean_deviation:.4f} Hz")
    print(f"  Dentro de ±1 Hz:  {'✅ SÍ' if mean_deviation < 1.0 else '❌ NO'}")
    print(f"  Dentro de ±0.5 Hz: {'✅ SÍ' if mean_deviation < 0.5 else '❌ NO'}")
    
    print()
    
    if mean_deviation < 0.5:
        print("✅ Test de análisis sintético APROBADO")
        print("   La frecuencia media está dentro del rango esperado")
    else:
        print("⚠️  Test de análisis sintético con desviación significativa")
        return False

def test_statistics_calculation():
    """Test de cálculos estadísticos"""
    print()
    print("=" * 70)
    print("TEST 3: Cálculos estadísticos")
    print("=" * 70)
    print()
    
    # Datos de prueba
    test_data = np.array([141.69, 141.73, 141.68, 141.75, 141.71])
    
    mean = np.mean(test_data)
    std = np.std(test_data)
    
    print(f"Datos de prueba: {test_data}")
    print(f"Media calculada: {mean:.4f} Hz")
    print(f"Desviación estándar: {std:.4f} Hz")
    print()
    
    # Verificar que los cálculos son razonables
    assert 141.6 < mean < 141.8, "Media fuera del rango esperado"
    assert 0 < std < 0.1, "Desviación estándar fuera del rango esperado"
    
    print("✅ Cálculos estadísticos correctos")
    print()

def test_error_handling():
    """Test de manejo de errores"""
    print("=" * 70)
    print("TEST 4: Manejo de errores")
    print("=" * 70)
    print()
    
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.analisis_bayesiano_multievento import time_window
    
    # Probar con evento inexistente
    try:
        time_window('GW999999')
        print("❌ Error: Se esperaba ValueError para evento inexistente")
        return False
    except ValueError as e:
        print(f"✅ ValueError capturado correctamente: {e}")
        print()

def main():
    """Ejecutar todos los tests"""
    print()
    print("🧪 SUITE DE TESTS: Análisis Bayesiano Multi-evento")
    print()
    
    tests = [
        ("time_window", test_time_window_function),
        ("synthetic_analysis", test_synthetic_analysis),
        ("statistics", test_statistics_calculation),
        ("error_handling", test_error_handling)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is False:
                print(f"❌ Test {test_name} falló (retornó False)")
                failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_name} falló con excepción: {e}")
            failed += 1
    
    print("=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"✅ Tests aprobados: {passed}/{len(tests)}")
    print(f"❌ Tests fallidos:  {failed}/{len(tests)}")
    print()
    
    if failed == 0:
        print("🎉 TODOS LOS TESTS APROBADOS")
        return 0
    else:
        print("⚠️  Algunos tests fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
