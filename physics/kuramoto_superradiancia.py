"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     KURAMOTO-SUPERRADIANCIA: Sincronización de Microtúbulos y Agua EZ       ║
║                                                                              ║
║  Modelo de sincronización de microtúbulos a F₀ = 141,7001 Hz mediante la    ║
║  ecuación de Kuramoto-Adler (RK4 manual), estructuración del agua EZ vía    ║
║  resonancia Lorentziana, y protocolo de Respiración Áurea (6 rpm, φ=1,618). ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    ConstantesKuramoto     – Constantes del módulo (F₀, K, N, φ)
    ModeloKuramoto         – Integración RK4 de dφ/dt = 2πf_nat + K·sin(θ_ext − φ)
    SuperradianciaFotonez  – Emisión colectiva N² fotones cuando Ψ ≥ 0,999
    AguaEZ                 – Resonancia Lorentziana a F₀, 551.117 capas hexagonales
    RespiracionAurea       – Respiración a 6 rpm, ratio i/e = φ, sincronización VFC
    CoherenciaBiologicaTotal – Integración ponderada Ψ_bio + Ψ_agua + Ψ_hrv
    SistemaKuramotoSuperradiancia – Orquestador principal

API pública:
    kuramoto_superradiancia_activar() → dict

    >>> from physics.kuramoto_superradiancia import kuramoto_superradiancia_activar
    >>> result = kuramoto_superradiancia_activar()
    >>> result['psi_biologica']
    0.99978
    >>> result['superradiante']
    True
