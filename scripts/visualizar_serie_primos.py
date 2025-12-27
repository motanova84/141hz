#!/usr/bin/env python3
"""
Visualización de la Serie Compleja de Números Primos

Genera gráficos que muestran:
1. Distribución de fases en el plano complejo
2. Coherencia vs. parámetro α
3. Comparación con distribución uniforme

Autor: José Manuel Mota Burruezo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest
import os
import sys

# Importar funciones del script principal
sys.path.insert(0, os.path.dirname(__file__))
from derivacion_frecuencia_prima import (
    generar_primos,
    serie_compleja_primos,
    calcular_coherencia
)


def visualizar_serie_plano_complejo(N=1000, alpha=0.551020, guardar=True):
    """
    Visualiza la serie compleja en el plano complejo.
    """
    primos = generar_primos(N)
    log_primos = np.log(primos)
    fases = 2 * np.pi * log_primos / alpha
    
    # Calcular términos
    z = np.exp(1j * fases)
    
    # Suma parcial acumulativa
    z_cumsum = np.cumsum(z)
    
    # Crear figura con 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Puntos individuales en el círculo unitario
    ax1.scatter(z.real, z.imag, alpha=0.5, s=10, c=range(N), cmap='viridis')
    ax1.add_patch(plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--'))
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('Parte Real')
    ax1.set_ylabel('Parte Imaginaria')
    ax1.set_title(f'Términos de la Serie (N={N}, α={alpha:.4f})')
    
    # Subplot 2: Suma acumulativa
    ax2.plot(z_cumsum.real, z_cumsum.imag, linewidth=0.5, alpha=0.7)
    ax2.scatter(z_cumsum[-1].real, z_cumsum[-1].imag, 
                color='red', s=100, marker='*', zorder=5,
                label=f'Suma Final: {abs(z_cumsum[-1]):.2f}')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Parte Real')
    ax2.set_ylabel('Parte Imaginaria')
    ax2.set_title(f'Suma Acumulativa')
    ax2.legend()
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    
    if guardar:
        output_dir = 'results/figures'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'serie_compleja_primos.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {output_file}")
    
    plt.show()
    return fig


def visualizar_coherencia_vs_alpha(N=1000, n_alphas=50, guardar=True):
    """
    Visualiza cómo varía la coherencia con el parámetro α.
    """
    alphas = np.linspace(0.1, 1.0, n_alphas)
    coherencias = []
    p_values = []
    
    primos = generar_primos(N)
    log_primos = np.log(primos)
    
    print(f"Calculando coherencia para {n_alphas} valores de α...")
    
    for i, alpha in enumerate(alphas):
        # Calcular coherencia
        C = calcular_coherencia(N, alpha)
        coherencias.append(C)
        
        # Calcular p-value del KS test
        fases = (2 * np.pi * log_primos / alpha) % (2 * np.pi)
        fases_norm = fases / (2 * np.pi)
        _, p_value = kstest(fases_norm, 'uniform')
        p_values.append(p_value)
        
        if (i + 1) % 10 == 0:
            print(f"  Progreso: {i+1}/{n_alphas}")
    
    # Encontrar α óptimo
    idx_opt = np.argmax(p_values)
    alpha_opt = alphas[idx_opt]
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Subplot 1: Coherencia
    ax1.plot(alphas, coherencias, linewidth=2, color='blue')
    ax1.axvline(alpha_opt, color='red', linestyle='--', 
                label=f'α_opt = {alpha_opt:.4f}')
    ax1.axvline(0.551020, color='green', linestyle=':', 
                label='α_teórico = 0.551020')
    ax1.set_xlabel('α')
    ax1.set_ylabel('Coherencia |S_N(α)|² / N')
    ax1.set_title(f'Coherencia de la Serie vs. Parámetro α (N={N})')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Subplot 2: p-value del KS test
    ax2.plot(alphas, p_values, linewidth=2, color='orange')
    ax2.axvline(alpha_opt, color='red', linestyle='--',
                label=f'α_opt = {alpha_opt:.4f} (p={p_values[idx_opt]:.4f})')
    ax2.axvline(0.551020, color='green', linestyle=':',
                label='α_teórico = 0.551020')
    ax2.axhline(0.05, color='gray', linestyle='--', alpha=0.5,
                label='Umbral p=0.05')
    ax2.set_xlabel('α')
    ax2.set_ylabel('p-value (KS test)')
    ax2.set_title('Significancia Estadística vs. α')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    if guardar:
        output_dir = 'results/figures'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'coherencia_vs_alpha.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {output_file}")
    
    plt.show()
    return fig


def visualizar_distribucion_fases(N=1000, alpha=0.551020, guardar=True):
    """
    Visualiza la distribución de fases y compara con distribución uniforme.
    """
    primos = generar_primos(N)
    log_primos = np.log(primos)
    fases = (2 * np.pi * log_primos / alpha) % (2 * np.pi)
    
    # KS test
    fases_norm = fases / (2 * np.pi)
    ks_stat, p_value = kstest(fases_norm, 'uniform')
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Histograma de fases
    ax1.hist(fases, bins=50, alpha=0.7, color='blue', 
             density=True, label='Fases observadas')
    ax1.axhline(1/(2*np.pi), color='red', linestyle='--',
                label='Distribución uniforme')
    ax1.set_xlabel('Fase (radianes)')
    ax1.set_ylabel('Densidad')
    ax1.set_title(f'Distribución de Fases (α={alpha:.4f})\n' + 
                  f'KS statistic={ks_stat:.4f}, p-value={p_value:.4f}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: QQ plot (cuantil-cuantil)
    fases_sorted = np.sort(fases_norm)
    uniform_quantiles = np.linspace(0, 1, N)
    
    ax2.scatter(uniform_quantiles, fases_sorted, alpha=0.5, s=10)
    ax2.plot([0, 1], [0, 1], 'r--', label='y=x (uniforme perfecto)')
    ax2.set_xlabel('Cuantiles teóricos (uniforme)')
    ax2.set_ylabel('Cuantiles observados')
    ax2.set_title('QQ Plot: Fases vs. Distribución Uniforme')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    
    if guardar:
        output_dir = 'results/figures'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'distribucion_fases.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {output_file}")
    
    plt.show()
    return fig


def main():
    """
    Genera todas las visualizaciones.
    """
    print("="*70)
    print("VISUALIZACIÓN DE SERIE COMPLEJA DE NÚMEROS PRIMOS")
    print("="*70)
    
    # Parámetros
    N = 1000
    alpha_opt = 0.551020
    
    print(f"\nParámetros:")
    print(f"  N (primos) = {N}")
    print(f"  α_opt = {alpha_opt}")
    
    # Visualización 1: Plano complejo
    print("\n[1/3] Generando visualización del plano complejo...")
    visualizar_serie_plano_complejo(N, alpha_opt)
    
    # Visualización 2: Coherencia vs α
    print("\n[2/3] Generando gráfico de coherencia vs α...")
    visualizar_coherencia_vs_alpha(N, n_alphas=50)
    
    # Visualización 3: Distribución de fases
    print("\n[3/3] Generando análisis de distribución de fases...")
    visualizar_distribucion_fases(N, alpha_opt)
    
    print("\n" + "="*70)
    print("VISUALIZACIONES COMPLETADAS")
    print("="*70)
    print("\nArchivos generados en: results/figures/")
    print("  - serie_compleja_primos.png")
    print("  - coherencia_vs_alpha.png")
    print("  - distribucion_fases.png")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualización de la serie compleja de números primos'
    )
    parser.add_argument(
        '--no-mostrar', action='store_true',
        help='No mostrar gráficos (solo guardar)'
    )
    
    args = parser.parse_args()
    
    if args.no_mostrar:
        plt.ioff()  # Modo no interactivo
    
    main()
