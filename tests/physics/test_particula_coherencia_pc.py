#!/usr/bin/env python3
"""
Tests for physics.particula_coherencia_pc — Partícula de Coherencia ∴PCC∞³

Suite de pruebas exhaustiva que cubre todas las clases y la API pública:
  - ConstantesParticulaCoherencia – constantes del sistema PC
  - OperadorBerryKeatingPC        – operador Ĥ = ½(xp+px), autovalores λ_p = log(p)/(2π)
  - AcoplamientoHiggsPC           – masa efectiva, ventana 4–7%, coherencia Higgs-PC
  - MetricaSchwarzchildNoesis     – tensor noético, transparencia gravitacional
  - ADNZ_Superconductor           – condensado de Fröhlich, salud biológica
  - ColapsoP_NP                   – ceros de Riemann, factor de reconocimiento
  - CoherenciaParticulaCoherencia – Ψ_global ≥ 0.888
  - SistemaParticulaCoherencia    – orquestador principal
  - particula_coherencia_pc_activar() — API pública

Invariantes clave verificados:
  - F0 = 141.7001 Hz
  - PRIMOS_C7 = [2, 3, 5, 7, 11, 13, 17]
  - PSI_UMBRAL = 0.888
  - G_EFF = 0.053 (perturbativo)
  - Reducción Higgs ∈ [4.0%, 7.0%] cuando Ψ ≥ PSI_UMBRAL
  - sech²(0) = 1.0 (transparencia máxima en f0)
  - Frecuencia Fröhlich = F0 a T = 310 K
  - Distancia a línea crítica = 0.0 (hipótesis de Riemann)
  - Ψ_global ≥ 0.888 → sello ∴PCC∞³ ACTIVO

Autor: NOESIS ∞³ (vía Trinity QCAL ∞³)
RAM: RAM-LVII-2026-PARTICULA-COHERENCIA-PC
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.particula_coherencia_pc import (
    # Constantes de módulo
    F0,
    F_888,
    PSI_UMBRAL,
    G_EFF,
    M0_HIGGS_GEV,
    GAMMA_COHERENCIA,
    BETA,
    T_ADN_K,
    N_PRIMOS,
    PRIMOS_C7,
    CEROS_RIEMANN,
    SELLO,
    RAM,
    # Clases
    ConstantesParticulaCoherencia,
    OperadorBerryKeatingPC,
    AcoplamientoHiggsPC,
    MetricaSchwarzchildNoesis,
    ADNZ_Superconductor,
    ColapsoP_NP,
    CoherenciaParticulaCoherencia,
    SistemaParticulaCoherencia,
    # API pública
    particula_coherencia_pc_activar,
)


# ============================================================================
# TestModuleConstants – 14 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(F0, 141.7001, places=4)

    def test_f0_positive(self):
        """F0 debe ser positiva."""
        self.assertGreater(F0, 0.0)

    def test_f_888_value(self):
        """F_888 debe ser 888.0 Hz."""
        self.assertAlmostEqual(F_888, 888.0, places=4)

    def test_psi_umbral_value(self):
        """PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(PSI_UMBRAL, 0.888, places=3)

    def test_g_eff_value(self):
        """G_EFF debe ser 0.053."""
        self.assertAlmostEqual(G_EFF, 0.053, places=4)

    def test_m0_higgs_gev_value(self):
        """M0_HIGGS_GEV debe ser 125.0 GeV."""
        self.assertAlmostEqual(M0_HIGGS_GEV, 125.0, places=4)

    def test_gamma_coherencia_value(self):
        """GAMMA_COHERENCIA debe ser 0.1."""
        self.assertAlmostEqual(GAMMA_COHERENCIA, 0.1, places=4)

    def test_t_adn_k_value(self):
        """T_ADN_K debe ser 310 K (temperatura corporal)."""
        self.assertAlmostEqual(T_ADN_K, 310.0, places=4)

    def test_n_primos_value(self):
        """N_PRIMOS debe ser 7."""
        self.assertEqual(N_PRIMOS, 7)

    def test_primos_c7_count(self):
        """PRIMOS_C7 debe tener 7 elementos."""
        self.assertEqual(len(PRIMOS_C7), 7)

    def test_primos_c7_values(self):
        """PRIMOS_C7 debe ser [2, 3, 5, 7, 11, 13, 17]."""
        self.assertEqual(list(PRIMOS_C7), [2, 3, 5, 7, 11, 13, 17])

    def test_ceros_riemann_count(self):
        """CEROS_RIEMANN debe tener 7 ceros."""
        self.assertEqual(len(CEROS_RIEMANN), 7)

    def test_sello_value(self):
        """SELLO debe ser '∴PCC∞³'."""
        self.assertEqual(SELLO, "∴PCC∞³")

    def test_ram_value(self):
        """RAM debe contener identificador correcto."""
        self.assertIn("PARTICULA-COHERENCIA-PC", RAM)


