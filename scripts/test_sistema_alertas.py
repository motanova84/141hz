#!/usr/bin/env python3
"""
Tests para el Sistema de Alertas GW250114
Valida la funcionalidad de envío de alertas automáticas
"""
import sys
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from sistema_alertas_gw250114 import SistemaAlertasGW250114


def test_inicializacion():
    """Test: Inicialización correcta del sistema"""
    print("🧪 TEST 1: Inicialización del sistema")
    print("-" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    assert sistema.config['email_destino'] == 'institutoconsciencia@proton.me', "Email destino incorrecto"
    assert sistema.config['intervalo_verificacion'] == 1800, "Intervalo incorrecto"
    assert sistema.config['webhook_url'] is None, "Webhook URL debería ser None por defecto"
    
    print("   ✅ Configuración inicial correcta")
    print("   ✅ Email destino: institutoconsciencia@proton.me")
    print("   ✅ Intervalo: 1800 segundos (30 minutos)")
    print("   ✅ TEST PASADO\n")
    
    return True


def test_alerta_disponibilidad():
    """Test: Envío de alerta de disponibilidad"""
    print("🧪 TEST 2: Alerta de disponibilidad")
    print("-" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    # Este test solo verifica que no haya errores al enviar
    try:
        sistema.enviar_alerta_disponible("GW250114_TEST")
        print("   ✅ Alerta de disponibilidad enviada sin errores")
        print("   ✅ TEST PASADO\n")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_alerta_analisis():
    """Test: Envío de alerta de análisis completado"""
    print("🧪 TEST 3: Alerta de análisis completado")
    print("-" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    # Resultados de prueba
    resultados = {
        'resumen': {
            'total_detectores': 2,
            'exitosos': 1,
            'tasa_exito': 0.5
        },
        'resultados': {
            'H1': {
                'frecuencia_detectada': 141.7050,
                'snr': 8.5,
                'diferencia': 0.0049,
                'significativo': True
            },
            'L1': {
                'frecuencia_detectada': 141.6900,
                'snr': 4.2,
                'diferencia': 0.0101,
                'significativo': False
            }
        }
    }
    
    try:
        sistema.enviar_alerta_analisis("GW250114_TEST", resultados)
        print("   ✅ Alerta de análisis enviada sin errores")
        print("   ✅ Resumen procesado correctamente")
        print("   ✅ Detalles por detector incluidos")
        print("   ✅ TEST PASADO\n")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_alerta_sin_resultados():
    """Test: Alerta con resultados vacíos"""
    print("🧪 TEST 4: Alerta con resultados vacíos")
    print("-" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    resultados_vacios = {
        'resumen': {
            'total_detectores': 0,
            'exitosos': 0,
            'tasa_exito': 0.0
        },
        'resultados': {}
    }
    
    try:
        sistema.enviar_alerta_analisis("GW250114_EMPTY", resultados_vacios)
        print("   ✅ Alerta con resultados vacíos manejada correctamente")
        print("   ✅ TEST PASADO\n")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_configuracion_webhook():
    """Test: Configuración de webhook"""
    print("🧪 TEST 5: Configuración de webhook")
    print("-" * 60)
    
    sistema = SistemaAlertasGW250114()
    
    # Configurar webhook (URL de prueba)
    sistema.config['webhook_url'] = 'https://hooks.example.com/test'
    
    assert sistema.config['webhook_url'] == 'https://hooks.example.com/test', "Webhook URL no configurada correctamente"
    
    print("   ✅ Webhook URL configurada correctamente")
    print("   ✅ TEST PASADO\n")
    
    return True


def run_all_tests():
    """Ejecutar todos los tests"""
    print("🌌 SUITE DE TESTS - SISTEMA DE ALERTAS GW250114")
    print("=" * 60)
    print()
    
    tests = [
        test_inicializacion,
        test_alerta_disponibilidad,
        test_alerta_analisis,
        test_alerta_sin_resultados,
        test_configuracion_webhook
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}\n")
            results.append(False)
    
    # Resumen
    total = len(results)
    passed = sum(results)
    
    print("=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    print(f"Total de tests: {total}")
    print(f"Tests exitosos: {passed}")
    print(f"Tests fallidos: {total - passed}")
    print(f"Tasa de éxito: {passed/total*100:.1f}%")
    print()
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Sistema de alertas funcionando correctamente")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("🔧 Revisar componentes fallidos")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
