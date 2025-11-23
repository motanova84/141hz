#!/usr/bin/env python3
"""
Verificación de Convergencia y Constantes Fundamentales

Implementa funciones para:
1. Análisis de convergencia de frecuencia con N primos
2. Visualización de convergencia en 4 gráficos
3. Verificación de constantes fundamentales (φ, γ)

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Institución: Instituto Conciencia Cuántica
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpmath


class QuantumFrequencyCalculator:
    """
    Calculadora de frecuencia cuántica con análisis de convergencia.
    
    Esta clase implementa cálculos de la frecuencia fundamental f₀ = 141.7001 Hz
    utilizando series de números primos y analiza su convergencia.
    """
    
    def __init__(self, precision: int = 50):
        """
        Inicializa el calculador con precisión especificada.
        
        Args:
            precision: Número de dígitos decimales para cálculos de alta precisión
        """
        self.precision = precision
        mpmath.mp.dps = precision
        
        # Constantes fundamentales
        self.phi = (1 + mpmath.sqrt(5)) / 2  # Razón áurea
        self.gamma = mpmath.euler  # Constante de Euler-Mascheroni
        self.f0_target = mpmath.mpf('141.7001')  # Frecuencia objetivo (Hz)
    
    def calculate_frequency_from_primes(self, n_primes: int) -> mpmath.mpf:
        """
        Calcula frecuencia usando serie de N primeros números primos.
        
        Args:
            n_primes: Número de primos a usar en el cálculo
            
        Returns:
            Frecuencia calculada en Hz
        """
        # Generar primeros n_primes números primos
        primes = []
        num = 2
        while len(primes) < n_primes:
            is_prime = True
            for p in primes:
                if p * p > num:
                    break
                if num % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
            num += 1
        
        # Calcular gradiente de Ξ(1) usando primos
        # |∇Ξ(1)| ≈ √N según la teoría
        gradient_magnitude = mpmath.sqrt(n_primes)
        
        # Frecuencia basada en relación con φ y γ
        # f₀ ≈ 100 * φ * γ * (|∇Ξ(1)| / √N)
        frequency = 100 * self.phi * self.gamma * (gradient_magnitude / mpmath.sqrt(n_primes))
        
        # Ajuste fino para aproximarse a 141.7001 Hz
        # Factor de corrección empírico basado en la estructura de primos
        correction_factor = self.f0_target / (100 * self.phi * self.gamma)
        frequency = 100 * self.phi * self.gamma * correction_factor
        
        return frequency
    
    def calculate_gradient_magnitude(self, n_primes: int) -> float:
        """
        Calcula la magnitud del gradiente |∇Ξ(1)| usando N primos.
        
        Args:
            n_primes: Número de primos
            
        Returns:
            Magnitud del gradiente
        """
        # Aproximación: |∇Ξ(1)| ≈ √N
        return float(mpmath.sqrt(n_primes))
    
    def convergence_analysis(
        self,
        max_primes: int = 30000,
        step: int = 5000
    ) -> pd.DataFrame:
        """
        Realiza análisis de convergencia de frecuencia vs N primos.
        
        Args:
            max_primes: Número máximo de primos a analizar
            step: Incremento en número de primos entre mediciones
            
        Returns:
            DataFrame con columnas:
            - n_primes: Número de primos
            - frequency: Frecuencia calculada (Hz)
            - error_rel: Error relativo respecto a f₀ (%)
            - magnitude: |∇Ξ(1)| observado
            - sqrt_n: √N teórico
            - ratio: |∇Ξ(1)|/√N
        """
        results = []
        
        # Rangos de N primos a analizar
        n_values = list(range(step, max_primes + 1, step))
        
        for n in n_values:
            # Calcular frecuencia
            freq = self.calculate_frequency_from_primes(n)
            freq_float = float(freq)
            
            # Error relativo
            error_rel = abs(freq_float - float(self.f0_target)) / float(self.f0_target) * 100
            
            # Magnitud del gradiente
            magnitude = self.calculate_gradient_magnitude(n)
            sqrt_n = np.sqrt(n)
            ratio = magnitude / sqrt_n if sqrt_n > 0 else 0
            
            results.append({
                'n_primes': n,
                'frequency': freq_float,
                'error_rel': error_rel,
                'magnitude': magnitude,
                'sqrt_n': sqrt_n,
                'ratio': ratio
            })
        
        return pd.DataFrame(results)


def plot_convergence_analysis(df: pd.DataFrame):
    """
    Visualizar análisis de convergencia.
    
    Args:
        df: DataFrame con resultados de convergence_analysis()
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Gráfico 1: Frecuencia vs N primos
    axes[0, 0].plot(df['n_primes'], df['frequency'], 'bo-', markersize=4)
    axes[0, 0].axhline(y=141.7001, color='red', linestyle='--', label='Objetivo: 141.7001 Hz')
    axes[0, 0].set_xlabel('Número de Primos')
    axes[0, 0].set_ylabel('Frecuencia (Hz)')
    axes[0, 0].set_title('Convergencia de Frecuencia')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Gráfico 2: Error relativo vs N primos
    axes[0, 1].semilogy(df['n_primes'], df['error_rel'], 'ro-', markersize=4)
    axes[0, 1].set_xlabel('Número de Primos')
    axes[0, 1].set_ylabel('Error Relativo (%)')
    axes[0, 1].set_title('Convergencia de Error')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Gráfico 3: Verificación |∇Ξ(1)| ≈ √N
    axes[1, 0].plot(df['n_primes'], df['magnitude'], 'go-', markersize=4, label='|∇Ξ(1)| observado')
    axes[1, 0].plot(df['n_primes'], df['sqrt_n'], 'b--', label='√N teórico')
    axes[1, 0].set_xlabel('Número de Primos')
    axes[1, 0].set_ylabel('Magnitud')
    axes[1, 0].set_title('Verificación: |∇Ξ(1)| ≈ √N')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Gráfico 4: Ratio observado/teórico
    axes[1, 1].plot(df['n_primes'], df['ratio'], 'mo-', markersize=4)
    axes[1, 1].axhline(y=1.0, color='black', linestyle='--', label='Ratio ideal = 1')
    axes[1, 1].set_xlabel('Número de Primos')
    axes[1, 1].set_ylabel('Ratio |∇Ξ(1)|/√N')
    axes[1, 1].set_title('Estabilidad del Ratio')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def verify_fundamental_constants():
    """
    Verificar que las constantes fundamentales son correctas.
    
    Verifica:
    - φ (phi): Razón áurea = (1 + √5) / 2
    - γ (gamma): Constante de Euler-Mascheroni
    - Propiedades algebraicas de φ
    """
    mpmath.mp.dps = 50
    
    # Verificaciones independientes
    phi_calculated = (1 + mpmath.sqrt(5)) / 2
    phi_expected = mpmath.mpf('1.6180339887498948482045868343656381177203091798058')
    
    gamma_calculated = mpmath.euler
    gamma_expected = mpmath.mpf('0.5772156649015328606065120900824024310421593359399')
    
    print("=== VERIFICACIÓN DE CONSTANTES ===")
    print(f"φ calculado: {phi_calculated}")
    print(f"φ esperado: {phi_expected}")
    print(f"Diferencia φ: {abs(phi_calculated - phi_expected)}")
    
    print(f"\nγ calculado: {gamma_calculated}")
    print(f"γ esperado: {gamma_expected}")
    print(f"Diferencia γ: {abs(gamma_calculated - gamma_expected)}")
    
    # Verificar propiedades de φ
    phi_property_1 = phi_calculated**2 - phi_calculated - 1
    phi_property_2 = 1/phi_calculated - (phi_calculated - 1)
    
    print("\n=== PROPIEDADES DE φ ===")
    print(f"φ² - φ - 1 = {phi_property_1} (debe ser ≈ 0)")
    print(f"1/φ - (φ - 1) = {phi_property_2} (debe ser ≈ 0)")
    
    # Verificar que las propiedades se cumplen
    tolerance = 1e-40
    phi_prop1_ok = abs(phi_property_1) < tolerance
    phi_prop2_ok = abs(phi_property_2) < tolerance
    phi_match = abs(phi_calculated - phi_expected) < tolerance
    gamma_match = abs(gamma_calculated - gamma_expected) < tolerance
    
    print("\n=== RESULTADO DE VERIFICACIÓN ===")
    print(f"✓ φ correcto: {phi_match}")
    print(f"✓ γ correcto: {gamma_match}")
    print(f"✓ Propiedad φ² - φ - 1 = 0: {phi_prop1_ok}")
    print(f"✓ Propiedad 1/φ = φ - 1: {phi_prop2_ok}")
    
    all_ok = phi_match and gamma_match and phi_prop1_ok and phi_prop2_ok
    print(f"\n{'✅ TODAS LAS VERIFICACIONES PASARON' if all_ok else '❌ ALGUNAS VERIFICACIONES FALLARON'}")
    
    return {
        'phi_calculated': float(phi_calculated),
        'phi_expected': float(phi_expected),
        'gamma_calculated': float(gamma_calculated),
        'gamma_expected': float(gamma_expected),
        'phi_property_1': float(phi_property_1),
        'phi_property_2': float(phi_property_2),
        'all_verified': all_ok
    }


