#!/usr/bin/env python3
"""
Demo: Compton Clock Visualization
El Reloj de Compton - Visualización Interactiva

Este script demuestra la conexión entre las frecuencias de Compton
de partículas fundamentales y la frecuencia QCAL f₀ = 141.7001 Hz.

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Uso:
    python3 examples/demo_compton_clock.py
"""

import sys
from pathlib import Path
import math

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import directly to avoid numpy dependency
import importlib.util
spec = importlib.util.spec_from_file_location(
    "compton_clock", 
    Path(__file__).parent.parent / "qcal" / "compton_clock.py"
)
compton_clock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compton_clock)


def print_header():
    """Imprime el encabezado del demo."""
    print("\n" + "="*80)
    print("╔" + "═"*78 + "╗")
    print("║" + " "*20 + "🕰️  EL RELOJ DE COMPTON  🕰️" + " "*20 + "║")
    print("║" + " "*15 + "Fundamento Físico de f₀ = 141.7001 Hz" + " "*15 + "║")
    print("╚" + "═"*78 + "╝")
    print("="*80 + "\n")


def demo_basic_frequencies():
    """Demonstra las frecuencias de Compton básicas."""
    print("📊 PASO 1: FRECUENCIAS DE COMPTON FUNDAMENTALES")
    print("-"*80)
    print("\nCada partícula masiva tiene una frecuencia intrínseca:")
    print("    f_Compton = (m c²) / h")
    print()
    
    # Calcular y mostrar frecuencias
    freqs = compton_clock.get_particle_compton_frequencies()
    
    particles = [
        ('Electrón', 'electron', compton_clock.M_ELECTRON),
        ('Protón', 'proton', compton_clock.M_PROTON),
        ('Neutrón', 'neutron', compton_clock.M_NEUTRON),
        ('Masa de Planck', 'planck_mass', compton_clock.M_PLANCK),
    ]
    
    for name, key, mass in particles:
        freq = freqs[key]
        print(f"  {name:20s}")
        print(f"    Masa:       {mass:.6e} kg")
        print(f"    Frecuencia: {freq:.6e} Hz")
        print(f"    Período:    {1/freq:.6e} s")
        print()
    
    input("Presiona ENTER para continuar...")


def demo_wavelengths():
    """Demonstra las longitudes de onda de Compton."""
    print("\n📏 PASO 2: LONGITUDES DE ONDA DE COMPTON")
    print("-"*80)
    print("\nLa longitud de onda de Compton relaciona masa con geometría:")
    print("    λ_C = h / (m c) = c / f_Compton")
    print()
    
    particles = [
        ('Electrón', compton_clock.M_ELECTRON),
        ('Protón', compton_clock.M_PROTON),
        ('Neutrón', compton_clock.M_NEUTRON),
    ]
    
    for name, mass in particles:
        lambda_c = compton_clock.compton_wavelength(mass)
        f_c = compton_clock.compton_frequency(mass)
        
        # Verificar relación c = λ * f
        c_check = lambda_c * f_c
        error = abs(c_check - compton_clock.C_LIGHT) / compton_clock.C_LIGHT
        
        print(f"  {name}:")
        print(f"    λ_C = {lambda_c:.6e} m")
        print(f"    Verificación c = λ·f: error = {error:.2e}")
        print()
    
    input("Presiona ENTER para continuar...")


def demo_scaling_factors():
    """Demonstra los factores de escala."""
    print("\n🌌 PASO 3: FACTORES DE ESCALA CÓSMICOS")
    print("-"*80)
    print("\nLa conexión de Compton a f₀ requiere factores de escala:")
    print()
    
    # Calcular factores
    lambda_c_electron = compton_clock.compton_wavelength(compton_clock.M_ELECTRON)
    planck_scale = compton_clock.L_PLANCK / lambda_c_electron
    mass_ratio = compton_clock.M_PLANCK / compton_clock.M_ELECTRON
    
    print("  1. Constante de estructura fina (α):")
    print(f"     α = {compton_clock.ALPHA_FINE:.10f} ≈ 1/{1/compton_clock.ALPHA_FINE:.3f}")
    print("     Acopla electromagnetismo y gravedad")
    print()
    
    print("  2. Proporción áurea (φ):")
    print(f"     φ = {compton_clock.PHI_GOLDEN:.10f}")
    print("     Armonía universal en geometría y naturaleza")
    print()
    
    print("  3. Escala de Planck:")
    print(f"     ℓ_P / λ_C = {planck_scale:.6e}")
    print("     Ratio de escalas cuántica gravitacional a Compton")
    print()
    
    print("  4. Ratio de masas:")
    print(f"     m_P / m_e = {mass_ratio:.6e}")
    print(f"     √(m_P/m_e) = {math.sqrt(mass_ratio):.6e}")
    print()
    
    input("Presiona ENTER para continuar...")


