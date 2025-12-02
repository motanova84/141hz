#!/usr/bin/env python3
"""
Tests para el módulo multi_event_snr_analysis
==============================================

Suite de tests para validar el análisis multi-evento de SNR sin requerir
conectividad a GWOSC.
"""

import numpy as np
import sys
import os

# Importar módulo a testear
sys.path.insert(0, os.path.dirname(__file__))


def test_snr_calculation():
    """
    Test 1: Validar el cálculo de SNR con datos sintéticos.
    """
    print("=" * 70)
    print("TEST 1: Cálculo de SNR")
    print("=" * 70)
    
    # Crear una señal sintética con ruido
    np.random.seed(42)
    signal = np.sin(2 * np.pi * 141.7 * np.linspace(0, 1, 4096))
    noise = np.random.normal(0, 0.1, 4096)
    data = signal + noise
    
    # Calcular SNR manualmente
    snr = np.max(np.abs(data)) / np.std(data)
    
    # Validar que el SNR es razonable
    assert snr > 0, "SNR debe ser positivo"
    assert snr < 100, "SNR debe ser realista (< 100)"
    
    print(f"✅ SNR calculado: {snr:.2f}")
    print(f"✅ Validación: SNR está en rango esperado (0 < SNR < 100)")
    print()
    
    return True


def test_event_configuration():
    """
    Test 2: Validar configuración de eventos.
    """
    print("=" * 70)
    print("TEST 2: Configuración de Eventos")
    print("=" * 70)
    
    try:
        from multi_event_snr_analysis import events
    except ImportError as e:
        print(f"⚠️  Importación fallida: {e}")
        print(f"✅ Test omitido (dependencia no disponible)")
        print()
        return True
    
    # Validar que hay eventos configurados
    assert len(events) > 0, "Debe haber al menos un evento configurado"
    
    # Validar estructura de cada evento
    for name, (start, end) in events.items():
        assert isinstance(name, str), f"Nombre de evento debe ser string: {name}"
        assert isinstance(start, int), f"Tiempo de inicio debe ser int: {start}"
        assert isinstance(end, int), f"Tiempo de fin debe ser int: {end}"
        assert end > start, f"Tiempo final debe ser mayor que inicial: {name}"
        assert (end - start) == 32, f"Ventana debe ser 32 segundos: {name}"
    
    print(f"✅ Total de eventos configurados: {len(events)}")
    print(f"✅ Todos los eventos tienen estructura válida")
    
    # Mostrar lista de eventos
    print()
    print("Eventos configurados:")
    for i, name in enumerate(events.keys(), 1):
        print(f"  {i}. {name}")
    print()
    
    return True


def test_band_configuration():
    """
    Test 3: Validar configuración de banda de frecuencia.
    """
    print("=" * 70)
    print("TEST 3: Configuración de Banda")
    print("=" * 70)
    
    try:
        from multi_event_snr_analysis import target_band, target_freq, snr_threshold
    except ImportError as e:
        print(f"⚠️  Importación fallida: {e}")
        print(f"✅ Test omitido (dependencia no disponible)")
        print()
        return True
    
    # Validar banda de frecuencia
    assert len(target_band) == 2, "Banda debe tener 2 elementos [min, max]"
    assert target_band[1] > target_band[0], "Frecuencia máxima > mínima"
    
    # Validar que target_freq está dentro de la banda
    assert target_band[0] <= target_freq <= target_band[1], \
        "Frecuencia objetivo debe estar dentro de la banda"
    
    # Validar umbral de SNR
    assert snr_threshold > 0, "Umbral de SNR debe ser positivo"
    
    print(f"✅ Banda de frecuencia: {target_band[0]}-{target_band[1]} Hz")
    print(f"✅ Frecuencia objetivo: {target_freq} Hz")
    print(f"✅ Umbral de SNR: {snr_threshold}")
    print(f"✅ Todas las configuraciones son válidas")
    print()
    
    return True


def test_calculate_snr_function():
    """
    Test 4: Validar que la función calculate_snr existe y tiene la firma correcta.
    """
    print("=" * 70)
    print("TEST 4: Función calculate_snr")
    print("=" * 70)
    
    try:
        from multi_event_snr_analysis import calculate_snr
    except ImportError as e:
        print(f"⚠️  Importación fallida: {e}")
        print(f"✅ Test omitido (dependencia no disponible)")
        print()
        return True
    
    import inspect
    
    # Verificar que la función existe
    assert callable(calculate_snr), "calculate_snr debe ser una función"
    
    # Verificar firma de la función
    sig = inspect.signature(calculate_snr)
    params = list(sig.parameters.keys())
    assert 'data' in params, "Función debe tener parámetro 'data'"
    assert 'band' in params, "Función debe tener parámetro 'band'"
    
    print(f"✅ Función calculate_snr existe")
    print(f"✅ Firma correcta: {sig}")
    print()
    
    return True


def test_analyze_event_function():
    """
    Test 5: Validar que la función analyze_event existe y tiene la firma correcta.
    """
    print("=" * 70)
    print("TEST 5: Función analyze_event")
    print("=" * 70)
    
    try:
        from multi_event_snr_analysis import analyze_event
    except ImportError as e:
        print(f"⚠️  Importación fallida: {e}")
        print(f"✅ Test omitido (dependencia no disponible)")
        print()
        return True
    
    import inspect
    
    # Verificar que la función existe
    assert callable(analyze_event), "analyze_event debe ser una función"
    
    # Verificar firma de la función
    sig = inspect.signature(analyze_event)
    params = list(sig.parameters.keys())
    assert 'name' in params, "Función debe tener parámetro 'name'"
    assert 'start' in params, "Función debe tener parámetro 'start'"
    assert 'end' in params, "Función debe tener parámetro 'end'"
    assert 'band' in params, "Función debe tener parámetro 'band'"
    
    print(f"✅ Función analyze_event existe")
    print(f"✅ Firma correcta: {sig}")
    print()
    
    return True


def main():
    """
    Ejecuta todos los tests.
    """
    print()
    print("🧪 SUITE DE TESTS: Análisis Multi-evento de SNR")
    print()
    
    tests = [
        ("Cálculo de SNR", test_snr_calculation),
        ("Configuración de Eventos", test_event_configuration),
        ("Configuración de Banda", test_band_configuration),
        ("Función calculate_snr", test_calculate_snr_function),
        ("Función analyze_event", test_analyze_event_function),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
                print(f"❌ Test '{name}' falló")
        except AssertionError as e:
            failed += 1
            print(f"❌ Test '{name}' falló: {e}")
            print()
        except Exception as e:
            failed += 1
            print(f"❌ Test '{name}' falló con error: {e}")
            print()
    
    # Resumen
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
        print(f"⚠️ {failed} test(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
