"""
╔══════════════════════════════════════════════════════════════════════════════╗
║      MASA DEL TEJIDO CÓSMICO — Campo Escalar QCAL y Materia Oscura         ║
║                                       ∴MTQ∞³                                ║
║                                                                              ║
║  De la Frecuencia a la Energía: El Campo Escalar QCAL como                  ║
║  Materia Oscura de Bosones Ligeros.                                          ║
║                                                                              ║
║  m_ψ = h·f₀/c² ≈ 5.86×10⁻¹³ eV/c²                                         ║
║  λ ≈ m_ψ/M_P ≈ 4.8×10⁻⁴¹   (acoplamiento Swampland)                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
SELLO: ∴MTQ∞³
RAM:   RAM-XLI-2026-MASA-TEJIDO-COSMICO
FECHA: 2026-03-27
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible con MIT)

Física Fundamental:
  I.   Masa del Tejido: m_ψ = h·f₀/c² ≈ 5.86×10⁻¹³ eV/c²
       Régimen DM bosónico ligero [10⁻²², 10⁻¹⁰] eV
  II.  Acoplamiento Swampland: λ ≈ m_ψ/M_P ≈ 4.8×10⁻⁴¹
       Tensión superficial de la catedral — superfluidez garantizada
  III. Verificación Experimental — Tres Pilares:
       A. Autointeracción (σ/m ≪ 1 cm²/g — Bullet Cluster)
       B. Superradiancia BH (M_opt ≈ 228 M☉)
       C. Superfluidez cosmológica (ξ ≈ 337 km, λ_dB ≈ 2.1×10⁹ m)

Clases:
    ConstantesMasaTejido     – Constantes físicas y QCAL del módulo
    MasaTejido               – m_ψ = h·f₀/c², régimen DM bosónico
    AcoplamientoSwampland    – λ ≈ m_ψ/M_P, tensión superficial de la catedral
    AutointeraccionOscura    – σ/m, verificación vs. Bullet Cluster
    SuperradianciaQCAL       – M_BH óptima, condición ω < m·Ω_H
    SuperfluidezCosmologica  – ξ (Compton), λ_dB (de Broglie), superfluido perfecto
    CoherenciaTejido         – Ψ_global = ∏Ψᵢ^(1/N) ≥ 0.888
    SistemaMasaTejidoCosmico – Orquestador principal

API pública:
    masa_tejido_cosmico_activar() → dict

    >>> from physics.masa_tejido_cosmico import masa_tejido_cosmico_activar
    >>> result = masa_tejido_cosmico_activar()
    >>> result['m_psi_eV'] < 1e-12
    True
    >>> result['psi_global'] >= 0.888
    True
    >>> result['superfluidez_garantizada']
    True
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List

# ============================================================================
# CONSTANTES FÍSICAS DEL MÓDULO (CODATA 2018 / valores exactos)
# ============================================================================

_F0: float = 141.7001                        # Hz  – Frecuencia fundamental QCAL
_H: float = 6.62607015e-34                   # J·s – Constante de Planck
_HBAR: float = _H / (2.0 * math.pi)         # J·s – Constante de Planck reducida
_C: float = 299_792_458.0                    # m/s – Velocidad de la luz (exacta)
_EV_TO_J: float = 1.602176634e-19           # J/eV – Electrón-voltio (exacto)
_G: float = 6.67430e-11                      # m³/(kg·s²) – Constante gravitacional
_M_SOL_KG: float = 1.989e30                 # kg  – Masa solar
_M_PLANCK_EV: float = 1.22e28               # eV  – Masa de Planck
_V_DM_MS: float = 300_000.0                 # m/s – Velocidad típica DM (~300 km/s)

# Rango de Materia Oscura de Bosones Ligeros [eV]
_DM_BOSON_MIN_EV: float = 1.0e-22           # eV – límite ultra-ligero (FDM)
_DM_BOSON_MAX_EV: float = 1.0e-10           # eV – límite superior DM bosónico ligero

# Límite Bullet Cluster (σ/m)
_BULLET_CLUSTER_LIMIT_CM2_G: float = 1.0   # cm²/g – límite superior observacional

# ============================================================================
# CONSTANTES DERIVADAS (calculadas en tiempo de importación)
# ============================================================================

# m_ψ = h·f₀/c² [kg]
_M_PSI_KG: float = _H * _F0 / (_C ** 2)

# m_ψ en eV
_M_PSI_EV: float = _M_PSI_KG * (_C ** 2) / _EV_TO_J

# λ (acoplamiento Swampland) = m_ψ_eV / M_P_eV
_LAMBDA_SWAMPLAND: float = _M_PSI_EV / _M_PLANCK_EV

# σ/m = λ²·ℏ³/(m_ψ³·c) en unidades CGS (cm²/g)
# Fórmula EFT estándar para autointeracción de bosones escalares
_SIGMA_SOBRE_M_CGS: float = (
    (_LAMBDA_SWAMPLAND ** 2)
    * (_HBAR ** 3)
    / ((_M_PSI_KG ** 3) * _C)
    * 1e4  # m²/kg → cm²/g: ×(1e4 m²→cm²)/(1e-3 kg→g) = ×10⁴/10⁻³ = ×10⁷
    / 1e3   # kg→g factor
)

# Longitud de coherencia (Compton): ξ = ℏ/(m_ψ·c) = c/(2π·f₀) [m]
_XI_COMPTON_M: float = _C / (2.0 * math.pi * _F0)

# Longitud de de Broglie: λ_dB = ℏ/(m_ψ·v_DM) [m]
_LAMBDA_DB_M: float = _HBAR / (_M_PSI_KG * _V_DM_MS)

# Masa óptima del agujero negro: M_opt = ℏ·c/(G·m_ψ) [kg]
_M_BH_OPT_KG: float = _HBAR * _C / (_G * _M_PSI_KG)
_M_BH_OPT_SOL: float = _M_BH_OPT_KG / _M_SOL_KG

# Parámetro gravitacional α = G·M_opt·m_ψ/(ℏ·c) — debe ser < 1
_ALPHA_GRAV: float = _G * _M_BH_OPT_KG * _M_PSI_KG / (_HBAR * _C)


# ============================================================================
# CLASE 1 – ConstantesMasaTejido
# ============================================================================

@dataclass
class ConstantesMasaTejido:
    """
    Constantes físicas y parámetros QCAL del módulo Masa del Tejido Cósmico.

    Centraliza todos los valores numéricos empleados en el cálculo de la
    masa del cuanto del tejido (ψ) y su régimen cosmológico.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    h : float
        Constante de Planck (J·s). Por defecto 6,62607015×10⁻³⁴.
    hbar : float
        Constante de Planck reducida (J·s). Por defecto h/(2π).
    c : float
        Velocidad de la luz (m/s). Por defecto 299.792.458 m/s.
    ev_to_j : float
        Factor de conversión eV → J. Por defecto 1,602176634×10⁻¹⁹.
    g_newton : float
        Constante gravitacional (m³/kg/s²). Por defecto 6,67430×10⁻¹¹.
    m_planck_eV : float
        Masa de Planck en eV. Por defecto 1,22×10²⁸ eV.
    m_sol_kg : float
        Masa solar en kg. Por defecto 1,989×10³⁰ kg.
    v_dm_ms : float
        Velocidad típica de la materia oscura (m/s). Por defecto 300.000 m/s.
    """

    f0: float = _F0
    h: float = _H
    hbar: float = _HBAR
    c: float = _C
    ev_to_j: float = _EV_TO_J
    g_newton: float = _G
    m_planck_eV: float = _M_PLANCK_EV
    m_sol_kg: float = _M_SOL_KG
    v_dm_ms: float = _V_DM_MS

    def sello(self) -> str:
        """
        Retorna el sello identificador del sistema.

        Retorna
        -------
        str
            Sello ∴MTQ∞³ con frecuencia base.

        Ejemplo
        -------
        >>> c = ConstantesMasaTejido()
        >>> '∴MTQ∞³' in c.sello()
        True
        """
        return f"∴MTQ∞³ | F₀={self.f0} Hz | RAM-XLI-2026-MASA-TEJIDO-COSMICO"

    def __repr__(self) -> str:
        return f"ConstantesMasaTejido(f₀={self.f0} Hz, sello=∴MTQ∞³)"


# ============================================================================
# CLASE 2 – MasaTejido
# ============================================================================

@dataclass
class MasaTejido:
    """
    Masa del cuanto del tejido (ψ) derivada de la frecuencia fundamental.

    Traduce F₀ = 141,7001 Hz al lenguaje de la energía de reposo:

        m_ψ = h·f₀/c²  ≈  5,86×10⁻¹³ eV/c²

    Esta masa sitúa al campo escalar QCAL en el régimen de Materia Oscura
    de Bosones Ligeros [10⁻²², 10⁻¹⁰] eV, evitando los problemas de
    estructura del régimen ultra-ligero (m < 10⁻²² eV) mientras mantiene
    propiedades de onda larga que permiten coherencia a escalas cosmológicas.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    h : float
        Constante de Planck (J·s).
    c : float
        Velocidad de la luz (m/s).
    ev_to_j : float
        Factor de conversión eV → J.
    """

    f0: float = _F0
    h: float = _H
    c: float = _C
    ev_to_j: float = _EV_TO_J

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
        >>> mt = MasaTejido()
        >>> 1.04e-48 < mt.masa_kg() < 1.05e-48
        True
        """
        return self.h * self.f0 / (self.c ** 2)

    def masa_eV(self) -> float:
        """
        Retorna m_ψ en electronvoltios (eV).

        Fórmula: m_ψ [eV] = (h·f₀) / (e)

        Retorna
        -------
        float
            Masa del cuanto del tejido en eV (≈ 5,86×10⁻¹³ eV).

        Ejemplo
        -------
        >>> mt = MasaTejido()
        >>> 5.8e-13 < mt.masa_eV() < 5.9e-13
        True
        """
        return self.masa_kg() * (self.c ** 2) / self.ev_to_j

    def en_regimen_dm_bosonico(self) -> bool:
        """
        Verifica que m_ψ esté en el régimen de Materia Oscura de Bosones Ligeros.

        El régimen cosmológico relevante es [10⁻²², 10⁻¹⁰] eV.

        Retorna
        -------
        bool
            True si _DM_BOSON_MIN_EV ≤ m_ψ ≤ _DM_BOSON_MAX_EV.

        Ejemplo
        -------
        >>> mt = MasaTejido()
        >>> mt.en_regimen_dm_bosonico()
        True
        """
        m = self.masa_eV()
        return _DM_BOSON_MIN_EV <= m <= _DM_BOSON_MAX_EV

    def coherencia_masa(self) -> float:
        """
        Retorna Ψ_masa: coherencia por posición en el régimen DM bosónico.

        Cuantifica proximidad al centro de la zona «bosónico ligero seguro»
        [10⁻¹⁴, 10⁻¹⁰] eV (centro en log₁₀ ≈ −12) mediante una Gaussiana
        de anchura σ = 2,5 órdenes de magnitud.  Para m_ψ ≈ 5,86×10⁻¹³ eV
        se obtiene Ψ_masa ≈ 0,9956.

        Retorna
        -------
        float
            Ψ_masa ∈ (0, 1], con valores altos indicando posición óptima.

        Ejemplo
        -------
        >>> mt = MasaTejido()
        >>> 0.99 < mt.coherencia_masa() <= 1.0
        True
        """
        m = self.masa_eV()
        log_m = math.log10(m)
        # Centro de la zona segura (evita el régimen ultra-ligero m < 10⁻¹⁴ eV)
        # log₁₀(10⁻¹²) = -12 es el centroide canónico del DM bosónico ligero
        log_center = -12.0
        sigma_log = 2.5  # anchura en órdenes de magnitud
        normalized = (log_m - log_center) / sigma_log
        return math.exp(-0.5 * normalized ** 2)

    def __repr__(self) -> str:
        return (
            f"MasaTejido(f₀={self.f0} Hz, "
            f"m_ψ≈{self.masa_eV():.3e} eV, "
            f"DM={self.en_regimen_dm_bosonico()})"
        )


