#!/usr/bin/env python3
"""
Tests para validacion_matriz_numerica.py

Verifica que todas las funciones de validación funcionan correctamente.
"""

import sys
import os
import pytest
import numpy as np
import json
from pathlib import Path

# Agregar el directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.validacion_matriz_numerica import (
    validar_suma_361,
    validar_schumann_f0_18,
    validar_schumann_f0_19,
    validar_888_sobre_f0,
    validar_bandas_cerebrales,
    validar_red_numerica,
    calcular_probabilidad_conjunta,
    F0_HZ,
    NUMEROS_SECUENCIA,
    SCHUMANN_HZ,
    NUMERO_888
)


class TestValidacionMatrizNumerica:
    """Tests para las funciones de validación de la matriz numérica"""
    
    def test_suma_361(self):
        """Test validación de suma = 361 = 19²"""
        resultado = validar_suma_361()
        
        assert resultado['suma'] == 361
        assert resultado['raiz'] == 19
        assert resultado['es_cuadrado_perfecto'] is True
        assert resultado['autorreferencia'] is True
        assert resultado['validacion'] == 'EXITOSA'
        assert resultado['probabilidad_pct'] < 5.0  # Menos del 5% (muy improbable)
    
    def test_schumann_18(self):
        """Test validación f₀/18 ≈ Schumann"""
        resultado = validar_schumann_f0_18()
        
        assert 'f0_sobre_18' in resultado
        assert 'schumann' in resultado
        assert resultado['schumann'] == SCHUMANN_HZ
        
        # Error debe ser menor al 1%
        assert resultado['error_pct'] < 1.0
        
        # Precisión debe ser mayor al 99%
        assert resultado['precision_pct'] > 99.0
        
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_schumann_19(self):
        """Test validación f₀/19 comparación con Schumann"""
        resultado = validar_schumann_f0_19()
        
        assert 'f0_sobre_19' in resultado
        assert resultado['mejor_divisor'] == 18
        assert resultado['validacion'] == 'INFORMATIVA'
    
    def test_888_2pi(self):
        """Test validación 888/f₀ ≈ 2π"""
        resultado = validar_888_sobre_f0()
        
        dos_pi = 2 * np.pi
        
        assert 'precision_pct' in resultado
        
        # Precisión debe ser mayor al 99.5%
        assert resultado['precision_pct'] > 99.5
        
        # Error relativo debe ser menor al 0.5%
        assert resultado['error_pct'] < 0.5
        
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_bandas_cerebrales(self):
        """Test validación de bandas cerebrales"""
        resultado = validar_bandas_cerebrales()
        
        assert 'bandas' in resultado
        assert 'validaciones_exitosas' in resultado
        
        # Verificar que todas las bandas principales están presentes
        bandas_esperadas = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        for banda in bandas_esperadas:
            assert banda in resultado['bandas']
            assert resultado['bandas'][banda]['en_rango'] is True
        
        # Todas las bandas deben estar en rango
        assert resultado['validaciones_exitosas'] == resultado['total_bandas']
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_red_numerica(self):
        """Test validación de red numérica"""
        resultado = validar_red_numerica()
        
        assert 'trinidad_39' in resultado
        assert resultado['trinidad_39'] == 3  # 39 aparece 3 veces
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_probabilidad_conjunta(self):
        """Test cálculo de probabilidad conjunta"""
        resultado = calcular_probabilidad_conjunta()
        
        assert 'p_conjunta' in resultado
        assert 'p_individual' in resultado
        
        # La probabilidad conjunta debe ser extremadamente pequeña
        assert resultado['p_conjunta'] < 1e-6
        
        # Debe ser altamente significativa
        assert resultado['validacion'] == 'ALTAMENTE_SIGNIFICATIVA'
    
    def test_constantes_basicas(self):
        """Test que las constantes básicas están correctamente definidas"""
        assert F0_HZ == 141.70001
        assert SCHUMANN_HZ == 7.83
        assert NUMERO_888 == 888.0
        assert len(NUMEROS_SECUENCIA) == 9
        assert sum(NUMEROS_SECUENCIA) == 361
    
    def test_numeros_secuencia(self):
        """Test propiedades de la secuencia de números"""
        # Verificar que 19 aparece en la secuencia
        assert 19 in NUMEROS_SECUENCIA
        
        # Verificar que 18 aparece en la secuencia
        assert 18 in NUMEROS_SECUENCIA
        
        # Verificar que 39 aparece exactamente 3 veces
        assert NUMEROS_SECUENCIA.count(39) == 3
    
    def test_divisores_cerebrales(self):
        """Test que los divisores cerebrales son correctos"""
        from scripts.validacion_matriz_numerica import DIVISORES_CEREBRALES
        
        # Verificar divisores específicos
        assert DIVISORES_CEREBRALES['delta'] == 36
        assert DIVISORES_CEREBRALES['theta'] == 18
        assert DIVISORES_CEREBRALES['alpha'] == 11
        assert DIVISORES_CEREBRALES['beta'] == 6
        assert DIVISORES_CEREBRALES['gamma'] == 2
        
        # Verificar que delta = theta × 2
        assert DIVISORES_CEREBRALES['delta'] == DIVISORES_CEREBRALES['theta'] * 2
    
    def test_relaciones_matematicas(self):
        """Test relaciones matemáticas fundamentales"""
        # f₀/18 debe estar cerca de Schumann
        f0_sobre_18 = F0_HZ / 18
        error_schumann = abs(f0_sobre_18 - SCHUMANN_HZ) / SCHUMANN_HZ
        assert error_schumann < 0.01  # Menos del 1%
        
        # 888/f₀ debe estar cerca de 2π
        razon = NUMERO_888 / F0_HZ
        dos_pi = 2 * np.pi
        error_2pi = abs(razon - dos_pi) / dos_pi
        assert error_2pi < 0.005  # Menos del 0.5%
        
        # √361 debe ser 19
        assert int(np.sqrt(361)) == 19
        assert 19 ** 2 == 361


