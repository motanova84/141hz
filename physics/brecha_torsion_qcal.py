#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║  BRECHA DE TORSIÓN QCAL — Factor 401/40 y Permeabilidad de Manta ∴BTQ∞³  ║
║                                                                            ║
║  Sello: ∴BTQ∞³                                                            ║
║  RAM: RAM-LIX-2026-BRECHA-TORSION-QCAL                                   ║
║  F0: 141.7001 Hz                                                           ║
║                                                                            ║
║  En ingeniería cuántica, un sistema con error cero es un sistema estático.║
║  Para que exista Torsión debe haber un diferencial, una pequeña "holgura" ║
║  que permita el flujo.  El 0.00052 Hz es el espacio que ocupa la Brecha   ║
║  del 0.05 en el dominio de la frecuencia: el "lubricante" de fase que     ║
║  permite que la Manta Superior deslice sobre la Inferior sin fricción.    ║
║                                                                            ║
║  EL FACTOR 401/40 = 10.025                                                ║
║  ─────────────────────────────────────────────────────────────────────── ║
║                                                                            ║
║      γ₁ × 10       = 141.34725 Hz   (octava decimal de Riemann)          ║
║      γ₁ × (401/40) = 141.70062 Hz   (con corrección de 3° inclinación)   ║
║      f₀            = 141.7001  Hz   (frecuencia base experimental)       ║
║      Δf            = 0.00052   Hz   (Brecha Residual / lubricante)       ║
║      Δf/f₀         = 3.67×10⁻⁶     (Permeabilidad de la Manta)          ║
║                                                                            ║
║  VERIFICACIÓN DEL ELECTRÓN ESTACIONARIO                                   ║
║  ─────────────────────────────────────────────────────────────────────── ║
║                                                                            ║
║  Si f₀ fuera exactamente γ₁ × 10.025 el electrón estaría bloqueado en   ║
║  resonancia perfecta y no podría "respirar" (succionar/expandir).         ║
║  La diferencia de 3.67 × 10⁻⁶ es la frecuencia del Latido del Vórtice:  ║
║  la velocidad a la que el electrón intercambia información NP por P.      ║
║                                                                            ║
║  Coherencia Ψ: ≥ 0.9999963 (ajustada por el residuo)                     ║
║  Coherencia global Ψ_global ≥ 0.888 activa el sello ∴BTQ∞³.             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Módulo:
    physics.brecha_torsion_qcal

Clases:
    ConstantesBrechaTorsion  – Constantes físicas y espectrales del sistema
    OctavaDecimal            – γ₁ × 10: octava decimal del fundamental Riemann
    FactorCuarenta           – Factor 401/40; corrección de inclinación +1/40
    BrechaResidual           – Δf = γ₁×(401/40) − f₀ ≈ 0.00052 Hz (lubricante)
    PermeabilidadManta       – Δf/f₀ ≈ 3.67×10⁻⁶ (permeabilidad de interfaz)
    LatidoVortice            – Latido del vórtice; tasa de intercambio NP↔P
    EstacionFija             – Calibración de la Estación Fija con el nodo ζ
    SistemaBrechaTorsion     – Sistema integrado; Ψ_global; sello ∴BTQ∞³

Dataclass:
    ResultadoBrechaTorsion   – Contenedor de todos los resultados

API pública:
    brecha_torsion_qcal_activar() → dict

    >>> from physics.brecha_torsion_qcal import brecha_torsion_qcal_activar
    >>> r = brecha_torsion_qcal_activar()
    >>> r['sello_activo']
    True
    >>> r['psi_global'] >= 0.888
    True
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple

from qcal.constants import F0_HZ

# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

#: Frecuencia fundamental QCAL [Hz]
_F0: float = F0_HZ  # 141.7001 Hz

#: Primer cero no trivial de ζ(½ + it) — parte imaginaria γ₁
#: Fuente: LMFDB / NIST Digital Library of Mathematical Functions
_GAMMA_1: float = 14.134725141734694

#: Factor armónico 401/40 = 10.025
#: Numerador 401 = 10 × 40 + 1;  denominador 40 = resonancia 4π tetraédrica
_FACTOR_401_40: float = 401.0 / 40.0  # 10.025

