#!/usr/bin/env python3
"""
Dashboard Mejorado con Visualizaciones Interactivas y Alertas en Tiempo Real
Integra Plotly para gráficos interactivos y sistema de alertas
"""

from flask import Flask, render_template, jsonify, Response, request
import json
import time
import numpy as np
from datetime import datetime
import threading
import os
import sys

# Añadir src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️  Plotly no disponible. Usando gráficos estáticos.")

app = Flask(__name__)

class MonitorAnalisis:
    """Monitor de análisis en tiempo real con alertas"""
    
    def __init__(self):
        self.metricas_tiempo_real = {}
        self.estado_sistema = "OPTIMO"
        self.ultima_actualizacion = time.time()
        self.alertas = []
        self.historial_metricas = {
            'snr': [],
            'frecuencia': [],
            'confianza': [],
            'timestamps': []
        }
        self.analisis_activos = []
        
        # Umbrales de alerta
        self.umbral_snr = 5.0
        self.umbral_frecuencia_min = 141.5
        self.umbral_frecuencia_max = 141.9
        
    def agregar_alerta(self, tipo: str, mensaje: str, nivel: str = "info"):
        """
        Agregar nueva alerta al sistema
        
        Args:
            tipo: Tipo de alerta (deteccion, sistema, calidad)
            mensaje: Mensaje de la alerta
            nivel: Nivel de severidad (info, warning, error)
        """
        alerta = {
            'timestamp': datetime.now().isoformat(),
            'tipo': tipo,
            'mensaje': mensaje,
            'nivel': nivel
        }
        self.alertas.insert(0, alerta)  # Más reciente primero
        
        # Mantener solo las últimas 50 alertas
        if len(self.alertas) > 50:
            self.alertas = self.alertas[:50]
    
    def actualizar_metricas(self):
        """Actualizar métricas en tiempo real"""
        # Simular métricas (en producción, estas vendrían del análisis real)
        snr = float(np.random.uniform(3, 12))
        frecuencia = float(np.random.uniform(141.5, 141.9))
        confianza = float(np.random.uniform(0.7, 0.99))
        
        self.metricas_tiempo_real = {
            'timestamp': datetime.now().isoformat(),
            'snr': snr,
            'frecuencia': frecuencia,
            'confianza': confianza,
            'detectores_activos': 2,
            'eventos_procesados': int(np.random.randint(100, 1000)),
            'cpu_usage': float(np.random.uniform(10, 40)),
            'memory_usage': float(np.random.uniform(40, 70)),
            'latencia_red': float(np.random.uniform(5, 25)),
            'sistema_estado': self.estado_sistema
        }
        
        # Actualizar historial
        self.historial_metricas['snr'].append(snr)
        self.historial_metricas['frecuencia'].append(frecuencia)
        self.historial_metricas['confianza'].append(confianza)
        self.historial_metricas['timestamps'].append(time.time())
        
        # Mantener solo últimos 100 puntos
        for key in ['snr', 'frecuencia', 'confianza', 'timestamps']:
            if len(self.historial_metricas[key]) > 100:
                self.historial_metricas[key] = self.historial_metricas[key][-100:]
        
        # Verificar umbrales y generar alertas
        if snr > self.umbral_snr:
            if np.random.random() > 0.9:  # 10% de probabilidad de alerta
                self.agregar_alerta(
                    'deteccion',
                    f'Detección significativa: SNR={snr:.2f} en f={frecuencia:.2f} Hz',
                    'info'
                )
        
        if frecuencia < self.umbral_frecuencia_min or frecuencia > self.umbral_frecuencia_max:
            if np.random.random() > 0.95:  # 5% de probabilidad
                self.agregar_alerta(
                    'calidad',
                    f'Frecuencia fuera del rango objetivo: {frecuencia:.2f} Hz',
                    'warning'
                )
        
        self.ultima_actualizacion = time.time()
    
    def generar_grafico_tiempo_real(self):
        """Generar gráfico interactivo de métricas en tiempo real"""
        if not PLOTLY_AVAILABLE or len(self.historial_metricas['timestamps']) < 2:
            return None
        
        # Crear timestamps relativos
        timestamps = np.array(self.historial_metricas['timestamps'])
        timestamps_rel = timestamps - timestamps[0]
        
        # Crear gráfico con subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('SNR en Tiempo Real', 'Frecuencia Detectada (Hz)', 'Confianza (%)'),
            vertical_spacing=0.1
        )
        
        # SNR
        fig.add_trace(
            go.Scatter(
                x=timestamps_rel,
                y=self.historial_metricas['snr'],
                mode='lines+markers',
                name='SNR',
                line=dict(color='#00d4ff', width=2)
            ),
            row=1, col=1
        )
        
        # Línea de umbral SNR
        fig.add_hline(
            y=self.umbral_snr,
            line_dash="dash",
            line_color="red",
            row=1, col=1
        )
        
        # Frecuencia
        fig.add_trace(
            go.Scatter(
                x=timestamps_rel,
                y=self.historial_metricas['frecuencia'],
                mode='lines+markers',
                name='Frecuencia',
                line=dict(color='#4CAF50', width=2)
            ),
            row=2, col=1
        )
        
        # Líneas de umbral de frecuencia
        fig.add_hline(
            y=141.7,
            line_dash="dot",
            line_color="yellow",
            row=2, col=1
        )
        
        # Confianza
        fig.add_trace(
            go.Scatter(
                x=timestamps_rel,
                y=np.array(self.historial_metricas['confianza']) * 100,
                mode='lines+markers',
                name='Confianza',
                line=dict(color='#ff6b6b', width=2),
                fill='tozeroy'
            ),
            row=3, col=1
        )
        
        fig.update_xaxes(title_text="Tiempo (s)", row=3, col=1)
        fig.update_yaxes(title_text="SNR", row=1, col=1)
        fig.update_yaxes(title_text="Frecuencia (Hz)", row=2, col=1)
        fig.update_yaxes(title_text="Confianza (%)", row=3, col=1)
        
        fig.update_layout(
            height=800,
            template='plotly_dark',
            showlegend=False,
            title=dict(
                text="Monitoreo en Tiempo Real - GW250114",
                x=0.5,
                xanchor='center'
            )
        )
        
        return fig.to_json()