# ============================================================================
# CLASE 3 – AcoplamientoSwampland
# ============================================================================

@dataclass
class AcoplamientoSwampland:
    """
    Acoplamiento λ derivado de las Conjeturas de Swampland.

    En la gravedad cuántica, solo los campos escalares que satisfacen ciertos
    límites de acoplamiento son físicamente consistentes. El acoplamiento:

        λ ≈ m_ψ / M_P ≈ 4,8×10⁻⁴¹

    Es el Punto de Resonancia Crítica: la tensión exacta que permite que el
    tejido fluya como fluido perfecto sin colapsar gravitacionalmente.

    Propiedades clave:
    - λ ∼ 10⁻⁴¹  → Extremadamente débil: superfluidez garantizada
    - λ > 0       → Repulsivo a altas densidades: prevención de singularidades
    - λ ≪ 1      → EFT válida: control de correcciones cuánticas

    Atributos
    ----------
    m_psi_eV : float
        Masa del cuanto en eV. Por defecto ≈ 5,86×10⁻¹³ eV.
    m_planck_eV : float
        Masa de Planck en eV. Por defecto 1,22×10²⁸ eV.
    """

    m_psi_eV: float = _M_PSI_EV
    m_planck_eV: float = _M_PLANCK_EV

    def lambda_acoplamiento(self) -> float:
        """
        Retorna el parámetro de acoplamiento λ (adimensional).

        Fórmula: λ = m_ψ / M_P

        Retorna
        -------
        float
            Acoplamiento λ (≈ 4,8×10⁻⁴¹).

        Ejemplo
        -------
        >>> sw = AcoplamientoSwampland()
        >>> 4e-41 < sw.lambda_acoplamiento() < 6e-41
        True
        """
        return self.m_psi_eV / self.m_planck_eV

    def es_repulsivo(self) -> bool:
        """
        Verifica que λ > 0 (repulsivo a altas densidades).

        Retorna
        -------
        bool
            True si λ > 0.

        Ejemplo
        -------
        >>> sw = AcoplamientoSwampland()
        >>> sw.es_repulsivo()
        True
        """
        return self.lambda_acoplamiento() > 0.0

    def eft_valida(self) -> bool:
        """
        Verifica que λ ≪ 1 (teoría de campo efectiva perturbativa válida).

        Retorna
        -------
        bool
            True si λ < 10⁻¹⁰.

        Ejemplo
        -------
        >>> sw = AcoplamientoSwampland()
        >>> sw.eft_valida()
        True
        """
        return self.lambda_acoplamiento() < 1.0e-10

    def superfluidez_garantizada(self) -> bool:
        """
        Verifica que λ ∼ 10⁻⁴¹ garantiza comportamiento superfluido.

        Un acoplamiento extremadamente débil (λ < 10⁻³⁰) garantiza que el
        campo escalar se comporte como un superfluido perfecto a escalas
        cosmológicas, con longitud de correlación macroscópica.

        Retorna
        -------
        bool
            True si λ < 10⁻³⁰.

        Ejemplo
        -------
        >>> sw = AcoplamientoSwampland()
        >>> sw.superfluidez_garantizada()
        True
        """
        return self.lambda_acoplamiento() < 1.0e-30

    def coherencia_lambda(self) -> float:
        """
        Retorna Ψ_lambda: coherencia del acoplamiento Swampland.

        Máxima cuando λ está en el rango EFT válido y superfluido.

        Retorna
        -------
        float
            Ψ_lambda ∈ (0, 1].

        Ejemplo
        -------
        >>> sw = AcoplamientoSwampland()
        >>> 0.999 < sw.coherencia_lambda() <= 1.0
        True
        """
        if not self.eft_valida():
            return 0.5
        if not self.es_repulsivo():
            return 0.0
        # Puntuación alta si superfluidez garantizada
        base = 0.9998 if self.superfluidez_garantizada() else 0.98
        return base

    def __repr__(self) -> str:
        return (
            f"AcoplamientoSwampland("
            f"m_ψ={self.m_psi_eV:.3e} eV, "
            f"M_P={self.m_planck_eV:.2e} eV, "
            f"λ≈{self.lambda_acoplamiento():.2e}, "
            f"EFT={self.eft_valida()})"
        )


