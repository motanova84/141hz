"""
core/operator.py — Wrapper de compatibilidad del Operador DΨ (Canon v3.0.2)

Este módulo es un ENLACE FINO (thin wrapper) que re-exporta la capa espectral
implementada en core/riemann_spectral.py bajo la nomenclatura canónica del
ecosistema (DΨOperator, S_n_extended, C_asymptotic, cos_theta_B, D_Ψ_base).

NO duplica lógica: importa y re-expone. NO toca el canon 4D sellado
(ecuacion_resurreccion.py, KAPPA_THETA=19.061). Coexistencia de capas.
"""

import os
import importlib.util
from mpmath import mp

mp.dps = 100

# Carga directa de la capa espectral (repo_141hz no es paquete, sin __init__.py)
_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "riemann_spectral", os.path.join(_HERE, "riemann_spectral.py")
)
_rs = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_rs)

# ── Re-exportación de constantes ──
GAMMA_1 = _rs.GAMMA_1
GAMMA_2 = _rs.GAMMA_2
THETA_B = _rs.THETA_B
COS_THETA_B = _rs.COS_THETA_B
ZETA_DOUBLE_PRIME_HALF = _rs.ZETA_DOUBLE_PRIME_HALF
LAMBDA_0 = _rs.LAMBDA_0
F0 = _rs.F0
S_1 = _rs.S_1
S_FAMILY = _rs.S_FAMILY
C_ASYMPTOTIC = _rs.C_ASYMPTOTIC
SERIES_SUM_APPROX = _rs.SERIES_SUM_APPROX

# ── Aliases de compatibilidad con la nomenclatura del ecosistema ──
gamma_1 = GAMMA_1
gamma_2 = GAMMA_2
theta_B = THETA_B
cos_theta_B = COS_THETA_B
zeta_double_prime_half = ZETA_DOUBLE_PRIME_HALF
Lambda_0 = LAMBDA_0
f0 = F0
S_n_extended = S_FAMILY        # índice de estabilidad (n=1..19)
C_asymptotic = C_ASYMPTOTIC    # constante asintótica S_n ~ C/n²
D_Ψ_base = mp.mpf("-3.922646")  # valor base canónico (SABIO∞⁴, no modificado)


class DΨOperator(_rs.DPsiSpectral):
    """
    Operador D_Ψ (SABIO∞⁴) con fase viva de Berry — alias canónico.

    Hereda la implementación completa de DPsiSpectral (core/riemann_spectral.py).
    Modos: 'raw', 'S1' (canónico, exacto), 'series_finite', 'series_asymptotic'.
    """

    def __init__(self, damping_mode: str = "S1", **kwargs):
        super().__init__(damping_mode=damping_mode)
        # Métricas expuestas en la nomenclatura heredada (D_Ψ_phased, D_Ψ_base)
        self.D_Ψ_base = self.D_psi_base

    @property
    def D_Ψ_phased(self):
        """Valor D_Ψ,phased (depende del modo de amortiguación)."""
        return self.D_psi_phased

    def get_metrics(self):
        """Todas las métricas relevantes (idioma del ecosistema)."""
        m = super().get_metrics()
        m["D_Ψ_phased"] = m.pop("D_psi_phased")
        m["D_Ψ_base"] = m.pop("D_psi_base")
        return m

    def __repr__(self):
        return super().__repr__().replace("DPsiSpectral", "DΨOperator")


__all__ = [
    "DΨOperator",
    "gamma_1", "gamma_2", "theta_B", "cos_theta_B",
    "zeta_double_prime_half", "Lambda_0", "f0",
    "S_n_extended", "C_asymptotic", "D_Ψ_base",
    "GAMMA_1", "GAMMA_2", "THETA_B", "COS_THETA_B",
    "S_FAMILY", "S_1",
]

__version__ = "3.0.2"
__status__ = "wrapper de compatibilidad — coexiste con canon 4D"