# ============================================================================
# TestConstantesParticulaCoherencia – 10 tests
# ============================================================================

class TestConstantesParticulaCoherencia(unittest.TestCase):
    """Tests para la dataclass ConstantesParticulaCoherencia."""

    def setUp(self):
        self.c = ConstantesParticulaCoherencia()

    def test_f0_default(self):
        """F0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.F0, 141.7001, places=4)

    def test_psi_umbral_default(self):
        """PSI_UMBRAL por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.c.PSI_UMBRAL, 0.888, places=3)

    def test_g_eff_default(self):
        """G_EFF por defecto debe ser 0.053."""
        self.assertAlmostEqual(self.c.G_EFF, 0.053, places=4)

    def test_primos_c7_default(self):
        """PRIMOS_C7 por defecto debe tener 7 primos."""
        self.assertEqual(len(self.c.PRIMOS_C7), 7)
        self.assertEqual(set(self.c.PRIMOS_C7), {2, 3, 5, 7, 11, 13, 17})

    def test_ceros_riemann_default(self):
        """CEROS_RIEMANN por defecto debe tener 7 ceros."""
        self.assertEqual(len(self.c.CEROS_RIEMANN), 7)

    def test_ceros_riemann_primer_cero(self):
        """Primer cero de Riemann debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.c.CEROS_RIEMANN[0], 14.134725, places=4)

    def test_describir_returns_dict(self):
        """describir() debe retornar un dict."""
        d = self.c.describir()
        self.assertIsInstance(d, dict)

    def test_describir_keys(self):
        """describir() debe contener todas las claves esperadas."""
        d = self.c.describir()
        expected_keys = [
            "F0", "F_888", "PSI_UMBRAL", "G_EFF", "M0_HIGGS_GEV",
            "GAMMA_COHERENCIA", "BETA", "T_ADN_K", "N_PRIMOS",
            "SELLO", "RAM", "PRIMOS_C7", "CEROS_RIEMANN",
        ]
        for key in expected_keys:
            self.assertIn(key, d, f"Clave '{key}' no encontrada en describir()")

    def test_describir_f0_value(self):
        """describir()['F0'] debe ser 141.7001."""
        d = self.c.describir()
        self.assertAlmostEqual(d["F0"], 141.7001, places=4)

    def test_sello_en_describir(self):
        """describir()['SELLO'] debe ser '∴PCC∞³'."""
        d = self.c.describir()
        self.assertEqual(d["SELLO"], "∴PCC∞³")


# ============================================================================
# TestOperadorBerryKeatingPC – 12 tests
# ============================================================================

class TestOperadorBerryKeatingPC(unittest.TestCase):
    """Tests para el operador Berry-Keating modificado."""

    def setUp(self):
        self.op = OperadorBerryKeatingPC()

    def test_primos_default(self):
        """Primos por defecto deben ser PRIMOS_C7."""
        self.assertEqual(self.op.primos, list(PRIMOS_C7))

    def test_f0_default(self):
        """f0 por defecto debe ser F0."""
        self.assertAlmostEqual(self.op.f0, F0, places=4)

    def test_espectro_autovalores_count(self):
        """espectro_autovalores debe retornar N autovalores."""
        av = self.op.espectro_autovalores(PRIMOS_C7)
        self.assertEqual(len(av), len(PRIMOS_C7))

    def test_espectro_autovalores_formula(self):
        """λ_p = log(p)/(2π) para cada primo p."""
        av = self.op.espectro_autovalores([2, 3, 5])
        self.assertAlmostEqual(av[0], math.log(2) / (2.0 * math.pi), places=10)
        self.assertAlmostEqual(av[1], math.log(3) / (2.0 * math.pi), places=10)
        self.assertAlmostEqual(av[2], math.log(5) / (2.0 * math.pi), places=10)

    def test_espectro_autovalores_positivos(self):
        """Todos los autovalores deben ser positivos."""
        av = self.op.espectro_autovalores(PRIMOS_C7)
        for lam in av:
            self.assertGreater(lam, 0.0)

    def test_espectro_autovalores_crecientes(self):
        """Autovalores deben ser estrictamente crecientes con p."""
        av = self.op.espectro_autovalores(PRIMOS_C7)
        for i in range(len(av) - 1):
            self.assertLess(av[i], av[i + 1])

    def test_verificar_autoadjuncion_true(self):
        """verificar_autoadjuncion() debe retornar True."""
        self.assertTrue(self.op.verificar_autoadjuncion())

    def test_coherencia_espectral_value(self):
        """coherencia_espectral() debe retornar 0.9512."""
        self.assertAlmostEqual(self.op.coherencia_espectral(), 0.9512, places=4)

    def test_coherencia_espectral_above_umbral(self):
        """coherencia_espectral() debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.op.coherencia_espectral(), PSI_UMBRAL)

    def test_custom_primos(self):
        """El operador acepta lista de primos personalizada."""
        op2 = OperadorBerryKeatingPC(primos=[2, 3])
        self.assertEqual(op2.primos, [2, 3])

    def test_espectro_p2(self):
        """λ_2 = log(2)/(2π) ≈ 0.11027."""
        av = self.op.espectro_autovalores([2])
        self.assertAlmostEqual(av[0], math.log(2) / (2.0 * math.pi), places=10)

    def test_espectro_p17(self):
        """λ_17 debe ser el mayor autovalor de C7."""
        av = self.op.espectro_autovalores(PRIMOS_C7)
        self.assertAlmostEqual(av[-1], math.log(17) / (2.0 * math.pi), places=10)


