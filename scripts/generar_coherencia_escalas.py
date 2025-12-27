#!/usr/bin/env python3
"""
Script para generar visualización de coherencia de f₀ en distintas escalas.
Crea la imagen coherence_f0_scales.png que muestra la consistencia de la 
frecuencia fundamental 141.7001 Hz a través de escalas Planck, LIGO y CMB.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Datos simulados representativos para las curvas y frecuencias
frecuencia_f0 = 141.7001

# Rangos de escala para cada dominio (valores hipotéticos para visualización)
escalas = {
    'Planck': np.logspace(-44, -35, 100),  # en metros
    'LIGO': np.logspace(1, 3, 100),        # en Hz convertido a metros equivalente (simplificación)
    'CMB': np.logspace(-3, 1, 100)          # en escalas cosmológicas, grados o Hz
}

# Funciones para las diferentes curvas (hipotéticas para la demostración)
def zeta_curve(s):
    """Función zeta representativa"""
    return np.abs(np.sin(np.log10(s)*5)) * 1e-2

def modulation_eeg(s):
    """Modulación EEG representativa"""
    return 0.5 + 0.5 * np.sin(np.log10(s)*2) * 1e-2

def gravitational_waves(s):
    """Ondas gravitacionales representativas"""
    return 0.3 + 0.7 * np.exp(-np.log10(s)**2 / 10)

def cmb_pattern(s):
    """Patrón CMB representativo"""
    return 0.2 + 0.3 * np.cos(np.log10(s)*3)

# Convertir frecuencia f0 a las mismas escalas como referencia
frecuencia_reference = {
    'Planck': 1e-35,  # Escala Planck - posición arbitraria para f0
    'LIGO': frecuencia_f0,  # Hz directa
    'CMB': 1e0
}

def generar_visualizacion():
    """Genera la visualización de coherencia de f₀ en distintas escalas"""
    
    plt.figure(figsize=(12, 7))

    # Graficar en escala logarítmica para cada dominio
    for dominio, scale in escalas.items():
        plt.plot(scale, zeta_curve(scale), label=f'ζ(s) {dominio}', alpha=0.7)
        plt.plot(scale, modulation_eeg(scale), label=f'Modulación EEG {dominio}', alpha=0.7)
        plt.plot(scale, gravitational_waves(scale), label=f'Ondas gravitacionales {dominio}', alpha=0.7)
        plt.plot(scale, cmb_pattern(scale), label=f'Patrón CMB {dominio}', alpha=0.7)
        # Marcar la frecuencia f0 en el dominio correspondiente
        plt.axvline(frecuencia_reference[dominio], linestyle='--', linewidth=2, 
                   label=f'f₀ = {frecuencia_f0} Hz en {dominio}')

    plt.xscale('log')
    plt.xlabel('Escala (log)', fontsize=12)
    plt.ylabel('Amplitud (relativa)', fontsize=12)
    plt.title('Visualización de coherencia de $f_0$ en distintas escalas', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
    plt.tight_layout()
    
    # Determinar directorio de salida
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'results', 'figures')
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar en el directorio de resultados
    output_path = os.path.join(output_dir, 'coherence_f0_scales.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Imagen guardada en: {output_path}")
    
    # También guardar en la raíz para fácil acceso en README
    root_output_path = os.path.join(project_root, 'coherence_f0_scales.png')
    plt.savefig(root_output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Imagen guardada en: {root_output_path}")
    
    plt.close()
    
    return output_path, root_output_path

if __name__ == "__main__":
    print("🌌 Generando visualización de coherencia de f₀...")
    print(f"Frecuencia objetivo: {frecuencia_f0} Hz")
    print()
    
    output_path, root_output_path = generar_visualizacion()
    
    print()
    print("=" * 60)
    print("✅ Visualización generada exitosamente")
    print("=" * 60)
    print()
    print("📊 Archivos generados:")
    print(f"  - {output_path}")
    print(f"  - {root_output_path}")
    print()
    print("📝 Para incluir en README.md, usar:")
    print("  ![Coherencia f₀](coherence_f0_scales.png)")
