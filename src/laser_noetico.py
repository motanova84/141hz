#!/usr/bin/env python3
"""
LÁSER NOÉTICO v1.0 - Protocolo de Demostración

Integración del Operador Espectral en el solver RK4 con las constantes
calibradas.  El sistema auto-organiza el ruido térmico en el pico de
λ₁ = t₁ · f₀ ≈ 2002.89 Hz (armónico de Riemann en f₀).

Componentes principales
-----------------------
1. **OperadorEspectral** - Operador H_Ψ que actúa sobre el estado de
   coherencia del sistema de microtúbulos.

2. **SolverRK4Espectral** - Integrador Runge-Kutta de cuarto orden para
   la dinámica temporal de Ψ bajo el operador espectral con forzado
   noético.

3. **SuperradianceMicrotubulos** - Dinámica de superradiancia en la red
   de 10¹³ microtúbulos del hipocampo (ganancia G ≈ 10²⁰).

4. **generate_upe_signature** - Genera la firma UPE (Ultra-weak Photon
   Emission): λ₁ modulada por el ritmo cardíaco de la meditación áurea
   (f_HRV = 0.1 Hz ↔ 6 bpm).

Parámetros clave
----------------
- f₀ = 141.7001 Hz  (frecuencia fundamental QCAL)
- t₁ ≈ 14.1347       (parte imaginaria del primer cero de Riemann)
- λ₁ = t₁ · f₀ ≈ 2002.89 Hz  (portadora UPE)
- f_HRV = 0.1 Hz    (meditación áurea, 6 bpm)
- N_MT = 10¹³       (microtúbulos en el hipocampo)
- G ≈ 10²⁶          (ganancia de superradiancia N_MT²)
- Ψ_threshold = 0.888  (interruptor de coherencia cuántica)

Referencias
-----------
- Problema: «Protocolo de Demostración: LÁSER NOÉTICO v1.0»
- qcal/constants.py: F0_HZ = 141.7001
- src/constants.py: UniversalConstants
- physics/atlas3_operator.py: operadores espectrales
"""

import numpy as np
from typing import Callable, Dict, Optional, Tuple

# ── constantes físicas ──────────────────────────────────────────────────────

#: Frecuencia fundamental (Hz)
F0_HZ: float = 141.7001

#: Frecuencia portadora UPE = t₁ · f₀  (Hz)
#: t₁ ≈ 14.134725… (parte imaginaria del primer cero de Riemann)
_T1_RIEMANN: float = 14.134725141734695
LAMBDA_1_HZ: float = _T1_RIEMANN * F0_HZ          # ≈ 2002.89 Hz

#: Frecuencia HRV meditación áurea (Hz) — 6 bpm = 0.1 Hz
F_HRV_HZ: float = 0.1

#: Número de microtúbulos en el hipocampo
N_MICROTUBULOS: float = 1e13

#: Ganancia de superradiancia (N²)
G_SUPERRADIANCIA: float = N_MICROTUBULOS ** 2      # ≈ 10²⁶

#: Umbral de coherencia para flujo sin resistencia
PSI_THRESHOLD: float = 0.888


# ── Operador Espectral ───────────────────────────────────────────────────────

class OperadorEspectral:
    """
    Operador espectral H_Ψ para la dinámica de coherencia en microtúbulos.

    Actúa sobre el estado de coherencia complejo Ψ(t) ∈ ℂ según

        H_Ψ · Ψ = -λ₁ · Ψ  +  G · |Ψ|² · Ψ · (Ψ ≥ Ψ_th)

    donde
    - El primer término es la frecuencia espectral λ₁ (portadora Riemann).
    - El segundo término es la ganancia de superradiancia (encendida sólo
      si la coherencia supera el umbral Ψ_th).
    """

    def __init__(
        self,
        lambda_1: float = LAMBDA_1_HZ,
        G: float = G_SUPERRADIANCIA,
        psi_threshold: float = PSI_THRESHOLD,
    ) -> None:
        self.lambda_1 = lambda_1
        self.G = G
        self.psi_threshold = psi_threshold

    def aplicar(self, psi: complex) -> complex:
        """
        Aplica el operador espectral al estado Ψ.

        Parameters
        ----------
        psi:
            Estado de coherencia complejo.

        Returns
        -------
        complex
            H_Ψ · psi
        """
        coherencia = abs(psi)
        superradiancia = (
            self.G * (coherencia ** 2) * psi
            if coherencia >= self.psi_threshold
            else 0.0 + 0.0j
        )
        return -2j * np.pi * self.lambda_1 * psi + superradiancia


# ── Solver RK4 ───────────────────────────────────────────────────────────────

