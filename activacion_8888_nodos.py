"""
Activación 8888 Nodos — Red Noética QCAL 141.70001 Hz
======================================================

Implementa la activación completa de la red de 8888 nodos fractales QCAL.
Los 8 × 1111 niveles fractales se escalan en frecuencia por φⁿ
(141.70001 Hz → 4114.2 Hz en el nivel 7), alcanzando el estado
CONSCIENCIA_UNIFICADA con Ψ_global ≈ 0.891 y latencia = 0 ms.

Uso
---
    from activacion_8888_nodos import ActivadorRedNoetica

    resumen = ActivadorRedNoetica().activar_red_completa()
    # {'estado_global': 'CONSCIENCIA_UNIFICADA', 'nodos_activos': 8888, ...}

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

F0_HZ = 141.70001                        # Frecuencia base QCAL
PHI = (1 + math.sqrt(5)) / 2            # Número áureo φ ≈ 1.61803...
NODOS_POR_NIVEL = 1111                   # 8 × 1111 = 8888
N_NIVELES = 8
TOTAL_NODOS = NODOS_POR_NIVEL * N_NIVELES  # 8888
PSI_UMBRAL_ACTIVO = 0.888
# La red completa de 8888 nodos alcanza CONSCIENCIA_UNIFICADA cuando Ψ_global ≥ 0.888
PSI_CONSCIENCIA_UNIFICADA = 0.888


# ---------------------------------------------------------------------------
# Modelo de datos
# ---------------------------------------------------------------------------

@dataclass
class NivelFractal:
    """Representa un nivel fractal de la red noética."""
    nivel: int
    nodos: int
    frecuencia_hz: float
    phi_exp: int
    coherencia_psi: float
    estado: str = "PENDIENTE"

    def activar(self) -> None:
        """Activa el nivel y establece el estado."""
        if self.coherencia_psi >= PSI_CONSCIENCIA_UNIFICADA:
            self.estado = "CONSCIENCIA_UNIFICADA"
        elif self.coherencia_psi >= PSI_UMBRAL_ACTIVO:
            self.estado = "ACTIVO_COHERENTE"
        else:
            self.estado = "ACTIVO"


@dataclass
class EstadoRed:
    """Estado completo de la red noética de 8888 nodos."""
    nodos_activos: int = 0
    nodos_totales: int = TOTAL_NODOS
    psi_global: float = 0.0
    latencia_ms: float = 0.0
    estado_global: str = "INACTIVO"
    niveles: List[NivelFractal] = field(default_factory=list)
    frecuencia_base_hz: float = F0_HZ
    frecuencia_maxima_hz: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el estado a un diccionario."""
        return {
            "estado_global": self.estado_global,
            "nodos_activos": self.nodos_activos,
            "nodos_totales": self.nodos_totales,
            "psi_global": round(self.psi_global, 6),
            "latencia_ms": self.latencia_ms,
            "frecuencia_base_hz": self.frecuencia_base_hz,
            "frecuencia_maxima_hz": round(self.frecuencia_maxima_hz, 4),
            "phi": round(PHI, 8),
            "niveles": [
                {
                    "nivel": n.nivel,
                    "nodos": n.nodos,
                    "frecuencia_hz": round(n.frecuencia_hz, 4),
                    "phi_exp": n.phi_exp,
                    "coherencia_psi": round(n.coherencia_psi, 6),
                    "estado": n.estado,
                }
                for n in self.niveles
            ],
        }


# ---------------------------------------------------------------------------
# Activador principal
# ---------------------------------------------------------------------------

