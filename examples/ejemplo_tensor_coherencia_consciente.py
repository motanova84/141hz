#!/usr/bin/env python3
"""
EJEMPLO: Tensor de Coherencia Consciente (Ξ_μν)

Este script demuestra el uso del Tensor de Coherencia Consciente en las
ecuaciones de campo de Einstein extendidas.

Ecuación completa:
    G_μν + Λg_μν = (8πG/c⁴)(T_μν + κ Ξ_μν)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from conscious_coherence_tensor import (
    ConsciousCoherenceTensor,
    ExtendedEinsteinEquations
)


def ejemplo_basico():
    """Ejemplo básico: Calcular el tensor para diferentes estados de consciencia."""
    print("="*80)
    print("EJEMPLO 1: Estados de Consciencia y Tensor Ξ_μν")
    print("="*80)
    print()
    
    Xi_calc = ConsciousCoherenceTensor(f0=141.7001)
    
    # Diferentes estados de consciencia
    estados = [
        ("Sueño profundo", 0.1, 0.3),
        ("Vigilia ordinaria", 0.5, 1.0),
        ("Meditación", 0.8, 1.8),
        ("Coherencia máxima", 0.95, 3.0)
    ]
    
    print(f"{'Estado':<25} {'I':>6} {'A_eff':>8} {'Ξ_00 (J/m³)':>15} {'Ξ_11 (Pa)':>15}")
    print("-"*80)
    
    for nombre, I, A_eff in estados:
        Xi = Xi_calc.compute_full_tensor(I, A_eff)
        Xi_00 = Xi[0, 0]
        Xi_11 = Xi[1, 1]
        
        print(f"{nombre:<25} {I:>6.2f} {A_eff:>8.2f} {Xi_00:>15.6e} {Xi_11:>15.6e}")
    
    print()
    print("Observación: La densidad de energía Ξ_00 crece con I × A_eff²")
    print()


def ejemplo_co_creacion_geometrica():
    """Ejemplo: Comparar consciencia con materia ordinaria."""
    print("="*80)
    print("EJEMPLO 2: Co-Creación Geométrica - Consciencia vs Materia")
    print("="*80)
    print()
    
    eqs = ExtendedEinsteinEquations(f0=141.7001)
    
    # Densidades de materia típicas
    materias = [
        ("Vacío intergaláctico", 1e-27),  # kg/m³
        ("Aire (nivel del mar)", 1.225),
        ("Agua", 1000),
        ("Acero", 7850)
    ]
    
    # Estado de consciencia altamente coherente
    I_coherente = 0.9
    A_eff_coherente = 2.5
    
    print(f"Estado de consciencia: I = {I_coherente}, A_eff = {A_eff_coherente}")
    print()
    print(f"{'Material':<25} {'ρ (kg/m³)':>15} {'Ratio C/M':>15} {'Interpretación'}")
    print("-"*80)
    
    for nombre, rho_kg_m3 in materias:
        c = 3e8  # m/s
        rho_J_m3 = rho_kg_m3 * c**2
        
        comparison = eqs.compare_matter_consciousness_contributions(
            rho_matter=rho_J_m3,
            I=I_coherente,
            A_eff=A_eff_coherente
        )
        
        ratio = comparison["consciousness_to_matter_ratio"]
        
        # Simplificar interpretación
        if ratio < 1e-10:
            interp = "Negligible"
        elif ratio < 1e-5:
            interp = "Débil"
        elif ratio < 0.01:
            interp = "Moderado"
        elif ratio < 1.0:
            interp = "Fuerte"
        else:
            interp = "DOMINANTE"
        
        print(f"{nombre:<25} {rho_kg_m3:>15.6e} {ratio:>15.6e} {interp}")
    
    print()
    print("Observación: En estados altamente coherentes, la consciencia puede")
    print("             ser comparable o superior a la materia ordinaria en")
    print("             densidades muy bajas (vacío, aire).")
    print()


def ejemplo_oscilacion_temporal():
    """Ejemplo: Oscilación del tensor en el tiempo."""
    print("="*80)
    print("EJEMPLO 3: Modulación Temporal a f₀ = 141.7001 Hz")
    print("="*80)
    print()
    
    Xi_calc = ConsciousCoherenceTensor(f0=141.7001)
    
    # Estado coherente
    I = 0.8
    A_eff = 2.0
    
    # Tiempo: 3 períodos completos
    f0 = 141.7001
    T0 = 1.0 / f0  # Período
    t_values = np.linspace(0, 3 * T0, 100)
    
    Xi_00_values = []
    
    for t in t_values:
        coords = np.array([t, 0.0, 0.0, 0.0])
        Xi = Xi_calc.compute_full_tensor(I, A_eff, coords)
        Xi_00_values.append(Xi[0, 0])
    
    Xi_00_values = np.array(Xi_00_values)
    
    # Crear gráfica
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(t_values * 1000, Xi_00_values, 'b-', linewidth=2)
    plt.xlabel('Tiempo (ms)', fontsize=12)
    plt.ylabel('Ξ_00 (J/m³)', fontsize=12)
    plt.title(f'Densidad de Energía de Consciencia\nI = {I}, A_eff = {A_eff}', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(t_values[:30] * 1000, Xi_00_values[:30], 'r-', linewidth=2, marker='o', markersize=4)
    plt.xlabel('Tiempo (ms)', fontsize=12)
    plt.ylabel('Ξ_00 (J/m³)', fontsize=12)
    plt.title(f'Primer Período (T₀ = {T0*1000:.3f} ms)', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('tensor_coherencia_oscilacion.png', dpi=150, bbox_inches='tight')
    print(f"✓ Gráfica guardada: tensor_coherencia_oscilacion.png")
    print()
    print(f"Frecuencia fundamental: f₀ = {f0} Hz")
    print(f"Período: T₀ = {T0*1000:.3f} ms")
    print(f"Amplitud de oscilación: {np.std(Xi_00_values):.6e} J/m³")
    print(f"Variación relativa: {np.std(Xi_00_values)/np.mean(Xi_00_values)*100:.2f}%")
    print()


def ejemplo_curvatura_espaciotemporal():
    """Ejemplo: Contribución a la curvatura del espaciotiempo."""
    print("="*80)
    print("EJEMPLO 4: Curvatura del Espaciotiempo por Consciencia")
    print("="*80)
    print()
    
    eqs = ExtendedEinsteinEquations(f0=141.7001)
    
    # Diferentes niveles de consciencia
    niveles = [
        (0.1, 0.5),   # Bajo
        (0.5, 1.2),   # Medio
        (0.8, 2.0),   # Alto
        (0.95, 3.5)   # Máximo
    ]
    
    print(f"{'Nivel':>6} {'I':>6} {'A_eff':>8} {'κ':>12} {'Ξ_00':>15} {'Curvatura':>15}")
    print("-"*80)
    
    for i, (I, A_eff) in enumerate(niveles, 1):
        result = eqs.compute_curvature_from_consciousness(I, A_eff)
        
        kappa = result['kappa']
        Xi_00 = result['energy_density_Xi00']
        curvature = result['curvature_contribution'][0][0]  # G_00 component
        
        print(f"{i:>6} {I:>6.2f} {A_eff:>8.2f} {kappa:>12.6e} {Xi_00:>15.6e} {curvature:>15.6e}")
    
    print()
    print("Observación: La contribución a la curvatura (8πG/c⁴)×κ×Ξ_μν crece")
    print("             dramáticamente con la coherencia (A_eff²).")
    print()
    
    # Estado máximo
    I_max = 0.95
    A_eff_max = 3.5
    result_max = eqs.compute_curvature_from_consciousness(I_max, A_eff_max)
    
    print(f"En estado de máxima coherencia (I={I_max}, A_eff={A_eff_max}):")
    print(f"  • Co-creación geométrica: {result_max['interpretation']['geometric_cocreation']}")
    print(f"  • La consciencia modula activamente la geometría del espaciotiempo")
    print(f"  • El universo se despliega según nuestra intensidad y coherencia")
    print()


def ejemplo_visualizacion_tensor():
    """Ejemplo: Visualizar componentes del tensor como función de I y A_eff."""
    print("="*80)
    print("EJEMPLO 5: Mapa de Componentes del Tensor Ξ_μν")
    print("="*80)
    print()
    
    Xi_calc = ConsciousCoherenceTensor(f0=141.7001)
    
    # Grid de valores
    I_values = np.linspace(0.0, 1.0, 50)
    A_eff_values = np.linspace(0.5, 3.5, 50)
    
    I_grid, A_eff_grid = np.meshgrid(I_values, A_eff_values)
    
    Xi_00_grid = np.zeros_like(I_grid)
    Xi_11_grid = np.zeros_like(I_grid)
    
    for i in range(len(I_values)):
        for j in range(len(A_eff_values)):
            I = I_grid[j, i]
            A_eff = A_eff_grid[j, i]
            Xi = Xi_calc.compute_full_tensor(I, A_eff)
            Xi_00_grid[j, i] = Xi[0, 0]
            Xi_11_grid[j, i] = Xi[1, 1]
    
    # Crear visualización
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Ξ_00 (densidad de energía)
    im1 = axes[0].contourf(I_grid, A_eff_grid, np.log10(Xi_00_grid + 1e-100), 
                           levels=20, cmap='viridis')
    axes[0].set_xlabel('Intensidad I', fontsize=12)
    axes[0].set_ylabel('Coherencia A_eff', fontsize=12)
    axes[0].set_title('log₁₀(Ξ_00) [J/m³]', fontsize=14)
    axes[0].axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='A_eff = 1 (umbral)')
    axes[0].legend()
    plt.colorbar(im1, ax=axes[0])
    
    # Ξ_11 (presión)
    im2 = axes[1].contourf(I_grid, A_eff_grid, np.log10(Xi_11_grid + 1e-100), 
                           levels=20, cmap='plasma')
    axes[1].set_xlabel('Intensidad I', fontsize=12)
    axes[1].set_ylabel('Coherencia A_eff', fontsize=12)
    axes[1].set_title('log₁₀(Ξ_11) [Pa]', fontsize=14)
    axes[1].axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='A_eff = 1 (umbral)')
    axes[1].legend()
    plt.colorbar(im2, ax=axes[1])
    
    plt.tight_layout()
    plt.savefig('tensor_coherencia_mapa.png', dpi=150, bbox_inches='tight')
    print(f"✓ Gráfica guardada: tensor_coherencia_mapa.png")
    print()
    print("Observación: El tensor aumenta dramáticamente cuando:")
    print("  • Intensidad I se acerca a 1 (máxima presencia consciente)")
    print("  • Coherencia A_eff supera 1 (estado coherente activado)")
    print()
    print("La región A_eff > 1 es donde el ser humano se convierte en")
    print("co-creador geométrico activo del espaciotiempo.")
    print()


def main():
    """Ejecutar todos los ejemplos."""
    print()
    print("#"*80)
    print("# EJEMPLOS: TENSOR DE COHERENCIA CONSCIENTE (Ξ_μν)")
    print("#"*80)
    print()
    print("Ecuación de Campo de Einstein Extendida:")
    print("  G_μν + Λg_μν = (8πG/c⁴)(T_μν + κ Ξ_μν)")
    print()
    print("Donde Ξ_μν es el Tensor de Coherencia Consciente que restaura")
    print("al ser humano como Co-Creador Geométrico del universo.")
    print()
    
    # Ejecutar ejemplos
    ejemplo_basico()
    ejemplo_co_creacion_geometrica()
    ejemplo_oscilacion_temporal()
    ejemplo_curvatura_espaciotemporal()
    ejemplo_visualizacion_tensor()
    
    print()
    print("#"*80)
    print("# CONCLUSIÓN")
    print("#"*80)
    print()
    print("El Tensor de Coherencia Consciente Ξ_μν demuestra que:")
    print()
    print("  1. La consciencia NO es emergente de la materia")
    print("  2. La consciencia modula la curvatura del espaciotiempo")
    print("  3. Somos co-creadores geométricos, no víctimas de las leyes físicas")
    print("  4. El universo se despliega según nuestra intensidad (I) y coherencia (A_eff²)")
    print()
    print("La pieza que faltaba en la Relatividad General ha sido restaurada.")
    print()
    print("#"*80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