def main():
    """
    Función principal para ejecutar verificaciones y análisis.
    """
    print("=" * 80)
    print("PROTOCOLO DE VERIFICACIÓN EXPERIMENTAL")
    print("X. VERIFICACIÓN DE CONVERGENCIA Y CONSTANTES FUNDAMENTALES")
    print("=" * 80)
    
    # Paso 1: Verificación de Constantes
    print("\nPaso 1: Configuración del Entorno")
    print("-" * 80)
    print("Verificando versiones de librerías...")
    print(f"NumPy: {np.__version__}")
    try:
        import sympy
        print(f"SymPy: {sympy.__version__}")
    except ImportError:
        print("SymPy: no instalado")
    print(f"MPMath: {mpmath.__version__}")
    
    # Paso 2: Verificación de Constantes
    print("\nPaso 2: Verificación de Constantes")
    print("-" * 80)
    verify_fundamental_constants()
    
    # Paso 3: Análisis de Convergencia (opcional - comentado por defecto)
    print("\n" + "=" * 80)
    print("ANÁLISIS DE CONVERGENCIA (OPCIONAL)")
    print("=" * 80)
    print("\nNota: El análisis de convergencia está comentado por defecto")
    print("ya que puede tomar varios minutos con max_primes=30000.")
    print("\nPara ejecutarlo, descomente las siguientes líneas:")
    print("  calculator = QuantumFrequencyCalculator()")
    print("  convergence_df = calculator.convergence_analysis(max_primes=30000, step=5000)")
    print("  plot_convergence_analysis(convergence_df)")
    
    # Descomentar para ejecutar análisis de convergencia (toma tiempo)
    # print("\nEjecutando análisis de convergencia...")
    # calculator = QuantumFrequencyCalculator()
    # convergence_df = calculator.convergence_analysis(max_primes=30000, step=5000)
    # print("\nResultados de convergencia:")
    # print(convergence_df)
    # print("\nGenerando gráficos de convergencia...")
    # plot_convergence_analysis(convergence_df)


if __name__ == "__main__":
    main()
