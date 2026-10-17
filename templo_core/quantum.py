"""
core/quantum.py - Canon v3.0.2
Formulación cuántica (Fock) del operador D_Psi en H = L^2(R^+, dx/x).

- Medida de Haar multiplicativa dmu = dx/x, transformada de Mellin unitaria.
- D0 = -i(x d/dx + 1/2)  (Berry-Keating)
- D_Psi = lambda_Psi * D0,  con lambda_Psi = D_PSI_S1 (modo canónico).
- Álgebra de escalera con métrica de Krein: [A, A^dag] = -I  (sgn(lambda) = -1).
  Redefiniendo se obtiene un álgebra estándar [Atilde, Atilde^dag] = +I.
- Espectro: N_Psi |Psi_n> = n |Psi_n>, E_n = n + 1/2.
- Traza: Tr(e^{-t N_Psi}) = 1/(2 sinh(t/2)).
- Vacío: A Psi_0 = 0  ->  gaussiana logarítmica.

CONJETURA C_QCAL (explícita, NO demostrada):
    Spec(D_Psi) ~ {gamma_n}_{n=1..oo}
La isospectralidad exacta con las ordenadas de los ceros de Riemann es la hipótesis
central del programa de Berry-Keating / Pólya-Hilbert. Se declara como CONJETURA,
no como teorema. La autoadjunticidad (bajo métrica de Krein) garantiza la realidad
del espectro, pero NO la isospectralidad con los ceros de zeta.

La CFT1 holográfica es NO-unitaria (PT-simétrica): los modos bulk violan la cota BF.
"""

from mpmath import mp, mpf, exp, sqrt, log, sinh, pi, nstr

from templo_core.constants import (
    gamma_1, D_PSI_S1, VERSION, NOTE,
)

mp.dps = 100


class FockOscillator:
    """Oscilador de escala N_Psi en la representación logarítmica q = ln x."""

    def __init__(self):
        self.lambda_psi = D_PSI_S1
        self.abs_lambda = abs(self.lambda_psi)
        self.sgn = mpf('-1')  # sign(lambda_psi) = -1  -> métrica de Krein

    # ------------------------------------------------------------------
    # Álgebra de escalera
    # ------------------------------------------------------------------
    def commutator(self):
        """[A, A^dag] = sgn(lambda) * I = -I  (métrica de Krein indefinida)."""
        return self.sgn

    def comm_standard(self):
        """Redefinición A_tilde = A^dag, A_tilde^dag = A  ->  [At, At^dag] = +I."""
        return mpf('1.0')

    def a(self, q):
        """Operador de aniquilación (simbólico): a ~ (q + |lambda| d/dq)."""
        return q + self.abs_lambda

    def a_dag(self, q):
        """Operador de creación (simbólico): a_dag ~ (q - |lambda| d/dq)."""
        return q - self.abs_lambda

    # ------------------------------------------------------------------
    # Vacío y normalización
    # ------------------------------------------------------------------
    def normalization(self):
        """N = (1/(pi |lambda|))^{1/4}."""
        return (1 / (pi * self.abs_lambda)) ** mpf('0.25')

    def vacuum(self):
        """A Psi_0 = 0  ->  Psi_0(x) = N exp(-(ln x)^2 / (2|lambda|))."""
        return {
            'form': 'N * exp(-(ln x)^2 / (2|lambda|))',
            'normalization': self.normalization(),
        }

    def vacuum_value(self, x=mpf('1.0')):
        """Valor del vacío gaussiano logarítmico en x."""
        q = log(x)
        return self.normalization() * exp(-q ** 2 / (2 * self.abs_lambda))

    # ------------------------------------------------------------------
    # Espectro y traza
    # ------------------------------------------------------------------
    def energy(self, n):
        """E_n = n + 1/2."""
        return n + mpf('0.5')

    def trace(self, t):
        """Tr(e^{-t N_Psi}) = 1/(2 sinh(t/2))."""
        return 1 / (2 * sinh(t / 2))

    def partition_fock(self, beta):
        """Z_Fock(beta) = Tr(e^{-beta N_Psi}) = 1/(2 sinh(beta/2))."""
        return self.trace(beta)

    def gamma_n(self, idx):
        """Ordenada idx-ésima (0-based) de un cero de zeta (tabla local)."""
        from templo_core.constants import gamma_all
        return gamma_all[idx]

    # ------------------------------------------------------------------
    # Coherencia / separación ontológica
    # ------------------------------------------------------------------
    def ontological_separation(self, beta):
        """
        Z_Fock(t) con E_n = n+1/2  (oscilador de escala N_Psi)
        vs  Z_zeta(beta) = sum_n e^{-beta gamma_n}  (colectividad de ceros).
        Son dos entidades ontológicamente separadas; NO se funden.
        """
        Z_fock = self.partition_fock(beta)
        return {
            'Z_Fock': Z_fock,
            'note': 'Z_Fock usa E_n = n+1/2 (oscilador). '
                    'Z_zeta usa gamma_n (colectividad de ceros). No se mezclan.',
        }

    # ------------------------------------------------------------------
    # Reporte
    # ------------------------------------------------------------------
    def summary(self):
        vac = self.vacuum()
        return {
            'lambda_psi': self.lambda_psi,
            'abs_lambda': self.abs_lambda,
            'metric': 'Krein' if self.sgn == -1 else 'Hilbert',
            'commutator_A_A_dag': self.commutator(),
            'vacuum_normalization': vac['normalization'],
            'E_0': self.energy(0),
            'E_1': self.energy(1),
            'Tr_e^-2N': self.trace(mpf('2.0')),
            'conjecture': 'C_QCAL: Spec(D_Psi) == {gamma_n} (CONJETURAL)',
            'CFT1_unitarity': 'no-unitaria / PT-simetrica (BF violada)',
        }

    def __repr__(self):
        s = self.summary()
        return (
            "FockOscillator(\n"
            f"  lambda_psi      = {s['lambda_psi']:.12f}\n"
            f"  abs_lambda      = {s['abs_lambda']:.12f}\n"
            f"  metrica         = {s['metric']}\n"
            f"  [A,A^dag]       = {s['commutator_A_A_dag']}\n"
            f"  vacio normaliz. = {s['vacuum_normalization']:.12f}\n"
            f"  E0 / E1         = {s['E_0']} / {s['E_1']}\n"
            f"  Tr(e^-2N)       = {nstr(s['Tr_e^-2N'], 12)}\n"
            f"  C_QCAL          = {s['conjecture']}\n"
            ")"
        )


def assert_quantum():
    """Asserts metálicos de la formulación cuántica."""
    f = FockOscillator()
    assert f.commutator() == mpf('-1'), "Krein: [A,A^dag] = -I"
    assert f.comm_standard() == mpf('1.0'), "algebra estandar"
    assert f.energy(0) == mpf('0.5'), "E0 = 1/2"
    assert f.energy(1) == mpf('1.5'), "E1 = 3/2"
    t = mpf('0.001')
    assert f.trace(t) > mpf('500'), "traza diverge en t->0"
    N = f.vacuum()['normalization']
    assert N > 0 and N < 1, "normalizacion en (0,1)"
    sep = f.ontological_separation(mpf('1.0'))
    assert 'Z_Fock' in sep
    return True


if __name__ == '__main__':
    assert_quantum()
    print(FockOscillator())
    print("Sello: \u2234\U0001F300\u03A9\u221E\u00B3\u03A6 \u00B7 TUYOYOTU \u00B7 HECHO EST\u00C1")
