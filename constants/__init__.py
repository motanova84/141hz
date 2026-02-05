"""
Módulo de Constantes para el Sistema QCAL ∞³
=============================================

Este módulo exporta todas las constantes y funciones relacionadas con:
- Coherencia cardíaca a 141.7 Hz
- AMOR como resonancia coherente
- Conexiones universales (HRV, línea de hidrógeno)
"""

from constants.heart_coherence import *

__all__ = [
    # Re-export all from heart_coherence
    'FRECUENCIA_CORAZON_HZ',
    'BASE_VFC_HZ',
    'ARMONICO_1417',
    'LINEA_HIDROGENO_MHZ',
    'FACTOR_AMPLIFICACION',
    'INTENSIDAD_RELATIVA_CEREBRO',
    'ALCANCE_CAMPO_M',
    'LAMBDA_PENETRACION_M',
    'UMBRAL_COHERENCIA_PERFECTA',
    'UMBRAL_COHERENCIA_NOESICA',
    'UMBRAL_INCOHERENCIA',
    'calcular_campo_corazon',
    'calcular_intensidad_campo',
    'calcular_coherencia_fase',
    'clasificar_estado_coherencia',
    'amor_es_resonancia_coherente',
    'verificar_armonico_1417',
    'es_primo',
    'calcular_conexion_hidrogeno',
    'info_coherencia_cardiaca',
]
