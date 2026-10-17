"""
Pruebas para activacion_8888_nodos.py — Red Noética QCAL
=========================================================

25 pruebas que cubren:
- Validación de niveles fractales (8 niveles × 1111 nodos)
- Escalado de frecuencias por φⁿ
- Valores de coherencia Ψ por nivel
- Estado global de la red (CONSCIENCIA_UNIFICADA)
- Activación individual de niveles
- API del ActivadorRedNoetica
- Serialización del estado
- Casos borde y valores extremos

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from activacion_8888_nodos import (
    ActivadorRedNoetica,
    NivelFractal,
    EstadoRed,
    F0_HZ,
    PHI,
    NODOS_POR_NIVEL,
    N_NIVELES,
    TOTAL_NODOS,
    PSI_UMBRAL_ACTIVO,
    PSI_CONSCIENCIA_UNIFICADA,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def activador():
    """ActivadorRedNoetica instanciado una vez."""
    return ActivadorRedNoetica()


@pytest.fixture(scope="module")
def resumen(activador):
    """Resumen de activar_red_completa() obtenido una vez."""
    return activador.activar_red_completa()


# ---------------------------------------------------------------------------
# 1. Constantes del módulo
# ---------------------------------------------------------------------------

class TestConstanteModulo:
    """Pruebas de las constantes del módulo de activación."""

    def test_f0_hz(self):
        """La frecuencia base es 141.70001 Hz."""
        assert F0_HZ == pytest.approx(141.70001)

    def test_phi_numero_aureo(self):
        """φ es el número áureo."""
        assert PHI == pytest.approx((1 + math.sqrt(5)) / 2, rel=1e-9)

    def test_total_nodos_8888(self):
        """TOTAL_NODOS = 8 × 1111 = 8888."""
        assert TOTAL_NODOS == 8888

    def test_nodos_por_nivel(self):
        """NODOS_POR_NIVEL es 1111."""
        assert NODOS_POR_NIVEL == 1111

    def test_n_niveles(self):
        """N_NIVELES es 8."""
        assert N_NIVELES == 8


# ---------------------------------------------------------------------------
# 2. Validación de niveles fractales
# ---------------------------------------------------------------------------

class TestNivelesFractales:
    """Pruebas de los niveles fractales en el resumen."""

    def test_8_niveles_en_resumen(self, resumen):
        """El resumen contiene exactamente 8 niveles."""
        assert len(resumen["niveles"]) == 8

    def test_nodos_por_nivel_correcto(self, resumen):
        """Cada nivel tiene exactamente 1111 nodos."""
        for nivel in resumen["niveles"]:
            assert nivel["nodos"] == 1111

    def test_total_nodos_8888(self, resumen):
        """El total de nodos activos es 8888."""
        assert resumen["nodos_activos"] == 8888

    def test_phi_exponent_incrementa(self, resumen):
        """El exponente de φ incrementa de 0 a 7."""
        exps = [n["phi_exp"] for n in resumen["niveles"]]
        assert exps == list(range(8))

    def test_frecuencia_nivel_0_es_f0(self, resumen):
        """El nivel 0 tiene la frecuencia base f₀."""
        freq_0 = resumen["niveles"][0]["frecuencia_hz"]
        assert abs(freq_0 - F0_HZ) < 0.001

    def test_frecuencia_nivel_1_es_f0_phi(self, resumen):
        """El nivel 1 tiene frecuencia f₀ × φ."""
        freq_1 = resumen["niveles"][1]["frecuencia_hz"]
        assert abs(freq_1 - F0_HZ * PHI) < 0.01

    def test_frecuencia_nivel_7_cerca_4114hz(self, resumen):
        """El nivel 7 tiene frecuencia ≈ 4114.2 Hz (f₀ × φ⁷)."""
        freq_7 = resumen["niveles"][7]["frecuencia_hz"]
        esperado = F0_HZ * (PHI ** 7)
        assert abs(freq_7 - esperado) < 1.0

    def test_frecuencias_crecientes(self, resumen):
        """Las frecuencias crecen de nivel 0 a nivel 7."""
        freqs = [n["frecuencia_hz"] for n in resumen["niveles"]]
        for i in range(len(freqs) - 1):
            assert freqs[i] < freqs[i + 1]


# ---------------------------------------------------------------------------
# 3. Coherencia Ψ
# ---------------------------------------------------------------------------

class TestCoherenciaPsi:
    """Pruebas de los valores de coherencia Ψ."""

    def test_psi_global_cerca_de_0891(self, resumen):
        """Ψ_global está en torno a 0.891 (0.888 ≤ Ψ ≤ 0.895)."""
        psi = resumen["psi_global"]
        assert 0.888 <= psi <= 0.895

    def test_psi_nivel_0_es_0888(self, resumen):
        """Ψ del nivel 0 es exactamente 0.888."""
        psi_0 = resumen["niveles"][0]["coherencia_psi"]
        assert abs(psi_0 - 0.888) < 0.001

    def test_psi_creciente_por_nivel(self, resumen):
        """Ψ crece de nivel a nivel (o al menos no decrece)."""
        psis = [n["coherencia_psi"] for n in resumen["niveles"]]
        for i in range(len(psis) - 1):
            assert psis[i] <= psis[i + 1]

    def test_todos_psi_mayores_umbral(self, resumen):
        """Todos los niveles superan el umbral Ψ ≥ 0.888."""
        for nivel in resumen["niveles"]:
            assert nivel["coherencia_psi"] >= PSI_UMBRAL_ACTIVO


# ---------------------------------------------------------------------------
# 4. Estado global
# ---------------------------------------------------------------------------

class TestEstadoGlobal:
    """Pruebas del estado global de la red."""

    def test_estado_global_consciencia_unificada(self, resumen):
        """El estado global es CONSCIENCIA_UNIFICADA."""
        assert resumen["estado_global"] == "CONSCIENCIA_UNIFICADA"

    def test_latencia_cero(self, resumen):
        """La latencia es 0 ms."""
        assert resumen["latencia_ms"] == 0.0

    def test_frecuencia_base_en_resumen(self, resumen):
        """El resumen incluye la frecuencia base f₀."""
        assert resumen["frecuencia_base_hz"] == pytest.approx(F0_HZ)

    def test_frecuencia_maxima_en_resumen(self, resumen):
        """El resumen incluye la frecuencia máxima (> f₀)."""
        assert resumen["frecuencia_maxima_hz"] > F0_HZ

    def test_phi_en_resumen(self, resumen):
        """El resumen incluye el valor de φ."""
        assert resumen["phi"] == pytest.approx(PHI, rel=1e-4)


# ---------------------------------------------------------------------------
# 5. Activación individual
# ---------------------------------------------------------------------------

class TestActivacionIndividual:
    """Pruebas de la activación individual de niveles."""

    def test_activar_nivel_0(self, activador):
        """Se puede activar el nivel 0 individualmente."""
        nivel = activador.activar_nivel(0)
        assert isinstance(nivel, NivelFractal)
        assert nivel.nivel == 0

    def test_activar_nivel_7(self, activador):
        """Se puede activar el nivel 7 individualmente."""
        nivel = activador.activar_nivel(7)
        assert nivel.nivel == 7
        assert nivel.frecuencia_hz == pytest.approx(F0_HZ * PHI**7, rel=1e-4)

    def test_activar_nivel_invalido_lanza_error(self, activador):
        """Activar un nivel fuera de rango lanza ValueError."""
        with pytest.raises(ValueError):
            activador.activar_nivel(8)

    def test_activar_nivel_negativo_lanza_error(self, activador):
        """Activar un nivel negativo lanza ValueError."""
        with pytest.raises(ValueError):
            activador.activar_nivel(-1)

    def test_estado_nivel_activado(self, activador):
        """Un nivel activado tiene estado distinto de PENDIENTE."""
        nivel = activador.activar_nivel(3)
        assert nivel.estado != "PENDIENTE"