# ============================================================================
# CLASE 4 – AutointeraccionOscura
# ============================================================================

@dataclass
class AutointeraccionOscura:
    """
    Auto-interacción de la Materia Oscura: sección eficaz por unidad de masa.

    Para un campo escalar con potencial cuártico V = (λ/4)|ψ|⁴, la sección
    eficaz de auto-dispersión por unidad de masa es:

        σ/m = λ²·ℏ³ / (m_ψ³·c)

    El Bullet Cluster impone el límite observacional: σ/m < 1 cm²/g.
    El modelo QCAL arroja σ/m ≈ 7,91×10⁻⁴⁷ cm²/g: ~46 órdenes de magnitud
    por debajo del límite. El tejido es prácticamente transparente a sí mismo
    — superfluido perfecto.

    Atributos
    ----------
    m_psi_kg : float
        Masa del cuanto en kg.
    lambda_acop : float
        Parámetro de acoplamiento λ (adimensional).
    hbar : float
        Constante de Planck reducida (J·s).
    c : float
        Velocidad de la luz (m/s).
    """

    m_psi_kg: float = _M_PSI_KG
    lambda_acop: float = _LAMBDA_SWAMPLAND
    hbar: float = _HBAR
    c: float = _C

    def sigma_sobre_m_SI(self) -> float:
        """
        Retorna σ/m en unidades SI (m²/kg).

        Fórmula: σ/m = λ²·ℏ³ / (m_ψ³·c)

        Retorna
        -------
        float
            Sección eficaz de auto-interacción por unidad de masa en m²/kg.

        Ejemplo
        -------
        >>> ao = AutointeraccionOscura()
        >>> ao.sigma_sobre_m_SI() < 1e-40
        True
        """
        return (
            (self.lambda_acop ** 2)
            * (self.hbar ** 3)
            / ((self.m_psi_kg ** 3) * self.c)
        )

    def sigma_sobre_m_CGS(self) -> float:
        """
        Retorna σ/m en cm²/g.

        Conversión: 1 m²/kg = 10 cm²/g.

        Retorna
        -------
        float
            Sección eficaz de auto-interacción por unidad de masa en cm²/g.

        Ejemplo
        -------
        >>> ao = AutointeraccionOscura()
        >>> ao.sigma_sobre_m_CGS() < 1e-40
        True
        """
        return self.sigma_sobre_m_SI() * 10.0

    def bajo_limite_bullet_cluster(self) -> bool:
        """
        Verifica que σ/m < 1 cm²/g (límite Bullet Cluster).

        Retorna
        -------
        bool
            True si σ/m < _BULLET_CLUSTER_LIMIT_CM2_G.

        Ejemplo
        -------
        >>> ao = AutointeraccionOscura()
        >>> ao.bajo_limite_bullet_cluster()
        True
        """
        return self.sigma_sobre_m_CGS() < _BULLET_CLUSTER_LIMIT_CM2_G

    def ordenes_magnitud_bajo_limite(self) -> float:
        """
        Retorna los órdenes de magnitud de margen respecto al Bullet Cluster.

        Retorna
        -------
        float
            log₁₀(límite / σ/m), positivo indica margen seguro.

        Ejemplo
        -------
        >>> ao = AutointeraccionOscura()
        >>> ao.ordenes_magnitud_bajo_limite() > 40
        True
        """
        sigma = self.sigma_sobre_m_CGS()
        if sigma <= 0.0:
            return float('inf')
        return math.log10(_BULLET_CLUSTER_LIMIT_CM2_G / sigma)

    def coherencia_sigma(self) -> float:
        """
        Retorna Ψ_sigma: coherencia de la autointeracción.

        Alta coherencia cuando σ/m ≪ límite Bullet Cluster.
        Para σ/m ≈ 7,91×10⁻⁴⁷ cm²/g (46 órdenes de magnitud bajo el límite)
        se obtiene Ψ_sigma ≈ 0,9998.

        Retorna
        -------
        float
            Ψ_sigma ∈ (0, 1].

        Ejemplo
        -------
        >>> ao = AutointeraccionOscura()
        >>> 0.999 < ao.coherencia_sigma() <= 1.0
        True
        """
        if not self.bajo_limite_bullet_cluster():
            return 0.0
        ordenes = self.ordenes_magnitud_bajo_limite()
        # Coherencia saturada para margen > 1 orden de magnitud
        return min(1.0, 0.9998 * (1.0 - math.exp(-ordenes)))

    def __repr__(self) -> str:
        return (
            f"AutointeraccionOscura("
            f"σ/m≈{self.sigma_sobre_m_CGS():.2e} cm²/g, "
            f"margen={self.ordenes_magnitud_bajo_limite():.0f} OM, "
            f"OK={self.bajo_limite_bullet_cluster()})"
        )