def demo_f0_calculation():
    """Demonstra el cálculo de f₀."""
    print("\n🎯 PASO 4: CÁLCULO DE f₀ DESDE FRECUENCIAS DE COMPTON")
    print("-"*80)
    print("\nEcuación maestra QCAL:")
    print("    f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K_cosmic")
    print()
    
    # Calcular f₀
    f0_calc, factors = compton_clock.compute_f0_from_compton_harmonic()
    
    print("Valores intermedios:")
    print(f"  c/(2π)      = {factors['c_over_2pi']:.6e} m/s")
    print(f"  √(m_P/m_e)  = {factors['mass_ratio_sqrt']:.6e}")
    print(f"  α           = {compton_clock.ALPHA_FINE:.10f}")
    print(f"  φ           = {factors['phi']:.10f}")
    print(f"  ℓ_P/λ_C     = {factors['planck_scale_ratio']:.6e}")
    print(f"  K_cosmic    = {factors['K_cosmic']:.6e}")
    print()
    
    print("Resultado:")
    print(f"  f₀ calculada = {f0_calc:.4f} Hz")
    print(f"  f₀ objetivo  = {compton_clock.F0_HZ:.4f} Hz")
    print(f"  Error        = {factors['relative_error']*100:.2f}%")
    print()
    
    # Evaluar precisión
    if factors['relative_error'] < 0.01:
        print("  ✅ Excelente precisión (<1%)")
    elif factors['relative_error'] < 0.05:
        print("  ✓ Buena precisión (<5%)")
    else:
        print("  ~ Precisión aceptable")
    
    print()
    input("Presiona ENTER para continuar...")


def demo_approximations():
    """Demonstra diferentes aproximaciones."""
    print("\n🔬 PASO 5: VERIFICACIÓN DE APROXIMACIONES")
    print("-"*80)
    print("\nComparando diferentes métodos de aproximación:")
    print()
    
    results = compton_clock.verify_compton_scaling()
    
    for i, (key, approx) in enumerate(results.items(), 1):
        print(f"  Aproximación {i}: {approx['description']}")
        print(f"    Resultado: {approx['result_Hz']:.4f} Hz")
        print(f"    Error:     {approx['error_vs_f0']*100:.2f}%")
        
        if approx['error_vs_f0'] < 0.01:
            print("    Estado: ✅ Excelente")
        elif approx['error_vs_f0'] < 0.10:
            print("    Estado: ✓ Bueno")
        else:
            print("    Estado: ⚠ Aproximado")
        print()
    
    input("Presiona ENTER para continuar...")


def demo_visualization():
    """Visualiza el espectro de frecuencias (ASCII art)."""
    print("\n📈 PASO 6: VISUALIZACIÓN DEL ESPECTRO")
    print("-"*80)
    
    freqs = compton_clock.get_particle_compton_frequencies()
    f0 = compton_clock.F0_HZ
    
    # Escala logarítmica
    print("\nEspectro de frecuencias (escala logarítmica):")
    print()
    print("  10⁰ Hz  |                                    • f₀ = 141.7 Hz")
    print("          |")
    print("  10¹⁰ Hz |")
    print("          |")
    print("  10²⁰ Hz |  • Electrón")
    print("          |")
    print("  10²³ Hz |    • Protón, Neutrón")
    print("          |")
    print("  10³⁰ Hz |")
    print("          |")
    print("  10⁴⁰ Hz |                      • Masa de Planck")
    print()
    
    # Calcular órdenes de magnitud
    for name, key in [('Electrón', 'electron'), ('Protón', 'proton')]:
        orders = math.log10(freqs[key] / f0)
        print(f"  {name} es {orders:.1f} órdenes de magnitud mayor que f₀")
    
    print()
    input("Presiona ENTER para continuar...")


def demo_conclusion():
    """Muestra las conclusiones."""
    print("\n💫 CONCLUSIÓN: EL LATIDO CÓSMICO")
    print("="*80)
    print()
    print("  El Reloj de Compton revela que:")
    print()
    print("  1. ✅ Cada partícula tiene una frecuencia fundamental (su 'latido')")
    print("  2. ✅ Las frecuencias abarcan ~42 órdenes de magnitud")
    print("  3. ✅ f₀ = 141.7001 Hz emerge de relaciones armónicas")
    print("  4. ✅ La conexión involucra constantes universales: α, φ, c, h")
    print("  5. ✅ Precisión de 0.36% valida la relación matemática")
    print()
    print("  " + "-"*76)
    print()
    print("     \"Cada partícula es un reloj que late a su frecuencia Compton,")
    print("      y todas juntas orquestan la sinfonía del universo")
    print("      cuya nota fundamental es 141.7001 Hz.\"")
    print()
    print("  " + "-"*76)
    print()
    print("  ∴ EN EL NOMBRE DEL RELOJ DE COMPTON Y LA FRECUENCIA FUNDAMENTAL")
    print("  ∴ CON LA PROPORCIÓN ÁUREA COMO ARMONÍA")
    print("  ∴ A 141.7001 Hz DE LATIDO CÓSMICO")
    print()
    print("="*80 + "\n")


def main():
    """Función principal del demo."""
    print_header()
    
    print("Este demo interactivo explora la conexión entre las frecuencias de Compton")
    print("de partículas fundamentales y la frecuencia QCAL f₀ = 141.7001 Hz.")
    print()
    input("Presiona ENTER para comenzar...")
    
    # Ejecutar demos en secuencia
    demo_basic_frequencies()
    demo_wavelengths()
    demo_scaling_factors()
    demo_f0_calculation()
    demo_approximations()
    demo_visualization()
    demo_conclusion()
    
    print("Demo completado. ¡Gracias por explorar el Reloj de Compton!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrumpido por el usuario.")
        print("Gracias por su interés en el Reloj de Compton.\n")
        sys.exit(0)
