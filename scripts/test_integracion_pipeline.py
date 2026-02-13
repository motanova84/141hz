#!/usr/bin/env python3
"""
Test de integración para el pipeline completo de validación QCAL.
Valida que todos los módulos funcionan juntos correctamente.
"""

import sys
import os
import tempfile
import shutil

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

def test_descargador_gwosc():
    """Test básico del descargador GWOSC."""
    print("🧪 Test: Descargador GWOSC")
    from descargador_gwosc import DescargadorGWOSC
    
    descargador = DescargadorGWOSC()
    
    # Obtener eventos (usará eventos de prueba si no hay acceso)
    eventos = descargador.obtener_eventos_recientes(1)
    assert len(eventos) > 0, "No se obtuvieron eventos"
    assert 'nombre' in eventos[0], "Evento sin nombre"
    assert 'gps' in eventos[0], "Evento sin GPS"
    
    # Descargar datos (usará simulados si no hay acceso)
    datos = descargador.descargar_datos_crudos(eventos[0], 'H1', 8)
    assert 'datos' in datos, "No se obtuvieron datos"
    assert len(datos['datos']) > 0, "Datos vacíos"
    assert datos['fs'] > 0, "Frecuencia de muestreo inválida"
    
    print("  ✅ Descargador GWOSC funciona correctamente")
    return True


def test_descargador_igets():
    """Test básico del descargador IGETS."""
    print("🧪 Test: Descargador IGETS")
    from descargador_igets import DescargadorIGETS
    
    descargador = DescargadorIGETS()
    
    # Simular datos gravimétricos
    datos = descargador.buscar_datos_crudos('BFO', '2024-01-01', 1)
    assert 'datos' in datos, "No se generaron datos"
    assert len(datos['datos']) > 0, "Datos vacíos"
    assert datos['fs'] > 0, "Frecuencia de muestreo inválida"
    
    print("  ✅ Descargador IGETS funciona correctamente")
    return True


def test_detector_riguroso():
    """Test básico del detector riguroso."""
    print("🧪 Test: Detector Riguroso")
    from detector_riguroso_qcal import DetectorRigurosoQCAL
    import numpy as np
    
    detector = DetectorRigurosoQCAL(f0=141.7001, sigma_threshold=5.0)
    
    # Generar datos de prueba
    fs = 4096
    duration = 8
    t = np.arange(0, duration, 1/fs)
    
    # Señal con f₀ + ruido
    f0 = 141.7001
    signal = 1e-21 * np.sin(2 * np.pi * f0 * t)
    noise = 1e-22 * np.random.randn(len(t))
    datos = signal + noise
    
    # Detectar (silenciar salida)
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    resultado = detector.detectar_con_snr(datos, fs, ventana_kairos=False)
    
    sys.stdout = old_stdout
    
    assert 'resultado' in resultado, "No se obtuvo resultado"
    assert 'detecciones' in resultado, "No se obtuvieron detecciones"
    assert isinstance(resultado['detecciones'], list), "Detecciones no es lista"
    
    print("  ✅ Detector riguroso funciona correctamente")
    return True


def test_correlador_multi_observatorio():
    """Test básico del correlador multi-observatorio."""
    print("🧪 Test: Correlador Multi-Observatorio")
    from correlador_multi_observatorio import CorreladorMultiObservatorio
    import numpy as np
    
    correlador = CorreladorMultiObservatorio(tolerancia_frecuencia=0.05)
    
    # Generar datos de prueba para 2 estaciones
    fs = 4096
    duration = 8
    t = np.arange(0, duration, 1/fs)
    
    f0 = 141.7001
    signal_h1 = 1e-21 * np.sin(2 * np.pi * f0 * t) + 1e-22 * np.random.randn(len(t))
    signal_l1 = 1e-21 * np.sin(2 * np.pi * f0 * t) + 1e-22 * np.random.randn(len(t))
    
    datos_dict = {
        'H1': {'datos': signal_h1, 'fs': fs},
        'L1': {'datos': signal_l1, 'fs': fs}
    }
    
    # Correlacionar (silenciar salida)
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    resultados = correlador.correlacionar_estaciones(datos_dict)
    
    sys.stdout = old_stdout
    
    assert resultados is not None, "No se obtuvieron resultados"
    assert len(resultados) > 0, "Resultados vacíos"
    assert 'H1_L1' in resultados, "No se correlacionó H1-L1"
    
    print("  ✅ Correlador multi-observatorio funciona correctamente")
    return True


