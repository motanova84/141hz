#!/usr/bin/env python3
"""
Generador de Mensaje Visual: Coherencia Cardíaca a 141.7 Hz
============================================================

Este script crea una infografía visual del mensaje central
sobre coherencia cardíaca y el AMOR como resonancia coherente.

Autor: José Manuel Mota Burruezo (JMMB Ψ ∞³)
Fecha: 31 de Enero 2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np


def create_heart_message():
    """Crea el mensaje visual de coherencia cardíaca."""
    
    # Configurar figura
    fig, ax = plt.subplots(figsize=(14, 18), facecolor='#0a0a0a')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Colores
    color_title = '#ff1744'
    color_heart = '#ff4444'
    color_text = '#ffffff'
    color_accent = '#ffeb3b'
    color_box = '#1a1a1a'
    
    # Título principal
    ax.text(5, 13.2, '💗 COHERENCIA CARDÍACA A 141.7 Hz 💗',
            fontsize=28, weight='bold', ha='center', va='top',
            color=color_title, family='monospace')
    
    # Subtítulo
    ax.text(5, 12.5, '"El amor no es emoción. Es RESONANCIA COHERENTE."',
            fontsize=16, ha='center', va='top', style='italic',
            color=color_accent, family='serif')
    
    # Pregunta central
    y_pos = 11.5
    
    fancy_box = FancyBboxPatch((0.5, y_pos - 0.6), 9, 1.2,
                               boxstyle="round,pad=0.1",
                               edgecolor=color_heart, facecolor=color_box,
                               linewidth=3, alpha=0.8)
    ax.add_patch(fancy_box)
    
    ax.text(5, y_pos, '¿Por qué el corazón resuena EXACTAMENTE a 141.7 Hz?',
            fontsize=18, weight='bold', ha='center', va='center',
            color=color_text, family='sans-serif')
    
    # Respuesta: 4 puntos clave
    y_pos = 10.0
    box_height = 0.7
    
    puntos = [
        ('✓', 'Sincroniza todo el cuerpo'),
        ('✓', 'Genera el campo electromagnético más fuerte (5000× cerebro)'),
        ('✓', 'Resuena en coherencia con el campo cuántico'),
        ('✓', 'Conecta conciencia con materia'),
    ]
    
    for i, (check, texto) in enumerate(puntos):
        y = y_pos - i * 0.9
        
        # Caja de fondo
        box = FancyBboxPatch((1, y - 0.35), 8, box_height,
                             boxstyle="round,pad=0.05",
                             edgecolor=color_accent, facecolor=color_box,
                             linewidth=2, alpha=0.6)
        ax.add_patch(box)
        
        # Check mark
        ax.text(1.5, y, check, fontsize=20, weight='bold',
                ha='center', va='center', color=color_heart)
        
        # Texto
        ax.text(2.2, y, texto, fontsize=14, ha='left', va='center',
                color=color_text, family='sans-serif')
    
    # Declaración central
    y_pos = 6.0
    
    # Caja para "NO es"
    no_box = FancyBboxPatch((1.5, y_pos - 0.4), 7, 0.8,
                            boxstyle="round,pad=0.05",
                            edgecolor='#ff5555', facecolor='#2a0a0a',
                            linewidth=3, alpha=0.9)
    ax.add_patch(no_box)
    
    ax.text(5, y_pos, '141.7 Hz NO es la frecuencia del pensamiento.',
            fontsize=16, weight='bold', ha='center', va='center',
            color='#ff8888', family='monospace')
    
    # Caja para "ES"
    y_pos = 5.0
    es_box = FancyBboxPatch((1.5, y_pos - 0.4), 7, 0.8,
                            boxstyle="round,pad=0.05",
                            edgecolor=color_heart, facecolor='#0a2a0a',
                            linewidth=3, alpha=0.9)
    ax.add_patch(es_box)
    
    ax.text(5, y_pos, 'Es la frecuencia del AMOR.',
            fontsize=18, weight='bold', ha='center', va='center',
            color=color_heart, family='monospace')
    
    # Declaración final
    y_pos = 3.8
    
    # Línea separadora
    ax.plot([1, 9], [y_pos + 0.4, y_pos + 0.4], color=color_accent, linewidth=2, alpha=0.7)
    
    ax.text(5, y_pos, 'El amor NO es emoción.',
            fontsize=16, weight='bold', ha='center', va='center',
            color=color_text, family='sans-serif')
    
    y_pos = 3.2
    ax.text(5, y_pos, 'Es RESONANCIA COHERENTE.',
            fontsize=20, weight='bold', ha='center', va='center',
            color=color_heart, family='monospace')
    
    # Constantes fundamentales
    y_pos = 2.0
    
    fancy_box2 = FancyBboxPatch((0.8, y_pos - 1.2), 8.4, 1.5,
                                boxstyle="round,pad=0.1",
                                edgecolor=color_accent, facecolor=color_box,
                                linewidth=2, alpha=0.8)
    ax.add_patch(fancy_box2)
    
    ax.text(5, y_pos, 'CONSTANTES FUNDAMENTALES',
            fontsize=14, weight='bold', ha='center', va='top',
            color=color_accent, family='monospace')
    
    # Constantes en columnas
    y_const = y_pos - 0.4
    ax.text(2.5, y_const, 'f₀ = 141.7001 Hz', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    ax.text(6.5, y_const, 'Ψ ≥ 0.888 (AMOR)', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    
    y_const -= 0.35
    ax.text(2.5, y_const, 'Base HRV: 0.1 Hz', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    ax.text(6.5, y_const, 'Ψ < 0.5 (EMOCIÓN)', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    
    y_const -= 0.35
    ax.text(2.5, y_const, 'Armónico: 1417 (primo)', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    ax.text(6.5, y_const, 'Alcance: 3 metros', fontsize=11, ha='left', va='top',
            color=color_text, family='monospace')
    
    # Firma
    y_pos = 0.5
    ax.text(5, y_pos, '∴𓂀Ω∞³',
            fontsize=24, weight='bold', ha='center', va='center',
            color=color_accent, family='serif')
    
    ax.text(5, y_pos - 0.4, 'El corazón late a 141.7 Hz porque el AMOR',
            fontsize=11, ha='center', va='center',
            color=color_text, style='italic', family='serif')
    
    ax.text(5, y_pos - 0.65, 'es la frecuencia de coherencia universal.',
            fontsize=11, ha='center', va='center',
            color=color_text, style='italic', family='serif')
    
    # Autor y fecha
    ax.text(5, y_pos - 1.0, 'José Manuel Mota Burruezo (JMMB Ψ ∞³) | 31 de Enero 2026',
            fontsize=9, ha='center', va='center',
            color=color_accent, alpha=0.7, family='monospace')
    
    # Guardar
    output_file = 'HEART_COHERENCE_MESSAGE.png'
    plt.savefig(output_file, dpi=200, bbox_inches='tight',
                facecolor='#0a0a0a', edgecolor='none')
    print(f"✓ Mensaje visual creado: {output_file}")
    
    plt.close()


def main():
    """Función principal."""
    print("\n╔════════════════════════════════════════════════════════════════╗")
    print("║  Generando mensaje visual de Coherencia Cardíaca a 141.7 Hz  ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    create_heart_message()
    
    print("\n✓ Generación completa.")
    print("\nEl amor no es emoción. Es RESONANCIA COHERENTE.")
    print("\n∴𓂀Ω∞³\n")


if __name__ == "__main__":
    main()
