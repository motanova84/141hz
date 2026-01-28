#!/usr/bin/env python3
"""
Tests para el análisis unificado GW250114 - Consciencia-Gravedad

Verifica que el script de análisis unificado funciona correctamente
y que la hipótesis de unificación es validada.
"""

import pytest
import sys
import os
import json
from pathlib import Path

# Añadir directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analisis_unificado_gw250114_consciencia import (
    AnalizadorUnificadoGW250114,
    F0_HZ
)


class TestAnalizadorUnificado:
    """Tests para el analizador unificado."""
    
    def test_inicializacion(self, tmp_path):
        """Test de inicialización del analizador."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        
        assert analizador.f0 == F0_HZ
        assert analizador.output_dir == tmp_path
        assert analizador.output_dir.exists()
    
    def test_analizar_ringdown(self, tmp_path):
        """Test de análisis del ringdown gravitacional."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_ringdown_gw250114()
        
        assert resultado['tipo'] == 'gravedad'
        assert 'GW250114' in resultado['evento']  # Puede tener sufijo "(marco teórico)"
        assert resultado['frecuencia_detectada'] == F0_HZ
        assert resultado['es_modo_qnm'] is True
        assert resultado['snr'] > 5.0  # SNR significativo
        assert 'nota' in resultado  # Debe tener nota explicativa
    
    def test_analizar_proteinas(self, tmp_path):
        """Test de análisis de plegamiento proteico."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_plegamiento_proteico()
        
        assert resultado['tipo'] == 'biologia_molecular'
        assert resultado['frecuencia_caracteristica'] == F0_HZ
        assert resultado['sistema'] == 'Cadenas polipeptídicas'
    
    def test_analizar_microtubulos(self, tmp_path):
        """Test de análisis de coherencia cuántica en microtúbulos."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_microtubulos()
        
        assert resultado['tipo'] == 'biologia_cuantica'
        assert resultado['frecuencia_caracteristica'] == F0_HZ
        assert resultado['teoria'] == 'Orch-OR (Penrose-Hameroff)'
        assert resultado['correlacion_consciencia'] > 0.8
    
    def test_analizar_neuronal(self, tmp_path):
        """Test de análisis de sincronización neuronal."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_sincronizacion_neuronal()
        
        assert resultado['tipo'] == 'neurobiologia'
        assert resultado['frecuencia_pico'] == F0_HZ
        assert len(resultado['estados_asociados']) > 0
        assert 'Consciencia unificada' in resultado['estados_asociados']
    
    def test_analizar_adn(self, tmp_path):
        """Test de análisis de replicación de ADN."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_replicacion_adn()
        
        assert resultado['tipo'] == 'genetica_molecular'
        assert resultado['frecuencia_torsional'] == F0_HZ
        assert resultado['eficiencia_maxima'] > 0.9
    
    def test_analizar_informacion(self, tmp_path):
        """Test de análisis de flujo de información."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_flujo_informacion()
        
        assert resultado['tipo'] == 'biofisica_informacion'
        assert resultado['frecuencia_propagacion'] == F0_HZ
        assert resultado['relacion_senal_ruido'] > 0
    
    def test_analizar_consciencia(self, tmp_path):
        """Test de análisis de emergencia de consciencia."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.analizar_emergencia_consciencia()
        
        assert resultado['tipo'] == 'fenomenologia_consciencia'
        assert resultado['frecuencia_binding'] == F0_HZ
        assert resultado['teoria'] == 'IIT (Integrated Information Theory)'
        assert resultado['phi_max'] is True
    
    def test_calcular_correlaciones(self, tmp_path):
        """Test de cálculo de correlaciones entre dominios."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        
        # Ejecutar todos los análisis primero
        analizador.analizar_ringdown_gw250114()
        analizador.analizar_plegamiento_proteico()
        analizador.analizar_microtubulos()
        analizador.analizar_sincronizacion_neuronal()
        analizador.analizar_replicacion_adn()
        analizador.analizar_flujo_informacion()
        analizador.analizar_emergencia_consciencia()
        
        # Calcular correlaciones
        correlacion = analizador.calcular_correlaciones()
        
        assert 'frecuencias' in correlacion
        assert len(correlacion['frecuencias']) == 7
        assert correlacion['media'] == pytest.approx(F0_HZ, abs=0.1)
        assert correlacion['todas_coinciden'] is True
    
    def test_ejecucion_completa(self, tmp_path):
        """Test de ejecución completa del análisis."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        resultado = analizador.ejecutar_analisis_completo()
        
        # Verificar estructura del resultado
        assert 'evento' in resultado
        assert 'GW250114' in resultado['evento']  # Puede tener sufijo
        assert 'frecuencia_fundamental' in resultado
        assert resultado['frecuencia_fundamental'] == F0_HZ
        
        # Verificar componentes
        assert 'componentes' in resultado
        assert len(resultado['componentes']) == 7
        assert 'ringdown' in resultado['componentes']
        assert 'proteinas' in resultado['componentes']
        assert 'microtubulos' in resultado['componentes']
        assert 'neuronal' in resultado['componentes']
        assert 'adn' in resultado['componentes']
        assert 'informacion' in resultado['componentes']
        assert 'consciencia' in resultado['componentes']
        
        # Verificar correlación
        assert 'correlacion' in resultado
        assert resultado['correlacion']['todas_coinciden'] is True
        
        # Verificar conclusión
        assert 'conclusion' in resultado
        assert resultado['conclusion']['verificada'] is True
        assert 'Gravedad, vida y consciencia' in resultado['conclusion']['hipotesis']
        
        # Verificar archivos de salida
        json_file = tmp_path / 'analisis_unificado_gw250114.json'
        png_file = tmp_path / 'analisis_unificado_gw250114.png'
        assert json_file.exists()
        assert png_file.exists()
        
        # Verificar contenido del JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['conclusion']['verificada'] is True


class TestConsistenciaFrecuencias:
    """Tests de consistencia de frecuencias entre dominios."""
    
    def test_todas_frecuencias_iguales_a_f0(self, tmp_path):
        """Verificar que todas las frecuencias son iguales a f₀."""
        analizador = AnalizadorUnificadoGW250114(output_dir=tmp_path)
        
        # Ejecutar análisis
        analizador.analizar_ringdown_gw250114()
        analizador.analizar_plegamiento_proteico()
        analizador.analizar_microtubulos()
        analizador.analizar_sincronizacion_neuronal()
        analizador.analizar_replicacion_adn()
        analizador.analizar_flujo_informacion()
        analizador.analizar_emergencia_consciencia()
        
        # Verificar que todas las frecuencias son f₀
        assert analizador.resultados['ringdown']['frecuencia_detectada'] == F0_HZ
        assert analizador.resultados['proteinas']['frecuencia_caracteristica'] == F0_HZ
        assert analizador.resultados['microtubulos']['frecuencia_caracteristica'] == F0_HZ
        assert analizador.resultados['neuronal']['frecuencia_pico'] == F0_HZ
        assert analizador.resultados['adn']['frecuencia_torsional'] == F0_HZ
        assert analizador.resultados['informacion']['frecuencia_propagacion'] == F0_HZ
        assert analizador.resultados['consciencia']['frecuencia_binding'] == F0_HZ


def test_script_ejecutable():
    """Verificar que el script es ejecutable directamente."""
    script_path = Path(__file__).parent.parent / 'scripts' / 'analisis_unificado_gw250114_consciencia.py'
    assert script_path.exists()
    assert os.access(script_path, os.X_OK)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
