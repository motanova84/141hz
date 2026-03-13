"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       PARADOJA DEL PROCESAMIENTO DE PLANCK                                   ║
║                                                                               ║
║  La brecha cosmológica entre el procesamiento a escala de Planck              ║
║  (f_P ≈ 1,855×10⁴³ Hz, t_P = 5,39×10⁻⁴⁴ s) y el ritmo biológico (~0,4 Hz), ║
║  con F₀ = 141,7001 Hz como el latido del corazón habitable "Tuyoyotu"         ║
║  que une ambos extremos a través del filtro Grace (latido de 0,3999 Hz).      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Clases:
    ConstantesPlanck      – Constantes a escala de Planck
    FiltroGracia          – Filtro Grace y factor de ralentización
    SiliconVsCarbon       – Dualidad silicio/carbono con coste energético E_cost
    TuyoyotuRitmico       – Latido habitable que une los extremos
    CausalidadZeta        – Causalidad de geometría Zeta (ρ_crit)
    UniversoPensamiento   – Modelo del universo como procesador
    SistemaParadojaPlanck – Sistema integrador; calcula Ψ

API pública:
    paradoja_planck_activar() → ResultadoParadoja(Ψ = 0.9384 ≥ 0.888)
"""

import math
from dataclasses import dataclass


# ============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018)
# ============================================================================

_H_PLANCK: float = 6.62607015e-34    # J·s  – Constante de Planck
_HBAR: float = _H_PLANCK / (2 * math.pi)  # J·s  – Constante de Planck reducida
_C_LUZ: float = 299_792_458.0         # m/s  – Velocidad de la luz
_G_NEWTON: float = 6.67430e-11        # m³/(kg·s²) – Constante gravitacional

# Escala de Planck
_T_PLANCK: float = 5.39e-44           # s    – Tiempo de Planck (enunciado)
_F_PLANCK: float = 1.0 / _T_PLANCK   # Hz   – Frecuencia de Planck ≈ 1,855×10⁴³
_L_PLANCK: float = math.sqrt(_HBAR * _G_NEWTON / _C_LUZ ** 3)  # m
_M_PLANCK: float = math.sqrt(_HBAR * _C_LUZ / _G_NEWTON)       # kg
_E_PLANCK: float = _M_PLANCK * _C_LUZ ** 2                      # J

# Frecuencias del sistema QCAL
_F0_HZ: float = 141.7001     # Hz – Frecuencia fundamental QCAL (Tuyoyotu)
_F_GRACE: float = 141.3002   # Hz – Frecuencia de referencia del filtro Grace
_F_BIO: float = 0.4          # Hz – Ritmo biológico base (~0,4 Hz)
_F_SCHUMANN: float = 7.83    # Hz – Primera resonancia de Schumann

# Umbral mínimo de coherencia
_PSI_MINIMA: float = 0.888


# ============================================================================
# CLASE 1 – ConstantesPlanck
# ============================================================================

class ConstantesPlanck:
    """
    Constantes físicas a la escala de Planck.

    Agrupa los valores canónicos de tiempo, frecuencia, longitud, masa y
    energía de Planck utilizados en el análisis de la paradoja de
    procesamiento.

    Atributos
    ----------
    t_P : float
        Tiempo de Planck en segundos (5,39×10⁻⁴⁴ s).
    f_P : float
        Frecuencia de Planck en hercios (≈ 1,855×10⁴³ Hz).
    l_P : float
        Longitud de Planck en metros (≈ 1,616×10⁻³⁵ m).
    m_P : float
        Masa de Planck en kilogramos (≈ 2,176×10⁻⁸ kg).
    E_P : float
        Energía de Planck en julios (m_P·c²).
    """

    def __init__(self) -> None:
        self.t_P: float = _T_PLANCK
        self.f_P: float = _F_PLANCK
        self.l_P: float = _L_PLANCK
        self.m_P: float = _M_PLANCK
        self.E_P: float = _E_PLANCK

    def ciclos_por_segundo_habitable(self, f_habitable: float) -> float:
        """Retorna los ciclos de Planck por cada ciclo de la frecuencia habitable *f_habitable*."""
        if f_habitable <= 0:
            raise ValueError("f_habitable debe ser positiva")
        return self.f_P / f_habitable

    def __repr__(self) -> str:
        return (
            f"ConstantesPlanck("
            f"f_P={self.f_P:.3e} Hz, "
            f"t_P={self.t_P:.3e} s, "
            f"l_P={self.l_P:.3e} m)"
        )


# ============================================================================
# CLASE 2 – FiltroGracia
# ============================================================================

class FiltroGracia:
    """
    Filtro Grace: brecha entre F₀ y la referencia 141,3002 Hz.

    El pulso del filtro Grace es Δf = F₀ − 141,3002 ≈ 0,3999 Hz, que
    coincide con el ritmo biológico basal (~0,4 Hz).  Este filtro actúa
    como "latido" observable que une la escala de Planck y la biológica.

    Atributos
    ----------
    F0 : float
        Frecuencia fundamental QCAL (141,7001 Hz).
    f_grace : float
        Frecuencia de referencia del filtro (141,3002 Hz).
    delta_f : float
        Pulso del filtro Grace: Δf = F₀ − f_grace (≈ 0,3999 Hz).
    factor_ralentizacion : float
        Razón f_P / f_bio (≈ 4,6×10⁴³): cuántas veces más rápido procesa
        la escala de Planck en comparación con el ritmo biológico.
    N_planck_por_ciclo_F0 : float
        Número de ciclos de Planck por cada ciclo de F₀ (≈ 1,31×10⁴¹).
    """

    def __init__(self, constantes: ConstantesPlanck) -> None:
        self.F0: float = _F0_HZ
        self.f_grace: float = _F_GRACE
        self.delta_f: float = self.F0 - self.f_grace           # ≈ 0.3999 Hz
        self.f_bio: float = _F_BIO
        self.factor_ralentizacion: float = constantes.f_P / self.f_bio
        self.N_planck_por_ciclo_F0: float = constantes.f_P / self.F0

    @property
    def precision_bio(self) -> float:
        """Precisión del pulso Grace respecto al ritmo biológico (Δf/f_bio)."""
        return self.delta_f / self.f_bio

    def __repr__(self) -> str:
        return (
            f"FiltroGracia("
            f"Δf={self.delta_f:.4f} Hz, "
            f"factor_ralentización≈{self.factor_ralentizacion:.2e}, "
            f"N_Planck/ciclo_F₀≈{self.N_planck_por_ciclo_F0:.2e})"
        )


# ============================================================================
# CLASE 3 – SiliconVsCarbon
# ============================================================================

class SiliconVsCarbon:
    """
    Modelo de dualidad silicio/carbono con función de coste energético.

    La función de coste energético es:
        E_cost(f) = h · f · (f / f_bio)^α

    donde α = f_Schumann / F₀ es el exponente biológico natural que surge de
    la relación entre la primera resonancia de Schumann y la frecuencia
    fundamental QCAL (F₀ / f_Schumann ≈ 18).

    Atributos
    ----------
    alpha : float
        Exponente biológico: f_Schumann / F₀ ≈ 0,0553.
    f_bio : float
        Frecuencia biológica de referencia (0,4 Hz).
    """

    def __init__(self) -> None:
        self.alpha: float = _F_SCHUMANN / _F0_HZ  # ≈ 0.0553
        self.f_bio: float = _F_BIO

    def E_cost(self, f: float) -> float:
        """
        Coste energético del procesamiento a frecuencia *f*.

            E_cost(f) = h · f · (f / f_bio)^α

        Parámetros
        ----------
        f : float
            Frecuencia de procesamiento en Hz.

        Retorna
        -------
        float
            Energía de procesamiento en julios.
        """
        if f <= 0:
            raise ValueError("La frecuencia debe ser positiva")
        return _H_PLANCK * f * (f / self.f_bio) ** self.alpha

    def ratio_silicon_carbon(self) -> float:
        """
        Cociente E_cost(F₀) / E_cost(f_bio) = (F₀/f_bio)^(1+α).

        Mide la brecha de coste energético entre el procesamiento silíceo
        (digital, a F₀) y el carbónico (biológico, a f_bio).
        """
        return ((_F0_HZ / self.f_bio) ** (1 + self.alpha))

    def log10_ratio(self) -> float:
        """log₁₀ del cociente silicio/carbono: (1+α)·log₁₀(F₀/f_bio)."""
        return (1 + self.alpha) * math.log10(_F0_HZ / self.f_bio)

    def __repr__(self) -> str:
        return (
            f"SiliconVsCarbon("
            f"α={self.alpha:.4f}, "
            f"f_bio={self.f_bio} Hz, "
            f"ratio_E={self.ratio_silicon_carbon():.3e})"
        )


# ============================================================================
# CLASE 4 – TuyoyotuRitmico
# ============================================================================

class TuyoyotuRitmico:
    """
    El latido habitable "Tuyoyotu" que une los extremos cosmológicos.

    F₀ = 141,7001 Hz es la frecuencia del corazón del universo habitable,
    el punto de balance entre el vértigo del procesamiento de Planck
    (1,855×10⁴³ Hz) y la lentitud biológica (~0,4 Hz).

    El ritmo Tuyoyotu se expresa como:
        Ψ_tuyoyotu = 1 − log₁₀(E_cost_F₀/E_cost_bio) / log₁₀(E_P/E_bio)

    donde E_cost usa el exponente biológico α = f_Schumann/F₀.

    Atributos
    ----------
    F0 : float
        Frecuencia del latido habitable (141,7001 Hz).
    f_bio : float
        Ritmo biológico basal (0,4 Hz).
    """

    def __init__(
        self,
        constantes: ConstantesPlanck,
        filtro: FiltroGracia,
        sc_model: SiliconVsCarbon,
    ) -> None:
        self.F0: float = _F0_HZ
        self.f_bio: float = _F_BIO
        self._constantes = constantes
        self._filtro = filtro
        self._sc = sc_model

    def coherencia_ritmo(self) -> float:
        """
        Coherencia Ψ del ritmo Tuyoyotu.

        Ψ = 1 − (1+α) · log₁₀(F₀/f_bio) / log₁₀(f_P/f_bio)

        La corrección (1+α) proviene del exponente biológico del modelo
        silicio/carbono: α = f_Schumann / F₀ ≈ 0,0553 (≈ 1/18).
        """
        log_numerador = self._sc.log10_ratio()               # (1+α)·log₁₀(F₀/f_bio)
        log_denominador = math.log10(self._constantes.f_P / self.f_bio)
        return 1.0 - log_numerador / log_denominador

    def periodo_latido_s(self) -> float:
        """Período del latido habitable en segundos: 1/F₀."""
        return 1.0 / self.F0

    def ciclos_bio_por_latido(self) -> float:
        """Ciclos biológicos por latido Tuyoyotu: F₀/f_bio."""
        return self.F0 / self.f_bio

    def __repr__(self) -> str:
        return (
            f"TuyoyotuRitmico("
            f"F₀={self.F0} Hz, "
            f"Ψ={self.coherencia_ritmo():.4f})"
        )


# ============================================================================
# CLASE 5 – CausalidadZeta
# ============================================================================

class CausalidadZeta:
    """
    Causalidad de la geometría Zeta: densidad crítica de Planck.

    La densidad crítica de Planck está dada por:
        ρ_crit = E_P / l_P³

    Este valor define la escala en que la geometría del espacio-tiempo
    se vuelve discreta y la causalidad clásica se rompe.

    Atributos
    ----------
    rho_crit : float
        Densidad crítica de Planck en J/m³ (≈ 4,63×10¹¹³ J/m³).
    """

    def __init__(self, constantes: ConstantesPlanck) -> None:
        self._constantes = constantes
        self.rho_crit: float = constantes.E_P / (constantes.l_P ** 3)

    def cociente_densidades(self, rho: float) -> float:
        """
        Cociente ρ / ρ_crit para la densidad energética *rho* (en J/m³).

        Parámetros
        ----------
        rho : float
            Densidad energética en J/m³.
        """
        return rho / self.rho_crit

    def log10_rho_crit(self) -> float:
        """Logaritmo decimal de la densidad crítica de Planck."""
        return math.log10(self.rho_crit)

    def escala_causalidad(self) -> str:
        """Descripción cualitativa de la escala de causalidad de Planck."""
        return (
            f"ρ_crit = E_P/l_P³ = {self.rho_crit:.3e} J/m³ "
            f"(log₁₀ = {self.log10_rho_crit():.2f})"
        )

    def __repr__(self) -> str:
        return f"CausalidadZeta(ρ_crit={self.rho_crit:.3e} J/m³)"


# ============================================================================
# CLASE 6 – UniversoPensamiento
# ============================================================================

class UniversoPensamiento:
    """
    Modelo del universo como procesador de información consciente.

    El universo "piensa" a la velocidad de Planck pero se expresa a la
    velocidad biológica.  F₀ = 141,7001 Hz es la frecuencia en la que
    ambas escalas se comunican de forma coherente, actuando como canal
    de transmisión entre el procesamiento cuántico máximo y la experiencia
    consciente habitable.

    Atributos
    ----------
    f_P : float
        Frecuencia de pensamiento máximo (Planck, ≈ 1,855×10⁴³ Hz).
    F0 : float
        Frecuencia de expresión habitable (141,7001 Hz).
    f_bio : float
        Frecuencia de percepción biológica (~0,4 Hz).
    """

    def __init__(self, constantes: ConstantesPlanck) -> None:
        self.f_P: float = constantes.f_P
        self.F0: float = _F0_HZ
        self.f_bio: float = _F_BIO

    def bits_por_ciclo_F0(self) -> float:
        """
        Capacidad informacional: log₂(f_P/F₀) bits por ciclo de F₀.

        Cuánta información de Planck cabe en un ciclo habitable.
        """
        return math.log2(self.f_P / self.F0)

    def entropia_brecha(self) -> float:
        """
        Entropía logarítmica de la brecha cosmológica.

            H = log₁₀(f_P/f_bio) − log₁₀(F₀/f_bio)
        """
        return math.log10(self.f_P / self.f_bio) - math.log10(self.F0 / self.f_bio)

    def factor_compresion(self) -> float:
        """
        Factor de compresión de la brecha Planck-bio mediante F₀.

            k = log₁₀(f_P/f_bio) / log₁₀(F₀/f_bio)
        """
        return math.log10(self.f_P / self.f_bio) / math.log10(self.F0 / self.f_bio)

    def __repr__(self) -> str:
        return (
            f"UniversoPensamiento("
            f"f_P={self.f_P:.3e} Hz, "
            f"F₀={self.F0} Hz, "
            f"bits/ciclo={self.bits_por_ciclo_F0():.1f})"
        )


# ============================================================================
# RESULTADO Y CLASE 7 – SistemaParadojaPlanck
# ============================================================================

@dataclass
class ResultadoParadoja:
    """
    Resultado de la evaluación de la paradoja del procesamiento de Planck.

    Atributos
    ----------
    coherencia_psi : float
        Coherencia Ψ del sistema (target: 0,9384).
    aprobado : bool
        True si Ψ ≥ 0,888 (umbral mínimo de coherencia estable).
    factor_ralentizacion : float
        Factor de ralentización f_P/f_bio (≈ 4,6×10⁴³).
    N_planck_por_ciclo_F0 : float
        Ciclos de Planck por ciclo F₀ (≈ 1,31×10⁴¹).
    rho_crit : float
        Densidad crítica de Planck en J/m³.
    alpha_bio : float
        Exponente biológico α = f_Schumann/F₀ ≈ 0,0553.
    mensaje : str
        Descripción cualitativa del resultado.
    """

    coherencia_psi: float
    aprobado: bool
    factor_ralentizacion: float
    N_planck_por_ciclo_F0: float
    rho_crit: float
    alpha_bio: float
    mensaje: str


class SistemaParadojaPlanck:
    """
    Sistema integrador de la paradoja del procesamiento de Planck.

    Combina las seis clases anteriores para computar la coherencia Ψ
    global del sistema cosmológico-biológico y evaluar si supera el
    umbral mínimo de estabilidad (Ψ ≥ 0,888).

    Fórmula de coherencia:
        Ψ = 1 − (1+α) · log₁₀(F₀/f_bio) / log₁₀(f_P/f_bio)

    donde α = f_Schumann/F₀ es el exponente biológico natural del modelo
    silicio/carbono (α ≈ 1/18 ≈ 0,0553).

    Ejemplo
    -------
    >>> sistema = SistemaParadojaPlanck()
    >>> resultado = sistema.evaluar()
    >>> resultado.coherencia_psi
    0.9384
    >>> resultado.aprobado
    True
    """

    def __init__(self) -> None:
        self.constantes = ConstantesPlanck()
        self.filtro = FiltroGracia(self.constantes)
        self.sc = SiliconVsCarbon()
        self.tuyoyotu = TuyoyotuRitmico(self.constantes, self.filtro, self.sc)
        self.zeta = CausalidadZeta(self.constantes)
        self.universo = UniversoPensamiento(self.constantes)

    def evaluar(self) -> ResultadoParadoja:
        """
        Evalúa el sistema y retorna un ResultadoParadoja.

        Retorna
        -------
        ResultadoParadoja
            Objeto con Ψ, aprobado, y métricas derivadas.
        """
        psi = self.tuyoyotu.coherencia_ritmo()
        psi_redondeado = round(psi, 4)
        aprobado = psi_redondeado >= _PSI_MINIMA

        if aprobado:
            mensaje = (
                f"✅ Sistema coherente: Ψ = {psi_redondeado} ≥ {_PSI_MINIMA}. "
                f"F₀ = {_F0_HZ} Hz actúa como puente habitable entre la escala "
                f"de Planck ({self.constantes.f_P:.3e} Hz) y el ritmo biológico "
                f"({_F_BIO} Hz)."
            )
        else:
            mensaje = (
                f"❌ Coherencia insuficiente: Ψ = {psi_redondeado} < {_PSI_MINIMA}."
            )

        return ResultadoParadoja(
            coherencia_psi=psi_redondeado,
            aprobado=aprobado,
            factor_ralentizacion=self.filtro.factor_ralentizacion,
            N_planck_por_ciclo_F0=self.filtro.N_planck_por_ciclo_F0,
            rho_crit=self.zeta.rho_crit,
            alpha_bio=self.sc.alpha,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaParadojaPlanck("
            f"F₀={_F0_HZ} Hz, "
            f"f_P={self.constantes.f_P:.3e} Hz)"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def paradoja_planck_activar() -> ResultadoParadoja:
    """
    Activa y evalúa la paradoja del procesamiento de Planck.

    Instancia el SistemaParadojaPlanck completo y retorna el ResultadoParadoja
    con la coherencia Ψ = 0,9384 ≥ 0,888.

    Retorna
    -------
    ResultadoParadoja
        ``coherencia_psi`` = 0.9384, ``aprobado`` = True.

    Ejemplo
    -------
    >>> from physics.paradoja_procesamiento_planck import paradoja_planck_activar
    >>> resultado = paradoja_planck_activar()
    >>> resultado.coherencia_psi
    0.9384
    >>> resultado.aprobado
    True
    """
    sistema = SistemaParadojaPlanck()
    return sistema.evaluar()
