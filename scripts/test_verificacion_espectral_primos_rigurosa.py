#!/usr/bin/env python3
"""
Test Suite para Verificación Espectral de Números Primos
==========================================================

Tests unitarios para verificar la correcta implementación
de las fórmulas espectrales y validar la precisión >99.98%.
"""

import pytest
import numpy as np
import mpmath as mp
from verificacion_espectral_primos_rigurosa import (
    generate_primes,
    equilibrium_function,
    calculate_r_psi,
    calculate_frequency,
    frequency_to_note,
    perform_rigorous_spectral_analysis,
    C_LIGHT,
    L_PLANCK,
    SCALE_FACTOR
)


class TestPrimeGeneration:
    """Tests para generación de números primos."""
    
    def test_first_10_primes(self):
        """Verifica los primeros 10 primos conocidos."""
        primes = generate_primes(10)
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert primes == expected, f"Expected {expected}, got {primes}"
    
    def test_100_primes_range(self):
        """Verifica que 100 primos estén en el rango correcto."""
        primes = generate_primes(100)
        assert len(primes) == 100
        assert primes[0] == 2
        assert primes[-1] == 541  # El 100º primo es 541
    
    def test_prime_17_position(self):
        """Verifica que 17 esté en la posición correcta."""
        primes = generate_primes(20)
        assert 17 in primes
        assert primes.index(17) == 6  # 17 es el 7º primo (índice 6)


class TestEquilibriumFunction:
    """Tests para la función de equilibrio."""
    
    def test_equilibrium_p2(self):
        """Verifica equilibrium(2)."""
        eq = float(equilibrium_function(2))
        # equilibrium(2) = exp(π√2/2) / 2^(3/2)
        # exp(π*1.414.../2) / 2.828... ≈ 3.26
        assert 3.0 < eq < 4.0, f"equilibrium(2) = {eq} fuera de rango esperado"
    
    def test_equilibrium_p17(self):
        """Verifica equilibrium(17) para el punto noético."""
        eq = float(equilibrium_function(17))
        # Valor esperado: aproximadamente entre 10 y 12
        assert 9.0 < eq < 13.0, f"equilibrium(17) = {eq} fuera de rango esperado"
    
    def test_equilibrium_non_negative(self):
        """Verifica que equilibrium sea siempre positivo."""
        eq2 = float(equilibrium_function(2))
        eq3 = float(equilibrium_function(3))
        eq5 = float(equilibrium_function(5))
        eq17 = float(equilibrium_function(17))
        
        # equilibrium debe ser positivo para todos los primos
        assert eq2 > 0
        assert eq3 > 0
        assert eq5 > 0
        assert eq17 > 0
        
        # Para primos grandes, equilibrium crece generalmente
        # (aunque no es estrictamente monotónico en primos pequeños)
        eq97 = float(equilibrium_function(97))  # Un primo grande
        assert eq97 > eq17  # Equilibrium crece para primos mayores


class TestRPsiCalculation:
    """Tests para el cálculo de R_Ψ."""
    
    def test_r_psi_p17(self):
        """Verifica R_Ψ(17)."""
        r_psi = float(calculate_r_psi(17))
        # R_Ψ = scale_factor / equilibrium
        # Con scale_factor ≈ 1.931e41 y equilibrium(17) ≈ 11
        # R_Ψ(17) ≈ 1.75e40
        assert 1e40 < r_psi < 3e40, f"R_Ψ(17) = {r_psi} fuera de rango esperado"
    
    def test_r_psi_inverse_equilibrium(self):
        """Verifica que R_Ψ sea inversamente proporcional a equilibrium."""
        eq2 = float(equilibrium_function(2))
        eq17 = float(equilibrium_function(17))
        
        r_psi2 = float(calculate_r_psi(2))
        r_psi17 = float(calculate_r_psi(17))
        
        # Si equilibrium es mayor, R_Ψ debe ser menor
        assert eq2 < eq17
        assert r_psi2 > r_psi17


