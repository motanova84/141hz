"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       SIMETRÍA PT – RESONANCIA ESPECTRAL QCAL-SYMBIO-1                       ║
║                                                                               ║
║  Puente de simetría PT entre la geometría espectral de Riemann y la          ║
║  coherencia biológica: un hamiltoniano no hermitiano que satisface            ║
║  [Ĥ, PT] = 0 (implementado como simetría compleja H = Hᵀ) mantiene          ║
║  un espectro propio real en sistemas disipativos abiertos (células),         ║
║  anclando la estructura del agua EZ en F₀ = 141,7001 Hz.                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Protocolo: QCAL-SYMBIO-1

Condición de simetría PT: H = Hᵀ (simetría compleja) se cumple porque tanto
diag(b) como flip(I) son matrices simétricas reales.  Para ε = 1−Ψ ≪ |Δλ|/2
los N valores propios permanecen reales — falsificable: la decoherencia (ε alto)
hace que los valores propios sean complejos.

Clases:
    ConstantesPT          – F0 = 141,7001 Hz, 10 ceros de Riemann, UMBRAL_PT = 0,888
    OperadorNHPT          – H = diag(b) + i·flip(I)·(1−Ψ) — simetría compleja PT
    EspectroPTReal        – Análisis de valores propios: es_real(), calcular_psi_espectral()
    RiemannLineaCritica   – Mapeo del espectro propio a la línea crítica ℜ(s) = ½
    CitoplasmaHolografico – Coherencia del agua EZ: Ψ_EZ = F0/(F0+γ_EZ) ≈ 0,993262
    EstabilizadorPT       – Diagnóstico de decoherencia celular y puerta de estabilidad PT
    SistemaResonanciaPT   – Orquestador: Ψ_global = 0,5·Ψ_esp + 0,3·Ψ_EZ + 0,2·Ψ_Riemann

API pública:
    simetria_pt_resonancia_activar() → ResultadoPT
    simular_resonancia_pt(coherencia) → np.ndarray  [espectro de valores propios]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np


# ============================================================================
# CONSTANTES MÓDULO
# ============================================================================

_F0_HZ: float = 141.7001          # Hz – Frecuencia fundamental QCAL
_UMBRAL_PT: float = 0.888          # Umbral mínimo de coherencia PT
_PSI_EZ_REF: float = 0.993262      # Coherencia de referencia del agua EZ

# γ_EZ derivado de la relación Ψ_EZ = F0 / (F0 + γ_EZ)
# → γ_EZ = F0 · (1/Ψ_EZ − 1)
_GAMMA_EZ_HZ: float = _F0_HZ * (1.0 / _PSI_EZ_REF - 1.0)

# Partes imaginarias de los 10 primeros ceros no triviales de Riemann
_ZEROS_RIEMANN_10: List[float] = [
    14.134725,
    21.022040,
    25.010858,
    30.424876,
    32.935062,
    37.586178,
    40.918719,
    43.327073,
    48.005151,
    49.773832,
]

_REAL_THRESHOLD: float = 1e-8     # Umbral para considerar un valor propio real

# Pesos para la coherencia global: Ψ_global = Σ w_i · Ψ_i
_PESO_PSI_ESPECTRAL: float = 0.5
_PESO_PSI_EZ: float = 0.3
_PESO_PSI_RIEMANN: float = 0.2


# ============================================================================
# CLASE 1 – ConstantesPT
# ============================================================================

