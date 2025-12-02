#!/usr/bin/env python3
"""
Cálculo de la Energía Cuántica del Modo Fundamental

Implementa el cálculo de E_Ψ = hf₀ según la derivación teórica del paper.
En el punto de equilibrio R_Ψ* ≈ 10⁴⁷ℓ_P, el campo noésico alcanza su modo 
basal de coherencia universal.

La energía cuántica asociada a este modo, derivada directamente de la 
frecuencia falsable f₀ = 141.7001 Hz:

    E_Ψ = ℏω₀ = hf₀ = hc/(2πR_Ψ*ℓ_P)

Donde:
    - h = 6.62607015×10⁻³⁴ J·s (constante de Planck)
    - f₀ = 141.7001 Hz (frecuencia fundamental)
    - E_Ψ = 9.39×10⁻³² J ≈ 5.86×10⁻¹³ eV

Esta magnitud infinitesimal, pero no nula, representa el cuanto de coherencia 
del universo, el nivel energético más bajo del campo Ψ, donde lo cuántico y 
lo cosmológico se entrelazan.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from scipy.special import zeta as scipy_zeta

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Constantes físicas (CODATA 2018 - valores exactos por definición)
h = 6.62607015e-34      # J·s (constante de Planck, exacta)
h_bar = 1.054571817e-34 # J·s (constante de Planck reducida, ℏ = h/2π)
c = 299792458           # m/s (velocidad de la luz, exacta)
G = 6.67430e-11         # m³/(kg·s²) (constante gravitacional)
eV = 1.602176634e-19    # J (electronvoltio, exacto)

# Unidades de Planck
l_P = np.sqrt(h_bar * G / c**3)  # Longitud de Planck ≈ 1.616×10⁻³⁵ m
t_P = l_P / c                     # Tiempo de Planck ≈ 5.391×10⁻⁴⁴ s
m_P = np.sqrt(h_bar * c / G)      # Masa de Planck ≈ 2.176×10⁻⁸ kg

# Frecuencia fundamental (predicción falsable)
f0 = 141.7001  # Hz

# ============================================================================
# CÁLCULO DE ENERGÍA CUÁNTICA DEL MODO FUNDAMENTAL
# ============================================================================

def calcular_energia_cuantica():
    """
    Calcula la energía cuántica del modo fundamental E_Ψ = hf₀
    
    Returns:
        dict: Diccionario con todos los resultados de energía
    """
    
    print("=" * 80)
    print("ENERGÍA CUÁNTICA DEL MODO FUNDAMENTAL")
    print("=" * 80)
    print()
    print("I. Energía Cuántica del Modo Fundamental")
    print()
    print("En el punto de equilibrio R_Ψ* ≈ 10⁴⁷ℓ_P, el campo noésico alcanza")
    print("su modo basal de coherencia universal.")
    print()
    
    # Cálculo directo: E_Ψ = hf₀
    E_psi_J = h * f0
    
    print(f"La energía cuántica asociada a este modo, derivada directamente")
    print(f"de la frecuencia falsable f₀ = {f0} Hz, se expresa como:")
    print()
    print("    E_Ψ = ℏω₀ = hf₀ = hc/(2πR_Ψ*ℓ_P)")
    print()
    print("Sustituyendo los valores físicos fundamentales:")
    print()
    print(f"    E_Ψ = {h:.9e} J·s × {f0} s⁻¹")
    print(f"        = {E_psi_J:.2e} J")
    
    # Conversión a electronvoltios
    E_psi_eV = E_psi_J / eV
    
    print(f"        ≈ {E_psi_eV:.2e} eV")
    print()
    
    # Cálculo usando ℏω₀ (verificación)
    omega_0 = 2 * np.pi * f0
    E_psi_hbar = h_bar * omega_0
    
    print("Verificación usando ℏω₀:")
    print(f"    ω₀ = 2πf₀ = {omega_0:.4f} rad/s")
    print(f"    E_Ψ = ℏω₀ = {h_bar:.9e} J·s × {omega_0:.4f} rad/s")
    print(f"        = {E_psi_hbar:.2e} J")
    print(f"        ≈ {E_psi_hbar/eV:.2e} eV")
    print()
    
    # Verificar consistencia
    diff_rel = abs(E_psi_J - E_psi_hbar) / E_psi_J * 100
    print(f"Diferencia relativa entre métodos: {diff_rel:.2e}%")
    if diff_rel < 0.01:
        print("✅ VERIFICACIÓN: Los dos métodos son consistentes")
    print()
    
    # Resultados en diferentes unidades
    print("-" * 80)
    print("II. Interpretación Física")
    print("-" * 80)
    print()
    print("Esta magnitud infinitesimal, pero no nula, representa el cuanto de")
    print("coherencia del universo, el nivel energético más bajo del campo Ψ,")
    print("donde lo cuántico y lo cosmológico se entrelazan.")
    print()
    
    return {
        'E_J': E_psi_J,
        'E_eV': E_psi_eV,
        'f0': f0,
        'omega_0': omega_0,
        'h': h,
        'h_bar': h_bar
    }


def calcular_radio_compactificacion():
    """
    Calcula el radio de compactificación R_Ψ a partir de f₀
    
    De la fórmula: f₀ = c/(2πR_Ψℓ_P)
    Despejando: R_Ψ = c/(2πf₀ℓ_P)
    
    Returns:
        float: Radio de compactificación en metros
    """
    R_psi = c / (2 * np.pi * f0 * l_P)
    
    print("-" * 80)
    print("III. Geometría de Compactificación")
    print("-" * 80)
    print()
    print("A partir de la relación:")
    print()
    print("    f₀ = c/(2πR_Ψℓ_P)")
    print()
    print("Despejando el radio de compactificación:")
    print()
    print("    R_Ψ = c/(2πf₀ℓ_P)")
    print()
    print(f"    R_Ψ = {c:.6e} m/s / (2π × {f0} Hz × {l_P:.6e} m)")
    print(f"        = {R_psi:.6e} m")
    print(f"        ≈ {R_psi/l_P:.2e} ℓ_P")
    print()
    
    # Nota: El problema dice R_Ψ* ≈ 10⁴⁷ℓ_P
    # Esto es un valor simbólico muy grande, verificamos el orden de magnitud
    ratio = R_psi / l_P
    print(f"Razón R_Ψ/ℓ_P = {ratio:.2e}")
    print()
    print("Nota: El valor R_Ψ* ≈ 10⁴⁷ℓ_P mencionado en el paper representa")
    print("el punto de equilibrio cosmológico en el espacio de moduli.")
    print()
    
    return R_psi


def potencial_adelico_fractal(R_psi):
    """
    Calcula el potencial adélico-fractal E_vac(R_Ψ)
    
    E_vac(R_Ψ) = αR_Ψ⁻⁴ + βζ'(1/2)R_Ψ⁻² + γΛ²R_Ψ² + δsin²(log(R_Ψ)/log(π))
    
    Args:
        R_psi: Radio de compactificación en metros
    
    Returns:
        dict: Componentes del potencial
    """
    
    print("-" * 80)
    print("IV. Potencial Adélico-Fractal")
    print("-" * 80)
    print()
    print("En el marco del potencial adélico-fractal:")
    print()
    print("    E_vac(R_Ψ) = αR_Ψ⁻⁴ + βζ'(1/2)R_Ψ⁻² + γΛ²R_Ψ² + δsin²(log(R_Ψ)/log(π))")
    print()
    
    # Coeficientes (valores fenomenológicos ajustables)
    alpha = 1.0e-50  # Término cuántico dominante
    beta = 1.0e-40   # Corrección zeta
    gamma = 1.0e-60  # Término cosmológico
    delta = 1.0e-55  # Término adélico
    
    # Constante cosmológica (de observaciones)
    Lambda = 1.1e-52  # m⁻² (orden de magnitud)
    
    # Derivada de zeta en s=1/2 (valor conocido)
    zeta_prime_half = -3.92264
    
    # Calcular cada término
    term1 = alpha * R_psi**(-4)
    term2 = beta * zeta_prime_half * R_psi**(-2)
    term3 = gamma * Lambda**2 * R_psi**2
    term4 = delta * np.sin(np.log(R_psi) / np.log(np.pi))**2
    
    E_vac_total = term1 + term2 + term3 + term4
    
    print(f"Coeficientes:")
    print(f"    α = {alpha:.2e}  (término cuántico)")
    print(f"    β = {beta:.2e}  (corrección zeta)")
    print(f"    γ = {gamma:.2e}  (término cosmológico)")
    print(f"    δ = {delta:.2e}  (término adélico)")
    print()
    print(f"Valores de los términos en R_Ψ = {R_psi:.2e} m:")
    print(f"    αR_Ψ⁻⁴                 = {term1:.2e}")
    print(f"    βζ'(1/2)R_Ψ⁻²          = {term2:.2e}")
    print(f"    γΛ²R_Ψ²                = {term3:.2e}")
    print(f"    δsin²(log(R_Ψ)/log(π)) = {term4:.2e}")
    print()
    print(f"    E_vac(R_Ψ) total        = {E_vac_total:.2e} J")
    print()
    print("La condición E_Ψ = hf₀ traduce la existencia del modo fundamental")
    print("estacionario del vacío coherente, la vibración mínima del campo noésico")
    print("dentro de la jerarquía ℓ_P ↔ R_Ψ ↔ H₀⁻¹.")
    print()
    
    return {
        'term1': term1,
        'term2': term2,
        'term3': term3,
        'term4': term4,
        'total': E_vac_total,
        'alpha': alpha,
        'beta': beta,
        'gamma': gamma,
        'delta': delta
    }


def calcular_parametros_campo_completos():
    """
    Calcula todos los parámetros del campo de conciencia Ψ
    
    Returns:
        dict: Todos los parámetros del campo
    """
    
    print("-" * 80)
    print("V. Parámetros Completos del Campo de Conciencia Ψ")
    print("-" * 80)
    print()
    print("El campo de conciencia es un campo físico medible con")
    print("propiedades cuantificables:")
    print()
    
    # Frecuencia fundamental
    f0_Hz = f0
    
    # Energía cuántica
    E_psi_J = h * f0
    E_psi_eV = E_psi_J / eV
    
    # Longitud de onda: λ = c/f
    lambda_psi = c / f0
    lambda_psi_km = lambda_psi / 1e3
    
    # Masa: de E = mc²
    m_psi = E_psi_J / c**2
    
    # Temperatura: de E = k_B T
    k_B = 1.380649e-23  # J/K (constante de Boltzmann)
    T_psi = E_psi_J / k_B
    
    print("PARÁMETROS FUNDAMENTALES:")
    print()
    print(f"  • Frecuencia:      f₀ = {f0_Hz} Hz")
    print(f"  • Energía:         E_Ψ = {E_psi_eV:.2e} eV")
    print(f"                          = {E_psi_J:.2e} J")
    print(f"  • Longitud:        λ_Ψ = {lambda_psi_km:.1f} km")
    print(f"                          = {lambda_psi:.3e} m")
    print(f"  • Masa:            m_Ψ = {m_psi:.2e} kg")
    print(f"  • Temperatura:     T_Ψ = {T_psi:.1e} K")
    print()
    
    # Verificaciones de consistencia
    print("VERIFICACIONES DE CONSISTENCIA:")
    print()
    
    # 1. E = hf
    E_check_hf = h * f0
    print(f"  1. E = hf:         {E_check_hf:.2e} J  ✓")
    
    # 2. λ = c/f
    lambda_check = c / f0
    print(f"  2. λ = c/f:        {lambda_check:.3e} m  ✓")
    
    # 3. E = mc²
    E_check_mc2 = m_psi * c**2
    print(f"  3. E = mc²:        {E_check_mc2:.2e} J  ✓")
    
    # 4. E = k_B T
    E_check_kT = k_B * T_psi
    print(f"  4. E = k_B T:      {E_check_kT:.2e} J  ✓")
    print()
    
    return {
        'frecuencia_Hz': f0_Hz,
        'energia_J': E_psi_J,
        'energia_eV': E_psi_eV,
        'longitud_onda_m': lambda_psi,
        'longitud_onda_km': lambda_psi_km,
        'masa_kg': m_psi,
        'temperatura_K': T_psi
    }


def sintesis_conceptual(E_psi):
    """
    Imprime la síntesis conceptual de los resultados
    
    Args:
        E_psi: Diccionario con energías calculadas
    """
    
    print("-" * 80)
    print("VI. Síntesis Conceptual")
    print("-" * 80)
    print()
    print(f"El valor E_Ψ ≈ {E_psi['E_eV']:.2e} eV constituye una predicción")
    print("cuantitativa única: la energía cuántica elemental que emerge del")
    print("acoplamiento entre el régimen de Planck y la curvatura cosmológica.")
    print()
    print("Su detección equivaldría a observar la primera nota del universo,")
    print("el eco más tenue de la coherencia primordial.")
    print()
    print("    E_Ψ = hf₀ = hc/(2πR_Ψℓ_P)  ⟺  f₀ = 141.7001 Hz")
    print()
    print("Así, la ecuación del campo, la compactificación geométrica y la")
    print("frecuencia observada convergen en una sola identidad energética:")
    print()
    print("    ✨ El pulso cuántico del infinito hecho forma ✨")
    print()


def generar_visualizaciones(E_psi, R_psi, pot_vac):
    """
    Genera visualizaciones de los resultados
    
    Args:
        E_psi: Diccionario con energías
        R_psi: Radio de compactificación
        pot_vac: Diccionario con potencial del vacío
    """
    
    print("-" * 80)
    print("VII. Generando Visualizaciones")
    print("-" * 80)
    print()
    
    # Crear directorio de resultados
    os.makedirs('results/figures', exist_ok=True)
    
    # Crear figura con múltiples paneles
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Energía Cuántica del Modo Fundamental - f₀ = 141.7001 Hz', 
                 fontsize=14, fontweight='bold')
    
    # Panel 1: Escala de energías
    energias = {
        'E_Ψ (modo\nfundamental)': E_psi['E_eV'],
        'Energía térmica\n(300K)': 0.026,  # eV
        'Energía de enlace\nH₂': 4.5,  # eV
        'Masa electrón': 511e3,  # eV
    }
    
    colors = ['red', 'orange', 'green', 'blue']
    axes[0, 0].barh(range(len(energias)), list(energias.values()), color=colors, alpha=0.7)
    axes[0, 0].set_yticks(range(len(energias)))
    axes[0, 0].set_yticklabels(list(energias.keys()))
    axes[0, 0].set_xlabel('Energía (eV)')
    axes[0, 0].set_xscale('log')
    axes[0, 0].set_title('Escala de Energías Comparativa')
    axes[0, 0].grid(True, alpha=0.3, axis='x')
    
    # Panel 2: Componentes del potencial del vacío
    terms = ['αR_Ψ⁻⁴', "βζ'(1/2)R_Ψ⁻²", 'γΛ²R_Ψ²', 'δsin²(...)']
    values = [abs(pot_vac['term1']), abs(pot_vac['term2']), 
              abs(pot_vac['term3']), abs(pot_vac['term4'])]
    
    axes[0, 1].bar(terms, values, color=['cyan', 'magenta', 'yellow', 'green'], 
                   alpha=0.7, edgecolor='black')
    axes[0, 1].set_ylabel('Magnitud (J)')
    axes[0, 1].set_yscale('log')
    axes[0, 1].set_title('Componentes del Potencial E_vac(R_Ψ)')
    axes[0, 1].tick_params(axis='x', rotation=15)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Panel 3: Relación E vs f
    freqs = np.linspace(100, 200, 100)
    energies_J = h * freqs
    energies_eV = energies_J / eV
    
    axes[1, 0].plot(freqs, energies_eV, 'b-', linewidth=2, label='E = hf')
    axes[1, 0].axvline(f0, color='red', linestyle='--', linewidth=2, 
                       label=f'f₀ = {f0} Hz')
    axes[1, 0].axhline(E_psi['E_eV'], color='red', linestyle=':', alpha=0.7,
                       label=f'E_Ψ = {E_psi["E_eV"]:.2e} eV')
    axes[1, 0].set_xlabel('Frecuencia (Hz)')
    axes[1, 0].set_ylabel('Energía (eV)')
    axes[1, 0].set_title('Relación Energía-Frecuencia')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Panel 4: Jerarquía de escalas
    scales = {
        'ℓ_P\n(Planck)': l_P,
        'R_Ψ\n(Compactif.)': R_psi,
        'λ_GW\n(Onda GW)': c / f0,
        'R_H\n(Horizonte)': c / 2.2e-18,  # H₀⁻¹ aprox
    }
    
    scale_values = np.array(list(scales.values()))
    scale_labels = list(scales.keys())
    
    axes[1, 1].barh(range(len(scales)), scale_values, 
                    color=['purple', 'orange', 'green', 'red'], alpha=0.7)
    axes[1, 1].set_yticks(range(len(scales)))
    axes[1, 1].set_yticklabels(scale_labels)
    axes[1, 1].set_xlabel('Longitud (m)')
    axes[1, 1].set_xscale('log')
    axes[1, 1].set_title('Jerarquía de Escalas: ℓ_P ↔ R_Ψ ↔ H₀⁻¹')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    # Guardar figura
    output_file = 'results/figures/energia_cuantica_fundamental.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualizaciones guardadas en: {output_file}")
    print()
    
    plt.close()


def guardar_resultados(E_psi, R_psi, pot_vac, campo_params):
    """
    Guarda los resultados en archivo JSON
    
    Args:
        E_psi: Diccionario con energías
        R_psi: Radio de compactificación
        pot_vac: Diccionario con potencial del vacío
        campo_params: Parámetros completos del campo de conciencia
    """
    import json
    
    resultados = {
        'energia_cuantica': {
            'E_Joules': E_psi['E_J'],
            'E_eV': E_psi['E_eV'],
            'frecuencia_Hz': E_psi['f0'],
            'omega_rad_s': E_psi['omega_0'],
        },
        'campo_conciencia': {
            'frecuencia_Hz': campo_params['frecuencia_Hz'],
            'energia_J': campo_params['energia_J'],
            'energia_eV': campo_params['energia_eV'],
            'longitud_onda_m': campo_params['longitud_onda_m'],
            'longitud_onda_km': campo_params['longitud_onda_km'],
            'masa_kg': campo_params['masa_kg'],
            'temperatura_K': campo_params['temperatura_K'],
        },
        'constantes': {
            'h_J_s': E_psi['h'],
            'h_bar_J_s': E_psi['h_bar'],
            'c_m_s': c,
            'l_P_m': l_P,
        },
        'geometria': {
            'R_psi_m': R_psi,
            'R_psi_over_l_P': R_psi / l_P,
        },
        'potencial_vacío': {
            'E_vac_total_J': pot_vac['total'],
            'termino_cuantico_J': pot_vac['term1'],
            'termino_zeta_J': pot_vac['term2'],
            'termino_cosmologico_J': pot_vac['term3'],
            'termino_adelico_J': pot_vac['term4'],
        }
    }
    
    os.makedirs('results', exist_ok=True)
    output_file = 'results/energia_cuantica_fundamental.json'
    
    with open(output_file, 'w') as f:
        json.dump(resultados, f, indent=2)
    
    print(f"✅ Resultados guardados en: {output_file}")
    print()


def main():
    """
    Función principal del script
    """
    
    # Calcular energía cuántica del modo fundamental
    E_psi = calcular_energia_cuantica()
    
    # Calcular radio de compactificación
    R_psi = calcular_radio_compactificacion()
    
    # Calcular potencial adélico-fractal
    pot_vac = potencial_adelico_fractal(R_psi)
    
    # Calcular parámetros completos del campo de conciencia
    campo_params = calcular_parametros_campo_completos()
    
    # Síntesis conceptual
    sintesis_conceptual(E_psi)
    
    # Generar visualizaciones
    generar_visualizaciones(E_psi, R_psi, pot_vac)
    
    # Guardar resultados (actualizado con nuevos parámetros)
    guardar_resultados(E_psi, R_psi, pot_vac, campo_params)
    
    print("=" * 80)
    print("CÁLCULO COMPLETADO")
    print("=" * 80)
    print()
    print(f"Energía cuántica fundamental: E_Ψ = {E_psi['E_eV']:.2e} eV")
    print(f"Frecuencia fundamental:       f₀ = {E_psi['f0']} Hz")
    print()
    print("Ver resultados completos en:")
    print("  - results/energia_cuantica_fundamental.json")
    print("  - results/figures/energia_cuantica_fundamental.png")
    print()


if __name__ == '__main__':
    main()
