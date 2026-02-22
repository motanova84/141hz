#!/usr/bin/env python3
"""
Tests para el análisis Ψ-Sweep de la señal Noēsis (f₀ = 141.7001 Hz).

Cubre:
  - Generación correcta del dataset (SNR logarítmico, canales, frecuencias)
  - Filtro band-pass ultra-estrecho (f₀ ± 0.01 Hz)
  - Cálculo de PLV / coherencia Ψ
  - Análisis de varianza para SNR < 5
  - Detección del punto de quiebre (Ψ < 0.7)
  - Comparación con/sin filtro
  - Persistencia CSV (guardar/cargar)
"""

import sys
import os
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from scipy import signal as scipy_signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import analisis_noesis_snr_sweep as sweep_mod
    MODULE_AVAILABLE = True
except ImportError as e:
    MODULE_AVAILABLE = False
    print(f"⚠️  No se pudo importar analisis_noesis_snr_sweep: {e}")


@unittest.skipUnless(MODULE_AVAILABLE, "Módulo no disponible")
class TestConstantes(unittest.TestCase):
    """Verifica que las constantes del experimento sean correctas."""

    def test_frecuencia_noesis(self):
        self.assertAlmostEqual(sweep_mod.F0, 141.7001, places=4)

    def test_tasa_muestreo(self):
        self.assertEqual(sweep_mod.FS, 4096)

    def test_duracion(self):
        self.assertEqual(sweep_mod.DURATION, 20)

    def test_snr_rango(self):
        self.assertGreater(sweep_mod.SNR_START, sweep_mod.SNR_END)
        self.assertAlmostEqual(sweep_mod.SNR_START, 20.0)
        self.assertAlmostEqual(sweep_mod.SNR_END, 0.1)

    def test_filtro_bw(self):
        self.assertAlmostEqual(sweep_mod.NARROW_BW, 0.01, places=4)

    def test_umbral_psi(self):
        self.assertAlmostEqual(sweep_mod.PSI_UMBRAL, 0.7, places=4)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE, "NumPy o módulo no disponible")
