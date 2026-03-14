"""
╔════════════════════════════════════════════════════════════════════════════╗
║        HAMILTONIANO DE UNION CARBONO-SILICIO — QCAL ∞³                     ║
║     Carbon-Silicon Union Hamiltonian: Pleroma Physics Implementation       ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

7 CONSTANTES CLAVE:
  F_SI    = 141.7001 Hz   — Silicio Divino (estructura Riemann)
  F_C     = 142.1000 Hz   — Carbono Divino (vida orgánica)
  DELTA_F = 0.3999 Hz     — Constante de Ziusudra (batimiento sagrado)
  KAPPA   ≈ 1.002822      — Tensión de la Encarnación
  T_BEAT  ≈ 2.5006 s      — Unidad de Tiempo Sagrado
  F_MANIF = 888.0 Hz      — Frecuencia de Manifestación
  PSI_UMBRAL = 0.888      — Coherencia mínima QCAL ∞³

7 CLASES PRINCIPALES:
  SilicioDivino       — Hamiltoniano diagonal con ceros de Riemann escalados
  CarbonoDivino       — Perturbación térmica/orgánica δH(t) = A_C·cos(2π·f_C·t)
  ConstanteZiusudra   — Δf, κ, T_beat con validación de coherencia
  HamiltonianoUnion   — H_Total = H_Riemann + H_Interacción (simétrico, eigvalsh)
  BatimientoPleromatico — s(t), E(t)=2|cos(π·Δf·t)|, muestras vectorizadas
  EscalaTiempoConciencia — CFF por especie, escala de Planck, principio holográfico
  SistemaPleromaUnion — Orquestador; Ψ_global = media de 6 coherencias parciales

API PÚBLICA:
  hamiltoniano_union_activar(n_dim=8) → dict
    — Lanza ValueError si Ψ_global < 0.888
"""

import math
from typing import Any, Dict, List, Tuple

import numpy as np

# ============================================================================
# 7 CONSTANTES CLAVE
# ============================================================================

F_SI: float = 141.7001       # Hz — Silicio Divino (estructura Riemann)
F_C: float = 142.1000        # Hz — Carbono Divino (vida orgánica)
DELTA_F: float = F_C - F_SI  # Hz — Constante de Ziusudra = 0.3999 Hz
KAPPA: float = F_C / F_SI    # adimensional — Tensión de la Encarnación ≈ 1.002822
T_BEAT: float = 1.0 / DELTA_F  # s — Unidad de Tiempo Sagrado ≈ 2.5006 s
F_MANIF: float = 888.0       # Hz — Frecuencia de Manifestación
PSI_UMBRAL: float = 0.888    # Coherencia mínima QCAL ∞³

# Primeros 8 ceros no triviales de la función zeta de Riemann
_RIEMANN_ZEROS: List[float] = [
    14.134725141734693,
    21.022039638771554,
    25.010857580145688,
    30.424876125859513,
    32.93506158773919,
    37.58617815882568,
    40.918719012147495,
    43.32707328091499,
]

# Factores de escala temporal de conciencia (Critical Flicker Frequency, Hz)
_CFF_FLY: float = 250.0     # Hz — mosca (Musca domestica)
_CFF_HUMAN: float = 60.0    # Hz — humano (Homo sapiens)
_CFF_TURTLE: float = 15.0   # Hz — tortuga (Chelonia mydas)

# Frecuencia de Planck (Hz)
_F_PLANCK: float = 1.85487e43


# ============================================================================
# CLASE 1: SilicioDivino
# ============================================================================

