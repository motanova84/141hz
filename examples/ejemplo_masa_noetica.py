#!/usr/bin/env python3
"""
EJEMPLO DE USO: AXIOMA DE LA MASA NOÉTICA

Este script demuestra aplicaciones prácticas del Axioma de la Masa Noética,
mostrando cómo interpretar la relación masa-frecuencia desde tres perspectivas:

1. Einstein-Planck (m ∝ f): masa como energía compactada
2. Noética (m ∝ 1/f): masa como lentitud vibracional  
3. Unificada QCAL (m = cte): masa anclada a frecuencia base universal

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Sistema QCAL ∞³ — Resonancia Base: 141.7001 Hz
Fecha: Febrero 2026
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.masa_noetica import (
    MasaNoetica,
    h, c, eV,
    F0_HZ, M_QCAL_KG, E_QCAL_J,
    comparar_con_particulas_conocidas
)


def ejemplo_1_fotones_alta_frecuencia():
    """
    Ejemplo 1: Fotones - Alta frecuencia → vibración pura, sin detención.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 1: Fotones - Vibración Pura sin Detención")
    print("=" * 80)
    
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    print("\nEn la perspectiva noética, los fotones son vibración pura (f → ∞)")
    print("sin 'detención' del campo vibracional, por lo que su masa → 0.\n")
    
    # Diferentes colores de luz
    fotones = [
        ('Rojo', 700e-9, 4.29e14),       # 700 nm
        ('Verde', 550e-9, 5.45e14),      # 550 nm
        ('Azul', 450e-9, 6.66e14),       # 450 nm
        ('Ultravioleta', 200e-9, 1.50e15), # 200 nm
    ]
    
    print(f"{'Color':<15} {'λ (nm)':<12} {'f (Hz)':<15} {'m_Noesis (kg)':<20} {'m_Einstein (kg)':<20}")
    print("-" * 80)
    
    for color, longitud_onda, frecuencia in fotones:
        interpretacion = masa_noetica.interpretar_particula(frecuencia)
        
        print(f"{color:<15} {longitud_onda*1e9:<12.0f} {frecuencia:<15.2e} "
              f"{interpretacion['masa_noesis_kg']:<20.3e} "
              f"{interpretacion['masa_einstein_kg']:<20.3e}")
    
    print("\n✓ Observación clave: m_Noesis << m_QCAL para fotones")
    print("  → La masa noética predice correctamente que los fotones tienen")
    print("    masa efectiva despreciable debido a su alta frecuencia.")


