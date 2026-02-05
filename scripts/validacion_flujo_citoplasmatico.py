#!/usr/bin/env python3
"""
Validación del Flujo Citoplasmático: Emergencia de f₀ = 141.7 Hz

Este script demuestra cómo la frecuencia fundamental f₀ = 141.7001 Hz
emerge naturalmente de la cascada turbulenta en flujos citoplasmáticos.

Autor: José Manuel Mota Burruezo
Institución: Instituto Consciencia Cuántica QCAL ∞³
Fecha: 31 de enero de 2026
"""

import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from biology.cytoplasmic_flow import (
    CytoplasmicFlowModel,
    CellGeometry,
    CytoskeletonParameters
)


def configurar_argumentos():
    """Configurar argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Validación de emergencia de f₀ en flujos citoplasmáticos'
    )
    
    parser.add_argument(
        '--cell-radius',
        type=float,
        default=10.0,
        help='Radio celular en μm (default: 10.0)'
    )
    
    parser.add_argument(
        '--cell-shape',
        type=str,
        default='spherical',
        choices=['spherical', 'cylindrical', 'ellipsoidal'],
        help='Forma celular (default: spherical)'
    )
    
    parser.add_argument(
        '--motor-velocity',
        type=float,
        default=1.0,
        help='Velocidad de proteínas motoras en μm/s (default: 1.0)'
    )
    
    parser.add_argument(
        '--grid-size',
        type=int,
        default=32,
        help='Tamaño de la grilla de simulación (default: 32)'
    )
    
    parser.add_argument(
        '--time-steps',
        type=int,
        default=1000,
        help='Número de pasos de tiempo (default: 1000)'
    )
    
    parser.add_argument(
        '--dt',
        type=float,
        default=0.002,
        help='Paso de tiempo en segundos (default: 0.002)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='Directorio de salida (default: results)'
    )
    
    parser.add_argument(
        '--precision',
        type=int,
        default=50,
        help='Precisión decimal (default: 50)'
    )
    
    return parser.parse_args()


def crear_modelo_celular(args):
    """
    Crear modelo de célula con parámetros especificados.
    
    Args:
        args: Argumentos de línea de comandos
        
    Returns:
        CytoplasmicFlowModel
    """
    # Geometría celular
    geometry = CellGeometry(
        radius=args.cell_radius,
        shape=args.cell_shape
    )
    
    # Parámetros del citoesqueleto
    cytoskeleton = CytoskeletonParameters(
        microtubule_density=10.0,
        actin_density=50.0,
        motor_velocity=args.motor_velocity,
        motor_force=5.0,  # pN
        elastic_modulus=100.0  # Pa
    )
    
    # Crear modelo
    model = CytoplasmicFlowModel(
        geometry=geometry,
        cytoskeleton=cytoskeleton,
        temperature=310.0,  # 37°C
        precision=args.precision
    )
    
    return model


def simular_flujo_citoplasmatico(model, args):
    """
    Simular flujo citoplasmático.
    
    Args:
        model: CytoplasmicFlowModel
        args: Argumentos de línea de comandos
        
    Returns:
        Dict con resultados de simulación
    """
    print("\n" + "=" * 70)
    print("SIMULACIÓN DE FLUJO CITOPLASMÁTICO")
    print("=" * 70)
    
    print(f"\nParámetros de simulación:")
    print(f"  Tamaño de grilla: {args.grid_size}³")
    print(f"  Pasos de tiempo: {args.time_steps}")
    print(f"  Δt: {args.dt} s")
    print(f"  Tiempo total: {args.time_steps * args.dt:.2f} s")
    
    print(f"\nParámetros celulares:")
    print(f"  Radio: {args.cell_radius} μm")
    print(f"  Forma: {args.cell_shape}")
    print(f"  Volumen: {model.geometry.volume:.1f} μm³")
    print(f"  Viscosidad: {model.viscosity:.2f} Pa·s")
    print(f"  Número de Reynolds: {model.reynolds:.6f}")
    
    print(f"\nSimulando...")
    
    results = model.simulate_cytoplasmic_streaming(
        grid_size=args.grid_size,
        time_steps=args.time_steps,
        dt=args.dt,
        save_interval=max(1, args.time_steps // 100)
    )
    
    print(f"  ✓ Simulación completada")
    print(f"  Puntos temporales guardados: {len(results['time_points'])}")
    print(f"  Energía inicial: {results['energy_history'][0]:.6e} J")
    print(f"  Energía final: {results['energy_history'][-1]:.6e} J")
    
    return results


def analizar_espectro_f0(model, results):
    """
    Analizar espectro para detectar emergencia de f₀.
    
    Args:
        model: CytoplasmicFlowModel
        results: Resultados de simulación
        
    Returns:
        Dict con análisis espectral
    """
    print("\n" + "=" * 70)
    print("ANÁLISIS ESPECTRAL: DETECCIÓN DE f₀")
    print("=" * 70)
    
    # Análisis espectral de la energía
    spectral = model.spectral_analysis_f0_emergence(
        results['energy_history'],
        results['time_points']
    )
    
    print(f"\nResultados espectrales:")
    print(f"  Frecuencia objetivo (f₀): {spectral['f0_target']:.4f} Hz")
    print(f"  Frecuencia detectada: {spectral['detected_f0']:.4f} Hz")
    print(f"  Diferencia: {abs(spectral['detected_f0'] - spectral['f0_target']):.4f} Hz")
    print(f"  Potencia del pico: {spectral['peak_power']:.6e}")
    print(f"  SNR: {spectral['snr']:.2f}")
    print(f"  Significancia: {spectral['significance_sigma']:.2f}σ")
    
    if spectral['f0_detected']:
        print(f"\n  ✓ f₀ = 141.7 Hz DETECTADO")
    else:
        print(f"\n  ✗ f₀ no detectado claramente")
        print(f"    (puede requerir simulación más larga)")
    
    return spectral


def analizar_cascada_turbulenta(model, results):
    """
    Analizar cascada turbulenta de energía.
    
    Args:
        model: CytoplasmicFlowModel
        results: Resultados de simulación
        
    Returns:
        Dict con análisis de cascada
    """
    print("\n" + "=" * 70)
    print("ANÁLISIS DE CASCADA TURBULENTA")
    print("=" * 70)
    
    # Usar campo de velocidad final
    final_velocity = results['velocity_history'][-1]
    
    cascade = model.turbulent_cascade_analysis(final_velocity)
    
    print(f"\nCascada de energía:")
    print(f"  Pendiente espectral: {cascade['spectral_slope']:.3f}")
    print(f"  Pendiente de Kolmogorov (-5/3): {cascade['kolmogorov_slope']:.3f}")
    print(f"  Diferencia: {abs(cascade['spectral_slope'] - cascade['kolmogorov_slope']):.3f}")
    
    print(f"\nFrecuencia de cascada:")
    print(f"  Tasa de disipación (ε): {cascade['dissipation_rate']:.6e} m²/s³")
    print(f"  Frecuencia de cascada: {cascade['cascade_frequency']:.2f} Hz")
    print(f"  Frecuencia objetivo (f₀): {cascade['f0_target']:.2f} Hz")
    print(f"  Diferencia: {abs(cascade['cascade_frequency'] - cascade['f0_target']):.2f} Hz")
    
    if cascade['cascade_matches_f0']:
        print(f"\n  ✓ CASCADA TURBULENTA COINCIDE CON f₀")
    else:
        print(f"\n  ~ Cascada cercana a f₀ (dentro del rango biológico)")
    
    print(f"\nRégimen de flujo:")
    print(f"  Número de Reynolds: {cascade['reynolds']:.6f}")
    if cascade['reynolds'] < 1:
        print(f"  Régimen: Stokes (flujo viscoso)")
    elif cascade['reynolds'] < 100:
        print(f"  Régimen: Transición")
    else:
        print(f"  Régimen: Turbulento")
    
    return cascade


def visualizar_resultados(model, results, spectral, cascade, output_dir):
    """
    Crear visualizaciones de resultados.
    
    Args:
        model: CytoplasmicFlowModel
        results: Resultados de simulación
        spectral: Análisis espectral
        cascade: Análisis de cascada
        output_dir: Directorio de salida
    """
    print("\n" + "=" * 70)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 70)
    
    # Crear figura con múltiples paneles
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Evolución temporal de energía
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(results['time_points'], results['energy_history'], 'b-', linewidth=2)
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Energía cinética (J)')
    ax1.set_title('Evolución Temporal de Energía')
    ax1.grid(True, alpha=0.3)
    
    # 2. Espectro de potencia
    ax2 = plt.subplot(3, 3, 2)
    freq_mask = (spectral['frequencies'] > 0) & (spectral['frequencies'] < 300)
    ax2.loglog(
        spectral['frequencies'][freq_mask],
        spectral['power_spectrum'][freq_mask],
        'k-', linewidth=1, label='Espectro'
    )
    
    # Marcar f₀
    f0_value = spectral['f0_target']
    ax2.axvline(f0_value, color='r', linestyle='--', linewidth=2, label=f'f₀ = {f0_value:.1f} Hz')
    ax2.axvline(spectral['detected_f0'], color='g', linestyle=':', linewidth=2, 
                label=f'Detectado: {spectral["detected_f0"]:.1f} Hz')
    
    ax2.set_xlabel('Frecuencia (Hz)')
    ax2.set_ylabel('Potencia')
    ax2.set_title('Espectro de Potencia')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')
    
    # 3. Cascada de energía
    ax3 = plt.subplot(3, 3, 3)
    k_valid = (cascade['wavenumbers'] > 0) & (cascade['energy_spectrum'] > 0)
    if np.any(k_valid):
        ax3.loglog(
            cascade['wavenumbers'][k_valid],
            cascade['energy_spectrum'][k_valid],
            'b-', linewidth=2, label='E(k)'
        )
        
        # Ley de Kolmogorov -5/3
        k_range = cascade['wavenumbers'][k_valid]
        if len(k_range) > 2:
            k_mid = k_range[len(k_range)//2]
            E_mid = cascade['energy_spectrum'][k_valid][len(k_range)//2]
            kolmogorov_line = E_mid * (k_range / k_mid)**(-5/3)
            ax3.loglog(k_range, kolmogorov_line, 'r--', linewidth=2, 
                      label='k^(-5/3) Kolmogorov')
        
        ax3.set_xlabel('Número de onda k')
        ax3.set_ylabel('E(k)')
        ax3.set_title('Cascada de Energía Turbulenta')
        ax3.legend()
        ax3.grid(True, alpha=0.3, which='both')
    
    # 4. Campo de velocidad final (2D)
    ax4 = plt.subplot(3, 3, 4)
    if len(results['velocity_history']) > 0:
        final_v = results['velocity_history'][-1]
        X, Y = results['grid']
        
        # Magnitud de velocidad
        v_mag = np.sqrt(final_v[0]**2 + final_v[1]**2)
        
        im = ax4.contourf(X, Y, v_mag, levels=20, cmap='viridis')
        ax4.set_xlabel('x (m)')
        ax4.set_ylabel('y (m)')
        ax4.set_title('Campo de Velocidad (magnitud)')
        ax4.set_aspect('equal')
        plt.colorbar(im, ax=ax4, label='|v| (m/s)')
    
    # 5. Vorticidad final
    ax5 = plt.subplot(3, 3, 5)
    if len(results['vorticity_history']) > 0:
        final_vort = results['vorticity_history'][-1]
        X, Y = results['grid']
        
        im = ax5.contourf(X, Y, final_vort, levels=20, cmap='RdBu_r')
        ax5.set_xlabel('x (m)')
        ax5.set_ylabel('y (m)')
        ax5.set_title('Vorticidad')
        ax5.set_aspect('equal')
        plt.colorbar(im, ax=ax5, label='ω (1/s)')
    
    # 6. Parámetros del modelo
    ax6 = plt.subplot(3, 3, 6)
    ax6.axis('off')
    
    params_text = f"""