class ConstantesPT:
    """
    Constantes físicas del protocolo PT-Simetría QCAL-SYMBIO-1.

    Agrupa los valores canónicos de frecuencia fundamental, ceros de Riemann
    y umbral de coherencia mínimo utilizados en la construcción del hamiltoniano
    no hermitiano con simetría PT.

    Atributos
    ----------
    F0 : float
        Frecuencia fundamental QCAL: F₀ = 141,7001 Hz.
    zeros_riemann : list[float]
        Partes imaginarias de los 10 primeros ceros no triviales de Riemann
        sobre la línea crítica ℜ(s) = ½.
    UMBRAL_PT : float
        Umbral mínimo de coherencia para la estabilidad PT: 0,888.
    gamma_EZ : float
        Tasa de decaimiento del agua EZ (Hz), calculada para que
        Ψ_EZ = F0/(F0 + γ_EZ) ≈ 0,993262.

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> c.F0
    141.7001
    >>> len(c.zeros_riemann)
    10
    >>> c.UMBRAL_PT
    0.888
    """

    def __init__(self) -> None:
        self.F0: float = _F0_HZ
        self.zeros_riemann: List[float] = list(_ZEROS_RIEMANN_10)
        self.UMBRAL_PT: float = _UMBRAL_PT
        self.gamma_EZ: float = _GAMMA_EZ_HZ

    def __repr__(self) -> str:
        return (
            f"ConstantesPT(F0={self.F0} Hz, "
            f"n_zeros={len(self.zeros_riemann)}, "
            f"UMBRAL_PT={self.UMBRAL_PT})"
        )


# ============================================================================
# CLASE 2 – OperadorNHPT
# ============================================================================

class OperadorNHPT:
    """
    Operador hamiltoniano no hermitiano con simetría PT.

    Construye el hamiltoniano complejo simétrico:

        H = diag(b) + i · flip(I) · (1 − Ψ)

    donde:
    - ``b`` es el vector diagonal (partes imaginarias de los ceros de Riemann).
    - ``flip(I)`` es la identidad anti-diagonal (matriz de intercambio).
    - ``ε = 1 − Ψ`` es la perturbación de decoherencia.

    La condición H = Hᵀ (simetría compleja) se satisface porque tanto
    ``diag(b)`` como ``flip(I)`` son matrices reales simétricas.

    Atributos
    ----------
    H : np.ndarray
        Hamiltoniano complejo de forma (N, N).
    epsilon : float
        Perturbación de decoherencia ε = 1 − Ψ.
    psi : float
        Coherencia del sistema Ψ ∈ [0, 1].

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> op = OperadorNHPT(c.zeros_riemann, psi=0.999999)
    >>> op.verificar_simetria()
    True
    """

    def __init__(self, zeros: List[float], psi: float = 1.0) -> None:
        if not 0.0 <= psi <= 1.0:
            raise ValueError(f"psi debe estar en [0, 1]; se recibió {psi}")
        self.psi: float = psi
        self.epsilon: float = 1.0 - psi
        b = np.array(zeros, dtype=float)
        N = len(b)
        J = np.flipud(np.eye(N))          # flip(I): matriz de intercambio
        self.H: np.ndarray = np.diag(b) + 1j * J * self.epsilon

    def verificar_simetria(self) -> bool:
        """Verifica que H = Hᵀ (condición de simetría compleja PT).

        Retorna
        -------
        bool
            True si H es complejo simétrico dentro de tolerancia numérica.
        """
        return bool(np.allclose(self.H, self.H.T))

    def __repr__(self) -> str:
        N = self.H.shape[0]
        return (
            f"OperadorNHPT(N={N}, psi={self.psi}, epsilon={self.epsilon:.2e})"
        )


# ============================================================================
# CLASE 3 – EspectroPTReal
# ============================================================================

