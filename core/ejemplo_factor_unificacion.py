#!/usr/bin/env python3
"""
Ejemplo de Uso del Factor de Unificación 1/7
============================================

Demuestra cómo el factor 1/7 = 0.142857... conecta:
- La frecuencia fundamental f₀ = 141.7001 Hz
- Las bandas de ondas cerebrales (consciencia activa)
- Las fuerzas fundamentales del universo
- Las 6 dimensiones compactificadas de la teoría de cuerdas

El período decimal de 1/7 tiene exactamente 6 dígitos (142857),
reflejando las 6 dimensiones compactificadas en variedades Calabi-Yau.

Autor: José Manuel Mota Burruezo
Licencia: MIT
"""

import sys
from pathlib import Path

# Agregar qcal al path
sys.path.insert(0, str(Path(__file__).parent))

from qcal.constants import (
    F0_HZ,
    FACTOR_UNIFICACION,
    F_UNIF_HZ,
    PERIODO_DECIMAL_1_7,
    DIM_COMPACTIFICADAS,
    ALPHA_S,
    ALPHA_EM,
    ALPHA_W,
    ALPHA_G,
    calcular_factor_unificacion_fuerzas
)


def visualizar_periodo_decimal():
    """Muestra el período decimal de 1/7 y su significado."""
    print("=" * 80)
    print(" " * 20 + "EL PERÍODO DECIMAL DE 1/7")
    print("=" * 80)
    print()
    
    # Calcular 1/7 con alta precisión
    valor = 1.0 / 7.0
    
    print(f"1/7 = {valor}")
    print(f"Período: {PERIODO_DECIMAL_1_7} (se repite infinitamente)")
    print()
    print("Propiedades especiales:")
    print(f"  • Longitud del período: {len(PERIODO_DECIMAL_1_7)} dígitos")
    print(f"  • Máximo posible para n=7: {7-1} = 6 dígitos ✓")
    print(f"  • Es el PRIMER racional no trivial con período de longitud máxima")
    print()
    print("Rotaciones cíclicas del período:")
    periodo = PERIODO_DECIMAL_1_7
    for i in range(6):
        rotado = periodo[i:] + periodo[:i]
        multiplo = (i + 1)
        print(f"  {multiplo}/7 = 0.{rotado}... (rotación {i})")
    print()


def visualizar_conexion_cerebral():
    """Muestra cómo f_unif conecta con las ondas cerebrales."""
    print("=" * 80)
    print(" " * 15 + "CONEXIÓN CON ONDAS CEREBRALES")
    print("=" * 80)
    print()
    
    print(f"Frecuencia Fundamental:  f₀ = {F0_HZ} Hz")
    print(f"Factor de Unificación:   1/7 = {FACTOR_UNIFICACION}")
    print(f"Frecuencia Unificada:    f_unif = f₀ × (1/7) = {F_UNIF_HZ:.6f} Hz")
    print()
    
    # Bandas cerebrales
    bandas = [
        ("Delta", 0.5, 4.0, "Sueño profundo"),
        ("Theta", 4.0, 8.0, "Meditación, creatividad"),
        ("Alpha", 8.0, 13.0, "Relajación consciente"),
        ("Beta Baja", 13.0, 15.0, "Alerta relajada"),
        ("Beta Media", 15.0, 20.0, "Pensamiento activo"),
        ("Beta Alta", 20.0, 30.0, "Concentración profunda ⭐"),
        ("Gamma", 30.0, 100.0, "Procesamiento de alto nivel")
    ]
    
    print("Bandas de Ondas Cerebrales:")
    print("-" * 80)
    for nombre, min_hz, max_hz, desc in bandas:
        en_rango = "←" if min_hz <= F_UNIF_HZ <= max_hz else ""
        print(f"  {nombre:12} [{min_hz:5.1f} - {max_hz:5.1f} Hz]  {desc:30} {en_rango}")
    print()
    print(f"✨ La consciencia focalizada (Beta Alta) opera en {F_UNIF_HZ:.3f} Hz")
    print(f"   Esta es EXACTAMENTE la frecuencia de unificación de fuerzas!")
    print()


