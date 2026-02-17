#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  DEMOSTRACIÓN DEL RELOJ DE COMPTON                         ║
║                         Interactive Demo Script                             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA/DATE: 17 de febrero de 2026

Demostración interactiva del Reloj de Compton y la ecuación maestra QCAL.
"""

import sys
from pathlib import Path
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
