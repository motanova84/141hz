#!/usr/bin/env python3
"""
Visualización de la Torre Algebraica

Crea una visualización gráfica de la estructura de torre algebraica de 5 niveles
mostrando cómo emerge la teoría desde la ontología hasta la fenomenología.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.facecolor'] = 'white'


def crear_visualizacion_torre():
    """
    Crea la visualización de la torre algebraica.
    """
    fig, ax = plt.subplots(figsize=(14, 10))

    # Definir los niveles de la torre
    niveles = [
        {
            "nivel": 5,
            "nombre": "NIVEL 5: Ontología",
            "descripcion": "Campo Ψ universal",
            "ecuacion": "Ψ: ℝ⁴ → ℂ",
            "color": "#9b59b6",  # Púrpura profundo
            "y_pos": 0.85
        },
        {
            "nivel": 4,
            "nombre": "NIVEL 4: Geometría",
            "descripcion": "Variedades de Calabi-Yau",
            "ecuacion": "R_Ψ ≈ 10⁴⁰ m",
            "color": "#3498db",  # Azul
            "y_pos": 0.68
        },
        {
            "nivel": 3,
            "nombre": "NIVEL 3: Energía",
            "descripcion": "E_Ψ = hf₀, m_Ψ = hf₀/c², T_Ψ ≈ 10⁻⁹ K",
            "ecuacion": "f₀ = 141.7001 Hz",
            "color": "#2ecc71",  # Verde
            "y_pos": 0.51
        },
        {
            "nivel": 2,
            "nombre": "NIVEL 2: Dinámica",
            "descripcion": "C = I × A² × eff² × f₀",
            "ecuacion": "dC/dt = -γC + η·cos(2πf₀t)",
            "color": "#f39c12",  # Naranja
            "y_pos": 0.34
        },
        {
            "nivel": 1,
            "nombre": "NIVEL 1: Fenomenología",
            "descripcion": "E = mc², E = hf (casos límite)",
            "ecuacion": "Leyes observables",
            "color": "#e74c3c",  # Rojo
            "y_pos": 0.17
        }
    ]

    # Dibujar cada nivel como una caja
    for i, nivel in enumerate(niveles):
        # Caja principal
        box = FancyBboxPatch(
            (0.1, nivel['y_pos'] - 0.06),
            0.8,
            0.11,
            boxstyle="round,pad=0.01",
            edgecolor=nivel['color'],
            facecolor=nivel['color'],
            alpha=0.3,
            linewidth=3,
            transform=ax.transAxes
        )
        ax.add_patch(box)

        # Título del nivel
        ax.text(
            0.5, nivel['y_pos'] + 0.02,
            nivel['nombre'],
            ha='center', va='center',
            fontsize=14, fontweight='bold',
            color=nivel['color'],
            transform=ax.transAxes
        )

        # Descripción
        ax.text(
            0.5, nivel['y_pos'] - 0.015,
            nivel['descripcion'],
            ha='center', va='center',
            fontsize=11,
            color='black',
            transform=ax.transAxes
        )

        # Ecuación
        ax.text(
            0.5, nivel['y_pos'] - 0.04,
            nivel['ecuacion'],
            ha='center', va='center',
            fontsize=10,
            style='italic',
            color='#34495e',
            transform=ax.transAxes
        )

        # Flecha de emergencia al siguiente nivel (excepto el último)
        if i < len(niveles) - 1:
            arrow = FancyArrowPatch(
                (0.5, nivel['y_pos'] - 0.07),
                (0.5, niveles[i+1]['y_pos'] + 0.055),
                arrowstyle='->,head_width=0.4,head_length=0.4',
                color='#7f8c8d',
                linewidth=2.5,
                alpha=0.7,
                transform=ax.transAxes,
                mutation_scale=30
            )
            ax.add_patch(arrow)

            # Texto de la transición
            transiciones = [
                "Compactificación\ndimensional",
                "Modos\nvibracionales",
                "Acoplamiento\nresonante",
                "Límites\nasintóticos"
            ]

            mid_y = (nivel['y_pos'] - 0.07 + niveles[i+1]['y_pos'] + 0.055) / 2
            ax.text(
                0.65, mid_y,
                transiciones[i],
                ha='left', va='center',
                fontsize=9,
                style='italic',
                color='#7f8c8d',
                transform=ax.transAxes
            )

    # Título principal
    ax.text(
        0.5, 0.97,
        'Torre Algebraica de la Teoría Noésica',
        ha='center', va='top',
        fontsize=18, fontweight='bold',
        color='#2c3e50',
        transform=ax.transAxes
    )

    # Subtítulo
    ax.text(
        0.5, 0.935,
        'Estructura Emergente: Lo Abstracto → Lo Concreto',
        ha='center', va='top',
        fontsize=12,
        style='italic',
        color='#7f8c8d',
        transform=ax.transAxes
    )

    # Texto explicativo en la parte inferior
    texto_inferior = (
        'Cada nivel emerge naturalmente del anterior, demostrando cómo:\n'
        '• Lo abstracto (Ψ) genera lo concreto (fenómenos observables)\n'
        '• Lo simple da lugar a lo complejo (estructura del universo)\n'
        '• Similar a: Teoría de números → Geometría algebraica → Física teórica → Fenómenos'
    )

    ax.text(
        0.5, 0.04,
        texto_inferior,
        ha='center', va='bottom',
        fontsize=9,
        color='#34495e',
        transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8, edgecolor='#bdc3c7')
    )

    # Configurar ejes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Ajustar layout
    plt.tight_layout()

    return fig


def crear_diagrama_flujo():
    """
    Crea un diagrama de flujo simplificado de la emergencia.
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Definir posiciones y contenido
    boxes = [
        {"pos": (0.5, 0.9), "text": "Ontología\nCampo Ψ", "color": "#9b59b6"},
        {"pos": (0.5, 0.7), "text": "Geometría\nCalabi-Yau", "color": "#3498db"},
        {"pos": (0.5, 0.5), "text": "Energía\nE_Ψ = hf₀", "color": "#2ecc71"},
        {"pos": (0.5, 0.3), "text": "Dinámica\nC = I×A²×eff²×f₀", "color": "#f39c12"},
        {"pos": (0.5, 0.1), "text": "Fenomenología\nE=mc², E=hf", "color": "#e74c3c"}
    ]

    # Dibujar cajas
    for i, box in enumerate(boxes):
        rect = FancyBboxPatch(
            (box['pos'][0] - 0.15, box['pos'][1] - 0.05),
            0.3, 0.1,
            boxstyle="round,pad=0.01",
            edgecolor=box['color'],
            facecolor=box['color'],
            alpha=0.3,
            linewidth=2
        )
        ax.add_patch(rect)

        ax.text(
            box['pos'][0], box['pos'][1],
            box['text'],
            ha='center', va='center',
            fontsize=11, fontweight='bold',
            color=box['color']
        )

        # Flechas
        if i < len(boxes) - 1:
            arrow = FancyArrowPatch(
                (box['pos'][0], box['pos'][1] - 0.06),
                (boxes[i+1]['pos'][0], boxes[i+1]['pos'][1] + 0.06),
                arrowstyle='->,head_width=0.3,head_length=0.3',
                color='#7f8c8d',
                linewidth=2,
                mutation_scale=20
            )
            ax.add_patch(arrow)

    # Título
    ax.text(
        0.5, 0.97,
        'Flujo de Emergencia de la Torre Algebraica',
        ha='center', va='top',
        fontsize=16, fontweight='bold',
        color='#2c3e50'
    )

    # Configurar ejes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()

    return fig


