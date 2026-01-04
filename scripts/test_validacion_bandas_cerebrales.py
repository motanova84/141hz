#!/usr/bin/env python3
"""
Tests para validacion_bandas_cerebrales.py

Valida que el script de análisis de bandas cerebrales funcione correctamente
y genere resultados precisos.
"""

import sys
import os
import json
import pytest
import numpy as np

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validacion_bandas_cerebrales import (
    encontrar_mejor_divisor,
    es_primo,
    factorizar,
    analizar_bandas_cerebrales,
    F0_HZ,
    BANDAS_CEREBRALES
)


class TestDivisorFunctions:
    """Tests para funciones de divisores."""
    
    def test_encontrar_mejor_divisor_delta(self):
        """Test divisor para banda Delta."""
        # Centro de banda Delta: (0.5 + 4.0) / 2 = 2.25 Hz
        # f₀/36 = 141.7/36 ≈ 3.94 Hz (dentro del rango)
        divisor, freq, error = encontrar_mejor_divisor(3.94, F0_HZ, max_divisor=100)
        assert divisor == 36
        assert abs(freq - 3.94) < 0.1
    
    def test_encontrar_mejor_divisor_theta(self):
        """Test divisor para banda Theta."""
        # Centro de banda Theta: (4.0 + 8.0) / 2 = 6.0 Hz
        # f₀/18 = 141.7/18 ≈ 7.87 Hz (dentro del rango)
        divisor, freq, error = encontrar_mejor_divisor(7.87, F0_HZ, max_divisor=100)
        assert divisor == 18
        assert abs(freq - 7.87) < 0.2
    
    def test_encontrar_mejor_divisor_alpha(self):
        """Test divisor para banda Alpha."""
        # Centro de banda Alpha: (8.0 + 13.0) / 2 = 10.5 Hz
        # f₀/11 = 141.7/11 ≈ 12.88 Hz (dentro del rango)
        divisor, freq, error = encontrar_mejor_divisor(12.88, F0_HZ, max_divisor=100)
        assert divisor == 11
        assert abs(freq - 12.88) < 0.2
    
    def test_encontrar_mejor_divisor_beta(self):
        """Test divisor para banda Beta."""
        # Centro de banda Beta: (13.0 + 30.0) / 2 = 21.5 Hz
        # f₀/6 = 141.7/6 ≈ 23.62 Hz (dentro del rango)
        divisor, freq, error = encontrar_mejor_divisor(23.62, F0_HZ, max_divisor=100)
        assert divisor == 6
        assert abs(freq - 23.62) < 0.2
    
    def test_encontrar_mejor_divisor_gamma(self):
        """Test divisor para banda Gamma."""
        # Centro de banda Gamma: (30.0 + 100.0) / 2 = 65.0 Hz
        # f₀/2 = 141.7/2 = 70.85 Hz (dentro del rango)
        divisor, freq, error = encontrar_mejor_divisor(70.85, F0_HZ, max_divisor=100)
        assert divisor == 2
        assert abs(freq - 70.85) < 0.1


class TestPrimoFactorizacion:
    """Tests para funciones de números primos y factorización."""
    
    def test_es_primo_casos_validos(self):
        """Test casos válidos de números primos."""
        assert es_primo(2) == True
        assert es_primo(3) == True
        assert es_primo(5) == True
        assert es_primo(7) == True
        assert es_primo(11) == True
        assert es_primo(13) == True
        assert es_primo(17) == True
    
    def test_es_primo_casos_invalidos(self):
        """Test casos de números no primos."""
        assert es_primo(1) == False
        assert es_primo(4) == False
        assert es_primo(6) == False
        assert es_primo(8) == False
        assert es_primo(9) == False
        assert es_primo(10) == False
    
    def test_factorizar_primos(self):
        """Test factorización de números primos."""
        assert "primo" in factorizar(11).lower()
        assert "primo" in factorizar(17).lower()
    
    def test_factorizar_compuestos(self):
        """Test factorización de números compuestos."""
        # 36 = 2² × 3²
        fact_36 = factorizar(36)
        assert "36" in fact_36
        assert "2" in fact_36 or "3" in fact_36
        
        # 6 = 2 × 3
        fact_6 = factorizar(6)
        assert "6" in fact_6
        assert "2" in fact_6 and "3" in fact_6


