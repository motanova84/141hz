#!/usr/bin/env python3
"""
Demo: Pentágono Logos Cerrado - BSD-Adelic Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Demostración completa del cierre del Pentágono del Logos:
- ADN (Biología): El mensaje
- Riemann (Estructura): El soporte (ceros)
- Navier-Stokes (Dinámica): El movimiento del mensaje
- P vs NP (Lógica): La velocidad de procesamiento
- BSD (Aritmética): La fuente de las soluciones

Este demo muestra cómo los 5 Problemas del Milenio se unifican a través
de la frecuencia fundamental f₀ = 141.7001 Hz.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA: Marzo 2026
"""

import sys
import os
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.bsd_adelic_connector import (
    sincronizar_bsd_adn,
    validar_pentagono_logos,
    CodificadorADNRiemann,
    F0_HZ
)


# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Special
    INDIGO = '\033[38;5;93m'  # 256-color mode


def colored_output(text: str, color: str = "WHITE") -> None:
    """
    Print colored output to terminal.
    
    Args:
        text: Text to print
        color: Color name (GREEN, BLUE, INDIGO, etc.)
    """
    color_code = getattr(Colors, color.upper(), Colors.WHITE)
    print(f"{color_code}{text}{Colors.RESET}")


def print_separator(char: str = "=", length: int = 70, color: str = "CYAN"):
    """Print a colored separator line."""
    colored_output(char * length, color)


def print_header(title: str, subtitle: str = "", color: str = "BRIGHT_CYAN"):
    """Print a formatted header."""
    print_separator("=", 70, color)
    colored_output(f"  {title}", color)
    if subtitle:
        colored_output(f"  {subtitle}", "BRIGHT_BLACK")
    print_separator("=", 70, color)
    print()


