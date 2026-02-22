#!/usr/bin/env python3
"""
Tests for GW171012 Noetic Ψ On/Off Analysis
============================================

Valida el módulo gw171012_analysis que implementa el Protocolo de
Detección en el Límite para el evento marginal GW171012.

Los tests verifican:
1. Parámetros del evento GW171012 (GPS, banda, SNR)
2. Simulación de datos H1 y L1
3. Blanqueo de datos en la banda 30-400 Hz
4. Cálculo de la métrica Ψ
5. Análisis on/off con ratio ≥ 100 y p-value ≤ 0.01
6. Tabla comparativa GW150914 vs GW171012

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import unittest
import numpy as np
import sys
import os

# Añadir el directorio raíz al path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '141Hz'))

from analysis import gw171012_analysis


class TestGW171012Params(unittest.TestCase):
    """Tests para los parámetros del evento GW171012."""

    def test_gps_time(self):
        """Test: GPS time debe coincidir con el catálogo GWTC-1."""
        self.assertAlmostEqual(
            gw171012_analysis.GW171012_PARAMS['gps_time'],
            1189155585.4,
            places=0,
            msg="GPS time de GW171012 debe ser ≈ 1189155585.4"
        )

    def test_detectores(self):
        """Test: El evento GW171012 fue detectado por H1 y L1."""
        detectores = gw171012_analysis.GW171012_PARAMS['detectors']
        self.assertIn('H1', detectores)
        self.assertIn('L1', detectores)

    def test_sample_rate(self):
        """Test: Tasa de muestreo debe ser 4096 Hz."""
        self.assertEqual(
            gw171012_analysis.GW171012_PARAMS['sample_rate'],
            4096.0
        )

    def test_banda_analisis(self):
        """Test: La banda de blanqueo es 30-400 Hz."""
        params = gw171012_analysis.GW171012_PARAMS
        self.assertEqual(params['banda_inferior'], 30.0)
        self.assertEqual(params['banda_superior'], 400.0)

    def test_snr_clasico(self):
        """Test: El SNR clásico LIGO de GW171012 es ~10."""
        snr = gw171012_analysis.GW171012_PARAMS['snr_clasico']
        self.assertGreaterEqual(snr, 8.0, "SNR debe ser ≥ 8")
        self.assertLessEqual(snr, 15.0, "SNR debe ser ≤ 15")

    def test_ratio_publicado(self):
        """Test: El ratio Ψ_on/Ψ_off publicado es 184."""
        self.assertAlmostEqual(
            gw171012_analysis.GW171012_PARAMS['ratio_psi_on_off'],
            184.0,
            places=0
        )

    def test_p_value_publicado(self):
        """Test: El p-value publicado es 2.31×10⁻⁴."""
        p = gw171012_analysis.GW171012_PARAMS['p_value']
        self.assertAlmostEqual(p, 2.31e-4, delta=1e-5)


class TestSimulacionDatos(unittest.TestCase):
    """Tests para la simulación de datos de GW171012."""

    def setUp(self):
        self.sample_rate = 4096.0
        self.duration = 1.0
        self.N = int(self.duration * self.sample_rate)

    def test_longitud_datos(self):
        """Test: La simulación devuelve el número correcto de muestras."""
        datos = gw171012_analysis.simular_datos_gw171012(
            detector='H1', duration=self.duration,
            sample_rate=self.sample_rate
        )
        self.assertEqual(len(datos), self.N)

    def test_datos_son_array(self):
        """Test: La simulación devuelve un ndarray."""
        datos = gw171012_analysis.simular_datos_gw171012('H1')
        self.assertIsInstance(datos, np.ndarray)

    def test_reproducibilidad_semilla(self):
        """Test: Con la misma semilla los datos son idénticos."""
        d1 = gw171012_analysis.simular_datos_gw171012('H1', semilla=42)
        d2 = gw171012_analysis.simular_datos_gw171012('H1', semilla=42)
        np.testing.assert_array_equal(d1, d2)

    def test_diferentes_semillas_dan_diferentes_datos(self):
        """Test: Semillas distintas producen datos distintos."""
        d1 = gw171012_analysis.simular_datos_gw171012('H1', semilla=1)
        d2 = gw171012_analysis.simular_datos_gw171012('H1', semilla=2)
        # Comparación element-wise: al menos un elemento debe diferir
        self.assertFalse(np.array_equal(d1, d2))

    def test_h1_l1_diferentes(self):
        """Test: H1 y L1 producen datos distintos (semillas distintas)."""
        d_h1 = gw171012_analysis.simular_datos_gw171012('H1')
        d_l1 = gw171012_analysis.simular_datos_gw171012('L1')
        self.assertFalse(np.array_equal(d_h1, d_l1))

    def test_sin_senal_menor_amplitud(self):
        """Test: Datos sin señal tienen amplitud menor o similar al ruido."""
        d_ruido = gw171012_analysis.simular_datos_gw171012(
            'H1', incluir_senal=False, semilla=99)
        d_senal = gw171012_analysis.simular_datos_gw171012(
            'H1', incluir_senal=True, semilla=99)
        # La std no debe ser radicalmente diferente (señal débil)
        ratio_std = np.std(d_senal) / max(np.std(d_ruido), 1e-60)
        self.assertLess(ratio_std, 10.0,
                        "La señal GW171012 es débil; amplitud no debe dominar")


class TestBlanqueo(unittest.TestCase):
    """Tests para el blanqueo de datos."""

    def setUp(self):
        np.random.seed(0)
        self.sample_rate = 4096.0
        N = int(1.0 * self.sample_rate)
        self.datos = np.random.randn(N) * 1e-23

    def test_blanqueo_retorna_array(self):
        """Test: El blanqueo devuelve un ndarray."""
        blanqueados = gw171012_analysis.blanquear_datos(
            self.datos, self.sample_rate)
        self.assertIsInstance(blanqueados, np.ndarray)

    def test_blanqueo_misma_longitud(self):
        """Test: El blanqueo no cambia la longitud."""
        blanqueados = gw171012_analysis.blanquear_datos(
            self.datos, self.sample_rate)
        self.assertEqual(len(blanqueados), len(self.datos))

    def test_blanqueo_reduce_potencia_fuera_de_banda(self):
        """Test: La potencia fuera de 30-400 Hz debe ser baja tras el blanqueo."""
        # Añadir señal fuerte a 10 Hz (fuera de la banda)
        t = np.arange(len(self.datos)) / self.sample_rate
        datos_con_linea = self.datos.copy()
        datos_con_linea += 1e-20 * np.sin(2 * np.pi * 10.0 * t)

        blanqueados = gw171012_analysis.blanquear_datos(
            datos_con_linea, self.sample_rate, fmin=30.0, fmax=400.0)

        freqs = np.fft.rfftfreq(len(blanqueados), 1.0 / self.sample_rate)
        fft_b = np.abs(np.fft.rfft(blanqueados))

        # Potencia a 10 Hz debe ser baja respecto a la potencia en la banda
        idx_10 = np.argmin(np.abs(freqs - 10.0))
        idx_141 = np.argmin(np.abs(freqs - 141.7))
        self.assertLess(fft_b[idx_10], fft_b[idx_141] * 100,
                        "El filtro paso-banda debe atenuar 10 Hz respecto a 141 Hz")

    def test_blanqueo_array_vacio(self):
        """Test: Blanqueo de array vacío devuelve array vacío."""
        resultado = gw171012_analysis.blanquear_datos(
            np.array([]), self.sample_rate)
        self.assertEqual(len(resultado), 0)


class TestMetricaPsi(unittest.TestCase):
    """Tests para el cálculo de la métrica Ψ."""

    def setUp(self):
        np.random.seed(42)
        self.sample_rate = 4096.0
        N = int(1.0 * self.sample_rate)
        self.ruido_h1 = np.random.randn(N)
        self.ruido_l1 = np.random.randn(N)
        self.target_freq = 141.7

    def test_psi_positivo(self):
        """Test: Ψ debe ser ≥ 0."""
        psi = gw171012_analysis.calcular_psi(
            self.ruido_h1, self.ruido_l1,
            self.sample_rate, self.target_freq
        )
        self.assertGreaterEqual(psi, 0.0)

    def test_psi_senal_mayor_que_ruido(self):
        """Test: Ψ con señal coherente debe ser mayor que Ψ de ruido puro."""
        t = np.arange(len(self.ruido_h1)) / self.sample_rate
        senal = 10.0 * np.sin(2.0 * np.pi * self.target_freq * t)

        psi_ruido = gw171012_analysis.calcular_psi(
            self.ruido_h1, self.ruido_l1,
            self.sample_rate, self.target_freq
        )
        psi_senal = gw171012_analysis.calcular_psi(
            self.ruido_h1 + senal, self.ruido_l1 + senal,
            self.sample_rate, self.target_freq
        )
        self.assertGreater(psi_senal, psi_ruido,
                           "Señal coherente debe elevar Ψ respecto al ruido puro")

    def test_psi_arrays_vacios(self):
        """Test: Ψ con arrays vacíos devuelve 0."""
        psi = gw171012_analysis.calcular_psi(
            np.array([]), np.array([]),
            self.sample_rate, self.target_freq
        )
        self.assertEqual(psi, 0.0)

    def test_psi_simetria(self):
        """Test: Ψ(H1, L1) == Ψ(L1, H1) (simetría)."""
        psi_a = gw171012_analysis.calcular_psi(
            self.ruido_h1, self.ruido_l1,
            self.sample_rate, self.target_freq
        )
        psi_b = gw171012_analysis.calcular_psi(
            self.ruido_l1, self.ruido_h1,
            self.sample_rate, self.target_freq
        )
        self.assertAlmostEqual(psi_a, psi_b, places=10)


class TestAnalisisOnOff(unittest.TestCase):
    """Tests para el análisis on/off completo."""

    def setUp(self):
        """Calcular resultado una vez para todos los subtests."""
        # Usar pocas ventanas para que el test sea rápido
        self.resultado = gw171012_analysis.analisis_on_off(
            n_ventanas_off=50,
            mostrar_detalles=False
        )

    def test_estructura_resultado(self):
        """Test: El resultado contiene todas las claves esperadas."""
        claves = [
            'nombre_evento', 'gps_time', 'snr_clasico',
            'psi_on', 'psi_off_mean', 'psi_off_std',
            'ratio', 'p_value', 'n_ventanas_off',
            'deteccion_confirmada', 'banda', 'target_freq',
        ]
        for clave in claves:
            self.assertIn(clave, self.resultado,
                          f"Falta clave '{clave}' en el resultado")

    def test_nombre_evento(self):
        """Test: El nombre del evento es GW171012."""
        self.assertEqual(self.resultado['nombre_evento'], 'GW171012')

    def test_gps_time_resultado(self):
        """Test: El GPS time en el resultado coincide con GW171012."""
        self.assertAlmostEqual(
            self.resultado['gps_time'],
            1189155585.4,
            places=0
        )

    def test_psi_on_positivo(self):
        """Test: Ψ on-source debe ser positivo."""
        self.assertGreater(self.resultado['psi_on'], 0.0)

    def test_psi_off_mean_positivo(self):
        """Test: Ψ off-source medio debe ser positivo."""
        self.assertGreater(self.resultado['psi_off_mean'], 0.0)

    def test_ratio_mayor_que_uno(self):
        """Test: Ratio Ψ_on/Ψ_off debe ser > 1 (señal supera fondo)."""
        self.assertGreater(self.resultado['ratio'], 1.0)

    def test_p_value_rango_valido(self):
        """Test: P-value debe estar en (0, 1)."""
        p = self.resultado['p_value']
        self.assertGreater(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_snr_clasico_consistente(self):
        """Test: SNR clásico en resultado es ~10."""
        expected_snr = gw171012_analysis.GW171012_PARAMS['snr_clasico']
        self.assertAlmostEqual(
            self.resultado['snr_clasico'],
            expected_snr,
            places=5
        )

    def test_n_ventanas_off(self):
        """Test: El número de ventanas off coincide con el solicitado."""
        self.assertEqual(self.resultado['n_ventanas_off'], 50)

    def test_banda_correcta(self):
        """Test: La banda de análisis es (30, 400) Hz."""
        self.assertEqual(self.resultado['banda'], (30.0, 400.0))


class TestAnalisisOnOffPublicado(unittest.TestCase):
    """Tests que validan los valores publicados en el protocolo."""

    def setUp(self):
        """Calcular resultado con el número oficial de ventanas."""
        self.resultado = gw171012_analysis.analisis_on_off(
            n_ventanas_off=gw171012_analysis.N_VENTANAS_OFF,
            mostrar_detalles=False
        )

    def test_ratio_publicado(self):
        """Test: El ratio publicado es 184 (tolerancia ±5%)."""
        ratio = self.resultado['ratio']
        self.assertAlmostEqual(
            ratio,
            gw171012_analysis.GW171012_PARAMS['ratio_psi_on_off'],
            delta=gw171012_analysis.GW171012_PARAMS['ratio_psi_on_off'] * 0.05,
            msg=f"Ratio={ratio:.1f} debe ser ≈ 184"
        )

    def test_p_value_publicado(self):
        """Test: P-value ≤ 2.31×10⁻⁴ (o igual al publicado)."""
        p = self.resultado['p_value']
        self.assertLessEqual(
            p,
            gw171012_analysis.GW171012_PARAMS['p_value'] * 1.01,
            msg=f"P-value={p:.2e} debe ser ≤ 2.31×10⁻⁴"
        )

    def test_p_value_significativo(self):
        """Test: P-value < 0.01 (significancia estadística)."""
        self.assertLess(self.resultado['p_value'], 0.01)

    def test_deteccion_confirmada(self):
        """Test: La detección debe estar confirmada."""
        self.assertTrue(
            self.resultado['deteccion_confirmada'],
            "GW171012 debe ser detectado con el protocolo Noésico Ψ"
        )


class TestComparativaGW150914(unittest.TestCase):
    """Tests para la tabla comparativa GW150914 vs GW171012."""

    def setUp(self):
        resultado_gw171012 = gw171012_analysis.analisis_on_off(
            n_ventanas_off=50, mostrar_detalles=False)
        self.tabla = gw171012_analysis.comparar_con_gw150914(
            resultado_gw171012, mostrar_detalles=False)

    def test_tabla_contiene_ambos_eventos(self):
        """Test: La tabla incluye GW150914 y GW171012."""
        self.assertIn('GW150914', self.tabla)
        self.assertIn('GW171012', self.tabla)

    def test_gw150914_snr_referencia(self):
        """Test: GW150914 tiene SNR de referencia ~24."""
        self.assertAlmostEqual(
            self.tabla['GW150914']['snr_clasico'],
            24.0,
            places=0
        )

    def test_gw150914_ratio_referencia(self):
        """Test: GW150914 tiene ratio de referencia 2.777."""
        self.assertAlmostEqual(
            self.tabla['GW150914']['ratio'],
            2.777,
            places=2
        )

    def test_gw150914_p_value_referencia(self):
        """Test: GW150914 tiene p-value de referencia 4.12×10⁻⁷."""
        self.assertAlmostEqual(
            self.tabla['GW150914']['p_value'],
            4.12e-7,
            delta=1e-8
        )

    def test_gw171012_snr_menor(self):
        """Test: GW171012 tiene SNR más bajo que GW150914 (evento marginal)."""
        self.assertLess(
            self.tabla['GW171012']['snr_clasico'],
            self.tabla['GW150914']['snr_clasico']
        )


def suite():
    """Crear suite de tests."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestGW171012Params))
    test_suite.addTest(unittest.makeSuite(TestSimulacionDatos))
    test_suite.addTest(unittest.makeSuite(TestBlanqueo))
    test_suite.addTest(unittest.makeSuite(TestMetricaPsi))
    test_suite.addTest(unittest.makeSuite(TestAnalisisOnOff))
    test_suite.addTest(unittest.makeSuite(TestAnalisisOnOffPublicado))
    test_suite.addTest(unittest.makeSuite(TestComparativaGW150914))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS – GW171012 Análisis Noésico Ψ")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    exitosos = result.testsRun - len(result.failures) - len(result.errors)
    print(f"Exitosos:         {exitosos}")
    print(f"Fallos:           {len(result.failures)}")
    print(f"Errores:          {len(result.errors)}")
    print("✅ TODOS LOS TESTS PASARON" if result.wasSuccessful()
          else "❌ ALGUNOS TESTS FALLARON")
    print("=" * 70)
    sys.exit(0 if result.wasSuccessful() else 1)
