# PrimeHarmonicCalculator - Ejemplo de Uso

## Descripción

`PrimeHarmonicCalculator` es una implementación de producción que deriva la frecuencia fundamental 141.7001 Hz desde la estructura matemática de números primos y la función zeta de Riemann.

## Instalación de Dependencias

```bash
pip install numpy scipy matplotlib sympy mpmath pandas
```

## Uso Básico

### Ejemplo 1: Análisis Simple

```python
from prime_harmonic_calculator import PrimeHarmonicCalculator

# Crear instancia con 50 dígitos de precisión
calculator = PrimeHarmonicCalculator(precision_digits=50)

# Ejecutar análisis con 10000 primos
results = calculator.run_complete_analysis(n_primes=10000)

# Mostrar resultados
print(f"Frecuencia calculada: {results['final_frequency']:.4f} Hz")
print(f"Frecuencia objetivo: {results['target_frequency']:.4f} Hz")
print(f"Error absoluto: {results['error_absolute']:.4f} Hz")
print(f"Error relativo: {results['error_relative']:.4f}%")
```

### Ejemplo 2: Análisis de Convergencia

```python
from prime_harmonic_calculator import PrimeHarmonicCalculator

# Crear calculadora
calculator = PrimeHarmonicCalculator(precision_digits=50)

# Análisis de convergencia con diferentes números de primos
convergence_df = calculator.convergence_analysis(
    max_primes=30000,  # Hasta 30000 primos
    step=5000          # En pasos de 5000
)

# Ver resultados
print(convergence_df)

# Guardar resultados
convergence_df.to_csv('convergence_results.csv', index=False)
```

### Ejemplo 3: Análisis Detallado Paso a Paso

```python
from prime_harmonic_calculator import PrimeHarmonicCalculator

# Crear calculadora
calc = PrimeHarmonicCalculator(precision_digits=50)

# Paso 1: Generar primos
n_primes = 5000
primes = calc.generate_primes(n_primes)
print(f"Generados {len(primes)} primos: {primes[0]} a {primes[-1]}")

# Paso 2: Calcular fases
phases = calc.calculate_prime_phases(primes)
print(f"Rango de fases: {min(phases):.3f} a {max(phases):.3f} rad")

# Paso 3: Suma harmónica
harmonic_sum, magnitude = calc.calculate_harmonic_sum(primes, phases)
print(f"Magnitud |∇Ξ(1)|: {magnitude:.6f}")
print(f"Ratio observado/teórico: {magnitude/np.sqrt(n_primes):.6f}")

# Paso 4: Factor de amplificación
A_eff_squared = calc.calculate_A_eff_squared()
print(f"A_eff²: {A_eff_squared:.6f}")

# Paso 5: Frecuencia final
frequency = calc.calculate_final_frequency(magnitude, A_eff_squared)
print(f"Frecuencia final: {frequency:.4f} Hz")
```

## Estructura de Resultados

El método `run_complete_analysis()` retorna un diccionario con las siguientes claves:

- `n_primes`: Número de primos utilizados
- `primes`: Lista de números primos
- `phases`: Lista de fases calculadas
- `harmonic_sum`: Suma harmónica compleja
- `magnitude`: Magnitud de la suma harmónica
- `A_eff_squared`: Factor de amplificación espectral
- `final_frequency`: Frecuencia calculada en Hz
- `target_frequency`: Frecuencia objetivo (141.7001 Hz)
- `error_absolute`: Error absoluto en Hz
- `error_relative`: Error relativo en porcentaje
- `success`: Boolean indicando si el error es < 0.1 Hz

## Fundamentos Teóricos

La calculadora implementa la siguiente derivación:

1. **Fases de Primos**: Para cada primo p_n, se calcula la fase θ_n = 2π·log(p_n)/φ, donde φ es la proporción áurea.

2. **Suma Harmónica**: Se calcula ∇Ξ(1) = Σ e^(iθ_n), cuya magnitud escala como √N según la teoría de matrices aleatorias (GUE).

