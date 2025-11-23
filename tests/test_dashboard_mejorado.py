#!/usr/bin/env python3
"""
Tests para el dashboard mejorado con visualizaciones interactivas
"""

import sys
import os
import json

# Añadir el directorio dashboard al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_import_dashboard_mejorado():
    """Test 1: Verificar que se puede importar el módulo"""
    print("🧪 TEST 1: Importar módulo dashboard mejorado")
    print("-" * 60)
    
    try:
        from dashboard import dashboard_mejorado
        print("   ✅ Módulo importado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error al importar: {e}")
        return False

def test_monitor_analisis_class():
    """Test 2: Verificar la clase MonitorAnalisis"""
    print("\n🧪 TEST 2: Clase MonitorAnalisis")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_mejorado import MonitorAnalisis
        
        monitor = MonitorAnalisis()
        
        # Verificar atributos iniciales
        assert hasattr(monitor, 'metricas_tiempo_real'), "Falta atributo metricas_tiempo_real"
        assert hasattr(monitor, 'estado_sistema'), "Falta atributo estado_sistema"
        assert hasattr(monitor, 'alertas'), "Falta atributo alertas"
        assert hasattr(monitor, 'historial_metricas'), "Falta atributo historial_metricas"
        
        assert monitor.estado_sistema == "OPTIMO", "Estado inicial debe ser OPTIMO"
        assert isinstance(monitor.alertas, list), "Alertas debe ser una lista"
        
        print(f"   ✅ Estado inicial: {monitor.estado_sistema}")
        print(f"   ✅ Alertas iniciales: {len(monitor.alertas)}")
        print(f"   ✅ Atributos verificados correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agregar_alerta():
    """Test 3: Verificar agregar alertas"""
    print("\n🧪 TEST 3: Agregar alertas")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_mejorado import MonitorAnalisis
        
        monitor = MonitorAnalisis()
        
        # Agregar alerta
        monitor.agregar_alerta('deteccion', 'Test alerta', 'info')
        
        assert len(monitor.alertas) == 1, "Debe haber 1 alerta"
        assert monitor.alertas[0]['tipo'] == 'deteccion', "Tipo debe ser 'deteccion'"
        assert monitor.alertas[0]['mensaje'] == 'Test alerta', "Mensaje incorrecto"
        assert monitor.alertas[0]['nivel'] == 'info', "Nivel debe ser 'info'"
        
        print(f"   ✅ Alerta agregada correctamente")
        print(f"   ✅ Total de alertas: {len(monitor.alertas)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_actualizar_metricas():
    """Test 4: Verificar actualización de métricas"""
    print("\n🧪 TEST 4: Actualizar métricas")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_mejorado import MonitorAnalisis
        
        monitor = MonitorAnalisis()
        monitor.actualizar_metricas()
        
        assert 'snr' in monitor.metricas_tiempo_real, "Debe tener métrica SNR"
        assert 'frecuencia' in monitor.metricas_tiempo_real, "Debe tener métrica frecuencia"
        assert 'confianza' in monitor.metricas_tiempo_real, "Debe tener métrica confianza"
        
        assert len(monitor.historial_metricas['snr']) > 0, "Historial SNR debe tener datos"
        
        print(f"   ✅ Métricas actualizadas correctamente")
        print(f"   ✅ SNR: {monitor.metricas_tiempo_real['snr']:.2f}")
        print(f"   ✅ Frecuencia: {monitor.metricas_tiempo_real['frecuencia']:.2f} Hz")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app_mejorado():
    """Test 5: Verificar la aplicación Flask mejorada"""
    print("\n🧪 TEST 5: Aplicación Flask mejorada")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_mejorado import app
        
        # Verificar que es una aplicación Flask
        assert app is not None, "App no puede ser None"
        assert hasattr(app, 'route'), "App debe tener método route"
        
        print("   ✅ Aplicación Flask creada correctamente")
        
        # Verificar rutas
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = [
            '/', 
            '/api/metricas', 
            '/api/alertas',
            '/api/stream',
            '/api/grafico-tiempo-real',
            '/api/estado-sistema',
            '/api/analisis/iniciar',
            '/api/analisis/activos'
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Ruta '{route}' registrada")
            else:
                print(f"   ⚠️  Ruta '{route}' NO encontrada")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints_mejorados():
    """Test 6: Verificar endpoints de la API mejorada"""
    print("\n🧪 TEST 6: Endpoints de la API mejorada")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_mejorado import app
        
        # Crear cliente de prueba
        with app.test_client() as client:
            # Test endpoint principal
            response = client.get('/')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            print("   ✅ GET / - OK (200)")
            
            # Test endpoint métricas
            response = client.get('/api/metricas')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            print("   ✅ GET /api/metricas - OK (200)")
            
            # Test endpoint alertas
            response = client.get('/api/alertas')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            data = json.loads(response.data)
            assert 'alertas' in data, "Falta campo 'alertas'"
            print("   ✅ GET /api/alertas - OK (200)")
            
            # Test endpoint estado sistema
            response = client.get('/api/estado-sistema')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            data = json.loads(response.data)
            assert 'sistema' in data, "Falta campo 'sistema'"
            assert 'plotly_disponible' in data, "Falta campo 'plotly_disponible'"
            print("   ✅ GET /api/estado-sistema - OK (200)")
            print(f"   ✅ Plotly disponible: {data['plotly_disponible']}")
            
            # Test endpoint iniciar análisis
            response = client.post('/api/analisis/iniciar',
                                  json={'evento': 'TEST_GW'},
                                  content_type='application/json')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            data = json.loads(response.data)
            assert 'status' in data, "Falta campo 'status'"
            print("   ✅ POST /api/analisis/iniciar - OK (200)")
            
            # Test endpoint análisis activos
            response = client.get('/api/analisis/activos')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            data = json.loads(response.data)
            assert 'analisis' in data, "Falta campo 'analisis'"
            print("   ✅ GET /api/analisis/activos - OK (200)")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_mejorado_exists():
    """Test 7: Verificar que existe el template HTML mejorado"""
    print("\n🧪 TEST 7: Template HTML mejorado")
    print("-" * 60)
    
    try:
        template_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'dashboard',
            'templates', 
            'dashboard_mejorado.html'
        )
        
        if os.path.exists(template_path):
            print(f"   ✅ Template encontrado: {template_path}")
            
            # Verificar que contiene elementos clave
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            checks = [
                ('Dashboard Mejorado GW250114', 'Título del dashboard'),
                ('plotly', 'Plotly CDN'),
                ('/api/metricas', 'Endpoint de métricas'),
                ('/api/alertas', 'Endpoint de alertas'),
                ('/api/stream', 'Endpoint de stream'),
                ('/api/grafico-tiempo-real', 'Endpoint de gráfico'),
                ('realtime-plot', 'Contenedor de gráfico'),
                ('alertas-panel', 'Panel de alertas'),
                ('iniciarAnalisis', 'Función de control')
            ]
            
            for check_str, description in checks:
                if check_str in content:
                    print(f"   ✅ Contiene: {description}")
                else:
                    print(f"   ⚠️  No contiene: {description}")
            
            return True
        else:
            print(f"   ❌ Template no encontrado: {template_path}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🔬 TESTS DEL DASHBOARD MEJORADO CON VISUALIZACIONES INTERACTIVAS")
    print("=" * 70)
    print()
    
    tests = [
        ("Importar módulo", test_import_dashboard_mejorado),
        ("Clase MonitorAnalisis", test_monitor_analisis_class),
        ("Agregar alertas", test_agregar_alerta),
        ("Actualizar métricas", test_actualizar_metricas),
        ("Aplicación Flask", test_flask_app_mejorado),
        ("Endpoints de la API", test_api_endpoints_mejorados),
        ("Template HTML", test_template_mejorado_exists)
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