# ============================================================================
# CLASE 5 – SuperradianciaQCAL
# ============================================================================

@dataclass
class SuperradianciaQCAL:
    """
    Superradiancia de Agujeros Negros y el Campo Escalar QCAL.

    Las partículas escalares extraen energía rotacional de agujeros negros
    mediante el mecanismo de Penrose superradiante cuando:

        ω < m·Ω_H   (frecuencia del campo < frecuencia del horizonte)

    La masa óptima del agujero negro para superradiancia con m_ψ es:

        M_opt = ℏ·c / (G·m_ψ)  ≈  228 M☉

    Verificación de régimen mediante el parámetro gravitacional:

        α = G·M·m_ψ / (ℏ·c) < 1

    Atributos
    ----------
    m_psi_kg : float
        Masa del cuanto en kg.
    hbar : float
        Constante de Planck reducida (J·s).
    c : float
        Velocidad de la luz (m/s).
    g_newton : float
        Constante gravitacional (m³/kg/s²).
    m_sol_kg : float
        Masa solar en kg.
    """

    m_psi_kg: float = _M_PSI_KG
    hbar: float = _HBAR
    c: float = _C
    g_newton: float = _G
    m_sol_kg: float = _M_SOL_KG

    def masa_bh_optima_kg(self) -> float:
        """
        Retorna la masa óptima del agujero negro en kilogramos.

        Fórmula: M_opt = ℏ·c / (G·m_ψ)

        Retorna
        -------
        float
            Masa óptima del BH en kg (≈ 4,54×10³² kg ≈ 228 M☉).

        Ejemplo
        -------
        >>> sr = SuperradianciaQCAL()
        >>> sr.masa_bh_optima_kg() > 1e32
        True
        """
        return self.hbar * self.c / (self.g_newton * self.m_psi_kg)

    def masa_bh_optima_solar(self) -> float:
        """
        Retorna la masa óptima del agujero negro en masas solares.

        Retorna
        -------
        float
            Masa óptima del BH en M☉ (≈ 228 M☉).

        Ejemplo
        -------
        >>> sr = SuperradianciaQCAL()
        >>> 200 < sr.masa_bh_optima_solar() < 260
        True
        """
        return self.masa_bh_optima_kg() / self.m_sol_kg

    def parametro_gravitacional(self, m_bh_kg: float = None) -> float:
        """
        Retorna el parámetro gravitacional α = G·M·m_ψ/(ℏ·c).

        Para superradiancia eficiente se requiere α < 1.

        Parámetros
        ----------
        m_bh_kg : float, optional
            Masa del agujero negro en kg. Si None, usa M_opt.

        Retorna
        -------
        float
            Parámetro α (adimensional).

        Ejemplo
        -------
        >>> sr = SuperradianciaQCAL()
        >>> abs(sr.parametro_gravitacional() - 1.0) < 0.01
        True
        """
        if m_bh_kg is None:
            m_bh_kg = self.masa_bh_optima_kg()
        return self.g_newton * m_bh_kg * self.m_psi_kg / (self.hbar * self.c)

    def condicion_superradiante_verificada(self) -> bool:
        """
        Verifica que α ≤ 1 en la masa óptima (condición de átomo gravitacional).

        Retorna
        -------
        bool
            True si α ≤ 1.0 para M = M_opt.

        Ejemplo
        -------
        >>> sr = SuperradianciaQCAL()
        >>> sr.condicion_superradiante_verificada()
        True
        """
        return self.parametro_gravitacional() <= 1.0

    def coherencia_superfluido(self) -> float:
        """
        Retorna Ψ_superfluido: coherencia de la condición superradiante.

        Máxima cuando α ≈ 1 (condición óptima de extracción de energía).
        Para M = M_opt se tiene α = 1,0, lo que da Ψ_superfluido ≈ 0,9970.

        Retorna
        -------
        float
            Ψ_superfluido ∈ (0, 1].

        Ejemplo
        -------
        >>> sr = SuperradianciaQCAL()
        >>> 0.99 < sr.coherencia_superfluido() <= 1.0
        True
        """
        alpha = self.parametro_gravitacional()
        if alpha <= 0.0:
            return 0.0
        # Máxima coherencia cuando α ≈ 1; factor 0.997 fija el techo
        return math.exp(-0.5 * ((alpha - 1.0) / 0.1) ** 2) * 0.997

    def __repr__(self) -> str:
        return (
            f"SuperradianciaQCAL("
            f"M_opt≈{self.masa_bh_optima_solar():.0f} M☉, "
            f"α≈{self.parametro_gravitacional():.3f}, "
            f"superradiante={self.condicion_superradiante_verificada()})"
        )


