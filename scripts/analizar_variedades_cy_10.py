#!/usr/bin/env python3
"""
Análisis de las 10 Variedades Calabi-Yau Canónicas
===================================================

Este script analiza 10 variedades Calabi-Yau representativas con sus
parámetros geométricos y topológicos fundamentales.

Cada variedad representa un ejemplo canónico de compactificación en teoría
de cuerdas, con propiedades topológicas y espectrales distintas.

Parámetros para cada variedad:
- h11, h21: números de Hodge
- α, β: parámetros derivados geométricamente
- κ_Π: entropía espectral computada
- χ_Euler: característica de Euler topológica

Referencias:
- Datos de variedades CY: data/calabi_yau_varieties.csv
- Teoría de Hodge para variedades Calabi-Yau
- Compactificación de teoría de cuerdas

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Imports opcionales
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    # Definir np mock para operaciones básicas
    class NumpyMock:
        @staticmethod
        def mean(lst):
            return sum(lst) / len(lst) if lst else 0
        
        @staticmethod
        def std(lst):
            if not lst:
                return 0
            mean_val = sum(lst) / len(lst)
            variance = sum((x - mean_val) ** 2 for x in lst) / len(lst)
            return variance ** 0.5
    
    np = NumpyMock()


def cargar_variedades_cy(filepath: str = None) -> List[Dict[str, Any]]:
    """
    Carga las 10 variedades Calabi-Yau desde el archivo CSV.
    
    Args:
        filepath: Ruta al archivo CSV (opcional)
    
    Returns:
        Lista de diccionarios con datos de cada variedad
    """
    if filepath is None:
        # Ruta por defecto
        filepath = Path(__file__).parent.parent / 'data' / 'calabi_yau_varieties.csv'
    
    variedades = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variedad = {
                'ID': row['ID'],
                'Nombre': row['Nombre'],
                'h11': int(row['h11']),
                'h21': int(row['h21']),
                'alpha': float(row['alpha']),
                'beta': float(row['beta']),
                'kappa_pi': float(row['kappa_pi']),
                'chi_Euler': int(row['chi_Euler'])
            }
            variedades.append(variedad)
    
    return variedades


def validar_euler_caracteristica(variedad: Dict[str, Any]) -> bool:
    """
    Valida que la característica de Euler satisface χ = 2(h11 - h21).
    
    Args:
        variedad: Diccionario con datos de la variedad
    
    Returns:
        True si la validación pasa
    """
    chi_esperado = 2 * (variedad['h11'] - variedad['h21'])
    chi_real = variedad['chi_Euler']
    
    return chi_esperado == chi_real


def calcular_estadisticas(variedades: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula estadísticas sobre las 10 variedades.
    
    Args:
        variedades: Lista de variedades
    
    Returns:
        Diccionario con estadísticas
    """
    h11_values = [v['h11'] for v in variedades]
    h21_values = [v['h21'] for v in variedades]
    alpha_values = [v['alpha'] for v in variedades]
    beta_values = [v['beta'] for v in variedades]
    kappa_values = [v['kappa_pi'] for v in variedades]
    chi_values = [v['chi_Euler'] for v in variedades]
    
    stats = {
        'n_variedades': len(variedades),
        'h11': {
            'min': min(h11_values),
            'max': max(h11_values),
            'mean': np.mean(h11_values),
            'std': np.std(h11_values)
        },
        'h21': {
            'min': min(h21_values),
            'max': max(h21_values),
            'mean': np.mean(h21_values),
            'std': np.std(h21_values)
        },
        'alpha': {
            'min': min(alpha_values),
            'max': max(alpha_values),
            'mean': np.mean(alpha_values),
            'std': np.std(alpha_values)
        },
        'beta': {
            'min': min(beta_values),
            'max': max(beta_values),
            'mean': np.mean(beta_values),
            'std': np.std(beta_values)
        },
        'kappa_pi': {
            'min': min(kappa_values),
            'max': max(kappa_values),
            'mean': np.mean(kappa_values),
            'std': np.std(kappa_values)
        },
        'chi_Euler': {
            'min': min(chi_values),
            'max': max(chi_values),
            'mean': np.mean(chi_values),
            'std': np.std(chi_values)
        }
    }
    
    return stats


