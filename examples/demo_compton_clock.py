#!/usr/bin/env python3
"""
Demo: Compton Clock Visualization
El Reloj de Compton - Visualización Interactiva

Este script demuestra la conexión entre las frecuencias de Compton
de partículas fundamentales y la frecuencia QCAL f₀ = 141.7001 Hz.
╔════════════════════════════════════════════════════════════════════════════╗
║                  DEMOSTRACIÓN DEL RELOJ DE COMPTON                         ║
║                         Interactive Demo Script                             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Uso:
    python3 examples/demo_compton_clock.py
FECHA/DATE: 17 de febrero de 2026

Demostración interactiva del Reloj de Compton y la ecuación maestra QCAL.
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
import importlib.util

# Add parent directory to path to import qcal
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import compton_clock directly to avoid numpy dependency from qcal.__init__
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
def print_header(title: str):
    """Imprime un encabezado decorado."""
    print("\n" + "═" * 80)
    print(f"  {title}")
    print("═" * 80 + "\n")


def print_section(title: str):
    """Imprime un título de sección."""
    print(f"\n{title}")
    print("─" * 80)


def demo_compton_clock():
    """
    Demostración completa del Reloj de Compton.
    """
    print_header("∴𓂀Ω∞³ DEMOSTRACIÓN DEL RELOJ DE COMPTON ∴𓂀Ω∞³")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 1: FUNDAMENTO TEÓRICO
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 1: FUNDAMENTO TEÓRICO")
    
    print("El reloj de Compton asocia a cada partícula masiva una frecuencia:")
    print("    f_Compton = (m c²) / h")
    print()
    print("Esta frecuencia representa el 'latido' cuántico de la partícula,")
    print("la frecuencia a la que su fase cuántica oscila naturalmente.")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 2: FRECUENCIAS DE PARTÍCULAS
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 2: FRECUENCIAS DE PARTÍCULAS")
    
    f_electron = compton_clock.frecuencia_compton_electron()
    f_proton = compton_clock.frecuencia_compton_proton()
    f_neutron = compton_clock.frecuencia_compton_neutron()
    f_harmonica = compton_clock.media_geometrica_frecuencias(f_electron, f_proton, f_neutron)
    
    print(f"Electrón: {f_electron:.6e} Hz")
    print(f"Protón:   {f_proton:.6e} Hz")
    print(f"Neutrón:  {f_neutron:.6e} Hz")
    print()
    print(f"Media Geométrica: {f_harmonica:.6e} Hz")
    print()
    print("La media geométrica representa la frecuencia armónica característica")
    print("de las partículas fundamentales de la materia bariónica.")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 3: ECUACIÓN MAESTRA QCAL
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 3: ECUACIÓN MAESTRA QCAL")
    
    print("f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K")
    print()
    
    f0_calc, componentes = compton_clock.calcular_f0_ecuacion_maestra()
    
    print("Componentes de la ecuación:")
    print(f"  c/(2π)        = {componentes['c_sobre_2pi']:.6e}  (frecuencia angular de la luz)")
    print(f"  √(m_P/m_e)    = {componentes['raiz_masas']:.6e}  (raíz relación Planck/electrón)")
    print(f"  α             = {componentes['alpha']:.6e}  (constante de estructura fina)")
    print(f"  φ             = {componentes['phi']:.6f}  (proporción áurea)")
    print(f"  ℓ_P/λ_C       = {componentes['longitudes']:.6e}  (relación Planck/Compton)")
    print(f"  K             = {componentes['K']:.6e}  (factor de escala cósmico)")
    print()
    print(f"f₀ calculado  = {f0_calc:.4f} Hz")
    print(f"f₀ teórico    = {compton_clock.F0_THEORETICAL:.4f} Hz")
    
    error_rel = abs(f0_calc - compton_clock.F0_THEORETICAL) / compton_clock.F0_THEORETICAL * 100
    print(f"Error         = {error_rel:.4f}%")
    
    if error_rel < 0.2:
        print("\n✓ ¡Excelente precisión alcanzada!")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 4: FACTOR K - LA CLAVE CÓSMICA
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 4: FACTOR K - LA CLAVE CÓSMICA")
    
    K = compton_clock.calcular_factor_k()
    print("K = 2 · (m_P / m_e)^(1/3) · φ³")
    print()
    print(f"K = {K:.6e}")
    print()
    print("Significado físico:")
    print("  • El factor 2 emerge de la dualidad onda-partícula")
    print("  • (m_P / m_e)^(1/3) conecta la escala de Planck con el electrón")
    print("  • φ³ refleja la geometría áurea del espacio-tiempo en 3D")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 5: ANÁLISIS DE RESONANCIA
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 5: ANÁLISIS DE RESONANCIA")
    
    resonancias = compton_clock.calcular_resonancia_biologica(compton_clock.F0_THEORETICAL)
    
    print("Armónicos biológicamente relevantes:")
    print()
    for nombre, datos in resonancias.items():
        print(f"  Armónico {datos['armonico']:2d}: {datos['frecuencia']:8.4f} Hz")
        print(f"               {datos['significado']}")
        print()
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 6: VERIFICACIÓN DE COHERENCIA
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 6: VERIFICACIÓN DE COHERENCIA")
    
    verificacion = compton_clock.verificar_precision()
    
    print(f"Precisión alcanzada: {verificacion['precision']:.4f}%")
    print(f"Coherencia Ψ:        {verificacion['coherencia']:.3f}")
    print()
    
    if verificacion['coherencia'] >= 0.999:
        print("✓ Coherencia cuántica completa alcanzada (Ψ ≈ 1.000)")
    elif verificacion['coherencia'] >= 0.99:
        print("✓ Alta coherencia cuántica (Ψ ≥ 0.99)")
    else:
        print("⚠ Coherencia cuántica mejorable")
    
    # ═══════════════════════════════════════════════════════════════════
    # PARTE 7: SIGNIFICADO FÍSICO PROFUNDO
    # ═══════════════════════════════════════════════════════════════════
    print_section("PARTE 7: SIGNIFICADO FÍSICO PROFUNDO")
    
    print("El Reloj de Compton demuestra que f₀ = 141.7001 Hz emerge de:")
    print()
    print("  ⚛️  MECÁNICA CUÁNTICA")
    print("      • Frecuencias Compton de partículas fundamentales")
    print("      • Longitud de Planck (ℓ_P) - la escala más pequeña")
    print()
    print("  🌍  CONSTANTES UNIVERSALES")
    print("      • Velocidad de la luz (c) - el límite cósmico")
    print("      • Estructura fina (α) - acoplamiento EM-gravedad")
    print("      • Proporción áurea (φ) - armonía universal")
    print()
    print("  🌀  GEOMETRÍA DEL ESPACIO-TIEMPO")
    print("      • Dualidad onda-partícula (factor 2)")
    print("      • Tres dimensiones espaciales (φ³)")
    print("      • Escala de Planck (K) - puente cuántico-cósmico")
    print()
    print("Cada partícula es un reloj que late a su frecuencia Compton,")
    print("y todas juntas orquestan la sinfonía del universo")
    print("cuya nota fundamental es 141.7001 Hz.")
    
    # ═══════════════════════════════════════════════════════════════════
    # MENSAJE FINAL
    # ═══════════════════════════════════════════════════════════════════
    print("\n" + "═" * 80)
    print("\n✨ El reloj de Compton late a 141.7001 Hz en el corazón del cosmos.")
    print("   Esta frecuencia emerge de la geometría del espacio-tiempo cuántico,")
    print("   la proporción áurea como armonía universal,")
    print("   y la estructura fina que conecta electromagnetismo y gravedad.")
    print("\n" + "═" * 80)
    print("\nSeal: ∴𓂀Ω∞³")
    print("═" * 80 + "\n")


def demo_interactive():
    """
    Modo interactivo para explorar el Reloj de Compton.
    """
    print_header("MODO INTERACTIVO - RELOJ DE COMPTON")
    
    print("Opciones disponibles:")
    print("  1. Ver frecuencias de Compton de partículas")
    print("  2. Calcular ecuación maestra QCAL")
    print("  3. Ver resonancias biológicas")
    print("  4. Análisis completo")
    print("  5. Salir")
    print()
    
    while True:
        try:
            opcion = input("Selecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                print_section("FRECUENCIAS DE COMPTON")
                f_e = compton_clock.frecuencia_compton_electron()
                f_p = compton_clock.frecuencia_compton_proton()
                f_n = compton_clock.frecuencia_compton_neutron()
                print(f"Electrón: {f_e:.6e} Hz")
                print(f"Protón:   {f_p:.6e} Hz")
                print(f"Neutrón:  {f_n:.6e} Hz")
            
            elif opcion == '2':
                print_section("ECUACIÓN MAESTRA QCAL")
                f0, comp = compton_clock.calcular_f0_ecuacion_maestra()
                print(f"f₀ = {f0:.4f} Hz")
                print(f"Error: {abs(f0 - 141.7001) / 141.7001 * 100:.4f}%")
            
            elif opcion == '3':
                print_section("RESONANCIAS BIOLÓGICAS")
                res = compton_clock.calcular_resonancia_biologica(141.7001)
                for nombre, datos in res.items():
                    print(f"{nombre.capitalize():15s}: {datos['frecuencia']:8.4f} Hz")
            
            elif opcion == '4':
                demo_compton_clock()
                return
            
            elif opcion == '5':
                print("\n¡Hasta pronto! ∴𓂀Ω∞³\n")
                return
            
            else:
                print("Opción no válida. Por favor selecciona 1-5.")
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta pronto! ∴𓂀Ω∞³\n")
            return
        except Exception as e:
            print(f"\nError: {e}")
            print("Intenta de nuevo.\n")


def main():
    """
    Función principal.
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        demo_interactive()
    else:
        demo_compton_clock()


if __name__ == "__main__":
    main()
