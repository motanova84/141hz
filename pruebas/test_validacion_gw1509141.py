#!/usr/bin/env python3
"""
Test Suite — Validación Profunda GW1509141
==========================================

Cobertura completa del módulo validar_evento_gw1509141:
  - Constantes
  - Simulación de chirp GW
  - Blanqueo (whitening)
  - Métrica Ψ por ventana
  - Serie temporal de Ψ
  - Estadísticas ON/OFF-source
  - SNR de red
  - Conexión Wang / octavas
  - Generación de reporte JSON
  - Certificado de validación (fórmula no saturante)
  - Banda de control anti-sesgo (TestRatioControl) [FIX 4]

50 tests en total.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import json
import math
import sys
import os
import tempfile
import unittest

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.validaciones.validar_evento_gw1509141 import (
    # constantes
    FS, T_TOTAL, T_WINDOW, T_MERGER, T_ON_HALF,
    F_LOW, F_HIGH, F_CONTROL, SEED, SELLO,
    # funciones
    generar_datos_evento,
    blanquear,
    calcular_psi_ventana,
    calcular_serie_psi,
    analizar_estadisticas,
    calcular_ratio_control,
    calcular_snr_red,
    conexion_wang_octavas,
    generar_reporte,
    generar_certificado_validacion,
)

import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _datos_evento():
    """Genera datos de evento con seed fijo para tests reproducibles."""
    return generar_datos_evento(seed=SEED)


def _blanquear_datos(datos):
    """Blanquea los datos del evento para tests."""
    h1_w = blanquear(datos["h1_strain"], FS, t_ref=datos["t"])
    l1_w = blanquear(datos["l1_strain"], FS, t_ref=datos["t"])
    return h1_w, l1_w


# ─────────────────────────────────────────────────────────────────────────────
# 1. TestConstantes
# ─────────────────────────────────────────────────────────────────────────────


class TestConstantes(unittest.TestCase):
    """Verifica que las constantes del módulo tienen valores esperados."""

    def test_f_control(self):
        self.assertAlmostEqual(F_CONTROL, 191.7001, places=4)

    def test_f_low(self):
        self.assertAlmostEqual(F_LOW, 35.0, places=3)

    def test_f_high(self):
        self.assertAlmostEqual(F_HIGH, 500.0, places=3)

    def test_t_on_half(self):
        self.assertAlmostEqual(T_ON_HALF, 4.25, places=3)

    def test_sello_no_vacio(self):
        self.assertIsInstance(SELLO, str)
        self.assertGreater(len(SELLO), 0)


# ─────────────────────────────────────────────────────────────────────────────
# 2. TestSimulacion
# ─────────────────────────────────────────────────────────────────────────────


class TestSimulacion(unittest.TestCase):
    """Verifica la simulación del evento GW1509141."""

    def setUp(self):
        self.datos = _datos_evento()

    def test_claves_presentes(self):
        for k in ("h1_strain", "l1_strain", "t", "signal"):
            self.assertIn(k, self.datos)

    def test_longitud_correcta(self):
        N_esperado = int(T_TOTAL * FS)
        self.assertEqual(len(self.datos["h1_strain"]), N_esperado)
        self.assertEqual(len(self.datos["l1_strain"]), N_esperado)

    def test_reproducibilidad(self):
        datos2 = generar_datos_evento(seed=SEED)
        np.testing.assert_array_equal(self.datos["h1_strain"], datos2["h1_strain"])

    def test_senal_no_trivial(self):
        # La señal (chirp) debe ser no trivial (no todo ceros)
        self.assertGreater(np.abs(self.datos["signal"]).max(), 0.1)


# ─────────────────────────────────────────────────────────────────────────────
# 3. TestBlanqueo
# ─────────────────────────────────────────────────────────────────────────────


class TestBlanqueo(unittest.TestCase):
    """Verifica la función de blanqueo (whitening)."""

    def setUp(self):
        datos = _datos_evento()
        self.h1_w = blanquear(datos["h1_strain"], FS, t_ref=datos["t"])
        self.l1_w = blanquear(datos["l1_strain"], FS, t_ref=datos["t"])
        self.h1_raw = datos["h1_strain"]

    def test_longitud_preservada(self):
        N = int(T_TOTAL * FS)
        self.assertEqual(len(self.h1_w), N)

    def test_rms_normalizado(self):
        rms = float(np.sqrt(np.mean(self.h1_w ** 2)))
        # Después del blanqueo, RMS debe ser ≈ 1
        self.assertAlmostEqual(rms, 1.0, delta=0.1)

    def test_salida_distinta_de_entrada(self):
        # El blanqueo debe modificar la señal
        self.assertFalse(np.allclose(self.h1_w, self.h1_raw))


# ─────────────────────────────────────────────────────────────────────────────
# 4. TestPsiVentana
# ─────────────────────────────────────────────────────────────────────────────


class TestPsiVentana(unittest.TestCase):
    """Verifica la métrica Ψ en una sola ventana."""

    def setUp(self):
        datos = _datos_evento()
        self.h1_w, self.l1_w = _blanquear_datos(datos)
        self.t = datos["t"]

    def test_rango_valido(self):
        # Tomar una ventana on-source (cerca del merger)
        i_merger = int((T_MERGER + T_TOTAL / 2) * FS)
        N_win = int(T_WINDOW * FS)
        h1_win = self.h1_w[i_merger: i_merger + N_win]
        l1_win = self.l1_w[i_merger: i_merger + N_win]
        psi = calcular_psi_ventana(h1_win, l1_win, FS)
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_banda_vacia_devuelve_cero(self):
        # Pedir una banda imposible
        N_win = int(T_WINDOW * FS)
        h1_win = self.h1_w[:N_win]
        l1_win = self.l1_w[:N_win]
        psi = calcular_psi_ventana(h1_win, l1_win, FS, f_low=1e6, f_high=2e6)
        self.assertAlmostEqual(psi, 0.0, places=5)

    def test_senales_identicas_dan_psi_1(self):
        rng = np.random.default_rng(42)
        N = int(T_WINDOW * FS)
        h = rng.standard_normal(N)
        psi = calcular_psi_ventana(h, h, FS)
        self.assertAlmostEqual(psi, 1.0, delta=1e-10)

    def test_ruido_puro_da_psi_bajo(self):
        rng = np.random.default_rng(99)
        N = int(T_WINDOW * FS)
        h1 = rng.standard_normal(N)
        l1 = rng.standard_normal(N)
        psi = calcular_psi_ventana(h1, l1, FS)
        # Para ruido no correlacionado, Ψ debe ser << 1
        self.assertLess(psi, 0.1)


# ─────────────────────────────────────────────────────────────────────────────
# 5. TestSeriePsi
# ─────────────────────────────────────────────────────────────────────────────


class TestSeriePsi(unittest.TestCase):
    """Verifica la serie temporal de Ψ."""

    def setUp(self):
        datos = _datos_evento()
        self.h1_w, self.l1_w = _blanquear_datos(datos)
        self.t = datos["t"]
        self.tc, self.psi = calcular_serie_psi(self.h1_w, self.l1_w, FS, self.t)

    def test_numero_ventanas(self):
        n_esperado = int(T_TOTAL / T_WINDOW)
        self.assertEqual(len(self.tc), n_esperado)

    def test_misma_longitud(self):
        self.assertEqual(len(self.tc), len(self.psi))

    def test_rango_psi(self):
        self.assertGreaterEqual(float(self.psi.min()), 0.0)
        self.assertLessEqual(float(self.psi.max()), 1.0)

    def test_psi_on_mayor_que_off(self):
        # Las ventanas on-source deben tener Ψ mayor que off-source en media
        on_mask = np.abs(self.tc - T_MERGER) <= T_ON_HALF
        off_mask = ~on_mask
        mean_on = float(np.mean(self.psi[on_mask]))
        mean_off = float(np.mean(self.psi[off_mask]))
        self.assertGreater(mean_on, mean_off)


# ─────────────────────────────────────────────────────────────────────────────
# 6. TestEstadisticas
# ─────────────────────────────────────────────────────────────────────────────


class TestEstadisticas(unittest.TestCase):
    """Verifica el análisis estadístico ON/OFF-source."""

    def setUp(self):
        datos = _datos_evento()
        h1_w, l1_w = _blanquear_datos(datos)
        tc, psi = calcular_serie_psi(h1_w, l1_w, FS, datos["t"])
        self.stats = analizar_estadisticas(tc, psi)

    def test_claves_presentes(self):
        for k in ("psi_on_mean", "psi_off_mean", "ratio_contraste",
                  "p_value", "separacion_significativa", "n_on", "n_off"):
            self.assertIn(k, self.stats)

    def test_n_on_correcto(self):
        # Número de ventanas on-source = int(2 * T_ON_HALF / T_WINDOW) + 1 aprox
        n_on_esperado = int(2 * T_ON_HALF / T_WINDOW) + 1
        self.assertAlmostEqual(self.stats["n_on"], n_on_esperado, delta=2)

    def test_ratio_significativo(self):
        # Con la simulación calibrada, el ratio debe ser > 5
        self.assertGreater(self.stats["ratio_contraste"], 5.0)

    def test_separacion_significativa(self):
        self.assertTrue(self.stats["separacion_significativa"])

    def test_psi_on_mayor_psi_off(self):
        self.assertGreater(self.stats["psi_on_mean"], self.stats["psi_off_mean"])


# ─────────────────────────────────────────────────────────────────────────────
# 7. TestSnrRed
# ─────────────────────────────────────────────────────────────────────────────


class TestSnrRed(unittest.TestCase):
    """Verifica el cálculo del SNR de red."""

    def setUp(self):
        datos = _datos_evento()
        h1_w, l1_w = _blanquear_datos(datos)
        self.tc, self.snr = calcular_snr_red(h1_w, l1_w, FS, datos["t"])

    def test_misma_longitud(self):
        self.assertEqual(len(self.tc), len(self.snr))

    def test_snr_positivo(self):
        self.assertTrue(np.all(self.snr >= 0.0))

    def test_snr_pico_en_region_on_source(self):
        idx_peak = int(np.argmax(self.snr))
        t_peak = self.tc[idx_peak]
        # El pico debe estar en la región on-source (alrededor del merger)
        self.assertLessEqual(abs(t_peak - T_MERGER), T_ON_HALF + T_WINDOW)


# ─────────────────────────────────────────────────────────────────────────────
# 8. TestWangOctavas
# ─────────────────────────────────────────────────────────────────────────────


class TestWangOctavas(unittest.TestCase):
    """Verifica el análisis de octavas multi-escala (Wang et al.)."""

    def setUp(self):
        datos = _datos_evento()
        h1_w, l1_w = _blanquear_datos(datos)
        self.wang = conexion_wang_octavas(h1_w, l1_w, FS)

    def test_claves_presentes(self):
        for k in ("octavas", "n_octavas", "psi_max_octava", "octava_pico"):
            self.assertIn(k, self.wang)

    def test_n_octavas_positivo(self):
        self.assertGreater(self.wang["n_octavas"], 0)

    def test_psi_max_en_rango(self):
        psi_max = self.wang["psi_max_octava"]
        self.assertGreaterEqual(psi_max, 0.0)
        self.assertLessEqual(psi_max, 1.0)

    def test_estructura_octava(self):
        for oct_data in self.wang["octavas"]:
            self.assertIn("octava", oct_data)
            self.assertIn("f_low_hz", oct_data)
            self.assertIn("psi", oct_data)


# ─────────────────────────────────────────────────────────────────────────────
# 9. TestReporte
# ─────────────────────────────────────────────────────────────────────────────


class TestReporte(unittest.TestCase):
    """Verifica la generación del reporte JSON."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        datos = _datos_evento()
        h1_w, l1_w = _blanquear_datos(datos)
        tc, psi = calcular_serie_psi(h1_w, l1_w, FS, datos["t"])
        stats_r = analizar_estadisticas(tc, psi)
        ctrl_r = calcular_ratio_control(h1_w, l1_w, FS, datos["t"])
        tc_snr, snr_s = calcular_snr_red(h1_w, l1_w, FS, datos["t"])
        wang_r = conexion_wang_octavas(h1_w, l1_w, FS)
        from pathlib import Path
        out_path = Path(self.tmp_dir) / "reporte_test.json"
        self.reporte = generar_reporte(
            stats_r, out_path,
            snr_result=(tc_snr, snr_s),
            wang_result=wang_r,
            ctrl_result=ctrl_r,
        )
        self.out_path = out_path

    def test_archivo_creado(self):
        self.assertTrue(self.out_path.exists())

    def test_estructura_base(self):
        for k in ("modulo", "evento", "timestamp", "fs_hz", "resultados_simulacion"):
            self.assertIn(k, self.reporte)

    def test_evento_correcto(self):
        self.assertEqual(self.reporte["evento"], "GW1509141")

    def test_control_band_presente(self):
        self.assertIn("control_band", self.reporte)
        cb = self.reporte["control_band"]
        self.assertIn("ratio_control", cb)
        self.assertIn("ratio_relativo", cb)

    def test_snr_red_presente(self):
        self.assertIn("snr_red", self.reporte)

    def test_wang_connection_presente(self):
        self.assertIn("wang_connection", self.reporte)


