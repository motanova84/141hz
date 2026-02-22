#!/usr/bin/env python3
"""
Visualización del Análisis Espectral de los Primeros 100 Números Primos.

Este script genera visualizaciones de alta calidad para el análisis espectral
de los 100 primeros números primos, incluyendo:

1. Gráfico de frecuencias vs. primos
2. Estructura fractal (log-log)
3. Distribución por octavas
4. Mapa de notas musicales
5. Comparación con frecuencias conocidas

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import sys
import os
from pathlib import Path

# Agregar el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from analisis_espectral_100_primos import (
    analyze_prime_spectrum,
    C0_FREQUENCY
)

# Configuración de matplotlib para publicación
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'


def plot_frequency_spectrum(result, output_path="results/prime_spectrum_frequencies.png"):
    """
    Gráfico 1: Frecuencias fundamentales vs. números primos.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    primes = [pd.prime for pd in result.prime_data]
    frequencies = [pd.frequency_hz for pd in result.prime_data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot principal
    ax.semilogy(primes, frequencies, 'o-', 
                color='#2E86AB', markersize=4, linewidth=1.5,
                label='Frecuencias fundamentales')
    
    # Resaltar p=17 (punto noético)
    freq_17 = float([pd.frequency_hz for pd in result.prime_data if pd.prime == 17][0])
    ax.semilogy(17, freq_17, 'o', 
                color='#A23B72', markersize=12, 
                label=f'p=17 (Punto noético: {freq_17:.2f} Hz)', zorder=5)
    
    # Líneas de referencia
    ax.axhline(y=20, color='gray', linestyle='--', alpha=0.5, 
               label='Límite infrasonido (20 Hz)')
    ax.axhline(y=20000, color='gray', linestyle='--', alpha=0.5,
               label='Límite ultrasonido (20 kHz)')
    ax.axhline(y=141.7, color='#A23B72', linestyle='--', alpha=0.7,
               label='Frecuencia noética (141.7 Hz)')
    
    ax.set_xlabel('Número Primo $p$', fontsize=12)
    ax.set_ylabel('Frecuencia Fundamental $f_0(p)$ [Hz]', fontsize=12)
    ax.set_title('Espectro de Frecuencias de los Primeros 100 Números Primos\n'
                 'Estructura Adélico-Fractal', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def plot_fractal_structure(result, output_path="results/prime_spectrum_fractal.png"):
    """
    Gráfico 2: Estructura fractal log(f₀) vs. √p.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    primes = np.array([pd.prime for pd in result.prime_data])
    frequencies = np.array([pd.frequency_hz for pd in result.prime_data])
    
    sqrt_p = np.sqrt(primes)
    log_f = np.log10(frequencies)
    
    # Regresión lineal
    fa = result.fractal_analysis
    slope = fa['slope_a']
    intercept = fa['intercept_b']
    r_squared = fa['r_squared']
    
    # Predicción
    log_f_pred = slope * sqrt_p + intercept
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Puntos de datos
    ax.plot(sqrt_p, log_f, 'o', 
            color='#2E86AB', markersize=6, alpha=0.7,
            label='Datos observados')
    
    # Línea de regresión
    ax.plot(sqrt_p, log_f_pred, '-', 
            color='#A23B72', linewidth=2,
            label=f'Regresión lineal: $\\log_{{10}}(f_0) = {slope:.3f}\\sqrt{{p}} + {intercept:.3f}$')
    
    # Resaltar p=17
    sqrt_17 = np.sqrt(17)
    log_f_17 = np.log10([pd.frequency_hz for pd in result.prime_data if pd.prime == 17][0])
    ax.plot(sqrt_17, log_f_17, 'o', 
            color='#F18F01', markersize=12, 
            label=f'p=17 (Punto noético)', zorder=5)
    
    ax.set_xlabel('$\\sqrt{p}$', fontsize=14)
    ax.set_ylabel('$\\log_{10}(f_0)$ [Hz]', fontsize=14)
    ax.set_title(f'Estructura Fractal del Espectro de Primos\n'
                 f'$R^2 = {r_squared:.6f}$', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def plot_octave_distribution(result, output_path="results/prime_spectrum_octaves.png"):
    """
    Gráfico 3: Distribución de primos por octava.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    octaves = sorted(result.octave_distribution.keys())
    counts = [len(result.octave_distribution[oct]) for oct in octaves]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Colores diferentes para octavas especiales
    colors = ['#F18F01' if oct == 3 else '#2E86AB' for oct in octaves]
    
    bars = ax.bar(octaves, counts, color=colors, alpha=0.7, edgecolor='black')
    
    # Etiquetar octava noética
    noetic_idx = octaves.index(3)
    bars[noetic_idx].set_label('Octava 3 (Noética)')
    
    ax.set_xlabel('Octava Musical', fontsize=12)
    ax.set_ylabel('Número de Primos', fontsize=12)
    ax.set_title('Distribución de los 100 Primeros Primos por Octava Musical',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(octaves[::2])  # Mostrar cada segunda octava
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)
    
    # Añadir texto con estadísticas
    total_octaves = len(octaves)
    ax.text(0.98, 0.97, 
            f'Total de octavas: {total_octaves}\n'
            f'Octava noética: 3\n'
            f'Rango: {min(octaves)} - {max(octaves)}',
            transform=ax.transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=9)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def plot_musical_notes(result, output_path="results/prime_spectrum_notes.png"):
    """
    Gráfico 4: Distribución de notas musicales.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    # Extraer solo los nombres de las notas (sin octava)
    notes_with_octaves = [pd.musical_note for pd in result.prime_data]
    notes = [note[:-1] for note in notes_with_octaves]  # Eliminar número de octava
    
    # Contar ocurrencias
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_counts = {note: notes.count(note) for note in note_names}
    
    # Ordenar por frecuencia
    sorted_notes = sorted(note_counts.items(), key=lambda x: x[1], reverse=True)
    note_labels = [n[0] for n in sorted_notes]
    counts = [n[1] for n in sorted_notes]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Colores especiales para C# (nota noética)
    colors = ['#A23B72' if note == 'C#' else '#2E86AB' for note in note_labels]
    
    bars = ax.bar(range(len(note_labels)), counts, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(note_labels)))
    ax.set_xticklabels(note_labels)
    
    # Resaltar C# (nota noética)
    cs_idx = note_labels.index('C#')
    bars[cs_idx].set_label('C# (Nota noética)')
    
    ax.set_xlabel('Nota Musical', fontsize=12)
    ax.set_ylabel('Número de Primos', fontsize=12)
    ax.set_title('Distribución de Notas Musicales en los Primeros 100 Primos\n'
                 'Escala Pentatónica Menor Predominante',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)
    
    # Añadir porcentajes
    for i, (note, count) in enumerate(zip(note_labels, counts)):
        percentage = 100 * count / sum(counts)
        ax.text(i, count + 0.5, f'{percentage:.1f}%', 
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def plot_special_primes(result, output_path="results/prime_spectrum_special.png"):
    """
    Gráfico 5: Comparación de primos especiales con frecuencias conocidas.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    special = result.special_primes
    
    # Frecuencias de referencia
    reference_frequencies = {
        'Límite infrasonido': 20,
        'Fundamental (p=3)': special['fundamental']['frequency_hz'],
        'Frecuencia noética (p=17)': special['noetic_point']['frequency_hz'],
        'C medio (C4)': 261.63,
        'Cercano a C4 (p=23)': special['closest_c4']['frequency_hz'],
        'La concierto (A4)': 440,
        'Cercano a A4 (p=29)': special['closest_a4']['frequency_hz'],
        'Límite ultrasonido': 20000,
    }
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Ordenar por frecuencia
    sorted_refs = sorted(reference_frequencies.items(), key=lambda x: x[1])
    labels = [r[0] for r in sorted_refs]
    freqs = [r[1] for r in sorted_refs]
    
    # Colores
    colors = []
    for label in labels:
        if 'noética' in label:
            colors.append('#A23B72')
        elif 'p=' in label:
            colors.append('#F18F01')
        elif 'Límite' in label:
            colors.append('#666666')
        else:
            colors.append('#2E86AB')
    
    # Gráfico horizontal de barras (escala log)
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, freqs, color=colors, alpha=0.7, edgecolor='black')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xscale('log')
    ax.set_xlabel('Frecuencia [Hz]', fontsize=12)
    ax.set_title('Primos Especiales y Frecuencias de Referencia',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Añadir valores
    for i, (label, freq) in enumerate(zip(labels, freqs)):
        ax.text(freq, i, f'  {freq:.2f} Hz', 
                va='center', fontsize=8)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def plot_equilibrium_distribution(result, output_path="results/prime_spectrum_equilibrium.png"):
    """
    Gráfico 6: Distribución de la función de equilibrio.
    
    Args:
        result: Resultado del análisis espectral
        output_path: Ruta para guardar la imagen
    """
    primes = [pd.prime for pd in result.prime_data]
    equilibriums = [pd.equilibrium for pd in result.prime_data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot
    ax.semilogy(primes, equilibriums, 'o-', 
                color='#2E86AB', markersize=4, linewidth=1.5,
                label='equilibrium(p)')
    
    # Resaltar p=3 (mínimo)
    eq_3 = [pd.equilibrium for pd in result.prime_data if pd.prime == 3][0]
    ax.semilogy(3, eq_3, 'o', 
                color='#F18F01', markersize=12, 
                label=f'p=3 (Mínimo: {eq_3:.3f})', zorder=5)
    
    # Resaltar p=17
    eq_17 = [pd.equilibrium for pd in result.prime_data if pd.prime == 17][0]
    ax.semilogy(17, eq_17, 'o', 
                color='#A23B72', markersize=12, 
                label=f'p=17 (Noético: {eq_17:.3f})', zorder=5)
    
    ax.set_xlabel('Número Primo $p$', fontsize=12)
    ax.set_ylabel('$\\mathrm{equilibrium}(p) = \\frac{e^{\\pi\\sqrt{p}/2}}{p^{3/2}}$', 
                  fontsize=12)
    ax.set_title('Función de Equilibrio Adélico-Fractal',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    print(f"✓ Gráfico guardado: {output_path}")
    plt.close()


def generate_all_visualizations(n_primes=100, output_dir="results"):
    """
    Genera todas las visualizaciones para el análisis espectral.
    
    Args:
        n_primes: Número de primos a analizar
        output_dir: Directorio de salida para las imágenes
    """
    print(f"\n{'='*80}")
    print(f"GENERACIÓN DE VISUALIZACIONES - {n_primes} PRIMOS")
    print(f"{'='*80}\n")
    
    # Ejecutar análisis
    print(f"Ejecutando análisis espectral de {n_primes} primos...")
    result = analyze_prime_spectrum(n_primes)
    print("✓ Análisis completado\n")
    
    # Generar cada gráfico
    print("Generando visualizaciones...")
    
    plot_frequency_spectrum(result, f"{output_dir}/prime_spectrum_frequencies.png")
    plot_fractal_structure(result, f"{output_dir}/prime_spectrum_fractal.png")
    plot_octave_distribution(result, f"{output_dir}/prime_spectrum_octaves.png")
    plot_musical_notes(result, f"{output_dir}/prime_spectrum_notes.png")
    plot_special_primes(result, f"{output_dir}/prime_spectrum_special.png")
    plot_equilibrium_distribution(result, f"{output_dir}/prime_spectrum_equilibrium.png")
    
    print(f"\n{'='*80}")
    print("✓ TODAS LAS VISUALIZACIONES GENERADAS EXITOSAMENTE")
    print(f"{'='*80}\n")
    print(f"Directorio de salida: {output_dir}/")
    print("\nArchivos generados:")
    print("  1. prime_spectrum_frequencies.png - Espectro de frecuencias")
    print("  2. prime_spectrum_fractal.png - Estructura fractal")
    print("  3. prime_spectrum_octaves.png - Distribución por octavas")
    print("  4. prime_spectrum_notes.png - Distribución de notas musicales")
    print("  5. prime_spectrum_special.png - Primos especiales")
    print("  6. prime_spectrum_equilibrium.png - Función de equilibrio")


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generación de visualizaciones para análisis espectral de primos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    python visualizar_espectro_100_primos.py              # Todas las visualizaciones
    python visualizar_espectro_100_primos.py -n 50        # Solo 50 primos
    python visualizar_espectro_100_primos.py -o figures/  # Directorio personalizado
        """
    )
    parser.add_argument(
        "-n", "--num-primes",
        type=int,
        default=100,
        help="Número de primos a analizar (default: 100)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="results",
        help="Directorio de salida (default: results)"
    )
    
    args = parser.parse_args()
    
    generate_all_visualizations(
        n_primes=args.num_primes,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