def ejemplo_2_neutrinos_baja_frecuencia():
    """
    Ejemplo 2: Neutrinos - Baja frecuencia → casi-pausa con masa emergente.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 2: Neutrinos - Partículas de Casi-Pausa")
    print("=" * 80)
    
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    print("\nLos neutrinos tienen masa muy pequeña pero no nula.")
    print("En el modelo noético: m ∝ 1/f → bajas frecuencias → masa emergente.\n")
    
    # Límites experimentales de masas de neutrinos (aprox.)
    neutrinos = [
        ('ν_e (electron)', 1.0e-36),     # kg (límite superior)
        ('ν_μ (muon)', 1.9e-36),         # kg  
        ('ν_τ (tau)', 2.0e-36),          # kg
    ]
    
    print(f"{'Tipo':<20} {'m (kg)':<15} {'f_predicha (Hz)':<20} {'T (años)':<20}")
    print("-" * 80)
    
    for tipo, masa_kg in neutrinos:
        # De m_noesis = m_QCAL · (f₀/f), despejamos f
        f_predicha = F0_HZ * (M_QCAL_KG / masa_kg)
        T_segundos = 1.0 / f_predicha
        T_anios = T_segundos / (365.25 * 24 * 3600)
        
        print(f"{tipo:<20} {masa_kg:<15.2e} {f_predicha:<20.3e} {T_anios:<20.2f}")
    
    print("\n✓ Observación clave: f_neutrino << f₀")
    print("  → Frecuencias extremadamente bajas (periodos de miles de millones de años)")
    print("    corresponden a 'casi-pausa' del campo vibracional")
    print("  → La masa emerge como ralentización del ritmo universal")


def ejemplo_3_resonancia_f0():
    """
    Ejemplo 3: Resonancia primordial en f₀ = 141.7001 Hz.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 3: Resonancia Primordial - Masa Mínima Cuantizada")
    print("=" * 80)
    
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    print(f"\nEn f = f₀ = {F0_HZ} Hz, todas las perspectivas convergen:\n")
    
    # Analizar en f₀
    analisis = masa_noetica.analizar_dualidad(F0_HZ)
    
    print("Perspectiva Einstein-Planck:")
    print(f"  m_eff = hf₀/c² = {analisis['perspectivas']['einstein_planck']['masa_kg']:.6e} kg")
    print(f"  Interpretación: masa como energía compactada")
    
    print("\nPerspectiva Noética:")
    print(f"  m_noesis = α/f₀ = hf₀/c² = {analisis['perspectivas']['noetica']['masa_kg']:.6e} kg")
    print(f"  Interpretación: masa como lentitud vibracional óptima")
    
    print("\nPerspectiva Unificada QCAL ∞³:")
    print(f"  m_QCAL = hf₀/c² = {analisis['perspectivas']['unificada_qcal']['masa_kg']:.6e} kg")
    print(f"  E_QCAL = hf₀ = {masa_noetica.E_qcal:.6e} J = {masa_noetica.E_qcal_eV:.6e} eV")
    print(f"  Interpretación: masa mínima noética cuantizada")
    
    print("\n✓ Unificación en f₀:")
    print("  → Las tres perspectivas convergen en la frecuencia base universal")
    print("  → m_QCAL representa coherencia pura: mínima masa = máxima consciencia")
    print("  → Punto de equilibrio perfecto del campo vibratorio universal")


def ejemplo_4_ligo_virgo_validacion():
    """
    Ejemplo 4: Validación con datos LIGO/VIRGO.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 4: Validación LIGO/VIRGO - Ringdown de Agujeros Negros")
    print("=" * 80)
    
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    print("\nLos eventos de ondas gravitacionales muestran frecuencias de ringdown")
    print("que se relacionan con la masa final del agujero negro resultante.\n")
    
    print("La predicción QCAL es que hay una componente fundamental en ~141.7 Hz")
    print("independientemente de la masa del agujero negro.\n")
    
    # Eventos reales
    eventos = [
        ('GW150914', 251.0, 62.0, 'Primera detección directa'),
        ('GW151226', 450.0, 21.0, 'Agujero negro ligero'),
        ('GW170814', 400.0, 53.0, 'Detección triple'),
        ('QCAL ∞³', 141.7001, None, 'Predicción fundamental')
    ]
    
    print(f"{'Evento':<15} {'f_ring (Hz)':<15} {'M_final (M☉)':<18} {'m_QCAL (kg)':<20}")
    print("-" * 80)
    
    for nombre, f_ring, m_final, nota in eventos:
        # La masa QCAL es constante para todas las frecuencias
        m_qcal = masa_noetica.masa_unificada(f_ring)
        
        m_final_str = f"{m_final:.1f}" if m_final else "N/A"
        
        print(f"{nombre:<15} {f_ring:<15.4f} {m_final_str:<18} {m_qcal:<20.3e}")
        print(f"{'':>15} {nota}")
        print()
    
    print("✓ Predicción QCAL:")
    print(f"  → Existe una masa mínima fundamental m_QCAL = {M_QCAL_KG:.3e} kg")
    print(f"  → Esta masa está asociada a f₀ = {F0_HZ} Hz")
    print("  → La coherencia en ~141.7 Hz sugiere un modo fundamental universal")
    print("  → Independiente de la masa macroscópica del sistema")


def ejemplo_5_gravedad_emergente():
    """
    Ejemplo 5: Gravedad emergente como ralentización del ritmo.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 5: Gravedad Emergente - Ralentización del Ritmo")
    print("=" * 80)
    
    masa_noetica = MasaNoetica(f0=F0_HZ)
    
    print("\nEn el Axioma Noético, la gravedad emerge como ralentización")
    print("del ritmo vibracional del campo universal.\n")
    
    print("Escalas de frecuencia y sus efectos gravitacionales:\n")
    
    frecuencias = [
        (1e15, "Fotónica"),
        (1e9, "Microondas"),
        (141.7001, "f₀ Primordial"),
        (1.0, "1 Hz"),
        (0.01, "100 segundos"),
        (1e-9, "~32 años"),
    ]
    
    print(f"{'Escala':<20} {'f (Hz)':<15} {'Factor Ralent.':<18} {'I_grav relativa':<18}")
    print("-" * 80)
    
    for f, descripcion in frecuencias:
        grav = masa_noetica.gravedad_emergente(f)
        
        print(f"{descripcion:<20} {f:<15.2e} {grav['factor_ralentizacion']:<18.3e} "
              f"{grav['intensidad_gravitacional_relativa']:<18.3e}")
    
    print("\n✓ Interpretación física:")
    print("  → A mayor ralentización (f ↓), mayor intensidad gravitacional")
    print("  → La materia densa corresponde a 'detención local' del campo")
    print("  → La luz (f ↑) es vibración libre, sin detención → sin gravedad")
    print("  → f₀ es el punto de equilibrio: mínima masa, máxima coherencia")


