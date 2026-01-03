#!/usr/bin/env python3
"""
Test unitario para analisis_cmb_l144.py
Verifica el funcionamiento del análisis CMB
"""
import sys
import os
import numpy as np

# Agregar directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_analisis_cmb_inicializacion():
    """Test: Inicialización de AnalisisCMB"""
    print("🧪 Test 1: Inicialización de AnalisisCMB")
    
    try:
        from analisis_cmb_l144 import AnalisisCMB
        
        analisis = AnalisisCMB()
        
        # Verificar atributos
        assert analisis.l_max == 300, "l_max debe ser 300"
        assert analisis.l_objetivo == 144, "l_objetivo debe ser 144"
        
        print("   ✅ Test PASSED - Inicialización correcta")
        return True
    except Exception as e:
        print(f"   ❌ Test FAILED - {e}")
        return False

def test_simular_espectro_cmb():
    """Test: Simulación de espectro CMB"""
    print("\n🧪 Test 2: Simulación de espectro CMB")
    
    try:
        from analisis_cmb_l144 import AnalisisCMB
        
        analisis = AnalisisCMB()
        espectro = analisis.simular_espectro_cmb()
        
        # Verificar características del espectro
        assert len(espectro) == analisis.l_max + 1, f"Longitud del espectro debe ser {analisis.l_max + 1}"
        assert np.all(espectro >= 0), "Todos los valores del espectro deben ser positivos"
        assert espectro[144] > espectro[50], "Debe haber anomalía en l=144"
        
        print(f"   Longitud del espectro: {len(espectro)}")
        print(f"   Valor en l=144: {espectro[144]:.6e}")
        print(f"   Valor máximo: {np.max(espectro):.6e}")
        print("   ✅ Test PASSED - Simulación correcta")
        return True
    except Exception as e:
        print(f"   ❌ Test FAILED - {e}")
        return False

def test_buscar_anomalia_l144():
    """Test: Búsqueda de anomalía en l=144"""
    print("\n🧪 Test 3: Búsqueda de anomalía en l=144")
    
    try:
        from analisis_cmb_l144 import AnalisisCMB
        
        analisis = AnalisisCMB()
        espectro = analisis.simular_espectro_cmb()
        resultados = analisis.buscar_anomalia_l144(espectro)
        
        # Verificar resultados
        assert 'l_pico' in resultados, "Debe contener 'l_pico'"
        assert 'amplitud_pico' in resultados, "Debe contener 'amplitud_pico'"
        assert 'ancho_pico' in resultados, "Debe contener 'ancho_pico'"
        assert 'diferencia_l' in resultados, "Debe contener 'diferencia_l'"
        assert 'significativo' in resultados, "Debe contener 'significativo'"
        
        # Con datos simulados, debería detectar el pico cerca de 144
        if resultados['l_pico'] is not None:
            assert abs(resultados['l_pico'] - 144) < 5, "El pico detectado debe estar cerca de l=144"
            print(f"   l del pico detectado: {resultados['l_pico']:.2f}")
            print(f"   Diferencia con l=144: {resultados['diferencia_l']:.2f}")
            print(f"   Anomalía significativa: {resultados['significativo']}")
        
        print("   ✅ Test PASSED - Búsqueda de anomalía funciona")
        return True
    except Exception as e:
        print(f"   ❌ Test FAILED - {e}")
        return False

def test_cargar_datos_planck():
    """Test: Carga de datos Planck (usando simulación)"""
    print("\n🧪 Test 4: Carga de datos Planck")
    
    try:
        from analisis_cmb_l144 import AnalisisCMB
        
        analisis = AnalisisCMB()
        espectro = analisis.cargar_datos_planck()
        
        # Verificar que devuelve un array válido
        assert espectro is not None, "Debe devolver un espectro"
        assert len(espectro) > 0, "El espectro no debe estar vacío"
        
        print(f"   Espectro cargado con {len(espectro)} elementos")
        print("   ✅ Test PASSED - Carga de datos funciona (simulación)")
        return True
    except Exception as e:
        print(f"   ❌ Test FAILED - {e}")
        return False

def test_ejecutar_analisis_completo():
    """Test: Ejecución completa del análisis"""
    print("\n🧪 Test 5: Análisis completo")
    
    try:
        from analisis_cmb_l144 import AnalisisCMB
        
        analisis = AnalisisCMB()
        resultados = analisis.ejecutar_analisis_completo()
        
        # Verificar que devuelve resultados
        assert resultados is not None, "Debe devolver resultados"
        assert isinstance(resultados, dict), "Los resultados deben ser un diccionario"
        
        print("   ✅ Test PASSED - Análisis completo funciona")
        return True
    except Exception as e:
        print(f"   ❌ Test FAILED - {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("Test de Validación de analisis_cmb_l144.py")
    print("=" * 70)
    
    tests = [
        test_analisis_cmb_inicializacion,
        test_simular_espectro_cmb,
        test_buscar_anomalia_l144,
        test_cargar_datos_planck,
        test_ejecutar_analisis_completo
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} tests pasados")
    
    if all(results):
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())