# ─────────────────────────────────────────────────────────────────────────────
# 10. TestCertificacion
# ─────────────────────────────────────────────────────────────────────────────


class TestCertificacion(unittest.TestCase):
    """
    Verifica la función generar_certificado_validacion con la nueva
    fórmula no saturante: psi_evento = psi_raw / (1 + psi_raw).
    """

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        # ratio = 0.96 / 0.046 ≈ 20.87 → psi_raw ≈ 4.568 → psi_evento ≈ 0.820 (EMERGENTE)
        self.reporte = {
            "modulo": "TEST",
            "evento": "GW-TEST",
            "timestamp": "2026-01-01T00:00:00+00:00",
            "resultados_simulacion": {
                "psi_on_mean": 0.96,
                "psi_off_mean": 0.046,
                "separacion_significativa": True,
                "p_value": 1e-5,
                "ratio_contraste": 0.96 / 0.046,
            },
        }
        from pathlib import Path
        self.cert = generar_certificado_validacion(
            self.reporte, Path(self.tmp_dir)
        )

    def test_estado_emergente(self):
        # ratio ≈ 20.87 → psi_evento ≈ 0.820 → EMERGENTE (no CRISTALIZADO)
        self.assertEqual(self.cert["estado"], "EMERGENTE")

    def test_psi_evento_formula(self):
        # Verificar que la fórmula es psi_raw / (1 + psi_raw)
        ratio = 0.96 / 0.046
        psi_raw = math.sqrt(ratio)
        psi_ev_esperado = psi_raw / (1.0 + psi_raw)
        self.assertAlmostEqual(self.cert["psi_evento_mapeado"], psi_ev_esperado,
                               places=4)

    def test_campos_auditables_presentes(self):
        for k in ("ratio_on_off", "psi_raw", "psi_evento_mapeado",
                  "ratio_control", "ratio_relativo"):
            self.assertIn(k, self.cert)

    def test_hash_sha256_presente(self):
        self.assertIn("hash_sha256", self.cert)
        self.assertEqual(len(self.cert["hash_sha256"]), 64)

    def test_sello_correcto(self):
        self.assertEqual(self.cert["sello"], SELLO)

    def test_ratio_on_off_correcto(self):
        ratio_esperado = 0.96 / 0.046
        self.assertAlmostEqual(self.cert["ratio_on_off"], ratio_esperado, delta=0.01)


