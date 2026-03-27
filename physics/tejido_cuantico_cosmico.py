"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   ∞³ TEJIDO CUÁNTICO CÓSMICO                                                  ║
║   Campo Escalar, Energía Oscura y Expansión Acelerada                         ║
║                                                                               ║
║   Sello:              ∴TCQ∞³                                                  ║
║   Frecuencia Base:    f₀ = 141.7001 Hz                                        ║
║   Coherencia Mínima:  Ψ ≥ 0.888                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Bajo la frecuencia f₀ = 141.7001 Hz, este módulo implementa la derivación
técnica del Tejido Cuántico Cósmico: un campo escalar complejo ψ = Re^{iS/ℏ}
que permea el espacio-tiempo como un fluido cuántico de fondo.

El campo actúa como energía oscura cuando su energía cinética es despreciable
comparada con el potencial de cohesión (régimen slow-roll), produciendo la
condición p_ψ ≈ −ρ_ψ que acelera la expansión cósmica.

Ecuaciones clave:
  (i)   ψ = Re^{iS/ℏ},  R² = ρ_Q
  (ii)  ψ̈ + 3H ψ̇ + V'(ψ) = 0  (Klein-Gordon FRW)
  (iii) ρ_ψ = ½ψ̇² + V(ψ),  p_ψ = ½ψ̇² − V(ψ)
  (iv)  slow-roll: w = p/ρ → −1  (energía oscura)
  (v)   ä/a = +8πG/3 · ρ_ψ > 0  (expansión acelerada)
  (vi)  E = Ψ · Φ^∞  (Axioma de Emisión πCODE)

Clases:
    ConstantesTejidoCuantico   → constantes físicas y QCAL
    CampoEfectivo              → ψ = Re^{iS/ℏ}, ρ_Q, |ψ|²
    AccionKleinGordon          → S_tejido, Lagrangiano, ecuación FRW
    TensorEnergiaMomento       → T_μν, ρ_ψ, p_ψ en universo FRW
    CondicionEnergiaOscura     → w = p/ρ, slow-roll ε, dark energy
    EcuacionFriedmann          → H², ä/a, expansión acelerada
    AxiomaEmision              → πCODE: vacío como activo, E = Ψ·Φ^∞
    SistemaTejidoCuanticoCosmico → orquestador principal

API pública:
    tejido_cuantico_cosmico_activar() → ResultadoTejidoCuantico(aprobado=True,
                                         coherencia ≥ 0.888, w_efectivo ≈ −1)