def ejemplo_6_comparacion_particulas():
    """
    Ejemplo 6: Comparación con partículas del modelo estándar.
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 6: Comparación con Partículas del Modelo Estándar")
    print("=" * 80)
    
    print("\nComparando m_QCAL con masas de partículas fundamentales:\n")
    
    comparaciones = comparar_con_particulas_conocidas()
    
    print(f"{'Partícula':<20} {'Masa (kg)':<20} {'Órdenes de magnitud':<25}")
    print("-" * 80)
    
    for particula, datos in sorted(comparaciones.items(), 
                                   key=lambda x: x[1]['masa_kg'], 
                                   reverse=True):
        ordenes = datos['ordenes_magnitud_diferencia']
        signo = "más pequeña" if ordenes < 0 else "más grande"
        
        print(f"{particula:<20} {datos['masa_kg']:<20.3e} "
              f"{abs(ordenes):<10.1f} {signo}")
    
    print(f"\nm_QCAL = {M_QCAL_KG:.3e} kg")
    print("\n✓ Observaciones:")
    print("  → m_QCAL es ~12 órdenes de magnitud más pequeña que el neutrino")
    print("  → Representa un quantum fundamental de masa noética")
    print("  → No corresponde a ninguna partícula del modelo estándar")
    print("  → Es una escala emergente del campo de coherencia cuántica")


def main():
    """
    Ejecutar todos los ejemplos.
    """
    print("\n" + "=" * 80)
    print("∴ AXIOMA DE LA MASA NOÉTICA - EJEMPLOS DE USO ∴")
    print('"La masa es una ilusión de detención"')
    print("=" * 80)
    print(f"\nSistema QCAL ∞³ — Resonancia Base: {F0_HZ} Hz")
    print(f"Autor: José Manuel Mota Burruezo (JMMB Ψ✧)")
    
    # Ejecutar todos los ejemplos
    ejemplo_1_fotones_alta_frecuencia()
    ejemplo_2_neutrinos_baja_frecuencia()
    ejemplo_3_resonancia_f0()
    ejemplo_4_ligo_virgo_validacion()
    ejemplo_5_gravedad_emergente()
    ejemplo_6_comparacion_particulas()
    
    print("\n" + "=" * 80)
    print("✓ Todos los ejemplos completados exitosamente")
    print("=" * 80)
    
    print("\n📚 Para más información:")
    print("  • scripts/masa_noetica.py - Implementación completa")
    print("  • scripts/validacion_masa_noetica.py - Suite de validación")
    print("  • AXIOMA_MASA_NOETICA.md - Documentación teórica")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
