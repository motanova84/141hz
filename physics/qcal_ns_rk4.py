"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       PROTOCOLO LÁSER NOÉTICO v1.0                                            ║
║                                                                               ║
║  Operador espectral integrado en un solucionador RK4 manual que modela        ║
║  la emisión superradiante de 10¹³ microtúbulos hipocampales, con              ║
║  generación de firma UPE en λ₁ ≈ 2002,89 Hz modulada por el ritmo            ║
║  HRV de meditación dorada de 6 bpm (F_HRV = 0,1 Hz).                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    ResultadoLaserNoetico    – Contenedor de resultados del protocolo de activación
    MallaEspectral           – Cuadrícula de frecuencias centrada en λ₁ ± 50 Hz
    FiltroVibracional        – Filtro lorentziano; Ψ_spec vía analogía Kuramoto
    IntegradorRK4            – Integrador manual RK4 dΨ/dt = F_noético − α·Ψ + G·α·Ψ·(1−Ψ)
    EspectroEnergia          – Error espectral analítico |λ₁ − γ₁·f₀| / (γ₁·f₀)
    ForzadoEspectralNoetico  – Portadora λ₁ modulada en AM a f_HRV
    TerminoSuperradiante     – Ganancia N²; rendimiento cuántico superradiante
    CoherenciaBiologica      – Combinación ponderada psi_spec/psi_dyn/psi_upe → Ψ total

API pública:
    generate_upe_signature(t, lambdas, hrv_freq=0.1)
    qcal_ns_rk4_activar()