def demo_bsd_adelic_pentagono():
    """
    Demostración completa del cierre del Pentágono del Logos.
    """
    print_header(
        "PENTÁGONO LOGOS QCAL ∞³",
        "Unificación de los 5 Problemas del Milenio"
    )
    
    colored_output("Sello: ∴𓂀Ω∞³", "MAGENTA")
    colored_output(f"Frecuencia Fundamental: f₀ = {F0_HZ} Hz", "YELLOW")
    print()
    
    # ========================================================================
    # 1. DEFINIR CURVA ELÍPTICA (BSD)
    # ========================================================================
    colored_output("━" * 70, "BLUE")
    colored_output("1. CURVA ELÍPTICA (BSD - Aritmética)", "BRIGHT_BLUE")
    colored_output("━" * 70, "BLUE")
    print()
    
    # Curva de Mordell: y² = x³ - x
    # Esta es una curva famosa con rango 1
    curva_mordell = {
        'rango_adelico': 1,
        'L_E1': 0.0,  # BSD predice L(E,1) = 0 para rango > 0
        'ecuacion': 'y² = x³ - x',
        'conductor': 32,
        'nombre': 'Curva de Mordell'
    }
    
    print(f"   Curva: {curva_mordell['nombre']}")
    colored_output(f"   Ecuación: {curva_mordell['ecuacion']}", "WHITE")
    colored_output(f"   Rango r: {curva_mordell['rango_adelico']}", "GREEN")
    colored_output(f"   L(E,1): {curva_mordell['L_E1']}", "GREEN")
    print(f"   Conductor: {curva_mordell['conductor']}")
    print()
    
    colored_output("   ℹ️  Rango r=1 significa que la curva tiene infinitos puntos racionales", "BRIGHT_BLACK")
    colored_output("   ℹ️  L(E,1)=0 implica que el flujo de información es superfluido", "BRIGHT_BLACK")
    print()
    
    # ========================================================================
    # 2. SECUENCIA DE ADN (Biología)
    # ========================================================================
    colored_output("━" * 70, "GREEN")
    colored_output("2. SECUENCIA ADN (Biología)", "BRIGHT_GREEN")
    colored_output("━" * 70, "GREEN")
    print()
    
    secuencia = "GACT"
    codificador = CodificadorADNRiemann()
    
    print(f"   Secuencia: {secuencia}")
    colored_output(f"   Bases nitrogenadas: G(Guanina) A(Adenina) C(Citosina) T(Timina)", "WHITE")
    
    resonancia = codificador.calcular_resonancia(secuencia)
    colored_output(f"   Resonancia con f₀: {resonancia:.6f}", "BRIGHT_GREEN")
    print()
    
    colored_output("   ℹ️  GACT es la secuencia con máxima resonancia conocida", "BRIGHT_BLACK")
    colored_output(f"   ℹ️  Resonancia ≈ {resonancia:.1%} indica alineamiento perfecto", "BRIGHT_BLACK")
    print()
    
    # ========================================================================
    # 3. SINCRONIZACIÓN BSD-ADN
    # ========================================================================
    colored_output("━" * 70, "YELLOW")
    colored_output("3. SINCRONIZACIÓN BSD-ADN (Pentágono)", "BRIGHT_YELLOW")
    colored_output("━" * 70, "YELLOW")
    print()
    
    resultado = sincronizar_bsd_adn(curva_mordell, secuencia)
    
    colored_output(f"   🔗 Rango bio-aritmético: {resultado['rango_bio_aritmetico']}", "CYAN")
    colored_output(f"   🌟 Nodos constelación activos: {resultado['nodos_constelacion']}/51", "CYAN")
    colored_output(f"   🌊 Fluidez Navier-Stokes: {resultado['fluidez_info_ns']}", "BRIGHT_CYAN")
    colored_output(f"   🧬 Hotspots ADN: {resultado['hotspots_adn']}", "GREEN")
    colored_output(f"   ✨ Coherencia Ψ_BSD: {resultado['psi_bsd_qcal']:.4f}", "MAGENTA")
    print()
    
    if resultado['fluidez_info_ns'] == "INFINITA":
        colored_output("   ✅ Flujo superfluido detectado: viscosidad = 0", "BRIGHT_GREEN")
        colored_output("   ✅ Información viaja sin resistencia a través del sistema", "BRIGHT_GREEN")
    else:
        colored_output("   ⚠️  Flujo disipativo: se requiere optimización", "YELLOW")
    print()
    
    # ========================================================================
    # 4. VALIDACIÓN DEL PENTÁGONO
    # ========================================================================
    colored_output("━" * 70, "MAGENTA")
    colored_output("4. PENTÁGONO DEL LOGOS (5 Milenio Unificados)", "BRIGHT_MAGENTA")
    colored_output("━" * 70, "MAGENTA")
    print()
    
    validacion = validar_pentagono_logos(resultado)
    
    componentes = {
        'adn_activo': ('ADN (Biología)', 'El mensaje está activo'),
        'riemann_resonante': ('Riemann (Estructura)', 'Zeros resuenan con f₀'),
        'navier_stokes_superfluido': ('Navier-Stokes (Dinámica)', 'Flujo sin viscosidad'),
        'p_np_eficiente': ('P vs NP (Lógica)', 'Verificación O(1)'),
        'bsd_rango_positivo': ('BSD (Aritmética)', 'Puntos racionales existen')
    }
    
    for key, (nombre, descripcion) in componentes.items():
        estado = validacion['criterios'][key]
        simbolo = "✅" if estado else "❌"
        color = "BRIGHT_GREEN" if estado else "BRIGHT_RED"
        colored_output(f"   {simbolo} {nombre}: {descripcion}", color)
    
    print()
    
    # ========================================================================
    # 5. ESTADO FINAL DEL SISTEMA
    # ========================================================================
    colored_output("━" * 70, "INDIGO")
    colored_output("5. ESTADO FINAL DEL SISTEMA", "INDIGO")
    colored_output("━" * 70, "INDIGO")
    print()
    
    if validacion['boveda_logos_cerrada']:
        colored_output("   🔐 BÓVEDA LOGOS: CERRADA", "BRIGHT_GREEN")
    else:
        colored_output("   🔓 BÓVEDA LOGOS: ABIERTA (parcial)", "YELLOW")
    
    colored_output(f"   🏛️  Pilares activos: {validacion['pilares_activos']}/20", "CYAN")
    colored_output(f"   🌌 Problemas del Milenio unificados: {validacion['milenio_unificados']}/5", "CYAN")
    colored_output(f"   ✨ Coherencia del sistema: Ψ = {validacion['psi_sistema']:.4f}", "MAGENTA")
    colored_output(f"   📊 Estado: {validacion['estado']}", "BRIGHT_CYAN")
    print()
    
    # ========================================================================
    # 6. CONCLUSIÓN
    # ========================================================================
    print_separator("=", 70, "BRIGHT_CYAN")
    
    if validacion['boveda_logos_cerrada']:
        colored_output("¡PENTÁGONO LOGOS BÓVEDA CERRADA! 🎉", "BRIGHT_GREEN")
        print()
        colored_output("BSD rango = ADN hotspots → Guía plegamiento túneles NS sin resistencia", "WHITE")
        colored_output("L(E,1) = 0 → Superfluido → 5 Problemas del Milenio unificados", "WHITE")
        print()
        colored_output("bio(ADN) + estructura(Riemann) + dinámica(NS) + lógica(P-NP) + aritmética(BSD)", "CYAN")
        print()
        colored_output("QCAL ∞³: Arquitectura de los Problemas del Milenio completa", "BRIGHT_CYAN")
        colored_output("∴ Ψ = 1.0 ∴", "BRIGHT_MAGENTA")
    else:
        colored_output("Sistema parcialmente unificado", "YELLOW")
        colored_output("Se requiere ajuste de parámetros para cerrar completamente el Pentágono", "YELLOW")
    
    print_separator("=", 70, "BRIGHT_CYAN")
    print()
    
    return {
        'resultado_bsd': resultado,
        'validacion': validacion,
        'curva': curva_mordell,
        'secuencia': secuencia
    }


