#!/usr/bin/env python3
"""
Ejemplo de uso de PrimeHarmonicCalculator
Script interactivo para derivar 141.7001 Hz desde números primos
"""

from prime_harmonic_calculator import PrimeHarmonicCalculator
import matplotlib.pyplot as plt
import os


def mostrar_menu():
    """Mostrar el menú de opciones"""
    print("\n" + "="*60)
    print("OPCIONES:")
    print("="*60)
    print("1. Análisis rápido (100 primos)")
    print("2. Análisis estándar (10000 primos)")
    print("3. Análisis extendido (30000 primos)")
    print("4. Análisis de convergencia")
    print("5. Análisis personalizado")
    print("0. Salir")
    print("="*60)


def procesar_opcion(opcion, calc):
    """Procesar la opción seleccionada"""
    if opcion == "0":
        print("\n¡Hasta pronto!")
        return False

    elif opcion == "1":
        ejecutar_analisis_simple(calc, n_primes=100)

    elif opcion == "2":
        ejecutar_analisis_simple(calc, n_primes=10000)

    elif opcion == "3":
        ejecutar_analisis_simple(calc, n_primes=30000)

    elif opcion == "4":
        ejecutar_analisis_convergencia(calc)

    elif opcion == "5":
        try:
            n = int(input("Ingrese el número de primos a usar: "))
            if n > 0:
                ejecutar_analisis_simple(calc, n_primes=n)
            else:
                print("Error: El número debe ser positivo")
        except ValueError:
            print("Error: Ingrese un número válido")
    else:
        print("Opción no válida. Intente nuevamente.")

    return True


def main():
    """Función principal del ejemplo"""
    print("╔" + "═"*58 + "╗")
    print("║" + " "*10 + "PRIME HARMONIC CALCULATOR" + " "*23 + "║")
    print("║" + " "*8 + "Derivación de 141.7001 Hz" + " "*25 + "║")
    print("╚" + "═"*58 + "╝")
    print()

    # Crear calculadora
    print("Inicializando calculadora con precisión de 50 dígitos...")
    calc = PrimeHarmonicCalculator(precision_digits=50)
    print()

    # Menú de opciones
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()
        if not procesar_opcion(opcion, calc):
            break


def ejecutar_analisis_simple(calc, n_primes):
    """
    Ejecutar análisis simple con número específico de primos

    Args:
        calc: Instancia de PrimeHarmonicCalculator
        n_primes: Número de primos a utilizar
    """
    print(f"\n{'='*60}")
    print(f"EJECUTANDO ANÁLISIS CON {n_primes} PRIMOS")
    print(f"{'='*60}\n")

    results = calc.run_complete_analysis(n_primes=n_primes)

    # Mostrar resultados formateados
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*18 + "RESULTADOS FINALES" + " "*22 + "║")
    print("╠" + "═"*58 + "╣")
    print(f"║  Frecuencia calculada:  {results['final_frequency']:>10.4f} Hz" + " "*18 + "║")
    print(f"║  Frecuencia objetivo:   {results['target_frequency']:>10.4f} Hz" + " "*18 + "║")
    print(f"║  Error absoluto:        {results['error_absolute']:>10.4f} Hz" + " "*18 + "║")
    print(f"║  Error relativo:        {results['error_relative']:>10.2f} %" + " "*19 + "║")
    print("╠" + "═"*58 + "╣")
    if results['success']:
        print("║  Estado: ✅ VERIFICACIÓN EXITOSA" + " "*27 + "║")
    else:
        print("║  Estado: ⚠  VERIFICACIÓN PARCIAL" + " "*27 + "║")
    print("╚" + "═"*58 + "╝")

    # Preguntar si guardar resultados
    guardar = input("\n¿Guardar resultados en archivo? (s/n): ").strip().lower()
    if guardar == 's':
        filename = f"results_prime_harmonic_{n_primes}.txt"
        with open(filename, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PRIME HARMONIC CALCULATOR - RESULTADOS\n")
            f.write("="*60 + "\n\n")
            f.write(f"Número de primos utilizados: {n_primes}\n")
            f.write(f"Frecuencia calculada: {results['final_frequency']:.4f} Hz\n")
            f.write(f"Frecuencia objetivo: {results['target_frequency']:.4f} Hz\n")
            f.write(f"Error absoluto: {results['error_absolute']:.4f} Hz\n")
            f.write(f"Error relativo: {results['error_relative']:.4f}%\n")
            f.write(f"\nDetalles:\n")
            f.write(f"  Magnitud |∇Ξ(1)|: {results['magnitude']:.6f}\n")
            f.write(f"  A_eff²: {results['A_eff_squared']:.6f}\n")
            f.write(f"  Primer primo: {results['primes'][0]}\n")
            f.write(f"  Último primo: {results['primes'][-1]}\n")
        print(f"✅ Resultados guardados en '{filename}'")


def ejecutar_analisis_convergencia(calc):
    """
    Ejecutar análisis de convergencia

    Args:
        calc: Instancia de PrimeHarmonicCalculator
    """
    print("\n" + "="*60)
    print("ANÁLISIS DE CONVERGENCIA")
    print("="*60)

    # Parámetros por defecto
    max_primes_default = 30000
    step_default = 5000

    print("\nParámetros por defecto:")
    print(f"  Máximo de primos: {max_primes_default}")
    print(f"  Paso: {step_default}")

    usar_default = input("\n¿Usar parámetros por defecto? (s/n): ").strip().lower()

    if usar_default == 's':
        max_primes = max_primes_default
        step = step_default
    else:
        try:
            max_primes = int(input("Ingrese el número máximo de primos: "))
            step = int(input("Ingrese el tamaño del paso: "))
        except ValueError:
            print("Error: Valores inválidos. Usando valores por defecto.")
            max_primes = max_primes_default
            step = step_default

    print("\nEjecutando análisis de convergencia...")
    print(f"  Rango: {step} - {max_primes} primos")
    print(f"  Paso: {step}")
    print()

    df = calc.convergence_analysis(max_primes=max_primes, step=step)

    # Guardar resultados
    csv_file = 'convergence_results.csv'
    df.to_csv(csv_file, index=False)
    print(f"\n✅ Resultados guardados en '{csv_file}'")

    # Crear visualización
    crear_visualizacion = input("\n¿Crear gráfico de convergencia? (s/n): ").strip().lower()
    if crear_visualizacion == 's':
        try:
            # Crear directorio para figuras si no existe
            os.makedirs('results/figures', exist_ok=True)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            # Gráfico 1: Frecuencia vs. número de primos
            ax1.plot(df['n_primes'], df['frequency'], 'o-', linewidth=2,
                     markersize=8)
            ax1.axhline(y=141.7001, color='r', linestyle='--', linewidth=2,
                        label='Objetivo: 141.7001 Hz')
            ax1.set_xlabel('Número de primos', fontsize=12)
            ax1.set_ylabel('Frecuencia (Hz)', fontsize=12)
            ax1.set_title('Convergencia de frecuencia', fontsize=14, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Gráfico 2: Error relativo vs. número de primos
            ax2.plot(df['n_primes'], df['error_rel'], 'o-', color='orange',
                     linewidth=2, markersize=8)
            ax2.set_xlabel('Número de primos', fontsize=12)
            ax2.set_ylabel('Error relativo (%)', fontsize=12)
            ax2.set_title('Convergencia del error', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')

            plt.tight_layout()

            output_file = 'results/figures/convergence_analysis.png'
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"✅ Gráfico guardado en '{output_file}'")

        except Exception as e:
            print(f"Error al crear visualización: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
