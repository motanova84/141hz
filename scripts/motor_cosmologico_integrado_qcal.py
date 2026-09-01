#!/usr/bin/env python3
"""
Motor Cuántico Cosmocéntrico Integrado QCAL

Integra los Axiomas del Pleroma ∴APQ∞³ con el Simulador de Wheeler-DeWitt
Adélico en un bucle de control activo con Kill-Switch de gauge.

El bucle principal avanza la evolución cosmológica si y sólo si la coherencia
global del Pleroma supera el umbral de activación (Ψ_Pleroma ≥ 0.888).
Si la coherencia cae, el interruptor congela el espacio de Hilbert e
interrumpe la propagación para conservar la invariancia de gauge.

Protocolo: QCAL-COSMO-MOTOR v1.0.0
"""

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from scipy.linalg import expm

# =====================================================================
# CONSTANTES CONFIGURACIONALES Y DE GAUGE (SI)
# =====================================================================
C_LUZ = 299792458.0
G_NEWTON = 6.67430e-11
HBAR_SI = 1.054571817e-34
H_PLANCK_SI = 2.0 * np.pi * HBAR_SI

F0_OBJETIVO = 141.7001
GAMMA_1_RIEMANN = 14.1347251417


# =====================================================================
# NÚCLEO ∴APQ∞³: AXIOMAS DEL PLEROMA QCAL
# =====================================================================
@dataclass(frozen=True)
class ConstantesAxiomasPleroma:
    f0: float = F0_OBJETIVO
    gamma1: float = GAMMA_1_RIEMANN
    c_luz: float = C_LUZ
    h_planck: float = H_PLANCK_SI
    hbar: float = HBAR_SI
    theta_torsion_ref: float = 3.00052
    primos: List[int] = field(default_factory=lambda: [2, 3, 5, 7, 11, 13])


@dataclass
class AtomoBlancoSaturado:
    entropia_pleroma: float = 0.0
    n_posibilidades: int = 1

    def calcular_psi1(self) -> float:
        if self.n_posibilidades <= 1:
            return 1.0
        log_n = math.log(float(self.n_posibilidades))
        return float(max(0.0, min(1.0, 1.0 - (self.entropia_pleroma / log_n))))


@dataclass
class MateriaBucle4Pi:
    theta_torsion_medido: float = 3.00052
    constantes: ConstantesAxiomasPleroma = field(
        default_factory=ConstantesAxiomasPleroma
    )

    def calcular_psi2(self) -> float:
        desviacion = abs(
            self.theta_torsion_medido - self.constantes.theta_torsion_ref
        )
        return float(math.exp(-desviacion))


@dataclass
class MantaAdelicaRiemann:
    intencion: float = 1.0
    a_eff: float = 1.0

    def calcular_psi3(self) -> float:
        return float(
            max(0.0, min(1.0, self.intencion))
            * (max(0.0, min(1.0, self.a_eff)) ** 2)
        )


@dataclass
class OperadorRiemannHubble:
    constantes: ConstantesAxiomasPleroma = field(
        default_factory=ConstantesAxiomasPleroma
    )
    r_gue_observado: float = 0.579

    def calcular_psi4(self) -> float:
        return float(max(0.0, 1.0 - abs(self.r_gue_observado - 0.579139)))


@dataclass
class InmortalidadDinamicaLuz:
    psi_inicial: float = 0.888
    alpha: float = 1.0
    t_evolucion: float = 0.007057
    constantes: ConstantesAxiomasPleroma = field(
        default_factory=ConstantesAxiomasPleroma
    )

    def calcular_psi5(self) -> float:
        if self.alpha <= 0.0:
            return 0.0
        omega = 2.0 * math.pi * self.constantes.f0
        factor_retorno = math.exp(
            -abs(math.sin(omega * self.t_evolucion / self.alpha))
        )
        return float(max(0.0, min(1.0, self.psi_inicial * factor_retorno)))


