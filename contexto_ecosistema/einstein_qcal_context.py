"""
╔════════════════════════════════════════════════════════════════════════════╗
║     Contexto Einstein-QCAL — Anclaje al Ecosistema Matemático QCAL ∞³     ║
║      Métrica de Coherencia Espectral y Velocidad de la Luz Efectiva       ║
╚════════════════════════════════════════════════════════════════════════════╝

Este módulo proporciona el contexto del postulado Einstein-QCAL dentro del
ecosistema matemático más amplio de QCAL ∞³ y sus repositorios hermanos.

QUÉ APORTA:
- Operador de coherencia Ψ̂ sobre L²(𝔸_ℚ/ℚ) deformando la métrica de Minkowski
- Velocidad efectiva de la luz c_eff(Ψ) = c · Ω(Ψ)
- Tensor de energía-momento de coherencia T_μν^(Ψ) y constante Λ(Ψ) emergente
- Tabla comparativa: estado incoherente vs. estado resonante

CONEXIÓN CON EL ECOSISTEMA:
┌─────────────────────────────────────────────────────────────────────────┐
│ Riemann-adélico: los ceros γₙ de ζ(s) fijan los modos de resonancia    │
│   f_n = f₀ · γₙ / γ₁  que entran como frecuencias propias de H_QCAL   │
│                                                                         │
│ BSD adélico: el espectro adélico ancla p=17 (ciclo Magicicada) y f₀    │
│   como emergentes de la geometría aritmética de curvas elípticas        │
│                                                                         │
│ Navier-Stokes: ν_min QCAL limita la dispersión p-ádica en el árbol     │
│   de Bruhat-Tits; el flujo citoplasmático sigue geodésicas de g_μν(Ψ) │
│                                                                         │
│ Ramsey: κ_Π = 2.5773 acota vibracionalmente la red métrica              │
│   |Ω(Ψ) - 1| < κ_Π · Δ_gap / (2π f₀)                                 │
│                                                                         │
│ P≠NP: el horizonte de trazabilidad computacional se expresa como        │
│   O(2^n) → O(n^κ_Π) por resonancia exacta en f₀                       │
└─────────────────────────────────────────────────────────────────────────┘
"""

from qcal.constants import F0_HZ, C, KAPPA_PI
from qcal.einstein_qcal import (
    CoherenceState,
    EinsteinQCALField,
    EinsteinQCALMetric,
    CoherenceTensor,
    c_eff,
    lambda_emergent,
    omega_coupling,
    quantum_refractive_index,
    PSI_RESONANCE,
    ALPHA_ADELIC,
    LAMBDA_0,
    KAPPA_GR,
    G_NEWTON,
)

# ═══════════════════════════════════════════════════════════════════════════
# RE-EXPORTACIONES PARA EL ECOSISTEMA
# ═══════════════════════════════════════════════════════════════════════════

__all__ = [
    # Clases principales
    "CoherenceState",
    "EinsteinQCALField",
    "EinsteinQCALMetric",
    "CoherenceTensor",
    # Funciones clave
    "c_eff",
    "lambda_emergent",
    "omega_coupling",
    "quantum_refractive_index",
    # Constantes
    "PSI_RESONANCE",
    "ALPHA_ADELIC",
    "LAMBDA_0",
    "KAPPA_GR",
    "G_NEWTON",
    # Funciones de contexto
    "get_resonant_field",
    "get_incoherent_field",
    "compute_c_eff_at_psi",
    "riemann_mode_coherence",
]


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CONTEXTO — INTEGRACIÓN CON REPOSITORIOS HERMANOS
# ═══════════════════════════════════════════════════════════════════════════

def get_resonant_field() -> EinsteinQCALField:
    """
    Retorna el campo Einstein-QCAL en estado de resonancia absoluta.

    Ψ = Ψ_res = 0.999999 → c_eff ≈ c, Λ ≈ 0, métrica Minkowski.

    Retorna
    -------
    EinsteinQCALField
        Campo en coherencia máxima.
    """
    return EinsteinQCALField(state=CoherenceState(psi=PSI_RESONANCE, f_observer=F0_HZ))


def get_incoherent_field(psi: float = 0.5) -> EinsteinQCALField:
    """
    Retorna el campo Einstein-QCAL en estado de incoherencia parcial.

    Parámetros
    ----------
    psi : float
        Nivel de coherencia Ψ ∈ [0, 1).

    Retorna
    -------
    EinsteinQCALField
        Campo en estado incoherente.
    """
    return EinsteinQCALField(state=CoherenceState(psi=psi, f_observer=F0_HZ))


def compute_c_eff_at_psi(psi: float, f_observer: float = F0_HZ) -> dict:
    """
    Calcula c_eff, Ω y n para un estado de coherencia dado.

    Parámetros
    ----------
    psi : float
        Coherencia Ψ ∈ [0, 1].
    f_observer : float
        Frecuencia del procesador observador [Hz].

    Retorna
    -------
    dict
        Resultados: c_eff_m_s, omega, n_refraction, lambda_eff_m2.
    """
    state = CoherenceState(psi=psi, f_observer=f_observer)
    field_ = EinsteinQCALField(state=state)
    return field_.summary()


def riemann_mode_coherence(gamma_n: float, gamma_1: float = 14.134725) -> CoherenceState:
    """
    Genera un estado de coherencia sintonizado al n-ésimo cero de Riemann.

    Conexión con repositorio hermano Riemann-adélico:
        f_n = f₀ · γₙ / γ₁

    El operador H_QCAL tiene como frecuencias propias los modos Riemannianos.
    La coherencia Ψ_n se define como la proyección espectral en ese modo:

        Ψ_n = 1 − |f_n − f₀| / f₀

    Parámetros
    ----------
    gamma_n : float
        Parte imaginaria del n-ésimo cero de ζ(s) en la línea crítica σ=½.
    gamma_1 : float
        Parte imaginaria del primer cero (γ₁ = 14.134725).

    Retorna
    -------
    CoherenceState
        Estado de coherencia sintonizado al modo Riemanniano f_n.
    """
    f_n = F0_HZ * gamma_n / gamma_1
    # Coherencia como proximidad relativa al modo fundamental
    psi_n = max(0.0, min(1.0, 1.0 - abs(f_n - F0_HZ) / F0_HZ))
    return CoherenceState(psi=psi_n, f_observer=f_n)


# ═══════════════════════════════════════════════════════════════════════════
# RESUMEN DEL ECOSISTEMA
# ═══════════════════════════════════════════════════════════════════════════

ECOSYSTEM_SUMMARY = {
    "module": "einstein_qcal",
    "description": "Postulado Einstein-QCAL: métrica deformada por coherencia espectral",
    "key_result": "c_eff(Ψ) = c · Ω(Ψ)  →  c invariante sii Ψ → 1 (resonancia con f₀)",
    "f0_hz": F0_HZ,
    "c_m_s": C,
    "psi_resonance": PSI_RESONANCE,
    "alpha_adelic": ALPHA_ADELIC,
    "lambda_0_m2": LAMBDA_0,
    "kappa_pi": KAPPA_PI,
    "connected_repos": [
        "motanova84/Riemann-adelic  →  ceros γₙ como modos propios de H_QCAL",
        "motanova84/adelic-bsd      →  espectro adélico ancla f₀ y p=17",
        "motanova84/3D-Navier-Stokes →  ν_min QCAL limita dispersión p-ádica",
        "motanova84/Ramsey          →  κ_Π acota vibraciones de la red métrica",
        "motanova84/P-NP            →  κ_Π clasifica costo de incoherencia",
    ],
}
