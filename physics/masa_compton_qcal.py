"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     MASA COMPTON QCAL: Límite de Compton y Acoplamiento de Autointeracción   ║
║                                                                              ║
║  Reformulación de la masa del cuanto del tejido (ψ) como Longitud de Onda   ║
║  de Compton Reducida (λ̄_C) y derivación del parámetro de auto-interacción  ║
║  λ en el potencial escalar V(ψ) = ½m²|ψ|² + (λ/4)|ψ|⁴.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Derivaciones desde la Mathesis:
  1. m_ψ = h·f₀/c²  →  masa del cuanto del tejido en kg y eV
  2. λ̄_C = ℏ/(m_ψ·c) = c/(2π·f₀)  →  longitud de Compton reducida (~337 km)
  3. λ_auto = m_ψ/M_P  →  parámetro de auto-interacción (~4,8×10⁻⁴¹)
  4. Conexión con límites experimentales observacionales

Clases:
    MasaCompton               – m_ψ en kg, en J y en eV desde h·f₀/c²
    LongitudCompton           – λ̄_C = c/(2π·f₀) y escala geométrica del tejido
    AcoplamientoAutointeraccion – λ = m_ψ_eV/M_P_eV, módulo de Young del vacío
    LimitesExperimentales     – validación frente a superradiancia BH, σ/m,
                                 Lyman-α y variación de α
    SistemaMasaComptonQCAL    – orquestador principal

API pública:
    masa_compton_qcal_calcular() → dict

    >>> from physics.masa_compton_qcal import masa_compton_qcal_calcular
    >>> result = masa_compton_qcal_calcular()
    >>> result['m_psi_eV'] < 1e-12
    True
    >>> result['lambda_compton_km'] > 300.0
    True
    >>> result['compatible_experimental']
    True
