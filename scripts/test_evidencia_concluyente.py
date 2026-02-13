#!/usr/bin/env python3
"""
Test unitario para el módulo de evidencia concluyente
Valida la estructura de datos y las funciones del módulo
"""
import sys
from pathlib import Path

# Importar el módulo a testear
from evidencia_concluyente import (
    evidencia_concluyente,
    eventos_detallados,
    metricas_estadisticas,
    validar_estructura_evidencia,
    obtener_evento,
    listar_eventos_confirmados,
    obtener_metricas_estadisticas
)


def test_estructura_basica():
    """Test: Validar estructura básica de evidencia_concluyente"""
    print("🧪 Test 1: Estructura básica")
    
    assert 'eventos_confirmados' in evidencia_concluyente, "Falta clave 'eventos_confirmados'"
    assert 'significancia_estadistica' in evidencia_concluyente, "Falta clave 'significancia_estadistica'"
    
    assert len(evidencia_concluyente['eventos_confirmados']) == 5, "Deben haber 5 eventos confirmados"
    
    print("   ✅ Estructura básica correcta")
    return True


def test_eventos_detallados():
    """Test: Validar que todos los eventos tienen datos completos"""
    print("🧪 Test 2: Eventos detallados")
    
    eventos_esperados = ['GW150914', 'GW151012', 'GW170104', 'GW190521', 'GW200115']
    
    for evento in eventos_esperados:
        assert evento in eventos_detallados, f"Falta evento {evento}"
        
        datos = eventos_detallados[evento]
        campos_requeridos = ['frecuencia_hz', 'snr_h1', 'snr_l1', 'diferencia_objetivo', 
                            'gps_time', 'detector_primario', 'validacion', 'error_relativo']
        
        for campo in campos_requeridos:
            assert campo in datos, f"Falta campo '{campo}' en {evento}"
    
    print(f"   ✅ {len(eventos_esperados)} eventos con datos completos")
    return True


def test_metricas_estadisticas():
    """Test: Validar métricas estadísticas consolidadas"""
    print("🧪 Test 3: Métricas estadísticas")
    
    assert 'significancia_global' in metricas_estadisticas
    assert 'coherencia_multi_detector' in metricas_estadisticas
    assert 'precision_frecuencial' in metricas_estadisticas
    assert 'snr_consolidado' in metricas_estadisticas
    
    # Validar p-value
    p_value = metricas_estadisticas['significancia_global']['p_value']
    assert p_value < 0.01, f"p-value {p_value} no es significativo (debe ser < 0.01)"
    
    # Validar Bayes factor
    bf = metricas_estadisticas['significancia_global']['log_bayes_factor']
    assert bf > 2.0, f"Bayes factor {bf} no indica evidencia fuerte (debe ser > 2.0)"
    
    # Validar coherencia
    coherencia = metricas_estadisticas['coherencia_multi_detector']['tasa_coincidencia']
    assert coherencia >= 0.8, f"Tasa de coincidencia {coherencia} muy baja (debe ser >= 0.8)"
    
    print("   ✅ Métricas estadísticas válidas")
    return True


def test_rangos_frecuencia():
    """Test: Validar que todas las frecuencias están cerca de 141.7 Hz"""
    print("🧪 Test 4: Rangos de frecuencia")
    
    frecuencia_objetivo = 141.7001
    tolerancia = 0.1  # Hz
    
    for evento, datos in eventos_detallados.items():
        freq = datos['frecuencia_hz']
        diferencia = abs(freq - frecuencia_objetivo)
        
        assert diferencia <= tolerancia, \
            f"{evento}: frecuencia {freq} Hz muy alejada del objetivo (diferencia: {diferencia:.3f} Hz)"
    
    print(f"   ✅ Todas las frecuencias dentro de ±{tolerancia} Hz del objetivo")
    return True


def test_snr_significativo():
    """Test: Validar que todos los SNR son significativos"""
    print("🧪 Test 5: SNR significativo")
    
    umbral_snr = 5.0
    
    for evento, datos in eventos_detallados.items():
        snr_h1 = datos['snr_h1']
        
        # H1 debe tener SNR alto (es el detector primario)
        assert snr_h1 >= umbral_snr, \
            f"{evento}: SNR H1 ({snr_h1:.2f}) por debajo del umbral ({umbral_snr})"
    
    print(f"   ✅ Todos los eventos con SNR H1 > {umbral_snr}")
    return True


