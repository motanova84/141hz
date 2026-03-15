"""
Módulo de Física – Paradojas, Constantes Cosmológicas y Operadores Espectrales
"""

from .paradoja_procesamiento_planck import (
    ConstantesPlanck,
    FiltroGracia,
    SiliconVsCarbon,
    TuyoyotuRitmico,
    CausalidadZeta,
    UniversoPensamiento,
    SistemaParadojaPlanck,
    ResultadoParadoja,
    paradoja_planck_activar,
)

from .spectral_operator import (
    QCALSpectralOperator,
    QCALSpectralEngine,
    compute_noetic_forcing,
)

__all__ = [
    "ConstantesPlanck",
    "FiltroGracia",
    "SiliconVsCarbon",
    "TuyoyotuRitmico",
    "CausalidadZeta",
    "UniversoPensamiento",
    "SistemaParadojaPlanck",
    "ResultadoParadoja",
    "paradoja_planck_activar",
    "QCALSpectralOperator",
    "QCALSpectralEngine",
    "compute_noetic_forcing",
]