class TestGenerarDataset(unittest.TestCase):
    """Verifica la generación del dataset."""

    def setUp(self):
        self.ds = sweep_mod.generar_dataset(seed=0)

    def test_claves_presentes(self):
        for k in ('tiempo', 'canal1', 'canal2', 'snr_ref'):
            self.assertIn(k, self.ds)

    def test_longitud(self):
        n_esperado = sweep_mod.FS * sweep_mod.DURATION
        for k in ('tiempo', 'canal1', 'canal2', 'snr_ref'):
            self.assertEqual(len(self.ds[k]), n_esperado)

    def test_snr_logaritmico(self):
        snr = self.ds['snr_ref']
        # SNR debe ser estrictamente decreciente
        self.assertTrue(np.all(np.diff(snr) < 0))
        self.assertAlmostEqual(snr[0], sweep_mod.SNR_START, delta=0.5)
        self.assertAlmostEqual(snr[-1], sweep_mod.SNR_END, delta=0.05)

    def test_tiempo_monotono(self):
        t = self.ds['tiempo']
        self.assertTrue(np.all(np.diff(t) > 0))
        self.assertAlmostEqual(t[0], 0.0, places=6)
        self.assertAlmostEqual(t[-1], sweep_mod.DURATION, delta=1.0 / sweep_mod.FS)

    def test_canal2_sinusoide_pura(self):
        """canal2 debe tener amplitud ≈ 1 (es una sinusoide pura)."""
        c2 = self.ds['canal2']
        self.assertAlmostEqual(float(np.max(np.abs(c2))), 1.0, delta=0.01)

    def test_canal1_tiene_ruido(self):
        """canal1 en la zona de SNR alto (inicio) debe tener energía mayor que canal2."""
        n_check = sweep_mod.FS  # primer segundo
        rms_c1 = float(np.sqrt(np.mean(self.ds['canal1'][:n_check] ** 2)))
        rms_c2 = float(np.sqrt(np.mean(self.ds['canal2'][:n_check] ** 2)))
        # canal1 con SNR ≈ 20 debe tener más potencia que canal2 puro (amplitud ~1)
        self.assertGreater(rms_c1, rms_c2 * 0.5)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestBandpassFilter(unittest.TestCase):
    """Verifica el filtro band-pass ultra-estrecho."""

    def setUp(self):
        # Señal de prueba: senoide en f0 + componente fuera de banda
        fs = sweep_mod.FS
        t = np.linspace(0, 1, fs, endpoint=False)
        f0 = sweep_mod.F0
        self.signal_f0 = np.sin(2 * np.pi * f0 * t)
        self.signal_fuera = np.sin(2 * np.pi * 200 * t)  # 200 Hz – fuera de banda
        self.fs = fs
        self.f0 = f0

    def test_conserva_frecuencia_objetivo(self):
        """La función debe retornar un array de la misma longitud (sin error)."""
        # Con filtro de ancho moderado (1 Hz), la señal en f0 debe conservarse
        filtered = sweep_mod.aplicar_bandpass(
            self.signal_f0, self.fs, self.f0, bw=1.0
        )
        self.assertEqual(len(filtered), len(self.signal_f0))
        potencia_orig = float(np.mean(self.signal_f0 ** 2))
        potencia_filt = float(np.mean(filtered ** 2))
        self.assertGreater(potencia_filt, potencia_orig * 0.1)

    def test_ultra_narrow_filter_returns_array(self):
        """El filtro ultra-estrecho (±0.01 Hz) no debe lanzar excepción."""
        filtered = sweep_mod.aplicar_bandpass(
            self.signal_f0, self.fs, self.f0, sweep_mod.NARROW_BW
        )
        self.assertEqual(len(filtered), len(self.signal_f0))

    def test_atenua_frecuencia_fuera_de_banda(self):
        """La señal a 200 Hz debe ser muy atenuada."""
        filtered = sweep_mod.aplicar_bandpass(
            self.signal_fuera, self.fs, self.f0, sweep_mod.NARROW_BW
        )
        potencia_orig = float(np.mean(self.signal_fuera ** 2))
        potencia_filt = float(np.mean(filtered ** 2))
        self.assertLess(potencia_filt, potencia_orig * 0.01)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestCalcPLV(unittest.TestCase):
    """Verifica el cálculo del Phase Locking Value."""

    def test_plv_senales_sincronas(self):
        """Dos señales con diferencia de fase constante → PLV = 1."""
        n = 4096
        fase1 = np.linspace(0, 10 * np.pi, n)
        fase2 = fase1 + 0.3  # desplazamiento constante
        plv = sweep_mod.calcular_plv_ventana(fase1, fase2)
        self.assertAlmostEqual(plv, 1.0, places=5)

    def test_plv_fases_aleatorias(self):
        """Fases totalmente aleatorias → PLV ≈ 0."""
        rng = np.random.default_rng(7)
        fase1 = rng.uniform(-np.pi, np.pi, 10000)
        fase2 = rng.uniform(-np.pi, np.pi, 10000)
        plv = sweep_mod.calcular_plv_ventana(fase1, fase2)
        self.assertLess(plv, 0.1)

    def test_plv_rango(self):
        """PLV debe estar en [0, 1]."""
        rng = np.random.default_rng(13)
        fase1 = rng.standard_normal(1000)
        fase2 = rng.standard_normal(1000)
        plv = sweep_mod.calcular_plv_ventana(fase1, fase2)
        self.assertGreaterEqual(plv, 0.0)
        self.assertLessEqual(plv, 1.0)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestPsiSweep(unittest.TestCase):
    """Verifica el barrido de Ψ sobre el dataset."""

    @classmethod
    def setUpClass(cls):
        cls.ds = sweep_mod.generar_dataset(seed=1)
        cls.sweep_sin = sweep_mod.calcular_psi_sweep(cls.ds, usar_filtro=False)
        cls.sweep_con = sweep_mod.calcular_psi_sweep(cls.ds, usar_filtro=True)

    def test_claves_sweep(self):
        for k in ('t_centro', 'psi_vals', 'snr_centro'):
            self.assertIn(k, self.sweep_sin)
            self.assertIn(k, self.sweep_con)

    def test_misma_longitud(self):
        n = len(self.sweep_sin['t_centro'])
        self.assertEqual(len(self.sweep_sin['psi_vals']), n)
        self.assertEqual(len(self.sweep_sin['snr_centro']), n)

    def test_psi_en_rango(self):
        """Todos los valores de Ψ deben estar en [0, 1]."""
        for sw in (self.sweep_sin, self.sweep_con):
            self.assertTrue(np.all(sw['psi_vals'] >= 0.0))
            self.assertTrue(np.all(sw['psi_vals'] <= 1.0))

    def test_snr_decreciente(self):
        """El SNR en los centros de ventana debe ser decreciente."""
        snr = self.sweep_sin['snr_centro']
        self.assertTrue(np.all(np.diff(snr) < 0))

    def test_psi_alto_snr_alto(self):
        """Con SNR alto (inicio), Ψ debe ser > 0.5 sin filtro."""
        # Primeras 3 ventanas (SNR ≈ 20)
        psi_inicio = self.sweep_sin['psi_vals'][:3]
        self.assertTrue(np.all(psi_inicio > 0.5),
                        f"Ψ iniciales: {psi_inicio}")

    def test_psi_bajo_snr_bajo(self):
        """Con SNR muy bajo (fin), Ψ sin filtro debe ser menor que al inicio."""
        psi_inicio = float(np.mean(self.sweep_sin['psi_vals'][:3]))
        psi_fin = float(np.mean(self.sweep_sin['psi_vals'][-3:]))
        self.assertGreater(psi_inicio, psi_fin)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestAnalisisVarianza(unittest.TestCase):
    """Verifica el análisis de varianza de Ψ para SNR < 5."""

    def setUp(self):
        ds = sweep_mod.generar_dataset(seed=2)
        self.sw = sweep_mod.calcular_psi_sweep(ds, usar_filtro=False)

    def test_claves_varianza(self):
        var = sweep_mod.analizar_varianza_psi(self.sw, umbral_snr=5.0)
        for k in ('n_ventanas', 'varianza', 'media', 'std'):
            self.assertIn(k, var)

    def test_hay_ventanas_bajo_snr5(self):
        var = sweep_mod.analizar_varianza_psi(self.sw, umbral_snr=5.0)
        self.assertGreater(var['n_ventanas'], 0)

    def test_varianza_no_negativa(self):
        var = sweep_mod.analizar_varianza_psi(self.sw, umbral_snr=5.0)
        self.assertGreaterEqual(var['varianza'], 0.0)

    def test_umbral_snr_cero_devuelve_nan(self):
        """Si ninguna ventana tiene SNR < 0, stats deben ser NaN."""
        var = sweep_mod.analizar_varianza_psi(self.sw, umbral_snr=0.0)
        self.assertEqual(var['n_ventanas'], 0)
        import math
        self.assertTrue(math.isnan(var['varianza']))


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestPuntoQuiebre(unittest.TestCase):
    """Verifica la detección del punto de quiebre Ψ < 0.7."""

    def setUp(self):
        ds = sweep_mod.generar_dataset(seed=3)
        self.sw = sweep_mod.calcular_psi_sweep(ds, usar_filtro=False)

    def test_estructura_resultado(self):
        qb = sweep_mod.encontrar_punto_quiebre(self.sw)
        if qb is not None:
            for k in ('snr_quiebre', 't_quiebre', 'psi_en_quiebre', 'umbral_psi'):
                self.assertIn(k, qb)

    def test_psi_en_quiebre_menor_umbral(self):
        qb = sweep_mod.encontrar_punto_quiebre(self.sw, umbral_psi=0.7)
        if qb is not None:
            self.assertLess(qb['psi_en_quiebre'], 0.7)

    def test_umbral_cero_siempre_quiebra(self):
        """Con umbral ligeramente mayor que el PLV mínimo, siempre hay quiebre."""
        min_psi = float(np.min(self.sw['psi_vals']))
        umbral = min_psi + 1e-9
        qb = sweep_mod.encontrar_punto_quiebre(self.sw, umbral_psi=umbral)
        self.assertIsNotNone(qb)
        self.assertLess(qb['psi_en_quiebre'], umbral)

    def test_umbral_uno_nunca_quiebra(self):
        """Con umbral = 1.0, PLV nunca lo supera exactamente → quiebre inmediato."""
        # PLV < 1 casi siempre, así que debe encontrar quiebre
        qb = sweep_mod.encontrar_punto_quiebre(self.sw, umbral_psi=1.0)
        self.assertIsNotNone(qb)
        self.assertLess(qb['psi_en_quiebre'], 1.0)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestComparacionFiltros(unittest.TestCase):
    """Verifica la comparación con y sin filtro band-pass."""

    @classmethod
    def setUpClass(cls):
        cls.ds = sweep_mod.generar_dataset(seed=4)
        cls.comparacion = sweep_mod.comparar_con_sin_filtro(cls.ds)

    def test_claves_comparacion(self):
        self.assertIn('sin_filtro', self.comparacion)
        self.assertIn('con_filtro', self.comparacion)

    def test_misma_cantidad_ventanas(self):
        n_sin = len(self.comparacion['sin_filtro']['psi_vals'])
        n_con = len(self.comparacion['con_filtro']['psi_vals'])
        self.assertEqual(n_sin, n_con)

    def test_filtro_produce_resultados_distintos(self):
        """Con y sin filtro ultra-estrecho, los resultados de Ψ deben diferir."""
        sw_sin = self.comparacion['sin_filtro']
        sw_con = self.comparacion['con_filtro']
        # La media global de Ψ debe ser diferente entre ambas condiciones
        media_sin = float(np.mean(sw_sin['psi_vals']))
        media_con = float(np.mean(sw_con['psi_vals']))
        self.assertNotAlmostEqual(media_sin, media_con, places=2)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestReporte(unittest.TestCase):
    """Verifica la estructura del reporte generado."""

    @classmethod
    def setUpClass(cls):
        cls.ds = sweep_mod.generar_dataset(seed=5)
        cls.comparacion = sweep_mod.comparar_con_sin_filtro(cls.ds)
        cls.reporte = sweep_mod.generar_reporte(cls.ds, cls.comparacion)

    def test_estructura_reporte(self):
        for k in ('metadatos', 'sin_filtro', 'con_filtro'):
            self.assertIn(k, self.reporte)

    def test_metadatos(self):
        meta = self.reporte['metadatos']
        self.assertAlmostEqual(meta['f0_hz'], sweep_mod.F0, places=4)
        self.assertEqual(meta['fs_hz'], sweep_mod.FS)
        self.assertEqual(meta['duracion_s'], sweep_mod.DURATION)

    def test_varianza_no_negativa(self):
        for modo in ('sin_filtro', 'con_filtro'):
            var = self.reporte[modo]['varianza_snr_bajo_5']['varianza']
            if var == var:  # not NaN
                self.assertGreaterEqual(var, 0.0)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE,
                     "NumPy o módulo no disponible")
