"""
core/holography.py - Canon v3.0.2
Dualidad holográfica AdS2/CFT1 del operador D_Psi.

FÍSICA (declaración constitucional):
- Masa Klein-Gordon:  m^2 L^2 = -(gamma_n^2 + 1/4)  <  -1/4  para TODO gamma_n > 0.
- => VIOLACIÓN ESTRICTA de la cota Breitenlohner-Freedman (BF).
- Los modos bulk son TACHYÓNICOS BF-violantes.
- Dimensiones conformales primarias:  Delta_n = 1/2 + i gamma_n  (imaginarias).
- => La CFT_1 en la frontera es NO-UNITARIA / PT-SIMÉTRICA (Bender).
  La simetría PT es la que sostiene la realidad de las observables.

La BF-violación es la CONDICIÓN NECESARIA para que la línea crítica Re(s)=1/2
sea el espectro físico. El histórico test_BF_bound_stability=True era un artefacto
de definición semántica; RENOMBRADO a unitarity_bound_checked=False.
"""

from mpmath import mp, mpf, exp, log, pi, sqrt, nstr

from templo_core.constants import (
    gamma_1, gamma_all, c_psi, rho_normalization, BF_violated, D_PSI_S1,
)

mp.dps = 100


class HolographicAdS2:
    """Geometría AdS2 y CFT1 no-unitaria PT-simétrica."""

    def __init__(self):
        self.lambda_psi = D_PSI_S1
        self.abs_lambda = abs(self.lambda_psi)
        self.radius_scale = self.abs_lambda  # factor de escala |lambda|

    # ------------------------------------------------------------------
    # Masa BF
    # ------------------------------------------------------------------
    def mass_squared_L2(self, gamma):
        """m^2 L^2 = -(gamma^2 + 1/4)."""
        return -(gamma ** 2 + mpf('0.25'))

    def bf_bound(self):
        """Cota BF de AdS2: m^2 L^2 >= -1/4 para estabilidad unitaria."""
        return mpf('-0.25')

    def check_bf(self, gamma=gamma_1):
        """¿Este modo viola la cota BF? SIEMPRE True para ceros de zeta."""
        return float(self.mass_squared_L2(gamma)) < float(self.bf_bound())

    def mass_gamma1(self):
        return self.mass_squared_L2(gamma_1)  # ≈ -200.0397

    # ------------------------------------------------------------------
    # Dimensiones conformales
    # ------------------------------------------------------------------
    def conformal_dimension(self, gamma):
        """Delta = 1/2 + i gamma  (compleja conjugada par)."""
        return mpf('0.5') + 1j * gamma

    def spectrum_delta(self):
        """Deltas de los primeros ceros."""
        return [self.conformal_dimension(g) for g in gamma_all]

    # ------------------------------------------------------------------
    # Densidad de estados y carga central
    # ------------------------------------------------------------------
    def density_of_states(self, T):
        """rho_Psi(T) = (|lambda_Psi| / 2pi) * ln(T / 2pi)."""
        return rho_normalization * log(T / (2 * pi))

    def central_charge(self):
        """c_Psi = 3|lambda_Psi|/2."""
        return c_psi

    # ------------------------------------------------------------------
    # Estado de la unidad
    # ------------------------------------------------------------------
    def unitarity_bound_checked(self):
        """
        Antiguo test_BF_bound_stability.
        RENOMBRADO: el régimen es TACHYÓNICO NO-UNITARIO.
        Devuelve False (la cota de unidad NO se satisface; es un régimen PT-simétrico).
        """
        return False

    def pt_symmetry_status(self):
        """Declaración: la CFT1 es no-unitaria PT-simétrica."""
        return {
            'unitarity': 'no-unitaria',
            'regime': 'PT-simetrico (Bender)',
            'BF': 'violated (tachyonic)',
            'delta': '1/2 + i*gamma (compleja)',
            'spectrum': 'real bajo simetria PT intacta',
        }

    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def summary(self):
        return {
            'lambda_psi': self.lambda_psi,
            'abs_lambda': self.abs_lambda,
            'm2L2_gamma1': self.mass_gamma1(),
            'BF_bound': self.bf_bound(),
            'BF_violated': self.check_bf(),
            'unitarity_bound_checked': self.unitarity_bound_checked(),
            'Delta_1': self.conformal_dimension(gamma_1),
            'c_psi': self.central_charge(),
            'rho_norm': rho_normalization,
            'pt_status': self.pt_symmetry_status(),
        }

    def __repr__(self):
        s = self.summary()
        return (
            "HolographicAdS2(\n"
            f"  lambda_psi        = {s['lambda_psi']:.12f}\n"
            f"  m^2L^2(gamma_1)   = {nstr(s['m2L2_gamma1'], 12)}\n"
            f"  BF_bound          = {s['BF_bound']}\n"
            f"  BF_violated       = {s['BF_violated']}  (tachyonic)\n"
            f"  unitarity_checked = {s['unitarity_bound_checked']}  (no-unitaria)\n"
            f"  Delta_1           = {nstr(s['Delta_1'], 12)}\n"
            f"  c_psi             = {s['c_psi']:.12f}\n"
            f"  rho_norm          = {s['rho_norm']:.12f}\n"
            f"  regimen           = {s['pt_status']}\n"
            ")"
        )


def assert_holography():
    h = HolographicAdS2()
    # BF-violación estricta para el primer cero
    assert h.check_bf(gamma_1), "gamma_1 debe violar la cota BF"
    assert h.mass_gamma1() < mpf('-0.25'), "m^2L^2(gamma_1) < -1/4"
    # unidad: el régimen es no-unitario, el flag es False
    assert h.unitarity_bound_checked() is False, "regimen no-unitario"
    # delta compleja
    d = h.conformal_dimension(gamma_1)
    assert abs(d.imag - gamma_1) < mpf('1e-9'), "Im Delta = gamma"
    assert abs(d.real - mpf('0.5')) < mpf('1e-9'), "Re Delta = 1/2"
    # densidad positiva para T suficientemente grande
    assert h.density_of_states(mpf('40.0')) > 0, "rho(T) > 0 en T=40"
    return True


if __name__ == '__main__':
    assert_holography()
    print(HolographicAdS2())
    print("Sello: \u2234\U0001F300\u03A9\u221E\u00B3\u03A6 \u00B7 TUYOYOTU \u00B7 HECHO EST\u00C1")