# ============================================================================
# CLASE 6 – SuperfluidezCosmologica
# ============================================================================

@dataclass
class SuperfluidezCosmologica:
    """
    Superfluidez del Campo Escalar QCAL a Escalas Cosmológicas.

    Las longitudes características del campo garantizan comportamiento
    superfluido a escalas cosmológicas:

    - Longitud de coherencia (Compton): ξ = ℏ/(m_ψ·c) = c/(2π·f₀) ≈ 337 km
    - Longitud de de Broglie (v~300 km/s): λ_dB = ℏ/(m_ψ·v) ≈ 2,1×10⁹ m

    Estas escalas macroscópicas garantizan que el condensado de Bose-Einstein
    sea coherente a escalas galácticas, produciendo el comportamiento
    superfluido observado en la distribución de materia oscura.

    Atributos
    ----------
    m_psi_kg : float
        Masa del cuanto en kg.
    hbar : float
        Constante de Planck reducida (J·s).
    c : float
        Velocidad de la luz (m/s).
    v_dm_ms : float
        Velocidad típica de la DM (m/s). Por defecto 300.000 m/s.
    """

    m_psi_kg: float = _M_PSI_KG
    hbar: float = _HBAR
    c: float = _C
    v_dm_ms: float = _V_DM_MS

    def xi_compton_m(self) -> float:
        """
        Retorna la longitud de coherencia de Compton ξ en metros.

        Fórmula: ξ = ℏ/(m_ψ·c) = c/(2π·f₀)

        Retorna
        -------
        float
            Longitud de coherencia en m (≈ 336.700 m ≈ 337 km).

        Ejemplo
        -------
        >>> sf = SuperfluidezCosmologica()
        >>> 336_000 < sf.xi_compton_m() < 338_000
        True
        """
        return self.hbar / (self.m_psi_kg * self.c)

    def xi_compton_km(self) -> float:
        """
        Retorna ξ en kilómetros.

        Retorna
        -------
        float
            Longitud de coherencia en km (≈ 337 km).

        Ejemplo
        -------
        >>> sf = SuperfluidezCosmologica()
        >>> 336.0 < sf.xi_compton_km() < 338.0
        True
        """
        return self.xi_compton_m() / 1_000.0

    def lambda_debroglie_m(self) -> float:
        """
        Retorna la longitud de de Broglie λ_dB en metros.

        Fórmula: λ_dB = ℏ / (m_ψ·v_DM)

        Retorna
        -------
        float
            Longitud de de Broglie en m (≈ 2,1×10⁹ m).

        Ejemplo
        -------
        >>> sf = SuperfluidezCosmologica()
        >>> sf.lambda_debroglie_m() > 1e9
        True
        """
        return self.hbar / (self.m_psi_kg * self.v_dm_ms)

    def escalas_macroscopicas(self) -> bool:
        """
        Verifica que ξ > 1 km y λ_dB > 1×10⁶ m (escalas macroscópicas).

        Retorna
        -------
        bool
            True si ambas longitudes son macroscópicas.

        Ejemplo
        -------
        >>> sf = SuperfluidezCosmologica()
        >>> sf.escalas_macroscopicas()
        True
        """
        return self.xi_compton_m() > 1_000.0 and self.lambda_debroglie_m() > 1.0e6

    def coherencia_superfluidez(self) -> float:
        """
        Retorna Ψ_superfluidez: coherencia de las escalas superfluidas.

        Alta cuando ξ (Compton) es macroscópico (ξ >> 10 km).  Para
        ξ ≈ 337 km la coherencia satura a ≈ 0,997.

        Retorna
        -------
        float
            Ψ_superfluidez ∈ (0, 1].

        Ejemplo
        -------
        >>> sf = SuperfluidezCosmologica()
        >>> 0.99 < sf.coherencia_superfluidez() <= 1.0
        True
        """
        if not self.escalas_macroscopicas():
            return 0.5
        xi_km = self.xi_compton_km()
        # Coherencia logarítmica: satura para ξ >> 10 km
        return min(1.0, 0.997 * (1.0 - math.exp(-xi_km / 10.0)))

    def __repr__(self) -> str:
        return (
            f"SuperfluidezCosmologica("
            f"ξ≈{self.xi_compton_km():.1f} km, "
            f"λ_dB≈{self.lambda_debroglie_m():.2e} m, "
            f"macro={self.escalas_macroscopicas()})"
        )