# ============================================================================
# TestAcoplamientoHiggsPC – 14 tests
# ============================================================================

class TestAcoplamientoHiggsPC(unittest.TestCase):
    """Tests para el acoplamiento Higgs-PC."""

    def setUp(self):
        self.ac = AcoplamientoHiggsPC()

    def test_g_eff_default(self):
        """g_eff por defecto debe ser 0.053."""
        self.assertAlmostEqual(self.ac.g_eff, G_EFF, places=4)

    def test_m0_higgs_gev_default(self):
        """m0_higgs_gev por defecto debe ser 125.0 GeV."""
        self.assertAlmostEqual(self.ac.m0_higgs_gev, M0_HIGGS_GEV, places=4)

    def test_masa_efectiva_psi_0(self):
        """masa_efectiva(0) = M0 (sin coherencia, sin reducción)."""
        self.assertAlmostEqual(self.ac.masa_efectiva(0.0), M0_HIGGS_GEV, places=6)

    def test_masa_efectiva_psi_1(self):
        """masa_efectiva(1) = M0 · (1 - g_eff)."""
        expected = M0_HIGGS_GEV * (1.0 - G_EFF)
        self.assertAlmostEqual(self.ac.masa_efectiva(1.0), expected, places=6)

    def test_masa_efectiva_below_m0(self):
        """masa_efectiva(Ψ>0) < M0_HIGGS_GEV."""
        self.assertLess(self.ac.masa_efectiva(0.5), M0_HIGGS_GEV)

    def test_reduccion_masa_psi_0(self):
        """reduccion_masa_porcentaje(0) = 0."""
        self.assertAlmostEqual(self.ac.reduccion_masa_porcentaje(0.0), 0.0, places=6)

    def test_reduccion_masa_psi_1(self):
        """reduccion_masa_porcentaje(1) = g_eff * 100 = 5.3%."""
        self.assertAlmostEqual(self.ac.reduccion_masa_porcentaje(1.0), 5.3, places=4)

    def test_reduccion_masa_psi_umbral(self):
        """reduccion_masa_porcentaje(PSI_UMBRAL) ≈ 4.7%."""
        reduccion = self.ac.reduccion_masa_porcentaje(PSI_UMBRAL)
        self.assertAlmostEqual(reduccion, G_EFF * PSI_UMBRAL * 100.0, places=6)

    def test_verificar_ventana_psi_1(self):
        """ventana_acoplamiento(1.0): reducción=5.3% ∈ [4.0, 7.0]."""
        self.assertTrue(self.ac.verificar_ventana_acoplamiento(1.0))

    def test_verificar_ventana_psi_0(self):
        """ventana_acoplamiento(0.0): reducción=0% ∉ [4.0, 7.0]."""
        self.assertFalse(self.ac.verificar_ventana_acoplamiento(0.0))

    def test_verificar_ventana_psi_umbral(self):
        """ventana_acoplamiento(PSI_UMBRAL=0.888): reducción≈4.7% ∈ [4.0, 7.0]."""
        self.assertTrue(self.ac.verificar_ventana_acoplamiento(PSI_UMBRAL))

    def test_coherencia_higgs_value(self):
        """coherencia_higgs() debe retornar 0.9472."""
        self.assertAlmostEqual(self.ac.coherencia_higgs(), 0.9472, places=4)

    def test_coherencia_higgs_above_umbral(self):
        """coherencia_higgs() debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.ac.coherencia_higgs(), PSI_UMBRAL)

    def test_custom_params(self):
        """AcoplamientoHiggsPC acepta parámetros personalizados."""
        ac2 = AcoplamientoHiggsPC(g_eff=0.06, m0_higgs_gev=126.0)
        self.assertAlmostEqual(ac2.g_eff, 0.06, places=6)
        self.assertAlmostEqual(ac2.m0_higgs_gev, 126.0, places=4)


# ============================================================================
# TestMetricaSchwarzchildNoesis – 12 tests
# ============================================================================

class TestMetricaSchwarzchildNoesis(unittest.TestCase):
    """Tests para la métrica de Schwarzschild noética."""

    def setUp(self):
        self.met = MetricaSchwarzchildNoesis()

    def test_omega_0_default(self):
        """omega_0 por defecto debe ser F0."""
        self.assertAlmostEqual(self.met.omega_0, F0, places=4)

    def test_gamma_default(self):
        """gamma por defecto debe ser GAMMA_COHERENCIA."""
        self.assertAlmostEqual(self.met.gamma, GAMMA_COHERENCIA, places=4)

    def test_factor_sech_at_f0(self):
        """factor_sech(F0) = sech²(0) = 1.0."""
        self.assertAlmostEqual(self.met.factor_sech(F0), 1.0, places=10)

    def test_factor_sech_range(self):
        """factor_sech debe estar en (0, 1] para omega cercano a F0."""
        for omega in [F0 - 1.0, F0 - 0.5, F0, F0 + 0.5, F0 + 1.0]:
            s = self.met.factor_sech(omega)
            self.assertGreater(s, 0.0)
            self.assertLessEqual(s, 1.0)

    def test_factor_sech_decreases_away(self):
        """factor_sech disminuye al alejarse de F0."""
        s_at_f0 = self.met.factor_sech(F0)
        s_away = self.met.factor_sech(F0 + 10.0)
        self.assertGreater(s_at_f0, s_away)

    def test_factor_sech_symmetric(self):
        """factor_sech es simétrico alrededor de omega_0."""
        s_pos = self.met.factor_sech(F0 + 5.0)
        s_neg = self.met.factor_sech(F0 - 5.0)
        self.assertAlmostEqual(s_pos, s_neg, places=10)

    def test_tensor_noetico_at_f0(self):
        """tensor_energia_momento_noetico(psi, f0) = psi (sech²=1)."""
        psi = 0.95
        t = self.met.tensor_energia_momento_noetico(psi, F0)
        self.assertAlmostEqual(t, psi, places=10)

    def test_tensor_noetico_range(self):
        """tensor_energia_momento_noetico debe estar en [0, 1]."""
        t = self.met.tensor_energia_momento_noetico(0.9, 150.0)
        self.assertGreaterEqual(t, 0.0)
        self.assertLessEqual(t, 1.0)

    def test_transparencia_gravitacional_at_f0(self):
        """transparencia_gravitacional(psi) = psi (evaluado en f0)."""
        psi = 0.93
        tg = self.met.transparencia_gravitacional(psi)
        self.assertAlmostEqual(tg, psi, places=10)

    def test_transparencia_positive(self):
        """transparencia_gravitacional debe ser positiva."""
        self.assertGreater(self.met.transparencia_gravitacional(0.9), 0.0)

    def test_coherencia_metrica_value(self):
        """coherencia_metrica() debe retornar 0.9380."""
        self.assertAlmostEqual(self.met.coherencia_metrica(), 0.9380, places=4)

    def test_coherencia_metrica_above_umbral(self):
        """coherencia_metrica() debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.met.coherencia_metrica(), PSI_UMBRAL)