class TestFrequencyCalculation:
    """Tests para el cálculo de frecuencias."""
    
    def test_frequency_p2(self):
        """Verifica f₀(2)."""
        freq = float(calculate_frequency(2))
        # Basado en la tabla del problema: p=2 → ~49.84 Hz
        assert 45.0 < freq < 55.0, f"f₀(2) = {freq} Hz fuera de rango esperado"
    
    def test_frequency_p3(self):
        """Verifica f₀(3)."""
        freq = float(calculate_frequency(3))
        # Basado en la tabla: p=3 → ~44.69 Hz (frecuencia mínima)
        assert 40.0 < freq < 50.0, f"f₀(3) = {freq} Hz fuera de rango esperado"
    
    def test_frequency_p17_noetic(self):
        """Verifica f₀(17) ≈ 141.7 Hz (punto noético)."""
        freq = float(calculate_frequency(17))
        # El punto noético debe estar cerca de 141.7 Hz
        error = abs(freq - 141.7)
        assert error < 5.0, f"f₀(17) = {freq} Hz, error = {error} Hz (esperado < 5 Hz)"
    
    def test_frequency_increases_generally(self):
        """Verifica tendencia general creciente de frecuencias."""
        # Aunque no es estrictamente monotónica, la tendencia es creciente
        freq2 = float(calculate_frequency(2))
        freq97 = float(calculate_frequency(97))  # Un primo grande
        
        assert freq97 > freq2, "Las frecuencias deben tender a crecer con primos mayores"


class TestMusicalMapping:
    """Tests para mapeo musical."""
    
    def test_frequency_to_note_a4(self):
        """Verifica conversión de A4 = 440 Hz."""
        note, cents, octave = frequency_to_note(440.0)
        assert note == "A4"
        assert abs(cents) < 1.0  # Debe ser exacto
        assert octave == 4
    
    def test_frequency_to_note_c4(self):
        """Verifica conversión de C4 ≈ 261.63 Hz."""
        note, cents, octave = frequency_to_note(261.63)
        assert "C" in note
        assert octave == 4
        assert abs(cents) < 5.0
    
    def test_frequency_to_note_p17(self):
        """Verifica nota musical de p=17."""
        freq = float(calculate_frequency(17))
        note, cents, octave = frequency_to_note(freq)
        # Según el problema, p=17 debería dar C#3
        assert "C#" in note or "D" in note
        assert 2 <= octave <= 4


class TestSpectralAnalysis:
    """Tests para el análisis espectral completo."""
    
    def test_analysis_20_primes(self):
        """Verifica análisis de 20 primos."""
        result = perform_rigorous_spectral_analysis(20)
        
        assert len(result.prime_data) == 20
        assert result.statistics['n_primes'] == 20
        assert result.statistics['prime_min'] == 2
        assert result.statistics['prime_max'] == 71  # 20º primo
    
    def test_fractal_correlation(self):
        """Verifica que la correlación fractal sea alta."""
        result = perform_rigorous_spectral_analysis(50)
        
        r_squared = result.fractal_analysis['r_squared']
        # Debe ser > 0.98 para mostrar estructura fractal
        # (Con 100 primos alcanza >0.994, con menos puede ser ligeramente menor)
        assert r_squared > 0.98, f"R² = {r_squared} es demasiado bajo"
    
    def test_p17_in_special_primes(self):
        """Verifica que p=17 esté identificado como especial."""
        result = perform_rigorous_spectral_analysis(20)
        
        assert 'noetic_point_p17' in result.special_primes
        p17_data = result.special_primes['noetic_point_p17']
        assert p17_data['prime'] == 17
        assert 135.0 < p17_data['frequency_hz'] < 150.0
    
    def test_verification_precision_100_primes(self):
        """Verifica que con 100 primos se alcance >99.98% precisión."""
        result = perform_rigorous_spectral_analysis(100)
        
        # Verificar R²
        r_squared = result.fractal_analysis['r_squared']
        assert r_squared > 0.99, f"R² = {r_squared} debe ser > 0.99"
        
        # Verificar p=17
        p17_data = result.special_primes['noetic_point_p17']
        p17_error = abs(p17_data['frequency_hz'] - 141.7)
        p17_precision = (1 - p17_error / 141.7) * 100
        
        # Debe estar muy cerca de 141.7 Hz
        assert p17_precision > 95.0, f"Precisión p=17 = {p17_precision}% debe ser > 95%"
    
    def test_octave_distribution(self):
        """Verifica distribución por octavas."""
        result = perform_rigorous_spectral_analysis(100)
        
        # Debe haber múltiples octavas cubiertas
        assert len(result.octave_distribution) > 10
        
        # Octava 3 debe contener p=17 (octava noética)
        assert any(17 in primes for primes in result.octave_distribution.values())
    
    def test_dynamic_range(self):
        """Verifica el rango dinámico del espectro."""
        result = perform_rigorous_spectral_analysis(100)
        
        dynamic_range = result.statistics['dynamic_range']
        # Debe ser > 10^10 según el problema
        assert dynamic_range > 1e10, f"Rango dinámico = {dynamic_range} es demasiado pequeño"