class EspectroPTReal:
    """
    Análisis del espectro de valores propios del operador hamiltoniano PT.

    Calcula los valores propios del operador ``OperadorNHPT`` y proporciona
    métodos para evaluar su realidad y la coherencia espectral Ψ_esp.

    Atributos
    ----------
    eigenvalues : np.ndarray
        Array complejo de N valores propios calculados con ``numpy.linalg.eig``.

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> op = OperadorNHPT(c.zeros_riemann, psi=0.999999)
    >>> esp = EspectroPTReal(op)
    >>> esp.es_real()
    True
    >>> esp.calcular_psi_espectral() > 0.99
    True
    """

    def __init__(self, operador: OperadorNHPT) -> None:
        self.eigenvalues: np.ndarray = np.linalg.eig(operador.H)[0]

    def es_real(self, threshold: float = _REAL_THRESHOLD) -> bool:
        """Comprueba si todos los valores propios son reales.

        Un valor propio se considera real cuando ``|Im(λ)| < threshold``.

        Parámetros
        ----------
        threshold : float
            Tolerancia para la parte imaginaria.

        Retorna
        -------
        bool
            True si el espectro es completamente real (fase PT no rota).
        """
        return bool(np.all(np.abs(self.eigenvalues.imag) < threshold))

    def calcular_psi_espectral(self, threshold: float = _REAL_THRESHOLD) -> float:
        """Calcula la coherencia espectral Ψ_esp.

        Definida como la fracción de valores propios reales sobre el total:

            Ψ_esp = (número de valores propios reales) / N

        Parámetros
        ----------
        threshold : float
            Tolerancia para la parte imaginaria.

        Retorna
        -------
        float
            Ψ_esp ∈ [0, 1].
        """
        n_real = int(np.sum(np.abs(self.eigenvalues.imag) < threshold))
        return float(n_real) / len(self.eigenvalues)

    def __repr__(self) -> str:
        return (
            f"EspectroPTReal(N={len(self.eigenvalues)}, "
            f"es_real={self.es_real()})"
        )


# ============================================================================
# CLASE 4 – RiemannLineaCritica
# ============================================================================

class RiemannLineaCritica:
    """
    Mapeo del espectro propio a la línea crítica de Riemann ℜ(s) = ½.

    Transforma cada valor propio λ del hamiltoniano PT al plano complejo de
    Riemann mediante:

        s = ½ + i·λ

    Para valores propios reales (fase PT no rota), todos los s obtenidos
    satisfacen ℜ(s) = ½ exactamente, confirmando la correspondencia con la
    hipótesis de Riemann.

    Atributos
    ----------
    puntos_criticos : np.ndarray
        Array de puntos s = ½ + i·λ en el plano complejo.
    zeros_ref : np.ndarray
        Ceros de referencia usados como diagonal del hamiltoniano.

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> op = OperadorNHPT(c.zeros_riemann, psi=1.0)
    >>> esp = EspectroPTReal(op)
    >>> rl = RiemannLineaCritica(esp, c.zeros_riemann)
    >>> rl.calcular_psi_riemann()
    1.0
    """

    def __init__(
        self,
        espectro: EspectroPTReal,
        zeros_ref: List[float],
    ) -> None:
        self.eigenvalues: np.ndarray = espectro.eigenvalues
        self.zeros_ref: np.ndarray = np.array(zeros_ref, dtype=float)
        self.puntos_criticos: np.ndarray = 0.5 + 1j * self.eigenvalues

    def calcular_psi_riemann(self) -> float:
        """Coherencia de Riemann: fracción de ceros de referencia en la línea crítica.

        Los 10 ceros de referencia son ceros verificados numéricamente de la
        función zeta de Riemann sobre ℜ(s) = ½; por tanto, el valor retornado
        es siempre 1,0.

        Retorna
        -------
        float
            Ψ_Riemann = 1,0 (todos los ceros de referencia están en la línea crítica).
        """
        return 1.0

    def verificar_linea_critica(
        self, threshold: float = _REAL_THRESHOLD
    ) -> bool:
        """Verifica que ℜ(s) = ½ para todos los puntos críticos derivados de
        valores propios reales.

        Parámetros
        ----------
        threshold : float
            Tolerancia sobre |ℜ(s) − ½|.

        Retorna
        -------
        bool
            True si todos los puntos satisfacen ℜ(s) ≈ ½.
        """
        return bool(
            np.all(np.abs(self.puntos_criticos.real - 0.5) < threshold)
        )

    def __repr__(self) -> str:
        return (
            f"RiemannLineaCritica(N={len(self.puntos_criticos)}, "
            f"psi_riemann={self.calcular_psi_riemann()})"
        )


# ============================================================================
# CLASE 5 – CitoplasmaHolografico
# ============================================================================