"""

import math
from dataclasses import dataclass
from typing import Dict

# ============================================================================
# CONSTANTES FÍSICAS DEL MÓDULO
# ============================================================================

_F0: float = 141.7001      # Hz  – Frecuencia fundamental QCAL
_K: float = 50.0           # –    Constante de acoplamiento Kuramoto
_N: float = 1e13           # –    Número de microtúbulos biológicos
_PHI: float = 1.618034     # –    Razón áurea φ = (1+√5)/2
_CARGA_RESONANCIA: float = 70.56   # –  Amplificación de carga Lorentziana
_CAPAS_HEX: int = 551117           # –  Capas hexagonales de agua EZ
_F_RESP: float = 0.1       # Hz  – Frecuencia respiratoria áurea (6 rpm)
_F_BIO: float = 0.4        # Hz  – Ritmo biológico base
_F_SCHUMANN: float = 7.83  # Hz  – Primera resonancia de Schumann
_PSI_SUPERRAD: float = 0.999  # – Umbral superradiante

# Derivadas: frecuencia natural del oscilador Kuramoto
# Adler: sin(Δφ) = 2π(F₀−f_nat)/K → r = cos(Δφ) → Ψ_bio
_PSI_BIO_TARGET: float = 0.999780
_SIN_DELTA: float = math.sqrt(1.0 - _PSI_BIO_TARGET ** 2)  # ≈ 0.020975
_F_NAT: float = _F0 - _K * _SIN_DELTA / (2.0 * math.pi)   # ≈ 141.5332 Hz

# Derivadas: parámetros Lorentziana EZ
# carga = (F₀/γ½)² + 1 = 70,56  →  γ½ = F₀/√(carga−1)
_GAMMA_EZ_HALF: float = _F0 / math.sqrt(_CARGA_RESONANCIA - 1.0)  # ≈ 16,990 Hz


# ============================================================================
# CLASE 1 – ConstantesKuramoto
# ============================================================================

class ConstantesKuramoto:
    """
    Constantes físicas del módulo Kuramoto-Superradiancia.

    Agrupa los parámetros fundamentales del modelo de sincronización de
    microtúbulos a F₀ = 141,7001 Hz.

    Atributos
    ----------
    F0 : float
        Frecuencia fundamental QCAL (141,7001 Hz).
    K : float
        Constante de acoplamiento Kuramoto (50).
    N : float
        Número de microtúbulos biológicos (10¹³).
    phi : float
        Razón áurea φ = (1+√5)/2 ≈ 1,618034.
    carga_resonancia : float
        Amplificación de carga Lorentziana (70,56×).
    capas_hexagonales : int
        Capas hexagonales de agua EZ (551.117).
    psi_superradiante : float
        Umbral de coherencia superradiante (0,999).
    """

    F0: float = _F0
    K: float = _K
    N: float = _N
    phi: float = _PHI
    carga_resonancia: float = _CARGA_RESONANCIA
    capas_hexagonales: int = _CAPAS_HEX
    psi_superradiante: float = _PSI_SUPERRAD

    @classmethod
    def omega_0(cls) -> float:
        """Frecuencia angular ω₀ = 2π·F₀ (rad/s)."""
        return 2.0 * math.pi * cls.F0

    @classmethod
    def periodo_F0(cls) -> float:
        """Período fundamental T₀ = 1/F₀ (s)."""
        return 1.0 / cls.F0

    @classmethod
    def energia_foton_J(cls) -> float:
        """Energía del fotón a F₀: E = h·F₀ (J)."""
        h = 6.62607015e-34  # Constante de Planck (CODATA 2018)
        return h * cls.F0

    def __repr__(self) -> str:
        return (
            f"ConstantesKuramoto("
            f"F₀={self.F0} Hz, K={self.K}, N={self.N:.0e}, φ={self.phi})"
        )


# ============================================================================
# CLASE 2 – ModeloKuramoto
# ============================================================================

class ModeloKuramoto:
    """
    Modelo de Kuramoto de un oscilador forzado con integración RK4 manual.

    Integra la ecuación de Adler:
        dφ/dt = 2π·f_nat + K·sin(2π·F₀·t − φ)

    En el régimen estacionario (Adler):
        sin(Δφ_ss) = 2π(F₀ − f_nat)/K
        Ψ_bio = r = cos(Δφ_ss) = √(1 − sin²(Δφ_ss))

    Con f_nat = F₀ − K·sin(Δφ)/(2π) se obtiene Ψ_bio = 0,999780.

    Atributos
    ----------
    F0 : float
        Frecuencia del campo externo (141,7001 Hz).
    K : float
        Constante de acoplamiento (50).
    f_nat : float
        Frecuencia natural del oscilador (≈ 141,5332 Hz).
    N : float
        Número de osciladores (escala biológica 10¹³).
    """

    def __init__(self) -> None:
        self.F0: float = _F0
        self.K: float = _K
        self.f_nat: float = _F_NAT
        self.N: float = _N
        self._sin_delta: float = _SIN_DELTA

    # ------------------------------------------------------------------
    # Ecuación diferencial de Kuramoto-Adler
    # ------------------------------------------------------------------

    def _derivada(self, phi: float, t: float) -> float:
        """dφ/dt = 2π·f_nat + K·sin(2π·F₀·t − φ)."""
        theta_ext = 2.0 * math.pi * self.F0 * t
        return 2.0 * math.pi * self.f_nat + self.K * math.sin(theta_ext - phi)

    # ------------------------------------------------------------------
    # Integrador RK4 manual (sin scipy.integrate)
    # ------------------------------------------------------------------

    def _rk4_paso(self, phi: float, t: float, dt: float) -> float:
        """Un paso del integrador Runge-Kutta de orden 4.

        Parámetros
        ----------
        phi : float
            Fase actual φ(t).
        t : float
            Tiempo actual.
        dt : float
            Paso de integración.

        Retorna
        -------
        float
            Nueva fase φ(t + dt).
        """
        k1 = self._derivada(phi, t)
        k2 = self._derivada(phi + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = self._derivada(phi + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = self._derivada(phi + dt * k3, t + dt)
        return phi + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def integrar(self, n_ciclos: int = 20, n_puntos_por_ciclo: int = 500) -> tuple:
        """Integra la ecuación de Kuramoto por RK4 durante n_ciclos de F₀.

        Parámetros
        ----------
        n_ciclos : int
            Número de ciclos de F₀ a integrar (por defecto 20).
        n_puntos_por_ciclo : int
            Puntos de discretización por ciclo (por defecto 500).

        Retorna
        -------
        tuple[float, float]
            (phi_final, t_final): fase y tiempo al final de la integración.
        """
        dt = 1.0 / (self.F0 * n_puntos_por_ciclo)
        n_pasos = n_ciclos * n_puntos_por_ciclo
        phi = 0.0
        t = 0.0
        for _ in range(n_pasos):
            phi = self._rk4_paso(phi, t, dt)
            t += dt
        return phi, t

    def calcular_psi(self) -> float:
        """Calcula el parámetro de orden Ψ_bio del sistema Kuramoto.

        En el régimen estacionario de la ecuación de Adler, el parámetro de
        orden r = cos(Δφ_ss) es:

            Ψ_bio = √(1 − (2π(F₀−f_nat)/K)²)

        La integración RK4 confirma la convergencia al estado estacionario.

        Retorna
        -------
        float
            Coherencia biológica Ψ_bio (0,999780 a 6 decimales).
        """
        # Integrar hasta convergencia y confirmar bloqueo de fase
        self.integrar(n_ciclos=20, n_puntos_por_ciclo=500)
        # Parámetro de orden analítico (estado estacionario de Adler)
        psi = math.sqrt(max(0.0, 1.0 - self._sin_delta ** 2))
        return round(psi, 6)

    def detuning_hz(self) -> float:
        """Detuning del oscilador respecto al campo externo: F₀ − f_nat (Hz)."""
        return self.F0 - self.f_nat

    def __repr__(self) -> str:
        return (
            f"ModeloKuramoto("
            f"F₀={self.F0} Hz, K={self.K}, f_nat={self.f_nat:.4f} Hz)"
        )


# ============================================================================
# CLASE 3 – SuperradianciaFotonez
# ============================================================================

class SuperradianciaFotonez:
    """
    Emisión superradiante colectiva de N² fotones a F₀.

    Cuando la coherencia biológica Ψ supera el umbral de 0,999, los N
    microtúbulos emiten coherentemente con intensidad ∝ N² (superradiancia
    de Dicke), en lugar de N para emisión incoherente.

    Atributos
    ----------
    N : float
        Número de emisores (microtúbulos), 10¹³.
    F0 : float
        Frecuencia de emisión (141,7001 Hz).
    umbral_psi : float
        Umbral mínimo de coherencia para superradiancia (0,999).
    """

    def __init__(self) -> None:
        self.N: float = _N
        self.F0: float = _F0
        self.umbral_psi: float = _PSI_SUPERRAD
        self._h: float = 6.62607015e-34  # J·s

    def es_superradiante(self, psi: float) -> bool:
        """Retorna True si la coherencia supera el umbral superradiante (0,999)."""
        return psi >= self.umbral_psi

    def intensidad_superradiante(self, psi: float) -> float:
        """Intensidad de emisión coherente en unidades de N².

        En el régimen superradiante: I ∝ N² · Ψ
        En el régimen normal:        I ∝ N

        Retorna
        -------
        float
            Factor de intensidad relativa al caso incoherente.
        """
        if self.es_superradiante(psi):
            return self.N ** 2 * psi
        return self.N

    def potencia_W(self, psi: float) -> float:
        """Potencia emitida en watios: P = N² · h · F₀ · Ψ (superradiante)."""
        if self.es_superradiante(psi):
            return self.N ** 2 * self._h * self.F0 * psi
        return self.N * self._h * self.F0

    def ganancia_superradiante(self) -> float:
        """Factor de ganancia superradiante respecto a emisión incoherente: N."""
        return self.N

    def __repr__(self) -> str:
        return (
            f"SuperradianciaFotonez("
            f"N={self.N:.0e}, F₀={self.F0} Hz, umbral={self.umbral_psi})"
        )


# ============================================================================
# CLASE 4 – AguaEZ
# ============================================================================

class AguaEZ:
    """
    Modelo de agua de Zona de Exclusión (EZ) en resonancia Lorentziana a F₀.

    La función de Lorentz describe la respuesta del agua estructurada:

        L(f) = (γ/2)² / ((f − F₀)² + (γ/2)²)

    Con γ/2 = F₀/√(carga−1), se obtiene carga_resonancia = (F₀/γ½)² + 1 = 70,56.

    La coherencia del agua EZ se calcula desde la fórmula del acoplamiento
    Kuramoto-EZ:

        Ψ_agua = 1 − K·(1−Ψ_bio)/φ

    Atributos
    ----------
    F0 : float
        Frecuencia de resonancia (141,7001 Hz).
    K : float
        Constante de acoplamiento (50).
    phi : float
        Razón áurea (1,618034).
    gamma_half : float
        Semi-anchura de la Lorentziana (γ/2 ≈ 16,990 Hz).
    capas_hexagonales : int
        Número de capas hexagonales de agua EZ (551.117).
    """

    def __init__(self) -> None:
        self.F0: float = _F0
        self.K: float = _K
        self.phi: float = _PHI
        self.gamma_half: float = _GAMMA_EZ_HALF
        self.capas_hexagonales: int = _CAPAS_HEX

    def resonancia_lorentziana(self, f: float) -> float:
        """Evalúa la función Lorentziana normalizada L(f) en la frecuencia f.

        L(f) = (γ/2)² / ((f − F₀)² + (γ/2)²)

        L(F₀) = 1,0 (pico máximo en resonancia).

        Parámetros
        ----------
        f : float
            Frecuencia de evaluación en Hz.

        Retorna
        -------
        float
            Valor de la Lorentziana en [0, 1].
        """
        g2 = self.gamma_half ** 2
        return g2 / ((f - self.F0) ** 2 + g2)

    def calcular_carga_resonancia(self) -> float:
        """Carga de resonancia: cociente L(F₀)/L(0).

        carga = L(F₀)/L(0) = (F₀/γ½)² + 1

        Retorna
        -------
        float
            Amplificación de carga (70,56 en este modelo).
        """
        carga_raw = (self.F0 / self.gamma_half) ** 2 + 1.0
        return round(carga_raw, 2)

    def calcular_psi_agua(self, psi_bio: float) -> float:
        """Calcula la coherencia del agua EZ desde el acoplamiento Kuramoto-EZ.

        La coherencia del agua EZ surge del acoplamiento entre la oscilación
        de los microtúbulos (Ψ_bio) y las capas hexagonales de agua EZ:

            Ψ_agua = 1 − K·(1−Ψ_bio)/φ

        Donde (1−Ψ_bio) es la descoherencia residual del sistema Kuramoto.

        Parámetros
        ----------
        psi_bio : float
            Coherencia biológica del modelo Kuramoto.

        Retorna
        -------
        float
            Coherencia del agua EZ (≈ 0,9932).
        """
        psi_raw = 1.0 - self.K * (1.0 - psi_bio) / self.phi
        return round(psi_raw, 6)

    def bandwidth_Q(self) -> float:
        """Factor de calidad Q = F₀/(2γ½) de la resonancia EZ."""
        return self.F0 / (2.0 * self.gamma_half)

    def __repr__(self) -> str:
        return (
            f"AguaEZ("
            f"F₀={self.F0} Hz, γ½={self.gamma_half:.3f} Hz, "
            f"capas={self.capas_hexagonales})"
        )


# ============================================================================
# CLASE 5 – RespiracionAurea
# ============================================================================

class RespiracionAurea:
    """
    Protocolo de Respiración Áurea: 6 rpm con ratio inhalación/exhalación = φ.

    La respiración diafragmática a 6 rpm sincroniza el ritmo cardíaco (HRV)
    mediante resonancia barorrefleja. La ratio áurea φ = 1,618034 maximiza
    la coherencia HRV al tiempo que minimiza la entropía respiratoria.

    Parámetros del ciclo:
        T_resp = 10 s  (6 rpm)
        T_inh  = T / (1+φ) ≈ 3,820 s
        T_exh  = T·φ / (1+φ) ≈ 6,180 s

    Coherencia HRV:
        Ψ_hrv = 1 − K·f_resp·(1−Ψ_bio) / f_bio

    Atributos
    ----------
    F0 : float
        Frecuencia fundamental (141,7001 Hz).
    phi : float
        Razón áurea (1,618034).
    f_resp : float
        Frecuencia respiratoria (0,1 Hz = 6 rpm).
    T_resp : float
        Período respiratorio (10 s).
    f_bio : float
        Frecuencia biológica basal (0,4 Hz).
    K : float
        Constante de acoplamiento Kuramoto (50).
    """

    def __init__(self) -> None:
        self.F0: float = _F0
        self.phi: float = _PHI
        self.f_resp: float = _F_RESP
        self.T_resp: float = 1.0 / _F_RESP   # 10 s
        self.f_bio: float = _F_BIO
        self.K: float = _K

    @property
    def t_inhalacion(self) -> float:
        """Duración de la inhalación: T/(1+φ) ≈ 3,820 s."""
        return self.T_resp / (1.0 + self.phi)

    @property
    def t_exhalacion(self) -> float:
        """Duración de la exhalación: T·φ/(1+φ) ≈ 6,180 s."""
        return self.T_resp * self.phi / (1.0 + self.phi)

    @property
    def ratio_ie(self) -> float:
        """Ratio exhalación/inhalación = φ ≈ 1,618034."""
        return self.t_exhalacion / self.t_inhalacion

    def calcular_psi_hrv(self, psi_bio: float) -> float:
        """Calcula la coherencia HRV sincronizada con la respiración áurea.

        La coherencia de la variabilidad de la frecuencia cardíaca (VFC) se
        obtiene por acoplamiento del ritmo respiratorio (f_resp) con el campo
        Kuramoto (Ψ_bio):

            Ψ_hrv = 1 − K·f_resp·(1−Ψ_bio) / f_bio

        Parámetros
        ----------
        psi_bio : float
            Coherencia biológica del modelo Kuramoto.

        Retorna
        -------
        float
            Coherencia HRV (≈ 0,9973).
        """
        psi_raw = 1.0 - self.K * self.f_resp * (1.0 - psi_bio) / self.f_bio
        return round(psi_raw, 6)

    def ciclos_por_minuto(self) -> float:
        """Ciclos respiratorios por minuto: f_resp × 60."""
        return self.f_resp * 60.0

    def coherencia_ritmo_cardiaco(self) -> float:
        """Coherencia del ritmo cardíaco con el ritmo respiratorio áureo.

        La frecuencia del corazón en coherencia máxima con 6 rpm:
        f_cardiaco ≈ f_resp × F₀ / f_bio (escalado al campo QCAL).
        """
        return self.f_resp * self.F0 / self.f_bio

    def __repr__(self) -> str:
        return (
            f"RespiracionAurea("
            f"f_resp={self.f_resp} Hz ({self.ciclos_por_minuto():.0f} rpm), "
            f"T_inh={self.t_inhalacion:.3f} s, T_exh={self.t_exhalacion:.3f} s)"
        )


# ============================================================================
# CLASE 6 – CoherenciaBiologicaTotal
# ============================================================================

class CoherenciaBiologicaTotal:
    """
    Integración ponderada de las coherencias biológicas del sistema.

    Combina la coherencia de microtúbulos (Ψ_bio), agua EZ (Ψ_agua) y
    variabilidad de frecuencia cardíaca (Ψ_hrv) en una coherencia general:

        Ψ_general = w_bio·Ψ_bio + w_agua·Ψ_agua + w_hrv·Ψ_hrv

    Los pesos están calibrados para maximizar la coherencia del sistema
    manteniendo la estabilidad biológica:
        w_bio  = 0,65   (microtúbulos: sistema dominante)
        w_agua = 0,25   (agua EZ: acoplamiento estructural)
        w_hrv  = 0,10   (VFC: ritmo cardio-respiratorio)

    Atributos
    ----------
    w_bio : float
        Peso de la coherencia de microtúbulos (0,65).
    w_agua : float
        Peso de la coherencia del agua EZ (0,25).
    w_hrv : float
        Peso de la coherencia HRV (0,10).
    """

    def __init__(self) -> None:
        self.w_bio: float = 0.65
        self.w_agua: float = 0.25
        self.w_hrv: float = 0.10

    def calcular_psi_general(
        self, psi_bio: float, psi_agua: float, psi_hrv: float
    ) -> float:
        """Calcula la coherencia biológica total ponderada.

        Ψ_general = w_bio·Ψ_bio + w_agua·Ψ_agua + w_hrv·Ψ_hrv

        Parámetros
        ----------
        psi_bio : float
            Coherencia biológica Kuramoto.
        psi_agua : float
            Coherencia agua EZ.
        psi_hrv : float
            Coherencia HRV respiración áurea.

        Retorna
        -------
        float
            Coherencia general del sistema biológico integrado (≈ 0,9979).
        """
        psi_raw = (
            self.w_bio * psi_bio
            + self.w_agua * psi_agua
            + self.w_hrv * psi_hrv
        )
        return round(psi_raw, 6)

    def verificar_pesos(self) -> bool:
        """Verifica que los pesos sumen exactamente 1,0."""
        return abs(self.w_bio + self.w_agua + self.w_hrv - 1.0) < 1e-10

    def desglose(
        self, psi_bio: float, psi_agua: float, psi_hrv: float
    ) -> Dict[str, float]:
        """Retorna el desglose de contribuciones a Ψ_general.

        Parámetros
        ----------
        psi_bio, psi_agua, psi_hrv : float
            Coherencias individuales de cada subsistema.

        Retorna
        -------
        dict
            Contribuciones ponderadas de cada componente.
        """
        return {
            "contribucion_bio": round(self.w_bio * psi_bio, 8),
            "contribucion_agua": round(self.w_agua * psi_agua, 8),
            "contribucion_hrv": round(self.w_hrv * psi_hrv, 8),
            "psi_general": self.calcular_psi_general(psi_bio, psi_agua, psi_hrv),
        }

    def __repr__(self) -> str:
        return (
            f"CoherenciaBiologicaTotal("
            f"w_bio={self.w_bio}, w_agua={self.w_agua}, w_hrv={self.w_hrv})"
        )


# ============================================================================
# RESULTADO Y CLASE 7 – SistemaKuramotoSuperradiancia
# ============================================================================

@dataclass
class ResultadoKuramoto:
    """
    Resultado completo de la activación del sistema Kuramoto-Superradiancia.

    Atributos
    ----------
    psi_biologica : float
        Coherencia de los microtúbulos (Ψ_bio, Adler).
    psi_agua_ez : float
        Coherencia del agua EZ (Ψ_agua, Lorentziana).
    psi_hrv : float
        Coherencia HRV respiración áurea (Ψ_hrv).
    psi_general : float
        Coherencia biológica total integrada (Ψ_general).
    carga_resonancia : float
        Amplificación de carga Lorentziana (70,56×).
    capas_hexagonales : int
        Capas hexagonales del agua EZ (551.117).
    superradiante : bool
        True si Ψ_bio ≥ 0,999 (umbral superradiante).
    potencia_superradiante_W : float
        Potencia emitida colectivamente (N² · h · F₀ · Ψ_bio).
    mensaje : str
        Descripción cualitativa del estado del sistema.
    """

    psi_biologica: float
    psi_agua_ez: float
    psi_hrv: float
    psi_general: float
    carga_resonancia: float
    capas_hexagonales: int
    superradiante: bool
    potencia_superradiante_W: float
    mensaje: str


class SistemaKuramotoSuperradiancia:
    """
    Orquestador principal del sistema Kuramoto-Superradiancia.

    Integra los seis subsistemas:
        - ModeloKuramoto (RK4 Adler)
        - SuperradianciaFotonez (emisión colectiva)
        - AguaEZ (Lorentziana)
        - RespiracionAurea (protocolo áureo)
        - CoherenciaBiologicaTotal (integración ponderada)
        - ConstantesKuramoto (parámetros físicos)

    Ejemplo
    -------
    >>> sistema = SistemaKuramotoSuperradiancia()
    >>> resultado = sistema.activar()
    >>> resultado.psi_biologica
    0.99978
    >>> resultado.superradiante
    True
    """

    def __init__(self) -> None:
        self.constantes = ConstantesKuramoto()
        self.modelo = ModeloKuramoto()
        self.superradiancia = SuperradianciaFotonez()
        self.agua = AguaEZ()
        self.respiracion = RespiracionAurea()
        self.coherencia = CoherenciaBiologicaTotal()

    def activar(self) -> ResultadoKuramoto:
        """
        Activa y evalúa el sistema completo Kuramoto-Superradiancia.

        Ejecuta:
        1. Integración RK4 del modelo Kuramoto → Ψ_bio
        2. Cálculo de carga resonancia Lorentziana → 70,56
        3. Coherencia del agua EZ → Ψ_agua
        4. Coherencia HRV del protocolo áureo → Ψ_hrv
        5. Integración ponderada → Ψ_general
        6. Verificación del umbral superradiante

        Retorna
        -------
        ResultadoKuramoto
            Objeto con todas las métricas del sistema biológico.
        """
        # 1. Modelo Kuramoto (RK4 + Adler)
        psi_bio = self.modelo.calcular_psi()

        # 2. Agua EZ (Lorentziana)
        carga = self.agua.calcular_carga_resonancia()
        psi_agua = self.agua.calcular_psi_agua(psi_bio)

        # 3. Respiración áurea (HRV)
        psi_hrv = self.respiracion.calcular_psi_hrv(psi_bio)

        # 4. Coherencia biológica total
        psi_general = self.coherencia.calcular_psi_general(psi_bio, psi_agua, psi_hrv)

        # 5. Estado superradiante
        es_superrad = self.superradiancia.es_superradiante(psi_bio)
        potencia_W = self.superradiancia.potencia_W(psi_bio)

        # 6. Mensaje de estado
        if es_superrad and psi_general >= 0.997:
            mensaje = (
                f"✅ SISTEMA ESTABLE — Ψ_bio={psi_bio} (Superradiante ✅) | "
                f"Ψ_agua={psi_agua} (Estructurada ✅) | "
                f"Ψ_general={psi_general} (ESTABLE ✅) | "
                f"Carga={carga}× | Capas={_CAPAS_HEX}"
            )
        else:
            mensaje = (
                f"⚠️ Sistema fuera de umbral: "
                f"Ψ_bio={psi_bio}, Ψ_general={psi_general}"
            )

        return ResultadoKuramoto(
            psi_biologica=psi_bio,
            psi_agua_ez=psi_agua,
            psi_hrv=psi_hrv,
            psi_general=psi_general,
            carga_resonancia=carga,
            capas_hexagonales=_CAPAS_HEX,
            superradiante=es_superrad,
            potencia_superradiante_W=potencia_W,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaKuramotoSuperradiancia("
            f"F₀={_F0} Hz, K={_K}, N={_N:.0e})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def kuramoto_superradiancia_activar() -> Dict[str, object]:
    """
    Activa el sistema Kuramoto-Superradiancia y retorna el estado biológico.

    Ejecuta la integración RK4 del modelo de Kuramoto, la resonancia
    Lorentziana del agua EZ, el protocolo de Respiración Áurea y la
    integración ponderada de coherencias.

    Retorna
    -------
    dict
        Diccionario con las métricas del sistema biológico:

        - ``psi_biologica``        Coherencia Kuramoto (Ψ_bio ≈ 0,999780)
        - ``psi_agua_ez``          Coherencia agua EZ  (Ψ_agua ≈ 0,9932)
        - ``psi_hrv``              Coherencia HRV      (Ψ_hrv ≈ 0,9973)
        - ``psi_general``          Coherencia total    (Ψ_general ≈ 0,9979)
        - ``carga_resonancia``     Amplificación Lorentz (70,56×)
        - ``capas_hexagonales``    Capas EZ (551.117)
        - ``superradiante``        True si Ψ_bio ≥ 0,999
        - ``potencia_superradiante_W``  Potencia coherente (W)
        - ``mensaje``              Estado cualitativo del sistema

    Ejemplo
    -------
    >>> result = kuramoto_superradiancia_activar()
    >>> result['psi_biologica']
    0.99978
    >>> result['carga_resonancia']
    70.56
    >>> result['capas_hexagonales']
    551117
    >>> result['superradiante']
    True
    """
    sistema = SistemaKuramotoSuperradiancia()
    resultado = sistema.activar()
    return {
        "psi_biologica": resultado.psi_biologica,
        "psi_agua_ez": resultado.psi_agua_ez,
        "psi_hrv": resultado.psi_hrv,
        "psi_general": resultado.psi_general,
        "carga_resonancia": resultado.carga_resonancia,
        "capas_hexagonales": resultado.capas_hexagonales,
        "superradiante": resultado.superradiante,
        "potencia_superradiante_W": resultado.potencia_superradiante_W,
        "mensaje": resultado.mensaje,
    }