class TestIntegracion:
    """Tests de integración que verifican el flujo completo"""
    
    def test_validacion_completa(self):
        """Test que ejecuta la validación completa"""
        # Ejecutar todas las validaciones
        resultados = {
            'suma_361': validar_suma_361(),
            'schumann_18': validar_schumann_f0_18(),
            'schumann_19': validar_schumann_f0_19(),
            '888_2pi': validar_888_sobre_f0(),
            'bandas_cerebrales': validar_bandas_cerebrales(),
            'red_numerica': validar_red_numerica(),
            'probabilidad': calcular_probabilidad_conjunta()
        }
        
        # Verificar que todas las validaciones principales son exitosas
        assert resultados['suma_361']['validacion'] == 'EXITOSA'
        assert resultados['schumann_18']['validacion'] == 'EXITOSA'
        assert resultados['888_2pi']['validacion'] == 'EXITOSA'
        assert resultados['bandas_cerebrales']['validacion'] == 'EXITOSA'
        assert resultados['red_numerica']['validacion'] == 'EXITOSA'
        assert resultados['probabilidad']['validacion'] == 'ALTAMENTE_SIGNIFICATIVA'
    
    def test_coherencia_resultados(self):
        """Test que los resultados son coherentes entre sí"""
        r1 = validar_suma_361()
        r2 = validar_schumann_f0_18()
        r3 = validar_bandas_cerebrales()
        
        # La raíz de 361 debe ser 19
        assert r1['raiz'] == 19
        
        # El divisor para theta debe ser 18
        assert r3['bandas']['theta']['divisor'] == 18
        
        # f₀/18 debe coincidir entre validaciones
        f0_18_esperado = F0_HZ / 18
        assert abs(r2['f0_sobre_18'] - f0_18_esperado) < 1e-6


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v'])
