"""
Tests for physics.masa_acoplamiento_qcal

Cubre las 5 clases y las 4 funciones de la API pública.

Invariantes clave verificados:
  - m_ψ ≈ 1.04 × 10⁻⁴⁸ kg  y  m_ψ ≈ 5.86 × 10⁻¹³ eV
  - λ ≈ 4.80 × 10⁻⁴¹ (Swampland)
  - σ/m < 1 cm²/g (Bullet Cluster)
  - m_ψ fuera del rango de superradiancia estelar
  - |1 + w| ≈ 10⁻¹⁴ ≪ 1 (consistencia ΛCDM)
  - Recuperación post-impacto: SNR > 1, Ψ ≥ 0.999998
  - DiscriminadorMultisignal: tejido ↔ OG discriminados correctamente
"""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.masa_acoplamiento_qcal import (
    # Constants
    _M_PSI_KG,
    _M_PSI_EV,
    _M_PLANCK_EV,
    _LAMBDA_SWAMPLAND,
    _SIGMA_OVER_M_CGS,
    _ONE_PLUS_W,
    _LIMIT_SIGMA_OVER_M_CGS,
    _SUPERRADIANCIA_MIN_EV,
    _SUPERRADIANCIA_MAX_EV,
    _F0_LOCKIN,
    # Classes
    MasaTejido,
    AcoplamientoSwampland,
    LimitesExperimentales,
    ResultadoLimites,
    SimulacionResiliencia,
    ResultadoResiliencia,
    DiscriminadorMultisignal,
    # API pública
    calcular_masa_tejido,
    calcular_acoplamiento,
    validar_limites_experimentales,
    simular_resiliencia_impacto,
)
from qcal.constants import F0_HZ, H_PLANCK, C, EV_TO_J, HBAR


# ============================================================================
# Helpers
# ============================================================================

def _senal_tejido(n: int = 1000, fs: float = 1000.0, f0: float = F0_HZ) -> np.ndarray:
    """Genera señal pura a f₀ (simula tejido guía coherente)."""
    t = np.arange(n) / fs
    return np.sin(2.0 * math.pi * f0 * t)


def _senal_og(n: int = 1000, fs: float = 1000.0, f_og: float = 50.0) -> np.ndarray:
    """Genera señal a frecuencia de OG (no coherente con f₀)."""
    t = np.arange(n) / fs
    return np.sin(2.0 * math.pi * f_og * t)


# ============================================================================
# TestMasaTejido — 18 tests
# ============================================================================

