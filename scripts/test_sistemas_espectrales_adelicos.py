#!/usr/bin/env python3
"""
Tests para el módulo de Sistemas Espectrales Adélicos.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from sistemas_espectrales_adelicos import (
    SistemaAdelico,
    FuncionZetaEspectral,
    ConexionRiemannFrecuencia,
    UnificacionRiemannFrecuencia,
    f0_observed,
    CRITICAL_LINE
)


# ============================================================================
# TESTS: SISTEMA ADÉLICO
# ============================================================================

class TestSistemaAdelico:
    """Tests para la clase SistemaAdelico."""
    
    def test_inicializacion(self):
        """Test de inicialización básica."""
        sistema = SistemaAdelico(primes_limit=100)
        assert sistema.primes_limit == 100
        assert len(sistema.primes) > 0
        
    def test_generacion_primos(self):
        """Test de generación de números primos."""
        sistema = SistemaAdelico(primes_limit=100)
        primos = sistema.primes
        
        # Verificar que son primos
        assert 2 in primos
        assert 3 in primos
        assert 5 in primos
        assert 7 in primos
        
        # Verificar que no hay compuestos
        assert 4 not in primos
        assert 6 not in primos
        assert 9 not in primos
        
    def test_primos_ordenados(self):
        """Test que los primos están ordenados."""
        sistema = SistemaAdelico(primes_limit=100)
        primos = sistema.primes
        
        # Verificar ordenamiento
        assert np.all(primos[:-1] <= primos[1:])
        
    def test_producto_euler(self):
        """Test del producto de Euler."""
        sistema = SistemaAdelico(primes_limit=100)
        
        # Para s = 2, ζ(2) = π²/6 ≈ 1.6449
        resultado = sistema.producto_euler(2.0)
        esperado = np.pi**2 / 6
        
        # Tolerancia del 5% (producto parcial)
        assert abs(resultado - esperado) / esperado < 0.05
        
    def test_componente_adelico(self):
        """Test de la componente adélica del potencial."""
        sistema = SistemaAdelico()
        
        R_psi = 3.37e5  # metros (aproximado)
        resultado = sistema.componente_adelico(R_psi)
        
        assert "A_R" in resultado
        assert "A0" in resultado
        assert "R_psi" in resultado
        assert isinstance(resultado["A_R"], float)
        

# ============================================================================
# TESTS: FUNCIÓN ZETA ESPECTRAL
# ============================================================================

class TestFuncionZetaEspectral:
    """Tests para la clase FuncionZetaEspectral."""
    
    def test_inicializacion(self):
        """Test de inicialización."""
        zeta = FuncionZetaEspectral()
        assert zeta is not None
        
    def test_zeta_derivada_critica(self):
        """Test del valor de ζ'(1/2)."""
        zeta = FuncionZetaEspectral()
        valor = zeta.zeta_derivada_critica()
        
        # Valor conocido: ζ'(1/2) ≈ -3.923
        assert -4.0 < valor < -3.9
        assert abs(valor + 3.92264614) < 0.01
        
    def test_formula_von_mangoldt(self):
        """Test de la fórmula explícita de von Mangoldt."""
        zeta = FuncionZetaEspectral()
        
        # Evaluar en x = 100
        resultado = zeta.formula_explicita_von_mangoldt(100, num_zeros=5)
        
        # Ψ(100) debe ser un número real positivo
        assert isinstance(resultado, (int, float))
        assert resultado > 0
        
    def test_distribucion_ceros_energia(self):
        """Test de mapeo de ceros a energías."""
        zeta = FuncionZetaEspectral()
        
        energia_max = 1.0  # 1 eV
        energias = zeta.distribucion_ceros_energia(energia_max)
        
        # Verificar que hay energías
        assert len(energias) > 0
        
        # Todas las energías deben ser positivas
        assert all(e > 0 for e in energias)
        
        # La máxima debe estar cerca de energia_max
        assert max(energias) <= energia_max * 1.1


# ============================================================================
# TESTS: CONEXIÓN RIEMANN-FRECUENCIA
# ============================================================================

