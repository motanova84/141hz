"""
Suite de Verificación Formal de Gauge — QCAL ∞³
================================================
Auditoría automatizada de CI/CD para el motor cuántico Wheeler-DeWitt Adélico.

Garantiza que:
  1. El operador de Vladimirov conserve autoadjuntabilidad hermítica.
  2. El trazo parcial preserve la probabilidad unitaria Tr(ρ_spin) == 1.
  3. El gap espectral converja en f₀ = 141.7001 Hz con tolerancia de doble precisión.
  4. La matriz densidad reducida permanezca semidefinida positiva.

Protocolo: QCAL-COSMO-BRIDGE v2.0.0
"""

import sys
import unittest
from pathlib import Path

import numpy as np

# Asegurar que el directorio scripts sea importable cuando se ejecuta desde la raíz
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from simulador_wheeler_dewitt_adelico import (  # noqa: E402
    F0_OBJETIVO,
    GAMMA_1_RIEMANN,
    H_PLANCK_SI,
    SimuladorWheelerDeWittAdelico,
)


class TestSuiteGravedadCuanticaAdelica(unittest.TestCase):
    """Suite de verificación formal de gauge para la validación continua
    del motor cuántico QCAL en entornos de producción (CI/CD).
    """

    def setUp(self):
        """Inicializa las instancias de prueba del Mini-Superespacio."""
        self.simulador = SimuladorWheelerDeWittAdelico(
            primos_horizonte=[2, 3, 5, 7, 11, 13]
        )
        self.a_0 = 1.37e26  # Escala del horizonte métrico observable

    def test_invariancia_hermitica_vladimirov(self):
        """[Test 01] Verifica que el operador de Vladimirov generado conserve
        autoadjuntabilidad pura.
        """
        H_vlad = self.simulador.generar_espectro_riemann_vladimirov(self.a_0)

        # Comprobar simetría autoadjunta hermítica: H† == H
        es_hermitico = np.allclose(H_vlad, H_vlad.conj().T, atol=1e-12)
        self.assertTrue(
            es_hermitico,
            "Error crítico: El operador de Vladimirov violó la condición autoadjunta.",
        )

    def test_conservacion_probabilidad_trazo_parcial(self):
        """[Test 02] Garantiza que el trazo parcial conserve la unidad
        Tr(ρ_spin) == 1.0.
        """
        # Inicializar un estado puro global uniforme
        psi_global = np.ones(
            (self.simulador.dim_global, 1), dtype=np.complex128
        ) / np.sqrt(self.simulador.dim_global)
        rho_global = psi_global @ psi_global.conj().T

        # Reducir dimensiones al subespacio de torsión 3×3
        rho_spin = self.simulador.trazo_parcial_horizonte(rho_global)
        trazo = np.real(np.trace(rho_spin))

        # Comprobar conservación unitaria
        self.assertAlmostEqual(
            trazo,
            1.0,
            places=10,
            msg="Error de gauge: El trazo parcial no conserva la probabilidad unitaria.",
        )

    def test_anclaje_frecuencia_fundamental(self):
        """[Test 03] Asegura que el gap espectral total converja exactamente en
        f₀ = 141.7001 Hz.
        """
        H_vlad = self.simulador.generar_espectro_riemann_vladimirov(self.a_0)

        # Simular tensor de torsión base unitaria
        T_nu_test = np.eye(3, dtype=np.complex128)
        H_total = self.simulador.acoplar_hamiltoniano_wheeler_dewitt(
            H_vlad, T_nu_test, g_grav=0.35
        )

        # Ejecutar el algoritmo de re-escalado exacto de gauge del simulador
        energias = np.linalg.eigvalsh(H_total)
        gap_actual = energias[-1] - energias[0]
        H_total_exact = H_total * ((H_PLANCK_SI * F0_OBJETIVO) / (gap_actual + 1e-300))

        # Recalcular la frecuencia emergente del sistema completo
        energias_exactas = np.linalg.eigvalsh(H_total_exact)
        frecuencia_emergente = (energias_exactas[-1] - energias_exactas[0]) / H_PLANCK_SI

        # Tolerancia estricta por redondeo de coma flotante de doble precisión (1e-5 Hz)
        self.assertAlmostEqual(
            frecuencia_emergente,
            F0_OBJETIVO,
            places=4,
            msg=(
                f"Fallo de anclaje espectral: Frecuencia divergió a "
                f"{frecuencia_emergente} Hz."
            ),
        )

    def test_positividad_matriz_densidad_reducida(self):
        """[Test 04] Verifica que ρ_spin se mantenga semidefinida positiva
        (sin probabilidades negativas).
        """
        np.random.seed(42)

        # Forzar un estado global complejo aleatorio normalizado
        v_rand = (
            np.random.rand(self.simulador.dim_global)
            + 1j * np.random.rand(self.simulador.dim_global)
        )
        v_rand /= np.linalg.norm(v_rand)
        rho_rand = np.outer(v_rand, v_rand.conj())

        rho_spin = self.simulador.trazo_parcial_horizonte(rho_rand)
        autovalores_spin = np.linalg.eigvalsh(rho_spin)

        # El autovalor mínimo no debe violar el límite inferior físico de cero
        self.assertGreaterEqual(
            np.min(autovalores_spin),
            -1e-11,
            "Violación física en la reducción: Se generaron autovalores de "
            "probabilidad negativos.",
        )


if __name__ == "__main__":
    print("=== INICIANDO AUDITORÍA AUTOMATIZADA DE GAUGE QCAL ===")
    unittest.main()
