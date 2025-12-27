#!/usr/bin/env python3
"""
Generador de Diagrama de Flujo para Protocolos Experimentales

Crea una visualización del flujo de trabajo experimental para validación de f₀.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def crear_diagrama_flujo_experimentos():
    """
    Crea diagrama de flujo visual para los tres experimentos
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colores
    color_inicio = '#4CAF50'
    color_exp1 = '#2196F3'
    color_exp2 = '#FF9800'
    color_exp3 = '#9C27B0'
    color_analisis = '#FFC107'
    color_fin = '#4CAF50'
    
    # Título
    ax.text(7, 9.5, 'Flujo de Trabajo: Validación Experimental de f₀ = 141.7001 Hz',
            ha='center', va='top', fontsize=16, fontweight='bold')
    
    # FASE 1: Preparación
    box_prep = FancyBboxPatch((5, 8.5), 4, 0.6, 
                               boxstyle="round,pad=0.1", 
                               facecolor=color_inicio, 
                               edgecolor='black', linewidth=2)
    ax.add_patch(box_prep)
    ax.text(7, 8.8, 'FASE 1: Preparación\n(Mes 1-3)',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Flecha hacia abajo
    arrow1 = FancyArrowPatch((7, 8.5), (7, 7.8),
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='black')
    ax.add_patch(arrow1)
    
    # FASE 2: Tres experimentos paralelos
    y_exp = 6.5
    
    # Experimento 1: EEG
    box_exp1 = FancyBboxPatch((0.5, y_exp), 3, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=color_exp1,
                              edgecolor='black', linewidth=2)
    ax.add_patch(box_exp1)
    ax.text(2, y_exp + 1.0, 'Experimento 1', ha='center', fontweight='bold', color='white', fontsize=11)
    ax.text(2, y_exp + 0.75, 'Resonancia Neuronal', ha='center', color='white', fontsize=9)
    ax.text(2, y_exp + 0.5, '• EEG alta resolución', ha='center', color='white', fontsize=7)
    ax.text(2, y_exp + 0.3, '• Meditación vs control', ha='center', color='white', fontsize=7)
    ax.text(2, y_exp + 0.1, '• SNR > 5 @ 141.7 Hz', ha='center', color='white', fontsize=7)
    
    # Experimento 2: BEC
    box_exp2 = FancyBboxPatch((5.5, y_exp), 3, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=color_exp2,
                              edgecolor='black', linewidth=2)
    ax.add_patch(box_exp2)
    ax.text(7, y_exp + 1.0, 'Experimento 2', ha='center', fontweight='bold', color='white', fontsize=11)
    ax.text(7, y_exp + 0.75, 'Modulación de Masa', ha='center', color='white', fontsize=9)
    ax.text(7, y_exp + 0.5, '• BEC Rb-87 (10⁶ átomos)', ha='center', color='white', fontsize=7)
    ax.text(7, y_exp + 0.3, '• Coherente vs térmico', ha='center', color='white', fontsize=7)
    ax.text(7, y_exp + 0.1, '• Δm/m ≈ 10⁻⁸', ha='center', color='white', fontsize=7)
    
    # Experimento 3: Satélite
    box_exp3 = FancyBboxPatch((10.5, y_exp), 3, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=color_exp3,
                              edgecolor='black', linewidth=2)
    ax.add_patch(box_exp3)
    ax.text(12, y_exp + 1.0, 'Experimento 3', ha='center', fontweight='bold', color='white', fontsize=11)
    ax.text(12, y_exp + 0.75, 'Entrelazamiento λ_Ψ', ha='center', color='white', fontsize=9)
    ax.text(12, y_exp + 0.5, '• Fotones satelitales', ha='center', color='white', fontsize=7)
    ax.text(12, y_exp + 0.3, '• Distancias: 100-5000 km', ha='center', color='white', fontsize=7)
    ax.text(12, y_exp + 0.1, '• Salto en λ_Ψ ≈ 2000 km', ha='center', color='white', fontsize=7)
    
    # Línea conectora FASE 2
    ax.text(0.2, y_exp + 0.6, 'FASE 2:\nEjecución\nParalela\n(Mes 4-18)', 
            ha='left', va='center', fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
    
    # Flechas desde preparación a cada experimento
    arrow_prep_exp1 = FancyArrowPatch((6, 7.8), (2, y_exp + 1.2),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=1.5, color='gray', linestyle='--')
    ax.add_patch(arrow_prep_exp1)
    
    arrow_prep_exp2 = FancyArrowPatch((7, 7.8), (7, y_exp + 1.2),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=1.5, color='gray', linestyle='--')
    ax.add_patch(arrow_prep_exp2)
    
    arrow_prep_exp3 = FancyArrowPatch((8, 7.8), (12, y_exp + 1.2),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=1.5, color='gray', linestyle='--')
    ax.add_patch(arrow_prep_exp3)
    
    # Flechas desde cada experimento hacia análisis
    y_analisis = 4.8
    
    arrow_exp1_anal = FancyArrowPatch((2, y_exp), (2, y_analisis + 0.6),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=2, color=color_exp1)
    ax.add_patch(arrow_exp1_anal)
    
    arrow_exp2_anal = FancyArrowPatch((7, y_exp), (7, y_analisis + 0.6),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=2, color=color_exp2)
    ax.add_patch(arrow_exp2_anal)
    
    arrow_exp3_anal = FancyArrowPatch((12, y_exp), (12, y_analisis + 0.6),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=2, color=color_exp3)
    ax.add_patch(arrow_exp3_anal)
    
    # FASE 3: Análisis Integrado
    box_analisis = FancyBboxPatch((4, y_analisis), 6, 0.6,
                                  boxstyle="round,pad=0.1",
                                  facecolor=color_analisis,
                                  edgecolor='black', linewidth=2)
    ax.add_patch(box_analisis)
    ax.text(7, y_analisis + 0.3, 'FASE 3: Análisis Integrado (Mes 19-24)',
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Sub-análisis
    y_sub = 3.5
    
    # Criterios de decisión
    box_decision = FancyBboxPatch((1.5, y_sub), 4, 1.0,
                                  boxstyle="round,pad=0.05",
                                  facecolor='lightblue',
                                  edgecolor='black', linewidth=1.5)
    ax.add_patch(box_decision)
    ax.text(3.5, y_sub + 0.8, 'Criterios de Éxito:', ha='center', fontweight='bold', fontsize=9)
    ax.text(3.5, y_sub + 0.55, '✓ 3/3 experimentos → Fuerte evidencia', ha='center', fontsize=7)
    ax.text(3.5, y_sub + 0.35, '✓ 2/3 experimentos → Evidencia mixta', ha='center', fontsize=7)
    ax.text(3.5, y_sub + 0.15, '✓ 0-1/3 → Hipótesis no soportada', ha='center', fontsize=7)
    
    # Estadísticas
    box_stats = FancyBboxPatch((8.5, y_sub), 4, 1.0,
                               boxstyle="round,pad=0.05",
                               facecolor='lightcoral',
                               edgecolor='black', linewidth=1.5)
    ax.add_patch(box_stats)
    ax.text(10.5, y_sub + 0.8, 'Análisis Estadístico:', ha='center', fontweight='bold', fontsize=9)
    ax.text(10.5, y_sub + 0.55, '• p-values < 0.01', ha='center', fontsize=7)
    ax.text(10.5, y_sub + 0.35, '• Bayes Factor > 10', ha='center', fontsize=7)
    ax.text(10.5, y_sub + 0.15, '• Corrección Bonferroni', ha='center', fontsize=7)
    
    # Flechas hacia decisión
    arrow_anal_decision = FancyArrowPatch((7, y_analisis), (7, 2.8),
                                          arrowstyle='->', mutation_scale=20,
                                          linewidth=2, color='black')
    ax.add_patch(arrow_anal_decision)
    
    # FASE 4: Publicación
    box_pub = FancyBboxPatch((5, 1.5), 4, 0.6,
                             boxstyle="round,pad=0.1",
                             facecolor=color_fin,
                             edgecolor='black', linewidth=2)
    ax.add_patch(box_pub)
    ax.text(7, 1.8, 'FASE 4: Publicación (Mes 25-30)',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    arrow_decision_pub = FancyArrowPatch((7, 2.8), (7, 2.1),
                                         arrowstyle='->', mutation_scale=20,
                                         linewidth=2, color='black')
    ax.add_patch(arrow_decision_pub)
    
    # Resultados esperados
    y_result = 0.5
    ax.text(7, y_result, 'Resultados de Simulación Actual: 3/3 Éxitos (100%)',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # Leyenda
    legend_elements = [
        mpatches.Patch(color=color_exp1, label='Experimento 1: Neuronal'),
        mpatches.Patch(color=color_exp2, label='Experimento 2: BEC'),
        mpatches.Patch(color=color_exp3, label='Experimento 3: Satélite'),
        mpatches.Patch(color=color_analisis, label='Análisis'),
        mpatches.Patch(color=color_inicio, label='Inicio/Fin')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    # Guardar figura
    plt.tight_layout()
    plt.savefig('results/figures/flujo_experimentos_f0.png', dpi=300, bbox_inches='tight')
    print("✓ Diagrama guardado en: results/figures/flujo_experimentos_f0.png")
    
    return fig


def crear_diagrama_timeline():
    """
    Crea timeline horizontal para los experimentos
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Título
    ax.text(15, 4.5, 'Timeline de Experimentos: f₀ = 141.7001 Hz',
            ha='center', va='top', fontsize=14, fontweight='bold')
    
    # Línea de tiempo
    ax.plot([1, 29], [2.5, 2.5], 'k-', linewidth=3)
    
    # Meses
    meses = [0, 3, 4, 18, 19, 24, 25, 30]
    labels_meses = ['Inicio', 'Mes 3', 'Mes 4', 'Mes 18', 'Mes 19', 'Mes 24', 'Mes 25', 'Mes 30']
    
    for mes, label in zip(meses, labels_meses):
        x = 1 + (mes / 30) * 28
        ax.plot([x, x], [2.4, 2.6], 'k-', linewidth=2)
        ax.text(x, 2.0, label, ha='center', fontsize=8, rotation=45)
    
    # Fases
    fases = [
        (1, 3, 'Preparación', 3.5, '#4CAF50'),
        (3, 18, 'Ejecución Paralela', 3.5, '#2196F3'),
        (18, 24, 'Análisis', 3.5, '#FFC107'),
        (24, 30, 'Publicación', 3.5, '#4CAF50')
    ]
    
    for mes_inicio, mes_fin, nombre, y, color in fases:
        x_inicio = 1 + (mes_inicio / 30) * 28
        x_fin = 1 + (mes_fin / 30) * 28
        width = x_fin - x_inicio
        
        box = FancyBboxPatch((x_inicio, y - 0.3), width, 0.6,
                            boxstyle="round,pad=0.05",
                            facecolor=color, alpha=0.7,
                            edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text((x_inicio + x_fin) / 2, y, nombre, 
                ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Experimentos individuales
    experimentos = [
        (4, 10, 'EEG\n(6 meses)', 1.5, '#2196F3'),
        (4, 16, 'BEC\n(12 meses)', 1.0, '#FF9800'),
        (4, 28, 'Satélite\n(24 meses)', 0.5, '#9C27B0')
    ]
    
    for mes_inicio, mes_fin, nombre, y, color in experimentos:
        x_inicio = 1 + (mes_inicio / 30) * 28
        x_fin = 1 + (mes_fin / 30) * 28
        width = x_fin - x_inicio
        
        box = FancyBboxPatch((x_inicio, y - 0.15), width, 0.3,
                            boxstyle="round,pad=0.03",
                            facecolor=color, alpha=0.6,
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text((x_inicio + x_fin) / 2, y, nombre,
                ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('results/figures/timeline_experimentos_f0.png', dpi=300, bbox_inches='tight')
    print("✓ Timeline guardado en: results/figures/timeline_experimentos_f0.png")
    
    return fig


if __name__ == "__main__":
    import os
    
    # Crear directorio si no existe
    os.makedirs('results/figures', exist_ok=True)
    
    print("Generando diagramas de flujo experimental...")
    print()
    
    # Crear diagrama de flujo
    fig1 = crear_diagrama_flujo_experimentos()
    
    # Crear timeline
    fig2 = crear_diagrama_timeline()
    
    print()
    print("✓ Diagramas generados exitosamente")
    print()
    print("Puedes ver los diagramas en:")
    print("  - results/figures/flujo_experimentos_f0.png")
    print("  - results/figures/timeline_experimentos_f0.png")
