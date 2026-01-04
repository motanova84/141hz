#!/usr/bin/env python3
"""
Tests para las 10 Variedades Calabi-Yau Canónicas

Verifica que los datos de las 10 variedades CY sean correctos y
que satisfagan las relaciones topológicas esperadas.
"""

import csv
import sys
from pathlib import Path

import pytest

# Añadir scripts al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analizar_variedades_cy_10 import (
    cargar_variedades_cy,
    validar_euler_caracteristica,
    calcular_estadisticas
)


class TestCargaDatos:
    """Tests para la carga de datos de las variedades."""
    
    def test_cargar_variedades_existe_archivo(self):
        """Test que el archivo de datos existe."""
        filepath = Path(__file__).parent.parent / 'data' / 'calabi_yau_varieties.csv'
        assert filepath.exists(), f"Archivo no encontrado: {filepath}"
    
    def test_cargar_variedades_10_registros(self):
        """Test que se cargan exactamente 10 variedades."""
        variedades = cargar_variedades_cy()
        assert len(variedades) == 10, f"Se esperaban 10 variedades, se encontraron {len(variedades)}"
    
    def test_estructura_variedad(self):
        """Test que cada variedad tiene la estructura correcta."""
        variedades = cargar_variedades_cy()
        
        campos_requeridos = ['ID', 'Nombre', 'h11', 'h21', 'alpha', 'beta', 'kappa_pi', 'chi_Euler']
        
        for v in variedades:
            for campo in campos_requeridos:
                assert campo in v, f"Campo {campo} faltante en variedad {v.get('ID', 'desconocida')}"
    
    def test_tipos_datos(self):
        """Test que los tipos de datos son correctos."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert isinstance(v['ID'], str)
            assert isinstance(v['Nombre'], str)
            assert isinstance(v['h11'], int)
            assert isinstance(v['h21'], int)
            assert isinstance(v['alpha'], float)
            assert isinstance(v['beta'], float)
            assert isinstance(v['kappa_pi'], float)
            assert isinstance(v['chi_Euler'], int)


class TestVariedadesEspecificas:
    """Tests para variedades específicas."""
    
    def test_cy001_quintica(self):
        """Test de la variedad CY-001 (Quíntica ℂℙ⁴[5])."""
        variedades = cargar_variedades_cy()
        cy001 = variedades[0]
        
        assert cy001['ID'] == 'CY-001'
        assert 'Quíntica' in cy001['Nombre']
        assert cy001['h11'] == 1
        assert cy001['h21'] == 101
        assert cy001['chi_Euler'] == -200
        assert abs(cy001['alpha'] - 0.385) < 0.001
        assert abs(cy001['beta'] - 0.244) < 0.001
        assert abs(cy001['kappa_pi'] - 1.65805) < 0.00001
    
    def test_cy002(self):
        """Test de la variedad CY-002."""
        variedades = cargar_variedades_cy()
        cy002 = variedades[1]
        
        assert cy002['ID'] == 'CY-002'
        assert cy002['h11'] == 2
        assert cy002['h21'] == 90
        assert cy002['chi_Euler'] == -176
    
    def test_cy010_kreuzer(self):
        """Test de la variedad CY-010 (Kreuzer 302)."""
        variedades = cargar_variedades_cy()
        cy010 = variedades[9]
        
        assert cy010['ID'] == 'CY-010'
        assert 'Kreuzer' in cy010['Nombre']
        assert cy010['h11'] == 12
        assert cy010['h21'] == 48
        assert cy010['chi_Euler'] == -72
        assert abs(cy010['alpha'] - 0.402) < 0.001
        assert abs(cy010['beta'] - 0.233) < 0.001
        assert abs(cy010['kappa_pi'] - 1.65194) < 0.00001


class TestRelacionesTopologicas:
    """Tests para las relaciones topológicas."""
    
    def test_euler_caracteristica_formula(self):
        """Test que χ = 2(h11 - h21) para todas las variedades."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            chi_esperado = 2 * (v['h11'] - v['h21'])
            assert v['chi_Euler'] == chi_esperado, \
                f"Variedad {v['ID']}: χ={v['chi_Euler']}, esperado={chi_esperado}"
    
    def test_validar_euler_caracteristica(self):
        """Test de la función de validación de χ."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert validar_euler_caracteristica(v), \
                f"Validación falló para {v['ID']}"
    
    def test_euler_negativo(self):
        """Test que todas las características de Euler son negativas."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert v['chi_Euler'] < 0, \
                f"Variedad {v['ID']} tiene χ={v['chi_Euler']} >= 0"
    
    def test_h21_mayor_h11(self):
        """Test que h21 > h11 para todas las variedades (típico de CY3)."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert v['h21'] > v['h11'], \
                f"Variedad {v['ID']}: h21={v['h21']} no es mayor que h11={v['h11']}"


class TestParametrosGeometricos:
    """Tests para los parámetros geométricos α y β."""
    
    def test_alpha_rango(self):
        """Test que α está en el rango esperado [0.38, 0.41]."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert 0.38 <= v['alpha'] <= 0.41, \
                f"Variedad {v['ID']}: α={v['alpha']} fuera de rango"
    
    def test_beta_rango(self):
        """Test que β está en el rango esperado [0.23, 0.25]."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert 0.23 <= v['beta'] <= 0.25, \
                f"Variedad {v['ID']}: β={v['beta']} fuera de rango"
    
    def test_alpha_monotono_creciente(self):
        """Test que α es monotónicamente creciente."""
        variedades = cargar_variedades_cy()
        
        for i in range(len(variedades) - 1):
            assert variedades[i]['alpha'] <= variedades[i+1]['alpha'], \
                f"α no es creciente entre {variedades[i]['ID']} y {variedades[i+1]['ID']}"
    
    def test_beta_monotono_decreciente(self):
        """Test que β es monotónicamente decreciente."""
        variedades = cargar_variedades_cy()
        
        for i in range(len(variedades) - 1):
            assert variedades[i]['beta'] >= variedades[i+1]['beta'], \
                f"β no es decreciente entre {variedades[i]['ID']} y {variedades[i+1]['ID']}"


class TestEntropiaEspectral:
    """Tests para la entropía espectral κ_Π."""
    
    def test_kappa_pi_rango(self):
        """Test que κ_Π está en un rango razonable."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            # Rango esperado basado en los datos
            assert 1.65 <= v['kappa_pi'] <= 1.66, \
                f"Variedad {v['ID']}: κ_Π={v['kappa_pi']} fuera de rango"
    
    def test_kappa_pi_casi_constante(self):
        """Test que κ_Π es casi constante (universalidad)."""
        variedades = cargar_variedades_cy()
        kappa_values = [v['kappa_pi'] for v in variedades]
        
        kappa_min = min(kappa_values)
        kappa_max = max(kappa_values)
        
        # La variación debe ser pequeña (menos de 1%)
        variacion = (kappa_max - kappa_min) / kappa_min
        assert variacion < 0.01, \
            f"Variación de κ_Π es {variacion*100:.2f}%, esperado < 1%"
    
    def test_kappa_pi_positivo(self):
        """Test que κ_Π es positivo."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert v['kappa_pi'] > 0, \
                f"Variedad {v['ID']}: κ_Π={v['kappa_pi']} <= 0"


class TestEstadisticas:
    """Tests para las estadísticas calculadas."""
    
    def test_calcular_estadisticas(self):
        """Test que se pueden calcular estadísticas."""
        variedades = cargar_variedades_cy()
        stats = calcular_estadisticas(variedades)
        
        assert 'n_variedades' in stats
        assert stats['n_variedades'] == 10
        
        # Verificar que existen todas las claves de estadísticas
        for campo in ['h11', 'h21', 'alpha', 'beta', 'kappa_pi', 'chi_Euler']:
            assert campo in stats
            assert 'min' in stats[campo]
            assert 'max' in stats[campo]
            assert 'mean' in stats[campo]
            assert 'std' in stats[campo]
    
    def test_estadisticas_h11(self):
        """Test de estadísticas de h11."""
        variedades = cargar_variedades_cy()
        stats = calcular_estadisticas(variedades)
        
        assert stats['h11']['min'] == 1
        assert stats['h11']['max'] == 12
    
    def test_estadisticas_h21(self):
        """Test de estadísticas de h21."""
        variedades = cargar_variedades_cy()
        stats = calcular_estadisticas(variedades)
        
        assert stats['h21']['min'] == 48
        assert stats['h21']['max'] == 101
    
    def test_estadisticas_kappa_pi_universalidad(self):
        """Test que κ_Π tiene desviación estándar pequeña."""
        variedades = cargar_variedades_cy()
        stats = calcular_estadisticas(variedades)
        
        # La desviación estándar debe ser pequeña en comparación con la media
        cv = stats['kappa_pi']['std'] / stats['kappa_pi']['mean']  # Coeficiente de variación
        assert cv < 0.005, \
            f"Coeficiente de variación de κ_Π es {cv:.4f}, esperado < 0.005"


class TestNombresVariedades:
    """Tests para los nombres de las variedades."""
    
    def test_ids_secuenciales(self):
        """Test que los IDs son secuenciales CY-001 a CY-010."""
        variedades = cargar_variedades_cy()
        
        for i, v in enumerate(variedades, start=1):
            expected_id = f'CY-{i:03d}'
            assert v['ID'] == expected_id, \
                f"Se esperaba ID {expected_id}, se encontró {v['ID']}"
    
    def test_nombres_no_vacios(self):
        """Test que todos los nombres son no vacíos."""
        variedades = cargar_variedades_cy()
        
        for v in variedades:
            assert len(v['Nombre'].strip()) > 0, \
                f"Variedad {v['ID']} tiene nombre vacío"
    
    def test_categorias_variedades(self):
        """Test que las variedades están en las categorías esperadas."""
        variedades = cargar_variedades_cy()
        
        # Verificar que hay variedades de diferentes tipos
        categorias = set()
        for v in variedades:
            nombre = v['Nombre']
            if 'Quíntica' in nombre or 'ℂℙ' in nombre:
                categorias.add('Fermat/Hypersurface')
            elif 'CICY' in nombre:
                categorias.add('CICY')
            elif 'Toric' in nombre:
                categorias.add('Toric')
            elif 'Kreuzer' in nombre:
                categorias.add('Kreuzer')
        
        # Debe haber al menos 2 categorías diferentes
        assert len(categorias) >= 2, \
            f"Solo se encontraron {len(categorias)} categorías, esperado >= 2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
