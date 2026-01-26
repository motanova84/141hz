#!/usr/bin/env python3
"""
Tests para el análisis de resonancias Schumann y f₀

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import pytest
import numpy as np
import json
from pathlib import Path
import sys

# Importar módulo bajo test
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
import analizar_resonancias_schumann as ars


class TestConstantes:
    """Tests para verificar constantes fundamentales."""
    
    def test_f0_value(self):
        """Verifica que f₀ tiene el valor correcto."""
        assert ars.F0_HZ == 141.70001
    
    def test_schumann_fundamental(self):
        """Verifica la resonancia Schumann fundamental."""
        assert ars.SCHUMANN_RESONANCES['fundamental'] == 7.83
    
    def test_schumann_harmonics(self):
        """Verifica que existen múltiples armónicos Schumann."""
        assert len(ars.SCHUMANN_RESONANCES) >= 5
        assert 'fundamental' in ars.SCHUMANN_RESONANCES
        assert 'segunda' in ars.SCHUMANN_RESONANCES


class TestCalculoResonancia:
    """Tests para cálculos de resonancia Schumann."""
    
    def test_resonancia_teorica_modo_1(self):
        """Verifica cálculo del modo fundamental teórico."""
        f1 = ars.calcular_resonancia_schumann_teorica(1)
        # Debe estar cerca de 10.6 Hz (valor teórico aproximado)
        assert 9.0 <= f1 <= 12.0
    
    def test_resonancia_teorica_modos_superiores(self):
        """Verifica que modos superiores tienen frecuencias mayores."""
        f1 = ars.calcular_resonancia_schumann_teorica(1)
        f2 = ars.calcular_resonancia_schumann_teorica(2)
        f3 = ars.calcular_resonancia_schumann_teorica(3)
        
        assert f2 > f1
        assert f3 > f2
    
    def test_f0_dividido_por_18(self):
        """Verifica que f₀/18 ≈ Schumann fundamental."""
        f0_div_18 = ars.F0_HZ / 18
        schumann_fund = ars.SCHUMANN_RESONANCES['fundamental']
        
        # Debe estar dentro del 1%
        error_rel = abs(f0_div_18 - schumann_fund) / schumann_fund
        assert error_rel < 0.01  # < 1% error


class TestAnalisisRelacion:
    """Tests para el análisis de relación f₀-Schumann."""
    
    def test_analizar_relacion_retorna_dict(self):
        """Verifica que analizar_relacion_f0_schumann retorna un dict."""
        resultado = ars.analizar_relacion_f0_schumann()
        assert isinstance(resultado, dict)
        assert 'f0' in resultado
        assert 'relaciones' in resultado
        assert 'fundamental' in resultado
    
    def test_precision_fundamental_alta(self):
        """Verifica que la precisión de la relación fundamental es alta."""
        resultado = ars.analizar_relacion_f0_schumann()
        precision = resultado['fundamental']['precision']
        
        # Debe tener > 99% de precisión
        assert precision > 99.0
    
    def test_divisor_fundamental_es_18(self):
        """Verifica que el divisor óptimo es 18."""
        resultado = ars.analizar_relacion_f0_schumann()
        divisor = resultado['fundamental']['divisor']
        assert divisor == 18


class TestAnalisisArmonicos:
    """Tests para el análisis de armónicos."""
    
    def test_analizar_armonicos_retorna_dict(self):
        """Verifica que analizar_armonicos_schumann retorna un dict."""
        resultado = ars.analizar_armonicos_schumann()
        assert isinstance(resultado, dict)
        assert 'armonicos_teoricos' in resultado
        assert 'comparacion' in resultado
    
    def test_todos_los_modos_analizados(self):
        """Verifica que se analizan todos los modos de Schumann."""
        resultado = ars.analizar_armonicos_schumann()
        num_modos = len(resultado['comparacion'])
        assert num_modos >= 5  # Al menos 5 modos


class TestProbabilidad:
    """Tests para el análisis de probabilidad."""
    
    def test_calcular_probabilidad_retorna_dict(self):
        """Verifica que calcular_probabilidad_coincidencia retorna un dict."""
        resultado = ars.calcular_probabilidad_coincidencia()
        assert isinstance(resultado, dict)
        assert 'probabilidad' in resultado
        assert 'significancia_aproximada' in resultado
    
    def test_probabilidad_es_baja(self):
        """Verifica que la probabilidad de coincidencia aleatoria es baja."""
        resultado = ars.calcular_probabilidad_coincidencia()
        p = resultado['probabilidad']
        
        # Probabilidad debe ser < 10% (coincidencia significativa)
        assert p < 0.10
    
    def test_significancia_es_alta(self):
        """Verifica que la significancia estadística es alta."""
        resultado = ars.calcular_probabilidad_coincidencia()
        sig = resultado['significancia_aproximada']
        
        # Significancia debe ser > 10 (muy significativo)
        assert sig > 10


class TestIntegracion:
    """Tests de integración del análisis completo."""
    
    def test_analisis_completo_sin_errores(self):
        """Verifica que el análisis completo ejecuta sin errores."""
        # Ejecutar análisis completo
        resultado_relacion = ars.analizar_relacion_f0_schumann()
        resultado_armonicos = ars.analizar_armonicos_schumann()
        resultado_probabilidad = ars.calcular_probabilidad_coincidencia()
        
        # Verificar que todos retornan resultados válidos
        assert resultado_relacion is not None
        assert resultado_armonicos is not None
        assert resultado_probabilidad is not None
    
    def test_consistencia_resultados(self):
        """Verifica consistencia entre diferentes análisis."""
        resultado_relacion = ars.analizar_relacion_f0_schumann()
        
        # El divisor óptimo debe dar la mejor precisión
        precision_18 = resultado_relacion['fundamental']['precision']
        
        # Calcular precisión con otros divisores
        for divisor in [17, 19]:
            freq_calc = ars.F0_HZ / divisor
            error = abs(freq_calc - ars.SCHUMANN_RESONANCES['fundamental'])
            precision_alt = (1 - error / ars.SCHUMANN_RESONANCES['fundamental']) * 100
            
            # Divisor 18 debe tener mejor o igual precisión
            assert precision_18 >= precision_alt


class TestVisualizaciones:
    """Tests para la generación de visualizaciones."""
    
    def test_crear_visualizaciones_genera_archivo(self):
        """Verifica que se genera el archivo de visualización."""
        resultado_relacion = ars.analizar_relacion_f0_schumann()
        resultado_armonicos = ars.analizar_armonicos_schumann()
        
        imagen_path = ars.crear_visualizaciones(resultado_relacion, resultado_armonicos)
        
        # Verificar que el archivo existe
        assert Path(imagen_path).exists()
        assert imagen_path.endswith('.png')
    
    def test_guardar_resultados_genera_json(self):
        """Verifica que se genera el archivo JSON de resultados."""
        resultado_relacion = ars.analizar_relacion_f0_schumann()
        resultado_armonicos = ars.analizar_armonicos_schumann()
        resultado_probabilidad = ars.calcular_probabilidad_coincidencia()
        imagen_path = ars.crear_visualizaciones(resultado_relacion, resultado_armonicos)
        
        json_path = ars.guardar_resultados(
            resultado_relacion, 
            resultado_armonicos,
            resultado_probabilidad,
            imagen_path
        )
        
        # Verificar que el archivo existe y es válido JSON
        assert Path(json_path).exists()
        assert json_path.endswith('.json')
        
        # Verificar que se puede leer
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        assert 'titulo' in data
        assert 'f0_hz' in data
        assert 'conclusiones' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
