"""
core/blackhole_entropy.py - Canon v3.0.2
Termodinámica de agujeros negros y su corrección por gravedad cuántica de lazos (LQG).

- Área cuantizada:  A_n = 8*pi*gamma_LQG * l_Pl^2 * (n + 1/2)   (gamma_LQG = 0.2375, Barbero-Immirzi)
- Entropía Bekenstein-Hawking:  S_BH = A / (4 G_N)
- Correcciones:  S(A) = S_BH - (3/2) log(A/(4 G_N)) + sum_n exp(-gamma_n * A / (4 G_N))

Las correcciones logarítmicas y exponenciales (Riemann) emergen de la estructura
espectral del operador D_Psi. La relación holográfica S = (2*pi^2/3) c_Psi * T.
"""

from mpmath import mp, mpf, exp, log, pi, sqrt, nstr

from templo_core.constants import (
    gamma_all, D_PSI_S1, c_psi,
)

mp.dps = 100

# ---------- constantes físicas (natural units, l_Pl = G_N = 1 por defecto) ----------
G_N_DEFAULT = mpf('1.0')          # unidades naturales
l_Pl2_DEFAULT = mpf('1.0')        # l_Pl^2 en unidades naturales
gamma_LQG = mpf('0.2375')         # parámetro Barbero-Immirzi


class BlackHoleEntropy:
    """Entropía de agujero negro con correcciones LQG y de Riemann."""

    def __init__(self, G_N=G_N_DEFAULT, l_Pl2=l_Pl2_DEFAULT):
        self.G_N = G_N
        self.l_Pl2 = l_Pl2
        self.lambda_psi = D_PSI_S1
        self.abs_lambda = abs(self.lambda_psi)
        self.c_psi = c_psi

    # ------------------------------------------------------------------
    # Área cuantizada (LQG)
    # ------------------------------------------------------------------
    def area_n(self, n):
        """A_n = 8*pi*gamma_LQG * l_Pl^2 * (n + 1/2)."""
        return 8 * pi * gamma_LQG * self.l_Pl2 * (n + mpf('0.5'))

    def area_spectrum(self, N=10):
        """Primeros N niveles de área."""
        return [self.area_n(n) for n in range(N)]

    # ------------------------------------------------------------------
    # Entropía
    # ------------------------------------------------------------------
    def bekenstein_hawking(self, A):
        """S_BH = A / (4 G_N)."""
        A = mpf(A)
        return A / (4 * self.G_N)

    def log_correction(self, A):
        """-(3/2) log(A/(4 G_N))."""
        A = mpf(A)
        return -mpf('1.5') * log(A / (4 * self.G_N))

    def riemann_correction(self, A, n_terms=5):
        """sum_{k} exp(-gamma_k * A / (4 G_N)) — corrección de Riemann."""
        A = mpf(A)
        s = mpf('0.0')
        for k in range(min(n_terms, len(gamma_all))):
            s += exp(-gamma_all[k] * A / (4 * self.G_N))
        return s

    def entropy_total(self, A, n_terms=5):
        """S(A) = S_BH + corrección logs + corrección Riemann."""
        return (
            self.bekenstein_hawking(A)
            + self.log_correction(A)
            + self.riemann_correction(A, n_terms)
        )

    # ------------------------------------------------------------------
    # Relación holográfica
    # ------------------------------------------------------------------
    def holographic_entropy(self, T):
        """S = (2*pi^2/3) * c_Psi * T."""
        return (2 * pi ** 2 / 3) * self.c_psi * T

    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def summary(self, A=mpf('10.0')):
        A = mpf(A)
        return {
            'area_0': self.area_n(0),
            'area_1': self.area_n(1),
            'S_BH(10)': self.bekenstein_hawking(A),
            'log_corr(10)': self.log_correction(A),
            'riemann_corr(10)': self.riemann_correction(A),
            'S_total(10)': self.entropy_total(A),
            'gamma_LQG': gamma_LQG,
        }

    def __repr__(self):
        s = self.summary()
        return (
            "BlackHoleEntropy(\n"
            f"  gamma_LQG   = {gamma_LQG}\n"
            f"  A_0         = {nstr(s['area_0'], 12)}\n"
            f"  A_1         = {nstr(s['area_1'], 12)}\n"
            f"  S_BH(10)    = {nstr(s['S_BH(10)'], 12)}\n"
            f"  log_corr    = {nstr(s['log_corr(10)'], 12)}\n"
            f"  riemann_corr= {nstr(s['riemann_corr(10)'], 12)}\n"
            f"  S_total(10) = {nstr(s['S_total(10)'], 12)}\n"
            ")"
        )


def assert_entropy():
    bh = BlackHoleEntropy()
    A = mpf('10.0')
    # entropías positivas
    assert bh.bekenstein_hawking(A) > 0, "S_BH > 0"
    assert bh.area_n(0) > 0, "A_0 > 0"
    # escalamiento de área con n
    assert bh.area_n(1) > bh.area_n(0), "A_1 > A_0"
    # corrección log: negativa (reducción)
    assert bh.log_correction(A) < 0, "correccion log negativa"
    # corrección Riemann: positiva y decreciente con A
    assert bh.riemann_correction(A) > 0, "correccion riemann positiva"
    assert bh.riemann_correction(mpf('100.0')) < bh.riemann_correction(mpf('10.0')), "decae con A"
    # entropía holográfica crece con T
    assert bh.holographic_entropy(mpf('2.0')) > bh.holographic_entropy(mpf('1.0')), "S holografica crece"
    return True


if __name__ == '__main__':
    assert_entropy()
    print(BlackHoleEntropy())
    print("Sello: \u2234\U0001F300\u03A9\u221E\u00B3\u03A6 \u00B7 TUYOYOTU \u00B7 HECHO EST\u00C1")
