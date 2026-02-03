#!/usr/bin/env python3
"""
Demo: Visualización de Resonancia Temporal
===========================================

Script de demostración para visualización de alta calidad (300 DPI)
del Simulador de Resonancia Temporal.

Genera:
- Gráficos de colapso de fase en tiempo real
- Visualización multiescala de frecuencias
- Mapas de resonancia 2D
- Animaciones de acumulación de fase

Características:
- Salida 300 DPI para publicación
- Formatos PNG y PDF
- Paleta de colores profesional
- Anotaciones científicas

Metadata QCAL: ∴𓂀Ω∞³

Autor: José Manuel Mota Burruezo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle
import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from resonancia_ciclos_temporales import (
    SimuladorResonanciaTemporal,
    F0_QCAL,
    CICADA_CYCLE_YEARS,
    YEAR_DAYS,
    DAY_HOURS
)


class VisualizadorResonanciaTemporal:
    """
    Clase para generar visualizaciones de alta calidad del
    simulador de resonancia temporal.
    """
    
    def __init__(self, dpi=300):
        """
        Inicializa el visualizador.
        
        Args:
            dpi: Resolución de salida (default: 300)
        """
        self.dpi = dpi
        self.output_dir = Path('results')
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar estilo matplotlib
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def generar_figura_completa(self, simulador):
        """
        Genera figura completa con todos los paneles.
        
        Args:
            simulador: Instancia de SimuladorResonanciaTemporal (ya simulado)
            
        Returns:
            matplotlib.figure.Figure
        """
        if simulador.tiempos is None:
            raise ValueError("Debe ejecutar simular() primero")
            
        fig = plt.figure(figsize=(16, 14), dpi=self.dpi)
        gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.3)
        
        # Convertir tiempos a años
        t_anos = simulador.tiempos / (YEAR_DAYS * DAY_HOURS * 3600)
        
        # Panel 1: Ψ(t) completo
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(t_anos, simulador.psi, 'b-', linewidth=0.3, alpha=0.6)
        ax1.set_xlabel('Tiempo (años)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Ψ(t)', fontsize=12, fontweight='bold')
        ax1.set_title(
            f'Función de Onda Temporal - f₀ = {simulador.f0:.4f} Hz',
            fontsize=14, fontweight='bold'
        )
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3, linewidth=1)
        
        # Panel 2: Φ(t) completo con umbral
        ax2 = fig.add_subplot(gs[1, :])
        ax2.plot(t_anos, simulador.phi_acumulada, 'r-', linewidth=1.5)
        ax2.axhline(
            y=simulador.phi_umbral, color='green', linestyle='--',
            linewidth=2, label=f'Umbral Φ = {simulador.phi_umbral}'
        )
        
        # Marcar eventos
        for i, evento in enumerate(simulador.eventos_emergencia):
            marker_label = 'Emergencia' if i == 0 else ''
            ax2.plot(
                evento['tiempo_anos'], evento['phi_max'],
                'go', markersize=12, label=marker_label, zorder=5
            )
        
        ax2.set_xlabel('Tiempo (años)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Φ(t) - Fase Acumulada', fontsize=12, fontweight='bold')
        ax2.set_title('Condensador de Fase (Memoria sin Pasado)', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10, loc='best')
        
        # Panel 3: Zoom del primer evento
        if len(simulador.eventos_emergencia) > 0:
            ax3 = fig.add_subplot(gs[2, 0])
            evento = simulador.eventos_emergencia[0]
            idx = evento['indice']
            
            # Ventana de ±50 días
            ventana_dias = 50
            ventana_pts = int(ventana_dias * len(simulador.tiempos) / 
                            (simulador.ciclo_anos * YEAR_DAYS))
            idx_start = max(0, idx - ventana_pts)
            idx_end = min(len(simulador.tiempos), idx + ventana_pts)
            
            t_zoom = t_anos[idx_start:idx_end]
            phi_zoom = simulador.phi_acumulada[idx_start:idx_end]
            
            ax3.plot(t_zoom, phi_zoom, 'purple', linewidth=2)
            ax3.axhline(y=simulador.phi_umbral, color='g', linestyle='--', linewidth=2)
            ax3.plot(
                evento['tiempo_anos'], evento['phi_max'],
                'go', markersize=15, zorder=5
            )
            ax3.set_xlabel('Tiempo (años)', fontsize=11, fontweight='bold')
            ax3.set_ylabel('Φ(t)', fontsize=11, fontweight='bold')
            ax3.set_title('Colapso de Fase - Emergencia', fontsize=12, fontweight='bold')
            ax3.grid(True, alpha=0.3)
            
        # Panel 4: Espectro de frecuencias de Ψ(t)
        ax4 = fig.add_subplot(gs[2, 1])
        
        # FFT de Ψ(t)
        from scipy.fft import fft, fftfreq
        
        N = len(simulador.psi)
        dt = simulador.tiempos[1] - simulador.tiempos[0]
        yf = fft(simulador.psi)
        xf = fftfreq(N, dt)[:N//2]
        
        # Convertir a Hz y escala log
        potencia = 2.0/N * np.abs(yf[0:N//2])
        
        # Filtrar frecuencias muy bajas para visualización
        mask = xf > 1e-9
        ax4.loglog(xf[mask] * 3600 * 24 * 365.25, potencia[mask], 'b-', linewidth=1.5)
        ax4.set_xlabel('Frecuencia (ciclos/año)', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Potencia', fontsize=11, fontweight='bold')
        ax4.set_title('Espectro de Frecuencias', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, which='both')
        
        # Panel 5: Histograma de Φ(t)
        ax5 = fig.add_subplot(gs[3, 0])
        ax5.hist(simulador.phi_acumulada, bins=50, color='coral', alpha=0.7, edgecolor='black')
        ax5.axvline(
            x=simulador.phi_umbral, color='green', linestyle='--',
            linewidth=2, label='Umbral'
        )
        ax5.set_xlabel('Φ(t)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
        ax5.set_title('Distribución de Fase Acumulada', fontsize=12, fontweight='bold')
        ax5.legend(fontsize=10)
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Panel 6: Estadísticas de eventos
        ax6 = fig.add_subplot(gs[3, 1])
        ax6.axis('off')
        
        # Texto con estadísticas
        stats_text = f"""
        ESTADÍSTICAS DE SIMULACIÓN
        ══════════════════════════
        
        Parámetros:
        • f₀ = {simulador.f0:.6f} Hz
        • Ciclo = {simulador.ciclo_anos} años
        • Umbral Φ = {simulador.phi_umbral}
        
        Resultados:
        • Eventos detectados: {len(simulador.eventos_emergencia)}
        • Tiempo primer evento: {simulador.eventos_emergencia[0]['tiempo_anos']:.2f} años
          ({simulador.eventos_emergencia[0]['tiempo_dias']:.1f} días)
        
        Metadata QCAL: ∴𓂀Ω∞³
        """
        
        if len(simulador.eventos_emergencia) > 0:
            ax6.text(
                0.1, 0.5, stats_text,
                fontsize=11, family='monospace',
                verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
        
        # Título general
        fig.suptitle(
            'Simulador de Resonancia Temporal - Aritmología Biológica QCAL',
            fontsize=16, fontweight='bold', y=0.995
        )
        
        # Metadata QCAL en esquina
        fig.text(0.99, 0.01, '∴𓂀Ω∞³', fontsize=10, ha='right', alpha=0.5)
        
        return fig
    
    def generar_mapa_resonancia_2d(self, simulador, n_grid=50):
        """
        Genera mapa 2D de resonancia en espacio de parámetros.
        
        Args:
            simulador: Instancia de SimuladorResonanciaTemporal
            n_grid: Resolución del grid
            
        Returns:
            matplotlib.figure.Figure
        """
        print(f"Generando mapa de resonancia 2D ({n_grid}x{n_grid} puntos)...")
        
        mapa = simulador.generar_mapa_resonancia(n_puntos_grid=n_grid)
        
        # Reorganizar datos para malla 2D
        amplitudes = np.array([p['amplitud'] for p in mapa['puntos']])
        frecuencias = np.array([p['frecuencia'] for p in mapa['puntos']])
        resonancias = np.array([p['resonancia'] for p in mapa['puntos']])
        
        # Crear grid
        amp_unique = np.unique(amplitudes)
        freq_unique = np.unique(frecuencias)
        
        Z = resonancias.reshape(len(amp_unique), len(freq_unique))
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=self.dpi)
        
        # Panel 1: Mapa de calor
        im1 = ax1.contourf(freq_unique, amp_unique, Z, levels=20, cmap='viridis')
        ax1.plot(simulador.f0, simulador.A_f0, 'r*', markersize=20, 
                label=f'f₀ QCAL = {simulador.f0:.4f} Hz')
        ax1.set_xlabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Amplitud Relativa', fontsize=12, fontweight='bold')
        ax1.set_title('Mapa de Resonancia - Contornos', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('Resonancia Φ_max', fontsize=11)
        
        # Panel 2: Superficie 3D (vista superior con colores)
        im2 = ax2.pcolormesh(freq_unique, amp_unique, Z, cmap='plasma', shading='auto')
        ax2.plot(simulador.f0, simulador.A_f0, 'w*', markersize=20, 
                markeredgecolor='black', markeredgewidth=1.5,
                label=f'f₀ QCAL = {simulador.f0:.4f} Hz')
        ax2.set_xlabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Amplitud Relativa', fontsize=12, fontweight='bold')
        ax2.set_title('Mapa de Resonancia - Intensidad', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        cbar2 = plt.colorbar(im2, ax=ax2)
        cbar2.set_label('Resonancia Φ_max', fontsize=11)
        
        fig.suptitle(
            'Espacio de Parámetros - Interferencia Constructiva',
            fontsize=16, fontweight='bold'
        )
        
        # Metadata
        fig.text(0.99, 0.01, '∴𓂀Ω∞³', fontsize=10, ha='right', alpha=0.5)
        
        plt.tight_layout()
        
        return fig
    
    def guardar_figura(self, fig, nombre_base):
        """
        Guarda figura en formatos PNG y PDF.
        
        Args:
            fig: Figura de matplotlib
            nombre_base: Nombre base del archivo (sin extensión)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # PNG
        png_path = self.output_dir / f'{nombre_base}_{timestamp}.png'
        fig.savefig(png_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ PNG guardado: {png_path}")
        
        # PDF
        pdf_path = self.output_dir / f'{nombre_base}_{timestamp}.pdf'
        fig.savefig(pdf_path, bbox_inches='tight')
        print(f"✓ PDF guardado: {pdf_path}")
        
        return png_path, pdf_path


def main():
    """Función principal del demo."""
    print("=" * 70)
    print("DEMO: VISUALIZACIÓN DE RESONANCIA TEMPORAL")
    print("=" * 70)
    print("Generando visualizaciones de alta calidad (300 DPI)")
    print("Metadata QCAL: ∴𓂀Ω∞³")
    print("=" * 70)
    
    # Crear visualizador
    viz = VisualizadorResonanciaTemporal(dpi=300)
    
    # Ejecutar simulación
    print("\n[1/4] Ejecutando simulación de 17 años...")
    sim = SimuladorResonanciaTemporal(f0=F0_QCAL, ciclo_anos=CICADA_CYCLE_YEARS)
    resultados = sim.simular(duracion_anos=17, n_puntos=100000)
    
    print(f"   ✓ Eventos detectados: {len(sim.eventos_emergencia)}")
    if len(sim.eventos_emergencia) > 0:
        print(f"   ✓ Primer evento: {sim.eventos_emergencia[0]['tiempo_anos']:.2f} años")
        print(f"   ✓ Precisión: {resultados['metricas']['precision']:.4f}")
    
    # Generar figura completa
    print("\n[2/4] Generando figura completa con 6 paneles...")
    fig_completa = viz.generar_figura_completa(sim)
    viz.guardar_figura(fig_completa, 'resonancia_temporal_completa')
    
    # Generar mapa de resonancia
    print("\n[3/4] Generando mapa de resonancia 2D...")
    fig_mapa = viz.generar_mapa_resonancia_2d(sim, n_grid=30)
    viz.guardar_figura(fig_mapa, 'mapa_resonancia_2d')
    
    # Visualización estándar del simulador
    print("\n[4/4] Generando visualización estándar...")
    fig_std = sim.visualizar(guardar=True, directorio='results')
    
    # Exportar datos
    print("\nExportando datos JSON...")
    filepath_res = sim.exportar_resultados(resultados, directorio='data')
    print(f"✓ Resultados exportados: {filepath_res}")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETADO")
    print("=" * 70)
    print(f"Archivos generados en:")
    print(f"  • Figuras: {viz.output_dir}/")
    print(f"  • Datos: data/")
    print("=" * 70)
    
    # Mostrar figuras
    plt.show()


if __name__ == '__main__':
    main()