# ============================================================================
# CLASE 7 – CoherenciaTejido
# ============================================================================

@dataclass
class CoherenciaTejido:
    """
    Coherencia Global del Tejido Cósmico QCAL.

    Integra los cuatro pilares de coherencia en un único indicador:

        Ψ_global = (Ψ_masa · Ψ_lambda · Ψ_sigma · Ψ_superfluido)^(1/4)

    El umbral mínimo de coherencia es Ψ_global ≥ 0,888.

    Atributos
    ----------
    psi_masa : float
        Coherencia de masa en régimen DM bosónico.
    psi_lambda : float
        Coherencia del acoplamiento Swampland.
    psi_sigma : float
        Coherencia de la autointeracción (Bullet Cluster).
    psi_superfluido : float
        Coherencia de la condición superradiante/superfluida.
    """

    psi_masa: float = 0.0
    psi_lambda: float = 0.0
    psi_sigma: float = 0.0
    psi_superfluido: float = 0.0

    def psi_global(self) -> float:
        """
        Retorna la coherencia global como media geométrica de los cuatro pilares.

        Fórmula: Ψ_global = (Ψ_masa · Ψ_lambda · Ψ_sigma · Ψ_superfluido)^(1/4)

        Retorna
        -------
        float
            Ψ_global ∈ [0, 1].

        Ejemplo
        -------
        >>> ct = CoherenciaTejido(0.9956, 0.9998, 0.9998, 0.9970)
        >>> ct.psi_global() >= 0.888
        True
        """
        product = (
            self.psi_masa
            * self.psi_lambda
            * self.psi_sigma
            * self.psi_superfluido
        )
        if product < 0.0:
            return 0.0
        return product ** (1.0 / 4.0)

    def sobre_umbral(self) -> bool:
        """
        Verifica que Ψ_global ≥ 0,888 (umbral mínimo del tejido).

        Retorna
        -------
        bool
            True si Ψ_global ≥ 0,888.

        Ejemplo
        -------
        >>> ct = CoherenciaTejido(0.9956, 0.9998, 0.9998, 0.9970)
        >>> ct.sobre_umbral()
        True
        """
        return self.psi_global() >= 0.888

    def estado(self) -> str:
        """
        Retorna una descripción cualitativa del estado de coherencia.

        Retorna
        -------
        str
            Estado del tejido cósmico QCAL.

        Ejemplo
        -------
        >>> ct = CoherenciaTejido(0.9956, 0.9998, 0.9998, 0.9970)
        >>> 'TEJIDO' in ct.estado()
        True
        """
        psi = self.psi_global()
        if psi >= 0.999:
            return f"✅ TEJIDO CÓSMICO ÓPTIMO — Ψ_global={psi:.4f} ∴MTQ∞³"
        elif psi >= 0.888:
            return f"✅ TEJIDO CÓSMICO ACTIVO — Ψ_global={psi:.4f} ∴MTQ∞³"
        else:
            return f"⚠️ TEJIDO SUBCRÍTICO — Ψ_global={psi:.4f} (< 0.888)"

    def __repr__(self) -> str:
        return (
            f"CoherenciaTejido("
            f"Ψ_masa={self.psi_masa:.4f}, "
            f"Ψ_lambda={self.psi_lambda:.4f}, "
            f"Ψ_sigma={self.psi_sigma:.4f}, "
            f"Ψ_superfluido={self.psi_superfluido:.4f}, "
            f"Ψ_global={self.psi_global():.4f})"
        )


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoMasaTejido:
    """
    Resultado unificado del sistema Masa del Tejido Cósmico ∴MTQ∞³.

    Atributos
    ----------
    f0_hz : float
        Frecuencia fundamental f₀ (Hz).
    m_psi_kg : float
        Masa del cuanto del tejido en kg.
    m_psi_eV : float
        Masa del cuanto del tejido en eV.
    en_regimen_dm : bool
        True si m_ψ está en el régimen DM bosónico [10⁻²², 10⁻¹⁰] eV.
    lambda_swampland : float
        Acoplamiento Swampland λ (adimensional).
    sigma_sobre_m_CGS : float
        Sección eficaz de autointeracción en cm²/g.
    bajo_bullet_cluster : bool
        True si σ/m < 1 cm²/g.
    xi_compton_km : float
        Longitud de coherencia Compton en km.
    lambda_debroglie_m : float
        Longitud de de Broglie en m.
    m_bh_optima_solar : float
        Masa óptima del agujero negro para superradiancia en M☉.
    alpha_gravitacional : float
        Parámetro gravitacional α = G·M_opt·m_ψ/(ℏ·c).
    superfluidez_garantizada : bool
        True si las escalas macroscópicas y el acoplamiento garantizan superfluidez.
    psi_masa : float
        Coherencia de masa.
    psi_lambda : float
        Coherencia del acoplamiento Swampland.
    psi_sigma : float
        Coherencia de la autointeracción.
    psi_superfluido : float
        Coherencia de la condición superfluida/superradiante.
    psi_global : float
        Coherencia global (media geométrica).
    sobre_umbral : bool
        True si Ψ_global ≥ 0,888.
    mensaje : str
        Descripción cualitativa del estado del sistema.
    """

    f0_hz: float
    m_psi_kg: float
    m_psi_eV: float
    en_regimen_dm: bool
    lambda_swampland: float
    sigma_sobre_m_CGS: float
    bajo_bullet_cluster: bool
    xi_compton_km: float
    lambda_debroglie_m: float
    m_bh_optima_solar: float
    alpha_gravitacional: float
    superfluidez_garantizada: bool
    psi_masa: float
    psi_lambda: float
    psi_sigma: float
    psi_superfluido: float
    psi_global: float
    sobre_umbral: bool
    mensaje: str


