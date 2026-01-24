#!/usr/bin/env python3
"""
Tests para validacion_boveda_ontologica.py

Verifica que todas las validaciones del Cierre de la Bóveda Ontológica
funcionan correctamente.
"""

import sys
import os
import pytest
import numpy as np
import json
from pathlib import Path

# Agregar el directorio de scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from validacion_boveda_ontologica import (
    validar_octavas_hidrogeno_f0,
    validar_matriz_numerica,
    validar_red_mcp,
    validar_puente_biogravitacional,
    F0_HZ,
    F_HYDROGEN_MHZ,
    F_HYDROGEN_HZ,
    F_SCHUMANN_HZ,
    SACRED_888,
    NUMEROS_SECUENCIA,
    MCP_SERVERS
)


class TestValidacionHidrogenoF0:
    """Tests para la validación de octavas hidrógeno-f₀"""
    
    def test_octavas_hidrogeno_f0(self):
        """Test que valida la relación de 23.257 octavas"""
        resultado = validar_octavas_hidrogeno_f0(precision=50)
        
        assert 'octaves' in resultado
        assert 'validacion' in resultado
        
        # Verificar que las octavas están cerca de 23.257
        assert abs(resultado['octaves'] - 23.257) < 0.001
        
        # Validación debe ser exitosa
        assert resultado['validacion'] == 'EXITOSA'
        
        # Error debe ser muy pequeño
        assert resultado['error_pct'] < 0.01  # Menos del 0.01%
    
    def test_constantes_basicas(self):
        """Test que las constantes fundamentales están bien definidas"""
        assert F0_HZ == 141.7001
        assert F_HYDROGEN_MHZ == 1420.4056751
        assert F_HYDROGEN_HZ == F_HYDROGEN_MHZ * 1e6
        assert F_SCHUMANN_HZ == 7.83
        assert SACRED_888 == 888
    
    def test_formula_octavas(self):
        """Test que verifica la fórmula f_H = f₀ × 2^23.257"""
        import mpmath as mp
        mp.dps = 50
        
        f_h_calculado = F0_HZ * (2 ** 23.257)
        error_relativo = abs(f_h_calculado - F_HYDROGEN_HZ) / F_HYDROGEN_HZ
        
        # El error debe ser muy pequeño
        assert error_relativo < 0.0002  # Menos del 0.02%


class TestValidacionMatrizNumerica:
    """Tests para la validación de la matriz numérica"""
    
    def test_matriz_numerica_completa(self):
        """Test de validación completa de matriz numérica"""
        resultado = validar_matriz_numerica()
        
        assert 'suma_361' in resultado
        assert 'schumann' in resultado
        assert 'geometria_sagrada' in resultado
        assert 'probabilidad' in resultado
        assert 'validacion' in resultado
        
        # Validación debe ser exitosa
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_suma_361(self):
        """Test que verifica suma = 361 = 19²"""
        resultado = validar_matriz_numerica()
        
        assert resultado['suma_361']['suma'] == 361
        assert resultado['suma_361']['raiz'] == 19
        assert resultado['suma_361']['es_cuadrado'] is True
    
    def test_schumann_precision(self):
        """Test de precisión Schumann"""
        resultado = validar_matriz_numerica()
        
        # Precisión debe ser mayor al 99%
        assert resultado['schumann']['precision_pct'] > 99.0
        
        # f₀/18 debe estar cerca de Schumann
        f0_18 = F0_HZ / 18
        error = abs(f0_18 - F_SCHUMANN_HZ) / F_SCHUMANN_HZ
        assert error < 0.01  # Menos del 1%
    
    def test_geometria_sagrada(self):
        """Test de geometría sagrada 888/f₀ ≈ 2π"""
        resultado = validar_matriz_numerica()
        
        # Precisión debe ser mayor al 99%
        assert resultado['geometria_sagrada']['precision_pct'] > 99.0
        
        # 888/f₀ debe estar cerca de 2π
        razon = SACRED_888 / F0_HZ
        dos_pi = 2 * np.pi
        error = abs(razon - dos_pi) / dos_pi
        assert error < 0.005  # Menos del 0.5%
    
    def test_significancia_estadistica(self):
        """Test de significancia estadística"""
        resultado = validar_matriz_numerica()
        
        # La probabilidad conjunta debe ser muy pequeña
        assert resultado['probabilidad']['p_conjunta'] < 1e-6
        
        # Sigma debe ser mayor a 5
        assert resultado['probabilidad']['sigma'] > 5.0