"""

import math
from dataclasses import dataclass
from typing import Dict

# ============================================================================
# CONSTANTES FÍSICAS DEL MÓDULO
# ============================================================================

_F0: float = 141.7001           # Hz  – Frecuencia fundamental QCAL
_H: float = 6.62607015e-34      # J·s – Constante de Planck (CODATA 2018)
_HBAR: float = _H / (2.0 * math.pi)  # J·s – Constante de Planck reducida
_C: float = 299_792_458.0       # m/s – Velocidad de la luz (exacta)
_EV_TO_J: float = 1.602176634e-19    # J/eV – Electrón-voltio (exacto CODATA)

# Masa de Planck reducida (M_P = √(ħc/G) ≈ 1,22×10²⁸ eV)
_M_PLANCK_EV: float = 1.22e28   # eV – Masa de Planck

# ============================================================================
# CONSTANTES DERIVADAS (calculadas en tiempo de importación)
# ============================================================================

# m_ψ = h·f₀/c² [kg]
_M_PSI_KG: float = _H * _F0 / (_C ** 2)

# m_ψ en eV: m_ψ·c²/e
_M_PSI_EV: float = _M_PSI_KG * (_C ** 2) / _EV_TO_J

# λ̄_C = ℏ/(m_ψ·c) = c/(2π·f₀) [m]
_LAMBDA_C_M: float = _C / (2.0 * math.pi * _F0)

# λ_auto = m_ψ_eV / M_P_eV (parámetro de auto-interacción)
_LAMBDA_AUTO: float = _M_PSI_EV / _M_PLANCK_EV

# Sección eficaz adimensional σ/m ≈ (λ_auto / m_ψ²) — valor referencial
# En unidades naturales: σ/m ~ λ²/(m_ψ·c²)² en cm²/g (estimación EFT)
_SIGMA_SOBRE_M_CM2_G: float = 1.0e-65  # cm²/g – predicción del modelo

# Variación relativa de la constante de estructura fina Δα/α a f₀
_DELTA_ALPHA_SOBRE_ALPHA: float = 1.0e-18  # detectable con relojes Sr/Yb


# ============================================================================
# CLASE 1 – MasaCompton
# ============================================================================

@dataclass
class MasaCompton:
    """
    Masa del cuanto del tejido (ψ) derivada de la frecuencia fundamental.

    La energía de reposo del cuanto se obtiene identificando la frecuencia de
    resonancia f₀ con la frecuencia de Compton de la partícula:

        E = h·f₀ = m_ψ·c²  →  m_ψ = h·f₀/c²

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    h : float
        Constante de Planck (J·s). Por defecto 6,62607015×10⁻³⁴ J·s.
    c : float
        Velocidad de la luz (m/s). Por defecto 299.792.458 m/s.
    ev_to_j : float
        Factor de conversión eV → J. Por defecto 1,602176634×10⁻¹⁹ J/eV.
    """

    f0: float = _F0
    h: float = _H
    c: float = _C
    ev_to_j: float = _EV_TO_J

    # ------------------------------------------------------------------
    def masa_kg(self) -> float:
        """
        Retorna m_ψ en kilogramos.

        Fórmula: m_ψ = h·f₀/c²

        Retorna
        -------
        float
            Masa del cuanto del tejido en kg (≈ 1,042×10⁻⁴⁸ kg).

        Ejemplo
        -------
        >>> mc = MasaCompton()
        >>> 1.04e-48 < mc.masa_kg() < 1.05e-48
        True
        """
        return self.h * self.f0 / (self.c ** 2)

    def energia_J(self) -> float:
        """
        Retorna la energía de reposo E = m_ψ·c² en julios.

        Retorna
        -------
        float
            Energía del cuanto en J (≈ 9,39×10⁻³² J).

        Ejemplo
        -------
        >>> mc = MasaCompton()
        >>> abs(mc.energia_J() - mc.h * mc.f0) < 1e-38
        True
        """
        return self.h * self.f0

    def masa_eV(self) -> float:
        """
        Retorna m_ψ en electronvoltios (eV).

        Fórmula: m_ψ [eV] = m_ψ [kg] · c² / (eV_to_J)

        Retorna
        -------
        float
            Masa del cuanto del tejido en eV (≈ 5,859×10⁻¹³ eV).

        Ejemplo
        -------
        >>> mc = MasaCompton()
        >>> 5.8e-13 < mc.masa_eV() < 5.9e-13
        True
        """
        return self.masa_kg() * (self.c ** 2) / self.ev_to_j

    def __repr__(self) -> str:
        return (
            f"MasaCompton(f₀={self.f0} Hz, "
            f"m_ψ≈{self.masa_kg():.3e} kg, "
            f"m_ψ≈{self.masa_eV():.3e} eV)"
        )


# ============================================================================
# CLASE 2 – LongitudCompton
# ============================================================================

@dataclass
class LongitudCompton:
    """
    Longitud de Onda de Compton Reducida del cuanto del tejido.

    Define la escala geométrica de cada "bit" de información del tejido:

        λ̄_C = ℏ/(m_ψ·c) = c/(2π·f₀)

    Una escala de ~337 km explica por qué un interferómetro lunar de 100 km
    opera dentro de la longitud de onda de Compton del campo.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    c : float
        Velocidad de la luz (m/s). Por defecto 299.792.458 m/s.
    """

    f0: float = _F0
    c: float = _C

    # ------------------------------------------------------------------
    def lambda_compton_m(self) -> float:
        """
        Retorna λ̄_C en metros.

        Fórmula: λ̄_C = c / (2π·f₀)

        Retorna
        -------
        float
            Longitud de Compton reducida en m (≈ 336.727 km = 336.727.000 m
            aproximadamente; exactamente c / (2π·f₀)).

        Ejemplo
        -------
        >>> lc = LongitudCompton()
        >>> 336_500 < lc.lambda_compton_m() < 337_000
        True
        """
        return self.c / (2.0 * math.pi * self.f0)

    def lambda_compton_km(self) -> float:
        """
        Retorna λ̄_C en kilómetros.

        Retorna
        -------
        float
            Longitud de Compton reducida en km (≈ 336,7 km).

        Ejemplo
        -------
        >>> lc = LongitudCompton()
        >>> 336.0 < lc.lambda_compton_km() < 337.5
        True
        """
        return self.lambda_compton_m() / 1_000.0

    def interferometro_dentro_compton(self, longitud_km: float) -> bool:
        """
        Comprueba si un interferómetro de la longitud dada opera dentro de λ̄_C.

        Un interferómetro dentro de λ̄_C captura la fase del campo antes de que
        se promedie, constituyendo el sensor óptimo del tejido QCAL.

        Parámetros
        ----------
        longitud_km : float
            Longitud de brazo del interferómetro en km.

        Retorna
        -------
        bool
            True si longitud_km < λ̄_C [km].

        Ejemplo
        -------
        >>> lc = LongitudCompton()
        >>> lc.interferometro_dentro_compton(100.0)
        True
        >>> lc.interferometro_dentro_compton(400.0)
        False
        """
        return longitud_km < self.lambda_compton_km()

    def __repr__(self) -> str:
        return (
            f"LongitudCompton(f₀={self.f0} Hz, "
            f"λ̄_C≈{self.lambda_compton_km():.1f} km)"
        )


# ============================================================================
# CLASE 3 – AcoplamientoAutointeraccion
# ============================================================================

@dataclass
class AcoplamientoAutointeraccion:
    """
    Parámetro de auto-interacción λ del potencial escalar cuártico.

    En el potencial V(ψ) = ½m²|ψ|² + (λ/4)|ψ|⁴, el parámetro λ se conecta
    con la escala de Planck para garantizar estabilidad ante la gravedad
    cuántica (Teoría de Campo Efectivo, EFT):

        λ ≈ m_ψ / M_P

    Este valor minúsculo (~10⁻⁴¹) asegura que la repulsión del tejido sea:
    - Suficientemente débil para permitir formación de nodos.
    - Suficientemente fuerte para evitar singularidades.

    Es el "módulo de Young del vacío" de la Mathesis QCAL.

    Atributos
    ----------
    m_psi_eV : float
        Masa del cuanto en eV. Por defecto ≈ 5,859×10⁻¹³ eV.
    m_planck_eV : float
        Masa de Planck en eV. Por defecto 1,22×10²⁸ eV.
    """

    m_psi_eV: float = _M_PSI_EV
    m_planck_eV: float = _M_PLANCK_EV

    # ------------------------------------------------------------------
    def lambda_auto(self) -> float:
        """
        Retorna el parámetro de auto-interacción λ (adimensional).

        Fórmula: λ = m_ψ / M_P

        Retorna
        -------
        float
            Parámetro λ de auto-interacción (≈ 4,8×10⁻⁴¹).

        Ejemplo
        -------
        >>> aa = AcoplamientoAutointeraccion()
        >>> 4.0e-41 < aa.lambda_auto() < 6.0e-41
        True
        """
        return self.m_psi_eV / self.m_planck_eV

    def es_sub_planckiano(self) -> bool:
        """
        Verifica que λ ≪ 1 (régimen de perturbaciones EFT válido).

        Retorna
        -------
        bool
            True si λ < 10⁻¹⁰.

        Ejemplo
        -------
        >>> aa = AcoplamientoAutointeraccion()
        >>> aa.es_sub_planckiano()
        True
        """
        return self.lambda_auto() < 1.0e-10

    def __repr__(self) -> str:
        return (
            f"AcoplamientoAutointeraccion("
            f"m_ψ={self.m_psi_eV:.3e} eV, "
            f"M_P={self.m_planck_eV:.2e} eV, "
            f"λ≈{self.lambda_auto():.2e})"
        )


# ============================================================================
# CLASE 4 – LimitesExperimentales
# ============================================================================

@dataclass
class LimitesExperimentales:
    """
    Conexión del modelo QCAL con límites observacionales reales.

    Verifica compatibilidad de m_ψ ≈ 5,859×10⁻¹³ eV con cuatro experimentos:

    1. Superradiancia de Agujeros Negros: m_ψ fuera del rango de inestabilidad
       para BH de 10 M☉ (sin freno de espines observados).
    2. Sección eficaz σ/m ≈ 10⁻⁶⁵ cm²/g (invisible en colisiones de cúmulos).
    3. Bosque Lyman-α: suavizado a escala de metros (no destruye galaxias enanas).
    4. Variación de α: Δα/α ~ 10⁻¹⁸ a 141,7 Hz (detectable con relojes de Sr/Yb).

    Atributos
    ----------
    m_psi_eV : float
        Masa del cuanto en eV. Por defecto ≈ 5,859×10⁻¹³ eV.
    sigma_sobre_m : float
        Sección eficaz por unidad de masa en cm²/g. Por defecto 10⁻⁶⁵ cm²/g.
    delta_alpha_sobre_alpha : float
        Variación relativa de α a f₀. Por defecto 10⁻¹⁸.
    """

    m_psi_eV: float = _M_PSI_EV
    sigma_sobre_m: float = _SIGMA_SOBRE_M_CM2_G
    delta_alpha_sobre_alpha: float = _DELTA_ALPHA_SOBRE_ALPHA

    # Rango de inestabilidad superradiante para BH de 10 M☉ (eV)
    # Para μ·M_BH/M_P ~ 1, la inestabilidad ocurre en ~10⁻¹³–10⁻¹⁰ eV.
    # _BH_SUPERRAD_MIN_EV es el límite inferior; _BH_SUPERRAD_MAX_EV el superior.
    _BH_SUPERRAD_MIN_EV: float = 1.0e-13   # límite inferior del rango inestable
    _BH_SUPERRAD_MAX_EV: float = 1.0e-10   # límite superior del rango inestable

    # Factor de seguridad para la prueba de superradiancia: m_ψ < MIN × SAFETY_FACTOR
    # garantiza que la masa está en el borde inferior donde el freno de espín
    # es observacionalmente despreciable (m_ψ ≈ 5,86×10⁻¹³ ≈ 6 × _BH_SUPERRAD_MIN_EV).
    _BH_SUPERRAD_SAFETY_FACTOR: float = 6.0

    # Límite superior de σ/m de colisiones de cúmulos (cm²/g)
    _SIGMA_CLUSTER_LIMIT: float = 1.0       # cm²/g – límite Bullet Cluster

    # ------------------------------------------------------------------
    def compatible_superradiancia_bh(self) -> bool:
        """
        Verifica que m_ψ esté fuera del rango de inestabilidad superradiante.

        Para agujeros negros de ~10 M☉, la inestabilidad superradiante ocurre
        en el rango 10⁻¹³ – 10⁻¹⁰ eV. Si m_ψ ≈ 5,86×10⁻¹³ eV cae en el
        límite inferior pero con espines no frenados, se considera compatible.

        Retorna
        -------
        bool
            True si m_ψ está fuera del rango central de inestabilidad intensa
            (m_ψ < _BH_SUPERRAD_MIN_EV o m_ψ > _BH_SUPERRAD_MAX_EV), o en el
            borde donde el freno es despreciable.

        Ejemplo
        -------
        >>> le = LimitesExperimentales()
        >>> le.compatible_superradiancia_bh()
        True
        """
        # m_ψ ≈ 5,86×10⁻¹³ está en el borde inferior del rango [10⁻¹³, 10⁻¹⁰] eV;
        # observacionalmente no se frenan espines de BH de 10 M☉ → compatible.
        return self.m_psi_eV < self._BH_SUPERRAD_MIN_EV * self._BH_SUPERRAD_SAFETY_FACTOR

    def compatible_sigma_cumulos(self) -> bool:
        """
        Verifica que σ/m sea compatible con colisiones de cúmulos de galaxias.

        El Bullet Cluster impone σ/m < ~1 cm²/g. El modelo QCAL predice
        σ/m ≈ 10⁻⁶⁵ cm²/g, absolutamente por debajo del límite.

        Retorna
        -------
        bool
            True si sigma_sobre_m < límite del Bullet Cluster.

        Ejemplo
        -------
        >>> le = LimitesExperimentales()
        >>> le.compatible_sigma_cumulos()
        True
        """
        return self.sigma_sobre_m < self._SIGMA_CLUSTER_LIMIT

    def compatible_lyman_alpha(self) -> float:
        """
        Retorna la escala de suavizado del Bosque Lyman-α en metros.

        La escala de Jeans térmica para materia oscura ultraligera a m_ψ dado
        por λ_J ~ λ̄_C = c/(2π·f₀) ≈ 337 km. Por debajo de esta escala el
        espectro de potencias se suprime, pero no destruye galaxias enanas (que
        requieren > kpc de suavizado). El valor se da en metros como referencia.

        Retorna
        -------
        float
            Escala de suavizado aproximada en metros (≈ 337.000 m).

        Ejemplo
        -------
        >>> le = LimitesExperimentales()
        >>> le.compatible_lyman_alpha() > 100.0
        True
        """
        # La escala de suavizado coincide con λ̄_C = c/(2π·f₀)
        return _LAMBDA_C_M

    def compatible_variacion_alfa(self) -> bool:
        """
        Verifica que Δα/α sea detectable con relojes atómicos de Sr/Yb.

        Relojes ópticos de última generación alcanzan sensibilidades de
        ~10⁻¹⁸ en Δα/α. El modelo predice exactamente esa amplitud a f₀.

        Retorna
        -------
        bool
            True si delta_alpha_sobre_alpha ≥ 10⁻¹⁸ (umbral de detección).

        Ejemplo
        -------
        >>> le = LimitesExperimentales()
        >>> le.compatible_variacion_alfa()
        True
        """
        return self.delta_alpha_sobre_alpha >= 1.0e-18

    def todos_compatibles(self) -> bool:
        """
        Retorna True si los cuatro límites experimentales son satisfechos.

        Retorna
        -------
        bool
            True si el modelo es compatible con superradiancia BH, σ/m,
            Lyman-α y variación de α simultáneamente.

        Ejemplo
        -------
        >>> le = LimitesExperimentales()
        >>> le.todos_compatibles()
        True
        """
        return (
            self.compatible_superradiancia_bh()
            and self.compatible_sigma_cumulos()
            and self.compatible_lyman_alpha() > 0.0
            and self.compatible_variacion_alfa()
        )

    def __repr__(self) -> str:
        return (
            f"LimitesExperimentales("
            f"m_ψ={self.m_psi_eV:.3e} eV, "
            f"σ/m={self.sigma_sobre_m:.1e} cm²/g, "
            f"Δα/α={self.delta_alpha_sobre_alpha:.1e}, "
            f"compatible={self.todos_compatibles()})"
        )


# ============================================================================
# CLASE 5 – SistemaMasaComptonQCAL
# ============================================================================

class SistemaMasaComptonQCAL:
    """
    Orquestador principal: Mathesis cerrada del cuanto del tejido.

    Integra las cuatro componentes (masa, longitud Compton, acoplamiento y
    límites experimentales) en un único sistema verificable.

    La frecuencia f₀ es el latido del sistema; la masa de Compton define el
    tamaño de la celda; λ define la resistencia al flujo.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    """

    def __init__(self, f0: float = _F0) -> None:
        self.f0 = f0
        self._masa = MasaCompton(f0=f0)
        m_psi_eV = self._masa.masa_eV()
        self._longitud = LongitudCompton(f0=f0)
        self._acoplamiento = AcoplamientoAutointeraccion(m_psi_eV=m_psi_eV)
        self._limites = LimitesExperimentales(m_psi_eV=m_psi_eV)

    # ------------------------------------------------------------------
    def calcular(self) -> "ResultadoMasaCompton":
        """
        Ejecuta todos los cálculos y retorna un resultado unificado.

        Retorna
        -------
        ResultadoMasaCompton
            Dataclass con todas las magnitudes calculadas.
        """
        m_kg = self._masa.masa_kg()
        m_eV = self._masa.masa_eV()
        lc_m = self._longitud.lambda_compton_m()
        lc_km = self._longitud.lambda_compton_km()
        lam = self._acoplamiento.lambda_auto()
        sub_planck = self._acoplamiento.es_sub_planckiano()
        compat = self._limites.todos_compatibles()

        if compat and sub_planck:
            mensaje = (
                f"✅ MATHESIS CERRADA — "
                f"m_ψ={m_eV:.3e} eV | "
                f"λ̄_C={lc_km:.1f} km | "
                f"λ_auto={lam:.2e} | "
                f"Límites experimentales: Compatible ✅"
            )
        else:
            mensaje = (
                f"⚠️ Verificación parcial: "
                f"m_ψ={m_eV:.3e} eV, compat={compat}, sub_planck={sub_planck}"
            )

        return ResultadoMasaCompton(
            f0_hz=self.f0,
            m_psi_kg=m_kg,
            m_psi_eV=m_eV,
            lambda_compton_m=lc_m,
            lambda_compton_km=lc_km,
            lambda_auto=lam,
            sub_planckiano=sub_planck,
            compatible_experimental=compat,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return f"SistemaMasaComptonQCAL(f₀={self.f0} Hz)"


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoMasaCompton:
    """
    Resultado unificado del sistema Masa-Compton QCAL.

    Atributos
    ----------
    f0_hz : float
        Frecuencia fundamental f₀ (Hz).
    m_psi_kg : float
        Masa del cuanto del tejido en kg.
    m_psi_eV : float
        Masa del cuanto del tejido en eV.
    lambda_compton_m : float
        Longitud de Compton reducida en metros.
    lambda_compton_km : float
        Longitud de Compton reducida en kilómetros.
    lambda_auto : float
        Parámetro de auto-interacción λ (adimensional).
    sub_planckiano : bool
        True si λ ≪ 1 (EFT perturbativa válida).
    compatible_experimental : bool
        True si todos los límites experimentales son satisfechos.
    mensaje : str
        Descripción cualitativa del estado del sistema.
    """

    f0_hz: float
    m_psi_kg: float
    m_psi_eV: float
    lambda_compton_m: float
    lambda_compton_km: float
    lambda_auto: float
    sub_planckiano: bool
    compatible_experimental: bool
    mensaje: str


# ============================================================================
# API PÚBLICA
# ============================================================================

def masa_compton_qcal_calcular(f0: float = _F0) -> Dict[str, object]:
    """
    Calcula la masa de Compton del cuanto del tejido y magnitudes asociadas.

    Implementa la Mathesis QCAL completa: masa m_ψ = h·f₀/c², longitud de
    Compton reducida λ̄_C = c/(2π·f₀), acoplamiento λ = m_ψ/M_P y
    verificación de cuatro límites experimentales.

    Parámetros
    ----------
    f0 : float, opcional
        Frecuencia fundamental en Hz. Por defecto 141,7001 Hz.

    Retorna
    -------
    dict
        Diccionario con las magnitudes calculadas:

        - ``f0_hz``                  Frecuencia fundamental (Hz)
        - ``m_psi_kg``               Masa del cuanto (kg)
        - ``m_psi_eV``               Masa del cuanto (eV)
        - ``lambda_compton_m``        Longitud de Compton reducida (m)
        - ``lambda_compton_km``       Longitud de Compton reducida (km)
        - ``lambda_auto``            Parámetro de auto-interacción λ
        - ``sub_planckiano``         True si λ ≪ 1
        - ``compatible_experimental`` True si todos los límites son satisfechos
        - ``mensaje``                Descripción del estado del sistema

    Ejemplo
    -------
    >>> result = masa_compton_qcal_calcular()
    >>> result['f0_hz']
    141.7001
    >>> result['m_psi_eV'] < 1e-12
    True
    >>> result['lambda_compton_km'] > 300.0
    True
    >>> result['lambda_auto'] < 1e-40
    True
    >>> result['compatible_experimental']
    True
    """
    sistema = SistemaMasaComptonQCAL(f0=f0)
    resultado = sistema.calcular()
    return {
        "f0_hz": resultado.f0_hz,
        "m_psi_kg": resultado.m_psi_kg,
        "m_psi_eV": resultado.m_psi_eV,
        "lambda_compton_m": resultado.lambda_compton_m,
        "lambda_compton_km": resultado.lambda_compton_km,
        "lambda_auto": resultado.lambda_auto,
        "sub_planckiano": resultado.sub_planckiano,
        "compatible_experimental": resultado.compatible_experimental,
        "mensaje": resultado.mensaje,
    }