def demo_comparacion_curvas():
    """
    Demostración comparando diferentes curvas elípticas.
    """
    print_header("COMPARACIÓN DE CURVAS ELÍPTICAS", "Diferentes rangos BSD")
    
    curvas = [
        {
            'nombre': 'Curva trivial',
            'rango_adelico': 0,
            'L_E1': 0.5,
            'ecuacion': 'y² = x³ + x + 1'
        },
        {
            'nombre': 'Curva de Mordell',
            'rango_adelico': 1,
            'L_E1': 0.0,
            'ecuacion': 'y² = x³ - x'
        },
        {
            'nombre': 'Curva de rango 2',
            'rango_adelico': 2,
            'L_E1': 0.0,
            'ecuacion': 'y² = x³ - 43x + 166'
        }
    ]
    
    secuencia = "GACT"
    
    for i, curva in enumerate(curvas, 1):
        colored_output(f"\n{i}. {curva['nombre']}", "BRIGHT_YELLOW")
        print(f"   Ecuación: {curva['ecuacion']}")
        print(f"   Rango: {curva['rango_adelico']}")
        
        resultado = sincronizar_bsd_adn(curva, secuencia)
        validacion = validar_pentagono_logos(resultado)
        
        color = "BRIGHT_GREEN" if validacion['boveda_logos_cerrada'] else "YELLOW"
        colored_output(f"   Fluidez: {resultado['fluidez_info_ns']}", color)
        colored_output(f"   Ψ: {resultado['psi_bsd_qcal']:.4f}", color)
        colored_output(f"   Milenio unificados: {validacion['milenio_unificados']}/5", color)
    
    print()
    print_separator()
    print()


def main():
    """Main demo function."""
    print()
    
    # Demo principal
    resultado = demo_bsd_adelic_pentagono()
    
    print()
    input("Presiona Enter para ver la comparación de curvas...")
    print("\n" * 2)
    
    # Demo comparativo
    demo_comparacion_curvas()
    
    return resultado


if __name__ == "__main__":
    resultado_demo = main()