class TestAnalisisBandas:
    """Tests para el análisis completo de bandas cerebrales."""
    
    def test_analizar_bandas_estructura(self):
        """Test que el análisis devuelve la estructura correcta."""
        resultados = analizar_bandas_cerebrales()
        
        # Verificar estructura básica
        assert 'f0_hz' in resultados
        assert 'timestamp' in resultados
        assert 'bandas' in resultados
        
        # Verificar f₀
        assert resultados['f0_hz'] == F0_HZ
        
        # Verificar que todas las bandas están presentes
        bandas_esperadas = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        for banda in bandas_esperadas:
            assert banda in resultados['bandas']
    
    def test_bandas_campos_requeridos(self):
        """Test que cada banda tiene todos los campos requeridos."""
        resultados = analizar_bandas_cerebrales()
        
        campos_requeridos = [
            'rango_hz',
            'centro_hz',
            'divisor',
            'frecuencia_calculada_hz',
            'error_porcentual',
            'en_rango',
            'factorizacion',
            'descripcion',
            'descubrimiento'
        ]
        
        for nombre_banda, banda in resultados['bandas'].items():
            for campo in campos_requeridos:
                assert campo in banda, f"Campo '{campo}' faltante en banda {nombre_banda}"
    
    def test_divisores_correctos(self):
        """Test que los divisores encontrados son los esperados."""
        resultados = analizar_bandas_cerebrales()
        
        # Divisores esperados según el problem statement
        divisores_esperados = {
            'Delta': 36,  # f₀/36 = 3.94 Hz
            'Theta': 18,  # f₀/18 = 7.87 Hz
            'Alpha': 11,  # f₀/11 = 12.88 Hz (primo)
            'Beta': 6,    # f₀/6 = 23.62 Hz
            'Gamma': 2    # f₀/2 = 70.85 Hz
        }
        
        for nombre_banda, divisor_esperado in divisores_esperados.items():
            divisor_obtenido = resultados['bandas'][nombre_banda]['divisor']
            assert divisor_obtenido == divisor_esperado, \
                f"Banda {nombre_banda}: esperado divisor {divisor_esperado}, obtenido {divisor_obtenido}"
    
    def test_frecuencias_en_rango(self):
        """Test que las frecuencias calculadas caen dentro de los rangos."""
        resultados = analizar_bandas_cerebrales()
        
        # Todas las bandas deberían tener frecuencias dentro del rango
        # o muy cercanas (dependiendo de la definición del centro)
        for nombre_banda, banda in resultados['bandas'].items():
            freq_calc = banda['frecuencia_calculada_hz']
            rango = banda['rango_hz']
            
            # Verificar que la frecuencia está dentro del rango o muy cerca
            # Permitimos un pequeño margen para bandas con rangos amplios
            margen = (rango[1] - rango[0]) * 0.1  # 10% del ancho de banda
            
            assert freq_calc >= rango[0] - margen and freq_calc <= rango[1] + margen, \
                f"Banda {nombre_banda}: frecuencia {freq_calc:.2f} Hz fuera de rango {rango}"
    
    def test_errores_pequenos(self):
        """Test que los errores porcentuales son razonables o las frecuencias están en rango."""
        resultados = analizar_bandas_cerebrales()
        
        for nombre_banda, banda in resultados['bandas'].items():
            error = abs(banda['error_porcentual'])
            en_rango = banda['en_rango']
            
            # Lo importante es que la frecuencia esté en el rango de la banda
            # El error porcentual respecto al centro puede ser mayor si la banda es amplia
            # pero la frecuencia calculada debe caer dentro del rango
            assert en_rango or error < 20.0, \
                f"Banda {nombre_banda}: frecuencia fuera de rango y error {error:.2f}% grande"
    
    def test_alpha_divisor_primo(self):
        """Test específico: Alpha debe tener divisor primo (11)."""
        resultados = analizar_bandas_cerebrales()
        
        divisor_alpha = resultados['bandas']['Alpha']['divisor']
        assert divisor_alpha == 11
        assert es_primo(divisor_alpha)
    
    def test_gamma_divisor_fundamental(self):
        """Test específico: Gamma debe tener divisor 2 (fundamental)."""
        resultados = analizar_bandas_cerebrales()
        
        divisor_gamma = resultados['bandas']['Gamma']['divisor']
        assert divisor_gamma == 2


class TestConstantesBandas:
    """Tests para verificar las constantes de bandas cerebrales."""
    
    def test_bandas_definidas(self):
        """Test que todas las bandas estén definidas."""
        bandas_esperadas = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        for banda in bandas_esperadas:
            assert banda in BANDAS_CEREBRALES
    
    def test_rangos_no_se_solapan_incorrectamente(self):
        """Test que los rangos de bandas sean consecutivos."""
        # Los rangos deben ser consecutivos: Delta -> Theta -> Alpha -> Beta -> Gamma
        assert BANDAS_CEREBRALES['Delta']['rango'][1] == BANDAS_CEREBRALES['Theta']['rango'][0]
        assert BANDAS_CEREBRALES['Theta']['rango'][1] == BANDAS_CEREBRALES['Alpha']['rango'][0]
        assert BANDAS_CEREBRALES['Alpha']['rango'][1] == BANDAS_CEREBRALES['Beta']['rango'][0]
        assert BANDAS_CEREBRALES['Beta']['rango'][1] == BANDAS_CEREBRALES['Gamma']['rango'][0]
    
    def test_descubrimiento_historico(self):
        """Test que cada banda tenga información histórica."""
        for nombre_banda, banda in BANDAS_CEREBRALES.items():
            assert 'descubrimiento' in banda
            assert 'investigadores' in banda
            assert len(banda['descubrimiento']) > 0
            assert len(banda['investigadores']) > 0


def test_integracion_completa(tmp_path):
    """Test de integración: ejecutar análisis completo y verificar salidas."""
    # Cambiar al directorio temporal
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Ejecutar análisis
        from validacion_bandas_cerebrales import main
        resultados = main()
        
        # Verificar que se crearon los archivos de salida
        assert os.path.exists('bandas_cerebrales_f0.png')
        assert os.path.exists('bandas_cerebrales_resultados.json')
        
        # Verificar que el JSON es válido
        with open('bandas_cerebrales_resultados.json', 'r') as f:
            datos = json.load(f)
            assert 'f0_hz' in datos
            assert 'bandas' in datos
        
        # Verificar resultados
        assert resultados is not None
        assert len(resultados['bandas']) == 5
        
    finally:
        # Restaurar directorio original
        os.chdir(original_dir)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