# Instancia global del monitor
monitor = MonitorAnalisis()

def actualizar_metricas_continuo():
    """Thread para actualizar métricas continuamente"""
    while True:
        monitor.actualizar_metricas()
        time.sleep(2)  # Actualizar cada 2 segundos

@app.route('/')
def dashboard_principal():
    """Página principal del dashboard"""
    return render_template('dashboard_mejorado.html')

@app.route('/api/metricas')
def obtener_metricas():
    """Obtener métricas actuales"""
    return jsonify(monitor.metricas_tiempo_real)

@app.route('/api/alertas')
def obtener_alertas():
    """Obtener alertas recientes"""
    return jsonify({
        'alertas': monitor.alertas,
        'total': len(monitor.alertas)
    })

@app.route('/api/stream')
def stream_metricas():
    """Stream SSE de métricas en tiempo real"""
    def generate():
        while True:
            yield f"data: {json.dumps(monitor.metricas_tiempo_real)}\n\n"
            time.sleep(2)
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/grafico-tiempo-real')
def grafico_tiempo_real():
    """Obtener gráfico de tiempo real en formato JSON"""
    grafico_json = monitor.generar_grafico_tiempo_real()
    if grafico_json:
        return Response(grafico_json, mimetype='application/json')
    else:
        return jsonify({'error': 'No hay datos suficientes o Plotly no disponible'}), 503

@app.route('/api/estado-sistema')
def estado_sistema():
    """Obtener estado completo del sistema"""
    return jsonify({
        'sistema': 'Monitor Avanzado GW250114 con Visualizaciones Interactivas',
        'version': '3.0.0',
        'estado': monitor.estado_sistema,
        'ultima_actualizacion': datetime.now().isoformat(),
        'plotly_disponible': PLOTLY_AVAILABLE,
        'metricas': monitor.metricas_tiempo_real,
        'alertas_recientes': len(monitor.alertas),
        'umbrales': {
            'snr': monitor.umbral_snr,
            'frecuencia_min': monitor.umbral_frecuencia_min,
            'frecuencia_max': monitor.umbral_frecuencia_max
        }
    })

@app.route('/api/analisis/iniciar', methods=['POST'])
def iniciar_analisis():
    """Endpoint para iniciar un nuevo análisis"""
    data = request.get_json()
    
    # Validar entrada
    if not data:
        return jsonify({'status': 'error', 'mensaje': 'No se proporcionaron datos'}), 400
    
    evento = data.get('evento', 'GW_UNKNOWN')
    
    # Validar evento (solo caracteres alfanuméricos y guiones bajos)
    import re
    if not re.match(r'^[A-Za-z0-9_-]+$', evento):
        return jsonify({'status': 'error', 'mensaje': 'Nombre de evento inválido'}), 400
    
    analisis_id = f"ANALISIS_{int(time.time())}"
    monitor.analisis_activos.append({
        'id': analisis_id,
        'evento': evento,
        'inicio': datetime.now().isoformat(),
        'estado': 'EJECUTANDO'
    })
    
    monitor.agregar_alerta(
        'sistema',
        f'Análisis iniciado: {evento} (ID: {analisis_id})',
        'info'
    )
    
    return jsonify({
        'status': 'success',
        'analisis_id': analisis_id,
        'mensaje': f'Análisis iniciado para {evento}'
    })

@app.route('/api/analisis/activos')
def analisis_activos():
    """Obtener lista de análisis activos"""
    return jsonify({
        'analisis': monitor.analisis_activos,
        'total': len(monitor.analisis_activos)
    })

# Iniciar thread de actualización de métricas
thread = threading.Thread(target=actualizar_metricas_continuo, daemon=True)
thread.start()

if __name__ == '__main__':
    print("=" * 70)
    print("🌌 Dashboard Mejorado con Visualizaciones Interactivas")
    print("=" * 70)
    print(f"📊 Plotly disponible: {'✅ Sí' if PLOTLY_AVAILABLE else '❌ No'}")
    print("🌐 Acceder a: http://localhost:5000")
    print("📡 API endpoints disponibles:")
    print("   - GET  /api/metricas          : Métricas actuales")
    print("   - GET  /api/alertas           : Alertas recientes")
    print("   - GET  /api/stream            : Stream en tiempo real (SSE)")
    print("   - GET  /api/grafico-tiempo-real : Gráfico interactivo")
    print("   - GET  /api/estado-sistema    : Estado completo")
    print("   - POST /api/analisis/iniciar  : Iniciar análisis")
    print("   - GET  /api/analisis/activos  : Análisis activos")
    print("=" * 70)
    print("\n⚠️  NOTA DE SEGURIDAD:")
    print("   El servidor está configurado para escuchar en 0.0.0.0 (todas las interfaces)")
    print("   Para uso en producción, considere:")
    print("   - Usar host='127.0.0.1' para acceso solo local")
    print("   - Implementar autenticación y autorización")
    print("   - Usar HTTPS con certificados SSL/TLS")
    print("=" * 70)
    
    # Solo debug en desarrollo
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    # Para producción, considerar usar host='127.0.0.1' o implementar autenticación
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    app.run(debug=debug_mode, host=host, port=5000, threaded=True)
