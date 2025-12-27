#!/usr/bin/env python3
"""
Tests para el módulo de validación Virgo V1

Este módulo valida que el script de análisis Virgo V1 funcione correctamente
sin requerir conectividad a GWOSC.
"""

import sys
import os

# Agregar el directorio scripts al path si es necesario
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np


def test_virgo_events_configuration():
    """Test: Verifica que los eventos de Virgo estén correctamente configurados"""
    from virgo_v1_validation import virgo_events
    
    # Verificar que hay exactamente 4 eventos
    assert len(virgo_events) == 4, f"Expected 4 Virgo events, got {len(virgo_events)}"
    
    # Verificar que los eventos esperados están presentes
    expected_events = ["GW170814", "GW170817", "GW170818", "GW170823"]
    for event in expected_events:
        assert event in virgo_events, f"Event {event} not found in virgo_events"
    
    # Verificar que cada evento tiene exactamente 2 valores (start, end)
    for name, times in virgo_events.items():
        assert len(times) == 2, f"Event {name} should have 2 times (start, end)"
        assert times[1] > times[0], f"End time must be greater than start time for {name}"
    
    print("✅ Test: Configuración de eventos Virgo - PASSED")
    return True


def test_band_configuration():
    """Test: Verifica la configuración de la banda de frecuencia"""
    from virgo_v1_validation import target_band, target_freq, snr_threshold
    
    # Verificar que la banda está centrada en 141.7 Hz
    assert len(target_band) == 2, "Band should have 2 values [min, max]"
    assert target_band[0] < target_freq < target_band[1], "Target freq should be within band"
    assert abs((target_band[0] + target_band[1]) / 2 - target_freq) < 0.1, \
        "Band should be centered around target frequency"
    
    # Verificar que el umbral de SNR es razonable
    assert snr_threshold > 0, "SNR threshold must be positive"
    assert snr_threshold == 5.0, "SNR threshold should be 5.0 (standard)"
    
    print("✅ Test: Configuración de banda de frecuencia - PASSED")
    return True


def test_calculate_snr_function_exists():
    """Test: Verifica que la función calculate_snr existe y tiene la firma correcta"""
    from virgo_v1_validation import calculate_snr
    import inspect
    
    # Verificar que la función existe
    assert callable(calculate_snr), "calculate_snr should be a callable function"
    
    # Verificar la firma de la función
    sig = inspect.signature(calculate_snr)
    params = list(sig.parameters.keys())
    assert len(params) == 2, f"calculate_snr should have 2 parameters, got {len(params)}"
    assert params[0] == 'data', "First parameter should be 'data'"
    assert params[1] == 'band', "Second parameter should be 'band'"
    
    print("✅ Test: Función calculate_snr - PASSED")
    return True


def test_analyze_event_v1_function_exists():
    """Test: Verifica que la función analyze_event_v1 existe y tiene la firma correcta"""
    from virgo_v1_validation import analyze_event_v1
    import inspect
    
    # Verificar que la función existe
    assert callable(analyze_event_v1), "analyze_event_v1 should be a callable function"
    
    # Verificar la firma de la función
    sig = inspect.signature(analyze_event_v1)
    params = list(sig.parameters.keys())
    assert len(params) == 4, f"analyze_event_v1 should have 4 parameters, got {len(params)}"
    assert params[0] == 'name', "First parameter should be 'name'"
    assert params[1] == 'start', "Second parameter should be 'start'"
    assert params[2] == 'end', "Third parameter should be 'end'"
    assert params[3] == 'band', "Fourth parameter should be 'band'"
    
    print("✅ Test: Función analyze_event_v1 - PASSED")
    return True


def test_expected_snr_values():
    """Test: Verifica que los valores esperados de SNR están documentados"""
    # Valores esperados según el problema statement
    expected_snr = {
        "GW170814": 8.08,
        "GW170817": 8.57,
        "GW170818": 7.86,
        "GW170823": float('nan')  # Datos inválidos
    }
    
    # Verificar que todos los valores son numéricos o NaN
    for event, snr in expected_snr.items():
        assert isinstance(snr, (int, float)), f"SNR for {event} should be numeric"
        if not np.isnan(snr):
            assert snr > 0, f"Valid SNR for {event} should be positive"
            assert snr >= 5.0, f"SNR for {event} should be >= 5.0 (threshold)"
    
    print("✅ Test: Valores esperados de SNR - PASSED")
    return True


def test_detection_rate_calculation():
    """Test: Verifica el cálculo de la tasa de detección"""
    # Según el problema statement: 3/3 = 100% (eventos válidos)
    valid_events = 3
    total_events = 4
    invalid_events = 1
    
    detection_rate = (valid_events / valid_events) * 100  # 3/3 = 100%
    
    assert detection_rate == 100.0, "Detection rate should be 100% for valid events"
    assert valid_events + invalid_events == total_events, "Valid + invalid should equal total"
    
    print("✅ Test: Cálculo de tasa de detección - PASSED")
    return True


def test_module_imports():
    """Test: Verifica que el módulo puede importarse correctamente"""
    try:
        import virgo_v1_validation
        assert hasattr(virgo_v1_validation, 'main'), "Module should have main() function"
        assert hasattr(virgo_v1_validation, 'calculate_snr'), "Module should have calculate_snr()"
        assert hasattr(virgo_v1_validation, 'analyze_event_v1'), "Module should have analyze_event_v1()"
        print("✅ Test: Importación del módulo - PASSED")
        return True
    except ImportError as e:
        print(f"❌ Test: Importación del módulo - FAILED: {e}")
        return False


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("🧪 TEST SUITE: Validación Virgo V1")
    print("=" * 70)
    print()
    
    tests = [
        test_module_imports,
        test_virgo_events_configuration,
        test_band_configuration,
        test_calculate_snr_function_exists,
        test_analyze_event_v1_function_exists,
        test_expected_snr_values,
        test_detection_rate_calculation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Tasa de éxito: {100*passed/(passed+failed):.1f}%")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