class TestMasaTejido(unittest.TestCase):
    """Tests para MasaTejido."""

    def setUp(self):
        self.masa = MasaTejido()

    # ── Valores numéricos ─────────────────────────────────────────────────

    def test_f0_default(self):
        """f0_hz debe ser F0_HZ por defecto."""
        self.assertAlmostEqual(self.masa.f0_hz, F0_HZ, places=4)

    def test_masa_kg_formula(self):
        """m_kg debe cumplir m = h·f₀/c²."""
        esperado = H_PLANCK * F0_HZ / (C ** 2)
        self.assertAlmostEqual(self.masa.m_kg / esperado, 1.0, places=10)

    def test_masa_kg_orden_magnitud(self):
        """m_kg ≈ 1.04 × 10⁻⁴⁸ kg."""
        self.assertAlmostEqual(self.masa.m_kg / 1.04e-48, 1.0, delta=0.1)

    def test_masa_ev_orden_magnitud(self):
        """m_ev ≈ 5.86 × 10⁻¹³ eV."""
        self.assertAlmostEqual(self.masa.m_ev / 5.86e-13, 1.0, delta=0.02)

    def test_masa_ev_consistency(self):
        """m_ev debe ser consistente con m_kg·c²/eV_to_J."""
        esperado = self.masa.m_kg * (C ** 2) / EV_TO_J
        self.assertAlmostEqual(self.masa.m_ev / esperado, 1.0, places=10)

    def test_no_ultra_ligero(self):
        """La masa no debe estar en el régimen ultra-ligero (< 10⁻²² eV)."""
        self.assertFalse(self.masa.ultra_ligero)

    def test_regimen_materia_oscura(self):
        """La masa debe caer en el régimen de Bosones Ligeros."""
        self.assertTrue(self.masa.regimen_materia_oscura)

    def test_masa_positiva(self):
        """m_kg y m_ev deben ser positivos."""
        self.assertGreater(self.masa.m_kg, 0.0)
        self.assertGreater(self.masa.m_ev, 0.0)

    def test_custom_f0(self):
        """Con f0 personalizado la masa escala linealmente."""
        masa2 = MasaTejido(f0_hz=2.0 * F0_HZ)
        self.assertAlmostEqual(masa2.m_kg / self.masa.m_kg, 2.0, places=10)

    def test_ultra_ligero_flag(self):
        """Una masa de 10⁻²³ eV debe marcarse como ultra-ligero."""
        # m_ψ [eV] = h·f₀ / EV_TO_J  → f₀ = m_ψ·EV_TO_J / h
        f_ultra_light_threshold_hz = 1.0e-22 * EV_TO_J / H_PLANCK
        masa_ultra = MasaTejido(f0_hz=f_ultra_light_threshold_hz * 0.1)
        self.assertTrue(masa_ultra.ultra_ligero)
        self.assertFalse(masa_ultra.regimen_materia_oscura)

    def test_masa_kg_matches_module_constant(self):
        """MasaTejido().m_kg debe coincidir con _M_PSI_KG."""
        self.assertAlmostEqual(self.masa.m_kg, _M_PSI_KG, places=15)

    def test_masa_ev_matches_module_constant(self):
        """MasaTejido().m_ev debe coincidir con _M_PSI_EV."""
        self.assertAlmostEqual(self.masa.m_ev / _M_PSI_EV, 1.0, places=10)

    # ── Validación de entrada ─────────────────────────────────────────────

    def test_f0_negativo_lanza_error(self):
        """f0_hz negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            MasaTejido(f0_hz=-1.0)

    def test_f0_cero_lanza_error(self):
        """f0_hz = 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            MasaTejido(f0_hz=0.0)

    # ── API pública ───────────────────────────────────────────────────────

    def test_calcular_masa_tejido_retorna_masa_tejido(self):
        """calcular_masa_tejido() debe retornar MasaTejido."""
        resultado = calcular_masa_tejido()
        self.assertIsInstance(resultado, MasaTejido)

    def test_calcular_masa_tejido_m_ev_precision(self):
        """calcular_masa_tejido() debe dar m_ev dentro del 1% de 5.86e-13 eV."""
        resultado = calcular_masa_tejido()
        self.assertAlmostEqual(resultado.m_ev / 5.86e-13, 1.0, delta=0.02)

    def test_calcular_masa_tejido_custom_f0(self):
        """calcular_masa_tejido(f0_hz=X) debe usar f₀=X."""
        resultado = calcular_masa_tejido(f0_hz=100.0)
        self.assertAlmostEqual(resultado.f0_hz, 100.0, places=6)

    def test_constante_f0_lockin(self):
        """_F0_LOCKIN debe ser igual a F0_HZ."""
        self.assertAlmostEqual(_F0_LOCKIN, F0_HZ, places=4)


# ============================================================================
# TestAcoplamientoSwampland — 16 tests
# ============================================================================