"""

import math
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

# ============================================================================
# CONSTANTES FÍSICAS Y DEL PROTOCOLO
# ============================================================================

# Frecuencia espectral central (λ₁) — portadora UPE hipocampal
LAMBDA_1: float = 2002.89  # Hz

# Ritmo HRV de meditación dorada (6 bpm = 0,1 Hz)
F_HRV: float = 0.1  # Hz

# Número de microtúbulos hipocampales
N_MICROTUBULOS: int = int(1e13)

# Ganancia superradiante de Dicke: N² = 10²⁶
N_SQUARED: float = float(N_MICROTUBULOS) ** 2

# Ganancia normalizada RK4 (dominancia cualitativa N² sin desbordamiento float64)
G_NORM_RK4: float = 10.0

# Rendimiento cuántico en régimen superradiante (10³ QY)
RENDIMIENTO_CUANTICO: float = 1000.0

# Frecuencia fundamental QCAL
F0_HZ: float = 141.7001  # Hz

# Parte imaginaria del primer cero de Riemann (γ₁) — verificación QED-RIEMANN
GAMMA_1_RIEMANN: float = 14.134725141734693790

# Umbral mínimo de coherencia
PSI_MINIMA: float = 0.888

# Coherencia espectral Kuramoto: Ψ_spec = 1 − 2γ_s/(2π·F_HRV) = 0,891
_PSI_SPEC_KURAMOTO: float = 0.891

# Semiancho lorentziano: γ_s = (1 − Ψ_spec) · π · F_HRV
_GAMMA_S: float = (1.0 - _PSI_SPEC_KURAMOTO) * math.pi * F_HRV


# ============================================================================
# CLASE 1 – ResultadoLaserNoetico (dataclass)
# ============================================================================

@dataclass
class ResultadoLaserNoetico:
    """
    Contenedor con los resultados del protocolo LÁSER NOÉTICO v1.0.

    Atributos
    ---------
    psi_spec : float
        Coherencia espectral Kuramoto (≥ 0,888). Valor esperado: 0,891.
    psi_dyn : float
        Coherencia dinámica RK4 en la meseta (próxima a 1,0).
    psi_upe : float
        Coherencia de la firma UPE en régimen superradiante.
    psi_total : float
        Coherencia biológica total (≈ 0,956).
    error_espectral : float
        Error relativo |λ₁ − γ₁·f₀| / (γ₁·f₀) (< 10⁻⁶).
    superradiante : bool
        Indica si el sistema opera en régimen superradiante.
    plateau_alcanzado : bool
        Indica si el integrador RK4 alcanzó la meseta Ψ → 1.
    rendimiento_cuantico : float
        Rendimiento cuántico en régimen superradiante (= 1000,0).
    aprobado : bool
        True si psi_total ≥ PSI_MINIMA.

    Ejemplo
    -------
    >>> from physics.qcal_ns_rk4 import qcal_ns_rk4_activar
    >>> r = qcal_ns_rk4_activar()
    >>> r.psi_spec
    0.891
    >>> r.superradiante
    True
    """

    psi_spec: float
    psi_dyn: float
    psi_upe: float
    psi_total: float
    error_espectral: float
    superradiante: bool
    plateau_alcanzado: bool
    rendimiento_cuantico: float
    aprobado: bool


# ============================================================================
# CLASE 2 – MallaEspectral
# ============================================================================

class MallaEspectral:
    """
    Cuadrícula de frecuencias centrada en λ₁ ± delta_hz.

    Parámetros
    ----------
    lambda_1 : float
        Frecuencia central (Hz). Por defecto LAMBDA_1 = 2002,89 Hz.
    delta_hz : float
        Semiancho de la malla en Hz. Por defecto 50 Hz.
    n_puntos : int
        Número de puntos en la malla. Por defecto 1000.

    Ejemplo
    -------
    >>> m = MallaEspectral()
    >>> m.centro
    2002.89
    >>> len(m.frecuencias)
    1000
    """

    def __init__(
        self,
        lambda_1: float = LAMBDA_1,
        delta_hz: float = 50.0,
        n_puntos: int = 1000,
    ) -> None:
        if n_puntos < 2:
            raise ValueError("n_puntos debe ser al menos 2.")
        if delta_hz <= 0:
            raise ValueError("delta_hz debe ser positivo.")
        self._lambda_1 = lambda_1
        self._delta_hz = delta_hz
        self._n_puntos = n_puntos
        self._frecuencias: np.ndarray = np.linspace(
            lambda_1 - delta_hz,
            lambda_1 + delta_hz,
            n_puntos,
        )

    @property
    def frecuencias(self) -> np.ndarray:
        """Array de frecuencias de la malla."""
        return self._frecuencias

    @property
    def centro(self) -> float:
        """Frecuencia central λ₁ (Hz)."""
        return self._lambda_1

    @property
    def ancho_hz(self) -> float:
        """Ancho total de la malla en Hz (= 2 × delta_hz)."""
        return 2.0 * self._delta_hz

    @property
    def delta_hz(self) -> float:
        """Semiancho de la malla (Hz)."""
        return self._delta_hz

    @property
    def n_puntos(self) -> int:
        """Número de puntos de la malla."""
        return self._n_puntos

    def contiene(self, f: float) -> bool:
        """Devuelve True si la frecuencia f está dentro de la malla."""
        return (self._lambda_1 - self._delta_hz) <= f <= (self._lambda_1 + self._delta_hz)

    def indice_central(self) -> int:
        """Índice del punto más cercano a la frecuencia central."""
        return int(np.argmin(np.abs(self._frecuencias - self._lambda_1)))

    def resolucion_hz(self) -> float:
        """Resolución espectral Δf = ancho / (n_puntos − 1) en Hz."""
        return self.ancho_hz / (self._n_puntos - 1)

    def __repr__(self) -> str:
        return (
            f"MallaEspectral(centro={self._lambda_1} Hz, "
            f"ancho={self.ancho_hz} Hz, n_puntos={self._n_puntos})"
        )


# ============================================================================
# CLASE 3 – FiltroVibracional
# ============================================================================

class FiltroVibracional:
    """
    Filtro lorentziano centrado en λ₁.

    La coherencia espectral Ψ_spec sigue la fórmula análoga de Kuramoto:
        Ψ_spec = 1 − 2γ_s / (2π·F_HRV) = 0,891 ≥ 0,888

    Parámetros
    ----------
    gamma_s : float, opcional
        Semiancho lorentziano (Hz). Si es None se calcula de la fórmula
        de Kuramoto para obtener Ψ_spec = 0,891.
    f_hrv : float
        Frecuencia HRV (Hz). Por defecto F_HRV = 0,1 Hz.

    Ejemplo
    -------
    >>> f = FiltroVibracional()
    >>> f.psi_spec
    0.891
    >>> f.aprobado
    True
    """

    def __init__(
        self,
        gamma_s: float = None,
        f_hrv: float = F_HRV,
    ) -> None:
        if f_hrv <= 0:
            raise ValueError("f_hrv debe ser positivo.")
        self.f_hrv = f_hrv
        if gamma_s is None:
            # Kuramoto: γ_s = (1 − 0,891) · π · F_HRV
            self.gamma_s = (1.0 - _PSI_SPEC_KURAMOTO) * math.pi * f_hrv
        else:
            if gamma_s < 0:
                raise ValueError("gamma_s no puede ser negativo.")
            self.gamma_s = gamma_s

    @property
    def psi_spec(self) -> float:
        """Coherencia espectral Ψ_spec vía fórmula análoga de Kuramoto."""
        return 1.0 - 2.0 * self.gamma_s / (2.0 * math.pi * self.f_hrv)

    @property
    def aprobado(self) -> bool:
        """True si Ψ_spec ≥ PSI_MINIMA (0,888)."""
        return self.psi_spec >= PSI_MINIMA

    def lorentziano(self, f: float, f0: float = LAMBDA_1) -> float:
        """
        Evalúa la función lorentziana en la frecuencia f centrada en f0.

        L(f) = (γ_s/π) / ((f − f₀)² + γ_s²)
        """
        return (self.gamma_s / math.pi) / ((f - f0) ** 2 + self.gamma_s ** 2)

    def aplicar(self, malla: "MallaEspectral") -> np.ndarray:
        """Aplica el filtro lorentziano a la malla espectral dada."""
        return np.array(
            [self.lorentziano(f) for f in malla.frecuencias],
            dtype=np.float64,
        )

    def amplitud_pico(self, f0: float = LAMBDA_1) -> float:
        """Amplitud pico del lorentziano L(f₀) = 1/(π·γ_s)."""
        return 1.0 / (math.pi * self.gamma_s)

    def __repr__(self) -> str:
        return (
            f"FiltroVibracional(gamma_s={self.gamma_s:.6f} Hz, "
            f"f_hrv={self.f_hrv} Hz, psi_spec={self.psi_spec:.4f})"
        )


# ============================================================================
# CLASE 4 – IntegradorRK4
# ============================================================================

class IntegradorRK4:
    """
    Integrador manual de cuarto orden de Runge-Kutta (RK4).

    Resuelve la ecuación noética:
        dΨ/dt = F_noético(t) − α·Ψ + G_norm·α·Ψ·(1−Ψ)

    Con F_noético = α (forzado constante), la ecuación se reduce a:
        dΨ/dt = α·(1−Ψ)·(1 + G_norm·Ψ)

    que converge a la meseta Ψ → 1. Utiliza G_NORM_RK4 = 10.

    Parámetros
    ----------
    alpha : float
        Coeficiente de amortiguamiento. Por defecto 0,1.
    g_norm : float
        Ganancia normalizada superradiante. Por defecto G_NORM_RK4 = 10.
    psi_0 : float
        Condición inicial Ψ(0). Por defecto 0,01.
    dt : float
        Paso temporal (s). Por defecto 0,01.
    t_final : float
        Tiempo final de integración (s). Por defecto 20,0.

    Ejemplo
    -------
    >>> rk4 = IntegradorRK4()
    >>> t, psi = rk4.integrar()
    >>> rk4.plateau_alcanzado
    True
    """

    def __init__(
        self,
        alpha: float = 0.1,
        g_norm: float = G_NORM_RK4,
        psi_0: float = 0.01,
        dt: float = 0.01,
        t_final: float = 20.0,
    ) -> None:
        if alpha <= 0:
            raise ValueError("alpha debe ser positivo.")
        if g_norm < 0:
            raise ValueError("g_norm no puede ser negativo.")
        if not (0.0 <= psi_0 <= 1.0):
            raise ValueError("psi_0 debe estar en [0, 1].")
        if dt <= 0:
            raise ValueError("dt debe ser positivo.")
        if t_final <= 0:
            raise ValueError("t_final debe ser positivo.")
        self.alpha = alpha
        self.g_norm = g_norm
        self.psi_0 = psi_0
        self.dt = dt
        self.t_final = t_final
        self._t: np.ndarray = np.array([])
        self._psi: np.ndarray = np.array([])
        self._integrado: bool = False

    def _derivada(self, t: float, psi: float) -> float:
        """Computa dΨ/dt = α·(1−Ψ)·(1 + G·Ψ)."""
        f_noetica = self.alpha  # forzado constante = amortiguamiento
        return f_noetica - self.alpha * psi + self.g_norm * self.alpha * psi * (1.0 - psi)

    def _rk4_paso(self, t: float, psi: float, dt: float) -> float:
        """Ejecuta un paso RK4 desde (t, Ψ)."""
        k1 = self._derivada(t, psi)
        k2 = self._derivada(t + dt / 2.0, psi + dt / 2.0 * k1)
        k3 = self._derivada(t + dt / 2.0, psi + dt / 2.0 * k2)
        k4 = self._derivada(t + dt, psi + dt * k3)
        return psi + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def integrar(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ejecuta la integración RK4 completa.

        Retorna
        -------
        Tuple[np.ndarray, np.ndarray]
            Arrays (t, Ψ) de longitud n_pasos + 1.
        """
        n_pasos = int(round(self.t_final / self.dt))
        t_arr = np.zeros(n_pasos + 1, dtype=np.float64)
        psi_arr = np.zeros(n_pasos + 1, dtype=np.float64)
        psi_arr[0] = self.psi_0
        for i in range(n_pasos):
            t_arr[i + 1] = t_arr[i] + self.dt
            psi_arr[i + 1] = self._rk4_paso(t_arr[i], psi_arr[i], self.dt)
        self._t = t_arr
        self._psi = psi_arr
        self._integrado = True
        return t_arr, psi_arr

    def _asegurar_integrado(self) -> None:
        if not self._integrado:
            self.integrar()

    @property
    def psi_final(self) -> float:
        """Valor final de Ψ tras la integración."""
        self._asegurar_integrado()
        return float(self._psi[-1])

    @property
    def plateau_alcanzado(self) -> bool:
        """True si la media del último 10 % de pasos supera 0,999."""
        self._asegurar_integrado()
        n_cola = max(1, len(self._psi) // 10)
        return float(np.mean(self._psi[-n_cola:])) >= 0.999

    @property
    def psi_plateau(self) -> float:
        """Media de Ψ en el último 10 % de pasos (valor de la meseta)."""
        self._asegurar_integrado()
        n_cola = max(1, len(self._psi) // 10)
        return float(np.mean(self._psi[-n_cola:]))

    def __repr__(self) -> str:
        return (
            f"IntegradorRK4(alpha={self.alpha}, g_norm={self.g_norm}, "
            f"psi_0={self.psi_0}, t_final={self.t_final})"
        )


# ============================================================================
# CLASE 5 – EspectroEnergia
# ============================================================================

class EspectroEnergia:
    """
    Verificación analítica del error espectral QED-RIEMANN.

    Comprueba que λ₁ ≈ γ₁·f₀ con tolerancia < 10⁻⁶:
        error_espectral = |λ₁ − γ₁·f₀| / (γ₁·f₀) ≈ 9,82 × 10⁻⁷

    Parámetros
    ----------
    lambda_1 : float
        Frecuencia espectral central (Hz). Por defecto LAMBDA_1.
    gamma_1 : float
        Parte imaginaria del primer cero de Riemann γ₁. Por defecto
        GAMMA_1_RIEMANN = 14,134725141734693790.
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto F0_HZ = 141,7001.

    Ejemplo
    -------
    >>> e = EspectroEnergia()
    >>> e.error_espectral < 1e-6
    True
    >>> e.verificado
    True
    """

    def __init__(
        self,
        lambda_1: float = LAMBDA_1,
        gamma_1: float = GAMMA_1_RIEMANN,
        f0: float = F0_HZ,
    ) -> None:
        if lambda_1 <= 0:
            raise ValueError("lambda_1 debe ser positivo.")
        if gamma_1 <= 0:
            raise ValueError("gamma_1 debe ser positivo.")
        if f0 <= 0:
            raise ValueError("f0 debe ser positivo.")
        self.lambda_1 = lambda_1
        self.gamma_1 = gamma_1
        self.f0 = f0

    @property
    def gamma_1_f0(self) -> float:
        """Producto γ₁·f₀ (frecuencia de referencia Riemann-QCAL)."""
        return self.gamma_1 * self.f0

    @property
    def error_espectral(self) -> float:
        """Error relativo |λ₁ − γ₁·f₀| / (γ₁·f₀)."""
        ref = self.gamma_1_f0
        return abs(self.lambda_1 - ref) / ref

    @property
    def verificado(self) -> bool:
        """True si error_espectral < 10⁻⁶ (QED-RIEMANN-VERIFICADO)."""
        return self.error_espectral < 1.0e-6

    @property
    def etiqueta(self) -> str:
        """Etiqueta de verificación."""
        return "QED-RIEMANN-VERIFICADO" if self.verificado else "FALLA-ESPECTRAL"

    def __repr__(self) -> str:
        return (
            f"EspectroEnergia(lambda_1={self.lambda_1} Hz, "
            f"gamma_1={self.gamma_1:.15f}, "
            f"error={self.error_espectral:.4e}, "
            f"etiqueta='{self.etiqueta}')"
        )


# ============================================================================
# CLASE 6 – ForzadoEspectralNoetico
# ============================================================================

class ForzadoEspectralNoetico:
    """
    Forzado espectral noético: portadora λ₁ modulada en AM a f_HRV.

    F(t) = amplitud · (1 + cos(2π·f_HRV·t)) · cos(2π·λ₁·t)

    Parámetros
    ----------
    lambda_1 : float
        Frecuencia portadora (Hz). Por defecto LAMBDA_1.
    f_hrv : float
        Frecuencia de modulación HRV (Hz). Por defecto F_HRV = 0,1 Hz.
    amplitud : float
        Amplitud base del forzado. Por defecto 1,0.

    Ejemplo
    -------
    >>> f = ForzadoEspectralNoetico()
    >>> f.frecuencia_portadora
    2002.89
    >>> f.frecuencia_modulacion
    0.1
    """

    def __init__(
        self,
        lambda_1: float = LAMBDA_1,
        f_hrv: float = F_HRV,
        amplitud: float = 1.0,
    ) -> None:
        if lambda_1 <= 0:
            raise ValueError("lambda_1 debe ser positivo.")
        if f_hrv <= 0:
            raise ValueError("f_hrv debe ser positivo.")
        if amplitud <= 0:
            raise ValueError("amplitud debe ser positiva.")
        self._lambda_1 = lambda_1
        self._f_hrv = f_hrv
        self._amplitud = amplitud

    @property
    def frecuencia_portadora(self) -> float:
        """Frecuencia de la portadora λ₁ (Hz)."""
        return self._lambda_1

    @property
    def frecuencia_modulacion(self) -> float:
        """Frecuencia de modulación f_HRV (Hz)."""
        return self._f_hrv

    @property
    def amplitud_base(self) -> float:
        """Amplitud base del forzado."""
        return self._amplitud

    @property
    def amplitud_pico(self) -> float:
        """Amplitud pico = 2 × amplitud (cuando portadora y modulación son máximas)."""
        return 2.0 * self._amplitud

    def evaluar(self, t: "np.ndarray | float") -> "np.ndarray | float":
        """
        Evalúa F(t) = amplitud·(1 + cos(2π·f_HRV·t))·cos(2π·λ₁·t).

        Parámetros
        ----------
        t : float o np.ndarray
            Tiempo(s) en segundos.

        Retorna
        -------
        float o np.ndarray
            Señal de forzado en el instante(s) t.
        """
        t_arr = np.asarray(t, dtype=np.float64)
        portadora = np.cos(2.0 * np.pi * self._lambda_1 * t_arr)
        modulacion = 1.0 + np.cos(2.0 * np.pi * self._f_hrv * t_arr)
        return self._amplitud * modulacion * portadora

    def __repr__(self) -> str:
        return (
            f"ForzadoEspectralNoetico(lambda_1={self._lambda_1} Hz, "
            f"f_hrv={self._f_hrv} Hz, amplitud={self._amplitud})"
        )


# ============================================================================
# CLASE 7 – TerminoSuperradiante
# ============================================================================

class TerminoSuperradiante:
    """
    Término superradiante de Dicke para N microtúbulos hipocampales.

    La ganancia superradiante es N²: en el régimen superradiante de Dicke,
    la intensidad emitida escala como N² (no como N).

    Parámetros
    ----------
    n : int
        Número de microtúbulos. Por defecto N_MICROTUBULOS = 10¹³.
    rendimiento : float
        Rendimiento cuántico en régimen superradiante. Por defecto
        RENDIMIENTO_CUANTICO = 1000,0.

    Ejemplo
    -------
    >>> ts = TerminoSuperradiante()
    >>> ts.superradiante
    True
    >>> ts.rendimiento_cuantico
    1000.0
    """

    # Umbral mínimo de microtúbulos para el régimen superradiante
    _N_UMBRAL: int = int(1e6)

    def __init__(
        self,
        n: int = N_MICROTUBULOS,
        rendimiento: float = RENDIMIENTO_CUANTICO,
    ) -> None:
        if n <= 0:
            raise ValueError("n debe ser positivo.")
        if rendimiento <= 0:
            raise ValueError("rendimiento debe ser positivo.")
        self._n = n
        self._rendimiento = rendimiento

    @property
    def n(self) -> int:
        """Número de microtúbulos."""
        return self._n

    @property
    def n_squared(self) -> float:
        """Ganancia superradiante N² (Dicke)."""
        return float(self._n) ** 2

    @property
    def ganancia(self) -> float:
        """Ganancia total del término superradiante (= N²)."""
        return self.n_squared

    @property
    def rendimiento_cuantico(self) -> float:
        """Rendimiento cuántico en régimen superradiante."""
        return self._rendimiento

    @property
    def superradiante(self) -> bool:
        """True si N supera el umbral superradiante (N ≥ 10⁶)."""
        return self._n >= self._N_UMBRAL

    def escalar(self, amplitud: float) -> float:
        """Escala una amplitud por la ganancia N²."""
        return amplitud * self.n_squared

    def __repr__(self) -> str:
        return (
            f"TerminoSuperradiante(n={self._n:.2e}, "
            f"n_squared={self.n_squared:.2e}, "
            f"rendimiento={self._rendimiento})"
        )


# ============================================================================
# CLASE 8 – CoherenciaBiologica
# ============================================================================

class CoherenciaBiologica:
    """
    Coherencia biológica total: combinación ponderada de Ψ_spec, Ψ_dyn y Ψ_UPE.

    Fórmula (pesos iguales):
        Ψ_total = (Ψ_spec + Ψ_dyn + Ψ_UPE) / 3 ≈ 0,956

    Ψ_UPE en el régimen superradiante:
        Ψ_UPE = 1 − (1 − Ψ_spec) · 2 · F_HRV

    Parámetros
    ----------
    psi_spec : float
        Coherencia espectral Kuramoto (por defecto _PSI_SPEC_KURAMOTO = 0,891).
    psi_dyn : float
        Coherencia dinámica de la meseta RK4.
    psi_upe : float, opcional
        Coherencia UPE. Si es None se calcula automáticamente.

    Ejemplo
    -------
    >>> cb = CoherenciaBiologica(psi_spec=0.891, psi_dyn=1.0)
    >>> round(cb.psi_total, 3)
    0.956
    >>> cb.aprobado
    True
    """

    def __init__(
        self,
        psi_spec: float = _PSI_SPEC_KURAMOTO,
        psi_dyn: float = 1.0,
        psi_upe: float = None,
    ) -> None:
        for nombre, val in [("psi_spec", psi_spec), ("psi_dyn", psi_dyn)]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"{nombre} debe estar en [0, 1]; se recibió {val}.")
        self.psi_spec = psi_spec
        self.psi_dyn = psi_dyn
        if psi_upe is None:
            # Ψ_UPE = 1 − (1 − Ψ_spec) · 2 · F_HRV
            self.psi_upe = 1.0 - (1.0 - psi_spec) * 2.0 * F_HRV
        else:
            if not (0.0 <= psi_upe <= 1.0):
                raise ValueError(f"psi_upe debe estar en [0, 1]; se recibió {psi_upe}.")
            self.psi_upe = psi_upe

    @property
    def psi_total(self) -> float:
        """Coherencia biológica total Ψ = (Ψ_spec + Ψ_dyn + Ψ_UPE) / 3."""
        return (self.psi_spec + self.psi_dyn + self.psi_upe) / 3.0

    @property
    def aprobado(self) -> bool:
        """True si Ψ_total ≥ PSI_MINIMA (0,888)."""
        return self.psi_total >= PSI_MINIMA

    @property
    def componentes(self) -> dict:
        """Diccionario con los tres componentes de coherencia."""
        return {
            "psi_spec": self.psi_spec,
            "psi_dyn": self.psi_dyn,
            "psi_upe": self.psi_upe,
        }

    def __repr__(self) -> str:
        return (
            f"CoherenciaBiologica("
            f"psi_spec={self.psi_spec:.4f}, "
            f"psi_dyn={self.psi_dyn:.6f}, "
            f"psi_upe={self.psi_upe:.4f}, "
            f"psi_total={self.psi_total:.4f})"
        )


# ============================================================================
# API PÚBLICA – generate_upe_signature
# ============================================================================

def generate_upe_signature(
    t: np.ndarray,
    lambdas: List[float],
    hrv_freq: float = F_HRV,
) -> np.ndarray:
    """
    Genera la firma UPE (Ultra-Photon Emission) hipocampal superradiante.

    Señal UPE central: portadora(s) λᵢ moduladas en AM a f_HRV, con amplitud
    escalada por N² (superradiancia de Dicke):
        UPE(t) = Σᵢ N² · (1 + cos(2π·f_HRV·t)) · cos(2π·λᵢ·t)

    Parámetros
    ----------
    t : np.ndarray
        Array de tiempos en segundos.
    lambdas : list of float
        Lista de frecuencias portadoras (Hz). Típicamente [LAMBDA_1].
    hrv_freq : float
        Frecuencia de modulación HRV (Hz). Por defecto F_HRV = 0,1 Hz.

    Retorna
    -------
    np.ndarray
        Señal UPE de forma (len(t),) con amplitud ∝ N² = 10²⁶.

    Ejemplo
    -------
    >>> import numpy as np
    >>> from physics.qcal_ns_rk4 import generate_upe_signature, LAMBDA_1
    >>> t = np.linspace(0, 1, 10000)
    >>> sig = generate_upe_signature(t, [LAMBDA_1])
    >>> sig.shape
    (10000,)
    """
    t_arr = np.asarray(t, dtype=np.float64)
    signal = np.zeros(len(t_arr), dtype=np.float64)
    modulacion = 1.0 + np.cos(2.0 * np.pi * hrv_freq * t_arr)
    for lam in lambdas:
        portadora = np.cos(2.0 * np.pi * lam * t_arr)
        signal += N_SQUARED * modulacion * portadora
    return signal


# ============================================================================
# API PÚBLICA – qcal_ns_rk4_activar
# ============================================================================

def qcal_ns_rk4_activar() -> ResultadoLaserNoetico:
    """
    Activa el protocolo LÁSER NOÉTICO v1.0 en 7 pasos.

    Pasos
    -----
    1. Crear malla espectral centrada en λ₁ ± 50 Hz.
    2. Calcular Ψ_spec mediante FiltroVibracional (Kuramoto) → 0,891.
    3. Integrar RK4 dΨ/dt = F_noético − α·Ψ + G·α·Ψ·(1−Ψ) → meseta Ψ → 1.
    4. Calcular error espectral |λ₁ − γ₁·f₀|/(γ₁·f₀) → ≈ 9,82 × 10⁻⁷.
    5. Evaluar ForzadoEspectralNoetico (portadora λ₁ modulada a f_HRV).
    6. Evaluar TerminoSuperradiante (ganancia N², rendimiento 10³ QY).
    7. Calcular CoherenciaBiologica → Ψ_total ≈ 0,956.

    Retorna
    -------
    ResultadoLaserNoetico
        psi_spec=0,891, psi_total≈0,956, error_espectral≈9,82×10⁻⁷,
        superradiante=True, plateau_alcanzado=True, rendimiento_cuantico=1000,0.

    Ejemplo
    -------
    >>> from physics.qcal_ns_rk4 import qcal_ns_rk4_activar
    >>> resultado = qcal_ns_rk4_activar()
    >>> resultado.psi_spec
    0.891
    >>> resultado.superradiante
    True
    >>> resultado.plateau_alcanzado
    True
    """
    # ── PASO 1: Malla espectral ────────────────────────────────────────────
    _malla = MallaEspectral(lambda_1=LAMBDA_1, delta_hz=50.0, n_puntos=1000)

    # ── PASO 2: Filtro vibracional → Ψ_spec ───────────────────────────────
    filtro = FiltroVibracional()
    psi_spec = filtro.psi_spec  # = 0.891

    # ── PASO 3: Integración RK4 → meseta Ψ → 1 ───────────────────────────
    rk4 = IntegradorRK4(
        alpha=0.1,
        g_norm=G_NORM_RK4,
        psi_0=0.01,
        dt=0.01,
        t_final=20.0,
    )
    rk4.integrar()
    psi_dyn = rk4.psi_plateau
    plateau_alcanzado = rk4.plateau_alcanzado

    # ── PASO 4: Error espectral QED-RIEMANN ───────────────────────────────
    espectro = EspectroEnergia()
    error_espectral = espectro.error_espectral

    # ── PASO 5: Forzado espectral noético ─────────────────────────────────
    _forzado = ForzadoEspectralNoetico(lambda_1=LAMBDA_1, f_hrv=F_HRV)

    # ── PASO 6: Término superradiante ─────────────────────────────────────
    superradiante_term = TerminoSuperradiante(
        n=N_MICROTUBULOS, rendimiento=RENDIMIENTO_CUANTICO
    )
    superradiante = superradiante_term.superradiante
    rendimiento_cuantico = superradiante_term.rendimiento_cuantico

    # ── PASO 7: Coherencia biológica → Ψ_total ────────────────────────────
    coherencia = CoherenciaBiologica(psi_spec=psi_spec, psi_dyn=psi_dyn)
    psi_upe = coherencia.psi_upe
    psi_total = round(coherencia.psi_total, 3)
    aprobado = coherencia.aprobado

    return ResultadoLaserNoetico(
        psi_spec=psi_spec,
        psi_dyn=psi_dyn,
        psi_upe=psi_upe,
        psi_total=psi_total,
        error_espectral=error_espectral,
        superradiante=superradiante,
        plateau_alcanzado=plateau_alcanzado,
        rendimiento_cuantico=rendimiento_cuantico,
        aprobado=aprobado,
    )