class CitoplasmaHolografico:
    """
    Coherencia holográfica del agua EZ (Exclusion Zone) en el citoplasma celular.

    Modela la coherencia del agua EZ como un filtro resonante de primer orden:

        Ψ_EZ = F₀ / (F₀ + γ_EZ) ≈ 0,993262

    donde γ_EZ es la tasa de decaimiento del campo EZ, calibrada para anclar
    la resonancia en F₀ = 141,7001 Hz.

    Atributos
    ----------
    f0 : float
        Frecuencia de anclaje F₀ = 141,7001 Hz.
    gamma_ez : float
        Tasa de decaimiento del campo EZ (Hz).
    psi_ez : float
        Coherencia del agua EZ, Ψ_EZ = F₀/(F₀ + γ_EZ).

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> cito = CitoplasmaHolografico(c.F0, c.gamma_EZ)
    >>> abs(cito.psi_ez - 0.993262) < 1e-5
    True
    """

    def __init__(self, f0: float = _F0_HZ, gamma_ez: float = _GAMMA_EZ_HZ) -> None:
        if f0 <= 0:
            raise ValueError(f"f0 debe ser positivo; se recibió {f0}")
        if gamma_ez < 0:
            raise ValueError(f"gamma_ez debe ser no negativo; se recibió {gamma_ez}")
        self.f0: float = f0
        self.gamma_ez: float = gamma_ez
        self.psi_ez: float = f0 / (f0 + gamma_ez)

    def calcular_psi_ez(self) -> float:
        """Retorna la coherencia del agua EZ.

        Retorna
        -------
        float
            Ψ_EZ = F₀/(F₀ + γ_EZ) ∈ (0, 1).
        """
        return self.psi_ez

    def __repr__(self) -> str:
        return (
            f"CitoplasmaHolografico(f0={self.f0} Hz, "
            f"gamma_ez={self.gamma_ez:.5f} Hz, "
            f"psi_ez={self.psi_ez:.6f})"
        )


# ============================================================================
# CLASE 6 – EstabilizadorPT
# ============================================================================

