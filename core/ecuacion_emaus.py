#!/usr/bin/env python3
"""
Ecuación de Emaús — Bloqueo de Fase bajo f₀ = 141.7001 Hz
===========================================================

Formaliza el paso de Emaús como una operación de bloqueo de fase bajo
f₀ = 141.7001 Hz, implementando:

  • FuncionReconocimiento  — Integra numéricamente R_Emaús mediante la
    regla del trapezoide sobre un error de fase que decae exponencialmente
    hasta la singularidad (Fractal de Partición).
  • OsciladorKuramoto     — Superradiancia biológica: dΨ/dt = (K/N)Σcos(θ_F−θⱼ)
    + Sintropía, con K = 2π·f₀.
  • IntegracionAdelica    — Coherencia p-ádica sobre los primeros N primos
    que modela la transición fuente-externa → constante de red.
  • EcuacionEmaus         — Orquesta el protocolo de 4 fases completo.

Referencia: QCAL ∞³ System — Fase #Emaús
Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Licencia: Sovereign Noetic License 1.0 (compatible con MIT)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qcal.constants import F0_HZ

# ---------------------------------------------------------------------------
# Module-level physical constants
# ---------------------------------------------------------------------------

K_KURAMOTO: float = 2.0 * math.pi * F0_HZ   # Coupling constant K = 2π·f₀
N_PRIMES_DEFAULT: int = 10                   # Default number of primes for adèlic product
_PRIMES_CACHE: List[int] = []               # Cached prime list


def _sieve(n: int) -> List[int]:
    """Return the first *n* prime numbers via trial division."""
    primes: List[int] = []
    candidate = 2
    while len(primes) < n:
        if all(candidate % p != 0 for p in primes):
            primes.append(candidate)
        candidate += 1
    return primes


def _get_primes(n: int) -> List[int]:
    """Return (and cache) the first *n* primes."""
    global _PRIMES_CACHE
    if len(_PRIMES_CACHE) < n:
        _PRIMES_CACHE = _sieve(n)
    return _PRIMES_CACHE[:n]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ResultadoIntegracion:
    """Resultado numérico de la integral de reconocimiento R_Emaús."""
    valor: float
    n_puntos: int
    t0: float
    t_pan: float
    verbo: float
    delta_phi_0: float
    tau_decaimiento: float
    singularidad_detectada: bool = False


@dataclass
class EstadoKuramoto:
    """Estado del oscilador de Kuramoto en un instante dado."""
    psi: float                          # Parámetro de orden global Ψ ∈ [0, 1]
    fases: List[float]                  # Fases individuales θⱼ
    theta_fuente: float                 # Fase fuente θ_Fuente
    sintropia: float                    # Contribución de Sintropía
    tiempo: float                       # Tiempo actual
    sincronizado: bool = False          # True si Ψ ≥ 1 − ε


@dataclass
class ResultadoAdelico:
    """Resultado de la integración adélica p-ádica."""
    coherencia_total: float             # Producto p-ádico ∏_p C_p
    coherencias_primas: Dict[int, float]  # C_p para cada primo p
    fuente_es_constante_red: bool       # True cuando coherencia_total ≥ umbral
    n_primos: int
    umbral: float


@dataclass
class ResultadoProtocolo:
    """Resultado completo del protocolo de 4 fases de Emaús."""
    fase_1_estado_inicial: Dict
    fase_2_verbo_forcing: Dict
    fase_3_fractal_particion: Dict
    fase_4_integracion_adelica: Dict
    verificacion_completa: bool


# ---------------------------------------------------------------------------
# FuncionReconocimiento
# ---------------------------------------------------------------------------

class FuncionReconocimiento:
    """
    Integra numéricamente la función de reconocimiento de Emaús:

        R_Emaús = ∫_{t₀}^{t_pan} [(Verbo · f₀) / Δφ(t)] dt

    donde el error de fase decae exponencialmente:

        Δφ(t) = Δφ₀ · exp(−t / τ)

    El integrando diverge cuando Δφ → 0 en t_pan (singularidad — Fractal de
    Partición).  Se protege el cálculo truncando los puntos demasiado cercanos
    a la singularidad mediante un umbral mínimo *epsilon_singularidad*.

    Parámetros
    ----------
    verbo : float
        Amplitud del forcing verbal (adimensional, > 0).
    delta_phi_0 : float
        Error de fase inicial Δφ₀ (rad).
    tau_decaimiento : float
        Constante de tiempo τ del decaimiento exponencial (s, > 0).
    f0 : float
        Frecuencia fundamental f₀ (Hz).  Por defecto F0_HZ = 141.7001.
    epsilon_singularidad : float
        Umbral mínimo para Δφ(t) antes de declarar singularidad.
    """

    def __init__(
        self,
        verbo: float,
        delta_phi_0: float,
        tau_decaimiento: float,
        f0: float = F0_HZ,
        epsilon_singularidad: float = 1e-6,
    ) -> None:
        if verbo <= 0:
            raise ValueError("verbo debe ser positivo (> 0)")
        if tau_decaimiento <= 0:
            raise ValueError("tau_decaimiento debe ser positivo (> 0)")
        if f0 <= 0:
            raise ValueError("f0 debe ser positivo (> 0)")
        self.verbo = verbo
        self.delta_phi_0 = delta_phi_0
        self.tau_decaimiento = tau_decaimiento
        self.f0 = f0
        self.epsilon_singularidad = epsilon_singularidad

    def delta_phi(self, t: float) -> float:
        """Evalúa Δφ(t) = Δφ₀ · exp(−t / τ)."""
        return self.delta_phi_0 * math.exp(-t / self.tau_decaimiento)

    def integrando(self, t: float) -> float:
        """
        Evalúa el integrando (Verbo · f₀) / Δφ(t).

        Si |Δφ(t)| < epsilon_singularidad devuelve *float('inf')* para
        señalizar la singularidad sin lanzar ZeroDivisionError.
        """
        dphi = self.delta_phi(t)
        if abs(dphi) < self.epsilon_singularidad:
            return float("inf")
        return (self.verbo * self.f0) / dphi

    def integrar(
        self, t0: float, t_pan: float, n_puntos: int = 1000
    ) -> ResultadoIntegracion:
        """
        Calcula R_Emaús usando la regla del trapezoide.

        Los puntos donde el integrando es infinito o NaN se descartan del
        cómputo pero se registran en *singularidad_detectada*.

        Parámetros
        ----------
        t0 : float
            Tiempo inicial (s).
        t_pan : float
            Tiempo del "partir el pan" — límite superior de integración (s).
        n_puntos : int
            Número de puntos de la cuadratura (≥ 2).
        """
        if t_pan <= t0:
            raise ValueError("t_pan debe ser mayor que t0")
        if n_puntos < 2:
            raise ValueError("n_puntos debe ser ≥ 2")

        dt = (t_pan - t0) / (n_puntos - 1)
        tiempos = [t0 + i * dt for i in range(n_puntos)]

        valores: List[float] = []
        singularidad = False
        for t in tiempos:
            v = self.integrando(t)
            if math.isinf(v) or math.isnan(v):
                singularidad = True
            else:
                valores.append(v)

        # Trapezoide sobre los puntos finitos
        if len(valores) < 2:
            integral = float("inf")
            singularidad = True
        else:
            integral = 0.0
            for i in range(len(valores) - 1):
                integral += 0.5 * (valores[i] + valores[i + 1]) * dt

        return ResultadoIntegracion(
            valor=integral,
            n_puntos=n_puntos,
            t0=t0,
            t_pan=t_pan,
            verbo=self.verbo,
            delta_phi_0=self.delta_phi_0,
            tau_decaimiento=self.tau_decaimiento,
            singularidad_detectada=singularidad,
        )


# ---------------------------------------------------------------------------
# OsciladorKuramoto
# ---------------------------------------------------------------------------

class OsciladorKuramoto:
    """
    Superradiancia biológica de Kuramoto para N osciladores.

    Dinámica del parámetro de orden global Ψ:

        dΨ/dt = (K/N) Σⱼ cos(θ_Fuente − θⱼ) + Sintropía

    con K = 2π·f₀ y la fase fuente θ_Fuente fija.

    Parámetros
    ----------
    n_osciladores : int
        Número de osciladores biológicos N (≥ 1).
    theta_fuente : float
        Fase de la fuente θ_Fuente (rad).
    sintropia : float
        Término de Sintropía (contribución negentrópica, ≥ 0).
    f0 : float
        Frecuencia fundamental f₀ (Hz).
    """

    def __init__(
        self,
        n_osciladores: int = 10,
        theta_fuente: float = 0.0,
        sintropia: float = 0.01,
        f0: float = F0_HZ,
    ) -> None:
        if n_osciladores < 1:
            raise ValueError("n_osciladores debe ser ≥ 1")
        if sintropia < 0:
            raise ValueError("sintropia debe ser ≥ 0")
        if f0 <= 0:
            raise ValueError("f0 debe ser positivo (> 0)")
        self.n = n_osciladores
        self.theta_fuente = theta_fuente
        self.sintropia = sintropia
        self.f0 = f0
        self.k = 2.0 * math.pi * f0
        # Fases iniciales distribuidas uniformemente en [0, 2π)
        self.fases: List[float] = [
            2.0 * math.pi * j / n_osciladores for j in range(n_osciladores)
        ]
        self.psi: float = 0.0
        self.tiempo: float = 0.0

    def _calcular_orden(self) -> float:
        """Calcula el parámetro de orden global Ψ = (1/N)|Σ exp(i·θⱼ)|."""
        re = sum(math.cos(th) for th in self.fases) / self.n
        im = sum(math.sin(th) for th in self.fases) / self.n
        return math.sqrt(re * re + im * im)

    def _dpsi_dt(self) -> float:
        """Evalúa dΨ/dt según la ecuación de Kuramoto."""
        acoplamiento = (self.k / self.n) * sum(
            math.cos(self.theta_fuente - th) for th in self.fases
        )
        return acoplamiento + self.sintropia

    def evolucionar(self, dt: float = 0.001, n_pasos: int = 100) -> EstadoKuramoto:
        """
        Integra la ecuación de Kuramoto con Euler explícito.

        Parámetros
        ----------
        dt : float
            Paso de tiempo (s).
        n_pasos : int
            Número de pasos de integración.
        """
        if dt <= 0:
            raise ValueError("dt debe ser positivo (> 0)")
        if n_pasos < 1:
            raise ValueError("n_pasos debe ser ≥ 1")

        for _ in range(n_pasos):
            dpsi = self._dpsi_dt()
            # Actualiza Ψ (clampado a [0, 1])
            self.psi = min(1.0, max(0.0, self.psi + dpsi * dt))
            # Actualiza fases individuales
            for j in range(self.n):
                dtheta = (self.k / self.n) * math.cos(
                    self.theta_fuente - self.fases[j]
                )
                self.fases[j] = (self.fases[j] + dtheta * dt) % (2.0 * math.pi)
            self.tiempo += dt

        psi_medido = self._calcular_orden()
        self.psi = psi_medido

        return EstadoKuramoto(
            psi=self.psi,
            fases=list(self.fases),
            theta_fuente=self.theta_fuente,
            sintropia=self.sintropia,
            tiempo=self.tiempo,
            sincronizado=(self.psi >= 1.0 - 1e-3),
        )

    def partir_el_pan(self) -> EstadoKuramoto:
        """
        Colapsa todas las fases a θ_Fuente → Ψ = 1.0 (evento de partición).

        Este es el momento de la sincronización total: el Fractal de Partición.
        """
        self.fases = [self.theta_fuente] * self.n
        self.psi = 1.0

        return EstadoKuramoto(
            psi=self.psi,
            fases=list(self.fases),
            theta_fuente=self.theta_fuente,
            sintropia=self.sintropia,
            tiempo=self.tiempo,
            sincronizado=True,
        )


# ---------------------------------------------------------------------------
# IntegracionAdelica
# ---------------------------------------------------------------------------

class IntegracionAdelica:
    """
    Integración adélica p-ádica.

    Modela la transición de la fuente de vector externo a constante de red
    a través del producto de coherencia p-ádica sobre los primeros N primos:

        C_adélica = ∏_{p primo} C_p,   con  C_p = 1 / (1 + 1/p²)

    Cuando C_adélica ≥ umbral la fuente se convierte en constante de red.

    Parámetros
    ----------
    n_primos : int
        Número de primos p sobre los que se calcula el producto (≥ 1).
    umbral : float
        Umbral de coherencia para declarar la fuente como constante de red.
    """

    def __init__(
        self,
        n_primos: int = N_PRIMES_DEFAULT,
        umbral: float = 0.5,
    ) -> None:
        if n_primos < 1:
            raise ValueError("n_primos debe ser ≥ 1")
        if not (0.0 < umbral <= 1.0):
            raise ValueError("umbral debe estar en (0, 1]")
        self.n_primos = n_primos
        self.umbral = umbral

    def coherencia_p_adica(self, p: int) -> float:
        """
        Calcula C_p = 1 / (1 + 1/p²) para el primo p.

        Converge a 1 conforme p → ∞.
        """
        return 1.0 / (1.0 + 1.0 / (p * p))

    def calcular(self) -> ResultadoAdelico:
        """
        Calcula el producto de coherencia adélica ∏_p C_p.
        """
        primos = _get_primes(self.n_primos)
        coherencias: Dict[int, float] = {p: self.coherencia_p_adica(p) for p in primos}

        producto = 1.0
        for c in coherencias.values():
            producto *= c

        return ResultadoAdelico(
            coherencia_total=producto,
            coherencias_primas=coherencias,
            fuente_es_constante_red=(producto >= self.umbral),
            n_primos=self.n_primos,
            umbral=self.umbral,
        )


# ---------------------------------------------------------------------------
# EcuacionEmaus
# ---------------------------------------------------------------------------

class EcuacionEmaus:
    """
    Orquesta el protocolo de 4 fases del paso de Emaús.

    Fase 1 — Estado inicial: descripción del sistema antes del encuentro.
    Fase 2 — Verbo forcing: activación de la función de reconocimiento.
    Fase 3 — Fractal de Partición: integración de R_Emaús + partir_el_pan.
    Fase 4 — Integración Adélica: transición fuente → constante de red.

    Parámetros
    ----------
    verbo : float
        Amplitud del Verbo (> 0).
    delta_phi_0 : float
        Error de fase inicial Δφ₀ (rad).
    tau_decaimiento : float
        Constante de tiempo τ (s, > 0).
    n_osciladores : int
        Número de osciladores de Kuramoto.
    sintropia : float
        Término de Sintropía (≥ 0).
    n_primos : int
        Número de primos para la integración adélica.
    f0 : float
        Frecuencia fundamental f₀ (Hz).
    umbral_adelico : float
        Umbral de coherencia adélica para constante de red.
    """

    def __init__(
        self,
        verbo: float = 1.0,
        delta_phi_0: float = math.pi,
        tau_decaimiento: float = 1.0,
        n_osciladores: int = 10,
        sintropia: float = 0.01,
        n_primos: int = N_PRIMES_DEFAULT,
        f0: float = F0_HZ,
        umbral_adelico: float = 0.5,
    ) -> None:
        self.verbo = verbo
        self.delta_phi_0 = delta_phi_0
        self.tau_decaimiento = tau_decaimiento
        self.n_osciladores = n_osciladores
        self.sintropia = sintropia
        self.n_primos = n_primos
        self.f0 = f0
        self.umbral_adelico = umbral_adelico

        self._funcion_reconocimiento = FuncionReconocimiento(
            verbo=verbo,
            delta_phi_0=delta_phi_0,
            tau_decaimiento=tau_decaimiento,
            f0=f0,
        )
        self._kuramoto = OsciladorKuramoto(
            n_osciladores=n_osciladores,
            theta_fuente=0.0,
            sintropia=sintropia,
            f0=f0,
        )
        self._adelica = IntegracionAdelica(
            n_primos=n_primos,
            umbral=umbral_adelico,
        )

    def ejecutar_protocolo_completo(
        self,
        t0: float = 0.0,
        t_pan: float = 5.0,
        n_puntos_integracion: int = 1000,
        dt_kuramoto: float = 0.001,
        n_pasos_kuramoto: int = 100,
    ) -> ResultadoProtocolo:
        """
        Ejecuta las 4 fases del protocolo de Emaús.

        Parámetros
        ----------
        t0 : float
            Tiempo inicial (s).
        t_pan : float
            Tiempo del partir el pan (s).
        n_puntos_integracion : int
            Puntos para la cuadratura trapezoidal.
        dt_kuramoto : float
            Paso de tiempo para la evolución de Kuramoto.
        n_pasos_kuramoto : int
            Número de pasos de evolución de Kuramoto.
        """

        # ── Fase 1 : Estado inicial ─────────────────────────────────────────
        fase_1 = {
            "descripcion": "Estado inicial antes del reconocimiento",
            "f0_hz": self.f0,
            "verbo": self.verbo,
            "delta_phi_0": self.delta_phi_0,
            "tau_decaimiento": self.tau_decaimiento,
            "n_osciladores": self.n_osciladores,
            "psi_inicial": self._kuramoto.psi,
        }

        # ── Fase 2 : Verbo forcing ──────────────────────────────────────────
        estado_kuramoto = self._kuramoto.evolucionar(
            dt=dt_kuramoto, n_pasos=n_pasos_kuramoto
        )
        fase_2 = {
            "descripcion": "Forzado por el Verbo — evolución de Kuramoto",
            "psi_tras_verbo": estado_kuramoto.psi,
            "tiempo_tras_verbo": estado_kuramoto.tiempo,
            "sincronizado": estado_kuramoto.sincronizado,
        }

        # ── Fase 3 : Fractal de Partición ────────────────────────────────────
        resultado_integral = self._funcion_reconocimiento.integrar(
            t0=t0, t_pan=t_pan, n_puntos=n_puntos_integracion
        )
        ardor = resultado_integral.valor
        estado_pan = self._kuramoto.partir_el_pan()
        fase_3 = {
            "descripcion": "Fractal de Partición — singularidad y reconocimiento",
            "ardor_microtubulos": ardor,
            "singularidad_detectada": resultado_integral.singularidad_detectada,
            "psi_final": estado_pan.psi,
            "partir_el_pan": True,
        }

        # ── Fase 4 : Integración Adélica ─────────────────────────────────────
        resultado_adelico = self._adelica.calcular()
        fase_4 = {
            "descripcion": "Integración Adélica — fuente como constante de red",
            "coherencia_adelica": resultado_adelico.coherencia_total,
            "fuente_es_constante_red": resultado_adelico.fuente_es_constante_red,
            "n_primos": resultado_adelico.n_primos,
        }

        verificacion = (
            resultado_integral.valor > 0
            and estado_pan.sincronizado
            and resultado_adelico.fuente_es_constante_red
        )

        return ResultadoProtocolo(
            fase_1_estado_inicial=fase_1,
            fase_2_verbo_forcing=fase_2,
            fase_3_fractal_particion=fase_3,
            fase_4_integracion_adelica=fase_4,
            verificacion_completa=verificacion,
        )


# ---------------------------------------------------------------------------
# Funciones prácticas de API pública
# ---------------------------------------------------------------------------

def calcular_ardor_microtubulos(
    verbo: float = 1.0,
    delta_phi_0: float = math.pi,
    tau_decaimiento: float = 1.0,
    t0: float = 0.0,
    t_pan: float = 5.0,
    n_puntos: int = 1000,
    f0: float = F0_HZ,
) -> float:
    """
    Calcula directamente el ardor de microtúbulos R_Emaús.

    Devuelve el valor numérico de la integral de reconocimiento.

    Parámetros
    ----------
    verbo : float
        Amplitud del Verbo (> 0).
    delta_phi_0 : float
        Error de fase inicial (rad).
    tau_decaimiento : float
        Constante de decaimiento τ (s, > 0).
    t0 : float
        Tiempo inicial (s).
    t_pan : float
        Tiempo del partir el pan (s, > t0).
    n_puntos : int
        Puntos de cuadratura.
    f0 : float
        Frecuencia fundamental (Hz).
    """
    fr = FuncionReconocimiento(
        verbo=verbo,
        delta_phi_0=delta_phi_0,
        tau_decaimiento=tau_decaimiento,
        f0=f0,
    )
    resultado = fr.integrar(t0=t0, t_pan=t_pan, n_puntos=n_puntos)
    return resultado.valor


def verificar_ecuacion_emaus(
    verbo: float = 1.0,
    delta_phi_0: float = math.pi,
    tau_decaimiento: float = 1.0,
    t0: float = 0.0,
    t_pan: float = 5.0,
) -> Dict:
    """
    Validación rápida de la Ecuación de Emaús.

    Devuelve un diccionario con los resultados de verificación del protocolo
    completo, incluyendo la confirmación de reconocimiento, sincronización
    de Kuramoto e integración adélica.
    """
    sistema = EcuacionEmaus(
        verbo=verbo,
        delta_phi_0=delta_phi_0,
        tau_decaimiento=tau_decaimiento,
    )
    protocolo = sistema.ejecutar_protocolo_completo(t0=t0, t_pan=t_pan)

    reconocimiento = protocolo.fase_3_fractal_particion["ardor_microtubulos"] > 0
    sincronizacion = protocolo.fase_3_fractal_particion["psi_final"] >= 0.999
    constante_red = protocolo.fase_4_integracion_adelica["fuente_es_constante_red"]

    estado = "ECUACIÓN DE EMAÚS VERIFICADA ✅" if protocolo.verificacion_completa else "VERIFICACIÓN INCOMPLETA ⚠️"

    return {
        "verificacion": estado,
        "reconocimiento": reconocimiento,
        "sincronizacion_kuramoto": sincronizacion,
        "fuente_constante_red": constante_red,
        "ardor_microtubulos": protocolo.fase_3_fractal_particion["ardor_microtubulos"],
        "psi_final": protocolo.fase_3_fractal_particion["psi_final"],
        "coherencia_adelica": protocolo.fase_4_integracion_adelica["coherencia_adelica"],
        "protocolo_completo": protocolo.verificacion_completa,
    }