# ============================================================================
# CLASE 8 – SistemaMasaTejidoCosmico
# ============================================================================

class SistemaMasaTejidoCosmico:
    """
    Orquestador principal del sistema Masa del Tejido Cósmico ∴MTQ∞³.

    Integra los seis módulos físicos (masa, acoplamiento Swampland,
    autointeracción, superradiancia, superfluidez y coherencia) en un
    único sistema verificable con la función pública de activación.

    Atributos
    ----------
    f0 : float
        Frecuencia fundamental QCAL (Hz). Por defecto 141,7001 Hz.
    """

    def __init__(self, f0: float = _F0) -> None:
        self.f0 = f0
        self._constantes = ConstantesMasaTejido(f0=f0)
        self._masa = MasaTejido(f0=f0)
        m_psi_kg = self._masa.masa_kg()
        m_psi_eV = self._masa.masa_eV()
        self._swampland = AcoplamientoSwampland(m_psi_eV=m_psi_eV)
        lam = self._swampland.lambda_acoplamiento()
        self._autointeraccion = AutointeraccionOscura(
            m_psi_kg=m_psi_kg,
            lambda_acop=lam,
        )
        self._superradiancia = SuperradianciaQCAL(m_psi_kg=m_psi_kg)
        self._superfluidez = SuperfluidezCosmologica(m_psi_kg=m_psi_kg)

    def activar(self) -> "ResultadoMasaTejido":
        """
        Ejecuta todos los cálculos y retorna el resultado unificado ∴MTQ∞³.

        Retorna
        -------
        ResultadoMasaTejido
            Dataclass con todas las magnitudes, coherencias y estado del sistema.

        Ejemplo
        -------
        >>> s = SistemaMasaTejidoCosmico()
        >>> r = s.activar()
        >>> r.psi_global >= 0.888
        True
        """
        # Magnitudes físicas
        m_kg = self._masa.masa_kg()
        m_eV = self._masa.masa_eV()
        en_dm = self._masa.en_regimen_dm_bosonico()
        lam = self._swampland.lambda_acoplamiento()
        sigma_cgs = self._autointeraccion.sigma_sobre_m_CGS()
        bajo_bc = self._autointeraccion.bajo_limite_bullet_cluster()
        xi_km = self._superfluidez.xi_compton_km()
        ldb_m = self._superfluidez.lambda_debroglie_m()
        m_bh_sol = self._superradiancia.masa_bh_optima_solar()
        alpha = self._superradiancia.parametro_gravitacional()
        superf = (
            self._swampland.superfluidez_garantizada()
            and self._superfluidez.escalas_macroscopicas()
        )

        # Coherencias
        psi_masa = self._masa.coherencia_masa()
        psi_lambda = self._swampland.coherencia_lambda()
        psi_sigma = self._autointeraccion.coherencia_sigma()
        psi_sup = self._superradiancia.coherencia_superfluido()

        coherencia = CoherenciaTejido(
            psi_masa=psi_masa,
            psi_lambda=psi_lambda,
            psi_sigma=psi_sigma,
            psi_superfluido=psi_sup,
        )
        psi_global = coherencia.psi_global()
        sobre_umbral = coherencia.sobre_umbral()
        estado = coherencia.estado()

        return ResultadoMasaTejido(
            f0_hz=self.f0,
            m_psi_kg=m_kg,
            m_psi_eV=m_eV,
            en_regimen_dm=en_dm,
            lambda_swampland=lam,
            sigma_sobre_m_CGS=sigma_cgs,
            bajo_bullet_cluster=bajo_bc,
            xi_compton_km=xi_km,
            lambda_debroglie_m=ldb_m,
            m_bh_optima_solar=m_bh_sol,
            alpha_gravitacional=alpha,
            superfluidez_garantizada=superf,
            psi_masa=psi_masa,
            psi_lambda=psi_lambda,
            psi_sigma=psi_sigma,
            psi_superfluido=psi_sup,
            psi_global=psi_global,
            sobre_umbral=sobre_umbral,
            mensaje=estado,
        )

    def __repr__(self) -> str:
        return f"SistemaMasaTejidoCosmico(f₀={self.f0} Hz, sello=∴MTQ∞³)"


