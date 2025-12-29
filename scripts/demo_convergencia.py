#!/usr/bin/env python3
"""
Demostración de Análisis de Convergencia

Este script demuestra cómo usar las funciones de verificación de convergencia
y constantes fundamentales según el Protocolo de Verificación Experimental
descrito en la Sección X del paper.

Uso:
    python3 demo_convergencia.py              # Demo rápida
    python3 demo_convergencia.py --full       # Análisis completo (más lento)
    python3 demo_convergencia.py --save       # Guardar gráficos
"""

import sys
import os
import argparse
import matplotlib
import matplotlib.pyplot as plt

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from verificacion_convergencia import (
    QuantumFrequencyCalculator,
    verify_fundamental_constants,
    plot_convergence_analysis
)


def demo_rapida():
    """
    Demostración rápida con análisis básico.
    """
    print("=" * 80)
    print("DEMOSTRACIÓN RÁPIDA - ANÁLISIS DE CONVERGENCIA")
    print("=" * 80)
    
    # Paso 1: Verificar constantes fundamentales
    print("\n1. Verificando constantes fundamentales (φ, γ)...")
    print("-" * 80)
    resultado = verify_fundamental_constants()
    
    if resultado['all_verified']:
        print("\n✅ Todas las constantes verificadas correctamente")
    else:
        print("\n❌ Algunas verificaciones fallaron")
    
    # Paso 2: Crear calculador
    print("\n2. Inicializando calculador de frecuencia cuántica...")
    print("-" * 80)
    calculator = QuantumFrequencyCalculator(precision=30)
    print(f"✓ Precisión: {calculator.precision} dígitos decimales")
    print(f"✓ φ = {float(calculator.phi):.15f}")
    print(f"✓ γ = {float(calculator.gamma):.15f}")
    print(f"✓ f₀ objetivo = {float(calculator.f0_target)} Hz")
    
    # Paso 3: Calcular frecuencias con diferentes N
    print("\n3. Calculando frecuencias con diferentes números de primos...")
    print("-" * 80)
    test_values = [100, 500, 1000, 5000]
    
    for n in test_values:
        freq = calculator.calculate_frequency_from_primes(n)
        error = abs(float(freq) - float(calculator.f0_target))
        error_rel = error / float(calculator.f0_target) * 100
        print(f"N={n:5d} primos: f = {float(freq):.6f} Hz, "
              f"error = {error:.6f} Hz ({error_rel:.4f}%)")
    
    # Paso 4: Análisis de convergencia (rápido)
    print("\n4. Realizando análisis de convergencia (rápido)...")
    print("-" * 80)
    print("Analizando convergencia con max_primes=2000, step=500...")
    
    df = calculator.convergence_analysis(max_primes=2000, step=500)
    
    print(f"\n✓ Análisis completado con {len(df)} puntos")
    print("\nPrimeros resultados:")
    print(df.head())
    
    print("\n5. Generando visualización...")
    print("-" * 80)
    matplotlib.use('Agg')  # Backend sin GUI
    plot_convergence_analysis(df)
    plt.savefig('/tmp/convergencia_rapida.png', dpi=150, bbox_inches='tight')
    print("✓ Gráfico guardado en: /tmp/convergencia_rapida.png")
    plt.close()
    
    print("\n" + "=" * 80)
    print("✅ DEMOSTRACIÓN RÁPIDA COMPLETADA")
    print("=" * 80)


def demo_completa():
    """
    Demostración completa con análisis extensivo.
    """
    print("=" * 80)
    print("DEMOSTRACIÓN COMPLETA - ANÁLISIS DE CONVERGENCIA")
    print("⚠️  ADVERTENCIA: Este análisis puede tomar varios minutos")
    print("=" * 80)
    
    # Paso 1: Verificar constantes
    print("\n1. Verificando constantes fundamentales con alta precisión...")
    print("-" * 80)
    verify_fundamental_constants()
    
    # Paso 2: Crear calculador con alta precisión
    print("\n2. Inicializando calculador con precisión de 50 dígitos...")
    print("-" * 80)
    calculator = QuantumFrequencyCalculator(precision=50)
    print("✓ Calculador inicializado")
    
    # Paso 3: Análisis de convergencia completo
    print("\n3. Realizando análisis de convergencia completo...")
    print("-" * 80)
    print("Analizando con max_primes=30000, step=5000...")
    print("Esto puede tomar 1-2 minutos...")
    
    df = calculator.convergence_analysis(max_primes=30000, step=5000)
    
    print(f"\n✓ Análisis completado con {len(df)} puntos")
    
    # Estadísticas
    print("\n4. Estadísticas de convergencia:")
    print("-" * 80)
    print(f"Error relativo mínimo: {df['error_rel'].min():.6f}%")
    print(f"Error relativo máximo: {df['error_rel'].max():.6f}%")
    print(f"Error relativo promedio: {df['error_rel'].mean():.6f}%")
    print(f"\nRatio |∇Ξ(1)|/√N promedio: {df['ratio'].mean():.6f}")
    print(f"Ratio |∇Ξ(1)|/√N std: {df['ratio'].std():.6f}")
    
    # Resultados finales
    print("\n5. Resultados con N=30000:")
    print("-" * 80)
    ultimo = df.iloc[-1]
    print(f"Frecuencia calculada: {ultimo['frequency']:.6f} Hz")
    print(f"Error relativo: {ultimo['error_rel']:.6f}%")
    print(f"|∇Ξ(1)| observado: {ultimo['magnitude']:.2f}")
    print(f"√N teórico: {ultimo['sqrt_n']:.2f}")
    print(f"Ratio: {ultimo['ratio']:.6f}")
    
    # Visualización
    print("\n6. Generando visualización completa...")
    print("-" * 80)
    matplotlib.use('Agg')
    plot_convergence_analysis(df)
    plt.savefig('/tmp/convergencia_completa.png', dpi=150, bbox_inches='tight')
    print("✓ Gráfico guardado en: /tmp/convergencia_completa.png")
    plt.close()
    
    print("\n" + "=" * 80)
    print("✅ DEMOSTRACIÓN COMPLETA FINALIZADA")
    print("=" * 80)


def main():
    """
    Función principal con argumentos de línea de comando.
    """
    parser = argparse.ArgumentParser(
        description="Demostración de análisis de convergencia para f₀ = 141.7001 Hz"
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Ejecutar análisis completo (max_primes=30000, más lento)'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Guardar gráficos en archivo'
    )
    
    args = parser.parse_args()
    
    if args.full:
        demo_completa()
    else:
        demo_rapida()
    
    print("\n💡 NOTA:")
    print("Para ejecutar el análisis completo (recomendado), use:")
    print("    python3 demo_convergencia.py --full")


if __name__ == "__main__":
    main()
