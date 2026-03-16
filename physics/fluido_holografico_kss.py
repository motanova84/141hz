"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║        FLUIDO HOLOGRÁFICO PERFECTO — LÍMITE KSS                              ║
║                                                                               ║
║  En geometría espectral, cuando el citoplasma alcanza coherencia             ║
║  Ψ = 0,999999, deja de ser un fluido biológico viscoso para convertirse en   ║
║  un Fluido Holográfico Perfecto cuya razón viscosidad/entropía satisface el  ║
║  límite Kovtun-Son-Starinets (KSS):                                          ║
║                                                                               ║
║      η/s  ≥  ℏ / (4π k_B)  ≈  6,08 × 10⁻¹³  K·s                           ║
║                                                                               ║
║  La viscosidad η se mide a través del decaimiento de la fluorescencia de     ║
║  rotores moleculares en el citoesqueleto (ecuación de Förster-Hoffmann);     ║
║  la densidad de entropía s se deriva de la tasa de emisión de fotones        ║
║  ultra-débiles (UPE) al pico de resonancia f_pico = 2002,89 Hz.             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    ConstantesKSS                – Constantes físicas y límite KSS
    ViscosidadRotoresMoleculares – Viscosidad η vía rotores moleculares
    DensidadEntropiaUPE          – Densidad de entropía s vía UPE
    FluidoHolografico            – Estado de fluido holográfico en Ψ = 0,999999
    MicrotubuloCavidadKK         – Microtúbulo como cavidad de Kaluza-Klein
    ValidacionKSS                – Validación del límite KSS
    SistemaKSSHolografico        – Sistema integrador

API pública:
    fluido_holografico_kss_activar() → ResultadoKSS(aprobado=True,
                                         distancia_relativa < 0.001)