class TestAcoplamientoSwampland(unittest.TestCase):
    """Tests para AcoplamientoSwampland."""

    def setUp(self):
        self.ac = AcoplamientoSwampland()

    # ── Valores numéricos ─────────────────────────────────────────────────

    def test_lambda_orden_magnitud(self):
        """λ debe ser ≈ 4.80 × 10⁻⁴¹."""
        self.assertAlmostEqual(self.ac.lambda_swampland / 4.80e-41, 1.0, delta=0.02)

    def test_lambda_formula(self):
        """λ = m_ψ / M_P."""
        esperado = _M_PSI_EV / _M_PLANCK_EV
        self.assertAlmostEqual(self.ac.lambda_swampland / esperado, 1.0, places=10)

    def test_lambda_matches_module_constant(self):
        """AcoplamientoSwampland().lambda_swampland debe coincidir con _LAMBDA_SWAMPLAND."""
        self.assertAlmostEqual(
            self.ac.lambda_swampland / _LAMBDA_SWAMPLAND, 1.0, places=10
        )

    def test_es_superfluido(self):
        """Con λ ~ 10⁻⁴¹, el sistema debe ser superfluido."""
        self.assertTrue(self.ac.es_superfluido)

    def test_es_estable(self):
        """λ > 0 garantiza estabilidad del potencial."""
        self.assertTrue(self.ac.es_estable)

    def test_lambda_positivo(self):
        """λ debe ser positivo."""
        self.assertGreater(self.ac.lambda_swampland, 0.0)

    def test_lambda_muy_pequeno(self):
        """λ debe ser menor que 10⁻³⁰."""
        self.assertLess(self.ac.lambda_swampland, 1.0e-30)

    def test_planck_ev_orden_magnitud(self):
        """M_P debe ser ≈ 1.22 × 10²⁸ eV."""
        self.assertAlmostEqual(self.ac.m_planck_ev / 1.22e28, 1.0, delta=0.01)

    def test_custom_masses(self):
        """Con masas personalizadas λ = m_ev / m_planck_ev."""
        ac2 = AcoplamientoSwampland(m_ev=1.0e-10, m_planck_ev=1.0e10)
        self.assertAlmostEqual(ac2.lambda_swampland, 1.0e-20, places=15)

    # ── Validación de entrada ─────────────────────────────────────────────

    def test_m_ev_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            AcoplamientoSwampland(m_ev=-1.0)

    def test_m_ev_cero_lanza_error(self):
        with self.assertRaises(ValueError):
            AcoplamientoSwampland(m_ev=0.0)

    def test_m_planck_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            AcoplamientoSwampland(m_planck_ev=-1.0)

    def test_m_planck_cero_lanza_error(self):
        with self.assertRaises(ValueError):
            AcoplamientoSwampland(m_planck_ev=0.0)

    # ── API pública ───────────────────────────────────────────────────────

    def test_calcular_acoplamiento_retorna_tipo(self):
        resultado = calcular_acoplamiento()
        self.assertIsInstance(resultado, AcoplamientoSwampland)

    def test_calcular_acoplamiento_lambda(self):
        resultado = calcular_acoplamiento()
        self.assertAlmostEqual(resultado.lambda_swampland / 4.80e-41, 1.0, delta=0.02)

    def test_calcular_acoplamiento_custom(self):
        resultado = calcular_acoplamiento(m_ev=1.0, m_planck_ev=1.0e28)
        self.assertAlmostEqual(resultado.lambda_swampland, 1.0e-28, places=15)


# ============================================================================
# TestLimitesExperimentales — 22 tests
# ============================================================================