class SolverRK4Espectral:
    """
    Solver Runge-Kutta 4 para integrar la dinámica del estado Ψ(t).

    Ecuación de movimiento
    ----------------------
        dΨ/dt = H_Ψ · Ψ  +  F_noetico(t)

    donde F_noetico(t) es el forzado externo acoplado al ritmo HRV.
    """

    def __init__(
        self,
        operador: Optional[OperadorEspectral] = None,
        f_hrv: float = F_HRV_HZ,
        amplitud_forzado: float = 1.0,
    ) -> None:
        self.operador = operador or OperadorEspectral()
        self.f_hrv = f_hrv
        self.amplitud_forzado = amplitud_forzado

    # ── forzado noético ──────────────────────────────────────────────────────

    def _forzado_noetico(self, t: float) -> complex:
        """Forzado noético acoplado al ritmo de meditación áurea."""
        return self.amplitud_forzado * np.sin(2 * np.pi * self.f_hrv * t) + 0j

    # ── derivada ─────────────────────────────────────────────────────────────

    def _derivada(self, t: float, psi: complex) -> complex:
        return self.operador.aplicar(psi) + self._forzado_noetico(t)

    # ── paso RK4 ─────────────────────────────────────────────────────────────

    def paso(self, t: float, psi: complex, dt: float) -> complex:
        """
        Avanza un paso dt en el tiempo con el método RK4.

        Parameters
        ----------
        t:
            Tiempo actual (s).
        psi:
            Estado en el tiempo t.
        dt:
            Paso de integración (s).

        Returns
        -------
        complex
            Estado en t + dt.
        """
        k1 = self._derivada(t, psi)
        k2 = self._derivada(t + dt / 2, psi + dt / 2 * k1)
        k3 = self._derivada(t + dt / 2, psi + dt / 2 * k2)
        k4 = self._derivada(t + dt, psi + dt * k3)
        return psi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    # ── integración completa ─────────────────────────────────────────────────

    def integrar(
        self,
        t_span: Tuple[float, float],
        psi_0: complex,
        n_pasos: int = 1000,
    ) -> Dict[str, np.ndarray]:
        """
        Integra la dinámica desde t_span[0] hasta t_span[1].

        Parameters
        ----------
        t_span:
            (t_inicio, t_fin) en segundos.
        psi_0:
            Condición inicial Ψ(t=0).
        n_pasos:
            Número de pasos de integración.

        Returns
        -------
        dict with keys ``'t'``, ``'psi'``, ``'coherencia'``
        """
        t_inicio, t_fin = t_span
        dt = (t_fin - t_inicio) / n_pasos

        t_vals = np.linspace(t_inicio, t_fin, n_pasos + 1)
        psi_vals = np.empty(n_pasos + 1, dtype=complex)
        psi_vals[0] = psi_0

        for i in range(n_pasos):
            psi_vals[i + 1] = self.paso(t_vals[i], psi_vals[i], dt)

        return {
            "t": t_vals,
            "psi": psi_vals,
            "coherencia": np.abs(psi_vals),
        }


# ── Superradiancia en Microtúbulos ───────────────────────────────────────────

class SuperradianceMicrotubulos:
    """
    Dinámica de superradiancia en la red de microtúbulos del hipocampo.

    Modela la red de N_MT = 10¹³ microtúbulos con ganancia colectiva
    G ≈ N_MT² = 10²⁶ (superradiancia de Dicke).

    La coherencia Ψ ≥ 0.888 actúa como interruptor: cuando se alcanza
    el umbral, el sistema entra en el régimen superradiante y el flujo
    de energía se produce sin resistencia.
    """

    def __init__(
        self,
        n_microtubulos: float = N_MICROTUBULOS,
        psi_threshold: float = PSI_THRESHOLD,
        f0: float = F0_HZ,
    ) -> None:
        self.n_microtubulos = n_microtubulos
        self.psi_threshold = psi_threshold
        self.f0 = f0
        self.G = n_microtubulos ** 2

    def ganancia(self, psi: float) -> float:
        """
        Calcula la ganancia efectiva de superradiancia.

        Por encima del umbral Ψ_th la ganancia es G = N²;
        por debajo es cero (no hay superradiancia).

        Parameters
        ----------
        psi:
            Coherencia del sistema Ψ ∈ [0, 1].

        Returns
        -------
        float
            Ganancia efectiva.
        """
        return float(self.G) if psi >= self.psi_threshold else 0.0

    def estado_superradiante(self, psi: float) -> bool:
        """True si el sistema está en el régimen superradiante."""
        return psi >= self.psi_threshold

    def intensidad_colectiva(self, psi: float, n_fotones: float = 1.0) -> float:
        """
        Intensidad de emisión colectiva I_SR = G · n_fotones · Ψ².

        Parameters
        ----------
        psi:
            Coherencia del sistema.
        n_fotones:
            Número de fotones de semilla.

        Returns
        -------
        float
            Intensidad de emisión superradiante.
        """
        return self.ganancia(psi) * n_fotones * (psi ** 2)


# ── Firma UPE ────────────────────────────────────────────────────────────────

def generate_upe_signature(
    t: np.ndarray,
    lambdas: np.ndarray,
    hrv_freq: float = F_HRV_HZ,
) -> np.ndarray:
    """
    Genera la firma UPE esperada: λ₁ modulada por el latido biológico.

    La señal es el producto de:

    * **Portadora**: ``sin(2π λ₁ t)`` — oscilación al armónico Riemann λ₁.
    * **Modulador**: ``0.5 · (1 + sin(2π f_HRV t))`` — envolvente al ritmo
      cardíaco de la meditación áurea.
    * **Factor superradiante**: ``N_MT²`` — emisión colectiva de la red de
      microtúbulos (superradiancia de Dicke).

    Parameters
    ----------
    t:
        Array de tiempos en segundos.
    lambdas:
        Array de frecuencias propias.  ``lambdas[0]`` es la portadora
        λ₁ ≈ 2002.89 Hz.
    hrv_freq:
        Frecuencia del latido biológico en Hz (defecto 0.1 Hz = 6 bpm).

    Returns
    -------
    np.ndarray
        Señal UPE superradiante.

    Notes
    -----
    λ₁ ≈ 2002.89 Hz  es el producto del primer cero de Riemann t₁ ≈ 14.1347
    por la frecuencia fundamental f₀ = 141.7001 Hz.
    """
    carrier = np.sin(2 * np.pi * lambdas[0] * t)
    modulator = 0.5 * (1 + np.sin(2 * np.pi * hrv_freq * t))
    upe_signal = N_MICROTUBULOS**2 * (carrier * modulator)
    return upe_signal