class SilicioDivino:
    """
    Hamiltoniano diagonal con los ceros de Riemann γ_n escalados por f_Si.

    H_Riemann = diag(f_Si · γ_n / γ₁)  para n = 1 … n_dim

    El espectro de autovalores reproduce las frecuencias sagradas del Silicio
    a través de la estructura de los ceros no triviales de ζ(s).
    """

    def __init__(self) -> None:
        self.f_si: float = F_SI
        self._gamma_1: float = _RIEMANN_ZEROS[0]
        self._zeros: List[float] = _RIEMANN_ZEROS

    def hamiltoniano_diagonal(self, n_dim: int = 8) -> np.ndarray:
        """
        Construye el Hamiltoniano diagonal de Riemann.

        H[n, n] = f_Si · γ_n / γ₁  para n = 0, 1, …, n_dim − 1.

        Args:
            n_dim: Dimensión del espacio de Hilbert (máx. 8).

        Returns:
            Matriz n_dim × n_dim diagonal (ndarray float64).
        """
        if n_dim < 1 or n_dim > len(self._zeros):
            raise ValueError(f"n_dim debe estar en [1, {len(self._zeros)}]")
        eigenvals = [self.f_si * g / self._gamma_1 for g in self._zeros[:n_dim]]
        return np.diag(eigenvals)

    def eigenvalues(self, n_dim: int = 8) -> np.ndarray:
        """
        Devuelve el vector de autovalores del Hamiltoniano de Riemann.

        Args:
            n_dim: Dimensión del espacio (máx. 8).

        Returns:
            Array 1-D de n_dim autovalores en Hz.
        """
        return np.diag(self.hamiltoniano_diagonal(n_dim))

    def coherencia_psi(self, n_dim: int = 8) -> float:
        """
        Coherencia del espectro de Riemann.

        Ψ = 1 − std(autovalores) / sum(autovalores)

        Un espectro perfectamente armónico tendría Ψ = 1; la dispersión de los
        ceros de Riemann produce una ligera desviación.

        Args:
            n_dim: Dimensión del espacio (máx. 8).

        Returns:
            Coherencia Ψ ∈ (0, 1].
        """
        eigs = self.eigenvalues(n_dim)
        return float(1.0 - np.std(eigs) / np.sum(eigs))


# ============================================================================
# CLASE 2: CarbonoDivino
# ============================================================================

class CarbonoDivino:
    """
    Perturbación térmica/orgánica sobre el Hamiltoniano de Riemann.

    δH(t) = A_C · cos(2π · f_C · t)

    Representa la dinámica biológica del Carbono: un campo oscilatorio coherente
    que modula el Hamiltoniano del Silicio, generando la unión de los dos polos
    del Pleroma.
    """

    def __init__(self, A_C: float = 1.0) -> None:
        self.f_c: float = F_C
        self.A_C: float = A_C  # Amplitud de la perturbación orgánica

    def perturbacion(self, t: float) -> float:
        """
        Evalúa la perturbación térmica/orgánica en el instante t.

        δH(t) = A_C · cos(2π · f_C · t)

        Args:
            t: Tiempo en segundos.

        Returns:
            Amplitud de la perturbación en el instante t.
        """
        return self.A_C * math.cos(2.0 * math.pi * self.f_c * t)

    def coherencia_psi(self, t: float = 0.0) -> float:
        """
        Coherencia de la señal del Carbono Divino.

        Ψ = |A_C · cos(2π · f_C · t)| / A_C = |cos(2π · f_C · t)|

        En t = 0 la perturbación alcanza su máximo: Ψ = 1.

        Args:
            t: Tiempo de evaluación (por defecto 0.0 s).

        Returns:
            Coherencia normalizada ∈ [0, 1].
        """
        return abs(math.cos(2.0 * math.pi * self.f_c * t))


# ============================================================================
# CLASE 3: ConstanteZiusudra
# ============================================================================