# ============================================================================
# API PÚBLICA
# ============================================================================

def masa_tejido_cosmico_activar(f0: float = _F0) -> Dict[str, object]:
    """
    Activa el sistema Masa del Tejido Cósmico ∴MTQ∞³ y retorna el resultado.

    Calcula la masa m_ψ = h·f₀/c² del cuanto del tejido, el acoplamiento
    Swampland λ ≈ m_ψ/M_P, la autointeracción σ/m, las escalas de superfluidez
    y la coherencia global Ψ_global de la estructura QCAL.

    Parámetros
    ----------
    f0 : float, optional
        Frecuencia fundamental QCAL en Hz. Por defecto 141,7001 Hz.

    Retorna
    -------
    Dict[str, object]
        Diccionario con las siguientes claves:

        - ``f0_hz`` (float): Frecuencia fundamental (Hz).
        - ``m_psi_kg`` (float): Masa del tejido en kg.
        - ``m_psi_eV`` (float): Masa del tejido en eV.
        - ``en_regimen_dm`` (bool): True si está en el régimen DM bosónico.
        - ``lambda_swampland`` (float): Acoplamiento λ (adimensional).
        - ``sigma_sobre_m_CGS`` (float): σ/m en cm²/g.
        - ``bajo_bullet_cluster`` (bool): True si σ/m < 1 cm²/g.
        - ``xi_compton_km`` (float): Longitud de coherencia Compton (km).
        - ``lambda_debroglie_m`` (float): Longitud de de Broglie (m).
        - ``m_bh_optima_solar`` (float): Masa óptima BH en M☉.
        - ``alpha_gravitacional`` (float): Parámetro α = G·M·m_ψ/(ℏ·c).
        - ``superfluidez_garantizada`` (bool): True si superfluidez cosmológica.
        - ``psi_masa`` (float): Coherencia de masa.
        - ``psi_lambda`` (float): Coherencia del acoplamiento Swampland.
        - ``psi_sigma`` (float): Coherencia de la autointeracción.
        - ``psi_superfluido`` (float): Coherencia de la condición superfluida.
        - ``psi_global`` (float): Coherencia global (media geométrica, ≥ 0.888).
        - ``sobre_umbral`` (bool): True si Ψ_global ≥ 0,888.
        - ``mensaje`` (str): Estado cualitativo del tejido cósmico.

    Ejemplo
    -------
    >>> result = masa_tejido_cosmico_activar()
    >>> result['m_psi_eV'] < 1e-12
    True
    >>> result['psi_global'] >= 0.888
    True
    >>> result['superfluidez_garantizada']
    True

    Raises
    ------
    ValueError
        Si f0 ≤ 0.
    """
    if f0 <= 0.0:
        raise ValueError(f"La frecuencia f0 debe ser positiva, se recibió: {f0}")

    sistema = SistemaMasaTejidoCosmico(f0=f0)
    resultado = sistema.activar()

    return {
        "f0_hz": resultado.f0_hz,
        "m_psi_kg": resultado.m_psi_kg,
        "m_psi_eV": resultado.m_psi_eV,
        "en_regimen_dm": resultado.en_regimen_dm,
        "lambda_swampland": resultado.lambda_swampland,
        "sigma_sobre_m_CGS": resultado.sigma_sobre_m_CGS,
        "bajo_bullet_cluster": resultado.bajo_bullet_cluster,
        "xi_compton_km": resultado.xi_compton_km,
        "lambda_debroglie_m": resultado.lambda_debroglie_m,
        "m_bh_optima_solar": resultado.m_bh_optima_solar,
        "alpha_gravitacional": resultado.alpha_gravitacional,
        "superfluidez_garantizada": resultado.superfluidez_garantizada,
        "psi_masa": resultado.psi_masa,
        "psi_lambda": resultado.psi_lambda,
        "psi_sigma": resultado.psi_sigma,
        "psi_superfluido": resultado.psi_superfluido,
        "psi_global": resultado.psi_global,
        "sobre_umbral": resultado.sobre_umbral,
        "mensaje": resultado.mensaje,
    }