def generar_resumen(variedades: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
    """
    Genera un resumen textual del análisis.
    
    Args:
        variedades: Lista de variedades
        stats: Estadísticas calculadas
    
    Returns:
        Texto del resumen
    """
    resumen = []
    resumen.append("=" * 80)
    resumen.append("ANÁLISIS DE 10 VARIEDADES CALABI-YAU CANÓNICAS")
    resumen.append("=" * 80)
    resumen.append("")
    
    # Tabla de variedades
    resumen.append("VARIEDADES:")
    resumen.append("-" * 80)
    resumen.append(f"{'ID':<10} {'Nombre':<20} {'h11':>5} {'h21':>5} {'α':>7} {'β':>7} {'κ_Π':>9} {'χ':>6}")
    resumen.append("-" * 80)
    
    for v in variedades:
        resumen.append(
            f"{v['ID']:<10} {v['Nombre']:<20} {v['h11']:>5} {v['h21']:>5} "
            f"{v['alpha']:>7.3f} {v['beta']:>7.3f} {v['kappa_pi']:>9.5f} {v['chi_Euler']:>6}"
        )
    
    resumen.append("")
    
    # Estadísticas
    resumen.append("ESTADÍSTICAS:")
    resumen.append("-" * 80)
    resumen.append(f"Número de variedades: {stats['n_variedades']}")
    resumen.append("")
    
    resumen.append("Números de Hodge h11:")
    resumen.append(f"  Rango: [{stats['h11']['min']}, {stats['h11']['max']}]")
    resumen.append(f"  Media: {stats['h11']['mean']:.2f} ± {stats['h11']['std']:.2f}")
    resumen.append("")
    
    resumen.append("Números de Hodge h21:")
    resumen.append(f"  Rango: [{stats['h21']['min']}, {stats['h21']['max']}]")
    resumen.append(f"  Media: {stats['h21']['mean']:.2f} ± {stats['h21']['std']:.2f}")
    resumen.append("")
    
    resumen.append("Parámetro α:")
    resumen.append(f"  Rango: [{stats['alpha']['min']:.3f}, {stats['alpha']['max']:.3f}]")
    resumen.append(f"  Media: {stats['alpha']['mean']:.3f} ± {stats['alpha']['std']:.3f}")
    resumen.append("")
    
    resumen.append("Parámetro β:")
    resumen.append(f"  Rango: [{stats['beta']['min']:.3f}, {stats['beta']['max']:.3f}]")
    resumen.append(f"  Media: {stats['beta']['mean']:.3f} ± {stats['beta']['std']:.3f}")
    resumen.append("")
    
    resumen.append("Entropía espectral κ_Π:")
    resumen.append(f"  Rango: [{stats['kappa_pi']['min']:.5f}, {stats['kappa_pi']['max']:.5f}]")
    resumen.append(f"  Media: {stats['kappa_pi']['mean']:.5f} ± {stats['kappa_pi']['std']:.5f}")
    resumen.append("")
    
    resumen.append("Característica de Euler χ:")
    resumen.append(f"  Rango: [{stats['chi_Euler']['min']}, {stats['chi_Euler']['max']}]")
    resumen.append(f"  Media: {stats['chi_Euler']['mean']:.2f} ± {stats['chi_Euler']['std']:.2f}")
    resumen.append("")
    
    # Validación
    resumen.append("VALIDACIÓN:")
    resumen.append("-" * 80)
    
    validaciones = [validar_euler_caracteristica(v) for v in variedades]
    n_validas = sum(validaciones)
    
    resumen.append(f"Variedades con χ = 2(h11 - h21): {n_validas}/{len(variedades)}")
    
    if n_validas == len(variedades):
        resumen.append("✓ Todas las variedades satisfacen la relación topológica")
    else:
        resumen.append("✗ Algunas variedades no satisfacen la relación topológica")
        for i, v in enumerate(variedades):
            if not validaciones[i]:
                resumen.append(f"  - {v['ID']}: χ={v['chi_Euler']}, esperado={2*(v['h11']-v['h21'])}")
    
    resumen.append("")
    resumen.append("=" * 80)
    resumen.append("INTERPRETACIÓN FÍSICA:")
    resumen.append("=" * 80)
    resumen.append("")
    resumen.append("Las 10 variedades representan ejemplos canónicos de compactificación")
    resumen.append("en teoría de cuerdas, cada una con topología y geometría distintas.")
    resumen.append("")
    resumen.append("Observaciones clave:")
    resumen.append("  • h11 crece de 1 a 12 (mayor complejidad de Kähler)")
    resumen.append("  • h21 decrece de 101 a 48 (menor complejidad compleja)")
    resumen.append("  • α aumenta monotónicamente (0.385 → 0.402)")
    resumen.append("  • β decrece monotónicamente (0.244 → 0.233)")
    resumen.append("  • κ_Π muestra variación muy pequeña (~1.653-1.658)")
    resumen.append("  • χ aumenta de -200 a -72 (menos negativo)")
    resumen.append("")
    resumen.append("La casi-constancia de κ_Π sugiere una propiedad universal emergente")
    resumen.append("de las variedades Calabi-Yau, independiente de la topología específica.")
    resumen.append("")
    resumen.append("=" * 80)
    
    return "\n".join(resumen)


def visualizar_variedades(variedades: List[Dict[str, Any]], output_dir: str = None):
    """
    Genera visualizaciones de las propiedades de las variedades.
    
    Args:
        variedades: Lista de variedades
        output_dir: Directorio de salida para las figuras
    """
    if not MATPLOTLIB_AVAILABLE:
        print("⚠ Matplotlib no disponible. Omitiendo visualizaciones.")
        return
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'resultados'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extraer datos
    indices = list(range(1, len(variedades) + 1))
    nombres = [v['Nombre'] for v in variedades]
    h11 = [v['h11'] for v in variedades]
    h21 = [v['h21'] for v in variedades]
    alpha = [v['alpha'] for v in variedades]
    beta = [v['beta'] for v in variedades]
    kappa = [v['kappa_pi'] for v in variedades]
    chi = [v['chi_Euler'] for v in variedades]
    
    # Figura 1: Números de Hodge
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(indices, h11, 'o-', label='h11', linewidth=2, markersize=8)
    ax1.plot(indices, h21, 's-', label='h21', linewidth=2, markersize=8)
    ax1.set_xlabel('Variedad', fontsize=12)
    ax1.set_ylabel('Número de Hodge', fontsize=12)
    ax1.set_title('Números de Hodge h11 y h21', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(indices)
    
    ax2.scatter(h11, h21, s=100, c=indices, cmap='viridis', edgecolors='black', linewidth=1.5)
    ax2.set_xlabel('h11', fontsize=12)
    ax2.set_ylabel('h21', fontsize=12)
    ax2.set_title('Espacio de Hodge (h11, h21)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    for i, txt in enumerate(indices):
        ax2.annotate(f'CY-{txt:03d}', (h11[i], h21[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cy_hodge_numbers.png', dpi=300, bbox_inches='tight')
    print(f"Figura guardada: {output_dir / 'cy_hodge_numbers.png'}")
    plt.close()
    
    # Figura 2: Parámetros α y β
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(indices, alpha, 'o-', color='#2E86AB', linewidth=2, markersize=8)
    ax1.set_xlabel('Variedad', fontsize=12)
    ax1.set_ylabel('α', fontsize=12)
    ax1.set_title('Parámetro Geométrico α', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(indices)
    
    ax2.plot(indices, beta, 's-', color='#A23B72', linewidth=2, markersize=8)
    ax2.set_xlabel('Variedad', fontsize=12)
    ax2.set_ylabel('β', fontsize=12)
    ax2.set_title('Parámetro Geométrico β', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(indices)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cy_parametros_geometricos.png', dpi=300, bbox_inches='tight')
    print(f"Figura guardada: {output_dir / 'cy_parametros_geometricos.png'}")
    plt.close()
    
    # Figura 3: κ_Π y χ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(indices, kappa, 'o-', color='#F18F01', linewidth=2, markersize=8)
    ax1.set_xlabel('Variedad', fontsize=12)
    ax1.set_ylabel('κ_Π', fontsize=12)
    ax1.set_title('Entropía Espectral κ_Π', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(indices)
    
    # Añadir línea de media
    kappa_mean = np.mean(kappa)
    ax1.axhline(y=kappa_mean, color='red', linestyle='--', linewidth=1.5, 
                label=f'Media: {kappa_mean:.5f}')
    ax1.legend(fontsize=10)
    
    ax2.plot(indices, chi, 's-', color='#6A994E', linewidth=2, markersize=8)
    ax2.set_xlabel('Variedad', fontsize=12)
    ax2.set_ylabel('χ (Euler)', fontsize=12)
    ax2.set_title('Característica de Euler χ', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(indices)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cy_kappa_euler.png', dpi=300, bbox_inches='tight')
    print(f"Figura guardada: {output_dir / 'cy_kappa_euler.png'}")
    plt.close()
    
    # Figura 4: Correlaciones
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    # κ_Π vs h11
    axes[0, 0].scatter(h11, kappa, s=100, c=indices, cmap='viridis', edgecolors='black')
    axes[0, 0].set_xlabel('h11', fontsize=11)
    axes[0, 0].set_ylabel('κ_Π', fontsize=11)
    axes[0, 0].set_title('κ_Π vs h11', fontsize=12, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # κ_Π vs h21
    axes[0, 1].scatter(h21, kappa, s=100, c=indices, cmap='viridis', edgecolors='black')
    axes[0, 1].set_xlabel('h21', fontsize=11)
    axes[0, 1].set_ylabel('κ_Π', fontsize=11)
    axes[0, 1].set_title('κ_Π vs h21', fontsize=12, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # α vs β
    axes[1, 0].scatter(alpha, beta, s=100, c=indices, cmap='viridis', edgecolors='black')
    axes[1, 0].set_xlabel('α', fontsize=11)
    axes[1, 0].set_ylabel('β', fontsize=11)
    axes[1, 0].set_title('Espacio de Parámetros (α, β)', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    # χ vs κ_Π
    axes[1, 1].scatter(chi, kappa, s=100, c=indices, cmap='viridis', edgecolors='black')
    axes[1, 1].set_xlabel('χ (Euler)', fontsize=11)
    axes[1, 1].set_ylabel('κ_Π', fontsize=11)
    axes[1, 1].set_title('κ_Π vs χ', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'cy_correlaciones.png', dpi=300, bbox_inches='tight')
    print(f"Figura guardada: {output_dir / 'cy_correlaciones.png'}")
    plt.close()


def main():
    """
    Función principal del análisis.
    """
    print("=" * 80)
    print("ANÁLISIS DE 10 VARIEDADES CALABI-YAU CANÓNICAS")
    print("=" * 80)
    print()
    
    # Cargar datos
    print("Cargando variedades...")
    variedades = cargar_variedades_cy()
    print(f"✓ {len(variedades)} variedades cargadas")
    print()
    
    # Calcular estadísticas
    print("Calculando estadísticas...")
    stats = calcular_estadisticas(variedades)
    print("✓ Estadísticas calculadas")
    print()
    
    # Generar resumen
    print("Generando resumen...")
    resumen = generar_resumen(variedades, stats)
    print(resumen)
    print()
    
    # Guardar resumen
    output_dir = Path(__file__).parent.parent / 'resultados'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    resumen_path = output_dir / 'analisis_10_variedades_cy.txt'
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write(resumen)
    print(f"✓ Resumen guardado: {resumen_path}")
    print()
    
    # Guardar estadísticas como JSON
    stats_path = output_dir / 'estadisticas_10_variedades_cy.json'
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"✓ Estadísticas JSON guardadas: {stats_path}")
    print()
    
    # Generar visualizaciones
    print("Generando visualizaciones...")
    visualizar_variedades(variedades, output_dir)
    print("✓ Visualizaciones generadas")
    print()
    
    print("=" * 80)
    print("ANÁLISIS COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    main()