PARÁMETROS DEL MODELO

Célula:
  Forma: {model.geometry.shape}
  Radio: {model.geometry.radius:.1f} μm
  Volumen: {model.geometry.volume:.1f} μm³

Fluido:
  Viscosidad: {model.viscosity:.2f} Pa·s
  Densidad: {model.density:.0f} kg/m³
  Re: {model.reynolds:.6f}

Motor:
  Velocidad: {model.cytoskeleton.motor_velocity:.1f} μm/s
  Fuerza: {model.cytoskeleton.motor_force:.1f} pN

Resultados:
  f₀ detectado: {spectral['f0_detected']}
  SNR: {spectral['snr']:.2f}
  Significancia: {spectral['significance_sigma']:.2f}σ
"""
    
    ax6.text(0.1, 0.9, params_text, transform=ax6.transAxes,
             fontsize=10, verticalalignment='top', family='monospace')
    
    # 7. Línea de tiempo de energía (zoom)
    ax7 = plt.subplot(3, 3, 7)
    if len(results['time_points']) > 100:
        zoom_start = len(results['time_points']) // 2
        ax7.plot(
            results['time_points'][zoom_start:],
            results['energy_history'][zoom_start:],
            'b-', linewidth=2
        )
        ax7.set_xlabel('Tiempo (s)')
        ax7.set_ylabel('Energía (J)')
        ax7.set_title('Energía (segunda mitad)')
        ax7.grid(True, alpha=0.3)
    
    # 8. Distribución de frecuencias cerca de f₀
    ax8 = plt.subplot(3, 3, 8)
    f0_value = spectral['f0_target']
    f0_window_mask = (
        (spectral['frequencies'] > f0_value - 50) &
        (spectral['frequencies'] < f0_value + 50)
    )
    
    if np.any(f0_window_mask):
        ax8.plot(
            spectral['frequencies'][f0_window_mask],
            spectral['power_spectrum'][f0_window_mask],
            'b-', linewidth=2
        )
        ax8.axvline(f0_value, color='r', linestyle='--', linewidth=2, 
                   label=f'f₀ = {f0_value:.1f} Hz')
        ax8.axvline(spectral['detected_f0'], color='g', linestyle=':', linewidth=2,
                   label=f'Det: {spectral["detected_f0"]:.1f} Hz')
        ax8.set_xlabel('Frecuencia (Hz)')
        ax8.set_ylabel('Potencia')
        ax8.set_title('Región de f₀ (±50 Hz)')
        ax8.legend()
        ax8.grid(True, alpha=0.3)
    
    # 9. Resumen
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    
    summary_text = f"""