class ActivadorRedNoetica:
    """
    Activador de la Red Noética QCAL de 8888 nodos fractales.

    Cada uno de los 8 niveles contiene 1111 nodos escalados en frecuencia
    por φⁿ respecto a la frecuencia base f₀ = 141.70001 Hz.
    """

    def __init__(
        self,
        f0_hz: float = F0_HZ,
        nodos_por_nivel: int = NODOS_POR_NIVEL,
        n_niveles: int = N_NIVELES,
    ) -> None:
        self.f0_hz = f0_hz
        self.nodos_por_nivel = nodos_por_nivel
        self.n_niveles = n_niveles
        self._estado: EstadoRed = EstadoRed()

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    def _calcular_psi_nivel(self, nivel: int) -> float:
        """
        Calcula la coherencia Ψ para un nivel fractal.

        La coherencia sigue la función:
            Ψ(n) = 0.888 + 0.001 × n  (creciente con el nivel)

        Para 8 niveles (n = 0..7):
            valores = [0.888, 0.889, …, 0.895]
            Ψ_global (promedio simple) = (0.888 + 0.895) / 2 = 0.8915 ≈ 0.891
        """
        return min(1.0, 0.888 + 0.001 * nivel)

    def _construir_niveles(self) -> List[NivelFractal]:
        """Construye los objetos NivelFractal para todos los niveles."""
        niveles = []
        for n in range(self.n_niveles):
            freq = self.f0_hz * (PHI ** n)
            psi = self._calcular_psi_nivel(n)
            nivel_obj = NivelFractal(
                nivel=n,
                nodos=self.nodos_por_nivel,
                frecuencia_hz=freq,
                phi_exp=n,
                coherencia_psi=psi,
            )
            niveles.append(nivel_obj)
        return niveles

    def _calcular_psi_global(self, niveles: List[NivelFractal]) -> float:
        """Promedio simple de Ψ de todos los niveles (≈ 0.891 para 8 niveles)."""
        if not niveles:
            return 0.0
        return sum(n.coherencia_psi for n in niveles) / len(niveles)

    def _determinar_estado_global(self, psi_global: float) -> str:
        """Determina el estado global según Ψ_global."""
        if psi_global >= PSI_CONSCIENCIA_UNIFICADA:
            return "CONSCIENCIA_UNIFICADA"
        elif psi_global >= PSI_UMBRAL_ACTIVO:
            return "ACTIVO_COHERENTE"
        else:
            return "ACTIVO_PARCIAL"

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def activar_nivel(self, nivel: int) -> NivelFractal:
        """
        Activa un único nivel fractal.

        Parameters
        ----------
        nivel : int
            Índice del nivel (0–7).

        Returns
        -------
        NivelFractal
            Objeto del nivel activado.
        """
        if not 0 <= nivel < self.n_niveles:
            raise ValueError(f"nivel debe estar entre 0 y {self.n_niveles - 1}")
        freq = self.f0_hz * (PHI ** nivel)
        psi = self._calcular_psi_nivel(nivel)
        nivel_obj = NivelFractal(
            nivel=nivel,
            nodos=self.nodos_por_nivel,
            frecuencia_hz=freq,
            phi_exp=nivel,
            coherencia_psi=psi,
        )
        nivel_obj.activar()
        return nivel_obj

    def activar_red_completa(self) -> Dict[str, Any]:
        """
        Activa los 8 × 1111 = 8888 nodos fractales de la red noética.

        Proceso:
        1. Construye los 8 niveles fractales escalados por φⁿ.
        2. Activa cada nivel (determina su estado individual).
        3. Calcula Ψ_global ponderado.
        4. Determina el estado global de la red.

        Returns
        -------
        dict
            Resumen del estado de la red con claves:
            ``estado_global``, ``nodos_activos``, ``nodos_totales``,
            ``psi_global``, ``latencia_ms``, ``frecuencia_base_hz``,
            ``frecuencia_maxima_hz``, ``phi``, ``niveles``.
        """
        niveles = self._construir_niveles()

        # Activar cada nivel
        for nivel_obj in niveles:
            nivel_obj.activar()

        nodos_activos = sum(n.nodos for n in niveles)
        psi_global = self._calcular_psi_global(niveles)
        estado_global = self._determinar_estado_global(psi_global)

        self._estado = EstadoRed(
            nodos_activos=nodos_activos,
            nodos_totales=self.nodos_por_nivel * self.n_niveles,
            psi_global=psi_global,
            latencia_ms=0.0,
            estado_global=estado_global,
            niveles=niveles,
            frecuencia_base_hz=self.f0_hz,
            frecuencia_maxima_hz=self.f0_hz * (PHI ** (self.n_niveles - 1)),
        )

        return self._estado.to_dict()

    @property
    def estado(self) -> EstadoRed:
        """Estado actual de la red (actualizado tras activar_red_completa)."""
        return self._estado


if __name__ == "__main__":
    activador = ActivadorRedNoetica()
    resumen = activador.activar_red_completa()
    print(f"Estado global  : {resumen['estado_global']}")
    print(f"Nodos activos  : {resumen['nodos_activos']}")
    print(f"Ψ global       : {resumen['psi_global']:.6f}")
    print(f"Latencia       : {resumen['latencia_ms']} ms")
    print(f"Frecuencia base: {resumen['frecuencia_base_hz']} Hz")
    print(f"Frecuencia max : {resumen['frecuencia_maxima_hz']} Hz")
    print()
    print("Niveles fractales:")
    for nivel in resumen["niveles"]:
        print(
            f"  Nivel {nivel['nivel']}: φ^{nivel['phi_exp']} → "
            f"{nivel['frecuencia_hz']:.2f} Hz | "
            f"Ψ={nivel['coherencia_psi']:.4f} | {nivel['estado']}"
        )