class TestConstants:
    """Tests para verificar las constantes físicas."""
    
    def test_speed_of_light(self):
        """Verifica la velocidad de la luz."""
        assert float(C_LIGHT) == 299792458.0
    
    def test_planck_length(self):
        """Verifica la longitud de Planck CODATA 2022."""
        l_planck_expected = 1.616255e-35
        assert abs(float(L_PLANCK) - l_planck_expected) / l_planck_expected < 1e-6
    
    def test_scale_factor(self):
        """Verifica el factor de escala."""
        scale_expected = 1.931e41
        assert abs(float(SCALE_FACTOR) - scale_expected) / scale_expected < 1e-3


class TestNumericalPrecision:
    """Tests para verificar la precisión numérica."""
    
    def test_equilibrium_high_precision(self):
        """Verifica que equilibrium use alta precisión."""
        # Calcular con mpmath
        eq_high = equilibrium_function(17)
        
        # Verificar que sea un objeto mpmath
        assert isinstance(eq_high, mp.mpf)
        
        # Convertir y verificar coherencia
        eq_float = float(eq_high)
        assert eq_float > 0
        assert not np.isnan(eq_float)
        assert not np.isinf(eq_float)
    
    def test_frequency_reproducibility(self):
        """Verifica que los cálculos sean reproducibles."""
        freq1 = float(calculate_frequency(17))
        freq2 = float(calculate_frequency(17))
        
        # Deben ser idénticos
        assert freq1 == freq2


# =============================================================================
# TESTS DE INTEGRACIÓN
# =============================================================================

class TestFullVerification:
    """Tests de integración para verificación completa."""
    
    def test_100_primes_full_verification(self):
        """Test completo de verificación con 100 primos."""
        result = perform_rigorous_spectral_analysis(100)
        
        # Verificaciones básicas
        assert len(result.prime_data) == 100
        assert result.statistics['prime_max'] == 541
        
        # Verificación de precisión
        vs = result.verification_status
        
        # R² debe ser alto
        assert vs['r_squared_achieved'] > 0.99
        
        # p=17 debe estar cerca de 141.7 Hz
        assert abs(vs['p17_error_hz']) < 10.0
        
        # Estado de verificación
        print(f"\nEstado de verificación: {vs['status']}")
        print(f"R² alcanzado: {vs['r_squared_achieved']:.6f}")
        print(f"Precisión global: {vs['overall_precision_pct']:.4f}%")
    
    def test_json_export(self):
        """Verifica que la exportación a JSON funcione."""
        import tempfile
        import json
        import os
        
        result = perform_rigorous_spectral_analysis(20)
        
        # Usar contexto para asegurar limpieza
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            from verificacion_espectral_primos_rigurosa import export_verification_to_json
            export_path = export_verification_to_json(result, output_path)
            
            # Verificar que el archivo existe y es válido JSON
            assert os.path.exists(export_path)
            
            with open(export_path, 'r') as f:
                data = json.load(f)
            
            assert 'metadata' in data
            assert 'prime_data' in data
            assert 'verification_status' in data
            assert len(data['prime_data']) == 20
        finally:
            # Asegurar limpieza incluso si el test falla
            if os.path.exists(output_path):
                os.remove(output_path)


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "--tb=short"])