def test_validacion_estructura():
    """Test: Función validar_estructura_evidencia()"""
    print("🧪 Test 6: Función de validación")
    
    resultado = validar_estructura_evidencia()
    
    assert 'valido' in resultado
    assert 'errores' in resultado
    assert 'advertencias' in resultado
    assert 'eventos_validados' in resultado
    
    assert resultado['eventos_validados'] == 5, \
        f"Eventos validados: {resultado['eventos_validados']}, esperados: 5"
    
    if not resultado['valido']:
        print("   ⚠️  Advertencias encontradas:")
        for adv in resultado['advertencias']:
            print(f"      - {adv}")
    
    print("   ✅ Función de validación operativa")
    return True


def test_funciones_acceso():
    """Test: Funciones de acceso a datos"""
    print("🧪 Test 7: Funciones de acceso")
    
    # Test obtener_evento
    evento_gw150914 = obtener_evento('GW150914')
    assert evento_gw150914 is not None, "No se pudo obtener GW150914"
    assert evento_gw150914['frecuencia_hz'] == 141.69, "Frecuencia incorrecta para GW150914"
    
    # Test listar_eventos_confirmados
    eventos = listar_eventos_confirmados()
    assert len(eventos) == 5, f"Se esperaban 5 eventos, se obtuvieron {len(eventos)}"
    assert 'GW150914' in eventos, "GW150914 no está en la lista"
    
    # Test obtener_metricas_estadisticas
    metricas = obtener_metricas_estadisticas()
    assert 'significancia_global' in metricas, "Faltan métricas de significancia"
    
    print("   ✅ Todas las funciones de acceso funcionan correctamente")
    return True


def test_error_relativo():
    """Test: Validar que el error relativo es bajo"""
    print("🧪 Test 8: Error relativo")
    
    umbral_error = 0.03  # 0.03% como indica la especificación
    
    for evento, datos in eventos_detallados.items():
        error = datos['error_relativo']
        assert error <= umbral_error, \
            f"{evento}: error relativo {error:.3f}% excede umbral ({umbral_error}%)"
    
    print(f"   ✅ Todos los errores relativos < {umbral_error}%")
    return True


def test_coherencia_multi_detector():
    """Test: Validar coherencia entre detectores"""
    print("🧪 Test 9: Coherencia multi-detector")
    
    coherencia_data = metricas_estadisticas['coherencia_multi_detector']
    
    assert coherencia_data['coincidencias'] == coherencia_data['total_eventos'], \
        "No todos los eventos tienen coincidencia multi-detector"
    
    assert coherencia_data['tasa_coincidencia'] == 1.0, \
        f"Tasa de coincidencia {coherencia_data['tasa_coincidencia']:.1%} no es 100%"
    
    assert coherencia_data['estado'] == 'Confirmado', \
        f"Estado '{coherencia_data['estado']}' no es 'Confirmado'"
    
    print("   ✅ Coherencia multi-detector 100% confirmada")
    return True


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests y reporta resultados"""
    print("=" * 70)
    print("🧪 TEST SUITE: EVIDENCIA CONCLUYENTE")
    print("=" * 70)
    print()
    
    tests = [
        ("Estructura básica", test_estructura_basica),
        ("Eventos detallados", test_eventos_detallados),
        ("Métricas estadísticas", test_metricas_estadisticas),
        ("Rangos de frecuencia", test_rangos_frecuencia),
        ("SNR significativo", test_snr_significativo),
        ("Validación estructura", test_validacion_estructura),
        ("Funciones de acceso", test_funciones_acceso),
        ("Error relativo", test_error_relativo),
        ("Coherencia multi-detector", test_coherencia_multi_detector)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            exito = test_func()
            resultados.append((nombre, exito, None))
        except AssertionError as e:
            print(f"   ❌ FALLÓ: {e}")
            resultados.append((nombre, False, str(e)))
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            resultados.append((nombre, False, str(e)))
        print()
    
    # Resumen final
    print("=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    
    exitosos = sum(1 for _, exito, _ in resultados if exito)
    total = len(resultados)
    
    for nombre, exito, error in resultados:
        simbolo = "✅" if exito else "❌"
        print(f"{simbolo} {nombre}")
        if error:
            print(f"   Error: {error}")
    
    print()
    print(f"Total: {exitosos}/{total} tests exitosos ({exitosos/total*100:.1f}%)")
    print("=" * 70)
    
    if exitosos == total:
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print(f"❌ {total - exitosos} TESTS FALLARON")
        return 1


if __name__ == "__main__":
    exit_code = ejecutar_todos_los_tests()
    sys.exit(exit_code)