class TestConexionRiemannFrecuencia:
    """Tests para la clase ConexionRiemannFrecuencia."""
    
    def test_inicializacion(self):
        """Test de inicialización."""
        conexion = ConexionRiemannFrecuencia()
        assert conexion.sistema_adelico is not None
        assert conexion.zeta_espectral is not None
        
    def test_frecuencia_desde_zeta_prima(self):
        """Test de derivación de f₀ desde ζ'(1/2)."""
        conexion = ConexionRiemannFrecuencia()
        resultado = conexion.frecuencia_desde_zeta_prima()
        
        # Verificar campos requeridos
        assert "zeta_prime_half" in resultado
        assert "f0_derivada_Hz" in resultado
        assert "f0_observada_Hz" in resultado
        assert "precision_relativa" in resultado
        
        # Verificar tipos
        assert isinstance(resultado["f0_derivada_Hz"], (int, float))
        assert isinstance(resultado["precision_relativa"], (int, float))
        
        # Verificar valores razonables
        f0_derivada = resultado["f0_derivada_Hz"]
        assert 100 < f0_derivada < 200  # Rango físicamente razonable
        
    def test_distribucion_primos_frecuencia(self):
        """Test de análisis de distribución de primos."""
        conexion = ConexionRiemannFrecuencia()
        resultado = conexion.distribucion_primos_frecuencia(50)
        
        # Verificar campos
        assert "n_primos" in resultado
        assert "primo_maximo" in resultado
        assert "desviacion_media" in resultado
        assert "interpretacion" in resultado
        
        # Verificar valores
        assert resultado["n_primos"] == 50
        assert resultado["primo_maximo"] > 0
        
    def test_mecanismo_emergencia_vibracion(self):
        """Test del mecanismo completo de emergencia."""
        conexion = ConexionRiemannFrecuencia()
        resultado = conexion.mecanismo_emergencia_vibración()
        
        # Verificar los 5 niveles
        assert "nivel_1_aritmetica" in resultado
        assert "nivel_2_analitico" in resultado
        assert "nivel_3_adelico" in resultado
        assert "nivel_4_geometrico" in resultado
        assert "nivel_5_observable" in resultado
        
        # Verificar síntesis
        assert "sintesis" in resultado
        assert isinstance(resultado["sintesis"], str)
        assert len(resultado["sintesis"]) > 100  # Descripción sustancial


# ============================================================================
# TESTS: UNIFICACIÓN COMPLETA
# ============================================================================

class TestUnificacionRiemannFrecuencia:
    """Tests para la clase UnificacionRiemannFrecuencia."""
    
    def test_inicializacion(self):
        """Test de inicialización."""
        unificacion = UnificacionRiemannFrecuencia()
        assert unificacion.conexion is not None
        assert unificacion.timestamp is not None
        
    def test_analisis_completo(self):
        """Test del análisis completo."""
        unificacion = UnificacionRiemannFrecuencia()
        resultado = unificacion.analisis_completo()
        
        # Verificar estructura completa
        assert "metadata" in resultado
        assert "tesis_central" in resultado
        assert "derivacion_f0" in resultado
        assert "distribucion_primos" in resultado
        assert "mecanismo_emergencia" in resultado
        assert "validacion" in resultado
        
        # Verificar metadata
        assert "autor" in resultado["metadata"]
        assert "fecha" in resultado["metadata"]
        
    def test_validar_consistencia(self):
        """Test de validación de consistencia."""
        unificacion = UnificacionRiemannFrecuencia()
        validacion = unificacion._validar_consistencia()
        
        # Verificar campos de validación
        assert "f0_teorica_Hz" in validacion
        assert "f0_observada_Hz" in validacion
        assert "error_relativo" in validacion
        assert "validacion_exitosa" in validacion
        
        # Verificar tipos
        assert isinstance(validacion["error_relativo"], float)
        assert isinstance(validacion["validacion_exitosa"], bool)
        
        # La validación debería tener un error razonable
        assert validacion["error_relativo"] >= 0
        
    def test_exportar_json(self, tmp_path):
        """Test de exportación a JSON."""
        unificacion = UnificacionRiemannFrecuencia()
        
        # Exportar a directorio temporal
        output_path = tmp_path / "test_unificacion.json"
        resultado = unificacion.exportar_json(str(output_path))
        
        # Verificar que el archivo existe
        assert output_path.exists()
        
        # Verificar que el resultado tiene estructura esperada
        assert "metadata" in resultado
        assert "derivacion_f0" in resultado


# ============================================================================
# TESTS: CONSISTENCIA MATEMÁTICA
# ============================================================================