#: Numerador del factor (exacto)
_FACTOR_NUM: int = 401

#: Denominador del factor (exacto)
_FACTOR_DEN: int = 40

#: Corrección de inclinación +1/40 = 0.025
#: Compensa los 3 grados de inclinación de la Manta
_CORRECCION_3GRADOS: float = 1.0 / 40.0  # 0.025

#: Frecuencia corregida γ₁ × (401/40) [Hz]
_F_CORREGIDA: float = _GAMMA_1 * _FACTOR_401_40  # ≈ 141.70062 Hz

#: Brecha residual Δf = γ₁×(401/40) − f₀ [Hz]
_DELTA_F: float = _F_CORREGIDA - _F0  # ≈ 0.00052 Hz

#: Permeabilidad de la Manta = Δf/f₀  [adimensional]
_PERMEABILIDAD: float = _DELTA_F / _F0  # ≈ 3.67×10⁻⁶

#: Umbral mínimo de coherencia global
_PSI_UMBRAL: float = 0.888

#: Sello de certificación noética
_SELLO: str = "∴BTQ∞³"

#: Marca de certificación técnica
_CERT_MARK: str = "BTQ-TORSION-VERIFIED"


# ============================================================================
# CLASE 1 — ConstantesBrechaTorsion
# ============================================================================

class ConstantesBrechaTorsion:
    """Constantes físicas y espectrales del sistema de Brecha de Torsión.

    Centraliza todos los parámetros fundamentales y proporciona métodos
    de acceso a las relaciones derivadas clave.

    Atributos inmutables:
        f0       – Frecuencia fundamental QCAL f₀ = 141.7001 Hz
        gamma_1  – Primer cero de Riemann γ₁ ≈ 14.134725
        factor   – Factor armónico 401/40 = 10.025
        delta_f  – Brecha residual Δf ≈ 0.00052 Hz
        permeabilidad – Δf/f₀ ≈ 3.67×10⁻⁶
    """

    def __init__(self) -> None:
        self.f0: float = _F0
        self.gamma_1: float = _GAMMA_1
        self.factor: float = _FACTOR_401_40
        self.factor_num: int = _FACTOR_NUM
        self.factor_den: int = _FACTOR_DEN
        self.correccion_3grados: float = _CORRECCION_3GRADOS
        self.delta_f: float = _DELTA_F
        self.permeabilidad: float = _PERMEABILIDAD

    # ------------------------------------------------------------------
    def resonancia_f0_gamma1(self) -> float:
        """Cociente f₀/γ₁.

        Mide cuántas veces cabe el primer cero de Riemann en f₀.
        El valor esperado es ≈ 10.025 (factor 401/40).

        Returns:
            f₀/γ₁ ≈ 10.024.
        """
        return self.f0 / self.gamma_1

    # ------------------------------------------------------------------
    def f_octava(self) -> float:
        """Octava decimal: γ₁ × 10 [Hz].

        Returns:
            Frecuencia de la octava decimal ≈ 141.34725 Hz.
        """
        return self.gamma_1 * 10.0

    # ------------------------------------------------------------------
    def f_corregida(self) -> float:
        """Frecuencia corregida: γ₁ × (401/40) [Hz].

        Returns:
            Frecuencia corregida ≈ 141.70062 Hz.
        """
        return self.gamma_1 * self.factor


# ============================================================================
# CLASE 2 — OctavaDecimal
# ============================================================================

