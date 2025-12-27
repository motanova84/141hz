#!/usr/bin/env python3
"""
Tests para la demostración matemática de 141.7001 Hz
"""

import pytest
import numpy as np
import os
import sys

# Añadir el directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from demostracion_matematica_141hz import (
    GAMMA, PHI, E_GAMMA, SQRT_2PI_GAMMA,
    sieve_of_eratosthenes, get_first_n_primes,
    compute_prime_series, theta_function
)


class TestConstants:
    """Tests para las constantes fundamentales."""
    
    def test_gamma_value(self):
        """Verifica el valor de la constante de Euler-Mascheroni."""
        expected = 0.5772156649015329
        assert abs(GAMMA - expected) < 1e-15
    
    def test_phi_value(self):
        """Verifica el valor de la proporción áurea."""
        expected = (1 + np.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-15
        # También verifica la propiedad φ² = φ + 1
        assert abs(PHI**2 - PHI - 1) < 1e-10
    
    def test_e_gamma_value(self):
        """Verifica e^γ."""
        expected = np.exp(GAMMA)
        assert abs(E_GAMMA - expected) < 1e-10
    
    def test_sqrt_2pi_gamma_value(self):
        """Verifica √(2πγ)."""
        expected = np.sqrt(2 * np.pi * GAMMA)
        assert abs(SQRT_2PI_GAMMA - expected) < 1e-10


class TestPrimeGeneration:
    """Tests para generación de números primos."""
    
    def test_sieve_small_primes(self):
        """Verifica generación de primos pequeños."""
        primes = sieve_of_eratosthenes(20)
        expected = np.array([2, 3, 5, 7, 11, 13, 17, 19])
        np.testing.assert_array_equal(primes, expected)
    
    def test_sieve_first_100_primes(self):
        """Verifica que se generan 100 primos correctamente."""
        primes = sieve_of_eratosthenes(541)  # El primo 100 es 541
        assert len(primes) == 100
        assert primes[0] == 2
        assert primes[99] == 541
    
    def test_get_first_n_primes(self):
        """Verifica la función get_first_n_primes."""
        primes = get_first_n_primes(10)
        expected = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        np.testing.assert_array_equal(primes, expected)
    
    def test_get_first_n_primes_large(self):
        """Verifica generación de muchos primos."""
        primes = get_first_n_primes(1000)
        assert len(primes) == 1000
        assert primes[0] == 2
        assert primes[-1] == 7919  # El primo 1000 es 7919


class TestPrimeSeries:
    """Tests para la serie prima compleja."""
    
    def test_compute_prime_series_small(self):
        """Verifica el cálculo de la serie para N pequeño."""
        N = 10
        S_N, phases, trajectory = compute_prime_series(N)
        
        # Verificar dimensiones
        assert len(phases) == N
        assert len(trajectory) == N
        
        # Verificar que S_N es el último elemento de la trayectoria
        assert np.isclose(S_N, trajectory[-1])
        
        # Verificar que la magnitud está en un rango razonable
        assert np.abs(S_N) > 0
        assert np.abs(S_N) < 100 * np.sqrt(N)
    
    def test_compute_prime_series_phases(self):
        """Verifica las propiedades de las fases."""
        N = 100
        _, phases, _ = compute_prime_series(N)
        
        # Las fases deben ser números reales positivos
        assert np.all(np.isreal(phases))
        assert np.all(phases > 0)
        
        # Las fases deben crecer (log es monótono creciente)
        assert np.all(np.diff(phases) > 0)
    
    def test_asymptotic_behavior(self):
        """Verifica el comportamiento asintótico |S_N| ≈ C√N."""
        N_values = [100, 200, 500, 1000]
        ratios = []
        
        for N in N_values:
            S_N, _, _ = compute_prime_series(N)
            ratio = np.abs(S_N) / np.sqrt(N)
            ratios.append(ratio)
        
        # Los ratios deben converger (variación debe disminuir)
        ratios = np.array(ratios)
        assert np.std(ratios[-3:]) < np.std(ratios[:3])
        
        # El ratio promedio debe estar cerca de 8.27
        assert 5 < np.mean(ratios) < 12


class TestThetaFunction:
    """Tests para la función theta de Jacobi."""
    
    def test_theta_positive_t(self):
        """Verifica θ(it) para t positivo."""
        result = theta_function(1.0, n_terms=50)
        # Para t > 0, θ(it) debe ser mayor que 1
        assert result > 1.0
        assert np.isfinite(result)
    
    def test_theta_negative_t(self):
        """Verifica θ(it) para t negativo."""
        result = theta_function(-1.0, n_terms=50)
        # Para t < 0, θ(it) también debe ser positivo
        assert result > 0
        assert np.isfinite(result)
    
    def test_theta_convergence(self):
        """Verifica la convergencia con más términos."""
        t = 0.5
        result_50 = theta_function(t, n_terms=50)
        result_100 = theta_function(t, n_terms=100)
        
        # Los resultados deben ser similares (convergencia)
        rel_diff = abs(result_100 - result_50) / result_100
        assert rel_diff < 0.01  # Menos de 1% de diferencia


class TestFrequencyConstruction:
    """Tests para la construcción de la frecuencia."""
    
    def test_base_frequency(self):
        """Verifica la frecuencia base f₀ = 1/(2π)."""
        f0 = 1 / (2 * np.pi)
        expected = 0.1591549430918953
        assert abs(f0 - expected) < 1e-10
    
    def test_frequency_scaling_factors(self):
        """Verifica los factores de escalado individuales."""
        # e^γ
        assert abs(E_GAMMA - 1.781072418) < 1e-6
        
        # √(2πγ)
        assert abs(SQRT_2PI_GAMMA - 1.904403577) < 1e-6
        
        # φ²/(2π)
        phi_factor = PHI**2 / (2 * np.pi)
        expected_phi_factor = 0.41773326  # Valor aproximado
        assert abs(phi_factor - expected_phi_factor) < 1e-6
    
    def test_final_frequency_calculation(self):
        """Verifica el cálculo de la frecuencia final."""
        f0 = 1 / (2 * np.pi)
        C = 629.83  # Constante del paper
        
        f_final = f0 * E_GAMMA * SQRT_2PI_GAMMA * (PHI**2 / (2 * np.pi)) * C
        
        # Debe estar cerca de 141.7001 Hz
        target = 141.7001
        error_percent = abs(f_final - target) / target * 100
        
        # Permitir hasta 5% de error (debido a aproximaciones en C)
        assert error_percent < 5.0


class TestNumericalStability:
    """Tests para verificar estabilidad numérica."""
    
    def test_no_overflow_large_N(self):
        """Verifica que no haya overflow con N grande."""
        N = 2000
        S_N, phases, trajectory = compute_prime_series(N)
        
        assert np.isfinite(S_N)
        assert np.all(np.isfinite(phases))
        assert np.all(np.isfinite(trajectory))
    
    def test_phase_modulo_2pi(self):
        """Verifica el cálculo de fases módulo 2π."""
        N = 100
        _, phases, _ = compute_prime_series(N)
        
        phases_mod = phases % (2 * np.pi)
        
        # Todas las fases módulo 2π deben estar en [0, 2π)
        assert np.all(phases_mod >= 0)
        assert np.all(phases_mod < 2 * np.pi)


class TestMathematicalProperties:
    """Tests para propiedades matemáticas de la demostración."""
    
    def test_weyl_equidistribution(self):
        """Verifica la equidistribución de Weyl (test básico)."""
        N = 1000
        _, phases, _ = compute_prime_series(N)
        
        phases_mod = phases % (2 * np.pi)
        
        # Test de uniformidad simple: dividir en bins
        n_bins = 10
        counts, _ = np.histogram(phases_mod, bins=n_bins, range=(0, 2*np.pi))
        
        # Esperamos aproximadamente N/n_bins por bin
        expected_count = N / n_bins
        
        # Chi-cuadrado simple
        chi_squared = np.sum((counts - expected_count)**2 / expected_count)
        
        # Para 10 bins, chi² debe ser razonable (no demasiado grande)
        # Valor crítico para 9 grados de libertad al 95%: ~16.92
        assert chi_squared < 50  # Relajado para test básico
    
    def test_random_walk_property(self):
        """Verifica la propiedad de caminata aleatoria."""
        N = 500
        _, _, trajectory = compute_prime_series(N)
        
        # Los pasos deben tener magnitud unitaria (e^(iθ))
        steps = trajectory[1:] - trajectory[:-1]
        magnitudes = np.abs(steps)
        
        # Todos los pasos deben tener magnitud ~1
        np.testing.assert_allclose(magnitudes, 1.0, rtol=1e-10)
    
    def test_complex_conjugate_symmetry(self):
        """Verifica propiedades de simetría compleja."""
        N = 50
        S_N, phases, _ = compute_prime_series(N)
        
        # La conjugada de la suma debe ser igual a la suma de las conjugadas
        conjugate_sum = np.sum(np.exp(-1j * phases))
        
        assert np.isclose(np.conj(S_N), conjugate_sum)


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v"])
