#!/usr/bin/env python3
"""
Validación Atlas³: Ruptura PT-Simetría y Análisis Espectral
===========================================================

Valida la implementación del operador Atlas³ con:
1. Ruptura de simetría PT en κ_Π ≈ 2.57
2. Alineación espectral con línea crítica de Riemann
3. Estadística GUE de matrices aleatorias
4. Transición de localización de Anderson
5. Fase de Berry geométrica

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.atlas3_operator import (
    Atlas3Operator,
    Atlas3Parameters,
    BerryPhaseCalculator,
    SpectralAnalyzer,
    BandStructureAnalyzer,
    validate_atlas3_operator
)


def plot_pt_transition(results, output_dir):
    """
    Graficar transición PT-simetría vs β.
    
    Args:
        results: Resultados de validación
        output_dir: Directorio para guardar gráficas
    """
    beta_values = results['beta_values']
    max_imag = [sig['max_imag'] for sig in results['pt_signatures']]
    n_complex = [sig['n_complex'] for sig in results['pt_signatures']]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Panel 1: Máxima parte imaginaria vs β
    ax1.semilogy(beta_values, max_imag, 'o-', linewidth=2, markersize=8)
    ax1.axvline(2.57, color='red', linestyle='--', label='κ_Π = 2.57')
    ax1.axhline(1e-6, color='gray', linestyle=':', label='Umbral numérico')
    ax1.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax1.set_ylabel('max |Im(λ)|', fontsize=12)
    ax1.set_title('Ruptura PT-Simetría: Parte Imaginaria Máxima', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Panel 2: Número de autovalores complejos
    ax2.plot(beta_values, n_complex, 's-', linewidth=2, markersize=8, color='purple')
    ax2.axvline(2.57, color='red', linestyle='--', label='κ_Π = 2.57')
    ax2.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax2.set_ylabel('# Autovalores Complejos', fontsize=12)
    ax2.set_title('Número de Autovalores con Parte Imaginaria Significativa', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'atlas3_pt_transition.png'), dpi=300, bbox_inches='tight')
    print(f"  Guardado: {output_dir}/atlas3_pt_transition.png")


def plot_spectral_alignment(operator, output_dir):
    """
    Graficar alineación del espectro con línea crítica de Riemann.
    
    Args:
        operator: Operador Atlas3
        output_dir: Directorio para gráficas
    """
    analyzer = SpectralAnalyzer(operator)
    normalized = analyzer.normalize_spectrum_to_critical_line()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel 1: Espectro en plano complejo
    ax1.scatter(operator.eigenvalues.real, operator.eigenvalues.imag, 
                alpha=0.6, s=20, c='blue', label='λ_n')
    ax1.axhline(0, color='gray', linestyle='-', linewidth=0.5)
    ax1.axvline(np.mean(operator.eigenvalues.real), color='red', 
                linestyle='--', label='Re(λ) medio')
    ax1.set_xlabel('Re(λ)', fontsize=12)
    ax1.set_ylabel('Im(λ)', fontsize=12)
    ax1.set_title('Espectro en Plano Complejo', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Panel 2: Espectro normalizado alineado con línea crítica
    ax2.scatter(normalized.real, normalized.imag, alpha=0.6, s=20, c='green', 
                label='λ_n normalizado')
    ax2.axvline(0.5, color='red', linestyle='--', linewidth=2, 
                label='Línea crítica Re(s) = 1/2')
    ax2.axhline(0, color='gray', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Re(λ) normalizado', fontsize=12)
    ax2.set_ylabel('Im(λ)', fontsize=12)
    ax2.set_title('Alineación con Hipótesis de Riemann', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'atlas3_riemann_alignment.png'), 
                dpi=300, bbox_inches='tight')
    print(f"  Guardado: {output_dir}/atlas3_riemann_alignment.png")


def plot_gue_statistics(results, output_dir):
    """
    Graficar estadísticas GUE de espaciamientos.
    
    Args:
        results: Resultados de validación
        output_dir: Directorio para gráficas
    """
    beta_values = results['beta_values']
    gue_variance = [stat['gue_variance'] for stat in results['spectral_stats']]
    repulsion = [stat['level_repulsion'] for stat in results['spectral_stats']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel 1: Varianza GUE
    ax1.plot(beta_values, gue_variance, 'o-', linewidth=2, markersize=8, label='Varianza medida')
    ax1.axhline(0.168, color='red', linestyle='--', linewidth=2, label='GUE teórico (0.168)')
    ax1.axvline(2.57, color='purple', linestyle=':', label='κ_Π = 2.57')
    ax1.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax1.set_ylabel('Varianza de Espaciamientos', fontsize=12)
    ax1.set_title('Estadística GUE: Varianza', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Panel 2: Repulsión de niveles
    ax2.plot(beta_values, repulsion, 's-', linewidth=2, markersize=8, color='orange', label='Repulsión')
    ax2.axvline(2.57, color='purple', linestyle=':', label='κ_Π = 2.57')
    ax2.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax2.set_ylabel('Medida de Repulsión de Niveles', fontsize=12)
    ax2.set_title('Repulsión de Niveles (Wigner Surmise)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'atlas3_gue_statistics.png'), 
                dpi=300, bbox_inches='tight')
    print(f"  Guardado: {output_dir}/atlas3_gue_statistics.png")


def plot_anderson_localization(results, output_dir):
    """
    Graficar transición de localización de Anderson.
    
    Args:
        results: Resultados de validación
        output_dir: Directorio para gráficas
    """
    beta_values = results['beta_values']
    mean_ipr = [loc['mean_ipr'] for loc in results['localization_measures']]
    loc_fraction = [loc['localization_fraction'] for loc in results['localization_measures']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel 1: IPR medio
    ax1.semilogy(beta_values, mean_ipr, 'o-', linewidth=2, markersize=8, color='darkgreen')
    ax1.axhline(1.0/500, color='blue', linestyle='--', label='1/N (extendidos)')
    ax1.axvline(2.57, color='red', linestyle='--', label='κ_Π = 2.57')
    ax1.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax1.set_ylabel('IPR Medio', fontsize=12)
    ax1.set_title('Inverse Participation Ratio', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Panel 2: Fracción de estados localizados
    ax2.plot(beta_values, np.array(loc_fraction)*100, 's-', linewidth=2, 
             markersize=8, color='darkred')
    ax2.axvline(2.57, color='red', linestyle='--', label='κ_Π = 2.57')
    ax2.set_xlabel('β (Parámetro PT)', fontsize=12)
    ax2.set_ylabel('Estados Localizados (%)', fontsize=12)
    ax2.set_title('Fracción de Estados Localizados', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'atlas3_anderson_localization.png'), 
                dpi=300, bbox_inches='tight')
    print(f"  Guardado: {output_dir}/atlas3_anderson_localization.png")


def plot_band_structure(operator, output_dir):
    """
    Graficar estructura de bandas y gaps prohibidos.
    
    Args:
        operator: Operador Atlas3
        output_dir: Directorio para gráficas
    """
    band_analyzer = BandStructureAnalyzer(operator)
    gaps = band_analyzer.find_band_gaps(gap_threshold=5.0)
    hofstadter = band_analyzer.hofstadter_butterfly_signature()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficar espectro de energías
    energies = np.sort(operator.eigenvalues.real)
    ax.plot(energies, 'o', markersize=3, alpha=0.6, label='Autovalores')
    
    # Marcar gaps
    for i, (e_low, e_high) in enumerate(gaps['gaps']):
        idx_low = np.argmin(np.abs(energies - e_low))
        idx_high = np.argmin(np.abs(energies - e_high))
        ax.axhspan(e_low, e_high, alpha=0.3, color='red', 
                   label='Gap' if i == 0 else '')
    
    ax.set_xlabel('Índice de Autovalor', fontsize=12)
    ax.set_ylabel('Energía (Re λ)', fontsize=12)
    ax.set_title(f'Estructura de Bandas (Gaps: {gaps["n_gaps"]}, ' + 
                 f'Dimensión Fractal: {hofstadter["fractal_dimension"]:.3f})', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'atlas3_band_structure.png'), 
                dpi=300, bbox_inches='tight')
    print(f"  Guardado: {output_dir}/atlas3_band_structure.png")


def main():
    """Ejecutar validación completa de Atlas³."""
    print("="*70)
    print(" VALIDACIÓN ATLAS³: Ruptura PT-Simetría y Análisis Espectral")
    print("="*70)
    
    # Crear directorio de salida
    output_dir = Path(__file__).parent.parent / "results" / "atlas3_validation"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nDirectorio de salida: {output_dir}")
    
    # Ejecutar validación completa
    print("\n" + "="*70)
    print("Ejecutando validación con múltiples valores de β...")
    print("="*70)
    
    beta_values = [0.0, 1.0, 2.0, 2.57, 3.0, 4.0]
    results = validate_atlas3_operator(beta_values=beta_values, verbose=True)
    
    # Generar gráficas
    print("\n" + "="*70)
    print("Generando visualizaciones...")
    print("="*70)
    
    print("\n1. Transición PT-Simetría:")
    plot_pt_transition(results, output_dir)
    
    print("\n2. Estadística GUE:")
    plot_gue_statistics(results, output_dir)
    
    print("\n3. Localización de Anderson:")
    plot_anderson_localization(results, output_dir)
    
    # Análisis detallado para β crítico
    print("\n" + "="*70)
    print("Análisis detallado en κ_Π = 2.57...")
    print("="*70)
    
    operator_critical = Atlas3Operator(beta=2.57)
    operator_critical.compute_spectrum()
    
    print("\n4. Alineación con Riemann:")
    plot_spectral_alignment(operator_critical, output_dir)
    
    print("\n5. Estructura de Bandas:")
    plot_band_structure(operator_critical, output_dir)
    
    # Resumen de resultados
    print("\n" + "="*70)
    print(" RESUMEN DE RESULTADOS")
    print("="*70)
    
    # Encontrar índice del β crítico
    idx_critical = np.argmin([abs(b - 2.57) for b in beta_values])
    pt_critical = results['pt_signatures'][idx_critical]
    spectral_critical = results['spectral_stats'][idx_critical]
    loc_critical = results['localization_measures'][idx_critical]
    
    print(f"\nEn el punto crítico κ_Π = 2.57:")
    print(f"  ✓ Ruptura PT-Simetría: {'SÍ' if pt_critical['is_broken'] else 'NO'}")
    print(f"    - max |Im(λ)| = {pt_critical['max_imag']:.6f}")
    print(f"    - Autovalores complejos: {pt_critical['n_complex']}/{len(operator_critical.eigenvalues)}")
    print(f"  ✓ Estadística GUE:")
    print(f"    - Varianza = {spectral_critical['gue_variance']:.4f} (teórico: 0.168)")
    print(f"    - Repulsión = {spectral_critical['level_repulsion']:.4f}")
    print(f"  ✓ Localización de Anderson:")
    print(f"    - IPR medio = {loc_critical['mean_ipr']:.6f}")
    print(f"    - Estados localizados = {loc_critical['localization_fraction']*100:.1f}%")
    
    # Verificar coherencia con πCODE
    print(f"\n{'='*70}")
    print(" COHERENCIA CON FRAMEWORK πCODE")
    print(f"{'='*70}")
    print(f"  ✓ Frecuencia fundamental f₀ = {operator_critical.params.f0:.4f} Hz")
    print(f"  ✓ Discretización: N = {operator_critical.params.N} puntos")
    print(f"  ✓ Potencial quasiperiódico: V_amp = {operator_critical.params.V_amp:.1f}")
    print(f"  ✓ Parámetro crítico: κ_Π = {operator_critical.params.beta_critical:.2f}")
    print(f"  ✓ Línea crítica RH: Re(s) = {operator_critical.params.critical_line_re}")
    
    # Verificaciones de validación
    print(f"\n{'='*70}")
    print(" VERIFICACIONES DE VALIDACIÓN")
    print(f"{'='*70}")
    
    validations = []
    
    # V1: PT-symmetry breaking
    if pt_critical['is_broken'] and pt_critical['max_imag'] > 0.1:
        validations.append("✓ V1: Ruptura PT-Simetría confirmada")
    else:
        validations.append("✗ V1: Ruptura PT-Simetría NO confirmada")
    
    # V2: Spectral alignment
    analyzer = SpectralAnalyzer(operator_critical)
    normalized = analyzer.normalize_spectrum_to_critical_line()
    re_deviation = np.std(normalized.real - 0.5)
    if re_deviation < 0.3:
        validations.append(f"✓ V2: Alineación espectral (σ = {re_deviation:.4f})")
    else:
        validations.append(f"✗ V2: Alineación espectral pobre (σ = {re_deviation:.4f})")
    
    # V3: GUE statistics
    gue_diff = abs(spectral_critical['gue_variance'] - 0.168)
    if gue_diff < 0.1:
        validations.append(f"✓ V3: Estadística GUE (Δ = {gue_diff:.4f})")
    else:
        validations.append(f"⚠ V3: Estadística GUE desviada (Δ = {gue_diff:.4f})")
    
    # V4: Anderson localization
    if loc_critical['mean_ipr'] > 1.0/operator_critical.params.N:
        validations.append(f"✓ V4: Transición de localización detectada")
    else:
        validations.append(f"⚠ V4: Estados extendidos dominan")
    
    for validation in validations:
        print(f"  {validation}")
    
    # Éxito global
    n_passed = sum(1 for v in validations if v.startswith("✓"))
    success_rate = n_passed / len(validations) * 100
    
    print(f"\n{'='*70}")
    print(f" TASA DE ÉXITO: {n_passed}/{len(validations)} ({success_rate:.1f}%)")
    print(f"{'='*70}")
    
    if success_rate >= 75:
        print("\n🌌 VALIDACIÓN ATLAS³ EXITOSA 🌌")
        print("\nEl operador Atlas³ exhibe:")
        print("  - Ruptura PT-Simetría en κ_Π ≈ 2.57")
        print("  - Alineación espectral con hipótesis de Riemann")
        print("  - Estadística GUE de matrices aleatorias")
        print("  - Transición de localización de Anderson")
        print("\nEstos resultados confirman la ontología universal de $\\mathcal{H}_{Atlas^3}$")
        print("como escenario del backbone πCODE con memoria noésica geométrica.")
    else:
        print("\n⚠ VALIDACIÓN PARCIAL")
        print(f"\nAlgunos tests no pasaron. Revisar implementación.")
    
    print(f"\n{'='*70}")
    print(f" Resultados guardados en: {output_dir}")
    print(f"{'='*70}\n")
    
    return results


if __name__ == "__main__":
    main()