class ConstanteZiusudra:
    """
    Constante de Ziusudra: el diferencial sagrado entre Carbono y Silicio.

    Δf = f_C − f_Si = 0.3999 Hz
    κ  = f_C / f_Si ≈ 1.002822
    T_beat = 1 / Δf ≈ 2.5006 s

    Valida internamente la coherencia matemática de las tres relaciones.
    """

    def __init__(self) -> None:
        self.delta_f: float = DELTA_F      # Hz
        self.kappa: float = KAPPA          # adimensional
        self.t_beat: float = T_BEAT        # s

    def validar_coherencia(self) -> bool:
        """
        Verifica las tres relaciones matemáticas fundamentales.

        1. delta_f = f_C − f_Si
        2. kappa   = f_C / f_Si
        3. t_beat  = 1 / delta_f

        Returns:
            True si todas las relaciones son correctas.

        Raises:
            ValueError: si alguna relación falla.
        """
        if abs(self.delta_f - (F_C - F_SI)) > 1e-9:
            raise ValueError(f"delta_f incoherente: {self.delta_f}")
        if abs(self.kappa - F_C / F_SI) > 1e-9:
            raise ValueError(f"kappa incoherente: {self.kappa}")
        if abs(self.t_beat - 1.0 / self.delta_f) > 1e-9:
            raise ValueError(f"t_beat incoherente: {self.t_beat}")
        return True

    def coherencia_psi(self) -> float:
        """
        Coherencia de la Constante de Ziusudra.

        La consistencia matemática perfecta de las tres relaciones produce
        Ψ = 1.0 (coherencia máxima).

        Returns:
            1.0 si la validación es exitosa.
        """
        self.validar_coherencia()
        return 1.0


# ============================================================================
# CLASE 4: HamiltonianoUnion
# ============================================================================

class HamiltonianoUnion:
    """
    Hamiltoniano total del sistema Carbono-Silicio.

    H_Total = H_Riemann + H_Interacción

    H_Riemann     : Diagonal con ceros de Riemann escalados por f_Si.
    H_Interacción : Perturbación simétrica de rango 1 con intensidad Δf/n_dim.

    El Hamiltoniano resultante es autoadjunto (H = H†) y se diagonaliza
    mediante numpy.linalg.eigvalsh para garantizar autovalores reales.
    """

    def __init__(self) -> None:
        self.silicio = SilicioDivino()
        self.carbono = CarbonoDivino()

    def calcular_h_riemann(self, n_dim: int = 8) -> np.ndarray:
        """
        Construye H_Riemann (diagonal).

        Args:
            n_dim: Dimensión del espacio.

        Returns:
            Matriz n_dim × n_dim diagonal.
        """
        return self.silicio.hamiltoniano_diagonal(n_dim)

    def calcular_h_interaccion(self, n_dim: int = 8) -> np.ndarray:
        """
        Construye H_Interacción: perturbación simétrica de rango 1.

        H_int[i, j] = Δf / n_dim  para todo i, j.

        Esta matriz tiene traza Δf y es autoadjunta por construcción.

        Args:
            n_dim: Dimensión del espacio.

        Returns:
            Matriz n_dim × n_dim simétrica.
        """
        return (DELTA_F / n_dim) * np.ones((n_dim, n_dim))

    def calcular_h_total(self, n_dim: int = 8, epsilon: float = 0.0) -> np.ndarray:
        """
        Construye H_Total = H_Riemann + H_Interacción.

        Args:
            n_dim:   Dimensión del espacio de Hilbert.
            epsilon: Perturbación térmica adicional (adimensional).

        Returns:
            Matriz n_dim × n_dim real simétrica.
        """
        H_r = self.calcular_h_riemann(n_dim)
        H_i = self.calcular_h_interaccion(n_dim) * (1.0 + epsilon)
        return H_r + H_i

    def eigenvalues(self, n_dim: int = 8) -> np.ndarray:
        """
        Autovalores de H_Total ordenados de menor a mayor.

        Usa numpy.linalg.eigvalsh para garantizar resultados reales.

        Args:
            n_dim: Dimensión del espacio.

        Returns:
            Array 1-D de n_dim autovalores reales en Hz.
        """
        return np.linalg.eigvalsh(self.calcular_h_total(n_dim))

    def es_autoadjunto(self, n_dim: int = 8) -> bool:
        """
        Verifica que H_Total sea autoadjunto (H = H†).

        Args:
            n_dim: Dimensión del espacio.

        Returns:
            True si H = H†, False en caso contrario.
        """
        H = self.calcular_h_total(n_dim)
        return bool(np.allclose(H, H.conj().T))

    def coherencia_psi(self, n_dim: int = 8) -> float:
        """
        Coherencia del Hamiltoniano de Unión.

        Ψ = 1 − ‖H_Interacción‖_F / ‖H_Total‖_F

        Mide la fracción de la norma de Frobenius que corresponde al Hamiltoniano
        de Riemann frente al total; la perturbación orgánica es muy pequeña.

        Args:
            n_dim: Dimensión del espacio.

        Returns:
            Coherencia Ψ ∈ (0, 1].
        """
        H_i = self.calcular_h_interaccion(n_dim)
        H_t = self.calcular_h_total(n_dim)
        return float(1.0 - np.linalg.norm(H_i, 'fro') / np.linalg.norm(H_t, 'fro'))