3. **Factor de Amplificación**: Se deriva A_eff² de las derivadas de la función ξ(s) de Riemann en s=1.

4. **Frecuencia Final**: f₀ = (|∇Ξ(1)| · ω₀ · S · A_eff²) / (2π), donde:
   - ω₀ = 2π / ⟨δ⟩ es la frecuencia angular fundamental
   - S es el factor de escalado (e^γ · √(2πγ) · φ²/(2π))
   - ⟨δ⟩ = 2.246359 es el espaciamiento promedio de ceros (Montgomery-Odlyzko)

## Constantes Fundamentales

- **φ** (phi): Proporción áurea = (1 + √5)/2 ≈ 1.618034
- **γ** (gamma): Constante de Euler-Mascheroni ≈ 0.577216
- **π** (pi): Número pi
- **e**: Número de Euler
- **⟨δ⟩**: Espaciamiento promedio de ceros de Riemann ≈ 2.246359

## Precisión Numérica

La implementación usa `mpmath` para cálculos de alta precisión. El parámetro `precision_digits` controla el número de dígitos decimales:

- 30 dígitos: Suficiente para verificaciones rápidas
- 50 dígitos: Recomendado para cálculos de producción (default)
- 100+ dígitos: Para análisis de alta precisión

## Rendimiento

Tiempos aproximados (en una máquina típica):

- 100 primos: < 1 segundo
- 1,000 primos: < 1 segundo
- 10,000 primos: ~30-40 segundos
- 50,000 primos: ~3-5 minutos

El cuello de botella principal es la generación de números primos usando `sympy.prime()`.

## Ejemplo Completo de Script

```python
#!/usr/bin/env python3
"""
Script de ejemplo para ejecutar análisis completo
"""
from prime_harmonic_calculator import PrimeHarmonicCalculator
import matplotlib.pyplot as plt

def main():
    # Crear calculadora
    print("Inicializando calculadora...")
    calc = PrimeHarmonicCalculator(precision_digits=50)
    
    # Ejecutar análisis principal
    print("\nEjecutando análisis con 10000 primos...")
    results = calc.run_complete_analysis(n_primes=10000)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    print(f"Frecuencia calculada: {results['final_frequency']:.4f} Hz")
    print(f"Frecuencia objetivo:  {results['target_frequency']:.4f} Hz")
    print(f"Error absoluto:       {results['error_absolute']:.4f} Hz")
    print(f"Error relativo:       {results['error_relative']:.4f}%")
    print(f"Verificación:         {'✅ EXITOSA' if results['success'] else '⚠ PARCIAL'}")
    
    # Opcional: análisis de convergencia
    respuesta = input("\n¿Ejecutar análisis de convergencia? (s/n): ")
    if respuesta.lower() == 's':
        print("\nEjecutando análisis de convergencia...")
        df = calc.convergence_analysis(max_primes=20000, step=5000)
        
        # Guardar resultados
        df.to_csv('convergence_results.csv', index=False)
        print("\nResultados guardados en 'convergence_results.csv'")
        
        # Visualizar convergencia
        plt.figure(figsize=(10, 6))
        plt.plot(df['n_primes'], df['frequency'], 'o-', label='Frecuencia calculada')
        plt.axhline(y=141.7001, color='r', linestyle='--', label='Objetivo: 141.7001 Hz')
        plt.xlabel('Número de primos')
        plt.ylabel('Frecuencia (Hz)')
        plt.title('Convergencia de frecuencia vs. número de primos')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('convergence_plot.png', dpi=150, bbox_inches='tight')
        print("Gráfico guardado en 'convergence_plot.png'")

if __name__ == "__main__":
    main()
```

## Referencias

- Teoría de matrices aleatorias y GUE (Gaussian Unitary Ensemble)
- Función zeta de Riemann y distribución de ceros
- Conjetura de Montgomery-Odlyzko sobre espaciamiento de ceros
- Teoría Noésica Unificada (JMMB)

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)

Versión: 1.0 - Producción
Fecha: 21 agosto 2025