def main():
    """
    Función principal que genera las visualizaciones.
    """
    print("=" * 80)
    print("VISUALIZACIÓN DE LA TORRE ALGEBRAICA")
    print("=" * 80)
    print()

    # Crear directorio de resultados
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    print("Generando visualizaciones...")
    print()

    # 1. Visualización completa de la torre
    print("  1. Torre algebraica completa...")
    fig1 = crear_visualizacion_torre()
    output_file1 = results_dir / "torre_algebraica_completa.png"
    fig1.savefig(output_file1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    print(f"     ✓ Guardado: {output_file1}")

    # 2. Diagrama de flujo
    print("  2. Diagrama de flujo de emergencia...")
    fig2 = crear_diagrama_flujo()
    output_file2 = results_dir / "torre_algebraica_flujo.png"
    fig2.savefig(output_file2, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    print(f"     ✓ Guardado: {output_file2}")

    print()
    print("=" * 80)
    print("VISUALIZACIONES COMPLETADAS")
    print("=" * 80)
    print()
    print("Archivos generados:")
    print(f"  • {output_file1}")
    print(f"  • {output_file2}")
    print()
    print("Estas visualizaciones demuestran la estructura emergente de la")
    print("teoría noésica desde los principios abstractos hasta los fenómenos")
    print("observables concretos.")
    print()


if __name__ == "__main__":
    main()
