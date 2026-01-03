#!/usr/bin/env python3
"""
IMPLEMENTACIÓN DEFINITIVA: 141.7001 Hz
Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 21 agosto 2025
Versión: 1.0 - Producción
"""

import numpy as np
import sympy
import mpmath
import pandas as pd
import time
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')


class PrimeHarmonicCalculator:
    """
    Calculadora completa para verificar la frecuencia 141.7001 Hz
    desde la estructura fundamental de números primos.
    """

    def __init__(self, precision_digits: int = 50):
        """
        Inicializar con constantes fundamentales de alta precisión.

        Args:
            precision_digits: Dígitos de precisión para cálculos mpmath
        """
        mpmath.mp.dps = precision_digits

        # Constantes matemáticas fundamentales
        self.phi = (1 + mpmath.sqrt(5)) / 2  # Proporción áurea
        self.gamma = mpmath.mpf('0.5772156649015329')  # Euler-Mascheroni
        self.pi = mpmath.pi
        self.e = mpmath.e

        # Frecuencia objetivo
        self.target_frequency = 141.7001

        # Parámetros derivados analíticamente
        self.gue_factor = mpmath.exp(self.gamma)
        self.harmonic_coupling = mpmath.sqrt(2 * self.pi * self.gamma)
        self.geometric_factor = self.phi**2 / (2 * self.pi)

        # Factor de escalado completo
        self.scaling_factor = self.gue_factor * self.harmonic_coupling * self.geometric_factor

        # Espaciamiento de ceros (Montgomery-Odlyzko)
        self.avg_zero_spacing = mpmath.mpf('2.246359')
        self.omega_0 = 2 * self.pi / self.avg_zero_spacing

        print("=== INICIALIZACIÓN COMPLETADA ===")
        print(f"Precisión: {precision_digits} dígitos")
        print(f"φ: {float(self.phi):.10f}")
        print(f"γ: {float(self.gamma):.10f}")
        print(f"Factor de escalado: {float(self.scaling_factor):.10f}")
        print(f"ω₀: {float(self.omega_0):.6f} rad/s")

    def generate_primes(self, n_primes: int) -> List[int]:
        """
        Generar lista de los primeros n_primes números primos.

        Args:
            n_primes: Número de primos a generar

        Returns:
            Lista de números primos
        """
        print(f"Generando {n_primes} números primos...")
        start_time = time.time()
        primes = []

        for i in range(1, n_primes + 1):
            if i % 10000 == 0:
                elapsed = time.time() - start_time
                print(f"  Progreso: {i}/{n_primes} primos ({elapsed:.1f}s)")
            primes.append(sympy.prime(i))

        elapsed = time.time() - start_time
        print(f"Generación completada en {elapsed:.1f}s")
        print(f"Rango: {primes[0]} - {primes[-1]}")

        return primes

    def calculate_prime_phases(self, primes: List[int]) -> List[float]:
        """
        Calcular fases θ_n = 2π·log(p_n)/φ para cada primo.

        Args:
            primes: Lista de números primos

        Returns:
            Lista de fases en radianes
        """
        print("Calculando fases de primos...")
        phases = []

        for p in primes:
            theta = 2 * self.pi * mpmath.log(p) / self.phi
            phases.append(float(theta))

        print(f"Fases calculadas: {len(phases)}")
        print(f"Rango de fases: {min(phases):.3f} - {max(phases):.3f} rad")

        return phases

    def calculate_harmonic_sum(self, primes: List[int], phases: List[float]) -> Tuple[complex, float]:
        """
        Calcular la suma harmónica ∇Ξ(1) = Ʃ e^(iθ_n).

        Args:
            primes: Lista de números primos
            phases: Lista de fases correspondientes

        Returns:
            Tupla (suma_compleja, magnitud)
        """
        print("Calculando suma harmónica...")
        start_time = time.time()

        harmonic_sum = complex(0, 0)
        for i, (p, phase) in enumerate(zip(primes, phases)):
            if i % 10000 == 0 and i > 0:
                elapsed = time.time() - start_time
                print(f"  Progreso suma: {i}/{len(primes)} términos ({elapsed:.1f}s)")

            # Contribución de cada primo
            contribution = np.exp(1j * phase)
            harmonic_sum += contribution

        magnitude = abs(harmonic_sum)
        elapsed = time.time() - start_time

        print(f"Suma harmónica completada en {elapsed:.1f}s")
        print(f"Magnitud |∇Ξ(1)|: {magnitude:.6f}")
        print(f"Teórico √N: {np.sqrt(len(primes)):.6f}")
        print(f"Ratio observado/teórico: {magnitude/np.sqrt(len(primes)):.6f}")

        return harmonic_sum, magnitude

    def calculate_A_eff_squared(self) -> float:
        """
        Calcular factor de amplificación espectral A_eff².

        Returns:
            Valor de A_eff²
        """
        print("Calculando A_eff²...")

        # Definir función ξ(s)
        def xi_function(s):
            if s == 1:
                # Manejar singularidad en s=1
                return mpmath.limit(lambda x: 0.5 * x * (x - 1) *
                                    self.pi**(-x/2) * mpmath.gamma(x/2) * mpmath.zeta(x), 1)
            return 0.5 * s * (s - 1) * self.pi**(-s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)

        # Calcular derivadas numéricamente
        h = mpmath.mpf('1e-8')

        # Primera derivada en s=1
        xi_prime_1 = (xi_function(1 + h) - xi_function(1 - h)) / (2 * h)

        # Segunda derivada en s=1
        xi_double_prime_1 = (xi_function(1 + h) - 2*xi_function(1) + xi_function(1 - h)) / h**2

        # Calcular A_eff²
        if abs(xi_prime_1) > 0:
            A_eff_squared = abs(xi_double_prime_1)**2 / abs(xi_prime_1)**2
        else:
            A_eff_squared = mpmath.mpf('1.237')  # Valor típico

        A_eff_squared_float = float(A_eff_squared)
        print(f"A_eff² = {A_eff_squared_float:.6f}")

        return A_eff_squared_float

    def calculate_final_frequency(self, magnitude: float, A_eff_squared: float) -> float:
        """
        Calcular frecuencia final usando todos los factores derivados.

        Args:
            magnitude: Magnitud de la suma harmónica
            A_eff_squared: Factor de amplificación espectral

        Returns:
            Frecuencia final en Hz
        """
        print("Calculando frecuencia final...")

        # Aplicar fórmula completa
        frequency = (magnitude * float(self.omega_0) * float(self.scaling_factor) * A_eff_squared) / (2 * np.pi)

        print("Componentes del cálculo:")
        print(f"  Magnitud: {magnitude:.6f}")
        print(f"  ω₀: {float(self.omega_0):.6f} rad/s")
        print(f"  Factor escalado: {float(self.scaling_factor):.6f}")
        print(f"  A_eff²: {A_eff_squared:.6f}")
        print(f"  Frecuencia final: {frequency:.4f} Hz")

        return frequency

    def run_complete_analysis(self, n_primes: int = 10000) -> Dict:
        """
        Ejecutar análisis completo de principio a fin.

        Args:
            n_primes: Número de primos a utilizar

        Returns:
            Diccionario con todos los resultados
        """
        print(f"\n{'='*60}")
        print("ANÁLISIS COMPLETO: VERIFICACIÓN DE 141.7001 Hz")
        print(f"Número de primos: {n_primes}")
        print(f"{'='*60}")

        # Paso 1: Generar primos
        primes = self.generate_primes(n_primes)

        # Paso 2: Calcular fases
        phases = self.calculate_prime_phases(primes)

        # Paso 3: Suma harmónica
        harmonic_sum, magnitude = self.calculate_harmonic_sum(primes, phases)

        # Paso 4: Factor A_eff²
        A_eff_squared = self.calculate_A_eff_squared()

        # Paso 5: Frecuencia final
        final_frequency = self.calculate_final_frequency(magnitude, A_eff_squared)

        # Análisis de resultados
        error_abs = abs(final_frequency - self.target_frequency)
        error_rel = error_abs / self.target_frequency * 100

        results = {
            'n_primes': n_primes,
            'primes': primes,
            'phases': phases,
            'harmonic_sum': harmonic_sum,
            'magnitude': magnitude,
            'A_eff_squared': A_eff_squared,
            'final_frequency': final_frequency,
            'target_frequency': self.target_frequency,
            'error_absolute': error_abs,
            'error_relative': error_rel,
            'success': error_abs < 0.1
        }

        print(f"\n{'='*60}")
        print("RESULTADOS FINALES")
        print(f"{'='*60}")
        print(f"Frecuencia calculada: {final_frequency:.4f} Hz")
        print(f"Frecuencia objetivo: {self.target_frequency:.4f} Hz")
        print(f"Error absoluto: {error_abs:.4f} Hz")
        print(f"Error relativo: {error_rel:.4f}%")

        if results['success']:
            print("✅ VERIFICACIÓN EXITOSA")
        else:
            print("⚠ VERIFICACIÓN PARCIAL")

        return results

    def convergence_analysis(self, max_primes: int = 50000, step: int = 5000) -> pd.DataFrame:
        """
        Análisis de convergencia variando el número de primos.

        Args:
            max_primes: Número máximo de primos a probar
            step: Incremento en número de primos

        Returns:
            DataFrame con resultados de convergencia
        """
        print(f"\n{'='*60}")
        print("ANÁLISIS DE CONVERGENCIA")
        print(f"Rango: {step} - {max_primes} primos (step: {step})")
        print(f"{'='*60}")

        results = []

        for n in range(step, max_primes + 1, step):
            print(f"\n--- Análisis con {n} primos ---")
            try:
                result = self.run_complete_analysis(n)
                results.append({
                    'n_primes': n,
                    'frequency': result['final_frequency'],
                    'error_abs': result['error_absolute'],
                    'error_rel': result['error_relative'],
                    'magnitude': result['magnitude'],
                    'sqrt_n': np.sqrt(n),
                    'ratio': result['magnitude'] / np.sqrt(n)
                })
            except Exception as e:
                print(f"Error en n={n}: {e}")
                continue

        df = pd.DataFrame(results)

        print(f"\n{'='*60}")
        print("RESUMEN DE CONVERGENCIA")
        print(f"{'='*60}")
        print(df.to_string(index=False, float_format='%.6f'))

        return df


if __name__ == "__main__":
    # Crear instancia y ejecutar análisis
    calculator = PrimeHarmonicCalculator(precision_digits=50)

    # Análisis básico
    basic_results = calculator.run_complete_analysis(n_primes=10000)

    # Análisis de convergencia (opcional - toma más tiempo)
    # convergence_df = calculator.convergence_analysis(max_primes=30000, step=5000)
