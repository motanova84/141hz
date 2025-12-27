#!/usr/bin/env python3
"""
Tests para el módulo de visualizaciones interactivas
"""

import sys
import os
import numpy as np

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_import_visualizaciones():
    """Test 1: Verificar que se puede importar el módulo"""
    print("🧪 TEST 1: Importar módulo de visualizaciones")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        print("   ✅ Módulo importado correctamente")
        return True
    except ImportError as e:
        print(f"   ❌ Error al importar: {e}")
        return False

def test_crear_visualizador():
    """Test 2: Crear instancia del visualizador"""
    print("\n🧪 TEST 2: Crear visualizador")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        
        viz = VisualizadorInteractivo()
        assert viz is not None, "Visualizador no puede ser None"
        assert viz.theme == "plotly_dark", "Tema por defecto debe ser plotly_dark"
        
        print("   ✅ Visualizador creado correctamente")
        print(f"   ✅ Tema: {viz.theme}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_espectro_interactivo():
    """Test 3: Crear espectro interactivo"""
    print("\n🧪 TEST 3: Crear espectro interactivo")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        import plotly.graph_objects as go
        
        viz = VisualizadorInteractivo()
        
        # Datos de prueba
        frecuencias = np.linspace(100, 200, 1000)
        potencias = np.random.lognormal(0, 1, 1000) * 1e-40
        
        fig = viz.crear_espectro_interactivo(
            frecuencias=frecuencias,
            potencias=potencias,
            frecuencia_objetivo=141.7,
            detector="H1",
            snr=8.5
        )
        
        assert isinstance(fig, go.Figure), "Debe retornar una figura de Plotly"
        assert len(fig.data) > 0, "La figura debe tener datos"
        
        print("   ✅ Espectro interactivo creado correctamente")
        print(f"   ✅ Número de trazas: {len(fig.data)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_serie_temporal():
    """Test 4: Crear serie temporal interactiva"""
    print("\n🧪 TEST 4: Crear serie temporal interactiva")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        import plotly.graph_objects as go
        
        viz = VisualizadorInteractivo()
        
        # Datos de prueba
        tiempo = np.linspace(0, 10, 1000)
        datos = np.sin(2 * np.pi * tiempo) * 1e-21
        
        fig = viz.crear_serie_temporal_interactiva(
            tiempo=tiempo,
            datos=datos,
            detector="H1"
        )
        
        assert isinstance(fig, go.Figure), "Debe retornar una figura de Plotly"
        
        print("   ✅ Serie temporal creada correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_grafico_snr():
    """Test 5: Crear gráfico de SNR"""
    print("\n🧪 TEST 5: Crear gráfico de SNR")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        import plotly.graph_objects as go
        
        viz = VisualizadorInteractivo()
        
        eventos = ['GW150914', 'GW151226', 'GW170814']
        snr_valores = [8.5, 6.2, 10.3]
        
        fig = viz.crear_grafico_snr(
            eventos=eventos,
            snr_valores=snr_valores,
            snr_umbral=5.0
        )
        
        assert isinstance(fig, go.Figure), "Debe retornar una figura de Plotly"
        
        print("   ✅ Gráfico de SNR creado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_guardar_html():
    """Test 6: Guardar figura como HTML"""
    print("\n🧪 TEST 6: Guardar figura como HTML")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        
        viz = VisualizadorInteractivo()
        
        # Crear figura simple
        frecuencias = np.linspace(100, 200, 100)
        potencias = np.random.lognormal(0, 1, 100) * 1e-40
        
        fig = viz.crear_espectro_interactivo(
            frecuencias=frecuencias,
            potencias=potencias,
            frecuencia_objetivo=141.7
        )
        
        # Guardar
        import tempfile
        output_path = os.path.join(tempfile.gettempdir(), 'test_espectro.html')
        viz.guardar_html(fig, output_path)
        
        assert os.path.exists(output_path), "Archivo HTML debe existir"
        
        # Verificar contenido
        with open(output_path, 'r') as f:
            content = f.read()
            assert 'plotly' in content.lower(), "HTML debe contener referencia a Plotly"
        
        print(f"   ✅ Archivo guardado: {output_path}")
        print(f"   ✅ Tamaño: {os.path.getsize(output_path)} bytes")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_comparativo():
    """Test 7: Crear dashboard comparativo"""
    print("\n🧪 TEST 7: Crear dashboard comparativo")
    print("-" * 60)
    
    try:
        from visualizaciones_interactivas import VisualizadorInteractivo
        import plotly.graph_objects as go
        
        viz = VisualizadorInteractivo()
        
        # Datos de prueba
        frecuencias = np.linspace(100, 200, 1000)
        potencias_h1 = np.random.lognormal(0, 1, 1000) * 1e-40
        potencias_l1 = np.random.lognormal(0, 1, 1000) * 1e-40
        
        datos_h1 = {'frecuencias': frecuencias, 'potencias': potencias_h1}
        datos_l1 = {'frecuencias': frecuencias, 'potencias': potencias_l1}
        
        fig = viz.crear_dashboard_comparativo(
            datos_h1=datos_h1,
            datos_l1=datos_l1,
            frecuencia_objetivo=141.7
        )
        
        assert isinstance(fig, go.Figure), "Debe retornar una figura de Plotly"
        assert len(fig.data) > 0, "Debe tener múltiples trazas"
        
        print("   ✅ Dashboard comparativo creado correctamente")
        print(f"   ✅ Número de trazas: {len(fig.data)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🔬 TESTS DEL MÓDULO DE VISUALIZACIONES INTERACTIVAS")
    print("=" * 70)
    print()
    
    tests = [
        ("Importar módulo", test_import_visualizaciones),
        ("Crear visualizador", test_crear_visualizador),
        ("Espectro interactivo", test_espectro_interactivo),
        ("Serie temporal", test_serie_temporal),
        ("Gráfico SNR", test_grafico_snr),
        ("Guardar HTML", test_guardar_html),
        ("Dashboard comparativo", test_dashboard_comparativo)
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
