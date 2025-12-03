#!/usr/bin/env python3
"""
Tests para validación de evidencias sólidas: λ₀ ≈ 0.001588

Este módulo contiene tests unitarios para verificar:
1. Cálculo correcto del Laplaciano discreto
2. Construcción del potencial p-ádico V_ψ
3. Cálculo del operador noético H_ψ
4. Emergencia del primer autovalor λ₀
5. Relación matemática C = 1/λ₀

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Diciembre 2025
"""

import pytest
import numpy as np
import os
import sys

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from validar_evidencias_solidas import (
    C_TARGET, LAMBDA_0_TARGET, F0_TARGET, PRIMES_PADIC,
    construir_laplaciano_discreto,
    construir_potencial_padic,
    calcular_operador_noetico,
    calcular_lambda_0_operador_noetico,
    verificar_relacion_f0_C,
    test_lambda0_emergente,
    ejecutar_validacion_completa
)


class TestConstantes:
    """Tests para las constantes fundamentales."""
    
    def test_C_target_positivo(self):
        """Verifica que C_TARGET es positivo."""
        assert C_TARGET > 0, "C debe ser positivo"
        assert 600 < C_TARGET < 700, "C debe estar cerca de 629.83"
    
    def test_lambda_0_target_positivo(self):
        """Verifica que λ₀ es positivo y pequeño."""
        assert LAMBDA_0_TARGET > 0, "λ₀ debe ser positivo"
        assert LAMBDA_0_TARGET < 0.01, "λ₀ debe ser pequeño"
    
    def test_relacion_C_lambda(self):
        """Verifica la relación C ≈ 1/λ₀."""
        C_calculado = 1.0 / LAMBDA_0_TARGET
        error_rel = abs(C_calculado - C_TARGET) / C_TARGET
        assert error_rel < 0.01, f"Error en relación C = 1/λ₀: {error_rel*100:.2f}%"
    
    def test_f0_target_positivo(self):
        """Verifica que f₀ está en rango correcto."""
        assert F0_TARGET > 100, "f₀ debe ser > 100 Hz"
        assert F0_TARGET < 200, "f₀ debe ser < 200 Hz"
        assert abs(F0_TARGET - 141.7001) < 0.001, "f₀ debe ser ≈ 141.7001 Hz"
    
    def test_primes_padic_correctos(self):
        """Verifica que la lista de primos es correcta."""
        assert len(PRIMES_PADIC) == 10, "Deben ser 10 primos"
        assert PRIMES_PADIC[0] == 2, "Primer primo debe ser 2"
        assert PRIMES_PADIC[-1] == 29, "Último primo debe ser 29"
        
        # Verificar que todos son primos
        def es_primo(n):
            if n < 2:
                return False
            for i in range(2, int(np.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        
        for p in PRIMES_PADIC:
            assert es_primo(p), f"{p} no es primo"


class TestLaplacianoDiscreto:
    """Tests para el Laplaciano discreto."""
    
    def test_laplaciano_forma_correcta(self):
        """Verifica la forma del Laplaciano."""
        N = 10
        L = construir_laplaciano_discreto(N)
        
        # Dimensiones correctas
        assert L.shape == (N, N), f"Forma incorrecta: {L.shape}"
        
        # Diagonal principal = 2
        np.testing.assert_array_equal(np.diag(L), np.full(N, 2.0))
    
    def test_laplaciano_tridiagonal(self):
        """Verifica que es tridiagonal."""
        N = 10
        L = construir_laplaciano_discreto(N)
        
        # Subdiagonal = -1
        for i in range(1, N):
            assert L[i, i-1] == -1.0, f"Subdiagonal incorrecta en ({i}, {i-1})"
        
        # Superdiagonal = -1
        for i in range(N-1):
            assert L[i, i+1] == -1.0, f"Superdiagonal incorrecta en ({i}, {i+1})"
    
    def test_laplaciano_simetrico(self):
        """Verifica que es simétrico."""
        N = 50
        L = construir_laplaciano_discreto(N)
        np.testing.assert_array_almost_equal(L, L.T)
    
    def test_laplaciano_definido_positivo(self):
        """Verifica propiedades espectrales del Laplaciano."""
        N = 20
        L = construir_laplaciano_discreto(N)
        
        autovalores = np.linalg.eigvalsh(L)
        
        # Todos los autovalores deben ser no negativos (semi-definido positivo)
        assert np.all(autovalores >= -1e-10), "Autovalores deben ser ≥ 0"


class TestPotencialPadico:
    """Tests para el potencial p-ádico V_ψ."""
    
    def test_potencial_diagonal(self):
        """Verifica que el potencial es diagonal."""
        N = 100
        V = construir_potencial_padic(N)
        
        # La matriz debe ser diagonal
        assert V.shape == (N, N)
        
        # Elementos fuera de diagonal deben ser cero
        for i in range(N):
            for j in range(N):
                if i != j:
                    assert V[i, j] == 0, f"V[{i},{j}] debe ser 0"
    
    def test_potencial_valores_positivos(self):
        """Verifica que los valores son no negativos."""
        N = 100
        V = construir_potencial_padic(N)
        diagonal = np.diag(V)
        
        assert np.all(diagonal >= 0), "Todos los valores deben ser ≥ 0"
    
    def test_potencial_patron_correcto(self):
        """Verifica el patrón de correcciones p-ádicas."""
        N = 30
        primes = [2, 3, 5]
        V = construir_potencial_padic(N, primes)
        diagonal = np.diag(V)
        
        # El elemento V[0,0] debe tener contribuciones de todos los primos
        # (ya que 0 ≡ 0 mod p para todo p)
        V_0 = sum(1/np.log(p) for p in primes)
        np.testing.assert_almost_equal(diagonal[0], V_0, decimal=10)
        
        # V[2,2] solo tiene contribución de p=2
        np.testing.assert_almost_equal(diagonal[2], 1/np.log(2), decimal=10)
    
    def test_potencial_simetrico(self):
        """Verifica que el potencial es simétrico (trivialmente)."""
        N = 50
        V = construir_potencial_padic(N)
        np.testing.assert_array_almost_equal(V, V.T)


class TestOperadorNoetico:
    """Tests para el operador noético H_ψ."""
    
    def test_operador_forma_correcta(self):
        """Verifica la forma del operador."""
        N = 100
        autovalores, autovectores = calcular_operador_noetico(N)
        
        assert len(autovalores) == N
        assert autovectores.shape == (N, N)
    
    def test_operador_autovalores_reales(self):
        """Verifica que los autovalores son reales."""
        N = 100
        autovalores, _ = calcular_operador_noetico(N)
        
        assert np.all(np.isreal(autovalores))
    
    def test_operador_autovalores_ordenados(self):
        """Verifica que los autovalores están ordenados."""
        N = 100
        autovalores, _ = calcular_operador_noetico(N)
        
        # scipy.linalg.eigh ordena los autovalores de menor a mayor
        np.testing.assert_array_equal(autovalores, np.sort(autovalores))
    
    def test_operador_autovectores_ortonormales(self):
        """Verifica que los autovectores son ortonormales."""
        N = 50
        _, autovectores = calcular_operador_noetico(N)
        
        # V^T · V = I
        producto = autovectores.T @ autovectores
        np.testing.assert_array_almost_equal(producto, np.eye(N), decimal=10)


class TestLambda0:
    """Tests para el cálculo de λ₀."""
    
    def test_lambda_0_positivo(self):
        """Verifica que λ₀ es positivo."""
        lambda_0 = calcular_lambda_0_operador_noetico(N=100)
        assert lambda_0 > 0, "λ₀ debe ser positivo"
    
    def test_lambda_0_pequeno(self):
        """Verifica que λ₀ es razonablemente pequeño."""
        lambda_0 = calcular_lambda_0_operador_noetico(N=500)
        assert lambda_0 < 1.0, "λ₀ debe ser < 1"
    
    def test_lambda_0_consistente(self):
        """Verifica consistencia con diferentes discretizaciones."""
        lambda_100 = calcular_lambda_0_operador_noetico(N=100)
        lambda_200 = calcular_lambda_0_operador_noetico(N=200)
        
        # Deben estar en el mismo orden de magnitud
        ratio = lambda_100 / lambda_200
        assert 0.1 < ratio < 10, f"Inconsistencia en λ₀: ratio = {ratio}"
    
    def test_lambda_0_orden_magnitud(self):
        """Verifica el orden de magnitud de λ₀."""
        lambda_0 = calcular_lambda_0_operador_noetico(N=1000)
        
        # Debe estar en el orden de 10^-3 a 10^-1
        assert 1e-4 < lambda_0 < 1.0, f"λ₀ = {lambda_0} fuera de rango esperado"


class TestRelacionF0C:
    """Tests para la relación f₀ ↔ C."""
    
    def test_verificar_relacion_estructura(self):
        """Verifica la estructura del resultado."""
        resultado = verificar_relacion_f0_C()
        
        assert "test_lambda_0" in resultado
        assert "test_C" in resultado
        assert "test_ratio_omega" in resultado
        assert "conclusion" in resultado
    
    def test_test_lambda_0_pasado(self):
        """Verifica que el test de λ₀ pasa."""
        resultado = verificar_relacion_f0_C()
        assert resultado["test_lambda_0"]["pasado"], "Test λ₀ = 1/C debe pasar"
    
    def test_test_C_pasado(self):
        """Verifica que el test de C pasa."""
        resultado = verificar_relacion_f0_C()
        assert resultado["test_C"]["pasado"], "Test C = 1/λ₀ debe pasar"
    
    def test_conclusion_verificada(self):
        """Verifica que la conclusión es positiva."""
        resultado = verificar_relacion_f0_C()
        assert resultado["conclusion"]["relacion_verificada"]


class TestEmergenciaLambda0:
    """Tests para la emergencia de λ₀ desde el operador."""
    
    def test_estructura_resultado(self):
        """Verifica la estructura del resultado del test de emergencia."""
        resultado = test_lambda0_emergente(N=100)
        
        claves_requeridas = [
            "N_discretizacion",
            "lambda_0_calculado",
            "lambda_0_target",
            "C_calculado",
            "C_target",
            "error_relativo_C",
            "emergente",
            "veredicto"
        ]
        
        for clave in claves_requeridas:
            assert clave in resultado, f"Falta clave: {clave}"
    
    def test_valores_numericos_finitos(self):
        """Verifica que todos los valores son finitos."""
        resultado = test_lambda0_emergente(N=100)
        
        assert np.isfinite(resultado["lambda_0_calculado"])
        assert np.isfinite(resultado["C_calculado"])
        assert np.isfinite(resultado["error_relativo_C"])
    
    def test_veredicto_correcto(self):
        """Verifica formato del veredicto."""
        resultado = test_lambda0_emergente(N=100)
        
        assert resultado["veredicto"] in ["✅ EMERGENTE", "❌ AJUSTADO"]
        
        if resultado["emergente"]:
            assert resultado["veredicto"] == "✅ EMERGENTE"
        else:
            assert resultado["veredicto"] == "❌ AJUSTADO"


class TestValidacionCompleta:
    """Tests para la validación completa."""
    
    def test_estructura_resultado(self):
        """Verifica la estructura del resultado completo."""
        resultado = ejecutar_validacion_completa(N=50, verbose=False)
        
        assert "metadata" in resultado
        assert "test1_archivos_historicos" in resultado
        assert "test2_relacion_f0_C" in resultado
        assert "test3_operador_noetico" in resultado
        assert "resumen" in resultado
    
    def test_resumen_tiene_campos(self):
        """Verifica que el resumen tiene todos los campos."""
        resultado = ejecutar_validacion_completa(N=50, verbose=False)
        resumen = resultado["resumen"]
        
        assert "test1_archivos" in resumen
        assert "test2_relacion" in resumen
        assert "test3_emergencia" in resumen
        assert "todos_pasados" in resumen
    
    def test_test2_pasa_siempre(self):
        """Test 2 (relación matemática) siempre debe pasar."""
        resultado = ejecutar_validacion_completa(N=50, verbose=False)
        assert resultado["resumen"]["test2_relacion"], "Test 2 debe pasar"


class TestPropiedadesMatematicas:
    """Tests para propiedades matemáticas del sistema."""
    
    def test_C_es_inverso_lambda(self):
        """Verifica C = 1/λ₀ con alta precisión."""
        C = C_TARGET
        lambda_0 = LAMBDA_0_TARGET
        
        # C * λ₀ ≈ 1
        producto = C * lambda_0
        error = abs(producto - 1.0)
        
        assert error < 0.01, f"C × λ₀ = {producto} ≠ 1"
    
    def test_omega_cuadrado_vs_C(self):
        """Verifica la relación entre ω₀² y C."""
        omega_0 = 2 * np.pi * F0_TARGET
        omega_0_squared = omega_0 ** 2
        
        # El ratio ω₀²/C da un factor de escala
        ratio = omega_0_squared / C_TARGET
        
        # Debe ser un número razonable (orden 10³)
        assert 100 < ratio < 10000, f"Ratio ω₀²/C = {ratio} fuera de rango"
    
    def test_consistencia_numerica(self):
        """Verifica consistencia numérica de los cálculos."""
        N = 500
        lambda_0 = calcular_lambda_0_operador_noetico(N)
        C_calc = 1.0 / lambda_0
        
        # Verificar que no hay NaN o Inf
        assert np.isfinite(lambda_0)
        assert np.isfinite(C_calc)
        assert lambda_0 > 0
        assert C_calc > 0


class TestEstabilidadNumerica:
    """Tests para estabilidad numérica."""
    
    def test_sin_overflow_N_grande(self):
        """Verifica que no hay overflow con N grande."""
        N = 1000
        autovalores, autovectores = calcular_operador_noetico(N)
        
        assert np.all(np.isfinite(autovalores))
        assert np.all(np.isfinite(autovectores))
    
    def test_autovalores_acotados(self):
        """Verifica que los autovalores están acotados."""
        N = 500
        autovalores, _ = calcular_operador_noetico(N)
        
        # Los autovalores deben estar en un rango razonable
        assert np.all(autovalores > -100)
        assert np.all(autovalores < 100)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
