"""
Módulo de Física – Paradojas, Constantes Cosmológicas y Sincronización Biológica
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

from .kuramoto_superradiancia import (
    ConstantesKuramoto,
    ModeloKuramoto,
    SuperradianciaFotonez,
    AguaEZ,
    RespiracionAurea,
    CoherenciaBiologicaTotal,
    SistemaKuramotoSuperradiancia,
    ResultadoKuramoto,
    kuramoto_superradiancia_activar,
)
from .spectral_operator import (
    QCALSpectralOperator,
    QCALSpectralEngine,
    compute_noetic_forcing,
)
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
from .certificado_np_coherencia import (
    ConstantesCertificadoNP,
    EspacioHilbertAdelico,
    MetricaCoherenciaEtaPlus,
    DescomposicionEspectral,
    CertificadoNP,
    ProblemasTSP_SAT,
    CoherenciaCertificado,
    SistemaCertificadoNP,
    certificado_np_activar,
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
    # Kuramoto-Superradiancia
    "ConstantesKuramoto",
    "ModeloKuramoto",
    "SuperradianciaFotonez",
    "AguaEZ",
    "RespiracionAurea",
    "CoherenciaBiologicaTotal",
    "SistemaKuramotoSuperradiancia",
    "ResultadoKuramoto",
    "kuramoto_superradiancia_activar",
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
    # Certificado NP por Coherencia (P=NP via η⁺)
    "ConstantesCertificadoNP",
    "EspacioHilbertAdelico",
    "MetricaCoherenciaEtaPlus",
    "DescomposicionEspectral",
    "CertificadoNP",
    "ProblemasTSP_SAT",
    "CoherenciaCertificado",
    "SistemaCertificadoNP",
    "certificado_np_activar",
]