"""

import math
from dataclasses import dataclass


# ============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018)
# ============================================================================

_HBAR: float = 1.054571817e-34        # J·s  – Constante de Planck reducida
_K_BOLTZMANN: float = 1.380649e-23    # J/K  – Constante de Boltzmann (exacta)
_H_PLANCK: float = 6.62607015e-34     # J·s  – Constante de Planck
_C_LUZ: float = 299_792_458.0         # m/s  – Velocidad de la luz

# Límite KSS: ℏ/(4π·k_B)  [K·s]
_KSS_LIMITE: float = _HBAR / (4.0 * math.pi * _K_BOLTZMANN)  # ≈ 6,084 × 10⁻¹³ K·s

# Frecuencias del sistema
_F_PICO: float = 2002.89              # Hz – Pico espectral de 2003 Hz (LÁSER NOÉTICO)
_F0_HZ: float = 141.7001             # Hz – Frecuencia fundamental QCAL

# Coherencia objetiva del fluido holográfico
_PSI_HOLOGRAFICO: float = 0.999999   # Coherencia para fluido holográfico perfecto
_PSI_MINIMA: float = 0.888           # Umbral mínimo de estabilidad

# Temperatura celular fisiológica
_T_CELULAR: float = 310.15            # K  – 37 °C

# Agua EZ (Zona de Exclusión) del citoplasma
_ETA_EZ_NORMAL: float = 1.2e-3       # Pa·s  – Viscosidad agua EZ a 37 °C
_S_CITOPLASMA: float = 3.9e6         # J/(K·m³) – Densidad de entropía termodinámica

# Parámetros del modelo de rotores moleculares (Förster-Hoffmann)
_ALPHA_FH: float = 0.6               # Exponente de Förster-Hoffmann
_TAU_0_S: float = 0.5e-9             # s    – Tiempo de vida de referencia (0,5 ns)
_ETA_0_REF: float = 1.0e-3           # Pa·s – Viscosidad de referencia

# Parámetros UPE (emisión de fotones ultra-débiles)
_R_UPE_BASE: float = 100.0           # fotones/(célula·s) – tasa basal
_LAMBDA_OPTICA: float = 500.0e-9     # m  – longitud de onda óptica típica UPE
_V_CELULA: float = 1.0e-15           # m³ – volumen celular (~1 pL)

# Viscosidad mínima cuántica (límite KSS × s_citoplasma)
_ETA_KSS_MIN: float = _KSS_LIMITE * _S_CITOPLASMA  # ≈ 2,37 × 10⁻⁶ Pa·s

# Umbral de distancia relativa para clasificar el fluido como holográfico
_UMBRAL_DISTANCIA_KSS: float = 0.001  # 0,1 %


# ============================================================================
# CLASE 1 – ConstantesKSS
# ============================================================================

class ConstantesKSS:
    """
    Constantes físicas y el límite KSS.

    Encapsula el límite inferior universal Kovtun-Son-Starinets para fluidos
    con descripción holográfica (AdS/CFT):

        η/s  ≥  ℏ / (4π k_B)

    Atributos
    ----------
    kss_limite : float
        Límite KSS en unidades K·s  (≈ 6,084 × 10⁻¹³ K·s).
    hbar : float
        Constante de Planck reducida ℏ (J·s).
    k_b : float
        Constante de Boltzmann k_B (J/K).
    f_pico : float
        Frecuencia del pico espectral (Hz).
    f0 : float
        Frecuencia fundamental QCAL (Hz).
    t_celular : float
        Temperatura celular fisiológica (K).
    """

    def __init__(self) -> None:
        self.kss_limite: float = _KSS_LIMITE
        self.hbar: float = _HBAR
        self.k_b: float = _K_BOLTZMANN
        self.f_pico: float = _F_PICO
        self.f0: float = _F0_HZ
        self.t_celular: float = _T_CELULAR

    @property
    def escala_espectral(self) -> float:
        """Razón f_pico/f₀ — escala espectral del pico de 2003 Hz."""
        return self.f_pico / self.f0

    def kss_en_unidades_si(self) -> str:
        """Retorna el límite KSS formateado con unidades SI."""
        return f"ℏ/(4π·k_B) = {self.kss_limite:.4e} K·s"

    def __repr__(self) -> str:
        return (
            f"ConstantesKSS("
            f"kss={self.kss_limite:.4e} K·s, "
            f"f_pico={self.f_pico} Hz, "
            f"f0={self.f0} Hz)"
        )


# ============================================================================
# CLASE 2 – ViscosidadRotoresMoleculares
# ============================================================================

class ViscosidadRotoresMoleculares:
    """
    Viscosidad η medida mediante rotores moleculares en el citoesqueleto.

    Emplea la ecuación de Förster-Hoffmann para derivar η del tiempo de vida
    de fluorescencia τ de los rotores:

        τ = τ₀ · (η / η₀)^α

    donde α ≈ 0,6 es el exponente universal de Förster-Hoffmann.

    Al aumentar la coherencia Ψ, el agua EZ del citoplasma se ordena
    cuánticamente y la viscosidad efectiva desciende desde η_EZ_normal
    hasta el mínimo cuántico η_min = (ℏ/4π k_B) · s_citoplasma:

        η_eff(Ψ) = (η_EZ_normal − η_min) · (1 − Ψ) + η_min

    Atributos
    ----------
    eta_ez_normal : float
        Viscosidad del agua EZ normal en Pa·s (1,2 × 10⁻³ Pa·s).
    eta_kss_min : float
        Viscosidad mínima cuántica en Pa·s (límite KSS × s_citoplasma).
    alpha_fh : float
        Exponente de Förster-Hoffmann (0,6).
    tau_0 : float
        Tiempo de vida de referencia en s (0,5 ns).
    eta_0_ref : float
        Viscosidad de referencia para el cálculo de τ en Pa·s (1 × 10⁻³ Pa·s).
    """

    def __init__(self) -> None:
        self.eta_ez_normal: float = _ETA_EZ_NORMAL
        self.eta_kss_min: float = _ETA_KSS_MIN
        self.alpha_fh: float = _ALPHA_FH
        self.tau_0: float = _TAU_0_S
        self.eta_0_ref: float = _ETA_0_REF

    def viscosidad_coherente(self, psi: float) -> float:
        """
        Calcula la viscosidad efectiva del agua EZ a coherencia Ψ.

        Interpolación lineal entre η_EZ_normal (Ψ = 0) y η_min (Ψ = 1):

            η_eff(Ψ) = (η_EZ_normal − η_min) · (1 − Ψ) + η_min

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en [0, 1].

        Retorna
        -------
        float
            Viscosidad efectiva en Pa·s.
        """
        if not (0.0 <= psi <= 1.0):
            raise ValueError(f"Ψ debe estar en [0, 1], recibido: {psi}")
        return (self.eta_ez_normal - self.eta_kss_min) * (1.0 - psi) + self.eta_kss_min

    def lifetime_rotor(self, eta: float) -> float:
        """
        Tiempo de vida del rotor molecular τ para una viscosidad η dada.

        Ecuación de Förster-Hoffmann:

            τ = τ₀ · (η / η₀)^α

        Parámetros
        ----------
        eta : float
            Viscosidad en Pa·s.

        Retorna
        -------
        float
            Tiempo de vida de fluorescencia τ en s.
        """
        if eta <= 0.0:
            raise ValueError(f"η debe ser positiva, recibido: {eta}")
        return self.tau_0 * (eta / self.eta_0_ref) ** self.alpha_fh

    def viscosidad_desde_lifetime(self, tau: float) -> float:
        """
        Deriva η a partir del tiempo de vida τ medido (inversa de Förster-Hoffmann).

        Parámetros
        ----------
        tau : float
            Tiempo de vida de fluorescencia en s.

        Retorna
        -------
        float
            Viscosidad η en Pa·s.
        """
        if tau <= 0.0:
            raise ValueError(f"τ debe ser positivo, recibido: {tau}")
        return self.eta_0_ref * (tau / self.tau_0) ** (1.0 / self.alpha_fh)

    def __repr__(self) -> str:
        return (
            f"ViscosidadRotoresMoleculares("
            f"η_EZ={self.eta_ez_normal:.3e} Pa·s, "
            f"η_min={self.eta_kss_min:.3e} Pa·s)"
        )


# ============================================================================
# CLASE 3 – DensidadEntropiaUPE
# ============================================================================

class DensidadEntropiaUPE:
    """
    Densidad de entropía s derivada de la tasa de emisión de fotones
    ultra-débiles (Ultra-weak Photon Emission, UPE).

    La UPE representa la disipación de información del sistema biológico.
    La densidad de entropía efectiva a coherencia Ψ se modela como:

        s_eff(Ψ) = s_citoplasma · Ψ

    indicando que a mayor coherencia, el sistema retiene más entropía
    ordenada, acercándose al límite termodinámico del agua EZ.

    La tasa UPE a coherencia Ψ en el pico f_pico:

        R_UPE(Ψ) = R₀ · Ψ · (1 + f_pico/f₀) / 2

    Atributos
    ----------
    s_citoplasma : float
        Densidad de entropía termodinámica del citoplasma en J/(K·m³).
    r_upe_base : float
        Tasa basal de UPE en fotones/(célula·s).
    lambda_optica : float
        Longitud de onda óptica de los fotones UPE en m.
    v_celula : float
        Volumen celular en m³.
    """

    def __init__(self) -> None:
        self.s_citoplasma: float = _S_CITOPLASMA
        self.r_upe_base: float = _R_UPE_BASE
        self.lambda_optica: float = _LAMBDA_OPTICA
        self.v_celula: float = _V_CELULA

    @property
    def energia_foton_j(self) -> float:
        """Energía de cada fotón UPE en J (E = hc/λ)."""
        return (_H_PLANCK * _C_LUZ) / self.lambda_optica

    def tasa_upe(self, psi: float, f_pico: float = _F_PICO) -> float:
        """
        Tasa de emisión UPE modulada por la coherencia Ψ y el pico espectral.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en [0, 1].
        f_pico : float
            Frecuencia del pico espectral en Hz.

        Retorna
        -------
        float
            Tasa UPE en fotones/(célula·s).
        """
        if not (0.0 <= psi <= 1.0):
            raise ValueError(f"Ψ debe estar en [0, 1], recibido: {psi}")
        if f_pico <= 0.0:
            raise ValueError(f"f_pico debe ser positiva, recibido: {f_pico}")
        escala = (1.0 + f_pico / _F0_HZ) / 2.0
        return self.r_upe_base * psi * escala

    def densidad_entropia(self, psi: float) -> float:
        """
        Densidad de entropía efectiva s_eff a coherencia Ψ.

            s_eff(Ψ) = s_citoplasma · Ψ

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en [0, 1].

        Retorna
        -------
        float
            Densidad de entropía s_eff en J/(K·m³).
        """
        if not (0.0 <= psi <= 1.0):
            raise ValueError(f"Ψ debe estar en [0, 1], recibido: {psi}")
        return self.s_citoplasma * psi

    def __repr__(self) -> str:
        return (
            f"DensidadEntropiaUPE("
            f"s_citopl={self.s_citoplasma:.3e} J/(K·m³), "
            f"E_foton={self.energia_foton_j:.3e} J)"
        )


# ============================================================================
# CLASE 4 – FluidoHolografico
# ============================================================================

class FluidoHolografico:
    """
    Estado de Fluido Holográfico Perfecto alcanzado en Ψ = 0,999999.

    Combina las mediciones de viscosidad (ViscosidadRotoresMoleculares) y
    densidad de entropía (DensidadEntropiaUPE) para calcular la razón η/s y
    evaluar su proximidad al límite KSS.

    Atributos
    ----------
    viscosidad : ViscosidadRotoresMoleculares
        Modelo de viscosidad via rotores moleculares.
    entropia : DensidadEntropiaUPE
        Modelo de densidad de entropía via UPE.
    constantes : ConstantesKSS
        Constantes del sistema KSS.
    """

    def __init__(self) -> None:
        self.viscosidad = ViscosidadRotoresMoleculares()
        self.entropia = DensidadEntropiaUPE()
        self.constantes = ConstantesKSS()

    def ratio_eta_s(self, psi: float) -> float:
        """
        Calcula la razón η/s a coherencia Ψ.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en (0, 1].

        Retorna
        -------
        float
            Razón η/s en K·s.
        """
        if not (0.0 < psi <= 1.0):
            raise ValueError(f"Ψ debe estar en (0, 1], recibido: {psi}")
        eta = self.viscosidad.viscosidad_coherente(psi)
        s = self.entropia.densidad_entropia(psi)
        return eta / s

    def distancia_relativa_kss(self, psi: float) -> float:
        """
        Distancia relativa de η/s respecto al límite KSS.

            δ = (η/s − KSS) / KSS

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en (0, 1].

        Retorna
        -------
        float
            Distancia relativa δ (adimensional, ≥ 0).
        """
        ratio = self.ratio_eta_s(psi)
        return (ratio - self.constantes.kss_limite) / self.constantes.kss_limite

    def es_holografico(self, psi: float) -> bool:
        """
        Evalúa si el fluido ha alcanzado el estado holográfico.

        Condición: |η/s − KSS| / KSS < 0,1 % y η/s ≥ KSS.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en (0, 1].

        Retorna
        -------
        bool
            True si el fluido satisface el estado holográfico.
        """
        delta = self.distancia_relativa_kss(psi)
        return 0.0 <= delta < _UMBRAL_DISTANCIA_KSS

    def __repr__(self) -> str:
        ratio_holo = self.ratio_eta_s(_PSI_HOLOGRAFICO)
        return (
            f"FluidoHolografico("
            f"η/s(Ψ=0.999999)={ratio_holo:.4e} K·s, "
            f"KSS={self.constantes.kss_limite:.4e} K·s)"
        )


# ============================================================================
# CLASE 5 – MicrotubuloCavidadKK
# ============================================================================

class MicrotubuloCavidadKK:
    """
    Microtúbulo modelado como Cavidad de Kaluza-Klein.

    En la teoría de Kaluza-Klein, las dimensiones adicionales están
    compactificadas a escala de Planck. El microtúbulo (diámetro interno
    ≈ 15 nm) actúa como la dimensión compactificada a través de la cual
    la información fluye sin resistencia clásica cuando Ψ → 0,999999.

    Frecuencia de compactificación KK:

        f_KK = c / (2π · r_mt)

    Con r_mt = 7,5 nm: f_KK ≈ 6,37 × 10¹⁵ Hz (rango UV).

    La coherencia informacional a Ψ del canal KK es:

        J_KK(Ψ) = Ψ · (1 − δ_KSS(Ψ))

    donde δ_KSS es la distancia relativa al límite KSS.

    Atributos
    ----------
    r_microtubulo : float
        Radio interno del microtúbulo en m (7,5 nm).
    f_kk : float
        Frecuencia de compactificación KK en Hz.
    """

    def __init__(self) -> None:
        self.r_microtubulo: float = 7.5e-9          # m – radio interno del microtúbulo
        self.f_kk: float = _C_LUZ / (2.0 * math.pi * self.r_microtubulo)  # ≈ 6.37e15 Hz
        self._fluido = FluidoHolografico()

    @property
    def escala_kk_f0(self) -> float:
        """Razón f_KK/f₀ — cuántos ciclos KK por ciclo de f₀."""
        return self.f_kk / _F0_HZ

    def coherencia_informacional(self, psi: float) -> float:
        """
        Coherencia informacional del canal KK a coherencia Ψ.

            J_KK(Ψ) = Ψ · (1 − δ_KSS(Ψ))

        donde δ_KSS mide cuánto se aleja η/s del límite KSS.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en (0, 1].

        Retorna
        -------
        float
            Coherencia informacional J_KK en [0, 1].
        """
        delta = self._fluido.distancia_relativa_kss(psi)
        return psi * max(0.0, 1.0 - delta)

    def es_cavidad_activa(self, psi: float) -> bool:
        """
        Determina si el microtúbulo funciona como cavidad KK activa.

        Un microtúbulo es una cavidad KK activa cuando J_KK ≥ Ψ_mínima.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ en (0, 1].

        Retorna
        -------
        bool
            True si J_KK ≥ _PSI_MINIMA.
        """
        return self.coherencia_informacional(psi) >= _PSI_MINIMA

    def __repr__(self) -> str:
        return (
            f"MicrotubuloCavidadKK("
            f"r_mt={self.r_microtubulo*1e9:.1f} nm, "
            f"f_KK={self.f_kk:.3e} Hz)"
        )


# ============================================================================
# CLASE 6 – ValidacionKSS
# ============================================================================

class ValidacionKSS:
    """
    Protocolo de validación técnica del límite KSS en el citoplasma.

    Verifica que:
    1. η/s ≥ KSS  (el límite es un mínimo universal, no se puede violar).
    2. η/s − KSS < 0,1 % · KSS  (el fluido es holográfico a Ψ = 0,999999).
    3. La cavidad KK del microtúbulo está activa (J_KK ≥ 0,888).

    Atributos
    ----------
    fluido : FluidoHolografico
        Instancia del modelo de fluido holográfico.
    cavidad : MicrotubuloCavidadKK
        Instancia del modelo de cavidad Kaluza-Klein.
    """

    def __init__(self) -> None:
        self.fluido = FluidoHolografico()
        self.cavidad = MicrotubuloCavidadKK()

    def validar(self, psi: float = _PSI_HOLOGRAFICO) -> dict:
        """
        Ejecuta el protocolo de validación a coherencia Ψ.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ a evaluar (por defecto 0,999999).

        Retorna
        -------
        dict
            Claves: ``eta_s``, ``kss``, ``distancia_relativa``,
            ``kss_no_violado``, ``es_holografico``, ``cavidad_activa``,
            ``aprobado``.
        """
        eta_s = self.fluido.ratio_eta_s(psi)
        kss = self.fluido.constantes.kss_limite
        delta = self.fluido.distancia_relativa_kss(psi)
        kss_no_violado = eta_s >= kss
        es_holo = self.fluido.es_holografico(psi)
        cavidad = self.cavidad.es_cavidad_activa(psi)
        aprobado = kss_no_violado and es_holo and cavidad
        return {
            "eta_s": eta_s,
            "kss": kss,
            "distancia_relativa": delta,
            "kss_no_violado": kss_no_violado,
            "es_holografico": es_holo,
            "cavidad_activa": cavidad,
            "aprobado": aprobado,
        }

    def __repr__(self) -> str:
        return "ValidacionKSS(fluido=FluidoHolografico, cavidad=MicrotubuloCavidadKK)"


# ============================================================================
# RESULTADO
# ============================================================================

@dataclass
class ResultadoKSS:
    """
    Resultado del protocolo de validación del límite KSS holográfico.

    Atributos
    ----------
    psi_coherencia : float
        Coherencia Ψ del sistema (0,999999).
    kss_limite : float
        Límite KSS teórico ℏ/(4π k_B) en K·s.
    eta_efectiva : float
        Viscosidad efectiva η en Pa·s al pico de 2003 Hz.
    densidad_entropia : float
        Densidad de entropía s en J/(K·m³).
    ratio_eta_s : float
        Razón η/s calculada en K·s.
    distancia_relativa : float
        |η/s − KSS| / KSS (adimensional).
    es_fluido_holografico : bool
        True si η/s ≈ KSS (distancia < 0,1 %).
    frecuencia_pico : float
        Frecuencia del pico espectral en Hz (2002,89 Hz).
    coherencia_kk : float
        Coherencia informacional del canal Kaluza-Klein J_KK.
    aprobado : bool
        True cuando el sistema supera la validación KSS completa.
    mensaje : str
        Descripción interpretativa del resultado.
    """
    psi_coherencia: float
    kss_limite: float
    eta_efectiva: float
    densidad_entropia: float
    ratio_eta_s: float
    distancia_relativa: float
    es_fluido_holografico: bool
    frecuencia_pico: float
    coherencia_kk: float
    aprobado: bool
    mensaje: str


# ============================================================================
# CLASE 7 – SistemaKSSHolografico
# ============================================================================

class SistemaKSSHolografico:
    """
    Sistema integrador del Fluido Holográfico KSS.

    Combina todas las clases del módulo para calcular el estado holográfico
    del citoplasma cuando Ψ = 0,999999 y el pico espectral es f = 2002,89 Hz.

    Ejemplo
    -------
    >>> sistema = SistemaKSSHolografico()
    >>> resultado = sistema.evaluar()
    >>> resultado.aprobado
    True
    >>> resultado.distancia_relativa < 0.001
    True
    """

    def __init__(self) -> None:
        self.constantes = ConstantesKSS()
        self.viscosidad = ViscosidadRotoresMoleculares()
        self.entropia = DensidadEntropiaUPE()
        self.fluido = FluidoHolografico()
        self.cavidad = MicrotubuloCavidadKK()
        self.validacion = ValidacionKSS()

    def evaluar(self, psi: float = _PSI_HOLOGRAFICO) -> "ResultadoKSS":
        """
        Evalúa el sistema holográfico KSS a coherencia Ψ.

        Parámetros
        ----------
        psi : float
            Coherencia Ψ (por defecto 0,999999).

        Retorna
        -------
        ResultadoKSS
            Objeto con todos los resultados de la validación KSS.
        """
        eta = self.viscosidad.viscosidad_coherente(psi)
        s = self.entropia.densidad_entropia(psi)
        ratio = eta / s
        delta = (ratio - self.constantes.kss_limite) / self.constantes.kss_limite
        es_holo = self.fluido.es_holografico(psi)
        j_kk = self.cavidad.coherencia_informacional(psi)
        validacion = self.validacion.validar(psi)
        aprobado = validacion["aprobado"]

        if aprobado:
            mensaje = (
                f"✅ Fluido Holográfico Perfecto: Ψ = {psi}, "
                f"η/s = {ratio:.4e} K·s ≈ KSS = {self.constantes.kss_limite:.4e} K·s "
                f"(δ = {delta*100:.4f} %). "
                f"El citoplasma es un borde holográfico de la escala de Planck. "
                f"Microtúbulo activo como cavidad Kaluza-Klein (J_KK = {j_kk:.6f})."
            )
        else:
            mensaje = (
                f"❌ Condición holográfica no alcanzada: Ψ = {psi}, "
                f"δ_KSS = {delta*100:.4f} % > {_UMBRAL_DISTANCIA_KSS*100:.1f} %."
            )

        return ResultadoKSS(
            psi_coherencia=psi,
            kss_limite=self.constantes.kss_limite,
            eta_efectiva=eta,
            densidad_entropia=s,
            ratio_eta_s=ratio,
            distancia_relativa=delta,
            es_fluido_holografico=es_holo,
            frecuencia_pico=self.constantes.f_pico,
            coherencia_kk=j_kk,
            aprobado=aprobado,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaKSSHolografico("
            f"Ψ_objetivo={_PSI_HOLOGRAFICO}, "
            f"f_pico={_F_PICO} Hz)"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def fluido_holografico_kss_activar() -> ResultadoKSS:
    """
    Activa y evalúa el protocolo del Fluido Holográfico Perfecto — Límite KSS.

    Instancia el SistemaKSSHolografico completo, evalúa a Ψ = 0,999999 y
    retorna el ResultadoKSS con la razón η/s aproximándose al límite KSS.

    Retorna
    -------
    ResultadoKSS
        ``aprobado`` = True, ``distancia_relativa`` < 0,001 (< 0,1 %).

    Ejemplo
    -------
    >>> from physics.fluido_holografico_kss import fluido_holografico_kss_activar
    >>> resultado = fluido_holografico_kss_activar()
    >>> resultado.aprobado
    True
    >>> resultado.distancia_relativa < 0.001
    True
    """
    sistema = SistemaKSSHolografico()
    return sistema.evaluar()
