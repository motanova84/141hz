"""
Módulo de Física QCAL
Constantes físicas fundamentales y frecuencias sagradas
"""

from .FRECUENCIAS_SAGRADAS import (
    # Frecuencias Sagradas
    FRECUENCIA_INTENCION,
    FRECUENCIA_AMOR,
    FRECUENCIA_MANIFESTACION,
    FRECUENCIA_FIRMA,
    FRECUENCIA_FUSION,
    FRECUENCIA_PULSO_PICODE,
    FRECUENCIA_SCHUMANN,
    FRECUENCIA_CUBO,
    FRECUENCIA_FIBONACCI,
    FRECUENCIA_UNIVERSAL,
    FRECUENCIA_ADN,
    F0_HZ,
    F888_HZ,
    
    # Constantes Matemáticas
    PHI,
    PI,
    TAU,
    E,
    INFINITO,
    
    # Funciones de utilidad
    obtener_armónico,
    es_armónico_de_f0,
    mostrar_relaciones_frecuencias,
)

from .pleroma_carbono_silicio import (
    # Frecuencias del Pleroma
    F_SILICIO_DIVINO,
    F_SI,
    F_CARBONO_DIVINO,
    F_C,

    # Constante de Ziusudra
    CONSTANTE_ZIUSUDRA,
    DELTA_F_ZIUSUDRA,
    DELTA_F,

    # Tensión de la Encarnación
    TENSION_ENCARNACION,
    KAPPA_ENCARNACION,

    # Período del Batimiento
    PERIODO_BATIMIENTO_S,
    FRECUENCIA_BATIMIENTO,

    # Funciones del Pleroma
    calcular_batimiento,
    coherencia_psi,
    hamiltoniano_total,
    frecuencia_media_pleroma,
    mostrar_pleroma,
)

from .reloj_universo_f0 import (
    # Constantes derivadas de Riemann
    GAMMA_1,
    MULTIPLICADOR_TUYOYOTU,
    F0_EXACT_HZ,
    DELTA_FASE_ZIUSUDRA,
    FISURA_ZIUSUDRA,
    F0_OCTAVA_HZ,
    CONSTANTES_FISICAS,
)

__all__ = [
    # Frecuencias Sagradas
    'FRECUENCIA_INTENCION',
    'FRECUENCIA_AMOR',
    'FRECUENCIA_MANIFESTACION',
    'FRECUENCIA_FIRMA',
    'FRECUENCIA_FUSION',
    'FRECUENCIA_PULSO_PICODE',
    'FRECUENCIA_SCHUMANN',
    'FRECUENCIA_CUBO',
    'FRECUENCIA_FIBONACCI',
    'FRECUENCIA_UNIVERSAL',
    'FRECUENCIA_ADN',
    'F0_HZ',
    'F888_HZ',
    
    # Constantes Matemáticas
    'PHI',
    'PI',
    'TAU',
    'E',
    'INFINITO',
    
    # Funciones
    'obtener_armónico',
    'es_armónico_de_f0',
    'mostrar_relaciones_frecuencias',

    # Pleroma Carbono-Silicio
    'F_SILICIO_DIVINO',
    'F_SI',
    'F_CARBONO_DIVINO',
    'F_C',
    'CONSTANTE_ZIUSUDRA',
    'DELTA_F_ZIUSUDRA',
    'DELTA_F',
    'TENSION_ENCARNACION',
    'KAPPA_ENCARNACION',
    'PERIODO_BATIMIENTO_S',
    'FRECUENCIA_BATIMIENTO',
    'calcular_batimiento',
    'coherencia_psi',
    'hamiltoniano_total',
    'frecuencia_media_pleroma',
    'mostrar_pleroma',

    # Constantes derivadas de Riemann (reloj_universo_f0)
    'GAMMA_1',
    'MULTIPLICADOR_TUYOYOTU',
    'F0_EXACT_HZ',
    'DELTA_FASE_ZIUSUDRA',
    'FISURA_ZIUSUDRA',
    'F0_OCTAVA_HZ',
    'CONSTANTES_FISICAS',
]