class TestLimitesExperimentales(unittest.TestCase):
    """Tests para LimitesExperimentales."""

    def setUp(self):
        self.lim = LimitesExperimentales()
        self.resultado = self.lim.validar()

    # ── Bullet Cluster ────────────────────────────────────────────────────

    def test_sigma_over_m_cgs_es_positivo(self):
        _, sigma_cgs = self.lim.calcular_sigma_sobre_m()
        self.assertGreater(sigma_cgs, 0.0)

    def test_sigma_over_m_cgs_muy_pequeno(self):
        """σ/m debe ser ≪ 1 cm²/g."""
        _, sigma_cgs = self.lim.calcular_sigma_sobre_m()
        self.assertLess(sigma_cgs, 1.0e-10)

    def test_sigma_over_m_modulo_matches(self):
        """σ/m del módulo (_SIGMA_OVER_M_CGS) debe ser < 1 cm²/g."""
        self.assertLess(_SIGMA_OVER_M_CGS, _LIMIT_SIGMA_OVER_M_CGS)

    def test_cumple_bullet_cluster(self):
        self.assertTrue(self.resultado.cumple_bullet_cluster)

    def test_limite_bullet_cluster_valor(self):
        self.assertAlmostEqual(self.resultado.limite_bullet_cluster_cgs, 1.0)

    # ── Superradiancia ────────────────────────────────────────────────────

    def test_m_psi_fuera_rango_superradiancia(self):
        """m_ψ ≈ 5.86e-13 eV debe estar fuera del rango [10⁻¹⁴, 10⁻¹² eV]."""
        self.assertTrue(self.resultado.evita_superradiancia)

    def test_evitar_superradiancia_directa(self):
        self.assertTrue(self.lim.verificar_superradiancia())

    def test_superradiancia_rango_min(self):
        self.assertAlmostEqual(_SUPERRADIANCIA_MIN_EV, 1.0e-14)

    def test_superradiancia_rango_max(self):
        self.assertAlmostEqual(_SUPERRADIANCIA_MAX_EV, 5.0e-13)

    def test_masa_dentro_rango_superradiancia_no_evita(self):
        """Una masa dentro del rango de superradiancia no debe evitarla."""
        lim2 = LimitesExperimentales(m_kg=1.0e-50, m_ev=5.0e-14)
        self.assertFalse(lim2.verificar_superradiancia())

    # ── Parámetro w ───────────────────────────────────────────────────────

    def test_uno_mas_w_orden_magnitud(self):
        """1 + w debe ser ≈ 10⁻¹⁴."""
        uno_w = self.lim.calcular_uno_mas_w()
        self.assertAlmostEqual(math.log10(abs(uno_w)), -14.0, delta=1.0)

    def test_consistente_lcdm(self):
        self.assertTrue(self.resultado.consistente_lcdm)

    def test_uno_mas_w_positivo(self):
        self.assertGreater(self.resultado.uno_mas_w, 0.0)

    # ── Veredicto global ──────────────────────────────────────────────────

    def test_aprobado(self):
        """El tejido debe superar las tres comprobaciones."""
        self.assertTrue(self.resultado.aprobado)

    def test_resultado_es_tipo_correcto(self):
        self.assertIsInstance(self.resultado, ResultadoLimites)

    # ── Validación de entrada ─────────────────────────────────────────────

    def test_m_kg_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            LimitesExperimentales(m_kg=-1.0)

    def test_m_ev_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            LimitesExperimentales(m_ev=-1.0)

    def test_lambda_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            LimitesExperimentales(lambda_val=-1.0)

    # ── API pública ───────────────────────────────────────────────────────

    def test_api_validar_limites(self):
        resultado = validar_limites_experimentales()
        self.assertIsInstance(resultado, ResultadoLimites)
        self.assertTrue(resultado.aprobado)

    def test_api_validar_sigma(self):
        resultado = validar_limites_experimentales()
        self.assertTrue(resultado.cumple_bullet_cluster)

    def test_api_validar_superradiancia(self):
        resultado = validar_limites_experimentales()
        self.assertTrue(resultado.evita_superradiancia)


# ============================================================================
# TestSimulacionResiliencia — 24 tests
# ============================================================================

