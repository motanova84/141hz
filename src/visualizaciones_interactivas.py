#!/usr/bin/env python3
"""
Módulo de Visualizaciones Interactivas para Análisis de Ondas Gravitacionales
Utiliza Plotly para crear gráficos interactivos explorables
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Optional
import json


class VisualizadorInteractivo:
    """Clase para generar visualizaciones interactivas de datos de ondas gravitacionales"""
    
    def __init__(self, theme: str = "plotly_dark"):
        """
        Inicializar visualizador
        
        Args:
            theme: Tema de plotly a usar (plotly_dark, plotly_white, etc.)
        """
        self.theme = theme
        self.config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'gw_analysis',
                'height': 1080,
                'width': 1920,
                'scale': 2
            }
        }
    
    def crear_espectro_interactivo(
        self,
        frecuencias: np.ndarray,
        potencias: np.ndarray,
        frecuencia_objetivo: float = 141.7,
        titulo: str = "Espectro de Potencia Interactivo",
        detector: str = "H1",
        snr: Optional[float] = None
    ) -> go.Figure:
        """
        Crear gráfico interactivo del espectro de potencia
        
        Args:
            frecuencias: Array de frecuencias (Hz)
            potencias: Array de potencias
            frecuencia_objetivo: Frecuencia objetivo a destacar
            titulo: Título del gráfico
            detector: Nombre del detector
            snr: Relación señal-ruido (opcional)
        
        Returns:
            Figura de plotly interactiva
        """
        fig = go.Figure()
        
        # Línea principal del espectro
        fig.add_trace(go.Scatter(
            x=frecuencias,
            y=potencias,
            mode='lines',
            name=f'Espectro {detector}',
            line=dict(color='#00d4ff', width=1.5),
            hovertemplate='<b>Frecuencia:</b> %{x:.2f} Hz<br>' +
                         '<b>Potencia:</b> %{y:.2e}<br>' +
                         '<extra></extra>'
        ))
        
        # Línea vertical en la frecuencia objetivo
        fig.add_vline(
            x=frecuencia_objetivo,
            line_dash="dash",
            line_color="red",
            annotation_text=f"{frecuencia_objetivo} Hz",
            annotation_position="top"
        )
        
        # Configuración del layout
        titulo_completo = titulo
        if snr is not None:
            titulo_completo += f" (SNR: {snr:.2f})"
        
        fig.update_layout(
            title=dict(
                text=titulo_completo,
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4ff')
            ),
            xaxis=dict(
                title="Frecuencia (Hz)",
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            yaxis=dict(
                title="Potencia",
                type='log',
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            template=self.theme,
            hovermode='x unified',
            height=600,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
    
    def crear_serie_temporal_interactiva(
        self,
        tiempo: np.ndarray,
        datos: np.ndarray,
        titulo: str = "Serie Temporal",
        detector: str = "H1",
        zoom_inicio: Optional[float] = None,
        zoom_fin: Optional[float] = None
    ) -> go.Figure:
        """
        Crear gráfico interactivo de serie temporal
        
        Args:
            tiempo: Array de tiempo (segundos)
            datos: Array de datos (strain)
            titulo: Título del gráfico
            detector: Nombre del detector
            zoom_inicio: Tiempo inicial para zoom (opcional)
            zoom_fin: Tiempo final para zoom (opcional)
        
        Returns:
            Figura de plotly interactiva
        """
        fig = go.Figure()
        
        # Serie temporal
        fig.add_trace(go.Scatter(
            x=tiempo,
            y=datos,
            mode='lines',
            name=f'Strain {detector}',
            line=dict(color='#4CAF50', width=1),
            hovertemplate='<b>Tiempo:</b> %{x:.4f} s<br>' +
                         '<b>Strain:</b> %{y:.2e}<br>' +
                         '<extra></extra>'
        ))
        
        # Configuración del layout
        xaxis_config = dict(
            title="Tiempo (s)",
            gridcolor='rgba(128,128,128,0.2)',
            showgrid=True
        )
        
        if zoom_inicio is not None and zoom_fin is not None:
            xaxis_config['range'] = [zoom_inicio, zoom_fin]
        
        fig.update_layout(
            title=dict(
                text=titulo,
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4ff')
            ),
            xaxis=xaxis_config,
            yaxis=dict(
                title="Strain",
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            template=self.theme,
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def crear_espectrograma_interactivo(
        self,
        tiempo: np.ndarray,
        frecuencias: np.ndarray,
        potencias_2d: np.ndarray,
        frecuencia_objetivo: float = 141.7,
        titulo: str = "Espectrograma Interactivo"
    ) -> go.Figure:
        """
        Crear espectrograma interactivo
        
        Args:
            tiempo: Array de tiempo
            frecuencias: Array de frecuencias
            potencias_2d: Matriz 2D de potencias (frecuencia x tiempo)
            frecuencia_objetivo: Frecuencia objetivo a destacar
            titulo: Título del gráfico
        
        Returns:
            Figura de plotly interactiva
        """
        fig = go.Figure()
        
        # Convertir a dB
        potencias_db = 10 * np.log10(potencias_2d + 1e-10)
        
        # Heatmap
        fig.add_trace(go.Heatmap(
            x=tiempo,
            y=frecuencias,
            z=potencias_db,
            colorscale='Viridis',
            colorbar=dict(title="Potencia (dB)"),
            hovertemplate='<b>Tiempo:</b> %{x:.2f} s<br>' +
                         '<b>Frecuencia:</b> %{y:.2f} Hz<br>' +
                         '<b>Potencia:</b> %{z:.2f} dB<br>' +
                         '<extra></extra>'
        ))
        
        # Línea horizontal en la frecuencia objetivo
        fig.add_hline(
            y=frecuencia_objetivo,
            line_dash="dash",
            line_color="red",
            annotation_text=f"{frecuencia_objetivo} Hz"
        )
        
        fig.update_layout(
            title=dict(
                text=titulo,
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4ff')
            ),
            xaxis=dict(
                title="Tiempo (s)",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            yaxis=dict(
                title="Frecuencia (Hz)",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            template=self.theme,
            height=600
        )
        
        return fig
    
    def crear_dashboard_comparativo(
        self,
        datos_h1: Dict[str, np.ndarray],
        datos_l1: Dict[str, np.ndarray],
        frecuencia_objetivo: float = 141.7
    ) -> go.Figure:
        """
        Crear dashboard comparativo de múltiples detectores
        
        Args:
            datos_h1: Diccionario con 'frecuencias' y 'potencias' para H1
            datos_l1: Diccionario con 'frecuencias' y 'potencias' para L1
            frecuencia_objetivo: Frecuencia objetivo
        
        Returns:
            Figura de plotly con subplots
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Espectro H1', 'Espectro L1', 
                          'Zoom H1', 'Zoom L1'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Espectro H1
        fig.add_trace(
            go.Scatter(
                x=datos_h1['frecuencias'],
                y=datos_h1['potencias'],
                mode='lines',
                name='H1',
                line=dict(color='#00d4ff'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Espectro L1
        fig.add_trace(
            go.Scatter(
                x=datos_l1['frecuencias'],
                y=datos_l1['potencias'],
                mode='lines',
                name='L1',
                line=dict(color='#ff6b6b'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Zoom H1
        mask_h1 = (datos_h1['frecuencias'] >= 130) & (datos_h1['frecuencias'] <= 160)
        fig.add_trace(
            go.Scatter(
                x=datos_h1['frecuencias'][mask_h1],
                y=datos_h1['potencias'][mask_h1],
                mode='lines',
                name='H1 Zoom',
                line=dict(color='#00d4ff'),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Zoom L1
        mask_l1 = (datos_l1['frecuencias'] >= 130) & (datos_l1['frecuencias'] <= 160)
        fig.add_trace(
            go.Scatter(
                x=datos_l1['frecuencias'][mask_l1],
                y=datos_l1['potencias'][mask_l1],
                mode='lines',
                name='L1 Zoom',
                line=dict(color='#ff6b6b'),
                showlegend=False
            ),
            row=2, col=2
        )
        
        # Agregar líneas verticales para frecuencia objetivo
        for row in [1, 2]:
            for col in [1, 2]:
                fig.add_vline(
                    x=frecuencia_objetivo,
                    line_dash="dash",
                    line_color="red",
                    row=row, col=col
                )
        
        # Configuración de ejes y
        for i in range(1, 5):
            fig.update_yaxes(type='log', row=(i-1)//2+1, col=(i-1)%2+1)
        
        fig.update_layout(
            title=dict(
                text="Comparación Detectores H1 vs L1",
                x=0.5,
                xanchor='center',
                font=dict(size=22, color='#00d4ff')
            ),
            template=self.theme,
            height=900,
            showlegend=False
        )
        
        return fig
    
    def crear_grafico_snr(
        self,
        eventos: list,
        snr_valores: list,
        snr_umbral: float = 5.0,
        titulo: str = "SNR por Evento"
    ) -> go.Figure:
        """
        Crear gráfico de barras interactivo para SNR de múltiples eventos
        
        Args:
            eventos: Lista de nombres de eventos
            snr_valores: Lista de valores SNR
            snr_umbral: Umbral de detección
            titulo: Título del gráfico
        
        Returns:
            Figura de plotly
        """
        # Determinar colores basados en umbral
        colores = ['#4CAF50' if snr >= snr_umbral else '#ff6b6b' 
                   for snr in snr_valores]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=eventos,
            y=snr_valores,
            marker_color=colores,
            text=[f'{snr:.2f}' for snr in snr_valores],
            textposition='outside',
            hovertemplate='<b>Evento:</b> %{x}<br>' +
                         '<b>SNR:</b> %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Línea de umbral
        fig.add_hline(
            y=snr_umbral,
            line_dash="dash",
            line_color="orange",
            annotation_text=f"Umbral: {snr_umbral}",
            annotation_position="right"
        )
        
        fig.update_layout(
            title=dict(
                text=titulo,
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4ff')
            ),
            xaxis=dict(
                title="Eventos",
                gridcolor='rgba(128,128,128,0.2)'
            ),
            yaxis=dict(
                title="SNR",
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True
            ),
            template=self.theme,
            height=600,
            showlegend=False
        )
        
        return fig
    
    def guardar_html(self, fig: go.Figure, ruta: str):
        """
        Guardar figura interactiva como HTML
        
        Args:
            fig: Figura de plotly
            ruta: Ruta donde guardar el archivo
        """
        fig.write_html(ruta, config=self.config)
    
    def guardar_imagen(self, fig: go.Figure, ruta: str, formato: str = 'png'):
        """
        Guardar figura como imagen estática
        
        Args:
            fig: Figura de plotly
            ruta: Ruta donde guardar el archivo
            formato: Formato de imagen (png, jpg, svg, pdf)
        """
        fig.write_image(ruta, format=formato, width=1920, height=1080, scale=2)
    
    def exportar_datos_figura(self, fig: go.Figure, ruta: str):
        """
        Exportar datos de la figura como JSON
        
        Args:
            fig: Figura de plotly
            ruta: Ruta donde guardar el archivo JSON
        """
        with open(ruta, 'w') as f:
            json.dump(fig.to_dict(), f, indent=2)


def crear_ejemplo_visualizacion():
    """Función de ejemplo para demostrar el uso del módulo"""
    # Generar datos de ejemplo
    frecuencias = np.linspace(100, 200, 1000)
    potencias = np.random.lognormal(0, 1, 1000) * 1e-40
    
    # Añadir un pico en 141.7 Hz
    idx_pico = np.argmin(np.abs(frecuencias - 141.7))
    potencias[idx_pico-5:idx_pico+5] *= 10
    
    # Crear visualizador
    viz = VisualizadorInteractivo()
    
    # Crear gráfico
    fig = viz.crear_espectro_interactivo(
        frecuencias=frecuencias,
        potencias=potencias,
        frecuencia_objetivo=141.7,
        titulo="Ejemplo de Espectro Interactivo",
        detector="H1",
        snr=8.5
    )
    
    # Guardar
    viz.guardar_html(fig, '/tmp/ejemplo_espectro.html')
    print("✅ Ejemplo guardado en /tmp/ejemplo_espectro.html")
    
    return fig


if __name__ == "__main__":
    crear_ejemplo_visualizacion()
