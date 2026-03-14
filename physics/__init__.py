"""
Módulo de Física – Paradojas y Constantes Cosmológicas
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
from .riemann_adelic_core import (
    PHI,
    F0_HZ,
    PSI_MIN,
    BERRY_CORRECTION_BASE,
    BERRY_CORRECTION_EXPONENT,
    RIEMANN_ZEROS_T,
    PsiMinResult,
    RiemannComparison,
    calcular_psi_min,
    simulate_h_qcal,
    comparar_con_riemann,
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
    # riemann_adelic_core
    "PHI",
    "F0_HZ",
    "PSI_MIN",
    "BERRY_CORRECTION_BASE",
    "BERRY_CORRECTION_EXPONENT",
    "RIEMANN_ZEROS_T",
    "PsiMinResult",
    "RiemannComparison",
    "calcular_psi_min",
    "simulate_h_qcal",
    "comparar_con_riemann",
]