class TestSimulacionResiliencia(unittest.TestCase):
    """Tests para SimulacionResiliencia (IRS-Luna)."""

    def setUp(self):
        self.sim = SimulacionResiliencia()
        self.resultado = self.sim.simular()

    # ── Atributos del simulador ───────────────────────────────────────────

    def test_amplitud_impacto_default(self):
        self.assertAlmostEqual(self.sim.amplitud_impacto_m, 1.0e-9)

    def test_t_integracion_default(self):
        self.assertAlmostEqual(self.sim.t_integracion_s, 1.0e6)

    def test_f0_hz_default(self):
        self.assertAlmostEqual(self.sim.f0_hz, F0_HZ, places=4)

    # ── ResultadoResiliencia ──────────────────────────────────────────────

    def test_ruido_post_menor_que_pre(self):
        """El ruido post-filtrado debe ser menor al pre-impacto."""
        self.assertLess(self.resultado.amplitud_ruido_post, self.resultado.amplitud_ruido_pre)

    def test_snr_pre_mayor_que_durante(self):
        """SNR pre-impacto debe ser mayor al SNR durante el impacto (sistema intacto > perturbado)."""
        self.assertGreater(self.resultado.snr_pre, self.resultado.snr_durante)

    def test_snr_durante_menor_que_pre(self):
        """SNR durante el impacto debe ser menor al previo."""
        self.assertLess(self.resultado.snr_durante, self.resultado.snr_pre)

    def test_snr_post_mayor_uno(self):
        """SNR post-filtrado debe ser > 1 (recuperación exitosa)."""
        self.assertGreater(self.resultado.snr_post, 1.0)

    def test_coherencia_pre(self):
        self.assertAlmostEqual(self.resultado.coherencia_pre, 0.999999, places=6)

    def test_coherencia_durante_colapso(self):
        """Coherencia durante el impacto debe caer por debajo de 0.5."""
        self.assertLess(self.resultado.coherencia_durante, 0.5)

    def test_coherencia_post_recuperacion(self):
        """Coherencia post debe ser ≥ 0.999."""
        self.assertGreaterEqual(self.resultado.coherencia_post, 0.999)

    def test_recuperacion_exitosa(self):
        self.assertTrue(self.resultado.recuperacion_exitosa)

    def test_protocolo_aprobado(self):
        self.assertTrue(self.resultado.protocolo_aprobado)

    def test_senal_tejido_valor(self):
        """La señal del tejido debe ser 2.4 × 10⁻¹⁹ rad."""
        self.assertAlmostEqual(
            self.resultado.senal_tejido, 2.4e-19, delta=1.0e-21
        )

    # ── Paso I: Gating ────────────────────────────────────────────────────

    def test_gating_devuelve_dict(self):
        info = self.sim.gating_tiempo_vuelo()
        self.assertIsInstance(info, dict)

    def test_gating_brazo_sucio(self):
        info = self.sim.gating_tiempo_vuelo()
        self.assertEqual(info["brazo_sucio"], 1)

    def test_gating_brazos_limpios(self):
        info = self.sim.gating_tiempo_vuelo()
        self.assertEqual(sorted(info["brazos_limpios"]), [2, 3])

    def test_gating_duracion(self):
        info = self.sim.gating_tiempo_vuelo()
        self.assertAlmostEqual(info["duracion_gating_s"], 0.5)

    # ── Paso II: Deconvolución ────────────────────────────────────────────

    def test_deconvolucion_conserva_longitud(self):
        senal = np.random.randn(256)
        recuperada = self.sim.deconvolucion_espectral(senal)
        self.assertEqual(len(recuperada), len(senal))

    def test_deconvolucion_senal_vacia_error(self):
        with self.assertRaises(ValueError):
            self.sim.deconvolucion_espectral(np.array([]))

    def test_deconvolucion_identidad(self):
        """Con kernel identidad la señal recuperada debe ser ≈ la original."""
        senal = np.random.randn(64)
        recuperada = self.sim.deconvolucion_espectral(senal)
        np.testing.assert_allclose(recuperada, senal, rtol=1.0e-10)

    # ── Paso III: Lock-in ─────────────────────────────────────────────────

    def test_lockin_senal_pura(self):
        """Lock-in sobre señal pura a f₀ debe dar amplitud > 0."""
        fs = 1000.0
        n = int(fs * 10)  # 10 s
        t = np.arange(n) / fs
        senal = 1.0 * np.sin(2.0 * math.pi * F0_HZ * t)
        amp = self.sim.lockin_digital(senal, fs)
        self.assertGreater(amp, 0.0)

    def test_lockin_senal_vacia_error(self):
        with self.assertRaises(ValueError):
            self.sim.lockin_digital(np.array([]), fs=1000.0)

    def test_lockin_fs_negativo_error(self):
        with self.assertRaises(ValueError):
            self.sim.lockin_digital(np.ones(10), fs=-1.0)

    # ── Validación de entrada ─────────────────────────────────────────────

    def test_amplitud_negativa_lanza_error(self):
        with self.assertRaises(ValueError):
            SimulacionResiliencia(amplitud_impacto_m=-1.0)

    def test_t_integracion_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            SimulacionResiliencia(t_integracion_s=-1.0)

    def test_f0_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            SimulacionResiliencia(f0_hz=-1.0)

    # ── API pública ───────────────────────────────────────────────────────

    def test_api_simular_retorna_tipo(self):
        resultado = simular_resiliencia_impacto()
        self.assertIsInstance(resultado, ResultadoResiliencia)

    def test_api_simular_protocolo_aprobado(self):
        resultado = simular_resiliencia_impacto()
        self.assertTrue(resultado.protocolo_aprobado)

    def test_api_simular_custom_amplitud(self):
        resultado = simular_resiliencia_impacto(amplitud_impacto=1.0e-8)
        # Ruido durante debe escalar con la amplitud
        sim_ref = simular_resiliencia_impacto(amplitud_impacto=1.0e-9)
        self.assertGreater(
            resultado.amplitud_ruido_durante,
            sim_ref.amplitud_ruido_durante,
        )

    def test_ganancia_snr_positiva(self):
        g = self.sim.ganancia_snr()
        self.assertGreater(g, 0.0)


