"""
Derivada Analítica ∂θ*/∂f₀ — Acoplamiento No Mínimo ζRΨ² y el Horizonte Acústico
==================================================================================

Formalización de la derivación explícita de la sensibilidad de la posición
angular del primer pico acústico del CMB, θ* = r_s(η*)/D_M(η*), respecto a la
frecuencia fundamental f₀ = 141,7001 Hz, bajo un acoplamiento no mínimo
ζ R |Ψ|² entre la curvatura y el condensado de coherencia Ψ (marco de Jordan).

Pipeline analítico implementado (ver docs/DERIVADA_THETA_STAR_F0.md):

1. Marco de Jordan → masa de Planck efectiva M_eff²(η) = M_pl² Ω²(η).
2. Tiempo conforme η* en recombinación (a* ≈ 1/1090) vía Friedmann estándar.
3. Dinámica homogénea del condensado χ(η), oscilando a ω₀ = 2π f₀, con
   desacoplamiento fijado por H(a_osc) = 2π f₀.
4. Horizonte de sonido r_s(η*, f₀) y distancia comóvil D_M(η*, f₀):
   se demuestra ∂D_M/∂f₀ ≈ 0, de modo que toda la sensibilidad recae en r_s.
5. Cálculo cerrado de ∂θ*/∂f₀ y de la derivada logarítmica adimensional
   |d ln θ*/d ln f₀|, evaluada con los parámetros de Planck 2018.
6. Veredicto: el acoplamiento perturbativo de fondo (ζ|Ψ|²/M_pl² ≪ 1) es
   insuficiente por >10 órdenes de magnitud para que Δf₀ = ±0,0012 Hz rompa
   3σ en Planck. El efecto observado, si existe, no puede ser una
   perturbación suave del fondo de Friedmann: debe ser una resonancia
   no adiabática de modos discretos (denominador divergente), no un
   δc_s distribuido en el plasma.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Licencia: MIT
"""

import math
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qcal.constants import F0_HZ, C  # noqa: E402

# ============================================================================
# PARÁMETROS COSMOLÓGICOS (Planck 2018, TT,TE,EE+lowE+lensing)
# ============================================================================

H0_KM_S_MPC: float = 67.4          # km/s/Mpc
MPC_TO_M: float = 3.0856775814913673e22  # m
H0_SI: float = H0_KM_S_MPC * 1.0e3 / MPC_TO_M  # s^-1  (≈ 2.184e-18 s^-1)

OMEGA_R0: float = 9.15e-5          # Densidad de radiación hoy
OMEGA_M0: float = 0.315            # Densidad de materia hoy
Z_STAR: float = 1090.0             # Redshift de recombinación
A_STAR: float = 1.0 / (1.0 + Z_STAR)  # ≈ 9.174e-4

R_S_MPC: float = 147.21            # Horizonte de sonido comóvil, Planck 2018
R_S_M: float = R_S_MPC * MPC_TO_M  # ≈ 4.542e24 m

DELTA_F0_HZ: float = 0.0012        # Desviación de frecuencia bajo escrutinio

# Umbral de ruptura de 3σ en θ* derivado de la sección observacional previa
LOG_DERIVATIVE_3SIGMA_THRESHOLD: float = 105.57


@dataclass(frozen=True)
class ResultadoDerivadaThetaStar:
    """Resultado numérico completo de la derivación ∂θ*/∂f₀."""

    prefactor_cinematico: float          # (4π H0 √Ω_r0)^{1/2}  [s^-1/2]
    f0_sqrt: float                       # f0^{1/2}             [s^-1/2]
    coeficiente_sensibilidad: float      # (f0/r_s)|∂r_s/∂f0| / (ζχ0²/Mpl²)
    zeta_chi0_sobre_mpl2_critico: float  # Umbral no perturbativo requerido
    log_derivative_perturbativo: float   # |d ln θ*/d ln f0| en régimen ζχ0²/Mpl² ~ 1
    ordenes_magnitud_insuficiente: float # log10(umbral requerido / régimen perturbativo)
    veredicto: str


def prefactor_cinematico(h0: float = H0_SI, omega_r0: float = OMEGA_R0) -> float:
    """(4π H0 √Ω_r0)^{1/2}, en s^-1/2."""
    return math.sqrt(4.0 * math.pi * h0 * math.sqrt(omega_r0))


def coeficiente_sensibilidad_logaritmica(
    f0: float = F0_HZ,
    r_s: float = R_S_M,
    h0: float = H0_SI,
    omega_r0: float = OMEGA_R0,
    c: float = C,
) -> float:
    """
    Calcula el coeficiente adimensional K tal que:

        |d ln θ*/d ln f0| = K · (ζ χ0² / M_pl²)

    donde:

        K = c / [√6 · r_s · (4π H0 √Ω_r0)^{1/2} · f0^{1/2}]

    proveniente de derivar el horizonte de sonido r_s(η*, f0) respecto de f0
    en el régimen dominado por radiación con corte infrarrojo físico en
    a_osc = (H0 √Ω_r0 / 2π f0)^{1/2} (inicio de la coherencia del condensado).
    """
    prefactor = prefactor_cinematico(h0, omega_r0)
    return c / (math.sqrt(6.0) * r_s * prefactor * math.sqrt(f0))