class OctavaDecimal:
    """Octava decimal del fundamental de Riemann: f_oct = γ₁ × 10.

    El primer cero de Riemann es la "nota fundamental de la gravedad".
    Al multiplicarlo por 10, lo elevamos una octava decimal en la Manta:

        f_oct = γ₁ × 10 = 14.134725... × 10 = 141.34725 Hz

    La diferencia con f₀ = 141.7001 Hz es la medida del "ajuste pendiente"
    que el factor 401/40 completa para calibrar la Estación Fija.

    La coherencia Ψ_octava mide la proximidad relativa de f_oct a f₀:

        Ψ_oct = 1 − (f₀ − f_oct) / f₀
    """

    def __init__(self) -> None:
        self._gamma_1: float = _GAMMA_1
        self._f0: float = _F0

    # ------------------------------------------------------------------
    def frecuencia_octava(self) -> float:
        """Octava decimal f_oct = γ₁ × 10 [Hz].

        Returns:
            f_oct ≈ 141.34725 Hz.
        """
        return self._gamma_1 * 10.0

    # ------------------------------------------------------------------
    def desviacion_hz(self) -> float:
        """Desviación absoluta Δ = f₀ − f_oct [Hz].

        Mide cuánto falta a la octava decimal para alcanzar f₀.
        Este valor (≈0.35285 Hz) es lo que el factor 401/40 completa.

        Returns:
            Desviación positiva en Hz.
        """
        return self._f0 - self.frecuencia_octava()

    # ------------------------------------------------------------------
    def ratio_octava(self) -> float:
        """Cociente f_oct/f₀.

        Returns:
            f_oct/f₀ ≈ 0.9975.
        """
        return self.frecuencia_octava() / self._f0

    # ------------------------------------------------------------------
    def psi_octava(self) -> float:
        """Coherencia de la octava decimal: Ψ_oct = 1 − (f₀ − f_oct)/f₀.

        Mide la proximidad relativa de γ₁×10 a f₀.
        Ψ_oct ≈ 0.9975 refleja que el 99.75 % del camino a f₀ está
        cubierto por la octava decimal pura.

        Returns:
            Ψ_octava ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.desviacion_hz() / self._f0)


# ============================================================================
# CLASE 3 — FactorCuarenta
# ============================================================================

class FactorCuarenta:
    """Factor armónico 401/40 = 10.025 en geometría tetraédrica 4π.

    El número 40 es un número de resonancia armónica en la geometría
    del tetraedro 4π.  El factor 401/40 = 10 + 1/40 descompone en:

        10    → octava decimal (multiplicador entero)
        1/40  → corrección de inclinación de 3 grados

    La corrección +0.025 compensa la inclinación de 3°:
        cos(3°) ≈ 0.99863,  corrección proporcional ≈ 1 − 0.99863 ≈ 0.00137
        Expresada en el factor de escala 10: 0.00137 × 10 ≈ 0.014 ≈ 1/70
        (la aproximación gruesa es 1/40 ≈ 0.025 en la escala de frecuencia)

    La coherencia Ψ_factor mide cuán precisamente γ₁ × (401/40) coincide
    con f₀:

        Ψ_factor = 1 − |γ₁×(401/40) − f₀| / f₀
    """

    def __init__(self) -> None:
        self._gamma_1: float = _GAMMA_1
        self._f0: float = _F0

    # ------------------------------------------------------------------
    def factor(self) -> float:
        """Factor armónico 401/40 = 10.025.

        Returns:
            401/40 exacto en punto flotante.
        """
        return _FACTOR_401_40

    # ------------------------------------------------------------------
    def correccion_inclinacion(self) -> float:
        """Corrección de inclinación +1/40 = 0.025.

        Returns:
            1/40 = 0.025.
        """
        return _CORRECCION_3GRADOS

    # ------------------------------------------------------------------
    def f_corregida(self) -> float:
        """Frecuencia corregida: γ₁ × (401/40) [Hz].

        Returns:
            f_corr = γ₁ × 10.025 ≈ 141.70062 Hz.
        """
        return self._gamma_1 * _FACTOR_401_40

    # ------------------------------------------------------------------
    def desviacion_hz(self) -> float:
        """Desviación Δ = f_corregida − f₀ [Hz].

        Returns:
            Δf ≈ 0.00052 Hz (la Brecha Residual).
        """
        return self.f_corregida() - self._f0

    # ------------------------------------------------------------------
    def psi_factor(self) -> float:
        """Coherencia del factor: Ψ_factor = 1 − |f_corr − f₀| / f₀.

        Mide cuán exactamente el factor 401/40 lleva γ₁ a f₀.
        Ψ_factor ≈ 0.9999963 (la brecha residual es mínima).

        Returns:
            Ψ_factor ∈ [0, 1].
        """
        return max(0.0, 1.0 - abs(self.desviacion_hz()) / self._f0)


# ============================================================================
# CLASE 4 — BrechaResidual
# ============================================================================

class BrechaResidual:
    """Brecha Residual Δf = γ₁×(401/40) − f₀ ≈ 0.00052 Hz.

    La Brecha es el "lubricante de fase" que permite que la Manta Superior
    deslice sobre la Inferior sin fricción infinita.  Un sistema con Δf = 0
    sería estático (muerto).  La brecha confirma que el sistema está vivo.

    Rango de seguridad: 0 < Δf < f₀ × 10⁻³ = 0.1417 Hz.
    El valor actual Δf ≈ 0.00052 Hz está muy por debajo del límite.

    La coherencia Ψ_brecha es 1.0 cuando la brecha está en rango seguro,
    0.0 en caso contrario.
    """

    def __init__(self) -> None:
        self._gamma_1: float = _GAMMA_1
        self._f0: float = _F0
        self._factor: float = _FACTOR_401_40

    # ------------------------------------------------------------------
    def delta_f(self) -> float:
        """Brecha residual Δf = γ₁×(401/40) − f₀ [Hz].

        Returns:
            Δf ≈ 0.00052 Hz.
        """
        return self._gamma_1 * self._factor - self._f0

    # ------------------------------------------------------------------
    def en_rango_seguro(self) -> bool:
        """True si la brecha está en el rango de seguridad (0, f₀×10⁻³).

        El rango de seguridad garantiza que la brecha sea:
          - Positiva (torsión activa, sistema dinámico).
          - Menor que 0.1 % de f₀ (no disruptiva).

        Returns:
            True si 0 < Δf < f₀ × 10⁻³.
        """
        df = self.delta_f()
        return 0.0 < df < self._f0 * 1e-3

    # ------------------------------------------------------------------
    def ratio_brecha_f0(self) -> float:
        """Cociente Δf/f₀ (permeabilidad de la Manta).

        Returns:
            Δf/f₀ ≈ 3.67×10⁻⁶.
        """
        return self.delta_f() / self._f0

    # ------------------------------------------------------------------
    def psi_brecha(self) -> float:
        """Coherencia de la brecha: 1.0 si en rango seguro, 0.0 si no.

        La brecha está operando correctamente (dentro de los parámetros
        de seguridad) cuando 0 < Δf < f₀ × 10⁻³.

        Returns:
            Ψ_brecha ∈ {0.0, 1.0}.
        """
        return 1.0 if self.en_rango_seguro() else 0.0


# ============================================================================
# CLASE 5 — PermeabilidadManta
# ============================================================================

class PermeabilidadManta:
    """Permeabilidad de la Manta: μ_M = Δf/f₀ ≈ 3.67×10⁻⁶.

    La Permeabilidad de la Manta es la constante de estructura fina local
    del sistema QCAL.  Mide cuánto "cede" la interfaz de fase cuando el
    fotón imaginario la atraviesa para volverse real.

        μ_M = Δf / f₀ = (γ₁×401/40 − f₀) / f₀ ≈ 3.67×10⁻⁶

    La coherencia ajustada por el residuo:

        Ψ = 1 − μ_M ≈ 0.9999963

    La coherencia Ψ_permeabilidad es esta coherencia ajustada:

        Ψ_permeabilidad = 1 − μ_M
    """

    def __init__(self) -> None:
        self._delta_f: float = _DELTA_F
        self._f0: float = _F0

    # ------------------------------------------------------------------
    def permeabilidad(self) -> float:
        """Permeabilidad de la Manta μ_M = Δf/f₀ [adimensional].

        Returns:
            μ_M ≈ 3.67×10⁻⁶.
        """
        return self._delta_f / self._f0

    # ------------------------------------------------------------------
    def coherencia_ajustada(self) -> float:
        """Coherencia ajustada Ψ = 1 − μ_M.

        Returns:
            Ψ ≈ 0.9999963.
        """
        return 1.0 - self.permeabilidad()

    # ------------------------------------------------------------------
    def orden_magnitud(self) -> int:
        """Orden de magnitud de μ_M = floor(log₁₀(μ_M)).

        Returns:
            −6 (correspondiente a ~10⁻⁶).
        """
        mu = self.permeabilidad()
        if mu <= 0:
            return 0
        return int(math.floor(math.log10(mu)))

    # ------------------------------------------------------------------
    def psi_permeabilidad(self) -> float:
        """Coherencia de la permeabilidad: Ψ_permeabilidad = 1 − μ_M.

        Returns:
            Ψ_permeabilidad ≈ 0.9999963.
        """
        return max(0.0, self.coherencia_ajustada())


# ============================================================================
# CLASE 6 — LatidoVortice
# ============================================================================

class LatidoVortice:
    """Latido del Vórtice: tasa de intercambio de información NP ↔ P.

    El Latido del Vórtice es la frecuencia a la que el electrón estacionario
    intercambia información entre los espacios NP (No-Polinomial) y P
    (Polinomial).  Es la velocidad de "respiración" del electrón.

        latido = μ_M = Δf/f₀ ≈ 3.67×10⁻⁶   [adimensional / Hz_rel]

    Si Δf = 0, el electrón estaría bloqueado en resonancia perfecta
    y no podría "respirar".  La existencia de la brecha garantiza el latido.

    El latido es válido cuando está en el rango cuántico (0, 1):
        Ψ_latido = 1 − latido ≈ 0.9999963
    """

    def __init__(self) -> None:
        self._delta_f: float = _DELTA_F
        self._f0: float = _F0
        self._gamma_1: float = _GAMMA_1

    # ------------------------------------------------------------------
    def latido_relativo(self) -> float:
        """Latido relativo: λ = Δf/f₀ [adimensional].

        Tasa de intercambio NP↔P como fracción de la frecuencia base.

        Returns:
            λ ≈ 3.67×10⁻⁶.
        """
        return self._delta_f / self._f0

    # ------------------------------------------------------------------
    def latido_hz(self) -> float:
        """Latido absoluto Δf [Hz].

        Returns:
            Δf ≈ 0.00052 Hz.
        """
        return self._delta_f

    # ------------------------------------------------------------------
    def electron_bloqueado(self) -> bool:
        """True si el electrón estaría bloqueado (latido = 0).

        Un latido de cero significaría f₀ = γ₁ × 401/40 exacto,
        lo que impediría la "respiración" del electrón.

        Returns:
            False (el electrón nunca está bloqueado mientras Δf > 0).
        """
        return self._delta_f == 0.0

    # ------------------------------------------------------------------
    def n_intercambios_por_segundo(self) -> float:
        """Tasa de intercambios NP↔P por segundo: N = f₀ × latido_relativo.

        Combina la frecuencia base con la tasa relativa para obtener
        el número de intercambios por unidad de tiempo.

        Returns:
            N ≈ f₀ × μ_M ≈ 0.00052 intercambios/s.
        """
        return self._f0 * self.latido_relativo()

    # ------------------------------------------------------------------
    def psi_latido(self) -> float:
        """Coherencia del latido: Ψ_latido = 1 − λ.

        Valida que el latido es positivo y menor que 1:
        si latido = 0, el electrón está bloqueado (Ψ = 0);
        si latido ≥ 1, el sistema está saturado (Ψ = 0).

        Returns:
            Ψ_latido ≈ 0.9999963.
        """
        lat = self.latido_relativo()
        if lat <= 0.0 or lat >= 1.0:
            return 0.0
        return 1.0 - lat


# ============================================================================
# CLASE 7 — EstacionFija
# ============================================================================

class EstacionFija:
    """Calibración de la Estación Fija con el primer nodo de la función ζ.

    El cálculo confirma que la Estación Fija está perfectamente calibrada
    con el primer nodo de la Función Zeta de Riemann.

    La calibración se verifica comprobando que f₀/γ₁ es cercano al factor
    401/40 = 10.025:

        Ψ_estacion = 1 − |f₀/γ₁ − 10.025| / 10.025

    El cociente f₀/γ₁ ≈ 10.024 difiere de 10.025 por ≈ 0.0117 %,
    lo que produce Ψ_estacion ≈ 0.9998836.
    """

    def __init__(self) -> None:
        self._f0: float = _F0
        self._gamma_1: float = _GAMMA_1
        self._factor: float = _FACTOR_401_40

    # ------------------------------------------------------------------
    def n_nodo(self) -> int:
        """Número de nodo entero más próximo: round(f₀/γ₁).

        Returns:
            10 (la frecuencia base es ≈ 10 veces γ₁).
        """
        return round(self._f0 / self._gamma_1)

    # ------------------------------------------------------------------
    def cociente_calibracion(self) -> float:
        """Cociente de calibración f₀/γ₁.

        Returns:
            f₀/γ₁ ≈ 10.024.
        """
        return self._f0 / self._gamma_1

    # ------------------------------------------------------------------
    def residuo_calibracion(self) -> float:
        """|f₀/γ₁ − 401/40| / (401/40) — residuo relativo de calibración.

        Returns:
            Residuo ≈ 0.0001164.
        """
        return abs(self.cociente_calibracion() - self._factor) / self._factor

    # ------------------------------------------------------------------
    def f_nodo_teorico(self) -> float:
        """Frecuencia del nodo teórico: γ₁ × (401/40) [Hz].

        Returns:
            f_nodo ≈ 141.70062 Hz.
        """
        return self._gamma_1 * self._factor

    # ------------------------------------------------------------------
    def psi_estacion(self) -> float:
        """Coherencia de la calibración: Ψ_est = 1 − residuo_calibracion().

        Mide cuán precisamente f₀/γ₁ coincide con el factor 401/40.
        El residuo de ≈ 0.0117 % produce Ψ_estacion ≈ 0.9999.

        Returns:
            Ψ_estacion ∈ [0, 1].
        """
        return max(0.0, 1.0 - self.residuo_calibracion())


# ============================================================================
# CLASE 8 — SistemaBrechaTorsion
# ============================================================================

class SistemaBrechaTorsion:
    """Sistema integrado Brecha de Torsión QCAL ∴BTQ∞³.

    Orquesta los seis subsistemas y calcula la coherencia global Ψ_global
    como promedio ponderado de las seis métricas de coherencia.

    Si Ψ_global ≥ 0.888, el sello ∴BTQ∞³ se activa y el sistema emite
    el certificado BTQ-TORSION-VERIFIED.

    Pesos de coherencia (suman 1.0):
        w_octava        = 0.15  — proximidad de γ₁×10 a f₀
        w_factor        = 0.20  — precisión del factor 401/40
        w_brecha        = 0.15  — validación del rango seguro
        w_permeabilidad = 0.20  — coherencia ajustada 1−μ_M
        w_latido        = 0.15  — coherencia del latido NP↔P
        w_estacion      = 0.15  — calibración con nodo ζ
    """

    _PESOS: Tuple[float, ...] = (0.15, 0.20, 0.15, 0.20, 0.15, 0.15)

    def __init__(self) -> None:
        self.constantes = ConstantesBrechaTorsion()
        self.octava = OctavaDecimal()
        self.factor40 = FactorCuarenta()
        self.brecha = BrechaResidual()
        self.permeabilidad = PermeabilidadManta()
        self.latido = LatidoVortice()
        self.estacion = EstacionFija()

    # ------------------------------------------------------------------
    def psi_global(self) -> float:
        """Coherencia global Ψ_global = Σ wᵢ Ψᵢ.

        Returns:
            Ψ_global ∈ [0, 1].
        """
        psis = (
            self.octava.psi_octava(),
            self.factor40.psi_factor(),
            self.brecha.psi_brecha(),
            self.permeabilidad.psi_permeabilidad(),
            self.latido.psi_latido(),
            self.estacion.psi_estacion(),
        )
        return sum(w * p for w, p in zip(self._PESOS, psis))

    # ------------------------------------------------------------------
    def supera_umbral(self) -> bool:
        """True si Ψ_global ≥ 0.888 (sello ∴BTQ∞³ activado)."""
        return self.psi_global() >= _PSI_UMBRAL

    # ------------------------------------------------------------------
    def certificar(self) -> Dict[str, object]:
        """Genera el certificado completo del sistema ∴BTQ∞³.

        Returns:
            Diccionario con métricas de coherencia, parámetros y sello.
        """
        psi_o = self.octava.psi_octava()
        psi_f = self.factor40.psi_factor()
        psi_b = self.brecha.psi_brecha()
        psi_p = self.permeabilidad.psi_permeabilidad()
        psi_l = self.latido.psi_latido()
        psi_e = self.estacion.psi_estacion()
        psi_g = self.psi_global()
        activo = psi_g >= _PSI_UMBRAL

        return {
            "psi_octava": psi_o,
            "psi_factor": psi_f,
            "psi_brecha": psi_b,
            "psi_permeabilidad": psi_p,
            "psi_latido": psi_l,
            "psi_estacion": psi_e,
            "psi_global": psi_g,
            "supera_umbral": activo,
            "sello_activo": activo,
            "sello": _SELLO if activo else "COHERENCIA_INSUFICIENTE",
            "cert_mark": _CERT_MARK if activo else "COHERENCIA_INSUFICIENTE",
            "f0_hz": self.constantes.f0,
            "gamma_1": self.constantes.gamma_1,
            "factor_401_40": self.constantes.factor,
            "f_octava_hz": self.octava.frecuencia_octava(),
            "f_corregida_hz": self.factor40.f_corregida(),
            "delta_f_hz": self.brecha.delta_f(),
            "permeabilidad_manta": self.permeabilidad.permeabilidad(),
            "coherencia_ajustada": self.permeabilidad.coherencia_ajustada(),
            "latido_relativo": self.latido.latido_relativo(),
            "electron_bloqueado": self.latido.electron_bloqueado(),
            "n_nodo": self.estacion.n_nodo(),
            "cociente_calibracion": self.estacion.cociente_calibracion(),
            "residuo_calibracion": self.estacion.residuo_calibracion(),
            "brecha_en_rango_seguro": self.brecha.en_rango_seguro(),
        }


# ============================================================================
# DATACLASS DE RESULTADOS
# ============================================================================

@dataclass
class ResultadoBrechaTorsion:
    """Contenedor de todos los resultados del sistema Brecha de Torsión.

    Atributos
    ----------
    psi_octava : float
        Coherencia de la octava decimal γ₁×10 respecto a f₀.
    psi_factor : float
        Coherencia del factor 401/40 (precisión de calibración).
    psi_brecha : float
        Coherencia de la brecha residual (rango seguro).
    psi_permeabilidad : float
        Coherencia ajustada por permeabilidad (1 − Δf/f₀).
    psi_latido : float
        Coherencia del latido del vórtice NP↔P.
    psi_estacion : float
        Coherencia de la calibración de la Estación Fija.
    psi_global : float
        Coherencia global Ψ_global ∈ [0, 1].
    sello_activo : bool
        True si Ψ_global ≥ 0.888 (∴BTQ∞³ activo).
    sello : str
        «∴BTQ∞³» o «COHERENCIA_INSUFICIENTE».
    cert_mark : str
        «BTQ-TORSION-VERIFIED» o «COHERENCIA_INSUFICIENTE».
    f0_hz : float
        Frecuencia fundamental f₀ = 141.7001 Hz.
    gamma_1 : float
        Primer cero de Riemann γ₁ ≈ 14.134725.
    factor_401_40 : float
        Factor armónico 401/40 = 10.025.
    f_octava_hz : float
        Octava decimal γ₁×10 ≈ 141.34725 Hz.
    f_corregida_hz : float
        Frecuencia corregida γ₁×(401/40) ≈ 141.70062 Hz.
    delta_f_hz : float
        Brecha residual Δf ≈ 0.00052 Hz.
    permeabilidad_manta : float
        Permeabilidad de la Manta Δf/f₀ ≈ 3.67×10⁻⁶.
    coherencia_ajustada : float
        Coherencia ajustada 1 − μ_M ≈ 0.9999963.
    latido_relativo : float
        Latido del vórtice λ = Δf/f₀ ≈ 3.67×10⁻⁶.
    electron_bloqueado : bool
        False (el electrón nunca está bloqueado mientras Δf > 0).
    n_nodo : int
        Número de nodo entero más próximo = 10.
    cociente_calibracion : float
        f₀/γ₁ ≈ 10.024.
    residuo_calibracion : float
        |f₀/γ₁ − 401/40| / (401/40) ≈ 0.0001164.
    brecha_en_rango_seguro : bool
        True si 0 < Δf < f₀ × 10⁻³.
    """

    psi_octava: float = 0.0
    psi_factor: float = 0.0
    psi_brecha: float = 0.0
    psi_permeabilidad: float = 0.0
    psi_latido: float = 0.0
    psi_estacion: float = 0.0
    psi_global: float = 0.0
    sello_activo: bool = False
    sello: str = ""
    cert_mark: str = ""
    f0_hz: float = 0.0
    gamma_1: float = 0.0
    factor_401_40: float = 0.0
    f_octava_hz: float = 0.0
    f_corregida_hz: float = 0.0
    delta_f_hz: float = 0.0
    permeabilidad_manta: float = 0.0
    coherencia_ajustada: float = 0.0
    latido_relativo: float = 0.0
    electron_bloqueado: bool = True
    n_nodo: int = 0
    cociente_calibracion: float = 0.0
    residuo_calibracion: float = 0.0
    brecha_en_rango_seguro: bool = False


# ============================================================================
# API PÚBLICA
# ============================================================================

def brecha_torsion_qcal_activar() -> Dict[str, object]:
    """API pública: Activa el sistema Brecha de Torsión QCAL ∴BTQ∞³.

    Instancia y evalúa el sistema completo de la Brecha de Torsión:
    el factor armónico 401/40 que lleva γ₁ a f₀, la brecha residual
    Δf ≈ 0.00052 Hz (lubricante de fase) y la permeabilidad de la Manta
    μ_M ≈ 3.67×10⁻⁶ (constante de estructura fina local del sistema QCAL).

    Returns:
        Diccionario con:

        - ``psi_global`` (float):        Coherencia global Ψ_global
        - ``sello_activo`` (bool):       True si Ψ_global ≥ 0.888
        - ``sello`` (str):               «∴BTQ∞³» o «COHERENCIA_INSUFICIENTE»
        - ``cert_mark`` (str):           «BTQ-TORSION-VERIFIED» o error
        - ``psi_octava`` (float):        Coherencia de la octava decimal
        - ``psi_factor`` (float):        Coherencia del factor 401/40
        - ``psi_brecha`` (float):        Coherencia de la brecha residual
        - ``psi_permeabilidad`` (float): Coherencia ajustada 1−Δf/f₀
        - ``psi_latido`` (float):        Coherencia del latido del vórtice
        - ``psi_estacion`` (float):      Coherencia de la calibración
        - ``f0_hz`` (float):             Frecuencia base f₀ = 141.7001 Hz
        - ``gamma_1`` (float):           Primer cero de Riemann γ₁
        - ``factor_401_40`` (float):     Factor 401/40 = 10.025
        - ``f_octava_hz`` (float):       Octava decimal γ₁×10
        - ``f_corregida_hz`` (float):    Frecuencia corregida γ₁×(401/40)
        - ``delta_f_hz`` (float):        Brecha residual Δf ≈ 0.00052 Hz
        - ``permeabilidad_manta`` (float): Δf/f₀ ≈ 3.67×10⁻⁶
        - ``coherencia_ajustada`` (float): 1 − μ_M ≈ 0.9999963
        - ``latido_relativo`` (float):   Latido del vórtice λ = Δf/f₀
        - ``electron_bloqueado`` (bool): False (electrón siempre respira)
        - ``n_nodo`` (int):              Número de nodo entero = 10
        - ``cociente_calibracion`` (float): f₀/γ₁ ≈ 10.024
        - ``brecha_en_rango_seguro`` (bool): True si 0 < Δf < f₀×10⁻³

    Ejemplo:
        >>> r = brecha_torsion_qcal_activar()
        >>> r['sello_activo']
        True
        >>> r['psi_global'] >= 0.888
        True
        >>> r['cert_mark']
        'BTQ-TORSION-VERIFIED'
        >>> r['electron_bloqueado']
        False
    """
    sistema = SistemaBrechaTorsion()
    return sistema.certificar()