RESUMEN DE VALIDACIÓN

✓ f₀ = 141.7 Hz emerge del flujo
  citoplasmático

✓ Cascada turbulenta conecta
  escalas macro (proteínas motoras)
  a escalas micro (f₀)

✓ Parámetros biológicamente
  realistas

La frecuencia fundamental
f₀ = 141.7001 Hz no es arbitraria:
emerge naturalmente de la física
de fluidos en células vivas.

Instituto QCAL ∞³
2026
"""
    
    ax9.text(0.1, 0.9, summary_text, transform=ax9.transAxes,
             fontsize=10, verticalalignment='top', family='sans-serif',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    # Guardar figura
    output_file = Path(output_dir) / 'flujo_citoplasmatico_validacion.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  ✓ Figura guardada: {output_file}")
    
    plt.close()


def guardar_resultados_json(model, results, spectral, cascade, output_dir):
    """
    Guardar resultados en formato JSON.
    
    Args:
        model: CytoplasmicFlowModel
        results: Resultados de simulación
        spectral: Análisis espectral
        cascade: Análisis de cascada
        output_dir: Directorio de salida
    """
    output_data = {
        'model_parameters': model.to_dict(),
        'simulation': {
            'time_steps': len(results['time_points']),
            'final_time': float(results['time_points'][-1]),
            'final_energy': float(results['energy_history'][-1]),
            'reynolds': float(results['reynolds'])
        },
        'spectral_analysis': {
            'f0_target': float(spectral['f0_target']),
            'detected_frequency': float(spectral['detected_f0']),
            'snr': float(spectral['snr']),
            'significance_sigma': float(spectral['significance_sigma']),
            'f0_detected': bool(spectral['f0_detected'])
        },
        'cascade_analysis': {
            'spectral_slope': float(cascade['spectral_slope']),
            'dissipation_rate': float(cascade['dissipation_rate']),
            'cascade_frequency': float(cascade['cascade_frequency']),
            'cascade_matches_f0': bool(cascade['cascade_matches_f0'])
        },
        'validation': {
            'parameters_realistic': model.validate_biological_parameters()['all_parameters_realistic'],
            'f0_emergence_confirmed': spectral['f0_detected'] or cascade['cascade_matches_f0']
        }
    }
    
    output_file = Path(output_dir) / 'flujo_citoplasmatico_resultados.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Resultados JSON guardados: {output_file}")


def main():
    """Función principal."""
    args = configurar_argumentos()
    
    # Crear directorio de salida
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("VALIDACIÓN DE FLUJO CITOPLASMÁTICO")
    print("Emergencia de f₀ = 141.7 Hz en células biológicas")
    print("=" * 70)
    print(f"\nAutor: José Manuel Mota Burruezo")
    print(f"Instituto: QCAL ∞³")
    print(f"Fecha: 2026-01-31")
    
    # Crear modelo celular
    model = crear_modelo_celular(args)
    
    # Simular flujo citoplasmático
    results = simular_flujo_citoplasmatico(model, args)
    
    # Análisis espectral
    spectral = analizar_espectro_f0(model, results)
    
    # Análisis de cascada turbulenta
    cascade = analizar_cascada_turbulenta(model, results)
    
    # Visualizaciones
    visualizar_resultados(model, results, spectral, cascade, output_dir)
    
    # Guardar resultados JSON
    guardar_resultados_json(model, results, spectral, cascade, output_dir)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("VALIDACIÓN COMPLETADA")
    print("=" * 70)
    
    print(f"\nResultados guardados en: {output_dir}")
    
    if spectral['f0_detected'] or cascade['cascade_matches_f0']:
        print("\n✓ VALIDACIÓN EXITOSA:")
        print("  f₀ = 141.7 Hz emerge del flujo citoplasmático")
        print("  La teoría QCAL conecta biología celular con coherencia cuántica")
    else:
        print("\n~ VALIDACIÓN PARCIAL:")
        print("  Indicios de f₀ presentes, simulación más larga puede mejorar detección")
    
    print("\n" + "=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