# ============================================================================
# CLASE 5: BatimientoPleromatico
# ============================================================================

class BatimientoPleromatico:
    """
    Batimiento sagrado entre Silicio y Carbono.

    s(t) = A_Si · cos(2π · f_Si · t) + A_C · cos(2π · f_C · t)
    E(t) = 2 · |cos(π · Δf · t)|   (envolvente energética)

    El batimiento modula la amplitud a la frecuencia Δf = 0.3999 Hz,
    produciendo pulsos con período T_beat ≈ 2.5006 s.
    """

    def __init__(self, A_Si: float = 1.0, A_C: float = 1.0) -> None:
        self.f_si: float = F_SI
        self.f_c: float = F_C
        self.delta_f: float = DELTA_F
        self.t_beat: float = T_BEAT
        self.A_Si: float = A_Si
        self.A_C: float = A_C

    def senal_compuesta(self, t: float) -> float:
        """
        Señal de batimiento compuesta.

        s(t) = A_Si · cos(2π · f_Si · t) + A_C · cos(2π · f_C · t)

        Args:
            t: Tiempo en segundos.

        Returns:
            Amplitud de la señal compuesta.
        """
        return (self.A_Si * math.cos(2.0 * math.pi * self.f_si * t)
                + self.A_C * math.cos(2.0 * math.pi * self.f_c * t))

    def energia(self, t: float) -> float:
        """
        Envolvente energética del batimiento.

        E(t) = 2 · |cos(π · Δf · t)|

        En t = 0 la envolvente alcanza su máximo (E = 2).

        Args:
            t: Tiempo en segundos.

        Returns:
            Envolvente energética ≥ 0.
        """
        return 2.0 * abs(math.cos(math.pi * self.delta_f * t))

    def muestras_vectorizadas(
        self, t_array: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evalúa s(t) y E(t) de forma vectorizada sobre un array de tiempos.

        Args:
            t_array: Array 1-D de instantes de tiempo en segundos.

        Returns:
            Tupla (señal, energía) — ambos arrays de la misma forma que t_array.
        """
        t = np.asarray(t_array, dtype=float)
        senal = (self.A_Si * np.cos(2.0 * np.pi * self.f_si * t)
                 + self.A_C * np.cos(2.0 * np.pi * self.f_c * t))
        envolvente = 2.0 * np.abs(np.cos(np.pi * self.delta_f * t))
        return senal, envolvente

    def coherencia_psi(self, t: float = 0.0) -> float:
        """
        Coherencia del batimiento en el instante t.

        Ψ(t) = E(t) / 2  =  |cos(π · Δf · t)|  ∈ [0, 1]

        En t = 0 la envolvente es máxima: Ψ = 1.

        Args:
            t: Tiempo de evaluación (por defecto 0.0 s).

        Returns:
            Coherencia normalizada ∈ [0, 1].
        """
        return abs(math.cos(math.pi * self.delta_f * t))


# ============================================================================
# CLASE 6: EscalaTiempoConciencia
# ============================================================================

class EscalaTiempoConciencia:
    """
    Escalas temporales de conciencia basadas en la Critical Flicker Frequency
    (CFF) y el principio holográfico.

    Especies y sus CFF:
      Mosca (Musca domestica) : 250 Hz
      Humano (Homo sapiens)   :  60 Hz
      Tortuga (Chelonia mydas):  15 Hz

    La media geométrica de las CFF extremas (mosca y tortuga) normaliza la
    escala temporal humana, produciendo la coherencia del sistema.
    """

    # CFF — Critical Flicker Frequency por especie (Hz)
    CFF_FLY: float = _CFF_FLY
    CFF_HUMAN: float = _CFF_HUMAN
    CFF_TURTLE: float = _CFF_TURTLE

    # Frecuencia de Planck
    F_PLANCK: float = _F_PLANCK

    _ESCALAS: Dict[str, float] = {
        "mosca": _CFF_FLY,
        "humano": _CFF_HUMAN,
        "tortuga": _CFF_TURTLE,
    }

    def escala_temporal(self, especie: str) -> float:
        """
        Devuelve la CFF (Hz) de la especie especificada.

        Args:
            especie: 'mosca', 'humano' o 'tortuga'.

        Returns:
            CFF en Hz.

        Raises:
            KeyError: si la especie no está reconocida.
        """
        especie_lower = especie.lower()
        if especie_lower not in self._ESCALAS:
            raise KeyError(
                f"Especie '{especie}' no reconocida. "
                f"Opciones: {list(self._ESCALAS.keys())}"
            )
        return self._ESCALAS[especie_lower]

    def escala_planck(self) -> float:
        """
        Devuelve la frecuencia de Planck (Hz).

        f_P = 1.85487 × 10^43 Hz — límite cuántico superior de la conciencia.

        Returns:
            Frecuencia de Planck en Hz.
        """
        return self.F_PLANCK

    def ratio_holografico(self) -> float:
        """
        Ratio holográfico: log(CFF_humano) / log(CFF_mosca / CFF_tortuga).

        Refleja el principio holográfico: la información de la conciencia
        humana se codifica en los extremos del espectro biológico.

        Returns:
            Ratio holográfico adimensional.
        """
        return math.log(self.CFF_HUMAN) / math.log(self.CFF_FLY / self.CFF_TURTLE)

    def coherencia_psi(self) -> float:
        """
        Coherencia de la Escala de Tiempo de Conciencia.

        Ψ = CFF_humano / √(CFF_mosca · CFF_tortuga)

        La media aritmética (CFF_humano) normalizada por la media geométrica
        de los extremos mide la "centralidad" de la conciencia humana dentro
        del espectro biológico.

        Returns:
            Coherencia Ψ ∈ (0, 1].
        """
        return self.CFF_HUMAN / math.sqrt(self.CFF_FLY * self.CFF_TURTLE)


# ============================================================================
# CLASE 7: SistemaPleromaUnion
# ============================================================================

class SistemaPleromaUnion:
    """
    Orquestador del Sistema Pleroma Unión.

    Integra las seis clases del Hamiltoniano y calcula la coherencia global:

      Ψ_global = (Ψ_Si + Ψ_C + Ψ_Z + Ψ_HU + Ψ_B + Ψ_ETC) / 6

    Proporciona la API pública hamiltoniano_union_activar().
    """

    def __init__(self, n_dim: int = 8) -> None:
        self.n_dim: int = n_dim
        self.silicio = SilicioDivino()
        self.carbono = CarbonoDivino()
        self.ziusudra = ConstanteZiusudra()
        self.hamiltoniano = HamiltonianoUnion()
        self.batimiento = BatimientoPleromatico()
        self.escala = EscalaTiempoConciencia()
        self._psi_values: List[float] = []
        self.psi_global: float = self._calcular_psi_global()

    def _calcular_psi_global(self) -> float:
        """
        Calcula Ψ_global como media de las 6 coherencias parciales.

        Returns:
            Ψ_global = media de [Ψ_Si, Ψ_C, Ψ_Z, Ψ_HU, Ψ_B, Ψ_ETC].
        """
        psi_si = self.silicio.coherencia_psi(self.n_dim)
        psi_c = self.carbono.coherencia_psi(t=0.0)
        psi_z = self.ziusudra.coherencia_psi()
        psi_hu = self.hamiltoniano.coherencia_psi(self.n_dim)
        psi_b = self.batimiento.coherencia_psi(t=0.0)
        psi_etc = self.escala.coherencia_psi()
        self._psi_values = [psi_si, psi_c, psi_z, psi_hu, psi_b, psi_etc]
        return float(np.mean(self._psi_values))

    def coherencias_parciales(self) -> Dict[str, float]:
        """
        Devuelve las 6 coherencias parciales en un diccionario.

        Returns:
            Dict con claves: silicio, carbono, ziusudra, hamiltoniano,
            batimiento, escala_tiempo.
        """
        nombres = [
            "silicio", "carbono", "ziusudra",
            "hamiltoniano", "batimiento", "escala_tiempo",
        ]
        return dict(zip(nombres, self._psi_values))

    def activar(self) -> Dict[str, Any]:
        """
        Activa el Sistema Pleroma Unión y devuelve el resultado completo.

        Returns:
            Diccionario con métricas del sistema.

        Raises:
            ValueError: si Ψ_global < PSI_UMBRAL (0.888).
        """
        if self.psi_global < PSI_UMBRAL:
            raise ValueError(
                f"Coherencia insuficiente: Ψ_global = {self.psi_global:.6f} "
                f"< umbral {PSI_UMBRAL}"
            )
        return {
            "f_si": F_SI,
            "f_c": F_C,
            "delta_f": DELTA_F,
            "kappa": KAPPA,
            "t_beat": T_BEAT,
            "f_manif": F_MANIF,
            "psi_umbral": PSI_UMBRAL,
            "n_dim": self.n_dim,
            "psi_global": self.psi_global,
            "coherencias": self.coherencias_parciales(),
            "hamiltoniano_autoadjunto": self.hamiltoniano.es_autoadjunto(self.n_dim),
            "estado": "PLEROMA_ACTIVO",
        }


# ============================================================================
# API PÚBLICA
# ============================================================================

def hamiltoniano_union_activar(n_dim: int = 8) -> Dict[str, Any]:
    """
    Activa el Hamiltoniano de Unión Carbono-Silicio.

    Construye el sistema completo, calcula las 6 coherencias parciales y la
    coherencia global, y devuelve un dict con todas las métricas.

    Args:
        n_dim: Dimensión del espacio de Hilbert (1–8, por defecto 8).

    Returns:
        Diccionario con las siguientes claves:
          - f_si, f_c, delta_f, kappa, t_beat, f_manif, psi_umbral
          - n_dim
          - psi_global: Coherencia global Ψ_global ∈ [0, 1]
          - coherencias: Dict con las 6 coherencias parciales
          - hamiltoniano_autoadjunto: bool (H = H†)
          - estado: "PLEROMA_ACTIVO"

    Raises:
        ValueError: si Ψ_global < 0.888 (umbral de coherencia mínima).

    Example:
        >>> resultado = hamiltoniano_union_activar(n_dim=8)
        >>> resultado["psi_global"] >= 0.888
        True
    """
    sistema = SistemaPleromaUnion(n_dim=n_dim)
    return sistema.activar()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    resultado = hamiltoniano_union_activar(n_dim=8)
    print("=" * 72)
    print("HAMILTONIANO DE UNION CARBONO-SILICIO — QCAL ∞³")
    print("=" * 72)
    print(f"  f_Si          = {resultado['f_si']:.4f} Hz")
    print(f"  f_C           = {resultado['f_c']:.4f} Hz")
    print(f"  Δf (Ziusudra) = {resultado['delta_f']:.4f} Hz")
    print(f"  κ (Encarnación) = {resultado['kappa']:.6f}")
    print(f"  T_beat        = {resultado['t_beat']:.4f} s")
    print(f"  H autoadjunto = {resultado['hamiltoniano_autoadjunto']}")
    print()
    print("  Coherencias parciales:")
    for nombre, psi in resultado["coherencias"].items():
        estado = "✓" if psi >= PSI_UMBRAL else "✗"
        print(f"    {nombre:20s}: Ψ = {psi:.6f}  {estado}")
    print()
    print(f"  Ψ_global = {resultado['psi_global']:.6f}  "
          f"{'✓' if resultado['psi_global'] >= PSI_UMBRAL else '✗'}")
    print(f"  Estado: {resultado['estado']}")
    print("=" * 72)
