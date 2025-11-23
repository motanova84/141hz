#!/usr/bin/env python3
"""
Ejemplo de uso del módulo de visualizaciones interactivas y generación de informes
Demuestra cómo crear gráficos interactivos e informes automáticos para análisis de ondas gravitacionales
"""

import sys
import os
import numpy as np

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from visualizaciones_interactivas import VisualizadorInteractivo
from generador_informes import GeneradorInformes


def generar_datos_ejemplo():
    """Generar datos de ejemplo para demostración"""
    print("📊 Generando datos de ejemplo...")
    
    # Espectro de frecuencias
    frecuencias = np.linspace(100, 200, 2000)
    potencias_h1 = np.random.lognormal(0, 1, 2000) * 1e-40
    potencias_l1 = np.random.lognormal(0, 1, 2000) * 1e-40
    
    # Añadir pico en 141.7 Hz
    idx_pico = np.argmin(np.abs(frecuencias - 141.7))
    potencias_h1[idx_pico-10:idx_pico+10] *= 15
    potencias_l1[idx_pico-10:idx_pico+10] *= 12
    
    # Serie temporal
    tiempo = np.linspace(0, 4, 16384)
    strain_h1 = np.sin(2 * np.pi * 141.7 * tiempo) * 1e-21
    strain_h1 += np.random.normal(0, 5e-22, len(tiempo))
    
    return {
        'frecuencias': frecuencias,
        'potencias_h1': potencias_h1,
        'potencias_l1': potencias_l1,
        'tiempo': tiempo,
        'strain_h1': strain_h1
    }


def ejemplo_visualizaciones_interactivas():
    """Ejemplo 1: Crear visualizaciones interactivas"""
    print("\n" + "=" * 70)
    print("📈 EJEMPLO 1: Visualizaciones Interactivas")
    print("=" * 70)
    
    # Generar datos
    datos = generar_datos_ejemplo()
    
    # Crear visualizador
    viz = VisualizadorInteractivo(theme="plotly_dark")
    
    # 1. Espectro de potencia interactivo
    print("\n1️⃣  Creando espectro de potencia interactivo...")
    fig_espectro = viz.crear_espectro_interactivo(
        frecuencias=datos['frecuencias'],
        potencias=datos['potencias_h1'],
        frecuencia_objetivo=141.7,
        titulo="Espectro de Potencia H1 - GW250114",
        detector="H1",
        snr=10.5
    )
    
    # Guardar como HTML
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    viz.guardar_html(fig_espectro, os.path.join(output_dir, 'espectro_interactivo.html'))
    print(f"   ✅ Guardado: {output_dir}/espectro_interactivo.html")
    
    # 2. Serie temporal interactiva
    print("\n2️⃣  Creando serie temporal interactiva...")
    fig_temporal = viz.crear_serie_temporal_interactiva(
        tiempo=datos['tiempo'],
        datos=datos['strain_h1'],
        titulo="Serie Temporal H1 - Zoom en Ringdown",
        detector="H1"
    )
    viz.guardar_html(fig_temporal, os.path.join(output_dir, 'serie_temporal_interactiva.html'))
    print(f"   ✅ Guardado: {output_dir}/serie_temporal_interactiva.html")
    
    # 3. Dashboard comparativo
    print("\n3️⃣  Creando dashboard comparativo H1 vs L1...")
    fig_comparativo = viz.crear_dashboard_comparativo(
        datos_h1={'frecuencias': datos['frecuencias'], 'potencias': datos['potencias_h1']},
        datos_l1={'frecuencias': datos['frecuencias'], 'potencias': datos['potencias_l1']},
        frecuencia_objetivo=141.7
    )
    viz.guardar_html(fig_comparativo, os.path.join(output_dir, 'dashboard_comparativo.html'))
    print(f"   ✅ Guardado: {output_dir}/dashboard_comparativo.html")
    
    # 4. Gráfico de SNR para múltiples eventos
    print("\n4️⃣  Creando gráfico de SNR...")
    eventos = ['GW150914', 'GW151226', 'GW170814', 'GW200129', 'GW250114']
    snr_valores = [8.5, 6.2, 10.3, 7.8, 10.5]
    
    fig_snr = viz.crear_grafico_snr(
        eventos=eventos,
        snr_valores=snr_valores,
        snr_umbral=5.0,
        titulo="SNR de Eventos con Componente 141.7 Hz"
    )
    viz.guardar_html(fig_snr, os.path.join(output_dir, 'snr_eventos.html'))
    print(f"   ✅ Guardado: {output_dir}/snr_eventos.html")
    
    print("\n✅ Todas las visualizaciones interactivas creadas exitosamente")
    return [fig_espectro, fig_temporal, fig_comparativo, fig_snr]


