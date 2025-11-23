#!/usr/bin/env python3
"""
Tests para el módulo de generación de informes
"""

import sys
import os
import numpy as np

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_import_generador():
    """Test 1: Verificar que se puede importar el módulo"""
    print("🧪 TEST 1: Importar módulo generador de informes")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        print("   ✅ Módulo importado correctamente")
        return True
    except ImportError as e:
        print(f"   ❌ Error al importar: {e}")
        return False

def test_crear_generador():
    """Test 2: Crear instancia del generador"""
    print("\n🧪 TEST 2: Crear generador de informes")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        
        generador = GeneradorInformes(directorio_salida='/tmp/test_reports')
        assert generador is not None, "Generador no puede ser None"
        assert os.path.exists('/tmp/test_reports'), "Directorio debe existir"
        
        print("   ✅ Generador creado correctamente")
        print(f"   ✅ Directorio: {generador.directorio_salida}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crear_template_base():
    """Test 3: Crear template HTML base"""
    print("\n🧪 TEST 3: Crear template HTML base")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        
        generador = GeneradorInformes(directorio_salida='/tmp/test_reports')
        template_html = generador._crear_template_html_base()
        
        assert template_html is not None, "Template no puede ser None"
        assert len(template_html) > 0, "Template no puede estar vacío"
        assert '<!DOCTYPE html>' in template_html, "Debe ser HTML válido"
        assert 'plotly' in template_html.lower(), "Debe incluir Plotly"
        
        print("   ✅ Template HTML creado correctamente")
        print(f"   ✅ Tamaño: {len(template_html)} caracteres")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_generar_informe_html():
    """Test 4: Generar informe HTML completo"""
    print("\n🧪 TEST 4: Generar informe HTML")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        from visualizaciones_interactivas import VisualizadorInteractivo
        
        # Crear generador
        generador = GeneradorInformes(directorio_salida='/tmp/test_reports')
        
        # Crear visualizaciones
        viz = VisualizadorInteractivo()
        frecuencias = np.linspace(100, 200, 100)
        potencias = np.random.lognormal(0, 1, 100) * 1e-40
        
        fig = viz.crear_espectro_interactivo(
            frecuencias=frecuencias,
            potencias=potencias,
            frecuencia_objetivo=141.7,
            detector="H1",
            snr=8.5
        )
        
        # Datos del informe
        metricas = [
            {'label': 'SNR', 'valor': '8.5', 'unidad': ''},
            {'label': 'Frecuencia', 'valor': '141.7', 'unidad': 'Hz'}
        ]
        
        hallazgos = [
            {
                'tipo': 'info',
                'titulo': 'Detección',
                'descripcion': 'Pico detectado en 141.7 Hz'
            }
        ]
        
        # Generar informe
        ruta = generador.generar_informe_html(
            titulo='Test Informe',
            subtitulo='Informe de prueba',
            metricas_principales=metricas,
            hallazgos=hallazgos,
            graficos=[fig],
            conclusiones='<p>Test exitoso</p>',
            nombre_archivo='test_informe.html'
        )
        
        assert os.path.exists(ruta), "Archivo debe existir"
        
        # Verificar contenido
        with open(ruta, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Test Informe' in content, "Debe contener el título"
            assert 'plotly' in content.lower(), "Debe contener Plotly"
        
        print(f"   ✅ Informe generado: {ruta}")
        print(f"   ✅ Tamaño: {os.path.getsize(ruta)} bytes")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_generar_informe_completo():
    """Test 5: Generar informe completo desde datos"""
    print("\n🧪 TEST 5: Generar informe completo")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        from visualizaciones_interactivas import VisualizadorInteractivo
        
        # Crear visualizaciones
        viz = VisualizadorInteractivo()
        frecuencias = np.linspace(100, 200, 100)
        potencias = np.random.lognormal(0, 1, 100) * 1e-40
        
        fig = viz.crear_espectro_interactivo(
            frecuencias=frecuencias,
            potencias=potencias,
            frecuencia_objetivo=141.7
        )
        
        # Datos del análisis
        datos_analisis = {
            'titulo': 'Test Análisis Completo',
            'subtitulo': 'Prueba de informe completo',
            'metricas': [
                {'label': 'SNR', 'valor': '10.0', 'unidad': ''}
            ],
            'hallazgos': [
                {
                    'tipo': 'info',
                    'titulo': 'Test',
                    'descripcion': 'Hallazgo de prueba'
                }
            ],
            'graficos': [fig],
            'conclusiones': '<p>Conclusiones de prueba</p>'
        }
        
        # Generar
        generador = GeneradorInformes(directorio_salida='/tmp/test_reports')
        archivos = generador.generar_informe_completo(
            datos_analisis=datos_analisis,
            incluir_pdf=False  # No generar PDF en tests
        )
        
        assert 'html' in archivos, "Debe incluir archivo HTML"
        assert os.path.exists(archivos['html']), "HTML debe existir"
        
        print("   ✅ Informe completo generado")
        print(f"   ✅ HTML: {archivos['html']}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tabla_resultados():
    """Test 6: Informe con tabla de resultados"""
    print("\n🧪 TEST 6: Informe con tabla de resultados")
    print("-" * 60)
    
    try:
        from generador_informes import GeneradorInformes
        
        generador = GeneradorInformes(directorio_salida='/tmp/test_reports')
        
        # Tabla de prueba
        tabla = {
            'columnas': ['Evento', 'SNR', 'Frecuencia'],
            'filas': [
                ['GW150914', '8.5', '141.7 Hz'],
                ['GW151226', '6.2', '141.8 Hz']
            ]
        }
        
        ruta = generador.generar_informe_html(
            titulo='Test con Tabla',
            subtitulo='Informe con tabla de resultados',
            metricas_principales=[],
            hallazgos=[],
            graficos=[],
            tabla_resultados=tabla,
            conclusiones='<p>Test de tabla</p>',
            nombre_archivo='test_tabla.html'
        )
        
        assert os.path.exists(ruta), "Archivo debe existir"
        
        with open(ruta, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'GW150914' in content, "Debe contener datos de la tabla"
            assert '<table>' in content, "Debe tener tabla HTML"
        
        print(f"   ✅ Informe con tabla generado: {ruta}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🔬 TESTS DEL MÓDULO DE GENERACIÓN DE INFORMES")
    print("=" * 70)
    print()
    
    tests = [
        ("Importar módulo", test_import_generador),
        ("Crear generador", test_crear_generador),
        ("Template HTML base", test_crear_template_base),
        ("Generar informe HTML", test_generar_informe_html),
        ("Generar informe completo", test_generar_informe_completo),
        ("Tabla de resultados", test_tabla_resultados)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ Error ejecutando test '{nombre}': {e}")
            resultados.append((nombre, False))
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    
    for nombre, resultado in resultados:
        status = "✅ PASADO" if resultado else "❌ FALLADO"
        print(f"{status}: {nombre}")
    
    exitosos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    print(f"\n📈 Resultado: {exitosos}/{total} tests pasados")
    print("=" * 70)
    
    if exitosos == total:
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())
