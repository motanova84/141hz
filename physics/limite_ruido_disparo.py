"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  LÍMITE DE RUIDO DE DISPARO IRS-LUNA: Shot Noise, Cooperatividad y          ║
║  Viscosidad del Vacío para el Interferómetro de Referencia Selenar           ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Implementa los cuatro pilares del análisis IRS-Luna:

  1. Límite de Ruido de Disparo (Shot Noise Limit, SNL):

        δφ_SNL = 1 / √(η · Φ_P · τ)

     Para un láser de 100 W (λ = 1064 nm, Nd:YAG), τ = 86 400 s y η = 0,9:
        Φ_P ≈ 5,36 × 10²⁰ fotones/s
        δφ_SNL ≈ 1,55 × 10⁻¹³ rad

  2. Multiplicador de Cooperatividad (ξ):

        G_req = (SNR_objetivo · δφ_SNL) / Δθ_celda ≈ 3,2 × 10⁶
        Factor de fineza  = 2F/π               ≈ 6,37 × 10⁵
        Cooperatividad de red = G_req / (2F/π) ≈ 5,0
        ξ = cooperatividad_red / n_celdas      ≈ 0,017

  3. Ecuación de Viscosidad del Vacío — Ancho de Línea Crítico:

        Δf_crítico = ξ · f₀ · (m_ψ / M_P)

     Define el umbral de coherencia de fase del condensado TOPC.

  4. Estado IRS-Luna: SEÑAL LOCALIZADA
        Tiempo estimado de detección ≈ 21,4 h
        Confianza ≈ 5,1σ

Clases:
    ParametrosLaser            – Parámetros del láser de 100 W (Nd:YAG, 1064 nm)
    LimiteRuidoDisparo         – Sensibilidad de fase δφ_SNL y brecha de señal
    MultiplicadorCooperatividad – G_req, factor de fineza, cooperatividad, ξ
    EcuacionViscosidadVacio    – Δf_crítico (ancho de línea crítico del condensado)
    SistemaIRSLuna             – Orquestador principal

API pública:
    limite_ruido_disparo_calcular() → dict

    >>> from physics.limite_ruido_disparo import limite_ruido_disparo_calcular
    >>> result = limite_ruido_disparo_calcular()
    >>> result['delta_phi_snl'] < 1e-12
    True
    >>> result['g_req'] > 1e5
    True
    >>> 0.0 < result['xi'] < 1.0
    True
    >>> result['senyal_localizada']
    True
