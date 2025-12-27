#!/usr/bin/env python3
# dashboard/estado_gw250114.py
from flask import Flask, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/estado-gw250114')
def estado_gw250114():
    """Endpoint para estado de GW250114"""
    
    estado = {
        'evento': 'GW250114',
        'ultima_verificacion': datetime.now().isoformat(),
        'disponible': False,
        'estado': 'NO_DISPONIBLE',
        'mensaje': 'Esperando publicación en GWOSC',
        'eventos_similares': [],
        'timestamp': datetime.now().timestamp()
    }
    
    # Verificar si hay resultados de análisis
    # Intentar diferentes rutas relativas
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resultados', 'analisis_GW250114.json')
    ]
    
    for results_path in possible_paths:
        if os.path.exists(results_path):
            with open(results_path, 'r') as f:
                datos_analisis = json.load(f)
                estado.update({
                    'disponible': True,
                    'estado': 'ANALIZADO',
                    'resultados': datos_analisis
                })
            break
    
    return jsonify(estado)

@app.route('/monitor-gw')
def monitor_gw():
    """Página de monitoreo de eventos GW"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monitor GW250114 - Teoría Ψ</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #0f0f23; color: white; }
            .estado { padding: 20px; border-radius: 10px; margin: 10px 0; }
            .disponible { background: #2ecc71; color: white; }
            .no-disponible { background: #e74c3c; color: white; }
            .monitoreo { background: #f39c12; color: white; }
        </style>
    </head>
    <body>
        <h1>🌌 Monitor GW250114 - Validación Teoría Ψ</h1>
        <div id="estado">Cargando...</div>
        
        <script>
            async function actualizarEstado() {
                const respuesta = await fetch('/estado-gw250114');
                const datos = await respuesta.json();
                
                let html = '';
                if (datos.disponible) {
                    html = `<div class="estado disponible">
                        <h2>🎯 GW250114 DISPONIBLE</h2>
                        <p>¡El evento está disponible para análisis!</p>
                        <p><strong>Última verificación:</strong> ${new Date(datos.ultima_verificacion).toLocaleString()}</p>
                    </div>`;
                } else {
                    html = `<div class="estado no-disponible">
                        <h2>⏳ GW250114 NO DISPONIBLE</h2>
                        <p>Esperando publicación en GWOSC...</p>
                        <p><strong>Última verificación:</strong> ${new Date(datos.ultima_verificacion).toLocaleString()}</p>
                        <p>El sistema verifica automáticamente cada 30 minutos</p>
                    </div>`;
                }
                
                document.getElementById('estado').innerHTML = html;
            }
            
            actualizarEstado();
            setInterval(actualizarEstado, 30000); // Actualizar cada 30 segundos
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # WARNING: Do not use debug=True in production. This configuration is for development only.
    app.run(debug=False, host='0.0.0.0', port=5000)