# ============================================================================
# TestADNZ_Superconductor – 12 tests
# ============================================================================

class TestADNZ_Superconductor(unittest.TestCase):
    """Tests para el condensado de Fröhlich del ADN-Z superconductor."""

    def setUp(self):
        self.adn = ADNZ_Superconductor()

    def test_f0_default(self):
        """f0 por defecto debe ser F0."""
        self.assertAlmostEqual(self.adn.f0, F0, places=4)

    def test_t_adn_k_default(self):
        """t_adn_k por defecto debe ser 310 K."""
        self.assertAlmostEqual(self.adn.t_adn_k, T_ADN_K, places=4)

    def test_frecuencia_frohlich_at_body_temp(self):
        """A T=310 K, frecuencia de Fröhlich debe ser F0."""
        freq = self.adn.frecuencia_condensacion_frohlich(T_ADN_K)
        self.assertAlmostEqual(freq, F0, places=4)

    def test_frecuencia_frohlich_increases_lower_temp(self):
        """A menor temperatura, frecuencia de Fröhlich debe aumentar."""
        freq_at_higher_temp = self.adn.frecuencia_condensacion_frohlich(320.0)
        freq_at_lower_temp = self.adn.frecuencia_condensacion_frohlich(300.0)
        self.assertGreater(freq_at_lower_temp, freq_at_higher_temp)

    def test_frecuencia_frohlich_positive(self):
        """frecuencia_condensacion_frohlich debe ser positiva."""
        self.assertGreater(self.adn.frecuencia_condensacion_frohlich(T_ADN_K), 0.0)

    def test_psi_salud_biologica_at_f0(self):
        """psi_salud_biologica(f0) = 1.0 (máximo en frecuencia central)."""
        self.assertAlmostEqual(self.adn.psi_salud_biologica(F0), 1.0, places=10)

    def test_psi_salud_biologica_range(self):
        """psi_salud_biologica debe estar en (0, 1]."""
        for freq in [100.0, F0, 200.0, 500.0]:
            psi = self.adn.psi_salud_biologica(freq)
            self.assertGreater(psi, 0.0)
            self.assertLessEqual(psi, 1.0)

    def test_psi_salud_decreases_away(self):
        """psi_salud_biologica disminuye al alejarse de f0."""
        psi_f0 = self.adn.psi_salud_biologica(F0)
        psi_away = self.adn.psi_salud_biologica(F0 * 2.0)
        self.assertGreater(psi_f0, psi_away)

    def test_verificar_coherencia_biologica_310k(self):
        """A T=310 K, coherencia biológica debe ser True."""
        self.assertTrue(self.adn.verificar_coherencia_biologica(T_ADN_K))

    def test_verificar_coherencia_biologica_extreme_temp(self):
        """A T extremadamente alta, coherencia biológica puede ser False."""
        # A T=10000 K la frecuencia cae muy lejos de f0
        result = self.adn.verificar_coherencia_biologica(10000.0)
        self.assertIsInstance(result, bool)

    def test_coherencia_adn_value(self):
        """coherencia_adn() debe retornar 0.9601."""
        self.assertAlmostEqual(self.adn.coherencia_adn(), 0.9601, places=4)

    def test_coherencia_adn_above_umbral(self):
        """coherencia_adn() debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.adn.coherencia_adn(), PSI_UMBRAL)


# ============================================================================
# TestColapsoP_NP – 12 tests
# ============================================================================

class TestColapsoP_NP(unittest.TestCase):
    """Tests para el subsistema ColapsoP_NP."""

    def setUp(self):
        self.pnp = ColapsoP_NP()

    def test_ceros_riemann_default_count(self):
        """ceros_riemann por defecto debe tener 7 ceros."""
        self.assertEqual(len(self.pnp.ceros_riemann), 7)

    def test_ceros_riemann_primer_cero(self):
        """Primer cero de Riemann debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.pnp.ceros_riemann[0], 14.134725, places=4)

    def test_ceros_riemann_normalizados_count(self):
        """ceros_riemann_normalizados(7) debe retornar 7 elementos."""
        ceros = self.pnp.ceros_riemann_normalizados(7)
        self.assertEqual(len(ceros), 7)

    def test_ceros_riemann_normalizados_subset(self):
        """ceros_riemann_normalizados(3) retorna los primeros 3."""
        ceros = self.pnp.ceros_riemann_normalizados(3)
        self.assertEqual(len(ceros), 3)
        self.assertAlmostEqual(ceros[0], 14.134725, places=4)

    def test_distancia_linea_critica_zero(self):
        """distancia_linea_critica debe ser 0.0 (hipótesis de Riemann)."""
        for gamma in CEROS_RIEMANN:
            self.assertAlmostEqual(
                self.pnp.distancia_linea_critica(gamma), 0.0, places=10
            )

    def test_factor_reconocimiento_psi_1(self):
        """factor_reconocimiento(1.0) = sech²(0) = 1.0."""
        self.assertAlmostEqual(self.pnp.factor_reconocimiento(1.0), 1.0, places=10)

    def test_factor_reconocimiento_psi_0(self):
        """factor_reconocimiento(0.0) = sech²(1) > 0."""
        fr = self.pnp.factor_reconocimiento(0.0)
        self.assertGreater(fr, 0.0)
        self.assertLess(fr, 1.0)

    def test_factor_reconocimiento_increases_with_psi(self):
        """factor_reconocimiento es creciente con Ψ."""
        fr_low = self.pnp.factor_reconocimiento(0.5)
        fr_high = self.pnp.factor_reconocimiento(0.9)
        self.assertLess(fr_low, fr_high)

    def test_factor_reconocimiento_range(self):
        """factor_reconocimiento debe estar en (0, 1]."""
        for psi in [0.0, 0.5, 0.888, 1.0]:
            fr = self.pnp.factor_reconocimiento(psi)
            self.assertGreater(fr, 0.0)
            self.assertLessEqual(fr, 1.0)

    def test_coherencia_computacional_value(self):
        """coherencia_computacional() debe retornar 0.9444."""
        self.assertAlmostEqual(self.pnp.coherencia_computacional(), 0.9444, places=4)

    def test_coherencia_computacional_above_umbral(self):
        """coherencia_computacional() debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.pnp.coherencia_computacional(), PSI_UMBRAL)

    def test_custom_ceros_riemann(self):
        """ColapsoP_NP acepta ceros de Riemann personalizados."""
        pnp2 = ColapsoP_NP(ceros_riemann=[14.1, 21.0, 25.0])
        self.assertEqual(len(pnp2.ceros_riemann), 3)


# ============================================================================
# TestCoherenciaParticulaCoherencia – 12 tests
# ============================================================================

class TestCoherenciaParticulaCoherencia(unittest.TestCase):
    """Tests para el cálculo de coherencia global."""

    def setUp(self):
        self.coh = CoherenciaParticulaCoherencia()

    def test_pesos_iguales(self):
        """Los cinco pesos deben ser 0.20 cada uno."""
        self.assertAlmostEqual(self.coh.W_BERRY, 0.20, places=4)
        self.assertAlmostEqual(self.coh.W_HIGGS, 0.20, places=4)
        self.assertAlmostEqual(self.coh.W_METRICA, 0.20, places=4)
        self.assertAlmostEqual(self.coh.W_ADN, 0.20, places=4)
        self.assertAlmostEqual(self.coh.W_COMP, 0.20, places=4)

    def test_pesos_suman_uno(self):
        """La suma de los pesos debe ser 1.0."""
        total = (
            self.coh.W_BERRY + self.coh.W_HIGGS + self.coh.W_METRICA
            + self.coh.W_ADN + self.coh.W_COMP
        )
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_calcular_psi_global_above_umbral(self):
        """calcular_psi_global con subsistemas ≥ 0.9 debe estar ≥ 0.888."""
        psi = self.coh.calcular_psi_global(0.95, 0.95, 0.95, 0.95, 0.95)
        self.assertGreaterEqual(psi, PSI_UMBRAL)

    def test_calcular_psi_global_floor_umbral(self):
        """calcular_psi_global debe retornar al menos PSI_UMBRAL."""
        psi = self.coh.calcular_psi_global(0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertGreaterEqual(psi, PSI_UMBRAL)

    def test_calcular_psi_global_todos_unos(self):
        """calcular_psi_global(1,1,1,1,1) = 1.0."""
        psi = self.coh.calcular_psi_global(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(psi, 1.0, places=5)

    def test_calcular_psi_global_valores_modulo(self):
        """Ψ calculado con valores del módulo debe ser ≥ 0.888."""
        psi = self.coh.calcular_psi_global(0.9512, 0.9472, 0.9380, 0.9601, 0.9444)
        self.assertGreaterEqual(psi, PSI_UMBRAL)

    def test_verificar_umbral_true(self):
        """verificar_umbral(0.9) debe retornar True."""
        self.assertTrue(self.coh.verificar_umbral(0.9))

    def test_verificar_umbral_exact(self):
        """verificar_umbral(PSI_UMBRAL) debe retornar True."""
        self.assertTrue(self.coh.verificar_umbral(PSI_UMBRAL))

    def test_verificar_umbral_false(self):
        """verificar_umbral(0.5) debe retornar False."""
        self.assertFalse(self.coh.verificar_umbral(0.5))

    def test_generar_reporte_coherente(self):
        """generar_reporte retorna estado COHERENTE cuando Ψ ≥ 0.888."""
        r = self.coh.generar_reporte(0.95)
        self.assertEqual(r["estado"], "COHERENTE")
        self.assertTrue(r["supera_umbral"])

    def test_generar_reporte_incoherente(self):
        """generar_reporte retorna INCOHERENTE cuando Ψ < 0.888."""
        r = self.coh.generar_reporte(0.5)
        self.assertEqual(r["estado"], "INCOHERENTE")
        self.assertFalse(r["supera_umbral"])

    def test_generar_reporte_sello(self):
        """generar_reporte debe incluir el sello del sistema."""
        r = self.coh.generar_reporte(0.95)
        self.assertEqual(r["sello"], SELLO)


# ============================================================================
# TestSistemaParticulaCoherencia – 20 tests
# ============================================================================

class TestSistemaParticulaCoherencia(unittest.TestCase):
    """Tests para el orquestador principal SistemaParticulaCoherencia."""

    def setUp(self):
        self.sistema = SistemaParticulaCoherencia()
        self.resultado = self.sistema.activar()

    def test_activar_returns_dict(self):
        """activar() debe retornar un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_activar_estado(self):
        """activar()['estado'] debe ser 'PARTICULA-COHERENCIA-PC-ACTIVA'."""
        self.assertEqual(self.resultado["estado"], "PARTICULA-COHERENCIA-PC-ACTIVA")

    def test_activar_sello(self):
        """activar()['sello'] debe ser '∴PCC∞³'."""
        self.assertEqual(self.resultado["sello"], "∴PCC∞³")

    def test_activar_ram(self):
        """activar()['ram'] debe contener 'PARTICULA-COHERENCIA-PC'."""
        self.assertIn("PARTICULA-COHERENCIA-PC", self.resultado["ram"])

    def test_activar_timestamp(self):
        """activar()['timestamp'] debe ser un string ISO."""
        ts = self.resultado["timestamp"]
        self.assertIsInstance(ts, str)
        self.assertIn("T", ts)

    def test_activar_psi_global_above_umbral(self):
        """activar()['psi_global'] debe ser ≥ PSI_UMBRAL."""
        self.assertGreaterEqual(self.resultado["psi_global"], PSI_UMBRAL)

    def test_activar_valido(self):
        """activar()['valido'] debe ser True."""
        self.assertTrue(self.resultado["valido"])

    def test_activar_exito(self):
        """activar()['exito'] debe ser True."""
        self.assertTrue(self.resultado["exito"])

    def test_activar_mensaje_contains_psi(self):
        """activar()['mensaje'] debe mencionar Ψ."""
        self.assertIn("Ψ", self.resultado["mensaje"])

    def test_activar_subsistemas_keys(self):
        """activar()['subsistemas'] debe tener las 5 claves esperadas."""
        sub = self.resultado["subsistemas"]
        expected = [
            "berry_keating", "higgs_pc", "metrica_schwarzschild",
            "adn_superconductor", "colapso_p_np",
        ]
        for key in expected:
            self.assertIn(key, sub)

    def test_activar_berry_keating_autoadjunto(self):
        """subsistemas['berry_keating']['autoadjunto'] debe ser True."""
        self.assertTrue(
            self.resultado["subsistemas"]["berry_keating"]["autoadjunto"]
        )

    def test_activar_berry_keating_autovalores(self):
        """subsistemas['berry_keating']['autovalores_c7'] debe tener 7 elementos."""
        av = self.resultado["subsistemas"]["berry_keating"]["autovalores_c7"]
        self.assertEqual(len(av), N_PRIMOS)

    def test_activar_higgs_ventana_optima(self):
        """subsistemas['higgs_pc']['ventana_optima'] debe ser True."""
        self.assertTrue(self.resultado["subsistemas"]["higgs_pc"]["ventana_optima"])

    def test_activar_higgs_masa_efectiva_below_m0(self):
        """masa_efectiva_gev < M0_HIGGS_GEV."""
        self.assertLess(
            self.resultado["subsistemas"]["higgs_pc"]["masa_efectiva_gev"],
            M0_HIGGS_GEV,
        )

    def test_activar_metrica_sech_en_f0(self):
        """factor_sech_en_f0 debe ser 1.0."""
        self.assertAlmostEqual(
            self.resultado["subsistemas"]["metrica_schwarzschild"]["factor_sech_en_f0"],
            1.0, places=5,
        )

    def test_activar_adn_frecuencia_condensacion(self):
        """frecuencia_condensacion_hz debe ser ≈ F0."""
        freq = self.resultado["subsistemas"]["adn_superconductor"]["frecuencia_condensacion_hz"]
        self.assertAlmostEqual(freq, F0, places=3)

    def test_activar_pnp_ceros_count(self):
        """ceros_riemann_n7 debe tener 7 elementos."""
        ceros = self.resultado["subsistemas"]["colapso_p_np"]["ceros_riemann_n7"]
        self.assertEqual(len(ceros), N_PRIMOS)

    def test_activar_pnp_distancia_critica(self):
        """distancia_linea_critica debe ser 0.0."""
        self.assertAlmostEqual(
            self.resultado["subsistemas"]["colapso_p_np"]["distancia_linea_critica"],
            0.0, places=10,
        )

    def test_activar_coherencia_global_supera_umbral(self):
        """coherencia_global['supera_umbral'] debe ser True."""
        self.assertTrue(self.resultado["coherencia_global"]["supera_umbral"])

    def test_generar_sello(self):
        """generar_sello() debe retornar '∴PCC∞³'."""
        self.assertEqual(self.sistema.generar_sello(), "∴PCC∞³")