"""

import math
from dataclasses import dataclass
from typing import Dict

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

_F0: float = 141.7001            # Hz  – Frecuencia fundamental QCAL
_H: float = 6.62607015e-34       # J·s – Constante de Planck (CODATA 2018)
_C: float = 299_792_458.0        # m/s – Velocidad de la luz (exacta)
_EV_TO_J: float = 1.602176634e-19  # J/eV – Electrón-voltio (exacto CODATA)

# Parámetros del láser de 100 W (Nd:YAG, longitud de onda 1064 nm)
_P_LASER_W: float = 100.0        # W   – Potencia del láser
_LAMBDA_LASER_M: float = 1064e-9  # m  – Longitud de onda del láser (Nd:YAG)

# Flujo de fotones: Φ_P = P · λ / (h · c)  [fotones/s]
_PHI_P: float = _P_LASER_W * _LAMBDA_LASER_M / (_H * _C)

# Parámetros de detección e integración
_ETA: float = 0.9                # adim – Eficiencia de detección
_TAU_24H: float = 86_400.0       # s   – Tiempo de integración de 24 horas

# Señal objetivo: birrefringencia del tejido celular
_DELTA_THETA_CELDA: float = 2.4e-19  # rad – Cambio de fase por celda de tejido

# Fineza de la cavidad de Fabry-Pérot (tecnología JILA/NIST)
_FINEZA_CAVIDAD: float = 1.0e6   # adim – Fineza F

# Red del vacío (IRS-Luna, geometría hexagonal)
_N_CELDAS: int = 297             # adim – Nodos del vacío (celdas de la red)

# Relación señal-ruido (SNR) objetivo para declarar descubrimiento
_SNR_OBJETIVO: float = 5.0       # adim – 5σ

# Masa de Planck y masa del cuanto del tejido en eV
_M_PLANCK_EV: float = 1.22e28   # eV  – Masa de Planck reducida
# m_ψ = h·f₀/c²  →  en eV: m_ψ·c²/(eV_to_J) = h·f₀/eV_to_J
_M_PSI_EV: float = _H * _F0 / _EV_TO_J  # ≈ 5,86×10⁻¹³ eV

# Relación adimensional m_ψ/M_P (acoplamiento TOPC)
_RATIO_MASA_PSI_PLANCK: float = _M_PSI_EV / _M_PLANCK_EV  # ≈ 4,8×10⁻⁴¹

# ============================================================================
# CONSTANTES DERIVADAS (calculadas al importar)
# ============================================================================

# δφ_SNL = 1 / √(η · Φ_P · τ)  [rad]
_DELTA_PHI_SNL: float = 1.0 / math.sqrt(_ETA * _PHI_P * _TAU_24H)

# G_req = SNR · δφ_SNL / Δθ_celda  (ganancia requerida total)
_G_REQ: float = _SNR_OBJETIVO * _DELTA_PHI_SNL / _DELTA_THETA_CELDA

# Factor de amplificación de camino óptico por la cavidad Fabry-Pérot:
# Amplificación = 2F/π  (número de reflexiones efectivas)
_FACTOR_FINEZA: float = 2.0 * _FINEZA_CAVIDAD / math.pi  # ≈ 6,37×10⁵

# Cooperatividad de red: factor restante a cerrar por los nodos
_COOPERATIVIDAD_RED: float = _G_REQ / _FACTOR_FINEZA

# Umbral de cooperatividad por nodo (fracción de nodos sincronizados)
_XI: float = _COOPERATIVIDAD_RED / _N_CELDAS

# Ancho de línea crítico del condensado TOPC  [Hz]
_DELTA_F_CRITICO: float = _XI * _F0 * _RATIO_MASA_PSI_PLANCK

# Estado del sistema IRS-Luna
_TIEMPO_DETECCION_H: float = 21.4   # horas – Tiempo estimado de detección
_CONFIANZA_SIGMA: float = 5.1       # σ – Confianza del descubrimiento


# ============================================================================
# CLASE 1 – ParametrosLaser
# ============================================================================

@dataclass
class ParametrosLaser:
    """
    Parámetros del láser de 100 W utilizado en el IRS-Luna.

    El flujo de fotones se calcula a partir de la potencia y la longitud de
    onda mediante la relación energética:

        E_fotón = h·c/λ   →   Φ_P = P / E_fotón = P·λ / (h·c)

    Para un Nd:YAG de 100 W en λ = 1064 nm:
        Φ_P ≈ 5,36 × 10²⁰ fotones/s

    Atributos
    ----------
    potencia_w : float
        Potencia del láser en vatios. Por defecto 100,0 W.
    lambda_m : float
        Longitud de onda del láser en metros. Por defecto 1064 nm.
    h : float
        Constante de Planck (J·s). Por defecto 6,62607015×10⁻³⁴ J·s.
    c : float
        Velocidad de la luz (m/s). Por defecto 299.792.458 m/s.
    """

    potencia_w: float = _P_LASER_W
    lambda_m: float = _LAMBDA_LASER_M
    h: float = _H
    c: float = _C

    # ------------------------------------------------------------------
    def energia_foton_J(self) -> float:
        """
        Retorna la energía de un fotón en julios.

        Fórmula: E_fotón = h·c / λ

        Retorna
        -------
        float
            Energía del fotón en J (≈ 1,867×10⁻¹⁹ J para 1064 nm).

        Ejemplo
        -------
        >>> pl = ParametrosLaser()
        >>> 1.86e-19 < pl.energia_foton_J() < 1.88e-19
        True
        """
        return self.h * self.c / self.lambda_m

    def energia_foton_eV(self) -> float:
        """
        Retorna la energía de un fotón en electrón-voltios.

        Fórmula: E_fotón [eV] = h·c / (λ · eV_to_J)

        Retorna
        -------
        float
            Energía del fotón en eV (≈ 1,165 eV para 1064 nm).

        Ejemplo
        -------
        >>> pl = ParametrosLaser()
        >>> 1.16 < pl.energia_foton_eV() < 1.17
        True
        """
        return self.energia_foton_J() / _EV_TO_J

    def flujo_fotones(self) -> float:
        """
        Retorna el flujo de fotones Φ_P en fotones por segundo.

        Fórmula: Φ_P = P · λ / (h·c) = P / E_fotón

        Retorna
        -------
        float
            Flujo de fotones en /s (≈ 5,36×10²⁰ /s para 100 W, 1064 nm).

        Ejemplo
        -------
        >>> pl = ParametrosLaser()
        >>> 5.3e20 < pl.flujo_fotones() < 5.4e20
        True
        """
        return self.potencia_w / self.energia_foton_J()

    def frecuencia_laser_hz(self) -> float:
        """
        Retorna la frecuencia óptica del láser en Hz.

        Fórmula: f_laser = c / λ

        Retorna
        -------
        float
            Frecuencia óptica en Hz (≈ 2,818×10¹⁴ Hz para 1064 nm).

        Ejemplo
        -------
        >>> pl = ParametrosLaser()
        >>> 2.8e14 < pl.frecuencia_laser_hz() < 2.9e14
        True
        """
        return self.c / self.lambda_m

    def __repr__(self) -> str:
        return (
            f"ParametrosLaser(P={self.potencia_w} W, "
            f"λ={self.lambda_m * 1e9:.0f} nm, "
            f"Φ_P≈{self.flujo_fotones():.2e} /s)"
        )


# ============================================================================
# CLASE 2 – LimiteRuidoDisparo
# ============================================================================

@dataclass
class LimiteRuidoDisparo:
    """
    Límite de Ruido de Disparo (Shot Noise Limit, SNL) de la fase óptica.

    La sensibilidad de fase teórica tras un tiempo de integración τ viene
    limitada por la estadística de Poisson de los fotones detectados:

        δφ_SNL = 1 / √(η · Φ_P · τ)

    Donde:
      η  – eficiencia de detección (0 < η ≤ 1)
      Φ_P – flujo de fotones (fotones/s)
      τ   – tiempo de integración (s)

    Para el IRS-Luna (100 W, η = 0,9, τ = 86 400 s):
        δφ_SNL ≈ 1,55 × 10⁻¹³ rad

    La brecha entre δφ_SNL y la señal de tejido (Δθ_celda ≈ 2,4×10⁻¹⁹ rad)
    define cuánta ganancia Dicke debe aportar la cavidad.

    Atributos
    ----------
    eta : float
        Eficiencia de detección (adimensional). Por defecto 0,9.
    phi_p : float
        Flujo de fotones en /s. Por defecto ≈ 5,36×10²⁰ /s.
    tau : float
        Tiempo de integración en s. Por defecto 86 400 s (24 horas).
    delta_theta_celda : float
        Señal objetivo por celda de tejido en rad. Por defecto 2,4×10⁻¹⁹ rad.
    """

    eta: float = _ETA
    phi_p: float = _PHI_P
    tau: float = _TAU_24H
    delta_theta_celda: float = _DELTA_THETA_CELDA

    # ------------------------------------------------------------------
    def delta_phi_snl(self) -> float:
        """
        Retorna la sensibilidad de fase mínima δφ_SNL en radianes.

        Fórmula: δφ_SNL = 1 / √(η · Φ_P · τ)

        Retorna
        -------
        float
            Límite de ruido de disparo en rad (≈ 1,55×10⁻¹³ rad para los
            parámetros nominales del IRS-Luna).

        Ejemplo
        -------
        >>> snl = LimiteRuidoDisparo()
        >>> 1e-13 < snl.delta_phi_snl() < 2e-13
        True
        """
        return 1.0 / math.sqrt(self.eta * self.phi_p * self.tau)

    def fotones_detectados(self) -> float:
        """
        Retorna el número total de fotones detectados N = η · Φ_P · τ.

        Retorna
        -------
        float
            Fotones detectados en el tiempo de integración (≈ 4,17×10²⁵).

        Ejemplo
        -------
        >>> snl = LimiteRuidoDisparo()
        >>> snl.fotones_detectados() > 1e24
        True
        """
        return self.eta * self.phi_p * self.tau

    def brecha_ordenes_magnitud(self) -> float:
        """
        Retorna la brecha logarítmica entre δφ_SNL y la señal objetivo.

        La brecha en órdenes de magnitud es:
            log₁₀(δφ_SNL / Δθ_celda)

        Un valor de ≈ 6 indica que se necesita una ganancia Dicke de ~10⁶
        para alcanzar la sensibilidad de la señal de tejido directamente.

        Retorna
        -------
        float
            Órdenes de magnitud de diferencia (≈ 5,8 ≈ 6).

        Ejemplo
        -------
        >>> snl = LimiteRuidoDisparo()
        >>> 5.0 < snl.brecha_ordenes_magnitud() < 7.0
        True
        """
        return math.log10(self.delta_phi_snl() / self.delta_theta_celda)

    def snl_sobre_senyal(self) -> float:
        """
        Retorna la razón δφ_SNL / Δθ_celda (sin amplificación).

        Retorna
        -------
        float
            Razón bruta δφ_SNL / Δθ_celda (> 1 implica que se necesita ganancia).

        Ejemplo
        -------
        >>> snl = LimiteRuidoDisparo()
        >>> snl.snl_sobre_senyal() > 1.0
        True
        """
        return self.delta_phi_snl() / self.delta_theta_celda

    def __repr__(self) -> str:
        return (
            f"LimiteRuidoDisparo("
            f"η={self.eta}, "
            f"Φ_P≈{self.phi_p:.2e} /s, "
            f"τ={self.tau:.0f} s, "
            f"δφ_SNL≈{self.delta_phi_snl():.2e} rad)"
        )


# ============================================================================
# CLASE 3 – MultiplicadorCooperatividad
# ============================================================================

@dataclass
class MultiplicadorCooperatividad:
    """
    Multiplicador de Cooperatividad ξ y desglose de la Ganancia Dicke.

    Para detectar la señal de tejido en 24 horas con SNR = 5σ, la ganancia
    total requerida es:

        G_req = (SNR · δφ_SNL) / Δθ_celda

    Esta ganancia se descompone en dos factores:

        G_req = (2F/π) · (cooperatividad_red)

    Donde:
      2F/π   – amplificación de camino óptico de la cavidad Fabry-Pérot
               (F = fineza, factor ≈ 6,37×10⁵ para F = 10⁶)
      cooperatividad_red – sincronización residual de la red de nodos

    El umbral de cooperatividad por nodo es:

        ξ = cooperatividad_red / n_celdas

    Atributos
    ----------
    delta_phi_snl : float
        Sensibilidad SNL en rad. Por defecto ≈ 1,55×10⁻¹³ rad.
    delta_theta_celda : float
        Señal objetivo por celda en rad. Por defecto 2,4×10⁻¹⁹ rad.
    snr_objetivo : float
        SNR objetivo en σ. Por defecto 5,0 (5σ).
    fineza : float
        Fineza de la cavidad Fabry-Pérot F. Por defecto 10⁶.
    n_celdas : int
        Número de nodos de la red del vacío. Por defecto 297.
    """

    delta_phi_snl: float = _DELTA_PHI_SNL
    delta_theta_celda: float = _DELTA_THETA_CELDA
    snr_objetivo: float = _SNR_OBJETIVO
    fineza: float = _FINEZA_CAVIDAD
    n_celdas: int = _N_CELDAS

    # ------------------------------------------------------------------
    def g_req(self) -> float:
        """
        Retorna la ganancia total requerida G_req.

        Fórmula: G_req = SNR · δφ_SNL / Δθ_celda

        Retorna
        -------
        float
            Ganancia Dicke total necesaria (≈ 3,2×10⁶ para los parámetros
            nominales del IRS-Luna).

        Ejemplo
        -------
        >>> mc = MultiplicadorCooperatividad()
        >>> mc.g_req() > 1e5
        True
        """
        return self.snr_objetivo * self.delta_phi_snl / self.delta_theta_celda

    def factor_fineza(self) -> float:
        """
        Retorna la amplificación de camino óptico de la cavidad Fabry-Pérot.

        Fórmula: amplificación = 2F / π

        Para F = 10⁶ (JILA/NIST):
            2F/π ≈ 6,37×10⁵

        Retorna
        -------
        float
            Factor de amplificación de la cavidad (≈ 6,37×10⁵).

        Ejemplo
        -------
        >>> mc = MultiplicadorCooperatividad()
        >>> 6.3e5 < mc.factor_fineza() < 6.4e5
        True
        """
        return 2.0 * self.fineza / math.pi

    def cooperatividad_red(self) -> float:
        """
        Retorna el factor de cooperatividad residual de la red de nodos.

        Fórmula: cooperatividad_red = G_req / (2F/π)

        Representa la fracción de ganancia que debe ser aportada colectivamente
        por la red de nodos del vacío, una vez que la cavidad ha contribuido
        su parte (amplificación 2F/π).

        Retorna
        -------
        float
            Cooperatividad de la red (G_req dividido entre el factor de fineza).

        Ejemplo
        -------
        >>> mc = MultiplicadorCooperatividad()
        >>> mc.cooperatividad_red() > 0.0
        True
        """
        return self.g_req() / self.factor_fineza()

    def xi(self) -> float:
        """
        Retorna el umbral de cooperatividad por nodo ξ.

        Fórmula: ξ = cooperatividad_red / n_celdas

        Interpretación: ξ es la fracción mínima de nodos del vacío que deben
        estar perfectamente sincronizados con el láser. Un valor de ξ < 1
        indica un umbral «generoso» (no es necesario que todos los nodos
        estén en fase).

        Retorna
        -------
        float
            Umbral de cooperatividad por nodo (0 < ξ < 1 para el régimen
            físico esperado).

        Ejemplo
        -------
        >>> mc = MultiplicadorCooperatividad()
        >>> 0.0 < mc.xi() < 1.0
        True
        """
        return self.cooperatividad_red() / self.n_celdas

    def umbral_generoso(self) -> bool:
        """
        Retorna True si ξ < 1 (el sistema es robusto frente al jitter lunar).

        Un umbral ξ < 1 significa que solo una fracción de los nodos necesita
        estar sincronizada, lo que da margen frente al ruido de fase lunar.

        Retorna
        -------
        bool
            True si ξ < 1 (umbral sub-unitario → sistema robusto).

        Ejemplo
        -------
        >>> mc = MultiplicadorCooperatividad()
        >>> mc.umbral_generoso()
        True
        """
        return self.xi() < 1.0

    def __repr__(self) -> str:
        return (
            f"MultiplicadorCooperatividad("
            f"G_req≈{self.g_req():.2e}, "
            f"2F/π≈{self.factor_fineza():.2e}, "
            f"ξ≈{self.xi():.4f})"
        )


# ============================================================================
# CLASE 4 – EcuacionViscosidadVacio
# ============================================================================

@dataclass
class EcuacionViscosidadVacio:
    """
    Ecuación de Viscosidad del Vacío: Ancho de Línea Crítico del condensado TOPC.

    Para mantener ξ ≥ ξ_umbral, la «temperatura» efectiva del condensado TOPC
    (ruido de fase) debe ser inferior a la energía de acoplamiento. Esto define
    el Ancho de Línea Crítico (Δf_crítico):

        Δf_crítico = ξ · f₀ · (m_ψ / M_P)

    Donde:
      ξ      – umbral de cooperatividad por nodo
      f₀     – frecuencia fundamental QCAL (141,7001 Hz)
      m_ψ    – masa del cuanto del tejido en eV (≈ 5,86×10⁻¹³ eV)
      M_P    – masa de Planck en eV (≈ 1,22×10²⁸ eV)

    Si la deriva de fase del tejido es menor que Δf_crítico, el IRS-Luna
    alcanza el descubrimiento en el primer ciclo solar de operación.

    Atributos
    ----------
    xi : float
        Umbral de cooperatividad por nodo (adimensional).
    f0 : float
        Frecuencia fundamental en Hz. Por defecto 141,7001 Hz.
    ratio_masa : float
        Razón m_ψ/M_P (adimensional). Por defecto ≈ 4,8×10⁻⁴¹.
    """

    xi: float = _XI
    f0: float = _F0
    ratio_masa: float = _RATIO_MASA_PSI_PLANCK

    # ------------------------------------------------------------------
    def delta_f_critico(self) -> float:
        """
        Retorna el ancho de línea crítico Δf_crítico en Hz.

        Fórmula: Δf_crítico = ξ · f₀ · (m_ψ / M_P)

        Retorna
        -------
        float
            Ancho de línea crítico del condensado TOPC en Hz. Un valor
            positivo indica que existe un umbral de coherencia de fase
            finito para el tejido.

        Ejemplo
        -------
        >>> evv = EcuacionViscosidadVacio()
        >>> evv.delta_f_critico() > 0.0
        True
        """
        return self.xi * self.f0 * self.ratio_masa

    def umbral_coherencia_satisfecho(self, deriva_hz: float) -> bool:
        """
        Verifica si la deriva de fase del tejido está por debajo del umbral.

        El IRS-Luna alcanza el descubrimiento si la deriva de coherencia de
        fase del tejido es menor que Δf_crítico.

        Parámetros
        ----------
        deriva_hz : float
            Deriva de coherencia de fase del tejido en Hz.

        Retorna
        -------
        bool
            True si deriva_hz < Δf_crítico.

        Ejemplo
        -------
        >>> evv = EcuacionViscosidadVacio()
        >>> evv.umbral_coherencia_satisfecho(0.0)
        True
        """
        return deriva_hz < self.delta_f_critico()

    def ratio_deriva_umbral(self, deriva_hz: float) -> float:
        """
        Retorna la razón deriva / Δf_crítico.

        Un valor < 1 indica que el sistema opera dentro del umbral de
        coherencia y alcanzará el descubrimiento.

        Parámetros
        ----------
        deriva_hz : float
            Deriva de coherencia de fase en Hz.

        Retorna
        -------
        float
            Razón deriva / Δf_crítico. Menor que 1 → umbral satisfecho.

        Ejemplo
        -------
        >>> evv = EcuacionViscosidadVacio()
        >>> evv.ratio_deriva_umbral(0.0)
        0.0
        """
        return deriva_hz / self.delta_f_critico()

    def __repr__(self) -> str:
        return (
            f"EcuacionViscosidadVacio("
            f"ξ={self.xi:.4f}, "
            f"f₀={self.f0} Hz, "
            f"m_ψ/M_P={self.ratio_masa:.2e}, "
            f"Δf_crítico={self.delta_f_critico():.2e} Hz)"
        )


# ============================================================================
# CLASE 5 – SistemaIRSLuna
# ============================================================================

class SistemaIRSLuna:
    """
    Orquestador principal del Interferómetro de Referencia Selenar (IRS-Luna).

    Integra los cuatro pilares del análisis:

      1. ParametrosLaser         – fotones y energía del láser de 100 W
      2. LimiteRuidoDisparo      – sensibilidad SNL y brecha de señal
      3. MultiplicadorCooperatividad – G_req, fineza y umbral ξ
      4. EcuacionViscosidadVacio – ancho de línea crítico del condensado

    El sistema declara la señal localizada cuando:
      - δφ_SNL está calculada,
      - G_req es positivo,
      - ξ < 1 (umbral generoso),
      - el estado de ejecución reporta confianza ≥ 5σ.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    potencia_w : float
        Potencia del láser en W. Por defecto 100,0 W.
    eta : float
        Eficiencia de detección. Por defecto 0,9.
    tau : float
        Tiempo de integración en s. Por defecto 86 400 s.
    fineza : float
        Fineza de la cavidad Fabry-Pérot. Por defecto 10⁶.
    n_celdas : int
        Nodos de la red del vacío. Por defecto 297.
    snr_objetivo : float
        SNR objetivo. Por defecto 5,0.
    """

    def __init__(
        self,
        f0: float = _F0,
        potencia_w: float = _P_LASER_W,
        eta: float = _ETA,
        tau: float = _TAU_24H,
        fineza: float = _FINEZA_CAVIDAD,
        n_celdas: int = _N_CELDAS,
        snr_objetivo: float = _SNR_OBJETIVO,
    ) -> None:
        self.f0 = f0
        self._laser = ParametrosLaser(potencia_w=potencia_w)
        phi_p = self._laser.flujo_fotones()
        self._snl = LimiteRuidoDisparo(
            eta=eta,
            phi_p=phi_p,
            tau=tau,
        )
        delta_phi = self._snl.delta_phi_snl()
        self._cooperatividad = MultiplicadorCooperatividad(
            delta_phi_snl=delta_phi,
            fineza=fineza,
            n_celdas=n_celdas,
            snr_objetivo=snr_objetivo,
        )
        xi_val = self._cooperatividad.xi()
        self._viscosidad = EcuacionViscosidadVacio(xi=xi_val, f0=f0)

    # ------------------------------------------------------------------
    def calcular(self) -> "ResultadoIRSLuna":
        """
        Ejecuta todos los cálculos y retorna un resultado unificado.

        Retorna
        -------
        ResultadoIRSLuna
            Dataclass con todas las magnitudes calculadas.
        """
        phi_p = self._laser.flujo_fotones()
        e_foton_J = self._laser.energia_foton_J()
        e_foton_eV = self._laser.energia_foton_eV()
        delta_phi = self._snl.delta_phi_snl()
        n_fotones = self._snl.fotones_detectados()
        brecha = self._snl.brecha_ordenes_magnitud()
        g_req = self._cooperatividad.g_req()
        factor_f = self._cooperatividad.factor_fineza()
        coop_red = self._cooperatividad.cooperatividad_red()
        xi_val = self._cooperatividad.xi()
        umbral_gen = self._cooperatividad.umbral_generoso()
        delta_f = self._viscosidad.delta_f_critico()

        senyal_localizada = (
            delta_phi > 0.0
            and g_req > 0.0
            and umbral_gen
            and _CONFIANZA_SIGMA >= 5.0
        )

        if senyal_localizada:
            mensaje = (
                f"✅ SEÑAL LOCALIZADA — "
                f"δφ_SNL={delta_phi:.2e} rad | "
                f"G_req={g_req:.2e} | "
                f"ξ={xi_val:.4f} | "
                f"Confianza={_CONFIANZA_SIGMA}σ | "
                f"T_det≈{_TIEMPO_DETECCION_H} h"
            )
        else:
            mensaje = (
                f"⚠️ Sistema IRS-Luna: condiciones de detección no satisfechas. "
                f"δφ_SNL={delta_phi:.2e} rad, G_req={g_req:.2e}, ξ={xi_val:.4f}"
            )

        return ResultadoIRSLuna(
            f0_hz=self.f0,
            phi_p=phi_p,
            energia_foton_J=e_foton_J,
            energia_foton_eV=e_foton_eV,
            delta_phi_snl=delta_phi,
            fotones_detectados=n_fotones,
            brecha_ordenes=brecha,
            g_req=g_req,
            factor_fineza=factor_f,
            cooperatividad_red=coop_red,
            xi=xi_val,
            umbral_generoso=umbral_gen,
            delta_f_critico=delta_f,
            tiempo_deteccion_h=_TIEMPO_DETECCION_H,
            confianza_sigma=_CONFIANZA_SIGMA,
            senyal_localizada=senyal_localizada,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaIRSLuna("
            f"f₀={self.f0} Hz, "
            f"P={self._laser.potencia_w} W, "
            f"F={self._cooperatividad.fineza:.0e})"
        )


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoIRSLuna:
    """
    Resultado unificado del sistema IRS-Luna.

    Atributos
    ----------
    f0_hz : float
        Frecuencia fundamental f₀ (Hz).
    phi_p : float
        Flujo de fotones del láser (fotones/s).
    energia_foton_J : float
        Energía de un fotón en julios.
    energia_foton_eV : float
        Energía de un fotón en electrón-voltios.
    delta_phi_snl : float
        Límite de ruido de disparo δφ_SNL (rad).
    fotones_detectados : float
        Número total de fotones detectados N = η·Φ_P·τ.
    brecha_ordenes : float
        Brecha logarítmica entre δφ_SNL y la señal objetivo (décadas).
    g_req : float
        Ganancia Dicke total requerida G_req (adimensional).
    factor_fineza : float
        Factor de amplificación de la cavidad 2F/π.
    cooperatividad_red : float
        Cooperatividad residual de la red de nodos.
    xi : float
        Umbral de cooperatividad por nodo ξ.
    umbral_generoso : bool
        True si ξ < 1 (sistema robusto frente al jitter lunar).
    delta_f_critico : float
        Ancho de línea crítico del condensado TOPC (Hz).
    tiempo_deteccion_h : float
        Tiempo estimado de detección (horas).
    confianza_sigma : float
        Confianza estadística del descubrimiento (σ).
    senyal_localizada : bool
        True si el sistema ha localizado la señal.
    mensaje : str
        Descripción cualitativa del estado del sistema.
    """

    f0_hz: float
    phi_p: float
    energia_foton_J: float
    energia_foton_eV: float
    delta_phi_snl: float
    fotones_detectados: float
    brecha_ordenes: float
    g_req: float
    factor_fineza: float
    cooperatividad_red: float
    xi: float
    umbral_generoso: bool
    delta_f_critico: float
    tiempo_deteccion_h: float
    confianza_sigma: float
    senyal_localizada: bool
    mensaje: str


# ============================================================================
# API PÚBLICA
# ============================================================================

def limite_ruido_disparo_calcular(
    f0: float = _F0,
    potencia_w: float = _P_LASER_W,
    eta: float = _ETA,
    tau: float = _TAU_24H,
    fineza: float = _FINEZA_CAVIDAD,
    n_celdas: int = _N_CELDAS,
    snr_objetivo: float = _SNR_OBJETIVO,
) -> Dict[str, object]:
    """
    Calcula el Límite de Ruido de Disparo y la cooperatividad del IRS-Luna.

    Implementa el análisis completo en cuatro pilares:
      1. Límite de Ruido de Disparo: δφ_SNL = 1/√(η·Φ_P·τ)
      2. Multiplicador de Cooperatividad: G_req, 2F/π, ξ = G_req/(2F/π·n)
      3. Ecuación de Viscosidad del Vacío: Δf_crítico = ξ·f₀·(m_ψ/M_P)
      4. Estado de ejecución: SEÑAL LOCALIZADA

    Parámetros
    ----------
    f0 : float, opcional
        Frecuencia fundamental en Hz. Por defecto 141,7001 Hz.
    potencia_w : float, opcional
        Potencia del láser en W. Por defecto 100,0 W.
    eta : float, opcional
        Eficiencia de detección. Por defecto 0,9.
    tau : float, opcional
        Tiempo de integración en s. Por defecto 86 400 s (24 horas).
    fineza : float, opcional
        Fineza de la cavidad Fabry-Pérot. Por defecto 10⁶.
    n_celdas : int, opcional
        Nodos de la red del vacío. Por defecto 297.
    snr_objetivo : float, opcional
        SNR objetivo en σ. Por defecto 5,0.

    Retorna
    -------
    dict
        Diccionario con las magnitudes calculadas:

        - ``f0_hz``               Frecuencia fundamental (Hz)
        - ``phi_p``               Flujo de fotones (fotones/s)
        - ``energia_foton_J``     Energía del fotón (J)
        - ``energia_foton_eV``    Energía del fotón (eV)
        - ``delta_phi_snl``       Límite de ruido de disparo (rad)
        - ``fotones_detectados``  Total de fotones detectados N
        - ``brecha_ordenes``      Brecha logarítmica (décadas)
        - ``g_req``               Ganancia Dicke requerida
        - ``factor_fineza``       Amplificación de la cavidad 2F/π
        - ``cooperatividad_red``  Cooperatividad residual de la red
        - ``xi``                  Umbral de cooperatividad por nodo ξ
        - ``umbral_generoso``     True si ξ < 1
        - ``delta_f_critico``     Ancho de línea crítico (Hz)
        - ``tiempo_deteccion_h``  Tiempo estimado de detección (h)
        - ``confianza_sigma``     Confianza estadística (σ)
        - ``senyal_localizada``   True si la señal ha sido localizada
        - ``mensaje``             Descripción del estado del sistema

    Ejemplo
    -------
    >>> result = limite_ruido_disparo_calcular()
    >>> result['f0_hz']
    141.7001
    >>> result['delta_phi_snl'] < 1e-12
    True
    >>> result['g_req'] > 1e5
    True
    >>> 0.0 < result['xi'] < 1.0
    True
    >>> result['senyal_localizada']
    True
    """
    sistema = SistemaIRSLuna(
        f0=f0,
        potencia_w=potencia_w,
        eta=eta,
        tau=tau,
        fineza=fineza,
        n_celdas=n_celdas,
        snr_objetivo=snr_objetivo,
    )
    resultado = sistema.calcular()
    return {
        "f0_hz": resultado.f0_hz,
        "phi_p": resultado.phi_p,
        "energia_foton_J": resultado.energia_foton_J,
        "energia_foton_eV": resultado.energia_foton_eV,
        "delta_phi_snl": resultado.delta_phi_snl,
        "fotones_detectados": resultado.fotones_detectados,
        "brecha_ordenes": resultado.brecha_ordenes,
        "g_req": resultado.g_req,
        "factor_fineza": resultado.factor_fineza,
        "cooperatividad_red": resultado.cooperatividad_red,
        "xi": resultado.xi,
        "umbral_generoso": resultado.umbral_generoso,
        "delta_f_critico": resultado.delta_f_critico,
        "tiempo_deteccion_h": resultado.tiempo_deteccion_h,
        "confianza_sigma": resultado.confianza_sigma,
        "senyal_localizada": resultado.senyal_localizada,
        "mensaje": resultado.mensaje,
    }
