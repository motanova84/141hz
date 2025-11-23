#!/usr/bin/env python3
"""
Script de prueba para el verificador GW250114
"""
import sys
import os
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from verificador_gw250114 import VerificadorGW250114

def test_basic_initialization():
    """Test básico de inicialización"""
    print("🧪 TEST 1: Inicialización básica")
    
    verificador = VerificadorGW250114()
    
    assert verificador.evento_objetivo == "GW250114"
    assert verificador.estado_actual == "DESCONOCIDO"
    assert verificador.data_dir.exists()
    assert verificador.resultados_dir.exists()
    
    print("   ✅ Inicialización correcta")
    print(f"   ✅ Directorio datos: {verificador.data_dir}")
    print(f"   ✅ Directorio resultados: {verificador.resultados_dir}")
    
    return True

def test_generar_resumen():
    """Test de generación de resumen"""
    print("\n🧪 TEST 2: Generación de resumen")
    
    verificador = VerificadorGW250114()
    
    # Crear resultados de prueba
    resultados_test = {
        'H1': {
            'frecuencia_detectada': 141.7001,
            'snr': 7.5,
            'diferencia': 0.0001,
            'significativo': True
        },
        'L1': {
            'frecuencia_detectada': 141.75,
            'snr': 3.2,
            'diferencia': 0.0499,
            'significativo': False
        }
    }
    
    resumen = verificador.generar_resumen(resultados_test)
    
    assert resumen['total_detectores'] == 2
    assert resumen['exitosos'] == 1
    assert resumen['tasa_exito'] == 0.5
    assert 'H1' in resumen['detectores_significativos']
    assert 'L1' not in resumen['detectores_significativos']
    
    print("   ✅ Resumen generado correctamente")
    print(f"   ✅ Detectores significativos: {resumen['detectores_significativos']}")
    print(f"   ✅ Tasa de éxito: {resumen['tasa_exito']}")
    
    return True

def test_guardar_resultados():
    """Test de guardado de resultados"""
    print("\n🧪 TEST 3: Guardado de resultados")
    
    verificador = VerificadorGW250114()
    
    # Crear resultados de prueba
    resultados_test = {
        'H1': {
            'frecuencia_detectada': 141.7001,
            'snr': 7.5,
            'significativo': True
        }
    }
    
    # Guardar resultados
    verificador.guardar_resultados("TEST_EVENT", resultados_test)
    
    # Verificar que el archivo existe
    archivo_esperado = verificador.resultados_dir / "analisis_TEST_EVENT.json"
    assert archivo_esperado.exists()
    
    # Leer y verificar contenido
    import json
    with open(archivo_esperado, 'r') as f:
        datos = json.load(f)
    
    assert datos['evento'] == "TEST_EVENT"
    assert 'timestamp_analisis' in datos
    assert datos['resultados'] == resultados_test
    assert 'resumen' in datos
    
    print("   ✅ Resultados guardados correctamente")
    print(f"   ✅ Archivo: {archivo_esperado}")
    
    # Limpiar archivo de test
    archivo_esperado.unlink()
    
    return True

def main():
    """Ejecutar todos los tests"""
    print("🌌 TEST SUITE - VERIFICADOR GW250114")
    print("=" * 50)
    
    tests = [
        test_basic_initialization,
        test_generar_resumen,
        test_guardar_resultados
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"   ❌ Test falló: {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"   ❌ Error en test {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {passed} pasados, {failed} fallados")
    
    if failed == 0:
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())