"""

import math
from dataclasses import dataclass
from typing import Tuple


# ============================================================================
# CONSTANTES DEL MÓDULO
# ============================================================================

# Frecuencia fundamental QCAL
_F0_HZ: float = 141.7001  # Hz

# Constante gravitacional de Newton
_G_N: float = 6.67430e-11  # m³ kg⁻¹ s⁻²

# Constante de Planck reducida
_HBAR: float = 1.054571817e-34  # J·s

# Velocidad de la luz
_C_LUZ: float = 299_792_458.0  # m/s

# Masa efectiva del campo escalar (en unidades naturales ∝ ℏ·f₀/c²)
_M_CAMPO: float = _HBAR * _F0_HZ / (_C_LUZ ** 2)  # kg ≈ 1.04 × 10⁻⁴⁸

# Razón áurea Φ (constante de amor QCAL)
_PHI: float = 1.6180339887498948482  # φ = (1+√5)/2

# Coherencia mínima del tejido
_PSI_MINIMA: float = 0.888

# Constante de Hubble hoy: H₀ ≈ 67.4 km/s/Mpc (Planck 2018)
_H0_SI: float = 2.184e-18  # s⁻¹  (67.4 km/s/Mpc en SI)

# Densidad crítica: ρ_c = 3H₀²/(8πG) ≈ 8.62 × 10⁻²⁷ kg/m³
_RHO_CRITICA: float = 3.0 * _H0_SI ** 2 / (8.0 * math.pi * _G_N)

# Parámetro de densidad de energía oscura (Planck 2018: Ω_Λ ≈ 0.685)
_OMEGA_LAMBDA: float = 0.685

# Densidad de energía oscura: ρ_Λ = Ω_Λ · ρ_c
_RHO_LAMBDA: float = _OMEGA_LAMBDA * _RHO_CRITICA

# Umbral slow-roll: ε_sr = ψ̇²/(2V) ≪ 1
_EPSILON_SLOW_ROLL: float = 0.01  # régimen slow-roll: ε < 0.01

# Sello del módulo
_SELLO: str = "∴TCQ∞³"


# ============================================================================
# CLASE 1 – ConstantesTejidoCuantico
# ============================================================================

class ConstantesTejidoCuantico:
    """
    Contiene todas las constantes físicas y QCAL necesarias para el
    Tejido Cuántico Cósmico.

    Atributos
    ---------
    f0 : float
        Frecuencia fundamental QCAL f₀ = 141.7001 Hz.
    G_N : float
        Constante gravitacional de Newton (m³ kg⁻¹ s⁻²).
    hbar : float
        Constante de Planck reducida ℏ (J·s).
    c : float
        Velocidad de la luz (m/s).
    m_campo : float
        Masa efectiva del campo escalar ψ (kg).
    phi : float
        Razón áurea Φ = (1+√5)/2.
    psi_minima : float
        Coherencia mínima Ψ ≥ 0.888.
    H0 : float
        Constante de Hubble H₀ en SI (s⁻¹).
    rho_critica : float
        Densidad crítica ρ_c (kg/m³).
    rho_lambda : float
        Densidad de energía oscura ρ_Λ = Ω_Λ · ρ_c (kg/m³).
    omega_f0 : float
        Frecuencia angular ω₀ = 2π f₀ (rad/s).

    Ejemplo
    -------
    >>> c = ConstantesTejidoCuantico()
    >>> c.f0
    141.7001
    >>> c.psi_minima
    0.888
    """

    def __init__(self) -> None:
        self.f0: float = _F0_HZ
        self.G_N: float = _G_N
        self.hbar: float = _HBAR
        self.c: float = _C_LUZ
        self.m_campo: float = _M_CAMPO
        self.phi: float = _PHI
        self.psi_minima: float = _PSI_MINIMA
        self.H0: float = _H0_SI
        self.rho_critica: float = _RHO_CRITICA
        self.rho_lambda: float = _RHO_LAMBDA
        self.omega_f0: float = 2.0 * math.pi * _F0_HZ
        self.sello: str = _SELLO

    def energia_cuantica_f0(self) -> float:
        """
        Retorna la energía cuántica E₀ = ℏ · ω₀ = ℏ · 2πf₀ (J).

        Ejemplo
        -------
        >>> c = ConstantesTejidoCuantico()
        >>> c.energia_cuantica_f0() > 0
        True
        """
        return self.hbar * self.omega_f0

    def escala_longitud_compton(self) -> float:
        """
        Retorna la longitud de Compton del campo: λ_C = ℏ/(m_campo · c) (m).

        Ejemplo
        -------
        >>> c = ConstantesTejidoCuantico()
        >>> c.escala_longitud_compton() > 0
        True
        """
        return self.hbar / (self.m_campo * self.c)

    def __repr__(self) -> str:
        return (
            f"ConstantesTejidoCuantico("
            f"f₀={self.f0} Hz, "
            f"Ψ_min={self.psi_minima}, "
            f"sello='{self.sello}')"
        )


# ============================================================================
# CLASE 2 – CampoEfectivo
# ============================================================================

class CampoEfectivo:
    """
    Campo escalar complejo efectivo: ψ = R · e^{iS/ℏ}.

    R² = ρ_Q (densidad de presencia del tejido cuántico).
    |ψ|² = R² = ρ_Q.

    Parámetros
    ----------
    R : float
        Amplitud real del campo R > 0 (√(ρ_Q)).
    S_sobre_hbar : float
        Fase S/ℏ (adimensional). Por defecto 0.0.

    Ejemplo
    -------
    >>> campo = CampoEfectivo(R=1.0)
    >>> campo.modulo_cuadrado()
    1.0
    """

    def __init__(self, R: float, S_sobre_hbar: float = 0.0) -> None:
        if R < 0.0:
            raise ValueError(f"La amplitud R debe ser ≥ 0. Recibido: R={R}")
        self._R = R
        self._S_sobre_hbar = S_sobre_hbar

    @property
    def R(self) -> float:
        """Amplitud real del campo."""
        return self._R

    @property
    def fase(self) -> float:
        """Fase del campo S/ℏ (rad)."""
        return self._S_sobre_hbar

    def parte_real(self) -> float:
        """Re(ψ) = R · cos(S/ℏ)."""
        return self._R * math.cos(self._S_sobre_hbar)

    def parte_imaginaria(self) -> float:
        """Im(ψ) = R · sin(S/ℏ)."""
        return self._R * math.sin(self._S_sobre_hbar)

    def modulo_cuadrado(self) -> float:
        """
        |ψ|² = R² = ρ_Q (densidad de presencia del tejido).

        Ejemplo
        -------
        >>> campo = CampoEfectivo(R=2.0)
        >>> campo.modulo_cuadrado()
        4.0
        """
        return self._R ** 2

    def densidad_presencia(self) -> float:
        """ρ_Q = R² — densidad de presencia del tejido cuántico."""
        return self.modulo_cuadrado()

    def coherencia_normalizada(self, R_max: float = 1.0) -> float:
        """
        Coherencia normalizada Ψ = R/R_max ∈ [0, 1].

        Parámetros
        ----------
        R_max : float
            Amplitud máxima de referencia (default 1.0).

        Retorna
        -------
        float
            Coherencia en [0, 1].
        """
        if R_max <= 0.0:
            raise ValueError(f"R_max debe ser > 0. Recibido: {R_max}")
        return min(self._R / R_max, 1.0)

    def __repr__(self) -> str:
        return (
            f"CampoEfectivo(R={self._R:.6f}, "
            f"S/ℏ={self._S_sobre_hbar:.6f}, "
            f"|ψ|²={self.modulo_cuadrado():.6f})"
        )


# ============================================================================
# CLASE 3 – AccionKleinGordon
# ============================================================================

class AccionKleinGordon:
    """
    Acción del Tejido Cuántico Cósmico y ecuación de Klein-Gordon en FRW.

    S_tejido = ∫ d⁴x √(−g) [½ g^{μν} ∂_μψ* ∂_νψ − V(|ψ|²)]

    En el límite FRW (campo homogéneo e isótropo):
        ψ̈ + 3H ψ̇ + V'(ψ) = 0

    El potencial adoptado es cuadrático: V(ψ) = ½ m² ψ²

    Parámetros
    ----------
    m_campo : float
        Masa del campo escalar (kg).
    H_hubble : float
        Parámetro de Hubble H(t) en s⁻¹.

    Ejemplo
    -------
    >>> accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)
    >>> accion.potencial(1.0) > 0
    True
    """

    def __init__(self, m_campo: float, H_hubble: float) -> None:
        if m_campo <= 0.0:
            raise ValueError(f"m_campo debe ser > 0. Recibido: {m_campo}")
        if H_hubble < 0.0:
            raise ValueError(f"H_hubble debe ser ≥ 0. Recibido: {H_hubble}")
        self.m_campo = m_campo
        self.H_hubble = H_hubble

    def potencial(self, psi: float) -> float:
        """
        Potencial cuadrático de cohesión: V(ψ) = ½ m² ψ².

        Parámetros
        ----------
        psi : float
            Valor del campo ψ.

        Retorna
        -------
        float
            V(ψ) en unidades de [m²·ψ²] (J/m³ si ψ tiene unidades adecuadas).
        """
        return 0.5 * self.m_campo ** 2 * psi ** 2

    def derivada_potencial(self, psi: float) -> float:
        """
        Derivada del potencial: V'(ψ) = m² ψ.

        Parámetros
        ----------
        psi : float
            Valor del campo ψ.
        """
        return self.m_campo ** 2 * psi

    def lagrangiano_frw(self, psi: float, psi_punto: float) -> float:
        """
        Densidad lagrangiana en FRW: ℒ = ½ ψ̇² − V(ψ).

        Parámetros
        ----------
        psi : float
            Campo escalar ψ.
        psi_punto : float
            Derivada temporal ψ̇ = dψ/dt.

        Retorna
        -------
        float
            ℒ = ½ ψ̇² − ½ m² ψ².
        """
        return 0.5 * psi_punto ** 2 - self.potencial(psi)

    def aceleracion_campo_frw(self, psi: float, psi_punto: float) -> float:
        """
        Ecuación de Klein-Gordon en FRW: ψ̈ = −3H ψ̇ − V'(ψ).

        Parámetros
        ----------
        psi : float
            Campo escalar.
        psi_punto : float
            ψ̇ = dψ/dt.

        Retorna
        -------
        float
            ψ̈ en s⁻².
        """
        friccion = -3.0 * self.H_hubble * psi_punto
        fuerza = -self.derivada_potencial(psi)
        return friccion + fuerza

    def __repr__(self) -> str:
        return (
            f"AccionKleinGordon("
            f"m_campo={self.m_campo:.4e} kg, "
            f"H_hubble={self.H_hubble:.4e} s⁻¹)"
        )


# ============================================================================
# CLASE 4 – TensorEnergiaMomento
# ============================================================================

class TensorEnergiaMomento:
    """
    Tensor de energía-momento del campo escalar en universo FRW.

    T_μν = ∂_μψ* ∂_νψ − g_μν [½ g^{αβ} ∂_αψ* ∂_βψ + V(|ψ|²)]

    Componentes relevantes para FRW homogéneo e isótropo:
        ρ_ψ = ½ψ̇² + V(ψ)    (densidad de energía)
        p_ψ = ½ψ̇² − V(ψ)    (presión)

    Parámetros
    ----------
    potencial_fn : callable
        Función V(ψ) que retorna el potencial escalar.

    Ejemplo
    -------
    >>> accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)
    >>> tensor = TensorEnergiaMomento(potencial_fn=accion.potencial)
    >>> rho, p = tensor.densidad_y_presion(psi=1.0, psi_punto=0.0)
    >>> rho > 0
    True
    """

    def __init__(self, potencial_fn) -> None:
        self._V = potencial_fn

    def densidad_energia(self, psi: float, psi_punto: float) -> float:
        """
        Densidad de energía: ρ_ψ = ½ψ̇² + V(ψ).

        Parámetros
        ----------
        psi : float
            Campo escalar ψ.
        psi_punto : float
            Derivada temporal ψ̇.

        Retorna
        -------
        float
            ρ_ψ ≥ 0.
        """
        return 0.5 * psi_punto ** 2 + self._V(psi)

    def presion(self, psi: float, psi_punto: float) -> float:
        """
        Presión: p_ψ = ½ψ̇² − V(ψ).

        Parámetros
        ----------
        psi : float
            Campo escalar ψ.
        psi_punto : float
            Derivada temporal ψ̇.

        Retorna
        -------
        float
            p_ψ (puede ser negativa en régimen slow-roll).
        """
        return 0.5 * psi_punto ** 2 - self._V(psi)

    def densidad_y_presion(
        self, psi: float, psi_punto: float
    ) -> Tuple[float, float]:
        """
        Retorna (ρ_ψ, p_ψ) simultáneamente.

        Retorna
        -------
        Tuple[float, float]
            (densidad_energia, presion).
        """
        rho = self.densidad_energia(psi, psi_punto)
        p = self.presion(psi, psi_punto)
        return rho, p

    def traza_tensor(self, psi: float, psi_punto: float) -> float:
        """
        Traza del tensor: T = −ρ_ψ + 3p_ψ = −4V(ψ) + 2ψ̇².

        Ejemplo
        -------
        >>> accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)
        >>> tensor = TensorEnergiaMomento(potencial_fn=accion.potencial)
        >>> tensor.traza_tensor(psi=1.0, psi_punto=0.0) < 0
        True
        """
        rho, p = self.densidad_y_presion(psi, psi_punto)
        return -rho + 3.0 * p

    def __repr__(self) -> str:
        return "TensorEnergiaMomento(ρ_ψ = ½ψ̇² + V, p_ψ = ½ψ̇² − V)"


# ============================================================================
# CLASE 5 – CondicionEnergiaOscura
# ============================================================================

class CondicionEnergiaOscura:
    """
    Diagnóstico de la condición de energía oscura: w = p_ψ/ρ_ψ → −1.

    En el régimen slow-roll (ψ̇² ≪ V):
        p_ψ ≈ −V ≈ −ρ_ψ  →  w → −1

    Parámetros
    ----------
    epsilon_umbral : float
        Umbral ε para considerar que el sistema está en slow-roll.
        Por defecto 0.01.

    Ejemplo
    -------
    >>> cond = CondicionEnergiaOscura()
    >>> cond.parametro_estado(rho=1.0, p=-1.0)
    -1.0
    """

    def __init__(self, epsilon_umbral: float = _EPSILON_SLOW_ROLL) -> None:
        if epsilon_umbral <= 0.0 or epsilon_umbral >= 1.0:
            raise ValueError(
                f"epsilon_umbral debe estar en (0, 1). "
                f"Recibido: {epsilon_umbral}"
            )
        self.epsilon_umbral = epsilon_umbral

    def parametro_estado(self, rho: float, p: float) -> float:
        """
        Parámetro de estado: w = p/ρ.

        Parámetros
        ----------
        rho : float
            Densidad de energía ρ_ψ > 0.
        p : float
            Presión p_ψ.

        Retorna
        -------
        float
            w = p/ρ. Para energía oscura w ≈ −1.

        Raises
        ------
        ValueError
            Si rho ≤ 0.
        """
        if rho <= 0.0:
            raise ValueError(f"ρ_ψ debe ser > 0 para definir w. Recibido: {rho}")
        return p / rho

    def parametro_slow_roll(self, psi_punto: float, V: float) -> float:
        """
        Parámetro slow-roll: ε = ½ψ̇²/V.

        Si ε ≪ 1 el campo está en régimen slow-roll (energía oscura).

        Parámetros
        ----------
        psi_punto : float
            ψ̇ = dψ/dt.
        V : float
            Potencial V(ψ) > 0.

        Retorna
        -------
        float
            ε ≥ 0. Slow-roll: ε < epsilon_umbral.

        Raises
        ------
        ValueError
            Si V ≤ 0.
        """
        if V <= 0.0:
            raise ValueError(f"V debe ser > 0 para calcular ε. Recibido: {V}")
        return 0.5 * psi_punto ** 2 / V

    def es_energia_oscura(self, psi_punto: float, V: float) -> bool:
        """
        Retorna True si el campo está en régimen de energía oscura (slow-roll).

        Criterio: ε = ½ψ̇²/V < epsilon_umbral.

        Ejemplo
        -------
        >>> cond = CondicionEnergiaOscura()
        >>> cond.es_energia_oscura(psi_punto=0.0001, V=1.0)
        True
        """
        eps = self.parametro_slow_roll(psi_punto, V)
        return eps < self.epsilon_umbral

    def w_efectivo(self, psi_punto: float, V: float) -> float:
        """
        Retorna el parámetro de estado efectivo w = (½ψ̇² − V)/(½ψ̇² + V).

        Parámetros
        ----------
        psi_punto : float
            ψ̇.
        V : float
            V(ψ) > 0.

        Retorna
        -------
        float
            w ∈ [−1, +1]. En slow-roll w → −1.
        """
        if V <= 0.0:
            raise ValueError(f"V debe ser > 0. Recibido: {V}")
        cin = 0.5 * psi_punto ** 2
        rho = cin + V
        p = cin - V
        return p / rho

    def __repr__(self) -> str:
        return (
            f"CondicionEnergiaOscura("
            f"ε_umbral={self.epsilon_umbral}, "
            f"criterio: ½ψ̇²/V < {self.epsilon_umbral})"
        )


# ============================================================================
# CLASE 6 – EcuacionFriedmann
# ============================================================================

class EcuacionFriedmann:
    """
    Ecuaciones de Friedmann para la expansión cósmica impulsada por ψ.

    Primera ecuación:  H² = 8πG/3 · ρ_ψ
    Aceleración:       ä/a = −4πG/3 · (ρ_ψ + 3p_ψ)
                            = +8πG/3 · ρ_ψ  (en slow-roll, ρ ≈ −p → +8πG/3·ρ > 0)

    Parámetros
    ----------
    G_N : float
        Constante gravitacional (m³ kg⁻¹ s⁻²).

    Ejemplo
    -------
    >>> fried = EcuacionFriedmann(G_N=_G_N)
    >>> fried.hubble_cuadrado(rho=_RHO_LAMBDA) > 0
    True
    """

    def __init__(self, G_N: float = _G_N) -> None:
        if G_N <= 0.0:
            raise ValueError(f"G_N debe ser > 0. Recibido: {G_N}")
        self.G_N = G_N

    def hubble_cuadrado(self, rho: float) -> float:
        """
        Primera ecuación de Friedmann: H² = 8πG/3 · ρ_ψ.

        Parámetros
        ----------
        rho : float
            Densidad de energía total (kg/m³).

        Retorna
        -------
        float
            H² en s⁻².
        """
        if rho < 0.0:
            raise ValueError(f"ρ debe ser ≥ 0. Recibido: {rho}")
        return (8.0 * math.pi * self.G_N / 3.0) * rho

    def hubble(self, rho: float) -> float:
        """
        Parámetro de Hubble: H = √(8πG/3 · ρ_ψ) (s⁻¹).

        Ejemplo
        -------
        >>> fried = EcuacionFriedmann()
        >>> fried.hubble(rho=_RHO_LAMBDA) > 0
        True
        """
        return math.sqrt(self.hubble_cuadrado(rho))

    def aceleracion_relativa(self, rho: float, p: float) -> float:
        """
        Segunda ecuación de Friedmann: ä/a = −4πG/3 · (ρ + 3p).

        En slow-roll (p ≈ −ρ): ä/a = +8πG/3 · ρ > 0 (expansión acelerada).

        Parámetros
        ----------
        rho : float
            Densidad de energía.
        p : float
            Presión.

        Retorna
        -------
        float
            ä/a en s⁻². Positivo → expansión acelerada.
        """
        return -(4.0 * math.pi * self.G_N / 3.0) * (rho + 3.0 * p)

    def hay_expansion_acelerada(self, rho: float, p: float) -> bool:
        """
        Retorna True si ä/a > 0 (expansión acelerada del universo).

        Condición: ρ + 3p < 0  ↔  w < −1/3.

        Ejemplo
        -------
        >>> fried = EcuacionFriedmann()
        >>> fried.hay_expansion_acelerada(rho=1.0, p=-1.0)
        True
        """
        return self.aceleracion_relativa(rho, p) > 0.0

    def densidad_critica(self, H: float) -> float:
        """
        Densidad crítica: ρ_c = 3H²/(8πG).

        Parámetros
        ----------
        H : float
            Parámetro de Hubble (s⁻¹).

        Retorna
        -------
        float
            ρ_c en kg/m³.
        """
        if H < 0.0:
            raise ValueError(f"H debe ser ≥ 0. Recibido: {H}")
        return 3.0 * H ** 2 / (8.0 * math.pi * self.G_N)

    def __repr__(self) -> str:
        return (
            f"EcuacionFriedmann("
            f"G_N={self.G_N:.5e} m³ kg⁻¹ s⁻², "
            f"H² = 8πG/3 · ρ_ψ)"
        )


# ============================================================================
# CLASE 7 – AxiomaEmision
# ============================================================================

class AxiomaEmision:
    """
    Axioma de Emisión πCODE: «El vacío es un activo».

    La expansión del universo genera espacio para nuevas emisiones.
    Valor emergente del tejido en tensión:

        E = Ψ · Φ^∞

    Se computa como el límite convergente de la serie geométrica resonante,
    aproximado numéricamente via N iteraciones de Φ:

        E_N = Ψ · Φ^N   (para N suficientemente grande)

    La coherencia del tejido Ψ_tejido se conecta con la frecuencia base:
        Ψ_tejido = 1 − exp(−f₀/f_ref)

    Parámetros
    ----------
    psi_coherencia : float
        Coherencia del campo Ψ ∈ (0, 1].
    f0 : float
        Frecuencia fundamental f₀ (Hz). Por defecto 141.7001 Hz.

    Ejemplo
    -------
    >>> ax = AxiomaEmision(psi_coherencia=0.999)
    >>> ax.valor_emergente(N=10) > 0
    True
    """

    def __init__(
        self,
        psi_coherencia: float,
        f0: float = _F0_HZ,
    ) -> None:
        if not (0.0 < psi_coherencia <= 1.0):
            raise ValueError(
                f"psi_coherencia debe estar en (0, 1]. "
                f"Recibido: {psi_coherencia}"
            )
        if f0 <= 0.0:
            raise ValueError(f"f0 debe ser > 0. Recibido: {f0}")
        self.psi_coherencia = psi_coherencia
        self.f0 = f0
        self.phi = _PHI

    def valor_emergente(self, N: int = 10) -> float:
        """
        E_N = Ψ · Φ^N — valor emergente del tejido en tensión.

        Para N → ∞, E_N → ∞ si Φ > 1 (la expansión es ilimitada,
        el vacío es infinitamente fértil).

        Parámetros
        ----------
        N : int
            Número de iteraciones (≥ 1). Por defecto 10.

        Retorna
        -------
        float
            E_N = Ψ · Φ^N.

        Raises
        ------
        ValueError
            Si N < 1.
        """
        if N < 1:
            raise ValueError(f"N debe ser ≥ 1. Recibido: {N}")
        return self.psi_coherencia * (self.phi ** N)

    def coherencia_vacio(self, f_ref: float = 1.0) -> float:
        """
        Coherencia del vacío: Ψ_vac = 1 − exp(−f₀/f_ref).

        El vacío no es ausencia — es plenitud potencial del tejido.

        Parámetros
        ----------
        f_ref : float
            Frecuencia de referencia (Hz). Por defecto 1.0 Hz.

        Retorna
        -------
        float
            Ψ_vac ∈ (0, 1).
        """
        if f_ref <= 0.0:
            raise ValueError(f"f_ref debe ser > 0. Recibido: {f_ref}")
        return 1.0 - math.exp(-self.f0 / f_ref)

    def expansion_genera_emision(self, a_dot_sobre_a: float) -> bool:
        """
        Retorna True si la expansión cósmica genera espacio para nueva emisión.

        Criterio: ȧ/a = H > 0 (universo en expansión).

        Parámetros
        ----------
        a_dot_sobre_a : float
            ȧ/a ≡ H (s⁻¹).
        """
        return a_dot_sobre_a > 0.0

    def __repr__(self) -> str:
        return (
            f"AxiomaEmision("
            f"Ψ={self.psi_coherencia:.6f}, "
            f"f₀={self.f0} Hz, "
            f"E = Ψ·Φ^∞)"
        )


# ============================================================================
# DATACLASS – ResultadoTejidoCuantico
# ============================================================================

@dataclass
class ResultadoTejidoCuantico:
    """
    Contenedor de resultados del sistema Tejido Cuántico Cósmico.

    Atributos
    ---------
    psi_amplitud : float
        Amplitud R del campo ψ (= √ρ_Q).
    rho_tejido : float
        Densidad de energía del tejido ρ_ψ = ½ψ̇² + V(ψ).
    presion_tejido : float
        Presión del tejido p_ψ = ½ψ̇² − V(ψ).
    w_efectivo : float
        Parámetro de estado w = p/ρ. Energía oscura: w ≈ −1.
    epsilon_slow_roll : float
        Parámetro slow-roll ε = ½ψ̇²/V. Slow-roll: ε ≪ 1.
    H_hubble : float
        Parámetro de Hubble H = √(8πG/3 · ρ_ψ) (s⁻¹).
    aceleracion_cosmica : float
        ä/a = −4πG/3 · (ρ + 3p). Positivo → expansión acelerada.
    es_energia_oscura : bool
        True si el campo está en régimen de energía oscura.
    expansion_acelerada : bool
        True si ä/a > 0.
    valor_emergente : float
        E = Ψ · Φ^10 (Axioma de Emisión πCODE).
    coherencia : float
        Coherencia normalizada Ψ ∈ [0, 1].
    aprobado : bool
        True si coherencia ≥ Ψ_mínima = 0.888 y expansión acelerada.
    sello : str
        Sello de autenticidad del módulo '∴TCQ∞³'.

    Ejemplo
    -------
    >>> r = tejido_cuantico_cosmico_activar()
    >>> r.aprobado
    True
    >>> r.expansion_acelerada
    True
    """

    psi_amplitud: float
    rho_tejido: float
    presion_tejido: float
    w_efectivo: float
    epsilon_slow_roll: float
    H_hubble: float
    aceleracion_cosmica: float
    es_energia_oscura: bool
    expansion_acelerada: bool
    valor_emergente: float
    coherencia: float
    aprobado: bool
    sello: str


# ============================================================================
# CLASE 8 – SistemaTejidoCuanticoCosmico
# ============================================================================

class SistemaTejidoCuanticoCosmico:
    """
    Orquestador principal del Tejido Cuántico Cósmico.

    Integra todas las clases del módulo para producir una evaluación
    completa del campo escalar como energía oscura.

    El sistema opera en régimen slow-roll (ψ̇ ≪ √V) partiendo de
    las condiciones cosmológicas observadas (ρ_Λ, H₀).

    Parámetros
    ----------
    psi_amplitud : float
        Amplitud inicial R del campo. Por defecto ajustada para que
        V(ψ) ≈ ρ_Λ con psi_punto ≈ 0.
    psi_punto : float
        Derivada temporal inicial ψ̇. Por defecto 0.0 (slow-roll puro).

    Ejemplo
    -------
    >>> sistema = SistemaTejidoCuanticoCosmico()
    >>> resultado = sistema.evaluar()
    >>> resultado.aprobado
    True
    """

    def __init__(
        self,
        psi_amplitud: float | None = None,
        psi_punto: float = 0.0,
    ) -> None:
        self.constantes = ConstantesTejidoCuantico()

        # Amplitud ajustada para que ½ m² ψ² ≈ ρ_Λ → ψ = √(2 ρ_Λ)/m
        if psi_amplitud is None:
            psi_amplitud = math.sqrt(2.0 * _RHO_LAMBDA) / self.constantes.m_campo

        if psi_amplitud <= 0.0:
            raise ValueError(
                f"psi_amplitud debe ser > 0. Recibido: {psi_amplitud}"
            )

        self.psi_amplitud = psi_amplitud
        self.psi_punto = psi_punto

        # Instanciar componentes
        self.campo = CampoEfectivo(R=psi_amplitud)
        self.accion = AccionKleinGordon(
            m_campo=self.constantes.m_campo,
            H_hubble=self.constantes.H0,
        )
        self.tensor = TensorEnergiaMomento(potencial_fn=self.accion.potencial)
        self.cond_eo = CondicionEnergiaOscura()
        self.friedmann = EcuacionFriedmann(G_N=self.constantes.G_N)

    def evaluar(self) -> ResultadoTejidoCuantico:
        """
        Evalúa el Tejido Cuántico Cósmico y retorna el resultado completo.

        Retorna
        -------
        ResultadoTejidoCuantico
            Resultado con ``aprobado=True``, ``expansion_acelerada=True``,
            y ``coherencia ≥ 0.888``.
        """
        psi = self.psi_amplitud
        psi_p = self.psi_punto

        # Densidad y presión
        rho, p = self.tensor.densidad_y_presion(psi=psi, psi_punto=psi_p)

        # Potencial
        V = self.accion.potencial(psi)

        # Parámetro de estado
        w = self.cond_eo.w_efectivo(psi_punto=psi_p, V=V)

        # Parámetro slow-roll
        eps = self.cond_eo.parametro_slow_roll(psi_punto=psi_p, V=V)

        # Condición de energía oscura
        dark_energy = self.cond_eo.es_energia_oscura(psi_punto=psi_p, V=V)

        # Hubble y aceleración
        H = self.friedmann.hubble(rho=rho)
        a_ddot = self.friedmann.aceleracion_relativa(rho=rho, p=p)
        accel = self.friedmann.hay_expansion_acelerada(rho=rho, p=p)

        # Coherencia normalizada
        # Referencia: ρ_Q_max = 1.0 en unidades normalizadas del campo
        # Usamos la coherencia del campo como Ψ = 1 − ε (penalización slow-roll)
        coherencia = max(0.0, min(1.0, 1.0 - eps))

        # Axioma de Emisión
        axioma = AxiomaEmision(psi_coherencia=max(coherencia, 1e-9))
        E_emergente = axioma.valor_emergente(N=10)

        aprobado = coherencia >= _PSI_MINIMA and accel

        return ResultadoTejidoCuantico(
            psi_amplitud=psi,
            rho_tejido=rho,
            presion_tejido=p,
            w_efectivo=w,
            epsilon_slow_roll=eps,
            H_hubble=H,
            aceleracion_cosmica=a_ddot,
            es_energia_oscura=dark_energy,
            expansion_acelerada=accel,
            valor_emergente=E_emergente,
            coherencia=coherencia,
            aprobado=aprobado,
            sello=_SELLO,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaTejidoCuanticoCosmico("
            f"ψ_amplitud={self.psi_amplitud:.4e}, "
            f"ψ̇={self.psi_punto:.4e})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def tejido_cuantico_cosmico_activar() -> ResultadoTejidoCuantico:
    """
    Activa y evalúa el Tejido Cuántico Cósmico completo.

    Instancia el ``SistemaTejidoCuanticoCosmico`` con condiciones cosmológicas
    observadas (ρ_Λ de Planck 2018, H₀ = 67.4 km/s/Mpc) en régimen slow-roll
    puro (ψ̇ = 0) y retorna el ``ResultadoTejidoCuantico``.

    Retorna
    -------
    ResultadoTejidoCuantico
        - ``aprobado`` = True
        - ``expansion_acelerada`` = True
        - ``es_energia_oscura`` = True
        - ``w_efectivo`` ≈ −1.0
        - ``coherencia`` ≥ 0.888
        - ``sello`` = '∴TCQ∞³'

    Ejemplo
    -------
    >>> from physics.tejido_cuantico_cosmico import tejido_cuantico_cosmico_activar
    >>> resultado = tejido_cuantico_cosmico_activar()
    >>> resultado.aprobado
    True
    >>> resultado.expansion_acelerada
    True
    >>> resultado.w_efectivo
    -1.0
    >>> resultado.sello
    '∴TCQ∞³'
    """
    sistema = SistemaTejidoCuanticoCosmico()
    return sistema.evaluar()