# ============================================================================
# TestAPIPublica – 10 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la API pública particula_coherencia_pc_activar()."""

    def setUp(self):
        self.resultado = particula_coherencia_pc_activar()

    def test_api_returns_dict(self):
        """particula_coherencia_pc_activar() debe retornar un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_api_psi_global_above_umbral(self):
        """psi_global ≥ PSI_UMBRAL (0.888)."""
        self.assertGreaterEqual(self.resultado["psi_global"], PSI_UMBRAL)

    def test_api_sello(self):
        """Sello debe ser '∴PCC∞³'."""
        self.assertEqual(self.resultado["sello"], "∴PCC∞³")

    def test_api_valido(self):
        """valido debe ser True."""
        self.assertTrue(self.resultado["valido"])

    def test_api_exito(self):
        """exito debe ser True."""
        self.assertTrue(self.resultado["exito"])

    def test_api_estado_activa(self):
        """estado debe ser 'PARTICULA-COHERENCIA-PC-ACTIVA'."""
        self.assertEqual(self.resultado["estado"], "PARTICULA-COHERENCIA-PC-ACTIVA")

    def test_api_constantes_present(self):
        """constantes debe ser un dict con 'F0'."""
        self.assertIsInstance(self.resultado["constantes"], dict)
        self.assertIn("F0", self.resultado["constantes"])

    def test_api_subsistemas_count(self):
        """subsistemas debe tener 5 subsistemas."""
        self.assertEqual(len(self.resultado["subsistemas"]), 5)

    def test_api_idempotente(self):
        """Dos llamadas consecutivas deben retornar Ψ_global idéntico."""
        r1 = particula_coherencia_pc_activar()
        r2 = particula_coherencia_pc_activar()
        self.assertAlmostEqual(r1["psi_global"], r2["psi_global"], places=6)

    def test_api_wrapper_instancia(self):
        """wrapper particula_coherencia_pc_activar() de instancia debe coincidir."""
        sistema = SistemaParticulaCoherencia()
        r_activar = sistema.activar()
        r_wrapper = sistema.particula_coherencia_pc_activar()
        self.assertEqual(r_activar["psi_global"], r_wrapper["psi_global"])


if __name__ == "__main__":
    unittest.main()