class CoherenciaAxiomasPleroma:

    def __init__(self, umbral: float = 0.888):
        self.umbral = umbral

    def calcular_global(self, valores_psi: List[float]) -> float:
        if not valores_psi or len(valores_psi) != 5:
            return 0.0
        producto = 1.0
        for psi in valores_psi:
            producto *= max(0.0, min(1.0, psi))
        return float(producto ** (1.0 / 5.0))


class SistemaAxiomasPleroma:

    def __init__(self):
        self.constantes = ConstantesAxiomasPleroma()
        self.agregador = CoherenciaAxiomasPleroma()

    def activar(self, intencion_dinamica: float = 1.0) -> Dict[str, Any]:
        psi1 = AtomoBlancoSaturado().calcular_psi1()
        psi2 = MateriaBucle4Pi(constantes=self.constantes).calcular_psi2()
        psi3 = MantaAdelicaRiemann(intencion=intencion_dinamica).calcular_psi3()
        psi4 = OperadorRiemannHubble(constantes=self.constantes).calcular_psi4()
        psi5 = InmortalidadDinamicaLuz(constantes=self.constantes).calcular_psi5()

        psi_global = self.agregador.calcular_global(
            [psi1, psi2, psi3, psi4, psi5]
        )
        return {
            "sello": "∴APQ∞³",
            "sello_activo": psi_global >= self.agregador.umbral,
            "psi_global": psi_global,
        }


def axiomas_pleroma_qcal_activar(
    intencion_dinamica: float = 1.0,
) -> Dict[str, Any]:
    return SistemaAxiomasPleroma().activar(intencion_dinamica)


# =====================================================================
# SIMULADOR COSMOLÓGICO WHEELER-DEWITT CON FILTRO DE GAUGE
# =====================================================================
class SimuladorWheelerDeWittAdelico:

    def __init__(self, primos_horizonte=None):
        if primos_horizonte is None:
            self.primos = [2, 3, 5, 7, 11, 13]
        else:
            self.primos = primos_horizonte

        self.N_spec = len(self.primos)
        self.dim_global = self.N_spec * 3
        self.l_planck = np.sqrt((HBAR_SI * G_NEWTON) / (C_LUZ**3))

    def generar_espectro_riemann_vladimirov(self, a_t: float) -> np.ndarray:
        H_base = np.zeros((self.N_spec, self.N_spec), dtype=np.complex128)
        omega_riemann = (GAMMA_1_RIEMANN * C_LUZ) / (2.0 * np.pi * a_t)

        for x in range(self.N_spec):
            for y in range(self.N_spec):
                if x == y:
                    H_base[x, y] = self.primos[x] * np.cos(
                        omega_riemann * 1e-18
                    )
                else:
                    diff = abs(x - y)
                    p_local = self.primos[x]
                    k = 0
                    while diff > 0 and diff % p_local == 0:
                        diff //= p_local
                        k += 1
                    val_p = float(p_local) ** (-k) if k > 0 else 1.0

                    H_base[x, y] = -(val_p**(-2.0)) * np.sin(
                        omega_riemann * 1e-18
                    )
                    H_base[x, x] += val_p**(-2.0)

        H_vlad = (H_base + H_base.conj().T) / 2.0
        eigvals = np.linalg.eigvalsh(H_vlad)
        gap = eigvals[-1] - eigvals[0]
        return H_vlad * (H_PLANCK_SI * F0_OBJETIVO / (gap + 1e-35))

    def trazo_parcial_horizonte(self, rho_global: np.ndarray) -> np.ndarray:
        rho_tensor = rho_global.reshape(self.N_spec, 3, self.N_spec, 3)
        return np.trace(rho_tensor, axis1=0, axis2=2)

    def evaluar_invariantes_cuanticos(self, rho_spin: np.ndarray):
        gamma = float(np.real(np.trace(rho_spin @ rho_spin)))
        autovals = np.real(np.linalg.eigvalsh(rho_spin))
        autovals = autovals[autovals > 1e-12]
        s_von = float(-np.sum(autovals * np.log2(autovals)))
        return gamma, s_von

    def resolver_emergencia_cosmologica(
        self, gamma: float, s_von: float
    ) -> float:
        factor_supresion = 3.0 * s_von * (1.0 - gamma) * (self.l_planck**2)
        a_0 = 1.37e26
        return (factor_supresion / (a_0**2)) * 1.57e104

    def acoplar_hamiltoniano_wheeler_dewitt(self, H_vlad, T_nu_cosmo, g_grav):
        H_spec_g = np.kron(H_vlad, np.eye(3, dtype=np.complex128))
        H_tors_g = np.kron(
            np.eye(self.N_spec, dtype=np.complex128),
            H_PLANCK_SI * F0_OBJETIVO * T_nu_cosmo,
        )
        H_int = g_grav * np.kron(H_vlad, T_nu_cosmo)
        return H_spec_g + H_tors_g + H_int