def zeta_chi0_sobre_mpl2_critico(
    threshold: float = LOG_DERIVATIVE_3SIGMA_THRESHOLD,
    f0: float = F0_HZ,
    r_s: float = R_S_M,
    h0: float = H0_SI,
    omega_r0: float = OMEGA_R0,
    c: float = C,
) -> float:
    """
    Despeja el acoplamiento no perturbativo ζχ0²/M_pl² requerido para que
    |d ln θ*/d ln f0| alcance el umbral de ruptura de 3σ de Planck.
    """
    k = coeficiente_sensibilidad_logaritmica(f0, r_s, h0, omega_r0, c)
    return threshold / k


def derivar_theta_star_f0(
    threshold: float = LOG_DERIVATIVE_3SIGMA_THRESHOLD,
    f0: float = F0_HZ,
    r_s: float = R_S_M,
    h0: float = H0_SI,
    omega_r0: float = OMEGA_R0,
    c: float = C,
    regimen_perturbativo_zeta_chi2_mpl2: float = 1.0,
) -> ResultadoDerivadaThetaStar:
    """
    Ejecuta la derivación analítica completa de ∂θ*/∂f0 y evalúa el veredicto
    físico: ¿puede un acoplamiento perturbativo de fondo (ζχ0²/Mpl² ≪ 1)
    justificar que Δf0 = ±0,0012 Hz rompa 3σ en Planck?
    """
    prefactor = prefactor_cinematico(h0, omega_r0)
    k = coeficiente_sensibilidad_logaritmica(f0, r_s, h0, omega_r0, c)
    zeta_critico = threshold / k

    log_derivative_perturbativo = k * regimen_perturbativo_zeta_chi2_mpl2
    ordenes_magnitud = math.log10(zeta_critico / regimen_perturbativo_zeta_chi2_mpl2)

    veredicto = (
        "INVIABLE EN REGIMEN PERTURBATIVO: se requiere zeta*chi0^2/Mpl^2 ~ "
        f"{zeta_critico:.3e} para alcanzar |d ln theta*/d ln f0| >= {threshold:.2f}, "
        "descartado por BBN y anisotropias CMB. "
        "El pliegue, si existe, debe formularse como resonancia no adiabatica "
        "de modos discretos (denominador divergente), no como perturbacion "
        "suave del fondo de Friedmann (dTheta*/df0 vía r_s, eta*)."
    )

    return ResultadoDerivadaThetaStar(
        prefactor_cinematico=prefactor,
        f0_sqrt=math.sqrt(f0),
        coeficiente_sensibilidad=k,
        zeta_chi0_sobre_mpl2_critico=zeta_critico,
        log_derivative_perturbativo=log_derivative_perturbativo,
        ordenes_magnitud_insuficiente=ordenes_magnitud,
        veredicto=veredicto,
    )


def a_osc(f0: float = F0_HZ, h0: float = H0_SI, omega_r0: float = OMEGA_R0) -> float:
    """Factor de escala de desacoplamiento del condensado: H(a_osc) = 2π f0."""
    return math.sqrt(h0 * math.sqrt(omega_r0) / (2.0 * math.pi * f0))


def delta_phi_1(
    delta_f0: float = DELTA_F0_HZ,
    f0: float = F0_HZ,
    q_hecke: float = 1.0,
) -> float:
    """Δφ₁ = π (Δf0/f0) Q_Hecke — desfase de la primera oscilación acústica."""
    return math.pi * (delta_f0 / f0) * q_hecke


if __name__ == "__main__":
    resultado = derivar_theta_star_f0()
    print("=" * 78)
    print("DERIVADA ANALITICA d(theta*)/d(f0) — ACOPLAMIENTO ZETA R |PSI|^2")
    print("=" * 78)
    print(f"Prefactor cinematico (4pi H0 sqrt(Omega_r0))^0.5 : "
          f"{resultado.prefactor_cinematico:.4e} s^-1/2")
    print(f"f0^0.5                                            : "
          f"{resultado.f0_sqrt:.4f} s^-1/2")
    print(f"Coeficiente K  |d ln theta*/d ln f0| = K*(zeta*chi0^2/Mpl^2) : "
          f"{resultado.coeficiente_sensibilidad:.4e}")
    print(f"zeta*chi0^2/Mpl^2 critico (3-sigma Planck)        : "
          f"{resultado.zeta_chi0_sobre_mpl2_critico:.4e}")
    print(f"Ordenes de magnitud de insuficiencia perturbativa : "
          f"{resultado.ordenes_magnitud_insuficiente:.2f}")
    print(f"a_osc (desacople del condensado a f0={F0_HZ} Hz)  : {a_osc():.4e}")
    print(f"Delta_phi_1 (Delta_f0={DELTA_F0_HZ} Hz, Q_Hecke=1) : {delta_phi_1():.4e} rad")
    print("-" * 78)
    print(resultado.veredicto)