class TestConsistenciaMatematica:
    """Tests de consistencia matemática global."""
    
    def test_f0_en_rango_esperado(self):
        """Test que f₀ derivada está en el rango esperado."""
        conexion = ConexionRiemannFrecuencia()
        resultado = conexion.frecuencia_desde_zeta_prima()
        
        f0_derivada = resultado["f0_derivada_Hz"]
        
        # f₀ debe estar en el rango [100, 200] Hz (rango amplio)
        assert 100 <= f0_derivada <= 200
        
    def test_precision_derivacion_aceptable(self):
        """Test que la precisión de la derivación es aceptable."""
        conexion = ConexionRiemannFrecuencia()
        resultado = conexion.frecuencia_desde_zeta_prima()
        
        precision = resultado["precision_relativa"]
        
        # Error relativo debe ser < 30% (tolerancia para derivación teórica)
        assert precision < 0.30
        
    def test_zeta_prima_valor_correcto(self):
        """Test que ζ'(1/2) tiene el valor correcto."""
        zeta = FuncionZetaEspectral()
        valor = zeta.zeta_derivada_critica()
        
        # Valor de referencia: -3.92264614
        assert abs(valor + 3.92264614) < 0.001
        
    def test_linea_critica_correcta(self):
        """Test que la línea crítica es 1/2."""
        assert CRITICAL_LINE == 0.5
        
    def test_f0_observada_correcta(self):
        """Test que f₀ observada es el valor esperado."""
        assert abs(f0_observed - 141.7001) < 1e-4


# ============================================================================
# TESTS: INTEGRACIÓN CON TORRE ALGEBRAICA
# ============================================================================

class TestIntegracionTorreAlgebraica:
    """Tests de integración con la Torre Algebraica existente."""
    
    def test_importar_torre_algebraica(self):
        """Test que se puede importar torre_algebraica."""
        try:
            from torre_algebraica import TorreAlgebraica, f0
            assert f0 == f0_observed
        except ImportError:
            pytest.skip("torre_algebraica.py no disponible")
            
    def test_consistencia_R_psi(self):
        """Test de consistencia del radio de compactificación."""
        try:
            from torre_algebraica import NivelGeometria, c
            
            # Calcular R_Ψ desde f₀
            R_psi_f0 = c / (2 * np.pi * f0_observed)
            
            # Obtener R_Ψ de la torre algebraica
            geometria = NivelGeometria()
            R_psi_torre = geometria.R_psi
            
            # Deben coincidir
            assert abs(R_psi_f0 - R_psi_torre) / R_psi_torre < 1e-6
            
        except ImportError:
            pytest.skip("torre_algebraica.py no disponible")


# ============================================================================
# TESTS: PROPIEDADES DE NÚMEROS PRIMOS
# ============================================================================

class TestPropiedadesPrimos:
    """Tests de propiedades de números primos."""
    
    def test_primer_primo_es_2(self):
        """Test que el primer primo es 2."""
        sistema = SistemaAdelico(primes_limit=10)
        assert sistema.primes[0] == 2
        
    def test_todos_primos_mayores_1(self):
        """Test que todos los primos son > 1."""
        sistema = SistemaAdelico(primes_limit=100)
        assert np.all(sistema.primes > 1)
        
    def test_numero_primos_aproximado(self):
        """Test del número aproximado de primos (teorema de números primos)."""
        sistema = SistemaAdelico(primes_limit=1000)
        n_primos = len(sistema.primes)
        
        # π(1000) ≈ 1000/log(1000) ≈ 145
        # El valor exacto es 168
        assert 140 <= n_primos <= 180


# ============================================================================
# TESTS: VALIDACIÓN DE SALIDA JSON
# ============================================================================

class TestValidacionJSON:
    """Tests de validación de estructura JSON."""
    
    def test_estructura_json_completa(self):
        """Test que la estructura JSON es completa."""
        unificacion = UnificacionRiemannFrecuencia()
        resultado = unificacion.analisis_completo()
        
        # Campos obligatorios
        campos_obligatorios = [
            "metadata",
            "tesis_central",
            "derivacion_f0",
            "distribucion_primos",
            "mecanismo_emergencia",
            "validacion"
        ]
        
        for campo in campos_obligatorios:
            assert campo in resultado
            
    def test_metadata_completa(self):
        """Test que los metadatos son completos."""
        unificacion = UnificacionRiemannFrecuencia()
        resultado = unificacion.analisis_completo()
        
        metadata = resultado["metadata"]
        
        assert "titulo" in metadata
        assert "autor" in metadata
        assert "fecha" in metadata
        assert "version" in metadata


# ============================================================================
# FUNCIÓN PRINCIPAL DE TESTS
# ============================================================================

def run_all_tests():
    """Ejecuta todos los tests."""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