# =====================================================================
# BUCLE EN CALIENTE CON CONTROL DE APQ ACTIVO
# =====================================================================
if __name__ == "__main__":
    print("=== MOTOR COSMOLÓGICO INTEGRADO QCAL CON CONTROL DE GAUGE ===")
    simulador = SimuladorWheelerDeWittAdelico()

    psi_u = np.ones(
        (simulador.dim_global, 1), dtype=np.complex128
    ) / np.sqrt(simulador.dim_global)
    rho_universo = psi_u @ psi_u.conj().T

    a_t = 1.37e26
    dt = 1.0
    g_grav = 0.35

    # Simulación de decaimiento en el paso 4 para verificar el Kill-Switch
    intenciones_por_paso = [1.0, 1.0, 0.95, 0.92, 0.40]

    print(
        f"{'Paso':<6}{'Ψ_Pleroma':<14}{'Sello':<10}{'Pureza γ':<12}{'Λ (m^-2)':<16}{'Estado Operacional':<18}"
    )
    print("-" * 76)

    for paso in range(5):
        analisis_pleroma = axiomas_pleroma_qcal_activar(
            intencion_dinamica=intenciones_por_paso[paso]
        )
        psi_global = analisis_pleroma["psi_global"]
        sello_valido = (
            "VALIDO" if analisis_pleroma["sello_activo"] else "COLAPSO"
        )

        if not analisis_pleroma["sello_activo"]:
            print(
                f"{paso:<6}{psi_global:<14.4f}{sello_valido:<10}{'---':<12}{'---':<16}{'ABORTAR EVOLUCIÓN':<18}"
            )
            print(
                "\n[SISTEMA INTERRUMPIDO] El interruptor general congeló el espacio de Hilbert."
            )
            print(
                f"La coherencia del Pleroma cayó a {psi_global:.4f} (< 0.888). Conservación de gauge protegida."
            )
            break

        H_vlad = simulador.generar_espectro_riemann_vladimirov(a_t)
        rho_spin = simulador.trazo_parcial_horizonte(rho_universo)
        gamma, s_von = simulador.evaluar_invariantes_cuanticos(rho_spin)
        Lambda_t = simulador.resolver_emergencia_cosmologica(gamma, s_von)

        tau = np.tanh(s_von * (1.0 - gamma))
        T_nu_cosmo = np.array(
            [[1.0, 0.0, 0.0], [0.0, tau, 0.0], [0.0, 0.0, tau]],
            dtype=np.complex128,
        )

        H_total = simulador.acoplar_hamiltoniano_wheeler_dewitt(
            H_vlad, T_nu_cosmo, g_grav
        )

        energias = np.linalg.eigvalsh(H_total)
        gap_actual = energias[-1] - energias[0]
        H_total_exact = H_total * (
            (H_PLANCK_SI * F0_OBJETIVO) / (gap_actual + 1e-35)
        )

        print(
            f"{paso:<6}{psi_global:<14.4f}{sello_valido:<10}{gamma:<12.4f}{Lambda_t:<16.4e}{'SÍNCRONO (141.7 Hz)':<18}"
        )

        U = expm(-1j * dt * H_total_exact / HBAR_SI)
        rho_universo = U @ rho_universo @ U.conj().T