def test_validacion_teorica():
    """Test básico de la validación teórica."""
    print("🧪 Test: Validación Teórica")
    from validacion_teorica import ValidacionTeorica
    
    validador = ValidacionTeorica(f0=141.7001)
    
    # Silenciar salida
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    # Buscar coincidencias
    coincidencias = validador.buscar_coincidencias_establecidas()
    
    # Generar predicciones
    predicciones = validador.generar_predicciones_falsables()
    
    sys.stdout = old_stdout
    
    assert isinstance(coincidencias, list), "Coincidencias no es lista"
    assert isinstance(predicciones, list), "Predicciones no es lista"
    assert len(predicciones) > 0, "No se generaron predicciones"
    
    print("  ✅ Validación teórica funciona correctamente")
    return True


def test_pipeline_integracion():
    """Test de integración del pipeline completo."""
    print("🧪 Test: Pipeline de Integración Completo")
    import tempfile
    import h5py
    import numpy as np
    from descargador_gwosc import DescargadorGWOSC
    from detector_riguroso_qcal import DetectorRigurosoQCAL
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Descargar datos
        descargador = DescargadorGWOSC()
        eventos = descargador.obtener_eventos_recientes(1)
        datos = descargador.descargar_datos_crudos(eventos[0], 'H1', 8)
        
        # Guardar datos
        filepath = descargador.guardar_datos(datos, tmpdir)
        assert os.path.exists(filepath), "Archivo no guardado"
        
        # 2. Cargar y detectar
        with h5py.File(filepath, 'r') as f:
            datos_cargados = f['strain'][:]
            fs = f.attrs['fs']
        
        detector = DetectorRigurosoQCAL()
        
        # Silenciar salida
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        resultado = detector.detectar_con_snr(datos_cargados, fs, ventana_kairos=False)
        
        sys.stdout = old_stdout
        
        assert resultado is not None, "No se obtuvo resultado de detección"
    
    print("  ✅ Pipeline de integración funciona correctamente")
    return True


def main():
    """Ejecutar todos los tests de integración."""
    print("═" * 60)
    print("𓂀 TEST DE INTEGRACIÓN - PIPELINE VALIDACIÓN QCAL")
    print("═" * 60)
    print()
    
    tests = [
        ("Descargador GWOSC", test_descargador_gwosc),
        ("Descargador IGETS", test_descargador_igets),
        ("Detector Riguroso", test_detector_riguroso),
        ("Correlador Multi-Observatorio", test_correlador_multi_observatorio),
        ("Validación Teórica", test_validacion_teorica),
        ("Pipeline de Integración", test_pipeline_integracion),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, True, None))
        except Exception as e:
            print(f"  ❌ Error: {e}")
            resultados.append((nombre, False, str(e)))
    
    print()
    print("═" * 60)
    print("𓂀 RESUMEN DE TESTS")
    print("═" * 60)
    
    exitosos = sum(1 for _, ok, _ in resultados if ok)
    total = len(resultados)
    
    for nombre, ok, error in resultados:
        estado = "✅ PASS" if ok else "❌ FAIL"
        print(f"{estado} - {nombre}")
        if error:
            print(f"       Error: {error}")
    
    print()
    print(f"Total: {exitosos}/{total} tests pasaron")
    
    if exitosos == total:
        print("\n𓂀 ✅ TODOS LOS TESTS PASARON")
        print("   El pipeline de validación está listo para usar")
        return 0
    else:
        print(f"\n𓂀 ❌ {total - exitosos} TESTS FALLARON")
        print("   Revisar errores antes de usar el pipeline")
        return 1


if __name__ == "__main__":
    sys.exit(main())