def ejemplo_generacion_informes(figuras):
    """Ejemplo 2: Generar informes automáticos"""
    print("\n" + "=" * 70)
    print("📄 EJEMPLO 2: Generación de Informes Automáticos")
    print("=" * 70)
    
    # Crear generador de informes
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'reports')
    generador = GeneradorInformes(directorio_salida=output_dir)
    
    # Preparar datos del informe
    datos_analisis = {
        'titulo': 'Análisis de GW250114',
        'subtitulo': 'Detección de Componente Espectral en 141.7 Hz',
        'metricas': [
            {'label': 'Frecuencia Detectada', 'valor': '141.70', 'unidad': 'Hz'},
            {'label': 'SNR H1', 'valor': '10.5', 'unidad': ''},
            {'label': 'SNR L1', 'valor': '9.8', 'unidad': ''},
            {'label': 'Confianza', 'valor': '99.2', 'unidad': '%'},
            {'label': 'Coherencia H1-L1', 'valor': '0.92', 'unidad': ''},
            {'label': 'Detectores Activos', 'valor': '2', 'unidad': ''}
        ],
        'hallazgos': [
            {
                'tipo': 'info',
                'titulo': 'Detección Confirmada',
                'descripcion': 'Se detectó un pico espectral significativo en 141.70 Hz con SNR > 5 en ambos detectores'
            },
            {
                'tipo': 'info',
                'titulo': 'Coherencia entre Detectores',
                'descripcion': 'La señal es coherente entre H1 y L1 con correlación de 0.92'
            }
        ],
        'graficos': figuras,
        'tabla_resultados': {
            'columnas': ['Detector', 'SNR', 'Frecuencia (Hz)', 'Confianza'],
            'filas': [
                ['H1', '10.5', '141.70 ± 0.01', '99.5%'],
                ['L1', '9.8', '141.69 ± 0.01', '98.9%']
            ]
        },
        'conclusiones': '<p>El análisis confirma la presencia de una componente espectral en 141.7 Hz en el evento GW250114.</p>'
    }
    
    print("\n1️⃣  Generando informe HTML completo...")
    archivos = generador.generar_informe_completo(
        datos_analisis=datos_analisis,
        incluir_pdf=False
    )
    
    print(f"   ✅ Informe HTML: {archivos['html']}")
    print("\n✅ Informe generado exitosamente")
    return archivos


def ejemplo_dashboard_uso():
    """Ejemplo 3: Información sobre el uso del dashboard"""
    print("\n" + "=" * 70)
    print("🌐 EJEMPLO 3: Dashboard Web en Tiempo Real")
    print("=" * 70)
    
    print("\nPara iniciar el dashboard mejorado:")
    print("\n   $ cd dashboard")
    print("   $ python3 dashboard_mejorado.py")
    print("\nLuego abrir: http://localhost:5000")
    
    print("\n📊 Características:")
    print("   • Visualizaciones interactivas con Plotly")
    print("   • Monitoreo en tiempo real")
    print("   • Sistema de alertas automáticas")
    print("   • API REST completa")


def main():
    """Ejecutar todos los ejemplos"""
    print("=" * 70)
    print("🚀 EJEMPLOS DE USO: Visualizaciones Interactivas e Informes")
    print("=" * 70)
    
    try:
        figuras = ejemplo_visualizaciones_interactivas()
        ejemplo_generacion_informes(figuras)
        ejemplo_dashboard_uso()
        
        print("\n" + "=" * 70)
        print("✅ TODOS LOS EJEMPLOS EJECUTADOS EXITOSAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