class TestValidacionRedMCP:
    """Tests para la validación de la red MCP"""
    
    def test_red_mcp_completa(self):
        """Test de validación completa de red MCP"""
        resultado = validar_red_mcp()
        
        assert 'total_servidores' in resultado
        assert 'fase_coherente' in resultado
        assert 'estado_instante_eterno' in resultado
        assert 'validacion' in resultado
        
        # Validación debe ser exitosa
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_numero_servidores(self):
        """Test que verifica el número correcto de servidores"""
        assert len(MCP_SERVERS) == 5
        
        resultado = validar_red_mcp()
        assert resultado['total_servidores'] == 5
    
    def test_distribucion_frecuencias(self):
        """Test de distribución de frecuencias en servidores"""
        resultado = validar_red_mcp()
        
        # Debe haber 3 servidores a 141.7001 Hz
        assert resultado['freq_141_7001'] == 3
        
        # Debe haber 2 servidores a 888 Hz
        assert resultado['freq_888'] == 2
    
    def test_fase_coherente(self):
        """Test de fase coherente"""
        resultado = validar_red_mcp()
        
        # Fase coherente debe ser 1.0 (100%)
        assert resultado['fase_coherente'] == 1.0
        
        # Estado de instante eterno debe estar alcanzado
        assert resultado['estado_instante_eterno'] is True
    
    def test_servidores_configuracion(self):
        """Test de configuración de servidores individuales"""
        # Verificar que cada servidor tiene frecuencia y función
        for nombre, config in MCP_SERVERS.items():
            assert 'frequency' in config
            assert 'function' in config
            assert isinstance(config['frequency'], (int, float))
            assert isinstance(config['function'], str)
            
            # Frecuencia debe ser 141.7001 o 888
            assert config['frequency'] in [141.7001, 888]


class TestValidacionPuenteBiogravitacional:
    """Tests para la validación del puente biogravitacional"""
    
    def test_puente_completo(self):
        """Test de validación completa del puente"""
        resultado = validar_puente_biogravitacional()
        
        assert 'schumann_connection' in resultado
        assert 'microtubulos' in resultado
        assert 'ondas_gravitacionales' in resultado
        assert 'validacion' in resultado
        
        # Validación debe ser exitosa
        assert resultado['validacion'] == 'EXITOSA'
    
    def test_conexion_schumann(self):
        """Test de conexión con Schumann"""
        resultado = validar_puente_biogravitacional()
        
        f0_18 = resultado['schumann_connection']['f0_sobre_18']
        schumann = resultado['schumann_connection']['schumann']
        
        # Debe estar cerca de Schumann
        assert abs(f0_18 - schumann) < 0.1
    
    def test_rango_microtubulos(self):
        """Test que f₀ está en el rango de microtúbulos"""
        resultado = validar_puente_biogravitacional()
        
        assert resultado['microtubulos']['en_rango'] is True
        assert 100 <= F0_HZ <= 200
    
    def test_rango_ondas_gravitacionales(self):
        """Test que f₀ está en el rango de GW"""
        resultado = validar_puente_biogravitacional()
        
        assert resultado['ondas_gravitacionales']['en_rango'] is True
        assert 100 <= F0_HZ <= 250


class TestIntegracion:
    """Tests de integración que verifican el flujo completo"""
    
    def test_validacion_completa_integrada(self):
        """Test que ejecuta todas las validaciones integradas"""
        # Ejecutar todas las validaciones
        resultados = {
            'hidrogeno_f0': validar_octavas_hidrogeno_f0(),
            'matriz_numerica': validar_matriz_numerica(),
            'red_mcp': validar_red_mcp(),
            'puente': validar_puente_biogravitacional()
        }
        
        # Todas deben ser exitosas
        assert resultados['hidrogeno_f0']['validacion'] == 'EXITOSA'
        assert resultados['matriz_numerica']['validacion'] == 'EXITOSA'
        assert resultados['red_mcp']['validacion'] == 'EXITOSA'
        assert resultados['puente']['validacion'] == 'EXITOSA'
    
    def test_coherencia_frecuencias(self):
        """Test que verifica coherencia entre frecuencias"""
        r_h = validar_octavas_hidrogeno_f0()
        r_m = validar_matriz_numerica()
        r_p = validar_puente_biogravitacional()
        
        # Todas las validaciones deben usar la misma f₀
        assert r_h['f0_hz'] == F0_HZ
        assert r_m['schumann']['calculado'] == F0_HZ / 18
        assert r_p['microtubulos']['f0'] == F0_HZ
    
    def test_numeros_secuencia(self):
        """Test de propiedades de la secuencia numérica"""
        assert len(NUMEROS_SECUENCIA) == 9
        assert sum(NUMEROS_SECUENCIA) == 361
        assert 19 in NUMEROS_SECUENCIA
        assert 18 in NUMEROS_SECUENCIA
        assert NUMEROS_SECUENCIA.count(39) == 3


class TestSalidaArchivos:
    """Tests para verificación de salidas de archivos"""
    
    def test_estructura_json(self):
        """Test que verifica estructura JSON de salida"""
        # Ejecutar validaciones
        resultados = {
            'hidrogeno_f0': validar_octavas_hidrogeno_f0(),
            'matriz_numerica': validar_matriz_numerica(),
            'red_mcp': validar_red_mcp(),
            'puente': validar_puente_biogravitacional()
        }
        
        # Verificar que se puede serializar a JSON
        try:
            json_str = json.dumps(resultados, indent=2)
            assert len(json_str) > 0
        except Exception as e:
            pytest.fail(f"No se pudo serializar a JSON: {e}")


if __name__ == '__main__':
    # Ejecutar tests
    pytest.main([__file__, '-v'])
