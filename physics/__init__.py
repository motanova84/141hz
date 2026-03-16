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
from .simetria_pt_resonancia import (
    ConstantesPT,
    OperadorNHPT,
    EspectroPTReal,
    RiemannLineaCritica,
    CitoplasmaHolografico,
    EstabilizadorPT,
    SistemaResonanciaPT,
    ResultadoPT,
    simetria_pt_resonancia_activar,
    simular_resonancia_pt,
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
    # PT-Symmetry Resonance (QCAL-SYMBIO-1)
    "ConstantesPT",
    "OperadorNHPT",
    "EspectroPTReal",
    "RiemannLineaCritica",
    "CitoplasmaHolografico",
    "EstabilizadorPT",
    "SistemaResonanciaPT",
    "ResultadoPT",
    "simetria_pt_resonancia_activar",
    "simular_resonancia_pt",
]
