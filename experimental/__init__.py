#!/usr/bin/env python3
"""
Módulo de Protocolos de Validación Experimental QCAL

Este módulo implementa protocolos experimentales rigurosos para validar
la existencia física de SU(Ψ) y T_μν(Φ).

Fases:
- Fase I: Validación de SU(Ψ) - Grupo de Coherencia Cuántica
- Fase II: Validación de T_μν(Φ) - Tensor de Stress Emocional
- Fase III: Validación a Nivel Colectivo
- Fase IV: Meta-Análisis y Síntesis

Autor: José Manuel Mota Burruezo (JMMB)
Institución: Instituto Consciencia Cuántica
"""

__version__ = "1.0.0"
__author__ = "José Manuel Mota Burruezo"

# Imports with error handling for missing dependencies
try:
    from .fase1_su_psi import (
        extraer_estado_psi,
        calcular_coherencia,
        test_estructura_grupo_SU,
        analizar_geodesicas,
        analisis_estadistico_SU
    )
    _fase1_available = True
except ImportError as e:
    _fase1_available = False
    print(f"Warning: Fase I imports failed: {e}")

try:
    from .fase2_tensor_stress import (
        construir_campo_emocional,
        calcular_tensor_stress_energia,
        calcular_curvatura_emocional,
        test_correlacion_T00_amigdala,
        test_flujo_emocional_diadas,
        rct_frecuencia_141_7_Hz,
        estudio_longitudinal_curvatura
    )
    _fase2_available = True
except ImportError as e:
    _fase2_available = False
    print(f"Warning: Fase II imports failed: {e}")

try:
    from .fase3_red_social import (
        experimento_red_social,
        analizar_efectos_red,
        analizar_efectos_segundo_orden
    )
    _fase3_available = True
except ImportError as e:
    _fase3_available = False
    print(f"Warning: Fase III imports failed: {e}")

try:
    from .fase4_meta_analisis import (
        meta_analisis_QCAL,
        generar_conclusion,
        generar_recomendacion,
        generar_roadmap_validacion
    )
    _fase4_available = True
except ImportError as e:
    _fase4_available = False
    print(f"Warning: Fase IV imports failed: {e}")

__all__ = [
    # Fase I
    'extraer_estado_psi',
    'calcular_coherencia',
    'test_estructura_grupo_SU',
    'analizar_geodesicas',
    'analisis_estadistico_SU',
    # Fase II
    'construir_campo_emocional',
    'calcular_tensor_stress_energia',
    'calcular_curvatura_emocional',
    'test_correlacion_T00_amigdala',
    'test_flujo_emocional_diadas',
    'rct_frecuencia_141_7_Hz',
    'estudio_longitudinal_curvatura',
    # Fase III
    'experimento_red_social',
    'analizar_efectos_red',
    'analizar_efectos_segundo_orden',
    # Fase IV
    'meta_analisis_QCAL',
    'generar_conclusion',
    'generar_recomendacion',
    'generar_roadmap_validacion',
]