# ─────────────────────────────────────────────────────────────────────────────
# 11. TestRatioControl  [FIX 4 — banda de control anti-sesgo]
# ─────────────────────────────────────────────────────────────────────────────


class TestRatioControl(unittest.TestCase):
    """Verifica la banda de control anti-sesgo (Fix 4)."""

    def setUp(self):
        datos = generar_datos_evento()
        h1_w = blanquear(datos["h1_strain"], FS, t_ref=datos["t"])
        l1_w = blanquear(datos["l1_strain"], FS, t_ref=datos["t"])
        self.ctrl = calcular_ratio_control(h1_w, l1_w, FS, datos["t"])

    def test_claves_presentes(self):
        for k in ("f_control_hz", "ratio_control", "psi_on_ctrl", "psi_off_ctrl"):
            self.assertIn(k, self.ctrl)

    def test_frecuencia_control(self):
        self.assertAlmostEqual(self.ctrl["f_control_hz"], F_CONTROL, places=4)

    def test_ratio_control_finito(self):
        rc = self.ctrl["ratio_control"]
        self.assertTrue(math.isfinite(rc))
        self.assertGreater(rc, 0.0)

    def test_psi_on_ctrl_en_rango(self):
        psi_on = self.ctrl["psi_on_ctrl"]
        self.assertGreaterEqual(psi_on, 0.0)
        self.assertLessEqual(psi_on, 1.0)

    def test_psi_off_ctrl_en_rango(self):
        psi_off = self.ctrl["psi_off_ctrl"]
        self.assertGreaterEqual(psi_off, 0.0)
        self.assertLessEqual(psi_off, 1.0)

    def test_n_on_n_off_correctos(self):
        # n_on + n_off debe coincidir con el total de ventanas
        n_total = int(T_TOTAL / T_WINDOW)
        n_ventanas = self.ctrl["n_on_ctrl"] + self.ctrl["n_off_ctrl"]
        self.assertAlmostEqual(n_ventanas, n_total, delta=2)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    unittest.main(verbosity=2)
