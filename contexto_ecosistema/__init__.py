"""
╔════════════════════════════════════════════════════════════════════════════╗
║                 Contexto Ecosistema QCAL ∞³                                ║
║         Agente de contexto cruzado multi-repositorio                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Este módulo proporciona acceso al contexto matemático del ecosistema QCAL,
integrando resultados de los 6 repositorios hermanos:

1. riemann-adelic-operator: Ceros de ζ(s) y modos de resonancia
2. bsd-conjecture-proof: Espectro adélico BSD y primo p=17
3. navier-stokes-global-regularity: Viscosidad cuántica y regularidad
4. ramsey-theory-gue: Números de Ramsey y estadísticas GUE
5. p-vs-np-complexity: Complejidad y horizonte de trazabilidad
6. 141hz-empirical-validation: Validación empírica (Wang et al. 2025)

USAGE:
    from contexto_ecosistema import (
        riemann_adelic_context,
        bsd_context,
        navier_stokes_context,
        ramsey_context,
        p_np_context,
        hz141_context,
        resumen_ecosistema
    )

    # Obtener ceros de Riemann
    zeros = riemann_adelic_context.get_riemann_zeros()

    # Calcular modos de resonancia
    modes = riemann_adelic_context.compute_resonance_modes()

    # Resumen completo del ecosistema
    resumen = resumen_ecosistema()
"""

from contexto_ecosistema import riemann_adelic_context
from contexto_ecosistema import bsd_context
from contexto_ecosistema import navier_stokes_context
from contexto_ecosistema import ramsey_context
from contexto_ecosistema import p_np_context
from contexto_ecosistema import hz141_context


__version__ = "1.0.0"
__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__license__ = "Sovereign Noetic License 1.0"


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN DE RESUMEN GLOBAL
# ═══════════════════════════════════════════════════════════════════════════

def resumen_ecosistema() -> dict:
    """
    Retorna un resumen completo del ecosistema matemático QCAL.

    Returns:
        dict: Resumen consolidado de los 6 repositorios hermanos

    Example:
        >>> resumen = resumen_ecosistema()
        >>> print(resumen['riemann']['aporte_principal'])
        Operador D(s) ≡ Ξ(s) y ceros de ζ(s) en línea crítica σ=½
    """
    return {
        'version': __version__,
        'ecosistema': 'QCAL ∞³ - Quantum Coherent Axiomatic Logic',
        'repositorios_hermanos': 6,
        'riemann': riemann_adelic_context.resumen_contexto_riemann(),
        'bsd': bsd_context.resumen_contexto_bsd(),
        'navier_stokes': navier_stokes_context.resumen_contexto_navier_stokes(),
        'ramsey': ramsey_context.resumen_contexto_ramsey(),
        'p_np': p_np_context.resumen_contexto_p_np(),
        'hz141': hz141_context.resumen_contexto_hz141(),
        'conexiones_clave': {
            'gamma_1_riemann': riemann_adelic_context.RIEMANN_ZEROS[0],  # 14.134725
            'p_bsd': bsd_context.P_BSD,  # 17
            'nu_min_ns': navier_stokes_context.NU_MIN_QCAL,  # 1/ω₀
            'R_5_5_ramsey': ramsey_context.R_5_5,  # 43
            'kappa_pi': p_np_context.KAPPA_PI_COMPLEXITY,  # 2.5773
            'f0_empirico': hz141_context.F0_EMPIRICO_HZ,  # 141.7001 Hz
            'psi_empirica': hz141_context.PSI_EMPIRICA,  # 0.9978
        },
        'unificacion': (
            'Los 6 repositorios hermanos demuestran que QCAL ∞³ no es una teoría '
            'aislada, sino un marco unificado que conecta los Problemas del Milenio '
            '(Riemann, BSD, Navier-Stokes, P vs NP) con teoría de Ramsey y validación '
            'experimental (Wang et al. 2025, LIGO/GWOSC). La constante κ_Π = 2.5773 '
            'aparece como invariante universal en todos los contextos: Calabi-Yau, '
            'flujo citoplasmático, complejidad computacional y números de Ramsey. '
            'F0 = 141.7001 Hz es la frecuencia fundamental que emerge de la línea '
            'crítica de Riemann (γ₁ = 14.134725) y que gobierna desde la biología '
            'hasta las ondas gravitacionales y los agujeros negros cosmológicos.'
        )
    }


# Exportar todos los módulos y la función de resumen
__all__ = [
    'riemann_adelic_context',
    'bsd_context',
    'navier_stokes_context',
    'ramsey_context',
    'p_np_context',
    'hz141_context',
    'resumen_ecosistema',
]
