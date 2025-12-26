#!/usr/bin/env python3
"""
Visualización de SNR Multi-Evento para Análisis O4 y GWTC-1
===========================================================

Genera visualizaciones de los resultados de SNR para eventos O4 y GWTC-1
basado en los análisis realizados.

Autor: José Manuel Mota Burruezo
Fecha: Noviembre 2025
"""

import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    import numpy as np
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib no disponible - solo generará datos numéricos")


def visualizar_o4_detecciones():
    """Visualiza las detecciones del catálogo O4"""
    if not MATPLOTLIB_AVAILABLE:
        print("⚠️  Requiere matplotlib para visualización")
        return
    
    # Datos documentados de O4
    eventos = [
        'GW240109_050431',
        'GW240107_013215',
        'GW240105_151143',
        'GW240104_164932',
        'GW231231_154016'
    ]
    
    frecuencias = [140.95, 140.77, 141.20, 142.05, 140.40]
    deltas = [-0.7501, -0.9301, -0.5001, +0.3499, -1.3001]
    
    f0 = 141.7001
    
    # Crear figura con subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Análisis Catálogo O4: Detección en 141.7 Hz', 
                 fontsize=16, fontweight='bold')
    
    # Gráfico 1: Frecuencias detectadas
    ax1.bar(range(len(eventos)), frecuencias, color='cyan', alpha=0.7, 
            edgecolor='navy', linewidth=2)
    ax1.axhline(y=f0, color='red', linestyle='--', linewidth=2, 
                label=f'f₀ = {f0} Hz')
    ax1.set_ylabel('Frecuencia (Hz)', fontsize=12)
    ax1.set_title('Frecuencias Detectadas por Evento', fontsize=14)
    ax1.set_xticks(range(len(eventos)))
    ax1.set_xticklabels([e.replace('GW', '') for e in eventos], 
                         rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Desviaciones Δf
    colors = ['green' if abs(d) <= 0.55 else 'orange' for d in deltas]
    bars = ax2.bar(range(len(eventos)), deltas, color=colors, alpha=0.7,
                   edgecolor='black', linewidth=2)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.axhline(y=0.55, color='green', linestyle=':', linewidth=1.5, 
                label='Tolerancia (±0.55 Hz)')
    ax2.axhline(y=-0.55, color='green', linestyle=':', linewidth=1.5)
    ax2.set_ylabel('Δf = f - f₀ (Hz)', fontsize=12)
    ax2.set_title('Desviaciones Respecto a f₀', fontsize=14)
    ax2.set_xticks(range(len(eventos)))
    ax2.set_xticklabels([e.replace('GW', '') for e in eventos], 
                         rotation=45, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Gráfico 3: Scatter de desviaciones
    ax3.scatter(range(len(eventos)), deltas, s=200, c='purple', 
                alpha=0.6, edgecolor='black', linewidth=2)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1.5, 
                label='f₀ (Δf = 0)')
    ax3.axhline(y=0.55, color='green', linestyle='--', linewidth=1.5, alpha=0.5)
    ax3.axhline(y=-0.55, color='green', linestyle='--', linewidth=1.5, alpha=0.5)
    ax3.fill_between(range(len(eventos)), -0.55, 0.55, 
                      color='green', alpha=0.1, label='Zona de tolerancia')
    ax3.set_xlabel('Evento', fontsize=12)
    ax3.set_ylabel('Δf (Hz)', fontsize=12)
    ax3.set_title('Dispersión de Desviaciones', fontsize=14)
    ax3.set_xticks(range(len(eventos)))
    ax3.set_xticklabels([e.replace('GW', '') for e in eventos], 
                         rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar figura
    output_dir = Path(__file__).parent.parent / 'results' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'o4_detecciones_multievento.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualización guardada en: {output_file}")
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS O4:")
    print(f"   Media Δf: {np.mean(deltas):.4f} Hz")
    print(f"   Std Δf: {np.std(deltas, ddof=1):.4f} Hz")
    print(f"   Min |Δf|: {min(abs(d) for d in deltas):.4f} Hz")
    print(f"   Max |Δf|: {max(abs(d) for d in deltas):.4f} Hz")


def visualizar_gwtc1_snr():
    """Visualiza SNR de GWTC-1 tri-detector"""
    if not MATPLOTLIB_AVAILABLE:
        print("⚠️  Requiere matplotlib para visualización")
        return
    
    # Datos documentados de GWTC-1
    eventos = [
        'GW150914', 'GW151012', 'GW151226', 'GW170104', 'GW170608',
        'GW170729', 'GW170809', 'GW170814', 'GW170817', 'GW170818', 'GW170823'
    ]
    
    snr_h1 = [14.49, 12.04, 23.17, 19.48, 26.81, 31.35, 26.51, 22.26, 10.78, 20.83, 27.50]
    snr_l1 = [13.87, 27.31, 30.04, 15.79, 10.36, 4.90, 15.65, 12.96, 3.40, 12.38, 18.31]
    
    # Eventos con Virgo
    eventos_virgo = ['GW170814', 'GW170817', 'GW170818']
    snr_v1 = [8.08, 8.57, 7.86]
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Validación GWTC-1: SNR en Banda 141.7 Hz - Tri-Detector', 
                 fontsize=16, fontweight='bold')
    
    # Gráfico 1: SNR por evento
    x = np.arange(len(eventos))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, snr_h1, width, label='H1 (Hanford)', 
                    color='blue', alpha=0.7, edgecolor='navy', linewidth=1.5)
    bars2 = ax1.bar(x + width/2, snr_l1, width, label='L1 (Livingston)', 
                    color='orange', alpha=0.7, edgecolor='darkorange', linewidth=1.5)
    
    # Agregar Virgo en eventos específicos
    virgo_indices = [eventos.index(e) for e in eventos_virgo]
    ax1.scatter(virgo_indices, snr_v1, s=200, c='red', marker='D', 
                label='V1 (Virgo)', edgecolor='darkred', linewidth=2, zorder=5)
    
    ax1.axhline(y=5, color='red', linestyle='--', linewidth=2, 
                label='Umbral 5σ', alpha=0.5)
    ax1.set_ylabel('SNR', fontsize=12)
    ax1.set_title('SNR por Evento y Detector', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(eventos, rotation=45, ha='right')
    ax1.legend(loc='upper left')
    ax1.grid(axis='y', alpha=0.3)
    
    # Agregar valores sobre las barras
    for i, (h1, l1) in enumerate(zip(snr_h1, snr_l1)):
        ax1.text(i - width/2, h1 + 1, f'{h1:.1f}', ha='center', va='bottom', 
                 fontsize=8, color='navy')
        ax1.text(i + width/2, l1 + 1, f'{l1:.1f}', ha='center', va='bottom', 
                 fontsize=8, color='darkorange')
    
    # Gráfico 2: Distribución de SNR
    all_snr = snr_h1 + snr_l1 + snr_v1
    ax2.hist([snr_h1, snr_l1, snr_v1], bins=15, 
             label=['H1 (n=11)', 'L1 (n=11)', 'V1 (n=3)'],
             color=['blue', 'orange', 'red'], alpha=0.6, 
             edgecolor='black', linewidth=1.5)
    
    # Líneas de estadísticas
    ax2.axvline(x=np.mean(snr_h1), color='blue', linestyle='--', linewidth=2, 
                label=f'Media H1: {np.mean(snr_h1):.2f}')
    ax2.axvline(x=np.mean(snr_l1), color='orange', linestyle='--', linewidth=2, 
                label=f'Media L1: {np.mean(snr_l1):.2f}')
    ax2.axvline(x=np.mean(snr_v1), color='red', linestyle='--', linewidth=2, 
                label=f'Media V1: {np.mean(snr_v1):.2f}')
    ax2.axvline(x=5, color='red', linestyle=':', linewidth=2, 
                label='Umbral 5σ', alpha=0.5)
    
    ax2.set_xlabel('SNR', fontsize=12)
    ax2.set_ylabel('Frecuencia', fontsize=12)
    ax2.set_title('Distribución de SNR por Detector', fontsize=14)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar figura
    output_dir = Path(__file__).parent.parent / 'results' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'gwtc1_snr_tridetector.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualización guardada en: {output_file}")
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS GWTC-1:")
    print(f"   H1 - Media: {np.mean(snr_h1):.2f} ± {np.std(snr_h1, ddof=1):.2f}")
    print(f"   L1 - Media: {np.mean(snr_l1):.2f} ± {np.std(snr_l1, ddof=1):.2f}")
    print(f"   V1 - Media: {np.mean(snr_v1):.2f} ± {np.std(snr_v1, ddof=1):.2f}")
    print(f"   H1 - Rango: [{min(snr_h1):.2f}, {max(snr_h1):.2f}]")
    print(f"   L1 - Rango: [{min(snr_l1):.2f}, {max(snr_l1):.2f}]")
    print(f"   V1 - Rango: [{min(snr_v1):.2f}, {max(snr_v1):.2f}]")
    print(f"   Todos > 5σ: {'✅' if min(all_snr) > 5 else '❌'}")


def main():
    """Función principal"""
    print("=" * 80)
    print("🎨 VISUALIZACIÓN MULTI-EVENTO - SNR en 141.7 Hz")
    print("=" * 80)
    print()
    
    if not MATPLOTLIB_AVAILABLE:
        print("❌ matplotlib no está instalado")
        print("   Instalar con: pip install matplotlib")
        return 1
    
    # Generar visualizaciones
    print("📊 Generando visualización O4...")
    visualizar_o4_detecciones()
    
    print("\n📊 Generando visualización GWTC-1...")
    visualizar_gwtc1_snr()
    
    print("\n" + "=" * 80)
    print("✨ VISUALIZACIONES COMPLETADAS")
    print("=" * 80)
    print("\n📂 Archivos guardados en: results/figures/")
    print("   • o4_detecciones_multievento.png")
    print("   • gwtc1_snr_tridetector.png")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