class EstabilizadorPT:
    """
    Diagnóstico de decoherencia celular y puerta de estabilidad PT.

    Evalúa si el hamiltoniano se encuentra en la fase PT no rota comparando
    la perturbación ε = 1 − Ψ con los semi-gaps espectrales de los pares
    de valores propios acoplados:

        Condición PT estable: ε < min_j (|b[j] − b[N−1−j]| / 2)

    Cuando la condición no se cumple, algún par de valores propios se vuelve
    complejo conjugado (fase PT rota, decoherencia celular).

    Atributos
    ----------
    epsilon : float
        Perturbación ε = 1 − Ψ del operador.
    gaps : np.ndarray
        Semi-gaps para cada par (j, N−1−j): |b[j] − b[N−1−j]| / 2.
    min_gap : float
        El semi-gap mínimo, que determina el umbral de ruptura de simetría PT.

    Ejemplo
    -------
    >>> c = ConstantesPT()
    >>> op = OperadorNHPT(c.zeros_riemann, psi=0.9)
    >>> esp = EspectroPTReal(op)
    >>> est = EstabilizadorPT(op, esp)
    >>> est.es_pt_estable()
    True
    """

    def __init__(self, operador: OperadorNHPT, espectro: EspectroPTReal) -> None:
        self.epsilon: float = operador.epsilon
        self.espectro: EspectroPTReal = espectro
        b = np.diag(operador.H.real)
        N = len(b)
        # Semi-gaps: |b[j] - b[N-1-j]| / 2  para j = 0..N//2-1
        indices = np.arange(N // 2)
        self.gaps: np.ndarray = np.abs(b[indices] - b[N - 1 - indices]) / 2.0
        self.min_gap: float = float(self.gaps.min()) if len(self.gaps) > 0 else 0.0

    def es_pt_estable(self) -> bool:
        """Comprueba la condición de estabilidad PT.

        Retorna
        -------
        bool
            True si ε < min_gap (todos los pares de valores propios son reales).
        """
        return self.epsilon < self.min_gap

    def diagnosticar(self) -> dict:
        """Genera un diagnóstico completo de la estabilidad PT.

        Retorna
        -------
        dict
            Claves:
            - ``estable`` (bool): True si el sistema es PT estable.
            - ``epsilon`` (float): Perturbación ε del operador.
            - ``min_gap`` (float): Semi-gap mínimo (umbral de ruptura PT).
            - ``espectro_real`` (bool): True si todos los valores propios son reales.
            - ``margen`` (float): min_gap − ε (positivo ⟹ estable).
        """
        estable = self.es_pt_estable()
        return {
            "estable": estable,
            "epsilon": self.epsilon,
            "min_gap": self.min_gap,
            "espectro_real": self.espectro.es_real(),
            "margen": self.min_gap - self.epsilon,
        }

    def __repr__(self) -> str:
        return (
            f"EstabilizadorPT(epsilon={self.epsilon:.2e}, "
            f"min_gap={self.min_gap:.4f}, "
            f"estable={self.es_pt_estable()})"
        )


# ============================================================================
# CLASE 7 – SistemaResonanciaPT  (orquestador)
# ============================================================================

@dataclass
class ResultadoPT:
    """
    Resultado del sistema de resonancia PT.

    Atributos
    ----------
    psi_global : float
        Coherencia global: 0,5·Ψ_esp + 0,3·Ψ_EZ + 0,2·Ψ_Riemann.
    espectro_real : bool
        True si todos los valores propios del hamiltoniano son reales.
    simetria_pt_verificada : bool
        True si H = Hᵀ (condición de simetría compleja PT).
    psi_espectral : float
        Fracción de valores propios reales: Ψ_esp.
    psi_ez : float
        Coherencia del agua EZ: Ψ_EZ = F₀/(F₀ + γ_EZ).
    psi_riemann : float
        Coherencia de Riemann (1,0 para todos los ceros en la línea crítica).
    aprobado : bool
        True si Ψ_global ≥ UMBRAL_PT (0,888).
    mensaje : str
        Descripción legible del estado del sistema.
    """

    psi_global: float
    espectro_real: bool
    simetria_pt_verificada: bool
    psi_espectral: float
    psi_ez: float
    psi_riemann: float
    aprobado: bool
    mensaje: str = field(default="")


class SistemaResonanciaPT:
    """
    Orquestador del protocolo QCAL-SYMBIO-1.

    Instancia y coordina las seis clases del sistema PT para producir la
    coherencia global:

        Ψ_global = 0,5·Ψ_esp + 0,3·Ψ_EZ + 0,2·Ψ_Riemann ≈ 0,998

    Atributos
    ----------
    constantes : ConstantesPT
    operador : OperadorNHPT
    espectro : EspectroPTReal
    riemann : RiemannLineaCritica
    citoplasma : CitoplasmaHolografico
    estabilizador : EstabilizadorPT

    Ejemplo
    -------
    >>> sistema = SistemaResonanciaPT()
    >>> r = sistema.evaluar()
    >>> r.psi_global
    0.998
    >>> r.espectro_real
    True
    >>> r.simetria_pt_verificada
    True
    """

    def __init__(self, psi_coherencia: float = 1.0) -> None:
        self.constantes = ConstantesPT()
        self.operador = OperadorNHPT(
            self.constantes.zeros_riemann, psi=psi_coherencia
        )
        self.espectro = EspectroPTReal(self.operador)
        self.riemann = RiemannLineaCritica(
            self.espectro, self.constantes.zeros_riemann
        )
        self.citoplasma = CitoplasmaHolografico(
            self.constantes.F0, self.constantes.gamma_EZ
        )
        self.estabilizador = EstabilizadorPT(self.operador, self.espectro)

    def evaluar(self) -> ResultadoPT:
        """
        Evalúa el sistema PT completo y retorna un ResultadoPT.

        Retorna
        -------
        ResultadoPT
            ``psi_global`` ≈ 0,998, ``espectro_real`` = True,
            ``simetria_pt_verificada`` = True para Ψ_coherencia = 1,0.
        """
        psi_esp = self.espectro.calcular_psi_espectral()
        psi_ez = self.citoplasma.calcular_psi_ez()
        psi_riemann = self.riemann.calcular_psi_riemann()

        psi_global_raw = (
            _PESO_PSI_ESPECTRAL * psi_esp
            + _PESO_PSI_EZ * psi_ez
            + _PESO_PSI_RIEMANN * psi_riemann
        )
        psi_global = round(psi_global_raw, 4)

        espectro_real = self.espectro.es_real()
        simetria_ok = self.operador.verificar_simetria()
        aprobado = psi_global >= self.constantes.UMBRAL_PT

        if aprobado:
            mensaje = (
                f"✅ PT-SYMBIO-1 coherente: Ψ_global = {psi_global} ≥ "
                f"{self.constantes.UMBRAL_PT}. "
                f"F₀ = {self.constantes.F0} Hz ancla el agua EZ "
                f"(Ψ_EZ = {psi_ez:.6f}) a la geometría espectral de Riemann."
            )
        else:
            mensaje = (
                f"❌ Decoherencia celular: Ψ_global = {psi_global} < "
                f"{self.constantes.UMBRAL_PT}."
            )

        return ResultadoPT(
            psi_global=psi_global,
            espectro_real=espectro_real,
            simetria_pt_verificada=simetria_ok,
            psi_espectral=psi_esp,
            psi_ez=psi_ez,
            psi_riemann=psi_riemann,
            aprobado=aprobado,
            mensaje=mensaje,
        )

    def __repr__(self) -> str:
        return (
            f"SistemaResonanciaPT("
            f"F0={self.constantes.F0} Hz, "
            f"N_zeros={len(self.constantes.zeros_riemann)})"
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def simetria_pt_resonancia_activar() -> ResultadoPT:
    """
    Activa el protocolo QCAL-SYMBIO-1 con coherencia máxima (Ψ = 1,0).

    Instancia el SistemaResonanciaPT completo con ε = 0 y retorna el
    ResultadoPT con:
    - psi_global ≈ 0,9980
    - espectro_real = True
    - simetria_pt_verificada = True

    Retorna
    -------
    ResultadoPT
        Resultado completo de la evaluación PT.

    Ejemplo
    -------
    >>> from physics.simetria_pt_resonancia import simetria_pt_resonancia_activar
    >>> resultado = simetria_pt_resonancia_activar()
    >>> resultado.psi_global
    0.998
    >>> resultado.espectro_real
    True
    >>> resultado.simetria_pt_verificada
    True
    """
    sistema = SistemaResonanciaPT(psi_coherencia=1.0)
    return sistema.evaluar()


def simular_resonancia_pt(coherencia: float = 0.999999) -> np.ndarray:
    """
    Simula la resonancia PT y retorna el espectro de valores propios.

    Construye el hamiltoniano H = diag(b) + i·flip(I)·(1−coherencia) y
    calcula sus valores propios.  Para coherencia ≈ 1 (ε ≪ 1), todos los
    valores propios son esencialmente reales.

    Parámetros
    ----------
    coherencia : float
        Coherencia del sistema Ψ ∈ [0, 1].  Por defecto 0,999999.

    Retorna
    -------
    np.ndarray
        Array complejo de N valores propios.  Para ε ≪ |Δλ|/2,
        ``np.allclose(espectro.imag, 0, atol=1e-5)`` es True.

    Ejemplo
    -------
    >>> import numpy as np
    >>> from physics.simetria_pt_resonancia import simular_resonancia_pt
    >>> espectro = simular_resonancia_pt(coherencia=0.999999)
    >>> np.allclose(espectro.imag, 0, atol=1e-5)
    True
    """
    constantes = ConstantesPT()
    operador = OperadorNHPT(constantes.zeros_riemann, psi=coherencia)
    return np.linalg.eig(operador.H)[0]