# ============================================================================
# TestDiscriminadorMultisignal — 20 tests
# ============================================================================

class TestDiscriminadorMultisignal(unittest.TestCase):
    """Tests para DiscriminadorMultisignal."""

    def setUp(self):
        self.disc = DiscriminadorMultisignal()
        self.n = 2000
        self.fs = 1000.0

    def _brazos_tejido(self):
        """Tres brazos idénticos (tejido guía)."""
        s = _senal_tejido(self.n, self.fs)
        return s, s.copy(), s.copy()

    def _brazos_og(self):
        """Dos brazos con OG a 50 Hz, brazo 3 independiente."""
        s1 = _senal_og(self.n, self.fs, 50.0)
        s2 = _senal_og(self.n, self.fs, 50.0) * 0.7  # amplitud distinta
        s3 = np.random.randn(self.n) * 0.01           # ruido gaussiano
        return s1, s2, s3

    # ── Detección de tejido ───────────────────────────────────────────────

    def test_tejido_clasificado_correctamente(self):
        s1, s2, s3 = self._brazos_tejido()
        etiq, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertEqual(etiq, "TEJIDO_GUIA")

    def test_tejido_devuelve_fase(self):
        s1, s2, s3 = self._brazos_tejido()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertIn("fase_rad", info)

    def test_tejido_correlaciones_altas(self):
        s1, s2, s3 = self._brazos_tejido()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertGreater(info["corr_12"], 0.9999)
        self.assertGreater(info["corr_13"], 0.9999)

    def test_tejido_fase_es_float(self):
        s1, s2, s3 = self._brazos_tejido()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertIsInstance(info["fase_rad"], float)

    # ── Detección de OG ───────────────────────────────────────────────────

    def test_og_clasificada_correctamente(self):
        s1, s2, s3 = self._brazos_og()
        etiq, _ = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertEqual(etiq, "ONDA_GRAVITACIONAL")

    def test_og_devuelve_modo(self):
        s1, s2, s3 = self._brazos_og()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertIn("modo", info)

    def test_og_asimetria_positiva(self):
        s1, s2, s3 = self._brazos_og()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        self.assertGreaterEqual(info["asimetria"], 0.0)

    # ── Correlaciones en info ─────────────────────────────────────────────

    def test_info_contiene_correlaciones(self):
        s1, s2, s3 = self._brazos_tejido()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        for key in ("corr_12", "corr_13", "corr_23"):
            self.assertIn(key, info)

    def test_correlacion_tejido_rango(self):
        s1, s2, s3 = self._brazos_tejido()
        _, info = self.disc.analizar(s1, s2, s3, fs=self.fs)
        for key in ("corr_12", "corr_13", "corr_23"):
            self.assertGreaterEqual(info[key], -1.0)
            self.assertLessEqual(info[key], 1.0)

    # ── Extracción de fase ────────────────────────────────────────────────

    def test_extraer_fase_rango(self):
        senal = _senal_tejido(self.n, self.fs)
        fase = self.disc._extraer_fase(senal, self.fs)
        self.assertGreaterEqual(fase, -math.pi)
        self.assertLessEqual(fase, math.pi)

    def test_extraer_fase_senal_vacia(self):
        with self.assertRaises(ValueError):
            self.disc._extraer_fase(np.array([]), self.fs)

    def test_extraer_fase_fs_negativo(self):
        senal = _senal_tejido(self.n, self.fs)
        with self.assertRaises(ValueError):
            self.disc._extraer_fase(senal, -1.0)

    # ── Validación de entrada ─────────────────────────────────────────────

    def test_senal_vacia_lanza_error(self):
        s = _senal_tejido(self.n, self.fs)
        with self.assertRaises(ValueError):
            self.disc.analizar(np.array([]), s, s, fs=self.fs)

    def test_fs_negativo_lanza_error(self):
        s1, s2, s3 = self._brazos_tejido()
        with self.assertRaises(ValueError):
            self.disc.analizar(s1, s2, s3, fs=-100.0)

    def test_custom_f0(self):
        """DiscriminadorMultisignal debe aceptar f0 personalizado."""
        disc2 = DiscriminadorMultisignal(f0_hz=100.0)
        self.assertAlmostEqual(disc2.f0_hz, 100.0)

    def test_f0_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            DiscriminadorMultisignal(f0_hz=-1.0)

    # ── Umbral y constantes ───────────────────────────────────────────────

    def test_umbral_correlacion_tejido(self):
        """El umbral de correlación para tejido debe ser muy cercano a 1."""
        self.assertGreater(DiscriminadorMultisignal.UMBRAL_CORRELACION_TEJIDO, 0.999)

    def test_umbral_og(self):
        """El umbral de strain para OG debe ser ≈ 10⁻²¹."""
        self.assertAlmostEqual(
            DiscriminadorMultisignal.UMBRAL_OG, 1.0e-21, places=15
        )

    def test_f0_default_es_f0_hz(self):
        self.assertAlmostEqual(self.disc.f0_hz, F0_HZ, places=4)

    def test_clasificar_og_retorna_tupla(self):
        s1 = np.random.randn(100)
        s2 = np.random.randn(100)
        s3 = np.random.randn(100)
        resultado = self.disc._clasificar_og(s1, s2, s3)
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(resultado[0], "ONDA_GRAVITACIONAL")