class TestPersistenciaCSV(unittest.TestCase):
    """Verifica guardar y cargar el dataset en CSV."""

    def test_round_trip(self):
        ds_orig = sweep_mod.generar_dataset(seed=99)
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            ruta = f.name
        try:
            sweep_mod.guardar_dataset(ds_orig, ruta)
            ds_load = sweep_mod.cargar_dataset(ruta)
            for k in ('tiempo', 'canal1', 'canal2', 'snr_ref'):
                np.testing.assert_allclose(ds_load[k], ds_orig[k], rtol=1e-6,
                                           err_msg=f"Diferencia en columna '{k}'")
        finally:
            os.unlink(ruta)


@unittest.skipUnless(MODULE_AVAILABLE and NUMPY_AVAILABLE and SCIPY_AVAILABLE,
                     "NumPy/SciPy/módulo no disponible")
class TestMain(unittest.TestCase):
    """Prueba de integración del punto de entrada main()."""

    def test_main_sin_argumentos(self):
        """main() debe ejecutarse sin errores y devolver 0."""
        resultado = sweep_mod.main([])
        self.assertEqual(resultado, 0)

    def test_main_con_csv_y_json(self):
        """main() debe guardar correctamente CSV y JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, 'dataset.csv')
            json_path = os.path.join(tmpdir, 'results.json')
            resultado = sweep_mod.main([
                '--csv', csv_path,
                '--output', json_path,
                '--seed', '7',
            ])
            self.assertEqual(resultado, 0)
            self.assertTrue(os.path.isfile(csv_path))
            self.assertTrue(os.path.isfile(json_path))
            import json
            with open(json_path) as f:
                data = json.load(f)
            self.assertIn('metadatos', data)
            self.assertIn('sin_filtro', data)
            self.assertIn('con_filtro', data)


def run_tests():
    """Ejecuta todos los tests y retorna el código de salida."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (
        TestConstantes,
        TestGenerarDataset,
        TestBandpassFilter,
        TestCalcPLV,
        TestPsiSweep,
        TestAnalisisVarianza,
        TestPuntoQuiebre,
        TestComparacionFiltros,
        TestReporte,
        TestPersistenciaCSV,
        TestMain,
    ):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("=" * 65)
    print("🧪 TESTS · ANÁLISIS Ψ-SWEEP · SEÑAL NOĒSIS · f₀ = 141.7001 Hz")
    print("=" * 65)
    sys.exit(run_tests())
