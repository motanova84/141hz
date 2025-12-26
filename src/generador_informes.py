#!/usr/bin/env python3
"""
Módulo de Generación de Informes Automáticos
Genera informes en formato HTML y PDF con gráficos interactivos y resúmenes de hallazgos
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
import plotly.graph_objects as go
import numpy as np


class GeneradorInformes:
    """Clase para generar informes automáticos de análisis de ondas gravitacionales"""
    
    def __init__(self, directorio_salida: str = "reports"):
        """
        Inicializar generador de informes
        
        Args:
            directorio_salida: Directorio donde guardar los informes
        """
        self.directorio_salida = directorio_salida
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Configurar Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(template_dir, exist_ok=True)
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def _crear_template_html_base(self) -> str:
        """Crear template HTML base si no existe"""
        template_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }} - Informe de Análisis</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(26, 31, 58, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
            padding: 40px;
            text-align: center;
            border-bottom: 4px solid #00d4ff;
        }
        
        .header h1 {
            color: #00d4ff;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        }
        
        .header .subtitle {
            color: #b0b0b0;
            font-size: 1.2em;
        }
        
        .header .metadata {
            margin-top: 20px;
            font-size: 0.9em;
            color: #808080;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
            background: rgba(30, 35, 55, 0.6);
            border-radius: 10px;
            padding: 30px;
            border-left: 4px solid #00d4ff;
        }
        
        .section h2 {
            color: #00d4ff;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 2px solid rgba(0, 212, 255, 0.3);
            padding-bottom: 10px;
        }
        
        .section h3 {
            color: #4db8ff;
            font-size: 1.4em;
            margin: 20px 0 15px 0;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: rgba(0, 212, 255, 0.1);
            border: 2px solid #00d4ff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }
        
        .metric-label {
            color: #b0b0b0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .metric-value {
            color: #00d4ff;
            font-size: 2em;
            font-weight: bold;
        }
        
        .metric-unit {
            color: #808080;
            font-size: 0.8em;
        }
        
        .plot-container {
            background: rgba(10, 14, 39, 0.8);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .hallazgos-list {
            list-style: none;
            padding: 0;
        }
        
        .hallazgos-list li {
            background: rgba(76, 175, 80, 0.1);
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .hallazgos-list li.warning {
            background: rgba(255, 152, 0, 0.1);
            border-left-color: #FF9800;
        }
        
        .hallazgos-list li.error {
            background: rgba(244, 67, 54, 0.1);
            border-left-color: #f44336;
        }
        
        .footer {
            background: rgba(10, 14, 39, 0.9);
            padding: 20px;
            text-align: center;
            color: #808080;
            font-size: 0.9em;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        th {
            background: rgba(0, 212, 255, 0.2);
            color: #00d4ff;
            font-weight: bold;
        }
        
        tr:hover {
            background: rgba(0, 212, 255, 0.05);
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .status-success {
            background: rgba(76, 175, 80, 0.3);
            color: #4CAF50;
            border: 1px solid #4CAF50;
        }
        
        .status-warning {
            background: rgba(255, 152, 0, 0.3);
            color: #FF9800;
            border: 1px solid #FF9800;
        }
        
        .status-error {
            background: rgba(244, 67, 54, 0.3);
            color: #f44336;
            border: 1px solid #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ titulo }}</h1>
            <p class="subtitle">{{ subtitulo }}</p>
            <div class="metadata">
                <p>Fecha de generación: {{ fecha }}</p>
                <p>Versión del análisis: {{ version }}</p>
            </div>
        </div>
        
        <div class="content">
            <!-- Resumen Ejecutivo -->
            <div class="section">
                <h2>📊 Resumen Ejecutivo</h2>
                <div class="metrics-grid">
                    {% for metrica in metricas_principales %}
                    <div class="metric-card">
                        <div class="metric-label">{{ metrica.label }}</div>
                        <div class="metric-value">
                            {{ metrica.valor }}
                            <span class="metric-unit">{{ metrica.unidad }}</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Hallazgos Principales -->
            <div class="section">
                <h2>🔍 Hallazgos Principales</h2>
                <ul class="hallazgos-list">
                    {% for hallazgo in hallazgos %}
                    <li class="{{ hallazgo.tipo }}">
                        <strong>{{ hallazgo.titulo }}:</strong> {{ hallazgo.descripcion }}
                    </li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- Gráficos Interactivos -->
            <div class="section">
                <h2>📈 Visualizaciones Interactivas</h2>
                {% for grafico in graficos %}
                <div class="plot-container">
                    <h3>{{ grafico.titulo }}</h3>
                    <div id="{{ grafico.id }}"></div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Tabla de Resultados -->
            {% if tabla_resultados %}
            <div class="section">
                <h2>📋 Tabla de Resultados Detallados</h2>
                <table>
                    <thead>
                        <tr>
                            {% for columna in tabla_resultados.columnas %}
                            <th>{{ columna }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for fila in tabla_resultados.filas %}
                        <tr>
                            {% for valor in fila %}
                            <td>{{ valor }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
            
            <!-- Conclusiones -->
            <div class="section">
                <h2>✅ Conclusiones</h2>
                {{ conclusiones | safe }}
            </div>
        </div>
        
        <div class="footer">
            <p>Informe generado automáticamente por el Sistema de Análisis de Ondas Gravitacionales</p>
            <p>Proyecto 141Hz - Análisis de Componentes Espectrales</p>
        </div>
    </div>
    
    <script>
        // Renderizar gráficos de Plotly
        {% for grafico in graficos %}
        var data_{{ grafico.id }} = {{ grafico.data | safe }};
        var layout_{{ grafico.id }} = {{ grafico.layout | safe }};
        Plotly.newPlot('{{ grafico.id }}', data_{{ grafico.id }}, layout_{{ grafico.id }}, {responsive: true});
        {% endfor %}
    </script>
</body>
</html>
"""
        return template_html
    
    def generar_informe_html(
        self,
        titulo: str,
        subtitulo: str,
        metricas_principales: List[Dict[str, Any]],
        hallazgos: List[Dict[str, str]],
        graficos: List[go.Figure],
        tabla_resultados: Optional[Dict[str, Any]] = None,
        conclusiones: str = "",
        nombre_archivo: Optional[str] = None
    ) -> str:
        """
        Generar informe HTML completo
        
        Args:
            titulo: Título principal del informe
            subtitulo: Subtítulo del informe
            metricas_principales: Lista de métricas clave
            hallazgos: Lista de hallazgos importantes
            graficos: Lista de figuras de plotly
            tabla_resultados: Diccionario con columnas y filas (opcional)
            conclusiones: Texto de conclusiones (HTML)
            nombre_archivo: Nombre del archivo (opcional, se genera automáticamente)
        
        Returns:
            Ruta del archivo generado
        """
        # Generar nombre de archivo si no se proporciona
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"informe_analisis_{timestamp}.html"
        
        ruta_completa = os.path.join(self.directorio_salida, nombre_archivo)
        
        # Preparar datos de gráficos para el template
        graficos_data = []
        for i, fig in enumerate(graficos):
            grafico_id = f"plot_{i}"
            # Convertir figura a JSON usando método de plotly
            fig_json = fig.to_json()
            fig_dict = json.loads(fig_json)
            
            graficos_data.append({
                'id': grafico_id,
                'titulo': fig.layout.title.text if fig.layout.title else f"Gráfico {i+1}",
                'data': json.dumps(fig_dict['data']),
                'layout': json.dumps(fig_dict['layout'])
            })
        
        # Datos del template
        template_data = {
            'titulo': titulo,
            'subtitulo': subtitulo,
            'fecha': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'version': '2.0.0',
            'metricas_principales': metricas_principales,
            'hallazgos': hallazgos,
            'graficos': graficos_data,
            'tabla_resultados': tabla_resultados,
            'conclusiones': conclusiones
        }
        
        # Crear template base si no existe
        template_path = os.path.join(
            os.path.dirname(__file__), 
            'templates', 
            'informe_base.html'
        )
        if not os.path.exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(self._crear_template_html_base())
        
        # Renderizar template
        template = self.env.get_template('informe_base.html')
        html_content = template.render(**template_data)
        
        # Guardar archivo
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Informe HTML generado: {ruta_completa}")
        return ruta_completa
    
    def generar_informe_pdf(
        self,
        html_path: str,
        pdf_path: Optional[str] = None
    ) -> str:
        """
        Generar informe PDF desde HTML
        
        Args:
            html_path: Ruta del archivo HTML
            pdf_path: Ruta del PDF de salida (opcional)
        
        Returns:
            Ruta del archivo PDF generado
        """
        try:
            from weasyprint import HTML, CSS
            
            if pdf_path is None:
                pdf_path = html_path.replace('.html', '.pdf')
            
            # Generar PDF
            HTML(filename=html_path).write_pdf(pdf_path)
            
            print(f"✅ Informe PDF generado: {pdf_path}")
            return pdf_path
        
        except ImportError:
            print("⚠️  WeasyPrint no está instalado. No se puede generar PDF.")
            print("   Instalar con: pip install weasyprint")
            return None
        except Exception as e:
            print(f"❌ Error generando PDF: {e}")
            return None
    
    def generar_informe_completo(
        self,
        datos_analisis: Dict[str, Any],
        incluir_pdf: bool = True
    ) -> Dict[str, str]:
        """
        Generar informe completo (HTML y opcionalmente PDF) desde datos de análisis
        
        Args:
            datos_analisis: Diccionario con todos los datos del análisis
            incluir_pdf: Si se debe generar también la versión PDF
        
        Returns:
            Diccionario con rutas de archivos generados
        """
        # Extraer datos
        titulo = datos_analisis.get('titulo', 'Análisis de Ondas Gravitacionales')
        subtitulo = datos_analisis.get('subtitulo', 'Detección de componente 141.7 Hz')
        
        # Métricas principales
        metricas = datos_analisis.get('metricas', [])
        
        # Hallazgos
        hallazgos = datos_analisis.get('hallazgos', [])
        
        # Gráficos
        graficos = datos_analisis.get('graficos', [])
        
        # Tabla de resultados
        tabla = datos_analisis.get('tabla_resultados', None)
        
        # Conclusiones
        conclusiones = datos_analisis.get('conclusiones', '<p>No se proporcionaron conclusiones.</p>')
        
        # Generar HTML
        html_path = self.generar_informe_html(
            titulo=titulo,
            subtitulo=subtitulo,
            metricas_principales=metricas,
            hallazgos=hallazgos,
            graficos=graficos,
            tabla_resultados=tabla,
            conclusiones=conclusiones
        )
        
        resultados = {'html': html_path}
        
        # Generar PDF si se solicita
        if incluir_pdf:
            pdf_path = self.generar_informe_pdf(html_path)
            if pdf_path:
                resultados['pdf'] = pdf_path
        
        return resultados


class PlotlyJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para objetos de Plotly"""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super().default(obj)


def crear_ejemplo_informe():
    """Función de ejemplo para generar un informe de prueba"""
    from visualizaciones_interactivas import VisualizadorInteractivo
    
    # Crear datos de ejemplo
    frecuencias = np.linspace(100, 200, 1000)
    potencias = np.random.lognormal(0, 1, 1000) * 1e-40
    idx_pico = np.argmin(np.abs(frecuencias - 141.7))
    potencias[idx_pico-5:idx_pico+5] *= 10
    
    # Crear visualizaciones
    viz = VisualizadorInteractivo()
    fig1 = viz.crear_espectro_interactivo(
        frecuencias=frecuencias,
        potencias=potencias,
        frecuencia_objetivo=141.7,
        titulo="Espectro de Potencia H1",
        detector="H1",
        snr=8.5
    )
    
    # Datos del informe
    datos_analisis = {
        'titulo': 'Análisis de GW250114',
        'subtitulo': 'Detección de componente espectral en 141.7 Hz',
        'metricas': [
            {'label': 'Frecuencia Detectada', 'valor': '141.70', 'unidad': 'Hz'},
            {'label': 'SNR', 'valor': '8.5', 'unidad': ''},
            {'label': 'Confianza', 'valor': '95.2', 'unidad': '%'},
            {'label': 'Detectores', 'valor': '2', 'unidad': ''}
        ],
        'hallazgos': [
            {
                'tipo': 'info',
                'titulo': 'Detección Confirmada',
                'descripcion': 'Se detectó un pico espectral significativo en 141.7 Hz con SNR > 5'
            },
            {
                'tipo': 'warning',
                'titulo': 'Coherencia entre detectores',
                'descripcion': 'La señal es coherente entre H1 y L1 con correlación de 0.85'
            }
        ],
        'graficos': [fig1],
        'conclusiones': '<p>El análisis confirma la presencia de una componente espectral en 141.7 Hz consistente con las predicciones teóricas.</p>'
    }
    
    # Generar informe
    generador = GeneradorInformes(directorio_salida='/tmp/informes')
    archivos = generador.generar_informe_completo(datos_analisis, incluir_pdf=False)
    
    print(f"\n✅ Informe de ejemplo generado:")
    for tipo, ruta in archivos.items():
        print(f"   {tipo.upper()}: {ruta}")
    
    return archivos


if __name__ == "__main__":
    crear_ejemplo_informe()