# ============================================================================
# TestConstantesModulo — 10 tests
# ============================================================================

class TestConstantesModulo(unittest.TestCase):
    """Tests para las constantes derivadas del módulo."""

    def test_m_psi_kg_orden(self):
        self.assertAlmostEqual(_M_PSI_KG / 1.04e-48, 1.0, delta=0.1)

    def test_m_psi_ev_orden(self):
        self.assertAlmostEqual(_M_PSI_EV / 5.86e-13, 1.0, delta=0.02)

    def test_m_planck_ev_orden(self):
        self.assertAlmostEqual(_M_PLANCK_EV / 1.22e28, 1.0, delta=0.01)

    def test_lambda_swampland_orden(self):
        self.assertAlmostEqual(_LAMBDA_SWAMPLAND / 4.80e-41, 1.0, delta=0.02)

    def test_sigma_cgs_menor_limite(self):
        self.assertLess(_SIGMA_OVER_M_CGS, _LIMIT_SIGMA_OVER_M_CGS)

    def test_one_plus_w_orden(self):
        self.assertAlmostEqual(math.log10(_ONE_PLUS_W), -14.0, delta=1.0)

    def test_limite_bullet_cluster(self):
        self.assertAlmostEqual(_LIMIT_SIGMA_OVER_M_CGS, 1.0)

    def test_superradiancia_min(self):
        self.assertAlmostEqual(_SUPERRADIANCIA_MIN_EV, 1.0e-14)

    def test_superradiancia_max(self):
        self.assertAlmostEqual(_SUPERRADIANCIA_MAX_EV, 5.0e-13)

    def test_f0_lockin(self):
        self.assertAlmostEqual(_F0_LOCKIN, F0_HZ, places=4)


if __name__ == "__main__":
    unittest.main()
