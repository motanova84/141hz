"""
Simetría PT – Motor de Resonancia de Riemann (Protocolo QCAL-SYMBIO-1).

Simulates how a non-Hermitian open system sustains real Riemann-zero spectra
via PT (Parity-Time) symmetry.  When [Ĥ, PT] = 0, the spectrum remains real,
acting as a phase anchor for cellular EZ-water coherence.

The operator is constructed as:
    Ĥ = diag(base_riemann) + i · (1 − Ψ) · fliplr(I_N)

As coherence Ψ → 1 the imaginary (dissipative) coupling vanishes and all
eigenvalues collapse to the real axis, emulating the Riemann critical line.

Classes:
    ResultadoResonanciaPT -- result dataclass for QCAL-SYMBIO-1 protocol
    BaseRiemann           -- spectral proxy for Riemann zeros
    OperadorPT            -- non-Hermitian PT Hamiltonian
    EspectroEigenvalores  -- eigenvalue spectrum analysis
    MotorResonanciaPT     -- integration engine

Public API:
    simular_resonancia_pt(n_dimension, coherencia, *, semilla) -> ndarray
    activar_protocolo_qcal_symbio_1(n_dimension, coherencia, *, semilla) -> ResultadoResonanciaPT
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import numpy.typing as npt


# ============================================================================
# CONSTANTES
# ============================================================================

_PSI_COHERENCIA_UMBRAL: float = 0.888   # Umbral mínimo de coherencia biológica
_ATOL_ESTABILIDAD: float = 1e-5         # Tolerancia para autovalores reales
_N_DIMENSION_DEFAULT: int = 100         # Dimensión por defecto del operador
_COHERENCIA_DEFAULT: float = 0.999999   # Coherencia por defecto (Ψ → 1)


# ============================================================================
# DATACLASS DE RESULTADO
# ============================================================================

@dataclass
class ResultadoResonanciaPT:
    """
    Resultado del protocolo QCAL-SYMBIO-1 de simetría PT.

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ utilizado en la simulación.
    n_dimension : int
        Dimensión del espacio de Hilbert simulado.
    autovalores : npt.NDArray[np.complexfloating]
        Array de autovalores complejos del operador Ĥ_total.
    estable : bool
        True si todos los autovalores tienen parte imaginaria ≈ 0
        (|Im(λ)| < atol), indicando estabilidad PT.
    media_imaginaria : float
        Media de |Im(autovalores)|; idealmente 0.0 bajo PT perfecta.
    max_imaginario : float
        Máximo de |Im(autovalores)|; idealmente 0.0 bajo PT perfecta.
    """

    coherencia: float
    n_dimension: int
    autovalores: npt.NDArray[np.complexfloating]
    estable: bool
    media_imaginaria: float
    max_imaginario: float

    def resumen(self) -> str:
        """Cadena de texto con los indicadores clave del resultado."""
        bio_ok = self.coherencia >= _PSI_COHERENCIA_UMBRAL
        return (
            f"Coherencia del Sistema: Ψ = {self.coherencia}\n"
            f"Umbral biológico (Ψ ≥ {_PSI_COHERENCIA_UMBRAL}): {bio_ok}\n"
            f"Dimensión del operador: N = {self.n_dimension}\n"
            f"Estabilidad PT: {self.estable}\n"
            f"Parte imaginaria media: {self.media_imaginaria:.6e}\n"
            f"Parte imaginaria máx:   {self.max_imaginario:.6e}"
        )


# ============================================================================
# CLASE 1 – BaseRiemann
# ============================================================================

class BaseRiemann:
    """
    Proxy espectral de los ceros de Riemann.

    Genera una base de valores reales ordenados que aproximan la distribución
    espectral de los ceros no triviales de la función ζ de Riemann.  En un
    sistema real, estos corresponderían a los modos de vibración de la cuerda
    EZ del citoplasma.

    Atributos
    ----------
    n : int
        Número de modos espectrales.
    valores : npt.NDArray[np.float64]
        Array de n valores ordenados de menor a mayor.
    """

    def __init__(self, n: int, semilla: Optional[int] = None) -> None:
        if n < 1:
            raise ValueError(f"n debe ser >= 1, se recibió {n}")
        self.n = n
        rng = np.random.default_rng(semilla)
        self.valores: npt.NDArray[np.float64] = np.sort(
            rng.standard_normal(n).astype(np.float64)
        )

    def como_diagonal(self) -> npt.NDArray[np.float64]:
        """Devuelve los valores como matriz diagonal N×N."""
        return np.diag(self.valores)


# ============================================================================
# CLASE 2 – OperadorPT
# ============================================================================

class OperadorPT:
    """
    Hamiltoniano no-hermítico con simetría PT (Paridad–Tiempo).

    El operador se construye como:
        Ĥ = H_real + i · H_disipativo

    donde:
        H_real       = diag(base_riemann)          (parte hermítica)
        H_disipativo = (1 − Ψ) · voltear(I_N)     (acoplamiento disipativo)

    Cuando Ψ → 1 la parte imaginaria se suprime completamente, los
    autovalores colapsan a la línea real y el sistema alcanza la
    coherencia PT completa.

    Atributos
    ----------
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    n : int
        Dimensión del espacio de Hilbert.
    """

    def __init__(self, base: BaseRiemann, coherencia: float) -> None:
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        self.coherencia: float = coherencia
        self.n: int = base.n
        self._base = base

    def construir(self) -> npt.NDArray[np.complexfloating]:
        """
        Construye y devuelve la matriz compleja Ĥ_total (N×N).

        Returns
        -------
        npt.NDArray[np.complexfloating]
            Operador no-hermítico con simetría PT.
        """
        h_real = self._base.como_diagonal()
        h_imaginario = np.fliplr(np.eye(self.n)) * (1.0 - self.coherencia)
        return h_real + 1j * h_imaginario


# ============================================================================
# CLASE 3 – EspectroEigenvalores
# ============================================================================

class EspectroEigenvalores:
    """
    Calcula y analiza el espectro de autovalores de un operador.

    Atributos
    ----------
    autovalores : npt.NDArray[np.complexfloating]
        Array de autovalores complejos calculados.
    """

    def __init__(self, operador: npt.NDArray[np.complexfloating]) -> None:
        self.autovalores: npt.NDArray[np.complexfloating] = np.linalg.eigvals(operador)

    def es_estable(self, atol: float = _ATOL_ESTABILIDAD) -> bool:
        """
        True si todos los autovalores tienen parte imaginaria ≈ 0.

        Parámetros
        ----------
        atol : float
            Tolerancia absoluta para considerar la parte imaginaria nula.
        """
        return bool(np.allclose(self.autovalores.imag, 0.0, atol=atol))

    def media_imaginaria(self) -> float:
        """Media de |Im(autovalores)|."""
        return float(np.mean(np.abs(self.autovalores.imag)))

    def max_imaginario(self) -> float:
        """Máximo de |Im(autovalores)|."""
        return float(np.max(np.abs(self.autovalores.imag)))


# ============================================================================
# CLASE 4 – MotorResonanciaPT
# ============================================================================

class MotorResonanciaPT:
    """
    Motor integrador del protocolo QCAL-SYMBIO-1.

    Orquesta la construcción del operador PT y el análisis espectral para
    producir un ResultadoResonanciaPT completo.

    Parámetros
    ----------
    n_dimension : int
        Dimensión del espacio de Hilbert (número de modos espectrales).
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].
    semilla : int | None
        Semilla para el generador de números aleatorios (reproducibilidad).
    """

    def __init__(
        self,
        n_dimension: int = _N_DIMENSION_DEFAULT,
        coherencia: float = _COHERENCIA_DEFAULT,
        semilla: Optional[int] = None,
    ) -> None:
        if n_dimension < 1:
            raise ValueError(f"n_dimension debe ser >= 1, se recibió {n_dimension}")
        if not (0.0 < coherencia <= 1.0):
            raise ValueError(
                f"coherencia debe estar en (0, 1], se recibió {coherencia}"
            )
        self.n_dimension = n_dimension
        self.coherencia = coherencia
        self.semilla = semilla

    def ejecutar(self) -> ResultadoResonanciaPT:
        """
        Ejecuta el protocolo y devuelve el resultado.

        Returns
        -------
        ResultadoResonanciaPT
            Resultado completo incluyendo autovalores y métricas de estabilidad.
        """
        base = BaseRiemann(self.n_dimension, semilla=self.semilla)
        operador = OperadorPT(base, self.coherencia)
        h_total = operador.construir()
        espectro = EspectroEigenvalores(h_total)

        return ResultadoResonanciaPT(
            coherencia=self.coherencia,
            n_dimension=self.n_dimension,
            autovalores=espectro.autovalores,
            estable=espectro.es_estable(),
            media_imaginaria=espectro.media_imaginaria(),
            max_imaginario=espectro.max_imaginario(),
        )


# ============================================================================
# API PÚBLICA
# ============================================================================

def simular_resonancia_pt(
    n_dimension: int = _N_DIMENSION_DEFAULT,
    coherencia: float = _COHERENCIA_DEFAULT,
    *,
    semilla: Optional[int] = None,
) -> npt.NDArray[np.complexfloating]:
    """
    Simula la estabilidad de un operador no-hermítico bajo simetría PT.

    Representa el citoplasma como un borde holográfico donde la información
    de Riemann se vuelve real.  Al alcanzar la coherencia Ψ → 1.0 los
    autovalores "colapsan" hacia la línea crítica, transformando el ruido
    en geometría.

    Parámetros
    ----------
    n_dimension : int
        Dimensión del espacio de Hilbert simulado (modos espectrales).
        Debe ser >= 1.  Por defecto 100.
    coherencia : float
        Parámetro de coherencia Ψ ∈ (0, 1].  Por defecto 0.999999.
    semilla : int | None
        Semilla opcional para la reproducibilidad del generador aleatorio.

    Returns
    -------
    npt.NDArray[np.complexfloating]
        Array de autovalores complejos del operador PT.
        Cuando coherencia ≈ 1.0 las partes imaginarias son ≈ 0.

    Raises
    ------
    ValueError
        Si n_dimension < 1 o coherencia ∉ (0, 1].
    """
    motor = MotorResonanciaPT(n_dimension=n_dimension, coherencia=coherencia, semilla=semilla)
    resultado = motor.ejecutar()
    return resultado.autovalores


def activar_protocolo_qcal_symbio_1(
    n_dimension: int = _N_DIMENSION_DEFAULT,
    coherencia: float = _COHERENCIA_DEFAULT,
    *,
    semilla: Optional[int] = None,
) -> ResultadoResonanciaPT:
    """
    Ejecuta el protocolo QCAL-SYMBIO-1 completo.

    Parámetros
    ----------
    n_dimension : int
        Dimensión del espacio de Hilbert.  Por defecto 100.
    coherencia : float
        Coherencia Ψ ∈ (0, 1].  Por defecto 0.999999.
    semilla : int | None
        Semilla para reproducibilidad.

    Returns
    -------
    ResultadoResonanciaPT
        Resultado con autovalores, estabilidad PT y métricas espectrales.
    """
    motor = MotorResonanciaPT(n_dimension=n_dimension, coherencia=coherencia, semilla=semilla)
    return motor.ejecutar()


# ============================================================================
# EJECUCIÓN DIRECTA – Protocolo QCAL-SYMBIO-1
# ============================================================================

if __name__ == "__main__":  # pragma: no cover
    import sys

    resultado = activar_protocolo_qcal_symbio_1()
    print(resultado.resumen())

    # Visualización del espectro PT (opcional, requiere matplotlib)
    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(resultado.autovalores.real, resultado.autovalores.imag, s=10, alpha=0.7)
        ax.axhline(0, color="r", linewidth=0.8, label="Im = 0 (línea crítica)")
        ax.set_xlabel("Real")
        ax.set_ylabel("Im")
        ax.set_title("Espectro PT – Protocolo QCAL-SYMBIO-1")
        ax.legend()
        fig.tight_layout()
        fig.savefig("espectro_pt.png", dpi=150)
        print("Espectro guardado en espectro_pt.png")
        plt.close(fig)
    except ImportError:
        print("matplotlib no disponible; omitiendo visualización.", file=sys.stderr)