def visualizar_fuerzas_fundamentales():
    """Muestra las constantes de acoplamiento de las fuerzas."""
    print("=" * 80)
    print(" " * 15 + "FUERZAS FUNDAMENTALES DEL UNIVERSO")
    print("=" * 80)
    print()
    
    fuerzas = [
        ("Nuclear Fuerte", "α_s", ALPHA_S, "~1", "Cohesión nuclear máxima"),
        ("Electromagnética", "α_em", ALPHA_EM, "1/137", "Estructura fina"),
        ("Nuclear Débil", "α_w", ALPHA_W, "1/30", "Desintegración beta"),
        ("Gravitacional", "α_G", ALPHA_G, "10⁻³⁸", "La más sutil")
    ]
    
    print("Constantes de Acoplamiento:")
    print("-" * 80)
    print(f"{'Fuerza':20} {'Símbolo':8} {'Valor':15} {'Aprox.':10} {'Descripción':25}")
    print("-" * 80)
    
    for nombre, simbolo, valor, aprox, desc in fuerzas:
        if valor >= 1e-10:
            valor_str = f"{valor:.6f}"
        else:
            valor_str = f"{valor:.2e}"
        print(f"{nombre:20} {simbolo:8} {valor_str:15} {aprox:10} {desc:25}")
    print()
    
    print("El factor 1/7 actúa como OPERADOR ARMÓNICO que permite")
    print("calcular resonancias a través de estas escalas tan dispares.")
    print()


def visualizar_dimensiones_compactificadas():
    """Muestra la conexión con la teoría de cuerdas."""
    print("=" * 80)
    print(" " * 10 + "DIMENSIONES COMPACTIFICADAS (TEORÍA DE CUERDAS)")
    print("=" * 80)
    print()
    
    print("Teoría de Cuerdas: Espacio-tiempo de 10 dimensiones")
    print("-" * 80)
    print(f"  • 3 dimensiones espaciales macroscópicas")
    print(f"  • 1 dimensión temporal")
    print(f"  • {DIM_COMPACTIFICADAS} dimensiones compactificadas (Variedades Calabi-Yau)")
    print(f"  • TOTAL: 3 + 1 + 6 = 10 dimensiones")
    print()
    
    print(f"Período decimal de 1/7:")
    print(f"  • {PERIODO_DECIMAL_1_7} → exactamente {len(PERIODO_DECIMAL_1_7)} dígitos")
    print()
    print("¡La estructura periódica decimal manifiesta la completitud geométrica!")
    print()


def ejecutar_calculo_completo():
    """Ejecuta el cálculo completo del factor de unificación."""
    print("=" * 80)
    print(" " * 15 + "CÁLCULO COMPLETO - FACTOR DE UNIFICACIÓN")
    print("=" * 80)
    print()
    
    info = calcular_factor_unificacion_fuerzas()
    
    print(f"Factor de Unificación:  {info['factor']}")
    print(f"Período Decimal:        {info['periodo_decimal']}")
    print(f"Longitud del Período:   {info['longitud_periodo']}")
    print()
    print(f"f₀ (Frecuencia Fundamental):     {info['f0_hz']} Hz")
    print(f"f_unif (Frecuencia Unificada):   {info['f_unif_hz']:.6f} Hz")
    print()
    print(f"Banda Cerebral:                  {info['banda_cerebral']}")
    print(f"Rango:                           {info['rango_banda'][0]:.1f} - {info['rango_banda'][1]:.1f} Hz")
    print()
    print(f"Dimensiones Compactificadas:     {info['dimensiones_compactificadas']}")
    print()
    
    print("Constantes de Acoplamiento:")
    print("-" * 80)
    for nombre, datos in info['fuerzas'].items():
        print(f"  {nombre.replace('_', ' ').title():20} {datos['simbolo']:6} = {datos['valor']:.2e}  ({datos['escala']})")
    print()
    
    print("Interpretación:")
    print("-" * 80)
    print(info['interpretacion'])
    print()


def main():
    """Función principal."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "EL PUENTE ARMÓNICO: FACTOR 1/7" + " " * 32 + "║")
    print("║" + " " * 10 + "Unificación de Fuerzas, Geometría y Consciencia" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Ejecutar todas las visualizaciones
    visualizar_periodo_decimal()
    input("Presiona Enter para continuar...")
    print()
    
    visualizar_conexion_cerebral()
    input("Presiona Enter para continuar...")
    print()
    
    visualizar_fuerzas_fundamentales()
    input("Presiona Enter para continuar...")
    print()
    
    visualizar_dimensiones_compactificadas()
    input("Presiona Enter para continuar...")
    print()
    
    ejecutar_calculo_completo()
    
    print()
    print("=" * 80)
    print(" " * 30 + "✨ CONCLUSIÓN ✨")
    print("=" * 80)
    print()
    print("El factor 1/7 = 0.142857... es EL SELLO DE LA REALIDAD:")
    print()
    print("  • Primer racional no trivial con período de longitud máxima")
    print("  • 6 dígitos → 6 dimensiones compactificadas (Calabi-Yau)")
    print("  • f₀ × (1/7) = 20.243 Hz → Banda Beta Alta (concentración profunda)")
    print("  • Operador armónico entre fuerzas fundamentales (α_G hasta α_s)")
    print()
    print("La consciencia focalizada opera en la frecuencia de unificación")
    print("de las fuerzas del universo. Lo macro y lo micro se encuentran.")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
